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
  - source chart-part style values embedded as CHART_STYLE and SOURCE_CHART_AUDIT
  - manual on-bar dollar labels over a percentage-normalized stacked chart
  - separate legend/category labels when the chart has a single category
  - status icons and dashed leader lines tied to an explanatory table
  - off-house status note, footnote, and Preliminary chip preservation

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
  custom status icons, leader lines, source note, and Preliminary chip. Minor
  differences can remain in PowerPoint's internal chart XML ordering versus the
  original chart part.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from dataclasses import dataclass

from deck_core.primitives import (
    slide, run, paragraph, text_box, custom_geometry, connector, line_break, table, trow, tcell, tcell_rich, tpara, trun, tbreak, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.charts import graphic_frame, column_chart
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, FONT

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
SOURCE_VALUE_AXIS_MAJOR_UNIT = None  # source XML omits <c:majorUnit>
SOURCE_SEGMENT_LINE_WIDTH = 3_175
SOURCE_AXIS_LINE_WIDTH = 9_525
SOURCE_XML_COMPONENT_FILL_COLORS: tuple[str, ...] = (
    BASIC_OCEAN_RATE,
    FUEL_SURCHARGE,
    TERMINAL_CHARGE,
    TERMINAL_CHARGE,
    WHARFAGE,
    WHARFAGE,
    OTHER_FEES,
)

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
    "value_axis_min": SOURCE_VALUE_AXIS_MIN,
    "value_axis_max": SOURCE_VALUE_AXIS_MAX,
    "plot_layout": dict(SOURCE_PLOT_LAYOUT),
    "cat_header": "Route",
}

CHARTS = [column_chart(**CHART_STYLE)]

SOURCE_CHART_AUDIT = {
    "source_xml": "slide134_chart78.xml",
    "source_workbook": "slide134_chart78.xlsb",
    "workbook_rows": [SOURCE_XLSB_COMPONENT_PCT_VALUES],
    "xml_style": {
        "manualLayout": SOURCE_PLOT_LAYOUT,
        "barDir": "col",
        "grouping": "stacked",
        "gapWidth": SOURCE_GAP_WIDTH,
        "overlap": SOURCE_BAR_OVERLAP,
        "valueAxisMin": SOURCE_VALUE_AXIS_MIN,
        "valueAxisMax": SOURCE_VALUE_AXIS_MAX,
        "valueAxisMajorUnit": SOURCE_VALUE_AXIS_MAJOR_UNIT,
        "segmentLineWidth": SOURCE_SEGMENT_LINE_WIDTH,
        "axisLineWidth": SOURCE_AXIS_LINE_WIDTH,
        "seriesFillsBottomToTop": SOURCE_XML_COMPONENT_FILL_COLORS,
    },
}


def _validate_source_chart_alignment() -> None:
    """Fail fast if a future edit drifts from the source XML/XLSB values."""

    if len(CHART_CATEGORIES) != 1:
        raise ValueError("slide134_chart78 contains exactly one chart category / stacked bar.")
    if len(FREIGHT_COMPONENTS) != 7:
        raise ValueError("Expected seven freight-charge components from slide134_chart78.xlsb.")
    actual_values = tuple(component.workbook_pct for component in FREIGHT_COMPONENTS)
    if actual_values != SOURCE_XLSB_COMPONENT_PCT_VALUES:
        raise ValueError("Freight component percentages no longer match slide134_chart78.xlsb.")
    actual_colors = tuple(component.fill for component in FREIGHT_COMPONENTS)
    if actual_colors != SOURCE_XML_COMPONENT_FILL_COLORS:
        raise ValueError("Freight component fills no longer match slide134_chart78.xml series colors.")
    if abs(sum(SOURCE_XLSB_COMPONENT_PCT_VALUES) - 100.0) > 1e-9:
        raise ValueError("Freight component percentages should sum to the source 100% stack.")
    if CHART_STYLE["gap_width"] != SOURCE_GAP_WIDTH or CHART_STYLE["bar_overlap"] != SOURCE_BAR_OVERLAP:
        raise ValueError("Chart gap/overlap must match slide134_chart78.xml.")
    if CHART_STYLE["plot_layout"] != SOURCE_PLOT_LAYOUT:
        raise ValueError("Manual plot layout must match slide134_chart78.xml.")
    if CHART_STYLE["value_axis_min"] != SOURCE_VALUE_AXIS_MIN or CHART_STYLE["value_axis_max"] != SOURCE_VALUE_AXIS_MAX:
        raise ValueError("Value-axis bounds must match slide134_chart78.xml.")
    if SOURCE_VALUE_AXIS_MAJOR_UNIT is None and "value_axis_major_unit" in CHART_STYLE:
        raise ValueError("Source XML omits c:majorUnit; do not hard-code a native major unit.")
    if CHART_STYLE["seg_line_width"] != SOURCE_SEGMENT_LINE_WIDTH:
        raise ValueError("Segment outline width must match slide134_chart78.xml.")


