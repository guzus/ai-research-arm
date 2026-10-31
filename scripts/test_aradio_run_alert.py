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
from datetime import datetime, timezone
from typing import Callable
from unittest import mock

import yaml

import aradio_run_alert as ara

ROOT = Path(__file__).resolve().parent.parent
SINCE = "2026-10-31T08:53:00Z"
NOW = datetime(2026, 10, 31, 14, 20, tzinfo=timezone.utc)
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


def run(run_id: int, created_at: str, conclusion: str | None = "failure",
        updated_at: str | None = None, started_at: str | None = None) -> dict:
    record = {"id": run_id, "created_at": created_at, "conclusion": conclusion}
    if updated_at:
        record["updated_at"] = updated_at
    if started_at:  # a re-run attempt: queued then, though created long before
        record["run_started_at"] = started_at
    return record


def no_runs():
    raise AssertionError("a run that did not publish must not query GitHub")


def no_jobs(run_id):
    raise AssertionError(f"run {run_id}'s jobs must not be looked up")


def forced(run_id: int, created_at: str, conclusion: str = "cancelled",
           updated_at: str | None = None) -> dict:
    return {"id": run_id, "created_at": created_at, "conclusion": conclusion,
            "display_title": ara.FORCED_TITLE, "updated_at": updated_at or created_at}


def jobs(*steps: tuple[str, str]) -> list[dict]:
    """One job that got a runner, with these (name, conclusion) steps."""
    return [{"runner_name": "gunux-guzus-ai-research-arm",
             "steps": [{"name": name, "conclusion": conclusion} for name, conclusion in steps]}]


# What the jobs API returns for each kind of run (shapes from this repo's runs).
EDITOR_FAILED = jobs(("Set up job", "success"), (ara.EDITOR_STEP, "failure"))
# A job past timeout-minutes: the step then running ends cancelled, and so does the run.
EDITOR_HUNG = jobs(("Set up job", "success"), (ara.EDITOR_STEP, "cancelled"))
SETUP_FAILED = jobs(("Set up job", "success"), ("Checkout repository", "failure"),
                    (ara.EDITOR_STEP, "skipped"))
PUBLISHED = jobs(("Set up job", "success"), (ara.EDITOR_STEP, "success"))
NEVER_STARTED: list[dict] = []  # cancelled while it waited in the queue
WAITED_FOR_A_RUNNER = [{"runner_name": "", "steps": [], "conclusion": "cancelled"}]


def jobs_of(by_id: dict, asked: list) -> Callable[[object], list[dict]]:
    def jobs_fn(run_id):
        asked.append(run_id)
        return by_id[run_id]
    return jobs_fn


