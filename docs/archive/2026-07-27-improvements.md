# Methodology improvements — 2026-07-27

## Issue found

`research/youtube/2026-07-26.md` (and every daily file from `2026-07-23.md`
through `2026-07-27.md`, all identically 2,411 bytes) shows:

```
- Unique videos collected: 0
- High-signal videos selected: 0
- Fetch errors: 8
```

with 8 of the 10 registered `tuber-api` sources returning `HTTPError: HTTP
Error 500: Internal Server Error`. That's a step-function break from the
88–90 unique videos/day the lane produced through 2026-07-22, and the
2026-07-26 daily digest's own Executive Summary noted "YouTube's fetch
failing across 8 of 10 tracked channels" — so the degradation was visible in
downstream synthesis but nothing in the pipeline escalated it.

`daily-youtube.yml` and `scripts/fetch_youtube_signal.py` still committed
and pushed this empty-content file every day as a clean, exit-0 run — no
Telegram/hooker alert, no failed job — because `main()` already had a
signal-loss guard (added after a 2026-07-12 total-outage incident, see the
code comment at `scripts/fetch_youtube_signal.py`), but that guard only
fired when **every** checked source raised an exception
(`len(fetch_errors) == len(sources)`). The 2 non-erroring "trending"-kind
sources returned empty payloads rather than raising, so the literal
all-failed check never tripped, and the lane silently wrote a zero-content
shell as a "successful" partial failure for five straight days.

## Fix

`scripts/fetch_youtube_signal.py`: generalized the zero-signal guard from
"every source raised" (`len(fetch_errors) == len(sources)`) to "at least one
source raised **and** zero candidates were collected overall"
(`sources and not candidates and fetch_errors`). This still exits 0 and
writes normally for:
- a partial failure where at least one source contributed a candidate
  (existing `test_partial_failure_still_writes_daily_file` behavior,
  unchanged), and
- a genuinely empty registry or a real zero-error/zero-candidate slow news
  day (no evidence of a fetch problem, so no reason to fail loudly),

but now also exits `EXIT_TOTAL_FETCH_FAILURE` (3) and writes nothing for the
exact 2026-07-23..07-27 shape: some sources error, the rest return nothing
useful, total candidates collected across the whole registry is zero. That
puts the outage back in front of the freshness watchdog / job failure
signal instead of resetting its git-recency clock with a clean-looking
empty file.

Added `test_zero_candidates_with_partial_errors_exits_3` to
`scripts/test_fetch_youtube_signal.py`, reproducing the observed
partial-error/zero-candidate shape and asserting exit code 3 and no file
write. Updated the existing `TotalFetchFailureGuardTest` docstring to match
the generalized condition. Full suite (20 tests, stdlib `unittest`, no
network) passes.

## Expected impact

The next time `tuber-api`'s `/search` endpoint (or any subset of sources)
degrades while a minority of sources keep responding without error, the
`daily-youtube.yml` job will fail loudly on the first affected day instead
of silently degrading for days before `liveness-check.yml` or a human
happens to notice the digest's own commentary. This does not fix the
underlying `tuber-api` `/search` 500s (external service, out of this repo's
control) — it restores the fail-loud contract the 2026-07-12 fix intended,
which had a gap for the "partial-but-effectively-total" failure shape.
