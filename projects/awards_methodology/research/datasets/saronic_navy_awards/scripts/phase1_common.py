#!/usr/bin/env python3
"""Phase-1 backtest shared library — requirement-family unit, leakage-safe as-of features.

Reuses the universe/clock/date helpers from backtest_v2_precision_recall.py (v2) and adds the
pieces the v2 cell-level design lacked, per the approved plan:

  - requirement FAMILY as the unit (group vehicles by segment+NAICS4+PSC+builder), with the
    family GROUPING stable (all-time, a labeling construct) but every predictive FEATURE
    recomputed AS-OF the freeze (≤-freeze actions only). v2's all-time incumbent is leaky as a
    feature and is quarantined here.
  - leakage-safe clock: ldo_as_of() (the lastDateToOrder known at freeze from FPDS mod history);
    final_ldo / successor identity / post-freeze mods never touch a feature row.
  - score transform: clip(HORIZON - months_to_clock, 0, HORIZON)/HORIZON  (1.0 = clock at/just
    past freeze, 0 = clock >= HORIZON away) so a PR curve can be swept over the threshold.
  - maturity rule: a (family, freeze) is mature for horizon H only if freeze + H + reporting_lag
    <= data_cutoff (DoD 90d revealed-data lag). A "no successor" before maturity is CENSORED.

Segments: maritime_idiq (FPDS as-of clocks) and ddg_myp = Arm A (high fidelity);
navy_widened = Arm B (low-fidelity breadth, PoP-end clock). Reported separately, never pooled.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date, timedelta

import backtest_v2_precision_recall as v2
import segment_classify as sc

EX = v2.EX
HORIZON = v2.HORIZON          # 36 months
REPORTING_LAG_DAYS = 90       # DoD revealed-data rule
d10, months, minus_months, bkey = v2.d10, v2.months, v2.minus_months, v2.bkey


# ── data cutoff (latest award we can observe) ────────────────────────────────
def data_cutoff(vehicles):
    return max(d10(v["first"]) for v in vehicles if d10(v["first"]))


def is_mature(freeze, horizon, cutoff):
    """Outcome for a `horizon`-month window from `freeze` is fully observable."""
    return minus_months(freeze, -horizon) + timedelta(days=REPORTING_LAG_DAYS) <= cutoff


# ── per-order detail (maritime) for as-of features ───────────────────────────
def maritime_orders():
    """parent_idv_piid -> list of order records (date_signed, recipient, oblig, extent, offers,
    single/multiple). Powers as-of incumbent / run-rate / prior-rebuy without look-ahead."""
    idx = json.loads((EX / "_detail_index.json").read_text())
    by_idv = defaultdict(list)
    for e in idx:
        p = e.get("parent_idv_piid")
        if not p:
            continue
        by_idv[p].append({
            "date": (e.get("date_signed") or "")[:10],
            "recipient": e.get("recipient_name") or "",
            "oblig": e.get("total_obligation") or 0,
            "extent": e.get("extent_competed_description") or "",
            "offers": e.get("number_of_offers_received"),
            "soc": e.get("single_or_multiple_award") or "",
            "solicitation": e.get("solicitation_identifier") or "",
        })
    return by_idv


# ── families: stable grouping (all-time); features are as-of ──────────────────
def family_id(segment, naics, psc, builder):
    raw = f"{segment}|{(naics or '')[:4]}|{psc or ''}|{builder or ''}"
    return segment[:4] + "_" + hashlib.md5(raw.encode()).hexdigest()[:10]


def build_families(arm):
    """arm 'A' -> maritime_idiq + ddg_myp; arm 'B' -> navy_widened. Returns
    {family_id: {segment, fidelity, naics, psc, builder, vehicles:[v,...]}} with vehicles sorted
    by first-award date. Vehicle dicts are v2's (piid, first, builder, naics, psc, oblig,
    clock_final?)."""
    if arm == "A":
        vs = [dict(v, fidelity="high") for v in v2.build_maritime()] + \
             [dict(v, fidelity="high") for v in v2.build_ddg()]
    else:
        vs = [dict(v, fidelity="low") for v in v2.build_widened()]
    fams = {}
    for v in vs:
        fid = family_id(v["segment"], v.get("naics"), v.get("psc"), v["builder"])
        f = fams.setdefault(fid, {"family_id": fid, "segment": v["segment"],
                                  "fidelity": v["fidelity"], "naics": v.get("naics"),
                                  "psc": v.get("psc"), "builder": v["builder"], "vehicles": []})
        f["vehicles"].append(v)
    for f in fams.values():
        f["vehicles"].sort(key=lambda x: x["first"])
        # market-segment reframe: assign a primary segment (A-J) + tags + ring from the locked
        # taxonomy. `segment` (above) stays the CLOCK type (maritime_idiq/ddg_myp/navy_widened);
        # segment_primary is the orthogonal mission axis used for per-segment reporting.
        desc = " ".join((v.get("description") or "") for v in f["vehicles"])
        braw = f["vehicles"][0].get("builder_raw") or ""
        cls = sc.classify_segment(f.get("naics"), f.get("psc"), desc, braw)
        f["segment_primary"] = cls["primary"]
        f["segment_tags"] = cls["tags"]
        f["ring"] = cls["ring"]
        f["classifier_basis"] = cls["classifier_basis"]
        f["classifier_confidence"] = cls["classifier_confidence"]
    return fams


# ── as-of clock (segment-aware, point-in-time) ───────────────────────────────
def clock_asof(v, freeze, cache):
    return v2.clock_as_of(v, freeze, cache)


def clock_history(v, cache):
    """Distinct lastDateToOrder values + the date each was first recorded (maritime), for the
    extension-drift table. ddg/widened: single base==final value."""
    if v["segment"] != "maritime_idiq":
        cf = d10(v.get("clock_final"))
        return [(v["first"][:10], cf)] if cf else []
    seen, out = None, []
    for sgn, ldo, _m in sorted(cache.get(v["piid"], []), key=lambda a: a[0]):
        ld = d10(ldo)
        if ld and ld != seen:
            out.append((sgn, ld))
            seen = ld
    return out


# ── leakage-safe as-of features ──────────────────────────────────────────────
def vehicle_features(v, freeze, cache, orders_by_idv):
    """Feature row for vehicle v at freeze (≤-freeze data only). Returns None if v not yet
    awarded at freeze."""
    fv = d10(v["first"])
    if not fv or fv > freeze:
        return None
    ck = clock_asof(v, freeze, cache)
    m2c = months(ck, freeze) if ck else None
    # as-of obligation run-rate + incumbent + churn (maritime uses per-order detail)
    if v["segment"] == "maritime_idiq":
        orders = [o for o in orders_by_idv.get(v["piid"], []) if d10(o["date"]) and d10(o["date"]) <= freeze]
        oblig = sum(o["oblig"] or 0 for o in orders)
        recip = Counter()
        for o in orders:
            recip[o["recipient"]] += (o["oblig"] or 0)
        incumbent = bkey(max(recip, key=recip.get)) if recip else v["builder"]
    else:
        oblig = (v.get("oblig") or 0) if not isinstance(v.get("oblig"), str) else _num(v.get("oblig"))
        incumbent = v["builder"]
    months_active = max(1.0, months(freeze, fv))
    hist = [(s, l) for s, l in clock_history(v, cache) if d10(s) and d10(s) <= freeze]
    return {
        "clock_asof": ck.isoformat() if ck else "",
        "months_to_clock_asof": m2c,
        "run_rate_asof": round(oblig / months_active, 1),
        "oblig_asof": round(oblig),
        "incumbent_asof": incumbent,
        "n_clock_values_asof": len(hist),     # churn signal (all ≤ freeze)
        "months_active_asof": round(months_active, 1),
    }


def _num(x):
    try:
        return float(x)
    except Exception:
        return 0.0


def score_from_clock(months_to_clock, horizon=HORIZON):
    """Deterministic radar score in [0,1]: 1.0 when the as-of clock is at/just past the freeze,
    0 when >= horizon away or unknown. Monotone in clock proximity → sweepable for PR curves."""
    if months_to_clock is None:
        return 0.0
    return max(0.0, min(horizon, horizon - months_to_clock)) / horizon


# ── ground truth: successor vehicle in the same family ───────────────────────
def successor_of(fam, v):
    """The next vehicle in the family after v (by first-award date), gap >= MIN_GAP months."""
    vs = fam["vehicles"]
    try:
        i = vs.index(v)
    except ValueError:
        return None
    for s in vs[i + 1:]:
        if months(d10(s["first"]), d10(v["first"])) >= v2.MIN_GAP:
            return s
    return None


def successor_within(fam, v, freeze, horizon):
    """True iff a real successor to v was awarded within (freeze, freeze+horizon]."""
    s = successor_of(fam, v)
    if not s:
        return False
    return 0 < months(d10(s["first"]), freeze) <= horizon


if __name__ == "__main__":
    # quick profile / sanity check
    cache = json.loads(v2.CACHE.read_text()) if v2.CACHE.exists() else {}
    ob = maritime_orders()
    for arm in ("A", "B"):
        fams = build_families(arm)
        nveh = sum(len(f["vehicles"]) for f in fams.values())
        multi = sum(1 for f in fams.values() if len(f["vehicles"]) >= 2)
        pos = sum(1 for f in fams.values() for v in f["vehicles"] if successor_of(f, v))
        segs = Counter(f["segment"] for f in fams.values())
        print(f"Arm {arm}: families={len(fams)} vehicles={nveh} multi-vehicle={multi} "
              f"positive_events={pos} segments={dict(segs)}")
    # feature smoke test on one maritime family with an event
    A = build_families("A")
    cutoff = data_cutoff([v for f in A.values() for v in f["vehicles"]])
    print(f"data_cutoff={cutoff}  reporting_lag={REPORTING_LAG_DAYS}d  HORIZON={HORIZON}mo")
    for f in A.values():
        if f["segment"] != "maritime_idiq":
            continue
        pair = next(((v, successor_of(f, v)) for v in f["vehicles"] if successor_of(f, v)), None)
        if not pair:
            continue
        v, s = pair
        fr = v2.minus_months(d10(s["first"]), 12)
        feat = vehicle_features(v, fr, cache, ob)
        gt = successor_within(f, v, fr, HORIZON)
        print(f"sample: fam={f['family_id']} pred={v['piid']} -> succ={s['piid']} freeze={fr} "
              f"months_to_clock={feat['months_to_clock_asof']} score={score_from_clock(feat['months_to_clock_asof']):.2f} "
              f"run_rate={feat['run_rate_asof']} incumbent={feat['incumbent_asof']} truth_within_H={gt}")
        break
