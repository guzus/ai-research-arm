#!/usr/bin/env python3
"""Fetch AI-exposed issuer earnings signal from SEC EDGAR into a per-event lane.

Two tiers, and the second one is always optional:

  Tier 1 (authoritative, never skipped) - the issuer's own earnings filing on
  EDGAR. Domestic filers announce results in an 8-K carrying Item 2.02;
  foreign private issuers (TSM, ARM) use a 6-K, whose ``items`` field the
  submissions API returns EMPTY, so they need a separate structural test. From
  the filing we read the EX-99 exhibits (press release, CFO commentary,
  shareholder letter) and pull SHORT attributed excerpts plus the headline
  figures the issuer itself printed.

  Tier 2 (best-effort) - the issuer's OWN investor-relations transcript of the
  call, discovered through the Q4 Inc IR-platform event feed or a per-issuer
  URL template. We record a LINK and provenance only. Every Tier 2 failure is
  non-fatal: the event file is still written from Tier 1.

Licensing posture, enforced in code rather than prose: everything quoted here
was deliberately disseminated to the public by the issuer under Reg FD, and we
publish only short attributed excerpts as news reporting. ``MAX_QUOTES`` /
``MAX_QUOTE_WORDS`` / ``MAX_HEADLINE_ITEMS`` cap that mechanically, and no
transcript body is ever fetched, stored, or rendered - only its URL. Third-
party transcript vendors (Alpha Vantage, FMP, Seeking Alpha, Motley Fool) are
deliberately absent: their terms forbid the republication this lane performs.

Empty is NOT an outage here - it is the normal state ~325 days a year, so this
lane INVERTS the youtube lane's rule: it writes nothing and exits 0 when no
issuer reported, and exits EXIT_TOTAL_FETCH_FAILURE only when every tracked
issuer's SEC fetch failed (a real EDGAR outage during earnings week).
"""

from __future__ import annotations

import argparse
import calendar
import dataclasses
import datetime as dt
import html
import json
import os
import re
import ssl
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "data" / "sources" / "earnings_issuers.json"
DEFAULT_OUT_DIR = REPO_ROOT / "research" / "earnings"

# SEC fair access (https://www.sec.gov/search-filings/edgar-search-assistance/
# accessing-edgar-data) requires a declared CONTACT in the User-Agent and caps
# traffic at 10 requests/second. The contact must be an address, not a URL:
# verified 2026-08-01 from this host, "ai-research-arm/1.0 (https://github.com/
# guzus/ai-research-arm)" gets HTTP 403 while the e-mail form gets HTTP 200.
# That is also why SEC fetches do NOT go through scripts/source_cache.py -
# its fixed User-Agent carries a GitHub URL and is 403'd by both www.sec.gov
# and data.sec.gov. Do not "simplify" this into source_cache without re-testing.
DEFAULT_CONTACT = "birdyopensource@gmail.com"
USER_AGENT_TEMPLATE = "ai-research-arm/1.0 ({contact})"
TIMEOUT_SECONDS = 25
# ~5 req/s worst case, half the published ceiling. 18 issuers x <=5 requests
# stays well under a minute even with the sleep.
REQUEST_INTERVAL_SECONDS = 0.2
RETRY_DELAY_SECONDS = 2.0

# Exit code for "every tracked issuer's SEC fetch failed". Distinct from 2
# (argument/registry validation) so the workflow can tell an EDGAR outage from
# a bad invocation. Mirrors scripts/fetch_youtube_signal.py.
EXIT_TOTAL_FETCH_FAILURE = 3

# Republication guards. These ARE the licensing position, so they live in code
# and are enforced by scripts/test_fetch_earnings_signal.py.
MAX_QUOTES = 6
MAX_QUOTE_WORDS = 60
MAX_HEADLINE_ITEMS = 6
MAX_HEADLINE_WORDS = 40
MAX_TRANSCRIPT_LINKS = 3
# Exhibits are HTML; the largest observed earnings release is ~900KB.
MAX_DOCUMENT_BYTES = 8 * 1024 * 1024
MAX_EXHIBITS_PER_FILING = 4

SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
SEC_FILING_BASE = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession_nodash}"

PRIORITIES = ("P0", "P1", "P2")
FILER_TYPES = ("domestic", "fpi")
TRANSCRIPT_SOURCES = ("q4-event-feed", "url-template", "none")

# Domestic earnings announcements are Item 2.02 ("Results of Operations and
# Financial Condition") of Form 8-K.
EARNINGS_ITEM = "2.02"

# FPI gate 3: the 6-K cover page + its exhibit descriptions have to read like
# an earnings report. Verified against the real text of ARM
# 0001973239-26-000113 ("99.1 Earnings Press Release dated July 29, 2026") and
# TSM 0001046179-26-000451 ("99.2 2026 Second Quarter Earnings Conference
# Presentation Material").
DEFAULT_FPI_MATCH = r"(?i)earnings|results of operations|financial results|quarter(?:ly)? results"
# FPI gate 1, applied FIRST and to the primary document FILENAME - never to
# document text, where "revenue" appears in every genuine earnings release.
# TSM files monthly revenue 6-Ks (tsm-revenue*.htm, tsm-monthend6k*.htm).
DEFAULT_FPI_EXCLUDE = r"(?i)revenue|month[-_ ]?end"

DEFAULT_TRANSCRIPT_ATTACHMENT_MATCH = r"(?i)transcript"
# NVIDIA titles its call "NVIDIA 1st Quarter FY27 Financial Results", Alphabet
# "2026 Q2 Earnings Call" - hence both alternatives.
DEFAULT_TRANSCRIPT_EVENT_MATCH = r"(?i)earnings|financial results|quarter(?:ly)? results"
TRANSCRIPT_EVENT_WINDOW_DAYS = 3

Q4_EVENT_FEED_PATH = "/feed/Event.svc/GetEventList"
Q4_EVENT_FEED_PARAMS = {
    "LanguageId": "1",
    "bodyType": "0",
    "eventDateTime": "1",
    "includeTags": "false",
    "excludeSelection": "1",
}

