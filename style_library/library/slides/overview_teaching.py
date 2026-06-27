"""Teaching exemplar: Overview two-column context/objectives slide.

ROLE
  deck_orientation / executive_context

USE WHEN
  A slide needs to orient the reader before a strategy or market-analysis deck:
  one short Context block, one denser Objectives block, and a bottom preliminary
  banner that frames the rest of the document as still-evolving analysis.

TEACHES
  - maintain a nonstandard source layout via `LAYOUT = "slideLayout3"`
  - keep a layout-native title placeholder when the source placeholder has no xfrm
  - author dense native tables through semantic paragraph records
  - separate table CONTENT from table MECHANICS with local cell / border helpers
  - preserve bullet hierarchy, italic prefix runs, table rules, and text colors
  - use a bottom banner callout without converting it into a table row

TEXT-FIT PRECEDENT
  context_table:
    geometry: 5.700in wide x 3.089in high, one-column native table
    type: Arial 16pt bold header, Arial 14pt body, GRAY_1 text
    content: one parent bullet + two dash sub-bullets + one parent data-source bullet
    copy_when: a deck opener needs one compact narrative context block

  objectives_table:
    geometry: 5.700in wide x 4.522in high, one-column native table
    type: Arial 16pt bold header, Arial 14pt body, black text
    content: ten objective bullets; final three carry italic ongoing-effort prefixes
    copy_when: the right block must carry a full workplan / scope inventory

  preliminary_banner:
    geometry: 5.700in wide x 0.528in high
    type: Arial 12pt bold italic, centered, PRELIM fill
    content: one sentence; use as a cross-document caveat, not a paragraph box

SOURCE NOTE
  Teaching rewrite of the source-faithful `overview.py` module. This slide has no
  chart; the key conversion is table structure. The original already used native
  `table()` objects, but the teaching version promotes the two table bodies into
  semantic `BulletLine` / `OverviewTable` records and removes the unused `_src`
  sidecar path. The source's house `slideLayout3` is intentionally preserved.

FIDELITY NOTE
  This is a practical teaching rewrite, not a byte-identical raw converter port.
  It preserves the visible layout, table geometry, row rules, bullet hierarchy,
  italic ongoing-effort prefixes, bottom preliminary banner, and the Layout3 title
  placeholder contract. The title placeholder remains a minimal layout-inherited
  OOXML string because Layout3 owns its geometry.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from dataclasses import dataclass

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    table,
    trow,
    tcell,
    tcell_rich,
    tpara,
    trun,
)
from deck_core.style import IN, PT, BLACK, DK, PRELIM, GRAY_1, FONT

LAYOUT = "slideLayout3"
CHARTS: list = []

# Layout3 title placeholders inherit their geometry from the layout. The source
# converter therefore kept this as a raw placeholder shape with no explicit xfrm.
# Keeping it here is intentional: the teaching point is that the layout, not this
# module, owns title placement on the 50% Block + Title slide.
LAYOUT3_TITLE_PLACEHOLDER_XML = (
    '<p:sp><p:nvSpPr><p:cNvPr id="2000" name="Title 4" />'
    '<p:cNvSpPr><a:spLocks noGrp="1" /></p:cNvSpPr>'
    '<p:nvPr><p:ph type="title" /></p:nvPr></p:nvSpPr><p:spPr />'
    '<p:txBody><a:bodyPr vert="horz" /><a:lstStyle />'
    '<a:p><a:r><a:rPr lang="en-US" /><a:t>Overview</a:t></a:r></a:p>'
    '</p:txBody></p:sp>'
)

PRELIM_BORDER = "121415"
DEFAULT_TABLE_ROW_H = 0.406


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: small programmatic index for retrieval / agent search.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "deck_orientation / executive_context",
    "use_when": (
        "Use for a table-first overview slide with a left Context block, a right "
        "Objectives block, and a bottom caveat banner."
    ),
    "teaches": [
        "slideLayout3 preservation",
        "layout-inherited title placeholder",
        "semantic native table bodies",
        "bullet hierarchy in tpara records",
        "italic inline runs in table cells",
        "bottom preliminary banner",
    ],
    "source_module": "overview.py",
    "rebuild_strategy": "promote native table body content into semantic records",
}

TEXT_FIT = {
    "context_table": {
        "box_in": (5.700, 3.089),
        "font_pt": "16 header / 14 body",
        "content": "one parent bullet + two dash sub-bullets + one parent bullet",
        "note": "GRAY_1 text on no-fill table; keep it short enough for a left opener block.",
    },
    "objectives_table": {
        "box_in": (5.700, 4.522),
        "font_pt": "16 header / 14 body",
        "content": "ten objective bullets; final three use italic ongoing-effort prefixes",
        "note": "Do not convert this to prose; the scan pattern depends on discrete bullets.",
    },
    "preliminary_banner": {
        "box_in": (5.700, 0.528),
        "font_pt": 12,
        "content": "single centered bold-italic caveat sentence",
    },
}

COPY_RULES = (
    "Use the left block for why the deck exists; use the right block for what the deck delivers.",
    "Keep the final ongoing-effort items as italic prefixes, not separate status badges.",
    "Use Layout3 for this opener; do not silently move it to slideLayout4 chrome.",
)


# ════════════════════════════════════════════════════════════════════════════
# Small semantic geometry/content records.
# ════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Box:
    """Geometry in inches; converted to EMU at primitive boundaries."""

    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class TextRun:
    text: str
    color: str = BLACK
    size_pt: float = 14
    bold: bool = False
    italic: bool = False
    underline: bool = False

    def rich(self) -> str:
        return trun(
            self.text,
            size=PT(self.size_pt),
            bold=self.bold or None,
            italic=self.italic or None,
            underline=self.underline or None,
            color=self.color,
            font=FONT,
        )


@dataclass(frozen=True)
class BulletLine:
    """One table paragraph and its bullet/margin mechanics."""

    runs: tuple[TextRun, ...]
    bullet: bool = True
    bullet_char: str | None = None
    mar_l: int = 285_750
    indent: int = -285_750

    def paragraph(self) -> str:
        kwargs = {
            "bullet": self.bullet,
            "mar_l": self.mar_l,
            "indent": self.indent,
        }
        if self.bullet_char is not None:
            kwargs["bullet_char"] = self.bullet_char
        return tpara([r.rich() for r in self.runs], **kwargs)


@dataclass(frozen=True)
class OverviewTable:
    name: str
    box: Box
    header: str
    header_color: str
    rule_color: str
    lines: tuple[BulletLine, ...]


class ShapeIds:
    """Tiny deterministic id allocator for body shapes."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Native-table content: table data first, mechanics at render time.
