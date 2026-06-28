"""Teaching exemplar: Golden Dome Marauder comparison vs. DDGs.

ROLE
  cost_capability_comparison / procurement_tradeoff

USE WHEN
  A slide needs a compact left-hand stacked-cost chart, a right-hand capability
  comparison table, top-right service marks, and a source-heavy note line.

TEACHES
  - rebuilding a source styled stacked-column chart as a native chart factory
  - per-point colors inside a stacked column chart (DDG colors on one category,
    Marauder tranche colors on the other)
  - manual in-bar labels and total labels layered over a native chart
  - using a one-row native table as a section title bar
  - using a comparison table with spacer columns, row spans, and empty cells
  - keeping table-cell mechanics local and explicit rather than importing table_kit
  - preserving PowerPoint paint order through section-level paint functions

TEXT-FIT PRECEDENT
  capability_comparison_cells:
    geometry: 2.789in wide x 2.7in high effective content cells
    type: Arial 20pt headline + 12pt supporting copy, centered
    content: a bold numeric capacity line, one munitions line, and one caveat
    copy_when: a side-by-side comparison needs one high-salience number per option
               plus enough caveat text to prevent over-reading.

SOURCE NOTE
  Teaching rewrite of the source-faithful `comparison_vs_ddgs.py` module.
  The source chart template in `slide8_chart1.xml` and its workbook
  `slide8_chart1.xlsb` were used to transcribe the chart's data, colors, fixed
  value axis, gap width, overlap, and manual plot layout. This module does not
  read those files at runtime: it builds the chart through `column_chart()` so the
  data, colors, and axis choices are inspectable in Python.

FIDELITY NOTE
  This is a practical factory rebuild, not a byte-identical chart-template port.
  It preserves the visible chart semantics and major styling controls (stacked
  columns, per-point fills, hidden native category labels, fixed value axis,
  manual plot-area layout, no native legend, no segment outlines), while leaving
  the label system as slide text boxes exactly where the source placed them.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, Link, PT, Sources, body_slide, column_chart, graphic_frame, line_break,
    paragraph, picture, run, table, tbreak, tcell, tcell_rich, text_box, tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
GRAY_1 = "F2F2F2"
FONT = "Arial"

LAYOUT = "slideLayout4"

# Two service-mark images in the source slide. The build package wires these rIds
# to images in the deck's media directory; picture() only references them.
IMAGES = [
    {"rId": "rId3", "file": "image7_3071a231.jpeg"},
    {"rId": "rId4", "file": "image8_ffd85751.png"},
]


# ════════════════════════════════════════════════════════════════════════════
# Native chart spec: source chart XML -> declarative column_chart().
# ════════════════════════════════════════════════════════════════════════════
# Source-chart transcription summary:
#   chart part:       slide8_chart1.xml
#   source workbook:  slide8_chart1.xlsb
#   c:barDir:         col
#   c:grouping:       stacked
#   c:gapWidth:       80
#   c:overlap:        100
#   value axis:       min=0, max=11,000, major=1,000
#   plot layout:      manual inner plot rectangle below
#   categories:       source carried no native category labels; slide text boxes
#                     provide the category labels manually.
PROCUREMENT_CATEGORIES: tuple[str, ...] = (
    "4x Arleigh Burke-class destroyers",
    "240x Golden Dome Marauders",
)

DDG_STACK_COLORS = {
    "ddg_1": BLACK,
    "ddg_2": "808080",
    "ddg_3": "969696",
    "ddg_4": "C0C0C0",
}
MARAUDER_STACK_COLORS = {
    "co_located": "4C6C9C",
    "separate_platforms": "9DB1CF",
}

# Series are ordered bottom-to-top in the stacked columns. The first two series
# deliberately change color by category: the same workbook series represents a
# DDG segment in category 0 and a Marauder tranche in category 1. That pattern is
# copied from the source chart's <c:dPt> overrides.
PROCUREMENT_COST_SERIES: tuple[dict, ...] = (
    {
        "name": "DDG #1 / MR #1-#120 co-located",
        "color": DDG_STACK_COLORS["ddg_1"],
        "data_point_colors": [DDG_STACK_COLORS["ddg_1"], MARAUDER_STACK_COLORS["co_located"]],
        "values": [2700, 5040],
    },
    {
        "name": "DDG #2 / MR #121-#240 separate platforms",
        "color": DDG_STACK_COLORS["ddg_2"],
        "data_point_colors": [DDG_STACK_COLORS["ddg_2"], MARAUDER_STACK_COLORS["separate_platforms"]],
        "values": [2700, 5040],
    },
    {
        "name": "DDG #3",
        "color": DDG_STACK_COLORS["ddg_3"],
        "values": [2700, None],
    },
    {
        "name": "DDG #4",
        "color": DDG_STACK_COLORS["ddg_4"],
        "values": [2700, None],
    },
)

# Readable data mirror for downstream agents/tools that expect the converted-slide
# _CHART0_DATA shape. CHARTS below uses the same values through column_chart().
_CHART0_DATA = {
    "categories": PROCUREMENT_CATEGORIES,
    "series": PROCUREMENT_COST_SERIES,
}

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(PROCUREMENT_CATEGORIES),
    "series": [dict(series) for series in PROCUREMENT_COST_SERIES],
    "show_legend": False,
    "show_cat_labels": False,
    "show_value_labels": False,
    "show_gridlines": False,
    "show_value_axis_labels": True,
    "value_axis_format": '#,##0;"-"#,##0',
    "cat_label_size_pt": 10,
    "gap_width": 80,
    "bar_overlap": 100,
    "seg_line_color": None,
    "axis_line_color": DK,
    "axis_line_width": 9_525,
    "value_axis_min": 0,
    "value_axis_max": 11_000,
    "value_axis_major_unit": 1_000,
    "plot_layout": {
        "x": 0.11101573676680973,
        "y": 0.04653371320037987,
        "w": 0.87410586552217451,
        "h": 0.90693257359924029,
    },
    "cat_header": "Platform",
}

CHARTS = [column_chart(**CHART_STYLE)]


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: comments a future agent can inspect programmatically.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "cost_capability_comparison",
    "use_when": (
        "Use for a procurement-cost comparison where a left chart proves rough "
        "cost parity and a right table proves capability leverage."
    ),
    "teaches": [
        "native column_chart stacked chart rebuilt from source XML",
        "per-point chart colors through data_point_colors",
        "manual in-bar and above-bar labels over a chart",
        "one-row native table title bar",
        "comparison table with row spans and spacer column",
        "local table-cell helpers instead of centralized table_kit",
        "picture rId wiring for two top-right logos",
    ],
}

TEXT_FIT = {
    "chart_axis_title": {
        "box_in": (1.502, 0.167),
        "font_pt": 10,
        "content": "Procurement cost ($M)",
        "note": "External chart title, one line, no wrap.",
    },
    "marauder_tranche_labels": {
        "box_in": (1.276, 0.500),
        "font_pt": 10,
        "content": "3 centered lines, white, no wrap",
        "note": "Works only because each line is short and the label sits inside a wide bar.",
    },
    "capability_comparison_cells": {
        "box_in": (2.789, 2.700),
        "font_pt": "20 headline + 12 body",
        "content": "numeric capacity, munition line, caveat",
        "note": "Use row spans for the left/right cards and a narrow spacer column for Vs.",
    },
    "source_note": {
        "box_in": (12.367, 0.322),
        "font_pt": 8,
        "content": "single long Note/Source line via source_note()",
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


@dataclass(frozen=True)
class TextZone:
    name: str
    box: Box
    font_pt: float
    fit_note: str


@dataclass(frozen=True)
class PictureSlot:
    name: str
    r_id: str
    box: Box


@dataclass(frozen=True)
class ManualLabel:
    name: str
    box: Box
    lines: tuple[str, ...]
    color: str = BLACK
    bold: bool = False
    italic: bool = False
    align: str = "ctr"
    anchor: str = "ctr"
    wrap: str = "none"
    inset_x: int = 17_463
    sup: str = ""   # trailing superscript footnote marker (e.g. "1"), baseline-raised


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Layout zones: chart left, comparison table right, logos top-right.
# ════════════════════════════════════════════════════════════════════════════
CHART_FRAME = Box(0.418, 2.700, 6.068, 3.656)
CHART_AXIS_TITLE = TextZone(
    name="ChartAxisTitle",
    box=Box(0.531, 2.509, 1.502, 0.167),
    font_pt=10,
    fit_note="External y-axis title; keep one line, no wrap.",
)

COST_TABLE_TITLE = TextZone(
    name="CostComparisonTitleBar",
    box=Box(0.495, 1.694, 5.901, 0.333),
    font_pt=12,
    fit_note="One-row title bar above the cost chart.",
)

CAPABILITY_TABLE = TextZone(
    name="CapabilityComparisonTable",
    box=Box(6.962, 1.694, 6.000, 4.500),
    font_pt=12,
    fit_note="Right-hand comparison table with two large row-spanned cards.",
)

LOGO_SLOTS: tuple[PictureSlot, ...] = (
    PictureSlot("Picture 2", "rId3", Box(11.431, 0.048, 0.922, 0.922)),
    PictureSlot("Picture 8", "rId4", Box(12.372, 0.048, 0.922, 0.922)),
)

# Native manual labels intentionally carry the original source geometry. These
# paint after the chart frame so they sit on top of the bars.
DDG_BAR_LABELS: tuple[ManualLabel, ...] = (
    ManualLabel("DDGBarLabel", Box(2.148, 5.694, 0.538, 0.167), ("DDG #1",), color=WHITE),
    ManualLabel("DDGBarLabel", Box(2.148, 4.880, 0.538, 0.167), ("DDG #2",), color=WHITE),
    ManualLabel("DDGBarLabel", Box(2.148, 4.068, 0.538, 0.167), ("DDG #4",), color=WHITE),
)

CHART_CALLOUT_LABELS: tuple[ManualLabel, ...] = (
    ManualLabel("DDGTopSegmentLabel", Box(2.148, 3.253, 0.538, 0.167), ("DDG #4",), anchor="ctr"),
    ManualLabel(
        "DDGCategoryLabel",
        Box(1.446, 6.233, 1.943, 0.167),
        ("Arleigh Burke-class destroyers",),
        sup="1",
        inset_x=0,
    ),
    ManualLabel(
        "MarauderCoLocatedLabel",
        Box(4.432, 5.175, 1.276, 0.500),
        ("MR #1-#120", "(Co-located sensors", "and interceptors)"),
        color=WHITE,
    ),
    ManualLabel(
        "MarauderCategoryLabel",
        Box(4.260, 6.233, 1.618, 0.167),
        ("Golden Dome Marauders",),
        sup="2",
        inset_x=0,
    ),
    ManualLabel("DDGTotalLabel", Box(2.188, 2.736, 0.458, 0.167), ("10,800",), anchor="b"),
    ManualLabel("MarauderTotalLabel", Box(4.840, 2.953, 0.458, 0.167), ("10,080",), anchor="b"),
    ManualLabel(
        "MarauderSeparatePlatformsLabel",
        Box(4.420, 3.740, 1.299, 0.333),
        ("MR #121-#240 ", "(Separate platforms)"),
        color=BLACK,
    ),
)

# Source line with external hyperlinks. The chart is rId2 and the two logos rId3/
# rId4, so the source links start at rId5; the Sources band wires them via Link().
HYPERLINKS = [
    {"rId": "rId5", "url": "https://www.congress.gov/crs-product/RL32109"},                                                                                   # Congressional Research Service
    {"rId": "rId6", "url": "https://www.congress.gov/bill/119th-congress/house-bill/1/text"},                                                                 # OBBBA text
    {"rId": "rId7", "url": "https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/documents/naval-launchers-and-munitions/Mk70_Product_Card.pdf"},   # MK 70 Product Card
    {"rId": "rId8", "url": "https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/documents/naval-launchers-and-munitions/Mk_41_Product_Card_Update_24_08549.pdf"},  # MK 41 Product Card
]

NOTE_SOURCE_TEXT = Sources(
    note="(1) Flight III destroyers; Assumes $2.7B unit price based on OBBBA "
    "($5.4B for 2x), CRS estimate ($2.7B apiece), and FY26 Shipbuilding and "
    "Conversion, Navy Justification Book Exhibit P-5c, Ship Cost Analysis ($5.5B "
    "for 2x in FY24, $7.86B for 3x in FY25); (2) Marauder priced at $42M / unit "
    "excluding launcher costs; (3) 4x SM-3 or SM-6 per MK-70, with 4x MK-70 per "
    "Marauder for total of 16x SM-3 or SM-6 per Marauder",
    source=(
        Link("Congressional Research Service", "rId5"),
        Link("OBBBA text", "rId6"),
        "FY26 Budget Estimate",
        Link("Lockheed Martin MK 70 Product Card", "rId7"),
        Link("Lockheed Martin MK 41 Product Card", "rId8"),
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: local by design for teaching-module readability.
# ════════════════════════════════════════════════════════════════════════════
PAD = dict(l_ins=60_960, r_ins=60_960, t_ins=60_960, b_ins=60_960)


def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def border_dict(**edges):
    """Only draw the sides passed as L/R/T/B; omitted sides render as no-fill."""

    return {k: v for k, v in edges.items() if v is not None} or None


def table_run(
    text: str,
    *,
    size_pt: float = 10,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    color: str = BLACK,
    baseline: int | None = None,
) -> str:
    return trun(
        text,
        size=PT(size_pt),
        bold=bold or None,
        italic=italic or None,
        underline=underline or None,
        color=color,
        font=FONT,
        baseline=baseline,
    )


def empty_para(align: str = "ctr", end_size_pt: float = 1) -> str:
    """An empty table paragraph: spacing/border only, no runs. end_size_pt sets its
    <a:endParaRPr> size so a blank spacer row collapses to the source height instead
    of the renderer's default — PT1 for a tight spacer, PT12 for a body-height gap."""

    return tpara([], align=align, mar_l=0, indent=0, end_size=PT(end_size_pt))


