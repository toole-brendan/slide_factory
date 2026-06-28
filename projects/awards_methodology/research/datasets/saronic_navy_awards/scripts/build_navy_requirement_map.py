#!/usr/bin/env python3
"""v1 NAVY REQUIREMENT MAP from the widened discovery (navy_widened_discovered.csv).

Two cuts, both applying the subaward-concentration methodology
(Subaward_Vendor_Concentration_HHI_and_Activity_Methodology.md), lifted to the PRIME
grain:

  CUT 1 — capability-cell concentration ("where to play"): per PSC and per NAICS, the
          prime-market concentration (Top-1 share, HHI, effective firms) computed over
          POSITIVE spend only, at ULTIMATE-PARENT grain, with the reference's
          High/Moderate/Lower contestability label + the top holder.
  CUT 2 — recurring requirement-family proxies: parent-incumbent x PSC clusters with
          scale, breadth (distinct awards), duration (span), latest end date, instrument
          mix — the "is this a recurring requirement and who holds it" view.

v1 caveats (honest): families are header-grain proxies (no awarding office / place of
performance / last date to order yet — those need the detail + SAM.gov enrichment pass);
$ are nominal (not yet constant-FY2026$); parent rollup is a name heuristic, not the
detail-grade ultimate-parent crosswalk. Ranks the big recurring fields; precise governing
dates and true requirement families come in v2.

Run: python3 build_navy_requirement_map.py
"""
from __future__ import annotations

import ast
import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "extracted"
SRC = EX / "navy_widened_discovered.csv"

# --- ultimate-parent rollup (heuristic; the big defense primes likely to appear) ---
PARENTS = {
    "ELECTRIC BOAT": "General Dynamics", "BATH IRON WORKS": "General Dynamics",
    "GENERAL DYNAMICS": "General Dynamics", "NASSCO": "General Dynamics",
    "NATIONAL STEEL AND SHIPBUILDING": "General Dynamics",
    "HUNTINGTON INGALLS": "Huntington Ingalls", "INGALLS": "Huntington Ingalls",
    "NEWPORT NEWS": "Huntington Ingalls",
    "NORTHROP GRUMMAN": "Northrop Grumman",
    "LOCKHEED MARTIN": "Lockheed Martin", "SIKORSKY": "Lockheed Martin",
    "RAYTHEON": "RTX", "RTX": "RTX", "COLLINS AEROSPACE": "RTX",
    "BOEING": "Boeing", "L3HARRIS": "L3Harris", "L-3": "L3Harris", "HARRIS CORP": "L3Harris",
    "LEIDOS": "Leidos", "DYNETICS": "Leidos", "BAE": "BAE Systems",
    "GENERAL ATOMICS": "General Atomics", "TEXTRON": "Textron", "SAIC": "SAIC",
    "BOOZ ALLEN": "Booz Allen", "PERATON": "Peraton", "AUSTAL": "Austal",
    "FINCANTIERI": "Fincantieri", "MARINETTE": "Fincantieri", "BOLLINGER": "Bollinger",
    "KONGSBERG": "Kongsberg", "THALES": "Thales", "ELBIT": "Elbit",
    "ANDURIL": "Anduril", "PALANTIR": "Palantir", "PERATON": "Peraton",
}
_SUFFIX = re.compile(r"\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|"
                     r"LP|LLP|PLC|TECHNOLOGIES|TECHNOLOGY|SYSTEMS|GROUP|HOLDINGS|USA|US)\b")


def parent(name: str) -> str:
    u = (name or "").upper()
    for k, v in PARENTS.items():
        if k in u:
            return v
    u = _SUFFIX.sub("", u)
    u = re.sub(r"[^A-Z0-9 ]", " ", u)
    return " ".join(u.split()).title() or "(unknown)"


def code_of(cell: str) -> str:
    """Extract the code from a USAspending NAICS/PSC dict-cell."""
    if not cell:
        return ""
    try:
        d = ast.literal_eval(cell)
        if isinstance(d, dict):
            return str(d.get("code") or "")
    except (ValueError, SyntaxError):
        pass
    m = re.search(r"'code':\s*'([^']+)'", cell)
    return m.group(1) if m else cell.strip()


def desc_of(cell: str) -> str:
    try:
        d = ast.literal_eval(cell)
        if isinstance(d, dict):
            return str(d.get("description") or "")
    except (ValueError, SyntaxError):
        pass
    return ""


def yr(s):
    s = (s or "")[:4]
    return int(s) if s.isdigit() else None


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def concentration(rows):
    """Positive-spend, parent-grain HHI / Top-1 / eff-firms + contestability label."""
    net = sum(f(r["award_amount"]) for r in rows)
    pos_by_parent = defaultdict(float)
    for r in rows:
        amt = f(r["award_amount"])
        if amt > 0:
            pos_by_parent[r["_parent"]] += amt
    tot_pos = sum(pos_by_parent.values())
    if tot_pos <= 0:
        return dict(net=net, n=len(rows), primes=len(pos_by_parent), top1=0, hhi=0,
                    eff=0, holder="(n/a)", label="Check")
    shares = {p: v / tot_pos for p, v in pos_by_parent.items()}
    hhi = sum(s * s for s in shares.values())
    holder = max(pos_by_parent, key=pos_by_parent.get)
    top1 = shares[holder]
    eff = 1 / hhi if hhi else 0
    label = ("High" if (top1 >= 0.60 or hhi >= 0.40)
             else "Moderate" if eff <= 3 else "Lower")
    return dict(net=net, n=len(rows), primes=len(pos_by_parent), top1=top1, hhi=hhi,
                eff=eff, holder=holder, label=label)


