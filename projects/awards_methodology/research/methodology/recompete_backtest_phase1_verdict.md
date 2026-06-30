---
title: Recompete Methodology — Phase-1 Backtest Verdict
subtitle: Leakage-controlled, frozen-date award-side radar replay (parent IDIQ/MAC/GWAC)
status: Working result — honest pilot, not a full validation
---

# Phase-1 Backtest Verdict

**Scope (read first).** This validates only the **award-side parent-vehicle radar**: whether
last-date-to-order + as-of obligation history + incumbent/rebuy structure identify future vehicle
**successor awards** earlier than naive expiration baselines, point-in-time, no look-ahead. The
historical pre-solicitation layer is blocked through the *public* SAM Opportunities API
(latest-active-version, 1-yr-windowed, `status=archived` 500s — tested) but was partially
**unblocked** via the SAM Data Services **archived** bulk extracts (FY2023–2025); see the
forward-signal addendum below. Missing notices are a **visibility state, not an absent
opportunity**. Results are reported at **requirement-family / first-alert-episode** level;
vehicle×month cells are operating-burden diagnostics only.

## Pre-registered acceptance criteria

**Useful if (family-level):** (1) full method beats expiring-18mo, expiring-36mo, AND
LDO-proximity+run-rate on precision@K; (2) positive median first-alert lead; (3) false positives
mostly explainable; (4) directionally positive under family-bootstrap CIs; (5) no leakage-audit
failures. **Not validated if:** lift only at cell level; positives only from hand-selected chains;
FPs dominated by semantic mismatches; missing notices treated as no-procurement; Arm B drives the
conclusion.

## Cohort (counts, not "N≈20")

| Arm / segment | families | positive episodes | negative episodes | censored | fidelity |
|---|---|---|---|---|---|
| A / maritime_idiq | 34 | 18 | 28 | 8 | high (FPDS as-of clocks) |
| A / ddg_myp | 3 | 4 | 2 | 2 | high (block completion) |
| B / navy_widened | 1,910 | 2,250 | 1,891 | 699 | **low (proxy; subordinate)** |

## Results — Arm A maritime (the primary, high-fidelity result)

Episode-level, family-bootstrap / Wilson 95% CIs:

| Scorer | Precision | Recall | F1 | Median first-alert lead |
|---|---|---|---|---|
| **model** (clock-within-36mo radar) | 0.48 [0.32, 0.65] | **0.83 [0.61, 0.94]** | 0.61 | **~22 mo** |
| expiring-18mo | 0.39 | 0.50 | 0.44 | ~23 mo |
| expiring-36mo | 0.48 | 0.83 | 0.61 | ~22 mo |
| **incumbent-rebuy** | **0.80 [0.49, 0.94]** | 0.44 | 0.57 | ~40 mo |

Ranking (precision@10 / PR-AUC): model 0.27 / 0.40 · LDO+run-rate 0.28 / 0.39 · run-rate 0.24 ·
incumbent-rebuy 0.31. 

**Reading:**
- The radar **anticipates recompetes well**: recall 0.83 with a **~22-month median lead** — the
  ordering-period clock is genuinely visible years ahead. The methodology's core timing claim and
  its "incumbent end ≠ recompete date" warning hold.
- **But the timing clock is a weak *precision* instrument.** The `model` binary is *identical* to a
  naive 36-month expiration watchlist by construction, and the label-shuffle control shows its
  precision (0.48) sits at the top of the chance band [0.29, 0.48] just above the 0.39 base rate.
  Its value is **recall + lead, not precision**.
- **The elaborate features do not beat the simple baselines.** Adding obligation run-rate gives no
  ranking lift (PR-AUC 0.39 vs 0.40). The single most *precise* signal is **incumbent-rebuy**
  (0.80) — "this family has recompeted before and its clock is approaching" — at the cost of recall.

## The decisive finding: most "events" are not reachable opportunities

Of the 22 Arm-A recompete events (SAM Contract Awards taxonomy):

| Outcome | n |
|---|---|
| vehicle_recompete_limited_or_set_aside | 16 |
| **vehicle_recompete_open** (reachable by a new entrant) | **4** |
| option_or_ordering_period_extension (not a real recompete) | 1 |
| bridge_or_extension | 1 |

Only **4 of 22** flagged events are *open* recompetes. This is the empirical case for the
methodology's central design rule: **score event-probability and addressability separately** — a
recompete happening is not a reachable opportunity. A timing radar alone over-promises.

## Error review & robustness

- **False positives:** 17 negative episodes the radar flagged; **7/17 are on vehicles whose
  ordering clock drifted outward** (`extension_drift.csv`: 17/54 maritime vehicles shifted their
  LDO later) — a known, explainable cause, not random noise. The rest are genuine one-off vehicles.
