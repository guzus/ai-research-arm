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
    → Railway rebuilds the root Dockerfile image and deploys on every push to main
```

Daily-improve runs at the tail of the cycle, reads yesterday's output,
and opens a PR with methodology fixes.

## Key Components

| Path | What it is |
|---|---|
| [`ARA_DSL.md`](ARA_DSL.md) | Source format for generative-research articles. The compiler at `scripts/compile_ara.py` turns `.ara.md` into a validated `<article>` fragment. |
| [`COMPONENTS.md`](COMPONENTS.md) | Human reference for the `ara-*` component vocabulary. The machine-readable contract the validator loads is [`ARA_CATALOG.json`](ARA_CATALOG.json); the two are kept in lockstep (CI-enforced — see "Component catalog" below). The CSS at `dashboard/src/components/ara-research.css` is the rendering source of truth and intentionally carries *more* `ara-*` classes than the article allowlist (runtime + front-page layers). |
| [`ARA_CATALOG.json`](ARA_CATALOG.json) | Machine-readable ara-* component catalog the validator loads its class allowlist from. `scripts/ara_catalog.py` validates it stays in lockstep with COMPONENTS.md (CI-enforced; see "Component catalog" below). |
| [`docs/generative-research-backends.md`](docs/generative-research-backends.md) | Backend matrix for the generative-research lane (Claude vs DeepSeek vs local Oracle), env mapping, comparison commands. |
| [`docs/model-tickets.md`](docs/model-tickets.md) | Schema + lifecycle + dedup protocol for `research/models/tickets/*.md`. Read by the CRUD agent in `24h-model-timeline.yml` and enforced by `scripts/check_model_tickets.py`. |
| [`docs/wiki-schema.md`](docs/wiki-schema.md) | Canonical schema + page conventions for the LLM Wiki (`research/wiki/`). Read at runtime by the ingest agent in `wiki-ingest.yml` and enforced by `scripts/check_wiki.py`. |
| [`docs/hooker-telemetry.md`](docs/hooker-telemetry.md) | Non-blocking telemetry route via `https://hooker.guzus.xyz` topic `ara-telemetry`. |
| [`docs/archive/`](docs/archive/) | Historical improvement logs and superseded docs. |
| `dashboard/` | Vite + Bun + TypeScript SPA. `prebuild.mjs` copies `research/*` into `public/research/` and emits `manifest.json`; Railway auto-deploys on every push to `main` (next row). |
| [`Dockerfile`](Dockerfile) + [`Caddyfile`](Caddyfile) + [`railway.json`](railway.json) | The Railway deploy stack serving **ara.guzus.xyz** (behind Cloudflare — responses carry `x-railway-edge`). The root `Dockerfile` builds the dashboard with bun (`oven/bun:1-alpine`, plus `nodejs` for the pre/postbuild node scripts) and serves `dashboard/dist` with Caddy; `railway.json` pins the DOCKERFILE builder + `/` healthcheck. `dashboard/vercel.json` is the legacy Vercel config — Vercel no longer serves the domain (Load-bearing rule 3). |
| `data/` | Static lookup data used by aggregation scripts. |
| `research/` | All generated artifacts. Subdir map in "Output Locations" below. |

### Scripts (`scripts/`)

| Script | Purpose |
|---|---|
| `compile_ara.py` | `.ara.md` → validated HTML fragment. |
| `ara_catalog.py` | Loads + validates `ARA_CATALOG.json` (the validator's class allowlist) and checks it stays in lockstep with COMPONENTS.md. `uv run python scripts/ara_catalog.py` (exit 0 = in sync); CI runs the same check via `test_ara_dsl.py`. |
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
| `build_wiki_index.py` | Rebuilds `research/wiki/index.json` from the wiki pages. **CI-load-bearing**: `ci.yml` runs `--check` (exit 1 if the committed index is stale or any page fails validation); `wiki-ingest.yml` regenerates it every run. |
| `fetch_ai_blogs.py` | Per-feed AI-blog fetcher used by `daily-ai-blogs.yml`; boundary-handles bad feeds so one failure doesn't crash the run. |
| `source_cache.py` | Runtime primary-source fetch cache under `data/source-cache/` (gitignored), used by `generative-research.yml`. |
| `render_front_page.mjs` | Deterministic newspaper renderer used by `daily-front-page.yml`: digest → SVG → PNG via `@resvg/resvg-js` (no Chromium/model dependency), plus the `.ara.md` source for the interactive edition. Layout is budget-aware — overflow is ellipsized/dropped, never painted over. |
| `test_ara_dsl.py`, `test_dedupe_headline_alerts.py` | Pytest-style tests run in CI. (`test_ara_dsl.py` also asserts `ARA_CATALOG.json` ↔ `COMPONENTS.md` lockstep.) |

#### Experimental / manually-run scripts (NOT in the automated pipeline)

These exist in `scripts/` but are referenced by **zero** workflows — they
are run by hand, not on a schedule. Tested and functional, but not
pipeline code; don't assume the dashboard or any lane depends on them.

| Script | Purpose |
|---|---|
| `generate_generative_article_audio.py` | Backfill TTS audio for a generative article (Gemini Flash TTS / Vertex). Run manually; needs `GEMINI_API_KEY`. |
| `collect_viral_tweets.py`, `analyze_viral_tweets.py` | Viral-tweet collection + analysis. Write `research/twitter-viral/`. |
| `analyze_overperformance.py`, `enrich_overperformance.py`, `experiment_overperf_cv.py` | Tweet-overperformance analysis / enrichment / cross-validation experiments. |
| `enrich_bookmarks.py` | Enrich a bookmark export with engagement/features. |
| `tweet_content.py`, `tweet_features.py`, `tweet_virality_verifier.py` | Tweet content/feature extraction + virality scoring helpers used by the viral/overperf cluster. |

## GitHub Actions Workflows

Almost every workflow runs on **`runs-on: [self-hosted, Linux]`** — an
autoscaled fleet of ephemeral Cloud Run workers (the `runner-autoscaler`
service in `../runner`; see Load-bearing rule 5). A fresh
`cloud-run-worker-*` instance spins up per job, so "self-hosted" no longer
means one serial slot — jobs run in parallel, and each worker carries the
pipeline's baked-in state (bird CLI + birdy daemon, LFS-hydrated
`research/` checkout, pre-installed tooling). Aggregation,
synthesis, output, CI, and the Claude agent lanes all run here.

Only **two `runs-on: ubuntu-latest`** (GitHub-hosted) jobs exist, and both
are watchdogs that must survive a self-hosted/Cloud Run outage — a watchdog
that runs on the runners it is watching is useless:
- `liveness-check.yml` runs one job on EACH tier (its `ubuntu` job + its
  `self-hosted` job). No single runner survives both failure modes — a
  GitHub-hosted billing/spending-limit block vs. a self-hosted outage — so
  whichever tier is alive emits the hooker/Telegram staleness alert.
- `auto-rerun-on-runner-loss.yml` re-runs jobs whose ephemeral worker
  vanished mid-run (Load-bearing rule 11).

The per-workflow `ubuntu-latest` vs. `self-hosted` lists that used to live
here are gone on purpose: the answer is now "self-hosted unless it's one of
those two watchdogs." **Always read the workflow's actual `runs-on:` —
never trust a cached list** (the old list here drifted to 100% wrong once
the autoscaler landed and the stateless lanes moved back to self-hosted).

Claude workflows use `anthropics/claude-code-action@v1` with the model
passed via `claude_args: "--model opus"` (never as a separate `model:`
input).

### Aggregation (raw signal → `research/<source>/`)

| Workflow | Schedule | Output |
|---|---|---|
| `hourly-rss.yml` | `:30` every hour | `research/rss/` |
| `daily-ai-blogs.yml` | `:13` every 6h | `research/blogs/` |
| `hourly-twitter.yml` | every 3h `:07`; DeepSeek/Fireworks comparison lanes via matrix/manual dispatch | `research/twitter/` + `research/summaries/` + Telegram headline alerts; comparison outputs under `research/twitter-deepseek/`, `research/twitter-deepseek-pi/`, and `research/twitter-fireworks-pi/` |
| `2h-bluesky.yml` | twice daily `00:11`,`12:11` | `research/bluesky/` |
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
| **DeepSeek V4 Flash (via Fireworks)** | `generative-research backend=deepseek-v4-flash`; `hourly-twitter.yml` DeepSeek lanes | `FIREWORKS_API_KEY` | Uses Fireworks' Anthropic-compatible endpoint at `https://api.fireworks.ai/inference` with model `accounts/fireworks/models/deepseek-v4-flash` (base URL omits `/v1`; the client appends `/v1/messages`). Overrides `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_MODEL` so the Claude Code action transparently calls Fireworks. The direct DeepSeek API (`api.deepseek.com`) is retired (billing/credits). Selector token: `deepseek-v4-flash` (or `deepseek`). Generative-research retries up to 2x on socket drops before commit. |
| **Fireworks pi** | `hourly-twitter.yml backend=fireworks-pi` manual comparison lane | `FIREWORKS_API_KEY` | Uses pi's built-in Fireworks provider with `accounts/fireworks/models/kimi-k2p6`; writes `research/twitter-fireworks-pi/` plus a Telegram summary. |
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
├── blogs/                     # daily-ai-blogs.yml
├── summaries/                 # hourly-twitter.yml (Telegram digest + headline-alert state)
├── twitter/                   # hourly-twitter.yml
├── twitter-deepseek/          # hourly-twitter.yml backend=deepseek-claude-code
├── twitter-deepseek-pi/       # hourly-twitter.yml backend=deepseek-pi
├── twitter-fireworks-pi/      # hourly-twitter.yml backend=fireworks-pi
├── twitter-viral/             # experimental viral/overperf cluster (manual; see Scripts)
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
| `DEEPSEEK_API_KEY` | _Retired_ — DeepSeek lanes now route through Fireworks | No longer referenced by any workflow. |
| `FIREWORKS_API_KEY` | `generative-research backend=deepseek-v4-flash`; all `hourly-twitter.yml` non-claude lanes (`deepseek-claude-code`, `deepseek-pi`, `fireworks-pi`) | Required for the DeepSeek-V4-Flash-via-Fireworks and Kimi lanes. |
| `BIRD_AUTH_TOKEN`, `BIRD_CT0` | All bird-CLI workflows (`hourly-twitter*`, `24h-model-timeline`) | X/Twitter cookies. |
| `EXA_API_KEY`, `PERPLEXITY_API_KEY` | `daily-digest`, `ai-news-research`, `research-issue` | Optional; enhance MCP search. |
| `GEMINI_API_KEY` | `daily-digest` (inline Gemini Flash TTS for digest audio); also the manual `generate_generative_article_audio.py` | Optional; without it, audio generation is skipped. |
| `HOOKER_TOKEN` | Telemetry composite action | Optional; without it, telemetry steps no-op. |
| `HOOKER_URL` | Hooker telemetry composite + most workflows (the hooker endpoint, distinct from `HOOKER_TOKEN`) | The `https://hooker.guzus.xyz`-style base URL the telemetry/alert steps POST to. Referenced widely across workflows/actions. |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | `hourly-twitter*` | For headline alert delivery. |
| `VERCEL_DEPLOY_HOOK` | `24h-model-timeline`, `wiki-ingest`, `hourly-twitter` (claude tier) | Optional legacy nudge to a Vercel project that does NOT serve ara.guzus.xyz (prod deploys are Railway, git-push driven — Load-bearing rule 3; Vercel's last recorded deploy failed 2026-05-25). Harmless: the step no-ops when unset. |
| `GITHUB_TOKEN` | All workflows | Auto-provided. |

## Load-bearing Rules

These are the conventions that, if broken, will silently corrupt
output or break the pipeline. Read them before editing.

1. **ARA DSL compile + validate is mandatory.** Every commit to
   `research/generative/` must go through
   `scripts/compile_ara.py` (`.ara.md` → HTML) and pass
   `scripts/check_generative_research.py` (tag/class allowlist plus
   optional `--diversity-min`, `--callout-max`, `--strict-shape`
   design gates). `scripts/write_generative_research.py` is the
   **only** committer for that directory — it re-validates at write
   time and persists the `.ara.md` source verbatim alongside the
   generated HTML (there is no decompile step; the source is the
   committed `.ara.md`, not something regenerated from the HTML).
   Workflows that bypass the writer will fail review.

2. **The validator is exact-match.** Class tokens must start with
   `ara-` *and* be a base class in `ARA_CATALOG.json` (or be a valid
   `--variant` suffix of a cataloged base class). The allowlist is
   loaded from `ARA_CATALOG.json` (via `scripts/ara_catalog.py`), NOT
   parsed from `COMPONENTS.md` — `COMPONENTS.md` is the human reference
   kept in lockstep with the catalog (CI-enforced; see "Component
   catalog"). Tags outside the allowlist (`<style>`, `<script>`,
   `<iframe>`, `<h1>`, inline `style=`, `on*=`, `javascript:` URLs) are
   rejected. Reach for `:::raw` only when the DSL genuinely can't
   express the shape; invented classes still fail.

3. **Dashboard deploys are git-push driven — Railway is the deployer.**
   Railway watches `main` and rebuilds the Docker image on every push
   (root `Dockerfile`: bun build → Caddy serve; `railway.json` pins
   the builder + healthcheck). ara.guzus.xyz is served by that
   container behind Cloudflare (responses carry `x-railway-edge`) —
   NOT by Vercel, whose last recorded deploy failed 2026-05-25 and
   whose leftovers (`dashboard/vercel.json`, `VERCEL_DEPLOY_HOOK`)
   are legacy. There is still no workflow file for deploys.
   `dashboard/scripts/prebuild.mjs` copies `research/<source>/` into
   `public/research/` and emits `manifest.json` before Vite runs (the
   Docker build runs the same `bun run build` lifecycle). Touching it
   changes what the dashboard sees. Incident-learned corollary: the
   Dockerfile's package manager MUST stay in lockstep with the
   dashboard's (bun since #102) — a leftover `npm ci` froze prod at a
   stale build for ~a day with CI green, because CI never runs the
   Dockerfile. Deploy staleness is watched by
   `scripts/check_deploy_health.py`, wired into `liveness-check.yml`.

4. **Hooker telemetry is non-blocking.** Every workflow's final step
   posts to `https://hooker.guzus.xyz` via the local composite at
   `.github/actions/hooker-telemetry`. It must never fail a job —
   `continue-on-error: true` style. Don't add hard dependencies on
   telemetry success.

5. **Runner choice is load-bearing — default to self-hosted.** The
   self-hosted tier is an autoscaled Cloud Run worker fleet
   (`runner-autoscaler` in `../runner`): a fresh ephemeral
   `cloud-run-worker-*` registers per job, runs it, then deregisters, so
   jobs run in PARALLEL (no single serial slot) and each carries baked-in
   state — bird CLI + warm birdy daemon (`hourly-twitter*`,
   `24h-model-timeline`), LFS-hydrated `research/` for prior-output context
   (`daily-digest`, `ci.yml` dashboard job), pre-installed pnpm/Oracle
   tooling. (`daily-front-page` checks out with `lfs: false` and renders
   via resvg — it needs neither LFS media nor Chromium.) Use
   `[self-hosted, Linux]` for anything touching that state,
   which is nearly everything. Reserve `ubuntu-latest` for the two
   watchdogs that must outlive a self-hosted outage (`liveness-check.yml`,
   `auto-rerun-on-runner-loss.yml`). The tradeoff of ephemeral workers: an
   instance can vanish mid-job (preemption / maintenance / OOM), failing
   the run with no error in the log — rule 11 auto-recovers that. Before
   moving a job to `ubuntu-latest`, verify it needs neither the warm state
   nor bird/birdy — getting this wrong silently breaks the pipeline.

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
   never reaches the dashboard prebuild (and thus the next deployed
   Railway image).

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
    per-source firehose** (`twitter/`, `rss/`, `blogs/`, `community/`, `arxiv/`);
    re-reading the raw sources defeats the curation the digest performs.
    `docs/wiki-schema.md` and `scripts/check_wiki.py` are the contract
    and **must stay in lockstep** — a schema change unreflected in the
    validator (or vice versa) silently corrupts the lane. The agent
    iterates `check_wiki.py` until exit 0 before committing; CI runs it
    on every PR.

11. **Worker-death auto-rerun must stay loop-safe.**
    `.github/workflows/auto-rerun-on-runner-loss.yml` watches the
    unattended self-hosted pipelines via `workflow_run` and, when one fails
    because its ephemeral worker vanished (a failed/incomplete job with NO
    genuinely-failed step — "died at Set up job", or steps stuck
    `in_progress`/`null`), re-runs only the failed jobs. Three invariants
    keep it from becoming a retry storm or masking real red CI, and MUST be
    preserved if you edit it:
    (a) **Cap on `run_attempt`** — it only fires when
    `github.event.workflow_run.run_attempt < 3` (≤ 2 auto re-runs). This is
    the single load-bearing guard against infinite loops.
    (b) **Gate on the lost-runner signature** — never re-run a run whose
    failed job has a step with `conclusion == "failure"` (a genuine
    failure), nor a `cancelled` run. Only the "worker vanished" shape
    qualifies.
    (c) **Not self-referential, and `ubuntu-latest`** — the watchdog's own
    name is absent from its `workflows:` trigger list (so it can't
    self-trigger) and it runs GitHub-hosted (so a Cloud Run blip can't take
    out the recovery path too). Adding its name to the trigger list, or
    moving it to self-hosted, breaks both protections.

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

## Component catalog

The article-fragment class allowlist lives in **`ARA_CATALOG.json`**
(73 base `ara-*` classes). The validator
(`scripts/check_generative_research.py` → `write_generative_research.py`
→ `ara_catalog.load_catalog`/`catalog_classes`) loads its allowlist from
that file, NOT from `COMPONENTS.md`. `COMPONENTS.md` is the human
reference and documents the **same 73** classes;
`scripts/ara_catalog.py` (`validate_catalog_against_components`) asserts
the two stay in perfect lockstep and CI enforces it via
`test_ara_dsl.py`. To add a new primitive, add it to BOTH files in the
same PR (and ship the matching CSS); a class present in one but not the
other fails CI.

The CSS intentionally defines **more** `ara-*` classes than the article
allowlist. The extra classes are NOT drift and are NOT a commit-time
rejection risk — they belong to layers that live outside the
article-fragment contract on purpose:

- `dashboard/src/components/ara-research.css` defines ~98 base `ara-*`
  classes total: the 73 cataloged article primitives (`ara-doc`,
  `ara-callout`, `ara-figure`, …) that DO appear in `.ara.md` and ARE the
  allowlist, **plus** ~25 **runtime/interactive extras** — table-of-
  contents, figure lightbox, chart tooltips/axes/series (e.g.
  `ara-chart-series-*`, built at `main.ts` ~line 3311) — injected by
  `dashboard/src/main.ts` at runtime. The runtime extras never appear in
  `.ara.md` source, so they don't need to be in the allowlist.
- **Front-page template classes** (`ara-paper-*`, styled in
  `dashboard/src/style.css`) used by the daily-front-page newspaper
  render, which is its own template, not an ARA article.

So a higher CSS class count than `COMPONENTS.md`/`ARA_CATALOG.json` is
expected. Only worry about an undocumented class if it appears in an
*article fragment* — and then the fix is to add it to both
`ARA_CATALOG.json` and `COMPONENTS.md`, not to the CSS (the CSS may
already have it).

## Historical Docs

Pre-2026-Q2 improvement logs live in [`docs/archive/`](docs/archive/).
They're kept for context but no longer load-bearing.
