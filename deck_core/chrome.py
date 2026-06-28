"""deck_core.chrome - the author-facing house furniture for a body slide.

An author edits chrome as readable fields, never raw OOXML: a ``Chrome(...)`` record
(breadcrumb section/topic, the slide title + takeaway, the Preliminary chip, the
Sources band) plus ``body_slide(chrome, body)`` to assemble it around the body. For a
source slide whose title is a bare layout placeholder, ``layout_title`` /
``layout_placeholder`` keep that readable too. The locked geometry, ids, colors, and
sizes are private to this module - authors set chrome TEXT, never those.

    CHROME = Chrome(
        section="US-Built Ship Demand",
        topic="Status Quo",
        title="Status Quo Fleet Outlook",
        takeaway="Fleet shrinks ~144K GT p.a. '31-'50 (<2% of the 10M GT target).",
        preliminary=True,
        sources=Sources(source="Clarksons (US fleet size and GT data)"),
    )

    def render() -> str:
        return body_slide(CHROME, _body())
"""
from __future__ import annotations
from dataclasses import dataclass

from deck_core.layout import LEFT_MARGIN, CONTENT_W, SLIDE_W, SLIDE_H
from deck_core.primitives import esc, placeholder_sp, slide

# ── Locked chrome constants (private; verbatim from the template) ───────────
_DK = "162029"
_BLACK = "000000"
_BREADCRUMB = "44505C"
_PRELIM = "FFFFCC"
_SZ_BREADCRUMB = 1000
_SZ_SLIDE_TITLE = 2000
_SZ_PRELIM = 1200
_SZ_SOURCES = 800
_SZ_COVER_TITLE = 2800       # 28pt
_SZ_COVER_SUBTITLE = 2000    # 20pt
_SZ_DIVIDER_TITLE = 2800
_SZ_DIVIDER_SUBTITLE = 2000
_BREADCRUMB_X, _BREADCRUMB_Y, _BREADCRUMB_CX, _BREADCRUMB_CY = LEFT_MARGIN, 263_452, CONTENT_W, 153_888
_TITLE_X, _TITLE_Y, _TITLE_CX, _TITLE_CY = LEFT_MARGIN, 554_500, CONTENT_W, 640_080
_PRELIM_X, _PRELIM_Y, _PRELIM_CX, _PRELIM_CY = 10_232_214, 158_582, 1_467_986, 198_438
_SOURCES_X, _SOURCES_Y, _SOURCES_CX, _SOURCES_CY = LEFT_MARGIN, 5_930_000, CONTENT_W, 540_000
_SP_ID_BREADCRUMB = 2
_SP_ID_TITLE = 3
_SP_ID_PRELIM = 4
_SP_ID_SOURCES = 9999


def _chrome_run(text, *, size, bold=False, color=_DK, hyperlink_rid=None):
    """Locked chrome run: Arial, kern=1200, explicit size + color. Body text uses
    run(); chrome uses this so the staples stay byte-stable. hyperlink_rid wires an
    external link (slide-rels rId from the module's HYPERLINKS); None keeps the run
    byte-identical to the un-linked staple."""
    b = ' b="1"' if bold else ""
    hl = f'<a:hlinkClick r:id="{hyperlink_rid}"/>' if hyperlink_rid else ""
    return (f'<a:r><a:rPr lang="en-US" sz="{size}"{b} kern="1200" dirty="0">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/>'
            f'{hl}</a:rPr><a:t>{esc(text)}</a:t></a:r>')


def breadcrumb(section, topic_label, *, sp_id=_SP_ID_BREADCRUMB):
    """Top strip bound to slideLayout4 body placeholder idx=10: bold {Section}
    + non-bold " / {Topic Label}", Arial 10pt, breadcrumb color."""
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="Breadcrumb"/>'
            f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr><p:ph type="body" sz="quarter" idx="10"/></p:nvPr></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{_BREADCRUMB_X}" y="{_BREADCRUMB_Y}"/>'
            f'<a:ext cx="{_BREADCRUMB_CX}" cy="{_BREADCRUMB_CY}"/></a:xfrm></p:spPr>'
            f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p>'
            + _chrome_run(section, size=_SZ_BREADCRUMB, bold=True, color=_BREADCRUMB)
            + _chrome_run(f" / {topic_label}", size=_SZ_BREADCRUMB, color=_BREADCRUMB)
            + '</a:p></p:txBody></p:sp>')


