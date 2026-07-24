# CLAUDE.md

Operating guide for AI agents working in this repo. Read this before
touching workflows, research output, or the dashboard.

> **New here, or just found this on GitHub?** This file is the *operator's
> manual* for the live deployment and assumes the maintainer's infrastructure
> (self-hosted runners, S3, telemetry, X cookies). If you are exploring or
> forking the project, start with [`README.md`](README.md): its **Quickstart**
> runs with no accounts, and the **License** and **"What you can run vs. what
> needs accounts"** sections explain what is reproducible outside the original
> deployment.

## Project Overview

`ai-research-arm` (ARA) is an automated AI-news intelligence pipeline.
GitHub Actions on the self-hosted `gunux` Linux runner aggregate signal from
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
| [`ARA_DSL.md`](ARA_DSL.md) | Source format for generative-research articles; `scripts/compile_ara.py` turns `.ara.md` into a validated `<article>` fragment. |
| [`ARA_CATALOG.json`](ARA_CATALOG.json) + [`COMPONENTS.md`](COMPONENTS.md) | The `ara-*` class allowlist the validator loads, and its human reference. Kept in lockstep by CI — see "Component catalog" below. |
| [`data/agent-backends.json`](data/agent-backends.json) | Routing SSOT: per-lane backend, profile table, ordered fallback chain. See Backends. |
| `docs/*.md` | Per-lane contracts, read at runtime by the agents and enforced by the matching validator: `model-tickets`, `wiki-schema`, `okf`, `headline-dedupe`, `blog-subscriptions`, `twitter-account-curation`, `twitter-model-ab`, `generative-research-backends`, `backend-matrix` (generated), `hooker-telemetry`. [`docs/archive/`](docs/archive/) holds superseded docs + improvement logs. |
| `dashboard/` | Vite + Bun + TypeScript SPA. `prebuild.mjs` copies `research/*` into `public/research/` and emits `manifest.json`. |
| [`Dockerfile`](Dockerfile) + [`Caddyfile`](Caddyfile) + [`railway.json`](railway.json) | The Railway stack serving **ara.guzus.xyz** behind Cloudflare (responses carry `x-railway-edge`): bun build → Caddy serves `dashboard/dist`; `railway.json` pins the DOCKERFILE builder + `/` healthcheck. Vercel no longer serves the domain — rule 3. |
| `data/`, `research/` | Static lookup data for aggregation scripts; all generated artifacts (subdir map in "Output Locations"). |

### Scripts (`scripts/`)

| Script | Purpose |
|---|---|
**ARA DSL / generative research**

