# Session log — Navy-thesis corpus reframe: archive/budget localization + mission-segmented backtest

**Date:** 2026-06-28
**Project:** `/Users/brendantoole/projects3/slide_factory/` — recompete-methodology research under
`projects/awards_methodology/research/datasets/saronic_navy_awards/`. Analysis, not deck rendering.
**Continues:** `2026-06-28_recompete_methodology_backtest_and_forward_signal_validation.md` (Phase-1
verdict + forward-signal) and the slide-conversion log of the same date.
**Source spec:** `/Users/brendantoole/projects3/transcript.md` (23-section strategy doc). Approved plan
file: `/Users/brendantoole/.claude/plans/please-read-and-make-recursive-simon.md`.
**No commits.** All changes in the working tree; all moved data is gitignored.

---

## What this session did (4 phases, all code complete)

Reframed the recompete backtest from "small-USV awards" onto the broader thesis **Department of the
Navy distributed maritime autonomy + autonomy-ready expeditionary / small-to-medium platforms**, and
localized all the bulk data into the repo (dropped the earlier Google-Drive/rclone idea — with 248 GB
free and ~30 GB total, **local-only** is simpler/faster).

### Phase 0 — SAM Opportunity archives localized ✅ (forward_signal NOT yet re-run)
- **Moved all 10 archives** `FY2017–FY2026_archived_opportunities.csv` (~10 GB) from `~/Downloads`
  into the gitignored **`…/saronic_navy_awards/raw/sam/opportunities_archive/`**. Confirmed 10/10 in
  place, `~/Downloads` cleared.
- **macOS TCC gotcha (important):** the shell hosting Claude Code cannot read/move files in
  `~/Downloads` (TCC "Operation not permitted" — it can `stat` them but not open them). 3 files moved
  from a prior grant; the other 7 had to be moved by the **user** in Terminal.app. If this recurs:
  user moves files manually or grants Full Disk Access.
- **`forward_signal.py` repointed:** `DOWN = ~/Downloads` → `ARCH = EX.parent/raw/sam/opportunities_archive`;
  `archives()` now `sorted(ARCH.glob("FY*_archived_opportunities.csv"))`. Streaming/index/cache logic
  unchanged. Verified it resolves the dir and finds the files.
- ⚠️ **IMMEDIATE NEXT STEP:** `python3 forward_signal.py` has **not** been run with all 10 years yet
  (context ran out right after the last archive landed). The forward-signal notice-lead numbers in the
  verdict are still the **old FY2023–25-only** figures (2.6-mo notice vs 22-mo clock). Running it now
  refreshes them across the full FY2017–26 window. This is the first thing to do.

### Phase 1 — Navy budget books moved into repo ✅
- **56 files moved** (26 books × PDF+txt + masters) into gitignored **`…/raw/budget/navy/`** (52) and
  **`…/raw/budget/dod/`** (4), sha256-verified on arrival (0 mismatches, ~1.1 GB).
- Set = **Procurement + RDTE**: SCN FY22–27, OPN FY27 (BA1/2/3/4/5-8), WPN FY27, RDTEN FY22–26
  (BA1-3 & BA4) + FY27/PB27 (BA4/BA5/BA7-8), 30-Year Shipbuilding Plan, DoD P-1/R-1 masters.
  Excluded OMN, NDAA/DAA JES, and all non-Navy services.
- **Move-one-leave-duplicates**: sourced each from one projects2 location (sources deleted), left
  duplicates elsewhere. `research_shared/budget_books` left **untouched**. Unique items (OPN, RDTEN
  FY22-26, PB27 RDTEN, DoD masters) were removed from `_newbuild_ddg`, `RDTE/`, `maritime_range`
  respectively (flagged + approved). One-off move script: scratchpad `move_budget_books.py` (not in repo).

### Phase 2 — Corpus reframe ✅
- **NEW `taxonomy/segments.json`** — LOCKED A–J taxonomy (rings 0–3) with naics/psc/keyword seeds +
  `_weights {keyword:3, psc:2, naics:1}`. Segments: A USV/ASV, B unmanned-maritime, C MCM, D NSW/
  expeditionary, E patrol/force-protection, F contested-logistics, G C2/autonomy-software, H payloads/
  sensors/EW, I small-combatants/LCS, J traditional-shipbuilding (watch-only).
