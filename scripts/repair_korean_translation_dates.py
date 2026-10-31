#!/usr/bin/env python3
"""Repair garbled dates and signs in published Korean generative-research translations.

Each published ``.ko.html`` is its English ARA source compiled to HTML with
the text runs and translatable attribute values replaced, so the k-th run of
one aligns with the k-th run of the other. Every English calendar date the
translation pipeline recognizes (``generative_translation_segments``) was a
set of opaque tokens, so its exact source digits sit somewhere in the aligned
Korean run. This script finds the Korean phrase that holds exactly those
digits, decides how it was garbled, and rewrites it to the pipeline's own
Korean rendering of the English date. Every rewrite is parsed back and must
name the same year, months, and days as the English date; anything that does
not bind uniquely is listed, never guessed.

Classes (select with ``--classes``):

  A  factual: a month outside 1-12 or a day/year carrying the wrong unit
     ("29월 2026" for "October 29, 2026", "21년 2026월", "2025월"), plus a
     short hand-checked list of months the old renderer or model dropped.
  B  format: every number and the right month present but English word order
     or a missing unit ("10월 26, 2026", "4월 2026", "10일 7월 2026",
     "2일(2026년 8월)", "5월 말 2026", "유월 2026"), or an English date left
     untranslated, or a range's shared year left mid-range. B skips and lists
     dates in quotes, in titles of other works (reference entries, <cite>),
     and in URLs.
  B also writes a range the repair itself produced with the Korean wave
     dash ("2026년 7월 17-20일" becomes "2026년 7월 17~20일") when given
     ``--touched-since REV``: only spans that differ from REV change, so a
     range the translation wrote and the repair never touched stays as is.
  S  stray minus: a number the English glued to a word by a hyphen
     ("mid-60s", "7-of-10", "mid-2026") that the Korean prints as a negative
     ("-60대 중반", "7/-10", "-2026년 중반"), because the old masking made
     the hyphen part of the opaque token.

The script reads the working tree and is idempotent: a second run finds
nothing. ``--write`` applies the selected classes and refuses to write unless
each file is byte-identical to the original outside the rewritten spans.
"""

from __future__ import annotations

import argparse
import collections
import csv
import difflib
import hashlib
import html
import json
import random
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import generative_translation_segments as segments
from check_generative_translation import URL_RE
from compile_ara import compile_source

ROOT = Path(__file__).resolve().parent.parent
LIST_ATTRS = frozenset({"data-categories", "data-items", "data-labels", "data-x-labels"})
VOID_TAGS = frozenset(
    {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param",
     "source", "track", "wbr"}
)
TITLE_TAGS = frozenset({"cite"})  # <em> and <i> are emphasis in these articles
QUOTE_TAGS = frozenset({"blockquote", "q"})
QUOTE_PAIRS = (("「", "」"), ("『", "』"), ("“", "”"), ("‘", "’"))
HANGUL_MONTHS = {
    "십일월": 11, "십이월": 12, "일월": 1, "이월": 2, "삼월": 3, "사월": 4,
    "오월": 5, "유월": 6, "칠월": 7, "팔월": 8, "구월": 9, "시월": 10,
}
_HANGUL_MONTH = "|".join(sorted(HANGUL_MONTHS, key=len, reverse=True))
# A Korean number atom: digits with an optional date unit, or a Hangul month
# word. In prose a comma before a digit is a thousands mark; in a list
# attribute it separates labels.
ATOM_RE = {
    commas: re.compile(
        rf"(?<![0-9{'.,' if commas else '.'}A-Za-z_$€£₩¥+−#&])(?<![A-Za-z]-)"
        rf"(?:([0-9]+)(?![0-9])(?![{'.,' if commas else '.'}][0-9])([년월일])?(?![A-Za-z%×])"
        rf"|(?<![가-힣])({_HANGUL_MONTH}))"
    )
    for commas in (True, False)
}
GAP_RE = {
    True: re.compile(r"\s*(?:[,–—~\-]|과|와|및)?\s*"),
    False: re.compile(r"\s*(?:[–—~\-]|과|와|및)?\s*"),
}
DASH_RE = re.compile(r"[–—~\-]")
RANGE_GAP_RE = re.compile(r"\s*[–—~\-]\s*")
KOREAN_PART_RE = re.compile(rf"([0-9]+)(?:([년월일])|(?=\s*[–—~\-]\s*[0-9]+일))|({_HANGUL_MONTH})")
QUALIFIERS = "초순|상순|중순|하순|상반기|하반기|초|말|경"
HANGUL_RE = re.compile(r"[가-힣]")
RANGE_FORMS = frozenset({"cross_md", "cross_dm", "month_range"})
# How the old masking read a sign: any hyphen before a number.
SIGNED_NUMBER_RE = re.compile(
    r"(?<!\d)-((?:[$€£₩¥]\s*)?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:%|×|x)?)(?!\d)"
)
WORD_CHAR_RE = re.compile(r"[A-Za-z가-힣]")
# Two month names joined as a range with no year ("the March-June window",
# "the September-to-October comparison"), which no date form covers.
BARE_MONTH_RANGE_RE = re.compile(
    rf"(?P<m>{segments._MONTH})(?:\s*[–—-]\s*|-to-|\s+to\s+|\s+through\s+)(?P<m2>{segments._MONTH})"
)
RANGE_DASH = r"\s*[–—~-]\s*"

