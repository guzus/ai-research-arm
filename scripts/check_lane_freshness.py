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
  0  every artifact is available and every producer is healthy
  2  one or more availability/producer states alert
  1  internal error (e.g. not a git repository)

Per-lane thresholds are tuned to each lane's schedule (see CLAUDE.md
"GitHub Actions Workflows") with a buffer of roughly two missed cycles
plus runner-queue slack, so a single transient failure does not page.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Optional

from artifact_slos import freshness_entries

# lane -> max tolerated age in hours before we consider it stale.
# Cadence comments reference the schedules documented in CLAUDE.md.
# On-demand lanes (generative, issues) and experimental A/B lanes
# (twitter-deepseek*, twitter-viral) are intentionally excluded: they
# have no fixed cadence, so staleness is not a meaningful signal there.
_FRESHNESS_ENTRIES = freshness_entries()
LANE_THRESHOLDS_HOURS: dict[str, float] = {
    entry["id"]: float(entry["cadence"]["freshness_slo_hours"])
    for entry in _FRESHNESS_ENTRIES
}
LANE_FRESHNESS_PATHS: dict[str, tuple[str, ...]] = {
    entry["id"]: tuple(entry["freshness_paths"]) for entry in _FRESHNESS_ENTRIES
}
LANE_DEGRADED_SIGNALS: dict[str, dict[str, object]] = {
    entry["id"]: entry["degraded_signal"]
    for entry in _FRESHNESS_ENTRIES
    if isinstance(entry.get("degraded_signal"), dict)
}

FRESH = "fresh"
STALE = "stale"
MISSING = "missing"
UNKNOWN = "unknown"

AVAILABLE = "available"
UNAVAILABLE = "unavailable"
HEALTHY = "healthy"
DEGRADED = "degraded"

# States that should trigger an alert.
# UNKNOWN means the watchdog cannot prove freshness (commonly truncated git
# history or registry/path drift). Treating uncertainty as green recreated the
# exact silent-outage class this watchdog exists to close.
ALERTING_STATES = frozenset({STALE, MISSING, UNKNOWN})


@dataclass
class LaneStatus:
    lane: str
    threshold_hours: float
    age_hours: Optional[float]
    state: str
    producer_state: str = HEALTHY
    degraded_reason: Optional[str] = None

    @property
    def availability(self) -> str:
        if self.state == FRESH:
            return AVAILABLE
        if self.state in {STALE, MISSING}:
            return UNAVAILABLE
        return UNKNOWN

    @property
    def alerting(self) -> bool:
        return self.state in ALERTING_STATES or self.producer_state != HEALTHY


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
    paths = LANE_FRESHNESS_PATHS.get(lane, (f"research/{lane}",))
    return all(
        bool(glob.glob(os.path.join(repo_root, path)))
        if any(char in path for char in "*?[")
        else os.path.exists(os.path.join(repo_root, path))
        for path in paths
    )


def lane_age_hours(lane: str, now_epoch: int, repo_root: str) -> Optional[float]:
    """Hours since the last commit touching research/<lane>/.

    Returns None when the lane has no commits reachable in the current
    history (e.g. a shallow clone, or a genuinely never-written lane).
    """
    paths = LANE_FRESHNESS_PATHS.get(lane, (f"research/{lane}",))
    last = _git(["log", "-1", "--format=%ct", "--", *paths], repo_root)
    if not last:
        return None
    try:
        commit_epoch = int(last)
    except ValueError:
        return None
    return (now_epoch - commit_epoch) / 3600.0


def _select_values(value: object, selector: str) -> list[object]:
    """Resolve a deliberately small dotted selector with ``*`` wildcards.

    This is not JSONPath: keeping the grammar to object keys plus collection
    wildcard makes registry signals deterministic and easy to validate.
    """
    values = [value]
    for part in selector.split("."):
        next_values: list[object] = []
        for current in values:
            if part == "*":
                if isinstance(current, dict):
                    next_values.extend(current.values())
                elif isinstance(current, list):
                    next_values.extend(current)
            elif isinstance(current, dict) and part in current:
                next_values.append(current[part])
        values = next_values
    return values


