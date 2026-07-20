#!/usr/bin/env python3
"""Tests for build_wiki_changelogs.py — the git-derived changelog generator.

These build real throwaway git repos (not mocks): the whole point of the
generator is that its output is a function of commit history, so the history
has to be real for the test to mean anything.
"""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import build_wiki_changelogs as bwc
import check_wiki

PAGE = """---
slug: {slug}
title: {title}
type: {type}
description: {desc}
created_at: 2026-05-01
timestamp: {ts}
---

{body}
"""

SUBDIR = {"entity": "entities", "concept": "concepts", "theme": "themes"}


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True,
        env={"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1", "PATH": "/usr/bin:/bin:/usr/local/bin"},
    )
    if proc.returncode != 0 and args[0] not in ("show",):
        raise AssertionError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc.stdout


def init_repo(repo: Path) -> Path:
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "t")
    git(repo, "config", "user.email", "t@t")
    wiki = repo / "research" / "wiki"
    for sub in check_wiki.PAGE_SUBDIRS:
        (wiki / sub).mkdir(parents=True, exist_ok=True)
    return wiki


def write_page(wiki: Path, slug: str, *, type_: str = "entity", body: str = "Prose.", ts: str = "2026-05-01T00:00:00Z", desc: str = "One line.") -> Path:
    p = wiki / SUBDIR[type_] / f"{slug}.md"
    p.write_text(
        PAGE.format(slug=slug, title=slug.title(), type=type_, desc=desc, ts=ts, body=body),
        encoding="utf-8",
    )
    return p


def write_log(wiki: Path, lines: list[str]) -> None:
    (wiki / "log.md").write_text("# Wiki Log\n\n" + "\n\n".join(lines) + "\n", encoding="utf-8")


def commit(repo: Path, message: str, day: str) -> None:
    git(repo, "add", "-A")
    stamp = f"{day}T12:00:00"
    subprocess.run(
        ["git", "commit", "-q", "-m", message],
        cwd=repo, capture_output=True, text=True,
        env={
            "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
            "PATH": "/usr/bin:/bin:/usr/local/bin",
            "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp,
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
        },
    )


def entries_of(page: Path) -> list[str]:
    text = page.read_text(encoding="utf-8")
    if bwc.HEADING not in text:
        return []
    return [ln for ln in text.split(bwc.HEADING)[-1].strip().splitlines() if ln.strip()]


