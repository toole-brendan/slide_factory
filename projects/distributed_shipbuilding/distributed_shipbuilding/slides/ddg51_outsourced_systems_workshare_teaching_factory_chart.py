"""Teaching exemplar: DDG-51 outsourced workshare by SWBS with structural anchors.

ROLE
  ddg51_workshare_composition / systems_equipment_outsourcing

USE WHEN
  A slide needs to show that DDG-51 observed outsourced work is concentrated in
  machinery, equipment, electrical, auxiliary, and pre-outfitting content rather
  than primarily bare hull fabrication.

TEACHES
  - factory-native ranked horizontal bar chart with per-point SWBS colors
  - explicit SWBS mix values embedded as Python constants, no sidecar workbook
  - right-side executive callout that states both total-share and mapped-share
  - compact evidence table built with local native-table helpers
  - structural-unit anchor table with clear analyst-allocation caveat
  - public-source footer wording for SWBS shares and output classifications

TEXT-FIT PRECEDENT
  ranked_swbs_chart:
    geometry: 6.960in wide x 3.620in high
    type: native horizontal bar chart, 8 categories, Arial 8pt labels
    content: eight SWBS major groups with $M data labels
    copy_when: a composition slide needs rank order and exact values more than a
               time-series profile

  evidence_table:
    geometry: 5.100in wide x 1.415in high
    type: native table, Arial 8.5-9pt, short clause cells
    content: three interpretation rows tied back to the chart
    copy_when: the chart needs an auditable explanation but not a prose rail

  structural_anchor_table:
    geometry: 5.100in wide x 0.825in high
    type: native table, Arial 8-9pt, two data rows
    content: grand-block and structural-unit cost allocation anchors
    copy_when: a workshare slide must acknowledge distributed-build modules
               without implying actual subcontract quotes

SOURCE NOTE
  Built from the provided DDG-51 outsourced-work markdown. SWBS dollars, mapped
  shares, output-taxonomy interpretation, supplier counts, and structural-unit
  anchors are analysis outputs/classifications, not figures directly stated in a
  single public source.

FIDELITY NOTE
  This is a new, factory-native DDG-51 module in the style of the project source
  exemplars. It follows the slide-module contract (`LAYOUT`, `CHARTS`, `_body()`,
  `render()`), keeps chart data/style auditable in Python, and uses semantic
  records plus named paint layers rather than converter-era shape buckets.
"""
# HAND-POLISHED — new DDG-51 teaching module; no converter source exists.
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, Sources, bar_chart, body_slide, graphic_frame, paragraph, run,
    table, tcell, tcell_rich, text_box, tpara, trow, trun,
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

# Local semantic palette. These colors encode SWBS / workshare meaning.
AUX_SYSTEMS_BLUE = "364D6E"
PROPULSION_BLUE = "4C6C9C"
ELECTRIC_BLUE = "6F8DB9"
UNMAPPED_GRAY = "A6A6A6"
MINOR_GRAY = "D9D9D9"
HULL_SIGNAL_RED = "C30C3E"
CALLOUT_BLUE = "CEDDEC"
ANCHOR_BLUE = "E2E9EF"
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
class SwbsRow:
    """One SWBS major group in the observed DDG-51 subaward composition."""

    major_group: str
    value_m: float
    share_of_total: str
    fill: str
    interpretation: str


@dataclass(frozen=True)
class EvidenceRow:
    """One short interpretation row in the right-side evidence table."""

    signal: str
    evidence: str
    fill: str | None = None
    text_color: str = BLACK


@dataclass(frozen=True)
class StructuralAnchorRow:
    """One modular-construction cost-allocation anchor."""

    package: str
    total_bc: str
    supplier_addressable: str


@dataclass(frozen=True)
class LegendEntry:
    label: str
    fill: str
    swatch: Box
    label_box: Box


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


