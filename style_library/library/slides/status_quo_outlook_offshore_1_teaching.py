"""Teaching exemplar: offshore FSV/PSV retirement-replacement outlook.

ROLE
  scenario_forecast / serial_production_threshold

USE WHEN
  A slide needs one dominant forecast chart proving that retirement replacement
  alone is not enough for serial production, plus a right-side evidence table,
  serial-production threshold key, and a single takeaway banner.

TEACHES
  - rebuilding a source chart XML / workbook pair as a native editable `column_chart(...)`
  - readable source workbook rows for a negative stacked-column forecast
  - manual year ticks and source-positioned net-hull labels over a native chart
  - left-side shaded "no orderbook" evidence band beside the plot
  - compact legend placed outside the chart rather than relying on native legend XML
  - right-side retirement-replacement table with a merged commentary cell
  - serial-production marker key using repeated text glyphs instead of icons
  - bottom-right takeaway banner as the slide's decision-relevant conclusion

TEXT-FIT PRECEDENT
  orderbook_note:
    geometry: 1.354in wide x 4.276in high
    type: Arial 10pt italic, right aligned
    content: three short lines plus intentional whitespace
    copy_when: a small chart-side band needs to explain missing data, not carry a
               full caveat paragraph

  chart_title:
    geometry: 5.726in wide x 0.167in high
    type: Arial 10pt bold, no-wrap, bottom anchored
    content: one long technical chart title with unit and vessel-scope qualifier
    copy_when: the slide title carries the takeaway and the chart still needs a
               precise analytic caption

  retirement_table_commentary:
    geometry: two merged columns inside a 5.049in table
    type: Arial 10pt bullets with italic parenthetical run
    content: three bullets plus blank-bullet spacing
    copy_when: the chart proves the quantitative pattern and the table must add
               concise operating-context caveats

  takeaway_banner:
    geometry: 5.094in wide x 0.680in high
    type: Arial 12pt bold, centered
    content: one conclusion sentence, not a multi-bullet summary
    copy_when: a right-side table needs a decision-relevant implication below it

SOURCE NOTE
  Teaching rewrite of the source-faithful `status_quo_outlook_offshore_1.py`
  module. The original bundled `slide45_chart27.xml` and
  `slide45_chart27.xlsb` as external chart assets. This version transcribes the source workbook rows and
  key chart XML styling values into Python constants and builds the chart through
  the native `column_chart()` factory, so the module reads no sidecar chart files
  at runtime and PowerPoint Edit Data opens a generated `.xlsx`.

FIDELITY NOTE
  This is a practical native-chart rebuild, not a byte-identical source port. It
  preserves the visible chart semantics, workbook rows, point-level color override,
  fixed axis, manual plot layout, coordinates, labels, table, callouts, legend,
  source note, scenario chip, and takeaway banner. Shape ids are regenerated and
  the code is reorganized around authoring patterns rather than raw conversion
  clusters.
"""
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


# Local table-cell kit (was deck_core.table_kit).
def edge(color, w=12700):
    """One cell-border edge dict (default 1pt hairline)."""
    return {"color": color, "width": w}

def bd(L=None, R=None, T=None, B=None):
    """Border map from only the sides drawn; omitted sides render no-fill."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None

def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", span=1, rowspan=1,
         l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """Single-run text cell; borders via L/R/T/B=edge(...)."""
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))

def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """Multi-paragraph rich cell; borders via L/R/T/B=edge(...)."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))

LAYOUT = "slideLayout4"

