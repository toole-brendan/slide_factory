#!/usr/bin/env python3
"""WIDENED US-NAVY DISCOVERY — Saronic addressable market beyond maritime/small-craft.

Re-scopes pull_usaspending_discovery.py to the full Department of the Navy (EXCLUDING
Marine Corps) across the four capability clusters the company is growing into, plus the
core naval-vessel scope and cross-cutting R&D/engineering:

  core      vessels / boats                       NAICS 336611/336612; PSC 1905/1925/1940/1990/2090
  cluster 1 unmanned platforms & autonomy         NAICS 334511; PSC 1550 (+ vessel PSCs above)
  cluster 2 sensors & C5ISR                        NAICS 334511/334220/334290/517410;
                                                   PSC 5841/5845/5865/5826/6605/5820/5895/5810
  cluster 3 mission software & AI                  NAICS 511210/541511/541512; PSC 7030/D302/D399
  cluster 4 effects & weaponization                NAICS 332993/336414; PSC 1410/1336/1055
  x-cutting R&D / engineering services             NAICS 541330/541715

Instrument types are restricted to the three in scope for the recompete methodology:
  standalone definitive contract (D), task/delivery order (C),
  parent IDIQ/MAC/GWAC vehicle (IDV_A GWAC / IDV_B IDC / IDV_C FSS).
Excluded: purchase orders (B), BPA calls (A), BOAs (IDV_D), other IDV (IDV_E), OTs,
Marine Corps (M-prefix DoDAAC), and Saronic itself.

Does NOT touch the maritime corpus — writes only navy_widened_* outputs.
Run:  python3 pull_navy_widened_discovery.py        (full)
      SMOKE=1 python3 pull_navy_widened_discovery.py (2 codes, 2 pages — query/filter test)
"""
from __future__ import annotations

import csv
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import http_post_json, slugify, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "usaspending_raw"
EXTRACT = ROOT / "extracted"
LOG = ROOT / "pull_logs" / "navy_widened_discovery.log"

ENDPOINT = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
TIME_PERIOD = [{"start_date": "2015-01-01", "end_date": "2026-12-31"}]
FIELDS = ["Award ID", "Recipient Name", "Awarding Agency", "Awarding Sub Agency",
          "Funding Agency", "Funding Sub Agency", "Award Amount", "Description",
          "Contract Award Type", "Start Date", "End Date", "NAICS", "PSC"]

# In-scope instrument types only (the three the methodology targets).
CONTRACT_CODES = ["C", "D"]                 # C delivery/task order, D definitive contract
IDV_CODES = ["IDV_A", "IDV_B", "IDV_C"]     # GWAC, IDC/IDIQ, FSS  (exclude BOA/BPA/other)

# Awarding SUBTIER = Department of the Navy (covers Navy + USMC; USMC excluded post-hoc
# by M-prefix DoDAAC). Scoping the code axis to the Navy subtier makes the page cap apply
# WITHIN the Navy so the relevant tail isn't crowded out by the rest of DoD.
NAVY_SUBTIER = [{"type": "awarding", "tier": "subtier", "name": "Department of the Navy"}]

# Widened capability scope (core vessels + 4 clusters + x-cutting R&D).
CODE_QUERIES = [
    # core vessels
    ("naics", "336611"), ("naics", "336612"),
    ("psc", "1905"), ("psc", "1925"), ("psc", "1940"), ("psc", "1990"), ("psc", "2090"),
    # cluster 1 — unmanned platforms & autonomy
    ("naics", "334511"), ("psc", "1550"),
    # cluster 2 — sensors & C5ISR
    ("naics", "334220"), ("naics", "334290"), ("naics", "517410"),
    ("psc", "5841"), ("psc", "5845"), ("psc", "5865"), ("psc", "5826"),
    ("psc", "6605"), ("psc", "5820"), ("psc", "5895"), ("psc", "5810"),
    # cluster 3 — mission software & AI
    ("naics", "511210"), ("naics", "541511"), ("naics", "541512"),
    ("psc", "7030"), ("psc", "D302"), ("psc", "D399"),
    # cluster 4 — effects & weaponization
    ("naics", "332993"), ("naics", "336414"),
    ("psc", "1410"), ("psc", "1336"), ("psc", "1055"),
    # x-cutting R&D / engineering
    ("naics", "541330"), ("naics", "541715"),
]

PAGE_SIZE = 100
CODE_MAX_PAGES = 8

if os.environ.get("SMOKE"):
    CODE_QUERIES = [("naics", "334511"), ("psc", "1905")]
    CODE_MAX_PAGES = 2


def usmc(piid: str) -> bool:
    return (piid or "").upper().startswith("M")


def saronic(name: str) -> bool:
    return "SARONIC" in (name or "").upper()


