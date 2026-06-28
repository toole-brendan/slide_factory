#!/usr/bin/env python3
"""OTA LAYER (the stage Stage-1 discovery structurally MISSES). USAspending
spending_by_award filtered to award_type_codes A-D / IDV_* EXCLUDES Other Transactions,
so the discovery universe shows USV production primes as "$0 / absent". That is a pull
artifact, NOT proof the awards are invisible: OT agreements/orders ARE carried by the
SAM.gov Contract Awards API. This stage pulls them by awardee UEI for the known USV /
autonomous-maritime vendors and shows the OT layer the portal and a standard FPDS/A-D-IDV
view both miss -- but awards data surfaces.

Method: resolve each vendor name -> UEI(s) via SAM Entity, then SAM Contract Awards by
awardeeUniqueEntityId (the verified filter; q/legalBusinessName are unreliable). Group
mod-level records into families; family obligated = cumulative totalActionObligation (read
once, never summed across mods); ceiling = max totalBaseAndAllOptionsValue.

Inputs : VENDORS list below.
Outputs: extracted/ota_layer.csv (one row per award family), extracted/ota_layer_summary.json,
         sam_contract_awards_ota/<uei>.json (raw)
Run    : python3 pull_ota_layer.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import QuotaExhausted, env, http_get, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "sam_contract_awards_ota"
EXTRACT = ROOT / "extracted"
ENTITY = "https://api.sam.gov/entity-information/v3/entities"
CA = "https://api.sam.gov/contract-awards/v1/search"

VENDORS = ["SARONIC TECHNOLOGIES", "METAL SHARK", "SEA MACHINES", "BLUE WATER AUTONOMY",
           "OCEAN AERO", "SPATIAL INTEGRATED SYSTEMS", "MARITIME APPLIED PHYSICS",
           "HII UNMANNED SYSTEMS", "L3HARRIS TECHNOLOGIES", "TEXTRON SYSTEMS",
           "LEIDOS", "BOLLINGER", "AUSTAL USA"]


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def resolve_ueis(name, key, log):
    url = f"{ENTITY}?" + urlencode({"api_key": key, "legalBusinessName": name,
                                    "includeSections": "entityRegistration"})
    txt, st = http_get(url, headers={"Accept": "application/json"})
    if not txt:
        log(f"  entity {name!r}: status {st}")
        return []
    ents = (json.loads(txt).get("entityData") or [])
    out = []
    for e in ents:
        reg = e.get("entityRegistration") or {}
        if reg.get("ueiSAM"):
            out.append(reg["ueiSAM"])
    return out


def pull_uei(uei, key, log):
    recs, off = [], 0
    while off < 400:
        url = f"{CA}?" + urlencode({"api_key": key, "awardeeUniqueEntityId": uei,
                                    "limit": 100, "offset": off,
                                    "includeSections": "contractId,coreData,awardDetails"})
        txt, st = http_get(url, headers={"Accept": "application/json"})
        if not txt:
            break
        b = json.loads(txt)
        page = b.get("awardSummary") or []
        recs.extend(page)
        total = int(b.get("totalRecords") or 0)
        if not page or len(recs) >= total:
            break
        off += 100
        time.sleep(0.3)
    return recs


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    key = env("SAM_API_KEY")
    logf = open(ROOT / "pull_logs" / "ota_layer.log", "w")

    def log(m):
        print(m, flush=True); logf.write(m + "\n"); logf.flush()

    families = []
    try:
        for name in VENDORS:
            ueis = resolve_ueis(name, key, log)
            allrecs = []
            for uei in ueis:
                allrecs += pull_uei(uei, key, log)
                time.sleep(0.2)
            write_json(RAW / f"{name.replace(' ', '_')}.json", {"vendor": name, "ueis": ueis,
                                                                "n_records": len(allrecs), "records": allrecs})
            fam = defaultdict(lambda: {"type": set(), "signed": [], "ceiling": 0.0,
                                       "obligated": 0.0, "office": set()})
            for r in allrecs:
                cid = r.get("contractId") or {}; core = r.get("coreData") or {}
                det = r.get("awardDetails") or {}; dates = det.get("dates") or {}
                tot = det.get("totalContractDollars") or {}
                aoi = core.get("awardOrIDVType") or {}
                piid = cid.get("piid")
                g = fam[piid]
                g["type"].add(aoi.get("name") if isinstance(aoi, dict) else aoi)
                if dates.get("dateSigned"):
                    g["signed"].append(dates["dateSigned"][:10])
                g["ceiling"] = max(g["ceiling"], f(tot.get("totalBaseAndAllOptionsValue")))
                g["obligated"] = max(g["obligated"], f(tot.get("totalActionObligation")))
            for piid, g in fam.items():
                types = [t for t in g["type"] if t]
                is_ot = any("OTHER TRANSACTION" in (t or "").upper() for t in types)
                sd = sorted(g["signed"])
                families.append({"vendor": name, "piid": piid, "is_ot": "yes" if is_ot else "no",
                                 "award_type": "/".join(types), "base_signed": sd[0] if sd else "",
                                 "last_signed": sd[-1] if sd else "",
                                 "ceiling_$m": round(g["ceiling"] / 1e6, 1),
                                 "obligated_$m": round(g["obligated"] / 1e6, 1)})
            ot_d = sum(x["obligated_$m"] for x in families if x["vendor"] == name and x["is_ot"] == "yes")
            log(f"{name:26s} ueis={len(ueis)} recs={len(allrecs)} families={len([x for x in families if x['vendor']==name])} "
                f"OT_obligated=${ot_d:.0f}M")
    except QuotaExhausted as e:
        log(f"!! {e}")

    families.sort(key=lambda x: -x["obligated_$m"])
    import csv
    with open(EXTRACT / "ota_layer.csv", "w", newline="") as fh:
        cols = ["vendor", "piid", "is_ot", "award_type", "base_signed", "last_signed", "ceiling_$m", "obligated_$m"]
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(families)
    ot = [x for x in families if x["is_ot"] == "yes"]
    summary = {"vendors": len(VENDORS), "ot_families": len(ot),
               "ot_obligated_total_$m": round(sum(x["obligated_$m"] for x in ot), 1),
               "ot_ceiling_total_$m": round(sum(x["ceiling_$m"] for x in ot), 1),
               "by_vendor": {}}
    for name in VENDORS:
        vf = [x for x in families if x["vendor"] == name]
        vot = [x for x in vf if x["is_ot"] == "yes"]
        summary["by_vendor"][name] = {"families": len(vf), "ot_families": len(vot),
                                      "ot_obligated_$m": round(sum(x["obligated_$m"] for x in vot), 1),
                                      "ot_ceiling_$m": round(sum(x["ceiling_$m"] for x in vot), 1)}
    (EXTRACT / "ota_layer_summary.json").write_text(json.dumps(summary, indent=2))

    print(f"\nOTA layer: {len(ot)} OT award families across {len(VENDORS)} USV vendors; "
          f"${summary['ot_obligated_total_$m']/1000:.2f}B obligated / ${summary['ot_ceiling_total_$m']/1000:.2f}B ceiling")
    print("top OT families (invisible to SAM Opportunities AND to a standard FPDS/A-D-IDV pull):")
    for x in [x for x in families if x["is_ot"] == "yes"][:12]:
        print(f"  ${x['obligated_$m']:7.1f}M obl (${x['ceiling_$m']:7.1f}M ceil) {x['piid']:16} "
              f"{x['base_signed']} {x['vendor']}")
    logf.close()


if __name__ == "__main__":
    main()
