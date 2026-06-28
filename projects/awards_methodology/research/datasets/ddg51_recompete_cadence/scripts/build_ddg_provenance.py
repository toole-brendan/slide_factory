#!/usr/bin/env python3
"""Build the comprehensive DDG-51 MYP recompete-chain provenance CSV for the
awards-methodology slide 02 ("Recompete Cadence").

Two authoritative sources, merged per the API how-to (Federal_Awards_API_HowTo.md):
  - SAM.gov Contract Awards (already pulled by pull_ddg_myp_sam.py): the FPDS-native
    authority detail -- contracting office, type-of-IDC, family count.
  - USAspending (here, key-free, paginates correctly): the original award date, the
    §7 dollar measures (exact, matching the program-of-record), the per-mod
    transaction series -> obligation by fiscal year, AND the TAS appropriation
    tie-back (federal_account) -- the one field SAM does NOT carry (File-C).

Outputs (all under extracted/):
  - ddg_myp_recompete_provenance.csv   one wide row per vehicle: EVERY field
  - ddg_myp_obligation_by_fy.csv       long: piid x fiscal_year x obligated_$m
  - ddg_myp_provenance.json            the merged records
Raw USAspending kept under usaspending_raw/{detail,transactions,funding}/.

Run:  python3 build_ddg_provenance.py
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time
import urllib.parse
from collections import defaultdict
from pathlib import Path

SCRIPTS = ("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/"
           "awards_methodology/saronic_specific_awards_data/research/contracts/scripts")
sys.path.insert(0, SCRIPTS)
from _common import http_get, http_post_json, write_json  # noqa: E402

HERE = Path(__file__).resolve().parent
RAW = HERE / "usaspending_raw"
EXTRACT = HERE / "extracted"
AWARD_URL = "https://api.usaspending.gov/api/v2/awards/{gid}/"
TXN_URL = "https://api.usaspending.gov/api/v2/transactions/"
FUND_URL = "https://api.usaspending.gov/api/v2/awards/funding/"

# Same chain as the SAM pull; gid = CONT_AWD_{PIID}_9700_-NONE-_-NONE- (definitive
# contracts, no parent IDV), confirmed reachable on USAspending.
PIIDS = [
    ("N0002411C2307", "Huntington Ingalls", "FY11 single-ship"),
    ("N0002411C2309", "Huntington Ingalls", "FY11 single-ship"),
    ("N0002413C2305", "Bath Iron Works",    "FY13-17 MYP"),
    ("N0002413C2307", "Huntington Ingalls", "FY13-17 MYP"),
    ("N0002418C2305", "Bath Iron Works",    "FY18-22 MYP"),
    ("N0002418C2307", "Huntington Ingalls", "FY18-22 MYP"),
    ("N0002423C2307", "Huntington Ingalls", "FY23-27 MYP"),
    ("N0002423C2305", "Bath Iron Works",    "FY23-27 MYP"),
]


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def fed_fy(date_str):
    """US federal fiscal year from an ISO action_date (FY starts 1 Oct)."""
    if not date_str or len(date_str) < 7:
        return None
    y, m = int(date_str[:4]), int(date_str[5:7])
    return y + 1 if m >= 10 else y


def get_detail(gid):
    p = RAW / "detail" / f"{gid}.json"
    if p.exists():
        return json.loads(p.read_text())
    txt, st = http_get(AWARD_URL.format(gid=urllib.parse.quote(gid)))
    if st != 200 or not txt:
        return None
    d = json.loads(txt)
    write_json(p, d)
    return d


def get_paged(url, gid, sort, sub):
    p = RAW / sub / f"{gid}.json"
    if p.exists():
        return json.loads(p.read_text()).get("results", [])
    out, page = [], 1
    while page <= 100:
        body = {"award_id": gid, "page": page, "limit": 100, "sort": sort, "order": "asc"}
        data, st = http_post_json(url, body)
        if not data or st != 200:
            break
        res = data.get("results", [])
        out.extend(res)
        if not res or not (data.get("page_metadata") or {}).get("hasNext"):
            break
        page += 1
        time.sleep(0.1)
    write_json(p, {"award_id": gid, "count": len(out), "results": out})
    return out


def main():
    for d in (RAW / "detail", RAW / "transactions", RAW / "funding", EXTRACT):
        d.mkdir(parents=True, exist_ok=True)

    sam = {r["piid"]: r for r in json.loads((EXTRACT / "ddg_myp_fields.json").read_text())}

    rows, fy_rows = [], []
    for piid, yard, block in PIIDS:
        gid = f"CONT_AWD_{piid}_9700_-NONE-_-NONE-"
        d = get_detail(gid)
        if not d:
            print(f"  {piid}: USAspending detail 404 (gid {gid}) -- SAM-only row")
            d = {}
        txns = get_paged(TXN_URL, gid, "action_date", "transactions")
        funding = get_paged(FUND_URL, gid, "reporting_fiscal_date", "funding")
        time.sleep(0.1)

        pop = d.get("period_of_performance") or {}
        ltc = d.get("latest_transaction_contract_data") or {}
        s = sam.get(piid, {})

        permod = [(t.get("action_date"), _f(t.get("federal_action_obligation")) or 0.0) for t in txns]
        sum_obl = sum(v for _, v in permod)
        dates = sorted(dt for dt, _ in permod if dt)
        by_fy = defaultdict(float)
        for dt, v in permod:
            fy = fed_fy(dt)
            if fy:
                by_fy[fy] += v
        for fy in sorted(by_fy):
            fy_rows.append({"piid": piid, "yard": yard, "block": block,
                            "fiscal_year": f"FY{fy}", "obligated_$m": round(by_fy[fy] / 1e6, 2)})

        tas = sorted({f.get("federal_account") for f in funding if f.get("federal_account")})
        tas_titles = sorted({f.get("account_title") for f in funding if f.get("account_title")})

        rows.append({
            "piid": piid, "yard": yard, "block": block,
            # ---- contracting authority (FPDS-native) ----
            "award_type": d.get("type_description") or s.get("award_type"),
            "multiyear_contract": ltc.get("multi_year_contract") or ltc.get("multi_year") or s.get("multiyear_contract"),
            "type_of_contract_pricing": ltc.get("type_of_contract_pricing_description") or s.get("type_of_contract_pricing"),
            "extent_competed": ltc.get("extent_competed_description") or s.get("extent_competed"),
            "solicitation_procedures": ltc.get("solicitation_procedures_description") or s.get("solicitation_procedures"),
            "number_of_offers": ltc.get("number_of_offers_received") or s.get("number_of_offers"),
            "solicitation_id": ltc.get("solicitation_identifier") or s.get("solicitation_id"),
            "contracting_office": s.get("contracting_office"),     # SAM: clean office name
            "funding_office": s.get("funding_office"),
            "type_of_idc": s.get("type_of_idc"),
            # ---- classification ----
            "psc": (d.get("psc_hierarchy") or {}).get("base_code", {}).get("code") or s.get("psc"),
            "naics": (d.get("naics_hierarchy") or {}).get("base_code", {}).get("code") or s.get("naics"),
            "description": (d.get("latest_transaction_contract_data") or {}).get("description") or s.get("description"),
            # ---- dates ----
            "original_date_signed": d.get("date_signed") or (dates[0] if dates else None),
            "pop_start": pop.get("start_date"),
            "pop_current_end": pop.get("end_date"),
            "pop_potential_end": (pop.get("potential_end_date") or "")[:10] or None,
            "current_completion": s.get("current_completion"),
            "ultimate_completion": s.get("ultimate_completion"),
            "last_date_to_order": s.get("last_date_to_order"),     # None for definitive contracts
            "first_action_date": dates[0] if dates else None,
            "last_action_date": dates[-1] if dates else None,
            # ---- §7 dollar measures (never blend) ----
            "obligated_total_to_date_$m": round((_f(d.get("total_obligation")) or 0) / 1e6, 1),     # cumulative realized
            "obligated_summed_permod_$m": round(sum_obl / 1e6, 1),                                   # Σ transactions (cross-check)
            "base_exercised_options_$m": round((_f(d.get("base_exercised_options")) or 0) / 1e6, 1),  # current value
            "ceiling_base_and_all_options_$m": round((_f(d.get("base_and_all_options")) or 0) / 1e6, 1),  # capacity
            # ---- structure ----
            "n_transactions": len(txns),
            "n_mods_sam_latest": s.get("n_mods"),
            "family_count": s.get("family_count"),
            # ---- appropriation tie-back (TAS) ----
            "tas_federal_accounts": "; ".join(tas),
            "tas_account_titles": "; ".join(tas_titles),
            "n_funding_rows": len(funding),
        })
        print(f"  {piid} {yard:20s} {block:16s} signed={rows[-1]['original_date_signed']} "
              f"oblig=${rows[-1]['obligated_total_to_date_$m']}M ceil=${rows[-1]['ceiling_base_and_all_options_$m']}M "
              f"txns={len(txns)} TAS={tas} MYP={rows[-1]['multiyear_contract']}")

    write_json(EXTRACT / "ddg_myp_provenance.json", rows)
    cols = list(rows[0].keys())
    with open(EXTRACT / "ddg_myp_recompete_provenance.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    with open(EXTRACT / "ddg_myp_obligation_by_fy.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["piid", "yard", "block", "fiscal_year", "obligated_$m"])
        w.writeheader()
        w.writerows(fy_rows)
    print(f"\n=== done. {len(rows)} vehicles -> extracted/ddg_myp_recompete_provenance.csv "
          f"({len(cols)} cols); {len(fy_rows)} vehicle-FY rows -> ddg_myp_obligation_by_fy.csv ===")


if __name__ == "__main__":
    main()