- **False negatives:** 5 missed recompetes (clock not within horizon at any mature freeze).
- **Leakage controls — ALL PASS:** as-of feature invariance (0/220 mismatches when post-freeze data
  is deleted), label-shuffle (real skill collapses to chance, so no hidden leak), oracle control
  (a peeking feature drives precision/recall→1.0, proving the metric is leak-sensitive).
- **Semantic matcher self-consistency:** family key (NAICS4+PSC+builder) vs a builder+NAICS4
  requirement proxy → precision 1.00 [0.82,1.00], recall 0.89 [0.69,0.97] (AUTO-proxy; see
  `labeled_pairs.csv` seeded for manual adjudication — a sanity check, not a human validation).

## Arm B (breadth, subordinate — does NOT drive the verdict)

navy_widened (2,250 positives, contract-level proxy, PoP-end clock): model precision 0.50 / recall
0.69. At scale the ranking baselines **do** separate — precision@10: model 0.39 < run-rate 0.48 <
LDO+run-rate 0.58 < incumbent-rebuy 0.67; PR-AUC model 0.47 < LDO+run-rate 0.70. So obligation
run-rate and prior-rebuy add real ranking power at volume — corroborating direction only.

## Verdict against the criteria

**PARTIAL — validated as an early-warning screen, not as a standalone predictor.**

1. Beats all baselines on precision@K — **NOT MET.** Timing-model precision@10 (0.27) ties the
   strong LDO+run-rate baseline (0.28) and trails incumbent-rebuy (0.31); the model binary equals
   expiring-36mo.
2. Positive median lead — **MET** (~22 months).
3. FPs explainable — **MOSTLY MET** (clock drift + limited/option/bridge taxonomy).
4. Directionally positive under CIs — **MET for recall/lead**; precision overlaps the base rate.
5. No leakage failures — **MET.**

**Bottom line.** The award-side clock radar reliably and leak-cleanly *anticipates* recompetes with
multi-year lead (recall 0.83, ~22-mo lead), so the methodology's timing model is sound as a
**high-recall screen**. It is **not** a precise standalone classifier: timing alone barely beats a
36-month expiration list, the extra features add little at this scale, and most flagged events are
not open opportunities. Operationally, use the clock to *cast the net early*, then apply the
**addressability filter + incumbent-rebuy prior** to rank — exactly the two-axis design the
methodology prescribes. "Validated" (per the standard) is not reached: high-fidelity positives are
~22 with wide CIs, and the precision case needs either more FPDS-clock families (more NAICS/agencies)
or the addressability/forward-signal layers this data can't supply.

## Mission-segment reframe addendum (Navy distributed-maritime-autonomy, 2026-06-28)

The corpus was re-centered from "small-USV awards" onto the broader thesis **Department of the Navy
distributed maritime autonomy and autonomy-ready expeditionary / small-to-medium maritime
platforms**. A LOCKED taxonomy (`taxonomy/segments.json`, segments **A–J** with rings 0–3) and a
deterministic classifier (`segment_classify.py`, keyword-dominant, NAICS/PSC supporting) assign every
requirement family a `segment_primary`, secondary `tags`, a `ring`, and a **classifier provenance**
(`classifier_basis` ∈ description|mixed|code_only|none, `classifier_confidence` ∈ high|med|low).

**Reporting rule (never pool A and B).** Headline metrics use **Arm A on its high-fidelity clock
segments** (`maritime_idiq`/`ddg_myp`) and **Arm B on mission `segment_primary` (A–J)**. Arm A has no
award-description text, so its A–J labels are *code-only artifacts* and appear **only** in the
diagnostic crosswalk (`segment_crosswalk.csv`, every Arm-A cell `code_only`/`low`/`suppressed`).
Tiny Arm-B slices (`n_positive<10` or `n_families<30`: segments A, E, F, I) are likewise flagged
`suppressed=yes` and are not interpreted.

**Arm B per-mission-segment (model = clock radar; the strong `b_ldo_runrate` baseline shown by
PR-AUC). Subordinate breadth cohort — corroborates direction, does not drive the verdict:**

| Seg (mission) | families | pos | model P / R | lead | PR-AUC model / ldo+rr | basis/conf |
|---|---|---|---|---|---|---|
| B unmanned-maritime | 31 | 67 | 0.67 / 0.67 | 18.8 | 0.60 / 0.72 | description / high |
| C mine-countermeasures | 211 | 196 | 0.44 / 0.63 | 23.8 | 0.43 / 0.58 | code_only / low |
| D NSW / expeditionary | 49 | 103 | **0.71 / 0.73** | 20.3 | 0.69 / 0.78 | description / med |
| G C2 / autonomy software | 350 | 237 | 0.36 / **0.90** | 20.5 | 0.28 / 0.54 | code_only / low |
| H payloads / sensors / EW | 322 | 675 | 0.62 / 0.63 | 21.3 | — / — | code_only / low |
| J traditional shipbuilding | 248 | 583 | 0.69 / 0.69 | 21.6 | 0.65 / 0.85 | description / high |
| U unclassified | 649 | 218 | 0.24 / 0.69 | 24.0 | 0.26 / 0.41 | none / low |

