"""Teaching exemplar: DDG-51 outsourced TAM profile with observed SAM overlay.

ROLE
  ddg51_market_sizing / outsourced_demand_lumpiness

USE WHEN
  A slide needs to quantify a modeled supplier-addressable outsourced market by
  fiscal year, separate baseline Basic Construction from one-time overlays, and
  keep an observed transaction lens visually distinct from modeled TAM.

TEACHES
  - factory-native combo_chart with stacked columns plus an editable line overlay
  - explicit TAM/SAM values embedded as Python constants instead of sidecar XLSB
  - source-style manual total labels over a native chart
  - right-side KPI comparison pattern: large numeric card plus explanatory note
  - compact native outyear range table using local table helpers
  - public-source footer wording for modeled analyst calculations

TEXT-FIT PRECEDENT
  tam_profile_chart:
    geometry: 7.100in wide x 3.480in high
    type: native stacked-column + line chart, Arial 9pt axes, manual 8pt labels
    content: six fiscal-year bars and four observed-SAM line points
    copy_when: a program market-sizing slide must show a modeled lens and an
               observed transaction subset on one exhibit

  kpi_pair:
    geometry: 1.420in x 0.700in value card plus 3.190in x 0.700in note box
    type: Arial 18pt bold KPI plus Arial 9pt explanatory label
    content: one headline number; the note must be a short qualifier, not prose

  outyear_range_table:
    geometry: 4.640in wide x 0.650in high
    type: native table, Arial 8pt header / 9pt value cells
    content: FY28E-FY31E low/high outsourced-BC ranges
    copy_when: a forecast range is secondary evidence and should stay compact

SOURCE NOTE
  Built from the provided DDG-51 outsourced-work markdown. The figures on this
  slide are analysis outputs: modeled TAM, observed SAM totals, supplier
  coefficients, outyear ranges, and per-hull estimates are not stated as a single
  public-source fact. The footer therefore uses the corrected public-source
  posture from the accompanying source appendix.

FIDELITY NOTE
  This is a new, factory-native DDG-51 module in the style of the project source
  exemplars. It follows the slide-module contract (`LAYOUT`, `CHARTS`, `_body()`,
  `render()`), keeps chart data and style auditable in Python, and uses semantic
  records plus named paint layers rather than converter-era shape buckets.
"""
# HAND-POLISHED — new DDG-51 teaching module; no converter source exists.
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, Sources, body_slide, combo_chart, connector, graphic_frame,
    line_break, paragraph, run, table, tcell, text_box, trow,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
GRAY_1 = "F2F2F2"
GRAY_2 = "D9D9D9"
GRAY_3 = "BFBFBF"
FONT = "Arial"

LAYOUT = "slideLayout4"

# Local semantic palette. These are DDG-51 exhibit roles, not global tokens.
BC_BLUE = "364D6E"
OBBBA_BLUE = "6F8DB9"
AP_LTTM_GRAY = "BFBFBF"
OBSERVED_SAM_RED = "C30C3E"
CALLOUT_BLUE = "CEDDEC"
OUTYEAR_BLUE = "E2E9EF"
RULE_GRAY = "808080"


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
class TamYear:
    """One fiscal-year row in the TAM/SAM exhibit, all values in FY2026 $M."""

    fiscal_year: str
    bc_stream_m: float
    obbba_m: float
    ap_lltm_m: float
    observed_sam_m: float | None

    @property
    def modeled_tam_m(self) -> float:
        return self.bc_stream_m + self.obbba_m + self.ap_lltm_m


@dataclass(frozen=True)
class KpiPair:
    """Right-rail KPI: a value card paired with a short explanatory note."""

    value: str
    note: str
    value_box: Box
    note_box: Box
    value_fill: str = GRAY_1
    value_color: str = DK


@dataclass(frozen=True)
class BarTotalLabel:
    """Manual label above a modeled-TAM bar."""

    label: str
    box: Box
    text_color: str = BLACK
    fill: str | None = WHITE


@dataclass(frozen=True)
class LegendEntry:
    label: str
    fill: str
    swatch: Box
    label_box: Box
    line_color: str | None = "none"


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


