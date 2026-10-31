#!/usr/bin/env python3
"""Tests for scripts/aradio_run_alert.py: one alert per outage, one on recovery."""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

import aradio_run_alert as ara

ROOT = Path(__file__).resolve().parent.parent
SINCE = "2026-10-31T08:53:00Z"
TODAY = "2026-10-31"


def env(**values: str) -> dict[str, str]:
    base = {"JOB_STATUS": "success", "SINCE": SINCE, "GATE_REASON": "no new material",
            "GITHUB_RUN_ID": "900"}
    base.update(values)
    return base


def stuck(stage_env: str, **values: str) -> dict[str, str]:
    return env(**{"JOB_STATUS": "failure", "GATE_REASON": "1 new priority item(s)",
                  stage_env: "failure", **values})


def published(**values: str) -> dict[str, str]:
    return env(EDITOR="success", VALIDATE="success", WRITER="success", PUSH="success",
               GATE_REASON="138 min since the last editor run", **values)


def run(run_id: int, created_at: str, conclusion: str = "failure") -> dict:
    return {"id": run_id, "created_at": created_at, "conclusion": conclusion}


def no_runs(since):
    raise AssertionError("a run that did not publish must not query GitHub")


class OutageTest(unittest.TestCase):
    def test_a_healthy_run_keeps_the_defaults(self):
        shaped = ara.shape(env(), no_runs, TODAY)
        self.assertEqual({"title": "", "text": "Gate: no new material", "priority": "",
                          "tags": "aradio", "idempotency_key": ""}, shaped)

    def test_every_failing_hour_of_one_outage_shares_one_key(self):
        keys = {ara.shape(stuck("EDITOR", GITHUB_RUN_ID=str(run_id), GATE_REASON=reason),
                          no_runs, TODAY)["idempotency_key"]
                for run_id, reason in ((901, "1 new priority item(s)"),
                                       (902, "171 min since the last editor run"),
                                       (903, "forced by workflow_dispatch"))}
        self.assertEqual({f"aradio-stuck-editor-{SINCE}-{TODAY}"}, keys)
        shaped = ara.shape(stuck("EDITOR"), no_runs, TODAY)
        self.assertEqual(("Aradio stuck: editor failing", "5", "aradio,outage"),
                         (shaped["title"], shaped["priority"], shaped["tags"]))
        self.assertIn(f"Nothing has published since {SINCE}", shaped["text"])
        self.assertTrue(shaped["text"].startswith("Gate: 1 new priority item(s)\n"))

    def test_a_long_outage_re_alerts_once_a_day(self):
        # Hooker keeps a key whose every delivery failed, so a key that never
        # rolled over would let one lost delivery silence the whole outage.
        first = ara.shape(stuck("EDITOR"), no_runs, TODAY)["idempotency_key"]
        next_day = ara.shape(stuck("EDITOR"), no_runs, "2026-11-01")["idempotency_key"]
        self.assertNotEqual(first, next_day)
        self.assertEqual(f"aradio-stuck-editor-{SINCE}-2026-11-01", next_day)

    def test_a_new_cause_or_a_new_outage_alerts_again(self):
        editor = ara.shape(stuck("EDITOR"), no_runs, TODAY)["idempotency_key"]
        validation = ara.shape(stuck("VALIDATE", EDITOR="success"), no_runs, TODAY)
        later = ara.shape(stuck("EDITOR", SINCE="2026-10-31T12:50:00Z"), no_runs, TODAY)
        self.assertEqual(f"aradio-stuck-validation-{SINCE}-{TODAY}",
                         validation["idempotency_key"])
        self.assertEqual(3, len({editor, validation["idempotency_key"],
                                 later["idempotency_key"]}))

    def test_the_first_failed_stage_names_the_cause(self):
        cases = {
            "setup": dict(CHECKOUT="failure"),
            "gate": dict(CHECKOUT="success", DEPS="success", INBOX="failure"),
            "editor": dict(INBOX="success", EDITOR="failure"),
            "validation": dict(EDITOR="success", VALIDATE="failure"),
            "publish": dict(VALIDATE="success", WRITER="success", REQUIRE_OUTPUT="success",
                            DIFF_SCOPE="success", PUSH="failure"),
        }
        for stage, outcomes in cases.items():
            with self.subTest(stage):
                self.assertEqual(stage, ara.failed_stage(outcomes))
        # The ref guard or the quarantine failed: no stage outcome at all.
        self.assertEqual("setup", ara.failed_stage({}))

    def test_a_cancelled_run_that_published_nothing_is_stuck_too(self):
        shaped = ara.shape(env(JOB_STATUS="cancelled", EDITOR="failure"), no_runs, TODAY)
        self.assertEqual(f"aradio-stuck-editor-{SINCE}-{TODAY}", shaped["idempotency_key"])

    def test_before_the_first_bulletin_and_with_an_unknown_cursor(self):
        never = ara.shape(stuck("EDITOR", SINCE="never"), no_runs, TODAY)
        self.assertEqual(f"aradio-stuck-editor-never-{TODAY}", never["idempotency_key"])
        self.assertIn("since the station's first bulletin", never["text"])
        # The gate never read the cursor: at most one alert a day.
        unknown = ara.shape(env(JOB_STATUS="failure", SINCE="", GATE_REASON=""), no_runs, TODAY)
        self.assertEqual(f"aradio-stuck-setup-unknown-{TODAY}", unknown["idempotency_key"])
        self.assertIn("since an unknown time", unknown["text"])


