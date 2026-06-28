"""Teaching exemplar: SHIPS Act volume scenario slide.

ROLE
  scenario_forecast / demand_volume_ramp

USE WHEN
  A slide needs one dominant multi-year demand-volume exhibit, manual year ticks,
  a stacked demand-band legend, a confidence-scale annotation, capacity phase
  reference rules, bottom milestone badges, and caveat callouts.

TEACHES
  - source chart XML inspection before choosing chart machinery
  - native area_chart(mode="stacked") factory for a stacked-area exhibit
  - explicit chart categories, series names, values, colors, pattern fill, and
    axis settings instead of opaque chart cache data
  - manual category ticks and external axis titles over a native chart frame
  - capacity phase rules and right-arrow markers layered over the plot
  - manual legend construction, including a pattern key
  - bottom summary-badge row and caveat callouts layered after the chart
  - preserving source paint order even when the chrome appears before the chart

TEXT-FIT PRECEDENT
  scenario_title:
    geometry: 2.977in wide x 0.218in high
    type: Arial 12pt, bold, centered, 100% line spacing
    content: one short scenario-chip label
    copy_when: the slide needs an explicit scenario tag in addition to the
               house title and Preliminary chip
  demand_capacity_caption:
    geometry: 5.268in wide x 0.437in high
    type: Arial 12pt, bold, centered, 100% line spacing
    content: one sentence; works as a pale-blue chart overlay caption
  source_note:
    geometry: house source_note()
    type: house source-note styling
    content: one very long Note/Source line; this is dense but source-faithful
  confidence_scale:
    geometry: 1.063in x 0.133in center label + 0.6in x 0.1in endpoints
    type: Arial 8pt italic, centered
    content: one-to-two-word labels only

SOURCE NOTE
  Teaching rewrite of the source-faithful `ships_act_volume.py` module.
  The attached `slide51_chart30.xml` shows that the source chart is a stacked
  area chart, not a simple column chart. The chart is built with the native
  `area_chart(mode="stacked")` factory in deck_core.charts (promoted from this
  module's former local stacked-area shim); its data and style were transcribed
  from the attached chart XML/XLSB. The slide body keeps the
  source paint order, coordinates, manual labels, legend, phase rules, summary
  badges, Preliminary chip, and callouts.

FIDELITY NOTE
  The body render is source-faithful. The chart is a practical native factory
  rebuild: it preserves the source chart type (stacked area), visible values,
  fills, pattern-fill heritage target layer, hidden category labels, fixed value
  axis, no gridlines, and manual plot-area layout. It is not a byte-identical
  chart-template port; tiny differences in chart XML ordering or PowerPoint's
  native area rendering can remain versus the source chart part.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, Link, PT, Sources, area_chart, body_slide, connector, esc, graphic_frame,
    paragraph, run, source_note, text_box,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
PRELIM = "FFFFCC"
FONT = "Arial"

LAYOUT = "slideLayout4"


# ════════════════════════════════════════════════════════════════════════════
# Explicit chart data, transcribed from slide51_chart30.xml / .xlsb.
# ════════════════════════════════════════════════════════════════════════════
CHART_CATEGORIES: tuple[str, ...] = tuple(str(year) for year in range(2026, 2051))

ORDERBOOK = "808080"
RETIREMENT_REPLACEMENTS = "C0C0C0"
SHIPS_ACT = "364D6E"
HERITAGE_PATTERN = {"prst": "ltUpDiag", "fg": BLACK, "bg": WHITE}
EXCESS_US_CAPACITY = "C30C3E"

DEMAND_BAND_SERIES: tuple[dict, ...] = (
    {
        "name": "Orderbook",
        "color": ORDERBOOK,
        "values": [1, 2, 2, 5, 5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    },
    {
        "name": "Retirement replacements",
        "color": RETIREMENT_REPLACEMENTS,
        "values": [None, None, None, None, None, None, 9, 10, 3, None, 2, 1, 2, 2, 4, 2, 4, 5, 7, 7, 1, 1, None, 2, 3],
    },
    {
        "name": "SHIPS Act Scenario",
        "color": SHIPS_ACT,
        "values": [None, None, None, 7, 15, 30, 41, 23, 19, 11, 6, 4, 6, 4, 6, 3, 2, 3, 2, 3, 2, 2, 2, 2, 8],
    },
    {
        "name": "Heritage Foundation target (incremental)",
        "pattern": HERITAGE_PATTERN,
        "values": [None, None, None, None, None, None, None, 36, 81, 106, 126, 132, 131, 150, 150, 156, 60, None, None, None, None, None, None, None, None],
    },
    {
        "name": "Excess US capacity",
        "color": EXCESS_US_CAPACITY,
        "values": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 96, 156, 156, 156, 163, 163, 164, 162, 155],
    },
)

# Kept as a readable data mirror for agents/tools that expect the converted-slide
# data-dict shape. CHARTS consumes the same values through area_chart(mode="stacked").
_CHART0_DATA = {
    "categories": CHART_CATEGORIES,
    "series": DEMAND_BAND_SERIES,
}

CHART_STYLE = {
    "categories": list(CHART_CATEGORIES),
    "series": [dict(series) for series in DEMAND_BAND_SERIES],
    "show_cat_labels": False,
    "show_value_axis_labels": True,
    "show_gridlines": False,
    "value_axis_format": '#,##0;"-"#,##0',
    "axis_line_color": BLACK,
    "axis_line_width": 9_525,
    "value_axis_min": 0,
    "value_axis_max": 220,
    "value_axis_major_unit": 20,
    "plot_layout": {
        "x": 0.042624961668199936,
        "y": 0.043555555555555556,
        "w": 0.9494020239190433,
        "h": 0.9128888888888889,
    },
    "cat_header": "Year",
}

CHARTS = [area_chart(mode="stacked", **CHART_STYLE)]


TEXT_FIT = {
    "scenario_chip": {
        "box_in": (2.977, 0.218),
        "font_pt": 12,
        "content": "(2) SHIPS Act Scenario",
        "note": "Single-line centered chip; keep scenario labels short.",
    },
    "capacity_caption": {
        "box_in": (5.268, 0.437),
        "font_pt": 12,
        "content": "one sentence over the chart",
        "note": "Bold centered overlay. This is the practical maximum density at 12pt.",
    },
    "summary_badges": {
        "box_in": (0.451, 0.256),
        "font_pt": 10,
        "content": "short percentages only",
        "note": "Narrower than the US-delivery summary badges; <=3 visible chars plus % is safe.",
    },
    "callouts": {
        "font_pt": 8,
        "content": "short caveat sentence fragments",
        "note": "Speech bubbles use 100% line spacing and centered text.",
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
class Rule:
    name: str
    x: float
    y: float
    w: float
    h: float
    width: int = 9_525
    dashed: bool = True
    arrow: object = False     # False / True (tail) / "head" / "both"
    dash: str | None = None   # explicit prstDash preset (e.g. "lgDash"); overrides `dashed`
    color: str = BLACK        # "none" for an invisible source anchor line
    grad: tuple | None = None  # ((pos, hex), ...) gradient stops; overrides `color`
    grad_angle: int = 5_400_000


@dataclass(frozen=True)
class ReferenceMarker:
    y: float


@dataclass(frozen=True)
class YearTick:
    x: float
    label: str


@dataclass(frozen=True)
class LabelBox:
    name: str
    box: Box
    text: str
    font_pt: float = 10
    bold: bool = False
    italic: bool = False
    color: str | None = BLACK
    fill: str | None = None
    align: str | None = None
    anchor: str = "ctr"
    wrap: str = "none"
    zero_margins: bool = True
    vert: str | None = None   # "vert270" for a vertically-rotated label (year ticks)


@dataclass(frozen=True)
class LegendKey:
    name: str
    box: Box
    fill: str | None = None
    pattern: dict[str, str] | None = None


@dataclass(frozen=True)
class SummaryBadge:
    box: Box
    label: str


@dataclass(frozen=True)
class Callout:
    name: str
    box: Box
    text: str
    font_pt: float
    fill: str | None
    color: str
    prst: str = "rect"
    geom_adj: dict[str, str] | None = None
    bold: bool = False
    italic: bool = False
    line_color: str | None = "none"


@dataclass(frozen=True)
class SourceHotspot:
    """Invisible clickable area over the plain-text source line."""

    name: str
    box: Box
    r_id: str


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Layout zones: chart, manual labels, legend, bottom strip, and callouts.
# ════════════════════════════════════════════════════════════════════════════
CHART_FRAME = Box(0.429, 1.696, 11.323, 3.906)
# Source deck chip geometry: charts_originals.pptx slide6.xml / p:cNvPr name="PrelimChip".
# Keep raw EMU so the recurring preliminary-banner fix is exact, not rounded.
PRELIM_CHIP_EMU = (10_267_829, 111_556, 1_467_612, 290_000)
SOURCE_NOTE_EMU = (453_079, 5_930_000, 11_282_362, 540_000)

RIGHT_ARROW_MARK = TextZone(
    name="CapacityRuleArrowMarker",
    box=Box(11.717, 0.0, 0.141, 0.167),
    font_pt=0,
    fit_note="rightArrow marker rotated 180deg; y varies by phase rule",
)

YEAR_TICK_ZONE = TextZone(
    name="YearLabel",
    box=Box(0.0, 5.479, 0.167, 0.306),
    font_pt=10,
    fit_note="25 tight, right-aligned year labels; all in zero-inset no-wrap boxes.",
)

ANNOTATION_LABEL_H = 0.167
PCT_BADGE_ZONE = TextZone(
    name="PortAlphaShareBadge",
    box=Box(0.0, 5.868, 0.0, 0.256),
    font_pt=10,
    fit_note="five ellipse percentage badges across bottom strip",
)

LEGEND_PANEL = LegendKey("DemandLegendPanel", Box(0.979, 1.850, 3.910, 1.191), WHITE)

AXIS_RIGHT_CAP = LabelBox(
    "RightAxisCap",
    Box(11.913, 2.108, 0.552, 0.167),
    "10M GT",
    font_pt=10,
    align=None,
)
AXIS_TITLE = LabelBox(
    "ChartAxisTitle",
    Box(0.542, 1.505, 4.347, 0.167),
    "Additions to US-Built, Oceangoing Commercial Fleet (# deliveries)",
    font_pt=10,
    bold=True,
    align=None,
    anchor="b",
)

SUMMARY_CAPTION = LabelBox(
    "PortAlphaShareCaption",
    Box(0.249, 5.826, 1.923, 0.340),
    "Modeled % deliveries attributable to Port Alpha:",
    font_pt=10,
    bold=True,
    italic=True,
    wrap="square",
    zero_margins=False,
)

SCENARIO_CHIP = LabelBox(
    "ScenarioChip",
    Box(8.069, 0.173, 2.977, 0.218),
    "(2) SHIPS Act Scenario",
    font_pt=12,
    bold=True,
    color=None,
    fill="447BB2",
    align="ctr",
    wrap="square",
    zero_margins=False,
)

# Source-line external links (anchor, rId, url). The area chart takes rId2, so the
# 16 linked sources run rId3..rId18; HYPERLINKS feeds the builder one External
# relationship per rId, and the Sources band wires each anchor through Link().
_SOURCE_LINKS = (
    ("MAP", "rId3", "https://www.whitehouse.gov/maritimemight/"),
    ("SHIPS Act", "rId4", "https://www.congress.gov/bill/119th-congress/senate-bill/1541/text#toc-id9f432e34eabc4c5ea3d818bfdc7a838f"),
    ("Building Ships in America", "rId5", "https://www.congress.gov/bill/119th-congress/senate-bill/1536/text"),
    ("46 USC 53106 (MSP subsidy)", "rId6", "https://www.law.cornell.edu/uscode/text/46/53106%20(MSP%20Rates)"),
    ("46 USC 53406 (TSP subsidy)", "rId7", "https://www.law.cornell.edu/uscode/text/46/53406"),
    ("MARAD (MSP / TSP participation)", "rId8", "https://www.maritime.dot.gov/data-reports/us-flag-fleet-CY-2025"),
    ("MARAD (vessel characteristics)", "rId9", "https://www.maritime.dot.gov/sites/marad.dot.gov/files/2024-07/FACT%20SHEET%20for%20DOMESTIC%20SHIPBUILDING%20(JULY%202024)_0.pdf"),
    ("MARAD (US vs. foreign-flag operating costs)", "rId10", "https://www.maritime.dot.gov/outreach/publications/comparison-us-and-foreign-flag-operating-costs"),
    ("GAO report on Maritime Security", "rId11", "https://www.gao.gov/assets/gao-18-478.pdf"),
    ("FRED (PPI, BE Inflation)", "rId12", "https://fred.stlouisfed.org/series/PCU483111483111"),
    ("EIA AEO (Crude & LNG exports)", "rId13", "https://www.eia.gov/outlooks/aeo/data/browser/#/?id=76-AEO2025&cases=ref2025&sourcekey=0"),
    ("BP (conversions)", "rId14", "https://www.bp.com/content/dam/bp/business-sites/en/global/corporate/pdfs/energy-economics/statistical-review/bp-stats-review-2022-approximate-conversion-factors.pdf"),
    ("USTR (Section 301 Actions)", "rId15", "https://www.federalregister.gov/documents/2025/04/23/2025-06927/notice-of-action-and-proposed-action-in-section-301-investigation-of-chinas-targeting-the-maritime"),
    ("USTR (Section 301 Action modifications)", "rId16", "https://ustr.gov/sites/default/files/files/Press/Releases/2025/Federal%20Register%20Notice%2010.26.2025.pdf"),
    ("GAO (USG/USDA volume)", "rId17", "https://www.gao.gov/assets/gao-22-105160.pdf"),
    ("IMF (Import forecast)", "rId18", "https://www.imf.org/-/media/files/publications/weo/2025/october/english/ch1.pdf"),
)
HYPERLINKS = [{"rId": rid, "url": url} for _a, rid, url in _SOURCE_LINKS]

SOURCE_NOTE_ITEMS = tuple(a for a, _rid, _url in _SOURCE_LINKS) + (
    "S&P (Current and forecast prices, FX rates, US trade volumes and destinations)",
    "Drewry (foreign-flag opex; near-term cost growth outlook)",
    "Clarksons (Orderbook, current fleet, retirements, capacity, observed service life)",
    "Press releases (competitor expansion)",
    "Market participant feedback (Service life, build assumptions)",
)

SOURCE_NOTE = Sources(
    note="(1) Assumes avg. 50K GT per newbuild (~13K higher than current fleet avg.); "
    "10M GT target may be achieved with 140-160 deliveries / year with 60K-70K GT per newbuild",
    # Keep the visible source line source-faithful (black, non-underlined text).
    # Transparent hyperlink hotspots are overlaid separately so the anchors remain
    # clickable without LibreOffice/PowerPoint auto-restyling them as blue links.
    source=SOURCE_NOTE_ITEMS,
)

TITLE_SECTION = "US-Built Ship Demand"
TITLE_TOPIC = "With SHIPS Act"
TITLE_HEAD = "SHIPS Act Volume"
TITLE_TAKEAWAY = (
    "Current bill language specifying total funding for subsidies limits annual "
    "fleet additions to single digits by mid-2030s; revisions required to increase demand."
)

# House source band geometry from deck_core.chrome.source_note(). The visible text
# is emitted as one plain source note to match the reference render; hotspots
# below provide click targets for the first 16 source anchors without changing
# visible typography.
SOURCE_NOTE_Y = 5_930_000
SOURCE_HOTSPOTS: tuple[SourceHotspot, ...] = (
    # Row 1 starts at the Source: prefix and covers MAP through FRED.
    SourceHotspot("SourceHotspot MAP", Box(9.00, 6.610, 0.26, 0.105), "rId3"),
    SourceHotspot("SourceHotspot SHIPS Act", Box(9.25, 6.610, 0.53, 0.105), "rId4"),
    SourceHotspot("SourceHotspot Building Ships in America", Box(9.77, 6.610, 1.18, 0.105), "rId5"),
    SourceHotspot("SourceHotspot MSP", Box(10.93, 6.610, 0.78, 0.105), "rId6"),
    SourceHotspot("SourceHotspot TSP", Box(0.50, 6.735, 1.12, 0.105), "rId7"),
    SourceHotspot("SourceHotspot MARAD MSP TSP", Box(1.61, 6.735, 1.44, 0.105), "rId8"),
    SourceHotspot("SourceHotspot MARAD characteristics", Box(3.04, 6.735, 1.37, 0.105), "rId9"),
    SourceHotspot("SourceHotspot MARAD opex", Box(4.40, 6.735, 1.85, 0.105), "rId10"),
    SourceHotspot("SourceHotspot GAO Maritime", Box(6.24, 6.735, 1.74, 0.105), "rId11"),
    SourceHotspot("SourceHotspot FRED", Box(7.97, 6.735, 1.20, 0.105), "rId12"),
    # Row 2 covers EIA through IMF.
    SourceHotspot("SourceHotspot EIA AEO", Box(9.17, 6.735, 1.73, 0.105), "rId13"),
    SourceHotspot("SourceHotspot BP conversions", Box(10.88, 6.735, 0.68, 0.105), "rId14"),
    SourceHotspot("SourceHotspot USTR 301", Box(11.55, 6.735, 1.10, 0.105), "rId15"),
    SourceHotspot("SourceHotspot USTR modifications", Box(0.50, 6.860, 1.77, 0.105), "rId16"),
    SourceHotspot("SourceHotspot GAO volume", Box(2.26, 6.860, 1.15, 0.105), "rId17"),
    SourceHotspot("SourceHotspot IMF", Box(3.40, 6.860, 1.05, 0.105), "rId18"),
)


# ════════════════════════════════════════════════════════════════════════════
# Manual chart data labels, phase rules, and legends.
# ════════════════════════════════════════════════════════════════════════════
REFERENCE_MARKERS: tuple[ReferenceMarker, ...] = (
    ReferenceMarker(2.108),
    ReferenceMarker(2.658),
    ReferenceMarker(2.983),
    ReferenceMarker(3.630),
    ReferenceMarker(4.587),
    ReferenceMarker(4.280),
)

# Invisible lgDash "anchor" rules: the source stacks these (noFill) under the
# visible `dash` rules below. Drawing them black would double every dashed rule
# and muddy the dash pattern, so keep them color="none".
INITIAL_PHASE_RULES: tuple[Rule, ...] = (
    Rule("PhaseCapacityRuleAnchor", 0.911, 3.066, 10.750, 0.000, dash="lgDash", color="none"),
    Rule("PhaseCapacityRuleAnchor", 0.911, 2.191, 10.750, 0.000, dash="lgDash", color="none"),
    Rule("PhaseCapacityRuleAnchor", 0.911, 2.741, 10.750, 0.000, dash="lgDash", color="none"),
    Rule("PhaseCapacityRuleAnchor", 0.911, 3.714, 10.750, 0.000, dash="lgDash", color="none"),
    Rule("PhaseCapacityRuleAnchor", 0.911, 4.363, 10.750, 0.000, dash="lgDash", color="none"),
    Rule("PhaseCapacityRuleAnchor", 0.911, 4.670, 10.750, 0.000, dash="lgDash", color="none"),
)

MID_LEGEND_RULES: tuple[Rule, ...] = (
    Rule("PhaseCapacityRule", 0.913, 2.729, 10.900, 0.008),
    Rule("PhaseCapacityRule", 0.913, 2.183, 10.900, 0.008),
)

LATE_PHASE_RULES: tuple[Rule, ...] = (
    Rule("PhaseCapacityRule", 0.913, 3.052, 10.900, 0.008),
    Rule("PhaseCapacityRule", 0.913, 3.712, 10.900, 0.008),
    Rule("PhaseCapacityRule", 0.913, 4.349, 10.900, 0.008),
    Rule("PhaseCapacityRule", 0.911, 4.656, 10.900, 0.008),
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

REFERENCE_LABELS: tuple[LabelBox, ...] = (
    LabelBox("ReferenceLabel", Box(11.913, 2.658, 1.281, ANNOTATION_LABEL_H), "PA Phase 5 (125/yr.)"),
    LabelBox("ReferenceLabel", Box(11.913, 2.983, 1.281, ANNOTATION_LABEL_H), "PA Phase 4 (105/yr.)"),
    LabelBox("ReferenceLabel", Box(11.913, 3.630, 1.205, ANNOTATION_LABEL_H), "PA Phase 3 (65/yr.)"),
    LabelBox("ReferenceLabel", Box(11.913, 4.280, 1.205, ANNOTATION_LABEL_H), "PA Phase 2 (25/yr.)"),
    LabelBox("ReferenceLabel", Box(11.913, 4.587, 1.128, ANNOTATION_LABEL_H), "PA Phase 1 (6/yr.)"),
)

LEGEND_LABELS: tuple[LabelBox, ...] = (
    LabelBox("LegendLabel", Box(1.342, 1.922, 1.222, ANNOTATION_LABEL_H), "Excess US capacity"),
    LabelBox("LegendLabel", Box(1.342, 2.144, 2.488, ANNOTATION_LABEL_H), "Heritage Foundation target (incremental)"),
    LabelBox("LegendLabel", Box(1.342, 2.366, 1.236, ANNOTATION_LABEL_H), "SHIPS Act Scenario"),
    LabelBox("LegendLabel", Box(1.342, 2.589, 1.545, ANNOTATION_LABEL_H), "Retirement replacements"),
    LabelBox("LegendLabel", Box(1.342, 2.811, 0.653, ANNOTATION_LABEL_H), "Orderbook"),
)

SOLID_LEGEND_KEYS: tuple[LegendKey, ...] = (
    LegendKey("DemandLegendColorKey", Box(1.090, 1.927, 0.196, 0.146), EXCESS_US_CAPACITY),
    LegendKey("DemandLegendColorKey", Box(1.090, 2.372, 0.196, 0.146), SHIPS_ACT),
    LegendKey("DemandLegendColorKey", Box(1.090, 2.594, 0.196, 0.146), RETIREMENT_REPLACEMENTS),
    LegendKey("DemandLegendColorKey", Box(1.090, 2.816, 0.196, 0.146), ORDERBOOK),
)

HERITAGE_LEGEND_KEY = LegendKey(
    "HeritagePatternKey",
    Box(1.090, 2.149, 0.196, 0.146),
    pattern={"prst": "ltUpDiag", "fg": "scheme:tx1", "bg": "scheme:bg1"},
)

SUMMARY_BADGES: tuple[SummaryBadge, ...] = (
    SummaryBadge(Box(2.490, 5.868, 0.451, 0.256), "70%"),
    SummaryBadge(Box(4.717, 5.868, 0.451, 0.256), "83%"),
    SummaryBadge(Box(6.957, 5.868, 0.451, 0.256), "78%"),
    SummaryBadge(Box(9.196, 5.868, 0.451, 0.256), "75%"),
    SummaryBadge(Box(11.435, 5.868, 0.452, 0.256), "75%"),
)

SCALE_LABELS: tuple[LabelBox, ...] = (
    LabelBox("ConfidenceScaleLabel", Box(4.091, 2.912, 0.600, 0.100), "Higher", font_pt=8, italic=True, align="ctr", fill=None, zero_margins=False),
    LabelBox("ConfidenceScaleLabel", Box(4.091, 2.071, 0.600, 0.100), "Lower", font_pt=8, italic=True, align="ctr", fill=None, zero_margins=False),
    LabelBox("ConfidenceScaleLabel", Box(3.860, 2.475, 1.063, 0.133), "Confidence level", font_pt=8, italic=True, align="ctr", fill=WHITE, zero_margins=False),
)

# Red->green vertical gradient, double-headed (source confidence scale: C30C3E "Lower"
# top -> 008600 "Higher" bottom). grad overrides color; arrow="both" = head + tail.
CONFIDENCE_SCALE_ARROW = Rule(
    "ConfidenceScaleArrow", 4.391, 2.171, 0.000, 0.741, width=28_575,
    dashed=False, arrow="both", grad=((0, "C30C3E"), (100_000, "008600")), grad_angle=5_400_000,
)

CAPACITY_CAPTION = Callout(
    name="DemandCapacityCaption",
    box=Box(5.133, 1.499, 5.268, 0.437),
    text="Demand modeled with Port Alpha Phase 5 capacity; demand would spread over more years if capacity held at earlier phases ",
    font_pt=12,
    fill="CEDDEC",
    color=BLACK,
    bold=True,
)

CALLOUTS: tuple[Callout, ...] = (
    Callout(
        name="ContingencyCallout",
        box=Box(2.999, 4.934, 1.201, 0.278),
        text="Contingent upon SHIPS Act passing",
        font_pt=8,
        fill=None,
        color=WHITE,
        prst="wedgeRectCallout",
        geom_adj={"adj1": "val 19859", "adj2": "val -3695"},
        italic=True,
    ),
    Callout(
        name="TotalCapacityCallout",
        box=Box(10.500, 1.499, 2.694, 0.506),
        text="Total US delivery capacity by 2050 w/ PA phases and competitor expansion; PA deliveries in parenthetical",
        font_pt=10,
        fill=None,
        color=BLACK,
        italic=True,
    ),
    Callout(
        name="FundingCallout",
        box=Box(5.269, 4.934, 2.340, 0.278),
        text="Requires increased universal cargo fees and MSTF balance cap increase",
        font_pt=8,
        fill=WHITE,
        color=BLACK,
        prst="wedgeRectCallout",
        geom_adj={"adj1": "val 19859", "adj2": "val -3695"},
        italic=True,
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Text helpers: keep the paint functions at slide-intent level.
# ════════════════════════════════════════════════════════════════════════════
def _r(text: str, *, size_pt: float = 10, bold: bool = False, italic: bool = False, color: str | None = BLACK) -> str:
    return run(text, size=PT(size_pt), bold=bold or None, italic=italic or None, color=color, font=FONT)


def _empty_centered_para() -> str:
    return paragraph([], align="ctr", line_spacing=100_000)


def _tight_para(runs, *, align=None, zero_margins: bool = True) -> str:
    kwargs = {"align": align, "line_spacing": 100_000}
    if zero_margins:
        kwargs.update({"mar_l": 0, "indent": 0})
    return paragraph(runs, **kwargs)


def _label_box(ids: ShapeIds, label: LabelBox) -> str:
    return text_box(
        ids.next(),
        label.name,
        *label.box.emu(),
        [
            _tight_para(
                [_r(label.text, size_pt=label.font_pt, bold=label.bold, italic=label.italic, color=label.color)],
                align=label.align,
                zero_margins=label.zero_margins,
            )
        ],
        fill=label.fill,
        line_color="none",
        anchor=label.anchor,
        wrap=label.wrap,
        vert=label.vert,
        l_ins=0 if label.zero_margins else None,
        t_ins=0 if label.zero_margins else None,
        r_ins=0 if label.zero_margins else None,
        b_ins=0 if label.zero_margins else None,
    )


def _draw_rule(ids: ShapeIds, rule: Rule) -> str:
    return connector(
        ids.next(),
        rule.name,
        IN(rule.x),
        IN(rule.y),
        IN(rule.w),
        IN(rule.h),
        color=rule.color,
        width=rule.width,
        dashed=rule.dashed,
        dash=rule.dash,
        arrow=rule.arrow,
        grad=list(rule.grad) if rule.grad else None,
        grad_angle=rule.grad_angle,
    )


def _hyperlink_hotspot(ids: ShapeIds, hotspot: SourceHotspot) -> str:
    """Transparent shape-level link target; it renders invisibly."""

    x, y, w, h = hotspot.box.emu()
    sp_id = ids.next()
    name = esc(hotspot.name)
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="{name}">'
        f'<a:hlinkClick r:id="{hotspot.r_id}"/></p:cNvPr>'
        '<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        '<a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        '<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="en-US"/></a:p></p:txBody></p:sp>'
    )


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════


def paint_preliminary_chip(out: list[str], ids: ShapeIds) -> None:
    """Source-exact Preliminary chip dimensions from the reference deck."""

    out.append(
        text_box(
            4,
            "PrelimChip",
            *PRELIM_CHIP_EMU,
            [paragraph([run("Preliminary", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100_000)],
            fill=PRELIM,
            line_color=BLACK,
            line_width=19_050,
            anchor="ctr",
            wrap="square",
            l_ins=45_720,
            t_ins=9_144,
            r_ins=45_720,
            b_ins=9_144,
        )
    )

def paint_chrome_and_scenario(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            "ScenarioChip",
            *SCENARIO_CHIP.box.emu(),
            [paragraph([run(SCENARIO_CHIP.text, size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100_000)],
            fill=SCENARIO_CHIP.fill,    # 447BB2 = theme bg2 @ 50% lum (reference chip fill)
            line_color=BLACK,
            line_width=19050,           # 1.5pt — reference chip border (theme lnRef idx=2)
            anchor="ctr",
        )
    )


def paint_chart(out: list[str], ids: ShapeIds) -> None:
    out.append(
        graphic_frame(
            sp_id=ids.next(),
            name="Chart",
            x=IN(CHART_FRAME.x),
            y=IN(CHART_FRAME.y),
            cx=IN(CHART_FRAME.w),
            cy=IN(CHART_FRAME.h),
            rId="rId2",
        )
    )


def paint_reference_markers(out: list[str], ids: ShapeIds) -> None:
    for marker in REFERENCE_MARKERS:
        out.append(
            text_box(
                ids.next(),
                "LegendGlyphKey",
                IN(RIGHT_ARROW_MARK.box.x),
                IN(marker.y),
                IN(RIGHT_ARROW_MARK.box.w),
                IN(RIGHT_ARROW_MARK.box.h),
                [_empty_centered_para()],
                fill=DK,
                line_color="none",
                prst="rightArrow",
                geom_adj={"adj1": "val 100000", "adj2": "val 100000"},
                anchor="ctr",
                rot=10_800_000,
            )
        )


def paint_initial_phase_rules(out: list[str], ids: ShapeIds) -> None:
    for rule in INITIAL_PHASE_RULES:
        out.append(_draw_rule(ids, rule))


def paint_year_ticks(out: list[str], ids: ShapeIds) -> None:
    for tick in YEAR_TICKS:
        label = LabelBox(
            YEAR_TICK_ZONE.name,
            Box(tick.x, YEAR_TICK_ZONE.box.y, YEAR_TICK_ZONE.box.w, YEAR_TICK_ZONE.box.h),
            tick.label,
            font_pt=YEAR_TICK_ZONE.font_pt,
            align="r",
            vert="vert270",   # source year ticks are rotated 270 (read bottom-to-top)
        )
        out.append(_label_box(ids, label))


def paint_axis_titles(out: list[str], ids: ShapeIds) -> None:
    # Right cap has a separate footnote run in the source.
    out.append(
        text_box(
            ids.next(),
            "RightAxisCapLabel",
            *AXIS_RIGHT_CAP.box.emu(),
            [
                paragraph(
                    [
                        run("10M GT", size=PT(10), color=BLACK, font=FONT),
                        run("1", size=PT(10), color=BLACK, font=FONT),
                    ],
                    mar_l=0,
                    indent=0,
                    line_spacing=100_000,
                )
            ],
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
    out.append(_label_box(ids, AXIS_TITLE))


def paint_reference_labels_and_mid_rules(out: list[str], ids: ShapeIds) -> None:
    for label in REFERENCE_LABELS:
        out.append(_label_box(ids, label))
    for rule in MID_LEGEND_RULES:
        out.append(_draw_rule(ids, rule))


def paint_legend_panel_and_keys(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            LEGEND_PANEL.name,
            *LEGEND_PANEL.box.emu(),
            [_empty_centered_para()],
            fill=LEGEND_PANEL.fill,
            line_color="none",
            anchor="ctr",
        )
    )
    for key in SOLID_LEGEND_KEYS:
        out.append(
            text_box(
                ids.next(),
                key.name,
                *key.box.emu(),
                [_empty_centered_para()],
                fill=key.fill,
                line_color="none",
                anchor="ctr",
            )
        )
    out.append(
        text_box(
            ids.next(),
            "HeritageTargetPatternKey",
            *HERITAGE_LEGEND_KEY.box.emu(),
            [_empty_centered_para()],
            fill=None,
            line_color="none",
            pattern_fill=HERITAGE_LEGEND_KEY.pattern,
            anchor="ctr",
        )
    )


def paint_legend_labels(out: list[str], ids: ShapeIds) -> None:
    # The white legend panel is a real shape, so text must be painted after it
    # or the panel hides the legend labels. This mirrors the source slide order.
    for label in LEGEND_LABELS:
        out.append(_label_box(ids, label))


def paint_late_rules_and_scale(out: list[str], ids: ShapeIds) -> None:
    for rule in LATE_PHASE_RULES[:3]:
        out.append(_draw_rule(ids, rule))
    # Paint the confidence arrow BEFORE its labels so the white "Confidence level"
    # box (and Lower/Higher) sit on top of the arrow, matching source paint order.
    out.append(_draw_rule(ids, CONFIDENCE_SCALE_ARROW))
    for label in SCALE_LABELS:
        # Source scale labels intentionally retain default text-box insets.
        out.append(
            text_box(
                ids.next(),
                "ConfidenceScaleLabel",
                *label.box.emu(),
                [paragraph([_r(label.text, size_pt=8, italic=True)], align="ctr", line_spacing=100_000)],
                fill=label.fill,
                line_color="none",
                anchor="ctr",
            )
        )
    out.append(_draw_rule(ids, LATE_PHASE_RULES[3]))


# Reference drop-shadow on the light-blue callout (outerShdw, verbatim params from
# the source deck): 0.056" blur, 0.03" offset down-right, black @ 40% alpha.
CALLOUT_SHADOW = (
    '<a:effectLst><a:outerShdw blurRad="50800" dist="38100" dir="2700000" '
    'algn="tl" rotWithShape="0"><a:prstClr val="black"><a:alpha val="40000"/>'
    '</a:prstClr></a:outerShdw></a:effectLst>'
)


def paint_capacity_and_summary(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            CAPACITY_CAPTION.name,
            *CAPACITY_CAPTION.box.emu(),
            [
                paragraph(
                    [_r(CAPACITY_CAPTION.text, size_pt=CAPACITY_CAPTION.font_pt, bold=CAPACITY_CAPTION.bold, color=CAPACITY_CAPTION.color)],
                    align="ctr",
                    line_spacing=100_000,
                )
            ],
            fill=CAPACITY_CAPTION.fill,
            line_color=CAPACITY_CAPTION.line_color,
            prst=CAPACITY_CAPTION.prst,
            geom_adj=CAPACITY_CAPTION.geom_adj,
            anchor="ctr",
            effects=CALLOUT_SHADOW,
        )
    )
    out.append(
        text_box(
            ids.next(),
            "SummaryCaption",
            *SUMMARY_CAPTION.box.emu(),
            [paragraph([_r(SUMMARY_CAPTION.text, bold=True, italic=True)], line_spacing=100_000)],
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


def paint_callouts(out: list[str], ids: ShapeIds) -> None:
    for callout in CALLOUTS:
        out.append(
            text_box(
                ids.next(),
                callout.name,
                *callout.box.emu(),
                [
                    paragraph(
                        [_r(callout.text, size_pt=callout.font_pt, bold=callout.bold, italic=callout.italic, color=callout.color)],
                        align="ctr",
                        line_spacing=100_000,
                    )
                ],
                fill=callout.fill,
                line_color=callout.line_color,
                prst=callout.prst,
                geom_adj=callout.geom_adj,
                anchor="ctr",
            )
        )


def paint_source_note(out: list[str], ids: ShapeIds) -> None:
    out.append(source_note(SOURCE_NOTE.text(), y=SOURCE_NOTE_Y))
    for hotspot in SOURCE_HOTSPOTS:
        out.append(_hyperlink_hotspot(ids, hotspot))


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # Paint order matters in PowerPoint OOXML: later elements sit on top.
    paint_preliminary_chip(out, ids)
    paint_chrome_and_scenario(out, ids)
    paint_chart(out, ids)
    paint_reference_markers(out, ids)
    paint_initial_phase_rules(out, ids)
    paint_year_ticks(out, ids)
    paint_axis_titles(out, ids)
    paint_reference_labels_and_mid_rules(out, ids)
    paint_legend_panel_and_keys(out, ids)
    paint_legend_labels(out, ids)
    paint_late_rules_and_scale(out, ids)
    paint_capacity_and_summary(out, ids)
    paint_callouts(out, ids)
    paint_source_note(out, ids)

    return "".join(out)


CHROME = Chrome(
    section=TITLE_SECTION,
    topic=TITLE_TOPIC,
    title=TITLE_HEAD,
    takeaway=TITLE_TAKEAWAY,
    preliminary=False,  # painted manually to match source-deck chip geometry exactly
)


def render() -> str:
    return body_slide(CHROME, _body())