# EDGAR's filing index page carries an authoritative per-document Type column
# (EX-99.1, EX-101.SCH, GRAPHIC, ...). Reading it beats guessing from
# filenames, which is unreliable in both directions: NVDA's press release is
# `q1fy27pr.htm` and TSMC's is `a2q26e_withguidancexfinal.htm`.
TABLE_ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S | re.I)
TABLE_CELL_RE = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S | re.I)
EXHIBIT_TYPE_RE = re.compile(r"(?i)^EX-99(?:\.(\d+))?$")

HEADLINE_KEY_RE = re.compile(
    r"(?i)\b(revenue|earnings per share|EPS|operating income|net income|gross margin|"
    r"operating margin|data ?cent(?:er|re) revenue|cloud revenue|free cash flow|"
    r"capital expenditures|backlog|bookings|guidance)\b"
)
HEADLINE_FIGURE_RE = re.compile(r"\$\s?[\d.,]+|\d+(?:\.\d+)?\s?%")
# A flattened financial-statement table clears every other test (it is full of
# key terms and figures) and would otherwise be published as a "headline
# number". Two tells separate it from a real bullet: figure density, and the
# accounting-negative "$(480)" form that only appears inside tables.
MAX_FIGURES_PER_HEADLINE = 5
ACCOUNTING_NEGATIVE_RE = re.compile(r"\$\s?\(")
# EDGAR prepends its own document header to every exhibit it serves, e.g.
# "EX-99.1 2 q1fy27pr.htm EX-99.1 Document NVIDIA Announces ...". Strip it so
# the first extracted segment is the issuer's prose, not EDGAR's plumbing.
EDGAR_PREAMBLE_RE = re.compile(
    r"^(?:EX-[\w.\-]+|\d+-K|10-[QK])\s+\d+\s+\S+\.html?\s+"
    r"(?:(?:EX-[\w.\-]+|\d+-K|10-[QK]|Document|Exhibit\s+[\w.]+)\s+)*",
    re.IGNORECASE,
)
# 900 chars is ~150 words, already 2.5x the publish cap, and it is empirically
# the right ceiling: quote marks in an earnings release are not always balanced
# (footnote markers, nested quotes), so a wider window lets one stray mark pair
# with a distant one and swallow the real quotes inside a boilerplate span.
# Raising it to 2500 was tried against Vertiv's 2026-07-29 EX-99.1 and produced
# exactly that - both CEO quotes vanished into a misattributed non-GAAP
# paragraph. Dropping an over-long quote is the correct failure direction;
# publishing a misattributed one is not.
QUOTE_SPAN_RE = re.compile(r'"([^"]{40,900})"')
SAID_AFTER_RE = re.compile(
    r"^[,.]?\s*(?:said|added|commented|noted)\s+((?:[A-Z][\w'.\-]*)(?:\s+[A-Z][\w'.\-]*){0,3}"
    r"(?:\s*,\s*[^.\"]{0,120})?)"
)
SAID_BEFORE_RE = re.compile(
    r"((?:[A-Z][\w'.\-]*)(?:\s+[A-Z][\w'.\-]*){0,3}(?:\s*,\s*[^.\"]{0,120})?)"
    r"\s*(?:said|added|commented|noted)\s*[:,]?\s*$"
)
TAG_RE = re.compile(r"<[^>]+>")
ASCII_TRANSLATION = str.maketrans({
    "‘": "'",
    "’": "'",
    "‚": "'",
    "“": '"',
    "”": '"',
    "„": '"',
    "–": "-",
    "—": "-",
    "―": "-",
    "…": "...",
    " ": " ",
    " ": " ",
    " ": " ",
    " ": " ",
    "•": "*",
})
EVENT_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([A-Z0-9.\-]+)-(FY\d{2}Q\d)\.md$")


# ---------------------------------------------------------------------------
# Registry


@dataclasses.dataclass(frozen=True)
class Issuer:
    id: str
    ticker: str
    name: str
    cik: str
    filer_type: str
    fiscal_year_end: str
    priority: str
    tags: tuple[str, ...]
    include_in_digest: bool
    transcript: dict[str, str]
    fpi_match: str
    fpi_exclude_match: str
    notes: str = ""

    @property
    def cik_int(self) -> int:
        return int(self.cik)


@dataclasses.dataclass(frozen=True)
class Document:
    doc_type: str
    description: str
    name: str
    url: str
    size: int

    @property
    def label(self) -> str:
        return self.doc_type or self.name


@dataclasses.dataclass(frozen=True)
class Quote:
    speaker: str
    text: str
    source_label: str
    source_url: str
    truncated: bool


@dataclasses.dataclass(frozen=True)
class TranscriptLink:
    title: str
    url: str
    provider: str


@dataclasses.dataclass
class EarningsEvent:
    issuer: Issuer
    form: str
    items: str
    accession: str
    filing_date: dt.date
    report_date: str
    acceptance: str
    primary_document: str
    fiscal_year: int
    fiscal_quarter: int
    sec_fiscal_year_end: str = ""
    documents: list[Document] = dataclasses.field(default_factory=list)
    headline: list[str] = dataclasses.field(default_factory=list)
    quotes: list[Quote] = dataclasses.field(default_factory=list)
    transcripts: list[TranscriptLink] = dataclasses.field(default_factory=list)
    notes: list[str] = dataclasses.field(default_factory=list)

    @property
    def period(self) -> str:
        return period_label(self.fiscal_year, self.fiscal_quarter)

    @property
    def filing_base_url(self) -> str:
        return SEC_FILING_BASE.format(
            cik_int=self.issuer.cik_int,
            accession_nodash=self.accession.replace("-", ""),
        )

    @property
    def filename(self) -> str:
        return f"{self.filing_date.isoformat()}-{self.issuer.ticker}-{self.period}.md"


def _build_ssl_context() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE")
    if cafile and os.path.isfile(cafile):
        return ssl.create_default_context(cafile=cafile)
    for path in (
        "/etc/ssl/cert.pem",
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/pki/tls/certs/ca-bundle.crt",
        "/opt/homebrew/etc/openssl@3/cert.pem",
        "/usr/local/etc/openssl@3/cert.pem",
    ):
        if os.path.isfile(path):
            return ssl.create_default_context(cafile=path)
    return ssl.create_default_context()