# Hand-checked against the English source: months the old renderer stripped
# ("4월-6월" lost "-6" to strip_unsafe_digits) or the model dropped, which no
# rule can bind. (file prefix, unique needle, old, new, English, expected).
MANUAL_A = (
    ("2026-08-18T125414", "패널, –6월 2023)", "–6월 2023", "2023년 5월–6월",
     "May–June 2023", ("2023", (5, 6), ())),
    ("2026-08-18T125414", "베이스라인(–6월 2023 수집", "–6월 2023", "2023년 5월–6월",
     "May–June 2023", ("2023", (5, 6), ())),
    ("2026-08-19T005028", "5월월 2025년", "5월월 2025년", "2025년 5월–6월",
     "May-June 2025", ("2025", (5, 6), ())),
    ("2026-08-19T012518", "미감사 (4월월 2026)", "4월월 2026", "2026년 4월–6월",
     "Apr-Jun 2026", ("2026", (4, 6), ())),
    ("2026-08-19T012518", "투자자 출처; 4월월 2026 범위", "4월월 2026", "2026년 4월–6월",
     "Apr-Jun 2026", ("2026", (4, 6), ())),
    ("2026-09-25T150648", "테스트인 4월월 2024 상환", "4월월 2024", "2024년 4월–5월",
     "April-May 2024", ("2024", (4, 5), ())),
    ("2026-09-25T150648", "(8월월 2025)", "8월월 2025", "2025년 8월–9월",
     "August-September 2025", ("2025", (8, 9), ())),
    ("2026-09-25T150648", "(3월월 창)", "3월월", "3월–6월",
     "in the March-June window", (None, (3, 6), ())),
    ("2026-10-17T115206", "9월월 비교는", "9월월", "9월–10월",
     "the September-to-October comparison", (None, (9, 10), ())),
    ("2026-08-18T063812", "라운드를 2026년 –10월에", "2026년 –10월", "2026년 9월–10월",
     "September–October 2026", ("2026", (9, 10), ())),
    ("2026-08-18T063812", "보도상 2026년 –10월에", "2026년 –10월", "2026년 9월–10월",
     "September–October 2026", ("2026", (9, 10), ())),
    ("2026-10-31T110143", "가치로 2025에 조달", "2025에", "2025년 10월에",
     "in October 2025", ("2025", (10,), ())),
    ("2026-08-19T005028", "딥시크월-2025-대-지금", "딥시크월-2025", "딥시크-2025년 1월",
     "DeepSeek-January-2025-versus-now", ("2025", (1,), ())),
    # "Oct 30, 22:52 EST": the hour took 일 and the colon was lost.
    ("2026-10-31T125431", "30 10월 22일, 52 미 동부시간", "30 10월 22일, 52", "10월 30일 22:52",
     "Oct 30, 22:52 EST", (None, (10,), ("30",))),
    # "by July 20, 2026": the model moved the year to the sentence end.
    ("2026-08-19T001711", "$268.90(20년 7월)에", "20년 7월", "2026년 7월 20일",
     "by July 20, 2026", ("2026", (7,), ("20",))),
    ("2026-08-19T001711", "분기 이후 2026이다.", " 2026이다", "다",
     "by July 20, 2026 (displaced year)", None),
)


@dataclass(frozen=True)
class Unit:
    kind: str
    key: str
    start: int
    end: int
    contexts: frozenset[str]


@dataclass(frozen=True)
class Atom:
    start: int
    end: int
    digits: str
    unit: str | None
    word: bool = False  # a Hangul month word is only ever a month


@dataclass(frozen=True)
class Edit:
    start: int
    end: int
    after: str
    cls: str
    rule: str
    english: str
    expected: tuple | None
    flags: str = ""


@dataclass
class Change:
    file: str
    unit: str
    cls: str
    rule: str
    flags: str
    start: int
    end: int
    before: str
    after: str
    english: str
    context: str


@dataclass
class Report:
    changes: list[Change] = field(default_factory=list)
    unresolved: list[dict] = field(default_factory=list)

    def skip(self, file: str, unit: str, reason: str, english: str, korean: str) -> None:
        self.unresolved.append(
            {"file": file, "unit": unit, "reason": reason, "english": english, "korean": korean}
        )


def units(doc: str) -> list[Unit]:
    """Text runs and translatable attribute values with their element context."""
    out: list[Unit] = []
    stack: list[tuple[str, str, str]] = []
    excluded: list[str] = []
    cursor = 0

    def contexts() -> frozenset[str]:
        found = set()
        for name, classes, ident in stack:
            if name == "li" and ident.startswith("ref-"):
                found.add("reference")
            if name in TITLE_TAGS:
                found.add("title")
            if name in QUOTE_TAGS or "ara-quote" in classes.split():
                found.add("quote")
        if any("ara-quote-attr" in classes.split() for _, classes, _ in stack):
            found.discard("quote")  # an attribution is not quoted text
        return frozenset(found)

    for tag_start, tag_end in segments._tag_spans(doc):
        if tag_start > cursor and not excluded:
            out.append(Unit("text", "", cursor, tag_start, contexts()))
        tag = doc[tag_start:tag_end]
        match = segments.TAG_NAME_RE.match(tag)
        name = match.group(2).lower() if match else ""
        closing = bool(match and match.group(1))
        attrs = {
            attr.group(1).lower(): (attr.start(3), attr.end(3), attr.group(3))
            for attr in segments.ATTR_RE.finditer(tag)
        }
        if not excluded and not closing and not tag.startswith("<!"):
            for key, (value_start, value_end, _) in attrs.items():
                if key in segments.TRANSLATABLE_ATTRS or segments.SERIES_LABEL_RE.fullmatch(key):
                    out.append(
                        Unit("attr", key, tag_start + value_start, tag_start + value_end, contexts())
                    )
        if name in segments.EXCLUDED_TAGS:
            if closing:
                if excluded and excluded[-1] == name:
                    excluded.pop()
            elif not tag.rstrip().endswith("/>"):
                excluded.append(name)
        if match and not tag.startswith("<!"):
            if closing:
                for depth in range(len(stack) - 1, -1, -1):
                    if stack[depth][0] == name:
                        del stack[depth:]
                        break
            elif name not in VOID_TAGS and not tag.rstrip().endswith("/>"):
                classes = attrs.get("class", (0, 0, ""))[2]
                ident = attrs.get("id", (0, 0, ""))[2]
                stack.append((name, classes, ident))
        cursor = tag_end
    if cursor < len(doc) and not excluded:
        out.append(Unit("text", "", cursor, len(doc), contexts()))
    return [unit for unit in out if doc[unit.start : unit.end].strip()]


