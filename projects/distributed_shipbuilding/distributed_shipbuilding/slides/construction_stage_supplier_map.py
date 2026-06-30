"""Target slide #18: Construction-Stage Supplier Map.

Dedicated SAM ship-construction-lens matrix. This should eventually replace the
current work-type approximation with a stage-by-domain view.
"""
from __future__ import annotations

from deck_core.authoring import Chrome, Sources, body_slide

from ._ddg_slide_utils import (
    BLACK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, Box, DK, GRAY_1, GRAY_2,
    ORANGE, PALE_ORANGE, ShapeIds, WHITE, label, p, paras, shape,
)

LAYOUT = "slideLayout4"
CHARTS: list = []
IMAGES: list = []

CHROME = Chrome(
    section="SAM Ship Construction Lens",
    topic="Construction-Stage Supplier Map",
    title="Construction-Stage Supplier Map",
    takeaway="Map observed supplier work to build-stage evidence without forcing sparse rows into a false per-hull cube.",
    sources=Sources(
        source=(
            "workbook_factory/ddg/sheets/ddg_vendor_hull_lifecycle.py",
            "workbook_factory/ddg/sheets/ddg_archetype_lifecycle.py",
            "workbook_factory/ddg/sheets/ddg_cd_lifecycle_rollup.py",
            "workbook_factory/ddg/docs/ddg_sam_model_goals.md",
        ),
        note="A/B rows support exact-hull stage rollups; C/D rows support family-level candidate and lifecycle-confidence views only.",
    ),
)

STAGES = [
    ("Award / source", "Prime/subaward timing"),
    ("Fabricate", "material, parts, modules"),
    ("Equip", "machinery, systems, outfitting"),
    ("Install / integrate", "ship-system application"),
    ("Test / support", "services, trials, logistics"),
    ("Hull timing", "A/B exact; C/D family"),
]

ROWS = [
    ("Structures & modules\nD1 / P5", ["visible", "core", "support", "SWBS 100", "limited", "A/B + C/D"]),
    ("Machinery, power, fluids\nD2-D5 / P3", ["visible", "parts", "core", "SWBS 200/300/500", "test", "stage"]),
    ("Mission / combat / electronics\nD6-D7 / P4", ["visible", "parts", "systems", "SWBS 400/700", "support", "evidence"]),
    ("Materials / processes\nD8-D9 / P1-P2", ["visible", "core", "inputs", "application varies", "limited", "candidate"]),
    ("Interiors / outfitting\nD10 / P2-P5", ["visible", "parts", "outfit", "SWBS 600", "support", "stage"]),
    ("Services / technical work\nD11 / P6", ["visible", "support", "support", "SWBS 800/900", "core", "lifecycle"]),
    ("Unresolved / review\nD0 / P0 / X", ["research", "research", "research", "U00 / L00", "research", "do not allocate"]),
]

STYLE = {
    "core": (BLUE_4, WHITE),
    "systems": (BLUE_4, WHITE),
    "outfit": (BLUE_3, WHITE),
    "inputs": (BLUE_2, BLACK),
    "parts": (BLUE_2, BLACK),
    "visible": (BLUE_1, BLACK),
    "support": (GRAY_1, BLACK),
    "test": (GRAY_1, BLACK),
    "limited": (GRAY_2, BLACK),
    "stage": (BLUE_1, BLACK),
    "evidence": (BLUE_1, BLACK),
    "lifecycle": (BLUE_1, BLACK),
    "candidate": (PALE_ORANGE, BLACK),
    "A/B + C/D": (PALE_ORANGE, BLACK),
    "do not allocate": (PALE_ORANGE, BLACK),
    "research": (WHITE, ORANGE),
    "SWBS 100": (WHITE, BLACK),
    "SWBS 200/300/500": (WHITE, BLACK),
    "SWBS 400/700": (WHITE, BLACK),
    "SWBS 600": (WHITE, BLACK),
    "SWBS 800/900": (WHITE, BLACK),
    "U00 / L00": (WHITE, ORANGE),
    "application varies": (WHITE, BLACK),
}


