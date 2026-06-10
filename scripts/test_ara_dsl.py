#!/usr/bin/env python3

import tempfile
import unittest
import json
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import ara_catalog
import compile_ara
import write_generative_research as writer


def compile_ok(body: str) -> str:
    return compile_ara.compile_source(body)


def compile_newspaper_ok(body: str) -> str:
    return compile_ara.compile_source(body, target="newspaper")


class AraCatalogTest(unittest.TestCase):
    def test_catalog_matches_component_reference_classes(self):
        self.assertEqual([], ara_catalog.validate_catalog_against_components())

    def test_writer_loads_classes_from_catalog(self):
        writer._VALID_CLASSES_CACHE = None
        classes = writer.load_valid_classes()
        self.assertIn("ara-doc", classes)
        self.assertIn("ara-bar-chart", classes)
        self.assertNotIn("ara-grid", classes)


class AraDslTest(unittest.TestCase):
    def test_requires_frontmatter_title(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "frontmatter.*title"):
            compile_ok(
                """## 01. Missing title

Text.

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_cited_articles_require_references_block(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "references"):
            compile_ok(
                """---
title: No refs
---

## 01. Body

Claim [^1].
"""
            )

    def test_citation_must_match_reference(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "missing from :::references: 99"):
            compile_ok(
                """---
title: Bad cite
---

## 01. Body

Claim [^99].

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_duplicate_reference_ids_fail(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "duplicate reference"):
            compile_ok(
                """---
title: Duplicate refs
---

## 01. Body

Claim [^1].

:::references
- {id: 1, title: One}
- {id: 1, title: Again}
:::
"""
            )

    def test_references_must_be_last(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "references must be the final block"):
            compile_ok(
                """---
title: Refs order
---

## 01. Body

Claim [^1].

:::references
- {id: 1, title: Source}
:::

Trailing paragraph.
"""
            )

    def test_malformed_directive_opener_fails(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "invalid directive opener"):
            compile_ok(
                """---
title: Bad directive
---

## 01. Body

Claim [^1].

:::callout(label="unterminated)
Body
:::

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_malformed_slope_raises_syntax_error(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "slope table rows"):
            compile_ok(
                """---
title: Bad slope
---

## 01. Bad slope

Claim [^1].

:::slope(left-label=2020, right-label=2026)
| Item | 2020 | 2026 |
|------|------|------|
| A | 1 |
:::

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_chart_series_lengths_are_validated(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "has 3 values but x has 2 labels"):
            compile_ok(
                """---
title: Bad chart
---

## 01. Bad chart

Claim [^1].

:::line-chart
x: Jan,Feb
A: 1,2,3
:::

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_chart_values_must_be_numeric(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "expected a number"):
            compile_ok(
                """---
title: Bad chart
---

## 01. Bad chart

Claim [^1].

:::line-chart
x: Jan,Feb
A: nope,2
:::

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_bar_chart_vertical_stacked_emits_data_attrs(self):
        html = compile_ok(
            """---
title: Bar chart stacked
---

## 01. Revenue

Claim [^1].

:::bar-chart(title="Revenue by segment", orientation=vertical, mode=stacked, value-unit=$, value-suffix=B)
categories: FY 2023, FY 2024, FY 2025, Q1 2026
Connectivity (Starlink): 0, 0, 11.5, 3.2
Space: 0, 0, 3.0, 0.6
:::

:::references
- {id: 1, title: Source}
:::
"""
        )
        self.assertIn('class="ara-bar-chart"', html)
        self.assertIn('data-orientation="vertical"', html)
        self.assertIn('data-mode="stacked"', html)
        self.assertIn('data-categories="FY 2023,FY 2024,FY 2025,Q1 2026"', html)
        self.assertIn('data-series-1="0,0,11.5,3.2"', html)
        self.assertIn('data-series-1-label="Connectivity (Starlink)"', html)
        self.assertIn('data-series-2="0,0,3,0.6"', html)
        self.assertIn('data-unit="$"', html)
        self.assertIn('data-value-suffix="B"', html)

    def test_exhibit_wraps_nested_chart_with_single_wordmark(self):
        html = compile_ok(
            """---
title: Exhibit test
---

## 01. Exhibits

:::exhibit(num="Exhibit 1", title="Revenue by segment", subtitle="$ billion", source="Company filings", note="FY ends December.")
:::bar-chart(title="Revenue", orientation=vertical, value-unit=$, value-suffix=B)
categories: FY24, FY25
A: 10, 14
:::
:::
"""
        )
        # Frame parts present.
        self.assertIn('class="ara-exhibit"', html)
        self.assertIn('<span class="ara-exhibit-num">Exhibit 1</span>', html)
        self.assertIn('<div class="ara-exhibit-title">Revenue by segment</div>', html)
        self.assertIn('<div class="ara-exhibit-subtitle">$ billion</div>', html)
        self.assertIn('class="ara-exhibit-body"', html)
        # Nested chart compiled inside the body.
        self.assertIn('class="ara-bar-chart"', html)
        # Attribute-driven note + source rendered.
        self.assertIn('<span class="ara-note-label">Note</span>', html)
        self.assertIn('<span class="ara-source-label">Source</span>', html)
        # Exactly one wordmark per exhibit (no doubling).
        self.assertEqual(html.count('class="ara-wordmark"'), 1)

    def test_exhibit_accepts_nested_note_and_source_blocks(self):
        html = compile_ok(
            """---
title: Exhibit nested footnotes
---

## 01. Exhibits

:::exhibit(num="Exhibit 2", title="Share")
:::donut(center-label="100%")
- {label: One, value: 60}
- {label: Two, value: 40}
:::
:::note
A nested note with **markup**.
:::
:::source
A nested source line.
:::
:::
"""
        )
        self.assertIn('class="ara-donut"', html)
        self.assertIn('class="ara-note"', html)
        self.assertIn('class="ara-source"', html)
        self.assertEqual(html.count('class="ara-wordmark"'), 1)

    def test_exhibit_wordmark_can_be_suppressed(self):
        html = compile_ok(
            """---
title: Exhibit no wordmark
---

## 01. Exhibits

:::exhibit(num="Exhibit 3", title="Plain", wordmark=false)
:::bars
- {label: A, value: "60%", pct: 60}
:::
:::
"""
        )
        self.assertNotIn('class="ara-wordmark"', html)

    def test_statement_and_change_bubble_and_cols(self):
        html = compile_ok(
            """---
title: Statement and bubble
---

## 01. Body

Up {bubble:+12%} and down {bubble:-8%}.

:::statement(attr="ARA Research")
The compute keeps getting cheaper.
:::

:::cols
Paragraph one of the dense prose.

Paragraph two of the dense prose.
:::
"""
        )
        self.assertIn('class="ara-statement"', html)
        self.assertIn('<span class="ara-statement-attr">ARA Research</span>', html)
        self.assertIn('class="ara-bubble ara-bubble--up">+12%</span>', html)
        self.assertIn('class="ara-bubble ara-bubble--down">-8%</span>', html)
        self.assertIn('class="ara-cols"', html)

    def test_note_source_labels_can_be_omitted(self):
        html = compile_ok(
            """---
title: Bare footnote
---

## 01. Body

:::source(label="")
Raw provenance with no prefix label.
:::
"""
        )
        self.assertIn('class="ara-source"', html)
        self.assertNotIn('ara-source-label', html)

    def test_newspaper_target_emits_interactive_components(self):
        html = compile_newspaper_ok(
            """---
title: THE AGI AWARENESS POST
date: May 28, 2026
edition: All Sources Edition
volume: 2026
number: 149
---

:::paper-index
- {label: Lead, target: "#lead-top"}
- {label: Signals, target: "#meter-signals"}
:::

:::lead(id="lead-top", label="Top Story", title="Models move into production")
The day opens with ==production AI== pressure across labs.
:::

:::briefs(title="Breaking", columns=2)
- {headline: New model ships, tag: Models, body: Early customers report lower latency.}
- {headline: Regulator opens inquiry, tag: Policy}
:::

:::news-meter(id="meter-signals", title="Signal Mix")
- {label: Breaking, value: 75, display: "3 items", tone: hot}
- {label: Research, value: 40, max: 80, display: "2 papers", tone: research}
:::

:::story-deck(title="Departments")
- {headline: Models & Systems, summary: Release notes and benchmarks., meta: "3 items", tone: watch}
:::
"""
        )
        self.assertIn('class="ara-paper"', html)
        self.assertIn('class="ara-paper-toggle"', html)
        self.assertIn('aria-expanded="true"', html)
        self.assertIn('class="ara-paper-brief"', html)
        self.assertIn('class="ara-paper-meter-fill" data-pct="75"', html)
        self.assertIn('class="ara-paper-meter-fill" data-pct="50"', html)
        self.assertIn('class="ara-paper-story ara-paper-story--watch"', html)
        self.assertNotIn('class="ara-doc"', html)

    def test_newspaper_meter_rejects_out_of_range_values(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "0-100 percent"):
            compile_newspaper_ok(
                """---
title: Bad Paper
---

:::news-meter(title="Signals")
- {label: Broken, value: 101}
:::
"""
            )

    # --- Newspaper defense-in-depth validator (validate_newspaper_body) ---
    # compile_newspaper_source returns WITHOUT the article path's
    # FRAGMENT_ALLOWED_TAGS allowlist (it legitimately emits
    # <nav>/<button>/<details>/aria-*), so a denylist guards against the
    # dangerous constructs the trusted compiler never emits.

    def test_real_front_page_sources_still_compile(self):
        # Strongest non-breaking guard: compile EVERY committed front-page
        # newspaper source and assert the validator passes it. The front-page
        # output legitimately uses <nav>/<button>/<details>/<summary> +
        # aria-*/type/data-columns; the validator must not reject any of it.
        repo_root = Path(compile_ara.__file__).resolve().parent.parent
        sources = sorted((repo_root / "research" / "front-page").glob("*.ara.md"))
        self.assertGreater(len(sources), 0, "expected committed front-page .ara.md sources")
        for src in sources:
            with self.subTest(source=src.name):
                html = compile_ara.compile_source(
                    src.read_text(encoding="utf-8"), target="newspaper"
                )
                # Sanity: the legitimate interactive tags are present and kept.
                self.assertIn("<nav", html)
                self.assertIn("<button", html)
                self.assertIn("<details", html)
                self.assertIn('aria-expanded="true"', html)

    def test_newspaper_validator_passes_clean_interactive_output(self):
        # The full interactive newspaper fixture must pass end to end.
        html = compile_newspaper_ok(
            """---
title: Clean Paper
date: May 28, 2026
---

:::paper-index
- {label: Lead, target: "#lead-top"}
:::

:::lead(id="lead-top", label="Top Story", title="Models move into production")
The day opens with ==production AI== pressure.
:::

:::briefs(title="Breaking", columns=2)
- {headline: New model ships, tag: Models, body: Lower latency.}
:::

:::news-meter(title="Signal Mix")
- {label: Breaking, value: 75, display: "3 items", tone: hot}
:::
"""
        )
        self.assertIn('class="ara-paper"', html)
        # Idempotent: re-validating the already-compiled output is a no-op.
        compile_ara.validate_newspaper_body(html)

    def test_newspaper_validator_rejects_script_tag(self):
        # The gap the denylist closes: DISALLOWED_PATTERNS (style=/on*=/
        # javascript:) does NOT match a bare <script> tag. The tag patterns do.
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "disallowed pattern"):
            compile_ara.validate_newspaper_body(
                '<article class="ara-paper"><script>alert(1)</script></article>'
            )

    def test_newspaper_validator_rejects_style_and_iframe_tags(self):
        with self.assertRaises(compile_ara.AraSyntaxError):
            compile_ara.validate_newspaper_body(
                '<article class="ara-paper"><style>x{}</style></article>'
            )
        with self.assertRaises(compile_ara.AraSyntaxError):
            compile_ara.validate_newspaper_body(
                '<article class="ara-paper"><iframe src="x"></iframe></article>'
            )

    def test_newspaper_validator_rejects_inline_style_and_handlers(self):
        with self.assertRaises(compile_ara.AraSyntaxError):
            compile_ara.validate_newspaper_body(
                '<article class="ara-paper"><div style="color:red">x</div></article>'
            )
        with self.assertRaises(compile_ara.AraSyntaxError):
            compile_ara.validate_newspaper_body(
                '<article class="ara-paper"><button onclick="x()">x</button></article>'
            )
        with self.assertRaises(compile_ara.AraSyntaxError):
            compile_ara.validate_newspaper_body(
                '<article class="ara-paper"><a href="javascript:void(0)">x</a></article>'
            )

    def test_newspaper_validator_allows_legit_interactive_markup(self):
        # The exact tag/attribute shapes the compiler emits must NOT trip the
        # denylist: <nav aria-label>, <button type aria-expanded aria-controls>,
        # <details>/<summary>, <section data-columns>, data-paper-date.
        compile_ara.validate_newspaper_body(
            '<article class="ara-paper" data-paper-date="June 9, 2026">'
            '<nav class="ara-paper-index" aria-label="In this edition"></nav>'
            '<button class="ara-paper-toggle" type="button" aria-expanded="true" '
            'aria-controls="x-body"><span aria-hidden="true">v</span></button>'
            '<section class="ara-paper-briefs" data-columns="2">'
            '<details class="ara-paper-brief"><summary>x</summary></details>'
            "</section></article>"
        )

    def test_bar_chart_horizontal_diverging_keeps_negative(self):
        html = compile_ok(
            """---
title: Bar chart diverging
---

## 01. Margin

Claim [^1].

:::bar-chart(orientation=horizontal, value-unit=$, value-suffix=M)
categories: FY 2023, FY 2024, FY 2025
Operating income: -6800, -1200, 3400
:::

:::references
- {id: 1, title: Source}
:::
"""
        )
        self.assertIn('data-orientation="horizontal"', html)
        self.assertIn('data-series-1="-6800,-1200,3400"', html)
        # No mode attr emitted when mode is omitted.
        self.assertNotIn('data-mode=', html)

    def test_bar_chart_defaults_orientation_vertical(self):
        html = compile_ok(
            """---
title: Bar chart default
---

## 01. Capex

:::bar-chart(value-suffix=B)
categories: 2024, 2025
Capex: 1.2, 3.4
:::
"""
        )
        self.assertIn('data-orientation="vertical"', html)

    def test_bar_chart_series_length_mismatch_raises(self):
        with self.assertRaisesRegex(
            compile_ara.AraSyntaxError,
            "has 3 values but categories has 2 labels",
        ):
            compile_ok(
                """---
title: Bad bar chart
---

## 01. Bad bar chart

Claim [^1].

:::bar-chart
categories: 2024, 2025
A: 1, 2, 3
:::

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_bar_chart_stacked_rejects_negative(self):
        with self.assertRaisesRegex(
            compile_ara.AraSyntaxError,
            "stacked bar-chart cannot have negative values",
        ):
            compile_ok(
                """---
title: Bad stacked
---

## 01. Bad stacked

Claim [^1].

:::bar-chart(mode=stacked)
categories: 2024, 2025
A: 1, -2
:::

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_bar_chart_bad_orientation_raises(self):
        with self.assertRaisesRegex(
            compile_ara.AraSyntaxError,
            "orientation must be vertical",
        ):
            compile_ok(
                """---
title: Bad orientation
---

## 01. Bad orientation

Claim [^1].

:::bar-chart(orientation=diagonal)
categories: 2024, 2025
A: 1, 2
:::

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_percentages_must_be_0_to_100(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "pct must be between 0 and 100"):
            compile_ok(
                """---
title: Bad pct
---

## 01. Bad pct

Claim [^1].

:::bars
- {label: A, value: bad, pct: 999}
:::

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_inline_sparkline_must_be_numeric(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "sparkline: expected a number"):
            compile_ok(
                """---
title: Bad sparkline
---

## 01. Bad sparkline

Claim [^1] {sparkline:1,nope,3}.

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_korean_translation_backfills_existing_index_row(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            gen_dir = repo / "research" / "generative"
            gen_dir.mkdir(parents=True)
            index_path = gen_dir / "index.json"
            index_path.write_text(
                json.dumps(
                    [
                        {
                            "slug": "alpha",
                            "file": "2026-01-01T000000--alpha.html",
                            "kind": "fragment",
                            "language": "en",
                            "title": "Alpha",
                            "model": "seed",
                            "created_at": "2026-01-01T00:00:00Z",
                            "source": "seed",
                            "prompt": "Alpha",
                            "tags": [],
                        }
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            body_path = repo / "ko.html"
            body_path.write_text(
                '<article class="ara-doc"><h2 class="ara-display">알파</h2><p>한국어 본문입니다.</p></article>',
                encoding="utf-8",
            )

            rc = writer.main(
                [
                    "--topic",
                    "Alpha Korean",
                    "--html-body",
                    str(body_path),
                    "--model",
                    "test-model",
                    "--language",
                    "ko",
                    "--translation-of",
                    "alpha",
                    "--repo-root",
                    str(repo),
                    "--no-commit",
                ]
            )

            self.assertEqual(rc, 0)
            data = json.loads(index_path.read_text(encoding="utf-8"))
            self.assertEqual(len(data), 1)
            ko = data[0]["translations"]["ko"]
            self.assertEqual(ko["language"], "ko")
            self.assertEqual(ko["title"], "알파")
            self.assertTrue(ko["file"].endswith("--alpha.ko.html"))
            self.assertTrue((gen_dir / ko["file"]).exists())

    def test_non_ascii_quoted_attributes_survive(self):
        html = compile_ok(
            """---
title: Unicode attrs
---

## 01. Figure

Claim [^1].

:::figure(src=/img/x.png, alt="서울", caption="café")
:::

:::references
- {id: 1, title: Source}
:::
"""
        )
        self.assertIn('alt="서울"', html)
        self.assertIn("café", html)

    def test_tradingview_emits_safe_placeholder(self):
        html = compile_ok(
            """---
title: TradingView
---

## 01. Chart

:::tradingview(symbol="NASDAQ:NOW", interval=D, theme=dark, range=12M)
:::
"""
        )
        self.assertIn('<div class="ara-tradingview"', html)
        self.assertIn('data-symbol="NASDAQ:NOW"', html)
        self.assertIn('data-interval="D"', html)
        self.assertIn('data-theme="dark"', html)
        self.assertIn('data-range="12M"', html)
        self.assertIn(
            '<a class="ara-tradingview-fallback" '
            'href="https://www.tradingview.com/symbols/NASDAQ-NOW/">',
            html,
        )
        # The fragment must stay script-free — the dashboard injects the widget.
        self.assertNotIn("<script", html)
        self.assertNotIn("<iframe", html)

    def test_tradingview_symbol_only_omits_optional_attrs(self):
        html = compile_ok(
            """---
title: TradingView
---

## 01. Chart

:::tradingview(symbol="NYSE:BE")
:::
"""
        )
        self.assertIn('data-symbol="NYSE:BE"', html)
        self.assertNotIn("data-interval", html)
        self.assertNotIn("data-theme", html)
        self.assertNotIn("data-range", html)

    def test_tradingview_passes_fragment_validator(self):
        html = compile_ok(
            """---
title: TradingView
---

## 01. Chart

:::tradingview(symbol="NASDAQ:NOW", interval=W, theme=light, range=5Y)
:::
"""
        )
        # Must survive the writer's fragment validator (allowlisted data-* +
        # the ara-tradingview class). validate_body raises on any violation.
        writer.validate_body(html, writer.KIND_FRAGMENT)

    def test_tradingview_rejects_unsafe_symbol(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "symbol"):
            compile_ok(
                """---
title: TradingView
---

## 01. Chart

:::tradingview(symbol="bad symbol!")
:::
"""
            )

    def test_validator_rejects_trailing_newline_data_symbol(self):
        # Hand-crafted fragment fed straight to validate_body (bypassing the
        # compiler's .strip()). The gate uses \Z, not $ — Python's $ matches
        # before a trailing newline, which would let data-symbol="X\n" slip past
        # and diverge from the compiler's _TV_SYMBOL_RE. This locks in the mirror.
        frag = (
            '<article class="ara-doc"><h2 class="ara-display">T</h2>'
            '<div class="ara-tradingview" data-symbol="NASDAQ:NOW\n"></div>'
            "</article>"
        )
        with self.assertRaises(ValueError):
            writer.validate_body(frag, writer.KIND_FRAGMENT)

    def test_web_figure_emits_safe_image_with_credit(self):
        html = compile_ok(
            """---
title: Web figure
---

## 01. Figure

:::figure(src="https://images.example.com/chart.webp", alt="Chart", caption="Observed trend.", credit="Example Images", source-url="https://example.com/chart", variant=inline)
:::
"""
        )
        self.assertIn('<figure class="ara-figure ara-figure--inline">', html)
        self.assertIn('src="https://images.example.com/chart.webp"', html)
        self.assertIn('loading="lazy" decoding="async" referrerpolicy="no-referrer"', html)
        self.assertIn('<span class="ara-caption-text">Observed trend.</span>', html)
        self.assertIn('<span class="ara-credit">Source: <a href="https://example.com/chart">Example Images</a></span>', html)

    def test_web_figure_rejects_remote_svg(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "remote SVG"):
            compile_ok(
                """---
title: Bad figure
---

## 01. Figure

:::figure(src="https://images.example.com/chart.svg", alt="Chart")
:::
"""
            )

    def test_validator_rejects_raw_remote_svg_img(self):
        body = '<article class="ara-doc"><figure class="ara-figure"><img src="https://example.com/x.svg" alt="x"></figure></article>'
        with self.assertRaisesRegex(ValueError, "disallowed attributes"):
            writer.validate_body(body, writer.KIND_FRAGMENT)

    def test_inline_wrapper_can_contain_link(self):
        html = compile_ok(
            """---
title: Wrapped link
---

## 01. Inline

Claim [^1] from {accent}[the source](https://example.com){/}.

:::references
- {id: 1, title: Source, url: https://example.com}
:::
"""
        )
        self.assertIn('<strong class="ara-accent"><a href="https://example.com">the source</a></strong>', html)

    def test_validator_rejects_forbidden_doc_examples(self):
        body = '<article class="ara-doc"><div class="ara-grid">x</div></article>'
        with self.assertRaisesRegex(ValueError, "undocumented ara-\\* class"):
            writer.validate_body(body, writer.KIND_FRAGMENT)

    def test_validator_rejects_unexpected_attributes(self):
        body = '<article class="ara-doc"><div href="https://example.com">x</div></article>'
        with self.assertRaisesRegex(ValueError, "disallowed attributes"):
            writer.validate_body(body, writer.KIND_FRAGMENT)

    def test_validator_rejects_bad_raw_data_values(self):
        body = '<article class="ara-doc"><div class="ara-bar" data-pct="abc">x</div></article>'
        with self.assertRaisesRegex(ValueError, "disallowed attributes"):
            writer.validate_body(body, writer.KIND_FRAGMENT)

    def test_compile_source_runs_html_backstop_for_raw(self):
        with self.assertRaisesRegex(compile_ara.AraSyntaxError, "HTML validation failed"):
            compile_ok(
                """---
title: Bad raw
---

## 01. Raw

Claim [^1].

:::raw
<div class="ara-grid">bad</div>
:::

:::references
- {id: 1, title: Source}
:::
"""
            )

    def test_compile_cli_validates_raw_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.ara.md"
            path.write_text(
                """---
title: Bad raw
---

## 01. Raw

Claim [^1].

:::raw
<div class="ara-grid">bad</div>
:::

:::references
- {id: 1, title: Source}
:::
""",
                encoding="utf-8",
            )
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                self.assertEqual(compile_ara.main([str(path), "--out", "-"]), 1)


if __name__ == "__main__":
    unittest.main()
