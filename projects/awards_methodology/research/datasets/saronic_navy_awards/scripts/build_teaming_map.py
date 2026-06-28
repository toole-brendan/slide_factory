#!/usr/bin/env python3
"""TEAMING MAP (Mechanism 3): turn the first-tier subaward pull into Saronic's
route-to-market-as-a-supplier map. From the SAM subaward records under the maritime/USV
primes, build:
  * subaward_edges.csv  -- every prime -> sub edge (rolled up to sub parent), $ + date +
    inferred capability bucket + the reporting LAG (submittedDate - subAwardDate).
  * teaming_summary.csv -- suppliers ranked by $ and by # of distinct primes they serve
    (recurring suppliers = the established USV/maritime supply chain to partner with or
    displace); plus which integrators sub out the most (teaming targets).

Capability bucket is keyword-inferred from sub name + description (autonomy/software,
sensors/payload, platform/hull, propulsion, C2/comms, integration/eng services, materials)
-- a first cut; entity-NAICS enrichment (pull_sam_entity.py) can refine it later.

MANDATORY CAVEAT carried into the memo: first-tier FFATA reporting lags primes 6-18 mo and
some primes file nothing -> this is a FLOOR on the supply chain, not a census. The
submittedDate-minus-subAwardDate lag is emitted per edge so the lag is visible, not assumed.

Inputs : sam_subawards/*.json
Outputs: extracted/subaward_edges.csv, extracted/teaming_summary.csv, extracted/teaming_summary.json
Run    : python3 build_teaming_map.py
"""
from __future__ import annotations

import csv
import glob
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "sam_subawards"
EXTRACT = ROOT / "extracted"

BUCKETS = [
    ("autonomy_software", re.compile(r"(AUTONOM|UNMANNED|SOFTWARE|AI|MACHINE LEARN|ALGORITH|"
                                     r"NAVIGATION|GUIDANCE|MISSION SYSTEM|COMPUTER)", re.I)),
    ("sensors_payload", re.compile(r"(SENSOR|RADAR|SONAR|LIDAR|CAMERA|EO/IR|EOIR|ANTENNA|"
                                   r"ACOUSTIC|PAYLOAD|SEEKER|OPTIC)", re.I)),
    ("platform_hull", re.compile(r"(HULL|BOAT|VESSEL|SHIP|FABRICAT|ALUMINUM|COMPOSITE|"
                                 r"MARINE STRUCT|SHIPYARD|CRAFT)", re.I)),
    ("propulsion_power", re.compile(r"(ENGINE|PROPULS|MOTOR|GENERATOR|BATTER|POWER|"
                                    r"DRIVE|THRUSTER|FUEL)", re.I)),
    ("c2_comms", re.compile(r"(COMMUNICAT|RADIO|SATCOM|DATALINK|DATA LINK|NETWORK|"
                            r"COMMAND AND CONTROL|C2|C4ISR|RF)", re.I)),
    ("integration_eng_svcs", re.compile(r"(ENGINEER|INTEGRAT|TECHNICAL SERVIC|SUPPORT SERVIC|"
                                        r"LOGISTIC|TEST|PROFESSIONAL|CONSULT|STAFF)", re.I)),
    ("materials_components", re.compile(r"(STEEL|METAL|MATERIAL|COMPONENT|HARDWARE|VALVE|"
                                        r"CABLE|FASTENER|MACHINING|CASTING)", re.I)),
]


def bucket(name, desc):
    blob = f"{name} {desc}"
    for label, rx in BUCKETS:
        if rx.search(blob):
            return label
    return "other_unclassified"


def fnum(x):
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


def lag_months(sub_date, submitted):
    try:
        a = date.fromisoformat((sub_date or "")[:10])
        b = date.fromisoformat((submitted or "")[:10])
        return round((b - a).days / 30.4, 1)
    except Exception:
        return None


