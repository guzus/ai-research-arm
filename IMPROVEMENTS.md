# Methodology Improvements — 2026-05-05

Daily self-improvement audit of the 2026-05-04 research output. Two pipelines were
producing zero or near-zero signal; both root-caused to upstream API/feed changes
that the existing workflow's silent-fallback pattern had been masking.

(Note: a previous IMPROVEMENTS.md from 2026-02-01 proposed similar fixes but the
underlying workflow files in `main` still reference the dead URLs, so those
changes never actually shipped. This PR re-lands them, with all replacement
endpoints verified live on 2026-05-05.)

**Important: bot permission limitation.** The GitHub App that runs the
`daily-improve` workflow does not have the `workflows` permission, so it cannot
push edits to files under `.github/workflows/`. As a result, this PR ships:

- `IMPROVEMENTS.md` (this file) — the analysis and verification.
- `PROPOSED_WORKFLOW_CHANGES.patch` — a unified diff of the actual workflow
  edits, ready to apply with `git apply PROPOSED_WORKFLOW_CHANGES.patch` (or
  `git am` on the original commit).

A reviewer with `workflows` permission needs to apply the patch and commit it
manually. The same constraint will apply to every future improvement PR that
touches workflow YAML until the App's installation is granted Workflows write,
or the `daily-improve` workflow is updated to use a PAT with `workflow` scope.

## Issues Found

### 1. RSS pipeline silent for 7+ days (CRITICAL)

- Last RSS commit: `2026-04-27 09:18 UTC` (verified via `git log research/rss/`).
- The 2026-04-27 file itself reads "No new updates this hour" for every section.
- The 2026-05-04 daily digest documents the gap directly:
  *"RSS: Latest available 2026-04-27 (downstream from primary research files)."*
- Three feed URLs are dead, which is starving the per-run fetch into an unbroken
  streak of empty outputs:
  - `https://openrss.org/www.anthropic.com/news` → DNS unreachable (HTTP 000).
    Anthropic does not publish an official RSS feed, so the openrss.org mirror is
    the only path; that mirror is currently offline.
  - `https://ai.meta.com/blog/rss/` → HTTP 404. The Meta AI blog RSS endpoint has
    been retired.
  - `http://googleaiblog.blogspot.com/atom.xml` → HTTP 301 redirect to a dead
    FeedBurner URL. Redundant with `research.google/blog/rss/` regardless.

### 2. Bluesky pipeline fully broken (CRITICAL)

The 2026-05-04 and 2026-05-05 Bluesky outputs both report:
> *"all five pre-fetched data files returned an identical 403 Forbidden HTML
> response instead of JSON."*

Root cause: the public AppView hostname `public.api.bsky.app` now returns HTTP 403
to all unauthenticated requests. Direct verification from this runner:

```
$ curl -sI https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI
HTTP/2 403
$ curl -sI https://api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=AI
HTTP/2 200
```

The hostname `api.bsky.app` (no `public.` prefix) still serves unauthenticated
requests successfully and returns valid post arrays.

### 3. Silent-failure masking

Both workflows used `curl ... || echo "<rss></rss>"` and
`curl ... || echo '{"posts":[]}'`, which write valid-but-empty stubs *and* discard
the underlying HTTP status code. This is why the Bluesky pipeline ran for 7+ days
returning 403 without surfacing any signal — every run looked "successful" because
the stub fallback fired.

### 4. Source diversity gap

The RSS workflow was wired to 11 feeds, all lab-blog or generic-tech-press. None
of the high-signal AI commentators the daily digest actually cites (Simon
Willison, Nathan Lambert / Interconnects, SemiAnalysis, Latent Space, Import AI,
Lilian Weng, smol.ai, Marktechpost, MIT Tech Review, Stanford HAI, BAIR) was
ingested via RSS. Those signals arrived only via the Twitter pipeline, which
narrows the corpus and leaves a gap on days Twitter access is degraded.

## Changes Made

### `.github/workflows/hourly-rss.yml`

1. Removed the 3 dead feeds (openrss-anthropic, ai.meta.com/blog/rss,
   googleaiblog.blogspot).
