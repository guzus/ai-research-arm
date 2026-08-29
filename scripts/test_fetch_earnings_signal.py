#!/usr/bin/env python3
"""Tests for the SEC-EDGAR-backed earnings signal lane.

Every test injects a fake fetch function - the suite makes no network calls.
The fixtures are trimmed copies of the real filings named in each docstring,
so a regression here corresponds to a real observed shape.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import fetch_earnings_signal as earnings  # noqa: E402


REGISTRY_PATH = Path(__file__).resolve().parents[1] / "data" / "sources" / "earnings_issuers.json"


def make_issuer(**overrides) -> earnings.Issuer:
    base = dict(
        id="nvda",
        ticker="NVDA",
        name="NVIDIA Corporation",
        cik="0001045810",
        filer_type="domestic",
        fiscal_year_end="01-31",
        priority="P0",
        tags=("ai-compute",),
        include_in_digest=True,
        transcript={"source": "none"},
        fpi_match=earnings.DEFAULT_FPI_MATCH,
        fpi_exclude_match=earnings.DEFAULT_FPI_EXCLUDE,
        notes="",
    )
    base.update(overrides)
    return earnings.Issuer(**base)  # type: ignore[arg-type]


def submissions(rows: list[dict[str, str]], fiscal_year_end: str = "0131") -> dict:
    keys = ("form", "items", "accessionNumber", "filingDate", "reportDate",
            "acceptanceDateTime", "primaryDocument")
    return {
        "name": "TEST CO",
        "fiscalYearEnd": fiscal_year_end,
        "filings": {"recent": {key: [row.get(key, "") for row in rows] for key in keys}},
    }


def index_page(rows: list[tuple[str, str, str, int]]) -> str:
    """An EDGAR filing index page: (description, document, type, size) rows."""
    body = ["<table><tr><th>Seq</th><th>Description</th><th>Document</th>"
            "<th>Type</th><th>Size</th></tr>"]
    for seq, (description, document, doc_type, size) in enumerate(rows, start=1):
        body.append(
            f"<tr><td>{seq}</td><td>{description}</td>"
            f"<td><a href='/x/{document}'>{document}</a>&nbsp;&nbsp; iXBRL</td>"
            f"<td>{doc_type}</td><td>{size}</td></tr>"
        )
    body.append("</table>")
    return "".join(body)


# Trimmed from the real EX-99.1 of NVDA 0001045810-26-000051.
NVDA_RELEASE = (
    "<p>EX-99.1 2 q1fy27pr.htm EX-99.1 Document NVIDIA Announces Financial Results for "
    "First Quarter Fiscal 2027 &bull; Record revenue of $81.6 billion, up 85% from a year "
    "ago &bull; Record Data Center revenue of $75.2 billion, up 92% from a year ago "
    "&bull; NVIDIA today reported record revenue. “The buildout of AI factories — "
    "the largest infrastructure expansion in human history — is accelerating at "
    "extraordinary speed,” said Jensen Huang, founder and CEO of NVIDIA. “Agentic "
    "AI has arrived, doing productive work and scaling rapidly across companies and "
    "industries.”</p>"
)

# The ARM earnings 6-K cover page (0001973239-26-000113) - note the exhibit index.
ARM_COVER = (
    "<p>Form 6-K REPORT OF FOREIGN PRIVATE ISSUER Arm Holdings plc EXHIBIT INDEX "
    "Exhibit Number Description 99.1 Earnings Press Release dated July 29, 2026 "
    "99.2 Shareholder Letter dated July 29, 2026 SIGNATURES</p>"
)
# The TSMC earnings 6-K cover page (0001046179-26-000451).
TSM_COVER = (
    "<p>FORM 6-K Taiwan Semiconductor Manufacturing Company Limited Exhibits Exhibit "
    "Number Exhibit Description 99.1 Press release issued by TSMC on July 16, 2026. "
    "99.2 2026 Second Quarter Earnings Conference Presentation Material.</p>"
)


class FiscalPeriodTest(unittest.TestCase):
    """The 8-K reportDate is the ANNOUNCEMENT date, so the period is derived.

    Every pair below was checked against the issuer's own label for that
    filing; a wrong label is the most visible possible output bug because it
    is in the filename.
    """

    CASES = (
        ("01-31", dt.date(2026, 5, 20), 2027, 1),   # NVDA FY27Q1
        ("06-30", dt.date(2026, 7, 29), 2026, 4),   # MSFT FY26Q4
        ("12-31", dt.date(2026, 7, 29), 2026, 2),   # META FY26Q2
        ("03-31", dt.date(2026, 7, 29), 2027, 1),   # ARM  FY27Q1
        ("12-31", dt.date(2026, 7, 16), 2026, 2),   # TSM  FY26Q2
        ("01-30", dt.date(2026, 5, 28), 2027, 1),   # DELL FY27Q1
        ("12-26", dt.date(2026, 5, 5), 2026, 1),    # AMD  FY26Q1
        ("05-31", dt.date(2026, 9, 9), 2027, 1),    # ORCL FY27Q1
    )

    def test_period_matches_issuer_labels(self):
        for fiscal_year_end, filing_date, year, quarter in self.CASES:
            with self.subTest(fye=fiscal_year_end, filed=filing_date):
                self.assertEqual(
                    earnings.fiscal_period(fiscal_year_end, filing_date), (year, quarter)
                )

    def test_period_label_is_two_digit(self):
        self.assertEqual(earnings.period_label(2027, 1), "FY27Q1")
        self.assertEqual(earnings.period_label(2026, 4), "FY26Q4")

    def test_month_shift_clamps_to_month_end(self):
        self.assertEqual(earnings.shift_months(dt.date(2026, 5, 31), -3), dt.date(2026, 2, 28))
        self.assertEqual(earnings.shift_months(dt.date(2026, 1, 31), -9), dt.date(2025, 4, 30))


class RegistryTest(unittest.TestCase):
    def test_committed_registry_loads_and_is_consistent(self):
        issuers = earnings.load_issuers(REGISTRY_PATH)
        self.assertGreaterEqual(len(issuers), 14)
        self.assertEqual(len({issuer.cik for issuer in issuers}), len(issuers))
        for issuer in issuers:
            with self.subTest(issuer=issuer.id):
                self.assertRegex(issuer.cik, r"^\d{10}$")
                self.assertIn(issuer.filer_type, earnings.FILER_TYPES)
                self.assertIn(
                    issuer.transcript.get("source", "none"), earnings.TRANSCRIPT_SOURCES
                )

    def _load(self, rows):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "registry.json"
            path.write_text(json.dumps(rows), encoding="utf-8")
            return earnings.load_issuers(path)

    def _row(self, **overrides):
        row = {
            "id": "nvda", "ticker": "NVDA", "name": "NVIDIA", "cik": "0001045810",
            "filer_type": "domestic", "fiscal_year_end": "01-31", "priority": "P0",
            "tags": ["ai-compute"], "include_in_digest": True,
            "transcript": {"source": "none"},
        }
        row.update(overrides)
        return row

    def test_integer_cik_is_rejected(self):
        # An int CIK silently drops MSFT's leading zeros and 404s the API.
        with self.assertRaisesRegex(ValueError, "10-digit zero-padded string"):
            self._load([self._row(cik="1045810")])

    def test_duplicate_id_and_cik_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate issuer id"):
            self._load([self._row(), self._row(ticker="NVDA2", cik="0000789019")])
        with self.assertRaisesRegex(ValueError, "duplicate issuer cik"):
            self._load([self._row(), self._row(id="other", ticker="OTHR")])

    def test_transcript_source_requires_its_own_field(self):
        with self.assertRaisesRegex(ValueError, "requires host"):
            self._load([self._row(transcript={"source": "q4-event-feed"})])
        with self.assertRaisesRegex(ValueError, "requires url_template"):
            self._load([self._row(transcript={"source": "url-template"})])
        with self.assertRaisesRegex(ValueError, "invalid transcript.source"):
            self._load([self._row(transcript={"source": "seeking-alpha"})])

    def test_bad_fiscal_year_end_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "fiscal_year_end must be MM-DD"):
            self._load([self._row(fiscal_year_end="0131")])

    def test_invalid_regex_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid regex"):
            self._load([self._row(filer_type="fpi", fpi_exclude_match="(unclosed")])


class DocumentSelectionTest(unittest.TestCase):
    def test_exhibit_types_come_from_the_index_table(self):
        """NVDA 0001045810-26-000051: EX-99.1 press release + EX-99.2 commentary."""
        documents = earnings.parse_filing_documents(
            index_page([
                ("8-K", "nvda-20260520.htm", "8-K", 26803),
                ("EX-99.1", "q1fy27pr.htm", "EX-99.1", 274829),
                ("EX-99.2", "q1fy27cfocommentary.htm", "EX-99.2", 165436),
                ("NVDA LOGO", "nvdalogoa19a.jpg", "GRAPHIC", 13441),
                ("XBRL SCHEMA", "nvda-20260520.xsd", "EX-101.SCH", 2125),
            ]),
            "https://example.invalid/filing",
        )
        exhibits = earnings.exhibit_documents(documents)

        # EX-99.1 first even though EX-99.2 could win on any name heuristic.
        self.assertEqual([d.name for d in exhibits], ["q1fy27pr.htm", "q1fy27cfocommentary.htm"])
        self.assertEqual(exhibits[0].url, "https://example.invalid/filing/q1fy27pr.htm")
        self.assertEqual(exhibits[0].size, 274829)

    def test_xbrl_only_filing_has_no_exhibits(self):
        """ARM 0001973239-26-000114 - the interim financials filed 3 min later."""
        documents = earnings.parse_filing_documents(
            index_page([
                ("6-K", "arm-20260630.htm", "6-K", 1050860),
                ("XBRL SCHEMA", "arm-20260630.xsd", "EX-101.SCH", 52961),
                ("XBRL INSTANCE", "arm-20260630_htm.xml", "XML", 1024281),
            ]),
            "https://example.invalid/filing",
        )
        self.assertEqual(earnings.exhibit_documents(documents), [])


class ExtractionTest(unittest.TestCase):
    DOCUMENT = earnings.Document("EX-99.1", "EX-99.1", "pr.htm", "https://example.invalid/pr.htm", 100)

    def test_headline_numbers_come_from_the_issuers_own_bullets(self):
        text = earnings.normalize_text(NVDA_RELEASE)
        numbers = earnings.extract_headline_numbers(text)

        self.assertIn("Record revenue of $81.6 billion, up 85% from a year ago", numbers)
        self.assertLessEqual(len(numbers), earnings.MAX_HEADLINE_ITEMS)
        # The EDGAR document preamble must not leak into the artifact.
        self.assertFalse(any("q1fy27pr.htm" in item for item in numbers))

    def test_flattened_financial_table_is_not_a_headline_number(self):
        """MSFT's EX-99.1 renders its reconciliation table into one long line."""
        table = (
            "Non-GAAP Constant Currency Net Income $35,766 $(480) $35,286 $27,233 $1,575 "
            "$28,808 31% 31% $(2,055) 22% 22% Diluted Earnings per Share $4.81 $(0.07) "
            "$4.74 $3.65 $0.21 $3.86 32% 32%"
        )
        self.assertEqual(earnings.extract_headline_numbers(table), [])

    def test_headline_words_are_capped(self):
        long_bullet = "Revenue was $1.0 billion " + " ".join(["up"] * 60) + " 10%."
        [item] = earnings.extract_headline_numbers(long_bullet)

        self.assertGreater(len(long_bullet.split()), earnings.MAX_HEADLINE_WORDS)
        self.assertLessEqual(len(item.split()), earnings.MAX_HEADLINE_WORDS + 1)
        self.assertTrue(item.endswith("[...]"))

    def test_quotes_are_attributed(self):
        text = earnings.normalize_text(NVDA_RELEASE)
        quotes = earnings.extract_quotes(text, self.DOCUMENT)

        self.assertEqual(len(quotes), 2)
        self.assertEqual(quotes[0].speaker, "Jensen Huang, founder and CEO of NVIDIA")
        self.assertIn("buildout of AI factories", quotes[0].text)
        # The second paragraph inherits the speaker from the same attribution.
        self.assertEqual(quotes[1].speaker, quotes[0].speaker)
        self.assertEqual(quotes[0].source_url, self.DOCUMENT.url)

    def test_unattributed_quotes_are_dropped(self):
        """The safe-harbour paragraph quotes SEC section titles, not people."""
        text = earnings.normalize_text(
            "<p>please refer to the “Management's Discussion and Analysis of Financial "
            "Condition and Results of Operations” and “Risk Factors” sections "
            "of the annual report.</p>"
        )
        self.assertEqual(earnings.extract_quotes(text, self.DOCUMENT), [])

    def test_quote_word_cap_is_enforced_in_code(self):
        """The 60-word cap IS the licensing position - it must not be advisory."""
        body = " ".join(["word"] * 150)
        text = f'"{body}," said Jane Doe, chief executive officer of Example.'
        [quote] = earnings.extract_quotes(text, self.DOCUMENT)

        self.assertTrue(quote.truncated)
        self.assertTrue(quote.text.endswith("[...]"))
        # The cap is on the ISSUER's words; "[...]" is our elision marker.
        issuer_words = quote.text.removesuffix(" [...]").split()
        self.assertEqual(len(issuer_words), earnings.MAX_QUOTE_WORDS)

    def test_quote_count_cap_is_enforced_in_code(self):
        one = '"this is a long enough quoted sentence to pass the filter," said Jane Doe. '
        quotes = earnings.extract_quotes(one * 20, self.DOCUMENT)

        self.assertEqual(len(quotes), earnings.MAX_QUOTES)


