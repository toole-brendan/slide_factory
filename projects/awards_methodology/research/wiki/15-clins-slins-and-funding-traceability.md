---
title: CLINs, funding traceability, and program transition
---

# CLINs, funding traceability, and program transition

A **contract line item number (CLIN)** is the structural unit that organizes what a contract or order buys, and the line-item structure is also where the contractual work most often meets the appropriation that pays for it. This chapter describes what a CLIN organizes, the distinction between a CLIN and its **subline items (SLINs)**, how the **Accounting Classification Reference Number (ACRN)** connects a line item to a line of accounting, how line items behave on an indefinite-delivery contract, and how far a single obligated dollar can be traced from public award data toward a Department of Defense (DoD) Program Element or budget line. Line items belong to no single one of the dimensions set out in [The dimensions of a federal contract](01-dimensions-of-a-federal-contract.md); they are the level at which several dimensions — pricing, time, delivery, and above all funding — are recorded together for one piece of the work.

## What a CLIN is and what it organizes

A CLIN is a separately identified portion of a contract or order used to define what is being purchased and to organize its associated terms. A single line item collects, for that portion of the work, its description; quantity; price or estimated cost; fee; pricing type; funding; delivery schedule; period of performance; place of performance; inspection and acceptance; and payment terms. A CLIN is **not a separate contract**; it is a structural unit inside a contract or order, and the contract or order as a whole remains the legal instrument.

A worked example shows how one contract can hold several different kinds of work at once:

```text
One shipbuilding contract
│
├── CLIN 0001 — Submarine detailed design
│       Pricing: Cost-plus-fixed-fee
│       Quantity: 1 lot
│       POP: Oct. 1, 2026 – Sep. 30, 2028
│       Funding: RDT&E, Navy
│
├── CLIN 0002 — Long-lead propulsion material
│       Pricing: Firm-fixed-price
│       Quantity: 2 sets
│       Delivery: June 30, 2029
│       Funding: Shipbuilding and Conversion, Navy
│
└── CLIN 0003 — Technical data
        Pricing: Not separately priced
        Delivery: per CDRL
```

Because each line item carries its own pricing arrangement, a single contract can be a **hybrid contract**: a firm-fixed-price CLIN, a cost-reimbursement CLIN, a time-and-materials CLIN, and a not-separately-priced data CLIN can all coexist in the same contract. This is the line-item mechanism behind the rule, developed in [Pricing types and cost risk](08-pricing-types-and-cost-risk.md), that a vehicle and its pricing arrangement are independent: the contract is one instrument, but its CLINs can sit on different points of the cost-risk spectrum.

The FAR requires line items to identify, among other things, what is being purchased, the product or service code (PSC), the accounting classification, the quantity, pricing information, and the applicable delivery schedule or period of performance; it also requires the pricing type to be identified at the line-item level when a contract mixes pricing arrangements.[^c15-far41005] These required data elements are what make the CLIN, rather than the contract as a whole, the natural unit at which to read what a contract actually does.

## CLIN versus SLIN

A **SLIN** is a subline item underneath a CLIN, used to break a single line item into smaller administrative pieces without creating a new CLIN. DoD normally constructs CLINs from four numeric characters — `0001`, `0002`, `0003` — and forms SLINs by extending the parent CLIN number. The form of the extension signals what kind of subline item it is:

| Subline item type | Numbering form | Example |
|---|---|---|
| CLIN (base line item) | four numeric characters | `0001`, `0002`, `0003` |
| Separately deliverable SLIN | parent CLIN + two letters | `0001AA`, `0001AB`, `0001AC` |
| Informational SLIN | parent CLIN + two numeric characters | `000101`, `000102`, `000103` |

DoD uses SLINs to separate different deliveries, destinations, funding sources, performance periods, or other administrative characteristics within one line item.[^c15-dfarspgi204-71] The distinction between the two SLIN forms matters: a **separately deliverable SLIN** (the alphabetic form) identifies a separately deliverable or separately priced piece of the line item, whereas an **informational SLIN** (the numeric form) subdivides the line item for accounting or administrative purposes without changing what is delivered.

Two examples show the typical uses. A line item can be split across time:

```text
CLIN 0001 — Engineering support
├── SLIN 0001AA — Base year
├── SLIN 0001AB — Option year 1
└── SLIN 0001AC — Option year 2
```

