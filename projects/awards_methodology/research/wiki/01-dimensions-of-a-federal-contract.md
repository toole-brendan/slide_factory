---
title: The dimensions of a federal contract
---

# The dimensions of a federal contract

The single most useful idea for reading United States defense contracting is that the subject's vocabulary is not a list of mutually exclusive contract types but a set of **dimensions**, each of which answers a different question about the same award. An acquisition does not have to be *either* an indefinite-delivery indefinite-quantity (IDIQ) contract *or* a firm-fixed-price contract *or* a multiple-award contract; it is routinely all three at once, because "what ordering structure," "how is the contractor paid," and "how many companies hold the vehicle" are independent questions. Most confusion in reading contract announcements, federal spending data, and trade-press reporting comes from collapsing two or more of these dimensions into one — for example, treating IDIQ as though it were a pricing type, or treating a vehicle's ceiling as though it were money that has been spent. This chapter sets out the ten dimensions used throughout this reference and then walks a single example through all of them.

## Why a dimensional model

Consider the following description of one acquisition:

> A DoD **multiple-award IDIQ**, with **firm-fixed-price task orders**, a five-year **ordering period** plus options, **incremental funding**, and a large-business **prime contractor** using several **subcontractors**, supporting a weapon program acquired through **multiyear procurement**.

Read as a list of competing categories, that sentence appears self-contradictory: how can something be both an IDIQ and firm-fixed-price, both multiple-award and have a single prime performing, both incrementally funded and multiyear? Read as a set of dimensions, there is no contradiction at all. Each emphasized term names a value along a different axis. The IDIQ label describes the ordering structure; firm-fixed-price describes payment and risk; multiple-award describes the number of vehicle holders; the ordering period describes time; incremental funding describes how money is obligated; prime and subcontractor describe the performance chain; and multiyear procurement describes the funding-and-commitment method of the program the work supports. A reader who keeps the axes separate can classify almost any award correctly; a reader who does not will repeatedly mistake one dimension for another.

## The ten dimensions

The following ten questions classify any defense award. Each later chapter of this reference develops one or more of these dimensions in detail.

| Dimension | The question it answers | Representative values |
|---|---|---|
| Legal relationship | Who has a contract with whom? | Government–prime; prime–subcontractor; subcontractor–lower-tier subcontractor |
| Instrument | What legal vehicle is being used? | Standalone (definitive) contract, purchase order, IDIQ, requirements contract, BPA, BOA |
| Award structure | How many prime holders are there? | Single award, multiple award |
| Ordering | Is work bought at the parent level or through later orders? | Direct contract performance, task order, delivery order, BPA call |
| Pricing and risk | How is payment calculated and who bears cost risk? | FFP, FP-EPA, FPI, CPFF, CPIF, CPAF, T&M, labor-hour |
| Competition | Who may compete? | Full and open, set-aside, sole source, fair opportunity among vehicle holders |
| Time | How are future periods authorized? | Base period, option period, ordering period, order period of performance |
| Funding | When and how is money obligated? | Fully funded, incrementally funded, annual procurement, multiyear procurement |
| Performance chain | Who actually performs the work? | Prime employees, subcontractors, vendors, teammates |
| Data classification | How do SAM.gov and USAspending represent it? | Definitive contract, IDV, parent award, order, transaction, subaward |

Two pairings cause most of the trouble and are worth naming at the outset. First, the **instrument** dimension and the **pricing** dimension are fully independent: an IDIQ may issue firm-fixed-price orders, cost-reimbursement orders, or both, and the same is true of a standalone contract or a multiyear contract. The compact rule, developed in [Pricing types and cost risk](08-pricing-types-and-cost-risk.md), is that *vehicle type determines how work is accessed, while pricing type determines how the contractor is paid and who bears cost risk*. Second, the **award structure** dimension (single versus multiple award) and the **competition** dimension (full and open, set-aside, or sole source) are independent, so that a single-award contract may be the result of vigorous competition and is not the same thing as a sole-source award; that distinction is the subject of [Single-award, single-source, and sole-source](16-single-award-and-sole-source.md).

## A complete worked example

A single hypothetical connects most of the vocabulary. Suppose the U.S. Army needs engineering support over ten years but cannot predict in advance which specific projects will arise or in what quantity.

```text
Army engineering requirement
│
├── Solicitation for a multiple-award IDIQ
│
├── Prime Contract A
├── Prime Contract B
├── Prime Contract C
├── Prime Contract D
└── Prime Contract E
       │
       ├── Task Order 0001 — systems engineering
       │      ├── FFP CLIN
       │      ├── Cost-reimbursement CLIN
       │      ├── Base year
       │      ├── Two order-level options
       │      └── Subcontracts to two specialist firms
       │
       └── Task Order 0002 — testing services
```

