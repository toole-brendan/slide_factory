"""Slide: DDG subaward-to-hull linkage results — coverage bar + interpretation table.

ROLE
  attribution_results / subaward_to_hull_linkage_readout

USE WHEN
  A slide needs to report how much subaward spend could be attributed to a
  specific hull with confidence, WITHOUT forcing a complete hull-by-hull
  allocation: a dominant left-hand 100%-stacked coverage bar (exact vs.
  family-level vs. exception), a right-hand "what each result view supports"
  table, and a low caveat banner that frames the readout as coverage, not a
  forced allocation.

TEACHES
  - a single horizontal 100%-stacked coverage bar via bar_chart(mode="percent")
  - reading adjacent same-family shades as ONE block (A+B dark, C+D light) by
    dropping the per-segment divider (seg_line_color=None) so colour, not a
    white rule, marks the group boundary
  - outlining a sub-1% "exception" sliver with a per-series line override and
    pulling it out with a dashed leader-line callout placed OUTSIDE the bar
  - manual in-bar percentage labels over a native percent-stacked chart
  - a breakdown table whose first column is a row-spanned "spine" carrying the
    A+B / C+D / X group subtotals, and whose grade column IS the colour key
    (each grade cell is filled with its bar colour)
  - a compact right-hand interpretation table (result view / what enters /
    what it supports) paired to the same chart
  - a full-width low caveat banner used as an explanatory strip, not a
    conclusion box

DESIGN REFERENCES
  freight_charges.py        — primary: one stacked contribution bar + an
                              explanatory native table, manual on-bar labels,
                              an external legend, dashed leader callouts.
  comparison_vs_ddgs.py     — secondary: left stacked chart paired with a right
                              comparison table; row-spans / grid-spans, manual
                              data labels, a one-row title bar.
  status_quo_outlook_oceangoing.py
                            — backup: chart-plus-table density, manual labels,
                              a row-spanned spine + merged-commentary table.

NUMBERS (FY2026$, from the linkage run)
  Universe: $4,028.2M across 6,020 subaward records.
    A  Single-ship PIID ................... 69.0   1.7%   ┐ exact-hull
    B  Direct in-family hull text ........ 1,200.6  29.8% ┘  $1,269.7M / 31.5%
    C  Requirement-text signal only ...... 1,787.9  44.4% ┐ family-level
    D  PIID family only ................... 965.2   24.0% ┘  $2,753.1M / 68.3%
    X  Conflict / multi-hull .............. 5.4     0.1%    exception  $5.4M
  Shares are of the $4,028.2M universe (A..X sum to 100.0%).
"""
from __future__ import annotations

from deck_core.authoring import (
    Chrome, IN, PT, bar_chart, body_slide, connector, graphic_frame, line_break,
    paragraph, run, table, tbreak, tcell, tcell_rich, text_box, tpara, trow, trun,
)


# ── House colours (hex lives in the module; no shared palette) ───────────────
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
GRAY_1 = "F2F2F2"
GRAY_TX = "595959"        # muted caption text
RULE = "BFBFBF"           # thin within-group divider
GROUP_RULE = "808080"     # group separator
FONT = "Arial"

LAYOUT = "slideLayout4"

# ── Attribution-tier ramp ────────────────────────────────────────────────────
# A+B are two dark navies that read as one "exact-hull" block; C+D are two light
# blues that read as one "family-level" block; X is the crimson exception sliver.
EXACT_A = "16314B"        # darkest navy — single-ship PIID
EXACT_B = "2E5479"        # dark blue   — direct in-family hull text
FAMILY_C = "7E9BC0"       # light-medium blue — requirement-text signal only
FAMILY_D = "AEC2DC"       # light blue  — PIID family only
EXCEPTION_X = "C30C3E"    # crimson     — conflict / multi-hull
EXCEPTION_LN = "7A0A28"   # darker crimson outline for the X sliver


