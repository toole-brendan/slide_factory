---
title: Recompete Opportunity Methodology
subtitle: Finding market-entry windows through federal awards analysis
status: Working draft — proposed methodology with known gaps flagged
audience: Procurement-literate reviewers (terms of art used without expansion; see Appendix A)
---

# Recompete Opportunity Methodology

**What this is.** A method for using the federal award and opportunity record to
find *where, when, and how* an existing requirement is likely to be re-acquired,
and whether a given firm can reach the resulting action. It consolidates the
conceptual model in `research/wiki/05-recompetes-and-opportunity-intelligence.md`
with the empirical calibration produced under
`saronic_specific_awards_data/research/contracts/` (the recompete screen, the
award↔opportunity match, and the Phase-2 historical-replay backtest).

**What this is not.** It is not a database query. No federal system publishes a
field that says "this requirement will be recompeted on this date." A recompete is
an **inferred** acquisition event, assembled from the award history and joined to
forward demand signals. The honest output is a set of **probabilities and dated
ranges**, never a certainty.

---

## 1. First principles

Four disciplines govern the whole method. They are the difference between a
defensible read and a confident-but-wrong "opportunity score."

1. **A recompete is an inferred event, not a data element.** It is reconstructed,
   not retrieved. Every downstream number inherits that uncertainty.

2. **Score two quantities separately, never as one number.**
   - **Event probability** — the likelihood the requirement is bought again at
     all, on some timeline.
   - **Addressability** — the likelihood a given firm can reach and win the
     resulting action.
   A near-certain recompete on a vehicle the firm cannot access is not an
   opportunity for that firm; a perfectly addressable requirement that will never
   be re-bought is not an opportunity at all.

3. **Reason in dated bands across several period-of-performance dates, not from a
   single expiration.** A requirement does not have one end date. It has a
   *current completion date*, an *ultimate completion date*, option-exercise
   decision points, and — for indefinite-delivery vehicles — a *last date to
   order* (the ordering-period end date), which is distinct from all of the above.

4. **Match requirements semantically, not by identifier.** A successor commonly
   carries a new PIID, a different contracting office, and even a different PSC or
   NAICS. Identifier joins miss it; requirement-level matching (scope, place of
   performance, end user, incumbent) catches it.

---

## 2. The opportunity unit — what actually gets re-bought

The candidate events are not equivalent and do not share a period of performance
or a competitive posture. Identify the unit first.

| Opportunity unit | What the next event is | How it surfaces in data |
|---|---|---|
| Definitive contract | A follow-on contract for the same requirement | New contract PIID, usually preceded by a solicitation |
| Task / delivery order | A follow-on order under the same or a different IDV | New order PIID referencing a parent IDV |
| Parent IDV (IDIQ / MAC / GWAC / FSS) | Replacement of the ordering vehicle itself | New IDV PIID; existing orders may run on for years |
| IDIQ on-ramp / new pool | Added holder seats on an existing vehicle | A special notice or amendment, not a fresh competition |
| Subcontract package | A prime re-sources scope one tier down | Not in prime-award data; only via FFATA first-tier reporting |
| Bridge action | A short sole-source continuation of the incumbent | A sole-source modification or short interim award |
| OT production follow-on | A production action after a prototype Other Transaction | May never appear as an open competition |
| SBIR / STTR Phase III | A continuation of earlier SBIR/STTR work | Often sole-source, small public footprint |

An expiring task order does **not** imply that its parent IDV is expiring; a parent
IDV may be recompeted while orders beneath it perform for years. Single-award and
multiple-award IDVs imply different events: under a multiple-award IDV, the
addressable event is a task/delivery order won under fair opportunity (FAR
16.505) — open only to holders; replacing the vehicle is a separate, later event.

---

## 3. The award family and the fields that carry the signal

A single transaction says little. The signal lives in the **award family** — the
records that together describe one requirement over time, grouped by requirement
rather than by identifier. Retain the fields that carry recurrence, competitive
posture, and timing:

- **PIID; referenced IDV PIID** — separate an order from its parent vehicle.
- **Modification number and reason** — distinguish option exercises, incremental
  funding, period extensions, novations, and closeout.
