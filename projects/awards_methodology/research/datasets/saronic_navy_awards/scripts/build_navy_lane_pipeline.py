#!/usr/bin/env python3
"""v2 — dated recompete-opportunity pipeline for ONE capability lane.

Default lane: autonomy / sensors = NAICS 334511 + PSC 5865. Reads the widened
discovery (navy_widened_discovered.csv), restricts to the lane, resolves recurring
requirement families (parent x PSC), then DETAIL-enriches each top family's
representative award (the latest-running instrument) via the USAspending award-detail
endpoint to get the governing date (ultimate completion = pop_potential_end_date),
parent IDV, and competitive posture — bounded to the top families so the detail-call
count stays small. Applies the playbook timing to estimate the recompete window.

Governing date by instrument: definitive/order -> ultimate completion (potential end);
IDV -> potential end as an LDO proxy (true last-date-to-order is a v3 refinement — the
lane is overwhelmingly definitive/order, few IDVs). Window status is measured from TODAY
against the playbook lead (successor often awarded ~24mo before the incumbent end; PALT
adds months on top).

Run: python3 build_navy_lane_pipeline.py                 # 334511 + 5865, top 40 families
     python3 build_navy_lane_pipeline.py 1905 1925 60    # custom codes + top-N
"""
from __future__ import annotations

import ast
import csv
import json
import os
import re
import sys
import time
import urllib.parse
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import http_get, write_json  # noqa: E402
from build_navy_requirement_map import parent, code_of, desc_of, f as fnum  # reuse helpers

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "extracted"
DETAIL_DIR = ROOT / "usaspending_raw" / "detail"
SRC = EX / "navy_widened_discovered.csv"
AWARD_URL = "https://api.usaspending.gov/api/v2/awards/{gid}/"
TODAY = date(2026, 6, 26)
MO = 30.44

# lane codes + top-N from argv
args = sys.argv[1:]
TOPN = int(args[-1]) if args and args[-1].isdigit() else 40
LANE = [a for a in args if not a.isdigit()] or ["334511", "5865"]
LANE_SET = set(LANE)


def in_lane(r):
    mc = r.get("matched_codes", "")
    return any((f"naics:{c}" in mc or f"psc:{c}" in mc) for c in LANE_SET)


def d(s):
    s = (s or "")[:10]
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def detail(gid):
    """GET award detail (cached). -> dict or None."""
    path = DETAIL_DIR / ("".join(c if c.isalnum() or c in "._-" else "_" for c in gid) + ".json")
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    txt, status = http_get(AWARD_URL.format(gid=urllib.parse.quote(gid)))
    if status != 200 or not txt:
        return None
    try:
        j = json.loads(txt)
    except Exception:
        return None
    write_json(path, j)
    time.sleep(0.12)
    return j


