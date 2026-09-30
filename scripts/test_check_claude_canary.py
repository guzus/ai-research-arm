import copy
import tempfile
import unittest
from pathlib import Path

from check_claude_canary import validate


class CanaryTests(unittest.TestCase):
    def test_requires_requested_model_and_real_tool_round_trip(self):
        model = "claude-opus-5-5"
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "fixture.txt"
            fixture.write_text("unpredictable sentinel\n")
            transcript = [
                {"type": "assistant", "message": {"model": model, "content": [
                    {"type": "tool_use", "id": "read-1", "name": "Read", "input": {"file_path": str(fixture)}}]}},
                {"type": "user", "message": {"content": [
                    {"type": "tool_result", "tool_use_id": "read-1", "content": "1: unpredictable sentinel"}]}},
                {"type": "result", "is_error": False, "subtype": "success",
                 "modelUsage": {model: {"outputTokens": 10}}, "result": "unpredictable sentinel"},
            ]
            validate(transcript, model, fixture)
            cases = []
            for field, value in (("is_error", True), ("subtype", "error_max_turns"),
                                 ("modelUsage", {}), ("permission_denials", [{"tool_name": "Read"}]),
                                 ("result", "guessed answer")):
                changed = copy.deepcopy(transcript)
                changed[-1][field] = value
                cases.append(changed)
            wrong_model = copy.deepcopy(transcript)
            wrong_model[0]["message"]["model"] = "claude-opus-5"
            cases.extend([wrong_model, transcript[-1:], transcript[:1],
                          [transcript[0], transcript[-1]], []])
            for case in cases:
                with self.subTest(case=case), self.assertRaises(ValueError):
                    validate(case, model, fixture)