TEACHING_METADATA = {
    "role": "ddg51_workshare_composition / systems_equipment_outsourcing",
    "use_when": (
        "Use for naval-platform supplier-base slides where observed subaward "
        "composition must distinguish systems/equipment from bare structural work."
    ),
    "teaches": [
        "native ranked horizontal bar chart",
        "per-point SWBS colors",
        "right-side executive share callout",
        "native evidence table using local helpers",
        "structural-unit cost-allocation table",
        "analyst-classification source posture",
    ],
    "source_module": "new DDG-51 module",
    "rebuild_strategy": "author directly from markdown data using project factory conventions",
}

TEXT_FIT = {
    "ranked_swbs_chart": {
        "box_in": (6.960, 3.620),
        "font_pt": "8 category / 8 value labels",
        "content": "8 SWBS major groups with $M labels",
        "note": "Keep labels short; explanatory examples belong in the evidence table.",
    },
    "evidence_table": {
        "box_in": (5.100, 1.415),
        "font_pt": "8.5-9",
        "content": "three rows: systems signal, output taxonomy, hull contrast",
    },
    "structural_anchor_table": {
        "box_in": (5.100, 0.825),
        "font_pt": "8-9",
        "content": "two package rows and three columns",
    },
}

COPY_RULES = [
    "Keep U00 No SWBS Evidence visually distinct; do not fold it into a system group.",
    "Tie work-type interpretation to both SWBS evidence and output-taxonomy classification.",
    "Label grand-block / structural-unit values as cost-allocation anchors, not subcontract quotes.",
]

NATIVE_CHART_CONTRACT = {
    "factory": "bar_chart(mode='ranked')",
    "visible_encoding": {
        "category": "SWBS major group",
        "bar_length": "observed subaward dollars, FY2026 $M",
        "bar_color": "system/equipment groups, unmapped, hull signal, minor buckets",
    },
    "runtime_assets": "none; chart factory emits a native chart part and embedded .xlsx",
    "manual_shapes": "chart title, small legend note, right-side callout and native evidence/anchor tables",
}

# ════════════════════════════════════════════════════════════════════════════
# Source data: FY2026 $M, HII-Ingalls DDG-51 SWBS-coded subaward view.
# ════════════════════════════════════════════════════════════════════════════
SWBS_ROWS: tuple[SwbsRow, ...] = (
    SwbsRow("500 Auxiliary Systems", 1106, "27.9%", AUX_SYSTEMS_BLUE, "pumps, piping, ventilation, cooling, fire, steering, RAS"),
    SwbsRow("200 Propulsion Plant", 1094, "27.6%", PROPULSION_BLUE, "gas turbines, gears, shafting, bearings, propulsors"),
    SwbsRow("300 Electric Plant", 896, "22.6%", ELECTRIC_BLUE, "generation, conversion, switchgear, panels, motors"),
    SwbsRow("U00 No SWBS Evidence", 684, "17.3%", UNMAPPED_GRAY, "unmapped / insufficient evidence"),
    SwbsRow("600 Outfit & Furnishings", 73, "1.8%", MINOR_GRAY, "closures, coating, cathodic protection, deck covering"),
    SwbsRow("400 Command / Control", 56, "1.4%", MINOR_GRAY, "interior comms, alarms, radar/degaussing references"),
    SwbsRow("100 Hull Structure", 28, "0.7%", HULL_SIGNAL_RED, "small observed hull-structure signal"),
    SwbsRow("Other / Cross-cutting", 21, "0.5%", GRAY_3, "noise/vibration, legacy SWBS, ammunition handling"),
)

SYSTEM_GROUP_VALUE_M = 1106 + 1094 + 896
TOTAL_SWBS_VALUE_M = 3957
MAPPED_SWBS_VALUE_M = TOTAL_SWBS_VALUE_M - 684
SYSTEM_SHARE_TOTAL = SYSTEM_GROUP_VALUE_M / TOTAL_SWBS_VALUE_M
SYSTEM_SHARE_MAPPED = SYSTEM_GROUP_VALUE_M / MAPPED_SWBS_VALUE_M

