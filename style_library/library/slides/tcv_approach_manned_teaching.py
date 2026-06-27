"""Teaching exemplar: Approach to find TCV — currently manned capabilities.

ROLE
  market_sizing_flow / surface_cmc_tcv_primary

USE WHEN
  A slide needs to turn missions, kill-chain roles, and platform/effectors into a
  Navy market-sizing TCV build-up.

TEACHES
  - seven-step approach rail beside a dense mission-to-platform schematic
  - mission grid whose fills encode addressability
  - black platform/factor nodes feeding blue calculated outputs
  - parallel worked chain plus right-hand summary stack
  - connector fan-out from mission chips into platform/effectors

TEXT-FIT PRECEDENT
  mission_grid:
    geometry: 1.213in wide x 0.333in high cells
    type: Arial 9pt, centered, 100% line spacing
    content: compact mission names, occasionally two-line labels
    copy_when: a dense scope matrix must fit above a build-up flow

SOURCE NOTE
  Teaching rewrite of source-faithful `tcv_approach_manned.py`. This version
  replaces converter buckets with typed semantic records and named paint layers.

FIDELITY NOTE
  Geometry, colors, logo relationship, source text, and connector orientations are
  kept as reusable precedents. The module is organized for AI authors first; it is
  intentionally not a raw converter transcript.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, connector, line_break, paragraph, picture, run, text_box,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
DK = "162029"
BLUE_1 = "E2E9EF"
BLUE_2 = "B6C8D8"
BLUE_3 = "6E91B1"
BLUE_4 = "3D5972"
GRAY_1 = "F2F2F2"
GRAY_3 = "BFBFBF"
FONT = "Arial"

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []

SIZED_IN_ANOTHER_CAMPAIGN = "A6A6A6"
SCOPE_BLUE = "99B9D8"
PALE_SCOPE_BLUE = "CEDDEC"
SURFACE_BLUE = "447BB2"
RULE_GRAY = "808080"
NO_BORDER = "none"


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    def emu(self) -> tuple[int, int, int, int]:
        return IN(self.x), IN(self.y), IN(self.w), IN(self.h)


@dataclass(frozen=True)
class TextFitZone:
    name: str
    box: Box
    fit: str
    copy_when: str


@dataclass(frozen=True)
class RunSpec:
    text: str
    size: int = PT(10)
    color: str | None = BLACK
    bold: bool = False
    italic: bool = False
    break_before: bool = False


@dataclass(frozen=True)
class TextSpec:
    role: str
    name: str
    box: Box
    runs: tuple[RunSpec, ...]
    fill: str | None = None
    line_color: str | None = NO_BORDER
    line_width: int = 3175
    align: str | None = "ctr"
    anchor: str = "ctr"
    prst: str = "rect"
    rot: int = 0
    geom_adj: dict[str, str] | None = None
    dashed_line: bool = False
    wrap: str = "square"
    l_ins: int | None = None
    t_ins: int | None = None
    r_ins: int | None = None
    b_ins: int | None = None


@dataclass(frozen=True)
class StepCard:
    step: int
    box: Box
    label: str


@dataclass(frozen=True)
class FlowNode:
    role: str
    label: str
    box: Box
    fill: str | None
    line_color: str | None
    text_color: str
    line_width: int = 3175
    size: int = PT(9)


@dataclass(frozen=True)
class MissionCell:
    role: str
    label: str
    box: Box
    fill: str | None
    line_color: str | None
    text_color: str
    size: int = PT(9)


@dataclass(frozen=True)
class LegendEntry:
    label: str
    swatch: Box
    label_box: Box
    fill: str | None
    line_color: str | None
    label_align: str | None = "ctr"


@dataclass(frozen=True)
class GlyphSpec:
    role: str
    name: str
    box: Box
    prst: str
    rot: int = 0
    fill: str | None = BLACK
    line_color: str | None = BLACK
    line_width: int = 12700
    geom_adj: dict[str, str] | None = None


@dataclass(frozen=True)
class ConnectorSpec:
    role: str
    name: str
    box: Box
    color: str = BLACK
    width: int = 12700
    arrow: bool = False
    prst: str = "line"
    dashed: bool = False
    flip_h: bool = False
    flip_v: bool = False
    rot: int = 0
    adj: dict[str, str] | None = None


def _shape_ids():
    return iter(range(100, 2000))


def _p_from_runs(runs: tuple[RunSpec, ...], *, align: str | None = "ctr") -> str:
    body = []
    for spec in runs:
        if spec.break_before:
            body.append(line_break())
        body.append(run(
            spec.text,
            size=spec.size,
            color=spec.color,
            bold=spec.bold or None,
            italic=spec.italic or None,
            font=FONT,
        ))
    return paragraph(body, align=align, line_spacing=100000)


def _draw_text(out: list[str], n, spec: TextSpec) -> None:
    kwargs = dict(
        fill=spec.fill,
        line_color=spec.line_color,
        line_width=spec.line_width,
        anchor=spec.anchor,
        prst=spec.prst,
        rot=spec.rot,
        geom_adj=spec.geom_adj,
        dashed_line=spec.dashed_line,
        wrap=spec.wrap,
    )
    if spec.l_ins is not None:
        kwargs["l_ins"] = spec.l_ins
    if spec.t_ins is not None:
        kwargs["t_ins"] = spec.t_ins
    if spec.r_ins is not None:
        kwargs["r_ins"] = spec.r_ins
    if spec.b_ins is not None:
        kwargs["b_ins"] = spec.b_ins
    out.append(text_box(n(), spec.name, *spec.box.emu(), [_p_from_runs(spec.runs, align=spec.align)], **kwargs))


def _draw_step(out: list[str], n, step: StepCard) -> None:
    _draw_text(out, n, TextSpec(
        "approach_step",
        "ApproachStep",
        step.box,
        (RunSpec(step.label, PT(10), BLACK),),
        align=None,
        line_color=NO_BORDER,
    ))


def _draw_flow_node(out: list[str], n, node: FlowNode) -> None:
    out.append(text_box(
        n(),
        "FlowNode",
        *node.box.emu(),
        [paragraph([run(node.label, size=node.size, color=node.text_color, font=FONT)], align="ctr", line_spacing=100000)],
        fill=node.fill,
        line_color=node.line_color,
        line_width=node.line_width,
        anchor="ctr",
    ))


def _draw_mission_cell(out: list[str], n, cell: MissionCell) -> None:
    out.append(text_box(
        n(),
        "MissionCell",
        *cell.box.emu(),
        [paragraph([run(cell.label, size=cell.size, color=cell.text_color, font=FONT)], align="ctr", line_spacing=100000)],
        fill=cell.fill,
        line_color=cell.line_color,
        line_width=3175,
        anchor="ctr",
    ))


def _draw_glyph(out: list[str], n, glyph: GlyphSpec) -> None:
    out.append(text_box(
        n(),
        glyph.name,
        *glyph.box.emu(),
        [paragraph([], align="ctr", line_spacing=100000)],
        fill=glyph.fill,
        line_color=glyph.line_color,
        line_width=glyph.line_width,
        prst=glyph.prst,
        rot=glyph.rot,
        geom_adj=glyph.geom_adj,
        anchor="ctr",
    ))


def _draw_connector(out: list[str], n, c: ConnectorSpec) -> None:
    out.append(connector(
        n(),
        c.name,
        *c.box.emu(),
        color=c.color,
        width=c.width,
        arrow=c.arrow,
        prst=c.prst,
        dashed=c.dashed,
        flip_h=c.flip_h,
        flip_v=c.flip_v,
        rot=c.rot,
        adj=c.adj,
    ))


def _draw_legend(out: list[str], n) -> None:
    for entry in ADDRESSABILITY_LEGEND:
        out.append(text_box(
            n(),
            "LegendSwatch",
            *entry.swatch.emu(),
            [paragraph([], align="ctr", line_spacing=100000)],
            fill=entry.fill,
            line_color=entry.line_color,
            line_width=3175,
            anchor="ctr",
        ))
    for entry in ADDRESSABILITY_LEGEND:
        out.append(text_box(
            n(),
            "LegendLabel",
            *entry.label_box.emu(),
            [paragraph([run(entry.label, size=PT(8), color=BLACK, font=FONT)], align=entry.label_align, line_spacing=100000)],
            fill=None,
            line_color=NO_BORDER,
            anchor="ctr",
            wrap="none",
        ))

IMAGES = [{"rId": "rId2", "file": "image8_3071a231.jpeg"}]

TEACHING_METADATA = {
    "role": "market_sizing_flow / surface_cmc_tcv_primary",
    "use_when": "Current manned capability funding must be allocated through missions and platforms before TAM/SAM/TCV.",
    "teaches": (
        "mission-grid scoping",
        "ship-class row feeding platforms",
        "black factor nodes vs. blue outputs",
        "addressability legend and scope chip",
    ),
}

TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("approach_rail", Box(0.426, 1.484, 2.101, 5.285), "Arial 10pt; seven cards with one method action each", "copy for multi-step sizing methods"),
    TextFitZone("mission_grid", Box(2.667, 1.312, 9.027, 0.859), "Arial 9pt centered; mission names must be compact", "copy for scope grids over a flow"),
    TextFitZone("calculation_nodes", Box(3.003, 2.419, 9.975, 4.179), "Arial 9pt centered variables and factors", "copy for CMC TCV build-ups"),
)

COPY_RULES: tuple[str, ...] = (
    "Let mission chips answer what is in scope before the viewer reads the math.",
    "Use black nodes for inputs, role boxes, and factors; reserve the blue ramp for calculated outputs.",
    "Keep the right stack visually simple; put audit-trail complexity in the center chain.",
)

FLOW_GRAMMAR = {
    "scope": "missions → priority kill-chain roles → specific platforms/effectors",
    "budget_chain": "OBBBA items + Programs + Projects + Cost Elements = Total Funding",
    "conversion_chain": "Total Funding × allocation = TAM × adoption = SAM × share = Company TCV",
}

APPROACH_STEPS: tuple[StepCard, ...] = (
    StepCard(1, Box(0.426, 1.484, 2.101, 0.701), '1. Identify missions'),
    StepCard(2, Box(0.426, 2.248, 2.101, 0.701), '2. Identify priority kill chain roles'),
    StepCard(4, Box(0.426, 3.776, 2.101, 0.701), '4. Identify and sum corresponding budget items to find Total Funding'),
    StepCard(5, Box(0.426, 4.54, 2.101, 0.701), '5. Allocate platforms and effectors to missions to find TAM'),
    StepCard(6, Box(0.426, 5.304, 2.101, 0.701), '6. Multiply by unmanned adoption rate to find SAM'),
    StepCard(3, Box(0.426, 3.012, 2.101, 0.701), '3. Identify specific platforms / effectors for missions'),
    StepCard(7, Box(0.426, 6.068, 2.101, 0.701), '7. Multiply by Saronic market share to find Company TCV'),
)

FOOTNOTE_NOTES: tuple[TextSpec, ...] = (
    TextSpec('footnote_note', 'Label', Box(0.495, 6.642, 12.367, 0.354), (RunSpec('Note: (1) Programs and Projects included where relevant (e.g., no Cost Elements or Cost Elements in FY26 PBR account for small fraction of total Program/Project funds)', PT(10), BLACK),), align=None, line_color='none'),
)

CALCULATION_NODES: tuple[FlowNode, ...] = (
    FlowNode('right_summary_stack', 'Total Funding ($)', Box(11.46, 3.947, 1.519, 0.359), BLUE_1, BLACK, BLACK, 3175, PT(9)),
    FlowNode('right_summary_stack', 'TAM ($)', Box(11.46, 4.711, 1.519, 0.359), BLUE_2, BLACK, BLACK, 3175, PT(9)),
    FlowNode('role_scope_node', 'Combat Systems Integration (incl. CEC)', Box(10.956, 2.419, 2.022, 0.359), GRAY_1, GRAY_1, BLACK, 3175, PT(9)),
    FlowNode('role_scope_node', 'Sensors', Box(8.306, 2.419, 2.022, 0.359), GRAY_1, GRAY_1, BLACK, 3175, PT(9)),
    FlowNode('worked_chain_subtotal', 'Total Funding ($)', Box(3.003, 4.711, 2.549, 0.359), BLUE_1, BLACK, BLACK, 3175, PT(9)),
    FlowNode('worked_chain_subtotal', 'TAM ($)', Box(3.003, 5.475, 2.549, 0.359), BLUE_2, BLACK, BLACK, 3175, PT(9)),
    FlowNode('role_scope_node', 'Effectors', Box(5.656, 2.419, 2.022, 0.359), GRAY_1, GRAY_1, BLACK, 3175, PT(9)),
    FlowNode('right_summary_stack', 'SAM ($)', Box(11.46, 5.475, 1.519, 0.359), BLUE_3, BLACK, WHITE, 3175, PT(9)),
    FlowNode('right_summary_stack', 'Company TCV ($)', Box(11.46, 6.239, 1.519, 0.359), BLUE_4, BLACK, WHITE, 3175, PT(9)),
    FlowNode('black_factor_node', 'Platforms', Box(3.003, 2.419, 2.022, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('black_factor_node', 'Littoral Combat Ship', Box(9.768, 3.183, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('black_factor_node', 'Cost Elements ($)', Box(9.106, 3.947, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('black_factor_node', 'Mission allocations by platform and effector (%)', Box(8.077, 4.711, 2.548, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('black_factor_node', 'Unmanned adoption (%)', Box(8.088, 5.475, 2.548, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('worked_chain_subtotal', 'SAM ($)', Box(3.003, 6.239, 2.549, 0.359), BLUE_3, BLACK, WHITE, 3175, PT(9)),
    FlowNode('black_factor_node', 'Saronic market share (%)', Box(8.088, 6.239, 2.548, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('black_factor_node', 'OBBBA items ($)', Box(3.003, 3.947, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
)

MISSION_CELLS: tuple[MissionCell, ...] = (
    MissionCell('included_in_sizing', 'Anti-Air Warfare (incl. cUAS)', Box(2.777, 1.371, 1.213, 0.333), BLACK, BLACK, WHITE),
    MissionCell('included_in_sizing', 'Anti-Submarine Warfare', Box(5.344, 1.371, 1.213, 0.333), BLACK, BLACK, WHITE),
    MissionCell('sized_in_another_campaign', 'Amphibious Warfare', Box(9.196, 1.371, 1.213, 0.333), SIZED_IN_ANOTHER_CAMPAIGN, SIZED_IN_ANOTHER_CAMPAIGN, WHITE),
    MissionCell('included_in_sizing', 'Ballistic Missile Defense', Box(6.629, 1.371, 1.212, 0.333), BLACK, BLACK, WHITE),
    MissionCell('included_in_sizing', 'Electronic Warfare (D&D)', Box(7.912, 1.371, 1.213, 0.333), BLACK, BLACK, WHITE),
    MissionCell('included_in_sizing', 'Mine Warfare', Box(5.344, 1.772, 1.213, 0.333), BLACK, BLACK, WHITE),
    MissionCell('sized_in_another_campaign', 'Special Operations', Box(9.196, 1.772, 1.213, 0.333), SIZED_IN_ANOTHER_CAMPAIGN, SIZED_IN_ANOTHER_CAMPAIGN, WHITE),
    MissionCell('sized_in_another_campaign', 'Sealift', Box(10.48, 1.772, 1.213, 0.333), SIZED_IN_ANOTHER_CAMPAIGN, SIZED_IN_ANOTHER_CAMPAIGN, WHITE),
    MissionCell('included_in_sizing', 'Strike Warfare', Box(6.629, 1.774, 1.213, 0.333), BLACK, BLACK, WHITE),
    MissionCell('included_in_sizing', 'ISR', Box(4.06, 1.772, 1.213, 0.333), BLACK, BLACK, WHITE),
    MissionCell('sized_in_another_campaign', 'C4', Box(10.48, 1.371, 1.214, 0.333), SIZED_IN_ANOTHER_CAMPAIGN, SIZED_IN_ANOTHER_CAMPAIGN, WHITE),
    MissionCell('included_in_sizing', 'Electronic Warfare (Other)', Box(2.777, 1.778, 1.213, 0.333), BLACK, BLACK, WHITE),
)

ADDRESSABILITY_LEGEND: tuple[LegendEntry, ...] = (
    LegendEntry("Included in sizing", Box(7.764, 1.068, 0.200, 0.200), Box(7.987, 1.068, 1.068, 0.200), BLACK, BLACK, "ctr"),
    LegendEntry("Sized in another campaign", Box(9.078, 1.068, 0.200, 0.200), Box(9.301, 1.068, 1.448, 0.200), SIZED_IN_ANOTHER_CAMPAIGN, SIZED_IN_ANOTHER_CAMPAIGN, None),
    LegendEntry("Future effort", Box(10.773, 1.068, 0.200, 0.200), Box(10.996, 1.068, 0.817, 0.200), GRAY_1, GRAY_1, None),
    LegendEntry("Non-addressable", Box(11.836, 1.068, 0.200, 0.200), Box(12.060, 1.068, 0.913, 0.200), None, GRAY_3, "ctr"),
)

GRID_FRAME = TextSpec("mission_grid_frame", "MissionGridFrame", Box(2.667, 1.312, 6.497, 0.859), tuple(), None, BLACK)

SHIP_CLASS_BOXES: tuple[TextSpec, ...] = (
    TextSpec("ship_class", "Ticonderoga", Box(3.003, 3.183, 1.519, 0.359), (RunSpec("Ticonderoga", PT(9), WHITE, italic=True), RunSpec("-class cruisers", PT(9), WHITE)), BLACK, BLACK),
    TextSpec("ship_class", "ArleighBurke", Box(4.694, 3.183, 1.519, 0.359), (RunSpec("Arleigh Burke", PT(9), WHITE, italic=True), RunSpec("-class destroyers", PT(9), WHITE)), BLACK, BLACK),
    TextSpec("ship_class", "Zumwalt", Box(6.385, 3.183, 1.519, 0.359), (RunSpec("Zumwalt", PT(9), WHITE, italic=True), RunSpec("-class destroyers", PT(9), WHITE)), BLACK, BLACK),
    TextSpec("ship_class", "Constellation", Box(8.077, 3.183, 1.519, 0.359), (RunSpec("Constellation-", PT(9), WHITE, italic=True), RunSpec("class frigates", PT(9), WHITE)), BLACK, BLACK),
    TextSpec("ship_class", "Avenger", Box(11.460, 3.183, 1.519, 0.359), (RunSpec("Avenger", PT(9), WHITE, bold=True, italic=True), RunSpec("-class MCM ship", PT(9), WHITE, bold=True)), BLACK, BLACK),
)

PLATFORM_CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("mission_to_platform", "Connector: Elbow 47", Box(3.685, 2.855, 0.405, 0.252), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("mission_to_platform", "Connector: Elbow 48", Box(4.531, 2.261, 0.405, 1.440), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000),
    ConnectorSpec("mission_to_platform", "Connector: Elbow 49", Box(5.377, 1.415, 0.405, 3.131), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000),
    ConnectorSpec("mission_to_platform", "Connector: Elbow 50", Box(7.914, -1.122, 0.405, 8.205), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000),
    ConnectorSpec("mission_to_platform", "Connector: Elbow 51", Box(7.068, -0.276, 0.405, 6.514), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000),
    ConnectorSpec("mission_to_platform", "Connector: Elbow 52", Box(6.222, 0.570, 0.405, 4.822), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000),
)

BUDGET_FACTOR_BOXES: tuple[TextSpec, ...] = (
    TextSpec("budget_factor", "Programs", Box(5.037, 3.947, 1.519, 0.359), (RunSpec("Programs ($)", PT(9), WHITE), RunSpec("1", PT(9), WHITE)), BLACK, BLACK),
    TextSpec("budget_factor", "Projects", Box(7.072, 3.947, 1.519, 0.359), (RunSpec("Projects ($)", PT(9), WHITE), RunSpec(" 1", PT(9), WHITE)), BLACK, BLACK),
)

SUMMARY_CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("summary_arrow", "Connector: Elbow 63", Box(8.045, 0.538, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("summary_arrow", "Connector: Elbow 64", Box(8.045, 1.302, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("summary_arrow", "Connector: Elbow 65", Box(8.045, 2.065, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
)

BRACES: tuple[GlyphSpec, ...] = (
    GlyphSpec("grouping_brace", "Left Brace 69", Box(7.811, -1.253, 0.359, 9.975), "leftBrace", 16200000, None, BLACK, geom_adj={"adj1": "val 8333", "adj2": "val 7206"}),
    GlyphSpec("grouping_brace", "Left Brace 70", Box(7.811, -1.254, 0.359, 9.975), "leftBrace", 16200000, None, BLACK, geom_adj={"adj1": "val 8333", "adj2": "val 68631"}),
)

APPROACH_HEADER = TextSpec("approach_header", "ApproachStepsHeader", Box(0.425, 1.229, 2.101, 0.359), (RunSpec("Approach steps", PT(10), BLACK, italic=True),), line_color=NO_BORDER, align=None)
APPROACH_UNDERLINE = ConnectorSpec("approach_header_rule", "Approach underline", Box(0.426, 1.586, 2.100, 0.002), DK, 12700, flip_h=True)
MISSION_EXCEPTIONS: tuple[TextSpec, ...] = (
    TextSpec("mission_cell_multiline", "AntiShip", Box(4.060, 1.371, 1.213, 0.333), (RunSpec("Anti-Ship ", PT(9), WHITE), RunSpec("Warfare", PT(9), WHITE, break_before=True)), BLACK, BLACK),
    TextSpec("mission_cell_non_addressable", "VBSS", Box(11.765, 1.371, 1.213, 0.333), (RunSpec("VBSS", PT(9), GRAY_3),), None, GRAY_3),
)
MISSION_TO_PLATFORM_EXTRA = ConnectorSpec("mission_to_platform", "Connector: Elbow 112", Box(4.840, 1.344, 0.248, 1.902), BLACK, 12700, True, "bentConnector3", rot=5400000)
SCOPE_CHIP = TextSpec("scope_chip", "ScopeChip", Box(9.352, 0.137, 2.201, 0.376), (RunSpec("Currently manned capabilities – primary approach", PT(10), WHITE, bold=True),), SURFACE_BLUE, DK)


def paint_chrome(out: list[str], n) -> None:
    out.append("")
    out.append("")


def paint_approach_rail(out: list[str], n) -> None:
    for step in APPROACH_STEPS:
        _draw_step(out, n, step)
    for note in FOOTNOTE_NOTES:
        _draw_text(out, n, note)


def paint_scope_grid(out: list[str], n) -> None:
    for node in CALCULATION_NODES:
        _draw_flow_node(out, n, node)
    for cell in MISSION_CELLS:
        _draw_mission_cell(out, n, cell)


def paint_platforms_and_connectors(out: list[str], n) -> None:
    for spec in SHIP_CLASS_BOXES:
        _draw_text(out, n, spec)
    for c in PLATFORM_CONNECTORS:
        _draw_connector(out, n, c)
    _draw_text(out, n, BUDGET_FACTOR_BOXES[0])


def paint_operator_system(out: list[str], n) -> None:
    for y in (3.927, 4.691, 5.454, 6.218):
        _draw_glyph(out, n, GlyphSpec("equals_column", "Equals", Box(10.843, y, 0.400, 0.400), "mathEqual"))
    for y in (4.691, 5.454, 6.218):
        _draw_glyph(out, n, GlyphSpec("plus_column", "Plus", Box(6.629, y, 0.400, 0.400), "mathPlus", 2572505))
    for c in SUMMARY_CONNECTORS:
        _draw_connector(out, n, c)
    for brace in BRACES:
        _draw_glyph(out, n, brace)
    _draw_text(out, n, BUDGET_FACTOR_BOXES[1])
    for x in (6.614, 8.648, 4.579):
        _draw_glyph(out, n, GlyphSpec("budget_sum_plus", "Plus", Box(x, 3.927, 0.400, 0.400), "mathPlus", 5400000))
    _draw_text(out, n, APPROACH_HEADER)
    _draw_connector(out, n, APPROACH_UNDERLINE)


def paint_grid_frame_legend_and_scope(out: list[str], n) -> None:
    for spec in MISSION_EXCEPTIONS:
        _draw_text(out, n, spec)
    _draw_text(out, n, GRID_FRAME)
    _draw_connector(out, n, MISSION_TO_PLATFORM_EXTRA)
    _draw_legend(out, n)
    _draw_text(out, n, SCOPE_CHIP)
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))


def _body() -> str:
    out: list[str] = []
    ids = _shape_ids()
    n = lambda: next(ids)  # noqa: E731
    paint_chrome(out, n)
    paint_approach_rail(out, n)
    paint_scope_grid(out, n)
    paint_platforms_and_connectors(out, n)
    paint_operator_system(out, n)
    paint_grid_frame_legend_and_scope(out, n)
    return "".join(out)


CHROME = Chrome(
    section="Market Sizing",
    topic="Navy (Surface incl. MDA)",
    title="Approach to find TCV",
    takeaway="Currently manned capabilities",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
