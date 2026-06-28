"""Teaching exemplar: maritime-transport value-chain archetype map.

ROLE
  value_chain_archetype_map / value_capture_flow_diagram

USE WHEN
  A slide needs to explain which archetypes participate in a value-chain step,
  how value flows between them, and where margin/value capture differs.

TEACHES
  - value-chain stage headers reused from the logo-matrix family
  - centered archetype nodes with fill/text contrast encoded as data
  - value-flow panels for owned-vessel vs chartered-vessel paths
  - relationship connectors plus small italic edge labels
  - compact "$ TBD | EBIT margin" labels as quantitative badges
  - a manual legend that separates in-analysis archetypes from future effort

TEXT-FIT PRECEDENT
  description_blocks:
    geometry: 1.9in wide description boxes, 0.6-1.219in tall
    type: Arial 10pt, centered, zero left/right shape insets
    content: one operational definition per stage or archetype
    copy_when: a matrix cell needs an explanatory blurb without opening a rail

  metric_labels:
    geometry: ~1.576in wide x 0.225in high
    type: Arial 12pt bold; margin range italicized when known
    content: "Revenue | EBIT margin" readout
    copy_when: the slide needs compact economics facts beside a value-chain node

SOURCE NOTE
  Teaching rewrite of source-faithful `value_chain_maritime_transport.py`. The
  original kept converter-era clusters (`_FLOW_NODES`, `_ITEM_DESCRIPTIONS`, etc.).
  This version converts those into named semantic records: panels, stages,
  archetype nodes, descriptions, connectors, edge labels, metric labels, and
  legend entries.

FIDELITY NOTE
  Coordinates, text, colors, connectors, row-label tables, and the Preliminary
  chip are preserved. The module intentionally exposes the conceptual diagram
  grammar more strongly than the source paint-order buckets.
"""
from __future__ import annotations

from dataclasses import dataclass

from deck_core.authoring import (
    Chrome, IN, PT, body_slide, connector, line_break, paragraph, run, table, tbreak,
    tcell_rich, text_box, tpara, trow, trun,
)


# House colors (hex lives in the module; no shared palette).
BLACK = "000000"
WHITE = "FFFFFF"
BLUE_1 = "E2E9EF"
GRAY_1 = "F2F2F2"
GRAY_2 = "D9D9D9"
FONT = "Arial"


# Local table-cell kit (was deck_core.table_kit).
def edge(color, w=12700):
    """One cell-border edge dict (default 1pt hairline)."""
    return {"color": color, "width": w}

def bd(L=None, R=None, T=None, B=None):
    """Border map from only the sides drawn; omitted sides render no-fill."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None

def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """Multi-paragraph rich cell; borders via L/R/T/B=edge(...)."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))

LAYOUT = "slideLayout4"

CHARTS: list = []

DARK_STEP = "0E1924"
BLUE_STEP = "447BB2"
MID_GRAY = "808080"


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
class Panel:
    name: str
    box: Box
    text: str
    fill: str | None
    line: str | None
    italic: bool = True
    align: str = "ctr"
    fill_alpha: int | None = None   # source tints these grouping panels to ~10% opacity


@dataclass(frozen=True)
class StageHeader:
    label: str
    box: Box
    fill: str
    text_color: str
    prst: str = "chevron"


@dataclass(frozen=True)
class ArchetypeNode:
    name: str
    box: Box
    fill: str
    text_color: str


@dataclass(frozen=True)
class DescriptionBlock:
    role: str
    box: Box
    text: str


@dataclass(frozen=True)
class ConnectorSpec:
    name: str
    box: Box
    color: str = BLACK
    width: int = 12700
    dashed: bool = False
    arrow: bool = False
    prst: str = "line"
    flip_h: bool = False
    flip_v: bool = False
    rot: int = 0
    adj: dict[str, str] | None = None


@dataclass(frozen=True)
class EdgeLabel:
    text: str
    box: Box


@dataclass(frozen=True)
class MetricLabel:
    role: str
    box: Box
    margin: str
    fill: str | None = None
    italic_margin: bool = True


