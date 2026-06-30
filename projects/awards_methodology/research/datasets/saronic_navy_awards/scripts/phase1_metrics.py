#!/usr/bin/env python3
"""Phase-1 metrics — family/episode-level (primary), per-segment, never pooled.

Reads predictions_asof.csv (cell-level: family×freeze×vehicle). Rolls up to VEHICLE-EPISODES
(each family-incumbent period = one episode) — the honest unit, since a vehicle flagged for N
consecutive months is not N independent predictions. Reports, per (arm, segment):

  - cohort counts: positive / negative / censored episodes, families
  - episode-level confusion for binary scorers (model=clock-within-H, expiring18, expiring36,
    incumbent_rebuy): precision/recall/F1 with Wilson + family-bootstrap CIs; median first-alert lead
  - precision@K (freeze-date portfolio) for ranking scorers (model, run-rate, ldo×runrate, rebuy)
  - PR-AUC (episode-level) for continuous scorers (model, ldo×runrate)
  - extension_drift.csv: base vs final lastDateToOrder, # outward extensions, months of drift

NOTE: the timing-only `model` binary flag == expiring36 by construction; the model can only beat
expiring36 via RANKING (precision@K / PR-AUC). The strong baseline `b_ldo_runrate` is the bar.
Cell-level numbers (v2-style) are emitted ONLY as an operating-burden diagnostic, clearly labeled.
"""
from __future__ import annotations

import csv
import math
import random
from collections import defaultdict

import backtest_v2_precision_recall as v2
import phase1_common as p1

random.seed(1234)
EX = p1.EX
HORIZON = p1.HORIZON
d10, months = p1.d10, p1.months
BINARY = ["model", "b_expiring18", "b_expiring36", "b_incumbent_rebuy"]
RANKERS = ["model", "b_runrate", "b_ldo_runrate", "b_incumbent_rebuy"]


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - m) / d), min(1.0, (c + m) / d))


def fired(rows, scorer, thr):
    return any(float(r[scorer]) >= thr for r in rows)


def load_episodes():
    rows = list(csv.DictReader(open(EX / "predictions_asof.csv")))
    ep = defaultdict(lambda: {"rows": [], "succ_first": "", "seg": "", "arm": "", "fid": ""})
    for r in rows:
        k = (r["arm"], r["family_id"], r["vehicle_piid"])
        e = ep[k]
        e["rows"].append(r); e["succ_first"] = r["succ_first"]; e["seg"] = r["segment"]
        e["segp"] = r.get("segment_primary", "U"); e["ring"] = r.get("ring", "")
        e["cbasis"] = r.get("classifier_basis", ""); e["cconf"] = r.get("classifier_confidence", "")
        e["arm"] = r["arm"]; e["fid"] = r["family_id"]
    for e in ep.values():
        e["is_pos"] = e["succ_first"] != ""
        e["mature_rows"] = [r for r in e["rows"] if r["mature"] == "1"]
    return ep, rows


# binary thresholds: model/expiring use clock-window flags; "model" fires on clock-within-HORIZON
THR = {"model": 1e-9, "b_expiring18": 1, "b_expiring36": 1, "b_incumbent_rebuy": 1}


def confusion(eps, scorer):
    """Episode-level TP/FP/FN/TN + the per-episode first-alert lead list (TPs)."""
    tp = fp = fn = tn = 0
    leads = []
    for e in eps:
        mr = e["mature_rows"]
        if e["is_pos"]:
            if fired(mr, scorer, THR[scorer]):
                tp += 1
                hit = [r for r in mr if float(r[scorer]) >= THR[scorer]]
                f0 = min(d10(r["freeze"]) for r in hit); sf = d10(e["succ_first"])
                if sf:
                    leads.append(months(sf, f0))
            else:
                fn += 1
        elif mr:
            if fired(mr, scorer, THR[scorer]):
                fp += 1
            else:
                tn += 1
    return tp, fp, fn, tn, leads


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