def slide_title(topic, takeaway, *, sp_id=_SP_ID_TITLE, cx=None):
    """Slide title bound to the layout title placeholder: single run
    "{Topic} | {Finding}", Arial 20pt, dark. cx overrides the box width (EMU) to
    match a source title narrowed to clear top-right logos; None = full house width."""
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="Title"/>'
            f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{_TITLE_X}" y="{_TITLE_Y}"/>'
            f'<a:ext cx="{cx if cx is not None else _TITLE_CX}" cy="{_TITLE_CY}"/></a:xfrm></p:spPr>'
            f'<p:txBody><a:bodyPr rIns="0"/><a:lstStyle/><a:p>'
            + _chrome_run(f"{topic} | {takeaway}", size=_SZ_SLIDE_TITLE, color=_DK)
            + '</a:p></p:txBody></p:sp>')


def preliminary_chip(*, sp_id=_SP_ID_PRELIM, text="Preliminary"):
    """Top-right draft chip: draft-yellow fill, 1.5pt black border, 12pt bold.
    Required on every body slide; exempt on cover / divider."""
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="PrelimChip"/>'
            f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{_PRELIM_X}" y="{_PRELIM_Y}"/>'
            f'<a:ext cx="{_PRELIM_CX}" cy="{_PRELIM_CY}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{_PRELIM}"/></a:solidFill>'
            f'<a:ln w="19050"><a:solidFill><a:srgbClr val="{_BLACK}"/></a:solidFill></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" anchor="ctr" lIns="45720" tIns="9144" '
            f'rIns="45720" bIns="9144"/><a:lstStyle/><a:p><a:pPr algn="ctr"/>'
            + _chrome_run(text, size=_SZ_PRELIM, bold=True, color=_BLACK)
            + '</a:p></p:txBody></p:sp>')


def source_note(text, *, sp_id=_SP_ID_SOURCES, y=_SOURCES_Y):
    """Bottom strip: "Source: ...; ..." (singular "Source" per house style, even
    with many sources; semicolon-separated, no parenthetical numbering; a Note line
    may be combined via a pipe), Arial 8pt, top-anchored. Pass y to lift it above
    content that reaches the default band.

    `text` is a plain string (one staple run), or an iterable of segments — plain
    str pieces and Link(text, rId) pieces — for a source line carrying external
    hyperlinks. The plain-string path is byte-identical to the un-linked staple."""
    if isinstance(text, str):
        runs = _chrome_run(text, size=_SZ_SOURCES, color=_DK)
    else:
        runs = "".join(
            _chrome_run(seg.text, size=_SZ_SOURCES, color=_DK, hyperlink_rid=seg.rId)
            if isinstance(seg, Link)
            else _chrome_run(seg, size=_SZ_SOURCES, color=_DK)
            for seg in text)
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="Source"/>'
            f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{_SOURCES_X}" y="{y}"/>'
            f'<a:ext cx="{_SOURCES_CX}" cy="{_SOURCES_CY}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" anchor="t" lIns="91440" tIns="45720" '
            f'rIns="91440" bIns="45720"/><a:lstStyle/><a:p>'
            + runs
            + '</a:p></p:txBody></p:sp>')


def layout_title(text, *, sp_id, name, body_pr_xml='<a:bodyPr/>'):
    """A slide title that INHERITS its geometry from the slide layout (no explicit
    xfrm) - for a source slide (e.g. slideLayout3) whose title is a bare layout
    placeholder. The layout, not the module, owns title placement. Readable
    replacement for a hand-inlined raw <p:sp> title."""
    para = f'<a:p><a:r><a:rPr lang="en-US"/><a:t>{esc(text)}</a:t></a:r></a:p>'
    return placeholder_sp(sp_id, name, ph_type="title", body_pr_xml=body_pr_xml,
                          paragraphs=[para])