SSL_CTX = _build_ssl_context()


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def ascii_safe(value: str) -> str:
    value = value.translate(ASCII_TRANSLATION)
    value = value.encode("ascii", "ignore").decode("ascii")
    return "\n".join(line.rstrip() for line in value.splitlines()).strip()


def normalize_text(value: str) -> str:
    """Unicode-normalized, tag-free, single-spaced text for PARSING.

    Deliberately not ``ascii_safe``: bullet markers and dashes survive here so
    segmentation works; ASCII folding happens once, at render time.
    """
    value = TAG_RE.sub(" ", value)
    value = html.unescape(value)
    value = value.translate(ASCII_TRANSLATION)
    value = re.sub(r"[ \t\r\f\v]+", " ", value).strip()
    return EDGAR_PREAMBLE_RE.sub("", value)


def _validate_regex(pattern: str, field: str, issuer_id: str) -> None:
    try:
        re.compile(pattern)
    except re.error as exc:
        raise ValueError(f"{issuer_id}: invalid regex in {field}: {exc}") from exc


def load_issuers(path: Path) -> list[Issuer]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("earnings issuer registry must be a JSON array")
    seen_ids: set[str] = set()
    seen_ciks: set[str] = set()
    seen_tickers: set[str] = set()
    issuers: list[Issuer] = []
    for row in raw:
        if not isinstance(row, dict):
            raise ValueError("each earnings issuer must be an object")
        transcript = row.get("transcript") or {"source": "none"}
        if not isinstance(transcript, dict):
            raise ValueError(f"{row.get('id')}: transcript must be an object")
        issuer = Issuer(
            id=clean_text(row.get("id")),
            ticker=clean_text(row.get("ticker")).upper(),
            name=clean_text(row.get("name")),
            cik=clean_text(row.get("cik")),
            filer_type=clean_text(row.get("filer_type")),
            fiscal_year_end=clean_text(row.get("fiscal_year_end")),
            priority=clean_text(row.get("priority")),
            tags=tuple(clean_text(tag) for tag in row.get("tags", [])),
            include_in_digest=bool(row.get("include_in_digest", True)),
            transcript={key: clean_text(value) for key, value in transcript.items()},
            fpi_match=clean_text(row.get("fpi_match")) or DEFAULT_FPI_MATCH,
            fpi_exclude_match=clean_text(row.get("fpi_exclude_match")) or DEFAULT_FPI_EXCLUDE,
            notes=clean_text(row.get("notes")),
        )
        if not issuer.id or not issuer.ticker or not issuer.name:
            raise ValueError("earnings issuers require id, ticker and name")
        if issuer.id in seen_ids:
            raise ValueError(f"duplicate issuer id: {issuer.id}")
        if issuer.ticker in seen_tickers:
            raise ValueError(f"duplicate issuer ticker: {issuer.ticker}")
        # A 10-digit zero-padded STRING; an int would drop MSFT's leading zeros
        # and 404 the submissions endpoint.
        if not re.fullmatch(r"\d{10}", issuer.cik):
            raise ValueError(f"{issuer.id}: cik must be a 10-digit zero-padded string")
        if issuer.cik in seen_ciks:
            raise ValueError(f"duplicate issuer cik: {issuer.cik}")
        if issuer.filer_type not in FILER_TYPES:
            raise ValueError(f"{issuer.id}: invalid filer_type {issuer.filer_type!r}")
        if not re.fullmatch(r"\d{2}-\d{2}", issuer.fiscal_year_end):
            raise ValueError(f"{issuer.id}: fiscal_year_end must be MM-DD")
        month, day = (int(part) for part in issuer.fiscal_year_end.split("-"))
        if not 1 <= month <= 12 or not 1 <= day <= 31:
            raise ValueError(
                f"{issuer.id}: fiscal_year_end {issuer.fiscal_year_end!r} is not a date"
            )
        if issuer.priority not in PRIORITIES:
            raise ValueError(f"{issuer.id}: invalid priority {issuer.priority!r}")
        source = issuer.transcript.get("source", "none")
        if source not in TRANSCRIPT_SOURCES:
            raise ValueError(f"{issuer.id}: invalid transcript.source {source!r}")
        if source == "q4-event-feed" and not issuer.transcript.get("host"):
            raise ValueError(f"{issuer.id}: transcript.source=q4-event-feed requires host")
        if source == "url-template" and not issuer.transcript.get("url_template"):
            raise ValueError(f"{issuer.id}: transcript.source=url-template requires url_template")
        _validate_regex(issuer.fpi_match, "fpi_match", issuer.id)
        _validate_regex(issuer.fpi_exclude_match, "fpi_exclude_match", issuer.id)
        _validate_regex(
            issuer.transcript.get("attachment_match") or DEFAULT_TRANSCRIPT_ATTACHMENT_MATCH,
            "transcript.attachment_match",
            issuer.id,
        )
        _validate_regex(
            issuer.transcript.get("event_match") or DEFAULT_TRANSCRIPT_EVENT_MATCH,
            "transcript.event_match",
            issuer.id,
        )
        seen_ids.add(issuer.id)
        seen_ciks.add(issuer.cik)
        seen_tickers.add(issuer.ticker)
        issuers.append(issuer)
    return issuers


# ---------------------------------------------------------------------------
# Fetch boundary


class FetchError(Exception):
    """Any network/HTTP failure. Callers handle these at the lane boundary."""


FetchBytes = Callable[[str, str], bytes]

_last_request_at = 0.0


