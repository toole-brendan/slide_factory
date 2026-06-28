---
title: Recompete Opportunity Playbook
subtitle: Identifying market-entry opportunities through federal awards analysis — definitive contracts, task/delivery orders, and parent IDIQ/MAC/GWAC vehicles
status: Consolidated working methodology
audience: Procurement-literate reviewers (terms of art used without expansion; see Appendix A)
scope: Three award types only — standalone definitive contracts; task/delivery orders; parent IDIQ/MAC/GWAC vehicles
---

# Recompete Opportunity Playbook

**Purpose.** A workable method for using the federal award and opportunity record
to find *where, when, and how* a continuing requirement is likely to be
re-acquired, and whether a firm can reach the resulting action — restricted to the
three instrument types we pursue: **standalone definitive contracts**, **task /
delivery orders**, and **parent IDIQ / MAC / GWAC vehicles**.

**What it consolidates.** This document merges four working inputs into one:
(1) the inferred-event model and empirical calibration from
`recompete_opportunity_methodology.md` and the backtest under
`saronic_specific_awards_data/research/contracts/`; (2) the
requirement/award/budget three-layer model and budget-alignment confidence scale;
(3) the three-windows timing decomposition and the incumbent-retention authorities;
(4) the published PALT, protest, and statutory-length benchmarks.

**What it is not.** It is not a database query. No federal system publishes a field
that says "this requirement will be recompeted on this date." A recompete is an
**inferred acquisition event**, assembled from the award history and joined to
forward demand signals. The honest output is **probabilities and dated ranges**,
never a certainty.

---

## 1. First principles

1. **A recompete is an inferred event, not a data element.** It is reconstructed,
   not retrieved. Every downstream number inherits that uncertainty.

2. **Score two quantities separately, never as one number.**
   - **Event probability** — will the requirement be bought again, on some timeline?
   - **Addressability** — can a given firm reach and win the resulting action?
   A near-certain recompete on a vehicle a firm cannot access is not an opportunity
   for that firm; a perfectly addressable requirement that will never be re-bought
   is not an opportunity at all.

3. **Reason in dated bands across the several period-of-performance dates, not from
   one expiration.** The governing date differs by instrument (Section 4): a
   definitive contract has a *current completion date* and an *ultimate completion
   date*; an order has its own completion dates and option periods; a parent IDV has
   a *last date to order* (ordering-period end date), distinct from all of the above.

4. **Match requirements semantically, not by identifier.** A successor commonly
   carries a new PIID, a different contracting office, and even a different PSC or
   NAICS. Identifier joins miss it; requirement-level matching (scope, place of
   performance, end user, incumbent) catches it.

---

## 2. The three-layer model

Keep three dimensions separate; do not collapse them into one another.

| Layer | Question it answers | Best evidence |
|---|---|---|
| **Requirement** | What mission work is being bought? | Award/order descriptions, PSC/NAICS, requiring & funding office, place of performance, program/system keywords, solicitation text |
| **Award / vehicle** | How has it been bought historically? | Instrument type, incumbent, options, obligations, parent/child structure, current/ultimate completion, last date to order |
| **Budget / funding** | Is the requirement likely to remain executable? | Treasury Account Symbol / federal account, funding office, obligation trend, R-1/P-1/O-1 justification language, FYDP out-years, acquisition forecasts |

Contract data tells you what was executed. Budget data tells you whether money
appears to persist. Requirement analysis connects the two — even when the next
award has a new PIID, title, vehicle, PSC, or incumbent. **Budget alignment is a
confidence-and-timing signal (Sections 6, 8), not the primary key.** The primary
key is the **requirement family**.

---

## 3. The opportunity unit — by award type

The candidate events are not equivalent and do not share a governing date or a
competitive posture. Identify the unit first.

