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
├── methodology/      Narrative methodology
│   ├── recompete_opportunity_playbook.md
│   └── recompete_opportunity_methodology.md
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

## Git tracking

`datasets/*/raw/` and `datasets/*/extracted/` are gitignored (see repo-root
`.gitignore`): the ~150 MB of raw + derived corpora stay on disk but out of
version control. The `scripts/`, `methodology/`, and `wiki/` markdown are tracked.

## Not moved (still in the source pipeline repo)

Slide generators + source `.pptx`, `slide_specs/`, session `logs/`,
`EVIDENCE_MEMO.md`, the shiprepair recompete radar, pull logs, and the Excel
evidence workbook were intentionally left in
`ooxml_build_pipelines_light/projects/awards_methodology/`.
