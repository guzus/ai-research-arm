import io
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from check_cursor_canary import main as canary_main
from check_cursor_canary import validate as validate_canary
from summarize_claude_result import reply_sha256 as claude_reply_sha256
from summarize_cursor_result import (CLI_ERRORS, MAX_RESULT_BYTES, SUMMARY_PREFIX, cli_error,
                                     read_result, reply_sha256, summarize)
from summarize_cursor_result import main as summarize_main


TOKEN = "CURSOR-CLI-CANARY-OK"
# Attempt logs of real Cursor CLI Canary runs, verbatim (the model list of
# 32004994067 shortened).
CANARY_REPLY = b"CURSOR-CLI-CANARY-OK\n"  # 31998732492 ... 40136175298
USAGE_LIMIT = (b"ActionRequiredError: Weekly usage limit reached. It resets in 4 days. Buy "
               b"credits to keep going now, or upgrade your plan for more weekly usage.\n")
BAD_MODEL = (b"Cannot use this model: grok-4.6-fast. Available models: auto, gpt-5.3-codex-low, "
             b"cursor-grok-4.6-high-fast, composer-2.5, kimi-k2.7-code, glm-5.2-high, "
             b"glm-5.2-max\n")
# A reply that tries every workflow-command and line-splitting trick.
HOSTILE = (b"done\r::add-mask::SECRET-VALUE\n::error::INJECTED\n"
           b"::stop-commands::x\r\n%0A::warning::y\x1b[31m\x85\xe2\x80\xa8tail")
SUMMARY = re.compile(
    r"::notice title=Cursor result::status=[0-9]{1,3} reply_sha256=(?:[0-9a-f]{64}|-) "
    r"reply_bytes=(?:[0-9]+|-) reply_lines=(?:[0-9]+|-) cli_error=(?:"
    + "|".join(CLI_ERRORS) + r")")


def summary_of(path: Path, status: str = "0") -> str:
    out = io.StringIO()
    with mock.patch("sys.stdout", new=out):
        code = summarize_main(["--status", status, "--result-file", str(path)])
    assert code == 0
    return out.getvalue()


