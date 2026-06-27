"""Teaching exemplar: market-sizing level definitions with nested funnel.

ROLE
  definition_diagram / nested_market_level_funnel

USE WHEN
  A reference slide must define a hierarchy of market-sizing levels and pair a
  simple visual containment diagram with a formal definition table.

TEACHES
  - concentric/nested layers as a containment hierarchy, not a process flow
  - BLUE_1 → BLUE_5 depth encoding for progressively narrower market levels
  - largest-first paint order for nested shapes
  - mirrored terminology between diagram labels and definition-table rows
  - how to document a raw layout-placeholder residue without hiding it
  - top-right logo wiring for Navy market-sizing reference pages

TEXT-FIT PRECEDENT
  funnel_tags:
    geometry: 1.949in wide x 0.386in high
    type: Arial default size, bold, centered
    content: one level name only
    copy_when: diagram labels sit directly on color layers rather than in a legend

  definition_table:
    geometry: 6.257in wide x 5.711in high
    type: Arial 14pt, heavy 0.066in cell padding
    content: 5 market levels, each with one compact definition or two short clauses
    copy_when: a visual taxonomy needs an auditable table beside it

SOURCE NOTE
  Teaching rewrite of the source-faithful `definitions_market_levels.py` module.
  The render remains source-faithful in geometry, colors, raw-title residue, logo
  rId, and paint order. This version promotes the funnel and table into explicit
  semantic records so an AI author can copy the pattern deliberately.

FIDELITY NOTE
  The source title is a raw layout placeholder with no explicit xfrm. It is kept
  verbatim here as `RAW_TITLE_PLACEHOLDER_XML`. Rebuild it with title_placeholder()
  only when migrating the slide away from source-fidelity mode.
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
    BLUE_1,
    BLUE_2,
    BLUE_3,
    BLUE_4,
    BLUE_5,
    FONT,
    slide,
    run,
    paragraph,
    text_box,
    picture,
    table,
    trow,
    cell,
    rcell,
    edge,
    tpara,
    trun,
    tbreak,
    breadcrumb,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []
IMAGES = [
    {"rId": "rId2", "file": "image8_3071a231.jpeg"},
]

TEACHING_METADATA = {
    "role": "definition_diagram / nested_market_level_funnel",
    "use_when": (
        "Use when nested market-sizing terms must be taught once and then reused "
        "throughout a deck."
    ),
    "teaches": [
        "largest-first nested-layer paint order",
        "contrast-aware layer tags",
        "right-hand definition table that mirrors diagram terminology",
        "raw title-placeholder residue documented as source fidelity",
        "simple logo slot wiring",
    ],
}

TEXT_FIT = {
    "funnel_tag": {"box_in": (1.949, 0.386), "font_pt": "default run size", "content": "one level name"},
    "definition_table": {"box_in": (6.257, 5.711), "font_pt": 14, "content": "five rows with compact definitions"},
}

COPY_RULES = (
    "Paint nested layers largest-first so each smaller market level remains visible.",
    "Use the exact same market-level names in the diagram and table.",
    "Use white tag text on BLUE_3/4/5 and black tag text on BLUE_1/2.",
    "Keep definition prose short; this slide is a reference, not a methodology page.",
)

RAW_TITLE_PLACEHOLDER_XML = (
    '<p:sp><p:nvSpPr><p:cNvPr id="2000" name="Title 3" />'
    '<p:cNvSpPr><a:spLocks noGrp="1" /></p:cNvSpPr>'
    '<p:nvPr><p:ph type="title" /></p:nvPr></p:nvSpPr><p:spPr />'
    '<p:txBody><a:bodyPr vert="horz" /><a:lstStyle /><a:p><a:pPr marL="0" />'
    '<a:r><a:rPr lang="en-US" dirty="0"><a:solidFill><a:srgbClr val="000000" />'
    '</a:solidFill></a:rPr><a:t>Definitions | Sizing breaks the market down into five levels </a:t>'
    '</a:r></a:p></p:txBody></p:sp>'
)


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class ShapeIds:
    start: int = 100

    def next(self) -> int:
        value = self.start
        object.__setattr__(self, "start", value + 1)
        return value


@dataclass(frozen=True)
class FunnelLevel:
    key: str
    name: str
    layer: Box
    fill: str
    tag: Box
    tag_text_color: str


@dataclass(frozen=True)
class DefinitionRow:
    key: str
    level: str
    row_h: float
    definition_parts: tuple[str, ...]
    label_breaks: int = 0
    separate_definition_paragraphs: bool = False
    blank_definition_paragraph_between: bool = False
    top_rule_width: int = 6350
    bottom_rule_width: int | None = 6350


TAG_BOX = Box(2.352, 0.0, 1.949, 0.386)

FUNNEL_LEVELS: tuple[FunnelLevel, ...] = (
    FunnelLevel("total_funding", "Total Funding", Box(0.477, 1.307, 5.700, 5.700), BLUE_1, Box(2.352, 1.564, 1.949, 0.386), BLACK),
    FunnelLevel("tam", "TAM", Box(0.927, 2.207, 4.800, 4.800), BLUE_2, Box(2.352, 2.464, 1.949, 0.386), BLACK),
    FunnelLevel("sam", "SAM", Box(1.377, 3.107, 3.900, 3.900), BLUE_3, Box(2.352, 3.457, 1.949, 0.386), WHITE),
    FunnelLevel("company_tcv", "Company TCV", Box(1.777, 4.007, 3.100, 3.000), BLUE_4, Box(2.352, 4.450, 1.949, 0.386), WHITE),
    FunnelLevel("company_acv", "Company ACV", Box(2.277, 4.907, 2.100, 2.100), BLUE_5, Box(2.352, 5.800, 1.949, 0.386), WHITE),
)

DEFINITION_ROWS: tuple[DefinitionRow, ...] = (
    DefinitionRow("total_funding", "Total Funding", 0.956, ("All appropriations for relevant platforms, regardless of mission",), top_rule_width=12700),
    DefinitionRow(
        "tam",
        "Total Addressable Market (TAM)",
        1.272,
        (
            "Funding for missions that could be performed by unmanned platforms",
            "Portion of Total Funding for platforms allocated to specific missions",
        ),
        label_breaks=2,
    ),
    DefinitionRow(
        "sam",
        "Serviceable Addressable Market (SAM)",
        1.044,
        (
            "Funding for missions performed by unmanned platforms (i.e., adoption)",
            "Portion of TAM that USVs can likely penetrate",
        ),
        separate_definition_paragraphs=True,
    ),
    DefinitionRow(
        "company_tcv",
        "Company TCV",
        0.956,
        (
            "Funding for Saronic unmanned platforms (i.e., market share)",
            "Share of SAM that Saronic can likely capture",
        ),
        blank_definition_paragraph_between=True,
    ),
    DefinitionRow("company_acv", "Company ACV", 0.956, ("Portion of TCV exercised through Growth and Programs action",), bottom_rule_width=None),
)


def _r(text: str, *, size_pt: float = 14, bold: bool = False, color: str = BLACK):
    return trun(text, size=PT(size_pt), bold=bold or None, color=color, font=FONT)


def _label_cell(row: DefinitionRow):
    # TAM keeps two trailing line breaks from the source to align with its taller definition cell.
    runs = [_r(row.level)] + [tbreak() for _ in range(row.label_breaks)]
    return rcell([tpara(runs, mar_l=0, indent=0)], **TABLE_PAD, T=edge(DK, row.top_rule_width), **({} if row.bottom_rule_width is None else {"B": edge(DK, row.bottom_rule_width)}))


def _definition_cell(row: DefinitionRow):
    if row.separate_definition_paragraphs:
        paras = [tpara([_r(row.definition_parts[0]), tbreak()]), tpara([_r(row.definition_parts[1])])]
    elif row.blank_definition_paragraph_between:
        paras = [tpara([_r(row.definition_parts[0])]), tpara([]), tpara([_r(row.definition_parts[1])])]
    elif len(row.definition_parts) == 2:
        paras = [tpara([_r(row.definition_parts[0]), tbreak(), tbreak(), _r(row.definition_parts[1])])]
    else:
        paras = [tpara([_r(row.definition_parts[0])])]
    return rcell(paras, **TABLE_PAD, T=edge(DK, row.top_rule_width), **({} if row.bottom_rule_width is None else {"B": edge(DK, row.bottom_rule_width)}))


TABLE_PAD = dict(l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960)


def paint_funnel_layers(out: list[str], ids: ShapeIds) -> None:
    for level in FUNNEL_LEVELS:
        out.append(text_box(ids.next(), f"FunnelLayer_{level.key}", *level.layer.emu(), [paragraph([], align="ctr", line_spacing=100_000)], fill=level.fill, line_color="202223", line_width=3175, prst="ellipse"))


def paint_chrome_and_raw_title(out: list[str], ids: ShapeIds) -> None:
    out.append(breadcrumb("Market Sizing", "Navy (Surface incl. MDA)"))
    out.append(RAW_TITLE_PLACEHOLDER_XML)


def paint_definition_table(out: list[str], ids: ShapeIds) -> None:
    rows = [
        trow(
            [
                cell("Level", size=PT(14), bold=True, anchor="b", **TABLE_PAD, B=edge(DK)),
                cell("Definition", size=PT(14), bold=True, anchor="b", **TABLE_PAD, B=edge(DK)),
            ],
            h=IN(0.359),
        )
    ]
    for row in DEFINITION_ROWS:
        rows.append(trow([_label_cell(row), _definition_cell(row)], h=IN(row.row_h)))

    out.append(table(ids.next(), "MarketLevelDefinitionTable", IN(6.577), IN(1.408), IN(6.257), IN(5.711), col_widths=[IN(1.749), IN(4.509)], rows=rows))


def paint_level_tags(out: list[str], ids: ShapeIds) -> None:
    for level in FUNNEL_LEVELS:
        out.append(text_box(ids.next(), f"FunnelTag_{level.key}", *level.tag.emu(), [paragraph([run(level.name, bold=True, color=level.tag_text_color, font=FONT)], align="ctr", line_spacing=100_000)], fill=level.fill, line_color="none", anchor="ctr"))


def paint_logo(out: list[str], ids: ShapeIds) -> None:
    out.append(picture(ids.next(), "ProgramLogo", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))


def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    paint_funnel_layers(out, ids)
    paint_chrome_and_raw_title(out, ids)
    paint_definition_table(out, ids)
    paint_level_tags(out, ids)
    paint_logo(out, ids)

    return "".join(out)


def render() -> str:
    return slide(_body())