def cell(
    text: str = "",
    *,
    fill=None,
    bold: bool | None = None,
    italic: bool | None = None,
    color: str = BLACK,
    size_pt: float = 10,
    align: str = "l",
    anchor: str = "ctr",
    span: int = 1,
    rowspan: int = 1,
    l_ins: int = 45_720,
    r_ins: int = 45_720,
    t_ins: int = 45_720,
    b_ins: int = 45_720,
    **edges,
):
    """Plain tcell wrapper: content first, cell mechanics second."""

    return tcell(
        text,
        fill=fill,
        bold=bold,
        italic=italic,
        color=color,
        size=PT(size_pt),
        align=align,
        anchor=anchor,
        grid_span=span,
        row_span=rowspan,
        font=FONT,
        l_ins=l_ins,
        r_ins=r_ins,
        t_ins=t_ins,
        b_ins=b_ins,
        borders=border_dict(**edges),
    )


def rich_cell(
    paras,
    *,
    fill=None,
    anchor: str = "ctr",
    span: int = 1,
    rowspan: int = 1,
    l_ins: int = 45_720,
    r_ins: int = 45_720,
    t_ins: int = 45_720,
    b_ins: int = 45_720,
    **edges,
):
    """Rich tcell wrapper: tpara()/trun() content, then borders/insets/spans."""

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
# Text helpers: keep the paint functions at slide-intent level.
# ════════════════════════════════════════════════════════════════════════════
def _r(
    text: str,
    *,
    size_pt: float = 10,
    bold: bool = False,
    italic: bool = False,
    color: str = BLACK,
    baseline: int | None = None,
) -> str:
    return run(
        text,
        size=PT(size_pt),
        bold=bold or None,
        italic=italic or None,
        color=color,
        font=FONT,
        baseline=baseline,
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


def _manual_label_para(label: ManualLabel) -> str:
    runs: list[str] = []
    for idx, line in enumerate(label.lines):
        if idx:
            runs.append(line_break())
        runs.append(_r(line, bold=label.bold, italic=label.italic, color=label.color))
    if label.sup:
        runs.append(_r(label.sup, bold=label.bold, color=label.color, baseline=30000))
    return _tight_para(runs, align=label.align)


def _manual_label(out: list[str], ids: ShapeIds, label: ManualLabel) -> None:
    out.append(
        text_box(
            ids.next(),
            label.name,
            *label.box.emu(),
            [_manual_label_para(label)],
            fill=None,
            line_color="none",
            anchor=label.anchor,
            wrap=label.wrap,
            l_ins=label.inset_x,
            t_ins=0,
            r_ins=label.inset_x,
            b_ins=0,
        )
    )


def paint_logos(out: list[str], ids: ShapeIds) -> None:
    for slot in LOGO_SLOTS:
        out.append(picture(ids.next(), slot.name, slot.r_id, *slot.box.emu()))


def paint_chart(out: list[str], ids: ShapeIds) -> None:
    out.append(
        graphic_frame(
            sp_id=ids.next(),
            name="ProcurementCostChart",
            x=IN(CHART_FRAME.x),
            y=IN(CHART_FRAME.y),
            cx=IN(CHART_FRAME.w),
            cy=IN(CHART_FRAME.h),
            rId="rId2",
        )
    )


def paint_chart_manual_labels(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            CHART_AXIS_TITLE.name,
            *CHART_AXIS_TITLE.box.emu(),
            [_tight_para([_r("Procurement cost ($M)", bold=True)], align=None)],
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

    for label in DDG_BAR_LABELS:
        _manual_label(out, ids, label)

    for label in CHART_CALLOUT_LABELS:
        _manual_label(out, ids, label)


def paint_cost_comparison_title_bar(out: list[str], ids: ShapeIds) -> None:
    # One-row native table; the bottom rule aligns with the right-hand table's title rule.
    out.append(
        table(
            ids.next(),
            COST_TABLE_TITLE.name,
            *COST_TABLE_TITLE.box.emu(),
            col_widths=[IN(COST_TABLE_TITLE.box.w)],
            rows=[
                trow(
                    [
                        rich_cell(
                            [
                                tpara(
                                    [
                                        table_run("Cost comparison – ", size_pt=12, bold=True),
                                        table_run("Arleigh Burke", size_pt=12, bold=True, italic=True),
                                        table_run("-class destroyers ", size_pt=12, bold=True),
                                        table_run("vs. GD Marauders", size_pt=12, bold=True),
                                    ]
                                )
                            ],
                            anchor="b",
                            **PAD,
                            B=edge(DK),
                        )
                    ],
                    h=IN(0),
                )
            ],
        )
    )


def paint_capability_comparison_table(out: list[str], ids: ShapeIds) -> None:
    # col_widths defines the three column tracks: left comparison card, narrow
    # Vs. spacer, right comparison card. Row spans make the capacity cards behave
    # like big cards while the spacer column keeps a centered Vs. stack.
    out.append(
        table(
            ids.next(),
            CAPABILITY_TABLE.name,
            *CAPABILITY_TABLE.box.emu(),
            col_widths=[IN(2.789), IN(0.423), IN(2.789)],
            rows=[
                # Title bar: one cell spanning all three columns.
                trow(
                    [
                        cell(
                            "Capability comparison – Strike munitions capacity",
                            size_pt=12,
                            bold=True,
                            color=BLACK,
                            span=3,
                            anchor="b",
                            **PAD,
                            B=edge(DK),
                        )
                    ],
                    h=IN(0.338),
                ),
                # Thin rule row: PT1 spacers carry the top rule below the title.
                trow(
                    [
                        cell("", size_pt=1, align="ctr", anchor="b", **PAD, T=edge(DK)),
                        cell("", size_pt=1, align="ctr", anchor="b", **PAD, T=edge(DK)),
                        cell("", size_pt=1, align="ctr", anchor="b", **PAD, T=edge(DK)),
                    ],
                    h=IN(0.220),
                ),
                # Column heads: 4x DDGs | spacer | 240x Marauders.
                trow(
                    [
                        rich_cell(
                            [
                                tpara(
                                    [
                                        table_run("4x ", size_pt=12, bold=True, color=WHITE),
                                        table_run("Arleigh Burke-", size_pt=12, bold=True, italic=True, color=WHITE),
                                        table_run("class", size_pt=12, bold=True, color=WHITE),
                                        table_run(" ", size_pt=12, bold=True, italic=True, color=WHITE),
                                        table_run("destroyers", size_pt=12, bold=True, color=WHITE),
                                        table_run("1", size_pt=12, bold=True, baseline=30000, color=WHITE),
                                    ],
                                    align="ctr",
                                )
                            ],
                            fill="808080",
                            **PAD,
                        ),
                        cell("", size_pt=12, align="ctr", **PAD),
                        rich_cell(
                            [
                                tpara(
                                    [
                                        table_run("240x Marauders", size_pt=12, bold=True, color=WHITE),
                                        table_run("3", size_pt=12, bold=True, baseline=30000, color=WHITE),
                                    ],
                                    align="ctr",
                                )
                            ],
                            fill=MARAUDER_STACK_COLORS["co_located"],
                            **PAD,
                        ),
                    ],
                    h=IN(0.540),
                ),
                # Spacer row between headers and card bodies.
                trow(
                    [
                        rich_cell([empty_para()], **PAD),
                        rich_cell([empty_para()], **PAD),
                        rich_cell([empty_para()], **PAD),
                    ],
                    h=IN(0.192),
                ),
                # Capacity cards: left and right span the next five rows; the
                # middle column continues as a separate Vs. stack.
                trow(
                    [
                        rich_cell(
                            [
                                tpara(
                                    [
                                        table_run("Up to 384", size_pt=20, bold=True),
                                        tbreak(),
                                        table_run("SM-3 / SM-6", size_pt=12),
                                        tbreak(),
                                        tbreak(),
                                        table_run(
                                            "(384 represents total VLS capacity; actual interceptor quantity dependent on mission) ",
                                            size_pt=12,
                                            italic=True,
                                        ),
                                    ],
                                    align="ctr",
                                    mar_l=0,
                                    indent=0,
                                )
                            ],
                            fill=GRAY_1,
                            rowspan=5,
                            **PAD,
                        ),
                        rich_cell([empty_para(end_size_pt=12)], **PAD),
                        rich_cell(
                            [
                                tpara(
                                    [
                                        table_run("3,840 ", size_pt=20, bold=True),
                                        tbreak(),
                                        table_run("SM-3 / SM-6", size_pt=12),
                                        tbreak(),
                                        tbreak(),
                                        table_run("10x+ ", size_pt=12, underline=True),
                                        table_run("Arleigh Burke", size_pt=12, italic=True, underline=True),
                                        table_run(" capacity", size_pt=12, underline=True),
                                    ],
                                    align="ctr",
                                    mar_l=0,
                                    indent=0,
                                )
                            ],
                            fill="CEDDEC",
                            rowspan=5,
                            **PAD,
                        ),
                    ],
                    h=IN(0.732),
                ),
                trow([rich_cell([empty_para(end_size_pt=12)], **PAD)], h=IN(0.366)),
                trow(
                    [
                        rich_cell(
                            [tpara([table_run("Vs.", size_pt=12)], align="ctr", mar_l=0, indent=0)],
                            **PAD,
                        )
                    ],
                    h=IN(0.732),
                ),
                trow([rich_cell([empty_para(end_size_pt=12)], **PAD)], h=IN(0.366)),
                trow([rich_cell([empty_para(end_size_pt=12)], **PAD)], h=IN(1.013)),
            ],
        )
    )


def paint_sources(out: list[str], ids: ShapeIds) -> None:
    out.append("")


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # Paint order matters in PowerPoint OOXML: later elements sit on top.
    paint_logos(out, ids)
    paint_chart(out, ids)
    paint_chart_manual_labels(out, ids)
    paint_cost_comparison_title_bar(out, ids)
    paint_capability_comparison_table(out, ids)
    paint_sources(out, ids)

    return "".join(out)


CHROME = Chrome(
    section="Golden Dome Requirements",
    topic="Platform Quantities",
    title="Comparison vs. DDGs",
    takeaway="Total GD MR procurement cost is roughly the same as four Arleigh "
                "Burke-class destroyers while delivering 10x+ the interceptor capacity",
    preliminary=False,
    title_cx=IN(11.1),   # source narrows the title box so the takeaway clears the top-right DoD/MDA logos
    sources=NOTE_SOURCE_TEXT,
)


def render() -> str:
    return body_slide(CHROME, _body())
