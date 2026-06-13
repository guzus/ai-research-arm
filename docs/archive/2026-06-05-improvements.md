# Methodology Improvements — 2026-06-05

> **Blocked push — maintainer action required.** This PR is doc-only.
> The substantive change is a prompt edit to
> `.github/workflows/2h-bluesky.yml`, but the **claude[bot] GitHub App
> still lacks the `workflows: write` permission** (same blocker as
> `docs/archive/2026-05-18-improvements.md` §3), so the bot cannot push
> a branch that touches `.github/workflows/*` — the push is `remote
> rejected … without workflows permission`. The exact proposed diff is
> embedded verbatim at the bottom of this file ("Proposed patch"). To
> apply it, either (a) grant **claude[bot]** `workflows: write` in the
> repo's App-installation settings and re-run `daily-improve.yml`, or
> (b) apply the patch below by hand in a maintainer push. The edit is
> two prompt-only inserts inside the existing `prompt: |` block scalar —
> low-risk and self-contained.

Analysis of the 2026-06-04 output cycle. The synthesis lanes (digest,
model-timeline, front-page) and the high-volume aggregation lanes
(Twitter, HN, Reddit, arXiv, RSS) all produced healthy, well-sourced
output — no churn warranted there. The one lane with a clear,
measurable quality defect in yesterday's output was **Bluesky**, and
both defects are fixable at the prompt level (no new sources, no
network/handle re-verification required).

## 1. Bluesky: single-author domination

### Issue

In `research/bluesky/2026-06-04.md`, a single account — **@emollick** —
supplied **14 of 26 bullets (54%)** across the day's two cycles. The
"Notable Researchers" and "Research & Papers" sections were almost
entirely one voice. A feed that is meant to be a diverse cross-section
of AI researchers instead reads as one person's timeline.

### Root cause

The curated handle list in `2h-bluesky.yml` has been pruned to **7
accounts** (down from 14) because Bluesky reassigns/aliases handles and
several old entries silently resolved to the wrong person or to empty
feeds (documented in the workflow's own hygiene comments). With a small
pool and `getAuthorFeed?limit=30` per handle, one prolific poster
mechanically dominates — the prompt had no per-author cap.

### Fix

Added a **PER-AUTHOR CAP** to the curator prompt in `2h-bluesky.yml`:
include at most **4 posts per author per cycle** (keep that author's
highest-engagement / most newsworthy posts, drop the rest), and never
let one author exceed half the cycle's bullets. This is a pure
filtering rule — it does not touch the handle list, so it carries no
handle-reassignment risk.

> Note: expanding the handle pool itself is the more durable fix, but
> the lane's hygiene protocol (correctly) requires live `getAuthorFeed`
> verification of every candidate handle before adding it — Bluesky
> reassigns handles, so an unverified add can start surfacing a
> stranger's posts. That verification needs network egress that this
> headless improve run cannot perform, so it is deferred to a run that
> can probe handles. The per-author cap mitigates the symptom today
> regardless of pool size.

## 2. Bluesky: second daily cycle duplicates the first

### Issue

The lane runs twice a day (00:11 and 12:11 UTC) — the cron comment says
this exists to "roughly double candidate posts per day." But the two
cycles in `2026-06-04.md` are near-identical: the 13:41 section re-lists
the same Uber-cap, METR-superforecaster, "made out of weights," and
contract-law posts as the 02:02 section, only with bumped like counts.
The second pass surfaced almost no NEW posts — it duplicated the first,
so it added cost without adding the diversity it was scheduled to add.

### Root cause

The prompt said `FORMAT (append if file exists)` but gave no instruction
to dedup against earlier same-day cycles. The curator re-emitted whatever
each handle's feed currently showed, with no memory of what an earlier
cycle already published.

### Fix

Added a **CROSS-CYCLE DEDUP** step to the prompt: before writing, read
the existing daily file and skip any post already present in an earlier
cycle (match on post link/URI, or same author + same opening text). Only
genuinely new posts are appended; a cycle that finds nothing new writes
`_No new posts since the earlier cycle._` instead of re-listing. This
makes the second pass additive — its stated purpose — instead of
duplicative.

## Expected impact

- Bluesky digests become source-diverse: no single account exceeds ~15%
  of bullets (4 of ~26) instead of 54%, so the curated researcher pool
  is actually represented.
- The second daily cycle contributes net-new posts, justifying the
  twice-daily schedule and giving `daily-digest.yml` a richer, less
  redundant Bluesky source line.
- Both changes are prompt-only edits inside the existing `prompt: |`
  block scalar — no schema, source, or auth surface changes, and no
  handle-reassignment risk.

## What was deliberately not changed

- **Twitter, Hacker News, Reddit, arXiv, RSS, digest, model-timeline,
  front-page, wiki** — all produced healthy 2026-06-04 output; no churn
  warranted.
- **Bluesky handle-pool expansion** — deferred (see note under fix #1);
  requires live handle verification this headless run can't perform.

## Files changed

- `.github/workflows/2h-bluesky.yml` — **proposed** (blocked by the
  bot's missing `workflows: write`; patch embedded below)
- `docs/archive/2026-06-05-improvements.md` (this file, committed)

## Proposed patch (`.github/workflows/2h-bluesky.yml`)

Apply with `git apply`, or paste the two inserts into the `prompt: |`
block by hand. Both inserts use 12-space indentation to stay inside the
block scalar.

```diff
@@ -133,6 +133,17 @@ jobs:

             Write to: research/bluesky/${{ steps.datetime.outputs.date }}.md

+            CROSS-CYCLE DEDUP — do this BEFORE writing. This lane runs
+            twice a day (00:11 and 12:11 UTC) specifically to surface MORE
+            distinct posts, not to re-list the same ones. If the daily file
+            already exists (an earlier cycle ran today), READ it first and
+            SKIP any post already present in an earlier cycle — match on the
+            post link/URI, or on the same author + same opening text. Only
+            append posts that are genuinely NEW this cycle. If a cycle finds
+            no new posts beyond what's already in the file, append the cycle
+            header followed by `_No new posts since the earlier cycle._`
+            rather than duplicating the earlier section.
+
             FORMAT (append if file exists):
@@ -168,6 +179,14 @@ jobs:
             - Low engagement posts
             - Pure reposts where feed[].reason is a repost reason

+            PER-AUTHOR CAP — the curated handle set is small (≈7 accounts),
+            so one prolific poster can crowd out the rest: in the 2026-06-04
+            output a single account (@emollick) supplied 14 of 26 bullets
+            (54%). To keep the feed source-diverse, include AT MOST 4 posts
+            from any single author per cycle — keep that author's highest-
+            engagement / most newsworthy posts and drop the rest. Never let
+            one author exceed half the cycle's bullets.
+
             ## COMMIT
```
