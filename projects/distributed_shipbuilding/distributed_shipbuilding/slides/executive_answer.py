"""Target slide #3: Executive Answer.

KPI-card opener adapted from style_library/library/slides/fleet_overview.py.
The slide uses the DDG workbook's Executive Summary / Market Bridge / Where to
Play framing as data-backed content, but keeps hard dollar values out until the
rendered workbook values are pulled directly into charts.
"""
from __future__ import annotations

from deck_core.authoring import Chrome, Sources, body_slide

from ._ddg_slide_utils import (
    BLACK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, Box, DK, GRAY_1,
    ORANGE, ShapeIds, WHITE, arrow, card, metric_chip, p, paras, shape,
)

LAYOUT = "slideLayout4"
CHARTS: list = []
IMAGES: list = []

CHROME = Chrome(
    section="Market Answer and Scope",
    topic="Executive Answer",
    title="Executive Answer",
    takeaway="Read DDG-51 as a TAM-sized outsourced opportunity plus an observed first-tier SAM evidence layer.",
    sources=Sources(
        source=(
            "workbook_factory/ddg/sheets/executive_summary.py",
            "workbook_factory/ddg/sheets/market_bridge.py",
            "workbook_factory/ddg/sheets/where_to_play.py",
        ),
        note="Observed SAM is reported first-tier subaward evidence, not the full outsourced-market total.",
    ),
)


def _body() -> str:
    ids = ShapeIds(100)
    parts: list[str] = []

    parts.append(shape(
        ids, "AnswerBand", Box(0.50, 1.30, 12.30, 0.56),
        [p("DDG-51 new-construction supplier opportunity should be sized top-down, then interpreted bottom-up through reported supplier evidence.",
           size=14, bold=True, color=WHITE, align="ctr")],
        fill=BLUE_5, line_color="none", anchor="ctr",
    ))

    cards = [
        ("TAM denominator", "BC + AP/LLTM + OBBBA", "The DDG TAM tab sizes supplier-addressable outsourced new-construction spend by fiscal year."),
        ("Observed SAM", "First-tier subawards", "Reported subawards reveal supplier structure and timing; they do not equal total outsourced market spend."),
        ("Where to play", "D / P archetype pools", "Capability-domain and primary-output screens compare size, growth, concentration, incumbency and entry signals."),
        ("Construction lens", "SWBS / hull / lifecycle", "Ship-system, hull and lifecycle cuts are evidence-limited and should stay separate from entity archetypes."),
    ]
    x0 = 0.50
    for i, (kicker, headline, body) in enumerate(cards):
        fill = [WHITE, BLUE_1, WHITE, BLUE_1][i]
        parts.append(card(ids, f"KpiCard{i+1}", Box(x0 + i * 3.13, 2.02, 2.86, 1.33),
                          kicker, headline, body, fill=fill,
                          accent=[BLUE_4, BLUE_4, BLUE_3, BLUE_3][i], headline_size=14))

    findings = [
        ("1", "Scope discipline", "TAM is the addressable denominator. Observed SAM is the evidence layer used for structure, coverage and timing."),
        ("2", "Supplier answer", "Prioritize pools that are large or growing, strategically important, not fully locked by parent control, and visible in recurring subawards."),
        ("3", "Evidence boundary", "SWBS is HII-only today; exact-hull A/B rows support hull-stage rollups; C/D rows stay family-level without per-hull allocation."),
    ]
    for i, (num, title, body) in enumerate(findings):
        y = 3.68 + i * 0.72
        parts.append(metric_chip(ids, f"FindingNum{i+1}", Box(0.50, y, 0.58, 0.52), num, "finding",
                                 fill=[BLUE_1, BLUE_2, BLUE_3][i], accent=BLUE_5))
        parts.append(shape(
            ids, f"FindingText{i+1}", Box(1.18, y, 7.02, 0.52),
            [p(title, size=10.5, bold=True, color=BLACK), p(body, size=8.5, color=BLACK)],
            fill=GRAY_1, line_color="none", anchor="ctr",
        ))

    parts.append(shape(
        ids, "RightRailTitle", Box(8.55, 3.67, 4.24, 0.28),
        [p("How the story should read", size=10, bold=True, color=WHITE, align="ctr")],
        fill=BLUE_4, line_color="none", anchor="ctr",
    ))
    spine = [
        ("Scope", "Define DDG-51 new construction and denominator hierarchy"),
        ("TAM", "Build outsourced opportunity from construction spend streams"),
        ("SAM", "Use subawards to observe pool structure and timing"),
        ("Lens", "Map visible work to systems, hulls and lifecycle stages"),
    ]
    for i, (head, desc) in enumerate(spine):
        x = 8.55 + i * 1.08
        parts.append(shape(ids, f"SpineHead{i+1}", Box(x, 4.10, 0.90, 0.38),
                           [p(head, size=8.5, bold=True, color=WHITE, align="ctr")],
                           fill=BLUE_5 if i < 2 else BLUE_3, line_color="none", anchor="ctr"))
        parts.append(shape(ids, f"SpineDesc{i+1}", Box(x, 4.52, 0.90, 0.91),
                           paras(desc, size=7.3, color=BLACK, align="ctr"),
                           fill=WHITE, line_color=BLUE_2, anchor="ctr"))
        if i < 3:
            parts.append(arrow(ids, f"SpineArrow{i+1}", x + 0.92, 4.31, 0.24,
                               color=ORANGE, width=15_875))

    parts.append(shape(
        ids, "BottomCaveat", Box(0.50, 5.58, 12.30, 0.36),
        [p("Working convention for the new slides: use TAM for market size; use observed SAM for where-to-play, concentration, supplier continuity and traceability. Do not label observed SAM/TAM as penetration.",
           size=8.3, italic=True, color=DK, align="ctr")],
        fill=BLUE_1, line_color="none", anchor="ctr",
    ))
    return "".join(parts)


def render() -> str:
    return body_slide(CHROME, _body())
