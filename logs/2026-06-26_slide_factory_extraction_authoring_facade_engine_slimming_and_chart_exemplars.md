# Session log & handoff — `slide_factory` standalone extraction, the `authoring` façade + `table_kit`, engine slimming, and four chart-delivery teaching exemplars

**Date:** 2026-06-26
**Project:** `/Users/brendantoole/projects3/slide_factory/` — a **new, standalone** workspace created this session (a sibling of `ooxml_build_pipelines_light/`, not inside it).
**Build:** `cd slide_factory/style_library && python3 build_deck.py` → `library.pptx`. Pure Python stdlib, no deps, no CLI tools.
**Status at handoff:** builds green — **44 slides, 25 charts, 26 embeddings**. Not a git repo (git init declined).

Big picture: we lifted `deck_core` (the raw-OOXML engine) + the curated **style library** out of the shared monorepo into an isolated sandbox, then evolved the authoring architecture there per `projects3/transcript_1.rtf` (rulebook-led → **primitive-led + exemplar-led**). Three engine-level moves landed — a single **public façade** (`deck_core.authoring`), a shared **`table_kit`**, and an aggressive **slim-down** (renamed/deleted internals) — every one **output-neutral**, proven by a per-slide XML byte-diff against a pre-refactor baseline. Then we began the **teaching-exemplar** workstream: the same `us_delivery_capacity` slide authored **four ways** (factory chart / inline-asset chart / styled-from-`_src` / source-faithful) plus a pure-table `addressable_demand` exemplar, all rendering at the front of the deck for comparison. Hard constraint throughout: **the shared `deck_core` under `ooxml_build_pipelines_light/` is untouched** (mro/army/distributed_shipbuilding import it directly), so slide_factory now **diverges** from it — that's intentional; this is the sandbox.

---

## 0. The standalone extraction (why slide_factory exists)

Copied into a clean tree (artifacts excluded: `__pycache__`, `.DS_Store`, `logs/`, `reports/`, the 5 MB `infra/ooxml_reference/`, the stale prebuilt `library.pptx`):

```
slide_factory/
├─ deck_core/                 the engine (see §6 for current inventory)
├─ infra/{template, assets}   unzipped pptx template + brand media/embeddings
└─ style_library/             DECK_DIR (holds build_deck.py + library.pptx)
   ├─ _tools/                 convert_slide.py converter
   ├─ build_deck.py           ← run this
   └─ library/                the importable package
      ├─ __init__.py          sys.path bootstrap
      ├─ lib.py               pipeline bindings (OUT / TEMPLATE / ASSETS / IMAGES)
      └─ slides/{__init__.py, *.py, _src/, images/}
```

The old corpus triple-nested `projects/style_library/library/library/`; we **collapsed** it to `style_library/library/` and **dropped the `projects/` wrapper**. That changed depth-from-root 4→2, so the only code edits were two `parents[4] → parents[2]` rewires (`library/__init__.py` `_CORE_DIR`, `library/lib.py` `ROOT`). `slide_probe.py`'s `parents[1]` stayed valid because `deck_core/` is a direct child of the root. Also scrubbed the leftover **"schematics"** docstrings (this corpus was cloned from the `schematics_curated` archetype). First build reproduced the original deck **byte-for-byte** (same 211-part inventory) → extraction faithful.

---

## 1. The public surface — `deck_core.authoring` façade + `table_kit` (output-neutral)

The transcript's "consolidate the public surface" workstream. Two new engine files:

- **`deck_core/authoring.py`** — the **one file a slide author imports**. Re-exports the whole vocabulary (primitives + style tokens + charts + table_kit), grouped, with `__all__` **derived from the imports** (`[n for n in globals() if not n.startswith('_')]`) so it can't drift. **131 public names.** `AUTHORING_API.md` is the categorized quick-ref. Deliberately **off** the surface: `build_pptx` (build layer), `ooxml` (namespaces), `slide_probe`, and (now) `text_metrics`.
- **`deck_core/table_kit.py`** — the repeated table helpers lifted out of ~22 modules: **`edge`, `bd`, `cell`, `rcell`**.

Then **migrated all 40 slide modules** to `from deck_core.authoring import (...)` and deleted their local `edge/bd/cell/rcell` defs. Done with an AST script (precise line ranges, false-friend marker guards, pre-flight check that every name is in `__all__`).