def main():
    rows = list(csv.DictReader(open(SRC)))
    for r in rows:
        r["_parent"] = parent(r["recipient_name"])
        r["_psc"] = code_of(r["psc"])
        r["_naics"] = code_of(r["naics"])
        r["_pscd"] = desc_of(r["psc"])
        r["_naicsd"] = desc_of(r["naics"])
        r["_y0"], r["_y1"] = yr(r["start_date"]), yr(r["end_date"])
    print(f"universe: {len(rows)} Navy (non-USMC, non-Saronic) awards, "
          f"${sum(f(r['award_amount']) for r in rows)/1e9:.1f}B; "
          f"{len(set(r['_parent'] for r in rows))} distinct prime parents")

    # ---- CUT 1: capability-cell concentration ----
    def cell_table(keyf, descf, label_desc):
        cells = defaultdict(list)
        for r in rows:
            k = keyf(r)
            if k:
                cells[k].append(r)
        out = []
        for k, rs in cells.items():
            c = concentration(rs)
            yrs = sorted({r["_y0"] for r in rs if r["_y0"]})
            c.update(cell=k, desc=(descf(rs) or "")[:34],
                     span=(max(yrs) - min(yrs)) if len(yrs) > 1 else 0, n_years=len(yrs))
            out.append(c)
        out.sort(key=lambda x: -x["net"])
        print(f"\n=== CUT 1 — {label_desc} (top 15 by $) ===")
        print(f"{'code':6s} {'$M':>8s} {'awards':>6s} {'primes':>6s} {'top1':>5s} "
              f"{'HHI':>5s} {'eff':>5s} {'contest':>9s}  holder / desc")
        for c in out[:15]:
            print(f"{c['cell']:6s} {c['net']/1e6:>8,.0f} {c['n']:>6d} {c['primes']:>6d} "
                  f"{c['top1']*100:>4.0f}% {c['hhi']:>5.2f} {c['eff']:>5.1f} "
                  f"{c['label']:>9s}  {c['holder'][:20]:20s} {c['desc']}")
        return out

    psc_t = cell_table(lambda r: r["_psc"], lambda rs: rs[0]["_pscd"], "PSC capability cells")
    naics_t = cell_table(lambda r: r["_naics"], lambda rs: rs[0]["_naicsd"], "NAICS capability cells")

    # ---- CUT 2: recurring requirement-family proxies (parent x PSC) ----
    fam = defaultdict(list)
    for r in rows:
        if r["_psc"]:
            fam[(r["_parent"], r["_psc"])].append(r)
    fr = []
    for (par, psc), rs in fam.items():
        yrs = sorted({r["_y0"] for r in rs if r["_y0"]})
        ends = [r["_y1"] for r in rs if r["_y1"]]
        idv = sum(1 for r in rs if r["award_type_group"] == "idv")
        fr.append(dict(parent=par, psc=psc, desc=(rs[0]["_pscd"] or "")[:30],
                       net=sum(f(r["award_amount"]) for r in rs), breadth=len(rs),
                       n_years=len(yrs), span=(max(yrs) - min(yrs)) if len(yrs) > 1 else 0,
                       latest_end=max(ends) if ends else None, idv=idv))
    fr.sort(key=lambda x: -x["net"])
    print("\n=== CUT 2 — recurring requirement-family proxies (parent x PSC; top 20 by $) ===")
    print(f"{'$M':>8s} {'awd':>4s} {'yrs':>4s} {'span':>4s} {'end':>5s} {'idv':>4s}  parent / PSC")
    for x in fr[:20]:
        print(f"{x['net']/1e6:>8,.0f} {x['breadth']:>4d} {x['n_years']:>4d} {x['span']:>4d} "
              f"{str(x['latest_end'] or '-'):>5s} {x['idv']:>4d}  {x['parent'][:22]:22s} "
              f"{x['psc']} {x['desc']}")

    # ---- write outputs ----
    def dump(path, rowsout, cols):
        with open(path, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader(); w.writerows(rowsout)
    dump(EX / "navy_widened_psc_concentration.csv", psc_t,
         ["cell", "desc", "net", "n", "primes", "top1", "hhi", "eff", "label", "span", "n_years"])
    dump(EX / "navy_widened_naics_concentration.csv", naics_t,
         ["cell", "desc", "net", "n", "primes", "top1", "hhi", "eff", "label", "span", "n_years"])
    dump(EX / "navy_widened_requirement_families.csv", fr,
         ["parent", "psc", "desc", "net", "breadth", "n_years", "span", "latest_end", "idv"])
    print(f"\nwrote navy_widened_psc_concentration.csv ({len(psc_t)}), "
          f"navy_widened_naics_concentration.csv ({len(naics_t)}), "
          f"navy_widened_requirement_families.csv ({len(fr)})")


if __name__ == "__main__":
    main()
