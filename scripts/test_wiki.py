#!/usr/bin/env python3
"""Tests for check_wiki.py and wiki_search.py.

Run via: uv run python -m unittest discover -s scripts -p 'test_wiki.py'

All tests use tmp-dir fixtures for isolation — they never depend on the seeded
research/wiki/ content.
"""

from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

import check_wiki
import wiki_search


# --- fixture helpers ---------------------------------------------------------

VALID_PAGE = """---
slug: {slug}
title: {title}
type: {type}
aliases: {aliases}
tags: [alpha, beta]
summary: {summary}
created_at: 2026-05-24
updated_at: 2026-05-24
sources:
  - {{title: "ARA daily digest", path: research/digest/2026-05-24-digest.md}}
---

Body for {slug}. {body}
"""

SUBDIR = {"entity": "entities", "concept": "concepts", "theme": "themes"}


def make_wiki(tmp: Path) -> Path:
    """Create an empty wiki skeleton (subdirs + minimal index/log)."""
    root = tmp / "wiki"
    for sub in check_wiki.PAGE_SUBDIRS:
        (root / sub).mkdir(parents=True, exist_ok=True)
    return root


def write_page(
    root: Path,
    slug: str,
    *,
    type_: str = "entity",
    title: str | None = None,
    aliases: str = "[]",
    summary: str = "A one-line summary.",
    body: str = "No links here.",
    subdir: str | None = None,
    filename: str | None = None,
) -> Path:
    sub = subdir or SUBDIR[type_]
    fname = filename or f"{slug}.md"
    path = root / sub / fname
    path.write_text(
        VALID_PAGE.format(
            slug=slug,
            title=title or slug.title(),
            type=type_,
            aliases=aliases,
            summary=summary,
            body=body,
        ),
        encoding="utf-8",
    )
    return path


def write_index(root: Path, entities=(), concepts=(), themes=()) -> Path:
    lines = ["# Wiki Index", ""]
    for header, slugs in (("Entities", entities), ("Concepts", concepts), ("Themes", themes)):
        lines.append(f"## {header}")
        for slug in slugs:
            lines.append(f"- [[{slug}]] — summary for {slug}")
        lines.append("")
    path = root / "index.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_log(root: Path, lines=None) -> Path:
    if lines is None:
        lines = ["## [2026-05-24] seed | seeded pages"]
    path = root / "log.md"
    path.write_text("# Wiki Log\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    return path


def run_validate(root: Path, *, lint: bool = False, today: date | None = None) -> check_wiki.Report:
    targets = check_wiki.gather_pages(root)
    report = check_wiki.Report()
    check_wiki.validate(targets, root, report, lint=lint, today=today)
    return report


def fail_fields(report: check_wiki.Report) -> set[str]:
    return {f.field for f in report.failures}


# --- check_wiki: the happy path ---------------------------------------------


class ValidPageTest(unittest.TestCase):
    def test_minimal_valid_corpus_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="entity", body="Links to [[beta]].")
            write_page(root, "beta", type_="concept", body="Links to [[alpha]].")
            write_index(root, entities=["alpha"], concepts=["beta"])
            write_log(root)
            report = run_validate(root)
            self.assertTrue(report.ok(), msg=[f.__dict__ for f in report.failures])

    def test_flow_style_aliases_and_sources_accepted(self):
        # Mirrors the canonical nebius.md: flow-style list + inline mapping.
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            p = root / "entities" / "nbx.md"
            p.write_text(
                """---
slug: nbx
title: NBX Group
type: entity
aliases: [NBX, "N.B.X. Group"]
tags: [neocloud, gpu-cloud]
summary: Flow-style frontmatter must parse.
created_at: 2026-05-24
updated_at: 2026-05-24
sources:
  - {title: "Q1 results", url: "https://example.com/q1", date: 2026-05-20}
  - {title: "ARA digest", path: research/digest/2026-05-24-digest.md}
---

Body with no wikilinks; just prose to exercise flow-style frontmatter parsing.
""",
                encoding="utf-8",
            )
            write_index(root, entities=["nbx"])
            write_log(root)
            report = run_validate(root)
            self.assertTrue(report.ok(), msg=[f.__dict__ for f in report.failures])


# --- check_wiki: per-file failure modes -------------------------------------