def english_components(form: str, match: re.Match[str]) -> tuple:
    """(year, months, days) read straight from the English match."""
    groups = match.groupdict()
    months = [segments._month_number(groups["m"])]
    if groups.get("m2"):
        months.append(segments._month_number(groups["m2"]))
    if form == "day_list":
        days = re.findall(r"[0-9]+", groups["days"])
    else:
        days = [groups[name] for name in ("d", "d2") if groups.get(name)]
    return (groups.get("y"), tuple(months), tuple(days))


def range_components(english: str, rendered, k: int) -> tuple:
    """English (year, months, days) for the k-th date, with a range's year.

    A date borrows the next date's year, or gives its own to the date
    before, only across a range join in the English source.
    """
    form, match, _ = rendered[k]
    year, months, days = english_components(form, match)
    def joined(a: int, b: int) -> bool:
        first, second = rendered[a][1], rendered[b][1]
        last_month = segments._month_number(first.groupdict().get("m2") or first["m"])
        return bool(
            segments._RANGE_JOIN_RE.fullmatch(english[first.end() : second.start()])
            and last_month <= segments._month_number(second["m"])
        )

    borrow = (
        k + 1 < len(rendered) and not year and rendered[k + 1][1].groupdict().get("y")
        and joined(k, k + 1)
    )
    lend = k > 0 and year and not rendered[k - 1][1].groupdict().get("y") and joined(k - 1, k)
    if borrow:
        year = rendered[k + 1][1]["y"]
    elif lend:
        year = None
    return (year, months, days)


def korean_components(text: str) -> tuple:
    """(year, months, days) read back from a Korean date phrase."""
    year, months, days = None, [], []
    for match in KOREAN_PART_RE.finditer(text):
        digits, unit, word = match.groups()
        if word:
            months.append(HANGUL_MONTHS[word])
        elif unit == "년":
            year = digits
        elif unit == "월":
            months.append(int(digits))
        else:
            days.append(digits)
    return (year, tuple(months), tuple(days))


def atoms_of(korean: str, commas: bool) -> list[Atom]:
    out = []
    for match in ATOM_RE[commas].finditer(korean):
        if match.group(3):
            out.append(Atom(match.start(), match.end(), str(HANGUL_MONTHS[match.group(3)]), "월", True))
        else:
            out.append(Atom(match.start(), match.end(), match.group(1), match.group(2)))
    return out


def assign(atoms: list[Atom], required, months: tuple[int, ...], blocked: set[int]):
    """Give every atom a role: this date's month, or one of its source digits.

    N월 naming this date's month is always that month; N월 naming another
    month the run mentions is that month, so it is never a misread day.
    """
    need = collections.Counter(required)
    month_left = collections.Counter(months)
    roles: list[tuple[str, object]] = []

    def rec(k: int) -> bool:
        if k == len(atoms):
            return not +need
        atom = atoms[k]
        value = int(atom.digits)
        if atom.unit == "월" and (value in month_left or atom.word):
            if month_left[value] <= 0:
                return False
            month_left[value] -= 1
            roles.append(("month", value))
            if rec(k + 1):
                return True
            roles.pop()
            month_left[value] += 1
            return False
        if atom.unit == "월" and 1 <= value <= 12 and value in blocked:
            return False
        for role in ("day", "year"):
            if need[(atom.digits, role)] > 0:
                need[(atom.digits, role)] -= 1
                roles.append((role, atom.digits))
                if rec(k + 1):
                    return True
                roles.pop()
                need[(atom.digits, role)] += 1
        return False

    return list(roles) if rec(0) else None


def windows(text: str, atoms: list[Atom], required, months, blocked: set[int], commas: bool):
    """Maximal runs of atoms holding exactly one date's digits."""
    found = []
    for i in range(len(atoms)):
        for j in range(i, min(len(atoms), i + 12)):
            gap = text[atoms[j - 1].end : atoms[j].start] if j > i else ""
            if j > i and not GAP_RE[commas].fullmatch(gap):
                break
            # Inside one date a comma only sits between a day and a year
            # ("10월 26, 2026") and a dash never follows a year: after a year
            # or before a month they separate two dates ("5월 중순 2025, 5월
            # 말 2025", "8월 2025 – 8월 2026").
            if j > i and len(atoms[j - 1].digits) == 4 and ("," in gap or DASH_RE.search(gap)):
                break
            if j > i and "," in gap and atoms[j].unit == "월":
                break
            roles = assign(atoms[i : j + 1], required, months, blocked)
            if roles is not None:
                found.append((i, j, roles))
    return [
        (i, j, roles)
        for i, j, roles in found
        if not any((a, b) != (i, j) and a <= i and j <= b for a, b, _ in found)
    ]


