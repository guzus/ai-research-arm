# Methodology Improvements - 2026-05-10

> **TL;DR for the maintainer:** This is the **6th consecutive daily PR** (since
> 2026-05-05) bundling the same two-line fix that restores the Bluesky digest
> and the hourly RSS pipeline. The fixes have not yet landed on `main` because
> the daily-improve App's `GITHUB_TOKEN` cannot push `.github/workflows/*`
> changes (a GitHub Actions security restriction — see Issue #4 below). The
> patch in `improvements/2026-05-10-workflow-fixes.patch` applies cleanly to
> current `main`. **Please run `git apply improvements/2026-05-10-workflow-fixes.patch`
> on your local clone and push to `main` directly.** Once landed, this PR
> series can stop.

---

## Analysis Date: 2026-05-09 Output Review

### Confirmed Live Failures (re-verified 2026-05-10 00:25 UTC)

#### 1. Bluesky digest is empty — `public.api.bsky.app` returns HTTP 403 (CRITICAL)

- **Symptom:** `research/bluesky/2026-05-09.md` contains a single line:
  > _No posts processed: all pre-fetched Bluesky JSON files (`ai_announcements.json`,
  > `llm_releases.json`, `model_discussions.json`, `ml_papers.json`, `karpathy.json`)
  > returned a 403 Forbidden HTML response from the upstream fetcher rather than
  > valid JSON. The Bluesky API source appears to be blocking the fetch step._
- **Re-verification (2026-05-10 00:25 UTC):**
  - `GET https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI&limit=5` → **HTTP 403** (2,334-byte HTML stub, "Forbidden")
  - `GET https://api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI&limit=5` → **HTTP 200** (12,546 bytes valid JSON) ✅
  - `GET https://api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=karpathy.bsky.social&limit=3` → **HTTP 200** (6,300 bytes valid JSON) ✅
- **Fix in patch:** `2h-bluesky.yml` switches `BSKY_HOST` from `https://public.api.bsky.app`
  → `https://api.bsky.app`, replaces the broken `searchPosts(from:handle)` trick
  with `getAuthorFeed` for 9 known AI handles, and tells the Claude prompt how to
  read both `posts[]` (search) and `feed[]` (author) shapes.
- **Days dark:** ~10 days (Bluesky digests have been empty since early May).

#### 2. Hourly RSS pipeline silently dead — last commit 2026-04-27 09:18 UTC (CRITICAL)

- **Symptom:** `ls research/rss/` shows the most recent file is `2026-04-27.md`.
  `git log --oneline -- research/rss/ | head -1` confirms the last RSS commit was
  `90f15f30 RSS update 2026-04-27 09:18 UTC` — **13 days ago**.
- **Root cause:** The `openrss.org/www.anthropic.com/news` curl in
  `hourly-rss.yml` started taking >2 minutes to respond around 2026-04-27,
  and the original script had no `--max-time`. With `concurrency.cancel-in-progress:
  true`, the next hourly run cancels the previous one before it finishes
  fetching all feeds — so no feeds reach Claude, no markdown is written, no
  commit happens. The job appears to "succeed" with zero output.
- **Fix in patch:** `hourly-rss.yml` wraps every `curl` in a `fetch()` shell
  function with `--max-time 15` so a single slow upstream cannot stall the
  whole job. While we're there, the patch also:
  - Replaces the dead `ai.meta.com/blog/rss/` (404 in 2026) with
    `engineering.fb.com/feed/` (Engineering at Meta — covers FAIR / PyTorch /
    Llama infra).
  - Restores the real DeepMind feed (`deepmind.com/blog/feed/basic`) — the
    prior config had this slot accidentally aliased to `research.google`,
    causing AlphaEvolve / Gemini Deep Research drops to be missed.
  - Adds 7 new high-signal feeds repeatedly cited in our own digests as
    primary sources: **Simon Willison**, **Import AI** (Jack Clark),
    **AINews / smol-ai**, **Interconnects** (Nathan Lambert),
    **Last Week in AI**, **One Useful Thing** (Ethan Mollick),
    and the human-curated **Hugging Face Daily Papers** mirror.
- **Days dark:** 13 days.

#### 3. Reddit digest columns show "—" for every post (HIGH)

- **Symptom:** `research/community/2026-05-09-reddit.md` headers are
  `| Title | Score | Comments | Link |` but every Score / Comments cell is `—`,
  with three explicit notes from Claude saying _"Reddit Atom feeds expose post
  titles/links/timestamps but not score or comment counts; metric columns are
  marked '—'"_. The columns convey zero information across **every Reddit
  post in every cycle**.
- **Root cause:** Reddit's Atom RSS feeds (e.g.
  `https://www.reddit.com/r/MachineLearning/hot.rss`) genuinely do not include
  `<score>` or `<num_comments>` — those fields require the JSON API or a
  scraper. The `4h-community.yml` prompt was written assuming the fields
  exist, and also tells Claude to "SKIP posts with <10 score" — a no-op
  filter, since score is unavailable.
