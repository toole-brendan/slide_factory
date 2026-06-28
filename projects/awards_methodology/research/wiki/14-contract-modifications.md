---
title: Post-award administration, modifications, and closeout
---

# Post-award administration, modifications, and closeout

A **contract modification** is a written change to the terms of an existing contract or order. It can be tiny or enormous, funded or unfunded, administrative or substantive, and it is defined entirely by its relationship to an already-awarded instrument rather than by its dollar size (FAR 2.101).[^c14-far2101] A modification belongs to no single dimension of an award: a given modification might add money, change time, alter [pricing](08-pricing-types-and-cost-risk.md), revise scope, or merely correct an address, and the same instrument may be modified many times over its life. This chapter sets out what a modification is, the typical kinds, the bilateral-versus-unilateral distinction and the rule that only a contracting officer can modify the Government's contract, what is *not* a modification (most importantly, a new order under an indefinite-delivery indefinite-quantity (IDIQ) parent), why a modification need not add work or money, and why a modification can nonetheless be one of the largest actions in an acquisition program.

## What a modification is

Under FAR 2.101 a modification is any written change in the terms of a contract. The term is deliberately broad: it spans corrections of clerical errors, the obligation or deobligation of funds, changes to quantity or price, revisions to the statement of work, and partial or complete terminations. Because the category is defined by *what it does to an existing instrument* and not by magnitude, two modifications that look nothing alike — a one-line correction to a paying-office address and a multibillion-dollar addition of production work — are the same kind of contract action in the federal data systems. That breadth is the root of much misreading of contract announcements and spending data, a point developed in [How awards appear in federal data](04-contract-data-systems.md).

A modification operates on an existing award, so it inherits and is bounded by that award's other dimensions. It must stay within the instrument's stated **scope**, fall within any ceiling, be timely, be funded from a legally available appropriation, and be executed by an official with authority. Being within scope is necessary but never sufficient to make a modification lawful — the same validity test that governs every contract action, set out in [Period of performance and scope](10-period-of-performance-and-scope.md).

## Typical kinds of modification

Modifications recur in a recognizable set of forms. A single modification may combine several of these at once:

- add or remove funding (obligate additional money, or **deobligate** unused funds);
- exercise an **option**, the mechanics of which are described in [Options and award terms](09-options-and-award-terms.md);
- change quantity (increase or decrease the units ordered);
- change price or estimated cost;
- add, delete, or revise a **contract line-item number (CLIN)**, the structural units treated in [CLINs, SLINs, and funding traceability](15-clins-slins-and-funding-traceability.md);
- change a delivery date or period of performance;
- revise the statement of work;
- direct a **change** under the contract's Changes clause;
- negotiate an **equitable adjustment** following a Government-directed change;
- change accounting or payment information;
- **terminate** some or all of the contract (for convenience or for default); and
- **definitize** an initially unpriced action, converting it to firm terms.

Each of these touches a different axis of the underlying award — funding, time, pricing, scope, or the line-item structure — which is why the bare label "modification" conveys almost nothing about what actually changed.

## Bilateral versus unilateral

A modification can be **bilateral** or **unilateral**, and the difference lies in who signs it (FAR Subpart 43.1).[^c14-subpart431]

A **bilateral modification** — also called a supplemental agreement — is signed by both the contracting officer and the contractor. It is used where the change requires the contractor's assent, typically to reflect a negotiated agreement: definitizing an unpriced action, negotiating an equitable adjustment, or otherwise altering terms the contractor is not already obligated to accept.

A **unilateral modification** is signed only by the contracting officer. It is used where the Government may act on its own under authority the contract already grants — to exercise an option, make an administrative change (such as correcting a paying-office address), issue an authorized change order under the Changes clause, or give a termination notice. The Government can act unilaterally in these cases precisely because the underlying right or authority was fixed when the contract was awarded; the unilateral exercise of an option, for instance, works because the option's terms were established at award, as explained in [Options and award terms](09-options-and-award-terms.md).

### Only a contracting officer can modify the contract