| Script | Purpose |
|---|---|
| `compile_ara.py` | `.ara.md` → validated HTML fragment. |
| `ara_catalog.py` | Loads `ARA_CATALOG.json` (the validator's class allowlist) and asserts lockstep with COMPONENTS.md. CI-enforced via `test_ara_dsl.py`. |
| `check_generative_research.py` | Pre-commit validator: tag/class allowlist + optional `--diversity-min`, `--callout-max`, `--strict-shape`. Exit 0 = safe to commit. |
| `write_generative_research.py` | The **only** committer for `research/generative/`. Re-validates, writes HTML + `.ara.md`, updates `index.json`, commits. |
| `run_generative_research_oracle.py` | Local runner via `../oracle` (GPT-5.5 Pro) → validator (`--diversity-min 3 --callout-max 5 --strict-shape`) → writer. |
| `prior_context.py`, `research_search.py`, `stock_prices.py`, `source_cache.py` | Article-authoring helpers: find related prior articles; primary-source search wrappers; Yahoo Finance series for `:::line-chart`; runtime fetch cache under `data/source-cache/` (gitignored). |

**Backend routing** (see also Load-bearing rule 14)

| Script | Purpose |
|---|---|
| `select_backend.py` | Runtime backend selector for `.github/actions/agent-run`: resolves the lane, probes the provider, walks the ordered `fallback.chain` — first available wins; strict lanes never fall back. The claude probe is auth-only and has two traps — **read rule 14 before touching it**. |
| `resolve_backend_lane.py` | Field resolver for `data/agent-backends.json`; generative-research uses it for its SSOT default. Unknown lane = hard failure, never a silent default. |
| `build_backend_matrix.py` | Cross-checks the routing SSOT against `.github/workflows/*` (lane exists, all provider secrets passed, pi/native mirrors match) and regenerates `docs/backend-matrix.md`. **CI-load-bearing** (`--check`). |

**Validators + watchdogs** — all CI-enforced; the agent lanes iterate until exit 0

| Script | Purpose |
|---|---|
| `check_model_tickets.py` | `research/models/tickets/*.md` against `docs/model-tickets.md`. |
| `check_wiki.py` / `build_wiki_index.py` / `wiki_search.py` | Wiki page schema (`docs/wiki-schema.md`; `--lint` adds advisory checks); `index.json` rebuild (`--check` fails on a stale index); search wrapper the ingest agent MUST run before writing, so it updates rather than duplicates. |
| `check_digest_content.py` | Per-run hard content floor for the daily digest (`--min-bytes`, `--min-sections`, unexpanded-placeholder scan). Decides whether the deterministic composer takes over; complements the advisory `check_lane_content.py`. |
| `validate_twitter_public_output.py` | Twitter signal-only contract after every backend: heartbeat identity, exact public-item count, concrete story/Quick-hit presence, normalized same-hour headings, no operational/no-news filler. |
| `check_lane_freshness.py` | Per-lane git-commit recency vs. cadence thresholds; exit 2 → hooker/Telegram alert from `liveness-check.yml`. Stdlib-only so it runs on both runner tiers. |
| `export_wiki_okf.py` | `research/wiki/` → portable OKF bundle; rewrites `[[wikilinks]]` to Markdown links. |

**Deterministic (model-free) fallbacks** — each composes its lane's artifact from already-fetched data when the agent path fails. They never invent content; missing inputs are noted explicitly.

| Script | Lane | Note |
|---|---|---|
| `deterministic_daily_digest.py` | `daily-digest.yml` | Verbatim top excerpts per committed lane artifact. Fires on agent failure **or** sub-floor output. |
| `deterministic_rss_digest.py` | `hourly-rss.yml` | Appends a timestamped section to `research/rss/<date>.md`. |
| `deterministic_community_digest.py` | `4h-community.yml` | Pre-fetched HN JSON + Reddit RSS → `*-hn.md`, `*-reddit.md`. |
| `deterministic_arxiv_digest.py` | `daily-arxiv.yml` | Queries the arXiv Atom API; zero-paper windows still write an honest empty note. |
| `deterministic_bluesky_digest.py` | `2h-bluesky.yml` | Engagement-ranked, ≤8 bullets / ≤3 per author, 48h window. |
| `deterministic_twitter_digest.py` | `hourly-twitter.yml` | **Fail-closed, not a composer.** Restores the public digest to its pre-agent baseline and writes only a run-scoped `no_update` heartbeat — never reads Birdy, never authors news. The job then fails loudly and skips notifications. |

**Aggregation + rendering**

| Script | Purpose |
|---|---|
| `fetch_ai_blogs.py` | Per-feed AI-blog fetcher (`daily-ai-blogs.yml`); boundary-handles bad feeds so one failure doesn't crash the run. |
| `watch_blog_subscriptions.py` | RSS subscription watcher (`blog-subscriptions.yml`); seeds historical GUIDs without alerting, verifies Telegram responses, acknowledges each proven delivery atomically. |
| `fetch_youtube_signal.py` | tuber-backed YouTube lane; read-only by default — never triggers paid summary generation. |
| `dedupe_headline_alerts.py`, `headline_judge.py` | Twitter headline-alert dedup: deterministic layered check, then an agent-in-the-loop Haiku gate adjudicating the contested `[0.35,0.50)` Jaccard band (`shortlist` → judge → `apply`, fail-open, URL-keyed). Contract: [`docs/headline-dedupe.md`](docs/headline-dedupe.md). |
| `curate_twitter_accounts.py`, `explore_twitter_accounts.py` | Validate/curate `data/sources/twitter_accounts.json` + build the birdy fetch manifest; the scout scores candidates on trust-weighted mentions (needs ≥1 *monitored* citer), AI topicality, and bounded engagement, so viral off-topic accounts don't outrank genuine AI sources. Contract: [`docs/twitter-account-curation.md`](docs/twitter-account-curation.md). |
| `render_front_page.mjs` | Newspaper render for `daily-front-page.yml`: digest → SVG → PNG via `@resvg/resvg-js` (no Chromium, no model). Budget-aware — overflow is ellipsized/dropped, never painted over. |
| `test_*.py` | Pytest-style tests run in CI. |

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

**Runner tiers.** Most production lanes run on `[self-hosted, Linux]` — the
native Ubuntu host `gunux`, one systemd runner per repo. It carries the Birdy
read-only CLI/daemon, a recent `research/` checkout, and pre-installed
tooling; its home directory persists across jobs, so actions must overwrite
stale user-level settings explicitly rather than assume a fresh container.
(The old Cloud Run pools are paused rollback infrastructure, not the
production path.)

`ubuntu-latest` is reserved for two cases: **CI** (`ci.yml` — PRs can change
build scripts, tests, and workflow files, which must not execute on the
self-hosted host) and **watchdogs** (a watchdog running on the runners it
watches is useless). `liveness-check.yml` runs a job on *each* tier, because
no single tier survives both failure modes — a GitHub-hosted billing block
vs. a self-hosted outage — so whichever is alive still alerts.
`auto-rerun-on-runner-loss.yml` recovers jobs whose runner vanished mid-run
(rule 11).

**Always read the workflow's actual `runs-on:` — never trust a cached list.**
The per-workflow list that used to live here drifted to 100% wrong and was
deleted on purpose.

**Agent lanes use `.github/actions/agent-run`,** not
`anthropics/claude-code-action@v1` directly. It resolves the backend from the
routing SSOT (see Backends), sets up the sandbox centrally, and enforces two
commit contracts: `require-output` proves every expected pathspec changed
(`expected-paths` = exact artifact files; `allowed-paths` = everything the
agent may commit), and `require-diff-scope` proves the committed diff since
the pre-agent SHA stays inside those paths. PR/review/on-demand Claude
workflows may still call the action directly; when they do, pass the model
through `claude_args` (`"--model claude-sonnet-5"`) — never as a separate
`model:` input.

**A green run on a fallback lane is not evidence the agent path was
healthy.** RSS, community, arXiv, digest and Bluesky (plus the
twitter-deepseek tier) run a deterministic fallback after the agent step,
then a final `require-output` guard; the digest additionally gates agent
output on a hard content floor before deciding. Green means "an artifact was
committed" — read the agent/fallback step logs, or the fallback-used Telegram
alert, to learn which path produced it.

**Publishing uses `.github/actions/safe-push`** — see rule 13 for the
protected-branch fallback and what `pushed=true` actually means.

**Sandbox.** The checked-in `.claude/settings.json` sets
`sandbox.failIfUnavailable: true` and `sandbox.allowUnsandboxedCommands:
false`, so a missing sandbox fails the workflow instead of silently giving
Bash host filesystem access; it also blocks reads of `~/.ssh`, `~/.aws`,
`/proc`, `/var/run`. Linux needs `bubblewrap` + `socat`. Direct-Claude
workflows must run `.github/actions/setup-claude-sandbox` first; agent-run
lanes get it centrally.

**Pi lanes don't read Claude Code settings,** so they get their isolation
from `.github/actions/run-pi-container` instead: a small Node container with
`pi`, `bird`, `git`, `jq`, mounting only `$GITHUB_WORKSPACE`, `/tmp/bird`
read-only, and the prompt file. Missing Docker is a hard failure — never fall
back to host-level `pi --tools ... bash`.

### Aggregation (raw signal → `research/<source>/`)

| Workflow | Schedule | Output |
|---|---|---|
| `hourly-rss.yml` | `:30` every 2h | `research/rss/` |
| `daily-ai-blogs.yml` | `:13` every 6h | `research/blogs/` |
| `blog-subscriptions.yml` | `:47` every 2h | Telegram notifications for configured blog subscriptions + GUID state in `research/summaries/blog-subscriptions.json` |
| `daily-youtube.yml` | daily `23:20` for the next `00:00` digest | `research/youtube/` (tuber discovery + read-only summary/transcript evidence) |
| `hourly-twitter.yml` | every 3h `:07`; primary lane uses Fireworks through `.github/actions/agent-run`; comparison lanes via matrix/manual dispatch | `research/twitter/` + `research/summaries/` + Telegram headline alerts; comparison outputs under `research/twitter-deepseek/`, `research/twitter-deepseek-pi/`, `research/twitter-fireworks-pi/`, and `research/twitter-opencode-kimi/` |
| `twitter-account-explorer.yml` | weekly Tuesday `01:47` UTC + manual dispatch | Opens reviewed PRs for `data/sources/twitter_accounts.json` changes when high-signal account evidence exists |
| `2h-bluesky.yml` | daily `10:11` | `research/bluesky/` (supplemental expert commentary, capped output) |
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
| `arm-timeline.yml` | every 2h `:45` | Deterministic refresh of `research/arm/timeline.json` so the dashboard's Arm tab renders in prod (the Docker build context has no `.git`/`.github`, so prebuild falls back to this committed file; unrefreshed it ages out of the ±36h window). |
| `daily-improve.yml` | weekly, Monday `00:17` UTC | Opens improve/YYYY-MM-DD PR with methodology fixes; each run auto-closes prior unmerged `improve/*` PRs. See "Load-bearing rules" for where the IMPROVEMENTS file belongs. |
| `ci.yml` | push/PR on workflows/dashboard/scripts | actionlint + dashboard build + Python tests on GitHub-hosted runners |
| `claude.yml` | `@claude` mention in issue/PR/review | Interactive Claude-Code agent |
| `claude-code-review.yml` | PR opened/synced | Automated Claude code review |
| `twitter-model-ab.yml` | daily `21:40` UTC (temporary — remove after the eval week) + manual dispatch | Same-input, parity-locked model A/B eval (claude-sonnet-5 vs GLM-5.2 via Z.ai) on the Twitter-summary workload with a blinded position-swapped Opus judge → `research/eval/twitter-ab/`. Contract: [`docs/twitter-model-ab.md`](docs/twitter-model-ab.md). |

**Model convention:** scheduled workflows pass `--model opus`, but
`agent-run` remaps that alias to whatever the resolved backend serves —
the Fireworks or Z.ai profile model, or `native-model` (default
**`claude-sonnet-5`**) on the native path. Direct Claude workflows pin
`--model claude-sonnet-5` via `claude_args`. Read the workflow file
rather than assuming one provider everywhere.

## Backends

**[`data/agent-backends.json`](data/agent-backends.json) is the single
source of truth** for per-lane routing, the backend profile table, and the
ordered fallback chain — edit it to re-route with no workflow change (every
call site already carries all provider secrets). agent-run lanes resolve it
at runtime via `scripts/select_backend.py`; pi and direct
claude-code-action lanes are CI-enforced mirrors; strict lanes never fall
back. Human view: [`docs/backend-matrix.md`](docs/backend-matrix.md) —
regenerate with `uv run python scripts/build_backend_matrix.py` after any
routing change (CI runs `--check`).

The table below is the per-*backend* contract — the gotchas that aren't
derivable from the SSOT.

| Backend | When | Auth | Notes |
|---|---|---|---|
| **Claude** | Every production agent lane; `generative-research backend=claude` | `CLAUDE_CODE_OAUTH_TOKEN` | Native Anthropic, model **`claude-sonnet-5`** (the global `fallback.native_model`). Leads the fallback chain. Its token expiring is a fleet-wide outage — see rule 14 and the Authentication table. |
| **GLM 5.2 (via Z.ai Coding Plan)** | Second link in the fallback chain; `agent-run backend=zai-glm-5p2`; default manual `hourly-twitter.yml` backend; `zai-claude-code-canary.yml` | `ZAI_API_KEY` | Anthropic-compatible Claude Code endpoint `https://api.z.ai/api/anthropic`, model `glm-5.2`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000`. The `glm-5.2[1m]` alias was rejected as `Unknown Model` (canary run `28751367808`) — keep the endpoint-valid id unless a raw probe proves otherwise. Because it shares the harness and sandbox but not the credential, **the canary is the fastest way to tell a dead Claude token from a broken runner**. Selectors: `zai-glm-5p2`, `zai-glm-5.2`, `zai-glm52`, `zai`. |
| **GLM 5.2 (via Fireworks)** | `generative-research backend=glm-5p2` | `FIREWORKS_API_KEY` | Model `accounts/fireworks/models/glm-5p2`. Selectors: `fireworks-glm-5p2`, `glm-5p2`, `glm`. In `generative-research.yml` the workflow-level `fireworks_fallback` input falls back to native Claude by default. |
| **DeepSeek V4 Flash (via Fireworks)** | Low-cost/comparison: `generative-research backend=deepseek-v4-flash`; `hourly-twitter.yml` DeepSeek tiers | `FIREWORKS_API_KEY` | Endpoint `https://api.fireworks.ai/inference` (base URL omits `/v1`; the client appends `/v1/messages`), model `accounts/fireworks/models/deepseek-v4-flash`. Overrides `ANTHROPIC_BASE_URL`/`AUTH_TOKEN`/`MODEL` so the Claude action transparently calls Fireworks. The direct DeepSeek API is retired (billing). Scheduled DeepSeek lanes are STRICT comparison tiers that never fall back. |
| **Kimi K3 (via opencode)** | `generative-research`/`hourly-twitter` `backend=opencode-kimi-k3`; `opencode-kimi-canary.yml` | `OPENCODE_API_KEY` (Go, preferred) or `MOONSHOT_API_KEY` | opencode CLI pinned `opencode-ai@1.18.3` (>=1.18.3 required for kimi-k3) against Kimi K3 (1M ctx, $3/$15 per Mtok). Route resolves Go-first — `opencode-go/kimi-k3` on the $10/mo Go plan (caps $12/5h, $30/wk, $60/mo, K3 billed at full value), else `moonshotai/kimi-k3` pay-per-token. Plain env-var auth on both; no interactive login. **Strict — no Claude fallback**, so a Kimi-labeled article can never be silently authored by another model. Not on Fireworks or OpenCode Zen as of 2026-07-20. Selectors: `opencode-kimi-k3`, `opencode`, `opencode-kimi`, `kimi-k3`, `kimi`. |
| **Codex** | `generative-research backend=codex` | `CODEX_AUTH_JSON` | Codex CLI with ChatGPT-managed file auth (`auth.json` from `codex login`), so usage bills against the ChatGPT/Codex subscription, not the API. |
| **Fireworks pi** | `hourly-twitter.yml backend=fireworks-pi` manual comparison lane | `FIREWORKS_API_KEY` | Uses pi's built-in Fireworks provider with `accounts/fireworks/models/kimi-k2p7`; writes `research/twitter-fireworks-pi/` plus a Telegram summary. |
| **Local Oracle (GPT-5.5 Pro)** | `scripts/run_generative_research_oracle.py` | Local `../oracle` checkout (browser engine by default) | Runs entirely on the developer machine; outputs go through the same `check_generative_research.py` → `write_generative_research.py` contract. Source metadata: `local-oracle`. |

Backend selection details, env-var mapping, and comparison commands:
`docs/generative-research-backends.md`.

### Twitter-Seeded Generative Research

`generative-research.yml` takes `twitter_url` as a standalone
`workflow_dispatch` input (`topic` then optional), staged at
`.gen-input/twitter_url.txt`. The agent reads the thread with `bird read`
/ `bird thread`, infers the underlying research question, and treats the
tweet as primary evidence **only for what the author said** — every
underlying claim must be verified against independent primary sources
before the article is written.

```bash
/gen-research-tweet https://x.com/<handle>/status/<id>
# or: gh workflow run generative-research.yml \
#       -f twitter_url="https://x.com/<handle>/status/<id>" -f backend=claude
```

## Output Locations

```
research/
├── arxiv/                     # daily-arxiv.yml
├── arm/                       # arm-timeline.yml (dashboard Arm-tab timeline source; prod fallback for prebuild)
├── audio/                     # digest audio; mp3s live on S3 (since May 2026) — committed files are 0-byte stubs
├── bluesky/                   # 2h-bluesky.yml
├── community/                 # 4h-community.yml (-hn.md, -reddit.md)
├── digest/                    # daily-digest.yml
├── front-page/                # daily-front-page.yml (committed PNG + interactive .ara.md/.html edition)
├── generative/                # generative-research.yml + Oracle runner (HTML + .ara.md + index.json)
├── issues/                    # research-issue.yml
├── models/                    # 24h-model-timeline.yml
│   ├── tickets/                # persistent set, one .md per shipping artifact
│   └── <date>-timeline.md      # derived daily diff (created/updated/closed counts)
├── rss/                       # hourly-rss.yml
├── blogs/                     # daily-ai-blogs.yml
├── summaries/                 # Telegram digest, headline-alert, and blog-subscription state
├── twitter/                   # hourly-twitter.yml (signal-only daily Markdown + status/ run heartbeats)
├── youtube/                   # daily-youtube.yml (tuber read-only signal lane)
├── twitter-deepseek/          # hourly-twitter.yml backend=deepseek-claude-code
├── twitter-deepseek-pi/       # hourly-twitter.yml backend=deepseek-pi
├── twitter-fireworks-pi/      # hourly-twitter.yml backend=fireworks-pi
├── twitter-opencode-kimi/     # hourly-twitter.yml backend=opencode-kimi-k3
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
| `CLAUDE_CODE_OAUTH_TOKEN` | Every agent lane + direct-Claude workflows | Required by `claude-code-action@v1` (non-Claude routes still pass it for schema compatibility). **Expiry is a fleet-wide outage** — every production lane routes to `backend: claude`. Log signature: `is_error: true`, `num_turns: 1`, `total_cost_usd: 0`, `duration_ms` < ~2000, zero permission denials — the agent dies before doing any work. `show_full_output` is off, so the provider error body is hidden: **that shape IS the diagnosis.** Re-mint with `claude setup-token` → `gh secret set CLAUDE_CODE_OAUTH_TOKEN`. Dispatch `zai-claude-code-canary.yml` to separate a dead credential (canary green, lanes red) from a broken runner/sandbox (both red). Last expiry 2026-07-24; see rule 14. |
| `ZAI_API_KEY` | Fallback chain link 2; `agent-run backend=zai-glm-5p2`; `zai-claude-code-canary.yml` | Z.ai Coding Plan key. Now load-bearing for outage resilience, not just comparison. |
| `FIREWORKS_API_KEY` | `generative-research backend=glm-5p2`; DeepSeek/Kimi comparison lanes | Covers the GLM-via-Fireworks and DeepSeek-V4-Flash routes. |
| `OPENCODE_API_KEY` / `MOONSHOT_API_KEY` | `backend=opencode-kimi-k3`; `opencode-kimi-canary.yml` | Kimi K3 route, Go-first then pay-per-token. Go key: https://opencode.ai/auth (watch caps $12/5h, $30/wk, $60/mo). Moonshot key: https://platform.kimi.ai/console/api-keys — the account needs real balance, new-user vouchers cannot bill kimi-k3. Validate with the canary before a full run. |
| `CODEX_AUTH_JSON` | `generative-research backend=codex` | The file-backed `~/.codex/auth.json` from `codex login`. Treat like a password; one auth file per serialized runner stream. |
| `BIRD_AUTH_TOKEN`, `BIRD_CT0` | bird-CLI workflows (`hourly-twitter*`, `24h-model-timeline`) | X/Twitter cookies; they expire — see rule 6. |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | `blog-subscriptions`, `daily-digest`, `liveness-check` | Blog alerts, digest delivery, liveness escalation. |
| `HOOKER_URL`, `HOOKER_TOKEN` | Telemetry composite + most workflows | Base URL and token for the hooker POSTs. Optional — without them telemetry steps no-op (rule 4). |
| `S3_*` (4 vars), `GEMINI_API_KEY` | `daily-digest` audio | Optional. Gemini Flash TTS generates the mp3, S3 stores it; the committed `research/audio/*.mp3` are 0-byte stubs. Missing = that step skips. |
| `EXA_API_KEY`, `PERPLEXITY_API_KEY` | `daily-digest`, `ai-news-research`, `research-issue` | Optional MCP search. **Currently unset** (verified 2026-07-02) — `daily-digest` warns and uses local-source synthesis. |
| `GITHUB_TOKEN` | All workflows | Auto-provided. |
| `DEEPSEEK_API_KEY`, `VERCEL_DEPLOY_HOOK` | _Retired_ | Both removed from the repo (verified 2026-07-02). DeepSeek routes through Fireworks now; the `VERCEL_DEPLOY_HOOK` steps still in a few workflows are permanent no-ops — Vercel does NOT serve ara.guzus.xyz (rule 3). Safe to delete. |

## Load-bearing Rules

These are the conventions that, if broken, will silently corrupt
output or break the pipeline. Read them before editing.

1. **ARA DSL compile + validate is mandatory.** Every commit to
   `research/generative/` goes through `scripts/compile_ara.py` and must
   pass `scripts/check_generative_research.py`.
   `scripts/write_generative_research.py` is the **only** committer for
   that directory — it re-validates at write time and persists the
   `.ara.md` verbatim beside the HTML. There is no decompile step: the
   source is the committed `.ara.md`, never something regenerated from
   the HTML. Workflows that bypass the writer will fail review.

2. **The validator is exact-match.** Class tokens must start with `ara-`
   *and* be a base class in `ARA_CATALOG.json` (or a valid `--variant`
   suffix of one). The allowlist comes from the catalog, NOT from
   `COMPONENTS.md`. Tags outside the allowlist (`<style>`, `<script>`,
   `<iframe>`, `<h1>`, inline `style=`, `on*=`, `javascript:` URLs) are
   rejected. Reach for `:::raw` only when the DSL genuinely can't express
   the shape — invented classes still fail.

3. **Dashboard deploys are git-push driven — Railway is the deployer.**
   Railway watches `main` and rebuilds the Docker image on every push;
   there is no deploy workflow file. ara.guzus.xyz is served by that
   container behind Cloudflare — NOT by Vercel, whose last recorded
   deploy failed 2026-05-25 and whose config and secret are both gone
   (the remaining `VERCEL_DEPLOY_HOOK` steps are permanent no-ops).
   `dashboard/scripts/prebuild.mjs` copies `research/<source>/` into
   `public/research/` before Vite runs, so touching it changes what the
   dashboard sees. **Incident-learned corollary: the Dockerfile's package
   manager MUST stay in lockstep with the dashboard's** (bun since #102)
   — a leftover `npm ci` froze prod at a stale build for ~a day *with CI
   green*, because CI never runs the Dockerfile. Staleness is now watched
   by `scripts/check_deploy_health.py` via `liveness-check.yml`.

4. **Hooker telemetry is non-blocking.** The final telemetry step must
   never fail a job (`continue-on-error`). Don't add hard dependencies on
   telemetry success.

5. **Runner choice is load-bearing — default to self-hosted.** `gunux`
   carries the Birdy CLI + warm daemon, recent `research/` checkout, and
   pre-installed tooling (see `../runner/docs/CLOUD-RUN-SUNSET.md`). Its
   persistent home means actions must overwrite stale user-level settings
   explicitly and never assume a fresh container. Use `[self-hosted,
   Linux]` for anything touching that state — nearly everything; reserve
   `ubuntu-latest` for CI and watchdogs. The paused Cloud Run fleet is
   rollback infrastructure only; if restored, re-validate sandbox,
   Docker, state, and concurrency assumptions first.

6. **X/Twitter CLI calls must be graceful and read-only.** Use Birdy,
   pass `--json --plain`, and pipe to a fallback (`|| echo "[]"`). The
   cookies expire; workflows must continue with empty data rather than
   crash.

7. **Improvement logs belong in `docs/archive/YYYY-MM-DD-improvements.md`,**
   not repo root. The improve loop runs weekly on Mondays and auto-closes
   its own stale `improve/*` PRs.

8. **Atomic file writes.** Scripts writing into `research/` must write to
   a temp file in the same directory and `os.replace()` into place, so a
   half-finished file never reaches the dashboard prebuild — and thus the
   next deployed Railway image.

9. **Model tickets are CRUD'd, not regenerated.**
   `research/models/tickets/<slug>.md` is a persistent store — one ticket
   per shipping artifact (release, partnership, funding round, legal
   action). The `24h-model-timeline.yml` agent reads existing tickets +
   the last 24h of signal and chooses create/update/close per
   `docs/model-tickets.md`. **Never** regenerate by deleting and
   re-writing. Slugs are immutable, `history` is append-only, closure
   preserves history; `scripts/check_model_tickets.py` enforces the 5
   canonical states (rumored → in-testing → confirmed → released →
   closed). Legacy `<date>-timeline.md` files stay frozen on disk; new
   dates produce a *derived diff* of what the agent did.

10. **Wiki pages are CRUD'd, not regenerated.** `research/wiki/` is a
    compounding knowledge base — one page per entity/concept/theme, plus
    `index.md` and an append-only `log.md` (one
    `## [YYYY-MM-DD] ingest | <summary>` per run). The `wiki-ingest.yml`
    agent runs after the digest (`workflow_run`) and for each subject
    runs `scripts/wiki_search.py` first, so it UPDATEs an existing page
    (bump OKF `timestamp`, refine `[[links]]`/`aliases`) rather than
    duplicating. **Update is the default; creation is the exception.**
    Slugs are immutable (a rename updates title + aliases, never the
    filename), pages are never deleted, `log.md` is append-only.
    **The ingest reads the CURATED synthesis — the daily digest + model
    tickets — NOT the raw per-source firehose**; re-reading the raw
    sources defeats the curation the digest performs.
    `docs/wiki-schema.md` and `scripts/check_wiki.py` **must stay in
    lockstep** — a schema change unreflected in the validator silently
    corrupts the lane.

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

12. **Workflow-opened PRs need explicit token semantics.**
    `safe-push` has an automated protected-branch fallback: it pushes a
    generated branch, then attempts `gh pr create` with `GITHUB_TOKEN` when the
    workflow grants `pull-requests: write`, and by default (`pr-merge: true`)
    immediately squash-merges that PR (see rule 13). If repository settings
    still block Actions-created PRs, it leaves the generated branch in place
    and emits `publication-mode=branch` instead of failing the workflow. For agent-authored
    feature PRs, the older working pattern (used by `daily-improve.yml` and
    `twitter-account-explorer.yml`) is still valid: have the agent push the
    branch and run `gh pr create` **from inside the
    `anthropics/claude-code-action@v1` step** so the PR is authored as
    `app/claude` and triggers `pull_request` CI. In that case, set
    `env: GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` on the claude step, include
    `Bash(git push:*),Bash(gh:*)` in `--allowedTools`, and do the `gh pr create`
    in the prompt — not in a downstream plain-`GITHUB_TOKEN`
    `run:` step. (Learned when the explorer's first run curated accounts
    correctly but failed at an external publish step — PR #149.)

13. **`main` is PR-only; scheduled lanes publish via auto-merged safe-push
    PRs.** A repository ruleset (active since 2026-07-06, no bypass actors,
    squash merges only) rejects every direct push to `main` — including
    workflow `GITHUB_TOKEN` pushes — with `GH013`. Scheduled publishers
    therefore land output through safe-push's fallback: run-scoped
    `automation/safe-push/*` branch → PR → immediate squash-merge.
    `pushed=true` now means "content is on `main`" (direct, no-op, or merged
    fallback PR), and Railway still deploys on each merge because a merge IS
    a push to `main`. Two operational corollaries: (a) an
    `automation/safe-push/*` PR left OPEN means the auto-merge failed —
    usually a same-file conflict with a concurrent writer; resolve and merge
    it manually (oldest first) or the lane's data never reaches the
    dashboard, and (b) safe-push resets any checkout-persisted
    `http.<url>.extraheader` before injecting its own auth — do NOT "simplify"
    that away, or every fetch/push 400s with `Duplicate header:
    "Authorization"` (the 2026-07-06 outage: all lanes but hourly-twitter
    hard-failed at push because persisted credentials + injected header sent
    two Authorization headers).

14. **No single credential may be able to take down the whole agent fleet.**
    Every production lane in `data/agent-backends.json` routes to
    `backend: claude`, so the global `fallback.chain` is the ONLY thing
    standing between one dead credential and a total content outage. On
    2026-07-24 it wasn't: the chain was `["claude"]` and `probe_claude()`
    hardcoded "always available", so an expired `CLAUDE_CODE_OAUTH_TOKEN`
    killed every lane at once (digest, RSS, community, twitter, bluesky,
    arxiv, wiki) while `ZAI_API_KEY` sat configured and healthy — selection
    "succeeded" onto a backend that could not serve. Three invariants now
    keep that from recurring; preserve them if you edit the routing:
    (a) **`fallback.chain` spans ≥2 providers** — CI-enforced by
    `test_backend_matrix.test_global_fallback_chain_shape`. Claude leads
    (it is what the prompts are tuned against); it must not also terminate.
    (b) **`probe_claude()` is auth-only** — down on 401/403, up on
    200/429/5xx/network fault. Both sides are empirically pinned: a dead
    token answers `401 "OAuth access token is invalid."`, while a *live*
    subscription token answers the same raw 1-token ping with **429**. So
    treating non-200 as down would reroute a healthy fleet off Claude
    permanently. It must send
    `authorization: Bearer` + the oauth beta header and **never**
    `x-api-key` (which makes the API reject a *good* OAuth token with
    `401 invalid x-api-key`). `agent-run` must keep passing
    `CLAUDE_CODE_OAUTH_TOKEN` into the select step or the probe reports
    "not configured" and every lane reroutes.
    (c) **Deterministic fallbacks are damage control, not the fix** — the
    digest's model-free composer did fire and published, which is why the
    site stayed up, but it publishes an uncurated verbatim dump under a
    banner saying so. A green run on a fallback lane is not evidence the
    agent path is healthy; check the fallback-used Telegram alert.

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
- **X/Twitter CLI invocations:** Birdy read-only mode, `--json --plain`,
  and `|| echo "[]"` fallback.
- **Claude prompts in workflows:** quote multi-line prompts with `|`
  block scalars; pass user-controlled values (issue title/body) through
  `env:` rather than direct `${{ }}` interpolation in `run:` blocks
  to avoid script-injection.

## Component catalog

The article-fragment class allowlist is **`ARA_CATALOG.json`** (87 base
`ara-*` classes). The validator loads it from there, NOT from
`COMPONENTS.md` — that file is the human reference, kept in perfect
lockstep by `scripts/ara_catalog.py` and CI-enforced via `test_ara_dsl.py`.
To add a primitive, edit BOTH files in the same PR and ship the matching
CSS; a class in one but not the other fails CI.

**A higher CSS class count than the catalog is expected, not drift.** Two
layers live outside the article-fragment contract on purpose:
`dashboard/src/components/ara-research.css` also carries runtime extras
injected by `main.ts` (table of contents, figure lightbox, chart
tooltips/axes/generated `ara-chart-series-*`), and `style.css` carries the
front-page template classes (`ara-paper-*`), which are a newspaper render,
not an ARA article. Neither ever appears in `.ara.md`, so neither belongs
in the allowlist. Only worry about an undocumented class if it shows up in
an *article fragment* — and then fix the catalog + COMPONENTS.md, not the
CSS, which likely already has it.

## Historical Docs

Pre-2026-Q2 improvement logs live in [`docs/archive/`](docs/archive/).
They're kept for context but no longer load-bearing.
