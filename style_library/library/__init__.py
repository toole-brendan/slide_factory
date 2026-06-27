"""library - curated reference corpus of styled slide modules.

Single slides ported 1:1 from the source market-analysis decks onto the shared
``deck_core`` engine, organized as a style library: framework diagrams,
value-chain maps, definition tables, charted exhibits. Each module is emitted by
the converter at style_library/_tools/convert_slide.py: surrounding shapes become
idiomatic deck_core primitive calls (text_box / connector / table / picture),
<p:pic> images are wired via IMAGES + picture(), and native <c:chart> exhibits
are data-over-template styled_chart. think-cell OLE frames are dropped.

Thin per-deck package: binds the output path, the shared template + brand assets,
and the docProps identity (lib.py), and registers the slide modules (slides/).
The raw-OOXML engine is the canonical ``deck_core`` package at the workspace
root; the slide modules import ``deck_core.*`` directly. No vendored engine copy.

Two dirs go on sys.path so both packages resolve regardless of entry point:
  - the build dir (this package's parent) so ``library`` resolves;
  - the workspace root (two levels up) so ``deck_core`` resolves.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_BUILD_DIR = str(_HERE.parents[1])   # slide_factory/style_library/ (build dir)
_CORE_DIR = str(_HERE.parents[2])    # workspace root (holds deck_core + infra)

for _p in (_BUILD_DIR, _CORE_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
