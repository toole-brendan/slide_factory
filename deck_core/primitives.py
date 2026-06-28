"""Minimal OOXML primitives — self-contained string builders, shared by all decks.

Body / shape / table builders live here as importable functions:
run / paragraph / text_box / custom_geometry / table / connector / picture (plus
the table-cell emitters). The house chrome (breadcrumb / slide_title /
preliminary_chip / source_note) lives in deck_core.chrome, not here. Mechanical
geometry/units come from deck_core.layout. They are conveniences, not a cage: a
slide may still compose raw OOXML directly, or mix raw strings with these
builders, whenever that reads better.
"""
from __future__ import annotations
from xml.sax.saxutils import escape as _xml_escape

from deck_core.ooxml import XML_DECL, NS
from deck_core.layout import DEFAULT_FONT as FONT

# Mechanical defaults for the emitters below (line spacing, default body size).
LNSPC_BODY = 115_000     # 115% — body paragraph default
LNSPC_SINGLE = 100_000   # 100% — table-cell default
DENSE_BODY_10PT = 1000   # 10pt — default run() / table-cell body size

# Default text/border color for the emitters below. The house chrome (breadcrumb
# / title / Preliminary chip / sources) now lives in deck_core.chrome, with its
# own private geometry, colors, sizes, and ids.
BLACK = "000000"          # default run()/cell text + 1pt/1.5pt border color


# ── Private constants ─────────────────────────────────────────────────
# The XML decl + slide namespace come from deck_core.ooxml; the default font from
# deck_core.layout. No per-module copies.

_C_DK1 = "162029"

# Sentinel default for text_box(line_color=...): resolve from fill (house rule:
# a filled shape gets a black border unless the caller opts out).
_AUTO = object()


def _fill_clr_xml(color: str) -> str:
    """Inner color element for a fill: a "scheme:NAME" ref (e.g. "scheme:tx1")
    becomes <a:schemeClr val="NAME"/>; a 6-char hex becomes <a:srgbClr val="HEX"/>.
    Used by text_box(pattern_fill=...) for the pattern's fg/bg colors."""
    if color.startswith("scheme:"):
        return f'<a:schemeClr val="{color[len("scheme:"):]}"/>'
    return f'<a:srgbClr val="{color}"/>'


# ── Public API ─────────────────────────────────────────────────────────