TEACHING_METADATA = {
    "role": "ddg51_market_sizing / outsourced_demand_lumpiness",
    "use_when": (
        "Use for ship-program market-sizing slides where modeled TAM must be "
        "read separately from observed first-tier subaward activity."
    ),
    "teaches": [
        "native combo_chart stacked columns plus line overlay",
        "explicit source values and chart style constants",
        "manual total labels over native charts",
        "right-side KPI pair layout",
        "compact native outyear range table",
        "analyst-calculation source posture",
    ],
    "source_module": "new DDG-51 module",
    "rebuild_strategy": "author directly from markdown data using project factory conventions",
}

TEXT_FIT = {
    "tam_profile_chart": {
        "box_in": (7.100, 3.480),
        "font_pt": "9 axis / 8 total labels",
        "content": "six fiscal-year stacked columns plus observed SAM line overlay",
        "note": "Keep the chart title no-wrap; move method nuance to the right rail or footer.",
    },
    "kpi_pair": {
        "box_in": ((1.420, 0.700), (3.190, 0.700)),
        "font_pt": "18 value / 9 note",
        "content": "short number token plus two-line qualifier",
    },
    "outyear_range_table": {
        "box_in": (4.640, 0.650),
        "font_pt": "8 banner/header / 9 values",
        "content": "banner + four FY range cells",
    },
}

COPY_RULES = [
    "Keep modeled TAM and observed SAM visually separated; they answer different questions.",
    "Always call out FY26 as overlay-driven so it is not read as normalized ship-construction demand.",
    "Use the corrected public-source posture when presenting modeled dollar estimates or coefficients.",
]

NATIVE_CHART_CONTRACT = {
    "factory": "combo_chart(mode='stacked') with line_overlay_axis='same'",
    "bar_series": (
        "Basic Construction stream",
        "OBBBA mandatory overlay",
        "AP / LLTM overlay",
    ),
    "line_series": "Observed SAM subawards (reported first-tier subset)",
    "runtime_assets": "none; chart factory emits a native chart part and embedded .xlsx",
    "manual_shapes": "chart title, modeled-TAM total labels, manual legend, KPI rail, FY26 callout, outyear table",
}

# ════════════════════════════════════════════════════════════════════════════
# Source data: constant FY2026 $M.
# ════════════════════════════════════════════════════════════════════════════
TAM_YEARS: tuple[TamYear, ...] = (
    TamYear("FY22", 474, 0, 0, 163),
    TamYear("FY23", 1234, 0, 0, 289),
    TamYear("FY24", 874, 0, 0, 568),
    TamYear("FY25", 1194, 0, 42, 698),
    TamYear("FY26E", 71, 858, 1000, None),
    TamYear("FY27E", 674, 0, 0, None),
)

CHART_CATEGORIES: tuple[str, ...] = tuple(row.fiscal_year for row in TAM_YEARS)
MODELED_TOTALS_M: tuple[float, ...] = tuple(row.modeled_tam_m for row in TAM_YEARS)
OBSERVED_SAM_VALUES_M: tuple[float | None, ...] = tuple(row.observed_sam_m for row in TAM_YEARS)

# FY28-FY31 low/high outsourced Basic Construction range, FY2026 $M.
OUTYEAR_RANGES_M: tuple[tuple[str, str], ...] = (
    ("FY28E", "$557-577M"),
    ("FY29E", "$570-614M"),
    ("FY30E", "$876-981M"),
    ("FY31E", "$903-1,052M"),
)

TAM_STREAM_SERIES: tuple[dict, ...] = (
    {
        "name": "Basic Construction stream",
        "color": BC_BLUE,
        "values": [row.bc_stream_m for row in TAM_YEARS],
        "hide_labels": True,
    },
    {
        "name": "OBBBA mandatory overlay",
        "color": OBBBA_BLUE,
        "values": [row.obbba_m for row in TAM_YEARS],
        "hide_labels": True,
    },
    {
        "name": "AP / LLTM overlay",
        "color": AP_LTTM_GRAY,
        "values": [row.ap_lltm_m for row in TAM_YEARS],
        "hide_labels": True,
        "label_color": BLACK,
    },
)

OBSERVED_SAM_LINE = {
    "name": "Observed SAM subawards",
    "values": list(OBSERVED_SAM_VALUES_M),
    "color": OBSERVED_SAM_RED,
    "width": 19_050,
    "marker": "circle",
    "marker_size": 6,
    "smooth": False,
}

_CHART0_DATA = {
    "categories": CHART_CATEGORIES,
    "series": [
        {"name": series["name"], "values": list(series["values"])}
        for series in TAM_STREAM_SERIES
    ] + [{"name": OBSERVED_SAM_LINE["name"], "values": list(OBSERVED_SAM_VALUES_M)}],
}

