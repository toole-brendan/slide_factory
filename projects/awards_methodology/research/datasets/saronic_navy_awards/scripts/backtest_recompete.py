#!/usr/bin/env python3
"""HISTORICAL-REPLAY BACKTEST (Phase 2) for the recompete mechanism.

Ground truth: the small-boat IDIQ series (NAICS 336612) shows clear builder-level
recompete chains - each builder's boat-line vehicle gets re-bought every few years.
For each predecessor->successor pair we ask, POINT-IN-TIME (no look-ahead):

  at freeze f = successor_award - {6,12,18} months, using ONLY FPDS actions signed
  <= f, was the predecessor's ordering-period end (lastDateToOrder, as known then)
  scheduled to close within the radar's 36-month horizon?  If yes, the radar would
  have flagged the impending recompete at f.

Reports per-event anticipation, the lead time over the successor award, whether the
predecessor's clock was later EXTENDED (the honest false-positive-risk case), and an
aggregate hit rate. Baseline: the portal (these solicitations are absent from the
669 notices, so portal lead ~ 0).

Inputs : extracted/_detail_index.json, extracted/market_tiers.csv, FPDS (live)
Outputs: extracted/backtest_results.csv, extracted/_fpds_timelines.json (cache)
Run    : python3 backtest_recompete.py
"""
from __future__ import annotations

import csv
import json
import re
import time
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib import parse
from urllib.request import Request, urlopen
from xml.etree.ElementTree import fromstring

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "extracted"
CACHE = EXTRACT / "_fpds_timelines.json"
OUT = EXTRACT / "backtest_results.csv"

NS = {"a": "http://www.w3.org/2005/Atom", "ns1": "https://www.fpds.gov/FPDS"}
BASE = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
HDRS = {"User-Agent": "saronic-usv-backtest/1.0"}
HORIZON = 36          # radar forward horizon (months)
MIN_GAP = 18          # min months between predecessor and successor to count as a recompete


def _f(elem, path):
    x = elem.find(path, NS)
    return x.text if x is not None and x.text else None


def months(a: date, b: date) -> float:
    return round((a - b).days / 30.4, 1)


def d10(s):
    s = (s or "")[:10]
    try:
        return date.fromisoformat(s)
    except Exception:
        return None


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
    """[(signed_iso, lastDateToOrder_iso)] per IDV action, plus base signed date."""
    acts = []
    start = 0
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
    """The lastDateToOrder KNOWN as of `freeze`: the value on the latest action
    signed on or before freeze. None if no action with an LDO by then."""
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


