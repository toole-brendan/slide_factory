"""coordination_archetypes — Commercial Strategy Market Analysis deck (20260325), source slide 166.

EXHIBIT — "Coordination Archetypes": a single full-width reference table cataloguing
the entities that play in the Coordination step of the commercial maritime value
chain (subtitle: "Numerous entities play in the Coordination step of the value
chain."). Three columns — Categories · Archetypes · Responsibilities — list 18
archetypes grouped under five row-spanned category bands: Strategic & Integrated
Coordinators (BCO, 4PL), Operational & Execution Coordinators (3PL, Freight
Forwarders, Intermodal Marketing, Domestic Freight Broker, Drayage), Legal &
Contractual Coordinators (NVOCC, Customs Broker, Slot Charterer, Shipbroker),
Asset & Equipment Coordinators (IEP, Container Leasing, Empty Container Depots),
and "Financia & Risk Coordinators" (Commercial Banks, P&I Clubs, Marine Surveyor).
The category cells merge downward via row_span; horizontal hairline rules (808080)
separate archetype rows beneath a heavier black header underline.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ......... breadcrumb() + title_placeholder()
  • archetype table  one native table() (low-level table()/trow()/tcell()), col_widths
                     [1.546, 2.588, 8.167]; header row + 18 archetype rows; the five
                     Categories cells span their rows via row_span (2/5/4/3/3)

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: table=1, chrome_builders=2, dropped=1 (think-cell OLE frame).
Residue: the source's "Financia & Risk Coordinators" category label is misspelled
(missing the trailing "l"); kept verbatim so the render stays byte-identical.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder, IN,
    PT, BLACK, WHITE, FONT, edge, bd, cell, rcell,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell()/tcell_rich() form —
#    the only change is legibility. ──


# ── repeated-shape data table (drives _archetype_rows() in _body) ──
# local_meaning: the coordination archetypes, grouped under five row-spanned category
#   bands. Each group is (category label, category row_span, rows); each row is
#   (archetype, responsibility, h) where responsibility is a str (plain cell) or a
#   list[tpara] (rich cell, for the two split-run definitions). Border roles — the
#   header underline, hairline row separators, the open table foot, and the WHITE
#   right rule down the Responsibilities column — are applied by row position in
#   _archetype_rows(), not stored here.
_ARCHETYPE_GROUPS = [
    ("Strategic & Integrated Coordinators ", 2, [
        ("Beneficial Cargo Owner (BCO)", "Owns cargo and manages logistics using internal staff and direct carrier contracts", IN(0)),
        ("Fourth-Party Logistics (4PL)", [tpara([trun("Manages and optimizes entire supply chain for shippers; ", size=PT(10), color=BLACK, font=FONT), trun("does not own assets", size=PT(10), color=BLACK, font=FONT)])], IN(0.174)),
    ]),
    ("Operational & Execution Coordinators", 5, [
        ("Third-Party Logistics (3PL)", "Coordinates functional tasks such as warehousing, fulfillment, picking/packing, and regional distribution for shippers", IN(0)),
        ("Freight Forwarders", "Orchestrates multimodal transport and manages documentation; acts on behalf of shippers but does not assume liability of carriers", IN(0.174)),
        ("Intermodal Marketing Company", "Secures rail capacity by purchasing slots in bulk to provide inland rail transport", IN(0.174)),
        ("Domestic Freight Broker", "Coordinates domestic trucking capacity, matching independent drivers or small fleets with the inland needs of 3PLs or BCOs", IN(0.174)),
        ("Origin & Destination Drayage", "Moves containers between factories, rail ramps, and port terminals via truck", IN(0)),
    ]),
    ("Legal & Contractual Coordinators", 4, [
        ("Non-Vessel Operating Common Carrier", [tpara([trun("Books space on operator vessels and resells to shippers without owning ships; a", size=PT(10), color=BLACK, font=FONT), trun("ssumes direct legal liability for cargo", size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0)], IN(0)),
        ("Customs Broker", "Manages import/export customs and compliance", IN(0)),
        ("Slot Charterer", "Purchases container space on another carrier’s vessel to expand network without capital risk of operating an entire ship", IN(0.174)),
        ("Shipbroker", "Negotiates \"Charter Parties\" (leasing contracts) and vessel sale-and-purchase transactions between owners and operators", IN(0.174)),
    ]),
    ("Asset & Equipment Coordinators", 3, [
        ("IEP (Intermodal Equipment Provider)", "Owns and distributes chassis (trailers required to transport containers by road)", IN(0)),
        ("Container Leasing Companies", "Leases containers to ocean liners and NVOCCs, managing global inventory and repositioning of equipment", IN(0)),
        ("Empty Container Depots", "Coordinates storage, inspection, and repositioning of empty boxes", IN(0)),
    ]),
    ("Financia & Risk Coordinators", 3, [
        ("Commercial Banks & Trade Finance ", "Facilitates movement of money via Letters of Credit (LC), ensuring payment only when proof of shipment (Bill of Lading) is provided", IN(0.174)),
        ("P&I Clubs / Marine Insurers ", "Provides liability coverage for global ocean tonnage, managing the \"legal safety net\" for cargo loss or ship collisions", IN(0.174)),
        ("Marine Cargo Surveyor", "Verifies cargo condition and proper stowage, providing data needed to coordinate insurance claims between carriers and shippers", IN(0.174)),
    ]),
]


def _archetype_rows():
    """Build the archetype rows from _ARCHETYPE_GROUPS, applying the table's border
    roles by position: a BLACK 1pt underline beneath the header (the first data
    row's top), 808080 hairline separators between rows, an open foot (no bottom
    rule on the last row / last category band), and a WHITE right rule down the
    Responsibilities column."""
    HAIR = edge("808080", 6350)                  # uniform hairline row separator
    groups = _ARCHETYPE_GROUPS
    n_rows = sum(len(items) for _, _, items in groups)
    rows, di = [], 0
    for gi, (category, rspan, items) in enumerate(groups):
        last_group = (gi == len(groups) - 1)
        for ri, (archetype, responsibility, h) in enumerate(items):
            top = edge(BLACK) if di == 0 else HAIR       # header underline vs hairline
            row_b = {} if di == n_rows - 1 else {"B": HAIR}   # last row: open foot
            cells = []
            if ri == 0:                                  # category band spans the group
                cat_b = {} if last_group else {"B": HAIR}
                cells.append(cell(category, fill=WHITE, rowspan=rspan, T=top, **cat_b))
            cells.append(cell(archetype, fill=WHITE, T=top, **row_b))
            resp = rcell if isinstance(responsibility, list) else cell
            cells.append(resp(responsibility, fill=WHITE, T=top, R=edge(WHITE), **row_b))
            rows.append(trow(cells, h=h))
            di += 1
    return rows


# ── table-cell layout commentary ──
# table(): col_widths are column-level sizing and trow(h=...) is a minimum row
# height. Each tcell/tcell_rich owns internal padding via l_ins/r_ins/t_ins/b_ins
# and vertical alignment via anchor=...; horizontal alignment and paragraph
# margins live in tcell(..., align=...) or tpara(..., align=..., mar_l=..., indent=...).

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome ──
    out.append(breadcrumb("Commercial Maritime Value Chain", "Coordination Archetypes"))
    out.append(title_placeholder("Coordination Archetypes", "Numerous entities play in the Coordination step of the value chain."))
    # ── archetype table — Categories × Archetypes × Responsibilities ──
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    # header row, then 18 archetype rows; the five Categories cells span via row_span
    # palette — text: 000000 black; fills: FFFFFF white (all cells);
    #   rules: 000000 black (header underline) · 808080 gray (row hairlines) · FFFFFF white (right column rule).
    out.append(table(n(), "Table 11", IN(0.495), IN(1.641), IN(12.3), IN(4.8), col_widths=[IN(1.546), IN(2.588), IN(8.167)], rows=[
        trow([
            rcell([tpara([trun("Categories", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=WHITE, anchor="b", B=edge(BLACK)),
            rcell([tpara([trun("Archetypes", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=WHITE, anchor="b", B=edge(BLACK)),
            rcell([tpara([trun("Responsibilities", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=WHITE, anchor="b", R=edge(WHITE), B=edge(BLACK)),
        ], h=IN(0)),
        *_archetype_rows(),
    ]))
    return "".join(out)


def render() -> str:
    return slide(_body())
