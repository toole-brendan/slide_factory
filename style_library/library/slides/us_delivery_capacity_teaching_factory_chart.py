"""Teaching exemplar: US delivery-capacity forecast slide.

ROLE
  scenario_forecast / capacity_ramp

USE WHEN
  A slide needs one dominant forecast chart, manually placed chart labels, a
  right-hand assumptions rail, a bottom milestone strip, and a few callouts.

TEACHES
  - fully declarative native charting with column_chart(mode="stacked")
  - factory-level chart style instead of a bundled chart template
  - manual year ticks and delivery-total labels over a native chart
  - no-fill assumptions rail beside a dominant exhibit
  - empirical text-fit precedent for dense 10pt assumption bullets
  - bottom summary strip of repeated ellipse badges
  - callouts layered on top of chart + summary content

TEXT-FIT PRECEDENT
  assumptions_rail:
    geometry: 3.674in wide x 4.365in high
    type: Arial 10pt, black, 100% line spacing
    content: 3 mini-heads + 9 bullets + one trailing blank bullet
    copy_when: the chart carries the quantitative proof and the rail explains
               assumptions/method, not standalone findings

SOURCE NOTE
  Teaching rewrite of the source-faithful `us_delivery_capacity.py` module.
  This version intentionally replaces the source chart-template wrapper
  with a native `column_chart(mode="stacked", ...)` spec. The surrounding slide
  contract (`LAYOUT`, `CHARTS`, `_body()`, `render()`), coordinates, labels,
  assumptions rail, summary strip, and callouts are preserved; the chart is now
  authored from explicit categories, series names, colors, axis settings, and
  plot layout.

FIDELITY NOTE
  This is a practical factory rebuild, not a byte-identical chart-template port.
  It preserves the visible chart semantics and major styling controls (stacked
  columns, colors, hidden category labels, fixed value axis, manual plot-area
  layout, no native legend, no segment outlines, first-three in-chart labels),
  but PowerPoint may render tiny differences in native label placement and chart
  XML ordering versus the source chart part.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    line_break,
    table,
    trow,
    tcell_rich,
    tpara,
    trun,
    breadcrumb,
    title_placeholder,
    prelim_chip,
)
from deck_core.charts import graphic_frame, column_chart
from deck_core.style import IN, PT, BLACK, WHITE, FONT

LAYOUT = "slideLayout4"

# Fully declarative chart spec. The chart is a native editable PowerPoint stacked
# column chart; no chart XML template and no external workbook are bundled.
CHART_CATEGORIES: tuple[str, ...] = tuple(str(year) for year in range(2026, 2051))

# Series are ordered bottom-to-top in the stacked columns. The manual legend on
# the slide is intentionally displayed top-to-bottom in the reverse order.
SHIPYARD_CAPACITY_SERIES: tuple[dict, ...] = (
    {
        "name": "Saronic",
        "color": "007770",
        "values": [1, 2, 2, 7, 14, 23, 40, 56, 85, 97, 111, 110, 110, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125],
        # Source style exception: 2026-2028 pre-Port-Alpha capacity is drawn
        # in Hanwha Philly blue; the layer turns Saronic green from 2029 onward.
        "data_point_colors": ["364D6E", "364D6E", "364D6E"] + ["007770"] * 22,
        # Every bar-top total (incl. the first three: 1/2/2) is overlaid as a manual
        # text label ABOVE the bar via DELIVERY_TOTAL_LABELS. A native stacked-bar
        # label can only sit ctr/inEnd/inBase (i.e. ON the column), never above, so
        # we hide the native labels here and place all totals as slide text boxes.
        "hide_labels": True,
    },
    {
        "name": "Hanwha Philly",
        "color": "364D6E",
        "values": [None, None, None, 5, 6, 6, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20],
        "hide_labels": True,
    },
    {
        "name": "Hanwha 2nd Yard",
        "color": "4C6C9C",
        "values": [None, None, None, None, None, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5],
        # Source style exception: the 2031 point is Tampa Ship light blue.
        "data_point_colors": ["4C6C9C"] * 5 + ["C3CFE1"] + ["4C6C9C"] * 19,
        "hide_labels": True,
    },
    {
        "name": "New Entrant (e.g., HD Hyundai)",
        "color": "6F8DB9",
        "values": [None, None, None, None, None, None, 1, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        "hide_labels": True,
    },
    {
        "name": "Bollinger",
        "color": "9DB1CF",
        "values": [None, None, None, None, None, None, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        "hide_labels": True,
    },
    {
        "name": "Tampa Ship (HD HHI)",
        "color": "C3CFE1",
        "values": [None, None, None, None, None, None, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        "hide_labels": True,
    },
    {
        "name": "GD NASSCO (SHI)",
        "color": "808080",
        "values": [None, None, None, None, None, None, None, None, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        "hide_labels": True,
    },
)

# Kept as a readable data mirror for agents/tools that expect the converted-slide
# data-dict shape. CHARTS below uses the same values through column_chart().
_CHART0_DATA = {
    "categories": CHART_CATEGORIES,
    "series": SHIPYARD_CAPACITY_SERIES,
}

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(CHART_CATEGORIES),
    "series": [dict(series) for series in SHIPYARD_CAPACITY_SERIES],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": True,
    "show_gridlines": False,
    "show_value_labels": True,
    "value_axis_format": '#,##0;"-"#,##0',
    "value_label_format": '#,##0;"-"#,##0',
    "value_label_size_pt": 10,
    "value_label_bold": False,
    "cat_label_size_pt": 10,
    "gap_width": 130,
    "bar_overlap": 100,
    "seg_line_color": None,
    "axis_line_color": BLACK,
    "axis_line_width": 9525,
    "value_axis_min": 0,
    "value_axis_max": 180,
    "value_axis_major_unit": 20,
    "plot_layout": {
        "x": 0.053430713050163364,
        "y": 0.06807286673058485,
        "w": 0.9365750528541226,
        "h": 0.8638542665388304,
    },
    "cat_header": "Year",
}

CHARTS = [column_chart(**CHART_STYLE)]


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: these are comments the module can expose programmatically.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "scenario_forecast",
    "use_when": (
        "Use for a dominant multi-year capacity forecast with a right assumptions "
        "rail, a manual chart-label system, bottom milestone badges, and a few "
        "callouts."
    ),
    "teaches": [
        "fully declarative column_chart stacked chart",
        "inline chart categories / series / colors / axis scale",
        "manual year ticks",
        "manual data labels",
        "shipyard legend",
        "dense no-fill assumptions rail",
        "summary ellipse badge strip",
        "white callouts over chart/summary content",
    ],
}

TEXT_FIT = {
    "assumptions_rail": {
        "box_in": (3.674, 4.365),
        "font_pt": 10,
        "content": "3 mini-heads + 9 bullets + one trailing blank bullet",
        "note": (
            "This is a high-density rail that works because the chart is the main "
            "evidence. Do not turn it into independent narrative prose."
        ),
    },
    "source_note": {
        "box_in": (12.367, 0.322),
        "font_pt": 8,
        "content": "two source/note lines via line_break()",
    },
    "summary_badges": {
        "box_in": (0.602, 0.256),
        "font_pt": 10,
        "content": "short numeric tokens only: <=4 visible chars is safest",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Small semantic geometry/data records.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    """Geometry in inches; converted to EMU at the last possible moment."""

    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class TextZone:
    name: str
    box: Box
    font_pt: float
    fit_note: str


@dataclass(frozen=True)
class YearTick:
    x: float
    label: str


@dataclass(frozen=True)
class DeliveryTotalLabel:
    box: Box
    label: str


@dataclass(frozen=True)
class LegendEntry:
    label: str
    fill: str
    swatch: Box
    caption: Box


@dataclass(frozen=True)
class SummaryBadge:
    row: str
    box: Box
    label: str


@dataclass(frozen=True)
class AssumptionSection:
    heading: str
    bullets: tuple[str, ...]


@dataclass(frozen=True)
class Callout:
    name: str
    box: Box
    text: str
    fill: str = WHITE
    line_color: str = BLACK
    prst: str = "rect"
    geom_adj: dict[str, str] | None = None
    italic: bool = False


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Layout zones: the slide reads as chart + right rail + bottom summary strip.
# ════════════════════════════════════════════════════════════════════════════
CHART_FRAME = Box(0.429, 1.620, 9.033, 3.622)
CHART_TITLE = TextZone(
    name="ChartTitle",
    box=Box(0.542, 1.505, 5.773, 0.167),
    font_pt=10,
    fit_note="External chart title; keep one line, no wrap.",
)

YEAR_TICK_ZONE = TextZone(
    name="YearTick",
    box=Box(0.0, 5.042, 0.167, 0.306),
    font_pt=10,
    fit_note="25 tight, right-aligned year labels; never use long labels here.",
)
DELIVERY_TOTAL_ZONE = TextZone(
    name="DeliveryTotalLabel",
    box=Box(0.0, 0.0, 0.0, 0.167),
    font_pt=10,
    fit_note="One short value riding each bar; width expands from 0.191in to 0.267in for 3 digits.",
)

LEGEND_SWATCH_W = 0.196
LEGEND_SWATCH_H = 0.146
SHIPYARD_LABEL_H = 0.167

ASSUMPTIONS_HEADER = TextZone(
    name="AssumptionsRailHeader",
    box=Box(9.439, 1.431, 3.674, 0.300),
    font_pt=10,
    fit_note="One-line native-table header with black bottom rule.",
)
ASSUMPTIONS_RAIL = TextZone(
    name="AssumptionsRailBody",
    box=Box(9.439, 1.742, 3.674, 4.365),
    font_pt=10,
    fit_note="3 section heads + 9 bullets; this is the key text-fit precedent.",
)

SOURCE_NOTE = TextZone(
    name="SourceNote",
    box=Box(0.495, 6.675, 12.367, 0.322),
    font_pt=8,
    fit_note="Off-house source/note line kept with source geometry; two lines max.",
)

SUMMARY_BADGE_W = 0.602
SUMMARY_BADGE_H = 0.256
SUMMARY_LABEL_W = 2.000
SUMMARY_LABEL_H = 0.340

SCOPE_CHIP = TextZone(
    name="ScopeChip",
    box=Box(8.069, 0.174, 2.977, 0.217),
    font_pt=12,
    fit_note="Short scenario label, outlined, no fill.",
)


# ════════════════════════════════════════════════════════════════════════════
# Repeated chart labels and legend content.
# ════════════════════════════════════════════════════════════════════════════
YEAR_TICKS: tuple[YearTick, ...] = (
    YearTick(0.997, "2026"),
    YearTick(1.335, "2027"),
    YearTick(1.674, "2028"),
    YearTick(2.012, "2029"),
    YearTick(2.351, "2030"),
    YearTick(2.689, "2031"),
    YearTick(3.026, "2032"),
    YearTick(3.365, "2033"),
    YearTick(3.703, "2034"),
    YearTick(4.042, "2035"),
    YearTick(4.380, "2036"),
    YearTick(4.719, "2037"),
    YearTick(5.057, "2038"),
    YearTick(5.396, "2039"),
    YearTick(5.734, "2040"),
    YearTick(6.073, "2041"),
    YearTick(6.411, "2042"),
    YearTick(6.750, "2043"),
    YearTick(7.087, "2044"),
    YearTick(7.425, "2045"),
    YearTick(7.764, "2046"),
    YearTick(8.102, "2047"),
    YearTick(8.441, "2048"),
    YearTick(8.780, "2049"),
    YearTick(9.118, "2050"),
)

DELIVERY_TOTAL_LABELS: tuple[DeliveryTotalLabel, ...] = (
    # 2026-2028: the tiny Saronic-only bars (1/2/2). Native stacked labels can't
    # sit above a column, so these are manual text boxes like the rest, placed at
    # bar_top - 0.195in (the same offset the later totals use), the x-spine
    # continuing 0.339in/yr back from the 2029 "12" label.
    DeliveryTotalLabel(Box(0.983, 4.783, 0.191, 0.167), "1"),
    DeliveryTotalLabel(Box(1.322, 4.766, 0.191, 0.167), "2"),
    DeliveryTotalLabel(Box(1.661, 4.766, 0.191, 0.167), "2"),
    DeliveryTotalLabel(Box(2.000, 4.592, 0.191, 0.167), "12"),
    DeliveryTotalLabel(Box(2.339, 4.453, 0.191, 0.167), "20"),
    DeliveryTotalLabel(Box(2.677, 4.280, 0.191, 0.167), "30"),
    DeliveryTotalLabel(Box(3.014, 3.931, 0.191, 0.167), "50"),
    DeliveryTotalLabel(Box(3.352, 3.601, 0.191, 0.167), "69"),
    DeliveryTotalLabel(Box(3.653, 3.010, 0.267, 0.167), "103"),
    DeliveryTotalLabel(Box(3.991, 2.767, 0.267, 0.167), "117"),
    DeliveryTotalLabel(Box(4.330, 2.490, 0.267, 0.167), "133"),
    DeliveryTotalLabel(Box(4.668, 2.418, 0.267, 0.167), "137"),
    DeliveryTotalLabel(Box(5.007, 2.384, 0.267, 0.167), "139"),
    DeliveryTotalLabel(Box(5.345, 2.089, 0.267, 0.167), "156"),
    DeliveryTotalLabel(Box(5.684, 2.019, 0.267, 0.167), "160"),
    DeliveryTotalLabel(Box(6.023, 2.002, 0.267, 0.167), "161"),
    DeliveryTotalLabel(Box(6.361, 1.984, 0.267, 0.167), "162"),
    DeliveryTotalLabel(Box(6.700, 1.950, 0.267, 0.167), "164"),
    DeliveryTotalLabel(Box(7.036, 1.932, 0.267, 0.167), "165"),
    DeliveryTotalLabel(Box(7.375, 1.915, 0.267, 0.167), "166"),
    DeliveryTotalLabel(Box(7.714, 1.915, 0.267, 0.167), "166"),
    DeliveryTotalLabel(Box(8.052, 1.915, 0.267, 0.167), "166"),
    DeliveryTotalLabel(Box(8.391, 1.915, 0.267, 0.167), "166"),
    DeliveryTotalLabel(Box(8.729, 1.915, 0.267, 0.167), "166"),
    DeliveryTotalLabel(Box(9.068, 1.915, 0.267, 0.167), "166"),
)

SHIPYARD_LEGEND: tuple[LegendEntry, ...] = (
    LegendEntry("GD NASSCO (SHI)", "808080", Box(0.967, 1.927, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(1.219, 1.922, 1.194, SHIPYARD_LABEL_H)),
    LegendEntry("Tampa Ship (HD HHI)", "C3CFE1", Box(0.967, 2.149, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(1.219, 2.144, 1.356, SHIPYARD_LABEL_H)),
    LegendEntry("Bollinger", "9DB1CF", Box(0.967, 2.372, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(1.219, 2.366, 0.576, SHIPYARD_LABEL_H)),
    LegendEntry("New Entrant (e.g., HD Hyundai)", "6F8DB9", Box(0.967, 2.594, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(1.219, 2.589, 1.944, SHIPYARD_LABEL_H)),
    LegendEntry("Hanwha 2nd Yard", "4C6C9C", Box(0.967, 2.816, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(1.219, 2.811, 1.104, SHIPYARD_LABEL_H)),
    LegendEntry("Hanwha Philly", "364D6E", Box(0.967, 3.038, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(1.219, 3.033, 0.877, SHIPYARD_LABEL_H)),
    LegendEntry("Saronic", "007770", Box(0.967, 3.260, LEGEND_SWATCH_W, LEGEND_SWATCH_H), Box(1.219, 3.255, 0.469, SHIPYARD_LABEL_H)),
)


# ════════════════════════════════════════════════════════════════════════════
# Assumptions rail: this is the empirical text-fit guide for this role.
# ════════════════════════════════════════════════════════════════════════════
ASSUMPTION_SECTIONS: tuple[AssumptionSection, ...] = (
    AssumptionSection(
        "Total Delivery Capacity",
        (
            "US ramps to 8.3M GT by early 2050s based on Investor Presentation target (Jan ’26)",
            "Avg. GT stays ~50K / ship, in line with recent US built containerships; ~10K above 10-yr. avg. for commercially viable, ocean ships",
        ),
    ),
    AssumptionSection(
        "Saronic Capacity",
        (
            "Port Alpha ramps from 7 deliveries in 2029 to 125 delivery capacity by late ’30s to align with IP assertion of achieving 10M GT of US capacity",
        ),
    ),
    AssumptionSection(
        "Competitor Capacities",
        (
            "Hanwha Philly achieves 10 deliveries/yr. by mid-2030s and 20 deliveries/yr. by mid-2040s, in line with stated goals",
            "Hanwha purchase 2nd yard in the US, ramping to 5 deliveries/yr. by mid-2040s",
            "HD Hyundai potentially enters US market, purchasing a Gulf Coast yard, ramping production through 2030s",
            "Tampa Ship begins producing commercial vessels in early 2030s, enabled by HD HII partnership",
            "Bollinger begins producing commercial vessels in early-to-mid 2030s after completion of USCG vessels",
            "GD NASSCO begins delivering commercial vessels after completion of Navy T-AO in early-to-mid 2030s",
        ),
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Bottom summary strip: three rows x five milestones.
# ════════════════════════════════════════════════════════════════════════════
SUMMARY_BADGES: tuple[SummaryBadge, ...] = (
    SummaryBadge("total_us_gt", Box(2.128, 5.889, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "1.1M"),
    SummaryBadge("total_us_gt", Box(3.824, 5.889, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "6.0M"),
    SummaryBadge("total_us_gt", Box(5.517, 5.889, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "8.1M"),
    SummaryBadge("total_us_gt", Box(7.208, 5.889, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "8.4M"),
    SummaryBadge("total_us_gt", Box(8.900, 5.889, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "8.4M"),
    SummaryBadge("oceangoing_gt", Box(2.128, 5.492, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "1.0M"),
    SummaryBadge("oceangoing_gt", Box(3.824, 5.492, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "5.9M"),
    SummaryBadge("oceangoing_gt", Box(5.517, 5.492, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "8.0M"),
    SummaryBadge("oceangoing_gt", Box(7.208, 5.492, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "8.3M"),
    SummaryBadge("oceangoing_gt", Box(8.900, 5.492, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "8.3M"),
    SummaryBadge("port_alpha_share", Box(2.128, 6.285, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "70%"),
    SummaryBadge("port_alpha_share", Box(3.824, 6.285, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "83%"),
    SummaryBadge("port_alpha_share", Box(5.517, 6.285, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "78%"),
    SummaryBadge("port_alpha_share", Box(7.208, 6.285, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "75%"),
    SummaryBadge("port_alpha_share", Box(8.900, 6.285, SUMMARY_BADGE_W, SUMMARY_BADGE_H), "75%"),
)


# ════════════════════════════════════════════════════════════════════════════
# Callouts: top-layer annotations. These paint after the summary strip.
# ════════════════════════════════════════════════════════════════════════════
CALLOUTS: tuple[Callout, ...] = (
    Callout(
        name="NonOceangoingStableGTCallout",
        box=Box(9.990, 5.889, 2.797, 1.040),
        text=(
            "Est. ~100K GT for naval, USCG, offshore, and other vessels remains "
            "relatively stable through forecast; implied amount based on current "
            "orderbook for non-oceangoing commercial and assumed defense/national "
            "security production"
        ),
        line_color="121415",
        prst="wedgeRectCallout",
        geom_adj={"adj1": "val -62578", "adj2": "val -35925"},
    ),
    Callout(
        name="OrderbookCapacityCallout",
        box=Box(0.965, 3.546, 1.712, 0.699),
        text="Implied delivery capacity based on orderbook; excludes idle / underutilized yards",
        line_color="121415",
        prst="wedgeRectCallout",
        geom_adj={"adj1": "val -21817", "adj2": "val 120159"},
        italic=True,
    ),
    Callout(
        name="SaronicRampCallout",
        box=Box(5.224, 4.280, 3.993, 0.628),
        text=(
            "Saronic capacity assumes Port Alpha ramps from 7 delivery capacity in "
            "2029 to 125 deliveries by late 2030s to align with IP assertion of "
            "achieving 10M GT of US shipbuilding capacity "
        ),
        line_color=BLACK,
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: kept local so the module is ready against today's deck_core.
# Move this to deck_core.table_kit later if/when you centralize the authoring API.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def border_dict(**edges):
    """Only draw the sides passed as L/R/T/B; omitted sides render as no-fill."""

    return {k: v for k, v in edges.items() if v is not None} or None


def rich_cell(
    paras,
    *,
    fill=None,
    anchor="ctr",
    span=1,
    rowspan=1,
    l_ins=45_720,
    r_ins=45_720,
    t_ins=45_720,
    b_ins=45_720,
    **edges,
):
    """tcell_rich wrapper: content first, cell mechanics second."""

    return tcell_rich(
        paras,
        fill=fill,
        grid_span=span,
        row_span=rowspan,
        anchor=anchor,
        l_ins=l_ins,
        r_ins=r_ins,
        t_ins=t_ins,
        b_ins=b_ins,
        borders=border_dict(**edges),
    )


# ════════════════════════════════════════════════════════════════════════════
# Text helpers: keep the main paint functions at slide-intent level.
# ════════════════════════════════════════════════════════════════════════════
def _r(text: str, *, size_pt: float = 10, bold: bool = False, italic: bool = False, color: str = BLACK) -> str:
    return run(text, size=PT(size_pt), bold=bold or None, italic=italic or None, color=color, font=FONT)


def _tight_para(runs, *, align=None, bullet=False, italic=False):
    """100% line-spacing paragraph used by manual chart labels and this source slide."""

    return paragraph(
        runs,
        align=align,
        mar_l=0 if not bullet else 171_450,
        indent=0 if not bullet else -171_450,
        line_spacing=100_000,
        bullet=bullet,
    )


def _no_fill_label(ids: ShapeIds, name: str, box: Box, text: str, *, align="ctr", anchor="ctr", bold=False, italic=False) -> str:
    return text_box(
        ids.next(),
        name,
        *box.emu(),
        [_tight_para([_r(text, bold=bold, italic=italic)], align=align)],
        fill=None,
        line_color="none",
        anchor=anchor,
        wrap="none",
        l_ins=0,
        t_ins=0,
        r_ins=0,
        b_ins=0,
    )


def _assumptions_paragraphs() -> list[str]:
    paras: list[str] = []
    for section in ASSUMPTION_SECTIONS:
        paras.append(
            paragraph(
                [_r(section.heading, bold=True, italic=True)],
                line_spacing=100_000,
            )
        )
        for bullet in section.bullets:
            paras.append(
                paragraph(
                    [_r(bullet)],
                    mar_l=171_450,
                    indent=-171_450,
                    line_spacing=100_000,
                    bullet=True,
                )
            )
    # Source slide carries one trailing blank bullet; keep it because it affects fit.
    paras.append(paragraph([], mar_l=171_450, indent=-171_450, line_spacing=100_000, bullet=True))
    return paras


def _source_note_paragraph() -> str:
    """Two-line note/source paragraph; kept as runs for the explicit line break."""

    note = [
        _r("Note: (1) Assumes avg. 50K GT per newbuild (~13K higher than current fleet avg.); 10M GT target may be achieved with 140-160 deliveries / year with 60K-70K GT per newbuild ", size_pt=8),
        line_break(),
        _r("Source: Saronic IP (Jan ’26); ", size_pt=8),
        _r("Hanwha Philly", size_pt=8),
        _r("; ", size_pt=8),
        _r("Breaking Defense (Hanwha 2", size_pt=8),
        _r("nd", size_pt=8),
        _r(" Yard)", size_pt=8),
        _r("; ", size_pt=8),
        _r("Conrad Shipyard", size_pt=8),
        _r("; ", size_pt=8),
        _r("HD Hyundai (Tampa Ship)", size_pt=8),
        _r("; ", size_pt=8),
        _r("GD NASSCO", size_pt=8),
    ]
    return paragraph(note, line_spacing=100_000)


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def paint_chart(out: list[str], ids: ShapeIds) -> None:
    out.append(
        graphic_frame(
            sp_id=ids.next(),
            name="DeliveryCapacityChart",
            x=IN(CHART_FRAME.x),
            y=IN(CHART_FRAME.y),
            cx=IN(CHART_FRAME.w),
            cy=IN(CHART_FRAME.h),
            rId="rId2",
        )
    )


def paint_chart_manual_labels(out: list[str], ids: ShapeIds) -> None:
    # 25 year ticks under the chart. These labels are intentionally text boxes,
    # not native chart labels, because the source chart template owns the style.
    for tick in YEAR_TICKS:
        out.append(
            text_box(
                ids.next(),
                "ChartYearTick",
                IN(tick.x),
                IN(YEAR_TICK_ZONE.box.y),
                IN(YEAR_TICK_ZONE.box.w),
                IN(YEAR_TICK_ZONE.box.h),
                [_tight_para([_r(tick.label)], align="r")],
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

    for label in DELIVERY_TOTAL_LABELS:
        out.append(
            text_box(
                ids.next(),
                "DeliveryTotalLabel",
                *label.box.emu(),
                [_tight_para([_r(label.label)], align="ctr")],
                fill=None,
                line_color="none",
                anchor="b",
                wrap="none",
                l_ins=17_463,
                t_ins=0,
                r_ins=17_463,
                b_ins=0,
            )
        )

    out.append(
        text_box(
            ids.next(),
            CHART_TITLE.name,
            *CHART_TITLE.box.emu(),
            [_tight_para([_r("US-Built Oceangoing Commercial Delivery Capacity by Shipyard  (# potential deliveries)", bold=True)])],
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


def paint_shipyard_legend(out: list[str], ids: ShapeIds) -> None:
    # A two-pass legend mirrors the original paint order: all swatches, then labels.
    for entry in SHIPYARD_LEGEND:
        out.append(
            text_box(
                ids.next(),
                "ShipyardLegendSwatch",
                *entry.swatch.emu(),
                [paragraph([], align="ctr", line_spacing=100_000)],
                fill=entry.fill,
                line_color="none",
                anchor="ctr",
            )
        )

    for entry in SHIPYARD_LEGEND:
        out.append(
            text_box(
                ids.next(),
                "ShipyardLegendLabel",
                *entry.caption.emu(),
                [_tight_para([_r(entry.label)], align=None)],
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


def paint_chrome_and_source(out: list[str], ids: ShapeIds) -> None:
    out.append(breadcrumb("US-Built Ship Demand", "With SHIPS Act"))
    out.append(
        title_placeholder(
            "US Delivery Capacity",
            "Expansion largely driven by Saronic; Competitor growth enabled by ownership / partnerships with major ROK shipbuilders and completion of USN/USCG activity.",
        )
    )
    out.append(
        text_box(
            ids.next(),
            SOURCE_NOTE.name,
            *SOURCE_NOTE.box.emu(),
            [_source_note_paragraph()],
            fill=None,
            line_color="none",
        )
    )


def paint_assumptions_rail(out: list[str], ids: ShapeIds) -> None:
    # Body first, header second: the header rule paints on top of the rail.
    out.append(
        text_box(
            ids.next(),
            ASSUMPTIONS_RAIL.name,
            *ASSUMPTIONS_RAIL.box.emu(),
            _assumptions_paragraphs(),
            fill=None,
            line_color="none",
        )
    )

    out.append(
        table(
            ids.next(),
            ASSUMPTIONS_HEADER.name,
            *ASSUMPTIONS_HEADER.box.emu(),
            col_widths=[IN(ASSUMPTIONS_HEADER.box.w)],
            rows=[
                trow(
                    [
                        rich_cell(
                            [
                                tpara(
                                    [trun("Inputs & Assumptions ", size=PT(10), bold=True, color=BLACK, font=FONT)],
                                    mar_l=0,
                                    indent=0,
                                )
                            ],
                            l_ins=41_564,
                            r_ins=41_564,
                            T=edge(WHITE),
                            B=edge(BLACK),
                        )
                    ],
                    h=IN(0.300),
                )
            ],
        )
    )


def paint_summary_strip(out: list[str], ids: ShapeIds) -> None:
    # Total US GT row label paints first in the source, followed by all badges.
    out.append(
        text_box(
            ids.next(),
            "SummaryRowLabelTotalUSGT",
            IN(0.113),
            IN(5.846),
            IN(SUMMARY_LABEL_W),
            IN(SUMMARY_LABEL_H),
            [
                paragraph(
                    [
                        _r("Total US GT ", bold=True),
                        _r("(incl. non-ocean/commercial)", italic=True),
                        _r(":", bold=True),
                    ],
                    line_spacing=100_000,
                )
            ],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )

    for badge in SUMMARY_BADGES:
        out.append(
            text_box(
                ids.next(),
                f"SummaryBadge_{badge.row}",
                *badge.box.emu(),
                [paragraph([_r(badge.label)], align="ctr", line_spacing=100_000)],
                fill=None,
                line_color=BLACK,
                line_width=6_350,
                prst="ellipse",
                anchor="ctr",
                l_ins=0,
                r_ins=0,
            )
        )

    out.append(
        text_box(
            ids.next(),
            "SummaryRowLabelOceangoingGT",
            IN(0.113),
            IN(5.450),
            IN(SUMMARY_LABEL_W),
            IN(SUMMARY_LABEL_H),
            [
                paragraph(
                    [
                        _r("Oceangoing commercial GT", bold=True),
                        _r("1", bold=True),
                        _r(":", bold=True),
                    ],
                    line_spacing=100_000,
                )
            ],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )

    out.append(
        text_box(
            ids.next(),
            "SummaryRowLabelPortAlphaShare",
            IN(0.113),
            IN(6.243),
            IN(SUMMARY_LABEL_W),
            IN(SUMMARY_LABEL_H),
            [paragraph([_r("% oceangoing commercial attributable to Port Alpha:", bold=True, italic=True)], line_spacing=100_000)],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )


def paint_callouts(out: list[str], ids: ShapeIds) -> None:
    for callout in CALLOUTS:
        out.append(
            text_box(
                ids.next(),
                callout.name,
                *callout.box.emu(),
                [paragraph([_r(callout.text, italic=callout.italic)], align="ctr", line_spacing=100_000)],
                fill=callout.fill,
                line_color=callout.line_color,
                prst=callout.prst,
                geom_adj=callout.geom_adj,
                anchor="ctr",
            )
        )


def paint_scope_chip(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            SCOPE_CHIP.name,
            *SCOPE_CHIP.box.emu(),
            [paragraph([_r("All Scenarios", size_pt=12, bold=True)], align="ctr", line_spacing=100_000)],
            fill=None,
            line_color=BLACK,
            anchor="ctr",
        )
    )
    out.append(prelim_chip())


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # Paint order matters in PowerPoint OOXML: later elements sit on top.
    paint_chart(out, ids)
    paint_chart_manual_labels(out, ids)
    paint_shipyard_legend(out, ids)
    paint_chrome_and_source(out, ids)
    paint_assumptions_rail(out, ids)
    paint_summary_strip(out, ids)
    paint_callouts(out, ids)
    paint_scope_chip(out, ids)

    return "".join(out)


def render() -> str:
    return slide(_body())
