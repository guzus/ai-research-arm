# CLAUDE.md

Operating guide for AI agents working in this repo. Read this before
touching workflows, research output, or the dashboard.

## Project Overview

`ai-research-arm` (ARA) is an automated AI-news intelligence pipeline.
GitHub Actions on a self-hosted Linux runner aggregate signal from
Twitter/X, RSS, Bluesky, Hacker News, Reddit, and arXiv; synthesize it
into daily digests, model-release timelines, and long-form generative
articles; and publish everything to a Vite/TS SPA at
**[ara.guzus.xyz](https://ara.guzus.xyz)**.

## Core Pipeline Architecture

```
sources (Twitter/RSS/Bluesky/HN/Reddit/arXiv)
    → aggregator workflows (hourly/4h/daily) write into research/<source>/
    → synthesis workflows (digest, news research, model timeline) read research/
    → output workflows (front-page, generative-research) produce shareable artifacts
    → dashboard prebuild copies research/* into dashboard/public/research/
    → Vercel git integration auto-builds and deploys on every push to main
```

Daily-improve runs at the tail of the cycle, reads yesterday's output,
and opens a PR with methodology fixes.

## Key Components

| Path | What it is |
|---|---|
| [`ARA_DSL.md`](ARA_DSL.md) | Source format for generative-research articles. The compiler at `scripts/compile_ara.py` turns `.ara.md` into a validated `<article>` fragment. |
| [`COMPONENTS.md`](COMPONENTS.md) | Reference for the `ara-*` component vocabulary the validator enforces. The CSS at `dashboard/src/components/ara-research.css` is the live source of truth — currently ~113 classes vs ~81 documented (see "Known drift" below). |
| [`docs/generative-research-backends.md`](docs/generative-research-backends.md) | Backend matrix for the generative-research lane (Claude vs DeepSeek vs local Oracle), env mapping, comparison commands. |
| [`docs/model-tickets.md`](docs/model-tickets.md) | Schema + lifecycle + dedup protocol for `research/models/tickets/*.md`. Read by the CRUD agent in `24h-model-timeline.yml` and enforced by `scripts/check_model_tickets.py`. |
| [`docs/wiki-schema.md`](docs/wiki-schema.md) | Canonical schema + page conventions for the LLM Wiki (`research/wiki/`). Read at runtime by the ingest agent in `wiki-ingest.yml` and enforced by `scripts/check_wiki.py`. |
| [`docs/hooker-telemetry.md`](docs/hooker-telemetry.md) | Non-blocking telemetry route via `https://hooker.guzus.xyz` topic `ara-telemetry`. |
| [`docs/archive/`](docs/archive/) | Historical improvement logs and superseded docs. |
| `dashboard/` | Vite + Bun + TypeScript SPA. `prebuild.mjs` copies `research/*` into `public/research/` and emits `manifest.json`; Vercel auto-deploys on every push to `main`. |
| `data/` | Static lookup data used by aggregation scripts. |
| `research/` | All generated artifacts. Subdir map in "Output Locations" below. |

### Scripts (`scripts/`)

| Script | Purpose |
|---|---|
| `compile_ara.py` | `.ara.md` → validated HTML fragment. |
| `decompile_ara.py` | HTML fragment → `.ara.md` source (round-trip). |
| `check_generative_research.py` | Pre-commit validator. Tag/class allowlist + optional `--diversity-min`, `--callout-max`, `--strict-shape` design gates. Exit 0 = safe to commit. |
| `write_generative_research.py` | Single publisher for `research/generative/`. Validates body, writes HTML + DSL source, updates `index.json`, commits. |
| `run_generative_research_oracle.py` | Local runner: bundles ARA docs + recent research, calls `../oracle` (GPT-5.5 Pro), extracts `.ara.md`, runs the validator with `--diversity-min 3 --callout-max 5 --strict-shape`, then hands to the writer. |
| `prior_context.py` | Find prior generative-research articles related to a new topic. |
| `research_search.py` | Specialized search wrappers for primary-source research. |
| `stock_prices.py` | Yahoo Finance time series → copy-paste lines for `:::line-chart`. |
| `dedupe_headline_alerts.py` | Filter + record delivered Twitter headline alerts (used by `hourly-twitter.yml`). |
| `check_model_tickets.py` | Validator for `research/models/tickets/*.md` against the schema in `docs/model-tickets.md`. The CRUD agent in `24h-model-timeline.yml` runs it after every pass; CI runs it on every PR. |
| `check_wiki.py` | Validator for `research/wiki/` pages against the schema in `docs/wiki-schema.md`. `uv run python scripts/check_wiki.py` (exit 0 = safe); `--lint` adds advisory checks. The ingest agent in `wiki-ingest.yml` runs it until exit 0; CI runs it on every PR. |
| `wiki_search.py` | Search wrapper over `research/wiki/` (`uv run python scripts/wiki_search.py "<query>"`). The ingest agent runs it before writing any page so it UPDATEs an existing page instead of duplicating. |
| `check_lane_freshness.py` | Freshness watchdog. Measures git-commit recency per research lane against per-lane cadence thresholds; exits 2 (and emits a hooker/Telegram alert from `liveness-check.yml`) when a lane is stale. Stdlib-only so it runs on both runner tiers. |
| `test_ara_dsl.py`, `test_dedupe_headline_alerts.py` | Pytest-style tests run in CI. |

## GitHub Actions Workflows

Workflows split between two runners:

- **`runs-on: ubuntu-latest`** — stateless workflows (no bird-CLI state,
  no LFS hydration, no Puppeteer/Chrome, no warm caches). These run on
  GitHub-hosted runners so they don't queue behind the single self-hosted
  job slot. Currently: `hourly-rss.yml`, `daily-arxiv.yml`,
  `2h-bluesky.yml`, `daily-improve.yml`, `claude-code-review.yml`,
  `claude.yml`.
- **`runs-on: [self-hosted, Linux]`** — workflows that genuinely need
  the self-hosted runner's persistent state (bird CLI + birdy daemon,
  LFS-hydrated `research/` checkout, Puppeteer/Chrome, large agent
  pipelines). Currently: `hourly-twitter.yml`,
  `hourly-twitter-deepseek-*.yml`, `daily-digest.yml`,
  `daily-front-page.yml`, `generative-research.yml`,
  `24h-model-timeline.yml`, `ai-news-research.yml`, `ci.yml`,
  `research-issue.yml`, `4h-community.yml`, `wiki-ingest.yml`.
