"""Teaching exemplar: SHIPS Act Overview money-flow diagram.

ROLE
  policy_flow / funding_and_subsidy_system

USE WHEN
  A slide needs to explain how penalties, fees, or taxes fund a subsidy pool
  that then supports domestic capacity or demand.

TEACHES
  - bottom-to-top money-flow reading order
  - actor-tier swimlanes on the left with icons
  - transaction verbs placed directly on connector routes
  - funding pool and fee bands as horizontal anchors
  - policy caveat as a speech-bubble callout, not as another flow node

TEXT-FIT PRECEDENT
  money_flow_nodes:
    geometry: mostly 1.9–2.46in wide x 0.321in high
    type: Arial 10pt bold, centered
    copy_when: policy entities must stay node-like and auditable

SOURCE NOTE
  Teaching rewrite of source-faithful `ships_act_overview.py`. The old
  row tuples are promoted into `FlowNode`, `TextSpec`, and `ConnectorSpec`
  records, with paint layers named for the policy-flow grammar.

FIDELITY NOTE
  Coordinates, colors, image relationships, connector routing, and visible
  text are preserved. The reading instruction remains explicit because the
  diagram is intentionally bottom-to-top.
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
    hyperlink_rid: str | None = None   # slide-rels rId from HYPERLINKS, or None


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
    swatch: Box
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
            hyperlink_rid=spec.hyperlink_rid,
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
            n(), "LegendSwatch", *entry.swatch.emu(),
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


IMAGES = [
    {"rId": "rId2", "file": "image6_9f2e24d3.png"},
    {"rId": "rId3", "file": "image7_f6006d1c.png"},
]

# External hyperlink on the crew-requirement callout. Two images take rId2/rId3,
# so the link continues at rId4 (CREW_CALLOUT's "46 USC 8103" run references it).
HYPERLINKS = [
    {"rId": "rId4", "url": "https://www.law.cornell.edu/uscode/text/46/8103"},
]

TEACHING_METADATA = {
    "role": "policy_flow / funding_and_subsidy_system",
    "use_when": "A policy mechanism turns fees or penalties into subsidy-backed demand.",
    "teaches": (
        "bottom-to-top money flow",
        "left-side actor tier bands",
        "edge verbs on connector routes",
        "funding-pool horizontal bands",
    ),
}

TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("money_flow_nodes", Box(2.744, 2.870, 10.092, 3.782), "10pt bold centered labels", "copy for policy/actor/funding nodes"),
    TextFitZone("tier_bands", Box(1.161, 1.418, 1.500, 5.554), "12pt bold labels in vertical swimlanes", "copy for actor-class rows"),
    TextFitZone("edge_labels", Box(2.054, 1.927, 9.425, 4.539), "10pt italic verbs on white label boxes", "copy when arrows need transaction verbs"),
)

COPY_RULES: tuple[str, ...] = (
    "Use edge labels only where the transaction verb changes the read.",
    "Keep the funding pool as a band, not as a small node, when it governs multiple flows.",
    "Put legal or eligibility caveats in callouts so the money-flow chain stays clean.",
)

FLOW_GRAMMAR = {
    "sources": "foreign vessel owners/operators pay penalties and fees",
    "pool": "Maritime Security Trust Fund",
    "uses": "capital subsidies + operating subsidies fund SCF build-out",
    "reading_order": "bottom to top",
}

BACKGROUND_BAND = TextSpec("background_band", "BackgroundBand", Box(2.713, 6.539, 8.123, 0.496), (), "DFE7EB", BLACK, 3175, "ctr")
FLOW_NODES: tuple[FlowNode, ...] = (
    FlowNode('penalty_source', 'Other foreign ship operators', Box(8.792, 6.652, 2, 0.321), GRAY_1, BLACK, BLACK, 12700, PT(10)),
    FlowNode('subsidy_mechanism', 'Operating Subsidies', Box(7.831, 4.321, 2.46, 0.321), '6DCF9E', BLACK, BLACK, 12700, PT(10)),
    FlowNode('penalty_source', '25-49% of orderbook at PRC', Box(6.847, 6.652, 1.9, 0.321), GRAY_2, BLACK, BLACK, 12700, PT(10)),
    FlowNode('penalty_source', '50% of orderbook / fleet from PRC', Box(4.795, 6.652, 1.9, 0.321), GRAY_3, BLACK, BLACK, 12700, PT(10)),
    FlowNode('subsidy_mechanism', 'Capital Subsidies', Box(5.288, 4.321, 2.46, 0.321), '3D9970', BLACK, WHITE, 12700, PT(10)),
    FlowNode('domestic_buildout', 'US Built Ships', Box(2.744, 2.87, 2.462, 0.321), '447BB2', BLACK, WHITE, 12700, PT(10)),
    FlowNode('subsidy_mechanism', 'Penalties', Box(2.744, 5.765, 6.002, 0.321), 'C00000', BLACK, WHITE, 12700, PT(10)),
    FlowNode('penalty_source', 'PRC owned/operated', Box(2.744, 6.652, 1.9, 0.321), 'A6A6A6', BLACK, WHITE, 12700, PT(10)),
)
TIER_BANDS: tuple[FlowNode, ...] = (
    FlowNode("tier_band", 'US Shipbuilders', Box(1.161, 1.418, 1.5, 1.2), '223E59', BLACK, WHITE, 12700, PT(12)),
    FlowNode("tier_band", 'US-Built, US-Flagged Vessel Owners / Operators', Box(1.161, 2.87, 1.5, 1.2), '447BB2', BLACK, WHITE, 12700, PT(12)),
    FlowNode("tier_band", 'Foreign Vessel Owners / Operators', Box(1.161, 5.773, 1.5, 1.2), '808080', BLACK, WHITE, 12700, PT(12)),
)
EDGE_LABELS: tuple[TextSpec, ...] = (
    TextSpec("edge_label", "EdgeVerb", Box(2.975, 1.927, 0.605, 0.181), (RunSpec('Sells', PT(10), BLACK, italic=True),), WHITE, NO_BORDER, 3175, "ctr"),
    TextSpec("edge_label", "EdgeVerb", Box(5.287, 3.887, 5.003, 0.182), (RunSpec('Paid to US vessel owner / operators for each ship in SCF', PT(10), BLACK, italic=True),), WHITE, NO_BORDER, 3175, "ctr"),
    TextSpec("edge_label", "EdgeVerb", Box(6.56, 4.963, 2.46, 0.182), (RunSpec('Disburses', PT(10), BLACK, italic=True),), WHITE, NO_BORDER, 3175, "ctr"),
    TextSpec("edge_label", "EdgeVerb", Box(6.287, 2.787, 1.444, 0.198), (RunSpec('Placed into service ', PT(10), BLACK, italic=True),), WHITE, NO_BORDER, 3175, "ctr"),
    TextSpec("edge_label", "EdgeVerb", Box(2.054, 2.65, 0.605, 0.181), (RunSpec('Buys', PT(10), BLACK, italic=True),), WHITE, NO_BORDER, 3175, "ctr"),
    TextSpec("edge_label", "EdgeVerb", Box(5.438, 6.284, 0.615, 0.182), (RunSpec('Pays', PT(10), BLACK, italic=True),), WHITE, NO_BORDER, 3175, "ctr"),
    TextSpec("edge_label", "EdgeVerb", Box(9.484, 6.284, 0.615, 0.182), (RunSpec('Pays', PT(10), BLACK, italic=True),), WHITE, NO_BORDER, 3175, "ctr"),
    TextSpec("edge_label", "EdgeVerb", Box(11.479, 6.278, 0.615, 0.182), (RunSpec('Pays', PT(10), BLACK, italic=True),), WHITE, NO_BORDER, 3175, "ctr"),
)

MONEY_BANDS: tuple[TextSpec, ...] = (
    TextSpec("tonnage_tax", "RegularTonnageTaxes", Box(8.791, 5.765, 2.000, 0.321), (RunSpec("Regular Tonnage Taxes ", PT(10), BLACK, bold=True), RunSpec("(Subject to exemptions)", PT(10), BLACK, italic=True, break_before=True)), "FFC000", BLACK, 3175, "ctr"),
    TextSpec("trust_fund", "MaritimeSecurityTrustFund", Box(2.744, 5.200, 10.092, 0.321), (RunSpec("Maritime Security Trust Fund ", PT(10), WHITE, bold=True), RunSpec("($20B cap, appropriations specified from FY26-FY35)", PT(10), WHITE, italic=True)), "1B4332", BLACK, 3175, "ctr"),
    TextSpec("cargo_fees", "CargoFees", Box(10.836, 5.765, 2.000, 0.321), (RunSpec("Cargo Fees ($0.01+ / kg)", PT(10), WHITE, bold=True), RunSpec("SHIPS Act “Plus” only", PT(10), WHITE, italic=True, break_before=True)), "FB6B3C", BLACK, 3175, "ctr"),
)

GOVERNMENT_BAND = FlowNode("actor_tier", "US Government", Box(1.161, 4.321, 1.500, 1.200), SCOPE_BLUE, BLACK, BLACK, 12700, PT(12))
SCF_TARGET = TextSpec("scf_target", "SCFTarget", Box(8.747, 2.334, 4.088, 0.819), (RunSpec("Strategic Commercial Fleet (SCF)", PT(10), WHITE, bold=True), RunSpec("(250 commercial ships for foreign trade only; ", PT(10), WHITE, italic=True, break_before=True), RunSpec("permanently ineligible for coastwise trade i.e., Jones Act", PT(10), WHITE, bold=True, italic=True), RunSpec(")", PT(10), WHITE, italic=True)), "0E1924", BLACK, 3175, "ctr")
TAX_CREDIT_NOTE = TextSpec("policy_note", "TaxCreditNote", Box(9.754, 1.418, 3.080, 0.595), (RunSpec("Vessel and Shipyard Investment Tax Credits (40% and 25%, respectively) from Building Ships in America Act not shown", PT(10), BLACK, italic=True),), None, BLACK, 3175, "ctr")
ROW_MARKER = TextSpec("row_marker", "PlusRowMarker", Box(0.174, 6.652, 0.827, 0.321), (RunSpec("+ ROW", PT(10), BLACK, bold=True),), None, NO_BORDER, 3175, "ctr")
READING_NOTE = TextSpec("reading_note", "BottomToTopNote", Box(0.139, 1.120, 3.080, 0.245), (RunSpec("Chart reads from bottom to top", PT(10), BLACK, italic=True),), None, NO_BORDER, 3175, None)
CREW_CALLOUT = TextSpec("policy_callout", "CrewRequirementCallout", Box(4.610, 2.173, 1.958, 0.510), (RunSpec("US crew required to participate in SCF; SHIPS Act states vessels will be crewed IAW ", PT(8), BLACK, italic=True), RunSpec("46 USC 8103", PT(8), BLACK, italic=True, hyperlink_rid="rId4"), RunSpec(" ", PT(8), BLACK, italic=True)), None, BLACK, 3175, "ctr", prst="wedgeRectCallout", geom_adj={"adj1": "val 41650", "adj2": "val 74944"})

FUNDING_CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("funding_route", "Connector: Elbow 43", Box(4.437, 5.344, 0.565, 2.051), BLACK, 12700, True, "bentConnector3", flip_h=True, flip_v=True, rot=5400000),
    ConnectorSpec("funding_route", "Connector: Elbow 44", Box(6.488, 5.344, 0.565, 2.051), BLACK, 12700, True, "bentConnector3", flip_v=True, rot=16200000),
    ConnectorSpec("funding_route", "Connector: Elbow 50", Box(6.646, 4.621, 0.244, 2.045), BLACK, 12700, True, "bentConnector3", flip_h=True, flip_v=True, rot=5400000),
    ConnectorSpec("funding_route", "Connector: Elbow 54", Box(8.669, 4.643, 0.244, 2.001), BLACK, 12700, True, "bentConnector3", flip_v=True, rot=16200000),
)

POLICY_CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("owner_operator_route", "Connector: Elbow 65", Box(8.147, 4.286, 0.558, 1.271), BLACK, 12700, True, "bentConnector3", flip_h=True, flip_v=True, rot=5400000),
    ConnectorSpec("owner_operator_route", "Connector: Elbow 69", Box(6.875, 4.285, 0.558, 1.272), BLACK, 12700, True, "bentConnector3", flip_v=True, rot=16200000),
    ConnectorSpec("build_route", "Connector: Elbow 72", Box(2.661, 2.018, 1.314, 0.852), BLACK, 12700, True, "bentConnector2"),
    ConnectorSpec("subsidy_route", "Connector: Elbow 86", Box(4.681, 2.485, 1.131, 2.543), BLACK, 12700, True, "bentConnector3", flip_v=True, rot=16200000),
    ConnectorSpec("subsidy_route", "Connector: Elbow 89", Box(5.953, 1.213, 1.131, 5.086), BLACK, 12700, True, "bentConnector3", flip_v=True, rot=16200000),
    ConnectorSpec("scf_route", "Connector: Elbow 137", Box(5.206, 2.744, 3.541, 0.286), BLACK, 12700, True, "bentConnector3", flip_v=True),
    ConnectorSpec("buys_route", "Straight Arrow Connector 147", Box(1.911, 2.618, 0.000, 0.252), BLACK, 12700, True, "line", flip_v=True),
    ConnectorSpec("penalty_route", "Straight Arrow Connector 189", Box(5.745, 6.087, 0.000, 0.565), BLACK, 12700, True, "line", flip_v=True),
    ConnectorSpec("penalty_route", "Straight Arrow Connector 193", Box(9.791, 6.087, 0.000, 0.565), BLACK, 12700, True, "line", flip_h=True, flip_v=True),
    ConnectorSpec("cargo_fee_route", "Connector: Elbow 204", Box(10.836, 6.087, 1.000, 0.700), BLACK, 12700, True, "bentConnector2", flip_v=True),
    ConnectorSpec("cargo_fee_route", "Connector: Elbow 208", Box(9.691, 3.620, 0.244, 4.046), BLACK, 12700, True, "bentConnector3", flip_v=True, rot=16200000),
)


def paint_background_and_chrome(out: list[str], n) -> None:
    _draw_text(out, n, BACKGROUND_BAND)
    out.append("")
    out.append("")


def paint_flow_nodes_and_tiers(out: list[str], n) -> None:
    for node in FLOW_NODES:
        _draw_flow_node(out, n, node)
    _draw_text(out, n, MONEY_BANDS[0])
    for tier in TIER_BANDS:
        _draw_flow_node(out, n, tier)
    out.append(picture(n(), "ForeignTierFlag", "rId2", IN(0.287), IN(6.173), IN(0.600), IN(0.400)))
    out.append(picture(n(), "DomesticTierFlag", "rId3", IN(0.207), IN(1.818), IN(0.760), IN(0.400)))
    _draw_flow_node(out, n, GOVERNMENT_BAND)


def paint_funding_pool_and_routes(out: list[str], n) -> None:
    _draw_text(out, n, MONEY_BANDS[1])
    for route in FUNDING_CONNECTORS:
        _draw_connector(out, n, route)
    out.append(picture(n(), "OwnerTierFlag", "rId3", IN(0.207), IN(3.270), IN(0.760), IN(0.400)))
    out.append(picture(n(), "GovernmentTierFlag", "rId3", IN(0.207), IN(4.721), IN(0.760), IN(0.400)))
    for route in POLICY_CONNECTORS[:5]:
        _draw_connector(out, n, route)
    _draw_text(out, n, SCF_TARGET)


def paint_edge_labels_and_policy_notes(out: list[str], n) -> None:
    # Paint order IS the lesson here. Each white transaction-verb box is drawn
    # immediately AFTER the connector it sits on, so the label overlays (breaks)
    # the line behind its text — exactly as the source-faithful module does it.
    # The previous version painted every verb first and the routes afterward, which
    # let connectors 137/147/189/193/204 run over "Placed into service", "Buys",
    # and the three "Pays" labels.
    _draw_text(out, n, EDGE_LABELS[0])              # Sells (its route is already painted)
    _draw_text(out, n, EDGE_LABELS[1])              # Paid to US vessel owner / operators ...
    _draw_text(out, n, EDGE_LABELS[2])              # Disburses
    _draw_connector(out, n, POLICY_CONNECTORS[5])   # Elbow 137 — SCF "placed into service" route
    _draw_text(out, n, EDGE_LABELS[3])              # Placed into service
    _draw_connector(out, n, POLICY_CONNECTORS[6])   # Straight 147 — Buys route
    _draw_text(out, n, EDGE_LABELS[4])              # Buys
    _draw_text(out, n, TAX_CREDIT_NOTE)
    _draw_connector(out, n, POLICY_CONNECTORS[7])   # Straight 189 — penalty route
    _draw_text(out, n, EDGE_LABELS[5])              # Pays (penalties)
    _draw_connector(out, n, POLICY_CONNECTORS[8])   # Straight 193 — tonnage-tax route
    _draw_text(out, n, EDGE_LABELS[6])              # Pays (tonnage taxes)
    _draw_text(out, n, MONEY_BANDS[2])              # Cargo Fees band
    _draw_connector(out, n, POLICY_CONNECTORS[9])   # Elbow 204 — cargo-fee route
    _draw_text(out, n, EDGE_LABELS[7])              # Pays (cargo fees)
    _draw_connector(out, n, POLICY_CONNECTORS[10])  # Elbow 208 — cargo-fee return route
    _draw_text(out, n, ROW_MARKER)
    _draw_text(out, n, READING_NOTE)
    _draw_text(out, n, CREW_CALLOUT)


def _body() -> str:
    out: list[str] = []
    ids = _shape_ids()
    n = lambda: next(ids)  # noqa: E731
    paint_background_and_chrome(out, n)
    paint_flow_nodes_and_tiers(out, n)
    paint_funding_pool_and_routes(out, n)
    paint_edge_labels_and_policy_notes(out, n)
    return "".join(out)


CHROME = Chrome(
    section="US-Built Ship Demand",
    topic="With SHIPS Act",
    title="SHIPS Act Overview",
    takeaway="Foreign penalties fund domestic Strategic Commercial Fleet (SCF) build-out.",
    preliminary=False,
)


def render() -> str:
    return body_slide(CHROME, _body())