# Local semantic palette. Future authors should copy these names rather than the
# converter's generic color literals.
CREW_FAST_SUPPLY_BLUE = "9DB1CF"
PSV_BLUE = "4C6C9C"
SERIAL_PRODUCTION_GREEN = "007770"
SCENARIO_BLUE = "CEDDEC"
QUIET_RULE = "808080"
CALLOUT_DARK_LINE = "121415"


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: small programmatic index for retrieval / agent search.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "scenario_forecast / serial_production_threshold",
    "use_when": (
        "Use for an addressable-offshore forecast where negative retirement "
        "replacement volume must be compared against a serial-production threshold."
    ),
    "teaches": [
        "native negative stacked-column chart",
        "manual dense year ticks on a 25-year horizon",
        "selective net-hull labels rather than every bar label",
        "no-orderbook evidence band beside the chart",
        "right-side retirement replacement table with commentary",
        "serial-production threshold key using glyph markers",
        "takeaway banner below supporting table",
    ],
    "source_module": "status_quo_outlook_offshore_1.py",
    "source_chart_assets": ("slide45_chart27.xml", "slide45_chart27.xlsb"),
    "rebuild_strategy": "replace external chart assets with native column_chart",
}

TEXT_FIT = {
    "orderbook_note": {
        "box_in": (1.354, 4.276),
        "font_pt": 10,
        "content": "No orderbook orders for / FSV / PSV",
        "note": "Right aligned because it sits immediately left of the chart frame.",
    },
    "chart_title": {
        "box_in": (5.726, 0.167),
        "font_pt": 10,
        "content": "long chart title with vessel types and unit in parentheses",
        "note": "No-wrap, bottom anchored, zero inset.",
    },
    "year_ticks": {
        "box_in": (0.167, 0.306),
        "font_pt": 8,
        "content": "four-digit year rotated by narrow box geometry / right alignment",
    },
    "net_hull_labels": {
        "box_in": "0.161-0.238 wide x 0.167 high",
        "font_pt": 10,
        "content": "signed integer, max three characters",
    },
    "retirement_table_commentary": {
        "box_in": "merged 3.868in wide commentary cell",
        "font_pt": 10,
        "content": "three bullet paragraphs plus blank spacing paragraphs",
    },
    "takeaway_banner": {
        "box_in": (5.094, 0.680),
        "font_pt": 12,
        "content": "single centered conclusion sentence",
    },
    "source_note": {
        "box_in": (12.367, 0.306),
        "font_pt": 8,
        "content": "two-line Note / Source block",
    },
}

COPY_RULES = [
    "Use this pattern when the chart's conclusion depends on net negative bars, not segment-level chart labels.",
    "Use manual labels only for years that matter analytically; small or trailing retirements can stay unlabeled.",
    "Keep the serial-production key separate from the table when a metric is about strategic feasibility, not table mechanics.",
    "Use a shaded missing-data band only when absence of orderbook evidence is itself part of the argument.",
    "The takeaway banner should state the threshold implication; do not repeat the table values there.",
]


# ════════════════════════════════════════════════════════════════════════════
# Small semantic records.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    """Geometry in inches; converted to EMU only at the primitive boundary."""

    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class OffshoreRetirementLayer:
    """One source workbook row plus its default and point-level chart fills."""

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
class YearTick:
    """Manual category tick under the chart."""

    box: Box
    label: str


@dataclass(frozen=True)
class NetHullLabel:
    """Manual net-hull label attached to a selected forecast year."""

    year: str
    box: Box
    label: str


@dataclass(frozen=True)
class LegendEntry:
    """Outside-chart legend row."""

    label: str
    fill: str
    swatch_box: Box
    label_box: Box


@dataclass(frozen=True)
class ReplacementRow:
    """One row in the retirement-replacements table."""

    archetype: str
    fill: str
    total: str
    net_of_orderbook: str
    metric_color: str = BLACK


@dataclass(frozen=True)
class SerialKeyEntry:
    """One glyph + caption in the serial-production threshold key."""

    glyph_color: str
    label: str
    glyph_box: Box
    label_box: Box


