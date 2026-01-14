# AI Research

Automated AI news research agent powered by Claude and MCP (Model Context Protocol).

## Features

- Automated AI news research every 4 hours
- Uses Exa and Tavily MCP servers for web search
- Generates structured markdown reports
- Tracks the latest developments in AI

## Setup

### Required Secrets

Add these secrets to your GitHub repository (Settings > Secrets and variables > Actions):

| Secret | Description | Get it from |
|--------|-------------|-------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code authentication | Already set up via `/install-github-app` |
| `EXA_API_KEY` | Exa AI search API key | [dashboard.exa.ai](https://dashboard.exa.ai) |
| `TAVILY_API_KEY` | Tavily search API key (fallback) | [app.tavily.com](https://app.tavily.com) |

### MCP Servers Used

This project uses the following MCP servers in GitHub Actions:

1. **[Exa MCP Server](https://github.com/exa-labs/exa-mcp-server)** - Primary search tool
   - `web_search_exa`: Real-time web search
   - `deep_search_exa`: Deep search with query expansion

2. **[Tavily MCP Server](https://github.com/tavily-ai/tavily-mcp)** - Fallback search
   - Controlled web search with filtering options

### Other Recommended MCP Servers

| MCP Server | Use Case | Link |
|------------|----------|------|
| Perplexity MCP | AI-powered search with reasoning | [docs.perplexity.ai](https://docs.perplexity.ai/guides/mcp-server) |
| Brave Search MCP | Privacy-focused web search | [github.com/anthropics/brave-search-mcp](https://github.com/anthropics/brave-search-mcp) |
| Google News MCP | News-specific searches | [mcp.so](https://mcp.so) |
| MCP Omnisearch | Unified multi-provider search | [github.com/spences10/mcp-omnisearch](https://github.com/spences10/mcp-omnisearch) |

## Workflows

### AI News Research (`ai-news-research.yml`)

- **Schedule**: Every 4 hours
- **Output**: `research/YYYY-MM-DD-ai-news.md`
- **Manual trigger**: Go to Actions > AI News Research Agent > Run workflow

### Claude Code Review (`claude-code-review.yml`)

- **Trigger**: On PR open/update
- **Action**: Automated code review

### Claude Code (`claude.yml`)

- **Trigger**: Mention `@claude` in issues/PRs
- **Action**: Interactive code assistance

## Using MCP in GitHub Actions

Yes, MCP servers work in GitHub Actions via `anthropics/claude-code-action`:

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
      Then commit the changes.
```

## Resources

- [Claude Code Action Solutions](https://github.com/anthropics/claude-code-action/blob/main/docs/solutions.md) - Examples for scheduled workflows, file operations, and more
- [Claude Code Action Configuration](https://github.com/anthropics/claude-code-action/blob/main/docs/configuration.md) - Full configuration reference
