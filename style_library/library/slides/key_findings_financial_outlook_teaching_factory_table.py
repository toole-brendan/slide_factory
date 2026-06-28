"""Teaching exemplar: key-findings financial-outlook slide.

ROLE
  executive_summary / financial_outlook_findings

USE WHEN
  A slide needs to carry dense executive-summary prose as one full-width native
  table cell, preserve a multi-level bullet hierarchy, and layer a small
  contingency callout over the lower-right of the narrative.

TEACHES
  - rich single-cell native table as a prose container
  - deep bullet hierarchy inside tcell_rich()/tpara()/trun()
  - local run specs so dense prose is readable without repeating PT12/Arial
  - inline native-table styling without importing deck_core.table_kit
  - no-border table mechanics made explicit at the slide level
  - dashed text-box callout layered above table content
  - paint-order preservation for chrome, table, and callout

TEXT-FIT PRECEDENT
  findings_narrative_table:
    geometry: 12.300in wide x 5.950in high
    type: Arial 12pt, black, 100% line spacing inside a native table cell
    content: one numbered framing question + 3 segment headings + 12 nested
             dash bullets
    copy_when: a text-heavy key-findings page needs the table engine's compact
               paragraph layout and stable in-cell bullet indentation
  contingencies_callout:
    geometry: 4.685in wide x 0.913in high
    type: Arial 12pt, pale-blue fill, DK dashed outline, shadow effect
    content: centred heading + two bullets
    copy_when: a slide needs a visually explicit dependency note without adding
               another table column

SOURCE NOTE
  Teaching rewrite of the source-faithful `key_findings_financial_outlook.py`
  module. The slide remains a native-table build plus one dashed callout; charts,
  images, and centralized table-kit imports are intentionally absent. The table
  styling that matters here is the explicit no-border single rich cell.

FIDELITY NOTE
  This is an authoring/readability refactor, not a visual redesign. Geometry,
  row height, cell insets, bullet margins, run styling, callout styling, chrome,
  and paint order are preserved from the hand-polished source module. A few
  seemingly odd run splits mirror the converted source so the emitted OOXML stays
  stable.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, paragraph, run, table, tcell_rich, text_box, tpara, trow,
    trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
DK = "162029"
FONT = "Arial"

LAYOUT = "slideLayout4"
CHARTS: list = []


# ════════════════════════════════════════════════════════════════════════════
# Teaching metadata: slide-level guidance AI authors can inspect.
# ════════════════════════════════════════════════════════════════════════════
TEACHING_METADATA = {
    "role": "executive_summary_financial_outlook",
    "use_when": (
        "Use for a dense key-findings page whose body is best authored as one "
        "rich native-table cell, with a compact dependency callout layered on top."
    ),
    "teaches": [
        "single-cell rich native table",
        "multi-level bullet hierarchy in tpara()",
        "local run specs for PT12 Arial prose",
        "explicit no-border table-cell styling",
        "text-fit precedent for dense prose",
        "dashed contingency callout",
        "paint-order preservation",
    ],
}

TEXT_FIT = {
    "findings_narrative_table": {
        "box_in": (12.300, 5.950),
        "font_pt": 12,
        "content": "16 bulleted paragraphs across intro, BuildCo, OpCo, and ComboCo sections",
        "note": (
            "This is near the upper practical density for 12pt prose. Keep the "
            "question/answer wording concise; do not add another major section "
            "without reducing copy elsewhere."
        ),
    },
    "contingencies_callout": {
        "box_in": (4.685, 0.913),
        "font_pt": 12,
        "content": "heading + two bullets",
        "note": "Works as a short overlay because it uses centred vertical anchoring and tight 100% line spacing.",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Small semantic records: geometry, rich prose, and table/callout styles.
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
class FindingsRun:
    """One rich-text run inside the findings table."""

    text: str
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color: str = BLACK
    size_pt: float = 12


@dataclass(frozen=True)
class FindingsParagraph:
    """One table paragraph; bullet geometry is part of the content grammar."""

    runs: tuple[FindingsRun, ...]
    bullet: bool = True
    bullet_char: str | None = None
    level: int = 0
    mar_l: int | None = None
    indent: int | None = None
    space_before: int | None = 300
    space_after: int | None = 300


@dataclass(frozen=True)
class FindingsBlock:
    """A semantic section of the executive-summary prose."""

    name: str
    heading: FindingsParagraph
    bullets: tuple[FindingsParagraph, ...]


@dataclass(frozen=True)
class FindingsTableStyle:
    """The single-cell table style, kept inline as teaching material."""

    fill: str | None = None
    anchor: str = "ctr"
    l_ins: int = 41_564
    r_ins: int = 41_564
    t_ins: int = 45_720
    b_ins: int = 45_720
    border: str = "none"


@dataclass(frozen=True)
class ContingenciesCallout:
    name: str
    box: Box
    heading: str
    bullets: tuple[str, ...]
    fill: str = "CEDDEC"
    line_color: str = DK
    dashed_line: bool = True
    effects: str | None = None


class ShapeIds:
    """Tiny id allocator; chrome uses fixed ids inside deck_core primitives."""

    def __init__(self, start: int = 100) -> None:
        self._next = start

    def next(self) -> int:
        value = self._next
        self._next += 1
        return value


# ════════════════════════════════════════════════════════════════════════════
# Low-level table kit: intentionally inline, not imported from table_kit.py.
# ════════════════════════════════════════════════════════════════════════════
def edge(color: str, w: int = 12_700) -> dict[str, int | str]:
    """One native-table border edge; 12_700 EMU = 1pt."""

    return {"color": color, "width": w}


def border_dict(**edges):
    """Only draw sides passed as L/R/T/B; explicit "none" means no-fill."""

    return {k: v for k, v in edges.items() if v is not None} or None


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
    """Multi-paragraph native-table cell: content first, mechanics second."""

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
# Text helpers: local defaults keep the prose data readable.
# ════════════════════════════════════════════════════════════════════════════
def frun(
    text: str,
    *,
    b: bool = False,
    i: bool = False,
    u: bool = False,
    color: str = BLACK,
    size_pt: float = 12,
) -> FindingsRun:
    """One findings-table run; defaults match the source slide's PT12 Arial prose."""

    return FindingsRun(text, bold=b, italic=i, underline=u, color=color, size_pt=size_pt)


