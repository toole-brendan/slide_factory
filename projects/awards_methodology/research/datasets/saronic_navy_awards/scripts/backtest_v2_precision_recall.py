#!/usr/bin/env python3
"""WIDENED PRECISION/RECALL BACKTEST (v2) for the recompete-timing methodology.

The v1 backtest (backtest_recompete.py) only replays KNOWN predecessor->successor
pairs, so it measures *recall* on recompetes we already know happened — it cannot
see false positives (vehicles the radar would flag that were never recompeted). A
radar that flags everything scores 100% there. v2 fixes that by scoring EVERY
material vehicle at a grid of historical freeze dates.

DESIGN (no look-ahead):
  Universe per segment = every vehicle >= $5M reconstructed from the on-disk award
  corpus. For monthly freeze dates f (capped so outcomes are observable), score
  every vehicle "in scope" at f (awarded, ordering period not long past):
    radar flag at f : the vehicle's ordering-period end (last_date_to_order) KNOWN
                      as of f — using ONLY FPDS actions signed <= f (maritime) or
                      the block completion set at award (ddg) — falls within
                      [f, f+HORIZON]  ->  "recompete coming".
    ground truth    : a real successor (same builder family) was actually awarded
                      within [f, f+HORIZON].
  -> pooled confusion matrix (TP/FP/FN/TN) -> precision / recall / F1, PLUS an
  event-level view (per known recompete: anticipable at t-6/12/18/24 and the lead).

Segments: maritime_idiq (parent-IDV ordering vehicles, FPDS point-in-time clocks)
and ddg_myp (DDG-51 multiyear block recompetes; clock = block completion at award).

Inputs : extracted/_detail_index.json, market_tiers.csv, _fpds_timelines.json
         (FPDS cache, extended on the fly), ../ddg51_.../extracted/ddg_myp_recompete_provenance.csv
Outputs: extracted/backtest_v2_events.csv, backtest_v2_confusion.csv, backtest_v2_summary.json
Run    : python3 backtest_v2_precision_recall.py   (pulls missing FPDS timelines; resumable)
"""
from __future__ import annotations

import csv
import json
import re
import time
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
from urllib import parse
from urllib.request import Request, urlopen
from xml.etree.ElementTree import fromstring

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "extracted"
DDG_EX = ROOT.parent / "ddg51_recompete_cadence" / "extracted"
CACHE = EX / "_fpds_timelines.json"

MIN_OBLIG = 5e6
MIN_GAP = 18
HORIZON = 36
NS = {"a": "http://www.w3.org/2005/Atom", "ns1": "https://www.fpds.gov/FPDS"}
BASE = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
HDRS = {"User-Agent": "awards-methodology-backtest/2.0"}


# ── date helpers ─────────────────────────────────────────────────────────────
def d10(s):
    try:
        return date.fromisoformat((s or "")[:10])
    except Exception:
        return None


def months(a: date, b: date) -> float:
    return round((a - b).days / 30.4, 1)


def minus_months(d: date, n: int) -> date:
    m = d.month - 1 - n
    y = d.year + m // 12
    m = m % 12 + 1
    return date(y, m, min(d.day, 28))


def bkey(name: str) -> str:
    n = re.sub(r"[^A-Z ]", "", (name or "").upper())
    n = re.sub(r"\b(INC|LLC|CORP|CORPORATION|CO|COMPANY|LTD|LP|THE|INCORPORATED)\b", "", n)
    return re.sub(r"\s+", "", n)[:12]


# ── FPDS per-action ordering-period timeline (cached, resumable) ──────────────
def _f(elem, path):
    x = elem.find(path, NS)
    return x.text if x is not None and x.text else None


def fetch(q, start):
    url = f"{BASE}&{parse.urlencode({'q': q})}&start={start}"
    for attempt in range(4):
        try:
            with urlopen(Request(url, headers=HDRS), timeout=90) as r:
                return r.read().decode("utf-8")
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return None


def pull_timeline(piid):
    """[(signed_iso, lastDateToOrder_iso, mod)] per IDV action."""
    acts, start = [], 0
    while start // 10 < 40:
        text = fetch(f'PIID:"{piid}"', start)
        if not text:
            break
        try:
            root = fromstring(text)
        except Exception:
            break
        entries = root.findall("a:entry", NS)
        if not entries:
            break
        for entry in entries:
            content = entry.find("a:content", NS)
            idv = content.find(".//ns1:IDV", NS) if content is not None else None
            if idv is None:
                continue
            sgn = (_f(idv, ".//ns1:signedDate") or "")[:10]
            ldo = (_f(idv, ".//ns1:lastDateToOrder") or "")[:10]
            mod = _f(idv, ".//ns1:modNumber") or "0"
            if sgn:
                acts.append((sgn, ldo, mod))
        start += 10
        time.sleep(0.3)
    return acts