| Award type | What the next event actually is | Governing date | Direct-entry gate |
|---|---|---|---|
| **Standalone definitive contract** | A follow-on contract for the same requirement | Ultimate completion date (and remaining option periods) | Open competition — a non-incumbent **can bid directly** |
| **Task / delivery order** | A follow-on order under the same parent, an order under a *different* vehicle, a standalone contract, or a bridge | The **order's** current/ultimate completion + order-level options | **Holder-only** (FAR 16.505 fair opportunity) — non-holders cannot reach it directly |
| **Parent IDIQ / MAC / GWAC** | Replacement of the ordering vehicle itself, or an on-ramp / new pool (added holder seats) | **Last date to order** (ordering-period end) + remaining parent option ordering periods + order velocity | The vehicle recompete or on-ramp is the **only** direct-entry point |

Two rules that prevent the most common errors:

- An expiring task order does **not** imply that its parent IDV is expiring; a parent
  IDV may be recompeted while orders beneath it perform for years.
- **Last date to order applies only to parent ordering vehicles.** It does not tell
  you when a definitive contract or a single order ends.

---

## 4. The recompete window — there is no single window

"How long is the window" conflates three distinct intervals. Separating them *is*
the answer.

| Window | What it is | Practical magnitude |
|---|---|---|
| **Market-watch / capture window** | When industry should start tracking, shaping, and teaming | ~9–18 months (simpler buys) to ~18–30 months (complex/cleared/large), as a heuristic — but see the measured correction below |
| **Public notice window** | The legal minimum advertising time (FAR 5.203) | Synopsis ≥15 days before solicitation; ≥30 days response for actions over the simplified acquisition threshold; ≥45 days for many R&D actions |
| **PALT (solicitation → award)** | Procurement Administrative Lead Time — the buy itself once advertised | Highly variable by type, size, competition, and pricing (Section 5) |

PALT begins at solicitation issuance and ends at award; **requirements
development, market research, draft solicitations, and funding sit *outside* it**
(the FY2019 NDAA **§878** framing — *not* §890, which was a separate matter). So
PALT is one layer, never the whole window.

### The assembled front-to-back timeline

Working backward from the incumbent instrument's governing end date and combining
the published PALT benchmarks with our own backtest. **Match the PALT tier to the
segment** — do not apply the >$50M figure to a small buy.

```
  pre-solicitation        solicitation              SUCCESSOR        incumbent
  (sources sought,        issued                    AWARD            last date to
  market research,   ┌─── PALT ───►            ┌── transition ──►    order / ultimate
  draft RFP)         │   (§5)                  │   /protest         completion
  ── months to ──────┤                         │   (+1–3 mo)        │
     ~1–2 yr         │                         │                    │
                     └─────────── successor award lands ~24 months ─┘
                                  BEFORE the incumbent last date to order
                                  (measured, small-boat IDV segment — §9)
```

- **Successor award** lands a median **~24 months before** the incumbent's last
  date to order in the segment we measured (parallel re-buys; Section 9).
- **Solicitation** precedes that award by PALT — roughly **6 months** for an
  all-size Navy IDC, up to **~13 months** for a >$50M Navy IDC.
- ⇒ The competition opens **~26–37 months before** the incumbent's last date to
  order, depending on segment and dollar size.
- **Pre-solicitation** shaping precedes even that (months to ~1–2 years; not yet
  measured internally).
- **Protest** can add 30 days (commonly) to 100+ days (conservatively) after award.

**Headline for planning:** for a meaningful Navy recompete the solicitation drops
roughly **2.5–3 years before** the incumbent's ordering period ends, and shaping
starts earlier still. The textbook "watch 12–18 months out" is **too late** for the
parallel-rebuy pattern — our point-in-time anticipability was only ~5 of 11 events
at 12 months (Section 9).

---

## 5. PALT benchmarks (published)

Solicitation-to-award medians from GAO's defense-lead-time work (GAO-24-106528),
converted to months. **These are medians on awards that occurred; spot-verify the
specific figures against the source before external use** (Section 11).

| Cut | DoD median | Navy median |
|---|---|---|
| **By vehicle — orders** | 21 days (~0.7 mo) | 50 days (~1.6 mo) |
| **By vehicle — definitive contracts** | 97 days (~3.2 mo) | 132 days (~4.3 mo) |
| **By vehicle — IDC / IDIQ** | 179 days (~5.9 mo) | 185 days (~6.1 mo) |
| **High-dollar (>$50M) — definitive** | 245 days (~8.1 mo) | 273 days (~9.0 mo) |
| **High-dollar (>$50M) — IDC** | 300 days (~9.9 mo) | **393 days (~12.9 mo)** |
| **High-dollar (>$50M) — orders** | 139 days (~4.6 mo) | 179 days (~5.9 mo) |

