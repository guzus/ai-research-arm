# Methodology Improvements - 2026-02-02

## Analysis of 2026-02-01 Output

### Quality Assessment
- **Digest quality**: Excellent. The daily digest was comprehensive, well-structured, and covered all major stories with strong executive summary.
- **Twitter coverage**: Strong. 12 update cycles captured ~80 unique items across all categories.
- **arXiv coverage**: Good. 770+ papers processed with clear top-5 highlights and categorized tables.
- **Community (HN/Reddit)**: Adequate but limited. Only 3 subreddits monitored — missed significant discussions on r/singularity, r/ChatGPT, and r/OpenAI.
- **RSS coverage**: Weak. Only 15 articles captured from 3 tech news sites (TechCrunch, The Verge, VentureBeat). Many major publications not monitored.
- **Bluesky**: Complete failure. All 11 fetch attempts returned 403 Forbidden errors throughout the entire day. Zero posts collected.

### Issues Identified

#### 1. CRITICAL: Bluesky API Completely Down (0 posts captured all day)
The Bluesky `searchPosts` public API endpoint has been returning 403 errors consistently. This is a known upstream issue — Bluesky restricted unauthenticated access to the search endpoint (confirmed via GitHub issues bluesky-social/bsky-docs#332 and bluesky-social/atproto#2838).

**Fix**: Added authenticated session support via `BSKY_HANDLE` and `BSKY_APP_PASSWORD` secrets. The workflow now creates an authenticated session before making search requests, with graceful fallback to public API if credentials aren't configured. Also added 2 new search queries for AI safety and open source AI.

#### 2. HIGH: Anthropic and Meta AI RSS Feeds Still Broken
Despite previous improvements, both feeds consistently returned HTML pages instead of RSS XML throughout 2026-02-01. Every hourly check showed "Feed unavailable (returns HTML instead of RSS)".

**Fix**: Added RSS content validation after each fetch — if the response doesn't contain RSS/Atom XML markers (`<rss`, `<feed`, `<channel`), the workflow automatically tries alternative proxy sources (OpenRSS, RSS.app) as fallbacks.

#### 3. HIGH: RSS Source Coverage Still Too Narrow
Yesterday's RSS captured articles from only TechCrunch, The Verge, and VentureBeat. Missing major AI-focused publications:
- Wired AI, Ars Technica AI, MIT Technology Review — high-quality analytical coverage
- IEEE Spectrum AI — engineering perspective
- NVIDIA AI Blog, Microsoft AI Blog — infrastructure/hardware insights
- Unite.AI — dedicated AI news aggregator
- arXiv CS.CL — NLP papers (monitored daily but not hourly)

**Fix**: Added 8 new RSS feeds plus arXiv CS.CL for hourly monitoring. Total RSS sources: 11 -> 20 (+82%).

#### 4. MEDIUM: Reddit Coverage Misses Major Communities
Only r/MachineLearning, r/LocalLLaMA, and r/artificial were monitored. Missing:
- r/singularity — one of the most active AI discussion communities
- r/ChatGPT — 9M+ members, major product/UX discussions
- r/OpenAI — company-specific news and product updates

**Fix**: Added all three subreddits with proper rate-limiting (sleep 2 between requests).

#### 5. MEDIUM: Twitter Missing Key Voices from Yesterday's News
Several accounts that generated significant content in yesterday's coverage were not directly monitored:
- @romanyam (Roman Yampolskiy) — AI safety warnings
- @GaryMarcus — AI criticism and commentary
- @AdriGarriga — mechanistic interpretability researcher
- @iannuttall — broke the "Moltroad" black market story
- @Dan_Jeffries1 — led verification vs. alignment debate

Also missing dedicated search queries for Chinese AI labs (critical given mid-February DeepSeek V4/Qwen 3.5 releases) and AI agents/agentic workflows.

**Fix**: Added 6+ new monitored accounts and 2 new search queries.

---

## Changes Made

### `.github/workflows/2h-bluesky.yml`
- Added Bluesky authentication step (BSKY_HANDLE, BSKY_APP_PASSWORD secrets)
- Authenticated requests use `bsky.social/xrpc` endpoint instead of `public.api.bsky.app`
- Graceful fallback to public API if no credentials configured
- Added proper error handling with `|| echo '{"posts":[]}'` on all requests
- Added 2 new search queries: "AI safety alignment" and "open source AI model"
- Updated Claude prompt to include new data files (ai_safety.json, opensource_ai.json)

### `.github/workflows/hourly-rss.yml`
- **8 new RSS feeds**: Wired AI, Ars Technica AI, MIT Technology Review, IEEE Spectrum, NVIDIA Blog, Microsoft AI, Unite.AI, arXiv CS.CL
- **RSS validation**: Added content validation for Anthropic feed — checks for RSS markers, tries RSS.app as fallback
- **RSS validation**: Added content validation for Meta AI feed — checks for RSS markers, tries OpenRSS proxy as fallback
- Updated Claude prompt with complete feed list and expanded output format sections

### `.github/workflows/4h-community.yml`
- Added 3 new Reddit subreddits: r/singularity, r/ChatGPT, r/OpenAI
- Added proper rate-limiting (sleep 2) between Reddit requests
- Updated Claude prompt with new data sources
- Updated output format with new subreddit sections

### `.github/workflows/hourly-twitter.yml`
- Added @xaboratory (xAI lab) to monitored lab accounts
- Added @romanyam, @GaryMarcus, @AdriGarriga, @iannuttall, @Dan_Jeffries1 to monitored accounts
- Added search query: "DeepSeek OR Qwen OR ByteDance AI OR Moonshot AI" (Chinese AI labs)
- Added search query: "AI agent framework OR agentic AI OR MCP server" (AI agents)
- Updated RAW DATA LOCATIONS in Claude prompt

---

## Expected Impact

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| RSS feed sources | 11 | 20 | +82% |
| Reddit subreddits | 3 | 6 | +100% |
| Twitter monitored accounts | ~70 | ~77 | +10% |
| Twitter search queries | 7 | 9 | +29% |
| Bluesky search queries | 5 | 7 | +40% |
| Bluesky data (2026-02-01) | 0 posts | Expected recovery | Critical fix |
| Broken RSS feeds (Anthropic, Meta) | Silent failure | Validated + fallback | Bug fix |

### Coverage Improvements
- **Broader tech press**: Wired, Ars Technica, MIT Tech Review, IEEE Spectrum bring deeper analytical coverage
- **Hardware/infrastructure**: NVIDIA and Microsoft blogs fill hardware/cloud gap
- **Community scale**: r/singularity and r/ChatGPT add millions of users' perspectives
- **Chinese AI**: Dedicated search query ensures coverage of DeepSeek V4, Qwen 3.5, ByteDance releases
- **AI agents**: Dedicated search covers the rapidly growing agent ecosystem
- **Bluesky recovery**: Authenticated API should restore data collection

*Generated by Daily Self-Improvement Workflow on 2026-02-02*