- **Recipient UEI and CAGE; ultimate parent** — normalize subsidiaries, novations,
  and name changes (the corporate-identity trap).
- **Awarding office; funding office** — identify the buyer separately from the
  appropriation's owner.
- **PSC, NAICS, requirement description, place of performance** — reconstruct the
  requirement for semantic matching.
- **Extent competed; number of offers; type of set-aside; solicitation
  procedures; fair-opportunity exception** — estimate the future competitive
  posture and the access gate.
- **Solicitation identifier** — the join key between the award record and the
  opportunity-notice record.
- **Last date to order** (IDVs); **current completion date**; **ultimate
  completion date**; **option-exercise dates** — the several period-of-performance
  dates the entry window is read from.
- **Action obligation; total obligations** — measure realized, recurring demand.
- **Base-and-exercised value; base-and-all-options value / ceiling** — gauge
  contractual scale (capacity, *not* spending; never sum ceilings).
- **Treasury Account Symbol / federal account** — tie the award to its
  appropriation and period of availability (Section 5).

---

## 4. The entry window — precise definition

The phrase "how long is the window open" conflates several dates. Separating them
*is* the method. The entry window for a new participant has two edges and a
back-stop, each anchored on a different, individually knowable date.

```
            acquisition lead time (PALT + pre-solicitation phase)
      ┌──────────────────────────────────────────────┐
      │                                                │
  ────┼───────────────┬──────────────┬────────────────┼──────────────►  time
   sources-sought   presol/      solicitation       SUCCESSOR        incumbent
   / market         draft RFP    released           AWARD            last date
   research         (shaping)    (competition open) (window closes;  to order /
   (window opens)                                   re-locks 1 cycle) ultimate
                                                                      completion
```

- **Opening edge — acquisition lead time.** The buying activity begins the
  re-acquisition *ahead* of the incumbent instrument's relevant end date. The
  earliest actionable public signal is a **sources sought / request for
  information**; the competition opens at **solicitation** issuance. The interval
  from solicitation issuance to award is **Procurement Administrative Lead Time
  (PALT)**; the full front end adds the pre-solicitation (market research and
  shaping) phase ahead of that.

- **Closing edge — the successor award.** When the successor is awarded, the
  direct route is closed for one acquisition cycle (base period plus exercised
  option periods, or the next multiyear-procurement block boundary).

- **Back-stop — appropriation period of availability for obligation.** The
  appropriation funding the action ("color of money") must be obligated within its
  statutory period of availability. This bounds the *latest* an award can be made
  with a given year's funds and is read from the Treasury Account Symbol.

**The window a new participant cares about is the interval from the opening edge to
the closing edge** — roughly `[incumbent relevant end − acquisition lead time]` to
`[successor award]`. After the closing edge it is locked for one cycle.

A critical consequence, and the most common error this guards against: **the
incumbent instrument's end date is not the recompete date.** An on-time successor
is awarded *before* the incumbent's last date to order or ultimate completion; a
late one is awarded *after*, via a bridge action. Treating "this ends in FY-X →
opportunity in FY-X" as the window is wrong in both directions.

---

## 5. What determines the window's length

The opening-edge-to-closing-edge length is set by a small number of determinants,
in roughly this priority:

1. **Instrument and award structure.** A definitive-contract recompete runs a full
   new competition. A multiple-award IDV opens at the task/delivery-order level
   continuously *for holders*, but the vehicle itself opens only at recompete or at
   a defined on-ramp. A single-award IDV opens only at vehicle recompete. A
   multiyear procurement (production block buy) opens only at block boundaries. An
   OT or SBIR Phase III follow-on may present no open competition at all.

2. **Dollar value and complexity → acquisition lead time.** Larger, cleared, or
   integration-heavy requirements are planned earlier and take longer to award
   (longer PALT and a longer pre-solicitation phase).

3. **Competition strategy.** Full-and-open with formal source selection (and the
   attendant bid-protest exposure) lengthens the interval; a Justification and
   Approval to limit competition, or a bridge action, shortens and closes it.

4. **Appropriation period of availability for obligation** (the back-stop). The
   funding appropriation's availability bounds the latest obligation date — e.g.,
   the recompete cannot slip indefinitely if the funds expire.