def main():
    edges = []
    prime_subout = defaultdict(float)       # prime -> total subawarded $
    prime_names = {}
    files = sorted(glob.glob(str(RAW / "*.json")))
    for fp in files:
        d = json.load(open(fp))
        prime = d.get("recipient") or "?"
        ppiid = d.get("piid")
        prime_names[ppiid] = prime
        for rec in d.get("published") or []:
            sub_name = (rec.get("subEntityParentLegalBusinessName")
                        or rec.get("subEntityLegalBusinessName") or "?").strip()
            sub_key = (rec.get("subParentUei") or rec.get("subEntityUei")
                       or sub_name).strip()
            amt = fnum(rec.get("subAwardAmount"))
            desc = rec.get("subawardDescription") or rec.get("descriptionOfRequirement") or ""
            edges.append({
                "prime_piid": ppiid, "prime": prime, "prime_uei": rec.get("primeEntityUei"),
                "sub_key": sub_key, "sub_name": sub_name, "sub_uei": rec.get("subEntityUei"),
                "sub_amount": round(amt, 2), "sub_date": (rec.get("subAwardDate") or "")[:10],
                "capability": bucket(sub_name, desc),
                "report_lag_mo": lag_months(rec.get("subAwardDate"), rec.get("submittedDate")),
                "description": desc[:120],
            })
            prime_subout[(ppiid, prime)] += amt

    # ---- supplier rollup: $ and # distinct primes served --------------------------
    sup_dol = defaultdict(float)
    sup_primes = defaultdict(set)
    sup_name = {}
    sup_cap = defaultdict(lambda: defaultdict(float))
    for e in edges:
        sup_dol[e["sub_key"]] += e["sub_amount"]
        sup_primes[e["sub_key"]].add(e["prime"])
        sup_name.setdefault(e["sub_key"], e["sub_name"])
        sup_cap[e["sub_key"]][e["capability"]] += e["sub_amount"]
    suppliers = []
    for k in sup_dol:
        caps = sorted(sup_cap[k].items(), key=lambda kv: -kv[1])
        suppliers.append({"supplier": sup_name[k], "sub_key": k,
                          "total_sub_dollars": round(sup_dol[k], 2),
                          "n_distinct_primes": len(sup_primes[k]),
                          "primes": "; ".join(sorted(sup_primes[k])[:6]),
                          "primary_capability": caps[0][0] if caps else "?"})
    suppliers.sort(key=lambda s: -s["total_sub_dollars"])
    recurring = [s for s in suppliers if s["n_distinct_primes"] >= 2]

    # ---- capability totals + teaming-target primes --------------------------------
    cap_tot = defaultdict(float)
    for e in edges:
        cap_tot[e["capability"]] += e["sub_amount"]
    subout = sorted(({"prime": n, "piid": p, "subawarded_dollars": round(v, 2)}
                     for (p, n), v in prime_subout.items()), key=lambda x: -x["subawarded_dollars"])

    # ---- write --------------------------------------------------------------------
    with open(EXTRACT / "subaward_edges.csv", "w", newline="") as f:
        cols = ["prime_piid", "prime", "prime_uei", "sub_key", "sub_name", "sub_uei",
                "sub_amount", "sub_date", "capability", "report_lag_mo", "description"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(sorted(edges, key=lambda e: -e["sub_amount"]))
    with open(EXTRACT / "teaming_summary.csv", "w", newline="") as f:
        cols = ["supplier", "sub_key", "total_sub_dollars", "n_distinct_primes",
                "primary_capability", "primes"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(suppliers)

    grand = sum(e["sub_amount"] for e in edges)
    lags = [e["report_lag_mo"] for e in edges if e["report_lag_mo"] is not None]
    med_lag = sorted(lags)[len(lags) // 2] if lags else None
    summary = {"n_edges": len(edges), "n_suppliers": len(suppliers),
               "total_subaward_dollars": round(grand, 2),
               "n_recurring_suppliers": len(recurring),
               "median_report_lag_months": med_lag,
               "capability_totals": {k: round(v, 2) for k, v in sorted(cap_tot.items(), key=lambda kv: -kv[1])},
               "top_suppliers": suppliers[:15], "recurring_suppliers": recurring[:15],
               "top_subcontracting_primes": subout[:15]}
    (EXTRACT / "teaming_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    print(f"teaming map: {len(edges)} prime->sub edges, {len(suppliers)} distinct suppliers, "
          f"${grand/1e6:,.1f}M first-tier (a FLOOR; FFATA lags {med_lag}mo median).")
    print("\ncapability mix of the maritime/USV supply chain:")
    for k, v in sorted(cap_tot.items(), key=lambda kv: -kv[1]):
        print(f"  {k:22s} ${v/1e6:7,.1f}M")
    print(f"\nrecurring suppliers (serve >=2 primes): {len(recurring)}")
    for s in recurring[:12]:
        print(f"  ${s['total_sub_dollars']/1e6:6,.1f}M  {s['n_distinct_primes']}p  "
              f"{s['primary_capability']:20s} {s['supplier'][:40]}")
    print("\ntop integrators by $ subawarded out (teaming targets):")
    for s in subout[:10]:
        print(f"  ${s['subawarded_dollars']/1e6:6,.1f}M  {s['piid']:16s} {s['prime'][:38]}")
    print("\nwrote subaward_edges.csv, teaming_summary.csv, teaming_summary.json")


if __name__ == "__main__":
    main()
