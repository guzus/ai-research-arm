#!/usr/bin/env python3
"""Tests for the deterministic arXiv fallback writer (fixture-based, no network)."""

from __future__ import annotations

import datetime as dt
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, os.path.dirname(__file__))

import deterministic_arxiv_digest as arxiv  # noqa: E402

NOW = dt.datetime(2026, 7, 2, 6, 15, tzinfo=dt.timezone.utc)


def atom_fixture(entries: str) -> bytes:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom" '
        'xmlns:arxiv="http://arxiv.org/schemas/atom">\n'
        "<title>ArXiv Query Results</title>\n"
        f"{entries}\n"
        "</feed>"
    ).encode("utf-8")


def entry_fixture(
    *,
    arxiv_id: str = "2607.00123v1",
    title: str = "A Paper About Agents",
    published: str = "2026-07-01T17:59:59Z",
    updated: str = "2026-07-01T17:59:59Z",
    primary: str = "cs.AI",
    categories: tuple[str, ...] = ("cs.AI",),
    authors: tuple[str, ...] = ("Alice Ada", "Bob Byte"),
    summary: str = "First sentence of the abstract. Second sentence. Third one here.",
) -> str:
    author_xml = "".join(f"<author><name>{name}</name></author>" for name in authors)
    category_xml = "".join(f'<category term="{term}"/>' for term in categories)
    return (
        "<entry>"
        f"<id>http://arxiv.org/abs/{arxiv_id}</id>"
        f"<updated>{updated}</updated>"
        f"<published>{published}</published>"
        f"<title>{title}</title>"
        f"<summary>{summary}</summary>"
        f"{author_xml}"
        f'<arxiv:primary_category term="{primary}"/>'
        f"{category_xml}"
        f'<link href="http://arxiv.org/abs/{arxiv_id}" rel="alternate" type="text/html"/>'
        "</entry>"
    )


class ParsePapersTest(unittest.TestCase):
    def test_parses_namespaced_atom_entry(self):
        papers = arxiv.parse_papers(atom_fixture(entry_fixture()))

        self.assertEqual(len(papers), 1)
        paper = papers[0]
        self.assertEqual(paper.arxiv_id, "2607.00123v1")
        self.assertEqual(paper.title, "A Paper About Agents")
        self.assertEqual(paper.authors, ("Alice Ada", "Bob Byte"))
        self.assertEqual(paper.category, "cs.AI")
        self.assertEqual(paper.abs_url, "https://arxiv.org/abs/2607.00123v1")
        self.assertEqual(
            paper.published_at,
            dt.datetime(2026, 7, 1, 17, 59, 59, tzinfo=dt.timezone.utc),
        )

    def test_skips_entry_with_no_target_category(self):
        entries = entry_fixture(primary="math.CO", categories=("math.CO",))
        self.assertEqual(arxiv.parse_papers(atom_fixture(entries)), [])

    def test_cross_listed_paper_groups_under_first_target_term(self):
        entries = entry_fixture(primary="stat.ML", categories=("stat.ML", "cs.LG"))
        papers = arxiv.parse_papers(atom_fixture(entries))

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].category, "cs.LG")


class FilterWindowTest(unittest.TestCase):
    def _paper(self, published: dt.datetime) -> arxiv.Paper:
        return arxiv.Paper(
            arxiv_id="2607.00001v1",
            title="t",
            authors=("A",),
            abstract="a",
            category="cs.AI",
            published_at=published,
            updated_at=published,
        )

    def test_keeps_papers_inside_window_and_drops_older(self):
        fresh = self._paper(NOW - dt.timedelta(hours=25))
        stale = self._paper(NOW - dt.timedelta(hours=27))

        kept = arxiv.filter_window([fresh, stale], NOW, lookback_hours=26)

        self.assertEqual(kept, [fresh])

    def test_updated_timestamp_can_qualify_an_old_submission(self):
        paper = arxiv.Paper(
            arxiv_id="2606.09999v2",
            title="t",
            authors=("A",),
            abstract="a",
            category="cs.LG",
            published_at=NOW - dt.timedelta(days=20),
            updated_at=NOW - dt.timedelta(hours=3),
        )
        self.assertEqual(arxiv.filter_window([paper], NOW, 26), [paper])

    def test_missing_timestamps_are_dropped(self):
        paper = arxiv.Paper(
            arxiv_id="x",
            title="t",
            authors=(),
            abstract="",
            category="cs.AI",
            published_at=None,
            updated_at=None,
        )
        self.assertEqual(arxiv.filter_window([paper], NOW, 26), [])


class RenderTest(unittest.TestCase):
    def test_zero_papers_writes_honest_empty_note(self):
        text = arxiv.render("2026-07-02", NOW, 26, [])

        self.assertIn("# arXiv AI Research - 2026-07-02", text)
        self.assertIn("Deterministic model-free fallback", text)
        self.assertIn("No new papers found in the lookback window", text)

    def test_renders_category_sections_and_et_al(self):
        papers = arxiv.parse_papers(
            atom_fixture(
                entry_fixture(
                    authors=("A One", "B Two", "C Three", "D Four"),
                    categories=("cs.AI",),
                )
                + entry_fixture(
                    arxiv_id="2607.00456v1",
                    title="Vision Things",
                    primary="cs.CV",
                    categories=("cs.CV",),
                )
            )
        )
        text = arxiv.render("2026-07-02", NOW, 26, papers)

        self.assertIn("## cs.AI — Artificial Intelligence (1)", text)
        self.assertIn("## cs.CV — Computer Vision (1)", text)
        self.assertIn("A One, B Two, C Three et al.", text)
        self.assertIn("[A Paper About Agents](https://arxiv.org/abs/2607.00123v1)", text)
        self.assertIn("> First sentence of the abstract. Second sentence.", text)
        self.assertNotIn("Third one here", text)  # abstract trimmed to 2 sentences


class MainTest(unittest.TestCase):
    def test_main_writes_file_from_fetched_feed(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "arxiv"
            with mock.patch.object(
                arxiv, "fetch_feed", return_value=atom_fixture(entry_fixture())
            ):
                code = arxiv.main(
                    [
                        "--out-dir",
                        str(out_dir),
                        "--date",
                        "2026-07-02",
                        "--now",
                        "2026-07-02T06:15:00+00:00",
                    ]
                )

            self.assertEqual(code, 0)
            written = (out_dir / "2026-07-02-papers.md").read_text(encoding="utf-8")
            self.assertIn("A Paper About Agents", written)

    def test_main_exits_nonzero_when_fetch_entirely_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(
                arxiv, "fetch_feed", side_effect=RuntimeError("network down")
            ):
                code = arxiv.main(
                    ["--out-dir", tmp, "--date", "2026-07-02", "--now", "2026-07-02T06:15:00+00:00"]
                )

            self.assertEqual(code, 1)
            self.assertEqual(list(Path(tmp).iterdir()), [])  # nothing written


if __name__ == "__main__":
    unittest.main()
