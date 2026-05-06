# Daily Methodology Improvements — 2026-05-06

## Summary

Two production data pipelines have been silently failing for the past 8–10 days.
Yesterday's improvement PR (improve/2026-05-05) identified the same issues but
left the workflow edits in `PROPOSED_WORKFLOW_CHANGES.patch` rather than
applying them. **This PR re-applies the fixes directly.**

If the GitHub App backing this workflow lacks the `workflows` permission, the
push will be rejected for `.github/workflows/` paths; the patch file is kept on
the branch as a fallback for a maintainer with that permission to apply.

## Issues Found

### 1. RSS pipeline silent for 9+ days

- Last successful commit: **2026-04-27 09:18 UTC**.
- `research/rss/` has no `2026-04-28..2026-05-06` files.
- Three of the eleven configured feed URLs are dead, and the workflow
  swallows failures with `... 2>/dev/null || echo "<rss></rss>"`,
  so the dead feeds were never surfaced as errors:

  | Feed                                      | Status (verified 2026-05-06)                              |
  |-------------------------------------------|-----------------------------------------------------------|
  | `openrss.org/www.anthropic.com/news`      | DNS / connection failure (000)                            |
  | `ai.meta.com/blog/rss/`                   | 404 Not Found                                             |
  | `googleaiblog.blogspot.com/atom.xml`      | Redirects to deprecated FeedBurner; no fresh items        |

- **Downstream impact**: the `daily-digest.yml` step that synthesizes the
  daily digest reads from `research/rss/`. Yesterday's digest
  (`research/digest/2026-05-05-digest.md`) explicitly notes:
  *"RSS: Latest available 2026-04-27 (downstream from primary research files)"*.
  The digest's official-announcement section is currently sourced almost
  entirely from Twitter screenshots and HN votes — official-blog primary
  sourcing is missing.

### 2. Bluesky pipeline 403'd since at least 2026-04-26

- `research/bluesky/2026-04-26.md` through `research/bluesky/2026-05-05.md`
  are all stubs containing the same line:
  *"all source files in `data/bluesky/` returned HTTP 403 Forbidden from the
  Bluesky API fetch step"*.
- Verified live: `https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts`
  returns **403 Forbidden** from BunnyCDN-JP (text/html, not JSON), while the
  direct AppView at `https://api.bsky.app/xrpc/app.bsky.feed.searchPosts`
  returns **200 OK** with valid JSON. This appears to be a recently-imposed
  edge block on the public CDN host, not a credentialing issue.

### 3. No early-warning on data-source regressions

- The pattern `curl ... 2>/dev/null || echo "<rss></rss>"` silently substitutes
  an empty feed on failure, so a multi-week silent regression looks identical
  to a quiet news cycle. The Bluesky 403 is the canonical example: ten
  consecutive days of "no posts available" with no Actions warning.

## Improvements Made

### `.github/workflows/2h-bluesky.yml`

- **Switched hostname**: `public.api.bsky.app` → `api.bsky.app` (the AppView
  that still serves unauthenticated public-data XRPC calls).
- **Added 4 new search axes**: `agent framework tool-use`, plus posts from
  `simonwillison.net`, `emollick.bsky.social`, `natolambert.bsky.social`
  (top AI-discussion accounts on Bluesky).
- **Replaced silent fallback** with a `fetch_bsky` helper that validates HTTP
  status and JSON shape, emits `::warning::` annotations on failure, and
  writes a valid empty stub for downstream parsing. Failures will now show
  up in the Actions tab and in workflow run summaries.
- Updated the Claude prompt to enumerate the new files and to explicitly
  mark `{"posts":[]}` as a known failure-mode signal to skip silently.

### `.github/workflows/hourly-rss.yml`

- **Removed 3 dead feeds**: `openrss.org/www.anthropic.com/news`,
  `googleaiblog.blogspot.com/atom.xml`, `ai.meta.com/blog/rss/`.