def slide(shapes_xml: str, *, ext_lst: str = "") -> str:
    """Wrap shape XML in the full <p:sld> boilerplate.

    Returns the complete slide XML body that build() packs as
    ppt/slides/slideN.xml. `shapes_xml` is the concatenated output of
    whatever <p:sp> / <p:pic> / <p:graphicFrame> / <p:cxnSp> elements
    the slide contains; the caller is responsible for producing them.
    """
    return (
        f'{XML_DECL}\n'
        f'<p:sld {NS}>'
        f'<p:cSld><p:spTree>'
        f'<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        f'<p:grpSpPr><a:xfrm>'
        f'<a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
        f'<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/>'
        f'</a:xfrm></p:grpSpPr>'
        f'{shapes_xml}'
        f'</p:spTree>{ext_lst}</p:cSld>'
        f'<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>'
        f'</p:sld>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# Shared XML escape
# ─────────────────────────────────────────────────────────────────────────────


def esc(s: str) -> str:
    """XML-escape for element text or attribute values."""
    return _xml_escape(s, {'"': "&quot;", "'": "&apos;"})


# ─────────────────────────────────────────────────────────────────────────────
# Body builders — text runs / paragraphs / shapes / tables. Slides import these
# from deck_core.authoring rather than inlining raw OOXML. Colors are passed in as
# hex literals by the slide module (no central palette).
# ─────────────────────────────────────────────────────────────────────────────


def run(text, *, size=None, bold=None, italic=None, underline=None, color=None, font=None,
        highlight=None, lang="en-US", hyperlink_rid=None, baseline=None):
    """An <a:r> run. Any attribute left None is omitted from <a:rPr> so the
    placeholder / layout / master default applies. size is 1/100 pt
    (DENSE_BODY_10PT=1000 => 10pt, BODY_12PT=1200 => 12pt); color is 6-char
    hex, "scheme:tx1", or None. highlight is the PowerPoint text-highlighter
    colour (6-char hex / "scheme:NAME", e.g. "FFFF00"), or None for none.
    hyperlink_rid wires an external link: pass the slide-rels rId declared in the
    module's HYPERLINKS list ({"rId": ..., "url": ...}) to emit <a:hlinkClick>.
    baseline raises/lowers the run (OOXML 1/1000 %, e.g. 30000 = a superscript
    footnote marker, -25000 = subscript); None keeps it on the baseline."""
    return _emit_run({"text": text, "size": size, "bold": bold, "italic": italic,
                      "underline": underline, "color": color, "font": font,
                      "highlight": highlight, "lang": lang, "hyperlink_rid": hyperlink_rid,
                      "baseline": baseline})


def line_break():
    """An explicit in-paragraph line break (<a:br/>). Place it between run()s in a
    paragraph()'s run list to force a new line WITHOUT starting a new paragraph -
    e.g. a tight legend label that must read 'Shoreside' / 'variable costs' inside a
    narrow no-wrap box. The table-cell equivalent is tbreak()."""
    return '<a:br/>'


def paragraph(runs, *, align=None, bullet=False, bullet_char=None, level=0, space_after=0,
              space_before=None, mar_l=None, indent=None, line_spacing=LNSPC_BODY,
              end_size=None):
    """An <a:p>. `runs` is a list of run() outputs. bullet=True prepends a
    glyph (auto marL/indent); bullet_char picks the glyph ("•" default, "-" for a
    dash sub-bullet, or "auto" for an arabic-period number); space_after /
    line_spacing are pptx units. end_size (1/100 pt) sets the <a:endParaRPr> size
    of an EMPTY paragraph (no runs): a small value collapses a blank spacer line to
    that height — renderers otherwise clamp an empty line to a min height (~18pt)."""
    if bullet and mar_l is None and indent is None:
        mar_l = 142875
        indent = -142875
    attrs = []
    if align:
        attrs.append(f'algn="{align}"')
    if level:
        attrs.append(f'lvl="{level}"')
    if mar_l is not None:
        attrs.append(f'marL="{mar_l}"')
    if indent is not None:
        attrs.append(f'indent="{indent}"')
    pPr_attrs = (" " + " ".join(attrs)) if attrs else ""
    # <a:pPr> children in schema order: lnSpc -> spcAft -> buFont/buChar.
    pPr_children = ""
    if line_spacing:
        pPr_children += f'<a:lnSpc><a:spcPct val="{line_spacing}"/></a:lnSpc>'
    if space_before:
        pPr_children += f'<a:spcBef><a:spcPts val="{space_before}"/></a:spcBef>'
    if space_after:
        pPr_children += f'<a:spcAft><a:spcPts val="{space_after}"/></a:spcAft>'
    if bullet:
        if bullet_char == "auto":
            pPr_children += '<a:buAutoNum type="arabicPeriod"/>'
        else:
            pPr_children += ('<a:buFont typeface="Arial" panose="020B0604020202020204" '
                             'pitchFamily="34" charset="0"/>'
                             f'<a:buChar char="{esc(bullet_char or "•")}"/>')
    elif attrs or space_after or space_before or line_spacing:
        pPr_children += '<a:buNone/>'
    if pPr_children or attrs:
        ppr = f'<a:pPr{pPr_attrs}>{pPr_children}</a:pPr>'
    else:
        ppr = ''
    if runs:
        body = "".join(runs)
    elif end_size is not None:
        body = f'<a:endParaRPr lang="en-US" sz="{end_size}"/>'
    else:
        body = '<a:endParaRPr lang="en-US"/>'
    return f'<a:p>{ppr}{body}</a:p>'


def _prst_avlst_xml(geom_adj=None) -> str:
    """Adjustment-value list for <a:prstGeom>.

    geom_adj maps adjustment-handle names to values:
        None / {}            -> <a:avLst/>                       (no handles)
        {"adj": 42000}       -> <a:gd name="adj" fmla="val 42000"/>
        {"adj1": "val 6500"} -> formula string used verbatim
    Ints are wrapped as "val N"; strings are taken as the whole fmla. This lets a
    caller drive preset-geometry handles (a wedgeRectCallout tail via adj1/adj2,
    a roundRect corner via adj, ...) instead of the default empty list."""
    if not geom_adj:
        return '<a:avLst/>'
    parts = []
    for name, val in geom_adj.items():
        fmla = val if isinstance(val, str) else f"val {int(val)}"
        parts.append(f'<a:gd name="{esc(str(name))}" fmla="{esc(fmla)}"/>')
    return '<a:avLst>' + ''.join(parts) + '</a:avLst>'


def text_box(sp_id, name, x, y, cx, cy, paragraphs, *, anchor="t",
             fill=None, fill_alpha=None, pattern_fill=None, line_color=_AUTO, line_width=12700,
             dashed_line=False, num_cols=1, rot=0, prst="rect", geom_adj=None,
             l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720,
             insets=None, wrap="square", vert=None, body_attrs_extra="", tx_box=True,
             placeholder=None, effects=None):
    """A <p:sp> with a text body. `paragraphs` is a list of paragraph()
    strings. fill/line_color are 6-char hex or None; pass an INSETS_* tuple via
    `insets` or the four *_ins kwargs. Blue/gray fills must be ramp tokens.

    House border rule: a filled shape gets a 1pt black border automatically
    (line_color defaults to AUTO). Pass line_color="none" for a borderless
    filled shape, an explicit hex to recolor, or line_width=19050 for a 1.5pt
    focal border; an unfilled shape stays borderless.

    pattern_fill (optional) gives the shape a <a:pattFill> hatch/dot pattern
    instead of a solid fill — a dict {"prst": <DrawingML pattern>, "fg": <color>,
    "bg": <color>}, e.g. {"prst": "ltDnDiag"} for a light down-diagonal hatch.
    `prst` is a pattern preset name (ltDnDiag / dkUpDiag / pct50 / wdDnDiag / ...);
    fg/bg are a 6-char hex or a "scheme:NAME" theme ref and default to the
    think-cell standard "scheme:tx1" (dark) on "scheme:bg1" (light). When set it
    overrides `fill`; it still counts as "filled" for the AUTO border rule.

    geom_adj (optional) drives preset-geometry handles for a non-rect `prst` —
    e.g. prst="wedgeRectCallout" with {"adj1": ..., "adj2": ...} to aim the tail,
    or a roundRect corner radius. Default None emits an empty <a:avLst/>."""
    if insets is not None:
        l_ins, t_ins, r_ins, b_ins = insets
    if line_color is _AUTO:
        line_color = BLACK if (fill not in (None, "none") or pattern_fill is not None) else None
    if pattern_fill is not None:
        fill_xml = (f'<a:pattFill prst="{pattern_fill["prst"]}">'
                    f'<a:fgClr>{_fill_clr_xml(pattern_fill.get("fg", "scheme:tx1"))}</a:fgClr>'
                    f'<a:bgClr>{_fill_clr_xml(pattern_fill.get("bg", "scheme:bg1"))}</a:bgClr>'
                    f'</a:pattFill>')
    elif fill is None or fill == "none":
        fill_xml = '<a:noFill/>'
    elif fill_alpha is not None:
        # faded / transparent solid fill — fill_alpha is OOXML opacity in 1/1000 %
        # (100000 = opaque, 20000 = a 20%-opacity wash).
        fill_xml = (f'<a:solidFill><a:srgbClr val="{fill}">'
                    f'<a:alpha val="{fill_alpha}"/></a:srgbClr></a:solidFill>')
    else:
        fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
    if line_color in (None, "none"):
        line_xml = '<a:ln><a:noFill/></a:ln>'
    else:
        dash = '<a:prstDash val="dash"/>' if dashed_line else ''
        line_xml = (f'<a:ln w="{line_width}"><a:solidFill>'
                    f'<a:srgbClr val="{line_color}"/></a:solidFill>{dash}</a:ln>')
    col_attr = f' numCol="{num_cols}" spcCol="91440"' if num_cols > 1 else ''
    vert_attr = f' vert="{vert}"' if vert else ''
    rot_attr = f' rot="{rot}"' if rot else ""
    body = "".join(paragraphs)
    if placeholder is not None:
        ph_attrs = []
        if placeholder.get("type"):
            ph_attrs.append(f'type="{placeholder["type"]}"')
        if placeholder.get("sz"):
            ph_attrs.append(f'sz="{placeholder["sz"]}"')
        if placeholder.get("idx") is not None:
            ph_attrs.append(f'idx="{placeholder["idx"]}"')
        nv_pr = f'<p:nvPr><p:ph {" ".join(ph_attrs)}/></p:nvPr>'
    else:
        nv_pr = '<p:nvPr/>'
    cNvSpPr = ('<p:cNvSpPr txBox="1"/>' if tx_box
               else '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>')
    sp_pr = (f'<p:spPr><a:xfrm{rot_attr}><a:off x="{x}" y="{y}"/>'
             f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
             f'<a:prstGeom prst="{prst}">{_prst_avlst_xml(geom_adj)}</a:prstGeom>'
             f'{fill_xml}{line_xml}{effects or ""}</p:spPr>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="{esc(name)}"/>'
            f'{cNvSpPr}{nv_pr}</p:nvSpPr>{sp_pr}'
            f'<p:txBody><a:bodyPr wrap="{wrap}" anchor="{anchor}" lIns="{l_ins}" '
            f'tIns="{t_ins}" rIns="{r_ins}" bIns="{b_ins}"{col_attr}{vert_attr}{body_attrs_extra}/>'
            f'<a:lstStyle/>{body}</p:txBody></p:sp>')


def custom_geometry(sp_id, name, x, y, cx, cy, geom, *, fill=None,
                    line_color="none", line_width=12700, rot=0):
    """A <p:sp> whose outline is an arbitrary <a:custGeom> path — bézier / line
    art that no preset `prst` can express (think-cell status icons, logos, small
    vector marks). The companion to text_box for the one thing a preset shape
    can't do: a freeform path.

    `geom` is the verbatim <a:custGeom>...</a:custGeom> XML string. The path data
    (gdLst / pathLst) is intrinsic and cannot be parameterized, so lift it from
    the source and keep it as a module-level constant — and dedupe identical paths
    into ONE constant (e.g. a check glyph reused 3×). The path's own coordinate
    space scales to the cx/cy box, so position and SIZE are parameters here, along
    with fill and line: that is the faithful-but-idiomatic split — the geometry is
    verbatim, everything around it reads as Python.

    fill is a 6-char hex or None (no fill); line_color is hex or "none" (default
    "none" — these marks are usually fill-only, unlike text_box's filled-shape
    border rule). The shape carries no text (an empty body); use text_box for a
    text-bearing shape. Build a unique sp_id via the slide's n()."""
    rot_attr = f' rot="{rot}"' if rot else ""
    if fill in (None, "none"):
        fill_xml = '<a:noFill/>'
    else:
        fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
    if line_color in (None, "none"):
        line_xml = '<a:ln><a:noFill/></a:ln>'
    else:
        line_xml = (f'<a:ln w="{line_width}"><a:solidFill>'
                    f'<a:srgbClr val="{line_color}"/></a:solidFill></a:ln>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="{esc(name)}"/>'
            f'<p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm{rot_attr}><a:off x="{x}" y="{y}"/>'
            f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'{geom}{fill_xml}{line_xml}</p:spPr>'
            f'<p:txBody><a:bodyPr rtlCol="0"/><a:lstStyle/>'
            f'<a:p><a:endParaRPr lang="en-US"/></a:p></p:txBody></p:sp>')


def placeholder_sp(sp_id, name, *, ph_type=None, ph_sz=None, ph_idx=None,
                   geom=None, paragraphs=None, body_pr_xml='<a:bodyPr/>'):
    """A <p:sp> that binds to a layout placeholder by (type, sz, idx). Pass
    `geom` (dict x/y/cx/cy) to override the layout's inherited position."""
    if geom:
        sp_pr = (f'<p:spPr><a:xfrm><a:off x="{geom["x"]}" y="{geom["y"]}"/>'
                 f'<a:ext cx="{geom["cx"]}" cy="{geom["cy"]}"/></a:xfrm></p:spPr>')
    else:
        sp_pr = '<p:spPr/>'
    ph_attrs = []
    if ph_type:
        ph_attrs.append(f'type="{ph_type}"')
    if ph_sz:
        ph_attrs.append(f'sz="{ph_sz}"')
    if ph_idx is not None:
        ph_attrs.append(f'idx="{ph_idx}"')
    ph_xml = f'<p:ph {" ".join(ph_attrs)}/>' if ph_attrs else '<p:ph/>'
    body = "".join(paragraphs) if paragraphs else ''
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="{esc(name)}"/>'
            f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr>{ph_xml}</p:nvPr></p:nvSpPr>{sp_pr}'
            f'<p:txBody>{body_pr_xml}<a:lstStyle/>{body}</p:txBody></p:sp>')


