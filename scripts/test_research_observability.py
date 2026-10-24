"""Offline behavioral checks for the capture, export and RSI evidence boundary."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
import subprocess
import sys
import urllib.error
import unittest
from unittest.mock import patch

import yaml

import langfuse_research as lf
import research_trace as capture

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / "data/agent-backends.json").read_text())
MODEL = REGISTRY["fallback"]["native_model"]
SECRET = "sk-lf-never-export-this-sentinel"


def transcript():
    return [
        {"type": "assistant", "message": {"id": "m1", "model": MODEL,
         "usage": {"input_tokens": 15, "output_tokens": 2, "cache_read_input_tokens": 10},
         "content": [{"type": "thinking", "thinking": SECRET},
                     {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": SECRET}}]}},
        {"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "t1", "is_error": True, "content": SECRET}]}},
        {"type": "result", "is_error": True, "result": SECRET, "duration_ms": 5000,
         "num_turns": 1, "total_cost_usd": 0.12},
    ]


def job():
    return {"name": "generative-research", "started_at": "2026-10-24T00:00:00Z",
            "completed_at": "2026-10-24T00:01:00Z", "conclusion": "success",
            "steps": [{"name": name, "number": i + 1, "started_at": "2026-10-24T00:00:01Z",
                       "completed_at": "2026-10-24T00:00:50Z", "conclusion": "success"}
                      for i, name in enumerate(lf.STAGES.values())]}


def build(directory, **kwargs):
    return lf.build_trace(Path(directory), job(), REGISTRY, repository="guzus/ai-research-arm",
                          run_id="123", run_attempt=kwargs.pop("run_attempt", "1"), source_sha="a" * 40,
                          environment="evaluation", **kwargs)


def attributes(span):
    return {a["key"]: next(iter(a["value"].values())) for a in span["attributes"]}


class CaptureTests(unittest.TestCase):
    def test_real_array_and_jsonl_shape_strip_all_content(self):
        for text in [json.dumps(transcript(), indent=2), "\n".join(map(json.dumps, transcript()))]:
            with self.subTest(text=text[:1]), tempfile.TemporaryDirectory() as td:
                path = Path(td) / "execution.json"
                path.write_text(text)
                result = capture.capture(str(path), capture.known_identifiers(REGISTRY))
                self.assertNotIn(SECRET, json.dumps(result))
                self.assertEqual(result["coverage"], "structured")
                self.assertEqual(result["events"][0]["model"], MODEL)
                self.assertEqual(result["events"][1]["outcome"], "failure")
                self.assertEqual(result["result"]["runtime_estimated_cost_usd"], 0.12)

    def test_streaming_generation_updates_are_not_double_counted(self):
        original = transcript()[0]
        update = json.loads(json.dumps(original))
        update["message"]["usage"]["output_tokens"] = 8
        events = capture.normalize([original, update], {MODEL})["events"]
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["usage"]["output_tokens"], 8)

    def test_attempt_copies_survive_reused_transcript_path(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "execution.json"
            path.write_text(json.dumps(transcript()))
            first = capture.capture(str(path), {MODEL})
            capture.write_json(Path(td) / "gen-claude.json", first)
            path.write_text(json.dumps([{"type": "result", "is_error": False}]))
            second = capture.capture(str(path), {MODEL})
            self.assertNotEqual(first["transcript_sha256"], second["transcript_sha256"])
            self.assertTrue(json.loads((Path(td) / "gen-claude.json").read_text())["result"]["is_error"])

    def test_missing_malformed_and_symlink_are_explicit(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "execution.json"
            self.assertEqual(capture.capture("", set())["coverage"], "missing")
            self.assertEqual(capture.capture(str(path), set())["coverage"], "unreadable")
            path.write_text("{truncated")
            self.assertEqual(capture.capture(str(path), set())["coverage"], "unrecognized")
            link = Path(td) / "link.json"
            link.symlink_to(path)
            self.assertEqual(capture.capture(str(link), set())["coverage"], "unreadable")

    def test_unknown_labels_and_nonfinite_numbers_do_not_escape(self):
        objects = transcript()
        objects[0]["message"]["model"] = SECRET
        objects[0]["message"]["usage"] = {"input_tokens": float("inf"), "output_tokens": -1}
        objects[0]["message"]["content"][1]["name"] = SECRET
        result = capture.normalize(objects, {MODEL})
        self.assertNotIn(SECRET, json.dumps(result))
        self.assertEqual(result["events"][0]["usage"], {})
        self.assertEqual(result["events"][0]["model"], "unknown")
        self.assertEqual(result["events"][1]["name"], "other")

    def test_malformed_event_types_and_huge_integers_are_bounded(self):
        self.assertIsNone(capture.number(10 ** 400))
        self.assertEqual(capture.normalize([{"type": []}], set())["coverage"], "unrecognized")
        result = capture.summary({}, REGISTRY)
        self.assertIsNone(result["published"])
        self.assertIsNone(result["used_fallback"])


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        record = capture.normalize(transcript(), {MODEL})
        capture.write_json(self.directory / "gen-claude.json", {"schema_version": 1, **record})
        capture.write_json(self.directory / "summary.json", {
            "schema_version": 1, "requested_backend": "glm-5p2", "effective_backend": "claude",
            "used_fallback": True, "published": True, "has_article": True,
            "outcomes": {"gen-claude": "failure", "gen-claude-retry": "success", "quality": "success",
                         "verifier-audit": "failure", "methodology": "skipped", "push": "success"}})

    def test_spans_parentage_missing_timing_and_fallback(self):
        trace = build(self.directory)
        root = trace["spans"][0]
        root_meta = attributes(root)
        self.assertEqual(root_meta["langfuse.trace.metadata.requested_backend"], '"glm-5p2"')
        self.assertEqual(root_meta["langfuse.trace.metadata.effective_backend"], '"claude"')
        self.assertEqual(root_meta["langfuse.trace.metadata.used_fallback"], "true")
        self.assertNotIn("langfuse.observation.model.name", root_meta)
        ids = {s["spanId"] for s in trace["spans"]}
        for span in trace["spans"][1:]:
            self.assertIn(span["parentSpanId"], ids)
            self.assertEqual(span["traceId"], trace["trace_id"])
        generation = next(s for s in trace["spans"] if s["name"] == "model generation")
        self.assertEqual(generation["startTimeUnixNano"], generation["endTimeUnixNano"])
        self.assertEqual(attributes(generation)["langfuse.observation.metadata.timing"], '"not-reported"')
        tool = next(s for s in trace["spans"] if s["name"] == "Bash")
        self.assertEqual(tool["parentSpanId"], generation["spanId"])
        self.assertEqual(tool["status"]["code"], 2)
        cursor = next(s for s in trace["spans"] if s["name"] == lf.STAGES["gen-cursor"])
        self.assertEqual(attributes(cursor)["langfuse.observation.metadata.coverage"], '"not-instrumented"')

    def test_unknown_gate_is_not_a_passing_score_and_ids_are_stable(self):
        first, second = build(self.directory), build(self.directory)
        self.assertEqual(first, second)
        self.assertNotEqual(first["trace_id"], build(self.directory, run_attempt="2")["trace_id"])
        scores = {s["name"]: s["value"] for s in first["scores"]}
        self.assertEqual(scores["research.verifier-audit"], 0)
        self.assertNotIn("research.methodology", scores)

    def test_untrusted_artifact_cannot_forward_extra_fields(self):
        capture.write_json(self.directory / "gen-claude.json", {
            "schema_version": 1, "coverage": SECRET, "result": {"duration_ms": SECRET}, "secret": SECRET,
            "events": [{"kind": "generation", "model": SECRET, "usage": {"input_tokens": SECRET}, "input": SECRET},
                       {"kind": "tool", "name": SECRET, "outcome": "failure", "output": SECRET}]})
        trace = build(self.directory)
        self.assertNotIn(SECRET, json.dumps(trace))

    def test_absent_bundle_still_records_failure_without_fake_quality(self):
        with tempfile.TemporaryDirectory() as empty:
            trace = build(empty)
            self.assertTrue(trace["spans"])
            self.assertEqual(trace["scores"], [])
            self.assertEqual(attributes(trace["spans"][0])["langfuse.trace.metadata.summary_available"], "false")
            self.assertEqual(attributes(trace["spans"][0])["langfuse.trace.metadata.published"], "null")

    def test_capped_diagnostics_and_unknown_usage_reach_root(self):
        capture.write_json(self.directory / "gen-claude.json", {
            "schema_version": 1, "coverage": "structured", "events_capped": True,
            "events": [{"kind": "generation", "model": MODEL, "usage": {"output_tokens": 10 ** 400}},
                       {"kind": "tool", "name": "Read", "outcome": "failure"}]})
        trace = build(self.directory)
        attempts = json.loads(attributes(trace["spans"][0])["langfuse.observation.metadata.attempts"])
        first = next(a for a in attempts if a["attempt"] == "gen-claude")
        self.assertTrue(first["events_capped"])
        self.assertEqual(first["captured_event_count"], 2)
        self.assertIsNone(first["reported_tokens"])
        self.assertEqual(first["tool_outcomes"]["failure"], 1)
        capture.write_json(self.directory / "summary.json", {"schema_version": 1})
        self.assertEqual(build(self.directory)["scores"], [])

    def test_score_batch_and_replay_identity(self):
        class Client:
            def __init__(self): self.calls = []
            def request(self, path, payload):
                self.calls.append((path, payload))
                return {}
        client = Client()
        trace = build(self.directory)
        lf.export(client, trace)
        path, payload = client.calls[-1]
        self.assertEqual(path, "/api/public/scores")
        self.assertIsInstance(payload, list)
        self.assertEqual(payload[0]["timestamp"], job()["completed_at"])
        self.assertEqual(payload[0]["environment"], "evaluation")

    def test_partial_ingestion_is_a_detectable_failure(self):
        class Client:
            def request(self, *args):
                return {"partialSuccess": {"rejectedSpans": "1"}}
        with self.assertRaises(RuntimeError):
            lf.export(Client(), build(self.directory))

    def test_live_transport_requires_https_and_refuses_redirects(self):
        with patch.dict(os.environ, {"LANGFUSE_BASE_URL": "http://example.com", "LANGFUSE_PUBLIC_KEY": "pk", "LANGFUSE_SECRET_KEY": "sk"}):
            with self.assertRaises(ValueError):
                lf.Langfuse()
        with self.assertRaises(ValueError):
            lf.NoRedirect().redirect_request(None, None, 302, "", {}, "https://evil.invalid")

    def test_network_failure_is_bounded_and_does_not_echo_secrets(self):
        with patch.dict(os.environ, {"LANGFUSE_BASE_URL": "https://example.com", "LANGFUSE_PUBLIC_KEY": "pk", "LANGFUSE_SECRET_KEY": SECRET}):
            client = lf.Langfuse()
        with patch.object(client.opener, "open", side_effect=urllib.error.URLError(SECRET)) as request, patch.object(lf.time, "sleep"):
            with self.assertRaisesRegex(RuntimeError, "^Langfuse network error$"):
                client.request("/api/public/otel/v1/traces", {})
            self.assertEqual(request.call_count, 2)

    def test_missing_raw_outcome_does_not_infer_success_from_continue_on_error(self):
        (self.directory / "summary.json").unlink()
        trace = build(self.directory)
        attempt = next(s for s in trace["spans"] if s["name"] == capture.ATTEMPTS["gen-claude"])
        self.assertEqual(attributes(attempt)["langfuse.observation.metadata.outcome"], '"unknown"')
        self.assertEqual(attributes(attempt)["langfuse.observation.metadata.github_step_conclusion"], '"success"')

    def test_missing_article_failure_is_visible_to_rsi_without_transcript(self):
        actual = job()
        actual["conclusion"] = "failure"
        next(s for s in actual["steps"] if s["name"] == lf.STAGES["no-article-claude"])["conclusion"] = "failure"
        (self.directory / "summary.json").unlink()
        trace = lf.build_trace(self.directory, actual, REGISTRY, repository="guzus/ai-research-arm",
                               run_id="123", run_attempt="1", source_sha="a" * 40, environment="production")
        failures = json.loads(attributes(trace["spans"][0])["langfuse.observation.metadata.failed_stages"])
        self.assertIn("no-article-claude", failures)
        gate = next(s for s in trace["spans"] if s["name"] == lf.STAGES["no-article-claude"])
        self.assertEqual(gate["status"]["code"], 2)

    def test_documented_cli_round_trip_without_network_or_keys(self):
        raw = self.directory / "raw.json"
        raw.write_text(json.dumps(transcript()))
        bundle = self.directory / "bundle"
        environment = {k: v for k, v in os.environ.items() if not k.startswith("LANGFUSE_")}
        environment.update(EXECUTION_FILE=str(raw), GITHUB_REPOSITORY="guzus/ai-research-arm",
                           GITHUB_RUN_ID="123", GITHUB_RUN_ATTEMPT="1", RESEARCH_SOURCE_SHA="a" * 40)
        captured = subprocess.run([sys.executable, "scripts/research_trace.py", "capture", "--attempt", "gen-claude", "--output-dir", str(bundle)],
                                  cwd=ROOT, env=environment, capture_output=True, text=True)
        self.assertEqual(captured.returncode, 0, captured.stderr)
        jobs = self.directory / "jobs.json"
        jobs.write_text(json.dumps({"jobs": [job()]}))
        preview = self.directory / "preview.json"
        exported = subprocess.run([sys.executable, "scripts/langfuse_research.py", "export", "--bundle-dir", str(bundle),
                                   "--jobs-file", str(jobs), "--preview", str(preview)], cwd=ROOT, env=environment, capture_output=True, text=True)
        self.assertEqual(exported.returncode, 0, exported.stderr)
        result = json.loads(preview.read_text())
        self.assertTrue(result["spans"])
        self.assertNotIn(SECRET, preview.read_text())


class WorkflowTests(unittest.TestCase):
    def test_all_attempts_captured_before_next_model_and_reporting_is_isolated(self):
        flow = yaml.safe_load((ROOT / ".github/workflows/generative-research.yml").read_text())
        steps = flow["jobs"]["generative-research"]["steps"]
        captures = {step["name"]: i for i, step in enumerate(steps) if step["name"].startswith("Capture sanitized")}
        for i, step in enumerate(steps):
            key = step.get("id")
            if key in capture.ATTEMPTS:
                self.assertEqual(step["name"], capture.ATTEMPTS[key])
                self.assertEqual(captures[f"Capture sanitized trace ({key})"], i + 1)
                self.assertTrue(steps[i + 1]["continue-on-error"])
        self.assertNotIn("LANGFUSE_SECRET_KEY", json.dumps(steps))
        reporter = flow["jobs"]["langfuse-observability"]
        self.assertEqual(reporter["runs-on"], "ubuntu-latest")
        self.assertTrue(reporter["continue-on-error"])
        self.assertEqual(reporter["steps"][0]["with"]["ref"], "${{ github.workflow_sha }}")
        self.assertEqual(reporter["permissions"], {"contents": "read", "actions": "read"})
        for key, name in lf.STAGES.items():
            self.assertIn(name, {s["name"] for s in steps}, key)

    def test_rsi_agent_receives_only_evidence_no_langfuse_credentials(self):
        flow = yaml.safe_load((ROOT / ".github/workflows/daily-improve.yml").read_text())
        agent = flow["jobs"]["self-improve"]
        self.assertNotIn("LANGFUSE_SECRET_KEY", json.dumps(agent))
        self.assertEqual(agent["needs"], "langfuse-evidence")


class EvidenceTests(unittest.TestCase):
    def test_query_filters_production_expands_diagnostics_and_stops_pagination(self):
        class Client:
            def __init__(self): self.paths = []
            def request(self, path):
                self.paths.append(path)
                return {"data": [
                    {"name": lf.TRACE_NAME, "traceId": "smoke", "environment": "smoke-test"},
                    {"name": lf.TRACE_NAME, "traceId": "prod", "environment": "production",
                     "metadata": {"attempts": [{"coverage": "missing"}], "input": SECRET}}
                ], "meta": {"cursor": "next"}}
        client = Client()
        evidence = lf.evidence(client, 7)
        self.assertEqual(len(client.paths), 3)
        self.assertIn("environment=production", client.paths[0])
        self.assertIn("expandMetadata=outcomes%2Cattempts", client.paths[0])
        self.assertTrue(evidence["truncated"])
        self.assertTrue(all(row["trace_id"] == "prod" for row in evidence["runs"]))
        self.assertEqual(evidence["runs"][0]["attempts"], [{"coverage": "missing"}])
        self.assertNotIn(SECRET, json.dumps(evidence))

    def test_unavailable_writes_explicit_status_and_nonzero_exit(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {"LANGFUSE_BASE_URL": ""}):
            output = Path(td) / "evidence.json"
            with patch("sys.argv", ["langfuse_research.py", "evidence", "--output", str(output)]):
                self.assertEqual(lf.main(), 1)
            self.assertEqual(json.loads(output.read_text())["status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
