---
title: Period of performance and scope
---

# Period of performance and scope

The plain statement that "the contract expired" is almost always too imprecise to be useful, because a single defense acquisition runs several independent **clocks** at once, each governing a different question and each producing a different consequence when it ends. This chapter develops two of the dimensions set out in [The dimensions of a federal contract](01-dimensions-of-a-federal-contract.md): the *time* dimension, which asks how the windows for ordering, performing, and delivering are authorized and when they close, and a validity question that sits across the *competition* and *time* dimensions, namely whether a contemplated order or modification is **in scope**. The two are connected by a recurring fact pattern — the parent indefinite-delivery indefinite-quantity (IDIQ) contract whose ordering period has closed while child orders remain alive — and by a single governing principle stated at the end: being in scope is necessary but never sufficient to make a contract action lawful.

## The several independent clocks

Treating an acquisition as having one expiration date conflates distinct events that fall on different dates and carry different legal effects. The following clocks can all run on the same vehicle.

| Clock | What it governs | Consequence when it ends |
|---|---|---|
| Parent IDIQ ordering period | When the Government may issue new task or delivery orders | No new orders may be issued |
| Parent option-exercise window | When the Government may extend the parent ordering period | If not timely exercised, the unilateral right generally lapses |
| Order period of performance | When services under a particular order are scheduled to be performed | Performance becomes due, but the order does not vanish automatically |
| Order delivery schedule | When supplies must be delivered | Delivery becomes due; administration, acceptance, payment, and claims may continue |
| Order option window | When the Government may activate a future order period or quantity | The option must be exercised according to the order's terms |
| Ultimate delivery date | The latest date the contractor can be required to deliver under orders issued during the parent ordering period | Performance generally cannot be pushed beyond that date without additional authority |
| Appropriation availability | When particular funds may incur new obligations | Expired funds generally cannot finance a new need, although they may remain usable to liquidate or adjust valid existing obligations |
| Contract closeout | Administrative completion after final performance, acceptance, payment, audits, and claims | Records are closed; this can occur long after the performance date |

These clocks are anchored in the structure that current FAR Part 16 requires, which under the DoD class deviation reflects the Revolutionary FAR Overhaul rewrite.[^c10-deviation] An IDIQ must state its ordering period, its options, its minimum and maximum, its general scope, the activities authorized to order, and the last date by which delivery may be required. Each order, in turn, must separately contain its own date, line items, performance or delivery schedule, statement of work, and accounting and appropriation data. Because the parent and the order each carry their own time and funding terms, a question such as "may this work still be done?" has no single answer until the relevant clock is identified. The distinction between the parent ordering period and the order period of performance, and between a parent-level option and an order-level option, is introduced in [Indefinite-delivery contracts](06-indefinite-delivery-contracts.md); the mechanics and deadlines of exercising any option belong to [Options and award terms](09-options-and-award-terms.md).

## A timeline example

A concrete sequence shows how the parent ordering clock and an order's own clocks operate independently.

```text
Parent IDIQ ordering period .......... Oct 1, 2022  –  Sep 30, 2027
Ultimate date for performance/delivery ............... Sep 30, 2030

Task Order 0042 issued .............................. Sep 15, 2027
  Task Order 0042 base period ...... Oct 1, 2027  –  Sep 30, 2028
  Task Order 0042 option period .... Oct 1, 2028  –  Sep 30, 2029
```

Task Order 0042 was validly issued on September 15, 2027, before the parent ordering period closed on September 30, 2027. Its performance may continue afterward because FAR 52.216-22 provides that an order issued during the effective period of the indefinite-quantity contract may be completed within the time specified in the order, and the parent contract continues to govern that order even though no new orders may be placed under it.[^c10-clause] Several practical results follow. A new task order ordinarily could **not** be issued on October 1, 2027, because the ordering period had ended the day before. Task Order 0042 may nonetheless run through September 30, 2028 on its base period. Its option might be exercisable in August or September 2028 even though the parent ordering period has long since closed — but only if the parent contract and the order expressly support that arrangement, the option was part of the timely issued order, and the parent's scope, maximum value, and ultimate delivery date are all respected. What the Government cannot do is simply keep adding unrelated work through 2030: that date is the ultimate completion date, the outer boundary on finishing work already properly ordered, not a free additional ordering period.

## The "zombie IDIQ" question

The situation in the timeline — a parent IDIQ whose ordering period has expired while one or more child orders remain active — is sometimes described informally as a **"zombie" IDIQ**, but there is no formal legal category by that name. It is ordinary contract administration. A parent vehicle can be closed to new orders yet continue to govern valid orders issued while it was open, provided those orders were within the parent's scope, issued during the stated ordering period, and within the parent's maximum value. Difficulty arises only when a party tries to treat the surviving orders as a reason to do something that the closed ordering period no longer permits.

The following table separates the actions that are ordinarily available after the ordering period closes from those that ordinarily are not.

| Proposed action | Usually possible? |
|---|---|
| Accept completed work | Yes |
| Pay invoices | Yes |
| Deobligate excess funds | Yes |
| Add incremental funding for already-ordered work | Potentially |
| Pay a valid equitable adjustment or claim | Potentially |
| Extend the schedule so the contractor can finish the same work | Potentially |
| Exercise a previously established order option | Potentially |
| Add a new system, site, quantity, or service period | Usually no |
| Issue a new task order | No |
| Exceed the parent maximum | No |
| Continue recurring services indefinitely through modifications | No |

The pattern in the table is that administration of work already properly bought continues, while anything that amounts to buying new work after the ordering window has closed does not. The "potentially" entries turn on the specific contract terms and on funding, which is why the legal test cannot be reduced to whether money is involved.

## Why "adding money" is not the legal test

