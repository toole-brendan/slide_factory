#!/usr/bin/env python3
"""v3 — TRUE requirement families for the autonomy/sensors lane (334511 + 5865).

Resolves the parent x PSC PROXY into real requirement families by pivoting on the
recompete unit — the PARENT IDIQ — and labelling each with the system designator that
surfaces across its orders. Family types:

  • ORDER family   = a parent IDIQ + all its delivery/task orders. Governing date =
                     the parent's ordering-period end (pop.end_date — the last-date-to-order
                     proxy; USAspending's detail last_date_to_order is null, pop.end_date
                     carries the ordering-period close).
  • STANDALONE     = a definitive contract (no parent). Governing date = ultimate
                     completion (pop.potential_end_date).

Parent IDIQ is recovered for free from generated_internal_id
(CONT_AWD_<order>_<sub>_<PARENT>_<sub>); only the top-N families' governing instruments
are detail-enriched. System designator (AN/SSQ-53, AN/SLQ-25, ASPJ, SEWIP…) is the
requirement's identity, pulled from the order descriptions.

Run: python3 build_navy_lane_families.py        # 334511+5865, enrich top 45
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
import urllib.parse
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import http_get, write_json  # noqa: E402
from build_navy_requirement_map import parent, code_of, desc_of, f as fnum

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "extracted"
DETAIL_DIR = ROOT / "usaspending_raw" / "detail"
SRC = EX / "navy_widened_discovered.csv"
AWARD_URL = "https://api.usaspending.gov/api/v2/awards/{gid}/"
TODAY = date(2026, 6, 26)
MO = 30.44
LANE = {"334511", "5865"}
TOPN = 45


def in_lane(r):
    return any(f"naics:{c}" in r["matched_codes"] or f"psc:{c}" in r["matched_codes"] for c in LANE)


def d(s):
    s = (s or "")[:10]
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def designator(desc):
    u = (desc or "").upper()
    m = re.search(r"AN/[A-Z]{2,4}-?\d+[A-Z]?", u)
    if m:
        return m.group(0).replace(" ", "")
    for k in ("ASPJ", "SEWIP", "NIXIE", "ADC MK", "SONOBUOY", "DECOY", "JAMMER", "NULKA"):
        if k in u:
            return k
    return ""


def parent_idv(gid):
    p = gid.split("_")
    if len(p) >= 6 and p[1] == "AWD" and p[-2] != "-NONE-":
        return p[-2], f"CONT_IDV_{p[-2]}_{p[-1]}"   # (piid, gid)
    return None, None


def detail(gid):
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


def status_of(gov):
    if not gov:
        return None, "—"
    m = (gov - TODAY).days / MO
    s = ("PAST (recompeted/bridged?)" if m < -6 else "OPEN NOW" if m < 18
         else "FORMING (shape now)" if m < 42 else "MONITOR")
    return m, s


def main():
    rows = [r for r in csv.DictReader(open(SRC)) if in_lane(r)]
    for r in rows:
        r["_amt"] = fnum(r["award_amount"])
        r["_pidv"], r["_pgid"] = parent_idv(r["generated_internal_id"])
        r["_desig"] = designator(r["description"])
        r["_y0"] = (d(r["start_date"]) or date(1900, 1, 1)).year

    # group: ORDER families keyed by parent IDIQ; STANDALONE keyed by own gid
    fams = defaultdict(list)
    for r in rows:
        key = ("IDIQ", r["_pidv"]) if r["_pidv"] else ("STANDALONE", r["generated_internal_id"])
        fams[key].append(r)

    families = []
    for (kind, key), rs in fams.items():
        desigs = Counter(x["_desig"] for x in rs if x["_desig"])
        label = desigs.most_common(1)[0][0] if desigs else ""
        inc = Counter(parent(x["recipient_name"]) for x in rs).most_common(1)[0][0]
        yrs = sorted({x["_y0"] for x in rs})
        rep = max(rs, key=lambda x: (d(x["end_date"]) or date(1900, 1, 1), x["_amt"]))
        families.append(dict(kind=kind, key=key[1] or "(none)", incumbent=inc, label=label,
                             net=sum(x["_amt"] for x in rs), n=len(rs),
                             span=(max(yrs) - min(yrs)) if len(yrs) > 1 else 0,
                             rep_gid=(rs[0]["_pgid"] if kind == "IDIQ" else rep["generated_internal_id"]),
                             rep_end=d(rep["end_date"])))
    families.sort(key=lambda x: -(x["net"] * (1 + min(x["n"], 30) / 5)))
    top = families[:TOPN]
    print(f"lane 334511+5865: {len(rows)} awards -> {len(families)} TRUE families "
          f"({sum(1 for f in families if f['kind']=='IDIQ')} IDIQ-pivoted, "
          f"{sum(1 for f in families if f['kind']=='STANDALONE')} standalone); enriching top {len(top)}…")

    for x in top:
        det = detail(x["rep_gid"]) or {}
        pop = det.get("period_of_performance") or {}
        ltc = det.get("latest_transaction_contract_data") or {}
        aw = det.get("awarding_agency") or {}
        gov = (d(pop.get("end_date")) if x["kind"] == "IDIQ"
               else d(pop.get("potential_end_date"))) or x["rep_end"]
        x["governing"] = gov
        x["mo"], x["status"] = status_of(gov)
        x["competed"] = (ltc.get("extent_competed_description") or "")[:20]
        x["sa_ma"] = (det.get("parent_award") or {}).get("multiple_or_single_aw_desc") or \
                     (ltc.get("multiple_or_single_award_idv_description") or "")
        x["office"] = ((aw.get("office_agency_name") or aw.get("subtier_agency", {}).get("name") or "")[:22])
        x["piid"] = det.get("piid") or x["key"]

    print(f"\n=== AUTONOMY/SENSORS — TRUE REQUIREMENT FAMILIES (top {len(top)} by scale x recurrence) ===")
    print(f"{'$M':>7s} {'ord':>3s} {'yr':>2s} {'governing':>10s} {'mo':>4s} {'status':>26s} "
          f"{'designator':>11s}  incumbent · vehicle")
    for x in top:
        g = x["governing"].isoformat() if x.get("governing") else "-"
        m = f"{x['mo']:.0f}" if x.get("mo") is not None else "-"
        print(f"{x['net']/1e6:>7,.0f} {x['n']:>3d} {x['span']:>2d} {g:>10s} {m:>4s} "
              f"{x.get('status','—'):>26s} {(x['label'] or '·'):>11s}  "
              f"{x['incumbent'][:18]:18s} {x.get('piid','')[:16]} {x.get('competed','')}")

    cols = ["kind", "incumbent", "label", "piid", "net", "n", "span", "governing", "mo",
            "status", "competed", "sa_ma", "office"]
    with open(EX / "navy_lane_autonomy_sensors_families.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for x in top:
            o = dict(x); o["governing"] = x["governing"].isoformat() if x.get("governing") else ""
            o["mo"] = round(x["mo"], 1) if x.get("mo") is not None else ""
            w.writerow(o)
    print(f"\nwrote navy_lane_autonomy_sensors_families.csv ({len(top)})")


if __name__ == "__main__":
    main()
