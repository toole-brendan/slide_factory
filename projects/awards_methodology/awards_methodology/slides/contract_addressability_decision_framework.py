"""contract_addressability_decision_framework — slides new preview deck, source slide 2.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); pattern-fill swatches become
text_box(pattern_fill=…) and freeform <a:custGeom> icons become custom_geometry()
over a deduped path constant; think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=12, connector=13, chart=0, table=0, picture=0, custom_geometry=0, chrome_builders=3, clusters=2 (covering 9 shapes), raw_verbatim=0, dropped=0, frozen_fields=0.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, connector, line_break,
    breadcrumb, slide_title, preliminary_chip, IN, PT,
)

# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
GRAY_1 = "F2F2F2"
FONT = "Arial"

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates) ──
_NODE_H = IN(0.56)
_W1 = IN(0.7)   # shared x8
_H1 = IN(0.25)   # shared x8

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: TODO - flow nodes; sample: Does the requirement recur?, Can we compete?, Is there budget alignment?
_FLOW_NODES = [    # (x, y, cx, label) x4
    (0.512, 1.457, 2.956, "Does the requirement recur?"),
    (2.748, 2.548, 2.956, "Can we compete?"),
    (5.029, 3.639, 2.956, "Is there budget alignment?"),
    (7.34, 4.73, 2.957, "Can the opportunity be shaped?"),
]

# local_meaning: TODO - flow nodes2; sample: Holder-gated / Incumbent-led, One-time, Open competition
_FLOW_NODES2 = [    # (x, y, cx, cy, label) x5
    (3.426, 3.566, 1.53, 0.23, "Holder-gated / Incumbent-led"),
    (1.34, 2.747, 1.3, 0.2, "One-time"),
    (5.866, 2.945, 1.3, 0.17, "Open competition"),
    (3.503, 1.827, 1.5, 0.2, "FYDP / recurring obligations"),
    (8.43, 3.769, 0.9, 0.3, "Requested appropriations"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(preliminary_chip())
    out.append(slide_title("Contract Addressability", "A recompete opportunity becomes actionable when demand recurs, access exists, and funding is executable."))
    for _x, _y, _cx, _t in _FLOW_NODES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _NODE_H, [paragraph([run(_t, size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", space_after=80, line_spacing=100000)], fill=WHITE, line_color=BLACK, line_width=19050, anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))
    out.append(text_box(n(), "Non Addressable Band", IN(0.495), IN(5.818), IN(7.87), IN(0.552), [paragraph([run("Non-addressable", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color="808080", anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))
    out.append(text_box(n(), "Output Note", IN(8.82), IN(6.185), IN(3.79), IN(0.185), [paragraph([run("Direct recompete  •  vehicle on-ramp  •  prime / holder route", size=PT(8), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Timing Handoff", IN(9.018), IN(6.596), IN(3.4), IN(0.4), [paragraph([run("Determine recompete timing, outlook & pathway", size=PT(10), bold=True, font=FONT), line_break(), run("see following page for timing estimation", size=PT(8), italic=True, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color=BLACK, anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))
    out.append(connector(n(), "Addressable to Timing", IN(10.718), IN(6.302), IN(0), IN(0.294), color=BLACK, width=12700, arrow="tail"))
    out.append(text_box(n(), "Addressable Band", IN(8.602), IN(5.818), IN(4.232), IN(0.552), [paragraph([run("Addressable", size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="223E59", line_color="223E59", anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))
    out.append(connector(n(), "Requirement Yes H", IN(3.468), IN(1.737), IN(0.758), IN(0), color=BLACK, width=12700))
    out.append(connector(n(), "Requirement Yes V", IN(4.226), IN(1.737), IN(0), IN(0.811), color=BLACK, width=12700, arrow="tail"))
    out.append(text_box(n(), "Verdict Chip", IN(3.873), IN(2.141), _W1, _H1, [paragraph([run("Yes", size=PT(9), bold=True, font=FONT)], align="ctr", line_spacing=100000)], fill="D1E8DD", line_color="1B8A57", anchor="ctr", l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144))
    out.append(connector(n(), "Requirement No", IN(1.99), IN(2.017), IN(0), IN(3.801), color=BLACK, width=12700, arrow="tail"))
    out.append(text_box(n(), "Verdict Chip", IN(1.64), IN(3.422), _W1, _H1, [paragraph([run("No", size=PT(9), bold=True, font=FONT)], align="ctr", line_spacing=100000)], fill="F2CCCC", line_color="C00000", anchor="ctr", l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144))
    out.append(connector(n(), "Competition No", IN(4.226), IN(3.108), IN(0), IN(2.71), color=BLACK, width=12700, arrow="tail"))
    out.append(connector(n(), "Competition Yes H", IN(5.704), IN(2.828), IN(0.803), IN(0), color=BLACK, width=12700))
    out.append(connector(n(), "Competition Yes V", IN(6.507), IN(2.828), IN(0), IN(0.811), color=BLACK, width=12700, arrow="tail"))
    out.append(text_box(n(), "Verdict Chip", IN(6.166), IN(3.208), _W1, _H1, [paragraph([run("Yes", size=PT(9), bold=True, font=FONT)], align="ctr", line_spacing=100000)], fill="D1E8DD", line_color="1B8A57", anchor="ctr", l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144))
    out.append(connector(n(), "Budget Yes H", IN(7.985), IN(3.919), IN(2.733), IN(0), color=BLACK, width=12700))
    out.append(connector(n(), "Budget Yes V", IN(10.718), IN(3.919), IN(0), IN(1.899), color=BLACK, width=12700, arrow="tail"))
    out.append(connector(n(), "Budget No V", IN(6.507), IN(4.199), IN(0), IN(0.811), color=BLACK, width=12700))
    out.append(connector(n(), "Budget No H", IN(6.507), IN(5.01), IN(0.833), IN(0), color=BLACK, width=12700, arrow="tail"))
    for _x, _y, _cx, _cy, _t in _FLOW_NODES2:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(8), italic=True, color=DK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr", l_ins=36576, t_ins=18288, r_ins=36576, b_ins=18288))
    out.append(connector(n(), "Shaping Likely", IN(9.602), IN(5.29), IN(0), IN(0.528), color=BLACK, width=12700, arrow="tail"))
    out.append(text_box(n(), "Verdict Chip", IN(3.876), IN(4.054), _W1, _H1, [paragraph([run("No", size=PT(9), bold=True, font=FONT)], align="ctr", line_spacing=100000)], fill="F2CCCC", line_color="C00000", anchor="ctr", l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144))
    out.append(text_box(n(), "Verdict Chip", IN(9.58), IN(3.794), _W1, _H1, [paragraph([run("Yes", size=PT(9), bold=True, font=FONT)], align="ctr", line_spacing=100000)], fill="D1E8DD", line_color="1B8A57", anchor="ctr", l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144))
    out.append(text_box(n(), "Verdict Chip", IN(6.157), IN(4.499), _W1, _H1, [paragraph([run("No", size=PT(9), bold=True, font=FONT)], align="ctr", line_spacing=100000)], fill="F2CCCC", line_color="C00000", anchor="ctr", l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144))
    out.append(connector(n(), "Shaping Not Likely", IN(7.927), IN(5.29), IN(0), IN(0.528), color=BLACK, width=12700, arrow="tail"))
    out.append(text_box(n(), "Verdict Chip", IN(9.252), IN(5.45), _W1, _H1, [paragraph([run("Likely", size=PT(9), bold=True, font=FONT)], align="ctr", line_spacing=100000)], fill="D1E8DD", line_color="1B8A57", anchor="ctr", l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144))
    out.append(text_box(n(), "Verdict Chip", IN(7.569), IN(5.45), _W1, _H1, [paragraph([run("Not likely", size=PT(9), bold=True, font=FONT)], align="ctr", line_spacing=100000)], fill="F2CCCC", line_color="C00000", anchor="ctr", l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144))
    return "".join(out)


def render() -> str:
    return slide(_body())
