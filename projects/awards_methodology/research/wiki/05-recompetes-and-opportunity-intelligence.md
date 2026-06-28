---
title: Recompetes and opportunity intelligence from awards data
---

# Recompetes and opportunity intelligence from awards data

The preceding chapter describes how a federal award appears as a typed record; this chapter describes what those records, read together and read forward, can and cannot reveal about a *future* acquisition event. The subject sits on the **data-classification**, **competition**, and **time** dimensions at once, but as an inference layer over them rather than as another record type. Its governing distinction, and the most common error it guards against, is twofold: a **recompete is not a data field** — no system reports one — and the question "will a requirement be bought again?" must be kept separate from the question "could a particular firm win the resulting action?" Collapsing those two questions into a single "opportunity score" produces confident nonsense. This chapter is the analytical counterpart to the record model in [How awards appear in federal data](04-contract-data-systems.md) and to the pre-award lifecycle in [The acquisition lifecycle, source selection, and contracting authority](17-contracting-authority-and-award-decisions.md): it reads the historical record against forward demand signals to estimate where, when, and how an existing requirement may next be acquired.

## A recompete is an inferred event, not a data field

No federal system publishes a field that says "this requirement will be recompeted on this date." A recompete — or, more generally, a follow-on acquisition event — is **inferred** by assembling an award's history and joining it to forward-looking signals of continued demand. The raw material comes from two distinct public data planes: the contract-award record, exposed through the SAM.gov Contract Awards data and the Federal Procurement Data System,[^c05-samawards] and the opportunity-notice record, exposed through the SAM.gov contract-opportunities data.[^c05-samopps] Neither plane labels an event as a recompete; the inference is the analyst's.

The cardinal rule of the analysis is to estimate **two separate quantities** and never to merge them:

- **Event probability** — the likelihood that the requirement is bought again at all, on some timeline.
- **Addressability** — the likelihood that a given firm can reach and win the resulting action.

A near-certain recompete on a vehicle a firm cannot access is not an opportunity for that firm; a perfectly addressable requirement that will never be rebought is not an opportunity at all. Holding the two apart is what keeps the analysis honest, and the scoring section below treats them as two axes rather than one number.

## The opportunity unit is not one thing

A first discipline is to identify *what* would actually be rebought, because the candidate events are not equivalent and do not share a clock or a competitive posture.

| Opportunity unit | What the next event actually is | How it tends to surface in data |
|---|---|---|
| Standalone definitive contract | A follow-on contract for the same requirement | A new contract PIID, usually preceded by a new solicitation |
| Task or delivery order | A follow-on order, under the same or a different vehicle | A new order PIID referencing a parent IDV |
| Parent IDIQ or MAC | Replacement of the ordering vehicle itself | A new IDV PIID; existing orders may run on for years |
| IDIQ on-ramp or new pool | Added holder seats on an existing vehicle | A special notice or amendment, not a fresh competition |
| Subcontract package | A prime re-sources a scope one tier down | Not in prime-award data; only via first-tier reporting |
| Bridge action | A short sole-source continuation | A sole-source modification or short interim award |
| OT production follow-on | A production action after a prototype Other Transaction | May never appear as an open competition |
| SBIR/STTR Phase III | A continuation of earlier SBIR/STTR work | May be sole-source, with a small public footprint |

An expiring task order does not imply that its parent vehicle is expiring; conversely, a parent vehicle may be recompeted while orders beneath it continue for years. The vehicle-level units connect to [IDV, IDIQ, MAC, GWAC, and Schedules](07-idv-idiq-mac-gwac-schedules.md); the subcontract unit to [Prime contracting, subcontracting, teaming, and first-tier reporting](12-prime-contracting-subcontracting-teaming.md); the OT and Phase III units to [Alternative acquisition pathways and "not a contract type" traps](18-not-a-contract-type-traps.md); and the bridge unit to [Single-award, single-source, and sole-source](16-single-award-and-sole-source.md).

## Award families, not flat rows

A single transaction row says little; the signal lives in the **award family** — the set of records that together describe one requirement over time. Assembling a family means grouping records by the underlying requirement rather than by identifier alone, and retaining the fields that carry timing, recurrence, and competitive posture:

- **PIID and referenced IDV PIID** — to separate an order from its parent vehicle.
- **Modification number and modification reason** — to distinguish option exercises, funding actions, extensions, and closeout.
- **Recipient UEI and CAGE, and ultimate parent** — to normalize subsidiaries, mergers, and name changes.
- **Awarding office and funding office** — to identify the buyer separately from the money's owner.
- **PSC, NAICS, description, and place of performance** — to reconstruct the requirement.
- **Current completion date, ultimate completion date, and last date to order** — the several clocks.
- **Action obligation and total obligations** — to measure recurring demand.
- **Base-and-exercised and base-and-all-options values** — to gauge contractual scale (not spending).
- **Extent competed, number of offers, type of set-aside, and source-selection method** — to estimate future competitive posture.
- **Solicitation identifier** — to join the award to past or future notices.

The underlying record model — the PIID, the parent–child link, the transaction, and the value fields — is defined in [How awards appear in federal data](04-contract-data-systems.md) and is not repeated here; the contract-award data elements that populate these fields are exposed through the SAM.gov Contract Awards data.[^c05-samawards] A worked family looks like the following.

```text
Requirement: "Installation X network operations and maintenance"   (matched SEMANTICALLY)
│
├── Parent IDV — PIID P-AAAA   (MATOC; last date to order: 2027-09-30)
│      extent competed: full and open; set-aside: none
│
├── Task order O-0007  (parent ref P-AAAA)   ← the incumbent order
│      PSC D310 · NAICS 541512 · current completion 2026-09-30 · ultimate 2028-09-30
│      base+exercised $40M · base+all-options $55M · total obligations $31M
│      ├── mod P00003 — option exercise       → state: NOT YET (an option is live)
│      ├── mod P00005 — incremental funding    → no new event
│      └── mod P00007 — 6-month bridge          → the recompete is LATE, not dead
│
└── Candidate next events:
       • follow-on order under P-AAAA          (needs vehicle access — ch. 07 / ch. 12)
       • replacement of P-AAAA itself          (a parent-vehicle recompete)
       • bridge → later open or limited competition
```

## Classifying every transaction

Because the family is built from transactions, each must be classified into an opportunity-relevant type. The same calendar event — a modification near an end date — can mean very different things, and the classification, not the date, carries the signal.

| Transaction class | What it signals | Opportunity state |
|---|---|---|
| New award | A requirement entered the base | The clock starts |
| Incremental funding | Money added to existing work | No new event |
| Option exercise | The Government continued existing work | Not yet a recompete; the decision point moves out |
| Quantity addition | More of the same bought under the contract | Recurring demand; not an open competition |
| Period extension | The performance window lengthened | Planned continuation or a slip — read with other signals |
| Bridge extension | A short sole-source continuation | The recompete is late, not absent |
| Administrative change | Address, accounting, or name correction | No economic signal |
| Deobligation / closeout | Funds released; the instrument is winding down | Activity is ending, not beginning |
| Novation / name change | The holder's legal identity changed | The incumbent may be the same firm renamed |
| Termination | Work stopped early | The requirement may reopen sooner than scheduled |

The modification taxonomy itself — bilateral versus unilateral, and why a modification need not add work or money yet can be enormous — is owned by [Post-award administration, modifications, and closeout](14-contract-modifications.md); this chapter only maps those modification kinds onto opportunity states.

## Multiple clocks, not one expiration

A requirement does not have a single expiration date. It has several clocks, and useful monitoring works in **date bands** rather than from one date:

- **Current completion date** — the end of presently exercised performance, and the earliest meaningful continuation decision.
- **Next option date** — when the Government must decide whether to continue.
- **Ultimate completion date** — the end if every predetermined option is exercised.
- **Parent ordering-period end / last date to order** — the deadline for placing new orders under a vehicle, after which child orders may still run.
- **Expected acquisition lead time** — how long the buying organization needs to run the next acquisition.

As a capture heuristic — not a legal deadline — monitoring of complex, cleared, or integration-heavy requirements tends to begin roughly **18 to 30 months** before ultimate completion, and of smaller or simpler buys roughly **9 to 18 months** before. That an indefinite-delivery vehicle is governed by a last date to order rather than a single performance end date, and that its child orders may run past that date, follows the period-of-performance data model.[^c05-popwhitepaper]