class OutageTest(unittest.TestCase):
    def test_a_gate_stop_reports_once_an_hour(self):
        # Every lane that finishes wakes the station; one stop event an hour.
        shaped = ara.shape(env(), no_runs, no_jobs, NOW)
        self.assertEqual({"title": "", "text": "Gate: no new material", "priority": "",
                          "tags": "aradio", "idempotency_key": "aradio-stop-2026-10-31T14"},
                         shaped)
        later = ara.shape(env(GATE_REASON="routine material waits"), no_runs, no_jobs,
                          NOW.replace(minute=55))
        self.assertEqual(shaped["idempotency_key"], later["idempotency_key"])
        self.assertEqual("aradio-stop-2026-10-31T15", ara.shape(
            env(), no_runs, no_jobs, NOW.replace(hour=15))["idempotency_key"])

    def test_every_failing_hour_of_one_outage_shares_one_key(self):
        keys = {ara.shape(stuck("EDITOR", GITHUB_RUN_ID=str(run_id), GATE_REASON=reason),
                          no_runs, no_jobs, NOW)["idempotency_key"]
                for run_id, reason in ((901, "1 new priority item(s)"),
                                       (902, "171 min since the last editor run"),
                                       (903, "forced by workflow_dispatch"))}
        self.assertEqual({f"aradio-stuck-editor-{SINCE}-{TODAY}"}, keys)
        shaped = ara.shape(stuck("EDITOR"), no_runs, no_jobs, NOW)
        self.assertEqual(("Aradio stuck: editor failing", "5", "aradio,outage"),
                         (shaped["title"], shaped["priority"], shaped["tags"]))
        self.assertIn(f"Nothing has published since {SINCE}", shaped["text"])
        self.assertTrue(shaped["text"].startswith("Gate: 1 new priority item(s)\n"))

    def test_a_long_outage_re_alerts_once_a_day(self):
        # Hooker keeps a key whose every delivery failed, so a key that never
        # rolled over would let one lost delivery silence the whole outage.
        first = ara.shape(stuck("EDITOR"), no_runs, no_jobs, NOW)["idempotency_key"]
        next_day = ara.shape(stuck("EDITOR"), no_runs, no_jobs,
                             datetime(2026, 11, 1, 0, 50, tzinfo=timezone.utc))["idempotency_key"]
        self.assertNotEqual(first, next_day)
        self.assertEqual(f"aradio-stuck-editor-{SINCE}-2026-11-01", next_day)

    def test_a_new_cause_or_a_new_outage_alerts_again(self):
        editor = ara.shape(stuck("EDITOR"), no_runs, no_jobs, NOW)["idempotency_key"]
        validation = ara.shape(stuck("VALIDATE", EDITOR="success"), no_runs, no_jobs, NOW)
        later = ara.shape(stuck("EDITOR", SINCE="2026-10-31T12:50:00Z"), no_runs, no_jobs, NOW)
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
        shaped = ara.shape(env(JOB_STATUS="cancelled", EDITOR="failure"), no_runs, no_jobs, NOW)
        self.assertEqual(f"aradio-stuck-editor-{SINCE}-{TODAY}", shaped["idempotency_key"])

    def test_a_run_past_its_timeout_is_stuck_where_it_hung(self):
        # GitHub cancels a job past timeout-minutes: the step running then
        # ends cancelled, and the steps after it are skipped.
        shaped = ara.shape(env(JOB_STATUS="cancelled", INBOX="success", EDITOR="cancelled",
                               VALIDATE="skipped"), no_runs, no_jobs, NOW)
        self.assertEqual(f"aradio-stuck-editor-{SINCE}-{TODAY}", shaped["idempotency_key"])
        self.assertIn("ran past its timeout-minutes", shaped["text"])
        self.assertEqual("gate", ara.failed_stage({"CHECKOUT": "success", "INBOX": "cancelled",
                                                   "EDITOR": "skipped"}))
        self.assertNotIn("timeout", ara.shape(stuck("EDITOR"), no_runs, no_jobs, NOW)["text"])

    def test_before_the_first_bulletin_and_with_an_unknown_cursor(self):
        never = ara.shape(stuck("EDITOR", SINCE="never"), no_runs, no_jobs, NOW)
        self.assertEqual(f"aradio-stuck-editor-never-{TODAY}", never["idempotency_key"])
        self.assertIn("since the station's first bulletin", never["text"])
        # The gate never read the cursor: at most one alert a day.
        unknown = ara.shape(env(JOB_STATUS="failure", SINCE="", GATE_REASON=""), no_runs,
                            no_jobs, NOW)
        self.assertEqual(f"aradio-stuck-setup-unknown-{TODAY}", unknown["idempotency_key"])
        self.assertIn("since an unknown time", unknown["text"])