def main():
    idx = json.loads((EXTRACT / "_detail_index.json").read_text())
    tier = {r["generated_internal_id"]: r["tier"]
            for r in csv.DictReader(open(EXTRACT / "market_tiers.csv"))}

    # Reconstruct small-boat IDIQ vehicles (NAICS 336612, >=$5M) + their builder.
    veh = defaultdict(lambda: {"oblig": 0.0, "recip": defaultdict(float),
                               "naics": set(), "psc": set(), "first": None})
    for e in idx:
        pidv = e.get("parent_idv_piid")
        if not pidv or tier.get(e.get("generated_internal_id")) != "small_craft":
            continue
        v = veh[pidv]
        ob = e.get("total_obligation") or 0
        v["oblig"] += ob
        if e.get("recipient_name"):
            v["recip"][e["recipient_name"]] += ob
        v["naics"].add(e.get("naics_code") or "")
        v["psc"].add(e.get("psc_code") or "")
        ds = (e.get("date_signed") or "")[:10]
        if ds:
            v["first"] = min(v["first"], ds) if v["first"] else ds

    vehicles = []
    for p, v in veh.items():
        if "336612" not in v["naics"] or v["oblig"] < 5e6:
            continue
        builder = max(v["recip"], key=v["recip"].get)
        vehicles.append({"piid": p, "first": v["first"], "builder": builder,
                         "oblig": v["oblig"]})

    # Pull per-action timelines (resumable cache).
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    print(f"pulling FPDS timelines for {len(vehicles)} small-boat IDIQs …")
    for i, vv in enumerate(vehicles, 1):
        if vv["piid"] not in cache:
            cache[vv["piid"]] = pull_timeline(vv["piid"])
            CACHE.write_text(json.dumps(cache, indent=1))
            time.sleep(0.2)
        print(f"  [{i:2}/{len(vehicles)}] {vv['piid']:<16} {len(cache[vv['piid']])} actions")

    # Form recompete pairs: same builder, consecutive by date, gap >= MIN_GAP months.
    def bkey(name):
        return re.sub(r"[^A-Z]", "", name.upper())[:10]
    by_builder = defaultdict(list)
    for vv in vehicles:
        if vv["first"]:
            by_builder[bkey(vv["builder"])].append(vv)
    pairs = []
    for b, vs in by_builder.items():
        vs.sort(key=lambda x: x["first"])
        for a, s in zip(vs, vs[1:]):
            gap = months(d10(s["first"]), d10(a["first"]))
            if gap >= MIN_GAP:
                pairs.append((a, s, gap))

    # Point-in-time test per pair.
    results = []
    for pred, succ, gap in pairs:
        d_s = d10(succ["first"])             # successor award (first-order proxy)
        acts = cache[pred["piid"]]
        fin = final_ldo(acts)
        flags = {}
        for n in (6, 12, 18):
            f = date(d_s.year - (n // 12), d_s.month - (n % 12) if d_s.month - (n % 12) > 0
                     else d_s.month - (n % 12) + 12, min(d_s.day, 28))
            if d_s.month - (n % 12) <= 0 and n % 12:
                f = date(f.year - 1, f.month, f.day)
            ldo_known = ldo_as_of(acts, f)
            # radar flags pred if its then-known ordering-period end is within [f, f+36mo]
            flagged = bool(ldo_known and 0 <= months(ldo_known, f) <= HORIZON
                           or (ldo_known and months(ldo_known, f) < 0))  # already closed = also a signal
            flags[n] = (flagged, ldo_known.isoformat() if ldo_known else None)
        # lead time: earliest the radar could flag = max(pred award, pred_close - 36mo)
        lead = None
        if fin:
            radar_flag = max(d10(pred["first"]), date(fin.year - 3, fin.month, min(fin.day, 28)))
            lead = months(d_s, radar_flag)
        # was the clock extended after the t-12 freeze?
        f12 = flags[12][1]
        extended = bool(fin and f12 and d10(f12) and fin > d10(f12))
        # Is this a real recompete or a parallel-vehicle pair? gap = months from the
        # predecessor's ordering-period close to the successor award. >12mo positive ->
        # the predecessor was still ACTIVE well past the successor (a parallel vehicle the
        # builder held alongside, NOT a recompete the radar should have to flag).
        gap = months(fin, d_s) if fin else None
        if gap is None:
            ev_class = "unknown"
        elif gap > 12:
            ev_class = "parallel"          # predecessor still active -> not a recompete
        elif gap < -18:
            ev_class = "lapsed-rebuy"      # requirement lapsed, then re-bought
        else:
            ev_class = "recompete"         # clean back-to-back turnover
        results.append({
            "builder": bkey(pred["builder"]), "predecessor": pred["piid"],
            "successor": succ["piid"], "succ_award": succ["first"],
            "pred_final_close": fin.isoformat() if fin else "",
            "pred_close_vs_succ_mo": gap if gap is not None else "",
            "event_class": ev_class,
            "anticipable_t6": "Y" if flags[6][0] else "N",
            "anticipable_t12": "Y" if flags[12][0] else "N",
            "anticipable_t18": "Y" if flags[18][0] else "N",
            "ldo_known_at_t12": flags[12][1] or "",
            "lead_months": lead if lead is not None else "",
            "clock_extended_after_t12": "Y" if extended else "N",
        })

    results.sort(key=lambda r: r["succ_award"])
    cols = list(results[0].keys())
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader(); w.writerows(results)

    # Point-in-time clock-history (the no-look-ahead evidence): for each vehicle in the
    # events, the sequence of DISTINCT lastDateToOrder values with the date each was first
    # recorded -> shows the clock was known years ahead, and where it was later extended.
    roles = {}
    for pred, succ, _g in pairs:
        roles[pred["piid"]] = "predecessor"
        roles.setdefault(succ["piid"], "successor")
    tl = []
    for piid, role in roles.items():
        seen = None
        for sgn, ldo, mod in sorted(cache.get(piid, []), key=lambda a: a[0]):
            if ldo and ldo != seen:
                tl.append({"vehicle_piid": piid, "role": role, "clock_set": sgn,
                           "mod": mod, "last_date_to_order": ldo,
                           "event": "base clock" if seen is None else "EXTENDED / changed"})
                seen = ldo
    tl.sort(key=lambda r: (r["vehicle_piid"], r["clock_set"]))
    with open(EXTRACT / "backtest_pop_timeline.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["vehicle_piid", "role", "clock_set", "mod",
                                           "last_date_to_order", "event"])
        w.writeheader(); w.writerows(tl)

    n = len(results)
    hit12 = sum(1 for r in results if r["anticipable_t12"] == "Y")
    hit18 = sum(1 for r in results if r["anticipable_t18"] == "Y")
    ext = sum(1 for r in results if r["clock_extended_after_t12"] == "Y")
    leads = sorted(r["lead_months"] for r in results if isinstance(r["lead_months"], (int, float)))
    med = leads[len(leads) // 2] if leads else None
    print(f"\n=== BACKTEST: {n} recompete events (small-boat IDIQ chains) ===")
    print(f"  anticipable at t-12mo: {hit12}/{n} ({100*hit12//max(n,1)}%)")
    print(f"  anticipable at t-18mo: {hit18}/{n} ({100*hit18//max(n,1)}%)")
    print(f"  median radar lead time over the successor award: {med} months")
    print(f"  predecessor clock EXTENDED after t-12 (date-slip risk): {ext}/{n}")
    print(f"  portal baseline: these solicitations absent from the 669 notices -> ~0 lead")
    print(f"\n  {'builder':<11}{'predecessor':<15}{'successor':<15}{'succ_award':<12}"
          f"{'t12':<4}{'lead_mo':<8}{'extended'}")
    for r in results:
        print(f"  {r['builder']:<11}{r['predecessor']:<15}{r['successor']:<15}"
              f"{r['succ_award']:<12}{r['anticipable_t12']:<4}{str(r['lead_months']):<8}"
              f"{r['clock_extended_after_t12']}")
    print(f"\nwrote {OUT.name}")


if __name__ == "__main__":
    main()
