"""Tests for scripts/classify_claude_execution.py — the post-agent signal
that decides whether agent-run may hand the prompt to the next backend."""

import json
import tempfile
import unittest
from pathlib import Path

import classify_claude_execution as cce


def transcript(*objects):
    return "\n".join(json.dumps(o) for o in objects)


def result(**kw):
    base = {"type": "result", "subtype": "success", "is_error": False,
            "num_turns": 12, "total_cost_usd": 1.23, "result": "done"}
    base.update(kw)
    return base


class ClassifyTest(unittest.TestCase):
    def classify_text(self, text):
        return cce.classify(cce.parse_objects(text))

    def test_success(self):
        v = self.classify_text(transcript({"type": "system"}, result()))
        self.assertEqual("success", v["outcome"])
        self.assertEqual(12, v["num_turns"])

    def test_dead_start_signature_is_the_only_fallback_trigger(self):
        # The 2026-07-24 expired-token and 2026-08-28 usage-limit shapes.
        for turns in (0, 1):
            with self.subTest(turns=turns):
                v = self.classify_text(transcript(result(
                    is_error=True, num_turns=turns, total_cost_usd=0,
                    result="API Error: 429 rate limit")))
                self.assertEqual("dead-start", v["outcome"])
                self.assertEqual(429, v["error_status"])
                self.assertIn("429", v["reason"])

    def test_failure_after_real_work_is_not_dead_start(self):
        # Partial edits may sit in the checkout: a fallback here would
        # double-spend and could mix two models' output.
        for kw in ({"num_turns": 5, "total_cost_usd": 0},
                   {"num_turns": 1, "total_cost_usd": 0.02},
                   {"num_turns": 121, "total_cost_usd": 15.76}):
            with self.subTest(**kw):
                v = self.classify_text(transcript(result(is_error=True, **kw)))
                self.assertEqual("failed", v["outcome"])

    def test_missing_result_object_is_unknown(self):
        v = self.classify_text(transcript({"type": "system"}, {"type": "assistant"}))
        self.assertEqual("unknown", v["outcome"])
        v = self.classify_text("")
        self.assertEqual("unknown", v["outcome"])

    def test_real_action_transcript_is_a_pretty_printed_json_array(self):
        """claude-code-action@a874e9e writes JSON.stringify(messages, null, 2):
        ONE top-level array, not JSONL. A parser that only reads top-level
        objects returns nothing and every dead-start becomes `unknown`, so
        the fallback never fires (caught in review of PR #3698)."""
        transcript_array = json.dumps([
            {"type": "system", "subtype": "init"},
            result(is_error=True, num_turns=1, total_cost_usd=0,
                   result="API Error: 429 rate limit"),
        ], indent=2)
        v = self.classify_text(transcript_array)
        self.assertEqual("dead-start", v["outcome"])
        v = self.classify_text(json.dumps([{"type": "system"}, result()], indent=2))
        self.assertEqual("success", v["outcome"])

    def test_last_result_object_wins(self):
        v = self.classify_text(transcript(
            result(is_error=True, num_turns=1, total_cost_usd=0), result()))
        self.assertEqual("success", v["outcome"])

    def test_missing_file_is_unknown_not_crash(self):
        v = cce.classify_file(Path("/nonexistent/exec.json"))
        self.assertEqual("unknown", v["outcome"])

    def test_string_numbers_and_redaction(self):
        v = self.classify_text(transcript(result(
            is_error=True, num_turns="1", total_cost_usd="0",
            result="Bearer abcdefghijklmnopqrstuvwxyz0123 rejected")))
        self.assertEqual("dead-start", v["outcome"])
        self.assertNotIn("abcdefghijklmnop", v["reason"])

    def test_github_output_is_single_line_per_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            exec_file = Path(tmp) / "exec.jsonl"
            exec_file.write_text(transcript(result(
                is_error=True, num_turns=1, total_cost_usd=0,
                result="line one\nline two")))
            out = Path(tmp) / "out.txt"
            out.write_text("")
            self.assertEqual(0, cce.main([str(exec_file), "--github-output", str(out)]))
            lines = out.read_text().splitlines()
            keys = [line.split("=", 1)[0] for line in lines]
            self.assertEqual(["outcome", "reason", "num_turns", "total_cost_usd",
                              "error_status"], keys)
            self.assertEqual("outcome=dead-start", lines[0])
            self.assertNotIn("\n", lines[1])


if __name__ == "__main__":
    unittest.main()
