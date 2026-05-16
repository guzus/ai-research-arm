#!/usr/bin/env python3
"""Decompile a compiled `<article class="ara-doc">` HTML fragment back into
the `.ara.md` DSL that `compile_ara.py` would emit.

This is the inverse of `compile_ara.compile_source`. For every `emit_*`
function in the compiler there's a structural matcher here that walks the
HTML and rewrites it as a `:::directive(...)` block or as plain markdown.

We DO NOT trust class names alone. Several existing articles wrap blocks
in invented classes (`ara-references`, `ara-reflist`, `ara-refs`,
`ara-p`, `ara-ol`, `ara-link`, `ara-figcaption`, `ara-header`, `ara-dl`,
`ara-stats-dt`, `ara-stats-dd`). The decompiler matches on element shape
— `<ol>` whose `<li>` items have `id="ref-N"` is a references block
regardless of what class wraps it. Same logic for kv, stats, etc.

CLI:

    python3 scripts/decompile_ara.py path/to/article.html [-o out.ara.md]
    python3 scripts/decompile_ara.py path/to/article.html --in-place
    python3 scripts/decompile_ara.py --all
    python3 scripts/decompile_ara.py --all --verify
"""

from __future__ import annotations

import argparse
import io
import logging
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:  # pragma: no cover
    print(
        "decompile_ara: requires BeautifulSoup4. Install with: pip install beautifulsoup4",
        file=sys.stderr,
    )
    sys.exit(2)

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
GEN_DIR = REPO_ROOT / "research" / "generative"

LOG = logging.getLogger("decompile_ara")


# ----------------------------------------------------------------------
# YAML helpers — emit consistent, compiler-friendly YAML
# ----------------------------------------------------------------------


class _OrderedDumper(yaml.SafeDumper):
    """Default-flow-style off; quote strings that have markdown-significant
    characters (otherwise the YAML body could be misparsed as numbers,
    booleans, or anchors)."""


def _str_representer(dumper, data):
    """Use the literal block scalar for multiline; otherwise single line."""
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    # Force-quote anything that looks YAML-ambiguous (`123`, `yes`, `null`,
    # leading `-`, etc.) so we round-trip cleanly.
    needs_quote = bool(
        re.match(r"^[\s\-:?,&*!|>'\"%@`{}\[\]]", data)
        or re.match(r"^(true|false|null|yes|no|on|off|~)$", data, re.IGNORECASE)
        or re.match(r"^-?\d", data)
    )
    if needs_quote and not data.startswith("$"):
        # YAML can't represent backslash inside double-quoted scalars
        # without escaping; single-quoted handles everything except the
        # single quote itself, which we double.
        if "'" in data:
            quoted = data.replace("'", "''")
            return dumper.represent_scalar("tag:yaml.org,2002:str", quoted, style="'")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="'")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_OrderedDumper.add_representer(str, _str_representer)


def yaml_dump(obj: Any) -> str:
    """Dump as block-style YAML with stable ordering and good readability."""
    return yaml.dump(
        obj,
        Dumper=_OrderedDumper,
        sort_keys=False,
        allow_unicode=True,
        width=100,
        default_flow_style=False,
    ).rstrip("\n")


# ----------------------------------------------------------------------
# Text helpers — normalize HTML entities and tighten whitespace
# ----------------------------------------------------------------------

# The DSL is markdown — these characters need escaping when they appear
# as literal text inside a paragraph. We escape conservatively only.
INLINE_ESCAPE = re.compile(r"(?<!\\)([\[\]\\`*_])")
INLINE_ESCAPE_LIGHT = re.compile(r"(?<!\\)([\\`])")  # for use inside YAML strings