_validate_source_chart_alignment()


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: these are comments the module can expose programmatically.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "unit_economics / freight_charge_breakdown",
    "use_when": (
        "Use for a single-route freight price decomposition where one stacked "
        "chart needs to be read with a component legend, addressability table, "
        "and explicit vessel-operations vs. shoreside grouping."
    ),
    "teaches": [
        "native stacked column chart with one category",
        "source workbook values embedded as Python constants",
        "source XML styling embedded in CHART_STYLE",
        "manual dollar-value labels over percentage-normalized geometry",
        "manual legend labels for one-bar composition charts",
        "custom geometry status icons in an explanatory table",
        "dashed leader lines from chart components to table rows",
    ],
    "source_module": "freight_charges.py",
    "rebuild_strategy": "replace styled_chart template with native column_chart",
}

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
_SWATCH_X, _SWATCH_H = IN(0.585), IN(0.146)    # legend colour-chip x / height
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

# Two think-cell status-icon geometries (check / cross), de-duplicated out of the
# body into custom_geometry() calls. The bézier path data is intrinsic (custGeom),
# so each path stays verbatim in ONE named constant; position / fill are params.
_GLYPH_X = IN(8.302)       # status-icon column x (all 5 icons share it)   [shared x5]
_GLYPH_SZ = IN(0.3)        # status-icon box (square)
_GEOM_CHECK = "<a:custGeom><a:avLst /><a:gdLst><a:gd name=\"T0\" fmla=\"*/ 4549 w 4878\" /><a:gd name=\"T1\" fmla=\"*/ 3658 h 4877\" /><a:gd name=\"T2\" fmla=\"*/ 3659 w 4878\" /><a:gd name=\"T3\" fmla=\"*/ 4548 h 4877\" /><a:gd name=\"T4\" fmla=\"*/ 2439 w 4878\" /><a:gd name=\"T5\" fmla=\"*/ 4877 h 4877\" /><a:gd name=\"T6\" fmla=\"*/ 1220 w 4878\" /><a:gd name=\"T7\" fmla=\"*/ 4548 h 4877\" /><a:gd name=\"T8\" fmla=\"*/ 330 w 4878\" /><a:gd name=\"T9\" fmla=\"*/ 3658 h 4877\" /><a:gd name=\"T10\" fmla=\"*/ 0 w 4878\" /><a:gd name=\"T11\" fmla=\"*/ 2439 h 4877\" /><a:gd name=\"T12\" fmla=\"*/ 330 w 4878\" /><a:gd name=\"T13\" fmla=\"*/ 1219 h 4877\" /><a:gd name=\"T14\" fmla=\"*/ 1220 w 4878\" /><a:gd name=\"T15\" fmla=\"*/ 329 h 4877\" /><a:gd name=\"T16\" fmla=\"*/ 2439 w 4878\" /><a:gd name=\"T17\" fmla=\"*/ 0 h 4877\" /><a:gd name=\"T18\" fmla=\"*/ 3659 w 4878\" /><a:gd name=\"T19\" fmla=\"*/ 329 h 4877\" /><a:gd name=\"T20\" fmla=\"*/ 4549 w 4878\" /><a:gd name=\"T21\" fmla=\"*/ 1219 h 4877\" /><a:gd name=\"T22\" fmla=\"*/ 4878 w 4878\" /><a:gd name=\"T23\" fmla=\"*/ 2439 h 4877\" /><a:gd name=\"T24\" fmla=\"*/ 4549 w 4878\" /><a:gd name=\"T25\" fmla=\"*/ 3658 h 4877\" /><a:gd name=\"T26\" fmla=\"*/ 3963 w 4878\" /><a:gd name=\"T27\" fmla=\"*/ 1917 h 4877\" /><a:gd name=\"T28\" fmla=\"*/ 4013 w 4878\" /><a:gd name=\"T29\" fmla=\"*/ 1809 h 4877\" /><a:gd name=\"T30\" fmla=\"*/ 3963 w 4878\" /><a:gd name=\"T31\" fmla=\"*/ 1701 h 4877\" /><a:gd name=\"T32\" fmla=\"*/ 3747 w 4878\" /><a:gd name=\"T33\" fmla=\"*/ 1475 h 4877\" /><a:gd name=\"T34\" fmla=\"*/ 3634 w 4878\" /><a:gd name=\"T35\" fmla=\"*/ 1426 h 4877\" /><a:gd name=\"T36\" fmla=\"*/ 3521 w 4878\" /><a:gd name=\"T37\" fmla=\"*/ 1475 h 4877\" /><a:gd name=\"T38\" fmla=\"*/ 2046 w 4878\" /><a:gd name=\"T39\" fmla=\"*/ 2950 h 4877\" /><a:gd name=\"T40\" fmla=\"*/ 1358 w 4878\" /><a:gd name=\"T41\" fmla=\"*/ 2262 h 4877\" /><a:gd name=\"T42\" fmla=\"*/ 1244 w 4878\" /><a:gd name=\"T43\" fmla=\"*/ 2212 h 4877\" /><a:gd name=\"T44\" fmla=\"*/ 1131 w 4878\" /><a:gd name=\"T45\" fmla=\"*/ 2262 h 4877\" /><a:gd name=\"T46\" fmla=\"*/ 915 w 4878\" /><a:gd name=\"T47\" fmla=\"*/ 2488 h 4877\" /><a:gd name=\"T48\" fmla=\"*/ 866 w 4878\" /><a:gd name=\"T49\" fmla=\"*/ 2596 h 4877\" /><a:gd name=\"T50\" fmla=\"*/ 915 w 4878\" /><a:gd name=\"T51\" fmla=\"*/ 2704 h 4877\" /><a:gd name=\"T52\" fmla=\"*/ 1938 w 4878\" /><a:gd name=\"T53\" fmla=\"*/ 3727 h 4877\" /><a:gd name=\"T54\" fmla=\"*/ 2046 w 4878\" /><a:gd name=\"T55\" fmla=\"*/ 3776 h 4877\" /><a:gd name=\"T56\" fmla=\"*/ 2154 w 4878\" /><a:gd name=\"T57\" fmla=\"*/ 3727 h 4877\" /><a:gd name=\"T58\" fmla=\"*/ 3963 w 4878\" /><a:gd name=\"T59\" fmla=\"*/ 1917 h 4877\" /></a:gdLst><a:ahLst /><a:cxnLst><a:cxn ang=\"0\"><a:pos x=\"T0\" y=\"T1\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T2\" y=\"T3\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T4\" y=\"T5\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T6\" y=\"T7\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T8\" y=\"T9\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T10\" y=\"T11\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T12\" y=\"T13\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T14\" y=\"T15\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T16\" y=\"T17\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T18\" y=\"T19\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T20\" y=\"T21\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T22\" y=\"T23\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T24\" y=\"T25\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T26\" y=\"T27\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T28\" y=\"T29\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T30\" y=\"T31\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T32\" y=\"T33\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T34\" y=\"T35\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T36\" y=\"T37\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T38\" y=\"T39\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T40\" y=\"T41\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T42\" y=\"T43\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T44\" y=\"T45\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T46\" y=\"T47\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T48\" y=\"T49\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T50\" y=\"T51\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T52\" y=\"T53\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T54\" y=\"T55\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T56\" y=\"T57\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T58\" y=\"T59\" /></a:cxn></a:cxnLst><a:rect l=\"0\" t=\"0\" r=\"r\" b=\"b\" /><a:pathLst><a:path w=\"4878\" h=\"4877\"><a:moveTo><a:pt x=\"4549\" y=\"3658\" /></a:moveTo><a:cubicBezTo><a:pt x=\"4329\" y=\"4032\" /><a:pt x=\"4032\" y=\"4328\" /><a:pt x=\"3659\" y=\"4548\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3285\" y=\"4768\" /><a:pt x=\"2879\" y=\"4877\" /><a:pt x=\"2439\" y=\"4877\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"2000\" y=\"4877\" /><a:pt x=\"1594\" y=\"4768\" /><a:pt x=\"1220\" y=\"4548\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"846\" y=\"4328\" /><a:pt x=\"550\" y=\"4032\" /><a:pt x=\"330\" y=\"3658\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"110\" y=\"3284\" /><a:pt x=\"0\" y=\"2878\" /><a:pt x=\"0\" y=\"2439\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"0\" y=\"1999\" /><a:pt x=\"110\" y=\"1593\" /><a:pt x=\"330\" y=\"1219\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"550\" y=\"846\" /><a:pt x=\"846\" y=\"549\" /><a:pt x=\"1220\" y=\"329\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1594\" y=\"110\" /><a:pt x=\"2000\" y=\"0\" /><a:pt x=\"2439\" y=\"0\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"2879\" y=\"0\" /><a:pt x=\"3285\" y=\"110\" /><a:pt x=\"3659\" y=\"329\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"4032\" y=\"549\" /><a:pt x=\"4329\" y=\"846\" /><a:pt x=\"4549\" y=\"1219\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"4768\" y=\"1593\" /><a:pt x=\"4878\" y=\"1999\" /><a:pt x=\"4878\" y=\"2439\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"4878\" y=\"2878\" /><a:pt x=\"4768\" y=\"3284\" /><a:pt x=\"4549\" y=\"3658\" /></a:cubicBezTo><a:close /><a:moveTo><a:pt x=\"3963\" y=\"1917\" /></a:moveTo><a:cubicBezTo><a:pt x=\"3996\" y=\"1891\" /><a:pt x=\"4013\" y=\"1855\" /><a:pt x=\"4013\" y=\"1809\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"4013\" y=\"1763\" /><a:pt x=\"3996\" y=\"1727\" /><a:pt x=\"3963\" y=\"1701\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3747\" y=\"1475\" /><a:pt x=\"3747\" y=\"1475\" /><a:pt x=\"3747\" y=\"1475\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3714\" y=\"1442\" /><a:pt x=\"3677\" y=\"1426\" /><a:pt x=\"3634\" y=\"1426\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3591\" y=\"1426\" /><a:pt x=\"3554\" y=\"1442\" /><a:pt x=\"3521\" y=\"1475\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"2046\" y=\"2950\" /><a:pt x=\"2046\" y=\"2950\" /><a:pt x=\"2046\" y=\"2950\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1358\" y=\"2262\" /><a:pt x=\"1358\" y=\"2262\" /><a:pt x=\"1358\" y=\"2262\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1325\" y=\"2229\" /><a:pt x=\"1287\" y=\"2212\" /><a:pt x=\"1244\" y=\"2212\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1202\" y=\"2212\" /><a:pt x=\"1164\" y=\"2229\" /><a:pt x=\"1131\" y=\"2262\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"915\" y=\"2488\" /><a:pt x=\"915\" y=\"2488\" /><a:pt x=\"915\" y=\"2488\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"882\" y=\"2514\" /><a:pt x=\"866\" y=\"2550\" /><a:pt x=\"866\" y=\"2596\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"866\" y=\"2642\" /><a:pt x=\"882\" y=\"2678\" /><a:pt x=\"915\" y=\"2704\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1938\" y=\"3727\" /><a:pt x=\"1938\" y=\"3727\" /><a:pt x=\"1938\" y=\"3727\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1964\" y=\"3760\" /><a:pt x=\"2000\" y=\"3776\" /><a:pt x=\"2046\" y=\"3776\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"2092\" y=\"3776\" /><a:pt x=\"2128\" y=\"3760\" /><a:pt x=\"2154\" y=\"3727\" /></a:cubicBezTo><a:lnTo><a:pt x=\"3963\" y=\"1917\" /></a:lnTo><a:close /></a:path></a:pathLst></a:custGeom>"   # green check (Haken)
_GEOM_CROSS = "<a:custGeom><a:avLst /><a:gdLst><a:gd name=\"T0\" fmla=\"*/ 2438 w 4877\" /><a:gd name=\"T1\" fmla=\"*/ 0 h 4877\" /><a:gd name=\"T2\" fmla=\"*/ 3658 w 4877\" /><a:gd name=\"T3\" fmla=\"*/ 329 h 4877\" /><a:gd name=\"T4\" fmla=\"*/ 4548 w 4877\" /><a:gd name=\"T5\" fmla=\"*/ 1219 h 4877\" /><a:gd name=\"T6\" fmla=\"*/ 4877 w 4877\" /><a:gd name=\"T7\" fmla=\"*/ 2439 h 4877\" /><a:gd name=\"T8\" fmla=\"*/ 4548 w 4877\" /><a:gd name=\"T9\" fmla=\"*/ 3658 h 4877\" /><a:gd name=\"T10\" fmla=\"*/ 3658 w 4877\" /><a:gd name=\"T11\" fmla=\"*/ 4548 h 4877\" /><a:gd name=\"T12\" fmla=\"*/ 2438 w 4877\" /><a:gd name=\"T13\" fmla=\"*/ 4877 h 4877\" /><a:gd name=\"T14\" fmla=\"*/ 1219 w 4877\" /><a:gd name=\"T15\" fmla=\"*/ 4548 h 4877\" /><a:gd name=\"T16\" fmla=\"*/ 329 w 4877\" /><a:gd name=\"T17\" fmla=\"*/ 3658 h 4877\" /><a:gd name=\"T18\" fmla=\"*/ 0 w 4877\" /><a:gd name=\"T19\" fmla=\"*/ 2439 h 4877\" /><a:gd name=\"T20\" fmla=\"*/ 329 w 4877\" /><a:gd name=\"T21\" fmla=\"*/ 1219 h 4877\" /><a:gd name=\"T22\" fmla=\"*/ 1219 w 4877\" /><a:gd name=\"T23\" fmla=\"*/ 329 h 4877\" /><a:gd name=\"T24\" fmla=\"*/ 2438 w 4877\" /><a:gd name=\"T25\" fmla=\"*/ 0 h 4877\" /><a:gd name=\"T26\" fmla=\"*/ 3638 w 4877\" /><a:gd name=\"T27\" fmla=\"*/ 3078 h 4877\" /><a:gd name=\"T28\" fmla=\"*/ 2989 w 4877\" /><a:gd name=\"T29\" fmla=\"*/ 2439 h 4877\" /><a:gd name=\"T30\" fmla=\"*/ 3638 w 4877\" /><a:gd name=\"T31\" fmla=\"*/ 1799 h 4877\" /><a:gd name=\"T32\" fmla=\"*/ 3668 w 4877\" /><a:gd name=\"T33\" fmla=\"*/ 1716 h 4877\" /><a:gd name=\"T34\" fmla=\"*/ 3638 w 4877\" /><a:gd name=\"T35\" fmla=\"*/ 1632 h 4877\" /><a:gd name=\"T36\" fmla=\"*/ 3245 w 4877\" /><a:gd name=\"T37\" fmla=\"*/ 1239 h 4877\" /><a:gd name=\"T38\" fmla=\"*/ 3166 w 4877\" /><a:gd name=\"T39\" fmla=\"*/ 1209 h 4877\" /><a:gd name=\"T40\" fmla=\"*/ 3078 w 4877\" /><a:gd name=\"T41\" fmla=\"*/ 1239 h 4877\" /><a:gd name=\"T42\" fmla=\"*/ 2438 w 4877\" /><a:gd name=\"T43\" fmla=\"*/ 1888 h 4877\" /><a:gd name=\"T44\" fmla=\"*/ 1799 w 4877\" /><a:gd name=\"T45\" fmla=\"*/ 1239 h 4877\" /><a:gd name=\"T46\" fmla=\"*/ 1716 w 4877\" /><a:gd name=\"T47\" fmla=\"*/ 1209 h 4877\" /><a:gd name=\"T48\" fmla=\"*/ 1632 w 4877\" /><a:gd name=\"T49\" fmla=\"*/ 1239 h 4877\" /><a:gd name=\"T50\" fmla=\"*/ 1239 w 4877\" /><a:gd name=\"T51\" fmla=\"*/ 1632 h 4877\" /><a:gd name=\"T52\" fmla=\"*/ 1209 w 4877\" /><a:gd name=\"T53\" fmla=\"*/ 1711 h 4877\" /><a:gd name=\"T54\" fmla=\"*/ 1239 w 4877\" /><a:gd name=\"T55\" fmla=\"*/ 1799 h 4877\" /><a:gd name=\"T56\" fmla=\"*/ 1888 w 4877\" /><a:gd name=\"T57\" fmla=\"*/ 2439 h 4877\" /><a:gd name=\"T58\" fmla=\"*/ 1239 w 4877\" /><a:gd name=\"T59\" fmla=\"*/ 3078 h 4877\" /><a:gd name=\"T60\" fmla=\"*/ 1209 w 4877\" /><a:gd name=\"T61\" fmla=\"*/ 3161 h 4877\" /><a:gd name=\"T62\" fmla=\"*/ 1239 w 4877\" /><a:gd name=\"T63\" fmla=\"*/ 3245 h 4877\" /><a:gd name=\"T64\" fmla=\"*/ 1632 w 4877\" /><a:gd name=\"T65\" fmla=\"*/ 3638 h 4877\" /><a:gd name=\"T66\" fmla=\"*/ 1711 w 4877\" /><a:gd name=\"T67\" fmla=\"*/ 3668 h 4877\" /><a:gd name=\"T68\" fmla=\"*/ 1799 w 4877\" /><a:gd name=\"T69\" fmla=\"*/ 3638 h 4877\" /><a:gd name=\"T70\" fmla=\"*/ 2438 w 4877\" /><a:gd name=\"T71\" fmla=\"*/ 2989 h 4877\" /><a:gd name=\"T72\" fmla=\"*/ 3078 w 4877\" /><a:gd name=\"T73\" fmla=\"*/ 3638 h 4877\" /><a:gd name=\"T74\" fmla=\"*/ 3161 w 4877\" /><a:gd name=\"T75\" fmla=\"*/ 3668 h 4877\" /><a:gd name=\"T76\" fmla=\"*/ 3245 w 4877\" /><a:gd name=\"T77\" fmla=\"*/ 3638 h 4877\" /><a:gd name=\"T78\" fmla=\"*/ 3638 w 4877\" /><a:gd name=\"T79\" fmla=\"*/ 3245 h 4877\" /><a:gd name=\"T80\" fmla=\"*/ 3668 w 4877\" /><a:gd name=\"T81\" fmla=\"*/ 3166 h 4877\" /><a:gd name=\"T82\" fmla=\"*/ 3638 w 4877\" /><a:gd name=\"T83\" fmla=\"*/ 3078 h 4877\" /></a:gdLst><a:ahLst /><a:cxnLst><a:cxn ang=\"0\"><a:pos x=\"T0\" y=\"T1\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T2\" y=\"T3\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T4\" y=\"T5\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T6\" y=\"T7\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T8\" y=\"T9\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T10\" y=\"T11\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T12\" y=\"T13\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T14\" y=\"T15\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T16\" y=\"T17\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T18\" y=\"T19\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T20\" y=\"T21\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T22\" y=\"T23\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T24\" y=\"T25\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T26\" y=\"T27\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T28\" y=\"T29\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T30\" y=\"T31\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T32\" y=\"T33\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T34\" y=\"T35\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T36\" y=\"T37\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T38\" y=\"T39\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T40\" y=\"T41\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T42\" y=\"T43\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T44\" y=\"T45\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T46\" y=\"T47\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T48\" y=\"T49\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T50\" y=\"T51\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T52\" y=\"T53\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T54\" y=\"T55\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T56\" y=\"T57\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T58\" y=\"T59\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T60\" y=\"T61\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T62\" y=\"T63\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T64\" y=\"T65\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T66\" y=\"T67\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T68\" y=\"T69\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T70\" y=\"T71\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T72\" y=\"T73\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T74\" y=\"T75\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T76\" y=\"T77\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T78\" y=\"T79\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T80\" y=\"T81\" /></a:cxn><a:cxn ang=\"0\"><a:pos x=\"T82\" y=\"T83\" /></a:cxn></a:cxnLst><a:rect l=\"0\" t=\"0\" r=\"r\" b=\"b\" /><a:pathLst><a:path w=\"4877\" h=\"4877\"><a:moveTo><a:pt x=\"2438\" y=\"0\" /></a:moveTo><a:cubicBezTo><a:pt x=\"2878\" y=\"0\" /><a:pt x=\"3284\" y=\"110\" /><a:pt x=\"3658\" y=\"329\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"4032\" y=\"549\" /><a:pt x=\"4328\" y=\"846\" /><a:pt x=\"4548\" y=\"1219\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"4767\" y=\"1593\" /><a:pt x=\"4877\" y=\"1999\" /><a:pt x=\"4877\" y=\"2439\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"4877\" y=\"2878\" /><a:pt x=\"4767\" y=\"3284\" /><a:pt x=\"4548\" y=\"3658\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"4328\" y=\"4032\" /><a:pt x=\"4032\" y=\"4328\" /><a:pt x=\"3658\" y=\"4548\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3284\" y=\"4768\" /><a:pt x=\"2878\" y=\"4877\" /><a:pt x=\"2438\" y=\"4877\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1999\" y=\"4877\" /><a:pt x=\"1593\" y=\"4768\" /><a:pt x=\"1219\" y=\"4548\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"845\" y=\"4328\" /><a:pt x=\"549\" y=\"4032\" /><a:pt x=\"329\" y=\"3658\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"109\" y=\"3284\" /><a:pt x=\"0\" y=\"2878\" /><a:pt x=\"0\" y=\"2439\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"0\" y=\"1999\" /><a:pt x=\"109\" y=\"1593\" /><a:pt x=\"329\" y=\"1219\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"549\" y=\"846\" /><a:pt x=\"845\" y=\"549\" /><a:pt x=\"1219\" y=\"329\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1593\" y=\"110\" /><a:pt x=\"1999\" y=\"0\" /><a:pt x=\"2438\" y=\"0\" /></a:cubicBezTo><a:close /><a:moveTo><a:pt x=\"3638\" y=\"3078\" /></a:moveTo><a:cubicBezTo><a:pt x=\"2989\" y=\"2439\" /><a:pt x=\"2989\" y=\"2439\" /><a:pt x=\"2989\" y=\"2439\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3638\" y=\"1799\" /><a:pt x=\"3638\" y=\"1799\" /><a:pt x=\"3638\" y=\"1799\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3658\" y=\"1773\" /><a:pt x=\"3668\" y=\"1745\" /><a:pt x=\"3668\" y=\"1716\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3668\" y=\"1686\" /><a:pt x=\"3658\" y=\"1659\" /><a:pt x=\"3638\" y=\"1632\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3245\" y=\"1239\" /><a:pt x=\"3245\" y=\"1239\" /><a:pt x=\"3245\" y=\"1239\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3225\" y=\"1219\" /><a:pt x=\"3199\" y=\"1209\" /><a:pt x=\"3166\" y=\"1209\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3133\" y=\"1209\" /><a:pt x=\"3104\" y=\"1219\" /><a:pt x=\"3078\" y=\"1239\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"2438\" y=\"1888\" /><a:pt x=\"2438\" y=\"1888\" /><a:pt x=\"2438\" y=\"1888\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1799\" y=\"1239\" /><a:pt x=\"1799\" y=\"1239\" /><a:pt x=\"1799\" y=\"1239\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1773\" y=\"1219\" /><a:pt x=\"1745\" y=\"1209\" /><a:pt x=\"1716\" y=\"1209\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1686\" y=\"1209\" /><a:pt x=\"1658\" y=\"1219\" /><a:pt x=\"1632\" y=\"1239\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1239\" y=\"1632\" /><a:pt x=\"1239\" y=\"1632\" /><a:pt x=\"1239\" y=\"1632\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1219\" y=\"1652\" /><a:pt x=\"1209\" y=\"1678\" /><a:pt x=\"1209\" y=\"1711\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1209\" y=\"1744\" /><a:pt x=\"1219\" y=\"1773\" /><a:pt x=\"1239\" y=\"1799\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1888\" y=\"2439\" /><a:pt x=\"1888\" y=\"2439\" /><a:pt x=\"1888\" y=\"2439\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1239\" y=\"3078\" /><a:pt x=\"1239\" y=\"3078\" /><a:pt x=\"1239\" y=\"3078\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1219\" y=\"3104\" /><a:pt x=\"1209\" y=\"3132\" /><a:pt x=\"1209\" y=\"3161\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1209\" y=\"3191\" /><a:pt x=\"1219\" y=\"3219\" /><a:pt x=\"1239\" y=\"3245\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1632\" y=\"3638\" /><a:pt x=\"1632\" y=\"3638\" /><a:pt x=\"1632\" y=\"3638\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1652\" y=\"3658\" /><a:pt x=\"1678\" y=\"3668\" /><a:pt x=\"1711\" y=\"3668\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"1744\" y=\"3668\" /><a:pt x=\"1773\" y=\"3658\" /><a:pt x=\"1799\" y=\"3638\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"2438\" y=\"2989\" /><a:pt x=\"2438\" y=\"2989\" /><a:pt x=\"2438\" y=\"2989\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3078\" y=\"3638\" /><a:pt x=\"3078\" y=\"3638\" /><a:pt x=\"3078\" y=\"3638\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3104\" y=\"3658\" /><a:pt x=\"3132\" y=\"3668\" /><a:pt x=\"3161\" y=\"3668\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3191\" y=\"3668\" /><a:pt x=\"3219\" y=\"3658\" /><a:pt x=\"3245\" y=\"3638\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3638\" y=\"3245\" /><a:pt x=\"3638\" y=\"3245\" /><a:pt x=\"3638\" y=\"3245\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3658\" y=\"3225\" /><a:pt x=\"3668\" y=\"3199\" /><a:pt x=\"3668\" y=\"3166\" /></a:cubicBezTo><a:cubicBezTo><a:pt x=\"3668\" y=\"3134\" /><a:pt x=\"3658\" y=\"3104\" /><a:pt x=\"3638\" y=\"3078\" /></a:cubicBezTo><a:close /></a:path></a:pathLst></a:custGeom>"   # red cross (Kreuz)


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

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── native factory chart (stacked column) → CHARTS[0] ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.439), y=IN(2.062), cx=IN(5.568), cy=IN(4.109), rId="rId2"))
    out.append(text_box(n(), "Text Placeholder 25", IN(0.53), IN(1.87), IN(4.431), _TXT_H, [paragraph([run("Weighted avg. freight charges, normalized on TEU basis ($K, CY25)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    for _y, _t in _DATA_LABELS["bar_values"]:
        out.append(text_box(n(), "Label", _BARVAL_X, IN(_y), _BARVAL_W, _BARVAL_H, [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # FFFFFF white
    for _x, _y, _cx, _fill, _t in _DATA_LABELS["segment_values"]:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _SEG_H, [paragraph([run(_t, size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(3.108), IN(2.26), IN(0.229), _TXT_H, [paragraph([run("4.9", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(2.481), IN(6.128), IN(1.484), _TXT_H, [paragraph([run("Long Beach to Honolulu", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Rectangle 304", IN(0.439), IN(5.297), IN(1.965), IN(0.608), [paragraph([], align="ctr", line_spacing=100000)], fill=WHITE, line_color="364D6E", anchor="ctr"))   # FFFFFF white
    # ── legend keys and labels ──
    for _y, _cx, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", _SWATCH_X, IN(_y), IN(_cx), _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=DK, line_width=3175, anchor="ctr"))
    for _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", _CAT_X, IN(_y), IN(_cx), _CAT_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(0.837), IN(5.307), IN(0.997), _TXT_H, [paragraph([run("Fuel Surcharge", size=PT(10), color=BLACK, font=FONT), run("1", size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── chrome ──
    out.append(breadcrumb("Carrier Entry Point Attractiveness", "Matson Test Case"))
    out.append(title_placeholder("Freight Charges", "~70% of westbound freight charges are directly related to vessel operations; other charges pertain to shoreside activities."))
    # Native comparison table: col_widths defines the four columns and each
    # trow(h=...) is a minimum. Repeated cell insets/anchor can encode row/
    # column padding and vertical alignment; align/mar_l/indent place text.
    # palette - text: 000000 black (labels/descriptions) · FFFFFF white (Terminal/Fuel/Ocean labels) · 162029 dark navy (Wharfage desc);
    #   fills: C0C0C0 silver (Wharfage) · 808080 gray (Terminal) · 4C6C9C blue (Fuel Surcharge) · 364D6E dark blue (Basic Ocean Rate);
    #   rules: 162029 dark navy (header) · 808080 gray (inner).
    out.append(table(n(), "Table 238", IN(6.162), IN(1.755), IN(6.634), IN(4.25), col_widths=[IN(1.667), IN(1.219), IN(2.88), IN(0.868)], rows=[
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
    ]))
    # status icons (check/cross) — custom_geometry() over 2 deduped path constants
    out.append(custom_geometry(n(), "Haken, check", _GLYPH_X, IN(4.264), _GLYPH_SZ, _GLYPH_SZ, _GEOM_CHECK, fill="2E7D32"))   # 2E7D32 green
    out.append(custom_geometry(n(), "Haken, check", _GLYPH_X, IN(4.911), _GLYPH_SZ, _GLYPH_SZ, _GEOM_CHECK, fill="2E7D32"))   # 2E7D32 green
    out.append(custom_geometry(n(), "Cross, kreuz", _GLYPH_X, IN(2.367), _GLYPH_SZ, _GLYPH_SZ, _GEOM_CROSS, fill="C00000"))   # C00000 dark red
    out.append(custom_geometry(n(), "Cross, kreuz", _GLYPH_X, IN(2.995), _GLYPH_SZ, _GLYPH_SZ, _GEOM_CROSS, fill="C00000"))   # C00000 dark red
    out.append(custom_geometry(n(), "Cross, kreuz", _GLYPH_X, IN(3.637), _GLYPH_SZ, _GLYPH_SZ, _GEOM_CROSS, fill="C00000"))   # C00000 dark red
    for _x, _y, _cx, _cy, _fill, _lc, _t in _GROUP_CAPTIONS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, anchor="ctr"))
    for _x, _y, _cx, _cy, _fill, _lc, _t in _ANNOTATION_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 326", IN(0.439), IN(4.009), IN(1.965), IN(1.264), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="969696", anchor="ctr"))   # 969696 gray outline
    out.append(prelim_chip())
    out.append(text_box(n(), "Rectangle 407", IN(0.495), IN(6.681), IN(12.367), IN(0.317), [paragraph([run("Note: (1) Matson and Pasha charge a Fuel Surcharge of 16.5% as of September 2025; Basic Ocean Rates largely derived from Pasha Hawaii, whereas Terminal Charges are specific to Matson", size=PT(8), color=BLACK, font=FONT), line_break(), run("Source: ", size=PT(8), color=BLACK, font=FONT), run("Pasha Hawaii", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("Aloha Freight", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("Hawaii Department of Transportation", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    out.append(text_box(n(), "Rectangle 453", IN(6.153), IN(4.094), IN(6.643), IN(1.959), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="FB6B3C", line_width=19050, anchor="ctr"))   # FB6B3C orange outline
    out.append(text_box(n(), "Rectangle 465", IN(7.548), IN(5.909), IN(5.054), IN(0.293), [paragraph([run("Directly related to vessel operations; percentage varies based on basic ocean rate, fuel surcharge, discounts, and other factors ", size=PT(10), bold=True, color="FB6B3C", font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))   # FFFFFF white
    out.append(connector(n(), "Straight Arrow Connector 597", _LEADER_X, IN(4.052), IN(2.162), IN(0.696), color="808080", width=12700, dashed=True))   # 808080 gray
    out.append(connector(n(), "Straight Arrow Connector 637", _LEADER_X, IN(3.691), IN(2.171), IN(0.426), color="808080", width=12700, dashed=True))   # 808080 gray
    out.append(connector(n(), "Straight Arrow Connector 640", _LEADER_X, IN(2.729), IN(2.162), IN(0.704), color="808080", width=12700, dashed=True))   # 808080 gray
    out.append(connector(n(), "Straight Arrow Connector 646", _LEADER_X, IN(2.528), IN(2.171), IN(0.308), color="808080", width=12700, dashed=True))   # 808080 gray
    out.append(connector(n(), "Straight Arrow Connector 471", _LEADER_X, IN(2.2), IN(2.135), IN(0.3), color="808080", width=12700, dashed=True, flip_v=True))   # 808080 gray
    out.append(text_box(n(), "Rectangle 36", IN(0.53), IN(1.447), IN(3.2), IN(0.244), [paragraph([run("Spot Rate from CONUS", size=PT(11), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color="none", anchor="ctr"))   # CEDDEC pale blue
    return "".join(out)


def render() -> str:
    return slide(_body())
