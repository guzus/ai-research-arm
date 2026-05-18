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


class _RefHostMapCollector(HTMLParser):
    """Walks the HTML and builds {ref_num: host} for every
    `<li id="ref-N">`'s first http(s) URL.

    Used by the corroboration gate: each cite `[^N]` in the body
    rendered to `<sup><a class="ara-cite" href="#ref-N">N</a></sup>`
    must be resolvable to a SOURCE HOST so the gate can count
    distinct hosts per claim.

    Storage choice: only the FIRST http(s) URL inside each ref-li
    is captured. A ref-li with multiple URLs usually has the
    primary source first (publisher / DOI / arxiv) and supplementary
    secondary URLs after. Counting all of them per ref-li would
    artificially inflate host diversity — a single ref entry should
    represent a single source. Single-source-per-entry matches the
    bibliographic convention used in the corpus.

    Hosts are normalized via _normalize_host (lowercase, strip www.).
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._depth_in_ref_li = 0
        self._current_ref_num: int | None = None
        self._current_ref_host: str | None = None  # locked once first URL seen
        self.ref_hosts: dict[int, str] = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "li":
            ref_id = a.get("id", "")
            if ref_id.startswith("ref-"):
                try:
                    n = int(ref_id[4:])
                except ValueError:
                    n = None
                if n is not None:
                    self._depth_in_ref_li = 1
                    self._current_ref_num = n
                    self._current_ref_host = None
                    return
            if self._depth_in_ref_li > 0:
                self._depth_in_ref_li += 1
        if self._depth_in_ref_li > 0 and tag == "a":
            href = a.get("href", "")
            if (
                href.startswith(("http://", "https://"))
                and self._current_ref_host is None
            ):
                m = re.match(r"^https?://([^/]+)", href)
                if m:
                    self._current_ref_host = _normalize_host(m.group(1))

    def handle_endtag(self, tag):
        if tag == "li" and self._depth_in_ref_li > 0:
            self._depth_in_ref_li -= 1
            if self._depth_in_ref_li == 0:
                if self._current_ref_num is not None and self._current_ref_host:
                    self.ref_hosts[self._current_ref_num] = self._current_ref_host
                self._current_ref_num = None
                self._current_ref_host = None


def build_ref_host_map(body_html: str) -> dict[int, str]:
    """Return {ref_num: normalized_host} for every URL-bearing ref-li in
    the article. Ref entries without an http(s) URL (title-only refs)
    are omitted. This map is the lookup table for the corroboration
    gate: each cite marker `[^N]` resolves to a host via this map."""
    c = _RefHostMapCollector()
    c.feed(body_html)
    return c.ref_hosts


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
    """How many DISTINCT http(s) source URLs appear in the references list.

    Two layers of strictness, both responses to codex review feedback:
      1. Only counts URLs inside `<li id="ref-N">` items, not in-body
         hyperlinks.
      2. Counts the number of DISTINCT URLs after normalization (lower-
         case host, trailing-slash-stripped). An article with 20 ref-li
         entries that all point to the same URL counts as 1, not 20 —
         the workflow's "20 distinct source URLs" target wouldn't be met
         by a single URL repeated 20 times.

    A ref-li with no URL (title-only / personal-communication) does not
    contribute. A ref-li with multiple URLs contributes each distinct
    URL it carries.
    """
    collector = _ReferenceHrefCollector()
    collector.feed(body_html)
    return len({_normalize_url(u) for u in collector.ref_urls})


def _normalize_url(url: str) -> str:
    """Normalize a URL for distinct-counting. Lowercase scheme+host,
    strip trailing slash, drop default ports. Path/query are kept as-is
    (so /a vs /b are distinct, but http://X/ and https://X are not)."""
    m = re.match(r"^(https?)://([^/]+)(/.*)?$", url.strip())
    if not m:
        return url.strip().lower()
    scheme, host, path = m.group(1).lower(), m.group(2).lower(), m.group(3) or ""
    if host.startswith("www."):
        host = host[4:]
    # Drop default ports
    if scheme == "http" and host.endswith(":80"):
        host = host[:-3]
    elif scheme == "https" and host.endswith(":443"):
        host = host[:-4]
    path = path.rstrip("/")
    return f"{scheme}://{host}{path}"


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


# ---------------------------------------------------------------------------
# Corroboration gate (--min-corroborating-sources).
# ---------------------------------------------------------------------------
#
# A claim "cited at all" passes the existing cited-claims gate even when
# its only source is wrong (the NBIS failure pattern: adjacent-but-wrong
# numeric cite). The corroboration gate adds a SECOND-INDEPENDENT-SOURCE
# requirement for substantive factual claims. Single-source claims must
# be explicitly acknowledged via `==single-source: ...==` wrapping.
#
# Heuristics here are intentionally conservative:
#   * "Substantive claim" = sentence with cite marker AND (digit OR
#     percent OR dollar OR named-entity proxy). Same shape as
#     cited_claim_share() — reuses the same sensitivity.
#   * "Distinct sources" = distinct normalized hosts of the cited refs.
#     A claim cited 3 times to the same host counts as 1 host.
#   * "Single-source exemption" = the claim sentence is fully contained
#     inside a `<mark class="ara-mark">…</mark>` region whose inner text
#     begins with "single-source:" (case/whitespace tolerant). The agent
#     opts in by wrapping the claim in `==single-source: claim text==`
#     in the DSL.
#
# Sentence boundaries are approximate (regex split on .!?). Cite markers
# at the END of a sentence belong to that sentence. A multi-cite cluster
# `[^1][^2][^3]` at sentence end contributes refs 1, 2, 3 to that
# sentence's host count.

# Regex matches the rendered cite sup wrapper, capturing the ref number
# so we can map back to its host. Multi-cite `[^1,2]` compiles to
# adjacent <sup> elements so this finditer naturally yields each.
_RENDERED_CITE_WITH_NUM_RE = re.compile(
    r'<sup[^>]*>\s*<a[^>]*class="ara-cite"[^>]*href="#ref-([0-9]+)"[^>]*>'
    r'[^<]*</a>\s*</sup>',
    flags=re.IGNORECASE,
)
# Match <mark class="ara-mark">…</mark> regions; we don't depend on the
# class because validate_body already restricts <mark> use to ara-mark.
_MARK_REGION_RE = re.compile(
    r"<mark[^>]*>(.*?)</mark>", flags=re.DOTALL | re.IGNORECASE
)
# Headings often look "substantive" after tag-strip ("Cerebras WSE-3
# Pricing") because they're multi-word capitalized — but they rarely
# carry citations, and when they do, the cite is for the section
# topic, not a factual claim. Skip headings before sentence segmentation
# so they can't contribute false-positive substantive sentences.
_HEADING_STRIP_RE = re.compile(
    r"<h[1-6][^>]*>.*?</h[1-6]>", flags=re.DOTALL | re.IGNORECASE
)


def _extract_mark_inner_texts(body_html: str) -> list[str]:
    """Return the inner text of every `<mark>` region in the body,
    with cite markers and HTML tags stripped and whitespace normalized.

    Used to detect `==single-source: ...==` opt-out wrapping. The mark
    region INCLUDES the prefix `single-source:` followed by the claim
    text — both come from the same DSL `==…==` invocation that compiled
    to one <mark> region.

    Cite markers are stripped (rendered `<sup>…</sup>` -> nothing)
    so the inner text matches the claim sentence extracted from the
    body, which is also cite-stripped in _norm_for_match."""
    out: list[str] = []
    for m in _MARK_REGION_RE.finditer(body_html):
        inner_raw = m.group(1)
        # Strip cite-marker WRAPPERS first (while we still have full
        # HTML) so the digit text inside `<sup><a>N</a></sup>` doesn't
        # survive the tag strip.
        inner_decited = _strip_cite_markers(inner_raw)
        inner = re.sub(r"<[^>]+>", " ", inner_decited)
        inner = re.sub(r"\s+", " ", inner).strip()
        if inner:
            out.append(inner)
    return out


_SINGLE_SOURCE_PREFIX = "single-source:"


def _strip_single_source_prefix(s: str) -> str:
    """Remove a leading `single-source:` (case-insensitive) from a
    normalized text. Returns the original if no prefix present."""
    if s.lower().startswith(_SINGLE_SOURCE_PREFIX):
        return s[len(_SINGLE_SOURCE_PREFIX):].lstrip(" :;,-")
    return s


def _is_single_source_exempt(sentence_text: str, mark_inners: list[str]) -> bool:
    """A sentence is exempt from corroboration when the agent explicitly
    flagged it as single-sourced via `==single-source: ...==`.

    The compiled HTML for that DSL form is
        <mark class="ara-mark">single-source: <sentence body></mark>
    The `single-source:` literal text appears in BOTH the mark inner
    AND the sentence text extracted from the body (because tag-stripping
    leaves the literal prose intact). So we strip the prefix from BOTH
    sides before matching probe -> mark.

    Match policy: case-insensitive prefix on "single-source:", and the
    sentence's first ~60 substantive chars (after prefix strip) must
    appear inside the mark region's content (after prefix strip).
    Lenient enough to survive whitespace / cite-marker drift between
    probe and rendered mark."""
    if not mark_inners:
        return False
    probe = _norm_for_match(sentence_text)
    probe = _strip_single_source_prefix(probe)
    if not probe:
        return False
    probe_head = probe[:60]
    for inner in mark_inners:
        inner_l = inner.lower().strip()
        if not inner_l.startswith(_SINGLE_SOURCE_PREFIX):
            continue
        # Strip the prefix and any leading punctuation from the mark
        # body, then normalize for matching.
        body_after_prefix = inner_l[len(_SINGLE_SOURCE_PREFIX):].lstrip(" :;,-")
        body_after_prefix = _norm_for_match(body_after_prefix)
        if probe_head and probe_head in body_after_prefix:
            return True
    return False


def _norm_for_match(s: str) -> str:
    """Normalize text for case/whitespace-tolerant probe matching.
    Also strips citation markers (DSL `[^N]` and rendered `<sup>…</sup>`
    forms) so a probe extracted from one form matches text from the
    other. Returns lowercase, whitespace-collapsed, no cite-markers."""
    s = _strip_cite_markers(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def _claim_sentences_with_refs(
    body_html: str,
) -> list[tuple[str, list[int]]]:
    """Walk the article body, return [(sentence_text, [ref_nums...]), ...]
    for every substantive sentence that carries at least one cite marker.

    Algorithm:
      1. Strip <h1..h6> regions — headings rarely carry meaningful
         claims and their multi-word capitalized form would inflate
         the substantive-sentence rate.
      2. Replace each rendered cite sup with a sentinel that carries
         the ref number so sentence segmentation preserves the
         ref-to-sentence association.
      3. Strip remaining HTML tags. Split on .!? boundaries.
      4. For each sentence with a sentinel, check if it's substantive
         (digit/percent/dollar/multi-word capitalized). Yield (text,
         [ref nums extracted from sentinels]).
    """
    body = _HEADING_STRIP_RE.sub(" ", body_html)
    # Sentinel: \x00C<num>\x00 — distinct from existing _CITE_MARKER
    # and survives tag-strip + sentence-split intact.
    def _cite_sub(m: re.Match) -> str:
        return f" \x00C{m.group(1)}\x00 "
    marked = _RENDERED_CITE_WITH_NUM_RE.sub(_cite_sub, body)
    text = re.sub(r"<[^>]+>", " ", marked)
    sentinel_re = re.compile(r"\x00C([0-9]+)\x00")
    sents = _SENT_SPLIT.split(text)
    out: list[tuple[str, list[int]]] = []
    for s in sents:
        if not s.strip():
            continue
        nums = [int(n) for n in sentinel_re.findall(s)]
        if not nums:
            continue
        # Strip sentinels before substantive-check so the cite digits
        # don't make every cited sentence look "substantive."
        clean = sentinel_re.sub(" ", s)
        is_subs = (
            any(c.isdigit() for c in clean)
            or "%" in clean
            or "$" in clean
            or bool(_SUBSTANTIVE_NE.search(clean))
        )
        if is_subs:
            out.append((clean.strip(), nums))
    return out


def corroboration_audit(
    body_html: str, min_hosts: int
) -> tuple[list[dict], int]:
    """Return (failing_claims, total_claims).

    Each failing_claims entry: {"text": str, "ref_nums": [int],
                                "hosts": [str], "distinct_hosts": int}
    Total_claims = number of substantive cited sentences considered
    (NOT count of failures). Useful for the "X of Y claims pass" report."""
    if min_hosts < 1:
        raise ValueError(f"min_hosts must be >= 1, got {min_hosts}")
    ref_hosts = build_ref_host_map(body_html)
    mark_inners = _extract_mark_inner_texts(body_html)
    claims = _claim_sentences_with_refs(body_html)
    failing: list[dict] = []
    for text, nums in claims:
        hosts: list[str] = []
        for n in nums:
            h = ref_hosts.get(n)
            if h:
                hosts.append(h)
        distinct = sorted(set(hosts))
        if len(distinct) >= min_hosts:
            continue
        # Below threshold — check single-source exemption.
        if _is_single_source_exempt(text, mark_inners):
            continue
        failing.append({
            "text": text,
            "ref_nums": nums,
            "hosts": distinct,
            "distinct_hosts": len(distinct),
        })
    return failing, len(claims)


# ---------------------------------------------------------------------------
# Quantitative sanity (--qsanity) — heuristic numeric implausibility scan.
# ---------------------------------------------------------------------------
#
# v1 is intentionally NARROW and WARN-ONLY. Each pattern targets a
# common implausibility shape that's caused real article rework:
#   1. :::donut percentages summing > 105% (compiled to ara-donut-*)
#   2. Single-entity market share > 100%
#   3. YoY growth claims > 1000%
#   4. Future dates more than 10 years out (warn — forecasts are legitimate
#      but typo'd years are common; warning encourages a sanity look)
#
# Patterns NOT shipped in v1 (high false-positive risk per spec):
#   - Revenue-per-employee ratio (requires proximity pairing; FP risk on
#     early-stage SaaS with intentionally lean teams)
#   - P/S valuation/revenue ratio (same problem)
#   - Compute-claim plausibility tables (needs per-accelerator domain
#     encoding the spec admits is hard)
#
# All hits are stderr warnings — exit status unchanged. Once we have
# precision data from a few hundred runs, individual patterns may be
# promoted to hard-fail. Documented as such in CLI help.

_QSANITY_FUTURE_YEAR_HORIZON = 10  # years past current — beyond this is flagged
_QSANITY_DONUT_SUM_LIMIT = 105.0   # percent; rounding tolerance
_QSANITY_MARKET_SHARE_LIMIT = 100.0
_QSANITY_YOY_LIMIT = 1000.0


def _qsanity_donut_sums(body_html: str) -> list[str]:
    """For each `<div class="ara-donut">` block (or legacy `<ul>` form),
    sum the slice values and flag if the sum exceeds 105% (rounding
    tolerance).

    Compiler emits donuts as `<div class="ara-donut" data-labels="A,B,C"
    data-values="80,50,45"></div>` — see emit_donut() in compile_ara.py.
    Earlier draft of this helper matched `<ul>` with `<li data-pct>`,
    which never fires in production (caught by codex review). Both
    shapes are supported here so hand-authored `:::raw` donut markup
    (if anyone ever writes it) is also scanned.

    A sum of 175 is the textbook implausibility — either the agent
    listed overlapping categories or hallucinated values that don't
    share a denominator.

    Known false-positive class: donuts used for COMPARATIVE MAGNITUDE
    rather than percentage share. Example surfaced by corpus scan:
    home-inference-rack article uses a donut to compare $/M-tokens
    pricing across models ($180, $30, $25, $18) — the sum (253) has
    no meaning. v1 ships warn-only specifically so authors can ignore
    these legitimate non-share donuts. If a future iteration wants to
    hard-fail on donut sum, also require `data-pct` semantics in the
    DSL (e.g., introduce a `:::pct-donut` directive) so the gate has
    explicit consent to treat slices as shares."""
    warns: list[str] = []
    donut_index = 0

    # Primary shape: <div class="ara-donut" data-values="80,50,45"></div>
    # Self-closing divs would be unusual but the compiler emits them with
    # an explicit closing tag, so this regex matches either form.
    for m in re.finditer(
        r'<div[^>]*class="ara-donut[^"]*"([^>]*)>(?:.*?</div>)?',
        body_html, flags=re.DOTALL | re.IGNORECASE,
    ):
        donut_index += 1
        attrs = m.group(1)
        values_match = re.search(
            r'data-values="([0-9.,\s-]+)"', attrs
        )
        if not values_match:
            continue
        raw_values = values_match.group(1)
        nums: list[float] = []
        for part in raw_values.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                nums.append(float(part))
            except ValueError:
                # Non-numeric token — skip the donut rather than warn
                # on parse error. validate_body would have already
                # rejected an article with truly malformed data-values.
                nums = []
                break
        if not nums:
            continue
        total = sum(nums)
        if total > _QSANITY_DONUT_SUM_LIMIT:
            warns.append(
                f"qsanity: :::donut #{donut_index} values sum to {total:.1f}% "
                f"({len(nums)} slices) — exceeds {_QSANITY_DONUT_SUM_LIMIT:.0f}% "
                f"tolerance. Donuts represent slices of one whole; "
                f"if the categories overlap, use :::bars or :::rank-list "
                f"instead. Recheck the values for hallucinated digits."
            )

    # Legacy / hand-authored shape: <ul class="ara-donut">
    # <li data-pct="N">label</li>... </ul>. Kept for compatibility
    # with any article authored via :::raw that hand-rolls a donut.
    for block in re.findall(
        r'<ul[^>]*class="ara-donut[^"]*"[^>]*>(.*?)</ul>',
        body_html, flags=re.DOTALL | re.IGNORECASE,
    ):
        pcts = re.findall(r'data-pct="([0-9]+(?:\.[0-9]+)?)"', block)
        if not pcts:
            continue
        donut_index += 1
        total = sum(float(p) for p in pcts)
        if total > _QSANITY_DONUT_SUM_LIMIT:
            warns.append(
                f"qsanity: :::donut #{donut_index} percentages sum to {total:.1f}% "
                f"({len(pcts)} slices) — exceeds {_QSANITY_DONUT_SUM_LIMIT:.0f}% "
                f"tolerance. Donuts represent slices of one whole; "
                f"if the categories overlap, use :::bars or :::rank-list "
                f"instead. Recheck the values for hallucinated digits."
            )
    return warns


def _qsanity_text_only(body_html: str) -> str:
    """Return body text with HTML stripped. Helper for prose-pattern
    scans that don't depend on HTML structure."""
    # Strip cite markers first so "[citing 12.5%]" type artifacts don't
    # confuse the number extractors.
    s = re.sub(r"<[^>]+>", " ", body_html)
    return re.sub(r"\s+", " ", s)


def _qsanity_market_share_over_100(body_html: str) -> list[str]:
    """Flag any prose mention of "N% market share" / "N% of the market"
    where N > 100. Single-entity market share > 100% is impossible; a
    hit is almost certainly a digit-transposition (75% → 175%) or a
    units error (basis points / total addressable confusion)."""
    warns: list[str] = []
    text = _qsanity_text_only(body_html)
    # Capture the immediate context (up to 80 chars) for the warning.
    pattern = re.compile(
        r'\b(\d{2,3}(?:\.\d+)?)\s*%\s*(?:market\s+share|of\s+the\s+market)',
        flags=re.IGNORECASE,
    )
    for m in pattern.finditer(text):
        val = float(m.group(1))
        if val > _QSANITY_MARKET_SHARE_LIMIT:
            # Snip a small window around the match for context
            start = max(0, m.start() - 30)
            end = min(len(text), m.end() + 30)
            context = text[start:end].strip()
            warns.append(
                f"qsanity: market share {val:.1f}% > "
                f"{_QSANITY_MARKET_SHARE_LIMIT:.0f}% (impossible) "
                f"near: …{context}…"
            )
    return warns


def _qsanity_yoy_growth(body_html: str) -> list[str]:
    """Flag YoY growth claims > _QSANITY_YOY_LIMIT (default 1000%).
    Hit shape: `\\d+%\\s+(YoY|year-over-year|year over year)`.

    Genuine 1000%+ YoY growth exists (low base effects in startups)
    but is rare enough to deserve a sanity check. Pattern is permissive
    on YoY phrasing variants but conservative on the number itself
    (only 4+ digit percentages flagged)."""
    warns: list[str] = []
    text = _qsanity_text_only(body_html)
    pattern = re.compile(
        r'\b(\d{4,}(?:\.\d+)?)\s*%\s*(?:YoY|year[-\s]over[-\s]year)',
        flags=re.IGNORECASE,
    )
    for m in pattern.finditer(text):
        val = float(m.group(1))
        if val > _QSANITY_YOY_LIMIT:
            start = max(0, m.start() - 30)
            end = min(len(text), m.end() + 30)
            context = text[start:end].strip()
            warns.append(
                f"qsanity: YoY growth {val:.0f}% > "
                f"{_QSANITY_YOY_LIMIT:.0f}% (extreme — verify it's not a "
                f"digit-shift error) near: …{context}…"
            )
    return warns


def _qsanity_future_dates(body_html: str, current_year: int) -> list[str]:
    """Flag any 4-digit year > current_year + horizon. Forecasts and
    long-horizon timelines are legitimate; the warning's job is to
    surface them for sanity check, not to block. Excludes years
    inside well-known patent / patent-app number contexts (rare)."""
    warns: list[str] = []
    text = _qsanity_text_only(body_html)
    # Find 4-digit numbers in 19XX-21XX range — covers all plausible
    # year mentions without flagging stray 4-digit identifiers.
    pattern = re.compile(r'\b(19\d{2}|20\d{2}|21\d{2})\b')
    horizon = current_year + _QSANITY_FUTURE_YEAR_HORIZON
    flagged_years: set[int] = set()
    for m in pattern.finditer(text):
        y = int(m.group(1))
        if y > horizon and y not in flagged_years:
            flagged_years.add(y)
            warns.append(
                f"qsanity: year {y} appears in body — more than "
                f"{_QSANITY_FUTURE_YEAR_HORIZON} years past current "
                f"({current_year}). Forecast / timeline context is "
                f"fine; verify it's not a typo."
            )
    return warns


def qsanity_scan(body_html: str, current_year: int) -> list[str]:
    """Run all qsanity patterns. Returns the combined warning list.

    Each pattern is independent — adding a new one means writing
    another `_qsanity_*` function and appending its return value."""
    warns: list[str] = []
    warns.extend(_qsanity_donut_sums(body_html))
    warns.extend(_qsanity_market_share_over_100(body_html))
    warns.extend(_qsanity_yoy_growth(body_html))
    warns.extend(_qsanity_future_dates(body_html, current_year))
    return warns


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

    if getattr(args, "min_corroborating_sources", None) is not None:
        n = args.min_corroborating_sources
        failing, total = corroboration_audit(body_html, n)
        if failing:
            lines = [
                f"quality: {len(failing)} of {total} substantive cited "
                f"claim(s) lack {n} distinct source host(s). Each claim "
                f"below needs an additional source from a different "
                f"publisher, or wrap the sentence in "
                f"`==single-source: claim text==` to acknowledge the "
                f"single-source citation (which compiles to <mark>):",
            ]
            for f in failing[:8]:
                preview = f["text"][:120]
                if len(f["text"]) > 120:
                    preview += "…"
                hosts_str = ", ".join(f["hosts"]) if f["hosts"] else "(no resolvable host)"
                lines.append(
                    f"  - cites=[{','.join(str(r) for r in f['ref_nums'])}] "
                    f"hosts={hosts_str} "
                    f"distinct_hosts={f['distinct_hosts']}: {preview!r}"
                )
            if len(failing) > 8:
                lines.append(f"  ... and {len(failing) - 8} more failing claim(s)")
            errors.append("\n".join(lines))

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
        # Count distinct occurrences instead of using `probe in mark`:
        # if the claim appears N times in the body and only K < N are
        # wrapped in <mark>, the prior `probe not in mark_norm` test
        # would falsely treat the claim as demoted because the probe
        # exists somewhere in the mark blob. Strict version: an
        # unmarked occurrence survives if total body occurrences
        # exceeds the mark-region occurrences.
        body_occurrences = body_norm.count(probe)
        mark_occurrences = mark_norm.count(probe)
        if body_occurrences > mark_occurrences:
            surviving.append(
                {
                    "id": claim.get("id"),
                    "probe": probe,
                    "citation": claim.get("citation"),
                    "body_occurrences": body_occurrences,
                    "mark_occurrences": mark_occurrences,
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
    p.add_argument(
        "--min-corroborating-sources",
        type=int,
        default=None,
        metavar="INT",
        help=(
            "fail if any substantive cited claim is supported by fewer "
            "than INT DISTINCT source HOSTS. A claim sentence is "
            "'substantive' if it carries a cite marker AND contains "
            "a digit / percent / dollar / multi-word capitalized phrase. "
            "Hosts are extracted from the first URL in each `<li id=\"ref-N\">` "
            "entry. To explicitly acknowledge a single-source claim, "
            "wrap the sentence as `==single-source: claim text==` in the "
            "DSL (compiles to <mark class=\"ara-mark\">), and the gate "
            "exempts it. Default off (opt-in); recommended workflow "
            "value once calibrated: 2. Heuristic — see "
            "corroboration_audit() docstring for caveats."
        ),
    )
    p.add_argument(
        "--qsanity",
        action="store_true",
        help=(
            "scan the article for implausible numeric patterns and "
            "print warnings to stderr. WARN-ONLY (does not fail the "
            "build) in v1 — heuristics are conservative but can have "
            "false positives. Patterns checked: :::donut percentage "
            "sums above 105, single-entity market share above 100, "
            "YoY growth above 1000, dates more than 10 years past "
            "current. Documented patterns may be promoted to hard-fail "
            "in future revisions once precision is established."
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
            args.min_corroborating_sources,
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

    # Quantitative-sanity scan (--qsanity). Warn-only in v1: each
    # heuristic prints to stderr but exit status is unchanged. See
    # qsanity_scan() and the _qsanity_* helpers for the pattern set
    # and the rationale for each. Promotion to hard-fail is deferred
    # until per-pattern precision is established by running the scan
    # against the historical corpus and inspecting false positives.
    if args.kind == KIND_FRAGMENT and args.qsanity:
        from datetime import datetime, timezone
        cy = datetime.now(timezone.utc).year
        qwarns = qsanity_scan(body, cy)
        for line in qwarns:
            print(line, file=sys.stderr)
        if qwarns:
            print(
                f"qsanity: {len(qwarns)} warning(s) — review each; not "
                "blocking the build.",
                file=sys.stderr,
            )

    size = len(body.encode("utf-8"))
    src = "compiled from DSL" if is_dsl else "raw HTML"
    print(
        f"check: OK ({size:,} bytes, kind={args.kind}, {src}). Safe to commit.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
