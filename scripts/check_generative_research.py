#!/usr/bin/env python3
"""Compile-check a generative research article body without committing.

Runs the same validation rules write_generative_research.py enforces at
commit time — tag allowlist, ara-* exact-match class allowlist loaded
from ARA_CATALOG.json (modifier suffixes allowed), size cap, no inline
style/script/JS handlers, opening/closing <article> structure. The
allowlist comes from ARA_CATALOG.json via write_generative_research's
load_valid_classes(); COMPONENTS.md is the human reference kept in
lockstep with the catalog (CI-enforced via ara_catalog.py).

Optional design-system enforcement flags (off by default so check
stays additive):
  --diversity-min N   fail if fewer than N distinct visualization
                      primitives are used. Counts ara-line-chart,
                      ara-bar-chart, ara-donut, ara-slope,
                      ara-stack-bar, ara-stack-rows, ara-bars,
                      ara-rank-list, ara-compare, ara-iso,
                      ara-sparkline, ara-timeline, ara-kv. ara-table
                      and ara-callout
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

Text inside a `class="ara-position"` block is EXEMPT from all three
uncited-claim heuristics above (cite density, cited-claim share,
corroboration). A `:::position` block is labelled analyst judgment —
"Analyst position — not a sourced claim" — so counting it as an
uncited factual claim would penalise the article for using the
component correctly. It is NOT exempt from --audit-verifier-findings:
moving a claim the verifier rejected into a position block is not a
demotion, `<mark>` is.

Audit modes (each takes a path to a sidecar artifact):
  --audit-verifier-findings PATH  fail if an `unsupported` claim
                            survived in the body without being demoted
                            (<mark>) or removed.
  --audit-derived-claims PATH  recompute-verify the `type: "derived"`
                            entries in a claims ledger. A derived claim
                            (e.g. "30 GW at $60B/GW is ~$1.8T") has no
                            source URL by construction, so retrieval
                            cannot verify it; instead its inputs must
                            resolve to other claims in the same ledger
                            and its formula must reproduce its stated
                            result. Formulas are parsed under a
                            whitelisted AST — never eval()'d. See
                            audit_derived_claims() for rules R1-R7.

Exit status:
  0  — body is valid; safe to commit
  1  — body fails validation; the error is printed to stderr with
        specific fixes (e.g. "undocumented class ara-references → did
        you mean: ara-eyebrow")
  2  — argv error / file missing

Usage:
  uv run python scripts/check_generative_research.py /tmp/gen-research-body.html
  uv run python scripts/check_generative_research.py - < body.html     # stdin
  uv run python scripts/check_generative_research.py path --kind standalone
  uv run python scripts/check_generative_research.py path --diversity-min 3 --callout-max 5
  uv run python scripts/check_generative_research.py path --cite-density-min 10 --refs-min 20

The agent loop in the workflow / local skill: write the body, run this
check, fix anything it reports, re-check, and only then call the real
writer to commit. Deterministic — no agent self-validation needed.
"""

from __future__ import annotations

import argparse
import ast
import math
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
from generative_methodology import (  # noqa: E402
    validate_claim_ledger,
    validate_redteam_artifact,
    validate_verifier_artifact,
)

