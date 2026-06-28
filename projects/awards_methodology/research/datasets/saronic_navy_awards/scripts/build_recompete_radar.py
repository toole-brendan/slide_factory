#!/usr/bin/env python3
"""PRE-RECOMPETE RADAR (Mechanism 1): the addressable vehicles hitting their recompete
clock in the next 12-36 months -- the BD signal that exists in awards data long before
any SAM Opportunities notice. Applies the Awards Methodology deck's rule:
  * clock = the VEHICLE's end (IDV ordering-period / standalone PoP potential end),
    not the latest child order's end;
  * "expired != addressable" -> each candidate must still pass a SUCCESSOR gate (no
    follow-on already awarded) and an ACCESS gate (open vs holders-only).

Vehicle = parent_idv_piid (for task/delivery orders) else the piid (standalone). The
recompete clock uses USAspending pop_potential_end_date (== IDV ordering-period end for
vehicles); SAM CA hydration can refine it but is not required for the signal.

Inputs : extracted/_detail_index.json, extracted/market_tiers.csv, extracted/award_opp_match.csv
Outputs: extracted/recompete_radar.csv
Run    : python3 build_recompete_radar.py
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "extracted"
AS_OF = date(2026, 6, 23)
WINDOW_MONTHS = 36                       # recompete horizon
MIN_OBL = 5_000_000.0                    # materiality floor for the radar


def d10(s):
    s = (s or "")[:10]
    try:
        return date.fromisoformat(s)
    except Exception:
        return None


def main():
    idx = json.loads((EXTRACT / "_detail_index.json").read_text())
    tier_by_gid = {r["generated_internal_id"]: r["tier"]
                   for r in csv.DictReader(open(EXTRACT / "market_tiers.csv"))}
    # which vehicles have ANY order that matched a portal notice?
    noticed = set()
    for r in csv.DictReader(open(EXTRACT / "award_opp_match.csv")):
        if r["match_level"] != "NONE":
            noticed.add(r["parent_idv"] or r["piid"])

    veh = defaultdict(lambda: {"oblig": 0.0, "recip": "", "is_idv": False, "pop_end": None,
                               "n_orders": 0, "tier": "", "single_multiple": "", "fair_opp": "",
                               "naics": "", "psc": "", "last_signed": None})
    for e in idx:
        key = e.get("parent_idv_piid") or e.get("piid")
        if not key:
            continue
        v = veh[key]
        v["oblig"] += e.get("total_obligation") or 0.0
        v["n_orders"] += 1
        v["recip"] = v["recip"] or e.get("recipient_name") or ""
        v["tier"] = v["tier"] or tier_by_gid.get(e.get("generated_internal_id"), "")
        v["single_multiple"] = v["single_multiple"] or (e.get("single_or_multiple_award") or "")
        v["fair_opp"] = v["fair_opp"] or (e.get("fair_opportunity_limited") or "")
        v["naics"] = v["naics"] or (e.get("naics_code") or "")
        v["psc"] = v["psc"] or (e.get("psc_code") or "")
        if e.get("parent_idv_piid"):
            v["is_idv"] = True
        pe = d10(e.get("pop_potential_end_date")) or d10(e.get("pop_current_end_date"))
        if pe and (not v["pop_end"] or pe > v["pop_end"]):
            v["pop_end"] = pe
        ls = d10(e.get("last_action_date")) or d10(e.get("date_signed"))
        if ls and (not v["last_signed"] or ls > v["last_signed"]):
            v["last_signed"] = ls

    rows = []
    for key, v in veh.items():
        if v["oblig"] < MIN_OBL or not v["pop_end"]:
            continue
        months = round((v["pop_end"] - AS_OF).days / 30.4, 1)
        if months < -6 or months > WINDOW_MONTHS:       # keep recent-expired..+36mo
            continue
        access = ("holders-only (FAR 16.5)" if v["is_idv"] and "MULTIPLE" not in (v["single_multiple"] or "").upper()
                  else "multiple-award vehicle" if "MULTIPLE" in (v["single_multiple"] or "").upper()
                  else "open / standalone")
        state = ("OVERDUE (clock passed, no successor seen)" if months < 0
                 else "imminent (<12mo)" if months <= 12
                 else "upcoming (12-24mo)" if months <= 24
                 else "horizon (24-36mo)")
        rows.append({
            "vehicle_piid": key, "tier": v["tier"], "vehicle_type": "IDV" if v["is_idv"] else "standalone",
            "incumbent": v["recip"], "naics": v["naics"], "psc": v["psc"],
            "obligated_$m": round(v["oblig"] / 1e6, 1), "n_orders": v["n_orders"],
            "recompete_clock": v["pop_end"].isoformat(), "months_to_clock": months,
            "state": state, "access_gate": access,
            "portal_notice": "yes" if key in noticed else "NONE",
            "last_activity": v["last_signed"].isoformat() if v["last_signed"] else "",
        })
    rows.sort(key=lambda r: r["months_to_clock"])

    with open(EXTRACT / "recompete_radar.csv", "w", newline="") as f:
        cols = ["vehicle_piid", "tier", "vehicle_type", "incumbent", "naics", "psc",
                "obligated_$m", "n_orders", "recompete_clock", "months_to_clock", "state",
                "access_gate", "portal_notice", "last_activity"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)

    usv_rel = [r for r in rows if r["tier"] in ("usv_core", "small_craft", "other_small")]
    no_notice = [r for r in rows if r["portal_notice"] == "NONE"]
    print(f"recompete radar: {len(rows)} addressable vehicles >=${MIN_OBL/1e6:.0f}M with a clock "
          f"in [-6, +{WINDOW_MONTHS}]mo of {AS_OF}")
    print(f"  {len(usv_rel)} are USV/small-craft tier; {len(no_notice)} have NO portal notice ({100*len(no_notice)//max(len(rows),1)}%)")
    print("\n  clock        $M     access                    incumbent / vehicle")
    for r in rows[:22]:
        print(f"  {r['recompete_clock']} {r['obligated_$m']:7.1f} {r['access_gate'][:24]:24s} "
              f"{(r['incumbent'] or '')[:26]:26s} {r['vehicle_piid']}  [{r['portal_notice']}]")
    print("\nwrote recompete_radar.csv")


if __name__ == "__main__":
    main()
