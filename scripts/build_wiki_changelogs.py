#!/usr/bin/env python3
"""Generate each wiki page's `## Changelog` section from git commit history.

The changelog is a DERIVED artifact, not prose anyone writes. Two facts the
repo already records are enough to reconstruct it exactly:

  - **git** knows which commits touched a given page, and when. That is the
    authoritative spine: one entry per commit that substantively changed the
    page, dated by that commit's author date.
  - **research/wiki/log.md** knows what happened to that page on that date.
    Its per-run summaries already name the pages they touched
    (`updated 8 (deepseek — first external round CLOSED ...; ...)`), so the
    narrative half needs no new authoring either.

A commit counts as substantive only when the page's content *excluding its
changelog section* differs from the parent's. That single rule makes the
generator a fixpoint: the commit that writes a changelog is invisible to the
next regeneration, so re-running never grows the section.

It also keeps output stable across the squash-merge that publishes every
scheduled run (see CLAUDE.md load-bearing rule 13): entries are keyed on
author date and file content, never on a commit hash or subject that a squash
rewrites. Non-ingest commits with no matching log.md fragment fall back to the
commit subject with any `(#123)` PR suffix stripped, for the same reason.

Usage:
    uv run python scripts/build_wiki_changelogs.py             # rewrite sections
    uv run python scripts/build_wiki_changelogs.py --check     # exit 1 if stale
    uv run python scripts/build_wiki_changelogs.py --root DIR --rev main
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import check_wiki as cw

HEADING = "## Changelog"
SUMMARY_MAX = 220
# `slug — detail` inside a log.md run summary. The slug may carry a type word
# ("salesforce entity — ..."). The fragment ends at the next `; slug —` pair or
# at the end of the parenthesised group.
_FRAGMENT_TAIL = r"(?=;\s*[a-z0-9][a-z0-9-]*(?:\s+\w+)?\s*—|\)\s*[.;]|\)\s*$|$)"
PR_SUFFIX_RE = re.compile(r"\s*\(#\d+\)\s*$")
WIKILINK_MARKS_RE = re.compile(r"\[\[([^\[\]|]+)(?:\|([^\[\]]+))?\]\]")


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd)


def strip_changelog(text: str) -> str:
    """Return `text` with its changelog section removed, for content compares."""
    data, body = cw._split_frontmatter(text, Path("<mem>"), cw.Report())
    if data is None:
        return text.strip()
    lines = body.splitlines()
    headings = cw.find_changelog_headings(body)
    if headings:
        lines = lines[: headings[0]]
    # Frontmatter participates: an aliases/sources/timestamp-only edit is a
    # real change to the page even when the prose is untouched.
    header = text.split("\n---\n", 1)[0]
    return (header + "\n" + "\n".join(lines)).strip()


def _sanitize(summary: str) -> str:
    """One line, no wikilink syntax, length-capped."""
    text = WIKILINK_MARKS_RE.sub(lambda m: (m.group(2) or m.group(1)), summary)
    text = " ".join(text.split())
    text = text.rstrip(" .;,")
    if len(text) > SUMMARY_MAX:
        text = text[: SUMMARY_MAX - 1].rstrip(" .;,") + "…"
    return text


def parse_log_summaries(log_text: str) -> dict[str, list[str]]:
    """Map `YYYY-MM-DD` → that date's log.md run summaries."""
    out: dict[str, list[str]] = {}
    for line in log_text.splitlines():
        m = cw.LOG_LINE_RE.match(line)
        if m:
            out.setdefault(m.group(1), []).append(m.group(3))
    return out


def fragment_for(slug: str, summaries: list[str]) -> str | None:
    """Pull `slug`'s own detail out of a run summary, if it names the page."""
    pattern = re.compile(
        r"\b" + re.escape(slug) + r"\b(?:\s+(?:entity|concept|theme))?\s*—\s*(.+?)" + _FRAGMENT_TAIL
    )
    for summary in summaries:
        m = pattern.search(summary)
        if m and m.group(1).strip():
            return _sanitize(m.group(1))
    return None