class FpiClassificationTest(unittest.TestCase):
    """FPI 6-Ks have an EMPTY items field, so detection is structural."""

    ARM = make_issuer(
        id="arm", ticker="ARM", name="Arm Holdings plc", cik="0001973239",
        filer_type="fpi", fiscal_year_end="03-31",
    )
    TSM = make_issuer(
        id="tsm", ticker="TSM", name="TSMC", cik="0001046179",
        filer_type="fpi", fiscal_year_end="12-31",
    )
    EXHIBIT = [earnings.Document("EX-99.1", "EX-99.1", "ex991.htm", "https://x/ex991.htm", 5051)]

    def test_arm_earnings_6k_is_accepted(self):
        row = {"form": "6-K", "primaryDocument": "arm-20260729.htm"}
        self.assertIsNone(
            earnings.fpi_rejection_reason(
                self.ARM, row, self.EXHIBIT, earnings.normalize_text(ARM_COVER)
            )
        )

    def test_tsm_earnings_6k_is_accepted(self):
        row = {"form": "6-K", "primaryDocument": "tsm-20260716x6k.htm"}
        self.assertIsNone(
            earnings.fpi_rejection_reason(
                self.TSM, row, self.EXHIBIT, earnings.normalize_text(TSM_COVER)
            )
        )

    def test_tsm_monthly_revenue_6ks_are_rejected_by_filename(self):
        """These are REAL filings; a loose rule publishes fake quarterly results."""
        for document in (
            "tsm-revenue20260713.htm",
            "tsm-revenue20260610.htm",
            "tsm-monthend6kx20260724.htm",
            "tsm-monthend6kx20260625.htm",
        ):
            with self.subTest(document=document):
                reason = earnings.fpi_rejection_reason(
                    self.TSM,
                    {"form": "6-K", "primaryDocument": document},
                    self.EXHIBIT,
                    earnings.normalize_text(TSM_COVER),
                )
                self.assertIsNotNone(reason)
                self.assertIn("fpi_exclude_match", reason or "")

    def test_6k_without_exhibits_is_rejected(self):
        reason = earnings.fpi_rejection_reason(
            self.ARM, {"form": "6-K", "primaryDocument": "arm-20260630.htm"}, [], ARM_COVER
        )
        self.assertEqual(reason, "6-K carries no EX-99 exhibit")

    def test_non_earnings_6k_with_exhibits_is_rejected_on_content(self):
        cover = earnings.normalize_text(
            "<p>Form 6-K EXHIBIT INDEX 99.1 Press release announcing the appointment of a "
            "new director.</p>"
        )
        reason = earnings.fpi_rejection_reason(
            self.ARM, {"form": "6-K", "primaryDocument": "arm-20260506.htm"},
            self.EXHIBIT, cover,
        )
        self.assertEqual(reason, "6-K cover page does not match fpi_match")

    def test_domestic_detection_requires_item_202(self):
        self.assertTrue(earnings.is_domestic_earnings({"form": "8-K", "items": "2.02,9.01"}))
        self.assertTrue(earnings.is_domestic_earnings({"form": "8-K", "items": "2.02,7.01,9.01"}))
        self.assertFalse(earnings.is_domestic_earnings({"form": "8-K", "items": "5.02,9.01"}))
        self.assertFalse(earnings.is_domestic_earnings({"form": "6-K", "items": ""}))


