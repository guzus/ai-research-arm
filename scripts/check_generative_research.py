#!/usr/bin/env python3
"""Compile-check a generative research article body without committing.

Runs the same validation rules write_generative_research.py enforces at
commit time — tag allowlist, ara-* exact-match class allowlist parsed
from COMPONENTS.md (modifier suffixes allowed), size cap, no inline
style/script/JS handlers, opening/closing <article> structure.

Optional design-system enforcement flags (off by default so check
stays additive):
  --diversity-min N   fail if fewer than N distinct visualization
                      primitives are used. Counts ara-line-chart,
                      ara-donut, ara-slope, ara-stack-bar,
                      ara-stack-rows, ara-bars, ara-rank-list,
                      ara-compare, ara-iso, ara-sparkline,
                      ara-timeline, ara-kv. ara-table and ara-callout
                      are NOT counted — they're the safe defaults.
  --callout-max M     fail if more than M ara-callout blocks. Use to
                      stop agents from reaching for callouts as
                      cosmetic emphasis (a common failure mode).
  --strict-shape      WARN (not fail) when the article has 5+
                      standalone percentages in prose but no
                      distribution viz (donut, stack-bar, bars,
                      rank-list). This catches the "179 percentages,
                      zero donuts" pattern the corpus audit surfaced.

Optional research-quality gates (also off by default). Each is a
hard fail when the flag is passed. These convert the prose targets
in the workflow prompt into deterministic build checks:
  --cite-density-min FLOAT  minimum cited claims per 1,000 words.
                            Counts <a class="ara-cite"> markers /
                            (words / 1000). Workflow default: 10.0.
                            (Corpus audit: 4 articles shipped at 0.0
                             density before this gate existed.)
  --refs-min INT            minimum entries in the <ol class="ara-refs">
                            references list (counted by id="ref-N" li
                            elements). Workflow default: 20.
  --primary-share-min FLOAT minimum share (0.0-1.0) of references
                            whose host is a primary source. Primary =
                            *.gov, *.edu, arxiv.org, first-party AI/
                            chip-lab domains, official IR/blogs.
                            Heuristic — see PRIMARY_HOST_SUFFIXES.
                            Recommended >= 0.30 once calibrated.
  --cited-claims-min FLOAT  minimum share (0.0-1.0) of "substantive"
                            sentences that carry at least one cite
                            marker. Substantive = sentence containing
                            a digit, '%', '$', or 2+ adjacent
                            capitalized words / a 3+ char all-caps
                            token. Heuristic; high false-positive on
                            section headings — start conservative.

Exit status:
  0  — body is valid; safe to commit
  1  — body fails validation; the error is printed to stderr with
        specific fixes (e.g. "undocumented class ara-references → did
        you mean: ara-eyebrow")
  2  — argv error / file missing

Usage:
  python3 scripts/check_generative_research.py /tmp/gen-research-body.html
  python3 scripts/check_generative_research.py - < body.html     # stdin
  python3 scripts/check_generative_research.py path --kind standalone
  python3 scripts/check_generative_research.py path --diversity-min 3 --callout-max 5
  python3 scripts/check_generative_research.py path --cite-density-min 10 --refs-min 20

The agent loop in the workflow / local skill: write the body, run this
check, fix anything it reports, re-check, and only then call the real
writer to commit. Deterministic — no agent self-validation needed.
"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# Reuse the writer's validator so this script and the commit-time check
# stay in lockstep — if one accepts a body, so does the other.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from write_generative_research import (  # noqa: E402
    KIND_FRAGMENT,
    KINDS,
    detect_dsl,
    read_body,
    validate_body,
)
from compile_ara import AraSyntaxError, compile_source  # noqa: E402

# Component classification, keep in lockstep with ARA_DSL.md / COMPONENTS.md.
VIZ_PRIMITIVES = frozenset([
    "ara-line-chart", "ara-donut", "ara-slope",
    "ara-stack-bar", "ara-stack-rows",
    "ara-bars", "ara-rank-list", "ara-compare",
    "ara-iso", "ara-sparkline", "ara-timeline", "ara-kv",
])
DISTRIBUTION_VIZ = frozenset([
    "ara-donut", "ara-stack-bar", "ara-stack-rows",
    "ara-bars", "ara-rank-list",
])
FALLBACK_PRIMITIVES = frozenset(["ara-table", "ara-callout", "ara-quote"])

# ---------------------------------------------------------------------------
# Quality-gate heuristics — convert prose targets into deterministic checks.
# ---------------------------------------------------------------------------
#
# A "primary source" is one whose host matches a documented suffix. This is
# heuristic; calibrated against the corpus in research/generative/* — the
# task accepts that the list will need pruning over time. Keep the suffix
# list small and well-justified rather than spraying every dot-com.
PRIMARY_HOST_SUFFIXES = (
    # Government, military, intergovernmental
    ".gov", ".gov.uk", ".mil", ".int",
    # Academic + research institutions
    ".edu", ".ac.uk", ".ac.jp",
    # Preprint + peer-reviewed repositories
    "arxiv.org", "openreview.net", "biorxiv.org", "medrxiv.org",
    "ncbi.nlm.nih.gov", "pubmed.ncbi.nlm.nih.gov", "europepmc.org",
    "semanticscholar.org", "ssrn.com", "openalex.org",
    # AI / ML / research-lab primary
    "anthropic.com", "openai.com", "deepmind.com", "deepmind.google",
    "ai.meta.com", "research.facebook.com", "transformer-circuits.pub",
    "huggingface.co", "x.ai", "mistral.ai", "cohere.com",
    # Cloud / chip / infra primaries (corp domains + dev portals)
    "google.com", "research.google", "blog.google", "googleblog.com",
    "microsoft.com", "azure.microsoft.com",
    "aws.amazon.com", "amazon.com", "amazon.science",
    "nvidia.com", "amd.com", "intel.com", "apple.com",
    "developer.apple.com",
    "mlcommons.org",
    # Chip / inference vendor primaries observed in the corpus
    "cerebras.ai", "cerebras.net", "groq.com", "fireworks.ai",
    "together.ai", "deepinfra.com", "replicate.com", "deepseek.com",
    # Standards bodies
    "ietf.org", "w3.org", "rfc-editor.org", "iso.org",
)
# Hosts that EXACTLY match these get marked primary regardless of suffix
# matching. Use sparingly — for explicit IR / first-party portals.
PRIMARY_HOST_EXACT = frozenset({
    "investor.natera.com", "investor.bloomenergy.com",
    "investor.cerebras.net", "ir.coreweave.com", "ir.iren.com",
    "iris.energy",
    # GitHub source URLs count as primary for code/docs claims
    "github.com",
})


def _normalize_host(host: str) -> str:
    h = host.lower().strip()
    if h.startswith("www."):
        h = h[4:]
    return h


def is_primary_source(host: str | None) -> bool:
    if not host:
        return False
    h = _normalize_host(host)
    if h in PRIMARY_HOST_EXACT:
        return True
    for suf in PRIMARY_HOST_SUFFIXES:
        # suffix match supports both `.gov` (matches `data.gov`) and
        # `arxiv.org` (matches `www.arxiv.org` after the strip above)
        if h == suf.lstrip("."):
            return True
        if h.endswith(suf):
            return True
    return False


class _ReferenceHrefCollector(HTMLParser):
    """Walks the HTML and collects URLs found INSIDE `<li id="ref-N">`
    items — i.e. the references list. Plain in-body links don't count
    (they're often footnote anchors like #ref-5, not source URLs).

    Tracks two metrics:
      * `ref_urls`: every http(s) URL found inside a ref-li (one entry
                    may have multiple — used by primary_share).
      * `refs_with_urls`: count of distinct ref-li entries that
                    contained at least one URL (used by count_references
                    to gate against "20 title-only refs" attack)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._depth_in_ref_li = 0
        self._current_ref_has_url = False
        self.ref_urls: list[str] = []
        self.refs_with_urls: int = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "li" and a.get("id", "").startswith("ref-"):
            self._depth_in_ref_li = 1
            self._current_ref_has_url = False
            return
        if self._depth_in_ref_li > 0:
            if tag == "li":  # nested li, unusual but possible
                self._depth_in_ref_li += 1
            if tag == "a":
                href = a.get("href", "")
                if href.startswith(("http://", "https://")):
                    self.ref_urls.append(href)
                    self._current_ref_has_url = True

    def handle_endtag(self, tag):
        if tag == "li" and self._depth_in_ref_li > 0:
            self._depth_in_ref_li -= 1
            if self._depth_in_ref_li == 0:
                # We just closed the outermost ref-li; commit its
                # has-url flag to the counter.
                if self._current_ref_has_url:
                    self.refs_with_urls += 1
                self._current_ref_has_url = False


def _word_count(body_html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", body_html)
    return len(text.split())


def count_cite_markers(body_html: str) -> int:
    """How many citation superscripts appear in the article body. We
    count the rendered ara-cite class (one per [^N] in the DSL). Multi-
    cite footnotes (`[^1,2,3]`) compile to 3 separate <a class="ara-cite">
    spans so each gets counted — that matches the "claims with cite"
    intent more closely than counting outer <sup> wrappers would."""
    return len(re.findall(r'class="ara-cite', body_html))


def count_references(body_html: str) -> int:
    """How many references list entries carry at least one http(s) URL.

    Previously counted every `<li id="ref-N">` regardless of whether
    the entry actually had a source URL. An article with 20 title-only
    or duplicate-href references could pass `--refs-min 20` with zero
    real sources — defeating the gate's intent. We now count distinct
    ref-li elements that produced at least one `<a href="http(s)://…">`
    inside them. Mixed lists (some entries with URLs, some without)
    still count the URL-bearing entries — tolerant of legitimate
    no-URL entries like personal-communication citations, strict
    against pure-title attack patterns.
    """
    collector = _ReferenceHrefCollector()
    collector.feed(body_html)
    return collector.refs_with_urls


def primary_share(body_html: str) -> tuple[float, int, int]:
    """Return (share, primary_count, total_refs) of references whose
    host is a primary source. Share is 0.0 when no refs exist."""
    collector = _ReferenceHrefCollector()
    collector.feed(body_html)
    refs = collector.ref_urls
    if not refs:
        return 0.0, 0, 0
    primary = 0
    for url in refs:
        m = re.match(r"^https?://([^/]+)", url)
        host = m.group(1) if m else None
        if is_primary_source(host):
            primary += 1
    return primary / len(refs), primary, len(refs)


_SUBSTANTIVE_NE = re.compile(r"\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)+|\b[A-Z]{3,}\b")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_CITE_MARKER = "\x00CITE\x00"


def cited_claim_share(body_html: str) -> tuple[float, int, int]:
    """Heuristic: among substantive sentences, what share carries a cite?

    Substantive = sentence contains a digit, '%', '$', OR a named-entity
    proxy (two-or-more adjacent capitalized words, or a 3+ char ALL-CAPS
    token). This catches "$2.3B in Q4 2026" and "Cerebras WSE-3" but
    also section headings — false-positive expected.

    We pre-substitute `<sup>…<a class="ara-cite">…</a>…</sup>` with a
    sentinel so cite presence survives the strip-tags pass.

    Returns (share, cited_substantive, total_substantive). Share is 0.0
    when no substantive sentences exist (empty/HTML-only body).
    """
    marked = re.sub(
        r'<sup[^>]*>\s*<a[^>]*class="ara-cite"[^>]*>[^<]*</a>\s*</sup>',
        f" {_CITE_MARKER} ",
        body_html,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"<[^>]+>", " ", marked)
    sents = _SENT_SPLIT.split(text)
    total = 0
    cited = 0
    for s in sents:
        if not s.strip():
            continue
        clean = s.replace(_CITE_MARKER, "")
        is_subs = (
            any(c.isdigit() for c in clean)
            or "%" in clean
            or "$" in clean
            or bool(_SUBSTANTIVE_NE.search(clean))
        )
        if is_subs:
            total += 1
            if _CITE_MARKER in s:
                cited += 1
    if total == 0:
        return 0.0, 0, 0
    return cited / total, cited, total


def cite_density(body_html: str) -> tuple[float, int, int]:
    """Citations per 1000 words. Returns (density, cites, words)."""
    cites = count_cite_markers(body_html)
    words = _word_count(body_html)
    if words == 0:
        return 0.0, cites, 0
    return (cites / words) * 1000.0, cites, words


def enforce_quality(body_html: str, args: argparse.Namespace) -> list[str]:
    """Return a list of quality-gate failure messages. Empty = pass.
    Only the flags that were explicitly set are checked."""
    errors: list[str] = []

    if args.cite_density_min is not None:
        density, cites, words = cite_density(body_html)
        if density < args.cite_density_min:
            errors.append(
                f"quality: cite density {density:.2f}/1k words "
                f"({cites} cites in {words} words), need >= "
                f"{args.cite_density_min:.2f}. Add citations to the "
                f"claims that lack them — the gate counts <sup>"
                f"<a class=\"ara-cite\">N</a></sup> markers."
            )

    if args.refs_min is not None:
        refs = count_references(body_html)
        if refs < args.refs_min:
            errors.append(
                f"quality: only {refs} reference entries, need >= "
                f"{args.refs_min}. The references list is the "
                f":::references block at the bottom of the article."
            )

    if args.primary_share_min is not None:
        share, prim, total = primary_share(body_html)
        if total == 0:
            errors.append(
                "quality: no reference URLs found in the article; "
                "cannot evaluate primary-source share. The references "
                "block (li elements with id='ref-N') is missing or "
                "has no http(s):// links."
            )
        elif share < args.primary_share_min:
            errors.append(
                f"quality: primary-source share {share*100:.1f}% "
                f"({prim}/{total} refs), need >= "
                f"{args.primary_share_min*100:.1f}%. Primary = "
                f".gov/.edu, arxiv, official AI-lab / chip-vendor / "
                f"infra-vendor blogs and IR. See PRIMARY_HOST_SUFFIXES "
                f"in scripts/check_generative_research.py for the list. "
                f"Replace TechCrunch / Bloomberg / sell-side commentary "
                f"with the underlying SEC filing, paper, IR page, or "
                f"first-party blog."
            )

    if args.cited_claims_min is not None:
        share, cited, total = cited_claim_share(body_html)
        if total == 0:
            errors.append(
                "quality: no substantive sentences detected — article "
                "body may be empty or HTML-only."
            )
        elif share < args.cited_claims_min:
            errors.append(
                f"quality: cited-claim share {share*100:.1f}% "
                f"({cited}/{total} substantive sentences carry a "
                f"<sup><a class=\"ara-cite\">…</a></sup> marker), need "
                f">= {args.cited_claims_min*100:.1f}%. Substantive = "
                f"sentence with a digit, '%', '$', or a multi-word "
                f"capitalized phrase. Heuristic — section headings "
                f"may inflate the denominator; consider raising the "
                f"threshold once measured."
            )

    return errors


# Citation marker patterns we strip before matching verifier-findings
# probes against the body. The verifier reads the .ara.md DSL (which
# uses `[^N]` / `[^1,2,3]`) but the body we compare against is the
# compiled HTML (which renders `[^N]` as `<sup><a class="ara-cite">N</a></sup>`).
# Without normalization, a probe containing `[^12]` will never match a
# body containing `<sup>...12...</sup>` → surviving unsupported claim
# is treated as "removed" → false pass.
_DSL_CITE_MARKER_RE = re.compile(r"\[\^[0-9,\s]+\]")
_RENDERED_CITE_RE = re.compile(
    r'<sup[^>]*>\s*<a[^>]*class="ara-cite"[^>]*>[^<]*</a>\s*</sup>',
    flags=re.IGNORECASE,
)


def _strip_cite_markers(s: str) -> str:
    """Remove both DSL `[^N]` and rendered `<sup><a class="ara-cite">…</a></sup>`
    citation markers so verifier-findings text (DSL-shape) and HTML
    body text (rendered-shape) match each other after normalization."""
    s = _RENDERED_CITE_RE.sub(" ", s)
    s = _DSL_CITE_MARKER_RE.sub(" ", s)
    return s


def audit_verifier_findings(
    findings_path: Path, body_html: str
) -> tuple[int, list[dict]]:
    """Check that every `unsupported` claim flagged by the verifier
    sub-agent was either demoted (wrapped in `<mark>` / `==…==`) or
    removed during bounded revision.

    The verifier writes a structured findings JSON at the path passed
    to this function:

        {"claims": [
            {"id": "c1", "text": "<verbatim claim text>",
             "verdict": "supported|weak|unsupported",
             "citation": "<url or null>"},
            ...
        ]}

    Heuristic: strip citation markers (both DSL `[^N]` and the rendered
    `<sup><a class="ara-cite">N</a></sup>` form) from BOTH the claim
    text and the body before normalizing. The verifier reads DSL; the
    compiled HTML we audit uses the rendered form. Without stripping
    on both sides, any cited claim looks "removed" because the marker
    shapes never match. The first ~80 chars of the normalized text is
    the probe. If the probe appears in the body text AND is not inside
    a `<mark>…</mark>` region, the claim survived without being
    demoted → fail.

    Limitations (call out in PR + reviewer-facing docs):
      * Whole-claim-demotion semantics: if the agent demotes only the
        load-bearing number inside a longer claim sentence, the probe
        may match in body-text but NOT inside the mark region → false
        fail. Acceptable — pushes the agent toward marking the whole
        sentence.
      * Paraphrase-on-revision: if the agent rewrites the claim text
        on revision, the probe won't match anywhere → treated as
        "removed" → pass. Acceptable — paraphrase to a supported
        variant is a valid bounded-revision outcome.

    Returns (unsupported_total, surviving) where `surviving` is a list
    of dicts {id, probe, citation} for every unsupported claim that
    failed the audit. Empty `surviving` = pass.

    Raises ValueError if the findings JSON is malformed.
    """
    import json as _json

    try:
        data = _json.loads(findings_path.read_text(encoding="utf-8"))
    except (_json.JSONDecodeError, OSError) as e:
        raise ValueError(f"could not parse verifier findings JSON: {e}") from e

    claims = data.get("claims") if isinstance(data, dict) else None
    if not isinstance(claims, list):
        raise ValueError(
            "verifier findings JSON missing top-level 'claims' array; "
            f"got: {type(data).__name__}"
        )

    # Strip cite markers on the HTML side BEFORE tag-stripping so the
    # rendered <sup>…</sup> wrapper disappears cleanly. Then strip
    # remaining HTML tags. Both DSL and rendered citation forms are
    # gone, so the probe and body live on equal footing.
    body_decited = _strip_cite_markers(body_html)
    text_no_tags = re.sub(r"<[^>]+>", " ", body_decited)
    mark_regions: list[str] = re.findall(
        r"<mark[^>]*>(.*?)</mark>", body_html, flags=re.DOTALL | re.IGNORECASE
    )
    # Same cite-stripping inside the mark regions — claim text inside
    # a <mark> wrapper can also carry a `<sup>…</sup>` cite, and we
    # want it to match a DSL-shaped probe. ALSO strip remaining HTML
    # tags from inside the mark; demoted sentences may contain inline
    # markup (`<em>`, `<strong>`, `<a>`, `<code>`) that would
    # otherwise leave the mark blob in a different shape from the
    # tag-stripped body, causing valid demotions to fail the audit.
    mark_blob = re.sub(
        r"<[^>]+>",
        " ",
        " ".join(_strip_cite_markers(m) for m in mark_regions),
    )

    def _norm(s: str) -> str:
        return re.sub(r"\s+", " ", s).strip().lower()

    body_norm = _norm(text_no_tags)
    mark_norm = _norm(mark_blob)

    surviving: list[dict] = []
    unsupported_total = 0
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        verdict = str(claim.get("verdict", "")).lower()
        if verdict != "unsupported":
            continue
        unsupported_total += 1
        text = str(claim.get("text", "")).strip()
        if not text:
            # Verifier flagged a claim but gave no body text — we
            # can't audit. Treat as "needs manual review" by skipping
            # rather than failing (the verifier itself flagged the
            # missing data; rerun policy is upstream).
            continue
        # Strip cites from the probe text too, so a DSL-shaped probe
        # like "Nvidia hit 75% margin [^12]" doesn't fail to match a
        # body whose corresponding sentence has already had the cite
        # stripped from the HTML side.
        probe = _norm(_strip_cite_markers(text))[:80]
        if not probe:
            continue
        if probe in body_norm and probe not in mark_norm:
            surviving.append(
                {
                    "id": claim.get("id"),
                    "probe": probe,
                    "citation": claim.get("citation"),
                }
            )

    return unsupported_total, surviving


def count_classes(body_html: str) -> dict[str, int]:
    """Return a {class_name: count} map of every ara-* class in the
    article's HTML output, after compile."""
    counts: dict[str, int] = {}
    for cls in re.findall(r'class="(ara-[a-z0-9-]+(?:--[a-z0-9-]+)?)', body_html):
        counts[cls] = counts.get(cls, 0) + 1
    return counts


def count_standalone_percentages(body_html: str) -> int:
    """How many `\\d+%` tokens appear in flow text (not inside an
    `ara-bar-value` or `ara-stat-value`, where they're already
    visualized)."""
    text = re.sub(r'<(span|div)[^>]*class="ara-(bar-value|stat-value|rank-value|compare-value)"[^>]*>.*?</\1>',
                  ' ', body_html, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\b\d+(?:\.\d+)?\s?%", text))


def enforce_design(body_html: str, args: argparse.Namespace) -> list[str]:
    """Return a list of error messages. Empty list = pass."""
    errors: list[str] = []
    counts = count_classes(body_html)

    viz_used = {c for c in counts if c in VIZ_PRIMITIVES}
    if args.diversity_min is not None and len(viz_used) < args.diversity_min:
        sample = sorted(VIZ_PRIMITIVES - viz_used)[:6]
        errors.append(
            f"design: only {len(viz_used)} distinct viz primitive(s) used "
            f"({sorted(viz_used) or 'none'}), need ≥ {args.diversity_min}. "
            f"Reach for one of: {', '.join(sample)}."
        )

    callout_count = counts.get("ara-callout", 0)
    if args.callout_max is not None and callout_count > args.callout_max:
        errors.append(
            f"design: {callout_count} ara-callout blocks, max is "
            f"{args.callout_max}. Callouts are for thesis breaks / risk "
            f"flags only — most of these belong as inline prose or as "
            f"a structured viz (donut, stack-bar, kv)."
        )
    return errors


def soft_warnings(body_html: str) -> list[str]:
    """Non-fatal heuristics that nag at common design-system anti-
    patterns surfaced by the corpus audit. Printed to stderr but
    don't change exit status."""
    warns: list[str] = []
    counts = count_classes(body_html)
    pct = count_standalone_percentages(body_html)
    distribution_used = any(counts.get(c, 0) > 0 for c in DISTRIBUTION_VIZ)
    if pct >= 5 and not distribution_used:
        warns.append(
            f"warn: article cites {pct} standalone percentages in prose "
            f"but uses ZERO distribution viz (donut / stack-bar / bars / "
            f"rank-list). The data shape supports a viz; consider whether "
            f"a `:::donut` or `:::stack-bar` would replace prose."
        )
    callout_count = counts.get("ara-callout", 0)
    viz_count = sum(counts.get(c, 0) for c in VIZ_PRIMITIVES)
    if callout_count >= 5 and viz_count <= 1:
        warns.append(
            f"warn: {callout_count} callouts but only {viz_count} viz "
            f"primitive(s) — callouts are doing the visual heavy lifting. "
            f"That usually means a few of them want to be `:::kv` or `:::stats`."
        )
    return warns


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "body_path",
        help="path to the article body (use '-' to read from stdin)",
    )
    p.add_argument(
        "--kind",
        default=KIND_FRAGMENT,
        choices=KINDS,
        help="fragment (default) or standalone",
    )
    p.add_argument(
        "--diversity-min",
        type=int,
        default=None,
        help="fail if fewer than N distinct viz primitives are used",
    )
    p.add_argument(
        "--callout-max",
        type=int,
        default=None,
        help="fail if more than M ara-callout blocks are used",
    )
    p.add_argument(
        "--strict-shape",
        action="store_true",
        help="enable soft-warning heuristics (percentages-without-donut, etc.)",
    )
    # Research-quality gates. None = inactive (preserves backward-compat for
    # the bare `check_generative_research.py path.html` invocation). The
    # workflow passes explicit thresholds in step 7.5.
    p.add_argument(
        "--cite-density-min",
        type=float,
        default=None,
        metavar="FLOAT",
        help=(
            "fail if cite density < N citations per 1,000 words. "
            "Recommended workflow value: 10.0 (corpus-validated; "
            "discriminates 0-cite articles from 100+ cite articles)."
        ),
    )
    p.add_argument(
        "--refs-min",
        type=int,
        default=None,
        metavar="INT",
        help=(
            "fail if the references list has < N entries. "
            "Recommended workflow value: 20."
        ),
    )
    p.add_argument(
        "--primary-share-min",
        type=float,
        default=None,
        metavar="FLOAT",
        help=(
            "fail if < FLOAT (0-1) of references are from primary sources. "
            "Heuristic via PRIMARY_HOST_SUFFIXES; calibrate before "
            "wiring into the build gate."
        ),
    )
    p.add_argument(
        "--cited-claims-min",
        type=float,
        default=None,
        metavar="FLOAT",
        help=(
            "fail if < FLOAT (0-1) of substantive sentences carry a "
            "cite marker. Substantive = sentence with a digit, percent "
            "sign, dollar sign, or named-entity proxy. Heuristic with "
            "high false-positive on headings; calibrate before wiring "
            "into the build gate."
        ),
    )
    # Verifier-findings audit mode. When this flag is set we skip
    # validate_body / design / quality gates and instead audit the
    # body against the verifier sub-agent's JSON artifact. The
    # workflow's "bounded revision" step (step 7 of the agent prompt)
    # is otherwise unobservable from the build — this gate makes it
    # auditable.
    p.add_argument(
        "--audit-verifier-findings",
        type=str,
        default=None,
        metavar="PATH",
        help=(
            "path to .gen-verifier-findings.json written by the "
            "verifier sub-agent. When set, the script switches to "
            "audit mode: validates the JSON and fails if any "
            "unsupported claim survived in the body without being "
            "demoted (<mark>) or removed."
        ),
    )
    args = p.parse_args(argv)

    if args.body_path != "-" and not Path(args.body_path).exists():
        print(f"check: body file not found: {args.body_path}", file=sys.stderr)
        return 2

    try:
        raw = read_body(args.body_path)
    except OSError as e:
        print(f"check: read failed: {e}", file=sys.stderr)
        return 2

    is_dsl = detect_dsl(args.body_path, raw)
    if is_dsl:
        try:
            body = compile_source(raw)
        except AraSyntaxError as e:
            print(f"check: DSL compile failed: {e}", file=sys.stderr)
            return 1
    else:
        body = raw

    # Verifier-findings audit mode. Runs ONLY when --audit-verifier-findings
    # is set. Bypasses validate_body / design / quality so the audit can run
    # against a fully-committed (already-validated) article without redoing
    # those checks.
    if args.audit_verifier_findings:
        findings_path = Path(args.audit_verifier_findings)
        if not findings_path.exists():
            print(
                f"check: verifier findings file not found: {findings_path}",
                file=sys.stderr,
            )
            return 2
        try:
            total, surviving = audit_verifier_findings(findings_path, body)
        except ValueError as e:
            print(f"check: {e}", file=sys.stderr)
            return 1
        print(
            f"verifier-findings audit: {total} unsupported claim(s) "
            f"flagged; {len(surviving)} still present in the body outside "
            f"a <mark> region.",
            file=sys.stderr,
        )
        if surviving:
            print(
                "Bounded revision failed: the following unsupported "
                "claims were not demoted or removed:",
                file=sys.stderr,
            )
            for c in surviving[:10]:
                print(
                    f"  - id={c['id']}: {c['probe']!r}",
                    file=sys.stderr,
                )
            if len(surviving) > 10:
                print(
                    f"  ... and {len(surviving) - 10} more",
                    file=sys.stderr,
                )
            return 1
        return 0

    try:
        validate_body(body, args.kind)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    # Design-system gates (only active when explicitly opted in).
    if args.kind == KIND_FRAGMENT and (
        args.diversity_min is not None or args.callout_max is not None
    ):
        errors = enforce_design(body, args)
        if errors:
            for line in errors:
                print(line, file=sys.stderr)
            print(
                "Design gates failed. Either restructure the article to "
                "use more primitives, or relax the threshold for this run.",
                file=sys.stderr,
            )
            return 1

    # Research-quality gates (deterministic checks for the QUALITY TARGETS
    # the workflow prompt documents in prose). Each gate is opt-in; absent
    # flags = no check. Same kind=fragment scope as the design gates.
    if args.kind == KIND_FRAGMENT and any(
        v is not None for v in (
            args.cite_density_min,
            args.refs_min,
            args.primary_share_min,
            args.cited_claims_min,
        )
    ):
        errors = enforce_quality(body, args)
        if errors:
            for line in errors:
                print(line, file=sys.stderr)
            print(
                "Quality gates failed. The article does not meet the "
                "research-quality bar enforced by this build. Fix the "
                "underlying issues (add citations, swap secondary "
                "sources for primary, extend the references list) and "
                "re-check.",
                file=sys.stderr,
            )
            return 1

    # Soft warnings (don't change exit status; nudge the agent toward
    # the design system without blocking commits).
    if args.kind == KIND_FRAGMENT and args.strict_shape:
        for line in soft_warnings(body):
            print(line, file=sys.stderr)

    size = len(body.encode("utf-8"))
    src = "compiled from DSL" if is_dsl else "raw HTML"
    print(
        f"check: OK ({size:,} bytes, kind={args.kind}, {src}). Safe to commit.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