Reading: the **same recall+lead pattern holds across every mission segment** (recall 0.63–0.90, lead
~19–24 mo), reproducing the Arm-A finding at breadth; precision again rides the base rate and the
`b_ldo_runrate` baseline leads on ranking (PR-AUC, e.g. J 0.85, D 0.78). Description-backed segments
(B, D, J) are the trustworthy mission reads; code-only segments (C, G, H) are driven by NAICS/PSC
nets and should be read with the provenance caveat. The widened pull is still **awarding-subtier
Navy**; the customer-based broadening (`navy_funded`/`navy_requirement_owner` via funding office) is
wired but not yet re-pulled (network step).

**Caveats carried into the verdict:**
- *Arm A remains the high-fidelity timing/recall validation cohort; Arm B is the mission-segment
  reframe / breadth cohort.*
- *Arm A A–J mission slices are not interpreted because Arm A lacks description text; splitting 22
  positives across code-only labels would create false precision. Mission-segment conclusions are
  therefore drawn from Arm B, while Arm A supports the high-fidelity award-clock validation.*

## Forward-signal addendum (SAM Data Services archived bulk, FY2023–2025)

The archived Contract Opportunities bulk extracts (posted Oct-2022 … Sep-2025; ~4,800–5,400
maritime notices/yr, ~80% pre-award) recover the historical pre-award notices the public API
hides. `forward_signal.py` joins them to awards by normalized `Sol#`. Findings (in-window maritime
awards, n=276):

- **Award↔notice matching: 2 → 147** (the prior `award_opp_match` was 2/2048).
- **Portal incompleteness ≈ 47%:** only **53%** of in-window awards had *any* synopsized pre-award
  notice — the rest are "dark" (FAR 16.5 orders / OTs that never synopsize), empirically confirming
  the methodology's central caution.
- **The notice fires LATE:** median pre-solicitation lead **2.6 months** (sources-sought/presol
  **4.3 months**) before award — versus the award-side clock's **~22 months**. This *strengthens*
  the core thesis: the ordering-period clock beats the Opportunities portal as an early warning by
  ~18 months; the notice is a late confirmation, not the radar.
- **Recompete forward-signal — wired, gated only by archive years on hand.** The successor IDV is
  matched via its orders' Sol#s. With just FY2023–25 loaded, 13/18 events fall *outside* the notice
  window and 4 are dark; the 1 in-window match (a major-vehicle recompete) had a **Sources Sought
  18.2 months before award** — far longer than the 2.6-mo routine-order median, i.e. big recompetes
  *do* get early public signals. This is purely a data-coverage limit, **not** a method limit:
  `forward_signal.py` auto-ingests any `FY2001…FY2026` archive present, so adding the back-years
  puts all 18 events in-window and yields a full recompete pre-solicitation lead distribution +
  active-notice baseline. (Next data step: the FY2017–FY2026 archives are being localized into the
  in-repo `raw/sam/opportunities_archive/`; re-run `forward_signal.py` once all 10 are in place to
  refresh these numbers across the full window.)

Artifact: `extracted/forward_signal_match.csv` + cached `_notice_sol_index.json` (gitignored). The
multi-GB source CSVs live in the **gitignored** in-repo `raw/sam/opportunities_archive/` (moved off
`~/Downloads`); `forward_signal.py` streams them Sol#-targeted and caches a tiny index, so re-runs
are instant until the file set changes.

## Reproduce

```
cd projects/awards_methodology/research/datasets/saronic_navy_awards/scripts
python3 segment_classify.py       # taxonomy self-test + widened-corpus A-J distribution
python3 phase1_backtest.py        # frozen-date replay w/ negatives -> predictions_asof.csv (+ segment cols)
python3 phase1_metrics.py         # headline metrics (A=clock seg, B=segment_primary) -> metrics_by_segment.csv
                                  #   + segment_crosswalk.csv (both-axis diagnostic, provenance, suppression)
python3 phase1_leakage_tests.py   # negative controls (must ALL PASS)
python3 phase1_label_outcomes.py  # SAM pull + outcome taxonomy -> outcome_labels.csv
python3 phase1_review.py          # fp_review/fn_review/semantic_match_metrics
```
Outputs land in `…/extracted/` (gitignored); these scripts + this verdict are tracked.
Deferred / data-blocked (tested): historical pre-solicitation lead, active-notice baseline,
widened-corpus taxonomy, migration/split labels, decile calibration on Arm A.
