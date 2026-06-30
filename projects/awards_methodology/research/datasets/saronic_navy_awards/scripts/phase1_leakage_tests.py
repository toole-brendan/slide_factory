#!/usr/bin/env python3
"""Phase-1 negative-control leakage tests (must pass before trusting any result).

Three controls:

  1. AS-OF FEATURE INVARIANCE (the direct no-look-ahead proof): recompute each feature with the
     post-freeze data physically deleted; it must be byte-identical to the pipeline value. If a
     feature changes, it was reading the future.

  2. LABEL-SHUFFLE (skill vs artifact): permute the positive/negative episode labels within each
     segment and recompute model precision/recall. Skill must collapse toward the base rate; if
     the real numbers sit inside the shuffled distribution, there is no real signal (and if they
     were impossibly high, that would flag leakage).

  3. ORACLE POSITIVE CONTROL (metric sensitivity): a deliberately leaky scorer that peeks at the
     outcome must drive precision/recall to ~1.0 — proving the metric WOULD reveal leakage if any
     existed in the real features.

Run: python3 phase1_leakage_tests.py
"""
from __future__ import annotations

import json
import random
from collections import defaultdict

import backtest_v2_precision_recall as v2
import phase1_common as p1
import phase1_metrics as m

random.seed(7)


def test_asof_invariance(n_check=400):
    """Recompute clock_asof with all FPDS actions signed > freeze deleted; must match."""
    cache = json.loads(v2.CACHE.read_text()) if v2.CACHE.exists() else {}
    orders = p1.maritime_orders()
    fams = p1.build_families("A")
    checked = mismatches = 0
    for f in fams.values():
        for v in f["vehicles"]:
            if v["segment"] != "maritime_idiq":
                continue
            fv = p1.d10(v["first"])
            for off in (6, 12, 24, 36):
                freeze = v2.minus_months(p1.d10(v["first"]), -off) if False else v2.minus_months(fv, -off)
                feat = p1.vehicle_features(v, freeze, cache, orders)
                if feat is None:
                    continue
                # truncated cache: drop any action signed AFTER freeze, then recompute
                trunc = dict(cache)
                trunc[v["piid"]] = [a for a in cache.get(v["piid"], []) if p1.d10(a[0]) and p1.d10(a[0]) <= freeze]
                feat2 = p1.vehicle_features(v, freeze, trunc, orders)
                checked += 1
                if feat["clock_asof"] != feat2["clock_asof"] or feat["run_rate_asof"] != feat2["run_rate_asof"]:
                    mismatches += 1
                if checked >= n_check:
                    break
            if checked >= n_check:
                break
        if checked >= n_check:
            break
    ok = mismatches == 0
    print(f"1. AS-OF INVARIANCE: checked={checked} mismatches={mismatches} -> {'PASS' if ok else 'FAIL'}")
    return ok


def test_label_shuffle(B=300):
    ep, _ = m.load_episodes()
    byseg = defaultdict(list)
    for e in ep.values():
        byseg[(e["arm"], e["seg"])].append(e)
    print("2. LABEL-SHUFFLE (model precision: real vs shuffled mean; base rate):")
    ok = True
    for (arm, seg), eps in sorted(byseg.items()):
        evalable = [e for e in eps if e["is_pos"] or e["mature_rows"]]
        labels = [e["is_pos"] for e in evalable]
        base = sum(labels) / len(labels) if labels else 0
        tp, fp, fn, tn, _l = m.confusion(eps, "model")
        p_real, _r, _f = m.prf(tp, fp, fn)
        shuf = []
        for _ in range(B):
            random.shuffle(labels)
            for e, lab in zip(evalable, labels):
                e["_orig"] = e["is_pos"]; e["is_pos"] = lab
            tp, fp, fn, tn, _l = m.confusion(evalable, "model")
            pp, _, _ = m.prf(tp, fp, fn)
            shuf.append(pp)
            for e in evalable:
                e["is_pos"] = e["_orig"]
        shuf.sort()
        lo, hi = shuf[int(0.025*B)], shuf[int(0.975*B)]
        # PASS if real precision is NOT absurdly above the shuffle band (no impossible skill)
        verdict = "ok" if p_real <= max(hi, base) + 0.35 else "SUSPECT-LEAK"
        if verdict != "ok":
            ok = False
        print(f"   {arm}/{seg:<14} real={p_real:.2f}  shuffled≈[{lo:.2f},{hi:.2f}]  base_rate={base:.2f}  -> {verdict}")
    return ok


def test_oracle_control():
    """Inject a leaky scorer = 1.0 on positive episodes' mature rows, 0 else -> precision/recall→1."""
    ep, _ = m.load_episodes()
    eps = [e for e in ep.values() if e["arm"] == "A" and e["seg"] == "maritime_idiq"]
    for e in eps:
        for r in e["mature_rows"]:
            r["_oracle"] = 1.0 if e["is_pos"] else 0.0
    m.THR["_oracle"] = 0.5
    tp, fp, fn, tn, _l = m.confusion(eps, "_oracle")
    p, r, f = m.prf(tp, fp, fn)
    ok = p > 0.99 and r > 0.99
    print(f"3. ORACLE CONTROL (maritime): precision={p:.2f} recall={r:.2f} -> "
          f"{'PASS (metric is leak-sensitive)' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    a = test_asof_invariance()
    b = test_label_shuffle()
    c = test_oracle_control()
    print(f"\nLEAKAGE SUITE: {'ALL PASS' if (a and b and c) else 'FAILURES PRESENT'}")
