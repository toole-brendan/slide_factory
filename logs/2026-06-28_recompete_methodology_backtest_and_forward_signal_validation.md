# Session log — recompete methodology: backtests, leakage-controlled Phase-1 pilot, and forward-signal validation

**Date:** 2026-06-28
**Project:** `/Users/brendantoole/projects3/slide_factory/` — standalone pure-stdlib OOXML→PPTX workspace; this session is analysis, not deck rendering.
**Scope:** empirically test whether the awards_methodology **recompete-timing methodology** (behind the 3 slides ported earlier today) actually predicts recompetes, point-in-time. Work lives under `projects/awards_methodology/research/datasets/saronic_navy_awards/scripts/` (code, tracked) and `…/extracted/` (outputs, gitignored).

No commits; all changes in the working tree. The deck still builds (`cd projects/awards_methodology && python3 build_deck.py` → 3 slides). Continues the earlier log `2026-06-28_awards_methodology_slides_2_3_7_conversion_and_research_consolidation.md` (slide conversion + research move).

---

## 1. v2 precision/recall backtest (corrected v1's recall-only design)

The existing `backtest_recompete.py` (v1) only replayed 11 KNOWN maritime chains → measured recall, blind to false positives. Built `backtest_v2_precision_recall.py`: monthly-freeze replay scoring EVERY vehicle ≥$5M across 3 segments (maritime IDIQ via FPDS as-of `lastDateToOrder`; DDG-51 MYP; the 16k widened navy corpus), with a pooled confusion matrix + right-censoring. 533 ground-truth events. Result: recall ~60–65%, **precision ~0.11–0.18**, and the signature "successor precedes incumbent end" held at 63%. Wrote `methodology/recompete_backtest_findings.md`. (The ~0.11 precision later proved to be a **cell-level artifact** — see §4.)

## 2. SAM key + API how-to wired into the repo

Copied the SAM `.env` (key) to the repo root **gitignored first** (`.gitignore` now ignores `.env`/`*.env`), copied `Federal_Awards_API_HowTo.md` into `research/`, and repointed the key loader (`_common.py` now walks up to find `.env`; fixed the two DDG pull scripts whose `_common` import path our earlier research move had broken). Verified the key loads from the new location.

## 3. Tested the SAM Opportunities API (not just the docs)

User challenged the "forward-signal is data-blocked" claim. Probed the public API live: historical 1-yr windows return active notices, but `status=Archived` **and** lowercase `archived` both **500**; for our maritime NAICS, past sources-sought/presol/solicitation return **0** (only a few award notices). Conclusion (tested): historical **pre-solicitation** signal is blocked via the *public* API — so the backtest must be **award-side** (predict the follow-on award; lead measured before award, not before solicitation).

## 4. Phase-1 leakage-controlled award-side pilot (the main build)

Designed via plan agent, user-reviewed/green-lit with edits, then built (`phase1_common`, `phase1_backtest`, `phase1_metrics`, `phase1_leakage_tests`, `phase1_label_outcomes`, `phase1_review`):

- **Requirement-FAMILY / first-alert-episode** as the primary unit (cells demoted to operating-burden), **as-of-freeze features only** (incumbent/clock recomputed ≤freeze; `final_ldo`/successor identity quarantined), maturity rule with the DoD 90-day lag, **two arms** (high-fidelity maritime+DDG; widened breadth — never pooled).
- **Baselines:** expiring-18/36mo, top-run-rate, incumbent-rebuy, and the strong **LDO-proximity+run-rate**. **Metrics:** family-level precision/recall/F1, precision@K, PR-AUC, lead, with **Wilson + family-bootstrap CIs**; extension-drift table.
- **Leakage negative controls — ALL PASS:** as-of feature invariance (0/220 mismatches when post-freeze data deleted), label-shuffle (skill collapses to chance → no hidden leak), oracle control (peeking feature → precision/recall 1.0 → metric is leak-sensitive).
- **Outcome taxonomy** via fresh **SAM Contract Awards** pulls (`reasonForModification`; "EXERCISE AN OPTION" is code **G**, not D). Page key was `awardSummary` (fixed after an empty first pull).