def _normalize_ws(text: str) -> str:
    """Collapse internal whitespace runs (including \xa0) to a single
    space, then strip. Mirrors how the compiler joins paragraph lines
    with a single space before parsing inline syntax."""
    if text is None:
        return ""
    text = text.replace("\xa0", " ").replace("​", "")
    text = re.sub(r"[ \t]*\n[ \t]*", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _node_text(node) -> str:
    """Plain text of a node with whitespace normalized — for cases where
    we only want a label/value and don't need to preserve inline syntax."""
    if node is None:
        return ""
    if isinstance(node, NavigableString):
        return _normalize_ws(str(node))
    return _normalize_ws(node.get_text(" "))


def _strip_outer_ws(s: str) -> str:
    return s.strip()


def _escape_paragraph_text(text: str) -> str:
    """Escape markdown sigils inside a literal text run so they survive a
    re-parse. We escape `\\`, `*`, `_`, `` ` ``, `[`, `]`. We do NOT
    escape `<` `>` because the compiler's inline pass escapes those itself
    after the markdown syntax has run."""
    return INLINE_ESCAPE.sub(r"\\\1", text)


# ----------------------------------------------------------------------
# Inline decompiler — walk a tag's children, emit markdown-ish text
# ----------------------------------------------------------------------

# Track consecutive citation indexes so `<sup><a>1</a></sup><sup><a>2</a></sup>`
# becomes `[^1,2]` rather than `[^1][^2]`. The walker uses a small state
# machine for this.
_CITE_INSIDE_SUP_RE = re.compile(r"^[0-9]+$")


def _classes(tag) -> set[str]:
    if not isinstance(tag, Tag):
        return set()
    cls = tag.get("class") or []
    return set(cls)


def _is_cite_sup(tag) -> bool:
    """`<sup><a class="ara-cite" href="#ref-N">N</a></sup>` — possibly with
    more than one cite inside the same `<sup>` already grouped."""
    if not isinstance(tag, Tag) or tag.name != "sup":
        return False
    cites = tag.find_all("a", class_="ara-cite")
    return bool(cites) and len(cites) == len(
        [c for c in tag.children if isinstance(c, Tag)]
    )


def _cite_ids(sup_tag: Tag) -> list[str]:
    """Extract the [N] indexes from a <sup>-wrapped citation cluster."""
    ids: list[str] = []
    for a in sup_tag.find_all("a", class_="ara-cite"):
        href = a.get("href", "")
        m = re.match(r"^#ref-(\d+)$", href)
        if m:
            ids.append(m.group(1))
        else:
            text = _node_text(a)
            if _CITE_INSIDE_SUP_RE.match(text):
                ids.append(text)
    return ids


def _wrap_inline_safely(tag: Tag, open_tok: str, close_tok: str, in_code: bool) -> str:
    """Render `<strong>` / `<em>` content with the bold/em wrapping
    placed *around segments*, not around the whole interior. The compiler
    in compile_ara.py has a recursion bug in `parse_inline`: when `**...**`
    wraps content that itself uses ``code`` or `[link](url)`, the inner
    recursive `parse_inline` call leaves dangling placeholders that crash
    the outer pass. By splitting the bold/em into per-segment wraps
    (text-only on one side, code/link on the other with bold *inside*),
    we avoid the bug entirely while preserving semantics."""
    if tag is None:
        return ""
    # Walk children. For text segments, wrap with the token. For code
    # spans we emit ``code`` raw (inline code can't be bolded in the
    # compiler anyway — `<strong><code>` would visually still appear bold
    # because of CSS, but losing the literal bold on a single inline
    # `code` token is a tolerable trade for avoiding the crash). For
    # link spans we move the bold *into* the link label so we emit
    # `[**text**](url)`.
    segments: list[str] = []

    def _flush_text(text: str):
        text = text.strip()
        if not text:
            return
        segments.append(f"{open_tok}{text}{close_tok}")

    for child in tag.children:
        if isinstance(child, NavigableString):
            txt = str(child).replace("\xa0", " ").replace("​", "")
            txt = re.sub(r"\s+", " ", txt).strip()
            if txt:
                segments.append(f"{open_tok}{_escape_paragraph_text(txt)}{close_tok}")
            continue
        if not isinstance(child, Tag):
            continue
        name = child.name.lower()
        classes = _classes(child)
        if name == "code":
            body = inline_to_md(child, in_code=True)
            segments.append("`" + body + "`")
            continue
        if name == "a":
            href = child.get("href", "")
            label = inline_to_md(child, in_code=in_code).strip()
            if not label:
                label = href
            if re.match(r"^(?:https?://|/)", href):
                # Wrap the label with the formatting token INSIDE the
                # link brackets — the compiler's LINK_RE parses link
                # labels separately, sidestepping the outer bold pass.
                lbl = label.replace("]", "\\]").replace("[", "\\[")
                segments.append(f"[{open_tok}{lbl}{close_tok}]({href})")
            else:
                segments.append(f"{open_tok}{label}{close_tok}")
            continue
        if _is_cite_sup(child):
            # A citation cluster inside a bold span gets emitted bare —
            # citations are rendered as <sup><a class="ara-cite"> which
            # the dashboard styles, not bolded.
            ids = _cite_ids(child)
            if ids:
                segments.append(f"[^{','.join(ids)}]")
                continue
        # For any other inline (em inside strong, span, etc.), render
        # without re-applying the outer formatting — losing nested
        # emphasis is acceptable; preserving the outer bold across mixed
        # children is not worth the compiler crash.
        inner = inline_to_md(child, in_code=in_code).strip()
        if inner:
            segments.append(f"{open_tok}{inner}{close_tok}")

    out = " ".join(s for s in segments if s.strip())
    # Repair the case where bold/em spans were joined by spaces that
    # don't belong — e.g. `[**foo**](url)**.**` (a period that ended up
    # in its own segment because of mixed children). We rely on the
    # paragraph emitter's natural whitespace handling here.
    return out


def inline_to_md(tag, *, in_code: bool = False) -> str:
    """Render the inline content of `tag` back to compiler-ready markdown.

    Walks children left-to-right, merging adjacent `<sup>` citation
    clusters into a single `[^a,b,c]` token, escaping bare text for
    markdown sigils, and converting wrappers (`<strong>`, `<em>`, ...)
    to their DSL form."""
    if tag is None:
        return ""
    out: list[str] = []
    pending_cites: list[str] = []

    def flush_cites():
        if pending_cites:
            out.append(f"[^{','.join(pending_cites)}]")
            pending_cites.clear()

    children = list(tag.children)
    for child in children:
        if isinstance(child, NavigableString):
            text = str(child).replace("\xa0", " ").replace("​", "")
            # Collapse internal newlines/whitespace to a single space —
            # the compiler joins paragraph lines on a single space.
            text = re.sub(r"[ \t]*\n[ \t]*", " ", text)
            text = re.sub(r"[ \t]+", " ", text)
            if not text:
                continue
            # If we have a pending cite cluster, only flush if this run
            # contains non-whitespace text.
            if text.strip():
                flush_cites()
            if in_code:
                out.append(text)
            else:
                out.append(_escape_paragraph_text(text))
            continue
        if not isinstance(child, Tag):
            continue
        name = child.name.lower()
        classes = _classes(child)
        # Citation cluster: collect consecutive <sup>...</sup> citations
        if _is_cite_sup(child):
            ids = _cite_ids(child)
            if ids:
                pending_cites.extend(ids)
                continue
            # If sup contains no cite info, fall through and render literally
        # Anything else flushes pending cites first
        flush_cites()

        # Self-closing display primitives
        if name == "span" and "ara-sparkline" in classes:
            pts = child.get("data-points", "")
            out.append("{sparkline:" + pts + "}")
            continue
        if name == "span" and "ara-flag" in classes:
            variant = None
            for c in classes:
                if c.startswith("ara-flag--"):
                    variant = c.split("--", 1)[1]
                    break
            if variant is None:
                LOG.warning("flag span missing variant: %s", child)
                variant = "green"
            out.append("{flag:" + variant + "}")
            continue
        if name == "span" and "ara-h2-num" in classes:
            num = _node_text(child)
            out.append("{h2num:" + num + "}")
            continue

        # Wrappers
        if name == "strong" and "ara-accent" in classes:
            body = inline_to_md(child, in_code=in_code)
            out.append("{accent}" + body + "{/}")
            continue
        if name == "span" and "ara-tag" in classes:
            body = inline_to_md(child, in_code=in_code)
            out.append("{tag}" + body + "{/}")
            continue
        if name == "mark":
            # `<mark class="ara-mark">` → `==...==` (the simpler form
            # round-trips through the compiler's MARK_RE).
            body = inline_to_md(child, in_code=in_code)
            # Escape stray `==` inside the body just in case.
            body = body.replace("==", "\\==")
            out.append("==" + body + "==")
            continue
        if name == "strong":
            out.append(_wrap_inline_safely(child, "**", "**", in_code))
            continue
        if name == "em":
            out.append(_wrap_inline_safely(child, "*", "*", in_code))
            continue
        if name == "code":
            # Inline code — never escape the body.
            body = inline_to_md(child, in_code=True)
            out.append("`" + body + "`")
            continue
        if name == "a":
            href = child.get("href", "")
            label = inline_to_md(child, in_code=in_code).strip()
            if not label:
                label = href
            # The compiler's LINK_RE only matches URLs starting with
            # http(s):// or /. If the href is `#ref-N`, it would be
            # treated as a citation already; if it's something else like
            # `mailto:`, we fall back to plain text + URL in parens.
            if re.match(r"^(?:https?://|/)", href):
                # The label cannot contain unbalanced `]` — escape it.
                label = label.replace("]", "\\]").replace("[", "\\[")
                # If the rendered label has formatting tokens, that's OK;
                # the compiler's link parser then re-parses them.
                out.append("[" + label + "](" + href + ")")
            else:
                LOG.info("link href not http(s)/relative; flattening: %r", href)
                out.append(label)
            continue
        if name == "br":
            # The DSL has no <br>. Emit a literal newline; the paragraph
            # emitter collapses these into spaces, which is fine for our
            # corpus (none of the existing articles depend on hard line
            # breaks inside paragraphs).
            out.append(" ")
            continue
        if name == "sup":
            body = inline_to_md(child, in_code=in_code)
            # Stub: no DSL primitive for arbitrary sup. The compiler's
            # output for citations is wrapped in <sup> so we only get
            # here for non-cite cases. Fall back to plain text.
            out.append(body)
            continue
        if name == "sub":
            body = inline_to_md(child, in_code=in_code)
            out.append(body)
            continue
        if name == "abbr":
            body = inline_to_md(child, in_code=in_code)
            out.append(body)
            continue
        if name == "time":
            body = inline_to_md(child, in_code=in_code)
            out.append(body)
            continue
        if name == "span":
            body = inline_to_md(child, in_code=in_code)
            # Plain ara-stat-unit handled by its caller. Otherwise drop the
            # wrapper.
            out.append(body)
            continue
        # Unknown inline tag — flatten content
        body = inline_to_md(child, in_code=in_code)
        out.append(body)

    flush_cites()
    text = "".join(out)
    # Collapse multiple spaces produced by joining
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" ([.,;:!?\)])", r"\1", text)
    return text.strip()


