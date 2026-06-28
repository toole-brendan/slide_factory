#!/usr/bin/env python3
"""STAGE 2 - DETAIL. For every in-scope award discovered in Stage 1, pull the
three USAspending award sub-resources that carry the contract-layer facts:

  A. /api/v2/awards/{generated_internal_id}/   award detail  -> detail/<gid>.json
       current/ceiling value, dates (recompete radar), incumbent + UEI, parent
       IDV linkage, competition route, NAICS/PSC.
  B. /api/v2/transactions/  (POST, paged)      per-mod actions -> transactions/<gid>.json
       one row per modification. `federal_action_obligation` is THE per-mod
       obligation -> this is the ONLY money we sum (award_actions table, gotcha:
       never sum a cumulative/ceiling field across mods).
  C. /api/v2/awards/funding/ (POST, paged)     File-C account funding -> funding/<gid>.json
       Treasury Account Symbol (`federal_account`, e.g. 021-2035 = Other
       Procurement, Army) + program activity + object class -> the budget-layer
       TIE-BACK (TAS -> appropriation / PE / BLI). Not every award reports File C
       (recent awards & IDV task orders often report under the parent) -> 0 rows
       is normal, not an error.

Per project rule the RAW tier keeps FULL native records (every field). A thin
per-award index (`_detail_index.json`) + a distinct-vendor roster (`_vendors.json`)
are written as SEEDS for Stage 3 (FPDS by VENDOR_NAME) / Stage 6 (SAM Entity by
UEI) / the aggregate + recompete-radar steps.

Idempotent & RESUMABLE: a resource is skipped (and reloaded) if its JSON file
already exists, so the pull can be chunked or resumed after an interruption; only
missing/previously-failed resources are re-fetched. Seeds are processed in
descending award amount so a partial run still captures the material awards.

Run:  python3 pull_usaspending_detail.py            # all in-scope seeds
      python3 pull_usaspending_detail.py 25         # first 25 (smoke)

Agency-name note: scoping/joins here key off generated_internal_id, PIID, UEI and
TAS codes — never the toptier DoD name — so this pull is immune to the
"Department of Defense" -> "Department of War" rename (see memory).
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import http_get, http_post_json, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]            # research/contracts/
RAW = ROOT / "usaspending_raw"
DETAIL_DIR = RAW / "detail"
TXN_DIR = RAW / "transactions"
FUND_DIR = RAW / "funding"
EXTRACT = ROOT / "extracted"
SEEDS = EXTRACT / "_discovered_piids.json"
INDEX = EXTRACT / "_detail_index.json"
VENDORS = EXTRACT / "_vendors.json"
LOG = ROOT / "pull_logs" / "usaspending_detail.log"

AWARD_URL = "https://api.usaspending.gov/api/v2/awards/{gid}/"
TXN_URL = "https://api.usaspending.gov/api/v2/transactions/"
FUND_URL = "https://api.usaspending.gov/api/v2/awards/funding/"
PAGE_SIZE = 100
MAX_PAGES = 100          # 10k rows/award is far beyond any real award; pure backstop
SLEEP_AWARD = 0.12       # politeness between awards
SLEEP_PAGE = 0.1


def safe(gid: str) -> str:
    return "".join(c if (c.isalnum() or c in "._-") else "_" for c in gid)


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load_or_fetch_detail(gid: str):
    """Return (detail_dict, status_str). 'cached' if read from disk."""
    path = DETAIL_DIR / f"{safe(gid)}.json"
    if path.exists():
        try:
            return json.loads(path.read_text()), "cached"
        except Exception:
            pass  # corrupt -> refetch
    url = AWARD_URL.format(gid=urllib.parse.quote(gid))
    txt, status = http_get(url)
    if status != 200 or not txt:
        return None, f"http {status}"
    try:
        d = json.loads(txt)
    except Exception:
        return None, "bad json"
    write_json(path, d)
    return d, "ok"


def load_or_fetch_paged(url: str, gid: str, sort: str, out_dir: Path):
    """POST-paginate an award sub-resource (transactions / funding). Returns
    (results_list, status_str). Skips+loads if the file already exists."""
    path = out_dir / f"{safe(gid)}.json"
    if path.exists():
        try:
            return json.loads(path.read_text()).get("results", []), "cached"
        except Exception:
            pass
    out, page, status = [], 1, None
    while page <= MAX_PAGES:
        body = {"award_id": gid, "page": page, "limit": PAGE_SIZE,
                "sort": sort, "order": "asc"}
        data, status = http_post_json(url, body)
        if data is None or status != 200:
            return None, f"http {status}"          # don't persist partials
        res = data.get("results", [])
        out.extend(res)
        md = data.get("page_metadata") or {}
        if not res or not md.get("hasNext"):
            break
        page += 1
        time.sleep(SLEEP_PAGE)
    write_json(path, {"award_id": gid, "count": len(out), "results": out})
    return out, "ok"


def index_entry(seed: dict, detail: dict, txns: list, funding: list) -> dict:
    """Flatten the load-bearing fields into a thin per-award index row. RAW files
    keep everything; this is the navigable seed for downstream stages."""
    d = detail or {}
    rec = d.get("recipient") or {}
    pop = d.get("period_of_performance") or {}
    ltc = d.get("latest_transaction_contract_data") or {}
    parent = d.get("parent_award") or {}
    naics = (d.get("naics_hierarchy") or {}).get("base_code") or {}
    psc = (d.get("psc_hierarchy") or {}).get("base_code") or {}

    # award_actions money: the per-mod obligation is the ONLY thing we sum.
    sum_obl = sum(o for o in (_num(t.get("federal_action_obligation")) for t in txns) if o)
    action_dates = sorted(t.get("action_date") for t in txns if t.get("action_date"))

    tas = sorted({f.get("federal_account") for f in funding if f.get("federal_account")})
    tas_titles = sorted({f.get("account_title") for f in funding if f.get("account_title")})
    fund_obl = sum(o for o in (_num(f.get("transaction_obligated_amount")) for f in funding) if o)

    return {
        "generated_internal_id": seed.get("generated_internal_id"),
        "piid": d.get("piid") or seed.get("piid"),
        "award_type": d.get("type"),
        "award_type_description": d.get("type_description"),
        "category": d.get("category"),
        # incumbent
        "recipient_name": rec.get("recipient_name") or seed.get("recipient"),
        "recipient_uei": rec.get("recipient_uei"),
        "recipient_duns": rec.get("recipient_unique_id"),
        "parent_recipient_name": rec.get("parent_recipient_name"),
        # parent IDV (contract_family / recompete)
        "parent_idv_gid": parent.get("generated_unique_award_id"),
        "parent_idv_piid": parent.get("piid"),
        "idv_type_description": parent.get("idv_type_description"),
        "single_or_multiple_award": parent.get("multiple_or_single_aw_desc"),
        # money (amount_type discipline): seed amount, ceiling, exercised, obligation
        "award_amount_seed": seed.get("award_amount"),
        "total_obligation": _num(d.get("total_obligation")),
        "base_and_all_options": _num(d.get("base_and_all_options")),      # ceiling
        "base_exercised_options": _num(d.get("base_exercised_options")),  # current value
        "total_outlay": _num(d.get("total_outlay")),
        "sum_federal_action_obligation": round(sum_obl, 2),               # =sum(award_actions)
        "subaward_count": d.get("subaward_count"),
        "total_subaward_amount": _num(d.get("total_subaward_amount")),
        # timing -> recompete radar
        "date_signed": d.get("date_signed"),
        "pop_start_date": pop.get("start_date"),
        "pop_current_end_date": pop.get("end_date"),
        "pop_potential_end_date": pop.get("potential_end_date"),
        "n_transactions": len(txns),
        "first_action_date": action_dates[0] if action_dates else None,
        "last_action_date": action_dates[-1] if action_dates else None,
        # competitive route
        "extent_competed": ltc.get("extent_competed"),
        "extent_competed_description": ltc.get("extent_competed_description"),
        "solicitation_procedures_description": ltc.get("solicitation_procedures_description"),
        "fair_opportunity_limited": ltc.get("fair_opportunity_limited"),
        "number_of_offers_received": ltc.get("number_of_offers_received"),
        # solicitation identity -> bridge to the SAM Opportunities baseline (dark-award match)
        "solicitation_identifier": ltc.get("solicitation_identifier"),
        # classification
        "naics_code": naics.get("code"),
        "naics_description": naics.get("description"),
        "psc_code": psc.get("code"),
        "psc_description": psc.get("description"),
        "matched_axes": seed.get("matched_axes"),
        # budget tie-back (TAS -> appropriation/PE/BLI handled at aggregate time)
        "n_funding_rows": len(funding),
        "has_tas": bool(tas),
        "funding_federal_accounts": tas,
        "funding_account_titles": tas_titles,
        "funding_sum_obligated": round(fund_obl, 2),
    }


def main():
    for d in (DETAIL_DIR, TXN_DIR, FUND_DIR, EXTRACT, LOG.parent):
        d.mkdir(parents=True, exist_ok=True)
    logf = open(LOG, "w")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    seeds = json.loads(SEEDS.read_text())
    seeds.sort(key=lambda s: -(s.get("award_amount") or 0))   # material awards first
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    if limit:
        seeds = seeds[:limit]

    log(f"=== USAspending detail (Stage 2) {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"seeds={len(seeds)}  (resumable: existing resource files are reused)")

    index, fail = [], []
    counts = {"detail_ok": 0, "detail_cached": 0, "detail_fail": 0,
              "txn_fail": 0, "fund_fail": 0, "with_tas": 0}

    for i, seed in enumerate(seeds, 1):
        gid = seed.get("generated_internal_id")
        if not gid:
            continue
        detail, dstat = load_or_fetch_detail(gid)
        if detail is None:
            counts["detail_fail"] += 1
            fail.append({"gid": gid, "stage": "detail", "status": dstat})
            log(f"  [{i}/{len(seeds)}] DETAIL FAIL {dstat}: {gid}")
            time.sleep(SLEEP_AWARD)
            continue
        counts["detail_cached" if dstat == "cached" else "detail_ok"] += 1

        txns, tstat = load_or_fetch_paged(TXN_URL, gid, "action_date", TXN_DIR)
        if txns is None:
            counts["txn_fail"] += 1
            fail.append({"gid": gid, "stage": "transactions", "status": tstat})
            txns = []
        funding, fstat = load_or_fetch_paged(FUND_URL, gid, "reporting_fiscal_date", FUND_DIR)
        if funding is None:
            counts["fund_fail"] += 1
            fail.append({"gid": gid, "stage": "funding", "status": fstat})
            funding = []

        entry = index_entry(seed, detail, txns, funding)
        if entry["has_tas"]:
            counts["with_tas"] += 1
        index.append(entry)

        if i % 100 == 0 or i == len(seeds):
            log(f"  [{i}/{len(seeds)}] {gid[:46]:46s} "
                f"mods={entry['n_transactions']:>3} tas={len(entry['funding_federal_accounts'])} "
                f"d={dstat}/{tstat}/{fstat}")
        if dstat != "cached" or tstat != "cached" or fstat != "cached":
            time.sleep(SLEEP_AWARD)

    # ---- distinct-vendor roster (seed for Stage 3 FPDS / Stage 6 SAM Entity) ----
    vendors = {}
    for e in index:
        name = e["recipient_name"]
        if not name:
            continue
        v = vendors.setdefault(name, {"recipient_name": name, "recipient_uei": e["recipient_uei"],
                                      "n_awards": 0, "total_obligation": 0.0, "piids": []})
        v["n_awards"] += 1
        v["total_obligation"] += (e["total_obligation"] or 0.0)
        if e["piid"]:
            v["piids"].append(e["piid"])
        if not v["recipient_uei"] and e["recipient_uei"]:
            v["recipient_uei"] = e["recipient_uei"]
    vendor_list = sorted(vendors.values(), key=lambda v: -v["total_obligation"])
    for v in vendor_list:
        v["total_obligation"] = round(v["total_obligation"], 2)

    index.sort(key=lambda e: -(e["total_obligation"] or 0))
    write_json(INDEX, index)
    write_json(VENDORS, vendor_list)
    if fail:
        write_json(EXTRACT / "_detail_failures.json", fail)

    log(f"\n=== done. {len(index)} awards indexed; "
        f"detail ok={counts['detail_ok']} cached={counts['detail_cached']} fail={counts['detail_fail']}; "
        f"txn_fail={counts['txn_fail']} fund_fail={counts['fund_fail']}; "
        f"{counts['with_tas']} awards with TAS tie-back; {len(vendor_list)} distinct vendors.")
    if fail:
        log(f"    {len(fail)} resource failures -> _detail_failures.json (re-run to retry; cached resources are skipped)")
    log("\nTop 15 vendors by summed total_obligation:")
    for v in vendor_list[:15]:
        log(f"  ${v['total_obligation']/1e6:>9,.1f}M  {v['n_awards']:>3} awards  "
            f"{(v['recipient_uei'] or '-'):12s}  {v['recipient_name'][:44]}")
    logf.close()


if __name__ == "__main__":
    main()
