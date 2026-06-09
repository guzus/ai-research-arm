#!/usr/bin/env python3
"""Pipeline content/volume quality gate (advisory).

The freshness watchdog (scripts/check_lane_freshness.py) answers "did this
lane commit recently?" — but a lane can commit *on time* and still be
broken: bird cookies expire, an upstream feed 500s, an agent emits an empty
shell. The lane writes a near-empty file, the commit lands, freshness stays
green, and the digest synthesizes from nothing. Nothing alerts.

This script closes that gap. For each lane it inspects the MOST RECENT
artifact on disk and flags it when it is anomalously small relative to the
lane's own history. Two independent, deliberately conservative checks:

  1. Absolute floor (`min_bytes`): the latest artifact is smaller than a
     hard per-lane floor. The floors sit *well below* every legitimately
     committed day we have on record (see the calibration note on each
     lane), so a genuinely quiet day never trips this — only a near-empty
     or `[]`-shaped artifact does.

  2. Relative drop: the latest artifact is below `drop_ratio` of the
     trailing MEDIAN of the previous N artifacts AND below a soft floor
     (`min_bytes * soft_floor_mult`). Median (not mean) is used because
     real lanes are extremely bursty — twitter ranges 1.7KB–318KB, rss
     1.1KB–392KB day to day — and a mean is dragged around by those spikes.
     The two conditions are ANDed: a lane only flags when output has both
     collapsed relative to typical *and* fallen into "suspiciously small"
     territory. A quiet-but-normal day (e.g. bluesky dropping to a third of
     its median) clears the soft floor and is NOT flagged.

Why this design avoids alert fatigue:
  - Findings are ADVISORY. The script exits 0 even when it flags something
    (unless `--exit-code` is passed); the workflow routes anomalies to the
    alert channel without failing the job. Freshness remains the hard gate.
  - Empirically tuned: with the shipped defaults, a backtest over the full
    research/ history flags only the handful of genuinely near-dead days
    (rss at 4% of median, bluesky at 2-3%) and zero normal days.
  - The drop check needs `--history-min` (default 4) prior samples before it
    will fire, so a brand-new or sparse lane is never flagged on thin data.

Like the freshness watchdog this is stdlib-only, so it runs identically on
both the ubuntu-latest and self-hosted runner tiers. It reads files from the
working tree (the checkout the watchdog already has), not git history, so it
does not need full history or LFS blobs. (All inspected artifacts are
non-LFS text — the front-page lane deliberately reads the `.html` render, not
the LFS-tracked `.png`, so `lfs: false` checkouts still see real bytes.)

Known limitations (conscious MVP scope):
  - The gate measures BYTES, not item/line counts. It cannot catch a
    "template present but zero items" artifact that still clears the byte
    floor (e.g. a digest with section headers but no stories). Byte volume is
    a strong, cheap proxy that catches the dominant failure mode (empty/[]
    output); an item-count check could be layered on per lane later.
  - The wiki lane is effectively floor-only (log.md only ever grows, so the
    relative-drop arm is disabled). It catches a truncated/empty log, not a
    semantically-garbage ingest — acceptable given the CRUD-not-regenerate
    wiki semantics, where bytes are not a reliable signal of ingest quality.
  - The watchdog inspects the working-tree copy of *today's* file for
    sub-daily lanes (rss/twitter/community), which is partially accumulated.
    Verified non-issue: the schedule (00/06/12/18 UTC) means the 00:00 run
    predates today's first sub-daily write, and every lane's first daily cycle
    already commits well above its soft floor (twitter ~12KB, rss/community
    ~2.6KB vs soft floors 1.8KB/1.2KB), so a partial-day file never trips the
    drop arm.

Exit codes:
  0  default — even when anomalies are found (advisory). Anomalies are still
     surfaced via $GITHUB_OUTPUT (`anomaly=true`) and the step summary.
  2  one or more lanes anomalous, AND --exit-code was passed.
  1  internal error.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import statistics
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional


@dataclass(frozen=True)
class LaneSpec:
    """Per-lane content policy.

    glob:           shell glob (relative to repo root) selecting the lane's
                    canonical *primary* artifact across all dates. The most
                    recent match (lexical sort — the YYYY-MM-DD prefix makes
                    this chronological) is the artifact under inspection.
    min_bytes:      hard floor. Below this the latest artifact is flagged
                    regardless of history. Set below every real committed day.
    drop_ratio:     latest < drop_ratio * trailing-median triggers the
                    relative-drop arm (when also below the soft floor).
    soft_floor_mult: soft floor = min_bytes * this. The relative-drop arm
                    only fires when latest is ALSO below this, so a large lane
                    halving on a quiet day does not page.
    """

    glob: str
    min_bytes: int
    drop_ratio: float = 0.10
    soft_floor_mult: float = 3.0


# Per-lane content policy. Floors are calibrated from the real history in
# research/ (the inline "obs min" is the smallest legitimately committed
# artifact seen for that lane; the floor sits comfortably under it). The
# lane set mirrors check_lane_freshness.py: on-demand lanes (generative,
# issues) and experimental A/B lanes (twitter-deepseek*, twitter-fireworks*)
# are excluded — they have no steady cadence, so "small" is not a signal.
LANE_SPECS: dict[str, LaneSpec] = {
    # hourly RSS roundup.            obs min ~1.1KB
    "rss": LaneSpec("research/rss/[0-9]*.md", min_bytes=400),
    # 3-hourly twitter report.       obs min ~1.7KB; hugely bursty (→318KB)
    "twitter": LaneSpec("research/twitter/[0-9]*.md", min_bytes=600),
    # 4-hourly community (HN is the canonical primary; reddit runs parallel).
    #                                obs min ~1.5KB
    "community": LaneSpec("research/community/[0-9]*-hn.md", min_bytes=400),
    # twice-daily bluesky.           obs min ~165B (genuinely thin some days)
    "bluesky": LaneSpec("research/bluesky/[0-9]*.md", min_bytes=80),
    # daily arxiv papers.            obs min ~6KB
    "arxiv": LaneSpec("research/arxiv/[0-9]*-papers.md", min_bytes=1500),
    # daily synthesized digest.      obs min ~8.4KB
    "digest": LaneSpec("research/digest/[0-9]*-digest.md", min_bytes=2000),
    # daily model-timeline diff.     obs min ~455B (slow news days)
    "models": LaneSpec("research/models/[0-9]*-timeline.md", min_bytes=150),
    # daily front-page (HTML render is the stable text artifact; the PNG can
    # be an LFS pointer on read-only checkouts so we avoid it). obs min ~6.5KB
    "front-page": LaneSpec("research/front-page/[0-9]*-front-page.html", min_bytes=1500),
    # daily wiki ingest. The per-page slugs are CRUD'd (an UPDATE may not grow
    # bytes), but log.md is append-only — one entry per run — so it is the
    # reliable "the ingest ran and did something" signal. It only ever grows,
    # so the relative-drop arm is disabled (drop_ratio=0) and only the floor
    # applies.
    "wiki": LaneSpec("research/wiki/log.md", min_bytes=300, drop_ratio=0.0),
}

HEALTHY = "healthy"
EMPTY = "empty"          # below the absolute floor
DROP = "drop"            # collapsed vs trailing median
MISSING = "missing"      # no artifact found at all
INSUFFICIENT = "insufficient-history"  # too few samples to judge a drop

# States that should route an alert.
ANOMALOUS_STATES = frozenset({EMPTY, DROP, MISSING})


@dataclass
class LaneContent:
    lane: str
    spec: LaneSpec
    artifact: Optional[str]          # basename of the inspected artifact
    size: Optional[int]              # bytes of the latest artifact
    median: Optional[float]          # trailing median of prior samples
    sample_count: int                # number of prior samples available
    state: str
    detail: str = ""
    ratio: Optional[float] = field(default=None)

    @property
    def anomalous(self) -> bool:
        return self.state in ANOMALOUS_STATES


def lane_artifact_sizes(spec: LaneSpec, repo_root: str) -> list[tuple[str, int]]:
    """All artifacts matching the lane glob, oldest→newest, as (basename, bytes).

    Lexical sort is chronological because every artifact name is
    `YYYY-MM-DD-...` (or, for wiki, a single fixed file). Symlinks and
    non-files are skipped defensively.
    """
    pattern = os.path.join(repo_root, spec.glob)
    out: list[tuple[str, int]] = []
    for path in sorted(glob.glob(pattern)):
        if not os.path.isfile(path):
            continue
        try:
            out.append((os.path.basename(path), os.path.getsize(path)))
        except OSError:
            continue
    return out


def classify(
    sizes: list[tuple[str, int]],
    spec: LaneSpec,
    *,
    history_min: int,
    trailing_n: int,
) -> LaneContent:
    """Pure classification over a list of (name, size) samples for one lane.

    Kept free of IO so it is trivially unit-testable; lane_artifact_sizes is
    the injectable IO seam used by callers and tests. The lane name is filled
    in by the caller (evaluate) after construction.
    """
    if not sizes:
        return LaneContent(
            lane="", spec=spec, artifact=None, size=None, median=None,
            sample_count=0, state=MISSING, detail="no artifact matched glob",
        )

    latest_name, latest_size = sizes[-1]
    prior = [s for _, s in sizes[:-1]]
    trail = prior[-trailing_n:]
    median = statistics.median(trail) if trail else None
    soft_floor = spec.min_bytes * spec.soft_floor_mult
    ratio = (latest_size / median) if median else None

    # 1) Absolute floor — the strongest signal, evaluated first and
    #    independent of history. A truly empty / `[]`-shaped artifact.
    if latest_size < spec.min_bytes:
        return LaneContent(
            lane="", spec=spec, artifact=latest_name, size=latest_size,
            median=median, sample_count=len(trail), state=EMPTY, ratio=ratio,
            detail=f"{latest_size}B < floor {spec.min_bytes}B",
        )

    # 2) Relative drop — only when we have enough history to trust a median,
    #    the lane opts in (drop_ratio > 0), and the artifact is BOTH a small
    #    fraction of typical AND below the soft floor.
    if (
        spec.drop_ratio > 0
        and median is not None
        and len(trail) >= history_min
        and latest_size < spec.drop_ratio * median
        and latest_size < soft_floor
    ):
        return LaneContent(
            lane="", spec=spec, artifact=latest_name, size=latest_size,
            median=median, sample_count=len(trail), state=DROP, ratio=ratio,
            detail=(
                f"{latest_size}B is {ratio:.0%} of trailing median "
                f"{median:.0f}B (< {spec.drop_ratio:.0%}) and < soft floor "
                f"{soft_floor:.0f}B"
            ),
        )

    # Healthy, but note when we simply lacked the history to judge a drop so
    # the report is honest rather than implying we checked.
    if spec.drop_ratio > 0 and len(trail) < history_min:
        state = INSUFFICIENT
        detail = f"{latest_size}B (only {len(trail)} prior sample(s); drop check skipped)"
    else:
        state = HEALTHY
        detail = f"{latest_size}B" + (f" ({ratio:.0%} of median)" if ratio else "")

    return LaneContent(
        lane="", spec=spec, artifact=latest_name, size=latest_size,
        median=median, sample_count=len(trail), state=state, ratio=ratio,
        detail=detail,
    )


def evaluate(
    specs: dict[str, LaneSpec],
    repo_root: str,
    *,
    history_min: int = 4,
    trailing_n: int = 8,
    sizes_fn: Callable[[LaneSpec, str], list[tuple[str, int]]] = lane_artifact_sizes,
) -> list[LaneContent]:
    """Evaluate every configured lane. sizes_fn is injectable so the logic can
    be unit-tested without a real repository (mirrors check_lane_freshness.py's
    age_fn/dir_exists_fn pattern)."""
    results: list[LaneContent] = []
    for lane, spec in specs.items():
        sizes = sizes_fn(spec, repo_root)
        status = classify(sizes, spec, history_min=history_min, trailing_n=trailing_n)
        status.lane = lane
        results.append(status)
    return results


def _fmt_bytes(n: Optional[float]) -> str:
    if n is None:
        return "?"
    n = float(n)
    if n < 1024:
        return f"{n:.0f}B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f}KB"
    return f"{n / (1024 * 1024):.1f}MB"


def format_report(statuses: list[LaneContent]) -> str:
    """Markdown-friendly table. Anomalous lanes first."""
    icon = {
        HEALTHY: "✅",
        EMPTY: "🔴",
        DROP: "🟠",
        MISSING: "❓",
        INSUFFICIENT: "⚪",
    }
    order = {EMPTY: 0, DROP: 1, MISSING: 2, INSUFFICIENT: 3, HEALTHY: 4}
    rows = sorted(statuses, key=lambda s: (order.get(s.state, 9), s.lane))
    lines = ["| lane | state | latest | median | detail |", "|---|---|---|---|---|"]
    for s in rows:
        lines.append(
            f"| `{s.lane}` | {icon.get(s.state, '?')} {s.state} "
            f"| {_fmt_bytes(s.size)} | {_fmt_bytes(s.median)} | {s.detail} |"
        )
    return "\n".join(lines)


def idempotency_key(anomalous_lanes: list[str], now: datetime) -> str:
    """Stable per-day key over the anomalous set, so the same anomaly reported
    by both the ubuntu-latest and self-hosted watchdog jobs (and by repeat runs
    the same day) collapses to a single delivered alert. A change in the
    anomalous set produces a new key. Mirrors check_lane_freshness.idempotency_key
    with a distinct prefix so content and freshness alerts never collide."""
    date = now.strftime("%Y-%m-%d")
    part = "-".join(sorted(anomalous_lanes)) if anomalous_lanes else "none"
    return f"lane-content-{date}-{part}"


def _emit_github_output(anomalous_lanes: list[str], report: str, key: str) -> None:
    out_path = os.environ.get("GITHUB_OUTPUT")
    if not out_path:
        return
    anomaly = "true" if anomalous_lanes else "false"
    delim = "__ARA_CONTENT_REPORT_EOF__"
    with open(out_path, "a", encoding="utf-8") as fh:
        fh.write(f"anomaly={anomaly}\n")
        fh.write(f"anomalous_lanes={','.join(sorted(anomalous_lanes))}\n")
        fh.write(f"idempotency_key={key}\n")
        fh.write(f"report<<{delim}\n{report}\n{delim}\n")


def _emit_step_summary(report: str, anomalous_lanes: list[str]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    header = (
        f"### 🟠 Lane content: {len(anomalous_lanes)} lane(s) anomalous (advisory)\n\n"
        if anomalous_lanes
        else "### ✅ Lane content: all lanes look healthy\n\n"
    )
    with open(summary_path, "a", encoding="utf-8") as fh:
        fh.write(header + report + "\n")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Research lane content/volume quality gate (advisory).",
    )
    parser.add_argument(
        "--now",
        help="ISO-8601 UTC timestamp for the idempotency key (default: now). For testing.",
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="Repository root (default: git toplevel of CWD, else CWD).",
    )
    parser.add_argument(
        "--trailing-n",
        type=int,
        default=8,
        help="How many prior artifacts to take the median over (default: 8).",
    )
    parser.add_argument(
        "--history-min",
        type=int,
        default=4,
        help="Minimum prior samples before the drop check fires (default: 4).",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table.")
    parser.add_argument(
        "--exit-code",
        action="store_true",
        help="Exit 2 when any lane is anomalous (default: always exit 0 — advisory).",
    )
    args = parser.parse_args(argv)

    if args.now:
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

    repo_root = args.repo
    if repo_root is None:
        import subprocess

        try:
            top = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
            repo_root = top or os.getcwd()
        except (subprocess.CalledProcessError, FileNotFoundError):
            repo_root = os.getcwd()

    statuses = evaluate(
        LANE_SPECS,
        repo_root,
        history_min=args.history_min,
        trailing_n=args.trailing_n,
    )
    anomalous_lanes = [s.lane for s in statuses if s.anomalous]
    report = format_report(statuses)
    key = idempotency_key(anomalous_lanes, now_dt)

    if args.json:
        print(
            json.dumps(
                {
                    "now": now_dt.isoformat(),
                    "anomalous_lanes": sorted(anomalous_lanes),
                    "idempotency_key": key,
                    "lanes": [
                        {
                            "lane": s.lane,
                            "state": s.state,
                            "artifact": s.artifact,
                            "size": s.size,
                            "median": s.median,
                            "sample_count": s.sample_count,
                            "ratio": s.ratio,
                            "detail": s.detail,
                        }
                        for s in statuses
                    ],
                },
                indent=2,
            )
        )
    else:
        print(report)

    _emit_github_output(anomalous_lanes, report, key)
    _emit_step_summary(report, anomalous_lanes)

    if anomalous_lanes:
        print(
            f"\n::warning::content anomaly in lane(s): {', '.join(sorted(anomalous_lanes))} "
            "(advisory — does not fail the job)",
            file=sys.stderr,
        )
        return 2 if args.exit_code else 0
    print("\nall lanes look healthy", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
