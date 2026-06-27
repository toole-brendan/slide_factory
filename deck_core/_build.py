"""deck_core._build - the shared raw-OOXML PowerPoint build plumbing.

One generic builder, `build_pptx(...)`, that the per-program decks (deck_ddg,
deck_submarines, …) call with their own slide list + paths. This is the
de-duplicated "base pipeline" each deck used to carry its own copy of:
content-types, package rels, presentation.xml, the slide/chart render loop, and
the zip packer. Program-specific things (which slides, the output path, the
unzipped template dir, the Saronic assets, the docProps identity) are passed in.

Each slide module returns a complete <p:sld> XML string via a no-arg
`render() -> str` (the render_fn passed alongside the module), and may export
`CHARTS: list[dict]` (chart dicts from deck_core.charts — column_chart /
bar_chart / line_chart / waterfall_chart / marimekko_chart) which the loop wires
as native chart parts + per-slide chart rels. A module may also export
`IMAGES: list[dict]` — each `{"rId": "rIdN", "file": "<name in ppt/media>"}` — which
the loop wires as per-slide image relationships so a `picture(..., r_embed="rIdN")`
resolves (the bytes come from assets/media/ or the `images` dir).

A slide module declares `LAYOUT = "slideLayoutN"` at module scope for non-default
layouts (cover = slideLayout1, divider = slideLayout2); body slides omit it and
default to slideLayout4 (which auto-numbers - no manual page number).
"""
from __future__ import annotations

import datetime as dt
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape as _escape

from deck_core.ooxml import XML_DECL, NS
from deck_core.style import SLIDE_W, SLIDE_H

DEFAULT_LAYOUT = "slideLayout4"   # body slides (auto-number; no manual page number)

ROOT_RELS_XML = (
    f'{XML_DECL}\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
    '</Relationships>'
)


def _content_types_xml(n_slides: int, num_charts: int, embeds) -> str:
    overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
    ]
    for i in range(1, 7):
        overrides.append(f'<Override PartName="/ppt/slideLayouts/slideLayout{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>')
    for i in range(1, n_slides + 1):
        overrides.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
    for i in range(1, num_charts + 1):
        overrides.append(f'<Override PartName="/ppt/charts/chart{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.chart+xml"/>')
    # Declare each embedded workbook part with its own content type. Native
    # charts emit .xlsx (spreadsheetml.sheet); a verbatim-bundled chart may
    # reuse the source's .xlsb (binary) workbook. Embeds are keyed by chart
    # number, so with a mix the part names are NOT 1..N contiguous — iterate
    # the actual (PartName, content-type) set the build loop collected.
    for partname, content_type in embeds:
        overrides.append(f'<Override PartName="{partname}" ContentType="{content_type}"/>')
    overrides += [
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/ppt/theme/theme2.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/ppt/handoutMasters/handoutMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.handoutMaster+xml"/>',
        '<Override PartName="/ppt/tags/tag1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tags+xml"/>',
        '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>',
        '<Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>',
        '<Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
        '<Override PartName="/docMetadata/LabelInfo.xml" ContentType="application/vnd.ms-office.classificationlabels+xml"/>',
    ]
    defaults = [
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Default Extension="jpeg" ContentType="image/jpeg"/>',
        '<Default Extension="jpg" ContentType="image/jpeg"/>',
        '<Default Extension="png" ContentType="image/png"/>',
        '<Default Extension="svg" ContentType="image/svg+xml"/>',
        '<Default Extension="emf" ContentType="image/x-emf"/>',
        '<Default Extension="bin" ContentType="application/vnd.openxmlformats-officedocument.oleObject"/>',
    ]
    return (f'{XML_DECL}\n'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            + "".join(defaults) + "".join(overrides) + '</Types>')


def _core_xml(title: str, creator: str) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    title = _escape(title)        # &, <, > in deck title/creator would break the XML
    creator = _escape(creator)
    return (
        f'{XML_DECL}\n'
        '<cp:coreProperties '
        'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f'<dc:title>{title}</dc:title>'
        f'<dc:creator>{creator}</dc:creator>'
        f'<cp:lastModifiedBy>{creator}</cp:lastModifiedBy>'
        '<cp:revision>1</cp:revision>'
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
        '</cp:coreProperties>'
    )


