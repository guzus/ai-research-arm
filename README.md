# AI Research

Automated multi-source AI news research agent powered by Claude and MCP.

## Today's Front Page

<!-- FRONT_PAGE_START -->
![Today's Front Page](research/front-page/2026-06-05-front-page.png)
<!-- FRONT_PAGE_END -->

> *Generated daily at 00:30 UTC. See [`research/front-page/`](research/front-page/) for the archive.*

## Architecture

```mermaid
flowchart TB
    subgraph sources["📡 Real-Time Sources"]
        RSS["🔗 RSS Feeds<br/><i>Hourly</i>"]
        Bluesky["🦋 Bluesky<br/><i>Daily</i>"]
        Reddit["🔴 Reddit<br/><i>Every 4h</i>"]
        HN["🟠 Hacker News<br/><i>Every 4h</i>"]
        arXiv["📄 arXiv<br/><i>Daily</i>"]
        Twitter["🐦 Twitter/X<br/><i>Every 3h</i>"]
        Blogs["✍️ Expert Blogs<br/><i>Every 6h</i>"]
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
        blogs_out["research/blogs/"]
    end

    RSS --> rss_out
    Bluesky --> bluesky_out
    Reddit --> community_out
    HN --> community_out
    arXiv --> arxiv_out
    Twitter --> twitter_out
    Blogs --> blogs_out

    rss_out --> Digest
    bluesky_out --> Digest
    community_out --> Digest
    arxiv_out --> Digest
    twitter_out --> Digest
    blogs_out --> Digest

    Exa -.-> Digest
    Perplexity -.-> Digest

    Digest["📊 Daily Digest<br/><i>00:00 UTC</i>"]
    Digest --> digest_out["research/digest/"]

    subgraph improve["🔄 Self-Improvement"]
        Improve["daily-improve.yml<br/><i>00:17 UTC</i>"]
    end

    digest_out --> Improve
    Improve -->|"Creates PRs"| sources

    subgraph dashboard["🖥️ Dashboard"]
        Vercel["Vercel<br/><i>ara.guzus.xyz</i>"]
    end

    twitter_out --> Vercel
```

## Data Sources

| Source | Method | Frequency | Real-time? |
|--------|--------|-----------|------------|
| **Twitter/X** | bird CLI (33 accounts + 7 searches) | Every 3 hours | ✅ Yes |
| **RSS Feeds** | Direct XML fetch | Hourly | ✅ Yes |
| **Bluesky** | Public API | Daily | ✅ Yes |
| **Reddit** | RSS feeds | Every 4 hours | ✅ Yes |
| **Hacker News** | MCP Server | Every 4 hours | ✅ Yes |
| **arXiv** | MCP + RSS | Daily | ✅ Yes |
| **Expert Blogs** | Curated RSS/Atom registry | Every 6 hours | ✅ Yes |
| **Web Search** | Exa/Perplexity MCP | On-demand | ✅ Yes (via MCP) |

## Workflows

```mermaid
gantt
    title Daily Workflow Schedule (UTC)
    dateFormat HH:mm
    axisFormat %H:%M

    section Hourly
    RSS Feeds           :crit, 00:00, 1h

    section Every 3h
    Twitter/X           :active, 00:07, 3h

    section Every 4h
    Community (HN+Reddit) :00:19, 4h

    section Every 6h
    Expert Blogs        :00:13, 6h

    section Twice Daily
    AI News Research    :08:23, 1h

    section Daily
    Bluesky             :00:11, 1h
    arXiv Papers        :06:13, 1h
    Daily Digest        :00:00, 1h
    Self-Improve        :milestone, 00:17, 0h
```

| Workflow | Schedule | Source | Output |
|----------|----------|--------|--------|
| `hourly-rss.yml` | Every hour (:30) | Official blogs, TechCrunch, arXiv RSS | `research/rss/` |
| `daily-ai-blogs.yml` | Every 6 hours (:13) | Curated KOL Substacks, expert blogs, research/operator blogs | `research/blogs/` |
| `2h-bluesky.yml` | Daily 00:11 UTC | Bluesky AI posts | `research/bluesky/` |
| `4h-community.yml` | Every 4 hours | Reddit RSS + HN MCP | `research/community/` |
| `daily-arxiv.yml` | Daily 06:13 UTC | arXiv papers | `research/arxiv/` |
| `daily-digest.yml` | Daily 00:00 UTC | All sources + MCP search | `research/digest/` |
| `hourly-twitter.yml` (matrix) | claude tier every 3h (`:07`), deepseek-claude-code tier every 6h (`:37`), deepseek-pi and fireworks-pi tiers manual | Twitter/X via bird CLI (50+ accounts, 7 search queries) | `research/twitter/` (claude) + `research/twitter-deepseek/` (Claude Code) + `research/twitter-deepseek-pi/` (pi) + `research/twitter-fireworks-pi/` (Fireworks pi) |
| `ai-news-research.yml` | Twice daily (08:23, 20:23 UTC) | Perplexity/Exa MCP | `research/` |
| `daily-improve.yml` | Daily 00:17 UTC | Self-improvement | PRs with improvements |
| `research-issue.yml` | On issue label | Deep research on any topic | `research/issues/` |
| `generative-research.yml` | On `gen-research` issue label or `workflow_dispatch` (`topic` or `twitter_url`) | Claude or DeepSeek writes an HTML article | `research/generative/` |

Dashboard deploys are handled by **Vercel's git integration**, not a workflow file — every push to `main` triggers a build automatically.

`generative-research.yml` defaults to **Claude Opus 4.7** for new manual,
issue-triggered, and auto-dispatched runs. Use `backend=deepseek-v4-pro`
for the DeepSeek V4 Pro comparison path. See
[Generative Research Backends](docs/generative-research-backends.md)
for the exact env mapping and comparison commands.

Twitter-seeded generative research is a first-class manual primitive:
dispatch the workflow with only a tweet/status URL and it will read the
tweet/thread with bird, infer the research question, verify claims
against primary sources, and publish the article through the same
`research/generative/` writer path:

```bash
gh workflow run generative-research.yml \
  -f twitter_url="https://x.com/<handle>/status/<id>" \
  -f backend=claude
```

Claude command: `/gen-research-tweet <twitter-or-x-status-url>`.
Agents command: `.agents/commands/gen-research-tweet.md`.

For a concise framework on which AI industry areas matter most, see
[AI Industry Map](docs/ai-industry-map.md).

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

## Dashboard

Live at **[ara.guzus.xyz](https://ara.guzus.xyz/)**

A single-page dashboard that displays Twitter/X research reports with:
- Warm cream/parchment color palette for readability
- Source Serif 4 body font with Inter UI headings
- Each report time slot rendered as its own card (latest first)
- Clock icon with accurate local time conversion next to UTC timestamps
- @handle highlighting with distinct pill styling
- Section navigation (up/down arrows, keyboard shortcuts)
- Date picker, search, and refresh controls
- Mobile responsive with bottom nav bar

Built with **Vite + Bun + TypeScript**, deployed to Vercel via the git integration (root directory: `dashboard/`). Every push to `main` triggers a Vercel build; the `prebuild` hook in `dashboard/scripts/prebuild.mjs` copies `research/<source>/` into `public/research/` and emits `manifest.json` before Vite runs.

## Setup

### Local Python Tooling

Python dependencies are managed with **uv**:

```bash
uv sync --all-extras
uv run python -m unittest discover -s scripts -p 'test_*.py'
uv run python scripts/check_model_tickets.py
```

### Required Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Yes | Claude Code auth |
| `DEEPSEEK_API_KEY` | Yes for DeepSeek V4 Pro generative research and DeepSeek Twitter workflows | DeepSeek API key used through the Anthropic-compatible endpoint |
| `FIREWORKS_API_KEY` | Yes for the manual `fireworks-pi` Twitter workflow tier | Fireworks API key used by pi's built-in Fireworks provider |
| `BIRD_AUTH_TOKEN` | Yes | X/Twitter auth_token cookie for bird CLI |
| `BIRD_CT0` | Yes | X/Twitter ct0 cookie for bird CLI |
| `GEMINI_API_KEY` | Yes for article/digest audio | Gemini API key used for price-performant TTS audio generation |

### Optional API Keys (for enhanced features)

| Secret | Source | Benefit |
|--------|--------|---------|
| `EXA_API_KEY` | [dashboard.exa.ai](https://dashboard.exa.ai) | Neural web search via MCP |
| `PERPLEXITY_API_KEY` | [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api) | Real-time web search with citations via MCP |

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
│   └── 2026-01-14.md              # Twitter updates (every 3h via bird CLI)
├── issues/
│   └── 42-research.md             # On-demand research from GitHub Issues
├── digest/
│   └── 2026-01-14-digest.md       # Daily synthesized digest (enhanced with MCP tools)
└── summaries/
    └── 2026-01-14-summary.txt     # Telegram digest summaries

dashboard/                          # Vite + Bun + TypeScript SPA
├── src/
│   ├── main.ts                    # App logic, markdown rendering, clock icons
│   └── style.css                  # Warm cream palette, responsive styles
├── index.html                     # Entry point
├── scripts/prebuild.mjs           # Copies research/ into public/, builds manifest.json
├── vercel.json                    # Vercel build settings (framework, install, build)
├── vite.config.js                 # Vite config
└── package.json                   # Dependencies (vite, marked, dompurify)
```

## Data Source Details

### Twitter/X (Every 3 hours)
Via [bird CLI](https://github.com/steipete/bird) — 33 monitored accounts, 20 tweets each, 7 search queries.

**AI Labs & Companies (11):**
OpenAI, Anthropic, Google AI, DeepMind, Mistral, Meta AI, Cohere, AI21Labs, Stability AI, Hugging Face, NVIDIA AI Dev

**Hyperscalers (7):**
Elon Musk, Sam Altman, Demis Hassabis, Logan (Google AI), Alex Albert (Anthropic), Jim Fan (NVIDIA), Roon (OpenAI)

**Researchers, Analysts & Media (15):**
Karpathy, strawberry, Curran, fin (China AI), Jukan (semiconductors), Vitrupo, sankalp, JT, Semi Analysis, Ben Thompson, The Information, Gavin Baker, Mark, NIK, Chubby

**Search queries:** AI models & products, breakthroughs, research papers, infrastructure & hardware, policy & safety, business & funding, open source & dev tools

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

### Bluesky (Daily)
Public API search for:
- AI announcements
- LLM releases
- Model discussions
- ML papers
- Key researchers (Karpathy, etc.)

### Reddit (Every 4 hours)
RSS feeds (no API key needed):
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

See [docs/archive/](./docs/archive/) for improvement history and prior ideas.

## Resources

- [Claude Code Action](https://github.com/anthropics/claude-code-action)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Reddit RSS Feeds](https://www.reddit.com/wiki/rss/)
- [Bluesky API Docs](https://docs.bsky.app/)
