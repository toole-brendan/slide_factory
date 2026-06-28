---
title: Prime contracting, subcontracting, teaming, and first-tier reporting
---

# Prime contracting, subcontracting, teaming, and first-tier reporting

Most defense work is performed not by a single company but by a chain of them: a federal agency contracts with a **prime contractor**, the prime contracts with **subcontractors**, and those subcontractors may in turn contract with firms below them. This chapter develops the **performance chain**, the **legal relationship**, and part of the **data-classification** dimensions introduced in [The dimensions of a federal contract](01-dimensions-of-a-federal-contract.md): who actually performs the work, who holds a contract with whom, and how the lower tiers appear in public data. Its organizing legal idea is **privity of contract** — the Government's contractual relationship normally runs only to the prime — from which follow the rules on responsibility, payment, and claims; how prime-contract clauses "flow down"; how a firm that does not hold a vehicle can still enter the chain; what rights in technical data and software pass with the work; and how first-tier subcontracts are reported in public spending data. Two errors recur and the chapter guards against both: treating a named subcontractor as a direct federal contractor, and treating the single word **subaward** — which carries two distinct legal meanings and labels an instrument that is not legally an "award" at all — as though it named one thing.

## The contracting chain

A federal acquisition typically forms a tiered chain. The agency awards a prime contract or task order; the prime forms first-tier subcontracts; and first-tier subcontractors may form second-tier subcontracts. Running alongside that vertical chain, the prime also makes ordinary supplier and vendor purchases that support performance. The structure can be drawn as follows.

```text
Federal agency
│
└── Prime contract or task order  ← Government privity stops here
       │
       ├── First-tier subcontract
       │      │
       │      └── Second-tier subcontract
       │
       └── Supplier / vendor purchase order
```

The term **subcontract** is defined broadly: under FAR 44.101 it includes any contract or purchase order entered into by a subcontractor to furnish supplies or services for the performance of a prime contract or a higher-tier subcontract, so the definition reaches well beyond the first tier and captures purchase orders, not only formal contracts.[^c12-far44] As [the core vocabulary](02-core-vocabulary.md) notes, a subcontract is a real contract, but one between private parties rather than with the Government.

## Privity of contract and its four consequences

**Privity of contract** is the direct contractual relationship between two parties. In the normal arrangement the Government has privity with the prime contractor and not with any subcontractor, even a subcontractor performing the bulk of the work. Four consequences follow, and together they explain much of how the chain behaves.

- **Responsibility runs to the prime.** The prime is responsible for delivering the Government's requirement. Performance failures by a subcontractor are, as between the prime and the Government, the prime's problem to manage and cure; the agency looks to the prime, not to the firm that actually fell short.
- **Payment runs through the prime.** The prime normally pays its subcontractors out of what it receives, rather than the Government paying subcontractors directly. The flow of money tracks the contractual chain.
- **Claims run against the prime.** A subcontractor ordinarily submits contractual claims against the prime, not directly against the Government, because it has no contract with the Government on which to sue. Mechanisms by which a prime sponsors a subcontractor's claim against the Government exist but are the exception, not the rule.
- **Consent does not create a prime relationship.** Government approval of, or consent to, a subcontract does not ordinarily turn the subcontractor into a prime contractor. Consent (discussed below) is a control over the prime's purchasing decisions; it is not the award of a new prime contract and does not establish Government privity with the subcontractor.

These consequences are why the same work can be described as performed "by" a well-known subcontractor while the contract, the obligation, and the delivery responsibility all sit with a prime the public may never hear of. The distinction also underlies the warning in [the core vocabulary](02-core-vocabulary.md) against treating a named subcontractor as a direct federal contractor.

## When subcontractors enter

Subcontractors do not all appear at one moment. They can enter the structure at six distinct points across the life of an acquisition, and the point of entry affects what, if anything, the subcontractor is promised.