- **NEW `scripts/segment_classify.py`** — deterministic `classify_segment(naics,psc,description,builder)`.
  Keyword-dominant; if keyword evidence → best score (tie→lower ring); else code-only → best (tie→**higher**
  ring, conservative, so generic 336611→J); else `U`. Handles the CSV's stringified-dict naics/psc
  (`_code()` extracts the bare code — without this 91% came back U). Returns `classifier_basis`
  (description|mixed|code_only|none) + `classifier_confidence` (high|med|low).
- **`phase1_common.build_families`** now tags every family with `segment_primary`, `segment_tags`,
  `ring`, `classifier_basis`, `classifier_confidence`. **`segment` (clock type: maritime_idiq/ddg_myp/
  navy_widened) is LEFT UNCHANGED** — it drives the clock logic; segment_primary is the orthogonal
  reporting axis.
- **`backtest_v2_precision_recall.build_widened`** now carries `description` (needed for keyword
  classification of widened families).
- **`pull_navy_widened_discovery.py`** — added **customer-based scope**: `CUSTOMER_SCOPES` =
  navy_awarded (awarding subtier) + navy_funded (funding subtier), unioned per award into a new
  `customer_flags` column. **NOT re-pulled** (network); existing `navy_widened_discovered.csv` (16.4k,
  awarding-Navy only) still drives the current results.

### Phase 3 — Segmented backtest + metrics + leakage ✅
- **`phase1_backtest.py`** — predictions_asof.csv gains columns: `segment_primary, ring,
  classifier_basis, classifier_confidence`. Ran clean (144,779 rows).
- **`phase1_metrics.py`** — **HEADLINE reporting rule (per user directive): Arm A on clock segments
  (maritime_idiq/ddg_myp), Arm B on mission segment_primary (A–J), never pooled.** metrics_by_segment.csv
  gains a `report_axis` column. NEW **`segment_crosswalk.csv`** = both-axis diagnostic
  (arm × clock_segment × segment_primary) with `n_families/n_positive/n_negative_mature/n_censored`,
  modal `classifier_basis/confidence`, and `suppressed=yes` when n_pos<10 or n_families<30.
- **Leakage suite: ALL PASS** (as-of invariance 0/220, label-shuffle→chance, oracle 1.0/1.0).
- **`phase1_review.py`** re-ran (Arm A unchanged: 17 FP / 5 FN, semantic self-check 1.00/0.89).
- **Verdict** `methodology/recompete_backtest_phase1_verdict.md` — added a **Mission-segment reframe
  addendum** (per-segment table, provenance note, tiny-slice suppression) with the user's two verbatim
  caveats: *Arm A = high-fidelity timing/recall cohort; Arm B = mission/breadth cohort*, and *Arm A
  A–J slices are not interpreted (code-only) — mission conclusions come from Arm B*.
- **Deck still builds** (`cd projects/awards_methodology && python3 build_deck.py` → 3 slides). **Git
  hygiene clean** — only code+markdown tracked; the ~11 GB moved data is gitignored (`datasets/*/raw/`).

---

## Results (award-side backtest, existing widened pull; forward-signal NOT refreshed)

**Arm A (high-fidelity validation cohort) — unchanged, reproduces prior verdict:**
maritime_idiq (34 fam / 18 pos): model **P 0.48 [0.32,0.65] / R 0.83 [0.61,0.94] / ~22 mo lead**;
incumbent-rebuy P 0.80. ddg_myp tiny (4 pos).

**Arm B by mission segment (model = clock radar; strong baseline = ldo+runrate via PR-AUC):**

| Seg | fam | pos | model P / R | lead | PR-AUC model / ldo+rr | basis |
|---|---|---|---|---|---|---|
| D NSW/expeditionary | 49 | 103 | 0.71 / 0.73 | 20 | 0.69 / 0.78 | desc |
| B unmanned-maritime | 31 | 67 | 0.67 / 0.67 | 19 | 0.60 / 0.72 | desc |
| J traditional-shipbuilding | 248 | 583 | 0.69 / 0.69 | 22 | 0.65 / 0.85 | desc |
| H payloads/sensors/EW | 322 | 675 | 0.62 / 0.63 | 21 | — | code_only |
| C mine-countermeasures | 211 | 196 | 0.44 / 0.63 | 24 | 0.43 / 0.58 | code_only |
| G C2/autonomy-software | 350 | 237 | 0.36 / 0.90 | 21 | 0.28 / 0.54 | code_only |
| U unclassified | 649 | 218 | 0.24 / 0.69 | 24 | 0.26 / 0.41 | none |
| *(suppressed n<thr)* | A 11, E 7, F 6, I 26 | | *crosswalk only* | | I scored strong: PR-AUC 0.76/0.86 | |