# Source-like native chart style. Manual labels carry the bar totals, so the
# chart keeps native data labels off and leaves enough plot space for overlays.
SOURCE_PLOT_LAYOUT = {
    "x": 0.075,
    "y": 0.085,
    "w": 0.885,
    "h": 0.810,
}
VALUE_AXIS_MAX_M = 2200

CHART_STYLE = {
    "mode": "stacked",
    "categories": list(CHART_CATEGORIES),
    "series": [dict(series) for series in TAM_STREAM_SERIES],
    "line_overlay": [dict(OBSERVED_SAM_LINE)],
    "line_overlay_axis": "same",
    "show_legend": False,
    "show_cat_labels": True,
    "show_value_axis_labels": True,
    "show_gridlines": False,
    "show_value_labels": False,
    "value_axis_format": '$#,##0"M"',
    "cat_label_size_pt": 9,
    "value_label_size_pt": 9,
    "gap_width": 70,
    "bar_overlap": 100,
    "seg_line_color": None,
    "axis_line_color": BLACK,
    "axis_line_width": 9_525,
    "value_axis_line_color": "inherit",
    "value_axis_min": 0,
    "value_axis_max": VALUE_AXIS_MAX_M,
    "value_axis_major_unit": 500,
    "cat_axis_crosses": "min",
    "value_axis_crosses": "min",
    "plot_layout": dict(SOURCE_PLOT_LAYOUT),
    "cat_header": "Fiscal year",
}

CHARTS = [combo_chart(**CHART_STYLE)]

# ════════════════════════════════════════════════════════════════════════════
# Layout zones.
# ════════════════════════════════════════════════════════════════════════════
CHART_FRAME = Box(0.540, 1.770, 7.100, 3.480)
CHART_TITLE = Box(0.585, 1.505, 7.000, 0.205)
LEGEND_Y = 5.395

KPI_PAIRS: tuple[KpiPair, ...] = (
    KpiPair(
        "$6.42B",
        "FY22-FY27 modeled outsourced TAM across all streams",
        Box(8.020, 1.560, 1.420, 0.700),
        Box(9.520, 1.560, 3.190, 0.700),
        CALLOUT_BLUE,
    ),
    KpiPair(
        "$1.07B/yr",
        "average annual modeled TAM over FY22-FY27",
        Box(8.020, 2.395, 1.420, 0.700),
        Box(9.520, 2.395, 3.190, 0.700),
    ),
    KpiPair(
        "~$412M",
        "FY25 per-hull TAM anchor from the 3-ship buy",
        Box(8.020, 3.230, 1.420, 0.700),
        Box(9.520, 3.230, 3.190, 0.700),
    ),
)

FY26_CALLOUT = Box(8.020, 4.075, 4.690, 0.690)
OUTYEAR_TABLE = Box(8.020, 5.045, 4.640, 0.650)
METHOD_CUE = Box(8.020, 4.790, 4.640, 0.170)

LEGEND_ENTRIES: tuple[LegendEntry, ...] = (
    LegendEntry("BC stream", BC_BLUE, Box(0.825, LEGEND_Y, 0.160, 0.110), Box(1.030, LEGEND_Y - 0.030, 1.050, 0.170)),
    LegendEntry("OBBBA mandatory", OBBBA_BLUE, Box(2.085, LEGEND_Y, 0.160, 0.110), Box(2.290, LEGEND_Y - 0.030, 1.420, 0.170)),
    LegendEntry("AP / LLTM", AP_LTTM_GRAY, Box(3.885, LEGEND_Y, 0.160, 0.110), Box(4.090, LEGEND_Y - 0.030, 1.100, 0.170), BLACK),
)
SAM_LEGEND_LINE = Box(5.490, LEGEND_Y + 0.055, 0.330, 0.000)
SAM_LEGEND_LABEL = Box(5.900, LEGEND_Y - 0.030, 1.420, 0.170)


def _bar_total_label_box(idx: int, value_m: float) -> Box:
    """Approximate native-plot coordinates for source-style manual bar labels."""

    plot_x = CHART_FRAME.x + SOURCE_PLOT_LAYOUT["x"] * CHART_FRAME.w
    plot_y = CHART_FRAME.y + SOURCE_PLOT_LAYOUT["y"] * CHART_FRAME.h
    plot_w = SOURCE_PLOT_LAYOUT["w"] * CHART_FRAME.w
    plot_h = SOURCE_PLOT_LAYOUT["h"] * CHART_FRAME.h
    bar_x = plot_x + ((idx + 0.5) * plot_w / len(TAM_YEARS)) - 0.255
    bar_y = plot_y + (1 - (value_m / VALUE_AXIS_MAX_M)) * plot_h - 0.165
    return Box(bar_x, max(1.695, bar_y), 0.510, 0.150)


