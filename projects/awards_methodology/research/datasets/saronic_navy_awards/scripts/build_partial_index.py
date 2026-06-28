#!/usr/bin/env python3
"""Build _detail_index.json from whatever detail/txn/funding files are ALREADY cached,
without waiting for the (slow, mod-heavy) full detail pull to finish. Reuses the exact
index_entry() from pull_usaspending_detail so the schema matches. Safe to run repeatedly;
the full pull will overwrite _detail_index.json with the complete set when it finishes.

Run: python3 build_partial_index.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pull_usaspending_detail as D  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "extracted"
seeds = json.loads((EXTRACT / "_discovered_piids.json").read_text())

index = []
for seed in seeds:
    gid = seed.get("generated_internal_id")
    if not gid:
        continue
    dpath = D.DETAIL_DIR / f"{D.safe(gid)}.json"
    if not dpath.exists():
        continue
    try:
        detail = json.loads(dpath.read_text())
    except Exception:
        continue
    tpath = D.TXN_DIR / f"{D.safe(gid)}.json"
    fpath = D.FUND_DIR / f"{D.safe(gid)}.json"
    txns = json.loads(tpath.read_text()).get("results", []) if tpath.exists() else []
    funding = json.loads(fpath.read_text()).get("results", []) if fpath.exists() else []
    index.append(D.index_entry(seed, detail, txns, funding))

index.sort(key=lambda e: -(e.get("total_obligation") or 0))
(EXTRACT / "_detail_index.json").write_text(json.dumps(index, indent=2, default=str))
print(f"partial index built from cached files: {len(index)} awards "
      f"(of {len(seeds)} addressable seeds)")
