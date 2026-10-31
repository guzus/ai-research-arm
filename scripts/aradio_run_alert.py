#!/usr/bin/env python3
"""Aradio's view of its own run history: back off while stuck, alert once.

Failed runs commit nothing, so GitHub's run history is the only record of
them. This script reads it twice per run.

--history (before the gate) reads this workflow's runs since the cursor's
last_editor_run_at and writes the gate's --attempts record:

- failed: the runs that failed, or that started and were then cancelled.
  GitHub reports a job past its timeout-minutes as cancelled, so a hang
  counts; a run cancelled while it waited in the queue never started.
- editor_failures and last_editor_failure_at: those of them whose editor
  step ran, and when the newest one finished. Every editor run since the
  last bulletin failed (one that published moved the cursor), and these set
  the gate's doubling backoff (build_aradio_inbox.retry_at). A setup or gate
  failure spent no editor time, so it never adds to the wait.
- forced_run: a forced dispatch (run-name FORCED_TITLE) that the concurrency
  queue cancelled before it ran. GitHub keeps one pending run per group and
  cancels the older one when another run queues, so a lane's run queued
  behind a forced dispatch would otherwise drop `force` without a word. It
  stays pending until an editor runs after it: in a bulletin stamped later,
  or in a later run whose editor step ran. So exactly one editor run spends
  it, even one that then times out or is a re-run, and a run that fails
  before its editor passes it on. A forced run that started, or that was
  cancelled by hand while it waited (no run queued behind it), was not lost.
  A re-run never honours one: its first attempt had that chance, and the API
  shows only a run's latest attempt (docs/aradio.md lists the bounded edge
  cases).

Runs are ordered by when their latest attempt was queued: a re-run keeps its
created_at, and run_started_at is the attempt's queue time. A run's jobs cost
one API call, so at most MAX_JOB_LOOKUPS are made, newest run first. Past that
the counts are lower bounds, which can only shorten the backoff, and a forced
run whose fate the lookups cannot reach is honoured rather than lost.

Default (the run's last step): shapes the run's Hooker event, so an outage
alerts once a day and its recovery once.

aradio.yml posts one hooker-telemetry event per run, priority 5 when the job
fails. A run that fails WITHOUT publishing leaves research/aradio/cursor.json
as it was (CLAUDE.md rule 15c), so the next run retries the same material
and, while the cause lasts (editor quota or token, a validator mismatch, a
broken push), fails the same way. Such a stuck run's event is keyed on the
stage that failed, the cursor's last_editor_run_at (which only a publication
moves) and the UTC date, so Hooker's per-topic Idempotency-Key delivers the
first and drops the rest. A different stage failing alerts once more. The
date is there because Hooker records a key before it delivers and keeps it
when every delivery fails: without it, one lost Telegram delivery would
silence the whole outage. With it, a long outage re-alerts once a day, as
stale lanes do through liveness-check.yml.

The first run that publishes again takes the history step's count of failed
runs since the last publication (or reads the history itself) and, if there
were any, titles its event as the recovery, keyed on the same stamp. A run
that fails AFTER publishing (on-air audio missing, rule 15d) put a new
bulletin out, so it keeps its own per-run alert. A gate stop is keyed on the
UTC hour: every lane that finishes wakes the station, and one "nothing to
air" event an hour is enough.

Inputs are environment variables set by the workflow (step outcomes, the job
status, the gate's `since`, the history step's failure count). Outputs are
hooker-telemetry inputs: title, text, priority, tags and idempotency_key. An
empty value keeps the action's default, so a failure here can never silence
the telemetry step.
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from typing import Callable, Mapping, Optional

# Pipeline stages in order; the first one that failed names a stuck run's cause.
STAGES = (
    ("setup", ("CHECKOUT", "DEPS")),
    ("gate", ("INBOX",)),
    ("editor", ("EDITOR",)),
    ("validation", ("VALIDATE",)),
    ("publish", ("WRITER", "REQUIRE_OUTPUT", "DIFF_SCOPE", "PUSH")),
)
# A publication's stamp is its run's minute, rounded down, so the publishing
# run can have been queued up to a minute after it. Only runs queued after
# this margin certainly came after that publication.
AFTER_STAMP_MARGIN = timedelta(minutes=1)
# Runs that failed. A cancelled run failed only if it started.
FAILED_CONCLUSIONS = frozenset({"failure", "timed_out"})
WORKFLOW_FILE = "aradio.yml"
# aradio.yml's run-name for a forced workflow_dispatch, and its editor step's
# name (both test-pinned).
FORCED_TITLE = "Aradio (forced)"
EDITOR_STEP = "Edit the situation board with the SSOT-routed editor"
# Each run's jobs are one `gh api` call (about 0.4 s). A call that takes
# longer than GH_TIMEOUT is a failed lookup; the workflow step's
# timeout-minutes bounds them all.
MAX_JOB_LOOKUPS = 20
GH_TIMEOUT = 20
# GitHub cancels a pending run a second or two after the run that displaces
# it is queued (as observed on this repository's runs).
DISPLACED_SLACK = timedelta(seconds=30)


def parse_time(value: object) -> Optional[datetime]:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text[-1:] in ("Z", "z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def iso_z(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def failed_stage(env: Mapping[str, str]) -> str:
    for stage, names in STAGES:
        # A step still running at the job's timeout-minutes ends cancelled.
        if any(env.get(name) in ("failure", "cancelled") for name in names):
            return stage
    # The ref guard, the workspace quarantine or a cancellation before checkout.
    return "setup"


def queued_at(run: Mapping) -> Optional[datetime]:
    """When the run's latest attempt was queued (run_started_at; a re-run keeps created_at)."""
    return parse_time(run.get("run_started_at")) or parse_time(run.get("created_at"))


