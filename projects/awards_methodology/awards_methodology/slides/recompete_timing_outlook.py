"""recompete_timing_outlook — slides new preview deck, source slide 7.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); pattern-fill swatches become
text_box(pattern_fill=…) and freeform <a:custGeom> icons become custom_geometry()
over a deduped path constant; think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=19, connector=1, chart=0, table=1, picture=0, custom_geometry=0, chrome_builders=3, clusters=2 (covering 6 shapes), raw_verbatim=0, dropped=0, frozen_fields=0.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, connector, table, trow, tcell, tcell_rich,
    breadcrumb, slide_title, preliminary_chip, IN, PT,
)

# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
BLUE_3 = "6E91B1"
BLUE_4 = "3D5972"
BLUE_5 = "263746"
GRAY_1 = "F2F2F2"
GRAY_4 = "7F7F7F"
FONT = "Arial"

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets, borders,
#    spans). Renders identically to raw tcell()/tcell_rich(); hand-polish the cells from here. ──
PAD = dict(l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960)   # the source's heavier cell padding


def edge(color, w=12700):
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", vert=None, span=1, rowspan=1,
         l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, vert=vert, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def rcell(paras, *, fill=None, anchor="ctr", vert=None, span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor, vert=vert,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))

# ── layout anchors (shared coordinates) ──
_NODE_H = IN(0.3)
_LBL_Y, _LBL_W, _LBL_H = IN(6.52), IN(1.45), IN(0.22)
_W1 = IN(0.16)   # shared x4
_W2 = IN(0.18)   # shared x7
_H1 = IN(0.22)   # shared x8

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: TODO - flow nodes; sample: OPN base · $XXM, Follow-on OPN · $XXM (illus.), SCN forward-fit · $XXM
_FLOW_NODES = [    # (x, y, cx, fill, label) x3
    (1.655, 3.12, 3.048, BLUE_4, "OPN base · $XXM"),
    (8.047, 3.12, 2.752, BLUE_4, "Follow-on OPN · $XXM (illus.)"),
    (1.655, 3.57, 5.08, BLUE_5, "SCN forward-fit · $XXM"),
]

# local_meaning: TODO - labels; sample: RDT&E,N · 2-yr, OPN · 3-yr, SCN · 5-yr
_LABELS = [    # (x, label) x3
    (1.92, "RDT&E,N · 2-yr"),
    (3.02, "OPN · 3-yr"),
    (3.92, "SCN · 5-yr"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(slide_title("Recompete Timing and Outlook", "Ordering window closed FY26, recompete now open, no successor visible."))
    out.append(preliminary_chip())
    out.append(text_box(n(), "Illustrative chip", IN(9.524), IN(0.122), IN(1.605), IN(0.317), [paragraph([run("Illustrative", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="A6A6A6", line_color=BLACK, line_width=19050, anchor="ctr", l_ins=45720, t_ins=9144, r_ins=45720, b_ins=9144))
    out.append(text_box(n(), "Program", IN(0.495), IN(1.54), IN(9.3), IN(0.3), [paragraph([run("AN/SLQ-25 Nixie", size=PT(12), bold=True, color=BLACK, font=FONT), run("   ·   IDIQ N0025321D0002   ·   Ultra Electronics Ocean Systems", size=PT(12), color=BLACK, font=FONT)], align="l", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "FY Lane Grid", IN(0.495), IN(2.05), IN(12.336), IN(4.29), col_widths=[IN(1.16), IN(1.016), IN(1.016), IN(1.016), IN(1.016), IN(1.016), IN(1.016), IN(1.016), IN(1.016), IN(1.016), IN(1.016), IN(1.016)], rows=[
        trow([cell("", size=PT(10), align="ctr", B=edge(BLACK)), cell("FY21", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", R=edge("808080", 6350), B=edge(BLACK)), cell("FY22", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("FY23", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("FY24", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("FY25", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("FY26", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("FY27", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("FY28", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("FY29", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("FY30", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("FY31", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", L=edge("808080", 6350), B=edge(BLACK))], h=IN(0.28)),
        trow([cell("What program needs", size=PT(10), bold=True, color=BLACK, align="ctr", B=edge("808080", 6350)), cell("", size=PT(10), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), B=edge("808080", 6350))], h=IN(0.56)),
        trow([cell("Funding", size=PT(10), bold=True, color=BLACK, align="ctr", B=edge("808080", 6350)), cell("", size=PT(10), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge("808080", 6350)), cell("", size=PT(10), L=edge("808080", 6350), B=edge("808080", 6350))], h=IN(1.35)),
        trow([cell("Contracting", size=PT(10), bold=True, color=BLACK, align="ctr", B=edge(BLACK)), cell("", size=PT(10), R=edge("808080", 6350), B=edge(BLACK)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("", size=PT(10), L=edge("808080", 6350), R=edge("808080", 6350), B=edge(BLACK)), cell("", size=PT(10), L=edge("808080", 6350), B=edge(BLACK))], h=IN(2.1)),
    ]))
    out.append(text_box(n(), "Planned procurement", IN(1.655), IN(2.47), IN(11.176), IN(0.3), [paragraph([run("Planned procurement (units)", size=PT(9), bold=True, color=BLACK, font=FONT), run("   illustrative, pending P-1", size=PT(9), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color=DK, dashed_line=True, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    for _x, _y, _cx, _fill, _t in _FLOW_NODES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _NODE_H, [paragraph([run(_t, size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=WHITE, line_width=6350, anchor="ctr", l_ins=45720, t_ins=18000, r_ins=45720, b_ins=18000))
    out.append(connector(n(), "Obligation tie", IN(10.799), IN(3.42), IN(0), IN(1.36), color=GRAY_4, width=6350, dash="dash"))
    out.append(text_box(n(), "Active Ordering Period", IN(1.867), IN(4.36), IN(5.083), IN(0.5), [paragraph([run("Active Ordering Period", size=PT(11), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("26 orders · $103.1M realized", size=PT(9), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color=DK, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Likely Recompete Window", IN(6.949), IN(4.36), IN(2.328), IN(0.5), [paragraph([run("Likely Recompete Window", size=PT(11), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("open now · no successor in data", size=PT(9), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color=GRAY_4, dashed_line=True, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Start marker", IN(1.787), IN(4.8), _W1, _W1, [paragraph([], line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="ellipse", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Last-order marker", IN(6.869), IN(4.8), _W1, _W1, [paragraph([], line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="ellipse", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Obligation marker", IN(10.709), IN(4.78), _W2, IN(0.2), [paragraph([], line_spacing=100000)], fill=GRAY_4, line_color=DK, prst="triangle", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Start date", IN(1.66), IN(4.96), IN(1.05), _H1, [paragraph([run("2020-12-15", size=PT(9), bold=True, color=BLACK, font=FONT)], align="l", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    out.append(text_box(n(), "Last-order date", IN(6.499), IN(4.96), IN(0.9), _H1, [paragraph([run("2025-12-16", size=PT(9), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    out.append(text_box(n(), "Start desc", IN(1.66), IN(5.19), IN(2), _H1, [paragraph([run("Ordering period starts", size=PT(9), color=BLACK, font=FONT)], align="l", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    out.append(text_box(n(), "Last-order desc", IN(6.249), IN(5.19), IN(1.4), _H1, [paragraph([run("Common last date to order", size=PT(9), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    out.append(text_box(n(), "Obligation desc", IN(8.949), IN(5.05), IN(2), _H1, [paragraph([run("Obligation window complete", size=PT(9), italic=True, color=BLACK, font=FONT)], align="r", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    out.append(text_box(n(), "Legend label", IN(0.495), IN(6.52), IN(1.2), _H1, [paragraph([run("Color of money:", size=PT(9), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    out.append(text_box(n(), "Legend swatch", IN(1.7), IN(6.54), _W2, _W2, [paragraph([], line_spacing=100000)], fill=BLUE_3, line_color=WHITE, line_width=6350, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    for _x, _t in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), _LBL_Y, _LBL_W, _LBL_H, [paragraph([run(_t, size=PT(9), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    out.append(text_box(n(), "Legend swatch", IN(2.8), IN(6.54), _W2, _W2, [paragraph([], line_spacing=100000)], fill=BLUE_4, line_color=WHITE, line_width=6350, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Legend swatch", IN(3.7), IN(6.54), _W2, _W2, [paragraph([], line_spacing=100000)], fill=BLUE_5, line_color=WHITE, line_width=6350, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Legend note", IN(4.75), IN(6.52), IN(2.7), _H1, [paragraph([run("bar length = obligation window", size=PT(9), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    out.append(text_box(n(), "Legend key", IN(9.6), IN(6.52), IN(3.24), _H1, [paragraph([run("Solid: contract data  ·  Dashed: inferred", size=PT(9), italic=True, color=BLACK, font=FONT)], align="r", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    return "".join(out)


def render() -> str:
    return slide(_body())
