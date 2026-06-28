#!/usr/bin/env python3
"""Corroborate the DDG-51 supplier base against SAM.gov Subaward Reporting (the upstream
FFATA source) -- so the subaward layer carries the same SAM-primary provenance as the
prime layer -- and quantify the under-reporting (Bath Iron Works files a fraction of
Huntington Ingalls on the same block).

For each DDG prime PIID: pull first-tier Published subaward records from SAM, sum +
count, and compare to the workbook's reported subaward dollars for that prime.

Run:  python3 pull_ddg_sam_subawards.py
"""
from __future__ import annotations

import csv
import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlencode

SCRIPTS = ("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/"
           "awards_methodology/saronic_specific_awards_data/research/contracts/scripts")
sys.path.insert(0, SCRIPTS)
from _common import env, http_get, write_json, QuotaExhausted  # noqa: E402

BASE = "https://api.sam.gov/prod/contract/v1/subcontracts/search"
WORKBOOK_SUB = ("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/"
                "distributed_shipbuilding/sam/sam_awards_data/workbook_award_classification_refactor/"
                "extracted/ddg_subaward_transactions.csv")
HERE = Path(__file__).resolve().parent
RAW = HERE / "sam_subawards"
EXTRACT = HERE / "extracted"
PAGE_SIZE = 1000

PRIMES = [
    ("N0002413C2307", "Huntington Ingalls", "FY13-17 MYP"),
    ("N0002413C2305", "Bath Iron Works", "FY13-17 MYP"),
    ("N0002418C2307", "Huntington Ingalls", "FY18-22 MYP"),
    ("N0002418C2305", "Bath Iron Works", "FY18-22 MYP"),
    ("N0002423C2307", "Huntington Ingalls", "FY23-27 MYP"),
    ("N0002423C2305", "Bath Iron Works", "FY23-27 MYP"),
]


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def workbook_by_prime():
    out = defaultdict(float)
    for r in csv.DictReader(open(WORKBOOK_SUB)):
        out[(r.get("Prime PIID") or "").strip()] += _f(r.get("Subaward Amount $"))
    return out


def fetch_published(piid, key, log):
    path = RAW / f"{piid}.json"
    if path.exists():
        d = json.loads(path.read_text())
        return d.get("published", [])
    records, page = [], 0
    while True:
        params = {"api_key": key, "piid": piid, "pageNumber": page,
                  "pageSize": PAGE_SIZE, "status": "Published"}
        txt, st = http_get(BASE + "?" + urlencode(params), headers={"Accept": "application/json"})
        if st == 429:
            raise QuotaExhausted("SAM 429 -- daily quota exhausted.")
        if not txt:
            log(f"    {piid} page {page}: no response (status {st})")
            break
        body = json.loads(txt)
        data = body.get("data") or []
        nxt = body.get("nextPageLink") or ""
        if page == 0 and data and "piid=" not in nxt:
            log(f"    {piid}: WARNING nextPageLink missing piid= -> filter may be dropped")
        records.extend(data)
        total_pages = int(body.get("totalPages") or 0)
        if not data or len(data) < PAGE_SIZE or (total_pages and page + 1 >= total_pages):
            break
        page += 1
        time.sleep(0.35)
    write_json(path, {"piid": piid, "n_published": len(records), "published": records})
    time.sleep(0.35)
    return records


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    key = env("SAM_API_KEY")
    wb = workbook_by_prime()

    def log(m):
        print(m, flush=True)

    rows = []
    try:
        for piid, yard, block in PRIMES:
            recs = fetch_published(piid, key, log)
            sam_sum = sum(_f(r.get("subAwardAmount")) for r in recs)
            wb_sum = wb.get(piid, 0.0)
            rows.append({
                "piid": piid, "yard": yard, "block": block,
                "sam_fresh_subaward_$m": round(sam_sum / 1e6, 1),
                "sam_n_records": len(recs),
                "workbook_subaward_$m": round(wb_sum / 1e6, 1),
                "delta_$m": round((sam_sum - wb_sum) / 1e6, 1),
            })
            log(f"  {piid} {yard:20s} {block:12s} SAM=${sam_sum/1e6:>7.1f}M ({len(recs)} recs)  "
                f"workbook=${wb_sum/1e6:>7.1f}M")
    except QuotaExhausted as e:
        log(f"!! {e}")

    # under-reporting: HII vs BIW on the same block (SAM-fresh)
    by_block = defaultdict(dict)
    for r in rows:
        by_block[r["block"]][r["yard"]] = r["sam_fresh_subaward_$m"]

    write_json(EXTRACT / "ddg_subaward_sam_corroboration.json",
               {"per_prime": rows,
                "under_reporting_by_block": {
                    blk: {"Huntington Ingalls_$m": d.get("Huntington Ingalls", 0.0),
                          "Bath Iron Works_$m": d.get("Bath Iron Works", 0.0),
                          "biw_share_pct": (round(100 * d.get("Bath Iron Works", 0) /
                                                  (d.get("Huntington Ingalls", 0) + d.get("Bath Iron Works", 0)), 1)
                                            if (d.get("Huntington Ingalls", 0) + d.get("Bath Iron Works", 0)) else None)}
                    for blk, d in by_block.items()},
                "note": ("SAM.gov Subaward Reporting (FFATA), Published status, as pulled. "
                         "First-tier only; 6-18mo lag; a prime that files little shows little -- "
                         "BIW's near-zero is a reporting artifact, not its real supplier spend.")})
    with open(EXTRACT / "ddg_subaward_sam_corroboration.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["piid", "yard", "block", "sam_fresh_subaward_$m",
                                           "sam_n_records", "workbook_subaward_$m", "delta_$m"])
        w.writeheader()
        w.writerows(rows)
    print("\n=== SAM corroboration (HII vs BIW per block, SAM-fresh) ===")
    for blk, d in by_block.items():
        hii, biw = d.get("Huntington Ingalls", 0.0), d.get("Bath Iron Works", 0.0)
        print(f"  {blk:12} HII=${hii:>7.1f}M  BIW=${biw:>6.1f}M  -> BIW files "
              f"{(100*biw/(hii+biw) if (hii+biw) else 0):.1f}% of the block's reported subs")


if __name__ == "__main__":
    main()
