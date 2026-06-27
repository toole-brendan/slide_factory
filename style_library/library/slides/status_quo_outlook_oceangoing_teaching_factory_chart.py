"""Teaching exemplar: status-quo oceangoing retirement-replacement outlook.

ROLE
  scenario_outlook / retirement_replacement_sufficiency

USE WHEN
  A slide needs to show that a status-quo replacement market is too small to
  sustain serial production. This pattern pairs a left-side multi-year stacked
  chart with a right-side replacement-rate table, a paired legend, and explicit
  callouts that translate annual retirements/orderbook into production scale.

TEACHES
  - data-over-template charting with styled_chart(), using the source chart XML
    and workbook as the style/edit-data template
  - manual category ticks and bar-total labels around a bundled native chart
  - a paired legend system for negative retirements vs. positive orderbook
  - inline native-table helpers for borders, fills, spans, insets, and rich cells
  - a compact right-hand table that makes the chart's implication legible
  - paint-order discipline for chart -> labels -> chrome -> table -> legend -> callouts

TEXT-FIT PRECEDENT
  retirement_table:
    geometry: 5.049in wide x 3.867in high
    type: Arial 10pt table labels, 16pt red numeric values, single-spaced
    content: 3-column table with title row, header row, 4 archetype rows, and a
             2-column commentary cell with bullets
    copy_when: a chart proves the time series and a table must summarize the
               production-rate implication by category

  chart_callout:
    geometry: 2.382in wide x 0.425in high
    type: Arial 10pt italic, centered, single-spaced
    content: one sentence explaining that bar totals are net hulls added/removed

SOURCE NOTE
  Teaching rewrite of the source-faithful `status_quo_outlook_oceangoing.py`
  module. The chart remains a styled_chart() data-over-template exhibit using
  `slide44_chart26.xml` and `slide44_chart26.xlsb`; those files may live beside
  this module or in a sibling `_src/` directory. Table styling is intentionally
  inlined locally rather than imported from deck_core.table_kit.

FIDELITY NOTE
  This is a readability refactor of the polished source module. Coordinates,
  shape names, paint order, table spans/rules/fills, manual labels, and chart data
  are preserved so `render()` stays byte-identical to the source module when the
  same deck_core primitives are used.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    line_break,
    table,
    trow,
    tcell,
    tcell_rich,
    tpara,
    trun,
    breadcrumb,
    title_placeholder,
    prelim_chip,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, WHITE, GRAY_1, FONT

LAYOUT = "slideLayout4"


# ════════════════════════════════════════════════════════════════════════════
# Chart template and visible data.
# ════════════════════════════════════════════════════════════════════════════
def _chart_file(name: str) -> Path:
    """Resolve a chart source file either beside this module or under `_src/`."""

    here = Path(__file__).parent
    direct = here / name
    if direct.exists():
        return direct
    return here / "_src" / name


_CHART0_TPL = _chart_file("slide44_chart26.xml").read_text(encoding="utf-8")
_XLSB0 = _chart_file("slide44_chart26.xlsb").read_bytes()

CHART_CATEGORIES: tuple[str, ...] = tuple(str(year) for year in range(2026, 2051))


@dataclass(frozen=True)
class ChartSeries:
    """One template-backed chart series; styled_chart consumes only `values`."""

    name: str
    role: str
    values: list[int | None]


# The source chart template owns series names, colors, stacked-bar orientation,
# axis styling, and label styling. The values remain explicit here so agents can
# reason about the business logic without opening the embedded workbook.
STATUS_QUO_CHART_SERIES: tuple[ChartSeries, ...] = (
    ChartSeries(
        name="Container / orderbook and retirements",
        role="mixed orderbook additions and retirement removals",
        values=[1, 2, 2, 5, 5, -1, -1, -3, -2, None, -1, -1, -1, -2, -2, -2, -3, -2, -6, -5, -1, -2, -1, -1, -4],
    ),
    ChartSeries(
        name="General Cargo retirements",
        role="retirement removals",
        values=[-1, -3, None, -1, -1, None, -1, None, None, None, None, None, -1, None, -1, None, None, -2, -1, -1, -1, None, None, None, None],
    ),
    ChartSeries(
        name="RORO retirements",
        role="retirement removals",
        values=[-5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, -1, None, -1, None, None, None, None, None],
    ),
    ChartSeries(
        name="Tanker retirements",
        role="retirement removals",
        values=[-4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ),
)

# Keep the converted-slide data-dict shape exactly: categories stay None because
# the template carries the category cache; manual text boxes draw the visible ticks.
_CHART0_DATA = {
    "categories": None,
    "series": [{"values": series.values} for series in STATUS_QUO_CHART_SERIES],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: useful for agents choosing an exemplar.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "status_quo_retirement_replacement_outlook",
    "use_when": (
        "Use for a status-quo demand outlook where the chart shows annual net "
        "retirements/orderbook and the table translates that into replacement "
        "rates by archetype."
    ),
    "teaches": [
        "styled_chart data-over-template with visible Python data",
        "manual year ticks around a chart frame",
        "manual net-hull bar-total labels",
        "right-side retirement replacement table",
        "inline table border/fill/span helpers",
        "paired legend frames for retirements vs orderbook",
        "callouts and scenario chip layered after analytical content",
    ],
}

TEXT_FIT = {
    "orderbook_window_rail": {
        "box_in": (1.354, 4.276),
        "font_pt": 10,
        "content": "three italic words with explicit line breaks, bottom anchored",
    },
    "retirement_table": {
        "box_in": (5.049, 3.867),
        "font_pt": 10,
        "content": "title + header + 4 value rows + commentary row",
        "note": (
            "The table works because the large red numbers are short and the "
            "commentary is kept to two bullets inside a merged cell."
        ),
    },
    "takeaway_banner": {
        "box_in": (5.094, 0.680),
        "font_pt": 12,
        "content": "one bold sentence plus italic parenthetical",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Semantic records: geometry in inches; converted to EMU at the last moment.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
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
class TableZone:
    name: str
    box: Box
    col_widths: tuple[float, ...]
    fit_note: str


@dataclass(frozen=True)
class YearTick:
    x: float
    label: str


@dataclass(frozen=True)
class BarTotalLabel:
    box: Box
    label: str
    anchor: str = "t"


@dataclass(frozen=True)
class LegendEntry:
    label: str
    fill: str
    swatch: Box
    caption: Box


@dataclass(frozen=True)
class ReplacementRow:
    archetype: str
    fill: str
    total: str
    net_of_orderbook: str


@dataclass(frozen=True)
class Callout:
    name: str
    box: Box
    text: str
    fill: str | None = WHITE
    line_color: str | None = "none"
    prst: str = "rect"
    geom_adj: dict[str, str] | None = None
    italic: bool = True


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Layout zones.
# ════════════════════════════════════════════════════════════════════════════
ORDERBOOK_WINDOW_RAIL = TextZone(
    name="Rectangle 30",
    box=Box(0.783, 2.104, 1.354, 4.276),
    font_pt=10,
    fit_note="Bottom-anchored italic rail showing the years with orderbook data.",
)

CHART_FRAME = Box(0.325, 1.866, 7.359, 4.165)
CHART_TITLE = TextZone(
    name="Text Placeholder 25",
    box=Box(0.484, 1.752, 6.707, 0.167),
    font_pt=10,
    fit_note="Single-line chart title; no-wrap and zero-inset.",
)

YEAR_TICK_ZONE = TextZone(
    name="YearLabel",
    box=Box(0.0, 6.026, 0.167, 0.306),
    font_pt=8,
    fit_note="Right-aligned year ticks pinned to the chart categories.",
)

BAR_TOTAL_SIZE = (0.161, 0.167)
LEGEND_SWATCH_SIZE = (0.196, 0.146)
LEGEND_LABEL_H = 0.167

RETIREMENT_TABLE = TableZone(
    name="Table 769",
    box=Box(7.747, 1.685, 5.049, 3.867),
    col_widths=(1.181, 1.723, 2.145),
    fit_note="Right-hand summary table: archetype / total / net of orderbook.",
)

TAKEAWAY_BANNER = TextZone(
    name="Rectangle 690",
    box=Box(7.790, 5.652, 5.094, 0.680),
    font_pt=12,
    fit_note="One-line conclusion with italic parenthetical.",
)

SOURCE_NOTE = TextZone(
    name="Rectangle 694",
    box=Box(0.495, 6.680, 12.367, 0.317),
    font_pt=8,
    fit_note="Off-house note/source line kept as a normal text box.",
)


# ════════════════════════════════════════════════════════════════════════════
# Manual chart labels and legend data.
# ════════════════════════════════════════════════════════════════════════════
YEAR_TICKS: tuple[YearTick, ...] = (
    YearTick(0.830, "2026"),
    YearTick(1.102, "2027"),
    YearTick(1.375, "2028"),
    YearTick(1.648, "2029"),
    YearTick(1.920, "2030"),
    YearTick(2.193, "2031"),
    YearTick(2.465, "2032"),
    YearTick(2.738, "2033"),
    YearTick(3.010, "2034"),
    YearTick(3.283, "2035"),
    YearTick(3.556, "2036"),
    YearTick(3.828, "2037"),
    YearTick(4.101, "2038"),
    YearTick(4.375, "2039"),
    YearTick(4.648, "2040"),
    YearTick(4.920, "2041"),
    YearTick(5.193, "2042"),
    YearTick(5.465, "2043"),
    YearTick(6.010, "2045"),
    YearTick(6.283, "2046"),
    YearTick(6.556, "2047"),
    YearTick(6.828, "2048"),
    YearTick(7.101, "2049"),
    YearTick(7.373, "2050"),
    YearTick(5.738, "2044"),
)

BAR_TOTAL_LABELS: tuple[BarTotalLabel, ...] = (
    BarTotalLabel(Box(0.833, 5.812, *BAR_TOTAL_SIZE), "-9"),
    BarTotalLabel(Box(1.106, 4.528, *BAR_TOTAL_SIZE), "-1"),
    BarTotalLabel(Box(2.469, 4.344, *BAR_TOTAL_SIZE), "-2"),
    BarTotalLabel(Box(4.104, 4.344, *BAR_TOTAL_SIZE), "-2"),
    BarTotalLabel(Box(4.651, 4.528, *BAR_TOTAL_SIZE), "-3"),
    BarTotalLabel(Box(5.469, 4.894, *BAR_TOTAL_SIZE), "-5"),
    BarTotalLabel(Box(5.741, 5.262, *BAR_TOTAL_SIZE), "-7"),
    BarTotalLabel(Box(6.014, 5.262, *BAR_TOTAL_SIZE), "-7"),
    BarTotalLabel(Box(6.286, 4.344, *BAR_TOTAL_SIZE), "-2"),
)

ORDERBOOK_FOUR_LABELS: tuple[BarTotalLabel, ...] = (
    BarTotalLabel(Box(1.674, 2.837, 0.115, 0.167), "4", anchor="b"),
    BarTotalLabel(Box(1.946, 2.837, 0.115, 0.167), "4", anchor="b"),
)

LEGEND_ENTRIES: tuple[LegendEntry, ...] = (
    LegendEntry("Container", "9DB1CF", Box(5.330, 2.618, *LEGEND_SWATCH_SIZE), Box(5.582, 2.613, 0.599, LEGEND_LABEL_H)),
    LegendEntry("General", "6F8DB9", Box(5.330, 2.840, *LEGEND_SWATCH_SIZE), Box(5.582, 2.835, 0.491, LEGEND_LABEL_H)),
    LegendEntry("RORO", "4C6C9C", Box(5.330, 3.062, *LEGEND_SWATCH_SIZE), Box(5.582, 3.057, 0.417, LEGEND_LABEL_H)),
    LegendEntry("Tanker", "364D6E", Box(5.330, 3.285, *LEGEND_SWATCH_SIZE), Box(5.582, 3.280, 0.431, LEGEND_LABEL_H)),
    LegendEntry("Container", "C0C0C0", Box(6.292, 2.618, *LEGEND_SWATCH_SIZE), Box(6.543, 2.613, 0.599, LEGEND_LABEL_H)),
    LegendEntry("General", "969696", Box(6.292, 2.840, *LEGEND_SWATCH_SIZE), Box(6.543, 2.835, 0.491, LEGEND_LABEL_H)),
    LegendEntry("RORO", "808080", Box(6.292, 3.062, *LEGEND_SWATCH_SIZE), Box(6.543, 3.057, 0.417, LEGEND_LABEL_H)),
    LegendEntry("Tanker", BLACK, Box(6.292, 3.285, *LEGEND_SWATCH_SIZE), Box(6.543, 3.280, 0.431, LEGEND_LABEL_H)),
)

REPLACEMENT_ROWS: tuple[ReplacementRow, ...] = (
    ReplacementRow("Container", "9DB1CF", "~0.6", "~0.4"),
    ReplacementRow("General", "6F8DB9", "~0.2", "~0.2"),
    ReplacementRow("RORO", "4C6C9C", "~0.2", "~0.2"),
    ReplacementRow("Tanker", "364D6E", "~1.7", "~1.2"),
)

BAR_TOTAL_CALLOUT = Callout(
    name="Speech Bubble: Rectangle 645",
    box=Box(5.193, 1.965, 2.382, 0.425),
    text="Bar total values indicate net hulls added (removed) each year",
    fill=WHITE,
    line_color="none",
    prst="wedgeRectCallout",
    geom_adj={"adj1": "val -19106", "adj2": "val -3267"},
)

HANWHA_CALLOUT = Callout(
    name="Speech Bubble: Rectangle 2",
    box=Box(2.239, 3.166, 1.501, 0.416),
    text="12x purchased by Hanwha Shipping",
    fill=None,
    line_color=BLACK,
    prst="wedgeRectCallout",
    geom_adj={"adj1": "val -59329", "adj2": "val -21373"},
)


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: local by design, not imported from deck_core.table_kit.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def border_dict(**edges):
    """Only draw the sides passed as L/R/T/B; omitted sides render as no-fill."""

    return {k: v for k, v in edges.items() if v is not None} or None


def plain_cell(
    text: str = "",
    *,
    fill=None,
    bold=None,
    italic=None,
    color=BLACK,
    size=PT(10),
    align="l",
    anchor="ctr",
    span=1,
    rowspan=1,
    l_ins=45_720,
    r_ins=45_720,
    t_ins=45_720,
    b_ins=45_720,
    **edges,
):
    """Single-run tcell wrapper: content first, table mechanics second."""

    return tcell(
        text,
        fill=fill,
        bold=bold,
        italic=italic,
        color=color,
        size=size,
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
    anchor="ctr",
    span=1,
    rowspan=1,
    l_ins=45_720,
    r_ins=45_720,
    t_ins=45_720,
    b_ins=45_720,
    **edges,
):
    """Multi-paragraph tcell_rich wrapper; spans, insets, and borders stay local."""

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
# Small text emitters. Defaults mirror the original source calls exactly.
# ════════════════════════════════════════════════════════════════════════════
def _body_run(text: str, *, size_pt: float = 10, color=None, bold=None, italic=None):
    return run(text, size=PT(size_pt), bold=bold, italic=italic, color=color, font=FONT)


def _chart_label_para(text: str, *, size_pt: float = 10, color=None, align="ctr"):
    return paragraph(
        [_body_run(text, size_pt=size_pt, color=color)],
        align=align,
        mar_l=0,
        indent=0,
        line_spacing=100_000,
    )


# ════════════════════════════════════════════════════════════════════════════
# Table row builders. The row functions show the table mechanics rather than
# hiding them in a centralized kit.
# ════════════════════════════════════════════════════════════════════════════
def _replacement_value_rows() -> list[dict]:
    rows: list[dict] = []
    for i, row in enumerate(REPLACEMENT_ROWS):
        top_rule = edge(BLACK) if i == 0 else edge("808080", 6_350)
        bottom_rule = edge("808080", 6_350)
        rows.append(
            trow(
                [
                    plain_cell(row.archetype, bold=True, color=WHITE, fill=row.fill, T=top_rule, B=bottom_rule),
                    plain_cell(row.total, size=PT(16), bold=True, color="C30C3E", align="ctr", T=top_rule, B=bottom_rule),
                    plain_cell(row.net_of_orderbook, size=PT(16), bold=True, color="C30C3E", align="ctr", T=top_rule, B=bottom_rule),
                ],
                h=IN(0.6),
            )
        )
    return rows


def _commentary_paragraphs():
    return [
        tpara(
            [trun("Assumes owners replace retirements 1-for-1 and at the end of estimated service life", size=PT(10), color=BLACK, font=FONT)],
            bullet=True,
            mar_l=171_450,
            indent=-171_450,
        ),
        tpara([], bullet=True, mar_l=171_450, indent=-171_450),
        tpara(
            [trun("Tanker figures include multiple types, including product, chemical & oil, crude, and shuttle", size=PT(10), color=BLACK, font=FONT)],
            bullet=True,
            mar_l=171_450,
            indent=-171_450,
        ),
    ]


def _retirement_table_rows() -> list[dict]:
    rows = [
        trow(
            [plain_cell("Average retirement replacements required per year ’26-’50", bold=True, span=3, B=edge(BLACK))],
            h=IN(0),
        ),
        trow(
            [
                plain_cell("Archetype", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK)),
                plain_cell("Total", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK)),
                plain_cell("Net of Orderbook Deliveries", bold=True, align="ctr", T=edge(BLACK), B=edge(BLACK)),
            ],
            h=IN(0),
        ),
    ]
    rows.extend(_replacement_value_rows())
    rows.append(
        trow(
            [
                plain_cell("Commentary", bold=True, T=edge("808080", 6_350)),
                rich_cell(_commentary_paragraphs(), span=2, T=edge("808080", 6_350)),
            ],
            h=IN(0.6),
        )
    )
    return rows


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def paint_orderbook_window(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            ORDERBOOK_WINDOW_RAIL.name,
            *ORDERBOOK_WINDOW_RAIL.box.emu(),
            [
                paragraph(
                    [
                        run("Years with ", size=PT(10), italic=True, color=BLACK, font=FONT),
                        line_break(),
                        run("orderbook ", size=PT(10), italic=True, color=BLACK, font=FONT),
                        line_break(),
                        run("data", size=PT(10), italic=True, color=BLACK, font=FONT),
                        line_break(),
                        line_break(),
                        line_break(),
                    ],
                    align="r",
                    line_spacing=100_000,
                )
            ],
            fill=GRAY_1,
            line_color="none",
            anchor="b",
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


def paint_chart_manual_labels(out: list[str], ids: ShapeIds) -> None:
    for tick in YEAR_TICKS:
        out.append(
            text_box(
                ids.next(),
                YEAR_TICK_ZONE.name,
                IN(tick.x),
                IN(YEAR_TICK_ZONE.box.y),
                IN(YEAR_TICK_ZONE.box.w),
                IN(YEAR_TICK_ZONE.box.h),
                [
                    paragraph(
                        [run(tick.label, size=PT(8), color=BLACK, font=FONT)],
                        align="r",
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

    out.append(
        text_box(
            ids.next(),
            CHART_TITLE.name,
            *CHART_TITLE.box.emu(),
            [
                paragraph(
                    [
                        run(
                            "Implied Retirements vs. Orderbook of US-Built, US-Flagged Oceangoing Commercial Vessels (# Hulls)",
                            size=PT(10),
                            bold=True,
                            color=BLACK,
                            font=FONT,
                        )
                    ],
                    mar_l=0,
                    indent=0,
                    line_spacing=100_000,
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
    )

    for label in BAR_TOTAL_LABELS:
        out.append(
            text_box(
                ids.next(),
                "Label",
                *label.box.emu(),
                [_chart_label_para(label.label, align="ctr")],
                fill=None,
                line_color="none",
                wrap="none",
                l_ins=17_463,
                t_ins=0,
                r_ins=17_463,
                b_ins=0,
            )
        )

    for label in ORDERBOOK_FOUR_LABELS:
        out.append(
            text_box(
                ids.next(),
                "Text Placeholder 25",
                *label.box.emu(),
                [_chart_label_para(label.label, align="ctr")],
                fill=None,
                line_color="none",
                anchor=label.anchor,
                wrap="none",
                l_ins=17_463,
                t_ins=0,
                r_ins=17_463,
                b_ins=0,
            )
        )


def paint_chrome(out: list[str]) -> None:
    out.append(breadcrumb("US-Built Ship Demand", "Without SHIPS Act"))
    out.append(
        title_placeholder(
            "Status Quo Outlook (Oceangoing Commercial)",
            "Replacing retirements unlikely to support serial production, preventing meaningful newbuild cost reductions.",
        )
    )


def paint_retirement_table(out: list[str], ids: ShapeIds) -> None:
    out.append(
        table(
            ids.next(),
            RETIREMENT_TABLE.name,
            *RETIREMENT_TABLE.box.emu(),
            col_widths=[IN(width) for width in RETIREMENT_TABLE.col_widths],
            rows=_retirement_table_rows(),
        )
    )


def paint_paired_legend(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            "Rectangle 840",
            IN(5.283),
            IN(2.488),
            IN(0.932),
            IN(0.98),
            [paragraph([], align="ctr", line_spacing=100_000)],
            fill=None,
            line_color="121415",
            anchor="ctr",
        )
    )

    for entry in LEGEND_ENTRIES:
        out.append(
            text_box(
                ids.next(),
                "LegendSwatch",
                *entry.swatch.emu(),
                [paragraph([], align="ctr", line_spacing=100_000)],
                fill=entry.fill,
                line_color="none",
                anchor="ctr",
            )
        )

    for entry in LEGEND_ENTRIES:
        out.append(
            text_box(
                ids.next(),
                "Label",
                *entry.caption.emu(),
                [paragraph([run(entry.label, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100_000)],
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
            BAR_TOTAL_CALLOUT.name,
            *BAR_TOTAL_CALLOUT.box.emu(),
            [paragraph([run(BAR_TOTAL_CALLOUT.text, size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100_000)],
            fill=BAR_TOTAL_CALLOUT.fill,
            line_color=BAR_TOTAL_CALLOUT.line_color,
            prst=BAR_TOTAL_CALLOUT.prst,
            geom_adj=BAR_TOTAL_CALLOUT.geom_adj,
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            ids.next(),
            "Rectangle 839",
            IN(5.325),
            IN(2.412),
            IN(0.849),
            IN(0.159),
            [
                paragraph(
                    [
                        run("Retirements", size=PT(8), italic=True, color=BLACK, font=FONT),
                        run("1", size=PT(8), italic=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100_000,
                )
            ],
            fill=WHITE,
            line_color="none",
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            ids.next(),
            "Rectangle 688",
            IN(6.247),
            IN(2.488),
            IN(0.932),
            IN(0.98),
            [paragraph([], align="ctr", line_spacing=100_000)],
            fill=None,
            line_color="121415",
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            ids.next(),
            "Rectangle 689",
            IN(6.288),
            IN(2.412),
            IN(0.849),
            IN(0.159),
            [
                paragraph(
                    [
                        run("Orderbook", size=PT(8), italic=True, color=BLACK, font=FONT),
                        run("2", size=PT(8), italic=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100_000,
                )
            ],
            fill=WHITE,
            line_color="none",
            anchor="ctr",
        )
    )


def paint_takeaway_and_notes(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            TAKEAWAY_BANNER.name,
            *TAKEAWAY_BANNER.box.emu(),
            [
                paragraph(
                    [
                        run("~0.2-1.2 vessels per year is insufficient for serial production ", size=PT(12), bold=True, color=BLACK, font=FONT),
                        run("(5+ hulls/yr. to achieve max labor efficiencies by end of year 2)", size=PT(12), italic=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100_000,
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
            SOURCE_NOTE.name,
            *SOURCE_NOTE.box.emu(),
            [
                paragraph(
                    [
                        run(
                            "Note: (1) Service life assumptions – 40 years for Bulk, Container, General Cargo, and RORO, 35 years for Tankers, 30 years for PSVs, and 25 years for Crew/FSVs; (2) All Oceangoing Commercial vessels in orderbook are built at Hanwha Philly, including containerships purchased by Matson and 12x tankers (10x Chemical & Oil and 2x LNG) purchased by Hanwha Shipping | Source: Clarksons (US fleet size and GT data)",
                            size=PT(8),
                            color=BLACK,
                            font=FONT,
                        )
                    ],
                    line_spacing=100_000,
                )
            ],
            fill=None,
            line_color="none",
        )
    )


def paint_serial_production_key(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            "Rectangle 715",
            IN(10.438),
            IN(1.429),
            IN(0.301),
            IN(0.26),
            [paragraph([run("#", size=PT(16), bold=True, color="C30C3E", font=FONT)], align="ctr", line_spacing=100_000)],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            ids.next(),
            "TextBox 716",
            IN(10.694),
            IN(1.442),
            IN(2.101),
            IN(0.234),
            [paragraph([run("Does not support serial production", size=PT(10), font=FONT)], line_spacing=100_000)],
            fill=None,
            line_color="none",
            anchor="ctr",
            wrap="none",
        )
    )
    out.append(
        text_box(
            ids.next(),
            "Rectangle 717",
            IN(10.438),
            IN(1.187),
            IN(0.301),
            IN(0.26),
            [paragraph([run("#", size=PT(16), bold=True, color="007770", font=FONT)], align="ctr", line_spacing=100_000)],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            ids.next(),
            "TextBox 718",
            IN(10.694),
            IN(1.2),
            IN(2.101),
            IN(0.234),
            [paragraph([run("Supports serial production", size=PT(10), font=FONT)], line_spacing=100_000)],
            fill=None,
            line_color="none",
            anchor="ctr",
            wrap="none",
        )
    )


def paint_final_callouts_and_chip(out: list[str], ids: ShapeIds) -> None:
    out.append(prelim_chip())
    out.append(
        text_box(
            ids.next(),
            HANWHA_CALLOUT.name,
            *HANWHA_CALLOUT.box.emu(),
            [paragraph([run(HANWHA_CALLOUT.text, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100_000)],
            fill=HANWHA_CALLOUT.fill,
            line_color=HANWHA_CALLOUT.line_color,
            prst=HANWHA_CALLOUT.prst,
            geom_adj=HANWHA_CALLOUT.geom_adj,
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            ids.next(),
            "Rectangle 4",
            IN(8.069),
            IN(0.174),
            IN(2.977),
            IN(0.217),
            [paragraph([run("(1) Status Quo Scenario", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100_000)],
            fill="CEDDEC",
            line_color=BLACK,
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
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE.
    paint_orderbook_window(out, ids)
    paint_chart(out, ids)
    paint_chart_manual_labels(out, ids)
    paint_chrome(out)
    paint_retirement_table(out, ids)
    paint_paired_legend(out, ids)
    paint_takeaway_and_notes(out, ids)
    paint_serial_production_key(out, ids)
    paint_final_callouts_and_chip(out, ids)

    return "".join(out)


def render() -> str:
    return slide(_body())
