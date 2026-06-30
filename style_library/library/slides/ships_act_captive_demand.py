"""Teaching exemplar: SHIPS Act captive-demand bridge.

ROLE
  policy_mandate_comparison / captive_demand_stack

USE WHEN
  A slide needs a compact stacked-column chart comparing two demand totals, a
  right-hand policy-mandate table, a small manual legend, and a few callout
  outlines that mark modeled production scope.

TEACHES
  - rebuilding a source styled stacked-column chart as a native chart factory
  - encoding a source chart's per-point fills when one workbook series changes
    vessel-type meaning between categories
  - using a patterned native chart series for a hatched "Other" segment
  - suppressing all native chart labels and rebuilding the chart-label system
    as slide-level overlays, mirroring the slide3 annual-TAM module
  - using semantic ValueBadge / TextLabel records for segment labels, total
    labels, category labels, and legend labels instead of chart-native dLbls
  - exposing a machine-readable RENDER_CONTRACT so agents know the chart data,
    label overlays, and source-fragile geometry that must be updated together
  - using a dense right-hand mandate table with rich cells, row spans, and local
    cell-border helpers
  - preserving paint order while splitting a converted slide into teaching-level
    paint sections

TEXT-FIT PRECEDENT
  mandate_table:
    geometry: 7.089in wide x 4.007in high
    type: Arial 10pt rich cells, 12pt Yes/No flags, centered/stacked provision labels
    content: title row + header row + five mandate rows, including a two-row
             shared cargo-ramp cell
    copy_when: a policy table needs to map provisions to quantitative ramp
               assumptions and binary eligibility requirements.

SOURCE NOTE
  Teaching rewrite of the source-faithful `ships_act_captive_demand.py` module.
  The source chart template in `slide60_chart43.xml` and its workbook
  `slide60_chart43.xlsb` were used to transcribe the chart's data, colors,
  per-point overrides, fixed value axis, gap width, overlap, and manual plot
  layout. This module does not read those files at runtime: it builds the chart
  through `column_chart()` so the data, colors, and axis choices are inspectable
  in Python.

FIDELITY NOTE
  This is a practical factory rebuild, not a byte-identical chart-template port.
  It preserves the visible chart semantics and major styling controls (stacked
  columns, hidden native category labels, fixed value axis, manual plot-area
  layout, no native legend, no segment outlines, per-point fills, and a hatched
  "Other" series), while retaining the source slide's manually placed labels,
  thin-segment callouts, legend, leader lines, mandate table, and callouts as
  slide shapes.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, column_chart, connector, graphic_frame, line_break,
    paragraph, run, table, tbreak, tcell, tcell_rich, text_box, tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
BREADCRUMB = "44505C"
GRAY_2 = "D9D9D9"
FONT = "Arial"

LAYOUT = "slideLayout4"


# ════════════════════════════════════════════════════════════════════════════
# Native chart spec: source chart XML -> declarative column_chart().
# ════════════════════════════════════════════════════════════════════════════
# Source-chart transcription summary:
#   chart part:       slide60_chart43.xml
#   source workbook:  slide60_chart43.xlsb
#   c:barDir:         col
#   c:grouping:       stacked
#   c:gapWidth:       80
#   c:overlap:        100
#   value axis:       min=0, max=220, major=20
#   plot layout:      manual inner plot rectangle below
#   categories:       source carried no native category labels; slide text boxes
#                     provide the category labels manually.
CAPTIVE_DEMAND_CATEGORIES: tuple[str, ...] = (
    "Strategic Commercial Fleet (supported by MSTF)",
    "Legally Mandated Demand",
)

VESSEL_TYPE_COLORS = {
    "container": "007770",
    "lng": "C0C0C0",
    "crude_tanker": "1D4D68",
    "product_tanker": "4C6C9C",
    "bulk": BLACK,
    "ro_ro": "969696",
    "other_pattern_fg": BLACK,
    "other_pattern_bg": WHITE,
}

# Series are ordered bottom-to-top in the stacked columns. Two middle series are
# intentionally semantic bridges: the source chart uses the same workbook series
# for different vessel types in category 0 vs. category 1, so the Python spec uses
# data_point_colors to preserve those per-point fills.
CAPTIVE_DEMAND_SERIES: tuple[dict, ...] = (
    {
        "name": "Container",
        "color": VESSEL_TYPE_COLORS["container"],
        "values": [124, 46],
        "hide_labels": True,
    },
    {
        "name": "LNG",
        "color": VESSEL_TYPE_COLORS["lng"],
        "values": [46, 41],
        "hide_labels": True,
    },
    {
        "name": "Crude Tanker",
        "color": VESSEL_TYPE_COLORS["crude_tanker"],
        "values": [18, 15],
        "hide_labels": True,
    },
    {
        "name": "Ro-Ro / Product Tanker bridge",
        "color": VESSEL_TYPE_COLORS["ro_ro"],
        "data_point_colors": [
            VESSEL_TYPE_COLORS["ro_ro"],
            VESSEL_TYPE_COLORS["product_tanker"],
        ],
        "values": [9, 1],
        "hide_labels": True,
    },
    {
        "name": "Product Tanker / Bulk bridge",
        "color": VESSEL_TYPE_COLORS["bulk"],
        "data_point_colors": [
            VESSEL_TYPE_COLORS["product_tanker"],
            VESSEL_TYPE_COLORS["bulk"],
        ],
        "values": [1, 1],
        "hide_labels": True,
    },
    {
        "name": "Bulk",
        "color": VESSEL_TYPE_COLORS["bulk"],
        "values": [1, None],
        "hide_labels": True,
    },
    {
        "name": "Other",
        "values": [2, None],
        "pattern": {
            "prst": "ltDnDiag",
            "fg": VESSEL_TYPE_COLORS["other_pattern_fg"],
            "bg": VESSEL_TYPE_COLORS["other_pattern_bg"],
        },
        "hide_labels": True,
    },
)

# Readable data mirror for downstream agents/tools that expect the converted-slide
# _CHART0_DATA shape. CHARTS below uses the same values through column_chart().
_CHART0_DATA = {
    "categories": CAPTIVE_DEMAND_CATEGORIES,
    "series": CAPTIVE_DEMAND_SERIES,
}

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(CAPTIVE_DEMAND_CATEGORIES),
    "series": [dict(series) for series in CAPTIVE_DEMAND_SERIES],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_labels": False,
    "show_gridlines": False,
    "show_value_axis_labels": True,
    "value_axis_format": '#,##0;"-"#,##0',
    "value_label_format": '#,##0;"-"#,##0',
    "value_label_size_pt": 10,
    "value_label_bold": False,
    "cat_label_size_pt": 10,
    "gap_width": 80,
    "bar_overlap": 100,
    "seg_line_color": None,
    "axis_line_color": BLACK,
    "axis_line_width": 9_525,
    "value_axis_min": 0,
    "value_axis_max": 220,
    "value_axis_major_unit": 20,
    "plot_layout": {
        "x": 0.094205354117248397,
        "y": 0.05274888558692422,
        "w": 0.88817350050830224,
        "h": 0.8945022288261516,
    },
    "cat_header": "Demand Type",
}

# The slide3 reference suppresses all native chart labels and paints value labels
# as slide-level overlays.  The chart remains a normal editable native chart; the
# values, totals, and category captions are controlled below by ValueBadge and
# TextLabel records that are painted after the chart frame.
CHART_LABEL_POLICY = {
    "native_chart_labels": {
        "mechanism": "disabled: CHART_STYLE['show_value_labels'] is False and every series has hide_labels=True",
        "fit_class": "not_used",
        "copy_rule": "Keep native labels off; add/edit labels through SEGMENT_VALUE_BADGES, TOTAL_VALUE_LABELS, and CATEGORY_LABELS.",
    },
    "manual_value_badges": {
        "mechanism": "slide-level text_box overlays painted after the native chart, matching slide3",
        "fit_class": "exact_overlay",
        "box_in": "0.115-0.267in wide x 0.167in high",
        "font_pt": 10,
        "copy_rule": "Use for one- to three-character value tokens; update geometry when chart frame, plot_layout, axis scale, or values change.",
    },
    "manual_totals_and_categories": {
        "mechanism": "slide-level TextLabel records, not native category labels or chart data labels",
        "fit_class": "exact_overlay",
        "copy_rule": "Totals and category captions are manual labels and must be reconciled with chart data changes.",
    },
}

CHARTS = [column_chart(**CHART_STYLE)]

# Source-line external links. The column chart takes rId2, so links start at rId3;
# the SourceNote runs reference these rIds via run(..., hyperlink_rid=...). rId5's
# target mirrors the source deck's relative-looking AEO-crude link verbatim.
HYPERLINKS = [
    {"rId": "rId3", "url": "https://www.congress.gov/bill/119th-congress/senate-bill/1541/text#toc-id9f432e34eabc4c5ea3d818bfdc7a838f"},  # SHIPS Act text
    {"rId": "rId4", "url": "https://www.eia.gov/outlooks/aeo/data/browser/#/?id=76-AEO2025&cases=ref2025&sourcekey=0"},                   # EIA AEO LNG Export Table
    {"rId": "rId5", "url": "../https/www.eia.gov/outlooks/aeo/data/browser#/?id=11-AEO2025&cases=ref2025&sourcekey=0"},                   # EIA AEO Crude Export Table
    {"rId": "rId6", "url": "https://www.eia.gov/todayinenergy/detail.php?id=67064"},                                                      # EIA Crude Tanker Descriptions
    {"rId": "rId7", "url": "https://www.gao.gov/assets/gao-22-105160.pdf"},                                                               # GAO Report on Government Preference Cargo
]


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: comments a future agent can inspect programmatically.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "policy_mandate_comparison",
    "use_when": (
        "Use for a policy-backed demand comparison where a left stacked chart "
        "quantifies totals and a right table documents mandate mechanics."
    ),
    "teaches": [
        "native column_chart stacked chart rebuilt from source XML",
        "per-point chart colors through data_point_colors",
        "patterned chart series for a hatched segment",
        "manual slide-overlay value badges for all stacked-segment labels",
        "slide3-style label data records instead of patched chart-native dLbls",
        "CHART_LABEL_POLICY distinguishing chart data from overlay labels",
        "RENDER_CONTRACT for chart frame, label overlays, and table row policy",
        "dense mandate table with rich cells and row spans",
        "local table-cell helpers instead of centralized table_kit",
        "PowerPoint paint order split into semantic paint functions",
    ],
}

TEXT_FIT = {
    "mandate_table": {
        "box_in": (7.089, 4.007),
        "font_pt": "10 body + 12 Yes/No flags",
        "content": "title row + header row + five mandate rows",
        "note": "Rich provision cells use tbreak() for three-line labels; keep provision names short.",
    },
    "chart_value_badges": {
        "box_in": "0.115-0.267 wide x 0.167 high",
        "font_pt": 10,
        "content": "manual segment value labels painted as slide text boxes over the native chart",
        "note": "Mirrors slide3: keep native chart labels suppressed and edit labels in SEGMENT_VALUE_BADGES.",
    },
    "chart_category_labels": {
        "box_in": [(1.667, 0.333), (1.663, 0.167)],
        "font_pt": 10,
        "content": "manual category captions beneath two bars",
        "note": "The long SCF label fits only because it can wrap inside a 0.333in-high box.",
    },
    "source_note": {
        "box_in": (12.367, 0.322),
        "font_pt": 8,
        "content": "two source/note lines via line_break()",
    },
    "caveat_box": {
        "box_in": (7.089, 0.867),
        "font_pt": 12,
        "content": "one centered bold caveat sentence",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Small semantic geometry/data records.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    """Geometry in inches; converted to EMU only at the primitive call site."""

    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)

    def inches(self) -> tuple[float, float, float, float]:
        return self.x, self.y, self.w, self.h


@dataclass(frozen=True)
class TextZone:
    name: str
    box: Box
    font_pt: float
    fit_note: str


@dataclass(frozen=True)
class ValueBadge:
    """Manual slide-level chart value label, matching the slide3 label pattern.

    The native chart carries data only.  Every visible value token is a text_box
    overlay with explicit inch geometry, fill, and text color.  Fill usually
    matches the underlying chart segment so the overlay behaves like a data
    label rather than a visible UI chip.
    """

    name: str
    box: Box
    label: str
    fill: str | None
    text_color: str = BLACK
    source_binding: tuple[str, int] | None = None  # (series name, category idx)
    reason: str = "manual chart label overlay"
    fit_class: str = "exact_overlay"
    copy_rule: str = (
        "Use only for one- to three-character value tokens; update box geometry "
        "when chart frame, plot_layout, axis scale, category count, series order, "
        "or values change."
    )


@dataclass(frozen=True)
class TextLabel:
    name: str
    box: Box
    text: str
    font_pt: float = 10
    bold: bool = False
    italic: bool = False
    align: str | None = "ctr"
    anchor: str = "ctr"
    wrap: str = "none"


@dataclass(frozen=True)
class LegendSwatch:
    box: Box
    fill: str


@dataclass(frozen=True)
class LegendLabel:
    box: Box
    label: str


@dataclass(frozen=True)
class LeaderLine:
    name: str
    box: Box
    flip_h: bool = False
    flip_v: bool = False
    arrow: bool = False
    dashed: bool = True
    color: str = "808080"
    width: int = 6_350


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Layout zones and repeated shape data.
# ════════════════════════════════════════════════════════════════════════════
CHART_FRAME = Box(0.429, 1.620, 5.123, 4.674)
CHART_TITLE = TextZone(
    name="ChartTitle",
    box=Box(0.542, 1.505, 4.384, 0.167),
    font_pt=10,
    fit_note="External chart title; one line, no wrap.",
)
MANDATE_TABLE = TextZone(
    name="MandateTable",
    box=Box(5.703, 1.483, 7.089, 4.007),
    font_pt=10,
    fit_note="Dense right-hand policy table; row heights are source minima.",
)
SOURCE_NOTE = TextZone(
    name="SourceNote",
    box=Box(0.495, 6.675, 12.367, 0.322),
    font_pt=8,
    fit_note="Off-house source line; kept at source position.",
)
CAVEAT_BOX = TextZone(
    name="OpexDnaCaveat",
    box=Box(5.703, 5.560, 7.089, 0.867),
    font_pt=12,
    fit_note="One centered bold caveat sentence.",
)
SCENARIO_CHIP = TextZone(
    name="ScenarioChip",
    box=Box(8.069, 0.173, 2.977, 0.218),
    font_pt=12,
    fit_note="Top-right scenario tag; centered and bold.",
)
PORT_ALPHA_MARKER = Box(10.635, 1.191, 0.100, 0.234)
PORT_ALPHA_LABEL = TextZone(
    name="PortAlphaProductionModeledLabel",
    box=Box(10.691, 1.191, 2.101, 0.234),
    font_pt=10,
    fit_note="One-line legend caption for orange modeled-production outlines.",
)

MARKER_SIZE = Box(0, 0, 0.115, 0.167)
SWATCH_SIZE = Box(0, 0, 0.196, 0.146)
VESSEL_LABEL_X = 4.139
VESSEL_LABEL_H = 0.167
TEXT_ROW_H = 0.167

SEGMENT_VALUE_BADGES: tuple[ValueBadge, ...] = (
    # SCF / MSTF-supported demand stack, bottom-to-top.  Wider labels stay centered;
    # 1-vessel top-cap labels sit to the right and use the source leader lines.
    ValueBadge("SCFContainerValue", Box(1.915, 4.786, 0.267, TEXT_ROW_H), "124", VESSEL_TYPE_COLORS["container"], WHITE, ("Container", 0)),
    ValueBadge("SCFLngValue", Box(1.934, 3.170, 0.229, TEXT_ROW_H), "46", VESSEL_TYPE_COLORS["lng"], BLACK, ("LNG", 0)),
    ValueBadge("SCFCrudeTankerValue", Box(1.934, 2.562, 0.229, TEXT_ROW_H), "18", VESSEL_TYPE_COLORS["crude_tanker"], WHITE, ("Crude Tanker", 0)),
    ValueBadge("SCFRoRoValue", Box(1.991, 2.306, MARKER_SIZE.w, MARKER_SIZE.h), "9", VESSEL_TYPE_COLORS["ro_ro"], WHITE, ("Ro-Ro / Product Tanker bridge", 0)),
    ValueBadge(
        "SCFProductTankerValue",
        Box(2.309, 2.210, MARKER_SIZE.w, MARKER_SIZE.h),
        "1",
        VESSEL_TYPE_COLORS["product_tanker"],
        WHITE,
        ("Product Tanker / Bulk bridge", 0),
        reason="SCF-side 1-vessel product-tanker segment is too thin for a centered native label.",
    ),
    ValueBadge(
        "SCFBulkTopCapValue",
        Box(2.704, 2.2595, MARKER_SIZE.w, MARKER_SIZE.h),
        "1",
        None,
        BLACK,
        ("Bulk", 0),
        reason="SCF-side 1-vessel top-cap label is placed outside the stack with source leader-line support.",
    ),
    ValueBadge(
        "SCFOtherTopCapValue",
        Box(2.704, 2.0935, MARKER_SIZE.w, MARKER_SIZE.h),
        "2",
        None,
        BLACK,
        ("Other", 0),
        reason="SCF-side hatched Other segment label is placed outside the stack with source leader-line support.",
    ),
    # Legally mandated demand stack, bottom-to-top.
    ValueBadge("MandatedContainerValue", Box(4.210, 5.527, 0.229, TEXT_ROW_H), "46", VESSEL_TYPE_COLORS["container"], WHITE, ("Container", 1)),
    ValueBadge("MandatedLngValue", Box(4.210, 4.700, 0.229, TEXT_ROW_H), "41", VESSEL_TYPE_COLORS["lng"], BLACK, ("LNG", 1)),
    ValueBadge("MandatedCrudeTankerValue", Box(4.210, 4.168, 0.229, TEXT_ROW_H), "15", VESSEL_TYPE_COLORS["crude_tanker"], WHITE, ("Crude Tanker", 1)),
    ValueBadge(
        "MandatedProductTankerValue",
        Box(3.951, 4.016, MARKER_SIZE.w, MARKER_SIZE.h),
        "1",
        VESSEL_TYPE_COLORS["product_tanker"],
        WHITE,
        ("Ro-Ro / Product Tanker bridge", 1),
        reason="Legal-demand-side 1-vessel product-tanker segment is too thin for a centered native label.",
    ),
    ValueBadge(
        "MandatedBulkValue",
        Box(4.583, 3.997, MARKER_SIZE.w, MARKER_SIZE.h),
        "1",
        VESSEL_TYPE_COLORS["bulk"],
        WHITE,
        ("Product Tanker / Bulk bridge", 1),
        reason="Legal-demand-side 1-vessel bulk segment is too thin for a centered native label.",
    ),
)

TOTAL_VALUE_LABELS: tuple[ValueBadge, ...] = (
    ValueBadge("SCFTotalLabel", Box(1.915, 2.033, 0.267, TEXT_ROW_H), "201", None, BLACK),
    ValueBadge("MandatedDemandTotalLabel", Box(4.191, 3.830, 0.267, TEXT_ROW_H), "104", None, BLACK),
)

CATEGORY_LABELS: tuple[TextLabel, ...] = (
    TextLabel(
        "SCFCategoryLabel",
        Box(1.215, 6.094, 1.667, 0.333),
        "Strategic Commercial Fleet (supported by MSTF)",
        wrap="square",
    ),
    TextLabel("MandatedDemandCategoryLabel", Box(3.493, 6.094, 1.663, TEXT_ROW_H), "Legally Mandated Demand"),
)

LEGEND_SWATCHES: tuple[LegendSwatch, ...] = (
    LegendSwatch(Box(3.887, 2.149, SWATCH_SIZE.w, SWATCH_SIZE.h), VESSEL_TYPE_COLORS["ro_ro"]),
    LegendSwatch(Box(3.887, 2.372, SWATCH_SIZE.w, SWATCH_SIZE.h), VESSEL_TYPE_COLORS["bulk"]),
    LegendSwatch(Box(3.887, 2.594, SWATCH_SIZE.w, SWATCH_SIZE.h), VESSEL_TYPE_COLORS["product_tanker"]),
    LegendSwatch(Box(3.887, 2.816, SWATCH_SIZE.w, SWATCH_SIZE.h), VESSEL_TYPE_COLORS["crude_tanker"]),
    LegendSwatch(Box(3.887, 3.038, SWATCH_SIZE.w, SWATCH_SIZE.h), VESSEL_TYPE_COLORS["lng"]),
    LegendSwatch(Box(3.887, 3.260, SWATCH_SIZE.w, SWATCH_SIZE.h), VESSEL_TYPE_COLORS["container"]),
)

LEGEND_LABELS: tuple[LegendLabel, ...] = (
    LegendLabel(Box(VESSEL_LABEL_X, 1.922, 0.345, VESSEL_LABEL_H), "Other"),
    LegendLabel(Box(VESSEL_LABEL_X, 2.144, 0.401, VESSEL_LABEL_H), "Ro-Ro"),
    LegendLabel(Box(VESSEL_LABEL_X, 2.366, 0.269, VESSEL_LABEL_H), "Bulk"),
    LegendLabel(Box(VESSEL_LABEL_X, 2.589, 0.944, VESSEL_LABEL_H), "Product Tanker"),
    LegendLabel(Box(VESSEL_LABEL_X, 2.811, 0.845, VESSEL_LABEL_H), "Crude Tanker"),
    LegendLabel(Box(VESSEL_LABEL_X, 3.033, 0.285, VESSEL_LABEL_H), "LNG"),
    LegendLabel(Box(VESSEL_LABEL_X, 3.255, 0.599, VESSEL_LABEL_H), "Container"),
)

LEADER_LINES: tuple[LeaderLine, ...] = (
    LeaderLine("SegmentLabelLeader", Box(2.599, 2.274, 0.101, 0.069), color=BREADCRUMB, dashed=False, flip_h=True, flip_v=True),
    LeaderLine("SegmentLabelLeader", Box(2.599, 2.177, 0.101, 0.069), color=BREADCRUMB, dashed=False, flip_h=True),
    LeaderLine("SegmentLabelLeader", Box(4.958, 2.188, 0.745, 1.927), flip_v=True),
    LeaderLine("SegmentLabelLeader", Box(4.958, 2.854, 0.745, 1.536), flip_v=True),
    LeaderLine("SegmentLabelLeader", Box(4.958, 3.487, 0.745, 1.683), flip_v=True),
)

SOURCE_NOTE_TEXT = (
    "Note: Captive demand considers current cargo volumes, growth rates, and annual "
    "vessel capacity (driven by number of trips / year, cargo capacity, and utilization)"
)
SOURCE_LIST = (
    "Source: S&P Panjiva; Clarksons; SHIPS Act text; EIA AEO LNG Export Table; "
    "EIA AEO Crude Export Table; EIA Crude Tanker Descriptions; GAO Report on "
    "Government Preference Cargo"
)


def _badge_contract(badge: ValueBadge) -> dict:
    return {
        "name": badge.name,
        "label": badge.label,
        "box_in": badge.box.inches(),
        "fill": badge.fill,
        "text_color": badge.text_color,
        "source_binding": badge.source_binding,
        "fit_class": badge.fit_class,
        "reason": badge.reason,
        "copy_rule": badge.copy_rule,
    }


def _text_label_contract(label: TextLabel) -> dict:
    return {
        "name": label.name,
        "text": label.text,
        "box_in": label.box.inches(),
        "font_pt": label.font_pt,
        "bold": label.bold,
        "italic": label.italic,
        "align": label.align,
        "anchor": label.anchor,
        "wrap": label.wrap,
    }


RENDER_CONTRACT = {
    "slide": {
        "layout": LAYOUT,
        "canvas_in": (13.333, 7.500),
        "composition": (
            "left native stacked-column chart with slide-level manual value labels; "
            "right mandate table; source-positioned scenario annotations"
        ),
    },
    "native_chart": {
        "frame_in": CHART_FRAME.inches(),
        "factory": "column_chart(mode='stacked')",
        "categories": CAPTIVE_DEMAND_CATEGORIES,
        "value_axis": {"min": 0, "max": 220, "major_unit": 20},
        "gap_width": CHART_STYLE["gap_width"],
        "bar_overlap": CHART_STYLE["bar_overlap"],
        "plot_layout_inner": dict(CHART_STYLE["plot_layout"]),
        "native_category_labels": "hidden; slide text boxes provide category labels",
        "native_legend": "hidden; slide legend is manual",
        "segment_outlines": "none",
    },
    "label_system": {
        "native_chart_labels": CHART_LABEL_POLICY["native_chart_labels"],
        "manual_value_badges": {
            **CHART_LABEL_POLICY["manual_value_badges"],
            "records": tuple(_badge_contract(badge) for badge in SEGMENT_VALUE_BADGES),
        },
        "manual_totals": {
            **CHART_LABEL_POLICY["manual_totals_and_categories"],
            "records": tuple(_badge_contract(badge) for badge in TOTAL_VALUE_LABELS),
        },
        "manual_category_labels": {
            **CHART_LABEL_POLICY["manual_totals_and_categories"],
            "records": tuple(_text_label_contract(label) for label in CATEGORY_LABELS),
        },
    },
    "table": {
        "mandate_table": {
            "box_in": MANDATE_TABLE.box.inches(),
            "col_widths_in": (2.808, 1.799, 1.241, 1.241),
            "font_pt": "10 body; 12 Yes/No flags",
            "row_height_policy": (
                "source minima through trow(h=...); wrapped table text can still grow rows"
            ),
            "content_budget": (
                "title row + header row + five mandate rows; provision labels use "
                "three short lines at most"
            ),
            "fit_class": "tight_reference_table",
        },
    },
    "agent_copy_rules": (
        "Do not put prose in chart value badges; they are one- to three-character label overlays.",
        "When changing chart data or axis scale, update native chart data, SEGMENT_VALUE_BADGES, TOTAL_VALUE_LABELS, and CATEGORY_LABELS together.",
        "Keep CHART_STYLE['show_value_labels']=False; do not reintroduce chart-native dLbls unless the label system is deliberately redesigned.",
        "Use the slide3 pattern: chart first, then manual value badges, totals, category labels, and legend as slide shapes.",
    ),
}


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: local by design for teaching-module readability.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Only draw the sides passed as L/R/T/B; omitted sides render as no-fill."""

    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(
    text: str = "",
    *,
    fill=None,
    bold: bool | None = None,
    italic: bool | None = None,
    color: str = BLACK,
    size: int = PT(10),
    align: str = "l",
    anchor: str = "ctr",
    span: int = 1,
    rowspan: int = 1,
    **edges,
):
    """Plain tcell wrapper: content first, cell mechanics second."""

    return tcell(
        text,
        fill=fill,
        bold=bold,
        italic=italic,
        color=color,
        size=size,
        align=align,
        anchor=anchor,
        grid_span=span,
        row_span=rowspan,
        font=FONT,
        borders=bd(**edges),
    )


