"""Teaching exemplar: key-terms glossary slide.

ROLE
  reference_glossary / two_column_definitions

USE WHEN
  A slide needs compact, side-by-side glossary tables with banner headers,
  two-column term/definition structure, inline italic parentheticals, and a
  small analysis-terms section that uses a distinct banner colour.

TEACHES
  - fully inline native-table styling without importing deck_core.table_kit
  - table mechanics separated from glossary content through local helpers
  - two-column glossary construction from semantic entry records
  - table-wide style records for banner fill, banner text colour, rules, and
    definition text colour
  - rich definition cells built from run specs instead of pre-authored OOXML
  - paint-order preservation when chrome interleaves between tables

TEXT-FIT PRECEDENT
  industrial_policy_terms:
    geometry: 6.000in wide x 3.300in high
    type: Arial 12pt, black, native table cell defaults
    content: banner + column header + 9 rows
    copy_when: a top-left glossary has short abbreviations and mostly one-line
               expansions
  market_terms:
    geometry: 6.000in wide x 4.200in high
    type: Arial 12pt, black, 0.214in row minima
    content: banner + column header + 12 rows, including italic parentheticals
    copy_when: a glossary table must fit many short entries in a right-side rail
  analysis_terms:
    geometry: 6.000in wide x 1.800in high
    type: Arial 12pt, black term cells + DK definition cells
    content: banner + column header + 4 rows
    copy_when: a smaller bottom glossary needs a stronger coloured section label

SOURCE NOTE
  Teaching rewrite of the source-faithful `key_terms_glossary.py` module. The
  slide remains a pure native-table build: no charts, no images, no centralized
  table kit import. The table styling that used to be a small local utility is
  expanded into this module as explicit teaching material.

FIDELITY NOTE
  This is an authoring/readability refactor, not a visual redesign. The table
  geometry, row heights, column widths, fills, border rules, text sizes, chrome,
  and paint order are preserved from the hand-polished source module.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, table, tcell, tcell_rich, tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
GRAY_2 = "D9D9D9"
GRAY_3 = "BFBFBF"
FONT = "Arial"

LAYOUT = "slideLayout4"
CHARTS: list = []


TEXT_FIT = {
    "industrial_policy_terms": {
        "box_in": (6.000, 3.300),
        "font_pt": 12,
        "content": "banner + header + 9 one-line rows",
        "note": "The source uses zero row minima here; table height governs the fit.",
    },
    "market_terms": {
        "box_in": (6.000, 4.200),
        "font_pt": 12,
        "content": "banner + header + 12 rows, some rich parentheticals",
        "note": "0.214in row minima keep the dense right-hand table readable.",
    },
    "analysis_terms": {
        "box_in": (6.000, 1.800),
        "font_pt": 12,
        "content": "banner + header + 4 rows with DK definitions",
        "note": "Short labels allow a compact bottom-left table with a blue banner.",
    },
}


# ════════════════════════════════════════════════════════════════════════════
# Small semantic records: geometry, content, and table style.
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
class DefinitionRun:
    """One run inside a rich definition cell."""

    text: str
    bold: bool = False
    italic: bool = False
    color: str | None = None
    size_pt: float = 12


@dataclass(frozen=True)
class RichDefinition:
    """A definition that needs multiple runs, usually for italic parentheticals."""

    runs: tuple[DefinitionRun, ...]
    mar_l: int | None = None
    indent: int | None = None


@dataclass(frozen=True)
class GlossaryEntry:
    """One glossary row: left term/abbreviation plus right definition."""

    term: str
    definition: str | RichDefinition


@dataclass(frozen=True)
class GlossaryTableStyle:
    """Local table style: all styling choices stay visible in this module."""

    banner_fill: str
    banner_text_color: str = BLACK
    term_text_color: str = BLACK
    definition_text_color: str = BLACK
    header_rule_color: str = BLACK
    row_rule_color: str = "808080"
    header_rule_width: int = 12_700
    row_rule_width: int = 6_350


@dataclass(frozen=True)
class GlossaryTable:
    """A complete two-column glossary table specification."""

    name: str
    title: str
    box: Box
    col_headers: tuple[str, str]
    col_widths: tuple[float, float]
    entries: tuple[GlossaryEntry, ...]
    style: GlossaryTableStyle
    banner_h: float = 0.0
    header_h: float = 0.0
    row_h: float = 0.0


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
    """Only draw sides passed as L/R/T/B; omitted sides render as no-fill."""

    return {k: v for k, v in edges.items() if v is not None} or None


def plain_cell(
    text: str = "",
    *,
    fill=None,
    bold: bool = False,
    italic: bool = False,
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
    """Single-run table cell: content first, table mechanics second."""

    return tcell(
        text,
        fill=fill,
        bold=bold or None,
        italic=italic or None,
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
    """Multi-run/multi-paragraph table cell: content first, mechanics second."""

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
# Content helpers: readable glossary definitions, no raw table OOXML.
# ════════════════════════════════════════════════════════════════════════════
def d_run(text: str, *, bold: bool = False, italic: bool = False,
          color: str | None = None, size_pt: float = 12) -> DefinitionRun:
    """One run in a rich definition cell; defaults are this slide's table norm."""

    return DefinitionRun(text, bold=bold, italic=italic, color=color, size_pt=size_pt)