def _fmt_bar_total(value_m: float) -> str:
    if value_m >= 1000:
        return f"${value_m / 1000:.2f}B"
    return f"${int(value_m):,}M"


BAR_TOTAL_LABELS: tuple[BarTotalLabel, ...] = tuple(
    BarTotalLabel(_fmt_bar_total(value), _bar_total_label_box(i, value))
    for i, value in enumerate(MODELED_TOTALS_M)
)

# ════════════════════════════════════════════════════════════════════════════
# Low-level local table kit.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Border map from only the sides drawn; omitted sides render no-fill."""

    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text: str = "", *, fill=None, bold=None, italic=None, color=BLACK,
         size=PT(8), align="ctr", anchor="ctr", span=1,
         l_ins=30_480, r_ins=30_480, t_ins=15_240, b_ins=15_240, **edges):
    """Single-run table cell; borders via L/R/T/B=edge(...)."""

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
        font=FONT,
        l_ins=l_ins,
        r_ins=r_ins,
        t_ins=t_ins,
        b_ins=b_ins,
        borders=bd(**edges),
    )


# ════════════════════════════════════════════════════════════════════════════
# Tiny local authoring helpers.
# ════════════════════════════════════════════════════════════════════════════
def _textbox(sp_id: int, name: str, box: Box, paras: list[str], **kwargs) -> str:
    """text_box() wrapper that accepts semantic Box objects."""

    return text_box(sp_id, name, *box.emu(), paras, **kwargs)


def _one_line(text: str, *, size: int = PT(10), bold: bool = False,
              italic: bool = False, color: str = BLACK,
              align: str | None = None) -> str:
    """Tight one-run paragraph for labels, chips, and captions."""

    return paragraph(
        [run(text, size=size, bold=bold or None, italic=italic or None, color=color, font=FONT)],
        align=align,
        mar_l=0,
        indent=0,
        line_spacing=100000,
    )


def _empty_paragraph() -> str:
    return paragraph([], align="ctr", line_spacing=100000)


# ════════════════════════════════════════════════════════════════════════════
# Paint functions. Paint order mirrors source-style chart slides:
# chart -> labels/legend -> right rail -> compact table.
# ════════════════════════════════════════════════════════════════════════════
def paint_native_chart(n) -> list[str]:
    chart_x, chart_y, chart_cx, chart_cy = CHART_FRAME.emu()
    return [
        _textbox(
            n(),
            "ChartTitle",
            CHART_TITLE,
            [_one_line("Modeled DDG-51 outsourced TAM by stream vs. observed reported subawards ($M, FY26$)", size=PT(10), bold=True)],
            fill=None,
            line_color="none",
            anchor="b",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        ),
        graphic_frame(sp_id=n(), name="DDG51TAMProfileChart", x=chart_x, y=chart_y, cx=chart_cx, cy=chart_cy, rId="rId2"),
    ]


def paint_manual_total_labels(n) -> list[str]:
    shapes: list[str] = []
    for label in BAR_TOTAL_LABELS:
        shapes.append(_textbox(
            n(),
            "BarTotalLabel",
            label.box,
            [_one_line(label.label, size=PT(8), bold=True, color=label.text_color, align="ctr")],
            fill=label.fill,
            line_color="none",
            anchor="ctr",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        ))
    return shapes


def paint_manual_legend(n) -> list[str]:
    shapes: list[str] = []
    for entry in LEGEND_ENTRIES:
        shapes.append(_textbox(
            n(),
            "LegendSwatch",
            entry.swatch,
            [_empty_paragraph()],
            fill=entry.fill,
            line_color=entry.line_color,
            line_width=6_350,
            anchor="ctr",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        ))
        shapes.append(_textbox(
            n(),
            "LegendLabel",
            entry.label_box,
            [_one_line(entry.label, size=PT(8))],
            fill=None,
            line_color="none",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        ))
    shapes.append(connector(n(), "SAMLegendLine", *SAM_LEGEND_LINE.emu(), color=OBSERVED_SAM_RED, width=19_050))
    shapes.append(_textbox(
        n(),
        "SAMLegendLabel",
        SAM_LEGEND_LABEL,
        [_one_line("Observed SAM", size=PT(8))],
        fill=None,
        line_color="none",
        wrap="none",
        l_ins=0,
        t_ins=0,
        r_ins=0,
        b_ins=0,
    ))
    return shapes