Definitive-contract PALT by value (DoD): $250k–<$10M **90 d**; $10–<$50M **132 d**;
$50–<$250M **213 d**; ≥$250M **322 d (~10.6 mo)**. Cost-reimbursement runs far
longer than fixed-price (definitive cost-type ~209 d / ~6.9 mo vs fixed-price ~77 d).
GAO's older, non-generalizable weapon-system sample ranged from **under 1 month to
over 4 years** — i.e., the median hides a long tail.

**Read by award type:**
- **Orders** are fastest (the holder pool pre-exists) — ~1.6 mo typical, ~6 mo for
  high-dollar Navy orders.
- **Definitive contracts** — ~4 mo all-size Navy, ~9 mo for >$50M.
- **New parent IDC/IDIQ** — slowest — ~6 mo all-size Navy, **~13 mo for >$50M**.

---

## 6. What determines the window's length

In roughly descending priority:

1. **Instrument and award structure** (Section 3) — orders < definitive < new
   parent vehicle, on the front end.
2. **Dollar value and complexity → PALT** — larger, cleared, integration-heavy, or
   cost-reimbursement buys are planned earlier and awarded slower (Section 5).
3. **Competition strategy** — full-and-open source selection (and protest exposure)
   lengthens it; a logical follow-on or sole-source action shortens and closes it.
4. **Appropriation period of availability for obligation** — the funding
   appropriation must be obligated within its statutory window (O&M 1 yr;
   Procurement 3 yr, Shipbuilding/SCN 5 yr; RDT&E 2 yr), read from the Treasury
   Account Symbol. **This is the bridge between the budget layer and the timing
   layer:** it back-stops the latest an award can be made with a given year's funds.
5. **Option structure** — base plus option periods set the cadence; each
   option-exercise decision is a potential early opening (non-exercise) or deferral.
6. **Bid-protest exposure** — a GAO protest triggers a CICA automatic stay and a
   statutory decision interval (Section 7).
7. **Scope changes — bundling or splitting; set-aside or NAICS changes; new
   cybersecurity scope** — all lengthen the front end.
8. **Incumbency barriers** — incumbent control of data rights, software, interfaces,
   facilities, or a uniquely qualified workforce lengthens preparation or justifies
   a noncompetitive path.

---

## 7. When the instrument ends but no open recompete appears

A governing end date only creates a *candidate*. These authorities let the
incumbent continue with no open competition — the dominant source of false
positives.

| Mechanism | Why the incumbent keeps it | Authority |
|---|---|---|
| Option exercise | Priced option exercised; no new competition | FAR 17.207 |
| Services bridge extension | Existing services extended (total ≤ **6 months**) | FAR 52.217-8 |
| Order-level option after parent closes | Child-order option still live after parent's last date to order | FAR 16.505 |
| Logical follow-on order | Sole-source follow-on under an existing MAC/IDIQ | FAR 16.505(b)(2) |
| Only one holder capable | Order to one holder without fair opportunity | FAR 16.505(b)(2) |
| Schedule limited-source order/BPA | Limited to one source (urgency / sole capability / logical follow-on) | FAR 8.405-6 |
| Only one responsible source | New standalone follow-on to incumbent | FAR 6.302-1 |
| Major-system / specialized follow-on | Switching causes substantial duplicated cost or unacceptable delay | FAR 6.302-1 |
| Statutory sole source | 8(a) / HUBZone / SDVOSB / WOSB or other statutory source | FAR 6.302-5 |
| In-scope modification | Within scope, timely, funded — may need no new competition | FAR 6.301 / 43.2 |

**Key legal fact (cuts against "they'll just sole-source it"):** contracting without
full and open competition is unlawful unless a FAR 6.302 exception applies, and it
**cannot** be justified by lack of advance planning or by concern that funds will
expire (FAR 6.301(c)). A bridge action is a signal the recompete is *late, not
absent*.

---

## 8. Budget / funding alignment — a confidence scale, not a primary key