# ════════════════════════════════════════════════════════════════════════════
# Layout zones. These names are intentionally the teaching surface.
# ════════════════════════════════════════════════════════════════════════════
ORDERBOOK_NOTE = Box(0.783, 2.104, 1.354, 4.276)
CHART_FRAME = Box(0.325, 1.866, 7.359, 4.361)
CHART_TITLE = Box(0.484, 1.752, 5.726, 0.167)
RETIREMENT_REPLACEMENTS_TABLE = Box(7.747, 1.685, 5.049, 3.833)
NET_HULL_CALLOUT = Box(5.087, 1.965, 2.488, 0.425)
RETIREMENT_BACKLOG_CALLOUT = Box(1.271, 5.231, 2.012, 0.561)
SOURCE_NOTE = Box(0.495, 6.692, 12.367, 0.306)
TAKEAWAY_BANNER = Box(7.790, 5.652, 5.094, 0.680)
SCENARIO_CHIP = Box(8.069, 0.174, 2.977, 0.217)

YEAR_TICK_Y = 6.028
YEAR_TICK_W = 0.167
YEAR_TICK_H = 0.306
NET_LABEL_H = 0.167


# ════════════════════════════════════════════════════════════════════════════
# Chart data and semantic overlays.
# ════════════════════════════════════════════════════════════════════════════
YEARS: tuple[str, ...] = tuple(str(year) for year in range(2026, 2051))

PSV_RETIREMENTS: tuple[int | None, ...] = (
    -2, -3, -8, -12, -9, -3, -8, -14, -5, -5, -5, -11, -9, -9, -14,
    -4, -8, -14, -27, -17, -9, -4, -4, -2, -1,
)

CREW_FAST_SUPPLY_RETIREMENTS: tuple[int | None, ...] = (
    -30, None, -3, -3, -7, -4, -7, -9, -7, -2, -3, -5, -4, -6, -6,
    -2, -2, -1, -1, None, None, None, None, None, None,
)

SOURCE_PLOT_LAYOUT = {
    "x": 0.06157112526539278,
    "y": 0.05652866242038217,
    "w": 0.92616183062042934,
    "h": 0.88694267515923564,
}
SOURCE_GAP_WIDTH = 130
SOURCE_BAR_OVERLAP = 100
SOURCE_VALUE_AXIS_MIN = -35
SOURCE_VALUE_AXIS_MAX = 10
SOURCE_VALUE_AXIS_MAJOR_UNIT = 5
SOURCE_AXIS_LINE_WIDTH = 9_525
SOURCE_VALUE_AXIS_FORMAT = '#,##0;"-"#,##0'

# The source workbook's first row is mostly PSV retirements, but its 2027 point
# is explicitly filled light blue in the chart XML, making that point a
# Crew/Fast Supply retirement in the visible chart and in the replacement-rate
# arithmetic. Keeping the source rows plus point fills mirrors the reference
# native rewrites that preserve source-chart row structure while exposing the
# visual semantics in Python.
OFFSHORE_RETIREMENT_SERIES: tuple[OffshoreRetirementLayer, ...] = (
    OffshoreRetirementLayer(
        "Source workbook row 1",
        PSV_RETIREMENTS,
        PSV_BLUE,
        {1: CREW_FAST_SUPPLY_BLUE},
    ),
    OffshoreRetirementLayer(
        "Source workbook row 2",
        CREW_FAST_SUPPLY_RETIREMENTS,
        CREW_FAST_SUPPLY_BLUE,
        {},
    ),
)

YEAR_TICKS: tuple[YearTick, ...] = tuple(
    YearTick(Box(x, YEAR_TICK_Y, YEAR_TICK_W, YEAR_TICK_H), label)
    for x, label in (
        (0.830, "2026"), (1.102, "2027"), (1.375, "2028"), (1.648, "2029"),
        (1.920, "2030"), (2.193, "2031"), (2.465, "2032"), (2.738, "2033"),
        (3.010, "2034"), (3.283, "2035"), (3.556, "2036"), (3.828, "2037"),
        (4.101, "2038"), (4.375, "2039"), (4.648, "2040"), (4.920, "2041"),
        (5.193, "2042"), (5.465, "2043"), (5.738, "2044"), (6.010, "2045"),
        (6.283, "2046"), (6.556, "2047"), (6.828, "2048"), (7.101, "2049"),
        (7.373, "2050"),
    )
)