def _app_xml(n_slides: int, n_hidden: int, app: str) -> str:
    app = _escape(app)            # defensive: app name flows straight into XML text
    return (
        f'{XML_DECL}\n'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        f'<Application>{app}</Application>'
        '<PresentationFormat>Widescreen</PresentationFormat>'
        f'<Slides>{n_slides}</Slides><Notes>0</Notes>'
        f'<HiddenSlides>{n_hidden}</HiddenSlides>'
        '<MMClips>0</MMClips><ScaleCrop>false</ScaleCrop>'
        '<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
        '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion>'
        '</Properties>'
    )


def _presentation_xml(n_slides: int) -> str:
    slide_ids = "".join(f'<p:sldId id="{256 + i}" r:id="rId{i + 2}"/>' for i in range(n_slides))
    return (
        f'{XML_DECL}\n'
        f'<p:presentation {NS} saveSubsetFonts="1" autoCompressPictures="0">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        f'<p:handoutMasterIdLst><p:handoutMasterId r:id="rId{n_slides + 2}"/></p:handoutMasterIdLst>'
        f'<p:sldIdLst>{slide_ids}</p:sldIdLst>'
        f'<p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}"/>'
        '<p:notesSz cx="6934200" cy="9220200"/>'
        '<p:defaultTextStyle>'
        '<a:defPPr><a:defRPr lang="en-US"/></a:defPPr>'
        '<a:lvl1pPr marL="0" algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" latinLnBrk="0" hangingPunct="1">'
        '<a:defRPr sz="1800" kern="1200"><a:solidFill><a:schemeClr val="tx1"/></a:solidFill>'
        '<a:latin typeface="+mn-lt"/><a:ea typeface="+mn-ea"/><a:cs typeface="+mn-cs"/></a:defRPr></a:lvl1pPr>'
        '</p:defaultTextStyle></p:presentation>'
    )