- **Fix in patch:** `4h-community.yml` replaces the Score / Comments columns
  with **Posted (UTC)** (from the entry's `<published>`) and **Author** (from
  `<author><name>` — `/u/handle`), both of which Atom does expose. The
  no-op `<10 score` filter is replaced with a content-based filter
  (`AutoModerator / sticky / Self-Promotion Thread / Job Postings /
  Conference Decisions`).

#### 4. arXiv digest has "(multiple)" for every author (MEDIUM — NEW today)

- **Symptom:** `research/arxiv/2026-05-09-papers.md` lists **17 / 17 paper rows**
  with author field `(multiple)` or `(multiple, see paper)`. The Highlights
  Top 5 and every By-Category table row are unable to attribute work to a
  research group, which makes the digest near-useless for tracking which lab
  shipped what (Anthropic vs DeepMind vs Meta SuperIntelligence Lab vs
  individual academic groups).
- **Root cause:** The `daily-arxiv.yml` Claude prompt template specifies
  `**Authors**: [names]` without telling Claude how to format the list,
  and the surrounding "By Category" tables ask for an `Authors` column
  without bound. `arxiv-mcp-server` returns full author lists in the
  `authors` array of each result, but Claude defaults to the lazy
  `(multiple)` placeholder under length pressure.
- **Fix in patch:** `daily-arxiv.yml` prompt is updated to specify the
  author format explicitly — _"first 3 author surnames + 'et al.' if more —
  e.g. 'Chen, Patel, Yamamoto et al.'; never write '(multiple)' or
  '(see paper)'"_ — and renames the table column to `First Author` so
  the schema is unambiguous. Adds an `AUTHOR EXTRACTION` paragraph at the
  bottom of the format spec citing the field's load-bearing role for
  cross-day de-dup.

#### 5. Structural — daily-improve App lacks `workflows: write` permission (META)

- **Symptom:** This same patch has been bundled in `improvements/*.patch` files
  on the `improve/2026-05-{05,06,07,08,09}` branches but never reaches `main`.
- **Why:** The `GITHUB_TOKEN` issued to a workflow run cannot modify
  `.github/workflows/*` files — this is a GitHub Actions security feature to
  prevent runaway workflow self-modification, and is **not configurable via
  the workflow's `permissions:` block**. (Commit `c1813ee9` previously
  attempted to add `workflows: write` and had to be reverted; it is not a
  valid permission key for `permissions:`.)