- **Added live Anthropic mirror**:
  `raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml`
  and `feed_anthropic_engineering.xml` — community-maintained feeds, refreshed
  hourly. Verified 2026-05-06: news feed has `lastBuildDate Wed, 06 May 2026
  01:10:10 +0000` with current items ("Agents for financial services" matches
  yesterday's HN top story).
- **Replaced Google AI Blogspot with `blog.google/technology/ai/rss/`** plus
  `research.google/blog/rss/` (kept) and `deepmind.google/blog/rss.xml` (new).
- **Added arXiv cs.CL** (NLP) alongside the existing cs.AI and cs.LG.
- **Added 5 high-signal commentary feeds**:
  - `simonwillison.net/atom/everything/` (Simon Willison)
  - `importai.substack.com/feed` (Jack Clark / Import AI)
  - `marktechpost.com/feed/` (Marktechpost)
  - `bair.berkeley.edu/blog/feed.xml` (Berkeley AI Research)
  - `technologyreview.com/feed/` (MIT Technology Review)
- **Replaced silent fallback** with a `fetch_feed` helper that validates
  HTTP 200, body size > 200 bytes, and the presence of `<item>` or `<entry>`,
  and emits `::warning::` annotations otherwise.
- Updated the Claude prompt to cover the new section structure (Frontier-Lab
  / Commentary / Press & Analysis), to skip empty-stub feeds, and to filter
  Verge/Marktechpost output for AI relevance (those feeds carry non-AI items).

## Expected Impact

- **RSS pipeline back online**: Anthropic news and Google AI announcements
  will once again flow into `research/rss/<date>.md` and downstream into
  `research/digest/<date>-digest.md`. The 9-day gap should close on the
  next hourly run after merge.
- **Bluesky pipeline back online**: `research/bluesky/<date>.md` will go from
  10 consecutive empty-stub days to actual curated posts from Karpathy,
  Simon Willison, Ethan Mollick, Nathan Lambert, plus 5 search axes.
- **Source breadth**: RSS adds 7 new feeds (2 Anthropic, 1 cs.CL, 5
  commentary). Bluesky adds 4 new accounts/queries. Combined, the daily
  digest should pick up commentary signals (Simon Willison's takes, Import
  AI's policy coverage) that currently only surface via HN front-page votes.
- **Visibility on regressions**: `::warning::` annotations in the Actions UI
  will surface dead feeds and 403'd APIs immediately, instead of letting them
  fester for weeks.

## Caveats

- Anthropic mirror depends on a third-party repo (`Olshansk/rss-feeds`).
  If it lapses, the `fetch_feed` validator will surface the failure as a
  warning. Revisit if Anthropic ships an official feed.
- No working Meta AI feed identified during search (ai.meta.com has no
  `/rss`, `/feed`, or `/atom.xml`; OpenRSS is unreachable; rsshub returns
  403). Meta AI announcements continue to come from press coverage
  (TechCrunch / VentureBeat) and Twitter. Filed as a follow-up.
- Yesterday's improve branch (`improve/2026-05-05`) hit a "GitHub App lacks
  `workflows` permission" wall when pushing edits to `.github/workflows/`.
  If the same wall blocks this PR, only the patch file and this
  `IMPROVEMENTS.md` will land, and a maintainer with that permission will
  need to apply `PROPOSED_WORKFLOW_CHANGES.patch` manually:

  ```bash
  git apply PROPOSED_WORKFLOW_CHANGES.patch
  git add .github/workflows/2h-bluesky.yml .github/workflows/hourly-rss.yml
  git commit -m "Apply improve/2026-05-06 workflow patch"
  ```

## Verification Done Pre-Push

| Check                                                       | Result          |
|-------------------------------------------------------------|-----------------|
| `curl https://api.bsky.app/xrpc/.../searchPosts?...`        | 200 OK, JSON    |
| `curl https://public.api.bsky.app/...` (old host)           | 403 Forbidden   |
| `curl https://openai.com/news/rss.xml`                      | 200             |
| `curl https://blog.google/technology/ai/rss/`               | 200             |
| `curl https://research.google/blog/rss/`                    | 200             |
| `curl https://deepmind.google/blog/rss.xml`                 | 200             |
| `curl https://huggingface.co/blog/feed.xml`                 | 200             |
| `Olshansk/rss-feeds/.../feed_anthropic_news.xml`            | 200, fresh      |
| `curl https://export.arxiv.org/rss/cs.CL`                   | 200             |
| `curl https://simonwillison.net/atom/everything/`           | 200             |
| `curl https://importai.substack.com/feed`                   | 200             |
| `curl https://www.marktechpost.com/feed/`                   | 200             |
| `curl https://bair.berkeley.edu/blog/feed.xml`              | 200             |
| `curl https://www.technologyreview.com/feed/`               | 200             |
| `curl https://openrss.org/www.anthropic.com/news` (removed) | 000 (timeout)   |
| `curl https://ai.meta.com/blog/rss/` (removed)              | 404             |
