"""Target slide #12: SAM Where-to-Play Scorecard.

Full-width strategic matrix drawing from workbook_factory/ddg/sheets/where_to_play.py.
"""
from __future__ import annotations

from deck_core.authoring import Chrome, Sources, body_slide

from ._ddg_slide_utils import (
    BLACK, BLUE_1, BLUE_2, BLUE_4, BLUE_5, Box, DK, GRAY_1, GRAY_2,
    ORANGE, ShapeIds, WHITE, label, p, paras, shape,
)

LAYOUT = "slideLayout4"
CHARTS: list = []
IMAGES: list = []

CHROME = Chrome(
    section="SAM Supplier Market Structure",
    topic="Where-to-Play Scorecard",
    title="SAM Where-to-Play Scorecard",
    takeaway="Use annual D/P archetype screens to separate attractive supplier pools from merely visible spend.",
    sources=Sources(
        source=(
            "workbook_factory/ddg/sheets/where_to_play.py",
            "workbook_factory/ddg/sheets/domain_concentration.py",
            "workbook_factory/ddg/sheets/kit/taxonomy.py",
        ),
        note="Scorecard is an observed-SAM screen; it is not proof of full-market contestability.",
    ),
)

COLORS = {
    "primary": BLUE_4,
    "support": BLUE_2,
    "watch": "FFF2CC",
    "boundary": GRAY_2,
}


def _cell(ids: ShapeIds, name: str, box: Box, text: str, *, fill: str,
          color: str = BLACK, bold: bool = False, size: float = 7.7):
    return shape(ids, name, box, paras(text, size=size, bold=bold, color=color, align="ctr"),
                 fill=fill, line_color=WHITE, anchor="ctr")


def _body() -> str:
    ids = ShapeIds(100)
    parts: list[str] = []

    parts.append(shape(
        ids, "TopFrame", Box(0.50, 1.24, 12.30, 0.42),
        [p("Primary SAM answer: rank supplier pools by size, momentum, control, continuity and entry signals at one consistent annual grain.",
           size=12.5, bold=True, color=WHITE, align="ctr")],
        fill=BLUE_5, line_color="none", anchor="ctr",
    ))

    x0 = 0.50
    y0 = 1.88
    row_h = 0.43
    col_w = [1.75, 1.44, 1.42, 1.42, 1.42, 1.42, 1.42, 1.61]
    headers = [
        "Question", "Size", "Momentum", "Supplier breadth", "Parent control",
        "Incumbency", "Entry signal", "Scorecard readout",
    ]
    x = x0
    for i, (h, w) in enumerate(zip(headers, col_w)):
        fill = BLUE_4 if i else BLUE_5
        parts.append(label(ids, f"Header{i}", Box(x, y0, w, 0.42), h,
                           size=8, bold=True, color=WHITE, fill=fill, line_color=WHITE))
        x += w

    rows = [
        (
            "Where is spend visible?",
            "Net Subaward $M",
            "YoY $ Growth",
            "Active Suppliers",
            "Parent Top-1 / HHI",
            "Incumbent $ %",
            "First-observed / Reactivated $ %",
            "Large / growing pools with non-fortress structure rise to the top.",
            "primary",
        ),
        (
            "Which capability domains matter?",
            "D-axis program share",
            "FY2022-25 trend",
            "D-axis active UEIs",
            "Parent effective firms",
            "Retention %",
            "New or reactivated dollars",
            "Capability-domain pools identify technical areas to prioritize.",
            "primary",
        ),
        (
            "Which outputs are buyable?",
            "P-axis spend",
            "P-axis growth",
            "Output supplier count",
            "Parent concentration",
            "Incumbent vendors %",
            "First-observed suppliers",
            "Primary-output pools show the physical form of the supplier opportunity.",
            "support",
        ),
        (
            "Where is control tight?",
            "Large spend alone is not enough",
            "Growth can be captive",
            "Low supplier count flag",
            "High HHI / Top-1 flag",
            "High incumbent $ flag",
            "Low entry flag",
            "Treat fortress pools as partner / acquisition / long-cycle lanes, not quick-entry whitespace.",
            "watch",
        ),
        (
            "What still needs evidence?",
            "D0 / P0 unresolved",
            "Sparse FY series",
            "Small-N suppliers",
            "Parent mapping gaps",
            "One-off continuity",
            "Ambiguous first-observed rows",
            "Send weak cells to research queue before making priority-pool claims.",
            "boundary",
        ),
    ]

    y = y0 + 0.46
    for r, row in enumerate(rows):
        kind = row[-1]
        fills = [WHITE] + [COLORS[kind] if kind in ("primary", "support") else COLORS[kind]] * 7
        x = x0
        for c, (txt, w) in enumerate(zip(row[:-1], col_w)):
            if c == 0:
                fill = BLUE_1 if r % 2 == 0 else GRAY_1
                color = BLACK
                bold = True
            elif c == 7:
                fill = WHITE if kind != "boundary" else GRAY_1
                color = BLACK
                bold = False
            else:
                fill = fills[c]
                color = WHITE if kind in ("primary", "support") else BLACK
                bold = False
            parts.append(_cell(ids, f"R{r}C{c}", Box(x, y, w, row_h), txt,
                               fill=fill, color=color, bold=bold,
                               size=7.2 if c not in (0, 7) else 7.6))
            x += w
        y += row_h + 0.03

    parts.append(shape(
        ids, "TaxonomyStrip", Box(0.50, 4.68, 6.02, 0.92),
        [
            p("Classification grain", size=8, bold=True, color=BLUE_4),
            p("D = capability domain supported by the supplier. P = primary delivered form and integration level. Both are assigned at UEI × Program grain, not transaction grain.",
              size=8, color=BLACK),
        ],
        fill=BLUE_1, line_color="none",
    ))
    parts.append(shape(
        ids, "DecisionStrip", Box(6.78, 4.68, 6.02, 0.92),
        [
            p("Decision rule", size=8, bold=True, color=BLUE_4),
            p("Priority pools should combine attractive observed spend with a contestability signal and a clear construction relevance story. A large but highly concentrated pool may still be strategic, but the route differs.",
              size=8, color=BLACK),
        ],
        fill=GRAY_1, line_color="none",
    ))

    legend = [
        ("Primary sizing signal", BLUE_4, WHITE),
        ("Supporting screen", BLUE_2, WHITE),
        ("Contestability watchout", "FFF2CC", BLACK),
        ("Evidence boundary", GRAY_2, BLACK),
    ]
    x = 0.50
    for i, (txt, fill, color) in enumerate(legend):
        parts.append(label(ids, f"Legend{i}", Box(x, 5.78, 2.15, 0.26), txt,
                           size=7.2, bold=True, color=color, fill=fill, line_color=WHITE))
        x += 2.25

    parts.append(shape(
        ids, "BottomNote", Box(9.78, 5.73, 3.02, 0.37),
        [p("Next module can promote the highest-scoring D/P cells into Priority Supplier Pools.",
           size=7.5, italic=True, color=DK, align="ctr")],
        fill=WHITE, line_color=ORANGE, dashed_line=True, anchor="ctr",
    ))
    return "".join(parts)


def render() -> str:
    return body_slide(CHROME, _body())
