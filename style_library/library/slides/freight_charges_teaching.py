"""Teaching exemplar: Freight Charges — stacked contribution bar + addressability table.

ROLE
  unit_economics / freight_charge_breakdown

USE WHEN
  A slide needs to decompose one all-in freight price into component charges,
  show which components are vessel-operations-addressable, and connect the chart
  to a short explanatory table.

TEACHES
  - fully declarative native stacked-column charting with column_chart(mode="stacked")
  - source workbook values embedded as Python constants instead of sidecar XLSB
  - source chart-part style values embedded as CHART_STYLE
  - manual on-bar dollar labels over a percentage-normalized stacked chart
  - separate legend/category labels when the chart has a single category
  - status icons and dashed leader lines tied to an explanatory table
  - off-house status note, hyperlinked source note, footnote, and Preliminary chip preservation

TEXT-FIT PRECEDENT
  chart_component_labels:
    geometry: 0.229-0.311in wide x 0.167in high
    type: Arial 10pt, centered, zero/tight insets, no wrap
    content: one short $K value token only, e.g. 2.8 / 0.5 / <0.1
    copy_when: a single stacked bar uses percentage-normalized geometry while the
               audience needs dollarized component labels
  charge_component_table:
    geometry: 6.634in wide x 4.250in high
    type: Arial 10pt with a compact header and six component rows
    copy_when: the chart alone does not explain addressability or pass-through
               mechanics for each price component
  group_captions:
    geometry: 1.37in wide, Arial 10pt italic
    content: short group labels only; avoid paragraph explanations inside brackets

SOURCE NOTE
  Teaching rewrite of source-faithful `freight_charges.py`. The original used a
  `styled_chart(...)` wrapper backed by slide134_chart78.xml/.xlsb. This version
  intentionally replaces that runtime template dependency with a native editable
  `column_chart(mode="stacked", ...)` spec. The chart values are the exact Sheet1
  workbook row from slide134_chart78.xlsb, and the key XML chart styling values
  (manual layout, gap width, overlap, value-axis bounds, segment outlines, and
  series fills) are explicit constants in the module.

FIDELITY NOTE
  This is a practical factory-native rebuild, not a byte-identical chart-template
  port. It preserves the visible chart semantics, percentage-normalized stack,
  manual $K labels, total label, route label, legend, grouping brackets, table,
  custom status icons, leader lines, hyperlinked source note, and Preliminary chip. Minor
  differences can remain in PowerPoint's internal chart XML ordering versus the
  original chart part.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, column_chart, connector, custom_geometry, graphic_frame,
    line_break, paragraph, run, table, tbreak, tcell, tcell_rich, text_box, tpara, trow,
    trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
GRAY_1 = "F2F2F2"
FONT = "Arial"

LAYOUT = "slideLayout4"


# ════════════════════════════════════════════════════════════════════════════
# Source chart data and factory-native chart specification.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class FreightComponent:
    """One bottom-to-top segment in the stacked freight-charge bar."""

    name: str
    fill: str
    workbook_pct: float
    dollar_label_k: str
    addressability_group: str


BASIC_OCEAN_RATE = "364D6E"
FUEL_SURCHARGE = "4C6C9C"
TERMINAL_CHARGE = "808080"
WHARFAGE = "C0C0C0"
OTHER_FEES = WHITE
SEGMENT_OUTLINE = BLACK

CHART_CATEGORIES: tuple[str, ...] = ("Long Beach to Honolulu",)
TOTAL_FREIGHT_CHARGE_K = 4.9

# Exact Sheet1 row read from slide134_chart78.xlsb. These values are percentages
# of the normalized westbound freight charge; manual labels convert the same
# stack into visible $K / TEU labels.
SOURCE_XLSB_COMPONENT_PCT_VALUES: tuple[float, ...] = (
    57.14285714285715,
    10.204081632653061,
    16.326530612244905,
    10.204081632653061,
    2.0408163265306145,
    4.081632653061229,
    0.0,
)

# Exact chart-part styling values pulled from slide134_chart78.xml.
SOURCE_PLOT_LAYOUT = {
    "x": 0.016214530714062987,
    "y": 0.021968736797634135,
    "w": 0.967570938571874,
    "h": 0.9560625264047318,
}
SOURCE_GAP_WIDTH = 250
SOURCE_BAR_OVERLAP = 100
SOURCE_VALUE_AXIS_MIN = 0
SOURCE_VALUE_AXIS_MAX = 110.00000000000001
SOURCE_SEGMENT_LINE_WIDTH = 3_175
SOURCE_AXIS_LINE_WIDTH = 9_525

FREIGHT_COMPONENTS: tuple[FreightComponent, ...] = (
    FreightComponent("Basic Ocean Rate", BASIC_OCEAN_RATE, SOURCE_XLSB_COMPONENT_PCT_VALUES[0], "2.8", "vessel_operations"),
    FreightComponent("Fuel Surcharge", FUEL_SURCHARGE, SOURCE_XLSB_COMPONENT_PCT_VALUES[1], "0.5", "vessel_operations"),
    FreightComponent("Terminal - Long Beach", TERMINAL_CHARGE, SOURCE_XLSB_COMPONENT_PCT_VALUES[2], "0.8", "shoreside"),
    FreightComponent("Terminal - Honolulu", TERMINAL_CHARGE, SOURCE_XLSB_COMPONENT_PCT_VALUES[3], "0.5", "shoreside"),
    FreightComponent("Wharfage - Long Beach", WHARFAGE, SOURCE_XLSB_COMPONENT_PCT_VALUES[4], "0.1", "shoreside"),
    FreightComponent("Wharfage - Honolulu", WHARFAGE, SOURCE_XLSB_COMPONENT_PCT_VALUES[5], "0.2", "shoreside"),
    FreightComponent("Other fees", OTHER_FEES, SOURCE_XLSB_COMPONENT_PCT_VALUES[6], "<0.1", "shoreside"),
)

FREIGHT_CHARGE_SERIES: tuple[dict, ...] = tuple(
    {
        "name": component.name,
        "color": component.fill,
        "values": [component.workbook_pct],
        "hide_labels": True,
    }
    for component in FREIGHT_COMPONENTS
)

# Kept as a readable data mirror for agents/tools that expect the converted-slide
# data-dict shape. CHARTS consumes the same values through column_chart().
_CHART0_DATA = {
    "categories": CHART_CATEGORIES,
    "series": [
        {"name": component.name, "values": [component.workbook_pct]}
        for component in FREIGHT_COMPONENTS
    ],
}

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(CHART_CATEGORIES),
    "series": [dict(series) for series in FREIGHT_CHARGE_SERIES],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": False,
    "show_gridlines": False,
    "show_value_labels": False,
    "value_axis_format": "General",
    "value_label_format": "General",
    "cat_label_size_pt": 10,
    "value_label_size_pt": 10,
    "gap_width": SOURCE_GAP_WIDTH,
    "bar_overlap": SOURCE_BAR_OVERLAP,
    "seg_line_color": SEGMENT_OUTLINE,
    "seg_line_width": SOURCE_SEGMENT_LINE_WIDTH,
    "axis_line_color": BLACK,
    "axis_line_width": SOURCE_AXIS_LINE_WIDTH,
    "value_axis_line_color": "none",      # audit-fix: source hides the value (y) axis; keep only the category spine
    "cat_axis_crosses": "min",            # source chart part uses crosses="min" on both axes
    "value_axis_crosses": "min",
    "value_axis_min": SOURCE_VALUE_AXIS_MIN,
    "value_axis_max": SOURCE_VALUE_AXIS_MAX,
    "plot_layout": dict(SOURCE_PLOT_LAYOUT),
    "cat_header": "Route",
}

CHARTS = [column_chart(**CHART_STYLE)]

# Source-line external links. The native chart takes rId2, so source-note links
# start at rId3 and mirror the source-faithful freight_charges.py module.
HYPERLINKS = [
    {"rId": "rId3", "url": "https://www.pashahawaiitariffs.com/tariffs/rates#0200-00-0500/false/"},
    {"rId": "rId4", "url": "https://www.alohafreight.com/hawaii-fsc-decrease-09-14-25"},
    {"rId": "rId5", "url": "https://hidot.hawaii.gov/harbors/files/2025/04/Cargo-Wharfage-Tariff-Rates-Effective-July-1-2025-June-30-2026.pdf"},
]


TEXT_FIT = {
    "chart_component_labels": {
        "box_in": "0.229-0.311 wide x 0.167 high",
        "font_pt": 10,
        "content": "one short $K value token: 2.8 / 0.5 / 0.8 / 0.1 / <0.1",
        "note": "Use manual labels because the chart values are percentages but visible labels are dollars.",
    },
    "charge_component_table": {
        "box_in": (6.634, 4.250),
        "font_pt": 10,
        "content": "header + six component rows + one italic source-method row",
    },
    "analysis_status_note": {
        "box_in": (3.900, 0.290),
        "font_pt": 10,
        "content": "single italic status sentence",
    },
}


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell()/tcell_rich() form —
#    the only change is legibility. ──
def edge(color, w=12700):
    """One cell-border edge (default 1pt hairline)."""
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Border dict from only the edges drawn; omitted sides render no-fill (as the source does)."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", span=1, rowspan=1,
         l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell with span/align/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...)."""
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell_rich with span/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...)."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_BARVAL_X, _BARVAL_W, _BARVAL_H = IN(3.108), IN(0.229), IN(0.167)   # on-bar $-value-label geometry
_SEG_H = IN(0.167)        # thin-segment value-label height
_KEY_X, _KEY_H = IN(0.585), IN(0.146)    # legend colour-chip x / height
_CAT_X, _CAT_H = IN(0.837), IN(0.167)          # charge-category label x / height
_TXT_H = IN(0.167)        # chart-title / axis-label height        [shared x4]
_LEADER_X = IN(3.99)      # dashed leader-line x                   [shared x5]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the on-bar $ value labels plus the thin-segment $ labels.
_DATA_LABELS = {
    # Main-bar and thin-segment labels retain their distinct geometry/style loops.
    "bar_values": [
        (4.977, "2.8"),
        (3.774, "0.5"),
        (3.3, "0.8"),
        (2.828, "0.5"),
    ],
    "segment_values": [
        (2.724, 2.609, 0.229, "C0C0C0", "0.1"),   # C0C0C0 silver
        (3.493, 2.5, 0.229, None, "0.2"),
        (2.684, 2.427, 0.311, WHITE, "<0.1"),   # FFFFFF white
    ],
}