def _body() -> str:
    ids = ShapeIds(100)
    parts: list[str] = []

    parts.append(shape(
        ids, "TopNote", Box(0.50, 1.23, 12.30, 0.38),
        [p("Construction-stage map: use observed SAM to show where supplier work appears in the build flow, while preserving evidence limits for hull and lifecycle attribution.",
           size=10.5, bold=True, color=WHITE, align="ctr")],
        fill=BLUE_5, line_color="none", anchor="ctr",
    ))

    x0 = 2.20
    y0 = 1.86
    label_w = 1.62
    col_w = 1.67
    row_h = 0.43

    parts.append(label(ids, "RowHeader", Box(0.50, y0, label_w, 0.52),
                       "Supplier pool / domain", size=7.7, bold=True,
                       color=WHITE, fill=BLUE_5, line_color=WHITE))
    for i, (head, sub) in enumerate(STAGES):
        parts.append(shape(
            ids, f"StageHeader{i+1}", Box(x0 + i * col_w, y0, col_w - 0.04, 0.52),
            [p(head, size=7.6, bold=True, color=WHITE, align="ctr"),
             p(sub, size=6.2, color=WHITE, align="ctr")],
            fill=BLUE_4 if i not in (0, 5) else BLUE_5,
            line_color=WHITE, anchor="ctr",
        ))

    y = y0 + 0.56
    for r, (row_name, cells) in enumerate(ROWS):
        row_fill = BLUE_1 if r % 2 == 0 else GRAY_1
        parts.append(shape(ids, f"DomainRow{r}", Box(0.50, y, label_w, row_h),
                           paras(row_name, size=6.7, bold=True, color=BLACK, align="ctr"),
                           fill=row_fill, line_color=WHITE, anchor="ctr"))
        for c, value in enumerate(cells):
            fill, color = STYLE.get(value, (WHITE, BLACK))
            dashed = value in {"research", "do not allocate", "U00 / L00"}
            parts.append(shape(ids, f"MapCell{r}_{c}", Box(x0 + c * col_w, y, col_w - 0.04, row_h),
                               paras(value, size=6.8, bold=value in {"core", "systems"}, color=color, align="ctr"),
                               fill=fill, line_color=ORANGE if dashed else WHITE,
                               dashed_line=dashed, anchor="ctr"))
        y += row_h + 0.03

    legend_items = [
        ("Core observed stage", BLUE_4, WHITE),
        ("Visible / supporting evidence", BLUE_1, BLACK),
        ("Candidate or family-level timing", PALE_ORANGE, BLACK),
        ("Research / unresolved", WHITE, ORANGE),
    ]
    for i, (txt, fill, color) in enumerate(legend_items):
        parts.append(label(ids, f"Legend{i}", Box(0.50 + i * 2.37, 5.28, 2.18, 0.28),
                           txt, size=7, bold=True, color=color, fill=fill,
                           line_color=ORANGE if color == ORANGE else WHITE))

    parts.append(shape(
        ids, "Interpretation", Box(10.10, 4.82, 2.70, 0.72),
        [p("How to read", size=8, bold=True, color=BLUE_4),
         p("The matrix is directional until dollar values are rendered from the lifecycle rollups. Keep A/B exact-hull and C/D family-level views separate.",
           size=7.2, color=BLACK)],
        fill=GRAY_1, line_color="none",
    ))

    parts.append(shape(
        ids, "BottomBoundary", Box(0.50, 5.77, 12.30, 0.32),
        [p("Boundary: do not split C/D candidate-family dollars across hulls inside the evidence model; use them for narrowing and lifecycle-confidence readouts only.",
           size=7.6, italic=True, color=DK, align="ctr")],
        fill=PALE_ORANGE, line_color="none", anchor="ctr",
    ))
    return "".join(parts)


def render() -> str:
    return body_slide(CHROME, _body())
