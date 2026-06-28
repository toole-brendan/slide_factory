"""Teaching exemplar: Approach to find TCV — undersea currently manned capabilities.

ROLE
  market_sizing_flow / undersea_cmc_tcv

USE WHEN
  A slide needs to allocate undersea missions and submarine/platform/effectors
  into Total Funding, TAM, SAM, and Company TCV.

TEACHES
  - undersea CMC variant of the Navy TCV build-up grammar
  - six-step rail plus an interleaved step-2b explanatory card
  - mission grid with undersea-specific labels and non-addressable strategic deterrence
  - submarine class row feeding platform/effectors
  - explicit line-width exceptions for high-emphasis factor nodes

TEXT-FIT PRECEDENT
  mission_grid:
    geometry: 1.213in wide x 0.333in high cells
    type: Arial 9pt, centered, white-on-black or grey-on-outline
    content: undersea mission labels, some two-line manual labels
    copy_when: a compact scope grid must sit above a calculation schematic

SOURCE NOTE
  Teaching rewrite of source-faithful `tcv_approach_manned_undersea.py`.
  Converter buckets are replaced by typed semantic records and named paint layers.

FIDELITY NOTE
  Coordinates, connector orientation, logo relationship, and original labels are
  preserved as reusable precedents. Organization is intentionally pedagogical.
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
BLUE_1 = "E2E9EF"
BLUE_2 = "B6C8D8"
BLUE_3 = "6E91B1"
BLUE_4 = "3D5972"
GRAY_1 = "F2F2F2"
GRAY_3 = "BFBFBF"
FONT = "Arial"

LAYOUT = "slideLayout4"

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
    key_box: Box
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
            "LegendColorKey",
            *entry.key_box.emu(),
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

IMAGES = [{"rId": "rId2", "file": "image6_3071a231.jpeg"}]


TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("approach_rail", Box(0.426, 1.484, 2.101, 5.285), "Arial 10pt; six numbered method cards plus one 2b card", "copy for undersea CMC build-ups"),
    TextFitZone("mission_grid", Box(2.721, 1.301, 9.027, 0.859), "Arial 9pt compact mission labels", "copy for dense undersea scope grids"),
    TextFitZone("calculation_nodes", Box(3.003, 2.419, 9.975, 4.179), "Arial 10pt centered labels", "copy when nodes have slightly more breathing room than surface CMC"),
)

COPY_RULES: tuple[str, ...] = (
    "Use the step-2b card when the platform/effectors row needs a caveat.",
    "Keep undersea mission cells short; use separate outlined cells for exclusions.",
    "Use thicker borders only for factor nodes whose logic should read as gates.",
)

FLOW_GRAMMAR = {
    "scope": "undersea missions → submarine classes / platforms / effectors",
    "budget_chain": "OBBBA items + Programs + Projects + Cost Elements = Total Funding",
    "conversion_chain": "Total Funding × mission allocation = TAM × adoption = SAM × share = Company TCV",
}

APPROACH_STEPS: tuple[StepCard, ...] = (
    StepCard(1, Box(0.426, 1.484, 2.101, 0.701), '1. Identify priority missions'),
    StepCard(2, Box(0.426, 2.248, 2.101, 0.701), '2. Identify priority kill chain roles'),
    StepCard(3, Box(0.426, 3.776, 2.101, 0.701), '3. Identify and sum corresponding budget items to find Total Funding'),
    StepCard(4, Box(0.426, 4.54, 2.101, 0.701), '4. Allocate platforms and effectors to missions to find TAM'),
    StepCard(5, Box(0.426, 5.304, 2.101, 0.701), '5. Multiply by unmanned adoption rate to find SAM'),
    StepCard(6, Box(0.426, 6.068, 2.101, 0.701), '6. Multiply by Saronic market share to find Company TCV'),
)

FOOTNOTE_NOTES: tuple[TextSpec, ...] = (
    TextSpec('footnote_note', 'Label', Box(0.495, 6.642, 12.367, 0.354), (RunSpec('Note: (1) Programs and Projects included where relevant (e.g., no Cost Elements or Cost Elements in FY26 PBR account for small fraction of total Program/Project funds)', PT(10), BLACK),), align=None, line_color='none'),
)

CALCULATION_NODES: tuple[FlowNode, ...] = (
    FlowNode('right_summary_stack', 'Total Funding ($)', Box(11.46, 3.947, 1.519, 0.359), BLUE_1, BLACK, BLACK, 3175, PT(10)),
    FlowNode('right_summary_stack', 'TAM ($)', Box(11.46, 4.711, 1.519, 0.359), BLUE_2, BLACK, BLACK, 3175, PT(10)),
    FlowNode('role_scope_node', 'Combat Systems Integration (incl. CEC)', Box(10.956, 2.419, 2.022, 0.359), GRAY_1, GRAY_1, BLACK, 3175, PT(10)),
    FlowNode('role_scope_node', 'Sensors', Box(8.306, 2.419, 2.022, 0.359), GRAY_1, GRAY_1, BLACK, 3175, PT(10)),
    FlowNode('worked_chain_subtotal', 'Total Funding ($)', Box(3.003, 4.711, 2.549, 0.359), BLUE_1, BLACK, BLACK, 3175, PT(10)),
    FlowNode('worked_chain_subtotal', 'TAM ($)', Box(3.003, 5.475, 2.549, 0.359), BLUE_2, BLACK, BLACK, 3175, PT(10)),
    FlowNode('right_summary_stack', 'SAM ($)', Box(11.46, 5.475, 1.519, 0.359), BLUE_3, BLACK, WHITE, 3175, PT(10)),
    FlowNode('right_summary_stack', 'Company TCV ($)', Box(11.46, 6.239, 1.519, 0.359), BLUE_4, BLACK, WHITE, 3175, PT(10)),
    FlowNode('black_factor_node', 'Oceanographic Ships', Box(8.077, 3.183, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(10)),
    FlowNode('black_factor_node', 'MK-48 torpedoes', Box(9.768, 3.183, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(10)),
    FlowNode('black_factor_node', 'MK-54 torpedoes', Box(11.46, 3.183, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(10)),
    FlowNode('worked_chain_subtotal', 'SAM ($)', Box(3.003, 6.239, 2.549, 0.359), BLUE_3, BLACK, WHITE, 3175, PT(10)),
    FlowNode('black_factor_node', 'Platforms', Box(3.003, 2.419, 2.022, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('black_factor_node', 'Cost Elements ($)', Box(9.106, 3.947, 1.519, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('black_factor_node', 'Mission allocations by platform and effector (%)', Box(8.077, 4.711, 2.548, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('black_factor_node', 'Unmanned adoption (%)', Box(8.088, 5.475, 2.548, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('black_factor_node', 'Saronic market share (%)', Box(8.088, 6.239, 2.548, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('black_factor_node', 'OBBBA items ($)', Box(3.003, 3.947, 1.519, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
)

MISSION_CELLS: tuple[MissionCell, ...] = (
    MissionCell('included_in_sizing', 'Electronic Warfare (Other)', Box(7.913, 1.35, 1.213, 0.333), BLACK, SIZED_IN_ANOTHER_CAMPAIGN, WHITE),
    MissionCell('included_in_sizing', 'ISR', Box(2.777, 1.745, 1.213, 0.333), BLACK, BLACK, WHITE),
    MissionCell('included_in_sizing', 'C5', Box(5.345, 1.35, 1.214, 0.333), BLACK, BLACK, WHITE),
    MissionCell('included_in_sizing', 'Electronic Warfare (D&D)', Box(6.629, 1.35, 1.213, 0.333), BLACK, SIZED_IN_ANOTHER_CAMPAIGN, WHITE),
    MissionCell('included_in_sizing', 'Mine Warfare', Box(4.061, 1.745, 1.213, 0.333), BLACK, BLACK, WHITE),
    MissionCell('included_in_sizing', 'Strike Warfare', Box(5.345, 1.745, 1.213, 0.333), BLACK, BLACK, WHITE),
    MissionCell('included_in_sizing', 'Subsea & Seabed Warfare', Box(6.629, 1.745, 1.213, 0.333), BLACK, BLACK, WHITE),
    MissionCell('sized_in_another_campaign', 'Special Operations', Box(9.197, 1.35, 1.213, 0.333), SIZED_IN_ANOTHER_CAMPAIGN, SIZED_IN_ANOTHER_CAMPAIGN, WHITE),
)

ADDRESSABILITY_LEGEND: tuple[LegendEntry, ...] = (
    LegendEntry("Included in sizing", Box(7.764, 1.068, 0.200, 0.200), Box(7.987, 1.068, 1.068, 0.200), BLACK, BLACK, "ctr"),
    LegendEntry("Sized in another campaign", Box(9.078, 1.068, 0.200, 0.200), Box(9.301, 1.068, 1.448, 0.200), SIZED_IN_ANOTHER_CAMPAIGN, SIZED_IN_ANOTHER_CAMPAIGN, None),
    LegendEntry("Future effort", Box(10.773, 1.068, 0.200, 0.200), Box(10.996, 1.068, 0.817, 0.200), GRAY_1, GRAY_1, None),
    LegendEntry("Non-addressable", Box(11.836, 1.068, 0.200, 0.200), Box(12.060, 1.068, 0.913, 0.200), None, GRAY_3, "ctr"),
)

STEP_2B = TextSpec("approach_step_detail", "Step2B", Box(0.426, 3.012, 2.101, 0.701), (RunSpec("2. Identify specific platforms / effectors for missions ", PT(10), BLACK), RunSpec("(platforms/effectors shown are not exhaustive)", PT(10), BLACK, italic=True)), line_color=NO_BORDER, align=None)

SUBMARINE_CLASS_BOXES: tuple[TextSpec, ...] = (
    TextSpec("submarine_class", "LosAngeles", Box(3.003, 3.183, 1.519, 0.359), (RunSpec("Los Angeles", PT(10), WHITE, italic=True), RunSpec("-class submarines", PT(10), WHITE)), BLACK, BLACK),
    TextSpec("submarine_class", "Ohio", Box(4.694, 3.183, 1.519, 0.359), (RunSpec("Ohio-", PT(10), WHITE, italic=True), RunSpec("class submarines", PT(10), WHITE)), BLACK, BLACK),
    TextSpec("submarine_class", "Virginia", Box(6.385, 3.183, 1.519, 0.359), (RunSpec("Virginia", PT(10), WHITE, italic=True), RunSpec("-class submarines", PT(10), WHITE)), BLACK, BLACK),
)

PLATFORM_CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("mission_to_platform", "MissionToPlatformArrow", Box(3.685, 2.855, 0.405, 0.252), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("mission_to_platform", "MissionToPlatformArrow", Box(4.531, 2.261, 0.405, 1.440), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000),
    ConnectorSpec("mission_to_platform", "MissionToPlatformArrow", Box(5.377, 1.415, 0.405, 3.131), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000),
    ConnectorSpec("mission_to_platform", "MissionToPlatformArrow", Box(9.240, 0.205, 0.405, 5.552), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000, adj={"adj1": "val 28752"}),
    ConnectorSpec("mission_to_platform", "MissionToPlatformArrow", Box(8.395, 1.050, 0.405, 3.861), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000, adj={"adj1": "val 28752"}),
    ConnectorSpec("mission_to_platform", "MissionToPlatformArrow", Box(7.549, 1.896, 0.405, 2.169), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000, adj={"adj1": "val 28752"}),
)

BUDGET_FACTOR_BOXES: tuple[TextSpec, ...] = (
    TextSpec("budget_factor", "Programs", Box(5.037, 3.947, 1.519, 0.359), (RunSpec("Programs ($)", PT(10), WHITE), RunSpec("1", PT(10), WHITE)), BLACK, BLACK, line_width=12700),
    TextSpec("budget_factor", "Projects", Box(7.072, 3.947, 1.519, 0.359), (RunSpec("Projects ($)", PT(10), WHITE), RunSpec(" 1", PT(10), WHITE)), BLACK, BLACK, line_width=12700),
    TextSpec("factor_node", "Effectors", Box(5.656, 2.419, 2.022, 0.359), (RunSpec("Effectors ", PT(10), WHITE), RunSpec("(ASuW and ASW only)", PT(10), WHITE, italic=True, break_before=True)), BLACK, BLACK, line_width=12700),
)

SUMMARY_CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("summary_arrow", "SummaryCollectionArrow", Box(8.045, 0.538, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("summary_arrow", "SummaryCollectionArrow", Box(8.045, 1.302, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("summary_arrow", "SummaryCollectionArrow", Box(8.045, 2.065, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
)

BRACES: tuple[GlyphSpec, ...] = (
    GlyphSpec("grouping_brace", "Left Brace 69", Box(7.811, -1.253, 0.359, 9.975), "leftBrace", 16200000, None, BLACK, geom_adj={"adj1": "val 8333", "adj2": "val 7206"}),
    GlyphSpec("grouping_brace", "Left Brace 70", Box(7.811, -1.254, 0.359, 9.975), "leftBrace", 16200000, None, BLACK, geom_adj={"adj1": "val 8333", "adj2": "val 68631"}),
)

APPROACH_HEADER = TextSpec("approach_header", "ApproachStepsHeader", Box(0.425, 1.229, 2.101, 0.359), (RunSpec("Approach steps", PT(10), BLACK, italic=True),), line_color=NO_BORDER, align=None)
APPROACH_UNDERLINE = ConnectorSpec("approach_header_rule", "Approach underline", Box(0.426, 1.586, 2.100, 0.002), DK, 12700, flip_h=True)
GRID_FRAME = TextSpec("mission_grid_frame", "MissionGridFrame", Box(2.721, 1.301, 6.454, 0.859), tuple(), None, BLACK)
MISSION_GRID_EXTRAS: tuple[TextSpec, ...] = (
    TextSpec("mission_cell_multiline", "AntiSurface", Box(4.061, 1.350, 1.213, 0.333), (RunSpec("Anti-Surface Ship ", PT(9), WHITE), RunSpec("Warfare", PT(9), WHITE, break_before=True)), BLACK, BLACK),
    TextSpec("mission_cell_multiline", "AntiSubmarine", Box(2.777, 1.350, 1.213, 0.333), (RunSpec("Anti-Submarine", PT(9), WHITE), RunSpec("Warfare", PT(9), WHITE, break_before=True)), BLACK, BLACK),
    TextSpec("mission_cell_non_addressable", "StrategicDeterrence", Box(10.481, 1.350, 1.213, 0.333), (RunSpec("Strategic Deterrence", PT(9), GRAY_3), RunSpec("5", PT(9), GRAY_3)), None, GRAY_3),
)
MISSION_TO_PLATFORM_EXTRA = ConnectorSpec("mission_to_platform", "MissionToPlatformArrow", Box(4.851, 1.322, 0.260, 1.935), BLACK, 12700, True, "bentConnector3", rot=5400000)
MISSION_TO_EFFECTOR_EXTRA = ConnectorSpec("mission_to_effectors", "MissionToEffectorsArrow", Box(6.178, 1.931, 0.260, 0.718), BLACK, 12700, True, "bentConnector3", flip_h=True, rot=16200000)
SCOPE_CHIP = TextSpec("scope_chip", "ScopeChip", Box(9.121, 0.074, 2.663, 0.500), (RunSpec("Currently manned capabilities", PT(12), WHITE, bold=True),), SURFACE_BLUE, DK)


def paint_approach_rail(out: list[str], n) -> None:
    for step in APPROACH_STEPS:
        _draw_step(out, n, step)
    for note in FOOTNOTE_NOTES:
        _draw_text(out, n, note)
    _draw_text(out, n, STEP_2B)


def paint_calculation_nodes(out: list[str], n) -> None:
    for node in CALCULATION_NODES:
        _draw_flow_node(out, n, node)


def paint_platforms_and_connectors(out: list[str], n) -> None:
    for spec in SUBMARINE_CLASS_BOXES:
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
    _draw_text(out, n, BUDGET_FACTOR_BOXES[2])
    _draw_text(out, n, APPROACH_HEADER)
    _draw_connector(out, n, APPROACH_UNDERLINE)
    _draw_connector(out, n, MISSION_TO_PLATFORM_EXTRA)
    _draw_text(out, n, SCOPE_CHIP)


def paint_legend_grid_and_logo(out: list[str], n) -> None:
    _draw_legend(out, n)
    _draw_text(out, n, GRID_FRAME)
    for cell in MISSION_CELLS:
        _draw_mission_cell(out, n, cell)
    for spec in MISSION_GRID_EXTRAS[:2]:
        _draw_text(out, n, spec)
    _draw_connector(out, n, MISSION_TO_EFFECTOR_EXTRA)
    out.append(picture(n(), "NavyLogo", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    _draw_text(out, n, MISSION_GRID_EXTRAS[2])


def _body() -> str:
    out: list[str] = []
    ids = _shape_ids()
    n = lambda: next(ids)  # noqa: E731
    paint_approach_rail(out, n)
    paint_calculation_nodes(out, n)
    paint_platforms_and_connectors(out, n)
    paint_operator_system(out, n)
    paint_legend_grid_and_logo(out, n)
    return "".join(out)


CHROME = Chrome(
    section="Market Sizing",
    topic="Navy (Undersea)",
    title="Approach to find TCV",
    takeaway="Currently manned capabilities",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