A common shortcut treats any modification that adds money as the same kind of action, but the dollar figure is not the test; the question is what the added obligation actually purchases. Consider five hypothetical modifications that each add $5 million to an existing order: (1) funding another increment of the cost already estimated for work that is within the existing order; (2) paying an equitable adjustment caused by a Government-directed change; (3) exercising an option that was evaluated as part of the order; (4) settling a claim arising from past performance; and (5) adding an entirely new work package. The first four may be lawful, depending on the contract documents and the availability of funds, because they pay for, adjust, or complete work already within the deal. The fifth may be an out-of-scope procurement even though it uses the same contractor, the same program, the same contracting office, and the same technology. The converse also holds: a modification can be out of scope even though it adds no money at all — for example, by substantially changing the nature of the required work, or by replacing one deliverable with a materially different one. The treatment of modifications generally, including bilateral and unilateral changes and why a modification need not add work or money, is the subject of [Contract modifications](14-contract-modifications.md), governed under the DoD deviation by the rewritten FAR Part 43.[^c10-part43]

## The two-envelope scope analysis

When the contemplated action sits under an IDIQ, the scope question is not asked once but twice, because the work must fit inside two nested boundaries. A child-order modification generally must satisfy both the **parent IDIQ scope** and the **child order scope**: the parent's scope contains the order's scope, which in turn must contain the proposed modification. Picturing the relationship as nested envelopes makes the trap visible — being within the parent IDIQ's broad scope is not necessarily enough. If the added work was not reasonably within the competed scope of the *existing order*, the Government may need to conduct another order competition among the eligible holders or otherwise justify a noncompetitive action, even though the work would have fit comfortably within the parent vehicle as a whole.

### The scope factors

Scope is not determined merely by matching a Product Service Code, a North American Industry Classification System (NAICS) code, a program name, or a broad phrase such as "engineering support"; two actions can share all of those labels and still differ in scope. The factors that bear on whether added work is within scope include the change in the type or purpose of the work; the change in quantity or required outcome; the change in period of performance; the magnitude of the price increase; any geographic or organizational expansion; the skills and resources required; whether the original solicitation warned offerors about the possible change; whether the original competitors reasonably could have anticipated it; and whether the change would have attracted a materially different field of competitors. Air Force acquisition rules at DAFFARS 5343.102-90 direct contracting officers to document scope determinations and to consider expressly the changes in the work, the performance period, and the cost, together with whether the change was reasonably anticipated and how it affects the field of competition.[^c10-scope]

### Who decides whether it is in scope

Operationally, the **contracting officer** makes or adopts the scope determination. The program office and engineers supply the technical facts about what is changing, while agency counsel, competition advocates, and other reviewers may advise or concur, but only a contracting officer acting within delegated authority may execute the modification. That label is not final in an absolute sense. The Government Accountability Office (GAO) or the Court of Federal Claims may review an allegedly out-of-scope order or modification in a bid protest; a board of contract appeals or the Court of Federal Claims may address scope in a contract dispute; and auditors or inspectors general may examine the transaction afterward. Current FAR Part 16 expressly preserves an order protest on the ground that an order increased the parent contract's scope, period, or maximum value — one of the narrow grounds on which order placements remain protestable, as described in [Indefinite-delivery contracts](06-indefinite-delivery-contracts.md). The several distinct meanings of contracting "authority," and the limits of a warranted contracting officer's power, are developed in [Contracting authority and who makes the award](17-contracting-authority-and-award-decisions.md).

## Governing principle: necessary but not sufficient

The clocks and the scope envelopes converge on a single rule that recurs throughout this reference: **"in scope" is necessary, but not sufficient.** A contract action that fits within both the parent and the order scope may still be unlawful for an independent reason. To be valid, the action must also be timely — taken while the relevant ordering or option clock is open — within the maximum ceiling, properly competed or justified where competition is required, funded from a legally available appropriation, and executed by a contracting officer acting within delegated authority. Each of those is a separate dimension, and a defect in any one of them is enough to defeat the action no matter how clearly the work falls within the contract's scope. The matched distinction between number-of-holders and absence-of-competition that underlies the competition requirement is developed in [Single-award, single-source, and sole-source](16-single-award-and-sole-source.md).

[^c10-deviation]: Department of Defense class deviation adopting the Revolutionary FAR Overhaul rewrite of FAR Part 16, effective March 16, 2026; the rewritten Part 16 sets out the required contents of an indefinite-delivery contract (ordering period, options, minimum and maximum, general scope, authorized ordering activities, and last delivery date) and of each order. <https://www.acquisition.gov/sites/default/files/page_file_uploads/DoD_RFO_Deviation_Part-16.pdf>; deviation text at <https://www.acquisition.gov/far-overhaul/far-part-deviation-guide/far-overhaul-part-16>.
[^c10-clause]: FAR 52.216-22, Indefinite Quantity. The clause provides that an order issued during the effective period of the contract and not completed within that period shall be completed by the contractor within the time specified in the order, and that the contract governs the contractor's and Government's rights and obligations with respect to that order to the same extent as if completed during the effective period. <https://www.acquisition.gov/far/52.216-22>.
[^c10-part43]: Revolutionary FAR Overhaul, Part 43 deviation guide, governing contract modifications under the current DoD class deviation. <https://www.acquisition.gov/far-overhaul/far-part-deviation-guide/far-overhaul-part-43>.
[^c10-scope]: DAFFARS 5343.102-90, Contract Scope Considerations, directing Air Force contracting officers to document scope determinations and to consider changes in the work, performance period, and cost, whether the change was reasonably anticipated, and the effect on the field of competition. <https://www.acquisition.gov/daffars/5343.102-90-contract-scope-considerations>.