# Source-positioned net-hull labels. The original slide split these between
# slide-level text labels and selected native chart data labels; the native
# rebuild keeps them all as editable slide labels so no chart template is needed.
NET_HULL_LABELS: tuple[NetHullLabel, ...] = (
    NetHullLabel("2026", Box(0.795, 5.750, 0.238, NET_LABEL_H), "-32"),
    NetHullLabel("2027", Box(1.105, 3.258, 0.161, NET_LABEL_H), "-3"),
    NetHullLabel("2028", Box(1.340, 3.946, 0.238, NET_LABEL_H), "-11"),
    NetHullLabel("2029", Box(1.613, 4.290, 0.238, NET_LABEL_H), "-15"),
    NetHullLabel("2030", Box(1.885, 4.375, 0.238, NET_LABEL_H), "-16"),
    NetHullLabel("2031", Box(2.196, 3.602, 0.161, NET_LABEL_H), "-7"),
    NetHullLabel("2032", Box(2.431, 4.290, 0.238, NET_LABEL_H), "-15"),
    NetHullLabel("2033", Box(2.703, 4.977, 0.238, NET_LABEL_H), "-23"),
    NetHullLabel("2034", Box(2.976, 4.031, 0.238, NET_LABEL_H), "-12"),
    NetHullLabel("2035", Box(3.286, 3.602, 0.161, NET_LABEL_H), "-7"),
    NetHullLabel("2036", Box(3.559, 3.688, 0.161, NET_LABEL_H), "-8"),
    NetHullLabel("2037", Box(3.793, 4.375, 0.238, NET_LABEL_H), "-16"),
    NetHullLabel("2038", Box(4.066, 4.118, 0.238, NET_LABEL_H), "-13"),
    NetHullLabel("2039", Box(4.340, 4.290, 0.238, NET_LABEL_H), "-15"),
    NetHullLabel("2040", Box(4.613, 4.719, 0.238, NET_LABEL_H), "-20"),
    NetHullLabel("2041", Box(4.924, 3.516, 0.161, NET_LABEL_H), "-6"),
    NetHullLabel("2042", Box(5.158, 3.859, 0.238, NET_LABEL_H), "-10"),
    NetHullLabel("2043", Box(5.431, 4.290, 0.238, NET_LABEL_H), "-15"),
    NetHullLabel("2044", Box(5.703, 5.406, 0.238, NET_LABEL_H), "-28"),
    NetHullLabel("2045", Box(5.975, 4.461, 0.238, NET_LABEL_H), "-17"),
    NetHullLabel("2046", Box(6.286, 3.774, 0.161, NET_LABEL_H), "-9"),
    NetHullLabel("2047", Box(6.559, 3.344, 0.161, NET_LABEL_H), "-4"),
    NetHullLabel("2048", Box(6.831, 3.344, 0.161, NET_LABEL_H), "-4"),
    NetHullLabel("2049", Box(7.104, 3.172, 0.161, NET_LABEL_H), "-2"),
    NetHullLabel("2050", Box(7.376, 3.086, 0.161, NET_LABEL_H), "-1"),
)

LEGEND_ENTRIES: tuple[LegendEntry, ...] = (
    LegendEntry(
        "Crew/Fast Supply",
        CREW_FAST_SUPPLY_BLUE,
        Box(5.194, 2.451, 0.196, 0.146),
        Box(5.446, 2.446, 1.092, 0.167),
    ),
    LegendEntry(
        "PSV",
        PSV_BLUE,
        Box(5.194, 2.674, 0.196, 0.146),
        Box(5.446, 2.668, 0.276, 0.167),
    ),
)

RETIREMENT_REPLACEMENT_ROWS: tuple[ReplacementRow, ...] = (
    ReplacementRow("Crew/Fast Supply", CREW_FAST_SUPPLY_BLUE, "~4.2", "~4.2"),
    ReplacementRow("PSV", PSV_BLUE, "~8.2", "~8.2", SERIAL_PRODUCTION_GREEN),
)