# ════════════════════════════════════════════════════════════════════════════
# Coverage bar: one horizontal 100%-stacked bar, FY2026$ shares of the universe.
# ════════════════════════════════════════════════════════════════════════════
# Series stack left-to-right in author order (A at the base/left ... X at the
# right). Values are FY2026$M; mode="percent" normalises each to its share, so
# the single bar reads as 100% coverage of the $4,028.2M universe.
COVERAGE_SERIES: tuple[dict, ...] = (
    {"name": "A — Single-ship PIID",            "color": EXACT_A,  "values": [69.0]},
    {"name": "B — Direct in-family hull text",  "color": EXACT_B,  "values": [1200.6]},
    {"name": "C — Requirement-text signal only","color": FAMILY_C, "values": [1787.9]},
    {"name": "D — PIID family only",            "color": FAMILY_D, "values": [965.2]},
    # The exception sliver is ~0.13% wide — too small to read, so it carries its
    # own crimson outline and is pulled out by the dashed leader callout below.
    {"name": "X — Conflict / multi-hull",       "color": EXCEPTION_X,
     "values": [5.4], "line": {"color": EXCEPTION_LN, "width": 9525}},
)

CHART_STYLE = {
    "mode": "percent",
    "categories": ["DDG subawards"],
    "series": [dict(s) for s in COVERAGE_SERIES],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": False,
    "show_value_labels": False,        # manual in-bar % labels instead
    "show_gridlines": False,
    "seg_line_color": None,            # no per-segment rule -> A+B and C+D read as blocks
    "value_axis_line_color": "none",   # hide the value (bottom) axis line
    "gap_width": 40,                   # one category -> a thick coverage bar
    "bar_overlap": 100,
    "cat_header": "Population",
    # Pin the inner plot rectangle so the manual labels register to the segments.
    "plot_layout": {"x": 0.004, "y": 0.06, "w": 0.992, "h": 0.88},
}

CHARTS = [bar_chart(**CHART_STYLE)]


# ── Chart-frame + manual-label geometry (inches) ─────────────────────────────
# Frame and pinned plot rectangle, used to place the in-bar % labels.
_CF_X, _CF_Y, _CF_W, _CF_H = 0.48, 2.06, 6.05, 0.80
_PLOT_X0 = _CF_X + 0.004 * _CF_W              # 0.5042  inner-plot left
_PLOT_W = 0.992 * _CF_W                       # 6.0016  inner-plot width
_PLOT_R = _PLOT_X0 + _PLOT_W                   # 6.5058  inner-plot right (X sliver)
_BAR_Y = 2.36                                  # in-bar label band (centred on the bar)
_LBL_H = 0.20


def _seg_center_x(cum_mid_pct: float) -> float:
    """x (in) of a segment's centre along the pinned plot, given its cumulative
    mid-point as a percent of the 100%-stacked bar."""
    return _PLOT_X0 + (cum_mid_pct / 100.0) * _PLOT_W


# Cumulative mid-points: A 0.85 · B 16.6 · C 53.7 · D 87.9 · X 99.95. Only the
# three wide segments (B, C, D) hold an in-bar label; A and X are too thin.
_INBAR_LABELS = (
    # (segment_center_pct, text, text_color)
    (16.6, "29.8%", WHITE),    # B — dark fill -> white
    (53.7, "44.4%", BLACK),    # C — light fill -> black
    (87.9, "24.0%", BLACK),    # D — light fill -> black
)


