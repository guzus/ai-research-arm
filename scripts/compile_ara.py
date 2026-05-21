#!/usr/bin/env python3
"""Compile an .ara.md source file into a validated HTML fragment.

The DSL is markdown plus YAML frontmatter plus `:::block(...)` directives
that map 1:1 to the `ara-*` component vocabulary documented in
COMPONENTS.md. The agent writes in this DSL; the compiler is the only
thing allowed to emit raw HTML, so invented classes and tag mistakes
become unrepresentable at the source level.

Pipeline:

    .ara.md  ->  compile_ara.compile_source(text)  ->  <article> fragment
                                                       (then runs through
                                                        validate_body in
                                                        write_generative_research.py
                                                        as a backstop)

The grammar:

    --- YAML frontmatter ---     -> <header> with eyebrow / display / deck / lede
    --- end ---

    ## 01. Section title          -> <h3 class="ara-h2"><span class="ara-h2-num">01</span>...
    ### Sub heading               -> <h4 class="ara-h3">
    paragraph text                -> <p>
    > blockquote                  -> <blockquote class="ara-quote">
    ---                           -> <hr class="ara-divider">
    1. item                       -> <ol> / <li>
    - item                        -> <ul> / <li>
    | a | b |                     -> <table class="ara-table">

    :::block(attr=val) ... :::    -> the matching ara-* component
    {accent}text{/}, [^N], ==m==  -> inline ara primitives

Run standalone:

    uv run python scripts/compile_ara.py path/to/source.ara.md
    uv run python scripts/compile_ara.py - < source.ara.md
"""

from __future__ import annotations

import argparse
import ast
import html
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

import yaml

# ----------------------------------------------------------------------
# Frontmatter
# ----------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(source: str) -> tuple[dict, str]:
    """Pull `--- yaml --- \n body` off the top. Frontmatter optional."""
    m = FRONTMATTER_RE.match(source)
    if not m:
        return {}, source
    raw = m.group(1)
    try:
        meta = yaml.safe_load(raw) or {}
    except yaml.YAMLError as e:
        raise AraSyntaxError(f"invalid YAML in frontmatter: {e}") from e
    if not isinstance(meta, dict):
        raise AraSyntaxError("frontmatter must be a YAML mapping (key: value)")
    body = source[m.end():]
    return meta, body


# ----------------------------------------------------------------------
# Errors
# ----------------------------------------------------------------------


class AraSyntaxError(ValueError):
    """Raised for any compile error. Carries an optional line number."""

    def __init__(self, message: str, line: int | None = None):
        if line is not None:
            super().__init__(f"line {line}: {message}")
        else:
            super().__init__(message)
        self.line = line


# ----------------------------------------------------------------------
# Attribute parsing for :::block(key=value, key2="quoted")
# ----------------------------------------------------------------------

# Match key=value pairs. Values can be:
#   - "quoted string with spaces"
#   - bareword: alphanumerics + - . % $ / : (URL-safe-ish set)
#   - [list, of, barewords]
#   - bare key (treated as true)
ATTR_PAIR_RE = re.compile(
    r"""
    \s*
    ([a-zA-Z_][a-zA-Z0-9_-]*)              # key
    (?:
        \s*=\s*
        (
            "(?:[^"\\]|\\.)*"               # double-quoted
            | '(?:[^'\\]|\\.)*'             # single-quoted
            | \[[^\]]*\]                    # [bracketed list]
            | [^\s,)]+                      # bareword
        )
    )?
    \s*(?:,|$)
    """,
    re.VERBOSE,
)


def parse_attrs(text: str) -> dict[str, Any]:
    """Parse the `key=value, key2="quoted"` payload of a `:::name(...)`."""
    if not text or not text.strip():
        return {}
    attrs: dict[str, Any] = {}
    pos = 0
    while pos < len(text):
        m = ATTR_PAIR_RE.match(text, pos)
        if not m or m.end() == pos:
            raise AraSyntaxError(f"can't parse attributes at {text[pos:pos+30]!r}")
        key, raw_val = m.group(1), m.group(2)
        if raw_val is None:
            attrs[key] = True
        elif raw_val.startswith('"') or raw_val.startswith("'"):
            try:
                attrs[key] = ast.literal_eval(raw_val)
            except (SyntaxError, ValueError) as e:
                raise AraSyntaxError(f"can't parse quoted attribute {key!r}") from e
        elif raw_val.startswith("["):
            inner = raw_val[1:-1].strip()
            if not inner:
                attrs[key] = []
            else:
                attrs[key] = [_coerce_scalar(p.strip()) for p in inner.split(",")]
        else:
            attrs[key] = _coerce_scalar(raw_val)
        pos = m.end()
    return attrs


def _coerce_scalar(raw: str) -> Any:
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False
    try:
        if "." in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        return raw


# ----------------------------------------------------------------------
# Inline syntax
# ----------------------------------------------------------------------

# {accent}text{/}, {tag}cdn{/}, {mark}text{/}
INLINE_WRAP_RE = re.compile(r"\{(accent|tag|mark)\}(.*?)\{/\}", re.DOTALL)
# {sparkline:5.2,5.4,5.5}, {flag:green}, {flag-red}
INLINE_SELF_RE = re.compile(r"\{(sparkline|flag|h2num):([^}]+)\}")
# Cite refs: [^1], [^1,2,3]
CITE_RE = re.compile(r"\[\^([0-9]+(?:,\s*[0-9]+)*)\]")
# Highlight: ==text==
MARK_RE = re.compile(r"==([^=].*?)==", re.DOTALL)
# Strong: **text**
STRONG_RE = re.compile(r"\*\*(\S.*?\S|\S)\*\*", re.DOTALL)
# Emphasis: *text*  (single underscore is too noisy; underscore not used)
EM_RE = re.compile(r"(?<![\w*])\*([^\s*][^*\n]*?)\*(?!\w)")
# Inline code: `code`
CODE_RE = re.compile(r"`([^`\n]+)`")
# Links: [text](url) — url is %-encoded URL chars only
LINK_RE = re.compile(r"\[([^\]\n]+)\]\(((?:https?://|/)[^\s)]+)\)")

# Sentinel marker used to temporarily mask code/link spans so wrapping
# regexes don't reach inside them. Format chosen to avoid collisions.
PLACEHOLDER = "\x00ARA{}{}\x00"