class RecoveryTest(unittest.TestCase):
    def test_the_first_publication_after_failures_reports_the_recovery(self):
        seen = []

        def runs(since):
            seen.append(since)
            return [run(950, "2026-10-31T11:50:12Z"), run(949, "2026-10-31T10:50:09Z"),
                    run(948, "2026-10-31T09:50:11Z", "success")]

        shaped = ara.shape(published(), runs, TODAY)
        self.assertEqual([ara.parse_time(SINCE)], seen)
        self.assertEqual(("✅ Aradio recovered", "3", "aradio,recovered",
                          f"aradio-recovered-{SINCE}"),
                         (shaped["title"], shaped["priority"], shaped["tags"],
                          shaped["idempotency_key"]))
        self.assertIn(f"after 2 failed run(s) since {SINCE}", shaped["text"])

    def test_no_recovery_without_a_later_failure(self):
        runs = [
            # The run that published SINCE: created in the same minute, then
            # failed on audio after publishing.
            run(940, "2026-10-31T08:53:32Z"),
            run(900, "2026-10-31T11:50:00Z"),            # this run
            run(951, "2026-10-31T10:50:00Z", "cancelled"),  # superseded pending run
            run(952, "2026-10-31T09:50:00Z", "success"),
        ]
        shaped = ara.shape(published(), lambda since: runs, TODAY)
        self.assertEqual(("", "", ""), (shaped["title"], shaped["priority"],
                                        shaped["idempotency_key"]))
        self.assertNotIn("Published again", shaped["text"])

    def test_a_recovery_that_misses_its_audio_keeps_the_audio_alert(self):
        shaped = ara.shape(published(JOB_STATUS="failure"),
                           lambda since: [run(950, "2026-10-31T11:50:12Z")], TODAY)
        self.assertEqual(("", "", ""), (shaped["title"], shaped["priority"],
                                        shaped["idempotency_key"]))
        self.assertIn("Published again after 1 failed run(s)", shaped["text"])

    def test_the_first_bulletin_counts_every_earlier_failure(self):
        shaped = ara.shape(published(SINCE="never"),
                           lambda since: [run(1, "2026-10-30T09:50:00Z")], TODAY)
        self.assertEqual("aradio-recovered-never", shaped["idempotency_key"])
        self.assertIn("since the first bulletin", shaped["text"])

    def test_a_failed_lookup_never_blocks_the_telemetry(self):
        def broken(since):
            raise subprocess.CalledProcessError(1, ["gh"])

        with contextlib.redirect_stderr(io.StringIO()) as err:
            shaped = ara.shape(published(), broken, TODAY)
        self.assertEqual("", shaped["idempotency_key"])
        self.assertIn("::warning::", err.getvalue())
        # Without the gate's stamp there is nothing to compare against.
        self.assertEqual("", ara.shape(published(SINCE=""), no_runs, TODAY)["idempotency_key"])

    def test_query_lists_only_runs_after_the_publication(self):
        completed = subprocess.CompletedProcess([], 0, stdout=json.dumps(
            {"workflow_runs": [run(1, "2026-10-31T10:50:00Z"), "junk"]}))
        with mock.patch.object(ara.subprocess, "run", return_value=completed) as call:
            runs = ara.query_runs("o/r", ara.parse_time(SINCE))
        self.assertEqual([run(1, "2026-10-31T10:50:00Z")], runs)
        args = call.call_args.args[0]
        self.assertEqual(["gh", "api", "-X", "GET",
                          "repos/o/r/actions/workflows/aradio.yml/runs"], args[:5])
        self.assertIn("created=>2026-10-31T08:54:00Z", args)
        self.assertIn("branch=main", args)
        with mock.patch.object(ara.subprocess, "run", return_value=completed) as call:
            ara.query_runs("o/r", None)
        self.assertFalse(any(arg.startswith("created=") for arg in call.call_args.args[0]))
        bad = subprocess.CompletedProcess([], 0, stdout="[]")
        with mock.patch.object(ara.subprocess, "run", return_value=bad), \
                self.assertRaises(ValueError):
            ara.query_runs("o/r", None)


