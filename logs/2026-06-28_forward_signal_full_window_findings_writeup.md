# Session log — Forward-signal full-window run + findings/advice/timeline write-up

**Date:** 2026-06-28
**Project:** `/Users/brendantoole/projects3/slide_factory/` — recompete-methodology research under
`projects/awards_methodology/research/datasets/saronic_navy_awards/`. Analysis, not deck rendering.
**Continues:** `2026-06-28_navy_thesis_reframe_storage_localization_and_segmented_backtest.md`
(its open item #1: re-run `forward_signal.py` over the full archive set).
**No commits.** New markdown is tracked; all regenerated data is gitignored.

## What this session did

Realized the prior log's "Do this first" step, then — per a mid-task user redirect — packaged the
result as a **new standalone markdown** instead of editing the verdict/README in place.

1. **Ran `forward_signal.py` over the full FY2017–26 archive set.** All 10 archives present (~10 GB).
   Forced a clean cache rebuild (`rm extracted/_notice_sol_index.json`) to confirm a fresh stream
   reproduces the numbers, not a stale cache: ~75 s to stream all 10, identical output. Regenerated
   `extracted/forward_signal_match.csv` + cache (both gitignored).

2. **Full-window results** (notice span 2016-10-01 … 2026-06-27; 466 award↔notice Sol# matches):
   in-window awards **276 → 856**; have a notice **53% → 69%**; **portal-dark 47% → 31%**; median
   pre-sol lead **2.6 → 4.6 mo** (early-signal SS/Presol-only **4.3 → 9.8 mo**); recompete-successor
   **1 in-window → 8/18 matched, median 9.7 mo** (7 dark, 3 out-of-window). Pre-sol lead is right-skewed
   (p25 1.1 / median 4.6 / p75 16.6). Thesis intact: clock (~22-mo lead) still beats the portal as
   early warning by ~17 mo; full window softens only the dark-rate magnitude.

3. **Assembled real award-timeline triplets** (T1 method-flag = award − lead_months from
   `backtest_v2_events.csv`; T2 notice = award − notice-lead from the `forward_signal.py` recompete
   block; T3 award). Six examples across small-craft builders + a DDG dark case + an honest counter:
   Metal Shark/Gravois (hero, 43.6 vs 18.2 mo), Metalcraft (29.4 vs 5.2), Willard (18.7 vs 5.7),
   Snow (12.1 vs 9.7), **Bath Iron Works DDG-51 FY18-22 MYP $5.3B — method 21.3 mo, portal fully dark**,
   Ribcraft (counterexample: portal led by ~10 mo when the clock sat far out).

4. **Wrote the deliverable:** `methodology/recompete_forward_signal_findings_and_timeline_examples.md`
   — section A (results + old→new table), section B (methodology improve-or-not, grounded in §10–12),
   section C (timeline-slide examples + an ASCII "how to draw it" mock). It states it **supersedes** the
   verdict's FY2023–25 forward-signal addendum; the verdict and README were left **unchanged** per the
   redirect.

## Files
- **Created (tracked):** `methodology/recompete_forward_signal_findings_and_timeline_examples.md`;
  this log.
- **Regenerated (gitignored):** `extracted/forward_signal_match.csv`, `extracted/_notice_sol_index.json`.
- **Unchanged:** `recompete_backtest_phase1_verdict.md`, `research/README.md` (still cite the FY2023–25
  slice; the new md is the canonical full-window write-up).

## Notes / next
- If desired later, refresh the verdict addendum + README forward-signal paragraph to the full-window
  numbers and correct the now-false "streamed from ~/Downloads, not copied into the repo" line (the
  archives are in-repo at `raw/sam/opportunities_archive/`). Deferred per scope.
- Prior log's other open items (#2 widened re-pull with customer scope, #3 outcome labeling, #4
  adjudication, #5 full program) remain untouched.

## Rev 2 — review fixes (same session)

User reviewed the write-up: endorsed the conclusion, asked for metric/wording fixes before it's canonical.
All applied to `recompete_forward_signal_findings_and_timeline_examples.md`:

1. **Metric relabel** — `preaward_lead_months` is *earliest-matched-SAM-notice→award* lead, NOT
   "pre-solicitation lead" (it's the earliest of SS/Presol/Solicitation/Combined Synopsis per
   `forward_signal.py:37,121,126`). `early_lead_months` = SS/Presol-only notice→award. Named the two
   front-end leads we do NOT yet measure (solicitation→award PALT proxy; sources-sought→solicitation).
2. **Denominators** — 466 = unique normalized award Sol# keys matched; 594 = in-window award *rows* with
   ≥1 matched notice; 856 = in-window rows; 262 dark; 254 out-of-window. Stated explicitly.
3. **Dark phrasing** — everywhere now "no matched notice via the normalized solicitation-number join"
   (upper bound). **Key correction:** the DDG-51 example is NOT dark — manual provenance check shows it had
   a competitive solicitation **N0002418R2302** (FULL & OPEN AFTER EXCLUSION, 2 offers). It only read dark
   because the recompete join keyed on the contract PIID, and N0002418R2302 is neither in the maritime
   award-sol universe nor was queried against the archive. It's a **join miss**, not a dark buy — removed
   the "$5.3B invisible to portal" slide punchline; reframed as the motivation for join calibration.
4. **Paired deltas** — computed method_lead − notice_lead on the matched recompete events directly:
   n=7 evaluable, **median +2.4 mo** (p25 −10.3, p75 +24.2), clock leads 5/7. Much more modest than the
   distribution-level ~17-mo gap (which mixes the Arm-A method cohort with the all-rows notice
   distribution). Report both, labeled; lead with the conservative paired figure. Added two honest example
   rows: Ribcraft (portal led −10.3) and Silver Ships (radar missed, clock ran to 2028, −47.4).
5. **"Full window" → "full local archive window, FY2017–FY2026"** throughout (10 local files, not the
   full SAM history back to ~2001).
6. **Active-notice baseline** added as the explicit next forward-signal task (gives the portal layer a
   real precision estimate, not just award-outcome recall).

Also added a closing "What this does / does not establish" section. No code changed; only the markdown.
Verdict/README still untouched (the new md remains canonical for full-window results).

## Rev 3 — recompete-join fix (real Sol#, not PIID) + active-notice baseline (code change)

User asked to actually fix the join bug rev-2 surfaced, and fold in the active-notice baseline. All in
`scripts/forward_signal.py` (its internals aren't imported elsewhere; `build_ddg/build_maritime`
untouched). Plan: approved `please-read-logs-2026-06-28-navy-thesis-merry-hollerith.md`.

**Code changes:**
- New `succ_sol_map(idv_sols)` — unified `successor piid -> set(real Sol#)`: maritime via the existing
  `idv_sols` (parent_idv_piid → order solicitation_identifiers), DDG via `ddg_myp_recompete_provenance.csv`
  `solicitation_id`. Recompete loop now uses this and drops the wrong `norm(s["piid"])` fallback;
  classifies each event **matched / dark / unresolved / out-of-window**.
- Successor sols injected into `want` so DDG solicitations (e.g. N0002418R2302) get indexed while streaming.
- `build_index` refactored: same single stream now also collects the **active-notice baseline** (Navy
  Sub-Tier + NAICS 336611/2 or PSC 1905/1925/1940 → per-sol earliest pre-award + earliest Award Notice),
  writes `extracted/forward_signal_active_notice_baseline.csv`. Cache made **exact** (schema_version=2 +
  file sig + sha1 want-hash + DDG-provenance sig) so adding sols can't reuse a stale index; hashlib (not
  builtin hash) for cross-run stability.

**Results (fresh ~72 s stream; verified cache hit on 2nd run; outputs gitignored):**
- Recompete join: **8 matched/7 dark → 12 matched / 2 truly-dark / 1 unresolved / 3 oow.** The DDG MYPs
  were never dark — Bath/Huntington FY18-22 had a **Presol 9.4 mo** (sol N0002418R2302); FY23-27 a
  **Presol 14.3 mo** (N0002422R2302). The rev-2 "DDG is a join miss / $5.3B invisible" was wrong; it's now
  a *matched* example.
- **Segment split (paired method−notice):** maritime IDIQ **+2.4 mo, clock leads 5/7**; DDG MYP
  **−7.4 mo, clock leads 1/4** — the block-completion clock points years past the calendar-cadence MYP
  recompete, so the Presol leads. This is the headline new finding: the clock is the right radar for IDIQ,
  the wrong one for MYP. Folded into the markdown's conclusion + §B "Change" + §C.2.
- **Active-notice baseline:** 7,507 Navy-maritime sols; 5,576 with a pre-award notice (Presol 1,643 / SS
  1,579 / Solicitation 1,298 / Combined 1,056); **11% (656/5,576)** convert to a same-Sol# Award Notice,
  median lead 2.8 mo. Framed as a LOWER BOUND (award-notice sparsity + Sol# drift), not portal precision.

Markdown rewritten to rev-3 (recompete table old→new, segment-split paired table, DDG reframed from "dark"
to "wrong-radar-for-MYP", new §A.4 baseline, updated establishes/doesn't-establish). Verdict/README still
untouched.

## Reproduce
```
cd projects/awards_methodology/research/datasets/saronic_navy_awards
python3 scripts/forward_signal.py   # -> forward_signal_match.csv + forward_signal_active_notice_baseline.csv
```