5. **Option structure (FAR 17.2).** Base plus option periods set the cadence:
   each option-exercise decision is a potential early opening (non-exercise) or a
   deferral (exercise). The ultimate completion date, not the current completion
   date, dates the latest direct opening for a definitive instrument.

6. **Bid protest exposure.** A GAO protest triggers a CICA automatic stay and a
   statutory decision interval, extending the time to a final, locked award.

> External published benchmarks for items 2 and 6 (PALT distributions by dollar
> band; protest-stay durations; statutory ordering-period and option limits under
> FAR 16.504/16.505, 10 U.S.C. 3403, and FAR 17.204) are being gathered
> separately; see "Current unknowns."

---

## 6. Forward demand signals

The award record is retrospective. It must be paired with forward signals from the
opportunity-notice record (SAM.gov Contract Opportunities) and the budget.

| Signal | What it implies about the next event |
|---|---|
| Sources sought / RFI | The market is being surveyed; a buy is forming (earliest actionable signal) |
| Presolicitation / draft solicitation | A solicitation is imminent; shaping (FAR 15.201) is still possible |
| Solicitation / combined synopsis–solicitation | The competition is open now |
| Intent to bundle | Scope is being consolidated across requirements |
| J&A / fair-opportunity exception / intent to sole-source | Competition will be limited or absent |
| Acquisition forecast / budget justification (P-1, R-1, PE/BLI) | The requirement persists in plans (non-binding, FAR 5.404) |
| Industry day | Early shaping; the requirement is live |
| Bridge action | The intended competition is running late |

Two cautions: SAM.gov Contract Opportunities returns only the **latest active
version** of a notice, so an audit trail requires snapshotting notices over time;
and acquisition forecasts and budget justifications are **non-binding** planning
estimates, useful as persistence clues, not commitments.

---

## 7. Scoring — event probability × addressability

Score the two quantities independently, then read them as a 2×2, not a single
rank. Weights below are an operating heuristic, **not** a calibrated scheme (see
"Likely weak spots").

| Event-probability factor | Addressability factor |
|---|---|
| Proximity to a decision point (option / completion / last date to order) | Vehicle access or a credible prime partner |
| Recurring obligation pattern | Technical and mission fit |
| Requirement persists in budget or forecast | Readiness to perform (security, clearance, delivery posture) |
| Active procurement signals present | Relevant past performance |
| Likelihood of competition vs likely sole-source | Transition and data-rights barriers; set-aside alignment |

```
                       ADDRESSABILITY (can the firm capture it?)
                         low                         high
              ┌──────────────────────────┬──────────────────────────┐
   EVENT high │ team with / route through │ pursue capture directly   │
   PROB.      │ a holder or prime         │                           │
              ├──────────────────────────┼──────────────────────────┤
        low   │ monitor                   │ shape the requirement     │
              │                           │ early (FAR 15.201)        │
              └──────────────────────────┴──────────────────────────┘
```

---

## 8. Data-availability discipline (no look-ahead)

A reproducible screen can only act on data that was **public at the time**. Two
points govern this.

- **The last date to order is a base-award data element.** For an indefinite-
  delivery vehicle, the ordering-period end date is populated on the base award
  (modification 0) and is therefore knowable from the award's signed date forward —
  *not* added at a later milestone. (Measured: 20/20 vehicles in the backtest
  carried it at modification 0; none first appeared on a later modification.)

- **It can be extended outward by later modifications**, and DoD records are
  released on a delay. The value seen at award is the *then-current* ordering-period
  end; exercised option ordering periods or extensions push it outward (measured:
  4/20 extended — two DoD IDIQs once each, two FSS Schedules repeatedly, five years
  at a time). And the public feed lags the signed date — roughly 90 days for DoD,
  with classified actions omitted entirely. So "knowable from award day" means
  "from award day plus the reporting lag," and the value is a **floor that can
  drift later**, never earlier.

**Consequence for any lead-time measurement:** anchor leads on the date a datum
became *public* (the signed date of the action that established it, plus reporting
lag), and treat option-bearing or Schedule-type instruments as floor dates likely
to drift. Anchoring on a future end date with perfect foresight overstates how
early the event was actually anticipable.

---

## 9. Empirical calibration to date

