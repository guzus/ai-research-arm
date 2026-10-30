#!/usr/bin/env python3
"""Validate and normalize the Aradio editor artifact (`.tmp/aradio/edit.json`).

The editor agent (prompts/aradio-editor.md) runs in an isolated container and
returns exactly one untrusted file. This script is the trusted gate between
that file and research/aradio/ (contract: docs/aradio.md -> "Validation").

* Hard errors exit 1: nothing is published and the cursor does not advance,
  so the next run retries the same material.
* Soft errors are repaired and listed in the normalized edit's `warnings`,
  which the writer copies into the bulletin.

Provenance is enforced here, not trusted from the editor:

* an evidence URL survives only if it is in this run's trusted inbox
  (`url`/`links`) or already on the board; its `kind` and `at` always come
  from that trusted record;
* a `quote` survives only if it is EXACTLY ONE COMPLETE SENTENCE of ONE
  transcript window of a spoken item or ONE "Key quotes" line of an earnings
  item (never titles, show notes, or the model-written Twitter/ticket text),
  at most QUOTE_MAX_WORDS words. The editor's string is only a search key:
  what is published is that whole sentence in the source's own wording, so
  inserted punctuation cannot change what was said, and a cut-out span cannot
  drop the negation, condition or question mark around it. The URL rule alone
  cannot stop a fabricated quote attributed to a real source, so quotes are
  checked against what the editor was actually shown;
* a transcript quote never carries `speaker` (captions do not record who is
  talking, and a name in a window is not its speaker); a Key-quotes quote
  carries the line's own attribution. A quoted entry's `label` is the
  trusted source name (the dashboard prints "speaker, label" under a quote);
* quoting follows the earnings lane's excerpt policy across the whole board:
  at most QUOTES_PER_SOURCE quotes / QUOTE_WORDS_PER_SOURCE words per source,
  and QUOTES_PER_RUN new quotes per run.

This module is also the lane's single source of truth for limits and spoken
text handling: build_aradio_inbox.py (context.json), aradio_tts.py and
write_aradio_bulletin.py (which re-validates before applying any op) import it.

Usage:
  check_aradio.py --edit .tmp/aradio/edit.json --inbox $T/trusted/inbox.json \
      --state research/aradio/state.json --out $T/edit.normalized.json \
      [--github-output "$GITHUB_OUTPUT"]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SCHEMA = 1
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SLUG_MAX = 64
MAX_CREATES = 3
MAX_UNRESOLVED = 10
MAX_EVIDENCE = 8
STATUSES = ("developing", "escalating", "steady", "resolved")
OPEN_STATUSES = ("developing", "escalating", "steady")
EVIDENCE_KINDS = ("podcast", "video", "earnings-call", "earnings", "twitter", "ticket")
TEXT_LIMITS = {"title": 90, "now": 400, "changed": 240, "watch": 200, "change": 200}
HEADLINE_MAX = 140
NOTE_MAX = 300
LABEL_MAX = 90  # the dashboard shows evidence labels up to 90 characters
SPEAKER_MAX = 80
QUOTE_MAX_WORDS = 40
# Quoted words are republished (everything under research/ is public), so the
# board follows the earnings lane's excerpt policy, counted across the whole
# board and not per op: per source item at most QUOTES_PER_SOURCE distinct
# quotes and QUOTE_WORDS_PER_SOURCE quoted words, and at most QUOTES_PER_RUN
# new quotes per edit. Excess quotes are dropped; their evidence stays.
QUOTES_PER_SOURCE = 2
QUOTE_WORDS_PER_SOURCE = 60
QUOTES_PER_RUN = 8
# A quote is what someone SAID: a transcript window of a spoken item, or the
# issuer's own attributed line under an earnings item's "Key quotes:". Never
# a title, show notes, or the Twitter/ticket lanes' text, which is ARA's own
# model-written summary.
SPOKEN_KINDS = ("podcast", "video", "earnings-call")
EARNINGS_KIND = "earnings"
QUOTABLE_KINDS = SPOKEN_KINDS + (EARNINGS_KIND,)
KEY_QUOTES_HEADER = "Key quotes:"
# `- Andy Jassy, President and CEO, Amazon: "…" (EX-99.1)` as the inbox
# builder renders the earnings lane's `## Key Quotes` bullets.
KEY_QUOTE_LINE_RE = re.compile(
    r'^- (?P<who>[^"“”]{1,200}?): ["“](?P<words>.+)["”](?: \([^()]{0,120}\))?$')
# A quote is one WHOLE sentence (see split_sentences). This replaced a
# substring rule plus a heuristic that refused a span starting within four
# words of a negation: any substring rule can be outrun by a longer gap ("I
# don't think that over the next decade | we will see AGI"), a condition ("if
# | OpenAI goes bankrupt") or a question ("will | Nvidia margins hold"),
# while a whole sentence carries its own negation, condition and question
# mark. Sentence ends are judged conservatively: a missed split only makes a
# sentence longer (harder to quote), a wrong one would start a quote
# mid-sentence. So these never end a sentence, even before a capital:
ABBREVIATIONS = frozenset({
    "mr.", "mrs.", "ms.", "dr.", "prof.", "st.", "jr.", "sr.", "gen.", "sen.", "rep.",
    "gov.", "pres.", "inc.", "corp.", "co.", "ltd.", "llc.", "plc.", "vs.", "etc.", "e.g.",
    "i.e.", "cf.", "al.", "approx.", "est.", "fig.", "no.", "vol.", "jan.", "feb.", "mar.",
    "apr.", "jun.", "jul.", "aug.", "sep.", "sept.", "oct.", "nov.", "dec.",
})
INITIALS_RE = re.compile(r"(?:[a-z]\.)+")  # "U.S.", "A.I.", "J." (lower-cased)
SENTENCE_CLOSERS = "\"'”’)]}»›"
SENTENCE_OPENERS = "\"'“‘([{«‹"
# Caption speaker-change marker. The inbox keeps it in transcript windows
# (fetch_podcast_signal.select_windows with sentence_end=...); a sentence
# never spans one.
TURN_RE = re.compile(r">>+")
# What the inbox builder puts at a transcript window's edge where the window
# cuts into a sentence ("…" glued to the first or last word): the sentence
# there is not whole, and any sentence holding an ellipsis is unquotable.
CUT_MARK = "…"
YOUTUBE_HOSTS = frozenset({"youtube.com", "m.youtube.com", "music.youtube.com",
                           "youtube-nocookie.com"})
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
# Hard bounds (validator) and the editor's targets (prompt). The gap is the
# tolerance that keeps a slightly long or short script from wasting a run.
SCRIPT_LINES = (8, 30)
SCRIPT_WORDS = (250, 900)
TARGET_SCRIPT_LINES = (10, 24)
TARGET_SCRIPT_WORDS = (350, 750)
TAG_LIMITS = {"[high_energy]": 1, "[emphasis]": 3, "[dramatic_pause]": 1}
MAX_TAGS = 5
WORDS_PER_MINUTE = 188
MAX_EDIT_BYTES = 1024 * 1024

SCRIPT_LINE_RE = re.compile(r"^Speaker [12]: \S")
SPEAKER_PREFIX_RE = re.compile(r"^Speaker ([12]):\s*")
KNOWN_TAG_RE = re.compile(r"\[(?:high_energy|emphasis|/emphasis|dramatic_pause)\]")
BRACKET_TOKEN_RE = re.compile(r"\[[^\[\]\n]{0,60}\]")
ANGLE_TOKEN_RE = re.compile(r"<[^<>\n]{0,60}>")
# URLs never belong in prose fields or the spoken script (they live in
# evidence), and link-shaped text must not survive to a page that might render
# it: plain URLs, www. hosts and script-capable schemes are stripped.
URL_IN_TEXT_RE = re.compile(
    r"(?:https?://|www\.)\S+|\b(?:javascript|vbscript|data|file):\S+", re.IGNORECASE)
MD_LINK_RE = re.compile(
    r"\[([^\[\]\n]{0,300})\]\((?:[^()\n]|\([^()\n]{0,200}\)){0,2100}\)")
# The strict third-party URL rule, applied at every Aradio boundary (inbox
# items, evidence, published files). Prefix checks are not enough: a "URL"
# like `https://a.example/x) [y](javascript:alert(1))` must never reach a
# page. Same rule as fetch_podcast_signal.safe_url.
SAFE_URL_SCHEMES = frozenset({"https", "http"})
SAFE_URL_FORBIDDEN = frozenset('<>"\'()[]{}|\\^`')
SAFE_URL_MAX = 2048
MARKDOWN_CHARS_RE = re.compile(r"[*`]")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f-\x9f  ]")
TRANSCRIPT_FILE_RE = re.compile(r"^transcripts/[0-9]{1,3}\.txt$")

TOP_LEVEL_KEYS = ("schema", "on_air", "headline", "ops", "script", "covers", "note")
# Accepted (and ignored) so the writer can re-validate this script's own output.
NORMALIZED_ONLY_KEYS = ("warnings", "stats")
OP_FIELDS = {
    "create": ("op", "slug", "title", "status", "importance", "now", "changed",
               "watch", "evidence", "change"),
    "update": ("op", "slug", "title", "status", "importance", "now", "changed",
               "watch", "add_evidence", "change"),
    "resolve": ("op", "slug", "changed", "change"),
}
REQUIRED_FIELDS = {
    "create": ("title", "now", "changed", "change"),
    "update": ("changed", "change"),
    "resolve": ("changed", "change"),
}
EVIDENCE_FIELDS = ("url", "label", "speaker", "quote")

EXIT_OK = 0
EXIT_HARD = 1

_QUOTE_FOLD = str.maketrans({
    "‘": "'", "’": "'", "‛": "'", "′": "'",
    "“": '"', "”": '"', "—": " ", "–": " ", "−": "-",
})


# ---------------------------------------------------------------------------
# Shared text helpers (also used by the inbox builder, TTS and writer)
# ---------------------------------------------------------------------------

def gh_escape(text: Any) -> str:
    """Escape untrusted text for a GitHub workflow command's data part.

    Agent-authored strings printed raw could start a new line with `::...::`
    and inject a workflow command; escaped, they stay one inert line.
    """
    return (str(text).replace("%", "%25").replace("\r", "%0D")
            .replace("\n", "%0A"))


def safe_url(url: Any) -> str | None:
    """Return `url` unchanged if it passes the strict rule, else None.

    Identical to fetch_podcast_signal.safe_url (the podcasts lane), so a URL
    that lane publishes is exactly a URL this lane can cite: http(s) scheme, a
    host, no userinfo, a well-formed port, at most 2048 characters, and none
    of <>"'()[]{}|\\^` , whitespace, or control/format (Unicode C*) characters,
    which also covers bidi overrides. Nothing is repaired or re-encoded.
    """
    if not isinstance(url, str) or not url or len(url) > SAFE_URL_MAX:
        return None
    for char in url:
        if (char in SAFE_URL_FORBIDDEN or char.isspace()
                or unicodedata.category(char)[0] == "C"):
            return None
    try:
        parts = urllib.parse.urlsplit(url)
        parts.port  # raises ValueError on a malformed port
    except ValueError:
        return None
    if parts.scheme not in SAFE_URL_SCHEMES or not parts.netloc or not parts.hostname:
        return None
    if "@" in parts.netloc:  # credentials in a URL are never published
        return None
    return url


def strip_urls(text: str) -> tuple[str, bool]:
    """Remove markdown link targets and URL-like tokens; (text, changed)."""
    stripped = MD_LINK_RE.sub(lambda match: match.group(1), text)
    stripped = URL_IN_TEXT_RE.sub(" ", stripped)
    stripped = " ".join(stripped.split())
    return stripped, stripped != " ".join(text.split())


def fingerprint(value: Any) -> str:
    return "url#" + hashlib.sha256(str(value).encode("utf-8", "replace")).hexdigest()[:10]


def defang(message: str) -> str:
    """Diagnostics are published (bulletin `warnings`): never echo a URL."""
    message = MD_LINK_RE.sub(lambda match: match.group(1) + " " + fingerprint(match.group(0)),
                             message)
    return URL_IN_TEXT_RE.sub(lambda match: fingerprint(match.group(0)), message)


def clean_text(value: str) -> str:
    """NFC, control characters to spaces, whitespace collapsed to one line."""
    text = unicodedata.normalize("NFC", value)
    text = CONTROL_RE.sub(" ", text)
    return " ".join(text.split())


def clip(text: str, limit: int) -> tuple[str, bool]:
    """Truncate to `limit` characters, preferring a word boundary."""
    if len(text) <= limit:
        return text, False
    cut = text[: limit - 1].rstrip()
    space = cut.rfind(" ")
    if space >= int(limit * 0.6):
        cut = cut[:space].rstrip()
    return cut + "…", True


SPACE_BEFORE_PUNCT_RE = re.compile(r"\s+([,.;:!?])")


def tidy_spaces(text: str) -> str:
    """Collapse whitespace and drop spaces a removed tag left before punctuation."""
    return SPACE_BEFORE_PUNCT_RE.sub(r"\1", " ".join(text.split()))


def strip_audio_tags(text: str) -> str:
    """Display form: remove the known audio tags and collapse whitespace."""
    return tidy_spaces(KNOWN_TAG_RE.sub(" ", text))


def split_script_line(line: str) -> tuple[str, str]:
    """('Speaker 1', 'raw text with tags') for a validated script line."""
    match = SPEAKER_PREFIX_RE.match(line)
    if not match:
        raise ValueError(f"not a speaker line: {line[:40]!r}")
    return f"Speaker {match.group(1)}", line[match.end():]


def spoken_text(line: str) -> str:
    match = SPEAKER_PREFIX_RE.match(line)
    body = line[match.end():] if match else line
    return strip_audio_tags(body)


def count_spoken_words(lines: list[str]) -> int:
    return sum(len(spoken_text(line).split()) for line in lines)


def expected_duration_s(words: int) -> float:
    return words / WORDS_PER_MINUTE * 60.0


def _fold_char(char: str) -> str:
    """One character in match form: word characters lower-cased, anything else
    a space; apostrophes vanish, so "don't" and "dont" are the same word."""
    folded = unicodedata.normalize("NFKC", char).translate(_QUOTE_FOLD).lower()
    return "".join(ch if ch.isalnum() or ch == "_" else " " for ch in folded if ch != "'")


def match_words(text: str) -> tuple[list[str], list[tuple[int, int]]]:
    """`text` in match form (case, quote marks, dashes, punctuation folded) as
    words, each with the [start, end) range of the characters it came from.

    Folding is per character, so any substring of `text` folds to the
    matching run of words; that map is what lets the validator publish the
    source's own characters rather than the editor's.
    """
    words: list[str] = []
    spans: list[tuple[int, int]] = []
    current: list[str] = []
    start = end = 0
    for index, char in enumerate(text):
        for ch in _fold_char(char):
            if ch != " ":
                if not current:
                    start = index
                current.append(ch)
                end = index + 1
            elif current:
                words.append("".join(current))
                spans.append((start, end))
                current = []
    if current:
        words.append("".join(current))
        spans.append((start, end))
    return words, spans


_ELLIPSIS_RE = re.compile(r"\[\s*\.\.\.\s*\]|\.\.\.|…")
_OPENERS = {"(": ")", "[": "]", "{": "}", "“": "”", "‘": "’", "«": "»", "‹": "›"}
_CLOSERS = {close: opener for opener, close in _OPENERS.items()}
_DANGLING = ",;:<>*•·–—"  # never part of a word, so never worth publishing at an end
_TOKEN_RE = re.compile(r"\S+")


def _has_run(words: Any, run: list[str]) -> bool:
    size = len(run)
    return any(list(words[i:i + size]) == run for i in range(len(words) - size + 1))


def _trim_span(text: str, start: int, end: int) -> tuple[int, int]:
    """Drop unbalanced quote marks and brackets and dangling punctuation from
    the ends of a span. Only non-word characters go, so its words are kept."""
    while start < end:
        span, first, last = text[start:end], text[start], text[end - 1]
        if first in _DANGLING or (first in _OPENERS and _OPENERS[first] not in span[1:]):
            start += 1
        elif last in _DANGLING or (last in _CLOSERS and _CLOSERS[last] not in span[:-1]):
            end -= 1
        elif first in "\"'" and span.count(first) % 2:
            start += 1
        elif last in "\"'" and span.count(last) % 2:
            end -= 1
        else:
            break
    return start, end


def sentence_end(word: str, next_word: str | None = None) -> bool:
    """True when the whitespace-delimited token `word` ends a sentence.

    It must end in `.`, `!` or `?` (closing quotes or brackets may follow),
    and not be an ellipsis, an abbreviation (ABBREVIATIONS) or initials
    ("U.S."); and the next token, when known, must not start in lower case
    ('he asked "why?" and left' is one sentence). Numbers never end one
    inside ("32.5", "1.5B": no whitespace follows the point). The inbox
    builder judges transcript-window edges with this same function, so a
    window and the validator always agree on where a sentence ends.
    """
    core = word.rstrip(SENTENCE_CLOSERS)
    if not core or core[-1] not in ".!?" or core.endswith(".."):
        return False
    bare = core.lstrip(SENTENCE_OPENERS).lower()
    if bare in ABBREVIATIONS or INITIALS_RE.fullmatch(bare):
        return False
    if next_word is not None and next_word.lstrip(SENTENCE_OPENERS)[:1].islower():
        return False
    return True


@dataclass(frozen=True)
class QuoteSource:
    """One place a quote may come from, in the source's own wording.

    `text` is a transcript window (with its `>>` speaker changes and `…` cut
    marks, as the inbox staged it), or the quoted words of one earnings
    Key-quotes line; a published quote is always one whole sentence of it.
    `attribution` is that earnings line's named speaker ("Andy Jassy, President
    and CEO, Amazon"); None for a transcript window, whose quotes never name
    a speaker.
    """

    text: str
    attribution: str | None = None


@dataclass(frozen=True)
class Sentence:
    text: str                 # the source's wording, as published
    words: tuple[str, ...]    # match form
    problem: str | None       # why it may not be quoted; None when it may


def split_sentences(source: QuoteSource) -> list[Sentence]:
    """The source's text as sentences, in order.

    Boundaries: a token that ends a sentence (sentence_end), a `>>` speaker
    change, and the ends of the source. A sentence may be quoted only if it
    holds no ellipsis (a pause, or the inbox's cut mark at a window edge
    that falls mid-sentence) and ends with its own `.`, `!` or `?`; the last
    sentence of an earnings Key-quotes line is exempt from the latter, as the
    issuer's quotation itself ends there (the earnings lane drops the comma
    before "said"). So unpunctuated captions yield no quotable sentence: the
    editor paraphrases them instead.
    """
    found: list[Sentence] = []
    turns = TURN_RE.split(source.text)
    for turn_index, turn in enumerate(turns):
        tokens = list(_TOKEN_RE.finditer(turn))
        first = 0
        for index, token in enumerate(tokens):
            following = tokens[index + 1].group(0) if index + 1 < len(tokens) else None
            if following is not None and not sentence_end(token.group(0), following):
                continue
            raw = turn[tokens[first].start():token.end()]
            first = index + 1
            words = tuple(match_words(raw)[0])
            if not words:
                continue
            last_of_line = (source.attribution is not None and following is None
                            and turn_index == len(turns) - 1)
            problem = None
            if _ELLIPSIS_RE.search(raw):
                problem = ("is cut: the sentence runs past the window edge or holds an "
                           "ellipsis in the source")
            elif not sentence_end(token.group(0)) and not last_of_line:
                problem = ("has no closing . ! or ? in the source (unpunctuated captions, "
                           "or a sentence cut off by a speaker change)")
            start, end = _trim_span(raw, 0, len(raw))
            found.append(Sentence(text=" ".join(raw[start:end].split()), words=words,
                                  problem=problem))
    return found


@dataclass(frozen=True)
class QuoteMatch:
    quote: str                # the whole sentence, in the source's wording
    source: QuoteSource
    problem: str | None       # why this sentence may not be quoted, if it may not


def find_quote(key: str, sources: tuple[QuoteSource, ...] | list[QuoteSource]
               ) -> list[QuoteMatch]:
    """Every sentence of `sources` that `key` matches WHOLE, quotable or not.

    The editor's string is only a search key: case and punctuation are folded
    to compare it with each sentence (split_sentences), then the source's own
    sentence is published, so inserted punctuation can never change what a
    speaker said ("I don't think. We are going to see AGI"), and a span cut
    out of a sentence ("we will see AGI" from "I don't think that over the
    next decade we will see AGI.") never matches at all. A key with an
    ellipsis never matches: it would stitch words spoken apart.
    """
    if _ELLIPSIS_RE.search(key):
        return []
    needle = tuple(match_words(key)[0])
    if not needle:
        return []
    return [QuoteMatch(quote=sentence.text, source=source, problem=sentence.problem)
            for source in sources for sentence in split_sentences(source)
            if sentence.words == needle]


def quote_miss(key: str, sources: tuple[QuoteSource, ...] | list[QuoteSource]) -> str:
    """Why `key` matches no whole sentence (published in warnings: no text)."""
    if _ELLIPSIS_RE.search(key):
        return "contains an ellipsis; a quote is one whole sentence"
    needle = match_words(key)[0]
    if needle and any(_has_run(match_words(chunk)[0], needle)
                      for source in sources for chunk in TURN_RE.split(source.text)):
        return ("is part of a sentence, or joins sentences, in the source; a quote is "
                "exactly one whole sentence")
    if needle and any(_has_run(match_words(source.text)[0], needle) for source in sources):
        return "crosses a speaker change ('>>') in the transcript"
    return "is not a sentence of one transcript window or Key-quotes line"


def parse_key_quotes(text: str) -> list[QuoteSource]:
    """The attributed lines under an earnings item's "Key quotes:" header,
    each as (the issuer's quoted words, the speaker the line names). A line
    that does not parse, e.g. one the inbox clipped, is not quotable."""
    found: list[QuoteSource] = []
    in_block = False
    for raw in text.splitlines():
        line = " ".join(raw.split())
        if line == KEY_QUOTES_HEADER:
            in_block = True
            continue
        if not in_block:
            continue
        if not line.startswith("- "):
            in_block = False
            continue
        match = KEY_QUOTE_LINE_RE.match(line)
        if match and match.group("words").strip() and match.group("who").strip():
            found.append(QuoteSource(text=match.group("words").strip(),
                                     attribution=match.group("who").strip()))
    return found


def source_of_url(url: str) -> str:
    """The source a URL points into, for counting quotes per source: one
    YouTube video whatever the deep link (`&t=…s`, youtu.be, /live/), else
    host and path without scheme, query or fragment (coarser is stricter)."""
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return "web:" + url
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    video = ""
    segments = parts.path.strip("/").split("/")
    if host == "youtu.be":
        video = segments[0]
    elif host in YOUTUBE_HOSTS:
        if segments[0] == "watch":
            video = (urllib.parse.parse_qs(parts.query).get("v") or [""])[0]
        elif len(segments) >= 2 and segments[0] in ("embed", "shorts", "live", "v"):
            video = segments[1]
    if YOUTUBE_ID_RE.match(video):
        return "youtube:" + video
    return f"web:{host}{parts.path.rstrip('/')}"


def atomic_write_text(path: Path, text: str) -> None:
    """Temp file in the same directory + os.replace (CLAUDE.md rule 8).

    The `.<name>.*.tmp` shape matches the repo's gitignored debris pattern.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp",
                               dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, 0o644)  # mkstemp creates 0600; published files are plain data
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def dump_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def atomic_write_json(path: Path, data: Any) -> None:
    atomic_write_text(path, dump_json(data))


def empty_board() -> dict:
    return {"schema": SCHEMA, "updated_at": None, "headline": "", "threads": []}


def load_board(path: Path | None) -> dict:
    """Load research/aradio/state.json; absent means the empty first-run board."""
    if path is None or not path.exists():
        return empty_board()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("threads"), list):
        raise ValueError(f"{path}: board must be an object with a threads list")
    return data


