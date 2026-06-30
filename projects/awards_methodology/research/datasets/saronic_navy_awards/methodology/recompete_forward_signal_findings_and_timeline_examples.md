# Forward-signal over the local SAM archive (FY2017–FY2026): findings, methodology advice, and timeline-slide examples

**Date:** 2026-06-28 (rev. 3 — recompete join now matches on the **real solicitation number** instead of
the contract PIID, which corrected the "dark" recompete counts and revealed an IDIQ-vs-MYP segment split;
added an active-notice baseline. Rev. 2 fixed metric labels, denominators, paired deltas, and dark phrasing.)
**Scope:** `forward_signal.py` run against the in-repo archive set
(`raw/sam/opportunities_archive/FY2017…FY2026_archived_opportunities.csv`, 10 files, ~10 GB, gitignored).
This is the **full local archive window, FY2017–FY2026** — ten local files, *not* the entire SAM/FBO
historical universe (back to ~2001).
**Supersedes** the FY2023–25-only "Forward-signal addendum" in `recompete_backtest_phase1_verdict.md`
(left unchanged).
**Reproduce:** `cd …/saronic_navy_awards && python3 scripts/forward_signal.py` (~75 s; regenerates
`extracted/forward_signal_match.csv`, `extracted/forward_signal_active_notice_baseline.csv`, + cache).

The "forward signal" is the SAM.gov Contract **Opportunities** record — the pre-award notices (Sources
Sought, Presolicitation, Solicitation, Combined Synopsis) that precede an award. The archived bulk
extracts recover historical notices the public API hides. We join them to awards by **normalized
solicitation number** and ask: how far ahead of the award does the portal fire, how often is it dark, and
how does that compare to the award-side ordering-period clock the methodology uses as its radar?

> **Conclusion (refined by the join fix):** the archived Opportunities files recover a real historical
> notice layer and materially improve the evidence base; they do **not** overturn the methodology. But the
> calibrated join shows two things the buggy version hid: (1) the portal recovers **far more** recompetes
> than first reported — only **2 of 15** in-window recompetes are truly dark, not 7; and (2) the clock's
> edge is **segment-dependent** — for ordering-period **IDIQ** recompetes the clock leads the portal, but
> for **multiyear (MYP)** blocks the block-completion clock points years past the actual recompete, so the
> portal's Presolicitation is the better signal. Net: the clock is the primary radar **for IDIQ
> recompetes**; for MYP it is the wrong instrument and the portal/budget cadence leads.

A note on the join: matching is by normalized solicitation number. **Rev. 3 fixed a real bug** — the
recompete matcher keyed on the successor *contract PIID*, which never matches a notice, so every DDG
recompete was silently "dark." It now resolves each successor's real solicitation number (maritime IDV
orders via `_detail_index.json`; DDG via `ddg_myp_recompete_provenance.csv`). A "no match" now means a
*resolved solicitation with no notice in the archive* (true dark), distinct from *no solicitation
resolvable* (unresolved). The award-row join (§A) still can't prove "no notice ever existed," only "no
matched notice via the join."

---

## A. Results — full local archive window, FY2017–FY2026

Notice archive span **2016-10-01 … 2026-06-27**.

### A.1 Award-side coverage (unchanged by the join fix — independent analysis)

| Metric | FY2023–25 slice (old) | **FY2017–26 local archive (new)** |
|---|---|---|
| In-window maritime award **rows** | 276 | **856** |
| Award↔notice **unique Sol# keys** matched | 2 (public API) → 147 | **466** |
| In-window award rows with ≥1 matched notice | 53% | **69%** (594 / 856) |
| In-window rows with **no matched notice via join** | 47% | **31%** (262 / 856) |
| Median **earliest-matched-notice → award** lead | 2.6 mo | **4.6 mo** (n=594) |
| Median **early-notice → award** lead (SS/Presol only) | 4.3 mo | **9.8 mo** (n=371) |

**Denominators (count different things):** **466** = unique normalized *award* Sol# keys matched ≥1
notice; **594** = in-window award *rows* with a matched notice; **856** = in-window award *rows*; **262**
have no matched notice (31% "dark via join"); **254** are out-of-window (signed before notice coverage).