Whether a modification is bilateral or unilateral, the Government's signature must come from a **warranted contracting officer**. Only an authorized contracting officer can modify the Government's contract (FAR 43.102).[^c14-far43102] A program manager, a contracting officer's representative (COR), an engineer, or any other government employee cannot legally change the contract merely by sending instructions, expressing a preference, or directing the contractor in the field. Apparent direction from someone without contracting authority does not bind the Government and can expose the contractor to performing uncompensated or unauthorized work; the limits of who holds that authority are the subject of [Contracting authority and who makes the award](17-contracting-authority-and-award-decisions.md). The Revolutionary FAR Overhaul rewrite of the modification rules retains this core allocation of authority to the contracting officer.[^c14-overhaul]

## What is not a modification

Not every change in the contracting relationship is a modification of an existing instrument. The most important case is the **new order under an IDIQ**. A new task order or delivery order placed against an IDIQ parent is generally a *new order under the parent*, not a *modification to the parent IDIQ*. FAR Part 43 expressly distinguishes orders that do not otherwise change the parent contract's terms from modifications. Placing an order draws on the ordering authority the parent already established (the indefinite-delivery framework is described in [Indefinite-delivery contracts](06-indefinite-delivery-contracts.md)); it does not rewrite the parent's terms.

The distinction matters because each order, once issued, is itself a contract action that can be modified on its own. A modification to a task order changes that order — not necessarily the parent IDIQ:

```text
Parent IDIQ contract
│   (placing an order is NOT a modification of the parent)
│
├── Task Order 0001
│      ├── Modification 01 — add funding      ← modifies the ORDER
│      └── Modification 02 — extend schedule  ← modifies the ORDER
│
└── Task Order 0002
```

Here, Modification 01 and Modification 02 change Task Order 0001; they do not necessarily change the parent IDIQ. Keeping the layers separate — order versus parent — is essential to reading the action correctly, and it parallels the parent-level-versus-order-level distinction drawn for options in [Options and award terms](09-options-and-award-terms.md) and for the core terms in [The core vocabulary](02-core-vocabulary.md).

## Why a modification need not add work or money

A modification does not inherently mean "more work," and it does not even necessarily mean more money. The category includes actions that remove money, add nothing of substance, or change only an administrative detail. The following table shows how loosely "modification" correlates with either adding funds or adding work:

| Modification | Adds money? | Adds work? |
|---|---|---|
| Correct the paying-office address | No | No |
| Deobligate unused funds | Reduces money | No |
| Add the next increment of funding for already ordered cost-type work | Yes | No |
| Exercise an option | Yes, usually | Yes |
| Pay an equitable adjustment for an earlier Government change | Yes | Not necessarily |
| Add a new deliverable | Usually | Yes |
| Extend schedule due to contractor delay | Maybe not | No |
| Add another year of recurring services | Usually | Yes |

Two rows reward attention. Adding the next **increment of funding** for cost-type work that was already ordered puts money on the contract without adding any new work — the work was already authorized, and the modification merely obligates the next tranche against it, a pattern tied to incremental funding and traced in [Awards, ceilings, obligations, and spending](03-awards-ceilings-obligations-spending.md). Conversely, paying an **equitable adjustment** adds money to compensate the contractor for an earlier Government-directed change, not necessarily to buy additional deliverables. The key question is therefore not just whether money was added; it is *which contractual obligation was changed or created*.

## A modification can be enormous

Because a modification is defined by its relationship to an existing contract and not by its dollar value, a single modification can represent most of a major acquisition program. The clearest example is the Navy's 2019 Virginia-class **Block V** action: a roughly **$22.2 billion** fixed-price-incentive, multiyear modification to an existing contract that added construction of nine submarines and included an option for a tenth (DoD daily "Contracts" announcement, December 2, 2019).[^c14-blockv] In structural terms this single action exercised the [pricing](08-pricing-types-and-cost-risk.md) dimension (fixed-price-incentive), the funding-and-commitment dimension ([multiyear procurement](11-multiyear-procurement-and-production.md)), and the [options](09-options-and-award-terms.md) dimension at the same time, while being recorded as a modification.