Or a single, integrated effort can be split only for funding, while remaining one deliverable:

```text
CLIN 0002 — One integrated development effort
├── SLIN 000201 — Army funding (informational)
├── SLIN 000202 — Navy funding (informational)
└── SLIN 000203 — Air Force funding (informational)
```

In the second case the work is not divided — there is one development effort — but the funds come from three sources, so informational SLINs record the split without implying three separate deliverables.

## CLINs, SLINs, and the ACRN: connecting work to a line of accounting

The CLIN or SLIN is frequently the point at which an award's contractual work intersects with the **line of accounting** that funds it. In DoD instruments this connection is made through an **ACRN**, a two-character code that ties a CLIN or SLIN to one or more accounting citations; the system is intended to permit traceability from funding to contract actions.[^c15-dfarspgi204-7107] An ACRN functions as a short pointer: rather than repeating a full accounting classification beside every line item, the instrument assigns each line of accounting an ACRN and then references that code where the funds are applied.

A simple mapping illustrates the pointer:

```text
CLIN 0001 → ACRN AA → FY2026 RDT&E, Navy
CLIN 0002 → ACRN AB → FY2025 Shipbuilding and Conversion, Navy
CLIN 0003 → ACRN AC → FY2026 O&M, Navy
```

Public award data may expose only the high-level account behind such a mapping; the signed contract schedule and the ACRN data provide the more granular link from a specific line item to a specific appropriation, fiscal year, and account. This is the same obligation-tracing problem framed in [Awards, ceilings, obligations, and spending](03-awards-ceilings-obligations-spending.md): the obligation that matters lives on a line item, and the ACRN is what attaches that line item to the appropriation it draws on.

## CLINs on an IDIQ

On an indefinite-delivery indefinite-quantity (IDIQ) contract, line items appear at two levels, and the two should not be confused. At the **parent indefinite-delivery vehicle (IDV)** level, CLINs may describe only broad categories of work — for example, CLIN 0001 systems engineering services, CLIN 0002 software development, and CLIN 0003 travel and other direct costs — without committing specific quantities, prices, or funding. The actual work is specified on the **child order**, whose order CLINs state the real quantity, price, funding, delivery schedule, and period of performance for that order.

The relationship between the two levels is now explicit in regulation: under the rewritten FAR Part 16 that DoD applies through the current class deviation, an order must include both its own line-item information and the corresponding line item from the parent contract.[^c15-far16] An order CLIN therefore carries the order's own terms while remaining traceable to the parent category it draws from. This is consistent with the broader treatment of indefinite-delivery vehicles in [Indefinite-delivery contracts (FAR 16.5)](06-indefinite-delivery-contracts.md): the parent vehicle is a framework, and the obligations that fund real work are recorded on the orders placed under it, line item by line item.

## Can an award be tied to a Program Element or budget line?

There is usually **no standardized public contract-award field** that proves a one-to-one connection between an award and a DoD Program Element or a P-1 budget line item. The connection can sometimes be established from the underlying documents, but it is rarely available as a clean field in public data, and the reason is structural: budget documents and contract data are built on different hierarchies for different purposes.

### The DoD budget-exhibit families

DoD publishes its budget justification in several exhibit families, one per appropriation area, because the appropriation areas are not arranged as a single universal hierarchy.

| Appropriation area | Common public budget exhibit |
|---|---|
| Research, development, test, and evaluation (RDT&E) | R-1 Program Element, with more detailed R-2 / R-2A material |
| Procurement | P-1 procurement line item and supporting exhibits |
| Operation and Maintenance | O-1 |
| Military Construction | C-1 |
| Military Personnel | M-1 |
| Revolving or management funds | RF-1 and supporting materials |

These are published as separate budget-document families precisely because they do not form one common structure.[^c15-comptroller] An RDT&E effort is identified by a Program Element on an R-1; a procurement buy is identified by a line item on a P-1; the two numbering systems do not interoperate, and neither maps cleanly onto a contract's CLINs.

### What a Treasury Account Symbol does and does not identify

