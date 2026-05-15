#!/usr/bin/env python3
"""Write a generative research HTML fragment into research/generative/.

Used by all three trigger paths (local slash command, GitHub issue label,
workflow_dispatch). Pure I/O — never calls an LLM. The contract:

  * Body must be a single <article>...</article> fragment.
  * No <script>, <style>, or inline style= attributes.
  * The file is named <YYYY-MM-DDTHHMMSS>--<slug>.html (UTC).
  * research/generative/index.json holds the canonical list (ascending).

The dashboard reads index.json via the deploy manifest and renders the
list newest-first.
"""

from __future__ import annotations

import argparse
import html.parser
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

MAX_BODY_BYTES = 200_000
MAX_STANDALONE_BYTES = 2_000_000
SLUG_MAX = 60
KIND_FRAGMENT = "fragment"
KIND_STANDALONE = "standalone"
KINDS = (KIND_FRAGMENT, KIND_STANDALONE)
DISALLOWED_PATTERNS = [
    re.compile(r"\sstyle\s*=", re.IGNORECASE),
    re.compile(r"\son\w+\s*=", re.IGNORECASE),  # onclick=, onload=, etc.
    re.compile(r"javascript:", re.IGNORECASE),
]
# Fragment articles must compose from this fixed tag set + the ara-* class
# vocabulary defined in dashboard/src/components/ara-research.css. See
# COMPONENTS.md for the human-readable reference.
FRAGMENT_ALLOWED_TAGS = frozenset([
    "article", "section", "div", "header", "footer",
    "h2", "h3", "h4",
    "p", "span", "em", "strong", "code", "mark", "sup", "sub", "abbr", "time",
    "ul", "ol", "li", "dl", "dt", "dd",
    "a", "img", "figure", "figcaption",
    "table", "thead", "tbody", "tr", "th", "td",
    "blockquote", "pre",
    "br", "hr",
])
FRAGMENT_CLASS_PREFIX = "ara-"
ARTICLE_OPEN = re.compile(r"<article\b[^>]*>", re.IGNORECASE)
ARTICLE_CLOSE = re.compile(r"</article\s*>", re.IGNORECASE)
H2_TEXT = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.IGNORECASE | re.DOTALL)
HTML_TITLE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
H1_TEXT = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
TAG_STRIP = re.compile(r"<[^>]+>")


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    if len(text) > SLUG_MAX:
        text = text[:SLUG_MAX].rstrip("-")
    return text or "untitled"