def picture(sp_id, name, r_embed, x, y, cx, cy, *, src_rect=None):
    """A <p:pic> image. `r_embed` is the slide-rels rId for the media part. Declare the
    same rId in the module's IMAGES list ({"rId": r_embed, "file": "<name in ppt/media>"})
    and build_pptx wires the rel for you. Image rIds continue after chart rIds (no charts
    -> rId2; one chart -> rId3).

    src_rect crops the source image before it fills the frame: a dict of any of
    l/r/t/b in 1/1000 of a percent (e.g. {"t": 39000, "b": 39000} keeps the middle
    ~22%). Source decks crop a logo strip out of a square canvas this way; drop the
    crop and the whole canvas is stretched into the frame, so the logo renders as a
    thin sliver. Omit (None) for an uncropped image."""
    sr = ""
    if src_rect:
        attrs = "".join(f' {k}="{src_rect[k]}"' for k in ("l", "t", "r", "b") if src_rect.get(k))
        sr = f"<a:srcRect{attrs}/>" if attrs else ""
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{sp_id}" name="{esc(name)}"/>'
            f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>'
            f'<p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{r_embed}"/>{sr}'
            f'<a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/>'
            f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')


def connector(sp_id, name, x, y, cx, cy, *, color=BLACK, dashed=False, dash=None,
              width=12700, arrow=False, grad=None, grad_angle=5400000,
              prst="line", flip_h=False, flip_v=False, rot=0, adj=None):
    """Straight / right-angled connector. arrow adds a triangle arrowhead:
    True/"tail" on the tail, "head" on the head, "both" on both ends.
    width in EMU (12700 = 1pt). color None or "none" => invisible line.
    Connector lines default to BLACK (always black; solid or dashed, usually
    with an arrow at one end).

    grad (optional) makes the line a gradient instead of a solid colour: a list
    of (pos, hex) stops, e.g. [(0, "C30C3E"), (100000, "008600")] for a red->green
    confidence scale; grad_angle is the linear angle in 60000ths of a degree
    (5400000 = top-to-bottom). When set it overrides `color`.

    Dash control: `dash` names the prstDash preset explicitly ("dash", "lgDash",
    "sysDash", "sysDot", ...) to match a source line exactly; it takes precedence
    over the legacy `dashed=True` shorthand (which still means val="dash"). Leave
    both unset for a solid line.

    DrawingML <a:ext> must be a non-negative size box: a left/up vector
    (negative cx/cy) is normalized to a positive extent + flipH/flipV with the
    offset shifted, so callers can pass any signed cx/cy without tripping a
    PowerPoint "repair" on open.

    To reproduce a source connector faithfully, pass a POSITIVE cx/cy box plus its
    orientation: flip_h/flip_v (mirror within the box), rot (60000ths of a degree,
    applied about the box centre - elbow connectors are often rot=5400000/16200000),
    and adj (preset-geometry adjustments, e.g. {"adj1": "val 25000"} for an elbow's
    bend point; omit for the 50% default). flip_h/flip_v OR with the sign of cx/cy,
    so the signed-vector shorthand above still works for simple straight lines."""
    do_flip_h = flip_h or cx < 0
    do_flip_v = flip_v or cy < 0
    off_x = x + cx if cx < 0 else x
    off_y = y + cy if cy < 0 else y
    cx, cy = abs(cx), abs(cy)
    flip_attr = (' flipH="1"' if do_flip_h else '') + (' flipV="1"' if do_flip_v else '')
    rot_attr = f' rot="{rot}"' if rot else ''
    if dash:
        dash_xml = f'<a:prstDash val="{dash}"/>'
    elif dashed:
        dash_xml = '<a:prstDash val="dash"/>'
    else:
        dash_xml = ''
    head = '<a:headEnd type="triangle" w="med" len="med"/>' if arrow in ("head", "both") else ''
    tail = '<a:tailEnd type="triangle" w="med" len="med"/>' if arrow in (True, "tail", "both") else ''
    if adj:
        av_xml = '<a:avLst>' + ''.join(
            f'<a:gd name="{k}" fmla="{v}"/>' for k, v in adj.items()) + '</a:avLst>'
    else:
        av_xml = '<a:avLst/>'
    if grad:
        stops = "".join(f'<a:gs pos="{pos}"><a:srgbClr val="{c}"/></a:gs>' for pos, c in grad)
        ln_fill = (f'<a:gradFill flip="none" rotWithShape="1"><a:gsLst>{stops}</a:gsLst>'
                   f'<a:lin ang="{grad_angle}" scaled="1"/></a:gradFill>')
    elif color in (None, "none"):
        ln_fill = '<a:noFill/>'
    else:
        ln_fill = f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
    return (f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{sp_id}" name="{esc(name)}"/>'
            f'<p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>'
            f'<p:spPr><a:xfrm{rot_attr}{flip_attr}><a:off x="{off_x}" y="{off_y}"/>'
            f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="{prst}">{av_xml}</a:prstGeom>'
            f'<a:ln w="{width}">{ln_fill}{dash_xml}{head}{tail}</a:ln></p:spPr></p:cxnSp>')


