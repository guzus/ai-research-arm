# Twitter fallback stale-row regression - 2026-07-09

## Root cause

The deterministic Twitter fallback ranked every tweet-like row from the Bird JSON snapshot by engagement without checking whether the tweet belonged to the current monitoring window. Account snapshots can contain older high-engagement rows, so stale tweets such as Karpathy's May 2026 Anthropic announcement outranked fresh lower-engagement posts in July fallback output.

## Fix

- `scripts/deterministic_twitter_digest.py` now parses the workflow timestamp and only accepts rows whose `createdAt` falls within a 36-hour freshness window, with 15 minutes of future skew tolerance.
- Rows with missing or unparseable timestamps are excluded from fallback ranking.
- `scripts/test_deterministic_twitter_digest.py` has a regression test where a 50-day-old high-engagement Karpathy row must lose to a fresh lower-engagement row.

## Cleanup

Removed or corrected July 6-9 generated artifacts where stale fallback rows were presented as current Twitter/X signal. Valid May historical coverage was left intact.

## Verification

- `PYTHONPATH=scripts uv run python -m unittest scripts.test_backend_matrix scripts.test_deterministic_twitter_digest`
- `git diff --check`
- Repository search confirms the stale Karpathy/Niels rows no longer appear in July 6-9 research artifacts.
