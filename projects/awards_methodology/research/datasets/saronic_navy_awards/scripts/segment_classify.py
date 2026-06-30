#!/usr/bin/env python3
"""Deterministic market-segment classifier for the Navy distributed-maritime-autonomy reframe.

Reads the LOCKED taxonomy (../taxonomy/segments.json) and assigns each award/requirement a primary
segment (A-J), secondary tags, and a ring. Mission segments (MCM, NSW, patrol, contested logistics)
are KEYWORD-driven; NAICS/PSC are supporting evidence. Rule:

  1. If any segment has a keyword hit -> pick the highest-scoring keyword-positive segment
     (tie -> lower ring = more Saronic-core).
  2. Else if only code (NAICS/PSC) evidence exists -> pick the highest-scoring code-positive
     segment (tie -> HIGHER ring = conservative; generic vessel codes fall to J = watch-only,
     per the transcript's warning that broad 336611 is dominated by capital ships).
  3. Else -> "U" (unclassified), ring 3.

No look-ahead, no network, pure stdlib. Used by phase1_common.build_families.
Run: python3 segment_classify.py   (self-test + segment distribution over the widened corpus)
"""
from __future__ import annotations

import ast
import json
import re
from functools import lru_cache
from pathlib import Path

TAXONOMY_PATH = Path(__file__).resolve().parents[1] / "taxonomy" / "segments.json"


@lru_cache(maxsize=1)
def load_taxonomy(path: str = "") -> dict:
    return json.loads(Path(path or TAXONOMY_PATH).read_text())


def ring_of(segment_id: str) -> int:
    for s in load_taxonomy()["segments"]:
        if s["id"] == segment_id:
            return s["ring"]
    return 3


def _code(field: str) -> str:
    """Bare NAICS/PSC code from any of: '336611', '336611 | SHIP...', or the stringified dict
    "{'code': '336611', 'description': '...'}" that the USAspending pull stores."""
    s = (field or "").strip()
    if not s:
        return ""
    if s.startswith("{"):
        try:
            d = ast.literal_eval(s)
            if isinstance(d, dict):
                return str(d.get("code", "")).strip()
        except Exception:
            m = re.search(r"'code':\s*'([^']+)'", s)
            return m.group(1) if m else ""
    return re.split(r"[\s|/,]", s, 1)[0].strip()


def _kw_hit(kw: str, text: str) -> bool:
    """Word-boundary match for short acronyms (usv, mcm, c2, lcs...), substring for phrases."""
    if len(kw) <= 4 and " " not in kw:
        return re.search(r"\b" + re.escape(kw) + r"\b", text) is not None
    return kw in text


def classify_segment(naics: str = "", psc: str = "", description: str = "", builder: str = "") -> dict:
    """-> {primary, primary_name, ring, tags, scores, classifier_basis, classifier_confidence}.

    classifier_basis  = description | mixed | code_only | none   (provenance of the decision)
    classifier_confidence = high | medium | low
    Mission labels resting only on codes (no description text) get basis=code_only/conf=low so
    downstream reporting can refuse to read them as mission conclusions (e.g. Arm A maritime)."""
    tax = load_taxonomy()
    w = tax["_weights"]
    desc_l = (description or "").lower()
    build_l = (builder or "").lower()
    text = desc_l + " " + build_l
    naics = _code(naics)
    psc = _code(psc).upper()

    rows = []
    for seg in tax["segments"]:
        kw = sum(1 for k in seg["keyword_seeds"] if _kw_hit(k.lower(), text))
        nm = 1 if naics and any(naics.startswith(n) for n in seg["naics_seeds"]) else 0
        pm = 1 if psc and any(psc == p or psc.startswith(p) for p in seg["psc_seeds"]) else 0
        rows.append({"id": seg["id"], "ring": seg["ring"], "name": seg["name"], "kw": kw,
                     "code": nm + pm, "score": kw * w["keyword"] + pm * w["psc"] + nm * w["naics"]})

    desc_kw = sum(1 for seg in tax["segments"] for k in seg["keyword_seeds"] if _kw_hit(k.lower(), desc_l))
    build_kw = sum(1 for seg in tax["segments"] for k in seg["keyword_seeds"] if _kw_hit(k.lower(), build_l))
    has_code = any(r["code"] for r in rows)
    basis = ("description" if desc_kw else "mixed" if build_kw else "code_only" if has_code else "none")

    kw_pos = [r for r in rows if r["kw"] > 0]
    if kw_pos:
        primary = sorted(kw_pos, key=lambda r: (-r["score"], r["ring"], r["id"]))[0]
        pool = kw_pos
    else:
        code_pos = [r for r in rows if r["score"] > 0]
        if not code_pos:
            return {"primary": "U", "primary_name": "Unclassified", "ring": 3, "tags": [],
                    "scores": {}, "classifier_basis": "none", "classifier_confidence": "low"}
        # code-only tie-break prefers the HIGHER ring (conservative default)
        primary = sorted(code_pos, key=lambda r: (-r["score"], -r["ring"], r["id"]))[0]
        pool = code_pos

    confidence = ("high" if basis == "description" and primary["kw"] >= 2
                  else "medium" if basis in ("description", "mixed") else "low")
    tags = [r["id"] for r in sorted(pool, key=lambda r: (-r["score"], r["ring"]))
            if r["id"] != primary["id"] and r["score"] > 0]
    return {"primary": primary["id"], "primary_name": primary["name"], "ring": primary["ring"],
            "tags": tags, "scores": {r["id"]: r["score"] for r in rows if r["score"] > 0},
            "classifier_basis": basis, "classifier_confidence": confidence}


def primary_segment(naics="", psc="", description="", builder="") -> str:
    return classify_segment(naics, psc, description, builder)["primary"]


if __name__ == "__main__":
    import csv
    from collections import Counter

    print("=== self-test (synthetic) ===")
    cases = [
        ("Unmanned surface vessel (USV) medium displacement prototype", "336611", "1905"),
        ("Mine countermeasure mission package integration MCM", "541330", "5865"),
        ("Combatant craft for Naval Special Warfare expeditionary teams", "336612", "1925"),
        ("Mission planning and command and control autonomy software", "541512", "7030"),
        ("Containerized modular payload with ISR sensor suite", "334290", "5865"),
        ("DDG-51 class destroyer construction and overhaul", "336611", "1905"),
        ("Bulk office supplies", "453210", "7510"),
    ]
    for desc, n, p in cases:
        r = classify_segment(n, p, desc)
        print(f"  [{r['primary']} r{r['ring']}] tags={str(r['tags']):<16}  {desc[:54]}")

    csvp = Path(__file__).resolve().parents[1] / "extracted" / "navy_widened_discovered.csv"
    if csvp.exists():
        prim, ring = Counter(), Counter()
        n = 0
        for row in csv.DictReader(open(csvp)):
            r = classify_segment(row.get("naics", ""), row.get("psc", ""), row.get("description", ""))
            prim[r["primary"]] += 1
            ring[r["ring"]] += 1
            n += 1
        print(f"\n=== widened corpus segment distribution (n={n}) ===")
        for sid, c in sorted(prim.items()):
            print(f"  {sid}: {c:>5}  ({100*c//max(n,1)}%)")
        print("  by ring: " + ", ".join(f"ring{k}={ring[k]}" for k in sorted(ring)))
    else:
        print(f"\n(no widened corpus at {csvp} — run pull_navy_widened_discovery.py to populate)")