# -- Tables (native <a:tbl> via <p:graphicFrame>) -----------------------------

# Built-in "No Style, No Grid" table style — the SAME GUID house_table() uses, so
# a low-level table() table and a house_table() table share one posture and pick
# up no theme grid lines on edit / copy / reset. Built-in style GUIDs resolve
# internally; no tableStyles.xml entry is needed.
NO_STYLE_NO_GRID = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"


def trun(text, *, size=DENSE_BODY_10PT, bold=None, italic=None, underline=None,
         color=BLACK, font=FONT, hyperlink_rid=None, baseline=None):
    """Run dict for table cells (consumed by tpara / tcell_rich). hyperlink_rid
    wires an external link via the module's HYPERLINKS rId (see run()). baseline
    raises/lowers the run (OOXML 1/1000 %, e.g. 30000 = a superscript footnote
    marker); None keeps it on the baseline."""
    return {"text": text, "size": size, "bold": bold, "italic": italic,
            "underline": underline, "color": color, "font": font,
            "hyperlink_rid": hyperlink_rid, "baseline": baseline}


def tbreak():
    """An explicit line break inside a table cell paragraph - the tpara()/trun()
    equivalent of line_break(). Place it between trun()s in a tpara()'s run list."""
    return {"break": True}


def tpara(runs, *, align="l", line_spacing=LNSPC_SINGLE, space_after=None, space_before=None,
          end_size=None, bullet=False, bullet_char=None, level=0, mar_l=None, indent=None):
    """Paragraph dict for table cells. line_spacing defaults to single (100%) —
    the correct density for tabular data (body text is 115%); raise it only for a
    cell that needs breathing room. space_after is in EMU pts (rarely needed).
    end_size (1/100 pt) sets the <a:endParaRPr> size of an EMPTY paragraph (no
    runs): a small value (e.g. 100 = 1pt) collapses a spacer row/column, which an
    empty run cannot do — renderers clamp an empty run to a min line height.

    bullet/bullet_char/level/mar_l/indent give a cell paragraph the same bulleting
    + hanging indent the text_box paragraph() has (a bulleted list inside a cell):
    bullet_char picks the glyph ("•" default, "-" for a dash sub-bullet, "auto" for
    an arabic-period number); mar_l/indent are the EMU hanging-indent pair."""
    p = {"align": align, "runs": runs, "line_spacing": line_spacing}
    if space_after is not None:
        p["space_after"] = space_after
    if space_before is not None:
        p["space_before"] = space_before
    if end_size is not None:
        p["end_size"] = end_size
    if bullet:
        p["bullet"] = True
        p["bullet_char"] = bullet_char if bullet_char is not None else "•"
    if level:
        p["level"] = level
    if mar_l is not None:
        p["marL"] = mar_l
    if indent is not None:
        p["indent"] = indent
    return p