class FrontmatterFailureTest(unittest.TestCase):
    def _one_page_report(self, build) -> check_wiki.Report:
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            build(root)
            write_log(root)
            return run_validate(root)

    def test_missing_required_field_fails(self):
        # Drop `summary` (required).
        def build(root):
            p = root / "entities" / "alpha.md"
            p.write_text(
                "---\nslug: alpha\ntitle: Alpha\ntype: entity\n"
                "created_at: 2026-05-24\nupdated_at: 2026-05-24\n---\n\nBody.\n",
                encoding="utf-8",
            )
            write_index(root, entities=["alpha"])

        report = self._one_page_report(build)
        self.assertFalse(report.ok())
        self.assertIn("summary", fail_fields(report))

    def test_bad_slug_fails(self):
        def build(root):
            # Underscore is illegal; file named to match the bad slug so the
            # slug-regex error is what fires.
            write_page(root, "bad_slug", filename="bad_slug.md")
            write_index(root)

        report = self._one_page_report(build)
        self.assertFalse(report.ok())
        self.assertIn("slug", fail_fields(report))

    def test_slug_not_matching_stem_fails(self):
        def build(root):
            # Valid slug, but filename stem differs.
            write_page(root, "alpha", filename="different.md")
            write_index(root)

        report = self._one_page_report(build)
        self.assertFalse(report.ok())
        self.assertIn("slug", fail_fields(report))
        self.assertTrue(any("must match slug" in f.msg for f in report.failures))

    def test_bad_type_enum_fails(self):
        def build(root):
            write_page(root, "alpha", type_="entity")
            # Rewrite with an illegal type but keep it in entities/.
            (root / "entities" / "alpha.md").write_text(
                "---\nslug: alpha\ntitle: Alpha\ntype: widget\n"
                "summary: x\ncreated_at: 2026-05-24\nupdated_at: 2026-05-24\n---\n\nBody.\n",
                encoding="utf-8",
            )
            write_index(root, entities=["alpha"])

        report = self._one_page_report(build)
        self.assertFalse(report.ok())
        self.assertIn("type", fail_fields(report))

    def test_type_subdir_mismatch_fails(self):
        def build(root):
            # type=concept but file placed in entities/.
            write_page(root, "alpha", type_="concept", subdir="entities")
            write_index(root, concepts=["alpha"])

        report = self._one_page_report(build)
        self.assertFalse(report.ok())
        self.assertTrue(any("pages live in" in f.msg for f in report.failures))

    def test_updated_before_created_fails(self):
        def build(root):
            p = root / "entities" / "alpha.md"
            p.write_text(
                "---\nslug: alpha\ntitle: Alpha\ntype: entity\nsummary: x\n"
                "created_at: 2026-05-24\nupdated_at: 2026-05-01\n---\n\nBody.\n",
                encoding="utf-8",
            )
            write_index(root, entities=["alpha"])

        report = self._one_page_report(build)
        self.assertFalse(report.ok())
        self.assertIn("updated_at", fail_fields(report))

    def test_bad_date_format_fails(self):
        def build(root):
            p = root / "entities" / "alpha.md"
            p.write_text(
                "---\nslug: alpha\ntitle: Alpha\ntype: entity\nsummary: x\n"
                'created_at: "05/24/2026"\nupdated_at: 2026-05-24\n---\n\nBody.\n',
                encoding="utf-8",
            )
            write_index(root, entities=["alpha"])

        report = self._one_page_report(build)
        self.assertFalse(report.ok())
        self.assertIn("created_at", fail_fields(report))

    def test_empty_body_fails(self):
        def build(root):
            p = root / "entities" / "alpha.md"
            p.write_text(
                "---\nslug: alpha\ntitle: Alpha\ntype: entity\nsummary: x\n"
                "created_at: 2026-05-24\nupdated_at: 2026-05-24\n---\n\n   \n",
                encoding="utf-8",
            )
            write_index(root, entities=["alpha"])

        report = self._one_page_report(build)
        self.assertFalse(report.ok())
        self.assertIn("body", fail_fields(report))

    def test_multiline_summary_fails(self):
        def build(root):
            p = root / "entities" / "alpha.md"
            p.write_text(
                "---\nslug: alpha\ntitle: Alpha\ntype: entity\n"
                "summary: |\n  line one\n  line two\n"
                "created_at: 2026-05-24\nupdated_at: 2026-05-24\n---\n\nBody.\n",
                encoding="utf-8",
            )
            write_index(root, entities=["alpha"])

        report = self._one_page_report(build)
        self.assertFalse(report.ok())
        self.assertIn("summary", fail_fields(report))

    def test_bad_source_missing_title_fails(self):
        def build(root):
            p = root / "entities" / "alpha.md"
            p.write_text(
                "---\nslug: alpha\ntitle: Alpha\ntype: entity\nsummary: x\n"
                "created_at: 2026-05-24\nupdated_at: 2026-05-24\n"
                "sources:\n  - {url: \"https://example.com\"}\n---\n\nBody.\n",
                encoding="utf-8",
            )
            write_index(root, entities=["alpha"])

        report = self._one_page_report(build)
        self.assertFalse(report.ok())
        self.assertIn("sources", fail_fields(report))


