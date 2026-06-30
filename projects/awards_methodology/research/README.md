# Awards Methodology — Research

Supporting research behind the `awards_methodology` deck (Defense Market Strategy /
Market Access Framework). The slides in `../awards_methodology/slides/` are the
visual output; the material here is the evidence and reasoning behind them.

Moved here from `ooxml_build_pipelines_light/projects/awards_methodology/` and
reorganized into a flatter, intent-revealing layout. Original data filenames are
preserved — only the folder structure was changed.

## Layout

```
research/
├── Federal_Awards_API_HowTo.md   Practitioner guide to USAspending / SAM / FPDS APIs
├── methodology/      Narrative methodology + validation
│   ├── recompete_opportunity_playbook.md
│   ├── recompete_opportunity_methodology.md
│   └── recompete_backtest_findings.md   Does it work? point-in-time backtest verdict
├── wiki/             18-topic federal-contract lexicon (INDEX.md + 01–18)
└── datasets/         Evidence corpora, one folder per dataset
    ├── ddg51_recompete_cadence/      DDG-51 MYP / subaward recompete cadence
    └── saronic_navy_awards/          Navy widened-discovery award corpus
```

Each dataset folder is split three ways:

- `scripts/` — the pull / build Python that produced the corpus *(tracked)*
- `extracted/` — analysis-ready derived CSV/JSON tables *(gitignored)*
- `raw/` — raw API pulls, split by source system *(gitignored)*
  - `raw/sam/…` — SAM.gov contract-award / subaward JSON
  - `raw/usaspending/…` — USAspending pulls (`detail/`, `funding/`, `transactions/`)

## What backs which slide

- **Contract Addressability** (decision framework) and **Recompete Timing**
  (color-of-money obligation windows) — `methodology/` + wiki topics 03, 05, 07,
  11, 15.
- **Recompete Timing & Outlook** (AN/SLQ-25 "Nixie" case study) — the Nixie IDIQ
  N0025321D0002 records live in `datasets/saronic_navy_awards/` (USAspending /
  SAM pulls for NAICS 334511 / PSC 5865).

## Backtest (does the methodology work?)

**Phase-1 (current, rigorous):** a leakage-controlled, frozen-date **award-side** radar replay at
requirement-family / first-alert-episode level, with negatives, baselines, family-bootstrap CIs,
an outcome taxonomy (SAM `reasonForModification`), and negative-control leakage tests. Verdict +
numbers: `methodology/recompete_backtest_phase1_verdict.md`. Scripts: `…/scripts/phase1_*.py`
(`phase1_common`, `phase1_backtest`, `phase1_metrics`, `phase1_leakage_tests`,
`phase1_label_outcomes`, `phase1_review`). Headline: the clock radar **anticipates** recompetes
well (recall 0.83, ~22-mo lead, leak-clean) but is a weak **precision** instrument — a high-recall
screen that needs the addressability axis; only 4/22 flagged events are *open* opportunities.

**Forward-signal layer:** `…/scripts/forward_signal.py` joins the SAM Data Services **archived**
Contract Opportunities bulk extracts (FY2023–2025, streamed from `~/Downloads`, not copied into the
repo) to awards by `Sol#` — recovering the historical pre-award notices the public API blocks.
Findings (in `phase1_verdict.md`): award↔notice matching 2→147, ~47% of in-window awards are "dark"
(no notice), and the notice fires only ~2.6 mo before award vs the clock's ~22 mo — i.e. the
award-side clock beats the portal as an early warning.

**Earlier:** `backtest_recompete.py` (v1, recall-only, 11 chains) and
`backtest_v2_precision_recall.py` (v2, cell-level precision/recall, 3 segments —
`methodology/recompete_backtest_findings.md`; its ~0.11 precision is a cell-level artifact that
Phase-1 corrects to ~0.48 at family level). All reuse the FPDS clock cache
`…/extracted/_fpds_timelines.json`.

## Running the pull / analysis scripts

The `pull_*.py` scripts (SAM.gov pulls) read `SAM_API_KEY` from a `.env` at the
slide_factory repo root (resolved by `…/saronic_navy_awards/scripts/_common.py`, which walks
up to find the nearest `.env`). The `.env` is **gitignored** — never commit it. The FPDS
ATOM feed used by the backtest needs no key.

## Git tracking

`datasets/*/raw/` and `datasets/*/extracted/` are gitignored (see repo-root
`.gitignore`): the ~150 MB of raw + derived corpora stay on disk but out of
version control. The `scripts/`, `methodology/`, and `wiki/` markdown are tracked.

## Not moved (still in the source pipeline repo)

Slide generators + source `.pptx`, `slide_specs/`, session `logs/`,
`EVIDENCE_MEMO.md`, the shiprepair recompete radar, pull logs, and the Excel
evidence workbook were intentionally left in
`ooxml_build_pipelines_light/projects/awards_methodology/`.