class SummarizeCursorResultTest(unittest.TestCase):
    def assert_typed_line(self, text: str) -> None:
        self.assertTrue(text.endswith("\n"), repr(text))
        line = text[:-1]
        self.assertRegex(line, f"^{SUMMARY.pattern}$")
        self.assertNotIn("\r", line)
        self.assertNotIn("\n", line)
        self.assertEqual(1, line.count("::notice"))
        self.assertEqual(2, line.count("::"))

    def test_summary_prints_typed_fields_never_the_reply(self):
        for status in (0, 1, 124):
            for raw in (CANARY_REPLY, USAGE_LIMIT, BAD_MODEL, HOSTILE, b"", b"\xff\xfe\x00"):
                with self.subTest(status=status, raw=raw[:20]):
                    line = summarize(status, raw)
                    self.assert_typed_line(line + "\n")
                    for leaked in (b"SECRET-VALUE", b"INJECTED", b"add-mask", b"stop-commands",
                                   b"warning", b"Weekly", b"grok-4.6-fast", b"CANARY-OK"):
                        self.assertNotIn(leaked.decode(), line)
        self.assertEqual(
            f"{SUMMARY_PREFIX}status=0 reply_sha256={reply_sha256(TOKEN)} reply_bytes=21 "
            "reply_lines=1 cli_error=none", summarize(0, CANARY_REPLY))

    def test_hash_is_the_claude_reply_convention(self):
        for reply in (TOKEN, f"  {TOKEN}\n", "", "two\nlines\n", "é　"):
            self.assertEqual(claude_reply_sha256(reply), reply_sha256(reply))
        # Trailing newline and surrounding whitespace do not change the digest.
        self.assertIn(f"reply_sha256={reply_sha256(TOKEN)} ",
                      summarize(0, b"\n  CURSOR-CLI-CANARY-OK \r\n"))
        self.assertNotIn(f"reply_sha256={reply_sha256(TOKEN)} ",
                         summarize(0, b"Sure: CURSOR-CLI-CANARY-OK\n"))

    def test_sizes_count_bytes_and_newline_delimited_lines(self):
        self.assertIn(" reply_bytes=0 reply_lines=0 ", summarize(1, b""))
        self.assertIn(" reply_bytes=1 reply_lines=1 ", summarize(0, b"x"))
        self.assertIn(" reply_bytes=4 reply_lines=2 ", summarize(0, b"a\nbc"))
        self.assertIn(" reply_bytes=2 reply_lines=2 ", summarize(0, b"\n\n"))
        # A bare carriage return is not a line break; it is never printed either.
        self.assertIn(" reply_bytes=4 reply_lines=1 ", summarize(0, b"a\rb\n"))

    def test_classifies_known_cli_error_text(self):
        cases = {
            "usage_limit": [USAGE_LIMIT, b"Insufficient credits", b"402 Payment Required"],
            "model": [BAD_MODEL, b"Model not found: x", b"No models available for this account."],
            "auth": [b"\xe2\x9a\xa0 Warning: The provided API key is invalid.\n",
                     b"Error: Authentication required. Please run 'agent login' first",
                     b"Your stored authentication is invalid. Please log in again.",
                     b"[unauthenticated] token expired", b"401 Unauthorized"],
            "network": [b"ConnectError: [unavailable] getaddrinfo ENOTFOUND api2.cursor.sh",
                        b"TypeError: fetch failed", b"socket hang up", b"read ECONNRESET",
                        b"UND_ERR_CONNECT_TIMEOUT"],
            "other": [b"", b"Segmentation fault", b"\xff\xfe", b"xECONNRESETx", b"EPIPELINE"],
        }
        for expected, texts in cases.items():
            for raw in texts:
                with self.subTest(expected=expected, raw=raw[:40]):
                    self.assertTrue(summarize(1, raw).endswith(f" cli_error={expected}"))
        # Auth and billing (the fatal pattern's families) win over the rest.
        self.assertEqual("auth", cli_error(1, "Unauthorized: usage limit, fetch failed"))
        self.assertEqual("usage_limit", cli_error(143, "usage limit; Cannot use this model"))
        self.assertEqual("model", cli_error(1, "Cannot use this model after socket hang up"))

    def test_exit_zero_is_none_whatever_the_reply_says(self):
        # On success the file is the model reply: its words prove nothing.
        for raw in (USAGE_LIMIT, BAD_MODEL, b"Unauthorized access was the story", b""):
            self.assertTrue(summarize(0, raw).endswith(" cli_error=none"))
        self.assertEqual("none", cli_error(0, None))
        self.assertEqual("other", cli_error(2, None))

    def test_unreadable_results_degrade_to_placeholders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "elsewhere.txt"
            target.write_bytes(CANARY_REPLY)
            link = root / "link.txt"
            link.symlink_to(target)
            fifo = root / "fifo"
            os.mkfifo(fifo)
            folder = root / "folder"
            folder.mkdir()
            oversized = root / "oversized.txt"
            oversized.write_bytes(b"x" * (MAX_RESULT_BYTES + 1))
            at_cap = root / "at-cap.txt"
            at_cap.write_bytes(b"y" * MAX_RESULT_BYTES)
            for path in (link, fifo, folder, oversized, root / "missing.txt"):
                with self.subTest(path=path.name):
                    self.assertIsNone(read_result(path))
                    text = summary_of(path, "1")
                    self.assert_typed_line(text)
                    self.assertTrue(text.endswith(
                        " reply_sha256=- reply_bytes=- reply_lines=- cli_error=other\n"))
            self.assertIn(" reply_bytes=1048576 reply_lines=1 ", summary_of(at_cap))
            self.assertEqual(CANARY_REPLY, read_result(target))
            # No file at all: the host rejected it.
            out = io.StringIO()
            with mock.patch("sys.stdout", new=out):
                self.assertEqual(0, summarize_main(["--status", "0"]))
            self.assertEqual(f"{SUMMARY_PREFIX}status=0 reply_sha256=- reply_bytes=- "
                             "reply_lines=- cli_error=none\n", out.getvalue())

    def test_status_must_be_a_host_exit_status(self):
        for bad in ("", "-1", "256", "1000", "0x1", " 1", "1\n", "+1", "٣", "1.0"):
            out, err = io.StringIO(), io.StringIO()
            with self.subTest(bad=bad), mock.patch("sys.stdout", new=out), \
                    mock.patch("sys.stderr", new=err), self.assertRaises(SystemExit) as raised:
                summarize_main(["--status", bad])
            self.assertEqual(2, raised.exception.code)
            self.assertEqual("", out.getvalue())
        self.assertIn("status=255 ", summarize(255, b""))


