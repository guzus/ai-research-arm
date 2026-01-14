# AI Research

Automated multi-source AI news research agent powered by Claude and MCP (Model Context Protocol).

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI Research Pipeline                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │ Twitter  │   │ Hacker   │   │  Reddit  │   │  arXiv   │     │
│  │ (hourly) │   │  News    │   │ (4 hrs)  │   │ (daily)  │     │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘     │
│       │              │              │              │             │
│       ▼              ▼              ▼              ▼             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              research/ directory                         │    │
│  │  ├── twitter/YYYY-MM-DD.md                              │    │
│  │  ├── community/YYYY-MM-DD-hn.md                         │    │
│  │  ├── community/YYYY-MM-DD-reddit.md                     │    │
│  │  ├── arxiv/YYYY-MM-DD-papers.md                         │    │
│  │  └── digest/YYYY-MM-DD-digest.md                        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                    │
│                              ▼                                    │
│                    ┌──────────────────┐                          │
│                    │   Daily Digest   │                          │
│                    │   (11 PM UTC)    │                          │
│                    └──────────────────┘                          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Workflows

| Workflow | Schedule | Source | Output |
|----------|----------|--------|--------|
| `hourly-twitter.yml` | Every hour | Twitter/X | `research/twitter/` |
| `4h-community.yml` | Every 4 hours | Hacker News, Reddit | `research/community/` |
| `daily-arxiv.yml` | Daily 6 AM UTC | arXiv papers | `research/arxiv/` |
| `daily-digest.yml` | Daily 11 PM UTC | All sources | `research/digest/` |
| `ai-news-research.yml` | Every 4 hours | Web search | `research/` |

## Setup

### Required Secrets

Add these secrets to your GitHub repository (Settings > Secrets and variables > Actions):

| Secret | Required | Description | Get it from |
|--------|----------|-------------|-------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Yes | Claude Code authentication | `/install-github-app` |
| `EXA_API_KEY` | No | Exa AI search (enhanced) | [dashboard.exa.ai](https://dashboard.exa.ai) |
| `TWITTER_BEARER_TOKEN` | No | Twitter API access | [developer.twitter.com](https://developer.twitter.com) |
| `REDDIT_CLIENT_ID` | No | Reddit API access | [reddit.com/prefs/apps](https://reddit.com/prefs/apps) |
| `REDDIT_CLIENT_SECRET` | No | Reddit API secret | Same as above |

### MCP Servers Used

| Server | Purpose | NPM Package |
|--------|---------|-------------|
| [Exa](https://github.com/exa-labs/exa-mcp-server) | Web search | `exa-mcp-server` |
| [Hacker News](https://github.com/paabloLC/mcp-hacker-news) | HN stories | `mcp-hackernews` |
| [arXiv](https://github.com/blazickjp/arxiv-mcp-server) | Research papers | `arxiv-mcp-server` |
| [Twitter](https://github.com/EnesCinr/twitter-mcp) | Twitter/X | `@mcp/twitter-server` |

## Output Structure

```
research/
├── twitter/
│   └── 2026-01-14.md          # Hourly Twitter updates (appended)
├── community/
│   ├── 2026-01-14-hn.md       # Hacker News digest
│   └── 2026-01-14-reddit.md   # Reddit digest
├── arxiv/
│   └── 2026-01-14-papers.md   # Daily arXiv papers
├── digest/
│   └── 2026-01-14-digest.md   # Synthesized daily digest
└── 2026-01-14-ai-news.md      # General web search results
```

## Data Sources Strategy

### Tier 1: Real-time (Hourly)
- **Twitter/X**: Breaking announcements from @OpenAI, @AnthropicAI, @GoogleDeepMind, key researchers

### Tier 2: Community Signal (Every 4 hours)
- **Hacker News**: Tech community curated, high signal-to-noise
- **Reddit**: r/MachineLearning, r/LocalLLaMA for deeper technical discussions

### Tier 3: Research (Daily)
- **arXiv**: New papers in cs.AI, cs.LG, cs.CL, cs.CV

### Tier 4: Synthesis (Daily)
- **Daily Digest**: Combines all sources into executive summary

## Manual Triggers

All workflows support manual triggering via GitHub Actions UI:
1. Go to Actions tab
2. Select the workflow
3. Click "Run workflow"

## Using MCP in GitHub Actions

```yaml
- name: Create MCP Config
  run: |
    cat > /tmp/mcp-config.json << 'EOF'
    {
      "mcpServers": {
        "exa": {
          "command": "npx",
          "args": ["-y", "exa-mcp-server"],
          "env": {
            "EXA_API_KEY": "${{ secrets.EXA_API_KEY }}"
          }
        }
      }
    }
    EOF

- uses: anthropics/claude-code-action@v1
  with:
    claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
    claude_args: |
      --mcp-config /tmp/mcp-config.json
      --allowedTools "Read,Write,Edit,Bash(git:*),mcp__exa__web_search_exa"
    prompt: |
      Search for AI news and save a report to research/report.md
```

## Resources

- [Claude Code Action Solutions](https://github.com/anthropics/claude-code-action/blob/main/docs/solutions.md)
- [Claude Code Action Configuration](https://github.com/anthropics/claude-code-action/blob/main/docs/configuration.md)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Servers Directory](https://mcp.so/)