# ---------------------------------------------------------------------------
# Trusted inbox view
# ---------------------------------------------------------------------------

@dataclass
class TrustedInbox:
    """The host-side copy of this run's inbox (never the agent's copy)."""

    items: list[dict]
    base_dir: Path | None = None
    url_owner: dict[str, dict] = field(default_factory=dict)
    source_owner: dict[str, str] = field(default_factory=dict)
    _quote_sources: dict[int, tuple[QuoteSource, ...]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # The first-party lanes (spoken media, earnings) claim their URLs
        # before items that merely link to them: a tweet linking to an episode
        # must not turn the episode's URL into "twitter" evidence, because an
        # evidence entry's kind, time and quotability all come from its owner.
        order = sorted(range(len(self.items)),
                       key=lambda i: (self.items[i].get("kind") not in QUOTABLE_KINDS, i))
        for index in order:
            item = self.items[index]
            key = item.get("key")
            for url in item_urls(item):
                self.url_owner.setdefault(url, item)
                if isinstance(key, str) and key:
                    self.source_owner.setdefault(source_of_url(url), key)

    @classmethod
    def from_obj(cls, obj: Any, base_dir: Path | None = None) -> "TrustedInbox":
        if not isinstance(obj, dict) or not isinstance(obj.get("items"), list):
            raise ValueError("trusted inbox must be an object with an items list")
        items = [item for item in obj["items"] if isinstance(item, dict)]
        return cls(items=items, base_dir=base_dir)

    @classmethod
    def load(cls, path: Path) -> "TrustedInbox":
        obj = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_obj(obj, base_dir=path.parent)

    def keys(self) -> list[str]:
        return [str(item.get("key")) for item in self.items if item.get("key")]

    def quote_sources(self, item: dict) -> tuple[QuoteSource, ...]:
        """Where a quote on this item may come from — kept apart so a quote
        can never bridge two of them: each transcript window of a spoken item,
        or each Key-quotes line of an earnings item. Nothing else: titles,
        show notes and the Twitter/ticket lanes' text are not what anyone said."""
        if id(item) in self._quote_sources:
            return self._quote_sources[id(item)]
        sources: list[QuoteSource] = []
        kind = item.get("kind")
        transcript = item.get("transcript_file")
        if (kind in SPOKEN_KINDS and self.base_dir is not None and isinstance(transcript, str)
                and TRANSCRIPT_FILE_RE.match(transcript)):
            candidate = self.base_dir / transcript
            if candidate.is_file() and not candidate.is_symlink():
                text = candidate.read_text(encoding="utf-8", errors="replace")
                for line in text.splitlines():
                    window = " ".join(re.sub(r"^\[[0-9:]+\]\s*", "", line).split())
                    if window:
                        sources.append(QuoteSource(text=window))
        elif kind == EARNINGS_KIND:
            sources = parse_key_quotes(str(item.get("text") or ""))
        self._quote_sources[id(item)] = tuple(sources)
        return self._quote_sources[id(item)]

    def source_identity(self, url: str) -> str:
        """What a URL's quotes count against: the inbox item that carries its
        source (a deep link `&t=…s` counts as its episode), else the source
        itself, so board evidence from earlier runs counts the same way."""
        source = source_of_url(url)
        key = self.source_owner.get(source)
        return "item:" + key if key else source


def item_urls(item: dict) -> list[str]:
    """The item's citable URLs: only those passing the strict rule."""
    urls: list[str] = []
    candidates = [item.get("url")]
    if isinstance(item.get("links"), list):
        candidates.extend(item["links"])
    for value in candidates:
        url = safe_url(value)
        if url and url not in urls:
            urls.append(url)
    return urls


def board_evidence(board: dict) -> dict[str, dict]:
    found: dict[str, dict] = {}
    for thread in board.get("threads") or []:
        if not isinstance(thread, dict):
            continue
        for evidence in thread.get("evidence") or []:
            if isinstance(evidence, dict) and safe_url(evidence.get("url")):
                found.setdefault(evidence["url"], evidence)
    return found


@dataclass
class QuoteBudget:
    """How much of each source the board quotes, and this run's new quotes.

    Seeded from every quote already on the board (resolved threads too: they
    are still published), so a source cannot be quoted past the policy by
    spreading quotes over threads, ops, deep-link URLs or runs.
    """

    quoted: dict[str, dict[str, int]] = field(default_factory=dict)  # source -> {quote: words}
    new: int = 0

    @classmethod
    def from_board(cls, board: dict, inbox: "TrustedInbox") -> "QuoteBudget":
        budget = cls()
        for thread in board.get("threads") or []:
            entries = thread.get("evidence") if isinstance(thread, dict) else None
            for evidence in entries if isinstance(entries, list) else []:
                if (isinstance(evidence, dict) and safe_url(evidence.get("url"))
                        and isinstance(evidence.get("quote"), str) and evidence["quote"].strip()):
                    source = budget.quoted.setdefault(inbox.source_identity(evidence["url"]), {})
                    source[evidence["quote"]] = len(evidence["quote"].split())
        return budget

    def charge(self, source_id: str, quote: str) -> str | None:
        """Record `quote` against its source; None if allowed, else the reason.
        A quote the board already carries from that source is free: re-citing
        it republishes nothing new."""
        quoted = self.quoted.setdefault(source_id, {})
        if quote in quoted:
            return None
        words = len(quote.split())
        if len(quoted) >= QUOTES_PER_SOURCE or sum(quoted.values()) + words > QUOTE_WORDS_PER_SOURCE:
            return (f"this source is already quoted {len(quoted)} time(s), "
                    f"{sum(quoted.values())} words, on the board and in this edit; limit "
                    f"{QUOTES_PER_SOURCE} quotes and {QUOTE_WORDS_PER_SOURCE} words per source")
        if self.new >= QUOTES_PER_RUN:
            return f"limit {QUOTES_PER_RUN} new quotes per run"
        quoted[quote] = words
        self.new += 1
        return None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def hard(self, message: str) -> None:
        self.errors.append(message)

    def soft(self, message: str) -> None:
        message = defang(message)
        if message not in self.warnings:
            self.warnings.append(message)


def _short(value: Any, limit: int = 80) -> str:
    text = clean_text(str(value))
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _text_field(op: dict, name: str, where: str, report: Report, *,
                required: bool, allow_empty: bool = False) -> str | None:
    """Required fields are schema (hard); optional ones are repaired (soft)."""
    if name not in op:
        if required:
            report.hard(f"{where}: missing required field '{name}'")
        return None
    value = op[name]
    if not isinstance(value, str):
        if required:
            report.hard(f"{where}: field '{name}' must be a string")
        else:
            report.soft(f"{where}: non-string '{name}' dropped")
        return None
    text, had_url = strip_urls(clean_text(value))
    if had_url:
        report.soft(f"{where}: URL stripped from '{name}'")
    if not text:
        if required:
            report.hard(f"{where}: field '{name}' must not be empty")
            return None
        if not allow_empty:
            report.soft(f"{where}: empty '{name}' ignored")
            return None
        return ""
    limit = TEXT_LIMITS.get(name)
    if limit is not None:
        text, cut = clip(text, limit)
        if cut:
            report.soft(f"{where}: '{name}' truncated to {limit} characters")
    return text


def _importance(value: Any, where: str, report: Report) -> int | None:
    number: int | None = None
    if isinstance(value, bool):
        number = None
    elif isinstance(value, int):
        number = value
    elif isinstance(value, float) and value.is_integer():
        number = int(value)
    elif isinstance(value, str) and value.strip().isdigit():
        number = int(value.strip())
    if number is None:
        report.soft(f"{where}: importance {_short(value)!r} is not an integer 1-5; ignored")
        return None
    if number < 1 or number > 5:
        report.soft(f"{where}: importance {number} clamped to 1-5")
        number = max(1, min(5, number))
    return number


def _status(value: Any, where: str, report: Report) -> str | None:
    if isinstance(value, str) and value in OPEN_STATUSES:
        return value
    if value == "resolved":
        report.soft(f"{where}: status 'resolved' ignored; use the resolve op")
    else:
        report.soft(f"{where}: unknown status {_short(value)!r} ignored")
    return None


def _evidence_quote(entry: dict, where: str, url: str, owner: dict | None,
                    existing: dict | None, inbox: TrustedInbox, report: Report,
                    stats: dict[str, int], budget: QuoteBudget) -> dict[str, str]:
    """The verified {quote, label, speaker?} of one evidence entry, or {}.

    * The published quote is one whole sentence of a quotable source of the
      entry's owner (a transcript window, or an earnings Key-quotes line), in
      the source's own wording; the editor's string is only the search key
      (find_quote). It must fit QUOTE_MAX_WORDS and the per-source and
      per-run budget.
    * `speaker` is never the editor's: a transcript quote carries none
      (captions do not record who is talking, and a name in a window may be
      its subject), a Key-quotes quote carries that line's own attribution.
    * A quoted entry is labelled with the trusted source name: the dashboard
      prints "speaker, label" under a quote, so an editor-written label would
      attribute the quote to whoever the editor chose.

    Warnings give a word count, never the text: they are published with the
    bulletin, and echoing a dropped quote would republish it anyway.
    """
    raw_quote = entry.get("quote")
    quote = clean_text(raw_quote) if isinstance(raw_quote, str) else ""
    if raw_quote is not None and raw_quote != "" and not quote:
        report.soft(f"{where}: invalid quote dropped")
    raw_speaker = entry.get("speaker")
    speaker = strip_urls(clean_text(raw_speaker))[0] if isinstance(raw_speaker, str) else ""
    if raw_speaker is not None and not speaker:
        report.soft(f"{where}: invalid speaker dropped")
    elif len(speaker) > SPEAKER_MAX:
        report.soft(f"{where}: speaker over {SPEAKER_MAX} characters dropped")
        speaker = ""
    if not quote:
        if speaker:
            report.soft(f"{where}: speaker dropped; a speaker is kept only with a verified quote")
        return {}

    def drop(reason: str) -> dict[str, str]:
        stats["quotes_dropped"] += 1
        report.soft(f"{where}: quote ({len(quote.split())} words) {reason}; dropped"
                    + (" with its speaker" if speaker else ""))
        return {}

    def unspoken() -> None:
        if speaker:
            report.soft(f"{where}: speaker dropped; a transcript quote never names a speaker "
                        "(captions do not record who is talking): attribute it in prose "
                        "to the show or call")

    if strip_urls(quote)[1]:
        return drop("contains a URL")
    if len(quote.split()) > QUOTE_MAX_WORDS:
        return drop(f"is over {QUOTE_MAX_WORDS} words")
    if owner is None:
        # Not in this run's inbox: only a quote the board already verified may
        # travel, and it travels with the board's attribution (none for a
        # transcript quote).
        board_quote = existing.get("quote") if existing is not None else None
        kind = existing.get("kind") if existing is not None else None
        if not isinstance(board_quote, str) or board_quote != quote or kind not in QUOTABLE_KINDS:
            return drop("cannot be verified (source not in this run's inbox)")
        reason = budget.charge(inbox.source_identity(url), board_quote)
        if reason:
            return drop(f"exceeds the excerpt policy ({reason})")
        stats["quotes_kept"] += 1
        result = {"quote": board_quote,
                  "label": clip(clean_text(str(existing.get("label") or "")) or "source",
                                LABEL_MAX)[0]}
        if kind in SPOKEN_KINDS:
            unspoken()
            return result
        board_speaker = existing.get("speaker")
        if isinstance(board_speaker, str) and board_speaker:
            result["speaker"] = board_speaker
        if speaker and speaker != result.get("speaker"):
            report.soft(f"{where}: speaker replaced by the board's attribution of this quote")
        return result
    if owner.get("kind") not in QUOTABLE_KINDS:
        return drop("is not from a transcript or an earnings Key-quotes line")
    sources = inbox.quote_sources(owner)
    matches = find_quote(quote, sources)
    usable = [match for match in matches if match.problem is None]
    if not usable:
        return drop(matches[0].problem if matches else quote_miss(quote, sources))
    best = next((match for match in usable if match.quote == quote), usable[0])
    if len(best.quote.split()) > QUOTE_MAX_WORDS:
        return drop(f"is over {QUOTE_MAX_WORDS} words as the source words it")
    reason = budget.charge(inbox.source_identity(url), best.quote)
    if reason:
        return drop(f"exceeds the excerpt policy ({reason})")
    stats["quotes_kept"] += 1
    if best.quote != quote:
        report.soft(f"{where}: quote replaced by the source's exact wording")
    label = clip(clean_text(str(owner.get("source") or owner.get("title") or ""))
                 or str(owner.get("kind")), LABEL_MAX)[0]
    result = {"quote": best.quote, "label": label}
    if best.source.attribution is None:
        unspoken()
        return result
    attribution = clip(strip_urls(clean_text(best.source.attribution))[0], SPEAKER_MAX)[0]
    if attribution:
        result["speaker"] = attribution
    if speaker and speaker != attribution:
        report.soft(f"{where}: speaker set to the Key-quotes line's own attribution")
    return result


def _normalize_evidence(raw: Any, where: str, inbox: TrustedInbox,
                        on_board: dict[str, dict], report: Report,
                        stats: dict[str, int], budget: QuoteBudget) -> list[dict]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        report.soft(f"{where}: evidence must be a list; ignored")
        return []
    kept: list[dict] = []
    seen: set[str] = set()
    for index, entry in enumerate(raw):
        label_where = f"{where} evidence[{index}]"
        if len(kept) >= MAX_EVIDENCE:
            # Before any quote is checked: entries past the cap must not
            # spend the quote budget.
            report.soft(f"{where}: evidence capped at {MAX_EVIDENCE}")
            break
        if not isinstance(entry, dict) or not isinstance(entry.get("url"), str):
            report.soft(f"{label_where}: not an object with a url; dropped")
            stats["evidence_dropped"] += 1
            continue
        url = entry["url"].strip()
        if url.startswith("<") and url.endswith(">"):
            url = url[1:-1].strip()  # inbox.md shows URLs as <autolinks>
        if safe_url(url) is None:
            report.soft(f"{label_where}: unsafe URL dropped ({fingerprint(url)})")
            stats["evidence_dropped"] += 1
            continue
        owner = inbox.url_owner.get(url)
        existing = on_board.get(url)
        if owner is None and existing is None:
            report.soft(f"{label_where}: URL is not in this run's inbox or on the "
                        f"board; dropped: {_short(url, 120)}")
            stats["evidence_dropped"] += 1
            continue
        if url in seen:
            report.soft(f"{label_where}: duplicate URL dropped")
            continue
        unknown = sorted(set(entry) - set(EVIDENCE_FIELDS) - {"kind", "at"})
        if unknown:
            report.soft(f"{label_where}: unknown fields dropped: {', '.join(unknown)}")
        if owner is not None:
            kind = str(owner.get("kind", ""))
            at = owner.get("at")
            default_label = str(owner.get("source") or owner.get("title") or "")
        else:
            kind = str(existing.get("kind", ""))
            at = existing.get("at")
            default_label = str(existing.get("label") or "")
        if kind not in EVIDENCE_KINDS:
            report.soft(f"{label_where}: source kind {kind!r} is not publishable; dropped")
            stats["evidence_dropped"] += 1
            continue
        label = entry.get("label")
        label_text = strip_urls(clean_text(label))[0] if isinstance(label, str) else ""
        if not label_text:
            label_text = clean_text(default_label) or kind
            if label is not None:
                report.soft(f"{label_where}: empty or invalid label replaced")
        label_text, cut = clip(label_text, LABEL_MAX)
        if cut:
            report.soft(f"{label_where}: label truncated to {LABEL_MAX} characters")
        normalized: dict[str, Any] = {"url": url, "kind": kind, "label": label_text}
        if isinstance(at, str) and at:
            normalized["at"] = at
        quoted = _evidence_quote(entry, label_where, url, owner, existing, inbox, report,
                                 stats, budget)
        if quoted:
            if quoted["label"] != label_text:
                report.soft(f"{label_where}: label set to the source's name because the "
                            "evidence carries a quote")
            normalized["label"] = quoted["label"]
            if "speaker" in quoted:
                normalized["speaker"] = quoted["speaker"]
            normalized["quote"] = quoted["quote"]
        seen.add(url)
        kept.append(normalized)
    stats["evidence_kept"] += len(kept)
    return kept


def repair_script(lines: list[str], report: Report) -> list[str]:
    """Soft repairs: URLs, markdown, unknown/excess tags, blank lines."""
    counts = {tag: 0 for tag in TAG_LIMITS}
    total = 0
    repaired: list[str] = []
    for index, raw in enumerate(lines):
        where = f"script[{index}]"
        line = clean_text(raw)
        if not line:
            report.soft(f"{where}: blank line dropped")
            continue
        line, had_url = strip_urls(line)
        if had_url:
            report.soft(f"{where}: URL stripped")
        if MARKDOWN_CHARS_RE.search(line):
            line = MARKDOWN_CHARS_RE.sub("", line)
            report.soft(f"{where}: markdown characters stripped")

        def bracket(match: re.Match) -> str:
            token = match.group(0)
            if KNOWN_TAG_RE.fullmatch(token):
                return token
            report.soft(f"{where}: unknown audio tag {_short(token, 40)} stripped")
            return " "

        line = BRACKET_TOKEN_RE.sub(bracket, line)
        if ANGLE_TOKEN_RE.search(line):
            line = ANGLE_TOKEN_RE.sub(" ", line)
            report.soft(f"{where}: angle-bracket tag stripped")

        emphasis_open = False

        def limit(match: re.Match) -> str:
            nonlocal total, emphasis_open
            token = match.group(0)
            if token == "[/emphasis]":
                if emphasis_open:
                    emphasis_open = False
                    return token
                return " "
            if token == "[emphasis]" and emphasis_open:
                return " "
            if counts[token] >= TAG_LIMITS[token] or total >= MAX_TAGS:
                report.soft(f"{where}: excess {token} tag stripped")
                return " "
            counts[token] += 1
            total += 1
            if token == "[emphasis]":
                emphasis_open = True
            return token

        line = KNOWN_TAG_RE.sub(limit, line)
        if emphasis_open:
            line = line + "[/emphasis]"
        repaired.append(" ".join(line.split()))
    return repaired


def validate_edit(edit: Any, inbox: TrustedInbox, board: dict
                  ) -> tuple[dict | None, Report]:
    """Return (normalized edit or None on hard error, report)."""
    report = Report()
    stats = {"creates": 0, "updates": 0, "resolves": 0, "evidence_kept": 0,
             "evidence_dropped": 0, "quotes_kept": 0, "quotes_dropped": 0,
             "script_lines": 0, "script_words": 0}
    if not isinstance(edit, dict):
        report.hard("edit must be a JSON object")
        return None, report
    schema = edit.get("schema")
    if isinstance(schema, bool) or schema != SCHEMA:
        report.hard(f"schema must be {SCHEMA}")
    unknown = sorted(set(edit) - set(TOP_LEVEL_KEYS) - set(NORMALIZED_ONLY_KEYS))
    if unknown:
        report.soft(f"unknown top-level fields dropped: {', '.join(_short(k, 30) for k in unknown)}")
    on_air = edit.get("on_air")
    if not isinstance(on_air, bool):
        report.hard("on_air must be true or false")
    headline_raw = edit.get("headline")
    headline = ""
    if not isinstance(headline_raw, str) or not clean_text(headline_raw):
        report.hard("headline must be a non-empty string")
    else:
        headline, had_url = strip_urls(clean_text(headline_raw))
        if had_url:
            report.soft("URL stripped from headline")
        if not headline:
            report.hard("headline must contain text, not only a URL")
        headline, cut = clip(headline, HEADLINE_MAX)
        if cut:
            report.soft(f"headline truncated to {HEADLINE_MAX} characters")
    note = ""
    note_raw = edit.get("note")
    if note_raw is not None:
        if isinstance(note_raw, str):
            note, had_url = strip_urls(clean_text(note_raw))
            if had_url:
                report.soft("URL stripped from note")
            note, cut = clip(note, NOTE_MAX)
            if cut:
                report.soft(f"note truncated to {NOTE_MAX} characters")
        else:
            report.soft("note must be a string; dropped")

    threads = {t.get("slug"): t for t in board.get("threads") or []
               if isinstance(t, dict) and isinstance(t.get("slug"), str)}
    simulated = {slug: str(thread.get("status", "")) for slug, thread in threads.items()}
    on_board = board_evidence(board)
    budget = QuoteBudget.from_board(board, inbox)

    ops_raw = edit.get("ops")
    normalized_ops: list[dict] = []
    if not isinstance(ops_raw, list):
        report.hard("ops must be a list")
        ops_raw = []
    for index, op in enumerate(ops_raw):
        where = f"ops[{index}]"
        if not isinstance(op, dict):
            report.hard(f"{where}: op must be an object")
            continue
        name = op.get("op")
        if name not in OP_FIELDS:
            report.hard(f"{where}: unknown op {_short(name, 30)!r}")
            continue
        slug = op.get("slug")
        if not isinstance(slug, str) or len(slug) > SLUG_MAX or not SLUG_RE.match(slug):
            report.hard(f"{where}: malformed slug {_short(slug, 70)!r} "
                        f"(lowercase kebab-case, at most {SLUG_MAX} characters)")
            continue
        where = f"{where} {name} {slug}"
        op = dict(op)
        if name == "update" and "evidence" in op and "add_evidence" not in op:
            op["add_evidence"] = op.pop("evidence")
            report.soft(f"{where}: 'evidence' on update treated as add_evidence")
        if name == "create" and "add_evidence" in op and "evidence" not in op:
            op["evidence"] = op.pop("add_evidence")
            report.soft(f"{where}: 'add_evidence' on create treated as evidence")
        extra = sorted(set(op) - set(OP_FIELDS[name]))
        if extra:
            report.soft(f"{where}: unknown fields dropped: "
                        f"{', '.join(_short(k, 30) for k in extra)}")
        if name == "create":
            if slug in simulated:
                report.hard(f"{where}: slug already exists on the board")
                continue
            stats["creates"] += 1
        elif slug not in simulated:
            report.hard(f"{where}: unknown slug (not on the board)")
            continue

        errors_before = len(report.errors)
        values: dict[str, Any] = {}
        for text_field in ("title", "now", "changed", "watch", "change"):
            if text_field not in OP_FIELDS[name]:
                continue
            required = text_field in REQUIRED_FIELDS[name]
            # `watch` may be cleared ("nothing scheduled"); title/now may not.
            value = _text_field(op, text_field, where, report, required=required,
                                allow_empty=text_field == "watch")
            if value is not None:
                values[text_field] = value
        if len(report.errors) > errors_before:
            continue

        out: dict[str, Any] = {"op": name, "slug": slug}
        if name == "create":
            status = _status(op["status"], where, report) if "status" in op else None
            importance = (_importance(op["importance"], where, report)
                          if "importance" in op else None)
            out.update({
                "title": values["title"],
                "status": status or "developing",
                "importance": importance if importance is not None else 3,
                "now": values["now"],
                "changed": values["changed"],
                "watch": values.get("watch", ""),
                "evidence": _normalize_evidence(op.get("evidence"), where, inbox,
                                                on_board, report, stats, budget),
                "change": values["change"],
            })
            simulated[slug] = out["status"]
        elif name == "update":
            stats["updates"] += 1
            if "title" in values:
                out["title"] = values["title"]
            if "status" in op:
                status = _status(op["status"], where, report)
                if status:
                    out["status"] = status
            if "importance" in op:
                importance = _importance(op["importance"], where, report)
                if importance is not None:
                    out["importance"] = importance
            if "now" in values:
                out["now"] = values["now"]
            out["changed"] = values["changed"]
            if "watch" in values:
                out["watch"] = values["watch"]
            if "add_evidence" in op:
                out["add_evidence"] = _normalize_evidence(
                    op.get("add_evidence"), where, inbox, on_board, report, stats, budget)
            out["change"] = values["change"]
            if "status" in out:
                simulated[slug] = out["status"]
            elif simulated.get(slug) == "resolved":
                report.soft(f"{where}: update of a resolved thread keeps it resolved; "
                            "set status to reopen it")
        else:
            stats["resolves"] += 1
            if simulated.get(slug) == "resolved":
                report.soft(f"{where}: thread is already resolved")
            out["changed"] = values["changed"]
            out["change"] = values["change"]
            simulated[slug] = "resolved"
        normalized_ops.append(out)

    if stats["creates"] > MAX_CREATES:
        report.hard(f"{stats['creates']} create ops; at most {MAX_CREATES} per run")

    script: list[str] = []
    covers: list[str] = []
    script_raw = edit.get("script")
    covers_raw = edit.get("covers")
    if on_air is True:
        if not isinstance(script_raw, list) or not all(isinstance(line, str)
                                                       for line in script_raw):
            report.hard("on_air requires script: a list of strings")
        else:
            script = repair_script(script_raw, report)
            bad = [i for i, line in enumerate(script) if not SCRIPT_LINE_RE.match(line)]
            for i in bad[:5]:
                report.hard(f"script line {i + 1} does not start with "
                            f"'Speaker 1: ' or 'Speaker 2: ' followed by text")
            if not (SCRIPT_LINES[0] <= len(script) <= SCRIPT_LINES[1]):
                report.hard(f"script has {len(script)} lines; must be "
                            f"{SCRIPT_LINES[0]}-{SCRIPT_LINES[1]}")
            words = count_spoken_words(script)
            stats["script_lines"] = len(script)
            stats["script_words"] = words
            if not (SCRIPT_WORDS[0] <= words <= SCRIPT_WORDS[1]):
                report.hard(f"script has {words} spoken words; must be "
                            f"{SCRIPT_WORDS[0]}-{SCRIPT_WORDS[1]}")
        if covers_raw is None:
            report.soft("on_air without covers; recorded as an empty list")
        elif not isinstance(covers_raw, list) or not all(isinstance(slug, str)
                                                         for slug in covers_raw):
            report.hard("covers must be a list of slugs")
        else:
            for slug in covers_raw:
                if slug in covers:
                    report.soft(f"covers: duplicate {_short(slug, 70)} dropped")
                    continue
                if slug not in simulated:
                    report.hard(f"covers: {_short(slug, 70)!r} is not on the board "
                                "after the ops")
                    continue
                covers.append(slug)
            if not covers and not report.errors:
                report.soft("on_air with an empty covers list")
    elif on_air is False:
        if script_raw:
            report.soft("script ignored because on_air is false")
        if covers_raw:
            report.soft("covers ignored because on_air is false")
        if not note:
            report.soft("on_air is false but no note explains why")

    if report.errors:
        return None, report
    normalized = {
        "schema": SCHEMA,
        "on_air": on_air,
        "headline": headline,
        "ops": normalized_ops,
        "script": script,
        "covers": covers,
        "note": note,
        "warnings": list(report.warnings),
        "stats": stats,
    }
    return normalized, report


def read_edit_file(path: Path) -> Any:
    """Read the untrusted artifact defensively (regular file, bounded size)."""
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"{path} is missing or not a regular file")
    size = path.stat().st_size
    if size > MAX_EDIT_BYTES:
        raise ValueError(f"{path} is {size} bytes; limit is {MAX_EDIT_BYTES}")
    raw = path.read_bytes()
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path} is not valid UTF-8 JSON: {exc}") from exc


