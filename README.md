# slide_factory

A self-contained workspace for authoring native PowerPoint slides from raw OOXML —
the `deck_core` rendering engine plus a curated **style library** of hand-polished
slide modules ported 1:1 from real market-analysis decks.

Pure Python **standard library** — no pip packages, no CLI tools (LibreOffice etc.)
required to build.

## Layout

```
slide_factory/
├─ deck_core/          the raw-OOXML rendering engine
│  ├─ authoring.py     the one public import surface (re-exports the vocabulary)
│  ├─ AUTHORING_API.md categorized quick-ref for deck_core.authoring
│  ├─ primitives.py    text_box / connector / table / picture / slide builders
│  ├─ table_kit.py     edge / bd / cell / rcell table-cell helpers
│  ├─ charts.py        native PowerPoint chart XML
│  ├─ style.py         palette / type scale / canvas geometry tokens
│  ├─ _build.py        build_pptx(): packs slides/charts/media into a .pptx
│  ├─ new_slide.py     starter skeleton for a new slide module
│  └─ slide_probe.py   read-only OOXML inspector (QA)
├─ infra/
│  ├─ template/        unzipped .pptx template (layouts / master / theme)
│  └─ assets/          brand media/ + chart embeddings/
└─ style_library/
   ├─ _tools/          convert_slide.py — source-deck OOXML → idiomatic module
   ├─ build_deck.py    ← run this
   └─ library/         the importable package
      ├─ lib.py        pipeline bindings (output path, template, assets, images)
      └─ slides/       one module per slide + _src/ (chart data) + images/
```

## Build

```bash
cd style_library
python3 build_deck.py
```

Output: `style_library/library.pptx`.

## Add a slide

Convert a slide out of a source `.pptx` into an idiomatic `deck_core` module, then
register it in `style_library/library/slides/__init__.py`:

```bash
python3 style_library/_tools/convert_slide.py SOURCE.pptx N \
    --out style_library/library/slides/<name>.py \
    --src-dir style_library/library/slides/_src \
    --module-name <name>
```
