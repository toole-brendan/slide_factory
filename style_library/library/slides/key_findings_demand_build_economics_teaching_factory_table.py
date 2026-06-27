"""Teaching exemplar: key findings as a one-cell executive-summary table.

ROLE
  executive_summary / text_heavy_findings

USE WHEN
  A slide needs to carry a dense, multi-level findings narrative where the
  strongest design constraint is text hierarchy, not chart/table data comparison.
  This pattern uses a single native table cell as the text frame so PowerPoint
  keeps a stable rich-text layout while authors can express every paragraph and
  run declaratively.

TEACHES
  - a one-cell native table used as a full-slide narrative container
  - rich table paragraphs with auto-number, bullet, and dash sub-bullet levels
  - inline run-level emphasis for question prompts, caveats, and quantified claims
  - local table styling helpers instead of centralized table_kit imports
  - paint-order discipline for chrome -> table -> off-house footnote
  - empirical text-fit precedent for dense Arial 12pt executive-summary bullets

TEXT-FIT PRECEDENT
  findings_table:
    geometry: 12.300in wide x 5.900in high
    type: Arial 12pt, black, single-spaced table paragraphs
    content: 4 framing questions + 9 subordinate bullets / caveats
    copy_when: the slide is meant to be read as an executive-summary memo, and
               the table is a stable rich-text frame rather than a data grid

SOURCE NOTE
  Teaching rewrite of the source-faithful `key_findings_demand_build_economics.py`
  module. There are no charts on this slide; CHARTS is intentionally empty. The
  core artifact is the one-cell native table, with local table helpers that make
  table mechanics explicit without importing deck_core.table_kit.

FIDELITY NOTE
  This is a readability refactor of the source-converted slide module. Coordinates,
  paint order, text, paragraph hierarchy, table insets, no-rule borders, and the
  off-house footnote geometry are preserved from the polished source module.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    table,
    trow,
    tcell_rich,
    tpara,
    trun,
    breadcrumb,
    title_placeholder,
    prelim_chip,
)
from deck_core.style import IN, PT, BLACK, DK, FONT

LAYOUT = "slideLayout4"
CHARTS: list = []

TEAL = "1D4D68"
RED = "FF0000"
NO_EDGE = "none"

_SECTION = "Commercial Strategy"
_TOPIC = "Research Overview"
_TITLE = "Key Findings (1/3)"
_TAKEAWAY = "Demand, build cost, and vessel economics."


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: useful for agents choosing an exemplar.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "executive_summary",
    "use_when": (
        "Use for a dense findings page where one native table cell acts as the "
        "narrative frame and the important authoring problem is rich bullet "
        "hierarchy, not data-grid construction."
    ),
    "teaches": [
        "one-cell native table as a rich-text frame",
        "rich table paragraphs via tpara/trun",
        "auto-numbered framing questions",
        "nested bullets and dash note bullets",
        "inline table styling helpers",
        "off-house footnote box preservation",
    ],
}

TEXT_FIT = {
    "findings_table": {
        "box_in": (12.300, 5.900),
        "font_pt": 12,
        "content": "4 framing questions + 9 subordinate bullets / caveats",
        "note": (
            "This is an intentionally dense executive-summary memo. Keep the "
            "question prompts short and put quantified proof points in the "
            "sub-bullets instead of adding extra top-level bullets."
        ),
    },
    "footnote": {
        "box_in": (4.679, 0.300),
        "font_pt": 8,
        "content": "single note line",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Semantic records: geometry in inches, text hierarchy as data.
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
class RunSpec:
    text: str
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color: str = BLACK
    size_pt: float = 12


@dataclass(frozen=True)
class ParagraphStyle:
    """The paragraph mechanics that make the hierarchy visible in PowerPoint."""

    name: str
    bullet_char: str | None
    level: int
    mar_l: int
    indent: int
    space_after: int = 600
    space_before: int = 0


@dataclass(frozen=True)
class FindingParagraph:
    intent: str
    style: ParagraphStyle
    runs: tuple[RunSpec, ...]


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
FINDINGS_TABLE = TextZone(
    name="FindingsNarrativeTable",
    box=Box(0.495, 1.066, 12.300, 5.900),
    font_pt=12,
    fit_note="Single-column native table; one rich cell holds all narrative bullets.",
)
FOOTNOTE = TextZone(
    name="Footnote",
    box=Box(0.495, 7.002, 4.679, 0.300),
    font_pt=8,
    fit_note="Off-house note kept at source position below the main slide canvas.",
)

# Cell/table mechanics from the source native table. These live here, rather
# than in table_kit.py, so the module is self-contained as a teaching specimen.
FINDINGS_CELL_INSET_X = 41_564
FINDINGS_TABLE_ROW_H = IN(0)


# ════════════════════════════════════════════════════════════════════════════
# Paragraph hierarchy.
# ════════════════════════════════════════════════════════════════════════════
TOP_QUESTION = ParagraphStyle(
    name="top_question_auto_number",
    bullet_char="auto",
    level=0,
    mar_l=227_013,
    indent=-227_013,
)
SCENARIO_BULLET = ParagraphStyle(
    name="scenario_capacity_bullet",
    bullet_char=None,
    level=1,
    mar_l=342_900,
    indent=-117_475,
)
SCENARIO_NOTE = ParagraphStyle(
    name="scenario_note_dash_bullet",
    bullet_char="−",
    level=2,
    mar_l=457_200,
    indent=-114_300,
)
DETAIL_BULLET = ParagraphStyle(
    name="detail_bullet",
    bullet_char=None,
    level=1,
    mar_l=342_900,
    indent=-114_300,
)
AUTONOMY_BULLET = ParagraphStyle(
    name="autonomy_detail_bullet",
    bullet_char=None,
    level=1,
    mar_l=339_725,
    indent=-112_713,
)


def T(
    text: str,
    *,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    color: str = BLACK,
    size_pt: float = 12,
) -> RunSpec:
    """Compact RunSpec constructor; data below reads like marked-up copy."""

    return RunSpec(text, bold=bold, italic=italic, underline=underline, color=color, size_pt=size_pt)


FINDINGS_PARAGRAPHS: tuple[FindingParagraph, ...] = (
    FindingParagraph(
        "addressable_demand_question",
        TOP_QUESTION,
        (
            T("What is the addressable demand for US-built ships?", bold=True, italic=True, underline=True, color=TEAL),
            T(" ", italic=True),
            T(
                "We evaluated four scenarios for oceangoing commercial ships assuming Port Alpha buildout to Phase 5: "
                "(1) Jones Act status quo, (2) SHIPS Act as written, (3) SHIPS Act “Plus” with key bill revisions "
                "and expansion of existing programs, and (4) SHIPS Act “Plus” with Heritage Foundation target fleet; "
            ),
            T("these scenarios suggest path to Port Alpha Phase", bold=True),
            T(" ", bold=True, color=RED),
            T("2+", bold=True, color=DK),
            T(" ", bold=True, color=RED),
            T("requires additional demand signals", bold=True),
        ),
    ),
    FindingParagraph(
        "orderbook_question",
        TOP_QUESTION,
        (
            T("What does demand imply for Port Alpha’s orderbook?", bold=True, italic=True, underline=True, color=TEAL),
            T(" ", italic=True),
            T("’28-’38 demand as percentage of Port Alpha Phase 2 capacity "),
            T("(25 deliveries / year; containerships and tankers) ", italic=True),
            T("by scenario:"),
        ),
    ),
    FindingParagraph(
        "scenario_1_status_quo",
        SCENARIO_BULLET,
        (
            T("(1) Status Quo accounts for an avg. of ~5% of capacity; ", bold=True),
            T("outlook contingent upon Jones Act fleet recapitalization"),
        ),
    ),
    FindingParagraph(
        "scenario_2_ships_act_as_written",
        SCENARIO_BULLET,
        (
            T("(2) SHIPS Act as written accounts for ~45%;", bold=True),
            T(" ", bold=True),
            T("requires passage of both SHIPS Act and Building Ships in America Act"),
        ),
    ),
    FindingParagraph(
        "scenario_3_ships_act_plus",
        SCENARIO_BULLET,
        (
            T("(3) SHIPS Act “Plus”", bold=True),
            T("1", bold=True),
            T(" accounts for ~95%, ", bold=True),
            T("with demand"),
            T(" ", bold=True),
            T("declining by the mid-’30s and remaining low through ‘50; requires "),
            T("USG to subsidize full opex and D&A differential ", bold=True),
            T("vs. foreign ships, supported by "),
            T("universal cargo fees ", bold=True),
            T("($0.01+ per kg imported by foreign-built ships) and other revisions to pending legislation "),
        ),
    ),
    FindingParagraph(
        "scenario_3_legislative_note",
        SCENARIO_NOTE,
        (
            T("NOTE:", bold=True, italic=True, underline=True),
            T(" Headwinds are currently impacting the legislative path for the SHIPS Act", bold=True, italic=True),
        ),
    ),
    FindingParagraph(
        "scenario_4_heritage",
        SCENARIO_BULLET,
        (
            T("(4) SHIPS Act “Plus” with Heritage accounts for ~230%", bold=True),
            T(", with demand declining by the early ‘40s and remaining low through 50; "),
            T("requires "),
            T("universal cargo fees of $0.07+ ", bold=True),
            T("per kg by 2050 and Maritime Security Trust Fund balance cap increase "),
        ),
    ),
    FindingParagraph(
        "scenario_4_funding_note",
        SCENARIO_NOTE,
        (
            T("NOTE:", bold=True, italic=True, underline=True),
            T(
                " Pending legislation supports <20% of Heritage Foundation’s target fleet; funding required likely challenges demand materialization",
                bold=True,
                italic=True,
            ),
        ),
    ),
    FindingParagraph(
        "newbuild_price_question",
        TOP_QUESTION,
        (
            T(
                "What are the impacts on US newbuild prices vs. those of major international shipbuilders?",
                bold=True,
                italic=True,
                underline=True,
                color=TEAL,
            ),
            T(" "),
            T("With yard automation, SHIPS Act demand, and vessel investment tax credits, expected "),
            T("Port Alpha newbuild prices remain ~1.4-2.2x above ", bold=True),
            T("those of Asian shipyards, down from ~4-6x today"),
        ),
    ),
    FindingParagraph(
        "capital_subsidy_detail",
        DETAIL_BULLET,
        (
            T("Government capital subsidies required ", bold=True),
            T("to achieve prices below Asian yards in the "),
            T("absence of vessel ITCs ", bold=True),
            T("(US-flag & foreign trade required for ITC eligibility)"),
        ),
    ),
    FindingParagraph(
        "price_reduction_drivers",
        DETAIL_BULLET,
        (
            T("Labor hour reduction and volume discounts primarily drive build price reductions", bold=True),
            T(
                "; shipyard ITCs may reduce prices by ~0-1% given capex scale and D&A mechanics; however, "
                "Shipyard ITCs meaningfully de-risk yard capacity expansion "
            ),
            T("(discussed on subsequent page)", italic=True),
        ),
    ),
    FindingParagraph(
        "vessel_economics_question",
        TOP_QUESTION,
        (
            T(
                "How do US-flagged vessel economics compare to foreign-flagged today? How do industrial policy and automation change the gap?",
                bold=True,
                italic=True,
                underline=True,
                color=TEAL,
            ),
            T(" ", italic=True),
            T("(2) SHIPS "),
            T("Act as written unlikely to make US-built, US-flagged vessels attractive enough to realize full potential of SCF given estimated "),
            T(
                "US opex and D&A gap vs. foreign of ~$10M after subsidies and ITCs; (3) SHIPS Act “Plus” may result in US-built and flagged vessels being cheaper to own and operate"
            ),
        ),
    ),
    FindingParagraph(
        "automation_opex_detail",
        AUTONOMY_BULLET,
        (
            T("With automation, "),
            T("US-flagged opex likely "),
            T("remains more expensive than foreign-flagged ", bold=True),
            T("given new autonomy-related expenses offsetting reduction in other opex categories"),
            T("; ", bold=True),
            T("Saronic may see lower opex than other Jones Act players when operating autonomous vessels, with cost advantage driven by vertical integration as ComboCo "),
        ),
    ),
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


def findings_cell(paras):
    """The slide's single table cell: no fill, no borders, tight source insets."""

    return rich_cell(
        paras,
        l_ins=FINDINGS_CELL_INSET_X,
        r_ins=FINDINGS_CELL_INSET_X,
        L=NO_EDGE,
        R=NO_EDGE,
        T=NO_EDGE,
        B=NO_EDGE,
    )


