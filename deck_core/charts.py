"""Native PowerPoint chart XML generation with embedded xlsx data.

Public factories (each returns the dict below; marimekko_chart also returns
label_meta — see its docstring):

    column_chart(...)      vertical columns  — mode: clustered | stacked | percent | ranked
    bar_chart(...)         horizontal bars   — same modes (auto top-to-bottom ranked look)
    line_chart(...)        one line per series
    waterfall_chart(...)   waterfall as a stacked-column workaround (native, editable)
    marimekko_chart(...)   variable-width percent-stacked columns (native, editable)
    graphic_frame(...)     the <p:graphicFrame> that places a chart on a slide

Two more entry points handle a chart ported verbatim from a source deck:
editable_bundled_chart() reattaches the source workbook to a byte-exact chart
part (the data stays opaque, in caches + workbook only); styled_chart() keeps
the source part as a pure style template but rewrites its data caches from a
Python dict, so the values live in the slide module (readable / editable) while
the look stays pixel-identical to the source — the faithful way to surface a
real, style-dense chart's data without a lossy factory rebuild (it even covers
bar+line combos). extract_chart_data() reads a chart part into that dict shape.

column_chart / bar_chart are thin faces over the private _bars() engine; the
specialty factories transform their inputs and call the same engine, so every
chart shares one code path, one embedded-workbook mechanism, and one look.
For the static-think-cell aesthetic, spread THINKCELL_BARS (below) into
column_chart/bar_chart and pair with deck_core.style.chart_accent_seq() +
deck_core.chart_key.chart_key().

Each factory returns a dict with three parts:

    {
        "chart_xml":  str    — body of ppt/charts/chartN.xml
        "embed_xlsx": bytes  — complete .xlsx zip (ppt/embeddings/Microsoft_Excel_WorksheetN.xlsx)
        "chart_rels": str    — body of ppt/charts/_rels/chartN.xml.rels (template;
                                _build.py formats it with the global chart_num)
    }

Each chart ships with its own embedded mini-xlsx inside the .pptx zip. The
chart XML references the embedded workbook through c:strRef / c:numRef +
parallel c:strCache / c:numCache blocks; a <c:externalData r:id="rId1"/>
element at the end of <c:chartSpace> wires the chart to its embedded
workbook via the chart's own rels file. Result: PowerPoint's "Edit Data"
button opens a real mini-Excel pane on the chart's data; edits flow back
to the chart on save. The embedded workbook is self-contained — no link
to sub_workbook/sub.xlsx.

When embed_data=False, the function falls back to inline literal data
(c:strLit / c:numLit) and returns embed_xlsx=None, chart_rels=None.
PowerPoint will render the chart but "Edit Data" stays disabled.

See infra/ooxml_reference/ooxml_cheat_sheet_pptx.md §20-23 (chart architecture) and
2026-05-28_deck_expansion_ooxml_companion.md "Embedded workbooks for
editable chart data" for the full mechanics.

Slide-side usage: build the chart, expose CHARTS, place a graphic_frame at rId2.
At build time _build.py reads each module's `CHARTS` list, writes the chart part
+ rels + embedded xlsx, and wires the slide->chart relationship.
"""
from __future__ import annotations

import io
import zipfile
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape as _esc_text

# Shared XML decl + chart-root namespace string (single source of truth).
from deck_core.ooxml import (
    XML_DECL as _XML_DECL, NS_CHART as _NS, NS_A, NS_C, NS_MC, NS_R,
)


def _esc(s: str) -> str:
    """Escape for XML element content (&, <, >). Quotes pass through."""
    return _esc_text(s)


def _esc_attr(s: str) -> str:
    """Escape for an XML attribute value (&, <, >, and double-quote).

    Required for number format codes like `"$"#,##0.0"M"` where the
    formatCode string contains literal double-quotes that would otherwise
    close the attribute prematurely.
    """
    return _esc_text(s, {'"': "&quot;"})


# ── Readable data-label color (the "dark text on a dark bar" fix) ─────────
# A data label drawn INSIDE a bar/column must flip to white on a dark fill or
# it becomes unreadable. Charts are exhibits, not chrome: default label/axis/
# title text is BLACK (default exhibit text is 000000);
# WHITE is the on-dark text.
BLACK = "000000"   # default chart/exhibit label color
WHITE = "FFFFFF"   # label color on a dark fill

# Label positions that draw the label ON the bar (vs on the plot background).
_INSIDE_DLBL_POS = {"ctr", "inEnd", "inBase"}


def _perceived_brightness(hex6: str) -> float:
    """Perceived brightness of an RRGGBB hex on 0..1 (ITU-R BT.601 luma).
    Higher = lighter."""
    h = hex6.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0


def _label_color_on(fill_hex: str | None) -> str:
    """Readable label color for text drawn on `fill_hex`: WHITE on a dark fill
    (brightness < 0.55 — BLUE_3/4/5, GRAY_4/5), else BLACK. A None/empty fill
    means the label sits on the light plot background, so BLACK. The 0.55 cutoff
    matches the house rule "WHITE on BLUE_3/4/5, GRAY_5"; tune here if the
    palette changes."""
    if not fill_hex:
        return BLACK
    return WHITE if _perceived_brightness(fill_hex) < 0.55 else BLACK


# ────────────────────────────────────────────────────────────────────────
# Embedded-xlsx static parts
# ────────────────────────────────────────────────────────────────────────
# Six OOXML files compose the minimum-viable embedded workbook PowerPoint
# accepts. Five are identical for every chart (constants below); the sixth
# (xl/worksheets/sheet1.xml) holds the chart's data and is built per-chart
# by _build_sheet1().

_EMBED_CONTENT_TYPES = (
    f'{_XML_DECL}\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" '
    'ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/xl/workbook.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
    '<Override PartName="/xl/worksheets/sheet1.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
    '<Override PartName="/xl/styles.xml" '
    'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
    '</Types>'
)

_EMBED_ROOT_RELS = (
    f'{_XML_DECL}\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
    'Target="xl/workbook.xml"/>'
    '</Relationships>'
)

_EMBED_WORKBOOK = (
    f'{_XML_DECL}\n'
    '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets>'
    '</workbook>'
)

_EMBED_WORKBOOK_RELS = (
    f'{_XML_DECL}\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
    'Target="worksheets/sheet1.xml"/>'
    '<Relationship Id="rId2" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
    'Target="styles.xml"/>'
    '</Relationships>'
)

_EMBED_STYLES = (
    f'{_XML_DECL}\n'
    '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
    '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
    '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
    '<borders count="1"><border/></borders>'
    '<cellStyleXfs count="1">'
    '<xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>'
    '</cellStyleXfs>'
    '<cellXfs count="1">'
    '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
    '</cellXfs>'
    '</styleSheet>'
)

# Chart's own rels file (lives at ppt/charts/_rels/chartN.xml.rels). An OPC
# relationship Target is resolved relative to the SOURCE PART (ppt/charts/chartN.xml),
# i.e. relative to ppt/charts/ — not relative to the _rels folder. So
# "../embeddings/..." goes ppt/charts/ -> up to ppt/ -> down into ppt/embeddings/.
# The {chart_num} placeholder is filled in by _build.py at build time so each
# chart's rels points at its own embed.
_CHART_RELS_TEMPLATE = (
    f'{_XML_DECL}\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" '
    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/package" '
    'Target="../embeddings/Microsoft_Excel_Worksheet{chart_num}.xlsx"/>'
    '</Relationships>'
)