1. **Before the prime solicitation.** Companies position themselves by establishing **teaming agreements** or nondisclosure agreements in anticipation of a requirement, before the Government has issued a solicitation.
2. **In the prime proposal.** The offeror identifies key subcontractors and describes the proposed workshare, capabilities, labor, and costs as part of its proposal to the Government.
3. **At parent-vehicle award.** On award of a parent vehicle — for example an indefinite-delivery indefinite-quantity (IDIQ) contract — the prime establishes long-term subcontracts intended to support future orders rather than any single deliverable.
4. **During an order competition.** When competing for a specific task or delivery order, the prime adds specialists assembled specifically for that order. Order-level competition under indefinite-delivery vehicles is described in [Indefinite-delivery contracts](06-indefinite-delivery-contracts.md).
5. **During performance.** As the work proceeds, the prime purchases materials, services, or specialized work that the contract requires.
6. **Through lower tiers.** First-tier subcontractors themselves purchase work from other firms, extending the chain downward to second and lower tiers.

A recurring misconception attaches to the second point. A company named as a "team member" in a proposal is **not automatically guaranteed a subcontract**. Whether that company actually receives work depends on the private teaming agreement or subcontract agreement creating an obligation; being listed in a winning proposal, by itself, does not. This matters when a parent vehicle is later used to place orders, because the long-term subcontracts formed at award (the third point) and the order-specific specialists added later (the fourth point) may be entirely different firms.

## Teaming and the entry choices for a non-holder

The points of entry above also describe the routes by which a firm that cannot, or does not, win a prime contract on its own still reaches federal work. A firm that does not hold a relevant vehicle has, in practice, a bounded menu of choices:

- **Win as a prime** on an open-market competition or by qualifying for the applicable vehicle.
- **Join a vehicle through an on-ramp** — taking a holder's seat when a multiple-award vehicle adds holders, as described in [IDV, IDIQ, MAC, GWAC, and Schedules](07-idv-idiq-mac-gwac-schedules.md).
- **Team with an existing holder**, contributing to the holder's proposal and performance under a teaming arrangement.
- **Subcontract to the likely prime**, supplying a defined scope one tier below the prime contract.
- **Sell a separable component or capability** that the Government or a prime can adopt without displacing the wider integration.

Two cautions govern this menu. First, a **teaming arrangement is a private contract**: a contractor team arrangement or teaming agreement binds the parties to each other on the terms they negotiate, and — as the six points of entry establish — being named on a winning team does not by itself guarantee a subcontract or a fixed share of the work. Second, **vehicle access can be the binding constraint** rather than capability: where a requirement will be competed only among the holders of a particular multiple-award contract, a non-holder must secure a seat, qualify under another vehicle, or take one of the teaming or subcontract routes above before technical merit can matter at all. How heavily that access constraint weighs on a given pursuit is the **addressability** question developed in [Recompetes and opportunity intelligence from awards data](05-recompetes-and-opportunity-intelligence.md); the limiting case of a closed holder set is the single-award vehicle treated in [Single-award, single-source, and sole-source](16-single-award-and-sole-source.md).

## Flowdown clauses

Some clauses in a prime contract must be included in applicable subcontracts. Such clauses are called **flowdowns**. The mechanism allows the Government to extend selected obligations down the chain even though it has no privity with the lower-tier firms: the obligation is carried by the prime's contract with its subcontractor, which the prime is directed to write in.

A central and frequently missed point is that **not every prime-contract clause automatically flows down**. Whether a particular clause must appear in a given subcontract depends on several variables:

- the **value** of the subcontract;
- the **tier** of the subcontract (first-tier, second-tier, and so on);
- whether the subcontract is for a **commercial product or commercial service**;
- the **place of performance**;
- the **type of data or system access** involved;
- whether **classified or controlled information** is implicated;
- **domestic-source** rules; and
- the exact **prescription or wording** of the clause itself, which states where and how far it flows.

