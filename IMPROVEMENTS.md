# Methodology Improvements — 2026-05-08

## Issues Found

### 1. Bluesky digest is empty: `public.api.bsky.app` returning HTTP 403
Yesterday's `research/bluesky/2026-05-07.md` contained only:

> "all five pre-fetched data files (ai_announcements, llm_releases,
> model_discussions, ml_papers, karpathy) returned an identical 403
> Forbidden HTML response instead of JSON"

Verified live from this runner:

```
$ curl -o /dev/null -w "%{http_code}\n" \
    "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI&limit=2&sort=latest"
403

$ curl -o /dev/null -w "%{http_code}\n" \
    "https://api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI&limit=2&sort=latest"
200
```

Bluesky has tightened anonymous access on the `public.*` host but
`api.bsky.app` still serves these endpoints unauthenticated. We've been
silently producing zero-signal Bluesky digests since the change.

### 2. RSS workflow: broken Meta AI feed (HTTP 404)
`https://ai.meta.com/blog/rss/` → 404. Every hourly run was spending one
curl on a dead source. Replaced with `https://engineering.fb.com/feed/`
(Engineering at Meta — covers FAIR, PyTorch, Llama infrastructure, and
ranking systems).

### 3. RSS workflow: "DeepMind" slot was actually Google Research
The `deepmind.xml` slot was fetching `https://research.google/blog/rss/`,
which is the Google Research blog, not DeepMind. The real DeepMind feed
is at `https://deepmind.com/blog/feed/basic` (verified 200, currently
headlined with the AlphaEvolve drop that trended on HN today). Both
feeds now exist as separate slots (`google_research.xml` + `deepmind.xml`).

### 4. Coverage gap: high-signal AI newsletters
Our own digests routinely cite Simon Willison's live blogs, smol-ai's
AINews, and Nathan Lambert's Interconnects as primary sources — but the
RSS workflow wasn't pulling them. We were re-discovering them via HN/X
each cycle instead of catching them at publish time.

### 5. Coverage gap: Hugging Face Daily Papers
The arXiv firehose (cs.AI + cs.LG) has very high noise. Hugging Face's
human-curated Daily Papers list is one of the highest-precision filters
available; an unofficial RSS exists at `https://papers.takara.ai/api/feed`
(verified 200, refreshes daily).

## Changes Made

> **Token-permission note.** The `daily-improve` GitHub App that opens
> these PRs does not hold the `workflows` permission needed to push
> edits to files under `.github/workflows/`. The patch is therefore
> attached as `improvements/2026-05-08-workflow-fixes.patch` and must
> be applied manually by a maintainer:
>
> ```bash
> git checkout main
> git apply improvements/2026-05-08-workflow-fixes.patch
> git commit -am "Apply 2026-05-08 RSS + Bluesky workflow fixes"
> ```
>
> The same constraint affected yesterday's PR (`improve/2026-05-07`),
> which carried `improvements/2026-05-07-workflow-fixes.patch` with a
> superset-compatible Bluesky fallback. Today's patch supersedes it.

### `.github/workflows/2h-bluesky.yml`
- Switched from `public.api.bsky.app` → `api.bsky.app` for `searchPosts`.
- Replaced the single `searchPosts(from:karpathy)` author probe with a
  loop over **9 verified AI researcher / lab handles** using
  `getAuthorFeed`, which is more reliable for handle-anchored queries
  (`karpathy`, `simonwillison.net`, `ylecun`, `goodfellow`, `soumith`,
  `anthropic.com`, `openai.com`, `deepmind.google`, `huggingface`).
- Added explicit handling instructions for the `getAuthorFeed` shape
  (`feed[].post.*`) and for skipping reposts (items with `feed[].reason`).
- Added graceful-skip behavior for empty / errored JSON files instead
  of failing the whole digest.

### `.github/workflows/hourly-rss.yml`
- Removed broken Meta AI feed; replaced with Engineering at Meta.
- Restored real DeepMind feed; kept Google Research as a separate slot.
- Added 6 newsletter feeds: Simon Willison, Import AI, smol-ai/AINews,
  Interconnects, Last Week in AI, One Useful Thing.
- Added Hugging Face Daily Papers (curated paper feed).
- Added MarkTechPost (model/research-release coverage).
- Refactored 11 inline `curl` invocations into a single `fetch()` helper
  with a 15-second timeout — readable, diff-friendly source list.
- Updated the Claude prompt with the new feed inventory and added a
  "Newsletters & Analysis" output section so commentary doesn't get
  mixed into "Company Announcements".

## Expected Impact

| Symptom yesterday                          | Expected after this PR                                    |
|--------------------------------------------|-----------------------------------------------------------|
| Bluesky digest = "all five files 403"      | Live Bluesky search + 9 author feeds via api.bsky.app     |
| `Meta AI` slot = empty XML stub each hour  | Engineering at Meta posts (FAIR, PyTorch, Llama)          |
| AlphaEvolve / DeepMind drops missed        | DeepMind blog now its own feed                            |
| Newsletters surfaced via HN, day-late      | Newsletters captured at publish time, hourly              |
| arXiv-only paper coverage (very noisy)     | HF Daily Papers gives a curated complement                |

Net: ~7 net-new sources, 1 broken feed retired, 1 mis-aliased feed
fixed, 1 deprecated host swapped — without changing the schedule, the
runner footprint, or the downstream digest format.