# local_meaning: the seven charge-component colour chips.
_LEGEND_KEYS = [    # (y, cx, fill) x7 — charge-component colour keys
    (4.201, 0.196, WHITE),   # FFFFFF white
    (4.424, 0.196, "C0C0C0"),   # C0C0C0 silver
    (4.646, 0.196, "C0C0C0"),   # C0C0C0 silver
    (4.868, 0.196, "808080"),   # 808080 gray
    (5.09, 0.196, "808080"),   # 808080 gray
    (5.312, 0.196, "4C6C9C"),   # 4C6C9C blue
    (5.535, 0.196, "364D6E"),   # 364D6E dark blue
]

# local_meaning: the six charge-component captions.
_LEGEND_LABELS = [    # (y, cx, label) x6 — charge-component captions
    (4.196, 0.644, "Other fees"),
    (4.418, 1.267, "Wharfage - Honolulu"),
    (4.641, 1.457, "Wharfage - Long Beach"),
    (4.863, 1.208, "Terminal - Honolulu"),
    (5.085, 1.398, "Terminal - Long Beach"),
    (5.53, 1.113, "Basic Ocean Rate"),
]

# local_meaning: the vessel-operations vs shoreside grouping captions.
_GROUP_CAPTIONS = [    # vessel-operations vs shoreside grouping captions
    (0.71, 5.744, 1.368, 0.307, WHITE, "none", "Directly related to vessel operations"),   # FFFFFF white
    (0.708, 3.92, 1.37, 0.174, WHITE, "none", "Shoreside charges"),   # FFFFFF white
]

