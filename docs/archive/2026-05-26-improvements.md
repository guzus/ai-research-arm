# Methodology Improvements — 2026-05-26

Analysis of the 2026-05-25 output surfaced one concrete, recurring
data-quality bug in the community lane plus two freshness observations
that are infrastructure-shaped rather than workflow-shaped.

> **⚠️ Delivery note — workflow edit could not be auto-pushed.**
> The fix in §1 edits `.github/workflows/4h-community.yml`, but the
> `claude[bot]` GitHub App push was **rejected**:
> `refusing to allow a GitHub App to create or update workflow
> .github/workflows/4h-community.yml without `workflows` permission`.
> This is the exact App-installation blocker called out in the
> 2026-05-18 improvement doc (§3) and is **not** settable from workflow
> YAML. So this PR ships **docs-only**; the complete, ready-to-apply
> workflow patch is embedded verbatim in the
> [Appendix](#appendix-workflow-patch-not-yet-applied) below.
> **Action required:** grant the `claude[bot]` App `workflows: write` on
> this repo, then apply the appendix patch (or re-run daily-improve so it
> can push the edit directly).

## 1. Hacker News: intermittent empty section ("HN live data unavailable")

### Issue

`research/community/2026-05-25-hn.md` degraded in its final pass:

> _HN live data unavailable — network access restricted in this runner
> environment. Snapshot reflects 17:02 UTC state; see cross-platform
> signals below._

This is not a one-off. The same "unavailable / restricted" failure mode
recurs across many community digests — e.g. 2026-01-15, 2026-02-04/05/07,
2026-03-09/14/15/16, 2026-04-15/17/28, 2026-05-07/15/17/18, and again
2026-05-25. On those passes the HN section is empty or frozen, while the
Reddit section in the *same file* is fine.

### Root cause

The asymmetry is the tell. In `4h-community.yml`, **Reddit is pre-fetched
deterministically** in a shell step (`curl` the subreddit RSS feeds into
`data/reddit/*.rss`) and handed to the agent as files. **Hacker News has
no such pre-fetch** — it relies solely on the `mcp-hackernews` MCP server
spun up via `npx -y mcp-hackernews` *inside* the agent. When that MCP
server fails to start, can't reach its upstream, or the agent's tool call
errors, there is no fallback and the HN section goes empty.

### Fix

Gave HN the same deterministic pre-fetch Reddit already has, using the
**Algolia HN Search API** (`hn.algolia.com/api/v1/search?tags=front_page`)
— the public, no-auth JSON backend that powers HN's own search. Verified
today from this environment: returns the live front page (top item was
"Magnifica Humanitas", 1326 pts / 744 comments — matching the day's news),
fast, no anti-bot risk, no documented rate limit for read access.

Edits to `.github/workflows/4h-community.yml`:

- **New step `Fetch Hacker News front page (Algolia)`** curls the
  front-page endpoint (`hitsPerPage=50`) into `/tmp/hn/frontpage.json`,
  with a graceful `|| printf '{"hits":[]}'` fallback and a guard that
  rewrites the file to an empty set if the body doesn't contain `"hits"`
  (defends against HTML error pages). This mirrors the existing Reddit
  RSS step and honors the repo's "fetch gracefully, never crash the run"
  rule (CLAUDE.md #6).
- **New step `Copy HN data to working directory`** copies it to
  `data/hn/frontpage.json` (parallel to `data/reddit/`).
- **Prompt TASK 1 rewritten**: `data/hn/frontpage.json` is now the
  PRIMARY HN source (documented fields: `title`, `url`, `points`,
  `num_comments`, `objectID`; discussion link =
  `news.ycombinator.com/item?id={objectID}`). The `mcp-hackernews` MCP is
  demoted to a best-effort SUPPLEMENT for fresher counts / "new" stories.
  The prompt now explicitly forbids emitting an "HN data unavailable"
  placeholder while `frontpage.json` has hits.

The MCP config is intentionally left in place — when it works it adds
fresher comment counts and "new" (not-yet-front-page) stories on top of
the guaranteed Algolia baseline.

### Expected impact

The HN section of every community digest gets a guaranteed source
independent of the MCP server's reliability. Ends the recurring empty /
frozen HN passes; the section degrades to "front page only" instead of
"nothing" when the MCP is down.

## What was deliberately not changed

- **Daily digest gaps (2026-05-22, -23, -25 missing; last is -24).**
  `research/digest/` is missing three of the last four days. This reads
  as the self-hosted runner being unavailable / the 00:00 job being
  queued or skipped, not a methodology defect — the digest *prompt* and
  inputs are healthy on the days it does run. A workflow edit can't fix a
  runner that isn't executing the job, so no speculative change was made.
  Flagging it for operator attention: confirm the self-hosted runner is
  online and the `Daily AI Digest` schedule is firing. (Note the
  downstream effect: `wiki-ingest.yml` triggers on the digest's
  `workflow_run`, so missing digests also starve the wiki lane.)
- **Bluesky staleness.** `research/bluesky/2026-05-25.md` reported "No
  posts from monitored accounts within the strict 24-hour window" and
  fell back to May 19–22 content. The 2026-05-18 PR already rebuilt this
  lane (14 curated `getAuthorFeed` handles, relaxed engagement gate); the
  remaining thinness is a function of once-daily cadence × a 14-handle
  list on a quiet weekend, and the agent's labeled graceful degradation
  is acceptable. Expanding the handle list risks inventing handles that
  404, so no change was made this pass. Candidate future improvement:
  add a few *verified* high-signal handles and/or widen the lookback to
  48h with clear labeling.
- **`research/twitter-viral/`** is produced by local `scripts/*viral*`
  /`*overperf*` tooling, not a scheduled workflow, so it's out of scope
  for the pipeline-improvement lane (it is, however, undocumented in
  CLAUDE.md's Output Locations — minor doc drift, left for a focused doc
  PR).

## Files changed

- `docs/archive/2026-05-26-improvements.md` (this file) — **the only file
  in this PR**, because the workflow edit could not be pushed (see the
  delivery note at the top).
- `.github/workflows/4h-community.yml` — **patch attached below, not yet
  applied**; needs the `workflows` App permission to land.

## Appendix: workflow patch (not yet applied)

Apply with `git apply` from the repo root once the `workflows` permission
is granted:

```diff
diff --git a/.github/workflows/4h-community.yml b/.github/workflows/4h-community.yml
index bcd011a8..8aeff7d4 100644
--- a/.github/workflows/4h-community.yml
+++ b/.github/workflows/4h-community.yml
@@ -75,6 +75,38 @@ jobs:
           cp /tmp/reddit/*.rss data/reddit/ || echo "No files to copy"
           ls -la data/reddit/
 
+      # Deterministic HN pre-fetch (mirrors the Reddit RSS approach above).
+      # The mcp-hackernews MCP server has failed intermittently inside the
+      # agent ("HN live data unavailable"), leaving the HN section empty.
+      # The Algolia HN Search API is a public, reliable, no-auth JSON
+      # endpoint (the official HN search backend), so fetching it here in a
+      # shell step gives the agent a guaranteed HN source. Graceful fallback
+      # to an empty result set on failure (cf. the bird `|| echo "[]"` rule).
+      - name: Fetch Hacker News front page (Algolia)
+        id: hackernews
+        run: |
+          mkdir -p /tmp/hn
+
+          echo "Fetching HN front page (Algolia)..."
+          curl -sL -m 30 \
+            "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=50" \
+            -H "User-Agent: AIResearchBot/1.0" \
+            > /tmp/hn/frontpage.json || printf '{"hits":[]}\n' > /tmp/hn/frontpage.json
+
+          # Guard against HTML error pages / truncated bodies: if the file
+          # doesn't look like the expected JSON, replace with an empty set.
+          if ! grep -q '"hits"' /tmp/hn/frontpage.json; then
+            echo "Algolia response missing hits[] — writing empty set"
+            printf '{"hits":[]}\n' > /tmp/hn/frontpage.json
+          fi
+          echo "HN frontpage.json size: $(wc -c < /tmp/hn/frontpage.json) bytes"
+
+      - name: Copy HN data to working directory
+        run: |
+          mkdir -p data/hn
+          cp /tmp/hn/*.json data/hn/ || echo "No files to copy"
+          ls -la data/hn/
+
       - name: Create MCP Config
         run: |
           cat > /tmp/mcp-config.json << 'EOF'
@@ -103,8 +135,26 @@ jobs:
 
             ## TASK 1: Hacker News
 
-            Use the Hacker News MCP tools to get current top/new stories.
-            Filter for AI/ML/LLM related content.
+            PRIMARY SOURCE (always available): read the pre-fetched front
+            page from data/hn/frontpage.json. This is the Algolia HN Search
+            API response; each item in hits[] has:
+            - title          (story title)
+            - url            (external link; may be null for Ask/Show HN)
+            - points         (score)
+            - num_comments   (comment count)
+            - objectID       (HN story id)
+
+            Build the HN discussion link as:
+              https://news.ycombinator.com/item?id={objectID}
+
+            Filter hits[] for AI/ML/LLM-related content and rank by points.
+
+            SUPPLEMENT (best-effort): if the Hacker News MCP tools respond,
+            use them to refine scores/comment counts or pull "new" stories
+            not yet on the front page. If the MCP tools error or return
+            nothing, DO NOT leave the HN section empty — the
+            data/hn/frontpage.json file is sufficient on its own. Never emit
+            an "HN data unavailable" placeholder while frontpage.json has hits.
 
             Write to: research/community/${{ steps.datetime.outputs.date }}-hn.md
```
