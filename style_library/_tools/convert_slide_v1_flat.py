#!/usr/bin/env python3
"""convert_slide.py - convert one source-.pptx slide into an idiomatic deck_core module.

Reads a single slide from a source PowerPoint file and emits a Python slide module
that rebuilds it through deck_core primitives. The goal is a module that (a) renders
faithfully and (b) reads like a hand-authored deck_core slide, so an AI agent can
study it as a worked example.

What it does, per the faithful-port methodology (docs/faithful_deck_port_methodology.md):
  - <p:sp> with explicit geometry  -> text_box(...) at the source EMU coords, with
    fill / border / preset / insets / anchor / rotation and per-run text transcribed.
  - <a:fld> labels (think-cell)     -> FROZEN to static run()s using the field's cached
    <a:t> text, so PowerPoint can't refresh a "datetime" field and destroy the label.
  - schemeClr (incl. lumMod/lumOff) -> resolved to literal hex against the source theme
    (lumMod/lumOff baked via the HLS transform; soffice mis-renders lumOff otherwise).
    A hex that exactly equals a deck_core.style token is emitted as that token.
  - native <c:chart> graphicFrame   -> graphic_frame(rId="rId2") + the chart part and
    its .xlsb copied into _src/; CHARTS = [editable_bundled_chart(...)] (byte-exact,
    still "Edit Data"-editable). Charts are NOT rebuilt from data.
  - think-cell OLE frame ("... do not delete") + its EMF preview <p:pic> -> DROPPED.
  - <p:cxnSp>                        -> connector(...) (stCxn/endCxn glue dropped; the
    line renders statically from its own xfrm).
  - anything exotic (custGeom, gradient/pattern/picture fill, a placeholder with no
    explicit geometry, a table) -> emitted as a RAW verbatim OOXML string (id renumbered),
    tagged with a `# RAW:` comment so a human can later lift it to a primitive.

Usage:
    python convert_slide.py SOURCE.pptx N \\
        --out  ../deck_commercial_strategy/slides/<name>.py \\
        --src-dir ../deck_commercial_strategy/slides/_src \\
        --module-name <name> [--layout slideLayout4] [--id-base 100]

It is deliberately self-contained (stdlib only) so it can be copied next to any
deck pipeline.
"""
from __future__ import annotations

import argparse
import colorsys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
C = "http://schemas.openxmlformats.org/drawingml/2006/chart"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"

for _pfx, _uri in (("a", A), ("p", P), ("c", C), ("r", R)):
    ET.register_namespace(_pfx, _uri)


def q(ns: str, t: str) -> str:
    return f"{{{ns}}}{t}"


# hex (upper) -> deck_core.style token name. Exact matches only (no nearest-snap, which
# would shift a brand color). Brand accents stay literal hex on purpose.
TOKENS = {
    "000000": "BLACK", "FFFFFF": "WHITE", "162029": "DK",
    "44505C": "BREADCRUMB", "FFFFCC": "PRELIM",
    "E2E9EF": "BLUE_1", "B6C8D8": "BLUE_2", "6E91B1": "BLUE_3",
    "3D5972": "BLUE_4", "263746": "BLUE_5",
    "F2F2F2": "GRAY_1", "D9D9D9": "GRAY_2", "BFBFBF": "GRAY_3",
    "7F7F7F": "GRAY_4", "646464": "GRAY_5",
}


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
    # placeholder aliases used in shapes (tx1<->dk1, bg1<->lt1, tx2<->dk2, bg2<->lt2)
    m["tx1"], m["bg1"] = m.get("dk1", "000000"), m.get("lt1", "FFFFFF")
    m["tx2"], m["bg2"] = m.get("dk2", "000000"), m.get("lt2", "FFFFFF")
    return m


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
    """DrawingML <a:shade>/<a:tint> (per-channel sRGB): shade darkens toward
    black, tint lightens toward white. Values are fractions (15000 -> 0.15)."""
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
    lm = clr.find(q(A, "lumMod"))
    lo = clr.find(q(A, "lumOff"))
    lummod = int(lm.get("val")) / 100000 if lm is not None else None
    lumoff = int(lo.get("val")) / 100000 if lo is not None else None
    if lummod is not None or lumoff is not None:
        base = _bake_lum(base, lummod, lumoff)
    sh = clr.find(q(A, "shade"))
    ti = clr.find(q(A, "tint"))
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
    return sf.find(q(A, "srgbClr")) if sf.find(q(A, "srgbClr")) is not None else sf.find(q(A, "schemeClr"))