This is precisely why procurement databases can mislead. An action labeled "modification" carries no implication that it is small or routine; economically it may be the bulk of a flagship program. A reader who treats "modification" as a synonym for a minor adjustment — or who tries to reconstruct program spending without distinguishing the substance of each modification — will badly misjudge where the money is. As with the ambiguity of "award amount," the safe practice is to look past the label to the obligations actually recorded, the discipline developed in [How awards appear in federal data](04-contract-data-systems.md).

## Post-award kickoff and the administration phase

Award begins the work; it does not end it. A signed contract or order marks the point at which performance, billing, oversight, and eventual closeout commence, and modifications are only one of the instruments that operate during the long administration phase that follows. It is common, soon after award, for the parties to hold a **post-award orientation** — often a kickoff conference — to align expectations, walk through the statement of work and deliverables, confirm reporting and invoicing mechanics, and identify the officials who will administer the contract on each side. FAR Subpart 42.5 treats post-award orientation as a tool for reaching a clear and mutual understanding of contract requirements and for resolving potential problems before they arise; it is a means of administration, not a renegotiation, and it changes nothing in the contract.[^c14-postaward] From that point the contract is **administered** against its terms: the Government monitors performance, inspects and accepts work, pays invoices, records contractor performance, processes any changes through the contracting officer, and ultimately closes the file. The sections that follow trace that arc, with modifications — already treated above — sitting at its center.

## The administering roles

Contract administration is carried out by a defined set of roles whose authority is deliberately uneven. The central distinction is between officials who can legally bind or change the Government's contract and those who cannot, and that distinction is the post-award expression of the same authority rule developed for the award itself in [Contracting authority and who makes the award](17-contracting-authority-and-award-decisions.md).

- The **procuring contracting officer (PCO)** is the warranted contracting officer who awards the contract and ordinarily retains authority over its substantive terms, including modifications, unless that authority is delegated.
- The **administrative contracting officer (ACO)** is a warranted contracting officer to whom contract administration functions are assigned, often at a different office than the one that awarded the contract; the ACO performs the administration functions enumerated at FAR 42.302 and can bind the Government within the scope of that assignment.
- The **contracting officer's representative (COR)** is a Government employee designated in writing by the contracting officer to perform specified technical or administrative monitoring functions. A COR's authority is limited to what the written designation grants and, under FAR 1.604, **does not include authority to make any commitment or change that affects price, quality, quantity, delivery, or other terms** of the contract.[^c14-roles]
- The **Defense Contract Management Agency (DCMA)** is the DoD component that performs contract administration services on many DoD contracts; its personnel include ACOs and supporting specialists who administer contracts delegated to the agency.
- The **program office** owns the requirement and the mission outcome and is the source of much technical direction, but program officials are not contracting officers and cannot, by virtue of program authority, change the contract.

The allocation is summarized below. The decisive column is the last one.

```text
Contract-administration roles and authority
Role          | Primary function                                  | Can change the contract?
PCO           | Awards the contract; retains substantive terms    | Yes — warranted CO
ACO           | Performs assigned administration functions        | Yes — within the delegated scope
COR           | Monitors technical/administrative performance     | No — designation excludes term changes
DCMA          | Provides delegated contract-administration svcs   | Through its warranted COs only
Program office| Owns the requirement and mission outcome          | No — not a contracting officer
```

The governing rule is unchanged from the award context: a contract action that binds or changes the Government must be executed by a contracting officer acting within the scope of a warrant (FAR 1.602), the administration functions are organized under FAR 42.1 and following, and the COR's limited delegated authority is fixed by FAR 1.604.[^c14-roles] A COR, an engineer, or a program manager who issues direction outside that framework cannot change the contract, however senior — the reason informal direction is a recurring source of disputes, taken up below.

## Deliverables and CDRLs

