"""Teaching exemplar: Approach to find TCV — IAMD OBBBA / SHIELD.

ROLE
  market_sizing_flow / domain_role_allocation_tcv

USE WHEN
  A market-sizing slide needs to allocate funding first by domain, then by
  kill-chain role, before moving through Total Funding, TAM, SAM, and TCV.

TEACHES
  - step 1 as a standalone method card, with steps 2–6 as a repeated rail
  - domain and kill-chain filters as flow nodes, not prose annotations
  - dashed allocation-percentage boxes as method notes
  - right-hand BLUE_1→BLUE_4 output stack
  - raw/verbatim title-placeholder residue documented as intentional

TEXT-FIT PRECEDENT
  allocation_callouts:
    geometry: 4.741–5.001in wide dashed boxes
    type: Arial 10pt italic, one label only
    copy_when: a model narrows a funding pool through allocation percentages

SOURCE NOTE
  Teaching rewrite of source-faithful `tcv_approach_iamd.py`. The old
  converter buckets are promoted into typed `StepCard`, `FlowNode`,
  `GlyphSpec`, `LegendEntry`, `TextSpec`, and `ConnectorSpec` records.

FIDELITY NOTE
  Coordinates, raw title placeholder, colors, logo relationship, connector
  geometry, and visible text are preserved. Paint order is expressed via
  named layers so agents can copy the diagram grammar by role.
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
BLUE_5 = "263746"
GRAY_1 = "F2F2F2"
GRAY_2 = "D9D9D9"
GRAY_3 = "BFBFBF"
FONT = "Arial"

LAYOUT = "slideLayout4"

CHARTS: list = []

NO_BORDER = "none"
OTHER_CAMPAIGN = "A6A6A6"
PALE_SCOPE_BLUE = "CEDDEC"
SCOPE_BLUE = "99B9D8"
SURFACE_BLUE = "447BB2"
RULE_GRAY = "808080"


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
    align: str | None = None
    anchor: str = "ctr"
    prst: str = "rect"
    rot: int = 0
    geom_adj: dict[str, str] | None = None
    dashed_line: bool = False
    wrap: str = "square"
    size: int = PT(10)


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
class LegendEntry:
    label: str
    key_box: Box
    label_box: Box
    fill: str | None
    line_color: str | None
    align: str | None = None


@dataclass(frozen=True)
class GlyphSpec:
    role: str
    name: str
    box: Box
    prst: str
    fill: str | None = BLACK
    line_color: str | None = BLACK
    line_width: int = 12700
    rot: int = 0
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


def _p(runs: tuple[RunSpec, ...], *, align: str | None = None, mar_l: int | None = None, indent: int | None = None) -> str:
    pieces: list[str] = []
    for spec in runs:
        if spec.break_before:
            pieces.append(line_break())
        pieces.append(run(
            spec.text,
            size=spec.size,
            color=spec.color,
            bold=spec.bold or None,
            italic=spec.italic or None,
            font=FONT,
        ))
    kwargs = {"line_spacing": 100000}
    if align is not None:
        kwargs["align"] = align
    if mar_l is not None:
        kwargs["mar_l"] = mar_l
    if indent is not None:
        kwargs["indent"] = indent
    return paragraph(pieces, **kwargs)


def _draw_text(out: list[str], n, spec: TextSpec) -> None:
    x, y, w, h = spec.box.emu()
    out.append(text_box(
        n(), spec.name, x, y, w, h,
        [_p(spec.runs, align=spec.align)],
        fill=spec.fill,
        line_color=spec.line_color,
        line_width=spec.line_width,
        anchor=spec.anchor,
        prst=spec.prst,
        rot=spec.rot,
        geom_adj=spec.geom_adj,
        dashed_line=spec.dashed_line,
        wrap=spec.wrap,
    ))


def _draw_flow_node(out: list[str], n, node: FlowNode) -> None:
    out.append(text_box(
        n(), "FlowNode", *node.box.emu(),
        [paragraph([run(node.label, size=node.size, color=node.text_color, font=FONT)], align="ctr", line_spacing=100000)],
        fill=node.fill,
        line_color=node.line_color,
        line_width=node.line_width,
        anchor="ctr",
    ))


def _draw_step(out: list[str], n, step: StepCard) -> None:
    _draw_text(out, n, TextSpec("approach_step", "ApproachStep", step.box, (RunSpec(step.label, PT(10)),), align=None))


def _draw_glyph(out: list[str], n, glyph: GlyphSpec) -> None:
    out.append(text_box(
        n(), glyph.name, *glyph.box.emu(),
        [paragraph([], align="ctr", line_spacing=100000)],
        fill=glyph.fill,
        line_color=glyph.line_color,
        line_width=glyph.line_width,
        prst=glyph.prst,
        rot=glyph.rot,
        geom_adj=glyph.geom_adj,
        anchor="ctr",
    ))


def _draw_connector(out: list[str], n, spec: ConnectorSpec) -> None:
    out.append(connector(
        n(), spec.name, *spec.box.emu(),
        color=spec.color,
        width=spec.width,
        arrow=spec.arrow,
        prst=spec.prst,
        dashed=spec.dashed,
        flip_h=spec.flip_h,
        flip_v=spec.flip_v,
        rot=spec.rot,
        adj=spec.adj,
    ))


def _draw_legend(out: list[str], n, entries: tuple[LegendEntry, ...]) -> None:
    for entry in entries:
        out.append(text_box(
            n(), "LegendColorKey", *entry.key_box.emu(),
            [paragraph([], align="ctr", line_spacing=100000)],
            fill=entry.fill,
            line_color=entry.line_color,
            line_width=3175,
            anchor="ctr",
        ))
    for entry in entries:
        out.append(text_box(
            n(), "LegendLabel", *entry.label_box.emu(),
            [paragraph([run(entry.label, size=PT(8), color=BLACK, font=FONT)], align=entry.align, line_spacing=100000)],
            fill=None,
            line_color=NO_BORDER,
            anchor="ctr",
            wrap="none",
        ))


IMAGES = [{"rId": "rId2", "file": "image8_3071a231.jpeg"}]


TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("step_rail", Box(0.522, 1.882, 2.385, 4.359), "Arial 10pt; step 1 includes a short italic qualifier", "copy for filtered sizing methods"),
    TextFitZone("allocation_callouts", Box(5.751, 2.526, 5.001, 1.380), "Arial 10pt italic; one allocation label", "copy for percentage-allocation notes"),
    TextFitZone("domain_role_nodes", Box(5.793, 2.785, 4.910, 1.090), "Arial 10pt centered; categorical filters", "copy for market narrowing stages"),
)

COPY_RULES: tuple[str, ...] = (
    "Show allocation percentages as dashed method notes, not as financial-value boxes.",
    "Use this pattern when a funding pool is narrowed through multiple filters before TAM.",
    "Document raw-placeholder residue rather than silently replacing it with house chrome.",
)

FLOW_GRAMMAR = {
    "source_pool": "relevant OBBBA / SHIELD funding items",
    "filters": "domain allocation → kill-chain-role allocation",
    "conversion_chain": "Total Funding → TAM by year → SAM → Company TCV",
}


STEP_ONE = TextSpec("approach_step", "StepOne", Box(0.522, 1.882, 2.385, 0.701), (RunSpec("1. Identify relevant OBBBA items ", PT(10)), RunSpec("(items shown are not exhaustive)", PT(10), italic=True)), align=None)

APPROACH_STEPS: tuple[StepCard, ...] = (
    StepCard(2, Box(0.522, 2.614, 2.385, 0.701), '2. Allocate to domains to find maritime-specific funding'),
    StepCard(4, Box(0.522, 4.077, 2.385, 0.701), '4. Multiply by FY allocations to find TAM by year'),
    StepCard(5, Box(0.522, 4.808, 2.385, 0.701), '5. Multiply by unmanned adoption rate to find SAM'),
    StepCard(6, Box(0.522, 5.540, 2.385, 0.701), '6. Multiply by Saronic market share to find Company TCV'),
    StepCard(3, Box(0.522, 3.345, 2.385, 0.701), '3. Allocate to kill chain roles to find Total Funding'),
)

FLOW_NODES: tuple[FlowNode, ...] = (
    FlowNode('right_summary_stack', 'Total Funding ($)', Box(11.268, 3.517, 1.867, 0.359), BLUE_1, DK, BLACK, 3175, PT(10)),
    FlowNode('domain_filter', 'Space', Box(9.236, 2.785, 1.467, 0.359), GRAY_1, GRAY_1, BLACK, 3175, PT(10)),
    FlowNode('domain_filter', 'Ground', Box(7.66, 2.785, 1.467, 0.359), GRAY_1, GRAY_1, BLACK, 3175, PT(10)),
    FlowNode('right_summary_stack', 'TAM ($)', Box(11.268, 4.248, 1.867, 0.359), BLUE_2, DK, BLACK, 3175, PT(10)),
    FlowNode('worked_chain_subtotal', 'Total Funding ($)', Box(2.989, 4.248, 2.266, 0.359), BLUE_1, DK, BLACK, 3175, PT(10)),
    FlowNode('worked_chain_subtotal', 'TAM ($)', Box(2.989, 4.979, 2.266, 0.359), BLUE_2, DK, BLACK, 3175, PT(10)),
    FlowNode('kill_chain_filter', 'Sensors', Box(8.293, 3.516, 1.16, 0.359), GRAY_1, GRAY_1, BLACK, 3175, PT(10)),
    FlowNode('kill_chain_filter', 'Combat Sys. Integration', Box(9.543, 3.516, 1.16, 0.359), GRAY_1, GRAY_1, BLACK, 3175, PT(10)),
    FlowNode('domain_filter', 'Maritime', Box(6.083, 2.785, 1.467, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('conversion_factor', 'FY allocations (%)', Box(8.436, 4.248, 2.267, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('conversion_factor', 'Unmanned adoption (%)', Box(8.437, 4.979, 2.266, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('conversion_factor', 'Saronic market share (%)', Box(8.437, 5.711, 2.266, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('right_summary_stack', 'Maritime-specific funding ($)', Box(11.268, 2.785, 1.867, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('worked_chain_subtotal', 'Relevant OBBBA items ($) ', Box(2.989, 2.785, 2.267, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('source_funding_item', 'Hypersonic test bed program ($)', Box(2.989, 2.054, 2.106, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('source_funding_item', 'Hypersonic defense systems ($)', Box(8.597, 2.054, 2.106, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('source_funding_item', 'Military missile defense capabilities ($)', Box(5.793, 2.054, 2.106, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('right_summary_stack', 'Relevant OBBBA items ($) ', Box(11.268, 2.054, 1.867, 0.359), DK, DK, WHITE, 12700, PT(10)),
    FlowNode('kill_chain_filter', 'Platforms', Box(5.793, 3.516, 1.16, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('worked_chain_subtotal', 'Maritime-specific funding ($)', Box(2.988, 3.516, 2.266, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('kill_chain_filter', 'Effectors', Box(7.043, 3.516, 1.16, 0.359), BLACK, BLACK, WHITE, 12700, PT(10)),
    FlowNode('right_summary_stack', 'SAM ($)', Box(11.268, 4.979, 1.867, 0.359), BLUE_3, DK, WHITE, 3175, PT(10)),
    FlowNode('right_summary_stack', 'Company TCV ($)', Box(11.268, 5.711, 1.867, 0.359), BLUE_4, DK, WHITE, 3175, PT(10)),
    FlowNode('worked_chain_subtotal', 'SAM ($)', Box(2.989, 5.711, 2.266, 0.359), BLUE_3, DK, WHITE, 3175, PT(10)),
)

OPERATOR_GLYPHS: tuple[GlyphSpec, ...] = (
    GlyphSpec('equals_column', "OperatorGlyph", Box(10.786, 2.765, 0.4, 0.4), 'mathEqual', BLACK, BLACK, 12700, 0),
    GlyphSpec('equals_column', "OperatorGlyph", Box(10.786, 4.227, 0.4, 0.4), 'mathEqual', BLACK, BLACK, 12700, 0),
    GlyphSpec('equals_column', "OperatorGlyph", Box(10.786, 5.69, 0.4, 0.4), 'mathEqual', BLACK, BLACK, 12700, 0),
    GlyphSpec('equals_column', "OperatorGlyph", Box(10.786, 4.959, 0.4, 0.4), 'mathEqual', BLACK, BLACK, 12700, 0),
    GlyphSpec('equals_column', "OperatorGlyph", Box(10.786, 3.496, 0.4, 0.4), 'mathEqual', BLACK, BLACK, 12700, 0),
    GlyphSpec('equals_column', "OperatorGlyph", Box(10.786, 2.033, 0.4, 0.4), 'mathEqual', BLACK, BLACK, 12700, 0),
    GlyphSpec('plus_operator', "OperatorGlyph", Box(5.433, 2.765, 0.4, 0.4), 'mathPlus', BLACK, BLACK, 12700, 2572505),
    GlyphSpec('plus_operator', "OperatorGlyph", Box(6.646, 4.959, 0.4, 0.4), 'mathPlus', BLACK, BLACK, 12700, 2572505),
    GlyphSpec('plus_operator', "OperatorGlyph", Box(6.646, 5.69, 0.4, 0.4), 'mathPlus', BLACK, BLACK, 12700, 2572505),
    GlyphSpec('plus_operator', "OperatorGlyph", Box(6.646, 4.227, 0.4, 0.4), 'mathPlus', BLACK, BLACK, 12700, 2572505),
    GlyphSpec('plus_operator', "OperatorGlyph", Box(5.303, 3.496, 0.4, 0.4), 'mathPlus', BLACK, BLACK, 12700, 2572505),
)

ADDRESSABILITY_LEGEND: tuple[LegendEntry, ...] = (
    LegendEntry("Sized in another campaign", Box(9.265, 1.582, 0.200, 0.200), Box(9.488, 1.582, 1.448, 0.200), OTHER_CAMPAIGN, OTHER_CAMPAIGN, None),
    LegendEntry("Non-addressable", Box(12.023, 1.582, 0.200, 0.200), Box(12.247, 1.582, 0.913, 0.200), None, GRAY_3, "ctr"),
    LegendEntry("Included in sizing", Box(7.951, 1.582, 0.200, 0.200), Box(8.174, 1.582, 1.068, 0.200), BLACK, BLACK, "ctr"),
    LegendEntry("Future effort", Box(10.960, 1.582, 0.200, 0.200), Box(11.183, 1.582, 0.817, 0.200), GRAY_1, GRAY_1, None),
)

ALLOCATION_NOTES: tuple[TextSpec, ...] = (
    TextSpec("domain_allocation", "DomainAllocation", Box(6.010, 2.526, 4.741, 0.664), (RunSpec("Domain allocations (%)", PT(10), italic=True),), None, DK, 3175, None, "t", dashed_line=True),
    TextSpec("kill_chain_allocation", "KillChainAllocation", Box(5.751, 3.290, 5.001, 0.616), (RunSpec("Kill chain role allocations (%)", PT(10), italic=True),), None, DK, 3175, None, "t", dashed_line=True),
)

APPROACH_HEADER = TextSpec("approach_header", "ApproachStepsHeader", Box(0.522, 1.507, 2.291, 0.359), (RunSpec("Approach steps", PT(10), italic=True),), align=None)
HEADER_RULE = ConnectorSpec("approach_header_rule", "ApproachHeaderRule", Box(0.523, 1.864, 2.289, 0.002), DK, 12700, False, "line", flip_h=True)
HEADER_CHIP = TextSpec("scope_chip", "ScopeChip", Box(9.352, 0.137, 2.201, 0.376), (RunSpec("Currently manned capabilities – OBBBA / IDIQ approach", PT(10), WHITE, bold=True),), SURFACE_BLUE, DK, 3175, "ctr")

ROUTE_CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("allocation_route", "AllocationRouteArrow", Box(7.975, 0.022, 0.373, 8.079), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("allocation_route", "AllocationRouteArrow", Box(7.975, 0.754, 0.373, 8.079), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("allocation_route", "AllocationRouteArrow", Box(7.976, -1.441, 0.372, 8.079), BLACK, 12700, True, "bentConnector3", rot=5400000, adj={"adj1": "val 15352"}),
    ConnectorSpec("allocation_route", "AllocationRouteArrow", Box(7.975, -0.710, 0.372, 8.080), BLACK, 12700, True, "bentConnector3", rot=5400000, adj={"adj1": "val 32676"}),
    ConnectorSpec("allocation_route", "AllocationRouteArrow", Box(7.975, 1.485, 0.373, 8.079), BLACK, 12700, True, "bentConnector3", rot=5400000),
)


def paint_chrome_and_raw_title(out: list[str], n) -> None:
    out.append("")
    out.append("")


def paint_approach_rail(out: list[str], n) -> None:
    _draw_text(out, n, STEP_ONE)
    for step in APPROACH_STEPS:
        _draw_step(out, n, step)


def paint_flow_nodes(out: list[str], n) -> None:
    for node in FLOW_NODES:
        _draw_flow_node(out, n, node)


def paint_operators_and_routes(out: list[str], n) -> None:
    for glyph in OPERATOR_GLYPHS:
        _draw_glyph(out, n, glyph)
    _draw_connector(out, n, ROUTE_CONNECTORS[0])
    _draw_connector(out, n, ROUTE_CONNECTORS[1])
    _draw_text(out, n, ALLOCATION_NOTES[0])
    _draw_glyph(out, n, GlyphSpec("source_sum_plus", "Plus Sign 131", Box(5.244, 2.033, 0.400, 0.400), "mathPlus", rot=5400000))
    _draw_glyph(out, n, GlyphSpec("source_sum_plus", "Plus Sign 132", Box(8.048, 2.033, 0.400, 0.400), "mathPlus", rot=5400000))
    _draw_text(out, n, APPROACH_HEADER)
    _draw_connector(out, n, HEADER_RULE)
    _draw_connector(out, n, ROUTE_CONNECTORS[2])
    _draw_text(out, n, ALLOCATION_NOTES[1])
    _draw_connector(out, n, ROUTE_CONNECTORS[3])
    _draw_connector(out, n, ROUTE_CONNECTORS[4])


def paint_legend_scope_and_logo(out: list[str], n) -> None:
    _draw_legend(out, n, ADDRESSABILITY_LEGEND)
    _draw_text(out, n, HEADER_CHIP)
    out.append(picture(n(), "NavyLogo", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))


def _body() -> str:
    out: list[str] = []
    ids = _shape_ids()
    n = lambda: next(ids)  # noqa: E731
    paint_chrome_and_raw_title(out, n)
    paint_approach_rail(out, n)
    paint_flow_nodes(out, n)
    paint_operators_and_routes(out, n)
    paint_legend_scope_and_logo(out, n)
    return "".join(out)


CHROME = Chrome(
    section="Market Sizing",
    topic="Navy (Surface incl. MDA)",
    title="Approach to find TCV",
    takeaway="IAMD (OBBBA and SHIELD)",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
