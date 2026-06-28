#!/usr/bin/env python3
"""STAGE 3 - AUTHORITATIVE PER-MOD ACTIONS (FPDS Atom feed).

USAspending (Stages 1-2) is the discovery + structure layer; FPDS is pulled here
for its one real strength: authoritative, per-modification contract actions with
exact obligated dollars and dates. Pulled BY VENDOR (the discovered roster), then
reconciled to our PIID set at aggregate time (FPDS wins on $ conflicts).

FPDS field reality (verified live 2026-06-20 — the May-2026 shipbuilding reference
is STALE here):
  * `VENDOR_NAME:"..."` is NO LONGER honored — FPDS silently drops it and returns
    the ENTIRE 17M-record feed. Use `VENDOR_UEI:"<uei>"` (primary; we have UEIs
    from Stage 2) or exact-phrase `VENDOR_FULL_NAME:"<name>"` (fallback).
  * `CONTRACTING_AGENCY_ID:"2100"` = Department of the Army AND captures USACE
    Engineer Districts (W071/W074/W07V/W2SD ENDIST...) AND TACOM watercraft
    (W4GG) — i.e. the full Army+USACE scope in ONE code. (`DEPARTMENT_*` filters
    don't resolve.) Keying off this CODE + UEI means the pull is immune to the
    DoD -> "Department of War" toptier rename (see memory).
  * Per-mod `obligatedAmount` is the sum-able field. NEVER sum `totalObligatedAmount`
    (cumulative -> double counts). We keep both; aggregate sums obligatedAmount.

Per project rule the RAW tier keeps the FULL native record: each action is stored
as the faithful `xml_to_dict` of its <award>/<IDV> element, alongside a flat header
for convenience + reconciliation.

Scope control: pull only vendors at/above a $ floor (default $1M summed
total_obligation from Stage 2). The dropped tail (tiny one-off USACE survey/dredge
awards) is already fully captured in USAspending; its size + dollars are LOGGED so
the cap is never silent.

Run:  python3 pull_fpds_actions.py                 # all vendors >= floor
      python3 pull_fpds_actions.py 12              # top 12 vendors (smoke)
      MIN_OBL=5000000 python3 pull_fpds_actions.py # raise the floor
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from urllib import parse
from urllib.request import Request, urlopen
from xml.etree.ElementTree import fromstring
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import slugify, write_json, xml_to_dict  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]            # research/contracts/
RAW = ROOT / "fpds_raw"
EXTRACT = ROOT / "extracted"
VENDORS = EXTRACT / "_vendors.json"
INDEX = EXTRACT / "_fpds_index.json"
LOG = ROOT / "pull_logs" / "fpds_actions.log"

NS = {"a": "http://www.w3.org/2005/Atom", "ns1": "https://www.fpds.gov/FPDS"}
BASE = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
HDRS = {"User-Agent": "army-usv-market-research/1.0 (where-to-play workbook)"}
ARMY_AGENCY = 'CONTRACTING_AGENCY_ID:"2100"'          # Army + USACE + TACOM (verified)
DATE_WINDOW = "SIGNED_DATE:[2015/01/01,2026/12/31]"   # matches Stage-1 discovery window
MIN_OBL = float(os.environ.get("MIN_OBL", "1000000"))
MAX_PAGES = 400
SLEEP = 0.35


def fetch(url, tries=4):
    for attempt in range(tries):
        try:
            with urlopen(Request(url, headers=HDRS), timeout=90) as r:
                return r.read().decode("utf-8")
        except Exception as e:
            if attempt == tries - 1:
                return None
            time.sleep(2 ** attempt)
    return None


def total_pages(xml_text):
    m = re.search(r'rel="last".*?start=(\d+)', xml_text)
    return (int(m.group(1)) // 10) + 1 if m else 1


def _f(elem, path):
    x = elem.find(path, NS)
    return x.text if x is not None and x.text else None


def _a(elem, path, attr):
    x = elem.find(path, NS)
    return x.get(attr) if x is not None else None


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def parse_entries(xml_text):
    """Yield (flat_header, full_native_dict) per award/IDV element."""
    try:
        root = fromstring(xml_text)
    except Exception:
        return []
    out = []
    for entry in root.findall("a:entry", NS):
        content = entry.find("a:content", NS)
        if content is None:
            continue
        award = content.find(".//ns1:award", NS)
        ot_award = content.find(".//ns1:OtherTransactionAward", NS)
        ot_idv = content.find(".//ns1:OtherTransactionIDV", NS)
        idv = content.find(".//ns1:IDV", NS)
        elem = award or ot_award or ot_idv or idv
        if elem is None:
            continue
        rtype = ("award" if award is not None else
                 "OtherTransactionAward" if ot_award is not None else
                 "OtherTransactionIDV" if ot_idv is not None else "IDV")
        piid = None
        for p in (".//ns1:awardContractID/ns1:PIID",
                  ".//ns1:OtherTransactionAwardContractID/ns1:PIID",
                  ".//ns1:OtherTransactionIDVContractID/ns1:PIID",
                  ".//ns1:IDVID/ns1:PIID"):
            piid = _f(elem, p)
            if piid:
                break
        ref_idv = _f(elem, ".//ns1:referencedIDVID/ns1:PIID")
        full_piid = f"{ref_idv}/{piid}" if (ref_idv and piid and ref_idv != piid) else piid
        flat = {
            "record_type": rtype,
            "piid": piid,
            "referenced_idv_piid": ref_idv,
            "full_piid": full_piid,
            "mod_number": _f(elem, ".//ns1:modNumber") or "",
            "transaction_number": _f(elem, ".//ns1:transactionNumber"),
            "vendor_name": _f(elem, ".//ns1:vendorName"),
            "vendor_uei": _f(elem, ".//ns1:UEI") or _f(elem, ".//ns1:vendorUEIInformation/ns1:UEI"),
            "this_obligated": _num(_f(elem, ".//ns1:obligatedAmount")),            # SUM this
            "total_obligated": _num(_f(elem, ".//ns1:totalObligatedAmount")),      # do NOT sum
            "base_and_exercised": _num(_f(elem, ".//ns1:baseAndExercisedOptionsValue")),
            "base_and_all_options": _num(_f(elem, ".//ns1:baseAndAllOptionsValue")),
            "total_base_and_all_options": _num(_f(elem, ".//ns1:totalBaseAndAllOptionsValue")),
            "signed_date": _f(elem, ".//ns1:signedDate"),
            "effective_date": _f(elem, ".//ns1:effectiveDate"),
            "current_completion_date": _f(elem, ".//ns1:currentCompletionDate"),
            "ultimate_completion_date": _f(elem, ".//ns1:ultimateCompletionDate"),
            "contracting_agency": _a(elem, ".//ns1:contractingOfficeAgencyID", "name"),
            "contracting_office": _a(elem, ".//ns1:contractingOfficeID", "name"),
            "contracting_office_id": _f(elem, ".//ns1:contractingOfficeID"),
            "funding_agency": _a(elem, ".//ns1:fundingRequestingAgencyID", "name"),
            "funding_office": _a(elem, ".//ns1:fundingRequestingOfficeID", "name"),
            "naics": _f(elem, ".//ns1:principalNAICSCode"),
            "naics_desc": _a(elem, ".//ns1:principalNAICSCode", "description"),
            "psc": _f(elem, ".//ns1:productOrServiceCode"),
            "psc_desc": _a(elem, ".//ns1:productOrServiceCode", "description"),
            "contract_action_type": _a(elem, ".//ns1:contractActionType", "description"),
            "pricing_type": _a(elem, ".//ns1:typeOfContractPricing", "description"),
            "extent_competed": _a(elem, ".//ns1:extentCompeted", "description"),
            "solicitation_procedures": _a(elem, ".//ns1:solicitationProcedures", "description"),
            "number_of_offers": _f(elem, ".//ns1:numberOfOffersReceived"),
            "description": (_f(elem, ".//ns1:descriptionOfContractRequirement") or "")[:1000],
        }
        out.append((flat, xml_to_dict(elem)))   # full native record kept per rule
    return out


def paginate(q, log):
    """Return deduped list of {**flat, 'raw': full_dict} for a query."""
    records, seen, start, tp, fetched = [], set(), 0, None, 0
    while True:
        url = f"{BASE}&{parse.urlencode({'q': q})}&start={start}"
        text = fetch(url)
        if text is None:
            log(f"      FETCH FAIL at start={start}")
            break
        if tp is None:
            tp = total_pages(text)
            log(f"      ~{tp} pages for: {q[:90]}")
            if tp > MAX_PAGES:
                log(f"      !! capping at {MAX_PAGES} pages (vendor has more Army actions than expected)")
        entries = parse_entries(text)
        if not entries:
            break
        for flat, full in entries:
            sig = (flat.get("full_piid") or flat.get("piid"),
                   flat.get("mod_number"), flat.get("transaction_number"), flat.get("signed_date"))
            if sig in seen:
                continue
            seen.add(sig)
            rec = dict(flat)
            rec["raw"] = full
            records.append(rec)
        fetched += 1
        start += 10
        if start // 10 >= min(tp, MAX_PAGES):
            break
        if fetched % 25 == 0:
            log(f"      ...{fetched} pages, {len(records)} records")
        time.sleep(SLEEP)
    return records


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    logf = open(LOG, "w")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    vendors = json.loads(VENDORS.read_text())
    vendors.sort(key=lambda v: -(v.get("total_obligation") or 0))
    top_n = int(sys.argv[1]) if len(sys.argv) > 1 else None

    selected = [v for v in vendors if (v.get("total_obligation") or 0) >= MIN_OBL]
    if top_n:
        selected = vendors[:top_n]
    dropped = [v for v in vendors if v not in selected]
    dropped_oblig = sum(v.get("total_obligation") or 0 for v in dropped)

    log(f"=== FPDS actions (Stage 3) {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"vendors total={len(vendors)}  selected={len(selected)} (floor=${MIN_OBL/1e6:.1f}M"
        f"{f', top_n={top_n}' if top_n else ''})  scope={ARMY_AGENCY} {DATE_WINDOW}")
    log(f"DROPPED tail: {len(dropped)} vendors below floor, "
        f"${dropped_oblig/1e6:,.1f}M summed USAspending obligation (already captured in Stages 1-2).")

    index = []
    for i, v in enumerate(selected, 1):
        name = v.get("recipient_name")
        uei = v.get("recipient_uei")
        slug = slugify(name)[:60]
        key = f'VENDOR_UEI:"{uei}"' if uei else f'VENDOR_FULL_NAME:"{name}"'
        q = f"{key} {ARMY_AGENCY} {DATE_WINDOW}"
        log(f"\n--- [{i}/{len(selected)}] {name}  ({'UEI '+uei if uei else 'name-only'})")
        recs = paginate(q, log)

        sum_obl = round(sum(r["this_obligated"] for r in recs), 2)
        piids = sorted({r.get("full_piid") or r.get("piid") for r in recs if (r.get("full_piid") or r.get("piid"))})
        dates = sorted(r["signed_date"] for r in recs if r.get("signed_date"))
        write_json(RAW / f"{slug}.json", {
            "recipient_name": name, "recipient_uei": uei, "query": q,
            "key_field": "VENDOR_UEI" if uei else "VENDOR_FULL_NAME",
            "record_count": len(recs), "distinct_piids": len(piids),
            "sum_obligated_amount": sum_obl, "records": recs,
        })
        index.append({
            "recipient_name": name, "recipient_uei": uei, "slug": slug,
            "key_field": "VENDOR_UEI" if uei else "VENDOR_FULL_NAME",
            "n_actions": len(recs), "n_piids": len(piids),
            "sum_obligated_amount": sum_obl,
            "usaspending_total_obligation": v.get("total_obligation"),
            "first_signed": dates[0] if dates else None,
            "last_signed": dates[-1] if dates else None,
            "piids": piids,
        })
        log(f"    -> {len(recs)} per-mod actions, {len(piids)} PIIDs, "
            f"sum obligatedAmount=${sum_obl/1e6:,.1f}M  (USAspending said ${ (v.get('total_obligation') or 0)/1e6:,.1f}M)")

    index.sort(key=lambda e: -(e["sum_obligated_amount"] or 0))
    write_json(INDEX, index)

    grand = sum(e["sum_obligated_amount"] for e in index)
    log(f"\n=== done. {len(index)} vendors pulled; "
        f"{sum(e['n_actions'] for e in index)} total per-mod actions; "
        f"${grand/1e6:,.1f}M summed obligatedAmount (Army+USACE scope).")
    log("\nTop 15 vendors by FPDS summed obligatedAmount:")
    for e in index[:15]:
        log(f"  ${e['sum_obligated_amount']/1e6:>9,.1f}M  {e['n_actions']:>4} actions  "
            f"{e['n_piids']:>3} PIIDs  {(e['recipient_name'] or '')[:42]}")
    logf.close()


if __name__ == "__main__":
    main()