class RecoveryTest(unittest.TestCase):
    def test_the_first_publication_after_failures_reports_the_recovery(self):
        runs = [run(950, "2026-10-31T11:50:12Z"), run(949, "2026-10-31T10:50:09Z"),
                run(948, "2026-10-31T09:50:11Z", "success")]
        shaped = ara.shape(published(), lambda: runs, no_jobs, NOW)
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
            run(900, "2026-10-31T11:50:00Z", None),         # this run
            run(951, "2026-10-31T10:50:00Z", "cancelled"),  # superseded pending run
            run(952, "2026-10-31T09:50:00Z", "success"),
        ]
        asked = []
        shaped = ara.shape(published(), lambda: runs, jobs_of({951: NEVER_STARTED}, asked), NOW)
        self.assertEqual(("", "", ""), (shaped["title"], shaped["priority"],
                                        shaped["idempotency_key"]))
        self.assertNotIn("Published again", shaped["text"])
        self.assertEqual([951], asked)

    def test_a_run_that_hung_past_its_timeout_was_an_outage_too(self):
        # GitHub reports a job past timeout-minutes as cancelled.
        runs = [run(951, "2026-10-31T10:50:00Z", "cancelled")]
        shaped = ara.shape(published(), lambda: runs, jobs_of({951: EDITOR_HUNG}, []), NOW)
        self.assertEqual(f"aradio-recovered-{SINCE}", shaped["idempotency_key"])
        self.assertIn("after 1 failed run(s)", shaped["text"])

    def test_a_recovery_that_misses_its_audio_keeps_the_audio_alert(self):
        shaped = ara.shape(published(JOB_STATUS="failure"),
                           lambda: [run(950, "2026-10-31T11:50:12Z")], no_jobs, NOW)
        self.assertEqual(("", "", ""), (shaped["title"], shaped["priority"],
                                        shaped["idempotency_key"]))
        self.assertIn("Published again after 1 failed run(s)", shaped["text"])

    def test_the_first_bulletin_counts_every_earlier_failure(self):
        shaped = ara.shape(published(SINCE="never"),
                           lambda: [run(1, "2026-10-30T09:50:00Z")], no_jobs, NOW)
        self.assertEqual("aradio-recovered-never", shaped["idempotency_key"])
        self.assertIn("since the first bulletin", shaped["text"])

    def test_a_failed_lookup_never_blocks_the_telemetry(self):
        def broken(*args):
            raise subprocess.CalledProcessError(1, ["gh"])

        for name, runs_fn, jobs_fn in (
                ("runs", broken, no_jobs),
                ("jobs", lambda: [run(951, "2026-10-31T10:50:00Z", "cancelled")], broken)):
            with self.subTest(name), contextlib.redirect_stderr(io.StringIO()) as err:
                shaped = ara.shape(published(), runs_fn, jobs_fn, NOW)
            self.assertEqual("", shaped["idempotency_key"])
            self.assertIn("::warning::", err.getvalue())
        # Without the gate's stamp there is nothing to compare against.
        self.assertEqual("", ara.shape(published(SINCE=""), no_runs, no_jobs,
                                       NOW)["idempotency_key"])

    def test_query_lists_the_newest_runs_on_main(self):
        completed = subprocess.CompletedProcess([], 0, stdout=json.dumps(
            {"workflow_runs": [run(1, "2026-10-31T10:50:00Z"), "junk"]}))
        with mock.patch.object(ara.subprocess, "run", return_value=completed) as call:
            runs = ara.query_runs("o/r")
        self.assertEqual([run(1, "2026-10-31T10:50:00Z")], runs)
        args = call.call_args.args[0]
        self.assertEqual(["gh", "api", "-X", "GET",
                          "repos/o/r/actions/workflows/aradio.yml/runs"], args[:5])
        self.assertIn("branch=main", args)
        # Filtered here on each attempt's queue time: a created= filter would
        # drop a re-run of an older run.
        self.assertFalse(any(arg.startswith("created=") for arg in args))
        bad = subprocess.CompletedProcess([], 0, stdout="[]")
        with mock.patch.object(ara.subprocess, "run", return_value=bad), \
                self.assertRaises(ValueError):
            ara.query_runs("o/r")


