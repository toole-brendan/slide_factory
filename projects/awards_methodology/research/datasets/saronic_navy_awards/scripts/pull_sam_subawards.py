#!/usr/bin/env python3
"""STAGE 4 - FIRST-TIER SUBAWARDS (SAM.gov Acquisition Subaward Reporting API).

For each discovered prime PIID, pull its first-tier (FFATA) subcontract records.
SAM.gov is the upstream FFATA source — no ~2,500/prime cap (unlike USAspending's
subaward endpoint) and clean dedup (`subAwardReportId` is unique). This is where the
"who actually builds the boat under the prime" signal lives -> Platform/Sensors/
Effectors/C2 capability attribution of the subcontractor base.

SAM gotchas baked in (see SAM_GOV_HOWTO.md + army log):
  * Endpoint MUST keep `/prod/`. Param name is lowercase `piid` (uppercase silently
    dropped). VERIFY the filter was honored by checking `nextPageLink` echoes `piid=`.
  * Task orders: also pass `referencedIDVPIID` (+ agency) so piid="0001" doesn't
    paginate every "0001" in the dataset. Both parsed from the generated_internal_id.
  * `pageSize=1000`, zero-indexed `pageNumber`; stop when `nextPageLink` is null.
  * Pull `status=Published` and `status=Deleted` separately (audit trail).
  * Numeric fields are STRINGS (coerce later). Use `subAwardDate` for FY, not
    `submittedDate`. Roll up by `subParentUei`. Don't dedup `subAwardReportId`.
  * 1,000 req/day quota; `_common` traps 429 -> QuotaExhausted and HALTS CLEANLY.
    => PIIDs processed BIGGEST-OBLIGATION-FIRST so a mid-run halt keeps the material
    primes. Resumable: existing per-PIID files are skipped.

Scope control: only primes with USAspending obligation >= floor (default $1M, ~2
calls each). The dropped tail (tiny one-off awards) rarely has FFATA subs. Floor +
cap are LOGGED (never silent). Raise/lower with MIN_OBL / a top-N arg.

Run:  python3 pull_sam_subawards.py                  # all primes >= $1M
      python3 pull_sam_subawards.py 1 W912BU23C0020  # smoke one PIID
      MIN_OBL=5000000 python3 pull_sam_subawards.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import QuotaExhausted, env, http_get, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]            # research/contracts/
RAW = ROOT / "sam_subawards"
EXTRACT = ROOT / "extracted"
INDEX_IN = EXTRACT / "_detail_index.json"             # preferred: has total_obligation
SEEDS_IN = EXTRACT / "_discovered_piids.json"         # fallback if Stage 2 not run yet
INDEX_OUT = EXTRACT / "_subawards_index.json"
LOG = ROOT / "pull_logs" / "sam_subawards.log"

BASE = "https://api.sam.gov/prod/contract/v1/subcontracts/search"
PAGE_SIZE = 1000
MIN_OBL = float(os.environ.get("MIN_OBL", "1000000"))
# Deleted-status records are near-always empty (~1 per 42 PIIDs per SAM_GOV_HOWTO);
# SKIP_DELETED=1 halves the call budget when quota is tight (drops the audit pass).
SKIP_DELETED = os.environ.get("SKIP_DELETED", "") == "1"
SLEEP = 0.35


def parse_gid(gid: str):
    """generated_internal_id -> (piid, agency_id, ref_idv_piid, ref_idv_agency).
    AWD: CONT_AWD_{PIID}_{AG}_{REFIDV}_{REFAG}; IDV: CONT_IDV_{PIID}_{AG}."""
    if not gid:
        return None, None, None, None
    for pre in ("CONT_AWD_", "CONT_IDV_", "ASST_NON_", "ASST_AGG_"):
        if gid.startswith(pre):
            rest = gid[len(pre):].split("_")
            piid = rest[0] if rest else None
            ag = rest[1] if len(rest) > 1 else None
            ref = rest[2] if len(rest) > 2 and rest[2] != "-NONE-" else None
            refag = rest[3] if len(rest) > 3 and rest[3] != "-NONE-" else None
            return piid, ag, ref, refag
    return None, None, None, None


def fetch_status(piid, agency, ref_idv, ref_agency, status, api_key, log):
    """Paginate all subaward records for a PIID under one status. Returns list or
    raises QuotaExhausted (propagated to halt cleanly)."""
    records, page = [], 0
    while True:
        params = {"api_key": api_key, "piid": piid, "pageNumber": page,
                  "pageSize": PAGE_SIZE, "status": status}
        if agency:
            params["agencyId"] = agency
        if ref_idv:
            params["referencedIDVPIID"] = ref_idv
            if ref_agency:
                params["referencedIDVAgencyId"] = ref_agency
        url = f"{BASE}?{urlencode(params)}"
        txt, st = http_get(url, headers={"Accept": "application/json"})
        if txt is None:
            log(f"      [{status}] page {page}: NO RESPONSE (status {st})")
            break
        try:
            body = json.loads(txt)
        except Exception:
            log(f"      [{status}] page {page}: bad JSON")
            break
        data = body.get("data") or []
        records.extend(data)
        nxt = body.get("nextPageLink") or ""
        if page == 0 and data and "piid=" not in nxt:
            # filter-honored check: nextPageLink echoes only recognized filters
            log(f"      [{status}] WARNING: nextPageLink missing piid= -> filter may be dropped: {nxt[:120]}")
        # Stop on the LAST page. NB: SAM returns a non-null nextPageLink even at 0
        # records (it points back to page 0), so "stop when nextPageLink null" loops
        # forever. Authoritative stop = empty page, short page, or totalPages reached.
        total_pages = int(body.get("totalPages") or 0)
        if not data or len(data) < PAGE_SIZE or (total_pages and page + 1 >= total_pages):
            break
        page += 1
        time.sleep(SLEEP)
    return records


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    api_key = env("SAM_API_KEY")
    logf = open(LOG, "w")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    # Build the prime list (prefer the Stage-2 index w/ obligations; else seeds).
    smoke_piid = sys.argv[2] if len(sys.argv) > 2 else None
    if INDEX_IN.exists():
        rows = json.loads(INDEX_IN.read_text())
        primes = [{"gid": r["generated_internal_id"], "piid": r["piid"],
                   "recipient": r["recipient_name"], "oblig": r.get("total_obligation") or 0}
                  for r in rows]
    else:
        rows = json.loads(SEEDS_IN.read_text())
        primes = [{"gid": r["generated_internal_id"], "piid": r["piid"],
                   "recipient": r["recipient"], "oblig": r.get("award_amount") or 0}
                  for r in rows]
    primes.sort(key=lambda p: -(p["oblig"] or 0))

    if smoke_piid:
        primes = [p for p in primes if p["piid"] == smoke_piid][:1]
    else:
        selected = [p for p in primes if (p["oblig"] or 0) >= MIN_OBL]
        dropped = len(primes) - len(selected)
        primes = selected
    top_n = int(sys.argv[1]) if len(sys.argv) > 1 and not smoke_piid else None
    if top_n:
        primes = primes[:top_n]

    log(f"=== SAM subawards (Stage 4) {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"primes selected={len(primes)} (floor=${MIN_OBL/1e6:.1f}M){'' if smoke_piid else f', dropped below floor={dropped}'}")
    log("quota=1000/day entity-role; biggest-obligation-first; resumable (existing files skipped).")

    index = []
    try:
        for i, p in enumerate(primes, 1):
            piid, agency, ref_idv, ref_agency = parse_gid(p["gid"])
            piid = piid or p["piid"]
            out_path = RAW / f"{piid}_{agency or 'NA'}{('_'+ref_idv) if ref_idv else ''}.json"
            if out_path.exists():
                try:
                    prev = json.loads(out_path.read_text())
                    index.append({"piid": piid, "recipient": p["recipient"],
                                  "n_published": len(prev.get("published", [])),
                                  "n_deleted": len(prev.get("deleted", [])),
                                  "oblig": p["oblig"], "cached": True})
                    continue
                except Exception:
                    pass
            pub = fetch_status(piid, agency, ref_idv, ref_agency, "Published", api_key, log)
            det = [] if SKIP_DELETED else fetch_status(piid, agency, ref_idv, ref_agency, "Deleted", api_key, log)
            sub_sum = sum(float(r.get("subAwardAmount") or 0) for r in pub)
            write_json(out_path, {"piid": piid, "agency_id": agency,
                                  "referenced_idv_piid": ref_idv, "recipient": p["recipient"],
                                  "prime_obligation": p["oblig"],
                                  "n_published": len(pub), "n_deleted": len(det),
                                  "sum_subaward_amount": round(sub_sum, 2),
                                  "published": pub, "deleted": det})
            index.append({"piid": piid, "recipient": p["recipient"], "n_published": len(pub),
                          "n_deleted": len(det), "sum_subaward_amount": round(sub_sum, 2),
                          "oblig": p["oblig"], "cached": False})
            if i % 25 == 0 or i == len(primes) or pub:
                log(f"  [{i}/{len(primes)}] {piid:18s} pub={len(pub):>4} del={len(det):>2} "
                    f"subs=${sub_sum/1e6:>7,.1f}M  ({(p['recipient'] or '')[:34]})")
            time.sleep(SLEEP)
    except QuotaExhausted as e:
        log(f"\n!! {e}\n!! Halting; {len(index)} primes done. Re-run after midnight UTC to resume (cached primes skipped).")

    write_json(INDEX_OUT, sorted(index, key=lambda x: -(x.get("sum_subaward_amount") or 0)))
    with_subs = [x for x in index if x["n_published"]]
    grand = sum(x.get("sum_subaward_amount") or 0 for x in index)
    log(f"\n=== done. {len(index)} primes processed; {len(with_subs)} have subawards; "
        f"${grand/1e6:,.1f}M first-tier subaward dollars.")
    for x in sorted(with_subs, key=lambda x: -(x.get('sum_subaward_amount') or 0))[:15]:
        log(f"  ${(x.get('sum_subaward_amount') or 0)/1e6:>8,.1f}M  {x['n_published']:>4} subs  "
            f"{x['piid']:18s}  {(x['recipient'] or '')[:34]}")
    logf.close()


if __name__ == "__main__":
    main()
