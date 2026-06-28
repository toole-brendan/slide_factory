#!/usr/bin/env python3
"""Pull the DDG-51 (Arleigh Burke) MYP recompete-chain prime contracts from
SAM.gov Contract Awards -- the complete FPDS-replacement feed -- to provenance the
awards-methodology slide 02 ("Recompete Cadence") example.

Why SAM Contract Awards (not USAspending): it carries the full FPDS-native field
set -- contracting authority, competition, pricing, the multiyear flag, the §7
dollar trio, contracting office -- and is the authoritative FPDS-lineage source
(Federal_Awards_API_HowTo.md §4, §7). The ONE field it does not carry is the
Treasury Account Symbol (File-C, USAspending /awards/funding/) -- see the
companion TAS pull if the appropriation tie-back is needed.

Per project rule the RAW tier keeps full native mod-level records. A tidy
per-vehicle provenance table (ddg_myp_fields.{json,csv}) is derived for the slide.

Idempotent / resumable: a PIID is skipped+reloaded if its raw file exists.
Run:  python3 pull_ddg_myp_sam.py            # all PIIDs
      python3 pull_ddg_myp_sam.py 2          # first 2 (smoke)
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlencode

# Reuse the proven SAM client (IPv4 force, key from root .env, bounded retry, 429 halt).
SCRIPTS = ("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/"
           "awards_methodology/saronic_specific_awards_data/research/contracts/scripts")
sys.path.insert(0, SCRIPTS)
from _common import env, http_get, write_json, QuotaExhausted  # noqa: E402

CA = "https://api.sam.gov/contract-awards/v1/search"
HERE = Path(__file__).resolve().parent
RAW = HERE / "sam_contract_awards"
EXTRACT = HERE / "extracted"
MAX_PAGES = 60          # 6,000 mods/PIID backstop
PAGE = 100

# DDG-51 prime contracts: the recompete chain (FY13-17 -> FY18-22 -> FY23-27),
# dual-sourced Huntington Ingalls (HII) + Bath Iron Works (BIW), plus the pre-MYP
# FY11 single-ship baseline. N0002423C2305 is a probe (was the FY23-27 BIW award
# captured? -- not present in the shipbuilding pull).
PIIDS = [
    ("N0002411C2307", "Huntington Ingalls", "FY11 single-ship"),
    ("N0002411C2309", "Huntington Ingalls", "FY11 single-ship"),
    ("N0002413C2305", "Bath Iron Works",    "FY13-17 MYP"),
    ("N0002413C2307", "Huntington Ingalls", "FY13-17 MYP"),
    ("N0002418C2305", "Bath Iron Works",    "FY18-22 MYP"),
    ("N0002418C2307", "Huntington Ingalls", "FY18-22 MYP"),
    ("N0002423C2307", "Huntington Ingalls", "FY23-27 MYP"),
    ("N0002423C2305", "Bath Iron Works",    "FY23-27 MYP (probe)"),
]


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def deep(d, *path):
    for k in path:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def find_first(rec, key_lower):
    """First non-null value for any nested key matching key_lower (case-insensitive).
    Returns the .name if the value is a {code,name} object."""
    out = {"v": None}

    def walk(o):
        if out["v"] is not None:
            return
        if isinstance(o, dict):
            for k, v in o.items():
                if k.lower() == key_lower:
                    val = v.get("name") or v.get("code") if isinstance(v, dict) else v
                    if val not in (None, "", "N/A"):
                        out["v"] = val
                        return
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(rec)
    return out["v"]


def pull_piid(piid, key, log):
    path = RAW / f"{piid}.json"
    if path.exists():
        try:
            return json.loads(path.read_text()), "cached"
        except Exception:
            pass
    recs, off, agg, total = [], 0, None, None
    for _ in range(MAX_PAGES):
        url = CA + "?" + urlencode({
            "api_key": key, "piid": piid, "piidAggregation": "yes",
            "includeSections": "contractId,coreData,awardDetails",
            "limit": PAGE, "offset": off})
        txt, st = http_get(url, headers={"Accept": "application/json"})
        if st == 429:
            raise QuotaExhausted("SAM 429 -- daily quota exhausted; resume tomorrow.")
        if not txt or st != 200:
            log(f"  {piid}: HTTP {st} at offset {off} (stopping this PIID)")
            break
        b = json.loads(txt)
        if agg is None:
            agg = b.get("piidAggregation")
        total = int(b.get("totalRecords") or 0)
        raw_page = b.get("awardSummary") or []
        recs.extend(r for r in raw_page if deep(r, "contractId", "piid") == piid)
        # totalRecords is unreliable (returns 0 when piidAggregation=yes) -> stop on a
        # short/empty page, the robust condition (Federal_Awards_API_HowTo.md §5).
        if len(raw_page) < PAGE:
            break
        off += PAGE
        time.sleep(0.3)
    out = {"piid": piid, "totalRecords": total, "n_records": len(recs),
           "piidAggregation": agg, "records": recs}
    write_json(path, out)
    return out, "ok"


def extract(piid, yard, block, data):
    recs = data.get("records") or []
    if not recs:
        return {"piid": piid, "yard": yard, "block": block, "n_mods": 0,
                "award_type": None, "note": "no records returned"}

    def ds(r):
        return (deep(r, "awardDetails", "dates", "dateSigned") or "")

    base = min((r for r in recs if ds(r)), key=ds, default=recs[0])
    core = base.get("coreData") or {}
    det = base.get("awardDetails") or {}
    acq = core.get("acquisitionData") or {}
    comp = core.get("competitionInformation") or {}
    fo = deep(core, "federalOrganization", "contractingInformation", "contractingOffice") or {}
    funo = deep(core, "federalOrganization", "fundingInformation", "fundingOffice") or {}
    dates = det.get("dates") or {}
    naics = deep(core, "productOrServiceInformation", "principalNaics")
    naics_code = (naics[0].get("code") if isinstance(naics, list) and naics else None)

    # §7 money: cumulative + ceiling are restated snapshots -> max across mods.
    cum = max((_f(deep(r, "awardDetails", "totalContractDollars", "totalActionObligation")) or 0) for r in recs)
    ceil = max((_f(deep(r, "awardDetails", "totalContractDollars", "totalBaseAndAllOptionsValue")) or 0) for r in recs)
    bexo = max((_f(deep(r, "awardDetails", "totalContractDollars", "totalBaseAndExercisedOptionsValue")) or 0) for r in recs)
    # the ONLY summable field: per-mod actionObligation -> realized obligation + FY series.
    permod = [(ds(r)[:10], _f(deep(r, "awardDetails", "dollars", "actionObligation")) or 0.0) for r in recs]
    sum_obl = sum(v for _, v in permod)
    by_fy = defaultdict(float)
    for d, v in permod:
        if d:
            by_fy[d[:4]] += v
    signed = sorted(d for d, _ in permod if d)

    return {
        "piid": piid, "yard": yard, "block": block,
        # --- contracting authority ---
        "award_type": deep(core, "awardOrIDVType", "name"),
        "multiyear_contract": find_first(base, "multiyearcontract"),
        "type_of_contract_pricing": deep(acq, "typeOfContractPricing", "name"),
        "type_of_idc": deep(acq, "typeOfIdc", "code"),
        "extent_competed": deep(comp, "extentCompeted", "name"),
        "solicitation_procedures": deep(comp, "solicitationProcedures", "name"),
        "number_of_offers": find_first(base, "numberofoffersreceived"),
        "solicitation_id": core.get("solicitationId"),
        "contracting_office": (f"{fo.get('code','')} {fo.get('name','')}").strip() or None,
        "funding_office": (f"{funo.get('code','')} {funo.get('name','')}").strip() or None,
        "psc": deep(core, "productOrServiceInformation", "productOrService", "code"),
        "naics": naics_code,
        "description": deep(det, "productOrServiceInformation", "descriptionOfContractRequirement"),
        # --- dates ---
        "original_date_signed": signed[0] if signed else None,
        "last_action_date": signed[-1] if signed else None,
        "pop_start": (dates.get("periodOfPerformanceStartDate") or "")[:10] or None,
        "current_completion": (dates.get("currentCompletionDate") or "")[:10] or None,
        "ultimate_completion": (dates.get("ultimateCompletionDate") or "")[:10] or None,
        "last_date_to_order": dates.get("lastDateToOrder"),       # None for a definitive contract
        # --- §7 dollar universes (never blend) ---
        "obligated_cumulative_$m": round(cum / 1e6, 1),           # restated snapshot (measure #2)
        "obligated_summed_permod_$m": round(sum_obl / 1e6, 1),    # Σ per-mod = realized spend (measure #1)
        "ceiling_base_and_all_options_$m": round(ceil / 1e6, 1),  # capacity (measure #3)
        "base_and_exercised_options_$m": round(bexo / 1e6, 1),
        # --- structure ---
        "n_mods": len(recs),
        "family_count": deep(data, "piidAggregation", "awardFamilySummary", "count"),
        "obligation_by_fy_$m": {k: round(v / 1e6, 1) for k, v in sorted(by_fy.items())},
    }


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    EXTRACT.mkdir(parents=True, exist_ok=True)
    (HERE / "pull_logs").mkdir(parents=True, exist_ok=True)
    logf = open(HERE / "pull_logs" / "ddg_myp_sam.log", "w")

    def log(m):
        print(m, flush=True)
        logf.write(m + "\n")
        logf.flush()

    key = env("SAM_API_KEY")
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    targets = PIIDS[:limit] if limit else PIIDS
    log(f"=== DDG-51 MYP SAM Contract Awards pull {time.strftime('%Y-%m-%d %H:%M:%S')} "
        f"({len(targets)} PIIDs) ===")

    rows = []
    try:
        for piid, yard, block in targets:
            data, stat = pull_piid(piid, key, log)
            row = extract(piid, yard, block, data)
            rows.append(row)
            log(f"  {piid}  {yard:20s} {block:22s} type={row.get('award_type')} "
                f"mods={row['n_mods']:>4} total={data.get('totalRecords')} "
                f"oblig=${row.get('obligated_cumulative_$m')}M ceil=${row.get('ceiling_base_and_all_options_$m')}M "
                f"MYP={row.get('multiyear_contract')} [{stat}]")
    except QuotaExhausted as e:
        log(f"!! {e}")

    write_json(EXTRACT / "ddg_myp_fields.json", rows)
    cols = ["piid", "yard", "block", "award_type", "multiyear_contract",
            "type_of_contract_pricing", "extent_competed", "solicitation_procedures",
            "number_of_offers", "contracting_office", "original_date_signed",
            "current_completion", "ultimate_completion", "last_date_to_order",
            "obligated_cumulative_$m", "obligated_summed_permod_$m",
            "ceiling_base_and_all_options_$m", "n_mods", "family_count"]
    with open(EXTRACT / "ddg_myp_fields.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    log(f"\n=== done. {len(rows)} vehicles -> extracted/ddg_myp_fields.(json|csv); "
        f"raw -> sam_contract_awards/<PIID>.json ===")
    logf.close()


if __name__ == "__main__":
    main()
