---
title: How awards appear in federal data
---

# How awards appear in federal data

The last of the ten dimensions introduced in [The dimensions of a federal contract](01-dimensions-of-a-federal-contract.md) is **data classification**: how the federal systems of record represent a given acquisition as one or more discrete records. The same award that the preceding chapters classify by instrument, pricing, and funding is, inside the data systems, a typed record with an identifier, a place in a parent–child hierarchy, and a set of value and obligation fields. The principal values of this dimension are **definitive contract**, **indefinite-delivery vehicle (IDV)**, **parent award**, **order**, **transaction**, and **subaward**. Confusing these record types — most damagingly, adding a parent vehicle's ceiling to the values of the orders placed beneath it — is the most common source of error in interpreting federal spending data. This chapter describes how SAM.gov, USAspending.gov, and the Federal Procurement Data System (FPDS) represent an award; it defers the definitions of the underlying money concepts to [Awards, ceilings, obligations, and spending](03-awards-ceilings-obligations-spending.md) and defers the detailed budget-line and accounting-classification tracing to [CLINs, SLINs, and funding traceability](15-clins-slins-and-funding-traceability.md), keeping the money-tracing workflow here only at the level of which records carry which numbers.

## The systems of record

Three public systems hold most of what is provable about a federal contract action. The **Federal Procurement Data System (FPDS)** is the contract-action system of record: contracting officers report each award and each subsequent action there, and its data model — typed records, instrument identifiers, and parent–child links — is the model the other systems inherit. **USAspending.gov** is the public spending portal that draws procurement records from FPDS and adds federal-account, transaction, and subaward layers, exposing the same data through a documented application programming interface (API).[^c04-sources] **SAM.gov**, the System for Award Management, is the registration and reporting hub; among other functions it now hosts first-tier subaward and subcontract reporting, which moved there when the legacy FFATA Subaward Reporting System (FSRS) was retired on March 8, 2025.[^c04-fsrs] These systems share a common vocabulary of record types, so that a record described as an IDV in one is the same kind of object in the others.

## The public-data reporting delay

Public contract-action data is not real-time. Contracting officers report actions to FPDS on a lag, and for the Department of Defense the public release of contract-action data is further delayed — DoD-funded and DoD-awarded actions are generally withheld from the public systems for roughly **90 days** after the date the action is signed. The consequence for any analysis built on public data is that recency is lagged: the absence of a recent action does not establish that none occurred, and a monitoring process must treat the latest public picture of DoD work as on the order of a quarter stale.[^c04-delay] This currency limit is one of the reasons the inference of future acquisition events from award history, developed in [Recompetes and opportunity intelligence from awards data](05-recompetes-and-opportunity-intelligence.md), yields probabilities and lead times rather than certainties.

## The record types

### Definitive contract

A **definitive contract** is a standalone award that is complete in itself: it states the work, the price or pricing arrangement, and the period of performance at the time of award, and it does not exist to host later orders. In the data it appears as a single award record carrying its own identifier and its own obligation history. The full vocabulary distinction between a definitive contract and an ordering vehicle is drawn in [The core vocabulary](02-core-vocabulary.md); for data purposes the salient point is that a definitive contract is a leaf, not a framework — it has obligations of its own but no child orders placed against it.

### Indefinite-delivery vehicle (IDV)

An **indefinite-delivery vehicle (IDV)** is the data category for an ordering framework against which later orders are placed. For federal reporting the IDV category is broad: it covers indefinite-delivery contracts, Federal Supply Schedules, blanket purchase agreements (BPAs), basic ordering agreements (BOAs), and other agreements that carry ordering provisions, as contemplated by the contract-reporting rules of FAR Subpart 4.6.[^c04-far46] An IDV record typically reports a ceiling and other framework-level values, but the money the Government actually commits is generally recorded not on the IDV itself but on the orders beneath it. The distinction between the IDV *data category* and the various *instruments* it can contain — and the differences among IDIQ, multiple-award, multi-agency, GWAC, and Schedule vehicles — is the subject of [IDV, IDIQ, MAC, GWAC, and Schedules](07-idv-idiq-mac-gwac-schedules.md).

### Parent award and order

These two record types are defined by their relationship to each other. A **parent award** is a record that other records are placed against; in practice a parent is either an IDV or, occasionally, a standalone contract that hosts orders. An **order** — a task order for services or a delivery order for supplies — is a child record placed against a parent. Crucially, an order generally carries its own **Procurement Instrument Identifier (PIID)** while also identifying the PIID of the parent instrument, so that the data preserves the link between the order and the framework it was issued under.[^c04-far46] The result is a two-level hierarchy: the parent describes the framework and its boundaries, while each child order describes a specific buy and carries the obligations for that buy. The contractual nature of an order — that a task or delivery order is itself a binding contract within the parent framework — is developed in [Indefinite-delivery contracts (FAR 16.5)](06-indefinite-delivery-contracts.md).