def classify(text: str, atoms: list[Atom], roles, months) -> str | None:
    """Return 'A', 'B', a reason to list it, or None for acceptable Korean."""
    pairs = list(zip(atoms, roles))
    misstated = any(
        (role == "day" and atom.unit not in (None, "일"))
        or (role == "year" and atom.unit not in (None, "년"))
        for atom, (role, _) in pairs
    )
    if misstated:
        if len(atoms) == 1:
            atom = atoms[0]
            # One atom binds only when it cannot be a real Korean date part:
            # an impossible month, or a year with 월/일.
            impossible = atom.unit == "월" and not 1 <= int(atom.digits) <= 12
            year_unit = len(atom.digits) == 4 and atom.unit in {"월", "일"}
            if not (impossible or year_unit):
                return "lone number too weak to bind"
        return "A"
    have = collections.Counter(value for role, value in roles if role == "month")
    if collections.Counter(months) - have:
        # The month may sit outside the window (an English month left in
        # place, a dropped range end), so a person decides.
        return "month left implicit" if all(atom.unit for atom in atoms) else "month missing"
    kinds = [role for role, _ in roles]
    first_other = next((k for k, kind in enumerate(kinds) if kind != "year"), len(kinds))
    year_late = "year" in kinds[first_other:]
    day_first = first_other < len(kinds) and kinds[first_other] == "day"
    bare_day = any(
        role == "day"
        and atom.unit is None
        and not (
            k + 1 < len(pairs)
            and pairs[k + 1][1][0] == "day"
            and RANGE_GAP_RE.fullmatch(text[atom.end : pairs[k + 1][0].start])
        )
        for k, (atom, (role, _)) in enumerate(pairs)
    )
    bare_year = any(role == "year" and atom.unit is None for atom, (role, _) in pairs)
    return "B" if (year_late or day_first or bare_day or bare_year) else None


def fit_particle(phrase: str, tail: str) -> tuple[str, int]:
    """Particle agreeing with the phrase's final syllable: (text, consumed)."""
    return segments.fit_particle(phrase[-1], tail)


def inside_quotes(run: str, start: int) -> bool:
    before = run[:start]
    if any(before.count(opener) > before.count(closer) for opener, closer in QUOTE_PAIRS):
        return True
    return (before.count('"') + before.count("&quot;")) % 2 == 1


