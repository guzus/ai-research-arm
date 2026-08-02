#!/usr/bin/env python3
"""BM25 search over the cross-article claim store (research/claims/index.json).

Usage:
    uv run python scripts/claim_search.py "hyperscaler capex"
    uv run python scripts/claim_search.py "tpu lease" --top 5 --json
    uv run python scripts/claim_search.py --host sec.gov --top 10
    uv run python scripts/claim_search.py --url https://www.sec.gov/Archives/...
    uv run python scripts/claim_search.py "alphabet credit derivative notional" --candidates

The generative-research agent runs this BEFORE building its own claim ledger,
so it REUSES a claim another article already verified instead of re-deriving
it — and so it notices when what it is about to assert disagrees with what we
published before.

TWO OUTPUT CONTRACTS THAT CALLERS MUST HONOUR
---------------------------------------------
1. `reusable` is not advisory. A hit with `reusable: false` carries a
   `reuse_block` reason (`volatile`, `contested`, `single-source`, `no-as-of`,
   `low-confidence`) and MUST be re-verified against a live source before it
   is restated. Reusing a stale volatile metric under the authority of
   "already in the store" is the specific failure this field exists to
   prevent. Only `reusable: true` hits may be cited directly, and even then
   the `as_of` travels with the claim into the new article.

2. `--candidates` emits CANDIDATES, never verdicts. It shortlists prior
   claims that overlap the query strongly AND carry a differing number of the
   same unit. That is a deterministic heuristic, not semantic contradiction
   detection: two claims can differ numerically and both be true (different
   period, scope, or entity). The agent adjudicates. A false "we contradicted
   ourselves" is worse than silence, because it invites rewriting a correct
   claim to resolve a conflict that does not exist. This mirrors the
   dedupe_headline_alerts.py -> headline_judge.py split already used for
   headline dedupe.

Scoring: Okapi BM25 over a per-claim bag of tokens assembled from weighted
fields — the claim sentence itself is heaviest, then the article title, tags
and cited hosts. The IDF term is clamped to >= 0 so terms appearing in more
than half the corpus do not become anti-signal.

stdlib only.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "research" / "claims" / "index.json"

# Reuse the builder's tokenizer/normalizers so the read and write sides can
# never drift apart on what counts as a token or a host.
from build_claim_index import canonical_url, normalize_host, tokenize  # noqa: E402

K1 = 1.5
B = 0.75

FIELD_WEIGHTS = {"claim": 3, "title": 1, "tags": 1, "hosts": 1}

# Token-overlap floor for --candidates. Below this the two claims are not
# plausibly about the same fact and a numeric difference means nothing.
CANDIDATE_MIN_JACCARD = 0.28
# Two numbers of the same unit within this relative distance are treated as
# the same figure restated (rounding), not a disagreement.
CANDIDATE_REL_TOL = 0.02


def load_index(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(
            f"error: no claim index at {path}. Build it with "
            "`uv run python scripts/build_claim_index.py`"
        )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise SystemExit(f"error: could not read claim index: {exc}") from exc


def _doc_tokens(claim: dict[str, Any]) -> list[str]:
    bag: list[str] = []
    bag += tokenize(claim.get("claim", "")) * FIELD_WEIGHTS["claim"]
    bag += tokenize(claim.get("article_title", "")) * FIELD_WEIGHTS["title"]
    bag += tokenize(" ".join(claim.get("hosts", []))) * FIELD_WEIGHTS["hosts"]
    return bag


def bm25(query: str, claims: list[dict[str, Any]]) -> list[tuple[float, dict[str, Any]]]:
    q = tokenize(query)
    if not q:
        return []
    docs = [_doc_tokens(c) for c in claims]
    lens = [len(d) or 1 for d in docs]
    avg = sum(lens) / len(lens) if lens else 1.0
    n = len(docs)

    df: Counter[str] = Counter()
    tfs: list[Counter[str]] = []
    for d in docs:
        tf = Counter(d)
        tfs.append(tf)
        for term in set(q):
            if tf.get(term):
                df[term] += 1

    scored: list[tuple[float, dict[str, Any]]] = []
    for i, claim in enumerate(claims):
        score = 0.0
        for term in q:
            f = tfs[i].get(term, 0)
            if not f:
                continue
            # Clamp IDF at 0: with a small corpus a term in >half the docs
            # would otherwise score negative and actively demote good hits.
            idf = max(0.0, math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5)))
            score += idf * (f * (K1 + 1)) / (f + K1 * (1 - B + B * lens[i] / avg))
        if score > 0:
            scored.append((score, claim))
    scored.sort(key=lambda t: (-t[0], t[1]["key"]))
    return scored


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def find_candidates(query: str, index: dict[str, Any]) -> list[dict[str, Any]]:
    """Shortlist prior claims that may disagree with `query`. NOT a verdict."""
    q_tokens = set(tokenize(query))
    q_nums = _numerics_of(query)
    out: list[dict[str, Any]] = []
    for claim in index.get("claims", []):
        overlap = _jaccard(q_tokens, set(tokenize(claim.get("claim", ""))))
        if overlap < CANDIDATE_MIN_JACCARD:
            continue
        # Recomputed from the claim text rather than read from the index —
        # figures are derivable, so storing them would only create a second
        # copy free to drift from the sentence it describes.
        diffs = _numeric_conflicts(q_nums, _numerics_of(claim.get("claim", "")))
        if not diffs:
            continue
        out.append(
            {
                "key": claim["key"],
                "claim": claim["claim"],
                "article": claim["article"],
                "as_of": claim.get("as_of", ""),
                "risk": claim.get("risk", ""),
                "confidence": claim.get("confidence", ""),
                "source_urls": claim.get("source_urls", []),
                "token_overlap": round(overlap, 3),
                "numeric_differences": diffs,
                "note": (
                    "CANDIDATE ONLY — overlapping wording with a differing "
                    "figure. May be a different period, scope or entity. "
                    "Adjudicate against the sources before treating this as a "
                    "contradiction."
                ),
            }
        )
    out.sort(key=lambda c: (-c["token_overlap"], c["key"]))
    return out


def _numerics_of(text: str) -> list[dict[str, Any]]:
    from build_claim_index import extract_numerics

    return extract_numerics(text)


def _numeric_conflicts(
    a: list[dict[str, Any]], b: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Query figures that have NO counterpart in the stored claim.

    This is a MATCHING problem, not a cross-product. A sentence carries
    several unrelated numbers ("revenue $215.9B, up 65%, Data Center up
    68%"), so comparing every number against every same-unit number
    manufactures conflicts out of an identical claim — 65% "disagreeing"
    with 68% when they are simply different quantities. That false positive
    is worse than silence: it invites the agent to rewrite a correct claim
    to resolve a contradiction that does not exist.

    So: greedily pair each query figure with an equal (within rounding
    tolerance) stored figure of the same unit and consume it. Only figures
    left unpaired are evidence of disagreement — and only when the stored
    claim has some same-unit figure to disagree WITH. A query figure with
    no comparable counterpart at all is extra information, not a conflict.
    """
    diffs: list[dict[str, Any]] = []
    pool = list(b)
    for x in a:
        matched = None
        for i, y in enumerate(pool):
            if x["unit"] != y["unit"]:
                continue
            hi = max(abs(x["value"]), abs(y["value"]))
            rel = 0.0 if hi == 0 else abs(x["value"] - y["value"]) / hi
            if rel <= CANDIDATE_REL_TOL:
                matched = i
                break
        if matched is not None:
            pool.pop(matched)
            continue
        rivals = [y for y in pool if y["unit"] == x["unit"]]
        if not rivals:
            # Nothing comparable in the stored claim — not a disagreement.
            continue
        nearest = min(rivals, key=lambda y: abs(y["value"] - x["value"]))
        hi = max(abs(x["value"]), abs(nearest["value"])) or 1.0
        diffs.append(
            {
                "query_figure": x["raw"],
                "stored_figure": nearest["raw"],
                "unit": x["unit"],
                "relative_difference": round(abs(x["value"] - nearest["value"]) / hi, 4),
            }
        )
    return diffs


