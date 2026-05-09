# Methodology Improvements — 2026-05-09

> **Carry-forward note.** Yesterday's improve PR (`improve/2026-05-08`,
> "Methodology improvements for 2026-05-08 (docs + patch)") proposed
> the same Bluesky + RSS workflow fixes documented here, but is **not
> yet merged** to `main`. As a result both pipelines are still broken
> on `main`:
>
> - `research/bluesky/2026-05-08.md` carries the same single-line "all
>   five files 403" stub as the prior 4 days.
> - `research/rss/` has produced no commits since `2026-04-27 09:18 UTC`
>   — the broken upstreams cause every hourly run to write the same
>   "No new updates this hour" snapshot, which `git commit` correctly
>   refuses to push as a no-op.
>
> Today's patch is a strict superset of yesterday's: identical Bluesky
> and RSS hunks plus a new fix for the Reddit-metric gap (issue #3
> below). If yesterday's PR merges first, today's PR's Bluesky/RSS
> hunks will collapse to a no-op rebase and only the new Reddit hunk
> will land.

## Issues Found

### 1. Bluesky digest empty: `public.api.bsky.app` returning HTTP 403 (CARRY)
Yesterday's `research/bluesky/2026-05-08.md` is again a one-line stub:

> "all five pre-fetched data files (ai_announcements, llm_releases,
> model_discussions, ml_papers, karpathy) returned an identical 403
> Forbidden HTML response instead of JSON"

Re-verified live from the runner:

```
$ curl -o /dev/null -w "%{http_code}\n" \
    "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI&limit=2&sort=latest"
403

$ curl -o /dev/null -w "%{http_code}\n" \
    "https://api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI&limit=2&sort=latest"
200
```

Bluesky has tightened anonymous access on the `public.*` host but
`api.bsky.app` still serves these endpoints unauthenticated. Until
the workflow swap lands, every run produces zero-signal Bluesky.

### 2. RSS workflow silent since 2026-04-27 (CARRY + escalation)
Last commit on `research/rss/` was `90f15f30 RSS update 2026-04-27
09:18 UTC` — twelve days ago. Probed each upstream from the runner:

| Upstream                                            | HTTP | Items |
|-----------------------------------------------------|-----:|------:|
| `https://openai.com/news/rss.xml`                   | 200  | 20+   |
| `https://huggingface.co/blog/feed.xml`              | 200  | 20+   |
| `https://techcrunch.com/category/.../feed/`         | 200  | 20    |
| `https://www.theverge.com/rss/.../index.xml`        | 200  | 10    |
| `https://venturebeat.com/category/ai/feed/`         | 200  | 7     |
| `http://googleaiblog.blogspot.com/atom.xml`         | 200  | 25    |
| `https://export.arxiv.org/rss/cs.AI`                | 200  | 20+   |
| `https://research.google/blog/rss/` (DeepMind slot) | 200  | **1** |
| `https://openrss.org/www.anthropic.com/news`        | 200  | **0** (HTML body) |
| `https://ai.meta.com/blog/rss/`                     | **404** | — |

