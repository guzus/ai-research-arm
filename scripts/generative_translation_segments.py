#!/usr/bin/env python3
"""Prepare and render structure-preserving generative-research translations.

The model never authors ARA or HTML. Trusted code compiles the canonical ARA
source, exposes only reader-facing text slots with immutable literals replaced
by opaque tokens, and reconstructs HTML after validating complete model output.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

from check_generative_translation import NUMBER_RE, URL_RE
from compile_ara import AraSyntaxError, compile_source


MANIFEST_PATH = Path(".agent-input/translation-segments.json")
RESULT_PATH = Path(".tmp/generative-translation.ko.segments.jsonl")
DRAFT_PATH = Path(".tmp/generative-translation.ko.html")
TAG_NAME_RE = re.compile(r"<\s*(/?)\s*([A-Za-z][A-Za-z0-9:-]*)")
ATTR_RE = re.compile(
    r"\s([A-Za-z_:][A-Za-z0-9_.:-]*)\s*=\s*([\"'])(.*?)\2", re.DOTALL
)
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
TOKEN_RE = re.compile(r"\u27e6ARA\d{4}\u27e7")
EXCLUDED_TAGS = frozenset({"code", "pre", "script", "style"})
TRANSLATABLE_ATTRS = frozenset(
    {
        "alt",
        "title",
        "data-categories",
        "data-center-label",
        "data-items",
        "data-labels",
        "data-left-label",
        "data-right-label",
        "data-subtitle",
        "data-title",
        "data-x-labels",
    }
)
SERIES_LABEL_RE = re.compile(r"data-series-\d+-label")


@dataclass(frozen=True)
class Segment:
    id: str
    start: int
    end: int
    text: str
    tokens: list[str]
    literals: list[str]
    context: str
    attribute: bool
    forbid_commas: bool


def _mask(text: str, *, preserve_commas: bool) -> tuple[str, list[str], list[str]]:
    patterns = [URL_RE, NUMBER_RE]
    spans: list[tuple[int, int]] = []
    for pattern in patterns:
        spans.extend((match.start(), match.end()) for match in pattern.finditer(text))
    if preserve_commas:
        spans.extend((match.start(), match.end()) for match in re.finditer(r",", text))
    spans.sort()
    nonoverlap: list[tuple[int, int]] = []
    for start, end in spans:
        if nonoverlap and start < nonoverlap[-1][1]:
            continue
        nonoverlap.append((start, end))
    out: list[str] = []
    tokens: list[str] = []
    literals: list[str] = []
    cursor = 0
    for index, (start, end) in enumerate(nonoverlap):
        token = f"\u27e6ARA{index:04d}\u27e7"
        out.extend((text[cursor:start], token))
        tokens.append(token)
        literals.append(text[start:end])
        cursor = end
    out.append(text[cursor:])
    return "".join(out), tokens, literals


def _add_segment(
    segments: list[Segment],
    source: str,
    start: int,
    end: int,
    *,
    context: str,
    attribute: bool,
    preserve_commas: bool = False,
) -> None:
    raw_full = source[start:end]
    leading = len(raw_full) - len(raw_full.lstrip())
    trailing = len(raw_full) - len(raw_full.rstrip())
    start += leading
    end -= trailing
    if start >= end:
        return
    raw = source[start:end]
    decoded = html.unescape(raw)
    if not WORD_RE.search(decoded):
        return
    masked, tokens, literals = _mask(decoded, preserve_commas=preserve_commas)
    segments.append(
        Segment(
            id=f"s{len(segments) + 1:05d}",
            start=start,
            end=end,
            text=masked,
            tokens=tokens,
            literals=literals,
            context=context,
            attribute=attribute,
            forbid_commas=preserve_commas,
        )
    )


def _tag_spans(source: str):
    """Yield HTML tag/comment spans without treating quoted ``>`` as a close."""
    cursor = 0
    while True:
        start = source.find("<", cursor)
        if start < 0:
            return
        if source.startswith("<!--", start):
            close = source.find("-->", start + 4)
            if close < 0:
                return
            yield start, close + 3
            cursor = close + 3
            continue
        quote = ""
        index = start + 1
        while index < len(source):
            char = source[index]
            if quote:
                if char == quote:
                    quote = ""
            elif char in {'"', "'"}:
                quote = char
            elif char == ">":
                yield start, index + 1
                cursor = index + 1
                break
            index += 1
        else:
            return


def extract_segments(compiled_html: str) -> list[Segment]:
    segments: list[Segment] = []
    excluded: list[str] = []
    cursor = 0
    for tag_start, tag_end in _tag_spans(compiled_html):
        if tag_start > cursor and not excluded:
            _add_segment(
                segments,
                compiled_html,
                cursor,
                tag_start,
                context="visible text",
                attribute=False,
            )
        tag = compiled_html[tag_start:tag_end]
        name_match = TAG_NAME_RE.match(tag)
        name = name_match.group(2).lower() if name_match else ""
        closing = bool(name_match and name_match.group(1))
        if not excluded and not closing:
            for attr in ATTR_RE.finditer(tag):
                key = attr.group(1).lower()
                if key not in TRANSLATABLE_ATTRS and not SERIES_LABEL_RE.fullmatch(key):
                    continue
                value_start = tag_start + attr.start(3)
                value_end = tag_start + attr.end(3)
                _add_segment(
                    segments,
                    compiled_html,
                    value_start,
                    value_end,
                    context=f"{name or 'element'} {key}",
                    attribute=True,
                    preserve_commas=key
                    in {"data-categories", "data-items", "data-labels", "data-x-labels"},
                )
        if name in EXCLUDED_TAGS:
            if closing:
                if excluded and excluded[-1] == name:
                    excluded.pop()
            elif not tag.rstrip().endswith("/>"):
                excluded.append(name)
        cursor = tag_end
    if cursor < len(compiled_html) and not excluded:
        _add_segment(
            segments,
            compiled_html,
            cursor,
            len(compiled_html),
            context="visible text",
            attribute=False,
        )
    return segments


def build_manifest(source_path: Path, source_sha256: str) -> tuple[str, dict]:
    payload = source_path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != source_sha256:
        raise ValueError("canonical translation source changed before segment preparation")
    try:
        compiled = compile_source(payload.decode("utf-8"))
    except (UnicodeDecodeError, AraSyntaxError) as exc:
        raise ValueError(f"cannot compile canonical ARA source: {exc}") from exc
    segments = extract_segments(compiled)
    if not segments:
        raise ValueError("canonical article contains no translatable text segments")
    manifest = {
        "version": 1,
        "source_sha256": source_sha256,
        "result_path": RESULT_PATH.as_posix(),
        "segment_count": len(segments),
        "segments": [
            {
                "id": segment.id,
                "text": segment.text,
                "tokens": segment.tokens,
                "context": segment.context,
                "forbid_commas": segment.forbid_commas,
            }
            for segment in segments
        ],
    }
    return compiled, manifest


def _atomic_write(path: Path, payload: str) -> None:
    path.parent.mkdir(exist_ok=True)
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError(f"refusing unsafe translation output path: {path}")
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def write_manifest(source_path: Path, source_sha256: str, manifest_path: Path) -> dict:
    if manifest_path != MANIFEST_PATH:
        raise ValueError(f"manifest path must be exactly {MANIFEST_PATH}")
    _, manifest = build_manifest(source_path, source_sha256)
    _atomic_write(
        manifest_path,
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
    return manifest


def _read_results(path: Path) -> dict[str, str]:
    if not path.is_file() or path.is_symlink() or path != RESULT_PATH:
        raise ValueError(f"translation result must be the regular file {RESULT_PATH}")
    translations: dict[str, str] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid translation result JSON on line {line_no}: {exc}") from exc
        if not isinstance(value, dict) or set(value) != {"id", "text"}:
            raise ValueError(f"translation result line {line_no} has invalid fields")
        segment_id, text = value["id"], value["text"]
        if not isinstance(segment_id, str) or not isinstance(text, str) or not text.strip():
            raise ValueError(f"translation result line {line_no} has invalid id/text")
        if segment_id in translations:
            raise ValueError(f"duplicate translation segment: {segment_id}")
        translations[segment_id] = text
    return translations


def render(source_path: Path, source_sha256: str, result_path: Path, draft_path: Path) -> None:
    if result_path != RESULT_PATH or draft_path != DRAFT_PATH:
        raise ValueError("translation result/draft paths do not match the fixed contract")
    compiled, manifest = build_manifest(source_path, source_sha256)
    segments = extract_segments(compiled)
    translations = _read_results(result_path)
    expected = {segment.id for segment in segments}
    if set(translations) != expected:
        missing = sorted(expected - set(translations))[:8]
        extra = sorted(set(translations) - expected)[:8]
        raise ValueError(f"translation segment coverage mismatch; missing={missing}, extra={extra}")

    rendered = compiled
    for segment in reversed(segments):
        translated = translations[segment.id]
        found_tokens = TOKEN_RE.findall(translated)
        if found_tokens != segment.tokens:
            raise ValueError(
                f"translation segment {segment.id} changed immutable tokens; "
                f"expected={segment.tokens}, got={found_tokens}"
            )
        if segment.forbid_commas and "," in translated:
            raise ValueError(
                f"translation segment {segment.id} added an unprotected list separator"
            )
        for token, literal in zip(segment.tokens, segment.literals, strict=True):
            translated = translated.replace(token, literal, 1)
        escaped = html.escape(translated, quote=segment.attribute)
        rendered = rendered[: segment.start] + escaped + rendered[segment.end :]
    _atomic_write(draft_path, rendered if rendered.endswith("\n") else rendered + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--source", type=Path, required=True)
    prepare.add_argument("--source-sha256", required=True)
    prepare.add_argument("--manifest", type=Path, required=True)
    render_cmd = sub.add_parser("render")
    render_cmd.add_argument("--source", type=Path, required=True)
    render_cmd.add_argument("--source-sha256", required=True)
    render_cmd.add_argument("--result", type=Path, required=True)
    render_cmd.add_argument("--draft", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == "prepare":
        manifest = write_manifest(args.source, args.source_sha256, args.manifest)
        print(f"prepared {manifest['segment_count']} protected translation segments")
    else:
        render(args.source, args.source_sha256, args.result, args.draft)
        print(f"rendered trusted Korean HTML: {args.draft}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
