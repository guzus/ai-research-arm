#!/usr/bin/env python3
"""Shape Aradio's per-run Hooker event: an outage alerts once, recovery once.

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
per-run alert.

Inputs are environment variables set by the workflow (step outcomes, the job
status, the gate's `since`). Outputs are hooker-telemetry inputs: title,
text, priority, tags and idempotency_key. An empty value keeps the action's
default, so a failure here can never silence the telemetry step.
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


def shape(env: Mapping[str, str], runs_fn: Callable[[Optional[datetime]], list[dict]],
          today: str) -> dict[str, str]:
    status = env.get("JOB_STATUS", "")
    since_raw = env.get("SINCE", "").strip()
    since = parse_time(since_raw)
    reason = env.get("GATE_REASON", "").strip()
    lines = [f"Gate: {reason}"] if reason else []
    shaped = {"title": "", "text": "", "priority": "", "tags": "aradio", "idempotency_key": ""}

    if env.get("PUSH") == "success":
        if since is None and since_raw != "never":
            return {**shaped, "text": "\n".join(lines)}
        try:
            failed = failed_runs_since(runs_fn(since), since, env.get("GITHUB_RUN_ID", ""))
        except (OSError, subprocess.SubprocessError, ValueError) as exc:
            print(f"::warning::cannot list earlier Aradio runs, so no recovery check: "
                  f"{type(exc).__name__}", file=sys.stderr)
            failed = []
        if failed:
            label = since_raw if since else "the first bulletin"
            lines.append(f"Published again after {len(failed)} failed run(s) since {label}; "
                         "the outage is over.")
            if status == "success":
                shaped.update(title="✅ Aradio recovered", priority="3",
                              tags="aradio,recovered",
                              idempotency_key=f"aradio-recovered-{since_raw}")
        return {**shaped, "text": "\n".join(lines)}

    if status == "success":
        return {**shaped, "text": "\n".join(lines)}

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
    args = parser.parse_args(argv)
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    shaped = shape(os.environ, lambda since: query_runs(repository, since),
                   datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    write_outputs(args.github_output, shaped)
    print(json.dumps(shaped, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