A **Treasury Account Symbol (TAS)** identifies the high-level federal account: the agency responsible for the account, the appropriation's period of availability, and the particular fund or account classification.[^c15-gaotas] A TAS does **not** ordinarily identify a specific R-1 Program Element, a P-1 line item, an R-2 project, an O-1 subactivity group, a weapon-system lot, a contract CLIN, or an internal cost center. The granularity gap is large: one TAS may contain dozens or hundreds of program elements, budget lines, activities, and projects. Knowing the TAS therefore locates the appropriation but not the program within it.

### What USAspending can expose

At the award or transaction level, USAspending can expose the federal account or accounts; transaction-level obligation amounts; the awarding agency and office; the funding agency and office; award and order identifiers; action dates; program activities; object classes; and other award attributes. The USAspending API specifically supports award-account and award-funding queries that return federal accounts, funding and awarding organizations, and transaction obligations.[^c15-usaspending] However, a DATA Act **program activity** is not automatically the same thing as a DoD R-1 Program Element or P-1 line item; they are separate reporting structures, and although the names may occasionally align or permit a strong inference, the alignment is not guaranteed. The data systems behind these fields are described further in [How awards appear in federal data](04-contract-data-systems.md).

### Why the mapping is difficult

The mapping from an award to a budget line resists a simple text match for several compounding reasons. A single order can contain several CLINs; several fiscal years of funds; multiple appropriations and multiple TAS values; several internal lines of accounting; both RDT&E and procurement funding; funding from more than one component or agency; and subsequent deobligations or upward adjustments. The parent IDIQ may carry no meaningful program-level funding at all, with the actual funds appearing only on child orders and their modifications. More fundamentally, budget documents describe **formulation and congressional justification**, while contract data describe **execution**; reprogrammings, transfers, working-capital-fund purchases, interagency acquisitions, and changing execution plans can all weaken a simple text match between a budget exhibit and an award. The same execution-versus-plan gap appears in [Multiyear procurement and major weapon production](11-multiyear-procurement-and-production.md), where advance procurement and economic-order-quantity buys spread one program's funding across appropriations and years.

### The document that can close the gap

The instrument that can close the gap is a **signed task order or modification**, which should contain accounting and appropriation data organized through an ACRN. In DoD instruments the ACRN is effectively a pointer to a full line of accounting that may include the appropriation and fiscal year; the program or budget activity; the Program Element or procurement line; the object class; the organization or cost center; the project or subproject; the funding document number; and other service-specific accounting fields. The public version of such a document may redact or omit portions, but the unredacted award file and the accounting system normally contain a more exact funding trail. The modification dimension of this is treated in [Contract modifications](14-contract-modifications.md): because obligations and their accounting data are frequently added by modification, the funding trail of a mature award lives across its modifications, not only in the original signed instrument.

## Tracing where the money came from

Tracing a dollar should begin from the individual contract action or order, not merely from the parent IDV, because the obligation and its accounting data live on the action. The public-data workflow proceeds in nine steps:

1. Identify the prime contract procurement instrument identifier (PIID) and, when applicable, the task or delivery order number.
2. Separate the original award from each modification or transaction.
3. Record the federal action obligation for each transaction.
4. Retrieve the funding agency, funding office, federal account, and TAS.
5. Determine the appropriation family and fiscal-year availability.
6. Review the associated program activity, award description, PSC, NAICS code, and funding office.
7. Match that information against the appropriate R-1, P-1, O-1, C-1, or other budget exhibit.
8. Obtain the signed order and funding modifications to find the ACRNs and lines of accounting.
9. Use the purchase request, Military Interdepartmental Purchase Request (MIPR), funds-certification document, or internal accounting crosswalk when an exact Program Element or budget-line match is required.

The steps are ordered by increasing difficulty and decreasing public availability: the early steps draw on public transaction data, while the later steps require the signed award file or the accounting system.

### Confidence levels of funding conclusions

How firmly a funding conclusion can be stated depends on which of these steps it relies on. The following table pairs typical conclusions with the confidence they can be asserted at from public data.

| Conclusion | Typical confidence |
|---|---|
| "This transaction obligated $12 million from this federal account / TAS" | Usually directly provable publicly |
| "The funding came from Army RDT&E rather than Army procurement" | Usually directly provable |
| "The funding office was this command or component" | Usually directly provable |
| "This probably supports Program Element X" | Often inferable |
| "Exactly $7.2 million came from PE X, Project Y, and $4.8 million from PE Z" | Usually requires the award's accounting data or internal records |
| "This contract is funded entirely by the budget line mentioned in the press release" | Unsafe without transaction and accounting evidence |