2. Replaced with working equivalents (all verified 200 OK on 2026-05-05):
   - `blog.google/technology/ai/rss/` (Google AI blog, native — fresh items dated
     2026-05-04 confirmed)
   - `deepmind.google/blog/rss.xml` (DeepMind native feed)
   - `about.fb.com/news/feed/` (Meta Newsroom — closest replacement; prompt
     instructs Claude to filter aggressively for AI relevance)
3. Added 12 high-signal feeds:
   - Simon Willison (`simonwillison.net/atom/everything/`)
   - Interconnects (Nathan Lambert)
   - SemiAnalysis
   - Import AI (Jack Clark)
   - Latent Space
   - Lilian Weng
   - smol.ai daily AI news (`buttondown.com/ainews/rss`)
   - BAIR Berkeley
   - Stanford HAI
   - MIT Technology Review AI
   - Marktechpost
   - The Decoder
4. Added `arxiv_cl` (cs.CL / NLP) — was a coverage gap.
5. Replaced `curl … || echo "<rss></rss>"` with a `fetch_feed` helper that:
   - validates HTTP 200 status,
   - validates response size > 200 bytes,
   - validates the response contains `<item>` or `<entry>` tags,
   - emits `::warning::` annotations for failures (visible in Actions UI),
   - writes a valid empty stub on failure so downstream parsing still works.
6. Updated the Claude prompt to:
   - reflect the new feed list and section structure,
   - explicitly tell Claude empty-stub feeds are a handled failure mode and not
     worth flagging in the digest,
   - require AI-relevance filtering for general-press feeds.

### `.github/workflows/2h-bluesky.yml`

1. Switched all endpoints from `public.api.bsky.app` to `api.bsky.app`.
2. Added `Accept: application/json` and a User-Agent header.
3. Replaced the 5 untyped `curl` calls with a `fetch_bsky` helper that validates
   the response starts with `{` (i.e. is JSON, not the HTML 403 page) and counts
   the number of returned post URIs.
4. Added 4 high-signal-author searches (Simon Willison, Ethan Mollick, Nathan
   Lambert, plus existing Karpathy) and one new query (`agents_tools`) to broaden
   the agent-tooling signal.
5. Updated the Claude prompt to acknowledge empty-stub files as a handled state.

## Expected Impact

- **RSS pipeline**: should resume producing daily files immediately. New feed
  inventory raises lab-blog coverage from 5→6 working sources, adds 12
  high-signal commentary sources, and adds NLP-paper coverage. The validation
  helper means future feed deaths surface as Actions warnings rather than as
  silent week-long outages.
- **Bluesky pipeline**: should produce non-empty daily files for the first time
  since the `public.api.bsky.app` 403 regression began. The 4 new author
  searches align Bluesky coverage with the commentators the digest already cites
  from Twitter, providing redundancy if Twitter access degrades.
- **Daily digest**: the Sources line currently noting *"RSS: Latest available
  2026-04-27 (downstream from primary research files)"* should disappear within
  24 hours of merge.
- **Observability**: silent failures in either pipeline now surface as
  `::warning::` annotations in the Actions UI, so the next regression of this
  shape gets detected within hours instead of weeks.

## Verification

All new/replaced URLs probed live on 2026-05-05:

| URL | Status |
|---|---|
| `blog.google/technology/ai/rss/` | 200, fresh items dated 2026-05-04 |
| `deepmind.google/blog/rss.xml` | 200 |
| `about.fb.com/news/feed/` | 200, 10 items |
| `simonwillison.net/atom/everything/` | 200 |
| `interconnects.ai/feed` | 200 |
| `semianalysis.com/feed/` | 200 |
| `importai.substack.com/feed` | 200 |
| `latent.space/feed` | 200 |
| `lilianweng.github.io/index.xml` | 200 |
| `buttondown.com/ainews/rss` | 200 |
| `bair.berkeley.edu/blog/feed.xml` | 200 |
| `hai.stanford.edu/news/rss` | 200 |
| `technologyreview.com/topic/artificial-intelligence/feed` | 200 |
| `marktechpost.com/feed/` | 200 |
| `the-decoder.com/feed/` | 200 |
| `api.bsky.app/xrpc/app.bsky.feed.searchPosts` | 200, returns 9 posts in test |

*Generated by Daily Self-Improvement Workflow on 2026-05-05.*