def d_rich(*runs: DefinitionRun, mar_l: int | None = None,
           indent: int | None = None) -> RichDefinition:
    """Definition made of multiple runs. mar_l/indent are emitted only if passed."""

    return RichDefinition(tuple(runs), mar_l=mar_l, indent=indent)


def _definition_run_xml(run_spec: DefinitionRun, *, default_color: str) -> dict:
    return trun(
        run_spec.text,
        size=PT(run_spec.size_pt),
        bold=run_spec.bold or None,
        italic=run_spec.italic or None,
        color=run_spec.color if run_spec.color is not None else default_color,
        font=FONT,
    )


def _definition_paragraph(definition: RichDefinition, *, style: GlossaryTableStyle) -> dict:
    return tpara(
        [_definition_run_xml(run_spec, default_color=style.definition_text_color) for run_spec in definition.runs],
        mar_l=definition.mar_l,
        indent=definition.indent,
    )


# ════════════════════════════════════════════════════════════════════════════
# Glossary content. Definitions are plain strings unless they need rich runs.
# ════════════════════════════════════════════════════════════════════════════
INDUSTRIAL_POLICY_ENTRIES: tuple[GlossaryEntry, ...] = (
    GlossaryEntry("ITC", "Investment Tax Credit"),
    GlossaryEntry("MAP", "Maritime Action Plan"),
    GlossaryEntry("MSP", "Maritime Security Program"),
    GlossaryEntry("MSTF", "Maritime Security Trust Fund"),
    GlossaryEntry("NDRF", "National Defense Reserve Fleet"),
    GlossaryEntry("OBBBA", "One Big Beautiful Bill Act (Reconciliation)"),
    GlossaryEntry("SCF", "Strategic Commercial Fleet"),
    GlossaryEntry("TSP", "Tanker Security Program"),
    GlossaryEntry("USTR", "US Trade Representative"),
)

MARKET_ENTRIES: tuple[GlossaryEntry, ...] = (
    GlossaryEntry("CGT", "Compensated Gross Ton"),
    GlossaryEntry("DWT", "Deadweight Ton"),
    GlossaryEntry("FEU", d_rich(d_run("Forty-Foot Equivalent Unit "), d_run("(Container)", italic=True))),
    GlossaryEntry("FSV", "Fast Supply Vessel"),
    GlossaryEntry("GT", "Gross Ton"),
    GlossaryEntry("OSV", "Offshore Support Vessel"),
    GlossaryEntry("PSV", "Platform Supply Vessel"),
    GlossaryEntry("RORO", "Roll-on, Roll-off ship "),
    GlossaryEntry("TEU", d_rich(d_run("Twenty-Foot Equivalent Unit "), d_run("(Container)", italic=True))),
    GlossaryEntry("THC", d_rich(d_run("Terminal Handling Charges "), d_run("(Incl. stevedoring)", italic=True), mar_l=0, indent=0)),
    GlossaryEntry("VOCC", d_rich(d_run("Vessel Operating Common Carriers"), mar_l=0, indent=0)),
    GlossaryEntry("WTI", d_rich(d_run("West Texas Intermediate "), d_run("(Crude prices, $ / barrel)", italic=True), mar_l=0, indent=0)),
)

