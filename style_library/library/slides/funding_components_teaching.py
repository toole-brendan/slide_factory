"""Teaching exemplar: Navy funding-components addressability matrix.

ROLE
  funding_scope_matrix / addressability_legend_grid

USE WHEN
  A slide needs to show which mission areas, budget sources, and colors of money
  are in scope for a market-sizing model.

TEACHES
  - matrix cells whose fill encodes addressability, not row grouping
  - rotated row-spine labels for compact group names
  - top-right addressability legend with four visual states
  - funding-type headers that sit above the mission grid
  - dashed structural rules separating Funding Inputs, Budget Data Sources, and
    Color of Money rows
  - a source/footnote row that is intentionally off the house Source position

TEXT-FIT PRECEDENT
  mission_cells:
    geometry: mostly 1.213in wide x 0.333in high
    type: Arial 9pt, centered, 100% line spacing
    content: short mission labels plus inline numeric footnote markers
    copy_when: a dense matrix needs each cell to stay legible at one-line height

  row_spines:
    geometry: 1.2-2.147in wide x 0.562-0.563in high, rotated -90 degrees
    type: Arial 11pt, centered
    content: one row-group label
    copy_when: row groups are important but cannot consume a full left column

SOURCE NOTE
  Teaching rewrite of source-faithful `funding_components.py`. The original kept
  converter buckets that mixed row bands, mission cells, and role cells because
  they shared style. This version makes the semantic split explicit: row bands,
  mission cells, funding headers, role cells, legend entries, structure rules,
  callout, and logo.

FIDELITY NOTE
  Coordinates, text, footnote markers, fills, lines, logo rId, and structural
  rules are preserved. The render order is simplified into conceptual matrix
  layers for teaching readability.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, connector, line_break, paragraph, picture, run, text_box,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
GRAY_1 = "F2F2F2"
GRAY_3 = "BFBFBF"
FONT = "Arial"

LAYOUT = "slideLayout4"

CHARTS: list = []
IMAGES = [
    {"rId": "rId2", "file": "image8_3071a231.jpeg"},
]

BLUE_HEADER = "447BB2"
PALE_BLUE = "99B9D8"
DARK_NAVY = "0E1924"
ANOTHER_CAMPAIGN = "A6A6A6"
RULE_BLUE = "88AABD"


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float


@dataclass(frozen=True)
class TextFitZone:
    name: str
    box: Box
    fit: str
    copy_when: str


@dataclass(frozen=True)
class MatrixBox:
    role: str
    text: str
    box: Box
    fill: str | None
    line: str | None
    text_color: str = BLACK
    size: int = PT(9)
    footnote: str | None = None
    line2: str | None = None
    line2_italic: bool = False
    italic: bool = False
    bold: bool = False
    rot: int = 0
    anchor: str = "ctr"
    line_width: int = 3175


@dataclass(frozen=True)
class LegendEntry:
    label: str
    key_box: Box
    label_box: Box
    fill: str | None
    line: str | None


@dataclass(frozen=True)
class ConnectorSpec:
    name: str
    box: Box
    color: str
    width: int
    dashed: bool = False
    flip_h: bool = False
    flip_v: bool = False


TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("mission_cells", Box(0.902, 2.323, 11.911, 1.632), "Arial 9pt centered in 0.333in-high cells", "copy for very dense addressability matrices"),
    TextFitZone("funding_headers", Box(0.604, 1.889, 12.229, 0.333), "Arial 11pt centered; one header wraps to two lines", "copy for grouped column headers over a matrix"),
    TextFitZone("footnote_row", Box(0.495, 6.642, 12.367, 0.354), "Arial 10pt, one long note line", "copy when a matrix needs footnote markers but no full source rail"),
)

COPY_RULES: tuple[str, ...] = (
    "Make cell fill mean addressability; do not use fill merely as decoration.",
    "Keep mission-cell labels short; long methodology belongs in a supporting slide.",
    "Use rotated row spines only when they replace repeated row labels.",
    "Keep the legend physically close to the grid so colors can be decoded before reading cells.",
)

ROW_BANDS: tuple[MatrixBox, ...] = (
    MatrixBox("budget_source", "FY26 PBR & Congressional Committee markups", Box(0.604, 4.093, 12.229, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("budget_source", "OBBBA & Congressional Committee intent", Box(0.604, 4.528, 12.229, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("budget_source", "SHIELD IDIQ", Box(9.599, 4.963, 3.222, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("color_of_money", "Procurement", Box(0.604, 5.399, 12.229, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("color_of_money", "RDT&E", Box(0.604, 5.834, 12.229, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("color_of_money", "O&M", Box(0.604, 6.269, 12.229, 0.333), GRAY_1, GRAY_1, BLACK),
)

SPINE_LABELS: tuple[MatrixBox, ...] = (
    MatrixBox("row_spine", "Funding Inputs", Box(-0.781, 2.659, 2.147, 0.563), None, "none", BLACK, size=PT(11), rot=16200000),
    MatrixBox("row_spine", "Budget Data Sources", Box(-0.308, 4.412, 1.200, 0.562), None, "none", BLACK, size=PT(11), rot=16200000),
    MatrixBox("row_spine", "Color of Money", Box(-0.308, 5.714, 1.200, 0.562), None, "none", BLACK, size=PT(11), rot=16200000),
)

FUNDING_HEADERS: tuple[MatrixBox, ...] = (
    MatrixBox("funding_header", "Unmanned-specified funding (USV)", Box(0.604, 1.889, 1.807, 0.333), PALE_BLUE, DK, BLACK, size=PT(11)),
    MatrixBox("funding_header", "Currently manned capabilities (CMC) funding ", Box(2.485, 1.889, 8.468, 0.333), BLUE_HEADER, DK, WHITE, size=PT(11), line2="Surface missions", line2_italic=True),
    MatrixBox("funding_header", "Kill chain roles", Box(11.026, 1.889, 1.807, 0.333), DARK_NAVY, DK, WHITE, size=PT(11)),
)

MISSION_CELLS: tuple[MatrixBox, ...] = (
    MatrixBox("usv", "sUSV", Box(0.902, 2.323, 1.212, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("usv", "mUSV", Box(0.902, 2.758, 1.212, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("usv", "USV Enabling Capabilities", Box(0.902, 3.190, 1.212, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("cmc", "Anti-Air Warfare (incl. cUAS)", Box(2.641, 2.323, 1.213, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("cmc", "Electronic Warfare (Other)", Box(2.641, 2.758, 1.213, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("cmc", "C4", Box(2.641, 3.190, 1.214, 0.333), ANOTHER_CAMPAIGN, ANOTHER_CAMPAIGN, WHITE, footnote="4"),
    MatrixBox("cmc", "Anti-Surface Ship Warfare", Box(4.033, 2.323, 1.213, 0.333), BLACK, BLACK, WHITE, footnote="1"),
    MatrixBox("cmc", "ISR", Box(4.033, 2.758, 1.213, 0.333), BLACK, BLACK, WHITE, footnote="1"),
    MatrixBox("cmc", "Special Operations", Box(4.033, 3.190, 1.213, 0.333), ANOTHER_CAMPAIGN, ANOTHER_CAMPAIGN, WHITE, footnote="5"),
    MatrixBox("cmc", "Anti-Submarine Warfare", Box(5.424, 2.323, 1.213, 0.333), BLACK, BLACK, WHITE, footnote="1"),
    MatrixBox("cmc", "Mine Warfare", Box(5.424, 2.758, 1.213, 0.333), BLACK, BLACK, WHITE, footnote="1"),
    MatrixBox("cmc", "Sealift", Box(5.424, 3.190, 1.213, 0.333), ANOTHER_CAMPAIGN, ANOTHER_CAMPAIGN, WHITE, footnote="3"),
    MatrixBox("cmc", "Ballistic Missile Defense", Box(6.817, 2.323, 1.212, 0.333), BLACK, BLACK, WHITE, footnote="2"),
    MatrixBox("cmc", "Strike Warfare", Box(6.816, 2.758, 1.213, 0.333), BLACK, BLACK, WHITE, footnote="1"),
    MatrixBox("cmc", "VBSS", Box(6.816, 3.190, 1.213, 0.333), None, GRAY_3, GRAY_3, footnote="6"),
    MatrixBox("cmc_other_campaign", "Electronic Warfare (D&D)", Box(8.208, 2.323, 1.213, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("cmc_other_campaign", "Amphibious Warfare", Box(8.208, 2.758, 1.213, 0.333), ANOTHER_CAMPAIGN, ANOTHER_CAMPAIGN, WHITE, footnote="3"),
    MatrixBox("iamd", "IAMD (OBBBA)", Box(9.599, 2.323, 1.213, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("iamd", "IAMD (SHIELD)", Box(9.599, 2.758, 1.213, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("kill_chain", "Platforms", Box(11.046, 2.323, 1.767, 0.333), BLACK, BLACK, WHITE),
    MatrixBox("kill_chain", "Effectors", Box(11.045, 2.758, 1.768, 0.333), GRAY_1, GRAY_1, BLACK),
    MatrixBox("kill_chain", "Sensors", Box(11.046, 3.190, 1.768, 0.333), GRAY_1, GRAY_1, BLACK),
    MatrixBox("kill_chain", "Combat Systems Integration (incl. CEC)", Box(11.045, 3.622, 1.768, 0.333), GRAY_1, GRAY_1, BLACK),
)

LEGEND: tuple[LegendEntry, ...] = (
    LegendEntry("Included in sizing", Box(7.614, 1.563, 0.200, 0.200), Box(7.837, 1.563, 1.068, 0.200), BLACK, BLACK),
    LegendEntry("Sized in another campaign", Box(8.929, 1.563, 0.200, 0.200), Box(9.152, 1.563, 1.448, 0.200), ANOTHER_CAMPAIGN, ANOTHER_CAMPAIGN),
    LegendEntry("Future effort", Box(10.623, 1.563, 0.200, 0.200), Box(10.846, 1.563, 0.817, 0.200), GRAY_1, GRAY_1),
    LegendEntry("Non-addressable", Box(11.687, 1.563, 0.200, 0.200), Box(11.910, 1.563, 0.913, 0.200), None, GRAY_3),
)

STRUCTURE_RULES: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("left_spine_top", Box(0.515, 1.889, 0.000, 2.100), DK, 12700),
    ConnectorSpec("funding_to_budget_divider", Box(0.486, 4.041, 12.267, 0.000), RULE_BLUE, 3175, dashed=True, flip_h=True),
    ConnectorSpec("left_spine_budget", Box(0.512, 4.093, 0.002, 1.200), DK, 12700),
    ConnectorSpec("budget_to_color_divider", Box(0.486, 5.342, 12.267, 0.000), RULE_BLUE, 3175, dashed=True, flip_h=True),
    ConnectorSpec("left_spine_color", Box(0.512, 5.394, 0.002, 1.200), DK, 12700),
    ConnectorSpec("kill_chain_divider", Box(10.989, 1.889, 0.000, 2.066), RULE_BLUE, 3175, dashed=True, flip_v=True),
)

SPECIAL_NOTES: tuple[MatrixBox, ...] = (
    MatrixBox("approach_exception", "Sizing approach different vs. other CMC", Box(9.459, 2.249, 1.493, 1.706), None, DK, BLACK, size=PT(9), italic=True, anchor="b"),
    MatrixBox("footnote", "Note: (1) Only addressable by Surface materiel; (2) Current BMD mission; (3) Sized in USMC Campaign, with Sealift pertaining to Contested Logistics; (4) Undersea portion sized in Navy (Undersea) Campaign; (5) Sized in SOCOM Campaign; (6) Requires manned presence to fulfill mission", Box(0.495, 6.642, 12.367, 0.354), None, "none", BLACK, size=PT(10)),
)


def _xywh(box: Box) -> tuple[int, int, int, int]:
    return IN(box.x), IN(box.y), IN(box.w), IN(box.h)


def _box_paragraph(shape: MatrixBox) -> str:
    runs = [run(shape.text, size=shape.size, color=shape.text_color, bold=shape.bold or None, italic=shape.italic or None, font=FONT)]
    if shape.footnote:
        runs.append(run(shape.footnote, size=shape.size, color=shape.text_color, font=FONT))
    if shape.line2 is not None:
        runs.append(line_break())
        runs.append(run(shape.line2, size=shape.size, color=shape.text_color, italic=shape.line2_italic or None, font=FONT))
    return paragraph(runs, align="ctr", line_spacing=100000)


def _draw_box(out: list[str], n, shape: MatrixBox) -> None:
    out.append(
        text_box(
            n(),
            f"{shape.role}:{shape.text[:32]}",
            *_xywh(shape.box),
            [_box_paragraph(shape)],
            fill=shape.fill,
            line_color=shape.line,
            line_width=shape.line_width,
            anchor=shape.anchor,
            rot=shape.rot,
        )
    )


def paint_row_bands_and_headers(out: list[str], n) -> None:
    for shape in (*FUNDING_HEADERS, *ROW_BANDS):
        _draw_box(out, n, shape)


def paint_mission_grid(out: list[str], n) -> None:
    for shape in MISSION_CELLS:
        _draw_box(out, n, shape)


def paint_legend(out: list[str], n) -> None:
    for item in LEGEND:
        out.append(text_box(n(), f"LegendColorKey:{item.label}", *_xywh(item.key_box), [paragraph([], align="ctr", line_spacing=100000)], fill=item.fill, line_color=item.line, line_width=3175, anchor="ctr"))
        out.append(text_box(n(), f"LegendLabel:{item.label}", *_xywh(item.label_box), [paragraph([run(item.label, size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))


def paint_structure(out: list[str], n) -> None:
    for shape in SPINE_LABELS:
        _draw_box(out, n, shape)
    for rule in STRUCTURE_RULES:
        out.append(connector(n(), rule.name, *_xywh(rule.box), color=rule.color, width=rule.width, dashed=rule.dashed, flip_h=rule.flip_h, flip_v=rule.flip_v))


def paint_notes_callout_and_logo(out: list[str], n) -> None:
    for note in SPECIAL_NOTES:
        _draw_box(out, n, note)
    out.append(
        text_box(
            n(),
            "Callout:sUSVCapabilities",
            IN(0.551),
            IN(3.574),
            IN(2.785),
            IN(0.407),
            [paragraph([run("sUSV expected to deliver counter-UAS, Deception & Decoy, and ISR capabilities", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)],
            fill=None,
            line_color="none",
            prst="wedgeRectCallout",
            geom_adj={"adj1": "val -48497", "adj2": "val -3486"},
        )
    )
    out.append(picture(n(), "Logo:Saronic", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))


def _body() -> str:
    out: list[str] = []
    ids = iter(range(100, 2000))
    n = lambda: next(ids)  # noqa: E731 - sequential shape ids
    paint_row_bands_and_headers(out, n)
    paint_mission_grid(out, n)
    paint_legend(out, n)
    paint_structure(out, n)
    paint_notes_callout_and_logo(out, n)
    return "".join(out)


CHROME = Chrome(
    section="Market Sizing",
    topic="Navy (Surface incl. MDA)",
    title="Components",
    takeaway="The following funding inputs, sources, and colors of money are considered for sizing the Navy (Surface) market",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
