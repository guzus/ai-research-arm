# Methodology Improvements — 2026-06-15

## Concrete defect found

**Lane:** Bluesky (`2h-bluesky.yml`, twice-daily `00:11` / `12:11` UTC).

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

**Why it matters:** the twice-daily cadence was added *specifically* to
"roughly double candidate posts per day" (see the cron comment in the
workflow — a single daily snapshot kept yielding <3 posts). The overwrite
behavior **inverts that intent**: instead of doubling, the evening run
*halved* the day's Bluesky signal and dropped its strongest posts before
the digest could read them.

**Root cause:** the agent prompt only asked to "append if file exists" as a
weak parenthetical inside the FORMAT heading, while the agent held the
`Write` tool (which overwrites) and owned the `git commit`. Correctness
depended on the model *choosing* to append — and on 06-13/06-14 it chose
to overwrite. The twitter lane avoids this by appending sections
deterministically; Bluesky did not.

## Fix

Made the append **deterministic** in `.github/workflows/2h-bluesky.yml`,
mirroring the proven `daily-front-page.yml` bash-commit pattern:

1. **New pre-step `Ensure daily Bluesky file exists`** — idempotently
   creates `research/bluesky/<date>.md` with its `# Bluesky AI Feed` title
   header if missing.
2. **Agent contract narrowed** — it now writes ONLY its per-run section
   (starting at `## <timestamp>`) to `/tmp/bluesky-section.md`. The
   `git` tool was removed from `allowedTools` (now `Read,Write,Bash(ls:*)`)
   and the prompt forbids touching `research/bluesky/`, so the model can no
   longer clobber or commit the daily file. A quiet cycle still emits a
   `## <timestamp>` heading with `_No qualifying posts this cycle._`.
3. **New post-step `Append section to daily file and commit`** —
   `cat /tmp/bluesky-section.md >> research/bluesky/<date>.md`, then commits
   under the standard `github-actions[bot]` identity. `safe-push` pushes it
   as before.

## Expected impact

- The evening run can no longer erase the morning run; both snapshots
  accumulate, restoring the twice-daily cadence's intended doubling of
  Bluesky candidate posts.
- High-engagement posts captured early in the day reach the daily digest
  instead of being silently deleted before it runs.
- Append behavior no longer depends on model discretion — it is enforced
  by the workflow, matching the determinism of the other aggregation lanes.
