import io
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import summarize_cursor_result
from summarize_claude_result import reply_sha256 as claude_reply_sha256
from summarize_pi_result import (CLI_ERRORS, MAX_RESULT_BYTES, SUMMARY_PREFIX, cli_error,
                                 read_result, reply_sha256, summarize)
from summarize_pi_result import main as summarize_main


# Provider errors as pi prints them (assistantMsg.errorMessage), and a reply
# that tries every workflow-command and line-splitting trick.
SUSPENDED = (b"412 Account getclarito-5mege6wpl is suspended, possibly due to reaching the "
             b"monthly spending limit or failure to pay past invoices\n")
HOSTILE = (b"done\r::add-mask::SECRET-VALUE\n::error::INJECTED\n##[warning]legacy\n"
           b"::stop-commands::x\r\n%0A::warning::y\x1b[31m\x85\xe2\x80\xa8tail")
SUMMARY = re.compile(
    r"::notice title=pi result::status=[0-9]{1,3} reply_sha256=(?:[0-9a-f]{64}|-) "
    r"reply_bytes=(?:[0-9]+|-) reply_lines=(?:[0-9]+|-) cli_error=(?:"
    + "|".join(CLI_ERRORS) + r")")


class SummarizePiResultTest(unittest.TestCase):
    def test_summary_prints_typed_fields_never_the_reply(self):
        for status in (0, 1, 124):
            for raw in (b"## 10:00 UTC\nDigest\n", SUSPENDED, HOSTILE, b"", b"\xff\xfe\x00"):
                with self.subTest(status=status, raw=raw[:20]):
                    line = summarize(status, raw)
                    self.assertRegex(line, f"^{SUMMARY.pattern}$")
                    self.assertEqual(2, line.count("::"))
                    self.assertNotIn("##[", line)
                    for leaked in ("SECRET-VALUE", "INJECTED", "add-mask", "legacy", "suspended",
                                   "Digest", "\r", "\n"):
                        self.assertNotIn(leaked, line)

    def test_shares_the_reply_hash_and_file_rules_of_the_cursor_summary(self):
        for reply in ("TOKEN", "  TOKEN\n", "", "two\nlines\n", "é　"):
            self.assertEqual(claude_reply_sha256(reply), reply_sha256(reply))
        self.assertEqual(summarize_cursor_result.MAX_RESULT_BYTES, MAX_RESULT_BYTES)
        for raw in (b"", b"x", b"a\nbc", b"\n\n", HOSTILE):
            pi_fields = summarize(0, raw)[len(SUMMARY_PREFIX):]
            cursor_fields = summarize_cursor_result.summarize(0, raw)[
                len(summarize_cursor_result.SUMMARY_PREFIX):]
            self.assertEqual(cursor_fields, pi_fields)

    def test_classifies_known_provider_error_text(self):
        cases = {
            "auth": (b"401 Unauthorized\n", b"Error: Invalid API key\n", b"403 Forbidden\n"),
            "usage_limit": (SUSPENDED, b"402 Payment Required\n", b"Insufficient credits\n"),
            "rate_limit": (b"429 Too Many Requests\n", b"rate limit exceeded\n"),
            "model": (b"No models available. Use --list-models\n", b"404 model not found\n"),
            "network": (b"TypeError: fetch failed\n", b"connect ECONNREFUSED 1.2.3.4:443\n"),
            "other": (b"Error: something new\n", b""),
        }
        for expected, samples in cases.items():
            for raw in samples:
                with self.subTest(raw=raw):
                    self.assertTrue(summarize(1, raw).endswith(f"cli_error={expected}"))
        # A successful reply proves nothing about errors, whatever it says.
        self.assertEqual("none", cli_error(0, SUSPENDED.decode()))
        self.assertEqual("other", cli_error(1, None))

    def test_unreadable_results_degrade_to_placeholders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target.txt"
            target.write_bytes(b"secret\n")
            os.symlink(target, root / "link.txt")
            os.mkfifo(root / "fifo")
            (root / "big.txt").write_bytes(b"x" * (MAX_RESULT_BYTES + 1))
            for name in ("link.txt", "fifo", "big.txt", "missing.txt"):
                with self.subTest(name=name):
                    self.assertIsNone(read_result(root / name))
                    out = io.StringIO()
                    with mock.patch("sys.stdout", new=out):
                        self.assertEqual(0, summarize_main(["--status", "1", "--result-file",
                                                            str(root / name)]))
                    self.assertIn("reply_sha256=- reply_bytes=- reply_lines=- cli_error=other",
                                  out.getvalue())
            self.assertEqual(b"secret\n", read_result(target))

    def test_status_must_be_a_host_exit_status(self):
        for bad in ("-1", "256", "1e2", "", "0;id"):
            with self.subTest(bad=bad), self.assertRaises(SystemExit):
                with mock.patch("sys.stderr", new=io.StringIO()):
                    summarize_main(["--status", bad])
        out = io.StringIO()
        with mock.patch("sys.stdout", new=out):
            self.assertEqual(0, summarize_main(["--status", "7"]))
        self.assertEqual(f"{SUMMARY_PREFIX}status=7 reply_sha256=- reply_bytes=- "
                         "reply_lines=- cli_error=other\n", out.getvalue())


if __name__ == "__main__":
    unittest.main()