def parse_inline(text: str) -> str:
    """Markdown-ish inline to HTML. The order matters: we mask code and
    links first so wrapping regexes (bold, italic, mark) can't reach
    inside them, then we unmask after the wrappers have run."""
    masks: list[str] = []

    def _mask(html_str: str) -> str:
        token = PLACEHOLDER.format(len(masks), 0)
        masks.append(html_str)
        return token

    def _on_code(m):
        return _mask(f"<code>{html.escape(m.group(1))}</code>")

    def _on_link(m):
        label = parse_inline(m.group(1))
        href = html.escape(m.group(2), quote=True)
        return _mask(f'<a href="{href}">{label}</a>')

    def _on_cite(m):
        ids = [n.strip() for n in m.group(1).split(",")]
        return _mask(
            "".join(
                f'<sup><a class="ara-cite" href="#ref-{n}">{n}</a></sup>'
                for n in ids
            )
        )

    def _on_self(m):
        kind, payload = m.group(1), m.group(2).strip()
        if kind == "sparkline":
            pts = ",".join(_csv_numbers(payload, "sparkline", None))
            return _mask(f'<span class="ara-sparkline" data-points="{html.escape(pts, quote=True)}"></span>')
        if kind == "flag":
            variant = payload.strip().lower()
            if variant not in ("green", "yellow", "red"):
                raise AraSyntaxError(f"flag color must be green|yellow|red, got {variant!r}")
            return _mask(f'<span class="ara-flag ara-flag--{variant}"></span>')
        if kind == "h2num":
            return _mask(f'<span class="ara-h2-num">{html.escape(payload)}</span>')
        raise AraSyntaxError(f"unknown inline directive {kind!r}")

    def _on_wrap(m):
        kind = m.group(1)
        raw_body = m.group(2)
        body = raw_body if "\x00" in raw_body else parse_inline(raw_body)
        if kind == "accent":
            return _mask(f'<strong class="ara-accent">{body}</strong>')
        if kind == "tag":
            return _mask(f'<span class="ara-tag">{body}</span>')
        if kind == "mark":
            return _mask(f'<mark class="ara-mark">{body}</mark>')
        raise AraSyntaxError(f"unknown wrap directive {kind!r}")

    # Mask high-precedence atoms first. Every emitter that produces HTML
    # must mask its output — otherwise the bare-text escape pass below
    # will turn <strong> into &lt;strong&gt;.
    text = CODE_RE.sub(_on_code, text)
    text = LINK_RE.sub(_on_link, text)
    text = CITE_RE.sub(_on_cite, text)
    text = INLINE_SELF_RE.sub(_on_self, text)
    text = INLINE_WRAP_RE.sub(_on_wrap, text)

    # Wrap directives. Only recurse into parse_inline when the matched
    # inner text contains NO placeholders — recursing on text that
    # already has \x00ARA…\x00 markers would have the inner call try
    # to resolve them against its own (empty) masks list and crash.
    # When placeholders are present we emit the wrapper around the
    # masked inner text directly and let the final unmask phase resolve
    # them in the outer scope.
    def _wrap(html_tag_open: str, html_tag_close: str):
        def _sub(m: re.Match) -> str:
            inner = m.group(1)
            if "\x00" in inner:
                return _mask(f"{html_tag_open}{inner}{html_tag_close}")
            return _mask(f"{html_tag_open}{parse_inline(inner)}{html_tag_close}")
        return _sub

    text = MARK_RE.sub(_wrap('<mark class="ara-mark">', "</mark>"), text)
    text = STRONG_RE.sub(_wrap("<strong>", "</strong>"), text)
    text = EM_RE.sub(_wrap("<em>", "</em>"), text)

    # Escape any remaining bare text (the masked placeholders are
    # ASCII-NUL flanked, so they survive html.escape).
    parts = text.split("\x00")
    for i, chunk in enumerate(parts):
        if not chunk.startswith("ARA"):
            parts[i] = html.escape(chunk, quote=False)
    text = "\x00".join(parts)

    # Iterative unmask. Masks may contain other placeholders (a wrap
    # built around already-masked content), so loop until the text
    # stabilizes.
    def _unmask(m: re.Match) -> str:
        return masks[int(m.group(1))]

    prev: str | None = None
    while prev != text:
        prev = text
        text = re.sub(r"\x00ARA(\d+)0\x00", _unmask, text)
    return text


# ----------------------------------------------------------------------
# Block parsing
# ----------------------------------------------------------------------

_DIRECTIVE_NAME_RE = re.compile(r"^:::([a-z][a-z0-9-]*)")
DIRECTIVE_CLOSE_RE = re.compile(r"^:::\s*$")


def parse_directive_open(line: str) -> tuple[str, str] | None:
    """Return (name, attrs_str) if `line` opens a directive, else None.
    Uses a quote-aware paren walker so quoted attribute values can
    contain commas and parens (e.g. `title="(Yahoo Finance) chart"`)
    without breaking the parse."""
    rest = line.rstrip()
    if not rest.startswith(":::") or DIRECTIVE_CLOSE_RE.match(rest):
        return None
    m = _DIRECTIVE_NAME_RE.match(rest)
    if not m:
        return None
    name = m.group(1)
    tail = rest[m.end():]
    if not tail:
        return (name, "")
    if tail[0] != "(":
        return None
    depth = 1
    i = 1
    in_quote: str | None = None
    while i < len(tail):
        c = tail[i]
        if in_quote:
            if c == "\\" and i + 1 < len(tail):
                i += 2
                continue
            if c == in_quote:
                in_quote = None
            i += 1
            continue
        if c in ('"', "'"):
            in_quote = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                attrs_str = tail[1:i]
                trailing = tail[i + 1:].strip()
                if trailing != "":
                    return None
                return (name, attrs_str)
        i += 1
    return None
HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$")
TABLE_ROW_RE = re.compile(r"^\|.*\|\s*$")
TABLE_DIVIDER_RE = re.compile(r"^\|\s*:?-{2,}.*\|\s*$")
LIST_ITEM_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.+?)\s*$")
BLOCKQUOTE_RE = re.compile(r"^>\s?(.*?)\s*$")
HR_RE = re.compile(r"^-{3,}\s*$")
CODE_FENCE_RE = re.compile(r"^```\s*([a-zA-Z0-9_-]*)\s*$")


