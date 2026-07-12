#!/usr/bin/env python3
"""Tests for scripts/check_model_tickets.py — focused on the optional
`polymarket:` frontmatter contract (docs/model-tickets.md, "Polymarket
market mappings") plus a base-schema smoke test."""

import tempfile
import textwrap
import unittest
from pathlib import Path

import check_model_tickets as cmt

VALID_MAPPING = textwrap.dedent(
    """\
    polymarket:
      - event_slug: anthropic-ipo-by
        market_id: "2413330"
        token_id: "48566046548914168443252668519852295704538578584318207505303160546351275413281"
        question: "Anthropic IPO by Dec 31, 2026?"
        outcome: "Dec 31 2026"
    """
)


def make_ticket(polymarket_block: str = "") -> str:
    return textwrap.dedent(
        """\
        ---
        slug: test-ticket
        title: Test ticket
        company: TestCo
        model: TestModel
        status: confirmed
        verification: confirmed
        sources:
          - "@testhandle"
        {polymarket}created_at: 2026-07-01
        updated_at: 2026-07-13
        closed_at: null
        closed_reason: null
        history:
          - ts: 2026-07-01
            change: Created
        ---

        Body narrative.
        """
    ).format(polymarket=polymarket_block)


class CheckPolymarketTest(unittest.TestCase):
    def check(self, text: str) -> cmt.Report:
        report = cmt.Report()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test-ticket.md"
            path.write_text(text, encoding="utf-8")
            cmt.check_ticket(path, report)
        return report

    def polymarket_failures(self, report: cmt.Report) -> list[str]:
        return [f.msg for f in report.failures if f.field == "polymarket"]

    def test_absent_key_passes(self):
        report = self.check(make_ticket())
        self.assertTrue(report.ok(), [f"{f.field}: {f.msg}" for f in report.failures])

    def test_valid_mapping_passes(self):
        report = self.check(make_ticket(VALID_MAPPING))
        self.assertTrue(report.ok(), [f"{f.field}: {f.msg}" for f in report.failures])

    def test_null_key_passes(self):
        report = self.check(make_ticket("polymarket: null\n"))
        self.assertTrue(report.ok(), [f"{f.field}: {f.msg}" for f in report.failures])

    def test_outcome_is_optional(self):
        block = "\n".join(line for line in VALID_MAPPING.splitlines() if "outcome" not in line) + "\n"
        report = self.check(make_ticket(block))
        self.assertTrue(report.ok(), [f"{f.field}: {f.msg}" for f in report.failures])

    def test_missing_token_id_fails(self):
        block = "\n".join(line for line in VALID_MAPPING.splitlines() if "token_id" not in line) + "\n"
        report = self.check(make_ticket(block))
        self.assertFalse(report.ok())
        self.assertTrue(any("token_id" in msg for msg in self.polymarket_failures(report)))

    def test_unquoted_numeric_market_id_fails(self):
        block = VALID_MAPPING.replace('market_id: "2413330"', "market_id: 2413330")
        report = self.check(make_ticket(block))
        self.assertFalse(report.ok())
        self.assertTrue(any("market_id" in msg for msg in self.polymarket_failures(report)))

    def test_unquoted_numeric_token_id_fails(self):
        # token_id is the load-bearing precision field: unquoted, YAML parses
        # the ~78-digit id as a number (and JS parsers lose precision), so the
        # validator must reject non-string values outright.
        block = VALID_MAPPING.replace(
            'token_id: "48566046548914168443252668519852295704538578584318207505303160546351275413281"',
            "token_id: 48566046548914168443252668519852295704538578584318207505303160546351275413281",
        )
        self.assertNotEqual(block, VALID_MAPPING)  # guard: replacement matched
        report = self.check(make_ticket(block))
        self.assertFalse(report.ok())
        self.assertTrue(any("token_id" in msg for msg in self.polymarket_failures(report)))

    def test_more_than_three_mappings_fails(self):
        entry_lines = "\n".join(VALID_MAPPING.splitlines()[1:])  # the "- event_slug: ..." mapping lines
        block = "polymarket:\n" + (entry_lines + "\n") * 4
        report = self.check(make_ticket(block))
        self.assertFalse(report.ok())
        self.assertTrue(any("at most 3" in msg for msg in self.polymarket_failures(report)))

    def test_empty_list_fails(self):
        report = self.check(make_ticket("polymarket: []\n"))
        self.assertFalse(report.ok())
        self.assertTrue(any("omit the key" in msg for msg in self.polymarket_failures(report)))

    def test_unknown_key_inside_mapping_fails(self):
        block = VALID_MAPPING.rstrip() + '\n    midpoint: "0.5"\n'
        report = self.check(make_ticket(block))
        self.assertFalse(report.ok())
        self.assertTrue(any("unknown key" in msg for msg in self.polymarket_failures(report)))

    def test_non_list_fails(self):
        report = self.check(make_ticket('polymarket: "anthropic-ipo-by"\n'))
        self.assertFalse(report.ok())
        self.assertTrue(any("must be a list" in msg for msg in self.polymarket_failures(report)))

    def test_base_schema_still_enforced(self):
        # Sanity: an unrelated schema violation still fails alongside the new key.
        text = make_ticket(VALID_MAPPING).replace("status: confirmed", "status: imaginary")
        report = self.check(text)
        self.assertFalse(report.ok())
        self.assertTrue(any(f.field == "status" for f in report.failures))


if __name__ == "__main__":
    unittest.main()