@dataclass(frozen=True)
class LegendEntry:
    label: tuple[str, ...]
    swatch_x: float
    label_box: Box
    fill: str | None


TEACHING_METADATA = {
    "role": "value_chain_archetype_map / value_capture_flow_diagram",
    "use_when": "Explain participants, relationships, and value capture in one value-chain step.",
    "teaches": (
        "archetype nodes as semantic records",
        "description blocks that define each stage/archetype",
        "relationship connectors labeled with small italic text",
        "manual metric labels for value capture",
    ),
    "fidelity": "source geometry and text preserved; diagram grammar promoted into typed data",
}

TEXT_FIT: tuple[TextFitZone, ...] = (
    TextFitZone("description_blocks", Box(2.285, 2.094, 10.410, 3.468), "10pt centered; zero left/right insets; 1.9in width", "copy for compact explanatory blurbs"),
    TextFitZone("archetype_nodes", Box(2.235, 3.938, 10.560, 2.709), "10pt bold centered; dark nodes use white text", "copy when a diagram mixes in-scope and out-of-scope actors"),
    TextFitZone("metric_labels", Box(3.873, 3.042, 8.659, 3.873), "12pt bold; italic margin values", "copy for compact economics readouts next to nodes"),
)

COPY_RULES: tuple[str, ...] = (
    "Use pale panels to group the path logic before drawing individual nodes.",
    "Keep stage descriptions centered and short; use a narrative rail for anything longer.",
    "Put metric labels near the node whose value capture they describe, not in a separate legend.",
    "Use arrow connectors only for actual value-flow logic; dashed rules are explanatory guides.",
)

PANELS: tuple[Panel, ...] = (
    Panel("cargo_moved_by_archetypes", Box(4.948, 3.457, 7.959, 1.850), "Cargo moved by one or more of the following maritime transport archetypes", GRAY_1, BLACK, align="l", fill_alpha=10196),
    Panel("chartered_vessels", Box(9.145, 5.962, 2.461, 1.000), "Value flow for chartered vessels", None, BLACK),
    Panel("owned_vessels", Box(3.600, 5.962, 4.975, 1.000), "Value flow for owned vessels", BLUE_1, MID_GRAY, fill_alpha=10196),
    Panel("charter_metric_frame", Box(5.088, 4.948, 4.853, 0.275), "", None, BLACK, italic=False),
)

STAGE_HEADERS: tuple[StageHeader, ...] = (
    StageHeader("Customer / Shipper Requires Cargo Shipment", Box(2.235, 1.695, 2.100, 0.400), GRAY_2, BLACK, "homePlate"),
    StageHeader("Coordination", Box(4.350, 1.695, 2.100, 0.400), GRAY_2, BLACK),
    StageHeader("Origin Shoreside Logistics", Box(6.465, 1.695, 2.100, 0.400), BLUE_STEP, WHITE),
    StageHeader("Maritime Transport", Box(8.580, 1.695, 2.100, 0.400), DARK_STEP, WHITE),
    StageHeader("Destination Shoreside Logistics", Box(10.695, 1.695, 2.100, 0.400), BLUE_STEP, WHITE),
)

ARCHETYPE_NODES: tuple[ArchetypeNode, ...] = (
    ArchetypeNode("Shipbuilders", Box(3.662, 6.246, 2.000, 0.401), DARK_STEP, WHITE),
    ArchetypeNode("Vessel Operating Common Carriers", Box(5.088, 3.938, 2.000, 0.400), DARK_STEP, WHITE),
    ArchetypeNode("Private Carriers", Box(10.795, 3.938, 2.000, 0.400), DARK_STEP, WHITE),
    ArchetypeNode("Charter Companies", Box(9.368, 6.246, 2.000, 0.401), DARK_STEP, WHITE),
    ArchetypeNode("Non-Vessel Operating Common Carriers", Box(2.235, 3.938, 2.000, 0.400), GRAY_2, BLACK),
    ArchetypeNode("MRO", Box(6.515, 6.246, 2.000, 0.401), GRAY_2, BLACK),
    ArchetypeNode("Tramp Carriers", Box(7.942, 3.938, 2.000, 0.400), GRAY_2, BLACK),
)