There is no public field that proves a one-to-one tie between an award and a Program
Element, P-1 line, R-2 project, or O-1 activity. Public data shows funding agency,
funding office, federal account / Treasury Account Symbol, program activity, and
obligations — exact line traceability usually needs the signed order, modification,
ACRN, purchase request, or MIPR. So record budget alignment as a **confidence
level** feeding event probability, never as a forced crosswalk.

| Level | Label | Meaning |
|---|---|---|
| **A** | Direct budget trace | Accounting data / ACRN ties the obligation to a specific PE, P-1 line, R-2 project, or line of accounting |
| **B** | Strong public inference | Funding office, federal account, program activity, description, PSC/NAICS, and justification language all align |
| **C** | Portfolio alignment | Broad account/category/program area continues; no clean contract-to-line match |
| **D** | Weak / no alignment | Award history exists, but public budget materials give no useful demand signal |
| **X** | Misleading-alignment risk | Title match exists, but funding office / account / scope does not support it |

**Budget-alignment posture by award type:**
- **Standalone definitive contract** — the strongest case (the contract *is* the
  performance instrument; no parent layer). Target **Level B**.
- **Task / delivery order** — align at the **order / funding-office / requirement**
  level ("does this funded mission continue?"), not "does the parent IDIQ have a
  budget line." Typically **B–C**.
- **Parent IDIQ / MAC / GWAC** — use **demand alignment, not line-item alignment**.
  A parent vehicle is a buying channel funded by many accounts via child orders;
  tying it to one R-1/P-1/O-1 line is a Level-X error. Ask "do the agencies using
  this vehicle still have funded demand for the categories it covers?" — **Level C**
  at best.

---

## 9. Forward-looking indicators

The award record (§§1–3) is retrospective. On its own it gives only modest lead —
our backtest anticipated just ~5 of 11 recompetes from data public 12 months out
(§13). The 2.5–3-year lead the §4 timeline calls for comes from the **forward
layer**. Organize it on two orthogonal axes: **where** a signal lives (how reliable
it is) and **when** it fires (how much lead it gives). The two run opposite — the
most explicit signal is the latest and most certain; the earliest signals are the
least certain.

### 9.1 Where active requirements live — the certainty axis

There is no single public database of active requirements. They surface in layers,
most explicit to most inferential.

| Layer | Source | Role |
|---|---|---|
| **1 · Procurement notices** | SAM.gov Contract Opportunities (sources sought, RFI, presolicitation, solicitation, J&A / sole-source, award notices) | The explicit plane; first stop for *active monitoring*. Returns only the **latest active version** — snapshot to keep an audit trail. |
| **2 · Acquisition forecasts** | Agency recurring procurement forecasts; FAR 5.404 long-range estimates; GSA forecast tool; APEX | Not solicitations, not commitments, but often **months earlier** than a notice. Non-binding, irregularly published. |
| **3 · Budget materials** | P-1 / R-1 / O-1 / M-1 / C-1, PE/BLI; FYDP out-years | Demand *persistence* — the **earliest** signal. Non-binding; no clean contract-to-line crosswalk (§8). |
| **4 · Restricted ordering channels** | Holder-only fair-opportunity competitions (FAR 16.505); GSA eBuy RFQs (FAR 8.405-2) | **A visibility blind spot** — order-level opportunities may never appear as a public notice. A public-data-only screen is blind unless you hold the vehicle, team with a holder, or read award outcomes after the fact (§11). |
| **5 · Awards data** | SAM.gov Contract Awards / FPDS / USAspending | Backward-looking (DoD delayed ~90 days), but the best predictor of *which recurring requirements reappear* (§§1–3). |

### 9.2 The early-warning ladder — the lead-time axis

The same signals, ordered by how far ahead each one fires.

