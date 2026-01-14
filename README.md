# AI Research

Automated multi-source AI news research agent powered by Claude and MCP.

## Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AI Research Pipeline                             │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  REAL-TIME SOURCES                                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │   RSS    │ │ Bluesky  │ │  Reddit  │ │  Hacker  │ │  arXiv   │     │
│  │ (hourly) │ │ (2 hrs)  │ │  JSON    │ │  News    │ │ (daily)  │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
│       │            │            │            │            │            │
│       ▼            ▼            └─────┬──────┘            ▼            │
│  ┌─────────┐ ┌─────────┐       ┌─────┴─────┐       ┌─────────┐        │
│  │research/│ │research/│       │ research/ │       │research/│        │
│  │  rss/   │ │bluesky/ │       │community/ │       │ arxiv/  │        │
│  └────┬────┘ └────┬────┘       └─────┬─────┘       └────┬────┘        │
│       │           │                  │                  │              │
│       └───────────┴────────┬─────────┴──────────────────┘              │
│                            ▼                                           │
│                   ┌────────────────┐                                   │
│                   │  Daily Digest  │                                   │
│                   │  (11 PM UTC)   │                                   │
│                   └────────────────┘                                   │
│                            │                                           │
│                            ▼                                           │
│                   research/digest/                                     │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## Data Sources

| Source | Method | Frequency | Real-time? |
|--------|--------|-----------|------------|
| **RSS Feeds** | Direct XML fetch | Hourly | ✅ Yes |
| **Bluesky** | Public API | Every 2 hours | ✅ Yes |
| **Reddit** | JSON endpoint | Every 4 hours | ✅ Yes |
| **Hacker News** | MCP Server | Every 4 hours | ✅ Yes |
| **arXiv** | MCP + RSS | Daily | ✅ Yes |
| **Web Search** | Exa/WebSearch | Every 4 hours | Cached |

## Workflows

| Workflow | Schedule | Source | Output |
|----------|----------|--------|--------|
| `hourly-rss.yml` | Every hour | Official blogs, TechCrunch, arXiv RSS | `research/rss/` |
| `2h-bluesky.yml` | Every 2 hours | Bluesky AI posts | `research/bluesky/` |
| `4h-community.yml` | Every 4 hours | Reddit JSON + HN MCP | `research/community/` |
| `daily-arxiv.yml` | Daily 6 AM UTC | arXiv papers | `research/arxiv/` |
| `daily-digest.yml` | Daily 11 PM UTC | All sources | `research/digest/` |
| `hourly-twitter.yml` | Every hour | Twitter/X (needs API key) | `research/twitter/` |
| `daily-improve.yml` | Daily midnight | Self-improvement | PRs with improvements |

## Setup

### Required Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Yes | Claude Code auth |

### Optional API Keys (for enhanced features)

| Secret | Source | Benefit |
|--------|--------|---------|
| `EXA_API_KEY` | [dashboard.exa.ai](https://dashboard.exa.ai) | Better web search |
| `TWITTER_BEARER_TOKEN` | [developer.twitter.com](https://developer.twitter.com) | Direct Twitter access |

## Output Structure

```
research/
├── rss/
│   └── 2026-01-14.md              # Official blog posts, tech news
├── bluesky/
│   └── 2026-01-14.md              # Bluesky AI researcher posts
├── community/
│   ├── 2026-01-14-hn.md           # Hacker News digest
│   └── 2026-01-14-reddit.md       # Reddit real-time posts
├── arxiv/
│   └── 2026-01-14-papers.md       # Daily arXiv papers
├── twitter/
│   └── 2026-01-14.md              # Twitter updates (if API key set)
└── digest/
    └── 2026-01-14-digest.md       # Daily synthesized digest
```

## Data Source Details

### RSS Feeds (Hourly)
Official announcements from:
- OpenAI Blog
- Anthropic News
- Google AI Blog
- DeepMind Blog
- Meta AI Blog
- Hugging Face Blog
- TechCrunch AI
- The Verge AI
- VentureBeat AI
- arXiv CS.AI & CS.LG

### Bluesky (Every 2 hours)
Public API search for:
- AI announcements
- LLM releases
- Model discussions
- ML papers
- Key researchers (Karpathy, etc.)

### Reddit (Every 4 hours)
Direct JSON endpoint (no API key needed):
- r/MachineLearning
- r/LocalLLaMA
- r/artificial

### Hacker News (Every 4 hours)
MCP Server for:
- Top AI/ML stories
- Trending discussions

## Manual Triggers

All workflows can be triggered manually:
1. Go to Actions tab
2. Select workflow
3. Click "Run workflow"

## Self-Improvement System

The pipeline includes a **self-improving meta-workflow** (`daily-improve.yml`) that:

1. **Analyzes** yesterday's research output quality
2. **Identifies** coverage gaps and data freshness issues
3. **Searches** for new MCP servers, RSS feeds, and data sources
4. **Creates PRs** with proposed improvements

This creates a feedback loop where the system continuously improves its own methodology.

See [IMPROVEMENTS_LOG.md](./IMPROVEMENTS_LOG.md) for improvement history and future ideas.

## Resources

- [Claude Code Action](https://github.com/anthropics/claude-code-action)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Reddit JSON API](https://data365.co/blog/reddit-json-api)
- [Bluesky API Docs](https://docs.bsky.app/)
