#!/usr/bin/env python3
"""BM25 search over the LLM Wiki (research/wiki/{entities,concepts,themes}/*.md).

Usage:
    uv run python scripts/wiki_search.py "query"
    uv run python scripts/wiki_search.py "gpu cloud" --top 3
    uv run python scripts/wiki_search.py "nebius" --json
    uv run python scripts/wiki_search.py "neocloud" --root path/to/wiki

Prints ranked (slug, score, snippet). With --json, prints a JSON array.

Scoring: Okapi BM25 over a per-page bag of tokens assembled from weighted
fields — title + aliases (heaviest), tags, summary, body — so a name match in
the title beats a passing mention in the body. The corpus is tiny (~6 pages),
so two BM25 quirks are handled explicitly: the IDF term is clamped to >= 0
(otherwise terms appearing in >half the corpus become anti-signal), and field
weighting is what makes ranking sensible at this scale.

stdlib (math/re/collections) + yaml only.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "research" / "wiki"
PAGE_SUBDIRS = ("entities", "concepts", "themes")

# BM25 hyperparameters (standard defaults).
BM25_K1 = 1.5
BM25_B = 0.75

# Field repetition weights: a token in `title` counts as N occurrences. This is
# the standard "field boosting via term duplication" trick — keeps a single
# BM25 pass while privileging name/title matches over body mentions.
FIELD_WEIGHTS = {
    "title": 3,
    "aliases": 3,
    "tags": 2,
    "summary": 2,
    "body": 1,
}

TOKEN_RE = re.compile(r"[a-z0-9]+")
# Strip fenced code blocks from the body before tokenizing so code samples
# don't dominate term frequencies. Same fence rule as check_wiki.py.
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")


def tokenize(text: str) -> list[str]:
    """Lowercase, split on non-alphanumerics."""
    return TOKEN_RE.findall(text.lower())


def _strip_fences(body: str) -> str:
    out: list[str] = []
    fence: str | None = None
    fence_indent = ""
    for line in body.splitlines():
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                fence = m.group(2)
                fence_indent = m.group(1)
                continue
            out.append(line)
        else:
            if m and m.group(2)[0] == fence[0] and len(m.group(2)) >= len(fence) and m.group(1) == fence_indent:
                if not line[m.end():].strip():
                    fence = None
    return "\n".join(out)


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Lenient frontmatter split for search (don't raise on odd files)."""
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) < 2:
        return {}, text
    try:
        data = yaml.safe_load(parts[0][4:]) or {}
    except yaml.YAMLError:
        data = {}
    if not isinstance(data, dict):
        data = {}
    return data, parts[1].lstrip("\n")


@dataclass
class Doc:
    slug: str
    title: str
    summary: str
    tokens: Counter  # weighted term frequencies
    length: int  # total weighted token count
    body_text: str  # raw body, for snippet generation


def _field_text(data: dict, body: str) -> dict[str, str]:
    def join_list(key: str) -> str:
        v = data.get(key)
        if isinstance(v, list):
            return " ".join(str(x) for x in v)
        return ""

    return {
        "title": str(data.get("title", "") or ""),
        "aliases": join_list("aliases"),
        "tags": join_list("tags"),
        "summary": str(data.get("summary", "") or ""),
        "body": _strip_fences(body),
    }


def build_doc(path: Path) -> Doc | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    data, body = _split_frontmatter(text)
    slug = str(data.get("slug") or path.stem)
    fields = _field_text(data, body)

    tokens: Counter = Counter()
    for field_name, weight in FIELD_WEIGHTS.items():
        for tok in tokenize(fields[field_name]):
            tokens[tok] += weight
    length = sum(tokens.values())
    return Doc(
        slug=slug,
        title=fields["title"] or slug,
        summary=fields["summary"],
        tokens=tokens,
        length=length,
        body_text=body,
    )


def gather_docs(root: Path) -> list[Doc]:
    docs: list[Doc] = []
    for sub in PAGE_SUBDIRS:
        d = root / sub
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.md")):
            doc = build_doc(path)
            if doc is not None:
                docs.append(doc)
    return docs


def bm25_scores(docs: list[Doc], query: str) -> list[tuple[Doc, float]]:
    q_terms = tokenize(query)
    n = len(docs)
    if n == 0 or not q_terms:
        return [(d, 0.0) for d in docs]

    avgdl = sum(d.length for d in docs) / n if n else 0.0
    # Document frequency per query term.
    df: Counter = Counter()
    for term in set(q_terms):
        for d in docs:
            if d.tokens.get(term, 0) > 0:
                df[term] += 1

    scored: list[tuple[Doc, float]] = []
    for d in docs:
        score = 0.0
        for term in q_terms:
            f = d.tokens.get(term, 0)
            if f == 0:
                continue
            # Clamp IDF >= 0: with a tiny corpus, terms in >half the docs would
            # otherwise yield a negative IDF and become anti-signal.
            idf = max(0.0, math.log((n - df[term] + 0.5) / (df[term] + 0.5) + 1.0))
            denom = f + BM25_K1 * (1 - BM25_B + BM25_B * (d.length / avgdl if avgdl else 0.0))
            score += idf * (f * (BM25_K1 + 1)) / denom if denom else 0.0
        scored.append((d, score))
    scored.sort(key=lambda t: (-t[1], t[0].slug))
    return scored


def make_snippet(doc: Doc, query: str, width: int = 160) -> str:
    """Return summary if present, else a body window around the first query hit."""
    if doc.summary.strip():
        return doc.summary.strip()
    body = " ".join(doc.body_text.split())
    if not body:
        return ""
    q_terms = tokenize(query)
    low = body.lower()
    pos = -1
    for term in q_terms:
        pos = low.find(term)
        if pos != -1:
            break
    if pos == -1:
        return body[:width].rstrip() + ("…" if len(body) > width else "")
    start = max(0, pos - width // 3)
    end = min(len(body), start + width)
    snippet = body[start:end].strip()
    if start > 0:
        snippet = "…" + snippet
    if end < len(body):
        snippet = snippet + "…"
    return snippet


def search(root: Path, query: str, top: int | None = None) -> list[dict]:
    docs = gather_docs(root)
    scored = bm25_scores(docs, query)
    results = [
        {
            "slug": d.slug,
            "score": round(score, 4),
            "snippet": make_snippet(d, query),
        }
        for d, score in scored
        if score > 0.0
    ]
    if top is not None:
        results = results[:top]
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("query", help="search query")
    parser.add_argument("--top", type=int, default=None, help="limit to top N results")
    parser.add_argument("--json", action="store_true", help="emit JSON array")
    parser.add_argument("--root", default=None, help="wiki root dir (default research/wiki)")
    args = parser.parse_args(argv)

    root = Path(args.root) if args.root else WIKI_DIR
    results = search(root, args.query, top=args.top)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("(no matches)")
        return 0
    for r in results:
        print(f"{r['score']:>8.4f}  {r['slug']}")
        if r["snippet"]:
            print(f"          {r['snippet']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