**Metric-label correction (carried from rev. 2):** the script's `preaward_lead_months` is
**earliest_matched_SAM_notice_to_award_lead** (earliest of {SS, Presol, Solicitation, Combined Synopsis}
→ award), *not* "pre-solicitation lead"; `early_lead_months` is the same restricted to {SS, Presol}. Two
front-end leads we still do **not** measure: `solicitation_to_award_lead` (PALT proxy) and
`sources_sought_to_solicitation_front_end_lead`.

### A.2 Recompete-successor signal — corrected by the real-Sol# join

18 Arm-A recompete events; the wider archive puts **15 in-window**. With the calibrated join:

| Outcome | buggy PIID join (old) | **real-Sol# join (new)** |
|---|---|---|
| Matched a pre-award notice | 8 | **12** |
| Truly dark (sol resolved, no notice) | 7 | **2** |
| Unresolved (no solicitation #) | 0 | **1** |
| Out-of-window | 3 | 3 |

Median matched recompete notice-lead **9.7 mo** (n=12). The four newly-matched events are the **DDG MYP**
contracts the PIID join missed: Bath Iron Works + Huntington Ingalls **FY18-22 MYP** had a
**Presolicitation 9.4 mo** before award (sol `N0002418R2302`); the **FY23-27 MYP** pair had a
**Presolicitation 14.3 mo** out (sol `N0002422R2302`). The two genuinely dark recompetes are a
GSA-schedule order and a NAVSUP order (solicitation resolved, no notice). The one unresolved is a Johns
Hopkins APL action (no competitive solicitation to resolve).

### A.3 "Clock beats portal" — now with the segment split

Paired **method-lead − notice-lead** on the matched recompetes (n=11 with an evaluable method lead):

| Cohort | n | paired median | clock leads | reading |
|---|---|---|---|---|
| **maritime IDIQ** | 7 | **+2.4 mo** | 5 / 7 | ordering-period clock leads the portal (modestly) |
| **DDG MYP** | 4 | **−7.4 mo** | 1 / 4 | block-completion clock **lags** the portal — wrong radar for MYP |
| all matched | 11 | +2.2 mo | 6 / 11 | dominated by IDIQ; MYP drags the tail |

Distribution-level (different populations, not paired): clock median first-alert lead **~22 mo** (Arm-A
maritime cohort, verdict) vs portal **4.6 mo** notice→award. The ~17-mo gap is a population comparison;
the paired per-event medians above are the conservative, apples-to-apples figures — and they say the
clock's IDIQ edge is real but small, and its MYP "edge" is negative.

### A.4 Active-notice baseline (portal conversion / precision proxy)

New output `forward_signal_active_notice_baseline.csv`. Population = **Navy-maritime notices** in the
archive (`Sub-Tier = DEPT OF THE NAVY` AND NAICS 336611/336612 or PSC 1905/1925/1940; mirrors the
award-side taxonomy, easily widened):

- **7,507** Navy-maritime solicitations seen; **5,576** have a pre-award notice (Presolicitation 1,643;
  Sources Sought 1,579; Solicitation 1,298; Combined Synopsis 1,056).
- **Conversion to a same-Sol# Award Notice: 656 / 5,576 = 11%** (median notice→award lead **2.8 mo**;
  p25 0.7, p75 5.2, n=645).
- Cross-check: 258 of these sols are in our 745-award maritime corpus.

**Read this carefully — it is a lower bound, not the portal's precision.** "Conversion" here means an
*Award Notice posted under the same Sol#*. It undercounts true conversion for two reasons: (a) award-side
darkness — many real awards never post an Award Notice (the same gap the methodology flags); and (b) the
**same Sol#-drift** the recompete join just exposed — an award notice can carry a different solicitation
number than its pre-award notice. So 11% is the floor; the real precision needs a drift-robust notice→award
join (next step). The solid, defensible facts here are the **volume** (5,576 Navy-maritime pre-award
notices/decade, by type) and the **lead** (median 2.8 mo — last-minute, consistent with §A.1).

---

## B. Methodology — improve, or leave alone?

Grounded in `recompete_opportunity_methodology.md` (§10 unknowns, §11 weak spots, §12 next steps),
`recompete_opportunity_playbook.md`, and `recompete_backtest_phase1_verdict.md`.

### Keep — validated

- **Clock-as-primary-radar *for IDIQ ordering-period recompetes*.** Recall 0.83, ~22-mo lead (verdict);
  paired, it leads the portal 5/7 in maritime IDIQ.