| Lead before the event | Indicator | Source | Caveat |
|---|---|---|---|
| ~2–5 yr | Program persists / grows / declines in the out-years | FYDP, P-1 / R-1 / O-1, PE/BLI | Non-binding |
| ~1–2 yr | Listed in the agency acquisition forecast | FAR 5.404; GSA forecast tool | Non-binding, irregular |
| ~12–24 mo | Sources sought / RFI (earliest transaction-specific signal) | SAM.gov Contract Opportunities | — |
| ~6–12 mo | Industry day / draft RFP / presolicitation (shaping, FAR 15.201) | SAM.gov Contract Opportunities | — |
| now | Solicitation issued (FAR 5.203 minimums) | SAM.gov Contract Opportunities | — |
| lagging | Bridge action — the recompete is *late* | Award record | Confirms a slip, not a death (§7) |

Cross-cutting forward triggers: option-exercise decision proximity (the FAR 52.217-9
notice window), appropriation period-of-availability expiry (§6), and congressional
funding actions (marks, plus-ups, new-start notifications, supplementals).

### 9.3 Reading the two axes together

The certainty axis (9.1) tells you *how reliable* a source is; the lead-time axis
(9.2) tells you *how early* it fires — and they are inversely related. **Do not
confuse "most reliable" with "first to fire."** For *active monitoring*, start at
Layer 1 (notices). For *early warning* — the manager's question — start at Layers
2–3 (forecasts and the out-year budget profile) and treat the Layer-1 solicitation
as **confirmation**, not warning: by the time it posts, most of the shaping is done.

### 9.4 The product — a forward-looking requirement-family map

Joined to the award record, the forward layers turn the backward award-family map
(§§1–3) into an opportunity **pipeline**. The deliverable is a ranked dataset —
**one row per candidate requirement family, not per award / PIID** — each row
answering:

1. What is the recurring requirement?
2. Who owns and funds it (requiring & funding office)?
3. How has it been bought (instrument, vehicle, parent / child)?
4. Who is the incumbent (normalized to ultimate parent)?
5. What is the annual obligation run-rate?
6. What date forces the next decision (governing date, §3)?
7. Are options or bridges in play (§7)?
8. What public demand signals exist (Layers 1–2)?
9. What budget / funding signals exist (Layer 3; alignment level, §8)?
10. What vehicle access is required (§12)?
11. How competed / addressable is it (§10)?

The **least** useful output is "contracts expiring in the next 18 months" — noise
(options remaining, one-time buys, closeout tails, parent vehicles whose orders run
on, coming bridges, active-but-not-addressable). The map is the antidote: it says
where to look, when, who owns the demand, how large it is, which vehicle controls
access, and which forward signal would confirm the recompete is forming.

---

## 10. Scoring — event probability × addressability

Score the two quantities independently; read them as a 2×2, not a single rank.
Weights are an operating heuristic, **not** a calibrated scheme (Section 12).

| Event-probability factor | Addressability factor |
|---|---|
| Proximity to a decision point (option / completion / last date to order) | Vehicle access or a credible prime partner |
| Recurring obligation pattern | Technical and mission fit |
| Requirement persists in budget / forecast (budget-alignment level, §8) | Readiness to perform (security, clearance, delivery posture) |
| Active procurement signals present (§9) | Relevant past performance |
| Likelihood of competition vs likely sole-source (§7) | Transition / data-rights barriers; set-aside alignment |

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

Budget alignment belongs mostly in **event probability**; it should barely move
**addressability** — a well-funded recompete on a vehicle the firm cannot access is
not addressable.

---

## 11. Data-availability discipline (no look-ahead)

A reproducible screen can only act on data that was public at the time.

- **The last date to order is a base-award data element.** For a parent IDV it is
  populated on the base award (modification 0) and is knowable from the award's
  signed date forward — *not* added at a later milestone. (Measured: 20/20 vehicles
  carried it at modification 0; none first appeared on a later modification.)
- **It can be extended outward** by exercised option ordering periods or
  modifications (measured: 4/20 extended — two DoD IDIQs once each, two FSS
  Schedules repeatedly, five years at a time), and DoD records are released on a
  ~90-day delay with classified actions omitted. So the value is a **floor that can
  drift later, never earlier**, visible "from award day plus the reporting lag."
- **Some opportunities never reach the public notice plane.** Order-level
  competitions under multiple-award vehicles run among holders under FAR 16.505 fair
  opportunity, and Schedule RFQs may post only to GSA eBuy (FAR 8.405-2) — so a
  public-data-only screen cannot see them prospectively (§9, Layer 4). For
  holder-gated work, treat the *absence* of a notice as uninformative; rely on
  vehicle-holder status, a teaming route, or post-award outcome monitoring instead.