Because applicability turns on these factors, the set of clauses that flows into a $20,000 commercial purchase order differs sharply from the set that flows into a large, non-commercial, first-tier subcontract with system access. In DoD subcontracting, flowdowns commonly implicate cybersecurity and safeguarding requirements, data rights, specialty metals, Buy American and Berry Amendment domestic-source rules, counterfeit-parts controls, audit rights, cost or pricing data, and contractor business-system requirements. Several of these obligations ride along with the kinds of long-running production contracts treated in [Multiyear procurement and major weapon production](11-multiyear-procurement-and-production.md) and survive into [contract modifications](14-contract-modifications.md).

## Government rights in technical data and software

One flowdown subject is consequential enough to treat on its own: rights in **technical data** and **computer software**. The Government does not automatically own what a contractor develops; what it obtains is a *license* of defined scope, and the scope turns on who funded the development. The framework distinguishes **technical data** (recorded information of a scientific or technical nature) from **computer software**, and grades the Government's license — at orientation level — from **unlimited rights** (typically where development was funded entirely by the Government), through **government-purpose rights** (mixed funding, for a period), to **limited rights** in technical data and **restricted rights** in software (typically where development was funded entirely at private expense).[^c12-datarights]

Three practical points follow. First, **background intellectual property** — what a firm brings to the work, developed at its own expense — is treated differently from the deliverables produced under the contract, and the line between them is set by the contract and the funding source, not by who physically created the item. Second, **assertions and markings matter procedurally**: an offeror is generally required to identify, in or with its proposal, the technical data and software for which it asserts restrictions on the Government's rights, and a failure to assert in the required form can forfeit the restriction or even render an offer ineligible. Third, **data rights shape an incumbent's replaceability**: if the Government holds only limited or restricted rights in the data needed to recompete a requirement, a would-be successor cannot simply be handed the incumbent's drawings or software, which raises the transition barrier analyzed as part of addressability in [Recompetes and opportunity intelligence from awards data](05-recompetes-and-opportunity-intelligence.md). The same logic runs down the chain: an overly broad prime or teaming agreement can capture a subcontractor's background IP or its asserted rights, so the data-rights terms of a teaming arrangement deserve the same scrutiny as its workshare. The distinctive data-rights features of SBIR/STTR and Other Transaction work are noted in [Alternative acquisition pathways and "not a contract type" traps](18-not-a-contract-type-traps.md).

## What a procurement "subaward" legally is

For a federal procurement contract, the instrument that the transparency systems group under the heading *subaward* is legally a **first-tier subcontract award**. It is not a federal prime contract. It is a private contract between the prime contractor and the subcontractor, and the Government generally is not a party to it. The legal chain is best read as a sequence of distinct relationships:

```text
Federal agency
   │   prime contract  (Government ── prime contractor)
   ▼
Prime contractor
   │   first-tier subcontract  (prime ── subcontractor; Government not a party)
   ▼
Subcontractor
```

Because the FAR definition of *subcontract* reaches purchase orders and their modifications,[^c12-far44] the population of "subcontracts" under a prime contract is large and varied; only a subset of those subcontracts is ever *reported* under the transparency rules, a point developed below. The defining structural fact is that the subcontractor is not a direct federal contractor: the Government generally has privity of contract only with the prime, as the privity discussion above establishes. The general vocabulary distinction between a *subcontract* and a *subaward* is drawn in [The core vocabulary](02-core-vocabulary.md).

## The subcontract carries its own pricing arrangement

A first-tier subcontract has its own pricing arrangement, and that arrangement need not match the pricing type of the prime contract above it. The prime contractor and the subcontractor negotiate the subcontract's pricing between themselves, and because the Government generally is not a party to the subcontract, it is generally not a party to that pricing decision. The pricing arrangement on a subcontract may be any of the forms used in the wider acquisition system — **firm-fixed-price**, **cost-reimbursement**, **time-and-materials**, **labor-hour**, **fixed-price incentive**, a **purchase order**, a **long-term supplier agreement**, or a **negotiated commercial agreement** — and the choice is made on the merits of the supply relationship rather than dictated by the prime's own pricing type. The full taxonomy of pricing arrangements and the cost risk each allocates is the subject of [Pricing, commerciality, and cost risk](08-pricing-types-and-cost-risk.md).

