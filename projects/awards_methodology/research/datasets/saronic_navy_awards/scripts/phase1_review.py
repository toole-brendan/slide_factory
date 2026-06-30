#!/usr/bin/env python3
"""Phase-1 error review + semantic self-consistency.

- fp_review.csv : negative episodes (no successor) the model flagged at a mature freeze — the
  false positives — annotated with clock, run-rate, and extension-drift (a known FP cause).
- fn_review.csv : positive episodes the model never flagged — the misses.
- semantic self-consistency: how the (NAICS4+PSC+builder) family key behaves vs a looser
  (builder+NAICS4) requirement proxy on Arm A vehicle pairs. AUTO-PROXY, not human-labeled —
  a sanity check; `labeled_pairs.csv` is emitted as a seed for manual adjudication.

Run: python3 phase1_review.py
"""
from __future__ import annotations

import csv
from collections import defaultdict

import phase1_common as p1
import phase1_metrics as m

EX = p1.EX


def reviews():
    ep, _ = m.load_episodes()
    drift = {r["vehicle_piid"]: r for r in csv.DictReader(open(EX / "extension_drift.csv"))} \
        if (EX / "extension_drift.csv").exists() else {}
    fps, fns = [], []
    for e in ep.values():
        if e["arm"] != "A":
            continue
        mr = e["mature_rows"]
        fired = any(float(r["model"]) > 0 for r in mr)
        if e["is_pos"] and not fired:
            r0 = e["rows"][-1]
            fns.append({"segment": e["seg"], "family_id": e["fid"], "vehicle": r0["vehicle_piid"],
                        "succ_first": e["succ_first"], "clock_asof_last": r0["clock_asof"],
                        "months_to_clock_last": r0["months_to_clock_asof"]})
        elif (not e["is_pos"]) and mr and fired:
            r0 = max(mr, key=lambda r: float(r["model"]))
            dr = drift.get(r0["vehicle_piid"], {})
            fps.append({"segment": e["seg"], "family_id": e["fid"], "vehicle": r0["vehicle_piid"],
                        "freeze": r0["freeze"], "clock_asof": r0["clock_asof"],
                        "months_to_clock": r0["months_to_clock_asof"], "run_rate_asof": r0["run_rate_asof"],
                        "ldo_outward_shifts": dr.get("n_outward_shifts", ""),
                        "ldo_months_drift": dr.get("months_drift", "")})
    for name, rows in (("fp_review.csv", fps), ("fn_review.csv", fns)):
        if rows:
            with open(EX / name, "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"fp_review: {len(fps)} false-positive negative-episodes; fn_review: {len(fns)} missed positives")
    drifty = sum(1 for r in fps if str(r.get("ldo_outward_shifts") or "0") not in ("", "0"))
    print(f"  of FPs, {drifty}/{len(fps)} are on vehicles whose ordering clock drifted outward (a known FP cause)")
    return fps, fns


def semantic_selfcheck():
    fams = p1.build_families("A")
    vehs = [v for f in fams.values() for v in f["vehicles"] if v["segment"] == "maritime_idiq"]
    fam_of = {v["piid"]: f["family_id"] for f in fams.values() for v in f["vehicles"]}
    pairs, seed = [], []
    tp = fp = fn = 0
    for a in vehs:
        for s in vehs:
            if a["piid"] == s["piid"]:
                continue
            gap = p1.months(p1.d10(s["first"]), p1.d10(a["first"]))
            if not (18 <= gap <= 72):
                continue
            matched = fam_of[a["piid"]] == fam_of[s["piid"]]
            proxy = (a["builder"] == s["builder"]) and ((a.get("naics") or "")[:4] == (s.get("naics") or "")[:4])
            if matched and proxy:
                tp += 1
            elif matched and not proxy:
                fp += 1
            elif (not matched) and proxy:
                fn += 1
            if matched or proxy:
                seed.append({"predecessor": a["piid"], "successor": s["piid"], "gap_mo": round(gap),
                             "matcher_linked": int(matched), "proxy_same_requirement": int(proxy),
                             "manual_label_TODO": ""})
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    pl, ph = m.wilson(tp, tp + fp); rl, rh = m.wilson(tp, tp + fn)
    if seed:
        with open(EX / "labeled_pairs.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(seed[0].keys())); w.writeheader(); w.writerows(seed)
    with open(EX / "semantic_match_metrics.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["metric", "value", "ci_lo", "ci_hi", "tp", "fp", "fn", "note"])
        w.writerow(["precision_vs_proxy", round(prec, 3), round(pl, 3), round(ph, 3), tp, fp, fn, "AUTO-PROXY not human-labeled"])
        w.writerow(["recall_vs_proxy", round(rec, 3), round(rl, 3), round(rh, 3), tp, fp, fn, "AUTO-PROXY not human-labeled"])
    print(f"semantic self-consistency (NAICS4+PSC+builder key vs builder+NAICS4 proxy): "
          f"precision={prec:.2f}[{pl:.2f},{ph:.2f}] recall={rec:.2f}[{rl:.2f},{rh:.2f}] (tp={tp} fp={fp} fn={fn}) "
          f"-> seed labeled_pairs.csv for manual review")


if __name__ == "__main__":
    reviews()
    semantic_selfcheck()
    print("wrote fp_review.csv, fn_review.csv, semantic_match_metrics.csv, labeled_pairs.csv")