# ════════════════════════════════════════════════════════════════════════════
# Local table kit — content first, cell mechanics second (per the exemplars).
# ════════════════════════════════════════════════════════════════════════════
def edge(color, w=12700):
    """One native-table border edge (12_700 EMU = 1pt)."""
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Border dict from only the edges drawn; omitted sides render no-fill."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", span=1, rowspan=1,
         l_ins=45720, r_ins=45720, t_ins=36000, b_ins=36000, **edges):
    """tcell with content first; borders via L/R/T/B=edge(...)."""
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=36000, b_ins=36000, **edges):
    """tcell_rich with content first; borders via L/R/T/B=edge(...)."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def _r(text, *, size=PT(10), bold=None, italic=None, color=BLACK):
    return run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)


# ════════════════════════════════════════════════════════════════════════════
# Paint layer. Helpers append to the shared sequential id counter `n`; paint
# order is the slide z-order (later shapes sit on top).
# ════════════════════════════════════════════════════════════════════════════
def paint_chart(n) -> list[str]:
    """Native percent-stacked coverage bar + its title / universe sub-caption."""
    out: list[str] = []
    out.append(text_box(n(), "ChartTitle", IN(0.48), IN(1.56), IN(_CF_W), IN(0.44), [
        paragraph([_r("DDG subaward $ coverage by attribution confidence (FY2026$)",
                      size=PT(10), bold=True)], mar_l=0, indent=0, line_spacing=100000),
        paragraph([_r("Universe: $4,028.2M across 6,020 subaward records",
                      size=PT(8), italic=True, color=GRAY_TX)], mar_l=0, indent=0,
                  space_before=100, line_spacing=100000),
    ], fill=None, line_color="none", anchor="t", wrap="none",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(graphic_frame(sp_id=n(), name="CoverageBar",
                             x=IN(_CF_X), y=IN(_CF_Y), cx=IN(_CF_W), cy=IN(_CF_H), rId="rId2"))
    return out


def paint_inbar_labels(n) -> list[str]:
    """White/black % labels centred on the three wide segments (B, C, D)."""
    out: list[str] = []
    for mid_pct, text, color in _INBAR_LABELS:
        cx = _seg_center_x(mid_pct)
        out.append(text_box(n(), "InBarLabel", IN(cx - 0.45), IN(_BAR_Y), IN(0.90), IN(_LBL_H),
                            [paragraph([_r(text, size=PT(10), bold=True, color=color)],
                                       align="ctr", mar_l=0, indent=0, line_spacing=100000)],
                            fill=None, line_color="none", anchor="ctr", wrap="none",
                            l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    return out


def paint_exception_callout(n) -> list[str]:
    """Dashed leader from the right-end X sliver to a crimson 'held for review'
    callout below the bar (the sliver is too thin to label in place)."""
    out: list[str] = []
    # Dashed leader: top point at the sliver (bar bottom, far right), down to the
    # callout's top edge. A signed cx flips the box so it draws right-to-left.
    out.append(connector(n(), "ExceptionLeader",
                         IN(_PLOT_R), IN(2.71), IN(-0.12), IN(0.19),
                         color=EXCEPTION_X, width=12700, dash="dash"))
    out.append(text_box(n(), "ExceptionCallout", IN(4.50), IN(2.90), IN(2.05), IN(0.34),
                        [paragraph([_r("63 rows · $5.4M held for review",
                                       size=PT(8.5), bold=True, color=EXCEPTION_X)],
                                   align="ctr", line_spacing=100000)],
                        fill=WHITE, line_color=EXCEPTION_X, line_width=9525, anchor="ctr",
                        l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144))
    return out


def paint_breakdown_table(n) -> list[str]:
    """Left breakdown / legend table: a row-spanned tier 'spine' carrying the
    A+B / C+D / X subtotals, a grade column whose fills ARE the bar colour key,
    then the attribution basis, FY2026$M, and share columns."""
    th = dict(bold=True, align="ctr", anchor="ctr")          # header cell defaults
    rows = [
        trow([
            cell("Confidence tier", **th, B=edge(DK)),
            cell("Grade", **th, B=edge(DK)),
            cell("Attribution basis", bold=True, anchor="ctr", B=edge(DK)),
            cell("FY2026$M", **th, B=edge(DK)),
            cell("Share", **th, B=edge(DK)),
        ], h=IN(0.30)),
        # ── Exact-hull block (A + B) — one dark spine spanning both rows ──
        trow([
            rcell([
                tpara([trun("Exact-hull (A/B)", size=PT(9.5), bold=True, color=WHITE, font=FONT)], align="ctr"),
                tpara([trun("$1,269.7M · 31.5%", size=PT(9), color=WHITE, font=FONT)], align="ctr"),
            ], fill=EXACT_B, rowspan=2, B=edge(GROUP_RULE)),
            cell("A", fill=EXACT_A, color=WHITE, bold=True, align="ctr", B=edge(RULE)),
            cell("Single-ship PIID", B=edge(RULE)),
            cell("69.0", align="ctr", B=edge(RULE)),
            cell("1.7%", align="ctr", B=edge(RULE)),
        ], h=IN(0.40)),
        trow([
            cell("B", fill=EXACT_B, color=WHITE, bold=True, align="ctr", B=edge(GROUP_RULE)),
            cell("Direct in-family hull text", B=edge(GROUP_RULE)),
            cell("1,200.6", align="ctr", B=edge(GROUP_RULE)),
            cell("29.8%", align="ctr", B=edge(GROUP_RULE)),
        ], h=IN(0.40)),
        # ── Family-level block (C + D) — one light spine spanning both rows ──
        trow([
            rcell([
                tpara([trun("Family-level (C/D)", size=PT(9.5), bold=True, color=BLACK, font=FONT)], align="ctr"),
                tpara([trun("$2,753.1M · 68.3%", size=PT(9), color=BLACK, font=FONT)], align="ctr"),
            ], fill=FAMILY_C, rowspan=2, B=edge(GROUP_RULE)),
            cell("C", fill=FAMILY_C, color=BLACK, bold=True, align="ctr", B=edge(RULE)),
            cell("Requirement-text signal only", B=edge(RULE)),
            cell("1,787.9", align="ctr", B=edge(RULE)),
            cell("44.4%", align="ctr", B=edge(RULE)),
        ], h=IN(0.40)),
        trow([
            cell("D", fill=FAMILY_D, color=BLACK, bold=True, align="ctr", B=edge(GROUP_RULE)),
            cell("PIID family only", B=edge(GROUP_RULE)),
            cell("965.2", align="ctr", B=edge(GROUP_RULE)),
            cell("24.0%", align="ctr", B=edge(GROUP_RULE)),
        ], h=IN(0.40)),
        # ── Exception (X) ──
        trow([
            rcell([
                tpara([trun("Exception (X)", size=PT(9.5), bold=True, color=WHITE, font=FONT)], align="ctr"),
                tpara([trun("$5.4M · 0.1%", size=PT(9), color=WHITE, font=FONT)], align="ctr"),
            ], fill=EXCEPTION_X),
            cell("X", fill=EXCEPTION_X, color=WHITE, bold=True, align="ctr"),
            cell("Conflict / multi-hull"),
            cell("5.4", align="ctr"),
            cell("0.1%", align="ctr"),
        ], h=IN(0.40)),
    ]
    return [table(n(), "AttributionBreakdownTable", IN(0.48), IN(3.40), IN(6.00),
                  IN(2.30), col_widths=[IN(1.30), IN(0.55), IN(2.35), IN(0.90), IN(0.90)],
                  rows=rows)]


def paint_interpretation(n) -> list[str]:
    """Right side: caption + the compact 'result view / what enters / what it
    supports' table, then a one-line reconciliation footnote."""
    out: list[str] = []
    out.append(text_box(n(), "ResultViewsCaption", IN(6.85), IN(1.56), IN(6.00), IN(0.30),
                        [paragraph([_r("Downstream result views", size=PT(11), bold=True)],
                                   mar_l=0, indent=0, line_spacing=100000)],
                        fill=None, line_color="none", anchor="b", wrap="none",
                        l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "ResultViewsSubcaption", IN(6.85), IN(1.87), IN(6.00), IN(0.20),
                        [paragraph([_r("Built from the linked subaward rows", size=PT(9),
                                       italic=True, color=GRAY_TX)], mar_l=0, indent=0,
                                   line_spacing=100000)],
                        fill=None, line_color="none", anchor="t", wrap="none",
                        l_ins=0, t_ins=0, r_ins=0, b_ins=0))

    th = dict(bold=True, anchor="ctr")
    rows = [
        trow([
            cell("Result view", **th, B=edge(DK)),
            cell("What enters", **th, B=edge(DK)),
            cell("What it supports", **th, B=edge(DK)),
        ], h=IN(0.34)),
        trow([
            cell("Exact-hull spend summary", bold=True, B=edge(RULE)),
            cell("A/B rows only", B=edge(RULE)),
            cell("Hull-level spend readout", B=edge(RULE)),
        ], h=IN(0.58)),
        trow([
            cell("Vendor × Hull exposure", bold=True, B=edge(RULE)),
            cell("1,193 rows · 281 vendors · 24 hulls", B=edge(RULE)),
            cell("Supplier exposure by assigned hull", B=edge(RULE)),
        ], h=IN(0.80)),
        trow([
            cell("Vendor × Hull × SWBS", bold=True, B=edge(RULE)),
            cell("1,296 rows · HII-Ingalls only", B=edge(RULE)),
            cell("Functional-system view by hull", B=edge(RULE)),
        ], h=IN(0.66)),
        trow([
            cell("Exception queue", bold=True),
            cell("63 rows"),
            cell("Human review; excluded from hull roll-ups"),
        ], h=IN(0.70)),
    ]
    out.append(table(n(), "ResultViewsTable", IN(6.85), IN(2.16), IN(6.00), IN(3.08),
                     col_widths=[IN(1.85), IN(2.25), IN(1.90)], rows=rows))
    out.append(text_box(n(), "ReconciliationNote", IN(6.85), IN(5.30), IN(6.00), IN(0.36),
                        [paragraph([_r("Vendor-level views use exact (A/B) rows only; the "
                                       "SWBS view reconciles to the HII-Ingalls share of "
                                       "exact spend.", size=PT(9), italic=True, color=GRAY_TX)],
                                   mar_l=0, indent=0, line_spacing=100000)],
                        fill=None, line_color="none", anchor="t",
                        l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    return out


def paint_caveat_band(n) -> list[str]:
    """Full-width, low explanatory banner under the chart/table — coverage, not a
    forced allocation. A thin top rule sets it off without a boxed conclusion."""
    out: list[str] = []
    out.append(connector(n(), "CaveatRule", IN(0.48), IN(5.84), IN(11.88), IN(0),
                         color=DK, width=9525))
    out.append(text_box(n(), "CaveatBand", IN(0.48), IN(5.86), IN(11.88), IN(0.40), [
        paragraph([
            _r("Readout is coverage, not a forced hull-by-hull allocation.  ", size=PT(10), bold=True),
            _r("Exact rows roll forward; family-level rows remain visible; conflicts stay out of hull totals.",
               size=PT(10)),
        ], align="ctr", mar_l=0, indent=0, line_spacing=100000),
    ], fill=GRAY_1, line_color="none", anchor="ctr", l_ins=91440, t_ins=18288,
        r_ins=91440, b_ins=18288))
    return out


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 — sequential shape ids
    out: list[str] = []
    out += paint_chart(n)
    out += paint_inbar_labels(n)
    out += paint_exception_callout(n)
    out += paint_breakdown_table(n)
    out += paint_interpretation(n)
    out += paint_caveat_band(n)
    return "".join(out)


CHROME = Chrome(
    section="DDG-51 Subaward Attribution",
    topic="Linkage Results",
    title="DDG Subaward-to-Hull Linkage",
    takeaway="Exact hull attribution for ~one-third of dollars; the rest is "
             "retained at contract-family level or held for review",
)


def render() -> str:
    return body_slide(CHROME, _body())
