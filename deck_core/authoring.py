"""The single public surface a slide author imports from.

    from deck_core.authoring import (
        slide, text_box, table, trow, tcell, tcell_rich,
        IN, PT, BODY, graphic_frame, column_chart,
    )

One import, the whole vocabulary. This module only *re-exports* names that live
in the engine's internal modules - it owns no logic of its own:

  primitives  -> slide/chrome/text/shape/table builders
  layout      -> mechanical tokens: units, canvas/BODY geometry, DEFAULT_FONT
  charts      -> native chart factories + graphic_frame

What stays OFF this surface (import directly when you genuinely need it): the
packager ``deck_core._build.build_pptx`` (build layer, used by the pipeline, not by
slide bodies), ``deck_core.ooxml`` namespace plumbing, and the
``tools/slide_probe.py`` inspector. Visible styling (hex colors, PT sizes, insets)
lives in the slide modules; study the exemplars, not a token catalog.
"""
from __future__ import annotations

# ── slide + text + shapes + tables (primitives) ────────────────────────────
from deck_core.primitives import (
    slide, esc,
    run, line_break, paragraph, text_box, custom_geometry, picture, connector,
    trun, tbreak, tpara, tcell_rich, tcell, trow, table,
)

# ── house chrome — the author-facing furniture (chrome) ─────────────────────
from deck_core.chrome import (
    Chrome, Sources, Link, body_slide,
    breadcrumb, slide_title, preliminary_chip, source_note,
    layout_title, layout_placeholder, cover_layout, section_divider_layout,
)

# ── units + canvas / margins / BODY box (layout) ───────────────────────────
from deck_core.layout import (
    IN, PT, EMU_PER_INCH, SLIDE_W, SLIDE_H,
    LEFT_MARGIN, RIGHT_MARGIN, USABLE_W, CONTENT_W,
    BODY_X, BODY_Y, BODY_CX, BODY_CY, BODY, BODY_R, BODY_B,
)

# ── charts ─────────────────────────────────────────────────────────────────
from deck_core.charts import (
    graphic_frame, column_chart, bar_chart, combo_chart, bubble_chart, area_chart,
)

# Deliberately NOT on this surface: a color palette, a type-size hierarchy, and
# inset presets. Visible styling lives in the slide modules as hex literals,
# explicit PT() sizes, and explicit insets - study the exemplars. The table-cell
# helpers edge/bd/cell/rcell are likewise module-local now, not exported.

# Public surface = everything re-exported above (derived, so it can't drift from
# the imports). `from deck_core.authoring import *` yields exactly this set.
__all__ = [_n for _n in dict(globals()) if not _n.startswith("_") and _n != "annotations"]