EVIDENCE_ROWS: tuple[EvidenceRow, ...] = (
    EvidenceRow("SWBS signal", "Auxiliary + Propulsion + Electric = $3.10B / 78% of total", CALLOUT_BLUE),
    EvidenceRow("Mapped-spend view", "same three groups are ~95% excluding U00 No SWBS Evidence"),
    EvidenceRow("Hull contrast", "Hull Structure = $28M / 0.7%; treat bare-steel inference cautiously", GRAY_1),
)

STRUCTURAL_ANCHORS: tuple[StructuralAnchorRow, ...] = (
    StructuralAnchorRow("Grand block", "$74.9M", "~$19.0M"),
    StructuralAnchorRow("Structural unit", "$21.9M", "~$5.5M"),
)

CHART_CATEGORIES: tuple[str, ...] = tuple(row.major_group for row in SWBS_ROWS)
CHART_VALUES_M: tuple[float, ...] = tuple(row.value_m for row in SWBS_ROWS)
CHART_FILLS: tuple[str, ...] = tuple(row.fill for row in SWBS_ROWS)

_CHART0_DATA = {
    "categories": CHART_CATEGORIES,
    "series": [{"name": "Subaward $M", "values": list(CHART_VALUES_M)}],
}

CHART_STYLE = {
    "mode": "ranked",
    "categories": list(CHART_CATEGORIES),
    "series": [
        {
            "name": "Subaward $M",
            "values": list(CHART_VALUES_M),
            "color": AUX_SYSTEMS_BLUE,
            "data_point_colors": list(CHART_FILLS),
            "label_color": BLACK,
        }
    ],
    "show_legend": False,
    "show_cat_labels": True,
    "show_value_axis_labels": False,
    "show_gridlines": False,
    "show_value_labels": True,
    "value_axis_format": '#,##0"M"',
    "value_label_format": '#,##0"M"',
    "cat_label_size_pt": 8,
    "cat_label_bold": False,
    "value_label_size_pt": 8,
    "value_label_bold": True,
    "gap_width": 60,
    "bar_overlap": 0,
    "seg_line_color": None,
    "axis_line_color": BLACK,
    "axis_line_width": 9_525,
    "value_axis_line_color": "none",
    "value_axis_min": 0,
    "value_axis_max": 1250,
    "value_axis_major_unit": 250,
    "plot_layout": {
        "x": 0.255,
        "y": 0.030,
        "w": 0.675,
        "h": 0.925,
    },
    "cat_header": "SWBS major group",
}

CHARTS = [bar_chart(**CHART_STYLE)]

# ════════════════════════════════════════════════════════════════════════════
# Layout zones.
# ════════════════════════════════════════════════════════════════════════════
CHART_TITLE = Box(0.585, 1.505, 6.900, 0.205)
CHART_FRAME = Box(0.520, 1.760, 6.960, 3.620)
CHART_NOTE = Box(0.585, 5.520, 6.850, 0.285)

SHARE_CALLOUT = Box(7.710, 1.535, 5.100, 0.835)
EVIDENCE_TABLE = Box(7.710, 2.575, 5.100, 1.415)
ANCHOR_TITLE = Box(7.710, 4.210, 5.100, 0.185)
ANCHOR_TABLE = Box(7.710, 4.445, 5.100, 0.825)
ANCHOR_NOTE = Box(7.710, 5.435, 5.100, 0.340)

LEGEND_ENTRIES: tuple[LegendEntry, ...] = (
    LegendEntry("systems/equipment", AUX_SYSTEMS_BLUE, Box(0.820, 5.640, 0.145, 0.100), Box(1.010, 5.612, 1.380, 0.150)),
    LegendEntry("unmapped", UNMAPPED_GRAY, Box(2.530, 5.640, 0.145, 0.100), Box(2.720, 5.612, 0.900, 0.150)),
    LegendEntry("hull signal", HULL_SIGNAL_RED, Box(3.820, 5.640, 0.145, 0.100), Box(4.010, 5.612, 0.900, 0.150)),
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
         size=PT(9), align="l", anchor="ctr", span=1, rowspan=1,
         l_ins=45_720, r_ins=45_720, t_ins=30_480, b_ins=30_480, **edges):
    """Single-run text cell; borders via L/R/T/B=edge(...)."""

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
        borders=bd(**edges),
    )


