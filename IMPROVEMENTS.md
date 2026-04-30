# Methodology Improvements — 2026-04-30

Auto-generated review of the 2026-04-29 research output, with concrete
fixes proposed for three workflow files. Scope: digest timing, source
coverage, citation integrity, and silent-pipeline detection.

> **Delivery note.** The bot's GitHub App does not have the `workflows`
> permission, so it cannot push edits to files under `.github/workflows/`
> directly (`refusing to allow a GitHub App to create or update workflow ...
> without 'workflows' permission`). All workflow edits are bundled
> as a Git patch — `0001-Methodology-improvements-for-2026-04-30-workflow-pat.patch`
> in the repo root — that a maintainer can apply with:
>
> ```
> git am 0001-Methodology-improvements-for-2026-04-30-workflow-pat.patch
> ```
>
> Same workaround used by the prior `improve/2026-04-28` and
> `improve/2026-04-29` branches.

> **Relationship to prior PRs.** `improve/2026-04-28` and
> `improve/2026-04-29` are still open and unmerged. This PR addresses
> **different** issues — chosen specifically because they were not
> covered by the previous methodology runs. If/when those land first,
> the workflow hunks here may need a small rebase, but no semantic
> conflicts are expected.

## Issues Found in 2026-04-29 Output

### 1. Daily digest is structurally one day behind

`research/digest/2026-04-29-digest.md` reports as its lead stories the
Mag-7 earnings *preview*, Day 2 of *Musk v. Altman* (which was 04-28),
and the Fortune CFO/Friar piece (04-28). It even self-labels
"*Generated at 2026-04-29 00:00 UTC*".

Root cause: `daily-digest.yml` runs at `cron: '0 0 * * *'` — the very
first second of the new UTC day, before any of that day's source
collectors have run. The model is forced to summarize the previous
day's content under today's filename.

### 2. arXiv pipeline emits fabricated paper IDs and anonymous authors

`research/arxiv/2026-04-29-papers.md` cites:

```
[2604.21254](https://arxiv.org/abs/2604.21254) — Hyperloop Transformers
[2604.22981](https://arxiv.org/abs/2604.22981) — Reward Models Are…
[2604.04503](https://arxiv.org/abs/2604.04503) — Memory Intelligence Agent
```

These IDs are not verifiable (the model invented numerical suffixes
when the MCP tool didn't return real metadata), and authors are listed
as "(multi-author submission)" or "(anonymous arXiv preprint)" — both
documented as placeholder strings in the prior `improve/2026-04-29`
review. The prior PR addressed authors but did not require *URL
resolution* of the IDs themselves.

### 3. HuggingFace model drops only surfaced via Reddit chatter

Three significant model releases landed on 2026-04-29:

- Mistral Medium 3.5 ("Vibe", 128B)
- IBM Granite 4.1 (3B/8B/30B + Granite Speech 4.1)
- inclusionAI Ling-2.6-1T

None of them had a first-class capture path. They were noticed only
because the r/LocalLLaMA hot-feed scraper happened to pick up community
threads about them. The hourly-rss workflow polls company *blogs*
(which lag the HF drops by hours or never publish) but not HF directly.

### 4. Major OSS releases have no first-class source either

Zed 1.0 was the **#1 Hacker News story for the day** (1204 points, 388
comments). It is an AI-native code editor — squarely within scope —
and yet only appeared via the HN scrape. There is no GitHub-trending
feed in the pipeline.

### 5. AI security incidents are now first-class news with no bucket

The 2026-04-29 HN front page contained three independent AI-security
incidents:

- **HERMES.md auto-load billing bug** (560 points) — Anthropic refund
  dispute over Claude Code auto-loading a config that ran ~$200 of
  unexpected work.
- **Copy Fail / CVE-2026-31431** (239 points) — clipboard-based
  prompt-injection class against AI assistants.
- **PromptArmor write-up: Ramp Sheets AI exfiltrates customer
  financials** (56 points) — production-scale indirect prompt
  injection.

The current digest format has them shoved into "Community Buzz" or
"Tools & Resources" alongside unrelated items. Given how often these
now drive the day, they deserve their own section.

### 6. Silent pipelines fail without alerting

`research/twitter/` last commit: 2026-04-28 15:57 UTC.
`research/rss/` last commit: 2026-04-27 09:18 UTC. As of 2026-04-30
morning (digest generation time), both have been silent for **24-72
hours** with no visible alert. The digest model just notes "0 fresh
updates today" and moves on — no signal that the upstream collector is
broken.

## Changes Applied (in the patch)

