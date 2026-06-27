"""Teaching exemplar: archetype-comparison bubble chart with external legend.

ROLE
  archetype_comparison / margin_recovery_timeline

USE WHEN
  A slide needs one large style-dense performance chart, a compact manual
  archetype legend, and a constituent-company source note, but does NOT need a
  narrative rail. This is the cleaner, chart-dominant sibling of the VOCC
  performance teaching exemplar.

TEACHES
  - when to preserve a source bubble chart with `editable_bundled_chart(...)`
  - documenting an opaque chart-template contract without hiding it behind
    converter-era empty `_CHART0_DATA` series
  - full-width bubble-chart placement for a chart-only archetype comparison
  - manual year ticks below a template chart
  - manual y-axis title outside the chart frame
  - mixed legend grammar: solid archetype dots, a patterned archetype dot, and
    a revenue bubble-size ring
  - compact off-house source note with colored constituent labels
  - preserving a pristine source chart while making the slide module readable to
    an AI author

TEXT-FIT PRECEDENT
  chart_dominant_body:
    geometry: 12.540in wide x 5.200in high
    type: editable bundled bubble chart plus external labels
    content: 73 chart points across 2020-2024, encoded by x/y/bubble-size/color
    copy_when: the chart itself is the exhibit and the surrounding text should be
               limited to axis title, legend, and source detail

  manual_legend:
    geometry: approx. 2.46in wide x 1.50in high, bottom-right of chart body
    type: Arial 10pt no-wrap labels
    content: 5 archetype marks plus one $10B revenue bubble-size key
    copy_when: native chart legend is too opaque or template-driven to explain
               marker color, pattern, and size clearly

  source_note:
    geometry: 5.102in wide x 0.349in high
    type: Arial 7pt with colored bold archetype labels
    content: one dense constituent-company source line
    copy_when: source/constituent detail is important but should not occupy the
               locked house source band

SOURCE NOTE
  Teaching rewrite of the source-faithful `archetype_comps_newbuild_prices.py`
  module. The provided `slide32_chart17.xml` + `slide32_chart17.xlsb` pair is
  preserved as the editable chart template because the source chart is a
  think-cell-like bubble chart with per-point styles, revenue-scaled marker
  sizing, and no clean native chart-factory analogue. The surrounding slide
  contract (`LAYOUT`, `CHARTS`, `_body()`, `render()`), visible coordinates,
  legend, footnote, and chrome are preserved.

FIDELITY NOTE
  This is a practical teaching rewrite, not a byte-identical source port. It
  keeps the chart XML/workbook pair for visual fidelity and PowerPoint Edit Data
  support. The chart data remains in the chart cache/workbook; the module exposes
  a semantic template contract so future authors understand why the chart is
  opaque and which manual labels/legend/source-note belong outside the chart
  frame.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deck_core.authoring import (
    IN,
    PT,
    BLACK,
    DK,
    FONT,
    slide,
    run,
    paragraph,
    text_box,
    breadcrumb,
    title_placeholder,
    prelim_chip,
    graphic_frame,
    editable_bundled_chart,
)

LAYOUT = "slideLayout4"

# Local semantic palette. These are value-chain archetype colors, not house
# chrome colors. Keep them explicit so an authoring agent can copy the legend.
SHIPBUILDER_RED = "C30C3E"
OWNER_OPERATOR_BLUE = "364D6E"
CHARTER_GREEN = "27AE60"
TERMINAL_INTEGRATED_BLUE = "6F8DB9"
TERMINAL_STANDALONE_GRAY = "8A8F93"


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: small programmatic index for retrieval / agent search.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "archetype_comparison / margin_recovery_timeline",
    "use_when": (
        "Use when a slide compares margin behavior across value-chain "
        "archetypes with one full-width, style-dense bubble chart and a "
        "manual legend, rather than a chart-plus-commentary-rail layout."
    ),
    "teaches": [
        "template-backed editable bubble chart",
        "opaque chart-cache contract documented in Python",
        "full-width chart-dominant layout",
        "manual year ticks over a bubble chart",
        "manual y-axis title outside the chart frame",
        "external legend for marker color, hatch pattern, and bubble size",
        "compact colored source note",
    ],
    "source_module": "archetype_comps_newbuild_prices.py",
    "source_chart_assets": ("slide32_chart17.xml", "slide32_chart17.xlsb"),
    "rebuild_strategy": "preserve source bubble chart as editable_bundled_chart template",
}

TEXT_FIT = {
    "chart_frame": {
        "box_in": (12.540, 5.200),
        "content": "template chart with 73 bubble points and no text rail",
        "note": "The chart can span almost the full body because all explanation is externalized to legend + title.",
    },
    "manual_year_ticks": {
        "box_in": (0.306, 0.167),
        "font_pt": 10,
        "content": "four-digit year tick; five ticks only",
    },
    "legend_labels": {
        "box_in": "0.760-2.139 wide x 0.167 high",
        "font_pt": 10,
        "content": "no-wrap archetype captions",
        "note": "Longest label fits because it starts at x=10.601in and uses a 2.139in box.",
    },
    "source_note": {
        "box_in": (5.102, 0.349),
        "font_pt": 7,
        "content": "one dense constituent-company source line",
    },
}

COPY_RULES = [
    "Keep the chart template-backed when the important precedent is marker size plus per-point styling; do not force it into a native line/column factory.",
    "Use a full-width chart frame when the chart is the evidence and no explanatory right rail is needed.",
    "Use the slide-level legend as the semantic contract when the chart template groups points by cache bucket rather than clean archetype series.",
    "Keep manual ticks and y-axis title outside the chart when the source chart template hides or suppresses native labels.",
    "Use a colored source note for constituent detail when a full appendix table would overtake the exhibit.",
]

CHART_TEMPLATE_CONTRACT = {
    "why_editable_bundled_chart": (
        "The chart is a bubbleChart with seven internal template series, many "
        "per-point styles, and revenue-scaled bubble sizes. The chart cache and "
        "workbook therefore remain the data source of truth."
    ),
    "visible_encoding": {
        "x": "calendar year, 2020-2024",
        "y": "EBIT margin (%)",
        "bubble_size": "revenue, with $10B shown by the external ring key",
        "marker_color": "value-chain archetype",
    },
    "template_chart_xml": {
        "chart_type": "bubbleChart",
        "internal_series_count": 7,
        "point_count": 73,
        "bubble_scale": 66,
        "x_axis_min_max": (2019, 2025),
        "y_axis_min_max": (-50, 70),
    },
    "manual_shapes": (
        "year ticks, EBIT Margin y-axis title, archetype legend, revenue ring key, "
        "compact source note, and Preliminary chip"
    ),
}


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
class BubbleTemplateSeries:
    """One internal series bucket in the preserved bubble-chart template.

    These buckets are a chart-template implementation detail, not the external
    legend. Some archetype colors are applied through per-point overrides in the
    chart XML, so the external legend remains the semantic source for authors.
    """

    order: int
    point_count: int
    default_style: str
    cache_columns: str
    note: str


@dataclass(frozen=True)
class YearTick:
    """Manual x-axis tick under the chart template."""

    box: Box
    label: str


@dataclass(frozen=True)
class LegendEntry:
    """One external legend entry beside/below the plot area."""

    label: str
    marker: str
    marker_box: Box
    label_box: Box
    fill: str | None
    line_color: str = DK
    pattern_fill: dict | None = None


@dataclass(frozen=True)
class SourceRun:
    """A run in the compact colored source note."""

    text: str
    color: str = BLACK
    bold: bool = False


@dataclass(frozen=True)
class ChartReading:
    """Human reading encoded for the teaching corpus; not painted."""

    observation: str
    authoring_use: str


# ════════════════════════════════════════════════════════════════════════════
# Layout zones. These names are the teaching surface.
# ════════════════════════════════════════════════════════════════════════════
CHART_FRAME = Box(0.373, 1.696, 12.540, 5.200)
Y_AXIS_TITLE = Box(0.533, 1.505, 1.064, 0.167)
YEAR_TICK_Y = 6.736
YEAR_TICK_SIZE = (0.306, 0.167)
LEGEND_ZONE = Box(10.283, 5.139, 2.457, 1.500)
LEGEND_LABEL_H = 0.167
SOURCE_NOTE = Box(0.495, 7.081, 5.102, 0.349)


# ════════════════════════════════════════════════════════════════════════════
# Chart template semantics. The source workbook has no header row; the chart XML
# uses paired cache columns for y-values and bubble sizes. This table records the
# implementation contract without trying to flatten all 73 points into Python.
# ════════════════════════════════════════════════════════════════════════════
BUBBLE_TEMPLATE_SERIES: tuple[BubbleTemplateSeries, ...] = (
    BubbleTemplateSeries(0, 3, f"solid {SHIPBUILDER_RED}", "A / B / C", "template bucket with red default marker"),
    BubbleTemplateSeries(1, 12, f"solid {OWNER_OPERATOR_BLUE}", "A / D / E", "template bucket with owner/operator default marker and red point overrides"),
    BubbleTemplateSeries(2, 20, f"solid {CHARTER_GREEN}", "A / F / G", "template bucket with charter default marker and multiple point overrides"),
    BubbleTemplateSeries(3, 15, f"solid {OWNER_OPERATOR_BLUE}", "A / H / I", "template bucket with per-point overrides"),
    BubbleTemplateSeries(4, 14, "pct50 hatch", "A / J / K", "template bucket for standalone terminal-operator hatch behavior"),
    BubbleTemplateSeries(5, 6, f"solid {SHIPBUILDER_RED}", "A / L / M", "template bucket with per-point overrides"),
    BubbleTemplateSeries(6, 3, f"solid {SHIPBUILDER_RED}", "A / N / O", "template bucket with per-point overrides"),
)

# Legacy-shape mirror for agents/tools that expect the converted-slide dict
# shape. It is deliberately not passed to CHARTS: bubble data lives inside the
# source XML/workbook and is preserved via editable_bundled_chart.
_CHART0_DATA = {
    "categories": None,
    "series": [{"values": []} for _ in BUBBLE_TEMPLATE_SERIES],
}

CHART_READINGS: tuple[ChartReading, ...] = (
    ChartReading(
        "Shipbuilder margins recover by 2024 but remain low-to-mid-single-digit.",
        "Use the title for the takeaway; do not add a narrative rail unless the slide needs causality detail.",
    ),
    ChartReading(
        "Revenue bubble size is part of the comparison, so the $10B ring key is mandatory.",
        "Never remove the hollow ring legend when copying this chart grammar.",
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Manual labels and legend entries copied from source slide coordinates.
# ════════════════════════════════════════════════════════════════════════════
YEAR_TICKS: tuple[YearTick, ...] = tuple(
    YearTick(Box(x, YEAR_TICK_Y, *YEAR_TICK_SIZE), label)
    for x, label in (
        (2.674, "2020"),
        (4.672, "2021"),
        (6.672, "2022"),
        (8.672, "2023"),
        (10.670, "2024"),
    )
)

LEGEND_ENTRIES: tuple[LegendEntry, ...] = (
    LegendEntry(
        "Shipbuilders",
        "solid_archetype_dot",
        Box(10.373, 5.583, 0.146, 0.146),
        Box(10.601, 5.578, 0.760, LEGEND_LABEL_H),
        SHIPBUILDER_RED,
    ),
    LegendEntry(
        "Owner/Operator (Carrier Segment)",
        "solid_archetype_dot",
        Box(10.373, 5.806, 0.146, 0.146),
        Box(10.601, 5.800, 2.139, LEGEND_LABEL_H),
        OWNER_OPERATOR_BLUE,
    ),
    LegendEntry(
        "Charter Companies",
        "solid_archetype_dot",
        Box(10.373, 6.028, 0.146, 0.146),
        Box(10.601, 6.023, 1.200, LEGEND_LABEL_H),
        CHARTER_GREEN,
    ),
    LegendEntry(
        "Terminal Operators (Integrated)",
        "solid_archetype_dot",
        Box(10.373, 6.250, 0.146, 0.146),
        Box(10.601, 6.245, 1.944, LEGEND_LABEL_H),
        TERMINAL_INTEGRATED_BLUE,
    ),
    LegendEntry(
        "Terminal Operators (Standalone)",
        "hatched_archetype_dot",
        Box(10.373, 6.472, 0.146, 0.146),
        Box(10.601, 6.467, 2.021, LEGEND_LABEL_H),
        None,
        pattern_fill={"prst": "pct50", "fg": "scheme:tx1", "bg": "scheme:bg1"},
    ),
    LegendEntry(
        "$10B (Revenue)",
        "revenue_bubble_ring",
        Box(10.283, 5.139, 0.326, 0.326),
        Box(10.667, 5.224, 1.005, LEGEND_LABEL_H),
        None,
    ),
)

SOURCE_RUNS: tuple[SourceRun, ...] = (
    SourceRun("Source: Company filings |   "),
    SourceRun("Shipbuilders:", SHIPBUILDER_RED, True),
    SourceRun(" Austal, Hanwha Ocea, Fincantieri, HD Hyundai KSOE, Samsung Heavy. "),
    SourceRun("Owner/Operator", OWNER_OPERATOR_BLUE, True),
    SourceRun(": Matson OT segment, ZIM, Hapag Lloyd, Maersk Ocean segment. "),
    SourceRun("Charter Companies", CHARTER_GREEN, True),
    SourceRun(": Danaos, Costamare, Seaspan. "),
    SourceRun("Terminal Operators (Integrated)", TERMINAL_INTEGRATED_BLUE, True),
    SourceRun(": Maersk Terminals.         "),
    SourceRun("Terminal Operators (Standalone)", TERMINAL_STANDALONE_GRAY, True),
    SourceRun(": Hutchison Ports, ICTS. Note: Segment margins not burdened by corporate"),
)


# ════════════════════════════════════════════════════════════════════════════
# Source chart assets. The zip generated for this teaching module includes these
# files under `_src/`; a same-folder fallback makes sandbox smoke tests simple.
# ════════════════════════════════════════════════════════════════════════════
def _asset_path(filename: str) -> Path:
    here = Path(__file__).parent
    for candidate in (here / "_src" / filename, here / filename):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Missing chart asset {filename!r}; expected it in {here / '_src'}")


_CHART_TEMPLATE_XML = _asset_path("slide32_chart17.xml").read_text(encoding="utf-8")
_CHART_WORKBOOK_BYTES = _asset_path("slide32_chart17.xlsb").read_bytes()

CHARTS = [editable_bundled_chart(_CHART_TEMPLATE_XML, _CHART_WORKBOOK_BYTES, embed_ext="xlsb")]


# ════════════════════════════════════════════════════════════════════════════
# Validation helpers. These keep the manual teaching contract synchronized with
# the preserved template chart and the surrounding slide furniture.
# ════════════════════════════════════════════════════════════════════════════
def _validate_semantics() -> None:
    expected_series = CHART_TEMPLATE_CONTRACT["template_chart_xml"]["internal_series_count"]
    expected_points = CHART_TEMPLATE_CONTRACT["template_chart_xml"]["point_count"]
    if len(BUBBLE_TEMPLATE_SERIES) != expected_series:
        raise ValueError("Bubble chart template contract expects seven internal series buckets.")
    if "<c:bubbleChart" not in _CHART_TEMPLATE_XML:
        raise ValueError("slide32_chart17.xml must contain a bubbleChart template.")
    if _CHART_TEMPLATE_XML.count("<c:ser>") != len(BUBBLE_TEMPLATE_SERIES):
        raise ValueError("BUBBLE_TEMPLATE_SERIES no longer matches the chart XML series count.")
    if sum(series.point_count for series in BUBBLE_TEMPLATE_SERIES) != expected_points:
        raise ValueError("Bubble chart point-count contract should total 73 source workbook rows.")
    if '<c:bubbleScale val="66"' not in _CHART_TEMPLATE_XML:
        raise ValueError("The preserved chart template should keep the source bubble scale of 66.")
    if tuple(tick.label for tick in YEAR_TICKS) != ("2020", "2021", "2022", "2023", "2024"):
        raise ValueError("Manual year ticks should remain the five source years.")
    if len(LEGEND_ENTRIES) != 6:
        raise ValueError("Legend should include five archetype markers plus one revenue-size ring.")
    if next(entry for entry in LEGEND_ENTRIES if entry.marker == "hatched_archetype_dot").pattern_fill is None:
        raise ValueError("Standalone terminal-operator legend entry must keep the pct50 hatch fill.")


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


def _source_paragraph() -> str:
    return paragraph(
        [
            run(src.text, size=PT(7), bold=src.bold or None, color=src.color, font=FONT)
            for src in SOURCE_RUNS
        ],
        line_spacing=100000,
    )


# ════════════════════════════════════════════════════════════════════════════
# Paint functions. Order follows the source's effective stacking: chrome,
# preserved bubble chart, manual axis furniture, legend, source note, and the
# Preliminary chip.
# ════════════════════════════════════════════════════════════════════════════
def paint_chrome(next_id) -> list[str]:
    """House chrome for the value-chain performance section."""

    return [
        breadcrumb("Commercial Maritime Value Chain", "Performance"),
        title_placeholder(
            "Archetype Comps (1/3)",
            "Despite seeing improvement from rising new build prices and increased orders, shipbuilders only achieved low-to-mid-single digit EBIT margins by ‘24.",
        ),
    ]


def paint_template_bubble_chart(next_id) -> list[str]:
    """Opaque but editable bubble chart: x = year, y = margin, size = revenue."""

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


def paint_manual_axis_labels(next_id) -> list[str]:
    """Five manual year ticks plus the outside y-axis title."""

    shapes: list[str] = []
    for tick in YEAR_TICKS:
        shapes.append(
            _textbox(
                next_id(),
                "YearLabel",
                tick.box,
                [_one_line(tick.label, align="ctr")],
                fill=None,
                line_color="none",
                wrap="none",
                l_ins=0,
                t_ins=0,
                r_ins=0,
                b_ins=0,
            )
        )
    shapes.append(
        _textbox(
            next_id(),
            "YAxisTitle",
            Y_AXIS_TITLE,
            [_one_line("EBIT Margin (%)", bold=True)],
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
    return shapes


def paint_legend(next_id) -> list[str]:
    """External legend: archetype markers plus revenue bubble-size ring."""

    shapes: list[str] = []
    # Paint solid dots and the revenue-size ring first, then the hatch chip,
    # matching the original source stacking while keeping entries semantic.
    for entry in LEGEND_ENTRIES:
        if entry.marker == "hatched_archetype_dot":
            continue
        shapes.append(
            _textbox(
                next_id(),
                "LegendMarker",
                entry.marker_box,
                [_empty_centered_paragraph()],
                fill=entry.fill,
                line_color=entry.line_color,
                line_width=3175,
                prst="ellipse",
                anchor="ctr",
            )
        )

    hatched = next(entry for entry in LEGEND_ENTRIES if entry.marker == "hatched_archetype_dot")
    shapes.append(
        _textbox(
            next_id(),
            "LegendMarkerHatched",
            hatched.marker_box,
            [_empty_centered_paragraph()],
            fill=None,
            line_color=hatched.line_color,
            pattern_fill=hatched.pattern_fill,
            line_width=3175,
            prst="ellipse",
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
    """Compact source/constituent line retained at the source position."""

    return [
        _textbox(
            next_id(),
            "SourceNote",
            SOURCE_NOTE,
            [_source_paragraph()],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    ]


def paint_preliminary_chip(next_id) -> list[str]:
    """House Preliminary chip, intentionally painted after body content."""

    return [prelim_chip()]


def _body() -> str:
    shapes: list[str] = []
    ids = iter(range(100, 2000))
    next_id = lambda: next(ids)  # noqa: E731 - compact sequential shape ids

    shapes.extend(paint_chrome(next_id))
    shapes.extend(paint_template_bubble_chart(next_id))
    shapes.extend(paint_manual_axis_labels(next_id))
    shapes.extend(paint_legend(next_id))
    shapes.extend(paint_source_note(next_id))
    shapes.extend(paint_preliminary_chip(next_id))
    return "".join(shapes)


def render() -> str:
    return slide(_body())
