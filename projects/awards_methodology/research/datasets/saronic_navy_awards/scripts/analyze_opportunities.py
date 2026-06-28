#!/usr/bin/env python3
"""PORTAL-BLINDNESS analysis: what does the SAM.gov Opportunities portal actually
ADVERTISE for the maritime/USV market? Categorize the 669 notices already pulled
(saronic_specific_awards_data/research/extracted/opportunities_all.csv) by SUBJECT and BUYER to show
the portal is dominated by recurring ship repair/sustainment + small-boat buys, and is
nearly blind to Saronic's USV/autonomy market.

This is the "above the waterline" half of the evidence: the portal is a real but
narrow notice stream. No network calls -- pure analysis of the on-hand baseline.

Outputs: extracted/portal_content.csv (one row per notice, subject+buyer tag),
         extracted/portal_content_summary.json
Run    : python3 analyze_opportunities.py
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPPS = ROOT.parent / "extracted" / "opportunities_all.csv"
EXTRACT = ROOT / "extracted"

REPAIR_TITLE = re.compile(r"\b(repair|overhaul|drydock|dry-dock|dry dock|dockside|docking|"
                          r"availability|maintenance|restoration|PSA|MTA|deactivation|"
                          r"refurb|preservation|lay ?berth|lay-?up|voyage repair)\b", re.I)
USV_TITLE = re.compile(r"\b(unmanned|autonomous|uncrewed|optionally manned|USV|robotic|"
                       r"maritime autonomy|self-?driving)\b", re.I)


def subject(r):
    """Tag a notice by what is being bought."""
    tier = (r.get("tier") or "").upper()
    psc = (r.get("psc") or "").strip().upper()
    title = r.get("title") or ""
    if tier in ("STRONG", "MEDIUM") or (USV_TITLE.search(title) and "aircraft" not in title.lower()):
        return "usv_autonomy"
    if psc.startswith("J") or REPAIR_TITLE.search(title):
        return "ship_repair_maintenance"
    if psc in {"1905", "1925", "1940", "1990"} or psc.startswith("336"):
        return "vessel_procurement"
    if psc.startswith("20") or psc[:2] in {"59", "63", "66", "48", "47"} or psc == "2090":
        return "marine_components_parts"
    if psc.startswith("R") or psc.startswith("A") or psc.startswith("U") or psc.startswith("H"):
        return "services_rdte"
    return "other"


def buyer(r):
    ap = (r.get("agency_path") or "").upper()
    if "COAST GUARD" in ap or "70Z" in ap:
        return "Coast Guard"
    if "NAVY" in ap or "NAVSEA" in ap or "NIWC" in ap or "SPAWAR" in ap or "MARINE CORPS" in ap or "SEALIFT" in ap:
        return "Navy/USMC"
    if "ARMY" in ap or "CORPS OF ENGINEERS" in ap:
        return "Army"
    if "DEFENSE" in ap or "DARPA" in ap or "SOCOM" in ap or "TRANSPORTATION COMMAND" in ap:
        return "Other DoD"
    return "Civil/Other"


def main():
    rows = list(csv.DictReader(open(OPPS)))
    for r in rows:
        r["_subject"] = subject(r)
        r["_buyer"] = buyer(r)

    subj = Counter(r["_subject"] for r in rows)
    buy = Counter(r["_buyer"] for r in rows)
    subj_by_buyer = defaultdict(Counter)
    for r in rows:
        subj_by_buyer[r["_buyer"]][r["_subject"]] += 1

    n = len(rows)
    order = ["usv_autonomy", "ship_repair_maintenance", "vessel_procurement",
             "marine_components_parts", "services_rdte", "other"]
    summary = {
        "total_notices": n,
        "by_subject": {k: {"count": subj.get(k, 0), "pct": round(100 * subj.get(k, 0) / n, 1)}
                       for k in order},
        "by_buyer": dict(buy.most_common()),
        "usv_share_pct": round(100 * subj.get("usv_autonomy", 0) / n, 1),
        "sustainment_share_pct": round(100 * (subj.get("ship_repair_maintenance", 0)
                                              + subj.get("marine_components_parts", 0)) / n, 1),
    }
    (EXTRACT / "portal_content_summary.json").write_text(json.dumps(summary, indent=2))

    with open(EXTRACT / "portal_content.csv", "w", newline="") as f:
        cols = ["notice_id", "type", "pre_award", "posted", "_buyer", "_subject",
                "tier", "naics", "psc", "title", "solicitation_number", "agency_path"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"SAM Opportunities portal: {n} maritime/USV notices over 12 months\n")
    print("By SUBJECT (what is actually being advertised):")
    for k in order:
        c = subj.get(k, 0)
        print(f"  {k:26s} {c:4d}  {100*c/n:5.1f}%")
    print(f"\n  => USV/autonomy: {summary['usv_share_pct']}% of the portal")
    print(f"  => recurring sustainment (repair + parts): {summary['sustainment_share_pct']}%")
    print("\nBy BUYER:")
    for b, c in buy.most_common():
        usv = subj_by_buyer[b].get("usv_autonomy", 0)
        print(f"  {b:14s} {c:4d}  (usv/autonomy: {usv})")
    print("\nwrote portal_content.csv, portal_content_summary.json")


if __name__ == "__main__":
    main()
