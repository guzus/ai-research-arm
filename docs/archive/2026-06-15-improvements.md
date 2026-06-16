# Methodology Improvements — 2026-06-15

## Concrete defect found

**Lane:** Bluesky (`2h-bluesky.yml`, formerly twice-daily `00:11` /
`12:11` UTC; reduced here to daily `10:11` UTC).

**Defect:** the second daily run **overwrote** the daily file instead of
appending to it, destroying the first run's posts.

**Evidence (proven, not hypothetical):**

- `research/bluesky/2026-06-14.md` as committed contains a **single**
  `## 2026-06-14 22:02 UTC` section with 8 posts.
- Two runs committed that day:
  - `82b6d084` — "Bluesky feed 2026-06-14 10:36 UTC"
  - `e93efd0f` — "Bluesky feed 2026-06-14 22:02 UTC"
- `git show 82b6d084:research/bluesky/2026-06-14.md` shows the 10:36 run
  captured **12 posts**, including the day's highest-engagement items that
  never reached the digest: emollick's SimRefinery/Fable rebuild (❤️ 144),
  alexhanna on the "critical confabulations" rebrand (❤️ 137), the
  "shape of the graph" post (❤️ 95), and an OpenEvidence-vs-frontier-LLM
  clinical paper (❤️ 83).
- `git show e93efd0f -- research/bluesky/2026-06-14.md` is a net
  **−13 / +8** diff that deletes all 12 ❤️-bearing lines from the 10:36
  snapshot — i.e. a full rewrite, not an append.
- Same shape on `2026-06-13`: only one section survives despite the
  twice-daily schedule.

**Why it matters:** the twice-daily cadence was added to increase candidate
posts when the source list was sparse. After the May/June handle fixes, the
lane became reliable enough to produce real commentary but not valuable enough
to justify firehose behavior. The overwrite behavior **inverted the original
intent**: instead of accumulating useful signal, the later run erased the
earlier run's strongest posts before the digest could read them.

**Root cause:** the agent prompt only asked to "append if file exists" as a
weak parenthetical inside the FORMAT heading, while the agent held the
`Write` tool (which overwrites) and owned the `git commit`. Correctness
depended on the model *choosing* to append — and on 06-13/06-14 it chose
to overwrite. The twitter lane avoids this by appending sections
deterministically; Bluesky did not.

## Fix

Made the lane lower-maintenance and the append **deterministic** in
`.github/workflows/2h-bluesky.yml`, mirroring the proven
`daily-front-page.yml` bash-commit pattern:

1. **Cadence reduced to daily `10:11` UTC** — Bluesky is kept as a
   supplemental expert-commentary source, not a core breaking-news lane.
2. **New pre-step `Ensure daily Bluesky file exists`** — idempotently
   creates `research/bluesky/<date>.md` with its `# Bluesky AI Feed` title
   header if missing.
3. **Agent contract narrowed and capped** — it now writes ONLY its per-run section
   (starting at `## <timestamp>`) to `.tmp/bluesky-section.md`. The
   `git` tool was removed from `allowedTools` (now `Read,Write,Bash(ls:*)`)
   and the prompt forbids touching `research/bluesky/`, so the model can no
   longer clobber or commit the daily file. Output is capped at 8 bullets
   total and 3 bullets per author, with a quiet cycle still emitting a
   `## <timestamp>` heading with `_No qualifying posts this cycle._`.
4. **New post-step `Append section to daily file and commit`** — validates
   that the agent produced the section, drops any bullet whose Bluesky post
   link already exists in today's file, enforces the 8-total / 3-per-author
   caps, appends the filtered section to `research/bluesky/<date>.md`, then
   commits under the standard `github-actions[bot]` identity. `safe-push`
   pushes it as before.
5. **Daily-improve value check added** — future self-improvement runs should
   judge supplemental lanes such as Bluesky by distinct digest-worthy insight
   and prefer removal/demotion over more sources or cadence when value is low.

## Expected impact

- The lane keeps its useful part — expert interpretation from a small set of
  AI researchers/practitioners — without acting like a fragile twice-daily
  firehose.
- Manual re-runs can no longer erase prior output; snapshots accumulate as
  net-new posts instead of re-listing the same 48-hour window.
- Append and dedup behavior no longer depend on model discretion — they are
  enforced by the workflow, matching the determinism of the other aggregation
  lanes.