def plan_run(
    report: Report, name: str, unit: Unit, english_raw: str, korean: str,
    touched: list[tuple[int, int]] | None = None,
) -> list[Edit]:
    """Edits inside one aligned run; offsets are relative to the run.

    ``touched`` lists the run's spans that changed since a revision; the
    range-dash rule only runs inside them.
    """
    label = f"attr {unit.key}" if unit.kind == "attr" else "text"
    commas = unit.key not in LIST_ATTRS
    english = html.unescape(english_raw)
    rendered = segments.korean_dates(english, commas=commas)
    dates = [(form, match) for form, match, _ in rendered]
    if not dates and not (touched is not None and BARE_MONTH_RANGE_RE.search(english)):
        return []
    groups: dict[str, list[tuple[str, re.Match[str]]]] = collections.defaultdict(list)
    expected_of: dict[str, tuple] = {}
    for k, (form, match, canon) in enumerate(rendered):
        groups[canon].append((form, match))
        expected_of[canon] = range_components(english, rendered, k)
    covered = [(match.start(), match.end()) for _, match in dates]
    run_months = {
        segments._month_number(m.group())
        for m in re.finditer(rf"(?<![A-Za-z]){segments._MONTH}", english)
        if not any(s <= m.start() < e for s, e in covered)
    }
    run_years = set()
    for form, match in dates:
        year, months, _ = english_components(form, match)
        run_months.update(months)
        if year:
            run_years.add(year)
    urls = [(m.start(), m.end()) for m in URL_RE.finditer(korean)]
    edits: list[Edit] = []
    held: list[tuple[int, int]] = []  # spans deliberately left as they are
    handled: collections.Counter[str] = collections.Counter()

    def taken(start: int, end: int) -> bool:
        return any(start < e and s < end for s, e in [*((x.start, x.end) for x in edits), *held])

    def propose(edit: Edit, canon: str, form: str, match: re.Match[str]) -> None:
        handled[canon] += 1
        flags = set(unit.contexts)
        if inside_quotes(korean, edit.start):
            flags.add("quote")
        if form in RANGE_FORMS or match.groupdict().get("d2"):
            flags.add("range")
        if any(edit.start < e and s < edit.end for s, e in urls):
            held.append((edit.start, edit.end))
            report.skip(name, label, "inside a URL", edit.english, korean[edit.start : edit.end])
            return
        skipped = flags - {"range"}  # a range is rewritten, and flagged for review
        if edit.cls == "B" and skipped:
            held.append((edit.start, edit.end))
            report.skip(name, label, f"B skips dates in a {'/'.join(sorted(skipped))}",
                        edit.english, korean[max(0, edit.start - 16) : edit.end + 12])
            return
        edits.append(Edit(edit.start, edit.end, edit.after, edit.cls, edit.rule, edit.english,
                          edit.expected, ";".join(sorted(flags))))

    # An English date the translation left in place, in Korean prose or in a
    # run with no English prose ("12 Aug · 15:00").
    for form, match, canon in segments.korean_dates(korean, commas=commas):
        rest = korean[: match.start()] + korean[match.end() :]
        prose = re.findall(r"\b[a-z]{2,}\b", re.sub(r"@\w+|https?://\S+", "", rest))
        if canon in groups and not taken(*match.span()) and (HANGUL_RE.search(korean) or not prose):
            fitted, consumed = fit_particle(canon, korean[match.end() :])
            propose(Edit(match.start(), match.end() + consumed, canon + fitted, "B",
                         "untranslated English date", match.group(),
                         expected_of[canon]), canon, form, match)
    # "2026년 May 7일" kept the English month name in Korean order.
    for match in re.finditer(
        rf"(?<![0-9])((?:1[89]|2[01])[0-9]{{2}})년 ({segments._MONTH})(?: ([0-9]{{1,2}})일)?", korean
    ):
        year, word, day = match.groups()
        canon = f"{year}년 {segments._month_number(word)}월" + (f" {day}일" if day else "")
        if canon in groups and not taken(*match.span()):
            form, english_match = groups[canon][0]
            propose(Edit(match.start(), match.end(), canon, "B", "English month name",
                         english[english_match.start() : english_match.end()],
                         expected_of[canon]), canon, form, english_match)

    # A range whose shared year sits mid-range ("9월 10일부터 2026년 10월
    # 초까지"): move it to the front, as the pipeline now renders it.
    for k in range(len(rendered) - 1):
        (first_form, first, first_canon), (second_form, second, second_canon) = rendered[k], rendered[k + 1]
        old_first = segments.korean_date(first_form, first)
        old_second = segments.korean_date(second_form, second)
        if (old_first, old_second) == (first_canon, second_canon):
            continue
        pattern = rf"(?<![0-9]년 )(?<![0-9]){re.escape(old_first)}([^0-9<]{{0,16}}?){re.escape(old_second)}"
        for found in re.finditer(pattern, korean):
            start2 = found.start() + len(old_first) + len(found.group(1))
            if taken(found.start(), found.end()):
                continue
            english_pair = english[first.start() : second.end()]
            propose(Edit(found.start(), found.start() + len(old_first), first_canon, "B", "range year",
                         english_pair, expected_of[first_canon]), first_canon, first_form, first)
            propose(Edit(start2, start2 + len(old_second), second_canon, "B", "range year",
                         english_pair, expected_of[second_canon]), second_canon, second_form, second)

    # A range the repair wrote with a dash takes the wave dash the pipeline
    # now writes ("10월 26–27일" becomes "10월 26~27일").
    if touched is not None:
        def touches(start: int, end: int) -> bool:
            return any(start < e and s < end if s < e else start <= s <= end for s, e in touched)

        ranges = [(canon, form, match, expected_of[canon]) for form, match, canon in rendered if "~" in canon]
        for bare in BARE_MONTH_RANGE_RE.finditer(english):
            if any(bare.start() < match.end() and match.start() < bare.end() for _, match in dates):
                continue  # inside a dated range, which the line above covers
            months = (segments._month_number(bare["m"]), segments._month_number(bare["m2"]))
            ranges.append((f"{months[0]}월~{months[1]}월", None, bare, (None, months, ())))
        for canon, form, match, expected in ranges:
            pattern = RANGE_DASH.join(re.escape(part) for part in canon.split("~"))
            for found in re.finditer(rf"(?<![0-9]){pattern}(?![0-9])", korean):
                if found.group() == canon or taken(*found.span()) or not touches(*found.span()):
                    continue
                propose(Edit(found.start(), found.end(), canon, "B", "range dash",
                             english[match.start() : match.end()], expected),
                        canon, form or "month_range", match)

    # A rendered date followed by a particle fitted to some other final
    # syllable ("2025년 11월나" for 이나).
    for canon, members in groups.items():
        form, match = members[0]
        for found in re.finditer(rf"(?<![0-9]){re.escape(canon)}", korean):
            fitted, consumed = fit_particle(canon, korean[found.end() :])
            written = korean[found.end() : found.end() + consumed]
            if consumed and fitted != written and not taken(found.end(), found.end() + consumed):
                propose(Edit(found.end(), found.end() + consumed, fitted, "B", "particle",
                             english[match.start() : match.end()], ("particle", canon[-1])),
                        canon, form, match)
                handled[canon] -= 1  # the date itself still needs its own check

    atoms = atoms_of(korean, commas)
    claims: dict[tuple[int, int], set[str]] = collections.defaultdict(set)
    plans = []
    for canon, members in groups.items():
        form, match = members[0]
        english_phrase = english[match.start() : match.end()]
        expected = expected_of[canon]
        year, months, days = expected
        # "2일(2026년 8월)" holds every part of "2 August 2026".
        if year and len(months) == 1 and len(days) == 1:
            for found in re.finditer(rf"(?<![0-9]){days[0]}일\({year}년 {months[0]}월\)", korean):
                if not taken(*found.span()):
                    propose(Edit(found.start(), found.end(), canon, "B", "day(year month)",
                                 english_phrase, expected), canon, form, match)
        # "5월 말 2026" keeps its qualifier in front of the year.
        if year and len(months) == 1 and not days:
            for found in re.finditer(
                rf"(?<![0-9]){months[0]}월(\s*)({QUALIFIERS})\s*{year}(?:년)?(?![0-9])", korean
            ):
                if taken(*found.span()):
                    continue
                phrase = f"{year}년 {months[0]}월{found.group(1)}{found.group(2)}"
                fitted, consumed = fit_particle(phrase, korean[found.end() :])
                propose(Edit(found.start(), found.end() + consumed, phrase + fitted, "B",
                             "qualifier", english_phrase, expected), canon, form, match)
        if handled[canon] >= len(members):
            continue
        required = collections.Counter()
        for digits in days:
            required[(digits, "day")] += 1
        if year:
            required[(year, "year")] += 1
        cands = [
            cand
            for cand in windows(korean, atoms, required, months, run_months - set(months), commas)
            if not taken(atoms[cand[0]].start, atoms[cand[1]].end)
        ]
        if not cands:
            if not handled[canon]:
                report.skip(name, label, "no Korean phrase holds the date's digits",
                            english_phrase, korean[:160])
            continue
        if len(cands) > len(members):
            # A window holding every number and month of the date is that
            # date; a partial one elsewhere is a coincidence of digits.
            complete = [
                cand for cand in cands
                if not collections.Counter(months)
                - collections.Counter(value for role, value in cand[2] if role == "month")
            ]
            if not 1 <= len(complete) <= len(members):
                report.skip(name, label, f"{len(cands)} candidate phrases for {len(members)} date(s)",
                            english_phrase,
                            " | ".join(korean[atoms[i].start : atoms[j].end] for i, j, _ in cands))
                continue
            cands = complete
        for i, j, roles in cands:
            claims[(i, j)].add(canon)
            plans.append((canon, form, match, english_phrase, expected, i, j, roles))
    for canon, form, match, english_phrase, expected, i, j, roles in plans:
        window = atoms[i : j + 1]
        if len({other for (a, b), canons in claims.items() for other in canons if not (b < i or a > j)}) > 1:
            report.skip(name, label, "phrase claimed by two dates", english_phrase,
                        korean[window[0].start : window[-1].end])
            continue
        cls = classify(korean, window, roles, expected[1])
        if cls is None:
            continue
        if cls not in {"A", "B"}:
            report.skip(name, label, cls, english_phrase,
                        korean[max(0, window[0].start - 16) : window[-1].end + 12])
            continue
        # A neighbour joined by a date gap conflicts when it names a month or
        # year no date in the run uses (11월 26일 for "October 26").
        conflict = False
        for k in (i - 1, j + 1):
            if not 0 <= k < len(atoms):
                continue
            gap = korean[atoms[k].end : window[0].start] if k < i else korean[window[-1].end : atoms[k].start]
            atom = atoms[k]
            if GAP_RE[commas].fullmatch(gap) and (
                (atom.unit == "월" and int(atom.digits) not in run_months)
                or (atom.unit == "년" and atom.digits not in run_years)
            ):
                conflict = True
        if conflict:
            report.skip(name, label, "an adjacent dated number belongs to no source date",
                        english_phrase, korean[max(0, window[0].start - 12) : window[-1].end + 12])
            continue
        fitted, consumed = fit_particle(canon, korean[window[-1].end :])
        propose(Edit(window[0].start, window[-1].end + consumed, canon + fitted, cls, "phrase",
                     english_phrase, expected), canon, form, match)
    return edits


