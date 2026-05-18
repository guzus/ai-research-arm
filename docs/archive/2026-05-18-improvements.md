# Methodology Improvements — 2026-05-18

## Why this PR changes workflows

This PR now carries the workflow edits described below instead of only
documenting a blocked local branch. The earlier docs-only framing was
not actionable for maintainers because the referenced local
`improve/2026-05-18` branch was not available on GitHub.

One operational step still cannot be represented as a file diff:
`hourly-rss.yml` is currently disabled manually in GitHub Actions and
must be re-enabled after this PR lands if hourly RSS output should resume.

---

Two long-running source failures in the aggregation lane, plus the
meta-failure that hid workflow-edit push failures.

## 1. Bluesky pipeline: 30+ days of empty digests

### Issue

Every `research/bluesky/YYYY-MM-DD.md` from at least **2026-04-15 through
2026-05-17** is a single-line failure stub — same pattern, same five files
returning HTTP 403:

> _No posts processed: all five pre-fetched source files in `data/bluesky/`
> returned HTTP 403 Forbidden HTML pages instead of Bluesky JSON. Upstream
> fetch failed for `ai_announcements.json`, `llm_releases.json`,
> `model_discussions.json`, `ml_papers.json`, and `karpathy.json`._

### Root cause

The fetch step calls `app.bsky.feed.searchPosts` on `public.api.bsky.app`.
That endpoint now requires authentication — Bluesky locked it down to
combat scraper load. Reproduced today from this runner:

```
no-headers:            HTTP 403
with UA + Accept:      HTTP 403
```

