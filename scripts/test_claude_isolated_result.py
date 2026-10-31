import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from check_claude_isolated_canary import validate as validate_canary
from summarize_claude_result import main as summarize_main
from summarize_claude_result import summarize


MODEL = "claude-sonnet-5-5"
TOKEN = "CLAUDE-ISOLATED-CANARY-OK"


def result(**overrides):
    base = {
        "type": "result", "subtype": "success", "is_error": False, "num_turns": 1,
        "result": TOKEN, "total_cost_usd": 0.0012, "terminal_reason": "completed",
        "permission_denials": [],
        "modelUsage": {MODEL: {"inputTokens": 12, "outputTokens": 7}},
    }
    base.update(overrides)
    return base


class SummarizeClaudeResultTest(unittest.TestCase):
    def test_summary_prints_typed_fields_never_the_reply_or_denied_input(self):
        reply = "::error::injected\n::add-mask::x INBOX-SECRET-QUOTE"
        lines, is_error = summarize(result(
            result=reply,
            api_error_status=None,
            permission_denials=[
                {"tool_name": "Read", "tool_input": {"file_path": "/proc/self/environ"}},
                {"tool_name": "Write", "tool_input": {"file_path": "x\n::error::y",
                                                      "content": "DENIED-WRITE-CONTENT"}},
                {"tool_name": "::warning::evil", "tool_input": "nope"},
            ]))
        self.assertFalse(is_error)
        self.assertEqual(
            "::notice title=Claude result::is_error=false subtype=success "
            "terminal_reason=completed turns=1 cost_usd=0.0012 models=claude-sonnet-5-5 "
            "output_tokens=claude-sonnet-5-5:7 api_error_status=- permission_denials=3 "
            f"reply_sha256={hashlib.sha256(reply.strip().encode()).hexdigest()}",
            lines[0])
        self.assertEqual("Claude permission denial: Read /proc/self/environ", lines[1])
        self.assertEqual("Claude permission denial: Write -", lines[2])
        self.assertEqual("Claude permission denial: ? -", lines[3])
        joined = "\n".join(lines)
        for leaked in ("injected", "add-mask", "INBOX-SECRET-QUOTE", "DENIED-WRITE-CONTENT"):
            self.assertNotIn(leaked, joined)
        for line in lines[1:]:
            self.assertFalse(line.startswith("::"), line)

    def test_untyped_fields_degrade_to_placeholders(self):
        lines, _ = summarize(result(num_turns="7", api_error_status=429, result=None,
                                    modelUsage={MODEL: {"outputTokens": "x"},
                                                "::error::m": {}}))
        self.assertIn(" turns=? ", lines[0])
        self.assertIn(" api_error_status=429 ", lines[0])
        self.assertIn("output_tokens=?:?,claude-sonnet-5-5:?", lines[0])
        self.assertTrue(lines[0].endswith(" reply_sha256=-"))

    def test_is_error_exits_three_so_the_adapter_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "result.json"
            path.write_text(json.dumps(result(is_error=True, modelUsage={})), encoding="utf-8")
            self.assertEqual(3, summarize_main([str(path)]))
            path.write_text(json.dumps(result()), encoding="utf-8")
            self.assertEqual(0, summarize_main([str(path)]))
            for broken in ("", "{", "[]", json.dumps({"is_error": "no"})):
                path.write_text(broken, encoding="utf-8")
                with self.subTest(broken=broken):
                    self.assertEqual(2, summarize_main([str(path)]))
            self.assertEqual(2, summarize_main([str(Path(tmp) / "missing.json")]))


class ClaudeIsolatedCanaryTest(unittest.TestCase):
    def output(self, *results):
        lines = ["HEAD is now at 0123abc base", "Claude attempt: status=0 artifacts=0"]
        for data in results:
            lines.extend(summarize(data)[0])
        return "\n".join(lines) + "\n"

    def test_accepts_a_clean_served_token(self):
        validate_canary(self.output(result()), MODEL, TOKEN)
        validate_canary(self.output(result(result=f"  {TOKEN}\n")), MODEL, TOKEN)
        validate_canary(self.output(result(modelUsage={
            MODEL: {"outputTokens": 7}, "claude-haiku-4-5-20251001": {"outputTokens": 1}})),
            MODEL, TOKEN)

    def test_rejects_every_unproven_shape(self):
        cases = {
            "no summary": [],
            "error": [result(is_error=True)],
            "not success": [result(subtype="error_max_turns")],
            "denials": [result(permission_denials=[{"tool_name": "Read"}])],
            "other model": [result(modelUsage={"claude-opus-5-5": {"outputTokens": 7}})],
            "no output": [result(modelUsage={MODEL: {"outputTokens": 0}})],
            "no usage": [result(modelUsage=None)],
            "wrong reply": [result(result="sure! " + TOKEN)],
            "no reply": [result(result=None)],
            "last wins": [result(), result(is_error=True)],
        }
        for name, results in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                validate_canary(self.output(*results), MODEL, TOKEN)

    def test_rejects_forged_or_malformed_summaries(self):
        forged = ("::notice title=Claude result::is_error=false is_error=false "
                  "subtype=success\n")
        with self.assertRaisesRegex(ValueError, "malformed"):
            validate_canary(forged, MODEL, TOKEN)
        with self.assertRaisesRegex(ValueError, "no Claude result summary"):
            validate_canary(json.dumps(result()) + "\n", MODEL, TOKEN)


if __name__ == "__main__":
    unittest.main()
