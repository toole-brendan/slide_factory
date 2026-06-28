#!/usr/bin/env python3
"""MARKET-STRUCTURE analysis from the discovery universe (no network calls):
  (1) Tier shape -- USV-core vs small-craft vs broad-maritime, count + $.
  (2) Vehicle-gated: prime concentration per tier (top primes' $ share + HHI) -- shows
      the maritime market is locked up by a handful of incumbents under long vehicles.
  (3) USV-market composition: who holds the $0.45B visible USV prime market, split
      industry vs university/FFRDC (the "it's all R&D" finding), and USV obligations by year.
  (4) OTA absence-evidence: known USV production primes' footprint in the STANDARD
      A-D/IDV contract universe -- Saronic et al. are absent because their order books
      run through OT agreements/consortia invisible to both SAM Opportunities AND FPDS.

Inputs : extracted/contracts_discovered_all.csv, extracted/market_tiers.csv
Outputs: extracted/prime_concentration.csv, extracted/usv_market.csv,
         extracted/ota_absence.csv, extracted/market_structure_summary.json
Run    : python3 analyze_market_structure.py
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "extracted"

# recipient buckets for the USV-market R&D-vs-industry split
RND_RX = re.compile(r"(UNIVERSIT|INSTITUTE|RESEARCH|LABORATOR|APPLIED PHYSICS|"
                    r"GEORGIA TECH|JOHNS HOPKINS|PENN STATE|PENNSYLVANIA STATE|"
                    r"COLLEGE|FOUNDATION|REGENTS|TRUSTEES|SCIENCES)", re.I)
# known USV / autonomous-maritime production primes (for the absence check)
USV_PRIMES = ["SARONIC", "METAL SHARK", "SEA MACHINES", "BLUE WATER AUTONOM",
              "OCEAN AERO", "SPATIAL INTEGRATED", "MARITIME APPLIED", "HII UNMANNED",
              "L3HARRIS", "L3 TECHNOLOGIES", "TEXTRON SYSTEMS", "LEIDOS",
              "SWIFTSHIPS", "BOLLINGER", "AUSTAL", "FLEET"]


def fnum(x):
    try:
        return float(x or 0)
    except (TypeError, ValueError):
        return 0.0


def hhi(shares):
    """Herfindahl index (0-10000) from a list of fractional shares."""
    return round(sum((s * 100) ** 2 for s in shares), 0)


def main():
    rows = list(csv.DictReader(open(EXTRACT / "contracts_discovered_all.csv")))
    tier_by_gid = {r["generated_internal_id"]: r["tier"]
                   for r in csv.DictReader(open(EXTRACT / "market_tiers.csv"))}
    for r in rows:
        r["_tier"] = tier_by_gid.get(r["generated_internal_id"], "out_of_scope")
        r["_amt"] = fnum(r["award_amount"])

    tiers = ["usv_core", "small_craft", "other_small", "broad_maritime"]

    # ---- (1)(2) tier shape + prime concentration ----------------------------------
    prime_rows, summary_tiers = [], {}
    for t in tiers:
        tr = [r for r in rows if r["_tier"] == t]
        tot = sum(r["_amt"] for r in tr) or 1.0
        by_prime = defaultdict(float)
        for r in tr:
            by_prime[(r["recipient_name"] or "?")] += r["_amt"]
        ranked = sorted(by_prime.items(), key=lambda kv: -kv[1])
        shares = [v / tot for _, v in ranked]
        top5 = sum(v for _, v in ranked[:5]) / tot
        top10 = sum(v for _, v in ranked[:10]) / tot
        summary_tiers[t] = {"awards": len(tr), "dollars": round(tot, 2),
                            "n_primes": len(ranked), "top5_share_pct": round(100 * top5, 1),
                            "top10_share_pct": round(100 * top10, 1), "hhi": hhi(shares)}
        for name, v in ranked[:15]:
            prime_rows.append({"tier": t, "prime": name, "dollars": round(v, 2),
                               "share_pct": round(100 * v / tot, 2)})

    # ---- (3) USV-market composition ------------------------------------------------
    usv = [r for r in rows if r["_tier"] == "usv_core"]
    usv_tot = sum(r["_amt"] for r in usv) or 1.0
    rnd = [r for r in usv if RND_RX.search(r["recipient_name"] or "")]
    rnd_d = sum(r["_amt"] for r in rnd)
    by_year = defaultdict(float)
    for r in usv:
        y = (r.get("start_date") or "")[:4]
        if y.isdigit():
            by_year[y] += r["_amt"]
    usv_rows = []
    by_recip = defaultdict(float)
    for r in usv:
        by_recip[(r["recipient_name"] or "?")] += r["_amt"]
    for name, v in sorted(by_recip.items(), key=lambda kv: -kv[1])[:20]:
        usv_rows.append({"recipient": name, "dollars": round(v, 2),
                         "rnd_ffrdc": "yes" if RND_RX.search(name or "") else "no"})

    # ---- (4) OTA absence-evidence --------------------------------------------------
    ota_rows = []
    for v in USV_PRIMES:
        hits = [r for r in rows if v in (r["recipient_name"] or "").upper()]
        ota_rows.append({"usv_prime": v, "awards_in_standard_universe": len(hits),
                         "dollars": round(sum(r["_amt"] for r in hits), 2),
                         "verdict": "ABSENT (order book is OTA/consortia)" if not hits
                                    else "present (conventional contracts)"})

    # ---- write ---------------------------------------------------------------------
    with open(EXTRACT / "prime_concentration.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["tier", "prime", "dollars", "share_pct"])
        w.writeheader(); w.writerows(prime_rows)
    with open(EXTRACT / "usv_market.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["recipient", "dollars", "rnd_ffrdc"])
        w.writeheader(); w.writerows(usv_rows)
    with open(EXTRACT / "ota_absence.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["usv_prime", "awards_in_standard_universe", "dollars", "verdict"])
        w.writeheader(); w.writerows(ota_rows)

    summary = {
        "tiers": summary_tiers,
        "usv_market": {"dollars": round(usv_tot, 2), "awards": len(usv),
                       "rnd_ffrdc_dollars": round(rnd_d, 2),
                       "rnd_ffrdc_pct": round(100 * rnd_d / usv_tot, 1),
                       "by_year": {y: round(by_year[y], 2) for y in sorted(by_year)}},
        "ota_absent_primes": [r["usv_prime"] for r in ota_rows if "ABSENT" in r["verdict"]],
    }
    (EXTRACT / "market_structure_summary.json").write_text(json.dumps(summary, indent=2))

    # ---- console -------------------------------------------------------------------
    print("TIER SHAPE + vehicle-gating (prime concentration):")
    for t in tiers:
        s = summary_tiers[t]
        print(f"  {t:15s} {s['awards']:5d} awards  ${s['dollars']/1e9:7.2f}B  "
              f"top5={s['top5_share_pct']:5.1f}%  HHI={int(s['hhi'])}")
    print(f"\nUSV visible prime market: ${usv_tot/1e9:.2f}B across {len(usv)} awards; "
          f"R&D/FFRDC = {summary['usv_market']['rnd_ffrdc_pct']}% of it")
    print("USV obligations by award-start year:")
    for y in sorted(by_year):
        print(f"  {y}  ${by_year[y]/1e6:7.1f}M")
    print("\nOTA absence-evidence (known USV primes in the STANDARD A-D/IDV universe):")
    for r in ota_rows:
        print(f"  {r['usv_prime']:22s} {r['awards_in_standard_universe']:3d} awards "
              f"${r['dollars']/1e6:8.1f}M  -> {r['verdict']}")
    print("\nwrote prime_concentration.csv, usv_market.csv, ota_absence.csv, market_structure_summary.json")


if __name__ == "__main__":
    main()