# local_meaning: the dated analysis-status annotation.
_ANNOTATION_BOXES = [    # dated analysis-status annotation
    (7.196, 0.122, 3.9, 0.29, GRAY_1, BLACK, "Jan. ’26 analysis; Matson reported ’25 results end of Feb ‘26"),   # F2F2F2 off-white
]

# ── status icons: a colored disc with the check/cross knocked out ──
# The source ships these as think-cell freeform <a:custGeom> shapes. We keep the
# EXACT source vector (renders pixel-identical) but store it as a compact path DSL
# instead of the multi-KB exported blob: think-cell's <a:gdLst>/<a:cxnLst> connection
# metadata (the bulk of the export) draws nothing and is dropped, and the visible
# path uses literal coordinates, so it round-trips losslessly.
#   DSL: "Mx,y" moveTo | "Lx,y" lineTo | "Cx1,y1 x2,y2 x3,y3" cubic bezier | "Z" close
_GLYPH_X = IN(8.302)       # status-icon column x (all 5 icons share it)   [shared x5]
_GLYPH_SZ = IN(0.3)        # status-icon box (square)


def _cust_geom_from_d(w: int, h: int, d: str) -> str:
    """Compact path string -> a DrawingML <a:custGeom> (a real freeform vector, not
    a text glyph). Commands: Mx,y / Lx,y / Cx1,y1 x2,y2 x3,y3 / Z. Coordinates are
    verbatim from the source slide; only think-cell's non-rendering gdLst/cxnLst is
    dropped, so the icon renders identically to the source."""
    def pt(token: str) -> str:
        x, y = token.split(",", 1)
        return f'<a:pt x="{x}" y="{y}"/>'
    toks = d.split()
    out = [f'<a:custGeom><a:avLst/><a:pathLst><a:path w="{w}" h="{h}">']
    i = 0
    while i < len(toks):
        tok = toks[i]
        op = tok[0]
        if op == "M":
            out.append(f"<a:moveTo>{pt(tok[1:])}</a:moveTo>")
            i += 1
        elif op == "L":
            out.append(f"<a:lnTo>{pt(tok[1:])}</a:lnTo>")
            i += 1
        elif op == "C":
            out.append("<a:cubicBezTo>" + pt(tok[1:]) + pt(toks[i + 1]) + pt(toks[i + 2]) + "</a:cubicBezTo>")
            i += 3
        elif tok == "Z":
            out.append("<a:close/>")
            i += 1
        else:
            raise ValueError(f"Unsupported path token: {tok!r}")
    out.append("</a:path></a:pathLst></a:custGeom>")
    return "".join(out)

