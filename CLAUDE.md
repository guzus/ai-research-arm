# CLAUDE.md

## Project Overview

Automated AI news research pipeline that aggregates intelligence from Twitter/X, RSS feeds, Bluesky, Hacker News, Reddit, and arXiv. Produces daily digests with breaking news, model releases, research highlights, and industry trends.

## GitHub Actions Workflows

All workflows use `anthropics/claude-code-action@v1` and run on a self-hosted runner.

### Model Configuration

Pass the model via `claude_args`, not as a separate `model:` input:

```yaml
# Correct (v1)
claude_args: "--model opus"

# Wrong (beta format, do not use)
model: claude-opus-4-5-20251101
```

Reference: https://code.claude.com/docs/en/github-actions

### Common claude_args patterns

```yaml
claude_args: |
  --model opus --allowedTools "Read,Write,Edit,Bash(git:*)"
  --max-turns 10
```

### Authentication

- `CLAUDE_CODE_OAUTH_TOKEN` — Claude Code OAuth token
- `BIRD_AUTH_TOKEN` / `BIRD_CT0` — X/Twitter cookies for bird CLI
- `GITHUB_TOKEN` — auto-provided for git push

## Repository Structure

- `research/twitter/` — Twitter/X updates (every 3 hours)
- `research/rss/` — RSS feed articles (hourly)
- `research/bluesky/` — Bluesky posts (daily)
- `research/community/` — HN and Reddit discussions (every 4 hours)
- `research/arxiv/` — arXiv papers (daily)
- `research/digest/` — Daily synthesized digests
- `research/summaries/` — Digest summaries for Telegram
- `research/front-page/` — Daily newspaper-style PNG front pages
- `.github/workflows/` — All automation workflows

## Code Style

- Workflow files: YAML with comments for each logical section
- Commit messages: descriptive, e.g. "Twitter update 2026-01-27 15:36 UTC"
- Bird CLI: always use `--json --plain` flags and graceful fallback (`|| echo "[]"`)