def layout_placeholder(sp_id, name, *, ph_type=None, ph_sz=None, ph_idx=None,
                       geom=None, paragraphs=None, body_pr_xml='<a:bodyPr/>'):
    """A shape bound to a layout placeholder by (type, sz, idx), inheriting the
    layout's geometry unless `geom` overrides it. Readable wrapper over the
    placeholder primitive for richer layout-owned placeholders (subtitles, etc.)."""
    return placeholder_sp(sp_id, name, ph_type=ph_type, ph_sz=ph_sz, ph_idx=ph_idx,
                          geom=geom, paragraphs=paragraphs, body_pr_xml=body_pr_xml)


# ── Full-slide layout compositions (cover / section divider) ─────────────────


def cover_layout(title: str, subtitle: str | None = None, *,
                 footer: str | None = None) -> str:
    """Cover (deck-title) slide composition.

    Binds to the Cover layout (slideLayout1). The slide module MUST declare
    `LAYOUT = "slideLayout1"` at module scope so build() points the slide's rels
    at the Cover layout.

    Placeholder mapping (positioning inherited from slideLayout1):
        body idx=12  -> title (28pt) on line 1; subtitle (20pt italic)
                       on line 2 inside the same placeholder.
        title (idx=) -> small footer/date line at the bottom.
    """
    title_text = esc(title)
    paragraphs = (
        f'<a:p>'
        f'<a:pPr><a:lnSpc><a:spcPct val="115000"/></a:lnSpc></a:pPr>'
        f'<a:r>'
        f'<a:rPr lang="en-US" sz="{_SZ_COVER_TITLE}" kern="1200" dirty="0"/>'
        f'<a:t>{title_text}</a:t>'
        f'</a:r>'
        f'</a:p>'
    )
    if subtitle:
        subtitle_text = esc(subtitle)
        paragraphs += (
            f'<a:p>'
            f'<a:pPr><a:lnSpc><a:spcPct val="115000"/></a:lnSpc></a:pPr>'
            f'<a:r>'
            f'<a:rPr lang="en-US" sz="{_SZ_COVER_SUBTITLE}" i="1" kern="1200" dirty="0"/>'
            f'<a:t>{subtitle_text}</a:t>'
            f'</a:r>'
            f'</a:p>'
        )

    big_title_sp = (
        f'<p:sp>'
        f'<p:nvSpPr>'
        f'<p:cNvPr id="100" name="CoverTitle"/>'
        f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
        f'<p:nvPr><p:ph type="body" sz="quarter" idx="12"/></p:nvPr>'
        f'</p:nvSpPr>'
        # Override the layout placeholder geometry. The inherited width
        # (cx=7_776_399) wraps a multi-word title, so widen to the full content
        # width. Top-anchor (anchor="t") and pin the block low (y=4_140_000,
        # ~where the bottom-anchored 2-line cover used to sit) so a subtitle that
        # wraps to a 2nd line grows DOWNWARD instead of pushing the title up.
        f'<p:spPr>'
        f'<a:xfrm><a:off x="453080" y="4140000"/>'
        f'<a:ext cx="11285842" cy="2162129"/></a:xfrm>'
        f'</p:spPr>'
        f'<p:txBody>'
        f'<a:bodyPr anchor="t"/>'
        f'<a:lstStyle/>'
        f'{paragraphs}'
        f'</p:txBody>'
        f'</p:sp>'
    )

    if footer:
        footer_text = esc(footer)
        footer_sp = (
            f'<p:sp>'
            f'<p:nvSpPr>'
            f'<p:cNvPr id="101" name="CoverFooter"/>'
            f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr><p:ph type="title"/></p:nvPr>'
            f'</p:nvSpPr>'
            f'<p:spPr/>'
            f'<p:txBody>'
            f'<a:bodyPr/>'
            f'<a:lstStyle/>'
            f'<a:p>'
            f'<a:pPr><a:lnSpc><a:spcPct val="115000"/></a:lnSpc></a:pPr>'
            f'<a:r>'
            f'<a:rPr lang="en-US" kern="1200" dirty="0"/>'
            f'<a:t>{footer_text}</a:t>'
            f'</a:r>'
            f'</a:p>'
            f'</p:txBody>'
            f'</p:sp>'
        )
        return big_title_sp + footer_sp
    return big_title_sp