No header massaging makes it work. `app.bsky.feed.getAuthorFeed`, by
contrast, still returns `200` without auth. See
[bsky-docs#332](https://github.com/bluesky-social/bsky-docs/issues/332)
and related issues.

### Fix

Rewrote `.github/workflows/2h-bluesky.yml`:

- **Replaced 4 keyword searches** (`AI announcement`, `LLM release`,
  `GPT Claude Gemini`, `machine learning paper`) **with `getAuthorFeed`
  pulls on a curated list of 14 AI researcher / org handles**, each
  individually verified reachable via `getProfile` today:
  karpathy, emilymbender, mmitchell, huggingface, deeplearning,
  rasbt, jeremyhoward, yoavgo, swyx, simonw, hardmaru, moyix,
  arankomatsuzaki, schmidhuber (all `.bsky.social`).
- Per-handle HTTP status is logged; non-2xx responses are replaced with
  `{"feed":[]}` so the downstream Claude step never trips on an HTML
  error page.
- Updated the Claude prompt to match the new shape (`feed[].post.*`
  rather than `posts[].*`) and to skip pure reposts.
- Lowered the engagement gate from `>5 likes` to `>=2 likes OR >=1
  repost` — for a curated technical handle list, Bluesky's smaller
  AI audience makes the old threshold too aggressive.
- Removed the copied `data/bluesky/` inputs before the rebase/push loop.
  These files are transient Claude inputs, not publish artifacts; leaving
  them untracked can make `git pull --rebase` fail with "unstaged changes."
- Left a hook in the comments: if we ever add
  `BLUESKY_HANDLE` / `BLUESKY_APP_PASSWORD` secrets and a session-token
  step, the keyword-search lane can be restored.

### Expected impact

End the 30+ day stretch of empty Bluesky digests; downstream
`daily-digest.yml` regains a real Bluesky source line (currently shows
`Bluesky: upstream 403 — no data this cycle`).

## 2. RSS pipeline: 21 days of zero output

### Issue

`research/rss/` jumps from `2026-04-27.md` straight to nothing — **no daily
RSS file written for 2026-04-28 through 2026-05-17**.

### Root cause

The feeds themselves are mostly healthy — probed today:
```
openai: 200  anthropic: 200  google_ai: 200  deepmind: 200
huggingface: 200  arxiv_ai: 200  arxiv_lg: 200
techcrunch: 200  verge: 200  venturebeat: 200
meta_ai: 404   ← removed
```

The primary operational cause is that the GitHub Actions workflow is
disabled manually. GitHub currently reports `.github/workflows/hourly-rss.yml`
as `disabled_manually`, and the latest runs are from 2026-04-27. A file
change alone cannot restart scheduled RSS collection; the workflow must
be re-enabled in Actions after this PR lands.

There is also a workflow-quality issue worth fixing before re-enabling:
the prompt told the agent "If no new content, write 'No new updates this
hour'" but did not explicitly require creating the daily file when it was
missing. That made missing files harder to distinguish from quiet news
hours.

### Fix

Edited `.github/workflows/hourly-rss.yml`:

- **Dropped the Meta AI Blog feed** (404). Left commented in place so
  the next probe is one `curl` away if Meta restores it.
- **Reworded the "no new updates" rule** to explicitly require creating
  the file with its header and appending a timestamped `_No new updates
  this hour._` section. This converts the prior silent failure into a
  visible heartbeat — and means a future missing daily file is a real
  signal that the workflow itself isn't running.
- Kept the rebase/push retry loop loud: if publishing fails, the workflow
  should fail instead of hiding the problem.

### Action required

After merging, re-enable **Hourly RSS Official Announcements** in GitHub
Actions, or run:

```
gh workflow enable hourly-rss.yml --repo guzus/ai-research-arm
```

### Expected impact

Once the workflow is re-enabled, `research/rss/YYYY-MM-DD.md` should
exist for every UTC day going forward, even on slow news days.
Re-establishes the RSS source line for the daily digest synthesizer.

## 3. daily-improve.yml: PR push silently swallowed

### Issue

`docs/archive/` contains only **2 improvement docs** (2026-01-14,
2026-02-01) despite `daily-improve.yml` running every day for ~4
months. The agent runs and produces a branch, but the push step
catches the failure with `|| echo "Already pushed or no changes"`,
so a real auth failure looks identical to an idempotent no-op.

### Root cause

The `claude[bot]` GitHub App installation may not hold the `workflows`
permission. Pushes from the Claude GitHub App token that touch a
`.github/workflows/*` file can be rejected with:

```
! [remote rejected]   improve/2026-05-18 -> improve/2026-05-18
  (refusing to allow a GitHub App to create or update workflow
   `.github/workflows/2h-bluesky.yml` without `workflows` permission)
```

The `|| echo "Already pushed..."` line then prints success and the job
ends green, making a real push failure look like an idempotent no-op.

Note: this is an **App-installation-level permission** in the
`claude[bot]` App's repository-permissions page — it is **not**
settable from the workflow YAML's `permissions:` block.

### Fix

- Removed the `|| echo "Already pushed or no changes"` swallow in
  `.github/workflows/daily-improve.yml` so the next failure surfaces
  red instead of green. A real "nothing to push" outcome exits 0
  naturally; only auth / workflows-permission / network failures
  will exit non-zero, which is what we want to see.
- Added a comment on the `permissions:` block documenting the
  App-installation requirement so the next reviewer doesn't waste
  time trying to "fix" it from the YAML.
- Fixed the staging example so it points at `docs/archive/...` instead
  of the archived repo-root `IMPROVEMENTS.md` path.

### Action required (out of band)

Grant the **claude[bot] GitHub App** the `workflows: write` permission
in this repo's App-installation settings if daily-improve still cannot
push branches that touch workflow files. Once granted, this same daily
job will be able to publish improvement PRs that touch workflow files.

## What was deliberately not changed

- **Twitter, Hacker News, Reddit, arXiv, models-timeline, digest,
  front-page, audio-digest** are all producing healthy daily output —
  no churn warranted.
- **Perplexity quota** flagged itself in the 2026-05-17 digest sources
  ("Perplexity API quota exhausted; WebSearch used as primary backstop").
  Worth watching but not actionable in a workflow edit — needs an account
  / billing intervention.

## Files changed

- `.github/workflows/2h-bluesky.yml`
- `.github/workflows/hourly-rss.yml`
- `.github/workflows/daily-improve.yml`
- `docs/archive/2026-05-18-improvements.md` (this file)
