# Federal Awards & Subawards Data — A Practitioner's How‑To

A working guide to pulling and reading U.S. federal contract data from the free government APIs: **USAspending**, **SAM.gov Contract Awards**, **SAM.gov Subaward Reporting**, **SAM.gov Entity**, **SAM.gov Opportunities**, and the **FPDS Atom feed**. Written from hands‑on use — it leads with the mistakes that quietly produce wrong answers.

---

## 0. The one lesson that matters most

> **The "standard" contract feed silently drops Other Transactions (OTs/OTAs). If your market runs on OTs — as defense‑tech, autonomy, and prototyping increasingly do — a normal pull will report the biggest players as "$0 / absent," and you will believe it.**

Concretely: USAspending's `spending_by_award` filtered to `award_type_codes` A–D + IDV_* (the default contract/IDV universe) **does not return OTs at all**. A vendor with a $457M Navy Other Transaction Agreement can show up as zero awards. That is a *pull‑scope artifact*, not reality.

**The fix is one query, not three datasets:** the **SAM.gov Contract Awards API, filtered by `awardeeUniqueEntityId`**, returns a vendor's *complete* prime footprint — definitive contracts, IDVs, delivery/task orders, purchase orders, BPAs, **and** OT agreements/orders — in a single result. Always verify a "they have nothing" finding against SAM Contract Awards by UEI before believing it.

---

## 1. The mental model: four layers, each blind to different things

| Layer | What it is | Best source | Blind spots |
|---|---|---|---|
| **Pre‑award notices** | solicitations, sources‑sought, award notices | SAM **Opportunities** | exempt buys (FAR 16.5 orders, OTs) never appear; title‑only search; 1‑yr window |
| **Prime awards (standard)** | definitive contracts, IDVs, task/delivery orders | **USAspending** / FPDS | **excludes OTs**; cumulative‑dollar restatement traps |
| **Prime awards (complete, incl. OTs)** | everything above **plus** OT agreements/orders | SAM **Contract Awards** | DoD actions < 90 days old hidden on a non‑federal key |
| **Subawards** | first‑tier (FFATA) subcontracts | SAM **Subaward Reporting** | first‑tier only; 6–18 mo reporting lag; some primes file nothing |

No single layer is the market. "An opportunity" can be an open solicitation, a task order under an existing IDV, an OT under a consortium, a recompete 18 months out, or a subcontract under a prime — and the four layers see different ones.

---

## 2. Cross‑cutting setup (do this once)

- **API key (SAM only).** Free from sam.gov → Account Details → Public API Key (`SAM-xxxx…`). USAspending and FPDS need **no key**.
- **Quota tiers (per day, resets midnight UTC):** personal/no‑role **10**, account with a role on an employer's SAM entity **1,000**, federal system account **10,000**. Get the 1,000 tier before pulling anything real. **HTTP 429 = quota gone** — trap it, halt cleanly, resume next day.
- **macOS: force IPv4.** On networks with broken IPv6, `api.sam.gov` hangs ~225 s/request. Monkeypatch `socket.getaddrinfo` to `AF_INET` at process start. This is the single biggest perf gotcha.
- **Make every pull resumable.** Write one file per PIID/UEI/award; skip‑if‑exists on rerun. Process **biggest‑dollar‑first** so a mid‑run 429 still leaves you the material records.
- **Be immune to agency renames.** Key scoping and joins off **sub‑tier names + UEI**, never the top‑tier department name (e.g. a "Department of Defense → Department of War" rename breaks any top‑tier filter; sub‑tier "Department of the Navy" keeps working).
- **Keep raw.** Persist the full native record (every field) in a raw tier; derive thin indices separately. You will always discover you need a field you didn't extract.

---

## 3. USAspending — discovery + per‑mod detail (free, no key)

Base: `https://api.usaspending.gov/api/v2`. JSON. Clean **phrase** matching on keywords (unlike FPDS). Best for *discovering* a market and for *authoritative per‑mod dollars*.

### 3a. Discovery — `POST /search/spending_by_award/`
Find the candidate award universe by keyword and/or NAICS/PSC.