def boot_family_ci(eps, scorer, stat, B=2000):
    """Bootstrap a stat resampling whole FAMILIES (clusters), not episodes."""
    byfam = defaultdict(list)
    for e in eps:
        byfam[e["fid"]].append(e)
    fams = list(byfam)
    if len(fams) < 3:
        return ("", "")
    vals = []
    for _ in range(B):
        samp = [e for _ in fams for e in byfam[random.choice(fams)]]
        tp, fp, fn, tn, leads = confusion(samp, scorer)
        p, r, f = prf(tp, fp, fn)
        v = {"precision": p, "recall": r, "lead": (sorted(leads)[len(leads)//2] if leads else 0.0)}[stat]
        vals.append(v)
    vals.sort()
    return (round(vals[int(0.025 * B)], 3), round(vals[int(0.975 * B)], 3))


def precision_at_k(rows, scorer, k):
    """Freeze-date portfolio: rank mature in-scope vehicles by scorer, top-K, cell-truth precision."""
    byf = defaultdict(list)
    for r in rows:
        if r["mature"] == "1":
            byf[r["freeze"]].append(r)
    precs = []
    for fr, rs in byf.items():
        if len(rs) < k:
            continue
        top = sorted(rs, key=lambda r: float(r[scorer]), reverse=True)[:k]
        precs.append(sum(int(r["truth"]) for r in top) / k)
    return (sum(precs) / len(precs)) if precs else 0.0


def pr_auc(eps, scorer):
    """Episode-level PR-AUC: episode score = max scorer over its mature rows; sweep threshold."""
    pts = []
    for e in eps:
        mr = e["mature_rows"]
        if not (e["is_pos"] or mr):
            continue
        s = max((float(r[scorer]) for r in mr), default=0.0)
        pts.append((s, e["is_pos"]))
    P = sum(1 for _s, y in pts if y)
    if P == 0:
        return 0.0
    pts.sort(key=lambda x: -x[0])
    tp = fp = 0; prev_r = 0.0; auc = 0.0; last_p = 1.0
    for s, y in pts:
        tp += int(y); fp += int(not y)
        prec = tp / (tp + fp); rec = tp / P
        auc += (rec - prev_r) * (prec + last_p) / 2
        prev_r = rec; last_p = prec
    return auc


def extension_drift(rows):
    """Per maritime vehicle: base vs final lastDateToOrder, #outward shifts, months drift."""
    cache = __import__("json").loads(v2.CACHE.read_text()) if v2.CACHE.exists() else {}
    seen = set(); out = []
    for r in rows:
        if r["segment"] != "maritime_idiq" or r["vehicle_piid"] in seen:
            continue
        seen.add(r["vehicle_piid"])
        hist = [(s, l) for s, l in p1.clock_history({"segment": "maritime_idiq", "piid": r["vehicle_piid"], "first": r["freeze"]}, cache)]
        if not hist:
            continue
        base, final = hist[0][1], hist[-1][1]
        drift = months(final, base)
        out.append({"vehicle_piid": r["vehicle_piid"], "base_ldo": base.isoformat(),
                    "final_ldo": final.isoformat(), "n_clock_values": len(hist),
                    "n_outward_shifts": sum(1 for i in range(1, len(hist)) if hist[i][1] > hist[i-1][1]),
                    "months_drift": drift})
    return out


# HEADLINE reporting axis: Arm A on its high-fidelity CLOCK segments (maritime_idiq/ddg_myp);
# Arm B on mission segment_primary (A-J). Arm A's A-J labels are code-only (no descriptions) and
# are NOT used for headline mission metrics — only the diagnostic crosswalk. Never pool A and B.
def report_seg(arm, clock_seg, segp):
    return clock_seg if arm == "A" else segp


def report_axis(arm):
    return "clock_segment" if arm == "A" else "segment_primary"


def write_crosswalk(ep):
    """Diagnostic both-axis crosstab (arm x clock_segment x segment_primary) with classifier
    provenance and tiny-slice suppression. This is the ONLY place Arm A's A-J mission labels
    appear — flagged with basis/confidence, never used for headline metrics."""
    from collections import Counter
    cross = defaultdict(list)
    for e in ep.values():
        cross[(e["arm"], e["seg"], e["segp"])].append(e)
    cols = ["arm", "clock_segment", "segment_primary", "ring", "n_families", "n_positive",
            "n_negative_mature", "n_censored", "classifier_basis", "classifier_confidence", "suppressed"]
    out = []
    for (arm, cseg, segp), eps in sorted(cross.items()):
        npos = sum(1 for e in eps if e["is_pos"])
        nneg = sum(1 for e in eps if (not e["is_pos"]) and e["mature_rows"])
        ncens = sum(1 for e in eps if (not e["is_pos"]) and not e["mature_rows"])
        nfam = len({e["fid"] for e in eps})
        basis = Counter(e["cbasis"] for e in eps).most_common(1)[0][0]
        conf = Counter(e["cconf"] for e in eps).most_common(1)[0][0]
        ring = next((e["ring"] for e in eps), "")
        supp = "yes" if (npos < 10 or nfam < 30) else "no"
        out.append({"arm": arm, "clock_segment": cseg, "segment_primary": segp, "ring": ring,
                    "n_families": nfam, "n_positive": npos, "n_negative_mature": nneg,
                    "n_censored": ncens, "classifier_basis": basis,
                    "classifier_confidence": conf, "suppressed": supp})
    with open(EX / "segment_crosswalk.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(out)
    nsupp = sum(1 for r in out if r["suppressed"] == "yes")
    print(f"\nsegment_crosswalk.csv: {len(out)} (arm x clock_seg x segment_primary) cells, "
          f"{nsupp} suppressed (n_pos<10 or n_families<30)")


def main():
    ep, rows = load_episodes()
    out = [["arm", "report_axis", "segment", "metric", "scorer", "k_or_thr",
            "value", "ci_lo", "ci_hi", "n_pos", "n_neg"]]
    # group episodes by (arm, HEADLINE segment)
    byseg = defaultdict(list)
    for e in ep.values():
        byseg[(e["arm"], report_seg(e["arm"], e["seg"], e["segp"]))].append(e)
    rows_by_seg = defaultdict(list)
    for r in rows:
        rs = report_seg(r["arm"], r["segment"], r.get("segment_primary", "U"))
        rows_by_seg[(r["arm"], rs)].append(r)

    print(f"{'arm/seg':<22}{'scorer':<18}{'prec':>14}{'rec':>14}{'F1':>6}{'lead_mo':>9}")
    for (arm, seg), eps in sorted(byseg.items()):
        ax = report_axis(arm)
        npos = sum(1 for e in eps if e["is_pos"])
        nneg = sum(1 for e in eps if (not e["is_pos"]) and e["mature_rows"])
        ncens = sum(1 for e in eps if (not e["is_pos"]) and not e["mature_rows"])
        nfam = len({e["fid"] for e in eps})
        out.append([arm, ax, seg, "cohort", "-", "-", "", "", "", npos, nneg])
        print(f"\n[{arm}/{seg}] ({ax}) families={nfam} positive_ep={npos} negative_ep={nneg} censored_ep={ncens}")
        for sc in BINARY:
            tp, fp, fn, tn, leads = confusion(eps, sc)
            p, r, f = prf(tp, fp, fn)
            pl, ph = wilson(tp, tp + fp); rl, rh = wilson(tp, tp + fn)
            med = sorted(leads)[len(leads)//2] if leads else ""
            llo, lhi = boot_family_ci(eps, sc, "lead") if leads else ("", "")
            out += [[arm, ax, seg, "precision", sc, "bin", round(p, 3), round(pl, 3), round(ph, 3), npos, nneg],
                    [arm, ax, seg, "recall", sc, "bin", round(r, 3), round(rl, 3), round(rh, 3), npos, nneg],
                    [arm, ax, seg, "f1", sc, "bin", round(f, 3), "", "", npos, nneg],
                    [arm, ax, seg, "median_lead_mo", sc, "bin", med, llo, lhi, npos, nneg]]
            print(f"  {'':<20}{sc:<18}{p:>6.2f}[{pl:.2f},{ph:.2f}]{r:>6.2f}[{rl:.2f},{rh:.2f}]{f:>6.2f}{str(med):>9}")
        for sc in RANKERS:
            for k in (5, 10, 20):
                pk = precision_at_k(rows_by_seg[(arm, seg)], sc, k)
                out.append([arm, ax, seg, "precision_at_k", sc, k, round(pk, 3), "", "", npos, nneg])
            auc = pr_auc(eps, sc)
            out.append([arm, ax, seg, "pr_auc", sc, "-", round(auc, 3), "", "", npos, nneg])
        print("  precision@10:", {sc: round(precision_at_k(rows_by_seg[(arm, seg)], sc, 10), 2) for sc in RANKERS})
        print("  PR-AUC:", {sc: round(pr_auc(eps, sc), 2) for sc in ("model", "b_ldo_runrate")})

    with open(EX / "metrics_by_segment.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(out)
    write_crosswalk(ep)
    drift = extension_drift(rows)
    with open(EX / "extension_drift.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["vehicle_piid", "base_ldo", "final_ldo", "n_clock_values",
                                           "n_outward_shifts", "months_drift"]); w.writeheader(); w.writerows(drift)
    ndrift = sum(1 for r in drift if r["n_outward_shifts"] > 0)
    print(f"\nextension_drift: {ndrift}/{len(drift)} maritime vehicles had >=1 outward LDO shift "
          f"(median drift {sorted(r['months_drift'] for r in drift)[len(drift)//2] if drift else 0:.0f}mo)")
    print("wrote metrics_by_segment.csv, extension_drift.csv")


if __name__ == "__main__":
    main()