### `.github/workflows/daily-digest.yml`

- **Cron moves from `0 0 * * *` → `30 23 * * *`.** Generates at 23:30
  UTC, so the digest captures the full day's earnings calls, US
  business-day announcements, and after-close drops before the date
  rolls over. Fixes issue #1 directly.
- **New step: `Detect stale pipelines`.** Walks the `research/`
  subdirectories for `twitter/`, `rss/`, `bluesky/`, `community/`,
  `arxiv/`, `twitter-deepseek/`, `models/`. For each, finds the newest
  `YYYY-MM-DD-prefixed` file and flags any source whose newest dated
  file is more than 36h old. Result is fed into the digest prompt as a
  "STAGNANT-PIPELINE REPORT" passthrough.
- **Digest prompt:** read both today AND yesterday explicitly; never
  fall through to older files; surface stale-pipeline status under a
  "Pipeline Health" line in Sources.
- **New "AI Security & Incidents" section** added between Community
  Buzz and Funding & Business. Skipped on quiet days (explicit
  guidance to omit if nothing reportable).
- Both prompt branches (MCP-enabled and WebSearch fallback) updated
  identically so the format stays stable regardless of which keys are
  present.

### `.github/workflows/hourly-rss.yml`

- **HuggingFace: Daily Papers + Trending Models** added as JSON
  sources (`hf_daily_papers.json`, `hf_trending_models.json`). HF's
  API is authoritative for "this model just shipped" — closes the gap
  that let Mistral Medium 3.5 / IBM Granite 4.1 / Ling-2.6-1T pass
  through uncovered on 2026-04-29.
- **GitHub trending repos** added via OSSInsight's public JSON
  endpoint (`gh_trending_python.json`, `gh_trending_typescript.json`).
  Targets major OSS launches like Zed 1.0.
- Output format extended with "🤗 HuggingFace Drops" and "🐙 GitHub
  Trending" sections.
- Filter rules added: only surface an HF model the *first* time it
  appears (avoids weekly redundancy on long-trending models); GitHub
  filter explicitly requires AI/dev relevance and drops awesome-lists,
  dotfiles, generic libraries, scrapers, and memes.

### `.github/workflows/daily-arxiv.yml`

- **CITATION INTEGRITY (HARD REQUIREMENTS)** block added to the
  prompt:
  - Every cited paper must be *URL-verified* via MCP or WebSearch
    before inclusion. Unverified IDs are dropped, not estimated.
  - Authors must be real first-author surnames; placeholders like
    "(multi-author submission)" / "(anonymous)" are explicitly
    forbidden.
  - arXiv ID format guard (YYMM.NNNNN with valid YYMM and 5-digit
    NNNNN).
  - "Better fewer real papers than many fake ones" framing — the
    Top-5 slot count is a target, not a quota, so the model isn't
    pressured to invent IDs to fill the list.

## Expected Impact

- **Digest stops summarizing the wrong day.** The 2026-04-30 digest
  generated at 23:30 UTC tonight will include *today's* Apple Q2 FY26
  earnings, today's reactions to the Mistral 3.5 / Granite 4.1 drops,
  today's Musk v. Altman testimony — instead of yesterday's.
- **Model release coverage closes a known blind spot.** HF Daily
  Papers + trending models surfaces 5-15 new releases/day directly
  rather than via second-hand Reddit chatter.
- **Major OSS launches are caught at drop time.** GitHub trending on
  the hourly cadence means Zed-1.0-class news has a first-class path.
- **Digest has a coherent home for AI security news.** The class of
  story is now large enough (CVEs, prompt-injection write-ups,
  agent-billing bugs) to warrant its own section.
- **Silent collectors raise themselves.** Any source dark for >36h is
  surfaced inside the digest's Sources / Pipeline Health line, which
  serves as a daily watchdog without needing a separate alerting
  workflow.
- **arXiv citations become trustworthy again.** The verification gate
  trades quantity for quality — fewer entries, but no fabricated IDs.

## What Was Not Changed

- The hourly-twitter and hourly-rss runner-side outages (no commits
  for 24-72h) are *detected* by the new staleness check but not
  *fixed* here — diagnosis requires runner logs that aren't accessible
  from this self-improvement run. Once the staleness line lands, the
  outage will be visible in every day's digest until a maintainer
  investigates.
- Bluesky API 403 — this PR does not re-attempt the
  `public.api.bsky.app → api.bsky.app` switch; that fix is already
  staged in `improve/2026-04-29` and re-doing it would create merge
  noise.
- Reddit OAuth (for score/comment metadata) — out of scope; needs new
  secrets.
