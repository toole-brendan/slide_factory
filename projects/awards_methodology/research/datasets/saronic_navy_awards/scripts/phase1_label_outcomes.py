#!/usr/bin/env python3
"""Phase-1 outcome taxonomy — pull SAM Contract Awards for the Arm-A recompete events and label
each successor event. Distinguishes a real recompete from an incumbent option/extension, and an
open competition from a holder-gated order (FAR 16.505), so "an event happened" isn't conflated
with "a reachable opportunity."

Pull (resumable, cached to raw/sam/contract_awards/<PIID>.json): SAM Contract Awards by PIID with
piidAggregation=yes, sections contractId,coreData,awardDetails (same call the DDG puller proved).
Label (compound, not extent-alone):

  option_or_ordering_period_extension : predecessor has an "EXERCISE AN OPTION" mod (code G) near
                                        the successor window (the "successor" is really retention)
  vehicle_recompete_open              : successor base award competed (FULL&OPEN / SAP) AND not a
                                        holder-only multiple-award order
  successor_vehicle_holder_only       : successor is a multiple-award IDV order (reachable only by holders)
  bridge_or_extension                 : successor NOT COMPETED + <=1 offer + short PoP
  vehicle_recompete_limited_or_set_aside : competed-with-exclusions / set-aside
  unknown_manual_review               : insufficient SAM fields

Run: python3 phase1_label_outcomes.py   (live SAM pulls for uncached PIIDs; key from .env)
"""
from __future__ import annotations

import csv
import json
from urllib.parse import urlencode

import _common
import backtest_v2_precision_recall as v2
import phase1_common as p1

EX = p1.EX
RAW = v2.ROOT / "raw" / "sam" / "contract_awards"
CA = "https://api.sam.gov/contract-awards/v1/search"


def deep(d, *path):
    for k in path:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return None
    return d


def pull_piid(piid, key):
    path = RAW / f"{piid}.json"
    if path.exists():
        return json.loads(path.read_text())
    recs, off = [], 0
    while off < 300:
        url = CA + "?" + urlencode({"api_key": key, "piid": piid, "piidAggregation": "yes",
                                    "includeSections": "contractId,coreData,awardDetails",
                                    "limit": 100, "offset": off})
        txt, st = _common.http_get(url, headers={"Accept": "application/json"})
        if not txt or st != 200:
            break
        b = json.loads(txt)
        page = b.get("awardSummary") or []
        if not page:
            break
        recs.extend(r for r in page if deep(r, "contractId", "piid") == piid)
        if len(page) < 100:
            break
        off += 100
    out = {"piid": piid, "n_records": len(recs), "records": recs}
    RAW.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1))
    return out


def summarize(data):
    """Base-award competition posture + whether any mod exercised an option."""
    recs = data.get("records", [])
    if not recs:
        return None
    base = min(recs, key=lambda r: (deep(r, "contractId", "modificationNumber") or "0"))
    ci = deep(base, "coreData", "competitionInformation") or {}
    option = any((deep(r, "contractId", "reasonForModification", "name") or "").upper() == "EXERCISE AN OPTION"
                 for r in recs)
    return {
        "extent": (deep(ci, "extentCompeted", "name") or "").upper(),
        "sol_proc": (deep(ci, "solicitationProcedures", "name") or "").upper(),
        "offers": deep(ci, "numberOfOffersReceived"),
        "idv_multiple": (deep(base, "coreData", "contractData", "multipleOrSingleAwardIDV", "name")
                         or deep(base, "coreData", "awardOrIDVType", "name") or "").upper(),
        "has_option_mod": option, "n_records": len(recs),
    }


def label(succ_s):
    if not succ_s:
        return "unknown_manual_review"
    ext, sp = succ_s["extent"], succ_s["sol_proc"]
    if "MULTIPLE" in succ_s["idv_multiple"]:
        return "successor_vehicle_holder_only"
    if "NOT COMPETED" in ext and (succ_s["offers"] in (1, "1", None)) and "ONLY ONE" in sp:
        return "bridge_or_extension"
    if "FULL AND OPEN" in ext and "EXCLUSION" not in ext:
        return "vehicle_recompete_open"
    if "COMPETED" in ext or "EXCLUSION" in ext or "SET ASIDE" in ext or "SET-ASIDE" in ext:
        return "vehicle_recompete_limited_or_set_aside"
    if "NOT COMPETED" in ext:
        return "vehicle_recompete_limited_or_set_aside"
    return "unknown_manual_review"


def main():
    key = _common.env("SAM_API_KEY")
    fams = p1.build_families("A")
    events = []      # (family, pred, succ)
    for f in fams.values():
        for v in f["vehicles"]:
            s = p1.successor_of(f, v)
            if s and p1.d10(s["first"]) and p1.d10(s["first"]) <= p1.data_cutoff(
                    [vv for ff in fams.values() for vv in ff["vehicles"]]):
                events.append((f, v, s))
    piids = {p for _f, pred, succ in events for p in (pred["piid"], succ["piid"])}
    print(f"Arm A events: {len(events)}; unique PIIDs to resolve: {len(piids)}")
    summ = {}
    for i, piid in enumerate(sorted(piids), 1):
        # DDG PIIDs are already on disk under the ddg dataset; try saronic raw first, else pull
        data = pull_piid(piid, key)
        summ[piid] = summarize(data)
        if i % 10 == 0:
            print(f"  resolved {i}/{len(piids)}")
    rows = []
    for f, pred, succ in events:
        ss = summ.get(succ["piid"])
        ps = summ.get(pred["piid"])
        lab = label(ss)
        if ps and ps.get("has_option_mod") and lab in ("unknown_manual_review",):
            lab = "option_or_ordering_period_extension"
        rows.append({"family_id": f["family_id"], "segment": f["segment"],
                     "predecessor": pred["piid"], "successor": succ["piid"],
                     "succ_award": succ["first"], "succ_extent": (ss or {}).get("extent", ""),
                     "succ_sol_proc": (ss or {}).get("sol_proc", ""),
                     "succ_multiple": (ss or {}).get("idv_multiple", ""),
                     "pred_has_option_mod": (ps or {}).get("has_option_mod", ""),
                     "outcome_label": lab})
    rows.sort(key=lambda r: r["succ_award"])
    with open(EX / "outcome_labels.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    # successor_links.csv (the matcher's predecessor->successor links)
    with open(EX / "successor_links.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["family_id", "segment", "predecessor", "successor", "succ_award", "outcome_label"])
        w.writeheader()
        w.writerows({k: r[k] for k in ("family_id", "segment", "predecessor", "successor", "succ_award", "outcome_label")} for r in rows)
    from collections import Counter
    print("\noutcome taxonomy (Arm A events):")
    for lab, n in Counter(r["outcome_label"] for r in rows).most_common():
        print(f"  {lab:<40} {n}")
    print("\nwrote outcome_labels.csv, successor_links.csv")


if __name__ == "__main__":
    main()
