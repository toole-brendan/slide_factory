#!/usr/bin/env python3
"""STAGE 6 - VENDOR ENRICHMENT (SAM.gov Entity Management API).

Resolve each discovered vendor UEI -> registration detail: primary + full NAICS
list, CAGE code, business types (small/8(a)/HUBZone/SDVOSB...), physical address,
parent entity. This sharpens vendor -> capability-node (Platform/Sensors/Effectors/
C2) attribution and the small-biz/industrial-base read of the watercraft supplier set.

Endpoint (keep this exact shape — see SAM_GOV_HOWTO.md):
  GET https://api.sam.gov/entity-information/v3/entities?api_key=..&ueiSAM=<UEI>&samRegistered=Yes
  -> body.entityData[0]; NAICS at .assertions.goodsAndServices.{primaryNaics,naicsList}
  * Always samRegistered=Yes. The =No branch does a full-dataset scan (dramatically
    slower); record a miss as not_found instead of falling back to it.
  * 1,000 req/day quota; `_common` traps 429 -> QuotaExhausted, halts cleanly.
  * Vendors processed BIGGEST-OBLIGATION-FIRST; resumable (existing files skipped).
  * Keys off UEI codes only -> immune to the DoD -> "Department of War" rename.

Run:  python3 pull_sam_entity.py            # all vendors with a UEI
      python3 pull_sam_entity.py 25         # top 25 by obligation (smoke/coverage)
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import QuotaExhausted, env, http_get, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "sam_entity"
EXTRACT = ROOT / "extracted"
VENDORS = EXTRACT / "_vendors.json"
INDEX_OUT = EXTRACT / "_entity_index.json"
LOG = ROOT / "pull_logs" / "sam_entity.log"

BASE = "https://api.sam.gov/entity-information/v3/entities"
SLEEP = 0.3


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    api_key = env("SAM_API_KEY")
    logf = open(LOG, "w")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    vendors = json.loads(VENDORS.read_text())
    vendors = [v for v in vendors if v.get("recipient_uei")]
    vendors.sort(key=lambda v: -(v.get("total_obligation") or 0))
    top_n = int(sys.argv[1]) if len(sys.argv) > 1 else None
    if top_n:
        vendors = vendors[:top_n]

    log(f"=== SAM entity (Stage 6) {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"vendors with UEI={len(vendors)} (biggest-obligation-first; resumable; samRegistered=Yes)")

    index = []
    try:
        for i, v in enumerate(vendors, 1):
            uei = v["recipient_uei"]
            out_path = RAW / f"{uei}.json"
            if out_path.exists():
                try:
                    ed = json.loads(out_path.read_text()).get("entity_data")
                except Exception:
                    ed = None
            else:
                url = f"{BASE}?{urlencode({'api_key': api_key, 'ueiSAM': uei, 'samRegistered': 'Yes'})}"
                txt, st = http_get(url, headers={"Accept": "application/json"}, timeout=60)
                if txt is None:
                    log(f"  [{i}/{len(vendors)}] {uei} HTTP {st} (no response)")
                    index.append({"recipient_uei": uei, "recipient_name": v["recipient_name"],
                                  "status": f"http {st}"})
                    time.sleep(SLEEP)
                    continue
                body = json.loads(txt)
                eds = body.get("entityData") or []
                ed = eds[0] if eds else None
                write_json(out_path, {"recipient_uei": uei, "recipient_name": v["recipient_name"],
                                      "found": bool(ed), "entity_data": ed})
                time.sleep(SLEEP)

            gs = ((ed or {}).get("assertions") or {}).get("goodsAndServices") or {}
            reg = (ed or {}).get("entityRegistration") or {}
            core = (ed or {}).get("coreData") or {}
            primary = (gs.get("primaryNaics") or "")
            naics_list = [n.get("naicsCode") for n in (gs.get("naicsList") or []) if n.get("naicsCode")]
            bts = [(b.get("businessTypeCode"), b.get("businessTypeDesc"))
                   for b in (((core.get("businessTypes") or {}).get("businessTypeList")) or [])]
            index.append({
                "recipient_uei": uei,
                "recipient_name": v["recipient_name"],
                "found": bool(ed),
                "legal_business_name": reg.get("legalBusinessName"),
                "cage_code": reg.get("cageCode"),
                "registration_status": reg.get("registrationStatus"),
                "primary_naics": primary,
                "naics_list": naics_list,
                "business_types": bts,
                "n_awards": v.get("n_awards"),
                "total_obligation": v.get("total_obligation"),
            })
            if i % 25 == 0 or i == len(vendors):
                log(f"  [{i}/{len(vendors)}] {uei} {('NAICS '+str(primary)) if primary else 'not_found'} "
                    f"cage={reg.get('cageCode')}  {(v['recipient_name'] or '')[:34]}")
    except QuotaExhausted as e:
        log(f"\n!! {e}\n!! Halting; {len(index)} vendors done. Re-run after midnight UTC (cached skipped).")

    write_json(INDEX_OUT, index)
    found = sum(1 for x in index if x.get("found"))
    log(f"\n=== done. {len(index)} vendors processed; {found} resolved in SAM entity registry.")
    logf.close()


if __name__ == "__main__":
    main()
