# Methodology Improvements — 2026-06-22

## Concrete defect observed

**The r/LocalLLaMA Reddit lane has produced zero content for at least three
consecutive days, at every collection cycle.**

Evidence (committed output):

- `research/community/2026-06-21-reddit.md` — r/LocalLLaMA section empty at
  **all four** cycles (10:36, 14:59, 18:31, 22:05 UTC); lines 21-23, 48-50,
  77-79, 106-108: *"RSS feed returned no entries at collection time."*
- `research/community/2026-06-20-reddit.md` line 39: *"Feed unavailable
  (empty RSS) — no data for this run."*
- `research/community/2026-06-19-reddit.md` lines 35, 63, 90, 132: *"No posts
  available at time of fetch (feed empty)."* (every cycle)

This is not a transient blip — it is a persistent, silent lane degradation.
It also caused a **topic-relevant** coverage gap: the 2026-06-21 daily digest's
single biggest theme was the open-weights moat thesis (Zhipu's MIT-licensed
**GLM-5.2**). r/LocalLLaMA is the canonical community for local/open-weight
model discussion, and it contributed nothing on the exact day its core topic
led the news.

## Root cause

`.github/workflows/4h-community.yml`, the "Fetch Reddit RSS feeds" step,
fetched each subreddit feed exactly once with a generic
`User-Agent: AIResearchBot/1.0` and performed **no validation, no retry, and
no HTTP-status logging**:

```sh
curl -sL "https://www.reddit.com/r/LocalLLaMA/hot.rss?limit=25" \
  -H "User-Agent: AIResearchBot/1.0" > /tmp/reddit/localllama.rss
echo "LocalLLaMA RSS size: $(wc -c < /tmp/reddit/localllama.rss) bytes"
```

Reddit rate-limits/blocks generic bot User-Agents and datacenter IPs (the
ephemeral Cloud Run workers) by returning HTTP 429 with an empty or HTML body.
The single-shot fetch then silently wrote that empty body, and the curator
agent faithfully reported "feed empty." Notably the HN fetch in the same
workflow already validates its response (`grep -q '"hits"'`) and falls back to
an empty set — the Reddit fetch had none of that hardening. The step logged
only the byte count, so 429-vs-genuinely-empty was indistinguishable in the
run logs.

## Fix

Replaced the three single-shot Reddit fetches with a hardened `fetch_feed`
shell helper that, per feed:

1. Sends a **descriptive, Reddit-compliant User-Agent**
   (`web:ai-research-arm:1.0 (by /u/ai-research-arm)`) instead of the generic
   bot string Reddit 429s.
2. **Retries up to 3× with linear backoff** (3s, 6s, 9s).
3. **Validates** the body actually contains Atom `<entry>` items and the HTTP
   status is 200 before accepting it.
4. **Falls back to `old.reddit.com`** (less aggressively gated for RSS) when
   `www.reddit.com` keeps failing.
5. **Logs the HTTP status code** on every attempt, so future blocking is
   diagnosable from the run log.
6. **Always exits 0** with the best body obtained, so a still-blocked feed
   degrades gracefully and never crashes the run (CLAUDE.md load-bearing
   rule #6).

The change is confined to the fetch step; the curator-agent prompt, output
format, and commit/push flow are untouched.

## Expected impact

- r/LocalLLaMA (and r/artificial, which was empty at 3 of 4 cycles on
  06-21) recover content on the majority of runs instead of returning empty,
  restoring the open-weights/local-model community signal the digest depends
  on.
- When Reddit *does* hard-block a worker IP, the run log now shows the HTTP
  status (e.g. `429`) per attempt instead of an undifferentiated byte count,
  so the failure is diagnosable rather than silent.
- No new dependencies; stays curl-based and graceful, matching the existing
  HN-fetch hardening pattern already in the same workflow.
