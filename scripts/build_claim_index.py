#!/usr/bin/env python3
"""Build the cross-article claim index from committed methodology sidecars.

Usage:
    uv run python scripts/build_claim_index.py            # rewrite the index
    uv run python scripts/build_claim_index.py --check    # fail (exit 1) if stale

Every generative-research run commits a `<stem>.claims.json` ledger beside its
article: the claims the thesis rests on, each with source URLs, source tiers,
an `as_of` date, a confidence and a risk. Until this script existed nothing
read them back, so 1,300+ source-verified claims sat on disk while every new
article re-derived the same facts from zero.

This walks `research/generative/*.claims.json`, joins each ledger to its
article metadata in `research/generative/index.json`, and emits a single
queryable index at `research/claims/index.json`. `scripts/claim_search.py` is
the read side; the generative-research agent runs it BEFORE building its own
ledger so it reuses a verified claim rather than re-verifying it.

THE REUSE CONTRACT IS THE POINT, AND IT IS DELIBERATELY CONSERVATIVE.
A store whose value is "reuse instead of re-verify" is also a machine for
laundering stale numbers if it hands back a volatile metric from six months
ago under the authority of "already verified". So every record carries an
explicit `reusable` boolean plus a `reuse_block` reason, and a claim is
offered for direct reuse ONLY when it is `risk: stable`, carries an `as_of`,
and is not `confidence: low`. Everything else is returned flagged
re-verify-required. Callers must honour that flag; see docs/claim-store.md.

The output is a pure function of the inputs (no timestamps, sorted
throughout), so `--check` is a real drift gate and can run in CI the same way
`build_wiki_index.py --check` does.

stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATIVE_DIR = REPO_ROOT / "research" / "generative"
OUT_PATH = REPO_ROOT / "research" / "claims" / "index.json"

SCHEMA_VERSION = 1

# A claim is offered for direct reuse only when all three hold. Loosening any
# of these turns the store into a stale-number launderer — see module docstring.
REUSABLE_RISK = "stable"
BLOCKING_CONFIDENCE = "low"


def normalize_host(url: str) -> str:
    """Bare registrable-ish host for grouping. Cheap and deterministic."""
    try:
        host = (urlparse(url).netloc or "").lower()
    except ValueError:
        return ""
    if host.startswith("www."):
        host = host[4:]
    return host.split(":")[0]


def canonical_url(url: str) -> str:
    """Strip fragment + trailing slash so cosmetic variants group together.

    Deliberately NOT a full canonicalizer (no query-param sorting, no utm
    stripping) — `source_cache.py` owns that for fetching. Here we only need
    two citations of the same page to land in the same bucket.
    """
    u = (url or "").strip()
    u = u.split("#", 1)[0]
    if u.endswith("/") and len(u) > len("https://x/"):
        u = u[:-1]
    return u


_NUM_RE = re.compile(
    r"""
    (?P<currency>[$€£])?\s*
    (?P<num>\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)
    \s*
    (?P<suffix>%|percent|bps|billion|bn|million|mn|trillion|tn|[BMTK]\b)?
    """,
    re.VERBOSE | re.IGNORECASE,
)

_SCALE = {
    "b": 1e9, "bn": 1e9, "billion": 1e9,
    "m": 1e6, "mn": 1e6, "million": 1e6,
    "t": 1e12, "tn": 1e12, "trillion": 1e12,
    "k": 1e3,
}


def extract_numerics(text: str) -> list[dict[str, Any]]:
    """Pull comparable numbers out of a claim sentence.

    Used ONLY to shortlist contradiction CANDIDATES for an agent to
    adjudicate — never to decide that two claims contradict. Percentages and
    basis points are kept in their own units rather than scaled, so "50%" and
    "50 billion" can never be compared as if they were the same quantity.
    """
    out: list[dict[str, Any]] = []
    for m in _NUM_RE.finditer(text or ""):
        raw_num = m.group("num").replace(",", "")
        try:
            value = float(raw_num)
        except ValueError:
            continue
        suffix = (m.group("suffix") or "").lower().strip()
        if suffix in ("%", "percent"):
            unit = "percent"
        elif suffix == "bps":
            unit = "bps"
        else:
            unit = "currency" if m.group("currency") else "count"
            value *= _SCALE.get(suffix, 1.0)
        out.append({"value": value, "unit": unit, "raw": m.group(0).strip()})
    return out


_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9.\-]*")

# Deliberately small: this is a shortlisting aid, not a linguistic model.
_STOP = frozenset(
    """a an and are as at be been by for from had has have in is it its of on
    or that the to was were will with which this these those than then""".split()
)


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN_RE.findall((text or "").lower()) if t not in _STOP]


def _article_meta(generative_dir: Path) -> dict[str, dict[str, Any]]:
    """Map article stem -> metadata from research/generative/index.json.

    Missing metadata is not fatal: a ledger whose article row was never
    written still carries usable claims, and dropping it would silently
    shrink the store. Such rows get empty title/tags and are still indexed.
    """
    index_path = generative_dir / "index.json"
    if not index_path.is_file():
        return {}
    try:
        rows = json.loads(index_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(rows, list):
        return {}
    meta: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        fname = str(row.get("file") or "")
        stem = fname[: -len(".html")] if fname.endswith(".html") else fname
        if not stem:
            continue
        meta[stem] = {
            "slug": row.get("slug") or "",
            "title": row.get("title") or "",
            "created_at": row.get("created_at") or "",
            "tags": sorted(t for t in (row.get("tags") or []) if isinstance(t, str)),
        }
    return meta


def _reuse_verdict(claim: dict[str, Any]) -> tuple[bool, str | None]:
    """Decide whether a stored claim may be reused without re-verification."""
    risk = str(claim.get("risk") or "").strip()
    as_of = str(claim.get("as_of") or "").strip()
    confidence = str(claim.get("confidence") or "").strip()
    if not as_of:
        return False, "no-as-of"
    if risk != REUSABLE_RISK:
        # volatile / contested / single-source all need a fresh look, for
        # different reasons — keep the reason so the agent can tell them apart.
        return False, risk or "unknown-risk"
    if confidence == BLOCKING_CONFIDENCE:
        return False, "low-confidence"
    return True, None


def build_index(generative_dir: Path) -> dict[str, Any]:
    meta = _article_meta(generative_dir)
    claims: list[dict[str, Any]] = []
    articles: list[dict[str, Any]] = []
    by_host: dict[str, list[str]] = {}
    by_url: dict[str, list[str]] = {}

    for path in sorted(generative_dir.glob("*.claims.json")):
        stem = path.name[: -len(".claims.json")]
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"warning: skipping unreadable ledger {path.name}: {exc}", file=sys.stderr)
            continue
        rows = payload.get("claims") if isinstance(payload, dict) else None
        if not isinstance(rows, list):
            print(f"warning: {path.name} has no claims[] array", file=sys.stderr)
            continue

        art = meta.get(stem, {"slug": "", "title": "", "created_at": "", "tags": []})
        kept = 0
        for row in rows:
            if not isinstance(row, dict):
                continue
            cid = str(row.get("id") or "").strip()
            text = str(row.get("claim") or "").strip()
            if not text:
                continue
            # IDs are only unique WITHIN one ledger (c1..c99 repeat across
            # articles), so the global key must be composite. An id-less row
            # still gets indexed under a positional key rather than vanishing.
            key = f"{stem}#{cid}" if cid else f"{stem}#idx{kept}"

            urls = [canonical_url(u) for u in (row.get("source_urls") or []) if isinstance(u, str) and u.strip()]
            tiers = [t for t in (row.get("source_tiers") or []) if isinstance(t, str)]
            hosts = sorted({h for h in (normalize_host(u) for u in urls) if h})
            reusable, block = _reuse_verdict(row)

            claims.append(
                {
                    "key": key,
                    "article": stem,
                    "article_title": art["title"],
                    "article_created_at": art["created_at"],
                    "id": cid,
                    "claim": text,
                    "type": str(row.get("type") or "other"),
                    "source_urls": urls,
                    "source_tiers": tiers,
                    "hosts": hosts,
                    "as_of": str(row.get("as_of") or ""),
                    "confidence": str(row.get("confidence") or ""),
                    "risk": str(row.get("risk") or ""),
                    "reusable": reusable,
                    "reuse_block": block,
                    # NOTE: figures are deliberately NOT stored. They are a
                    # pure function of `claim` (extract_numerics), so
                    # committing them would put ~0.5 MB of derivable data in
                    # git and give it a second place to drift from the text
                    # it describes. claim_search.py recomputes them per query
                    # — a regex over a short string, thousands of times
                    # cheaper than the round trip that fetched the claim.
                }
            )
            for h in hosts:
                by_host.setdefault(h, []).append(key)
            for u in urls:
                by_url.setdefault(u, []).append(key)
            kept += 1

        articles.append(
            {
                "stem": stem,
                "slug": art["slug"],
                "title": art["title"],
                "created_at": art["created_at"],
                "tags": art["tags"],
                "claim_count": kept,
            }
        )

    claims.sort(key=lambda c: c["key"])
    articles.sort(key=lambda a: a["stem"])
    reusable_count = sum(1 for c in claims if c["reusable"])

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_from": "research/generative/*.claims.json",
        "article_count": len(articles),
        "claim_count": len(claims),
        "reusable_count": reusable_count,
        "articles": articles,
        "claims": claims,
        "by_host": {h: sorted(set(v)) for h, v in sorted(by_host.items())},
        "by_url": {u: sorted(set(v)) for u, v in sorted(by_url.items())},
    }


def render(index: dict[str, Any]) -> str:
    """Stable serialization: deterministic so --check is a real drift gate."""
    return json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _atomic_write(path: Path, text: str) -> None:
    """Temp file in the SAME directory + os.replace (load-bearing rule 8)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".claim-index-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if the committed index differs from a fresh build",
    )
    parser.add_argument("--root", default=str(GENERATIVE_DIR), help="generative dir")
    parser.add_argument("--out", default=str(OUT_PATH), help="index output path")
    args = parser.parse_args(argv)

    generative_dir = Path(args.root)
    out_path = Path(args.out)
    if not generative_dir.is_dir():
        print(f"error: no generative dir at {generative_dir}", file=sys.stderr)
        return 2

    index = build_index(generative_dir)
    text = render(index)

    if args.check:
        if not out_path.is_file():
            print(f"error: {out_path} is missing; run without --check", file=sys.stderr)
            return 1
        current = out_path.read_text(encoding="utf-8")
        if current != text:
            print(
                f"error: {out_path} is stale — rebuild with "
                "`uv run python scripts/build_claim_index.py`",
                file=sys.stderr,
            )
            return 1
        print(f"claim index OK: {index['claim_count']} claims across {index['article_count']} articles")
        return 0

    _atomic_write(out_path, text)
    print(
        f"wrote {out_path.relative_to(REPO_ROOT) if out_path.is_relative_to(REPO_ROOT) else out_path}: "
        f"{index['claim_count']} claims across {index['article_count']} articles "
        f"({index['reusable_count']} directly reusable)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
