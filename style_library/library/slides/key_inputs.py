"""key_inputs — Commercial Strategy Market Analysis deck (20260325), source slide 167.

EXHIBIT — "Key Inputs": a single full-width reference table cataloguing every
model input behind the Matson carrier-entry test case and where each one comes
from. Three columns — Category / Inputs / Source — with the left spine grouping
the inputs into four row-span blocks: Volume (voyages per vessel, cargo capacity,
utilization, Hawaii/Guam volumes, loaded-cargo direction & composition, TEU/FEU
mix), Price (commodity TEU/FEU rates, Fuel Adjustment Factor, shoreside charges),
Variable Costs (fuel costs with a bulleted sub-list, pilotage/dockage/tug/port
dues, shoreside charges), and Operating Expenses (crew, insurance, stores &
spares, R&M, dry-dock, management & admin, D&A). The Source column cites AIS via
Global Fishing Watch, Matson filings/investor presentations, internal estimates,
Reeve & Associates, USACE, Hapag-Lloyd, Pasha Hawaii, and open-source research.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ........ breadcrumb() + title_placeholder() + prelim_chip() (house builders)
  • inputs table .. one native table() ("Table 610"); 23 trow()s built low-level
                    from tcell_rich(); the Category spine and multi-line Source
                    cells span rows/cols via row_span / grid_span

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.
(No converter-generated data clusters or layout-anchor constants exist on
this slide — it is one table call — so no cluster rename was required; table-cell
layout commentary was added in place.)

Converter stats: table=1, chrome_builders=3, dropped=1 (think-cell OLE frame).
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, table, trow, tcell, tcell_rich, tpara, trun, tbreak, breadcrumb,
    title_placeholder, prelim_chip, IN, PT, BLACK, DK, FONT, edge, bd, rcell,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (borders,
#    spans). Renders identically to the raw tcell_rich() form — the only change is
#    legibility. (Every cell here is rich, so only rcell is needed.) ──


def r(text, *, b=False, i=False, u=False, color=BLACK, size=PT(10)):
    """One styled run (Arial FONT; size defaults to this table's dominant PT10)."""
    return trun(text, size=size, bold=b or None, italic=i or None, underline=u or None, color=color, font=FONT)


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
    # ── chrome ──
    out.append(breadcrumb("Carrier Entry Point Attractiveness", "Matson Test Case"))
    out.append(title_placeholder("Key Inputs", ""))
    out.append(prelim_chip())
    # ── inputs table — Category / Inputs / Source; merges via row_span/grid_span ──
    # col_widths defines the four column tracks and trow(h=...) the row minima.
    # Repeating cell insets/anchor/align across a block is the row- or column-
    # level padding/alignment policy; tpara mar_l/indent owns paragraph margins.
    # palette - text: 000000 black (header + Volume block) · 162029 dark navy (Price/Variable/Operating labels);
    #   fills: none; rules: 162029 dark navy (header + block tops) · 808080 gray (inner gridlines).
    out.append(table(n(), "Table 610", IN(0.484), IN(1.059), IN(12.3), IN(5.933), col_widths=[IN(1.505), IN(2.968), IN(2.968), IN(4.86)], rows=[
        # header row — Category | Inputs (spans 2 cols) | Source
        trow([rcell([tpara([r("Category", b=1)], align="ctr", mar_l=0, indent=0)], B=edge(DK)), rcell([tpara([r("Inputs", b=1)], align="ctr", mar_l=0, indent=0)], span=2, B=edge(DK)), rcell([tpara([r("Source", b=1)], align="ctr", mar_l=0, indent=0)], B=edge(DK))], h=IN(0)),
        # Volume block (Category cell rowspan=7)
        trow([rcell([tpara([r("Volume")], mar_l=0, indent=0)], rowspan=7, T=edge(DK), B=edge("808080", 6350)), rcell([tpara([r("Number of voyages per vessel")], mar_l=0, indent=0)], span=2, T=edge(DK), B=edge("808080", 6350)), rcell([tpara([r("Historical AIS data (accessed via Global Fishing Watch)")], mar_l=0, indent=0)], T=edge(DK), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Cargo capacity by vessel (TEUs, Reefer, and Autos) ")], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Matson public filings"), tbreak(), r("Matson investor presentations"), tbreak(), r("Internal estimates (utilization levels and Q4 ’25 volume)")], mar_l=0, indent=0)], rowspan=3, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Utilization levels by cargo type and route")], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Matson Hawaii and Guam service volumes (2024 and 2025)")], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Proportion of loaded Hawaii cargo by direction (WB and EB)")], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Reeve & Associates"), tbreak(), r("US Army Corps of Engineers (proportion of loaded cargo)")], mar_l=0, indent=0)], rowspan=2, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Composition of Hawaii cargo by direction (WB and EB)")], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("TEU / FEU mix by cargo type ")], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Hapag-Lloyd (container payload); Internal estimates")], mar_l=0, indent=0)], T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        # Price block (Category cell rowspan=3; Source "Pasha Hawaii" rowspan=3)
        trow([rcell([tpara([r("Price", color=DK)], mar_l=0, indent=0)], rowspan=3, T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Commodity-level TEU / FEU rates")], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Pasha Hawaii")], mar_l=0, indent=0)], rowspan=3, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Fuel Adjustment Factor", color=DK)], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Shoreside charges (handling/stevedoring, wharfage, and other fees)", color=DK)], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        # Variable Costs block (Category cell rowspan=3); fuel-cost row has bulleted sub-lists across two cells
        trow([rcell([tpara([r("Variable Costs", color=DK)], mar_l=0, indent=0)], rowspan=3, T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Fuel Costs:", color=DK)], mar_l=0, indent=0),
            tpara([r("Distance traveled by vessel and route", color=DK)], bullet=True, mar_l=171450, indent=-171450),
            tpara([r("Transit speeds by vessel and route", color=DK)], bullet=True, mar_l=171450, indent=-171450)], T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Fuel type used (scrubber presence)", color=DK)], bullet=True, mar_l=171450, indent=-171450),
            tpara([r("Other fuel burn / engine parameters", color=DK)], bullet=True, mar_l=171450, indent=-171450),
            tpara([r("Bunker fuel prices", color=DK)], bullet=True, mar_l=171450, indent=-171450)], T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Historical AIS data (accessed via Global Fishing Watch)"), r("; Open-source research; Internal estimates")], mar_l=0, indent=0)], T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Pilotage, dockage, tugboat, and port due fees", color=DK)], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Open-source research")], mar_l=0, indent=0)], T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Shoreside charges ", color=DK), r("(same as above)", i=1, color=DK)], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Pasha Hawaii ")], mar_l=0, indent=0)], T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        # Operating Expenses block (Category cell rowspan=7; shared Source cell rowspan=7)
        trow([rcell([tpara([r("Operating Expenses", color=DK)], mar_l=0, indent=0)], rowspan=7, T=edge("808080", 6350)), rcell([tpara([r("Crew", color=DK)], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350)), rcell([tpara([r("Open-source research"), tbreak(), r("Internal estimates (based on industry experience)")], mar_l=0, indent=0)], rowspan=7, T=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Insurance", color=DK)], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Stores & spares", color=DK)], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("R&M", color=DK)], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Dry-dock (annualized)", color=DK)], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Management & administrative", color=DK)], mar_l=0, indent=0)], span=2, T=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0)),
        trow([rcell([tpara([r("Depreciation & amortization", color=DK)], mar_l=0, indent=0)], span=2, T=edge("808080", 6350))], h=IN(0)),
    ]))
    return "".join(out)


def render() -> str:
    return slide(_body())
