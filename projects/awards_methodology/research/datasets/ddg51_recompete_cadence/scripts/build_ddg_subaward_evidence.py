#!/usr/bin/env python3
"""Characterize the DDG-51 MYP supplier base -- the addressable layer under the closed
prime duopoly -- for the awards-methodology slide 02 reframe (cadence -> sourcing wave
-> supply-chain entry).

Reads the first-tier (FFATA) subaward transactions already extracted in the
distributed_shipbuilding project and rolls them up four ways:
  1. subaward $ by block         -> the sourcing waves
  2. recurring suppliers (>=2 blocks) -> the established base you compete with / team with
  3. SWBS component map          -> which ship systems the subaward dollars buy
  4. wave by year x block        -> cadence -> demand-surge timing

CAVEAT carried in the outputs: FFATA subaward reporting is FIRST-TIER ONLY, lags 6-18
months, and is under-reported by some primes (Bath Iron Works reports a fraction of
Huntington Ingalls on the same block) -> every total is a FLOOR, not a census.

Run:  python3 build_ddg_subaward_evidence.py
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

SUB = ("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/"
       "distributed_shipbuilding/sam/sam_awards_data/workbook_award_classification_refactor/"
       "extracted/ddg_subaward_transactions.csv")
HERE = Path(__file__).resolve().parent
EXTRACT = HERE / "extracted"

BLOCK = {
    "N0002411C2307": "FY11 single-ship", "N0002411C2309": "FY11 single-ship",
    "N0002413C2305": "FY13-17 MYP", "N0002413C2307": "FY13-17 MYP",
    "N0002418C2305": "FY18-22 MYP", "N0002418C2307": "FY18-22 MYP",
    "N0002423C2305": "FY23-27 MYP", "N0002423C2307": "FY23-27 MYP",
}
YARD = {p: ("Bath Iron Works" if p.endswith("05") else "Huntington Ingalls") for p in BLOCK}
BLOCK_ORDER = ["FY11 single-ship", "FY13-17 MYP", "FY18-22 MYP", "FY23-27 MYP"]


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def main():
    EXTRACT.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(SUB)))
    A, NAME, PIID, DATE, SWBS = ("Subaward Amount $", "Subawardee Vendor Name",
                                 "Prime PIID", "Subaward Date", "SWBS Subsystem")

    by_block = defaultdict(lambda: {"reported_$m": 0.0, "n_transactions": 0, "subs": set(), "primes": set()})
    sup = defaultdict(lambda: {"$": 0.0, "blocks": set(), "n": 0, "swbs": defaultdict(float)})
    swbs = defaultdict(lambda: {"$": 0.0, "n": 0, "subs": set()})
    wave = defaultdict(float)

    for r in rows:
        blk = BLOCK.get((r.get(PIID) or "").strip())
        if not blk:
            continue
        a = f(r.get(A))
        name = (r.get(NAME) or "").strip() or "(unnamed)"
        sys_ = (r.get(SWBS) or "").strip() or "(unmapped)"
        yr = (r.get(DATE) or "")[:4]

        b = by_block[blk]
        b["reported_$m"] += a
        b["n_transactions"] += 1
        b["subs"].add(name)
        b["primes"].add(r.get(PIID))

        s = sup[name]
        s["$"] += a
        s["blocks"].add(blk)
        s["n"] += 1
        s["swbs"][sys_] += a

        w = swbs[sys_]
        w["$"] += a
        w["n"] += 1
        w["subs"].add(name)

        if yr.isdigit():
            wave[(blk, yr)] += a

    # 1. by block
    with open(EXTRACT / "ddg_subaward_by_block.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["block", "reported_subaward_$m", "n_transactions", "n_distinct_suppliers", "primes_reporting"])
        for blk in BLOCK_ORDER:
            d = by_block.get(blk)
            if d:
                w.writerow([blk, round(d["reported_$m"] / 1e6, 1), d["n_transactions"],
                            len(d["subs"]), "; ".join(sorted(d["primes"]))])

    # 2. recurring suppliers (>= 2 blocks)
    recurring = sorted(((n, v) for n, v in sup.items() if len(v["blocks"]) >= 2),
                       key=lambda x: -x[1]["$"])
    with open(EXTRACT / "ddg_recurring_suppliers.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["supplier", "n_blocks_served", "blocks_served", "reported_$m",
                    "n_subawards", "top_swbs_system"])
        for n, v in recurring:
            top_swbs = max(v["swbs"].items(), key=lambda x: x[1])[0] if v["swbs"] else ""
            w.writerow([n, len(v["blocks"]),
                        "; ".join(b for b in BLOCK_ORDER if b in v["blocks"]),
                        round(v["$"] / 1e6, 1), v["n"], top_swbs])

    # 3. SWBS component map
    swbs_sorted = sorted(swbs.items(), key=lambda x: -x[1]["$"])
    with open(EXTRACT / "ddg_subaward_by_swbs.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["swbs_subsystem", "reported_$m", "n_transactions", "n_distinct_suppliers"])
        for sys_, d in swbs_sorted:
            w.writerow([sys_, round(d["$"] / 1e6, 1), d["n"], len(d["subs"])])

    # 4. wave by year x block
    years = sorted({y for (_, y) in wave})
    with open(EXTRACT / "ddg_subaward_wave_by_year.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["block", "year", "reported_subaward_$m"])
        for blk in BLOCK_ORDER:
            for y in years:
                if (blk, y) in wave:
                    w.writerow([blk, y, round(wave[(blk, y)] / 1e6, 2)])

    summary = {
        "total_reported_subaward_$m": round(sum(d["reported_$m"] for d in by_block.values()) / 1e6, 1),
        "n_transactions": sum(d["n_transactions"] for d in by_block.values()),
        "n_distinct_suppliers": len(sup),
        "n_recurring_suppliers_2plus_blocks": len(recurring),
        "by_block": {blk: {"reported_$m": round(by_block[blk]["reported_$m"] / 1e6, 1),
                           "n_suppliers": len(by_block[blk]["subs"])}
                     for blk in BLOCK_ORDER if blk in by_block},
        "top_swbs_systems": [{"system": s, "reported_$m": round(d["$"] / 1e6, 1)}
                             for s, d in swbs_sorted[:8]],
        "caveat": ("FFATA first-tier subawards: floor not census; 6-18mo lag; under-reported "
                   "by some primes (BIW << HII on the same block)."),
    }
    (EXTRACT / "ddg_subaward_summary.json").write_text(json.dumps(summary, indent=2))

    print(f"=== DDG subaward evidence: ${summary['total_reported_subaward_$m']}M reported across "
          f"{summary['n_transactions']} transactions, {summary['n_distinct_suppliers']} suppliers "
          f"({summary['n_recurring_suppliers_2plus_blocks']} recurring >=2 blocks) ===")
    print("by block:")
    for blk in BLOCK_ORDER:
        d = by_block.get(blk)
        if d:
            print(f"  {blk:16} ${d['reported_$m']/1e6:>7.1f}M  {len(d['subs']):>3} suppliers  "
                  f"{d['n_transactions']:>4} txns  [{', '.join(sorted(d['primes']))}]")
    print(f"recurring suppliers (>=2 blocks): {len(recurring)} -> top 8:")
    for n, v in recurring[:8]:
        print(f"  ${v['$']/1e6:>7.1f}M  {len(v['blocks'])} blocks  {n[:40]}")
    print("top SWBS systems:")
    for s, d in swbs_sorted[:8]:
        print(f"  ${d['$']/1e6:>7.1f}M  {d['n']:>4} txns  {s[:46]}")


if __name__ == "__main__":
    main()