class BuildWikiChangelogsTest(unittest.TestCase):
    def test_entries_track_commits_that_changed_the_page(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            wiki = init_repo(repo)
            write_page(wiki, "alpha")
            write_log(wiki, ["## [2026-05-01] seed | seeded alpha"])
            commit(repo, "Wiki ingest 2026-05-01", "2026-05-01")

            write_page(wiki, "alpha", body="Prose, revised.")
            write_log(wiki, [
                "## [2026-05-01] seed | seeded alpha",
                "## [2026-05-04] ingest | Ingested digest. Updated 1 (alpha — folded in the Q2 print).",
            ])
            commit(repo, "Wiki ingest 2026-05-04", "2026-05-04")

            bwc.main(["--root", str(wiki), "--repo-root", str(repo)])
            got = entries_of(wiki / "entities" / "alpha.md")
            self.assertEqual(got[0], "- [2026-05-01] created | Wiki ingest 2026-05-01")
            # The log.md fragment supplies the summary for the second entry.
            self.assertEqual(got[1], "- [2026-05-04] updated | folded in the Q2 print")

    def test_untouched_page_gets_no_entry_for_someone_elses_commit(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            wiki = init_repo(repo)
            write_page(wiki, "alpha")
            write_page(wiki, "beta", type_="concept")
            write_log(wiki, ["## [2026-05-01] seed | seeded"])
            commit(repo, "Wiki ingest 2026-05-01", "2026-05-01")

            write_page(wiki, "alpha", body="Only alpha changed.")
            commit(repo, "Wiki ingest 2026-05-05", "2026-05-05")

            bwc.main(["--root", str(wiki), "--repo-root", str(repo)])
            self.assertEqual(len(entries_of(wiki / "entities" / "alpha.md")), 2)
            self.assertEqual(len(entries_of(wiki / "concepts" / "beta.md")), 1)

    def test_regeneration_is_a_fixpoint(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            wiki = init_repo(repo)
            write_page(wiki, "alpha")
            write_log(wiki, ["## [2026-05-01] seed | seeded alpha"])
            commit(repo, "Wiki ingest 2026-05-01", "2026-05-01")

            bwc.main(["--root", str(wiki), "--repo-root", str(repo)])
            first = (wiki / "entities" / "alpha.md").read_text(encoding="utf-8")
            # Commit the generated changelog, then regenerate: the
            # changelog-only commit must be invisible.
            commit(repo, "Wiki changelogs 2026-05-02", "2026-05-02")
            bwc.main(["--root", str(wiki), "--repo-root", str(repo)])
            self.assertEqual(first, (wiki / "entities" / "alpha.md").read_text(encoding="utf-8"))
            self.assertEqual(bwc.main(["--root", str(wiki), "--repo-root", str(repo), "--check"]), 0)

    def test_frontmatter_only_change_counts_as_substantive(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            wiki = init_repo(repo)
            write_page(wiki, "alpha")
            write_log(wiki, ["## [2026-05-01] seed | seeded alpha"])
            commit(repo, "Wiki ingest 2026-05-01", "2026-05-01")

            write_page(wiki, "alpha", ts="2026-05-06T00:00:00Z")  # body identical
            commit(repo, "Wiki ingest 2026-05-06", "2026-05-06")

            bwc.main(["--root", str(wiki), "--repo-root", str(repo)])
            self.assertEqual(len(entries_of(wiki / "entities" / "alpha.md")), 2)

    def test_pr_suffix_stripped_from_fallback_summary(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            wiki = init_repo(repo)
            write_page(wiki, "alpha")
            write_log(wiki, ["## [2026-05-01] seed | no page named here"])
            commit(repo, "Wiki ingest 2026-05-01 (#755)", "2026-05-01")

            bwc.main(["--root", str(wiki), "--repo-root", str(repo)])
            self.assertEqual(
                entries_of(wiki / "entities" / "alpha.md")[0],
                "- [2026-05-01] created | Wiki ingest 2026-05-01",
            )

    def test_generated_corpus_passes_the_validator(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            wiki = init_repo(repo)
            write_page(wiki, "alpha", body="Links to [[beta]].")
            write_page(wiki, "beta", type_="concept", body="Links to [[alpha]].")
            (wiki / "index.md").write_text(
                "# Wiki Index\n\n## Entities\n- [[alpha]] — One line.\n\n## Concepts\n- [[beta]] — One line.\n\n## Themes\n",
                encoding="utf-8",
            )
            write_log(wiki, ["## [2026-05-01] seed | seeded alpha and beta"])
            commit(repo, "Wiki ingest 2026-05-01", "2026-05-01")

            bwc.main(["--root", str(wiki), "--repo-root", str(repo)])
            report = check_wiki.Report()
            check_wiki.validate(check_wiki.gather_pages(wiki), wiki, report, lint=False)
            self.assertTrue(report.ok(), msg=[f.__dict__ for f in report.failures])

    def test_check_flags_a_stale_changelog(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            wiki = init_repo(repo)
            write_page(wiki, "alpha")
            write_log(wiki, ["## [2026-05-01] seed | seeded alpha"])
            commit(repo, "Wiki ingest 2026-05-01", "2026-05-01")
            self.assertEqual(bwc.main(["--root", str(wiki), "--repo-root", str(repo), "--check"]), 1)
            bwc.main(["--root", str(wiki), "--repo-root", str(repo)])
            self.assertEqual(bwc.main(["--root", str(wiki), "--repo-root", str(repo), "--check"]), 0)

    def test_shallow_clone_is_refused(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            origin = root / "origin"
            origin.mkdir()
            wiki = init_repo(origin)
            write_page(wiki, "alpha")
            write_log(wiki, ["## [2026-05-01] seed | seeded alpha"])
            commit(origin, "Wiki ingest 2026-05-01", "2026-05-01")
            write_page(wiki, "alpha", body="Second revision.")
            commit(origin, "Wiki ingest 2026-05-02", "2026-05-02")

            shallow = root / "shallow"
            git(root, "clone", "-q", "--depth", "1", f"file://{origin}", str(shallow))
            with self.assertRaises(SystemExit) as ctx:
                bwc.build(shallow / "research" / "wiki", shallow, "HEAD")
            self.assertIn("shallow", str(ctx.exception))

    def test_wikilink_syntax_is_stripped_from_summaries(self):
        # log.md fragments may contain [[links]]; leaving them in would make a
        # changelog entry participate in link resolution and could break the
        # validator on a page the fragment happens to mention.
        self.assertEqual(bwc._sanitize("folded in [[gpt-5-2|GPT-5.2]] and [[openai]]"),
                         "folded in GPT-5.2 and openai")

    def test_summary_is_length_capped(self):
        out = bwc._sanitize("x" * 400)
        self.assertLessEqual(len(out), bwc.SUMMARY_MAX)
        self.assertTrue(out.endswith("…"))


if __name__ == "__main__":
    unittest.main()