The pattern is consistent: the account, the appropriation family, and the funding office are usually provable from public data, while the exact Program Element split and any one-to-one budget-line claim usually require the award's accounting data or internal records. A claim that an entire contract is funded by the budget line named in a press release is unsafe without transaction and accounting evidence to support it.

**Interagency acquisitions** require special care, because the **funding agency** may provide the money while a different **awarding agency** conducts the procurement. In that case the awarding office named on the action is not the source of the funds, and the funding agency, funding office, and federal account fields — not the awarding fields — identify where the money came from. This is one more reason the obligation transaction, and ultimately the ACRN on the signed instrument, is the reliable unit for tracing a dollar, consistent with the question of who actually holds authority over an action treated in [Contracting authority and who makes the award](17-contracting-authority-and-award-decisions.md).

## Purpose, time, and amount

Tracing a dollar to its line of accounting answers where funds came from; it does not by itself answer whether those funds could lawfully be applied to the work in question. That second question is governed by federal fiscal law, which rests on three statutory pillars. An appropriation may be used only for its authorized **purpose**: the purpose statute provides that appropriations are to be applied only to the objects for which they were made, except as otherwise provided by law (31 U.S.C. 1301(a)). It may be obligated only within its **period of availability** — its **time**: an annual appropriation is generally available for obligation only during the fiscal year for which it was enacted, and a multiyear appropriation only across the years specified. And it may be obligated and expended only up to the **amount** appropriated: the **Antideficiency Act** prohibits obligations or expenditures in excess of, or in advance of, available appropriations (31 U.S.C. 1341), and a violation carries administrative and potential penal consequences for the responsible official. The authoritative treatment of these doctrines is GAO's *Principles of Federal Appropriations Law* — the **"Red Book"** — which is the standard reference an analyst consults when an obligation's legality, rather than merely its accounting, is at issue.[^c15-fiscallaw] These three constraints explain a recurring puzzle in awards data: a program can have an appropriation in hand and still be unable to spend it on a given task, because the funds are the wrong purpose, the wrong year, or already exhausted.

## The bona fide need rule

The time constraint has a sharp corollary in the **bona fide need rule**: a fiscal-year appropriation may be obligated only to meet a legitimate — *bona fide* — need arising in, or continuing through, the appropriation's period of availability (31 U.S.C. 1502(a)).[^c15-bonafide] An agency may not use a current year's funds to buy goods or services for a need that does not arise until a later year, nor (absent specific authority) reach back to satisfy a current need with a prior year's expired balances. The rule is what prevents an appropriation's period of availability from being circumvented by buying ahead or banking funds, and it is the doctrine behind many apparent timing anomalies in obligation data: an action's fiscal-year funding must correspond to the year in which the need genuinely exists. For supplies, the need is generally tied to when the items are required; for services, the analysis turns on whether the work is severable or nonseverable, treated next.

## Severable versus nonseverable work

Whether a single year's appropriation can fund work that spans fiscal years depends on whether the work is **severable** or **nonseverable**. **Severable** services are continuing and recurring in nature — the kind of effort that produces value period by period, such as routine maintenance, guard services, or ongoing technical support — and each increment is useful on its own. **Nonseverable** work produces a single end product or accomplishes one whole task — a study delivered as a finished report, a prototype, a discrete construction project — whose value is realized only on completion. The distinction controls funding. Nonseverable work must be **fully funded** in the appropriation current at the time of award, because the entire undertaking represents a single bona fide need of that year. Severable services, by contrast, may within limits **cross fiscal years** on a single year's appropriation: a severable-services contract or order may be funded from an appropriation current at the time of award even though performance extends into the next fiscal year, provided the total period does not exceed twelve months (10 U.S.C. 3133).[^c15-severable] This is why two superficially similar service awards can carry very different funding patterns — one incrementally funded across years, the other obligated in full at award — depending entirely on which side of the severability line the work falls.

## Expired versus cancelled funds