# ----------------------------------------------------------------------
# Header / frontmatter
# ----------------------------------------------------------------------


def extract_header(root: Tag) -> dict[str, Any]:
    """Pull the article header into a frontmatter dict.

    Accepts both the canonical form (loose `<span class="ara-eyebrow">` +
    `<h2 class="ara-display">` siblings of the article body) and the
    `<header class="ara-header">` wrapper form. Stats inside the header
    `<dl class="ara-stats">` or `<div class="ara-stats">` become the
    `stats:` frontmatter entry."""
    meta: dict[str, Any] = {}

    # A real <header> wrapper takes precedence; otherwise loose siblings
    # at the top of the <article>.
    header = root.find("header")
    if header is not None and header.parent is root:
        scope = header
    else:
        scope = root

    # eyebrow
    eyebrow = scope.find(class_="ara-eyebrow")
    if eyebrow:
        meta["eyebrow"] = inline_to_md(eyebrow)

    # display
    display = scope.find(class_="ara-display")
    if display:
        meta["title"] = inline_to_md(display)

    # deck
    deck = scope.find(class_="ara-deck")
    if deck:
        meta["deck"] = inline_to_md(deck)

    # lede (only the first one inside the scope — additional ara-lede are
    # rare and probably a writer error)
    lede = scope.find(class_="ara-lede")
    if lede:
        meta["lede"] = inline_to_md(lede)

    # stats inside header
    stats = None
    if header is not None and header.parent is root:
        stats = header.find(class_="ara-stats")
    if stats is None:
        # Some authors put the header stats outside the <header> wrapper.
        # Only adopt the FIRST ara-stats block as header stats if it
        # appears before any heading.
        for child in root.children:
            if isinstance(child, Tag):
                if child.name in ("h3", "h4") or "ara-h2" in _classes(child):
                    break
                if "ara-stats" in _classes(child) and child.name != "header":
                    stats = child
                    break
    if stats is not None:
        items = decompile_stats_items(stats)
        if items:
            meta["stats"] = items
            # Mark this node so the body walker skips it
            stats["__ara_consumed"] = "1"

    return meta


# ----------------------------------------------------------------------
# Stats and KV
# ----------------------------------------------------------------------


def decompile_stats_items(node: Tag) -> list[dict[str, Any]]:
    """Convert an `ara-stats` container into the list-of-dicts the
    `:::stats` directive expects. Accepts these structural variants:

    1. `<dl class="ara-stats">` with `<div class="ara-stat"><dt>L</dt><dd>V</dd></div>`
       (invented form using ara-stats-dt/dd or plain dt/dd)
    2. `<div class="ara-stats">` with `<div class="ara-stat"><span class="ara-stat-label">L</span><div class="ara-stat-value">V</div>...`
       (canonical form)
    3. `<section class="ara-stats">` with `<div class="ara-stat"><p class="ara-stat-figure">V</p><p class="ara-stat-label">L</p></div>`
       (invented form using ara-stat-figure for value, label is descriptive)
    """
    items: list[dict[str, Any]] = []
    for stat in node.find_all(class_="ara-stat", recursive=True):
        # Form 2 / 3: explicit value class (canonical ara-stat-value OR
        # invented ara-stat-figure). Both denote "the big number."
        label_node = stat.find(class_="ara-stat-label")
        value_node = stat.find(class_="ara-stat-value") or stat.find(class_="ara-stat-figure")
        note_node = stat.find(class_="ara-stat-note")
        if label_node and value_node:
            label = inline_to_md(label_node)
            # The value might wrap an <span class="ara-stat-unit">...</span>
            unit_node = value_node.find(class_="ara-stat-unit")
            unit = None
            if unit_node:
                unit = inline_to_md(unit_node)
                # Remove the unit from the value while preserving rest.
                unit_node.extract()
            value = inline_to_md(value_node)
            item: dict[str, Any] = {"label": label, "value": value}
            if unit:
                item["unit"] = unit
            if note_node:
                item["note"] = inline_to_md(note_node)
            items.append(item)
            continue
        # Form 1: <dt>/<dd> inside <div class="ara-stat">
        dt = stat.find("dt")
        dd = stat.find("dd")
        if dt and dd:
            items.append({"label": inline_to_md(dt), "value": inline_to_md(dd)})
            continue
        # Bare ara-stat with just text content
        text = inline_to_md(stat)
        if text:
            LOG.warning(
                "ara-stat lacked label/value structure; capturing as label-only: %r",
                text[:60],
            )
            items.append({"label": text, "value": ""})
    return items


def looks_like_stats(node: Tag) -> bool:
    if "ara-stats" not in _classes(node):
        return False
    return bool(node.find(class_="ara-stat"))


def looks_like_kv(node: Tag) -> bool:
    """Structural test: it's either a `<dl>` whose direct children are
    paired `<dt>`/`<dd>` (treated as kv), OR a `<div class="ara-kv">`,
    OR a `<dl class="ara-kv">`. We exclude the case where the `<dl>`
    holds `<div class="ara-stat">` items (which is the stats form)."""
    if "ara-kv" in _classes(node):
        # The stats form sometimes uses dl class="ara-stats" with inner
        # divs; for ara-kv specifically there should be no ara-stat child.
        return not node.find(class_="ara-stat")
    if "ara-dl" in _classes(node):
        return True
    if node.name == "dl" and not _classes(node):
        # Anonymous <dl> — only if it has dt/dd pairs and no ara-stat.
        if node.find(class_="ara-stat"):
            return False
        if node.find("dt") and node.find("dd"):
            return True
    return False


def decompile_kv(node: Tag) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    # Some <div class="ara-kv"> articles put the <dt>/<dd> directly inside
    # the div (no nested dl). BeautifulSoup still surfaces them.
    children = [c for c in node.children if isinstance(c, Tag)]
    # Walk dt → dd pairs
    pending_dt: list[Tag] = []
    for ch in children:
        if ch.name == "dt":
            pending_dt.append(ch)
        elif ch.name == "dd":
            if pending_dt:
                term = inline_to_md(pending_dt.pop(0))
                items.append({"term": term, "def": inline_to_md(ch)})
            else:
                LOG.warning("dd without preceding dt in kv block; dropping")
    # If we didn't see direct dt/dd (likely div-wrapper case), do a
    # full-descendants walk.
    if not items:
        dts = node.find_all("dt")
        dds = node.find_all("dd")
        for dt, dd in zip(dts, dds):
            items.append({"term": inline_to_md(dt), "def": inline_to_md(dd)})
    return items