class CollectionTest(unittest.TestCase):
    NVDA = make_issuer()

    def build_fetch(self, mapping, missing_ok=True):
        seen: list[str] = []

        def fetch(url: str, _accept: str) -> bytes:
            seen.append(url)
            for fragment, payload in mapping.items():
                if fragment in url:
                    if isinstance(payload, Exception):
                        raise payload
                    if isinstance(payload, (dict, list)):
                        return json.dumps(payload).encode()
                    return payload.encode()
            if missing_ok:
                raise earnings.FetchError(f"HTTP 404 for {url}")
            raise AssertionError(f"unexpected fetch: {url}")

        return fetch, seen

    def test_domestic_event_is_collected_without_a_transcript(self):
        fetch, _ = self.build_fetch({
            "submissions/CIK0001045810": submissions([{
                "form": "8-K", "items": "2.02,9.01",
                "accessionNumber": "0001045810-26-000051",
                "filingDate": "2026-05-20", "reportDate": "2026-05-20",
                "acceptanceDateTime": "2026-05-20T20:21:19.000Z",
                "primaryDocument": "nvda-20260520.htm",
            }]),
            "-index.html": index_page([
                ("8-K", "nvda-20260520.htm", "8-K", 26803),
                ("EX-99.1", "q1fy27pr.htm", "EX-99.1", 274829),
            ]),
            "q1fy27pr.htm": NVDA_RELEASE,
        })

        events, errors = earnings.collect_events(
            [self.NVDA], target_date=dt.date(2026, 5, 20), lookback_days=1, fetch_fn=fetch
        )

        self.assertEqual(errors, [])
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event.period, "FY27Q1")
        self.assertEqual(event.filename, "2026-05-20-NVDA-FY27Q1.md")
        self.assertEqual(event.transcripts, [])
        self.assertTrue(event.quotes, "Tier 1 must still yield quotes with no Tier 2")

    def test_transcript_failure_is_non_fatal(self):
        issuer = make_issuer(transcript={"source": "q4-event-feed", "host": "ir.example"})
        fetch, _ = self.build_fetch({
            "submissions/CIK0001045810": submissions([{
                "form": "8-K", "items": "2.02,9.01",
                "accessionNumber": "0001045810-26-000051",
                "filingDate": "2026-05-20", "acceptanceDateTime": "2026-05-20T20:21:19.000Z",
                "primaryDocument": "nvda-20260520.htm",
            }]),
            "-index.html": index_page([
                ("8-K", "nvda-20260520.htm", "8-K", 26803),
                ("EX-99.1", "q1fy27pr.htm", "EX-99.1", 274829),
            ]),
            "q1fy27pr.htm": NVDA_RELEASE,
            "Event.svc": earnings.FetchError("HTTP 500 for the IR feed"),
        })

        events, _ = earnings.collect_events(
            [issuer], target_date=dt.date(2026, 5, 20), lookback_days=1, fetch_fn=fetch
        )

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].transcripts, [])
        self.assertTrue(
            any("transcript lookup failed (non-fatal)" in note for note in events[0].notes)
        )

    def test_q4_feed_transcript_is_linked(self):
        issuer = make_issuer(transcript={"source": "q4-event-feed", "host": "ir.example"})
        fetch, _ = self.build_fetch({
            "submissions/CIK0001045810": submissions([{
                "form": "8-K", "items": "2.02,9.01",
                "accessionNumber": "0001045810-26-000051",
                "filingDate": "2026-05-20", "acceptanceDateTime": "2026-05-20T20:21:19.000Z",
                "primaryDocument": "nvda-20260520.htm",
            }]),
            "-index.html": index_page([("8-K", "nvda-20260520.htm", "8-K", 26803)]),
            "Event.svc": {"GetEventListResult": [
                {"Title": "Investor Day", "StartDate": "05/20/2026 13:30:00",
                 "Attachments": [{"Title": "Transcript", "Extension": "PDF",
                                  "Url": "https://cdn.example/investor-day.pdf"}]},
                {"Title": "Q1 2027 Earnings Call", "StartDate": "05/20/2026 21:00:00",
                 "Attachments": [
                     {"Title": "Press Release", "Extension": "PDF",
                      "Url": "https://cdn.example/pr.pdf"},
                     {"Title": "Earnings Call Transcript", "Extension": "PDF",
                      "Url": "https://cdn.example/transcript.pdf"},
                 ]},
            ]},
        })

        events, _ = earnings.collect_events(
            [issuer], target_date=dt.date(2026, 5, 20), lookback_days=1, fetch_fn=fetch
        )

        # Only the EARNINGS event's transcript, and only the transcript
        # attachment - not the press release, not the investor-day PDF.
        self.assertEqual(
            [link.url for link in events[0].transcripts], ["https://cdn.example/transcript.pdf"]
        )

    def test_twin_fpi_filings_produce_one_event(self):
        """ARM files its earnings 6-K and interim financials 3 minutes apart."""
        issuer = make_issuer(
            id="arm", ticker="ARM", name="Arm Holdings plc", cik="0001973239",
            filer_type="fpi", fiscal_year_end="03-31",
        )
        fetch, _ = self.build_fetch({
            "submissions/CIK0001973239": submissions([
                {"form": "6-K", "items": "", "accessionNumber": "0001973239-26-000114",
                 "filingDate": "2026-07-29", "acceptanceDateTime": "2026-07-29T16:05:46.000Z",
                 "primaryDocument": "arm-20260630.htm"},
                {"form": "6-K", "items": "", "accessionNumber": "0001973239-26-000113",
                 "filingDate": "2026-07-29", "acceptanceDateTime": "2026-07-29T16:02:28.000Z",
                 "primaryDocument": "arm-20260729.htm"},
            ], fiscal_year_end="0331"),
            "000197323926000114/0001973239-26-000114-index.html": index_page([
                ("6-K", "arm-20260630.htm", "6-K", 1050860),
                ("XBRL INSTANCE", "arm-20260630_htm.xml", "XML", 1024281),
            ]),
            "000197323926000113/0001973239-26-000113-index.html": index_page([
                ("6-K", "arm-20260729.htm", "6-K", 13805),
                ("EX-99.1", "exhibit991.htm", "EX-99.1", 5051),
                ("EX-99.2", "exhibit992.htm", "EX-99.2", 358410),
            ]),
            "arm-20260729.htm": ARM_COVER,
            "exhibit991.htm": "<p>Arm Holdings plc Reports Results.</p>",
            "exhibit992.htm": "<p>Total revenue increased 22% year-over-year to $1,289 million.</p>",
        })

        events, _ = earnings.collect_events(
            [issuer], target_date=dt.date(2026, 7, 29), lookback_days=1, fetch_fn=fetch
        )

        self.assertEqual([event.accession for event in events], ["0001973239-26-000113"])
        self.assertEqual(events[0].period, "FY27Q1")

    def test_unclassifiable_6k_is_skipped_not_published(self):
        issuer = make_issuer(
            id="tsm", ticker="TSM", name="TSMC", cik="0001046179",
            filer_type="fpi", fiscal_year_end="12-31",
        )
        fetch, _ = self.build_fetch({
            "submissions/CIK0001046179": submissions([{
                "form": "6-K", "items": "", "accessionNumber": "0001046179-26-000451",
                "filingDate": "2026-07-16", "acceptanceDateTime": "2026-07-16T11:45:43.000Z",
                "primaryDocument": "tsm-20260716x6k.htm",
            }], fiscal_year_end="1231"),
            "-index.html": earnings.FetchError("HTTP 503 for the filing index"),
        })

        stderr = StringIO()
        with redirect_stderr(stderr):
            events, errors = earnings.collect_events(
                [issuer], target_date=dt.date(2026, 7, 16), lookback_days=1, fetch_fn=fetch
            )

        self.assertEqual(events, [])
        self.assertEqual(errors, [])  # not a submissions failure
        self.assertIn("could not classify", stderr.getvalue())