An appropriation's period of availability marks the end of its life for new commitments, not its disappearance. After the period of availability closes, an appropriation **expires**: it is no longer available to incur **new** obligations, but for **five** additional fiscal years it remains available to record, adjust, and liquidate **existing** obligations — for example, to pay invoices on already-obligated work or to make permissible upward adjustments to prior obligations (31 U.S.C. 1553). At the end of that five-year period the account is **cancelled** (closed): the balance is withdrawn, and the appropriation is thereafter unavailable for **any** purpose, whether new obligations or adjustments to old ones (31 U.S.C. 1552).[^c15-expired] The practical consequence for awards analysis is that the apparent state of a years-old contract depends on this clock. A modification that adjusts an obligation against an expired-but-not-cancelled appropriation is permissible; the same adjustment against a cancelled appropriation is not and must instead be charged to current funds, subject to statutory limits. The funding trail of a mature award, which lives across its modifications as [Contract modifications](14-contract-modifications.md) develops, therefore cannot be read without knowing where each appropriation sits on the expired-to-cancelled timeline.

## Continuing resolutions

The three pillars assume that full-year appropriations exist. When they do not — when a fiscal year begins before Congress has enacted some or all of the regular appropriations acts — agencies operate under a **continuing resolution (CR)**, a temporary appropriation that maintains funding for a defined interval. A CR characteristically funds activities at or near the **prior year's rate** and carries restrictions that bear directly on acquisition: it generally bars **new-start** programs (efforts not funded in the prior year), limits **production-rate increases** beyond the prior year's level, and constrains actions whose execution depends on appropriations not yet enacted. The effect is that an action which is otherwise ready to award — a new program's first contract, or a rate increase on an existing one — may have to wait until full-year appropriations are enacted, even though the requirement is validated and the contractor is available. CR-driven delay is thus a distinct, calendar-driven reason a funded-in-concept action does not appear in obligation data when expected, separate from any deficiency in the requirement itself.

## Color of money and program transition

Defense appropriations are not fungible: they come in distinct **"colors,"** each a separate account with its own purpose and period of availability, and the purpose statute makes those boundaries binding. The principal colors are **Research, Development, Test & Evaluation (RDT&E)** — the Navy's, for instance, carried in the **"3600"** appropriation — used to develop and demonstrate capability; **Procurement**, used to buy production quantities of fielded systems; and **Operation & Maintenance (O&M)** — the **"3400"** appropriation — used to operate and sustain them. Because each color may be applied only to its own purpose, **prototype or RDT&E funding does not automatically pay for production**. Moving a capability from development into fielding requires a deliberate **transition** onto **procurement** or **O&M** money of the right year — a step that is budgetary, not merely technical or contractual.

This is the gap between an **endorsed** requirement and a **fundable** one. A program can have enthusiastic operational users, a successful prototype, and a validated need, and still lack **executable** funding, because no appropriation of the **right color and the right year** is available to pay for the next phase. The endorsement establishes that the work is wanted; only an appropriation of the correct color and availability makes it lawful to obligate for that work. The transition decision — and the budget cycle that must produce the procurement or O&M line to support it — is where many otherwise-successful efforts stall:

```text
RDT&E (e.g., "3600")               development / prototype funding
        │
        ▼
  ┌───────────────────────────────────────────┐
  │  TRANSITION DECISION                        │
  │  + an appropriation of the RIGHT COLOR      │
  │    and the RIGHT FISCAL YEAR                │
  │  (endorsed requirement → fundable one)      │
  └───────────────────────────────────────────┘
        │
        ├─────────────► Procurement   production-quantity funding
        │
        └─────────────► O&M (e.g., "3400")   operate / sustain funding
```

This transition-funding hinge is precisely where the alternative acquisition pathways treated in [Alternative acquisition pathways and "not a contract type" traps](18-not-a-contract-type-traps.md) most often falter: an innovation effort begun under a research program or Other Transaction can prove its capability and still have no procurement or O&M line waiting to field it. And it is one of the things an analyst tests when asking whether a requirement genuinely **persists in the budget and the forecast**, as developed in [Recompetes and opportunity intelligence from awards data](05-recompetes-and-opportunity-intelligence.md): a need that has not been funded into procurement or O&M of an actual budget year is endorsed but not yet executable. The obligation that ultimately appears on a line item, traced through its account in [Awards, ceilings, obligations, and spending](03-awards-ceilings-obligations-spending.md), is the downstream evidence that such a transition has in fact occurred.[^c15-coa]