- **Both tiers** — `liveness-check.yml` (the freshness watchdog) runs one
  job on each runner. No single runner survives both failure modes — an
  `ubuntu-latest` billing/spending-limit block (kills the GitHub-hosted
  tier) vs. a self-hosted outage — so the watchdog must run on both;
  whichever tier is alive emits the hooker/Telegram alert. See the
  workflow header for the rationale.

Claude workflows use `anthropics/claude-code-action@v1` with the model
passed via `claude_args: "--model opus"` (never as a separate `model:`
input).

### Aggregation (raw signal → `research/<source>/`)

| Workflow | Schedule | Output |
|---|---|---|
| `hourly-rss.yml` | `:30` every hour | `research/rss/` |
| `hourly-twitter.yml` | every 3h `:07` | `research/twitter/` + `research/summaries/` + Telegram headline alerts |
| `hourly-twitter-deepseek-agentic.yml` | every 6h `:37` | `research/twitter-deepseek/` (DeepSeek V4 Pro via Anthropic shim, capped at 5 follow-up bird calls) |
| `hourly-twitter-deepseek-pi.yml` | manual only | `research/twitter-deepseek-pi/` (A/B test using `pi-mono` harness) |
| `2h-bluesky.yml` | daily `00:11` | `research/bluesky/` |
| `4h-community.yml` | every 4h `:19` | `research/community/*-hn.md`, `*-reddit.md` |
| `daily-arxiv.yml` | daily `06:13` | `research/arxiv/` |

### Synthesis (digests + analysis from aggregated data)