def _presentation_rels_xml(n_slides: int) -> str:
    rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>']
    for i in range(n_slides):
        rels.append(f'<Relationship Id="rId{i + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i + 1}.xml"/>')
    base = n_slides + 2
    rels += [
        f'<Relationship Id="rId{base}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/handoutMaster" Target="handoutMasters/handoutMaster1.xml"/>',
        f'<Relationship Id="rId{base+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/>',
        f'<Relationship Id="rId{base+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/viewProps" Target="viewProps.xml"/>',
        f'<Relationship Id="rId{base+3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>',
        f'<Relationship Id="rId{base+4}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles" Target="tableStyles.xml"/>',
    ]
    return (f'{XML_DECL}\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(rels) + '</Relationships>')


def _slide_rels_xml(n: int, slide_rels: dict, default_layout: str) -> str:
    rels = slide_rels.get(n, [("rId1", "slideLayout", f"../slideLayouts/{default_layout}.xml")])
    parts = []
    for rId, t, target in rels:
        parts.append(f'<Relationship Id="{rId}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/{t}" Target="{target}"/>')
    return (f'{XML_DECL}\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(parts) + '</Relationships>')


def build_pptx(slide_module_renders, *, out: Path, extracted: Path, assets: Path,
               title: str, creator: str, app: str = "deck_core",
               images: Path | None = None, hidden: tuple[int, ...] = (),
               default_layout: str = DEFAULT_LAYOUT) -> None:
    """Render every slide and pack the .pptx.

    slide_module_renders: list of (module, render_fn) where render_fn() -> <p:sld>
      XML string and `module` may carry `LAYOUT`, `CHARTS`, and `IMAGES` attributes.
    extracted: the unzipped template dir (slideLayouts, slideMaster, theme, …).
    assets:    dir with a media/ subdir (Saronic chrome) + optional embeddings/.
    images:    optional dir of extra pictures; the bytes are copied into ppt/media/
      (brand chrome under assets/media/ is copied too). To SHOW an image, a slide
      module declares IMAGES = [{"rId": "rIdN", "file": "<name>"}, ...] and emits
      picture(sp_id, name, r_embed="rIdN", ...); the builder wires the per-slide image
      rel automatically. Image rIds continue AFTER chart rIds: with no charts the first
      image is rId2, with one chart it is rId3. See snippets "images".
    """
    out, extracted, assets = Path(out), Path(extracted), Path(assets)
    n_slides = len(slide_module_renders)

    def _ex(p: str) -> bytes:
        return (extracted / p).read_bytes()

    # Seed per-slide rels from each module's LAYOUT (local -> idempotent).
    slide_rels: dict[int, list] = {}
    for slot, (mod, _) in enumerate(slide_module_renders, start=1):
        layout = getattr(mod, "LAYOUT", default_layout)
        slide_rels[slot] = [("rId1", "slideLayout", f"../slideLayouts/{layout}.xml")]

    # Render slides; collect native chart parts + wire per-slide chart rels.
    chart_parts: dict[str, str | bytes] = {}
    global_chart_num = 0
    embeds: list[tuple[str, str]] = []   # (Content_Types PartName, content type)
    declared_images: list[tuple[int, str]] = []
    slides: list[str] = []
    for slide_idx, (mod, render_fn) in enumerate(slide_module_renders, start=1):
        slides.append(render_fn())
        for local_idx, chart in enumerate(list(getattr(mod, "CHARTS", []))):
            global_chart_num += 1
            if isinstance(chart, dict):
                chart_xml = chart["chart_xml"]; embed_bytes = chart.get("embed_xlsx"); chart_rels_tpl = chart.get("chart_rels")
                # Embed filename + content type default to the native-chart .xlsx
                # convention; a bundled chart reusing a source .xlsb overrides both
                # (see deck_core.charts.editable_bundled_chart). Both templates take
                # {chart_num} so each chart's embed is uniquely named.
                embed_name_tpl = chart.get("embed_filename", "Microsoft_Excel_Worksheet{chart_num}.xlsx")
                embed_ct = chart.get("embed_content_type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                chart_xml = chart; embed_bytes = None; chart_rels_tpl = None
                embed_name_tpl = ""; embed_ct = ""
            if embed_bytes is not None and not chart_rels_tpl:
                raise ValueError(
                    f"slide {slide_idx} chart {local_idx + 1}: "
                    f"embed_xlsx requires chart_rels")
            chart_parts[f"ppt/charts/chart{global_chart_num}.xml"] = chart_xml
            if embed_bytes is not None:
                embed_name = embed_name_tpl.format(chart_num=global_chart_num)
                embeds.append((f"/ppt/embeddings/{embed_name}", embed_ct))
                chart_parts[f"ppt/charts/_rels/chart{global_chart_num}.xml.rels"] = chart_rels_tpl.format(chart_num=global_chart_num)
                chart_parts[f"ppt/embeddings/{embed_name}"] = embed_bytes
            slide_rels[slide_idx].append((f"rId{local_idx + 2}", "chart", f"../charts/chart{global_chart_num}.xml"))
        # Wire per-slide image rels (symmetric to charts). A module declares
        # IMAGES = [{"rId": "rIdN", "file": "<name in ppt/media>"}, ...] and its
        # picture(..., r_embed="rIdN") must use the same rId. Image rIds continue
        # AFTER chart rIds (no charts -> first image rId2; one chart -> rId3).
        used_rids = [r for (r, _, _) in slide_rels[slide_idx]]
        first_image_rid = f"rId{len(used_rids) + 1}"
        for img in list(getattr(mod, "IMAGES", [])):
            if not (isinstance(img, dict) and "rId" in img and "file" in img):
                raise ValueError(
                    f"slide {slide_idx}: each IMAGES entry must be a dict with 'rId' "
                    f"and 'file' keys (got {img!r})")
            rId, fname = img["rId"], img["file"]
            if rId in used_rids:
                raise ValueError(
                    f"slide {slide_idx}: image rId {rId!r} collides with the layout, a "
                    f"chart, or another image; image rIds must continue after chart rIds "
                    f"(first image on this slide is {first_image_rid})")
            used_rids.append(rId)
            slide_rels[slide_idx].append((rId, "image", f"../media/{fname}"))
            declared_images.append((slide_idx, fname))

    for nidx in hidden:
        if not 1 <= nidx <= n_slides:
            raise ValueError(f"hidden slide index {nidx} out of range 1..{n_slides}")
        slides[nidx - 1] = slides[nidx - 1].replace("<p:sld ", '<p:sld show="0" ', 1)

    parts: dict[str, str | bytes] = {
        "[Content_Types].xml": _content_types_xml(n_slides, global_chart_num, embeds),
        "_rels/.rels": ROOT_RELS_XML,
        "docProps/core.xml": _core_xml(title, creator),
        "docProps/app.xml": _app_xml(n_slides, len(hidden), app),
        "docMetadata/LabelInfo.xml": _ex("docMetadata/LabelInfo.xml"),
        "ppt/presentation.xml": _presentation_xml(n_slides),
        "ppt/_rels/presentation.xml.rels": _presentation_rels_xml(n_slides),
        "ppt/presProps.xml": _ex("ppt/presProps.xml"),
        "ppt/viewProps.xml": _ex("ppt/viewProps.xml"),
        "ppt/tableStyles.xml": _ex("ppt/tableStyles.xml"),
        "ppt/theme/theme1.xml": _ex("ppt/theme/theme1.xml"),
        "ppt/theme/theme2.xml": _ex("ppt/theme/theme2.xml"),
        "ppt/slideMasters/slideMaster1.xml": _ex("ppt/slideMasters/slideMaster1.xml"),
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": _ex("ppt/slideMasters/_rels/slideMaster1.xml.rels"),
        "ppt/handoutMasters/handoutMaster1.xml": _ex("ppt/handoutMasters/handoutMaster1.xml"),
        "ppt/handoutMasters/_rels/handoutMaster1.xml.rels": _ex("ppt/handoutMasters/_rels/handoutMaster1.xml.rels"),
        "ppt/tags/tag1.xml": _ex("ppt/tags/tag1.xml"),
    }
    for i in range(1, 7):
        parts[f"ppt/slideLayouts/slideLayout{i}.xml"] = _ex(f"ppt/slideLayouts/slideLayout{i}.xml")
        parts[f"ppt/slideLayouts/_rels/slideLayout{i}.xml.rels"] = _ex(f"ppt/slideLayouts/_rels/slideLayout{i}.xml.rels")
    for i, body in enumerate(slides, 1):
        parts[f"ppt/slides/slide{i}.xml"] = body
        parts[f"ppt/slides/_rels/slide{i}.xml.rels"] = _slide_rels_xml(i, slide_rels, default_layout)
    parts.update(chart_parts)

    # Media (Saronic chrome) + optional photos/embeddings + thumbnail.
    # Skip dotfiles and non-files: a scaffold placeholder (e.g. a freshly-created
    # images/.gitkeep) copied verbatim into ppt/media/ has an extension absent from
    # [Content_Types].xml -> an invalid OPC package that PowerPoint "repairs" on open.
    def _packable(f):
        return f.is_file() and not f.name.startswith(".")
    if (assets / "media").is_dir():
        for f in (assets / "media").iterdir():
            if _packable(f):
                parts[f"ppt/media/{f.name}"] = f.read_bytes()
    if images and Path(images).is_dir():
        for f in Path(images).iterdir():
            if _packable(f):
                parts[f"ppt/media/{f.name}"] = f.read_bytes()
    if (assets / "embeddings").is_dir():
        for f in (assets / "embeddings").iterdir():
            if _packable(f):
                parts[f"ppt/embeddings/{f.name}"] = f.read_bytes()
    thumb = extracted / "docProps/thumbnail.jpeg"
    if thumb.is_file():
        parts["docProps/thumbnail.jpeg"] = thumb.read_bytes()

    # Every image declared in a module's IMAGES must resolve to a packaged media part,
    # else the wired rel dangles and PowerPoint "repairs" the file on open.
    media_names = {p.rsplit("/", 1)[-1] for p in parts if p.startswith("ppt/media/")}
    for slide_idx, fname in declared_images:
        if fname not in media_names:
            raise ValueError(
                f"slide {slide_idx}: image {fname!r} is declared in IMAGES but is not in "
                f"ppt/media/ — add it to assets/media/ or the images dir")

    out.parent.mkdir(parents=True, exist_ok=True)
    # Belt-and-suspenders OPC guard: every packaged part must have a declared content
    # type -- its extension in a <Default>, or the part name carried by an <Override>.
    # An undeclared part is an invalid OPC package that PowerPoint "repairs" on open;
    # fail loudly at build time instead of shipping a repairable pptx.
    ct_xml = parts["[Content_Types].xml"]
    declared_ext = {e.lower() for e in re.findall(r'Default Extension="([^"]+)"', ct_xml)}
    override_parts = set(re.findall(r'Override PartName="([^"]+)"', ct_xml))
    undeclared = []
    for p in parts:
        if p == "[Content_Types].xml":
            continue
        base = p.rsplit("/", 1)[-1]
        ext = base.rsplit(".", 1)[-1].lower() if "." in base else ""
        if ext not in declared_ext and ("/" + p) not in override_parts:
            undeclared.append(p)
    if undeclared:
        raise ValueError(
            "package contains parts with no declared content type (invalid OPC -- "
            "PowerPoint would 'repair' on open): " + ", ".join(sorted(undeclared)))

    order = ["[Content_Types].xml"] + sorted(p for p in parts if p != "[Content_Types].xml")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in order:
            zf.writestr(name, parts[name])
    print(f"wrote {out}  ({n_slides} slides, {global_chart_num} charts)")
