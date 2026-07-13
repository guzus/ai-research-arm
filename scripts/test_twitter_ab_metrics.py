#!/usr/bin/env python3
"""Tests for twitter_ab_metrics.py (+ report rendering smoke)."""

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import twitter_ab_metrics as ab
import twitter_ab_report as report

DATE = "2026-07-13"
HOUR = "21"
TS = "2026-07-13 21:40:00 UTC"
RUN_ID = "424242"
RUN_ATTEMPT = 1
SNAPSHOT_SHA = "a" * 64

STORY = """<article class="twitter-story" data-rank="1">
  <h3 class="twitter-story-title">Anthropic ships a 2M-token context window for enterprise</h3>
  <p class="twitter-story-lead">Anthropic enabled a 2M-token context tier priced at $4/MTok, per the official account.</p>
  <details class="twitter-story-details">
    <summary>Full analysis</summary>
    <div class="twitter-story-sources">
      <a class="twitter-source-chip" href="https://x.com/AnthropicAI/status/123456789">@AnthropicAI</a>
    </div>
    <div class="twitter-story-signals">
      <div><span>Verify</span>✓ multi-source confirmed — official post plus docs page</div>
      <div><span>Watch</span>Pricing page diff within 24h</div>
    </div>
    <div class="twitter-story-body">
      <p><strong>Evidence:</strong> Official announcement with docs link and $4/MTok figure.</p>
      <p><strong>Counter / contradicting:</strong> Docs still show the old tier for some regions.</p>
    </div>
  </details>
</article>"""


def make_digest() -> str:
    return (
        f"# Twitter/X AI Pulse (A/B eval) — {DATE}\n\n"
        f"## {HOUR}:00 UTC\n\n"
        "**Cycle summary**: Anthropic shipped a 2M-token enterprise context tier at $4/MTok.\n\n"
        "### Top stories\n\n"
        f"{STORY}\n\n"
        "### Watch list (next 24h)\n"
        "- Pricing page diff for the enterprise tier\n"
    )


def make_status(status="published", public_items=1) -> dict:
    return {
        "schema_version": 1,
        "date": DATE,
        "hour": f"{HOUR}:00 UTC",
        "generated_at": TS,
        "run_id": RUN_ID,
        "run_attempt": RUN_ATTEMPT,
        "status": status,
        "public_items": public_items,
    }


def make_execution_jsonl(
    *, is_error=False, num_turns=21, cost=1.234, denials=0, models=("claude-sonnet-5",)
) -> str:
    result = {
        "type": "result",
        "subtype": "success" if not is_error else "error_during_execution",
        "is_error": is_error,
        "duration_ms": 654321,
        "duration_api_ms": 500000,
        "num_turns": num_turns,
        "total_cost_usd": cost,
        "usage": {"input_tokens": 90000, "output_tokens": 8000},
        "permission_denials": [
            {"tool_name": "Bash", "tool_use_id": f"d{i}"} for i in range(denials)
        ],
        "modelUsage": {m: {"inputTokens": 1} for m in models},
    }
    return (
        json.dumps({"type": "system", "subtype": "init"})
        + "\n"
        + json.dumps({"type": "assistant", "message": {"content": "..."}})
        + "\n"
        + json.dumps(result)
        + "\n"
    )


