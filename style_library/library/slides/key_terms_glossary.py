"""key_terms_glossary — Commercial Strategy Market Analysis deck (20260325), source slide 5.

EXHIBIT — "For Reference · Key Terms Glossary": a reference page of three two-column
definition tables, each a banner header row spanning both columns over an
Abbreviation/Full-Name (or Term/Definition) header and a list of entries. Top-left
(GRAY_2 banner) = "Industrial Policy Terms" — ITC … USTR. Top-right (GRAY_3 banner,
the longest table) = "Market Terms" — CGT … WTI, several full names carrying an
italic parenthetical (e.g. FEU/TEU "(Container)", WTI "(Crude prices, $ / barrel)").
Bottom-left (447BB2 blue banner, WHITE title) = "Analysis Terms" — Reference Vessel /
BuildCo / OpCo / ComboCo, definitions set in DK with inline italic/coloured runs.
All rules are hairline 808080 row separators under a thicker BLACK header underline.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place — the two
house-chrome builders interleave between the first and second table):
  • Table 8 ........ "Industrial Policy Terms" glossary (top-left), table()/trow()/tcell()
  • chrome ......... title_placeholder("For Reference", "Key Terms Glossary.") + breadcrumb()
  • Table 10 ....... "Market Terms" glossary (top-right); tcell_rich() rows carry the
                     italic parentheticals, so they use tpara()/trun() not plain tcell()
  • Table 6 ........ "Analysis Terms" glossary (bottom-left); tcell_rich() definitions

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: table=3, chrome_builders=2, dropped=1 (think-cell OLE frame).
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder, IN,
    PT, BLACK, WHITE, DK, GRAY_2, GRAY_3, FONT, edge, bd, cell, rcell,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell()/tcell_rich() form —
#    the only change is legibility. ──


# ── glossary content (each list drives _glossary_rows() in _body) ──
# Every glossary shares one two-column shape: (term, definition) where definition is
# a str (plain cell) or a list[tpara] (rich cell — italic parentheticals or coloured
# definitions). The border roles (BLACK header underline, 808080 hairline separators,
# open foot) are applied by row position in _glossary_rows(), not stored per entry.
_INDUSTRIAL_POLICY_TERMS = [    # Table 8 (top-left) — abbreviation, full name
    ("ITC", "Investment Tax Credit"),
    ("MAP", "Maritime Action Plan"),
    ("MSP", "Maritime Security Program"),
    ("MSTF", "Maritime Security Trust Fund"),
    ("NDRF", "National Defense Reserve Fleet"),
    ("OBBBA", "One Big Beautiful Bill Act (Reconciliation)"),
    ("SCF", "Strategic Commercial Fleet"),
    ("TSP", "Tanker Security Program"),
    ("USTR", "US Trade Representative"),
]
_MARKET_TERMS = [    # Table 10 (top-right) — abbreviation, full name; italic parentheticals are rich
    ("CGT", "Compensated Gross Ton"),
    ("DWT", "Deadweight Ton"),
    ("FEU", [tpara([trun("Forty-Foot Equivalent Unit ", size=PT(12), font=FONT), trun("(Container)", size=PT(12), italic=True, font=FONT)])]),
    ("FSV", "Fast Supply Vessel"),
    ("GT", "Gross Ton"),
    ("OSV", "Offshore Support Vessel"),
    ("PSV", "Platform Supply Vessel"),
    ("RORO", "Roll-on, Roll-off ship "),
    ("TEU", [tpara([trun("Twenty-Foot Equivalent Unit ", size=PT(12), font=FONT), trun("(Container)", size=PT(12), italic=True, font=FONT)])]),
    ("THC", [tpara([trun("Terminal Handling Charges ", size=PT(12), color=BLACK, font=FONT), trun("(Incl. stevedoring)", size=PT(12), italic=True, color=BLACK, font=FONT)], mar_l=0, indent=0)]),
    ("VOCC", [tpara([trun("Vessel Operating Common Carriers", size=PT(12), color=BLACK, font=FONT)], mar_l=0, indent=0)]),
    ("WTI", [tpara([trun("West Texas Intermediate ", size=PT(12), color=BLACK, font=FONT), trun("(Crude prices, $ / barrel)", size=PT(12), italic=True, color=BLACK, font=FONT)], mar_l=0, indent=0)]),
]
_ANALYSIS_TERMS = [    # Table 6 (bottom-left) — term, definition; definitions set in DK with inline runs
    ("Reference Vessel", [tpara([trun("~900’ 3,600 TEU containership, Panamax size", size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)]),
    ("BuildCo", [tpara([trun("Port Alpha", size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)]),
    ("OpCo", [tpara([trun("Saronic as owner/operator", size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)]),
    ("ComboCo ", [tpara([trun("BuildCo", size=PT(12), color=DK, font=FONT), trun(" & ", size=PT(12), color=DK, font=FONT), trun("OpCo", size=PT(12), color=DK, font=FONT), trun(" combined (excl. Tech/", size=PT(12), color=DK, font=FONT), trun("ParentCo", size=PT(12), color=DK, font=FONT), trun(")", size=PT(12), color=DK, font=FONT)], mar_l=0, indent=0)]),
]


def _glossary_rows(entries, h):
    """Build a glossary's data rows from (term, definition) pairs at a fixed row
    height. A BLACK 1pt rule tops the first entry (meeting the header underline);
    every interior edge is an 808080 hairline; the last entry has an open foot."""
    HAIR = edge("808080", 6350)                  # uniform hairline row separator
    last = len(entries) - 1
    rows = []
    for i, (term, definition) in enumerate(entries):
        top = edge(BLACK) if i == 0 else HAIR     # first entry meets the header underline
        e = {"T": top} if i == last else {"T": top, "B": HAIR}   # last entry: open foot
        left = cell(term, size=PT(12), **e)
        right = rcell(definition, **e) if isinstance(definition, list) else cell(definition, size=PT(12), **e)
        rows.append(trow([left, right], h=h))
    return rows


# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level layout convention is expressed by repeating the
# same l_ins/r_ins/t_ins/b_ins, anchor, and alignment across the affected cells.
# In tcell()/tcell_rich(), those insets are internal padding and anchor is vertical
# alignment; tcell align or tpara align/mar_l/indent controls horizontal alignment
# and paragraph margins (including hanging bullet indents).


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── Table 8 — "Industrial Policy Terms" (top-left) ──
    # Two col_widths define abbreviation/name tracks and trow(h=...) row minima.
    # Repeated cell insets/anchor/align are the column/row padding-alignment
    # policy; paragraph margins remain at the cell helper defaults.
    # palette — text: 000000 black; fills: D9D9D9 light gray (banner);
    #   rules: 000000 black (header underline) · 808080 gray (row separators).
    out.append(table(n(), "Table 8", IN(0.495), IN(1.491), IN(6), IN(3.3), col_widths=[IN(1.7), IN(4.3)], rows=[
        trow([cell("Industrial Policy Terms", size=PT(12), bold=True, align="ctr", fill=GRAY_2, span=2)], h=IN(0)),
        trow([cell("Abbreviation", size=PT(12), bold=True, B=edge(BLACK)), cell("Full Name", size=PT(12), bold=True, B=edge(BLACK))], h=IN(0)),
        *_glossary_rows(_INDUSTRIAL_POLICY_TERMS, IN(0)),
    ]))
    # ── chrome (interleaves between the first and second table in paint order) ──
    out.append(title_placeholder("For Reference", "Key Terms Glossary."))
    out.append(breadcrumb("Commercial Strategy", "Research Overview"))
    # ── Table 10 — "Market Terms" (top-right, longest table) ──
    # It repeats the same two-column padding/alignment contract; tcell_rich()
    # delegates inline styling and paragraph margins to tpara()/trun().
    # palette — text: 000000 black; fills: BFBFBF silver-gray (banner);
    #   rules: 000000 black (header underline) · 808080 gray (row separators).
    out.append(table(n(), "Table 10", IN(6.835), IN(1.491), IN(6), IN(4.2), col_widths=[IN(1.7), IN(4.3)], rows=[
        trow([cell("Market Terms", size=PT(12), bold=True, align="ctr", fill=GRAY_3, span=2)], h=IN(0.214)),
        trow([cell("Abbreviation", size=PT(12), bold=True, B=edge(BLACK)), cell("Full Name", size=PT(12), bold=True, B=edge(BLACK))], h=IN(0.214)),
        *_glossary_rows(_MARKET_TERMS, IN(0.214)),
    ]))
    # ── Table 6 — "Analysis Terms" (bottom-left, blue 447BB2 banner); tcell_rich() definitions in DK with inline runs ──
    # palette — text: FFFFFF white (banner) · 000000 black (header + terms) · 162029 dark navy (definitions);
    #   fills: 447BB2 blue (banner); rules: 000000 black (header underline) · 808080 gray (row separators).
    out.append(table(n(), "Table 6", IN(0.495), IN(5.002), IN(6), IN(1.8), col_widths=[IN(1.7), IN(4.3)], rows=[
        trow([cell("Analysis Terms", size=PT(12), bold=True, color=WHITE, align="ctr", fill="447BB2", span=2)], h=IN(0)),
        trow([cell("Term", size=PT(12), bold=True, B=edge(BLACK)), cell("Definition", size=PT(12), bold=True, B=edge(BLACK))], h=IN(0)),
        *_glossary_rows(_ANALYSIS_TERMS, IN(0)),
    ]))
    return "".join(out)


def render() -> str:
    return slide(_body())