Measured on a focused maritime-IDIQ segment (NAICS 336611 / 336612) under
`saronic_specific_awards_data/research/contracts/`. **Treat as segment-specific and
small-sample**; see "Likely weak spots."

| Measurement | Result | Basis |
|---|---|---|
| **Ordering-period length** (last date to order − award start) | median **~53 months**; small-craft IDVs ~49mo, larger procurement IDVs ~84mo | 26 vehicles with a usable start date |
| **Successor vs incumbent end** | successor awarded a median **~24 months *before*** the predecessor's last date to order (8 of 11 re-buys ran in parallel with the incumbent) | 11 builder chains, historical replay |
| **Point-in-time anticipability** (from data public at the freeze) | **9/11** anticipable 6 months before the successor award; **5/11** at 12–18 months | same, no look-ahead |
| **Visibility lead** (successor award − date last date to order first recorded) | median **~48 months** off the base value; **~35 months** off the final value | last-date-to-order recording history |
| **Last date to order availability** | **20/20** present at base award (mod 0); **4/20** later extended outward | FPDS action timelines |
| **PALT** (solicitation → award) | **not measurable** from current pulls | one-year Opportunities window |
| **Front-end lead** (sources sought → solicitation) | **not measurable** (n=1) | differing solicitation numbers |

**Headline read.** In this segment the successor is competed and awarded roughly
two years *before* the incumbent vehicle's ordering period ends — so a screen that
keys on incumbent end dates alone fires ~2 years late. The ordering-period end is
public years ahead (a base-award element), so visibility is rarely the binding
constraint; what bounds usable lead is (a) how far ahead one chooses to look and
(b) outward drift from option/extension modifications.

---

## 10. Current unknowns

Explicit gaps where we do not yet have a defensible number or rule:

1. **PALT distributions** for the relevant segments — unmeasured internally (the
   SAM.gov Contract Opportunities pull spans a single 12 months, which truncates any
   procurement longer than the window). Pending external published benchmarks and/or
   a multi-year Opportunities pull.
2. **Front-end (pre-solicitation) lead** — the sources-sought→solicitation interval
   is unmeasured (sources sought and the eventual solicitation usually carry
   different solicitation numbers; no reliable join without semantic matching).
3. **Outward-drift base rate** — the probability and magnitude by which a last date
   to order is extended after award, by instrument type. Only 4/20 observed; too few
   to estimate a rate, and FSS Schedules clearly behave differently from definitive
   DoD IDIQs.
4. **Vehicle-substitution rate** — how often a recompete surfaces as an order under a
   *different* IDV (no fresh competition appears) versus a standalone solicitation.
   This determines whether the opportunity-notice record even shows the event.
5. **Portal coverage of exempt pathways** — the share of relevant demand flowing
   through OT agreements, consortium channels, and SBIR Phase III follow-ons that
   never synopsize on SAM.gov Contract Opportunities.
6. **Generalization** — whether the maritime-IDIQ "successor precedes incumbent end"
   pattern holds for services, single-award vehicles, and definitive production
   contracts. Likely segment-dependent.
7. **Public-release lag distribution** — assumed ~90 days for DoD; not measured, and
   it directly shifts every visibility-anchored lead.

---

## 11. Likely weak spots in the proposed methodology

Where the method is most likely to be wrong, and why:

1. **Anchoring on the last date to order when it drifts outward.** Option ordering
   periods and extensions move it later (especially FSS Schedules, which ratchet in
   five-year option increments). A recompete flagged off the early value can arrive
   far later than expected — a **timing false positive**, not a missing-data error.
2. **Semantic requirement matching is fuzzy and not yet automated.** The predecessor↔
   successor link rests on scope/office/place-of-performance/incumbent judgment.
   Identifier-based matching fails outright (requirement-identity trap), and the
   backtest's chains were hand-validated on a small set.
3. **Single-award vs multiple-award conflation.** The addressable event differs (a
   held task/delivery order vs a whole-vehicle recompete). Treating them alike
   mis-scores both probability and addressability.
4. **The bridge trap.** A sole-source bridge to the incumbent reads as "locked-up
   work" when in fact the recompete is *late, not absent* — suppressing a live
   opportunity.