class RenderTest(unittest.TestCase):
    def build_event(self, **overrides) -> earnings.EarningsEvent:
        event = earnings.EarningsEvent(
            issuer=make_issuer(),
            form="8-K",
            items="2.02,9.01",
            accession="0001045810-26-000051",
            filing_date=dt.date(2026, 5, 20),
            report_date="2026-05-20",
            acceptance="2026-05-20T20:21:19.000Z",
            primary_document="nvda-20260520.htm",
            fiscal_year=2027,
            fiscal_quarter=1,
        )
        for key, value in overrides.items():
            setattr(event, key, value)
        return event

    def test_missing_sections_are_declared_not_faked(self):
        text = earnings.render_event(self.build_event())

        self.assertIn("# NVIDIA Corporation (NVDA) FY27Q1 Earnings - 2026-05-20", text)
        self.assertNotIn("## Headline Numbers", text)
        self.assertNotIn("## Key Quotes", text)
        self.assertIn("- First-party transcript: no", text)
        self.assertIn("Headline Numbers omitted:", text)
        self.assertIn("Key Quotes omitted:", text)

    def test_render_carries_no_timestamp_so_reruns_are_no_ops(self):
        first = earnings.render_event(self.build_event())
        second = earnings.render_event(self.build_event())

        self.assertEqual(first, second)
        self.assertNotIn("Generated:", first)
        self.assertNotIn("UTC", first)

    def test_transcript_is_linked_never_reproduced(self):
        link = earnings.TranscriptLink(
            "Earnings Call Transcript", "https://cdn.example/t.pdf", "ir.example IR event feed"
        )
        text = earnings.render_event(self.build_event(transcripts=[link]))

        self.assertIn("- First-party transcript: yes", text)
        self.assertIn("https://cdn.example/t.pdf", text)
        self.assertIn("never stores or reproduces their text", text)


