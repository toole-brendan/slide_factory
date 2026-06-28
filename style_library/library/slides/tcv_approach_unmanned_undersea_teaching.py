"""Teaching exemplar: Approach to find TCV — unmanned undersea.

ROLE
  market_sizing_flow / unmanned_undersea_tcv

USE WHEN
  A slide must map UUV platform classes and undersea budget items into
  Total Funding, TAM, SAM, and Company TCV.

TEACHES
  - five-step method rail adapted from the USV-specified TCV exemplar
  - UUV platform taxonomy as compact black input nodes
  - budget-item summation with plus/equal glyphs and brace groupings
  - right-hand BLUE_1→BLUE_4 executive output stack
  - four-state addressability legend plus scope chip and logo

TEXT-FIT PRECEDENT
  approach_rail:
    geometry: 2.101in wide x 0.701in high cards
    type: Arial 10pt, left aligned, one numbered action per card
    copy_when: a market-sizing flow needs author logic beside the calculation body

  platform_taxonomy_inputs:
    geometry: 1.519in wide x 0.359in high nodes
    type: Arial 9pt, centered, short taxonomy labels
    copy_when: inputs are category labels rather than assumptions prose

SOURCE NOTE
  Teaching rewrite of source-faithful `tcv_approach_unmanned_undersea.py`.
  Converter-era tuple buckets are promoted into `StepCard`, `FlowNode`,
  `LegendEntry`, `TextSpec`, `GlyphSpec`, and `ConnectorSpec` records.

FIDELITY NOTE
  Coordinates, colors, visible text, logo relationship, connector routing,
  and source paint order are preserved. The teaching layer clarifies the
  shared TCV grammar and the undersea-specific platform taxonomy.
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


IMAGES = [{"rId": "rId2", "file": "image6_3071a231.jpeg"}]


TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("approach_rail", Box(0.425, 1.593, 2.101, 3.756), "Arial 10pt; one action per card", "copy for left-spine method rails"),
    TextFitZone("platform_inputs", Box(3.003, 1.764, 9.975, 0.359), "Arial 9pt; taxonomy labels only", "copy for domain/platform filters"),
    TextFitZone("output_stack", Box(11.460, 2.528, 1.519, 2.651), "Arial 9pt centered variables", "copy for TCV/TAM/SAM readouts"),
)

COPY_RULES: tuple[str, ...] = (
    "Keep platform taxonomy separate from budget taxonomy; connect them through operators/braces.",
    "Use the blue ramp only for calculated outputs; keep source inputs black or outlined.",
    "Preserve the footnote row when it qualifies the model boundary rather than a single node.",
)

FLOW_GRAMMAR = {
    "inputs": "S/M UUV + Large/XL UUV + Wave-powered UUV + Core Technologies",
    "budget_chain": "OBBBA items + Programs + Projects + Cost Elements = Total Funding",
    "conversion_chain": "Total Funding = TAM; TAM × adoption = SAM; SAM × Saronic share = Company TCV",
}

APPROACH_STEPS: tuple[StepCard, ...] = (
    StepCard(2, Box(0.425, 2.357, 2.101, 0.701), '2. Identify and sum corresponding budget items to find Total Funding'),
    StepCard(3, Box(0.425, 3.121, 2.101, 0.701), '3. Total Funding equals TAM'),
    StepCard(4, Box(0.425, 3.884, 2.101, 0.701), '4. Multiply by unmanned adoption rate to find SAM'),
    StepCard(1, Box(0.425, 1.593, 2.101, 0.701), '1. Identify applicable unmanned platforms'),
    StepCard(5, Box(0.425, 4.648, 2.101, 0.701), '5. Multiply by Saronic market share to find Company TCV'),
)

NOTE_REGIONS: tuple[TextSpec, ...] = (
    TextSpec("footnote", "MethodNote", Box(0.495, 6.642, 12.367, 0.354), (RunSpec('Note: (1) Programs and Projects included where relevant (e.g., no Cost Elements or Cost Elements in FY26 PBR account for small fraction of total Program/Project funds)', PT(10)),), align=None),
)

FLOW_NODES: tuple[FlowNode, ...] = (
    FlowNode('right_summary_stack', 'Total Funding ($)', Box(11.46, 2.528, 1.519, 0.359), BLUE_1, BLACK, BLACK, 3175, PT(9)),
    FlowNode('right_summary_stack', 'TAM ($)', Box(11.46, 3.292, 1.519, 0.359), BLUE_2, BLACK, BLACK, 3175, PT(9)),
    FlowNode('worked_chain_subtotal', 'Total Funding ($)', Box(3.003, 3.292, 2.549, 0.359), BLUE_1, BLACK, BLACK, 3175, PT(9)),
    FlowNode('worked_chain_subtotal', 'TAM ($)', Box(3.003, 4.056, 2.549, 0.359), BLUE_2, BLACK, BLACK, 3175, PT(9)),
    FlowNode('right_summary_stack', 'SAM ($)', Box(11.46, 4.056, 1.519, 0.359), BLUE_3, BLACK, WHITE, 3175, PT(9)),
    FlowNode('right_summary_stack', 'Company TCV ($)', Box(11.46, 4.82, 1.519, 0.359), BLUE_4, BLACK, WHITE, 3175, PT(9)),
    FlowNode('platform_taxonomy_input', 'S/M UUV', Box(3.003, 1.764, 1.519, 0.359), BLACK, 'A6A6A6', WHITE, 3175, PT(9)),
    FlowNode('platform_taxonomy_input', 'Large / XL UUV', Box(5.821, 1.764, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('budget_item_input', 'Cost Elements ($)', Box(9.106, 2.528, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('conversion_factor', 'Unmanned adoption (%) - 100% ', Box(8.088, 4.056, 2.548, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('worked_chain_subtotal', 'SAM ($)', Box(3.003, 4.819, 2.549, 0.359), BLUE_3, BLACK, WHITE, 3175, PT(9)),
    FlowNode('conversion_factor', 'Saronic market share (%)', Box(8.088, 4.819, 2.548, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('budget_item_input', 'OBBBA items ($)', Box(3.003, 2.528, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('platform_taxonomy_input', 'Wave-powered UUV', Box(8.64, 1.764, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
    FlowNode('right_summary_stack', 'Core Technologies', Box(11.459, 1.764, 1.519, 0.359), BLACK, BLACK, WHITE, 3175, PT(9)),
)

ADDRESSABILITY_LEGEND: tuple[LegendEntry, ...] = (
    LegendEntry("Sized in another campaign", Box(9.078, 1.068, 0.200, 0.200), Box(9.301, 1.068, 1.448, 0.200), OTHER_CAMPAIGN, OTHER_CAMPAIGN, None),
    LegendEntry("Non-addressable", Box(11.836, 1.068, 0.200, 0.200), Box(12.060, 1.068, 0.913, 0.200), None, GRAY_3, "ctr"),
    LegendEntry("Included in sizing", Box(7.764, 1.068, 0.200, 0.200), Box(7.987, 1.068, 1.068, 0.200), BLACK, BLACK, "ctr"),
    LegendEntry("Future effort", Box(10.773, 1.068, 0.200, 0.200), Box(10.996, 1.068, 0.817, 0.200), GRAY_1, GRAY_1, None),
)

PROGRAM_AND_PROJECT_BOXES: tuple[TextSpec, ...] = (
    TextSpec("budget_item", "Programs", Box(5.037, 2.528, 1.519, 0.359), (RunSpec("Programs ($)", PT(9), WHITE), RunSpec("1", PT(9), WHITE)), BLACK, BLACK, 3175, "ctr"),
    TextSpec("budget_item", "Projects", Box(7.072, 2.528, 1.519, 0.359), (RunSpec("Projects ($)", PT(9), WHITE), RunSpec(" 1", PT(9), WHITE)), BLACK, BLACK, 3175, "ctr"),
)

SUMMARY_CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("summary_route", "SummaryCollectionArrow", Box(8.045, -0.882, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("summary_route", "SummaryCollectionArrow", Box(8.045, -0.118, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
    ConnectorSpec("summary_route", "SummaryCollectionArrow", Box(8.045, 0.646, 0.405, 7.942), BLACK, 12700, True, "bentConnector3", rot=5400000),
)

BRACE_GLYPHS: tuple[GlyphSpec, ...] = (
    GlyphSpec("grouping_brace", "Left Brace 69", Box(7.811, -2.673, 0.359, 9.975), "leftBrace", None, BLACK, 12700, 16200000, {"adj1": "val 8333", "adj2": "val 7206"}),
    GlyphSpec("grouping_brace", "Left Brace 70", Box(7.811, -2.673, 0.359, 9.975), "leftBrace", None, BLACK, 3175, 16200000, {"adj1": "val 8333", "adj2": "val 68631"}),
)

APPROACH_HEADER = TextSpec("approach_header", "ApproachStepsHeader", Box(0.425, 1.229, 2.101, 0.359), (RunSpec("Approach steps", PT(10), BLACK, italic=True),), align=None)
APPROACH_UNDERLINE = ConnectorSpec("approach_header_rule", "Approach underline", Box(0.426, 1.586, 2.100, 0.002), DK, 12700, False, "line", flip_h=True)
SCOPE_CHIP = TextSpec("scope_chip", "ScopeChip", Box(9.121, 0.074, 2.663, 0.500), (RunSpec("Unmanned-specified", PT(12), DK, bold=True),), SCOPE_BLUE, DK, 3175, "ctr")


def paint_approach_rail(out: list[str], n) -> None:
    for step in APPROACH_STEPS:
        _draw_step(out, n, step)
    for note in NOTE_REGIONS:
        _draw_text(out, n, note)


def paint_calculation_nodes(out: list[str], n) -> None:
    for node in FLOW_NODES:
        _draw_flow_node(out, n, node)
    _draw_text(out, n, PROGRAM_AND_PROJECT_BOXES[0])


def paint_operator_routes(out: list[str], n) -> None:
    for y in (2.507, 3.271, 4.035, 4.799):
        _draw_glyph(out, n, GlyphSpec("equals_column", "Equals", Box(10.843, y, 0.400, 0.400), "mathEqual"))
    _draw_glyph(out, n, GlyphSpec("sam_conversion_plus", "Plus Sign 59", Box(6.629, 4.035, 0.400, 0.400), "mathPlus", rot=2572505))
    for route in SUMMARY_CONNECTORS:
        _draw_connector(out, n, route)
    _draw_glyph(out, n, GlyphSpec("tcv_conversion_plus", "Plus Sign 66", Box(6.629, 4.799, 0.400, 0.400), "mathPlus", rot=2572505))
    for brace in BRACE_GLYPHS:
        _draw_glyph(out, n, brace)
    _draw_text(out, n, PROGRAM_AND_PROJECT_BOXES[1])
    for x in (6.614, 8.648, 4.579):
        _draw_glyph(out, n, GlyphSpec("budget_sum_plus", "Plus", Box(x, 2.507, 0.300, 0.300), "mathPlus", rot=5400000))
    _draw_text(out, n, APPROACH_HEADER)
    _draw_connector(out, n, APPROACH_UNDERLINE)


def paint_legend_scope_and_logo(out: list[str], n) -> None:
    _draw_legend(out, n, ADDRESSABILITY_LEGEND)
    _draw_text(out, n, SCOPE_CHIP)
    out.append(picture(n(), "NavyLogo", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))


def _body() -> str:
    out: list[str] = []
    ids = _shape_ids()
    n = lambda: next(ids)  # noqa: E731
    paint_approach_rail(out, n)
    paint_calculation_nodes(out, n)
    paint_operator_routes(out, n)
    paint_legend_scope_and_logo(out, n)
    return "".join(out)


CHROME = Chrome(
    section="Market Sizing",
    topic="Navy (Undersea)",
    title="Approach to find TCV",
    takeaway="Unmanned-specified",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
