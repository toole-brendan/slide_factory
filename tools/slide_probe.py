#!/usr/bin/env python3
"""slide_probe — read-only OOXML inspector for any pptx slide.

Imports a slide module (or opens a built .pptx), parses the emitted <p:sld>
XML, and writes a Markdown + JSON inventory of every shape: identity,
geometry, fills, borders, text, fonts, anchors, insets, native tables,
chart frames, connector arrowheads, group-shape flattened coordinates.

Generic across pptx files — the parser handles canonical OOXML constructs
per infra/ooxml_reference/ooxml_cheat_sheet_pptx.md, not just the constructs these decks happen
to use.

Shared implementation — run it directly from the workspace root; it puts the
workspace root on sys.path so ``deck_core`` resolves, then imports the target
slide module by its dotted package path or opens a .pptx file. Program-agnostic:
the target names the project package (e.g. deck_ddg.slides.<name>).

CLI:
    python deck_core/slide_probe.py <target> [--slide N] [--text-estimate] [--table-fit] [--json] [--all]

Targets:
    A Python module path (e.g. deck_ddg.slides.<name>)
    OR a path to a .pptx file (e.g. path/to/some.pptx)

Output (per program):
    <deck>/reports/slide_probe/<name>.md
    <deck>/reports/slide_probe/<name>.json
    (re-probing a slide replaces its files; runs do not stack)

This script is a pure read-only inspector: it reports facts only. It does not
lint, validate, score, or pass/fail a slide. The optional --text-estimate and
--table-fit flags add extra informational sections to the report (per-text-box
wrap/height estimates and estimated native-table row-height info); they never
fail or rewrite anything.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import importlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# The probe imports a few deck_core constants (namespaces, slide size) and carries
# its own self-contained text-width / row-height model (below) — it is the only
# remaining consumer of that model. parents[1] of …/deck_core/slide_probe.py is the
# workspace root (which holds the deck_core package).
_CORE_ROOT = str(Path(__file__).resolve().parents[1])
if _CORE_ROOT not in sys.path:
    sys.path.insert(0, _CORE_ROOT)
from deck_core.ooxml import NS_MAP as NS  # noqa: E402
from deck_core.layout import SLIDE_W as DEFAULT_SLIDE_W, SLIDE_H as DEFAULT_SLIDE_H  # noqa: E402


# ── Constants ───────────────────────────────────────────────────────────

EMU_PER_INCH = 914_400
EMU_PER_POINT = 12_700
# DEFAULT_SLIDE_W / DEFAULT_SLIDE_H imported from deck_core.style (above).

# Default bodyPr insets per cheat sheet §12 (Office defaults).
DEFAULT_LINS = 91_440   # 0.1 in
DEFAULT_RINS = 91_440
DEFAULT_TINS = 45_720   # 0.05 in
DEFAULT_BINS = 45_720

# Locked chrome sp_ids (deck_core.style SP_ID_*). Body slides (slideLayout4)
# auto-number, so there is no PageNumber shape.
CHROME_SP_IDS = {2: "Breadcrumb", 3: "Title", 4: "PrelimChip",
                 9999: "Source"}

# House body box (single source of truth = deck_core.style.BODY). Used by the
# optional --table-fit info section to report a table's estimated honest bottom
# against the body floor.
from deck_core.layout import (  # noqa: E402
    BODY_X, BODY_Y, BODY_CX, BODY_CY, BODY_R, BODY_B,
)

# BODY_* (above) is used by the optional --table-fit info section to report a
# table's estimated honest bottom against the body floor — informational only.

# NS (prefix -> URI map) imported from deck_core.ooxml as NS_MAP (above).

# qname helpers — ET uses {namespace}tag form internally.
def _q(prefix: str, local: str) -> str:
    return f"{{{NS[prefix]}}}{local}"

P_SP        = _q("p", "sp")
P_CXNSP     = _q("p", "cxnSp")
P_GRPSP     = _q("p", "grpSp")
P_PIC       = _q("p", "pic")
P_GFRAME    = _q("p", "graphicFrame")
P_SPTREE    = _q("p", "spTree")
P_NVSPPR    = _q("p", "nvSpPr")
P_NVCXNSPPR = _q("p", "nvCxnSpPr")
P_NVPICPR   = _q("p", "nvPicPr")
P_NVGFPR    = _q("p", "nvGraphicFramePr")
P_NVGRPSPPR = _q("p", "nvGrpSpPr")
P_CNVPR     = _q("p", "cNvPr")
P_NVPR      = _q("p", "nvPr")
P_PH        = _q("p", "ph")
P_SPPR      = _q("p", "spPr")
P_GRPSPPR   = _q("p", "grpSpPr")
P_TXBODY    = _q("p", "txBody")
P_BLIPFILL  = _q("p", "blipFill")
P_XFRM_PFR  = _q("p", "xfrm")  # graphicFrame uses p:xfrm, not a:xfrm

A_XFRM      = _q("a", "xfrm")
A_OFF       = _q("a", "off")
A_EXT       = _q("a", "ext")
A_CHOFF     = _q("a", "chOff")
A_CHEXT     = _q("a", "chExt")
A_PRSTGEOM  = _q("a", "prstGeom")
A_CUSTGEOM  = _q("a", "custGeom")
A_PATHLST   = _q("a", "pathLst")
A_PATH      = _q("a", "path")
A_AVLST     = _q("a", "avLst")
A_GD        = _q("a", "gd")
A_SOLIDFILL = _q("a", "solidFill")
A_NOFILL    = _q("a", "noFill")
A_GRADFILL  = _q("a", "gradFill")
A_BLIPFILL  = _q("a", "blipFill")
A_PATTFILL  = _q("a", "pattFill")
A_SRGBCLR   = _q("a", "srgbClr")
A_SCHEMECLR = _q("a", "schemeClr")
A_LN        = _q("a", "ln")
A_PRSTDASH  = _q("a", "prstDash")
A_HEADEND   = _q("a", "headEnd")
A_TAILEND   = _q("a", "tailEnd")
A_BODYPR    = _q("a", "bodyPr")
A_P         = _q("a", "p")
A_PPR       = _q("a", "pPr")
A_R         = _q("a", "r")
A_RPR       = _q("a", "rPr")
A_T         = _q("a", "t")
A_LATIN     = _q("a", "latin")
A_LNSPC     = _q("a", "lnSpc")
A_SPCPCT    = _q("a", "spcPct")
A_SPCPTS    = _q("a", "spcPts")
A_BUCHAR    = _q("a", "buChar")
A_BUAUTONUM = _q("a", "buAutoNum")
A_BUNONE    = _q("a", "buNone")
A_ENDPARARPR= _q("a", "endParaRPr")
A_BLIP      = _q("a", "blip")
A_SRCRECT   = _q("a", "srcRect")
A_GRAPHIC   = _q("a", "graphic")
A_GRAPHICDATA = _q("a", "graphicData")
A_TBL       = _q("a", "tbl")
A_TBLPR     = _q("a", "tblPr")
A_TBLGRID   = _q("a", "tblGrid")
A_GRIDCOL   = _q("a", "gridCol")
A_TR        = _q("a", "tr")
A_TC        = _q("a", "tc")
A_TCPR      = _q("a", "tcPr")
A_LNL       = _q("a", "lnL")
A_LNR       = _q("a", "lnR")
A_LNT       = _q("a", "lnT")
A_LNB       = _q("a", "lnB")
A_TXBODY    = _q("a", "txBody")
A_STCXN     = _q("a", "stCxn")
A_ENDCXN    = _q("a", "endCxn")
A_OFF_      = _q("a", "off")

R_EMBED     = _q("r", "embed")
R_LINK      = _q("r", "link")
R_ID        = _q("r", "id")

C_CHART     = _q("c", "chart")
CX_CHART    = _q("cx", "chart")

MC_ALTERNATE = _q("mc", "AlternateContent")
MC_CHOICE    = _q("mc", "Choice")
MC_FALLBACK  = _q("mc", "Fallback")

# Graphic-frame URIs that discriminate chart vs chartEx vs table vs OLE.
URI_CHART   = "http://schemas.openxmlformats.org/drawingml/2006/chart"
URI_CHARTEX = "http://schemas.microsoft.com/office/drawing/2014/chartex"
URI_TABLE   = "http://schemas.openxmlformats.org/drawingml/2006/table"
URI_OLE     = "http://schemas.openxmlformats.org/presentationml/2006/ole"
URI_DIAGRAM = "http://schemas.openxmlformats.org/drawingml/2006/diagram"

# p:oleObj sits inside a:graphicData (sometimes wrapped in mc:AlternateContent).
P_OLEOBJ    = _q("p", "oleObj")


# ── Dataclasses ─────────────────────────────────────────────────────────


@dataclass(frozen=True)
class TextRun:
    text: str
    font: str | None
    size_pt: float | None
    bold: bool | None
    italic: bool | None
    underline: str | None
    color: str | None       # hex or "scheme:accent1" or None


@dataclass(frozen=True)
class Paragraph:
    runs: tuple[TextRun, ...]
    algn: str | None
    ln_spc_pct: float | None   # e.g. 115.0 for 115%
    ln_spc_pts: float | None   # alternative to pct
    bullet_char: str | None
    bullet_autonum: str | None
    level: int


@dataclass(frozen=True)
class BodyPr:
    anchor: str | None
    wrap: str | None
    l_ins: int
    r_ins: int
    t_ins: int
    b_ins: int
    rot: int | None


@dataclass(frozen=True)
class TextBody:
    body_pr: BodyPr
    paragraphs: tuple[Paragraph, ...]
    plain_text: str   # joined text content for quick inspection


@dataclass(frozen=True)
class Geometry:
    x: int | None
    y: int | None
    cx: int | None
    cy: int | None
    # Flattened coordinates differ from raw when the shape lives inside a group.
    x_abs: int | None = None
    y_abs: int | None = None
    # Transform metadata on a:xfrm / p:xfrm. The absolute box reported above is
    # axis-aligned and ignores rotation; consumers wanting the rotated visual
    # footprint should account for these explicitly.
    rot_deg: float | None = None    # degrees (a:xfrm/@rot, in 60_000ths/deg)
    flip_h: bool = False            # a:xfrm/@flipH
    flip_v: bool = False            # a:xfrm/@flipV


@dataclass(frozen=True)
class Fill:
    kind: str          # "solid" | "scheme" | "none" | "gradient" | "blip" | "pattern" | "unset"
    value: str | None  # hex (solid) or scheme name (scheme) or None
    blip_embed_rid: str | None = None   # populated when kind="blip" via a:blip/@r:embed
    blip_link_rid: str | None = None    # populated when kind="blip" via a:blip/@r:link


@dataclass(frozen=True)
class EndCap:
    type: str | None
    w: str | None
    len_: str | None


@dataclass(frozen=True)
class Line:
    kind: str           # "solid" | "none" | "unset" | "other"
    color: str | None   # hex or scheme name
    w_emu: int | None
    dash: str | None
    head_end: EndCap | None
    tail_end: EndCap | None


@dataclass(frozen=True)
class TableCell:
    row: int
    col: int
    grid_span: int        # 1 unless horizontally merged
    row_span: int         # 1 unless vertically merged
    h_merge: bool         # merged-into marker (cell continues another cell horizontally)
    v_merge: bool         # merged-into marker (cell continues another cell vertically)
    fill: Fill
    border_left: Line
    border_right: Line
    border_top: Line
    border_bottom: Line
    mar_l: int | None
    mar_r: int | None
    mar_t: int | None
    mar_b: int | None
    anchor: str | None
    text_body: TextBody | None


@dataclass(frozen=True)
class TableProbe:
    grid_cols_emu: tuple[int, ...]
    row_heights_emu: tuple[int, ...]
    cells: tuple[TableCell, ...]


@dataclass(frozen=True)
class ChartProbe:
    rid: str | None
    kind: str             # "chart" | "chartEx" | "unknown"
    resolved_path: str | None   # populated only in pptx-file mode


@dataclass(frozen=True)
class PictureProbe:
    embed_rid: str | None
    link_rid: str | None
    resolved_path: str | None
    crop_l_pct: float | None
    crop_r_pct: float | None
    crop_t_pct: float | None
    crop_b_pct: float | None


@dataclass(frozen=True)
class OleProbe:
    """Embedded object inside a <p:graphicFrame>.

    Carries progId so consumers can identify the embed type. Common progIds:
    "Excel.Sheet.12", "thinkcell.Chart.X" (the X varies by version),
    "Word.Document.12", "Equation.3". Thinkcell's classic embed is OLE
    with a progId starting with "thinkcell."; their newer custom URI embed
    is reported as kind="graphicFrame.unknown" with frame_uri populated
    and is_thinkcell=True.
    """
    prog_id: str | None
    rid: str | None
    resolved_path: str | None
    show_as_icon: bool
    is_thinkcell: bool


@dataclass(frozen=True)
class CustGeomSummary:
    path_count: int
    cmd_counts: dict[str, int]   # moveTo / lnTo / quadBezTo / cubicBezTo / arcTo / close


@dataclass(frozen=True)
class ShapeProbe:
    z: int
    kind: str             # "sp" | "cxnSp" | "graphicFrame.chart" | "graphicFrame.chartEx" | "graphicFrame.table" | "graphicFrame.unknown" | "pic" | "grpSp" | "unknown"
    sp_id: int | None
    name: str | None
    chrome_role: str | None     # "Breadcrumb" / "Title" / ... if sp_id matches CHROME_SP_IDS
    ph_type: str | None
    ph_idx: str | None
    is_placeholder: bool
    geometry: Geometry
    fill: Fill
    line: Line
    prst: str | None
    prst_avlst: dict[str, str] | None
    custgeom: CustGeomSummary | None
    text_body: TextBody | None
    table: TableProbe | None
    chart: ChartProbe | None
    picture: PictureProbe | None
    ole: OleProbe | None                # populated when kind == "graphicFrame.ole"
    frame_uri: str | None               # a:graphicData/@uri for any graphicFrame
    is_thinkcell: bool                  # progId or URI matches thinkcell
    cxn_start: tuple[int, int] | None   # (target sp_id, target idx)
    cxn_end: tuple[int, int] | None
    parent_group_id: int | None         # sp_id of nearest enclosing p:grpSp, or None
    group_scale_x: float | None
    group_scale_y: float | None
    raw_tag: str | None                 # populated when kind == "unknown"


# ── Helpers ─────────────────────────────────────────────────────────────


def _emu_to_in(emu: int | None) -> float | None:
    if emu is None:
        return None
    return round(emu / EMU_PER_INCH, 3)


def _emu_to_pt(emu: int | None) -> float | None:
    if emu is None:
        return None
    return round(emu / EMU_PER_POINT, 2)


def _parse_int_attr(el: ET.Element | None, attr: str) -> int | None:
    if el is None:
        return None
    v = el.get(attr)
    if v is None:
        return None
    try:
        return int(v)
    except ValueError:
        return None


def _parse_bool_attr(el: ET.Element | None, attr: str) -> bool | None:
    if el is None:
        return None
    v = el.get(attr)
    if v is None:
        return None
    return v not in ("0", "false", "False")


def _parse_fill(parent: ET.Element | None) -> Fill:
    """Look at the first fill-bearing child of `parent` (a:solidFill / a:noFill / ...)."""
    if parent is None:
        return Fill(kind="unset", value=None)
    for child in list(parent):
        tag = child.tag
        if tag == A_SOLIDFILL:
            srgb = child.find(A_SRGBCLR)
            if srgb is not None and srgb.get("val"):
                return Fill(kind="solid", value=srgb.get("val"))
            scheme = child.find(A_SCHEMECLR)
            if scheme is not None and scheme.get("val"):
                return Fill(kind="scheme", value=scheme.get("val"))
            return Fill(kind="solid", value=None)
        if tag == A_NOFILL:
            return Fill(kind="none", value=None)
        if tag == A_GRADFILL:
            return Fill(kind="gradient", value=None)
        if tag == A_BLIPFILL:
            blip = child.find(A_BLIP)
            embed = blip.get(R_EMBED) if blip is not None else None
            link = blip.get(R_LINK) if blip is not None else None
            return Fill(kind="blip", value=None,
                        blip_embed_rid=embed, blip_link_rid=link)
        if tag == A_PATTFILL:
            return Fill(kind="pattern", value=None)
    return Fill(kind="unset", value=None)


def _parse_end_cap(el: ET.Element | None) -> EndCap | None:
    if el is None:
        return None
    return EndCap(type=el.get("type"), w=el.get("w"), len_=el.get("len"))


def _parse_line(parent: ET.Element | None) -> Line:
    """Look for an `a:ln` child under `parent` and decode it."""
    if parent is None:
        return Line(kind="unset", color=None, w_emu=None, dash=None,
                    head_end=None, tail_end=None)
    ln = parent.find(A_LN)
    if ln is None:
        return Line(kind="unset", color=None, w_emu=None, dash=None,
                    head_end=None, tail_end=None)
    w_emu = _parse_int_attr(ln, "w")
    # nested fill determines kind/color
    if ln.find(A_NOFILL) is not None:
        kind = "none"
        color = None
    else:
        fill = _parse_fill(ln)
        if fill.kind == "solid":
            kind = "solid"; color = fill.value
        elif fill.kind == "scheme":
            kind = "solid"; color = f"scheme:{fill.value}"
        elif fill.kind == "unset":
            kind = "unset"; color = None
        else:
            kind = "other"; color = None
    dash_el = ln.find(A_PRSTDASH)
    dash = dash_el.get("val") if dash_el is not None else None
    return Line(
        kind=kind, color=color, w_emu=w_emu, dash=dash,
        head_end=_parse_end_cap(ln.find(A_HEADEND)),
        tail_end=_parse_end_cap(ln.find(A_TAILEND)),
    )


def _parse_xfrm(xfrm: ET.Element | None) -> tuple[int | None, int | None, int | None, int | None, float | None, bool, bool]:
    """Return (x, y, cx, cy, rot_deg, flip_h, flip_v) from an a:xfrm / p:xfrm element."""
    if xfrm is None:
        return (None, None, None, None, None, False, False)
    off = xfrm.find(A_OFF)
    ext = xfrm.find(A_EXT)
    x = _parse_int_attr(off, "x")
    y = _parse_int_attr(off, "y")
    cx = _parse_int_attr(ext, "cx")
    cy = _parse_int_attr(ext, "cy")
    rot_raw = xfrm.get("rot")
    rot_deg: float | None = None
    if rot_raw is not None:
        try:
            rot_deg = round(int(rot_raw) / 60000.0, 2)
        except ValueError:
            rot_deg = None
    flip_h = xfrm.get("flipH") in ("1", "true")
    flip_v = xfrm.get("flipV") in ("1", "true")
    return (x, y, cx, cy, rot_deg, flip_h, flip_v)


def _parse_geometry(sp_pr: ET.Element | None) -> Geometry:
    if sp_pr is None:
        return Geometry(x=None, y=None, cx=None, cy=None)
    xfrm = sp_pr.find(A_XFRM)
    x, y, cx, cy, rot, fh, fv = _parse_xfrm(xfrm)
    return Geometry(x=x, y=y, cx=cx, cy=cy, rot_deg=rot, flip_h=fh, flip_v=fv)


def _parse_prst(sp_pr: ET.Element | None) -> tuple[str | None, dict[str, str] | None, CustGeomSummary | None]:
    if sp_pr is None:
        return (None, None, None)
    prst_el = sp_pr.find(A_PRSTGEOM)
    if prst_el is not None:
        prst = prst_el.get("prst")
        avlst: dict[str, str] = {}
        av = prst_el.find(A_AVLST)
        if av is not None:
            for gd in av.findall(A_GD):
                n = gd.get("name")
                f = gd.get("fmla")
                if n is not None and f is not None:
                    avlst[n] = f
        return (prst, avlst or None, None)
    cust = sp_pr.find(A_CUSTGEOM)
    if cust is not None:
        path_lst = cust.find(A_PATHLST)
        paths = path_lst.findall(A_PATH) if path_lst is not None else []
        cmd_counts: dict[str, int] = {}
        for p in paths:
            for c in list(p):
                local = c.tag.split("}", 1)[-1]
                cmd_counts[local] = cmd_counts.get(local, 0) + 1
        return (None, None, CustGeomSummary(path_count=len(paths), cmd_counts=cmd_counts))
    return (None, None, None)


def _parse_color_in_rpr(rpr: ET.Element | None) -> str | None:
    if rpr is None:
        return None
    sf = rpr.find(A_SOLIDFILL)
    if sf is None:
        return None
    srgb = sf.find(A_SRGBCLR)
    if srgb is not None and srgb.get("val"):
        return srgb.get("val")
    scheme = sf.find(A_SCHEMECLR)
    if scheme is not None and scheme.get("val"):
        return f"scheme:{scheme.get('val')}"
    return None


def _parse_run(r: ET.Element) -> TextRun:
    rpr = r.find(A_RPR)
    t_el = r.find(A_T)
    text = t_el.text if (t_el is not None and t_el.text is not None) else ""
    size_pt: float | None = None
    bold: bool | None = None
    italic: bool | None = None
    underline: str | None = None
    font: str | None = None
    if rpr is not None:
        sz = rpr.get("sz")
        if sz is not None:
            try:
                size_pt = round(int(sz) / 100.0, 2)
            except ValueError:
                size_pt = None
        bold = _parse_bool_attr(rpr, "b")
        italic = _parse_bool_attr(rpr, "i")
        underline = rpr.get("u")
        latin = rpr.find(A_LATIN)
        if latin is not None:
            font = latin.get("typeface")
    color = _parse_color_in_rpr(rpr)
    return TextRun(text=text, font=font, size_pt=size_pt, bold=bold,
                   italic=italic, underline=underline, color=color)


def _parse_paragraph(p: ET.Element) -> Paragraph:
    ppr = p.find(A_PPR)
    algn = None
    ln_spc_pct: float | None = None
    ln_spc_pts: float | None = None
    bullet_char: str | None = None
    bullet_autonum: str | None = None
    level = 0
    if ppr is not None:
        algn = ppr.get("algn")
        lvl = ppr.get("lvl")
        if lvl is not None:
            try:
                level = int(lvl)
            except ValueError:
                level = 0
        lspc = ppr.find(A_LNSPC)
        if lspc is not None:
            pct = lspc.find(A_SPCPCT)
            pts = lspc.find(A_SPCPTS)
            if pct is not None and pct.get("val"):
                try:
                    ln_spc_pct = round(int(pct.get("val")) / 1000.0, 2)
                except ValueError:
                    pass
            if pts is not None and pts.get("val"):
                try:
                    ln_spc_pts = round(int(pts.get("val")) / 100.0, 2)
                except ValueError:
                    pass
        bu_char_el = ppr.find(A_BUCHAR)
        if bu_char_el is not None:
            bullet_char = bu_char_el.get("char")
        bu_auto = ppr.find(A_BUAUTONUM)
        if bu_auto is not None:
            bullet_autonum = bu_auto.get("type")
    runs = tuple(_parse_run(r) for r in p.findall(A_R))
    return Paragraph(runs=runs, algn=algn, ln_spc_pct=ln_spc_pct,
                     ln_spc_pts=ln_spc_pts, bullet_char=bullet_char,
                     bullet_autonum=bullet_autonum, level=level)


def _with_default(v: int | None, default: int) -> int:
    """Return v when present (including the int 0); otherwise default.

    `v or default` silently coerces explicit zero into the default — wrong
    for OOXML attributes like lIns="0" where 0 is a meaningful value
    distinct from "attribute omitted, inherit Office default".
    """
    return v if v is not None else default


def _parse_body_pr(bp: ET.Element | None) -> BodyPr:
    if bp is None:
        return BodyPr(anchor=None, wrap=None, l_ins=DEFAULT_LINS,
                      r_ins=DEFAULT_RINS, t_ins=DEFAULT_TINS,
                      b_ins=DEFAULT_BINS, rot=None)
    return BodyPr(
        anchor=bp.get("anchor"),
        wrap=bp.get("wrap"),
        l_ins=_with_default(_parse_int_attr(bp, "lIns"), DEFAULT_LINS),
        r_ins=_with_default(_parse_int_attr(bp, "rIns"), DEFAULT_RINS),
        t_ins=_with_default(_parse_int_attr(bp, "tIns"), DEFAULT_TINS),
        b_ins=_with_default(_parse_int_attr(bp, "bIns"), DEFAULT_BINS),
        rot=_parse_int_attr(bp, "rot"),
    )


def _parse_text_body(tx: ET.Element | None) -> TextBody | None:
    if tx is None:
        return None
    body_pr = _parse_body_pr(tx.find(A_BODYPR))
    paragraphs = tuple(_parse_paragraph(p) for p in tx.findall(A_P))
    plain = "\n".join(
        "".join(r.text for r in para.runs)
        for para in paragraphs
    )
    return TextBody(body_pr=body_pr, paragraphs=paragraphs, plain_text=plain)


def _parse_table(tbl: ET.Element) -> TableProbe:
    grid = tbl.find(A_TBLGRID)
    cols = tuple(_parse_int_attr(gc, "w") or 0
                 for gc in (grid.findall(A_GRIDCOL) if grid is not None else []))
    row_heights: list[int] = []
    cells: list[TableCell] = []
    for r_idx, tr in enumerate(tbl.findall(A_TR)):
        row_heights.append(_parse_int_attr(tr, "h") or 0)
        for c_idx, tc in enumerate(tr.findall(A_TC)):
            tc_pr = tc.find(A_TCPR)
            cell_fill = _parse_fill(tc_pr) if tc_pr is not None else Fill(kind="unset", value=None)
            border_l = _parse_table_border(tc_pr.find(A_LNL) if tc_pr is not None else None)
            border_r = _parse_table_border(tc_pr.find(A_LNR) if tc_pr is not None else None)
            border_t = _parse_table_border(tc_pr.find(A_LNT) if tc_pr is not None else None)
            border_b = _parse_table_border(tc_pr.find(A_LNB) if tc_pr is not None else None)
            cells.append(TableCell(
                row=r_idx, col=c_idx,
                grid_span=int(tc.get("gridSpan", "1")),
                row_span=int(tc.get("rowSpan", "1")),
                h_merge=tc.get("hMerge") == "1",
                v_merge=tc.get("vMerge") == "1",
                fill=cell_fill,
                border_left=border_l,
                border_right=border_r,
                border_top=border_t,
                border_bottom=border_b,
                mar_l=_parse_int_attr(tc_pr, "marL"),
                mar_r=_parse_int_attr(tc_pr, "marR"),
                mar_t=_parse_int_attr(tc_pr, "marT"),
                mar_b=_parse_int_attr(tc_pr, "marB"),
                anchor=(tc_pr.get("anchor") if tc_pr is not None else None),
                text_body=_parse_text_body(tc.find(A_TXBODY)),
            ))
    return TableProbe(grid_cols_emu=cols, row_heights_emu=tuple(row_heights),
                      cells=tuple(cells))


def _parse_table_border(ln_el: ET.Element | None) -> Line:
    """Parse an a:lnL/lnR/lnT/lnB element (the element itself is the border)."""
    if ln_el is None:
        return Line(kind="unset", color=None, w_emu=None, dash=None,
                    head_end=None, tail_end=None)
    w_emu = _parse_int_attr(ln_el, "w")
    if ln_el.find(A_NOFILL) is not None:
        return Line(kind="none", color=None, w_emu=w_emu, dash=None,
                    head_end=None, tail_end=None)
    fill = _parse_fill(ln_el)
    if fill.kind == "solid":
        return Line(kind="solid", color=fill.value, w_emu=w_emu, dash=None,
                    head_end=None, tail_end=None)
    if fill.kind == "scheme":
        return Line(kind="solid", color=f"scheme:{fill.value}", w_emu=w_emu,
                    dash=None, head_end=None, tail_end=None)
    return Line(kind="unset", color=None, w_emu=w_emu, dash=None,
                head_end=None, tail_end=None)


def _parse_placeholder(nv_sp_pr: ET.Element | None) -> tuple[str | None, str | None]:
    if nv_sp_pr is None:
        return (None, None)
    nv_pr = nv_sp_pr.find(P_NVPR)
    if nv_pr is None:
        return (None, None)
    ph = nv_pr.find(P_PH)
    if ph is None:
        return (None, None)
    return (ph.get("type"), ph.get("idx"))


def _identity(parent: ET.Element, container_tag: str) -> tuple[int | None, str | None]:
    container = parent.find(container_tag)
    if container is None:
        return (None, None)
    cnv = container.find(P_CNVPR)
    if cnv is None:
        return (None, None)
    raw_id = cnv.get("id")
    sp_id: int | None = None
    try:
        sp_id = int(raw_id) if raw_id is not None else None
    except ValueError:
        sp_id = None
    return (sp_id, cnv.get("name"))


# ── Shape parsers ───────────────────────────────────────────────────────


def _parse_sp(el: ET.Element, *, z: int, parent_group_id: int | None,
              scale_x: float, scale_y: float, group_off: tuple[int, int],
              group_ch_off: tuple[int, int]) -> ShapeProbe:
    sp_id, name = _identity(el, P_NVSPPR)
    ph_type, ph_idx = _parse_placeholder(el.find(P_NVSPPR))
    sp_pr = el.find(P_SPPR)
    geom = _parse_geometry(sp_pr)
    geom = _apply_group_transform(geom, parent_group_id, scale_x, scale_y, group_off, group_ch_off)
    fill = _parse_fill(sp_pr)
    line = _parse_line(sp_pr)
    prst, prst_av, custgeom = _parse_prst(sp_pr)
    text_body = _parse_text_body(el.find(P_TXBODY))
    chrome = CHROME_SP_IDS.get(sp_id) if sp_id is not None else None
    return ShapeProbe(
        z=z, kind="sp", sp_id=sp_id, name=name, chrome_role=chrome,
        ph_type=ph_type, ph_idx=ph_idx, is_placeholder=ph_type is not None,
        geometry=geom, fill=fill, line=line, prst=prst, prst_avlst=prst_av,
        custgeom=custgeom, text_body=text_body, table=None, chart=None,
        picture=None, ole=None, frame_uri=None, is_thinkcell=False,
        cxn_start=None, cxn_end=None,
        parent_group_id=parent_group_id,
        group_scale_x=(scale_x if parent_group_id else None),
        group_scale_y=(scale_y if parent_group_id else None),
        raw_tag=None,
    )


def _parse_cxn_sp(el: ET.Element, *, z: int, parent_group_id: int | None,
                  scale_x: float, scale_y: float, group_off: tuple[int, int],
                  group_ch_off: tuple[int, int]) -> ShapeProbe:
    sp_id, name = _identity(el, P_NVCXNSPPR)
    sp_pr = el.find(P_SPPR)
    geom = _parse_geometry(sp_pr)
    geom = _apply_group_transform(geom, parent_group_id, scale_x, scale_y, group_off, group_ch_off)
    fill = _parse_fill(sp_pr)
    line = _parse_line(sp_pr)
    prst, prst_av, custgeom = _parse_prst(sp_pr)
    # Connection endpoints live inside p:nvCxnSpPr/p:cNvCxnSpPr
    nv = el.find(P_NVCXNSPPR)
    cxn_start = None
    cxn_end = None
    if nv is not None:
        # a:stCxn and a:endCxn live under p:cNvCxnSpPr (a sibling of p:cNvPr)
        cnv_cxn = nv.find(_q("p", "cNvCxnSpPr"))
        if cnv_cxn is not None:
            st = cnv_cxn.find(A_STCXN)
            if st is not None:
                cxn_start = (_parse_int_attr(st, "id") or 0,
                             _parse_int_attr(st, "idx") or 0)
            en = cnv_cxn.find(A_ENDCXN)
            if en is not None:
                cxn_end = (_parse_int_attr(en, "id") or 0,
                           _parse_int_attr(en, "idx") or 0)
    chrome = CHROME_SP_IDS.get(sp_id) if sp_id is not None else None
    return ShapeProbe(
        z=z, kind="cxnSp", sp_id=sp_id, name=name, chrome_role=chrome,
        ph_type=None, ph_idx=None, is_placeholder=False,
        geometry=geom, fill=fill, line=line, prst=prst, prst_avlst=prst_av,
        custgeom=custgeom, text_body=None, table=None, chart=None,
        picture=None, ole=None, frame_uri=None, is_thinkcell=False,
        cxn_start=cxn_start, cxn_end=cxn_end,
        parent_group_id=parent_group_id,
        group_scale_x=(scale_x if parent_group_id else None),
        group_scale_y=(scale_y if parent_group_id else None),
        raw_tag=None,
    )


def _parse_pic(el: ET.Element, *, z: int, parent_group_id: int | None,
               scale_x: float, scale_y: float, group_off: tuple[int, int],
               group_ch_off: tuple[int, int], rels: dict[str, str]) -> ShapeProbe:
    sp_id, name = _identity(el, P_NVPICPR)
    sp_pr = el.find(P_SPPR)
    geom = _parse_geometry(sp_pr)
    geom = _apply_group_transform(geom, parent_group_id, scale_x, scale_y, group_off, group_ch_off)
    fill = _parse_fill(sp_pr)
    line = _parse_line(sp_pr)
    prst, prst_av, custgeom = _parse_prst(sp_pr)
    blip_fill = el.find(P_BLIPFILL)
    embed_rid = link_rid = resolved = None
    crop_l = crop_r = crop_t = crop_b = None
    if blip_fill is not None:
        blip = blip_fill.find(A_BLIP)
        if blip is not None:
            embed_rid = blip.get(R_EMBED)
            link_rid = blip.get(R_LINK)
            if embed_rid and rels:
                resolved = rels.get(embed_rid)
        src = blip_fill.find(A_SRCRECT)
        if src is not None:
            def _pct(name: str) -> float | None:
                v = _parse_int_attr(src, name)
                return round(v / 1000.0, 3) if v is not None else None
            crop_l, crop_r, crop_t, crop_b = (_pct("l"), _pct("r"), _pct("t"), _pct("b"))
    pic = PictureProbe(embed_rid=embed_rid, link_rid=link_rid,
                       resolved_path=resolved, crop_l_pct=crop_l,
                       crop_r_pct=crop_r, crop_t_pct=crop_t, crop_b_pct=crop_b)
    chrome = CHROME_SP_IDS.get(sp_id) if sp_id is not None else None
    return ShapeProbe(
        z=z, kind="pic", sp_id=sp_id, name=name, chrome_role=chrome,
        ph_type=None, ph_idx=None, is_placeholder=False,
        geometry=geom, fill=fill, line=line, prst=prst, prst_avlst=prst_av,
        custgeom=custgeom, text_body=None, table=None, chart=None,
        picture=pic, ole=None, frame_uri=None, is_thinkcell=False,
        cxn_start=None, cxn_end=None,
        parent_group_id=parent_group_id,
        group_scale_x=(scale_x if parent_group_id else None),
        group_scale_y=(scale_y if parent_group_id else None),
        raw_tag=None,
    )


def _parse_graphic_frame(el: ET.Element, *, z: int, parent_group_id: int | None,
                         scale_x: float, scale_y: float, group_off: tuple[int, int],
                         group_ch_off: tuple[int, int], rels: dict[str, str]) -> ShapeProbe:
    sp_id, name = _identity(el, P_NVGFPR)
    # graphicFrame uses p:xfrm (not a:xfrm) and has no p:spPr
    pxfrm = el.find(P_XFRM_PFR)
    x, y, cx, cy, rot, fh, fv = _parse_xfrm(pxfrm)
    geom = Geometry(x=x, y=y, cx=cx, cy=cy, rot_deg=rot, flip_h=fh, flip_v=fv)
    geom = _apply_group_transform(geom, parent_group_id, scale_x, scale_y, group_off, group_ch_off)
    graphic = el.find(A_GRAPHIC)
    table_probe: TableProbe | None = None
    chart_probe: ChartProbe | None = None
    ole_probe: OleProbe | None = None
    frame_uri: str | None = None
    kind = "graphicFrame.unknown"
    is_thinkcell = False
    if graphic is not None:
        gd = graphic.find(A_GRAPHICDATA)
        if gd is not None:
            uri = gd.get("uri") or ""
            frame_uri = uri or None
            # Thinkcell sometimes uses a custom graphicData URI (their newer
            # embed mechanism). Detect via substring match on the URI.
            if uri and ("think-cell" in uri.lower() or "thinkcell" in uri.lower()):
                is_thinkcell = True
            if uri == URI_TABLE:
                tbl = gd.find(A_TBL)
                if tbl is not None:
                    table_probe = _parse_table(tbl)
                    kind = "graphicFrame.table"
            elif uri == URI_CHART:
                ch = gd.find(C_CHART)
                rid = ch.get(R_ID) if ch is not None else None
                chart_probe = ChartProbe(
                    rid=rid, kind="chart",
                    resolved_path=rels.get(rid) if (rid and rels) else None,
                )
                kind = "graphicFrame.chart"
            elif uri == URI_CHARTEX:
                ch = gd.find(CX_CHART)
                rid = ch.get(R_ID) if ch is not None else None
                chart_probe = ChartProbe(
                    rid=rid, kind="chartEx",
                    resolved_path=rels.get(rid) if (rid and rels) else None,
                )
                kind = "graphicFrame.chartEx"
            elif uri == URI_OLE:
                # p:oleObj can sit directly under a:graphicData OR be wrapped in
                # mc:AlternateContent (PowerPoint sometimes does that for
                # backward-compat). Search recursively for the first p:oleObj.
                ole_el = gd.find(f".//{P_OLEOBJ}")
                if ole_el is not None:
                    prog_id = ole_el.get("progId")
                    ole_rid = ole_el.get(R_ID)
                    show_icon = ole_el.get("showAsIcon") in ("1", "true")
                    tc = bool(prog_id and prog_id.lower().startswith("thinkcell"))
                    if tc:
                        is_thinkcell = True
                    ole_probe = OleProbe(
                        prog_id=prog_id, rid=ole_rid,
                        resolved_path=(rels.get(ole_rid) if (ole_rid and rels) else None),
                        show_as_icon=show_icon, is_thinkcell=tc,
                    )
                kind = "graphicFrame.ole"
            elif uri == URI_DIAGRAM:
                kind = "graphicFrame.diagram"
    chrome = CHROME_SP_IDS.get(sp_id) if sp_id is not None else None
    return ShapeProbe(
        z=z, kind=kind, sp_id=sp_id, name=name, chrome_role=chrome,
        ph_type=None, ph_idx=None, is_placeholder=False,
        geometry=geom, fill=Fill(kind="unset", value=None),
        line=Line(kind="unset", color=None, w_emu=None, dash=None,
                  head_end=None, tail_end=None),
        prst=None, prst_avlst=None, custgeom=None,
        text_body=None, table=table_probe, chart=chart_probe,
        picture=None, ole=ole_probe, frame_uri=frame_uri,
        is_thinkcell=is_thinkcell,
        cxn_start=None, cxn_end=None,
        parent_group_id=parent_group_id,
        group_scale_x=(scale_x if parent_group_id else None),
        group_scale_y=(scale_y if parent_group_id else None),
        raw_tag=None,
    )


def _apply_group_transform(geom: Geometry, parent_group_id: int | None,
                           scale_x: float, scale_y: float,
                           group_off: tuple[int, int],
                           group_ch_off: tuple[int, int]) -> Geometry:
    if parent_group_id is None or geom.x is None or geom.y is None:
        return dataclasses.replace(geom, x_abs=geom.x, y_abs=geom.y)
    abs_x = int(group_off[0] + (geom.x - group_ch_off[0]) * scale_x)
    abs_y = int(group_off[1] + (geom.y - group_ch_off[1]) * scale_y)
    return dataclasses.replace(geom, x_abs=abs_x, y_abs=abs_y)


def _walk_sp_tree(parent: ET.Element, *, parent_group_id: int | None,
                  scale_x: float, scale_y: float,
                  group_off: tuple[int, int], group_ch_off: tuple[int, int],
                  rels: dict[str, str], counter: list[int]) -> list[ShapeProbe]:
    out: list[ShapeProbe] = []
    for child in list(parent):
        tag = child.tag
        if tag in (P_NVGRPSPPR, P_GRPSPPR):
            # Root spTree's nvGrpSpPr / grpSpPr (the zero-transform wrapper) — skip.
            continue
        if tag == MC_ALTERNATE:
            # Markup-compatibility wrapper. Descend transparently: prefer
            # the first mc:Choice (newer markup); fall back to mc:Fallback.
            # The wrapper itself is not a visible object, so it does not
            # consume a z slot.
            chosen = None
            for sub in list(child):
                if sub.tag == MC_CHOICE:
                    chosen = sub
                    break
            if chosen is None:
                for sub in list(child):
                    if sub.tag == MC_FALLBACK:
                        chosen = sub
                        break
            if chosen is not None:
                out.extend(_walk_sp_tree(
                    chosen, parent_group_id=parent_group_id,
                    scale_x=scale_x, scale_y=scale_y,
                    group_off=group_off, group_ch_off=group_ch_off,
                    rels=rels, counter=counter,
                ))
            continue
        counter[0] += 1
        z = counter[0]
        if tag == P_SP:
            out.append(_parse_sp(child, z=z, parent_group_id=parent_group_id,
                                 scale_x=scale_x, scale_y=scale_y,
                                 group_off=group_off, group_ch_off=group_ch_off))
        elif tag == P_CXNSP:
            out.append(_parse_cxn_sp(child, z=z, parent_group_id=parent_group_id,
                                     scale_x=scale_x, scale_y=scale_y,
                                     group_off=group_off, group_ch_off=group_ch_off))
        elif tag == P_PIC:
            out.append(_parse_pic(child, z=z, parent_group_id=parent_group_id,
                                  scale_x=scale_x, scale_y=scale_y,
                                  group_off=group_off, group_ch_off=group_ch_off,
                                  rels=rels))
        elif tag == P_GFRAME:
            out.append(_parse_graphic_frame(child, z=z, parent_group_id=parent_group_id,
                                            scale_x=scale_x, scale_y=scale_y,
                                            group_off=group_off, group_ch_off=group_ch_off,
                                            rels=rels))
        elif tag == P_GRPSP:
            grp_sp_id, grp_name = _identity(child, P_NVGRPSPPR)
            grp_pr = child.find(P_GRPSPPR)
            grp_xfrm = grp_pr.find(A_XFRM) if grp_pr is not None else None
            grp_x, grp_y, grp_cx, grp_cy, grp_rot, grp_fh, grp_fv = _parse_xfrm(grp_xfrm)
            ch_off_el = grp_xfrm.find(A_CHOFF) if grp_xfrm is not None else None
            ch_ext_el = grp_xfrm.find(A_CHEXT) if grp_xfrm is not None else None
            ch_off_x = _parse_int_attr(ch_off_el, "x") or 0
            ch_off_y = _parse_int_attr(ch_off_el, "y") or 0
            ch_ext_cx = _parse_int_attr(ch_ext_el, "cx") or grp_cx or 0
            ch_ext_cy = _parse_int_attr(ch_ext_el, "cy") or grp_cy or 0
            new_scale_x = (grp_cx / ch_ext_cx) if (grp_cx and ch_ext_cx) else 1.0
            new_scale_y = (grp_cy / ch_ext_cy) if (grp_cy and ch_ext_cy) else 1.0
            new_off = (grp_x or 0, grp_y or 0)
            new_ch_off = (ch_off_x, ch_off_y)
            # Emit the group itself as a parent marker.
            out.append(ShapeProbe(
                z=z, kind="grpSp", sp_id=grp_sp_id, name=grp_name,
                chrome_role=None, ph_type=None, ph_idx=None,
                is_placeholder=False,
                geometry=Geometry(x=grp_x, y=grp_y, cx=grp_cx, cy=grp_cy,
                                  x_abs=grp_x, y_abs=grp_y,
                                  rot_deg=grp_rot, flip_h=grp_fh, flip_v=grp_fv),
                fill=Fill(kind="unset", value=None),
                line=Line(kind="unset", color=None, w_emu=None, dash=None,
                          head_end=None, tail_end=None),
                prst=None, prst_avlst=None, custgeom=None,
                text_body=None, table=None, chart=None, picture=None,
                ole=None, frame_uri=None, is_thinkcell=False,
                cxn_start=None, cxn_end=None,
                parent_group_id=parent_group_id,
                group_scale_x=None, group_scale_y=None,
                raw_tag=None,
            ))
            out.extend(_walk_sp_tree(
                child, parent_group_id=grp_sp_id,
                scale_x=new_scale_x, scale_y=new_scale_y,
                group_off=new_off, group_ch_off=new_ch_off,
                rels=rels, counter=counter,
            ))
        else:
            # Unknown shape-like element. Record so nothing silently disappears.
            local = tag.split("}", 1)[-1]
            out.append(ShapeProbe(
                z=z, kind="unknown", sp_id=None, name=None, chrome_role=None,
                ph_type=None, ph_idx=None, is_placeholder=False,
                geometry=Geometry(x=None, y=None, cx=None, cy=None),
                fill=Fill(kind="unset", value=None),
                line=Line(kind="unset", color=None, w_emu=None, dash=None,
                          head_end=None, tail_end=None),
                prst=None, prst_avlst=None, custgeom=None,
                text_body=None, table=None, chart=None, picture=None,
                ole=None, frame_uri=None, is_thinkcell=False,
                cxn_start=None, cxn_end=None,
                parent_group_id=parent_group_id,
                group_scale_x=None, group_scale_y=None,
                raw_tag=local,
            ))
    return out


# ── Public parse entry point ────────────────────────────────────────────


def parse_slide(sld_xml: str, *, rels: dict[str, str] | None = None) -> list[ShapeProbe]:
    root = ET.fromstring(sld_xml)
    sp_tree = root.find(f".//{P_SPTREE}")
    if sp_tree is None:
        return []
    counter = [0]
    return _walk_sp_tree(
        sp_tree, parent_group_id=None,
        scale_x=1.0, scale_y=1.0,
        group_off=(0, 0), group_ch_off=(0, 0),
        rels=rels or {}, counter=counter,
    )


# ── Loaders ─────────────────────────────────────────────────────────────


def _render_callable(mod, target: str):
    """Return a slide module's render entrypoint. The guide lets authors rename
    render() to the file stem, so accept either render() or a callable named
    after the module (deck_ddg.slides.foo -> foo())."""
    if callable(getattr(mod, "render", None)):
        return mod.render
    stem = target.rsplit(".", 1)[-1]
    fn = getattr(mod, stem, None)
    if callable(fn):
        return fn
    raise SystemExit(
        f"module '{target}' has no render() function and no callable {stem}()"
    )


def load_from_module(target: str) -> tuple[str, str, dict[str, str], tuple[int, int], str | None]:
    """Import a slide module and render it.

    Returns (slide_name, sld_xml, rels, canvas, layout_target). The layout
    binding is not known in module mode (the rendered <p:sld> string does
    not carry its own rels), so layout_target is always None here.
    """
    # The caller (the per-program shim) puts the program root on sys.path so
    # `target` (e.g. deck_ddg.slides.<name>) imports.
    mod = importlib.import_module(target)
    slide_name = target.rsplit(".", 1)[-1]
    fn = _render_callable(mod, target)
    # v5 body slides expose a no-arg render(); fall back to the legacy
    # render(*, page_num, total_pages) signature for any unmigrated module.
    try:
        sld_xml = fn()
    except TypeError:
        sld_xml = fn(page_num=1, total_pages=1)
    return (slide_name, sld_xml, {}, (DEFAULT_SLIDE_W, DEFAULT_SLIDE_H), None)


def load_from_pptx(pptx_path: Path, slide_idx: int) -> tuple[str, str, dict[str, str], tuple[int, int], str | None]:
    """Open pptx, read slideN.xml + its rels + canvas dims + layout binding.

    Returns (slide_name, sld_xml, rels, canvas, layout_target). layout_target
    is the slide-layout part the slide binds to (e.g. "../slideLayouts/slideLayout4.xml")
    or None if the slide has no slideLayout relationship.
    """
    with zipfile.ZipFile(pptx_path, "r") as zf:
        names = set(zf.namelist())
        slide_part = f"ppt/slides/slide{slide_idx}.xml"
        if slide_part not in names:
            raise SystemExit(
                f"slide {slide_idx} not found in {pptx_path} "
                f"(expected part {slide_part})"
            )
        sld_xml = zf.read(slide_part).decode("utf-8")
        rels_part = f"ppt/slides/_rels/slide{slide_idx}.xml.rels"
        rels: dict[str, str] = {}
        layout_target: str | None = None
        if rels_part in names:
            rels_xml = zf.read(rels_part).decode("utf-8")
            rels_root = ET.fromstring(rels_xml)
            ns_pkg = "{http://schemas.openxmlformats.org/package/2006/relationships}"
            for rel in rels_root.findall(f"{ns_pkg}Relationship"):
                rid = rel.get("Id")
                tgt = rel.get("Target")
                rtype = rel.get("Type") or ""
                if rid and tgt:
                    rels[rid] = tgt
                if tgt and rtype.endswith("/slideLayout"):
                    layout_target = tgt
        # Canvas from presentation.xml.
        canvas = (DEFAULT_SLIDE_W, DEFAULT_SLIDE_H)
        if "ppt/presentation.xml" in names:
            pres_xml = zf.read("ppt/presentation.xml").decode("utf-8")
            pres = ET.fromstring(pres_xml)
            sld_sz = pres.find(_q("p", "sldSz"))
            if sld_sz is not None:
                cx = _parse_int_attr(sld_sz, "cx") or DEFAULT_SLIDE_W
                cy = _parse_int_attr(sld_sz, "cy") or DEFAULT_SLIDE_H
                canvas = (cx, cy)
    slide_name = f"{pptx_path.stem}_slide{slide_idx}"
    return (slide_name, sld_xml, rels, canvas, layout_target)


def list_pptx_slides(pptx_path: Path) -> list[int]:
    with zipfile.ZipFile(pptx_path, "r") as zf:
        names = zf.namelist()
    slides = []
    for n in names:
        m = re.match(r"ppt/slides/slide(\d+)\.xml$", n)
        if m:
            slides.append(int(m.group(1)))
    return sorted(slides)


def list_module_registry(package: str) -> list[str]:
    """Return every importable slide module under `<package>.slides`.

    The deck's slide_module_renders is built inside build() and not exposed
    at module scope, so we walk the directory instead. Modules are filtered
    to those exposing a render entrypoint — render(), or a callable named after
    the file stem (the guide lets authors rename render to the filename). The
    caller (the per-program shim) has already put the program root on sys.path.
    """
    slides_pkg = importlib.import_module(f"{package}.slides")
    slides_dir = Path(slides_pkg.__file__).parent
    out: list[str] = []
    for f in sorted(slides_dir.glob("*.py")):
        if f.stem == "__init__":
            continue
        modname = f"{package}.slides.{f.stem}"
        try:
            mod = importlib.import_module(modname)
        except Exception:
            continue
        if callable(getattr(mod, "render", None)) or callable(getattr(mod, f.stem, None)):
            out.append(modname)
    return out


# ── Region summary ──────────────────────────────────────────────────────


def region_summary(shapes: list[ShapeProbe], canvas: tuple[int, int]) -> dict[str, Any]:
    """Convenient arithmetic from the parsed shapes. No judgment."""
    body_shapes = [s for s in shapes if s.kind not in ("grpSp", "unknown")
                   and s.chrome_role is None and s.geometry.x is not None
                   and s.geometry.y is not None]
    by_kind: dict[str, int] = {}
    for s in shapes:
        by_kind[s.kind] = by_kind.get(s.kind, 0) + 1
    top_most = bottom_most = None
    if body_shapes:
        top_most = min(body_shapes, key=lambda s: s.geometry.y_abs or s.geometry.y or 0)
        bottom_most = max(body_shapes,
                          key=lambda s: ((s.geometry.y_abs or s.geometry.y or 0)
                                         + (s.geometry.cy or 0)))
    chrome_shapes = {s.chrome_role: s for s in shapes if s.chrome_role}
    ole_count = sum(1 for s in shapes if s.ole is not None)
    thinkcell_count = sum(1 for s in shapes if s.is_thinkcell)
    return {
        "canvas_cx_emu": canvas[0],
        "canvas_cy_emu": canvas[1],
        "canvas_cx_in": _emu_to_in(canvas[0]),
        "canvas_cy_in": _emu_to_in(canvas[1]),
        "shape_count_by_kind": by_kind,
        "total_shapes": len(shapes),
        "ole_count": ole_count,
        "thinkcell_count": thinkcell_count,
        "top_most_body": (
            {"sp_id": top_most.sp_id, "name": top_most.name,
             "y_emu": top_most.geometry.y_abs or top_most.geometry.y,
             "y_in": _emu_to_in(top_most.geometry.y_abs or top_most.geometry.y)}
            if top_most else None
        ),
        "bottom_most_body": (
            {"sp_id": bottom_most.sp_id, "name": bottom_most.name,
             "bottom_emu": ((bottom_most.geometry.y_abs or bottom_most.geometry.y or 0)
                            + (bottom_most.geometry.cy or 0)),
             "bottom_in": _emu_to_in((bottom_most.geometry.y_abs or bottom_most.geometry.y or 0)
                                     + (bottom_most.geometry.cy or 0))}
            if bottom_most else None
        ),
        "chrome": {
            role: {"sp_id": s.sp_id,
                   "x_emu": s.geometry.x, "y_emu": s.geometry.y,
                   "cx_emu": s.geometry.cx, "cy_emu": s.geometry.cy}
            for role, s in chrome_shapes.items()
        },
    }


# ── Text estimator ──────────────────────────────────────────────────────


# ── Text-width / row-height model ────────────────────────────────────────
# Self-contained Arial char-width + greedy-wrap + row-height estimator (was
# deck_core.text_metrics; the probe is its only remaining consumer). Estimates
# are intentionally a touch generous (LINE_HEIGHT_FACTOR) so text isn't clipped.
AVG_CHAR_WIDTH_RATIO = 0.50      # Arial avg glyph advance / font size
LINE_HEIGHT_FACTOR = 1.2         # rendered single-spaced line pitch / font size
DEFAULT_CELL_INSET_V = 45_720    # house table-cell vertical inset (0.05in)
DEFAULT_CELL_INSET_H = 45_720
DEFAULT_MIN_ROW_H = 274_320      # one-line row floor (~0.3in)


def estimate_text_fit(text_body: TextBody, geom: Geometry) -> dict[str, Any] | None:
    if text_body is None or geom.cx is None or geom.cy is None:
        return None
    bp = text_body.body_pr
    avail_w_emu = max(0, geom.cx - bp.l_ins - bp.r_ins)
    avail_h_emu = max(0, geom.cy - bp.t_ins - bp.b_ins)
    total_lines = 0
    total_h_emu = 0
    line_breakdown: list[dict[str, Any]] = []
    for p in text_body.paragraphs:
        # Use the largest font size on the paragraph as the line-height driver.
        font_pts = [r.size_pt for r in p.runs if r.size_pt is not None]
        font_pt = max(font_pts) if font_pts else 18.0
        # Concatenated paragraph text.
        text = "".join(r.text for r in p.runs)
        avg_char_w_emu = font_pt * AVG_CHAR_WIDTH_RATIO * EMU_PER_POINT
        lines = _greedy_wrap(text, avail_w_emu, avg_char_w_emu)
        spacing = (p.ln_spc_pct or 100.0) / 100.0
        para_h_emu = int(len(lines) * font_pt * spacing / 72 * EMU_PER_INCH)
        total_lines += len(lines)
        total_h_emu += para_h_emu
        line_breakdown.append({
            "font_pt": font_pt, "lines": len(lines),
            "para_h_emu": para_h_emu, "para_h_in": _emu_to_in(para_h_emu),
        })
    return {
        "avail_w_emu": avail_w_emu, "avail_w_in": _emu_to_in(avail_w_emu),
        "avail_h_emu": avail_h_emu, "avail_h_in": _emu_to_in(avail_h_emu),
        "wrapped_lines": total_lines,
        "est_height_emu": total_h_emu, "est_height_in": _emu_to_in(total_h_emu),
        "fits": total_h_emu <= avail_h_emu,
        "overflow_emu": max(0, total_h_emu - avail_h_emu),
        "overflow_in": _emu_to_in(max(0, total_h_emu - avail_h_emu)),
        "paragraphs": line_breakdown,
    }


def avg_char_width_emu(size_pt: float) -> float:
    """Approximate average Arial glyph advance at `size_pt`, in EMU."""
    return size_pt * AVG_CHAR_WIDTH_RATIO * EMU_PER_POINT


def line_height_emu(size_pt: float) -> int:
    """Rendered single-spaced line pitch at `size_pt`, in EMU."""
    return int(size_pt * LINE_HEIGHT_FACTOR * EMU_PER_POINT)


def _greedy_wrap(text: str, avail_w_emu: float, avg_char_w_emu: float) -> list[str]:
    """Greedy word wrap by character count. Returns the lines `text` occupies in
    `avail_w_emu` of width (the probe and the row estimator wrap identically)."""
    if not text:
        return [""]
    if avg_char_w_emu <= 0:
        return [text]
    words = text.split()
    if not words:
        return [""]
    max_chars = max(1, int(avail_w_emu / avg_char_w_emu))
    lines: list[str] = []
    current: list[str] = []
    cur_len = 0
    for w in words:
        wlen = len(w)
        if not current:
            current = [w]
            cur_len = wlen
            continue
        if cur_len + 1 + wlen <= max_chars:
            current.append(w)
            cur_len += 1 + wlen
        else:
            lines.append(" ".join(current))
            current = [w]
            cur_len = wlen
    if current:
        lines.append(" ".join(current))
    return lines


def _wrapped_line_count(text: str, usable_width_emu: float, *, size_pt: float) -> int:
    """Lines `text` wraps to in `usable_width_emu` at `size_pt` (minimum 1)."""
    if usable_width_emu <= 0:
        return 1
    return max(1, len(_greedy_wrap(str(text), usable_width_emu, avg_char_width_emu(size_pt))))


def estimate_row_heights(rows, col_w, *, size_pt=10.0, header_size_pt=None,
                         inset_v=DEFAULT_CELL_INSET_V, inset_h=DEFAULT_CELL_INSET_H,
                         min_row_h=DEFAULT_MIN_ROW_H) -> list[int]:
    """Per-row EMU heights sized so every cell's wrapped text fits. rows[0] is the
    header (uses `header_size_pt`, default `size_pt`); a cell's usable width is its
    column width minus 2*inset_h."""
    if any(len(r) != len(col_w) for r in rows):
        raise ValueError(
            f"every row must have {len(col_w)} cells (got widths {[len(r) for r in rows]})")
    header_size_pt = header_size_pt if header_size_pt is not None else size_pt
    heights: list[int] = []
    for ri, row in enumerate(rows):
        sz = header_size_pt if ri == 0 else size_pt
        max_lines = 1
        for ci, cell in enumerate(row):
            usable = col_w[ci] - 2 * inset_h
            max_lines = max(max_lines, _wrapped_line_count(cell, usable, size_pt=sz))
        heights.append(max(min_row_h, max_lines * line_height_emu(sz) + 2 * inset_v))
    return heights


# ── Table-fit info (optional --table-fit report section) ─────────────────


def _tb_max_size_pt(tb: TextBody | None) -> float | None:
    """Largest run font size (pt) anywhere in a text body, or None."""
    if tb is None:
        return None
    sizes = [r.size_pt for p in tb.paragraphs for r in p.runs if r.size_pt is not None]
    return max(sizes) if sizes else None


def _table_grid_text(t: TableProbe) -> tuple[list[list[str]], float, float]:
    """Reconstruct a TableProbe into (rows_text, header_size_pt, body_size_pt)
    for the row-fit estimate. Assumes the house no-merge layout; merged cells
    are placed at their top-left and the spanned slots stay blank."""
    n_cols = len(t.grid_cols_emu)
    n_rows = len(t.row_heights_emu)
    grid = [["" for _ in range(n_cols)] for _ in range(n_rows)]
    hdr_sizes: list[float] = []
    body_sizes: list[float] = []
    for c in t.cells:
        if c.row >= n_rows or c.col >= n_cols:
            continue
        grid[c.row][c.col] = c.text_body.plain_text if c.text_body else ""
        sz = _tb_max_size_pt(c.text_body)
        if sz is not None:
            (hdr_sizes if c.row == 0 else body_sizes).append(sz)
    header_size = max(hdr_sizes) if hdr_sizes else 9.5
    body_size = max(body_sizes) if body_sizes else 9.5
    return grid, header_size, body_size


def table_fit_info(shapes: list[ShapeProbe]) -> list[dict[str, Any]]:
    """Estimated row-height information for every native table on the slide.

    Informational only. Does not validate, lint, fail, or classify a slide — it
    just reports, per table: authored vs content-required row heights (the probe's
    own row-height model), which rows are estimated shorter than their content, the
    estimated honest bottom, and whether that bottom lands within the body floor
    (BODY_B) as a plain fact. Consumed by the optional --table-fit report section.
    """
    findings: list[dict[str, Any]] = []
    for s in shapes:
        if s.kind != "graphicFrame.table" or s.table is None:
            continue
        t = s.table
        rows_text, hsz, bsz = _table_grid_text(t)
        col_w = list(t.grid_cols_emu)
        try:
            required = estimate_row_heights(
                rows_text, col_w, size_pt=bsz, header_size_pt=hsz)
        except ValueError as e:
            findings.append({"name": s.name, "sp_id": s.sp_id, "error": str(e)})
            continue
        authored = list(t.row_heights_emu)
        m = min(len(authored), len(required))
        overflow = [(i, authored[i], required[i]) for i in range(m)
                    if authored[i] < required[i]]
        y = s.geometry.y_abs if s.geometry.y_abs is not None else (s.geometry.y or 0)
        honest_bottom = y + sum(required)
        findings.append({
            "name": s.name, "sp_id": s.sp_id,
            "authored": authored, "required": required,
            "overflow_rows": overflow,
            "authored_total": sum(authored), "required_total": sum(required),
            "frame_y": y, "honest_bottom": honest_bottom,
            "fits_body": honest_bottom <= BODY_B,
        })
    return findings


# ── Renderers ───────────────────────────────────────────────────────────


def _fmt_int(v: int | None) -> str:
    return "—" if v is None else f"{v:,}"


def _fmt_in(v: int | None) -> str:
    if v is None:
        return "—"
    return f"{_emu_to_in(v):.3f}"


def _fill_str(f: Fill) -> str:
    if f.kind == "solid":
        return f.value or "(no color)"
    if f.kind == "scheme":
        return f"scheme:{f.value}"
    if f.kind == "none":
        return "none"
    if f.kind == "unset":
        return "—"
    if f.kind == "blip":
        if f.blip_embed_rid:
            return f"blip:{f.blip_embed_rid}"
        if f.blip_link_rid:
            return f"blip(link):{f.blip_link_rid}"
        return "blip"
    return f.kind


def _line_str(ln: Line) -> str:
    if ln.kind == "none":
        return "none"
    if ln.kind == "unset":
        return "—"
    parts = []
    if ln.color:
        parts.append(ln.color)
    if ln.dash:
        parts.append(f"dash={ln.dash}")
    if ln.head_end and ln.head_end.type and ln.head_end.type != "none":
        parts.append(f"head={ln.head_end.type}")
    if ln.tail_end and ln.tail_end.type and ln.tail_end.type != "none":
        parts.append(f"tail={ln.tail_end.type}")
    return ", ".join(parts) if parts else ln.kind


def _line_pt(ln: Line) -> str:
    if ln.w_emu is None:
        return "—"
    return f"{_emu_to_pt(ln.w_emu):.2f}"


def render_markdown(slide_name: str, shapes: list[ShapeProbe],
                    canvas: tuple[int, int], canvas_source: str, *,
                    layout_target: str | None = None,
                    text_estimate: bool, table_fit: bool = False) -> str:
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    out: list[str] = []
    out.append(f"# Slide probe: {slide_name}\n")
    out.append(f"_Generated {now}_\n")

    # Canvas
    out.append("## Canvas\n")
    out.append(f"- width: {canvas[0]:,} EMU / {_emu_to_in(canvas[0]):.3f} in")
    out.append(f"- height: {canvas[1]:,} EMU / {_emu_to_in(canvas[1]):.3f} in")
    out.append(f"- source: {canvas_source}")
    if layout_target:
        out.append(f"- layout: {layout_target}")
    out.append("")

    # Region summary
    rs = region_summary(shapes, canvas)
    out.append("## Region summary\n")
    out.append(f"- total shapes: {rs['total_shapes']}")
    kinds = ", ".join(f"{k}={v}" for k, v in sorted(rs["shape_count_by_kind"].items()))
    out.append(f"- by kind: {kinds}")
    if rs["top_most_body"]:
        tm = rs["top_most_body"]
        out.append(f"- top-most body object: sp_id={tm['sp_id']} name={tm['name']!r} y={tm['y_emu']:,} ({tm['y_in']:.3f} in)")
    if rs["bottom_most_body"]:
        bm = rs["bottom_most_body"]
        out.append(f"- bottom-most body object: sp_id={bm['sp_id']} name={bm['name']!r} bottom={bm['bottom_emu']:,} ({bm['bottom_in']:.3f} in)")
    if rs["chrome"]:
        out.append(f"- chrome detected: {', '.join(sorted(rs['chrome']))}")
    if rs["ole_count"] or rs["thinkcell_count"]:
        bits = []
        if rs["ole_count"]:
            bits.append(f"{rs['ole_count']} OLE embed(s)")
        if rs["thinkcell_count"]:
            bits.append(f"{rs['thinkcell_count']} thinkcell")
        out.append(f"- {' / '.join(bits)}")
    out.append("")

    # Shapes in z-order
    out.append("## Shapes in z-order\n")
    out.append("| z | id | name | kind | placeholder | x | y | cx | cy | x_in | y_in | w_in | h_in | right | bottom |")
    out.append("|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for s in shapes:
        g = s.geometry
        x_disp = "(layout)" if (s.is_placeholder and g.x is None) else _fmt_int(g.x_abs or g.x)
        y_disp = "(layout)" if (s.is_placeholder and g.y is None) else _fmt_int(g.y_abs or g.y)
        cx_disp = _fmt_int(g.cx)
        cy_disp = _fmt_int(g.cy)
        x_in_disp = _fmt_in(g.x_abs or g.x)
        y_in_disp = _fmt_in(g.y_abs or g.y)
        w_in_disp = _fmt_in(g.cx)
        h_in_disp = _fmt_in(g.cy)
        right_emu = ((g.x_abs or g.x or 0) + (g.cx or 0)) if g.x is not None else None
        bot_emu = ((g.y_abs or g.y or 0) + (g.cy or 0)) if g.y is not None else None
        ph = "—"
        if s.is_placeholder:
            ph = f"{s.ph_type or ''}/{s.ph_idx or ''}"
        elif s.chrome_role:
            ph = f"chrome:{s.chrome_role}"
        elif s.parent_group_id:
            ph = f"in grp #{s.parent_group_id}"
        name_disp = (s.name or "—").replace("|", "\\|")
        out.append(
            f"| {s.z} | {s.sp_id if s.sp_id is not None else '—'} "
            f"| {name_disp} | {s.kind} | {ph} "
            f"| {x_disp} | {y_disp} | {cx_disp} | {cy_disp} "
            f"| {x_in_disp} | {y_in_disp} | {w_in_disp} | {h_in_disp} "
            f"| {_fmt_int(right_emu)} | {_fmt_int(bot_emu)} |"
        )
    out.append("")

    # Visual styling
    out.append("## Visual styling\n")
    out.append("| id | name | kind | fill | line | line_pt | dash | prst |")
    out.append("|---:|---|---|---|---|---:|---|---|")
    for s in shapes:
        if s.kind in ("grpSp", "unknown") and s.fill.kind == "unset" and s.line.kind == "unset":
            continue
        name_disp = (s.name or "—").replace("|", "\\|")
        out.append(
            f"| {s.sp_id if s.sp_id is not None else '—'} "
            f"| {name_disp} | {s.kind} "
            f"| {_fill_str(s.fill)} | {_line_str(s.line)} "
            f"| {_line_pt(s.line)} | {s.line.dash or '—'} | {s.prst or '—'} |"
        )
    out.append("")

    # Preset-geometry adjustments (callout tails, corner radii, ...). Only the
    # shapes that actually carry handles, so a wedge/roundRect adj is inspectable.
    adjusted = [s for s in shapes if s.prst_avlst]
    if adjusted:
        out.append("## Preset geometry adjustments\n")
        out.append("| id | name | prst | avLst |")
        out.append("|---:|---|---|---|")
        for s in adjusted:
            av = ", ".join(f"{k}={v}" for k, v in s.prst_avlst.items())
            nm = (s.name or "—").replace("|", "\\|")
            out.append(
                f"| {s.sp_id if s.sp_id is not None else '—'} | {nm} "
                f"| {s.prst or '—'} | {av} |")
        out.append("")

    # Transformed shapes (rotation or flip). Only emit if anything qualifies.
    transformed = [
        s for s in shapes
        if (s.geometry.rot_deg not in (None, 0, 0.0)
            or s.geometry.flip_h or s.geometry.flip_v)
    ]
    if transformed:
        out.append("## Transformed shapes (rotation or flip)\n")
        out.append("Note: absolute_box columns above are axis-aligned and do not "
                   "account for rotation. The values below describe the transform.\n")
        out.append("| id | name | kind | rot_deg | flipH | flipV |")
        out.append("|---:|---|---|---:|:---:|:---:|")
        for s in transformed:
            name_disp = (s.name or "—").replace("|", "\\|")
            rot = s.geometry.rot_deg if s.geometry.rot_deg is not None else 0
            out.append(
                f"| {s.sp_id if s.sp_id is not None else '—'} "
                f"| {name_disp} | {s.kind} "
                f"| {rot:g} | {'yes' if s.geometry.flip_h else '—'} "
                f"| {'yes' if s.geometry.flip_v else '—'} |"
            )
        out.append("")

    # Text and font details
    text_shapes = [s for s in shapes if s.text_body is not None and s.text_body.paragraphs]
    if text_shapes:
        out.append("## Text and font details\n")
        for s in text_shapes:
            label = f"sp_id={s.sp_id} name={s.name!r}"
            if s.chrome_role:
                label += f" [chrome: {s.chrome_role}]"
            out.append(f"### {label}")
            g = s.geometry
            if g.x is not None:
                out.append(
                    f"- box: x={_fmt_int(g.x_abs or g.x)} y={_fmt_int(g.y_abs or g.y)} "
                    f"cx={_fmt_int(g.cx)} cy={_fmt_int(g.cy)} "
                    f"({_fmt_in(g.x_abs or g.x)},{_fmt_in(g.y_abs or g.y)} in; "
                    f"{_fmt_in(g.cx)}×{_fmt_in(g.cy)} in)"
                )
            else:
                out.append("- box: (layout-inherited)")
            bp = s.text_body.body_pr
            out.append(
                f"- bodyPr: anchor={bp.anchor or '—'} wrap={bp.wrap or '—'} "
                f"lIns={bp.l_ins:,} rIns={bp.r_ins:,} tIns={bp.t_ins:,} bIns={bp.b_ins:,} "
                f"(={_emu_to_in(bp.l_ins):.3f}/{_emu_to_in(bp.r_ins):.3f}/{_emu_to_in(bp.t_ins):.3f}/{_emu_to_in(bp.b_ins):.3f} in)"
            )
            out.append("- paragraphs:")
            for i, p in enumerate(s.text_body.paragraphs, 1):
                joined = "".join(r.text for r in p.runs) or "(empty)"
                pieces = [f'  {i}. "{joined}"']
                attrs = []
                if p.algn:
                    attrs.append(f"algn={p.algn}")
                if p.ln_spc_pct is not None:
                    attrs.append(f"lnSpc={p.ln_spc_pct:g}%")
                if p.ln_spc_pts is not None:
                    attrs.append(f"lnSpc={p.ln_spc_pts:g}pt")
                if p.bullet_char:
                    attrs.append(f"bu='{p.bullet_char}'")
                if p.bullet_autonum:
                    attrs.append(f"buAuto={p.bullet_autonum}")
                if p.level:
                    attrs.append(f"lvl={p.level}")
                if attrs:
                    pieces.append("     - para: " + ", ".join(attrs))
                for ri, r in enumerate(p.runs):
                    r_attrs = []
                    if r.font:
                        r_attrs.append(f"font={r.font}")
                    if r.size_pt is not None:
                        r_attrs.append(f"size={r.size_pt:g}pt")
                    if r.color:
                        r_attrs.append(f"color={r.color}")
                    if r.bold:
                        r_attrs.append("bold")
                    if r.italic:
                        r_attrs.append("italic")
                    if r.underline:
                        r_attrs.append(f"u={r.underline}")
                    if r_attrs:
                        pieces.append(f"     - run {ri}: " + ", ".join(r_attrs))
                out.append("\n".join(pieces))
            if text_estimate:
                est = estimate_text_fit(s.text_body, s.geometry)
                if est is not None:
                    out.append(
                        f"- text estimate: avail {_emu_to_in(est['avail_w_emu']):.3f}×{_emu_to_in(est['avail_h_emu']):.3f} in; "
                        f"{est['wrapped_lines']} estimated wrapped lines; "
                        f"est height {_emu_to_in(est['est_height_emu']):.3f} in; "
                        f"fits={est['fits']}"
                        + ("" if est['fits'] else f"; overflow {_emu_to_in(est['overflow_emu']):.3f} in")
                    )
            out.append("")

    # Tables
    table_shapes = [s for s in shapes if s.table is not None]
    if table_shapes:
        out.append("## Tables\n")
        for s in table_shapes:
            label = f"sp_id={s.sp_id} name={s.name!r}"
            out.append(f"### {label}")
            t = s.table
            cols_in = [f"{_emu_to_in(c):.3f}" for c in t.grid_cols_emu]
            cols_emu = [f"{c:,}" for c in t.grid_cols_emu]
            out.append(f"- grid columns ({len(t.grid_cols_emu)}): {', '.join(cols_emu)} EMU "
                       f"({', '.join(cols_in)} in)")
            rows_in = [f"{_emu_to_in(h):.3f}" for h in t.row_heights_emu]
            rows_emu = [f"{h:,}" for h in t.row_heights_emu]
            out.append(f"- row heights ({len(t.row_heights_emu)}): {', '.join(rows_emu)} EMU "
                       f"({', '.join(rows_in)} in)")
            n_rows = len(t.row_heights_emu)
            n_cols = len(t.grid_cols_emu)
            out.append("")
            out.append("| row\\col | " + " | ".join(f"c{i}" for i in range(n_cols)) + " |")
            out.append("|---:|" + "|".join("---" for _ in range(n_cols)) + "|")
            for r in range(n_rows):
                cells_in_row = [c for c in t.cells if c.row == r]
                cells_in_row.sort(key=lambda c: c.col)
                row_strs = [f"r{r}"]
                for c in range(n_cols):
                    cell = next((cl for cl in cells_in_row if cl.col == c), None)
                    if cell is None:
                        row_strs.append("—")
                        continue
                    txt = ((cell.text_body.plain_text if cell.text_body else "")
                           or "").replace("|", "\\|").replace("\n", " / ")
                    if not txt:
                        txt = "(empty)"
                    fill_marker = f" [{cell.fill.value}]" if cell.fill.kind == "solid" else ""
                    span = ""
                    if cell.grid_span > 1:
                        span += f" gSpan={cell.grid_span}"
                    if cell.row_span > 1:
                        span += f" rSpan={cell.row_span}"
                    if cell.h_merge:
                        span += " hMerge"
                    if cell.v_merge:
                        span += " vMerge"
                    row_strs.append(f"{txt}{fill_marker}{span}")
                out.append("| " + " | ".join(row_strs) + " |")
            out.append("")

    # Charts and graphic frames
    chart_shapes = [s for s in shapes if s.chart is not None]
    if chart_shapes:
        out.append("## Charts and graphic frames\n")
        for s in chart_shapes:
            label = f"sp_id={s.sp_id} name={s.name!r}"
            out.append(f"### {label}")
            c = s.chart
            out.append(f"- kind: {c.kind}")
            out.append(f"- rId: {c.rid or '—'}")
            out.append(f"- resolved chart part: {c.resolved_path or '(unresolved — module mode)'}")
            g = s.geometry
            if g.x is not None:
                out.append(
                    f"- frame box: x={_fmt_int(g.x)} y={_fmt_int(g.y)} "
                    f"cx={_fmt_int(g.cx)} cy={_fmt_int(g.cy)}"
                )
            out.append("")

    # OLE and other graphic frames (catches thinkcell — both classic OLE form
    # and the newer custom-URI form; also surfaces any diagram / unknown URIs
    # so nothing is silently invisible).
    other_frames = [
        s for s in shapes
        if s.kind in ("graphicFrame.ole", "graphicFrame.diagram", "graphicFrame.unknown")
    ]
    if other_frames:
        out.append("## OLE and other graphic frames\n")
        for s in other_frames:
            label = f"sp_id={s.sp_id} name={s.name!r}"
            out.append(f"### {label}")
            out.append(f"- kind: {s.kind}")
            if s.frame_uri:
                out.append(f"- graphicData URI: {s.frame_uri}")
            if s.is_thinkcell:
                out.append("- detected: **thinkcell embed**")
            if s.ole is not None:
                o = s.ole
                out.append(f"- OLE progId: {o.prog_id or '—'}")
                out.append(f"- OLE rId: {o.rid or '—'}")
                out.append(f"- resolved embed: {o.resolved_path or '(unresolved — module mode)'}")
                out.append(f"- show as icon: {o.show_as_icon}")
            g = s.geometry
            if g.x is not None:
                out.append(
                    f"- frame box: x={_fmt_int(g.x)} y={_fmt_int(g.y)} "
                    f"cx={_fmt_int(g.cx)} cy={_fmt_int(g.cy)}"
                )
            out.append("")

    # Pictures
    pic_shapes = [s for s in shapes if s.picture is not None]
    if pic_shapes:
        out.append("## Pictures\n")
        for s in pic_shapes:
            label = f"sp_id={s.sp_id} name={s.name!r}"
            out.append(f"### {label}")
            p = s.picture
            out.append(f"- embed rId: {p.embed_rid or '—'}")
            out.append(f"- link rId: {p.link_rid or '—'}")
            out.append(f"- resolved media: {p.resolved_path or '(unresolved — module mode)'}")
            if any(v is not None for v in (p.crop_l_pct, p.crop_r_pct, p.crop_t_pct, p.crop_b_pct)):
                out.append(
                    f"- crop: l={p.crop_l_pct}% r={p.crop_r_pct}% "
                    f"t={p.crop_t_pct}% b={p.crop_b_pct}%"
                )
            out.append("")

    # Connectors with endpoints
    cxn_shapes = [s for s in shapes if s.kind == "cxnSp" and (s.cxn_start or s.cxn_end)]
    if cxn_shapes:
        out.append("## Connectors with endpoint bindings\n")
        for s in cxn_shapes:
            out.append(f"- sp_id={s.sp_id} name={s.name!r}: "
                       f"start={s.cxn_start} end={s.cxn_end}")
        out.append("")

    # Unknown elements
    unknown = [s for s in shapes if s.kind == "unknown"]
    if unknown:
        out.append("## Unknown shape-like elements\n")
        for s in unknown:
            out.append(f"- z={s.z} raw tag: {s.raw_tag}")
        out.append("")

    # Table fit (estimated) — optional informational section (--table-fit).
    # Facts only: authored vs estimated-required row heights, any rows estimated
    # shorter than their content, the estimated honest bottom, and whether it
    # lands within the body floor. Not a check; nothing here fails the probe.
    if table_fit:
        infos = table_fit_info(shapes)
        out.append("## Table fit (estimated)\n")
        if not infos:
            out.append("_No native tables on this slide._\n")
        for f in infos:
            out.append(f"### sp_id={f['sp_id']} name={f['name']!r}")
            if f.get("error"):
                out.append(f"- could not estimate: {f['error']}")
                out.append("")
                continue
            out.append(
                f"- authored total height: {f['authored_total']:,} EMU "
                f"({_emu_to_in(f['authored_total']):.3f} in)")
            out.append(
                f"- estimated required total: {f['required_total']:,} EMU "
                f"({_emu_to_in(f['required_total']):.3f} in)")
            out.append(
                f"- estimated bottom: {f['honest_bottom']:,} EMU "
                f"({_emu_to_in(f['honest_bottom']):.3f} in); "
                f"within BODY_B ({BODY_B:,}): {f['fits_body']}")
            if f["overflow_rows"]:
                rows = ", ".join(f"row {i} authored {a:,} < est {r:,}"
                                 for i, a, r in f["overflow_rows"])
                out.append(f"- rows estimated short: {rows}")
            else:
                out.append("- rows estimated short: none")
            out.append("")

    return "\n".join(out) + "\n"


def render_json(slide_name: str, shapes: list[ShapeProbe],
                canvas: tuple[int, int], canvas_source: str, *,
                layout_target: str | None = None,
                text_estimate: bool, table_fit: bool = False) -> dict[str, Any]:
    now = _dt.datetime.now(_dt.timezone.utc).isoformat()

    def _shape_to_dict(s: ShapeProbe) -> dict[str, Any]:
        g = s.geometry
        d = {
            "z": s.z, "kind": s.kind, "sp_id": s.sp_id, "name": s.name,
            "chrome_role": s.chrome_role,
            "ph_type": s.ph_type, "ph_idx": s.ph_idx,
            "is_placeholder": s.is_placeholder,
            "geometry": {
                "x": g.x, "y": g.y, "cx": g.cx, "cy": g.cy,
                "x_abs": g.x_abs, "y_abs": g.y_abs,
                "x_in": _emu_to_in(g.x_abs or g.x),
                "y_in": _emu_to_in(g.y_abs or g.y),
                "cx_in": _emu_to_in(g.cx),
                "cy_in": _emu_to_in(g.cy),
                "right_emu": ((g.x_abs or g.x or 0) + (g.cx or 0)) if g.x is not None else None,
                "bottom_emu": ((g.y_abs or g.y or 0) + (g.cy or 0)) if g.y is not None else None,
                "rot_deg": g.rot_deg,
                "flip_h": g.flip_h,
                "flip_v": g.flip_v,
            },
            "fill": dataclasses.asdict(s.fill),
            "line": dataclasses.asdict(s.line),
            "prst": s.prst,
            "prst_avlst": s.prst_avlst,
            "custgeom": dataclasses.asdict(s.custgeom) if s.custgeom else None,
            "text_body": _text_body_to_dict(s.text_body) if s.text_body else None,
            "table": _table_to_dict(s.table) if s.table else None,
            "chart": dataclasses.asdict(s.chart) if s.chart else None,
            "picture": dataclasses.asdict(s.picture) if s.picture else None,
            "ole": dataclasses.asdict(s.ole) if s.ole else None,
            "frame_uri": s.frame_uri,
            "is_thinkcell": s.is_thinkcell,
            "cxn_start": list(s.cxn_start) if s.cxn_start else None,
            "cxn_end": list(s.cxn_end) if s.cxn_end else None,
            "parent_group_id": s.parent_group_id,
            "group_scale_x": s.group_scale_x,
            "group_scale_y": s.group_scale_y,
            "raw_tag": s.raw_tag,
        }
        if text_estimate and s.text_body is not None:
            d["text_estimate"] = estimate_text_fit(s.text_body, s.geometry)
        return d

    doc = {
        "slide_name": slide_name,
        "generated_at": now,
        "canvas": {
            "cx_emu": canvas[0], "cy_emu": canvas[1],
            "cx_in": _emu_to_in(canvas[0]), "cy_in": _emu_to_in(canvas[1]),
            "source": canvas_source,
            "layout_target": layout_target,
        },
        "region_summary": region_summary(shapes, canvas),
        "shapes": [_shape_to_dict(s) for s in shapes],
    }
    # Optional informational table-fit estimates (--table-fit). Facts only.
    if table_fit:
        doc["table_fit"] = table_fit_info(shapes)
    return doc


def _text_body_to_dict(tb: TextBody) -> dict[str, Any]:
    return {
        "body_pr": dataclasses.asdict(tb.body_pr),
        "paragraphs": [
            {
                "algn": p.algn, "ln_spc_pct": p.ln_spc_pct,
                "ln_spc_pts": p.ln_spc_pts,
                "bullet_char": p.bullet_char, "bullet_autonum": p.bullet_autonum,
                "level": p.level,
                "runs": [dataclasses.asdict(r) for r in p.runs],
            } for p in tb.paragraphs
        ],
        "plain_text": tb.plain_text,
    }


def _table_to_dict(t: TableProbe) -> dict[str, Any]:
    return {
        "grid_cols_emu": list(t.grid_cols_emu),
        "row_heights_emu": list(t.row_heights_emu),
        "cells": [
            {
                "row": c.row, "col": c.col,
                "grid_span": c.grid_span, "row_span": c.row_span,
                "h_merge": c.h_merge, "v_merge": c.v_merge,
                "fill": dataclasses.asdict(c.fill),
                "border_left": dataclasses.asdict(c.border_left),
                "border_right": dataclasses.asdict(c.border_right),
                "border_top": dataclasses.asdict(c.border_top),
                "border_bottom": dataclasses.asdict(c.border_bottom),
                "mar_l": c.mar_l, "mar_r": c.mar_r,
                "mar_t": c.mar_t, "mar_b": c.mar_b,
                "anchor": c.anchor,
                "text_body": _text_body_to_dict(c.text_body) if c.text_body else None,
            } for c in t.cells
        ],
    }


# ── CLI ─────────────────────────────────────────────────────────────────


def _probe_one(target: str | Path, *, slide_idx: int | None,
               text_estimate: bool, table_fit: bool, json_only: bool,
               out_dir: Path) -> Path:
    target_str = str(target)
    if target_str.lower().endswith(".pptx"):
        canvas_source = "p:sldSz"
        idx = slide_idx if slide_idx is not None else 1
        slide_name, sld_xml, rels, canvas, layout_target = load_from_pptx(Path(target_str), idx)
    else:
        canvas_source = "defaults (12_192_000 × 6_858_000)"
        slide_name, sld_xml, rels, canvas, layout_target = load_from_module(target_str)
    shapes = parse_slide(sld_xml, rels=rels)
    out_dir.mkdir(parents=True, exist_ok=True)
    # Wipe any prior outputs for this slide so re-probing replaces rather
    # than stacks. Matches every <slide_name>.* file in the output dir.
    for stale in out_dir.glob(f"{slide_name}.*"):
        try:
            stale.unlink()
        except OSError:
            pass
    json_doc = render_json(slide_name, shapes, canvas, canvas_source,
                           layout_target=layout_target,
                           text_estimate=text_estimate, table_fit=table_fit)
    json_path = out_dir / f"{slide_name}.json"
    json_path.write_text(json.dumps(json_doc, indent=2), encoding="utf-8")
    if not json_only:
        md_doc = render_markdown(slide_name, shapes, canvas, canvas_source,
                                 layout_target=layout_target,
                                 text_estimate=text_estimate, table_fit=table_fit)
        md_path = out_dir / f"{slide_name}.md"
        md_path.write_text(md_doc, encoding="utf-8")
        return md_path
    return json_path


def main(argv: list[str] | None = None, *, default_package: str = "deck_ddg",
         default_out_dir: Path | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Read-only OOXML inspector for any pptx slide.",
    )
    ap.add_argument(
        "target", nargs="?",
        help="Python module path (e.g. deck_ddg.slides.<name>) "
             "OR path to a .pptx file. Omit when using --all.",
    )
    ap.add_argument("--slide", type=int, default=None,
                    help="In pptx-file mode: 1-based slide index (default 1).")
    ap.add_argument("--text-estimate", action="store_true",
                    help="Add text wrap / height estimates per text box.")
    ap.add_argument("--json", action="store_true",
                    help="Write only the JSON file (skip Markdown).")
    ap.add_argument("--all", action="store_true",
                    help="Iterate every slide. Module mode: walks the deck's "
                         "slides package for any module with a render() function. "
                         "File mode: walks every ppt/slides/slideN.xml in the pptx.")
    ap.add_argument("--table-fit", action="store_true",
                    help="Add an informational table-fit section to the report: "
                         "each native table's authored vs estimated content-required "
                         "row heights and estimated bottom. Facts only — never fails.")
    ap.add_argument("--out-dir", default=None,
                    help="Output directory (default: <deck>/reports/slide_probe/).")
    args = ap.parse_args(argv)

    if args.out_dir:
        out_dir = Path(args.out_dir)
    elif default_out_dir is not None:
        out_dir = Path(default_out_dir)
    else:
        out_dir = Path(__file__).resolve().parent / "reports" / "slide_probe"

    if args.all:
        targets: list[tuple[str, int | None]] = []
        if args.target and args.target.lower().endswith(".pptx"):
            for n in list_pptx_slides(Path(args.target)):
                targets.append((args.target, n))
        else:
            for m in list_module_registry(default_package):
                targets.append((m, None))
        if not targets:
            print("no slides found", file=sys.stderr)
            return 1
        for tgt, idx in targets:
            try:
                path = _probe_one(tgt, slide_idx=idx,
                                  text_estimate=args.text_estimate,
                                  table_fit=args.table_fit,
                                  json_only=args.json, out_dir=out_dir)
                print(f"wrote {path}")
            except Exception as e:
                print(f"FAILED {tgt} slide={idx}: {e}", file=sys.stderr)
        return 0

    if not args.target:
        ap.error("target is required unless --all is set")
    path = _probe_one(args.target, slide_idx=args.slide,
                      text_estimate=args.text_estimate,
                      table_fit=args.table_fit,
                      json_only=args.json, out_dir=out_dir)
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
