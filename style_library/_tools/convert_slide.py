#!/usr/bin/env python3
"""convert_slide.py - convert one source-.pptx slide into an idiomatic deck_core module.

Reads a single slide from a source PowerPoint file and emits a Python slide module
that rebuilds it through deck_core primitives. The aim is a module that (a) renders
faithfully and (b) reads like a hand-authored deck_core slide, so an AI agent can
study it as a worked example.

Pipeline: parse every shape into a record -> detect roles/structure -> emit.

  - native <c:chart> graphicFrame -> graphic_frame(rId="rId2") + the chart part and
    its .xlsb copied into _src/. Its data caches are read into a _DATA dict literal and
    CHARTS = [styled_chart(_CHART_TPL, _DATA, _XLSB)]: the source part is the exact
    STYLE template (look byte-identical), the values live in Python, and "Edit Data"
    still works. Style-dense charts a factory can't rebuild (bar+line combos, pattern
    fills) come through faithfully; the chart is NEVER rebuilt by a factory. Falls back
    to editable_bundled_chart when the data or .xlsb can't be recovered.
  - <p:pic> images -> picture() + an IMAGES entry; the media bytes are copied into the
    deck's slides/images/ under a content-addressed name (identical media dedupes, names
    never collide across source decks). An .emf pic over a bundled native chart is that
    chart's think-cell vector PREVIEW and is dropped; a think-cell OLE data frame ("... do
    not delete") is dropped too.
  - <a:fld> labels (think-cell) -> FROZEN to static run()s from their cached text.
  - colour: schemeClr (lumMod/lumOff/shade/tint baked) -> hex; an exact deck_core
    token match is emitted as the token. Borders inherited from a <p:style><a:lnRef>
    (think-cell's callouts) are resolved too.
  - STANDARD CHROME (breadcrumb / title / Preliminary chip / sources) is recognised by
    placeholder + text + position and emitted via the house builders -- but only when
    the source sits within tolerance of the house position; otherwise it's kept as a
    verbatim shape so nothing moves.
  - STRUCTURE: shapes that share a style (>=3 of them) are collapsed into a module-level
    data table + a loop (the year axis, on-bar values, legend keys/labels, callouts),
    instead of N near-identical calls.
  - anything exotic (custGeom, gradient/pattern/picture fill, a placeholder with no
    geometry) -> emitted as a RAW verbatim OOXML string (cruft stripped, id renumbered).

Usage:
    python convert_slide.py SOURCE.pptx N \\
        --out  ../deck_<name>/slides/<name>.py \\
        --src-dir ../deck_<name>/slides/_src \\
        --module-name <name> [--layout slideLayout4]

Stdlib only, so it can be copied next to any deck pipeline.
"""
from __future__ import annotations

import argparse
import colorsys
import hashlib
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
C = "http://schemas.openxmlformats.org/drawingml/2006/chart"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

for _pfx, _uri in (("a", A), ("p", P), ("c", C), ("r", R)):
    ET.register_namespace(_pfx, _uri)


def q(ns: str, t: str) -> str:
    return f"{{{ns}}}{t}"


# hex (upper) -> deck_core.style token name. Exact matches only (no nearest-snap, which
# would shift a brand colour). Brand accents stay literal hex on purpose.
TOKENS = {
    "000000": "BLACK", "FFFFFF": "WHITE", "162029": "DK",
    "44505C": "BREADCRUMB", "FFFFCC": "PRELIM",
    "E2E9EF": "BLUE_1", "B6C8D8": "BLUE_2", "6E91B1": "BLUE_3",
    "3D5972": "BLUE_4", "263746": "BLUE_5",
    "F2F2F2": "GRAY_1", "D9D9D9": "GRAY_2", "BFBFBF": "GRAY_3",
    "7F7F7F": "GRAY_4", "646464": "GRAY_5",
}

# House chrome positions (deck_core.style) + tolerance, for chrome detection. A
# detected chrome shape becomes a builder only when its source position is within
# TOL of the house position; otherwise it stays a verbatim shape so nothing moves.
LEFT_MARGIN = 453079
HOUSE_POS = {
    "breadcrumb": (LEFT_MARGIN, 263452),
    "title": (LEFT_MARGIN, 554500),
    "prelim": (10267829, 111556),
    "sources": (LEFT_MARGIN, 5930000),
}
TOL = 91440   # 0.1 in
HOUSE_TITLE_CX = 11282362   # deck_core CONTENT_W: the house title box width

# House slideLayouts keyed by their <p:cSld name>. A source slide's own layout is
# matched to the house layout of the SAME NAME, so a "50% Block + Title", "Cover 1",
# "Section Divider", or "Glossary" source slide gets the house equivalent instead of
# being flattened onto the body layout. (Source decks reference layout NUMBERS that
# don't exist in infra/template -- e.g. slideLayout12/13 -- but the layout NAMES line
# up.) A name with no house match falls back to the --layout default (body slide).
HOUSE_LAYOUTS = {
    "Cover 1": "slideLayout1",
    "Section Divider": "slideLayout2",
    "50% Block + Title": "slideLayout3",
    "Light Blank": "slideLayout4",
    "Blank": "slideLayout5",
    "Glossary": "slideLayout6",
}

# fields a same-style cluster is allowed to vary on, in tuple order
VARYING_ORDER = ["x", "y", "cx", "cy", "fill", "line_color", "text", "geom_adj"]
VAR_NAMES = {"x": "_x", "y": "_y", "cx": "_cx", "cy": "_cy", "fill": "_fill",
             "line_color": "_lc", "text": "_t", "geom_adj": "_ga"}
FIELD_LABEL = {"x": "x", "y": "y", "cx": "cx", "cy": "cy", "fill": "fill",
               "line_color": "line", "text": "label", "geom_adj": "tail"}
DIM = {"x": "X", "y": "Y", "cx": "W", "cy": "H"}   # coordinate -> anchor-name dimension
MIN_CLUSTER = 3
SHARED_ANCHOR_MIN = 4   # a coord value repeated >= this across standalone shapes is hoisted

# coordinate units in the emitted module. "inches" -> every coord becomes IN(<inches>)
# (deck_core.style.IN converts back to EMU at build); "emu" -> raw EMU ints. Inch
# values use 3 decimals: visually exact (sub-0.05 px) but not byte-exact.
_UNITS = "inches"

# source-slide hyperlink rId -> module-level rId, populated per convert() run and
# read by render_run/render_trun to emit run(hyperlink_rid=...).
_HLINKS: dict = {}


def _inch(emu):
    return f"{emu / 914400:.3f}".rstrip("0").rstrip(".") or "0"


def coordlit(emu):
    """Inline coordinate literal: IN(<inches>) in inch mode, else the raw EMU int."""
    return f"IN({_inch(emu)})" if (_UNITS == "inches" and isinstance(emu, int)) else str(emu)


def coordfloat(emu):
    """Bare coordinate value for a data-table cell (the loop wraps it in IN())."""
    return _inch(emu) if (_UNITS == "inches" and isinstance(emu, int)) else str(emu)


def sizelit(sz):
    """Font size literal: PT(<points>) in inch/human mode, else the raw 1/100-pt int."""
    return f"PT({sz / 100:g})" if (_UNITS == "inches" and isinstance(sz, int)) else str(sz)


# ── colour resolution ────────────────────────────────────────────────────────
def build_theme_map(z: zipfile.ZipFile) -> dict:
    root = ET.fromstring(z.read("ppt/theme/theme1.xml"))
    scheme = root.find(".//" + q(A, "clrScheme"))
    m: dict[str, str] = {}
    for child in scheme:
        name = child.tag.split("}")[-1]
        srgb = child.find(q(A, "srgbClr"))
        sysc = child.find(q(A, "sysClr"))
        if srgb is not None:
            m[name] = srgb.get("val", "000000").upper()
        elif sysc is not None:
            m[name] = sysc.get("lastClr", "000000").upper()
    m["tx1"], m["bg1"] = m.get("dk1", "000000"), m.get("lt1", "FFFFFF")
    m["tx2"], m["bg2"] = m.get("dk2", "000000"), m.get("lt2", "FFFFFF")
    # theme line-style list (1-based) -> width, for borders inherited via <a:lnRef idx>
    lnlst = root.find(".//" + q(A, "lnStyleLst"))
    m["__lnw__"] = {}
    if lnlst is not None:
        for idx, ln in enumerate(lnlst.findall(q(A, "ln")), 1):
            if ln.get("w"):
                m["__lnw__"][idx] = int(ln.get("w"))
    return m


def build_table_style_map(z: zipfile.ZipFile) -> dict:
    """styleId -> {"firstRow"/"firstCol": True} for the parts a table style renders
    BOLD via its tcTxStyle. A header bold ONLY through its table style (no explicit
    run b="1") loses the bold on the No-Style rebuild; parse_table bakes these in.
    Stdlib-only, best-effort (absent/garbled file -> {})."""
    try:
        root = ET.fromstring(z.read("ppt/tableStyles.xml"))
    except (KeyError, ET.ParseError):
        return {}
    out: dict = {}
    for ts in root.findall(q(A, "tblStyle")):
        parts = {}
        for part in ("firstRow", "firstCol"):
            el = ts.find(q(A, part))
            tx = el.find(q(A, "tcTxStyle")) if el is not None else None
            if tx is not None and tx.get("b") == "on":
                parts[part] = True
        if parts:
            out[ts.get("styleId")] = parts
    return out


