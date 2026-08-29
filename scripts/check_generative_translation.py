#!/usr/bin/env python3
"""Deterministic source/translation parity checks for Korean ARA backfills."""

from __future__ import annotations

import argparse
import collections
import math
import re
from html.parser import HTMLParser
from pathlib import Path

from compile_ara import AraSyntaxError, compile_source


URL_RE = re.compile(r"https?://[^\s<>\"'()\]}]+")
NUMBER_RE = re.compile(r"(?<!\d)[+\-−]?(?:[$€£₩¥]\s*)?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:%|×|x)?(?!\d)")
FOOTNOTE_RE = re.compile(r"\[\^([A-Za-z0-9_-]+)\]")
BLOCK_DIRECTIVE_RE = re.compile(r"^\s*:::(?:([a-z][a-z0-9-]*)\b.*)?$", re.MULTILINE)
INLINE_DIRECTIVE_RE = re.compile(r"\{(/|[a-z][a-z0-9-]*)(?::[^{}]*)?\}")
HANGUL_RE = re.compile(r"[가-힣]")
LATIN_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z'-]*\b")
TRANSLATABLE_LIST_ATTRS = frozenset(
    {"data-categories", "data-items", "data-labels", "data-x-labels"}
)
TRANSLATABLE_DATA_ATTRS = frozenset(
    {
        "data-center-label",
        "data-left-label",
        "data-right-label",
        "data-subtitle",
        "data-title",
    }
)


def _urls(text: str) -> collections.Counter[str]:
    return collections.Counter(match.rstrip(".,;:!?") for match in URL_RE.findall(text))


def _numbers(text: str) -> collections.Counter[str]:
    return collections.Counter(NUMBER_RE.findall(text))


def _localized_integer_additions_are_safe(
    source_numbers: collections.Counter[str], target: str
) -> bool:
    """Allow only extra plain integers used as Korean counter/ordinal forms."""
    target_matches: dict[str, list[re.Match[str]]] = collections.defaultdict(list)
    for match in NUMBER_RE.finditer(target):
        target_matches[match.group()].append(match)
    target_numbers = collections.Counter(
        {token: len(matches) for token, matches in target_matches.items()}
    )
    if source_numbers - target_numbers:
        return False
    for token, target_count in target_numbers.items():
        extra_count = target_count - source_numbers[token]
        if extra_count <= 0:
            continue
        localized_count = sum(
            token.isascii()
            and token.isdigit()
            and match.end() < len(target)
            and bool(HANGUL_RE.fullmatch(target[match.end()]))
            for match in target_matches[token]
        )
        if localized_count < extra_count:
            return False
    return True


class TopologyParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.events: list[
            tuple[str, str, tuple[str, ...], tuple[tuple[str, str], ...]]
        ] = []

    @staticmethod
    def _classes(attrs: list[tuple[str, str | None]]) -> tuple[str, ...]:
        raw = next((value or "" for key, value in attrs if key == "class"), "")
        return tuple(sorted(part for part in raw.split() if part.startswith("ara-")))

    @staticmethod
    def _immutable_attrs(
        attrs: list[tuple[str, str | None]],
    ) -> tuple[tuple[str, str], ...]:
        """Fingerprint attribute shape while allowing reader-facing translation.

        Link/anchor identity and machine-readable chart values remain exact.
        Titles, labels, captions, and categorical axis text keep their key and
        (for lists) cardinality, but their prose may be translated.
        """
        fingerprint: list[tuple[str, str]] = []
        for key, value in attrs:
            if key == "class":
                continue
            raw = value or ""
            if key in {"id", "href", "src", "name"}:
                fingerprint.append((key, raw))
            elif (
                key in TRANSLATABLE_DATA_ATTRS
                or key in TRANSLATABLE_LIST_ATTRS
                or re.fullmatch(r"data-series-\d+-label", key)
            ):
                fingerprint.append((key, "<translated>"))
            elif key.startswith("data-"):
                # Fail closed for future component fields. New reader-facing
                # attributes must be added explicitly above; everything else
                # is treated as machine-readable state.
                fingerprint.append((key, raw))
            else:
                fingerprint.append((key, "<translated>"))
        return tuple(
            sorted(fingerprint)
        )

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.events.append(
            ("start", tag, self._classes(attrs), self._immutable_attrs(attrs))
        )

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.events.append(
            ("empty", tag, self._classes(attrs), self._immutable_attrs(attrs))
        )

    def handle_endtag(self, tag: str) -> None:
        self.events.append(("end", tag, (), ()))


def _as_html(path: Path, raw: str) -> str:
    if path.name.endswith(".ara.md"):
        try:
            return compile_source(raw)
        except AraSyntaxError as exc:
            raise ValueError(f"{path}: ARA compile failed: {exc}") from exc
    return raw


def _topology(
    html: str,
) -> list[tuple[str, str, tuple[str, ...], tuple[tuple[str, str], ...]]]:
    parser = TopologyParser()
    parser.feed(html)
    parser.close()
    return parser.events