def lane_producer_health(lane: str, repo_root: str) -> tuple[str, Optional[str]]:
    """Return producer health independently of artifact availability.

    A lane without an executable degraded signal is healthy by construction:
    its policy fails closed and therefore cannot publish a labelled degraded
    artifact. Configured signals are strict. Missing git/JSON evidence is
    UNKNOWN and alerts rather than silently claiming producer health.
    """
    signal = LANE_DEGRADED_SIGNALS.get(lane)
    if not signal:
        return HEALTHY, None
    label = str(signal["label"])
    kind = signal["kind"]
    if kind == "commit_subject":
        configured_paths = signal.get("paths")
        paths = (
            tuple(str(path) for path in configured_paths)
            if isinstance(configured_paths, list)
            else LANE_FRESHNESS_PATHS.get(lane, (f"research/{lane}",))
        )
        subject = _git(["log", "-1", "--format=%s", "--", *paths], repo_root)
        if subject is None:
            return UNKNOWN, f"{label}: commit subject unavailable"
        if re.fullmatch(str(signal["pattern"]), subject):
            return DEGRADED, f"{label}: {subject}"
        return HEALTHY, None
    if kind == "json_boolean_any":
        relative_glob = str(signal["path"])
        matches = sorted(glob.glob(os.path.join(repo_root, relative_glob)))
        if not matches:
            return UNKNOWN, f"{label}: no file matches {relative_glob}"
        artifact_path = matches[-1]
        display_path = os.path.relpath(artifact_path, repo_root)
        try:
            with open(artifact_path, encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            return UNKNOWN, f"{label}: cannot read {display_path}: {type(exc).__name__}"
        for selector in signal.get("required_selectors", []):
            if not _select_values(payload, str(selector)):
                return UNKNOWN, f"{label}: {display_path} missing required {selector}"
        observed = False
        for selector in signal["selectors"]:  # validated by artifact_slos
            values = _select_values(payload, str(selector))
            if not values:
                continue
            observed = True
            if any(not isinstance(value, bool) for value in values):
                return UNKNOWN, f"{label}: {display_path} {selector} is not boolean"
            if any(value is True for value in values):
                return DEGRADED, f"{label}: {display_path} {selector}=true"
        if not observed:
            if signal.get("absent_means_false") is True:
                return HEALTHY, None
            return UNKNOWN, f"{label}: {display_path} selectors matched no values"
        return HEALTHY, None
    if kind == "text_regex":
        relative_glob = str(signal["path"])
        matches = sorted(glob.glob(os.path.join(repo_root, relative_glob)))
        if not matches:
            return UNKNOWN, f"{label}: no file matches {relative_glob}"
        latest = matches[-1]
        try:
            with open(latest, encoding="utf-8") as handle:
                text = handle.read()
        except OSError as exc:
            return UNKNOWN, f"{label}: cannot read {relative_glob}: {type(exc).__name__}"
        if re.search(str(signal["pattern"]), text):
            return DEGRADED, f"{label}: {os.path.relpath(latest, repo_root)}"
        return HEALTHY, None
    return UNKNOWN, f"unsupported degraded signal kind: {kind}"


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
    producer_fn: Callable[[str, str], tuple[str, Optional[str]]] = lane_producer_health,
) -> list[LaneStatus]:
    """Evaluate every configured lane. age_fn/dir_exists_fn are injectable
    so the logic can be unit-tested without a real repository."""
    results: list[LaneStatus] = []
    for lane, threshold in thresholds.items():
        exists = dir_exists_fn(lane, repo_root)
        age = age_fn(lane, now_epoch, repo_root) if exists else None
        producer_state, reason = producer_fn(lane, repo_root) if exists else (UNKNOWN, None)
        results.append(
            LaneStatus(
                lane,
                threshold,
                age,
                classify(age, threshold, exists),
                producer_state,
                reason,
            )
        )
    return results


def _fmt_age(age_hours: Optional[float]) -> str:
    if age_hours is None:
        return "?"
    if age_hours < 48:
        return f"{age_hours:.1f}h"
    return f"{age_hours / 24:.1f}d"