def write_github_output(path: str | None, values: dict[str, str]) -> None:
    if not path:
        return
    with open(path, "a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--edit", type=Path, required=True)
    parser.add_argument("--inbox", type=Path, required=True,
                        help="trusted inbox.json (host copy, outside .tmp/ and .agent-input/)")
    parser.add_argument("--state", type=Path, required=True,
                        help="research/aradio/state.json (may not exist yet)")
    parser.add_argument("--out", type=Path, required=True,
                        help="normalized edit JSON for the TTS step and the writer")
    parser.add_argument("--github-output", default=None)
    args = parser.parse_args(argv)

    try:
        inbox = TrustedInbox.load(args.inbox)
        board = load_board(args.state)
    except (OSError, ValueError) as exc:
        print(f"::error::aradio validator: cannot load trusted inputs: {gh_escape(exc)}")
        return EXIT_HARD
    try:
        edit = read_edit_file(args.edit)
    except (OSError, ValueError) as exc:
        print(f"::error::aradio edit rejected: {gh_escape(exc)}")
        return EXIT_HARD

    normalized, report = validate_edit(edit, inbox, board)
    for warning in report.warnings[:40]:
        print(f"::warning::aradio edit repaired: {gh_escape(warning)}")
    if len(report.warnings) > 40:
        print(f"::warning::aradio edit: {len(report.warnings) - 40} more repairs not shown")
    if normalized is None:
        for error in report.errors[:40]:
            print(f"::error::aradio edit rejected: {gh_escape(error)}")
        print(f"aradio edit: {len(report.errors)} hard error(s); nothing will be "
              "published and the cursor will not advance")
        return EXIT_HARD

    atomic_write_json(args.out, normalized)
    stats = normalized["stats"]
    print(f"aradio edit OK: on_air={str(normalized['on_air']).lower()} "
          f"creates={stats['creates']} updates={stats['updates']} "
          f"resolves={stats['resolves']} script_lines={stats['script_lines']} "
          f"script_words={stats['script_words']} warnings={len(report.warnings)}")
    write_github_output(args.github_output, {
        "on_air": "true" if normalized["on_air"] else "false",
        "script_words": str(stats["script_words"]),
        "warnings": str(len(report.warnings)),
    })
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