# ── text ─────────────────────────────────────────────────────────────────────
def py_str(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')


def run_call(rPr, text: str, theme: dict) -> str:
    parts = [f'"{py_str(text)}"']
    if rPr is not None:
        sz = rPr.get("sz")
        if sz:
            parts.append(f"size={int(sz)}")          # OOXML sz and deck_core size are both 1/100 pt
        if rPr.get("b") == "1":
            parts.append("bold=True")
        if rPr.get("i") == "1":
            parts.append("italic=True")
        lit = color_lit(color_hex(_solid_child(rPr), theme))
        if lit is not None:
            parts.append(f"color={lit}")
    parts.append("font=FONT")
    return f"run({', '.join(parts)})"


def para_call(p, theme: dict) -> str:
    runs = []
    for ch in p:
        tag = ch.tag.split("}")[-1]
        if tag == "r":
            t = ch.find(q(A, "t"))
            runs.append(run_call(ch.find(q(A, "rPr")), t.text if t is not None else "", theme))
        elif tag == "fld":               # think-cell label -> frozen static run
            t = ch.find(q(A, "t"))
            runs.append(run_call(ch.find(q(A, "rPr")), t.text if t is not None else "", theme))
    pPr = p.find(q(A, "pPr"))
    kw = []
    if pPr is not None:
        if pPr.get("algn"):
            kw.append(f'align="{pPr.get("algn")}"')
        if pPr.get("lvl"):
            kw.append(f'level={int(pPr.get("lvl"))}')
        if pPr.get("marL"):
            kw.append(f'mar_l={int(pPr.get("marL"))}')
        if pPr.get("indent"):
            kw.append(f'indent={int(pPr.get("indent"))}')
        sa = pPr.find(q(A, "spcAft") + "/" + q(A, "spcPts"))
        if sa is not None:
            kw.append(f'space_after={int(sa.get("val"))}')
        ls = pPr.find(q(A, "lnSpc") + "/" + q(A, "spcPct"))
        if ls is not None:
            kw.append(f'line_spacing={int(ls.get("val"))}')
        if pPr.find(q(A, "buChar")) is not None:
            kw.append("bullet=True")
    runs_str = "[" + ", ".join(runs) + "]"
    tail = (", " + ", ".join(kw)) if kw else ""
    return f"paragraph({runs_str}{tail})"


# ── raw fallback ─────────────────────────────────────────────────────────────
# Elements that reference a slide relationship (or are think-cell bookkeeping) and
# would dangle once the shape is lifted into a freshly-relationshipped slide. A
# dangling r:id makes PowerPoint "repair" the file on open (soffice silently
# ignores it), so strip them — same cleaning extract_chart.py does (methodology §7).
_CRUFT = {
    q(P, "custDataLst"),   # <p:tags r:id=...> think-cell data -> dangles
    q(P, "extLst"), q(A, "extLst"),   # a14/a16 creationId etc. -> dead weight
    q(A, "hlinkClick"), q(A, "hlinkHover"),   # r:id hyperlinks -> dangle
}


def _strip_cruft(elem):
    """Recursively drop relationship-bearing / bookkeeping children at every depth.
    Visual properties (fill, geometry, run color) are untouched."""
    for child in list(elem):
        if child.tag in _CRUFT:
            elem.remove(child)
        else:
            _strip_cruft(child)
    return elem


def raw_literal(elem, new_id: int) -> str:
    """Verbatim element as a Python string literal, with its cNvPr id renumbered
    and dangling-ref / think-cell cruft stripped."""
    _strip_cruft(elem)
    nv = elem.find(".//" + q(P, "cNvPr"))
    if nv is not None:
        nv.set("id", str(new_id))
    xml = ET.tostring(elem, encoding="unicode")
    # collapse the redundant xmlns decls ET injects; slide() already declares a:/p:/r:
    for decl in (f' xmlns:a="{A}"', f' xmlns:p="{P}"', f' xmlns:r="{R}"', f' xmlns:c="{C}"'):
        xml = xml.replace(decl, "")
    return '"' + xml.replace("\\", "\\\\").replace('"', '\\"') + '"'


# ── shape emitters ───────────────────────────────────────────────────────────
def textbox_call(sp, theme, new_id):
    spPr = sp.find(q(P, "spPr"))
    xfrm = spPr.find(q(A, "xfrm")) if spPr is not None else None
    if xfrm is None:                       # placeholder w/o explicit geom -> keep verbatim
        return ("RAW", raw_literal(sp, new_id), "no explicit xfrm (layout placeholder)")
    # gradient / pattern / picture fills aren't modelled by text_box -> verbatim
    for exotic in ("gradFill", "pattFill", "blipFill"):
        if spPr.find(q(A, exotic)) is not None:
            return ("RAW", raw_literal(sp, new_id), f"{exotic}")
    if spPr.find(q(A, "custGeom")) is not None:
        return ("RAW", raw_literal(sp, new_id), "custGeom")

    nv = sp.find(".//" + q(P, "cNvPr"))
    name = nv.get("name", "Shape") if nv is not None else "Shape"
    off, ext = xfrm.find(q(A, "off")), xfrm.find(q(A, "ext"))
    x, y = int(off.get("x")), int(off.get("y"))
    cx, cy = int(ext.get("cx")), int(ext.get("cy"))
    rot = xfrm.get("rot")

    pg = spPr.find(q(A, "prstGeom"))
    prst = pg.get("prst") if pg is not None else "rect"
    geom_adj = {gd.get("name"): gd.get("fmla") for gd in pg.findall(q(A, "avLst") + "/" + q(A, "gd"))} if pg is not None else {}

    # fill
    if spPr.find(q(A, "noFill")) is not None:
        fill = "None"
    else:
        fill = color_lit(color_hex(_solid_child(spPr), theme)) or "None"

    # line / border. An <a:ln> may carry only a width and inherit its colour from
    # the shape's <p:style><a:lnRef> (think-cell's callouts do exactly this) — so
    # when the ln has no explicit fill, resolve the colour from the style ref.
    ln = spPr.find(q(A, "ln"))
    line_color, line_width, dashed = '"none"', None, False
    if ln is not None and ln.find(q(A, "noFill")) is None:
        lc = color_lit(color_hex(_solid_child(ln), theme))
        if lc is None:
            style = sp.find(q(P, "style"))
            lnRef = style.find(q(A, "lnRef")) if style is not None else None
            ref_clr = None
            if lnRef is not None:
                ref_clr = lnRef.find(q(A, "schemeClr"))
                if ref_clr is None:
                    ref_clr = lnRef.find(q(A, "srgbClr"))
            lc = color_lit(color_hex(ref_clr, theme))
        if lc is not None:
            line_color = lc
            w = ln.get("w")
            line_width = int(w) if w else None
            d = ln.find(q(A, "prstDash"))
            dashed = d is not None and d.get("val") not in (None, "solid")

    # body
    txBody = sp.find(q(P, "txBody"))
    bodyPr = txBody.find(q(A, "bodyPr")) if txBody is not None else None
    anchor, wrap, ins = "t", "square", {}
    if bodyPr is not None:
        anchor = bodyPr.get("anchor", "t")
        wrap = bodyPr.get("wrap", "square")
        for attr, kw in (("lIns", "l_ins"), ("tIns", "t_ins"), ("rIns", "r_ins"), ("bIns", "b_ins")):
            if bodyPr.get(attr) is not None:
                ins[kw] = int(bodyPr.get(attr))
    paras = [para_call(p, theme) for p in txBody.findall(q(A, "p"))] if txBody is not None else []
    paras_str = "[" + ", ".join(paras) + "]" if paras else "[paragraph([])]"

    args = [str(new_id), f'"{py_str(name)}"', str(x), str(y), str(cx), str(cy), paras_str]
    kw = [f"fill={fill}", f"line_color={line_color}"]
    if line_width is not None and line_width != 12700:
        kw.append(f"line_width={line_width}")
    if dashed:
        kw.append("dashed_line=True")
    if prst != "rect":
        kw.append(f'prst="{prst}"')
    if geom_adj:
        kw.append("geom_adj={" + ", ".join(f'"{k}": "{v}"' for k, v in geom_adj.items()) + "}")
    if anchor != "t":
        kw.append(f'anchor="{anchor}"')
    if wrap != "square":
        kw.append(f'wrap="{wrap}"')
    for k, v in ins.items():
        kw.append(f"{k}={v}")
    if rot:
        kw.append(f"rot={int(rot)}")
    return ("CALL", f"text_box({', '.join(args)}, {', '.join(kw)})", name)


def connector_call(cxn, theme, new_id):
    spPr = cxn.find(q(P, "spPr"))
    xfrm = spPr.find(q(A, "xfrm"))
    if xfrm is None:
        return ("RAW", raw_literal(cxn, new_id), "connector w/o xfrm")
    nv = cxn.find(".//" + q(P, "cNvPr"))
    name = nv.get("name", "Connector") if nv is not None else "Connector"
    off, ext = xfrm.find(q(A, "off")), xfrm.find(q(A, "ext"))
    x, y = int(off.get("x")), int(off.get("y"))
    cx, cy = int(ext.get("cx")), int(ext.get("cy"))
    if xfrm.get("flipH") == "1":
        cx = -cx
    if xfrm.get("flipV") == "1":
        cy = -cy
    pg = spPr.find(q(A, "prstGeom"))
    prst = pg.get("prst") if pg is not None else "line"
    ln = spPr.find(q(A, "ln"))
    color, width, dashed, arrow = "BLACK", 12700, False, False
    if ln is not None:
        w = ln.get("w")
        width = int(w) if w else 12700
        lc = color_lit(color_hex(_solid_child(ln), theme))
        if lc is not None:
            color = lc
        dashed = ln.find(q(A, "prstDash")) is not None
        arrow = ln.find(q(A, "tailEnd")) is not None or ln.find(q(A, "headEnd")) is not None
    kw = [f"color={color}", f"width={width}"]
    if dashed:
        kw.append("dashed=True")
    if arrow:
        kw.append("arrow=True")
    if prst not in ("line", "straightConnector1"):
        kw.append(f'prst="{prst}"')
    return ("CALL", f'connector({new_id}, "{py_str(name)}", {x}, {y}, {cx}, {cy}, {", ".join(kw)})', name)


# ── slide rels helpers ───────────────────────────────────────────────────────
def slide_rels(z, slide_no):
    root = ET.fromstring(z.read(f"ppt/slides/_rels/slide{slide_no}.xml.rels"))
    return {r.get("Id"): r.get("Target") for r in root}


def chart_xlsb(z, chart_target):
    """chart_target like '../charts/chart42.xml' -> (chart_xml str, xlsb bytes, chart_no)."""
    chart_path = "ppt/" + chart_target.split("../", 1)[-1]
    chart_no = "".join(c for c in chart_path.rsplit("/", 1)[-1] if c.isdigit())
    chart_xml = z.read(chart_path).decode("utf-8")
    rels = ET.fromstring(z.read(f"ppt/charts/_rels/chart{chart_no}.xml.rels"))
    xlsb_bytes = None
    for r in rels:
        tgt = r.get("Target")
        if tgt.lower().endswith((".xlsb", ".xlsx")):
            xlsb_bytes = z.read("ppt/" + tgt.split("../", 1)[-1])
    return chart_xml, xlsb_bytes, chart_no


# ── main ─────────────────────────────────────────────────────────────────────
def convert(src_pptx, slide_no, out_path, src_dir, module_name, layout, id_base):
    out_path, src_dir = Path(out_path), Path(src_dir)
    src_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(src_pptx) as z:
        theme = build_theme_map(z)
        rels = slide_rels(z, slide_no)
        root = ET.fromstring(z.read(f"ppt/slides/slide{slide_no}.xml"))
        spTree = root.find(q(P, "cSld") + "/" + q(P, "spTree"))

        body_lines: list[str] = []
        chart_assets: list[tuple[str, str]] = []   # (chart_xml_file, xlsb_file)
        stats = {"text_box": 0, "connector": 0, "chart": 0, "raw": 0, "dropped": 0, "fld": 0}
        nid = id_base

        for el in spTree:
            tag = el.tag.split("}")[-1]
            if tag == "graphicFrame":
                chart = el.find(".//" + q(C, "chart"))
                nvname = (el.find(".//" + q(P, "cNvPr")).get("name", "") or "").lower()
                if chart is not None:
                    rid = chart.get(q(R, "id"))
                    cx_xml, xlsb, cno = chart_xlsb(z, rels[rid])
                    cfile = f"slide{slide_no}_chart{cno}.xml"
                    xfile = f"slide{slide_no}_chart{cno}.xlsb"
                    (src_dir / cfile).write_text(cx_xml, encoding="utf-8")
                    if xlsb is not None:
                        (src_dir / xfile).write_bytes(xlsb)
                    chart_assets.append((cfile, xfile if xlsb is not None else None))
                    xf = el.find(q(P, "xfrm"))
                    off, ext = xf.find(q(A, "off")), xf.find(q(A, "ext"))
                    rId = f"rId{len(chart_assets) + 1}"   # rId1 = layout; charts start at rId2
                    body_lines.append(
                        f'    # native stacked-column chart (bundled verbatim + .xlsb; "Edit Data" works)\n'
                        f'    graphic_frame(sp_id={nid}, name="Chart", '
                        f'x={off.get("x")}, y={off.get("y")}, '
                        f'cx={ext.get("cx")}, cy={ext.get("cy")}, rId="{rId}"),')
                    stats["chart"] += 1
                    nid += 1
                else:
                    stats["dropped"] += 1   # OLE "do not delete" frame / table-less graphic
                    body_lines.append(f"    # DROPPED graphicFrame ('{nvname}') - think-cell OLE / non-chart")
                continue
            if tag == "pic":
                blip = el.find(".//" + q(A, "blip"))
                emb = blip.get(q(R, "embed")) if blip is not None else None
                tgt = rels.get(emb, "")
                if tgt.lower().endswith(".emf"):
                    stats["dropped"] += 1
                    body_lines.append(f"    # DROPPED <p:pic> {tgt.rsplit('/', 1)[-1]} (think-cell OLE preview)")
                else:
                    body_lines.append(f"    # TODO <p:pic> {tgt} - real image; wire via IMAGES + picture()")
                    stats["dropped"] += 1
                continue
            if tag == "cxnSp":
                kind, code, name = connector_call(el, theme, nid)
            elif tag == "sp":
                kind, code, name = textbox_call(el, theme, nid)
                stats["fld"] += len(el.findall(".//" + q(A, "fld")))
            else:
                continue
            if kind == "RAW":
                body_lines.append(f"    # RAW verbatim ({name}):")
                body_lines.append(f"    {code},")
                stats["raw"] += 1
            else:
                body_lines.append(f"    {code},")
                stats["text_box" if tag == "sp" else "connector"] += 1
            nid += 1

    module = build_module_text(module_name, slide_no, layout, chart_assets, body_lines, stats)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(module, encoding="utf-8")
    print(f"wrote {out_path}")
    print(f"  shapes: text_box={stats['text_box']} connector={stats['connector']} "
          f"chart={stats['chart']} raw={stats['raw']} dropped={stats['dropped']} "
          f"frozen_fields={stats['fld']}")
    print(f"  chart assets in {src_dir}: {[c for c, _ in chart_assets]}")


def build_module_text(module_name, slide_no, layout, chart_assets, body_lines, stats):
    charts_setup = ""
    charts_attr = "CHARTS: list = []"
    if chart_assets:
        reads = []
        bundles = []
        for i, (cfile, xfile) in enumerate(chart_assets):
            reads.append(f'_CHART{i} = (_SRC / "{cfile}").read_text(encoding="utf-8")')
            if xfile:
                reads.append(f'_XLSB{i} = (_SRC / "{xfile}").read_bytes()')
                bundles.append(f"editable_bundled_chart(_CHART{i}, _XLSB{i})")
            else:
                bundles.append(f'{{"chart_xml": _CHART{i}}}')
        charts_setup = "\n".join(reads) + "\n"
        charts_attr = "CHARTS = [" + ", ".join(bundles) + "]"
    body = "\n".join(body_lines)
    return f'''"""{module_name} - Commercial Strategy deck, source slide {slide_no}
(SHIPS Act Volume by Type).

Auto-converted 1:1 from the source .pptx by _tools/convert_slide.py, then
(optionally) hand-polished. The stacked-column exhibit is a native <c:chart>
bundled verbatim with its .xlsb (byte-exact, still "Edit Data"-editable); every
other object is an idiomatic deck_core primitive at the source EMU coordinates.
think-cell <a:fld> labels are frozen to static runs; the OLE frame + EMF preview
are dropped.

Converter stats: text_box={stats['text_box']}, connector={stats['connector']}, chart={stats['chart']}, \
raw_verbatim={stats['raw']}, dropped={stats['dropped']}, frozen_fields={stats['fld']}.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide, run, paragraph, text_box, connector
from deck_core.charts import graphic_frame, editable_bundled_chart
from deck_core.style import (
    BLACK, WHITE, DK, BREADCRUMB, PRELIM, FONT,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2, GRAY_3, GRAY_4, GRAY_5,
)

LAYOUT = "{layout}"

_SRC = Path(__file__).parent / "_src"
{charts_setup}
{charts_attr}


def _body() -> str:
    parts = [
{body}
    ]
    return "".join(parts)


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
    ap.add_argument("--id-base", type=int, default=100)
    a = ap.parse_args()
    convert(a.source, a.slide, a.out, a.src_dir, a.module_name, a.layout, a.id_base)


if __name__ == "__main__":
    main()