def format_report(statuses: list[LaneStatus]) -> str:
    """Human/markdown-friendly table. Alerting lanes first."""
    icon = {FRESH: "✅", STALE: "🔴", MISSING: "❓", UNKNOWN: "⚠️"}
    order = {STALE: 0, MISSING: 1, UNKNOWN: 2, FRESH: 3}
    rows = sorted(statuses, key=lambda s: (not s.alerting, order[s.state], s.lane))
    lines = [
        "| lane | availability | producer | legacy state | age | threshold | detail |",
        "|---|---|---|---|---|---|---|",
    ]
    for s in rows:
        detail = (s.degraded_reason or "-").replace("|", "\\|")
        lines.append(
            f"| `{s.lane}` | {icon[s.state]} {s.availability} | {s.producer_state} "
            f"| {s.state} | {_fmt_age(s.age_hours)} | {s.threshold_hours:g}h | {detail} |"
        )
    return "\n".join(lines)


def idempotency_key(alert_lanes: list[str], now: datetime) -> str:
    """Stable per-day key over the alert set, so the same outage reported
    by both the ubuntu-latest and self-hosted watchdog jobs (and by repeat
    runs the same day) collapses to a single delivered alert. A change in
    the alert set (escalation) produces a new key."""
    date = now.strftime("%Y-%m-%d")
    part = "-".join(sorted(alert_lanes)) if alert_lanes else "none"
    return f"lane-freshness-{date}-{part}"


def _emit_github_output(statuses: list[LaneStatus], report: str, key: str) -> None:
    out_path = os.environ.get("GITHUB_OUTPUT")
    if not out_path:
        return
    alert_lanes = sorted(s.lane for s in statuses if s.alerting)
    unavailable_lanes = sorted(s.lane for s in statuses if s.availability != AVAILABLE)
    degraded_lanes = sorted(s.lane for s in statuses if s.producer_state == DEGRADED)
    producer_unknown_lanes = sorted(s.lane for s in statuses if s.producer_state == UNKNOWN)
    # `stale` remains the compatibility alert bit consumed by existing actions.
    stale = "true" if alert_lanes else "false"
    delim = "__ARA_REPORT_EOF__"
    with open(out_path, "a", encoding="utf-8") as fh:
        fh.write(f"stale={stale}\n")
        fh.write(f"stale_lanes={','.join(alert_lanes)}\n")
        fh.write(f"alert={stale}\n")
        fh.write(f"alert_lanes={','.join(alert_lanes)}\n")
        fh.write(f"unavailable_lanes={','.join(unavailable_lanes)}\n")
        fh.write(f"degraded_lanes={','.join(degraded_lanes)}\n")
        fh.write(f"producer_unknown_lanes={','.join(producer_unknown_lanes)}\n")
        fh.write(f"idempotency_key={key}\n")
        fh.write(f"report<<{delim}\n{report}\n{delim}\n")


def _emit_step_summary(report: str, alert_lanes: list[str]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    header = (
        f"### 🔴 Pipeline health: {len(alert_lanes)} lane(s) alerting\n\n"
        if alert_lanes
        else "### ✅ Pipeline health: all artifacts available, producers healthy\n\n"
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
    alert_lanes = [s.lane for s in statuses if s.alerting]
    unavailable_lanes = [s.lane for s in statuses if s.availability != AVAILABLE]
    degraded_lanes = [s.lane for s in statuses if s.producer_state == DEGRADED]
    producer_unknown_lanes = [s.lane for s in statuses if s.producer_state == UNKNOWN]
    report = format_report(statuses)
    key = idempotency_key(alert_lanes, now_dt)

    if args.json:
        print(
            json.dumps(
                {
                    "now": now_dt.isoformat(),
                    "stale_lanes": sorted(alert_lanes),
                    "alert_lanes": sorted(alert_lanes),
                    "unavailable_lanes": sorted(unavailable_lanes),
                    "degraded_lanes": sorted(degraded_lanes),
                    "producer_unknown_lanes": sorted(producer_unknown_lanes),
                    "idempotency_key": key,
                    "lanes": [
                        {
                            "lane": s.lane,
                            "state": s.state,
                            "availability": s.availability,
                            "producer_state": s.producer_state,
                            "degraded_reason": s.degraded_reason,
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

    _emit_github_output(statuses, report, key)
    _emit_step_summary(report, alert_lanes)

    if alert_lanes:
        print(f"\n::error::lane health alerts: {', '.join(sorted(alert_lanes))}", file=sys.stderr)
        return 2
    print("\nall artifacts available; all producers healthy", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