def section_divider_layout(section: str, subtitle: str | None = None, *,
                           page_num: int | None = None,
                           total_pages: int | None = None) -> str:
    """Section-divider (transition) slide composition.

    Binds to the Section Divider layout (slideLayout2). The slide module MUST
    declare `LAYOUT = "slideLayout2"` at module scope so build() points the
    slide's rels at the divider layout.

    Placeholder mapping: the section name (line 1, 28pt) and subtitle (line 2,
    20pt italic) share ONE placeholder (body idx=11 - the slideLayout2 analog of
    the cover's idx=12), overridden to the cover's geometry so the two lines land
    exactly where cover_layout's title/subtitle do (full content width, top
    anchored, pinned low so a wrapping subtitle grows downward).

    If `page_num` and `total_pages` are both passed, an explicit page counter is
    rendered at the bottom-right (dividers do not auto-number, so this optional
    override is kept).
    """
    section_text = esc(section)
    # Title (line 1) + subtitle (line 2) share ONE top-anchored placeholder,
    # exactly like cover_layout, so the two lines land where the cover's do and a
    # wrapping subtitle grows downward rather than pushing the title up.
    paragraphs = (
        f'<a:p>'
        f'<a:pPr><a:lnSpc><a:spcPct val="115000"/></a:lnSpc></a:pPr>'
        f'<a:r>'
        f'<a:rPr lang="en-US" sz="{_SZ_DIVIDER_TITLE}" kern="1200" dirty="0"/>'
        f'<a:t>{section_text}</a:t>'
        f'</a:r>'
        f'</a:p>'
    )
    if subtitle:
        subtitle_text = esc(subtitle)
        paragraphs += (
            f'<a:p>'
            f'<a:pPr><a:lnSpc><a:spcPct val="115000"/></a:lnSpc></a:pPr>'
            f'<a:r>'
            f'<a:rPr lang="en-US" sz="{_SZ_DIVIDER_SUBTITLE}" i="1" kern="1200" dirty="0"/>'
            f'<a:t>{subtitle_text}</a:t>'
            f'</a:r>'
            f'</a:p>'
        )

    # Override idx=11 to the cover's title-block geometry: full content width,
    # top-anchored (anchor="t") and pinned low (y=4_140_000) so it matches the
    # cover and a wrapping subtitle grows downward (mirrors cover_layout).
    out = (
        f'<p:sp>'
        f'<p:nvSpPr>'
        f'<p:cNvPr id="110" name="DividerTitle"/>'
        f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
        f'<p:nvPr><p:ph type="body" sz="quarter" idx="11"/></p:nvPr>'
        f'</p:nvSpPr>'
        f'<p:spPr>'
        f'<a:xfrm><a:off x="453080" y="4140000"/>'
        f'<a:ext cx="11285842" cy="2162129"/></a:xfrm>'
        f'</p:spPr>'
        f'<p:txBody>'
        f'<a:bodyPr anchor="t"/>'
        f'<a:lstStyle/>'
        f'{paragraphs}'
        f'</p:txBody>'
        f'</p:sp>'
    )

    if page_num is not None and total_pages is not None:
        cx = 1_500_000
        cy = 230_000
        x = SLIDE_W - LEFT_MARGIN - cx
        y = SLIDE_H - 290_000
        pn_text = esc(f"{page_num} / {total_pages}")
        out += (
            f'<p:sp>'
            f'<p:nvSpPr>'
            f'<p:cNvPr id="4500" name="PageNumber"/>'
            f'<p:cNvSpPr txBox="1"/>'
            f'<p:nvPr/>'
            f'</p:nvSpPr>'
            f'<p:spPr>'
            f'<a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:noFill/>'
            f'<a:ln><a:noFill/></a:ln>'
            f'</p:spPr>'
            f'<p:txBody>'
            f'<a:bodyPr wrap="square" anchor="t" lIns="91440" tIns="45720" '
            f'rIns="91440" bIns="45720"/>'
            f'<a:lstStyle/>'
            f'<a:p>'
            f'<a:pPr algn="r"><a:lnSpc><a:spcPct val="115000"/></a:lnSpc></a:pPr>'
            f'<a:r>'
            f'<a:rPr lang="en-US" sz="{_SZ_SOURCES}" kern="1200" dirty="0">'
            f'<a:solidFill><a:srgbClr val="{_DK}"/></a:solidFill>'
            f'<a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/>'
            f'</a:rPr>'
            f'<a:t>{pn_text}</a:t>'
            f'</a:r>'
            f'</a:p>'
            f'</p:txBody>'
            f'</p:sp>'
        )

    return out


