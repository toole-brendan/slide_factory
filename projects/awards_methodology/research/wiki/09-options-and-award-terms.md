---
title: Options and award terms
---

# Options and award terms

An **option** is a unilateral right the Government reserves in a contract to acquire additional supplies or services, or to extend a period, on terms already established — a right, not an obligation. It belongs to the **time** dimension of a federal award: it answers how future periods or quantities are *authorized*, separately from the questions of how the contractor is paid (the [pricing dimension](08-pricing-types-and-cost-risk.md)) and how money is *committed* (the funding dimension covered in [Awards, ceilings, obligations, and spending](03-awards-ceilings-obligations-spending.md)). The single most important property of an option is that, until it is exercised, it generally represents **potential rather than committed work**: an unexercised option is neither an obligation of funds nor a guarantee of any future order. This chapter sets out what an option is, the standard option clauses, the distinction between options held at the parent level and at the order level, the related but distinct concept of an **award term**, and the mechanics of *when* and *how* an option is exercised.

## What an option is

Under the FAR an option gives the Government the right — exercisable at its discretion — to purchase additional quantities of a supply, to extend services for a limited time, to extend the overall term of a contract, or to extend the ordering period of an indefinite-delivery indefinite-quantity (IDIQ) vehicle. In every case the defining features are the same. The right is the Government's alone; the contractor cannot compel its exercise. The terms — price or pricing method, quantity, and duration — are fixed in advance when the contract is awarded, so that exercising an option does not reopen a negotiation. And the right is contingent: it lapses if it is not exercised within the agreed window.

Because an unexercised option is only a reserved right, it is easy to overstate. An option period that has been priced but not exercised adds nothing to what the Government has obligated and nothing to what it is committed to buy; it is one of the several distinct numbers that the phrase "award amount" can hide, alongside the estimated value, the vehicle ceiling, the minimum guarantee, the obligation, and the outlay. Treating the full value of every priced option as though it were committed spending overstates the real commitment in the same way that adding a parent vehicle's ceiling to its child orders does, an error developed in [Awards, ceilings, obligations, and spending](03-awards-ceilings-obligations-spending.md).

## The standard option clauses

The FAR provides a small set of standard option clauses, each addressing a different kind of additional right. A contract may include more than one.

| Clause | Title | What it reserves |
|---|---|---|
| FAR 52.217-6 | Option for Increased Quantity | The right to buy additional units of an item, priced in the contract |
| FAR 52.217-7 | Option for Increased Quantity—Separately Priced Line Item | The right to buy additional quantity carried as its own separately priced line item |
| FAR 52.217-8 | Option to Extend Services | The right to extend services for a short additional period (generally up to six months) |
| FAR 52.217-9 | Option to Extend the Term of the Contract | The right to extend the overall term of the contract by adding option periods |

The quantity options (FAR 52.217-6 and FAR 52.217-7) operate on *what* is bought; the extension options (FAR 52.217-8 and FAR 52.217-9) operate on *time*. Because each option's price or pricing method is established in the clause, the line item, or the Schedule, an exercised option carries forward whatever [pricing type](08-pricing-types-and-cost-risk.md) the underlying line item used — a firm-fixed-price line item yields a firm-fixed-price option, and a cost-reimbursement line item yields a cost-reimbursement option.

Exercise of any of these clauses is not automatic. It normally requires that funds be available, that the requirement still exist, that the contractor have complied with the option terms, that notice be given in time, and that the contracting officer determine that exercising the option is in accordance with the contract and otherwise appropriate. Those preconditions are set out at FAR 17.207 and are developed below.[^c09-far17207]

## Parent-level options versus order-level options

A persistent source of confusion is that options can sit at two different layers of an indefinite-delivery structure, and the two are not interchangeable.

A **parent-level option** extends the parent contract's ordering period or other parent-level authority. For example, a five-year IDIQ may carry a five-year *optional* ordering period, so that exercising the option keeps the vehicle open to new orders for an additional span. An **order-level option** extends or adds work under a single task order or delivery order. A task order might have a one-year base and four one-year options of its own, even though the parent IDIQ has a different ordering structure entirely. The two layers are governed by their own clauses, their own funded values, and their own exercise dates.

```text
IDIQ parent contract
│   ordering period: 5-year base + 5-year option   ← parent-level option
│
├── Task Order 0001
│      1-year base + four 1-year options           ← order-level options
│
└── Task Order 0002
       1-year base + two 1-year options            ← order-level options
```

An order-level option is constrained by its parent. It must be authorized by the parent contract, fall within the parent's scope and maximum value, and be properly evaluated or otherwise supported. The relationship between a vehicle's ordering period and an order's own period of performance — including the question of whether an order option may be exercised after the parent's ordering period has closed — is treated in [Period of performance and scope](10-period-of-performance-and-scope.md), and the indefinite-delivery framework that supplies the parent authority is described in [Indefinite-delivery contracts](06-indefinite-delivery-contracts.md). The practical rule is to never assume the parent's option and a child order's option are the same thing: exercising one does nothing to the other.