def runs_after(runs: list[dict], moment: Optional[datetime], run_id: str) -> list[dict]:
    """The other runs queued after `moment` (all of them when None), newest first."""
    found = []
    for run in runs:
        queued = queued_at(run)
        if str(run.get("id")) != run_id and queued is not None and (moment is None
                                                                     or queued > moment):
            found.append((queued, run))
    found.sort(key=lambda pair: pair[0], reverse=True)
    return [run for _, run in found]


class JobLookups:
    """Each run's jobs, fetched once, and at most `budget` fetches in all."""

    def __init__(self, jobs_fn: Callable[[object], list[dict]],
                 budget: int = MAX_JOB_LOOKUPS) -> None:
        self.jobs_fn, self.left, self.seen = jobs_fn, budget, {}

    def __call__(self, run: Mapping) -> Optional[list[dict]]:
        """The run's jobs, or None once the budget is spent."""
        key = str(run.get("id"))
        if key not in self.seen:
            if self.left <= 0:
                return None
            self.left -= 1
            self.seen[key] = self.jobs_fn(run.get("id"))
        return self.seen[key]


def never_started(jobs: list[dict]) -> bool:
    """A run cancelled while pending has no jobs, or none that got a runner."""
    return all(not job.get("runner_name") and not job.get("steps") for job in jobs)


def editor_ran(jobs: list[dict]) -> bool:
    """The editor step ran: a gate stop or an earlier failure skips it."""
    return any(step.get("name") == EDITOR_STEP and step.get("conclusion") not in (None, "skipped")
               for job in jobs for step in job.get("steps") or () if isinstance(step, dict))


def failures_since(runs: list[dict], since: Optional[datetime], run_id: str,
                   lookups: JobLookups, editors: bool = True) -> tuple[list[dict], list[dict]]:
    """Failed runs after the last bulletin (any, before the first), and those
    whose editor step ran, newest first.

    A cancelled run failed if it started. Lookups go to the newest runs
    first; past the budget a failed run still counts, but not as an editor
    run, and a cancelled one does not count. Without `editors`, only
    cancelled runs are looked up and the second list stays empty.
    """
    failed, editor = [], []
    for run in runs_after(runs, since + AFTER_STAMP_MARGIN if since else None, run_id):
        conclusion = run.get("conclusion")
        if conclusion not in FAILED_CONCLUSIONS and conclusion != "cancelled":
            continue
        jobs = lookups(run) if editors or conclusion == "cancelled" else None
        if conclusion == "cancelled" and (jobs is None or never_started(jobs)):
            continue
        failed.append(run)
        if jobs is not None and editor_ran(jobs):
            editor.append(run)
    return failed, editor


def newest_finish(runs: list[dict]) -> Optional[datetime]:
    """When the latest of these runs finished (its updated_at)."""
    times = [t for t in (parse_time(run.get("updated_at")) for run in runs) if t is not None]
    return max(times) if times else None


def editor_ran_after(runs: list[dict], moment: datetime, since: Optional[datetime],
                     run_id: str, lookups: JobLookups) -> bool:
    """An editor ran in a run queued after `moment`, which is not before `since`.

    A successful run after the last bulletin was a gate stop (its editor, had
    it run, would have published), so only failed and cancelled runs are
    looked up, plus a successful one queued within the margin after the
    bulletin's stamp: that may be the run that published it. Newest first,
    so the latest editor run is found first. Past the lookup budget the
    answer is no: the force is honoured rather than lost, and the run that
    honours it is the newest editor run when the next run looks.
    """
    publisher_until = since + AFTER_STAMP_MARGIN if since else None
    for run in runs_after(runs, moment, run_id):
        conclusion = run.get("conclusion")
        if conclusion == "success":
            if publisher_until is None or queued_at(run) > publisher_until:
                continue
        elif conclusion not in FAILED_CONCLUSIONS and conclusion != "cancelled":
            continue  # skipped, or still queued or running
        jobs = lookups(run)
        if jobs is None:
            return False
        if editor_ran(jobs):
            return True
    return False