class HistoryTest(unittest.TestCase):
    """--history: the gate's backoff record, read from the run history."""

    def cursor(self, tmp: str, last: str | None) -> str:
        path = Path(tmp) / "cursor.json"
        path.write_text(json.dumps({"schema": 1, "last_editor_run_at": last, "keys": {}}))
        return str(path)

    def record(self, last: str | None, runs: list[dict], by_id: dict,
               asked: list | None = None) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            return ara.history(self.cursor(tmp, last), lambda: runs, "900",
                               jobs_of(by_id, [] if asked is None else asked))

    def test_classifies_the_runs_since_the_last_bulletin(self):
        runs = [
            run(950, "2026-10-31T11:50:12Z", updated_at="2026-10-31T11:53:40Z"),
            run(949, "2026-10-31T10:50:09Z", "cancelled", updated_at="2026-10-31T11:20:09Z"),
            run(948, "2026-10-31T10:20:00Z", updated_at="2026-10-31T10:21:00Z"),
            run(951, "2026-10-31T11:58:00Z", "cancelled", updated_at="2026-10-31T11:58:01Z"),
            run(953, "2026-10-31T09:50:00Z", "success", updated_at="2026-10-31T09:50:30Z"),
            run(940, "2026-10-31T08:53:32Z", updated_at="2026-10-31T08:56:10Z"),  # published SINCE
            run(900, "2026-10-31T12:50:00Z", None),  # this run
        ]
        asked = []
        record = self.record("2026-10-31T17:53:00+09:00", runs, {
            950: EDITOR_FAILED, 949: EDITOR_HUNG, 948: SETUP_FAILED, 951: NEVER_STARTED},
            asked)
        # 950 failed in its editor, 949 hung there past timeout-minutes, and
        # 948 failed at checkout; 951 was superseded while it waited and 953
        # was a gate stop. Only editor runs set the backoff.
        self.assertEqual({"since": SINCE, "failed": 3, "editor_failures": 2,
                          "last_editor_failure_at": "2026-10-31T11:53:40Z",
                          "forced_run": None}, record)
        self.assertEqual([948, 949, 950, 951], sorted(asked))

    def test_a_re_run_counts_from_when_it_was_queued(self):
        # Created before the bulletin, re-run after it: GitHub keeps created_at.
        rerun = run(930, "2026-10-31T07:50:00Z", started_at="2026-10-31T10:00:00Z",
                    updated_at="2026-10-31T10:04:00Z")
        before = run(931, "2026-10-31T07:51:00Z", updated_at="2026-10-31T07:55:00Z")
        record = self.record(SINCE, [rerun, before], {930: EDITOR_FAILED})
        self.assertEqual((1, 1, "2026-10-31T10:04:00Z"),
                         (record["failed"], record["editor_failures"],
                          record["last_editor_failure_at"]))

    def test_a_healthy_or_never_published_station(self):
        self.assertEqual({"since": SINCE, "failed": 0, "editor_failures": 0,
                          "last_editor_failure_at": None, "forced_run": None},
                         self.record(SINCE, [], {}))
        never = self.record(None, [run(1, "2026-10-30T09:50:00Z",
                                       updated_at="2026-10-30T09:52:00Z")], {1: EDITOR_FAILED})
        self.assertEqual({"since": "never", "failed": 1, "editor_failures": 1,
                          "last_editor_failure_at": "2026-10-30T09:52:00Z",
                          "forced_run": None}, never)
        with tempfile.TemporaryDirectory() as tmp:  # no cursor.json yet, as for the gate
            self.assertEqual("never", ara.history(str(Path(tmp) / "cursor.json"),
                                                  lambda: [], "900", no_jobs)["since"])

    def test_lookups_stop_at_the_budget(self):
        runs = [run(1000 + n, f"2026-10-31T{10 + n // 60:02d}:{n % 60:02d}:00Z",
                    updated_at=f"2026-10-31T{10 + n // 60:02d}:{n % 60:02d}:30Z")
                for n in range(ara.MAX_JOB_LOOKUPS + 10)]
        asked = []
        record = self.record(SINCE, runs, {r["id"]: EDITOR_FAILED for r in runs}, asked)
        # Every failure counts; the editor runs among them are a lower bound,
        # which can only shorten the backoff, from the newest run down.
        self.assertEqual(len(runs), record["failed"])
        self.assertEqual(ara.MAX_JOB_LOOKUPS, record["editor_failures"])
        self.assertEqual(runs[-1]["updated_at"], record["last_editor_failure_at"])
        self.assertEqual(ara.MAX_JOB_LOOKUPS, len(asked))
        self.assertEqual(runs[-1]["id"], asked[0])

    def test_the_newest_runs_get_the_lookups(self):
        # Older runs superseded in the queue cannot crowd out the newest
        # editor failures, which are what the backoff waits on.
        superseded = [run(1000 + n, f"2026-10-31T09:{n:02d}:00Z", "cancelled")
                      for n in range(ara.MAX_JOB_LOOKUPS + 5)]
        newest = [run(2000 + n, f"2026-10-31T11:{n:02d}:00Z",
                      updated_at=f"2026-10-31T11:{n:02d}:40Z") for n in range(3)]
        by_id = {**{r["id"]: NEVER_STARTED for r in superseded},
                 **{r["id"]: EDITOR_FAILED for r in newest}}
        record = self.record(SINCE, superseded + newest, by_id)
        self.assertEqual((3, 3, "2026-10-31T11:02:40Z"),
                         (record["failed"], record["editor_failures"],
                          record["last_editor_failure_at"]))

    def test_main_writes_the_record_and_a_failed_lookup_means_no_backoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            cursor, out, record = self.cursor(tmp, SINCE), Path(tmp) / "out", Path(tmp) / "rec"
            runs = [run(950, "2026-10-31T11:50:12Z", updated_at="2026-10-31T11:53:40Z")]
            argv = ["--history", "--cursor", cursor, "--attempts-out", str(record),
                    "--github-output", str(out)]
            with mock.patch.object(ara, "query_runs", return_value=runs), \
                    mock.patch.object(ara, "query_jobs", return_value=EDITOR_FAILED), \
                    mock.patch.dict(os.environ, {"GITHUB_RUN_ID": "900"}), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, ara.main(argv))
            written = json.loads(record.read_text())
            self.assertEqual((1, 1), (written["failed"], written["editor_failures"]))
            self.assertRegex(out.read_text(), r"failed<<(\S+)\n1\n")
            self.assertRegex(out.read_text(), r"force_pending<<(\S+)\nfalse\n")
            broken = subprocess.CalledProcessError(1, ["gh"])
            for name, runs_side, jobs_side in (("runs", broken, None), ("jobs", None, broken)):
                with self.subTest(name):
                    record.unlink(missing_ok=True)
                    with mock.patch.object(ara, "query_runs", return_value=runs,
                                           side_effect=runs_side), \
                            mock.patch.object(ara, "query_jobs", return_value=EDITOR_FAILED,
                                              side_effect=jobs_side), \
                            contextlib.redirect_stdout(io.StringIO()), \
                            contextlib.redirect_stderr(io.StringIO()) as err:
                        self.assertEqual(0, ara.main(argv))
                    self.assertFalse(record.exists())
                    self.assertIn("without backoff", err.getvalue())

    def test_the_recovery_check_reuses_the_history_count(self):
        shaped = ara.shape(published(FAILED_SINCE="3"), no_runs, no_jobs, NOW)
        self.assertEqual("aradio-recovered-" + SINCE, shaped["idempotency_key"])
        self.assertIn("after 3 failed run(s)", shaped["text"])
        self.assertEqual("", ara.shape(published(FAILED_SINCE="0"), no_runs, no_jobs,
                                       NOW)["title"])