The practical consequence is that the prime and the subcontract do not need to use the same pricing type, so a complete classification of a subcontract names both its own arrangement and the arrangement of the prime it supports. A correct classification might read: *a first-tier, firm-fixed-price subcontract supporting a cost-plus-incentive-fee prime contract.* The two pricing dimensions are independent. Reading a subcontract's pricing off the prime's pricing type — or assuming a fixed-price prime is performed entirely through fixed-price subcontracts — conflates two separately negotiated arrangements and is a frequent error.

## Four distinct subcontracting-compliance systems

A frequent error is to collapse "subcontracting compliance" into a single concept. There are at least four separate systems, each with its own authority, trigger, and purpose; they should never be merged.

### First-tier subaward reporting

The first system is **public-transparency reporting** of first-tier subawards under FAR 52.204-10 and related authorities.[^c12-far52204] It exists so that subcontract awards, not just prime awards, appear in public spending data. The reporting system was formerly the FFATA Subaward Reporting System (FSRS), which was retired on **March 8, 2025**; first-tier subaward reporting then moved to SAM.gov.[^c12-fsrs] This system is about disclosure, not goals or performance shares, and is treated in detail in the reporting sections below.

### Small-business subcontracting plans

The second system is the **small-business subcontracting plan**, the FAR Part 19 framework — specifically FAR Subpart 19.7 — for establishing and reporting small-business subcontracting goals.[^c12-1907] A plan is generally required when subcontracting possibilities exist, the prime is not itself treated as a small business for the requirement, and the value exceeds the applicable threshold (generally above **$900,000**, or **$2 million** for construction). The former eSRS reporting capability for these plans moved into SAM.gov in 2026. This is a goal-and-reporting system distinct from transparency reporting, and it is developed fully in [Small business in defense contracting](13-small-business.md).

### Consent to subcontract and purchasing-system review

The third system is **consent to subcontract** and **purchasing-system review** under FAR Part 44. Certain subcontracts require the contracting officer's consent before the prime may proceed, with the requirement depending on the contract type, the value, and whether the prime holds an approved purchasing system. A **Contractor Purchasing System Review (CPSR)** examines how the prime manages its purchases and subcontracts; a prime with an approved purchasing system faces consent requirements different from one without. As noted above, consent is a control over the prime's purchasing process and does not create Government privity with the subcontractor.

### Limitations on subcontracting

The fourth system is **limitations on subcontracting**, which apply to small-business set-asides and may require the small-business prime to perform a specified portion of the work itself.[^c12-219-14] Its purpose is to ensure that a set-aside actually benefits the small-business awardee rather than passing the work through to other firms. This is separate both from subcontracting-plan goals (the second system) and from first-tier transparency reporting (the first system): it constrains how much of the *prime's own* work may be subcontracted, rather than reporting subawards or setting aspirational goals. It is treated in full in [Small business in defense contracting](13-small-business.md).

Keeping these four apart is essential to reading a defense subcontract correctly. Transparency reporting discloses who received subawards; subcontracting plans set and report small-business goals; consent and CPSR govern whether and how the prime may subcontract at all; and limitations on subcontracting cap how much a set-aside prime may push outside its own walls. A single subcontract can sit inside several of these systems at once, in the same way that a single award occupies several dimensions at once, but each system answers a different question.

## What first-tier reporting captures

For procurement contracts the applicable reporting rule is the clause at **FAR 52.204-10**, which implements the **Federal Funding Accountability and Transparency Act (FFATA, Pub. L. 109-282)**, the statute behind first-tier subaward transparency reporting.[^c12-far52204] The rule focuses on **first-tier subcontracts** — those awarded directly by the prime contractor for the performance of the prime contract. It does not reach into the lower tiers of the supply chain, and it excludes certain general supplier arrangements that benefit multiple contracts or that are charged through general and administrative (G&A) or other indirect costs rather than booked directly to the one prime contract. The reporting question, in other words, is not "did the prime spend money with another company," but "did the prime award a first-tier subcontract, directly chargeable to this prime contract, of a kind the rule requires to be reported."