def _bake_lum(hex6: str, lummod, lumoff) -> str:
    r, g, b = (int(hex6[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if lummod is not None:
        l *= lummod
    if lumoff is not None:
        l += lumoff
    l = max(0.0, min(1.0, l))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"{round(r * 255):02X}{round(g * 255):02X}{round(b * 255):02X}"


def _apply_shade_tint(hex6: str, shade, tint) -> str:
    r, g, b = (int(hex6[i:i + 2], 16) for i in (0, 2, 4))
    if shade is not None:
        r, g, b = r * shade, g * shade, b * shade
    if tint is not None:
        r = r * tint + 255 * (1 - tint)
        g = g * tint + 255 * (1 - tint)
        b = b * tint + 255 * (1 - tint)
    return f"{round(r):02X}{round(g):02X}{round(b):02X}"


def color_hex(clr, theme: dict):
    """An <a:srgbClr>/<a:schemeClr> element -> resolved 6-char hex (lum/shade/tint baked)."""
    if clr is None:
        return None
    tag = clr.tag.split("}")[-1]
    if tag == "srgbClr":
        base = clr.get("val", "000000").upper()
    elif tag == "schemeClr":
        base = theme.get(clr.get("val"), "000000")
    else:
        return None
    lm, lo = clr.find(q(A, "lumMod")), clr.find(q(A, "lumOff"))
    lummod = int(lm.get("val")) / 100000 if lm is not None else None
    lumoff = int(lo.get("val")) / 100000 if lo is not None else None
    if lummod is not None or lumoff is not None:
        base = _bake_lum(base, lummod, lumoff)
    sh, ti = clr.find(q(A, "shade")), clr.find(q(A, "tint"))
    if sh is not None or ti is not None:
        base = _apply_shade_tint(base,
                                 int(sh.get("val")) / 100000 if sh is not None else None,
                                 int(ti.get("val")) / 100000 if ti is not None else None)
    return base


def color_lit(hex6):
    """hex -> Python literal: a token name where it matches exactly, else a quoted hex."""
    if hex6 is None:
        return None
    return TOKENS.get(hex6.upper(), f'"{hex6.upper()}"')


def _solid_child(parent):
    sf = parent.find(q(A, "solidFill"))
    if sf is None:
        return None
    s = sf.find(q(A, "srgbClr"))
    return s if s is not None else sf.find(q(A, "schemeClr"))


def _lnref_color(el, theme):
    """Border colour inherited from a shape's <p:style><a:lnRef> (schemeClr/srgbClr)."""
    style = el.find(q(P, "style"))
    lnRef = style.find(q(A, "lnRef")) if style is not None else None
    if lnRef is None:
        return None
    ref = lnRef.find(q(A, "schemeClr"))
    if ref is None:
        ref = lnRef.find(q(A, "srgbClr"))
    return color_lit(color_hex(ref, theme))


def _parse_pattfill(pat, theme):
    """<a:pattFill> -> {"prst", "fg", "bg"} for text_box(pattern_fill=...). fg/bg
    come back as a "scheme:NAME" ref (kept symbolic, e.g. tx1/bg1, so the key
    tracks the theme like the source) or a baked hex; an absent colour is omitted
    so text_box falls back to its tx1/bg1 default."""
    def _clr(tagname):
        wrap = pat.find(q(A, tagname))
        if wrap is None:
            return None
        sc = wrap.find(q(A, "schemeClr"))
        if sc is not None:
            return "scheme:" + sc.get("val")
        sr = wrap.find(q(A, "srgbClr"))
        return color_hex(sr, theme) if sr is not None else None
    d = {"prst": pat.get("prst", "pct50")}
    fg, bg = _clr("fgClr"), _clr("bgClr")
    if fg is not None:
        d["fg"] = fg
    if bg is not None:
        d["bg"] = bg
    return d


def py_str(s: str) -> str:
    return ((s or "").replace("\\", "\\\\").replace('"', '\\"')
            .replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t"))


# ── parse: source element -> record dict ──────────────────────────────────────
def parse_run(rPr, text, theme, shape_el=None):
    d = {"text": text or "", "size": None, "bold": False, "bold_explicit": False,
         "italic": False, "underline": False, "color": None, "hlink": None, "baseline": None}
    if rPr is not None:
        if rPr.get("sz"):
            d["size"] = int(rPr.get("sz"))
        d["bold"] = rPr.get("b") == "1"
        d["bold_explicit"] = rPr.get("b") is not None   # so style-bold baking yields to it
        d["italic"] = rPr.get("i") == "1"
        d["underline"] = rPr.get("u") not in (None, "none")
        # superscript/subscript offset: think-cell footnote markers (the small raised
        # "1"/"2"/"3") are runs with baseline="30000". 0 = the default, so drop it.
        if rPr.get("baseline") not in (None, "0"):
            d["baseline"] = int(rPr.get("baseline"))
        d["color"] = color_lit(color_hex(_solid_child(rPr), theme))
        hl = rPr.find(q(A, "hlinkClick"))   # external hyperlink -> capture the source rId
        if hl is not None:
            d["hlink"] = hl.get(q(R, "id"))
    # A run with no explicit fill inherits its colour from the shape's
    # <p:style><a:fontRef> (think-cell chips: white text via fontRef idx="minor"
    # -> schemeClr lt1). Without this the run falls back to the body default and a
    # white-on-dark chip renders as black-on-dark.
    if d["color"] is None and shape_el is not None:
        style = shape_el.find(q(P, "style"))
        fontRef = style.find(q(A, "fontRef")) if style is not None else None
        if fontRef is not None:
            ref = fontRef.find(q(A, "schemeClr"))
            if ref is None:
                ref = fontRef.find(q(A, "srgbClr"))
            d["color"] = color_lit(color_hex(ref, theme))
    return d


def parse_para(p, theme, shape_el=None):
    runs = []
    for ch in p:
        tag = ch.tag.split("}")[-1]
        if tag in ("r", "fld"):    # <a:fld> = think-cell label, frozen by reading its cache
            t = ch.find(q(A, "t"))
            runs.append(parse_run(ch.find(q(A, "rPr")), t.text if t is not None else "", theme, shape_el))
        elif tag == "br":          # explicit in-paragraph line break (think-cell wraps tight labels)
            runs.append({"break": True})
    pPr = p.find(q(A, "pPr"))
    pa = {"align": None, "level": 0, "marL": None, "indent": None,
          "space_after": None, "space_before": None, "line_spacing": None, "bullet": False,
          "bullet_char": None, "end_size": None, "runs": runs}
    # <a:endParaRPr> drives an EMPTY paragraph's height. think-cell collapses
    # spacer rows/cols by giving their empty cells a tiny font (e.g. sz=100 = 1pt);
    # capture it so empty cells reproduce that height instead of the 10pt default.
    epr = p.find(q(A, "endParaRPr"))
    if epr is not None and epr.get("sz"):
        pa["end_size"] = int(epr.get("sz"))
    if pPr is not None:
        pa["align"] = pPr.get("algn")
        pa["level"] = int(pPr.get("lvl")) if pPr.get("lvl") else 0
        pa["marL"] = int(pPr.get("marL")) if pPr.get("marL") is not None else None
        pa["indent"] = int(pPr.get("indent")) if pPr.get("indent") is not None else None
        sb = pPr.find(q(A, "spcBef") + "/" + q(A, "spcPts"))
        pa["space_before"] = int(sb.get("val")) if sb is not None else None
        sa = pPr.find(q(A, "spcAft") + "/" + q(A, "spcPts"))
        pa["space_after"] = int(sa.get("val")) if sa is not None else None
        ls = pPr.find(q(A, "lnSpc") + "/" + q(A, "spcPct"))
        pa["line_spacing"] = int(ls.get("val")) if ls is not None else None
        # bullet: <a:buChar char="•"/> (or "-" sub-bullet) -> that glyph;
        # <a:buAutoNum> -> "auto" (numbered); <a:buNone>/absent -> no bullet.
        buchar = pPr.find(q(A, "buChar"))
        if buchar is not None:
            pa["bullet"], pa["bullet_char"] = True, buchar.get("char", "•")
        elif pPr.find(q(A, "buAutoNum")) is not None:
            pa["bullet"], pa["bullet_char"] = True, "auto"
    return pa


def parse_sp(el, theme):
    spPr = el.find(q(P, "spPr"))
    nv = el.find(".//" + q(P, "cNvPr"))
    rec = {"type": "sp", "el": el, "name": nv.get("name", "Shape") if nv is not None else "Shape",
           "raw": None, "role": None}
    ph = el.find(".//" + q(P, "ph"))
    rec["ph"] = (ph.get("type"), ph.get("idx")) if ph is not None else None
    xfrm = spPr.find(q(A, "xfrm")) if spPr is not None else None
    if xfrm is None:
        rec["raw"] = "no explicit xfrm (layout placeholder)"
        return rec
    # gradient / picture fills have no param form -> verbatim. pattFill and
    # custGeom DO: a pattFill becomes text_box(pattern_fill=...), a custGeom
    # becomes custom_geometry() (finalized after the text body is parsed, below).
    for exotic in ("gradFill", "blipFill"):
        if spPr.find(q(A, exotic)) is not None:
            rec["raw"] = exotic
            return rec
    custgeom_el = spPr.find(q(A, "custGeom"))
    off, ext = xfrm.find(q(A, "off")), xfrm.find(q(A, "ext"))
    rec["x"], rec["y"] = int(off.get("x")), int(off.get("y"))
    rec["cx"], rec["cy"] = int(ext.get("cx")), int(ext.get("cy"))
    rec["rot"] = int(xfrm.get("rot")) if xfrm.get("rot") else 0
    pg = spPr.find(q(A, "prstGeom"))
    rec["prst"] = pg.get("prst") if pg is not None else "rect"
    rec["geom_adj"] = ({gd.get("name"): gd.get("fmla") for gd in pg.findall(q(A, "avLst") + "/" + q(A, "gd"))}
                       if pg is not None else {})
    # pattern fill (think-cell hatch pattern) -> a pattern_fill= param on text_box
    pat = spPr.find(q(A, "pattFill"))
    rec["pattern_fill"] = _parse_pattfill(pat, theme) if pat is not None else None
    rec["fill"] = "None" if spPr.find(q(A, "noFill")) is not None \
        else (color_lit(color_hex(_solid_child(spPr), theme)) or "None")
    # solidFill opacity (<a:alpha>): think-cell tints a panel by dropping a brand colour
    # to ~10% alpha; emitting the resolved colour alone (fully opaque) reads far too
    # strong. Capture it -> text_box(fill_alpha=) so the wash renders at source opacity.
    _alpha_clr = _solid_child(spPr)
    _alpha_el = _alpha_clr.find(q(A, "alpha")) if _alpha_clr is not None else None
    rec["fill_alpha"] = int(_alpha_el.get("val")) if (_alpha_el is not None and rec["fill"] != "None") else None
    # border: explicit ln colour, else inherit from <p:style><a:lnRef> (think-cell callouts)
    rec["line_color"], rec["line_width"], rec["dashed"] = '"none"', None, False
    ln = spPr.find(q(A, "ln"))
    if ln is not None and ln.find(q(A, "noFill")) is None:
        lc = color_lit(color_hex(_solid_child(ln), theme))
        if lc is None:
            lc = _lnref_color(el, theme)   # <a:ln w=..> with no fill inherits colour from the style
        if lc is not None:
            rec["line_color"] = lc
            w = ln.get("w")
            if w:
                rec["line_width"] = int(w)
            else:
                # explicit <a:ln> colour but no w: the WIDTH still inherits from the
                # shape's <p:style><a:lnRef idx=N> (theme lnStyleLst). think-cell's
                # scenario chips do this - a 1.5pt (idx 2 = 19050) border with an
                # explicit black fill; a naive read drops the width to the 1pt default.
                style = el.find(q(P, "style"))
                lnRef = style.find(q(A, "lnRef")) if style is not None else None
                if lnRef is not None and lnRef.get("idx") not in (None, "0"):
                    rec["line_width"] = theme.get("__lnw__", {}).get(int(lnRef.get("idx")))
            d = ln.find(q(A, "prstDash"))
            rec["dashed"] = d is not None and d.get("val") not in (None, "solid")
    elif ln is None:
        # No <a:ln> at all: the border (if any) comes entirely from the shape's
        # <p:style><a:lnRef idx=N> - colour from the ref, width from the theme's
        # line-style list at idx (idx 0 = no line). think-cell's Preliminary chip
        # relies on this; soffice/PowerPoint render it but a naive parse drops it.
        style = el.find(q(P, "style"))
        lnRef = style.find(q(A, "lnRef")) if style is not None else None
        if lnRef is not None and lnRef.get("idx") not in (None, "0"):
            lc = _lnref_color(el, theme)
            if lc is not None:
                rec["line_color"] = lc
                rec["line_width"] = theme.get("__lnw__", {}).get(int(lnRef.get("idx")))
    # shadow / glow (think-cell callouts) -> verbatim effectLst on text_box(effects=).
    # An EMPTY <a:effectLst/> carries no effect; treat it as None so it neither emits
    # dead markup nor (via is_simple) blocks the shape from clustering.
    eff = spPr.find(q(A, "effectLst"))
    rec["effects"] = _elem_inner_xml(eff) if (eff is not None and len(eff)) else None
    txBody = el.find(q(P, "txBody"))
    bodyPr = txBody.find(q(A, "bodyPr")) if txBody is not None else None
    rec["anchor"], rec["wrap"], rec["ins"], rec["vert"] = "t", "square", {}, None
    if bodyPr is not None:
        rec["anchor"] = bodyPr.get("anchor", "t")
        rec["wrap"] = bodyPr.get("wrap", "square")
        # vertical text (vert270 = read bottom-to-top): think-cell rotates tight
        # year/axis labels this way. Captured so it can re-emit, not flatten to horizontal.
        rec["vert"] = bodyPr.get("vert")
        for attr, kw in (("lIns", "l_ins"), ("tIns", "t_ins"), ("rIns", "r_ins"), ("bIns", "b_ins")):
            if bodyPr.get(attr) is not None:
                rec["ins"][kw] = int(bodyPr.get(attr))
    rec["paras"] = [parse_para(p, theme, el) for p in txBody.findall(q(A, "p"))] if txBody is not None else []
    # custom geometry: a freeform <a:custGeom> path. Text-free -> custom_geometry()
    # (the path stays verbatim; position / fill / line become params). With text we
    # can't reposition, or combined with a pattern fill, keep the whole shape raw.
    if custgeom_el is not None:
        has_text = any((r.get("text") or "").strip()
                       for p in rec["paras"] for r in p["runs"])
        if has_text or rec["pattern_fill"] is not None:
            rec["raw"] = "custGeom"
        else:
            rec["custgeom"] = _elem_inner_xml(custgeom_el)
    return rec


def parse_cxn(el, theme):
    spPr = el.find(q(P, "spPr"))
    nv = el.find(".//" + q(P, "cNvPr"))
    rec = {"type": "cxn", "el": el, "name": nv.get("name", "Connector") if nv is not None else "Connector",
           "raw": None, "role": None}
    xfrm = spPr.find(q(A, "xfrm"))
    if xfrm is None:
        rec["raw"] = "connector w/o xfrm"
        return rec
    off, ext = xfrm.find(q(A, "off")), xfrm.find(q(A, "ext"))
    rec["x"], rec["y"] = int(off.get("x")), int(off.get("y"))
    # Keep the source's positive bounding box + orientation EXPLICIT (flip/rot)
    # rather than folding flip into a signed cx/cy: the signed-vector trick shifts
    # the box, which silently mis-routes flipped/rotated elbows (rot was dropped
    # entirely, so a 90/270-deg elbow rendered unrotated and shot off-slide).
    rec["cx"], rec["cy"] = int(ext.get("cx")), int(ext.get("cy"))
    rec["flip_h"] = xfrm.get("flipH") == "1"
    rec["flip_v"] = xfrm.get("flipV") == "1"
    rec["rot"] = int(xfrm.get("rot") or 0)
    pg = spPr.find(q(A, "prstGeom"))
    rec["prst"] = pg.get("prst") if pg is not None else "line"
    rec["adj"] = {}
    av = pg.find(q(A, "avLst")) if pg is not None else None
    if av is not None:
        for gd in av.findall(q(A, "gd")):
            if (gd.get("name"), gd.get("fmla")) != ("adj1", "val 50000"):  # 50% = elbow default
                rec["adj"][gd.get("name")] = gd.get("fmla")
    rec["color"], rec["width"], rec["dash"], rec["arrow"] = "BLACK", 12700, None, False
    rec["grad"], rec["grad_angle"] = None, None
    ln = spPr.find(q(A, "ln"))
    if ln is not None:
        w = ln.get("w")
        rec["width"] = int(w) if w else 12700
        if ln.find(q(A, "noFill")) is not None:
            # invisible line: think-cell stacks an unfilled lgDash "anchor" under the
            # visible dashed line. Drawing it (the default BLACK) doubles every dashed
            # rule and muddies the dash pattern, so keep it noFill.
            rec["color"] = '"none"'
        else:
            lc = color_lit(color_hex(_solid_child(ln), theme))
            if lc is not None:
                rec["color"] = lc
        # gradient-filled line (think-cell's red->green confidence scale): capture the
        # stops + linear angle so it renders as a gradient, not the solid BLACK fallback.
        gf = ln.find(q(A, "gradFill"))
        if gf is not None:
            stops = []
            for gs in gf.findall(q(A, "gsLst") + "/" + q(A, "gs")):
                clr = gs.find(q(A, "srgbClr"))
                if clr is None:
                    clr = gs.find(q(A, "schemeClr"))
                hx = color_hex(clr, theme)
                if hx is not None:
                    stops.append((int(gs.get("pos", "0")), hx.upper()))
            if stops:
                rec["grad"] = stops
                lin = gf.find(q(A, "lin"))
                if lin is not None and lin.get("ang"):
                    rec["grad_angle"] = int(lin.get("ang"))
        # Preserve the exact prstDash preset (dash / lgDash / sysDash / ...) rather
        # than collapsing to a boolean; "solid" (or absent) means a solid line.
        pd = ln.find(q(A, "prstDash"))
        rec["dash"] = pd.get("val") if (pd is not None and pd.get("val") not in (None, "solid")) else None
        # An arrowhead only when a head/tail end is a REAL arrow type. think-cell
        # writes <a:tailEnd type="none"/> to SUPPRESS the theme default; the element
        # is present but draws nothing, so presence alone must not imply an arrow.
        def _real_end(tag):
            e = ln.find(q(A, tag))
            return e is not None and e.get("type") not in (None, "none")
        _head, _tail = _real_end("headEnd"), _real_end("tailEnd")
        rec["arrow"] = "both" if (_head and _tail) else ("head" if _head else ("tail" if _tail else False))
    return rec


def parse_table(el, theme, tstyles=None):
    """A <p:graphicFrame> wrapping an <a:tbl> -> table record. Merge-filler cells
    (hMerge/vMerge) are dropped; the engine re-synthesizes them from the anchor
    cell's grid_span/row_span. Per-cell fill / borders / insets / anchor / vert are
    kept. firstRow/firstCol BOLD that comes from the table STYLE (not explicit run
    formatting) is baked into the header runs so it survives the No-Style rebuild."""
    nv = el.find(".//" + q(P, "cNvPr"))
    xfrm = el.find(q(P, "xfrm"))
    off, ext = xfrm.find(q(A, "off")), xfrm.find(q(A, "ext"))
    tbl = el.find(".//" + q(A, "tbl"))
    grid = tbl.find(q(A, "tblGrid"))
    cols = [int(c.get("w")) for c in grid.findall(q(A, "gridCol"))]
    # Table-style-driven bold: a header can be bold purely because the table style's
    # firstRow/firstCol sets b="on" (with NO explicit run bold). Resolve which parts
    # the style bolds AND the tblPr flags enable, so the baking pass below can apply
    # it. The module rebuilds with No-Style-No-Grid, so an un-baked style bold is lost.
    tblPr = tbl.find(q(A, "tblPr"))
    style_bold = {}
    if tblPr is not None and tstyles:
        sid = tblPr.find(q(A, "tableStyleId"))
        parts = tstyles.get(sid.text, {}) if sid is not None else {}
        for part in ("firstRow", "firstCol"):
            if parts.get(part) and tblPr.get(part) in ("1", "true"):
                style_bold[part] = True
    rows = []
    for tr in tbl.findall(q(A, "tr")):
        cells = []
        for tc in tr.findall(q(A, "tc")):
            if tc.get("hMerge") == "1" or tc.get("vMerge") == "1":
                continue
            tcPr = tc.find(q(A, "tcPr"))
            cell = {"grid_span": int(tc.get("gridSpan") or 1),
                    "row_span": int(tc.get("rowSpan") or 1),
                    "fill": None, "anchor": "t", "vert": None, "l_ins": None, "r_ins": None,
                    "t_ins": None, "b_ins": None, "borders": {}}
            if tcPr is not None:
                if tcPr.find(q(A, "solidFill")) is not None:
                    cell["fill"] = color_lit(color_hex(_solid_child(tcPr), theme))
                # The OOXML table-cell default vertical anchor is TOP ("t"), not centre:
                # think-cell writes anchor="ctr"/"b" explicitly when it wants them and
                # leaves the attr off for top-aligned cells. Defaulting to "ctr" (the old
                # behaviour) mis-centred every unset cell — definition rows, header labels.
                cell["anchor"] = tcPr.get("anchor", "t")
                cell["vert"] = tcPr.get("vert")   # vert270 etc. -> rotated spine labels
                if tcPr.get("marL") is not None:
                    cell["l_ins"] = int(tcPr.get("marL"))
                if tcPr.get("marR") is not None:
                    cell["r_ins"] = int(tcPr.get("marR"))
                if tcPr.get("marT") is not None:
                    cell["t_ins"] = int(tcPr.get("marT"))
                if tcPr.get("marB") is not None:
                    cell["b_ins"] = int(tcPr.get("marB"))
                for side, key in (("lnL", "L"), ("lnR", "R"), ("lnT", "T"), ("lnB", "B")):
                    ln = tcPr.find(q(A, side))
                    if ln is None:
                        continue
                    if ln.find(q(A, "noFill")) is not None:
                        cell["borders"][key] = "none"
                    elif ln.find(q(A, "solidFill")) is not None:
                        cell["borders"][key] = {"color": color_hex(_solid_child(ln), theme),
                                                "width": int(ln.get("w") or 12700)}
            txBody = tc.find(q(A, "txBody"))
            cell["paras"] = [parse_para(p, theme) for p in txBody.findall(q(A, "p"))] if txBody is not None else []
            cells.append(cell)
        rows.append({"h": int(tr.get("h") or 0), "cells": cells})
    # Bake style firstRow/firstCol bold into the header runs (explicit run bold wins).
    if style_bold:
        for ri, row in enumerate(rows):
            for ci, cell in enumerate(row["cells"]):
                if (style_bold.get("firstRow") and ri == 0) or \
                   (style_bold.get("firstCol") and ci == 0):
                    for p in cell["paras"]:
                        for r in p["runs"]:
                            if not r.get("break") and not r.get("bold_explicit"):
                                r["bold"] = True
    return {"type": "table", "el": el, "raw": None, "role": None,
            "name": nv.get("name", "Table") if nv is not None else "Table",
            "x": int(off.get("x")), "y": int(off.get("y")),
            "cx": int(ext.get("cx")), "cy": int(ext.get("cy")), "cols": cols, "rows": rows}


# ── render: record -> Python call string ──────────────────────────────────────
def render_run(d, text_override=None):
    if d.get("break"):
        return "line_break()"
    parts = [text_override if text_override is not None else f'"{py_str(d["text"])}"']
    if d["size"] is not None:
        parts.append(f"size={sizelit(d['size'])}")
    if d["bold"]:
        parts.append("bold=True")
    if d["italic"]:
        parts.append("italic=True")
    if d.get("underline"):
        parts.append("underline=True")
    if d.get("baseline") is not None:
        parts.append(f"baseline={d['baseline']}")
    if d["color"] is not None:
        parts.append(f"color={d['color']}")
    if d.get("hlink") and d["hlink"] in _HLINKS:
        parts.append(f'hyperlink_rid="{_HLINKS[d["hlink"]]}"')
    parts.append("font=FONT")
    return f"run({', '.join(parts)})"


def render_para(pa, text_override=None):
    if pa["runs"]:
        if text_override is not None and len(pa["runs"]) == 1:
            runs = [render_run(pa["runs"][0], text_override)]
        else:
            runs = [render_run(r) for r in pa["runs"]]
        runs_str = "[" + ", ".join(runs) + "]"
    else:
        runs_str = "[]"
    kw = []
    if pa["align"]:
        kw.append(f'align="{pa["align"]}"')
    if pa["level"]:
        kw.append(f"level={pa['level']}")
    if pa["marL"] is not None:
        kw.append(f"mar_l={pa['marL']}")
    if pa["indent"] is not None:
        kw.append(f"indent={pa['indent']}")
    if pa.get("space_before") is not None:
        kw.append(f"space_before={pa['space_before']}")
    if pa["space_after"] is not None:
        kw.append(f"space_after={pa['space_after']}")
    # deck_core paragraph() defaults to 115% (LNSPC_BODY house style); a ported text
    # box with no explicit lnSpc renders at the 100% default. Emit the source's
    # effective spacing so deck_core's 115% doesn't inflate a tight box (overflow).
    ls = pa["line_spacing"] if pa["line_spacing"] is not None else 100000
    if ls != 115000:
        kw.append(f"line_spacing={ls}")
    if pa["bullet"]:
        kw.append("bullet=True")
        bc = pa.get("bullet_char")
        if bc and bc != "•":
            kw.append(f'bullet_char="{py_str(bc)}"')
    return f"paragraph({runs_str}{(', ' + ', '.join(kw)) if kw else ''})"


def render_sp(rec, id_expr, varmap=None):
    """Render a text_box() call. varmap maps a varying field -> a loop-variable name
    (used inside a cluster loop); fields absent from varmap use the record's literal."""
    varmap = varmap or {}

    def v(field, lit):
        return varmap[field] if field in varmap else lit

    if "text" in varmap and len(rec["paras"]) == 1:
        paras_str = "[" + render_para(rec["paras"][0], varmap["text"]) + "]"
    elif rec["paras"]:
        paras_str = "[" + ", ".join(render_para(p) for p in rec["paras"]) + "]"
    else:
        paras_str = "[paragraph([])]"
    args = [id_expr, f'"{py_str(rec["name"])}"',
            v("x", coordlit(rec["x"])), v("y", coordlit(rec["y"])),
            v("cx", coordlit(rec["cx"])), v("cy", coordlit(rec["cy"])), paras_str]
    kw = [f"fill={v('fill', rec['fill'])}", f"line_color={v('line_color', rec['line_color'])}"]
    if rec.get("fill_alpha") is not None:
        kw.append(f"fill_alpha={rec['fill_alpha']}")
    if rec.get("pattern_fill"):
        pf = rec["pattern_fill"]
        pf_items = [f'"prst": "{pf["prst"]}"']
        if "fg" in pf:
            pf_items.append(f'"fg": "{pf["fg"]}"')
        if "bg" in pf:
            pf_items.append(f'"bg": "{pf["bg"]}"')
        kw.append("pattern_fill={" + ", ".join(pf_items) + "}")
    if rec["line_width"] is not None and rec["line_width"] != 12700:
        kw.append(f"line_width={rec['line_width']}")
    if rec["dashed"]:
        kw.append("dashed_line=True")
    if rec["prst"] != "rect":
        kw.append(f'prst="{rec["prst"]}"')
    if "geom_adj" in varmap:
        kw.append(f"geom_adj={varmap['geom_adj']}")
    elif rec["geom_adj"]:
        kw.append("geom_adj={" + ", ".join(f'"{k}": "{val}"' for k, val in rec["geom_adj"].items()) + "}")
    if rec["anchor"] != "t":
        kw.append(f'anchor="{rec["anchor"]}"')
    if rec["wrap"] != "square":
        kw.append(f'wrap="{rec["wrap"]}"')
    if rec.get("vert"):
        kw.append(f'vert="{rec["vert"]}"')
    for k, val in rec["ins"].items():
        kw.append(f"{k}={val}")
    if rec.get("rot"):
        kw.append(f"rot={rec['rot']}")
    if rec.get("effects"):
        kw.append("effects=" + '"' + rec["effects"].replace("\\", "\\\\").replace('"', '\\"') + '"')
    return f"text_box({', '.join(args)}, {', '.join(kw)})"


def render_cxn(rec, id_expr, coords=None):
    coords = coords or {}

    def c(field):
        return coords.get(field, coordlit(rec[field]))

    kw = [f"color={rec['color']}", f"width={rec['width']}"]
    if rec.get("grad"):
        kw.append("grad=[" + ", ".join(f'({pos}, "{c}")' for pos, c in rec["grad"]) + "]")
        if rec.get("grad_angle") is not None:
            kw.append(f"grad_angle={rec['grad_angle']}")
    if rec["dash"]:
        kw.append(f'dash="{rec["dash"]}"')
    if rec["arrow"]:
        kw.append(f'arrow="{rec["arrow"]}"')
    if rec["prst"] not in ("line", "straightConnector1"):
        kw.append(f'prst="{rec["prst"]}"')
    if rec.get("flip_h"):
        kw.append("flip_h=True")
    if rec.get("flip_v"):
        kw.append("flip_v=True")
    if rec.get("rot"):
        kw.append(f"rot={rec['rot']}")
    if rec.get("adj"):
        kw.append("adj={" + ", ".join(f'"{k}": "{v}"' for k, v in rec["adj"].items()) + "}")
    return (f'connector({id_expr}, "{py_str(rec["name"])}", '
            f'{c("x")}, {c("y")}, {c("cx")}, {c("cy")}, {", ".join(kw)})')


def render_chrome(rec):
    role, data = rec["role"]
    if role == "breadcrumb":
        return f'breadcrumb("{py_str(data[0])}", "{py_str(data[1])}")'
    if role == "title":
        cx = data[2] if len(data) > 2 else None
        cx_arg = f", cx={coordlit(cx)}" if (cx is not None and abs(cx - HOUSE_TITLE_CX) > TOL) else ""
        return f'title_placeholder("{py_str(data[0])}", "{py_str(data[1])}"{cx_arg})'
    if role == "prelim":
        return "prelim_chip()" if data is None else f'prelim_chip(text="{py_str(data)}")'
    if role == "sources":
        return f'sources_line("{py_str(data)}")'
    return ""


def render_trun(r):
    if r.get("break"):
        return "tbreak()"
    a = [f'"{py_str(r["text"])}"']
    if r["size"] is not None:
        a.append(f"size={sizelit(r['size'])}")
    if r["bold"]:
        a.append("bold=True")
    if r["italic"]:
        a.append("italic=True")
    if r.get("underline"):
        a.append("underline=True")
    if r.get("baseline") is not None:
        a.append(f"baseline={r['baseline']}")
    if r["color"] is not None:
        a.append(f"color={r['color']}")
    if r.get("hlink") and r["hlink"] in _HLINKS:
        a.append(f'hyperlink_rid="{_HLINKS[r["hlink"]]}"')
    a.append("font=FONT")
    return f"trun({', '.join(a)})"


def render_tpara(p):
    runs = ", ".join(render_trun(r) for r in p["runs"])
    kw = []
    if p["align"] and p["align"] != "l":
        kw.append(f'align="{p["align"]}"')
    if p.get("bullet"):
        kw.append("bullet=True")
        bc = p.get("bullet_char")
        if bc and bc != "•":
            kw.append(f'bullet_char="{py_str(bc)}"')
    if p.get("level"):
        kw.append(f"level={p['level']}")
    if p.get("marL") is not None:
        kw.append(f"mar_l={p['marL']}")
    if p.get("indent") is not None:
        kw.append(f"indent={p['indent']}")
    if p.get("line_spacing") is not None and p["line_spacing"] != 100000:
        kw.append(f"line_spacing={p['line_spacing']}")
    if p.get("space_before") is not None:
        kw.append(f"space_before={p['space_before']}")
    if p.get("space_after") is not None:
        kw.append(f"space_after={p['space_after']}")
    # An EMPTY paragraph (a spacer line between bullets, or a collapsed spacer row)
    # carries its height in <a:endParaRPr sz>. Without re-emitting it the blank line
    # renders at the renderer's default size — bloating inter-bullet gaps (the RHS
    # commentary cells) and over-tall spacer rows (the 1pt spacer rows). cell() does
    # this already for its shortcut path; rcell()'s paragraphs went without.
    if not p["runs"] and p.get("end_size") is not None:
        kw.append(f"end_size={sizelit(p['end_size'])}")
    return f"tpara([{runs}]{(', ' + ', '.join(kw)) if kw else ''})"


def _edge_lit(b):
    """A border edge -> edge(...) literal; the "none" sentinel -> None so the caller drops it
    (an omitted side renders <a:noFill/>, identical to an explicit "none")."""
    if b == "none":
        return None
    w = b["width"]
    return f"edge({color_lit(b['color'])}" + (f", {w}" if w != 12700 else "") + ")"


def _border_kw(borders):
    """L/R/T/B=edge(...) kwargs for the drawn sides only (omitted sides render no-fill)."""
    out = []
    for side in ("L", "R", "T", "B"):
        v = (borders or {}).get(side)
        if v is None:
            continue
        lit = _edge_lit(v)
        if lit is not None:
            out.append(f"{side}={lit}")
    return out


def _inset_kw(c):
    """Insets -> ['**PAD'] when all four are the source's 60960, [] when all are the engine
    default 45720, else explicit l_ins=.. for each non-default side."""
    vals = {k: (c.get(k) if c.get(k) is not None else 45720)
            for k in ("l_ins", "r_ins", "t_ins", "b_ins")}
    if all(v == 60960 for v in vals.values()):
        return ["**PAD"]
    return [f"{k}={v}" for k, v in vals.items() if v != 45720]


def render_cell(c):
    fill_kw = [f"fill={c['fill']}"] if (c["fill"] and c["fill"] != "None") else []
    span_kw = []
    if c["grid_span"] > 1:
        span_kw.append(f"span={c['grid_span']}")
    if c["row_span"] > 1:
        span_kw.append(f"rowspan={c['row_span']}")
    anchor_kw = [f'anchor="{c["anchor"]}"'] if (c["anchor"] and c["anchor"] != "ctr") else []
    vert_kw = [f'vert="{c["vert"]}"'] if c.get("vert") else []   # vert270 spine labels
    mech = fill_kw + anchor_kw + vert_kw + span_kw + _inset_kw(c) + _border_kw(c["borders"])
    paras = c["paras"]
    # cell() is a single-run shortcut with no bullet/indent support, so a cell whose lone
    # paragraph is bulleted or hanging-indented must take the rich rcell() path.
    plain = (not paras) or not (paras[0].get("bullet") or paras[0].get("marL") is not None
                                or paras[0].get("indent") is not None or paras[0].get("level"))
    if plain and len(paras) <= 1 and (not paras or len(paras[0]["runs"]) <= 1):   # cell() shortcut
        run = paras[0]["runs"][0] if (paras and paras[0]["runs"]) else None
        a = [f'"{py_str(run["text"]) if run else ""}"']
        if run:
            if run["size"] is not None:
                a.append(f"size={sizelit(run['size'])}")
            if run["bold"]:
                a.append("bold=True")
            if run["italic"]:
                a.append("italic=True")
            if run["color"] is not None:
                a.append(f"color={run['color']}")
        elif paras and paras[0].get("end_size") is not None:
            # empty cell: keep its <a:endParaRPr> font size so spacer rows/cols
            # stay collapsed (think-cell uses a 1pt font; the 10pt default bloats them)
            a.append(f"size={sizelit(paras[0]['end_size'])}")
        if paras and paras[0]["align"] and paras[0]["align"] != "l":
            a.append(f'align="{paras[0]["align"]}"')
        return f"cell({', '.join(a + mech)})"
    paras_str = ", ".join(render_tpara(p) for p in paras)
    return f"rcell([{paras_str}]{(', ' + ', '.join(mech)) if mech else ''})"


def render_table(rec, id_expr):
    cols = ", ".join(coordlit(w) for w in rec["cols"])
    rowlines = [f"        trow([{', '.join(render_cell(c) for c in r['cells'])}], h={coordlit(r['h'])}),"
                for r in rec["rows"]]
    return (f'table({id_expr}, "{py_str(rec["name"])}", {coordlit(rec["x"])}, {coordlit(rec["y"])}, '
            f'{coordlit(rec["cx"])}, {coordlit(rec["cy"])}, col_widths=[{cols}], rows=[\n'
            + "\n".join(rowlines) + "\n    ])")


# ── raw fallback ─────────────────────────────────────────────────────────────
_CRUFT = {q(P, "custDataLst"), q(P, "extLst"), q(A, "extLst"),
          q(A, "hlinkClick"), q(A, "hlinkHover")}


def _strip_cruft(elem):
    for child in list(elem):
        if child.tag in _CRUFT:
            elem.remove(child)
        else:
            _strip_cruft(child)
    return elem


def _strip_ns_decls(xml: str) -> str:
    """Drop the xmlns:a/p/r/c declarations ElementTree adds when serializing a
    subtree standalone — they are already declared on the slide root the string
    is embedded into."""
    for decl in (f' xmlns:a="{A}"', f' xmlns:p="{P}"', f' xmlns:r="{R}"', f' xmlns:c="{C}"'):
        xml = xml.replace(decl, "")
    return xml


def _elem_inner_xml(elem) -> str:
    """An element serialized to namespace-prefixed XML with the xmlns
    declarations stripped — used to lift a verbatim <a:custGeom> path into a
    module constant (custom_geometry() supplies the surrounding <p:sp>)."""
    return _strip_ns_decls(ET.tostring(elem, encoding="unicode"))


def raw_literal(elem, new_id: int) -> str:
    _strip_cruft(elem)
    nv = elem.find(".//" + q(P, "cNvPr"))
    if nv is not None:
        nv.set("id", str(new_id))
    xml = _strip_ns_decls(ET.tostring(elem, encoding="unicode"))
    return '"' + xml.replace("\\", "\\\\").replace('"', '\\"') + '"'


# ── detection ────────────────────────────────────────────────────────────────
def rec_text(rec):
    return "".join(r.get("text", "") for p in rec["paras"] for r in p["runs"])


def rec_first_bold(rec):
    for p in rec["paras"]:
        for r in p["runs"]:
            return r["bold"]
    return False


def _near(x, y, kind):
    hx, hy = HOUSE_POS[kind]
    return abs(x - hx) <= TOL and abs(y - hy) <= TOL


def detect_chrome(items):
    """Tag records that are standard chrome AND sit within tolerance of the house
    position (so swapping in the builder doesn't move them). Returns a list of
    (kind, moved) notes for divergent chrome left verbatim."""
    notes = []
    for rec in items:
        if rec["type"] != "sp" or rec["raw"]:
            continue
        text = rec_text(rec).strip()
        ph = rec.get("ph")
        x, y = rec["x"], rec["y"]
        if text == "Preliminary":
            if _near(x, y, "prelim"):
                rec["role"] = ("prelim", None)
            else:
                notes.append("Preliminary chip off house position - kept verbatim")
            continue
        if y < 400000 and "/" in text and rec_first_bold(rec):
            if _near(x, y, "breadcrumb"):
                sec, _, top = text.partition("/")
                rec["role"] = ("breadcrumb", (sec.strip(), top.strip()))
            else:
                notes.append("breadcrumb-like shape off house position - kept verbatim")
            continue
        if text.startswith(("Note:", "Source:", "Sources:")):   # before title: a footnote may contain " | "
            if any(r.get("hlink") for p in rec["paras"] for r in p["runs"]):
                # the house sources_line builder takes a FLAT string and would drop the
                # per-run external links; keep the footnote verbatim so its hlinkClick
                # runs survive (text_box -> render_run emits hyperlink_rid).
                notes.append("Source line carries hyperlinks - kept verbatim to preserve them")
            elif _near(x, y, "sources"):
                rec["role"] = ("sources", text)
            else:
                notes.append("Note/Source line off house position - kept verbatim")
            continue
        if (ph and ph[0] == "title") or " | " in text:
            if (ph and ph[0] == "title") or _near(x, y, "title"):
                topic, _, takeaway = text.partition(" | ")
                # carry the source title width: think-cell narrows it on slides with
                # top-right logos so the takeaway clears them; the house builder would
                # otherwise force full width and run the title text under the logos.
                rec["role"] = ("title", (topic.strip(), takeaway.strip(), rec.get("cx")))
            else:
                notes.append("title-like shape off house position - kept verbatim")
            continue
    return notes


def is_simple(rec):
    # pattern_fill / custgeom / effects shapes carry a fill, geometry, or shadow the
    # cluster machinery (which only varies x/y/cx/cy/fill/line/text/geom_adj) can't
    # reproduce, so keep them standalone — they emit text_box(pattern_fill=/effects=)
    # or custom_geometry() instead. (A shadowed callout collapsed into a same-style
    # loop would otherwise silently lose its effectLst.)
    return (rec["type"] == "sp" and not rec["raw"] and not rec["role"]
            and not rec.get("pattern_fill") and not rec.get("custgeom")
            and not rec.get("effects") and not rec.get("fill_alpha")
            and len(rec["paras"]) <= 1
            and (not rec["paras"] or len(rec["paras"][0]["runs"]) <= 1))


def const_key(rec):
    p = rec["paras"][0] if rec["paras"] else None
    r = next((x for x in p["runs"] if not x.get("break")), None) if p else None
    return (rec["prst"], rec["line_width"], rec["dashed"], rec["anchor"], rec["wrap"], rec.get("vert"),
            tuple(sorted(rec["ins"].items())), rec.get("rot", 0),
            tuple(sorted(rec["geom_adj"].keys())),
            p["align"] if p else None, p["level"] if p else 0,
            p["marL"] if p else None, p["indent"] if p else None,
            p["space_after"] if p else None, p["line_spacing"] if p else None,
            p["bullet"] if p else False,
            r["size"] if r else None, r["bold"] if r else False,
            r["italic"] if r else False, r["color"] if r else None, r is not None)


def _member_text(rec):
    return rec["paras"][0]["runs"][0].get("text", "") if (rec["paras"] and rec["paras"][0]["runs"]) else ""


def _bbox_overlap(a, b):
    return (a["x"] < b["x"] + b["cx"] and a["x"] + a["cx"] > b["x"]
            and a["y"] < b["y"] + b["cy"] and a["y"] + a["cy"] > b["y"])


def _cluster_z_safe(items, idxs):
    """A cluster is emitted as ONE loop at the FIRST member's z-position, so every
    member jumps to the front of the run. That is paint-safe only when no non-member
    drawable interleaved among the members (in document/paint order) overlaps a member
    that would jump ahead of it — otherwise that shape paints over/under the wrong
    neighbour (e.g. the confidence-scale arrow landing on top of its label)."""
    member_set = set(idxs)
    for j in range(min(idxs) + 1, max(idxs)):
        if j in member_set:
            continue
        rj = items[j]
        if rj.get("type") not in ("sp", "cxn") or rj.get("raw"):
            continue
        if not all(isinstance(rj.get(k), int) for k in ("x", "y", "cx", "cy")):
            continue
        if any(m > j and _bbox_overlap(rj, items[m]) for m in idxs):
            return False
    return True


def detect_clusters(items):
    groups = {}
    for i, rec in enumerate(items):
        if is_simple(rec):
            groups.setdefault(const_key(rec), []).append(i)
    clusters = []
    for idxs in groups.values():
        if len(idxs) < MIN_CLUSTER:
            continue
        if not _cluster_z_safe(items, idxs):   # clustering would reorder a paint-overlapping shape
            continue
        varying = []
        for field in ("x", "y", "cx", "cy", "fill", "line_color"):
            if len({items[i][field] for i in idxs}) > 1:
                varying.append(field)
        if len({_member_text(items[i]) for i in idxs}) > 1:
            varying.append("text")
        if any(items[i]["geom_adj"] for i in idxs):
            if len({tuple(sorted(items[i]["geom_adj"].items())) for i in idxs}) > 1:
                varying.append("geom_adj")
        varying = [f for f in VARYING_ORDER if f in varying]
        clusters.append({"idxs": idxs, "varying": varying, "leader": idxs[0]})
    return clusters


# Affordance vocabulary: map a style-cluster to a reusable, semantic VARIABLE name
# (what the shapes are/do on the canvas). These names never enter the produced XML —
# they only name the Python data table + its anchor constants — so re-conversion can
# emit them freely without changing one rendered byte. The shape-name string
# (cNvPr/@name) is chosen separately in cluster_identity and kept byte-faithful.
_MATH_PRST = re.compile(r"^math(?:Equal|Plus|Minus|Multiply|Divide|NotEqual)$")
_YEAR_TICK = re.compile(r"^(?:(?:19|20)\d\d|FY ?\d{2}(?:\d\d)?)$")
_NUMERIC_LBL = re.compile(r"^[~<>]?\$?-?\d[\d,. ]*%?$")


def affordance_name(lead, texts):
    """Best-effort affordance classification -> (table var name, anchor prefix).
    Heuristic and intentionally conservative: it nails the high-confidence cases
    (operators, callouts, chevrons, rings, year ticks, legend keys, numeric data
    labels, filled flow nodes) and otherwise falls back to a generic _LABELS /
    _GROUP that a human specializes. VARIABLE names only -- never the shape string."""
    prst = lead.get("prst") or "rect"
    filled = lead.get("fill", "None") != "None"
    ne = [(t or "").strip() for t in texts if (t or "").strip()]
    empty = not ne
    if _MATH_PRST.match(prst):                       # = + x / glyphs (operator glyphs, not legend keys)
        return "_OPERATOR_GLYPHS", "OP"
    if "Callout" in prst:                            # wedgeRectCallout, borderCallout, cloudCallout
        return "_CALLOUTS", "CALLOUT"
    if prst in ("chevron", "homePlate"):             # value-chain stage headers
        return "_STAGE_HEADERS", "STAGE"
    if prst == "ellipse" and empty and not filled:   # empty outline rings emphasizing chart numbers
        return "_HIGHLIGHT_RINGS", "RING"
    if ne and not filled and all(_YEAR_TICK.match(t) for t in ne):
        return "_CATEGORY_TICK_LABELS", "TICK"       # year / FY ticks under a chart axis
    if empty and filled:                             # filled, textless color chips/keys
        return "_LEGEND_KEYS", "KEY"
    if ne and all(_NUMERIC_LBL.match(t) for t in ne):
        return "_DATA_LABELS", "DLBL"                # numeric values riding marks (filled chips ok)
    if filled and ne:                                # filled boxes carrying text
        return "_FLOW_NODES", "NODE"
    if ne and not filled:                            # no-fill captions -> human specializes the role
        return "_LABELS", "LBL"
    return "_GROUP", "G"


def cluster_identity(items, cl, used):
    """Infer a cluster's identity -> (data-table var name, const-anchor prefix,
    shape-name string). The shape-name string (sn) keeps the ORIGINAL heuristic so
    cNvPr/@name -- and thus the produced XML -- stays byte-identical to prior output;
    the table var + anchor prefix take the affordance vocabulary (variables only)."""
    texts = [_member_text(items[i]) for i in cl["idxs"]]
    lead = items[cl["leader"]]
    # shape-name string (cNvPr/@name) -- UNCHANGED logic; XML-bearing, do not alter
    if lead["prst"] == "wedgeRectCallout":
        sn = "Callout"
    elif all(re.fullmatch(r"(19|20)\d\d", (t or "").strip()) for t in texts):
        sn = "YearLabel"
    elif all((t or "").strip() == "" for t in texts) and lead["fill"] != "None":
        sn = "LegendColorKey"
    elif all(re.fullmatch(r"~?\d{1,3}%?", (t or "").strip()) for t in texts if t):
        sn = "ValueLabel"
    elif all((t or "").strip() for t in texts):
        sn = "Label"
    else:
        sn = "Shape"
    # affordance VARIABLE name + anchor prefix -- semantic; never in XML
    base, pfx = affordance_name(lead, texts)
    name, k = base, 2
    while name in used:
        name, k = f"{base}{k}", k + 1
    used.add(name)
    pfx += name[len(base):]   # keep the const prefix unique in lockstep with the table name
    return name, pfx, sn


def render_value(rec, field):
    if field in ("x", "y", "cx", "cy"):
        return coordfloat(rec[field])
    if field == "fill":
        return rec["fill"]
    if field == "line_color":
        return rec["line_color"]
    if field == "text":
        return f'"{py_str(_member_text(rec))}"'
    if field == "geom_adj":
        return "{" + ", ".join(f'"{k}": "{v}"' for k, v in rec["geom_adj"].items()) + "}"
    return "None"


# ── chart rels ───────────────────────────────────────────────────────────────
def slide_rels(z, slide_no):
    root = ET.fromstring(z.read(f"ppt/slides/_rels/slide{slide_no}.xml.rels"))
    return {r.get("Id"): r.get("Target") for r in root}


def hyperlink_rels(z, slide_no):
    """{rId: external URL} for the slide's hyperlink relationships (TargetMode=External)."""
    try:
        root = ET.fromstring(z.read(f"ppt/slides/_rels/slide{slide_no}.xml.rels"))
    except KeyError:
        return {}
    return {r.get("Id"): r.get("Target") for r in root
            if (r.get("Type") or "").endswith("/hyperlink")}


def source_layout_name(z, slide_no):
    """The <p:cSld name> of the slideLayout this source slide references (e.g.
    'Light Blank', '50% Block + Title'), or None. Used to pick the matching house
    layout by name rather than forcing every slide onto the body layout."""
    try:
        rels = ET.fromstring(z.read(f"ppt/slides/_rels/slide{slide_no}.xml.rels"))
    except KeyError:
        return None
    tgt = next((r.get("Target") for r in rels
                if (r.get("Type") or "").endswith("/slideLayout")), None)
    if not tgt:
        return None
    layout_part = "ppt/" + tgt.split("../", 1)[-1]
    try:
        csld = ET.fromstring(z.read(layout_part)).find(q(P, "cSld"))
    except KeyError:
        return None
    return csld.get("name") if csld is not None else None


def chart_xlsb(z, chart_target):
    chart_path = "ppt/" + chart_target.split("../", 1)[-1]
    chart_no = "".join(c for c in chart_path.rsplit("/", 1)[-1] if c.isdigit())
    chart_xml = z.read(chart_path).decode("utf-8")
    rels = ET.fromstring(z.read(f"ppt/charts/_rels/chart{chart_no}.xml.rels"))
    xlsb = None
    for r in rels:
        if r.get("Target").lower().endswith((".xlsb", ".xlsx")):
            xlsb = z.read("ppt/" + r.get("Target").split("../", 1)[-1])
    return chart_xml, xlsb, chart_no


# ── chart data extraction (for styled_chart, data-over-template) ───────────────
# Mirrors deck_core.charts.extract_chart_data but stdlib-only and trimmed to the
# fields the emitted _DATA literal needs (categories + per-series name/values),
# keeping this tool copy-next-to-any-pipeline. Series come out in document order
# across every chart-type container (barChart then lineChart, ...) — the order
# styled_chart rewrites — so the round-trip reproduces the source, combos included.
def _chart_series_els(root):
    chart = root.find(q(C, "chart"))
    plot = (chart.find(q(C, "plotArea")) if chart is not None
            else root.find(".//" + q(C, "plotArea")))
    if plot is None:
        return []
    out = []
    for cont in list(plot):
        if cont.tag.split("}")[-1].endswith("Chart"):
            out.extend(cont.findall(q(C, "ser")))
    return out


def _cache_list(parent, *, numeric):
    """Ordered values from a <c:cat>/<c:val>/<c:tx> cache (None at blanks), or
    None when the parent/cache is absent."""
    if parent is None:
        return None
    node = None
    for kind in ("numCache", "strCache", "numLit", "strLit"):
        node = parent.find(".//" + q(C, kind))
        if node is not None:
            break
    if node is None:
        return None
    by_idx = {}
    for pt in node.findall(q(C, "pt")):
        v = pt.find(q(C, "v"))
        by_idx[int(pt.get("idx"))] = v.text if v is not None else None
    pc = node.find(q(C, "ptCount"))
    n = int(pc.get("val")) if pc is not None else 0
    n = max(n, (max(by_idx) + 1) if by_idx else 0)
    out = [by_idx.get(i) for i in range(n)]
    if numeric:
        out = [None if x in (None, "") else round(float(x), 4) for x in out]
    return out


def extract_chart_data(chart_xml):
    """Chart part -> {categories, series:[{name, values}]} for a styled_chart
    _DATA literal. categories / name come back None when the chart omits them
    (think-cell draws those as separate slide shapes)."""
    root = ET.fromstring(chart_xml)
    series, categories = [], None
    for ser in _chart_series_els(root):
        if categories is None:
            categories = _cache_list(ser.find(q(C, "cat")), numeric=False)
        tx = ser.find(q(C, "tx"))
        name = None
        if tx is not None:
            nm = _cache_list(tx, numeric=False)
            if nm:
                name = next((x for x in nm if x), None)
            elif tx.find(q(C, "v")) is not None:
                name = tx.find(q(C, "v")).text
        series.append({"name": name,
                       "values": _cache_list(ser.find(q(C, "val")), numeric=True) or []})
    return {"categories": categories, "series": series}


# ── main ─────────────────────────────────────────────────────────────────────
def _pic_record(el, rels):
    """Parse a <p:pic> into a 'pic' item (or a 'drop' if it lacks media/geometry).
    Coordinates are the element's own; flatten_group re-maps them into slide space."""
    blip = el.find(".//" + q(A, "blip"))
    tgt = rels.get(blip.get(q(R, "embed")), "") if blip is not None else ""
    xfrm = el.find(".//" + q(A, "xfrm"))
    off = xfrm.find(q(A, "off")) if xfrm is not None else None
    ext = xfrm.find(q(A, "ext")) if xfrm is not None else None
    cNvPr = el.find(".//" + q(P, "cNvPr"))
    nm = (cNvPr.get("name") if cNvPr is not None else "") or "Picture"
    if not tgt or off is None or ext is None:
        return {"type": "drop",
                "comment": f"DROPPED <p:pic> {(tgt.rsplit('/', 1)[-1] or '?')} (no media target or geometry)"}
    # <a:srcRect> crops the source image (l/r/t/b, 1/1000 %). Source decks crop a
    # logo strip out of a square canvas; keep it or the logo stretches to a sliver.
    sr = el.find(".//" + q(A, "srcRect"))
    src_rect = {k: int(v) for k, v in sr.attrib.items()} if (sr is not None and sr.attrib) else None
    return {"type": "pic", "name": nm, "target": tgt,
            "is_emf": tgt.lower().endswith(".emf"), "src_rect": src_rect,
            "x": int(off.get("x")), "y": int(off.get("y")),
            "cx": int(ext.get("cx")), "cy": int(ext.get("cy"))}


def flatten_group(grp, theme, rels, notes, parent_tx=None):
    """Flatten a <p:grpSp> into item records mapped into slide (parent) space.

    A group nests a child coordinate system: a child at (x, y) maps to
    off + (x - chOff) * (ext / chExt). Nested groups compose by threading the outer
    transform. Group rotation/flip is NOT applied to children (the schematic icon
    groups carry none); a rotated group is noted so the omission isn't silent."""
    xf = grp.find(q(P, "grpSpPr") + "/" + q(A, "xfrm"))
    nm = grp.find(".//" + q(P, "cNvPr"))
    gname = nm.get("name") if nm is not None else "Group"
    if xf is None:
        notes.append(f"group {gname!r} has no xfrm - skipped")
        return []
    if xf.get("rot") or xf.get("flipH") or xf.get("flipV"):
        notes.append(f"group {gname!r} is rotated/flipped - children placed without that transform")
    off, ext = xf.find(q(A, "off")), xf.find(q(A, "ext"))
    chOff, chExt = xf.find(q(A, "chOff")), xf.find(q(A, "chExt"))
    ox, oy = int(off.get("x")), int(off.get("y"))
    chx, chy = (int(chOff.get("x")), int(chOff.get("y"))) if chOff is not None else (0, 0)
    sx = int(ext.get("cx")) / int(chExt.get("cx")) if (chExt is not None and int(chExt.get("cx"))) else 1.0
    sy = int(ext.get("cy")) / int(chExt.get("cy")) if (chExt is not None and int(chExt.get("cy"))) else 1.0

    def tx(x, y, cx, cy):
        lx, ly, lcx, lcy = ox + (x - chx) * sx, oy + (y - chy) * sy, cx * sx, cy * sy
        return parent_tx(lx, ly, lcx, lcy) if parent_tx else (lx, ly, lcx, lcy)

    out = []
    for el in grp:
        tag = el.tag.split("}")[-1]
        if tag in ("nvGrpSpPr", "grpSpPr"):
            continue
        if tag == "grpSp":
            out.extend(flatten_group(el, theme, rels, notes, parent_tx=tx))
            continue
        if tag == "pic":
            rec = _pic_record(el, rels)
        elif tag == "cxnSp":
            rec = parse_cxn(el, theme)
        elif tag == "sp":
            rec = parse_sp(el, theme)
        elif tag == "graphicFrame":
            notes.append(f"group {gname!r} contains a graphicFrame (table/chart) - skipped")
            continue
        else:
            continue
        if not rec.get("raw") and all(k in rec for k in ("x", "y", "cx", "cy")):
            x, y, cx, cy = tx(rec["x"], rec["y"], rec["cx"], rec["cy"])
            rec["x"], rec["y"], rec["cx"], rec["cy"] = round(x), round(y), round(cx), round(cy)
        elif rec.get("raw"):
            notes.append(f"group {gname!r} child kept raw ({rec['raw']}) - not re-positioned")
        out.append(rec)
    return out


def derive_provenance(z, src_pptx, deck_name_override=None):
    """(deck_name, date_str) for the module docstring. Source decks are named
    YYYYMMDD_<name>_<version>.pptx, so the deck name comes from the filename (date
    prefix + trailing version tag stripped, underscores -> spaces) and the date is
    that leading YYYYMMDD. An explicit override wins; if the filename yields no
    name, fall back to docProps/core.xml <dc:title>. (Replaces the old hardcoded
    "Commercial Strategy deck" that mislabeled every ported module — including the
    Navy ones.)"""
    DC = "http://purl.org/dc/elements/1.1/"
    stem = Path(src_pptx).stem
    m = re.match(r"\s*(\d{8})[_\s-]+(.*)$", stem)
    date_str = m.group(1) if m else None
    if deck_name_override and deck_name_override.strip():
        return deck_name_override.strip(), date_str
    rest = m.group(2) if m else stem
    rest = re.sub(r"[_\s-]+v(?:\d[\d.]*|[A-Z])\s*$", "", rest)   # drop _vS / _v2.1 / _v3
    name = rest.replace("_", " ").strip()
    if not name:                                # filename gave nothing -> core.xml title
        try:
            core = ET.fromstring(z.read("docProps/core.xml"))
            t = core.find(q(DC, "title"))
            if t is not None and (t.text or "").strip():
                name = t.text.strip()
        except KeyError:
            pass
    return (name or stem), date_str


HANDPOLISH_MARKER = "HAND-POLISHED"   # modules carrying this sentinel are NEVER overwritten


def convert(src_pptx, slide_no, out_path, src_dir, module_name, layout, units="inches",
            images_dir=None, deck_name=None, force=False):
    global _UNITS
    _UNITS = units
    out_path, src_dir = Path(out_path), Path(src_dir)
    # Guardrail: never silently clobber an existing module (fail fast, before any work).
    if out_path.exists():
        if HANDPOLISH_MARKER in out_path.read_text(encoding="utf-8"):
            raise SystemExit(
                f"refusing to overwrite {out_path}: it is HAND-POLISHED (contains the "
                f"'{HANDPOLISH_MARKER}' sentinel). Re-converting would clobber manual edits "
                f"(affordance names, local_meaning, merges, the table kit). --force does NOT "
                f"override this; delete the file deliberately or pick a different --out.")
        if not force:
            raise SystemExit(
                f"refusing to overwrite existing {out_path}: pass --force to overwrite, "
                f"or pick a new --out path. (Never point --out at the curated slides/ dir.)")
    src_dir.mkdir(parents=True, exist_ok=True)
    images_dir = Path(images_dir) if images_dir else out_path.parent / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(src_pptx) as z:
        theme = build_theme_map(z)
        tstyles = build_table_style_map(z)
        deck_name, deck_date = derive_provenance(z, src_pptx, deck_name)
        rels = slide_rels(z, slide_no)
        # Pick the house layout whose name matches the source slide's layout (so a
        # cover/divider/50%-block/glossary slide gets its house base, not the body
        # one). Unmatched names keep the --layout default.
        src_layout = (source_layout_name(z, slide_no) or "").strip()
        mapped_layout = HOUSE_LAYOUTS.get(src_layout)
        layout_note = None
        if mapped_layout and mapped_layout != layout:
            layout_note = (f"layout: source uses {src_layout!r} -> house {mapped_layout} "
                           f"(was --layout {layout})")
            layout = mapped_layout
        root = ET.fromstring(z.read(f"ppt/slides/slide{slide_no}.xml"))
        spTree = root.find(q(P, "cSld") + "/" + q(P, "spTree"))

        items = []
        chart_assets = []
        group_notes = []
        for el in spTree:
            tag = el.tag.split("}")[-1]
            if tag == "graphicFrame":
                chart = el.find(".//" + q(C, "chart"))
                nm = (el.find(".//" + q(P, "cNvPr")).get("name", "") or "").lower()
                if chart is not None:
                    cx_xml, xlsb, cno = chart_xlsb(z, rels[chart.get(q(R, "id"))])
                    cfile, xfile = f"slide{slide_no}_chart{cno}.xml", f"slide{slide_no}_chart{cno}.xlsb"
                    (src_dir / cfile).write_text(cx_xml, encoding="utf-8")
                    if xlsb is not None:
                        (src_dir / xfile).write_bytes(xlsb)
                    try:
                        cdata = extract_chart_data(cx_xml)
                    except Exception:
                        cdata = None   # fall back to a verbatim bundle
                    chart_assets.append((cfile, xfile if xlsb is not None else None, cdata))
                    xf = el.find(q(P, "xfrm"))
                    off, ext = xf.find(q(A, "off")), xf.find(q(A, "ext"))
                    items.append({"type": "chart", "x": int(off.get("x")), "y": int(off.get("y")),
                                  "cx": int(ext.get("cx")), "cy": int(ext.get("cy")),
                                  "rId": f"rId{len(chart_assets) + 1}"})
                elif el.find(".//" + q(A, "tbl")) is not None:
                    items.append(parse_table(el, theme, tstyles))
                else:
                    items.append({"type": "drop", "comment": f"DROPPED graphicFrame ('{nm}') - think-cell OLE"})
            elif tag == "pic":
                items.append(_pic_record(el, rels))
            elif tag == "grpSp":
                items.extend(flatten_group(el, theme, rels, group_notes))
            elif tag == "cxnSp":
                items.append(parse_cxn(el, theme))
            elif tag == "sp":
                items.append(parse_sp(el, theme))

        # ── finalize <p:pic> images: EMF-preview gating, media copy, rId assignment ──
        # An .emf pic over a bundled native chart is the think-cell vector PREVIEW of
        # that chart -> drop it (the chart renders itself). With no native chart on the
        # slide the .emf IS the content (icon / vector graphic) -> keep it. Kept images
        # become picture() + an IMAGES entry; bytes are copied into images_dir under a
        # content-addressed name so identical media dedupes and names never collide
        # across source decks. Image rIds continue after the layout (rId1) and any chart
        # rIds, so the first image is rId{len(charts)+2} (matches deck_core._build).
        has_native_chart = any(r.get("type") == "chart" for r in items)
        images = []                       # [{"rId","file"}] -> the module IMAGES block
        tgt_to_img = {}                   # source media target -> (rId, copied filename)
        img_rid_base = len(chart_assets) + 2
        for rec in items:
            if rec.get("type") != "pic":
                continue
            if rec["is_emf"] and has_native_chart:
                rec["type"], rec["comment"] = "drop", (
                    f"DROPPED <p:pic> {rec['target'].rsplit('/', 1)[-1]} "
                    f"(EMF think-cell preview of a bundled chart)")
                continue
            tgt = rec["target"]
            if tgt not in tgt_to_img:
                fname_src = tgt.rsplit("/", 1)[-1]
                zip_path = "ppt/media/" + fname_src
                if zip_path not in z.namelist():
                    rec["type"], rec["comment"] = "drop", (
                        f"DROPPED <p:pic> {fname_src} (media part missing from source)")
                    continue
                data = z.read(zip_path)
                stem, _, ext = fname_src.rpartition(".")
                digest = hashlib.sha1(data).hexdigest()[:8]
                new_name = f"{stem or fname_src}_{digest}" + (f".{ext}" if ext else "")
                (images_dir / new_name).write_bytes(data)
                rid = f"rId{img_rid_base + len(tgt_to_img)}"
                tgt_to_img[tgt] = (rid, new_name)
                images.append({"rId": rid, "file": new_name})
            rec["rId"], rec["file"] = tgt_to_img[tgt]

        # ── hyperlinks: external links on runs become module rIds that continue AFTER
        #    the chart + image rIds (deck_core._build's rId order), wired via HYPERLINKS ──
        global _HLINKS
        _HLINKS = {}
        _hl_url = hyperlink_rels(z, slide_no)        # source rId -> URL
        hyperlinks = []
        _hl_base = len(chart_assets) + 2 + len(images)

        def _rec_runs(rec):
            if rec.get("type") == "table":
                return [r for row in rec["rows"] for c in row["cells"]
                        for p in c["paras"] for r in p["runs"]]
            return [r for p in rec.get("paras", []) for r in p["runs"]]

        for rec in items:
            for r in _rec_runs(rec):
                src = r.get("hlink")
                if src and src in _hl_url and src not in _HLINKS:
                    _HLINKS[src] = f"rId{_hl_base + len(_HLINKS)}"
                    hyperlinks.append({"rId": _HLINKS[src], "url": _hl_url[src]})

        notes = ([layout_note] if layout_note else []) + group_notes + detect_chrome(items)
        clusters = detect_clusters(items)

    leader_of = {cl["leader"]: cl for cl in clusters}
    member_set = {i for cl in clusters for i in cl["idxs"]}

    # cluster identity (data-table name / const-anchor prefix / shape name)
    used_names = set()
    for cl in clusters:
        cl["table"], cl["prefix"], cl["shape_name"] = cluster_identity(items, cl, used_names)

    # ── coordinate hoisting: name the structural anchors, keep per-shape coords raw ──
    anchor_defs = []   # module-level "layout anchor" constant lines (faithful: same values)
    # (a) each cluster's CONSTANT coords -> role-named anchors (_AXIS_Y, _SW_X, ...)
    for cl in clusters:
        amap, triples = {}, []
        for f in ("x", "y", "cx", "cy"):
            if f not in cl["varying"]:
                cname = f"_{cl['prefix']}_{DIM[f]}"
                amap[f] = cname
                triples.append((cname, items[cl["leader"]][f]))
        cl["coord_alias"] = amap
        if triples:
            vals = ", ".join(coordlit(v) for _, v in triples)
            cmt = "" if _UNITS == "inches" else \
                f"   # {', '.join(f'{v / 914400:.2f}in' for _, v in triples)}"
            anchor_defs.append(f"{', '.join(c for c, _ in triples)} = {vals}{cmt}")
    # (b) coords repeated across standalone shapes/connectors -> shared anchors (_Y1, _X1, ...)
    standalone = [i for i, rec in enumerate(items)
                  if i not in member_set and i not in leader_of and rec["type"] in ("sp", "cxn")
                  and not rec.get("role") and not rec.get("raw")]
    freq = {}
    for i in standalone:
        for f in ("x", "y", "cx", "cy"):
            v = items[i].get(f)
            if isinstance(v, int) and v > 0:
                freq[v] = freq.get(v, 0) + 1
    global_alias, dimk = {}, {"X": 0, "Y": 0, "W": 0, "H": 0}
    for i in standalone:
        for f in ("x", "y", "cx", "cy"):
            v = items[i].get(f)
            if isinstance(v, int) and v > 0 and freq[v] >= SHARED_ANCHOR_MIN and v not in global_alias:
                dimk[DIM[f]] += 1
                global_alias[v] = f"_{DIM[f]}{dimk[DIM[f]]}"
                anchor_defs.append(f"{global_alias[v]} = {coordlit(v)}   # shared x{freq[v]}")

    def coord_map_for(rec):
        return {f: global_alias[rec[f]] for f in ("x", "y", "cx", "cy")
                if isinstance(rec.get(f), int) and rec[f] in global_alias}

    # ── custom-geometry constants: dedup identical <a:custGeom> paths into one ──
    # module constant (e.g. freight_charges' 5 icon shapes = 2 unique geometries).
    geom_consts = {}          # geom xml -> constant name (_GEOM0, _GEOM1, ...)
    geom_meta = {}            # constant name -> [sample source shape name, count]
    for rec in items:
        g = rec.get("custgeom")
        if not g:
            continue
        if g not in geom_consts:
            cn = f"_GEOM{len(geom_consts)}"
            geom_consts[g] = cn
            geom_meta[cn] = [rec.get("name", "Shape"), 0]
        geom_meta[geom_consts[g]][1] += 1
    geom_defs = []
    for g, cn in geom_consts.items():
        src_name, cnt = geom_meta[cn]
        lit = '"' + g.replace("\\", "\\\\").replace('"', '\\"') + '"'
        times = f" x{cnt}" if cnt > 1 else ""
        geom_defs.append(f'{cn} = {lit}   # source: "{py_str(src_name)}"{times}')

    data_defs, body = [], []
    stats = {"text_box": 0, "connector": 0, "chart": 0, "table": 0, "picture": 0, "raw": 0,
             "dropped": 0, "fld": 0, "clusters": 0, "chrome": 0, "looped": 0, "custgeom": 0}
    raw_id = 2000
    for i, rec in enumerate(items):
        if i in leader_of:
            cl = leader_of[i]
            fields = cl["varying"]
            stats["clusters"] += 1
            stats["looped"] += len(cl["idxs"])
            stats["fld"] += sum(len(items[j]["el"].findall(".//" + q(A, "fld"))) for j in cl["idxs"])
            keycmt = ", ".join(FIELD_LABEL[f] for f in fields)
            # local_meaning slot: a human fills in the slide-specific read. The converter
            # seeds a TODO + sample text (it knows the affordance, not the slide's meaning).
            _lm_samples = [t for t in (_member_text(items[j]).strip() for j in cl["idxs"]) if t][:3]
            _lm = "# local_meaning: TODO - " + cl["table"].strip("_").lower().replace("_", " ")
            if _lm_samples:
                _lm += "; sample: " + ", ".join(_lm_samples)
            data_defs.append(_lm)
            data_defs.append(f"{cl['table']} = [    # ({keycmt}) x{len(cl['idxs'])}")
            for j in cl["idxs"]:
                vals = ", ".join(render_value(items[j], f) for f in fields)
                data_defs.append(f"    ({vals})," if len(fields) != 1 else f"    {vals},")
            data_defs.append("]")
            data_defs.append("")
            varmap = {}
            for f in fields:
                vn = VAR_NAMES[f]
                varmap[f] = (f"IN({vn})" if _UNITS == "inches" and f in ("x", "y", "cx", "cy") else vn)
            varmap.update(cl["coord_alias"])   # constant coords -> role-named anchors (already EMU)
            rec["name"] = cl["shape_name"]      # role-based shape name
            unpack = ", ".join(VAR_NAMES[f] for f in fields)
            body.append(f"    for {unpack} in {cl['table']}:")
            body.append(f"        out.append({render_sp(rec, 'n()', varmap)})")
            continue
        if i in member_set:
            continue
        if rec["type"] == "drop":
            body.append(f"    # {rec['comment']}")
            stats["dropped"] += 1
        elif rec["type"] == "table":
            body.append('    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)')
            body.append(f"    out.append({render_table(rec, 'n()')})")
            stats["table"] += 1
        elif rec["type"] == "chart":
            body.append('    # native chart, bundled verbatim + .xlsb ("Edit Data" works)')
            body.append(f'    out.append(graphic_frame(sp_id=n(), name="Chart", '
                        f'x={coordlit(rec["x"])}, y={coordlit(rec["y"])}, '
                        f'cx={coordlit(rec["cx"])}, cy={coordlit(rec["cy"])}, rId="{rec["rId"]}"))')
            stats["chart"] += 1
        elif rec["type"] == "pic":
            sr = rec.get("src_rect")
            sr_arg = f", src_rect={sr!r}" if sr else ""
            body.append('    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)')
            body.append(f'    out.append(picture(n(), "{py_str(rec["name"])}", "{rec["rId"]}", '
                        f'{coordlit(rec["x"])}, {coordlit(rec["y"])}, '
                        f'{coordlit(rec["cx"])}, {coordlit(rec["cy"])}{sr_arg}))')
            stats["picture"] += 1
        elif rec.get("role"):
            body.append(f"    out.append({render_chrome(rec)})")
            stats["chrome"] += 1
        elif rec["type"] == "cxn":
            if rec["raw"]:
                body.append(f"    out.append({raw_literal(rec['el'], raw_id)})")
                raw_id += 1
                stats["raw"] += 1
            else:
                body.append(f"    out.append({render_cxn(rec, 'n()', coord_map_for(rec))})")
                stats["connector"] += 1
        elif rec["type"] == "sp":
            stats["fld"] += len(rec["el"].findall(".//" + q(A, "fld")))
            if rec["raw"]:
                body.append(f"    # RAW verbatim ({rec['raw']}):")
                body.append(f"    out.append({raw_literal(rec['el'], raw_id)})")
                raw_id += 1
                stats["raw"] += 1
            elif rec.get("custgeom"):
                cn = geom_consts[rec["custgeom"]]
                kw = ""
                if rec["fill"] != "None":
                    kw += f", fill={rec['fill']}"
                if rec["line_color"] != '"none"':
                    kw += f", line_color={rec['line_color']}"
                    if rec["line_width"] not in (None, 12700):
                        kw += f", line_width={rec['line_width']}"
                if rec.get("rot"):
                    kw += f", rot={rec['rot']}"
                body.append('    # custom-geometry icon: verbatim <a:custGeom> path, pos/fill/line as params')
                body.append(f'    out.append(custom_geometry(n(), "{py_str(rec["name"])}", '
                            f'{coordlit(rec["x"])}, {coordlit(rec["y"])}, '
                            f'{coordlit(rec["cx"])}, {coordlit(rec["cy"])}, {cn}{kw}))')
                stats["custgeom"] += 1
            else:
                body.append(f"    out.append({render_sp(rec, 'n()', coord_map_for(rec))})")
                stats["text_box"] += 1

    module = build_module_text(module_name, slide_no, layout, chart_assets, images, hyperlinks,
                               anchor_defs, data_defs, geom_defs, body, stats, notes,
                               deck_name, deck_date)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(module, encoding="utf-8")
    print(f"wrote {out_path}")
    print(f"  text_box={stats['text_box']} connector={stats['connector']} chart={stats['chart']} "
          f"table={stats['table']} picture={stats['picture']} custom_geometry={stats['custgeom']} "
          f"raw={stats['raw']} dropped={stats['dropped']} frozen_fields={stats['fld']}")
    print(f"  chrome builders={stats['chrome']} | clusters={stats['clusters']} "
          f"collapsing {stats['looped']} shapes into loops")
    for nt in notes:
        print(f"  note: {nt}")


def _imports(text, chart_syms=()):
    prims = ["slide"]
    for nm in ("run", "paragraph", "text_box", "custom_geometry", "connector",
               "picture", "line_break",
               "table", "trow", "tcell", "tcell_rich", "tpara", "trun", "tbreak"):
        if re.search(rf"\b{nm}\(", text):
            prims.append(nm)
    chrome = [nm for nm in ("breadcrumb", "title_placeholder", "prelim_chip", "sources_line")
              if re.search(rf"\b{nm}\(", text)]
    toks = [t for t in dict.fromkeys(TOKENS.values()) if re.search(rf"\b{t}\b", text)]
    if "FONT" not in toks:
        toks.append("FONT")
    if re.search(r"\bPT\(", text):
        toks = ["PT"] + toks
    if re.search(r"\bIN\(", text):
        toks = ["IN"] + toks
    prim_line = "from deck_core.primitives import " + ", ".join(prims + chrome)
    if len(prim_line) > 95:
        prim_line = ("from deck_core.primitives import (\n    "
                     + ", ".join(prims + chrome) + ",\n)")
    lines = [prim_line]
    chart_imports = [s for s in ("graphic_frame", "styled_chart", "editable_bundled_chart")
                     if s in chart_syms]
    if chart_imports:
        lines.append("from deck_core.charts import " + ", ".join(chart_imports))
    lines.append("from deck_core.style import " + ", ".join(toks))
    return "\n".join(lines)


def _fmt_num_literal(v):
    """A number for a _DATA literal: None stays None, int-valued floats lose the
    '.0' (42.0 -> 42), everything else is repr (shortest round-trip)."""
    if v is None:
        return "None"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return repr(v)


def _format_chart_data(var, data):
    """Emit a readable _DATA literal: categories + one {name?, values} per series."""
    out = [f"{var} = {{"]
    cats = data.get("categories")
    if cats is None:
        out.append('    "categories": None,')
    else:
        out.append('    "categories": [' + ", ".join(repr(c) for c in cats) + "],")
    out.append('    "series": [')
    for s in data["series"]:
        vals = "[" + ", ".join(_fmt_num_literal(v) for v in s["values"]) + "]"
        if s.get("name") is not None:
            out.append(f'        {{"name": {s["name"]!r}, "values": {vals}}},')
        else:
            out.append(f'        {{"values": {vals}}},')
    out += ["    ],", "}"]
    return "\n".join(out)


_TABLE_KIT = '''
# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets, borders,
#    spans). Renders identically to raw tcell()/tcell_rich(); hand-polish the cells from here. ──
PAD = dict(l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960)   # the source's heavier cell padding


def edge(color, w=12700):
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", vert=None, span=1, rowspan=1,
         l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, vert=vert, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def rcell(paras, *, fill=None, anchor="ctr", vert=None, span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor, vert=vert,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))
'''


def build_module_text(module_name, slide_no, layout, chart_assets, images, hyperlinks, anchor_defs,
                      data_defs, geom_defs, body, stats, notes, deck_name, deck_date):
    chart_reads, data_literals, charts, chart_syms = [], [], [], set()
    for i, (cfile, xfile, cdata) in enumerate(chart_assets):
        # styled_chart (data-over-template) when we recovered both the .xlsb and
        # the series data; else fall back to a verbatim editable/raw bundle.
        if xfile and cdata and cdata.get("series"):
            chart_reads.append(f'_CHART{i}_TPL = (_SRC / "{cfile}").read_text(encoding="utf-8")')
            chart_reads.append(f'_XLSB{i} = (_SRC / "{xfile}").read_bytes()')
            data_literals.append(_format_chart_data(f"_CHART{i}_DATA", cdata))
            charts.append(f"styled_chart(_CHART{i}_TPL, _CHART{i}_DATA, _XLSB{i})")
            chart_syms.add("styled_chart")
        elif xfile:
            chart_reads.append(f'_CHART{i} = (_SRC / "{cfile}").read_text(encoding="utf-8")')
            chart_reads.append(f'_XLSB{i} = (_SRC / "{xfile}").read_bytes()')
            charts.append(f"editable_bundled_chart(_CHART{i}, _XLSB{i})")
            chart_syms.add("editable_bundled_chart")
        else:
            chart_reads.append(f'_CHART{i} = (_SRC / "{cfile}").read_text(encoding="utf-8")')
            charts.append(f'{{"chart_xml": _CHART{i}}}')
    if chart_assets:
        chart_syms.add("graphic_frame")
        blocks = ["\n".join(chart_reads)]
        blocks += data_literals
        blocks.append("CHARTS = [" + ", ".join(charts) + "]")
        chart_block = "\n\n".join(blocks)
    else:
        chart_block = "CHARTS: list = []"
    if images:
        img_lines = ["IMAGES = ["]
        for im in images:
            img_lines.append(f'    {{"rId": "{im["rId"]}", "file": "{im["file"]}"}},')
        img_lines.append("]")
        images_block = "\n" + "\n".join(img_lines)
    else:
        images_block = ""
    if hyperlinks:
        hl_lines = ["HYPERLINKS = ["]
        for h in hyperlinks:
            hl_lines.append(f'    {{"rId": "{h["rId"]}", "url": "{py_str(h["url"])}"}},')
        hl_lines.append("]")
        hyperlinks_block = "\n" + "\n".join(hl_lines)
    else:
        hyperlinks_block = ""
    kit_block = _TABLE_KIT if stats.get("table") else ""
    # include the kit in the text _imports() scans so tcell/tcell_rich/PT/BLACK/FONT (used
    # only inside the kit defs) still get imported even though the body calls cell()/rcell().
    all_text = "\n".join(anchor_defs + data_defs + body) + kit_block
    has_styled = any(xfile and cdata and cdata.get("series")
                     for (_, xfile, cdata) in chart_assets)
    if has_styled:
        chart_doc = ('The native <c:chart> exhibit is a data-over-template styled_chart: the\n'
                     'source chart part is the exact STYLE template and its values live in the\n'
                     '_CHART*_DATA literal (look byte-identical, "Edit Data" still works).')
    elif chart_assets:
        chart_doc = ('The native <c:chart> exhibit is bundled verbatim with its .xlsb\n'
                     '(byte-exact, still "Edit Data"-editable).')
    else:
        chart_doc = 'Shapes are rebuilt through deck_core primitives.'
    notes_doc = ("\n\nConverter notes:\n  - " + "\n  - ".join(notes)) if notes else ""
    data_section = ""
    if anchor_defs:
        data_section += ("# ── layout anchors (shared coordinates) ──\n"
                         + "\n".join(anchor_defs) + "\n\n")
    if data_defs:
        data_section += ("# ── repeated-shape data tables (each drives a loop in _body) ──\n"
                         + "\n".join(data_defs) + "\n")
    if geom_defs:
        data_section += ("# ── custom-geometry paths (verbatim <a:custGeom>, deduped) ──\n"
                         + "\n".join(geom_defs) + "\n\n")
    prov = f" ({deck_date})" if deck_date else ""
    return f'''"""{module_name} — {deck_name} deck{prov}, source slide {slide_no}.

Auto-converted from the source .pptx by _tools/convert_slide.py.
{chart_doc}
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); pattern-fill keys become
text_box(pattern_fill=…) and freeform <a:custGeom> icons become custom_geometry()
over a deduped path constant; think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box={stats['text_box']}, connector={stats['connector']}, chart={stats['chart']}, \
table={stats['table']}, picture={stats['picture']}, custom_geometry={stats['custgeom']}, \
chrome_builders={stats['chrome']}, clusters={stats['clusters']} (covering {stats['looped']} shapes), \
raw_verbatim={stats['raw']}, dropped={stats['dropped']}, frozen_fields={stats['fld']}.{notes_doc}
"""
from __future__ import annotations

from pathlib import Path

{_imports(all_text, chart_syms)}

LAYOUT = "{layout}"

_SRC = Path(__file__).parent / "_src"
{chart_block}{images_block}{hyperlinks_block}

{kit_block}
{data_section}def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
{chr(10).join(body)}
    return "".join(out)


def render() -> str:
    return slide(_body())
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source")
    ap.add_argument("slide", type=int)
    ap.add_argument("--out", required=True)
    ap.add_argument("--src-dir", required=True)
    ap.add_argument("--module-name", required=True)
    ap.add_argument("--layout", default="slideLayout4")
    ap.add_argument("--units", choices=("inches", "emu"), default="inches",
                    help="coordinate units in the emitted module (default inches via IN())")
    ap.add_argument("--images-dir", default=None,
                    help="dir to copy <p:pic> media into (default: <out>/../images, "
                         "i.e. the slides/images/ the build packs into ppt/media/)")
    ap.add_argument("--deck-name", default=None,
                    help="deck name for the module docstring provenance (default: "
                         "derived from the source filename, else docProps title)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing --out file (still refused if it is HAND-POLISHED)")
    a = ap.parse_args()
    convert(a.source, a.slide, a.out, a.src_dir, a.module_name, a.layout, a.units,
            a.images_dir, a.deck_name, a.force)


if __name__ == "__main__":
    main()