```text
            lead-time band (complex/cleared buy: 18–30 months)  ← heuristic, not a deadline
         ┌───────────────────────────────────────────────┐
   today │                                                 │ current completion (earliest decision)
   ──────┼──────────────┬───────────────┬─────────────────┼────────────────┬──────────────►
         │          next option     monitor window         │            ultimate completion
         │                          opens (smaller buy:     │
   parent last date to order ─────  9–18 months)            orders may run PAST last-date-to-order
```

The distinction between these capture-timing bands and the *legal* clocks — what may lawfully happen after an ordering period closes — matters: the legality is governed by [Period of performance and scope](10-period-of-performance-and-scope.md), while this chapter uses the same dates only as signals of when a buying decision is due.

## Joining award history to demand signals

Award history is retrospective; on its own it shows what happened, not whether the requirement still exists. It must be paired with forward demand signals drawn from the opportunity-notice plane and the budget.

| Signal | What it implies about the next event |
|---|---|
| Sources sought / request for information | The market is being surveyed; a buy is forming |
| Presolicitation notice | A solicitation is imminent |
| Solicitation / combined synopsis–solicitation | The competition is open now |
| Intent to bundle | Scope is being consolidated across requirements |
| J&A, fair-opportunity exception, or intent to sole-source | Competition will be limited or absent |
| Acquisition forecast / budget justification | The requirement persists in plans (nonbinding) |
| Industry day | Early shaping; the requirement is live |
| Bridge action | The intended competition is running late |
| Program- or small-business-office confirmation | Corroboration from outside the data |

Two cautions attach to the data. First, the SAM.gov contract-opportunities interface returns only the **latest active version** of a notice — active notices are refreshed daily and archived notices weekly — so a system that needs an audit trail of how a requirement evolved must **snapshot** notices over time rather than rely on the live record.[^c05-samopps] Second, agency acquisition forecasts and the long-range acquisition estimates contemplated by the FAR are explicitly **nonbinding** planning estimates, useful as clues to persistence but not as commitments.[^c05-forecast] The lifecycle meaning of each of these notices — what a sources-sought notice or a draft solicitation *is*, and why early exchanges matter — is developed in [The acquisition lifecycle, source selection, and contracting authority](17-contracting-authority-and-award-decisions.md); whether the requirement remains funded is a question for [CLINs, funding traceability, and program transition](15-clins-slins-and-funding-traceability.md).

## Scoring event probability and addressability separately

The two questions defined at the outset are best treated as two weighted axes, scored independently. The factors and illustrative weights below are an operating heuristic, not an official scheme.

| Event-probability factor | Weight |
|---|---:|
| Timing proximity to a decision point | 25 |
| Recurring obligation pattern | 20 |
| Requirement persists in budget or forecast | 20 |
| Active procurement signals present | 20 |
| Likelihood of competition (versus likely sole-source) | 15 |

| Addressability factor | Weight |
|---|---:|
| Vehicle access or a credible prime partner | 25 |
| Technical and mission fit | 20 |
| Readiness to perform (security, clearance, and delivery posture) | 20 |
| Relevant past performance | 15 |
| Transition and intellectual-property barriers | 10 |
| Set-aside alignment | 10 |

The readiness factor includes security and clearance posture only as one element among several; it is not a cybersecurity assessment. Scored separately, the two axes form a simple decision frame rather than a single ranking.

```text
                         ADDRESSABILITY  (can a given firm capture it?)
                           low                          high
                 ┌────────────────────────┬────────────────────────┐
   EVENT   high  │  team with, or route    │   pursue capture        │
 PROBABILITY     │  through, a holder       │   directly              │
 (will a buy     ├────────────────────────┼────────────────────────┤
  happen?)  low  │  monitor                 │  shape the requirement  │
                 │                          │  early (FAR 15.201)     │
                 └────────────────────────┴────────────────────────┘
```

Vehicle access and the teaming routes feed from [IDV, IDIQ, MAC, GWAC, and Schedules](07-idv-idiq-mac-gwac-schedules.md) and [Prime contracting, subcontracting, teaming, and first-tier reporting](12-prime-contracting-subcontracting-teaming.md); the intellectual-property barrier from the data-rights discussion in that same chapter; set-aside alignment from [Small business in defense contracting](13-small-business.md); and the "shape the requirement early" quadrant from the pre-award exchanges described in [The acquisition lifecycle, source selection, and contracting authority](17-contracting-authority-and-award-decisions.md).