def top_para(*runs: FindingsRun) -> FindingsParagraph:
    """Numbered top-level framing question."""

    return FindingsParagraph(tuple(runs), bullet_char="auto", mar_l=228_600, indent=-228_600)


def section_para(*runs: FindingsRun) -> FindingsParagraph:
    """Level-1 segment heading: BuildCo, OpCo, or ComboCo."""

    return FindingsParagraph(tuple(runs), level=1, mar_l=342_900, indent=-114_300)


def sub_para(*runs: FindingsRun) -> FindingsParagraph:
    """Level-2 dash bullet under a segment heading."""

    return FindingsParagraph(tuple(runs), bullet_char="−", level=2, mar_l=457_200, indent=-114_300)


def _table_run_xml(run_spec: FindingsRun) -> dict:
    return trun(
        run_spec.text,
        size=PT(run_spec.size_pt),
        bold=run_spec.bold or None,
        italic=run_spec.italic or None,
        underline=run_spec.underline or None,
        color=run_spec.color,
        font=FONT,
    )


def _table_para_xml(spec: FindingsParagraph) -> dict:
    return tpara(
        [_table_run_xml(run_spec) for run_spec in spec.runs],
        bullet=spec.bullet,
        bullet_char=spec.bullet_char,
        level=spec.level,
        mar_l=spec.mar_l,
        indent=spec.indent,
        space_before=spec.space_before,
        space_after=spec.space_after,
    )


def _box_run(text: str, *, size_pt: float = 12, bold: bool = False, color: str = BLACK) -> str:
    return run(text, size=PT(size_pt), bold=bold or None, color=color, font=FONT)


