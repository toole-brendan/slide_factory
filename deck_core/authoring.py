"""The single public surface a slide author imports from.

    from deck_core.authoring import (
        slide, text_box, table, trow, cell, rcell, edge, bd,
        IN, PT, BLACK, BLUE_3, FONT, BODY_12PT, graphic_frame, styled_chart,
    )

One import, the whole vocabulary. This module only *re-exports* names that live
in the engine's internal modules - it owns no logic of its own:

  primitives  -> slide/chrome/text/shape/table builders
  style       -> tokens: units, palette, type scale, layout/BODY, insets
  charts      -> native chart factories + styled_chart/graphic_frame
  chart_key   -> manual chart legends
  table_kit   -> edge/bd/cell/rcell table-cell helpers

What stays OFF this surface (import directly when you genuinely need it): the
packager ``deck_core._build.build_pptx`` (build layer, used by the pipeline, not by
slide bodies), ``deck_core.ooxml`` namespace plumbing, and the
``deck_core.slide_probe`` inspector. To judge how much text fits where, read the
exemplar modules - not a width model.

See AUTHORING_API.md for a categorized reference of every name below.
"""
from __future__ import annotations

# ── slide + chrome + text + shapes + tables (primitives) ───────────────────
from deck_core.primitives import (
    slide, cover_layout, section_divider_layout, esc,
    run, line_break, paragraph, text_box, custom_geometry, picture, connector,
    trun, tbreak, tpara, tcell_rich, tcell, trow, table,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
)

# ── units + helpers (style) ────────────────────────────────────────────────
from deck_core.style import (
    IN, PT, blue_pair, gray_pair, chart_accent_pair, chart_accent_seq,
)

# ── canvas / margins / BODY box (style) ────────────────────────────────────
from deck_core.style import (
    SLIDE_W, SLIDE_H, EMU_PER_INCH, LEFT_MARGIN, RIGHT_MARGIN, USABLE_W,
    CONTENT_W, BODY_X, BODY_Y, BODY_CX, BODY_CY, BODY, BODY_R, BODY_B,
)

# ── palette (style) ────────────────────────────────────────────────────────
from deck_core.style import (
    BLACK, WHITE, BODY_TEXT, DK, BREADCRUMB, PRELIM,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2, GRAY_3, GRAY_4, GRAY_5,
    CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3,
    CHART_ACCENT_4, CHART_ACCENT_5, CHART_ACCENT_6,
    BLUE_SCALE, BLUE_TEXT, GRAY_SCALE, GRAY_TEXT,
    CHART_ACCENT_SCALE, CHART_ACCENT_TEXT,
)

# ── type scale + line spacing (style) ──────────────────────────────────────
from deck_core.style import (
    FONT, LNSPC_BODY, LNSPC_SINGLE,
    SOURCES_8PT, FINEPRINT_8_5PT, LABEL_9PT, CONNECTOR_NOTE_8_5PT,
    DENSE_BODY_10PT, CHART_TITLE_10PT, MESSAGE_11PT, BODY_12PT, CAP_12PT,
    EXHIBIT_HEADER_13PT, VALUE_14PT, BADGE_16PT, RIBBON_KPI_18PT,
    ANSWER_KPI_24PT, HERO_32PT,
)

# ── chrome sizes + ids (style) ─────────────────────────────────────────────
from deck_core.style import (
    SZ_BREADCRUMB, SZ_PRELIM, SZ_SOURCES, SZ_SLIDE_TITLE, SZ_SUBTITLE,
    SZ_COVER_TITLE, SZ_COVER_SUBTITLE, SZ_DIVIDER_TITLE, SZ_DIVIDER_SUBTITLE,
    SP_ID_BREADCRUMB, SP_ID_TITLE, SP_ID_PRELIM, SP_ID_SOURCES,
)

# ── insets (style) ─────────────────────────────────────────────────────────
from deck_core.style import (
    PAD_X, PAD_Y, PAD_X_LG, PAD_Y_LG,
    INSETS_NONE, INSETS_DEFAULT, INSETS_CARD, INSETS_CHIP, INSETS_LABEL,
    INSETS_MICRO_CAP, INSETS_BADGE, INSETS_EVIDENCE, INSETS_MESSAGE,
    INSETS_RIBBON_CAP, INSETS_ANSWER_CARD,
)

# ── charts ─────────────────────────────────────────────────────────────────
from deck_core.charts import (
    graphic_frame, styled_chart, editable_bundled_chart,
    column_chart, bar_chart, line_chart, waterfall_chart, marimekko_chart,
    THINKCELL_BARS,
)
from deck_core.chart_key import chart_key, chart_legend

# ── table-cell kit ─────────────────────────────────────────────────────────
from deck_core.table_kit import edge, bd, cell, rcell

# Public surface = everything re-exported above (derived, so it can't drift from
# the imports). `from deck_core.authoring import *` yields exactly this set.
__all__ = [_n for _n in dict(globals()) if not _n.startswith("_") and _n != "annotations"]