```jsonc
{
  "filters": {
    "time_period": [{"start_date":"2015-01-01","end_date":"2026-12-31"}],
    "award_type_codes": ["A","B","C","D"],          // contracts ONLY in this call
    "keywords": ["unmanned surface vessel"],         // OR: "naics_codes":["336612"], "psc_codes":["1940"]
    "recipient_search_text": ["SARONIC"]             // OR scope by recipient
  },
  "fields": ["Award ID","Recipient Name","Award Amount","Awarding Sub Agency",
             "Start Date","End Date","NAICS","PSC","Description"],
  "sort": "Award Amount", "order": "desc", "limit": 100, "page": 1
}
```
- **You cannot mix contract codes (A–D) and IDV codes (`IDV_A…IDV_E`) in one call → HTTP 422.** Query the two groups separately and union by `generated_internal_id`.
- **`award_type_codes` has no OT option here → OTs are invisible to this endpoint.** (See §4 / §0.)
- Returns `generated_internal_id` — the handle for every detail call below. 100/page; results are capped (~the top‑N by your sort), so **scope tightly** (by sub‑tier agency, NAICS, or keyword) so the cap doesn't silently truncate the tail you care about.
- NAICS/PSC come back as objects (`{"code":"336612","description":"…"}`), not bare strings.

