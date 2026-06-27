"""Teaching exemplar: status-quo fleet outlook net-additions chart.

ROLE
  scenario_forecast / net_fleet_change

USE WHEN
  A slide needs one dominant time-series column chart with positive early-period
  additions, negative later-period retirements, manual axis ticks, manual bar
  totals, and a small explanatory legend/callout system.

TEACHES
  - native editable `column_chart(mode="stacked")` with positive and negative values
  - fixed value-axis scaling while hiding native tick labels in favor of manual labels
  - manual year ticks and manual net-total labels over a native chart
  - left-side shaded data-availability band beside the plot
  - compact legend outside the native chart, keyed by semantic series role
  - dashed trend connector plus wedge callouts layered over/around the chart
  - scenario-chip and footnote placement without using the house sources slot

TEXT-FIT PRECEDENT
  chart_title:
    geometry: 8.285in wide x 0.167in high
    type: Arial 10pt bold, no-wrap
    content: one dense chart title with unit and scope qualifier
    copy_when: the exhibit needs a long technical caption but the slide title
               already carries the executive takeaway

  bar_total_labels:
    geometry: 0.238-0.314in wide x 0.167in high
    type: Arial 10pt, centered, zero top/bottom inset
    content: one signed integer, max four characters
    copy_when: a column chart's analytical value is net movement by year rather
               than segment-level detail

  average_retirements_callout:
    geometry: 1.200in wide x 0.522in high
    type: Arial 10pt italic with one bold phrase
    content: one short sentence fragment, not a paragraph
    copy_when: a late-period trend needs one statistical readout

SOURCE NOTE
  Teaching rewrite of the source-faithful `status_quo_fleet_outlook.py` module.
  The original used `styled_chart(...)` with `slide43_chart25.xml/.xlsb`; this
  version intentionally rebuilds the chart as a native editable PowerPoint
  `column_chart(mode="stacked")`. The visible slide contract is preserved through
  source-positioned manual value-axis labels, year ticks, net labels, legend,
  callouts, off-house Note/Source block, chrome, and scenario chip.

FIDELITY NOTE
  This is a practical factory-native rebuild, not a byte-identical chart-template
  port. It preserves the data, fixed -350K to +350K scale, source labels,
  legend semantics, and major layout. Small differences in native column widths,
  gridline placement, or zero-line rendering may occur relative to the source
  chart template.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, column_chart, connector, graphic_frame, line_break,
    paragraph, run, text_box,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
GRAY_1 = "F2F2F2"
FONT = "Arial"

LAYOUT = "slideLayout4"

# Local semantic palette. These names are more useful to future authors than the
# source converter's anonymous color literals.
COMMERCIAL_TEAL = "007770"
OFFSHORE_AMBER = "FFC000"
SCENARIO_BLUE = "CEDDEC"
QUIET_GRIDLINE = "D9D9D9"
TREND_LINE = BLACK


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: a small programmatic index for retrieval / agent search.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "scenario_forecast / net_fleet_change",
    "use_when": (
        "Use for a forecast chart where early positive additions transition into "
        "long-run negative retirements, and the slide should foreground net totals."
    ),
    "teaches": [
        "native stacked column chart with positive and negative values",
        "fixed hidden value axis plus manual value-axis tick labels",
        "manual category ticks for a dense 25-year horizon",
        "manual signed bar-total labels",
        "orderbook-data availability band",
        "outside-chart four-entry legend",
        "dashed trend connector with callouts",
    ],
    "source_module": "status_quo_fleet_outlook.py",
    "rebuild_strategy": "replace styled_chart template with native column_chart",
}

TEXT_FIT = {
    "orderbook_data_band": {
        "box_in": (2.182, 4.196),
        "font_pt": 10,
        "content": "three short italic words split across line breaks",
        "note": "Use explicit line_break() instead of relying on wrapping.",
    },
    "value_axis_tick_labels": {
        "box_in": "0.076-0.276 wide x 0.167 high",
        "font_pt": 10,
        "content": "one y-axis tick value, right aligned",
        "note": "Keep labels manual when hidden native ticks allow a tighter plot area.",
    },
    "category_year_ticks": {
        "box_in": (0.319, 0.167),
        "font_pt": 10,
        "content": "four-digit year",
        "note": "This is a proven fit for 25 annual ticks across an 11in chart frame.",
    },
    "bar_total_labels": {
        "box_in": "0.238-0.314 wide x 0.167 high",
        "font_pt": 10,
        "content": "signed integer; max four characters",
    },
    "source_note": {
        "box_in": (12.367, 0.319),
        "font_pt": 8,
        "content": "two-line Note / Source block",
    },
}

COPY_RULES = [
    "Use this pattern when the meaningful readout is the net total per year; hide native labels and overlay the values manually.",
    "Keep the y-axis ticks manual when the native chart needs exact source-like tick placement or a nonstandard chart frame.",
    "Use a shaded data-availability band only when the early forecast years are governed by a different evidence basis than the long-run projection.",
    "Do not use the small right callout for multi-sentence reasoning; keep it to one trend statistic.",
]


# ════════════════════════════════════════════════════════════════════════════
# Small semantic geometry/data records.
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
class ForecastSeries:
    """One native chart series expressed in thousands of gross tons."""

    name: str
    fill: str
    values_k_gt: tuple[float | None, ...]

    def chart_dict(self) -> dict:
        return {
            "name": self.name,
            "color": self.fill,
            "values": list(self.values_k_gt),
            "hide_labels": True,
        }


@dataclass(frozen=True)
class AxisTick:
    """Manual y-axis tick label."""

    box: Box
    label: str


@dataclass(frozen=True)
class YearTick:
    """Manual x-axis category tick."""

    box: Box
    label: str


@dataclass(frozen=True)
class NetTotalLabel:
    """Signed net total label attached to one forecast year."""

    box: Box
    label: str
    anchor: str
    name: str = "NetTotalLabel"


@dataclass(frozen=True)
class LegendEntry:
    """Outside-chart legend row."""

    label: str
    fill: str
    swatch_box: Box
    label_box: Box


# ════════════════════════════════════════════════════════════════════════════
# Layout zones. These names are intentionally the teaching surface.
# ════════════════════════════════════════════════════════════════════════════
ORDERBOOK_DATA_BAND = Box(0.950, 2.104, 2.182, 4.196)
CHART_FRAME = Box(0.865, 2.023, 11.062, 4.155)
CHART_TITLE = Box(0.585, 1.752, 8.285, 0.167)
SOURCE_NOTE = Box(0.495, 6.679, 12.367, 0.319)
SCENARIO_CHIP = Box(8.069, 0.174, 2.977, 0.217)

YTICK_H = 0.167
YEAR_TICK_W = 0.319
YEAR_TICK_H = 0.167
YEAR_TICK_Y = 6.134
NET_LABEL_H = 0.167

LEGEND_SWATCH_X = 10.156
LEGEND_SWATCH_W = 0.196
LEGEND_SWATCH_H = 0.146
LEGEND_LABEL_X = 10.408
LEGEND_LABEL_H = 0.167

NET_TOTAL_CALLOUT = Box(10.306, 1.705, 2.488, 0.425)
AVG_RETIREMENT_CALLOUT = Box(11.806, 4.632, 1.200, 0.522)
TREND_CONNECTOR = (3.196, 4.898, 8.700, 0.000)


# ════════════════════════════════════════════════════════════════════════════
# Semantic chart data.
# Values are thousands of gross tons (K GT), matching the manual axis scale.
# The manual net labels below are generated from these values but keep source
# positions because those positions were hand-authored around the source chart.
# ════════════════════════════════════════════════════════════════════════════
YEARS: tuple[str, ...] = tuple(str(year) for year in range(2026, 2051))

COMMERCIAL_ORDERBOOK_AND_RETIREMENTS_K_GT = tuple(
    v / 1000
    for v in (
        48049, 96098, 222000, 285000, 285000, -8415, -22359, -31669, -15549,
        -13908, -14256, -29826, -23429, -25050, -33881, -11820, -31534,
        -45321, -103450, -58863, -35032, -16215, -18412, -7328, -1634,
    )
)

OFFSHORE_RETIREMENTS_K_GT = tuple(
    None if v is None else v / 1000
    for v in (
        -12518, -949, -16350, -24688, -18715, -1904, -61988, -91245, -61540,
        None, -85099, -85098, -86641, -196080, -230065, -196080, -87726,
        -221687, -208874, -216895, -55958, -59960, -29242, -62318, -151354,
    )
)

OFFSHORE_ORDERBOOK_K_GT = tuple(
    None if v is None else v / 1000
    for v in (
        -196731, -62895, None, -16771, -1495, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None,
    )
)

FORECAST_SERIES: tuple[ForecastSeries, ...] = (
    ForecastSeries(
        "Addressable Commercial Orderbook / Retirements",
        COMMERCIAL_TEAL,
        COMMERCIAL_ORDERBOOK_AND_RETIREMENTS_K_GT,
    ),
    ForecastSeries("Addressable Offshore Retirements", OFFSHORE_AMBER, OFFSHORE_RETIREMENTS_K_GT),
    ForecastSeries("Addressable Offshore Orderbook", OFFSHORE_AMBER, OFFSHORE_ORDERBOOK_K_GT),
)

NET_TOTALS_K_GT: tuple[int, ...] = tuple(
    round(sum(value or 0 for value in year_values))
    for year_values in zip(*(series.values_k_gt for series in FORECAST_SERIES))
)


# ════════════════════════════════════════════════════════════════════════════
# Manual labels copied from the source slide's coordinates.
# ════════════════════════════════════════════════════════════════════════════
VALUE_AXIS_TICKS: tuple[AxisTick, ...] = (
    AxisTick(Box(0.538, 6.003, 0.276, YTICK_H), "-350"),
    AxisTick(Box(0.538, 5.720, 0.276, YTICK_H), "-300"),
    AxisTick(Box(0.538, 5.436, 0.276, YTICK_H), "-250"),
    AxisTick(Box(0.538, 5.153, 0.276, YTICK_H), "-200"),
    AxisTick(Box(0.538, 4.868, 0.276, YTICK_H), "-150"),
    AxisTick(Box(0.538, 4.585, 0.276, YTICK_H), "-100"),
    AxisTick(Box(0.615, 4.300, 0.200, YTICK_H), "-50"),
    AxisTick(Box(0.738, 4.017, 0.076, YTICK_H), "0"),
    AxisTick(Box(0.661, 3.733, 0.153, YTICK_H), "50"),
    AxisTick(Box(0.585, 3.450, 0.229, YTICK_H), "100"),
    AxisTick(Box(0.585, 3.165, 0.229, YTICK_H), "150"),
    AxisTick(Box(0.585, 2.882, 0.229, YTICK_H), "200"),
    AxisTick(Box(0.585, 2.597, 0.229, YTICK_H), "250"),
    AxisTick(Box(0.585, 2.314, 0.229, YTICK_H), "300"),
    AxisTick(Box(0.585, 2.030, 0.229, YTICK_H), "350"),
)

YEAR_TICKS: tuple[YearTick, ...] = tuple(
    YearTick(Box(x, YEAR_TICK_Y, YEAR_TICK_W, YEAR_TICK_H), label)
    for x, label in (
        (1.012, "2026"), (1.446, "2027"), (1.882, "2028"), (2.318, "2029"),
        (2.753, "2030"), (3.188, "2031"), (3.623, "2032"), (4.059, "2033"),
        (4.493, "2034"), (4.929, "2035"), (5.365, "2036"), (5.800, "2037"),
        (6.234, "2038"), (6.670, "2039"), (7.106, "2040"), (7.542, "2041"),
        (7.976, "2042"), (8.411, "2043"), (8.847, "2044"), (9.281, "2045"),
        (9.717, "2046"), (10.153, "2047"), (10.589, "2048"), (11.023, "2049"),
        (11.458, "2050"),
    )
)

# Source-positioned net labels. The final text is checked against NET_TOTALS_K_GT
# by `_validate_semantics()` below so chart edits do not silently desynchronize.
NET_TOTAL_LABELS: tuple[NetTotalLabel, ...] = (
    NetTotalLabel(Box(1.016, 5.316, 0.314, NET_LABEL_H), "-161", "t"),
    NetTotalLabel(Box(3.229, 4.186, 0.238, NET_LABEL_H), "-10", "t"),
    NetTotalLabel(Box(3.665, 4.606, 0.238, NET_LABEL_H), "-84", "t"),
    NetTotalLabel(Box(4.062, 4.825, 0.314, NET_LABEL_H), "-123", "t"),
    NetTotalLabel(Box(4.535, 4.566, 0.238, NET_LABEL_H), "-77", "t"),
    NetTotalLabel(Box(5.406, 4.691, 0.238, NET_LABEL_H), "-99", "t"),
    NetTotalLabel(Box(5.804, 4.780, 0.314, NET_LABEL_H), "-115", "t"),
    NetTotalLabel(Box(6.238, 4.752, 0.314, NET_LABEL_H), "-110", "t"),
    NetTotalLabel(Box(6.674, 5.384, 0.314, NET_LABEL_H), "-221", "t"),
    NetTotalLabel(Box(7.109, 5.627, 0.314, NET_LABEL_H), "-264", "t"),
    NetTotalLabel(Box(7.545, 5.307, 0.314, NET_LABEL_H), "-208", "t"),
    NetTotalLabel(Box(7.979, 4.804, 0.314, NET_LABEL_H), "-119", "t"),
    NetTotalLabel(Box(4.970, 4.207, 0.238, NET_LABEL_H), "-14", "t"),
    NetTotalLabel(Box(8.851, 5.901, 0.314, NET_LABEL_H), "-312", "t"),
    NetTotalLabel(Box(9.285, 5.693, 0.314, NET_LABEL_H), "-276", "t"),
    NetTotalLabel(Box(9.759, 4.644, 0.238, NET_LABEL_H), "-91", "t"),
    NetTotalLabel(Box(10.194, 4.561, 0.238, NET_LABEL_H), "-76", "t"),
    NetTotalLabel(Box(10.630, 4.398, 0.238, NET_LABEL_H), "-48", "t"),
    NetTotalLabel(Box(11.064, 4.523, 0.238, NET_LABEL_H), "-70", "t"),
    NetTotalLabel(Box(11.462, 4.997, 0.314, NET_LABEL_H), "-153", "t"),
    NetTotalLabel(Box(8.415, 5.644, 0.314, NET_LABEL_H), "-267", "t"),
    NetTotalLabel(Box(1.510, 3.359, 0.191, NET_LABEL_H), "32", "b", "PositiveNetTotalLabel"),
    NetTotalLabel(Box(1.908, 2.646, 0.267, NET_LABEL_H), "206", "b", "PositiveNetTotalLabel"),
    NetTotalLabel(Box(2.344, 2.288, 0.267, NET_LABEL_H), "244", "b", "PositiveNetTotalLabel"),
    NetTotalLabel(Box(2.780, 2.288, 0.267, NET_LABEL_H), "265", "b", "PositiveNetTotalLabel"),
)

# Map from label text to the expected source order. Source paint order places
# labels in hand-authored stacking order, not chronological order. This tuple is
# the same labels sorted chronologically, used only for validation/documentation.
NET_TOTAL_LABELS_CHRONOLOGICAL: tuple[str, ...] = tuple(str(v) for v in NET_TOTALS_K_GT)

LEGEND_ENTRIES: tuple[LegendEntry, ...] = (
    LegendEntry(
        "Addressable Commercial Retirements",
        COMMERCIAL_TEAL,
        Box(LEGEND_SWATCH_X, 2.174, LEGEND_SWATCH_W, LEGEND_SWATCH_H),
        Box(LEGEND_LABEL_X, 2.168, 2.332, LEGEND_LABEL_H),
    ),
    LegendEntry(
        "Addressable Commercial Orderbook",
        COMMERCIAL_TEAL,
        Box(LEGEND_SWATCH_X, 2.396, LEGEND_SWATCH_W, LEGEND_SWATCH_H),
        Box(LEGEND_LABEL_X, 2.391, 2.238, LEGEND_LABEL_H),
    ),
    LegendEntry(
        "Addressable Offshore Retirements",
        OFFSHORE_AMBER,
        Box(LEGEND_SWATCH_X, 2.618, LEGEND_SWATCH_W, LEGEND_SWATCH_H),
        Box(LEGEND_LABEL_X, 2.613, 2.120, LEGEND_LABEL_H),
    ),
    LegendEntry(
        "Addressable Offshore Orderbook",
        OFFSHORE_AMBER,
        Box(LEGEND_SWATCH_X, 2.840, LEGEND_SWATCH_W, LEGEND_SWATCH_H),
        Box(LEGEND_LABEL_X, 2.835, 2.026, LEGEND_LABEL_H),
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Native editable chart specification.
# The chart draws bars/columns only. All labels and explanatory material are
# source-positioned slide text so future authors can see the annotation grammar.
# ════════════════════════════════════════════════════════════════════════════
CHART_STYLE = {
    "mode": "stacked",
    "categories": list(YEARS),
    "series": [series.chart_dict() for series in FORECAST_SERIES],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": False,
    "show_value_labels": False,
    "show_gridlines": True,
    "major_gridline_color": QUIET_GRIDLINE,
    "major_gridline_width": 3175,
    "value_axis_format": "0",
    "value_label_format": "0",
    "value_label_size_pt": 10,
    "value_label_bold": False,
    "cat_label_size_pt": 10,
    "gap_width": 88,
    "seg_line_color": WHITE,
    "seg_line_width": 6350,
    "axis_line_color": BLACK,
    "axis_line_width": 6350,
    "value_axis_min": -350,
    "value_axis_max": 350,
    "value_axis_major_unit": 50,
    "plot_layout": {"x": 0.025, "y": 0.015, "w": 0.950, "h": 0.930},
    "cat_header": "Year",
}

CHARTS = [column_chart(**CHART_STYLE)]


# ════════════════════════════════════════════════════════════════════════════
# Validation helpers. They intentionally run at import time only if something is
# structurally wrong in the teaching data.
# ════════════════════════════════════════════════════════════════════════════
def _validate_semantics() -> None:
    if len(YEARS) != 25:
        raise ValueError("Status-quo fleet outlook chart must carry 25 annual categories.")
    if any(len(series.values_k_gt) != len(YEARS) for series in FORECAST_SERIES):
        raise ValueError("Every forecast series must align to YEARS.")
    if NET_TOTAL_LABELS_CHRONOLOGICAL != (
        "-161", "32", "206", "244", "265", "-10", "-84", "-123", "-77",
        "-14", "-99", "-115", "-110", "-221", "-264", "-208", "-119",
        "-267", "-312", "-276", "-91", "-76", "-48", "-70", "-153",
    ):
        raise ValueError("Manual net-total labels no longer match chart data.")


_validate_semantics()


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


# ════════════════════════════════════════════════════════════════════════════
# Paint functions. Order follows the source's effective stacking: contextual
# band, chart, manual axes/labels, chart title, chrome, legend, callouts, note,
# scenario/prelim.
# ════════════════════════════════════════════════════════════════════════════
def paint_orderbook_data_band(next_id) -> list[str]:
    """Left-side shaded band marking the years backed by orderbook data."""

    return [
        _textbox(
            next_id(),
            "OrderbookDataBand",
            ORDERBOOK_DATA_BAND,
            [
                paragraph(
                    [
                        run("Years with ", size=PT(10), italic=True, color=BLACK, font=FONT),
                        line_break(),
                        run("orderbook ", size=PT(10), italic=True, color=BLACK, font=FONT),
                        line_break(),
                        run("data", size=PT(10), italic=True, color=BLACK, font=FONT),
                    ],
                    line_spacing=100000,
                )
            ],
            fill=GRAY_1,
            line_color="none",
        )
    ]


def paint_native_chart(next_id) -> list[str]:
    """Native editable chart frame. All labels are handled by slide text."""

    x, y, w, h = CHART_FRAME.emu()
    return [
        graphic_frame(
            sp_id=next_id(),
            name="Chart",
            x=x,
            y=y,
            cx=w,
            cy=h,
            rId="rId2",
        )
    ]


def paint_manual_axes(next_id) -> list[str]:
    """Manual y-axis tick labels and 25 year ticks."""

    shapes: list[str] = []
    for tick in VALUE_AXIS_TICKS:
        shapes.append(
            _textbox(
                next_id(),
                "ValueAxisTickLabel",
                tick.box,
                [_one_line(tick.label, align="r")],
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

    for tick in YEAR_TICKS:
        shapes.append(
            _textbox(
                next_id(),
                "YearTickLabel",
                tick.box,
                [_one_line(tick.label, align="ctr")],
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


def paint_net_total_labels(next_id) -> list[str]:
    """Manual labels for net K-GT additions/removals by year."""

    shapes: list[str] = []
    for label in NET_TOTAL_LABELS:
        shapes.append(
            _textbox(
                next_id(),
                label.name,
                label.box,
                [_one_line(label.label, align="ctr")],
                fill=None,
                line_color="none",
                anchor=label.anchor,
                wrap="none",
                l_ins=17463,
                t_ins=0,
                r_ins=17463,
                b_ins=0,
            )
        )
    return shapes


def paint_chart_title(next_id) -> list[str]:
    """Long technical chart title lives outside the native chart."""

    return [
        _textbox(
            next_id(),
            "ChartTitle",
            CHART_TITLE,
            [
                paragraph(
                    [
                        run(
                            "Implied Retirements vs. Orderbook of US-Flagged, US-Built Vessels (K GT, High and Partial Autonomy Fit Vessel Archetypes) ",
                            size=PT(10),
                            bold=True,
                            color=BLACK,
                            font=FONT,
                        )
                    ],
                    mar_l=0,
                    indent=0,
                    line_spacing=100000,
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


def paint_chrome(next_id) -> list[str]:
    """House chrome for the status-quo scenario page."""

    return [
        "",
        "",
    ]


def paint_legend(next_id) -> list[str]:
    """Four-entry outside-chart legend: source order, not chart-series order."""

    shapes: list[str] = []
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


def paint_callouts(next_id) -> list[str]:
    """Net-total explanation, trend connector, and long-run average callout."""

    return [
        _textbox(
            next_id(),
            "NetTonnageCallout",
            NET_TOTAL_CALLOUT,
            [
                paragraph(
                    [run("Bar totals indicate net gross tonnage added (removed) each year", size=PT(10), italic=True, color=BLACK, font=FONT)],
                    line_spacing=100000,
                )
            ],
            fill=WHITE,
            line_color="none",
            prst="wedgeRectCallout",
            geom_adj={"adj1": "val -19106", "adj2": "val -3267"},
            anchor="ctr",
        ),
        connector(
            next_id(),
            "RetirementTrendConnector",
            IN(TREND_CONNECTOR[0]),
            IN(TREND_CONNECTOR[1]),
            IN(TREND_CONNECTOR[2]),
            IN(TREND_CONNECTOR[3]),
            color=TREND_LINE,
            width=12700,
            dashed=True,
        ),
        _textbox(
            next_id(),
            "AverageRetirementsCallout",
            AVG_RETIREMENT_CALLOUT,
            [
                paragraph(
                    [
                        run("‘31-’50 avg. retirements: ", size=PT(10), italic=True, color=BLACK, font=FONT),
                        run("~144K GT p.a.", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill=None,
            line_color="none",
            prst="wedgeRectCallout",
            geom_adj={"adj1": "val -19106", "adj2": "val -3267"},
            anchor="ctr",
        ),
    ]


def paint_source_note(next_id) -> list[str]:
    """Off-house footnote block preserved at the source position."""

    return [
        _textbox(
            next_id(),
            "SourceNote",
            SOURCE_NOTE,
            [
                paragraph(
                    [
                        run(
                            "Note: Service life assumptions – 40 years for Bulk, Container, General Cargo, and RORO, 35 years for Tankers, 30 years for PSVs, and 25 years for Crew/FSVs ",
                            size=PT(8),
                            color=BLACK,
                            font=FONT,
                        ),
                        line_break(),
                        run("Source: Clarksons (US fleet size and GT data)", size=PT(8), color=BLACK, font=FONT),
                    ],
                    line_spacing=100000,
                )
            ],
            fill=None,
            line_color="none",
        )
    ]


def paint_scenario_chrome(next_id) -> list[str]:
    """Scenario chip + Preliminary chip; both intentionally paint late."""

    return [
        "",
        _textbox(
            next_id(),
            "ScenarioChip",
            SCENARIO_CHIP,
            [_one_line("(1) Status Quo Scenario", size=PT(12), bold=True, align="ctr")],
            fill=SCENARIO_BLUE,
            line_color=BLACK,
            anchor="ctr",
        ),
    ]


def _body() -> str:
    shapes: list[str] = []
    ids = iter(range(100, 2000))
    next_id = lambda: next(ids)  # noqa: E731 - compact sequential shape ids

    shapes.extend(paint_orderbook_data_band(next_id))
    shapes.extend(paint_native_chart(next_id))
    shapes.extend(paint_manual_axes(next_id))
    shapes.extend(paint_net_total_labels(next_id))
    shapes.extend(paint_chart_title(next_id))
    shapes.extend(paint_chrome(next_id))
    shapes.extend(paint_legend(next_id))
    shapes.extend(paint_callouts(next_id))
    shapes.extend(paint_source_note(next_id))
    shapes.extend(paint_scenario_chrome(next_id))
    return "".join(shapes)


CHROME = Chrome(
    section="US-Built Ship Demand",
    topic="Status Quo",
    title="Status Quo Fleet Outlook",
    takeaway="Following completion of orderbook deliveries, fleet is expected to shrink by ~144K GT p.a. ’31-’50 (<2% of 10M GT target).",
)


def render() -> str:
    return body_slide(CHROME, _body())
