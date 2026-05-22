# Methodology Improvements — 2026-05-22

## Summary

Yesterday's pipeline (2026-05-21) was healthy across every synthesis and
aggregation lane **except Bluesky**, which produced only **2 posts** —
down from 4 the day before. That makes **two consecutive thin days**,
which crosses from base-rate variance into a trend and **revises the
2026-05-21 "watch, don't churn" call** on this lane. The digest itself
flagged the weakness in its own sources line: *"Bluesky: 1 feed
snapshot."*

This PR ships a minimal, safe Bluesky fix as an **applyable patch**
(`docs/archive/2026-05-22-bluesky.patch`) and escalates the recurring
delivery blocker that has now kept **four** consecutive days of workflow
improvements from landing.

## ⚠ Recurring blocker (now 4 days running) — `workflows: write`

Every meaningful lever for the issues below lives in `.github/workflows/*`,
and the `claude[bot]` GitHub App still lacks `workflows: write`, so any
branch that edits a workflow file is rejected on push:

```
! [remote rejected] improve/<date> -> improve/<date>
  (refusing to allow a GitHub App to create or update workflow
   `.github/workflows/<file>.yml` without `workflows` permission)
```

Documented as an open item on **2026-05-18 (#3)**, **2026-05-20**, and
**2026-05-21**, and still unresolved. The cost is now visible: the
2026-05-21 RSS-feed improvement was committed only as a patch and
**never applied** — the live `hourly-rss.yml` still has no
independent-analysis feeds (verified: `grep -c simonwillison
.github/workflows/hourly-rss.yml` → 0).

**This is the #1 action item.** Until a maintainer either grants the App
`workflows: write` or applies the accumulated patches by hand, the
daily-improve loop can only *describe* workflow fixes, not ship them.

## What I reviewed

| Lane | File | Verdict |
|---|---|---|
| Digest | `research/digest/2026-05-21-digest.md` (11 KB) | Excellent — comprehensive, well-sourced. |
| AI-news sweep | `research/2026-05-21-ai-news.md` (14 KB) | Healthy. |
| Twitter | `research/twitter/2026-05-21.md` (95 KB) | Healthy. |
| Twitter (DeepSeek) | `research/twitter-deepseek/2026-05-21.md` (107 KB) | Healthy. |
| Reddit | `research/community/2026-05-21-reddit.md` (24 KB) | Healthy. |
| Hacker News | `research/community/2026-05-21-hn.md` (7 KB) | Healthy. |
| RSS | `research/rss/2026-05-21.md` (16 KB) | Healthy (lab + tech-news only; see RSS gap below). |
| arXiv | `research/arxiv/2026-05-21-papers.md` (8 KB) | Healthy. |
| Model timeline | `research/models/2026-05-21-timeline.md` | Healthy (1 ticket updated, 5 unchanged — quiet day). |
| Generative | 2 articles (servicenow-stock, variational-perpdex) | Both validate clean. |
| **Bluesky** | `research/bluesky/2026-05-21.md` (584 B) | **Thin — 2 posts, 2nd thin day.** |

## Issue: Bluesky lane is starved (now a trend, not variance)

The lane fetches author feeds for 14 curated researchers once daily and
filters to a **24-hour window**. AI researchers post to Bluesky
sporadically, so a single daily 24h snapshot of 14 handles frequently
nets fewer than 3 posts:

- **2026-05-21:** 2 posts (mmitchell, emilymbender)
- **2026-05-20:** 4 posts (from 2 of 14 handles)

The 2026-05-21 review left this alone as "variance on a quiet day"
because the lane had just been overhauled on 2026-05-18. A second
consecutive thin day removes that explanation: the structural cause is
**low candidate volume** (narrow window × small, sporadic handle set ×
once-daily cadence), not a quiet news cycle.

### Fix (shipped as a patch)

`docs/archive/2026-05-22-bluesky.patch` makes two minimal, low-risk
changes to `.github/workflows/2h-bluesky.yml`:

1. **Twice-daily cadence** — `cron: '11 0 * * *'` → `'11 0,12 * * *'`.
   Directly addresses the "1 feed snapshot" weakness the digest named;
   two passes ≈ double the candidate posts per day. The existing
   per-date append + engagement gate keep the output deduped and curated.
2. **Window 24h → 48h** in the prompt FILTERS (both INCLUDE and SKIP).
   Roughly doubles the candidate pool per fetch without touching the
   quality gate (`>=2 likes OR >=1 repost` is unchanged).

Both are safe under the workflow's existing graceful design (per-handle
`HTTP != 200 → {"feed":[]}` fallback). The patch was verified with
`git apply --check` → clean.

### Follow-up (not patched — needs curation + verification)

Expanding the 14-handle list is the higher-leverage fix but requires
verifying that candidate handles resolve and post original (non-repost)
AI content. Curated AI-researcher Bluesky starter packs are a good
sourcing ground — see
[blueskystarterpack.com/ai-researchers](https://blueskystarterpack.com/ai-researchers)
(27+ lists) and [blueskystarterpack.com/ai-research](https://blueskystarterpack.com/ai-research).
Deferred rather than guessing at handles that might not exist.

## Still-open from prior runs

- **RSS independent-analysis gap (2026-05-21).** The proposed feeds
  (Simon Willison's Weblog, MarkTechPost, Ars Technica AI) were never
  applied to `hourly-rss.yml`. Web research this run independently
  corroborates the gap: standard 2026 AI-monitoring stacks pair lab
  blogs + arXiv with editorial/aggregator feeds (MIT Technology Review
  AI, BAIR Blog, KDnuggets are common picks). The 2026-05-21 patch
  (`docs/archive/2026-05-21-hourly-rss.patch`) remains valid and should
  be applied alongside the Bluesky patch.
- **Perplexity quota exhausted** (recurring in the digest sources line)
  — an account/billing intervention, not a workflow edit.

## Deliberately not changed

- **Twitter / Twitter-DeepSeek / Reddit / HN / arXiv / digest /
  ai-news / model-timeline** — all producing healthy, substantive daily
  output; no churn warranted.
- **COMPONENTS.md ↔ CSS drift** (CLAUDE.md "Known Drift"). Real, but the
  used-but-undocumented `ara-*` classes (`ara-p`, `ara-link`, `ara-ol`,
  `ara-references`, `ara-stats-dt`, …) appear only in **3 articles dated
  2026-05-16**; yesterday's 2 generative articles validate clean. Not
  tied to yesterday's output, so deferred to a demand-driven fix per the
  CLAUDE.md protocol (document a class when a *real new* article needs it).

## Files in this PR

- `docs/archive/2026-05-22-improvements.md` (this file)
- `docs/archive/2026-05-22-bluesky.patch` (applyable workflow diff,
  `git apply`-verified)

Both are non-workflow files, so this branch pushes without hitting the
`workflows: write` rejection. To land the actual workflow change, a
maintainer runs:

```
git apply docs/archive/2026-05-22-bluesky.patch
git add .github/workflows/2h-bluesky.yml
git commit -m "Bluesky: twice-daily cadence + 48h window"
```