def split_blocks(body: str) -> list[tuple[int, str, list[str]]]:
    """Walk the body line by line and return a list of
    (start_line, kind, raw_lines) tuples where kind is one of:
        directive, heading, paragraph, blockquote, list, table,
        hr, code, blank
    The block walker is dumb on purpose — emitters do the real work."""
    lines = body.splitlines()
    blocks: list[tuple[int, str, list[str]]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Blank — coalesce so the emitters can use them as separators.
        if not line.strip():
            i += 1
            continue
        if HR_RE.match(line):
            blocks.append((i + 1, "hr", [line]))
            i += 1
            continue
        # Directive: collect until matching ::: at indent 0.
        m = parse_directive_open(line)
        if m:
            name, _ = m
            start_line = i + 1
            buf = [line]
            depth = 1
            i += 1
            while i < len(lines):
                inner = lines[i]
                if parse_directive_open(inner):
                    depth += 1
                elif DIRECTIVE_CLOSE_RE.match(inner):
                    depth -= 1
                buf.append(inner)
                i += 1
                if depth == 0:
                    break
            else:
                raise AraSyntaxError(
                    f"unterminated :::{name} block (no matching :::)",
                    line=start_line,
                )
            blocks.append((start_line, "directive", buf))
            continue
        if line.startswith(":::"):
            if DIRECTIVE_CLOSE_RE.match(line):
                raise AraSyntaxError("stray directive close without matching opener", line=i + 1)
            raise AraSyntaxError(f"invalid directive opener: {line!r}", line=i + 1)
        # Heading
        if HEADING_RE.match(line):
            blocks.append((i + 1, "heading", [line]))
            i += 1
            continue
        # Fenced code
        if CODE_FENCE_RE.match(line):
            start_line = i + 1
            buf = [line]
            i += 1
            while i < len(lines) and not CODE_FENCE_RE.match(lines[i]):
                buf.append(lines[i])
                i += 1
            if i < len(lines):
                buf.append(lines[i])
                i += 1
            blocks.append((start_line, "code", buf))
            continue
        # Table
        if TABLE_ROW_RE.match(line):
            start_line = i + 1
            buf = [line]
            i += 1
            while i < len(lines) and TABLE_ROW_RE.match(lines[i]):
                buf.append(lines[i])
                i += 1
            blocks.append((start_line, "table", buf))
            continue
        # Blockquote
        if BLOCKQUOTE_RE.match(line):
            start_line = i + 1
            buf = [line]
            i += 1
            while i < len(lines) and BLOCKQUOTE_RE.match(lines[i]):
                buf.append(lines[i])
                i += 1
            blocks.append((start_line, "blockquote", buf))
            continue
        # List
        if LIST_ITEM_RE.match(line):
            start_line = i + 1
            buf = [line]
            i += 1
            while i < len(lines) and (
                LIST_ITEM_RE.match(lines[i])
                or (lines[i].startswith("  ") and lines[i].strip())
            ):
                buf.append(lines[i])
                i += 1
            blocks.append((start_line, "list", buf))
            continue
        # Paragraph — keep accumulating until blank, heading, directive,
        # list item, blockquote, hr, table, code fence.
        start_line = i + 1
        buf = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if not nxt.strip():
                break
            if (
                parse_directive_open(nxt)
                or DIRECTIVE_CLOSE_RE.match(nxt)
                or HEADING_RE.match(nxt)
                or HR_RE.match(nxt)
                or LIST_ITEM_RE.match(nxt)
                or BLOCKQUOTE_RE.match(nxt)
                or TABLE_ROW_RE.match(nxt)
                or CODE_FENCE_RE.match(nxt)
            ):
                break
            buf.append(nxt)
            i += 1
        blocks.append((start_line, "paragraph", buf))
    return blocks


# ----------------------------------------------------------------------
# Markdown block emitters
# ----------------------------------------------------------------------


def emit_heading(line: str) -> str:
    """## N. Title  -> <h3 class="ara-h2"><span class="ara-h2-num">N</span>Title</h3>
    ## Title       -> <h3 class="ara-h2">Title</h3>
    ### Title      -> <h4 class="ara-h3">Title</h4>
    #### Title     -> <h4 class="ara-h4">Title</h4>"""
    m = HEADING_RE.match(line)
    if not m:
        raise AraSyntaxError(f"not a heading: {line!r}")
    level = len(m.group(1))
    raw = m.group(2)
    if level == 2:
        # Try to extract a leading number prefix: "01. Title", "1 — Title", etc.
        prefix_m = re.match(r"^(\d{1,2})\s*[.\-—–:]?\s+(.+)$", raw)
        if prefix_m:
            num, rest = prefix_m.group(1), prefix_m.group(2)
            return (
                f'<h3 class="ara-h2"><span class="ara-h2-num">{html.escape(num)}</span>'
                f'{parse_inline(rest)}</h3>'
            )
        return f'<h3 class="ara-h2">{parse_inline(raw)}</h3>'
    if level == 3:
        return f'<h4 class="ara-h3">{parse_inline(raw)}</h4>'
    if level == 4:
        return f'<h4 class="ara-h4">{parse_inline(raw)}</h4>'
    raise AraSyntaxError(f"unsupported heading level {level} (use ## / ### / ####)")


def emit_paragraph(lines: list[str]) -> str:
    text = " ".join(l.strip() for l in lines)
    return f"<p>{parse_inline(text)}</p>"


def emit_blockquote(lines: list[str]) -> str:
    """A blockquote becomes <blockquote class="ara-quote">. If the last
    non-blank line is `— Attribution`, lift it into <span class="ara-quote-attr">."""
    stripped = []
    attr = None
    for l in lines:
        m = BLOCKQUOTE_RE.match(l)
        stripped.append(m.group(1) if m else l)
    if stripped and re.match(r"^\s*[—–-]\s*\S", stripped[-1]):
        attr = re.sub(r"^\s*[—–-]\s*", "", stripped[-1])
        stripped = stripped[:-1]
    body = parse_inline(" ".join(s.strip() for s in stripped if s.strip()))
    out = f'<blockquote class="ara-quote"><p>{body}</p>'
    if attr:
        out += f'<span class="ara-quote-attr">{parse_inline(attr)}</span>'
    out += "</blockquote>"
    return out


def emit_hr(_lines: list[str]) -> str:
    return '<hr class="ara-divider">'


def emit_code_fence(lines: list[str]) -> str:
    body = "\n".join(lines[1:-1] if (len(lines) >= 2 and CODE_FENCE_RE.match(lines[-1])) else lines[1:])
    return f"<pre><code>{html.escape(body)}</code></pre>"


def emit_list(lines: list[str]) -> str:
    """Flat list (no nesting in v1). Detects ul vs ol by first marker."""
    first = LIST_ITEM_RE.match(lines[0])
    if not first:
        raise AraSyntaxError(f"list block didn't start with a list item: {lines[0]!r}")
    ordered = first.group(2)[0].isdigit()
    tag = "ol" if ordered else "ul"
    items = []
    buf: list[str] = []
    for l in lines:
        m = LIST_ITEM_RE.match(l)
        if m:
            if buf:
                items.append(buf)
            buf = [m.group(3)]
        else:
            buf.append(l.strip())
    if buf:
        items.append(buf)
    body = "".join(f"<li>{parse_inline(' '.join(it))}</li>" for it in items)
    return f"<{tag}>{body}</{tag}>"


def emit_table(lines: list[str]) -> str:
    """Markdown table -> <table class="ara-table">. First row is header,
    second row is the divider, rest is body. A row marked with a leading
    `*` cell becomes <tr class="ara-row-highlight">."""
    rows = [_split_row(l) for l in lines]
    if len(rows) < 2:
        raise AraSyntaxError("table needs at least a header row and a divider row")
    if not all(re.match(r"^\s*:?-{2,}:?\s*$", c) for c in rows[1]):
        raise AraSyntaxError("table's second row must be the |---|---| divider")
    head = rows[0]
    body = rows[2:]
    out = ['<table class="ara-table"><thead><tr>']
    for c in head:
        out.append(f"<th>{parse_inline(c)}</th>")
    out.append("</tr></thead><tbody>")
    for row in body:
        highlight = False
        if row and row[0].startswith("*"):
            row = [row[0][1:].lstrip()] + row[1:]
            highlight = True
        tr_attr = ' class="ara-row-highlight"' if highlight else ""
        out.append(f"<tr{tr_attr}>")
        for c in row:
            out.append(f"<td>{parse_inline(c)}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def _split_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [c.strip() for c in stripped.split("|")]


# ----------------------------------------------------------------------
# Directive emitters
# ----------------------------------------------------------------------


def _yaml_body(buf: list[str], line_no: int) -> Any:
    """Strip the ``:::name(...)`` and trailing ``:::``, parse the middle as YAML."""
    inner = "\n".join(buf[1:-1])
    try:
        return yaml.safe_load(inner) if inner.strip() else None
    except yaml.YAMLError as e:
        raise AraSyntaxError(f"invalid YAML body: {e}", line=line_no) from e


def _markdown_body(buf: list[str]) -> str:
    """Strip wrapper lines and return the inner markdown as a string."""
    return "\n".join(buf[1:-1])


def _opt(d: dict, key: str, default=None):
    return d.get(key, default) if isinstance(d, dict) else default


def _req(d: dict, key: str, ctx: str, line_no: int):
    if not isinstance(d, dict) or key not in d:
        raise AraSyntaxError(f"{ctx}: missing required field {key!r}", line=line_no)
    return d[key]


REMOTE_SVG_RE = re.compile(r"\.svgz?$", re.IGNORECASE)


def _has_unsafe_url_chars(value: str) -> bool:
    return any(ord(ch) < 32 for ch in value) or any(ch in value for ch in "<>\\")


def is_safe_http_url(value: str) -> bool:
    raw = value.strip()
    if not raw or _has_unsafe_url_chars(raw):
        return False
    parsed = urlparse(raw)
    return (
        parsed.scheme in ("http", "https")
        and bool(parsed.netloc)
        and not parsed.username
        and not parsed.password
    )


def is_safe_image_src(value: str) -> bool:
    raw = value.strip()
    if not raw or _has_unsafe_url_chars(raw):
        return False
    if raw.startswith("/") and not raw.startswith("//"):
        return True
    if not is_safe_http_url(raw):
        return False
    parsed = urlparse(raw)
    return not REMOTE_SVG_RE.search(parsed.path)


def require_safe_image_src(value: Any, ctx: str, line_no: int) -> str:
    src = str(value).strip()
    if not is_safe_image_src(src):
        raise AraSyntaxError(
            f"{ctx}: src must be an http(s) image URL or absolute local path; remote SVG is not allowed",
            line=line_no,
        )
    return src


def optional_safe_source_url(value: Any, ctx: str, line_no: int) -> str | None:
    if value is None:
        return None
    url = str(value).strip()
    if not is_safe_http_url(url):
        raise AraSyntaxError(f"{ctx}: source-url must be an http(s) URL", line=line_no)
    return url


def _as_finite_number(value: Any, ctx: str, line_no: int | None) -> float:
    try:
        n = float(str(value).strip())
    except (TypeError, ValueError) as e:
        raise AraSyntaxError(f"{ctx}: expected a number, got {value!r}", line=line_no) from e
    if not math.isfinite(n):
        raise AraSyntaxError(f"{ctx}: expected a finite number, got {value!r}", line=line_no)
    return n


def _format_number(n: float) -> str:
    return str(int(n)) if n.is_integer() else f"{n:g}"


def _number_text(value: Any, ctx: str, line_no: int | None) -> str:
    return _format_number(_as_finite_number(value, ctx, line_no))


def _pct_text(value: Any, ctx: str, line_no: int | None) -> str:
    n = _as_finite_number(value, ctx, line_no)
    if n < 0 or n > 100:
        raise AraSyntaxError(f"{ctx}: pct must be between 0 and 100, got {value!r}", line=line_no)
    return _format_number(n)


def _int_range_text(value: Any, ctx: str, line_no: int | None, lo: int, hi: int) -> str:
    n = _as_finite_number(value, ctx, line_no)
    if not n.is_integer() or n < lo or n > hi:
        raise AraSyntaxError(f"{ctx}: expected an integer from {lo} to {hi}, got {value!r}", line=line_no)
    return str(int(n))


def _csv_values(text: str) -> list[str]:
    return [part.strip() for part in text.split(",") if part.strip()]


def _csv_numbers(text: str, ctx: str, line_no: int | None) -> list[str]:
    vals = _csv_values(text)
    if not vals:
        raise AraSyntaxError(f"{ctx}: needs at least one number", line=line_no)
    return [_number_text(v, ctx, line_no) for v in vals]


def _attr(name: str, value: Any) -> str:
    if value is True:
        return f' {name}'
    if value is False or value is None or value == "":
        return ""
    return f' {name}="{html.escape(str(value), quote=True)}"'


def emit_stats(attrs: dict, body: Any, line_no: int) -> str:
    if not isinstance(body, list):
        raise AraSyntaxError(":::stats body must be a YAML list of {label, value, ...}", line=line_no)
    out = ['<div class="ara-stats">']
    for item in body:
        if not isinstance(item, dict):
            raise AraSyntaxError(":::stats items must be mappings", line=line_no)
        label = _req(item, "label", "stats item", line_no)
        value = _req(item, "value", "stats item", line_no)
        unit = _opt(item, "unit")
        note = _opt(item, "note")
        out.append('<div class="ara-stat">')
        out.append(f'<span class="ara-stat-label">{parse_inline(str(label))}</span>')
        if unit is not None and str(unit).strip():
            out.append(
                f'<div class="ara-stat-value">{parse_inline(str(value))}'
                f'<span class="ara-stat-unit">{parse_inline(str(unit))}</span></div>'
            )
        else:
            out.append(f'<div class="ara-stat-value">{parse_inline(str(value))}</div>')
        if note is not None and str(note).strip():
            out.append(f'<div class="ara-stat-note">{parse_inline(str(note))}</div>')
        out.append('</div>')
    out.append('</div>')
    return "".join(out)


def emit_kv(attrs: dict, body: Any, line_no: int) -> str:
    if not isinstance(body, list):
        raise AraSyntaxError(":::kv body must be a YAML list of {term, def}", line=line_no)
    out = ['<dl class="ara-kv">']
    for item in body:
        term = _req(item, "term", "kv item", line_no)
        defn = _req(item, "def", "kv item", line_no)
        out.append(f"<dt>{parse_inline(str(term))}</dt>")
        out.append(f"<dd>{parse_inline(str(defn))}</dd>")
    out.append("</dl>")
    return "".join(out)


def emit_callout(attrs: dict, body: str, line_no: int) -> str:
    kind = _opt(attrs, "kind", "info")
    if kind not in ("info", "success", "warn", "danger"):
        raise AraSyntaxError(
            f"callout kind must be info|success|warn|danger, got {kind!r}",
            line=line_no,
        )
    label = _opt(attrs, "label")
    inner = compile_blocks(split_blocks(body))
    out = [f'<div class="ara-callout ara-callout--{kind}">']
    if label:
        out.append(f'<span class="ara-callout-label">{parse_inline(str(label))}</span>')
    out.append(inner)
    out.append("</div>")
    return "".join(out)


def emit_quote(attrs: dict, body: str, line_no: int) -> str:
    attr = _opt(attrs, "attr") or _opt(attrs, "by")
    inner = compile_blocks(split_blocks(body))
    out = ['<blockquote class="ara-quote">', inner]
    if attr:
        out.append(f'<span class="ara-quote-attr">{parse_inline(str(attr))}</span>')
    out.append("</blockquote>")
    return "".join(out)


def emit_figure(attrs: dict, body: str, line_no: int) -> str:
    src = require_safe_image_src(_req(attrs, "src", "figure", line_no), "figure", line_no)
    alt = _opt(attrs, "alt", "")
    caption = _opt(attrs, "caption")
    credit = _opt(attrs, "credit") or _opt(attrs, "source")
    source_url = optional_safe_source_url(
        _opt(attrs, "source-url", _opt(attrs, "source_url")),
        "figure",
        line_no,
    )
    variant = _opt(attrs, "variant")
    classes = ["ara-figure"]
    if variant:
        variant = str(variant).strip()
        if variant not in ("wide", "inline", "bleed"):
            raise AraSyntaxError(
                f"figure: variant must be wide|inline|bleed, got {variant!r}",
                line=line_no,
            )
        classes.append(f"ara-figure--{variant}")
    out = [
        f'<figure class="{" ".join(classes)}">',
        (
            f'<img src="{html.escape(src, quote=True)}" '
            f'alt="{html.escape(str(alt), quote=True)}" '
            'loading="lazy" decoding="async" referrerpolicy="no-referrer">'
        ),
    ]
    if caption or credit or source_url:
        out.append('<figcaption class="ara-caption">')
        if caption:
            out.append(f'<span class="ara-caption-text">{parse_inline(str(caption))}</span>')
        if credit or source_url:
            label = parse_inline(str(credit)) if credit else "Source"
            if source_url:
                label = f'<a href="{html.escape(source_url, quote=True)}">{label}</a>'
            out.append(f'<span class="ara-credit">Source: {label}</span>')
        out.append("</figcaption>")
    out.append("</figure>")
    return "".join(out)


def emit_line_chart(attrs: dict, body: str, line_no: int) -> str:
    """Body lines:
        x: 2025-06,2025-07,...
        BE: 23.92,37.39,...
        NVDA: 100,105,110,...
    First non-`x:` row becomes series-1, second becomes series-2, etc."""
    x_labels: list[str] | None = None
    series: list[tuple[str, list[str]]] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise AraSyntaxError(
                f":::line-chart body line must be `LABEL: comma,nums`: {line!r}",
                line=line_no,
            )
        label, vals = line.split(":", 1)
        label = label.strip()
        if label.lower() == "x":
            x_labels = _csv_values(vals)
        else:
            series.append((label, _csv_numbers(vals, f"line-chart series {label!r}", line_no)))
    if x_labels is None:
        raise AraSyntaxError(":::line-chart body needs an `x:` row of labels", line=line_no)
    if not x_labels:
        raise AraSyntaxError(":::line-chart `x:` row needs at least one label", line=line_no)
    if not series or len(series) > 4:
        raise AraSyntaxError(
            f":::line-chart needs 1-4 data series, got {len(series)}",
            line=line_no,
        )
    for label, vals in series:
        if len(vals) != len(x_labels):
            raise AraSyntaxError(
                f"line-chart series {label!r} has {len(vals)} values but x has {len(x_labels)} labels",
                line=line_no,
            )
    parts = ['<div class="ara-line-chart"']
    parts.append(_attr("data-x-labels", ",".join(x_labels)))
    for idx, (label, vals) in enumerate(series, start=1):
        parts.append(_attr(f"data-series-{idx}", ",".join(vals)))
        parts.append(_attr(f"data-series-{idx}-label", label))
    for key in ("title", "subtitle", "y-unit"):
        if attrs.get(key) is not None:
            parts.append(_attr(f"data-{key}", attrs[key]))
    parts.append("></div>")
    return "".join(parts)


# TradingView symbols are EXCHANGE:TICKER (e.g. NASDAQ:NOW, NYSE:BE,
# BINANCE:BTCUSDT, FX:EURUSD). The strict charset keeps the value safe to
# interpolate into both the dashboard widget config and the fallback URL.
# \Z (not $) so a trailing newline can't sneak past — keeps this gate
# byte-identical to the writer's mirror in write_generative_research.py.
_TV_SYMBOL_RE = re.compile(r"^[A-Za-z0-9:._-]{1,32}\Z")
# interval/range are passed through to the third-party widget. We charset-gate
# them (rather than enumerate accepted values) so a genuinely valid TradingView
# value is never rejected — the widget ignores anything it doesn't recognise,
# and the fallback link works regardless.
_TV_INTERVAL_RE = re.compile(r"^[A-Za-z0-9]{1,5}\Z")
_TV_RANGE_RE = re.compile(r"^[A-Za-z0-9]{1,4}\Z")


def emit_tradingview(attrs: dict, body: str, line_no: int) -> str:
    """`:::tradingview(symbol="NASDAQ:NOW", interval=D, theme=dark, range=12M)`

    Emits a script-free placeholder div carrying the config in data-* attrs.
    The validator can't allow <script>/<iframe>, so the dashboard's
    renderTradingView enhancer injects the real TradingView Advanced Chart
    widget at view time. Outside the dashboard (the static .html artifact, a
    PDF) only the fallback <a> renders. `symbol` is required; the rest fall
    back to renderer defaults when omitted."""
    symbol = str(_req(attrs, "symbol", "tradingview", line_no)).strip()
    if not _TV_SYMBOL_RE.match(symbol):
        raise AraSyntaxError(
            "tradingview: symbol must be EXCHANGE:TICKER using [A-Za-z0-9:._-] "
            f"(e.g. NASDAQ:NOW), got {symbol!r}",
            line=line_no,
        )
    interval = _opt(attrs, "interval")
    if interval is not None:
        interval = str(interval).strip()
        if not _TV_INTERVAL_RE.match(interval):
            raise AraSyntaxError(
                f"tradingview: interval must be alphanumeric (e.g. D, W, M, 60), got {interval!r}",
                line=line_no,
            )
    rng = _opt(attrs, "range")
    if rng is not None:
        rng = str(rng).strip()
        if not _TV_RANGE_RE.match(rng):
            raise AraSyntaxError(
                f"tradingview: range must be alphanumeric (e.g. 12M, YTD, 5Y), got {rng!r}",
                line=line_no,
            )
    theme = _opt(attrs, "theme")
    if theme is not None:
        theme = str(theme).strip()
        if theme not in ("dark", "light"):
            raise AraSyntaxError(
                f"tradingview: theme must be dark|light, got {theme!r}",
                line=line_no,
            )
    # TradingView symbol pages live at /symbols/EXCHANGE-TICKER/.
    href = f"https://www.tradingview.com/symbols/{symbol.replace(':', '-')}/"
    parts = ['<div class="ara-tradingview"']
    parts.append(_attr("data-symbol", symbol))
    parts.append(_attr("data-interval", interval))
    parts.append(_attr("data-theme", theme))
    parts.append(_attr("data-range", rng))
    parts.append(">")
    parts.append(
        f'<a class="ara-tradingview-fallback" href="{html.escape(href, quote=True)}">'
        f"View {html.escape(symbol)} on TradingView ↗</a>"
    )
    parts.append("</div>")
    return "".join(parts)


def emit_bar_chart(attrs: dict, body: str, line_no: int) -> str:
    """Body lines (mirrors :::line-chart body-mode 'lines'):
        categories: FY 2023, FY 2024, FY 2025, Q1 2026
        Connectivity: 0, 0, 11.5, 3.2
        Space: 0, 0, 3.0, 0.6
    The `categories` row (case-insensitive label) is the shared category
    axis. Every other `LABEL: nums` row is one data series of RAW SIGNED
    numbers. Up to 6 series, each as long as the category list.

    orientation=vertical (default) | horizontal.
    mode=grouped | stacked (optional). Stacked rejects negative values —
    a stacked column with mixed signs is genuinely undefined geometry, so
    we fail at compile time rather than render garbage."""
    categories: list[str] | None = None
    series: list[tuple[str, list[str]]] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise AraSyntaxError(
                f":::bar-chart body line must be `LABEL: comma,nums`: {line!r}",
                line=line_no,
            )
        label, vals = line.split(":", 1)
        label = label.strip()
        if label.lower() == "categories":
            categories = _csv_values(vals)
        else:
            series.append((label, _csv_numbers(vals, f"bar-chart series {label!r}", line_no)))
    if categories is None:
        raise AraSyntaxError(":::bar-chart body needs a `categories:` row", line=line_no)
    if not categories:
        raise AraSyntaxError(":::bar-chart `categories:` row needs at least one label", line=line_no)
    if not series or len(series) > 6:
        raise AraSyntaxError(
            f":::bar-chart needs 1-6 data series, got {len(series)}",
            line=line_no,
        )
    for label, vals in series:
        if len(vals) != len(categories):
            raise AraSyntaxError(
                f"bar-chart series {label!r} has {len(vals)} values but categories has {len(categories)} labels",
                line=line_no,
            )

    orientation = attrs.get("orientation", "vertical")
    if orientation not in ("vertical", "horizontal"):
        raise AraSyntaxError(
            f":::bar-chart orientation must be vertical|horizontal, got {orientation!r}",
            line=line_no,
        )
    mode = attrs.get("mode")
    if mode is not None and mode not in ("grouped", "stacked"):
        raise AraSyntaxError(
            f":::bar-chart mode must be grouped|stacked, got {mode!r}",
            line=line_no,
        )
    if mode == "stacked":
        for label, vals in series:
            if any(float(v) < 0 for v in vals):
                raise AraSyntaxError(
                    f"stacked bar-chart cannot have negative values "
                    f"(series {label!r} has one)",
                    line=line_no,
                )

    parts = ['<div class="ara-bar-chart"']
    parts.append(_attr("data-categories", ",".join(categories)))
    for idx, (label, vals) in enumerate(series, start=1):
        parts.append(_attr(f"data-series-{idx}", ",".join(vals)))
        parts.append(_attr(f"data-series-{idx}-label", label))
    parts.append(_attr("data-orientation", orientation))
    if mode is not None:
        parts.append(_attr("data-mode", mode))
    if attrs.get("title") is not None:
        parts.append(_attr("data-title", attrs["title"]))
    if attrs.get("subtitle") is not None:
        parts.append(_attr("data-subtitle", attrs["subtitle"]))
    if attrs.get("value-unit") is not None:
        parts.append(_attr("data-unit", attrs["value-unit"]))
    if attrs.get("value-suffix") is not None:
        parts.append(_attr("data-value-suffix", attrs["value-suffix"]))
    parts.append("></div>")
    return "".join(parts)


def emit_donut(attrs: dict, body: Any, line_no: int) -> str:
    if not isinstance(body, list):
        raise AraSyntaxError(":::donut body must be a YAML list of {label, value}", line=line_no)
    labels = ",".join(str(_req(i, "label", "donut", line_no)) for i in body)
    values = ",".join(_number_text(_req(i, "value", "donut", line_no), "donut value", line_no) for i in body)
    parts = ['<div class="ara-donut"']
    parts.append(_attr("data-labels", labels))
    parts.append(_attr("data-values", values))
    if attrs.get("center-label"):
        parts.append(_attr("data-center-label", attrs["center-label"]))
    parts.append("></div>")
    return "".join(parts)


def emit_slope(attrs: dict, body: str, line_no: int) -> str:
    """Body is a markdown table with header `Item | Left | Right`."""
    table_lines = [l for l in body.splitlines() if l.strip()]
    if len(table_lines) < 3:
        raise AraSyntaxError(":::slope body needs a markdown table (3+ rows)", line=line_no)
    rows = [_split_row(l) for l in table_lines]
    if not all(len(r) >= 3 for r in rows):
        raise AraSyntaxError(":::slope table rows must have item, left value, and right value columns", line=line_no)
    rows = [rows[0]] + rows[2:]  # drop divider
    items = [r[0] for r in rows[1:]]
    left = [_number_text(r[1], "slope left value", line_no) for r in rows[1:]]
    right = [_number_text(r[2], "slope right value", line_no) for r in rows[1:]]
    parts = ['<div class="ara-slope"']
    parts.append(_attr("data-items", ",".join(items)))
    parts.append(_attr("data-left-values", ",".join(left)))
    parts.append(_attr("data-right-values", ",".join(right)))
    if attrs.get("left-label"):
        parts.append(_attr("data-left-label", attrs["left-label"]))
    if attrs.get("right-label"):
        parts.append(_attr("data-right-label", attrs["right-label"]))
    if attrs.get("unit"):
        parts.append(_attr("data-unit", attrs["unit"]))
    parts.append("></div>")
    return "".join(parts)


def emit_timeline(attrs: dict, body: Any, line_no: int) -> str:
    if not isinstance(body, list):
        raise AraSyntaxError(":::timeline body must be a YAML list of {date, headline, body}", line=line_no)
    out = ['<ol class="ara-timeline">']
    for item in body:
        date = _req(item, "date", "timeline", line_no)
        head = _req(item, "headline", "timeline", line_no)
        text = _opt(item, "body", "")
        out.append('<li class="ara-timeline-item">')
        out.append(f'<time class="ara-timeline-date">{html.escape(str(date))}</time>')
        out.append('<div class="ara-timeline-event">')
        out.append(f"<strong>{parse_inline(str(head))}</strong>")
        if text:
            out.append(f"<p>{parse_inline(str(text))}</p>")
        out.append('</div></li>')
    out.append("</ol>")
    return "".join(out)


def emit_iso(attrs: dict, body: Any, line_no: int) -> str:
    if not isinstance(body, list):
        raise AraSyntaxError(":::iso body must be a YAML list of {label, glyph, count}", line=line_no)
    out: list[str] = []
    for item in body:
        label = _req(item, "label", "iso", line_no)
        glyph = _req(item, "glyph", "iso", line_no)
        count = _int_range_text(_req(item, "count", "iso", line_no), "iso count", line_no, 0, 200)
        out.append('<div class="ara-iso">')
        out.append(f'<span class="ara-iso-label">{parse_inline(str(label))}</span>')
        out.append(
            f'<span class="ara-iso-glyphs"'
            f'{_attr("data-glyph", glyph)}'
            f'{_attr("data-count", count)}></span>'
        )
        out.append(f'<span class="ara-iso-total">{html.escape(str(count))}</span>')
        out.append('</div>')
    return "".join(out)


def emit_bars(attrs: dict, body: Any, line_no: int) -> str:
    if not isinstance(body, list):
        raise AraSyntaxError(":::bars body must be a YAML list of {label, value, pct}", line=line_no)
    out = ['<div class="ara-bars">']
    for item in body:
        label = _req(item, "label", "bars", line_no)
        value = _req(item, "value", "bars", line_no)
        pct = _pct_text(_req(item, "pct", "bars", line_no), "bars pct", line_no)
        out.append(f'<div class="ara-bar"{_attr("data-pct", pct)}>')
        out.append(f'<span class="ara-bar-label">{parse_inline(str(label))}</span>')
        out.append(f'<span class="ara-bar-value">{parse_inline(str(value))}</span>')
        out.append('</div>')
    out.append('</div>')
    return "".join(out)


def emit_stack_bar(attrs: dict, body: Any, line_no: int) -> str:
    if not isinstance(body, list):
        raise AraSyntaxError(":::stack-bar body must be a YAML list of {label, pct}", line=line_no)
    legend_on = bool(attrs.get("legend"))
    out = ['<div class="ara-stack-bar">']
    for idx, item in enumerate(body, start=1):
        if idx > 6:
            raise AraSyntaxError(":::stack-bar supports max 6 segments (variants --1..--6)", line=line_no)
        pct = _pct_text(_req(item, "pct", "stack-bar", line_no), "stack-bar pct", line_no)
        out.append(
            f'<span class="ara-stack-seg ara-stack-seg--{idx}"{_attr("data-pct", pct)}></span>'
        )
    out.append('</div>')
    if legend_on:
        out.append('<ul class="ara-stack-legend">')
        for idx, item in enumerate(body, start=1):
            label = _req(item, "label", "stack-bar", line_no)
            out.append(
                f'<li><span class="ara-stack-dot ara-stack-dot--{idx}"></span>'
                f'{parse_inline(str(label))}</li>'
            )
        out.append('</ul>')
    return "".join(out)


def emit_stack_rows(attrs: dict, body: Any, line_no: int) -> str:
    if not isinstance(body, dict):
        raise AraSyntaxError(
            ":::stack-rows body must be a YAML mapping with `categories:` and `rows:`",
            line=line_no,
        )
    cats = _req(body, "categories", "stack-rows", line_no)
    rows = _req(body, "rows", "stack-rows", line_no)
    if not isinstance(cats, list) or not isinstance(rows, list):
        raise AraSyntaxError(
            ":::stack-rows categories/rows must be lists",
            line=line_no,
        )
    if len(cats) > 6:
        raise AraSyntaxError(":::stack-rows supports max 6 categories", line=line_no)
    out = ['<div class="ara-stack-rows">']
    out.append('<div class="ara-stack-rows-legend">')
    for idx, cat in enumerate(cats, start=1):
        out.append(
            f'<span class="ara-stack-rows-cat ara-stack-rows-cat--{idx}">{parse_inline(str(cat))}</span>'
        )
    out.append('</div>')
    out.append('<div class="ara-stack-rows-grid">')
    for row in rows:
        label = _req(row, "label", "stack-rows row", line_no)
        values = _req(row, "values", "stack-rows row", line_no)
        if not isinstance(values, list) or len(values) != len(cats):
            raise AraSyntaxError(
                f":::stack-rows row {label!r} must have {len(cats)} values to match categories",
                line=line_no,
            )
        values = [_pct_text(v, "stack-rows value", line_no) for v in values]
        out.append('<div class="ara-stack-rows-row">')
        out.append(f'<span class="ara-stack-rows-label">{parse_inline(str(label))}</span>')
        out.append('<div class="ara-stack-bar">')
        for idx, v in enumerate(values, start=1):
            out.append(
                f'<span class="ara-stack-seg ara-stack-seg--{idx}"{_attr("data-pct", v)}></span>'
            )
        out.append('</div></div>')
    out.append('</div></div>')
    return "".join(out)


def emit_rank_list(attrs: dict, body: Any, line_no: int) -> str:
    if not isinstance(body, list):
        raise AraSyntaxError(":::rank-list body must be a YAML list", line=line_no)
    out = ['<ol class="ara-rank-list">']
    for idx, item in enumerate(body, start=1):
        label = _req(item, "label", "rank-list", line_no)
        value = _req(item, "value", "rank-list", line_no)
        pct = _pct_text(_opt(item, "pct", 0), "rank-list pct", line_no)
        highlight = " ara-row-highlight" if _opt(item, "highlight") else ""
        rank = _opt(item, "rank", idx)
        out.append(f'<li class="ara-rank-item{highlight}">')
        out.append(f'<span class="ara-rank-num">{html.escape(str(rank))}</span>')
        out.append(f'<span class="ara-rank-label">{parse_inline(str(label))}</span>')
        out.append(f'<span class="ara-rank-value">{parse_inline(str(value))}</span>')
        out.append(f'<span class="ara-rank-fill"{_attr("data-pct", pct)}></span>')
        out.append('</li>')
    out.append('</ol>')
    return "".join(out)


def emit_compare(attrs: dict, body: Any, line_no: int) -> str:
    if not isinstance(body, list):
        raise AraSyntaxError(":::compare body must be a YAML list of {role, name, value}", line=line_no)
    out = ['<div class="ara-compare">']
    for item in body:
        role = _req(item, "role", "compare", line_no)
        name = _req(item, "name", "compare", line_no)
        value = _req(item, "value", "compare", line_no)
        is_subject = str(role).lower() == "subject" or bool(_opt(item, "subject"))
        cls = "ara-compare-card ara-compare-card--subject" if is_subject else "ara-compare-card"
        out.append(f'<div class="{cls}">')
        out.append(f'<span class="ara-compare-role">{parse_inline(str(role))}</span>')
        out.append(f'<span class="ara-compare-name">{parse_inline(str(name))}</span>')
        out.append(f'<div class="ara-compare-value">{parse_inline(str(value))}</div>')
        out.append('</div>')
    out.append('</div>')
    return "".join(out)


def emit_references(attrs: dict, body: Any, line_no: int) -> str:
    if not isinstance(body, list):
        raise AraSyntaxError(":::references body must be a YAML list", line=line_no)
    if not body:
        raise AraSyntaxError(":::references needs at least one reference", line=line_no)
    out = [
        '<h3 class="ara-h2"><span class="ara-h2-num">R</span>References</h3>',
        '<ol>',
    ]
    for item in body:
        rid = _int_range_text(_req(item, "id", "references", line_no), "reference id", line_no, 1, 9999)
        title = _req(item, "title", "references", line_no)
        url = _opt(item, "url")
        source = _opt(item, "source")
        date = _opt(item, "date")
        bits = []
        if url:
            bits.append(
                f'<a href="{html.escape(str(url), quote=True)}">{parse_inline(str(title))}</a>'
            )
        else:
            bits.append(parse_inline(str(title)))
        if source:
            bits.append(f"— {parse_inline(str(source))}")
        if date:
            bits.append(f"({html.escape(str(date))})")
        out.append(f'<li id="ref-{html.escape(str(rid))}">' + " ".join(bits) + '</li>')
    out.append('</ol>')
    return "".join(out)


def emit_raw(attrs: dict, body: str, line_no: int) -> str:
    """Escape hatch. The body is emitted verbatim and then re-validated
    by the writer's tag/class allowlist. NOT a license to invent classes
    — those will still fail the strict validator at commit time."""
    return body


DIRECTIVES: dict[str, tuple[Callable, str]] = {
    # (emitter, body-kind) — body-kind: 'yaml', 'markdown', 'lines', 'none'
    "stats":       (emit_stats,       "yaml"),
    "kv":          (emit_kv,          "yaml"),
    "callout":     (emit_callout,     "markdown"),
    "quote":       (emit_quote,       "markdown"),
    "figure":      (emit_figure,      "markdown"),
    "line-chart":  (emit_line_chart,  "lines"),
    "tradingview": (emit_tradingview, "markdown"),
    "bar-chart":   (emit_bar_chart,   "lines"),
    "donut":       (emit_donut,       "yaml"),
    "slope":       (emit_slope,       "lines"),
    "timeline":    (emit_timeline,    "yaml"),
    "iso":         (emit_iso,         "yaml"),
    "bars":        (emit_bars,        "yaml"),
    "stack-bar":   (emit_stack_bar,   "yaml"),
    "stack-rows":  (emit_stack_rows,  "yaml"),
    "rank-list":   (emit_rank_list,   "yaml"),
    "compare":     (emit_compare,     "yaml"),
    "references":  (emit_references,  "yaml"),
    "raw":         (emit_raw,         "markdown"),
}


def emit_directive(buf: list[str], line_no: int) -> str:
    head = buf[0]
    parsed = parse_directive_open(head)
    if not parsed:
        raise AraSyntaxError(f"invalid directive opener: {head!r}", line=line_no)
    name, attrs_raw = parsed
    if name not in DIRECTIVES:
        raise AraSyntaxError(
            f"unknown directive :::{name}. Known: {', '.join(sorted(DIRECTIVES))}",
            line=line_no,
        )
    attrs = parse_attrs(attrs_raw)
    emitter, body_kind = DIRECTIVES[name]
    if body_kind == "yaml":
        body = _yaml_body(buf, line_no)
        return emitter(attrs, body, line_no)
    if body_kind == "markdown":
        body = _markdown_body(buf)
        return emitter(attrs, body, line_no)
    if body_kind == "lines":
        body = _markdown_body(buf)
        return emitter(attrs, body, line_no)
    raise AraSyntaxError(f"internal: unknown body kind {body_kind}", line=line_no)


# ----------------------------------------------------------------------
# Block compiler
# ----------------------------------------------------------------------


def compile_blocks(blocks: list[tuple[int, str, list[str]]]) -> str:
    out: list[str] = []
    for line_no, kind, buf in blocks:
        if kind == "heading":
            out.append(emit_heading(buf[0]))
        elif kind == "paragraph":
            out.append(emit_paragraph(buf))
        elif kind == "blockquote":
            out.append(emit_blockquote(buf))
        elif kind == "hr":
            out.append(emit_hr(buf))
        elif kind == "code":
            out.append(emit_code_fence(buf))
        elif kind == "list":
            out.append(emit_list(buf))
        elif kind == "table":
            out.append(emit_table(buf))
        elif kind == "directive":
            out.append(emit_directive(buf, line_no))
        else:
            raise AraSyntaxError(f"internal: unknown block kind {kind}", line=line_no)
    return "\n".join(out)


# ----------------------------------------------------------------------
# Article header from frontmatter
# ----------------------------------------------------------------------


def emit_header(meta: dict) -> str:
    if not meta:
        raise AraSyntaxError("frontmatter must include `title:`")
    parts = ["<header>"]
    if meta.get("eyebrow"):
        parts.append(f'<div class="ara-eyebrow">{parse_inline(str(meta["eyebrow"]))}</div>')
    if not meta.get("title"):
        raise AraSyntaxError("frontmatter must include `title:`")
    parts.append(f'<h2 class="ara-display">{parse_inline(str(meta["title"]))}</h2>')
    if meta.get("deck"):
        parts.append(f'<p class="ara-deck">{parse_inline(str(meta["deck"]))}</p>')
    if meta.get("lede"):
        parts.append(f'<p class="ara-lede">{parse_inline(str(meta["lede"]).strip())}</p>')
    if meta.get("stats"):
        parts.append(emit_stats({}, meta["stats"], line_no=0))
    parts.append("</header>")
    return "".join(parts)


# ----------------------------------------------------------------------
# Article-level contract checks
# ----------------------------------------------------------------------


HTML_CITE_RE = re.compile(r'href="#ref-([0-9]+)"')
HTML_REF_RE = re.compile(r'id="ref-([0-9]+)"')


def validate_block_contract(blocks: list[tuple[int, str, list[str]]]) -> None:
    reference_blocks: list[int] = []
    for idx, (line_no, kind, buf) in enumerate(blocks):
        if kind != "directive":
            continue
        parsed = parse_directive_open(buf[0])
        if parsed and parsed[0] == "references":
            reference_blocks.append(idx)
            if idx != len(blocks) - 1:
                raise AraSyntaxError(":::references must be the final block in the article", line=line_no)
    if len(reference_blocks) > 1:
        first = blocks[reference_blocks[1]][0]
        raise AraSyntaxError("article can only contain one :::references block", line=first)


def validate_article_contract(article_html: str) -> None:
    """Enforce article-level invariants that span multiple blocks."""
    cited = HTML_CITE_RE.findall(article_html)
    refs = HTML_REF_RE.findall(article_html)
    if not refs:
        if cited:
            raise AraSyntaxError("cited articles must include a final :::references block")
        return

    ref_ids = set(refs)
    duplicate_refs = sorted({rid for rid in refs if refs.count(rid) > 1}, key=int)
    if duplicate_refs:
        raise AraSyntaxError(f"duplicate reference id(s): {', '.join(duplicate_refs)}")

    missing = sorted(set(cited) - ref_ids, key=int)
    if missing:
        raise AraSyntaxError(f"citation id(s) missing from :::references: {', '.join(missing)}")


# ----------------------------------------------------------------------
# Section wrapping — every ## opens a fresh <section class="ara-section">
# ----------------------------------------------------------------------


def wrap_in_sections(body_html: str) -> str:
    """Walk the rendered blocks and wrap each `## heading` group in
    <section class="ara-section">. References stay inside their own
    section. Anything before the first heading goes into a leading
    unwrapped block."""
    pieces = body_html.split("\n")
    sections: list[list[str]] = [[]]
    for line in pieces:
        if line.startswith('<h3 class="ara-h2"'):
            sections.append([line])
        else:
            sections[-1].append(line)
    out: list[str] = []
    for idx, sec in enumerate(sections):
        if not sec or all(not s.strip() for s in sec):
            continue
        body = "\n".join(sec).strip()
        if idx == 0:
            out.append(body)
        else:
            out.append(f'<section class="ara-section">\n{body}\n</section>')
    return "\n".join(out)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------


def compile_source(source: str) -> str:
    meta, body = parse_frontmatter(source)
    header = emit_header(meta)
    blocks = split_blocks(body)
    validate_block_contract(blocks)
    body_html = compile_blocks(blocks)
    wrapped = wrap_in_sections(body_html)
    parts = ['<article class="ara-doc">']
    if header:
        parts.append(header)
    parts.append(wrapped)
    parts.append('</article>\n')
    article = "\n".join(parts)
    validate_article_contract(article)
    try:
        from write_generative_research import KIND_FRAGMENT, validate_body
        validate_body(article, KIND_FRAGMENT)
    except ValueError as e:
        raise AraSyntaxError(f"HTML validation failed: {e}") from e
    return article


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", help="path to .ara.md (or '-' for stdin)")
    p.add_argument(
        "--out",
        default="-",
        help="output path for compiled HTML (default: stdout)",
    )
    p.add_argument("--meta-json", help="if set, also dump frontmatter as JSON to this path")
    args = p.parse_args(argv)

    if args.source == "-":
        source = sys.stdin.read()
    else:
        source = Path(args.source).read_text(encoding="utf-8")

    try:
        html_out = compile_source(source)
    except AraSyntaxError as e:
        print(f"compile_ara: {e}", file=sys.stderr)
        return 1

    try:
        from write_generative_research import validate_body, KIND_FRAGMENT
        validate_body(html_out, KIND_FRAGMENT)
    except ValueError as e:
        print(f"compile_ara: validation failed: {e}", file=sys.stderr)
        return 1

    if args.out == "-":
        sys.stdout.write(html_out)
    else:
        Path(args.out).write_text(html_out, encoding="utf-8")

    if args.meta_json:
        meta, _ = parse_frontmatter(source)
        Path(args.meta_json).write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
