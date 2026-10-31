#!/usr/bin/env python3
"""Prepare and render structure-preserving generative-research translations.

The model never authors ARA or HTML. Trusted code compiles the canonical ARA
source, exposes only reader-facing text slots with immutable literals replaced
by opaque tokens, and reconstructs HTML after validating complete model output.
"""

from __future__ import annotations

import argparse
import collections
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
# A hyphen between Korean units is a range dash: 4월-6월 keeps its 6.
LOCALIZED_INTEGER_RE = re.compile(
    r"(?:(?<![0-9.,+\-−$€£₩¥])|(?<=[가-힣][\-–~]))[0-9]+(?=[가-힣])"
)
NUMBER_DEBRIS_RE = re.compile(r"[$€£₩¥%×]+")
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

# The model sees every source number as an opaque token, so it cannot tell a
# day from a year, and Korean dates put the year first. Asked to keep tokens
# in order without inventing digits, models wrote "29월 2026" for
# "October 29, 2026". Trusted code therefore masks a whole calendar date as
# one token whose literal is the finished Korean date.
_MONTH_FULL_NAMES = (
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
)
MONTH_NUMBERS = {name: number for number, name in enumerate(_MONTH_FULL_NAMES, 1)}
MONTH_NUMBERS.update(
    {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sept": 9,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }
)


def _spellings(names) -> str:
    return "|".join(
        spelling
        for name in sorted(names, key=len, reverse=True)
        for spelling in (name.title(), name.upper())
    )


# An abbreviation keeps its period only while the date continues, so the
# full stop in "on 12 Jun." stays prose.
_MONTH = (
    rf"(?:{_spellings(_MONTH_FULL_NAMES)}"
    rf"|(?:{_spellings(set(MONTH_NUMBERS) - set(_MONTH_FULL_NAMES))})"
    r"(?:\.(?=,?\s*[0-9–—-]))?)(?![A-Za-z])"
)
_DAY = r"(?:0?[1-9]|[12][0-9]|3[01])(?![0-9])"
_ORDINAL = r"(?:st|nd|rd|th)?"
_YEAR = r"(?:1[89]|2[01])[0-9]{2}(?![0-9])"
_RANGE = r"\s*[–—-]\s*"
# "Long March 5" is a rocket.
_MONTH_START = r"\b(?<!Long )"


def _date_forms(*, commas: bool) -> tuple[tuple[str, re.Pattern[str]], ...]:
    """Recognizers from longest to shortest.

    In a comma-separated list attribute every comma is a separator, so no date
    there spans one and a comma before a digit does not mean thousands.
    """
    comma = ",?" if commas else ""
    list_comma = r"(?:,\s*" + _DAY + _ORDINAL + r")*,?" if commas else ""
    separators = ".,+" if commas else ".+"
    day_start = rf"(?<![A-Za-z0-9{separators}\-−$€£₩¥/:#])"
    # A date ends before a decimal, time, ratio, percent, or glued word:
    # "Aug 18:00" is a time and "October 4.7" a version. A day glued to a
    # word by a hyphen is not a day either ("26 August 10-Q" is a filing),
    # though "Jun 2025-May 2026" and "October-2025-to-June" continue.
    decimal = r"[.,:][0-9]" if commas else r"[.:][0-9]"
    year_end = rf"(?![A-Za-z0-9%×/]|{decimal})"
    day_end = rf"(?![A-Za-z0-9%×/]|{decimal}|-(?!{_MONTH})[A-Za-z])"
    day_range = rf"(?P<d>{_DAY}){_ORDINAL}(?:(?P<sep>{_RANGE})(?P<d2>{_DAY}){_ORDINAL})?"
    forms = {
        "cross_md": (
            rf"{_MONTH_START}(?P<m>{_MONTH})\s+(?P<d>{_DAY}){_ORDINAL}(?P<sep>{_RANGE})"
            rf"(?P<m2>{_MONTH})\s+(?P<d2>{_DAY}){_ORDINAL}"
            rf"(?:{comma}\s+(?P<y>{_YEAR}){year_end}|{day_end})"
        ),
        "cross_dm": (
            rf"{day_start}(?P<d>{_DAY}){_ORDINAL}\s+(?P<m>{_MONTH})(?P<sep>{_RANGE})"
            rf"(?P<d2>{_DAY}){_ORDINAL}\s+(?P<m2>{_MONTH})"
            rf"(?:{comma}\s+(?P<y>{_YEAR}){year_end})?"
        ),
        "month_range": (
            rf"{_MONTH_START}(?P<m>{_MONTH})(?P<sep>{_RANGE})(?P<m2>{_MONTH}){comma}\s+"
            rf"(?P<y>{_YEAR}){year_end}"
        ),
        "day_list": (
            rf"{day_start}(?P<days>{_DAY}{_ORDINAL}{list_comma}\s+and\s+{_DAY}{_ORDINAL})"
            rf"\s+(?P<m>{_MONTH})(?:{comma}\s+(?P<y>{_YEAR}){year_end})?"
        ),
        "month_day_year": (
            rf"{_MONTH_START}(?P<m>{_MONTH})\s+{day_range}{comma}\s+(?P<y>{_YEAR}){year_end}"
        ),
        "day_month_year": (
            rf"{day_start}{day_range}\s+(?P<m>{_MONTH}){comma}\s+(?P<y>{_YEAR}){year_end}"
        ),
        "month_year": rf"{_MONTH_START}(?P<m>{_MONTH})(?:\s+|-)(?P<y>{_YEAR}){year_end}",
        "month_day": rf"{_MONTH_START}(?P<m>{_MONTH})\s+{day_range}{day_end}",
        "day_month": rf"{day_start}{day_range}\s+(?P<m>{_MONTH})",
    }
    return tuple((name, re.compile(pattern)) for name, pattern in forms.items())


_DATE_FORMS = {True: _date_forms(commas=True), False: _date_forms(commas=False)}


def _month_number(word: str) -> int:
    return MONTH_NUMBERS[word.rstrip(".").lower()]


def _korean_days(days: list[str]) -> str:
    if len(days) == 1:
        return f"{days[0]}일"
    return ", ".join(f"{day}일" for day in days[:-1]) + f"과 {days[-1]}일"


def korean_date(form: str, match: re.Match[str], year_digits: str | None = None) -> str:
    """Render one recognized English date in Korean order with the source digits.

    Days and years keep their exact source spelling ("05", "7-9") so the
    numeric-token parity check still finds every source literal; only month
    numbers glued to 월 are added. ``year_digits`` overrides the date's own
    year ("" drops it) when a range shares one.
    """
    groups = match.groupdict()
    if year_digits is None:
        year_digits = groups.get("y") or ""
    year = f"{year_digits}년 " if year_digits else ""
    month = _month_number(groups["m"])
    if form in {"cross_md", "cross_dm", "month_range"}:
        # A bare hyphen before a digit would read as a negative number token.
        sep = groups["sep"].replace("-", "–")
        month2 = _month_number(groups["m2"])
        first = f"{month}월" if form == "month_range" else f"{month}월 {groups['d']}일"
        second = f"{month2}월" if form == "month_range" else f"{month2}월 {groups['d2']}일"
        # The year follows the last part in English; a range that wraps past
        # December ("April–February 2026") gives it only to that part.
        if month > month2:
            return f"{first}{sep}{year}{second}"
        return f"{year}{first}{sep}{second}"
    if form == "day_list":
        return f"{year}{month}월 {_korean_days(re.findall(r'[0-9]+', groups['days']))}"
    if form == "month_year":
        return f"{year}{month}월"
    day = groups["d"] + (f"{groups['sep']}{groups['d2']}" if groups.get("d2") else "")
    return f"{year}{month}월 {day}일"


# A number another word owns is no day ("Top 10 March Madness", "Season 1
# Aug", "Gemini 3 June update"), and a month inside a name is no month.
_NUMBER_OWNERS = frozenset(
    {"top", "no", "no.", "#", "number", "rank", "season", "series", "episode", "chapter",
     "part", "phase", "stage", "round", "tier", "level", "gen", "grade", "week", "version",
     "fortune"}
)
_NUMBERED_NAMES = frozenset(
    {"GPT", "Gemini", "Claude", "Llama", "Grok", "Qwen", "DeepSeek", "Mistral", "Kimi", "GLM",
     "Fable", "Opus", "Sonnet", "Haiku", "iPhone", "Pixel", "Galaxy", "Windows", "iOS", "Android"}
)
_MONTH_IN_A_NAME_RE = re.compile(r"March\s+Madness|May\s+Day|March\s+of\s+Dimes")
_DAY_FIRST_FORMS = frozenset({"cross_dm", "day_list", "day_month_year", "day_month"})


def _not_a_date(text: str, form: str, match: re.Match[str]) -> bool:
    for name in ("m", "m2"):
        if match.groupdict().get(name) and _MONTH_IN_A_NAME_RE.match(text, match.start(name)):
            return True
    if form not in _DAY_FIRST_FORMS:
        return False
    owner = re.search(r"(\S+)\s+$", text[max(0, match.start() - 40) : match.start()])
    return bool(owner) and (owner.group(1).lower() in _NUMBER_OWNERS or owner.group(1) in _NUMBERED_NAMES)


def date_matches(text: str, *, commas: bool = True) -> list[tuple[str, re.Match[str]]]:
    """Return non-overlapping English calendar dates as (form, match).

    The longest reading wins ("Season 1 Aug 20, 2025" is August 20), then the
    earliest ("26 August 10 analysts" is August 26).
    """
    candidates = sorted(
        (
            (match.start() - match.end(), match.start(), priority, form, match)
            for priority, (form, pattern) in enumerate(_DATE_FORMS[commas])
            for match in pattern.finditer(text)
            if not _not_a_date(text, form, match)
        ),
        key=lambda item: item[:3],
    )
    found: list[tuple[str, re.Match[str]]] = []
    for _, start, _, form, match in candidates:
        if any(start < taken.end() and taken.start() < match.end() for _, taken in found):
            continue
        found.append((form, match))
    return sorted(found, key=lambda item: item[1].start())


# Two dates joined like this form one range ("from September 10 to early
# October 2026", "between June 3 and June 9, 2026").
_RANGE_JOIN_RE = re.compile(
    r"\s*(?:[–—~-]|to|through|thru|until|till|and|or)\s*"
    r"(?:(?:the\s+)?(?:early|mid|late|end\s+of|start\s+of|beginning\s+of|middle\s+of)[\s-]+)?"
)


def korean_dates(text: str, *, commas: bool = True) -> list[tuple[str, re.Match[str], str]]:
    """Recognized dates as (form, match, Korean); a range shares its year.

    English puts a range's year at its end ("September 10 to early October
    2026"); Korean puts it first, so the first date borrows it and the second
    drops it: 2026년 9월 10일 ... 10월. A range that wraps past December keeps
    the year where the source has it.
    """
    found = date_matches(text, commas=commas)
    rendered = [korean_date(form, match) for form, match in found]
    for k in range(len(found) - 1):
        (first_form, first), (second_form, second) = found[k], found[k + 1]
        year = second.groupdict().get("y")
        if first.groupdict().get("y") or not year:
            continue
        if not _RANGE_JOIN_RE.fullmatch(text[first.end() : second.start()]):
            continue
        last_month = _month_number(first.groupdict().get("m2") or first["m"])
        if last_month > _month_number(second["m"]):
            continue
        rendered[k] = korean_date(first_form, first, year)
        rendered[k + 1] = korean_date(second_form, second, "")
    return [(form, match, korean) for (form, match), korean in zip(found, rendered)]


def date_spans(text: str, *, commas: bool = True) -> list[tuple[int, int, str]]:
    """Return non-overlapping English calendar dates as (start, end, Korean)."""
    return [
        (match.start(), match.end(), korean)
        for _, match, korean in korean_dates(text, commas=commas)
    ]


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
    date_tokens: tuple[str, ...] = ()


def _mask(
    text: str, *, preserve_commas: bool
) -> tuple[str, list[str], list[str], list[str]]:
    spans: list[tuple[int, int, str | None]] = []
    for pattern in (URL_RE, NUMBER_RE):
        spans.extend((match.start(), match.end(), None) for match in pattern.finditer(text))
    spans.extend(date_spans(text, commas=not preserve_commas))
    if preserve_commas:
        spans.extend((match.start(), match.end(), None) for match in re.finditer(r",", text))
    # At one start the longest span wins, so "21 September 2026" masks as one
    # date rather than as the day 21.
    spans.sort(key=lambda span: (span[0], -span[1]))
    nonoverlap: list[tuple[int, int, str | None]] = []
    for span in spans:
        if nonoverlap and span[0] < nonoverlap[-1][1]:
            continue
        nonoverlap.append(span)
    out: list[str] = []
    tokens: list[str] = []
    literals: list[str] = []
    date_tokens: list[str] = []
    cursor = 0
    for index, (start, end, korean) in enumerate(nonoverlap):
        token = f"\u27e6ARA{index:04d}\u27e7"
        out.extend((text[cursor:start], token))
        tokens.append(token)
        literals.append(text[start:end] if korean is None else korean)
        if korean is not None:
            date_tokens.append(token)
        cursor = end
    out.append(text[cursor:])
    return "".join(out), tokens, literals, date_tokens


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
    masked, tokens, literals, date_tokens = _mask(decoded, preserve_commas=preserve_commas)
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
            date_tokens=tuple(date_tokens),
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
    lines = [
        json.dumps(
            {
                "version": manifest["version"],
                "segment_count": manifest["segment_count"],
            },
            separators=(",", ":"),
        )
    ]
    lines.extend(
        json.dumps(
            [
                segment["id"],
                segment["text"],
                1 if segment["forbid_commas"] else 0,
            ],
            ensure_ascii=False,
            separators=(",", ":"),
        )
        for segment in manifest["segments"]
    )
    _atomic_write(manifest_path, "\n".join(lines) + "\n")
    return manifest


_RESULT_LINE_RE = re.compile(
    r'\{"id"\s*:\s*"(?P<id>[^"]+)"\s*,\s*"text"\s*:\s*"(?P<text>.*)"\s*\}',
    re.DOTALL,
)


def _parse_result_objects(line: str) -> list[object]:
    """Parse one JSONL row, recovering Cursor Write leftovers.

    Accept a strict object, concatenated objects on one line, or a greedy
    {"id","text"} salvage when an unescaped quote makes json.loads see
    Extra data.
    """
    stripped = line.strip()
    if not stripped or not stripped.startswith("{"):
        return []
    try:
        return [json.loads(stripped)]
    except json.JSONDecodeError:
        pass
    decoder = json.JSONDecoder()
    objects: list[object] = []
    index = 0
    while index < len(stripped):
        while index < len(stripped) and stripped[index].isspace():
            index += 1
        if index >= len(stripped) or stripped[index] != "{":
            break
        try:
            value, end = decoder.raw_decode(stripped, index)
        except json.JSONDecodeError:
            break
        objects.append(value)
        index = end
    leftover = stripped[index:].strip() if objects else stripped
    if objects and leftover and not leftover.startswith("{"):
        # Unescaped quote closed the text early; take the greedy salvage.
        match = _RESULT_LINE_RE.search(stripped)
        if match:
            return [{"id": match.group("id"), "text": match.group("text")}]
    if objects:
        return objects
    match = _RESULT_LINE_RE.search(stripped)
    if match:
        return [{"id": match.group("id"), "text": match.group("text")}]
    return []


def _read_results(path: Path) -> dict[str, str]:
    if not path.is_file() or path.is_symlink() or path != RESULT_PATH:
        raise ValueError(f"translation result must be the regular file {RESULT_PATH}")
    translations: dict[str, str] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        # Cursor Write sometimes inserts blank lines or a non-object
        # separator between valid {"id","text"} rows. Coverage is still
        # checked after parse, so skipping junk cannot invent a segment.
        if not stripped or not stripped.startswith("{"):
            continue
        values = _parse_result_objects(stripped)
        if not values:
            preview = stripped[:80]
            raise ValueError(
                f"invalid translation result JSON on line {line_no}; preview={preview!r}"
            )
        for value in values:
            if not isinstance(value, dict) or set(value) != {"id", "text"}:
                raise ValueError(f"translation result line {line_no} has invalid fields")
            segment_id, text = value["id"], value["text"]
            if not isinstance(segment_id, str) or not isinstance(text, str) or not text.strip():
                raise ValueError(f"translation result line {line_no} has invalid id/text")
            translations[segment_id] = text
    return translations


def strip_unsafe_digits(text: str) -> str:
    """Drop leftover numeric literals while keeping tokens and 9일/3배 forms.

    Cursor writes a finished JSONL; unlike the OpenCode segment tool it does
    not reject leftover $2.5 / 30% / 2026 copies mid-flight. Those leftovers
    are not source literals (those are already ⟦ARA####⟧ tokens). Strip the
    whole NUMBER_RE match — not just the digits — so leftover `$` / `%` / `.`
    cannot glue onto a restored token and change the numeric-token multiset
    (`2.5` becoming `$2.5`).

    Digits are judged on the text with its tokens removed, exactly as the
    OpenCode segment tool judges them, so "가⟦ARA0001⟧-6월" keeps its range
    dash here whenever the tool would accept it.
    """
    prose: list[str] = []
    where: list[int] = []
    cursor = 0
    for token in [*TOKEN_RE.finditer(text), None]:
        stop = token.start() if token else len(text)
        prose.extend(text[cursor:stop])
        where.extend(range(cursor, stop))
        cursor = token.end() if token else stop
    joined = "".join(prose)
    keep = [True] * len(text)
    index = 0
    while index < len(joined):
        localized = LOCALIZED_INTEGER_RE.match(joined, index)
        if localized:
            index = localized.end()
            continue
        unsafe = NUMBER_RE.match(joined, index) or NUMBER_DEBRIS_RE.match(joined, index)
        if unsafe:
            for position in range(unsafe.start(), unsafe.end()):
                keep[where[position]] = False
            index = unsafe.end()
            continue
        index += 1
    return "".join(char for char, kept in zip(text, keep) if kept)


# A unit the model added after a token that is already a whole date, but
# not the first syllable of a word such as 월간, 월말, 일시, 일부, or 년도.
_DUPLICATE_DATE_UNIT_RE = re.compile(
    r"년(?![간대도차])|월(?!요일|[간말초급])|일(?!요일|부(?!터)|[시간정대반상련환제치])"
)
# Particles whose form depends on the final consonant before them, as
# (after a consonant, after a vowel). A one-syllable form that also begins
# ordinary words (나라, 다음, 고객, 면적, 가격, 이후) is fitted only before
# a word boundary. 으로/로 is separate: a final ㄹ or a vowel takes 로.
_PARTICLE_PAIRS = (
    ("이라는", "라는"), ("이라고", "라고"), ("이라며", "라며"), ("이라서", "라서"),
    ("이라도", "라도"), ("이라면", "라면"), ("이라니", "라니"), ("이야말로", "야말로"),
    ("이어서", "여서"), ("이어도", "여도"), ("이에요", "예요"), ("이지만", "지만"),
    ("이었", "였"), ("이며", "며"), ("은", "는"), ("을", "를"), ("과", "와"),
)
_BOUNDED_PARTICLE_PAIRS = (
    ("이나", "나"), ("이야", "야"), ("이란", "란"), ("이랑", "랑"),
    ("이다", "다"), ("이고", "고"), ("이면", "면"), ("이", "가"),
)


def fit_particle(final: str, tail: str) -> tuple[str, int]:
    """Refit the particle opening ``tail`` to a word ending in ``final``.

    Returns the particle to write and how many characters of ``tail`` it
    replaces; ("", 0) when ``tail`` opens with no particle.
    """
    if not "가" <= final <= "힣":
        return "", 0
    batchim = (ord(final) - 0xAC00) % 28
    for after_consonant, after_vowel in _PARTICLE_PAIRS:
        for written in (after_consonant, after_vowel):
            if tail.startswith(written):
                return (after_consonant if batchim else after_vowel), len(written)
    for after_consonant, after_vowel in _BOUNDED_PARTICLE_PAIRS:
        for written in (after_consonant, after_vowel):
            following = tail[len(written) : len(written) + 1]
            if tail.startswith(written) and not ("가" <= following <= "힣"):
                return (after_consonant if batchim else after_vowel), len(written)
    for written in ("으로", "로"):
        if tail.startswith(written):
            # ㄹ (batchim 8) takes 로 like a vowel.
            return ("으로" if batchim and batchim != 8 else "로"), len(written)
    return "", 0


def attach_korean_date(text: str, token: str, korean: str) -> str:
    """Replace a date token and fit the model's suffix to the hidden date.

    The model cannot see that a token is a whole date, so it may write the
    unit a bare year needs (⟦ARA0000⟧년에) or a particle chosen for a number
    that ends in a vowel (⟦ARA0000⟧는, ⟦ARA0000⟧라는).
    """
    index = text.find(token)
    if index < 0:
        return text
    tail = text[index + len(token) :]
    if _DUPLICATE_DATE_UNIT_RE.match(tail):
        tail = tail[1:]
    fitted, consumed = fit_particle(korean[-1], tail)
    return text[:index] + korean + fitted + tail[consumed:]


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
        # Korean word order may swap two numbers in one clause. Identity
        # replacement below still maps each token to its source literal.
        if collections.Counter(found_tokens) != collections.Counter(segment.tokens):
            raise ValueError(
                f"translation segment {segment.id} changed immutable tokens; "
                f"expected={segment.tokens}, got={found_tokens}"
            )
        translated = strip_unsafe_digits(translated)
        prose_without_tokens = TOKEN_RE.sub("", translated)
        if re.search(r"[0-9]", LOCALIZED_INTEGER_RE.sub("", prose_without_tokens)):
            raise ValueError(
                f"translation segment {segment.id} added an unsafe localized "
                "numeric token"
            )
        if segment.forbid_commas and "," in translated:
            raise ValueError(
                f"translation segment {segment.id} added an unprotected list separator"
            )
        for token, literal in zip(segment.tokens, segment.literals, strict=True):
            if token in segment.date_tokens:
                translated = attach_korean_date(translated, token, literal)
            else:
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