def tcell_rich(paragraphs, *, fill=None, grid_span=1, row_span=1, anchor="ctr",
               l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, borders=None,
               vert=None):
    """Multi-paragraph table cell. gridSpan/rowSpan filler cells are
    synthesized by the framework - do not author them. `borders` is keyed by
    side ("L"/"R"/"T"/"B") -> "none" or {"color": hex, "width": EMU}. t_ins/b_ins are
    the vertical text insets (EMU); tighten them to fit a dense, many-row table inside
    its frame height (think-cell auto-rows render compact). `vert` rotates the cell
    text via tcPr (e.g. "vert270" for a 270° spine label); None keeps it horizontal."""
    return {"paragraphs": paragraphs, "fill": fill, "gridSpan": grid_span,
            "rowSpan": row_span, "anchor": anchor, "vert": vert,
            "body_pr": {"lIns": l_ins, "rIns": r_ins, "tIns": t_ins, "bIns": b_ins},
            "borders": borders or {}}


def tcell(text, *, fill=None, size=DENSE_BODY_10PT, bold=None, italic=None, color=BLACK,
          align="l", grid_span=1, row_span=1, anchor="ctr", font=FONT,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, borders=None,
          line_spacing=LNSPC_SINGLE, vert=None):
    """Single-paragraph single-run cell - shortcut over tcell_rich(). line_spacing
    defaults to single (100%): tabular density, not the 115% body default. An empty
    text ("") emits a runless paragraph whose <a:endParaRPr> carries `size`, so a
    spacer cell at size=PT(1) collapses its row/column (an empty run would not —
    renderers clamp it to a minimum line height)."""
    if text == "":
        para = tpara([], align=align, line_spacing=line_spacing, end_size=size)
    else:
        para = tpara([trun(text, size=size, bold=bold, italic=italic,
                           color=color, font=font)], align=align, line_spacing=line_spacing)
    return tcell_rich([para],
                      fill=fill, grid_span=grid_span, row_span=row_span, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=borders,
                      vert=vert)


