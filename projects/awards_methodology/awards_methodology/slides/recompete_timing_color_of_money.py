"""recompete_timing_color_of_money — slides new preview deck, source slide 3.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); pattern-fill swatches become
text_box(pattern_fill=…) and freeform <a:custGeom> icons become custom_geometry()
over a deduped path constant; think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=22, connector=3, chart=0, table=0, picture=0, custom_geometry=0, chrome_builders=3, clusters=0 (covering 0 shapes), raw_verbatim=0, dropped=0, frozen_fields=0.

Converter notes:
  - title-like shape off house position - kept verbatim
  - title-like shape off house position - kept verbatim
  - title-like shape off house position - kept verbatim
  - title-like shape off house position - kept verbatim
  - title-like shape off house position - kept verbatim
  - title-like shape off house position - kept verbatim
  - title-like shape off house position - kept verbatim
"""
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, connector,
    breadcrumb, slide_title, preliminary_chip, IN, PT,
)

# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
GRAY_1 = "F2F2F2"
GRAY_2 = "D9D9D9"
GRAY_4 = "7F7F7F"
FONT = "Arial"

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates) ──
_X1 = IN(2.834)   # shared x10
_W1 = IN(5.98)   # shared x8
_Y1 = IN(2.888)   # shared x4
_W2 = IN(0.78)   # shared x4
_H1 = IN(0.2)   # shared x7
_Y2 = IN(3.48)   # shared x4
_H2 = IN(0.355)   # shared x7

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(slide_title("Recompete Timing", "Award type anchors the baseline date, color of money caps how late it can fall, and a handful of variables and signals move it from there."))
    out.append(preliminary_chip())
    out.append(text_box(n(), "Upper Bound Card", IN(0.495), IN(1.676), IN(2.128), IN(1.416), [paragraph([run("Upper Bound", size=PT(12), bold=True, italic=True, underline=True, color=BLACK, font=FONT)], align="ctr", space_after=160, line_spacing=100000), paragraph([], align="ctr", space_after=160, line_spacing=100000), paragraph([run("Color-of-money obligation period", size=PT(10), bold=True, color=DK, font=FONT)], align="ctr", space_after=160, line_spacing=100000), paragraph([run("Latest feasible award that can use a given FY’s money — not period of performance.", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color=BLACK, anchor="ctr", l_ins=18288, t_ins=36576, r_ins=18288, b_ins=36576))
    out.append(text_box(n(), "Color of Money Bar", _X1, IN(1.676), IN(10), IN(0.38), [paragraph([run("SCN", size=PT(10), bold=True, color=WHITE, font=FONT), run("  |  5-year obligation availability", size=PT(10), color=WHITE, font=FONT)], align="l", line_spacing=100000)], fill="007770", line_color=BLACK, line_width=6350, anchor="ctr", l_ins=91440, t_ins=27432, r_ins=91440, b_ins=27432))
    out.append(text_box(n(), "Color of Money Bar", _X1, IN(2.194), IN(6), IN(0.38), [paragraph([run("Procurement", size=PT(10), bold=True, color=WHITE, font=FONT), run("  |  3-year obligation availability", size=PT(10), color=WHITE, font=FONT)], align="l", line_spacing=100000)], fill="447BB2", line_color=BLACK, line_width=6350, anchor="ctr", l_ins=91440, t_ins=27432, r_ins=91440, b_ins=27432))
    out.append(text_box(n(), "Color of Money Bar", IN(2.83), IN(2.712), IN(4), IN(0.38), [paragraph([run("RDT&E", size=PT(10), bold=True, color=WHITE, font=FONT), run("  |  2-year obligation availability", size=PT(10), color=WHITE, font=FONT)], align="l", line_spacing=100000)], fill="7030A0", line_color=BLACK, line_width=6350, anchor="ctr", l_ins=91440, t_ins=27432, r_ins=91440, b_ins=27432))
    out.append(text_box(n(), "Upper Bound Caption", _X1, IN(3.185), _W1, IN(0.15), [paragraph([run("Bar length = how long that year’s money stays obligable; the cap moves only if a later appropriation funds the award.", size=PT(8), italic=True, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Funding Read Card", IN(9.045), IN(2.261), IN(3.789), IN(0.867), [paragraph([run("Funding read", size=PT(10), bold=True, color=BLACK, font=FONT)], space_after=110, line_spacing=100000), paragraph([run("Which color of money funds it, and how much obligation life remains — that sets the latest feasible award.", size=PT(9), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=WHITE, line_color="808080", l_ins=73152, t_ins=36576, r_ins=73152, b_ins=36576))
    out.append(text_box(n(), "Color Money Chip", IN(9.225), _Y1, _W2, _H1, [paragraph([run("O&M", size=PT(8), bold=True, color=WHITE, font=FONT), run(" 1 yr", size=PT(8), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_4, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Color Money Chip", IN(10.075), _Y1, _W2, _H1, [paragraph([run("RDT&E", size=PT(8), bold=True, color=WHITE, font=FONT), run(" 2 yr", size=PT(8), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="7030A0", line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Color Money Chip", IN(10.925), _Y1, _W2, _H1, [paragraph([run("Proc", size=PT(8), bold=True, color=WHITE, font=FONT), run(" 3 yr", size=PT(8), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Color Money Chip", IN(11.775), _Y1, _W2, _H1, [paragraph([run("SCN", size=PT(8), bold=True, color=WHITE, font=FONT), run(" 5 yr", size=PT(8), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="007770", line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Likely Window Output", IN(0.495), _Y2, IN(0.827), IN(2.813), [paragraph([run("Likely Window", size=PT(12), bold=True, italic=True, underline=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="223E59", line_color=BLACK, anchor="ctr", l_ins=27432, t_ins=36576, r_ins=27432, b_ins=36576))
    out.append(text_box(n(), "Lane Spine", IN(1.419), _Y2, IN(1.204), IN(1.131), [paragraph([run("Anchor", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("by award type", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_2, line_color=BLACK, anchor="ctr", l_ins=27432, t_ins=18288, r_ins=27432, b_ins=18288))
    out.append(text_box(n(), "Flow Row", _X1, _Y2, _W1, _H2, [paragraph([run("Standalone definitive contract", size=PT(9), bold=True, color=BLACK, font=FONT), run("  —  ", size=PT(8), color=GRAY_4, font=FONT), run("ultimate completion + options", size=PT(8), italic=True, color=DK, font=FONT)], align="l", line_spacing=100000)], fill=GRAY_1, line_color=BLACK, line_width=6350, anchor="ctr", l_ins=60960, t_ins=18288, r_ins=60960, b_ins=18288))
    out.append(text_box(n(), "Flow Row", _X1, IN(3.868), _W1, _H2, [paragraph([run("Task / delivery order", size=PT(9), bold=True, color=BLACK, font=FONT), run("  —  ", size=PT(8), color=GRAY_4, font=FONT), run("order completion + order options", size=PT(8), italic=True, color=DK, font=FONT)], align="l", line_spacing=100000)], fill=GRAY_1, line_color=BLACK, line_width=6350, anchor="ctr", l_ins=60960, t_ins=18288, r_ins=60960, b_ins=18288))
    out.append(text_box(n(), "Flow Row", _X1, IN(4.256), _W1, _H2, [paragraph([run("Parent IDIQ / MAC / GWAC", size=PT(9), bold=True, color=BLACK, font=FONT), run("  —  ", size=PT(8), color=GRAY_4, font=FONT), run("last date to order + parent options", size=PT(8), italic=True, color=DK, font=FONT)], align="l", line_spacing=100000)], fill=GRAY_1, line_color=BLACK, line_width=6350, anchor="ctr", l_ins=60960, t_ins=18288, r_ins=60960, b_ins=18288))
    out.append(text_box(n(), "Lane Spine", IN(1.419), IN(4.71), IN(1.204), IN(0.743), [paragraph([run("Shifts", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("pull / push", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_2, line_color=BLACK, anchor="ctr", l_ins=27432, t_ins=18288, r_ins=27432, b_ins=18288))
    out.append(text_box(n(), "Flow Row", _X1, IN(4.71), _W1, _H2, [paragraph([run("Pull earlier  ↑", size=PT(9), bold=True, color=BLACK, font=FONT), run("  |  ", size=PT(8), color=GRAY_4, font=FONT), run("award type, value & complexity, full-and-open, incumbency, scope changes", size=PT(8), color=BLACK, font=FONT)], align="l", line_spacing=100000)], fill="1B8A57", line_color="1B8A57", fill_alpha=16000, line_width=9525, anchor="ctr", l_ins=60960, t_ins=18288, r_ins=60960, b_ins=18288))
    out.append(text_box(n(), "Flow Row", _X1, IN(5.098), _W1, _H2, [paragraph([run("Push later  ↓", size=PT(9), bold=True, color=BLACK, font=FONT), run("  |  ", size=PT(8), color=GRAY_4, font=FONT), run("options exercised, bridge / sole-source, protest delay, date drift", size=PT(8), color=BLACK, font=FONT)], align="l", line_spacing=100000)], fill="C00000", line_color="C00000", fill_alpha=16000, line_width=9525, anchor="ctr", l_ins=60960, t_ins=18288, r_ins=60960, b_ins=18288))
    out.append(text_box(n(), "Lane Spine", IN(1.419), IN(5.55), IN(1.204), IN(0.743), [paragraph([run("Signals", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("is it forming?", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_2, line_color=BLACK, anchor="ctr", l_ins=27432, t_ins=18288, r_ins=27432, b_ins=18288))
    out.append(text_box(n(), "Flow Row", _X1, IN(5.55), _W1, _H2, [paragraph([run("Buy is forming", size=PT(9), bold=True, color=BLACK, font=FONT), run("  |  ", size=PT(8), color=GRAY_4, font=FONT), run("FYDP / obligations, forecast, sources-sought, draft RFP", size=PT(8), color=BLACK, font=FONT)], align="l", line_spacing=100000)], fill="1B8A57", line_color="1B8A57", fill_alpha=16000, line_width=9525, anchor="ctr", l_ins=60960, t_ins=18288, r_ins=60960, b_ins=18288))
    out.append(text_box(n(), "Flow Row", _X1, IN(5.938), _W1, _H2, [paragraph([run("Customer intel", size=PT(9), bold=True, color=BLACK, font=FONT), run("  |  ", size=PT(8), color=GRAY_4, font=FONT), run("acquisition authority, operational sponsor, PM signal", size=PT(8), color=BLACK, font=FONT)], align="l", line_spacing=100000)], fill="447BB2", line_color="447BB2", fill_alpha=16000, line_width=9525, anchor="ctr", l_ins=60960, t_ins=18288, r_ins=60960, b_ins=18288))
    out.append(text_box(n(), "Date Misleads Card", IN(9.045), _Y2, IN(3.789), IN(1.95), [paragraph([run("When the date misleads", size=PT(11), bold=True, color=BLACK, font=FONT)], space_after=60, line_spacing=100000), paragraph([], line_spacing=100000), paragraph([run("Options remain: ", size=PT(9), bold=True, color=BLACK, font=FONT), run("may trigger an option, not a recompete", size=PT(9), color=BLACK, font=FONT)], mar_l=142875, indent=-142875, space_after=80, line_spacing=100000, bullet=True), paragraph([run("LDO ≠ performance end: ", size=PT(9), bold=True, color=BLACK, font=FONT), run("an ordering deadline, not a PoP", size=PT(9), color=BLACK, font=FONT)], mar_l=142875, indent=-142875, space_after=80, line_spacing=100000, bullet=True), paragraph([run("Parent / child mismatch: ", size=PT(9), bold=True, color=BLACK, font=FONT), run("child orders can outlast the parent", size=PT(9), color=BLACK, font=FONT)], mar_l=142875, indent=-142875, space_after=80, line_spacing=100000, bullet=True), paragraph([run("Successor early: ", size=PT(9), bold=True, color=BLACK, font=FONT), run("rebuy can land before incumbent LDO", size=PT(9), color=BLACK, font=FONT)], mar_l=142875, indent=-142875, space_after=80, line_spacing=100000, bullet=True), paragraph([run("Retention path: ", size=PT(9), bold=True, color=BLACK, font=FONT), run("bridge or in-scope mod can defer it", size=PT(9), color=BLACK, font=FONT)], mar_l=142875, indent=-142875, line_spacing=100000, bullet=True)], fill="CEDDEC", line_color="223E59", dashed_line=True, l_ins=91440, t_ins=73152, r_ins=91440, b_ins=54864, effects="<a:effectLst><a:outerShdw blurRad=\"50800\" dist=\"38100\" dir=\"2700000\" algn=\"tl\" rotWithShape=\"0\"><a:prstClr val=\"black\"><a:alpha val=\"40000\" /></a:prstClr></a:outerShdw></a:effectLst>"))
    out.append(connector(n(), "Lane Cue", IN(2.63), IN(4.05), _H1, IN(0), color=DK, width=6350, arrow="tail"))
    out.append(connector(n(), "Lane Cue", IN(2.63), IN(5.08), _H1, IN(0), color=DK, width=6350, arrow="tail"))
    out.append(connector(n(), "Lane Cue", IN(2.63), IN(5.92), _H1, IN(0), color=DK, width=6350, arrow="tail"))
    return "".join(out)


def render() -> str:
    return slide(_body())