**Two load-bearing facts that made centralization safe:**
- `tcell`/`tcell_rich` default `l_ins=r_ins=t_ins=b_ins=45720` (primitives.py). So the "short" `cell`/`rcell` variants (omit insets → fall to the 45720 default) and the "long" variants (pass 45720 explicitly) emit **identical** OOXML → one canonical helper covers both.
- **GOTCHA — the `mt` false-friend:** `mt()` is NOT identical across its two users. `approach_unit_economics` uses `tpara([], …, end_size=PT(1))` (pins `<a:endParaRPr>` to 1pt); `comparison_vs_ddgs` uses `tpara([], …)` (no `end_size`). An audit wrongly called them identical. The **per-slide byte-diff caught it** (slide 38 grew 7 stray `sz="100"` attrs). Fix: **do not centralize `mt`** — kept local in both modules. Likewise `r()` (per-slide PT10/12/14 size) and `tx()` (matrix one-run) stay **local**. Lesson: only centralize helpers a byte-diff proves identical; verify against a pre-refactor baseline every time.

Verification: rebuild → **all 124 slide+chart parts byte-identical** to baseline. The façade is pure re-export so it returns the same function objects; migrating imports is output-neutral.

---

## 2. Engine slimming (per user directives; output-neutral)

All in slide_factory only. Verified: 121/124 parts byte-identical, the only intended rendered delta being §3.