ANALYSIS_ENTRIES: tuple[GlossaryEntry, ...] = (
    GlossaryEntry("Reference Vessel", d_rich(d_run("~900’ 3,600 TEU containership, Panamax size"), mar_l=0, indent=0)),
    GlossaryEntry("BuildCo", d_rich(d_run("Port Alpha"), mar_l=0, indent=0)),
    GlossaryEntry("OpCo", d_rich(d_run("Saronic as owner/operator"), mar_l=0, indent=0)),
    GlossaryEntry(
        "ComboCo ",
        d_rich(
            d_run("BuildCo"),
            d_run(" & "),
            d_run("OpCo"),
            d_run(" combined (excl. Tech/"),
            d_run("ParentCo"),
            d_run(")"),
            mar_l=0,
            indent=0,
        ),
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Table specs: styling and geometry are explicit per table.
# ════════════════════════════════════════════════════════════════════════════
INDUSTRIAL_POLICY_TABLE = GlossaryTable(
    name="IndustrialPolicyGlossary",
    title="Industrial Policy Terms",
    box=Box(0.495, 1.491, 6.000, 3.300),
    col_headers=("Abbreviation", "Full Name"),
    col_widths=(1.700, 4.300),
    entries=INDUSTRIAL_POLICY_ENTRIES,
    style=GlossaryTableStyle(banner_fill=GRAY_2),
)

MARKET_TABLE = GlossaryTable(
    name="MarketTermsGlossary",
    title="Market Terms",
    box=Box(6.835, 1.491, 6.000, 4.200),
    col_headers=("Abbreviation", "Full Name"),
    col_widths=(1.700, 4.300),
    entries=MARKET_ENTRIES,
    style=GlossaryTableStyle(banner_fill=GRAY_3),
    banner_h=0.214,
    header_h=0.214,
    row_h=0.214,
)

ANALYSIS_TABLE = GlossaryTable(
    name="AnalysisTermsGlossary",
    title="Analysis Terms",
    box=Box(0.495, 5.002, 6.000, 1.800),
    col_headers=("Term", "Definition"),
    col_widths=(1.700, 4.300),
    entries=ANALYSIS_ENTRIES,
    style=GlossaryTableStyle(
        banner_fill="447BB2",
        banner_text_color=WHITE,
        definition_text_color=DK,
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Table builders. These are intentionally slide-local teaching examples.
# ════════════════════════════════════════════════════════════════════════════
def _banner_row(spec: GlossaryTable) -> dict:
    return trow(
        [
            plain_cell(
                spec.title,
                size_pt=12,
                bold=True,
                color=spec.style.banner_text_color,
                align="ctr",
                fill=spec.style.banner_fill,
                span=2,
            )
        ],
        h=IN(spec.banner_h),
    )


def _column_header_row(spec: GlossaryTable) -> dict:
    header_rule = edge(spec.style.header_rule_color, spec.style.header_rule_width)
    left, right = spec.col_headers
    return trow(
        [
            plain_cell(left, size_pt=12, bold=True, B=header_rule),
            plain_cell(right, size_pt=12, bold=True, B=header_rule),
        ],
        h=IN(spec.header_h),
    )


def _definition_cell(definition: str | RichDefinition, spec: GlossaryTable, **edges):
    if isinstance(definition, str):
        return plain_cell(
            definition,
            size_pt=12,
            color=spec.style.definition_text_color,
            **edges,
        )
    return rich_cell(
        [_definition_paragraph(definition, style=spec.style)],
        **edges,
    )


def _glossary_rows(spec: GlossaryTable) -> list[dict]:
    """Build data rows with a thick first top rule, hairline interior rules, and
    an open foot on the last row. This mirrors the source's table grammar."""

    hairline = edge(spec.style.row_rule_color, spec.style.row_rule_width)
    header_top = edge(spec.style.header_rule_color, spec.style.header_rule_width)
    last = len(spec.entries) - 1
    rows: list[dict] = []
    for idx, entry in enumerate(spec.entries):
        top_rule = header_top if idx == 0 else hairline
        row_edges = {"T": top_rule} if idx == last else {"T": top_rule, "B": hairline}
        rows.append(
            trow(
                [
                    plain_cell(entry.term, size_pt=12, color=spec.style.term_text_color, **row_edges),
                    _definition_cell(entry.definition, spec, **row_edges),
                ],
                h=IN(spec.row_h),
            )
        )
    return rows


def paint_glossary_table(out: list[str], ids: ShapeIds, spec: GlossaryTable) -> None:
    # col_widths defines the abbreviation/term and definition tracks. trow(h=...)
    # is a row minimum, not a cap; zero-height rows let the table frame distribute
    # fit like the source table. The local helpers above own insets, alignment,
    # spans, and border sides.
    out.append(
        table(
            ids.next(),
            spec.name,
            *spec.box.emu(),
            col_widths=[IN(w) for w in spec.col_widths],
            rows=[
                _banner_row(spec),
                _column_header_row(spec),
                *_glossary_rows(spec),
            ],
        )
    )


# ════════════════════════════════════════════════════════════════════════════
# Slide render. Document order is PowerPoint paint order.
# ════════════════════════════════════════════════════════════════════════════
def _body() -> str:
    out: list[str] = []
    ids = ShapeIds(start=100)

    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE.
    paint_glossary_table(out, ids, INDUSTRIAL_POLICY_TABLE)
    paint_glossary_table(out, ids, MARKET_TABLE)
    paint_glossary_table(out, ids, ANALYSIS_TABLE)

    return "".join(out)


CHROME = Chrome(
    section="Commercial Strategy",
    topic="Research Overview",
    title="For Reference",
    takeaway="Key Terms Glossary.",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