Each feature of this structure sits on one of the ten axes:

- The **IDIQ** instrument is chosen because the quantity is uncertain and work will be bought through future orders rather than at award. The contract states a binding minimum and a stated maximum, as required for indefinite-quantity contracts under FAR 16.504.[^c1-far165]
- **Multiple award** is the award-structure value: five separate companies received five parallel prime contracts for the same scope. They do not jointly hold one contract, and none of them owns the entire ceiling.
- The vehicle's **ceiling** is the maximum aggregate value of orders the terms authorize; it is a contractual boundary, not money already obligated. This distinction is the whole subject of [Awards, ceilings, obligations, and spending](03-awards-ceilings-obligations-spending.md).
- When a specific need arises, the Army runs an **order competition** among the eligible holders — a fair opportunity to be considered, not a reopening of full and open competition to the whole market. Fair opportunity is governed by FAR Subpart 16.5 (in the current DoD deviation, primarily FAR 16.507) and is developed in [Indefinite-delivery contracts](06-indefinite-delivery-contracts.md).[^c1-deviation]
- The winning company receives a **task order**, which is itself a binding contract within the parent framework even though it is not a separate prime contract with the Government.
- The order may use **several pricing types at different contract line-item numbers (CLINs)** — here a firm-fixed-price CLIN alongside a cost-reimbursement CLIN — making the order a hybrid. CLIN structure is covered in [CLINs, SLINs, and funding traceability](15-clins-slins-and-funding-traceability.md).
- The order may carry **options** of its own, separate from any options on the parent IDIQ; an order-level option and a parent-level option are different things, as [Options and award terms](09-options-and-award-terms.md) explains.
- **Subcontractors** perform portions of the order, but the prime remains responsible to the Army, which generally has privity of contract only with the prime — the subject of [Prime–subcontractor structure, privity, and flowdowns](12-prime-contracting-subcontracting-teaming.md).
- Actual **funding** is recorded through obligations on the orders and their modifications, not by reading the parent ceiling. Tracing those obligations is covered in [How awards appear in federal data](04-contract-data-systems.md).

That one example exercises the instrument, award-structure, ordering, pricing, competition, time, funding, performance-chain, and data-classification dimensions simultaneously, which is precisely why no single label captures it.

## The two analytical warnings that follow from the model

The dimensional model produces two warnings that recur throughout this reference and are stated here so that later chapters can refer back to them.

The first concerns money. Because the instrument and funding dimensions are separate, the phrase **"award amount" is ambiguous to the point of being dangerous**: the estimated or potential value, the vehicle ceiling, the minimum guarantee, the obligation, and the outlay are five distinct numbers that can differ by orders of magnitude. The most consequential consequence is the prohibition on adding a parent IDV ceiling to the values of its child orders, which double-counts; expenditure analysis must follow the obligation transactions. This is developed in [Awards, ceilings, obligations, and spending](03-awards-ceilings-obligations-spending.md).

The second concerns validity. Because competition, time, funding, and authority are separate dimensions, being within an instrument's stated **scope** is necessary but never sufficient to make a contract action lawful. The action must also be timely (within the ordering period), within the ceiling, properly competed or justified, funded from a legally available appropriation, and executed by a warranted contracting officer. The interaction of these axes is the subject of [Period of performance and scope](10-period-of-performance-and-scope.md) and [Contracting authority and who makes the award](17-contracting-authority-and-award-decisions.md).

## Version note

The dimensional framework itself is stable, but the regulatory citations attached to particular dimensions are in transition. As of the article date (June 25, 2026), DoD contracting officers apply the Revolutionary FAR Overhaul rewrite of FAR Part 16 under a class deviation effective March 16, 2026, which places fair-opportunity ordering procedures primarily at FAR 16.507, whereas the still-codified FAR places many of those procedures at FAR 16.505.[^c1-deviation] Where a dimension's governing citation has moved, this reference gives the current DoD-deviation location and notes the codified one.

[^c1-far165]: FAR 16.504, indefinite-quantity contracts, requiring a stated minimum (more than a nominal quantity) and a stated maximum. <https://www.acquisition.gov/far-overhaul/far-part-deviation-guide/far-overhaul-part-16>.
[^c1-deviation]: Department of Defense class deviation adopting the Revolutionary FAR Overhaul of FAR Part 16, effective March 16, 2026; fair-opportunity procedures relocated primarily to FAR 16.507. <https://www.acquisition.gov/sites/default/files/page_file_uploads/DoD_RFO_Deviation_Part-16.pdf>.
