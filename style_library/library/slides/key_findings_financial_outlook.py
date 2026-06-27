"""key_findings_financial_outlook — Commercial Strategy Market Analysis deck (20260325), source slide 9.

EXHIBIT — "Key Findings (2/3)": a text-heavy "ComboCo financial outlook" slide that
answers, in prose, "What do these findings imply for ComboCo financials?". The body
is a single full-width native table cell holding a deep bulleted hierarchy — top-line
modelling assumptions (2026–2038 projections), then three nested segment blocks:
BuildCo (Port Alpha build-out to $3.5B CAPEX, 44%→~40% gross margins), OpCo (Saronic
as owner/operator buying 25 container ships for $4.2B), and ComboCo (combined
financing $2.8B OSC loan / $500M revolver / $2.25B equity, 12–14% EBIT, ~$2.5B
negative FCF NPV). A dashed light-blue callout (lower right) lists the two
contingencies the results depend on (proposed legislation/subsidies and Port Alpha
automation).

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............... breadcrumb() + title_placeholder() + prelim_chip()
  • findings table ....... "Table 8" = one full-width single-cell table whose cell is
                           the entire findings narrative (tcell_rich/tpara/trun; the
                           bullet hierarchy is carried by per-paragraph level/indent)
  • contingencies callout  "Rectangle 10" = dashed light-blue "Results detailed
                           contingent on:" box with two bullets

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=1, table=1, chrome_builders=3, dropped=1 (think-cell OLE frame).
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.authoring import (
    slide, run, paragraph, text_box, table, trow, tcell, tcell_rich, tpara, trun,
    breadcrumb, title_placeholder, prelim_chip, IN, PT, BLACK, DK, FONT,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── run kit (local): r() = one rich-text run with this slide's PT12 Arial defaults, so the
#    bullet prose reads without per-run size/color/font noise. Renders identically to trun(). ──
def r(text, *, b=False, i=False, u=False, color=BLACK, size=PT(12)):
    return trun(text, size=size, bold=b or None, italic=i or None, underline=u or None, color=color, font=FONT)


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(breadcrumb("Commercial Strategy", "Research Overview"))
    out.append(title_placeholder("Key Findings (2/3)", "ComboCo financial outlook."))
    out.append(prelim_chip())
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    # palette — text: 1D4D68 teal-blue (framing question) · 000000 black (body bullets);
    #   rules: none; cell fills: none.
    out.append(table(n(), "Table 8", IN(0.495), IN(1.066), IN(12.3), IN(5.95), col_widths=[IN(12.3)], rows=[
        trow([tcell_rich([tpara([r("What do these findings imply for ComboCo financials?", b=1, i=1, u=1, color="1D4D68"), r(" ", i=1), r("Projections were created from 2026-2038 ", b=1), r("after alignment with "), r("Finance and Port Alpha teams on starting assumptions (i.e., initial sale price, labor hours, CAPEX, vessel profiles)")], bullet=True, bullet_char="auto", mar_l=228600, indent=-228600, space_before=300, space_after=300),
            tpara([r("BuildCo (i.e., Saronic):", b=1, u=1), r(" ", b=1), r("Port Alpha build-out modeled to Phase 2 for $3.5B total CAPEX")], bullet=True, level=1, mar_l=342900, indent=-114300, space_before=300, space_after=300),
            tpara([r("Two ships were modelled ", b=1), r("– a Panamax containership and an Aframax / Suezmax Tanker; a"), r("ssumes"), r(" 182 containerships and 39 tankers ", b=1), r("are delivered during this period; n"), r("umber of deliveries were based off ("), r("i"), r(") SHIPS Act “Plus” and (ii) Port Alpha capacity (25 deliveries / year)")], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300),
            tpara([r("Gross Margins set at 44% in 2028, declining to ~40% by 2038", b=1), r(" given increased domestic competition; overall domestic prices supported by USG subsidies for vessel owners")], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300),
            tpara([r("EBIT margins vary, largely staying within 5-10% range in 2032+", b=1)], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300),
            tpara([r("Shipyard ITCs soften impact of capex on FCF in early years, while also reducing outside capital needs")], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300),
            tpara([r("OpCo (Saronic as owner/operator):", b=1, u=1), r(" ", b=1), r("P"), r("urchases "), r("25 total container ships for $4.2B ", b=1), r("in ‘33 and ‘34 that enter service the following year in the Strategic Commercial Fleet, operating on US Atlantic / Gulf Coast <> Europe / S. America routes "), r("(to consider Jones Act Marine Highway / OCONUS in future efforts)", i=1)], bullet=True, level=1, mar_l=342900, indent=-114300, space_before=300, space_after=300),
            tpara([r("Service starts in 2034, which softens cash outlay frequency; ", b=1), r("earlier service start would require more equity financing and prevents potentially antagonistic messaging of immediate competition with BuildCo customers ")], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300),
            tpara([r("BuildCo sells vessels to OpCo under favorable pricing (10% gross margin)", b=1)], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300),
            tpara([r("EBIT margins (inclusive of operating and capital subsidies) of ~25%")], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300),
            tpara([r("ComboCo (BuildCo + OpCo)", b=1, u=1)], bullet=True, level=1, mar_l=342900, indent=-114300, space_before=300, space_after=300),
            tpara([r("Financing: ", b=1), r("$2.8B OSC Loan / $500M Revolver / $2.25B in Equity + $500M in Cash; assumes only BuildCo qualifies for shipyard ITCs ")], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300),
            tpara([r("EBIT Margin reach 12-14% ", b=1), r("in the 2030s, in between traditional shipbuilders (~4-6%) and ship owners (15-20%)")], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300),
            tpara([r("Consistent Cash Flow positive in 2034 onwards ", b=1), r("after conclusion of BuildCo capex and OpCo vessel procurement")], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300),
            tpara([r("FCF NPV of (~$2.5B); primarily driven by frontloaded CAPEX timing, intersegment transfers, and absence of vessel ITCs ", b=1), r("(given current bill language)", i=1)], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300),
            tpara([r("Preliminary analysis suggests key determinants of Saronic’s commercial market success include pursuing new business models enabled by autonomy (i.e., marine highway), competing in Jones Act, developing incremental revenue streams (e.g., selling marine / cargo data), and ensuring ComboCo vessel ITC eligibility")], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=300, space_after=300)], l_ins=41564, r_ins=41564, borders={"L": "none", "R": "none", "T": "none", "B": "none"})], h=IN(0)),
    ]))
    out.append(text_box(n(), "Rectangle 10", IN(7.936), IN(4.204), IN(4.685), IN(0.913), [paragraph([run("Results detailed contingent on:", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("Implementation of proposed legislation, subsidies, tax credits & additional future policy action", size=PT(12), color=BLACK, font=FONT)], mar_l=285750, indent=-285750, line_spacing=100000, bullet=True), paragraph([run("High degree of automation and efficiency at Port Alpha", size=PT(12), color=BLACK, font=FONT)], mar_l=285750, indent=-285750, line_spacing=100000, bullet=True)], fill="CEDDEC", line_color=DK, dashed_line=True, anchor="ctr", effects="<a:effectLst><a:outerShdw blurRad=\"50800\" dist=\"38100\" dir=\"2700000\" algn=\"tl\" rotWithShape=\"0\"><a:prstClr val=\"black\"><a:alpha val=\"40000\" /></a:prstClr></a:outerShdw></a:effectLst>"))   # CEDDEC pale blue
    return "".join(out)


def render() -> str:
    return slide(_body())
