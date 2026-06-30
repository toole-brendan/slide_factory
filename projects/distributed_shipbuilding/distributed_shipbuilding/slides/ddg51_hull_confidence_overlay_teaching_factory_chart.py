"""DDG-51 hull-attribution confidence overlay (Slide 3 of the DDG SWBS decklet).

ROLE
  evidence_grain / hull_confidence_overlay

USE WHEN
  A "precision / grain" slide must hold two DIFFERENT denominators apart without
  sounding defensive: (left) the whole DDG-51 universe split by hull-attribution
  confidence, where only A/B is exact-hull (~31.5%); and (right) a curated recent
  exact-hull subset whose SWBS coverage is excellent and whose mix is propulsion-
  dominant. The design makes the left -> right "zoom" explicit so a reader never
  conflates "$870.9M" with "31.5% of all DDG dollars."

TEACHES
  - a left definition/confidence table paired with a right native 100% stacked column
  - exact-hull (A/B) vs not-exact (C/D) encoded as a two-band fill, not a smooth
    gradient (the tiers are categorical, not a continuum)
  - a focal outline + pale-blue takeaway note that turns the 31.5% into a callout
  - a single-category percent-stacked column with native centered % labels on the
    big three segments and the small two carried in a manual legend
  - U00 rendered as a hatched "caveat" fill, both in the chart series and the legend
    swatch (text_box pattern_fill), consistent with the Slide 1 treatment of U00
  - two big-number KPI cards (fleet_overview idiom) translating the chart
  - an explicit denominator caveat so the slide stays unimpeachable

DESIGN NOTES (decisions, with defaults taken from the design sign-off)
  - SWBS group colors below MUST match Slide 1. Reuse SWBS_200 / SWBS_500 /
    SWBS_300 / SWBS_OTHER / U00_PATTERN verbatim there.
  - Breadcrumb section/topic and the Sources line are PLACEHOLDERS; set them to
    match the rest of your DDG deck.
  - Right exhibit is a vertical 100% stacked column (the "small stacked bar").
  - The optional all-DDG-by-confidence strip (a second native chart) is NOT
    included, per the brief (the confidence definitions matter as much as the %).

SOURCE NOTE
  Built natively through column_chart(mode="percent"); the chart data, fills, and
  axis choices are inspectable Python (no sidecar XLSB). Figures are transcribed
  from the project workbook write-up (recent HII FY23-27 MYP exact-hull subset).
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, Sources, IN, PT, body_slide, column_chart, connector, graphic_frame,
    paragraph, run, table, tcell, text_box, trow,
)


# ── House colors (hex lives in the module; no shared palette) ───────────────
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
GRAY_1 = "F2F2F2"
GRAY_3 = "BFBFBF"
GRAY_MID = "808080"
BLUE_1 = "E2E9EF"   # not-exact (C/D) confidence band fill
BLUE_4 = "3D5972"   # exact-hull (A/B) confidence band fill
TEAL = "007770"     # focal accent: the usable / exact-hull story
SOFT_BLUE = "CEDDEC"  # house takeaway-note fill
FONT = "Arial"

# ── SWBS group palette — KEEP IN SYNC WITH SLIDE 1 ──────────────────────────
SWBS_200 = "1D4D68"   # 200 Propulsion Plant   (dark -> white label)
SWBS_500 = "4C6C9C"   # 500 Auxiliary Systems  (mid  -> white label)
SWBS_300 = "6E91B1"   # 300 Electric Plant     (light blue -> white label)
SWBS_OTHER = GRAY_3   # Other mapped groups
U00_PATTERN = {"prst": "ltUpDiag", "fg": GRAY_MID, "bg": WHITE}  # No SWBS evidence (caveat)

LAYOUT = "slideLayout4"


# ════════════════════════════════════════════════════════════════════════════
# Right exhibit: recent exact-hull subset SWBS mix (single-category 100% stack).
# One record drives BOTH the chart series and the manual legend, so they can
# never desync. The big three segments show native centered % labels; the two
# tiny segments (Other 1.9%, U00 1.5%) hide their native labels and are carried
# in the legend with their shares appended.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class SwbsSegment:
    name: str
    fill: str | None        # solid hex, or None when `pattern` is used
    share: float            # % share of the recent exact-hull subset
    pattern: dict | None = None
    show_native_label: bool = True


# Bottom-to-top stack order = largest at the bottom.
SWBS_SEGMENTS: tuple[SwbsSegment, ...] = (
    SwbsSegment("200 Propulsion Plant", SWBS_200, 50.0),
    SwbsSegment("500 Auxiliary Systems", SWBS_500, 26.2),
    SwbsSegment("300 Electric Plant", SWBS_300, 20.4),
    SwbsSegment("Other mapped", SWBS_OTHER, 1.9, show_native_label=False),
    SwbsSegment("U00 / No SWBS evidence", None, 1.5, pattern=U00_PATTERN, show_native_label=False),
)

CHART_CATEGORIES = ("Recent exact-hull subset",)


def _chart_series() -> list[dict]:
    series: list[dict] = []
    for seg in SWBS_SEGMENTS:
        s: dict = {"name": seg.name, "values": [seg.share]}
        if seg.pattern is not None:
            s["pattern"] = seg.pattern
        else:
            s["color"] = seg.fill
        if not seg.show_native_label:
            s["hide_labels"] = True
        series.append(s)
    return series


# House idiom: a 100% column is mode="stacked" with shares that already sum to
# 100 (no library chart uses mode="percent"). On a real 0-100 scale the value
# axis is a clean percent axis ('0"%"', ticks every 25) with no fractional-axis
# tricks, and value_axis_max == the share total keeps the column filling the plot.
_SHARE_TOTAL = sum(seg.share for seg in SWBS_SEGMENTS)   # 100.0

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(CHART_CATEGORIES),
    "series": _chart_series(),
    "show_legend": False,
    "show_cat_labels": False,            # single category; no native cat tick
    "show_value_axis_labels": True,      # 0-100% share axis on the left
    "show_gridlines": False,
    "show_value_labels": True,           # native centered % labels on big three
    "value_axis_format": '0"%"',         # 0-100 scale: append % (no x100)
    "value_label_format": '0.0"%"',
    "value_label_size_pt": 10,
    "value_label_bold": False,
    "value_axis_min": 0,
    "value_axis_max": _SHARE_TOTAL,
    "value_axis_major_unit": 25,         # ticks every 25%
    "gap_width": 60,
    "bar_overlap": 100,
    "seg_line_color": "000000",          # thin black dividers (freight_charges 100%-mix idiom)
    "seg_line_width": 3_175,             # 0.25pt
    "axis_line_color": "162029",         # visible dark category baseline (house)
    "value_axis_line_color": GRAY_MID,   # show the value-axis spine (gray)
    "plot_layout": {"x": 0.22, "y": 0.03, "w": 0.74, "h": 0.94},  # left inset holds the % labels
    "cat_header": "Subset",
}

CHARTS = [column_chart(**CHART_STYLE)]


# ════════════════════════════════════════════════════════════════════════════
# Left exhibit data: hull-attribution confidence ladder.
# A/B = exact hull (strong band); C/D = not exact (lighter band); X = conflict.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class ConfidenceRow:
    code: str
    meaning: str
    share: str
    code_fill: str
    code_color: str
    h: float


CONFIDENCE_ROWS: tuple[ConfidenceRow, ...] = (
    ConfidenceRow("A", "Official exact / single-ship PIID", "1.7%", BLUE_4, WHITE, 0.44),
    ConfidenceRow("B", "Direct subaward text names one in-family hull", "29.8%", BLUE_4, WHITE, 0.50),
    ConfidenceRow("C", "Prime requirement text only", "44.4%", BLUE_1, BLACK, 0.44),
    ConfidenceRow("D", "PIID family only", "24.0%", BLUE_1, BLACK, 0.44),
    ConfidenceRow("X", "Conflict / review", "0.1%", GRAY_3, BLACK, 0.40),
)

# A/B are the first two data rows; the focal band frames exactly those two.
_AB_BAND_ROW_COUNT = 2


# ════════════════════════════════════════════════════════════════════════════
# Geometry (inches; converted to EMU at the call site).
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


class ShapeIds:
    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        v = self._next
        self._next += 1
        return v


# Left / right zones, divider, and the source-anchored vertical band.
DIVIDER_X = 6.73
LEFT_X, LEFT_W = 0.495, 6.055
RIGHT_X, RIGHT_W = 6.95, 5.88

HEADER_Y, HEADER_H = 1.58, 0.28
RULE_Y = 1.92

TABLE = Box(LEFT_X, 1.98, LEFT_W, 0.0)            # h derived from rows
TABLE_HEADER_H = 0.34
TABLE_COLS = (0.95, 3.95, 1.155)                  # Confidence | Meaning | Share

CALLOUT = Box(LEFT_X, 4.70, LEFT_W, 0.55)
CAVEAT = Box(LEFT_X, 5.40, LEFT_W, 0.62)

ZOOM_CAPTION = Box(RIGHT_X, 1.96, RIGHT_W, 0.26)
CHIP_A = Box(RIGHT_X, 2.30, 2.85, 1.00)
CHIP_B = Box(9.98, 2.30, 2.85, 1.00)

# Center the chart+legend exhibit horizontally within the RHS zone. Unshifted,
# the exhibit (chart-frame left .. widest legend-label right) hugs the divider and
# leaves dead space at the right edge of the zone. One shared shift moves the chart
# frame, the legend, AND the chart title right by the same amount, so the chart->
# legend spacing is preserved and the whole group reads as centered:
#   group span  = [RIGHT_X .. LEGEND_X + LEGEND_LABEL_GAP + ~1.42]  (~6.95..10.92)
#   zone center = RIGHT_X + RIGHT_W/2 = 9.89   ->   shift ~= 0.95
RHS_EXHIBIT_SHIFT = 0.95
CHART_FRAME = Box(RIGHT_X + RHS_EXHIBIT_SHIFT, 3.55, 2.00, 2.55)

# External one-line chart title (house idiom — a no-fill text_box above the frame,
# exactly as Slide 1 does it, NOT a native c:title). Bottom-anchored so the text
# sits just above the column top; rides the same shift as the chart.
CHART_TITLE = Box(RIGHT_X + RHS_EXHIBIT_SHIFT, 3.32, 4.90, 0.20)

LEGEND_X = 9.20 + RHS_EXHIBIT_SHIFT      # 10.15 — keeps the 0.25in chart->swatch gap
LEGEND_ROW_DY = 0.245                 # tight vertical pitch
LEGEND_SWATCH = (0.17, 0.13)          # same chip size as the fingerprint legend
LEGEND_LABEL_GAP = 0.30               # swatch -> label x offset
LEGEND_LABEL_W = 1.75                 # widest label ~1.42in; no % suffix
# Anchor the legend so its BOTTOM row (200 Propulsion, the column's bottom-most
# segment) lines up with the column's visible 0% baseline; rows step upward from
# there. LEGEND_Y0 is the TOP row's vertical center.
_PL = CHART_STYLE["plot_layout"]
COLUMN_BOTTOM = CHART_FRAME.y + (_PL["y"] + _PL["h"]) * CHART_FRAME.h   # ~6.02in
# The visible 0% baseline sits a hair ABOVE the plot-rectangle bottom (the value-
# axis "0%" label reserves a sliver below it), so pinning the bottom row exactly
# at COLUMN_BOTTOM read slightly low. Lift the whole key by a small tunable amount.
LEGEND_BASELINE_LIFT = 0.08
LEGEND_Y0 = COLUMN_BOTTOM - LEGEND_BASELINE_LIFT - (len(SWBS_SEGMENTS) - 1) * LEGEND_ROW_DY


TEACHING_METADATA = {
    "role": "evidence_grain / hull_confidence_overlay",
    "use_when": (
        "Use for a precision/grain caveat slide that separates a robust program/"
        "vendor-level mix from a narrower confidence-scored exact-hull subset."
    ),
    "teaches": [
        "left confidence table + right native percent-stacked column",
        "A/B vs C/D as a two-band fill (categorical, not a gradient)",
        "focal outline + pale-blue takeaway note for the 31.5% callout",
        "single-category percent stack with native labels on the big segments",
        "tiny segments carried in a manual legend with shares appended",
        "U00 hatched caveat fill in both chart series and legend swatch",
        "two big-number KPI cards translating the chart",
        "an explicit denominator caveat to prevent base conflation",
    ],
}

TEXT_FIT = {
    "confidence_table": {"box_in": (6.055, 2.56), "font_pt": 10,
                         "content": "header + A/B/C/D/X; one-line meanings"},
    "kpi_cards": {"box_in": (2.85, 1.00), "font_pt": "26 KPI / 11 caption",
                  "content": "one number token + one short caption (+ small detail)"},
    "swbs_column": {"frame_in": (2.00, 2.55),
                    "content": "single 100% stacked column; big-3 native % labels"},
}


# ── Local table kit (inlined by design, like the exemplars) ─────────────────
def edge(color, w=12_700):
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", span=1, rowspan=1, **edges):
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 borders=bd(**edges))


# ── Small run/paragraph helpers ─────────────────────────────────────────────
def _r(text, *, size_pt=10, bold=False, italic=False, color=BLACK):
    return run(text, size=PT(size_pt), bold=bold or None, italic=italic or None,
               color=color, font=FONT)


def _p(runs, *, align=None):
    return paragraph(runs, align=align, mar_l=0, indent=0, line_spacing=100_000)


def _empty_para():
    return paragraph([], align="ctr", line_spacing=100_000)


# Reference drop-shadow for KPI cards (verbatim house params).
CALLOUT_SHADOW = (
    '<a:effectLst><a:outerShdw blurRad="50800" dist="38100" dir="2700000" '
    'algn="tl" rotWithShape="0"><a:prstClr val="black"><a:alpha val="40000"/>'
    '</a:prstClr></a:outerShdw></a:effectLst>'
)


# ════════════════════════════════════════════════════════════════════════════
# Paint sections (document order == PowerPoint paint order).
# ════════════════════════════════════════════════════════════════════════════
def paint_zone_headers(out: list[str], ids: ShapeIds) -> None:
    out.append(text_box(
        ids.next(), "LeftZoneHeader", IN(LEFT_X), IN(HEADER_Y), IN(LEFT_W), IN(HEADER_H),
        [_p([_r("All DDG-51 subaward $ \u2014 hull-attribution confidence", size_pt=11, bold=True, color=DK)])],
        fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))
    out.append(text_box(
        ids.next(), "RightZoneHeader", IN(RIGHT_X), IN(HEADER_Y), IN(RIGHT_W), IN(HEADER_H),
        [_p([_r("Recent exact-hull subset \u2014 SWBS mix", size_pt=11, bold=True, color=DK)])],
        fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))
    out.append(connector(ids.next(), "LeftHeaderRule", IN(LEFT_X), IN(RULE_Y), IN(LEFT_W), 0,
                         color=GRAY_MID, width=9_525))
    out.append(connector(ids.next(), "RightHeaderRule", IN(RIGHT_X), IN(RULE_Y), IN(RIGHT_W), 0,
                         color=GRAY_MID, width=9_525))


def paint_divider(out: list[str], ids: ShapeIds) -> None:
    out.append(connector(ids.next(), "ZoneDivider", IN(DIVIDER_X), IN(HEADER_Y), 0, IN(4.52),
                         color=GRAY_3, width=9_525))


def paint_confidence_table(out: list[str], ids: ShapeIds) -> None:
    rows = [trow([
        cell("Confidence", bold=True, align="ctr", anchor="b", B=edge(BLACK)),
        cell("Meaning", bold=True, align="l", anchor="b", B=edge(BLACK)),
        cell("Share of DDG $", bold=True, align="r", anchor="b", B=edge(BLACK)),
    ], h=IN(TABLE_HEADER_H))]

    for i, rw in enumerate(CONFIDENCE_ROWS):
        # Last row (X / "Conflict / review") closes with NO bottom rule; the inner
        # rows keep the thin gray separator.
        bottom = None if i == len(CONFIDENCE_ROWS) - 1 else edge(GRAY_MID, 6_350)
        rows.append(trow([
            cell(rw.code, bold=True, color=rw.code_color, fill=rw.code_fill, align="ctr", B=bottom),
            cell(rw.meaning, align="l", B=bottom),
            cell(rw.share, bold=True, align="r", B=bottom),
        ], h=IN(rw.h)))

    table_h = TABLE_HEADER_H + sum(rw.h for rw in CONFIDENCE_ROWS)
    out.append(table(
        ids.next(), "HullConfidenceTable", IN(TABLE.x), IN(TABLE.y), IN(TABLE.w), IN(table_h),
        col_widths=[IN(w) for w in TABLE_COLS], rows=rows,
    ))


def paint_ab_band(out: list[str], ids: ShapeIds) -> None:
    band_y = TABLE.y + TABLE_HEADER_H
    band_h = sum(CONFIDENCE_ROWS[i].h for i in range(_AB_BAND_ROW_COUNT))
    out.append(text_box(
        ids.next(), "ExactHullBandOutline", IN(TABLE.x), IN(band_y), IN(TABLE.w), IN(band_h),
        [_empty_para()], fill=None, line_color=TEAL, line_width=19_050, anchor="ctr",
    ))


def paint_callout_and_caveat(out: list[str], ids: ShapeIds) -> None:
    out.append(text_box(
        ids.next(), "ExactHull315Callout", *CALLOUT.emu(),
        [_p([_r("A/B exact-hull attribution = 31.5% of DDG $", size_pt=12, bold=True, color=BLACK)], align="ctr")],
        fill=SOFT_BLUE, line_color=TEAL, line_width=12_700, anchor="ctr", effects=CALLOUT_SHADOW,
    ))
    out.append(text_box(
        ids.next(), "DenominatorCaveat", *CAVEAT.emu(),
        [_p([_r("31.5% (A/B) is share of all observed DDG-51 $ (~$4.03B); the $870.9M recent "
                "subset is a curated FY23\u201327 MYP slice within the A/B band.",
                size_pt=9, italic=True, color=DK)])],
        fill=None, line_color="none", anchor="t",
    ))


def paint_zoom_caption(out: list[str], ids: ShapeIds) -> None:
    out.append(text_box(
        ids.next(), "ZoomCaption", *ZOOM_CAPTION.emu(),
        [_p([_r("Zoom into the A/B exact-hull band: recent FY23\u201327 MYP slice (DDG 141\u2013149)",
                size_pt=9, italic=True, color=TEAL)])],
        fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))


def paint_kpi_cards(out: list[str], ids: ShapeIds) -> None:
    out.append(text_box(
        ids.next(), "KpiCardAssignedSpend", *CHIP_A.emu(),
        [
            _p([_r("$870.9M", size_pt=26, bold=True, color=BLACK)], align="ctr"),
            _p([_r("Recent exact-hull assigned spend", size_pt=11, color=BLACK)], align="ctr"),
            _p([_r("FY23\u201327 MYP \u00b7 DDG 141\u2013149", size_pt=9, italic=True, color=GRAY_MID)], align="ctr"),
        ],
        fill=GRAY_1, line_color="none", anchor="ctr", effects=CALLOUT_SHADOW,
    ))
    out.append(text_box(
        ids.next(), "KpiCardCoverage", *CHIP_B.emu(),
        [
            _p([_r("98.5%", size_pt=26, bold=True, color=TEAL)], align="ctr"),
            _p([_r("SWBS coverage of that subset", size_pt=11, color=BLACK)], align="ctr"),
            paragraph([], align="ctr", line_spacing=100_000, end_size=PT(9)),
        ],
        fill=GRAY_1, line_color="none", anchor="ctr", effects=CALLOUT_SHADOW,
    ))


def paint_chart(out: list[str], ids: ShapeIds) -> None:
    out.append(graphic_frame(
        sp_id=ids.next(), name="RecentExactHullSwbsMix",
        x=IN(CHART_FRAME.x), y=IN(CHART_FRAME.y), cx=IN(CHART_FRAME.w), cy=IN(CHART_FRAME.h),
        rId="rId2",
    ))
    # External one-line chart title (house idiom; see Slide 1): bold subject + gray
    # unit qualifier, bottom-anchored just above the column top, no wrap.
    out.append(text_box(
        ids.next(), "ChartTitle", *CHART_TITLE.emu(),
        [_p([_r("Exact-hull subset by SWBS group ", size_pt=10, bold=True, color=BLACK),
             _r("(% of $870.9M; incl. U00)", size_pt=10, color=GRAY_MID)])],
        fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))


def paint_legend(out: list[str], ids: ShapeIds) -> None:
    # Reversed stack order (U00 top -> 200 bottom) so the key reads the same way
    # as the column; the bottom row (200) is level with the column baseline.
    # Chips match the fingerprint legend: uniform size + a thin dark border.
    sw_w, sw_h = LEGEND_SWATCH
    for i, seg in enumerate(reversed(SWBS_SEGMENTS)):
        yc = LEGEND_Y0 + i * LEGEND_ROW_DY            # row center
        sy = yc - sw_h / 2.0                          # swatch top
        if seg.pattern is not None:
            out.append(text_box(
                ids.next(), "LegendSwatchU00", IN(LEGEND_X), IN(sy), IN(sw_w), IN(sw_h),
                [_empty_para()], fill=None, line_color=DK, line_width=3_175,
                pattern_fill=seg.pattern, anchor="ctr",
            ))
        else:
            out.append(text_box(
                ids.next(), "LegendSwatch", IN(LEGEND_X), IN(sy), IN(sw_w), IN(sw_h),
                [_empty_para()], fill=seg.fill, line_color=DK, line_width=3_175, anchor="ctr",
            ))
        out.append(text_box(
            ids.next(), "LegendLabel", IN(LEGEND_X + LEGEND_LABEL_GAP), IN(yc - 0.10),
            IN(LEGEND_LABEL_W), IN(0.20),
            [_p([_r(seg.name, size_pt=9, color=BLACK)])],
            fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))


def paint_zoom_arrow(out: list[str], ids: ShapeIds) -> None:
    band_y = TABLE.y + TABLE_HEADER_H
    band_h = sum(CONFIDENCE_ROWS[i].h for i in range(_AB_BAND_ROW_COUNT))
    arrow_y = band_y + band_h / 2.0
    out.append(connector(
        ids.next(), "ZoomArrow", IN(6.58), IN(arrow_y), IN(0.34), 0,
        color=TEAL, dash="dash", width=12_700, arrow=True,
    ))


def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)
    paint_zone_headers(out, ids)
    paint_divider(out, ids)
    paint_confidence_table(out, ids)
    paint_ab_band(out, ids)
    paint_callout_and_caveat(out, ids)
    paint_zoom_caption(out, ids)
    paint_kpi_cards(out, ids)
    paint_chart(out, ids)
    paint_legend(out, ids)
    paint_zoom_arrow(out, ids)         # painted last so it sits over the divider
    return "".join(out)


# Breadcrumb section/topic and the Sources line are PLACEHOLDERS — match your deck.
CHROME = Chrome(
    section="Market Mapping",
    topic="DDG-51 Subawards",
    title="DDG-51 Hull Attribution",
    takeaway=("SWBS is strong at the HII program/vendor level, while exact hull "
              "attribution is a narrower confidence-scored subset."),
    preliminary=True,
    sources=Sources(
        note="$ in constant FY2026 dollars; shares may not sum to 100% due to rounding",
        source=("USAspending subaward data", "HII-Ingalls reported subawards", "[project workbook]"),
    ),
)


def render() -> str:
    return body_slide(CHROME, _body())
