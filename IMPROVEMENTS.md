# Methodology Improvements - 2026-01-31

## Analysis of 2026-01-30 Output

### Overall Assessment
Yesterday's pipeline produced a comprehensive daily digest covering breaking news, model releases, research, community buzz, funding, and policy. The digest quality was strong with 200+ lines of well-structured content. However, several data collection issues degraded source diversity and coverage.

### Issues Found

#### 1. Bluesky Completely Broken (CRITICAL)
- **Impact**: Zero data collected all day (11 collection attempts, all failed)
- **Root cause**: Bluesky's `public.api.bsky.app/xrpc/app.bsky.feed.searchPosts` endpoint returns 403 Forbidden. This is a [known bug](https://github.com/bluesky-social/bsky-docs/issues/332) with the public AppView API.
- **Evidence**: `research/bluesky/2026-01-30.md` shows "403 Forbidden" for all 11 feed queries

#### 2. Anthropic RSS Feed Broken (HIGH)
- **Impact**: No direct Anthropic blog updates captured via RSS (had to rely on Twitter/news for Anthropic coverage)
- **Root cause**: `openrss.org/www.anthropic.com/news` proxy returns HTML error page instead of valid RSS XML
- **Evidence**: RSS file notes "feed parse error" or "invalid XML token at line 17" in every hourly update

#### 3. Meta AI RSS Feed Broken (HIGH)
- **Impact**: No direct Meta AI blog updates captured
- **Root cause**: `ai.meta.com/blog/rss/` returns Facebook HTML page instead of RSS XML
- **Evidence**: RSS file notes "feed returns Facebook HTML instead of RSS" throughout the day

#### 4. VentureBeat Stale (MEDIUM)
- **Impact**: No VentureBeat articles since January 22 (8 days stale)
- **Root cause**: Feed may be rate-limited or URL changed; most recent article is from Jan 22

#### 5. Twitter Search Queries Outdated (MEDIUM)
- **Impact**: Missing coverage of current-generation hardware and models
- **Details**: Still searching for "NVIDIA H100" (last-gen) instead of H200/B200. Missing current model names like Kimi, DeepSeek V4, Grok, Qwen3. No search for AI agents/MCP (dominant 2026 trend).

#### 6. Missing Key RSS Sources (MEDIUM)
- **Impact**: Coverage gaps in tech journalism
- **Details**: No Ars Technica AI, The Decoder, MIT Technology Review. These outlets often break stories or provide analysis not found in TechCrunch/Verge.

#### 7. Incomplete arXiv Coverage (LOW-MEDIUM)
- **Impact**: Missing NLP and Computer Vision papers
- **Details**: arXiv workflow prompt mentions cs.CL and cs.CV categories but only CS.AI and CS.LG RSS feeds were fetched. NLP and CV papers are significant portions of AI research.

#### 8. Missing Reddit Communities (LOW-MEDIUM)
- **Impact**: Missing consumer AI sentiment and futurism discussions
- **Details**: Only monitoring r/MachineLearning, r/LocalLLaMA, r/artificial. Missing r/singularity (700K+ members, active AI discussion) and r/ChatGPT (large consumer AI community).

## Improvements Made

### Fix 1: Bluesky API Overhaul (`2h-bluesky.yml`)
- **Primary method**: Switched to `getAuthorFeed` for 14 known AI researchers/organizations (Karpathy, Anthropic, OpenAI, Google, HuggingFace, Simon Willison, Ethan Mollick, Jeff Dean, Yann LeCun, etc.)
- **Secondary method**: Kept searchPosts as fallback with HTTP status checking and graceful degradation (logs 403 instead of silently failing)
- **Updated Claude prompt**: Now handles both `feed[].post` and `posts[]` JSON structures

### Fix 2: Anthropic RSS Feed (`hourly-rss.yml`)
- Replaced broken `openrss.org` proxy with community-maintained RSS feed from [conoro/anthropic-engineering-rss-feed](https://github.com/conoro/anthropic-engineering-rss-feed)
- This feed scrapes `anthropic.com/engineering` hourly using Playwright and serves valid RSS XML via GitHub raw content

### Fix 3: Meta AI RSS Feed (`hourly-rss.yml`)
- Replaced broken `ai.meta.com/blog/rss/` with `research.facebook.com/feed/` (Meta Research)
- Added `engineering.fb.com/feed/` (Meta Engineering) as supplementary source
- Both feeds serve valid RSS XML and cover Meta's AI research and engineering posts

### Fix 4: New RSS Sources (`hourly-rss.yml`)
Added 3 new tech news feeds:
- **Ars Technica AI** (`arstechnica.com/ai/feed/`) - High-quality AI journalism
- **The Decoder** (`the-decoder.com/feed/`) - Dedicated AI news site with strong European perspective
- **MIT Technology Review AI** (`technologyreview.com/topic/artificial-intelligence/feed`) - Authoritative AI analysis

Added 2 new arXiv categories:
- **CS.CL** (Computation and Language / NLP)
- **CS.CV** (Computer Vision)

### Fix 5: Twitter Search Queries (`hourly-twitter.yml`)
- Updated hardware terms: H100 -> H200, added B200, Maia 200, TPU v7
- Added current model names: GPT-5, Gemini 3, Kimi, Qwen, DeepSeek, Grok
- Added new search category: AI agents, MCP, Claude Code, Codex, agentic AI
- Added AI IPO to business searches (relevant trend in 2026)

### Fix 6: Reddit Community Coverage (`4h-community.yml`)
Added 2 new subreddits:
- **r/singularity** - Large community (700K+) discussing AI developments, AGI timelines, and societal impact
- **r/ChatGPT** - Consumer AI community with real-world usage insights

## Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Bluesky data collected | 0 posts/day | ~200+ posts/day (14 account feeds + search) |
| Anthropic blog updates | 0 (broken feed) | All engineering blog posts |
| Meta AI blog updates | 0 (broken feed) | Research + engineering posts |
| RSS news sources | 3 (TC, Verge, VB) | 6 (+Ars Technica, The Decoder, MIT TR) |
| arXiv categories | 2 (AI, LG) | 4 (+CL, CV) |
| Reddit communities | 3 | 5 (+singularity, ChatGPT) |
| Twitter search coverage | 7 queries | 8 queries (updated terms) |

These changes should meaningfully improve source diversity and eliminate the data collection failures that affected 2026-01-30 output quality.
