#!/usr/bin/env python3
"""Forward-signal layer from the SAM.gov Data Services ARCHIVED Contract Opportunities bulk
extracts — the historical pre-award notices the public Opportunities API blocks (status=archived
500s). Drop any number of `FY####_archived_opportunities.csv` files into the (gitignored, in-repo)
raw/sam/opportunities_archive/ dir; this auto-discovers them, so coverage grows as you add years
(FY2017..FY2026 ⇒ the full recompete-event span 2013-2024 becomes in-window).

What it produces:
  - award<->notice matching by normalized Sol# (vs the prior 2/2048),
  - pre-solicitation LEAD (sources-sought / solicitation posted date -> award date),
  - PORTAL INCOMPLETENESS (share of awards with NO synopsized notice = FAR 16.5 / OT "dark" buying),
  - recompete-SUCCESSOR forward-signal: for each Arm-A recompete, did a notice precede the
    successor award, and by how long — matched via the successor's REAL solicitation #s (maritime IDV
    orders + DDG provenance solicitation_id), classified matched / dark / unresolved / out-of-window,
  - ACTIVE-NOTICE BASELINE: of Navy-maritime pre-award notices, how many convert to an Award Notice
    under the same Sol# and on what lead (extracted/forward_signal_active_notice_baseline.csv),
  - `forward_signal_visibility` per award.

It streams the (gitignored, in-repo) multi-GB sources once and CACHES the targeted index + baseline
(extracted/_notice_sol_index.json), keyed exactly on schema_version + file signature + the targeted-Sol#
set + the DDG-provenance signature, so re-runs are instant until any of those change.

Run: python3 forward_signal.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import phase1_common as p1

csv.field_size_limit(sys.maxsize)
EX = p1.EX
ARCH = EX.parent / "raw" / "sam" / "opportunities_archive"
CACHE = EX / "_notice_sol_index.json"
PRE_AWARD = {"Sources Sought", "Presolicitation", "Solicitation", "Combined Synopsis/Solicitation"}
EARLY = {"Sources Sought", "Presolicitation"}
AWARD_TYPE = "Award Notice"
# Active-notice baseline population: Navy maritime notices (mirrors the award-side taxonomy).
NAVY_SUBTIER = "DEPT OF THE NAVY"
MARITIME_NAICS = {"336611", "336612"}            # ship building / boat building
MARITIME_PSC = {"1905", "1925", "1940"}          # combat ships / special service vessels / small craft
# DDG successors are contracts (not IDVs), so their real solicitation # lives in the provenance CSV,
# not in _detail_index.json. Path mirrors backtest_v2_precision_recall.DDG_EX.
DDG_PROV = EX.parent.parent / "ddg51_recompete_cadence" / "extracted" / "ddg_myp_recompete_provenance.csv"
SCHEMA_VERSION = 2                                # bump to invalidate caches when streaming logic changes
d10, months = p1.d10, p1.months


def norm(s):
    return re.sub(r"[^A-Z0-9]", "", (s or "").upper())


def archives():
    """All FY####_archived_opportunities.csv under raw/sam/opportunities_archive/ (gitignored,
    in-repo). Sorted for deterministic streaming order."""
    return sorted(ARCH.glob("FY*_archived_opportunities.csv"))


def award_indexes():
    """(sol -> [(piid, date_signed)]) for award records, and (parent_idv_piid -> set(order sol#))
    so a recompete successor IDV can be matched via its orders' solicitation numbers."""
    idx = json.loads((EX / "_detail_index.json").read_text())
    by_sol = defaultdict(list)
    idv_sols = defaultdict(set)
    for e in idx:
        s = norm(e.get("solicitation_identifier"))
        if s:
            by_sol[s].append((e.get("piid"), (e.get("date_signed") or "")[:10]))
            if e.get("parent_idv_piid"):
                idv_sols[e["parent_idv_piid"]].add(s)
    return by_sol, idv_sols


def succ_sol_map(idv_sols):
    """successor vehicle piid -> set(normalized REAL solicitation #s). Maritime IDVs resolve via their
    orders' solicitation_identifiers (idv_sols, keyed by parent_idv_piid == vehicle piid); DDG successors
    are contracts whose solicitation lives only in the DDG provenance CSV (`solicitation_id`). Matching on
    the real Sol# — not the contract PIID — is what makes "dark" trustworthy (the PIID never matches a
    notice, so the old fallback silently marked every DDG recompete dark)."""
    m = {k: set(v) for k, v in idv_sols.items()}
    if DDG_PROV.exists():
        for r in csv.DictReader(open(DDG_PROV)):
            piid, sol = r.get("piid"), norm(r.get("solicitation_id"))
            if piid and sol:
                m.setdefault(piid, set()).add(sol)
    return m


def build_index(want):
    """Stream archives once and return four things, caching them keyed EXACTLY on the inputs:
      - `idx`     : sol -> [(type, posted)] for the targeted `want` sols (dedup by NoticeId),
      - `totals`  : portal-wide notice-type counts,
      - `span`    : posted-date min..max,
      - `baseline`: Navy-maritime sol -> {naics, psc, earliest pre-award (type,posted), earliest
                    Award Notice (date,amount)} for the active-notice baseline.
    Cache validity is exact (schema_version + file signature + want hash + DDG-provenance signature) so a
    changed `want` (e.g. newly added DDG successor sols) can never reuse a stale index. `want` hashing uses
    hashlib (process-stable), not builtin hash()."""
    files = archives()
    sig = [[f.name, f.stat().st_size] for f in files]
    want_hash = hashlib.sha1(",".join(sorted(want)).encode()).hexdigest()
    ddg_sig = [DDG_PROV.name, DDG_PROV.stat().st_size] if DDG_PROV.exists() else None
    if CACHE.exists():
        c = json.loads(CACHE.read_text())
        if (c.get("schema_version") == SCHEMA_VERSION and c.get("signature") == sig
                and c.get("want_hash") == want_hash and c.get("ddg_sig") == ddg_sig):
            print(f"  (cached index: {len(c['index'])} sols, {len(c.get('baseline', {}))} navy-maritime "
                  f"sols, from {len(sig)} files, {c.get('span')})")
            idx = {k: [tuple(x) for x in v] for k, v in c["index"].items()}
            return idx, c.get("totals", {}), c.get("span"), c.get("baseline", {})
    print(f"  streaming {len(files)} archive(s): {', '.join(f.name for f in files)}")
    idx = defaultdict(list); seen = set(); totals = defaultdict(int); mn = mx = None
    baseline = {}
    for f in files:
        with open(f, newline="", encoding="utf-8", errors="replace") as fh:
            for row in csv.DictReader(fh):
                t = row.get("Type") or ""; totals[t] += 1
                pd = (row.get("PostedDate") or "")[:10]
                if pd:
                    mn = pd if mn is None or pd < mn else mn; mx = pd if mx is None or pd > mx else mx
                s = norm(row.get("Sol#"))
                if not s:
                    continue
                if s in want:
                    nid = row.get("NoticeId")
                    if nid not in seen:
                        seen.add(nid)
                        idx[s].append((t, pd))
                # active-notice baseline: the Navy-maritime notice population (independent of `want`)
                if row.get("Sub-Tier") == NAVY_SUBTIER and (
                        (row.get("NaicsCode") or "") in MARITIME_NAICS
                        or (row.get("ClassificationCode") or "") in MARITIME_PSC):
                    rec = baseline.setdefault(s, {"naics": "", "psc": "", "pre": None, "award": None})
                    if not rec["naics"] and row.get("NaicsCode"):
                        rec["naics"] = row.get("NaicsCode")
                    if not rec["psc"] and row.get("ClassificationCode"):
                        rec["psc"] = row.get("ClassificationCode")
                    if t in PRE_AWARD and pd and (rec["pre"] is None or pd < rec["pre"][1]):
                        rec["pre"] = (t, pd)
                    if t == AWARD_TYPE:
                        ad = (row.get("AwardDate") or "")[:10] or pd
                        if ad and (rec["award"] is None or ad < rec["award"][0]):
                            rec["award"] = (ad, row.get("Award$") or "")
    span = f"{mn}..{mx}"
    CACHE.write_text(json.dumps({"schema_version": SCHEMA_VERSION, "signature": sig,
                                 "want_hash": want_hash, "ddg_sig": ddg_sig, "span": span,
                                 "totals": dict(totals), "index": idx, "baseline": baseline}))
    return idx, dict(totals), span, baseline


def earliest_pre(notes, on_or_before, types):
    cands = sorted([(d10(p), t) for t, p in notes if t in types and d10(p) and d10(p) <= on_or_before])
    return cands[0] if cands else None


def main():
    by_sol, idv_sols = award_indexes()
    print(f"award Sol#: {len(by_sol)}; parent IDVs with order Sol#: {len(idv_sols)}")

    # Arm-A recompete events (incumbent v -> successor s); compute early so their REAL solicitation #s
    # can be targeted while streaming (DDG successor sols are not in by_sol).
    fams = p1.build_families("A")
    succ_sols = succ_sol_map(idv_sols)
    events, _seen = [], set()
    for f in fams.values():
        for v in f["vehicles"]:
            s = p1.successor_of(f, v)
            if s and s["piid"] not in _seen:
                _seen.add(s["piid"]); events.append((f, v, s))
    want = set(by_sol)
    for _f, _v, s in events:
        want |= succ_sols.get(s["piid"], set())

    idx, totals, span, baseline = build_index(want)
    matched_sols = sum(1 for s in by_sol if s in idx)
    # "in-window" = award falls within the NOTICE archive's actual coverage (auto-widens with files)
    WINDOW_START = (span or "..").split("..")[0] or "9999"
    print(f"notice archive span: {span}; award<->notice Sol# matches: {matched_sols}; window_start={WINDOW_START}")

    rows = []
    for s, awards in by_sol.items():
        notes = idx.get(s, [])
        for piid, ds in awards:
            dd = d10(ds)
            if not dd:
                continue
            inwin = ds >= WINDOW_START
            fp = earliest_pre(notes, dd, PRE_AWARD)
            fe = earliest_pre(notes, dd, EARLY)
            rows.append({"piid": piid, "date_signed": ds, "in_window": int(inwin), "sol": s,
                         "first_preaward_type": fp[1] if fp else "",
                         "first_preaward_posted": fp[0].isoformat() if fp else "",
                         "preaward_lead_months": months(dd, fp[0]) if fp else "",
                         "early_lead_months": months(dd, fe[0]) if fe else "",
                         "forward_signal_visibility": "matched_data_services" if fp
                         else ("no_notice_in_archive" if inwin else "out_of_window")})
    with open(EX / "forward_signal_match.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

    def med(xs):
        return sorted(xs)[len(xs) // 2] if xs else None

    def pctl(sorted_xs, q):
        return sorted_xs[min(len(sorted_xs) - 1, int(q * len(sorted_xs)))] if sorted_xs else None
    inw = [r for r in rows if r["in_window"]]
    m = sum(1 for r in inw if r["first_preaward_posted"])
    leads = [r["preaward_lead_months"] for r in inw if r["preaward_lead_months"] != ""]
    early = [r["early_lead_months"] for r in inw if r["early_lead_months"] != ""]
    print("\n=== FORWARD-SIGNAL (in-window maritime awards) ===")
    print(f"  in-window awards: {len(inw)}; with a pre-award notice: {m} "
          f"({100*m//max(len(inw),1)}%) => ~{100-100*m//max(len(inw),1)}% dark")
    print(f"  pre-solicitation lead median {med(leads)} mo (n={len(leads)}); "
          f"early-signal lead median {med(early)} mo (n={len(early)})")

    # recompete-SUCCESSOR forward signal (matched via the successor's REAL solicitation #s, not its PIID)
    print(f"\n=== RECOMPETE-SUCCESSOR forward signal ({len(events)} Arm-A events) ===")
    matched = dark = unresolved = oow = 0; rec_leads = []
    for f, v, s in sorted(events, key=lambda e: e[2]["first"]):
        dd = d10(s["first"]); inwin = s["first"] >= WINDOW_START
        sols = succ_sols.get(s["piid"], set())
        notes = [n for so in sols for n in idx.get(so, [])]
        fp = earliest_pre(notes, dd, PRE_AWARD) if (sols and dd) else None
        if fp:
            matched += 1; rec_leads.append(months(dd, fp[0]))
            tag = f"{fp[1]} lead={months(dd, fp[0])}mo  via {'|'.join(sorted(sols))}"
        elif not inwin:
            oow += 1; tag = "(out of archive window)"
        elif not sols:
            unresolved += 1; tag = "— no solicitation # resolved (unresolved)"
        else:
            dark += 1; tag = f"— no notice for {'|'.join(sorted(sols))} (dark)"
        print(f"  {s['piid']:<16} award {s['first']}  {tag}")
    print(f"  matched {matched} / dark {dark} / unresolved {unresolved} / out-of-window {oow} "
          f"(of {len(events)}); median recompete lead {med(rec_leads)} mo (n={len(rec_leads)})")

    # ── ACTIVE-NOTICE BASELINE (portal precision proxy): of Navy-maritime pre-award notices, how many
    #    convert to an Award Notice under the same Sol#, and on what timeline. Archive-internal — an
    #    Award Notice is not ground truth (award-side darkness still applies), so this is a conversion /
    #    precision PROXY, not the portal's true precision.
    base_rows = []
    for sol, rec in baseline.items():
        pre, aw = rec.get("pre"), rec.get("award")
        lead = ""
        if pre and aw:
            d_pre, d_aw = d10(pre[1]), d10(aw[0])
            if d_pre and d_aw and d_aw >= d_pre:
                lead = months(d_aw, d_pre)
        base_rows.append({"sol": sol, "naics": rec.get("naics", ""), "psc": rec.get("psc", ""),
                          "pre_type": pre[0] if pre else "", "pre_posted": pre[1] if pre else "",
                          "award_date": aw[0] if aw else "", "award_amount": aw[1] if aw else "",
                          "notice_to_award_lead_months": lead, "in_award_corpus": int(sol in by_sol)})
    if base_rows:
        with open(EX / "forward_signal_active_notice_baseline.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(base_rows[0].keys()))
            w.writeheader(); w.writerows(base_rows)
    pre_rows = [r for r in base_rows if r["pre_type"]]
    conv = [r for r in pre_rows if r["award_date"]]
    blead = sorted(r["notice_to_award_lead_months"] for r in conv if r["notice_to_award_lead_months"] != "")
    by_type = defaultdict(int)
    for r in pre_rows:
        by_type[r["pre_type"]] += 1
    print("\n=== ACTIVE-NOTICE BASELINE (Navy-maritime: Sub-Tier Navy + NAICS 336611/2 or PSC 1905/1925/1940) ===")
    print(f"  navy-maritime sols: {len(base_rows)}; with a pre-award notice: {len(pre_rows)} "
          f"(by type: {dict(by_type)})")
    print(f"  converted to an Award Notice (same Sol#): {len(conv)}/{len(pre_rows)} "
          f"({100*len(conv)//max(len(pre_rows),1)}%)  [archive-internal proxy, NOT ground truth]")
    if blead:
        print(f"  notice->award lead: median {pctl(blead, .5)} mo "
              f"(p25 {pctl(blead, .25)}, p75 {pctl(blead, .75)}, n={len(blead)})")
    print(f"  cross-check: {sum(r['in_award_corpus'] for r in base_rows)} of these sols are in our "
          f"{len(by_sol)}-award maritime corpus")
    print("\nwrote forward_signal_match.csv + forward_signal_active_notice_baseline.csv "
          "(+ cached _notice_sol_index.json)")


if __name__ == "__main__":
    main()