def main():
    rows = [r for r in csv.DictReader(open(SRC)) if in_lane(r)]
    for r in rows:
        r["_parent"] = parent(r["recipient_name"])
        r["_psc"] = code_of(r["psc"])
        r["_pscd"] = desc_of(r["psc"])
        r["_end"] = d(r["end_date"])
        r["_amt"] = fnum(r["award_amount"])
    print(f"lane {'+'.join(LANE)}: {len(rows)} awards, ${sum(r['_amt'] for r in rows)/1e9:.1f}B, "
          f"{len(set(r['_parent'] for r in rows))} prime parents")

    # PSC-cell concentration within the lane (contestability overlay)
    psc_pos = defaultdict(lambda: defaultdict(float))
    for r in rows:
        if r["_amt"] > 0:
            psc_pos[r["_psc"]][r["_parent"]] += r["_amt"]
    psc_conc = {}
    for psc, byp in psc_pos.items():
        tot = sum(byp.values()) or 1
        sh = sorted((v / tot for v in byp.values()), reverse=True)
        hhi = sum(s * s for s in sh)
        psc_conc[psc] = dict(top1=sh[0] if sh else 0, hhi=hhi,
                             label=("High" if (sh and (sh[0] >= .6 or hhi >= .4))
                                    else "Moderate" if (1 / hhi if hhi else 0) <= 3 else "Lower"))

    # requirement families: parent x PSC within the lane
    fam = defaultdict(list)
    for r in rows:
        fam[(r["_parent"], r["_psc"])].append(r)
    families = []
    for (par, psc), rs in fam.items():
        yrs = sorted({d(x["start_date"]).year for x in rs if d(x["start_date"])})
        net = sum(x["_amt"] for x in rs)
        rep = max(rs, key=lambda x: (x["_end"] or date(1900, 1, 1), x["_amt"]))  # latest-running, then largest
        families.append(dict(parent=par, psc=psc, desc=(rs[0]["_pscd"] or "")[:30], net=net,
                             breadth=len(rs), n_years=len(yrs),
                             span=(max(yrs) - min(yrs)) if len(yrs) > 1 else 0,
                             idv=sum(1 for x in rs if x["award_type_group"] == "idv"),
                             rep_gid=rep["generated_internal_id"], rep_piid=rep["award_id"],
                             rep_end=rep["_end"], conc=psc_conc.get(psc, {})))
    # rank by scale x recurrence
    families.sort(key=lambda x: -(x["net"] * (1 + x["n_years"])))
    top = families[:TOPN]
    print(f"families: {len(families)}; detail-enriching top {len(top)} representative awards…")

    # enrich representatives
    for fam_ in top:
        det = detail(fam_["rep_gid"]) or {}
        pop = det.get("period_of_performance") or {}
        ltc = det.get("latest_transaction_contract_data") or {}
        par = det.get("parent_award") or {}
        gov = d(pop.get("potential_end_date")) or fam_["rep_end"]   # ultimate completion (fallback: discovery end)
        fam_["governing"] = gov
        fam_["extent"] = (ltc.get("extent_competed_description") or "")[:22]
        fam_["fair_opp"] = ltc.get("fair_opportunity_limited")
        fam_["parent_idv"] = par.get("piid")
        fam_["idv_type"] = (par.get("idv_type_description") or "")[:14]
        # window status from TODAY (playbook: window opens ~18mo+ before governing date)
        m = ((gov - TODAY).days / MO) if gov else None
        fam_["mo_to_gov"] = m
        fam_["status"] = ("—" if m is None else
                          "PAST (recompeted/bridged?)" if m < -6 else
                          "OPEN NOW" if m < 18 else
                          "FORMING (shape now)" if m < 42 else
                          "MONITOR")

    # output
    print(f"\n=== AUTONOMY/SENSORS RECOMPETE PIPELINE (top {len(top)} families, ranked) ===")
    print(f"{'$M':>7s} {'awd':>3s} {'yr':>2s} {'govern':>10s} {'mo':>4s} {'status':>26s} "
          f"{'contest':>8s} {'competed':>16s}  parent / PSC")
    for x in top:
        g = x["governing"].isoformat() if x["governing"] else "-"
        m = f"{x['mo_to_gov']:.0f}" if x["mo_to_gov"] is not None else "-"
        print(f"{x['net']/1e6:>7,.0f} {x['breadth']:>3d} {x['n_years']:>2d} {g:>10s} {m:>4s} "
              f"{x['status']:>26s} {x['conc'].get('label','?'):>8s} {x['extent']:>16s}  "
              f"{x['parent'][:20]:20s} {x['psc']} {x['desc']}")

    cols = ["parent", "psc", "desc", "net", "breadth", "n_years", "span", "idv",
            "governing", "mo_to_gov", "status", "extent", "fair_opp", "parent_idv",
            "idv_type", "rep_piid"]
    with open(EX / "navy_lane_autonomy_sensors_pipeline.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for x in top:
            x = dict(x); x["governing"] = x["governing"].isoformat() if x["governing"] else ""
            x["mo_to_gov"] = round(x["mo_to_gov"], 1) if x["mo_to_gov"] is not None else ""
            w.writerow(x)
    print(f"\nwrote navy_lane_autonomy_sensors_pipeline.csv ({len(top)})")


if __name__ == "__main__":
    main()
