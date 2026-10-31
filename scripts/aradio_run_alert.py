#!/usr/bin/env python3
"""Aradio's view of its own run history: back off while stuck, alert once.

Failed runs commit nothing, so GitHub's run history is the only record of
them. This script reads it twice per run.

--history (before the gate): counts this workflow's failed runs since the
cursor's last_editor_run_at and the newest failure's time, for the gate's
doubling backoff (build_aradio_inbox.retry_at), and writes them as the
gate's --attempts record. It also finds a forced dispatch that the
concurrency queue cancelled before it ran: GitHub keeps one pending run per
group and cancels the older one, so a lane's run queued behind a forced
dispatch would otherwise drop `force` without a word. The forced run is
marked by its run-name (FORCED_TITLE); the first run to execute after it
honours it.

Default (the run's last step): shapes the run's Hooker event, so an outage
alerts once a day and its recovery once.

aradio.yml posts one hooker-telemetry event per hourly run, priority 5 when
the job fails. A run that fails WITHOUT publishing leaves
research/aradio/cursor.json as it was (CLAUDE.md rule 15c), so the next hour
retries the same material and, while the cause lasts (editor quota or token,
a validator mismatch, a broken push), fails the same way: about 24 alerts a
day for one outage. Such a stuck run's event is keyed on the stage that
failed, the cursor's last_editor_run_at (which only a publication moves) and
the UTC date, so Hooker's per-topic Idempotency-Key delivers the first and
drops the rest. A different stage failing alerts once more. The date is
there because Hooker records a key before it delivers and keeps it when
every delivery fails: without it, one lost Telegram delivery would silence
the whole outage. With it, a long outage re-alerts once a day, as stale
lanes do through liveness-check.yml.

The first run that publishes again asks GitHub for this workflow's failed
runs created after that publication and, if there are any, titles its event
as the recovery, keyed on the same stamp. A run that fails AFTER publishing
(on-air audio missing, rule 15d) put a new bulletin out, so it keeps its own
per-run alert. A gate stop is keyed on the UTC hour: every lane that finishes
wakes the station, and one "nothing to air" event an hour is enough.

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
# The publishing run's own created_at can trail its minute-aligned stamp by
# up to a minute, so only runs created after this margin certainly came later.
CREATED_AFTER_MARGIN = timedelta(minutes=1)
# A cancelled run is usually a pending run GitHub superseded, not an outage.
FAILED_CONCLUSIONS = frozenset({"failure", "timed_out"})
WORKFLOW_FILE = "aradio.yml"
# aradio.yml's run-name for a forced workflow_dispatch (test-pinned).
FORCED_TITLE = "Aradio (forced)"
# Conclusions of runs whose job actually ran (a skipped job never did).
EXECUTED_CONCLUSIONS = frozenset({"success", "failure", "timed_out"})


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
        if any(env.get(name) == "failure" for name in names):
            return stage
    # The ref guard, the workspace quarantine or a cancellation.
    return "setup"


def failed_runs_since(runs: list[dict], since: Optional[datetime],
                      current_run_id: str) -> list[dict]:
    """Failed runs created after the last publication (any, before the first)."""
    cutoff = since + CREATED_AFTER_MARGIN if since else None
    found = []
    for run in runs:
        if str(run.get("id")) == current_run_id or run.get("conclusion") not in FAILED_CONCLUSIONS:
            continue
        created = parse_time(run.get("created_at"))
        if created is None or (cutoff is not None and created <= cutoff):
            continue
        found.append(run)
    return found


def newest_failure(runs: list[dict]) -> Optional[datetime]:
    """When the latest of these failed runs finished (its updated_at)."""
    times = [t for t in (parse_time(run.get("updated_at")) for run in runs) if t is not None]
    return max(times) if times else None


def read_since(cursor_path: str) -> tuple[Optional[datetime], str]:
    """The cursor's last publication, as the gate normalizes it (`since`)."""
    if not os.path.exists(cursor_path):  # before the first bulletin, as for the gate
        return None, "never"
    with open(cursor_path, encoding="utf-8") as handle:
        cursor = json.load(handle)
    last = parse_time(cursor.get("last_editor_run_at")) if isinstance(cursor, dict) else None
    return last, (iso_z(last) if last else "never")


def never_started(jobs: list[dict]) -> bool:
    """A run cancelled while pending has no jobs, or none that got a runner."""
    return all(not job.get("runner_name") and not job.get("steps") for job in jobs)