### Transaction

A **transaction** is a single reported contract action. The original award is one transaction; each later modification is another, separate transaction against the same award. Every transaction carries its own **federal action obligation** — the change in obligated funds effected by that action — which may be positive, zero, or negative. This is the level at which spending is actually recorded: an award's obligated total is the sum of its transactions, not a single figure read off the award header. Because a modification is its own transaction with its own obligation, expenditure analysis that ignores modification transactions will understate spending; the nature and reach of modifications, including why a single modification can carry most of a program's value, are treated in [Contract modifications](14-contract-modifications.md).

### Subaward

A **subaward** in the transparency data is a reported lower-tier award beneath a federal prime award. In the procurement context a subaward usually denotes a reported **first-tier subcontract** — a subcontract one level below the prime — and not a federal prime award in its own right. Subaward records are reported by the prime recipient rather than by a contracting officer, and since the retirement of FSRS that reporting is collected through SAM.gov.[^c04-fsrs] Because a subaward is a different kind of object from a prime transaction, subaward values must not be commingled with prime obligations when totaling federal spending. The two distinct meanings of "subaward," what the first-tier reporting captures and omits, and the move of that reporting to SAM.gov are the subject of [Subawards, subcontracts, and first-tier reporting](12-prime-contracting-subcontracting-teaming.md).

## Identifiers and the parent–child relationship

The element that ties the record types together is the **Procurement Instrument Identifier (PIID)**, the identifier each contract instrument carries under the contract-reporting rules of FAR Subpart 4.6.[^c04-far46] A standalone contract or an IDV has a PIID; an order placed against an IDV has its *own* PIID and additionally references the parent's PIID. Reading the two identifiers together is what lets an analyst place any order in its framework and distinguish a parent from its children.

```text
IDV (parent award) — PIID: P-AAAA
│   reports a ceiling (a framework boundary, not money obligated)
│
├── Order — PIID: O-0001, parent ref: P-AAAA
│      ├── Transaction: original award  — own federal action obligation
│      ├── Transaction: modification 01 — own federal action obligation
│      └── Transaction: modification 02 — own federal action obligation
│
└── Order — PIID: O-0002, parent ref: P-AAAA
       └── Transaction: original award  — own federal action obligation
              │
              └── (reported separately by the prime)
                  Subaward — first-tier subcontract beneath the prime
```

The hierarchy has a strict reading rule. The ceiling reported on the parent IDV is a boundary on what the orders beneath it may total; the obligations that represent actual spending live on the transactions of the child orders. The parent value and the child values therefore occupy different levels of one structure and overlap, which is why they cannot be added together.

## Period-of-performance fields and ordering periods

Award records also carry dates, and the date fields differ by record type in a way that parallels the parent–child distinction. An ordinary contract or order reports a **current completion date** — the end of the presently exercised performance — and an **ultimate completion date** — the end if all predetermined options are exercised. A procurement **IDV**, however, does not carry period-of-performance end dates in that sense: what bounds it is an **ordering-period end date**, or *last date to order*, and the performance of individual child orders may continue past that date. Reading an IDV's ordering deadline as if it were a performance end date, or expecting one expiration date to govern a vehicle and all of its orders at once, misreads the data model.[^c04-popwhitepaper] How these several clocks are read as signals of future acquisition activity is developed in [Recompetes and opportunity intelligence from awards data](05-recompetes-and-opportunity-intelligence.md); the legal question of what may lawfully happen after an ordering period closes is treated in [Indefinite-delivery contracts (FAR 16.5)](06-indefinite-delivery-contracts.md).

## Current versus potential value fields

A single award record commonly exposes more than one dollar field, and the two most often confused are **current** value and **potential** value. As a matter of database representation, the *current* value reports the presently awarded portion of the award — the base plus any options already exercised — while the *potential* value adds unexercised options and other contingencies; a separate field set records the **action and total obligations**. The distinction is decisive: the current value is a *contract-value* field, not a commitment of funds, and it can differ from the amount obligated; only the obligation fields measure money the Government has actually committed.[^c04-samvalues] The current and potential fields sit side by side because an award legitimately carries both an awarded value to date and a not-yet-exercised ceiling at once, but neither is a spending measure. The exact meaning of either field depends on the specific field consulted, so the field definition, not the label alone, controls the interpretation. These fields are the data-system *representation* of the money concepts — estimated value, ceiling, minimum guarantee, obligation, and outlay — defined in [Awards, ceilings, obligations, and spending](03-awards-ceilings-obligations-spending.md); this chapter describes the fields, while that chapter defines what the underlying amounts mean.

## The rule against double-counting

The single most important rule for working with this data follows directly from the parent–child model:

> **Never calculate federal spending by adding a parent IDV ceiling to the values of its child orders.** For expenditure analysis, follow the obligation transactions and respect the parent–child relationship between the vehicle and its orders.