class Fixture:
    """One leg on disk: output dir + execution transcript + meta JSON."""

    def __init__(self, root: Path, leg: str, expected_provider: str, expected_model: str):
        self.root = root
        self.leg = leg
        self.leg_dir = root / "research" / "eval" / "twitter-ab" / DATE / leg
        self.meta = {
            "leg": leg,
            "lane": f"twitter-ab-{'claude' if leg == 'claude' else 'zai'}",
            "expected_provider": expected_provider,
            "expected_model": expected_model,
            "outcome": "success",
            "requested_backend": "claude" if expected_provider == "claude" else "zai-glm-5p2",
            "effective_backend": "claude" if expected_provider == "claude" else "zai-glm-5p2",
            "used_fallback": "false",
            "model_id": "" if expected_provider == "claude" else expected_model,
            "native_model": expected_model if expected_provider == "claude" else "claude-sonnet-5",
            "execution_file": "",
            "leg_dir": str(self.leg_dir),
            "input_sha_pre": SNAPSHOT_SHA,
            "input_sha_post": SNAPSHOT_SHA,
            "prompt_sha256": "b" * 64,
            "started_at_epoch": 1000,
            "finished_at_epoch": 1500,
            "base_sha": "base000",
            "post_sha": "post111",
        }

    def write_artifacts(self, *, digest=True, headlines=None, execution_kwargs=None):
        execution_kwargs = dict(execution_kwargs or {})
        # The transcript's modelUsage must default to the leg's own expected
        # model, or the expected-model-not-observed guard (correctly) trips.
        execution_kwargs.setdefault("models", (self.meta["expected_model"],))
        self.leg_dir.mkdir(parents=True, exist_ok=True)
        (self.leg_dir / "status").mkdir(exist_ok=True)
        if digest:
            (self.leg_dir / f"{DATE}.md").write_text(make_digest())
            (self.leg_dir / "status" / f"{DATE}-{HOUR}h.json").write_text(
                json.dumps(make_status())
            )
            (self.leg_dir / f"{DATE}-twitter-ab-{HOUR}h-summary.txt").write_text(
                f"Twitter/X AI Pulse (A/B eval) - {TS}\n\nTOP STORIES:\n- 2M context tier\n"
            )
        else:
            (self.leg_dir / "status" / f"{DATE}-{HOUR}h.json").write_text(
                json.dumps(make_status(status="no_update", public_items=0))
            )
            (self.leg_dir / f"{DATE}-twitter-ab-{HOUR}h-summary.txt").write_text("")
        if headlines is None:
            headlines = (
                [
                    {
                        "headline": "ANTHROPIC SHIPS 2M-TOKEN ENTERPRISE CONTEXT AT $4/MTOK",
                        "source": "@AnthropicAI",
                        "url": "https://x.com/AnthropicAI/status/123456789",
                        "category": "model",
                    }
                ]
                if digest
                else []
            )
        (self.leg_dir / f"{DATE}-twitter-ab-{HOUR}h-headlines.json").write_text(
            json.dumps(headlines)
        )
        exec_path = self.root / f"{self.leg}-execution.json"
        exec_path.write_text(make_execution_jsonl(**execution_kwargs))
        self.meta["execution_file"] = str(exec_path)

    def write_meta(self) -> Path:
        path = self.root / f"leg-{self.leg}.json"
        path.write_text(json.dumps(self.meta))
        return path


def run_collect(root: Path, metas, *, judge_dir=None, seed=7, input_json=None):
    argv = [
        "collect",
        "--date", DATE,
        "--hour", HOUR,
        "--timestamp", TS,
        "--run-id", RUN_ID,
        "--run-attempt", str(RUN_ATTEMPT),
        "--snapshot-sha", SNAPSHOT_SHA,
        "--manifest-sha", "c" * 64,
        "--normalized-prompt-sha", "d" * 64,
        "--blind-seed", str(seed),
        "--out", str(root / "metrics.json"),
    ]
    for meta in metas:
        argv += ["--leg-meta", str(meta)]
    if judge_dir is not None:
        argv += ["--judge-dir", str(judge_dir)]
    if input_json is not None:
        argv += ["--input-json", str(input_json)]
    with redirect_stdout(StringIO()):
        assert ab.main(argv) == 0
    return json.loads((root / "metrics.json").read_text())