def read_body(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text(encoding="utf-8")


class _FragmentValidator(html.parser.HTMLParser):
    """Parse-aware check: every tag must be in FRAGMENT_ALLOWED_TAGS,
    every class= token must start with FRAGMENT_CLASS_PREFIX."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bad_tags: list[str] = []
        self.bad_classes: list[tuple[str, str]] = []

    def _check(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() not in FRAGMENT_ALLOWED_TAGS:
            self.bad_tags.append(tag.lower())
            return
        for name, value in attrs:
            if name.lower() != "class" or not value:
                continue
            for tok in value.split():
                if not tok.startswith(FRAGMENT_CLASS_PREFIX):
                    self.bad_classes.append((tag.lower(), tok))

    def handle_starttag(self, tag, attrs):
        self._check(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._check(tag, attrs)


def validate_body(body: str, kind: str) -> None:
    if kind == KIND_FRAGMENT:
        if len(body.encode("utf-8")) > MAX_BODY_BYTES:
            raise ValueError(f"fragment body exceeds {MAX_BODY_BYTES} bytes")
        if not ARTICLE_OPEN.search(body):
            raise ValueError("fragment body must contain an opening <article> tag")
        if not ARTICLE_CLOSE.search(body):
            raise ValueError("fragment body must contain a closing </article> tag")
        for pat in DISALLOWED_PATTERNS:
            m = pat.search(body)
            if m:
                raise ValueError(f"fragment body contains disallowed pattern: {m.group(0)!r}")
        parser = _FragmentValidator()
        parser.feed(body)
        if parser.bad_tags:
            uniq = sorted(set(parser.bad_tags))
            raise ValueError(
                f"fragment uses disallowed tags: {uniq}. "
                f"Allowed: {sorted(FRAGMENT_ALLOWED_TAGS)}. See COMPONENTS.md."
            )
        if parser.bad_classes:
            preview = ", ".join(f"<{t}> class={c!r}" for t, c in parser.bad_classes[:5])
            raise ValueError(
                f"fragment uses non-{FRAGMENT_CLASS_PREFIX}* classes: {preview}. "
                f"All class tokens must start with {FRAGMENT_CLASS_PREFIX!r}. "
                f"See COMPONENTS.md for the vocabulary."
            )
    elif kind == KIND_STANDALONE:
        # Standalone docs are full HTML pages rendered inside a sandboxed
        # iframe. The sandbox is the security boundary, not regex on the body.
        if len(body.encode("utf-8")) > MAX_STANDALONE_BYTES:
            raise ValueError(f"standalone body exceeds {MAX_STANDALONE_BYTES} bytes")
        if "<html" not in body.lower() and "<!doctype" not in body.lower():
            raise ValueError("standalone body should start with <!doctype html> or <html>")
    else:
        raise ValueError(f"unknown kind: {kind!r}")


def derive_title(body: str, kind: str, fallback: str) -> str:
    if kind == KIND_STANDALONE:
        for pat in (HTML_TITLE, H1_TEXT, H2_TEXT):
            m = pat.search(body)
            if m:
                text = TAG_STRIP.sub("", m.group(1)).strip()
                if text:
                    return text
    else:
        m = H2_TEXT.search(body)
        if m:
            text = TAG_STRIP.sub("", m.group(1)).strip()
            if text:
                return text
    return fallback.strip() or "Untitled"


def atomic_write_json(path: Path, data) -> None:
    fd, tmp = tempfile.mkstemp(prefix=".idx-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def load_index(path: Path) -> list:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError(f"{path} is not a JSON array")
    return data


def git_commit(repo: Path, files: list[Path], message: str) -> None:
    rels = [str(p.relative_to(repo)) for p in files]
    subprocess.run(["git", "-C", str(repo), "add", "--", *rels], check=True)
    diff = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--quiet"],
    )
    if diff.returncode == 0:
        print("write_generative_research: no staged changes; skipping commit", file=sys.stderr)
        return
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-m", message],
        check=True,
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--topic", required=True, help="user-supplied topic; default title source")
    p.add_argument("--html-body", required=True, help="path to <article> fragment, or '-' for stdin")
    p.add_argument("--model", required=True, help="model identifier, e.g. claude-opus-4-7")
    p.add_argument("--title", default=None, help="explicit title; falls back to first <h2> then topic")
    p.add_argument("--slug", default=None, help="url slug; falls back to slugify(topic)")
    p.add_argument("--prompt", default=None, help="original user prompt (stored in index)")
    p.add_argument("--tags", default="", help="comma-separated tags")
    p.add_argument("--source", default="local", help="trigger source: local, workflow_dispatch, issue, import")
    p.add_argument(
        "--kind",
        default=KIND_FRAGMENT,
        choices=KINDS,
        help=(
            "fragment (default) = single <article> rendered with dashboard styles; "
            "standalone = full HTML page rendered inside a sandboxed iframe"
        ),
    )
    p.add_argument("--no-commit", action="store_true", help="skip git commit")
    p.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="repo root (default: parent of scripts/)",
    )
    args = p.parse_args(argv)

    repo = Path(args.repo_root).resolve()
    gen_dir = repo / "research" / "generative"
    if not gen_dir.exists():
        raise SystemExit(f"missing dir: {gen_dir}")

    body = read_body(args.html_body)
    validate_body(body, args.kind)
    if not body.endswith("\n"):
        body += "\n"

    title = (args.title or derive_title(body, args.kind, args.topic)).strip()
    base_slug = (args.slug or slugify(args.topic)).strip("-") or "untitled"
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    now = datetime.now(timezone.utc).replace(microsecond=0)
    stamp = now.strftime("%Y-%m-%dT%H%M%S")
    iso = now.isoformat().replace("+00:00", "Z")

    index_path = gen_dir / "index.json"
    index = load_index(index_path)

    # Slug is the dashboard's hash route key, so it must be unique across the index.
    existing_slugs = {row.get("slug") for row in index if isinstance(row, dict)}
    slug = base_slug
    n = 2
    while slug in existing_slugs:
        slug = f"{base_slug}-{n}"
        n += 1

    filename = f"{stamp}--{slug}.html"
    html_path = gen_dir / filename
    if html_path.exists():
        raise SystemExit(f"refusing to overwrite existing file: {html_path}")

    row = {
        "slug": slug,
        "file": filename,
        "kind": args.kind,
        "title": title,
        "model": args.model,
        "created_at": iso,
        "source": args.source,
        "prompt": args.prompt or args.topic,
        "tags": tags,
    }
    index.append(row)

    html_path.write_text(body, encoding="utf-8")
    atomic_write_json(index_path, index)

    print(f"wrote {html_path.relative_to(repo)}")
    print(f"updated {index_path.relative_to(repo)} ({len(index)} entries)")

    if not args.no_commit:
        git_commit(
            repo,
            [html_path, index_path],
            f"Generative research: {title}",
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