- **Possible structural fixes (require maintainer action — out of this PR's
  scope):**
  1. **(Recommended)** Maintainer applies these patches manually via
     `git apply improvements/2026-05-XX-workflow-fixes.patch` on a local
     clone with PAT/SSH, then pushes to `main` directly. Stops the patch
     carry-forward churn.
  2. Replace the `GITHUB_TOKEN` in `daily-improve.yml` with a fine-grained
     PAT stored in `secrets.WORKFLOWS_WRITE_TOKEN` that has `workflows: write`
     scope. Carries the usual PAT-rotation hygiene cost.
  3. Move the workflow file modifications out of `daily-improve.yml` and
     into a separate workflow that is only triggered manually
     (`workflow_dispatch`) so a human is always in the loop.

---

### Stale-but-not-broken (not fixed in this patch — flagged for visibility)

- **`research/twitter-deepseek/`** last commit 2026-05-06 (4 days ago).
  `hourly-twitter-deepseek-agentic.yml` has a `cron: '37 */6 * * *'` schedule
  but no recent commits. Worth investigating in a follow-up — could be a
  DeepSeek API outage, an `--allowedTools` regression, or a workflow
  failure. Not bundled here because the fix requires diagnosis (the workflow
  is large and recently refactored to a daemon model).
- **`research/twitter-deepseek-pi/`** last commit 2026-04-27. The
  `hourly-twitter-deepseek-pi.yml` workflow is `workflow_dispatch:` only
  (no cron), so this is **expected** to be stale — it's an A/B sister
  workflow run manually, not a scheduled producer. **No action needed.**
- **`daily-digest.yml` schedule race:** The daily digest cron fires at
  `00:00 UTC`, before any of the day's source files exist (Bluesky 00:11,
  arXiv 06:13, model timeline 06:29, community 4h cycle, twitter 3h cycle).
  As a result, `research/digest/2026-05-09-digest.md` cites
  `research/twitter/2026-05-08.md`, `research/community/2026-05-07-hn.md`,
  `research/arxiv/2026-05-08-papers.md` — i.e. yesterday's files, even
  though today's files exist by mid-day. Consider moving the digest cron
  from `00:00` to `23:55` so it runs at end-of-day and cites today's files
  (would also align with the Bluesky / front-page / audio chain that follows).
  Not bundled here because it changes content semantics across the dashboard.

---

### Improvements Bundled in This PR

| File touched | Change | Lines |
|---|---|---|
| `.github/workflows/2h-bluesky.yml` | Switch host to `api.bsky.app`; add 9 `getAuthorFeed` probes; teach prompt about both JSON shapes | +47 / -22 |
| `.github/workflows/hourly-rss.yml` | Add `--max-time 15` to every curl; restore real DeepMind feed; replace dead Meta feed; add HF Daily Papers + 6 newsletter feeds | +63 / -53 |
| `.github/workflows/4h-community.yml` | Replace empty Score/Comments columns with Posted/Author from Atom fields; replace no-op `<10 score` filter with content-based filter | +18 / -9 |
| `.github/workflows/daily-arxiv.yml` | Specify author-format explicitly; rename Authors column → First Author; add load-bearing rationale | +18 / -7 |

All workflow file changes ship as a single unified patch in
`improvements/2026-05-10-workflow-fixes.patch` (verified to apply cleanly
against current `main` with `git apply --check`). **The patch contains only
workflow file changes; nothing else needs maintainer review.**

---

### Expected Impact (after maintainer applies the patch)

| Metric | Before | After | Delta |
|---|---|---|---|
| Days since last RSS commit | 13 | 0 (resumes hourly) | restored |
| Bluesky digest content | empty (403) | ~9 author feeds + 4 topic searches | restored |
| RSS feed sources | 11 (4 dead) | 19 (all live) | **+73%** working sources |
| Reddit digest column information density | 0 (all "—") | Posted UTC + Author (real) | restored |
| arXiv author attribution | "(multiple)" 17/17 | first-3 surnames | restored |
| Days of bundled-but-unmerged fixes | 5 (May 5–9) | 0 (if applied today) | unblocks pipeline |

---

*Generated by Daily Self-Improvement Workflow on 2026-05-10*