## The award term as a distinct concept

An **award term** is an additional period of performance that the contractor *earns* by achieving specified performance results, rather than one the Government simply elects to take. It resembles an option operationally — it extends performance on pre-established terms — but its trigger is different: it rests on an award-term plan and defined performance criteria measured over the contract, so that strong performance is rewarded with additional time and weak performance forecloses it.

The award term is distinct on two sides. It is not an ordinary option, because an option is exercised at the Government's discretion subject to FAR 17.207 preconditions, whereas an award term is contingent on the contractor's measured results under the award-term plan. And it is not an **award fee**, which is monetary compensation paid for performance under a cost-plus-award-fee arrangement (one of the cost-reimbursement pricing arrangements discussed in [Pricing types and cost risk](08-pricing-types-and-cost-risk.md)); an award term pays in *time*, not money. Keeping the three apart — option, award term, award fee — avoids conflating a reserved right, an earned period, and a performance payment.

## When exactly is an option exercised

An option does not float free in time. There is a date, or an **exercise window**, within which the Government must act, and outside of which the right is gone. The controlling information is normally found in a definite set of places: the option clause itself; the contract or order Schedule; the applicable contract line item (CLIN); and any prior modification that has changed the dates. A reader trying to determine whether an option is still live must check all four, because a modification can move a window that the original Schedule set.

The mechanics are clearest in FAR 52.217-9, **Option to Extend the Term of the Contract**, which is written with blanks that the solicitation fills in. Three blanks matter:

- the period within which the Government must give the **actual written notice** that it is exercising the option;
- the number of days of **preliminary notice** of the Government's intent to exercise; and
- the **maximum total duration** of the contract, including all option periods.

The clause uses **60 days** as the default preliminary-notice period unless the solicitation inserts a different number.[^c09-far21709] The preliminary notice is a courtesy that lets a contractor anticipate continued performance, but it is expressly **not an exercise of the option** and does not commit the Government: a Government that sends the preliminary notice may still decline to exercise. The actual exercise is a separate, later act — typically a **unilateral modification** or other written notice signed by the contracting officer within the option-exercise window. Unilateral exercise is possible precisely because the terms were fixed at award; the modification mechanics are described in [Contract modifications](14-contract-modifications.md).

Before exercising, the contracting officer must make the pre-exercise determinations required by FAR 17.207. In substance the contracting officer must determine that funds are available; that the requirement still exists; that exercising the option is the most advantageous method of fulfilling that requirement (for example, advantageous compared with a new competition); that the contractor's performance has been acceptable; and that the option was properly evaluated and priced, or is otherwise determinable under the original contract terms.[^c09-far17207] Only a warranted contracting officer may sign the exercise, a point of authority developed in [Contracting authority and who makes the award](17-contracting-authority-and-award-decisions.md). The use of option periods on a single award is also conceptually distinct from a multiyear commitment, in which the Government commits across program years up front; that contrast is the subject of [Multiyear procurement and major weapon production](11-multiyear-procurement-and-production.md).

## What happens when a deadline is missed

Because the option right is bounded by its window, timing is not a formality. A **late purported unilateral option exercise is generally defective**: the Government cannot unilaterally exercise a right it failed to exercise within the agreed window, and an attempt to do so after the window has closed does not bind the contractor on the option terms. The right has simply lapsed.

The parties can sometimes respond by entering a **bilateral agreement** to continue performance, but such an agreement is not a retroactive option exercise. It is a newly negotiated modification, and it must independently satisfy the other dimensions that make any contract action valid: it must respect competition requirements, stay within scope, be executed by a contracting officer with authority, comply with fiscal law and funding availability, and observe any limitations imposed by the parent vehicle. This is a direct application of the principle that being *in scope* is necessary but never sufficient — an action must also be timely, competed or justified, funded, and properly authorized — set out in [Period of performance and scope](10-period-of-performance-and-scope.md).

Two related misconceptions are worth retiring. An option does not exercise itself merely because money was **budgeted** for the period; budgeting is not obligation, and an appropriation set aside in anticipation does not constitute the contracting officer's written exercise. Nor does an option exercise itself because the **contractor kept working**: continued performance after a window closes does not convert a lapsed option into an exercised one. In both cases what exists is, at most, the basis for a negotiated modification that must satisfy the validity tests on its own — not a "magical" retroactive exercise of the option.

[^c09-far17207]: FAR 17.207, Exercise of options — preconditions including availability of funds, continuing need, that exercise is the most advantageous method of fulfilling the requirement, acceptable contractor performance, and that the option was evaluated and priced or is otherwise determinable under the contract. <https://www.acquisition.gov/far/17.207>.
[^c09-far21709]: FAR 52.217-9, Option to Extend the Term of the Contract — fill-in clause stating the written-notice period, the preliminary-notice period (60 days unless another period is inserted), and the maximum total contract duration; the preliminary notice is not an exercise of the option. <https://www.acquisition.gov/far/52.217-9>.