def trow(cells, *, h=274_320):
    """Row dict for table(). h is row height in EMU (a MINIMUM, not a cap).
    Default = the ~0.3in readability floor, so a single-line row clears the
    slide_probe --table-fit check; size a wrapping row up to clear its text
    (slide_probe's estimate_row_heights reports the honest per-row height)."""
    return {"h": h, "cells": cells}


def table(sp_id, name, x, y, cx, cy, *, col_widths, rows,
          first_row=True, first_col=True, band_row=False,
          table_style_id=NO_STYLE_NO_GRID):
    """Hand-built native <a:tbl> graphic frame. col_widths in EMU summing
    ~cx; rows is a list of trow() outputs. Cell fills follow the ramp rule.

    Defaults to the "No Style, No Grid" table style (same GUID as
    house_table()) with firstRow/firstCol semantics on, so explicit per-cell
    borders are the only edges that show and the table picks up no theme grid
    lines on edit / copy / reset. Any side a cell does not specify is emitted as
    an explicit no-fill border (see _emit_cell), so a cell with only a bottom
    rule is deterministically bottom-rule-only regardless of the table style."""
    return _emit_table_frame({"id": sp_id, "name": name,
                              "geom": {"x": x, "y": y, "cx": cx, "cy": cy},
                              "col_widths": col_widths, "rows": rows,
                              "first_row": first_row, "first_col": first_col,
                              "band_row": band_row,
                              "table_style_id": table_style_id})


_HMERGE_FILLER = ('<a:tc hMerge="1"><a:txBody><a:bodyPr/><a:lstStyle/>'
                  '<a:p><a:endParaRPr lang="en-US"/></a:p></a:txBody><a:tcPr/></a:tc>')
_VMERGE_FILLER = ('<a:tc vMerge="1"><a:txBody><a:bodyPr/><a:lstStyle/>'
                  '<a:p><a:endParaRPr lang="en-US"/></a:p></a:txBody><a:tcPr/></a:tc>')
_VHMERGE_FILLER = ('<a:tc vMerge="1" hMerge="1"><a:txBody><a:bodyPr/><a:lstStyle/>'
                   '<a:p><a:endParaRPr lang="en-US"/></a:p></a:txBody><a:tcPr/></a:tc>')


def _emit_cell(cell):
    paragraphs = cell.get("paragraphs", [])
    body_pr = cell.get("body_pr", {})
    fill = cell.get("fill")
    borders = cell.get("borders", {}) or {}
    anchor = cell.get("anchor", "ctr")
    # Cell text inset lives in tcPr (marL/marR/marT/marB) ONLY — not duplicated
    # on bodyPr, or PowerPoint can honor both and double the padding. These match
    # the 0.05in inset slide_probe's row-height estimator assumes, so they agree.
    CELL_INSET_V = 45720
    CELL_INSET_H = 45720
    lIns = body_pr.get("lIns") if body_pr.get("lIns") is not None else CELL_INSET_H
    rIns = body_pr.get("rIns") if body_pr.get("rIns") is not None else CELL_INSET_H
    tIns = body_pr.get("tIns") if body_pr.get("tIns") is not None else CELL_INSET_V
    bIns = body_pr.get("bIns") if body_pr.get("bIns") is not None else CELL_INSET_V
    bp_attrs = []
    if body_pr.get("wrap"):
        bp_attrs.append(f'wrap="{body_pr["wrap"]}"')
    bp_attrs.append(f'anchor="{anchor}"')
    bp_attr_str = " " + " ".join(bp_attrs)
    para_xml = ("".join(_emit_paragraph(p) for p in paragraphs)
                or '<a:p><a:endParaRPr lang="en-US"/></a:p>')
    # Emit ALL four sides explicitly: a side the caller omits becomes an explicit
    # no-fill border, so a cell with only a bottom rule is deterministic
    # regardless of the table style PowerPoint applies on edit / copy / reset.
    border_xml = ""
    for side in ("L", "R", "T", "B"):
        spec = borders.get(side)
        if spec is None or spec == "none":
            border_xml += f'<a:ln{side}><a:noFill/></a:ln{side}>'
        else:
            bcolor = spec.get("color")
            bwidth = spec.get("width", 0)
            attr_w = f' w="{bwidth}"' if bwidth else ''
            if bcolor and bcolor != "none":
                border_xml += (f'<a:ln{side}{attr_w} cap="flat" cmpd="sng" algn="ctr">'
                               f'<a:solidFill><a:srgbClr val="{bcolor}"/></a:solidFill>'
                               f'<a:prstDash val="solid"/></a:ln{side}>')
            else:
                border_xml += f'<a:ln{side}{attr_w}><a:noFill/></a:ln{side}>'
    fill_xml = (f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
                if fill and fill != "none" else '<a:noFill/>')
    vert = cell.get("vert")
    vert_attr = f' vert="{vert}"' if vert else ''
    tcPr = (f'<a:tcPr marL="{lIns}" marR="{rIns}" marT="{tIns}" '
            f'marB="{bIns}" anchor="{anchor}"{vert_attr}>{border_xml}{fill_xml}</a:tcPr>')
    span_attrs = ""
    if cell.get("gridSpan", 1) > 1:
        span_attrs += f' gridSpan="{cell["gridSpan"]}"'
    if cell.get("rowSpan", 1) > 1:
        span_attrs += f' rowSpan="{cell["rowSpan"]}"'
    if cell.get("hMerge"):
        span_attrs += ' hMerge="1"'
    if cell.get("vMerge"):
        span_attrs += ' vMerge="1"'
    return (f'<a:tc{span_attrs}><a:txBody><a:bodyPr{bp_attr_str}/>'
            f'<a:lstStyle/>{para_xml}</a:txBody>{tcPr}</a:tc>')