# --- check_wiki: corpus-level failure modes ---------------------------------


class CorpusFailureTest(unittest.TestCase):
    def test_duplicate_slug_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            # Same slug in two different subdirs.
            write_page(root, "alpha", type_="entity")
            write_page(root, "alpha", type_="concept")
            write_index(root, entities=["alpha"], concepts=["alpha"])
            write_log(root)
            report = run_validate(root)
            self.assertFalse(report.ok())
            self.assertTrue(any("collides" in f.msg for f in report.failures))

    def test_alias_collides_with_other_slug_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="entity")
            # beta declares alias "alpha" — collides with alpha's slug.
            write_page(root, "beta", type_="concept", aliases="[alpha]")
            write_index(root, entities=["alpha"], concepts=["beta"])
            write_log(root)
            report = run_validate(root)
            self.assertFalse(report.ok())
            self.assertTrue(any("collides" in f.msg for f in report.failures))

    def test_broken_link_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="entity", body="Links to [[ghost]].")
            write_index(root, entities=["alpha"])
            write_log(root)
            report = run_validate(root)
            self.assertFalse(report.ok())
            self.assertIn("links", fail_fields(report))

    def test_link_resolves_via_alias(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="entity", aliases='["Alpha Corp"]')
            # Link by alias (with different case) must resolve.
            write_page(root, "beta", type_="concept", body="See [[alpha corp]].")
            write_index(root, entities=["alpha"], concepts=["beta"])
            write_log(root)
            report = run_validate(root)
            self.assertTrue(report.ok(), msg=[f.__dict__ for f in report.failures])

    def test_link_inside_fenced_code_is_ignored(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            body = "Real link [[beta]].\n\n```\nExample: [[not-a-real-page]]\n```\n"
            write_page(root, "alpha", type_="entity", body=body)
            write_page(root, "beta", type_="concept", body="Back to [[alpha]].")
            write_index(root, entities=["alpha"], concepts=["beta"])
            write_log(root)
            report = run_validate(root)
            # [[not-a-real-page]] is inside a fence → must NOT be flagged.
            self.assertTrue(report.ok(), msg=[f.__dict__ for f in report.failures])


# --- check_wiki: index.md / log.md ------------------------------------------


class IndexLogFailureTest(unittest.TestCase):
    def test_index_missing_page_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="entity")
            write_page(root, "beta", type_="entity")
            # Only alpha listed; beta missing.
            write_index(root, entities=["alpha"])
            write_log(root)
            report = run_validate(root)
            self.assertFalse(report.ok())
            self.assertTrue(any("not listed in the index" in f.msg for f in report.failures))

    def test_index_lists_nonexistent_slug_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="entity")
            write_index(root, entities=["alpha", "ghost"])
            write_log(root)
            report = run_validate(root)
            self.assertFalse(report.ok())
            self.assertTrue(any("has no page file" in f.msg for f in report.failures))

    def test_index_wrong_section_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="concept")
            # concept listed under Entities.
            write_index(root, entities=["alpha"])
            write_log(root)
            report = run_validate(root)
            self.assertFalse(report.ok())
            self.assertTrue(any("belongs under" in f.msg for f in report.failures))

    def test_bad_log_line_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="entity")
            write_index(root, entities=["alpha"])
            # Missing the ' | summary' segment.
            write_log(root, lines=["## [2026-05-24] seed no-pipe-here"])
            report = run_validate(root)
            self.assertFalse(report.ok())
            self.assertIn("log", fail_fields(report))

    def test_bad_log_op_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="entity")
            write_index(root, entities=["alpha"])
            write_log(root, lines=["## [2026-05-24] frobnicate | did a thing"])
            report = run_validate(root)
            self.assertFalse(report.ok())
            self.assertTrue(any("must be one of" in f.msg for f in report.failures))

    def test_out_of_order_log_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="entity")
            write_index(root, entities=["alpha"])
            write_log(
                root,
                lines=[
                    "## [2026-05-24] seed | first",
                    "## [2026-05-20] ingest | earlier date after later one",
                ],
            )
            report = run_validate(root)
            self.assertFalse(report.ok())
            self.assertTrue(any("out of order" in f.msg for f in report.failures))