def displaced(forced: dict, runs: list[dict]) -> bool:
    """Another run was queued while the forced run waited: that cancelled it."""
    queued, ended = queued_at(forced), parse_time(forced.get("updated_at"))
    if queued is None or ended is None:
        return False
    return any(other is not forced and (t := queued_at(other)) is not None
               and queued < t <= ended + DISPLACED_SLACK for other in runs)


def lost_force(runs: list[dict], since: Optional[datetime], run_id: str,
               lookups: JobLookups) -> Optional[dict]:
    """The newest forced run the queue cancelled before it ran, if no editor ran since."""
    for run in runs_after(runs, None, run_id):
        if run.get("display_title") != FORCED_TITLE or run.get("conclusion") != "cancelled":
            continue
        queued = queued_at(run)
        if since is not None and since > queued:
            return None  # a bulletin stamped after it (and after any older one) spent it
        if not displaced(run, runs):
            continue  # cancelled by hand while it waited
        jobs = lookups(run)
        if jobs is None or not never_started(jobs):
            continue  # it ran (or cannot be looked up)
        return None if editor_ran_after(runs, queued, since, run_id, lookups) else run
    return None


def read_since(cursor_path: str) -> tuple[Optional[datetime], str]:
    """The cursor's last publication, as the gate normalizes it (`since`)."""
    if not os.path.exists(cursor_path):  # before the first bulletin, as for the gate
        return None, "never"
    with open(cursor_path, encoding="utf-8") as handle:
        cursor = json.load(handle)
    last = parse_time(cursor.get("last_editor_run_at")) if isinstance(cursor, dict) else None
    return last, (iso_z(last) if last else "never")


def history(cursor_path: str, runs_fn: Callable[[], list[dict]], run_id: str,
            jobs_fn: Callable[[object], list[dict]], rerun: bool = False) -> dict:
    """The gate's --attempts record, plus a forced run the queue cancelled.

    One listing of the newest runs serves both: a lost forced run can predate
    the last bulletin. The forced run is looked up first, so the budget's
    remainder bounds only the counts.
    """
    since, label = read_since(cursor_path)
    runs = runs_fn()
    lookups = JobLookups(jobs_fn)
    forced = None if rerun else lost_force(runs, since, run_id, lookups)
    failed, editor = failures_since(runs, since, run_id, lookups)
    last = newest_finish(editor)
    return {"since": label, "failed": len(failed), "editor_failures": len(editor),
            "last_editor_failure_at": iso_z(last) if last else None,
            "forced_run": forced.get("id") if forced else None}


def query_runs(repository: str) -> list[dict]:
    """This workflow's newest runs on main (read-only `gh api`, needs actions: read)."""
    raw = subprocess.run(
        ["gh", "api", "-X", "GET", f"repos/{repository}/actions/workflows/{WORKFLOW_FILE}/runs",
         "-f", "branch=main", "-f", "per_page=100", "-f", "exclude_pull_requests=true"],
        check=True, capture_output=True, text=True, timeout=GH_TIMEOUT).stdout
    payload = json.loads(raw)
    runs = payload.get("workflow_runs") if isinstance(payload, dict) else None
    if not isinstance(runs, list):
        raise ValueError("runs listing has no workflow_runs array")
    return [run for run in runs if isinstance(run, dict)]


def query_jobs(repository: str, run_id: object) -> list[dict]:
    """One run's jobs, latest attempt (read-only `gh api`); a run cancelled while pending has none."""
    raw = subprocess.run(["gh", "api", f"repos/{repository}/actions/runs/{run_id}/jobs"],
                         check=True, capture_output=True, text=True, timeout=GH_TIMEOUT).stdout
    payload = json.loads(raw)
    jobs = payload.get("jobs") if isinstance(payload, dict) else None
    if not isinstance(jobs, list):
        raise ValueError("jobs listing has no jobs array")
    return [job for job in jobs if isinstance(job, dict)]