| Workflow | Schedule | Output |
|---|---|---|
| `daily-digest.yml` | daily `00:00` | `research/digest/` |
| `ai-news-research.yml` | twice daily `08:23`, `20:23` | `research/` (broad topic sweep via Perplexity/Exa MCP) |
| `24h-model-timeline.yml` | daily `06:29` | `research/models/tickets/<slug>.md` (CRUD'd per release/event) + `research/models/<date>-timeline.md` (derived daily-diff) |
| `wiki-ingest.yml` | after the digest (via `workflow_run` on `Daily AI Digest (All Sources)`; `workflow_dispatch` fallback) | `research/wiki/` (CRUD'd pages — one per entity/concept/theme — from the curated digest + model tickets) |

### Output (shareable artifacts)

| Workflow | Trigger | Output |
|---|---|---|
| `daily-front-page.yml` | daily `00:30` (after digest) | `research/front-page/YYYY-MM-DD-front-page.png` |
| `generative-research.yml` | `gen-research` issue label or `workflow_dispatch` with `topic` or `twitter_url` | `research/generative/*.{html,ara.md}` + `index.json` |
| `research-issue.yml` | issue labeled `research` | `research/issues/{issue-number}-research.md` |

### Meta (CI, code-review, self-improvement)

| Workflow | Trigger | Purpose |
|---|---|---|
| `daily-improve.yml` | daily `00:17` | Opens improve/YYYY-MM-DD PR with workflow fixes. See "Load-bearing rules" for where the IMPROVEMENTS file belongs. |
| `ci.yml` | push/PR on workflows/dashboard/scripts | actionlint + dashboard build + Python tests |
| `claude.yml` | `@claude` mention in issue/PR/review | Interactive Claude-Code agent |
| `claude-code-review.yml` | PR opened/synced | Automated Claude code review |

Model convention: most Claude workflows pin `--model opus`. Cost-driven
moves to Sonnet/Haiku for specific steps are made on a per-PR basis;
defer to whatever the workflow file actually says rather than assuming
opus everywhere.

## Backends

| Backend | When | Auth | Notes |
|---|---|---|---|
| **Claude (default)** | All Claude workflows; `generative-research backend=claude` | `CLAUDE_CODE_OAUTH_TOKEN` | Native Anthropic. `claude-opus-4-7` for generative-research. |
| **DeepSeek V4 Pro (shim)** | `generative-research backend=deepseek-v4-pro`; the two `hourly-twitter-deepseek-*` workflows | `DEEPSEEK_API_KEY` | Uses Anthropic-compatible endpoint at `https://api.deepseek.com/anthropic`. Overrides `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_MODEL` so the Claude Code action transparently calls DeepSeek. Subagents use `deepseek-v4-flash`. Generative-research retries up to 2x on socket drops before commit. |
| **Local Oracle (GPT-5.5 Pro)** | `scripts/run_generative_research_oracle.py` | Local `../oracle` checkout (browser engine by default) | Runs entirely on the developer machine; outputs go through the same `check_generative_research.py` → `write_generative_research.py` contract. Source metadata: `local-oracle`. |

Backend selection details, env-var mapping, and comparison commands:
`docs/generative-research-backends.md`.

### Twitter-Seeded Generative Research

`generative-research.yml` accepts `twitter_url` as a standalone
`workflow_dispatch` input. When set, `topic` is optional. The workflow
stages the URL in `.gen-input/twitter_url.txt`; the agent must read the
tweet/thread with `bird read` and `bird thread`, infer the underlying
research question, treat the tweet as primary evidence only for what the
author said, and verify the underlying claims against independent
primary sources before writing the article.

Command entry points:

```bash
/gen-research-tweet https://x.com/<handle>/status/<id>
```

```bash
gh workflow run generative-research.yml \
  -f twitter_url="https://x.com/<handle>/status/<id>" \
  -f backend=claude
```

## Output Locations

```
research/
├── arxiv/                     # daily-arxiv.yml
├── audio/                     # ad-hoc audio artifacts
├── bluesky/                   # 2h-bluesky.yml
├── community/                 # 4h-community.yml (-hn.md, -reddit.md)
├── digest/                    # daily-digest.yml
├── front-page/                # daily-front-page.yml (PNG)
├── generative/                # generative-research.yml + Oracle runner (HTML + .ara.md + index.json)
├── issues/                    # research-issue.yml
├── models/                    # 24h-model-timeline.yml
│   ├── tickets/                # persistent set, one .md per shipping artifact
│   └── <date>-timeline.md      # derived daily diff (created/updated/closed counts)
├── rss/                       # hourly-rss.yml
├── summaries/                 # hourly-twitter.yml (Telegram digest + headline-alert state)
├── twitter/                   # hourly-twitter.yml
├── twitter-deepseek/          # hourly-twitter-deepseek-agentic.yml
├── twitter-deepseek-pi/       # hourly-twitter-deepseek-pi.yml
└── wiki/                      # wiki-ingest.yml (compounding LLM knowledge base)
    ├── index.md                # entry point / page directory
    ├── log.md                  # append-only ingest log (one entry per run)
    ├── entities/               # companies, models, people, products
    ├── concepts/               # techniques, architectures, benchmarks, ideas
    └── themes/                 # ongoing storylines / trends
```

## Authentication

Secrets are configured in GitHub Actions. None are committed.

| Secret | Used by | Notes |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | All Claude workflows | Required. |
| `DEEPSEEK_API_KEY` | `generative-research backend=deepseek-v4-pro`, `hourly-twitter-deepseek-*` | Required when running the DeepSeek lane. |
| `BIRD_AUTH_TOKEN`, `BIRD_CT0` | All bird-CLI workflows (`hourly-twitter*`, `24h-model-timeline`) | X/Twitter cookies. |
| `EXA_API_KEY`, `PERPLEXITY_API_KEY` | `daily-digest`, `ai-news-research`, `research-issue` | Optional; enhance MCP search. |
| `HOOKER_TOKEN` | Telemetry composite action | Optional; without it, telemetry steps no-op. |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | `hourly-twitter*` | For headline alert delivery. |
| `GITHUB_TOKEN` | All workflows | Auto-provided. |

## Load-bearing Rules

These are the conventions that, if broken, will silently corrupt
output or break the pipeline. Read them before editing.

1. **ARA DSL round-trip is mandatory.** Every commit to
   `research/generative/` must go through
   `scripts/compile_ara.py` (`.ara.md` → HTML) and pass
   `scripts/check_generative_research.py` (tag/class allowlist plus
   optional `--diversity-min`, `--callout-max`, `--strict-shape`
   design gates). `scripts/write_generative_research.py` is the
   **only** committer for that directory — it re-validates at write
   time. Workflows that bypass the writer will fail review.

2. **The validator is exact-match.** Class tokens must start with
   `ara-` *and* be documented in `COMPONENTS.md` (or be a valid
   `--variant` suffix of a documented class). Tags outside the
   allowlist (`<style>`, `<script>`, `<iframe>`, `<h1>`, inline
   `style=`, `on*=`, `javascript:` URLs) are rejected. Reach for
   `:::raw` only when the DSL genuinely can't express the shape;
   invented classes still fail.

3. **Dashboard deploys are git-push driven.** Vercel watches `main`
   and rebuilds on every push (root `dashboard/`). There is no
   workflow file for deploys. `dashboard/scripts/prebuild.mjs` copies
   `research/<source>/` into `public/research/` and emits
   `manifest.json` before Vite runs. Touching it changes what the
   dashboard sees.

4. **Hooker telemetry is non-blocking.** Every workflow's final step
   posts to `https://hooker.guzus.xyz` via the local composite at
   `.github/actions/hooker-telemetry`. It must never fail a job —
   `continue-on-error: true` style. Don't add hard dependencies on
   telemetry success.

5. **Runner choice is load-bearing — pick by state dependency.** Two
   runners, two rules:
   - **Self-hosted** for workflows that depend on baked-in state: bird
     CLI + warm birdy daemon (`hourly-twitter*`, `24h-model-timeline`),
     LFS-hydrated `research/` for prior-output context
     (`daily-digest`, `daily-front-page`, `ci.yml` dashboard job),
     Puppeteer/Chrome (`daily-front-page`), or pre-installed
     pnpm/Oracle tooling.
   - **`ubuntu-latest`** for stateless workflows. The self-hosted runner
     processes one job at a time; stateless work on `ubuntu-latest`
     frees that queue. See the "GitHub Actions Workflows" section for
     the current split. Before flipping a workflow from self-hosted to
     `ubuntu-latest`, verify it doesn't read pre-populated dirs, depend
     on warm caches, or need bird/birdy state — the cost of getting
     this wrong is a silently-broken pipeline.

6. **bird CLI calls must be graceful.** Always pass `--json --plain`
   and pipe to a fallback (`|| echo "[]"`). The Twitter cookies expire;
   workflows must continue (with empty data) rather than crash the run.

7. **Improvement logs belong in `docs/archive/`.** When
   `daily-improve.yml` (or any agent) generates a new improvements
   file, write it to `docs/archive/YYYY-MM-DD-improvements.md`, not
   to repo root. The workflow prompt still says "Create an
   IMPROVEMENTS.md" — that text predates this rule. Follow this rule,
   not the older prompt.

8. **Atomic file writes.** Long-running aggregation scripts that
   write into `research/` should write to a temp file in the same
   directory and `os.replace()` into place, so a half-finished file
   never reaches Vercel's prebuild.

9. **Model tickets are CRUD'd, not regenerated.**
   `research/models/tickets/<slug>.md` is the persistent store for the
   model-release timeline — one ticket per shipping artifact (release,
   partnership, funding round, legal action). The `24h-model-timeline.yml`
   CRUD agent reads the existing tickets + last 24h of signal and
   chooses create/update/close per the protocol in
   `docs/model-tickets.md`. Never regenerate the table by deleting and
   re-writing tickets. Slugs are immutable; `history` is append-only;
   closure preserves history. `scripts/check_model_tickets.py` enforces
   the schema (5 canonical states: rumored → in-testing → confirmed →
   released → closed). The legacy `<date>-timeline.md` files (frozen
   format) remain on disk; new dates produce a *derived diff* summarizing
   what the agent did.

10. **Wiki pages are CRUD'd, not regenerated.** `research/wiki/` is a
    compounding knowledge base — one markdown page per entity, concept,
    or theme, plus `index.md` (the page directory) and an append-only
    `log.md` (one `## [YYYY-MM-DD] ingest | <summary>` entry per run).
    The `wiki-ingest.yml` agent runs daily *after the digest*
    (`workflow_run`), reads the schema doc, and for each subject runs
    `scripts/wiki_search.py` to find an existing page and UPDATE it
    (bump `updated_at`, refine `[[links]]`/`aliases`) rather than
    duplicating — it creates a new page only when none exists. Update is
    the default; creation is the exception. **Slugs are immutable** (a
    rename updates the title + aliases, never the filename); pages are
    never deleted; `log.md` is append-only. **The ingest reads the
    CURATED synthesis — the daily digest + model tickets — NOT the raw
    per-source firehose** (`twitter/`, `rss/`, `community/`, `arxiv/`);
    re-reading the raw sources defeats the curation the digest performs.
    `docs/wiki-schema.md` and `scripts/check_wiki.py` are the contract
    and **must stay in lockstep** — a schema change unreflected in the
    validator (or vice versa) silently corrupts the lane. The agent
    iterates `check_wiki.py` until exit 0 before committing; CI runs it
    on every PR.

## Code Style

- **Workflow YAML:** comment each logical section; group secrets near
  the step that consumes them.
- **Commit messages:** descriptive, dated. Examples:
  - `Twitter update 2026-05-17 09:43 UTC`
  - `Methodology improvements for 2026-02-01`
  - `Add AI news research for 2026-05-17`
- **Python:** stdlib-first; manage dependencies with `uv` in
  `pyproject.toml`/`uv.lock`. Error-handle at boundaries (network,
  subprocess, file IO); inner logic should fail fast.
- **bird CLI invocations:** `--json --plain` + `|| echo "[]"` fallback.
- **Claude prompts in workflows:** quote multi-line prompts with `|`
  block scalars; pass user-controlled values (issue title/body) through
  `env:` rather than direct `${{ }}` interpolation in `run:` blocks
  to avoid script-injection.

## Known Drift

- `dashboard/src/components/ara-research.css` defines ~113 `ara-*`
  classes; `COMPONENTS.md` documents ~81. If you encounter an
  undocumented `ara-*` class in a real article, grep the CSS (it's the
  live source of truth) and add the missing primitive to
  `COMPONENTS.md` in the same PR. The validator's allowlist comes from
  `COMPONENTS.md`, so an undocumented class will be rejected at commit
  time regardless of whether the CSS supports it.

## Historical Docs

Pre-2026-Q2 improvement logs live in [`docs/archive/`](docs/archive/).
They're kept for context but no longer load-bearing.
