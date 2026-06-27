"""Teaching exemplar: fleet-overview composition bar + KPI comparison slide.

ROLE
  scenario_context / fleet_baseline

USE WHEN
  A slide needs one compact exhibit chart on the left and a right-side stack of
  large KPI comparison cards that explains why the chart matters.

TEACHES
  - native editable horizontal bar chart via bar_chart(mode="clustered")
  - per-bar colors using data_point_colors instead of a bundled chart template
  - manual category labels and value labels placed as slide text
  - chart-only legend with no native chart legend
  - right-side big-number cards paired with explanatory text boxes
  - compact source note and scenario chip without disturbing the chart area

TEXT-FIT PRECEDENT
  comparison_cards:
    geometry: 1.466in wide x 1.000in high
    type: Arial 28pt bold KPI + Arial 16pt unit label
    content: one short number token plus a one/two-word unit label
    copy_when: a slide must compare two or three quantities at glance speed

  right_comparison_notes:
    geometry: 3.292in wide x 1.000in high; final note is 4.757in wide
    type: Arial 16pt bold, centered
    content: short phrase labels only; not paragraph prose
    copy_when: a KPI stack needs readable interpretation, not detailed method

SOURCE NOTE
  Teaching rewrite of the source-faithful `fleet_overview.py` module. The
  original carried a data-over-template `styled_chart(...)` wrapper around
  `slide42_chart24.xml/.xlsb`. This version intentionally rebuilds the visible
  chart as a native editable `bar_chart(mode="clustered")` from explicit segment
  records, values, fills, and axis settings. The manual category labels, manual
  value labels, right-side KPI cards, legend, source note, scenario chip, and
  chrome preserve the source slide's authored coordinates.

FIDELITY NOTE
  This is a practical factory-native rebuild, not a byte-identical chart-template
  port. The bar values are the exact source gross-tonnage figures from
  slide42_chart24 (6,628,515 / 3,347,252 / 739,991 / 625,304 / 334,461 /
  1,581,507 GT), the value axis max equals the Total (so the Total bar fills the
  plot, matching the source), and the per-bar fills match the source chart part —
  including the slate-blue (4C6C9C) Total bar and the 969696 default for the grey
  segments. Small differences in native bar thickness / internal plot margins may
  render differently from the original styled chart part.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, bar_chart, body_slide, graphic_frame, line_break, paragraph, run,
    text_box,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
GRAY_1 = "F2F2F2"
FONT = "Arial"

LAYOUT = "slideLayout4"

# Local palette names keep business meaning visible instead of burying the slide
# in anonymous hex strings.
TEAL_ADDRESSABLE_COMMERCIAL = "007770"
AMBER_ADDRESSABLE_OFFSHORE = "FFC000"
GRAY_NON_ADDRESSABLE = "969696"
SLATE_BLUE_TOTAL = "4C6C9C"  # source per-point color for the Total bar (slide42_chart24 dPt idx 0)
SOFT_BLUE_CALLOUT = "CEDDEC"
NEAR_BLACK_RULE = "121415"
NEGATIVE_RED = "C00000"


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: these are comments the module can expose programmatically.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "scenario_context",
    "use_when": (
        "Use for a baseline exhibit where a compact composition bar chart needs to be "
        "paired with a three-card KPI comparison on the right."
    ),
    "teaches": [
        "native bar_chart composition chart",
        "per-bar colors with data_point_colors",
        "manual category tick labels",
        "manual bar-end value labels",
        "big-number comparison card stack",
        "chart legend outside the native chart",
        "compact off-house source/note block",
    ],
}

TEXT_FIT = {
    "chart_title": {
        "box_in": (4.997, 0.167),
        "font_pt": 10,
        "content": "one-line chart title + footnote marker",
        "note": "Keep this title no-wrap; shorten language before shrinking type.",
    },
    "category_tick_labels": {
        "box_in": (0.307, 0.167),
        "font_pt": 10,
        "content": "short labels; the longest source label uses a 1.635in box",
        "note": "Right-align labels and keep them outside the chart frame.",
    },
    "comparison_cards": {
        "box_in": (1.466, 1.000),
        "font_pt": "28 KPI / 16 unit",
        "content": "short KPI token + 'Gross tons'",
    },
    "right_comparison_notes": {
        "box_in": (3.292, 1.000),
        "font_pt": 16,
        "content": "centered phrase, not prose",
    },
    "source_note": {
        "box_in": (12.367, 0.332),
        "font_pt": 8,
        "content": "two-line Note / Source block",
    },
}

COPY_RULES = [
    "Use this pattern when the chart alone is too quantitative for the takeaway; "
    "the KPI cards should translate the chart into the governing comparison.",
    "Keep the chart category labels manual when the native chart needs a tight, "
    "think-cell-like plot area and exact label positions.",
    "Do not let right-side notes become paragraphs. Once a note exceeds one short "
    "clause, move it to a separate assumptions rail pattern instead.",
]


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
class FleetSegment:
    """One fleet segment in the chart and its manual label geometry."""

    label: str
    value_gt: float  # exact gross tons (matches the source workbook slide42_chart24.xlsb)
    fill: str
    category_box: Box
    value_box: Box
    value_label: str
    include_in_legend: bool = True


@dataclass(frozen=True)
class ComparisonCard:
    """Right-hand KPI card: large number plus unit label."""

    box: Box
    value: str
    value_color: str = BLACK
    unit: str = "Gross tons"


@dataclass(frozen=True)
class ComparisonNote:
    """Centered explanatory label paired with a KPI card."""

    box: Box
    text: str
    fill: str | None = None


@dataclass(frozen=True)
class LegendEntry:
    """Manual addressability legend entry."""

    label: str
    fill: str
    swatch_box: Box
    label_box: Box


# ════════════════════════════════════════════════════════════════════════════
# Layout zones. These names are the teaching surface for future agents.
# ════════════════════════════════════════════════════════════════════════════
CHART_FRAME = Box(2.198, 1.958, 5.378, 4.142)
CHART_TITLE = Box(2.283, 1.766, 4.997, 0.167)
SOURCE_NOTE = Box(0.495, 6.665, 12.367, 0.332)
SCENARIO_CHIP = Box(8.069, 0.174, 2.977, 0.217)

KPI_CARD_W = 1.466
KPI_CARD_H = 1.000
KPI_CARD_X = 8.038
KPI_NOTE_X = 9.504
KPI_NOTE_W = 3.292
KPI_ROW_YS = (1.764, 2.939, 4.113)

LEGEND_FRAME = Box(5.510, 4.752, 2.104, 1.278)
LEGEND_TITLE = Box(5.997, 4.665, 1.130, 0.175)

SEGMENT_LABEL_H = 0.167
BAR_VALUE_W = 0.229
BAR_VALUE_H = 0.167


# ════════════════════════════════════════════════════════════════════════════
# Semantic content. The native chart and the manual labels are both driven from
# these records so future edits do not desynchronize chart values and annotations.
# ════════════════════════════════════════════════════════════════════════════
FLEET_SEGMENTS: tuple[FleetSegment, ...] = (
    FleetSegment(
        label="Total",
        value_gt=6628515,
        fill=SLATE_BLUE_TOTAL,
        category_box=Box(1.887, 2.295, 0.307, SEGMENT_LABEL_H),
        value_box=Box(7.514, 2.295, BAR_VALUE_W, BAR_VALUE_H),
        value_label="6.6",
        include_in_legend=False,
    ),
    FleetSegment(
        label="Addressable Commercial",
        value_gt=3347252,
        fill=TEAL_ADDRESSABLE_COMMERCIAL,
        category_box=Box(0.648, 2.955, 1.547, SEGMENT_LABEL_H),
        value_box=Box(4.941, 2.955, BAR_VALUE_W, BAR_VALUE_H),
        value_label="3.3",
    ),
    FleetSegment(
        label="Great Lakes Commercial",
        value_gt=739991,
        fill=GRAY_NON_ADDRESSABLE,
        category_box=Box(0.663, 3.616, 1.531, SEGMENT_LABEL_H),
        value_box=Box(2.896, 3.616, BAR_VALUE_W, BAR_VALUE_H),
        value_label="0.7",
    ),
    FleetSegment(
        label="Addressable Offshore",
        value_gt=625304,
        fill=AMBER_ADDRESSABLE_OFFSHORE,
        category_box=Box(0.859, 4.276, 1.335, SEGMENT_LABEL_H),
        value_box=Box(2.806, 4.276, BAR_VALUE_W, BAR_VALUE_H),
        value_label="0.6",
    ),
    FleetSegment(
        label="Non-Addressable Offshore",
        value_gt=334461,
        fill=GRAY_NON_ADDRESSABLE,
        category_box=Box(0.559, 4.936, 1.635, SEGMENT_LABEL_H),
        value_box=Box(2.578, 4.936, BAR_VALUE_W, BAR_VALUE_H),
        value_label="0.3",
    ),
    FleetSegment(
        label="Other Segments",
        value_gt=1581507,
        fill=GRAY_NON_ADDRESSABLE,
        category_box=Box(1.189, 5.597, 1.005, SEGMENT_LABEL_H),
        value_box=Box(3.556, 5.597, BAR_VALUE_W, BAR_VALUE_H),
        value_label="1.6",
    ),
)

# Legend intentionally follows the source legend order, not strict chart order:
# addressable categories first, then the grey/non-addressable categories.
ADDRESSABILITY_LEGEND: tuple[LegendEntry, ...] = (
    LegendEntry(
        label="Addressable Commercial",
        fill=TEAL_ADDRESSABLE_COMMERCIAL,
        swatch_box=Box(5.632, 4.905, 0.196, 0.146),
        label_box=Box(5.884, 4.899, 1.547, 0.167),
    ),
    LegendEntry(
        label="Addressable Offshore",
        fill=AMBER_ADDRESSABLE_OFFSHORE,
        swatch_box=Box(5.632, 5.127, 0.196, 0.146),
        label_box=Box(5.884, 5.122, 1.335, 0.167),
    ),
    LegendEntry(
        label="Great Lakes Commercial",
        fill=GRAY_NON_ADDRESSABLE,
        swatch_box=Box(5.632, 5.349, 0.196, 0.146),
        label_box=Box(5.884, 5.344, 1.531, 0.167),
    ),
    LegendEntry(
        label="Non-Addressable Offshore",
        fill=GRAY_NON_ADDRESSABLE,
        swatch_box=Box(5.632, 5.571, 0.196, 0.146),
        label_box=Box(5.884, 5.566, 1.635, 0.167),
    ),
    LegendEntry(
        label="Other Segments",
        fill=GRAY_NON_ADDRESSABLE,
        swatch_box=Box(5.632, 5.793, 0.196, 0.146),
        label_box=Box(5.884, 5.788, 1.005, 0.167),
    ),
)

COMPARISON_CARDS: tuple[ComparisonCard, ...] = (
    ComparisonCard(Box(KPI_CARD_X, KPI_ROW_YS[0], KPI_CARD_W, KPI_CARD_H), "10M"),
    ComparisonCard(Box(KPI_CARD_X, KPI_ROW_YS[1], KPI_CARD_W, KPI_CARD_H), "~6.6M", NEGATIVE_RED),
    ComparisonCard(Box(KPI_CARD_X, KPI_ROW_YS[2], KPI_CARD_W, KPI_CARD_H), "~3.9M", NEGATIVE_RED),
)

COMPARISON_NOTES: tuple[ComparisonNote, ...] = (
    ComparisonNote(Box(KPI_NOTE_X, KPI_ROW_YS[0], KPI_NOTE_W, KPI_CARD_H), "Annual target"),
    ComparisonNote(
        Box(KPI_NOTE_X, KPI_ROW_YS[1], KPI_NOTE_W, KPI_CARD_H),
        "Current US-flagged, US-built fleet gross tonnage",
    ),
    ComparisonNote(
        Box(KPI_NOTE_X, KPI_ROW_YS[2], KPI_NOTE_W, KPI_CARD_H),
        "Addressable Commercial and Offshore gross tonnage",
    ),
    ComparisonNote(
        Box(8.038, 5.288, 4.757, KPI_CARD_H),
        "Reaching throughput target requires rebuilding the entire fleet 1.5x every year",
        SOFT_BLUE_CALLOUT,
    ),
)


# Native editable chart spec. The manual labels below do the visual exposition;
# the native chart exists only to draw the six horizontal bars and carry editable
# workbook data inside the PPTX.
CHART_CATEGORIES: tuple[str, ...] = tuple(segment.label for segment in FLEET_SEGMENTS)
CHART_VALUES_GT: tuple[float, ...] = tuple(segment.value_gt for segment in FLEET_SEGMENTS)
CHART_BAR_FILLS: tuple[str, ...] = tuple(segment.fill for segment in FLEET_SEGMENTS)

_CHART0_DATA = {
    "categories": CHART_CATEGORIES,
    "series": [
        {
            "name": "Gross tonnage (GT)",
            "values": list(CHART_VALUES_GT),
            "data_point_colors": list(CHART_BAR_FILLS),
        }
    ],
}

CHART_STYLE = {
    "mode": "clustered",
    "categories": list(CHART_CATEGORIES),
    "series": [dict(_CHART0_DATA["series"][0])],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_axis_labels": False,
    "show_gridlines": False,
    "show_value_labels": False,
    "value_axis_format": "0.0",
    "value_label_format": "0.0",
    "cat_label_size_pt": 10,
    "value_label_size_pt": 10,
    "gap_width": 95,
    "bar_overlap": 0,
    "seg_line_color": "FFFFFF",
    "seg_line_width": 6350,
    "axis_line_color": WHITE,
    "axis_line_width": 3175,
    "value_axis_min": 0,
    "value_axis_max": 6628515,
    "value_axis_major_unit": 1000000,
    "plot_layout": {
        "x": 0.020,
        "y": 0.030,
        "w": 0.955,
        "h": 0.925,
    },
    "cat_header": "Fleet segment",
}

CHARTS = [bar_chart(**CHART_STYLE)]


# ════════════════════════════════════════════════════════════════════════════
# Tiny local authoring helpers.
# ════════════════════════════════════════════════════════════════════════════
def _textbox(sp_id: int, name: str, box: Box, paras: list[str], **kwargs) -> str:
    """text_box() wrapper that accepts semantic Box objects."""

    return text_box(sp_id, name, *box.emu(), paras, **kwargs)


def _one_line(text: str, *, size: int = PT(10), bold: bool = False,
              italic: bool = False, color: str = BLACK, align: str | None = None) -> str:
    """A tight one-run paragraph used for labels, chips, and legend captions."""

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
# Paint functions. The order mirrors the source slide's effective paint order:
# chart first, manual labels, chrome/source, KPI comparison, legend, top chips.
# ════════════════════════════════════════════════════════════════════════════
def paint_native_chart(next_id) -> list[str]:
    """Draw the editable chart and the separate source-faithful chart title."""

    shapes: list[str] = []
    chart_x, chart_y, chart_cx, chart_cy = CHART_FRAME.emu()
    shapes.append(graphic_frame(
        sp_id=next_id(),
        name="Chart",
        x=chart_x,
        y=chart_y,
        cx=chart_cx,
        cy=chart_cy,
        rId="rId2",
    ))
    shapes.append(_textbox(
        next_id(),
        "ChartTitle",
        CHART_TITLE,
        [paragraph([
            run(
                "US-Flagged, US-Built Fleet Composition by Gross Tonnage (GT in millions)",
                size=PT(10),
                bold=True,
                color=BLACK,
                font=FONT,
            ),
            run("1", size=PT(10), bold=True, color=BLACK, font=FONT),
        ], mar_l=0, indent=0, line_spacing=100000)],
        fill=None,
        line_color="none",
        anchor="b",
        wrap="none",
        l_ins=0,
        t_ins=0,
        r_ins=0,
        b_ins=0,
    ))
    return shapes


def paint_manual_chart_labels(next_id) -> list[str]:
    """Overlay source-positioned category ticks and M-GT labels."""

    shapes: list[str] = []
    for segment in FLEET_SEGMENTS:
        shapes.append(_textbox(
            next_id(),
            "CategoryTickLabel",
            segment.category_box,
            [_one_line(segment.label, align="r")],
            fill=None,
            line_color="none",
            anchor="ctr",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        ))

    for segment in FLEET_SEGMENTS:
        shapes.append(_textbox(
            next_id(),
            "BarValueLabel",
            segment.value_box,
            [_one_line(segment.value_label)],
            fill=None,
            line_color="none",
            anchor="ctr",
            wrap="none",
            l_ins=17463,
            t_ins=0,
            r_ins=17463,
            b_ins=0,
        ))
    return shapes


def paint_chrome_and_source(next_id) -> list[str]:
    """House chrome plus the source-faithful off-house note block."""

    return [
        "",
        "",
        _textbox(
            next_id(),
            "SourceNote",
            SOURCE_NOTE,
            [paragraph([
                run(
                    "Note: (1) As of January 2026; Addressable Commercial defined as oceangoing vessels",
                    size=PT(8),
                    color=BLACK,
                    font=FONT,
                ),
                line_break(),
                run("Source: Clarksons (US fleet size and GT data)", size=PT(8), color=BLACK, font=FONT),
            ], line_spacing=100000)],
            fill=None,
            line_color="none",
        ),
    ]


def paint_big_number_comparison(next_id) -> list[str]:
    """Right-side KPI cards and their short interpretation labels."""

    shapes: list[str] = []
    for card in COMPARISON_CARDS:
        shapes.append(_textbox(
            next_id(),
            "KpiComparisonCard",
            card.box,
            [
                paragraph(
                    [run(card.value, size=PT(28), bold=True, color=card.value_color, font=FONT)],
                    align="ctr",
                    line_spacing=100000,
                ),
                paragraph(
                    [run(card.unit, size=PT(16), color=BLACK, font=FONT)],
                    align="ctr",
                    line_spacing=100000,
                ),
            ],
            fill=GRAY_1,
            line_color="none",
            anchor="ctr",
        ))

    for note in COMPARISON_NOTES:
        shapes.append(_textbox(
            next_id(),
            "KpiComparisonNote",
            note.box,
            [paragraph(
                [run(note.text, size=PT(16), bold=True, color=BLACK, font=FONT)],
                align="ctr",
                line_spacing=100000,
            )],
            fill=note.fill,
            line_color="none",
            anchor="ctr",
        ))
    return shapes


def paint_addressability_legend(next_id) -> list[str]:
    """Manual legend: chart keys stay outside the native chart for exact packing."""

    shapes: list[str] = []
    shapes.append(_textbox(
        next_id(),
        "AddressabilityLegendFrame",
        LEGEND_FRAME,
        [_empty_centered_paragraph()],
        fill=None,
        line_color=NEAR_BLACK_RULE,
        anchor="ctr",
    ))
    shapes.append(_textbox(
        next_id(),
        "AddressabilityLegendTitle",
        LEGEND_TITLE,
        [_one_line("Addressability", italic=True, align="ctr")],
        fill=WHITE,
        line_color="none",
        anchor="ctr",
    ))

    for entry in ADDRESSABILITY_LEGEND:
        shapes.append(_textbox(
            next_id(),
            "LegendSwatch",
            entry.swatch_box,
            [_empty_centered_paragraph()],
            fill=entry.fill,
            line_color="none",
            anchor="ctr",
        ))
    for entry in ADDRESSABILITY_LEGEND:
        shapes.append(_textbox(
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
        ))
    return shapes


def paint_scenario_and_prelim(next_id) -> list[str]:
    """Top-right scenario tag plus the standard Preliminary chip."""

    return [
        _textbox(
            next_id(),
            "ScenarioChip",
            SCENARIO_CHIP,
            [_one_line("(1) Status Quo Scenario", size=PT(12), bold=True, align="ctr")],
            fill=SOFT_BLUE_CALLOUT,
            line_color=BLACK,
            anchor="ctr",
        ),
        "",
    ]


def _body() -> str:
    shapes: list[str] = []
    ids = iter(range(100, 2000))
    next_id = lambda: next(ids)  # noqa: E731 - compact sequential shape ids

    shapes.extend(paint_native_chart(next_id))
    shapes.extend(paint_manual_chart_labels(next_id))
    shapes.extend(paint_chrome_and_source(next_id))
    shapes.extend(paint_big_number_comparison(next_id))
    shapes.extend(paint_addressability_legend(next_id))
    shapes.extend(paint_scenario_and_prelim(next_id))
    return "".join(shapes)


CHROME = Chrome(
    section="US-Built Ship Demand",
    topic="Status Quo",
    title="US-Flagged, US-Built Fleet Overview",
    takeaway="Entire US-flagged and US-built fleet (~6.6M GT) is less than 1 year’s capacity target (10M GT); addressable fleet is ~3.9M GT.",
)


def render() -> str:
    return body_slide(CHROME, _body())
