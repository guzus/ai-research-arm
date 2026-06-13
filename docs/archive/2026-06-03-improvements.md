# Methodology Improvements — 2026-06-03

Analysis of the 2026-06-02 output cycle. The digest, twitter, community,
rss, bluesky, arxiv, and model-timeline lanes all produced fresh, dated
output for 2026-06-02 and the daily digest was high-quality (well-sourced,
primary-link-dense, good signal/noise). The issues below are *coverage and
observability gaps*, not content-quality regressions.

## Issue 1 — The expert-blog lane has been silently dead for 8 days

`daily-ai-blogs.yml` (`scripts/fetch_ai_blogs.py` → `research/blogs/`) was
added on **2026-05-26** and is scheduled every 6h (`cron: '13 */6 * * *'`).
Despite ~270 commits since, **`research/blogs/` has never been committed to
any branch** — `git log --all -- research/blogs` is empty and the directory
does not exist on disk.

Root cause of the runtime failure can't be confirmed from static analysis
alone (it needs the Actions job logs, which this analysis can't reach). What
*is* confirmable:

- The registry `data/sources/ai_blogs.json` validates cleanly against the
  script's rules (all priorities ∈ {P0,P1,P2}, all types valid, no duplicate
  IDs), so `load_sources()` is not crashing the lane.
- `scripts/fetch_ai_blogs.py` writes a file on **every** run (even a
  "no new posts" run emits a timestamped report), so a healthy run would
  always produce a committable diff.

So the failure is downstream (fetch/commit/push on the runner) — but the
**real defect is that nobody noticed for 8 days.** The freshness watchdog
(`scripts/check_lane_freshness.py`) exists precisely to "make silent
pipeline outages loud," yet `blogs` was never registered in
`LANE_THRESHOLDS_HOURS`. A scheduled lane was shipped without monitoring.

### Fix
- **`scripts/check_lane_freshness.py`** — register `blogs` with a 15h
  threshold (6h cadence ≈ 2 missed cycles + runner-queue slack, matching the
  ratio used for the other sub-daily lanes). The watchdog will now classify
  the lane as `MISSING` and page via `liveness-check.yml` until the lane
  starts producing output.

> **Reviewer note:** this change will *immediately* fire a staleness alert
> for `blogs`, because the lane is genuinely down. That alert is the
> intended signal — it points a human at the underlying runtime failure that
> has been invisible since 2026-05-26. It is not a false positive.

## Issue 2 — The digest never reads the expert-blog lane

Both `daily-digest.yml` synthesis prompts (the MCP path and the WebSearch
fallback) enumerate source subdirectories explicitly:

```
Check subdirectories: twitter/, community/, arxiv/, rss/, bluesky/, ...
```

`blogs/` was absent from both lists (and `models/` from the explicit list,
though the agent happened to find it via the weak "and any others"
catch-all). This means that even once the blog lane is producing output, the
high-signal expert-analysis stream (Simon Willison, Interconnects, Import
AI, Ahead of AI, etc.) is not deterministically surfaced into the digest —
exactly the curated analysis the digest's *Research Highlights* and *Tools &
Resources* sections should weight most heavily.

### Fix (maintainer-applied — see note below)
Add `blogs/` and `models/` to the explicit subdirectory list in **both**
`daily-digest.yml` prompts (the MCP path ~line 137 and the WebSearch
fallback ~line 233), with a one-line note that `blogs/` is the curated
expert-analysis lane. This change is **not** in the PR commit because the
bot token that opened it lacks the GitHub `workflows` permission and cannot
modify files under `.github/workflows/`. A maintainer should apply this
patch:

```diff
             STEP 1: Find and read today's source files
             Look in the research/ directory for any reports from today's date (${{ steps.date.outputs.date }}).
-            Check subdirectories: twitter/, community/, arxiv/, rss/, bluesky/, and any others.
+            Check subdirectories: twitter/, community/, arxiv/, rss/, bluesky/, blogs/, models/, and any others.
+            blogs/ is the curated expert-analysis lane (Simon Willison, Interconnects,
+            Import AI, etc.) — weight it for the Tools & Resources and Research sections.
             Read all relevant files you find.
```

(apply the same hunk to the WebSearch-fallback prompt, whose current line
reads `... bluesky/, perplexity/, and any others.`)

## Expected impact

- **Observability:** any future silent outage of the 6h expert-blog lane is
  caught within ~15h instead of going unnoticed indefinitely. Closes the
  monitoring gap that let this one run 8 days dark.
- **Coverage:** once the blog lane is healthy, the digest reliably ingests
  expert analysis instead of leaning entirely on official RSS + Twitter for
  that signal — improving source diversity and the depth of the analysis
  sections.

## Not changed (and why)

- The runtime cause of the blog-lane fetch/commit failure is left for a
  human with access to the Actions logs; guessing at a workflow edit without
  them risks introducing a new bug. The watchdog registration ensures the
  failure is now visible so it can be diagnosed properly.
- No new RSS feeds or sources were added: the registry already curates 22
  high-quality expert feeds. The lane's problem is that it doesn't *run*,
  not that it lacks sources — adding more would be noise.
</content>
</invoke>