## The false-positive traps

Most errors in this analysis are false positives — readings that treat ordinary contract life as a coming opportunity. The recurring traps are worth naming.

| Trap | Why a naive read misfires | The correct read |
|---|---|---|
| Option trap | Current completion is near, but options remain | The near-term event is an option exercise; watch the ultimate completion date |
| Bridge trap | A short sole-source extension looks like locked-up work | The recompete is late, not dead |
| Vehicle trap | The follow-on becomes an order under a different vehicle | No open competition appears; track the requirement across vehicles |
| Requirement-identity trap | The successor has a new PIID, office, PSC, NAICS, or title | Match requirements semantically, not by identifier |
| Bundling / splitting trap | One contract becomes several, or several become one | Expect the opportunity unit to change shape |
| Parent/order trap | A parent vehicle and a child order run different clocks | Track both clocks separately |
| Innovation-follow-on trap | A production OT or SBIR Phase III continues with no open competition | These statutory routes are lawful closed competitions |
| Administrative-activity trap | A late modification looks like live work | Invoicing, audits, and deobligations continue after performance ends |
| Visibility trap | Absence of data looks like absence of activity | DoD data is delayed and omits classified actions; sub-tiers report only first-tier |
| Corporate-identity trap | A new awardee name looks like a new competitor | It may be the same corporate family after a merger, novation, or UEI/CAGE change |

Several traps point directly at other chapters: the innovation-follow-on trap to the prototype-OT and SBIR Phase III routes in [Alternative acquisition pathways and "not a contract type" traps](18-not-a-contract-type-traps.md),[^c05-dfars206] the administrative-activity and visibility traps to the reporting delay and record model in [How awards appear in federal data](04-contract-data-systems.md) and the first-tier-only reporting in [Prime contracting, subcontracting, teaming, and first-tier reporting](12-prime-contracting-subcontracting-teaming.md), and the corporate-identity trap to novation as a modification in [Post-award administration, modifications, and closeout](14-contract-modifications.md).

## The throughline

Opportunity intelligence is an exercise in disciplined inference, and its discipline is a set of separations. Score two things, not one: whether a buy will happen, and whether a given firm can reach it. Build families, not rows; classify transactions, not just count them; reason in date bands, not from a single expiration; and match requirements by their substance, not by their identifiers. Above all, remember what the data is: public award records are delayed and incomplete, and notices show only their latest state, so the honest output of the method is a set of **probabilities and lead times**, never a certainty. Read that way — against the record model of the previous chapter and the lifecycle of the next — awards data becomes a forward-looking instrument without ceasing to be the backward-looking record it actually is.

[^c05-samawards]: SAM.gov Contract Awards data and the Federal Procurement Data System, exposing contract, date, dollar, competition, modification, office, recipient, and parent-reference data elements for awards and orders; public DoD contract data is released on a delay. <https://open.gsa.gov/api/contract-awards/>.
[^c05-samopps]: SAM.gov Get Opportunities (contract opportunities) public API, providing notice types including sources sought, presolicitation, combined synopsis/solicitation, special notice, justification and approval, and intent to bundle; it returns only the latest active version of a notice, with active notices refreshed daily and archived notices weekly. <https://open.gsa.gov/api/get-opportunities-public-api/>.
[^c05-popwhitepaper]: Federal Spending Transparency, period-of-performance data-element guidance, distinguishing the current and ultimate (potential) completion dates of an award from the ordering-period end date / last date to order applicable to procurement indefinite-delivery vehicles, whose child orders may run beyond it. <https://fedspendingtransparency.github.io/whitepapers/period-of-performance/>.
[^c05-forecast]: Department of Defense component acquisition forecasts, and the long-range acquisition estimates contemplated by FAR 5.404, are best-estimate planning information subject to change and do not bind the Government. <https://www.acquisition.gov/far/5.404>.
[^c05-dfars206]: DFARS 206.001-70, exception for prototype projects: a competitively awarded prototype Other Transaction that is successfully completed may be followed by a production contract or transaction without further competition when the original solicitation and agreement contemplated the follow-on and the statutory conditions are met. <https://www.acquisition.gov/dfars/206.001-70-exception-prototype-projects-follow-production-contracts.>.
