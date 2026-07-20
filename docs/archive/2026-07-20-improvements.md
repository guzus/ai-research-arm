# Methodology Improvements — 2026-07-20

Analysis of 2026-07-19 output across all research lanes, plus a git-history
audit of the pipeline's data-integrity files.

## Concrete defect found (cited)

**The Twitter headline-dedup ledger has been silently un-pushed for 16
days, and nothing in the pipeline surfaces it.**

Evidence:

- `research/summaries/twitter-announced-history.json` (529,046 bytes) has
  not been committed since `ce2df5de` "Track delivered Twitter headline
  alerts 2026-07-04 17:48 UTC". `git log --all --grep="Track delivered
  Twitter headline"` shows 338 prior commits at a steady ~4-8h cadence
  (max pre-outage gap 2026-07-01→07-04: 7.6h), then **zero** commits since.
- Yet `hourly-twitter.yml` ran continuously through 2026-07-19 and kept
  delivering headline alerts (`public_items` 6, 2, 2, 5, 3, 3 across the
  day per `research/twitter/status/2026-07-19-*.json`) — so the ledger
  *should* have kept updating.
- Root cause, `.github/workflows/hourly-twitter.yml` line 1336:
  `git_auth push origin "HEAD:main"` — a raw direct push to `main`,
  bypassing `.github/actions/safe-push` (used correctly by the same
  workflow's primary content push at line 1130). CLAUDE.md load-bearing
  rule 13 documents that the branch-protection ruleset active since
  2026-07-06 rejects every direct push to `main`, including workflow
  `GITHUB_TOKEN` pushes, with `GH013`. The retry loop at lines 1335-1345
  does `pull --rebase` between attempts, which cannot fix a ruleset
  rejection (it isn't a fast-forward problem), so this push has been
  structurally incapable of succeeding since 07-06.
- On exhaustion it only logs `::warning::Failed to push delivered-alert
  history after retries; alerts were already sent, continuing` (line 1347)
  and does **not** fail the job. No lane in `scripts/check_lane_freshness.py`
  covers this specific file — the `twitter` lane threshold only watches
  `research/twitter/`, which stays fresh every cycle from unrelated
  status-heartbeat commits — so the outage had **zero CI/telemetry
  signal** for 16 days. Impact: headline delivery itself is unaffected,
  but every headline sent since 07-04 is invisible to future
  cross-cycle/cross-day duplicate-suppression checks, undermining the
  contract in `docs/headline-dedupe.md`.

## Changes made

**`scripts/check_lane_freshness.py` — track the ledger file's own commit
recency, independent of its parent lane directory.**

- New `FILE_THRESHOLDS_HOURS` config (currently one entry:
  `twitter-dedup-ledger` → `research/summaries/twitter-announced-history.json`,
  30h threshold — ~4x headroom over the verified 7.6h pre-outage max gap).
- New `tracked_file_exists`/`tracked_file_age_hours`/`evaluate_files`,
  mirroring the existing directory-based `lane_dir_exists`/`lane_age_hours`/
  `evaluate` exactly (same `git log -1 --format=%ct -- <path>` recency
  signal), so a file-specific staleness check can run alongside the
  existing 12 lane checks with the same MISSING/STALE/FRESH/UNKNOWN
  semantics and the same alerting path.
- `main()` now merges both result sets into one report, so a stale ledger
  pages through the existing `.github/actions/lane-freshness-alert`
  channels (hooker + direct Telegram) and fails the watchdog job — with
  **no changes needed** to that action or to `liveness-check.yml`, since
  both consume the script's output generically.
- `scripts/test_check_lane_freshness.py` — 4 new tests (unit-level
  stale/fresh/missing classification via injected fakes, plus real-git
  integration tests backdating a commit to 2026-07-04 and asserting it's
  flagged STALE against a 2026-07-20 clock). Full suite:
  `python3 -m unittest test_check_lane_freshness -v` → 17/17 pass.
- Verified against the live repo: running the updated script now reports
  `twitter-dedup-ledger` STALE at 379.4h age (30h threshold) while all 12
  existing lanes remain FRESH — confirming both the fix and the absence
  of regressions to the pre-existing checks.

## Recommended follow-up (NOT in this PR — needs `workflows` permission)

The actual root-cause fix is a one-line change in
`.github/workflows/hourly-twitter.yml`: replace the raw
`git_auth push origin "HEAD:main"` retry loop (lines 1330-1348) with the
same `.github/actions/safe-push` composite action already used correctly
by this workflow's primary content push (lines 1116-1134). safe-push
handles the protected-`main` case by publishing to a run-scoped
`automation/safe-push/*` branch and auto-merging a PR — exactly the
mechanism the raw push loop lacks.

**This change is not included here because the bot's `GITHUB_TOKEN` lacks
the `workflows` permission to push workflow files** (`daily-improve.yml`'s
own permissions block documents: "Updating workflow files also requires
the claude[bot] GitHub App installation to have Workflows: read/write.
That App-level permission cannot be granted from this workflow's
permissions block."). The maintainer should apply the safe-push swap
manually; this PR's watchdog extension ensures the failure is loud in the
meantime instead of silent for weeks.

## Expected impact

- Within one `liveness-check.yml` cycle (every 6h) after this merges, the
  currently-stale ledger triggers an immediate Telegram/hooker alert
  instead of remaining invisible — closing the exact "no CI/telemetry
  signal" gap the defect exploited.
- Any future recurrence of this failure mode (or a similar single-file
  staleness issue elsewhere) is caught within ~1 day instead of ~16.
- No behavior change to the 12 existing lane checks — purely additive.
- Does not fix the root cause (the raw push itself); that requires the
  manual `workflows`-permission follow-up above.