**Consequence:** anchor any lead-time measurement on the date a datum became
*public* (the signed date of the action that established it, plus reporting lag),
and treat option-bearing or Schedule-type vehicles as floor dates likely to drift.
Anchoring on a future end date with perfect foresight overstates how early an event
was actually anticipable.

---

## 12. The operating playbook, by award type

The shared method, specialized. Build each candidate as a record with the five
layers (requirement identity · governing dates · execution evidence · budget
alignment · procurement/access signal).

### Comparison matrix

| Dimension | Standalone definitive contract | Task / delivery order | Parent IDIQ / MAC / GWAC |
|---|---|---|---|
| **Opportunity unit** | Follow-on contract | Follow-on order (same or different vehicle), or bridge | Vehicle replacement or on-ramp / new pool |
| **Governing date** | Ultimate completion + options | Order completion + order options | **Last date to order** + parent options + order velocity |
| **PALT benchmark (Navy)** | ~4 mo; ~9 mo if >$50M | ~1.6 mo; ~6 mo if high-dollar | ~6 mo; **~13 mo if >$50M** |
| **Statutory length** | Service options ≤5 yr total (FAR 17.204(e)) | Order within parent scope/period/ceiling (FAR 16.505) | 5-yr base, ≤10 yr total (10 U.S.C. §3403); A&AS ≤5 yr (§3405) |
| **Direct-entry gate** | Open competition — **bid directly** | **Holder-only** — need the vehicle, a teaming route, or the next recompete | Vehicle recompete / on-ramp is the **only** direct entry |
| **Budget alignment** | Strongest — target Level B | Order/requirement level — B–C | Demand alignment only — Level C (line-item match = Level-X error) |
| **Dominant retention risk** | Option exercise; 6.302-1 follow-on; data rights; 217-8 bridge | Logical follow-on (16.505); migration to a *different* vehicle | Successor vehicle awarded early; child orders run past last date to order |
| **Recommended watch-lead** | ~12–18 mo (simple) / ~18–30 mo (complex) before ultimate completion | Shorter (months) — but vehicle access is a year+ prerequisite | **2–4 years** for a major vehicle |

### Standalone definitive contract

The most addressable type for a non-incumbent: there is no parent layer and the
direct route is open. Watch the **ultimate completion date** (not the current
completion date — if options remain, the near-term event is an option exercise, not
a recompete). Confirm the requirement persists (recurring obligations, funding-office
continuity, justification language), then back-solve the timeline: solicitation
~PALT + transition before ultimate completion. Budget alignment is the strongest of
the three — Level B is achievable. Primary risks: a 6.302-1 only-one-source or
major-system follow-on, data-rights lock-in, or a 52.217-8 bridge.

### Task / delivery order

The order — not the parent vehicle — buys the work; align budget and dates at the
**order level**, and **never add the parent ceiling to child-order values**. The
binding constraint is **access**: orders are competed among holders under FAR 16.505
fair opportunity, so a non-holder cannot reach the order directly — it must already
be on the vehicle, team with a holder, or wait for the vehicle recompete/on-ramp.
The signature trap is **vehicle migration**: the follow-on may appear as an order
under a *different* vehicle with a new order number and slightly different scope, so
an identifier search misses it — match the requirement family instead. PALT is short
(the holder pool pre-exists), so the actionable lead is dominated by the *access*
prerequisite, not the order timeline.

### Parent IDIQ / MAC / GWAC

This is the only type where the **last date to order** is the right anchor, and the
strategic one: winning a seat at the vehicle recompete or on-ramp opens the
order-level market for the whole cycle. A parent is a **buying channel**, not a
funded requirement — use demand alignment (aggregate child-order obligations and the
portfolio budget), never a single budget line. Two structural facts from our
backtest: the **successor vehicle is typically awarded ~24 months before the
predecessor's last date to order** (so agencies have somewhere to place orders, and
old/new vehicles coexist), and **child orders perform past the parent's last date to
order**. So the parent closing to new orders ≠ the work ending. PALT is the longest
of the three (~13 months for a >$50M Navy IDC), and shaping for a major vehicle
begins 2–4 years out.