def rcell(
    paras,
    *,
    fill=None,
    anchor: str = "ctr",
    span: int = 1,
    rowspan: int = 1,
    **edges,
):
    """Rich tcell wrapper: tpara()/trun() content, then borders/spans."""

    return tcell_rich(
        paras,
        fill=fill,
        grid_span=span,
        row_span=rowspan,
        anchor=anchor,
        borders=bd(**edges),
    )


# ════════════════════════════════════════════════════════════════════════════
# Text helpers: keep paint functions at slide-intent level.
# ════════════════════════════════════════════════════════════════════════════
def _r(
    text: str,
    *,
    size_pt: float = 10,
    bold: bool = False,
    italic: bool = False,
    color: str = BLACK,
) -> str:
    return run(
        text,
        size=PT(size_pt),
        bold=bold or None,
        italic=italic or None,
        color=color,
        font=FONT,
    )


def _tight_para(runs, *, align: str | None = None):
    """100% line-spacing paragraph used by manual chart labels."""

    return paragraph(
        runs,
        align=align,
        mar_l=0,
        indent=0,
        line_spacing=100_000,
    )


def _empty_para(align: str = "ctr"):
    return paragraph([], align=align, line_spacing=100_000)


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def paint_opening_chrome(out: list[str], ids: ShapeIds) -> None:
    # Source paint order puts the title before the off-house note and breadcrumb.
    out.append(
        ""
    )
    out.append(
        text_box(
            ids.next(),
            SOURCE_NOTE.name,
            *SOURCE_NOTE.box.emu(),
            [
                paragraph(
                    [
                        run(SOURCE_NOTE_TEXT, size=PT(8), color=BLACK, font=FONT),
                        line_break(),
                        run("Source: S&P Panjiva; Clarksons; ", size=PT(8), color=BLACK, font=FONT),
                        run("SHIPS Act text", size=PT(8), color=BLACK, font=FONT, hyperlink_rid="rId3"),
                        run("; ", size=PT(8), color=BLACK, font=FONT),
                        run("EIA AEO LNG Export Table", size=PT(8), color=BLACK, font=FONT, hyperlink_rid="rId4"),
                        run("; ", size=PT(8), color=BLACK, font=FONT),
                        run("EIA AEO Crude Export Table", size=PT(8), color=BLACK, font=FONT, hyperlink_rid="rId5"),
                        run("; ", size=PT(8), color=BLACK, font=FONT),
                        run("EIA Crude Tanker Descriptions", size=PT(8), color=BLACK, font=FONT, hyperlink_rid="rId6"),
                        run("; ", size=PT(8), color=BLACK, font=FONT),
                        run("GAO Report on Government Preference Cargo", size=PT(8), color=BLACK, font=FONT, hyperlink_rid="rId7"),
                    ],
                    line_spacing=100_000,
                )
            ],
            fill=None,
            line_color="none",
        )
    )
    out.append("")


