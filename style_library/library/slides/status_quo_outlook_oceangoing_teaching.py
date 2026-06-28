"""Teaching exemplar: Status Quo Outlook — oceangoing commercial hull retirements.

ROLE
  scenario_forecast / net_hull_retirement_replacements

USE WHEN
  A slide needs to show that replacement-only demand is too sparse for serial
  production: a left-side net-hull additions/removals chart, a paired retirement
  vs. orderbook legend, and a right-side retirement-replacement table.

TEACHES
  - fully declarative native stacked-column charting with column_chart(mode="stacked")
  - source workbook rows embedded as Python constants instead of a sidecar XLSB
  - source chart-part style values embedded in CHART_STYLE
  - point-level colors to encode vessel archetype and positive orderbook values
  - manual year ticks and source-positioned bar-total labels over a native chart
  - semantic native table rows tied back to the chart color/value arithmetic
  - compact serial-production key, status-quo scenario chip, and off-house footnote

TEXT-FIT PRECEDENT
  chart_title:
    geometry: 6.707in wide x 0.167in high
    type: Arial 10pt bold, no-wrap
    content: one dense technical caption with unit/scope qualifier
    copy_when: the chart needs a precise title separate from the executive slide title
  year_ticks:
    geometry: 0.167in wide x 0.306in high
    type: Arial 8pt, right-aligned, no-wrap, zero insets
    content: four-digit fiscal/calendar years across a 25-year horizon
  bar_total_labels:
    geometry: 0.115-0.161in wide x 0.167in high
    type: Arial 10pt, centered, tight side insets
    content: one signed net-hull integer only
  retirement_replacement_table:
    geometry: 5.049in wide x 3.867in high
    type: Arial 10pt table body, 16pt bold red values
    content: four archetype rows + one commentary row
    copy_when: a charted retirement stream needs an explicit per-year replacement readout

SOURCE NOTE
  Teaching rewrite of the source-faithful `status_quo_outlook_oceangoing.py`
  module. The original used `styled_chart(...)` backed by slide44_chart26.xml/.xlsb.
  This version intentionally replaces the runtime XML/XLSB template dependency with
  a native editable `column_chart(mode="stacked", ...)` spec. The four exact Sheet1
  workbook rows from slide44_chart26.xlsb and the key chart XML styling values
  (manual plot layout, gap width, overlap, axis bounds, series/point fills, and
  selective data-label intent) are explicit constants in this module.

FIDELITY NOTE
  This is a practical factory-native rebuild, not a byte-identical chart-template
  port. It preserves the visible chart semantics, values, point colors, manual
  year ticks, bar-total labels, paired legend, replacement table, callouts,
  source note, serial-production key, Preliminary chip, and scenario chip. Tiny
  differences can remain in PowerPoint's internal chart XML ordering and native
  label placement versus the original chart part.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, column_chart, graphic_frame, line_break, paragraph, run,
    table, tcell, tcell_rich, text_box, tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
GRAY_1 = "F2F2F2"
FONT = "Arial"

LAYOUT = "slideLayout4"

# Local semantic palette. The same archetype appears twice in the slide's visual
# system: blue shades for retirements and grey/black shades for orderbook hulls.
CONTAINER_RETIREMENT = "9DB1CF"
GENERAL_RETIREMENT = "6F8DB9"
RORO_RETIREMENT = "4C6C9C"
TANKER_RETIREMENT = "364D6E"
CONTAINER_ORDERBOOK = "C0C0C0"
GENERAL_ORDERBOOK = "969696"
RORO_ORDERBOOK = "808080"
TANKER_ORDERBOOK = BLACK
SCENARIO_BLUE = "CEDDEC"
TABLE_VALUE_RED = "C30C3E"
OUTLINE_NEAR_BLACK = "121415"
# Reference drop-shadow on the light-blue takeaway banner (outerShdw, verbatim from
# the source deck): 0.056" blur, 0.03" offset down-right, black @ 40% alpha.
CALLOUT_SHADOW = (
    '<a:effectLst><a:outerShdw blurRad="50800" dist="38100" dir="2700000" '
    'algn="tl" rotWithShape="0"><a:prstClr val="black"><a:alpha val="40000"/>'
    '</a:prstClr></a:outerShdw></a:effectLst>'
)

YEARS: tuple[str, ...] = tuple(str(year) for year in range(2026, 2051))

SOURCE_WORKBOOK_ROWS: tuple[tuple[int | None, ...], ...] = (
    (1, 2, 2, 5, 5, -1, -1, -3, -2, None, -1, -1, -1, -2, -2, -2, -3, -2, -6, -5, -1, -2, -1, -1, -4),
    (-1, -3, None, -1, -1, None, -1, None, None, None, None, None, -1, None, -1, None, None, -2, -1, -1, -1, None, None, None, None),
    (-5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, -1, None, -1, None, None, None, None, None),
    (-4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None),
)

SOURCE_PLOT_LAYOUT = {
    "x": 0.06157112526539278,
    "y": 0.059191329720716966,
    "w": 0.9261618306204293,
    "h": 0.8816173405585661,
}
SOURCE_GAP_WIDTH = 130
SOURCE_BAR_OVERLAP = 100
SOURCE_VALUE_AXIS_MIN = -10
SOURCE_VALUE_AXIS_MAX = 10
SOURCE_VALUE_AXIS_MAJOR_UNIT = 5
SOURCE_AXIS_LINE_WIDTH = 9525
SOURCE_VALUE_AXIS_FORMAT = '#,##0;"-"#,##0'


@dataclass(frozen=True)
class ChartLayer:
    """One source workbook row plus its XML default and point-level fills."""

    name: str
    values: tuple[int | None, ...]
    default_fill: str
    point_fill_overrides: dict[int, str]

    def point_fills(self) -> tuple[str, ...]:
        fills = [self.default_fill] * len(self.values)
        for idx, fill in self.point_fill_overrides.items():
            fills[idx] = fill
        return tuple(fills)

    def chart_dict(self) -> dict:
        return {
            "name": self.name,
            "color": self.default_fill,
            "values": list(self.values),
            "data_point_colors": list(self.point_fills()),
            "hide_labels": True,
        }


@dataclass(frozen=True)
class ReplacementRow:
    archetype: str
    retirement_fill: str
    total_per_year: str
    net_of_orderbook_per_year: str


@dataclass(frozen=True)
class XmlLabelIntent:
    """A chart-part data label that was native inside slide44_chart26.xml."""

    idx: int
    text: str
    y_offset: float


CHART_LAYERS: tuple[ChartLayer, ...] = (
    ChartLayer(
        "Source chart layer 1",
        SOURCE_WORKBOOK_ROWS[0],
        TANKER_RETIREMENT,
        {
            0: CONTAINER_ORDERBOOK,
            1: CONTAINER_ORDERBOOK,
            2: TANKER_ORDERBOOK,
            3: TANKER_ORDERBOOK,
            4: TANKER_ORDERBOOK,
            5: CONTAINER_RETIREMENT,
        },
    ),
    ChartLayer(
        "Source chart layer 2",
        SOURCE_WORKBOOK_ROWS[1],
        CONTAINER_RETIREMENT,
        {
            0: TANKER_RETIREMENT,
            3: TANKER_RETIREMENT,
            12: GENERAL_RETIREMENT,
            14: RORO_RETIREMENT,
            17: RORO_RETIREMENT,
            19: RORO_RETIREMENT,
        },
    ),
    ChartLayer(
        "Source chart layer 3",
        SOURCE_WORKBOOK_ROWS[2],
        CONTAINER_RETIREMENT,
        {0: GENERAL_RETIREMENT},
    ),
    ChartLayer(
        "Source chart layer 4",
        SOURCE_WORKBOOK_ROWS[3],
        CONTAINER_RETIREMENT,
        {},
    ),
)

# Selective native data labels from the original chart part. The factory rebuild
# keeps native labels off and exposes these as manual label intent so the slide
# stays editable and the XML values remain auditable in Python.
SOURCE_XML_DATA_LABELS: tuple[XmlLabelIntent, ...] = (
    XmlLabelIntent(2, "2", -0.07086285952480201),
    XmlLabelIntent(5, "-1", -0.04877032096706961),
    XmlLabelIntent(7, "-3", -0.09295539808253439),
    XmlLabelIntent(8, "-2", -0.07086285952480201),
    XmlLabelIntent(10, "-1", -0.04877032096706961),
    XmlLabelIntent(11, "-1", -0.04877032096706961),
    XmlLabelIntent(13, "-2", -0.07086285952480201),
    XmlLabelIntent(15, "-2", -0.07086285952480201),
    XmlLabelIntent(16, "-3", -0.09295539808253439),
    XmlLabelIntent(21, "-2", -0.07086285952480201),
    XmlLabelIntent(22, "-1", -0.04877032096706961),
    XmlLabelIntent(23, "-1", -0.04877032096706961),
    XmlLabelIntent(24, "-4", -0.11504793664026677),
)

# Kept as a readable data mirror for agents/tools that expect the converted-slide
# data-dict shape. CHARTS consumes the same values through column_chart().
_CHART0_DATA = {
    "categories": YEARS,
    "series": [
        {"name": layer.name, "values": list(layer.values)}
        for layer in CHART_LAYERS
    ],
}

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(YEARS),
    "series": [layer.chart_dict() for layer in CHART_LAYERS],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": True,
    "show_gridlines": False,
    "show_value_labels": False,
    "value_axis_format": SOURCE_VALUE_AXIS_FORMAT,
    "value_label_format": SOURCE_VALUE_AXIS_FORMAT,
    "cat_label_size_pt": 8,
    "value_label_size_pt": 10,
    "gap_width": SOURCE_GAP_WIDTH,
    "bar_overlap": SOURCE_BAR_OVERLAP,
    "seg_line_color": None,
    "axis_line_color": BLACK,
    "axis_line_width": SOURCE_AXIS_LINE_WIDTH,
    "value_axis_min": SOURCE_VALUE_AXIS_MIN,
    "value_axis_max": SOURCE_VALUE_AXIS_MAX,
    "value_axis_major_unit": SOURCE_VALUE_AXIS_MAJOR_UNIT,
    "plot_layout": dict(SOURCE_PLOT_LAYOUT),
    "cat_header": "Year",
}

CHARTS = [column_chart(**CHART_STYLE)]

RETIREMENT_FILL_TO_ARCHETYPE = {
    CONTAINER_RETIREMENT: "Container",
    GENERAL_RETIREMENT: "General",
    RORO_RETIREMENT: "RORO",
    TANKER_RETIREMENT: "Tanker",
}
ORDERBOOK_FILL_TO_ARCHETYPE = {
    CONTAINER_ORDERBOOK: "Container",
    GENERAL_ORDERBOOK: "General",
    RORO_ORDERBOOK: "RORO",
    TANKER_ORDERBOOK: "Tanker",
}

RETIREMENT_REPLACEMENT_ROWS: tuple[ReplacementRow, ...] = (
    ReplacementRow("Container", CONTAINER_RETIREMENT, "~0.6", "~0.4"),
    ReplacementRow("General", GENERAL_RETIREMENT, "~0.2", "~0.2"),
    ReplacementRow("RORO", RORO_RETIREMENT, "~0.2", "~0.2"),
    ReplacementRow("Tanker", TANKER_RETIREMENT, "~1.7", "~1.2"),
)

TEACHING_METADATA = {
    "role": "scenario_forecast / net_hull_retirement_replacements",
    "use_when": (
        "Use for a 25-year status-quo forecast where orderbook deliveries and "
        "retirements are sparse, and the key readout is whether replacement demand "
        "can support serial production."
    ),
    "teaches": [
        "native stacked column chart with positive and negative hull counts",
        "source XLSB rows embedded as constants",
        "source XML styling embedded in CHART_STYLE",
        "point-level colors for archetype/orderbook semantics",
        "manual year ticks and net bar-total labels",
        "replacement-rate table generated from semantic rows",
        "serial-production key and scenario chip",
    ],
    "source_module": "status_quo_outlook_oceangoing.py",
    "rebuild_strategy": "replace styled_chart template with native column_chart",
}

TEXT_FIT = {
    "chart_title": {
        "box_in": (6.707, 0.167),
        "font_pt": 10,
        "content": "single dense no-wrap chart title",
    },
    "year_ticks": {
        "box_in": (0.167, 0.306),
        "font_pt": 8,
        "content": "four-digit years, right aligned",
    },
    "bar_total_labels": {
        "box_in": "0.115-0.161 wide x 0.167 high",
        "font_pt": 10,
        "content": "one signed net hull integer",
    },
    "retirement_replacement_table": {
        "box_in": (5.049, 3.867),
        "font_pt": "10 body / 16 red values",
        "content": "title + header + four archetype rows + commentary row",
    },
}


def _net_hulls_by_year() -> tuple[int, ...]:
    return tuple(
        sum(value or 0 for value in values_by_year)
        for values_by_year in zip(*(layer.values for layer in CHART_LAYERS))
    )


def _average_replacements_by_archetype() -> dict[str, tuple[float, float]]:
    retirements = {row.archetype: 0 for row in RETIREMENT_REPLACEMENT_ROWS}
    orderbook = {row.archetype: 0 for row in RETIREMENT_REPLACEMENT_ROWS}
    for layer in CHART_LAYERS:
        for value, fill in zip(layer.values, layer.point_fills()):
            if value is None:
                continue
            if value < 0 and fill in RETIREMENT_FILL_TO_ARCHETYPE:
                retirements[RETIREMENT_FILL_TO_ARCHETYPE[fill]] += abs(value)
            elif value > 0 and fill in ORDERBOOK_FILL_TO_ARCHETYPE:
                orderbook[ORDERBOOK_FILL_TO_ARCHETYPE[fill]] += value
    return {
        archetype: (retirements[archetype] / len(YEARS), (retirements[archetype] - orderbook[archetype]) / len(YEARS))
        for archetype in retirements
    }


def _display_average(value: float) -> str:
    return f"~{value:.1f}"


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
    """tcell with span/align/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...)."""
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell_rich with span/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...)."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def _replacement_table(sp_id: int) -> str:
    """Right-side native table, driven by semantic replacement-rate rows."""

    rows = [
        trow([cell("Average retirement replacements required per year ’26-’50", bold=True, span=3, B=edge(BLACK))], h=IN(0)),
        trow([
            cell("Archetype", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK)),
            cell("Total", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK)),
            cell("Net of Orderbook Deliveries", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK)),
        ], h=IN(0)),
    ]

    for idx, row in enumerate(RETIREMENT_REPLACEMENT_ROWS):
        rule = BLACK if idx == 0 else "808080"
        rows.append(
            trow([
                cell(row.archetype, bold=True, color=WHITE, fill=row.retirement_fill, T=edge(rule, 6350 if rule != BLACK else 12700), B=edge("808080", 6350)),
                cell(row.total_per_year, size=PT(16), bold=True, color=TABLE_VALUE_RED, align="ctr", T=edge(rule, 6350 if rule != BLACK else 12700), B=edge("808080", 6350)),
                cell(row.net_of_orderbook_per_year, size=PT(16), bold=True, color=TABLE_VALUE_RED, align="ctr", T=edge(rule, 6350 if rule != BLACK else 12700), B=edge("808080", 6350)),
            ], h=IN(0.6))
        )

    rows.append(
        trow([
            cell("Commentary", bold=True, T=edge("808080", 6350)),
            rcell([
                tpara([trun("Assumes owners replace retirements 1-for-1 and at the end of estimated service life", size=PT(10), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450),
                tpara([], bullet=True, mar_l=171450, indent=-171450),
                tpara([trun("Tanker figures include multiple types, including product, chemical & oil, crude, and shuttle", size=PT(10), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450),
            ], span=2, T=edge("808080", 6350)),
        ], h=IN(0.6))
    )

    return table(
        sp_id,
        "RetirementReplacementTable",
        IN(7.747),
        IN(1.685),
        IN(5.049),
        IN(3.867),
        col_widths=[IN(1.181), IN(1.723), IN(2.145)],
        rows=rows,
    )


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_AXIS_Y, _AXIS_W, _AXIS_H = IN(6.026), IN(0.167), IN(0.306)   # x-axis year-label row [x25]
_BARVAL_W, _BARVAL_H = IN(0.161), IN(0.167)                   # bar-total value-label box [x9]
_KEY_W, _KEY_H = IN(0.196), IN(0.146)                   # legend colour-chip [x8]
_LEGEND_LBL_H = IN(0.167)                                     # legend caption height [x8]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the twenty-five year ticks (2026-2050) along the category axis.
_CATEGORY_TICK_LABELS = [    # (x, label) x25 — category-axis year labels 2026–2050
    (0.83, "2026"),
    (1.102, "2027"),
    (1.375, "2028"),
    (1.648, "2029"),
    (1.92, "2030"),
    (2.193, "2031"),
    (2.465, "2032"),
    (2.738, "2033"),
    (3.01, "2034"),
    (3.283, "2035"),
    (3.556, "2036"),
    (3.828, "2037"),
    (4.101, "2038"),
    (4.375, "2039"),
    (4.648, "2040"),
    (4.92, "2041"),
    (5.193, "2042"),
    (5.465, "2043"),
    (6.01, "2045"),
    (6.283, "2046"),
    (6.556, "2047"),
    (6.828, "2048"),
    (7.101, "2049"),
    (7.373, "2050"),
    (5.738, "2044"),
]

# local_meaning: the net-hull total printed on each of the nine bars.
_DATA_LABELS = [    # (x, y, label) x9 — net-hull data labels riding the bars
    (0.833, 5.812, "-9"),
    (1.106, 4.528, "-1"),
    (2.469, 4.344, "-2"),
    (4.104, 4.344, "-2"),
    (4.651, 4.528, "-3"),
    (5.469, 4.894, "-5"),
    (5.741, 5.262, "-7"),
    (6.014, 5.262, "-7"),
    (6.286, 4.344, "-2"),
]

# The source chart part carried an additional selective data-label set inside
# slide44_chart26.xml. Because this factory-native rebuild disables native chart
# labels, we manualize those XML label values here. The x positions come from the
# manual year-tick grid; the y positions are solved from the source chart's own
# 4/-2/-3/-5/-7 label scale, so these stay close to the original chart labels.
_CATEGORY_X_BY_LABEL = {label: x for x, label in _CATEGORY_TICK_LABELS}


def _xml_label_y(label_text: str) -> float:
    value = int(label_text)
    if value >= 0:
        return 3.571 - 0.183 * value
    return 3.978 + 0.183 * abs(value)


_XML_DATA_LABELS = tuple(
    (
        _CATEGORY_X_BY_LABEL[YEARS[label.idx]] + 0.003,
        _xml_label_y(label.text),
        0.115 if len(label.text) == 1 else 0.161,
        label.text,
    )
    for label in SOURCE_XML_DATA_LABELS
)

# local_meaning: the paired legend chips: rows 1-4 are the Retirements ramp (blue shades), rows
#   5-8 the Orderbook ramp (greys->black), one per vessel archetype.
_LEGEND_KEYS = [    # (x, y, fill) x8 — Retirements legend (rows 1-4, blue shades) + Orderbook legend (rows 5-8, greys→black)
    (5.33, 2.618, "9DB1CF"),   # 9DB1CF light blue
    (5.33, 2.84, "6F8DB9"),   # 6F8DB9 blue
    (5.33, 3.062, "4C6C9C"),   # 4C6C9C blue
    (5.33, 3.285, "364D6E"),   # 364D6E dark blue
    (6.292, 2.618, "C0C0C0"),   # C0C0C0 silver
    (6.292, 2.84, "969696"),   # 969696 gray
    (6.292, 3.062, "808080"),   # 808080 gray
    (6.292, 3.285, BLACK),   # 000000 black
]

# local_meaning: the eight archetype captions: Retirements legend (left column) and Orderbook
#   legend (right column).
_LEGEND_LABELS = [    # (x, y, cx, label) x8 — archetype captions: Retirements legend (left col) + Orderbook legend (right col)
    (5.582, 2.613, 0.599, "Container"),
    (5.582, 2.835, 0.491, "General"),
    (5.582, 3.057, 0.417, "RORO"),
    (5.582, 3.28, 0.431, "Tanker"),
    (6.543, 2.613, 0.599, "Container"),
    (6.543, 2.835, 0.491, "General"),
    (6.543, 3.057, 0.417, "RORO"),
    (6.543, 3.28, 0.431, "Tanker"),
]
# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level layout convention is expressed by repeating the
# same l_ins/r_ins/t_ins/b_ins, anchor, and alignment across the affected cells.
# In tcell()/tcell_rich(), those insets are internal padding and anchor is vertical
# alignment; tcell align or tpara align/mar_l/indent controls horizontal alignment
# and paragraph margins (including hanging bullet indents).

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Explicit zero/tight insets and wrap="none"
# are alignment devices for chart/exhibit labels; omitted values retain the
# primitive defaults intentionally.


# ════════════════════════════════════════════════════════════════════════════
# Serial-production threshold key — one glyph + caption per support state.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class SerialKeyEntry:
    glyph_color: str
    glyph_x: float
    glyph_y: float
    label_x: float
    label_y: float
    label: str


SERIAL_PRODUCTION_KEY: tuple[SerialKeyEntry, ...] = (
    SerialKeyEntry(TABLE_VALUE_RED, 10.438, 1.429, 10.694, 1.442, "Does not support serial production"),
    SerialKeyEntry("007770", 10.438, 1.187, 10.694, 1.2, "Supports serial production"),
)


# ════════════════════════════════════════════════════════════════════════════
# Paint layer. Each helper appends shapes to the shared sequential id counter `n`
# in the source paint order; emitted names are the slide's teaching surface.
# ════════════════════════════════════════════════════════════════════════════
def paint_orderbook_band(n) -> list[str]:
    """Left-side grey rail flagging the years that carry orderbook data."""
    return [text_box(n(), "OrderbookDataBand", IN(0.783), IN(2.104), IN(1.354), IN(4.276), [paragraph([run("Years with ", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), run("orderbook ", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), run("data", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), line_break(), line_break()], align="r", line_spacing=100000)], fill=GRAY_1, line_color="none", anchor="b")]   # F2F2F2 off-white


def paint_native_chart(n) -> list[str]:
    """Native editable stacked-column chart frame; labels are slide-level objects."""
    # Chart XML/XLSB values are embedded above and generated through CHART_STYLE.
    return [graphic_frame(sp_id=n(), name="Chart", x=IN(0.325), y=IN(1.866), cx=IN(7.359), cy=IN(4.165), rId="rId2")]


def paint_year_ticks(n) -> list[str]:
    """Manual 2026-2050 category ticks: right-aligned, no-wrap, zero-inset so the
    boxes register precisely to the plotted categories."""
    return [text_box(n(), "YearTickLabel", IN(_x), _AXIS_Y, _AXIS_W, _AXIS_H, [paragraph([run(_t, size=PT(8), color=BLACK, font=FONT)], align="r", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", vert="vert270", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0) for _x, _t in _CATEGORY_TICK_LABELS]   # 000000 black; vert270 = rotated 270° (reads bottom-to-top), per source


def paint_chart_title(n) -> list[str]:
    return [text_box(n(), "ChartTitle", IN(0.484), IN(1.752), IN(6.707), IN(0.167), [paragraph([run("Implied Retirements vs. Orderbook of US-Built, US-Flagged Oceangoing Commercial Vessels (# Hulls)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0)]   # 000000 black


def paint_bar_total_labels(n) -> list[str]:
    """Net-hull bar totals, the manualized chart-XML labels, and the two standalone
    orderbook (+4) value labels — centered with tight side insets in source-fit boxes."""
    out: list[str] = []
    for _x, _y, _t in _DATA_LABELS:
        out.append(text_box(n(), "BarTotalLabel", IN(_x), IN(_y), _BARVAL_W, _BARVAL_H, [paragraph([run(_t, size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    for _x, _y, _w, _t in _XML_DATA_LABELS:
        out.append(text_box(n(), "ManualizedChartXmlLabel", IN(_x), IN(_y), IN(_w), _BARVAL_H, [paragraph([run(_t, size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    # two standalone "4" data labels (2029/2030 orderbook), interleaved in paint order
    out.append(text_box(n(), "OrderbookValueLabel", IN(1.674), IN(2.837), IN(0.115), IN(0.167), [paragraph([run("4", size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    out.append(text_box(n(), "OrderbookValueLabel", IN(1.946), IN(2.837), IN(0.115), IN(0.167), [paragraph([run("4", size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    return out


def paint_legend(n) -> list[str]:
    """Paired legend: Retirements frame + Orderbook frame, archetype keys + captions,
    and the bar-total wedge callout (all interleaved in source paint order)."""
    out: list[str] = []
    out.append(text_box(n(), "RetirementsLegendFrame", IN(5.283), IN(2.488), IN(0.932), IN(0.98), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=OUTLINE_NEAR_BLACK, anchor="ctr"))   # 121415 near-black outline
    # Keys have empty centered text bodies; caption boxes below are centered,
    # no-wrap, zero-inset, and use zero paragraph margins.
    for _x, _y, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendColorKey", IN(_x), IN(_y), _KEY_W, _KEY_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    for _x, _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "LegendLabel", IN(_x), IN(_y), IN(_cx), _LEGEND_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "BarTotalCallout", IN(5.193), IN(1.965), IN(2.382), IN(0.425), [paragraph([run("Bar total values indicate net hulls added (removed) each year", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=WHITE, line_color="none", prst="wedgeRectCallout", geom_adj={"adj1": "val -19106", "adj2": "val -3267"}, anchor="ctr"))   # FFFFFF white
    out.append(text_box(n(), "RetirementsLegendCaption", IN(5.325), IN(2.412), IN(0.849), IN(0.159), [paragraph([run("Retirements", size=PT(8), italic=True, color=BLACK, font=FONT), run("1", size=PT(8), italic=True, baseline=30000, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))   # FFFFFF white; "1" = superscript footnote marker
    out.append(text_box(n(), "OrderbookLegendFrame", IN(6.247), IN(2.488), IN(0.932), IN(0.98), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=OUTLINE_NEAR_BLACK, anchor="ctr"))   # 121415 near-black outline
    out.append(text_box(n(), "OrderbookLegendCaption", IN(6.288), IN(2.412), IN(0.849), IN(0.159), [paragraph([run("Orderbook", size=PT(8), italic=True, color=BLACK, font=FONT), run("2", size=PT(8), italic=True, baseline=30000, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))   # FFFFFF white; "2" = superscript footnote marker
    return out


def paint_takeaway_banner(n) -> list[str]:
    return [text_box(n(), "TakeawayBanner", IN(7.79), IN(5.652), IN(5.094), IN(0.68), [paragraph([run("~0.2-1.2 vessels per year is insufficient for serial production ", size=PT(12), bold=True, color=BLACK, font=FONT), run("(5+ hulls/yr. to achieve max labor efficiencies by end of year 2)", size=PT(12), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=SCENARIO_BLUE, line_color="none", anchor="ctr", effects=CALLOUT_SHADOW)]   # CEDDEC pale blue


def paint_source_note(n) -> list[str]:
    """Footnote kept verbatim (sits off the house Source position)."""
    return [text_box(n(), "SourceNote", IN(0.495), IN(6.68), IN(12.367), IN(0.317), [paragraph([run("Note: (1) Service life assumptions – 40 years for Bulk, Container, General Cargo, and RORO, 35 years for Tankers, 30 years for PSVs, and 25 years for Crew/FSVs; (2) All Oceangoing Commercial vessels in orderbook are built at Hanwha Philly, including containerships purchased by Matson and 12x tankers (10x Chemical & Oil and 2x LNG) purchased by Hanwha Shipping | Source: Clarksons (US fleet size and GT data)", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none")]   # 000000 black


def paint_serial_production_key(n) -> list[str]:
    """Red "#" (does not support) / teal "#" (supports) glyph + caption per state."""
    out: list[str] = []
    for entry in SERIAL_PRODUCTION_KEY:
        out.append(text_box(n(), "SerialProductionGlyph", IN(entry.glyph_x), IN(entry.glyph_y), IN(0.301), IN(0.26), [paragraph([run("#", size=PT(16), bold=True, color=entry.glyph_color, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # C30C3E crimson / 007770 teal
        out.append(text_box(n(), "SerialProductionLabel", IN(entry.label_x), IN(entry.label_y), IN(2.101), IN(0.234), [paragraph([run(entry.label, size=PT(10), font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    return out


def paint_hanwha_callout(n) -> list[str]:
    """Wedge callout over the chart noting the Hanwha Shipping tanker purchase."""
    return [text_box(n(), "HanwhaPurchaseCallout", IN(2.239), IN(3.166), IN(1.501), IN(0.416), [paragraph([run("12x purchased by Hanwha Shipping", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val -59329", "adj2": "val -21373"}, anchor="ctr")]   # 000000 black outline


def paint_scenario_chip(n) -> list[str]:
    return [text_box(n(), "ScenarioChip", IN(8.069), IN(0.174), IN(2.977), IN(0.217), [paragraph([run("(1) Status Quo Scenario", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=SCENARIO_BLUE, line_color=BLACK, line_width=19050, anchor="ctr")]   # CEDDEC pale blue; 1.5pt border (source lnRef idx 2)


def _body() -> str:
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE.
    # Paint order is the source z-order; ids stay sequential via the shared `n`.
    out: list[str] = []
    out += paint_orderbook_band(n)
    out += paint_native_chart(n)
    out += paint_year_ticks(n)
    out += paint_chart_title(n)
    out += paint_bar_total_labels(n)
    out.append(_replacement_table(n()))   # avg retirement replacements per year ’26-’50
    out += paint_legend(n)
    out += paint_takeaway_banner(n)
    out += paint_source_note(n)
    out += paint_serial_production_key(n)
    out += paint_hanwha_callout(n)
    out += paint_scenario_chip(n)
    return "".join(out)


CHROME = Chrome(
    section="US-Built Ship Demand",
    topic="Without SHIPS Act",
    title="Status Quo Outlook (Oceangoing Commercial)",
    takeaway="Replacing retirements unlikely to support serial production, preventing meaningful newbuild cost reductions.",
)


def render() -> str:
    return body_slide(CHROME, _body())