def plan_signs(report: Report, name: str, unit: Unit, english_raw: str, korean: str) -> list[Edit]:
    """Stray minus signs inside one aligned run (offsets relative to it).

    A minus is stray when the English glued that number to a word with a
    hyphen and the Korean prints it as a negative standing alone. When the
    English also has a genuine negative of the same number, or the Korean
    has more negatives than the English has compounds, a person decides.
    """
    label = f"attr {unit.key}" if unit.kind == "attr" else "text"
    english = html.unescape(english_raw)

    def kinds(text: str):
        glued, standalone = collections.defaultdict(list), collections.defaultdict(list)
        for match in SIGNED_NUMBER_RE.finditer(text):
            previous = text[match.start() - 1] if match.start() else ""
            (glued if WORD_CHAR_RE.fullmatch(previous) else standalone)[match.group(1)].append(match)
        return glued, standalone

    english_glued, english_negative = kinds(english)
    _, korean_negative = kinds(korean)
    edits = []
    for literal, matches in korean_negative.items():
        compounds = len(english_glued.get(literal, []))
        if not compounds:
            continue
        if english_negative.get(literal) or len(matches) > compounds:
            report.skip(name, label, "a negative number may be genuine",
                        f"-{literal} glued to a word {compounds}x", korean[:160])
            continue
        for match in matches:
            edits.append(Edit(match.start(), match.start() + 1, "", "S", "stray minus",
                              f"…-{literal} (a hyphenated compound)", None))
    return edits


def verify(edit: Edit, before: str) -> None:
    """Parse the rewrite back; it must name exactly the English date."""
    if edit.rule == "particle":
        final = edit.expected[1]
        if segments.fit_particle(final, before) != (edit.after, len(before)) or before == edit.after:
            raise SystemExit(f"particle edit {before!r} -> {edit.after!r} does not fit {final!r}")
        return
    if edit.cls == "S":
        if before != "-" or edit.after:
            raise SystemExit(f"stray-minus edit must remove one hyphen, not {before!r}")
        return
    if edit.expected is None:
        return
    got = korean_components(edit.after)
    if got != edit.expected:
        raise SystemExit(
            f"parse-back mismatch for {before!r} -> {edit.after!r}: {got} != {edit.expected} "
            f"({edit.english})"
        )