- **"Notice = confirmation, not warning"** for IDIQ. Median portal lead 4.6 mo; the playbook's existing
  stance holds.
- **Two-axis design (event-probability × addressability).** Only 4/22 flagged events are open recompetes
  (verdict) — unchanged.

### Change — the segment split is now evidence, not a hypothesis

The methodology's §11 already suspected generalization is "likely segment-dependent." The calibrated join
makes it concrete: **for multiyear (MYP) blocks the last-date-to-order / block-completion clock is the
wrong radar** — it points years past the actual recompete (DDG MYP paired median −7.4 mo; the FY23-27
block clock sat ~5 years past the award). For MYP, lead with the **calendar cadence + budget lines +
the Presolicitation** (which fired 9–14 mo ahead here), not the completion clock. Add an explicit
**segment gate**: apply the ordering-period clock to IDIQ/MAC vehicles; for MYP/production blocks switch
to a cadence/budget radar.

### Now enabled — the archive resolves a stated weak spot (use as confirmation, not radar)

§11's "thin forward signals … not auditable over time" is removed for the FY2017–26 local window: an
auditable notice history exists, the recompete join now spans 15/18 events with trustworthy matched/dark
labels, and the active-notice baseline gives a (lower-bound) conversion denominator. Replace the §11
language with: *"Historical SAM notice coverage is now auditable for the FY2017–26 local archive window,
but the notice layer remains late; use it as confirmation and timing evidence, and — for MYP — as an
earlier signal than the completion clock."*

### Improve — prioritized