---

## 13. Empirical calibration to date

Measured on a focused maritime-IDIQ segment (NAICS 336611 / 336612) under
`saronic_specific_awards_data/research/contracts/`. **Segment-specific and
small-sample** (Section 12 weights and Section 5 PALT are the external complements).

| Measurement | Result |
|---|---|
| Ordering-period length (last date to order − award start) | median ~53 months; small-craft IDVs ~49 mo, larger ~84 mo (n=26) |
| Successor vs incumbent end | successor awarded a median **~24 months before** the predecessor's last date to order (8 of 11 ran in parallel with the incumbent) |
| Point-in-time anticipability (no look-ahead) | **9/11** anticipable 6 months before the successor award; **5/11** at 12–18 months |
| Visibility lead (successor award − date last date to order first recorded) | median ~48 months (base) / ~35 months (final) |
| Last date to order availability | **20/20** present at base award (mod 0); **4/20** later extended outward |
| PALT (internal) | not measurable from current pulls (one-year Opportunities window) — use Section 5 |

---

## 14. Current unknowns

1. **Front-end (pre-solicitation) lead** for our segments — the sources-sought →
   solicitation interval is unmeasured (differing solicitation numbers; one-year
   Opportunities window). PALT (Section 5) covers only solicitation → award.
2. **Outward-drift base rate** — how often, and by how much, a last date to order is
   extended after award, by instrument type (only 4/20 observed).
3. **Vehicle-substitution rate** — how often a recompete surfaces as an order under a
   *different* vehicle (no fresh competition appears) versus a standalone solicitation.
4. **Generalization** — whether the maritime-IDIQ "successor precedes incumbent end"
   pattern holds for services and definitive production contracts (likely
   segment-dependent).
5. **Public-release lag distribution** — assumed ~90 days for DoD; unmeasured, and it
   shifts every visibility-anchored lead.
6. **PALT figure verification** — the Section 5 medians are sourced to GAO-24-106528
   but not yet spot-checked against the source document.

---

## 15. Likely weak spots

1. **Anchoring on the last date to order when it drifts outward** (option ordering
   periods, extensions; FSS Schedules especially) — a timing false positive, not a
   missing-data error.
2. **Semantic requirement matching is fuzzy and unautomated** — the predecessor↔
   successor link rests on scope/office/place-of-performance/incumbent judgment;
   identifier joins fail (requirement-identity trap); the backtest chains were
   hand-validated on a small set.
3. **Holder-only access for orders** — the order-level market is closed to
   non-holders; mis-scoring addressability here is the most expensive error.
4. **The bridge trap** — a sole-source bridge reads as "locked-up work" when the
   recompete is merely late.
5. **Thin forward signals** — the Opportunities join is a single-year, latest-version
   window with no historical snapshots, so the demand-signal half is weak and not
   auditable over time.
6. **Uncalibrated scoring** — the event-probability and addressability weights are
   heuristic; no outcome data has been used to fit them.
7. **Median-vs-tail in the PALT benchmarks** — Section 5 reports medians; the tail
   (cost-type, complex source selection, protests) runs far longer, and PALT is
   measured only on awards that occurred (survivorship; cancellations and slips drop
   out).
8. **Small, segment-specific calibration** — every internal number is from maritime
   IDVs, n in the tens.
9. **Source-data limits** — DoD reporting delay, omission of classified actions, and
   first-tier-only subaward reporting (the visibility trap).
10. **Conflating appropriation availability with period of performance** — the
    appropriation's period of availability for obligation and the contract's period
    of performance are different things; keep the Treasury Account Symbol read
    separate from the completion dates.

---

## 16. Protest exposure (reserve)