class ExecutionParsingTest(unittest.TestCase):
    def test_jsonl_result_extraction(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "exec.json"
            path.write_text(make_execution_jsonl(num_turns=33, cost=2.5, denials=2))
            result = ab.extract_result(path)
        self.assertTrue(result["result_found"])
        self.assertFalse(result["is_error"])
        self.assertEqual(result["num_turns"], 33)
        self.assertEqual(result["total_cost_usd"], 2.5)
        self.assertEqual(result["permission_denials_count"], 2)
        self.assertEqual(result["observed_models"], ["claude-sonnet-5"])

    def test_json_array_form(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "exec.json"
            objects = [json.loads(line) for line in make_execution_jsonl().splitlines()]
            path.write_text(json.dumps(objects))
            result = ab.extract_result(path)
        self.assertTrue(result["result_found"])
        self.assertEqual(result["num_turns"], 21)

    def test_missing_file(self):
        result = ab.extract_result(Path("/nonexistent/exec.json"))
        self.assertFalse(result["result_found"])
        self.assertIsNone(result["num_turns"])


class ScrubTest(unittest.TestCase):
    def test_model_strings_scrubbed_outside_urls(self):
        text = (
            "Claude and GLM-5.2 disagree; Anthropic said so at "
            "https://x.com/AnthropicAI/status/1 and Z.ai replied."
        )
        scrubbed, hits = ab.scrub_text(text)
        self.assertNotIn("Claude", scrubbed)
        self.assertNotIn("GLM", scrubbed)
        self.assertNotIn("Z.ai", scrubbed)
        # URL preserved verbatim, including the provider-named handle.
        self.assertIn("https://x.com/AnthropicAI/status/1", scrubbed)
        self.assertGreaterEqual(hits, 4)

    def test_plain_words_not_scrubbed(self):
        scrubbed, hits = ab.scrub_text("The glamorous sonnets of markets.")
        self.assertEqual(scrubbed, "The glamorous sonnets of markets.")
        self.assertEqual(hits, 0)


class CollectTest(unittest.TestCase):
    def _two_good_legs(self, tmp: Path, judge=True, seed=7):
        leg_a = Fixture(tmp, "claude", "claude", "claude-sonnet-5")
        leg_a.write_artifacts()
        leg_b = Fixture(tmp, "zai-glm-5p2", "zai", "glm-5.2")
        leg_b.write_artifacts()
        input_json = tmp / "all.json"
        input_json.write_text(json.dumps({"accounts": {}, "searches": {}, "news": [],
                                          "meta": {"total_tweets": 321}}))
        return run_collect(
            tmp,
            [leg_a.write_meta(), leg_b.write_meta()],
            judge_dir=(tmp / "judge") if judge else None,
            seed=seed,
            input_json=input_json,
        )

    def test_clean_run_metrics(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            metrics = self._two_good_legs(tmp)
            claude = metrics["legs"]["claude"]
            self.assertEqual(claude["agent"]["num_turns"], 21)
            self.assertEqual(claude["artifacts"]["required_written"], "3/3")
            self.assertTrue(claude["format"]["valid"])
            self.assertEqual(claude["format"]["public_items"], 1)
            self.assertEqual(claude["format"]["counted_public_items"], 1)
            self.assertEqual(claude["format"]["story_cards"], 1)
            self.assertEqual(claude["format"]["headline_count"], 1)
            self.assertEqual(claude["backend"]["served_model"], "claude-sonnet-5")
            self.assertEqual(claude["wall_time_seconds"], 500)
            self.assertEqual(claude["flags"], [])
            zai = metrics["legs"]["zai-glm-5p2"]
            self.assertEqual(zai["backend"]["served_model"], "glm-5.2")
            self.assertFalse(metrics["contamination"]["contaminated"])
            self.assertFalse(metrics["contamination"]["sandbox_suspect"])
            self.assertEqual(metrics["input"]["total_tweets"], 321)

    def test_blinding_staged_and_recorded_only_in_metrics(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            metrics = self._two_good_legs(tmp, seed=7)
            blinding = metrics["blinding"]
            self.assertEqual(sorted(blinding["pass1"].values()),
                             ["claude", "zai-glm-5p2"])
            # pass2 is the position swap of pass1
            self.assertEqual(blinding["pass2"]["A"], blinding["pass1"]["B"])
            self.assertEqual(blinding["pass2"]["B"], blinding["pass1"]["A"])
            for pass_name in ("pass1", "pass2"):
                for letter in ("A", "B"):
                    doc = (tmp / "judge" / pass_name / f"{letter}.md").read_text()
                    # scrubbed: no model/provider identity in prose
                    self.assertNotIn("Anthropic ships", doc)
                    self.assertNotIn("Anthropic enabled", doc)
                    self.assertNotIn("ANTHROPIC SHIPS", doc)
                    self.assertIn("[redacted] ships", doc)
                    # no leg/lane names anywhere in the judge-visible file
                    self.assertNotIn("zai", doc.lower().replace("x.com", ""))
                    # URLs and @handles are shared-snapshot evidence — preserved
                    self.assertIn("https://x.com/AnthropicAI/status/123456789", doc)
                    self.assertIn("@AnthropicAI", doc)
            self.assertTrue((tmp / "judge" / "snapshot.json").exists())
            self.assertTrue(metrics["judge_staged"])

    def test_blinding_seed_deterministic(self):
        with tempfile.TemporaryDirectory() as a_str, tempfile.TemporaryDirectory() as b_str:
            m1 = self._two_good_legs(Path(a_str), seed=11)
            m2 = self._two_good_legs(Path(b_str), seed=11)
            self.assertEqual(m1["blinding"]["pass1"], m2["blinding"]["pass1"])

    def test_missing_leg_scored_mechanically_and_judge_skipped(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            leg_a = Fixture(tmp, "claude", "claude", "claude-sonnet-5")
            leg_a.write_artifacts()
            leg_b = Fixture(tmp, "zai-glm-5p2", "zai", "glm-5.2")
            leg_b.meta["outcome"] = "failure"
            leg_b.meta["post_sha"] = leg_b.meta["base_sha"]  # nothing committed
            # leg dir never created — the leg wrote nothing at all
            metrics = run_collect(
                tmp, [leg_a.write_meta(), leg_b.write_meta()], judge_dir=tmp / "judge"
            )
            zai = metrics["legs"]["zai-glm-5p2"]
            self.assertEqual(zai["artifacts"]["required_written"], "0/3")
            self.assertFalse(zai["format"]["valid"])
            self.assertIn("leg-failed", zai["flags"])
            self.assertIn("no-commit", zai["flags"])
            self.assertIsNone(metrics["blinding"])
            self.assertIn("no main digest", metrics["judge_skip_reason"])
            self.assertFalse((tmp / "judge" / "pass1").exists())

    def test_no_update_leg_is_format_valid_but_skips_judge(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            leg_a = Fixture(tmp, "claude", "claude", "claude-sonnet-5")
            leg_a.write_artifacts()
            leg_b = Fixture(tmp, "zai-glm-5p2", "zai", "glm-5.2")
            leg_b.write_artifacts(digest=False)
            metrics = run_collect(
                tmp, [leg_a.write_meta(), leg_b.write_meta()], judge_dir=tmp / "judge"
            )
            zai = metrics["legs"]["zai-glm-5p2"]
            self.assertTrue(zai["format"]["valid"])
            self.assertEqual(zai["format"]["status"], "no_update")
            self.assertIsNone(metrics["blinding"])

    def test_backend_mismatch_contaminates(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            leg_a = Fixture(tmp, "claude", "claude", "claude-sonnet-5")
            leg_a.write_artifacts()
            leg_b = Fixture(tmp, "zai-glm-5p2", "zai", "glm-5.2")
            leg_b.write_artifacts()
            # Z.ai leg silently served by claude — the exact failure the guard exists for.
            leg_b.meta["effective_backend"] = "claude"
            leg_b.meta["used_fallback"] = "true"
            metrics = run_collect(tmp, [leg_a.write_meta(), leg_b.write_meta()])
            self.assertIn("backend-mismatch", metrics["legs"]["zai-glm-5p2"]["flags"])
            self.assertTrue(metrics["contamination"]["contaminated"])
            self.assertIn("zai-glm-5p2:backend-mismatch",
                          metrics["contamination"]["reasons"])

    def test_input_mismatch_contaminates(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            leg_a = Fixture(tmp, "claude", "claude", "claude-sonnet-5")
            leg_a.write_artifacts()
            leg_a.meta["input_sha_post"] = "f" * 64  # mutated during the leg
            metrics = run_collect(tmp, [leg_a.write_meta()])
            self.assertIn("input-mutated", metrics["legs"]["claude"]["flags"])
            self.assertTrue(metrics["contamination"]["contaminated"])

    def test_denials_mark_sandbox_suspect_not_contaminated(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            leg_a = Fixture(tmp, "claude", "claude", "claude-sonnet-5")
            leg_a.write_artifacts(execution_kwargs={"denials": 3})
            metrics = run_collect(tmp, [leg_a.write_meta()])
            self.assertIn("sandbox-suspect", metrics["legs"]["claude"]["flags"])
            self.assertTrue(metrics["contamination"]["sandbox_suspect"])
            self.assertFalse(metrics["contamination"]["contaminated"])

    def test_unexpected_served_model_contaminates(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            leg_b = Fixture(tmp, "zai-glm-5p2", "zai", "glm-5.2")
            leg_b.write_artifacts(execution_kwargs={"models": ("claude-sonnet-5",)})
            metrics = run_collect(tmp, [leg_b.write_meta()])
            self.assertIn("expected-model-not-observed",
                          metrics["legs"]["zai-glm-5p2"]["flags"])
            self.assertTrue(metrics["contamination"]["contaminated"])


class FinalizeTest(unittest.TestCase):
    def _staged(self, tmp: Path, seed=7):
        leg_a = Fixture(tmp, "claude", "claude", "claude-sonnet-5")
        leg_a.write_artifacts()
        leg_b = Fixture(tmp, "zai-glm-5p2", "zai", "glm-5.2")
        leg_b.write_artifacts()
        return run_collect(
            tmp, [leg_a.write_meta(), leg_b.write_meta()], judge_dir=tmp / "judge",
            seed=seed,
        )

    @staticmethod
    def _verdict(preferred, a_overall=8, b_overall=6):
        return {
            "scores": {
                "A": {"coverage": 8, "faithfulness": 9, "headline_quality": 7,
                      "skepticism": 8, "format": 9, "overall": a_overall},
                "B": {"coverage": 6, "faithfulness": 7, "headline_quality": 6,
                      "skepticism": 6, "format": 7, "overall": b_overall},
            },
            "rationale": {"A": "tighter and better sourced", "B": "thinner coverage"},
            "preferred": preferred,
        }

    def _finalize(self, tmp: Path):
        argv = [
            "finalize",
            "--metrics", str(tmp / "metrics.json"),
            "--judge-dir", str(tmp / "judge"),
            "--judge-model", "claude-opus-4-8",
            "--out-verdict", str(tmp / "judge-verdict.json"),
        ]
        with redirect_stdout(StringIO()):
            self.assertEqual(ab.main(argv), 0)
        return (
            json.loads((tmp / "judge-verdict.json").read_text()),
            json.loads((tmp / "metrics.json").read_text()),
        )

    def test_agreement_after_position_swap(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            metrics = self._staged(tmp)
            mapping1 = metrics["blinding"]["pass1"]
            # Judge consistently prefers the SAME LEG in both passes: in
            # pass 2 the letters are swapped, so the preferred letter flips.
            preferred_leg = mapping1["A"]
            (tmp / "judge" / "verdict-1.json").write_text(json.dumps(self._verdict("A")))
            (tmp / "judge" / "verdict-2.json").write_text(
                json.dumps(self._verdict("B", a_overall=6, b_overall=8))
            )
            verdict, updated = self._finalize(tmp)
            self.assertEqual(verdict["final_preference"], preferred_leg)
            self.assertEqual(verdict["passes_parsed"], 2)
            self.assertEqual(verdict["per_leg"][preferred_leg]["overall_avg"], 8.0)
            self.assertEqual(updated["judge"]["final_preference"], preferred_leg)

    def test_position_bias_yields_split(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            self._staged(tmp)
            # A lazy judge that always prefers the first-listed brief:
            # after de-blinding, the two passes name different legs → split.
            (tmp / "judge" / "verdict-1.json").write_text(json.dumps(self._verdict("A")))
            (tmp / "judge" / "verdict-2.json").write_text(json.dumps(self._verdict("A")))
            verdict, _ = self._finalize(tmp)
            self.assertEqual(verdict["final_preference"], "split")

    def test_missing_verdicts_fail_open(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            self._staged(tmp)
            verdict, updated = self._finalize(tmp)
            self.assertEqual(verdict["passes_parsed"], 0)
            self.assertEqual(verdict["final_preference"], "none")
            self.assertEqual(updated["judge"]["passes_parsed"], 0)

    def test_fenced_verdict_still_parses(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            metrics = self._staged(tmp)
            fenced = "```json\n" + json.dumps(self._verdict("tie")) + "\n```"
            (tmp / "judge" / "verdict-1.json").write_text(fenced)
            verdict, _ = self._finalize(tmp)
            self.assertEqual(verdict["passes_parsed"], 1)
            self.assertEqual(verdict["final_preference"], "tie")
            self.assertIsNotNone(metrics["blinding"])


class ReportTest(unittest.TestCase):
    def test_report_renders_clean_and_contaminated(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            leg_a = Fixture(tmp, "claude", "claude", "claude-sonnet-5")
            leg_a.write_artifacts()
            leg_b = Fixture(tmp, "zai-glm-5p2", "zai", "glm-5.2")
            leg_b.write_artifacts()
            metrics = run_collect(
                tmp, [leg_a.write_meta(), leg_b.write_meta()], judge_dir=tmp / "judge"
            )
            (tmp / "judge" / "verdict-1.json").write_text(
                json.dumps(FinalizeTest._verdict("A"))
            )
            argv = [
                "finalize", "--metrics", str(tmp / "metrics.json"),
                "--judge-dir", str(tmp / "judge"),
                "--out-verdict", str(tmp / "judge-verdict.json"),
            ]
            with redirect_stdout(StringIO()):
                self.assertEqual(ab.main(argv), 0)
            out = tmp / "report.md"
            summary = tmp / "summary.txt"
            with redirect_stdout(StringIO()):
                self.assertEqual(
                    report.main([
                        "--metrics", str(tmp / "metrics.json"),
                        "--out", str(out),
                        "--summary-out", str(summary),
                    ]),
                    0,
                )
            text = out.read_text()
            self.assertIn("Parity guards: clean", text)
            self.assertIn("| `claude` (claude-sonnet-5) |".replace("| ", "").split()[0], text)
            self.assertIn("claude-sonnet-5", text)
            self.assertIn("glm-5.2", text)
            self.assertIn("final preference", text)
            line = summary.read_text().strip()
            self.assertTrue(line.startswith(f"AB {DATE}:"))
            self.assertIn("clean", line)

            # contaminated variant
            metrics = json.loads((tmp / "metrics.json").read_text())
            metrics["contamination"] = {
                "contaminated": True,
                "reasons": ["zai-glm-5p2:backend-mismatch"],
                "sandbox_suspect": False,
            }
            (tmp / "metrics.json").write_text(json.dumps(metrics))
            with redirect_stdout(StringIO()):
                self.assertEqual(
                    report.main(["--metrics", str(tmp / "metrics.json"), "--out", str(out)]),
                    0,
                )
            text = out.read_text()
            self.assertIn("CONTAMINATED RUN", text)
            self.assertIn("zai-glm-5p2:backend-mismatch", text)

    def test_report_handles_missing_judge_and_missing_leg(self):
        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            leg_a = Fixture(tmp, "claude", "claude", "claude-sonnet-5")
            leg_a.write_artifacts()
            metrics_path = tmp / "metrics.json"
            run_collect(tmp, [leg_a.write_meta()])
            out = tmp / "report.md"
            with redirect_stdout(StringIO()):
                self.assertEqual(
                    report.main(["--metrics", str(metrics_path), "--out", str(out)]), 0
                )
            text = out.read_text()
            self.assertIn("Judge did not score this run", text)


if __name__ == "__main__":
    unittest.main()