DESCRIPTIONS: tuple[DescriptionBlock, ...] = (
    DescriptionBlock("customer", Box(2.335, 2.094, 1.900, 0.900), "Initiation of transportation process by owner of goods (e.g., retailer, commodity trader, or manufacturer)"),
    DescriptionBlock("coordination", Box(4.450, 2.094, 1.900, 0.900), "Arrangement of transport modes, storage, and compliance by coordinating entities (e.g., BCOs, freight forwarders)"),
    DescriptionBlock("origin_shoreside", Box(6.565, 2.094, 1.900, 0.900), "Movement of cargo from originating site onto ocean vessel; includes various transport modes, terminal ops, and export customs clearance"),
    DescriptionBlock("maritime_transport", Box(8.680, 2.094, 1.900, 0.900), "Transport of cargo across ocean between ports of loading and discharge by common or private carriers on owned or chartered vessels"),
    DescriptionBlock("destination_shoreside", Box(10.795, 2.094, 1.900, 0.900), "Movement of cargo from ocean vessel to destination site; includes various transport modes, terminal ops, and import customs clearance "),
    DescriptionBlock("nvocc", Box(2.285, 4.343, 1.900, 1.219), "Books space on operator vessels and resells to shippers without owning ships; NVOCC are a Coordination players that act like carriers by assuming legal liability for cargo"),
    DescriptionBlock("vocc", Box(5.138, 4.343, 1.900, 0.600), "Own/lease and operate vessels on fixed schedules for public use"),
    DescriptionBlock("private_carriers", Box(10.845, 4.343, 1.900, 0.600), "Shippers who own/lease and operate an internal fleet to move their own cargo"),
    DescriptionBlock("tramp", Box(7.992, 4.343, 1.900, 0.600), "Own/lease and operate vessels on demand for public use (no fixed schedule)"),
)