| Item | Rule | Reserve |
|---|---|---|
| GAO filing deadline | Solicitation defects before proposal due; otherwise within **10 days** of basis known (or 10 days after a required debriefing) — 4 CFR 21.2 | — |
| GAO decision deadline | ≤ **100 days** (express option ~65 days) — 4 CFR 21.9 | 100 days conservative |
| CICA automatic stay | Pre-award: no award while pending; post-award: stay if GAO notice within ~10 days of award / 5 days after required debriefing — 31 U.S.C. 3553 / FAR 33.104 | up to 100 days if not overridden |
| Observed DoD delay | GAO closes >½ of DoD protests within **30 days**, the rest within 100 | 30 days common |
| Agency-level protest | Best efforts within **35 days** (FAR 33.103); does not extend the GAO stay | ~35 days |

Corrective action can add more than the GAO decision interval itself (reopened discussions,
reevaluation, solicitation amendment, or recompete).

---

## Appendix A — Terminology discipline

This document uses procurement terms of art exactly and does **not** use the
informal word "clock." The precise terms:

- **Last date to order** — the ordering-period end date of a parent IDV; the
  deadline for placing new orders. Child orders may perform past it.
- **Current completion date** — end of presently-exercised performance.
- **Ultimate completion date** — end if every priced option is exercised.
- **Period of performance** — the performance window of an award/order.
- **Option period (FAR 17.2)** — a priced, unilaterally exercisable extension.
- **PALT (Procurement Administrative Lead Time)** — solicitation issuance → award.
- **Period of availability for obligation** — the statutory window during which an
  appropriation may be obligated ("color of money"), read from the Treasury Account
  Symbol — distinct from any period of performance.

Other terms: IDV (indefinite-delivery vehicle), IDIQ / IDC, MAC, GWAC, FSS (Federal
Supply Schedule); definitive contract; delivery / task order; extent competed; fair
opportunity (FAR 16.505); JEFO (Justification for Exception to Fair Opportunity);
J&A (Justification and Approval); set-aside; single- / multiple-award; bridge action;
novation; logical follow-on.

## Appendix B — Source systems and roles

| System | Role | Key fields |
|---|---|---|
| SAM.gov Contract Awards | Base pull — primes, IDVs, orders, structure, dates | PIID, referenced IDV PIID, last date to order, completion dates, extent competed, solicitation identifier |
| FPDS (Atom feed) | Per-action history and lineage (retiring FY2026) | Action signed dates, modification numbers, last date to order per action |
| SAM.gov Contract Opportunities | Forward demand signals | Notice type, posted date, solicitation number |
| USAspending | FY obligation and Treasury Account Symbol bridge | Federal action obligation, TAS, period-of-performance dates |
| President's Budget / justification (P-1, R-1, PE/BLI) | Forward funding persistence (non-binding) | Account, program element / budget line item, color of money |

## Appendix C — Statutory / regulatory reference

| Topic | Authority |
|---|---|
| PALT definition / reporting mandate | FY2019 NDAA **§878** (Pub. L. 115-232) |
| Task/delivery-order contract length | 10 U.S.C. **§3403** (5-yr base, ≤10 yr total; longer only by written exceptional-circumstances finding) |
| A&AS task-order contracts | 10 U.S.C. **§3405** (≤5 yr incl. options) |
| Service/supply option limits | FAR **17.204(e)** (generally ≤5 yr; excludes IT; subject to statute) |
| Ordering & fair opportunity | FAR **16.504 / 16.505** |
| Option exercise conditions | FAR **17.207** |
| Services bridge extension (≤6 mo) | FAR **52.217-8** |
| Sole-source authorities | FAR **6.302-1 / 6.302-5**; Schedule limiting sources **8.405-6** |
| No-competition limits | FAR **6.301** (lack of planning / expiring funds is not a justification) |
| Notice / response minimums | FAR **5.203** (15 / 30 / 45 days) |
| Early industry exchanges | FAR **15.201**; acquisition planning **7.104 / 7.105** |
| Bid protests | 4 CFR **21**; 31 U.S.C. **3553**; FAR **33.103 / 33.104** |
| PALT benchmarks | GAO-24-106528 (*spot-verify specific medians before external use*) |

---

*Cross-references:* `recompete_opportunity_methodology.md` (the longer conceptual
treatment); `research/wiki/05-recompetes-and-opportunity-intelligence.md` (the
false-positive traps and award-family model);
`saronic_specific_awards_data/research/contracts/scripts/backtest_recompete.py`
and `extracted/backtest_results.csv` (the historical-replay backtest).