**Story:** the Arm-A pattern (high recall 0.63–0.90 + ~19–24 mo lead, modest precision riding the base
rate, simple ldo+runrate winning ranking) **reproduces across the whole Navy mission map** — it's a
high-recall early-warning screen everywhere, not a maritime quirk. Most decision-useful: D, B, J.
Description-backed segments (B, D, J) are trustworthy; code-only (C, G, H) read with the provenance
caveat. **Verdict stays PARTIAL** — early-warning screen, not a precise standalone predictor — now
shown to hold at breadth.

---

## Files created / modified (all tracked code+markdown; data gitignored)

**Created:** `taxonomy/segments.json`, `scripts/segment_classify.py`.
**Modified:** `scripts/forward_signal.py`, `scripts/phase1_common.py`, `scripts/phase1_backtest.py`,
`scripts/phase1_metrics.py`, `scripts/backtest_v2_precision_recall.py`,
`scripts/pull_navy_widened_discovery.py`, `methodology/recompete_backtest_phase1_verdict.md`.
**New gitignored outputs:** `extracted/segment_crosswalk.csv` (+ refreshed predictions_asof.csv,
metrics_by_segment.csv, extension_drift.csv, fp/fn_review.csv, semantic_match_metrics.csv).
**New gitignored data:** `raw/sam/opportunities_archive/FY2017–2026*.csv`, `raw/budget/{navy,dod}/*`.

---

## Open / next (prioritized)

1. **RUN `python3 forward_signal.py`** (from `…/saronic_navy_awards/scripts`) — all 10 archives now in
   place; this refreshes the notice-lead distribution across FY2017–26. Then update the forward-signal
   addendum numbers in the verdict (currently FY2023–25-only). **Do this first.**
2. **Re-pull the widened corpus with the customer scope** (`python3 pull_navy_widened_discovery.py`,
   network; `SMOKE=1` first to smoke-test) to actually realize navy_funded breadth, then re-run
   phase1_backtest → phase1_metrics → phase1_leakage_tests. The funding path should pull in DIU/DARPA/
   SCO/ONR-awarded-but-Navy-funded autonomy/OT work the awarding-only filter missed.
3. (Optional) `python3 phase1_label_outcomes.py` (network, SAM) — only if Arm B outcome/addressability
   labels are wanted; Arm A's 22-event taxonomy is unchanged.
4. Manual adjudication of `extracted/labeled_pairs.csv` (real semantic-matcher validation vs the
   current auto-proxy).
5. Deferred "full program" (transcript): point-in-time notice 3-variant model, calibration, two-reviewer
   validation, addressability scoring model, budget-line crosswalk, pre-FY2017 archives.

## Reproduce

```
cd projects/awards_methodology/research/datasets/saronic_navy_awards/scripts
python3 segment_classify.py       # taxonomy self-test + widened A-J distribution (8% U)
python3 phase1_backtest.py        # -> predictions_asof.csv (with segment cols)
python3 phase1_metrics.py         # -> metrics_by_segment.csv + segment_crosswalk.csv
python3 phase1_leakage_tests.py   # negative controls (must ALL PASS)
python3 forward_signal.py         # NEXT: notice-lead over full FY2017-26 archive set
```

## Design decisions worth remembering
- **Reporting discipline (user directive):** never read Arm A's A–J mission labels as conclusions —
  Arm A has no descriptions so segment_primary is code-only/low-confidence. Arm A = clock-segment
  timing/recall cohort; Arm B = mission segment_primary breadth cohort; never pool. Every row carries
  classifier provenance; tiny slices suppressed. (Splitting Arm A's 22 positives across code-only labels
  would manufacture false precision.)
- Taxonomy is **locked before inspecting outcomes** (segments.json is editable to refine seeds).
- Pure-stdlib repo — no pandas/DuckDB/rclone added.