**Headline (Arm A maritime, 18 pos / 28 neg episodes):** recall **0.83 [0.61–0.94]**, precision **0.48 [0.32–0.65]**, **~22-mo median lead** — i.e. family-level precision is **~0.48, correcting v2's cell-level 0.11**. The timing `model` binary == expiring-36mo; label-shuffle shows its precision barely beats chance → **value is recall + lead, not precision**. **incumbent-rebuy is the most precise signal (0.80)**; run-rate adds no ranking lift at this scale. **Decisive:** of 22 flagged events only **4 are open recompetes** (16 limited/set-aside, 1 option, 1 bridge) — empirical case for the methodology's event-probability-vs-addressability split. Verdict in `methodology/recompete_backtest_phase1_verdict.md`: **PARTIAL — validated as a high-recall early-warning screen, not a standalone predictor.**

## 5. Forward-signal layer from SAM Data Services archived bulk

User supplied the **archived Contract Opportunities** bulk extracts (FY2023–25, ~1.2 GB each = the historical pre-award notices the public API blocks). Built `forward_signal.py`: streams them from `~/Downloads` (never copied into the repo), Sol#-targeted, caches a tiny index. Findings (in-window maritime awards, n=276):

- award↔notice matching **2 → 147**;
- **~47% "dark"** (only 53% had any synopsized notice) — empirical FAR 16.5 / OT incompleteness;
- **notice fires LATE: median 2.6-mo** lead (early signals 4.3-mo) vs the award-side clock's **~22-mo** → the clock beats the portal by ~18 months (strengthens the methodology's thesis);
- recompete-successor linkage works (one in-window major recompete had a **Sources Sought 18.2-mo** before award).

Generalized `forward_signal.py` to **auto-ingest any FY2001–FY2026** archive present (existence-check, not glob — macOS sandboxes `~/Downloads` against directory *listing* while allowing known-path reads; the glob silently returned nothing). With only 3 years loaded, 13/18 recompete events are simply out-of-window — a **data-coverage** gap, not a method limit; adding the back-years puts all events in-window for a full recompete pre-solicitation lead distribution + active-notice baseline. (Next data step: drop FY2009–2026 archives into `~/Downloads`; the tool picks them up, no code change.)

## Artifacts

- **Scripts (tracked):** `backtest_v2_precision_recall.py`, `phase1_common.py`, `phase1_backtest.py`, `phase1_metrics.py`, `phase1_leakage_tests.py`, `phase1_label_outcomes.py`, `phase1_review.py`, `forward_signal.py`; `_common.py` + DDG pull scripts repointed.
- **Methodology docs (tracked):** `recompete_backtest_findings.md` (v2), `recompete_backtest_phase1_verdict.md` (Phase-1 + forward-signal addendum); README updated.
- **Outputs (gitignored, in `extracted/`):** `predictions_asof.csv`, `metrics_by_segment.csv`, `extension_drift.csv`, `outcome_labels.csv`, `fp_review.csv`/`fn_review.csv`, `semantic_match_metrics.csv`, `labeled_pairs.csv` (seed for manual adjudication), `forward_signal_match.csv`, `_notice_sol_index.json`.

## Git posture

`.env` and all `datasets/*/raw|extracted/` corpora gitignored; scripts + methodology markdown tracked. Verified via `git check-ignore` / `git add -n`. The multi-GB SAM archives stay in `~/Downloads`, never committed.

## Open / next

- Drop the remaining FY archived-opportunities files (2009–2026) into `~/Downloads` → re-run `forward_signal.py` for the full recompete forward-signal backtest.
- Manual adjudication of `labeled_pairs.csv` for a real semantic-matcher validation (currently an auto-proxy sanity check).
- Phase 2/3 (standalone definitive contracts; task/delivery orders) remain future scope.