# ════════════════════════════════════════════════════════════════════════════
CONTEXT_TABLE = OverviewTable(
    name="ContextTable",
    box=Box(0.498, 1.653, 5.700, 3.089),
    header="Context",
    header_color=GRAY_1,
    rule_color=GRAY_1,
    lines=(
        BulletLine((TextRun("These materials provide foundational analysis to inform two key decisions:", color=GRAY_1),)),
        BulletLine(
            (TextRun("Determine where Saronic should play in the maritime value chain", color=GRAY_1),),
            bullet_char="-",
            mar_l=461_963,
            indent=-174_625,
        ),
        BulletLine(
            (TextRun("Understand how Saronic will win", color=GRAY_1),),
            bullet_char="-",
            mar_l=461_963,
            indent=-174_625,
        ),
        BulletLine(
            (
                TextRun(
                    "Analysis leverages data providers (S&P, Clarksons), US Government data and publications "
                    "(EIA, FRED, GAO, MARAD, USACE), market participants (Saronic experts), public filings, "
                    "published rate / tariff sheets, and other open-source research",
                    color=GRAY_1,
                ),
            ),
        ),
    ),
)

OBJECTIVES_TABLE = OverviewTable(
    name="ObjectivesTable",
    box=Box(7.009, 1.653, 5.700, 4.522),
    header="Objectives of this document",
    header_color=BLACK,
    rule_color=DK,
    lines=(
        BulletLine((TextRun("Define the commercial strategy effort, including objectives, key questions, focus areas, and timeline"),)),
        BulletLine((TextRun("Introduce and synthesize current economics for relevant archetypes across the maritime value chain"),)),
        BulletLine((TextRun("Assess US built vessel demand under different industrial policy scenarios"),)),
        BulletLine((TextRun("Compare US build cost competitiveness vs. Asian shipyards "),)),
        BulletLine((TextRun("Compare US-flagged and foreign-flagged vessel costs"),)),
        BulletLine((TextRun("Project BuildCo (Port Alpha) and OpCo financials"),)),
        BulletLine((TextRun("Delineate hypotheses for impact of automation on opex/fuel"),)),
        BulletLine((TextRun("(Ongoing effort) ", italic=True), TextRun("Determine attractive carrier entry points"))),
        BulletLine((TextRun("(Ongoing effort)", italic=True), TextRun(" Assess attractiveness of alternative service models unlocked by automation"))),
        BulletLine((TextRun("(Ongoing effort)", italic=True), TextRun(" Project ComboCo financials"))),
    ),
)

