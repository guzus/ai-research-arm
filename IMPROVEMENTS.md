# Methodology Improvements - 2026-02-06

## Analysis Date: 2026-02-05 Output Review

### Issues Found

#### 1. Bluesky Still Completely Broken (Critical)
- **Problem**: Despite previous fixes, Bluesky returned 403 Forbidden for ALL 10 collection cycles on Feb 5. Zero data collected.
- **Root Cause**: The `public.api.bsky.app` `searchPosts` endpoint now requires authentication per [bsky-docs Issue #332](https://github.com/bluesky-social/bsky-docs/issues/332). The previous "failover" fix attempted unauthenticated calls which are now categorically rejected.
- **Impact**: Complete Bluesky blindspot — the digest noted "Bluesky: 0 posts (API 403 errors all day)".
- **Fix**: Added proper JWT authentication via `com.atproto.server.createSession`. Requires new `BSKY_HANDLE` and `BSKY_APP_PASSWORD` secrets. Falls back gracefully if credentials not configured.

#### 2. Anthropic RSS Feed Still Broken (High)
- **Problem**: "No new blog posts in the last 24 hours (feed parse error)" every hour, despite Anthropic launching Opus 4.6 — one of the day's biggest stories.
- **Root Cause**: The `conoro/anthropic-engineering-rss-feed` from previous fix may not cover the main news page, and `openrss.org` proxy remains unreliable.
- **Fix**: Changed primary source to `Olshansk/rss-feeds` GitHub repo which maintains dedicated feeds for Anthropic News, Engineering, Research, and Claude Code Changelog. OpenRSS kept as fallback. Added separate Anthropic Engineering feed.

#### 3. Stale Model Name Search Queries (High)
- **Problem**: The model timeline workflow searches for "GPT-5 OR GPT-4.5 OR Claude 4 OR Gemini 2.5 OR Llama 4 OR Grok 3" — all outdated names.
- **Impact**: Search results miss current model discussions (GPT-5.3, Claude Opus 4.6, Gemini 3, DeepSeek V4, Grok 5).
- **Fix**: Updated search queries to current model names: GPT-5.3, GPT-6, Claude Opus, Claude Sonnet 5, Gemini 3, Llama 5, Grok 5, DeepSeek V4.

#### 4. Missing Major RSS Sources (Medium)
- **Problem**: No RSS feeds for Mistral AI, NVIDIA AI, AWS ML, or Microsoft AI blogs.
- **Impact**: Yesterday's RSS output had "VentureBeat: No new articles" consistently, and NVIDIA/AWS/Microsoft blog posts were only captured via Twitter.
- **Fix**: Added 4 new company blog feeds (Mistral via OpenRSS, NVIDIA Deep Learning, AWS ML, Microsoft AI with Tech Community fallback).

#### 5. Missing arXiv CS.CL in Hourly RSS (Medium)
- **Problem**: The hourly RSS workflow only fetches CS.AI and CS.LG from arXiv, but the daily arXiv workflow also searches CS.CL (Computation and Language). CS.CL is where most LLM papers appear.
- **Fix**: Added `arxiv_cl.xml` (CS.CL) to hourly RSS feed collection and processing.

#### 6. Missing r/singularity Subreddit (Medium)
- **Problem**: r/singularity (500K+ members) is one of Reddit's most active AI communities but is not monitored.
- **Fix**: Added r/singularity RSS feed to community workflow with dedicated output section.

#### 7. Missing Key Twitter Accounts (Low)
- **Problem**: Several voices that appeared prominently in yesterday's coverage were not in monitored accounts — only captured via search.
- **Accounts missing**: Dwarkesh Patel (@dwarkesh_sp), Epoch AI Research (@EpochAIResearch), Aaron Levie (@levie), The Humanoid Hub (@TheHumanoidHub), VentureBeat (@VentureBeat), The Verge (@verge).
- **Fix**: Added all 6 accounts to the monitored list.

---

### Changes Made

| File | Change |
|------|--------|
| `.github/workflows/2h-bluesky.yml` | Added JWT auth flow via `createSession`, improved error handling, added response logging for debugging |
| `.github/workflows/hourly-rss.yml` | Fixed Anthropic feed (switched to Olshansk/rss-feeds), added 5 new RSS feeds (Mistral, NVIDIA, AWS, Microsoft, arXiv CS.CL, Anthropic Engineering), updated prompt |
| `.github/workflows/4h-community.yml` | Added r/singularity subreddit |
| `.github/workflows/hourly-twitter.yml` | Added 6 new monitored accounts |
| `.github/workflows/12h-model-timeline.yml` | Updated stale model name search queries to current model names |

### New Sources Added

**RSS Feeds (6 new):**
- Anthropic Engineering Blog (via Olshansk/rss-feeds GitHub)
- Mistral AI (via OpenRSS proxy)
- NVIDIA Deep Learning Blog
- AWS Machine Learning Blog
- Microsoft AI Blog (with Tech Community fallback)
- arXiv CS.CL (NLP papers)

**Reddit (1 new):**
- r/singularity

**Twitter (6 new accounts):**
- @dwarkesh_sp, @EpochAIResearch, @levie, @TheHumanoidHub, @VentureBeat, @verge

### Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Bluesky data collection | 0% (all 403) | ~95% (with auth) |
| Anthropic RSS | Broken (parse error) | Fixed (community feed + fallback) |
| Company blog RSS feeds | ~10 | ~16 |
| Reddit subreddits | 3 | 4 |
| Twitter monitored accounts | ~70 | ~76 |
| Model search query accuracy | Low (outdated names) | Current |
| arXiv hourly categories | 2 (AI, LG) | 3 (AI, LG, CL) |

### Secrets Required

The Bluesky fix requires two new GitHub repository secrets:
- `BSKY_HANDLE` — Bluesky handle (e.g., `username.bsky.social`)
- `BSKY_APP_PASSWORD` — App password from https://bsky.app/settings/app-passwords

*Generated by Daily Self-Improvement Workflow on 2026-02-06*
