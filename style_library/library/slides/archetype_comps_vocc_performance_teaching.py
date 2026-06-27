"""Teaching exemplar: archetype-comparison bubble chart with narrative rail.

ROLE
  archetype_comparison / performance_bubble_chart

USE WHEN
  A slide needs to compare performance behavior across several business
  archetypes using one style-dense bubble chart, an external archetype legend,
  and a right-hand commentary rail that explains the drivers behind the plotted
  movement.

TEACHES
  - when to preserve a source bubble chart with `editable_bundled_chart(...)`
  - documenting an opaque bubble-chart template contract without hiding it in
    converter-era `_CHART0_DATA = [{"values": []}, ...]` noise
  - manual x-axis year ticks below a template chart
  - manual y-axis title outside the chart frame
  - mixed legend grammar: solid archetype dots, a patterned archetype dot, and
    a revenue bubble-size ring
  - dense no-fill narrative rail with bold archetype heads and hanging bullets
  - single-cell table used as a rail title band
  - compact off-house source note with colored constituent labels

TEXT-FIT PRECEDENT
  narrative_rail:
    geometry: 3.136in wide x 4.870in high
    type: Arial 10pt, black, 100% line spacing
    content: 4 archetype section heads + 7 hanging bullets
    copy_when: the chart carries the comparative evidence and the rail explains
               mechanism/timing rather than adding a second exhibit

  manual_legend:
    geometry: 2.4in wide x 1.5in high, below/right of plot area
    type: Arial 10pt, no-wrap labels
    content: 5 archetype marks plus one revenue bubble-size key
    copy_when: the chart template is too style-dense or semantically overloaded
               for a native chart legend

  source_note:
    geometry: 5.102in wide x 0.349in high
    type: Arial 7pt with colored bold archetype labels
    content: one dense constituent-company source line
    copy_when: source detail is needed but cannot occupy the house source band

SOURCE NOTE
  Teaching rewrite of the source-faithful `archetype_comps_vocc_performance.py`
  module. The provided `slide33_chart18.xml` + `slide33_chart18.xlsb` pair is
  preserved as the editable chart template because the chart is a think-cell-like
  bubble chart with many per-point styles and no simple native factory analogue.
  The surrounding slide contract (`LAYOUT`, `CHARTS`, `_body()`, `render()`),
  visible coordinates, legend, right rail, footnote, and chrome are preserved.

FIDELITY NOTE
  This is a practical teaching rewrite, not a byte-identical source port. It keeps
  the chart XML/workbook pair for visual fidelity and PowerPoint Edit Data support.
  The chart's bubble data remains in the chart cache/workbook; the module exposes
  a semantic template contract so future authors know why the chart is opaque and
  which manual labels/legend/rail belong outside the chart frame.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deck_core.authoring import (
    IN,
    PT,
    BLACK,
    WHITE,
    DK,
    FONT,
    slide,
    run,
    paragraph,
    text_box,
    table,
    trow,
    tpara,
    trun,
    breadcrumb,
    title_placeholder,
    prelim_chip,
    graphic_frame,
    editable_bundled_chart,
    edge,
    rcell,
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
    "role": "archetype_comparison / performance_bubble_chart",
    "use_when": (
        "Use when a slide compares performance across business archetypes with "
        "a style-dense bubble chart, where marker position shows margin, bubble "
        "size shows revenue, and the right rail explains period-specific drivers."
    ),
    "teaches": [
        "template-backed editable bubble chart",
        "opaque chart-cache contract documented in Python",
        "manual year ticks over a bubble chart",
        "manual y-axis title outside the chart frame",
        "external legend for marker color, hatch pattern, and bubble size",
        "dense narrative rail with section heads and hanging bullets",
        "single-cell table as rail header",
        "compact colored source note",
    ],
    "source_module": "archetype_comps_vocc_performance.py",
    "source_chart_assets": ("slide33_chart18.xml", "slide33_chart18.xlsb"),
    "rebuild_strategy": "preserve bubble chart as editable_bundled_chart template",
}

TEXT_FIT = {
    "narrative_rail": {
        "box_in": (3.136, 4.870),
        "font_pt": 10,
        "content": "4 heads + 7 bullets with bold time-period labels",
        "note": "Works because prose is sentence-fragment style, not full paragraphs.",
    },
    "rail_header": {
        "box_in": (3.135, 0.300),
        "font_pt": 10,
        "content": "Revenue and EBIT margin drivers",
        "note": "Single-cell table gives exact top/bottom rule behavior.",
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
    },
    "source_note": {
        "box_in": (5.102, 0.349),
        "font_pt": 7,
        "content": "one dense constituent-company source line",
    },
}

COPY_RULES = [
    "Keep a bubble chart template-backed when the important precedent is marker size + per-point styling; do not force it into a line or column factory.",
    "Use the slide-level legend as the semantic contract when the chart template groups points by internal cache buckets instead of clean archetype series.",
    "Use a right commentary rail when the chart explains what happened and the rail explains why it happened.",
    "Do not place long narrative inside the chart area; reserve the plot for markers, axis ticks, and a compact legend.",
    "A colored source note can carry constituent detail when a full appendix table would overtake the slide.",
]

CHART_TEMPLATE_CONTRACT = {
    "why_editable_bundled_chart": (
        "The chart is a bubbleChart with seven internal template series, many "
        "per-point styles, marker sizes tied to revenue, and no native factory "
        "surface in this deck_core pipeline. The chart cache/workbook therefore "
        "remain the data source of truth."
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
        "bubble_scale": 66,
        "x_axis_min_max": (2019, 2025),
        "y_axis_min_max": (-50, 70),
    },
    "manual_shapes": (
        "year ticks, EBIT Margin y-axis title, archetype legend, revenue ring key, "
        "right narrative rail, rail header, source note, and preliminary chip"
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
class NarrativeBullet:
    """One hanging bullet in the commentary rail."""

    prefix: str | None
    text: str


@dataclass(frozen=True)
class NarrativeSection:
    """Section head plus bullets for the right rail."""

    title: str
    qualifier: str | None
    bullets: tuple[NarrativeBullet, ...]


@dataclass(frozen=True)
class SourceRun:
    """A run in the compact colored source note."""

    text: str
    color: str = BLACK
    bold: bool = False


# ════════════════════════════════════════════════════════════════════════════
# Layout zones. These names are the teaching surface.
# ════════════════════════════════════════════════════════════════════════════
CHART_FRAME = Box(0.373, 1.696, 9.286, 5.200)
Y_AXIS_TITLE = Box(0.533, 1.505, 1.064, 0.167)
YEAR_TICK_Y = 6.736
YEAR_TICK_SIZE = (0.306, 0.167)
LEGEND_LABEL_H = 0.167
NARRATIVE_RAIL = Box(9.660, 1.866, 3.136, 4.870)
NARRATIVE_HEADER = Box(9.660, 1.563, 3.135, 0.300)
SOURCE_NOTE = Box(0.495, 7.081, 5.102, 0.349)


# ════════════════════════════════════════════════════════════════════════════
# Chart template semantics. The source workbook has no header row; the chart XML
# uses paired cache columns for y-values and bubble sizes. This table records the
# implementation contract without trying to flatten all 73 points into Python.
# ════════════════════════════════════════════════════════════════════════════
BUBBLE_TEMPLATE_SERIES: tuple[BubbleTemplateSeries, ...] = (
    BubbleTemplateSeries(0, 3, f"solid {SHIPBUILDER_RED}", "A / B / C", "template bucket with red default marker"),
    BubbleTemplateSeries(1, 12, f"solid {OWNER_OPERATOR_BLUE}", "A / D / E", "template bucket with owner/operator default marker"),
    BubbleTemplateSeries(2, 20, f"solid {CHARTER_GREEN}", "A / F / G", "template bucket with charter-company default marker"),
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


# ════════════════════════════════════════════════════════════════════════════
# Manual labels and legend entries copied from source slide coordinates.
# ════════════════════════════════════════════════════════════════════════════
YEAR_TICKS: tuple[YearTick, ...] = tuple(
    YearTick(Box(x, YEAR_TICK_Y, *YEAR_TICK_SIZE), label)
    for x, label in (
        (2.130, "2020"),
        (3.589, "2021"),
        (5.045, "2022"),
        (6.502, "2023"),
        (7.960, "2024"),
    )
)

LEGEND_ENTRIES: tuple[LegendEntry, ...] = (
    LegendEntry(
        "Shipbuilders",
        "solid_archetype_dot",
        Box(7.148, 5.583, 0.146, 0.146),
        Box(7.375, 5.578, 0.760, LEGEND_LABEL_H),
        SHIPBUILDER_RED,
    ),
    LegendEntry(
        "Owner/Operator (Carrier Segment)",
        "solid_archetype_dot",
        Box(7.148, 5.806, 0.146, 0.146),
        Box(7.375, 5.800, 2.139, LEGEND_LABEL_H),
        OWNER_OPERATOR_BLUE,
    ),
    LegendEntry(
        "Charter Companies",
        "solid_archetype_dot",
        Box(7.148, 6.028, 0.146, 0.146),
        Box(7.375, 6.023, 1.200, LEGEND_LABEL_H),
        CHARTER_GREEN,
    ),
    LegendEntry(
        "Terminal Operators (Integrated)",
        "solid_archetype_dot",
        Box(7.148, 6.250, 0.146, 0.146),
        Box(7.375, 6.245, 1.944, LEGEND_LABEL_H),
        TERMINAL_INTEGRATED_BLUE,
    ),
    LegendEntry(
        "Terminal Operators (Standalone)",
        "hatched_archetype_dot",
        Box(7.148, 6.472, 0.146, 0.146),
        Box(7.375, 6.467, 2.021, LEGEND_LABEL_H),
        None,
        pattern_fill={"prst": "pct50", "fg": "scheme:tx1", "bg": "scheme:bg1"},
    ),
    LegendEntry(
        "$10B (Revenue)",
        "revenue_bubble_ring",
        Box(7.066, 5.139, 0.326, 0.326),
        Box(7.450, 5.224, 1.005, LEGEND_LABEL_H),
        None,
    ),
)

NARRATIVE_SECTIONS: tuple[NarrativeSection, ...] = (
    NarrativeSection(
        "Shipbuilders",
        "(relating to Commercial market)",
        (
            NarrativeBullet("’21-’22:", "While orders recovered from ’20, earnings remained pressured by input materials and labor cost growth."),
            NarrativeBullet("’23-’24:", "Improvement driven by performance against orderbook contracts and rising new build prices"),
        ),
    ),
    NarrativeSection(
        "Owner/Operators",
        None,
        (
            NarrativeBullet("’21-’22:", "Freight rates reached historic highs driven by post-COVID pent-up demand and shift toward goods consumption, while port congestion and operational disruptions constrained effective vessel supply amid below-trend capacity additions."),
            NarrativeBullet("’23-’24:", "Freight rates normalized as consumer demand softened under inflationary pressure, coinciding with acceleration in new vessel deliveries that expanded global fleet capacity."),
        ),
    ),
    NarrativeSection(
        "Charter Companies",
        None,
        (
            NarrativeBullet("’21-’22:", "Charter rates surged alongside freight rates as operators sought to secure tonnage in supply-constrained market."),
            NarrativeBullet("’23-’24:", "Earnings remained supported by multi-year charter contracts signed at peak market conditions ’21-’22, partially insulating results from lower charter rates."),
        ),
    ),
    NarrativeSection(
        "Terminal Operators",
        None,
        (
            NarrativeBullet(None, "Relatively more stable margins given ability to pass on costs to operators."),
        ),
    ),
)

SOURCE_RUNS: tuple[SourceRun, ...] = (
    SourceRun("Source: Company filings |   "),
    SourceRun("Shipbuilders:", SHIPBUILDER_RED, True),
    SourceRun(" Austal, Hanwha Ocea, Fincantieri, HD Hyundai KSOE, Samsung Heavy. "),
    SourceRun("Owner/Operator", OWNER_OPERATOR_BLUE, True),
    SourceRun(": Matson OT segment, ZIM, Hapag Lloyd, Maersk Ocean segment. "),
    SourceRun("Charter Companies", CHARTER_GREEN, True),
    SourceRun(": Danaos, "),
    SourceRun("Costamare"),
    SourceRun(", Seaspan. "),
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


_CHART_TEMPLATE_XML = _asset_path("slide33_chart18.xml").read_text(encoding="utf-8")
_CHART_WORKBOOK_BYTES = _asset_path("slide33_chart18.xlsb").read_bytes()

CHARTS = [editable_bundled_chart(_CHART_TEMPLATE_XML, _CHART_WORKBOOK_BYTES, embed_ext="xlsb")]


# ════════════════════════════════════════════════════════════════════════════
# Validation helpers. These keep the manual teaching contract synchronized with
# the preserved template chart and the surrounding slide furniture.
# ════════════════════════════════════════════════════════════════════════════
def _validate_semantics() -> None:
    if len(BUBBLE_TEMPLATE_SERIES) != CHART_TEMPLATE_CONTRACT["template_chart_xml"]["internal_series_count"]:
        raise ValueError("Bubble chart template contract expects seven internal series buckets.")
    if "<c:bubbleChart" not in _CHART_TEMPLATE_XML:
        raise ValueError("slide33_chart18.xml must contain a bubbleChart template.")
    if _CHART_TEMPLATE_XML.count("<c:ser>") != len(BUBBLE_TEMPLATE_SERIES):
        raise ValueError("BUBBLE_TEMPLATE_SERIES no longer matches the chart XML series count.")
    if sum(series.point_count for series in BUBBLE_TEMPLATE_SERIES) != 73:
        raise ValueError("Bubble chart point-count contract should total 73 source workbook rows.")
    if tuple(tick.label for tick in YEAR_TICKS) != ("2020", "2021", "2022", "2023", "2024"):
        raise ValueError("Manual year ticks should remain the five source years.")
    if len(LEGEND_ENTRIES) != 6:
        raise ValueError("Legend should include five archetype markers plus one revenue-size ring.")


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


def _narrative_head(section: NarrativeSection) -> str:
    runs = [run(section.title, size=PT(10), bold=True, color=BLACK, font=FONT)]
    if section.qualifier:
        runs.append(run(" ", size=PT(10), color=BLACK, font=FONT))
        runs.append(run(section.qualifier, size=PT(10), italic=True, color=BLACK, font=FONT))
    return paragraph(runs, line_spacing=100000)


def _narrative_bullet(bullet: NarrativeBullet) -> str:
    runs = []
    if bullet.prefix:
        runs.append(run(bullet.prefix, size=PT(10), bold=True, color=BLACK, font=FONT))
        runs.append(run(" ", size=PT(10), color=BLACK, font=FONT))
    runs.append(run(bullet.text, size=PT(10), color=BLACK, font=FONT))
    return paragraph(runs, mar_l=171450, indent=-171450, line_spacing=100000, bullet=True)


def _narrative_paragraphs() -> list[str]:
    paras: list[str] = []
    for section in NARRATIVE_SECTIONS:
        paras.append(_narrative_head(section))
        paras.extend(_narrative_bullet(bullet) for bullet in section.bullets)
    return paras


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
# preserved bubble chart, manual axis furniture, legend, right rail, source note,
# and the Preliminary chip.
# ════════════════════════════════════════════════════════════════════════════
def paint_chrome(next_id) -> list[str]:
    """House chrome for the value-chain performance section."""

    return [
        breadcrumb("Commercial Maritime Value Chain", "Performance"),
        title_placeholder(
            "Archetype Comps (2/3)",
            "VOCC performance ’21-’22 driven by historically high freight rates; charter companies benefitted through ’24 from leases locked in ’21-’22.",
        ),
    ]


def paint_template_bubble_chart(next_id) -> list[str]:
    """Opaque but editable bubble chart: position = margin, size = revenue."""

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
    # Paint the revenue-size ring with the solid dots, matching the source order.
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


def paint_narrative_rail(next_id) -> list[str]:
    """Right rail explaining the margin drivers by archetype and period."""

    return [
        _textbox(
            next_id(),
            "RevenueAndMarginDriversRail",
            NARRATIVE_RAIL,
            _narrative_paragraphs(),
            fill=None,
            line_color="none",
        )
    ]


def paint_narrative_header(next_id) -> list[str]:
    """Single-cell table header for the right narrative rail."""

    return [
        table(
            next_id(),
            "RevenueAndMarginDriversHeader",
            *NARRATIVE_HEADER.emu(),
            col_widths=[IN(NARRATIVE_HEADER.w)],
            rows=[
                trow(
                    [
                        rcell(
                            [
                                tpara(
                                    [trun("Revenue and EBIT margin drivers", size=PT(10), bold=True, color=BLACK, font=FONT)],
                                    mar_l=0,
                                    indent=0,
                                )
                            ],
                            l_ins=41564,
                            r_ins=41564,
                            T=edge(WHITE),
                            B=edge(BLACK),
                        )
                    ],
                    h=IN(NARRATIVE_HEADER.h),
                )
            ],
        )
    ]


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
    shapes.extend(paint_narrative_rail(next_id))
    shapes.extend(paint_narrative_header(next_id))
    shapes.extend(paint_source_note(next_id))
    shapes.extend(paint_preliminary_chip(next_id))
    return "".join(shapes)


def render() -> str:
    return slide(_body())