def shape(env: Mapping[str, str], runs_fn: Callable[[], list[dict]],
          jobs_fn: Callable[[object], list[dict]], now: datetime) -> dict[str, str]:
    today = now.strftime("%Y-%m-%d")
    status = env.get("JOB_STATUS", "")
    since_raw = env.get("SINCE", "").strip()
    since = parse_time(since_raw)
    reason = env.get("GATE_REASON", "").strip()
    lines = [f"Gate: {reason}"] if reason else []
    shaped = {"title": "", "text": "", "priority": "", "tags": "aradio", "idempotency_key": ""}

    if env.get("PUSH") == "success":
        if since is None and since_raw != "never":
            return {**shaped, "text": "\n".join(lines)}
        counted = env.get("FAILED_SINCE", "").strip()
        if counted.isdigit():  # the history step already read them
            failed = int(counted)
        else:
            try:
                failed = len(failures_since(runs_fn(), since, env.get("GITHUB_RUN_ID", ""),
                                            JobLookups(jobs_fn), editors=False)[0])
            except (OSError, subprocess.SubprocessError, ValueError) as exc:
                print(f"::warning::cannot list earlier Aradio runs, so no recovery check: "
                      f"{type(exc).__name__}", file=sys.stderr)
                failed = 0
        if failed:
            label = since_raw if since else "the first bulletin"
            lines.append(f"Published again after {failed} failed run(s) since {label}; "
                         "the outage is over.")
            if status == "success":
                shaped.update(title="✅ Aradio recovered", priority="3",
                              tags="aradio,recovered",
                              idempotency_key=f"aradio-recovered-{since_raw}")
        return {**shaped, "text": "\n".join(lines)}

    if status == "success":
        # A gate stop: nothing published and nothing failed.
        return {**shaped, "text": "\n".join(lines),
                "idempotency_key": f"aradio-stop-{now:%Y-%m-%dT%H}"}

    stage = failed_stage(env)
    if since is not None or since_raw == "never":
        stamp, label = since_raw, (since_raw if since else "the station's first bulletin")
    else:
        stamp, label = "unknown", "an unknown time"  # the gate never read the cursor
    if status == "cancelled":
        lines.append("The job was cancelled: it ran past its timeout-minutes, or someone "
                     "cancelled it.")
    lines.append(f"Nothing has published since {label}. Further {stage} failures stay "
                 "silent for the rest of the UTC day; the first run that publishes again "
                 "reports the recovery.")
    shaped.update(title=f"Aradio stuck: {stage} failing", priority="5",
                  tags="aradio,outage",
                  idempotency_key=f"aradio-stuck-{stage}-{stamp}-{today}")
    return {**shaped, "text": "\n".join(lines)}


def write_outputs(path: Optional[str], values: Mapping[str, str]) -> None:
    if not path:
        return
    delimiter = f"ARADIO_ALERT_{secrets.token_hex(8)}"
    with open(path, "a", encoding="utf-8") as handle:
        for name, value in values.items():
            handle.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--github-output", default=os.environ.get("GITHUB_OUTPUT"))
    parser.add_argument("--history", action="store_true",
                        help="before the gate: write the --attempts record instead")
    parser.add_argument("--cursor", default="research/aradio/cursor.json")
    parser.add_argument("--attempts-out", default=None)
    args = parser.parse_args(argv)
    repository = os.environ.get("GITHUB_REPOSITORY", "")

    def runs_fn() -> list[dict]:
        return query_runs(repository)

    def jobs_fn(run_id: object) -> list[dict]:
        return query_jobs(repository, run_id)

    if args.history:
        try:
            record = history(args.cursor, runs_fn, os.environ.get("GITHUB_RUN_ID", ""), jobs_fn,
                             rerun=os.environ.get("GITHUB_RUN_ATTEMPT", "1") != "1")
        except (OSError, subprocess.SubprocessError, ValueError) as exc:
            # No record means no backoff: a broken lookup can cost attempts,
            # never a station that stops trying. A lost force waits for a run
            # that can read the history (unless this run's editor spends it).
            print(f"::warning::cannot read Aradio's run history ({type(exc).__name__}); "
                  "the gate runs without backoff, and a forced run the queue cancelled "
                  "is left to a later run", file=sys.stderr)
            return 0
        if args.attempts_out:
            with open(args.attempts_out, "w", encoding="utf-8") as handle:
                json.dump(record, handle)
        if record["forced_run"] is not None:
            print(f"::notice::honouring forced run {record['forced_run']}, which the "
                  "concurrency queue cancelled before it ran")
        write_outputs(args.github_output, {
            "failed": str(record["failed"]),
            "force_pending": "true" if record["forced_run"] is not None else "false"})
        print(json.dumps(record))
        return 0
    shaped = shape(os.environ, runs_fn, jobs_fn, datetime.now(timezone.utc))
    write_outputs(args.github_output, shaped)
    print(json.dumps(shaped, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