The following table illustrates how that test sorts a set of representative transactions. The right-hand column states whether each is normally reported as a first-tier subcontract.

| Transaction | Normally a reported first-tier subcontract? |
|---|---|
| Prime hires a company to design a subsystem for one federal contract | Yes, if reporting requirements apply |
| Prime buys specially manufactured components for that prime contract | Generally yes |
| Prime's major shipbuilding teammate performs 30% of the program | Yes |
| Prime buys ordinary office supplies used across the company | Generally no |
| First-tier subcontractor hires a second-tier subcontractor | Not normally reported as a first-tier award by the prime |
| Prime pays its employees | No |

Three patterns in the table are worth naming. First, work that is specific to the one prime contract — a designed subsystem, specially manufactured components, a teammate performing a substantial share of the program — is the heart of what first-tier reporting captures. Second, general inputs that are not specific to the contract, such as ordinary office supplies charged through indirect or G&A pools, generally fall outside first-tier reporting, as does paying the prime's own employees, which is not a subcontract at all. Third, the rule is explicitly *first-tier*: when a first-tier subcontractor in turn hires a second-tier subcontractor, that lower-tier award is not normally reported by the prime as a first-tier award. The reach of the rule is one level down from the prime, not the full depth of the supplier chain.

## The retirement of FSRS and the move to SAM.gov

The reporting just described was historically collected through the **FFATA Subaward Reporting System (FSRS)**, the system primes used to file first-tier subaward and subcontract reports. **FSRS was retired on March 8, 2025**, and the reporting function moved to **SAM.gov**, the System for Award Management.[^c12-fsrs] The migration did not change the underlying statutory obligation under FFATA or the substance of the FAR 52.204-10 reporting test; it changed the system through which the reports are filed and surfaced. The reporting obligation also survives the broader regulatory transition described elsewhere in this reference: the Department of Defense class deviation adopting the Revolutionary FAR Overhaul, effective March 16, 2026, rewrites FAR Part 16 and related parts but does not displace the first-tier subcontract reporting implemented under FAR 52.204-10.[^c12-deviation] The place of the resulting subaward record among the other federal data record types — and the rule that subaward values must not be commingled with prime obligations when totaling federal spending — is developed in [How awards appear in federal data](04-contract-data-systems.md).

In hosting the reporting, SAM.gov draws a clearer line than the legacy system between two kinds of report:

```text
SAM.gov first-tier reporting
   │
   ├── Subcontract Reports  ── associated with procurement contracts
   │                           (a first-tier subcontract under a prime contract)
   │
   └── Subaward Reports     ── associated with grants and other
                               financial-assistance awards
```

A **Subcontract Report** is associated with a procurement contract — that is, with a first-tier subcontract under a federal prime contract. A **Subaward Report** is associated with grants and other financial-assistance awards. The distinction matters because it maps directly onto the two legal meanings of *subaward* described next.

## The two meanings of "subaward"

The single word *subaward* is used for two different legal instruments, and keeping them apart resolves much of the confusion that surrounds the term.

In the **procurement context**, the chain runs from a federal prime contract to a first-tier subcontract:

```text
Federal prime contract
   └── first-tier subcontract   (legal instrument: a subcontract)
```

Here the legal instrument is a **subcontract**, even though USAspending and the legacy transparency systems sometimes group it under the broad heading *subaward*. The label is a transparency-data convention; the underlying instrument is governed by the FAR subcontract definition at FAR 44.101 and reported under FAR 52.204-10. Treating the subcontractor as a direct federal contractor because the data calls its subcontract a "subaward" is precisely the error the procurement meaning is meant to prevent.

In the **financial-assistance context**, the chain runs from a federal grant to an assistance subaward:

```text
Federal grant (to a prime recipient)
   └── assistance subaward      (to a subrecipient)
```

Here a **subaward** is a transfer of assistance from a prime recipient to a **subrecipient**. It is *not* a FAR procurement contract; it is a downstream flow of grant assistance, governed by the assistance framework rather than by the FAR's subcontracting rules. The instrument, the parties, and the governing rules all differ from the procurement case.