def apply(text: str, edits: list[tuple[int, int, str]]) -> str:
    out, cursor = [], 0
    for start, end, after in sorted(edits):
        if start < cursor:
            raise SystemExit(f"overlapping edits at {start}")
        out.extend((text[cursor:start], after))
        cursor = end
    out.append(text[cursor:])
    return "".join(out)


def masked(text: str, spans: list[tuple[int, int]]) -> str:
    out, cursor = [], 0
    for start, end in sorted(spans):
        out.extend((text[cursor:start], "\0"))
        cursor = end
    out.append(text[cursor:])
    return "".join(out)


def assert_identical_outside(old: str, new: str, edits: list[tuple[int, int, str]], file: str) -> None:
    """Byte-identity outside the rewritten spans, by masking them on both sides."""
    new_spans, shift = [], 0
    for start, end, after in sorted(edits):
        new_spans.append((start + shift, start + shift + len(after)))
        shift += len(after) - (end - start)
    if masked(old, [(s, e) for s, e, _ in edits]) != masked(new, new_spans):
        raise SystemExit(f"{file}: text changed outside the rewritten date spans")


def run_spans(spans: list[tuple[int, int]] | None, unit: Unit) -> list[tuple[int, int]] | None:
    """The file's changed spans that fall in one run, relative to it."""
    if spans is None:
        return None
    inside = []
    for start, end in spans:
        if start < unit.end and unit.start < end or (start == end and unit.start <= start <= unit.end):
            inside.append((max(start, unit.start) - unit.start, min(end, unit.end) - unit.start))
    return inside


def changed_spans(old: str, new: str) -> list[tuple[int, int]]:
    """Spans of ``new`` that differ from ``old``; a deletion is a point."""
    spans = []
    old_lines, new_lines = old.splitlines(keepends=True), new.splitlines(keepends=True)
    starts = [0]
    for line in new_lines:
        starts.append(starts[-1] + len(line))
    lines = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
    for tag, i1, i2, j1, j2 in lines.get_opcodes():
        if tag == "equal":
            continue
        before, after = "".join(old_lines[i1:i2]), "".join(new_lines[j1:j2])
        chars = difflib.SequenceMatcher(None, before, after, autojunk=False)
        for tag2, _, _, k1, k2 in chars.get_opcodes():
            if tag2 != "equal":
                spans.append((starts[j1] + k1, starts[j1] + k2))
    return spans


def plan_document(
    report: Report, file: str, source_html: str, korean: str,
    touched: list[tuple[int, int]] | None = None,
) -> list[Change] | None:
    source_units, korean_units = units(source_html), units(korean)
    if [(u.kind, u.key) for u in source_units] != [(u.kind, u.key) for u in korean_units]:
        report.skip(file, "-", "runs do not align with the source", "", "")
        return None
    changes = []
    for source_unit, korean_unit in zip(source_units, korean_units, strict=True):
        run = korean[korean_unit.start : korean_unit.end]
        label = f"attr {korean_unit.key}" if korean_unit.kind == "attr" else "text"
        english_run = source_html[source_unit.start : source_unit.end]
        dated = plan_run(report, file, korean_unit, english_run, run, run_spans(touched, korean_unit))
        signs = [
            edit for edit in plan_signs(report, file, korean_unit, english_run, run)
            if not any(edit.start < other.end and other.start < edit.end for other in dated)
        ]
        for edit in dated + signs:
            start, end = korean_unit.start + edit.start, korean_unit.start + edit.end
            verify(edit, korean[start:end])
            changes.append(Change(file, label, edit.cls, edit.rule, edit.flags, start, end,
                                  korean[start:end], edit.after, edit.english,
                                  korean[max(0, start - 24) : end + 16].replace("\n", " ")))
    return changes


def manual_changes(file: str, korean: str) -> list[Change]:
    changes = []
    for prefix, needle, old, new, english, expected in MANUAL_A:
        if not file.startswith(prefix):
            continue
        found = [m.start() for m in re.finditer(re.escape(needle), korean)]
        if not found:
            continue  # already repaired
        if len(found) != 1:
            raise SystemExit(f"{file}: manual needle {needle!r} is not unique")
        start = found[0] + needle.index(old)
        edit = Edit(start, start + len(old), new, "A", "hand-checked", english, expected)
        verify(edit, old)
        changes.append(Change(file, "text", "A", "hand-checked", "", start, start + len(old), old,
                              new, english, korean[max(0, start - 24) : start + len(old) + 16]))
    return changes


def translations(root: Path):
    index_path = root / "research" / "generative" / "index.json"
    for row in json.loads(index_path.read_text(encoding="utf-8")):
        ko = row.get("translations", {}).get("ko")
        if ko:
            yield row, ko


def source_html_for(root: Path, row: dict, ko: dict) -> tuple[str | None, str]:
    source_file = ko.get("source_file") or (
        f"research/generative/{row['file'].replace('.html', '.ara.md')}"
    )
    payload = (root / source_file).read_bytes()
    if ko.get("source_sha256") and hashlib.sha256(payload).hexdigest() != ko["source_sha256"]:
        return None, "source changed since the translation"
    return compile_source(payload.decode("utf-8")), ""


def at_revision(root: Path, revision: str, path: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), "show", f"{revision}:{path}"],
        check=True, capture_output=True, text=True,
    ).stdout