What a contract requires the contractor to furnish divides into two broad classes that are administered differently. **Deliverable supplies and services** are the end items and performance the contract buys — the hardware, the software, the maintenance, the studies. **Data deliverables** are the documents and data the contractor must submit about that work — drawings, test reports, manuals, status reports, and similar items. In DoD contracts the data deliverables are specified on a **Contract Data Requirements List (CDRL)**, recorded on **DD Form 1423**, with each CDRL line item typically tied to an authorizing **data item description (DID)** that defines the content and format of the required submission.[^c14-cdrl] A CDRL line item generally references the work it documents, frequently a line item of the kind described in [CLINs, SLINs, and funding traceability](15-clins-slins-and-funding-traceability.md), and a technical-data line item may itself be carried as not-separately-priced. Distinguishing the supply or service being bought from the data being delivered about it matters because acceptance, payment, and rights attach differently to each, and because a contract can be fully performed in its hardware while data deliverables remain outstanding.

## Inspection and acceptance

Before the Government pays for and takes responsibility for what a contract produces, it ordinarily **inspects** the supplies or services and then formally **accepts** them. FAR Part 46 establishes the quality-assurance framework: inspection determines whether the deliverable conforms to contract requirements, and acceptance is the Government's act of assuming ownership of, or approving, conforming supplies or services.[^c14-inspection] Acceptance carries legal consequences and is not a mere formality. Depending on the contract terms, acceptance can mark the **passage of title** to the Government, start a **warranty** period, and — subject to the contract's inspection clause and exceptions such as latent defects, fraud, or gross mistakes amounting to fraud — be **conclusive**, limiting the Government's later ability to reject the item. Because acceptance fixes these consequences, the question of *when and by whom* acceptance occurs is itself an administration question, and the authority to accept, like other binding acts, runs to the contracting officer or a duly authorized representative rather than to any official who happens to receive the work.

## Invoicing and payment

A contractor is paid by submitting invoices against the contract, and for DoD that submission is predominantly electronic. Invoices and receiving reports are processed through **Wide Area Workflow (WAWF)**, the invoicing and acceptance module of the **Procurement Integrated Enterprise Environment (PIEE)**, which routes a submission among the contractor, the acceptor, and the paying office.[^c14-wawf] Electronic submission is not merely a convenience: DFARS 252.232-7003 requires contractors to submit payment requests and receiving reports in electronic form, ordinarily through WAWF, with narrow exceptions.[^c14-wawf] Payment timing is governed by the **Prompt Payment Act**, under which the Government must pay proper invoices within the applicable period — generally 30 days after receipt of a proper invoice — or owe interest, with the FAR's Prompt Payment clauses implementing the rule. The mechanics of which line item and which line of accounting an invoice draws against are the funding-traceability subject of [CLINs, SLINs, and funding traceability](15-clins-slins-and-funding-traceability.md): an invoice is paid against specific CLINs and the accounting data attached to them, which is why a clean line-item and ACRN structure is what makes orderly payment possible.

## Contractor performance information (CPARS)

The Government keeps an official record of how contractors perform, and that record is **not public**. The **Contractor Performance Assessment Reporting System (CPARS)** is the governmentwide system in which agencies prepare past-performance evaluations on contracts and orders; under FAR Subpart 42.15 these evaluations assess contractor performance and are used to inform future source-selection decisions.[^c14-cpars] CPARS information is **controlled and source-selection sensitive**: completed evaluations feed the past-performance records used in later competitions, and access is restricted to authorized Government and contractor users, with the assessed contractor able to review and comment on its own report but the file as a whole shielded from public disclosure. A public analyst therefore **cannot see a contractor's full CPARS file**; the official performance record sits behind an access wall even though the underlying awards are visible in public data. This asymmetry is why past performance functions as a signal in [Recompetes and opportunity intelligence](05-recompetes-and-opportunity-intelligence.md) without ever being fully observable from outside, and it is the administration-phase counterpart to the responsibility and past-performance judgments that drive the award decisions described in [Contracting authority and who makes the award](17-contracting-authority-and-award-decisions.md).

## Constructive changes and unauthorized direction