def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45_720, r_ins=45_720, t_ins=30_480, b_ins=30_480, **edges):
    """Multi-paragraph rich cell; borders via L/R/T/B=edge(...)."""

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
        borders=bd(**edges),
    )


def table_para(text: str, *, size_pt: float = 9, bold: bool = False,
               italic: bool = False, color: str = BLACK,
               align: str = "l"):
    """One rich table paragraph."""

    return tpara(
        [trun(text, size=PT(size_pt), bold=bold or None, italic=italic or None, color=color, font=FONT)],
        align=align,
        line_spacing=100000,
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
# Paint functions.
# ════════════════════════════════════════════════════════════════════════════
def paint_native_chart(n) -> list[str]:
    chart_x, chart_y, chart_cx, chart_cy = CHART_FRAME.emu()
    return [
        _textbox(
            n(),
            "ChartTitle",
            CHART_TITLE,
            [_one_line("DDG-51 observed outsourced work by SWBS major group ($M, FY26$)", size=PT(10), bold=True)],
            fill=None,
            line_color="none",
            anchor="b",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        ),
        graphic_frame(sp_id=n(), name="DDG51SWBSWorkshareChart", x=chart_x, y=chart_y, cx=chart_cx, cy=chart_cy, rId="rId2"),
    ]


def paint_chart_note_and_legend(n) -> list[str]:
    shapes: list[str] = [
        _textbox(
            n(),
            "ChartEvidenceNote",
            CHART_NOTE,
            [_one_line("U00 remains unmapped; systems/equipment interpretation is based on mapped SWBS plus output taxonomy.", size=PT(8), italic=True, align="ctr")],
            fill=None,
            line_color="none",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        )
    ]
    for entry in LEGEND_ENTRIES:
        shapes.append(_textbox(
            n(),
            "LegendSwatch",
            entry.swatch,
            [_empty_paragraph()],
            fill=entry.fill,
            line_color="none",
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
            anchor="ctr",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        ))
    return shapes


def paint_share_callout(n) -> list[str]:
    return [
        _textbox(
            n(),
            "SystemsShareCalloutFill",
            SHARE_CALLOUT,
            [_empty_paragraph()],
            fill=CALLOUT_BLUE,
            line_color="none",
            anchor="ctr",
        ),
        _textbox(
            n(),
            "SystemsShareTitle",
            Box(SHARE_CALLOUT.x, SHARE_CALLOUT.y + 0.090, SHARE_CALLOUT.w, 0.170),
            [_one_line("Auxiliary + Propulsion + Electric", size=PT(10), bold=True, color=DK, align="ctr")],
            fill=None,
            line_color="none",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        ),
        _textbox(
            n(),
            "SystemsShareHeadline",
            Box(SHARE_CALLOUT.x, SHARE_CALLOUT.y + 0.310, SHARE_CALLOUT.w, 0.260),
            [_one_line("$3.10B / 78% of total", size=PT(18), bold=True, color=DK, align="ctr")],
            fill=None,
            line_color="none",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        ),
        _textbox(
            n(),
            "SystemsShareQualifier",
            Box(SHARE_CALLOUT.x, SHARE_CALLOUT.y + 0.610, SHARE_CALLOUT.w, 0.160),
            [_one_line("~95% of mapped spend excluding No SWBS Evidence", size=PT(8.5), color=BLACK, align="ctr")],
            fill=None,
            line_color="none",
            wrap="none",
            l_ins=0,
            t_ins=0,
            r_ins=0,
            b_ins=0,
        ),
    ]


def paint_evidence_table(n) -> list[str]:
    rows = [
        trow([
            cell("Signal", fill=DK, color=WHITE, bold=True, size=PT(8.5), align="ctr", B=edge(DK)),
            cell("What it supports", fill=DK, color=WHITE, bold=True, size=PT(8.5), align="ctr", B=edge(DK)),
        ], h=IN(0.215)),
    ]
    for row in EVIDENCE_ROWS:
        rows.append(trow([
            cell(row.signal, fill=row.fill, bold=True, size=PT(8.5), B=edge(RULE_GRAY, 6_350)),
            rcell(
                [table_para(row.evidence, size_pt=8.5)],
                fill=row.fill,
                B=edge(RULE_GRAY, 6_350),
                l_ins=45_720,
                r_ins=30_480,
                t_ins=15_240,
                b_ins=15_240,
            ),
        ], h=IN(0.385)))
    x, y, w, h = EVIDENCE_TABLE.emu()
    return [table(
        n(),
        "EvidenceTable",
        x,
        y,
        w,
        h,
        col_widths=[IN(1.210), IN(3.890)],
        rows=rows,
        first_row=False,
        first_col=False,
        band_row=False,
    )]


def paint_structural_anchor_table(n) -> list[str]:
    shapes: list[str] = [
        _textbox(
            n(),
            "StructuralAnchorTitle",
            ANCHOR_TITLE,
            [_one_line("Structural-unit cost-allocation anchors", size=PT(10), bold=True)],
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
    rows = [
        trow([
            cell("Package", fill=DK, color=WHITE, bold=True, size=PT(8), align="ctr", B=edge(DK)),
            cell("Total FY25 BC", fill=DK, color=WHITE, bold=True, size=PT(8), align="ctr", B=edge(DK)),
            cell("Supplier-addressable", fill=DK, color=WHITE, bold=True, size=PT(8), align="ctr", B=edge(DK)),
        ], h=IN(0.190)),
    ]
    for anchor in STRUCTURAL_ANCHORS:
        rows.append(trow([
            cell(anchor.package, fill=GRAY_1, bold=True, size=PT(8.5), B=edge(RULE_GRAY, 6_350)),
            cell(anchor.total_bc, fill=ANCHOR_BLUE, bold=True, size=PT(9), align="ctr", B=edge(RULE_GRAY, 6_350)),
            cell(anchor.supplier_addressable, fill=ANCHOR_BLUE, bold=True, size=PT(9), align="ctr", B=edge(RULE_GRAY, 6_350)),
        ], h=IN(0.295)))
    x, y, w, h = ANCHOR_TABLE.emu()
    shapes.append(table(
        n(),
        "StructuralAnchorTable",
        x,
        y,
        w,
        h,
        col_widths=[IN(1.500), IN(1.570), IN(2.030)],
        rows=rows,
        first_row=False,
        first_col=False,
        band_row=False,
    ))
    shapes.append(_textbox(
        n(),
        "StructuralAnchorNote",
        ANCHOR_NOTE,
        [_one_line("Note: anchors allocate ship Basic Construction cost across modular hierarchy; they are not subcontract quotes.", size=PT(8), italic=True, align="ctr")],
        fill=None,
        line_color="none",
        l_ins=0,
        t_ins=0,
        r_ins=0,
        b_ins=0,
    ))
    return shapes


def _body() -> str:
    shapes: list[str] = []
    ids = ShapeIds()
    n = ids.next

    shapes.extend(paint_native_chart(n))
    shapes.extend(paint_chart_note_and_legend(n))
    shapes.extend(paint_share_callout(n))
    shapes.extend(paint_evidence_table(n))
    shapes.extend(paint_structural_anchor_table(n))
    return "".join(shapes)


CHROME = Chrome(
    section="DDG-51 Outsourcing",
    topic="Workshare Composition",
    title="DDG-51 Outsourced Workshare Mix",
    takeaway="Observed outsourcing is systems/equipment-heavy; hull structure is a small observed signal.",
    sources=Sources(
        source=(
            "USAspending/SAM.gov reported subaward data",
            "Navy DDG-51 fact file and Surface Force DDG class page",
            "HII/BIW DDG-51 public pages",
            "Eastern Shipbuilding, HII, Marine Log, WorkBoat, USNI, and supplier public releases",
        ),
        note=(
            "SWBS shares, output taxonomy, supplier counts, and structural-unit anchors "
            "are analyst classifications/allocations, not directly stated public-source facts."
        ),
    ),
)


def render() -> str:
    return body_slide(CHROME, _body())