def lost_force(runs: list[dict], run_id: str,
               jobs_fn: Callable[[object], list[dict]]) -> Optional[dict]:
    """A forced run the queue cancelled before it ran, after the last run that ran.

    Runs are serialized, so a forced run created after the newest executed
    run was pending behind it. If it then ended cancelled without ever
    starting, the run executing now (or one it replaced) took its place.
    Every later run sees a newer executed run, so it is honoured once.
    """
    others = [run for run in runs if str(run.get("id")) != run_id]
    executed = [t for t in (parse_time(run.get("created_at")) for run in others
                            if run.get("conclusion") in EXECUTED_CONCLUSIONS) if t]
    newest_executed = max(executed) if executed else None
    for run in others:
        created = parse_time(run.get("created_at"))
        if (run.get("display_title") != FORCED_TITLE or run.get("conclusion") != "cancelled"
                or created is None or (newest_executed and created <= newest_executed)):
            continue
        if never_started(jobs_fn(run.get("id"))):
            return run
    return None


def history(cursor_path: str, runs_fn: Callable[[Optional[datetime]], list[dict]],
            run_id: str, jobs_fn: Callable[[object], list[dict]]) -> dict:
    """The gate's --attempts record, plus a forced run the queue cancelled.

    One listing of the newest runs serves both: the failures are filtered to
    those after the last bulletin here, and a lost forced run can predate it.
    """
    since, label = read_since(cursor_path)
    runs = runs_fn(None)
    failed = failed_runs_since(runs, since, run_id)
    last = newest_failure(failed)
    forced = lost_force(runs, run_id, jobs_fn)
    return {"since": label, "failed": len(failed),
            "last_failed_at": iso_z(last) if last else None,
            "forced_run": forced.get("id") if forced else None}


def query_runs(repository: str, since: Optional[datetime]) -> list[dict]:
    """This workflow's recent runs on main (read-only `gh api`, needs actions: read)."""
    args = ["gh", "api", "-X", "GET",
            f"repos/{repository}/actions/workflows/{WORKFLOW_FILE}/runs",
            "-f", "branch=main", "-f", "per_page=100", "-f", "exclude_pull_requests=true"]
    if since is not None:
        args += ["-f", f"created=>{iso_z(since + CREATED_AFTER_MARGIN)}"]
    raw = subprocess.run(args, check=True, capture_output=True, text=True, timeout=60).stdout
    payload = json.loads(raw)
    runs = payload.get("workflow_runs") if isinstance(payload, dict) else None
    if not isinstance(runs, list):
        raise ValueError("runs listing has no workflow_runs array")
    return [run for run in runs if isinstance(run, dict)]


def query_jobs(repository: str, run_id: object) -> list[dict]:
    """One run's jobs (read-only `gh api`); a run cancelled while pending has none."""
    raw = subprocess.run(["gh", "api", f"repos/{repository}/actions/runs/{run_id}/jobs"],
                         check=True, capture_output=True, text=True, timeout=60).stdout
    payload = json.loads(raw)
    jobs = payload.get("jobs") if isinstance(payload, dict) else None
    if not isinstance(jobs, list):
        raise ValueError("jobs listing has no jobs array")
    return [job for job in jobs if isinstance(job, dict)]


def shape(env: Mapping[str, str], runs_fn: Callable[[Optional[datetime]], list[dict]],
          now: datetime) -> dict[str, str]:
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
        if counted.isdigit():  # the history step already listed them
            failed = int(counted)
        else:
            try:
                failed = len(failed_runs_since(runs_fn(since), since,
                                               env.get("GITHUB_RUN_ID", "")))
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
    if args.history:
        try:
            record = history(args.cursor, lambda since: query_runs(repository, since),
                             os.environ.get("GITHUB_RUN_ID", ""),
                             lambda run_id: query_jobs(repository, run_id))
        except (OSError, subprocess.SubprocessError, ValueError) as exc:
            # No record means no backoff: a broken lookup can cost attempts,
            # never a station that stops trying. A lost force stays lost, so say so.
            print(f"::warning::cannot read Aradio's run history ({type(exc).__name__}); "
                  "the gate runs without backoff, and a forced run the queue cancelled "
                  "would not be honoured", file=sys.stderr)
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
    shaped = shape(os.environ, lambda since: query_runs(repository, since),
                   datetime.now(timezone.utc))
    write_outputs(args.github_output, shaped)
    print(json.dumps(shaped, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
