#!/usr/bin/env python3
"""Phase-1 frozen-date replay with negatives → predictions_asof.csv (+ candidate_families_asof.csv).

For each arm, each requirement family, each MONTHLY freeze: score the family's current vehicle
(latest awarded <= freeze) with the model + 5 baselines, record ground truth (a real successor
within HORIZON) and maturity. All features are as-of (≤ freeze). No look-ahead.

Model + baselines (each a per-row score; thresholds/ranking applied in phase1_metrics):
  model              = clock-proximity score (radar)               [the methodology's timing axis]
  b_expiring18/36    = clock within 18 / 36 months                 [naive watchlists]
  b_runrate          = as-of obligation run-rate (rank, portfolio) [big-recurring-spend heuristic]
  b_incumbent_rebuy  = prior family rebuy AND clock within 36mo     [recurrence heuristic]
  b_ldo_runrate      = model * normalized run-rate                  [STRONG simple baseline to beat]

Run: python3 phase1_backtest.py   (offline; uses on-disk + FPDS clock cache)
"""
from __future__ import annotations

import csv
import json
from collections import Counter

import backtest_v2_precision_recall as v2
import phase1_common as p1

EX = p1.EX
HORIZON = p1.HORIZON
d10, months, minus_months = p1.d10, p1.months, p1.minus_months


def current_vehicle(fam, freeze):
    """The family's latest vehicle awarded on/before freeze (the incumbent vehicle)."""
    cur = None
    for v in fam["vehicles"]:
        if d10(v["first"]) and d10(v["first"]) <= freeze:
            cur = v
        else:
            break
    return cur


def prior_rebuys(fam, freeze):
    """# of family vehicles awarded <= freeze, minus 1 (prior observed turnovers)."""
    n = sum(1 for v in fam["vehicles"] if d10(v["first"]) and d10(v["first"]) <= freeze)
    return max(0, n - 1)


def run():
    cache = json.loads(v2.CACHE.read_text()) if v2.CACHE.exists() else {}
    orders = p1.maritime_orders()
    rows = []
    cand = []
    for arm in ("A", "B"):
        fams = p1.build_families(arm)
        allv = [v for f in fams.values() for v in f["vehicles"]]
        cutoff = p1.data_cutoff(allv)
        start = min(d10(v["first"]) for v in allv if d10(v["first"]))
        # normalization for run-rate (per arm) -> a 0..1 baseline score
        rr_all = []
        # iterate monthly freezes
        for fam in fams.values():
            f = max(start, d10(fam["vehicles"][0]["first"]))
            f = f.replace(day=1)
            while f <= cutoff:
                v = current_vehicle(fam, f)
                if v is None:
                    f = minus_months(f, -1); continue
                feat = p1.vehicle_features(v, f, cache, orders)
                if feat is None:
                    f = minus_months(f, -1); continue
                m2c = feat["months_to_clock_asof"]
                # scope: drop vehicles whose ordering period closed > 12 mo before freeze
                if m2c is not None and m2c < -12:
                    f = minus_months(f, -1); continue
                truth = p1.successor_within(fam, v, f, HORIZON)
                succ = p1.successor_of(fam, v)
                succ_first = succ["first"][:10] if succ else ""
                mature = truth or p1.is_mature(f, HORIZON, cutoff)
                model = p1.score_from_clock(m2c)
                rebuys = prior_rebuys(fam, f)
                row = {
                    "arm": arm, "segment": fam["segment"],
                    "segment_primary": fam["segment_primary"], "ring": fam["ring"],
                    "classifier_basis": fam["classifier_basis"],
                    "classifier_confidence": fam["classifier_confidence"],
                    "fidelity": fam["fidelity"],
                    "family_id": fam["family_id"], "freeze": f.isoformat(),
                    "vehicle_piid": v["piid"], "succ_first": succ_first,
                    "incumbent_asof": feat["incumbent_asof"],
                    "months_to_clock_asof": m2c if m2c is not None else "",
                    "clock_asof": feat["clock_asof"], "run_rate_asof": feat["run_rate_asof"],
                    "n_clock_values_asof": feat["n_clock_values_asof"],
                    "prior_rebuys_asof": rebuys,
                    "model": round(model, 4),
                    "b_expiring18": 1 if (m2c is not None and 0 <= m2c <= 18) else 0,
                    "b_expiring36": 1 if (m2c is not None and 0 <= m2c <= 36) else 0,
                    "b_runrate": feat["run_rate_asof"],
                    "b_incumbent_rebuy": 1 if (rebuys >= 1 and m2c is not None and 0 <= m2c <= 36) else 0,
                    "truth": 1 if truth else 0, "mature": 1 if mature else 0,
                }
                rows.append(row)
                rr_all.append(feat["run_rate_asof"])
                cand.append({"arm": arm, "family_id": fam["family_id"], "segment": fam["segment"],
                             "freeze": f.isoformat(), "vehicle_piid": v["piid"],
                             "incumbent_asof": feat["incumbent_asof"], "oblig_asof": feat["oblig_asof"],
                             "clock_asof": feat["clock_asof"], "mature": 1 if mature else 0})
                f = minus_months(f, -1)
        # normalize run-rate -> 0..1 and build the strong combined baseline, per arm
        rr_sorted = sorted(rr_all)
        rmax = rr_sorted[-1] if rr_sorted else 1.0
        for r in rows:
            if r["arm"] != arm:
                continue
            rr_norm = (r["b_runrate"] / rmax) if rmax else 0.0
            r["b_ldo_runrate"] = round(r["model"] * rr_norm, 4)

    cols = ["arm", "segment", "segment_primary", "ring", "classifier_basis", "classifier_confidence",
            "fidelity", "family_id", "freeze", "vehicle_piid", "succ_first", "incumbent_asof",
            "months_to_clock_asof", "clock_asof", "run_rate_asof", "n_clock_values_asof",
            "prior_rebuys_asof", "model", "b_expiring18", "b_expiring36", "b_runrate",
            "b_incumbent_rebuy", "b_ldo_runrate", "truth", "mature"]
    with open(EX / "predictions_asof.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    with open(EX / "candidate_families_asof.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["arm", "family_id", "segment", "freeze", "vehicle_piid",
                                           "incumbent_asof", "oblig_asof", "clock_asof", "mature"])
        w.writeheader(); w.writerows(cand)

    # quick report
    for arm in ("A", "B"):
        ar = [r for r in rows if r["arm"] == arm]
        mat = [r for r in ar if r["mature"]]
        pos = sum(r["truth"] for r in mat)
        print(f"Arm {arm}: rows={len(ar)} mature={len(mat)} positives(mature)={pos} "
              f"censored={len(ar)-len(mat)} families={len({r['family_id'] for r in ar})} "
              f"segments={dict(Counter(r['segment'] for r in ar))}")
    print(f"\nwrote predictions_asof.csv ({len(rows)} rows), candidate_families_asof.csv")


if __name__ == "__main__":
    run()