The rule exists because the parent ceiling and the child-order obligations sit on different levels of the same hierarchy. The ceiling is the maximum that orders placed *under* the IDV may total; the orders are the instruments through which money is actually obligated within that boundary. Summing the two adds a boundary to the very transactions the boundary was meant to bound, double-counting and inflating apparent spending — sometimes by orders of magnitude. The correct unit of expenditure analysis is the obligation recorded on the transactions of the orders (and on any modifications), never a ceiling, an estimate, or a potential value. The derivation of this rule from the underlying money concepts is given in [Awards, ceilings, obligations, and spending](03-awards-ceilings-obligations-spending.md); the present chapter states it as a property of the record model.

## Action labels do not measure economic size

A related caution concerns transaction labels. The label on a transaction describes that action's *relationship* to an existing contract, not its economic magnitude. An action recorded as a **modification** can economically represent most of a major acquisition program — for instance, a multibillion-dollar production modification that exercises a large quantity under an existing contract. Conversely, an original award may be small. Reading the action type as a proxy for dollar size is therefore unreliable; the federal action obligation on the transaction, not its label, is the measure of size. Why a modification need not add scope or even money, and why it can nonetheless be enormous, are developed in [Contract modifications](14-contract-modifications.md).

## A light public-data reading workflow

The full funding-traceability procedure — tracing a dollar down to its budget line item, Program Element, and accounting classification — is a separate subject, covered in [CLINs, SLINs, and funding traceability](15-clins-slins-and-funding-traceability.md). At the level of *which records carry which numbers*, however, a public-data reading of an award proceeds in a few steps:

1. **Identify the instruments.** Record the prime contract PIID and, for an order, both the order's own PIID and the parent IDV's PIID, so the record's place in the parent–child hierarchy is fixed.
2. **Separate award from modifications.** Treat the original award and each modification as the distinct transactions they are, rather than as a single figure.
3. **Record the obligation per transaction.** Capture the federal action obligation for each transaction; their sum, not any header value, is the amount obligated.
4. **Retrieve the funding context.** Identify the funding agency, the funding office, and the federal account associated with the obligations.

The USAspending API supports this reading directly: its award-funding and award-account endpoints return the federal accounts, the funding and awarding organizations, and the transaction-level obligations for an award, so that spending can be traced through the obligation transactions rather than estimated from a ceiling.[^c04-api]

## Awarding agency versus funding agency

A final field distinction matters whenever the question is *who paid*. The **awarding agency** is the agency whose contracting office conducted the procurement and signed the award; the **funding agency** is the agency whose appropriation provided the money. These are separate fields because they are frequently different agencies: in interagency arrangements one agency may fund a requirement while another agency's contracting shop awards and administers the contract on its behalf. Treating "awarding agency" as a proxy for "who funded this" will misattribute spending in exactly those interagency cases, which is why the award-funding data exposes the funding organization separately from the awarding organization.[^c04-api]

[^c04-far46]: FAR Subpart 4.6, Contract Reporting, governing reporting of contract actions to the Federal Procurement Data System, the Procurement Instrument Identifier (PIID) assigned to each instrument, the identification of orders against their parent instruments, and the indefinite-delivery vehicle reporting category. <https://www.acquisition.gov/far/subpart-4.6>.
[^c04-sources]: USAspending.gov data sources, describing how procurement records flow from the Federal Procurement Data System into USAspending and how obligation, transaction, federal-account, and subaward data are organized. <https://www.usaspending.gov/submission-statistics/data-sources>.
[^c04-api]: USAspending.gov API documentation, including the award-funding and award-account endpoints that return federal accounts, funding and awarding organizations, and transaction-level obligations for an award. <https://api.usaspending.gov/docs/endpoints>.
[^c04-fsrs]: SAM.gov, FFATA Subaward Reporting System (FSRS) retirement effective March 8, 2025; first-tier subaward and subcontract reporting migrated to SAM.gov. <https://sam.gov/fsrs>.
[^c04-samvalues]: SAM.gov and the Federal Procurement Data System report the base and exercised options value, the base and all options value, and the action and total obligations as distinct fields; only the obligation fields measure funds committed. <https://open.gsa.gov/api/contract-awards/>.
[^c04-delay]: Public release of Department of Defense contract-action data is delayed approximately 90 days after the action is signed, under the contract-reporting framework of FAR Subpart 4.6 and DoD release practice; public DoD contract data is therefore not real-time. <https://www.acquisition.gov/far/subpart-4.6>.
[^c04-popwhitepaper]: Federal Spending Transparency, period-of-performance data-element guidance, distinguishing the current and ultimate (potential) completion dates of an award from the ordering-period end date / last date to order applicable to procurement indefinite-delivery vehicles, whose child orders may run beyond it. <https://fedspendingtransparency.github.io/whitepapers/period-of-performance/>.