The recommended usage for the procurement meaning, which this reference adopts throughout, states the relationship plainly: a **procurement subaward** is a transparency-data label for a reported first-tier subcontract under a federal prime contract. Read that way, the term names a *report about* an instrument rather than a new federal award, and it never implies that the subcontractor holds a prime contract with the Government.

## The throughline

The reliable way to read this part of the structure is to keep three legal layers and four compliance systems apart. The **instrument** is a subcontract, not a federal prime contract, so the subcontractor is not a direct federal contractor and the Government generally lacks privity with it. The subcontract's **pricing arrangement** is negotiated between prime and subcontractor and is independent of the prime's pricing type, so a fixed-price subcontract can sit beneath a cost-reimbursement prime. And the **transparency label** — *subaward* in legacy systems, now resolved into SAM.gov's *Subcontract Reports* for procurement and *Subaward Reports* for financial assistance — is a reporting convention layered on top, capturing only first-tier subcontracts and excluding lower-tier awards and indirect or general supplier costs. Around those layers sit the four compliance systems — first-tier reporting, small-business subcontracting plans, consent and purchasing-system review, and limitations on subcontracting — each answering a different question, together with the teaming, entry, and data-rights choices that determine who joins the chain and on what terms. A relationship correctly assigned to its instrument, its pricing, its reporting layer, and its compliance systems is rarely misread; the words *subcontract* and *subaward* borrowed loosely across all of them almost always are.

[^c12-far44]: FAR 44.101, definitions, defining a *subcontract* as any contract entered into by a subcontractor to furnish supplies or services for the performance of a prime contract or a subcontract, and including a purchase order and modifications to a purchase order. <https://www.acquisition.gov/far/44.101>.
[^c12-datarights]: DFARS Subpart 227.71 (rights in technical data) and Subpart 227.72 (rights in computer software and computer software documentation), including DFARS 227.7103-5 and 227.7203-5 on the categories of Government rights (unlimited, government-purpose, limited, and restricted) and the contractor's obligation to identify and assert restrictions and to mark deliverables accordingly. <https://www.acquisition.gov/dfars/subpart-227.71-rights-technical-data> and <https://www.acquisition.gov/dfars/subpart-227.72-rights-computer-software-and-computer-software-documentation>.
[^c12-far52204]: FAR 52.204-10, Reporting Executive Compensation and First-Tier Subcontract Awards, the clause implementing the Federal Funding Accountability and Transparency Act of 2006 (FFATA, Pub. L. 109-282) for procurement contracts; it focuses reporting on first-tier subcontracts awarded by the prime for performance of the prime contract and excludes certain general supplier arrangements charged through indirect or general and administrative costs. <https://www.acquisition.gov/far/52.204-10>.
[^c12-fsrs]: SAM.gov, retirement of the FFATA Subaward Reporting System (FSRS) effective March 8, 2025, with first-tier subcontract and subaward reporting migrated to SAM.gov, which distinguishes Subcontract Reports (procurement contracts) from Subaward Reports (grants and other financial-assistance awards). <https://sam.gov/fsrs>.
[^c12-1907]: FAR Subpart 19.7, the Small Business Subcontracting Program, establishing small-business subcontracting plans and goal reporting; plan threshold generally above $900,000, or $2 million for construction. <https://www.acquisition.gov/far/subpart-19.7>.
[^c12-219-14]: FAR 52.219-14, Limitations on Subcontracting, requiring a small-business prime on a set-aside to perform a specified portion of the work. <https://www.acquisition.gov/far/52.219-14>.
[^c12-deviation]: Department of Defense class deviation adopting the Revolutionary FAR Overhaul, effective March 16, 2026; the deviation rewrites FAR Part 16 and related parts applied by DoD contracting officers but does not displace the first-tier subcontract reporting obligation implemented under FAR 52.204-10. <https://www.acquisition.gov/sites/default/files/page_file_uploads/DoD_RFO_Deviation_Part-16.pdf>.
