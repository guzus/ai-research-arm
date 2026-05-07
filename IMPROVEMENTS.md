# Methodology Improvements — 2026-05-07

Analysis of the 2026-05-06 research output surfaced two silently-broken
ingestion pipelines and several low-cost coverage upgrades.

> **Apply note:** the GitHub App that runs `daily-improve.yml` does not
> hold the `workflows` permission, so its installation token cannot push
> changes to `.github/workflows/*.yml`. The workflow patches are therefore
> attached as a unified diff in `improvements/2026-05-07-workflow-fixes.patch`.
> A maintainer can apply the changes from the repo root with:
>
> ```bash
> git checkout main
> git apply improvements/2026-05-07-workflow-fixes.patch
> git commit -am "Methodology improvements 2026-05-07: RSS + Bluesky pipeline fixes"
> git push
> ```

## Issues Found

### 1. RSS pipeline silent outage (10 days)
- **Last successful run:** `2026-04-27 09:18 UTC` (commit `90f15f30`).
- **Effect:** `research/rss/2026-05-0*.md` does not exist; the daily digest's
  "Official Announcements" section has been falling back entirely to
  Twitter/community signal for the last 10 days.
- **Root cause:** `https://openrss.org/www.anthropic.com/news` started
  returning HTTP 000 (DNS / connection-level failure). The `curl` invocation
  in `hourly-rss.yml` had **no `--max-time`**, so the step hung until the
  GitHub-hosted runner killed the job — and the next hour's run cancelled
  the previous via `concurrency: cancel-in-progress`. The pipeline never
  produced a commit, so the failure was invisible.
- **Bonus regressions confirmed during triage:**
  - `https://ai.meta.com/blog/rss/` → 404 (Meta retired the public RSS).
  - `https://www.anthropic.com/news/rss.xml` → 404 (no official feed exists).

### 2. Bluesky pipeline returning empty payloads (≥ 6 days)
- `research/bluesky/2026-05-0*.md` files are 5 lines each, all containing
  `"upstream Bluesky fetch returned HTTP 403 Forbidden for all five source
  feeds"`.
- **Root cause:** `public.api.bsky.app/xrpc/app.bsky.feed.searchPosts` now
  returns `403 Request forbidden by administrative rules` for unauthenticated
  callers (see `bluesky-social/bsky-docs#332`). The sibling host
  `api.bsky.app` still accepts the same call without auth; `getAuthorFeed`
  also continues to work on the public host.

### 3. Coverage gaps
The 2026-05-06 digest cited Simon Willison, Jack Clark (Import AI), Zvi
Mowshowitz, and SemiAnalysis as primary sources, but none of those are in
the RSS workflow. The pipeline was only collecting four official-vendor
blogs and three press outlets.

## Changes Made

### `.github/workflows/hourly-rss.yml`
- Wrapped every fetch in a `fetch()` helper with `curl --max-time 15`, so a
  hung endpoint can no longer freeze the step. Empty / zero-byte responses
  are normalized to `<rss></rss>` so the parser never sees a missing file.
- Replaced `openrss.org/www.anthropic.com/news` with the community-maintained
  feed `taobojlen/anthropic-rss-feed` (verified 200 / fresh as of
  2026-05-06, tracks `anthropic.com/news`).
- Removed the dead `ai.meta.com/blog/rss/` source. Meta AI announcements
  are already covered by the Twitter and Bluesky pipelines.
- **Added eight new sources** (all verified 200 from the runner):
  - Microsoft AI Blog (`blogs.microsoft.com/ai`)
  - AWS Machine Learning Blog
  - Cloudflare AI tag
  - Together AI Blog
  - Ars Technica AI
  - arXiv `cs.CL` (NLP-specific, complements `cs.AI` / `cs.LG`)
  - Simon Willison (`simonwillison.net/atom/everything/`)
  - Jack Clark — Import AI (`importai.substack.com/feed`)
  - Zvi Mowshowitz (`thezvi.substack.com/feed`)
  - SemiAnalysis (`semianalysis.com/feed`)
- Updated the Claude prompt's source-file list and output template so the
  new categories actually surface in the daily file.

### `.github/workflows/2h-bluesky.yml`
- `searchPosts` now tries `api.bsky.app` first and falls back to
  `public.api.bsky.app`; both are wrapped with `--max-time 15`.
- Replaced the `from:karpathy.bsky.social` searchPosts hack (which stopped
  returning results) with **`getAuthorFeed`** calls for five high-signal
  accounts: Karpathy, LeCun, Emily M. Bender, Simon Willison, and Hugging
  Face. `getAuthorFeed` still works without auth on the public host.
- Updated the prompt to document the dual JSON shapes (`posts[]` for
  searches, `feed[].post` for author feeds) and to skip empty payloads
  silently rather than emitting `"(no data)"` placeholders.

## Expected Impact
- **RSS pipeline restored:** `research/rss/2026-05-07.md` should be created
  on the next hourly run (`30 * * * *`). Hourly file growth should match
  the 2026-04-22…2026-04-24 baseline (~30–35 KB / day).
- **Bluesky pipeline restored:** the next 00:11 UTC run should produce a
  populated `research/bluesky/2026-05-08.md` instead of the 5-line 403
  stub.
- **Better signal in the daily digest:** the four independent analysts now
  feeding RSS were already cited by name in yesterday's digest — they will
  no longer require Perplexity/Exa MCP backfill to surface.
- **Resilience:** hardcoded timeouts mean a single dead endpoint can never
  again take down the entire RSS step silently.