So the RSS workflow has been spending two of its eleven curl slots
on dead/empty upstreams every hour for at least 12 days, while
silently swallowing the failures. The DeepMind alias bug means we
also missed the AlphaEvolve drop that trended on HN today (`205 pts /
80 comments`, [DeepMind blog](https://deepmind.google/blog/alphaevolve-impact/)) at publish time.

### 3. Reddit table promises Score/Comments columns it can never fill (NEW)
`research/community/2026-05-08-reddit.md` contains 50+ rows like:

| Title                                            | Score | Comments | Link |
|--------------------------------------------------|-------|----------|------|
| People Interested in Continual Learning Research | —     | —        | reddit |
| Disillusionment with mech interp research [D]    | —     | —        | reddit |
| Gemma 4 26B Hits 600 Tok/s on One RTX 5090       | —     | —        | reddit |

The note at the top of the file acknowledges the cause:

> *Reddit Atom feeds expose post titles/links/timestamps but not
> score or comment counts; metric columns are marked "—". Rank
> reflects feed "hot" order. Filtered to remove memes, sticky/megathreads,
> and beginner help.*

Two structural problems:

1. **Real signal is being thrown away.** The Atom entries do contain
   `<author><name>` (the OP) and `<published>` (UTC ISO 8601) — both
   are useful for triage and both are currently dropped on the floor.
2. **The output prompt's `SKIP: posts with <10 score` filter is a
   no-op** because there are no scores to compare against — so it
   reads as if filtering happened when it didn't.

Adding Reddit OAuth (which would expose real scores) is out of scope
— it requires a new secret and rate-limit budget. The cheap fix is
to stop promising metrics we can't measure and replace those columns
with `Posted (UTC)` + `Author`, which the current data source already
provides. The workflow's prompt is also updated to filter on title
content rather than imaginary scores.

### 4. Meta-issue: improve PRs blocked by missing `workflows: write`
The `daily-improve` GitHub App that opens these PRs runs without
the `workflows` permission, so any change under `.github/workflows/`
must be shipped as a `.patch` file for a maintainer to apply
manually:

```bash
git checkout main
git apply improvements/2026-05-09-workflow-fixes.patch
git commit -am "Apply 2026-05-09 RSS + Bluesky + Reddit workflow fixes"
```

This means each daily run that finds a workflow bug stacks a fresh
patch on top of every previous unmerged one. The 2026-05-07 patch
was superseded by 2026-05-08's; 2026-05-08's is now superseded by
this one. **Resolving this for real requires a one-time human edit
to `.github/workflows/daily-improve.yml`** — adding `workflows:
write` under that workflow's `permissions:` block — which by
construction the bot itself cannot make. Flagging here so it's not
re-discovered on 2026-05-10.

## Changes Made

### `.github/workflows/2h-bluesky.yml` (CARRY)
- Switch from `public.api.bsky.app` → `api.bsky.app` for `searchPosts`.
- Replace single `searchPosts(from:karpathy)` author probe with a
  loop over **9 verified AI researcher / lab handles** using
  `getAuthorFeed` (more reliable for handle-anchored queries):
  `karpathy`, `simonwillison.net`, `ylecun`, `goodfellow`, `soumith`,
  `anthropic.com`, `openai.com`, `deepmind.google`, `huggingface`.
- Add explicit handling instructions for the `getAuthorFeed` shape
  (`feed[].post.*`) and skip reposts (items with `feed[].reason`).
- Graceful-skip behavior for empty / errored JSON files instead of
  failing the whole digest.

### `.github/workflows/hourly-rss.yml` (CARRY)
- Remove broken Meta AI feed; replace with **Engineering at Meta**.
- Restore real DeepMind feed; keep Google Research as a separate slot.
- Add 6 newsletter feeds: **Simon Willison**, **Import AI**, **smol-ai
  AINews**, **Interconnects**, **Last Week in AI**, **One Useful Thing**.
- Add **Hugging Face Daily Papers** (curated daily-papers feed).
- Add **MarkTechPost** (model/research-release coverage).
- Refactor 11 inline `curl` invocations into a single `fetch()` helper
  with a 15-second timeout — readable, diff-friendly source list.
- Update Claude prompt with new feed inventory; add a "Newsletters &
  Analysis" output section so commentary doesn't mix into "Company
  Announcements".

### `.github/workflows/4h-community.yml` (NEW today)
- Replace Reddit `Score | Comments` columns with `Posted (UTC) | Author`
  in all three subreddit tables — both columns are populated from
  fields already in the Atom feeds.
- Document the parsing of `<author><name>` and `<published>` in the
  prompt; add an explicit "Reddit RSS does NOT expose scores — do
  not invent metrics" note so future runs don't silently regress.
- Replace the no-op `SKIP: posts with <10 score` filter with title-content
  filters (memes, AutoModerator/sticky, recurring "Self-Promotion
  Thread" / "Job Postings" / "[Conf] Decisions" threads).

## Expected Impact

| Symptom yesterday                          | Expected after this PR                                    |
|--------------------------------------------|-----------------------------------------------------------|
| Bluesky digest = "all five files 403"      | Live Bluesky search + 9 author feeds via api.bsky.app     |
| RSS pipeline silent for 12 days            | 18 working feeds, dead Meta + empty Anthropic mirrors retired |
| AlphaEvolve / DeepMind drops missed at publish time | DeepMind blog now its own slot                   |
| Newsletters surfaced via HN, day-late      | Newsletters captured at publish time, hourly              |
| arXiv-only paper coverage (very noisy)     | HF Daily Papers gives a curated complement                |
| Reddit table = 50+ rows of "Score: —"      | Reddit table shows actual Posted (UTC) + Author per row   |
| `SKIP: <10 score` filter is a lie          | Replaced with content-based filters that actually run     |

Net: **2 broken sources retired, 1 mis-aliased source corrected, 1
deprecated host swapped, 7 net-new RSS sources**, and **Reddit output
now carries real per-row metadata** instead of two columns of em-dashes
— without changing the schedule, runner footprint, or downstream
digest format.

## How to apply

```bash
git checkout main
git apply improvements/2026-05-09-workflow-fixes.patch
git diff --stat HEAD     # 3 files changed: 2h-bluesky.yml, hourly-rss.yml, 4h-community.yml
git commit -am "Apply 2026-05-09 RSS + Bluesky + Reddit workflow fixes"
git push
```

Patch was generated from a clean apply against `main` at HEAD
`22a56061` and re-verified with `git apply --check` before commit.