# --- check_wiki: lint mode ---------------------------------------------------


class LintModeTest(unittest.TestCase):
    def test_lint_reports_orphan_but_does_not_fail(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            # gamma has no inbound links.
            write_page(root, "alpha", type_="entity", body="Links to [[beta]].")
            write_page(root, "beta", type_="concept", body="Links to [[alpha]].")
            write_page(root, "gamma", type_="theme", body="Links to [[alpha]].")
            write_index(root, entities=["alpha"], concepts=["beta"], themes=["gamma"])
            write_log(root)
            report = run_validate(root, lint=True)
            # Lint is advisory: corpus is otherwise valid → no hard failures.
            self.assertTrue(report.ok(), msg=[f.__dict__ for f in report.failures])
            kinds = {w.kind for w in report.warnings}
            self.assertIn("orphan", kinds)
            self.assertTrue(any(w.kind == "orphan" and "gamma" in w.msg for w in report.warnings))

    def test_lint_reports_stale(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="entity", body="Links to [[beta]].")
            write_page(root, "beta", type_="concept", body="Links to [[alpha]].")
            write_index(root, entities=["alpha"], concepts=["beta"])
            write_log(root)
            # Pages are dated 2026-05-24; pretend "today" is far later.
            report = run_validate(root, lint=True, today=date(2026, 12, 31))
            kinds = {w.kind for w in report.warnings}
            self.assertIn("stale", kinds)

    def test_lint_cli_always_exits_zero_even_with_hard_failures(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            # Broken link = hard failure in normal mode.
            write_page(root, "alpha", type_="entity", body="Links to [[ghost]].")
            write_index(root, entities=["alpha"])
            write_log(root)
            page = root / "entities" / "alpha.md"
            rc = check_wiki.main([str(page), "--root", str(root), "--lint"])
            self.assertEqual(rc, 0)

    def test_normal_mode_cli_exits_one_on_failure(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(root, "alpha", type_="entity", body="Links to [[ghost]].")
            write_index(root, entities=["alpha"])
            write_log(root)
            page = root / "entities" / "alpha.md"
            rc = check_wiki.main([str(page), "--root", str(root)])
            self.assertEqual(rc, 1)


# --- wiki_search -------------------------------------------------------------


class WikiSearchTest(unittest.TestCase):
    def _seed(self, root: Path) -> None:
        write_page(
            root,
            "nebius",
            type_="entity",
            title="Nebius Group",
            aliases="[Nebius, NBIS]",
            summary="Amsterdam neocloud provider for GPU compute.",
            body="Nebius rents GPU capacity. It competes with CoreWeave.",
        )
        write_page(
            root,
            "coreweave",
            type_="entity",
            title="CoreWeave",
            summary="GPU-as-a-service neocloud with a large backlog.",
            body="CoreWeave is the reference neocloud. Mentions nebius once.",
        )
        write_page(
            root,
            "neocloud",
            type_="concept",
            title="Neocloud",
            summary="Buy GPUs on debt, rent capacity back.",
            body="The neocloud model underwrites debt against contracts.",
        )

    def test_targeted_query_ranks_right_page_first(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            self._seed(root)
            results = wiki_search.search(root, "nebius")
            self.assertTrue(results)
            self.assertEqual(results[0]["slug"], "nebius")

    def test_alias_query_matches(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            self._seed(root)
            results = wiki_search.search(root, "NBIS")
            self.assertTrue(results)
            self.assertEqual(results[0]["slug"], "nebius")

    def test_concept_query_ranks_concept_first(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            self._seed(root)
            results = wiki_search.search(root, "neocloud model debt")
            self.assertTrue(results)
            self.assertEqual(results[0]["slug"], "neocloud")

    def test_top_limits_results(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            self._seed(root)
            results = wiki_search.search(root, "gpu", top=1)
            self.assertLessEqual(len(results), 1)

    def test_no_match_returns_empty(self):
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            self._seed(root)
            results = wiki_search.search(root, "zzzznonexistentzzz")
            self.assertEqual(results, [])

    def test_fenced_code_excluded_from_index(self):
        # A term only present inside a code fence should not make a page match.
        with tempfile.TemporaryDirectory() as td:
            root = make_wiki(Path(td))
            write_page(
                root,
                "alpha",
                type_="entity",
                title="Alpha",
                summary="No special terms.",
                body="Normal text.\n\n```\nquxzzytoken here\n```\n",
            )
            results = wiki_search.search(root, "quxzzytoken")
            self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