[^c15-far41005]: FAR 4.1005-1, required data elements for contract line items, including a description of what is being purchased, the product or service code, the accounting classification, quantity, pricing information, and the delivery schedule or period of performance, and identification of the pricing arrangement at the line-item level. <https://www.acquisition.gov/far/4.1005-1>.
[^c15-dfarspgi204-71]: DFARS PGI 204.71, Uniform Contract Line Item Numbering System, governing the four-character CLIN, the alphabetic separately deliverable SLIN, and the numeric informational SLIN, and the use of SLINs to separate deliveries, destinations, funding sources, and performance periods. <https://www.acquisition.gov/dfarspgi/pgi-204.71-uniform-contract-line-item-numbering-system>.
[^c15-dfarspgi204-7107]: DFARS PGI 204.7107, Contract Accounting Classification Reference Number (ACRN) and Agency Accounting Identifier (AAI), establishing the ACRN as the pointer connecting CLINs and SLINs to lines of accounting for funding traceability. <https://www.acquisition.gov/dfarspgi/pgi-204.7107-contract-accounting-classification-reference-number-acrn-and-agency-accounting-identifier-aai.>.
[^c15-far16]: Revolutionary FAR Overhaul rewrite of FAR Part 16, applied by DoD under the class deviation effective March 16, 2026, requiring an order to include its own line-item information together with the corresponding line item from the parent contract. <https://www.acquisition.gov/far-overhaul/far-part-deviation-guide/far-overhaul-part-16>.
[^c15-comptroller]: DoD Comptroller budget materials, publishing the R-1 (RDT&E Program Elements), P-1 (procurement line items), O-1, C-1, M-1, and RF-1 exhibit families as separate budget-document families. <https://comptroller.defense.gov/Budget-Materials/Budget2026/>.
[^c15-gaotas]: GAO federal appropriations-law and budget-process materials describing the Treasury Account Symbol as the identifier of the responsible agency, the appropriation's period of availability, and the fund or account classification. <https://www.gao.gov/assets/2019-11/675709.pdf>.
[^c15-usaspending]: USAspending.gov data sources and API, exposing federal accounts, transaction-level obligations, funding and awarding organizations, program activities, and object classes, and supporting award-account and award-funding queries. <https://www.usaspending.gov/submission-statistics/data-sources>; <https://api.usaspending.gov/docs/endpoints>.
[^c15-fiscallaw]: The three pillars of appropriations law — purpose (31 U.S.C. 1301(a), appropriations applied only to the objects for which made), time (period of availability), and amount (the Antideficiency Act, 31 U.S.C. 1341, barring obligations or expenditures exceeding or in advance of available appropriations) — as set out in GAO, *Principles of Federal Appropriations Law* (the "Red Book"). <https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title31-section1301>; <https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title31-section1341>; <https://www.gao.gov/legal/appropriations-law/red-book>.
[^c15-bonafide]: The bona fide need rule — a fiscal-year appropriation may be obligated only to meet a need arising in, or continuing through, its period of availability (31 U.S.C. 1502(a)). <https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title31-section1502>.
[^c15-severable]: Severable versus nonseverable work — nonseverable (single end product or whole task) must be fully funded in the appropriation current at award, while severable (continuing, recurring) services may cross fiscal years on a single year's appropriation for a period not exceeding twelve months (10 U.S.C. 3133). <https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title10-section3133>.
[^c15-expired]: Expired versus cancelled funds — after its period of availability an appropriation expires for new obligations but remains available for five fiscal years to adjust and liquidate existing ones (31 U.S.C. 1553), after which the account is cancelled and unavailable for any purpose (31 U.S.C. 1552). <https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title31-section1552>; <https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title31-section1553>.
[^c15-coa]: Color of money and program transition — RDT&E, Procurement, and Operation & Maintenance appropriations are distinct accounts, each available only for its own purpose and period, so prototype or RDT&E funding does not automatically pay for production; fielding a capability requires transition onto procurement or O&M money of the correct color and fiscal year, which is what separates an endorsed requirement from an executable one. <https://comptroller.defense.gov/Portals/45/documents/fmr/current/02a/02a_01.pdf>.