def page_entries(path: Path, repo_root: Path, rev: str, log_by_date: dict[str, list[str]]) -> list[str]:
    """Build one page's changelog entries, oldest first."""
    rel = path.relative_to(repo_root).as_posix()
    proc = _git(["log", "--format=%H%x1f%ad%x1f%s", "--date=short", "--reverse", rev, "--", rel], repo_root)
    records = [line.split("\x1f") for line in proc.stdout.strip().splitlines() if line]

    entries: list[str] = []
    for sha, day, subject in records:
        current = _git(["show", f"{sha}:{rel}"], repo_root)
        if current.returncode != 0:
            continue  # page absent at this commit (e.g. a deletion in old history)
        parent = _git(["show", f"{sha}^:{rel}"], repo_root)
        created = parent.returncode != 0
        if not created and strip_changelog(parent.stdout) == strip_changelog(current.stdout):
            continue  # changelog-only commit — invisible, keeping this a fixpoint
        summary = fragment_for(path.stem, log_by_date.get(day, [])) or _sanitize(
            PR_SUFFIX_RE.sub("", subject)
        )
        entries.append(f"- [{day}] {'created' if created else 'updated'} | {summary}")

    if not entries:
        # Uncommitted page (the run that creates it regenerates after commit).
        text = path.read_text(encoding="utf-8")
        data, _ = cw._split_frontmatter(text, path, cw.Report())
        created_at = (data or {}).get("created_at")
        entries.append(f"- [{created_at}] created | page created")
    return entries


def render_page(text: str, entries: list[str]) -> str:
    """Replace (or append) the page's changelog section."""
    data, body = cw._split_frontmatter(text, Path("<mem>"), cw.Report())
    if data is None:
        raise ValueError("page frontmatter did not parse")
    headings = cw.find_changelog_headings(body)
    kept = body.splitlines()[: headings[0]] if headings else body.splitlines()
    header = text.split("\n---\n", 1)[0]
    prose = "\n".join(kept).rstrip()
    return f"{header}\n---\n\n{prose}\n\n{HEADING}\n\n" + "\n".join(entries) + "\n"


def _write_atomic(path: Path, content: str) -> None:
    """Atomic replace (CLAUDE.md load-bearing rule 8)."""
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def assert_full_history(repo_root: Path) -> None:
    """Refuse to run against a shallow clone.

    A shallow checkout (`actions/checkout`'s default `fetch-depth: 1`) makes
    `git log -- <page>` return only the tip commit, which would silently
    rewrite every page's changelog down to a single bogus entry. Fail loudly
    instead: scheduled lanes that regenerate must check out `fetch-depth: 0`.
    """
    proc = _git(["rev-parse", "--is-shallow-repository"], repo_root)
    if proc.stdout.strip() == "true":
        raise SystemExit(
            "refusing to run on a shallow clone — per-page history would be truncated. "
            "Check out with `fetch-depth: 0` (see .github/workflows/wiki-ingest.yml)."
        )


def build(wiki_dir: Path, repo_root: Path, rev: str) -> dict[Path, str]:
    """Return {page path: rendered text} for every page."""
    assert_full_history(repo_root)
    log_text = (wiki_dir / "log.md").read_text(encoding="utf-8") if (wiki_dir / "log.md").is_file() else ""
    log_by_date = parse_log_summaries(log_text)
    out: dict[Path, str] = {}
    for path in cw.gather_pages(wiki_dir):
        text = path.read_text(encoding="utf-8")
        out[path] = render_page(text, page_entries(path, repo_root, rev, log_by_date))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=None, help="wiki root (default research/wiki)")
    parser.add_argument("--repo-root", default=None, help="git repo root (default: repo containing --root)")
    parser.add_argument("--rev", default="HEAD", help="revision whose history to read (default HEAD)")
    parser.add_argument("--check", action="store_true", help="exit 1 if any committed changelog is stale")
    args = parser.parse_args(argv)

    wiki_dir = Path(args.root).resolve() if args.root else cw.WIKI_DIR
    repo_root = Path(args.repo_root).resolve() if args.repo_root else cw.REPO_ROOT
    if not wiki_dir.is_dir():
        print(f"no wiki dir at {wiki_dir} — nothing to build", file=sys.stderr)
        return 0

    rendered = build(wiki_dir, repo_root, args.rev)

    if args.check:
        stale = [p for p, text in rendered.items() if p.read_text(encoding="utf-8") != text]
        if stale:
            for p in stale:
                print(f"FAIL {p.relative_to(wiki_dir)}: changelog is stale", file=sys.stderr)
            print(
                f"\n{len(stale)} stale changelog(s) — regenerate with "
                "`uv run python scripts/build_wiki_changelogs.py`",
                file=sys.stderr,
            )
            return 1
        print(f"OK — {len(rendered)} changelog(s) up to date")
        return 0

    changed = 0
    for path, text in rendered.items():
        if path.read_text(encoding="utf-8") != text:
            _write_atomic(path, text)
            changed += 1
    entries = sum(len(t.split(HEADING)[-1].strip().splitlines()) for t in rendered.values())
    print(f"wrote {changed} changed / {len(rendered)} page(s), {entries} entries from git history")
    return 0


if __name__ == "__main__":
    sys.exit(main())
