"""distributed_shipbuilding - <deck purpose; fill in>.

Thin per-deck package on the shared ``deck_core`` engine: binds the output path,
the shared template + brand assets under ``infra/``, and the docProps identity
(lib.py), and registers the slide modules (slides/). Slide modules import
``deck_core.*`` directly. No vendored engine copy.

Two dirs go on sys.path so both packages resolve regardless of entry point:
  - the build dir (this package's parent) so ``distributed_shipbuilding`` resolves;
  - the workspace root (three levels up) so ``deck_core`` resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_BUILD_DIR = str(_HERE.parents[1])   # slide_factory/projects/distributed_shipbuilding/ (build dir)
_CORE_DIR = str(_HERE.parents[3])    # workspace root (holds deck_core + infra)

for _p in (_BUILD_DIR, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