# ════════════════════════════════════════════════════════════════════════════
# Layout zones and local styles.
# ════════════════════════════════════════════════════════════════════════════
FINDINGS_TABLE = TextZone(
    name="FinancialOutlookTable",
    box=Box(0.495, 1.066, 12.300, 5.950),
    font_pt=12,
    fit_note="Full-slide prose container; one native table cell with compact bullet hierarchy.",
)

FINDINGS_TABLE_STYLE = FindingsTableStyle()

CALLOUT_SHADOW = (
    '<a:effectLst><a:outerShdw blurRad="50800" dist="38100" dir="2700000" '
    'algn="tl" rotWithShape="0"><a:prstClr val="black"><a:alpha val="40000" />'
    '</a:prstClr></a:outerShdw></a:effectLst>'
)

CONTINGENCIES = ContingenciesCallout(
    name="ContingenciesCallout",
    box=Box(7.936, 4.204, 4.685, 0.913),
    heading="Results detailed contingent on:",
    bullets=(
        "Implementation of proposed legislation, subsidies, tax credits & additional future policy action",
        "High degree of automation and efficiency at Port Alpha",
    ),
    effects=CALLOUT_SHADOW,
)


# ════════════════════════════════════════════════════════════════════════════
# Findings prose: one top framing bullet plus three semantic segment blocks.
# ════════════════════════════════════════════════════════════════════════════
INTRO_PARAGRAPH = top_para(
    frun("What do these findings imply for ComboCo financials?", b=True, i=True, u=True, color="1D4D68"),
    frun(" ", i=True),
    frun("Projections were created from 2026-2038 ", b=True),
    frun("after alignment with "),
    frun("Finance and Port Alpha teams on starting assumptions (i.e., initial sale price, labor hours, CAPEX, vessel profiles)"),
)

FINDINGS_BLOCKS: tuple[FindingsBlock, ...] = (
    FindingsBlock(
        name="BuildCo",
        heading=section_para(
            frun("BuildCo (i.e., Saronic):", b=True, u=True),
            frun(" ", b=True),
            frun("Port Alpha build-out modeled to Phase 2 for $3.5B total CAPEX"),
        ),
        bullets=(
            sub_para(
                frun("Two ships were modelled ", b=True),
                frun("– a Panamax containership and an Aframax / Suezmax Tanker; a"),
                frun("ssumes"),
                frun(" 182 containerships and 39 tankers ", b=True),
                frun("are delivered during this period; n"),
                frun("umber of deliveries were based off ("),
                frun("i"),
                frun(") SHIPS Act “Plus” and (ii) Port Alpha capacity (25 deliveries / year)"),
            ),
            sub_para(
                frun("Gross Margins set at 44% in 2028, declining to ~40% by 2038", b=True),
                frun(" given increased domestic competition; overall domestic prices supported by USG subsidies for vessel owners"),
            ),
            sub_para(frun("EBIT margins vary, largely staying within 5-10% range in 2032+", b=True)),
            sub_para(frun("Shipyard ITCs soften impact of capex on FCF in early years, while also reducing outside capital needs")),
        ),
    ),
    FindingsBlock(
        name="OpCo",
        heading=section_para(
            frun("OpCo (Saronic as owner/operator):", b=True, u=True),
            frun(" ", b=True),
            frun("P"),
            frun("urchases "),
            frun("25 total container ships for $4.2B ", b=True),
            frun("in ‘33 and ‘34 that enter service the following year in the Strategic Commercial Fleet, operating on US Atlantic / Gulf Coast <> Europe / S. America routes "),
            frun("(to consider Jones Act Marine Highway / OCONUS in future efforts)", i=True),
        ),
        bullets=(
            sub_para(
                frun("Service starts in 2034, which softens cash outlay frequency; ", b=True),
                frun("earlier service start would require more equity financing and prevents potentially antagonistic messaging of immediate competition with BuildCo customers "),
            ),
            sub_para(frun("BuildCo sells vessels to OpCo under favorable pricing (10% gross margin)", b=True)),
            sub_para(frun("EBIT margins (inclusive of operating and capital subsidies) of ~25%")),
        ),
    ),
    FindingsBlock(
        name="ComboCo",
        heading=section_para(frun("ComboCo (BuildCo + OpCo)", b=True, u=True)),
        bullets=(
            sub_para(
                frun("Financing: ", b=True),
                frun("$2.8B OSC Loan / $500M Revolver / $2.25B in Equity + $500M in Cash; assumes only BuildCo qualifies for shipyard ITCs "),
            ),
            sub_para(
                frun("EBIT Margin reach 12-14% ", b=True),
                frun("in the 2030s, in between traditional shipbuilders (~4-6%) and ship owners (15-20%)"),
            ),
            sub_para(
                frun("Consistent Cash Flow positive in 2034 onwards ", b=True),
                frun("after conclusion of BuildCo capex and OpCo vessel procurement"),
            ),
            sub_para(
                frun("FCF NPV of (~$2.5B); primarily driven by frontloaded CAPEX timing, intersegment transfers, and absence of vessel ITCs ", b=True),
                frun("(given current bill language)", i=True),
            ),
            sub_para(
                frun("Preliminary analysis suggests key determinants of Saronic’s commercial market success include pursuing new business models enabled by autonomy (i.e., marine highway), competing in Jones Act, developing incremental revenue streams (e.g., selling marine / cargo data), and ensuring ComboCo vessel ITC eligibility"),
            ),
        ),
    ),
)


