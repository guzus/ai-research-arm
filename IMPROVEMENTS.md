# Methodology Improvements — 2026-04-29

Auto-generated review of 2026-04-28 research output, with concrete fixes
proposed for the workflow files. Scope: data freshness, source coverage,
output quality.

> **Delivery note.** The bot's GitHub App does not have the `workflows`
> permission, so it cannot push edits to files under `.github/workflows/`
> directly (`refusing to allow a GitHub App to create or update workflow ...
> without 'workflows' permission`). All five workflow edits are bundled
> as a Git patch — `0001-Methodology-improvements-for-2026-04-29.patch`
> in the repo root — that a maintainer can apply with:
>
> ```
> git am 0001-Methodology-improvements-for-2026-04-29.patch
> ```
>
> Same workaround used by the prior `improve/2026-04-28` branch.

## Issues Found in 2026-04-28 Output

### 1. Bluesky workflow silently broken (`research/bluesky/2026-04-28.md`)

The 2026-04-28 Bluesky run produced an empty digest:

> _No posts curated this run: all five pre-fetched source files in
> `data/bluesky/` returned `403 Forbidden` HTML instead of JSON, so no
> post data was available to filter._

Root cause: Bluesky's `public.api.bsky.app` host now returns HTTP 403 for
unauthenticated `searchPosts` queries (CDN/anti-bot block). Confirmed by
direct curl (HTTP 403, ~2KB HTML error page) and by an upstream bsky-docs
issue (`bluesky-social/bsky-docs#332`).

Bluesky has effectively been a no-op data source since this regression.

### 2. Daily digest cited stale community sources

The 2026-04-28 daily digest (`research/digest/2026-04-28-digest.md`) listed:

> - Hacker News: latest available **2026-02-06**-hn.md (newer files not yet collected)
> - Reddit: latest available **2026-02-06**-reddit.md (newer files not yet collected)

But `research/community/2026-04-27-hn.md`, `2026-04-27-reddit.md`,
`2026-04-28-hn.md`, and `2026-04-28-reddit.md` all exist. The model fell
through to a 2-month-old file because it searched only for files matching
the `today's date` string and the digest is generated at 00:00 UTC — before
that day's community/twitter runs have produced output. The fallback should
be **yesterday**, not the entire archive.

### 3. RSS workflow appears stalled

Most recent RSS commit: `2026-04-27 09:18 UTC`. No `research/rss/2026-04-28.md`
file exists, even though the workflow runs hourly. The empty digest format
("No new updates this hour" repeated for every section) also makes it hard
to tell from the output whether the workflow ran or just found nothing.

(This change set adds new sources rather than diagnosing the runner gap;
the additional feeds give the workflow more material to write about and
make it easier to spot empty runs vs. actual outages.)

### 4. arXiv author placeholders

Every paper in `research/arxiv/2026-04-28-papers.md` is attributed to
"(arXiv group submission)" or "(arXiv)". This is a placeholder string the
model emits when it doesn't pull real metadata from the arXiv MCP tool.
Without real author surnames, paper provenance is opaque and the digest
loses citation quality.

### 5. Limited Reddit subreddit coverage

The community workflow polls only `r/MachineLearning`, `r/LocalLLaMA`, and
`r/artificial`. Major AI conversation centers — `r/singularity`,
`r/OpenAI`, `r/ClaudeAI` — were not being captured.

## Changes Applied

### `.github/workflows/2h-bluesky.yml`

- **Fix:** Switch from `public.api.bsky.app` → `api.bsky.app` for the
  XRPC `searchPosts` calls. Verified HTTP 200 + JSON payload from the
  research runner.
- **Hardening:** Added a defensive HTML-vs-JSON sniff (`head -c 1`) so if
  the AppView ever returns an error page again, we normalize to
  `{"posts":[]}` instead of failing the downstream parse silently.
- **Coverage:** Added 3 new search queries — `AI safety alignment`,
  `open weights model`, `arxiv.org abs` (catches paper-link drops).
- **Cleanup:** Replaced the unreliable `from:karpathy.bsky.social` query
  syntax with a plain handle keyword search.

### `.github/workflows/daily-digest.yml`

- Pass `yesterday` as a second template variable.
- Rewrite the source-file step to enumerate **specific yesterday + today
  paths** for twitter, community, arxiv, rss, bluesky, models, and
  twitter-deepseek.
- Add an explicit guard: "do NOT cite any source older than yesterday —
  if a source-type is missing for both dates, say 'no data' instead of
  citing stale files." Prevents the 2026-02-06 fallback we observed.
- Same rewrite applied to both the MCP-enabled branch and the
  WebSearch fallback branch.

### `.github/workflows/hourly-rss.yml`

Added 9 new high-signal feeds covering the gaps the 04-28 digest hit:

- **Tech press:** MIT Technology Review (AI), Ars Technica, The Information
  (titles only — paywalled), MarkTechPost (high-volume model coverage).
- **Analyst & researcher blogs:** SemiAnalysis (Dylan Patel — chips/capex),
  Simon Willison (applied LLM commentary), Latent Space (Swyx/Alessio),
  Import AI (Jack Clark — policy + research roundup).
- **Research:** arXiv `cs.CL` (Computation & Language / NLP) — was missing
  alongside the existing `cs.AI` and `cs.LG`.

Updated the prompt's source list and output format to include these.

### `.github/workflows/daily-arxiv.yml`

- New "AUTHOR ATTRIBUTION" instruction: extract real first-author surnames
  from the MCP / `<dc:creator>` metadata, format as "Smith et al." for
  papers with >3 authors, and **never** emit "(arXiv group submission)".
- If author metadata is missing for a paper, drop it from the digest
  rather than fake-attributing it.

### `.github/workflows/4h-community.yml`

- Add 3 new subreddits: `r/singularity`, `r/OpenAI`, `r/ClaudeAI`.
- Update the RSS file list and output format to include them.
- Add explicit guidance that Reddit RSS does not expose score/comment
  counts and that "N/A" is the correct value (instead of the model
  trying to invent or omit those columns).

## Expected Impact

- **Bluesky digest goes from 0 → tens of curated posts/day** once the
  endpoint switch lands. Direct restoration of a dead source.
- **Daily digest stops citing 2-month-old files.** Yesterday's twitter,
  HN, reddit, and arXiv data should now consistently feed the 00:00 UTC
  digest run.
- **+9 RSS sources** broadens coverage into chip/infra analysis
  (SemiAnalysis), policy commentary (Import AI), and applied LLM voices
  (Simon Willison, Latent Space) that the 04-28 digest had to source via
  WebSearch instead.
- **arXiv author quality** improves from generic "(arXiv)" placeholders
  to real first-author citations, restoring proper attribution.
- **+3 subreddits** captures Claude/OpenAI/singularity discourse that
  was previously invisible to the community digest.

## What Was Not Changed

- The `hourly-rss.yml` runner-side hang (no commits since 04-27 09:18 UTC)
  was not investigated as part of this PR — needs a runner-log dive
  rather than a workflow edit. If the new feeds also fail to write
  tomorrow, that's the signal to look at the runner.
- Reddit score/comment data: the `.rss` endpoint genuinely doesn't
  expose those fields. A switch to authenticated Reddit OAuth would
  restore them but would require new secrets — out of scope for an
  unattended self-improvement PR.
