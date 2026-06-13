# Methodology Improvements — 2026-06-08

Analysis of the 2026-06-07 research output across all lanes
(twitter, rss, community/HN+Reddit, bluesky, arxiv, models, digest,
ai-news). Most lanes were healthy and high-signal; one lane showed a
concrete, reproducible defect.

> **Docs-only PR.** The fix below lands in a `.github/workflows/` file,
> which the `claude[bot]` GitHub App installation cannot push (it lacks
> the App-level `Workflows: read/write` scope — see the comment block at
> the top of `daily-improve.yml`, and the matching push rejection this
> lane hits whenever it edits a workflow). The exact patch is therefore
> documented here for a maintainer to apply in one paste. Several prior
> improvement PRs are "(docs-only)" for the same reason.

## Issue Found — Bluesky lane: within-day snapshot duplication

`research/bluesky/2026-06-07.md` contains two timestamped snapshots
(01:24 UTC and 12:48 UTC). The **second snapshot re-listed the exact
same posts as the first**, differing only in like-counts:

- @minimaxir "remember when Google showed a demo of diffusion-based
  coding agents…" — identical text in both snapshots (❤️ 5 / ❤️ 5).
- @emollick "One reason you want AIs to be better writers…" —
  identical (❤️ 41 → ❤️ 58).
- @simonwillison.net MicroPython-in-WASM post — identical (❤️ 121 →
  ❤️ 125).
- @natolambert "Recording more post-training lectures…" — identical
  (❤️ 13 / ❤️ 13).

Root cause: the lane runs twice daily, the curator prompt's INCLUDE
filter is "posts from the last 48 hours," and the prompt said only
"append if file exists" with **no instruction to dedup against posts
already listed earlier the same day**. So on a quiet day every post
from the morning pass re-qualifies in the afternoon pass and gets
re-listed. The second snapshot adds bloat, not coverage — directly
undermining the *signal-vs-noise* and *source-diversity* goals the
twice-daily schedule was added (2026-05) to serve.

Notably, an earlier file (`2026-05-23.md`) shows the curator *can*
write a graceful "no new qualifying posts in this window" note — but
only did so by chance, because the prompt never mandated it. The
behavior was inconsistent run-to-run.

## Recommended Change (maintainer applies)

`.github/workflows/2h-bluesky.yml` — curator prompt only (no schedule,
runner, or source-list change). Two edits inside the existing
`prompt: |` block scalar (keep the 12-space indentation):

**(a)** After the `Write to: research/bluesky/…md` line and before
`FORMAT (append if file exists):`, insert:

```
            ## DEDUP ACROSS SNAPSHOTS (read before writing)

            This file may ALREADY contain an earlier snapshot from today (the
            lane runs twice daily, and the 48-hour INCLUDE window means most
            source posts re-qualify on the second pass). If the file exists,
            read it FIRST and collect every post link already listed today.

            When appending the new snapshot, SKIP any post whose link is
            already present earlier in today's file — only list posts that are
            genuinely new since the previous snapshot. A post that merely
            gained likes/reposts is NOT new; do not re-list it.

            If NO genuinely new qualifying posts exist since the earlier
            snapshot, still append the timestamped section but write a single
            italic line under it noting that no new qualifying posts appeared
            in this window (e.g. `_No new qualifying posts from tracked
            researchers since the previous snapshot._`). Do not pad the second
            snapshot by re-listing the first snapshot's posts — duplicated
            content is the failure mode this rule exists to prevent.
```

**(b)** Add a new first item to the FILTERS **SKIP** list so the rule
is visible at the point of filtering:

```
            - Posts already listed in an earlier snapshot in today's file
              (dedup by post link — see "DEDUP ACROSS SNAPSHOTS" above)
```

## Not Changed (and why)

- **No new Bluesky handles added.** Web research surfaced curated
  "AI researcher" starter packs, but the workflow's documented handle
  hygiene rule (see the comment block listing the "ingesting the wrong
  Simon Willison" reassignment bug) requires every handle to be
  live-`getAuthorFeed`-verified before adding. Blind-adding unverified
  handles from a starter pack would risk re-introducing exactly that
  bug. Verification requires a live API call against current Bluesky
  state and belongs in a dedicated, verified pass — not this note.

- **Perplexity MCP quota exhaustion** (noted in
  `digest/2026-06-08-digest.md`: "Perplexity quota exhausted; gaps
  filled via web search"). Logged as an observation. The digest's
  web-search fallback already handled it gracefully, and the fix is a
  quota/billing decision rather than a methodology change, so it is
  out of scope here.

## Expected Impact

- Bluesky daily files stop double-counting posts on quiet days; each
  snapshot reflects only genuinely new activity, so the file length is
  an honest signal of how much was actually said that day.
- Downstream synthesis (the daily digest reads the curated lanes) gets
  a cleaner, non-duplicated Bluesky input.
- Reproducible, low-risk: a prompt-text change inside an existing block
  scalar; no schedule, runner, source, or schema change.