class MainTest(unittest.TestCase):
    def run_main(self, args, out_dir):
        stdout, stderr = StringIO(), StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = earnings.main(args)
        return code, stdout.getvalue(), stderr.getvalue()

    def registry_file(self, td, rows=None):
        path = Path(td) / "registry.json"
        path.write_text(json.dumps(rows if rows is not None else [{
            "id": "nvda", "ticker": "NVDA", "name": "NVIDIA Corporation",
            "cik": "0001045810", "filer_type": "domestic", "fiscal_year_end": "01-31",
            "priority": "P0", "tags": ["ai-compute"], "include_in_digest": True,
            "transcript": {"source": "none"},
        }]), encoding="utf-8")
        return path

    def test_bad_date_exits_2(self):
        with tempfile.TemporaryDirectory() as td:
            code, _, err = self.run_main(
                ["--date", "yesterday", "--registry", str(self.registry_file(td)),
                 "--out-dir", str(Path(td) / "out")],
                Path(td) / "out",
            )
        self.assertEqual(code, 2)
        self.assertIn("invalid --date", err)

    def test_bad_registry_exits_2(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "registry.json"
            path.write_text('[{"id": "x"}]', encoding="utf-8")
            code, _, err = self.run_main(
                ["--registry", str(path), "--out-dir", str(Path(td) / "out")], Path(td) / "out"
            )
        self.assertEqual(code, 2)
        self.assertIn("invalid registry", err)

    def test_contact_without_address_exits_2(self):
        with tempfile.TemporaryDirectory() as td:
            code, _, err = self.run_main(
                ["--registry", str(self.registry_file(td)), "--out-dir", str(Path(td) / "out"),
                 "--contact", "https://github.com/guzus/ai-research-arm"],
                Path(td) / "out",
            )
        self.assertEqual(code, 2)
        self.assertIn("must be an e-mail address", err)

    def test_quiet_window_writes_nothing_and_exits_0(self):
        """~325 days a year nobody reports; that is NOT an outage."""
        original = earnings.collect_events
        try:
            earnings.collect_events = lambda issuers, **kwargs: ([], [])
            with tempfile.TemporaryDirectory() as td:
                out_dir = Path(td) / "out"
                code, out, _ = self.run_main(
                    ["--registry", str(self.registry_file(td)), "--out-dir", str(out_dir),
                     "--date", "2026-06-15"],
                    out_dir,
                )
                self.assertEqual(code, 0)
                self.assertIn("No earnings events in window", out)
                self.assertFalse(out_dir.exists(), "a quiet day must leave git clean")
        finally:
            earnings.collect_events = original

    def test_total_fetch_failure_exits_3_and_writes_nothing(self):
        rows = [
            {"id": "nvda", "ticker": "NVDA", "name": "NVIDIA", "cik": "0001045810",
             "filer_type": "domestic", "fiscal_year_end": "01-31", "priority": "P0",
             "transcript": {"source": "none"}},
            {"id": "msft", "ticker": "MSFT", "name": "Microsoft", "cik": "0000789019",
             "filer_type": "domestic", "fiscal_year_end": "06-30", "priority": "P0",
             "transcript": {"source": "none"}},
        ]
        original = earnings.http_get
        try:
            def dead(url, accept="*/*", **kwargs):
                raise earnings.FetchError(f"HTTP 503 for {url}")

            earnings.http_get = dead
            with tempfile.TemporaryDirectory() as td:
                out_dir = Path(td) / "out"
                code, out, err = self.run_main(
                    ["--registry", str(self.registry_file(td, rows)), "--out-dir", str(out_dir),
                     "--date", "2026-07-29"],
                    out_dir,
                )
        finally:
            earnings.http_get = original

        self.assertEqual(code, earnings.EXIT_TOTAL_FETCH_FAILURE)
        self.assertEqual(code, 3)  # distinct from 2 (argument validation)
        self.assertFalse(out_dir.exists())
        self.assertNotIn("Wrote", out)
        self.assertIn("total SEC fetch failure", err)
        self.assertIn("NVDA", err)
        self.assertIn("MSFT", err)

    def test_partial_failure_still_writes(self):
        rows = [
            {"id": "nvda", "ticker": "NVDA", "name": "NVIDIA Corporation", "cik": "0001045810",
             "filer_type": "domestic", "fiscal_year_end": "01-31", "priority": "P0",
             "transcript": {"source": "none"}},
            {"id": "msft", "ticker": "MSFT", "name": "Microsoft", "cik": "0000789019",
             "filer_type": "domestic", "fiscal_year_end": "06-30", "priority": "P0",
             "transcript": {"source": "none"}},
        ]
        payloads = {
            "CIK0001045810": json.dumps(submissions([{
                "form": "8-K", "items": "2.02,9.01",
                "accessionNumber": "0001045810-26-000051", "filingDate": "2026-05-20",
                "acceptanceDateTime": "2026-05-20T20:21:19.000Z",
                "primaryDocument": "nvda-20260520.htm",
            }])).encode(),
            "-index.html": index_page([
                ("8-K", "nvda-20260520.htm", "8-K", 26803),
                ("EX-99.1", "q1fy27pr.htm", "EX-99.1", 274829),
            ]).encode(),
            "q1fy27pr.htm": NVDA_RELEASE.encode(),
        }

        original = earnings.http_get
        try:
            def flaky(url, accept="*/*", **kwargs):
                if "CIK0000789019" in url:
                    raise earnings.FetchError(f"HTTP 503 for {url}")
                for fragment, payload in payloads.items():
                    if fragment in url:
                        return payload
                raise earnings.FetchError(f"HTTP 404 for {url}")

            earnings.http_get = flaky
            with tempfile.TemporaryDirectory() as td:
                out_dir = Path(td) / "out"
                code, out, err = self.run_main(
                    ["--registry", str(self.registry_file(td, rows)), "--out-dir", str(out_dir),
                     "--date", "2026-05-20", "--lookback-days", "1"],
                    out_dir,
                )
                written = sorted(path.name for path in out_dir.iterdir())
                index = json.loads((out_dir / "index.json").read_text(encoding="utf-8"))
                first = (out_dir / "2026-05-20-NVDA-FY27Q1.md").read_text(encoding="utf-8")

                # Re-running the same window must be a byte-identical no-op.
                self.run_main(
                    ["--registry", str(self.registry_file(td, rows)), "--out-dir", str(out_dir),
                     "--date", "2026-05-21", "--lookback-days", "2"],
                    out_dir,
                )
                second = (out_dir / "2026-05-20-NVDA-FY27Q1.md").read_text(encoding="utf-8")
        finally:
            earnings.http_get = original

        self.assertEqual(code, 0)
        self.assertEqual(written, ["2026-05-20-NVDA-FY27Q1.md", "index.json"])
        self.assertIn("MSFT", err)
        self.assertEqual(index["count"], 1)
        self.assertEqual(index["events"][0]["ticker"], "NVDA")
        self.assertEqual(index["events"][0]["period"], "FY27Q1")
        self.assertFalse(index["events"][0]["transcript"])
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
