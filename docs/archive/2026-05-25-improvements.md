# Methodology Improvements — 2026-05-25

## Why this is a docs-only PR

The fix below lives entirely in `.github/workflows/2h-bluesky.yml`, and
the `claude[bot]` GitHub App installation **cannot push workflow-file
changes** — it lacks the `Workflows: read/write` installation permission,
which (as noted in `daily-improve.yml:21-24`) cannot be granted from a
workflow's `permissions:` block. A `git push` carrying any
`.github/workflows/*` edit is rejected outright:

```
! [remote rejected] improve/2026-05-25 -> improve/2026-05-25
  (refusing to allow a GitHub App to create or update workflow
   `.github/workflows/2h-bluesky.yml` without `workflows` permission)
```

So this PR ships the analysis plus a **ready-to-apply patch** (below). A
maintainer with workflow write access applies it in one step:

```bash
git apply <<'PATCH'
<the diff in the "Proposed patch" section>
PATCH
```

(Same docs-only fallback used by the 2026-05-19 improvement run.)

## Context

Analysis of 2026-05-24 output. The aggregation lanes (Twitter, arXiv,
RSS, HN/Reddit community) were healthy and high-signal. The one lane
producing **zero usable signal** was Bluesky, and the root cause was a
stale, partly-wrong curated account list — a data-quality bug, not a
coverage strategy problem.

## Issues found

### 1. Bluesky was ingesting the wrong person as "Simon Willison" (data-quality bug)
`research/bluesky/2026-05-24.md` flagged it directly in its feed-health
note: `simonw.bsky.social` resolves to **"Simon Wigzell," a Swedish
comics blogger** posting Swedish-language comics reviews — **not** Simon
Willison, the independent AI researcher. We were silently treating a
comics blog as an AI source.

- **Verified fix:** Simon Willison's real Bluesky handle is the custom
  domain **`simonwillison.net`** (web-confirmed: ~39K followers, ~2K
  posts, self-described independent AI researcher, posts daily about
  LLMs). `getAuthorFeed` resolves custom-domain handles to a DID just
  like `*.bsky.social` handles, so the swap is drop-in.

### 2. Two tracked accounts were long dormant — burning API calls for nothing
The same feed-health note reported:
- `karpathy.bsky.social` — last activity **2023-05-27** (Karpathy is
  active on X, effectively dead on Bluesky).
- `arankomatsuzaki.bsky.social` — last post **2024-12-17**.

Both fall far outside the 24h engagement window every run, so they only
cost an HTTP request + 1s sleep each and clutter the "empty feeds" note.
Drop both. (Trivially re-added if either resumes posting.)

### 3. The handle list was duplicated in two places that could silently drift
The workflow lists the curated accounts twice:
1. the `handles=( … )` bash array that drives the fetch, and
2. a **hardcoded `data/bluesky/*.json` filename list** baked into the
   Claude prompt.

Editing one without the other makes the curator read a stale set (e.g.
still ingesting `simonw.json`, or never reading a newly-added account).
This is exactly the class of bug that let the wrong/missing handle
persist unnoticed. The patch replaces the prompt's hardcoded list with a
directory enumeration so future handle edits touch only the bash array.

## Proposed patch (apply to `.github/workflows/2h-bluesky.yml`)

```diff
@@ -38,8 +38,16 @@ jobs:

           # Public keyword search now returns HTTP 403 without an authenticated
           # session. Author feeds remain public, so use a curated AI-source list.
+          #
+          # Handle hygiene (verified 2026-05-25): `simonw.bsky.social` resolved
+          # to a Swedish comics blogger, NOT Simon Willison — his real handle is
+          # the custom domain `simonwillison.net`. `karpathy.bsky.social` (last
+          # post 2023-05-27) and `arankomatsuzaki.bsky.social` (last post
+          # 2024-12-17) were dormant and only burned API calls, so they were
+          # dropped. Custom-domain handles (no `.bsky.social` suffix) are fine:
+          # getAuthorFeed resolves the handle to a DID either way, and the slug
+          # below just keeps the full handle as the filename.
           handles=(
-            "karpathy.bsky.social"
             "emilymbender.bsky.social"
             "mmitchell.bsky.social"
             "huggingface.bsky.social"
@@ -48,10 +56,9 @@ jobs:
             "jeremyhoward.bsky.social"
             "yoavgo.bsky.social"
             "swyx.bsky.social"
-            "simonw.bsky.social"
+            "simonwillison.net"
             "hardmaru.bsky.social"
             "moyix.bsky.social"
-            "arankomatsuzaki.bsky.social"
             "schmidhuber.bsky.social"
           )

@@ -80,7 +87,7 @@ jobs:
         with:
           claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
           claude_args: |
-            --model sonnet --allowedTools "Read,Write,Edit,Bash(git:*)"
+            --model sonnet --allowedTools "Read,Write,Edit,Bash(ls:*),Bash(git:*)"
           prompt: |
             You are a Bluesky AI feed curator. Process REAL-TIME posts from Bluesky.

@@ -89,21 +96,10 @@ jobs:

             ## SOURCE FILES

-            Read these pre-fetched Bluesky JSON files from data/bluesky/:
-            - data/bluesky/arankomatsuzaki.json
-            - data/bluesky/deeplearning.json
-            - data/bluesky/emilymbender.json
-            - data/bluesky/hardmaru.json
-            - data/bluesky/huggingface.json
-            - data/bluesky/jeremyhoward.json
-            - data/bluesky/karpathy.json
-            - data/bluesky/mmitchell.json
-            - data/bluesky/moyix.json
-            - data/bluesky/rasbt.json
-            - data/bluesky/schmidhuber.json
-            - data/bluesky/simonw.json
-            - data/bluesky/swyx.json
-            - data/bluesky/yoavgo.json
+            Read EVERY `*.json` file in `data/bluesky/` (one per tracked
+            account; run `ls data/bluesky/` first to enumerate them). Do not
+            rely on a hardcoded filename list — the curated handle set changes
+            over time, so always process whatever files are present.

             The Bluesky JSON structure is:
             - feed[].post.author.handle (username like "user.bsky.social")
```

> Note: the `--allowedTools` line gains `Bash(ls:*)` so the curator can
> actually enumerate `data/bluesky/` (it previously had only
> `Bash(git:*)` and could not run `ls`).

## Deliberately NOT done

- **No new handles were guessed.** The whole bug here was an unverified
  handle (`simonw.bsky.social`). The Bluesky public `getAuthorFeed` API
  is the right way to verify candidate accounts (resolves? recent
  posts?), but live API verification was unavailable in this run's
  sandbox. Net-new accounts (e.g. `nsaphra.net` and other AI researchers
  on Bluesky) should be **API-verified for activity before** being added
  in a follow-up, rather than added speculatively.

## Expected impact

- Bluesky stops surfacing an unrelated Swedish comics blog as an AI
  source and starts pulling one of the highest-signal independent AI
  voices on the platform.
- ~2 fewer wasted API calls per run; cleaner feed-health output.
- Handle-list maintenance becomes single-source, removing the silent
  array/prompt drift that allowed the wrong-handle bug to persist.
