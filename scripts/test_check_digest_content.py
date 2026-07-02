#!/usr/bin/env python3
"""Tests for the daily-digest content floor checker."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import check_digest_content as floor  # noqa: E402


def healthy_digest(*, sections: int = 5, pad_bytes: int = 5000) -> str:
    body = ["# AI Daily Digest - 2026-07-02", ""]
    for index in range(sections):
        body.extend([f"## Section {index}", "", f"- real story {index} with detail", ""])
    body.append("x" * pad_bytes)
    return "\n".join(body)


class CheckDigestTest(unittest.TestCase):
    def test_healthy_digest_passes(self):
        failures = floor.check_digest(healthy_digest(), min_bytes=4000, min_sections=3)
        self.assertEqual(failures, [])

    def test_sub_floor_bytes_fail(self):
        failures = floor.check_digest(
            healthy_digest(pad_bytes=0), min_bytes=4000, min_sections=3
        )
        self.assertEqual(len(failures), 1)
        self.assertIn("byte floor", failures[0])

    def test_too_few_sections_fail(self):
        failures = floor.check_digest(
            healthy_digest(sections=2), min_bytes=4000, min_sections=3
        )
        self.assertEqual(len(failures), 1)
        self.assertIn("section floor", failures[0])

    def test_unexpanded_template_placeholders_fail_even_when_large(self):
        text = healthy_digest() + "\n## Executive Summary\n[3-5 bullet points of the day]\n"
        failures = floor.check_digest(text, min_bytes=4000, min_sections=3)
        self.assertEqual(len(failures), 1)
        self.assertIn("placeholder", failures[0])
        self.assertIn("[3-5 bullet", failures[0])

    def test_count_placeholder_fails_but_markdown_links_do_not(self):
        with_link = healthy_digest() + "\n- [a real link](https://example.com) and [count of X]\n"
        self.assertEqual(floor.check_digest(with_link, min_bytes=4000, min_sections=3), [])

        with_placeholder = healthy_digest() + "\n- Twitter: [count] updates\n"
        failures = floor.check_digest(with_placeholder, min_bytes=4000, min_sections=3)
        self.assertEqual(len(failures), 1)
        self.assertIn("'[count]'", failures[0])

    def test_multiple_failures_all_reported(self):
        failures = floor.check_digest("## One\n[Headline 1]", min_bytes=4000, min_sections=3)
        self.assertEqual(len(failures), 3)


class MainTest(unittest.TestCase):
    def test_missing_file_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = floor.main(["--file", str(Path(tmp) / "absent.md")])
        self.assertEqual(code, 1)

    def test_healthy_file_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "digest.md"
            path.write_text(healthy_digest(), encoding="utf-8")
            code = floor.main(["--file", str(path), "--min-bytes", "4000", "--min-sections", "3"])
        self.assertEqual(code, 0)

    def test_extra_placeholder_flag_is_honored(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "digest.md"
            path.write_text(healthy_digest() + "\nTODO-FILL-ME\n", encoding="utf-8")
            self.assertEqual(floor.main(["--file", str(path)]), 0)
            self.assertEqual(
                floor.main(["--file", str(path), "--placeholder", "TODO-FILL-ME"]), 1
            )


if __name__ == "__main__":
    unittest.main()
