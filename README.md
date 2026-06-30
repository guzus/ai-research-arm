![AI Research Arm — an automated AI-news intelligence pipeline](assets/banner.png)

# AI Research Arm

Automated multi-source AI news research agent powered by Claude and MCP.

## Today's Front Page

<!-- FRONT_PAGE_START -->
![Today's Front Page](research/front-page/2026-06-30-front-page.png)
<!-- FRONT_PAGE_END -->

> *Generated daily at 00:30 UTC. See [`research/front-page/`](research/front-page/) for the archive.*

## Quickstart (no accounts needed)

Prerequisites: [Bun](https://bun.sh) and [Git LFS](https://git-lfs.com) — the
committed front-page images are stored with Git LFS, so a `git clone` with
git-lfs installed hydrates them automatically (the dashboard prebuild fails on
unhydrated LFS pointers).

The dashboard builds and runs against the sample research data already
committed in this repo — no API keys or secrets required:

```bash
cd dashboard
bun install
bun run dev          # local dev server at http://localhost:5173
# or: bun run build  # production build into dashboard/dist/
```

Python tooling is stdlib-first and managed with [uv](https://docs.astral.sh/uv/):

```bash
uv sync --all-extras
uv run python -m unittest discover -s scripts -p 'test_*.py'
```

Running the **full data pipeline** needs the maintainer's accounts and
infrastructure — see [What you can run vs. what needs accounts](#what-you-can-run-vs-what-needs-accounts).

## Architecture

```mermaid
flowchart TB
    subgraph sources["📡 Real-Time Sources"]
        RSS["🔗 RSS Feeds<br/><i>Every 2h</i>"]
        Bluesky["🦋 Bluesky<br/><i>Daily</i>"]
        Reddit["🔴 Reddit<br/><i>Every 4h</i>"]
        HN["🟠 Hacker News<br/><i>Every 4h</i>"]
        arXiv["📄 arXiv<br/><i>Daily</i>"]
        Twitter["🐦 Twitter/X<br/><i>Every 3h</i>"]
        Blogs["✍️ Expert Blogs<br/><i>Every 6h</i>"]
        YouTube["▶️ YouTube/tuber<br/><i>Daily</i>"]
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
        youtube_out["research/youtube/"]
    end

    RSS --> rss_out
    Bluesky --> bluesky_out
    Reddit --> community_out
    HN --> community_out
    arXiv --> arxiv_out
    Twitter --> twitter_out
    Blogs --> blogs_out
    YouTube --> youtube_out

    rss_out --> Digest
    bluesky_out --> Digest
    community_out --> Digest
    arxiv_out --> Digest
    twitter_out --> Digest
    blogs_out --> Digest
    youtube_out --> Digest

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
        Railway["Railway<br/><i>ara.guzus.xyz</i>"]
    end

    twitter_out --> Railway
```

## Data Sources

| Source | Method | Frequency | Real-time? |
|--------|--------|-----------|------------|
| **Twitter/X** | bird CLI (reviewed account manifest + 7 searches) | Every 3 hours | ✅ Yes |
| **RSS Feeds** | Direct XML fetch | Every 2 hours | ✅ Yes |
| **Bluesky** | Public API | Daily | ✅ Yes |
| **Reddit** | RSS feeds | Every 4 hours | ✅ Yes |
| **Hacker News** | MCP Server | Every 4 hours | ✅ Yes |
| **arXiv** | MCP + RSS | Daily | ✅ Yes |
| **Expert Blogs** | Curated RSS/Atom registry | Every 6 hours | ✅ Yes |
| **YouTube** | tuber API discovery + read-only summaries/transcripts | Daily | ✅ Yes |
| **Web Search** | Exa/Perplexity MCP | On-demand | ✅ Yes (via MCP) |

## Workflows

```mermaid
gantt
    title Daily Workflow Schedule (UTC)
    dateFormat HH:mm
    axisFormat %H:%M

    section Every 2h
    RSS Feeds           :crit, 00:30, 2h

    section Every 3h
    Twitter/X           :active, 00:07, 3h

    section Every 4h
    Community (HN+Reddit) :00:19, 4h

    section Every 6h
    Expert Blogs        :00:13, 6h

    section Twice Daily
    AI News Research    :08:23, 1h

    section Daily
    YouTube Signal      :23:20, 1h
    Bluesky             :00:11, 1h
    arXiv Papers        :06:13, 1h
    Daily Digest        :00:00, 1h
    Self-Improve        :milestone, 00:17, 0h
```

| Workflow | Schedule | Source | Output |
|----------|----------|--------|--------|
| `hourly-rss.yml` | Every 2 hours (:30) | Official blogs, TechCrunch, arXiv RSS | `research/rss/` |
| `daily-ai-blogs.yml` | Every 6 hours (:13) | Curated KOL Substacks, expert blogs, research/operator blogs | `research/blogs/` |
| `daily-youtube.yml` | Daily 23:20 UTC for the next 00:00 digest | tuber API trending/search/channel metadata, existing summaries, transcript probes | `research/youtube/` |
| `2h-bluesky.yml` | Daily 00:11 UTC | Bluesky AI posts | `research/bluesky/` |
| `4h-community.yml` | Every 4 hours | Reddit RSS + HN MCP | `research/community/` |
| `daily-arxiv.yml` | Daily 06:13 UTC | arXiv papers | `research/arxiv/` |
| `daily-digest.yml` | Daily 00:00 UTC | All sources + MCP search | `research/digest/` |
| `hourly-twitter.yml` (matrix) | claude tier every 3h (`:07`), deepseek-claude-code tier every 6h (`:37`), deepseek-pi and fireworks-pi tiers manual | Twitter/X via bird CLI (reviewed account manifest, 7 search queries) | `research/twitter/` (claude) + `research/twitter-deepseek/` (Claude Code) + `research/twitter-deepseek-pi/` (pi) + `research/twitter-fireworks-pi/` (Fireworks pi) |
| `ai-news-research.yml` | Twice daily (08:23, 20:23 UTC) | Perplexity/Exa MCP | `research/` |
| `daily-improve.yml` | Daily 00:17 UTC | Self-improvement | PRs with improvements |
| `twitter-account-explorer.yml` | Weekly (Tue 01:47 UTC) + manual | Scouts high-signal AI accounts; trust-weighted curation of `data/sources/twitter_accounts.json` | Reviewed PRs (`app/claude`) |
| `research-issue.yml` | On issue label | Deep research on any topic | `research/issues/` |
| `generative-research.yml` | On `gen-research` issue label or `workflow_dispatch` (`topic` or `twitter_url`) | Claude, Codex, or Fireworks-backed models write an HTML article | `research/generative/` |

Dashboard deploys are handled by **Railway's git integration**, not a workflow file — every push to `main` rebuilds the root `Dockerfile` (bun build → Caddy serve) automatically.

`generative-research.yml` defaults to **Claude Opus 4.8** for new manual,
issue-triggered, and auto-dispatched runs. Use `backend=codex` for the OpenAI
Codex GitHub Action path, `backend=deepseek-v4-flash` for the DeepSeek V4 Flash
comparison path, or `backend=glm-5p2` for the GLM 5.2 Fireworks path. See
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

For portable data sharing from the ARA wiki, see
[Open Knowledge Format for ARA](docs/okf.md).

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

Built with **Vite + Bun + TypeScript**, deployed by Railway from the root `Dockerfile` (bun build → Caddy serve, behind Cloudflare; see also `Caddyfile` and `railway.json`). Every push to `main` triggers a Railway rebuild; the `prebuild` hook in `dashboard/scripts/prebuild.mjs` copies `research/<source>/` into `public/research/` and emits `manifest.json` before Vite runs.

## Setup

### Local Python Tooling

Python dependencies are managed with **uv**:

```bash
uv sync --all-extras
uv run python -m unittest discover -s scripts -p 'test_*.py'
uv run python scripts/check_model_tickets.py
```

### Required Secrets

All credentials are injected via GitHub Actions secrets (or a local `.env`,
which is gitignored) — see [`.env.example`](.env.example) for the full
annotated list of pipeline credentials. None of these are needed for the
[Quickstart](#quickstart-no-accounts-needed).

| Secret | Required | Description |
|--------|----------|-------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Yes | Claude Code auth |
| `CODEX_AUTH_JSON` | Yes for generative-research `backend=codex` | File-backed ChatGPT Codex auth cache from `~/.codex/auth.json` after `codex login`; treat like a password |
| `DEEPSEEK_API_KEY` | No — retired | DeepSeek lanes now route through Fireworks (`FIREWORKS_API_KEY`); no longer referenced by any workflow |
| `FIREWORKS_API_KEY` | Yes for generative-research `backend=deepseek-v4-flash` / `backend=glm-5p2` and all non-claude Twitter tiers (`deepseek-claude-code`, `deepseek-pi`, `fireworks-pi`) | Fireworks API key — serves DeepSeek V4 Flash and GLM 5.2 via the Anthropic-compatible endpoint, and Kimi via pi's Fireworks provider |
| `BIRD_AUTH_TOKEN` | Yes | X/Twitter auth_token cookie for bird CLI |
| `BIRD_CT0` | Yes | X/Twitter ct0 cookie for bird CLI |
| `GEMINI_API_KEY` | Yes for article/digest audio | Gemini API key used for price-performant TTS audio generation |

### Optional API Keys (for enhanced features)

| Secret | Source | Benefit |
|--------|--------|---------|
| `EXA_API_KEY` | [dashboard.exa.ai](https://dashboard.exa.ai) | Neural web search via MCP |
| `PERPLEXITY_API_KEY` | [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api) | Real-time web search with citations via MCP |

**Note:** Exa and Perplexity integrate as MCP (Model Context Protocol) tools, giving Claude enhanced web search capabilities during research workflows.

## What you can run vs. what needs accounts

This repo is one person's live pipeline, published as-is. Much of it is
reproducible; some of it points at the maintainer's private infrastructure and
is included for transparency rather than turnkey reuse.

**Runs with no accounts:**
- The **dashboard** — builds and serves from the sample data committed under
  `research/` (see [Quickstart](#quickstart-no-accounts-needed)).
- The **Python tooling + tests** — stdlib-first, `uv`-managed; validators and
  unit tests run offline.

**Needs your own credentials (drop-in):**
- **Claude / Codex / Fireworks backends** — set `CLAUDE_CODE_OAUTH_TOKEN`,
  `CODEX_AUTH_JSON`, or `FIREWORKS_API_KEY` for the synthesis/generative lane
  you want to run on your fork. The Codex lane uses ChatGPT-managed Codex
  auth, not OpenAI API billing.
- **Twitter/X lanes** — supply your own `BIRD_AUTH_TOKEN` / `BIRD_CT0` cookies
  (they expire often; lanes degrade to empty data without them).
- **Exa / Perplexity** search enrichment and **Gemini** TTS are all optional.

**Maintainer-specific (swap or disable to self-host):**
- **Runners:** nearly every workflow targets a private self-hosted Cloud Run
  fleet (`runs-on: [self-hosted, Linux]`); on a fork those jobs queue until you
  point them at your own runners (or change `runs-on`).
- **Services:** `hooker.guzus.xyz` (telemetry — no-ops if `HOOKER_URL` is
  unset), `tuber-api.guzus.xyz` (YouTube signal — no public equivalent), and
  `s3.guzus.xyz` (audio hosting). Override the non-secret endpoints via the env
  vars in [`.env.example`](.env.example) (`AUDIO_BASE_URL`,
  `POSTBUILD_SITE_ORIGIN`, `DEPLOY_HEALTH_URL`, …).
- **Deploy:** production is a Railway service watching `main`, and
  `ara.guzus.xyz` is the maintainer's domain. The static dashboard shell also
  embeds a Google Analytics tag in `dashboard/index.html` — remove it on a fork.
- **Sibling repos** `../oracle` and `../runner` referenced in the docs are
  private and not required for the default Claude/Codex/Fireworks paths.

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
├── vite.config.js                 # Vite config
└── package.json                   # Dependencies (vite, marked, dompurify)
```

## Data Source Details

### Twitter/X (Every 3 hours)
Via [bird CLI](https://github.com/steipete/bird) and birdy multi-fetch. The
reviewed source manifest is `data/sources/twitter_accounts.json` (currently 80
monitored accounts, periodically expanded by the explorer lane below), 20
tweets each, 7 search queries, and the AI-only news tab. Account add/remove
proposals are generated with `scripts/curate_twitter_accounts.py`; see
[`docs/twitter-account-curation.md`](docs/twitter-account-curation.md) for the
full contract. A weekly `twitter-account-explorer.yml` agent scouts for
high-signal additions — favoring accounts vouched for by ones already monitored
and on-topic for AI over merely viral handles — and opens reviewed PRs (as
`app/claude`) when the evidence is strong enough.

**Account groups:** AI labs/company accounts; hyperscalers, executives, and key
insiders; researchers, analysts, builders, and media.

**Search queries:** AI models & products, breakthroughs, research papers,
infrastructure & hardware, policy & safety, business & funding, open source &
dev tools

### RSS Feeds (Every 2 Hours)
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

## License

The **source code** in this repository (scripts, workflows, the dashboard, and
documentation) is released under the [MIT License](LICENSE).

The **contents of `research/`** are a different matter: they are automated
excerpts, summaries, and reproductions of third-party material (news articles
and posts from X/Twitter, Hacker News, Reddit, Bluesky, arXiv, and similar
sources) produced as the pipeline's output. They are **not** relicensed by the
MIT grant and remain the property of their original authors. If you reuse
anything under `research/`, you are responsible for complying with the original
sources' terms — including the X/Twitter Terms of Service and each publisher's
copyright.

Contributing: [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) ·
Security: [`.github/SECURITY.md`](.github/SECURITY.md)