def ldo_as_of(acts, freeze: date):
    """lastDateToOrder KNOWN as of freeze: value on the latest action signed <= freeze."""
    best_sgn, best_ldo = None, None
    for sgn, ldo, _m in acts:
        sd = d10(sgn)
        if sd and sd <= freeze and ldo:
            if best_sgn is None or sd > best_sgn:
                best_sgn, best_ldo = sd, ldo
    return d10(best_ldo) if best_ldo else None


def final_ldo(acts):
    vals = [d10(ldo) for _s, ldo, _m in acts if ldo]
    return max([v for v in vals if v], default=None)


# ── segment builders ─────────────────────────────────────────────────────────
def build_maritime():
    idx = json.loads((EX / "_detail_index.json").read_text())
    tier = {r["generated_internal_id"]: r["tier"]
            for r in csv.DictReader(open(EX / "market_tiers.csv"))}
    veh = defaultdict(lambda: {"oblig": 0.0, "recip": defaultdict(float),
                               "naics": Counter(), "psc": Counter(), "first": None, "tiers": Counter()})
    for e in idx:
        p = e.get("parent_idv_piid")
        if not p:
            continue
        v = veh[p]
        ob = e.get("total_obligation") or 0
        v["oblig"] += ob
        if e.get("recipient_name"):
            v["recip"][e["recipient_name"]] += ob
        if e.get("naics_code"):
            v["naics"][e["naics_code"]] += 1
        if e.get("psc_code"):
            v["psc"][e["psc_code"]] += 1
        t = tier.get(e.get("generated_internal_id"))
        if t:
            v["tiers"][t] += 1
        ds = (e.get("date_signed") or "")[:10]
        if ds:
            v["first"] = min(v["first"], ds) if v["first"] else ds
    out = []
    for p, v in veh.items():
        if v["oblig"] < MIN_OBLIG or not v["first"]:
            continue
        builder = max(v["recip"], key=v["recip"].get) if v["recip"] else "?"
        out.append({"segment": "maritime_idiq", "piid": p, "first": v["first"],
                    "builder": bkey(builder), "builder_raw": builder,
                    "naics": v["naics"].most_common(1)[0][0] if v["naics"] else "",
                    "psc": v["psc"].most_common(1)[0][0] if v["psc"] else "",
                    "tier": v["tiers"].most_common(1)[0][0] if v["tiers"] else "none",
                    "oblig": round(v["oblig"])})
    return out


def build_ddg():
    rows = list(csv.DictReader(open(DDG_EX / "ddg_myp_recompete_provenance.csv")))
    out = []
    for r in rows:
        first = (r.get("original_date_signed") or r.get("pop_start") or "")[:10]
        if not first:
            continue
        out.append({"segment": "ddg_myp", "piid": r["piid"], "first": first,
                    "builder": bkey(r.get("yard", "")), "builder_raw": r.get("yard", ""),
                    "naics": r.get("naics", ""), "psc": r.get("psc", ""),
                    "tier": r.get("block", ""), "oblig": r.get("obligated_total_to_date_$m"),
                    # production MYP: the recompete back-stop is the block completion,
                    # set at award -> the "clock" known from award day.
                    "clock_final": (r.get("ultimate_completion") or r.get("pop_potential_end")
                                    or r.get("pop_current_end") or "")[:10] or None})
    return out


def build_widened():
    """Large-n, LOWER-FIDELITY segment from the 16k widened navy corpus. No parent-IDV
    link and no FPDS mod history, so the 'clock' is the contract PoP end_date (a base-
    award element, like last_date_to_order) and the requirement family is keyed by
    recipient + NAICS-4. Coarser than the maritime/DDG segments — a breadth check, not
    a precise instrument."""
    rows = list(csv.DictReader(open(EX / "navy_widened_discovered.csv")))
    out = []
    for r in rows:
        first = (r.get("start_date") or "")[:10]
        amt = float(r.get("award_amount") or 0)
        if not first or amt < MIN_OBLIG:
            continue
        naics4 = (r.get("naics") or "")[:4]
        out.append({"segment": "navy_widened", "piid": r.get("award_id") or r["generated_internal_id"],
                    "first": first, "builder": f"{bkey(r.get('recipient_name',''))}|{naics4}",
                    "builder_raw": r.get("recipient_name", ""), "naics": r.get("naics", ""),
                    "psc": r.get("psc", ""), "tier": r.get("award_type_group", ""),
                    "description": r.get("description", ""),
                    "oblig": round(amt), "clock_final": (r.get("end_date") or "")[:10] or None})
    return out


