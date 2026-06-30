"""Target slide #13: Capability Domain by Primary Output Map.

D x P heatmap-style matrix using the workbook DDG taxonomy. This is the bridge
between the annual Where-to-Play scorecard and the Priority Supplier Pools slide.
"""
from __future__ import annotations

from deck_core.authoring import Chrome, Sources, body_slide

from ._ddg_slide_utils import (
    BLACK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, Box, DK, GRAY_1,
    GRAY_2, ORANGE, PALE_ORANGE, ShapeIds, WHITE, label, p, paras, shape,
)

LAYOUT = "slideLayout4"
CHARTS: list = []
IMAGES: list = []

CHROME = Chrome(
    section="SAM Supplier Market Structure",
    topic="Capability × Output Map",
    title="Capability Domain by Primary Output Map",
    takeaway="Use the D × P map to translate supplier capability into the physical outputs that can become priority pools.",
    sources=Sources(
        source=(
            "workbook_factory/ddg/sheets/where_to_play.py",
            "workbook_factory/ddg/sheets/domain_concentration.py",
            "workbook_factory/ddg/sheets/kit/taxonomy.py",
        ),
        note="D and P are UEI × Program labels; SWBS remains a separate transaction-level ship-system dimension.",
    ),
)

# Rows are compressed from the published D-axis taxonomy into deck-readable domain groups.
ROWS = [
    ("D1", "Hull / structures", ["", "parts", "", "", "module", "support"]),
    ("D2-D5", "Machinery / power / fluid / thermal", ["inputs", "parts", "equipment", "package", "", "support"]),
    ("D6-D7", "Mission / combat / electronics", ["", "parts", "equipment", "system", "", "technical"]),
    ("D8-D10", "Handling / materials / outfitting", ["inputs", "parts", "equipment", "", "module", "support"]),
    ("D11", "Services / non-material support", ["", "", "", "", "", "services"]),
    ("D0/P0", "Unresolved / attribution-only", ["review", "review", "review", "review", "review", "review"]),
]

COLS = [
    ("P1", "Materials"),
    ("P2", "Parts"),
    ("P3", "Equipment"),
    ("P4", "Systems"),
    ("P5", "Modules"),
    ("P6", "Services"),
]

STYLE = {
    "inputs": (BLUE_1, BLACK),
    "parts": (BLUE_2, BLACK),
    "equipment": (BLUE_3, WHITE),
    "package": (BLUE_4, WHITE),
    "system": (BLUE_4, WHITE),
    "module": (BLUE_5, WHITE),
    "support": (GRAY_1, BLACK),
    "technical": (GRAY_1, BLACK),
    "services": (BLUE_5, WHITE),
    "review": (PALE_ORANGE, BLACK),
    "": (WHITE, GRAY_2),
}


def _body() -> str:
    ids = ShapeIds(100)
    parts: list[str] = []

    parts.append(shape(
        ids, "TopNote", Box(0.50, 1.22, 12.30, 0.38),
        [p("The map separates what a supplier can do (D-axis) from what crosses the supplier boundary (P-axis), so priority pools are not just system names or vendor lists.",
           size=10.4, bold=True, color=WHITE, align="ctr")],
        fill=BLUE_5, line_color="none", anchor="ctr",
    ))

    x0 = 2.55
    y0 = 1.90
    row_label_w = 2.00
    col_w = 1.28
    row_h = 0.49

    parts.append(label(ids, "DomainHeader", Box(0.50, y0, row_label_w, 0.50),
                       "Capability domain", size=8, bold=True,
                       color=WHITE, fill=BLUE_5, line_color=WHITE))
    for c, (code, name) in enumerate(COLS):
        parts.append(shape(
            ids, f"ColHeader{c}", Box(x0 + c * col_w, y0, col_w - 0.03, 0.50),
            [p(code, size=8.4, bold=True, color=WHITE, align="ctr"),
             p(name, size=6.3, color=WHITE, align="ctr")],
            fill=BLUE_4 if c in (2, 3) else BLUE_3,
            line_color=WHITE, anchor="ctr",
        ))

    parts.append(shape(
        ids, "InterpretationRail", Box(10.42, y0, 2.38, 0.50),
        [p("What it says", size=8, bold=True, color=WHITE, align="ctr")],
        fill=BLUE_5, line_color=WHITE, anchor="ctr",
    ))

    rail = [
        "Structural opportunity concentrates in modules / outfitted assemblies.",
        "Equipment lanes cut across machinery, power, fluid and thermal domains.",
        "Mission-electronics pools are most strategic when delivered as configured systems.",
        "Materials, handling and outfitting are broad but need ship-application proof.",
        "Services are a separate non-material handoff, not a residual hardware bucket.",
        "D0/P0 stays in research before making pool claims.",
    ]

    y = y0 + 0.54
    for r, (code, name, cells) in enumerate(ROWS):
        parts.append(shape(
            ids, f"RowHead{r}", Box(0.50, y, row_label_w, row_h),
            [p(code, size=7.8, bold=True, color=BLUE_4, align="ctr"),
             p(name, size=6.5, color=BLACK, align="ctr")],
            fill=BLUE_1 if r % 2 == 0 else GRAY_1,
            line_color=WHITE, anchor="ctr",
        ))
        for c, value in enumerate(cells):
            fill, color = STYLE[value]
            display = value if value else "—"
            parts.append(shape(
                ids, f"MapR{r}C{c}", Box(x0 + c * col_w, y, col_w - 0.03, row_h),
                paras(display, size=6.8, bold=value in {"equipment", "package", "system", "module", "services"},
                      color=color, align="ctr"),
                fill=fill, line_color=ORANGE if value == "review" else WHITE,
                dashed_line=value == "review", anchor="ctr",
            ))
        parts.append(shape(
            ids, f"Rail{r}", Box(10.42, y, 2.38, row_h),
            paras(rail[r], size=6.7, color=BLACK, align="ctr"),
            fill=WHITE if r % 2 == 0 else GRAY_1,
            line_color=WHITE, anchor="ctr",
        ))
        y += row_h + 0.035

    legend = [
        ("Inputs / parts", BLUE_2, BLACK),
        ("Equipment", BLUE_3, WHITE),
        ("Systems / modules", BLUE_5, WHITE),
        ("Services / support", GRAY_1, BLACK),
        ("Research", PALE_ORANGE, BLACK),
    ]
    x = 0.50
    for i, (txt, fill, color) in enumerate(legend):
        parts.append(label(ids, f"Legend{i}", Box(x, 5.55, 1.70, 0.27), txt,
                           size=6.9, bold=True, color=color, fill=fill,
                           line_color=ORANGE if txt == "Research" else WHITE))
        x += 1.80

    parts.append(shape(
        ids, "BottomNote", Box(9.58, 5.40, 3.22, 0.58),
        [p("Next use: promote the large, recurring and strategically relevant D/P cells into the Priority Supplier Pools slide.",
           size=7.3, italic=True, color=DK, align="ctr")],
        fill=WHITE, line_color=ORANGE, dashed_line=True, anchor="ctr",
    ))

    return "".join(parts)


def render() -> str:
    return body_slide(CHROME, _body())
