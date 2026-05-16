#!/usr/bin/env python3

import tempfile
import unittest
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
