#!/usr/bin/env python3
"""Two supplier-base measures for the DDG-51 subaward layer, matching the workbook's
methods:

  1. MOCK PERIOD OF PERFORMANCE -- FFATA subawards carry no PoP, so use the count of
     unique subaward Report IDs per supplier as a duration/recurrence proxy (more
     filings = longer, more sustained engagement). Corroborated here with the actual
     first->last Subaward Date span (they diverge: a few big spaced orders vs. many
     small frequent ones).

  2. HHI CONCENTRATION -- Herfindahl-Hirschman Index of supplier dollar shares, overall
     and within each SWBS ship system. High HHI = a few entrenched suppliers (hard to
     enter, clear teaming targets); low HHI = fragmented (more enterable as a new sub).
     DOJ bands: <1500 competitive, 1500-2500 moderate, >2500 concentrated.

Run:  python3 build_ddg_subaward_concentration.py
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import openpyxl

MASTER = ("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/"
          "distributed_shipbuilding/sam/sam_awards_data/20260620_Distributed Shipbuilding Master SAM_vS.xlsx")
SUB = ("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/"
       "distributed_shipbuilding/sam/sam_awards_data/workbook_award_classification_refactor/"
       "extracted/ddg_subaward_transactions.csv")
EXTRACT = Path(__file__).resolve().parent / "extracted"

BLOCK = {
    "N0002411C2307": "FY11 single-ship", "N0002411C2309": "FY11 single-ship",
    "N0002413C2305": "FY13-17 MYP", "N0002413C2307": "FY13-17 MYP",
    "N0002418C2305": "FY18-22 MYP", "N0002418C2307": "FY18-22 MYP",
    "N0002423C2305": "FY23-27 MYP", "N0002423C2307": "FY23-27 MYP",
}
GNAME = {"100": "Hull structure", "200": "Propulsion plant", "300": "Electric plant",
         "400": "Command, control & surveillance", "500": "Auxiliary systems",
         "600": "Outfit & furnishings", "700": "Armament"}


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def months(d0, d1):
    if not d0 or not d1:
        return None
    return (int(d1[:4]) - int(d0[:4])) * 12 + (int(d1[5:7]) - int(d0[5:7]))


def hhi(shares_dollars):
    """HHI (0-10000) of a dict {entity: $}."""
    tot = sum(shares_dollars.values())
    if tot <= 0:
        return None
    return round(sum((v / tot) ** 2 for v in shares_dollars.values()) * 10000, 0)


def band(h):
    if h is None:
        return "n/a"
    return "concentrated" if h > 2500 else "moderate" if h >= 1500 else "competitive"


def load_code2grp():
    wb = openpyxl.load_workbook(MASTER, data_only=True)
    ws = wb["Mapping - HII Code to SWBS"]
    rows = list(ws.iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if r and "HII Code" in [str(c) for c in r])
    hdr = [str(c) for c in rows[hi]]
    ci_code, ci_swbs = hdr.index("HII Code"), hdr.index("SWBS")
    out = {}
    for r in rows[hi + 1:]:
        if not r or not r[ci_code]:
            continue
        lbl = str(r[ci_swbs]) if r[ci_swbs] else ""
        out[str(r[ci_code]).strip()] = lbl.split()[0] if lbl[:1].isdigit() else None
    return out


def main():
    EXTRACT.mkdir(parents=True, exist_ok=True)
    code2grp = load_code2grp()
    rows = list(csv.DictReader(open(SUB)))

    # ---- 1. mock period of performance per supplier --------------------------
    sup_rid = defaultdict(set)
    sup_dates = defaultdict(list)
    sup_amt = defaultdict(float)
    sup_blocks = defaultdict(set)
    sys_sup = defaultdict(lambda: defaultdict(float))   # swbs grp -> supplier -> $
    sup_all = defaultdict(float)

    for r in rows:
        s = (r.get("Subawardee Vendor Name") or "").strip() or "(unnamed)"
        a = f(r.get("Subaward Amount $"))
        sup_rid[s].add((r.get("Subaward Report ID") or "").strip())
        d = (r.get("Subaward Date") or "")[:10]
        if d:
            sup_dates[s].append(d)
        sup_amt[s] += a
        sup_all[s] += a
        blk = BLOCK.get((r.get("Prime PIID") or "").strip())
        if blk:
            sup_blocks[s].add(blk)
        grp = code2grp.get((r.get("HII Work-Item Code") or "").strip())
        if grp:
            sys_sup[grp][s] += a

    with open(EXTRACT / "ddg_subaward_supplier_mockpop.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["supplier", "mock_pop_n_report_ids", "date_span_months",
                    "first_subaward", "last_subaward", "reported_$m", "n_blocks"])
        for s, a in sorted(sup_amt.items(), key=lambda x: -x[1]):
            ds = sorted(sup_dates[s])
            span = months(ds[0], ds[-1]) if ds else None
            w.writerow([s, len(sup_rid[s]), span,
                        ds[0] if ds else "", ds[-1] if ds else "",
                        round(a / 1e6, 2), len(sup_blocks[s])])

    # ---- 2. HHI concentration -----------------------------------------------
    overall_hhi = hhi(sup_all)
    by_system = []
    for grp, sd in sys_sup.items():
        tot = sum(sd.values())
        top_sup, top_amt = max(sd.items(), key=lambda x: x[1])
        h = hhi(sd)
        by_system.append({
            "swbs_major_group": grp, "ship_system": GNAME.get(grp, grp),
            "reported_$m": round(tot / 1e6, 1), "n_suppliers": len(sd),
            "hhi": h, "concentration": band(h),
            "top_supplier": top_sup, "top_supplier_share_pct": round(100 * top_amt / tot, 1),
        })
    by_system.sort(key=lambda x: -x["reported_$m"])
    with open(EXTRACT / "ddg_subaward_hhi_by_system.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["swbs_major_group", "ship_system", "reported_$m",
                                           "n_suppliers", "hhi", "concentration",
                                           "top_supplier", "top_supplier_share_pct"])
        w.writeheader()
        w.writerows(by_system)

    # interpretive summary
    ranked = [s for s in by_system if s["hhi"] is not None]
    most = max(ranked, key=lambda x: x["hhi"])
    least = min(ranked, key=lambda x: x["hhi"])
    pops = [len(v) for v in sup_rid.values()]
    summary = {
        "overall_supplier_hhi": overall_hhi, "overall_band": band(overall_hhi),
        "n_suppliers": len(sup_amt),
        "mock_pop_note": "mock PoP = count of unique subaward Report IDs per supplier (FFATA has no PoP field)",
        "mock_pop_median_report_ids": sorted(pops)[len(pops) // 2],
        "mock_pop_max": max(pops),
        "most_concentrated_system": {k: most[k] for k in ("ship_system", "hhi", "top_supplier", "top_supplier_share_pct", "reported_$m")},
        "least_concentrated_system": {k: least[k] for k in ("ship_system", "hhi", "n_suppliers", "reported_$m")},
        "interpretation": ("Overall base is fragmented (low HHI) but concentration is system-specific: "
                           "the most-concentrated big systems are entrenched/teaming targets, the "
                           "least-concentrated are the most enterable as a new sub."),
    }
    (EXTRACT / "ddg_subaward_concentration_summary.json").write_text(json.dumps(summary, indent=2))

    print(f"=== Overall supplier HHI: {overall_hhi} ({band(overall_hhi)}); {len(sup_amt)} suppliers ===")
    print("\nMock PoP (unique report IDs) -- top suppliers vs. actual date span:")
    for s, a in sorted(sup_amt.items(), key=lambda x: -x[1])[:8]:
        ds = sorted(sup_dates[s])
        sp = months(ds[0], ds[-1]) if ds else None
        print(f"  {s[:34]:34} reportIDs={len(sup_rid[s]):>4} (mock PoP)  span={sp} mo  ${a/1e6:>6.1f}M")
    print("\nHHI concentration by ship system (where to enter):")
    print(f"  {'system':34} {'$M':>7} {'subs':>4} {'HHI':>6}  band         top supplier")
    for s in by_system:
        print(f"  {s['ship_system'][:34]:34} {s['reported_$m']:>7.0f} {s['n_suppliers']:>4} "
              f"{(s['hhi'] or 0):>6.0f}  {s['concentration']:<12} {s['top_supplier'][:24]} ({s['top_supplier_share_pct']:.0f}%)")


if __name__ == "__main__":
    main()
