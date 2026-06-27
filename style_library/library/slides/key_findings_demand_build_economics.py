"""key_findings_demand_build_economics — Commercial Strategy Market Analysis deck (20260325), source slide 8.

EXHIBIT — "Key Findings (1/3)": a text-only executive summary of the demand /
build-cost / vessel-economics workstream, subtitled "Demand, build cost, and
vessel economics." The whole slide is essentially ONE native table — a single
full-width cell of richly-formatted, multi-level bullets — organised around four
bold-italic teal (1D4D68) framing questions:
  1. addressable demand for US-built ships (four scenarios — Jones Act status quo,
     SHIPS Act as written, SHIPS Act "Plus", SHIPS Act "Plus" + Heritage fleet),
  2. what that demand implies for Port Alpha's orderbook (~5% / ~45% / ~95% / ~230%
     of Phase 2 capacity by scenario, with indented sub-bullets and NOTE caveats),
  3. US newbuild prices vs. major international shipbuilders (~1.4-2.2x above Asian
     yards, down from ~4-6x today), and
  4. US-flagged vs. foreign-flagged vessel economics under industrial policy and
     automation (~$10M opex/D&A gap after subsidies and ITCs).
A single footnote box closes it out.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ......... breadcrumb() + title_placeholder() + prelim_chip()
  • findings table . the one table() — a single 12.3in column / single rich cell
                     ("Table 13"); the four framing questions are tcell_rich()
                     paragraphs (tpara/trun), bullet levels carry the sub-points
  • footnote ....... "Rectangle 4" Note line (SHIPS Act modifications cross-ref)

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=1, table=1, chrome_builders=3, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim.
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
    out.append(title_placeholder("Key Findings (1/3)", "Demand, build cost, and vessel economics."))
    out.append(prelim_chip())
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    # palette — text: 1D4D68 teal-blue (framing questions) · 000000 black (body bullets) · 162029 dark navy (Phase 2+) · FF0000 red (accents);
    #   rules: none; cell fills: none.
    out.append(table(n(), "Table 13", IN(0.495), IN(1.066), IN(12.3), IN(5.9), col_widths=[IN(12.3)], rows=[
        trow([tcell_rich([tpara([r("What is the addressable demand for US-built ships?", b=1, i=1, u=1, color="1D4D68"), r(" ", i=1), r("We evaluated four scenarios for oceangoing commercial ships assuming Port Alpha buildout to Phase 5: (1) Jones Act status quo, (2) SHIPS Act as written, (3) SHIPS Act “Plus” with key bill revisions and expansion of existing programs, and (4) SHIPS Act “Plus” with Heritage Foundation target fleet; "), r("these scenarios suggest path to Port Alpha Phase", b=1), r(" ", b=1, color="FF0000"), r("2+", b=1, color=DK), r(" ", b=1, color="FF0000"), r("requires additional demand signals", b=1)], bullet=True, bullet_char="auto", mar_l=227013, indent=-227013, space_before=0, space_after=600),
            tpara([r("What does demand imply for Port Alpha’s orderbook?", b=1, i=1, u=1, color="1D4D68"), r(" ", i=1), r("’28-’38 demand as percentage of Port Alpha Phase 2 capacity "), r("(25 deliveries / year; containerships and tankers) ", i=1), r("by scenario:")], bullet=True, bullet_char="auto", mar_l=227013, indent=-227013, space_before=0, space_after=600),
            tpara([r("(1) Status Quo accounts for an avg. of ~5% of capacity; ", b=1), r("outlook contingent upon Jones Act fleet recapitalization")], bullet=True, level=1, mar_l=342900, indent=-117475, space_before=0, space_after=600),
            tpara([r("(2) SHIPS Act as written accounts for ~45%;", b=1), r(" ", b=1), r("requires passage of both SHIPS Act and Building Ships in America Act")], bullet=True, level=1, mar_l=342900, indent=-117475, space_before=0, space_after=600),
            tpara([r("(3) SHIPS Act “Plus”", b=1), r("1", b=1), r(" accounts for ~95%, ", b=1), r("with demand"), r(" ", b=1), r("declining by the mid-’30s and remaining low through ‘50; requires "), r("USG to subsidize full opex and D&A differential ", b=1), r("vs. foreign ships, supported by "), r("universal cargo fees ", b=1), r("($0.01+ per kg imported by foreign-built ships) and other revisions to pending legislation ")], bullet=True, level=1, mar_l=342900, indent=-117475, space_before=0, space_after=600),
            tpara([r("NOTE:", b=1, i=1, u=1), r(" Headwinds are currently impacting the legislative path for the SHIPS Act", b=1, i=1)], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=0, space_after=600),
            tpara([r("(4) SHIPS Act “Plus” with Heritage accounts for ~230%", b=1), r(", with demand declining by the early ‘40s and remaining low through 50; "), r("requires "), r("universal cargo fees of $0.07+ ", b=1), r("per kg by 2050 and Maritime Security Trust Fund balance cap increase ")], bullet=True, level=1, mar_l=342900, indent=-117475, space_before=0, space_after=600),
            tpara([r("NOTE:", b=1, i=1, u=1), r(" Pending legislation supports <20% of Heritage Foundation’s target fleet; funding required likely challenges demand materialization", b=1, i=1)], bullet=True, bullet_char="−", level=2, mar_l=457200, indent=-114300, space_before=0, space_after=600),
            tpara([r("What are the impacts on US newbuild prices vs. those of major international shipbuilders?", b=1, i=1, u=1, color="1D4D68"), r(" "), r("With yard automation, SHIPS Act demand, and vessel investment tax credits, expected "), r("Port Alpha newbuild prices remain ~1.4-2.2x above ", b=1), r("those of Asian shipyards, down from ~4-6x today")], bullet=True, bullet_char="auto", mar_l=227013, indent=-227013, space_before=0, space_after=600),
            tpara([r("Government capital subsidies required ", b=1), r("to achieve prices below Asian yards in the "), r("absence of vessel ITCs ", b=1), r("(US-flag & foreign trade required for ITC eligibility)")], bullet=True, level=1, mar_l=342900, indent=-114300, space_before=0, space_after=600),
            tpara([r("Labor hour reduction and volume discounts primarily drive build price reductions", b=1), r("; shipyard ITCs may reduce prices by ~0-1% given capex scale and D&A mechanics; however, Shipyard ITCs meaningfully de-risk yard capacity expansion "), r("(discussed on subsequent page)", i=1)], bullet=True, level=1, mar_l=342900, indent=-114300, space_before=0, space_after=600),
            tpara([r("How do US-flagged vessel economics compare to foreign-flagged today? How do industrial policy and automation change the gap?", b=1, i=1, u=1, color="1D4D68"), r(" ", i=1), r("(2) SHIPS "), r("Act as written unlikely to make US-built, US-flagged vessels attractive enough to realize full potential of SCF given estimated "), r("US opex and D&A gap vs. foreign of ~$10M after subsidies and ITCs; (3) SHIPS Act “Plus” may result in US-built and flagged vessels being cheaper to own and operate")], bullet=True, bullet_char="auto", mar_l=227013, indent=-227013, space_before=0, space_after=600),
            tpara([r("With automation, "), r("US-flagged opex likely "), r("remains more expensive than foreign-flagged ", b=1), r("given new autonomy-related expenses offsetting reduction in other opex categories"), r("; ", b=1), r("Saronic may see lower opex than other Jones Act players when operating autonomous vessels, with cost advantage driven by vertical integration as ComboCo ")], bullet=True, level=1, mar_l=339725, indent=-112713, space_before=0, space_after=600)], l_ins=41564, r_ins=41564, borders={"L": "none", "R": "none", "T": "none", "B": "none"})], h=IN(0)),
    ]))
    out.append(text_box(n(), "Rectangle 4", IN(0.495), IN(7.002), IN(4.679), IN(0.3), [paragraph([run("Note: (1) Refer to pg. 12 for full description of modifications to SHIPS Act and other relevant USG programs", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    return "".join(out)


def render() -> str:
    return slide(_body())