def _fmt(claim: dict[str, Any], score: float | None = None) -> str:
    head = f"{claim['key']}"
    if score is not None:
        head += f"  score={score:.2f}"
    flag = "REUSABLE" if claim.get("reusable") else f"RE-VERIFY ({claim.get('reuse_block')})"
    meta = f"    [{claim.get('type','?')}] as_of={claim.get('as_of') or '-'} risk={claim.get('risk') or '-'} conf={claim.get('confidence') or '-'}  {flag}"
    text = f"    {claim.get('claim','')}"
    srcs = claim.get("source_urls") or []
    src = f"    sources: {', '.join(srcs[:3])}{' …' if len(srcs) > 3 else ''}" if srcs else "    sources: (none)"
    return "\n".join([head, meta, text, src])


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("query", nargs="?", default="", help="free-text query")
    p.add_argument("--top", type=int, default=8, help="max results (default 8)")
    p.add_argument("--json", action="store_true", help="emit JSON")
    p.add_argument("--host", help="filter to claims citing this host")
    p.add_argument("--url", help="exact source-URL lookup")
    p.add_argument(
        "--candidates",
        action="store_true",
        help="shortlist prior claims that may disagree with the query (NOT a verdict)",
    )
    p.add_argument(
        "--reusable-only",
        action="store_true",
        help="return only claims safe to cite without re-verification",
    )
    p.add_argument("--index", default=str(INDEX_PATH), help="index path")
    args = p.parse_args(argv)

    index = load_index(Path(args.index))
    claims: list[dict[str, Any]] = index.get("claims", [])
    by_key = {c["key"]: c for c in claims}

    if args.candidates:
        if not args.query:
            print("error: --candidates needs a query", file=sys.stderr)
            return 2
        cands = find_candidates(args.query, index)[: args.top]
        if args.json:
            print(json.dumps({"candidates": cands}, indent=2, ensure_ascii=False))
        elif not cands:
            print("No overlapping prior claims with a differing figure.")
        else:
            print(
                f"{len(cands)} CANDIDATE(S) — overlapping wording, differing figure. "
                "Adjudicate; do not assume contradiction.\n"
            )
            for c in cands:
                print(f"{c['key']}  overlap={c['token_overlap']} as_of={c['as_of'] or '-'}")
                print(f"    {c['claim']}")
                for d in c["numeric_differences"][:3]:
                    print(f"    ! query {d['query_figure']} vs stored {d['stored_figure']} ({d['unit']})")
                print()
        return 0

    if args.url:
        keys = index.get("by_url", {}).get(canonical_url(args.url), [])
        hits = [by_key[k] for k in keys if k in by_key]
    elif args.host and not args.query:
        keys = index.get("by_host", {}).get(normalize_host("https://" + args.host), [])
        if not keys:
            keys = index.get("by_host", {}).get(args.host.lower(), [])
        hits = [by_key[k] for k in keys if k in by_key]
    else:
        scored = bm25(args.query, claims)
        if args.host:
            h = args.host.lower()
            scored = [(s, c) for s, c in scored if h in c.get("hosts", [])]
        hits = [c for _, c in scored]
        if args.reusable_only:
            hits = [c for c in hits if c.get("reusable")]
        hits = hits[: args.top]
        if args.json:
            print(json.dumps({"results": hits}, indent=2, ensure_ascii=False))
        else:
            if not hits:
                print("No matching prior claims.")
            else:
                print(f"{len(hits)} prior claim(s) — honour `reusable`; RE-VERIFY hits need a live source.\n")
            score_by_key = {c["key"]: s for s, c in scored}
            for c in hits:
                print(_fmt(c, score_by_key.get(c["key"])))
                print()
        return 0

    if args.reusable_only:
        hits = [c for c in hits if c.get("reusable")]
    hits = hits[: args.top]
    if args.json:
        print(json.dumps({"results": hits}, indent=2, ensure_ascii=False))
    else:
        if not hits:
            print("No matching prior claims.")
        else:
            print(f"{len(hits)} prior claim(s) — honour `reusable`; RE-VERIFY hits need a live source.\n")
        for c in hits:
            print(_fmt(c))
            print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