def paint_kpi_pairs(n) -> list[str]:
    shapes: list[str] = []
    for pair in KPI_PAIRS:
        shapes.append(_textbox(
            n(),
            "KpiValueCard",
            pair.value_box,
            [_one_line(pair.value, size=PT(18), bold=True, color=pair.value_color, align="ctr")],
            fill=pair.value_fill,
            line_color="none",
            anchor="ctr",
        ))
        shapes.append(_textbox(
            n(),
            "KpiQualifier",
            pair.note_box,
            [_one_line(pair.note, size=PT(9), color=BLACK, align=None)],
            fill=None,
            line_color="none",
            anchor="ctr",
            l_ins=0,
            r_ins=0,
            t_ins=0,
            b_ins=0,
        ))
    return shapes


def paint_fy26_callout(n) -> list[str]:
    return [
        _textbox(
            n(),
            "FY26OverlayCallout",
            FY26_CALLOUT,
            [paragraph([
                run("FY26E spike is overlay-driven", size=PT(11), bold=True, color=DK, font=FONT),
                line_break(),
                run("$858M OBBBA + $1.0B AP/LLTM; BC stream only $71M", size=PT(9), color=BLACK, font=FONT),
            ], align="ctr", line_spacing=100000, mar_l=0, indent=0)],
            fill=CALLOUT_BLUE,
            line_color=DK,
            line_width=12_700,
            anchor="ctr",
        ),
        _textbox(
            n(),
            "MethodCue",
            METHOD_CUE,
            [_one_line("TAM = modeled market lens; SAM = reported first-tier subaward subset", size=PT(8), italic=True, align="ctr")],
            fill=None,
            line_color="none",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        ),
    ]


def paint_outyear_range_table(n) -> list[str]:
    rows = [
        trow([
            cell("FY28-FY31E outsourced BC range", fill=DK, color=WHITE, bold=True, span=4, size=PT(8), T=edge(DK), B=edge(DK)),
        ], h=IN(0.170)),
        trow([
            cell(year, fill=GRAY_2, bold=True, size=PT(8), B=edge(WHITE, 6_350))
            for year, _value in OUTYEAR_RANGES_M
        ], h=IN(0.185)),
        trow([
            cell(value, fill=OUTYEAR_BLUE, bold=True, size=PT(8.5), B=edge(RULE_GRAY, 6_350))
            for _year, value in OUTYEAR_RANGES_M
        ], h=IN(0.275)),
    ]
    x, y, w, h = OUTYEAR_TABLE.emu()
    return [table(
        n(),
        "OutyearRangeTable",
        x,
        y,
        w,
        h,
        col_widths=[IN(1.160)] * 4,
        rows=rows,
        first_row=False,
        first_col=False,
        band_row=False,
    )]


def _body() -> str:
    shapes: list[str] = []
    ids = ShapeIds()
    n = ids.next

    shapes.extend(paint_native_chart(n))
    shapes.extend(paint_manual_total_labels(n))
    shapes.extend(paint_manual_legend(n))
    shapes.extend(paint_kpi_pairs(n))
    shapes.extend(paint_fy26_callout(n))
    shapes.extend(paint_outyear_range_table(n))
    return "".join(shapes)


CHROME = Chrome(
    section="DDG-51 Outsourcing",
    topic="Market Sizing",
    title="DDG-51 Outsourced TAM Profile",
    takeaway="$6.4B FY22-FY27 modeled TAM, but annual demand is lumpy and FY26 is overlay-driven.",
    sources=Sources(
        source=(
            "Department of the Navy FY2027 SCN justification book",
            "DoD FY2027 P-1",
            "GovInfo Public Law 119-21",
            "FY2026 Mandatory Funding Allocation Plan",
            "DoD Green Book deflators",
            "DoD/Navy DDG-51 MYP announcements",
            "USAspending/SAM.gov reported subaward data",
        ),
        note=(
            "Modeled dollar amounts are analyst calculations using public sources; "
            "figures are constant FY2026 dollars and not stated directly in one public source."
        ),
    ),
)


def render() -> str:
    return body_slide(CHROME, _body())