# Verbatim source path data (slide 134 "Haken, check" / "Cross, kreuz"), compacted.
_CHECK_D = (
    "M4549,3658 C4329,4032 4032,4328 3659,4548 C3285,4768 2879,4877 2439,4877 C2000,4877 1594,4768 1220,4548 C846,4328 "
    "550,4032 330,3658 C110,3284 0,2878 0,2439 C0,1999 110,1593 330,1219 C550,846 846,549 1220,329 C1594,110 2000,0 2439,0 "
    "C2879,0 3285,110 3659,329 C4032,549 4329,846 4549,1219 C4768,1593 4878,1999 4878,2439 C4878,2878 4768,3284 4549,3658 Z "
    "M3963,1917 C3996,1891 4013,1855 4013,1809 C4013,1763 3996,1727 3963,1701 C3747,1475 3747,1475 3747,1475 C3714,1442 "
    "3677,1426 3634,1426 C3591,1426 3554,1442 3521,1475 C2046,2950 2046,2950 2046,2950 C1358,2262 1358,2262 1358,2262 "
    "C1325,2229 1287,2212 1244,2212 C1202,2212 1164,2229 1131,2262 C915,2488 915,2488 915,2488 C882,2514 866,2550 866,2596 "
    "C866,2642 882,2678 915,2704 C1938,3727 1938,3727 1938,3727 C1964,3760 2000,3776 2046,3776 C2092,3776 2128,3760 "
    "2154,3727 L3963,1917 Z"
)
_CROSS_D = (
    "M2438,0 C2878,0 3284,110 3658,329 C4032,549 4328,846 4548,1219 C4767,1593 4877,1999 4877,2439 C4877,2878 4767,3284 "
    "4548,3658 C4328,4032 4032,4328 3658,4548 C3284,4768 2878,4877 2438,4877 C1999,4877 1593,4768 1219,4548 C845,4328 "
    "549,4032 329,3658 C109,3284 0,2878 0,2439 C0,1999 109,1593 329,1219 C549,846 845,549 1219,329 C1593,110 1999,0 2438,0 "
    "Z M3638,3078 C2989,2439 2989,2439 2989,2439 C3638,1799 3638,1799 3638,1799 C3658,1773 3668,1745 3668,1716 C3668,1686 "
    "3658,1659 3638,1632 C3245,1239 3245,1239 3245,1239 C3225,1219 3199,1209 3166,1209 C3133,1209 3104,1219 3078,1239 "
    "C2438,1888 2438,1888 2438,1888 C1799,1239 1799,1239 1799,1239 C1773,1219 1745,1209 1716,1209 C1686,1209 1658,1219 "
    "1632,1239 C1239,1632 1239,1632 1239,1632 C1219,1652 1209,1678 1209,1711 C1209,1744 1219,1773 1239,1799 C1888,2439 "
    "1888,2439 1888,2439 C1239,3078 1239,3078 1239,3078 C1219,3104 1209,3132 1209,3161 C1209,3191 1219,3219 1239,3245 "
    "C1632,3638 1632,3638 1632,3638 C1652,3658 1678,3668 1711,3668 C1744,3668 1773,3658 1799,3638 C2438,2989 2438,2989 "
    "2438,2989 C3078,3638 3078,3638 3078,3638 C3104,3658 3132,3668 3161,3668 C3191,3668 3219,3658 3245,3638 C3638,3245 "
    "3638,3245 3638,3245 C3658,3225 3668,3199 3668,3166 C3668,3134 3658,3104 3638,3078 Z"
)
_GEOM_CHECK = _cust_geom_from_d(4878, 4877, _CHECK_D)   # green check (Haken)
_GEOM_CROSS = _cust_geom_from_d(4877, 4877, _CROSS_D)   # red cross (Kreuz)