# Component classification, keep in lockstep with ARA_DSL.md / COMPONENTS.md.
VIZ_PRIMITIVES = frozenset([
    "ara-line-chart", "ara-bar-chart", "ara-donut", "ara-slope",
    "ara-stack-bar", "ara-stack-rows",
    "ara-bars", "ara-rank-list", "ara-compare",
    "ara-iso", "ara-sparkline", "ara-timeline", "ara-kv",
])
DISTRIBUTION_VIZ = frozenset([
    "ara-donut", "ara-bar-chart", "ara-stack-bar", "ara-stack-rows",
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


# ---------------------------------------------------------------------------
# :::position exemption — labelled analyst judgment is not a sourced claim.
# ---------------------------------------------------------------------------
#
# A `:::position` block compiles to an element carrying class
# `ara-position` (plus a confidence variant `ara-position--high|medium|low`)
# and renders a visible "Analyst position — not a sourced claim" label.
# Its whole purpose is to ship an explicit non-consensus call that is
# NOT presented as verified fact. The uncited-claim heuristics
# (cited_claim_share, corroboration_audit, cite-density accounting)
# therefore must not see it: a stance sentence like "Hyperscaler credit
# spreads compress rather than widen through Q4 2026" is substantive by
# every heuristic in this file and carries no cite by design, so leaving
# it in the denominator would penalise the article for using the
# component correctly.
#
# NOT exempt, deliberately:
#   * audit_verifier_findings() — moving an `unsupported` verifier claim
#     into a position block must NOT count as demotion. `<mark>` is the
#     demotion channel; a position block is an original call, not a
#     laundering slot for a claim that failed verification.
#   * soft_warnings()/qsanity — advisory only, never fail a build.
#   * primary_share()/count_references() — reference-list metrics; a
#     position block contains no `<li id="ref-N">` entries.

_POSITION_CLASS = "ara-position"

# Hard bound on how much text one position block may remove from the
# citation denominators.
#
# WHY THIS EXISTS: the exemption removes an author-controlled region from
# cite_density()'s denominator. Unbounded, it is a bypass of the live
# production gate `--cite-density-min 10`: relocate 1,200 words of
# uncited prose into a `:::position` block and a 7.94 density (FAIL)
# becomes 166.67 (PASS), using only the sanctioned DSL directive and
# allowlisted classes. Measured before this cap was added.
#
# The cap is fail-CLOSED: an oversized block is not exempted AT ALL, so
# every word of it stays in the denominator and the bypass yields
# nothing. Partial stripping was rejected — it would leave a half-block
# in the text and make the denominator depend on where the cut landed.
#
# The number is derived, not guessed: it is the largest block
# emit_position() in compile_ara.py can produce given that module's
# per-field word bound, plus headroom. scripts/test_ara_dsl.py asserts
# that inequality empirically (compile bound <= this cap), so the two
# modules cannot drift into a state where the compiler emits a block the
# validator refuses to exempt — which would show up as a mysterious
# density failure rather than a clear compile error.
_POSITION_MAX_EXEMPT_WORDS = 260


def _has_position_class(attrs: list[tuple[str, str | None]]) -> bool:
    """True when a start tag's class attribute carries the `ara-position`
    class as a WHOLE TOKEN (or its `ara-position--<variant>` modifier).

    Token matching matters: the inner elements of the block are
    `ara-position-label`, `ara-position-stance`, `ara-position-row`,
    `ara-position-key`, `ara-position-val`, `ara-position-meta`. A
    substring test would treat each of those as a block root and a naive
    `.*?` regex would then close the region at the first `</div>`."""
    for key, val in attrs:
        if key.lower() != "class" or not val:
            continue
        for tok in val.split():
            if tok == _POSITION_CLASS or tok.startswith(_POSITION_CLASS + "--"):
                return True
    return False


class _PositionBlockStripper(HTMLParser):
    """Records the character spans occupied by every top-level
    `ara-position` block, matching the block root's OWN tag name with a
    depth counter so nested markup (rows, spans, nested divs) cannot
    terminate the region early.

    `spans` is a list of (start, end) offsets into the source string;
    `open_depth` is non-zero at EOF when a block was never closed, which
    the caller treats as "give up and strip nothing" (fail open)."""

    def __init__(self, html: str):
        super().__init__(convert_charrefs=False)
        self._html = html
        # Precompute line-start offsets so getpos() (1-based line,
        # 0-based column) can be converted to an absolute index.
        self._line_starts = [0]
        for i, ch in enumerate(html):
            if ch == "\n":
                self._line_starts.append(i + 1)
        self._root_tag: str | None = None
        self.open_depth = 0
        self._span_start: int | None = None
        self.spans: list[tuple[int, int]] = []

    def _offset(self) -> int:
        line, col = self.getpos()
        if line - 1 >= len(self._line_starts):
            return len(self._html)
        return min(self._line_starts[line - 1] + col, len(self._html))

    def handle_starttag(self, tag, attrs):
        if self.open_depth == 0:
            if _has_position_class(attrs):
                self._root_tag = tag
                self.open_depth = 1
                self._span_start = self._offset()
        elif tag == self._root_tag:
            # Same-named element nested inside the block (e.g. a <div>
            # row inside a <div class="ara-position">). Its close tag
            # must not be mistaken for the block's.
            self.open_depth += 1

    def handle_startendtag(self, tag, attrs):
        # `<div class="ara-position"/>` — opens and closes at once, so it
        # never changes depth. Inside an already-open block it is just
        # content and needs no span of its own.
        if self.open_depth == 0 and _has_position_class(attrs):
            start = self._offset()
            raw = self.get_starttag_text() or ""
            self.spans.append((start, start + len(raw)))

    def handle_endtag(self, tag):
        if self.open_depth > 0 and tag == self._root_tag:
            self.open_depth -= 1
            if self.open_depth == 0:
                end = self._offset()
                gt = self._html.find(">", end)
                end = len(self._html) if gt == -1 else gt + 1
                if self._span_start is not None:
                    self.spans.append((self._span_start, end))
                self._span_start = None
                self._root_tag = None


def strip_position_blocks(body_html: str) -> str:
    """Return `body_html` with every `class="ara-position"` block removed
    (replaced by a single space so surrounding prose does not concatenate).

    Fail-open by construction — every abnormal shape returns the input
    UNCHANGED rather than deleting to end-of-document:
      * no `ara-position` substring at all -> identity, no parsing. This
        makes "no behaviour change on the existing corpus" checkable
        rather than merely argued.
      * a block whose root tag never closes (`open_depth > 0` at EOF, or
        a void root like `<br class="ara-position">`) -> identity. The
        alternative — stripping to EOF — would delete every downstream
        `ara-cite` marker and hard-fail a build that should have passed.
      * any parser exception -> identity.

    Limitation: the end-tag span ends at the first `>` at or after the
    end tag's start offset. HTML end tags carry no attributes, so that is
    exact for the compiled output this validator sees.

    Bounded: a block whose visible text exceeds
    `_POSITION_MAX_EXEMPT_WORDS` is left in place (see that constant).
    An analyst position is a short labelled call, not a container an
    author can pour arbitrary uncited prose into to shrink the
    cite-density denominator."""
    if _POSITION_CLASS not in body_html:
        return body_html
    parser = _PositionBlockStripper(body_html)
    try:
        parser.feed(body_html)
        parser.close()
    except Exception:  # noqa: BLE001 — boundary: never let a parse blow up a gate
        return body_html
    if parser.open_depth > 0 or not parser.spans:
        return body_html
    out: list[str] = []
    prev = 0
    for start, end in parser.spans:
        if start < prev or end < start:  # overlapping/degenerate — bail out
            return body_html
        if _word_count(body_html[start:end]) > _POSITION_MAX_EXEMPT_WORDS:
            # Oversized: exempt nothing. Leaving the span untouched keeps
            # every one of its words in the denominator, which is what
            # makes the relocation bypass worthless.
            continue
        out.append(body_html[prev:start])
        out.append(" ")
        prev = end
    out.append(body_html[prev:])
    return "".join(out)


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

    `ara-position` blocks are removed before segmentation — a labelled
    analyst position is explicitly not a sourced claim, so it belongs in
    neither the numerator nor the denominator (see strip_position_blocks).

    Returns (share, cited_substantive, total_substantive). Share is 0.0
    when no substantive sentences exist (empty/HTML-only body).
    """
    body_html = strip_position_blocks(body_html)
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
    """Citations per 1000 words. Returns (density, cites, words).

    `ara-position` blocks are excluded from BOTH terms: their words do
    not dilute the denominator and any cite inside them does not pad the
    numerator. Without the exclusion, an ~80-word analyst position would
    shave roughly 3% off the density of a 3,000-word article purely for
    using the component the contract provides. `count_cite_markers()` and
    `_word_count()` stay position-blind so callers that want raw totals
    (e.g. a reporting step) still get them."""
    scoped = strip_position_blocks(body_html)
    cites = count_cite_markers(scoped)
    words = _word_count(scoped)
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
    (NOT count of failures). Useful for the "X of Y claims pass" report.

    Claim extraction skips `ara-position` blocks (labelled analyst
    judgment is not a sourced claim). The ref-host map and the <mark>
    exemption index are still built from the FULL body: a position block
    contains no `<li id="ref-N">` entries, and building those from the
    stripped body would only create a way for odd nesting to erase hosts
    and manufacture failures."""
    if min_hosts < 1:
        raise ValueError(f"min_hosts must be >= 1, got {min_hosts}")
    ref_hosts = build_ref_host_map(body_html)
    mark_inners = _extract_mark_inner_texts(body_html)
    claims = _claim_sentences_with_refs(strip_position_blocks(body_html))
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


# Typographic folding for the verifier-findings audit: the verifier
# ledger and the rendered article routinely disagree on quote glyphs,
# ellipsis style, and dashes. Fold both sides to a common shape before
# substring probing (see audit_verifier_findings).
_TYPOGRAPHY_FOLD_TRANS = str.maketrans({
    "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
    "\u2032": "'",
    "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
    "\u2033": '"',
    "\u2026": "...",
    "\u2012": "-", "\u2013": "-", "\u2014": "-", "\u2015": "-",
    "\u00a0": " ",
})


def _fold_typography(s: str) -> str:
    """Fold curly quotes, Unicode ellipsis, dashes, and NBSP to ASCII
    equivalents so ledger text and body text compare on equal
    footing."""
    return s.translate(_TYPOGRAPHY_FOLD_TRANS)


_AUDIT_SEGMENT_MIN_WORDS = 5
_AUDIT_SHINGLE_WORDS = 8


def _claim_probes(norm_text: str) -> list[str]:
    """Build the substring probe set for one verifier claim.

    Input is the claim text already cite-stripped and normalized
    (typography-folded, quote-blind, lowercased, whitespace-collapsed
    -- see _norm inside audit_verifier_findings). Probes:

      * the first ~80 chars (legacy prefix probe -- cheap, exact);
      * each segment of >= 5 words after splitting on ellipses,
        colons, and semicolons (the verifier elides quotes with `...`
        and prefixes attribution with `X said:` / `X poses:`, so
        segments are the verbatim runs);
      * every 8-word shingle inside a segment, so verbatim survival is
        caught even when the ledger adds framing that shifts every
        longer probe.

    Windows never cross a split boundary: an elision or attribution
    colon is exactly where body text legitimately diverges from
    ledger text.
    """
    probes: list[str] = []
    if norm_text:
        probes.append(norm_text[:80])
    for raw_segment in re.split(r"\.\.\.|[:;]", norm_text):
        segment = raw_segment.strip(" \'\"")
        words = segment.split()
        if len(words) >= _AUDIT_SEGMENT_MIN_WORDS:
            probes.append(segment)
        if len(words) >= _AUDIT_SHINGLE_WORDS:
            for i in range(len(words) - _AUDIT_SHINGLE_WORDS + 1):
                probes.append(" ".join(words[i : i + _AUDIT_SHINGLE_WORDS]))
    return list(dict.fromkeys(p for p in probes if p))


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
    text and the body; decode HTML entities (html.unescape, applied
    after tag-stripping); fold typographic variants (curly quotes,
    Unicode ellipsis, dashes — see _fold_typography); drop quote
    characters; normalize whitespace/case. The verifier reads DSL and
    adds its own framing (attribution prefixes, `...` elisions); the
    compiled HTML we audit uses the rendered form. Each claim then
    yields a probe SET (see _claim_probes): the ~80-char prefix, every
    ellipsis/colon/semicolon-separated segment of >= 5 words, and
    every 8-word shingle. If ANY probe occurs in the body text more
    times than
    inside `<mark>…</mark>` regions, the claim survived without being
    demoted → fail.

    Limitations (call out in PR + reviewer-facing docs):
      * Whole-claim-demotion semantics: if the agent demotes only the
        load-bearing number inside a longer claim sentence, the probe
        may match in body-text but NOT inside the mark region → false
        fail. Acceptable — pushes the agent toward marking the whole
        sentence.
      * Paraphrase-on-revision: if the agent rewrites the claim text
        on revision, no probe will match anywhere → treated as
        "removed" → pass. Acceptable — paraphrase to a supported
        variant is a valid bounded-revision outcome.
      * Shingle floor: short verbatim runs (< 5 words, or 5-7 words
        not isolated by an ellipsis/colon/semicolon boundary) can
        still ghost through. Acceptable — below that, substring
        matching cannot tell survival from coincidence.

    Returns (unsupported_total, surviving) where `surviving` is a list
    of dicts {id, probe, citation} for every unsupported claim that
    failed the audit. Empty `surviving` = pass.

    Raises ValueError if the findings JSON is malformed.
    """
    import html as _html
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
    if not claims:
        raise ValueError(
            "verifier findings JSON claims[] is empty; verifier did not "
            "record any claim-level checks"
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
        # Quote-blind on top of typographic folding: the ledger may
        # single-quote what the body double-quotes. Apostrophes are
        # removed (no space) so "CFR\u2019s" == "CFR's" == "cfrs";
        # double quotes become spaces so adjacent words never fuse.
        # Entities first: ~10% of committed articles carry
        # typographic entities (&mdash;, &rsquo;, &hellip;) in visible
        # body text; unescaping after tag-stripping keeps &lt;/&gt;
        # harmless while putting entity-encoded bodies on the same
        # footing as literal-Unicode ones.
        s = _fold_typography(_html.unescape(s)).replace('"', " ").replace("'", "")
        return re.sub(r"\s+", " ", s).strip().lower()

    body_norm = _norm(text_no_tags)
    mark_norm = _norm(mark_blob)

    surviving: list[dict] = []
    unsupported_total = 0
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        verdict = str(claim.get("verdict", "")).lower()
        if verdict not in {"supported", "weak", "unsupported"}:
            raise ValueError(
                f"verifier findings JSON claim {claim.get('id')!r} has "
                f"invalid verdict {verdict!r}"
            )
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
        #
        # Probe SET, not a single prefix. The old logic probed only
        # `_norm(text)[:80]`; any framing the verifier added around a
        # quote (attribution prefix, `?...` elision, curly quotes)
        # shifted the prefix and the claim ghosted through as
        # "removed" — a real unsupported quote shipped exactly that
        # way on 2026-07-04 (anthropic-vs-the-pentagon, claim c23).
        # Verbatim survival of any ellipsis segment or 8-word shingle
        # now fails; genuine paraphrase (no 8-word run in common)
        # still passes, preserving the paraphrase-on-revision escape
        # documented above.
        norm_text = _norm(_strip_cite_markers(text))
        hit = None
        for probe in _claim_probes(norm_text):
            # Count distinct occurrences instead of using `probe in
            # mark`: if the claim appears N times in the body and only
            # K < N are wrapped in <mark>, a membership test would
            # falsely treat the claim as demoted because the probe
            # exists somewhere in the mark blob. Strict version: an
            # unmarked occurrence survives if total body occurrences
            # exceed the mark-region occurrences.
            body_occurrences = body_norm.count(probe)
            mark_occurrences = mark_norm.count(probe)
            if body_occurrences > mark_occurrences:
                hit = (probe, body_occurrences, mark_occurrences)
                break
        if hit is None:
            continue
        probe, body_occurrences, mark_occurrences = hit
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


# ---------------------------------------------------------------------------
# Derived-claim recompute audit (--audit-derived-claims).
# ---------------------------------------------------------------------------
#
# The rest of this file verifies claims by RETRIEVAL: does some cited URL
# assert this sentence? That structurally forbids arithmetic the analyst
# performs from cited inputs — "30 GW at $60B/GW is ~$1.8T of capex" has
# no source URL, so the verifier marks it unsupported and the workflow's
# verifier-findings audit fails the build.
#
# A derived claim is verified by RECOMPUTATION instead: it is supported
# iff its inputs are supported and the arithmetic checks out. That is
# stronger provenance than a citation, not weaker — the reader can redo
# the sum.
#
# Ledger entry shape (lives in the same .gen-claims-ledger.json as the
# retrieval claims; non-derived entries keep their existing shape):
#
#   {"id": "d1", "type": "derived",
#    "claim": "At 30 GW of CY28 additions and $60B per GW, capex is ~$1.8T.",
#    "inputs": [{"ref": "c3", "name": "gigawatts",   "value": 30,   "unit": "GW"},
#               {"ref": "c7", "name": "cost_per_gw", "value": 60e9, "unit": "USD/GW"}],
#    "formula": "gigawatts * cost_per_gw",
#    "result": 1800000000000, "unit": "USD",
#    "assumptions": ["Midpoint of the 25-35 GW consensus range"],
#    "as_of": "YYYY-MM-DD", "confidence": "high", "risk": "stable"}
#
# What this audit can and cannot do:
#   * CAN catch arithmetic that does not reproduce, dangling/circular
#     input references, formulas that reach outside pure arithmetic, and
#     derived claims resting on inputs the verifier rejected.
#   * CANNOT force the author to declare its arithmetic at all. The same
#     model writes the article, the ledger and the verifier findings, so
#     an undeclared sum simply never enters this audit. The gate makes a
#     DECLARED derivation checkable; it does not make declaration
#     mandatory. (The `formula`/`inputs`-without-`type: derived` check
#     below closes only the accidental version of that hole.)

_DERIVED_TYPE = "derived"
# The formula is LLM-authored and therefore untrusted input. It is never
# passed to eval()/exec(); it is parsed with ast.parse(mode="eval") and
# walked against this explicit node allowlist. Anything else — Call,
# Attribute, Subscript, Compare, comprehensions, walrus, f-strings — is
# a hard reject, so there is no name lookup, no attribute traversal and
# no callable in the evaluation path at all.
_DERIVED_ALLOWED_NODES: tuple[type[ast.AST], ...] = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,
    ast.Name,
    ast.Load,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
    ast.UAdd,
    ast.USub,
)
# Compute-bomb guards. `9**9**9` parses as three allowlisted nodes and
# would hang the runner, so the exponent is capped after the right
# operand is evaluated (inner-first evaluation means `9**9` = 387420489
# trips the cap at the outer Pow). The length/node caps bound parser work
# on pathological input.
_DERIVED_MAX_POW_EXPONENT = 64
_DERIVED_MAX_FORMULA_CHARS = 512
_DERIVED_MAX_FORMULA_NODES = 200
_DERIVED_DEFAULT_TOLERANCE = 0.01   # 1% relative
_DERIVED_DEFAULT_MAX_DEPTH = 5
# R7's traversal is path-sensitive, so a dense derived-on-derived graph
# costs O(branching ** max_depth). Bound total edge visits so a
# degenerate ledger fails closed instead of pinning the runner.
_DERIVED_MAX_GRAPH_STEPS = 100_000


class _FormulaError(ValueError):
    """Raised for any formula that fails R3 (shape) or R5 (evaluation)."""


def _parse_formula(formula: str) -> tuple[ast.Expression, set[str]]:
    """R3: parse `formula` under the whitelisted AST and return
    (tree, names_used). Raises _FormulaError on anything outside the
    allowlist. NEVER calls eval()/exec()."""
    if not isinstance(formula, str) or not formula.strip():
        raise _FormulaError("formula is missing or empty")
    if len(formula) > _DERIVED_MAX_FORMULA_CHARS:
        raise _FormulaError(
            f"formula is {len(formula)} chars, max {_DERIVED_MAX_FORMULA_CHARS}"
        )
    try:
        tree = ast.parse(formula, mode="eval")
    except (SyntaxError, ValueError, MemoryError, RecursionError) as e:
        raise _FormulaError(f"formula does not parse as an expression: {e}") from e

    names: set[str] = set()
    node_count = 0
    for node in ast.walk(tree):
        node_count += 1
        if node_count > _DERIVED_MAX_FORMULA_NODES:
            raise _FormulaError(
                f"formula has more than {_DERIVED_MAX_FORMULA_NODES} AST nodes"
            )
        if not isinstance(node, _DERIVED_ALLOWED_NODES):
            raise _FormulaError(
                f"formula uses disallowed syntax {type(node).__name__!r}; "
                f"only + - * / ** %, unary +/-, numeric literals and input "
                f"names are permitted"
            )
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(
                node.value, (int, float)
            ):
                raise _FormulaError(
                    f"formula contains a non-numeric literal "
                    f"{node.value!r} ({type(node.value).__name__})"
                )
        elif isinstance(node, ast.Name):
            if not isinstance(node.ctx, ast.Load):
                raise _FormulaError("formula may only read names, not assign them")
            names.add(node.id)
    return tree, names


def _eval_formula(tree: ast.Expression, env: dict[str, float]) -> float:
    """R5: evaluate a formula tree already checked by _parse_formula.

    Every intermediate value must stay a finite float. Division/modulo by
    zero, float overflow to inf/nan and out-of-range exponents are
    _FormulaError (a rejected claim), never a traceback."""

    def _num(value: float, what: str) -> float:
        if not math.isfinite(value):
            raise _FormulaError(f"{what} is not finite ({value})")
        return value

    def _walk(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return _walk(node.body)
        if isinstance(node, ast.Constant):
            try:
                return _num(float(node.value), "numeric literal")
            except OverflowError as e:
                raise _FormulaError(f"numeric literal overflows: {e}") from e
        if isinstance(node, ast.Name):
            if node.id not in env:
                raise _FormulaError(f"formula references unknown name {node.id!r}")
            return env[node.id]
        if isinstance(node, ast.UnaryOp):
            operand = _walk(node.operand)
            if isinstance(node.op, ast.UAdd):
                return operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise _FormulaError(f"unsupported unary operator {type(node.op).__name__}")
        if isinstance(node, ast.BinOp):
            left = _walk(node.left)
            right = _walk(node.right)
            op = node.op
            try:
                if isinstance(op, ast.Add):
                    out = left + right
                elif isinstance(op, ast.Sub):
                    out = left - right
                elif isinstance(op, ast.Mult):
                    out = left * right
                elif isinstance(op, ast.Div):
                    out = left / right
                elif isinstance(op, ast.Mod):
                    out = left % right
                elif isinstance(op, ast.Pow):
                    if abs(right) > _DERIVED_MAX_POW_EXPONENT:
                        raise _FormulaError(
                            f"exponent {right!r} exceeds the "
                            f"{_DERIVED_MAX_POW_EXPONENT} cap (compute-bomb guard)"
                        )
                    out = left ** right
                else:
                    raise _FormulaError(
                        f"unsupported binary operator {type(op).__name__}"
                    )
            except ZeroDivisionError as e:
                raise _FormulaError(f"division or modulo by zero: {e}") from e
            except OverflowError as e:
                raise _FormulaError(f"arithmetic overflow: {e}") from e
            except (TypeError, ValueError) as e:
                raise _FormulaError(f"arithmetic error: {e}") from e
            return _num(float(out), "intermediate result")
        raise _FormulaError(f"unsupported node {type(node).__name__}")

    return _walk(tree)


def _relative_diff(computed: float, declared: float) -> float:
    """Symmetric relative difference used by the R5 tolerance check.

    |computed - declared| / max(|computed|, |declared|); 0.0 when both
    are exactly zero. Symmetric (rather than dividing by the declared
    value) so a declared result of 0 with a non-zero computation is a
    clean 100% miss instead of a division by zero."""
    scale = max(abs(computed), abs(declared))
    if scale == 0.0:
        return 0.0
    return abs(computed - declared) / scale


def _is_number(value: object) -> bool:
    """Numeric for ledger purposes: int or float, not bool, and finite.
    `True` is an int in Python; a boolean input value is a schema error,
    not the number 1."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(float(value))
    except (OverflowError, ValueError):
        return False


def unsupported_claim_ids(findings_path: Path) -> set[str]:
    """Return the set of claim ids the verifier marked `unsupported`.

    Deliberately LENIENT at the boundary: a missing, unreadable or
    malformed findings file yields an empty set instead of raising. The
    canonical error for a bad verifier artifact belongs to
    --audit-verifier-findings / validate_verifier_artifact; this helper
    exists only to enrich R7, and must not change the exit code of a
    path that already has an owner.

    The join is by id string. The workflow prompt tells the verifier to
    reuse the claim-ledger ids (`c1`, `c2`, ...), so the namespaces line
    up by convention rather than by schema."""
    import json as _json

    try:
        data = _json.loads(findings_path.read_text(encoding="utf-8"))
    except (OSError, _json.JSONDecodeError):
        return set()
    claims = data.get("claims") if isinstance(data, dict) else None
    if not isinstance(claims, list):
        return set()
    out: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        if str(claim.get("verdict", "")).strip().lower() == "unsupported":
            cid = str(claim.get("id", "")).strip()
            if cid:
                out.add(cid)
    return out


def audit_derived_claims(
    ledger_path: Path,
    *,
    tolerance: float = _DERIVED_DEFAULT_TOLERANCE,
    max_depth: int = _DERIVED_DEFAULT_MAX_DEPTH,
    unsupported_ids: frozenset[str] | set[str] = frozenset(),
) -> tuple[int, list[dict]]:
    """Audit every `type: "derived"` entry in a claims-ledger JSON.

    Returns (derived_total, problems). `problems` entries are
    {"id": str, "rule": "R1".."R7", "message": str}; empty = pass. A
    ledger with no derived claims is a trivial pass — derived claims are
    an option the author may decline, not a quota.

    Rules (a derived claim fails if ANY of these is violated):
      R1 `inputs` is a non-empty list; each element carries ref, name,
         value (finite number, not bool) and a non-empty unit string.
         Names must be valid Python identifiers (an AST `Name` node can
         never carry "cost per gw", so a non-identifier name is reported
         as such rather than as a confusing R4 mismatch) and unique.
      R2 every `inputs[].ref` resolves to another claim id in the SAME
         ledger. Dangling refs and refs to an ambiguous duplicate id fail.
      R3 `formula` parses under the whitelisted AST (see
         _DERIVED_ALLOWED_NODES). Never eval()/exec().
      R4 the set of names in the formula equals the set of input names —
         no unbound name, no declared-but-unused input.
      R5 evaluating the formula with the input values reproduces
         `result` within `tolerance` (symmetric relative). Division by
         zero, overflow and non-finite intermediates are rejections, not
         crashes; Pow exponents are capped.
      R6 `assumptions` is a non-empty list of non-empty strings and
         `unit` is a non-empty string. Arithmetic without stated
         assumptions is not reproducible judgment, it is a bare number.
      R7 derived claims may reference other derived claims: reference
         CYCLES are rejected, the derived-to-derived dependency chain is
         capped at `max_depth` edges, and a derived claim whose
         transitive inputs include an id in `unsupported_ids` is itself
         unsupported.

    Limitations:
      * Units are checked for presence, not for dimensional consistency.
        "30 GW * $60B/GW = $1.8T" and "30 GW * 60 apples = 1800 apples"
        are equally acceptable here; the unit strings are for the reader.
      * `value` is trusted to match the referenced claim. Nothing in the
        ledger ties the number 30 to the prose of claim c3, so a derived
        claim can cite a real claim and then compute with a different
        number. Detecting that needs claim-text parsing, which this
        deliberately does not attempt.
      * R7's unsupported propagation only fires when the caller supplies
        `unsupported_ids`, and it looks at INPUTS only. A derived claim's
        own id appearing in `unsupported_ids` is ignored on purpose — the
        verifier marks derived sentences unsupported precisely because
        they carry no URL, which is the gap this audit closes. With no
        verifier findings passed at all, a derived claim resting entirely
        on rejected inputs passes silently.

    Raises ValueError if the ledger JSON is unreadable or has no
    top-level non-empty `claims[]` array (same contract as
    audit_verifier_findings).
    """
    import json as _json

    if tolerance < 0:
        raise ValueError(f"tolerance must be >= 0, got {tolerance}")
    if max_depth < 1:
        raise ValueError(f"max_depth must be >= 1, got {max_depth}")

    try:
        data = _json.loads(ledger_path.read_text(encoding="utf-8"))
    except (_json.JSONDecodeError, OSError) as e:
        raise ValueError(f"could not parse claims ledger JSON: {e}") from e

    claims = data.get("claims") if isinstance(data, dict) else None
    if not isinstance(claims, list):
        raise ValueError(
            "claims ledger JSON missing top-level 'claims' array; "
            f"got: {type(data).__name__}"
        )
    if not claims:
        raise ValueError("claims ledger JSON claims[] is empty")

    # Index the ledger. First id wins; duplicates are tracked so a ref
    # into an ambiguous id can be reported instead of silently resolving.
    by_id: dict[str, dict] = {}
    duplicate_ids: set[str] = set()
    for entry in claims:
        if not isinstance(entry, dict):
            continue
        cid = str(entry.get("id", "")).strip()
        if not cid:
            continue
        if cid in by_id:
            duplicate_ids.add(cid)
        else:
            by_id[cid] = entry

    def _is_derived(entry: dict) -> bool:
        return str(entry.get("type", "")).strip().lower() == _DERIVED_TYPE

    problems: list[dict] = []

    def _fail(cid: str, rule: str, message: str) -> None:
        problems.append({"id": cid, "rule": rule, "message": message})

    # Enumerate derived entries from `claims` DIRECTLY, never from
    # `by_id`. Indexing first-id-wins and then deriving the work list
    # from the index made two entries invisible to every rule below:
    #   * an entry with a missing/blank `id` was never indexed at all;
    #   * the SECOND entry sharing an id was dropped by first-id-wins.
    # In both cases the audit reported "0 derived claim(s)" and exited
    # 0 on a ledger whose arithmetic was wrong — a one-key bypass of the
    # whole gate. Every derived entry now gets a unique reportable
    # label, is counted, and is audited; a missing or duplicated id is
    # itself an R1 failure rather than a way to disappear.
    derived_entries: list[tuple[str, dict]] = []
    # Traversal keys for R7. Only an unambiguous id can be the TARGET of
    # an `inputs[].ref`, so the graph is keyed by those; label-keyed
    # entries can still be walk ORIGINS (see input_refs below).
    derived_set: set[str] = {
        cid for cid, e in by_id.items()
        if _is_derived(e) and cid not in duplicate_ids
    }
    for pos, entry in enumerate(claims, start=1):
        if not isinstance(entry, dict) or not _is_derived(entry):
            continue
        cid = str(entry.get("id", "")).strip()
        if not cid:
            label = f"claims[{pos}]"
            _fail(
                label, "R1",
                "derived claim has a missing or blank id, so nothing can "
                "reference it and it cannot be audited by id; give every "
                "derived claim a unique id",
            )
        elif cid in duplicate_ids:
            label = f"{cid}@claims[{pos}]"
            _fail(
                label, "R1",
                f"derived claim id {cid!r} is used by more than one ledger "
                f"entry; ids must be unique or a reference to it is "
                f"ambiguous",
            )
        else:
            label = cid
        derived_entries.append((label, entry))
    derived_ids = [label for label, _ in derived_entries]

    # A claim that carries derivation machinery but is not typed
    # `derived` would skip this audit entirely while still reading as
    # arithmetic to a human. Catch the accidental version of that
    # bypass. (No committed ledger in research/generative/ has these
    # keys, so this cannot fire retroactively.)
    for entry in claims:
        if not isinstance(entry, dict) or _is_derived(entry):
            continue
        stray = [k for k in ("formula", "inputs") if k in entry]
        if stray:
            _fail(
                str(entry.get("id", "")).strip() or "<no id>",
                "R1",
                f"carries {stray} but type is "
                f"{str(entry.get('type', '')).strip()!r}; arithmetic claims "
                f"must be typed {_DERIVED_TYPE!r} so they are recomputed",
            )

    derived_total = len(derived_ids)
    if derived_total == 0:
        return 0, problems

    # Per-claim structural + arithmetic rules.
    input_refs: dict[str, list[str]] = {}
    for cid, entry in derived_entries:
        env: dict[str, float] = {}
        refs: list[str] = []

        # ---- R1: inputs -------------------------------------------------
        # `env_ok` means "the name->value bindings are usable", and it is
        # the ONLY thing that gates R4/R5. A bad `ref` or a missing
        # `unit` records its own R1 problem (which fails the audit) but
        # leaves env_ok alone, so a unit typo cannot suppress the
        # recompute check and hide an arithmetic error behind itself.
        raw_inputs = entry.get("inputs")
        env_ok = isinstance(raw_inputs, list) and bool(raw_inputs)
        if not env_ok:
            _fail(cid, "R1", "inputs must be a non-empty array")
        else:
            seen_names: set[str] = set()
            for idx, item in enumerate(raw_inputs, start=1):
                where = f"inputs[{idx}]"
                if not isinstance(item, dict):
                    _fail(cid, "R1", f"{where} must be an object")
                    env_ok = False
                    continue
                ref = item.get("ref")
                name = item.get("name")
                value = item.get("value")
                unit = item.get("unit")
                if not isinstance(ref, str) or not ref.strip():
                    _fail(cid, "R1", f"{where} ref must be a non-empty string")
                else:
                    refs.append(ref.strip())
                if not isinstance(name, str) or not name.strip():
                    _fail(cid, "R1", f"{where} name must be a non-empty string")
                    env_ok = False
                elif not name.strip().isidentifier():
                    _fail(
                        cid, "R1",
                        f"{where} name {name!r} is not a valid identifier, so "
                        f"it can never appear in a formula",
                    )
                    env_ok = False
                elif name.strip() in seen_names:
                    _fail(cid, "R1", f"{where} duplicates input name {name.strip()!r}")
                    env_ok = False
                else:
                    seen_names.add(name.strip())
                if not _is_number(value):
                    _fail(
                        cid, "R1",
                        f"{where} value must be a finite number, got {value!r}",
                    )
                    env_ok = False
                elif isinstance(name, str) and name.strip().isidentifier():
                    env[name.strip()] = float(value)
                if not isinstance(unit, str) or not unit.strip():
                    _fail(cid, "R1", f"{where} unit must be a non-empty string")

        # ---- R2: refs resolve inside this ledger ------------------------
        for ref in refs:
            if ref == cid:
                _fail(cid, "R7", f"input ref {ref!r} points at its own claim (cycle)")
            elif ref in duplicate_ids:
                _fail(
                    cid, "R2",
                    f"input ref {ref!r} is ambiguous — the ledger has more "
                    f"than one claim with that id",
                )
            elif ref not in by_id:
                _fail(
                    cid, "R2",
                    f"input ref {ref!r} does not resolve to any claim id in "
                    f"this ledger",
                )
        input_refs[cid] = refs

        # ---- R6: assumptions + unit -------------------------------------
        assumptions = entry.get("assumptions")
        if not isinstance(assumptions, list) or not assumptions:
            _fail(cid, "R6", "assumptions must be a non-empty array")
        else:
            bad = [
                a for a in assumptions
                if not isinstance(a, str) or not a.strip()
            ]
            if bad:
                _fail(
                    cid, "R6",
                    f"assumptions must all be non-empty strings; bad "
                    f"entries: {bad[:3]!r}",
                )
        unit = entry.get("unit")
        if not isinstance(unit, str) or not unit.strip():
            _fail(cid, "R6", "unit must be a non-empty string")

        # ---- R3 + R4: formula shape and name binding --------------------
        tree: ast.Expression | None = None
        try:
            tree, names = _parse_formula(entry.get("formula"))
        except _FormulaError as e:
            _fail(cid, "R3", str(e))
            names = set()

        names_ok = False
        if tree is not None and env_ok:
            declared = set(env)
            missing = sorted(names - declared)
            unused = sorted(declared - names)
            if missing:
                _fail(
                    cid, "R4",
                    f"formula uses name(s) {missing} that are not declared "
                    f"in inputs",
                )
            if unused:
                _fail(
                    cid, "R4",
                    f"input(s) {unused} are declared but never used in the "
                    f"formula",
                )
            names_ok = not missing and not unused

        # ---- R5: recomputation ------------------------------------------
        if tree is not None and names_ok:
            declared_result = entry.get("result")
            if not _is_number(declared_result):
                _fail(
                    cid, "R5",
                    f"result must be a finite number, got {declared_result!r}",
                )
            else:
                try:
                    computed = _eval_formula(tree, env)
                except _FormulaError as e:
                    _fail(cid, "R5", f"formula could not be evaluated: {e}")
                else:
                    rel = _relative_diff(computed, float(declared_result))
                    if rel > tolerance:
                        _fail(
                            cid, "R5",
                            f"recomputation mismatch: formula yields "
                            f"{computed!r} but result declares "
                            f"{declared_result!r} "
                            f"({rel * 100:.4g}% off, tolerance "
                            f"{tolerance * 100:.4g}%)",
                        )

    # ---- R7: cycles, depth, transitive support --------------------------
    # `derived_set` was built above from unambiguous ids only — it is the
    # set of legal ref TARGETS. `derived_ids` holds the walk origins,
    # which may be synthetic labels for id-less/duplicated entries.
    # Path-sensitive traversal re-explores shared sub-graphs, so a dense
    # derived-on-derived ledger is O(branching ** max_depth). The ledger
    # is LLM-authored, so bound the total work and fail closed if the
    # graph is too big to verify rather than letting a runner spin.
    budget = [_DERIVED_MAX_GRAPH_STEPS]
    budget_reported = False

    for cid in derived_ids:
        # Walk the derived-to-derived edges from `cid`, carrying the
        # current path so a repeat on that path is a cycle (and the
        # recursion terminates instead of looping forever). `path` length
        # counts NODES, so `len(path) > max_depth` means the next edge
        # would be edge number max_depth+1: a derived claim built only
        # from retrieval claims is depth 0, and max_depth=5 permits a
        # five-edge chain. Both problems are reported at most once per
        # entry point so one bad graph does not flood the output.
        state = {"cycle": False, "depth": False}

        def _walk(node: str, path: tuple[str, ...], _cid=cid, _state=state) -> None:
            for ref in input_refs.get(node, []):
                if ref not in derived_set:
                    continue
                budget[0] -= 1
                if budget[0] < 0:
                    return
                if ref in path:
                    if not _state["cycle"]:
                        _state["cycle"] = True
                        _fail(
                            _cid, "R7",
                            "derived-claim reference cycle: "
                            + " -> ".join(path + (ref,)),
                        )
                    continue
                if len(path) > max_depth:
                    if not _state["depth"]:
                        _state["depth"] = True
                        _fail(
                            _cid, "R7",
                            f"derived dependency chain deeper than "
                            f"{max_depth}: " + " -> ".join(path + (ref,)),
                        )
                    continue
                _walk(ref, path + (ref,))

        _walk(cid, (cid,))
        if budget[0] < 0 and not budget_reported:
            budget_reported = True
            _fail(
                cid, "R7",
                f"derived-claim dependency graph exceeds the "
                f"{_DERIVED_MAX_GRAPH_STEPS} traversal-step budget; it is "
                f"too tangled to verify — flatten the derivations",
            )
            break

    if unsupported_ids:
        # INPUTS only — never the derived claim's own id. The verifier is
        # EXPECTED to mark a derived sentence `unsupported`: it has no
        # source URL, which is the entire gap this audit exists to close.
        # Self-taint would therefore fail every derived claim the moment
        # both flags are passed, i.e. exactly the case the feature is for.
        for cid in derived_ids:
            tainted: list[str] = []
            seen: set[str] = {cid}
            stack = list(input_refs.get(cid, []))
            while stack:
                ref = stack.pop()
                if ref in seen:
                    continue
                seen.add(ref)
                if ref in unsupported_ids:
                    tainted.append(ref)
                if ref in derived_set:
                    stack.extend(input_refs.get(ref, []))
            if tainted:
                _fail(
                    cid, "R7",
                    f"transitive input(s) {sorted(set(tainted))} were marked "
                    f"unsupported by the verifier, so the derived claim is "
                    f"unsupported too",
                )

    return derived_total, problems


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
    # Derived-claim recompute audit. Same audit-mode shape as
    # --audit-verifier-findings: point it at the claims ledger and it
    # exits 1 with a per-claim explanation when the arithmetic an
    # article performs from its cited inputs does not reproduce.
    p.add_argument(
        "--audit-derived-claims",
        type=str,
        default=None,
        metavar="PATH",
        help=(
            "path to .gen-claims-ledger.json. When set, every "
            "type='derived' entry is recompute-verified: inputs must "
            "resolve to other claims in the same ledger, the formula "
            "must parse under a whitelisted AST (never eval'd), and "
            "evaluating it must reproduce the declared result within "
            "--derived-tolerance. Reference cycles, over-deep "
            "dependency chains and derived claims resting on inputs "
            "the verifier rejected also fail. A ledger with no derived "
            "claims passes trivially. Pass it together with "
            "--audit-verifier-findings to enable the unsupported-input "
            "propagation check (R7)."
        ),
    )
    p.add_argument(
        "--derived-tolerance",
        type=float,
        default=_DERIVED_DEFAULT_TOLERANCE,
        metavar="FLOAT",
        help=(
            "relative tolerance for the derived-claim recompute check "
            f"(default {_DERIVED_DEFAULT_TOLERANCE} = 1%%). Compared "
            "symmetrically: |computed-declared| / max(|computed|, "
            "|declared|). Loosen it for claims stated as rounded "
            "headline figures; do not loosen it to paper over an "
            "arithmetic error."
        ),
    )
    p.add_argument(
        "--derived-max-depth",
        type=int,
        default=_DERIVED_DEFAULT_MAX_DEPTH,
        metavar="INT",
        help=(
            "maximum derived-to-derived dependency chain length "
            f"(default {_DERIVED_DEFAULT_MAX_DEPTH}). A derived claim "
            "built only from retrieval claims has depth 0."
        ),
    )
    p.add_argument(
        "--claims-ledger",
        type=str,
        default=None,
        metavar="PATH",
        help=(
            "path to .gen-claims-ledger.json. When provided, validate "
            "the source-tiered claim ledger schema used by the workflow "
            "methodology gate."
        ),
    )
    p.add_argument(
        "--redteam-findings",
        type=str,
        default=None,
        metavar="PATH",
        help=(
            "path to .gen-redteam-findings.json. When provided, validate "
            "that exactly three adversarial checks ran and none are "
            "placeholder redteam_failed entries."
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

    # Derived-claim recompute audit mode. Mirrors the verifier-findings
    # audit below: missing file = 2, malformed/failing = 1, clean = 0.
    #
    # Composition rule: when --audit-verifier-findings is ALSO passed, we
    # borrow its `unsupported` ids for R7 and then FALL THROUGH so the
    # verifier audit still runs and still owns the exit code. Passing
    # --audit-verifier-findings alone behaves exactly as it did before
    # this flag existed.
    if args.audit_derived_claims:
        ledger_path = Path(args.audit_derived_claims)
        if not ledger_path.exists():
            print(
                f"check: claims ledger file not found: {ledger_path}",
                file=sys.stderr,
            )
            return 2
        # R7's unsupported-input propagation needs the verifier's
        # verdicts. Without them the rule silently no-ops, and a derived
        # claim resting entirely on a REJECTED input passes with a clean
        # "0 failed" line — a contract rule not running looked exactly
        # like a contract rule passing. Two changes fix that: fall back
        # to the sibling verifier artifact the workflow writes next to
        # the ledger, and ALWAYS say on stderr which of the two happened.
        unsupported: set[str] = set()
        verifier_source: str | None = None
        if args.audit_verifier_findings:
            verifier_path = Path(args.audit_verifier_findings)
            if verifier_path.exists():
                # Lenient by design — a broken verifier artifact is the
                # verifier audit's error to report, not this one's.
                unsupported = unsupported_claim_ids(verifier_path)
                verifier_source = str(verifier_path)
        else:
            sibling = ledger_path.parent / ".gen-verifier-findings.json"
            if sibling.exists():
                unsupported = unsupported_claim_ids(sibling)
                verifier_source = f"{sibling} (auto-discovered sibling)"
        if verifier_source is None:
            print(
                "check: R7 unsupported-input propagation NOT checked — no "
                "verifier findings available (pass --audit-verifier-findings, "
                "or place .gen-verifier-findings.json beside the ledger). A "
                "derived claim resting on a rejected input will NOT be caught.",
                file=sys.stderr,
            )
        else:
            print(
                f"check: R7 unsupported-input propagation checked against "
                f"{verifier_source} ({len(unsupported)} unsupported id(s)).",
                file=sys.stderr,
            )
        try:
            derived_total, problems = audit_derived_claims(
                ledger_path,
                tolerance=args.derived_tolerance,
                max_depth=args.derived_max_depth,
                unsupported_ids=unsupported,
            )
        except ValueError as e:
            print(f"check: {e}", file=sys.stderr)
            return 1
        failing_ids = {p["id"] for p in problems}
        print(
            f"derived-claim audit: {derived_total} derived claim(s) in the "
            f"ledger; {len(failing_ids)} failed recompute verification "
            f"({len(problems)} problem(s)).",
            file=sys.stderr,
        )
        if problems:
            print(
                "Derived-claim verification failed. A derived claim is "
                "supported only if its inputs resolve and its arithmetic "
                "reproduces; fix the numbers, the formula, or drop the "
                "claim:",
                file=sys.stderr,
            )
            for prob in problems[:10]:
                print(
                    f"  - id={prob['id']} [{prob['rule']}]: {prob['message']}",
                    file=sys.stderr,
                )
            if len(problems) > 10:
                print(f"  ... and {len(problems) - 10} more", file=sys.stderr)
            return 1
        # Only short-circuit when this is the ONLY artifact check asked
        # for. --audit-derived-claims takes the same file as
        # --claims-ledger, so co-passing them is the natural wiring;
        # returning 0 here would silently skip the ledger-schema and
        # red-team gates that the caller explicitly requested.
        if not (
            args.audit_verifier_findings
            or args.claims_ledger
            or args.redteam_findings
        ):
            return 0
        # Fall through so the other requested checks still run and still
        # own the exit code. NOTE: the verifier-findings block below ends
        # in an unconditional return, so `--audit-verifier-findings`
        # co-passed with `--claims-ledger` still short-circuits the
        # methodology gate. That is pre-existing behaviour of that flag,
        # left untouched here.

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

    methodology_errors: list[str] = []
    if args.claims_ledger:
        claim_path = Path(args.claims_ledger)
        if not claim_path.exists():
            methodology_errors.append(f"methodology: claim ledger not found: {claim_path}")
        else:
            methodology_errors.extend(validate_claim_ledger(claim_path))
    if args.redteam_findings:
        redteam_path = Path(args.redteam_findings)
        if not redteam_path.exists():
            methodology_errors.append(f"methodology: red-team findings not found: {redteam_path}")
        else:
            methodology_errors.extend(validate_redteam_artifact(redteam_path))
    if args.claims_ledger or args.redteam_findings:
        if args.audit_verifier_findings:
            verifier_path = Path(args.audit_verifier_findings)
            if verifier_path.exists():
                methodology_errors.extend(validate_verifier_artifact(verifier_path))
        if methodology_errors:
            for line in methodology_errors:
                print(line, file=sys.stderr)
            return 1

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