def _findings_paragraph_specs() -> list[FindingsParagraph]:
    paragraphs = [INTRO_PARAGRAPH]
    for block in FINDINGS_BLOCKS:
        paragraphs.append(block.heading)
        paragraphs.extend(block.bullets)
    return paragraphs


def _findings_cell_style_edges(style: FindingsTableStyle) -> dict[str, str]:
    # The source table deliberately has no visible rules. Passing explicit no-fill
    # sides makes that design decision visible to authors reading this module.
    return {"L": style.border, "R": style.border, "T": style.border, "B": style.border}


def paint_findings_table(out: list[str], ids: ShapeIds) -> None:
    style = FINDINGS_TABLE_STYLE
    out.append(
        table(
            ids.next(),
            FINDINGS_TABLE.name,
            *FINDINGS_TABLE.box.emu(),
            col_widths=[IN(FINDINGS_TABLE.box.w)],
            rows=[
                trow(
                    [
                        rich_cell(
                            [_table_para_xml(spec) for spec in _findings_paragraph_specs()],
                            fill=style.fill,
                            anchor=style.anchor,
                            l_ins=style.l_ins,
                            r_ins=style.r_ins,
                            t_ins=style.t_ins,
                            b_ins=style.b_ins,
                            **_findings_cell_style_edges(style),
                        )
                    ],
                    h=IN(0),
                )
            ],
        )
    )


def paint_contingencies_callout(out: list[str], ids: ShapeIds) -> None:
    out.append(
        text_box(
            ids.next(),
            CONTINGENCIES.name,
            *CONTINGENCIES.box.emu(),
            [
                paragraph(
                    [_box_run(CONTINGENCIES.heading, bold=True)],
                    align="ctr",
                    line_spacing=100_000,
                ),
                *[
                    paragraph(
                        [_box_run(bullet)],
                        mar_l=285_750,
                        indent=-285_750,
                        line_spacing=100_000,
                        bullet=True,
                    )
                    for bullet in CONTINGENCIES.bullets
                ],
            ],
            fill=CONTINGENCIES.fill,
            line_color=CONTINGENCIES.line_color,
            dashed_line=CONTINGENCIES.dashed_line,
            anchor="ctr",
            effects=CONTINGENCIES.effects,
        )
    )


# ════════════════════════════════════════════════════════════════════════════
# Slide render.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE.
    # Paint order matters in PowerPoint OOXML: later elements sit on top.
    paint_findings_table(out, ids)
    paint_contingencies_callout(out, ids)

    return "".join(out)


CHROME = Chrome(
    section="Commercial Strategy",
    topic="Research Overview",
    title="Key Findings (2/3)",
    takeaway="ComboCo financial outlook.",
)


def render() -> str:
    return body_slide(CHROME, _body())