def run_query(label, base_filters, log):
    out = []
    for grp_name, codes in (("contract", CONTRACT_CODES), ("idv", IDV_CODES)):
        filters = dict(base_filters)
        filters["time_period"] = TIME_PERIOD
        filters["award_type_codes"] = codes
        page = 1
        grp = []
        while page <= CODE_MAX_PAGES:
            body = {"filters": filters, "fields": FIELDS, "sort": "Award Amount",
                    "order": "desc", "limit": PAGE_SIZE, "page": page}
            data, status = http_post_json(ENDPOINT, body)
            if data is None or status != 200:
                detail = (data or {}).get("detail") or (data or {}).get("messages") or status
                log(f"      [{grp_name}] page {page}: HTTP {status}: {str(detail)[:160]}")
                break
            results = data.get("results", [])
            for r in results:
                r["_matched_query"] = label
                r["_award_type_group"] = grp_name
            grp.extend(results)
            if not results or not (data.get("page_metadata") or {}).get("hasNext", False):
                break
            page += 1
            time.sleep(0.25)
        log(f"      [{grp_name}] {len(grp)} records")
        write_json(RAW / f"widened_{slugify(label)}_{grp_name}.json",
                   {"label": label, "award_type_group": grp_name, "record_count": len(grp),
                    "results": grp})
        out.extend(grp)
    return out


def main():
    EXTRACT.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    logf = open(LOG, "w")

    def log(msg):
        print(msg, flush=True); logf.write(msg + "\n"); logf.flush()

    log(f"=== widened Navy discovery {time.strftime('%Y-%m-%d %H:%M:%S')}  "
        f"({len(CODE_QUERIES)} codes, {CODE_MAX_PAGES} pages, instruments={CONTRACT_CODES}+{IDV_CODES})")
    all_records = []
    for kind, code in CODE_QUERIES:
        label = f"{kind}:{code}"
        log(f"  - {label}")
        filt = {"agencies": NAVY_SUBTIER, f"{kind}_codes": [code]}
        all_records.extend(run_query(label, filt, log))

    # consolidate by generated_internal_id; union the code provenance
    by_id = {}
    for r in all_records:
        gid = r.get("generated_internal_id") or r.get("Award ID")
        if not gid:
            continue
        cur = by_id.get(gid)
        if cur is None:
            r["_axes"] = {r.get("_matched_query")}
            by_id[gid] = r
        else:
            cur["_axes"].add(r.get("_matched_query"))

    rows = []
    for gid, r in by_id.items():
        piid = r.get("Award ID")
        name = r.get("Recipient Name")
        excl = "usmc" if usmc(piid) else ("saronic" if saronic(name) else "")
        rows.append({
            "generated_internal_id": gid, "award_id": piid, "recipient_name": name,
            "award_amount": r.get("Award Amount"),
            "contract_award_type": r.get("Contract Award Type"),
            "award_type_group": r.get("_award_type_group"),
            "awarding_sub_agency": r.get("Awarding Sub Agency"),
            "funding_sub_agency": r.get("Funding Sub Agency"),
            "naics": r.get("NAICS"), "psc": r.get("PSC"),
            "start_date": r.get("Start Date"), "end_date": r.get("End Date"),
            "in_scope": "no" if excl else "yes", "excluded": excl,
            "matched_codes": "; ".join(sorted(a for a in r["_axes"] if a)),
            "description": (r.get("Description") or "")[:400],
        })
    rows.sort(key=lambda x: (x["in_scope"] != "yes", -(x["award_amount"] or 0)))

    cols = ["generated_internal_id", "award_id", "recipient_name", "award_amount",
            "contract_award_type", "award_type_group", "awarding_sub_agency",
            "funding_sub_agency", "naics", "psc", "start_date", "end_date",
            "in_scope", "excluded", "matched_codes", "description"]

    def dump(path, only_in):
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
            for row in rows:
                if only_in and row["in_scope"] != "yes":
                    continue
                w.writerow(row)

    dump(EXTRACT / "navy_widened_discovered_all.csv", False)
    dump(EXTRACT / "navy_widened_discovered.csv", True)
    seeds = [{"generated_internal_id": r["generated_internal_id"], "piid": r["award_id"],
              "recipient": r["recipient_name"], "award_amount": r["award_amount"],
              "naics": r["naics"], "psc": r["psc"], "matched_codes": r["matched_codes"]}
             for r in rows if r["in_scope"] == "yes"]
    write_json(EXTRACT / "_navy_widened_piids.json", seeds)

    n_in = sum(1 for r in rows if r["in_scope"] == "yes")
    n_usmc = sum(1 for r in rows if r["excluded"] == "usmc")
    n_sar = sum(1 for r in rows if r["excluded"] == "saronic")
    log(f"\n=== {len(rows)} unique awards | {n_in} in-scope (Navy, non-USMC, non-Saronic) "
        f"| excluded {n_usmc} USMC, {n_sar} Saronic")
    from collections import Counter
    log("by instrument: " + str(dict(Counter(r["contract_award_type"] for r in rows if r["in_scope"] == "yes"))))
    log("top 15 in-scope by amount:")
    for row in [r for r in rows if r["in_scope"] == "yes"][:15]:
        log(f"  ${(row['award_amount'] or 0)/1e6:>9,.1f}M  {(row['award_id'] or '')[:18]:18s}  "
            f"{(row['recipient_name'] or '')[:30]:30s}  {row['matched_codes'][:24]}")
    logf.close()


if __name__ == "__main__":
    main()
