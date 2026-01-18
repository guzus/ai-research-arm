# AI Research

Automated multi-source AI news research agent powered by Claude and MCP.

## Architecture

```mermaid
flowchart TB
    subgraph sources["📡 Real-Time Sources"]
        RSS["🔗 RSS Feeds<br/><i>Hourly</i>"]
        Bluesky["🦋 Bluesky<br/><i>Every 2h</i>"]
        Reddit["🔴 Reddit<br/><i>Every 4h</i>"]
        HN["🟠 Hacker News<br/><i>Every 4h</i>"]
        arXiv["📄 arXiv<br/><i>Daily</i>"]
        Twitter["🐦 Twitter/X<br/><i>Hourly</i>"]
    end

    subgraph mcp["🔌 MCP Tools (Optional)"]
        Exa["Exa Search"]
        Perplexity["Perplexity"]
    end

    subgraph storage["📁 Research Storage"]
        rss_out["research/rss/"]
        bluesky_out["research/bluesky/"]
        community_out["research/community/"]
        arxiv_out["research/arxiv/"]
        twitter_out["research/twitter/"]
    end

    RSS --> rss_out
    Bluesky --> bluesky_out
    Reddit --> community_out
    HN --> community_out
    arXiv --> arxiv_out
    Twitter --> twitter_out

    rss_out --> Digest
    bluesky_out --> Digest
    community_out --> Digest
    arxiv_out --> Digest
    twitter_out --> Digest

    Exa -.-> Digest
    Perplexity -.-> Digest

    Digest["📊 Daily Digest<br/><i>11 PM UTC</i>"]
    Digest --> digest_out["research/digest/"]

    subgraph improve["🔄 Self-Improvement"]
        Improve["daily-improve.yml<br/><i>Midnight UTC</i>"]
    end

    digest_out --> Improve
    Improve -->|"Creates PRs"| sources
```

## Data Sources

| Source | Method | Frequency | Real-time? |
|--------|--------|-----------|------------|
| **RSS Feeds** | Direct XML fetch | Hourly | ✅ Yes |
| **Bluesky** | Public API | Every 2 hours | ✅ Yes |
| **Reddit** | JSON endpoint | Every 4 hours | ✅ Yes |
| **Hacker News** | MCP Server | Every 4 hours | ✅ Yes |
| **arXiv** | MCP + RSS | Daily | ✅ Yes |
| **Web Search** | Exa/Perplexity MCP | On-demand | ✅ Yes (via MCP) |

## Workflows

```mermaid
gantt
    title Daily Workflow Schedule (UTC)
    dateFormat HH:mm
    axisFormat %H:%M

    section Hourly
    RSS Feeds           :crit, 00:00, 1h
    Twitter/X           :00:00, 1h

    section Every 2h
    Bluesky             :active, 00:00, 2h

    section Every 4h
    Community (HN+Reddit) :00:00, 4h
    AI News Research    :00:00, 4h

    section Daily
    arXiv Papers        :06:00, 1h
    Daily Digest        :23:00, 1h
    Self-Improve        :milestone, 00:00, 0h
```

| Workflow | Schedule | Source | Output |
|----------|----------|--------|--------|
| `hourly-rss.yml` | Every hour | Official blogs, TechCrunch, arXiv RSS | `research/rss/` |
| `2h-bluesky.yml` | Every 2 hours | Bluesky AI posts | `research/bluesky/` |
| `4h-community.yml` | Every 4 hours | Reddit JSON + HN MCP | `research/community/` |
| `daily-arxiv.yml` | Daily 6 AM UTC | arXiv papers | `research/arxiv/` |
| `daily-digest.yml` | Daily 11 PM UTC | All sources + MCP search | `research/digest/` |
| `hourly-twitter.yml` | Every hour | Twitter/X (needs API key) | `research/twitter/` |
| `ai-news-research.yml` | Every 4 hours | Perplexity/Exa MCP | `research/` |
| `daily-improve.yml` | Daily midnight | Self-improvement | PRs with improvements |
| `research-issue.yml` | On issue label | Deep research on any topic | `research/issues/` |

## On-Demand Research Agent

Request deep research on any topic by creating a GitHub Issue with the `research` label.

### How to Use

1. **Create a new issue** with your research question as the title
2. **Add the `research` label** to the issue
3. **Claude will automatically:**
   - Acknowledge the request with a comment
   - Search the web using multiple tools (WebSearch, Exa, Perplexity)
   - Fetch and analyze relevant documentation, articles, and code
   - Create a comprehensive research report
   - Post findings back to the issue

### Example Research Requests

| Issue Title | What Claude Researches |
|-------------|------------------------|
| "Research how to make AI UGC for my iOS app" | AI-powered user-generated content tools, SDKs, APIs for iOS |
| "Best practices for LLM fine-tuning in 2026" | Latest fine-tuning techniques, tools, and frameworks |
| "Compare vector databases for RAG applications" | Pinecone vs Weaviate vs Chroma vs Milvus comparison |
| "How to implement voice cloning ethically" | Voice synthesis APIs, legal considerations, implementation guides |

### Research Output

Reports are saved to `research/issues/{issue-number}-research.md` with:

- **Executive Summary** - Quick overview of findings
- **Key Findings** - Detailed analysis by category
- **Recommended Approaches** - Ranked options with pros/cons
- **Tools & Libraries** - Relevant SDKs, APIs, frameworks
- **Code Examples** - Working code snippets
- **Resources** - Links to docs, tutorials, repos
- **Next Steps** - Actionable recommendations

### Trigger Methods

| Method | When It Triggers |
|--------|------------------|
| Create issue with `research` label | Immediately on issue creation |
| Add `research` label to existing issue | Immediately when label is added |

## Setup

### Required Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Yes | Claude Code auth |

### Optional API Keys (for enhanced features)

| Secret | Source | Benefit |
|--------|--------|---------|
| `EXA_API_KEY` | [dashboard.exa.ai](https://dashboard.exa.ai) | Neural web search via MCP |
| `PERPLEXITY_API_KEY` | [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api) | Real-time web search with citations via MCP |
| `TWITTER_BEARER_TOKEN` | [developer.twitter.com](https://developer.twitter.com) | Direct Twitter access |

**Note:** Exa and Perplexity integrate as MCP (Model Context Protocol) tools, giving Claude enhanced web search capabilities during research workflows.

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
├── issues/
│   └── 42-research.md             # On-demand research from GitHub Issues
└── digest/
    └── 2026-01-14-digest.md       # Daily synthesized digest (enhanced with MCP tools)
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