# ── Reattaching a source workbook to a verbatim-bundled chart ────────────
# A faithfully-ported chart part (pasted verbatim from a source deck, then had
# its <c:externalData> link stripped so it renders from cache alone) is NOT
# editable: PowerPoint greys out "Edit Data" because no workbook backs it.
# editable_bundled_chart restores that link by shipping the chart's ORIGINAL
# embedded workbook — the .xlsb/.xlsx its <c:f> formulas already reference —
# back into the package and re-adding <c:externalData r:id="rId1">. The chart's
# caches and every other byte stay untouched, so the rendered result is
# identical; only the Edit-Data backing is restored. Most faithful with the
# binary .xlsb the source actually carried (no data reconstruction).
_BUNDLED_EMBED_SPECS = {
    # ext -> (embeddings filename template, [Content_Types] content type)
    "xlsb": ("Microsoft_Excel_BinaryWorksheet{chart_num}.xlsb",
             "application/vnd.ms-excel.sheet.binary.macroEnabled.12"),
    "xlsx": ("Microsoft_Excel_Worksheet{chart_num}.xlsx",
             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
}


def editable_bundled_chart(chart_xml: str, embed_bytes: bytes, *,
                           embed_ext: str = "xlsb") -> dict:
    """Make a verbatim-bundled <c:chart> part editable by reattaching its
    source embedded workbook.

    Args:
        chart_xml: the bundled chart part — caches intact, <c:externalData>
            stripped (the faithful-port default). If it already carries
            <c:externalData>, it is left untouched.
        embed_bytes: the source workbook the chart's <c:f> refs point at,
            copied in verbatim (e.g. the original
            Microsoft_Excel_Binary_Worksheet*.xlsb).
        embed_ext: "xlsb" to reuse the binary source workbook (default, most
            faithful — no reconstruction), or "xlsx".

    Returns the CHARTS dict (chart_xml / embed_xlsx / chart_rels /
    embed_filename / embed_content_type) the build loop wires into the package.
    """
    if embed_ext not in _BUNDLED_EMBED_SPECS:
        raise ValueError(
            f"embed_ext must be one of {sorted(_BUNDLED_EMBED_SPECS)}; "
            f"got {embed_ext!r}")
    filename_tpl, content_type = _BUNDLED_EMBED_SPECS[embed_ext]
    if "<c:externalData" not in chart_xml:
        if "</c:chartSpace>" not in chart_xml:
            raise ValueError(
                "chart_xml has no </c:chartSpace> to anchor <c:externalData>")
        # externalData is the last chartSpace child here (no printSettings/
        # userShapes follow </c:chart> in these parts), so inserting right
        # before </c:chartSpace> keeps the CT_ChartSpace element order valid.
        chart_xml = chart_xml.replace(
            "</c:chartSpace>",
            '<c:externalData r:id="rId1"><c:autoUpdate val="0"/>'
            "</c:externalData></c:chartSpace>",
        )
    chart_rels = (
        f'{_XML_DECL}\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/package" '
        f'Target="../embeddings/{filename_tpl}"/>'
        '</Relationships>'
    )
    return {
        "chart_xml": chart_xml,
        "embed_xlsx": embed_bytes,
        "chart_rels": chart_rels,
        "embed_filename": filename_tpl,
        "embed_content_type": content_type,
    }


# ── Data-over-template charts (faithful style + Python-visible data) ──────────
# editable_bundled_chart (above) is byte-exact but opaque: a chart's data lives
# only inside its <c:numCache> blocks and the embedded workbook. styled_chart
# keeps that exact styling template yet rewrites the caches from a Python `data`
# dict, so the values become a readable/editable literal in the slide module
# while the look stays pixel-identical to the source — colors, axes, data-label
# selection, pattern fills, bar+line combos: everything that is *style* is
# inherited verbatim from the template. It is the editable-data half of "Edit
# Data" surfaced as Python; the style half stays templated by design. Because it
# never interprets the chart (only its caches), it reproduces charts a factory
# (column_chart/…) cannot. extract_chart_data() reads a part into the same shape.

# Microsoft chart-extension prefixes a source part may carry beyond c/a/r/mc.
# Registering every prefix makes ET re-serialize a parsed chart with its
# original prefixes (no ns0: churn), so a parse->serialize round-trip preserves
# the full element inventory (verified across the reference corpus).
_CHART_NS_REGISTRY = {
    "c": NS_C, "a": NS_A, "r": NS_R, "mc": NS_MC,
    "c14": "http://schemas.microsoft.com/office/drawing/2007/8/2/chart",
    "c15": "http://schemas.microsoft.com/office/drawing/2012/chart",
    "c16": "http://schemas.microsoft.com/office/drawing/2014/chart",
    "c16r2": "http://schemas.microsoft.com/office/drawing/2015/06/chart",
}
for _pfx, _uri in _CHART_NS_REGISTRY.items():
    ET.register_namespace(_pfx, _uri)


def _ct(tag: str) -> str:
    """Chart-namespaced ElementTree tag, e.g. _ct('ser') -> '{...chart}ser'."""
    return f"{{{NS_C}}}{tag}"


def _at(tag: str) -> str:
    """DrawingML-namespaced ElementTree tag, e.g. _at('solidFill')."""
    return f"{{{NS_A}}}{tag}"


def _iter_chart_series(root):
    """Yield every <c:ser> under plotArea, in document order across all
    chart-type containers (barChart series, then lineChart series, ...). This
    order is the contract `data['series']` must match — extraction and rewrite
    both use it, so they stay aligned even for bar+line combos."""
    chart = root.find(_ct("chart"))
    plot = (chart.find(_ct("plotArea")) if chart is not None
            else root.find(".//" + _ct("plotArea")))
    if plot is None:
        return
    for container in list(plot):
        if container.tag.split("}")[-1].endswith("Chart"):
            for ser in container.findall(_ct("ser")):
                yield ser


def _cache_node(parent):
    """The numCache/strCache (or numLit/strLit) under a <c:cat>/<c:val>/<c:tx>,
    or None when the parent or its cache is absent (think-cell omits cat/tx)."""
    if parent is None:
        return None
    for kind in ("numCache", "strCache", "numLit", "strLit"):
        node = parent.find(".//" + _ct(kind))
        if node is not None:
            return node
    return None


def _cache_values(parent, *, numeric):
    """Ordered values from a cache node — None at any blank/missing index. With
    numeric=True, parse floats (rounded; caches carry binary float artifacts)."""
    node = _cache_node(parent)
    if node is None:
        return None
    by_idx = {}
    for pt in node.findall(_ct("pt")):
        v = pt.find(_ct("v"))
        by_idx[int(pt.get("idx"))] = v.text if v is not None else None
    pc = node.find(_ct("ptCount"))
    n = int(pc.get("val")) if pc is not None else 0
    n = max(n, (max(by_idx) + 1) if by_idx else 0)
    out = [by_idx.get(i) for i in range(n)]
    if numeric:
        out = [None if x in (None, "") else round(float(x), 4) for x in out]
    return out


def _series_name(ser):
    """Series name from <c:tx> (cache or literal), or None if absent."""
    tx = ser.find(_ct("tx"))
    if tx is None:
        return None
    vals = _cache_values(tx, numeric=False)
    if vals:
        return next((v for v in vals if v), None)
    v = tx.find(_ct("v"))
    return v.text if v is not None else None


def _series_color(ser):
    """Series fill as a hex string from <c:spPr><a:solidFill><a:srgbClr>, or
    None (theme/scheme fills and per-point dPt fills stay in the template)."""
    sppr = ser.find(_ct("spPr"))
    if sppr is None:
        return None
    fill = sppr.find(_at("solidFill"))
    if fill is None:
        return None
    srgb = fill.find(_at("srgbClr"))
    return srgb.get("val") if srgb is not None else None


def extract_chart_data(chart_xml: str) -> dict:
    """Read a chart part into the `data` dict styled_chart consumes.

    Returns::

        {
            "categories": list[str] | None,   # None when the chart omits them
            "series": [{"name": str|None, "values": list[float|None],
                        "color": str|None}, ...],
            "value_axis_max": float | None,
            "gap_width": int | None,
            "overlap": int | None,
            "types": [{"type": str, "grouping": str|None, "n_ser": int}, ...],
        }

    Series come out in document order across every chart-type container — the
    order _iter_chart_series yields and styled_chart rewrites — so a round-trip
    (extract -> styled_chart) reproduces the source, combos included. think-cell
    parts omit categories and series names (they are drawn as separate slide
    shapes): both come back None; `values` and per-series solid `color` are
    recovered from the caches. `color` is informational (style stays templated)
    and is not consumed by styled_chart.
    """
    root = ET.fromstring(chart_xml)
    series, categories = [], None
    for ser in _iter_chart_series(root):
        if categories is None:
            categories = _cache_values(ser.find(_ct("cat")), numeric=False)
        series.append({
            "name": _series_name(ser),
            "values": _cache_values(ser.find(_ct("val")), numeric=True) or [],
            "color": _series_color(ser),
        })
    value_axis_max = None
    for axis in root.findall(".//" + _ct("valAx")):
        mx = axis.find(_ct("scaling") + "/" + _ct("max"))
        if mx is not None:
            value_axis_max = float(mx.get("val"))
            break
    gap = root.find(".//" + _ct("gapWidth"))
    overlap = root.find(".//" + _ct("overlap"))
    chart = root.find(_ct("chart"))
    plot = chart.find(_ct("plotArea")) if chart is not None else None
    types = []
    for container in (list(plot) if plot is not None else []):
        tag = container.tag.split("}")[-1]
        if tag.endswith("Chart"):
            grouping = container.find(_ct("grouping"))
            types.append({
                "type": tag,
                "grouping": grouping.get("val") if grouping is not None else None,
                "n_ser": len(container.findall(_ct("ser"))),
            })
    return {"categories": categories, "series": series,
            "value_axis_max": value_axis_max,
            "gap_width": int(gap.get("val")) if gap is not None else None,
            "overlap": int(overlap.get("val")) if overlap is not None else None,
            "types": types}


def _fmt_cache_num(v) -> str:
    """Shortest faithful text for a numeric cache value (42.0 -> '42')."""
    f = float(v)
    return str(int(f)) if f.is_integer() else repr(f)


def _set_cache(node, values, *, numeric):
    """Replace a cache's <c:pt> list (and ptCount) from `values`; blanks (None)
    are dropped, matching PowerPoint's gap encoding. formatCode/ptCount keep
    their leading position and the new pts append after — preserving the
    formatCode?, ptCount, pt* schema order."""
    pc = node.find(_ct("ptCount"))
    if pc is None:
        pc = ET.SubElement(node, _ct("ptCount"))
    pc.set("val", str(len(values)))
    for pt in node.findall(_ct("pt")):
        node.remove(pt)
    for idx, v in enumerate(values):
        if numeric:
            if v is None:
                continue
            text = _fmt_cache_num(v)
        else:
            if v is None or v == "":
                continue
            text = str(v)
        pt = ET.SubElement(node, _ct("pt"))
        pt.set("idx", str(idx))
        ET.SubElement(pt, _ct("v")).text = text


def _rewrite_chart_caches(template_xml: str, data: dict) -> str:
    """Return template_xml with its data caches rewritten from `data` — values
    per series, plus categories / series names where both the template carries
    that cache and `data` supplies the field. Everything else (the style) is
    left byte-for-byte. Raises if `data`'s series count != the template's."""
    root = ET.fromstring(template_xml)
    sers = list(_iter_chart_series(root))
    dseries = data.get("series", [])
    if len(dseries) != len(sers):
        raise ValueError(
            f"data has {len(dseries)} series but the chart template has "
            f"{len(sers)}; styled_chart needs one data series per template series")
    categories = data.get("categories")
    for ser, dser in zip(sers, dseries):
        vnode = _cache_node(ser.find(_ct("val")))
        if vnode is not None and "values" in dser:
            _set_cache(vnode, dser["values"], numeric=True)
        if categories:
            cnode = _cache_node(ser.find(_ct("cat")))
            if cnode is not None:
                _set_cache(cnode, categories, numeric=False)
        if dser.get("name") is not None:
            tnode = _cache_node(ser.find(_ct("tx")))
            if tnode is not None:
                _set_cache(tnode, [dser["name"]], numeric=False)
    return _XML_DECL + "\n" + ET.tostring(root, encoding="unicode")


def styled_chart(template_xml: str, data: dict, embed_bytes: bytes, *,
                 embed_ext: str = "xlsb") -> dict:
    """Data-over-template chart: keep `template_xml` as the exact style template
    and rewrite its data caches from `data`, so the values live in Python while
    the rendered look stays identical to the source chart.

    The companion to editable_bundled_chart: bundling keeps the data opaque
    (cache + workbook only); styled_chart surfaces it as a `data` literal
    (see extract_chart_data for the shape) yet still reattaches `embed_bytes`
    as the editable workbook, so "Edit Data" works. Type-agnostic — it never
    interprets the chart, only its caches — so it reproduces combos (bar+line)
    and exotic styling that a factory (column_chart/…) cannot.

    Args:
        template_xml: the source chart part, used verbatim as the style template
            (its caches are overwritten; all other bytes are preserved).
        data: categories + per-series values to write in (extract_chart_data's
            output, or a hand-authored dict of the same shape).
        embed_bytes: the source workbook to reattach (the chart's .xlsb/.xlsx).
        embed_ext: "xlsb" (default, reuse the binary source) or "xlsx".

    Returns the CHARTS dict the build loop wires into the package (same shape as
    editable_bundled_chart). For a faithful re-port `data` equals the cached
    values, so the result renders byte-for-byte like the bundled chart.

    Note: the reattached workbook is the source's; if `data` is edited to differ
    from it, the chart re-renders from the rewritten caches but PowerPoint's
    "Edit Data" pane shows the original workbook until it is regenerated.
    """
    rewritten = _rewrite_chart_caches(template_xml, data)
    return editable_bundled_chart(rewritten, embed_bytes, embed_ext=embed_ext)


def _is_blank(v) -> bool:
    """True if v should be treated as an empty cell (None or NaN)."""
    if v is None:
        return True
    # NaN check: float NaN != itself
    try:
        return v != v  # noqa: PLR0124
    except Exception:
        return False


def _col_letter(idx: int) -> str:
    """Map a 0-based column index to an Excel column letter. 0 -> A, 25 -> Z,
    26 -> AA (supports wide multi-series charts, e.g. waterfall / marimekko)."""
    if idx < 0:
        raise ValueError(f"negative column index: {idx}")
    n = idx + 1
    out: list[str] = []
    while n:
        n, rem = divmod(n - 1, 26)
        out.append(chr(ord("A") + rem))
    return "".join(reversed(out))


def _build_sheet1(
    *,
    categories: list[str],
    series_names: list[str],
    series_values: list[list],
    cat_header: str = "Category",
) -> str:
    """Build xl/worksheets/sheet1.xml for the embedded workbook.

    Layout:
        Column A:        category labels (inline strings)
        Columns B / C /…: per-series values, one column per series
        Row 1:           header row (cat_header in A; series names in B+)
        Rows 2 onward:   one row per category

    None / NaN values render as empty cells in the sheet (which the chart
    cache also omits, matching PowerPoint's "blank = gap" behavior).
    """
    rows: list[str] = []

    # Row 1: header.
    header_cells = [
        f'<c r="A1" t="inlineStr"><is><t>{_esc(cat_header)}</t></is></c>'
    ]
    for s_idx, name in enumerate(series_names):
        col = _col_letter(s_idx + 1)  # column B onward
        header_cells.append(
            f'<c r="{col}1" t="inlineStr"><is><t>{_esc(name)}</t></is></c>'
        )
    rows.append(f'<row r="1">{"".join(header_cells)}</row>')

    # Rows 2 onward: one per category.
    for i, cat in enumerate(categories):
        r = i + 2
        cells = [
            f'<c r="A{r}" t="inlineStr"><is><t>{_esc(str(cat))}</t></is></c>'
        ]
        for s_idx, values in enumerate(series_values):
            col = _col_letter(s_idx + 1)
            v = values[i]
            if _is_blank(v):
                cells.append(f'<c r="{col}{r}"/>')
            else:
                cells.append(f'<c r="{col}{r}"><v>{v}</v></c>')
        rows.append(f'<row r="{r}">{"".join(cells)}</row>')

    return (
        f'{_XML_DECL}\n'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetData>'
        + "".join(rows) +
        '</sheetData>'
        '</worksheet>'
    )


def _build_embed_xlsx(
    *,
    categories: list[str],
    series: list[dict],
    cat_header: str = "Category",
) -> bytes:
    """Build a complete embedded .xlsx as bytes.

    Six OOXML files in a deflated zip. Five are constants; sheet1.xml is
    built per-chart from the categories + series passed in.
    """
    series_names = [
        s.get("name", f"Series {i + 1}") for i, s in enumerate(series)
    ]
    series_values = [s["values"] for s in series]
    sheet1_xml = _build_sheet1(
        categories=categories,
        series_names=series_names,
        series_values=series_values,
        cat_header=cat_header,
    )

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", _EMBED_CONTENT_TYPES)
        zf.writestr("_rels/.rels", _EMBED_ROOT_RELS)
        zf.writestr("xl/workbook.xml", _EMBED_WORKBOOK)
        zf.writestr("xl/_rels/workbook.xml.rels", _EMBED_WORKBOOK_RELS)
        zf.writestr("xl/styles.xml", _EMBED_STYLES)
        zf.writestr("xl/worksheets/sheet1.xml", sheet1_xml)
    return buf.getvalue()


def _bars(
    *,
    categories: list[str],
    series: list[dict],
    horizontal: bool = True,
    grouping: str = "clustered",
    title: str | None = None,
    title_color: str = "000000",
    title_size_pt: int = 10,
    title_bold: bool = False,
    title_italic: bool = True,
    show_legend: bool = False,
    legend_pos: str = "b",
    value_axis_format: str = "General",
    show_gridlines: bool = False,
    major_gridline_color: str | None = None,
    major_gridline_width: int | None = None,
    show_value_labels: bool = True,
    show_cat_labels: bool = True,
    value_label_format: str | None = None,
    value_label_size_pt: int = 9,
    value_label_bold: bool = True,
    cat_label_size_pt: int = 9,
    cat_label_bold: bool = False,
    gap_width: int = 75,
    bar_overlap: int = -27,
    plot_area_fill: str | None = None,
    embed_data: bool = True,
    sheet_name: str = "Sheet1",
    cat_header: str = "Category",
    seg_line_color: str | None = "000000",
    seg_line_width: int = 6350,
    axis_line_color: str | None = None,
    axis_line_width: int = 9525,
    value_axis_min: float | None = None,
    value_axis_max: float | None = None,
    value_axis_major_unit: float | None = None,
    show_value_axis_labels: bool = True,
    plot_layout: dict | None = None,
) -> dict:
    """Private bar/column engine behind column_chart() / bar_chart() and the
    waterfall / marimekko factories. Call those public faces, not this directly.

    Returns a dict with three keys:
        chart_xml:  str — body of ppt/charts/chartN.xml
        embed_xlsx: bytes | None — complete .xlsx zip (None when embed_data=False)
        chart_rels: str | None — body of chartN.xml.rels with {chart_num}
                                  placeholder (None when embed_data=False)

    Args:
        categories: list of category-axis labels (one per data point per series)
        series: list of dicts. Each dict:
            - name (str): series name
            - values (list[float | None]): one value per category; None = blank
            - color (str, optional): single hex color (RRGGBB) for the whole series
            - data_point_colors (list[str], optional): per-bar hex colors
              (overrides 'color' if present). Must match len(categories).
            - no_fill (bool, optional): render the series transparent (a
              spacer/offset series for floating/range bars).
            - line (dict, optional): explicit whole-series outline —
              {"color": hex (default 000000), "width": EMU (default 6350),
              "dash": a:prstDash preset ("dash", "sysDot", "lgDash", ...;
              omit for solid)}. Overrides the chart-level seg_line_color for
              this series only. With no_fill it draws an OUTLINED EMPTY box
              (the think-cell "remainder of the denominator" frame: filled
              bar below, dashed/dotted open extension above).
            - pattern (dict, optional): whole-series a:pattFill instead of a
              solid fill — {"prst": preset (default "ltUpDiag"), "fg": line
              hex (default 000000), "bg": ground hex (default FFFFFF)}. The
              think-cell hatch for an "estimate" or "additive" segment.
              Ignored when no_fill is set; data_point_colors still override
              per point.
            - hide_labels (bool, optional): suppress this series' data labels.
              Two uses: a no_fill spacer series (below), or a segment too thin to
              hold its in-bar label — drop the native label and overlay a colored
              "chip" instead.
            - label_color (str, optional): explicit hex for ALL of this series'
              data labels. Omit to auto-pick: inside-bar labels (stacked /
              percent / waterfall / marimekko) flip to white on a dark fill and
              stay dark otherwise, so labels never vanish into a dark column.
            - label_colors (list[str], optional): per-point label hex, one per
              category (overrides label_color + auto). Must match len(categories).
        horizontal: True = horizontal bars (bar), False = vertical columns (col)
        grouping: "clustered" (default, side-by-side), "stacked", or
            "percentStacked". Stacked grouping forces overlap=100 and centers
            data labels (dLblPos="ctr"; "outEnd" is invalid on stacked charts and
            makes PowerPoint repair the file). For a floating / range ("dumbbell")
            bar, stack an invisible spacer series (series dict with
            "no_fill": True, "hide_labels": True) under a visible range series.
        title: optional chart title. If None, no title element emitted.
        title_color: hex color for the title text
        title_size_pt: title font size in points (will be * 100 for c: size attr)
        title_bold: bold the native title (default off — house style is light)
        title_italic: italicize the native title (default on — 10pt Arial italic).
            House preference is no native title at all: place a no-fill
            CHART_TITLE_10PT text_box above the chart frame instead.
        show_legend: whether to render legend (only useful with multiple series)
        legend_pos: "b" / "t" / "l" / "r" / "tr"
        value_axis_format: number format code for value axis (e.g. "$#,##0\"B\"")
        show_gridlines: render major-gridlines on the value axis
        major_gridline_color: optional hex color for major gridlines.
            Pair with major_gridline_width for a quiet banker-style
            gridline (default 0.25pt / BFBFBF when either is set).
        major_gridline_width: optional gridline width in EMU
            (e.g. 3_175 for 0.25pt).
        show_value_labels: render data-value labels on each bar
        value_label_format: optional override for label number format
        value_label_size_pt: data-label font size in points
        value_label_bold: bold the data-value labels (default True — historic
            behavior). Set False for the think-cell look, where in-bar segment
            labels and floated totals share one regular weight and read apart by
            position, not boldness.
        cat_label_size_pt: category-axis label font size in points
        cat_label_bold: bold the category-axis tick labels (default False —
            byte-identical to before this param existed; the value axis is
            unaffected).
        gap_width: % gap between bar groups (0-500). Smaller = thicker bars.
        bar_overlap: % bar overlap within a group (-100 to 100).
        plot_area_fill: optional hex color for the plot area background
        embed_data: True (default) emits c:strRef/c:numRef + cache + externalData
            and returns a real embedded xlsx; False emits c:strLit/c:numLit
            inline data (Edit Data disabled in PowerPoint)
        sheet_name: name of the inner workbook's sheet. Must be "Sheet1"
            (enforced — raises otherwise): the embedded workbook hard-codes that
            sheet and the chart-cell formulas reference it by name.
        show_cat_labels: render category-axis tick labels. False hides them
            (tickLblPos="none") without shrinking the legend — used by
            marimekko, where column labels are overlaid as slide text instead.
        cat_header: header label for column A in the embedded sheet
            (cosmetic — only visible if the user opens Edit Data)
        seg_line_color: hex color for the per-bar/per-segment outline
            (default "000000" — the historical 0.5pt black border). Set to
            "FFFFFF" for the think-cell look (white dividers between stacked
            segments).
        seg_line_width: bar/segment outline width in EMU (default 6350 =
            0.5pt; use 9525 = 0.75pt for the think-cell divider weight).
        axis_line_color: optional hex for an explicit cat+val axis line. When
            None (default) the axes keep PowerPoint's default spine; set e.g.
            "162029" (theme tx1) for the think-cell dark-navy axis.
        axis_line_width: axis-line width in EMU when axis_line_color is set
            (default 9525 = 0.75pt).
        value_axis_min: optional fixed value-axis minimum (else auto-scaled).
        value_axis_max: optional fixed value-axis maximum (else auto-scaled).
        value_axis_major_unit: optional fixed spacing between value-axis ticks
            (e.g. a 0-100 axis with major_unit=5 gives a tick every 5%). All
            three default None -> emit nothing (PowerPoint auto-scales), so
            existing charts stay byte-identical.
        show_value_axis_labels: render value-axis tick labels + tick marks.
            False sets tickLblPos="none" / majorTickMark="none" but keeps the
            axis present (delete=0) so min/max/major_unit scaling still holds —
            used when every bar is annotated directly and the scale row would
            be noise (the think-cell walk look).
        plot_layout: optional dict {"x","y","w","h"} of fractions (0-1) of the
            chart frame, pinning the INNER plot rectangle (the data-drawing area,
            excluding axis labels) via a manualLayout — use to place the plot/bars
            exactly (e.g. to match a transcribed exhibit). None (default) emits
            the bare <c:layout/> auto layout, byte-identical to before.
    """
    if sheet_name != "Sheet1":
        raise ValueError(
            "sheet_name must be 'Sheet1': the embedded workbook hard-codes that "
            "sheet name, so any other value breaks the chart's Edit Data link")
    bar_dir = "bar" if horizontal else "col"
    cat_axis_pos = "l" if horizontal else "b"
    val_axis_pos = "b" if horizontal else "l"

    if grouping not in ("clustered", "stacked", "percentStacked"):
        grouping = "clustered"
    is_stacked = grouping in ("stacked", "percentStacked")
    # Stacked bars MUST overlap fully; clustered keeps the caller's overlap.
    effective_overlap = 100 if is_stacked else bar_overlap
    # "outEnd" is illegal on stacked series (PowerPoint repairs the file).
    dlbl_pos = "ctr" if is_stacked else "outEnd"
    # Horizontal bars read top-to-bottom in category order (ranked look) only
    # when the category axis runs maxMin; vertical columns stay minMax.
    cat_orientation = "maxMin" if horizontal else "minMax"

    cat_count = len(categories)
    for s in series:
        if len(s["values"]) != cat_count:
            raise ValueError(
                f"Series '{s.get('name', '?')}' has {len(s['values'])} values "
                f"but {cat_count} categories"
            )

    # Stable axis IDs (any ints — must be referenced from both <c:catAx> and
    # <c:valAx> and from the barChart's two <c:axId> entries).
    CAT_AX_ID = 111_111_111
    VAL_AX_ID = 222_222_222

    # ── Title ────────────────────────────────────────────────────────
    if title:
        title_size = title_size_pt * 100
        title_b = "1" if title_bold else "0"
        title_i = "1" if title_italic else "0"
        title_xml = (
            "<c:title>"
            "<c:tx><c:rich>"
            '<a:bodyPr rot="0" spcFirstLastPara="1" vertOverflow="ellipsis" '
            'wrap="square" anchor="ctr" anchorCtr="1"/>'
            "<a:lstStyle/>"
            '<a:p><a:pPr algn="ctr">'
            f'<a:defRPr sz="{title_size}" b="{title_b}" i="{title_i}">'
            f'<a:solidFill><a:srgbClr val="{title_color}"/></a:solidFill>'
            '<a:latin typeface="Arial"/><a:ea typeface="Arial"/>'
            '<a:cs typeface="Arial"/>'
            '</a:defRPr></a:pPr>'
            f'<a:r><a:rPr lang="en-US" sz="{title_size}" b="{title_b}" i="{title_i}">'
            f'<a:solidFill><a:srgbClr val="{title_color}"/></a:solidFill>'
            '<a:latin typeface="Arial"/><a:ea typeface="Arial"/>'
            '<a:cs typeface="Arial"/>'
            f'</a:rPr><a:t>{_esc(title)}</a:t></a:r></a:p>'
            "</c:rich></c:tx>"
            '<c:overlay val="0"/>'
            "</c:title>"
            '<c:autoTitleDeleted val="0"/>'
        )
    else:
        title_xml = '<c:autoTitleDeleted val="1"/>'

    # ── Series ───────────────────────────────────────────────────────
    ser_xml_parts: list[str] = []
    for s_idx, s in enumerate(series):
        ser_xml_parts.append(_build_series(
            s_idx=s_idx,
            categories=categories,
            series=s,
            show_value_labels=show_value_labels,
            value_label_format=value_label_format or value_axis_format,
            value_label_size_pt=value_label_size_pt,
            value_label_bold=value_label_bold,
            embed_data=embed_data,
            sheet_name=sheet_name,
            dlbl_pos=dlbl_pos,
            seg_line_color=seg_line_color,
            seg_line_width=seg_line_width,
        ))

    # ── Bar chart body ───────────────────────────────────────────────
    bar_chart_xml = (
        "<c:barChart>"
        f'<c:barDir val="{bar_dir}"/>'
        f'<c:grouping val="{grouping}"/>'
        '<c:varyColors val="0"/>'
        + "".join(ser_xml_parts)
        + f'<c:gapWidth val="{gap_width}"/>'
        + f'<c:overlap val="{effective_overlap}"/>'
        + f'<c:axId val="{CAT_AX_ID}"/>'
        + f'<c:axId val="{VAL_AX_ID}"/>'
        + "</c:barChart>"
    )

    # ── Category axis ────────────────────────────────────────────────
    axis_label_rot = "0"

    # Optional explicit axis line (think-cell dark-navy spine). Goes in the
    # CT_CatAx / CT_ValAx <c:spPr> slot — after <c:tickLblPos> and before
    # <c:txPr> — or PowerPoint repairs the file.
    if axis_line_color:
        axis_ln_spPr = (
            "<c:spPr>"
            f'<a:ln w="{axis_line_width}" cap="flat">'
            f'<a:solidFill><a:srgbClr val="{axis_line_color}"/></a:solidFill>'
            '<a:prstDash val="solid"/>'
            "</a:ln>"
            "</c:spPr>"
        )
    else:
        axis_ln_spPr = ""

    cat_label_size = cat_label_size_pt * 100
    cat_ax_xml = (
        "<c:catAx>"
        f'<c:axId val="{CAT_AX_ID}"/>'
        f'<c:scaling><c:orientation val="{cat_orientation}"/></c:scaling>'
        '<c:delete val="0"/>'
        f'<c:axPos val="{cat_axis_pos}"/>'
        '<c:numFmt formatCode="General" sourceLinked="1"/>'
        # Hidden cat labels (marimekko) also drop the tick marks, else a tick
        # prints per bin; a normal chart keeps "out".
        f'<c:majorTickMark val="{"out" if show_cat_labels else "none"}"/>'
        '<c:minorTickMark val="none"/>'
        f'<c:tickLblPos val="{"nextTo" if show_cat_labels else "none"}"/>'
        + axis_ln_spPr +
        "<c:txPr>"
        f'<a:bodyPr rot="{axis_label_rot}" spcFirstLastPara="1" vertOverflow="ellipsis" '
        'wrap="square" anchor="ctr" anchorCtr="1"/>'
        "<a:lstStyle/>"
        "<a:p><a:pPr>"
        f'<a:defRPr sz="{cat_label_size}" b="{1 if cat_label_bold else 0}">'
        '<a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:ea typeface="Arial"/>'
        '<a:cs typeface="Arial"/>'
        "</a:defRPr></a:pPr>"
        '<a:endParaRPr lang="en-US"/></a:p>'
        "</c:txPr>"
        f'<c:crossAx val="{VAL_AX_ID}"/>'
        '<c:crosses val="autoZero"/>'
        '<c:auto val="1"/>'
        '<c:lblAlgn val="ctr"/>'
        '<c:lblOffset val="100"/>'
        '<c:noMultiLvlLbl val="0"/>'
        "</c:catAx>"
    )

    # ── Value axis ───────────────────────────────────────────────────
    # Major gridlines. When a color or width is given, emit a quiet,
    # banker-style styled gridline (default 0.25pt BFBFBF); otherwise fall back
    # to PowerPoint's default.
    if show_gridlines:
        if major_gridline_color or major_gridline_width:
            _gl_w = major_gridline_width if major_gridline_width is not None else 3_175
            _gl_color = major_gridline_color or "BFBFBF"
            gridlines_xml = (
                "<c:majorGridlines>"
                "<c:spPr>"
                f'<a:ln w="{_gl_w}" cap="flat">'
                f'<a:solidFill><a:srgbClr val="{_gl_color}"/></a:solidFill>'
                '<a:prstDash val="solid"/>'
                "</a:ln>"
                "</c:spPr>"
                "</c:majorGridlines>"
            )
        else:
            gridlines_xml = "<c:majorGridlines/>"
    else:
        gridlines_xml = ""
    # Optional fixed value-axis range + tick spacing (e.g. a 0-100% axis in 5%
    # steps). When all None, emit the historical bare scaling / no majorUnit so
    # existing charts are byte-identical. CT_Scaling order is orientation,max,min.
    def _axnum(v: float) -> str:
        return str(int(v)) if float(v).is_integer() else repr(float(v))
    val_scaling = "<c:scaling><c:orientation val=\"minMax\"/>"
    if value_axis_max is not None:
        val_scaling += f'<c:max val="{_axnum(value_axis_max)}"/>'
    if value_axis_min is not None:
        val_scaling += f'<c:min val="{_axnum(value_axis_min)}"/>'
    val_scaling += "</c:scaling>"
    val_major_unit = (
        f'<c:majorUnit val="{_axnum(value_axis_major_unit)}"/>'
        if value_axis_major_unit is not None else ""
    )
    val_ax_xml = (
        "<c:valAx>"
        f'<c:axId val="{VAL_AX_ID}"/>'
        + val_scaling +
        '<c:delete val="0"/>'
        f'<c:axPos val="{val_axis_pos}"/>'
        + gridlines_xml +
        f'<c:numFmt formatCode="{_esc_attr(value_axis_format)}" sourceLinked="0"/>'
        f'<c:majorTickMark val="{"out" if show_value_axis_labels else "none"}"/>'
        '<c:minorTickMark val="none"/>'
        f'<c:tickLblPos val="{"nextTo" if show_value_axis_labels else "none"}"/>'
        + axis_ln_spPr +
        "<c:txPr>"
        f'<a:bodyPr rot="{axis_label_rot}" spcFirstLastPara="1" vertOverflow="ellipsis" '
        'wrap="square" anchor="ctr" anchorCtr="1"/>'
        "<a:lstStyle/>"
        "<a:p><a:pPr>"
        f'<a:defRPr sz="{cat_label_size}" b="0">'
        '<a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:ea typeface="Arial"/>'
        '<a:cs typeface="Arial"/>'
        "</a:defRPr></a:pPr>"
        '<a:endParaRPr lang="en-US"/></a:p>'
        "</c:txPr>"
        f'<c:crossAx val="{CAT_AX_ID}"/>'
        '<c:crosses val="autoZero"/>'
        '<c:crossBetween val="between"/>'
        + val_major_unit +
        "</c:valAx>"
    )

    # ── Plot area ────────────────────────────────────────────────────
    if plot_area_fill:
        plot_spPr = (
            "<c:spPr>"
            f'<a:solidFill><a:srgbClr val="{plot_area_fill}"/></a:solidFill>'
            '<a:ln><a:noFill/></a:ln>'
            "</c:spPr>"
        )
    else:
        plot_spPr = ""
    if plot_layout:
        layout_xml = (
            "<c:layout><c:manualLayout>"
            '<c:layoutTarget val="inner"/>'
            '<c:xMode val="edge"/><c:yMode val="edge"/>'
            f'<c:x val="{repr(float(plot_layout["x"]))}"/>'
            f'<c:y val="{repr(float(plot_layout["y"]))}"/>'
            f'<c:w val="{repr(float(plot_layout["w"]))}"/>'
            f'<c:h val="{repr(float(plot_layout["h"]))}"/>'
            "</c:manualLayout></c:layout>"
        )
    else:
        layout_xml = "<c:layout/>"
    plot_area_xml = (
        "<c:plotArea>"
        + layout_xml
        + bar_chart_xml + cat_ax_xml + val_ax_xml + plot_spPr +
        "</c:plotArea>"
    )

    # ── Legend ───────────────────────────────────────────────────────
    if show_legend:
        legend_xml = (
            "<c:legend>"
            f'<c:legendPos val="{legend_pos}"/>'
            '<c:overlay val="0"/>'
            "<c:txPr>"
            '<a:bodyPr rot="0" spcFirstLastPara="1" vertOverflow="ellipsis" '
            'wrap="square" anchor="ctr" anchorCtr="1"/>'
            "<a:lstStyle/>"
            "<a:p><a:pPr>"
            f'<a:defRPr sz="{cat_label_size}" b="0">'
            '<a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
            '<a:latin typeface="Arial"/><a:ea typeface="Arial"/>'
            '<a:cs typeface="Arial"/>'
            "</a:defRPr></a:pPr>"
            '<a:endParaRPr lang="en-US"/></a:p>'
            "</c:txPr>"
            "</c:legend>"
        )
    else:
        legend_xml = ""

    # ── External-data declaration (only when embed_data=True) ────────
    # MUST go after </c:chart> but before </c:chartSpace> (cheat sheet §27
    # gotcha: element order inside chartSpace matters).
    if embed_data:
        external_data_xml = (
            '<c:externalData r:id="rId1">'
            '<c:autoUpdate val="0"/>'
            '</c:externalData>'
        )
    else:
        external_data_xml = ""

    # ── Assemble full chart ──────────────────────────────────────────
    chart_xml = (
        f'{_XML_DECL}\n'
        f'<c:chartSpace {_NS}>'
        '<c:lang val="en-US"/>'
        '<c:roundedCorners val="0"/>'
        '<c:chart>'
        + title_xml
        + plot_area_xml
        + legend_xml
        + '<c:plotVisOnly val="1"/>'
        + '<c:dispBlanksAs val="gap"/>'
        + '</c:chart>'
        + external_data_xml
        + '</c:chartSpace>'
    )

    # ── Embedded workbook + chart rels (only when embed_data=True) ───
    if embed_data:
        embed_xlsx = _build_embed_xlsx(
            categories=categories,
            series=series,
            cat_header=cat_header,
        )
        chart_rels = _CHART_RELS_TEMPLATE
    else:
        embed_xlsx = None
        chart_rels = None

    return {
        "chart_xml": chart_xml,
        "embed_xlsx": embed_xlsx,
        "chart_rels": chart_rels,
    }


# ── Public bar / column API (thin faces over _bars) ──────────────────────
# Mode = how series (or a single ranked series) combine into each bar.
_MODE_TO_GROUPING = {
    "clustered": "clustered",      # side-by-side; also a plain single series
    "ranked": "clustered",         # alias: one pre-sorted series (+ data_point_colors)
    "stacked": "stacked",          # segments stack to each bar's raw total
    "percent": "percentStacked",   # segments stack to 100%
}


def column_chart(*, mode: str = "clustered", **kwargs) -> dict:
    """Vertical-column chart. mode: clustered | stacked | percent | ranked
    ("ranked" = one pre-sorted series, often with a data_point_colors list for
    top-N emphasis; "stacked" = bars sum to their raw total; "percent" = to
    100%). All other kwargs forward to _bars (categories, series, title,
    show_legend, value_axis_format, show_value_labels, gridlines, gap_width,
    ...). Returns the standard {chart_xml, embed_xlsx, chart_rels} dict."""
    if mode not in _MODE_TO_GROUPING:
        raise ValueError(f"unknown mode {mode!r}; pick {list(_MODE_TO_GROUPING)}")
    return _bars(horizontal=False, grouping=_MODE_TO_GROUPING[mode], **kwargs)


def bar_chart(*, mode: str = "clustered", **kwargs) -> dict:
    """Horizontal-bar chart. Categories read top-to-bottom, so a single series
    is a ranked bar with no extra work. mode + kwargs are identical to
    column_chart; see _bars for the full styling parameter list."""
    if mode not in _MODE_TO_GROUPING:
        raise ValueError(f"unknown mode {mode!r}; pick {list(_MODE_TO_GROUPING)}")
    return _bars(horizontal=True, grouping=_MODE_TO_GROUPING[mode], **kwargs)


# Static-think-cell look in one spread: white 0.75pt segment dividers, dark-navy
# (tx1) axis, 8pt labels, no native legend or gridlines. Use as
# column_chart(mode=..., categories=..., series=..., **THINKCELL_BARS,
# value_axis_format=..., gap_width=...). Override a key with
# {**THINKCELL_BARS, "show_gridlines": True}. Pair series colors with
# deck_core.style.chart_accent_seq(n) and replace the dropped legend with
# deck_core.chart_key.chart_key(...).
THINKCELL_BARS = {
    "seg_line_color": "FFFFFF",    # bg1 white divider between segments
    "seg_line_width": 9525,        # 0.75pt
    "axis_line_color": "162029",   # tx1 dark-navy cat + val axis line
    "show_gridlines": False,
    "show_legend": False,
    "value_label_size_pt": 8,
    "cat_label_size_pt": 8,
}


def _build_series(
    *,
    s_idx: int,
    categories: list[str],
    series: dict,
    show_value_labels: bool,
    value_label_format: str,
    value_label_size_pt: int,
    value_label_bold: bool = True,
    embed_data: bool,
    sheet_name: str,
    dlbl_pos: str = "outEnd",
    seg_line_color: str | None = "000000",
    seg_line_width: int = 6350,
) -> str:
    name = series.get("name", f"Series {s_idx + 1}")
    values = series["values"]
    series_color = series.get("color")
    data_point_colors = series.get("data_point_colors")
    no_fill = series.get("no_fill", False)
    # pattern: whole-series a:pattFill (e.g. the hatched "estimate"/"additive"
    # segment of a think-cell walk). Dict keys: prst (preset name, default
    # ltUpDiag), fg (line color, default 000000), bg (ground, default FFFFFF).
    pattern = series.get("pattern")
    # hide_label_points: per-point label suppression (one or more category
    # indices). Use for a segment too thin to hold its in-bar label — drop the
    # native label here and overlay a colored "chip" instead (think-cell look;
    # see the chip recipe in the consolidated/MRO stacked-column slides). Differs
    # from hide_labels (whole series) — this removes only the listed points.
    hide_label_points = set(series.get("hide_label_points") or ())
    hide_labels = series.get("hide_labels", False)
    # line: explicit per-series outline override ({"color","width","dash"}).
    # Replaces the chart-level seg_line_color outline for this series; with
    # no_fill it yields an outlined empty box (denominator-remainder frame).
    line = series.get("line")
    # label_color: explicit series-level override; label_colors: explicit
    # per-point overrides. When neither is set, the label color is derived per
    # point from the bar fill + label position (see the data-label block below).
    label_color = series.get("label_color")
    label_colors = series.get("label_colors")

    n_cats = len(categories)
    val_col = _col_letter(s_idx + 1)   # column B for series 0, C for series 1, ...
    last_row = n_cats + 1              # row 1 is header; data spans rows 2..n_cats+1

    # ── Series name (c:tx) ───────────────────────────────────────────
    if embed_data:
        # Real cell reference into the embedded workbook header row.
        tx_xml = (
            "<c:tx><c:strRef>"
            f"<c:f>{sheet_name}!${val_col}$1</c:f>"
            '<c:strCache><c:ptCount val="1"/>'
            f'<c:pt idx="0"><c:v>{_esc(name)}</c:v></c:pt>'
            "</c:strCache>"
            "</c:strRef></c:tx>"
        )
    else:
        # Fake formula — Edit Data won't open. Legacy behavior.
        tx_xml = (
            "<c:tx><c:strRef>"
            f"<c:f>Series{s_idx + 1}</c:f>"
            '<c:strCache><c:ptCount val="1"/>'
            f'<c:pt idx="0"><c:v>{_esc(name)}</c:v></c:pt>'
            "</c:strCache>"
            "</c:strRef></c:tx>"
        )

    # Per-bar/segment outline (default 0.5pt black — byte-identical to the
    # historical hardcoded border; "FFFFFF" + 9525 gives the think-cell white
    # 0.75pt divider). Reused for the series fill and any per-point c:dPt fills
    # so every rect carries the same border. No cap attr: it's a closed
    # rectangle outline, so cap is irrelevant and omitting it keeps the default
    # output identical to before this param existed.
    # seg_line_color=None -> an explicit no-fill outline, so adjacent bars/bins
    # abut seamlessly (used by the marimekko, whose thin bins must not show
    # per-bin divider lines; column/segment dividers are overlaid instead).
    if seg_line_color is None:
        seg_ln = "<a:ln><a:noFill/></a:ln>"
    else:
        seg_ln = (
            f'<a:ln w="{seg_line_width}">'
            f'<a:solidFill><a:srgbClr val="{seg_line_color}"/></a:solidFill>'
            "</a:ln>"
        )
    # Per-series outline override (the `line` option). prstDash follows the
    # fill child per CT_LineProperties order.
    if line is not None:
        dash = f'<a:prstDash val="{line["dash"]}"/>' if line.get("dash") else ""
        seg_ln = (
            f'<a:ln w="{line.get("width", 6350)}">'
            f'<a:solidFill><a:srgbClr val="{line.get("color", "000000")}"/></a:solidFill>'
            f"{dash}</a:ln>"
        )

    # Whole-series default color/border. If data_point_colors is given,
    # per-point c:dPt entries override this. A no_fill series is the
    # transparent spacer for floating / range ("dumbbell") bars — unless an
    # explicit `line` is given, which keeps the outline visible on the empty box.
    if no_fill:
        ser_spPr = (
            "<c:spPr>"
            "<a:noFill/>"
            + (seg_ln if line is not None else "<a:ln><a:noFill/></a:ln>") +
            "</c:spPr>"
        )
    elif pattern:
        ser_spPr = (
            "<c:spPr>"
            f'<a:pattFill prst="{pattern.get("prst", "ltUpDiag")}">'
            f'<a:fgClr><a:srgbClr val="{pattern.get("fg", "000000")}"/></a:fgClr>'
            f'<a:bgClr><a:srgbClr val="{pattern.get("bg", "FFFFFF")}"/></a:bgClr>'
            "</a:pattFill>"
            + seg_ln +
            "</c:spPr>"
        )
    elif series_color:
        ser_spPr = (
            "<c:spPr>"
            f'<a:solidFill><a:srgbClr val="{series_color}"/></a:solidFill>'
            + seg_ln +
            "</c:spPr>"
        )
    else:
        ser_spPr = ""

    # Per-data-point colors (override series fill on a per-bar basis).
    d_pts_xml = ""
    if data_point_colors and not no_fill:
        if len(data_point_colors) != len(categories):
            raise ValueError(
                f"data_point_colors has {len(data_point_colors)} entries "
                f"but {len(categories)} categories"
            )
        for i, color in enumerate(data_point_colors):
            d_pts_xml += (
                "<c:dPt>"
                f'<c:idx val="{i}"/>'
                '<c:invertIfNegative val="0"/>'
                '<c:bubble3D val="0"/>'
                "<c:spPr>"
                f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
                + seg_ln +
                "</c:spPr>"
                "</c:dPt>"
            )

    # Data labels. A stacked-segment label centers inside the bar; a
    # spacer/hidden series carries none. Inside-bar labels flip to white on a
    # dark fill so they stay readable (the "dark text on a dark bar" bug).
    if show_value_labels and not hide_labels:
        label_size = value_label_size_pt * 100
        inside = dlbl_pos in _INSIDE_DLBL_POS
        if label_colors is not None and len(label_colors) != n_cats:
            raise ValueError(
                f"label_colors has {len(label_colors)} entries "
                f"but {n_cats} categories"
            )

        def _pt_label_color(i: int) -> str:
            # Precedence: explicit per-point -> explicit series -> auto.
            if label_colors is not None:
                return label_colors[i]
            if label_color is not None:
                return label_color
            if inside:
                if data_point_colors:
                    fill_i = data_point_colors[i]
                elif pattern:
                    fill_i = pattern.get("bg", "FFFFFF")  # label sits on the ground color
                else:
                    fill_i = series_color
                return _label_color_on(fill_i)
            return BLACK   # outside the bar: sits on the light plot background

        def _lbl_txpr(color: str) -> str:
            return (
                "<c:txPr>"
                '<a:bodyPr rot="0" spcFirstLastPara="1" vertOverflow="ellipsis" '
                'wrap="square" anchor="ctr" anchorCtr="1"/>'
                "<a:lstStyle/>"
                "<a:p><a:pPr>"
                f'<a:defRPr sz="{label_size}" b="{"1" if value_label_bold else "0"}">'
                f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
                '<a:latin typeface="Arial"/><a:ea typeface="Arial"/>'
                '<a:cs typeface="Arial"/>'
                "</a:defRPr></a:pPr>"
                '<a:endParaRPr lang="en-US"/></a:p>'
                "</c:txPr>"
            )

        _show_flags = (
            '<c:showLegendKey val="0"/>'
            '<c:showVal val="1"/>'
            '<c:showCatName val="0"/>'
            '<c:showSerName val="0"/>'
            '<c:showPercent val="0"/>'
            '<c:showBubbleSize val="0"/>'
        )

        pt_colors = [_pt_label_color(i) for i in range(n_cats)]
        uniform = len(set(pt_colors)) <= 1
        series_lbl_color = pt_colors[0] if (pt_colors and uniform) else (label_color or BLACK)

        # Per-point <c:dLbl> overrides: a deleted label (hide_label_points — a
        # too-thin segment whose label is overlaid as a chip instead) or a color
        # override (when points disagree, e.g. data_point_colors mixing dark +
        # light bars, or a marimekko with mixed segments). CT_DLbls requires these
        # BEFORE the series-level group, in ascending idx order, and each color
        # override must repeat position + show flags or PowerPoint repairs the file.
        per_point_parts = []
        for i in range(n_cats):
            if i in hide_label_points:
                per_point_parts.append(
                    f'<c:dLbl><c:idx val="{i}"/><c:delete val="1"/></c:dLbl>'
                )
            elif not uniform:
                per_point_parts.append(
                    "<c:dLbl>"
                    f'<c:idx val="{i}"/>'
                    + _lbl_txpr(pt_colors[i])
                    + f'<c:dLblPos val="{dlbl_pos}"/>'
                    + _show_flags
                    + "</c:dLbl>"
                )
        per_point_xml = "".join(per_point_parts)

        d_lbls_xml = (
            "<c:dLbls>"
            + per_point_xml
            + _lbl_txpr(series_lbl_color)
            + f'<c:dLblPos val="{dlbl_pos}"/>'
            + _show_flags
            + "</c:dLbls>"
        )
    else:
        d_lbls_xml = ""

    # ── Categories (c:cat) ───────────────────────────────────────────
    if embed_data:
        # Reference to Sheet1 column A; cache holds the same labels for
        # renderers that read the cache before opening the workbook.
        cat_cache_pts = "".join(
            f'<c:pt idx="{i}"><c:v>{_esc(str(c))}</c:v></c:pt>'
            for i, c in enumerate(categories)
        )
        cat_xml = (
            "<c:cat><c:strRef>"
            f"<c:f>{sheet_name}!$A$2:$A${last_row}</c:f>"
            "<c:strCache>"
            f'<c:ptCount val="{n_cats}"/>'
            + cat_cache_pts +
            "</c:strCache>"
            "</c:strRef></c:cat>"
        )
    else:
        # Inline literal.
        cat_pts = "".join(
            f'<c:pt idx="{i}"><c:v>{_esc(str(c))}</c:v></c:pt>'
            for i, c in enumerate(categories)
        )
        cat_xml = (
            "<c:cat><c:strLit>"
            f'<c:ptCount val="{n_cats}"/>'
            + cat_pts +
            "</c:strLit></c:cat>"
        )

    # ── Values (c:val) ───────────────────────────────────────────────
    # Skip <c:pt> entries for blank (None/NaN) values; ptCount stays at
    # n_cats (the total category slot count). Excel reads missing idx
    # entries as gaps under <c:dispBlanksAs val="gap"/>.
    val_cache_pts = "".join(
        f'<c:pt idx="{i}"><c:v>{v}</c:v></c:pt>'
        for i, v in enumerate(values)
        if not _is_blank(v)
    )

    if embed_data:
        val_xml = (
            "<c:val><c:numRef>"
            f"<c:f>{sheet_name}!${val_col}$2:${val_col}${last_row}</c:f>"
            "<c:numCache>"
            f'<c:formatCode>{_esc(value_label_format)}</c:formatCode>'
            f'<c:ptCount val="{n_cats}"/>'
            + val_cache_pts +
            "</c:numCache>"
            "</c:numRef></c:val>"
        )
    else:
        val_xml = (
            "<c:val><c:numLit>"
            f'<c:formatCode>{_esc(value_label_format)}</c:formatCode>'
            f'<c:ptCount val="{n_cats}"/>'
            + val_cache_pts +
            "</c:numLit></c:val>"
        )

    return (
        "<c:ser>"
        f'<c:idx val="{s_idx}"/>'
        f'<c:order val="{s_idx}"/>'
        + tx_xml
        + ser_spPr
        + '<c:invertIfNegative val="0"/>'
        + d_pts_xml
        + d_lbls_xml
        + cat_xml
        + val_xml
        + "</c:ser>"
    )


def _build_line_series(
    *,
    s_idx: int,
    categories: list[str],
    series: dict,
    embed_data: bool,
    sheet_name: str,
    line_width: int,
    marker_symbol: str,
    marker_size: int,
    smooth: bool,
) -> str:
    """One <c:ser> for a line chart (CT_LineSer child order).

    Per-series optional keys (each defaults to the chart-level argument, so
    existing callers are byte-identical): "dash" (a prstDash value, e.g.
    "dash" / "sysDot"; default solid), "marker" (symbol override, "none" to
    suppress), "width" (line width EMU).
    """
    name = series.get("name", f"Series {s_idx + 1}")
    values = series["values"]
    color = series.get("color", "3D5972")
    dash = series.get("dash")
    marker_symbol = series.get("marker", marker_symbol)
    line_width = series.get("width", line_width)

    n_cats = len(categories)
    val_col = _col_letter(s_idx + 1)
    last_row = n_cats + 1

    if embed_data:
        tx_xml = (
            "<c:tx><c:strRef>"
            f"<c:f>{sheet_name}!${val_col}$1</c:f>"
            '<c:strCache><c:ptCount val="1"/>'
            f'<c:pt idx="0"><c:v>{_esc(name)}</c:v></c:pt>'
            "</c:strCache></c:strRef></c:tx>"
        )
        cat_cache_pts = "".join(
            f'<c:pt idx="{i}"><c:v>{_esc(str(c))}</c:v></c:pt>'
            for i, c in enumerate(categories)
        )
        cat_xml = (
            "<c:cat><c:strRef>"
            f"<c:f>{sheet_name}!$A$2:$A${last_row}</c:f>"
            f'<c:strCache><c:ptCount val="{n_cats}"/>{cat_cache_pts}</c:strCache>'
            "</c:strRef></c:cat>"
        )
        val_cache_pts = "".join(
            f'<c:pt idx="{i}"><c:v>{v}</c:v></c:pt>'
            for i, v in enumerate(values) if not _is_blank(v)
        )
        val_xml = (
            "<c:val><c:numRef>"
            f"<c:f>{sheet_name}!${val_col}$2:${val_col}${last_row}</c:f>"
            f'<c:numCache><c:formatCode>General</c:formatCode>'
            f'<c:ptCount val="{n_cats}"/>{val_cache_pts}</c:numCache>'
            "</c:numRef></c:val>"
        )
    else:
        tx_xml = (
            "<c:tx><c:strRef>"
            f"<c:f>Series{s_idx + 1}</c:f>"
            '<c:strCache><c:ptCount val="1"/>'
            f'<c:pt idx="0"><c:v>{_esc(name)}</c:v></c:pt>'
            "</c:strCache></c:strRef></c:tx>"
        )
        cat_pts = "".join(
            f'<c:pt idx="{i}"><c:v>{_esc(str(c))}</c:v></c:pt>'
            for i, c in enumerate(categories)
        )
        cat_xml = (
            "<c:cat><c:strLit>"
            f'<c:ptCount val="{n_cats}"/>{cat_pts}</c:strLit></c:cat>'
        )
        val_cache_pts = "".join(
            f'<c:pt idx="{i}"><c:v>{v}</c:v></c:pt>'
            for i, v in enumerate(values) if not _is_blank(v)
        )
        val_xml = (
            "<c:val><c:numLit>"
            f'<c:ptCount val="{n_cats}"/>{val_cache_pts}</c:numLit></c:val>'
        )

    dash_xml = f'<a:prstDash val="{dash}"/>' if dash else ""
    line_spPr = (
        "<c:spPr>"
        f'<a:ln w="{line_width}" cap="rnd">'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        + dash_xml +
        '<a:round/>'
        "</a:ln></c:spPr>"
    )
    if marker_symbol and marker_symbol != "none":
        marker_xml = (
            "<c:marker>"
            f'<c:symbol val="{marker_symbol}"/>'
            f'<c:size val="{marker_size}"/>'
            "<c:spPr>"
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:ln w="9525"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln>'
            "</c:spPr></c:marker>"
        )
    else:
        marker_xml = '<c:marker><c:symbol val="none"/></c:marker>'

    return (
        "<c:ser>"
        f'<c:idx val="{s_idx}"/>'
        f'<c:order val="{s_idx}"/>'
        + tx_xml
        + line_spPr
        + marker_xml
        + cat_xml
        + val_xml
        + f'<c:smooth val="{1 if smooth else 0}"/>'
        + "</c:ser>"
    )


def line_chart(
    *,
    categories: list[str],
    series: list[dict],
    title: str | None = None,
    title_size_pt: int = 10,
    title_bold: bool = False,
    title_italic: bool = True,
    show_legend: bool = True,
    legend_pos: str = "b",
    value_axis_format: str = "General",
    show_gridlines: bool = True,
    major_gridline_color: str | None = "E6E6E6",
    major_gridline_width: int | None = 3_175,
    cat_label_size_pt: int = 9,
    marker_symbol: str = "circle",
    marker_size: int = 5,
    smooth: bool = False,
    line_width: int = 28_575,
    embed_data: bool = True,
    sheet_name: str = "Sheet1",
    cat_header: str = "Category",
) -> dict:
    """Generate a native line chart (one <c:ser> per series).

    Same return shape and embedded-workbook mechanics as column_chart /
    bar_chart. Each series dict takes name, values, and an optional hex color,
    plus optional per-series style overrides: "dash" (prstDash value, e.g.
    "dash" / "sysDot"; default solid), "marker" (symbol, "none" to suppress),
    "width" (line width EMU). Blank values render as gaps (dispBlanksAs=gap).
    grouping is fixed "standard" (the line-chart value).
    """
    if sheet_name != "Sheet1":
        raise ValueError(
            "sheet_name must be 'Sheet1': the embedded workbook hard-codes that "
            "sheet name, so any other value breaks the chart's Edit Data link")
    for s in series:
        if len(s["values"]) != len(categories):
            raise ValueError(
                f"Series '{s.get('name', '?')}' has {len(s['values'])} values "
                f"but {len(categories)} categories"
            )

    CAT_AX_ID = 333_333_333
    VAL_AX_ID = 444_444_444
    cat_label_size = cat_label_size_pt * 100

    if title:
        title_size = title_size_pt * 100
        title_b = "1" if title_bold else "0"
        title_i = "1" if title_italic else "0"
        title_xml = (
            "<c:title><c:tx><c:rich>"
            '<a:bodyPr rot="0" spcFirstLastPara="1" vertOverflow="ellipsis" '
            'wrap="square" anchor="ctr" anchorCtr="1"/><a:lstStyle/>'
            f'<a:p><a:pPr algn="ctr"><a:defRPr sz="{title_size}" b="{title_b}" i="{title_i}">'
            '<a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
            '<a:latin typeface="Arial"/></a:defRPr></a:pPr>'
            f'<a:r><a:rPr lang="en-US" sz="{title_size}" b="{title_b}" i="{title_i}">'
            '<a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
            '<a:latin typeface="Arial"/></a:rPr>'
            f'<a:t>{_esc(title)}</a:t></a:r></a:p>'
            "</c:rich></c:tx><c:overlay val=\"0\"/></c:title>"
            '<c:autoTitleDeleted val="0"/>'
        )
    else:
        title_xml = '<c:autoTitleDeleted val="1"/>'

    ser_xml = "".join(
        _build_line_series(
            s_idx=i, categories=categories, series=s, embed_data=embed_data,
            sheet_name=sheet_name, line_width=line_width,
            marker_symbol=marker_symbol, marker_size=marker_size, smooth=smooth,
        )
        for i, s in enumerate(series)
    )

    line_chart_xml = (
        "<c:lineChart>"
        '<c:grouping val="standard"/>'
        '<c:varyColors val="0"/>'
        + ser_xml
        + '<c:marker val="1"/>'
        + f'<c:axId val="{CAT_AX_ID}"/>'
        + f'<c:axId val="{VAL_AX_ID}"/>'
        + "</c:lineChart>"
    )

    _ax_txpr = (
        "<c:txPr>"
        '<a:bodyPr rot="0" spcFirstLastPara="1" vertOverflow="ellipsis" '
        'wrap="square" anchor="ctr" anchorCtr="1"/><a:lstStyle/>'
        f'<a:p><a:pPr><a:defRPr sz="{cat_label_size}" b="0">'
        '<a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
        '<a:latin typeface="Arial"/></a:defRPr></a:pPr>'
        '<a:endParaRPr lang="en-US"/></a:p></c:txPr>'
    )
    cat_ax_xml = (
        "<c:catAx>"
        f'<c:axId val="{CAT_AX_ID}"/>'
        '<c:scaling><c:orientation val="minMax"/></c:scaling>'
        '<c:delete val="0"/><c:axPos val="b"/>'
        '<c:numFmt formatCode="General" sourceLinked="1"/>'
        '<c:majorTickMark val="out"/><c:minorTickMark val="none"/>'
        '<c:tickLblPos val="nextTo"/>'
        + _ax_txpr
        + f'<c:crossAx val="{VAL_AX_ID}"/>'
        '<c:crosses val="autoZero"/><c:auto val="1"/>'
        '<c:lblAlgn val="ctr"/><c:lblOffset val="100"/>'
        '<c:noMultiLvlLbl val="0"/>'
        "</c:catAx>"
    )
    if show_gridlines:
        _gl_w = major_gridline_width if major_gridline_width is not None else 3_175
        _gl_color = major_gridline_color or "E6E6E6"
        gridlines_xml = (
            "<c:majorGridlines><c:spPr>"
            f'<a:ln w="{_gl_w}" cap="flat">'
            f'<a:solidFill><a:srgbClr val="{_gl_color}"/></a:solidFill>'
            '<a:prstDash val="solid"/></a:ln></c:spPr></c:majorGridlines>'
        )
    else:
        gridlines_xml = ""
    val_ax_xml = (
        "<c:valAx>"
        f'<c:axId val="{VAL_AX_ID}"/>'
        '<c:scaling><c:orientation val="minMax"/></c:scaling>'
        '<c:delete val="0"/><c:axPos val="l"/>'
        + gridlines_xml
        + f'<c:numFmt formatCode="{_esc_attr(value_axis_format)}" sourceLinked="0"/>'
        '<c:majorTickMark val="out"/><c:minorTickMark val="none"/>'
        '<c:tickLblPos val="nextTo"/>'
        + _ax_txpr
        + f'<c:crossAx val="{CAT_AX_ID}"/>'
        '<c:crosses val="autoZero"/><c:crossBetween val="between"/>'
        "</c:valAx>"
    )

    plot_area_xml = (
        "<c:plotArea><c:layout/>"
        + line_chart_xml + cat_ax_xml + val_ax_xml +
        "</c:plotArea>"
    )

    if show_legend:
        legend_xml = (
            "<c:legend>"
            f'<c:legendPos val="{legend_pos}"/><c:overlay val="0"/>'
            + _ax_txpr +
            "</c:legend>"
        )
    else:
        legend_xml = ""

    external_data_xml = (
        '<c:externalData r:id="rId1"><c:autoUpdate val="0"/></c:externalData>'
        if embed_data else ""
    )

    chart_xml = (
        f'{_XML_DECL}\n'
        f'<c:chartSpace {_NS}>'
        '<c:lang val="en-US"/><c:roundedCorners val="0"/>'
        '<c:chart>'
        + title_xml + plot_area_xml + legend_xml
        + '<c:plotVisOnly val="1"/><c:dispBlanksAs val="gap"/>'
        + '</c:chart>'
        + external_data_xml
        + '</c:chartSpace>'
    )

    if embed_data:
        embed_xlsx = _build_embed_xlsx(
            categories=categories, series=series, cat_header=cat_header)
        chart_rels = _CHART_RELS_TEMPLATE
    else:
        embed_xlsx = None
        chart_rels = None

    return {
        "chart_xml": chart_xml,
        "embed_xlsx": embed_xlsx,
        "chart_rels": chart_rels,
    }


# ── Waterfall (native stacked-column workaround) ─────────────────────────
def _waterfall_to_stacked_series(steps, *, increase_color, decrease_color,
                                 total_color):
    """Convert waterfall steps -> base / increase / decrease / total stacked
    series. Each step: {"label": str, "value": number|None,
    "kind": "start"|"delta"|"subtotal"|"end"}. start/subtotal/end draw a full
    bar to the running total (value=None uses the running total); a delta floats
    on a transparent base. Decrease deltas are stored as positive magnitudes so
    they stack correctly (see waterfall_chart re: labels)."""
    categories, base, increase, decrease, total = [], [], [], [], []
    running = 0.0
    for step in steps:
        kind = step.get("kind", "delta")
        raw = step.get("value")
        categories.append(step["label"])
        if kind in ("start", "subtotal", "end"):
            value = running if raw is None else float(raw)
            running = value
            base.append(None); increase.append(None)
            decrease.append(None); total.append(value)
            continue
        if raw is None:
            raise ValueError(f"delta step {step['label']!r} needs a numeric value")
        delta = float(raw)
        if delta >= 0:
            base.append(running); increase.append(delta)
            decrease.append(None); total.append(None)
        else:
            base.append(running + delta); increase.append(None)
            decrease.append(abs(delta)); total.append(None)
        running += delta
    series = [
        {"name": "_Base", "values": base, "no_fill": True, "hide_labels": True},
        {"name": "Increase", "values": increase, "color": increase_color},
        {"name": "Decrease", "values": decrease, "color": decrease_color},
        {"name": "Total", "values": total, "color": total_color},
    ]
    return categories, series


def waterfall_chart(*, steps, title: str | None = None,
                    value_axis_format: str = '"$"#,##0"M"',
                    increase_color: str = "3D5972",   # BLUE_4
                    decrease_color: str = "BFBFBF",   # GRAY_3
                    total_color: str = "263746",      # BLUE_5
                    show_value_labels: bool = False,
                    cat_header: str = "Step", **kwargs) -> dict:
    """Waterfall as a native stacked-column chart — a hidden base series plus
    visible increase / decrease / total series. Stays a real editable chart with
    an embedded xlsx (no Office-2016 ChartEx). Returns the standard chart dict.

        steps: list of {label, value, kind}; kind is start | delta | subtotal |
               end. A start/subtotal/end with value=None uses the running total.

    Labels default OFF: the decrease series is stored as a positive magnitude,
    so a built-in value label would read unsigned. For signed deltas, overlay
    slide text boxes (snippets) or pair the chart with a bridge table. Extra
    kwargs forward to _bars."""
    categories, series = _waterfall_to_stacked_series(
        steps, increase_color=increase_color, decrease_color=decrease_color,
        total_color=total_color)
    return _bars(horizontal=False, grouping="stacked", categories=categories,
                 series=series, title=title, show_legend=False,
                 value_axis_format=value_axis_format,
                 value_label_format=value_axis_format,
                 show_value_labels=show_value_labels, gap_width=60,
                 cat_header=cat_header, **kwargs)


# ── Marimekko (native binned percent-stacked-column workaround) ───────────
def _allocate_bins(widths: list[float], total_bins: int) -> list[int]:
    """Largest-remainder split of total_bins across columns proportional to
    width (each column gets at least 1 bin)."""
    if total_bins <= 0:
        raise ValueError("total_bins must be positive")
    total = sum(widths)
    if total <= 0:
        raise ValueError("widths must sum to a positive value")
    raw = [w / total * total_bins for w in widths]
    bins = [max(1, int(x)) for x in raw]
    while sum(bins) > total_bins:
        i = max(range(len(bins)), key=lambda j: bins[j] - raw[j])
        if bins[i] > 1:
            bins[i] -= 1
        else:
            break
    while sum(bins) < total_bins:
        i = max(range(len(bins)), key=lambda j: raw[j] - bins[j])
        bins[i] += 1
    return bins


def _marimekko_to_binned_series(*, columns, segments, values,
                                column_widths=None, colors=None, total_bins=100):
    """Convert mekko data -> repeated category bins for a percent-stacked column
    chart. Returns (categories, series, label_meta). Category labels are blank
    (the variable-width columns are labelled by slide overlays); label_meta
    carries each column's fractional x-span + width share for those overlays."""
    if column_widths is None:
        column_widths = {
            c: sum(values[c].get(s, 0.0) for s in segments) for c in columns
        }
    widths = [float(column_widths[c]) for c in columns]
    total_w = sum(widths)
    bins = _allocate_bins(widths, total_bins)
    categories: list[str] = []
    sv: dict = {s: [] for s in segments}
    label_meta: list[dict] = []
    cursor = 0
    for col, n in zip(columns, bins):
        for _ in range(n):
            categories.append("")          # axis blank; labels come from overlays
            for s in segments:
                sv[s].append(values[col].get(s, 0.0))
        label_meta.append({
            "label": col,
            "x0_frac": cursor / total_bins,
            "x1_frac": (cursor + n) / total_bins,
            "x_mid_frac": (cursor + n / 2) / total_bins,
            "width_share": float(column_widths[col]) / total_w,
        })
        cursor += n
    series = []
    for s in segments:
        d = {"name": s, "values": sv[s]}
        if colors and s in colors:
            d["color"] = colors[s]
        series.append(d)
    return categories, series, label_meta


def marimekko_chart(*, columns, segments, values, column_widths=None,
                    colors=None, total_bins=100, title: str | None = None,
                    show_legend: bool = True, legend_pos: str = "b", **kwargs):
    """Marimekko (variable-width, percent-stacked columns) as a NATIVE editable
    chart: each column is expanded into proportional thin bins and plotted
    percentStacked with gap_width=0, so it stays Edit-Data-backed (not shapes).

    Returns (chart_dict, label_meta): declare CHARTS=[chart_dict], and use
    label_meta to overlay column labels — the native axis can't label
    variable-width blocks, so the category axis is blanked and slide text boxes
    carry the names (see snippets).

        columns:  ordered column names (the wide axis)
        segments: ordered stack-segment names (one stack per column)
        values:   {column: {segment: value}}
        column_widths: {column: width}; default = the column's segment sum
        colors:   {segment: hex}
        total_bins: bin resolution for width fidelity (default 100)
    Extra kwargs forward to _bars."""
    categories, series, label_meta = _marimekko_to_binned_series(
        columns=columns, segments=segments, values=values,
        column_widths=column_widths, colors=colors, total_bins=total_bins)
    chart = _bars(horizontal=False, grouping="percentStacked",
                  categories=categories, series=series, title=title,
                  show_legend=show_legend, legend_pos=legend_pos,
                  value_axis_format="0%", show_gridlines=False,
                  show_value_labels=False, show_cat_labels=False,
                  gap_width=0, cat_header="Mekko bin", **kwargs)
    return chart, label_meta


def graphic_frame(
    *,
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    rId: str,
) -> str:
    """Emit a <p:graphicFrame> referencing a chart by rId.

    Drop this into a slide alongside other <p:sp> shapes. The rId must
    match the slide's chart relationship (managed by deck_core._build at
    build time — by convention rId2 for the first chart, rId3 second,
    etc., since rId1 is the slide-to-layout relationship).
    """
    return (
        "<p:graphicFrame>"
        "<p:nvGraphicFramePr>"
        f'<p:cNvPr id="{sp_id}" name="{_esc(name)}"/>'
        "<p:cNvGraphicFramePr/>"
        "<p:nvPr/>"
        "</p:nvGraphicFramePr>"
        "<p:xfrm>"
        f'<a:off x="{x}" y="{y}"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/>'
        "</p:xfrm>"
        "<a:graphic>"
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/chart">'
        '<c:chart xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        f'r:id="{rId}"/>'
        "</a:graphicData>"
        "</a:graphic>"
        "</p:graphicFrame>"
    )
