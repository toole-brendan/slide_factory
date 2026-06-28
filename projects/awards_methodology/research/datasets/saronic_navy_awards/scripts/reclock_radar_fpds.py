#!/usr/bin/env python3
"""Re-clock the recompete radar off the AUTHORITATIVE FPDS ordering-period field.

The Stage-2 (USAspending) radar clocks each vehicle off the MAX child-order
completion date, which a long-delivery tail order pushes years past the true
recompete trigger. FPDS carries the right field per action:
  * IDV  -> lastDateToOrder        (the date orders can no longer be placed)
  * award/standalone -> ultimateCompletionDate (PoP potential end)
We take the latest (current) value per vehicle. The feasibility pilot showed the
old clock ran a mean +3.2yr late on a 6-IDIQ sample, so this corrects the urgency.

Writes:
  extracted/recompete_radar_orderPoP.csv   (backup of the Stage-2 version)
  extracted/recompete_radar.csv            (re-clocked, + clock_basis / prev_clock)
  extracted/_fpds_clocks.json              (raw pulled clocks, resumable cache)
Run: python3 reclock_radar_fpds.py
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import time
from datetime import date
from pathlib import Path
from urllib import parse
from urllib.request import Request, urlopen
from xml.etree.ElementTree import fromstring

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "extracted"
RADAR = EXTRACT / "recompete_radar.csv"
BACKUP = EXTRACT / "recompete_radar_orderPoP.csv"
CACHE = EXTRACT / "_fpds_clocks.json"

NS = {"a": "http://www.w3.org/2005/Atom", "ns1": "https://www.fpds.gov/FPDS"}
BASE = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
HDRS = {"User-Agent": "saronic-usv-backtest/1.0 (recompete radar reclock)"}
AS_OF = date(2026, 6, 23)


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


def fpds_clock(piid):
    """(clock_iso, basis) for a PIID: max lastDateToOrder if it is an IDV, else
    max ultimateCompletionDate (award). (None, 'fpds-none') if FPDS returns nothing."""
    ldo, ult = [], []
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
            if content is None:
                continue
            idv = content.find(".//ns1:IDV", NS)
            if idv is not None:
                v = _f(idv, ".//ns1:lastDateToOrder")
                if v:
                    ldo.append(v[:10])
                continue
            award = content.find(".//ns1:award", NS)
            if award is not None:
                v = _f(award, ".//ns1:ultimateCompletionDate")
                if v:
                    ult.append(v[:10])
        start += 10
        time.sleep(0.3)
    if ldo:
        return max(ldo), "lastDateToOrder"
    if ult:
        return max(ult), "ultimateCompletionDate"
    return None, "fpds-none"


def state_for(months):
    if months < 0:
        return "OVERDUE (ordering period closed, no successor seen)"
    if months <= 12:
        return "imminent (<12mo)"
    if months <= 24:
        return "upcoming (12-24mo)"
    return "horizon (24-36mo)"


def main():
    rows = list(csv.DictReader(open(RADAR)))
    if not BACKUP.exists():
        shutil.copy(RADAR, BACKUP)
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}

    print(f"re-clocking {len(rows)} radar vehicles off FPDS …")
    for i, r in enumerate(rows, 1):
        piid = r["vehicle_piid"]
        if piid not in cache:
            clk, basis = fpds_clock(piid)
            cache[piid] = {"clock": clk, "basis": basis}
            CACHE.write_text(json.dumps(cache, indent=1))   # resumable
            time.sleep(0.2)
        c = cache[piid]
        print(f"  [{i:2}/{len(rows)}] {piid:<16} {c['basis']:<22} "
              f"FPDS={c['clock']}  (was {r['recompete_clock']})")

    out = []
    n_corrected = n_overdue = 0
    for r in rows:
        piid = r["vehicle_piid"]
        c = cache[piid]
        prev = r["recompete_clock"]
        if c["clock"]:
            y, m, d = (int(x) for x in c["clock"].split("-"))
            months = round((date(y, m, d) - AS_OF).days / 30.4, 1)
            clock, basis = c["clock"], c["basis"]
            if c["clock"] != prev:
                n_corrected += 1
        else:
            clock, basis = prev, "order-PoP (FPDS none)"
            months = float(r["months_to_clock"])
        if months < 0:
            n_overdue += 1
        nr = dict(r)
        nr["recompete_clock"] = clock
        nr["months_to_clock"] = months
        nr["state"] = state_for(months)
        nr["clock_basis"] = basis
        nr["prev_clock"] = prev
        out.append(nr)

    out.sort(key=lambda r: r["months_to_clock"])
    cols = ["vehicle_piid", "tier", "vehicle_type", "incumbent", "naics", "psc",
            "obligated_$m", "n_orders", "recompete_clock", "months_to_clock", "state",
            "access_gate", "portal_notice", "last_activity", "clock_basis", "prev_clock"]
    with open(RADAR, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    print(f"\ndone. {n_corrected}/{len(rows)} vehicles re-clocked to an earlier FPDS date; "
          f"{n_overdue} are now OVERDUE (ordering period closed).")
    print(f"wrote {RADAR.name} (+ backup {BACKUP.name})")


if __name__ == "__main__":
    main()