5. **Thin forward signals.** The opportunity-notice join is a single-year, latest-
   version-only window with no historical snapshots, so the demand-signal half of the
   method is currently weak and not auditable over time.
6. **Uncalibrated scoring.** The event-probability and addressability weights are
   heuristic. No outcome data has been used to fit them; the 2×2 is a frame, not a
   validated model.
7. **Small, segment-specific calibration.** Every internal number above comes from
   maritime IDVs (NAICS 336611/336612), n in the tens. Generalizing without
   re-measuring is unwarranted.
8. **Source-data limits.** DoD reporting delay, omission of classified actions, and
   first-tier-only subaward reporting mean absence of data is not absence of activity
   (the visibility trap).
9. **Conflating appropriation availability with period of performance.** The
   appropriation's period of availability for obligation and the contract's period of
   performance are different things; using one for the other over- or under-states the
   window. Keep the Treasury Account Symbol read separate from the completion dates.

---

## 12. Validation status and next steps

- **Done.** Historical-replay backtest on 11 builder chains (point-in-time, no
  look-ahead); ordering-period-length distribution; last-date-to-order availability
  and drift check; award↔opportunity structural-coverage match.
- **Next, internal.** Re-cut lead time as a *visibility lead* anchored on the public
  release date (replacing any perfect-foresight measure); add an **extension-watch
  flag** for instruments whose ordering period has moved or is structurally prone to
  drift (Schedules, unexercised option ordering periods); widen the calibration
  beyond maritime IDVs.
- **Next, external.** Published PALT, ordering-period/option statutory limits, and
  bid-protest-stay benchmarks to fill the unknowns the internal pulls cannot reach.

---

## Appendix A — Terminology discipline

This document uses procurement terms of art exactly. In particular it does **not**
use the informal word "clock"; the precise terms are:

- **Last date to order** — the ordering-period end date of an indefinite-delivery
  vehicle; the deadline for placing new orders. Child orders may perform past it.
- **Current completion date** — the end of presently-exercised performance.
- **Ultimate completion date** — the end if every priced option is exercised.
- **Period of performance** — the start-to-end performance window of an award/order.
- **Option period (FAR 17.2)** — a priced, unilaterally exercisable extension.
- **Acquisition lead time / PALT** — pre-solicitation phase plus Procurement
  Administrative Lead Time (solicitation issuance → award).
- **Period of availability for obligation** — the statutory window during which an
  appropriation may be obligated ("color of money"), read from the Treasury Account
  Symbol — distinct from any period of performance.

Other terms: IDV (indefinite-delivery vehicle), IDIQ / IDC, MAC, GWAC, FSS
(Federal Supply Schedule), BPA, BOA, OT (Other Transaction); definitive contract;
extent competed; fair opportunity (FAR 16.505); set-aside; single- / multiple-award;
Justification and Approval (J&A); bridge action; novation; sources sought,
presolicitation, combined synopsis/solicitation, special notice (SAM.gov Contract
Opportunities notice types).

## Appendix B — Source systems and roles

| System | Role in the method | Key fields |
|---|---|---|
| SAM.gov Contract Awards | Modern base pull — primes, IDVs, orders, structure, dates | PIID, referenced IDV PIID, last date to order, completion dates, extent competed, solicitation identifier |
| FPDS (Atom feed) | Per-action history and legacy lineage (retiring FY2026) | Action-level signed dates, modification numbers, last date to order per action |
| SAM.gov Contract Opportunities | Forward demand signals | Notice type, posted date, solicitation number |
| USAspending | FY obligation and Treasury Account Symbol bridge | Federal action obligation, TAS, period-of-performance dates |
| FFATA / FSRS first-tier reporting | The visible supplier layer (subcontract unit) | Subawardee UEI, subaward amount/date, prime PIID — first-tier only, lagged |
| President's Budget / justification (P-1, R-1, PE/BLI) | Forward funding persistence (non-binding) | Account, program element / budget line item, color of money |

---

*Cross-references:* `research/wiki/05-recompetes-and-opportunity-intelligence.md`
(conceptual model and false-positive traps);
`saronic_specific_awards_data/research/contracts/scripts/backtest_recompete.py`
and `extracted/backtest_results.csv` (the historical-replay backtest);
`extracted/recompete_radar.csv` (the screening output).