# (kind, y_in, fill) x5 — three shoreside crosses, two vessel-ops checks (body call order)
_STATUS_ICONS = (
    ("cross", 2.367, "C00000"),
    ("cross", 2.995, "C00000"),
    ("cross", 3.637, "C00000"),
    ("check", 4.264, "2E7D32"),
    ("check", 4.911, "2E7D32"),
)
_STATUS_GEOMS = {"check": ("Haken, check", _GEOM_CHECK), "cross": ("Cross, kreuz", _GEOM_CROSS)}


# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level convention is expressed by repeating the same
# l_ins/r_ins/t_ins/b_ins and anchor across its cells. In tcell/tcell_rich those
# insets are internal padding and anchor is vertical alignment; tcell align or
# tpara align/mar_l/indent controls horizontal alignment and paragraph margins.

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Omitted values intentionally retain the
# primitive defaults, so layout behavior stays visible at each call site.

# ════════════════════════════════════════════════════════════════════════════
# Paint layer. Helpers are ordered slices of the source paint order (z-order is
# load-bearing here — see paint_shoreside_caption). Each appends to the shared
# sequential id counter `n`, so ids stay identical to the pre-split module.
# ════════════════════════════════════════════════════════════════════════════
def paint_chart_labels(n) -> list[str]:
    """Native chart frame, title, on-bar/thin-segment $K labels, the total and
    route labels, and the vessel-operations grouping frame around the bar."""
    out: list[str] = []
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.439), y=IN(2.062), cx=IN(5.568), cy=IN(4.109), rId="rId2"))
    out.append(text_box(n(), "ChartTitle", IN(0.53), IN(1.87), IN(4.431), _TXT_H, [paragraph([run("Weighted avg. freight charges, normalized on TEU basis ($K, CY25)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    for _y, _t in _DATA_LABELS["bar_values"]:
        out.append(text_box(n(), "BarValueLabel", _BARVAL_X, IN(_y), _BARVAL_W, _BARVAL_H, [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # FFFFFF white
    for _x, _y, _cx, _fill, _t in _DATA_LABELS["segment_values"]:
        out.append(text_box(n(), "BarValueLabel", IN(_x), IN(_y), IN(_cx), _SEG_H, [paragraph([run(_t, size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "TotalFreightChargeLabel", IN(3.108), IN(2.26), IN(0.229), _TXT_H, [paragraph([run("4.9", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    out.append(text_box(n(), "RouteLabel", IN(2.481), IN(6.128), IN(1.484), _TXT_H, [paragraph([run("Long Beach to Honolulu", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "VesselOperationsBracket", IN(0.439), IN(5.297), IN(1.965), IN(0.608), [paragraph([], align="ctr", line_spacing=100000)], fill=WHITE, line_color="364D6E", anchor="ctr"))   # FFFFFF white
    return out


def paint_legend(n) -> list[str]:
    """Charge-component colour chips, their captions, and the Fuel Surcharge
    caption that carries the footnote superscript."""
    out: list[str] = []
    for _y, _cx, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendColorKey", _KEY_X, IN(_y), IN(_cx), _KEY_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=DK, line_width=3175, anchor="ctr"))
    for _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "LegendLabel", _CAT_X, IN(_y), IN(_cx), _CAT_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "LegendLabel", IN(0.837), IN(5.307), IN(0.997), _TXT_H, [paragraph([run("Fuel Surcharge", size=PT(10), color=BLACK, font=FONT), run("1", size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    return out


def paint_charge_component_table(n) -> list[str]:
    """Native addressability table: header + six component rows + italic method row.
    palette - text: 000000 black (labels/descriptions) · FFFFFF white (Terminal/
    Fuel/Ocean labels) · 162029 dark navy (Wharfage desc); fills: C0C0C0 silver
    (Wharfage) · 808080 gray (Terminal) · 4C6C9C blue (Fuel Surcharge) · 364D6E
    dark blue (Basic Ocean Rate); rules: 162029 dark navy (header) · 808080 gray."""
    return [table(n(), "ChargeComponentTable", IN(6.162), IN(1.755), IN(6.634), IN(4.25), col_widths=[IN(1.667), IN(1.219), IN(2.88), IN(0.868)], rows=[
        trow([
            cell("Freight Charges", bold=True, align="ctr", B=edge(DK)),
            cell("ASV Addressability", bold=True, align="ctr", B=edge(DK)),
            cell("Description", bold=True, align="ctr", B=edge(DK)),
            cell("% of total", bold=True, align="ctr", B=edge(DK)),
        ], h=IN(0.322)),
        trow([
            cell("Other Fees", bold=True, T=edge(DK), B=edge("808080", 6350)),
            cell("", align="ctr", T=edge(DK), B=edge("808080", 6350)),
            cell("Port security fees and Hawaii State Invasive Species tax; passed-through to customers", T=edge(DK), B=edge("808080", 6350)),
            cell("<1%", bold=True, align="ctr", T=edge(DK), B=edge("808080", 6350)),
        ], h=IN(0.636)),
        trow([
            cell("Wharfage ", bold=True, fill="C0C0C0", T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("", align="ctr", T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Pier usage fee charged by Ports of Long Beach and Honolulu; passed-through to customers", color=DK, T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("~6%", bold=True, align="ctr", T=edge("808080", 6350), B=edge("808080", 6350)),
        ], h=IN(0.636)),
        trow([
            cell("Terminal Charges ", bold=True, color=WHITE, fill="808080", T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("", align="ctr", T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Handling and stevedoring fees for loading in Long Beach and unloading in Honolulu; likely passed-through but collected by carriers", T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("~26%", bold=True, align="ctr", T=edge("808080", 6350), B=edge("808080", 6350)),
        ], h=IN(0.636)),
        trow([
            rcell([tpara([trun("Fuel Surcharge ", size=PT(10), bold=True, color=WHITE, font=FONT), tbreak(), trun("(or Adjustment Factor)", size=PT(10), italic=True, color=WHITE, font=FONT)])], fill="4C6C9C", T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("", align="ctr", T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Floating fee to protect carrier from fuel price volatility", T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("~10%", bold=True, align="ctr", T=edge("808080", 6350), B=edge("808080", 6350)),
        ], h=IN(0.636)),
        trow([
            cell("Basic Ocean Rate", bold=True, color=WHITE, fill="364D6E", T=edge("808080", 6350)),
            cell("", align="ctr", T=edge("808080", 6350)),
            cell("Core charge for ocean transport; spot rate shown (discounts likely given to high-volume shippers)", T=edge("808080", 6350)),
            cell("~58%", bold=True, align="ctr", T=edge("808080", 6350)),
        ], h=IN(0.636)),
        trow([
            cell("Pasha’s rates calculator breaks out each charge, allowing for isolation of Basic Ocean Rate and Fuel Adjustment Factor", bold=True, italic=True, align="ctr", span=4),
        ], h=IN(0.636)),
    ])]


def paint_status_icons(n) -> list[str]:
    """Colored discs with a check/cross knocked out (verbatim source freeform path).
    Source think-cell glyph names ('Haken, check' / 'Cross, kreuz') are retained."""
    out: list[str] = []
    for _kind, _y, _fill in _STATUS_ICONS:
        _name, _geom = _STATUS_GEOMS[_kind]
        out.append(custom_geometry(n(), _name, _GLYPH_X, IN(_y), _GLYPH_SZ, _GLYPH_SZ, _geom, fill=_fill))
    return out


def paint_addressability_brackets(n) -> list[str]:
    """Vessel-operations group caption, the shoreside grouping bracket, and the
    dated analysis-status annotation."""
    out: list[str] = []
    _x, _y, _cx, _cy, _fill, _lc, _t = _GROUP_CAPTIONS[0]
    out.append(text_box(n(), "VesselOperationsGroupCaption", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, anchor="ctr"))
    out.append(text_box(n(), "ShoresideChargesBracket", IN(0.439), IN(4.009), IN(1.965), IN(1.264), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="969696", anchor="ctr"))   # 969696 gray outline
    for _x, _y, _cx, _cy, _fill, _lc, _t in _ANNOTATION_BOXES:
        out.append(text_box(n(), "AnalysisStatusNote", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, anchor="ctr"))
    return out


def paint_source_note(n) -> list[str]:
    return [text_box(n(), "SourceNote", IN(0.495), IN(6.681), IN(12.367), IN(0.317), [paragraph([run("Note: (1) Matson and Pasha charge a Fuel Surcharge of 16.5% as of September 2025; Basic Ocean Rates largely derived from Pasha Hawaii, whereas Terminal Charges are specific to Matson", size=PT(8), color=BLACK, font=FONT), line_break(), run("Source: ", size=PT(8), color=BLACK, font=FONT), run("Pasha Hawaii", size=PT(8), color=BLACK, hyperlink_rid="rId3", font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("Aloha Freight", size=PT(8), color=BLACK, hyperlink_rid="rId4", font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("Hawaii Department of Transportation", size=PT(8), color=BLACK, hyperlink_rid="rId5", font=FONT)], line_spacing=100000)], fill=None, line_color="none")]   # 000000 black


def paint_vessel_operations_callout(n) -> list[str]:
    """Orange highlight around the addressable charges, the vessel-operations
    explanatory callout, and the dashed leaders from the chart to the table rows."""
    out: list[str] = []
    out.append(text_box(n(), "ChargeComponentHighlight", IN(6.153), IN(4.094), IN(6.643), IN(1.959), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="FB6B3C", line_width=19050, anchor="ctr"))   # FB6B3C orange outline
    out.append(text_box(n(), "VesselOperationsCallout", IN(7.548), IN(5.909), IN(5.054), IN(0.293), [paragraph([run("Directly related to vessel operations; percentage varies based on basic ocean rate, fuel surcharge, discounts, and other factors ", size=PT(10), bold=True, color="FB6B3C", font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))   # FFFFFF white
    out.append(connector(n(), "ChargeLeader_TerminalCharges", _LEADER_X, IN(4.052), IN(2.162), IN(0.696), color="808080", width=12700, dash="dash"))   # 808080 gray
    out.append(connector(n(), "ChargeLeader_WharfageHNL", _LEADER_X, IN(3.691), IN(2.171), IN(0.426), color="808080", width=12700, dash="dash"))   # 808080 gray
    out.append(connector(n(), "ChargeLeader_WharfageLB", _LEADER_X, IN(2.729), IN(2.162), IN(0.704), color="808080", width=12700, dash="dash"))   # 808080 gray
    out.append(connector(n(), "ChargeLeader_TerminalHNL", _LEADER_X, IN(2.528), IN(2.171), IN(0.308), color="808080", width=12700, dash="dash"))   # 808080 gray
    out.append(connector(n(), "ChargeLeader_OtherFees", _LEADER_X, IN(2.2), IN(2.135), IN(0.3), color="808080", width=12700, dash="dash", flip_v=True))   # 808080 gray
    return out


def paint_shoreside_caption(n) -> list[str]:
    """'Shoreside charges' caption. Source paint order matters: it is drawn after
    the bracket and leaders so the white label sits in front of the border line."""
    _x, _y, _cx, _cy, _fill, _lc, _t = _GROUP_CAPTIONS[1]
    return [text_box(n(), "ShoresideChargesGroupCaption", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, anchor="ctr")]


def paint_spot_rate_callout(n) -> list[str]:
    return [text_box(n(), "SpotRateCallout", IN(0.53), IN(1.447), IN(3.2), IN(0.244), [paragraph([run("Spot Rate from CONUS", size=PT(11), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color="none", anchor="ctr")]   # CEDDEC pale blue


def _body() -> str:
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE.
    # Paint order is the source z-order; ids stay sequential via the shared `n`.
    out: list[str] = []
    out += paint_chart_labels(n)
    out += paint_legend(n)
    out += paint_charge_component_table(n)
    out += paint_status_icons(n)
    out += paint_addressability_brackets(n)
    out += paint_source_note(n)
    out += paint_vessel_operations_callout(n)
    out += paint_shoreside_caption(n)
    out += paint_spot_rate_callout(n)
    return "".join(out)


CHROME = Chrome(
    section="Carrier Entry Point Attractiveness",
    topic="Matson Test Case",
    title="Freight Charges",
    takeaway="~70% of westbound freight charges are directly related to vessel operations; other charges pertain to shoreside activities.",
)


def render() -> str:
    return body_slide(CHROME, _body())