- **`lib.py` → `_build.py`.** Build plumbing, not authoring. Updated the one real import (`style_library/library/lib.py` → `from deck_core._build import build_pptx`) + all prose refs (incl. stale bare `lib.py` mentions in `charts.py`).
- **Deleted `text_metrics.py`** — relocated, not dropped, because two consumers needed it:
  - `chart_key.py` used `avg_char_width_emu` → **inlined** as a local `_avg_char_width_emu` (`size_pt * 0.50 * 12700`). `chart_key` is build-critical (re-exported by the façade), so this had to land **before** the delete.
  - `slide_probe.py` used `AVG_CHAR_WIDTH_RATIO` / `greedy_wrap` / `estimate_row_heights` → **moved the whole width/row-height model into `slide_probe.py`** (it's the only remaining consumer; the probe is now self-contained). Also repointed the probe's `BODY` box import from the (now-gone) `slide_base_template` to `deck_core.style` directly.
  - `primitives.py` only *mentioned* it in comments → reworded.
- **`slide_base_template.py` → `new_slide.py`** — replaced the 188-line guided template with a **tiny skeleton** that says "copy an exemplar." (User pushed back on a first draft that still embedded too much guidance — the starter must be minimal; the exemplars are the teacher.)
- **Deleted `slide_guide.md` + `slide_snippets.md`** — scrubbed every dangling `slide_guide`/`slide_snippets` pointer from `style.py`/`charts.py`/`primitives.py`/`README.md`. (Note: the transcript advised *keeping* `slide_guide.md`; user overrode. Originals survive in `ooxml_build_pipelines_light/deck_core/` if ever needed.)
- **`target_copy` references** removed from `style.py` (+ `primitives.py`/`charts.py` for consistency — `target_copy.txt` isn't in slide_factory, so all such refs were already dangling).

---

## 3. House style — **"Source" is always singular**

Per the user: the source-line label is **singular "Source"** no matter how many sources. The rendered slides were already mostly singular (transcribed verbatim), so this is mainly a convention surface:
- `primitives.py` `sources_line()` now emits shape `name="Source"` and its docstring illustrates `"Source: …; …"`.
- `new_slide.py` `_SOURCES = "Source: …; …"`.
- `slide_probe.py` `CHROME_SP_IDS[9999] = "Source"`.

This is the **one intended rendered change** of the whole §1–2 refactor — it altered exactly the 3 slides that call `sources_line()` (`comparison_vs_ddgs`, `ships_act_volume`, `ships_act_plus_volume`), each by a single removed `s` in the shape-name attr; all other slides stayed byte-identical. The shared deck_core still says "Sources" — divergence is intentional.

---

## 4. Teaching exemplars — the same slide authored four ways (render order, front of deck)

The start of the transcript's role-based teaching-rewrite workstream. Added these at the **front** of `SLIDE_RENDERS` (a "Teaching exemplars (render first)" block in `slides/__init__.py`). Current order:

1. **`us_delivery_capacity_teaching_factory_chart`** — chart via the native **`column_chart(mode="stacked", **CHART_STYLE)`** factory. **No template, no `_src`**; style is all Python params (categories/series/colors/axis min-max-major/`gap_width`/`plot_layout`/hidden cat labels) and it **generates its own editable `.xlsx`**. Practical rebuild, not a byte port (its own FIDELITY NOTE).
2. **`us_delivery_capacity_teaching_inline_chart`** — `styled_chart()` with the chart-style **XML template inline** (raw string) and the **workbook inline** (base64 → `base64.b64decode`). No `_src` dependency.
3. **`us_delivery_capacity_teaching`** — `styled_chart()` loading template + workbook from shared **`_src/slide53_chart32.{xml,xlsb}`**.
4. **`addressable_demand_teaching`** — pure **table/text-box** exemplar (`CHARTS=[]`, no chart, no image, no `_src`); criteria chips + rationale column + one-cell native `TierSpine_*` label tables.

(The source-faithful `us_delivery_capacity.py` remains further down the deck — a fifth point of comparison.) The first three render the **identical** forecast slide; they differ only in **where the chart's style/workbook assets live**.

**`styled_chart` mental model** (came up repeatedly): three pieces in three places — **data** inline (`_CHART0_DATA` dict), **style** in the `_CHART0_TPL` template, **workbook** in `_XLSB0`. The chart **renders from the caches** `styled_chart` rewrites from `_CHART0_DATA`; the `.xlsb` is reattached only so PowerPoint "Edit Data" works, and it holds the *original* numbers (can go stale if `_CHART0_DATA` is edited to differ). The **factory** route instead builds caches **and** a fresh workbook from the Python spec, so "Edit Data" is always correct.

**Caveat carried by all four teaching modules** (not yet reconciled — see §7): they import straight from `deck_core.primitives/charts/style`, **not** the `authoring` façade, and each carries its own local `edge`/`border_dict`/`rich_cell` kit (their own comments say "move to `deck_core.table_kit` when you centralize" — which §1 did).

---

## 5. The factory-chart data-label fix (stacked charts can't put labels above bars)

User: in the **factory** variant only, the first three labels (`1`/`2`/`2` for 2026–2028) sat **ON** the column instead of **above** it.

**Root cause:** `charts._build_series` defaults `dlbl_pos="outEnd"`, but **`outEnd` is illegal for a *stacked* column series** (OOXML allows only `ctr`/`inEnd`/`inBase`), so PowerPoint silently centers them on the bar. The `styled_chart` variants dodge this because label positions are baked into the source template.

**Fix (module-only, no engine change):** set the Saronic series to **`hide_labels: True`** (chart now emits **zero** native data labels — verified `0` `outEnd`, `0` `<c:dLbls>` in `chart1.xml`) and add the three values as **manual text boxes above the bars**, extending the existing `DELIVERY_TOTAL_LABELS` pattern backward: y = `bar_top − 0.195"` (the offset the later totals use), x stepping `0.339"/yr` back from the 2029 `"12"` label → `(0.983, 4.783)"1"`, `(1.322, 4.766)"2"`, `(1.661, 4.766)"2"`. Slide 1 now carries **25** uniform bar-top labels. Geometry derived from the plot rect (CHART_FRAME × `plot_layout`, value axis 0–180) and validated against the existing labels.

---

## 6. Current `deck_core/` inventory & how it diverges from the shared engine

```
deck_core/
  authoring.py        ← public façade (131 names)         [NEW]
  AUTHORING_API.md    ← categorized quick-ref             [NEW]
  table_kit.py        ← edge/bd/cell/rcell                [NEW]
  new_slide.py        ← tiny starter skeleton             [NEW, replaces slide_base_template.py]
  primitives.py  charts.py  chart_key.py  style.py  ooxml.py
  _build.py           ← was lib.py
  slide_probe.py      ← now carries the text/row-height model
  __init__.py
```

**Diverged from `ooxml_build_pipelines_light/deck_core/` (do NOT port these back — other projects depend on the shared one):** the `authoring`/`table_kit` façade, `lib→_build`, `text_metrics` deletion, `slide_base_template→new_slide`, the deleted `slide_guide.md`/`slide_snippets.md`, the scrubbed `target_copy`/doc pointers, and the singular-**Source** rule.

---

## 7. Deferred / next

From the transcript, still open:
- **Role-based exemplar reorg** into the 10 job buckets (orient → define-scope → explain-method → bridge-metric → baseline → compare → forecast → system/value-flow → inputs/assumptions → synthesize) + searchable `role/visual/text_fit` tags + an index. (The teaching exemplars in §4 are the *content* seed for this.)
- **Fit Atlas** — exemplar-derived text-fit references to replace `text_metrics`-as-authoring-guide (text_metrics is now demoted to the probe's internal model; the Atlas is the real replacement).
- **Align the §4 teaching modules to the façade + shared `table_kit`** (drop their direct submodule imports + local table kits) so the corpus is uniform — a one-pass cleanup once the variant comparison is settled.

**Verification methodology to reuse:** snapshot every `ppt/slides/slideN.xml` + `ppt/charts/*` from a pre-change build into scratch, then `zipfile` byte-diff after each change. Output-neutral refactors must diff clean; intended changes must isolate to exactly the expected parts. This is what caught the `mt` false-friend (§1) and confirmed the §2–3 slim-down touched nothing but the singular-Source label.
