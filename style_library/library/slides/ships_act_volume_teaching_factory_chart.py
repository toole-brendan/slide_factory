"""Teaching exemplar: SHIPS Act volume forecast slide.

ROLE
  scenario_forecast / policy_constrained_demand_ramp

USE WHEN
  A slide needs one dominant time-series demand exhibit, manual chart annotations,
  a small in-chart legend, capacity-phase reference rules, bottom milestone badges,
  and a few caveat callouts tied to legislation or funding assumptions.

TEACHES
  - data-over-template chart authoring with styled_chart() for a styled stacked-area exhibit
  - keeping chart data readable while preserving an existing chart XML template
  - manual year ticks and capacity reference labels over a chart frame
  - layered demand-band legend: panel, solid swatches, hatch swatch, labels, and
    confidence scale
  - repeated connector rules for capacity phases and demand-band thresholds
  - bottom milestone badge strip for scenario percentages
  - speech-bubble caveats layered over chart and badge content

TEXT-FIT PRECEDENT
  scenario_chip:
    geometry: 2.977in wide x 0.218in high
    type: Arial 12pt bold, centered
    content: one short scenario label
    copy_when: a slide needs a top-right scenario tag separate from the chrome
  chart_year_ticks:
    geometry: 0.167in wide x 0.306in high each
    type: Arial 10pt, right-aligned, no-wrap, zero insets
    content: 25 year labels from 2026-2050
    copy_when: a source chart hides native category labels and labels are
               overlaid manually for exact placement
  demand_band_legend:
    geometry: 3.910in wide x 1.191in high white panel
    type: Arial 10pt labels + 0.196in x 0.146in swatches
    content: five demand-band captions, one hatched swatch, and confidence scale
    copy_when: a legend must sit inside a chart frame without using the chart's
               native legend
  bottom_badges:
    geometry: 0.451-0.452in wide x 0.256in high each
    type: Arial 10pt, centered, ellipse outline
    content: five percentage labels
    copy_when: a forecast scenario needs compact milestone percentages below the
               chart

SOURCE NOTE
  Teaching rewrite of the source-faithful `ships_act_volume.py` module. The
  styled chart remains a data-over-template chart because the source part is a
  stacked-area chart with a hatched series and manual annotations; the current
  factory chart primitives do not expose a first-class area-chart rebuild. The
  attached `slide51_chart30.xml` and `slide51_chart30.xlsb` are read from `_src/`
  when present, with a same-folder fallback for standalone review.

FIDELITY NOTE
  This is an authoring/readability refactor, not a visual redesign. Geometry,
  shape names, shape ids, chart frame, chart data, annotation order, connector
  rules, legend swatches, caveats, chrome, and paint order are preserved from the
  hand-polished source module. The visible chart style remains owned by the
  source chart template; the values live in the `DEMAND_BAND_SERIES` records.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    connector,
    breadcrumb,
    title_placeholder,
    prelim_chip,
    sources_line,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, WHITE, DK, FONT

LAYOUT = "slideLayout4"


# ════════════════════════════════════════════════════════════════════════════
# Chart assets: prefer the production `_src/` location; accept colocated files
# for standalone teaching/review sessions where the chart XML/XLSB were uploaded
# next to this module.
# ════════════════════════════════════════════════════════════════════════════
_SLIDE_DIR = Path(__file__).parent
_SRC = _SLIDE_DIR / "_src"


def _chart_asset(name: str) -> Path:
    for candidate in (_SRC / name, _SLIDE_DIR / name):
        if candidate.exists():
            return candidate
    # Raise from the production path so the missing-file message names the
    # expected deck layout, but the fallback above keeps local review simple.
    return _SRC / name


_CHART0_TPL = _chart_asset("slide51_chart30.xml").read_text(encoding="utf-8")
_XLSB0 = _chart_asset("slide51_chart30.xlsb").read_bytes()


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: slide-level guidance AI authors can inspect.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "scenario_forecast_policy_constrained_demand",
    "use_when": (
        "Use for a policy-constrained demand forecast where a styled chart is "
        "the evidence surface and manual annotations explain capacity phases, "
        "confidence, and scenario contingencies."
    ),
    "teaches": [
        "styled_chart data-over-template charting",
        "external chart assets with local fallback",
        "semantic chart-series records",
        "manual year ticks and axis captions",
        "capacity-phase rule annotations",
        "in-chart demand-band legend",
        "confidence scale labels",
        "bottom scenario percentage badges",
        "legislative/funding caveat callouts",
    ],
}

TEXT_FIT = {
    "scenario_chip": {
        "box_in": (2.977, 0.218),
        "font_pt": 12,
        "content": "one centered scenario label",
        "note": "Keep scenario labels short; this chip is intentionally thin.",
    },
    "chart_year_ticks": {
        "box_in": (0.167, 0.306),
        "font_pt": 10,
        "content": "25 four-digit year labels, rotated by placement not text rotation",
        "note": "Use no-wrap and zero insets; labels are placed manually, not by the chart.",
    },
    "demand_band_legend": {
        "box_in": (3.910, 1.191),
        "font_pt": 10,
        "content": "five captions + four solid swatches + one hatched swatch + confidence scale",
        "note": "The white panel makes dense legend content readable over the chart.",
    },
    "bottom_badges": {
        "box_in": (0.451, 0.256),
        "font_pt": 10,
        "content": "short percentage labels only",
        "note": "The source uses ellipses as compact milestone badges; avoid long text here.",
    },
    "source_line": {
        "box_in": "house sources_line() placeholder",
        "font_pt": 8,
        "content": "long single Note/Source string",
        "note": "The source is folded into the house source line rather than a custom body text box.",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Small semantic records: geometry, chart data, annotation specs.
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
class DemandBandSeries:
    """One source chart series; `label`/`fill_note` document the template style."""

    label: str
    values: tuple[int | None, ...]
    fill_note: str


@dataclass(frozen=True)
class YearTick:
    x: float
    label: str


@dataclass(frozen=True)
class ReferenceMarker:
    y: float


@dataclass(frozen=True)
class RuleSpec:
    name: str
    box: Box
    width: int = 9_525
    dashed: bool = True
    arrow: bool = False


@dataclass(frozen=True)
class LabelSpec:
    box: Box
    text: str
    name: str = "Label"


@dataclass(frozen=True)
class LegendKey:
    box: Box
    fill: str


@dataclass(frozen=True)
class ScaleLabel:
    box: Box
    text: str
    fill: str | None = None


@dataclass(frozen=True)
class SummaryBadge:
    box: Box
    text: str


@dataclass(frozen=True)
class Callout:
    name: str
    box: Box
    text: str
    size_pt: float
    color: str = BLACK
    fill: str | None = WHITE
    line_color: str | None = "none"
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
# Chart data: the source area chart omits native categories/names, so the chart
# values stay in Python while labels/categories are overlaid as slide shapes.
# ════════════════════════════════════════════════════════════════════════════
BUILDOUT_YEARS: tuple[str, ...] = tuple(str(year) for year in range(2026, 2051))
_EMPTY_25: tuple[None, ...] = (None,) * len(BUILDOUT_YEARS)

DEMAND_BAND_SERIES: tuple[DemandBandSeries, ...] = (
    DemandBandSeries(
        "Orderbook",
        (1, 2, 2, 5, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None),
        "solid 808080 gray; bottom visible band",
    ),
    DemandBandSeries(
        "Retirement replacements",
        (None, None, None, None, None, None, 9, 10, 3, None, 2, 1, 2, 2, 4, 2, 4, 5, 7, 7, 1, 1, None, 2, 3),
        "solid C0C0C0 silver",
    ),
    DemandBandSeries(
        "SHIPS Act Scenario",
        (None, None, None, 7, 15, 30, 41, 23, 19, 11, 6, 4, 6, 4, 6, 3, 2, 3, 2, 3, 2, 2, 2, 2, 8),
        "solid 364D6E dark blue",
    ),
    DemandBandSeries(
        "Unused demand band placeholder 1",
        _EMPTY_25,
        "template keeps a 4C6C9C series slot; all values blank in this scenario",
    ),
    DemandBandSeries(
        "Unused demand band placeholder 2",
        _EMPTY_25,
        "template keeps a 6F8DB9 series slot; all values blank in this scenario",
    ),
    DemandBandSeries(
        "Unused demand band placeholder 3",
        _EMPTY_25,
        "template keeps a 9DB1CF series slot; all values blank in this scenario",
    ),
    DemandBandSeries(
        "Heritage Foundation target (incremental)",
        (None, None, None, None, None, None, None, 36, 81, 106, 126, 132, 131, 150, 150, 156, 60, None, None, None, None, None, None, None, None),
        "ltUpDiag hatch from the chart template",
    ),
    DemandBandSeries(
        "Excess US capacity",
        (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 96, 156, 156, 156, 163, 163, 164, 162, 155),
        "solid C30C3E crimson top band",
    ),
)

# styled_chart() only rewrites values for this think-cell-like template; the
# category labels and series captions are manual slide shapes. Do not pass names
# here unless you intend to rewrite template text caches and lose byte parity.
_CHART0_DATA = {
    "categories": None,
    "series": [{"values": list(series.values)} for series in DEMAND_BAND_SERIES],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ════════════════════════════════════════════════════════════════════════════
# Slide copy, zones, and constants.
# ════════════════════════════════════════════════════════════════════════════
SECTION = "US-Built Ship Demand"
TOPIC = "With SHIPS Act"
TITLE = "SHIPS Act Volume"
TAKEAWAY = (
    "Current bill language specifying total funding for subsidies limits annual "
    "fleet additions to single digits by mid-2030s; revisions required to increase demand."
)
SOURCE_NOTE = (
    "Note: (1) Assumes avg. 50K GT per newbuild (~13K higher than current fleet avg.); "
    "10M GT target may be achieved with 140-160 deliveries / year with 60K-70K GT per newbuild | "
    "Source: MAP; SHIPS Act; Building Ships in America; 46 USC 53106 (MSP subsidy); "
    "46 USC 53406 (TSP subsidy); MARAD (MSP / TSP participation); MARAD (vessel characteristics); "
    "MARAD (US vs. foreign-flag operating costs); GAO report on Maritime Security; FRED (PPI, BE Inflation); "
    "EIA AEO (Crude & LNG exports); BP (conversions); USTR (Section 301 Actions); "
    "USTR (Section 301 Action modifications); GAO (USG/USDA volume); IMF (Import forecast); "
    "S&P (Current and forecast prices, FX rates, US trade volumes and destinations); "
    "Drewry (foreign-flag opex; near-term cost growth outlook); Clarksons (Orderbook, current fleet, "
    "retirements, capacity, observed service life); Press releases (competitor expansion); "
    "Market participant feedback (Service life, build assumptions)"
)

CHART_FRAME = TextZone(
    "ChartFrame",
    Box(0.429, 1.696, 11.323, 3.906),
    10,
    "Styled chart frame; annotation shapes are layered over it.",
)
SCENARIO_CHIP = TextZone(
    "Rectangle 724",
    Box(8.069, 0.173, 2.977, 0.218),
    12,
    "Top-right scenario chip, one line.",
)
YEAR_TICK_ZONE = TextZone(
    "YearLabel",
    Box(0.0, 5.479, 0.167, 0.306),
    10,
    "Manual category-axis year labels; each tick supplies x only.",
)
TEN_M_GT_CAP = TextZone(
    "Text Placeholder 25",
    Box(11.913, 2.108, 0.552, 0.167),
    10,
    "Right-side target label; source footnote marker is plain 10pt.",
)
Y_AXIS_TITLE = TextZone(
    "Text Placeholder 25",
    Box(0.542, 1.505, 4.347, 0.167),
    10,
    "External y-axis title above the chart, bold, no-wrap.",
)
LEGEND_PANEL = Box(0.979, 1.850, 3.910, 1.191)
PATTERN_LEGEND_SWATCH = Box(1.090, 2.149, 0.196, 0.146)
PORT_ALPHA_PHASE_NOTE = TextZone(
    "Rectangle 804",
    Box(5.133, 1.499, 5.268, 0.437),
    12,
    "Pale-blue scenario note above chart body; keep to one compact sentence.",
)
PORT_ALPHA_SHARE_CAPTION = TextZone(
    "Rectangle 6",
    Box(0.249, 5.826, 1.923, 0.340),
    10,
    "Bottom-strip caption; bold italic, left of badges.",
)
CAPACITY_CAPTION = TextZone(
    "Rectangle 709",
    Box(10.500, 1.499, 2.694, 0.506),
    10,
    "Right-side capacity caption; compact italic explanatory note.",
)

ARROW_X = 11.717
ARROW_W = 0.141
ARROW_H = 0.167
ANNOT_LABEL_H = 0.167
PCT_BADGE_Y = 5.868
PCT_BADGE_H = 0.256
PHASE_RULE_X = 0.911
PHASE_RULE_W = 10.750
ARROW_RULE_X = 0.913
ARROW_RULE_W = 10.900
ARROW_RULE_H = 0.008


# ════════════════════════════════════════════════════════════════════════════
# Repeated annotation data.
# ════════════════════════════════════════════════════════════════════════════
REFERENCE_MARKERS: tuple[ReferenceMarker, ...] = (
    ReferenceMarker(2.108),
    ReferenceMarker(2.658),
    ReferenceMarker(2.983),
    ReferenceMarker(3.630),
    ReferenceMarker(4.587),
    ReferenceMarker(4.280),
)

PHASE_RULES: tuple[RuleSpec, ...] = (
    RuleSpec("Straight Connector 734", Box(PHASE_RULE_X, 3.066, PHASE_RULE_W, 0.000), arrow=True),
    RuleSpec("Straight Connector 735", Box(PHASE_RULE_X, 2.191, PHASE_RULE_W, 0.000), arrow=True),
    RuleSpec("Straight Connector 737", Box(PHASE_RULE_X, 2.741, PHASE_RULE_W, 0.000), arrow=True),
    RuleSpec("Straight Connector 740", Box(PHASE_RULE_X, 3.714, PHASE_RULE_W, 0.000), arrow=True),
    RuleSpec("Straight Connector 741", Box(PHASE_RULE_X, 4.363, PHASE_RULE_W, 0.000), arrow=True),
    RuleSpec("Straight Connector 743", Box(PHASE_RULE_X, 4.670, PHASE_RULE_W, 0.000), arrow=True),
)

YEAR_TICKS: tuple[YearTick, ...] = (
    YearTick(5.755, "2037"),
    YearTick(6.203, "2038"),
    YearTick(6.651, "2039"),
    YearTick(7.099, "2040"),
    YearTick(7.547, "2041"),
    YearTick(8.443, "2043"),
    YearTick(8.891, "2044"),
    YearTick(9.339, "2045"),
    YearTick(9.786, "2046"),
    YearTick(2.620, "2030"),
    YearTick(10.682, "2048"),
    YearTick(11.130, "2049"),
    YearTick(11.578, "2050"),
    YearTick(10.234, "2047"),
    YearTick(0.828, "2026"),
    YearTick(1.276, "2027"),
    YearTick(1.724, "2028"),
    YearTick(2.172, "2029"),
    YearTick(3.068, "2031"),
    YearTick(3.516, "2032"),
    YearTick(7.995, "2042"),
    YearTick(3.964, "2033"),
    YearTick(4.411, "2034"),
    YearTick(4.859, "2035"),
    YearTick(5.307, "2036"),
)

REFERENCE_LABELS: tuple[LabelSpec, ...] = (
    LabelSpec(Box(11.913, 2.658, 1.281, ANNOT_LABEL_H), "PA Phase 5 (125/yr.)"),
    LabelSpec(Box(11.913, 2.983, 1.281, ANNOT_LABEL_H), "PA Phase 4 (105/yr.)"),
    LabelSpec(Box(11.913, 3.630, 1.205, ANNOT_LABEL_H), "PA Phase 3 (65/yr.)"),
    LabelSpec(Box(11.913, 4.280, 1.205, ANNOT_LABEL_H), "PA Phase 2 (25/yr.)"),
    LabelSpec(Box(11.913, 4.587, 1.128, ANNOT_LABEL_H), "PA Phase 1 (6/yr.)"),
)

LEGEND_LABELS: tuple[LabelSpec, ...] = (
    LabelSpec(Box(1.342, 1.922, 1.222, ANNOT_LABEL_H), "Excess US capacity"),
    LabelSpec(Box(1.342, 2.144, 2.488, ANNOT_LABEL_H), "Heritage Foundation target (incremental)"),
    LabelSpec(Box(1.342, 2.366, 1.236, ANNOT_LABEL_H), "SHIPS Act Scenario"),
    LabelSpec(Box(1.342, 2.589, 1.545, ANNOT_LABEL_H), "Retirement replacements"),
    LabelSpec(Box(1.342, 2.811, 0.653, ANNOT_LABEL_H), "Orderbook"),
)

LEGEND_KEYS: tuple[LegendKey, ...] = (
    LegendKey(Box(1.090, 1.927, 0.196, 0.146), "C30C3E"),
    LegendKey(Box(1.090, 2.372, 0.196, 0.146), "364D6E"),
    LegendKey(Box(1.090, 2.594, 0.196, 0.146), "C0C0C0"),
    LegendKey(Box(1.090, 2.816, 0.196, 0.146), "808080"),
)

PRE_LEGEND_ARROW_RULES: tuple[RuleSpec, ...] = (
    RuleSpec("Straight Arrow Connector 777", Box(ARROW_RULE_X, 2.729, ARROW_RULE_W, ARROW_RULE_H)),
    RuleSpec("Straight Arrow Connector 778", Box(ARROW_RULE_X, 2.183, ARROW_RULE_W, ARROW_RULE_H)),
)

POST_LEGEND_ARROW_RULES: tuple[RuleSpec, ...] = (
    RuleSpec("Straight Arrow Connector 796", Box(ARROW_RULE_X, 3.052, ARROW_RULE_W, ARROW_RULE_H)),
    RuleSpec("Straight Arrow Connector 797", Box(ARROW_RULE_X, 3.712, ARROW_RULE_W, ARROW_RULE_H)),
    RuleSpec("Straight Arrow Connector 798", Box(ARROW_RULE_X, 4.349, ARROW_RULE_W, ARROW_RULE_H)),
)

SCALE_LABELS: tuple[ScaleLabel, ...] = (
    ScaleLabel(Box(4.091, 2.912, 0.600, 0.100), "Higher"),
    ScaleLabel(Box(4.091, 2.071, 0.600, 0.100), "Lower"),
    ScaleLabel(Box(3.860, 2.475, 1.063, 0.133), "Confidence level", WHITE),
)

SUMMARY_BADGES: tuple[SummaryBadge, ...] = (
    SummaryBadge(Box(2.490, PCT_BADGE_Y, 0.451, PCT_BADGE_H), "70%"),
    SummaryBadge(Box(4.717, PCT_BADGE_Y, 0.451, PCT_BADGE_H), "83%"),
    SummaryBadge(Box(6.957, PCT_BADGE_Y, 0.451, PCT_BADGE_H), "78%"),
    SummaryBadge(Box(9.196, PCT_BADGE_Y, 0.451, PCT_BADGE_H), "75%"),
    SummaryBadge(Box(11.435, PCT_BADGE_Y, 0.452, PCT_BADGE_H), "75%"),
)

CALLOUTS: tuple[Callout, ...] = (
    Callout(
        "Speech Bubble: Rectangle 9",
        Box(2.999, 4.934, 1.201, 0.278),
        "Contingent upon SHIPS Act passing",
        size_pt=8,
        color=WHITE,
        fill=None,
        prst="wedgeRectCallout",
        geom_adj={"adj1": "val 19859", "adj2": "val -3695"},
        italic=True,
    ),
    Callout(
        "Rectangle 709",
        CAPACITY_CAPTION.box,
        "Total US delivery capacity by 2050 w/ PA phases and competitor expansion; PA deliveries in parenthetical",
        size_pt=10,
        color=BLACK,
        fill=None,
        prst="rect",
        italic=True,
    ),
    Callout(
        "Speech Bubble: Rectangle 851",
        Box(5.269, 4.934, 2.340, 0.278),
        "Requires increased universal cargo fees and MSTF balance cap increase",
        size_pt=8,
        color=BLACK,
        fill=WHITE,
        prst="wedgeRectCallout",
        geom_adj={"adj1": "val 19859", "adj2": "val -3695"},
        italic=True,
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Text helpers: two paragraph styles matter for byte parity.
# ════════════════════════════════════════════════════════════════════════════
def _black_run(text: str, *, size_pt: float = 10, bold: bool = False, italic: bool = False) -> str:
    return run(text, size=PT(size_pt), bold=bold or None, italic=italic or None, color=BLACK, font=FONT)


def _white_run(text: str, *, size_pt: float = 10, bold: bool = False, italic: bool = False) -> str:
    return run(text, size=PT(size_pt), bold=bold or None, italic=italic or None, color=WHITE, font=FONT)


def _default_run(text: str, *, size_pt: float = 10, bold: bool = False, italic: bool = False) -> str:
    """Run with font/size but no explicit fill; used where the source omitted color."""

    return run(text, size=PT(size_pt), bold=bold or None, italic=italic or None, font=FONT)


def _chart_label_para(runs, *, align: str | None = None) -> str:
    """Manual chart labels use explicit zero paragraph margins/indent."""

    return paragraph(runs, align=align, mar_l=0, indent=0, line_spacing=100_000)


def _simple_para(runs, *, align: str | None = None) -> str:
    """Most non-chart text boxes use the primitive defaults plus 100% spacing."""

    return paragraph(runs, align=align, line_spacing=100_000)


def _empty_para() -> str:
    return paragraph([], align="ctr", line_spacing=100_000)


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def paint_chrome(out: list[str]) -> None:
    out.append(breadcrumb(SECTION, TOPIC))
    out.append(title_placeholder(TITLE, TAKEAWAY))
    out.append(sources_line(SOURCE_NOTE))
    out.append(prelim_chip())


def paint_scenario_chip(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            SCENARIO_CHIP.name,
            *SCENARIO_CHIP.box.emu(),
            [_simple_para([_default_run("(2) SHIPS Act Scenario", size_pt=12, bold=True)], align="ctr")],
            fill="447BB2",
            line_color=BLACK,
            anchor="ctr",
        )
    )


def paint_chart_frame(out: list[str], ids: ShapeIds) -> None:
    out.append(
        graphic_frame(
            sp_id=ids.next(),
            name="Chart",
            x=IN(CHART_FRAME.box.x),
            y=IN(CHART_FRAME.box.y),
            cx=IN(CHART_FRAME.box.w),
            cy=IN(CHART_FRAME.box.h),
            rId="rId2",
        )
    )


def paint_reference_markers(out: list[str], ids: ShapeIds) -> None:
    for marker in REFERENCE_MARKERS:
        out.append(
            text_box(
                ids.next(),
                "LegendSwatch",
                IN(ARROW_X),
                IN(marker.y),
                IN(ARROW_W),
                IN(ARROW_H),
                [_empty_para()],
                fill=DK,
                line_color="none",
                prst="rightArrow",
                geom_adj={"adj1": "val 100000", "adj2": "val 100000"},
                anchor="ctr",
                rot=10_800_000,
            )
        )


def _paint_rules(out: list[str], ids: ShapeIds, rules: tuple[RuleSpec, ...]) -> None:
    for rule in rules:
        out.append(
            connector(
                ids.next(),
                rule.name,
                *rule.box.emu(),
                color=BLACK,
                width=rule.width,
                dashed=rule.dashed,
                arrow=rule.arrow,
            )
        )


def paint_phase_rules(out: list[str], ids: ShapeIds) -> None:
    _paint_rules(out, ids, PHASE_RULES)


def paint_year_ticks(out: list[str], ids: ShapeIds) -> None:
    for tick in YEAR_TICKS:
        out.append(
            text_box(
                ids.next(),
                YEAR_TICK_ZONE.name,
                IN(tick.x),
                IN(YEAR_TICK_ZONE.box.y),
                IN(YEAR_TICK_ZONE.box.w),
                IN(YEAR_TICK_ZONE.box.h),
                [_chart_label_para([_black_run(tick.label)], align="r")],
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


def paint_axis_titles(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            TEN_M_GT_CAP.name,
            *TEN_M_GT_CAP.box.emu(),
            [_chart_label_para([_black_run("10M GT"), _black_run("1")])],
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
    out.append(
        text_box(
            ids.next(),
            Y_AXIS_TITLE.name,
            *Y_AXIS_TITLE.box.emu(),
            [_chart_label_para([_black_run("Additions to US-Built, Oceangoing Commercial Fleet (# deliveries)", bold=True)])],
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


def _paint_chart_label_specs(out: list[str], ids: ShapeIds, specs: tuple[LabelSpec, ...]) -> None:
    for spec in specs:
        out.append(
            text_box(
                ids.next(),
                spec.name,
                *spec.box.emu(),
                [_chart_label_para([_black_run(spec.text)])],
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


def paint_reference_and_legend_labels(out: list[str], ids: ShapeIds) -> None:
    _paint_chart_label_specs(out, ids, REFERENCE_LABELS)
    _paint_chart_label_specs(out, ids, LEGEND_LABELS)


def paint_legend_panel_and_keys(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            "LegendSwatch",
            *LEGEND_PANEL.emu(),
            [_empty_para()],
            fill=WHITE,
            line_color="none",
            anchor="ctr",
        )
    )
    for key in LEGEND_KEYS:
        out.append(
            text_box(
                ids.next(),
                "LegendSwatch",
                *key.box.emu(),
                [_empty_para()],
                fill=key.fill,
                line_color="none",
                anchor="ctr",
            )
        )
    out.append(
        text_box(
            ids.next(),
            "Rectangle 787",
            *PATTERN_LEGEND_SWATCH.emu(),
            [_empty_para()],
            fill=None,
            line_color="none",
            pattern_fill={"prst": "ltUpDiag", "fg": "scheme:tx1", "bg": "scheme:bg1"},
            anchor="ctr",
        )
    )


def paint_scale_and_late_rules(out: list[str], ids: ShapeIds) -> None:
    for label in SCALE_LABELS:
        out.append(
            text_box(
                ids.next(),
                "Label",
                *label.box.emu(),
                [_simple_para([_black_run(label.text, size_pt=8, italic=True)], align="ctr")],
                fill=label.fill,
                line_color="none",
                anchor="ctr",
            )
        )

    out.append(
        connector(
            ids.next(),
            "Straight Arrow Connector 800",
            IN(4.391),
            IN(2.171),
            IN(0),
            IN(0.741),
            color=BLACK,
            width=28_575,
            arrow=True,
        )
    )
    out.append(
        connector(
            ids.next(),
            "Straight Arrow Connector 803",
            IN(PHASE_RULE_X),
            IN(4.656),
            IN(ARROW_RULE_W),
            IN(ARROW_RULE_H),
            color=BLACK,
            width=9_525,
            dashed=True,
        )
    )


def paint_capacity_notes_and_badges(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            PORT_ALPHA_PHASE_NOTE.name,
            *PORT_ALPHA_PHASE_NOTE.box.emu(),
            [
                _simple_para(
                    [
                        _black_run(
                            "Demand modeled with Port Alpha Phase 5 capacity; demand would spread over more years if capacity held at earlier phases ",
                            size_pt=12,
                            bold=True,
                        )
                    ],
                    align="ctr",
                )
            ],
            fill="CEDDEC",
            line_color="none",
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            ids.next(),
            PORT_ALPHA_SHARE_CAPTION.name,
            *PORT_ALPHA_SHARE_CAPTION.box.emu(),
            [_simple_para([_black_run("Modeled % deliveries attributable to Port Alpha:", bold=True, italic=True)])],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )
    for badge in SUMMARY_BADGES:
        out.append(
            text_box(
                ids.next(),
                "ValueLabel",
                *badge.box.emu(),
                [_simple_para([_black_run(badge.text)], align="ctr")],
                fill=None,
                line_color=BLACK,
                line_width=6_350,
                prst="ellipse",
                anchor="ctr",
                l_ins=0,
                r_ins=0,
            )
        )


def paint_callouts(out: list[str], ids: ShapeIds) -> None:
    for callout in CALLOUTS:
        run_builder = _white_run if callout.color == WHITE else _black_run
        out.append(
            text_box(
                ids.next(),
                callout.name,
                *callout.box.emu(),
                [
                    _simple_para(
                        [run_builder(callout.text, size_pt=callout.size_pt, italic=callout.italic)],
                        align="ctr",
                    )
                ],
                fill=callout.fill,
                line_color=callout.line_color,
                prst=callout.prst,
                geom_adj=callout.geom_adj,
                anchor="ctr",
            )
        )


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # Paint order matters in PowerPoint OOXML: later elements sit on top.
    paint_chrome(out)
    paint_scenario_chip(out, ids)
    paint_chart_frame(out, ids)
    paint_reference_markers(out, ids)
    paint_phase_rules(out, ids)
    paint_year_ticks(out, ids)
    paint_axis_titles(out, ids)
    paint_reference_and_legend_labels(out, ids)
    _paint_rules(out, ids, PRE_LEGEND_ARROW_RULES)
    paint_legend_panel_and_keys(out, ids)
    _paint_rules(out, ids, POST_LEGEND_ARROW_RULES)
    paint_scale_and_late_rules(out, ids)
    paint_capacity_notes_and_badges(out, ids)
    paint_callouts(out, ids)

    return "".join(out)


def render() -> str:
    return slide(_body())