def successor_map(vehicles):
    by_builder = defaultdict(list)
    for v in vehicles:
        by_builder[(v["segment"], v["builder"])].append(v)
    succ, pairs = {}, []
    for _k, vs in by_builder.items():
        vs.sort(key=lambda x: x["first"])
        for a, s in zip(vs, vs[1:]):
            gap = months(d10(s["first"]), d10(a["first"]))
            if gap >= MIN_GAP:
                succ[a["piid"]] = s
                pairs.append((a, s, gap))
    return succ, pairs


# ── clock accessor (segment-aware, point-in-time) ────────────────────────────
def clock_as_of(v, freeze, cache):
    """The ordering-period end / block-completion KNOWN for vehicle v as of freeze."""
    if v["segment"] == "maritime_idiq":
        return ldo_as_of(cache.get(v["piid"], []), freeze)
    # ddg: the block completion is set at award; known once first <= freeze
    return d10(v.get("clock_final")) if d10(v["first"]) and d10(v["first"]) <= freeze else None


def clock_final_of(v, cache):
    if v["segment"] == "maritime_idiq":
        return final_ldo(cache.get(v["piid"], []))
    return d10(v.get("clock_final"))


# ── main: build, ensure FPDS timelines, score ────────────────────────────────
def main():
    mar = build_maritime()
    ddg = build_ddg()
    wid = build_widened()
    allv = mar + ddg + wid
    succ, pairs = successor_map(allv)
    by_piid = {v["piid"]: v for v in allv}

    # ensure FPDS timelines for every maritime vehicle (resumable cache)
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    need = [v["piid"] for v in mar if v["piid"] not in cache]
    print(f"maritime vehicles needing FPDS pull: {len(need)} (cached: {len(mar) - len(need)}/{len(mar)})")
    for i, piid in enumerate(need, 1):
        cache[piid] = pull_timeline(piid)
        CACHE.write_text(json.dumps(cache, indent=1))
        print(f"  [{i}/{len(need)}] {piid} -> {len(cache[piid])} actions")
        time.sleep(0.2)

    data_end = max(d10(v["first"]) for v in allv)   # latest award we can observe

    # ── EVENT-LEVEL recall (parallels v1, both segments): for each known recompete,
    #    was the predecessor's then-known clock within horizon at t-6/12/18/24? ──
    ev_rows = []
    for pred, s, gap in pairs:
        d_s = d10(s["first"])
        cf = clock_final_of(pred, cache)
        row = {"segment": pred["segment"], "builder": pred["builder"],
               "predecessor": pred["piid"], "successor": s["piid"],
               "succ_award": s["first"], "pred_clock_final": cf.isoformat() if cf else "",
               "gap_pred_clock_vs_succ_mo": months(cf, d_s) if cf else ""}
        for n in (6, 12, 18, 24):
            f = minus_months(d_s, n)
            ck = clock_as_of(pred, f, cache)
            flagged = bool(ck and -HORIZON <= months(ck, f) <= HORIZON)  # within horizon (or recently closed)
            row[f"flag_t{n}"] = "Y" if flagged else "N"
        # earliest radar flag = max(pred award, pred_clock - HORIZON); lead over successor
        if cf:
            radar = max(d10(pred["first"]), minus_months(cf, HORIZON))
            row["lead_months"] = months(d_s, radar)
        else:
            row["lead_months"] = ""
        ev_rows.append(row)

    # ── POOLED confusion matrix over monthly freezes (the precision/FP control) ──
    # in-scope at f: awarded (first<=f) and ordering period not closed >12mo before f.
    confusion = Counter()
    per_seg = defaultdict(Counter)
    f = date(2013, 1, 1)
    while f <= data_end:
        for v in allv:
            fv = d10(v["first"])
            if not fv or fv > f:
                continue
            ck = clock_as_of(v, f, cache)
            # scope: still orderable, or closed within the last 12mo (radar still watches)
            if ck is not None and months(f, ck) > 12:
                continue
            flag = bool(ck and -HORIZON <= months(ck, f) <= HORIZON)
            s = succ.get(v["piid"])
            truth = bool(s and 0 <= months(d10(s["first"]), f) <= HORIZON)
            # right-censoring: if we cannot observe the full horizon and saw no event, skip
            evaluable = truth or (minus_months(f, -HORIZON) <= data_end)
            if not evaluable:
                continue
            cell = "TP" if (flag and truth) else "FP" if (flag and not truth) \
                else "FN" if (not flag and truth) else "TN"
            confusion[cell] += 1
            per_seg[v["segment"]][cell] += 1
        f = minus_months(f, -1)   # +1 month

    def prf(c):
        tp, fp, fn = c["TP"], c["FP"], c["FN"]
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        return prec, rec, f1

    # ── write outputs ──
    ev_cols = ["segment", "builder", "predecessor", "successor", "succ_award",
               "pred_clock_final", "gap_pred_clock_vs_succ_mo",
               "flag_t6", "flag_t12", "flag_t18", "flag_t24", "lead_months"]
    with open(EX / "backtest_v2_events.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=ev_cols)
        w.writeheader()
        w.writerows(sorted(ev_rows, key=lambda r: r["succ_award"]))
    with open(EX / "backtest_v2_confusion.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["scope", "TP", "FP", "FN", "TN", "precision", "recall", "f1"])
        for name, c in [("ALL", confusion)] + sorted(per_seg.items()):
            p, r, f1 = prf(c)
            w.writerow([name, c["TP"], c["FP"], c["FN"], c["TN"],
                        f"{p:.3f}", f"{r:.3f}", f"{f1:.3f}"])

    # ── report ──
    n = len(ev_rows)
    leads = sorted(r["lead_months"] for r in ev_rows if isinstance(r["lead_months"], (int, float)))
    med = leads[len(leads) // 2] if leads else None
    nseg = len({r["segment"] for r in ev_rows})
    # methodology's signature claim: the successor is awarded BEFORE the predecessor's
    # ordering-period end (gap_pred_clock_vs_succ_mo > 0 -> clock is later than the award).
    gaps_ov = [r["gap_pred_clock_vs_succ_mo"] for r in ev_rows
               if isinstance(r["gap_pred_clock_vs_succ_mo"], (int, float))]
    overlap = sum(1 for g in gaps_ov if g > 0)
    print(f"\n=== WIDENED BACKTEST — {n} ground-truth recompete events, {nseg} segments ===")
    print(f"  signature claim 'successor precedes incumbent ordering-period end': "
          f"{overlap}/{len(gaps_ov)} ({100*overlap//max(len(gaps_ov),1)}%); "
          f"median months early: {sorted(gaps_ov)[len(gaps_ov)//2] if gaps_ov else None}")
    print(f"  span of successor awards: {min(r['succ_award'] for r in ev_rows)} .. {max(r['succ_award'] for r in ev_rows)}")
    for n_ in (6, 12, 18, 24):
        hit = sum(1 for r in ev_rows if r[f"flag_t{n_}"] == "Y")
        print(f"  EVENT recall — anticipable at t-{n_:>2}mo: {hit}/{n} ({100*hit//max(n,1)}%)")
    print(f"  median radar lead over successor award: {med} months")
    print("\n  POOLED PRECISION/RECALL over monthly freezes (the FP control v1 lacked):")
    print(f"    {'scope':<14}{'TP':>4}{'FP':>5}{'FN':>5}{'TN':>6}{'prec':>8}{'rec':>7}{'F1':>7}")
    for name, c in [("ALL", confusion)] + sorted(per_seg.items()):
        p, r, f1 = prf(c)
        print(f"    {name:<14}{c['TP']:>4}{c['FP']:>5}{c['FN']:>5}{c['TN']:>6}{p:>8.2f}{r:>7.2f}{f1:>7.2f}")

    summary = {"events": n, "event_recall": {str(k): sum(1 for r in ev_rows if r[f"flag_t{k}"] == "Y")
                                             for k in (6, 12, 18, 24)},
               "median_lead_months": med,
               "confusion": dict(confusion),
               "precision_recall_f1": dict(zip(("precision", "recall", "f1"), prf(confusion)))}
    (EX / "backtest_v2_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\nwrote backtest_v2_events.csv, backtest_v2_confusion.csv, backtest_v2_summary.json")


if __name__ == "__main__":
    main()