# ════════════════════════════════════════════════════════════════════════════
# Text helpers: keep paint functions at slide-intent level.
# ════════════════════════════════════════════════════════════════════════════
def _table_run(spec: RunSpec) -> dict:
    return trun(
        spec.text,
        size=PT(spec.size_pt),
        bold=spec.bold or None,
        italic=spec.italic or None,
        underline=spec.underline or None,
        color=spec.color,
        font=FONT,
    )


def _finding_paragraph(spec: FindingParagraph) -> dict:
    style = spec.style
    return tpara(
        [_table_run(run_spec) for run_spec in spec.runs],
        bullet=True,
        bullet_char=style.bullet_char,
        level=style.level,
        mar_l=style.mar_l,
        indent=style.indent,
        space_before=style.space_before,
        space_after=style.space_after,
    )


def _finding_paragraphs() -> list[dict]:
    return [_finding_paragraph(spec) for spec in FINDINGS_PARAGRAPHS]


def _body_run(text: str, *, size_pt: float, color: str = BLACK) -> str:
    return run(text, size=PT(size_pt), color=color, font=FONT)


# ════════════════════════════════════════════════════════════════════════════
# Paint sections. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def paint_chrome(out: list[str]) -> None:
    out.append(breadcrumb(_SECTION, _TOPIC))
    out.append(title_placeholder(_TITLE, _TAKEAWAY))
    out.append(prelim_chip())


def paint_findings_table(out: list[str], ids: ShapeIds) -> None:
    # One-cell native table used as a stable rich-text frame. col_widths is the
    # table geometry; findings_cell() owns the text insets and explicit no-rules.
    out.append(
        table(
            ids.next(),
            "Table 13",
            *FINDINGS_TABLE.box.emu(),
            col_widths=[IN(FINDINGS_TABLE.box.w)],
            rows=[
                trow(
                    [findings_cell(_finding_paragraphs())],
                    h=FINDINGS_TABLE_ROW_H,
                )
            ],
        )
    )


def paint_footnote(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            "Rectangle 4",
            *FOOTNOTE.box.emu(),
            [
                paragraph(
                    [
                        _body_run(
                            "Note: (1) Refer to pg. 12 for full description of modifications to SHIPS Act and other relevant USG programs",
                            size_pt=8,
                        )
                    ],
                    line_spacing=100_000,
                )
            ],
            fill=None,
            line_color="none",
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
    paint_chrome(out)
    paint_findings_table(out, ids)
    paint_footnote(out, ids)

    return "".join(out)


def render() -> str:
    return slide(_body())