CONNECTORS: tuple[ConnectorSpec, ...] = (
    ConnectorSpec("nvocc_to_vocc", Box(3.235, 3.154, 1.376, 0.783), arrow=True, prst="bentConnector2", flip_v=True, rot=10800000),
    ConnectorSpec("private_carrier_route", Box(10.410, 2.553, 0.604, 2.165), arrow=True, prst="bentConnector3", flip_h=True, rot=16200000, adj={"adj1": "val 65164"}),
    ConnectorSpec("stage_to_tramp", Box(7.557, 1.865, 0.604, 3.541), arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 65164"}),
    ConnectorSpec("tramp_elbow", Box(8.984, 3.291, 0.604, 0.688), arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 65251"}),
    ConnectorSpec("nvocc_leases_space", Box(4.235, 4.138, 0.853, 0.000), arrow=True),
    ConnectorSpec("chartered_value_flow", Box(9.324, 4.910, 0.655, 1.448), arrow=True, prst="bentConnector3", flip_h=True, rot=16200000),
    ConnectorSpec("owned_value_flow", Box(7.180, 4.214, 0.655, 2.840), arrow=True, prst="bentConnector3", rot=5400000),
    ConnectorSpec("shipbuilder_to_charter", Box(8.575, 6.462, 0.571, 0.000), arrow=True, flip_h=True),
    ConnectorSpec("destination_terminal_rule", Box(10.367, 3.532, 0.000, 1.700), color=MID_GRAY, width=19050, dashed=True),
)

EDGE_LABELS: tuple[EdgeLabel, ...] = (
    EdgeLabel("NVOCC leases space", Box(4.268, 3.836, 0.788, 0.267)),
    EdgeLabel("VOCC provides space", Box(4.268, 4.191, 0.788, 0.269)),
    EdgeLabel("Terminal Operators shown", Box(6.745, 3.259, 1.535, 0.183)),
    EdgeLabel("Terminal Operators shown", Box(10.997, 3.259, 1.535, 0.183)),
)

METRIC_LABELS: tuple[MetricLabel, ...] = (
    MetricLabel("tramp_carriers", Box(8.842, 3.042, 1.576, 0.225), "2 - 42%"),
    MetricLabel("shipbuilders", Box(3.873, 6.690, 1.576, 0.225), "2-6%", WHITE),
    MetricLabel("mro", Box(6.727, 6.689, 1.576, 0.226), "%TBD", WHITE, False),
    MetricLabel("coordination", Box(4.611, 3.042, 1.575, 0.225), "%TBD", WHITE, False),
    MetricLabel("origin_shoreside", Box(6.727, 3.042, 1.576, 0.225), "30-54%", WHITE),
    MetricLabel("destination_shoreside", Box(10.956, 3.042, 1.576, 0.225), "30-54%", WHITE),
    MetricLabel("charter_companies_mid", Box(8.153, 4.973, 1.575, 0.225), "%TBD", None, False),
    MetricLabel("charter_companies", Box(9.579, 6.690, 1.576, 0.225), "22-53%"),
    MetricLabel("vocc", Box(5.300, 4.973, 1.576, 0.225), "13-42%"),
)

LEGEND: tuple[LegendEntry, ...] = (
    LegendEntry(("Maritime Transport archetypes ", "considered in analysis"), 0.495, Box(0.707, 1.321, 1.760, 0.370), DARK_STEP),
    LegendEntry(("Other steps ", "considered in analysis"), 2.480, Box(2.693, 1.321, 1.312, 0.370), BLUE_STEP),
    LegendEntry(("Future effort",), 4.017, Box(4.229, 1.388, 0.817, 0.236), GRAY_2),
)


def _xywh(box: Box) -> tuple[int, int, int, int]:
    return IN(box.x), IN(box.y), IN(box.w), IN(box.h)


def _p(text: str, *, size=PT(10), bold=False, italic=False, color=BLACK, align="ctr") -> str:
    return paragraph([run(text, size=size, bold=bold or None, italic=italic or None, color=color, font=FONT)], align=align, line_spacing=100000)


def _metric_p(metric: MetricLabel) -> str:
    return paragraph(
        [
            run("$ TBD | ", size=PT(12), bold=True, color=BLACK, font=FONT),
            run(metric.margin, size=PT(12), bold=True, italic=metric.italic_margin or None, color=BLACK, font=FONT),
        ],
        align="ctr",
        line_spacing=100000,
    )


def paint_value_flow_panels(out: list[str], n) -> None:
    for panel in PANELS:
        paras = [_p(panel.text, size=PT(8), italic=panel.italic, align=panel.align)] if panel.text else [paragraph([], align="r", line_spacing=100000)]
        out.append(text_box(n(), f"ValueFlowPanel:{panel.name}", *_xywh(panel.box), paras, fill=panel.fill, fill_alpha=panel.fill_alpha, line_color=panel.line, line_width=6350 if panel.name == "charter_metric_frame" else 12700, dashed_line=panel.name == "charter_metric_frame"))


def paint_stage_headers(out: list[str], n) -> None:
    for header in STAGE_HEADERS:
        out.append(text_box(n(), f"StageHeader:{header.label}", *_xywh(header.box), [_p(header.label, bold=True, color=header.text_color)], fill=header.fill, line_color="none", prst=header.prst, geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))


def paint_archetype_nodes(out: list[str], n) -> None:
    for node in ARCHETYPE_NODES:
        out.append(text_box(n(), f"ArchetypeNode:{node.name}", *_xywh(node.box), [_p(node.name, bold=True, color=node.text_color)], fill=node.fill, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))


def paint_row_labels_and_metric_header(out: list[str], n) -> None:
    out.append(table(n(), "RowLabel:ValueChainStep", IN(0.495), IN(1.695), IN(1.600), IN(1.638), col_widths=[IN(1.600)], rows=[
        trow([rcell([tpara([trun("Value Chain Step", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), tbreak()], mar_l=0, indent=0)], fill=WHITE, anchor="t", R=edge(BLACK, 38100))], h=IN(1.638)),
    ]))
    out.append(table(n(), "MetricHeader:RevenueEbit", IN(9.579), IN(1.191), IN(3.215), IN(0.500), col_widths=[IN(3.215)], rows=[
        trow([rcell([tpara([trun("Revenue | ", size=PT(8), bold=True, color=BLACK, font=FONT), trun("EBIT margin %", size=PT(8), bold=True, italic=True, color=BLACK, font=FONT), tbreak(), trun("(Revenue = total value chain rev. indexed to $100; EBIT margins for 2024)", size=PT(8), italic=True, color=BLACK, font=FONT)], align="r", mar_l=0, indent=0)], anchor="t")], h=IN(0)),
    ]))
    out.append(table(n(), "RowLabel:Archetypes", IN(0.495), IN(3.457), IN(1.600), IN(3.505), col_widths=[IN(1.600)], rows=[
        trow([rcell([tpara([trun("Archetypes", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=WHITE, anchor="t", R=edge(BLACK, 38100))], h=IN(3.505)),
    ]))


def paint_descriptions(out: list[str], n) -> None:
    for desc in DESCRIPTIONS:
        out.append(text_box(n(), f"Description:{desc.role}", *_xywh(desc.box), [_p(desc.text, color=BLACK)], fill=None, line_color="none", l_ins=0, r_ins=0))


def paint_connectors_and_edge_labels(out: list[str], n) -> None:
    for item in CONNECTORS:
        out.append(connector(n(), item.name, *_xywh(item.box), color=item.color, width=item.width, dashed=item.dashed, arrow=item.arrow, prst=item.prst, flip_h=item.flip_h, flip_v=item.flip_v, rot=item.rot, adj=item.adj))
    for label in EDGE_LABELS:
        out.append(text_box(n(), f"EdgeLabel:{label.text}", *_xywh(label.box), [_p(label.text, size=PT(8), italic=True)], fill=None, line_color="none", anchor="ctr", l_ins=0, r_ins=0))


def paint_metric_labels(out: list[str], n) -> None:
    for metric in METRIC_LABELS:
        out.append(text_box(n(), f"Metric:{metric.role}", *_xywh(metric.box), [_metric_p(metric)], fill=metric.fill, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))
    out.append(text_box(n(), "MetricNote:RevenueAssumption", IN(6.756), IN(4.945), IN(1.665), IN(0.276), [_p("Revenue shown assumes one archetype moves goods", size=PT(8), italic=True)], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "MetricNote:CharterType", IN(10.144), IN(5.647), IN(2.461), IN(0.267), [paragraph([run("Amount dependent on charter type ", size=PT(8), italic=True, color=BLACK, font=FONT), line_break(), run("(e.g., time or voyage) ", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, r_ins=0))


def paint_legend(out: list[str], n) -> None:
    for entry in LEGEND:
        out.append(text_box(n(), "LegendSwatch", IN(entry.swatch_x), IN(1.406), IN(0.200), IN(0.200), [paragraph([], align="ctr", line_spacing=100000)], fill=entry.fill, line_color=BLACK, line_width=3175, anchor="ctr"))
        para_runs = []
        for idx, line in enumerate(entry.label):
            if idx:
                para_runs.append(line_break())
            para_runs.append(run(line, size=PT(8), color=BLACK, font=FONT))
        out.append(text_box(n(), f"LegendLabel:{''.join(entry.label)}", *_xywh(entry.label_box), [paragraph(para_runs, align="ctr" if len(entry.label) == 1 else "l", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))


def _body() -> str:
    out: list[str] = []
    ids = iter(range(100, 2000))
    n = lambda: next(ids)  # noqa: E731 - sequential shape ids
    paint_value_flow_panels(out, n)
    paint_stage_headers(out, n)
    paint_archetype_nodes(out, n)
    paint_row_labels_and_metric_header(out, n)
    paint_descriptions(out, n)
    paint_connectors_and_edge_labels(out, n)
    paint_metric_labels(out, n)
    paint_legend(out, n)
    return "".join(out)


CHROME = Chrome(
    section="Commercial Maritime Value Chain",
    topic="Overview",
    title="Value Chain (Maritime Transport)",
    takeaway="Shipbuilders capture the least value (2-6% EBIT margins); margin expansion likely requires vertical integration.",
)


def render() -> str:
    return body_slide(CHROME, _body())
