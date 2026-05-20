# Methodology Improvements — 2026-05-20

Analysis of the 2026-05-19 output cycle. The synthesis lanes (Twitter,
Hacker News, Reddit, arXiv, RSS, digest, model-timeline, front-page) are
all producing healthy, primary-source-linked output — the 2026-05-19
digest is strong. This PR targets the one lane that is measurably
under-performing and one concrete coverage miss in RSS.

## Issues found

### 1. Bluesky lane is starved (1 post on 2026-05-19)

Yesterday's PR (2026-05-18) fixed the 30+ day Bluesky outage by switching
from the now-auth-gated `searchPosts` endpoint to `getAuthorFeed` over a
curated list of 14 handles. That fix is working — no more HTTP 403 — but
`research/bluesky/2026-05-19.md` still contains only **one** post. The
digest's own Sources section reflects this: Bluesky barely contributes.

Auditing the 14 handles today via
`getAuthorFeed?...&filter=posts_no_replies` shows why:

| Handle | Feed |
|---|---|
| emilymbender, mmitchell, hardmaru, rasbt, yoavgo, simonw, karpathy | active |
| arankomatsuzaki | minimal |
| **huggingface.bsky.social** | **empty** (org dormant; real handle is `hf.co`, last post 2025-11) |
| **deeplearning.bsky.social** | **empty** (real handle `deeplearningai`, last post 2026-02) |
| jeremyhoward, swyx, moyix, schmidhuber | empty at audit time (kept — low cost, may post occasionally) |

So only ~7 of 14 handles ever produce posts, and on any given 24h window
only a couple of those have a fresh, above-threshold post. The lane is
under-sourced, not broken.

### 2. RSS missed a high-signal, widely-shared AI post

Simon Willison's "The last six months in LLMs in five minutes" was the
**#2 Hacker News story on 2026-05-19 (629 pts / 505 comments)**, yet the
RSS lane never surfaced it because his blog wasn't a subscribed feed. His
weblog is one of the most-cited independent LLM sources and publishes
daily; not subscribing to it is a real gap. The RSS tech-news set was
also relatively narrow (TechCrunch / The Verge / VentureBeat).

## Changes made

### `.github/workflows/2h-bluesky.yml`

- **Added 4 handles**, each verified posting on 2026-05-19 via
  `getAuthorFeed` (timestamps checked, not just handle-resolves):
  - `natolambert.bsky.social` — Nathan Lambert (Interconnects);
    post-training and open-model-release commentary.
  - `emollick.bsky.social` — Ethan Mollick; applied-AI, high engagement.
  - `alexhanna.bsky.social` — Alex Hanna (DAIR); AI policy / ethics.
  - `minimaxir.bsky.social` — Max Woolf; ML engineering / generative AI.
- **Removed 2 misrouted org handles** (`huggingface.bsky.social`,
  `deeplearning.bsky.social`) that returned empty feeds. The real org
  accounts (`hf.co`, `deeplearningai.bsky.social`) exist but are dormant
  on Bluesky (last posts 2025-11 and 2026-02), so they were not added.
- Updated the Claude prompt's source-file list to match the new handle
  set, keeping it alphabetical.

Net active-source count rises from ~7 to ~11; the four additions also
broaden the lane beyond AI-ethics/academia into model-release and
applied-AI signal.

### `.github/workflows/hourly-rss.yml`

Added 4 feeds, each probed HTTP 200 with fresh (2026-05-19) items today:

- **Simon Willison's Weblog** (`simonwillison.net/atom/everything/`, Atom)
  — new "Independent Analysis" section. Prompt notes the Atom shape
  (`entry/title/link[@href]/published`) and to keep only AI/LLM entries.
- **Ars Technica AI** (`arstechnica.com/ai/feed/`).
- **MIT Technology Review AI**
  (`technologyreview.com/topic/artificial-intelligence/feed/`).
- **The Decoder** (`the-decoder.com/feed/`) — AI-only news outlet.

All four use the existing graceful-fallback pattern (write an empty
`<rss>`/`<feed>` on failure) so a dead feed never breaks the run. The
output FORMAT block gained the matching subsections.

## Expected impact

- **Bluesky:** more days with multiple real posts instead of 0–1; a real
  Bluesky source line in the daily digest rather than a near-empty one.
- **RSS:** broader, higher-signal coverage; specifically, independent
  analysis (Simon Willison) and two more quality outlets that the
  TechCrunch/Verge/VentureBeat set was missing — closing the kind of gap
  that let the most-shared LLM post of 2026-05-19 slip through.

## What was deliberately not changed

- **Twitter / HN / Reddit / arXiv / digest / model-timeline /
  front-page** — all healthy on 2026-05-19; no churn warranted.
- **Dormant individual Bluesky handles** (jeremyhoward, swyx, moyix,
  schmidhuber) were kept rather than pruned — the per-handle cost is a
  few KB plus a 1s sleep, and these are real accounts that may post
  intermittently. Only the two clearly-misrouted *org* handles were
  removed.
- The known **claude[bot] `workflows: write`** App-permission caveat
  from the 2026-05-18 doc still applies: this PR touches workflow files,
  so if the push is rejected, that permission must be granted at the App
  installation level (not settable from workflow YAML).

## Applying the workflow changes

The `claude[bot]` GitHub App still lacks `workflows: write`, so this
branch **cannot** carry the `.github/workflows/*` edits directly — the
push is rejected with:

```
refusing to allow a GitHub App to create or update workflow
`.github/workflows/2h-bluesky.yml` without `workflows` permission
```

To keep the PR actionable without that permission, the exact two-file
diff is committed here as a patch a maintainer can apply in one step:

```
git apply docs/archive/2026-05-20-workflow-changes.patch
git add .github/workflows/2h-bluesky.yml .github/workflows/hourly-rss.yml
git commit -m "Apply 2026-05-20 RSS + Bluesky source improvements"
```

The durable fix is to grant the **claude[bot]** App `workflows: write`
at the repo's App-installation settings (not settable from workflow
YAML); after that, future daily-improve PRs can carry workflow edits
inline.

## Files changed

- `docs/archive/2026-05-20-improvements.md` (this file)
- `docs/archive/2026-05-20-workflow-changes.patch` (the `.github/workflows`
  diff for `2h-bluesky.yml` and `hourly-rss.yml`, applied via `git apply`)