def _emit_paragraph(p):
    align = p.get("align")
    level = p.get("level", 0)
    marL = p.get("marL")
    indent = p.get("indent")
    space_after = p.get("space_after")
    space_before = p.get("space_before")
    bullet = p.get("bullet")
    bullet_char = p.get("bullet_char")
    line_spacing = p.get("line_spacing", LNSPC_BODY)
    attrs = []
    if align:
        attrs.append(f'algn="{align}"')
    if level:
        attrs.append(f'lvl="{level}"')
    if marL is not None:
        attrs.append(f'marL="{marL}"')
    if indent is not None:
        attrs.append(f'indent="{indent}"')
    pPr_inner = ""
    if line_spacing:
        pPr_inner += f'<a:lnSpc><a:spcPct val="{line_spacing}"/></a:lnSpc>'
    if space_before:
        pPr_inner += f'<a:spcBef><a:spcPts val="{space_before}"/></a:spcBef>'
    if space_after:
        pPr_inner += f'<a:spcAft><a:spcPts val="{space_after}"/></a:spcAft>'
    if bullet:
        if bullet_char and bullet_char != "auto":
            pPr_inner += ('<a:buFont typeface="Arial" panose="020B0604020202020204" '
                          'pitchFamily="34" charset="0"/>'
                          f'<a:buChar char="{esc(bullet_char)}"/>')
        else:
            pPr_inner += '<a:buAutoNum type="arabicPeriod"/>'
    if attrs or pPr_inner:
        attr_s = (" " + " ".join(attrs)) if attrs else ""
        ppr = f'<a:pPr{attr_s}>{pPr_inner}</a:pPr>'
    else:
        ppr = ''
    if p.get("runs"):
        rxml = "".join(_emit_run(r) for r in p["runs"])
    else:
        # Runless paragraph -> <a:endParaRPr> only (no run). end_size collapses a
        # spacer cell; an empty run would be clamped to a min line height instead.
        end_sz = p.get("end_size")
        sz_attr = f' sz="{end_sz}"' if end_sz else ''
        rxml = f'<a:endParaRPr lang="en-US"{sz_attr}/>'
    return f'<a:p>{ppr}{rxml}</a:p>'


def _emit_run(r):
    if r.get("break"):          # tbreak() / line break inside a cell paragraph
        return '<a:br/>'
    text = r.get("text", "")
    size = r.get("size")
    bold = r.get("bold")
    italic = r.get("italic")
    underline = r.get("underline")
    color = r.get("color")
    font = r.get("font")
    lang = r.get("lang") or "en-US"
    rpr_attrs = [f'lang="{lang}"']
    if size is not None:
        rpr_attrs.append(f'sz="{size}"')
    if bold is not None:
        rpr_attrs.append(f'b="{1 if bold else 0}"')
    if italic is not None:
        rpr_attrs.append(f'i="{1 if italic else 0}"')
    if underline:
        rpr_attrs.append('u="sng"')
    baseline = r.get("baseline")
    if baseline is not None:
        rpr_attrs.append(f'baseline="{baseline}"')   # superscript/subscript (1/1000 %)
    rpr_attr_str = " " + " ".join(rpr_attrs)
    rpr_children = ""
    if color is not None:
        if color.startswith("scheme:"):
            rpr_children += (f'<a:solidFill><a:schemeClr '
                             f'val="{color[len("scheme:"):]}"/></a:solidFill>')
        elif color != "none":
            rpr_children += f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
    # <a:highlight> follows the run fill and precedes the font run (schema order).
    highlight = r.get("highlight")
    if highlight:
        if highlight.startswith("scheme:"):
            rpr_children += f'<a:highlight><a:schemeClr val="{highlight[len("scheme:"):]}"/></a:highlight>'
        elif highlight != "none":
            rpr_children += f'<a:highlight><a:srgbClr val="{highlight}"/></a:highlight>'
    if font is not None:
        rpr_children += (f'<a:latin typeface="{font}"/><a:ea typeface="{font}"/>'
                         f'<a:cs typeface="{font}"/>')
    # <a:hlinkClick> is the last rPr child (schema order); r: is declared on the
    # slide root, so a bare r:id resolves (same as chart graphic-frame refs).
    hyperlink_rid = r.get("hyperlink_rid")
    if hyperlink_rid:
        rpr_children += f'<a:hlinkClick r:id="{hyperlink_rid}"/>'
    if rpr_children:
        rpr = f'<a:rPr{rpr_attr_str} dirty="0">{rpr_children}</a:rPr>'
    else:
        rpr = f'<a:rPr{rpr_attr_str}/>'
    return f'<a:r>{rpr}<a:t>{esc(text)}</a:t></a:r>'