# ----------------------------------------------------------------------
# References
# ----------------------------------------------------------------------


def looks_like_references(node: Tag) -> bool:
    """An `<ol>` whose `<li>` children carry `id="ref-N"`. The class can be
    anything (`ara-references`, `ara-reflist`, `ara-refs`, or nothing).
    Also accepts a `<footer>` whose only content is such a list."""
    if node.name != "ol":
        return False
    lis = node.find_all("li", recursive=False)
    if not lis:
        return False
    ref_lis = [li for li in lis if re.match(r"^ref-\d+$", li.get("id", ""))]
    return len(ref_lis) >= max(1, len(lis) // 2)


REF_TITLE_TRAILING_DATE_RE = re.compile(r"\s*\(([^)]+)\)\s*$")
REF_TRAILING_SOURCE_RE = re.compile(r"\s*[—–-]\s*(.+?)\s*$")


def decompile_references(node: Tag) -> list[dict[str, Any]]:
    """Recover the four reference fields (`id`, `title`, `url?`, `source?`,
    `date?`) from a `<li id="ref-N">` row.

    The compiler's `emit_references` joins them in one of two patterns:

        <li id="ref-N"><a href="URL">TITLE</a> — SOURCE (DATE)</li>   # title is link label
        <li id="ref-N">TITLE — SOURCE (DATE)</li>                     # title only, no url

    Existing articles use a third pattern more often than the spec
    contemplates:

        <li id="ref-N">LEADING TITLE TEXT... <a href="URL">domain.com</a></li>

    where the link text is just the domain, and the real title is the
    leading prose. We need to recover the title from the LEADING text
    when present, and only fall back to the link label when the leading
    text is empty.
    """
    items: list[dict[str, Any]] = []
    for li in node.find_all("li", recursive=False):
        rid_raw = li.get("id", "")
        m = re.match(r"^ref-(\d+)$", rid_raw)
        if not m:
            LOG.warning(
                "reference <li> without id=ref-N: %r — assigning sequential id",
                rid_raw,
            )
            rid: Any = len(items) + 1
        else:
            rid = int(m.group(1))

        # Grab the LAST <a> (closest to the URL pattern). If there are
        # multiple <a>s, we still treat the last one as the canonical URL.
        anchors = li.find_all("a", recursive=True)
        url: str | None = None
        a_label = ""
        if anchors:
            a = anchors[-1]
            url = a.get("href", "") or None
            a_label = inline_to_md(a).strip()

        # Compute the leading text (everything before the last <a>).
        leading_text = ""
        trailing_text = ""
        if anchors:
            a = anchors[-1]
            # Clone the LI and remove the trailing <a> to extract the
            # leading text without mutating the source tree.
            li_copy = BeautifulSoup(str(li), "html.parser").find("li")
            anchors_copy = li_copy.find_all("a")
            last_a_copy = anchors_copy[-1]
            # Find what comes after the last <a> in the copy
            tail_nodes = []
            for sib in last_a_copy.next_siblings:
                tail_nodes.append(sib)
            trailing_text = "".join(
                str(n) if not isinstance(n, Tag) else n.get_text(" ")
                for n in tail_nodes
            )
            trailing_text = _normalize_ws(trailing_text)
            # Now remove the last <a> and grab the rest of the LI content
            last_a_copy.extract()
            # Also clear trailing text we just captured (which is what
            # was after the link)
            leading_text = inline_to_md(li_copy).strip()
            if trailing_text and leading_text.endswith(trailing_text):
                leading_text = leading_text[: -len(trailing_text)].strip()
        else:
            leading_text = inline_to_md(li).strip()

        # Three reference layouts in the wild:
        #
        # (A) <a href="URL">TITLE</a> — SOURCE [(DATE)]
        #     Canonical: title is the link label, source is trailing text.
        # (B) LEADING TITLE TEXT... <a href="URL">domain.com</a>
        #     Invented: title is the leading prose, link is a URL hint.
        # (C) TITLE without any link.
        title = ""
        source: str | None = None
        date: str | None = None

        if anchors:
            # Heuristic: if the link label is short and looks like a
            # bare URL/domain (`example.com`, `sec.gov/...`), it's a
            # URL hint — the real title is in the leading text (case B).
            looks_like_domain = bool(
                a_label
                and re.match(
                    r"^[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:/[\w./%~?#=&-]*)?\.?$",
                    a_label,
                )
            )
            if leading_text and (looks_like_domain or len(leading_text) > len(a_label) * 2):
                # Case B: title is the leading text
                title = leading_text
                # If there's substantial trailing text after the URL hint
                # (rare), append it.
                if trailing_text and trailing_text.strip("., "):
                    title = title.rstrip(".").strip() + ". " + trailing_text.strip()
            else:
                # Case A: title is the link label, source is trailing.
                title = a_label
                tail = trailing_text or ""
                if tail:
                    m_date = REF_TITLE_TRAILING_DATE_RE.search(tail)
                    if m_date:
                        candidate = m_date.group(1).strip()
                        # Only treat as date if it looks date-ish (numbers
                        # + month name OR year). Otherwise leave inline.
                        if re.search(r"\d{4}|\d{1,2}/\d{1,2}|January|February|March|April|May|June|July|August|September|October|November|December", candidate):
                            date = candidate
                            tail = REF_TITLE_TRAILING_DATE_RE.sub("", tail).strip()
                    # Leading em-dash / hyphen / en-dash signifies source
                    m_src = re.match(r"^\s*[—–-]\s*(.+)\s*$", tail, re.DOTALL)
                    if m_src:
                        source_text = m_src.group(1).strip().rstrip(".")
                        if source_text:
                            source = source_text
                    elif tail.strip(".,—– "):
                        # Trailing text without an em-dash separator;
                        # append it to title so we don't lose data.
                        title = title.rstrip(".").strip() + ". " + tail.strip()
        else:
            title = leading_text

        # Final cleanup
        title = re.sub(r"\.\s*$", "", title).strip()

        item: dict[str, Any] = {"id": rid, "title": title}
        if url:
            item["url"] = url
        if source:
            item["source"] = source
        if date:
            item["date"] = date
        items.append(item)
    return items


# ----------------------------------------------------------------------
# Tables
# ----------------------------------------------------------------------


def decompile_table(table: Tag) -> str:
    """`<table class="ara-table">` → markdown table. Prefixes the first
    cell of `<tr class="ara-row-highlight">` rows with `*`."""
    thead = table.find("thead")
    tbody = table.find("tbody")
    header_cells: list[str] = []
    if thead:
        tr = thead.find("tr")
        if tr:
            for th in tr.find_all(["th", "td"], recursive=False):
                header_cells.append(_md_table_cell(inline_to_md(th)))
    else:
        # Some articles skip <thead>; treat the first <tr> as the header.
        first_tr = table.find("tr")
        if first_tr:
            for th in first_tr.find_all(["th", "td"], recursive=False):
                header_cells.append(_md_table_cell(inline_to_md(th)))

    rows: list[tuple[bool, list[str]]] = []
    body_trs = []
    if tbody:
        body_trs = tbody.find_all("tr", recursive=False)
    else:
        all_trs = table.find_all("tr", recursive=False)
        body_trs = all_trs[1:] if thead is None and all_trs else all_trs
    for tr in body_trs:
        highlight = "ara-row-highlight" in _classes(tr)
        cells = [
            _md_table_cell(inline_to_md(td))
            for td in tr.find_all(["td", "th"], recursive=False)
        ]
        rows.append((highlight, cells))

    if not header_cells and rows:
        # Synthesize a blank header from the first row width
        header_cells = [""] * max(len(r[1]) for r in rows)

    width = max(len(header_cells), max((len(r[1]) for r in rows), default=0))
    header_cells = (header_cells + [""] * width)[:width]

    out_lines = ["| " + " | ".join(header_cells) + " |"]
    out_lines.append("|" + "|".join(["---"] * width) + "|")
    for highlight, cells in rows:
        padded = (cells + [""] * width)[:width]
        if highlight and padded:
            padded[0] = "*" + padded[0]
        out_lines.append("| " + " | ".join(padded) + " |")
    return "\n".join(out_lines)


def _md_table_cell(text: str) -> str:
    """Escape pipes inside cells; collapse newlines."""
    return text.replace("|", "\\|").replace("\n", " ")


# ----------------------------------------------------------------------
# Other directive matchers
# ----------------------------------------------------------------------


CALLOUT_KINDS = ("info", "success", "warn", "danger")


def decompile_callout(node: Tag) -> tuple[dict, str]:
    """Return (attrs, body markdown). Body keeps inner block structure."""
    kind = "info"
    for c in _classes(node):
        if c.startswith("ara-callout--"):
            k = c.split("--", 1)[1]
            if k in CALLOUT_KINDS:
                kind = k
                break
    label = None
    label_node = node.find(class_="ara-callout-label")
    if label_node:
        label = inline_to_md(label_node)
        label_node.extract()
    attrs = {"kind": kind}
    if label:
        attrs["label"] = label
    body = _block_children_to_md(node)
    return attrs, body


def decompile_figure(node: Tag) -> dict:
    img = node.find("img")
    cap = node.find(class_="ara-caption") or node.find(class_="ara-figcaption") or node.find("figcaption")
    attrs = {
        "src": img.get("src", "") if img else "",
        "alt": img.get("alt", "") if img else "",
    }
    if cap:
        attrs["caption"] = inline_to_md(cap)
    return attrs


def decompile_quote(node: Tag) -> tuple[str | None, str]:
    """Return (attribution, body markdown). The caller chooses between
    the simple `> ... — attr` form and the `:::quote(attr=)` form."""
    attr_node = node.find(class_="ara-quote-attr")
    attr = inline_to_md(attr_node) if attr_node else None
    if attr_node:
        attr_node.extract()
    # The quote body may be a series of <p> or just inline text.
    body = _block_children_to_md(node) or inline_to_md(node)
    return attr, body


def decompile_timeline(node: Tag) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for li in node.find_all("li", class_="ara-timeline-item"):
        date = li.find(class_="ara-timeline-date")
        ev = li.find(class_="ara-timeline-event")
        headline_tag = ev.find("strong") if ev else None
        body_tag = ev.find("p") if ev else None
        item: dict[str, Any] = {
            "date": _node_text(date) if date else "",
            "headline": inline_to_md(headline_tag) if headline_tag else "",
        }
        if body_tag:
            item["body"] = inline_to_md(body_tag)
        items.append(item)
    return items


def decompile_bars(node: Tag) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for bar in node.find_all(class_="ara-bar"):
        label = bar.find(class_="ara-bar-label")
        value = bar.find(class_="ara-bar-value")
        pct = bar.get("data-pct", 0)
        try:
            pct_val: Any = int(float(pct))
        except (TypeError, ValueError):
            pct_val = pct
        items.append(
            {
                "label": inline_to_md(label) if label else "",
                "value": inline_to_md(value) if value else "",
                "pct": pct_val,
            }
        )
    return items


def decompile_donut(node: Tag) -> tuple[dict, list[dict[str, Any]]]:
    labels = node.get("data-labels", "").split(",") if node.get("data-labels") else []
    values = node.get("data-values", "").split(",") if node.get("data-values") else []
    items = []
    for label, value in zip(labels, values):
        # Try to coerce value to a number for nicer YAML.
        try:
            v: Any = float(value)
            if v.is_integer():
                v = int(v)
        except ValueError:
            v = value.strip()
        items.append({"label": label.strip(), "value": v})
    attrs = {}
    center = node.get("data-center-label")
    if center:
        attrs["center-label"] = center
    return attrs, items


def decompile_slope(node: Tag) -> tuple[dict, str]:
    items = node.get("data-items", "").split(",") if node.get("data-items") else []
    left = node.get("data-left-values", "").split(",") if node.get("data-left-values") else []
    right = node.get("data-right-values", "").split(",") if node.get("data-right-values") else []
    attrs = {}
    for key in ("left-label", "right-label", "unit"):
        v = node.get(f"data-{key}")
        if v:
            attrs[key] = v
    # Compose a markdown table — header "Item | Left | Right"
    header = ["Item", attrs.get("left-label", "Left"), attrs.get("right-label", "Right")]
    lines = ["| " + " | ".join(header) + " |"]
    lines.append("|---|---|---|")
    for item, l, r in zip(items, left, right):
        lines.append(f"| {item.strip()} | {l.strip()} | {r.strip()} |")
    return attrs, "\n".join(lines)


def decompile_line_chart(node: Tag) -> tuple[dict, str]:
    """Reverse of emit_line_chart: dump x: ... + each series LABEL: ..."""
    attrs: dict[str, Any] = {}
    for k in ("title", "subtitle", "y-unit"):
        v = node.get(f"data-{k}")
        if v:
            attrs[k] = v
    body_lines = []
    x_labels = node.get("data-x-labels", "")
    if x_labels:
        body_lines.append("x: " + x_labels)
    for i in range(1, 5):
        series = node.get(f"data-series-{i}")
        label = node.get(f"data-series-{i}-label") or f"Series {i}"
        if series:
            body_lines.append(f"{label}: {series}")
    return attrs, "\n".join(body_lines)


def decompile_iso_group(nodes: list[Tag]) -> list[dict[str, Any]]:
    """Group of consecutive `<div class="ara-iso">` siblings → one
    `:::iso` directive with a YAML list of `{label, glyph, count}`."""
    items: list[dict[str, Any]] = []
    for node in nodes:
        label = node.find(class_="ara-iso-label")
        glyphs = node.find(class_="ara-iso-glyphs")
        total = node.find(class_="ara-iso-total")
        glyph = glyphs.get("data-glyph", "") if glyphs else ""
        count = glyphs.get("data-count", "") if glyphs else (_node_text(total) if total else "0")
        try:
            count_val: Any = int(count)
        except (TypeError, ValueError):
            count_val = count
        items.append(
            {
                "label": inline_to_md(label) if label else "",
                "glyph": glyph,
                "count": count_val,
            }
        )
    return items


def decompile_stack_bar(node: Tag, legend_node: Tag | None) -> tuple[dict, list[dict[str, Any]]]:
    items: list[dict[str, Any]] = []
    segs = node.find_all(class_="ara-stack-seg", recursive=False)
    legend_items = []
    if legend_node:
        for li in legend_node.find_all("li", recursive=True):
            # remove the dot span if present
            dot = li.find(class_="ara-stack-dot")
            if dot:
                dot.extract()
            legend_items.append(inline_to_md(li))
    for idx, seg in enumerate(segs):
        try:
            pct: Any = int(float(seg.get("data-pct", 0)))
        except (TypeError, ValueError):
            pct = seg.get("data-pct", 0)
        item: dict[str, Any] = {"pct": pct}
        if idx < len(legend_items):
            item["label"] = legend_items[idx]
        else:
            item["label"] = ""
        items.append(item)
    attrs: dict[str, Any] = {}
    if legend_node:
        attrs["legend"] = True
    return attrs, items


def decompile_stack_rows(node: Tag) -> tuple[dict, dict]:
    cats_legend = node.find(class_="ara-stack-rows-legend")
    cats: list[str] = []
    if cats_legend:
        for c in cats_legend.find_all(class_="ara-stack-rows-cat"):
            cats.append(inline_to_md(c))
    rows = []
    for row in node.find_all(class_="ara-stack-rows-row"):
        label_node = row.find(class_="ara-stack-rows-label")
        label = inline_to_md(label_node) if label_node else ""
        bar = row.find(class_="ara-stack-bar")
        values: list[Any] = []
        if bar:
            for seg in bar.find_all(class_="ara-stack-seg"):
                try:
                    pct: Any = int(float(seg.get("data-pct", 0)))
                except (TypeError, ValueError):
                    pct = seg.get("data-pct", 0)
                values.append(pct)
        rows.append({"label": label, "values": values})
    return {}, {"categories": cats, "rows": rows}


def decompile_rank_list(node: Tag) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for li in node.find_all("li", class_="ara-rank-item"):
        rank = li.find(class_="ara-rank-num")
        label = li.find(class_="ara-rank-label")
        value = li.find(class_="ara-rank-value")
        fill = li.find(class_="ara-rank-fill")
        pct: Any = 0
        if fill:
            try:
                pct = int(float(fill.get("data-pct", 0)))
            except (TypeError, ValueError):
                pct = fill.get("data-pct", 0)
        item: dict[str, Any] = {
            "label": inline_to_md(label) if label else "",
            "value": inline_to_md(value) if value else "",
            "pct": pct,
        }
        if rank is not None:
            rank_txt = _node_text(rank)
            try:
                rank_val: Any = int(rank_txt)
                if rank_val != len(items) + 1:
                    item["rank"] = rank_val
            except ValueError:
                if rank_txt:
                    item["rank"] = rank_txt
        if "ara-row-highlight" in _classes(li):
            item["highlight"] = True
        items.append(item)
    return items


def decompile_compare(node: Tag) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for card in node.find_all(class_="ara-compare-card", recursive=False):
        role = card.find(class_="ara-compare-role")
        name = card.find(class_="ara-compare-name")
        value = card.find(class_="ara-compare-value")
        item: dict[str, Any] = {
            "role": inline_to_md(role) if role else "",
            "name": inline_to_md(name) if name else "",
            "value": inline_to_md(value) if value else "",
        }
        items.append(item)
    return items


# ----------------------------------------------------------------------
# Block walker
# ----------------------------------------------------------------------


# Wrappers we transparently descend into (they hold blocks, not state).
TRANSPARENT_WRAPPERS = {"section", "div"}
# Headings that map back to the DSL.
HEADING_MAP = {
    "h3": "## ",  # paired with ara-h2 class
    "h4": "### ",  # paired with ara-h3 (default subsection)
}


def _block_children_to_md(parent: Tag) -> str:
    """Render the block-level children of `parent` to markdown."""
    out: list[str] = []
    children = [c for c in parent.children if isinstance(c, Tag) or (isinstance(c, NavigableString) and str(c).strip())]
    i = 0
    while i < len(children):
        node = children[i]
        # Skip stray whitespace strings
        if isinstance(node, NavigableString):
            i += 1
            continue
        # Skip nodes already consumed by the header pass
        if node.get("__ara_consumed"):
            i += 1
            continue
        # Recognize iso groups
        if "ara-iso" in _classes(node):
            group = [node]
            j = i + 1
            while j < len(children) and isinstance(children[j], Tag) and "ara-iso" in _classes(children[j]):
                group.append(children[j])
                j += 1
            items = decompile_iso_group(group)
            out.append(directive_block("iso", {}, yaml_dump(items)))
            i = j
            continue
        # Recognize stack-bar + (optional) immediately following legend
        if "ara-stack-bar" in _classes(node) and "ara-stack-seg" not in _classes(node):
            # Avoid double-handling nested stack-bars inside stack-rows.
            if node.find_parent(class_="ara-stack-rows") is None:
                legend = None
                if i + 1 < len(children):
                    nxt = children[i + 1]
                    if isinstance(nxt, Tag) and "ara-stack-legend" in _classes(nxt):
                        legend = nxt
                attrs, items = decompile_stack_bar(node, legend)
                out.append(directive_block("stack-bar", attrs, yaml_dump(items)))
                i += 2 if legend else 1
                continue
        emitted = _try_emit_node(node)
        if emitted is not None:
            out.append(emitted)
        i += 1
    # Separate adjacent blocks with a blank line
    return "\n\n".join(b for b in out if b is not None and b != "")


def _try_emit_node(node: Tag) -> str | None:
    classes = _classes(node)
    name = node.name.lower()

    # Recognized inline-class wrappers that don't appear at block level
    if name == "header":
        # Already handled at extract_header time; if it survived, walk
        # its children as blocks (rare).
        return _block_children_to_md(node)

    # Strip ara-section wrappers — the compiler re-adds them based on ##.
    if name == "section" and "ara-section" in classes:
        return _block_children_to_md(node)

    # Strip <footer> — usually the references container; the inner ol
    # gets recognized via looks_like_references. If it's a colophon,
    # we capture as :::raw.
    if name == "footer":
        body = _block_children_to_md(node)
        # If the footer only held a references block, body is the
        # references directive already.
        return body

    # Stats — block form
    if looks_like_stats(node):
        items = decompile_stats_items(node)
        return directive_block("stats", {}, yaml_dump(items))

    # KV — block form
    if looks_like_kv(node):
        items = decompile_kv(node)
        return directive_block("kv", {}, yaml_dump(items))

    # Callout
    if name == "div" and any(c == "ara-callout" or c.startswith("ara-callout--") for c in classes):
        attrs, body = decompile_callout(node)
        return directive_block("callout", attrs, body, body_kind="markdown")

    # Figure
    if name == "figure" and "ara-figure" in classes:
        attrs = decompile_figure(node)
        return directive_block("figure", attrs, "", body_kind="markdown")

    # Quote
    if name == "blockquote":
        attr, body = decompile_quote(node)
        # Prefer the simple `> ...` form when the body is a single paragraph.
        # Strip a wrapper <p> if present.
        body = body.strip()
        # Remove leading "<p>" / "</p>" tags if we ended up with a single-para body.
        body_text = re.sub(r"^>\s*", "", body)
        # If the body is a single block, emit > form. Otherwise wrap in :::quote.
        if "\n\n" in body_text:
            attrs = {}
            if attr:
                attrs["attr"] = attr
            return directive_block("quote", attrs, body_text, body_kind="markdown")
        lines = ["> " + body_text]
        if attr:
            lines.append("> — " + attr)
        return "\n".join(lines)

    # Line chart
    if name == "div" and "ara-line-chart" in classes:
        attrs, body = decompile_line_chart(node)
        return directive_block("line-chart", attrs, body, body_kind="lines")

    # Donut
    if name == "div" and "ara-donut" in classes:
        attrs, items = decompile_donut(node)
        return directive_block("donut", attrs, yaml_dump(items))

    # Slope
    if name == "div" and "ara-slope" in classes:
        attrs, body = decompile_slope(node)
        return directive_block("slope", attrs, body, body_kind="lines")

    # Timeline
    if name == "ol" and "ara-timeline" in classes:
        items = decompile_timeline(node)
        return directive_block("timeline", {}, yaml_dump(items))

    # Bars (group)
    if name == "div" and "ara-bars" in classes:
        items = decompile_bars(node)
        return directive_block("bars", {}, yaml_dump(items))

    # Stack-rows (table of stack bars)
    if name == "div" and "ara-stack-rows" in classes:
        attrs, body = decompile_stack_rows(node)
        return directive_block("stack-rows", attrs, yaml_dump(body))

    # Rank list
    if name == "ol" and "ara-rank-list" in classes:
        items = decompile_rank_list(node)
        return directive_block("rank-list", {}, yaml_dump(items))

    # Compare
    if name == "div" and "ara-compare" in classes:
        items = decompile_compare(node)
        return directive_block("compare", {}, yaml_dump(items))

    # References — by structure (ol with li#ref-N)
    if looks_like_references(node):
        items = decompile_references(node)
        return directive_block("references", {}, yaml_dump(items))

    # Headings
    if name == "h3" and "ara-h2" in classes:
        # Optionally prefixed with <span class="ara-h2-num">N</span>
        num_span = node.find(class_="ara-h2-num")
        if num_span is not None:
            num = _node_text(num_span)
            num_span.extract()
            title = inline_to_md(node).strip()
            return f"## {num}. {title}" if title else f"## {num}."
        title = inline_to_md(node).strip()
        # If the title text already starts with "N. " or "N." pattern, the
        # compiler will normalize it back to the numbered form, but we
        # don't need to do anything special.
        return f"## {title}"
    if name == "h4" and "ara-h3" in classes:
        return f"### {inline_to_md(node).strip()}"
    if name == "h4" and "ara-h4" in classes:
        return f"#### {inline_to_md(node).strip()}"
    if name == "h4":
        # Bare <h4> with no class — treat as #### (the visual default in
        # `.ara-doc` is the muted ara-h4 styling for class-less h4 too).
        return f"#### {inline_to_md(node).strip()}"
    if name == "h3":
        # Bare <h3> — treat as ##.
        return f"## {inline_to_md(node).strip()}"
    if name in ("h2",) and "ara-display" in classes:
        # Should already be in frontmatter; surface a warning if it leaked.
        LOG.warning("stray ara-display heading outside of <header>; skipping")
        return None

    # Divider
    if name == "hr":
        return "---"

    # Paragraph (including invented ara-p)
    if name == "p":
        # Strip the eyebrow/deck/lede that should have been consumed; if
        # they ended up in the body, fall through to plain text rendering.
        if any(c in classes for c in ("ara-eyebrow", "ara-deck", "ara-lede", "ara-display")):
            if node.get("__ara_consumed"):
                return None
        text = inline_to_md(node)
        if not text.strip():
            return None
        return text

    # Code block
    if name == "pre":
        code = node.find("code")
        body = code.get_text() if code else node.get_text()
        return "```\n" + body.rstrip("\n") + "\n```"

    # Lists — ordered/unordered, plain markdown
    if name in ("ul", "ol"):
        # Skip non-references ordered lists that we matched above.
        return _list_to_md(node)

    # Table
    if name == "table" and "ara-table" in classes:
        return decompile_table(node)
    if name == "table" and not classes:
        return decompile_table(node)

    # Plain <div> with no recognized class — descend.
    if name == "div":
        body = _block_children_to_md(node)
        if body.strip():
            return body
        return None

    # <dl> without ara-* class but with dt/dd — treat as kv.
    if name == "dl":
        items = decompile_kv(node)
        if items:
            return directive_block("kv", {}, yaml_dump(items))

    LOG.warning("unrecognized block <%s class=%s>; emitting :::raw passthrough", name, sorted(classes))
    return _raw_directive(node)


def _list_to_md(node: Tag) -> str:
    """Convert <ul>/<ol> to markdown list. Flat only (we don't try to
    detect nested lists — the compiler doesn't either)."""
    ordered = node.name == "ol"
    out_lines = []
    for idx, li in enumerate(node.find_all("li", recursive=False), start=1):
        # If the <li> contains block-level children (e.g. nested <ol>), we
        # flatten into a single line.
        text = inline_to_md(li)
        if not text.strip():
            continue
        prefix = f"{idx}. " if ordered else "- "
        out_lines.append(prefix + text)
    return "\n".join(out_lines)


def _raw_directive(node: Tag) -> str:
    """Final fallback — wrap the unrecognized fragment in :::raw so we
    don't lose data. Markdown body is the rendered HTML; the compiler
    will pass it through unchanged."""
    return directive_block("raw", {}, str(node), body_kind="markdown")


# ----------------------------------------------------------------------
# Directive serializer
# ----------------------------------------------------------------------


def _format_attr(value: Any) -> str:
    """Format a single attribute value for `key=value` inside a directive
    opener. Strings get quoted only if they have ambiguous chars."""
    if value is True:
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    # The compiler's bareword regex stops at whitespace, comma, or `)`,
    # so we quote anything that contains those, plus shell/HTML quotes.
    if not s:
        return '""'
    if re.search(r'[\s,)\'"]', s) or not re.match(r"^[A-Za-z0-9_\-./%$:]+$", s):
        # Quote and escape
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def _format_attrs(attrs: dict) -> str:
    if not attrs:
        return ""
    parts = []
    for k, v in attrs.items():
        if v is True:
            parts.append(k)
        elif v is False or v is None:
            continue
        else:
            parts.append(f"{k}={_format_attr(v)}")
    return ", ".join(parts)


def directive_block(name: str, attrs: dict, body: str, *, body_kind: str = "yaml") -> str:
    """Serialize a `:::name(attrs) body :::` block, indenting/spacing
    consistently so the round-trip diff is minimal."""
    attrs_str = _format_attrs(attrs)
    head = f":::{name}" if not attrs_str else f":::{name}({attrs_str})"
    body = body.rstrip("\n")
    if not body:
        return head + "\n:::"
    return head + "\n" + body + "\n:::"


# ----------------------------------------------------------------------
# Top-level
# ----------------------------------------------------------------------


def decompile(html_text: str) -> str:
    """Convert an `<article class="ara-doc">` fragment to .ara.md text."""
    soup = BeautifulSoup(html_text, "html.parser")
    article = soup.find("article", class_="ara-doc")
    if article is None:
        raise ValueError("no <article class=\"ara-doc\"> in source")

    # Frontmatter
    meta = extract_header(article)

    # Mark frontmatter-source nodes consumed so body walker skips them.
    for cls in ("ara-eyebrow", "ara-display", "ara-deck", "ara-lede"):
        node = article.find(class_=cls)
        if node:
            node["__ara_consumed"] = "1"
    # Mark the <header> wrapper itself consumed (its contents already
    # captured above), but leave its non-frontmatter children (rare) for
    # the body walker.
    header = article.find("header")
    if header is not None and header.parent is article:
        # Walk header's children — eyebrow/display/deck/lede/stats are
        # all consumed. Anything else falls through.
        leftover = []
        for child in list(header.children):
            if isinstance(child, Tag) and not child.get("__ara_consumed"):
                if any(c in _classes(child) for c in ("ara-eyebrow", "ara-display", "ara-deck", "ara-lede")):
                    continue
                # Stats consumed at extract_header time
                if "ara-stats" in _classes(child):
                    continue
                # Strip <p class="ara-eyebrow"> form
                leftover.append(child)
        # If the header has leftover content we don't know how to capture,
        # the body walker will pick it up later — leave it.

    # Body
    body_md = _block_children_to_md(article)

    # Frontmatter serialization — ordered: eyebrow, title, deck, lede, stats
    fm_keys_order = ["eyebrow", "title", "deck", "lede", "stats"]
    fm_ordered = {k: meta[k] for k in fm_keys_order if k in meta}
    for k, v in meta.items():
        if k not in fm_ordered:
            fm_ordered[k] = v

    out = []
    if fm_ordered:
        out.append("---")
        out.append(yaml_dump(fm_ordered))
        out.append("---")
        out.append("")
    out.append(body_md.strip())
    out.append("")  # trailing newline
    return "\n".join(out)


# ----------------------------------------------------------------------
# Verification
# ----------------------------------------------------------------------


def verify_roundtrip(original_html_path: Path, ara_md_text: str) -> tuple[str, str]:
    """Compile the .ara.md back to HTML, run the validator, and return a
    (status, detail) tuple where status is one of:
        OK round-trip          — recompiles & passes validation
        OK validates           — recompiles & passes validation; some drift
        FAIL                   — compile or validation failure
    """
    try:
        # Import lazily so the script can run as a pure decompiler when
        # the compiler isn't on the path.
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        from compile_ara import compile_source, AraSyntaxError  # type: ignore
        from write_generative_research import validate_body  # type: ignore
    except Exception as e:  # pragma: no cover
        return "FAIL", f"compiler import failed: {e}"

    try:
        recompiled = compile_source(ara_md_text)
    except AraSyntaxError as e:
        return "FAIL", f"DSL compile failed: {e}"
    except Exception as e:
        return "FAIL", f"DSL compile crashed: {e}"

    try:
        validate_body(recompiled, "fragment")
    except ValueError as e:
        # Trim very long error messages
        msg = str(e)
        if len(msg) > 400:
            msg = msg[:400] + "..."
        return "FAIL", f"validator rejected: {msg}"

    # Compare sizes as a rough indicator of round-trip fidelity.
    original = original_html_path.read_text(encoding="utf-8")
    orig_len = len(re.sub(r"\s+", " ", original))
    new_len = len(re.sub(r"\s+", " ", recompiled))
    drift_pct = abs(new_len - orig_len) / max(orig_len, 1) * 100
    if drift_pct < 5:
        return "OK round-trip", f"{drift_pct:.1f}% size drift"
    return "OK validates", f"{drift_pct:.1f}% size drift (content drift expected)"


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------


def cli(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", nargs="?", help="path to .html article")
    p.add_argument("-o", "--out", help="output path (default: stdout)")
    p.add_argument("--in-place", action="store_true", help="write to <source>.ara.md")
    p.add_argument("--all", action="store_true", help="walk research/generative/*.html")
    p.add_argument("--verify", action="store_true", help="also recompile + validate each output")
    p.add_argument("-v", "--verbose", action="store_true", help="INFO logging")
    args = p.parse_args(argv)

    logging.basicConfig(
        format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO if args.verbose else logging.WARNING,
        stream=sys.stderr,
    )

    if args.all:
        files = sorted(GEN_DIR.glob("*.html"))
        results: list[tuple[Path, str, str]] = []
        for f in files:
            try:
                html_text = f.read_text(encoding="utf-8")
                LOG.info("decompiling %s", f.name)
                # File-scoped logger to attach the filename to warnings.
                file_logger = logging.LoggerAdapter(LOG, {"file": f.name})
                ara_md = decompile(html_text)
                out_path = f.with_suffix(".ara.md")
                out_path.write_text(ara_md, encoding="utf-8")
                status, detail = ("OK", "decompiled")
                if args.verify:
                    status, detail = verify_roundtrip(f, ara_md)
                results.append((f, status, detail))
            except Exception as e:
                results.append((f, "FAIL", f"decompile crashed: {e}"))
                LOG.exception("decompile failed for %s", f)
        # Summary
        print("\nRound-trip summary:")
        print("=" * 80)
        for f, status, detail in results:
            print(f"  {status:18s} {f.name:60s} {detail}")
        ok_count = sum(1 for _, s, _ in results if s.startswith("OK"))
        print(f"\n{ok_count}/{len(results)} files succeeded")
        return 0 if ok_count == len(results) else 1

    if not args.source:
        p.print_help(sys.stderr)
        return 2

    src = Path(args.source)
    html_text = src.read_text(encoding="utf-8")
    ara_md = decompile(html_text)

    if args.in_place:
        out_path = src.with_suffix(".ara.md")
        out_path.write_text(ara_md, encoding="utf-8")
        print(str(out_path))
    elif args.out:
        Path(args.out).write_text(ara_md, encoding="utf-8")
        print(args.out)
    else:
        sys.stdout.write(ara_md)

    if args.verify:
        status, detail = verify_roundtrip(src, ara_md)
        print(f"\n{status}: {detail}", file=sys.stderr)
        return 0 if status.startswith("OK") else 1
    return 0


if __name__ == "__main__":
    sys.exit(cli())
