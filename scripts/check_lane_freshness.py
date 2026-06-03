#!/usr/bin/env python3
"""Pipeline freshness watchdog.

Measures how long it has been since each scheduled research lane last
produced output, and flags any lane that has gone stale relative to its
expected cadence. Designed to make silent pipeline outages loud.

Why git-commit recency (not file mtime, not filename dates):
  - mtime is rewritten to checkout-time by `actions/checkout`, so it is
    useless for measuring output freshness on a fresh CI checkout.
  - Filename-date prefixes (the previous liveness check's approach) only
    work for lanes whose files are named `YYYY-MM-DD-*`. Slug-named lanes
    (wiki entities, model tickets, generative articles) have no date in
    the filename, so that method silently can't see them.
  - The commit timestamp of the last commit touching `research/<lane>/`
    is universal across every lane and directly reflects "did this lane
    write anything." That is the signal we use.

Requires full git history for the paths under inspection. In CI, check
out with `fetch-depth: 0` (a shallow clone makes `git log` unreliable;
we warn when we detect one).

Exit codes:
  0  every lane is fresh
  2  one or more lanes are stale or their directory is missing (alert)
  1  internal error (e.g. not a git repository)

Per-lane thresholds are tuned to each lane's schedule (see CLAUDE.md
"GitHub Actions Workflows") with a buffer of roughly two missed cycles
plus runner-queue slack, so a single transient failure does not page.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Optional

# lane -> max tolerated age in hours before we consider it stale.
# Cadence comments reference the schedules documented in CLAUDE.md.
# On-demand lanes (generative, issues) and experimental A/B lanes
# (twitter-deepseek*, twitter-viral) are intentionally excluded: they
# have no fixed cadence, so staleness is not a meaningful signal there.
LANE_THRESHOLDS_HOURS: dict[str, float] = {
    "rss": 4,           # hourly at :30
    "blogs": 15,        # every 6h at :13 (~2 missed cycles + runner slack)
    "twitter": 9,       # every 3h at :07
    "community": 11,    # every 4h at :19
    "bluesky": 30,      # daily at 00:11
    "arxiv": 30,        # daily at 06:13
    "digest": 30,       # daily at 00:00
    "models": 30,       # daily at 06:29
    "front-page": 30,   # daily at 00:30
    "wiki": 30,         # daily, after the digest (workflow_run)
}

FRESH = "fresh"
STALE = "stale"
MISSING = "missing"
UNKNOWN = "unknown"

# States that should trigger an alert.
ALERTING_STATES = frozenset({STALE, MISSING})


@dataclass
class LaneStatus:
    lane: str
    threshold_hours: float
    age_hours: Optional[float]
    state: str

    @property
    def alerting(self) -> bool:
        return self.state in ALERTING_STATES


def _git(args: list[str], repo_root: str) -> Optional[str]:
    """Run a git command in repo_root; return stripped stdout or None."""
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return out.stdout.strip()


def lane_dir_exists(lane: str, repo_root: str) -> bool:
    return os.path.isdir(os.path.join(repo_root, "research", lane))


def lane_age_hours(lane: str, now_epoch: int, repo_root: str) -> Optional[float]:
    """Hours since the last commit touching research/<lane>/.

    Returns None when the lane has no commits reachable in the current
    history (e.g. a shallow clone, or a genuinely never-written lane).
    """
    path = f"research/{lane}"
    last = _git(["log", "-1", "--format=%ct", "--", path], repo_root)
    if not last:
        return None
    try:
        commit_epoch = int(last)
    except ValueError:
        return None
    return (now_epoch - commit_epoch) / 3600.0


def classify(age_hours: Optional[float], threshold_hours: float, dir_exists: bool) -> str:
    if not dir_exists:
        return MISSING
    if age_hours is None:
        return UNKNOWN
    return STALE if age_hours > threshold_hours else FRESH


def evaluate(
    thresholds: dict[str, float],
    now_epoch: int,
    repo_root: str,
    *,
    age_fn: Callable[[str, int, str], Optional[float]] = lane_age_hours,
    dir_exists_fn: Callable[[str, str], bool] = lane_dir_exists,
) -> list[LaneStatus]:
    """Evaluate every configured lane. age_fn/dir_exists_fn are injectable
    so the logic can be unit-tested without a real repository."""
    results: list[LaneStatus] = []
    for lane, threshold in thresholds.items():
        exists = dir_exists_fn(lane, repo_root)
        age = age_fn(lane, now_epoch, repo_root) if exists else None
        results.append(LaneStatus(lane, threshold, age, classify(age, threshold, exists)))
    return results


def _fmt_age(age_hours: Optional[float]) -> str:
    if age_hours is None:
        return "?"
    if age_hours < 48:
        return f"{age_hours:.1f}h"
    return f"{age_hours / 24:.1f}d"


def format_report(statuses: list[LaneStatus]) -> str:
    """Human/markdown-friendly table. Stale and missing lanes first."""
    icon = {FRESH: "✅", STALE: "🔴", MISSING: "❓", UNKNOWN: "⚠️"}
    order = {STALE: 0, MISSING: 1, UNKNOWN: 2, FRESH: 3}
    rows = sorted(statuses, key=lambda s: (order[s.state], s.lane))
    lines = ["| lane | state | age | threshold |", "|---|---|---|---|"]
    for s in rows:
        lines.append(
            f"| `{s.lane}` | {icon[s.state]} {s.state} "
            f"| {_fmt_age(s.age_hours)} | {s.threshold_hours:g}h |"
        )
    return "\n".join(lines)


def idempotency_key(stale_lanes: list[str], now: datetime) -> str:
    """Stable per-day key over the stale set, so the same outage reported
    by both the ubuntu-latest and self-hosted watchdog jobs (and by repeat
    runs the same day) collapses to a single delivered alert. A change in
    the stale set (escalation) produces a new key."""
    date = now.strftime("%Y-%m-%d")
    part = "-".join(sorted(stale_lanes)) if stale_lanes else "none"
    return f"lane-freshness-{date}-{part}"


def _emit_github_output(stale_lanes: list[str], report: str, key: str) -> None:
    out_path = os.environ.get("GITHUB_OUTPUT")
    if not out_path:
        return
    stale = "true" if stale_lanes else "false"
    delim = "__ARA_REPORT_EOF__"
    with open(out_path, "a", encoding="utf-8") as fh:
        fh.write(f"stale={stale}\n")
        fh.write(f"stale_lanes={','.join(sorted(stale_lanes))}\n")
        fh.write(f"idempotency_key={key}\n")
        fh.write(f"report<<{delim}\n{report}\n{delim}\n")


def _emit_step_summary(report: str, stale_lanes: list[str]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    header = (
        f"### 🔴 Pipeline freshness: {len(stale_lanes)} lane(s) stale\n\n"
        if stale_lanes
        else "### ✅ Pipeline freshness: all lanes fresh\n\n"
    )
    with open(summary_path, "a", encoding="utf-8") as fh:
        fh.write(header + report + "\n")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Research lane freshness watchdog.")
    parser.add_argument(
        "--now",
        help="ISO-8601 UTC timestamp to evaluate against (default: now). For testing.",
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="Repository root (default: git toplevel of CWD, else CWD).",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table.")
    args = parser.parse_args(argv)

    if args.now:
        # Python <3.11's fromisoformat rejects a trailing 'Z'; normalize it.
        raw = args.now[:-1] + "+00:00" if args.now.endswith("Z") else args.now
        try:
            now_dt = datetime.fromisoformat(raw)
        except ValueError:
            print(f"error: --now is not a valid ISO-8601 timestamp: {args.now}", file=sys.stderr)
            return 1
        if now_dt.tzinfo is None:
            now_dt = now_dt.replace(tzinfo=timezone.utc)
    else:
        now_dt = datetime.now(timezone.utc)
    now_epoch = int(now_dt.timestamp())

    repo_root = args.repo or _git(["rev-parse", "--show-toplevel"], ".") or os.getcwd()

    if _git(["rev-parse", "--is-inside-work-tree"], repo_root) != "true":
        print(f"error: {repo_root} is not a git repository", file=sys.stderr)
        return 1
    if _git(["rev-parse", "--is-shallow-repository"], repo_root) == "true":
        print(
            "::warning::shallow clone detected — git history is incomplete, "
            "freshness may be unreliable. Check out with fetch-depth: 0.",
            file=sys.stderr,
        )

    statuses = evaluate(LANE_THRESHOLDS_HOURS, now_epoch, repo_root)
    stale_lanes = [s.lane for s in statuses if s.alerting]
    report = format_report(statuses)
    key = idempotency_key(stale_lanes, now_dt)

    if args.json:
        print(
            json.dumps(
                {
                    "now": now_dt.isoformat(),
                    "stale_lanes": sorted(stale_lanes),
                    "idempotency_key": key,
                    "lanes": [
                        {
                            "lane": s.lane,
                            "state": s.state,
                            "age_hours": s.age_hours,
                            "threshold_hours": s.threshold_hours,
                        }
                        for s in statuses
                    ],
                },
                indent=2,
            )
        )
    else:
        print(report)

    _emit_github_output(stale_lanes, report, key)
    _emit_step_summary(report, stale_lanes)

    if stale_lanes:
        print(f"\n::error::stale lanes detected: {', '.join(sorted(stale_lanes))}", file=sys.stderr)
        return 2
    print("\nall lanes fresh", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