class OutputTest(unittest.TestCase):
    def test_outputs_round_trip_through_github_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out"
            ara.write_outputs(str(path), {"title": "t", "text": "a\nb", "priority": ""})
            text = path.read_text(encoding="utf-8")
        parsed, lines = {}, iter(text.splitlines())
        for line in lines:
            name, delimiter = line.split("<<", 1)
            value = []
            for inner in lines:
                if inner == delimiter:
                    break
                value.append(inner)
            parsed[name] = "\n".join(value)
        self.assertEqual({"title": "t", "text": "a\nb", "priority": ""}, parsed)

    def test_main_reads_the_workflow_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            with mock.patch.dict(os.environ, stuck("EDITOR", GITHUB_REPOSITORY="o/r"), clear=True), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, ara.main(["--github-output", str(out)]))
            self.assertIn(f"aradio-stuck-editor-{SINCE}", out.read_text(encoding="utf-8"))


FAKE_CURL = """#!{python}
import json, os, sys
with open(os.environ["FAKE_CURL_LOG"], "a", encoding="utf-8") as handle:
    handle.write(json.dumps(sys.argv[1:]) + "\\n")
"""


class WorkflowTest(unittest.TestCase):
    def setUp(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/aradio.yml").read_text())
        self.job = workflow["jobs"]["aradio"]
        self.steps = {step.get("id") or step.get("name"): step for step in self.job["steps"]}

    def test_every_stage_outcome_reaches_the_script(self):
        shape_step = self.steps["run_alert"]
        self.assertEqual("always()", shape_step["if"])
        self.assertTrue(shape_step.get("continue-on-error"))
        names = {name for _, stage in ara.STAGES for name in stage}
        for name in names:
            step_id = shape_step["env"][name].removeprefix("${{ steps.").split(".")[0]
            self.assertIn(step_id, self.steps, name)
            self.assertEqual(f"${{{{ steps.{step_id}.outcome }}}}", shape_step["env"][name])
        self.assertEqual("${{ steps.inbox.outputs.since }}", shape_step["env"]["SINCE"])
        self.assertEqual("read", self.job["permissions"]["actions"])
        names_in_order = [step.get("name") for step in self.job["steps"]]
        self.assertEqual(names_in_order.index("Publish Hooker workflow telemetry") - 1,
                         names_in_order.index("Shape the run's Hooker event"))
        telemetry = self.steps["Publish Hooker workflow telemetry"]["with"]
        self.assertEqual("${{ steps.run_alert.outputs.idempotency_key }}",
                         telemetry["idempotency-key"])
        self.assertIn("steps.run_alert.outputs.priority", telemetry["priority"])

    def run_telemetry_action(self, key: str) -> list[str]:
        action = yaml.safe_load((ROOT / ".github/actions/hooker-telemetry/action.yml").read_text())
        self.assertIn("idempotency-key", action["inputs"])
        step = action["runs"]["steps"][0]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "bin").mkdir()
            curl = tmp_path / "bin" / "curl"
            curl.write_text(FAKE_CURL.format(python=sys.executable), encoding="utf-8")
            curl.chmod(0o755)
            run_env = {"PATH": f"{tmp_path / 'bin'}{os.pathsep}{os.environ['PATH']}",
                       "FAKE_CURL_LOG": str(tmp_path / "curl.log"), "RUNNER_TEMP": tmp,
                       "HOOKER_TOKEN": "t", "HOOKER_URL": "https://hooker.test",
                       "HOOKER_TOPIC": "ara-telemetry", "TELEMETRY_STATUS": "failure",
                       "TELEMETRY_TITLE": "", "TELEMETRY_TEXT": "", "TELEMETRY_TAGS": "",
                       "TELEMETRY_PRIORITY": "", "TELEMETRY_IDEMPOTENCY_KEY": key,
                       "GITHUB_RUN_ID": "77", "GITHUB_RUN_ATTEMPT": "1", "GITHUB_JOB": "aradio"}
            result = subprocess.run(["bash", "-c", step["run"]], env=run_env, text=True,
                                    capture_output=True, check=False)
            self.assertEqual(0, result.returncode, result.stderr)
            return json.loads((tmp_path / "curl.log").read_text().splitlines()[0])

    def test_telemetry_action_sends_the_given_key_or_its_per_run_default(self):
        self.assertIn(f"Idempotency-Key: aradio-stuck-editor-{SINCE}",
                      self.run_telemetry_action(f"aradio-stuck-editor-{SINCE}"))
        self.assertIn("Idempotency-Key: ara-telemetry-77-1-aradio-failure",
                      self.run_telemetry_action(""))


if __name__ == "__main__":
    unittest.main()