COMMENTARY_BULLETS: tuple[tuple[str, str | None], ...] = (
    (
        "1-for-1 retirement replacements potentially challenged by O&G sector maintaining capital discipline that drives retirement deferrals ",
        "(potentially mitigated if crude prices remain high due to Persian Gulf disruptions)",
    ),
    (
        "Only Offshore O&G vessel types with orders are Multipurpose Support Vessels (2x on order), providing evidence of constrained upstream capex environment",
        None,
    ),
    (
        "Other Offshore O&G vessel types have smaller fleet counts than PSV and Crew/Fast Supply (1-66 vs. 206 and 105, respectively), likely precluding serial production",
        None,
    ),
)

SERIAL_PRODUCTION_KEY: tuple[SerialKeyEntry, ...] = (
    SerialKeyEntry(
        SERIAL_PRODUCTION_GREEN,
        "Supports serial production",
        Box(10.438, 1.187, 0.301, 0.260),
        Box(10.694, 1.200, 2.101, 0.234),
    ),
    SerialKeyEntry(
        BLACK,
        "Potentially supports serial production",
        Box(10.438, 1.429, 0.301, 0.260),
        Box(10.694, 1.442, 2.101, 0.234),
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Native chart wiring: source XML/XLSB values are explicit Python constants.
# ════════════════════════════════════════════════════════════════════════════
_CHART0_DATA = {
    "categories": YEARS,
    "series": [
        {"name": layer.name, "values": list(layer.values)}
        for layer in OFFSHORE_RETIREMENT_SERIES
    ],
}

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(YEARS),
    "series": [layer.chart_dict() for layer in OFFSHORE_RETIREMENT_SERIES],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": True,
    "show_gridlines": False,
    "show_value_labels": False,
    "value_axis_format": SOURCE_VALUE_AXIS_FORMAT,
    "value_label_format": SOURCE_VALUE_AXIS_FORMAT,
    "cat_label_size_pt": 10,
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


# ════════════════════════════════════════════════════════════════════════════
# Validation helpers. These catch teaching-data drift early.
# ════════════════════════════════════════════════════════════════════════════
def _average_replacements_by_fill(fill: str) -> float:
    total = 0
    for layer in OFFSHORE_RETIREMENT_SERIES:
        for value, point_fill in zip(layer.values, layer.point_fills()):
            if value is not None and value < 0 and point_fill == fill:
                total += abs(value)
    return total / len(YEARS)


def _display_average(value: float) -> str:
    return f"~{value:.1f}"


# ════════════════════════════════════════════════════════════════════════════
# Tiny local authoring helpers.
# ════════════════════════════════════════════════════════════════════════════
def _textbox(sp_id: int, name: str, box: Box, paras: list[str], **kwargs) -> str:
    return text_box(sp_id, name, *box.emu(), paras, **kwargs)


def _one_line(
    text: str,
    *,
    size: int = PT(10),
    bold: bool = False,
    italic: bool = False,
    color: str = BLACK,
    align: str | None = None,
) -> str:
    return paragraph(
        [run(text, size=size, bold=bold or None, italic=italic or None, color=color, font=FONT)],
        align=align,
        mar_l=0,
        indent=0,
        line_spacing=100000,
    )


def _empty_centered_paragraph() -> str:
    return paragraph([], align="ctr", line_spacing=100000)


def _commentary_paragraph(text: str, italic_tail: str | None = None) -> str:
    runs = [trun(text, size=PT(10), color=BLACK, font=FONT)]
    if italic_tail:
        runs.append(trun(italic_tail, size=PT(10), italic=True, color=BLACK, font=FONT))
    return tpara(runs, bullet=True, mar_l=171450, indent=-171450)


def _blank_bullet_spacing() -> str:
    return tpara([], bullet=True, mar_l=171450, indent=-171450, end_size=PT(10))


# ════════════════════════════════════════════════════════════════════════════
# Paint functions. Order follows the source's visible stacking while grouping
# shapes by reusable teaching purpose.
# ════════════════════════════════════════════════════════════════════════════
def paint_orderbook_note(next_id) -> list[str]:
    """Left-side evidence band: no orderbook orders for the plotted vessel types."""

    return [
        _textbox(
            next_id(),
            "NoOrderbookEvidenceBand",
            ORDERBOOK_NOTE,
            [
                paragraph(
                    [
                        run("No orderbook orders for ", size=PT(10), italic=True, color=BLACK, font=FONT),
                        line_break(),
                        run("FSV / PSV", size=PT(10), italic=True, color=BLACK, font=FONT),
                        line_break(),
                        line_break(),
                        line_break(),
                    ],
                    align="r",
                    line_spacing=100000,
                )
            ],
            fill=GRAY_1,
            line_color="none",
        )
    ]


def paint_native_chart(next_id) -> list[str]:
    """Native editable chart frame; labels are slide-level objects."""

    x, y, w, h = CHART_FRAME.emu()
    return [graphic_frame(sp_id=next_id(), name="Chart", x=x, y=y, cx=w, cy=h, rId="rId2")]


def paint_manual_year_ticks(next_id) -> list[str]:
    """Manual 2026-2050 year labels under the chart."""

    shapes: list[str] = []
    for tick in YEAR_TICKS:
        shapes.append(
            _textbox(
                next_id(),
                "YearTickLabel",
                tick.box,
                [_one_line(tick.label, size=PT(8), align="r")],
                fill=None,
                line_color="none",
                anchor="ctr",
                wrap="none",
                vert="vert270",   # rotate years to read bottom-to-top, matching the source
                l_ins=0,
                t_ins=0,
                r_ins=0,
                b_ins=0,
            )
        )
    return shapes


def paint_net_hull_labels(next_id) -> list[str]:
    """Selective manual labels for analytically meaningful net hull removals."""

    shapes: list[str] = []
    for label in NET_HULL_LABELS:
        shapes.append(
            _textbox(
                next_id(),
                "NetHullLabel",
                label.box,
                [_one_line(label.label, align="ctr")],
                fill=None,
                line_color="none",
                wrap="none",
                l_ins=17463,
                t_ins=0,
                r_ins=17463,
                b_ins=0,
            )
        )
    return shapes


def paint_chart_title(next_id) -> list[str]:
    """Technical chart caption outside the chart template."""

    return [
        _textbox(
            next_id(),
            "ChartTitle",
            CHART_TITLE,
            [
                _one_line(
                    "Implied Retirements vs. Orderbook of US-Built, US-Flagged Offshore FSV/PSV (# Hulls)",
                    size=PT(10),
                    bold=True,
                )
            ],
            fill=None,
            line_color="none",
            anchor="b",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        )
    ]


def paint_retirement_replacements_table(next_id) -> list[str]:
    """Right-side evidence table: replacement rates plus operating-context commentary."""

    commentary_paras: list[str] = []
    for idx, (text, italic_tail) in enumerate(COMMENTARY_BULLETS):
        if idx:
            commentary_paras.append(_blank_bullet_spacing())
        commentary_paras.append(_commentary_paragraph(text, italic_tail))

    rows = [
        trow(
            [cell("Average retirement replacements required per year ’26-’50", bold=True, anchor="t", span=3, B=edge(BLACK))],
            h=IN(0),
        ),
        trow(
            [
                cell("Archetype", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK)),
                cell("Total", bold=True, align="ctr", anchor="t", T=edge(BLACK), B=edge(BLACK)),
                cell("Net of Orderbook Deliveries", bold=True, align="ctr", anchor="t", T=edge(BLACK), B=edge(BLACK)),
            ],
            h=IN(0),
        ),
    ]

    row_rules = [
        (edge(BLACK), edge(QUIET_RULE, 6350)),
        (edge(QUIET_RULE, 6350), edge(QUIET_RULE, 6350)),
    ]
    for replacement, (top_rule, bottom_rule) in zip(RETIREMENT_REPLACEMENT_ROWS, row_rules):
        rows.append(
            trow(
                [
                    cell(
                        replacement.archetype,
                        bold=True,
                        color=WHITE,
                        fill=replacement.fill,
                        T=top_rule,
                        B=bottom_rule,
                    ),
                    rcell(
                        [tpara([trun(replacement.total, size=PT(16), bold=True, color=replacement.metric_color, font=FONT)], align="ctr", mar_l=0, indent=0)],
                        T=top_rule,
                        B=bottom_rule,
                    ),
                    rcell(
                        [tpara([trun(replacement.net_of_orderbook, size=PT(16), bold=True, color=replacement.metric_color, font=FONT)], align="ctr", mar_l=0, indent=0)],
                        T=top_rule,
                        B=bottom_rule,
                    ),
                ],
                h=IN(0.6),
            )
        )

    rows.append(
        trow(
            [
                cell("Commentary", bold=True, T=edge(QUIET_RULE, 6350)),
                rcell(commentary_paras, span=2, T=edge(QUIET_RULE, 6350)),
            ],
            h=IN(0.6),
        )
    )

    x, y, w, h = RETIREMENT_REPLACEMENTS_TABLE.emu()
    return [
        table(
            next_id(),
            "RetirementReplacementsTable",
            x,
            y,
            w,
            h,
            col_widths=[IN(1.181), IN(1.723), IN(2.145)],
            rows=rows,
        )
    ]


def paint_chart_callout_and_legend(next_id) -> list[str]:
    """The chart-local net-hulls explanation and two-entry archetype legend."""

    shapes = [
        _textbox(
            next_id(),
            "NetHullsCallout",
            NET_HULL_CALLOUT,
            [_one_line("Bar total values indicate net hulls added (removed) each year", italic=True)],
            fill=WHITE,
            line_color="none",
            prst="wedgeRectCallout",
            geom_adj={"adj1": "val -19106", "adj2": "val -3267"},
            anchor="ctr",
        )
    ]
    for entry in LEGEND_ENTRIES:
        shapes.append(
            _textbox(
                next_id(),
                "LegendSwatch",
                entry.swatch_box,
                [_empty_centered_paragraph()],
                fill=entry.fill,
                line_color="none",
                anchor="ctr",
            )
        )
    for entry in LEGEND_ENTRIES:
        shapes.append(
            _textbox(
                next_id(),
                "LegendLabel",
                entry.label_box,
                [_one_line(entry.label)],
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
    return shapes


def paint_source_note(next_id) -> list[str]:
    """Off-house Note / Source block preserved at the source position."""

    return [
        _textbox(
            next_id(),
            "SourceNote",
            SOURCE_NOTE,
            [
                paragraph(
                    [
                        run("Note: Service life assumptions – 30 years for PSVs and 25 years for Crew/FSVs ", size=PT(8), color=BLACK, font=FONT),
                        line_break(),
                        run("Source: Clarksons (US fleet size and GT data); ", size=PT(8), color=BLACK, font=FONT),
                        run("McKinsey article on O&G sector operating model", size=PT(8), color=BLACK, font=FONT),
                    ],
                    line_spacing=100000,
                )
            ],
            fill=None,
            line_color="none",
        )
    ]


def paint_retirement_backlog_callout(next_id) -> list[str]:
    """Over-chart caveat explaining why old vessels may stay in service."""

    return [
        _textbox(
            next_id(),
            "RetirementBacklogCallout",
            RETIREMENT_BACKLOG_CALLOUT,
            [_one_line("Retirement backlog suggests owners likely to keep vessels in service despite age", italic=True)],
            fill=WHITE,
            line_color=CALLOUT_DARK_LINE,
            prst="wedgeRectCallout",
            geom_adj={"adj1": "val -60475", "adj2": "val 8630"},
            anchor="ctr",
        )
    ]


def paint_serial_production_key(next_id) -> list[str]:
    """Glyph-based key for whether table values support serial production."""

    shapes: list[str] = []
    for entry in SERIAL_PRODUCTION_KEY:
        shapes.append(
            _textbox(
                next_id(),
                "SerialProductionGlyph",
                entry.glyph_box,
                [_one_line("#", size=PT(16), bold=True, color=entry.glyph_color, align="ctr")],
                fill=None,
                line_color="none",
                anchor="ctr",
            )
        )
        shapes.append(
            _textbox(
                next_id(),
                "SerialProductionLabel",
                entry.label_box,
                [_one_line(entry.label)],
                fill=None,
                line_color="none",
                anchor="ctr",
                wrap="none",
            )
        )
    return shapes


# Reference drop-shadow on the light-blue callout (outerShdw, verbatim params from
# the source deck): 0.056" blur, 0.03" offset down-right, black @ 40% alpha.
CALLOUT_SHADOW = (
    '<a:effectLst><a:outerShdw blurRad="50800" dist="38100" dir="2700000" '
    'algn="tl" rotWithShape="0"><a:prstClr val="black"><a:alpha val="40000"/>'
    '</a:prstClr></a:outerShdw></a:effectLst>'
)


def paint_takeaway_banner(next_id) -> list[str]:
    """Decision-relevant implication below the right-side evidence table."""

    return [
        _textbox(
            next_id(),
            "TakeawayBanner",
            TAKEAWAY_BANNER,
            [
                _one_line(
                    "Achieving PSV serial production requires capturing 60%+ of the market; potential to serve international demand as US remains competitive in OSVs",
                    size=PT(12),
                    bold=True,
                    align="ctr",
                )
            ],
            fill=SCENARIO_BLUE,
            line_color="none",
            anchor="ctr",
            effects=CALLOUT_SHADOW,
        )
    ]


def paint_scenario_chrome(next_id) -> list[str]:
    """Preliminary chip and scenario chip paint last, like the source slide."""

    return [
        "",
        _textbox(
            next_id(),
            "ScenarioChip",
            SCENARIO_CHIP,
            [_one_line("(1) Status Quo Scenario", size=PT(12), bold=True, align="ctr")],
            fill=SCENARIO_BLUE,         # CEDDEC = theme bg2 @ 90% lum (reference chip fill)
            line_color=BLACK,
            line_width=19050,           # 1.5pt — reference chip border (theme lnRef idx=2)
            anchor="ctr",
        ),
    ]


def _body() -> str:
    shapes: list[str] = []
    ids = iter(range(100, 2000))
    next_id = lambda: next(ids)  # noqa: E731 - compact sequential shape ids

    # The source slide had a dropped think-cell OLE frame. The rendered chart is
    # represented by the native chart part above.
    shapes.extend(paint_orderbook_note(next_id))
    shapes.extend(paint_native_chart(next_id))
    shapes.extend(paint_manual_year_ticks(next_id))
    shapes.extend(paint_net_hull_labels(next_id))
    shapes.extend(paint_chart_title(next_id))
    shapes.extend(paint_retirement_replacements_table(next_id))
    shapes.extend(paint_chart_callout_and_legend(next_id))
    shapes.extend(paint_source_note(next_id))
    shapes.extend(paint_retirement_backlog_callout(next_id))
    shapes.extend(paint_serial_production_key(next_id))
    shapes.extend(paint_takeaway_banner(next_id))
    shapes.extend(paint_scenario_chrome(next_id))
    return "".join(shapes)


CHROME = Chrome(
    section="US-Built Ship Demand",
    topic="Status Quo",
    title="Status Quo Outlook (Addressable Offshore 1/2)",
    takeaway="Achieving serial production of FSVs requires capturing 60%+ of the market and more favorable upstream player capex outlook.",
)


def render() -> str:
    return body_slide(CHROME, _body())
