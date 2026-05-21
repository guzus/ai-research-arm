#!/usr/bin/env python3

import tempfile
import unittest
import json
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import compile_ara
import write_generative_research as writer


def compile_ok(body: str) -> str:
    return compile_ara.compile_source(body)


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