PRELIMINARY_BANNER = Box(7.009, 6.425, 5.700, 0.528)
PRELIMINARY_BANNER_TEXT = (
    "Answers shown are preliminary; fidelity and insights will increase with "
    "further analysis, additional data, and expert input"
)


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: same teaching pattern as the factory-chart modules.
# Content records stay above; cell mechanics stay here.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def border_dict(**edges):
    """Only draw the sides passed as L/R/T/B; omitted sides render no-fill."""

    return {k: v for k, v in edges.items() if v is not None} or None


def cell(
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
    """tcell wrapper: scalar content first, table mechanics second."""

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
    """tcell_rich wrapper: paragraph content first, cell mechanics second."""

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
# Text helpers and paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def _body_run(text: str, *, size_pt: float = 12, color: str = BLACK, bold: bool = False, italic: bool = False) -> str:
    return run(text, size=PT(size_pt), bold=bold or None, italic=italic or None, color=color, font=FONT)


def _overview_table(sp_id: int, spec: OverviewTable) -> str:
    """Render one of the two native one-column overview tables."""

    return table(
        sp_id,
        spec.name,
        *spec.box.emu(),
        col_widths=[IN(spec.box.w)],
        rows=[
            trow(
                [
                    cell(
                        spec.header,
                        size=PT(16),
                        bold=True,
                        color=spec.header_color,
                        B=edge(spec.rule_color),
                    )
                ],
                h=IN(DEFAULT_TABLE_ROW_H),
            ),
            trow(
                [
                    rich_cell(
                        [line.paragraph() for line in spec.lines],
                        T=edge(spec.rule_color),
                    )
                ],
                h=IN(DEFAULT_TABLE_ROW_H),
            ),
        ],
    )


def paint_title(out: list[str]) -> None:
    out.append(LAYOUT3_TITLE_PLACEHOLDER_XML)


def paint_overview_tables(out: list[str], ids: ShapeIds) -> None:
    out.append(_overview_table(ids.next(), CONTEXT_TABLE))
    out.append(_overview_table(ids.next(), OBJECTIVES_TABLE))


def paint_preliminary_banner(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            "PreliminaryBanner",
            *PRELIMINARY_BANNER.emu(),
            [
                paragraph(
                    [_body_run(PRELIMINARY_BANNER_TEXT, size_pt=12, bold=True, italic=True)],
                    align="ctr",
                    line_spacing=100_000,
                )
            ],
            fill=PRELIM,
            line_color=PRELIM_BORDER,
            line_width=19_050,
            anchor="ctr",
        )
    )


def _body() -> str:
    out: list[str] = []
    ids = ShapeIds()
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    paint_title(out)
    paint_overview_tables(out, ids)
    paint_preliminary_banner(out, ids)
    return "".join(out)


# ════════════════════════════════════════════════════════════════════════════
# Import-time validation: fail fast if the teaching contract drifts.
# ════════════════════════════════════════════════════════════════════════════
def _validate_teaching_module() -> None:
    if LAYOUT != "slideLayout3":
        raise ValueError("overview teaching slide must remain on slideLayout3")
    if CHARTS != []:
        raise ValueError("overview is table-only and must not declare chart objects")
    if CONTEXT_TABLE.box.w != OBJECTIVES_TABLE.box.w:
        raise ValueError("context/objective columns should retain the same 5.7in width")
    if len(CONTEXT_TABLE.lines) != 4:
        raise ValueError("context table should have one parent bullet, two sub-bullets, and one data-source bullet")
    if len(OBJECTIVES_TABLE.lines) != 10:
        raise ValueError("objectives table should retain ten bullets")
    if not all(line.runs[0].italic for line in OBJECTIVES_TABLE.lines[-3:]):
        raise ValueError("final three objectives must retain italic ongoing-effort prefixes")
    if not LAYOUT3_TITLE_PLACEHOLDER_XML.startswith("<p:sp>"):
        raise ValueError("Layout3 title placeholder should remain a layout-inherited p:sp")


_validate_teaching_module()


def render() -> str:
    return slide(_body())