Because only a contracting officer can change the contract, direction from anyone else is a recurring source of trouble. A **constructive change** arises when the contractor is effectively required to perform work beyond the contract's requirements — not through a formal modification, but through informal direction, an interpretation imposed by a Government official, or conduct that has the practical effect of altering the work — without a proper change order having been issued. Direction from a COR, an inspector, an engineer, or a program official who lacks contracting authority can create exactly this situation: the work changes in fact, but no authorized instrument records it. The doctrine cuts in two directions at once. It can entitle the contractor to relief, because the Government received changed performance, while also confirming that the informal direction was **unauthorized** and that the only proper way to direct a change is through the contracting officer under the contract's Changes clause. The defensive posture follows directly: a contractor that receives change-like direction from someone other than the contracting officer ordinarily seeks written confirmation from the contracting officer before treating the contract as changed, because apparent direction that does not come from a warranted official does not bind the Government — the same authority limit drawn in [Contracting authority and who makes the award](17-contracting-authority-and-award-decisions.md).

## Claims and equitable adjustments

When a change — formal or constructive — affects the cost or time of performance, the contractor's remedy is monetary and runs through a defined sequence. A **request for equitable adjustment (REA)** is a request that the contract price or schedule be adjusted to account for the effect of a Government-directed or constructive change, typically grounded in the contract's **Changes** clause (FAR 52.243).[^c14-claims] An REA that the parties cannot resolve by negotiation may be converted into, or asserted as, a **claim** under the **Contract Disputes Act**, which the contractor submits to the contracting officer for a written **contracting officer's final decision**; claims above the statutory certification threshold must be certified.[^c14-claims] The contracting officer's final decision is the pivot of the FAR Part 33 **disputes** process, and it is appealable — to an agency **board of contract appeals** or to the **U.S. Court of Federal Claims**.[^c14-claims] The distinction between an REA and a claim is consequential: a claim triggers Contract Disputes Act mechanics, including the contracting officer's decision deadline, the running of **interest** from receipt of a proper claim, and the appeal route, whereas an REA is a negotiation posture that has not yet entered the formal dispute track. Either way the action is resolved by the contracting officer, not by the program office or the COR, which is why a constructive change asserted against informal direction must still be reduced to a request directed at a warranted official.

## Termination and closeout

A contract may end before performance is complete, and it always ends with an administrative wind-down. The Government may **terminate for convenience** when it is in the Government's interest, settling with the contractor for work performed and allowable costs rather than for breach, or **terminate for default** (for cause) when the contractor fails to perform; the two are governed by FAR Part 49, and they differ sharply in their financial and reputational consequences for the contractor.[^c14-closeout] A termination is itself executed by the contracting officer, ordinarily as a modification of the kind catalogued above. Whether a contract runs to full performance or is terminated, it then enters **closeout**: under FAR 4.804 the contracting office verifies that the contract is physically complete, that final payments and any deobligations have been made, that required reports and clearances are in place, and that the file can be administratively closed.[^c14-closeout] Closeout is the formal end of the administration phase, and it can lag performance by months or years — final invoices, deobligation of unspent balances, indirect-cost rate settlements, and audits all occur after the work itself is finished. That lag is the precise mechanism behind the **administrative-activity trap** described in [Recompetes and opportunity intelligence](05-recompetes-and-opportunity-intelligence.md): a deobligation, a final invoice, or a closeout audit appearing in the data long after performance ended is not evidence of live work, but the ordinary tail of administration and closeout playing out on a contract whose substantive effort is already over.