class LostForceTest(unittest.TestCase):
    """A forced dispatch the concurrency queue cancelled is honoured by exactly one editor run."""

    # 10:50 ran; a forced dispatch at 10:51 waited behind it; a lane's run
    # queued at 10:52 displaced it (GitHub cancelled it a second later) and
    # is now running as run 900.
    RAN = run(800, "2026-10-31T10:50:00Z", "success")
    FORCED = forced(801, "2026-10-31T10:51:00Z", updated_at="2026-10-31T10:52:01Z")
    NOW_RUNNING = run(900, "2026-10-31T10:52:00Z", None)
    LATER = run(901, "2026-10-31T11:50:00Z", None)

    def find(self, runs, by_id=None, run_id="900", since=SINCE):
        asked = []
        found = ara.lost_force(runs, ara.parse_time(since), run_id,
                               ara.JobLookups(jobs_of(dict(by_id or {}), asked)))
        return (found or {}).get("id"), asked

    def test_the_run_that_displaced_it_honours_it(self):
        self.assertEqual((801, [801]), self.find([self.NOW_RUNNING, self.FORCED, self.RAN],
                                                 {801: NEVER_STARTED}))
        # A job that waited for a runner and never got one did not start either.
        self.assertEqual(801, self.find([self.NOW_RUNNING, self.FORCED, self.RAN],
                                        {801: WAITED_FOR_A_RUNNER})[0])

    def test_an_editor_run_after_it_spends_it(self):
        # The honouring run's editor failed, or hung until GitHub cancelled the
        # job at timeout-minutes: either way the force is spent, not renewed.
        for name, conclusion, its_jobs in (("failed", "failure", EDITOR_FAILED),
                                           ("timed out", "cancelled", EDITOR_HUNG)):
            with self.subTest(name):
                honoured = run(900, "2026-10-31T10:52:00Z", conclusion)
                self.assertEqual((None, [801, 900]), self.find(
                    [self.LATER, honoured, self.FORCED, self.RAN],
                    {801: NEVER_STARTED, 900: its_jobs}, run_id="901"))

    def test_a_re_run_that_ran_its_editor_spends_it(self):
        # A re-run keeps its created_at; it was queued when it displaced the forced run.
        rerun = run(700, "2026-10-31T09:00:00Z", started_at="2026-10-31T10:52:00Z")
        self.assertEqual((None, [801, 700]), self.find(
            [self.LATER, self.FORCED, self.RAN, rerun],
            {801: NEVER_STARTED, 700: EDITOR_FAILED}, run_id="901"))

    def test_a_run_that_never_reached_its_editor_passes_it_on(self):
        failed_early = run(900, "2026-10-31T10:52:00Z")
        self.assertEqual((801, [801, 900]), self.find(
            [self.LATER, failed_early, self.FORCED, self.RAN],
            {801: NEVER_STARTED, 900: SETUP_FAILED}, run_id="901"))
        # A gate stop after it ran no editor (its history lookup must have
        # failed), so it is not even looked up.
        stopped = run(900, "2026-10-31T10:52:00Z", "success")
        self.assertEqual((801, [801]), self.find([self.LATER, stopped, self.FORCED, self.RAN],
                                                 {801: NEVER_STARTED}, run_id="901"))

    def test_a_bulletin_stamped_after_it_spends_it(self):
        self.assertEqual((None, []), self.find([self.LATER, self.FORCED, self.RAN],
                                               since="2026-10-31T10:53:00Z", run_id="901"))

    def test_the_run_that_published_in_the_stamps_minute_spent_it(self):
        # Displaced at 10:51:40 by run 900, which stamped 10:51:55 as 10:51.
        late = forced(801, "2026-10-31T10:51:30Z", updated_at="2026-10-31T10:51:41Z")
        publisher = run(900, "2026-10-31T10:51:40Z", "success")
        self.assertEqual((None, [801, 900]), self.find(
            [self.LATER, publisher, late, self.RAN], {801: NEVER_STARTED, 900: PUBLISHED},
            since="2026-10-31T10:51:00Z", run_id="901"))

    def test_a_forced_run_that_started_is_not_lost(self):
        for name, runs, by_id in (
                ("ran", [self.NOW_RUNNING, forced(801, "2026-10-31T10:51:00Z", "success"),
                         self.RAN], {}),
                ("cancelled mid-run", [self.NOW_RUNNING, self.FORCED, self.RAN],
                 {801: jobs(("Set up job", "success"))})):
            with self.subTest(name):
                self.assertIsNone(self.find(runs, by_id)[0])

    def test_a_forced_run_cancelled_by_hand_while_it_waited_is_not_lost(self):
        # Nothing was queued behind it before it was cancelled at 10:51:20.
        by_hand = forced(801, "2026-10-31T10:51:00Z", updated_at="2026-10-31T10:51:20Z")
        self.assertEqual((None, []), self.find([self.NOW_RUNNING, by_hand, self.RAN]))

    def test_unforced_cancellations_and_this_run_are_ignored(self):
        superseded = dict(self.FORCED, display_title="Aradio")
        self.assertEqual((None, []), self.find([self.NOW_RUNNING, superseded, self.RAN]))
        self.assertEqual((None, []), self.find([self.FORCED, self.RAN], run_id="801"))

    def test_gate_stops_while_stuck_are_never_looked_up(self):
        # Run 900 honoured it and its editor failed; the backoff then stopped
        # the gate on every trigger until now.
        stops = [run(910 + n, f"2026-10-31T{11 + n}:20:00Z", "success") for n in range(6)]
        current = run(999, "2026-10-31T17:50:00Z", None)
        honoured = run(900, "2026-10-31T10:52:00Z")
        self.assertEqual((None, [801, 900]), self.find(
            [current, *reversed(stops), honoured, self.FORCED, self.RAN],
            {801: NEVER_STARTED, 900: EDITOR_FAILED}, run_id="999"))

    def test_past_the_lookup_budget_it_is_honoured_rather_than_lost(self):
        # Every run since it failed at checkout, from the one that displaced
        # it at 10:52, more than the budget can read.
        failures = [run(1000 + n, f"2026-10-31T{10 + (52 + n) // 60:02d}:{(52 + n) % 60:02d}:00Z")
                    for n in range(ara.MAX_JOB_LOOKUPS + 5)]
        current = run(999, "2026-10-31T23:00:00Z", None)
        by_id = {801: NEVER_STARTED, **{f["id"]: SETUP_FAILED for f in failures}}
        found, asked = self.find([current, *failures, self.FORCED, self.RAN], by_id,
                                 run_id="999")
        self.assertEqual(801, found)
        self.assertEqual(ara.MAX_JOB_LOOKUPS, len(asked))

    def test_history_reports_it_and_main_raises_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            cursor = Path(tmp) / "cursor.json"
            cursor.write_text(json.dumps({"last_editor_run_at": SINCE, "keys": {}}))
            out, record = Path(tmp) / "out", Path(tmp) / "rec"
            with mock.patch.object(ara, "query_runs",
                                   return_value=[self.NOW_RUNNING, self.FORCED, self.RAN]), \
                    mock.patch.object(ara, "query_jobs", return_value=[]), \
                    mock.patch.dict(os.environ, {"GITHUB_RUN_ID": "900"}), \
                    contextlib.redirect_stdout(io.StringIO()) as stdout:
                self.assertEqual(0, ara.main(["--history", "--cursor", str(cursor),
                                              "--attempts-out", str(record),
                                              "--github-output", str(out)]))
            self.assertEqual(801, json.loads(record.read_text())["forced_run"])
            self.assertRegex(out.read_text(), r"force_pending<<(\S+)\ntrue\n")
            self.assertIn("::notice::honouring forced run 801", stdout.getvalue())

    def test_workflow_names_forced_runs_and_feeds_the_gate(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/aradio.yml").read_text())
        self.assertIn(f"inputs.force && '{ara.FORCED_TITLE}'", workflow["run-name"])
        steps = {step.get("id"): step for step in workflow["jobs"]["aradio"]["steps"]}
        self.assertEqual("${{ inputs.force || steps.history.outputs.force_pending == 'true' }}",
                         steps["inbox"]["env"]["FORCE"])
        # The history tells an editor run from a gate stop by this step's
        # name, and a gate stop skips it.
        self.assertEqual(ara.EDITOR_STEP, steps["editor"]["name"])
        self.assertEqual("steps.inbox.outputs.go == 'true'", steps["editor"]["if"])


class ReviewerReproTest(unittest.TestCase):
    """The cases of the review's check_lost_force.py, on the jobs data GitHub returns.

    Lettered as in the review: (a) timeout, (b) re-run, (c) early failure. As
    there, a forced run F queued at 10:05 waited behind R0 and a run queued
    later displaced it. GitHub cancels a displaced run about a second after
    the displacing run is queued, so F's updated_at is that moment. A run that
    honoured F ran its editor, since force opens the gate.
    """

    R0 = run(1, "2026-11-01T10:00:00Z", "success")
    STUCK_SINCE = "2026-11-01T09:00:00Z"  # the last bulletin, before all of this

    def forced_run(self, displaced_at: str) -> dict:
        return forced(2, "2026-11-01T10:05:00Z", updated_at=displaced_at)

    def honours(self, runs, by_id, since=STUCK_SINCE):
        found = ara.lost_force(runs, ara.parse_time(since), "99",
                               ara.JobLookups(jobs_of(by_id, [])))
        return found["id"] if found else None

    def test_baseline_the_run_after_the_honouring_run(self):
        # L displaced F at 10:20, honoured it and published (stamp 10:20).
        honoured = run(3, "2026-11-01T10:20:00Z", "success")
        self.assertIsNone(self.honours([honoured, self.forced_run("2026-11-01T10:20:01Z"),
                                        self.R0], {2: NEVER_STARTED},
                                       since="2026-11-01T10:20:00Z"))

    def test_a_the_honouring_run_timed_out(self):
        # Run 31886390685's shape: past timeout-minutes, the run ends cancelled.
        honoured = run(3, "2026-11-01T10:20:00Z", "cancelled")
        self.assertIsNone(self.honours([honoured, self.forced_run("2026-11-01T10:20:01Z"),
                                        self.R0], {2: NEVER_STARTED, 3: EDITOR_HUNG}))

    def test_b_the_honouring_run_was_a_re_run_of_an_older_run(self):
        # A re-run keeps created_at (09:00); its attempt was queued at 10:30.
        for name, conclusion, by_id, since in (
                ("published", "success", {2: NEVER_STARTED}, "2026-11-01T10:30:00Z"),
                ("failed after its editor", "failure", {2: NEVER_STARTED, 0: EDITOR_FAILED},
                 self.STUCK_SINCE)):
            with self.subTest(name):
                rerun = run(0, "2026-11-01T09:00:00Z", conclusion,
                            started_at="2026-11-01T10:30:00Z")
                self.assertIsNone(self.honours(
                    [self.forced_run("2026-11-01T10:30:01Z"), self.R0, rerun], by_id,
                    since=since))

    def test_c_the_replacing_run_failed_before_its_editor(self):
        failed_early = run(3, "2026-11-01T10:20:00Z", "failure")
        self.assertEqual(2, self.honours([failed_early, self.forced_run("2026-11-01T10:20:01Z"),
                                          self.R0], {2: NEVER_STARTED, 3: SETUP_FAILED}))

    def test_backoff_two_runs_past_timeout_minutes_are_two_failed_editor_runs(self):
        hung = [run(5, "2026-11-01T10:00:00Z", "cancelled"),
                run(6, "2026-11-01T11:00:00Z", "cancelled")]
        failed, editor = ara.failures_since(hung, ara.parse_time(self.STUCK_SINCE), "99",
                                            ara.JobLookups(jobs_of({5: EDITOR_HUNG,
                                                                    6: EDITOR_HUNG}, [])))
        self.assertEqual((2, 2), (len(failed), len(editor)))


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
        self.assertEqual("${{ steps.history.outputs.failed }}", shape_step["env"]["FAILED_SINCE"])
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