@dataclass(frozen=True)
class Link:
    """A hyperlinked span in a source line: visible `text` wired to the slide-rels
    `rId` declared in the module's HYPERLINKS list ({"rId": ..., "url": ...}). Drop
    Link(...) pieces into a Sources `source` tuple alongside plain strings."""
    text: str
    rId: str


@dataclass(frozen=True)
class Sources:
    """The house Sources band, as fields. `source` is a string or a tuple of
    items (joined with "; "); a tuple item may be a Link(...) to hyperlink that
    span. `note` prepends a "Note: ..." segment; `y` lifts the band above content
    that reaches the default floor."""
    source: object = None          # str | tuple[str | Link, ...] | None
    note: object = None            # str | None
    y: object = None               # int | None

    def _items(self) -> tuple:
        if not self.source:
            return ()
        return (self.source,) if isinstance(self.source, str) else tuple(self.source)

    def has_links(self) -> bool:
        return any(isinstance(it, Link) for it in self._items())

    def text(self) -> str:
        parts = []
        if self.note:
            parts.append(f"Note: {self.note}")
        if self.source:
            src = self.source if isinstance(self.source, str) else "; ".join(self.source)
            parts.append(f"Source: {src}")
        return " | ".join(parts)

    def segments(self) -> list:
        """The source line as a flat list of plain-str and Link segments — the rich
        equivalent of text(), used when any source item is a Link."""
        out = []
        if self.note:
            out.append(f"Note: {self.note}")
        items = self._items()
        if items:
            if self.note:
                out.append(" | ")
            out.append("Source: ")
            for i, it in enumerate(items):
                if i:
                    out.append("; ")
                out.append(it)
        return out


@dataclass(frozen=True)
class Chrome:
    """The editable house furniture of a body slide. Fields are plain text; the
    geometry/ids/colors are private to deck_core.chrome. `section`/`topic` are
    optional - omit them on a slide that carries no breadcrumb."""
    title: str
    takeaway: str = ""
    section: object = None         # str | None - breadcrumb left segment
    topic: object = None           # str | None - breadcrumb right segment
    preliminary: bool = True
    preliminary_text: str = "Preliminary"
    sources: object = None         # Sources | str | None
    title_cx: object = None        # int | None - narrow the title box (EMU) to clear top-right logos


def body_slide(chrome: Chrome, body_xml: str) -> str:
    """Assemble a complete <p:sld> from a Chrome record and the body XML: the
    optional breadcrumb, the slide title, the optional Preliminary chip, the body,
    and the optional Sources band. The body box clears the chrome regions, so
    chrome and body never overlap."""
    pieces = []
    if chrome.section is not None:
        pieces.append(breadcrumb(chrome.section, chrome.topic))
    pieces.append(slide_title(chrome.title, chrome.takeaway, cx=chrome.title_cx))
    if chrome.preliminary:
        pieces.append(preliminary_chip(text=chrome.preliminary_text))
    pieces.append(body_xml)
    src = chrome.sources
    if src is not None:
        if isinstance(src, Sources):
            payload = src.segments() if src.has_links() else src.text()
            pieces.append(source_note(payload, y=src.y) if src.y is not None
                          else source_note(payload))
        else:
            pieces.append(source_note(src))
    return slide("".join(pieces))