### 3b. Detail — three sub‑resources per award
For each `generated_internal_id`:
- `GET /awards/{id}/` → recipient + **UEI**, parent IDV linkage, `period_of_performance` (start/current‑end/**potential‑end**), `total_obligation`, `base_and_all_options` (ceiling), `base_exercised_options` (current value), `subaward_count`/`total_subaward_amount`, and `latest_transaction_contract_data` (which carries **`solicitation_identifier`**, `extent_competed`, `fair_opportunity_limited`, `number_of_offers_received`, `solicitation_procedures_description`).
- `POST /transactions/` (paged) → **one row per modification**; `federal_action_obligation` is the **per‑mod obligation** and `action_date` is the timestamp. This is the only dollar field you sum (see §7).
- `POST /awards/funding/` (paged) → Treasury Account Symbol (`federal_account`) → appropriation tie‑back. Zero rows is normal (orders often report under the parent).

> `number_of_offers_received: 999` is a **sentinel for "not meaningful"** (schedule/IDV actions), not a literal count.

---

## 4. SAM.gov Contract Awards — the complete prime feed (key required)

Base: `https://api.sam.gov/contract-awards/v1/search`. The modern FPDS replacement. **This is the only prime source that includes OTs.** Use it as your default for "what has vendor/agency/market X actually been awarded."

### 4a. Filters — what works and what lies
| Param | Behavior |
|---|---|
| **`awardeeUniqueEntityId`** | ✅ **Reliable.** The workhorse. Returns that UEI's complete footprint incl. OTs. |
| `naicsCode`, `productOrServiceCode` | ✅ Work. Lists up to 100 values; `~` = OR inside a value. |
| `dateSigned`, `lastModifiedDate`, `dollarsObligated` | ✅ Work; ranges as `[lo,hi]` (`MM/DD/YYYY`). |
| `piid` (+ `piidAggregation`) | ✅ Works; **UPPERCASE, no dashes** (e.g. `N0002417C2100`). Dashed → HTTP 400. |
| **`q` (free text)** | ❌ **Useless as a filter** — OR‑tokenizes and returns the *entire* ~650k‑record dataset. |
| **`awardeeLegalBusinessName`** | ❌ **Does not filter** — also returns everything. Use the UEI instead. |
| `awardOrIDVType` | ⚠️ Finicky (code values 400'd in testing); prefer to pull broadly and classify the returned `awardOrIDVType.name` client‑side. |

Always **verify the filter was honored**: check that returned `totalRecords` is sane and (where you can) that records carry the UEI/code you asked for. A response of "the whole dataset" means your filter was silently dropped.

### 4b. Reading a record
`includeSections=contractId,coreData,awardDetails,awardeeData` trims the (large) payload. Per mod‑level record:
- `contractId`: `piid`, `modificationNumber`, `reasonForModification`, `subtier`.
- `coreData`: `awardOrIDV`, **`awardOrIDVType.{code,name}`** (e.g. `OTHER TRANSACTION AGREEMENT`, `DELIVERY ORDER`, `FSS`, `IDC`), `solicitationId`, `federalOrganization…contractingOffice.code`.
- `awardDetails.dates`: `dateSigned`, **`lastDateToOrder`** (IDV ordering‑period end = the recompete clock), `currentCompletionDate`, `ultimateCompletionDate`, `periodOfPerformanceStartDate`.
- `awardDetails.dollars.actionObligation` = **this mod's** obligation; `awardDetails.totalContractDollars.{totalActionObligation, totalBaseAndAllOptionsValue}` = **cumulative** + **ceiling**.
- `awardeeData` is frequently **empty in search responses** — don't rely on it to confirm identity; rely on the UEI filter.

### 4c. Family rollups — `&piidAggregation=yes` (with `&piid=`)
One call returns the award *family*: `piidAggregation.awardFamilySummary.{count,totalDollars}` plus, for an IDV, `referencingDosOrBpaCallsSummary` (the task/delivery orders under it). The fastest "how big is this whole vehicle" answer and the way to hydrate an IDV's ordering‑period end + ceiling.

### 4d. Bulk Extract (async) — for whole‑market pulls
Add `format=csv|json` **and** `emailId=Yes|No` **together** (sending one without the other 400s). You get a `presignedUrl` containing `REPLACE_WITH_API_KEY`; substitute your key and GET it; early polls 303→S3 404 = file still generating → poll until the ZIP (`PK…`) arrives (~1–2 min). Up to 1M records, mod‑level → **group by `piid`** for base contracts.

### 4e. The DoD 90‑day rule
On a non‑federal key, **DoD actions signed < 90 days ago are hidden** ("Revealed" vs "Unrevealed"). For recent awards, backstop with USAspending (no 90‑day rule). Never call a < 90‑day‑old award "absent."

---

## 5. SAM.gov Subaward Reporting — first‑tier FFATA (key required)

Base: `https://api.sam.gov/prod/contract/v1/subcontracts/search` (**keep `/prod/`** — docs omit it → 404). This is where "who actually builds it under the prime" lives.

- **Params:** `piid` (**UPPERCASE, no dashes**), `agencyId`, and for task orders also `referencedIDVPIID` (+ `referencedIDVAgencyId`) so a generic order number like `0001` doesn't paginate the whole dataset. `pageSize=1000`, **zero‑indexed `pageNumber`**, `status=Published` (run `Deleted` separately for an audit trail).
- **Verify the filter:** the first page's `nextPageLink` must echo `piid=`; if it doesn't, the filter was dropped → re‑check casing before concluding "no subs."
- **Stop condition (infinite‑loop trap):** `nextPageLink` is **non‑null even at 0 records** (it points back to page 0). Stop on an **empty page, a short page (< pageSize), or `pageNumber+1 ≥ totalPages`** — not on "nextPageLink is null."
- **Useful fields:** `subAwardAmount` (string — coerce), `subAwardDate` (use for FY), **`submittedDate`** (the *reporting* date — use this for lag, not subAwardDate), `subEntityLegalBusinessName`, `subEntityUei`, **`subParentUei`** / `subEntityParentLegalBusinessName` (roll up to corporate parent), `subBusinessType`, `subawardDescription`, `primeNaics`, `primeEntityUei`. `subAwardReportId` is unique → no dedup needed.
- **Always caveat:** first‑tier only, **6–18 month reporting lag**, and some primes file nothing → treat totals as a **floor, not a census**. Triangulate against USAspending `subaward_count`/`total_subaward_amount` to flag under‑reporters. Never assert "prime X has no subs" — assert "no *reported* subs as of pull date."

---

## 6. SAM.gov Entity & Opportunities

### 6a. Entity — `…/entity-information/v3/entities` (key)
Resolve a name → UEI(s) and enrich a UEI → NAICS/CAGE/business types. `includeSections=entityRegistration,coreData`.
- **A company often has several UEIs** (registrations for different divisions/addresses). Searching `legalBusinessName` can return 5+ `entityData[].entityRegistration.ueiSAM`. **Query each UEI** when pulling that company's awards/subawards, or you'll miss part of its footprint.

### 6b. Opportunities — `…/opportunities/v2/search` (key)
Pre‑award notices (pre‑sol, solicitation, sources‑sought, award notice). `title=`, `ncode=` (NAICS), `ccode=` (PSC), `postedFrom`/`postedTo`.
- **Max 1‑year window** per call. **`title` searches titles only** (no description search). **`postedDate` = last‑modified**, not original post date. `status=Archived` 500s server‑side. The description field is a URL needing a second fetch. ~60 s/call regardless of size.
- It is a **notice** stream, not an opportunity radar: much real buying (FAR 16.5 orders, OTs, sole‑source) **never appears here at all.**

---

## 7. Money hygiene — the three universes (never blend them)

Three different dollar measures live on every award; summing across them, or summing a cumulative field across mods, is the most common way to produce a wrong market size.

1. **Per‑mod obligation** — `actionObligation` (SAM CA) / `federal_action_obligation` (USAspending). **This is the only field you sum across modifications** to get realized spend.
2. **Cumulative‑to‑date** — `totalActionObligation` / `total_obligation`. A *restated snapshot* repeated on every mod. **Never sum across mods** (you'll multiply‑count).
3. **Ceiling** — `totalBaseAndAllOptionsValue` / `base_and_all_options`. Maximum capacity of the vehicle, **not money spent.** A multiple‑award IDIQ's ceiling is shared across all holders and can be enormous (e.g. a $151B program‑level IDC ceiling is the *program's*, not one vendor's slice). Use ceilings to gauge headroom, never as spend.

Define the **family** as your dedup unit (parent‑IDV PIID for task/delivery orders; the PIID for standalones) so a task order's dollars are never counted both standalone and inside its IDV. When USAspending and SAM CA/FPDS disagree, the **FPDS‑lineage source (SAM CA / FPDS) is authoritative** (USAspending is derived from it).

---

## 8. Identifiers & joins

- **PIID** — contract/order id. Normalize to **UPPERCASE, no dashes** for SAM APIs.
- **UEI** — 12‑char entity id; the most reliable vendor key. Resolve via Entity API; expect **multiple per company**.
- **`generated_internal_id`** (USAspending) — the handle for detail calls; encodes type + PIID + agency + parent (`CONT_AWD_{PIID}_{AG}_{REFIDV}_{REFAG}`).
- **`referencedIdvPiid` / parent IDV** — links a task/delivery order to its vehicle; the unit for recompete and concentration analysis.
- **Solicitation number ↔ award.** To bridge an award to its pre‑award notice, match the award's `solicitationId` / `solicitation_identifier` to the opportunity's `solicitation_number`. **Normalize both: uppercase, strip every non‑alphanumeric, and split compound notice numbers on `-`** (e.g. `N66001_25_R_0024` → `N66001250024`; `70Z0…-70Z0…` → two keys). Calibrate the key on known award‑notice PIIDs before trusting "no match = no notice."

---

## 9. Reading timing: the recompete clock

The recompete clock is the **vehicle's** end, not the latest child order's end:
- IDV → **`lastDateToOrder`** (ordering‑period end).
- Standalone contract → `currentCompletionDate` / `ultimateCompletionDate` (potential end).
- OT → agreement‑specific; validate externally.

And **"expired ≠ addressable."** Before treating an expiring vehicle as an opportunity, apply two gates: **successor** (has a follow‑on already been awarded? check the universe for a later PIID under the same parent / office+NAICS) and **access** (is it a single‑ or multiple‑award vehicle, `fair_opportunity_limited`? — i.e. open bid vs holders‑only, where the route is an on‑ramp or a subcontract, not a proposal). PoP end dates are **indicators**, not guaranteed recompete dates.

---

## 10. Recipes

**A. A vendor's (or competitor's) complete federal footprint.**
Entity API by name → UEI(s) → **SAM Contract Awards by `awardeeUniqueEntityId`** for each UEI → group by `piid`, classify `awardOrIDVType`. *This one query returns OTs + conventional + schedules together.* (Don't rely on USAspending alone — it drops the OTs.)

**B. Size a market.**
USAspending discovery by NAICS/PSC/keywords (A–D and IDV separately) → **tier it** (the headline NAICS often hides the real segment: e.g. NAICS 336611 under the Navy is dominated by capital ships, and PSC 1905 includes submarines — the clean small‑craft/USV cut is **336612 + PSC 1940 + autonomy keywords**). Sum **per‑mod obligations** by tier. Add the **OT layer** (SAM CA by the known players' UEIs) or the whole market via NAICS Extract — markets with heavy OT activity are undersized without it.

**C. Recompete radar (12–36 mo of lead time).**
From detail, group awards into vehicles (parent IDV or PIID); take each vehicle's `lastDateToOrder`/potential‑end as the clock; keep those landing in your horizon with sustained obligation; apply the successor + access gates (§9); flag which have **no** pre‑award notice yet. That list is forward pipeline the Opportunities portal won't show for months.

**D. Supply‑chain / teaming map.**
SAM Subawards for the market's top primes (biggest‑obligation‑first) → roll subs up by `subParentUei` → find **recurring suppliers** (serve ≥2 primes = the established supply chain) and **integrators who sub the work out** (teaming targets). Caveat as a floor (§5).

**E. Measure how incomplete the Opportunities portal is.**
(i) *Structural:* the share of award dollars flowing via **FAR 16.5 task/delivery orders** (parent‑IDV present) and **OTs** — synopsis‑exempt by law, so the portal *can't* show them. (ii) *Empirical:* of awards signed **inside** the portal's posting window, the share with **no** matching notice (normalize + match per §8; verify a sample by hand so you're measuring darkness, not a broken join).

---

## 11. Gotcha quick‑reference

- USAspending A–D/IDV pull **omits OTs** → false "$0 absent." → SAM Contract Awards by UEI.
- USAspending: **can't mix A–D with IDV codes** in one call (422). Query separately.
- SAM CA `q` and `awardeeLegalBusinessName` **don't filter** (return everything). Use `awardeeUniqueEntityId` / NAICS / PSC / piid.
- SAM CA **`awardeeData` often empty** in search → confirm identity by the UEI filter, not the name field.
- SAM CA **DoD < 90‑day** actions hidden on a non‑federal key → backstop with USAspending.
- SAM Subawards: **`/prod/` required**, **PIID UPPERCASE no‑dash**, **0‑indexed pages**, **non‑null `nextPageLink` even at 0 records** (stop on empty/short/totalPages), verify `nextPageLink` echoes `piid=`.
- Subawards lag **6–18 mo** and are first‑tier only → a floor; gate point‑in‑time analyses on **`submittedDate`**, not `subAwardDate`.
- Opportunities: **1‑yr window**, **title‑only**, **`postedDate`=last‑modified**, Archived 500s.
- Money: sum **per‑mod** obligation only; **never** sum cumulative; ceiling ≠ spend; dedup by **family**.
- Vendors have **multiple UEIs** — query each.
- macOS: **force IPv4** or ~225 s/request hang on api.sam.gov.
- Scope/join off **sub‑tier + UEI**, never the top‑tier department name (rename‑proof).
- SAM key: **1,000/day** entity‑role; trap **429**, halt clean, resume; pull **biggest‑$ first**, **skip‑if‑exists**.

---

## 12. Which API answers which question

| Question | Go to |
|---|---|
| What has this vendor/competitor *actually* won (incl. OTs)? | **SAM Contract Awards by UEI** |
| What's in this market, by size/segment? | USAspending discovery → tier → + SAM CA OT layer |
| Per‑year spend / appropriation tie‑back? | USAspending transactions + funding |
| When does this vehicle recompete? | SAM CA `lastDateToOrder` (piidAggregation) |
| Who supplies the primes? | SAM Subaward Reporting |
| Name/UEI/NAICS of an entity? | SAM Entity |
| What's openly advertised right now? | SAM Opportunities (knowing it's a fraction of the truth) |
| Authoritative per‑mod action history (legacy cross‑check)? | FPDS Atom feed |

*The first row is the one people skip — and it's usually the one that changes the answer.*