class VisibleProseParser(HTMLParser):
    """Collect visible prose while excluding code that translation preserves."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._excluded_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"code", "pre", "script", "style"}:
            self._excluded_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"code", "pre", "script", "style"} and self._excluded_depth:
            self._excluded_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._excluded_depth:
            self.parts.append(data)


def _lowercase_prose_ngrams(html: str, size: int = 5) -> collections.Counter[tuple[str, ...]]:
    parser = VisibleProseParser()
    parser.feed(html)
    parser.close()
    # All-lowercase tokens intentionally exclude model names, tickers, and
    # most proper nouns. Those legitimately survive a Korean translation;
    # ordinary copied English prose does not.
    tokens = [
        token
        for token in LATIN_WORD_RE.findall(" ".join(parser.parts))
        if token.islower() and len(token) >= 3
    ]
    return collections.Counter(
        tuple(tokens[index : index + size])
        for index in range(len(tokens) - size + 1)
    )


def check_pair(
    source: Path,
    translation: Path,
    *,
    allow_localized_number_rendering: bool = False,
) -> list[str]:
    source_raw = source.read_text(encoding="utf-8")
    target_raw = translation.read_text(encoding="utf-8")
    errors: list[str] = []

    if not source.name.endswith(".ara.md") and translation.name.endswith(".ara.md"):
        errors.append("HTML sources cannot be compared with an ARA translation")
        return errors
    cross_representation = source.name.endswith(".ara.md") and not translation.name.endswith(".ara.md")
    source_comparison = _as_html(source, source_raw) if cross_representation else source_raw
    if _urls(source_comparison) != _urls(target_raw):
        errors.append("URL multiset changed")
    source_numbers = _numbers(source_comparison)
    target_numbers = _numbers(target_raw)
    if allow_localized_number_rendering:
        if not cross_representation:
            errors.append(
                "localized number rendering is only valid for ARA-to-HTML comparisons"
            )
        elif not _localized_integer_additions_are_safe(source_numbers, target_raw):
            missing = sorted((source_numbers - target_numbers).elements())
            extra = sorted((target_numbers - source_numbers).elements())
            errors.append(
                "source numeric-token multiset was not preserved or target added "
                "a non-localized numeric token"
            )
            errors.append(f"numeric-token diff missing={missing} extra={extra}")
    elif source_numbers != target_numbers:
        errors.append("numeric-token multiset changed")
    if source.name.endswith(".ara.md") and translation.name.endswith(".ara.md"):
        if collections.Counter(FOOTNOTE_RE.findall(source_raw)) != collections.Counter(FOOTNOTE_RE.findall(target_raw)):
            errors.append("citation/reference-id multiset changed")
        source_directives = [(m.group(1) or "close") for m in BLOCK_DIRECTIVE_RE.finditer(source_raw)]
        target_directives = [(m.group(1) or "close") for m in BLOCK_DIRECTIVE_RE.finditer(target_raw)]
        if source_directives != target_directives:
            errors.append("ARA block-directive topology changed")
        if INLINE_DIRECTIVE_RE.findall(source_raw) != INLINE_DIRECTIVE_RE.findall(target_raw):
            errors.append("ARA inline-directive topology changed")

    try:
        source_html = _as_html(source, source_raw)
        target_html = _as_html(translation, target_raw)
    except ValueError as exc:
        errors.append(str(exc))
        return errors
    if _topology(source_html) != _topology(target_html):
        errors.append("compiled HTML tag/class/immutable-attribute topology changed")

    source_ngrams = _lowercase_prose_ngrams(source_html)
    if sum(source_ngrams.values()) >= 20:
        target_ngrams = _lowercase_prose_ngrams(target_html)
        reused = sum((source_ngrams & target_ngrams).values())
        reuse_share = reused / sum(source_ngrams.values())
        if reuse_share > 0.35:
            errors.append(
                "too much visible English prose was copied unchanged "
                f"({reuse_share:.0%} of source lowercase 5-grams)"
            )

    hangul = len(HANGUL_RE.findall(re.sub(URL_RE, "", target_html)))
    source_words = len(LATIN_WORD_RE.findall(re.sub(URL_RE, "", source_comparison)))
    minimum_hangul = min(200, max(8, math.ceil(source_words * 0.10)))
    if hangul < minimum_hangul:
        errors.append(
            "translation contains too little Korean prose "
            f"({hangul} Hangul syllables; need {minimum_hangul} for this source)"
        )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-localized-number-rendering",
        action="store_true",
        help=(
            "for trusted ARA-to-HTML segment rendering, require every source "
            "numeric literal while allowing Korean prose to render spelled quantities as digits"
        ),
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("translation", type=Path)
    args = parser.parse_args(argv)
    errors = check_pair(
        args.source,
        args.translation,
        allow_localized_number_rendering=args.allow_localized_number_rendering,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Korean translation parity checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