def paint_mandate_table(out: list[str], ids: ShapeIds) -> None:
    # Table layout: col_widths fixes the mandate columns and trow(h=...) their
    # minimum heights; each cell controls insets/anchor while tpara align,
    # mar_l, and indent control horizontal alignment and paragraph margins.
    # palette - text: 000000 black (headers/rates) · FFFFFF white (provision labels) · 007770 teal (Yes) · C00000 dark red (No);
    #   fills: D9D9D9 light gray (title banner) · FFFFFF white (body) · 1D4D68 teal-blue / C0C0C0 silver / 007770 teal (provisions);
    #   rules: 000000 black (header) · 808080 gray (inner).
    out.append(table(ids.next(), MANDATE_TABLE.name, *MANDATE_TABLE.box.emu(), col_widths=[IN(2.808), IN(1.799), IN(1.241), IN(1.241)], rows=[
        # ── title banner (spans all 4 columns) ──
        trow([cell("Legally mandated demand from SHIPS Act Provisions", size=PT(10), bold=True, color=BLACK, align="ctr", fill=GRAY_2, span=4, anchor="b")], h=IN(0)),
        # ── column headers (black bottom rule) ──
        trow([
            rcell([tpara([trun("Provision ", size=PT(10), bold=True, color=BLACK, font=FONT), trun("(Bill Section)", size=PT(10), italic=True, color=BLACK, font=FONT), tbreak(), trun("Vessel Type Impacted", size=PT(10), color=BLACK, font=FONT)])], anchor="b", B=edge(BLACK)),
            rcell([tpara([trun("% of Cargo", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("(Start – ramp end)", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], anchor="b", B=edge(BLACK)),
            cell("US-Built", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", B=edge(BLACK)),
            cell("US-Flagged", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", B=edge(BLACK)),
        ], h=IN(0)),
        # ── Crude Exports (SEC. 420) ──
        trow([
            rcell([tpara([trun("Crude Exports from the US", size=PT(10), bold=True, color=WHITE, font=FONT)]), tpara([trun("SEC. 420", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Crude Tankers", size=PT(10), color=WHITE, font=FONT)])], fill="1D4D68", T=edge(BLACK), B=edge("808080", 6350)),
            rcell([tpara([trun("3% to 10%", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("2027-2040", size=PT(10), italic=True, color=BLACK, font=FONT), trun(" ", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, T=edge(BLACK), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge(BLACK), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge(BLACK), B=edge("808080", 6350)),
        ], h=IN(0.661)),
        # ── LNG Exports (SEC. 420) ──
        trow([
            rcell([tpara([trun("LNG Exports from the US", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("SEC. 420", size=PT(10), italic=True, color=BLACK, font=FONT), tbreak(), trun("LNG Ships", size=PT(10), color=BLACK, font=FONT)])], fill="C0C0C0", T=edge("808080", 6350), B=edge("808080", 6350)),
            rcell([tpara([trun("2% to 15%", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("2027-2047", size=PT(10), italic=True, color=BLACK, font=FONT), trun(" ", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
        ], h=IN(0.661)),
        # ── China Imports (SEC. 415) ──
        trow([
            rcell([tpara([trun("China Imports to the US", size=PT(10), bold=True, color=WHITE, font=FONT), tbreak(), trun("SEC. 415", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Containerships", size=PT(10), color=WHITE, font=FONT)])], fill="007770", T=edge("808080", 6350), B=edge("808080", 6350)),
            rcell([tpara([trun("1% to 10%", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("2031-2040", size=PT(10), italic=True, color=BLACK, font=FONT), trun(" ", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
        ], h=IN(0.661)),
        # ── US Government Cargo Preference (SEC. 411); %-of-cargo cell spans 2 rows ──
        trow([
            rcell([tpara([trun("US Government Cargo Preference", size=PT(10), bold=True, color=WHITE, font=FONT), tbreak(), trun("SEC. 411", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Containerships & Bulk", size=PT(10), color=WHITE, font=FONT)])], fill="007770", T=edge("808080", 6350), B=edge("808080", 6350)),
            rcell([tpara([trun("50% to 100%", size=PT(10), bold=True, color=BLACK, font=FONT), trun(" ", size=PT(10), color=BLACK, font=FONT), tbreak(), trun("180 days after bill passage", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, rowspan=2, T=edge("808080", 6350)),
            cell("No", size=PT(12), bold=True, color="C00000", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350), B=edge("808080", 6350)),
        ], h=IN(0.661)),
        # ── USDA Program Exports (SEC. 418); col 1 is covered by the row-span above ──
        trow([
            rcell([tpara([trun("USDA Program Exports", size=PT(10), bold=True, color=WHITE, font=FONT), tbreak(), trun("SEC. 418", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Containerships", size=PT(10), color=WHITE, font=FONT)])], fill="007770", T=edge("808080", 6350)),
            cell("No", size=PT(12), bold=True, color="C00000", align="ctr", fill=WHITE, T=edge("808080", 6350)),
            cell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, T=edge("808080", 6350)),
        ], h=IN(0.661)),
    ]))


def paint_chart(out: list[str], ids: ShapeIds) -> None:
    out.append(
        graphic_frame(
            sp_id=ids.next(),
            name="CaptiveDemandChart",
            x=IN(CHART_FRAME.x),
            y=IN(CHART_FRAME.y),
            cx=IN(CHART_FRAME.w),
            cy=IN(CHART_FRAME.h),
            rId="rId2",
        )
    )


def _paint_leader(out: list[str], ids: ShapeIds, line: LeaderLine) -> None:
    out.append(
        connector(
            ids.next(),
            line.name,
            *line.box.emu(),
            color=line.color,
            width=line.width,
            dashed=line.dashed,
            arrow=line.arrow,
            flip_h=line.flip_h,
            flip_v=line.flip_v,
        )
    )


def paint_chart_labels_and_legend(out: list[str], ids: ShapeIds) -> None:
    for line in LEADER_LINES[:2]:
        _paint_leader(out, ids, line)

    out.append(
        text_box(
            ids.next(),
            CHART_TITLE.name,
            *CHART_TITLE.box.emu(),
            [_tight_para([_r("SCF Supported by MSTF vs. Legally Mandated Demand (# vessels)", bold=True)])],
            fill=None,
            line_color="none",
            anchor="b",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        )
    )

    # Slide3-style chart labels: every visible data label is a manual slide
    # overlay painted above the chart frame.  The native chart has no data labels.
    for badge in SEGMENT_VALUE_BADGES:
        out.append(
            text_box(
                ids.next(),
                badge.name,
                *badge.box.emu(),
                [_tight_para([_r(badge.label, color=badge.text_color)], align="ctr")],
                fill=badge.fill,
                line_color="none",
                anchor="ctr",
                wrap="none",
                l_ins=17_463,
                t_ins=0,
                r_ins=17_463,
                b_ins=0,
            )
        )

    for badge in TOTAL_VALUE_LABELS:
        out.append(
            text_box(
                ids.next(),
                badge.name,
                *badge.box.emu(),
                [_tight_para([_r(badge.label, color=badge.text_color)], align="ctr")],
                fill=badge.fill,
                line_color="none",
                anchor="b",
                wrap="none",
                l_ins=17_463,
                t_ins=0,
                r_ins=17_463,
                b_ins=0,
            )
        )

    for label in CATEGORY_LABELS:
        out.append(
            text_box(
                ids.next(),
                label.name,
                *label.box.emu(),
                [_tight_para([_r(label.text, size_pt=label.font_pt, bold=label.bold, italic=label.italic)], align=label.align)],
                fill=None,
                line_color="none",
                anchor=label.anchor,
                wrap=label.wrap,
                l_ins=0,
                t_ins=0,
                r_ins=0,
                b_ins=0,
            )
        )

    # Pattern-fill legend swatch — text_box(pattern_fill=) mirrors the native
    # chart's hatched `Other` series without a per-module OOXML helper.
    out.append(
        text_box(
            ids.next(),
            "OtherPatternSwatch",
            IN(3.887),
            IN(1.927),
            IN(SWATCH_SIZE.w),
            IN(SWATCH_SIZE.h),
            [_empty_para()],
            fill=None,
            line_color="none",
            pattern_fill={"prst": "ltDnDiag", "fg": "scheme:tx1", "bg": "scheme:bg1"},
            anchor="ctr",
        )
    )

    for swatch in LEGEND_SWATCHES:
        out.append(
            text_box(
                ids.next(),
                "LegendSwatch",
                *swatch.box.emu(),
                [_empty_para()],
                fill=swatch.fill,
                line_color="none",
                anchor="ctr",
            )
        )
    for label in LEGEND_LABELS:
        out.append(
            text_box(
                ids.next(),
                "LegendLabel",
                *label.box.emu(),
                [_tight_para([_r(label.label)])],
                fill=None,
                line_color="none",
                anchor="ctr",
                wrap="none",
                l_ins=0,
                t_ins=0,
                r_ins=0,
                b_ins=0,
            )
        )


# Reference drop-shadow on the light-blue callout (outerShdw, verbatim params from
# the source deck): 0.056" blur, 0.03" offset down-right, black @ 40% alpha.
CALLOUT_SHADOW = (
    '<a:effectLst><a:outerShdw blurRad="50800" dist="38100" dir="2700000" '
    'algn="tl" rotWithShape="0"><a:prstClr val="black"><a:alpha val="40000"/>'
    '</a:prstClr></a:outerShdw></a:effectLst>'
)


def paint_scenario_annotations(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            CAVEAT_BOX.name,
            *CAVEAT_BOX.box.emu(),
            [
                paragraph(
                    [
                        run(
                            "Reaching ~200 vessels assumes owners accept Opex and D&A differential of operating US-built and flagged vessels vs. foreign-built and flagged",
                            size=PT(12),
                            bold=True,
                            color=BLACK,
                            font=FONT,
                        )
                    ],
                    align="ctr",
                    line_spacing=100_000,
                )
            ],
            fill="CEDDEC",
            line_color=BLACK,
            anchor="ctr",
            effects=CALLOUT_SHADOW,
        )
    )
    out.append("")
    out.append(
        text_box(
            ids.next(),
            SCENARIO_CHIP.name,
            *SCENARIO_CHIP.box.emu(),
            [paragraph([run("(2) SHIPS Act Scenario", size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100_000)],
            fill="447BB2",              # = theme bg2 @ 50% lum (reference chip fill)
            line_color=BLACK,
            line_width=19050,           # 1.5pt — reference chip border (theme lnRef idx=2)
            anchor="ctr",
        )
    )

    for line in LEADER_LINES[2:]:
        _paint_leader(out, ids, line)

    out.append(
        text_box(
            ids.next(),
            "PortAlphaMarker",
            *PORT_ALPHA_MARKER.emu(),
            [_empty_para()],
            fill=None,
            line_color="FB6B3C",
            line_width=19_050,
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            ids.next(),
            PORT_ALPHA_LABEL.name,
            *PORT_ALPHA_LABEL.box.emu(),
            [paragraph([run("Port Alpha production modeled", size=PT(10), color=BLACK, font=FONT)], line_spacing=100_000)],
            fill=None,
            line_color="none",
            anchor="ctr",
            wrap="none",
        )
    )
    out.append(
        text_box(
            ids.next(),
            "PortAlphaChartOutline1",
            IN(3.835),
            IN(2.569),
            IN(1.300),
            IN(0.426),
            [_empty_para()],
            fill=None,
            line_color="FB6B3C",
            line_width=19_050,
            anchor="b",
        )
    )
    out.append(
        text_box(
            ids.next(),
            "PortAlphaChartOutline2",
            IN(3.835),
            IN(3.236),
            IN(1.300),
            IN(0.207),
            [_empty_para()],
            fill=None,
            line_color="FB6B3C",
            line_width=19_050,
            anchor="b",
        )
    )


def _body() -> str:
    out: list[str] = []
    ids = ShapeIds()
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    paint_opening_chrome(out, ids)
    paint_mandate_table(out, ids)
    paint_chart(out, ids)
    paint_chart_labels_and_legend(out, ids)
    paint_scenario_annotations(out, ids)
    return "".join(out)


CHROME = Chrome(
    section="US-Built Ship Demand",
    topic="With SHIPS Act",
    title="SHIPS Act Captive Demand",
    takeaway="MSTF can support ~100 more vessels than legally mandated demand for SHIPS Act.",
)


def render() -> str:
    return body_slide(CHROME, _body())