def http_get(url: str, accept: str = "*/*", *, contact: str = DEFAULT_CONTACT,
             max_read: int | None = None) -> bytes:
    """Rate-limited GET with the SEC-mandated contact User-Agent.

    One retry on the transient shapes SEC actually emits (429 throttle, 5xx,
    socket errors); 403/404 fail immediately because retrying a rejected
    User-Agent or a missing document only burns request budget.
    """
    global _last_request_at
    headers = {
        "User-Agent": USER_AGENT_TEMPLATE.format(contact=contact),
        "Accept": accept,
        "Accept-Encoding": "identity",
    }
    attempts = 0
    while True:
        attempts += 1
        elapsed = time.monotonic() - _last_request_at
        if elapsed < REQUEST_INTERVAL_SECONDS:
            time.sleep(REQUEST_INTERVAL_SECONDS - elapsed)
        _last_request_at = time.monotonic()
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS, context=SSL_CTX) as resp:
                return resp.read(max_read) if max_read else resp.read()
        except urllib.error.HTTPError as exc:
            transient = exc.code == 429 or 500 <= exc.code < 600
            if transient and attempts == 1:
                time.sleep(RETRY_DELAY_SECONDS)
                continue
            raise FetchError(f"HTTP {exc.code} for {url}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if attempts == 1:
                time.sleep(RETRY_DELAY_SECONDS)
                continue
            raise FetchError(f"{type(exc).__name__}: {exc} for {url}") from exc


def fetch_json(url: str, fetch_fn: FetchBytes) -> Any:
    payload = fetch_fn(url, "application/json")
    try:
        # Some IR platforms serve the feed with a UTF-8 BOM.
        return json.loads(payload.decode("utf-8-sig", errors="replace"))
    except json.JSONDecodeError as exc:
        raise FetchError(f"invalid JSON from {url}: {exc}") from exc


def fetch_html(url: str, fetch_fn: FetchBytes) -> str:
    return fetch_fn(url, "text/html").decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Fiscal period labelling


def _last_day(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


def shift_months(value: dt.date, months: int) -> dt.date:
    """Shift by whole months, clamping to the target month's last day."""
    total = (value.year * 12 + value.month - 1) + months
    year, month = divmod(total, 12)
    month += 1
    return dt.date(year, month, min(value.day, _last_day(year, month)))


def fiscal_period(fiscal_year_end: str, filing_date: dt.date) -> tuple[int, int]:
    """(fiscal year, quarter) for the quarter that ended most recently.

    The 8-K's own ``reportDate`` is the ANNOUNCEMENT date, not the period end
    (MSFT: reportDate 2026-07-29 for the quarter ended 2026-06-30), so the
    period is derived from the issuer's fiscal-year-end instead. The fiscal
    year is labelled by the calendar year in which it ENDS, which is the
    convention every issuer in the registry uses (NVDA's Jan-2027 year is
    "FY27", MSFT's Jun-2026 year is "FY26").

    52/53-week filers drift a few days from the calendar month end; that only
    matters for a filing landing within days of the boundary, which no issuer
    does (the shortest observed announce-after-quarter-end gap is ~3 weeks).
    """
    month, day = (int(part) for part in fiscal_year_end.split("-"))
    best: tuple[dt.date, int, int] | None = None
    for year in (filing_date.year - 1, filing_date.year, filing_date.year + 1):
        year_end = dt.date(year, month, min(day, _last_day(year, month)))
        for quarter in (1, 2, 3, 4):
            quarter_end = shift_months(year_end, -3 * (4 - quarter))
            if quarter_end > filing_date:
                continue
            if best is None or quarter_end > best[0]:
                best = (quarter_end, year, quarter)
    if best is None:  # pragma: no cover - unreachable for any real filing date
        raise ValueError(f"cannot derive fiscal period for {fiscal_year_end} / {filing_date}")
    return best[1], best[2]


def period_label(fiscal_year: int, quarter: int) -> str:
    return f"FY{fiscal_year % 100:02d}Q{quarter}"


# ---------------------------------------------------------------------------
# Tier 1: EDGAR


def recent_rows(submissions: dict[str, Any]) -> list[dict[str, str]]:
    """Flatten ``filings.recent``'s parallel arrays into row dicts."""
    recent = ((submissions or {}).get("filings") or {}).get("recent") or {}
    rows: list[dict[str, str]] = []
    for index, form in enumerate(recent.get("form") or []):
        def at(key: str) -> str:
            values = recent.get(key) or []
            return clean_text(values[index]) if index < len(values) else ""

        rows.append({
            "form": clean_text(form),
            "items": at("items"),
            "accession": at("accessionNumber"),
            "filingDate": at("filingDate"),
            "reportDate": at("reportDate"),
            "acceptance": at("acceptanceDateTime"),
            "primaryDocument": at("primaryDocument"),
        })
    return rows


def in_window(filing_date: str, target: dt.date, lookback_days: int) -> bool:
    try:
        parsed = dt.date.fromisoformat(filing_date)
    except ValueError:
        return False
    return target - dt.timedelta(days=lookback_days) <= parsed <= target


def filing_base_url(cik: str, accession: str) -> str:
    return SEC_FILING_BASE.format(
        cik_int=int(cik), accession_nodash=accession.replace("-", "")
    )


def _cell_text(cell: str) -> str:
    return clean_text(html.unescape(TAG_RE.sub(" ", cell)).replace(" ", " "))


def parse_filing_documents(body: str, base_url: str) -> list[Document]:
    """Documents from an EDGAR filing index page, with their authoritative Type.

    The "Document Format Files" table is EDGAR-generated and stable; its Type
    column is what separates an EX-99.1 press release from XBRL viewer chrome
    without ever guessing at a filename.
    """
    documents: list[Document] = []
    seen: set[str] = set()
    for row in TABLE_ROW_RE.findall(body):
        cells = [_cell_text(cell) for cell in TABLE_CELL_RE.findall(row)]
        if len(cells) < 4 or cells[0].lower() in {"seq", ""}:
            continue
        description, document_cell, doc_type = cells[1], cells[2], cells[3]
        name = document_cell.split(" ")[0].strip()
        if not name or name in seen:
            continue
        try:
            size = int(cells[4]) if len(cells) > 4 and cells[4].isdigit() else 0
        except ValueError:
            size = 0
        seen.add(name)
        documents.append(
            Document(
                doc_type=doc_type if doc_type and doc_type != " " else "",
                description=description,
                name=name,
                url=f"{base_url}/{name}",
                size=size,
            )
        )
    return documents


def fetch_filing_documents(
    issuer: Issuer, accession: str, fetch_fn: FetchBytes
) -> list[Document]:
    base = filing_base_url(issuer.cik, accession)
    body = fetch_html(f"{base}/{accession}-index.html", fetch_fn)
    return parse_filing_documents(body, base)


def exhibit_documents(documents: list[Document]) -> list[Document]:
    """EX-99* HTML exhibits, EX-99.1 first.

    That single structural test is what separates a real earnings 6-K (ARM
    0001973239-26-000113: EX-99.1 + EX-99.2) from the interim-financials 6-K
    filed three minutes later (ARM ...000114: no exhibits at all) and from
    TSM's monthly revenue 6-K (also none).
    """
    exhibits: list[Document] = []
    for document in documents:
        match = EXHIBIT_TYPE_RE.match(document.doc_type)
        if not match:
            continue
        if not document.name.lower().endswith((".htm", ".html")):
            continue
        exhibits.append(document)
    return sorted(
        exhibits,
        key=lambda document: (
            int(EXHIBIT_TYPE_RE.match(document.doc_type).group(1) or 99),  # type: ignore[union-attr]
            -document.size,
            document.name,
        ),
    )


def is_domestic_earnings(row: dict[str, str]) -> bool:
    if row["form"] != "8-K":
        return False
    return EARNINGS_ITEM in [part.strip() for part in row["items"].split(",")]


def fpi_rejection_reason(
    issuer: Issuer,
    row: dict[str, str],
    exhibits: list[Document],
    cover_text: str,
) -> str | None:
    """None when the 6-K is an earnings report, else why it was rejected.

    Three gates, in this order:
      1. filename exclude - kills TSM's monthly revenue / month-end 6-Ks before
         any content is read. Applied to the FILENAME, never to the text, where
         "revenue" appears in every genuine earnings release.
      2. structural - the filing must carry an EX-99 exhibit.
      3. content - the 6-K cover page and its exhibit descriptions must read
         like earnings.
    """
    if row["form"] != "6-K":
        return "not a 6-K"
    if re.search(issuer.fpi_exclude_match, row["primaryDocument"]):
        return f"primary document {row['primaryDocument']} matches fpi_exclude_match"
    if not exhibits:
        return "6-K carries no EX-99 exhibit"
    if not re.search(issuer.fpi_match, cover_text):
        return "6-K cover page does not match fpi_match"
    return None


def clamp_words(text: str, max_words: int) -> tuple[str, bool]:
    words = text.split()
    if len(words) <= max_words:
        return text, False
    return " ".join(words[:max_words]).rstrip(",;:") + " [...]", True


def extract_quotes(text: str, document: Document, *, limit: int = MAX_QUOTES) -> list[Quote]:
    """Short attributed excerpts from an earnings release.

    Attribution is REQUIRED: a quoted span with no nearby "said <Name>" is
    dropped, which is what keeps boilerplate like the safe-harbour paragraph's
    quoted section titles out of the lane.
    """
    quotes: list[Quote] = []
    # End of the previous span INCLUDING its attribution clause, so a speaker's
    # second paragraph ("...," said Amy Hood, CFO of Microsoft. "We also...")
    # can inherit the attribution without a loose proximity guess.
    previous_span_end = -1
    previous_speaker = ""
    for match in QUOTE_SPAN_RE.finditer(text):
        body = clean_text(match.group(1))
        if len(body.split()) < 8:
            previous_span_end = match.end()
            continue
        after = text[match.end(): match.end() + 200]
        before = text[max(0, match.start() - 200): match.start()]
        speaker = ""
        span_end = match.end()
        after_match = SAID_AFTER_RE.match(after)
        if after_match:
            speaker = clean_text(after_match.group(1))
            span_end = match.end() + after_match.end()
        else:
            before_match = SAID_BEFORE_RE.search(before)
            if before_match:
                speaker = clean_text(before_match.group(1))
            elif previous_speaker and 0 <= match.start() - previous_span_end <= 20:
                speaker = previous_speaker
        previous_span_end = span_end
        if not speaker:
            continue
        previous_speaker = speaker
        clamped, truncated = clamp_words(body.rstrip(" ,;"), MAX_QUOTE_WORDS)
        quotes.append(
            Quote(
                speaker=speaker.rstrip(" .,"),
                text=clamped,
                source_label=document.label,
                source_url=document.url,
                truncated=truncated,
            )
        )
        if len(quotes) >= limit:
            break
    return quotes


def extract_headline_numbers(text: str, *, limit: int = MAX_HEADLINE_ITEMS) -> list[str]:
    """Figures exactly as the issuer printed them - never recomputed.

    Segments come from the release's own bullet markers when present (every
    observed AI-issuer release leads with them), else from sentences.
    """
    body = text.split("SIGNATURES")[0]
    segments = body.split("*") if "*" in body else re.split(r"(?<=[.!?])\s+", body)
    out: list[str] = []
    for segment in segments:
        candidate = clean_text(segment)
        if not 20 <= len(candidate) <= 320:
            continue
        if not HEADLINE_KEY_RE.search(candidate):
            continue
        figures = HEADLINE_FIGURE_RE.findall(candidate)
        if not figures or len(figures) > MAX_FIGURES_PER_HEADLINE:
            continue
        if ACCOUNTING_NEGATIVE_RE.search(candidate):
            continue
        candidate, _ = clamp_words(candidate, MAX_HEADLINE_WORDS)
        if candidate not in out:
            out.append(candidate)
        if len(out) >= limit:
            break
    return out


# ---------------------------------------------------------------------------
# Tier 2: first-party transcripts (link only - never the body)


def _parse_feed_date(value: str) -> dt.date | None:
    value = clean_text(value).split(" ")[0]
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def q4_feed_url(host: str, year: int) -> str:
    params = dict(Q4_EVENT_FEED_PARAMS, year=str(year))
    return f"https://{host}{Q4_EVENT_FEED_PATH}?{urllib.parse.urlencode(params)}"


def discover_transcripts(
    issuer: Issuer, event: EarningsEvent, fetch_fn: FetchBytes
) -> tuple[list[TranscriptLink], str]:
    """Best-effort. Returns (links, provenance note). Never raises.

    A Tier 2 failure must never turn the run red: the IR event feed is an
    undocumented platform API and the lane's value does not depend on it.
    """
    source = issuer.transcript.get("source", "none")
    if source == "none":
        return [], "no first-party transcript source configured for this issuer"
    try:
        if source == "q4-event-feed":
            return _discover_q4(issuer, event, fetch_fn)
        return _discover_template(issuer, event, fetch_fn)
    except FetchError as exc:
        return [], f"transcript lookup failed (non-fatal): {exc}"
    except (ValueError, TypeError, KeyError, AttributeError, IndexError) as exc:
        return [], f"transcript lookup failed (non-fatal): {type(exc).__name__}: {exc}"


def _discover_q4(
    issuer: Issuer, event: EarningsEvent, fetch_fn: FetchBytes
) -> tuple[list[TranscriptLink], str]:
    host = issuer.transcript["host"]
    event_match = issuer.transcript.get("event_match") or DEFAULT_TRANSCRIPT_EVENT_MATCH
    attachment_match = (
        issuer.transcript.get("attachment_match") or DEFAULT_TRANSCRIPT_ATTACHMENT_MATCH
    )
    years = [event.filing_date.year]
    if event.filing_date.month == 1:
        years.append(event.filing_date.year - 1)
    matched_event = ""
    for year in years:
        payload = fetch_json(q4_feed_url(host, year), fetch_fn)
        for row in (payload or {}).get("GetEventListResult") or []:
            if not isinstance(row, dict):
                continue
            title = clean_text(row.get("Title"))
            start = _parse_feed_date(row.get("StartDate", ""))
            if start is None or not re.search(event_match, title):
                continue
            if abs((start - event.filing_date).days) > TRANSCRIPT_EVENT_WINDOW_DAYS:
                continue
            matched_event = title
            links: list[TranscriptLink] = []
            for attachment in row.get("Attachments") or []:
                if not isinstance(attachment, dict):
                    continue
                attachment_title = clean_text(attachment.get("Title"))
                url = clean_text(attachment.get("Url"))
                if not url or not re.search(attachment_match, attachment_title):
                    continue
                links.append(TranscriptLink(attachment_title, url, f"{host} IR event feed"))
                if len(links) >= MAX_TRANSCRIPT_LINKS:
                    break
            if links:
                return links, f"matched IR event '{title}' on {start.isoformat()}"
    if matched_event:
        return [], f"IR event '{matched_event}' found but it publishes no transcript attachment"
    return [], f"no matching earnings event in the {host} IR event feed"


def _discover_template(
    issuer: Issuer, event: EarningsEvent, fetch_fn: FetchBytes
) -> tuple[list[TranscriptLink], str]:
    url = issuer.transcript["url_template"].format(
        fy=f"{event.fiscal_year % 100:02d}",
        fyfull=event.fiscal_year,
        q=event.fiscal_quarter,
        ticker=issuer.ticker,
        ticker_lower=issuer.ticker.lower(),
    )
    # Existence check only. The response body is discarded immediately: this
    # lane links transcripts, it never stores them.
    fetch_fn(url, "*/*")
    return (
        [TranscriptLink("Earnings call transcript", url, "issuer investor relations")],
        f"issuer transcript URL template resolved to {url}",
    )


# ---------------------------------------------------------------------------
# Collection


def collect_events(
    issuers: list[Issuer],
    *,
    target_date: dt.date,
    lookback_days: int,
    fetch_fn: FetchBytes,
) -> tuple[list[EarningsEvent], list[tuple[Issuer, str]]]:
    """(events, submission errors).

    Only the per-issuer submissions fetch feeds the total-failure guard: it is
    the one call every issuer makes. Per-document and per-transcript failures
    degrade the event file (recorded in its Provenance section) instead of
    losing the event.
    """
    events: list[EarningsEvent] = []
    errors: list[tuple[Issuer, str]] = []
    for issuer in issuers:
        try:
            submissions = fetch_json(SEC_SUBMISSIONS_URL.format(cik=issuer.cik), fetch_fn)
        except (FetchError, ValueError, TypeError) as exc:
            errors.append((issuer, str(exc) if isinstance(exc, FetchError)
                           else f"{type(exc).__name__}: {exc}"))
            continue
        sec_fiscal_year_end = clean_text((submissions or {}).get("fiscalYearEnd"))
        for row in recent_rows(submissions):
            if not in_window(row["filingDate"], target_date, lookback_days):
                continue
            document_note = ""
            if issuer.filer_type == "domestic":
                if not is_domestic_earnings(row):
                    continue
                try:
                    documents = fetch_filing_documents(issuer, row["accession"], fetch_fn)
                except FetchError as exc:
                    documents = []
                    document_note = f"filing index unavailable ({exc}); no excerpts extracted"
                exhibits = exhibit_documents(documents)
            else:
                # An FPI 6-K cannot be classified from the submissions index
                # alone, so fetch the filing first and judge second.
                if row["form"] != "6-K":
                    continue
                if re.search(issuer.fpi_exclude_match, row["primaryDocument"]):
                    continue
                try:
                    documents = fetch_filing_documents(issuer, row["accession"], fetch_fn)
                    exhibits = exhibit_documents(documents)
                    cover_text = ""
                    if exhibits:
                        cover_url = f"{filing_base_url(issuer.cik, row['accession'])}/{row['primaryDocument']}"
                        cover_text = normalize_text(fetch_html(cover_url, fetch_fn))
                        cover_text += " " + " ".join(
                            document.description for document in documents
                        )
                except FetchError as exc:
                    # Without the filing we cannot classify it, and a wrong
                    # POSITIVE would publish a fake earnings event. Skipping is
                    # the fail-closed choice; the warning keeps it visible.
                    print(
                        f"WARNING: {issuer.ticker}: skipped 6-K {row['accession']} - "
                        f"could not classify: {exc}",
                        file=sys.stderr,
                    )
                    continue
                if fpi_rejection_reason(issuer, row, exhibits, cover_text) is not None:
                    continue

            try:
                filing_date = dt.date.fromisoformat(row["filingDate"])
            except ValueError:
                continue
            fiscal_year, quarter = fiscal_period(issuer.fiscal_year_end, filing_date)
            event = EarningsEvent(
                issuer=issuer,
                form=row["form"],
                items=row["items"],
                accession=row["accession"],
                filing_date=filing_date,
                report_date=row["reportDate"],
                acceptance=row["acceptance"],
                primary_document=row["primaryDocument"],
                fiscal_year=fiscal_year,
                fiscal_quarter=quarter,
                sec_fiscal_year_end=sec_fiscal_year_end,
            )
            if document_note:
                event.notes.append(document_note)
            if not exhibits and not document_note:
                event.notes.append("filing carries no EX-99 exhibit; metadata only")
            enrich_event(event, exhibits, fetch_fn=fetch_fn)
            events.append(event)
    return dedupe_events(events), errors


def dedupe_events(events: list[EarningsEvent]) -> list[EarningsEvent]:
    """One event per (issuer, fiscal period); earliest accepted filing wins.

    ARM files its earnings 6-K and its interim-financials 6-K three minutes
    apart. The EX-99 gate already rejects the second one, but a per-period key
    means a future twin-filing shape cannot produce two artifacts for one
    quarter either.
    """
    by_key: dict[tuple[str, str], EarningsEvent] = {}
    for event in events:
        key = (event.issuer.id, event.period)
        previous = by_key.get(key)
        if previous is None or event.acceptance < previous.acceptance:
            by_key[key] = event
    return sorted(
        by_key.values(),
        key=lambda event: (event.filing_date.isoformat(), event.issuer.ticker),
    )


def enrich_event(
    event: EarningsEvent, exhibits: list[Document], *, fetch_fn: FetchBytes
) -> None:
    """Attach documents, headline figures, quotes and transcript links."""
    event.documents = exhibits[:MAX_EXHIBITS_PER_FILING]
    for document in event.documents:
        if event.headline and len(event.quotes) >= MAX_QUOTES:
            break
        if document.size > MAX_DOCUMENT_BYTES:
            event.notes.append(
                f"skipped oversized exhibit {document.name} ({document.size} bytes)"
            )
            continue
        try:
            text = normalize_text(fetch_html(document.url, fetch_fn))
        except FetchError as exc:
            event.notes.append(f"exhibit {document.name} unavailable (non-fatal): {exc}")
            continue
        if not event.headline:
            event.headline = extract_headline_numbers(text)
        if len(event.quotes) < MAX_QUOTES:
            event.quotes.extend(
                extract_quotes(text, document, limit=MAX_QUOTES - len(event.quotes))
            )
    event.headline = event.headline[:MAX_HEADLINE_ITEMS]
    event.quotes = event.quotes[:MAX_QUOTES]
    links, note = discover_transcripts(event.issuer, event, fetch_fn)
    event.transcripts = links[:MAX_TRANSCRIPT_LINKS]
    event.notes.append(f"Tier 2 (first-party transcript): {note}")


# ---------------------------------------------------------------------------
# Render


def source_urls(event: EarningsEvent) -> list[str]:
    urls = [
        SEC_SUBMISSIONS_URL.format(cik=event.issuer.cik),
        f"{event.filing_base_url}/",
        f"{event.filing_base_url}/{event.primary_document}",
    ]
    urls.extend(document.url for document in event.documents)
    urls.extend(link.url for link in event.transcripts)
    seen: set[str] = set()
    out: list[str] = []
    for url in urls:
        if url and url not in seen:
            seen.add(url)
            out.append(url)
    return out


def render_event(event: EarningsEvent) -> str:
    """Deterministic per-event Markdown.

    Deliberately carries NO generation timestamp: with a multi-day lookback the
    same filing is re-rendered on several consecutive runs, and a timestamp
    would make every one of those a git diff. Byte-identical re-renders let the
    workflow's `git commit || echo "No changes"` absorb them, so no state file
    is needed.
    """
    issuer = event.issuer
    lines = [
        f"# {issuer.name} ({issuer.ticker}) {event.period} Earnings - "
        f"{event.filing_date.isoformat()}",
        "",
        "## Event",
        f"- Issuer: {issuer.name} ({issuer.ticker}), CIK {issuer.cik}, {issuer.filer_type} filer",
        f"- Form: {event.form}" + (f" (items {event.items})" if event.items else ""),
        f"- Accession: {event.accession}",
        f"- Fiscal period: {event.period} (fiscal year ends {issuer.fiscal_year_end})",
        f"- Filed: {event.filing_date.isoformat()}"
        + (f"; SEC report date {event.report_date}" if event.report_date else ""),
        f"- Accepted: {event.acceptance or 'unknown'}",
        f"- Filing index: {event.filing_base_url}/",
        f"- Priority: {issuer.priority}; tags: {', '.join(issuer.tags) or 'none'}; "
        f"digest candidate: {'yes' if issuer.include_in_digest else 'no'}",
        "",
    ]

    if event.headline:
        lines.extend(["## Headline Numbers", ""])
        lines.extend(f"- {item}" for item in event.headline)
        lines.extend([
            "",
            "_Figures as printed in the issuer's own release; ARA does not recompute "
            "or adjust them._",
            "",
        ])

    if event.quotes:
        lines.extend(["## Key Quotes", ""])
        for quote in event.quotes:
            lines.append(
                f'- **{quote.speaker}**: "{quote.text}" '
                f"([{quote.source_label}]({quote.source_url}))"
            )
        lines.append("")

    lines.extend(["## Transcript", ""])
    lines.append(f"- First-party transcript: {'yes' if event.transcripts else 'no'}")
    for link in event.transcripts:
        lines.append(f"- [{link.title}]({link.url}) - published by the issuer via {link.provider}")
    if not event.transcripts:
        lines.append(
            "- No first-party call transcript was available for this event at fetch time; "
            "the filing exhibits above are the primary record."
        )
    lines.extend([
        "- ARA links first-party transcripts and never stores or reproduces their text.",
        "",
        "## Documents",
        "",
    ])
    if event.documents:
        for document in event.documents:
            lines.append(f"- [{document.label}]({document.url}) ({document.size} bytes)")
    else:
        lines.append("- No EX-99 exhibit documents were available for this filing.")
    lines.extend(["", "## Sources", ""])
    lines.extend(f"- {url}" for url in source_urls(event))

    lines.extend(["", "## Provenance", ""])
    lines.append(
        f"- Tier 1 (SEC EDGAR): {event.form} {event.accession}, accepted "
        f"{event.acceptance or 'unknown'}."
    )
    lines.append(
        f"- Excerpt policy: at most {MAX_QUOTES} attributed quotes of <= {MAX_QUOTE_WORDS} "
        f"words and {MAX_HEADLINE_ITEMS} headline figures of <= {MAX_HEADLINE_WORDS} words, "
        "all from documents the issuer disseminated publicly under Reg FD."
    )
    if not event.headline:
        lines.append(
            "- Headline Numbers omitted: no figure matched the deterministic patterns "
            "(the section is dropped rather than guessed)."
        )
    if not event.quotes:
        lines.append(
            "- Key Quotes omitted: no attributed excerpt was found in the filing exhibits."
        )
    if (
        event.sec_fiscal_year_end
        and event.sec_fiscal_year_end != issuer.fiscal_year_end.replace("-", "")
    ):
        lines.append(
            f"- Fiscal-year-end divergence: registry says {issuer.fiscal_year_end}, SEC "
            f"submissions metadata says {event.sec_fiscal_year_end}; the registry value was "
            "used (see its notes)."
        )
    lines.extend(f"- {note}" for note in event.notes)
    lines.extend(["", "---", "*Generated by `scripts/fetch_earnings_signal.py`.*", ""])
    return ascii_safe("\n".join(lines)) + "\n"


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False,
        prefix=f".{path.name}.", suffix=".tmp",
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


# ---------------------------------------------------------------------------
# Index


def _marker(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return ""


def build_index(out_dir: Path) -> dict[str, Any]:
    """Full rebuild from the directory contents - never read-modify-write.

    An append/merge index is the exact shape that leaves safe-push PRs stuck on
    a same-file conflict (CLAUDE.md rule 13a). Carries no timestamp, so a quiet
    run produces a byte-identical file and therefore no commit.
    """
    events: list[dict[str, Any]] = []
    for path in sorted(out_dir.glob("*.md")):
        match = EVENT_FILENAME_RE.match(path.name)
        if not match:
            continue
        text = path.read_text(encoding="utf-8")
        title = text.splitlines()[0] if text else ""
        title_match = re.match(r"^#\s+(.*?)\s+\([A-Z0-9.\-]+\)\s", title)
        events.append({
            "file": path.name,
            "date": match.group(1),
            "ticker": match.group(2),
            "period": match.group(3),
            "issuer": title_match.group(1) if title_match else "",
            "form": _marker(text, "- Form:").split(" (")[0],
            "accession": _marker(text, "- Accession:"),
            "transcript": _marker(text, "- First-party transcript:") == "yes",
        })
    events.sort(key=lambda row: (row["date"], row["ticker"]), reverse=True)
    return {"lane": "earnings", "schema": 1, "count": len(events), "events": events}


def write_index(out_dir: Path) -> Path:
    path = out_dir / "index.json"
    write_atomic(path, json.dumps(build_index(out_dir), indent=2) + "\n")
    return path


# ---------------------------------------------------------------------------
# CLI


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    parser.add_argument("--lookback-days", type=int, default=5)
    parser.add_argument(
        "--contact",
        default=os.environ.get("SEC_CONTACT_EMAIL", DEFAULT_CONTACT),
        help="contact address sent in the SEC-mandated User-Agent",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        target_date = dt.date.fromisoformat(args.date)
    except ValueError:
        print(f"ERROR: invalid --date {args.date!r}; expected YYYY-MM-DD", file=sys.stderr)
        return 2
    if not 0 <= args.lookback_days <= 90:
        print("ERROR: --lookback-days must be between 0 and 90", file=sys.stderr)
        return 2
    if "@" not in args.contact:
        print(
            "ERROR: --contact must be an e-mail address; SEC answers HTTP 403 to a "
            "User-Agent without one",
            file=sys.stderr,
        )
        return 2

    try:
        issuers = load_issuers(args.registry)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: invalid registry {args.registry}: {exc}", file=sys.stderr)
        return 2

    def fetch_fn(url: str, accept: str) -> bytes:
        return http_get(url, accept, contact=args.contact)

    events, errors = collect_events(
        issuers,
        target_date=target_date,
        lookback_days=args.lookback_days,
        fetch_fn=fetch_fn,
    )

    # Fail closed on a TOTAL outage only. Unlike the youtube lane, an empty
    # result is the NORMAL state here (~40 reporting days a year), so silence
    # is only suspicious when every tracked issuer failed to answer.
    if issuers and not events and len(errors) == len(issuers):
        print(
            f"ERROR: total SEC fetch failure: all {len(issuers)} tracked issuer(s) failed "
            f"against {SEC_SUBMISSIONS_URL.format(cik='<cik>')} and 0 earnings events were "
            "collected; refusing to write anything so the outage stays loud",
            file=sys.stderr,
        )
        for issuer, error in errors:
            print(f"ERROR:   {issuer.ticker}: {error}", file=sys.stderr)
        return EXIT_TOTAL_FETCH_FAILURE

    for issuer, error in errors:
        print(f"WARNING: {issuer.ticker} ({issuer.cik}): {error}", file=sys.stderr)

    if not events:
        window_start = target_date - dt.timedelta(days=args.lookback_days)
        print(
            f"No earnings events in window {window_start}..{target_date} across "
            f"{len(issuers)} tracked issuer(s); wrote nothing"
        )
        if args.out_dir.is_dir():
            write_index(args.out_dir)
        return 0

    for event in events:
        write_atomic(args.out_dir / event.filename, render_event(event))
    index_path = write_index(args.out_dir)
    print(
        f"Wrote {len(events)} earnings event file(s) to {args.out_dir} "
        f"({len(errors)} issuer fetch error(s)); rebuilt {index_path}: "
        + ", ".join(event.filename for event in events)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