class CursorCanaryTest(unittest.TestCase):
    def output(self, *summaries: str, tail: str = "") -> str:
        lines = ["HEAD is now at 0123abc base",
                 "Cursor attempt 1: status=0 translation_segment_calls=0 artifacts=0 "
                 "remaining_seconds=600"]
        lines.extend(summaries)
        return "\n".join(lines) + "\n" + tail

    def test_accepts_the_exact_token(self):
        validate_canary(self.output(summarize(0, CANARY_REPLY)), TOKEN)
        validate_canary(self.output(summarize(0, b"  CURSOR-CLI-CANARY-OK \r\n")), TOKEN)
        validate_canary(self.output(summarize(0, CANARY_REPLY), tail="\n\n"), TOKEN)
        validate_canary(self.output(summarize(1, USAGE_LIMIT), summarize(0, CANARY_REPLY)),
                        TOKEN)

    def test_rejects_every_unproven_shape(self):
        cases = {
            "no summary": [],
            "exit 1": [summarize(1, CANARY_REPLY)],
            "timeout": [summarize(124, CANARY_REPLY)],
            "usage limit": [summarize(1, USAGE_LIMIT)],
            "wrong reply": [summarize(0, b"Sure! CURSOR-CLI-CANARY-OK\n")],
            "token in a longer reply": [summarize(0, b"CURSOR-CLI-CANARY-OK\nextra\n")],
            "empty reply": [summarize(0, b"")],
            "no reply": [summarize(0, None)],
            "last wins": [summarize(0, CANARY_REPLY), summarize(1, CANARY_REPLY)],
        }
        for name, summaries in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                validate_canary(self.output(*summaries), TOKEN)

    def test_rejects_forged_or_malformed_summaries(self):
        good = summarize(0, CANARY_REPLY)
        # Container output after the summary means the summary is not the
        # host's final append.
        with self.assertRaisesRegex(ValueError, "not the final line"):
            validate_canary(self.output(good, tail="Cursor attempt 2: status=0\n"), TOKEN)
        with self.assertRaisesRegex(ValueError, "not the final line"):
            validate_canary(self.output(good, tail="x\r" + good + "\n"), TOKEN)
        for forged in (good + " status=0", good.replace(" cli_error=none", ""),
                       good + " extra=1", good.replace("status=0", "status=00000"),
                       good.replace(" reply_lines=1", "  reply_lines=1"),
                       good.replace("cli_error=none", "cli_error=fine"),
                       good.replace("reply_sha256=", "reply_sha256=X")):
            with self.subTest(forged=forged), self.assertRaisesRegex(ValueError, "malformed"):
                validate_canary(self.output(forged), TOKEN)
        with self.assertRaisesRegex(ValueError, "no Cursor result summary"):
            validate_canary(CANARY_REPLY.decode(), TOKEN)

    def test_main_reports_one_error_line_and_exit_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "canary.out"
            path.write_text(self.output(summarize(0, CANARY_REPLY)), encoding="utf-8")
            out = io.StringIO()
            with mock.patch("sys.stdout", new=out):
                self.assertEqual(0, canary_main([str(path), "--token", TOKEN]))
            self.assertIn("Verified isolated Cursor CLI canary", out.getvalue())
            path.write_text(self.output(summarize(1, USAGE_LIMIT)), encoding="utf-8")
            out = io.StringIO()
            with mock.patch("sys.stdout", new=out):
                self.assertEqual(1, canary_main([str(path), "--token", TOKEN]))
            self.assertEqual("::error::Cursor CLI canary failed: canary Cursor run exited 1 "
                             "(cli_error=usage_limit); check the API key, quota, and model.\n",
                             out.getvalue())
            out = io.StringIO()
            with mock.patch("sys.stdout", new=out):
                self.assertEqual(1, canary_main([str(Path(tmp) / "missing"), "--token", TOKEN]))
            self.assertEqual("::error::Cursor CLI canary output is unreadable "
                             "(FileNotFoundError).\n", out.getvalue())


if __name__ == "__main__":
    unittest.main()
