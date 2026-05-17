# Methodology Improvements Log

This file tracks improvements made to the AI research pipeline by the self-improvement workflow.

## How It Works

The `daily-improve.yml` workflow runs daily at 00:17 UTC and:
1. Analyzes yesterday's research output quality
2. Identifies coverage gaps and issues
3. Searches for new/better data sources
4. Creates a PR with proposed improvements

## Improvement History

### 2026-01-14 - Initial Setup

**Sources Added:**
- RSS feeds: OpenAI, Anthropic, Google AI, DeepMind, Meta AI, Hugging Face, TechCrunch, The Verge, VentureBeat, arXiv
- Bluesky: Public API search for AI content
- Reddit: RSS feeds (r/MachineLearning, r/LocalLLaMA, r/artificial)
- Hacker News: MCP server integration

**Architecture:**
- Hourly RSS feed checks
- 2-hour Bluesky updates
- 4-hour community digests
- Daily arXiv paper curation
- Daily synthesized digest

---

## Ideas for Future Improvements

- [ ] Add Discord server monitoring (AI Discord communities)
- [ ] Add Telegram channel feeds
- [ ] Add GitHub trending repos for AI
- [ ] Add AI newsletter aggregation
- [ ] Add podcast transcript summaries
- [ ] Add YouTube AI channel monitoring
- [ ] Add LinkedIn AI influencer tracking
- [ ] Improve filtering with ML-based relevance scoring
- [ ] Add sentiment analysis for community discussions
- [ ] Add citation tracking for research papers