def _emit_table_frame(entry):
    geom = entry["geom"]
    rows = entry.get("rows", [])
    col_widths = entry.get("col_widths", [])
    sp_id = entry["id"]
    name = entry["name"] or "Table"
    first_row = entry.get("first_row", True)
    first_col = entry.get("first_col", True)
    band_row = entry.get("band_row", False)
    style_id = entry.get("table_style_id", NO_STYLE_NO_GRID)
    grid = "".join(f'<a:gridCol w="{w}"/>' for w in col_widths)
    n_cols = len(col_widths)
    # vMerge bookkeeping per grid column (counts down each row; the _h_filler
    # flag marks columns also under a horizontal span, so the filler gets both).
    active_vmerge = [0] * n_cols
    vmerge_is_h_filler = [False] * n_cols
    tr_xml = []
    for row_idx, row in enumerate(rows):
        src_cells = row.get("cells", [])
        cells_xml_parts = []
        col = 0
        src_idx = 0
        while col < n_cols:
            if active_vmerge[col] > 0:
                cells_xml_parts.append(
                    _VHMERGE_FILLER if vmerge_is_h_filler[col] else _VMERGE_FILLER)
                active_vmerge[col] -= 1
                col += 1
                continue
            if src_idx >= len(src_cells):
                raise ValueError(f"table row {row_idx}: ran out of source cells at "
                                 f"column {col} (grid has {n_cols} columns)")
            c = src_cells[src_idx]
            src_idx += 1
            gs = c.get("gridSpan", 1)
            rs = c.get("rowSpan", 1)
            # Validate the span BEFORE emitting any cell/filler XML, and guard
            # the column overrun for horizontal merges too (not only rowSpan>1):
            # a pure horizontal over-merge would otherwise append too many filler
            # cells and push `col` past the grid silently.
            if gs < 1 or rs < 1:
                raise ValueError(f"table row {row_idx}: cell at column {col} has "
                                 f"gridSpan={gs}, rowSpan={rs}; both must be >= 1")
            if col + gs > n_cols:
                raise ValueError(f"table row {row_idx}: cell at column {col} "
                                 f"gridSpan={gs} extends past column count {n_cols}")
            cells_xml_parts.append(_emit_cell(c))
            if gs > 1:
                cells_xml_parts.extend([_HMERGE_FILLER] * (gs - 1))
            if rs > 1:
                active_vmerge[col] = rs - 1
                vmerge_is_h_filler[col] = False
                for k in range(1, gs):
                    active_vmerge[col + k] = rs - 1
                    vmerge_is_h_filler[col + k] = True
            col += gs
        if src_idx != len(src_cells):
            raise ValueError(f"table row {row_idx}: {len(src_cells) - src_idx} extra "
                             f"source cell(s) after grid was filled")
        tr_xml.append(f'<a:tr h="{row.get("h", 0)}">{"".join(cells_xml_parts)}</a:tr>')
    if any(v != 0 for v in active_vmerge):
        raise ValueError(f"table: rowSpan extends past last row ({active_vmerge})")
    rows_xml = "".join(tr_xml)
    return (f'<p:graphicFrame><p:nvGraphicFramePr>'
            f'<p:cNvPr id="{sp_id}" name="{esc(name)}"/>'
            f'<p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr>'
            f'<p:nvPr/></p:nvGraphicFramePr>'
            f'<p:xfrm><a:off x="{geom["x"]}" y="{geom["y"]}"/>'
            f'<a:ext cx="{geom["cx"]}" cy="{geom["cy"]}"/></p:xfrm>'
            f'<a:graphic>'
            f'<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
            f'<a:tbl><a:tblPr firstRow="{1 if first_row else 0}" '
            f'firstCol="{1 if first_col else 0}" '
            f'bandRow="{1 if band_row else 0}">'
            f'<a:tableStyleId>{style_id}</a:tableStyleId>'
            f'</a:tblPr><a:tblGrid>{grid}</a:tblGrid>{rows_xml}'
            f'</a:tbl></a:graphicData></a:graphic></p:graphicFrame>')
