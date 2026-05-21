# Methodology Improvements — 2026-05-21

## Summary

Yesterday's pipeline (2026-05-20) was healthy across nearly every lane —
the digest, ai-news sweep, HN/Reddit community pulls, arXiv curation,
Twitter cycles, and model-timeline diff were all rich and well-sourced.
The one structural gap worth fixing: the **RSS lane has no independent
analyst / research-aggregator layer**. Its only non-lab feeds are
general tech-news outlets (TechCrunch, The Verge, VentureBeat), so
high-signal independent commentary and research-news roundups never
reach the digest synthesizer through RSS.

This PR adds three feeds to `hourly-rss.yml` to close that gap.

## ⚠ Push blocked — workflow edit shipped as a patch, not a file diff

The `hourly-rss.yml` edit was written, validated, and committed locally,
but **could not be pushed**: the `claude[bot]` GitHub App still lacks the
`workflows: write` permission, so the remote rejects any branch that
touches `.github/workflows/*`:

```
! [remote rejected] improve/2026-05-21 -> improve/2026-05-21
  (refusing to allow a GitHub App to create or update workflow
   `.github/workflows/hourly-rss.yml` without `workflows` permission)
```

This is the **same blocker documented on 2026-05-18 (item #3)**, whose
out-of-band action item — grant the App `workflows: write` — was evidently
never completed. So this branch carries the workflow change as an
**applyable patch** (`docs/archive/2026-05-21-hourly-rss.patch`) plus the
inline diff below, rather than the edited workflow file itself.

**To land the change, a maintainer must either:**

1. `git apply docs/archive/2026-05-21-hourly-rss.patch` from the repo root
   and commit (a human push isn't subject to the App restriction); **or**
2. Grant the `claude[bot]` App `workflows: write` in the repo's
   App-installation settings, after which a future `daily-improve` run can
   push workflow edits directly.

## What I reviewed

- `research/digest/2026-05-20-digest.md` — comprehensive; sources line
  noted Perplexity quota exhausted (a billing issue, not workflow-fixable).
- `research/2026-05-20-ai-news.md`, `research/arxiv/2026-05-20-papers.md`,
  `research/community/2026-05-20-{hn,reddit}.md`, `research/twitter/2026-05-20.md`,
  `research/models/2026-05-20-timeline.md` — all healthy, no churn warranted.
- `research/bluesky/2026-05-20.md` — thin (4 posts from 2 of 14 handles),
  but the Bluesky lane was just overhauled on 2026-05-18 (switch to
  `getAuthorFeed`, curated handle list, lowered engagement gate). The
  thin output reads as base-rate variance on a quiet day, not a
  regression, so I left it alone rather than re-churn a 3-day-old fix.
- `.github/workflows/hourly-rss.yml` and the rest of the workflow set.

## Issue found: no independent-analysis source in the RSS lane

The RSS feed list covered:

- Lab blogs: OpenAI, Anthropic, Google AI, DeepMind/Google Research, Hugging Face
- Research: arXiv cs.AI, cs.LG
- Tech news: TechCrunch, The Verge, VentureBeat

Missing entirely: the **independent expert / research-aggregator layer**.
The 2026-05-20 digest itself flagged Simon Willison's "last six months in
LLMs in five minutes" as "the day's best single read" — yet that class of
source had no path into the pipeline via RSS.

## Changes made

Added three feeds to `.github/workflows/hourly-rss.yml`, each wired into
all three places the workflow needs them: the fetch step (with the
existing graceful `|| echo "<rss></rss>"` fallback so a bad URL is
non-fatal), the Claude prompt's source-file list, and the output format.

| Feed | URL | Why |
|---|---|---|
| **Simon Willison's Weblog** | `https://simonwillison.net/atom/everything/` | Canonical independent LLM observer; daily-ish cadence; repeatedly cited in our own digests as the best single read. |
| **MarkTechPost** | `https://www.marktechpost.com/feed/` | High-volume daily AI research/news aggregator — surfaces new papers, model releases, and open-source drops. |
| **Ars Technica AI** | `https://arstechnica.com/ai/feed/` | Quality long-form tech journalism; complements the existing TechCrunch/Verge/VentureBeat trio. |

Output now has a new **🔬 Independent & Analysis** section (Simon
Willison + MarkTechPost) plus Ars Technica under **📰 Tech News**.

The full diff (also saved as `docs/archive/2026-05-21-hourly-rss.patch`):

```diff
@@ fetch step @@
+          # Ars Technica AI RSS (section feed)
+          curl -sL "https://arstechnica.com/ai/feed/" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/arstechnica_ai.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/arstechnica_ai.xml
+
+          # Simon Willison's Weblog (Atom)
+          curl -sL "https://simonwillison.net/atom/everything/" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/simonwillison.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/simonwillison.xml
+
+          # MarkTechPost
+          curl -sL "https://www.marktechpost.com/feed/" \
+            -H "User-Agent: Mozilla/5.0 (compatible; AIResearchBot/1.0)" \
+            > /tmp/rss/marktechpost.xml 2>/dev/null || echo "<rss></rss>" > /tmp/rss/marktechpost.xml

@@ prompt source list @@
+            - arstechnica_ai.xml (Ars Technica AI)
+
+            **Independent & Analysis:**
+            - simonwillison.xml (Simon Willison's Weblog — Atom)
+            - marktechpost.xml (MarkTechPost — AI research/news aggregator)

@@ output format @@
+            #### Ars Technica
+            - [Title](url) - date
+
+            ### 🔬 Independent & Analysis
+            #### Simon Willison
+            - [Title](url) - date
+            #### MarkTechPost
+            - [Title](url) - date
```

## Validation

- `python3 -c "import yaml; yaml.safe_load(...)"` → YAML parses clean.
- Canonical feed URLs confirmed via web research. **Note:** this runner's
  sandbox blocks outbound `curl`/WebFetch, so the feed endpoints could not
  be HTTP-probed from here (unlike the 2026-05-18 pass). The risk is
  bounded: the workflow's per-feed `|| echo "<rss></rss>"` fallback means
  any URL that 404s or moves simply yields no items rather than breaking
  the run. If a feed is dead on the first scheduled run, the fetch log
  will show it and it can be swapped or dropped.

## What was deliberately not changed

- **Bluesky** — just fixed 2026-05-18; thin 2026-05-20 output is within
  normal variance. Watch, don't churn.
- **Twitter / HN / Reddit / arXiv / digest / model-timeline / front-page**
  — all producing healthy daily output.
- **Perplexity quota** — recurring "quota exhausted" note in the digest
  sources is an account/billing intervention, not a workflow edit.
- **Frontier-lab competitor blogs** (Mistral, xAI, DeepSeek, Cohere) —
  considered, but their RSS endpoints could not be verified from this
  sandbox and they publish rarely; deferred rather than guess at URLs.

## Files changed

- `.github/workflows/hourly-rss.yml` — **change captured as a patch, not
  pushed** (see "Push blocked" above). Apply via
  `docs/archive/2026-05-21-hourly-rss.patch`.
- `docs/archive/2026-05-21-hourly-rss.patch` (applyable workflow diff)
- `docs/archive/2026-05-21-improvements.md` (this file)