[^c14-far2101]: FAR 2.101, definitions, defining "modification" (and "contract modification") as any written change in the terms of a contract; the definition is by relationship to the instrument, not by dollar value. <https://www.acquisition.gov/far/2.101>.
[^c14-subpart431]: FAR Subpart 43.1, contract modifications (general), distinguishing bilateral modifications (supplemental agreements signed by both parties) from unilateral modifications (signed only by the contracting officer), and listing the uses of each. <https://www.acquisition.gov/far/subpart-43.1>.
[^c14-far43102]: FAR 43.102, policy, providing that only a contracting officer acting within the scope of authority may execute contract modifications on behalf of the Government, and that no one else may direct changes that bind the Government. <https://www.acquisition.gov/far/43.102>.
[^c14-overhaul]: Revolutionary FAR Overhaul — Part 43 deviation guide, the rewritten contract-modification rules DoD contracting officers apply under the class deviation, retaining the allocation of modification authority to the contracting officer. <https://www.acquisition.gov/far-overhaul/far-part-deviation-guide/far-overhaul-part-43>; Department of Defense class deviation adopting the Revolutionary FAR Overhaul, effective March 16, 2026, <https://www.acquisition.gov/sites/default/files/page_file_uploads/DoD_RFO_Deviation_Part-16.pdf>.
[^c14-blockv]: DoD daily "Contracts" announcement, December 2, 2019 — the approximately $22.2 billion Virginia-class Block V fixed-price-incentive multiyear modification to an existing contract, adding nine submarines and an option for a tenth. <https://www.defense.gov/News/Contracts/Contract/Article/2030017/>.
[^c14-postaward]: FAR Subpart 42.5, postaward orientation — orientation conferences and letters used to reach a clear and mutual understanding of contract requirements and to resolve potential problems, as a tool of contract administration that does not alter the contract. <https://www.acquisition.gov/far/subpart-42.5>.
[^c14-roles]: FAR 1.602 (contracting officers — authority to bind the Government within the scope of a warrant); FAR Subpart 42.1 and FAR 42.302 (assignment and listing of contract administration functions, including those delegated to an administrative contracting officer); and FAR 1.604 (contracting officer's representative — written designation whose authority excludes any commitment or change affecting price, quality, quantity, delivery, or other terms of the contract). <https://www.acquisition.gov/far/1.602>; <https://www.acquisition.gov/far/42.302>; <https://www.acquisition.gov/far/1.604>.
[^c14-cdrl]: Contract Data Requirements List (CDRL), DD Form 1423, the instrument by which DoD contracts specify data deliverables, each line item authorized by a data item description (DID); distinguished from the deliverable supplies and services the contract buys. <https://www.esd.whs.mil/Directives/forms/dd1000_1499/>.
[^c14-inspection]: FAR Part 46, Quality Assurance — inspection of supplies and services for conformance to contract requirements and the Government's acceptance, an act that may pass title, start a warranty period, and (subject to the inspection clause and exceptions such as latent defects, fraud, or gross mistakes amounting to fraud) be conclusive. <https://www.acquisition.gov/far/part-46>.
[^c14-wawf]: Wide Area Workflow (WAWF) within the Procurement Integrated Enterprise Environment (PIEE), the electronic system for submitting and accepting invoices and receiving reports; DFARS 252.232-7003 requires electronic submission of payment requests and receiving reports, ordinarily through WAWF, and the Prompt Payment Act governs payment timing and interest. <https://piee.eb.mil/>; <https://www.acquisition.gov/dfars/252.232-7003-electronic-submission-payment-requests-and-receiving-reports.>.
[^c14-cpars]: FAR Subpart 42.15, contractor performance information, and the Contractor Performance Assessment Reporting System (CPARS) — the Government's official, access-controlled, non-public record of contractor past performance, used in source selection and shielded from public disclosure. <https://www.acquisition.gov/far/subpart-42.15>; <https://www.cpars.gov/>.
[^c14-claims]: FAR 52.243 (Changes clauses, the basis for equitable adjustments) and FAR Part 33, Protests, Disputes, and Appeals — the Contract Disputes Act process under which an unresolved request for equitable adjustment may be asserted as a certified claim, decided by a contracting officer's final decision, and appealed to an agency board of contract appeals or the U.S. Court of Federal Claims, with interest running from receipt of a proper claim. <https://www.acquisition.gov/far/part-33>; <https://www.acquisition.gov/far/52.243-1>.
[^c14-closeout]: FAR Part 49 (Termination of Contracts — termination for convenience versus termination for default/cause) and FAR 4.804, closeout of contract files — the post-performance wind-down during which final payments, deobligations, rate settlements, audits, and required clearances are completed before the file is administratively closed. <https://www.acquisition.gov/far/part-49>; <https://www.acquisition.gov/far/4.804>.