1. **Calibrate the notice↔award join (Sol#-drift-robust).** The recompete fix (PIID→real Sol#) lifted
   matched recompetes 8→12 and cut "dark" 7→2; the *same* drift depresses the active-notice conversion
   (11% floor). A robust join (normalize + alias award↔solicitation numbers) is the single highest-value
   next step; it turns the conversion proxy into a real portal-precision estimate.
2. **Segment-gate the radar** (IDIQ clock vs MYP cadence), per the split above.
3. **Quantify dark by segment** — 31% award-row dark is a maritime average; recompute per segment once the
   join is calibrated; feed as an addressability prior.
4. **Widen calibration beyond maritime IDVs** (all internal n is NAICS 336611/336612, tens of events).

### Next forward-signal task — finish the active-notice baseline

Make conversion precision real: with a drift-robust join, of all Navy-maritime SS/Presol/Solicitation
notices, what fraction award (by segment, on what lead)? The 11% floor + 2.8-mo lead are the starting
point; the verdict deferred exactly this.

### Don't change

- **Do not promote SAM Opportunities to an early-warning layer for IDIQ.** It is late (4.6 mo) and
  incomplete (31% award-row dark). Keep it as confirmation there. (MYP is the exception — see "Change".)

---

## C. Award-timeline slide examples

Each example is a real incumbent → successor recompete with three dated events on one axis: **▲ T1** the
methodology flags it (first month the clock enters the 36-mo horizon ≈ incumbent clock − 36 mo;
method-lead = award − T1); **◆ T2** the earliest matched pre-award notice posts (notice-lead = award − T2);
**● T3** award signed. Values from this run (`backtest_v2_events.csv`; the `forward_signal.py` recompete
block; builders from the detail index / DDG provenance).

### C.1 Maritime IDIQ — the clock generally leads (the clean story)

| # | Builder (small combatant craft) | ▲ T1 | ◆ T2 notice (type) | ● T3 award | Method lead | Notice lead | Δ (m−n) |
|---|---|---|---|---|---|---|---|
| 1 (clean hero) | **Metalcraft Marine** | 2019-10 | 2021-10 (Solicitation) | 2022-03-09 | 29.4 mo | 5.2 mo | **+24.2** |
| 2 | **Metal Shark / Gravois**¹ | 2020-09 | 2022-11 (Sources Sought) | 2024-05-16 | 43.6 mo | 18.2 mo | **+25.4** |
| 3 | **Willard Marine** | 2015-09 | 2016-10 (Presolicitation) | 2017-04-03 | 18.7 mo | 5.7 mo | **+13.0** |
| 4 (near-tie) | **Snow & Company** | 2020-09 | 2020-11 (Sources Sought) | 2021-09-30 | 12.1 mo | 9.7 mo | +2.4 |
| 5 (counter) | **Ribcraft USA** | 2022-08 | 2021-10 (Sources Sought) | 2023-02-09 | 6.0 mo | 16.3 mo | **−10.3** (portal led) |
| 6 (radar miss) | **Silver Ships**² | — (clock 2028) | 2021 (Sources Sought) | 2021-09-30 | −47.4 mo | 9.5 mo | **−56.9** |

¹ Gravois: award landed ~8 mo **after** the predicted clock (a late/bridge recompete), inflating the
43.6-mo method lead. ² Silver Ships: the incumbent clock ran to 2028, so the 2021 recompete arrived before
the radar's horizon opened — the clock would not have flagged it; the portal's Sources Sought was the only
signal.

### C.2 DDG multiyear (MYP) — the clock is the wrong radar (the corrected DDG story)

The first draft wrongly called these "dark." With the real-Sol# join they **all match a notice** — and
they show why the completion clock fails for MYP:

| Program | ◆ notice (type, lead) | ● award | Method lead | Reading |
|---|---|---|---|---|
| **Bath Iron Works DDG-51 FY18-22 MYP** | Presolicitation, **9.4 mo** (sol N0002418R2302, 2 offers) | 2018-09-27 | 21.3 mo | clock led here (+11.9) |
| **DDG-51 FY23-27 MYP** | Presolicitation, **14.3 mo** (sol N0002422R2302) | 2023-08-01 | −30.7 mo | **clock lagged ~3.5 yr; Presol led** |

The block-completion clock points at the *prior* block's end (years past the recompete), so for the
calendar-cadence MYP it is unreliable — across the 4 DDG MYP events the clock leads only 1/4 (median
−7.4 mo). On a slide: this is the "different radar for multiyear programs" example, **not** a dark example.

### How to draw it

One horizontal time axis per award, stacked. Mark ▲ (method flag), ◆ (notice), ● (award); shade the
**method-lead** span in the brand color and the **notice-lead** span in grey. Recommended three-up: one
clean IDIQ leader (Metalcraft), the IDIQ counterexample (Ribcraft), and a DDG MYP (FY23-27) where the
Presol leads — so the slide carries the real, honest thesis instead of a single cherry-pick.

```
  Metalcraft Marine — IDIQ small-craft recompete      (clock leads ~24 mo)
  2019-10 ▲──────────── method radar (29.4 mo) ───────────────● 2022-03  award
                                  2021-10 ◆── Solicitation (5.2 mo) ─┘

  DDG-51 FY23-27 multiyear (MYP)                       (clock is WRONG here; Presol leads)
                              2022-06 ◆──── Presolicitation (14.3 mo) ───────● 2023-08  award
   completion-clock first-alert would be ~2026 ▲ (after the award) ── clock lagged ~3.5 yr
```

---

## What this does and does not establish

**Supported by the numbers:**
1. The archived Opportunities files materially improve historical notice coverage.
2. The earlier 47% dark estimate was too pessimistic; ~31% (award-row, join-based) is the better maritime
   figure. For *recompetes specifically*, the calibrated join shows only **2 of 15 in-window are truly
   dark** (was 7) — the portal recovers most recompetes.
3. The clock's advantage is **segment-dependent**: it leads the portal for IDIQ ordering-period recompetes
   (5/7, +2.4-mo median) but **lags** for MYP blocks (1/4, −7.4-mo median).
4. Notices fire late (median 4.6-mo award-row; 2.8-mo active-notice baseline) — last-minute is the norm.
5. There are ~5,576 Navy-maritime pre-award notices/decade; ≥11% convert to a same-Sol# award notice.

**Not yet established (do not claim):**
1. The portal's true precision — 11% conversion is a lower bound (award-notice sparsity + Sol# drift); a
   drift-robust notice→award join is required.
2. True "no notice existed" for the 2 dark recompetes — only "solicitation resolved, no notice in archive."
3. Generalized dark/lead rates outside the maritime / small-craft + DDG corpus.
4. True sources-sought→solicitation front-end lead (not computed).
5. Addressability — still needs separate scoring.

---

*Artifacts (gitignored): `extracted/forward_signal_match.csv`,
`extracted/forward_signal_active_notice_baseline.csv`, `extracted/_notice_sol_index.json` (cache),
`extracted/backtest_v2_events.csv`. Source archives in `raw/sam/opportunities_archive/`. DDG provenance:
`…/ddg51_recompete_cadence/extracted/ddg_myp_recompete_provenance.csv`.*