def plan(root: Path, report: Report, since: str | None = None) -> dict[str, list[Change]]:
    """All candidate changes, by file, for every class."""
    by_file: dict[str, list[Change]] = {}
    gen = root / "research" / "generative"
    index_raw = (gen / "index.json").read_text(encoding="utf-8")
    title_changes = []
    for row, ko in translations(root):
        file = ko["file"]
        korean = (gen / file).read_text(encoding="utf-8")
        source_html, problem = source_html_for(root, row, ko)
        if source_html is None:
            report.skip(file, "-", problem, "", "")
            continue
        touched = None
        if since:
            touched = changed_spans(at_revision(root, since, f"research/generative/{file}"), korean)
        changes = plan_document(report, file, source_html, korean, touched)
        if changes is None:
            continue
        manual = manual_changes(file, korean)
        changes = [c for c in changes if not any(m.start < c.end and c.start < m.end for m in manual)]
        # What a hand-checked rewrite resolves is no longer left as is.
        report.unresolved = [
            entry for entry in report.unresolved
            if not (entry["file"] == file and entry["english"] and any(
                m.before in entry["korean"] or entry["english"] in m.english for m in manual
            ))
        ]
        by_file[file] = sorted(changes + manual, key=lambda c: c.start)
        # Titles in index.json are plain text with the same garbles.
        title_unit = Unit("text", "", 0, len(ko["title"]), frozenset())
        edits = plan_run(report, "index.json", title_unit, html.escape(row["title"]), ko["title"])
        edits += plan_signs(report, "index.json", title_unit, html.escape(row["title"]), ko["title"])
        if edits:
            needle = json.dumps(ko["title"], ensure_ascii=False)
            if needle[1:-1] != ko["title"] or index_raw.count(needle) != 1:
                raise SystemExit(f"index.json title of {row['slug']} is not a unique plain string")
            offset = index_raw.index(needle) + 1
            for edit in edits:
                verify(edit, ko["title"][edit.start : edit.end])
                start, end = offset + edit.start, offset + edit.end
                title_changes.append(Change("index.json", f"title of {row['slug']}", edit.cls,
                                            edit.rule, edit.flags, start, end, index_raw[start:end],
                                            edit.after, edit.english, ko["title"]))
    if title_changes:
        by_file["index.json"] = title_changes
    return by_file


def write_reports(directory: Path, changes: list[Change], report: Report, seed: int) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    columns = ["file", "class", "rule", "unit", "flags", "english_source", "before", "after", "context"]
    rows = [
        [c.file, c.cls, c.rule, c.unit, c.flags, c.english, c.before, c.after, c.context]
        for c in changes
    ]
    with (directory / "repair-table.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)
    with (directory / "samples.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(random.Random(seed).sample(rows, min(20, len(rows))))
    counts = collections.defaultdict(collections.Counter)
    for c in changes:
        counts[c.file][c.cls] += 1
    classes = sorted({c.cls for c in changes})
    with (directory / "per-file-counts.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["file", *classes, "total"])
        for file in sorted(counts):
            writer.writerow([file, *(counts[file][cls] for cls in classes), sum(counts[file].values())])
    with (directory / "unresolved.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["file", "unit", "reason", "english_source", "korean"])
        for entry in report.unresolved:
            writer.writerow([entry[key] for key in ("file", "unit", "reason", "english", "korean")])


def run(
    root: Path, classes: set[str], write: bool, since: str | None = None
) -> tuple[list[Change], Report]:
    report = Report()
    gen = root / "research" / "generative"
    selected = [
        change
        for changes in plan(root, report, since).values()
        for change in changes
        if change.cls in classes
    ]
    if write:
        by_file: dict[str, list[Change]] = collections.defaultdict(list)
        for change in selected:
            by_file[change.file].append(change)
        for file, changes in by_file.items():
            path = gen / file
            old = path.read_text(encoding="utf-8")
            edits = [(c.start, c.end, c.after) for c in changes]
            for c in changes:
                if old[c.start : c.end] != c.before:
                    raise SystemExit(f"{file}: stale offsets at {c.start}")
            new = apply(old, edits)
            assert_identical_outside(old, new, edits, file)
            path.write_text(new, encoding="utf-8")
        again = [c for changes in plan(root, Report(), since).values() for c in changes if c.cls in classes]
        if again:
            raise SystemExit(f"not idempotent: {len(again)} changes remain after writing")
    report.changes = selected
    return selected, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--classes", default="A,B,S", help="comma-separated classes: A, B, S")
    parser.add_argument("--write", action="store_true", help="apply the changes in place")
    parser.add_argument("--report", type=Path, help="directory for the CSV repair table")
    parser.add_argument("--seed", type=int, default=0, help="seed for the 20 review samples")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--touched-since", metavar="REV",
                        help="write the wave dash in date ranges that changed since REV")
    args = parser.parse_args(argv)
    classes = {cls.strip() for cls in args.classes.split(",") if cls.strip()}
    if not classes <= {"A", "B", "S"}:
        parser.error("classes must be among A, B, S")
    changes, report = run(args.root, classes, args.write, args.touched_since)
    if args.report:
        write_reports(args.report, changes, report, args.seed)
    counts = collections.Counter(change.cls for change in changes)
    files = len({change.file for change in changes})
    verb = "rewrote" if args.write else "would rewrite"
    print(f"{verb} {sum(counts.values())} phrase(s) in {files} file(s): {dict(sorted(counts.items()))}")
    reasons = collections.Counter(entry["reason"] for entry in report.unresolved)
    print(f"listed and left as is: {sum(reasons.values())} {dict(sorted(reasons.items()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
