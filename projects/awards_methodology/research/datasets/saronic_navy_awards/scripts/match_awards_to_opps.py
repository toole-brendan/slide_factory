#!/usr/bin/env python3
"""Match the Saronic-addressable prime-award universe against the 669 SAM Opportunities
notices already pulled (projects/awards_methodology/saronic_specific_awards_data/research/extracted/opportunities_all.csv),
to measure how much of the market the Opportunities PORTAL cannot or does not surface.

Produces two complementary incompleteness numbers (the memo's hero stats):

  (A) STRUCTURALLY-EXEMPT share  -- computed directly from award structure, no matching
      needed. The fraction of addressable award $ (and actions) flowing via mechanisms
      the portal is EXEMPT from synopsizing:
        * delivery/task orders placed under an IDV  -> FAR 16.505, no separate synopsis
        * OT agreements/orders                      -> never synopsized on SAM Opportunities
      vs definitive contracts (which SHOULD have had a notice). This is the portal's
      structural blind spot and does not depend on the 1-year opportunities window.

  (B) EMPIRICALLY-DARK share (within window) -- of awards SIGNED inside the opportunities
      posted window [min,max posted], the fraction with NO matching notice by solicitation
      number / PIID. These could have had a discoverable notice, so a miss is "dark".

Match keys (each award, normalized = UPPER, non-alnum stripped; opp solnums also split on
'-' for the compound USCG dockside/drydock pairs): award.solicitation_identifier, award.piid,
award.parent_idv_piid  vs  the opportunity solicitation_number set.

Calibration: the 669 notices include 90 Award Notices; we measure how many of THEIR
solicitation numbers hit our award universe (full discovery PIIDs) -- a sanity check on
the key before trusting "no match == dark".

Inputs : extracted/_detail_index.json (addressable awards w/ solicitation_identifier),
         extracted/market_tiers.csv, extracted/contracts_discovered_all.csv (full universe
         for PIID calibration), ../extracted/opportunities_all.csv (the portal baseline).
Outputs: extracted/award_opp_match.csv, extracted/dark_awards.csv, extracted/incompleteness_summary.json
Run    : python3 match_awards_to_opps.py
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]            # research/contracts/
EXTRACT = ROOT / "extracted"
OPPS = ROOT.parent / "extracted" / "opportunities_all.csv"   # saronic_specific_awards_data/research/extracted/


def norm(s: str) -> str:
    """UPPER + strip every non-alphanumeric. 'N66001_25_R_0024' -> 'N66001250024'."""
    return re.sub(r"[^A-Z0-9]", "", (s or "").upper())


def opp_keys(solnum: str):
    """Normalized key(s) for an opportunity solicitation number; split compounds on '-'."""
    out = set()
    for part in (solnum or "").split("-"):
        k = norm(part)
        if len(k) >= 6:                       # ignore junk fragments
            out.add(k)
    k = norm(solnum)
    if len(k) >= 6:
        out.add(k)
    return out


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def main():
    # ---- 1. opportunities baseline -------------------------------------------------
    opps = list(csv.DictReader(open(OPPS)))
    posted = sorted(r["posted"] for r in opps if r.get("posted"))
    win_lo, win_hi = posted[0][:10], posted[-1][:10]
    opp_index = defaultdict(list)            # normalized solnum -> [opp rows]
    for r in opps:
        for k in opp_keys(r.get("solicitation_number")):
            opp_index[k].append(r)
    notice_solnums = {norm(r["solicitation_number"]) for r in opps
                      if r.get("solicitation_number")}

    # ---- 2. calibration: do Award-Notice solnums hit the FULL discovery universe? ---
    disc = list(csv.DictReader(open(EXTRACT / "contracts_discovered_all.csv")))
    disc_piids = {norm(r["award_id"]) for r in disc if r.get("award_id")}
    award_notices = [r for r in opps if "award notice" in (r.get("type") or "").lower()]
    an_keys = set()
    for r in award_notices:
        an_keys |= opp_keys(r.get("solicitation_number"))
    an_hit = sum(1 for k in an_keys if k in disc_piids)
    calib = {"award_notices": len(award_notices), "distinct_an_solnums": len(an_keys),
             "hit_full_discovery_piids": an_hit,
             "hit_rate": round(an_hit / max(len(an_keys), 1), 3)}

    # ---- 3. addressable awards: tier + structural class ----------------------------
    idx = json.loads((EXTRACT / "_detail_index.json").read_text())
    tier_by_gid = {r["generated_internal_id"]: r["tier"]
                   for r in csv.DictReader(open(EXTRACT / "market_tiers.csv"))}

    def struct_class(e):
        """Synopsis exemption class from award structure."""
        atype = (e.get("award_type") or "").upper()
        adesc = (e.get("award_type_description") or "").lower()
        if "OT" in atype or "other transaction" in adesc:
            return "ot_exempt"
        if e.get("parent_idv_piid"):
            return "task_order_exempt"          # delivery/task order under an IDV (FAR 16.5)
        if atype.startswith("IDV") or "idv" in adesc or "indefinite" in adesc:
            return "idv_vehicle"                # the IDV itself (a vehicle, not a buy)
        return "definitive_synopsizable"        # a standalone contract that SHOULD have a notice

    rows = []
    for e in idx:
        gid = e.get("generated_internal_id")
        oblig = fnum(e.get("sum_federal_action_obligation")) or fnum(e.get("total_obligation"))
        keys = [norm(e.get("solicitation_identifier")), norm(e.get("piid")),
                norm(e.get("parent_idv_piid"))]
        matched, mtype, mlevel = None, None, "NONE"
        for lvl, k in zip(("solnum", "piid", "parent_idv"), keys):
            if k and k in opp_index:
                matched = opp_index[k][0]
                mtype = matched.get("type")
                mlevel = lvl
                break
        signed = (e.get("date_signed") or "")[:10]
        in_window = bool(signed and win_lo <= signed <= win_hi)
        rows.append({
            "gid": gid, "piid": e.get("piid"), "parent_idv": e.get("parent_idv_piid"),
            "tier": tier_by_gid.get(gid, "?"), "struct_class": struct_class(e),
            "recipient": e.get("recipient_name"), "naics": e.get("naics_code"),
            "psc": e.get("psc_code"), "award_type": e.get("award_type"),
            "obligation": round(oblig, 2), "date_signed": signed,
            "in_opps_window": "yes" if in_window else "no",
            "solicitation_identifier": e.get("solicitation_identifier"),
            "match_level": mlevel, "matched_notice_type": mtype,
            "matched_notice_id": (matched or {}).get("notice_id"),
        })

    # ---- 4. metric (A): structurally-exempt share (all addressable, all years) ------
    def share(subset, total_rows):
        d = sum(r["obligation"] for r in subset)
        t = sum(r["obligation"] for r in total_rows) or 1.0
        return round(d, 2), round(100 * d / t, 1), len(subset)

    buys = [r for r in rows if r["struct_class"] != "idv_vehicle"]   # exclude the empty IDV shells
    exempt = [r for r in buys if r["struct_class"] in ("ot_exempt", "task_order_exempt")]
    definitive = [r for r in buys if r["struct_class"] == "definitive_synopsizable"]
    metric_A = {
        "addressable_buy_dollars": share(buys, buys)[0],
        "addressable_buy_actions": len(buys),
        "synopsis_exempt": dict(zip(("dollars", "pct_of_buys", "actions"), share(exempt, buys))),
        "task_orders_16_5": dict(zip(("dollars", "pct_of_buys", "actions"),
                                     share([r for r in buys if r["struct_class"] == "task_order_exempt"], buys))),
        "ot_agreements": dict(zip(("dollars", "pct_of_buys", "actions"),
                                  share([r for r in buys if r["struct_class"] == "ot_exempt"], buys))),
        "definitive_synopsizable": dict(zip(("dollars", "pct_of_buys", "actions"), share(definitive, buys))),
    }

    # ---- 5. metric (B): empirically-dark share, within the opportunities window -----
    win_buys = [r for r in buys if r["in_opps_window"] == "yes"]
    win_dark = [r for r in win_buys if r["match_level"] == "NONE"]
    win_def = [r for r in win_buys if r["struct_class"] == "definitive_synopsizable"]
    win_def_dark = [r for r in win_def if r["match_level"] == "NONE"]
    metric_B = {
        "opps_window": [win_lo, win_hi],
        "addressable_buys_in_window": dict(zip(("dollars", "pct", "actions"), share(win_buys, win_buys))),
        "dark_in_window": dict(zip(("dollars", "pct_of_window", "actions"), share(win_dark, win_buys))),
        "definitive_in_window_actions": len(win_def),
        "definitive_in_window_dark_actions": len(win_def_dark),
        "definitive_dark_dollars": round(sum(r["obligation"] for r in win_def_dark), 2),
    }

    # ---- 6. write outputs ----------------------------------------------------------
    cols = ["gid", "piid", "parent_idv", "tier", "struct_class", "recipient", "naics",
            "psc", "award_type", "obligation", "date_signed", "in_opps_window",
            "solicitation_identifier", "match_level", "matched_notice_type", "matched_notice_id"]
    with open(EXTRACT / "award_opp_match.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sorted(rows, key=lambda x: -x["obligation"]):
            w.writerow(r)
    dark = [r for r in buys if r["match_level"] == "NONE"]
    with open(EXTRACT / "dark_awards.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sorted(dark, key=lambda x: -x["obligation"]):
            w.writerow(r)

    summary = {"opportunities_total": len(opps), "opps_window": [win_lo, win_hi],
               "addressable_awards_indexed": len(rows), "calibration": calib,
               "metric_A_structurally_exempt": metric_A, "metric_B_empirically_dark": metric_B}
    (EXTRACT / "incompleteness_summary.json").write_text(json.dumps(summary, indent=2))

    # ---- 7. console headline -------------------------------------------------------
    print(f"opportunities baseline: {len(opps)} notices, posted {win_lo}..{win_hi}")
    print(f"calibration: {calib['hit_full_discovery_piids']}/{calib['distinct_an_solnums']} "
          f"award-notice solnums hit the discovery PIID universe ({calib['hit_rate']*100:.0f}%)")
    print(f"\naddressable buys (detail-indexed): {len(buys)} actions, "
          f"${metric_A['addressable_buy_dollars']/1e9:.2f}B obligated")
    print("METRIC A - structural portal blind spot (synopsis-exempt mechanisms):")
    ex = metric_A["synopsis_exempt"]
    print(f"  synopsis-EXEMPT: ${ex['dollars']/1e9:.2f}B = {ex['pct_of_buys']}% of buy $ "
          f"({ex['actions']} actions)")
    print(f"    - FAR 16.5 task/delivery orders under IDVs: "
          f"${metric_A['task_orders_16_5']['dollars']/1e9:.2f}B ({metric_A['task_orders_16_5']['pct_of_buys']}%)")
    print(f"    - OT agreements/orders: "
          f"${metric_A['ot_agreements']['dollars']/1e9:.2f}B ({metric_A['ot_agreements']['pct_of_buys']}%)")
    print(f"  definitive (synopsizable): ${metric_A['definitive_synopsizable']['dollars']/1e9:.2f}B "
          f"({metric_A['definitive_synopsizable']['pct_of_buys']}%)")
    print("METRIC B - empirically dark within the portal's 12-month window:")
    b = metric_B
    print(f"  addressable buys signed in window: {b['addressable_buys_in_window']['actions']} actions, "
          f"${b['addressable_buys_in_window']['dollars']/1e6:.0f}M")
    print(f"  with NO matching notice: {b['dark_in_window']['actions']} actions = "
          f"{b['dark_in_window']['pct_of_window']}% (${b['dark_in_window']['dollars']/1e6:.0f}M)")
    print(f"  definitive-only in window: {b['definitive_in_window_dark_actions']}/{b['definitive_in_window_actions']} dark")
    print(f"\nwrote award_opp_match.csv ({len(rows)}), dark_awards.csv ({len(dark)}), incompleteness_summary.json")


if __name__ == "__main__":
    main()
