---
title: Recompete Methodology — Backtest Findings
subtitle: Does the timing methodology actually predict recompetes? A widened, point-in-time validation
status: Working result — honest, data-bounded
---

# Recompete Methodology — Backtest Findings

**Question.** Would the recompete-timing methodology (`recompete_opportunity_methodology.md`,
`recompete_opportunity_playbook.md`) actually have predicted real recompetes, point-in-time,
with no look-ahead?

**Short answer.** The methodology's **core timing claims hold up** — recompetes are
visible ahead of time, with real lead, and the successor usually lands *before* the
incumbent's ordering period ends. But the timing clock **alone is a low-precision
screen**: "ordering-period end within 36 months" flags far more vehicles than actually
recompete in that window. It is a high-recall *filter*, not a standalone predictor — to be
decision-useful it needs the methodology's other layers (addressability, forward demand
signals, tighter requirement matching), which this data cannot fully backtest.

---

## How this differs from the prior backtest

The existing `backtest_recompete.py` (v1) replayed **11 known** maritime small-boat
predecessor→successor chains and measured only **recall** ("of recompetes that happened,
how many could we have flagged?"). It structurally **cannot see false positives** — a radar
that flags everything scores 100%. `backtest_v2_precision_recall.py` fixes this by scoring
**every material vehicle (≥ $5M)** at a monthly grid of historical freeze dates and
comparing the radar's flag against ground truth, yielding a real **confusion matrix**.

**Scope (widened to 3 segments, 533 ground-truth recompete events):**

| Segment | What it is | Vehicles | Clock source | Fidelity |
|---|---|---|---|---|
| `maritime_idiq` | parent-IDV ordering vehicles (all maritime tiers) | 55 | FPDS per-action `lastDateToOrder`, point-in-time | high |
| `ddg_myp` | DDG-51 multiyear production block recompetes | 8 | block completion set at award | medium |
| `navy_widened` | 16k-record widened navy corpus, recipient×NAICS-4 chains | ~3.6k | contract PoP `end_date` set at award | low (coarse matching) |

Point-in-time discipline: the clock "known as of freeze f" uses only actions signed ≤ f;
right-censored cells (outcome not yet observable) are excluded.

---

## Results

**1. The signature claim holds — the successor precedes the incumbent's end.**
338/533 (**63%**) of recompetes were awarded *before* the predecessor's ordering-period
end (median ~9 months early aggregate; the high-fidelity maritime subset runs ~24 months
early, matching v1). This directly confirms the methodology's central warning that **the
incumbent's end date is not the recompete date** — keying on it fires late.

**2. Anticipability (recall) is moderate and gives real lead.**

| Lead before successor award | Anticipable (radar clock within horizon) |
|---|---|
| t‑6 months  | 351/533 (65%) |
| t‑12 months | 323/533 (60%) |
| t‑18 months | 296/533 (55%) |
| t‑24 months | 227/533 (42%) |

Median radar lead over the successor award: **~23 months** (maritime-only ~12 months,
matching v1). The clock is genuinely visible ahead of time.

**3. Precision is LOW — the new, sobering finding the prior backtest hid.**

Pooled monthly confusion matrix:

| Scope | TP | FP | FN | TN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|
| ALL | 1,284 | 5,100* | 598* | 5,560* | **0.11** | 0.68 | 0.19 |
| maritime_idiq | 316 | 1,408 | 160 | 968 | **0.18** | 0.66 | 0.29 |
| ddg_myp | 23 | 169 | 129 | 156 | **0.12** | 0.15 | 0.13 |
| navy_widened | 1,250 | ~699k | ~5.7k | ~54k | **0.11** | 0.69 | 0.19 |

\*ALL is dominated by the large `navy_widened` counts; see the CSV for exact figures.

At any given month, only ~1 in 5–9 vehicles whose clock falls within 36 months actually
recompete within that window. The timing signal **over-flags**.

**4. Generalization is segment-specific.** The maritime IDIQ segment (for which the
methodology was designed) is strongest. DDG production MYP and the broad widened corpus are
weaker/coarser — exactly the caution the methodology raises in §11.

---

## Verdict

- **Directionally validated:** recompetes *are* anticipable point-in-time, with multi-month
  lead, and successors precede incumbent ends. The methodology's timing model is sound and
  its core warnings are empirically right.
- **Not a standalone classifier:** the ordering-period clock by itself is high-recall /
  low-precision. It is a *screen* that must be combined with the addressability filter and
  forward demand signals (the other half of the methodology) to be decision-useful.
- **Use it as designed:** score event-probability (timing/clock) and addressability
  separately, then read the 2×2 — the backtest shows why the timing axis alone isn't enough.

## Honest limits (why precision is a conservative floor, not a final number)

- **Monthly pooling** inflates FP: a vehicle flagged for many consecutive months with no
  recompete contributes one FP per month.
- **Coarse requirement matching** in `navy_widened` (recipient × NAICS-4) misses real
  successors; an unmatched true successor is counted as a false positive, so true precision
  is **higher** than reported here. Semantic matching is the methodology's known-hard,
  unautomated step (§11).
- **Base-award clock approximation** for `ddg_myp` / `navy_widened` (completion / PoP end at
  award) omits later option/extension drift — the high-fidelity maritime FPDS segment is the
  one to trust on lead time.
- **Cannot backtest** (per methodology §10): PALT, forward-signal lead, and the full
  addressability axis — the data has hard gaps (1‑yr opportunity window, latest-version-only
  notices). These would lift precision but aren't measurable here.

## Reproduce

```
cd projects/awards_methodology/research/datasets/saronic_navy_awards/scripts
python3 backtest_v2_precision_recall.py     # extends the FPDS cache (resumable), scores
```
Outputs (gitignored, in `extracted/`): `backtest_v2_events.csv`, `backtest_v2_confusion.csv`,
`backtest_v2_summary.json`. The original v1 replay remains at `backtest_recompete.py`.
