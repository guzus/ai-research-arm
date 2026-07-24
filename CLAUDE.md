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
| [`ARA_DSL.md`](ARA_DSL.md) | Source format for generative-research articles. The compiler at `scripts/compile_ara.py` turns `.ara.md` into a validated `<article>` fragment. |
| [`COMPONENTS.md`](COMPONENTS.md) | Human reference for the `ara-*` component vocabulary. The machine-readable contract the validator loads is [`ARA_CATALOG.json`](ARA_CATALOG.json); the two are kept in lockstep (CI-enforced — see "Component catalog" below). The CSS at `dashboard/src/components/ara-research.css` is the rendering source of truth and intentionally carries *more* `ara-*` classes than the article allowlist (runtime + front-page layers). |
| [`ARA_CATALOG.json`](ARA_CATALOG.json) | Machine-readable ara-* component catalog the validator loads its class allowlist from. `scripts/ara_catalog.py` validates it stays in lockstep with COMPONENTS.md (CI-enforced; see "Component catalog" below). |
| [`docs/generative-research-backends.md`](docs/generative-research-backends.md) | Backend matrix for the generative-research lane (Claude vs Codex vs Fireworks vs local Oracle), env mapping, comparison commands. |
| [`docs/okf.md`](docs/okf.md) | Open Knowledge Format export contract for sharing `research/wiki/` as a portable Markdown/YAML knowledge bundle. |
| [`docs/model-tickets.md`](docs/model-tickets.md) | Schema + lifecycle + dedup protocol for `research/models/tickets/*.md`. Read by the CRUD agent in `24h-model-timeline.yml` and enforced by `scripts/check_model_tickets.py`. |
| [`docs/wiki-schema.md`](docs/wiki-schema.md) | Canonical schema + page conventions for the LLM Wiki (`research/wiki/`). Read at runtime by the ingest agent in `wiki-ingest.yml` and enforced by `scripts/check_wiki.py`. |
| [`docs/hooker-telemetry.md`](docs/hooker-telemetry.md) | Non-blocking telemetry route via `https://hooker.guzus.xyz` topic `ara-telemetry`. |
| [`docs/headline-dedupe.md`](docs/headline-dedupe.md) | Dedup contract + Mermaid flow for the Twitter headline-alert ledger (`research/summaries/twitter-announced-history.json`): the deterministic layered `duplicate_reason` check (`scripts/dedupe_headline_alerts.py`) **plus** the agent-in-the-loop Haiku gate (`scripts/headline_judge.py`) that adjudicates the contested sub-floor band. Used by `hourly-twitter.yml`. |
| [`docs/blog-subscriptions.md`](docs/blog-subscriptions.md) | GUID-based RSS subscription, first-run seeding, proven Telegram delivery, partial-delivery acknowledgement, and durable state contract for `blog-subscriptions.yml`. |
| [`docs/archive/`](docs/archive/) | Historical improvement logs and superseded docs. |
| `dashboard/` | Vite + Bun + TypeScript SPA. `prebuild.mjs` copies `research/*` into `public/research/` and emits `manifest.json`; Railway auto-deploys on every push to `main` (next row). |
| [`Dockerfile`](Dockerfile) + [`Caddyfile`](Caddyfile) + [`railway.json`](railway.json) | The Railway deploy stack serving **ara.guzus.xyz** (behind Cloudflare — responses carry `x-railway-edge`). The root `Dockerfile` builds the dashboard with bun (`oven/bun:1-alpine`, plus `nodejs` for the pre/postbuild node scripts) and serves `dashboard/dist` with Caddy; `railway.json` pins the DOCKERFILE builder + `/` healthcheck. the legacy `dashboard/vercel.json` Vercel config was removed during open-sourcing; Vercel no longer serves the domain (Load-bearing rule 3). |
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
| `dedupe_headline_alerts.py` | Filter + record delivered Twitter headline alerts (used by `hourly-twitter.yml`). Layered deterministic dedup contract + Mermaid diagrams in [`docs/headline-dedupe.md`](docs/headline-dedupe.md). |
| `headline_judge.py` | Agent-in-the-loop final dedup gate (used by `hourly-twitter.yml`). Two deterministic subcommands — `shortlist` (surface send-set survivors whose nearest prior sits in the contested `[0.35,0.50)` Jaccard band) and `apply` (drop only the Haiku judge's HIGH-confidence duplicates, fail-open, URL-keyed) — bracketing one Haiku adjudication step. Contract in [`docs/headline-dedupe.md`](docs/headline-dedupe.md). |
| `curate_twitter_accounts.py` | Validates `data/sources/twitter_accounts.json`, builds the birdy fetch manifest, and writes/apply reviewable Twitter account add/remove proposals. |
| `explore_twitter_accounts.py` | Scout script for `twitter-account-explorer.yml`; runs broad bird searches and emits candidate JSON for reviewed account curation. Scores from three bounded signals — trust-weighted mentions (a mention-graph candidate needs ≥1 *monitored* citer, not just any search-surfaced one), AI topicality (bonus for AI-vocabulary terms in the evidence), and bounded engagement — so viral off-topic/spam accounts don't outrank genuine AI sources. Contract: [`docs/twitter-account-curation.md`](docs/twitter-account-curation.md). |
| `check_model_tickets.py` | Validator for `research/models/tickets/*.md` against the schema in `docs/model-tickets.md`. The CRUD agent in `24h-model-timeline.yml` runs it after every pass; CI runs it on every PR. |
| `check_wiki.py` | Validator for `research/wiki/` pages against the schema in `docs/wiki-schema.md`. `uv run python scripts/check_wiki.py` (exit 0 = safe); `--lint` adds advisory checks. The ingest agent in `wiki-ingest.yml` runs it until exit 0; CI runs it on every PR. |
| `wiki_search.py` | Search wrapper over `research/wiki/` (`uv run python scripts/wiki_search.py "<query>"`). The ingest agent runs it before writing any page so it UPDATEs an existing page instead of duplicating. |
| `export_wiki_okf.py` | Export `research/wiki/` as a portable Open Knowledge Format bundle: validates the OKF-native wiki pages and rewrites `[[wikilinks]]` to standard Markdown links. |
| `check_lane_freshness.py` | Freshness watchdog. Measures git-commit recency per research lane against per-lane cadence thresholds; exits 2 (and emits a hooker/Telegram alert from `liveness-check.yml`) when a lane is stale. Stdlib-only so it runs on both runner tiers. |
| `build_wiki_index.py` | Rebuilds `research/wiki/index.json` from the wiki pages. **CI-load-bearing**: `ci.yml` runs `--check` (exit 1 if the committed index is stale or any page fails validation); `wiki-ingest.yml` regenerates it every run. |
| `build_backend_matrix.py` | Cross-checks the routing SSOT (`data/agent-backends.json`) against `.github/workflows/*` (lane exists, all provider secrets passed, pi/native mirrors match) and regenerates the lane table in `docs/backend-matrix.md`. **CI-load-bearing**: `ci.yml` runs `--check`. |
| `resolve_backend_lane.py` | Stdlib-only field resolver for `data/agent-backends.json` — generative-research calls it on the runner for its SSOT default backend. Unknown lane = hard failure (never a silent default). |
| `select_backend.py` | Stdlib-only runtime backend selector used by `.github/actions/agent-run`: resolves the lane, probes the requested provider, and walks the ordered `fallback.chain` — first available candidate wins; strict lanes/`fireworks-fallback: none` never fall back. The claude probe is auth-only and has two traps — see Load-bearing rule 14. |
| `fetch_ai_blogs.py` | Per-feed AI-blog fetcher used by `daily-ai-blogs.yml`; boundary-handles bad feeds so one failure doesn't crash the run. |
| `watch_blog_subscriptions.py` | RSS subscription watcher used by `blog-subscriptions.yml`; seeds historical GUIDs without alerting, verifies Telegram responses, and acknowledges each proven delivery atomically. |
| `deterministic_rss_digest.py` | Model-free fallback for `hourly-rss.yml`; parses fetched RSS/Atom files and appends a timestamped `research/rss/YYYY-MM-DD.md` section when the agent path fails. |
| `deterministic_community_digest.py` | Model-free fallback for `4h-community.yml`; parses pre-fetched HN JSON and Reddit RSS into `research/community/*-hn.md` and `*-reddit.md` when the agent path fails. |
| `deterministic_twitter_digest.py` | Fail-closed operational fallback for the primary `hourly-twitter.yml` lane. The workflow first restores the public digest exactly to its pre-agent Git baseline; the script never reads Birdy data or authors news, and only writes a run-ID/attempt-scoped `no_update` recovery heartbeat plus empty summary/headline artifacts. The heartbeat is pushed for observability, then the workflow fails loudly and skips notifications. |
| `validate_twitter_public_output.py` | Enforces the Twitter signal-only contract after every backend: this run's heartbeat identity, exact public-item count, concrete story/Quick-hit presence, normalized same-hour headings, empty no-update reader artifacts, and no operational/no-news filler. |
| `deterministic_arxiv_digest.py` | Model-free fallback for `daily-arxiv.yml`; queries the arXiv Atom API directly and writes an uncurated per-category `research/arxiv/<date>-papers.md` when the agent path fails (zero-paper windows still write an honest empty note). |
| `deterministic_daily_digest.py` | Model-free fallback for `daily-digest.yml`; composes `research/digest/<date>-digest.md` (+ Telegram summary) verbatim from the day's committed lane artifacts when the agent fails or its output falls below the content floor. Never invents content; missing lanes are noted explicitly. |
| `deterministic_bluesky_digest.py` | Model-free fallback for `2h-bluesky.yml`; composes the per-run `.tmp/bluesky-section.md` (engagement-ranked, ≤8 bullets / ≤3 per author, 48h window) from the staged `data/bluesky/*.json` when the agent writes no section. |
| `check_digest_content.py` | Per-run hard content floor for the daily digest (`--min-bytes`, `--min-sections`, unexpanded-placeholder scan). `daily-digest.yml` runs it after the synthesis agent to decide whether the deterministic fallback composer takes over; complements the advisory `check_lane_content.py`. |
| `fetch_youtube_signal.py` | tuber-backed YouTube lane used by `daily-youtube.yml`; read-only by default (discovery, existing summary previews, transcript probes) and never triggers paid summary generation. |
| `source_cache.py` | Runtime primary-source fetch cache under `data/source-cache/` (gitignored), used by `generative-research.yml`. |
| `render_front_page.mjs` | Deterministic newspaper renderer used by `daily-front-page.yml`: digest → SVG → PNG via `@resvg/resvg-js` (no Chromium/model dependency), plus the `.ara.md` source for the interactive edition. Layout is budget-aware — overflow is ellipsized/dropped, never painted over. |
| `test_ara_dsl.py`, `test_dedupe_headline_alerts.py`, `test_headline_judge.py` | Pytest-style tests run in CI. (`test_ara_dsl.py` also asserts `ARA_CATALOG.json` ↔ `COMPONENTS.md` lockstep.) |

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

Almost every workflow runs on **`runs-on: [self-hosted, Linux]`** on the
native Ubuntu host `gunux`, with one systemd-managed runner for this repo.
The old Cloud Run worker pools are paused rollback infrastructure, not the
production path. The runner's home directory is persistent across jobs, so
user-level tool configuration can survive from one run to the next. The host
carries the Birdy read-only CLI/daemon, recent `research/` checkout, and
pre-installed tooling used by aggregation, synthesis, output, and agent lanes.

GitHub-hosted runners are used for jobs that must not execute
repository-controlled code on the self-hosted fleet:
- `ci.yml` runs on `ubuntu-latest`. Pull requests can change dashboard
  build scripts, package scripts, Python tests, and workflow/action files,
  so CI must not execute that code on the self-hosted runner host.
- Watchdog jobs also run on `ubuntu-latest` because they must survive a
  self-hosted outage — a watchdog that runs on the runners it is
  watching is useless:
- `liveness-check.yml` runs one job on EACH tier (its `ubuntu` job + its
  `self-hosted` job). No single runner survives both failure modes — a
  GitHub-hosted billing/spending-limit block vs. a self-hosted outage — so
  whichever tier is alive emits the hooker/Telegram staleness alert.
- `auto-rerun-on-runner-loss.yml` re-runs jobs whose runner process
  vanished mid-run (Load-bearing rule 11; primarily a rollback-fleet guard).

The per-workflow `ubuntu-latest` vs. `self-hosted` lists that used to live
here are gone on purpose: the answer is now "read the workflow's actual
`runs-on:`; most production lanes are self-hosted, but CI and watchdogs are
deliberately GitHub-hosted." **Always read the workflow's actual `runs-on:` —
never trust a cached list** (the old list here drifted to 100% wrong once
the autoscaler landed and the stateless lanes moved back to self-hosted).

Scheduled content workflows should use `.github/actions/agent-run` instead
of calling `anthropics/claude-code-action@v1` directly. The wrapper keeps the
Claude-Code-compatible tool harness but routes the primary freshness lanes
through Fireworks profiles when Fireworks preflight passes. If Fireworks is
unavailable (for example billing/spend-limit suspension), the wrapper falls
back to native Claude by default so scheduled freshness does not hard-stop.
It also enforces output and commit-scope contracts for agent lanes:
`.github/actions/require-output` proves every expected output pathspec changed,
while `.github/actions/require-diff-scope` proves the committed diff since
the pre-agent SHA is limited to the declared allowed pathspecs. Use
`expected-paths` for the exact artifact files that must exist when their names
are known, and `allowed-paths` for the full set of paths the agent may commit
(for example, a primary digest directory plus `research/summaries/`). The RSS,
HN/Reddit community, arXiv,
daily-digest, and Bluesky workflows (plus the twitter-deepseek comparison tier)
add deterministic model-free fallbacks after the agent step, then run a final
`.github/actions/require-output` guard — the digest additionally gates its
agent output on a hard content floor (`scripts/check_digest_content.py`) before
the fallback decision. For those lanes, a green run means a committed daily
artifact exists; inspect the agent/fallback step logs before treating it as
evidence that Fireworks or native Claude was healthy. PR/review/on-demand
Claude workflows may still call the Claude action directly; when they do, pass
the model via `claude_args` (e.g. `"--model claude-sonnet-5"`) — never as a
separate `model:` input.

Publishing generated commits uses `.github/actions/safe-push`. Direct pushes
to protected branches may be rejected by repository rules requiring pull
requests; in that case `safe-push` publishes the commit to a run-scoped
`automation/safe-push/...` branch and attempts to open a PR. It emits
`pushed=false` and `publication-mode=pull-request` (or `branch` if repository
settings block Actions-created PRs), so downstream deploys and public
notifications must continue to gate on `steps.push.outputs.pushed == 'true'`
when they link to `main`.

Claude Code runs are protected by the checked-in `.claude/settings.json`
sandbox policy. On Linux this requires `bubblewrap` and `socat`; workflows
that call Claude directly must run `.github/actions/setup-claude-sandbox`
before the Claude action, and scheduled lanes that use `.github/actions/agent-run`
get that setup centrally. The policy sets `sandbox.failIfUnavailable: true`
and `sandbox.allowUnsandboxedCommands: false`, so a missing sandbox fails
the workflow instead of silently running Bash commands with host filesystem
access. It also blocks reads of common host credential paths such as `~/.ssh`,
`~/.aws`, `/proc`, and `/var/run`.

Pi comparison lanes do not read Claude Code settings. When `hourly-twitter.yml`
runs `deepseek-pi` or `fireworks-pi`, it must use
`.github/actions/run-pi-container` instead of invoking `pi` on the host. That
wrapper builds a small Node container with `pi`, `bird`, `git`, and `jq`, mounts
only `$GITHUB_WORKSPACE`, `/tmp/bird` read-only, and the rendered prompt file,
then runs pi with a container-local home directory. Missing Docker is a hard
failure for pi lanes; do not fall back to host-level `pi --tools ... bash`.

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

Model convention: scheduled content workflows pass `--model opus` to the
Claude-Code-compatible CLI, but that alias is remapped by `agent-run`: to
the Fireworks profile model (`fireworks-deepseek-v4-flash` or
`fireworks-glm-5p2`) when preflight passes, to `zai-glm-5p2` for the
Z.ai Coding Plan route, or to the action's `native-model` input
(default **`claude-sonnet-5`**) on native-Claude runs and Fireworks
fallbacks. Direct Claude workflows pin
`--model claude-sonnet-5` through `claude_args`; defer to the workflow
file rather than assuming one provider everywhere.

## Backends

The table below is the per-*backend* contract. **Per-lane routing, the
backend profile table, and the ordered fallback chain are all defined in
[`data/agent-backends.json`](data/agent-backends.json) — the single source
of truth.** agent-run lanes resolve it at runtime via
`scripts/select_backend.py`, which probes providers and walks
`fallback.chain` in order when the requested one is down (edit the file to
re-route or re-order fallbacks with no workflow change; every call site
carries all provider secrets). pi and direct claude-code-action lanes are
CI-enforced mirrors. Strict lanes (zai-canary) never fall back. The human
view is the generated matrix in
[`docs/backend-matrix.md`](docs/backend-matrix.md); after any routing
change run `uv run python scripts/build_backend_matrix.py` (CI runs
`--check`).

| Backend | When | Auth | Notes |
|---|---|---|---|
| **Claude** | Explicit native-Claude workflows; `generative-research backend=claude`; Fireworks fallback path | `CLAUDE_CODE_OAUTH_TOKEN` | Native Anthropic. Default model **`claude-sonnet-5`** everywhere native Claude runs (the global `fallback.native_model` in `data/agent-backends.json`). Claude is a fallback or explicit comparison choice, not the preferred backend for generative content routing. |
| **Codex** | `generative-research backend=codex` | `CODEX_AUTH_JSON` | Runs Codex CLI with ChatGPT-managed file auth (`auth.json` from `codex login`), so usage follows the ChatGPT/Codex subscription entitlement rather than API billing. Publishes through the same writer/verifier contract and records `codex` metadata. |
| **Kimi K3 (via opencode)** | `generative-research backend=opencode-kimi-k3`; `hourly-twitter.yml backend=opencode-kimi-k3` manual comparison lane; `opencode-kimi-canary.yml` diagnostics | `OPENCODE_API_KEY` (OpenCode Go, preferred) or `MOONSHOT_API_KEY` (fallback) | Runs the opencode CLI (pinned `opencode-ai@1.18.3`; Moonshot's opencode guide requires >= 1.18.3 for kimi-k3) against Kimi K3 (1M context, $3/$15 per Mtok, $0.30 cache-hit). The workflow resolves the route Go-first: `opencode-go/kimi-k3` on the OpenCode Go subscription ($10/mo; usage caps $12/5h, $30/wk, $60/mo with K3 billing at full $3/$15 value), else `moonshotai/kimi-k3` pay-per-token. Auth is the plain env-var key on both routes — no interactive `opencode auth login`, no auth.json seeding. Selector tokens: `opencode-kimi-k3`, `opencode`, `opencode-kimi`, `kimi-k3`, `kimi`. Strict: the resolved route is preflighted and fails fast (no Claude fallback) so a Kimi-labeled article can never be silently authored by another model. Kimi K3 is NOT on Fireworks or pay-as-you-go OpenCode Zen as of 2026-07-20 (open weights promised by ~Jul 27); revisit Fireworks routing after the weights land. Publishes through the same writer/verifier contract and records `kimi-k3` metadata. |
| **GLM 5.2 (via Fireworks, preferred)** | Default `.github/actions/agent-run` backend; default `generative-research backend=glm-5p2`; primary scheduled RSS/Bluesky/Twitter/digest synthesis lanes | `FIREWORKS_API_KEY` | Uses the same Fireworks Anthropic-compatible env slots with model `accounts/fireworks/models/glm-5p2`. Selector token: `fireworks-glm-5p2`, `glm-5p2`, or `glm`. In scheduled `agent-run` lanes a Fireworks preflight failure walks the ordered `fallback.chain` in `data/agent-backends.json` (currently native Claude → Z.ai GLM); in `generative-research.yml` the workflow-level `fireworks_fallback` input still falls back to native Claude by default. |
| **GLM 5.2 (via Z.ai Coding Plan, preferred manual Twitter lane)** | `.github/actions/agent-run backend=zai-glm-5p2`; default manual `hourly-twitter.yml` backend; `zai-claude-code-canary.yml` for diagnostics | `ZAI_API_KEY` | Uses Z.ai's Anthropic-compatible Claude Code endpoint at `https://api.z.ai/api/anthropic` with model `glm-5.2` and `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000`. The `glm-5.2[1m]` alias was rejected by this endpoint with `Unknown Model` in canary run `28751367808`, so keep this workflow on the endpoint-valid model id unless a later raw probe proves the alias is accepted. Selector token: `zai-glm-5p2`, `zai-glm-5.2`, `zai-glm52`, or `zai`. Strict lanes (`zai-canary`, the comparison tiers) fail closed when Z.ai is unavailable; non-strict lanes walk the SSOT `fallback.chain`. If the primary Twitter analyst produces no valid files, its deterministic recovery path restores the public digest baseline, persists a recovery heartbeat, and deliberately fails the job; it never synthesizes replacement news. |
| **DeepSeek V4 Flash (via Fireworks)** | Explicit low-cost/comparison routes: `generative-research backend=deepseek-v4-flash`; `hourly-twitter.yml` DeepSeek comparison lanes | `FIREWORKS_API_KEY` | Uses Fireworks' Anthropic-compatible endpoint at `https://api.fireworks.ai/inference` with model `accounts/fireworks/models/deepseek-v4-flash` (base URL omits `/v1`; the client appends `/v1/messages`). Overrides `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`/`ANTHROPIC_MODEL` so the Claude Code action transparently calls Fireworks. The direct DeepSeek API (`api.deepseek.com`) is retired (billing/credits). Selector token: `fireworks-deepseek-v4-flash`, `deepseek-v4-flash`, or `deepseek`. In `generative-research.yml`, a Fireworks preflight failure falls back to native Claude by default (`fireworks_fallback=none` opts back into hard failure); scheduled `agent-run` DeepSeek lanes are STRICT comparison tiers that never fall back. Generative-research retries up to 2x on socket drops before commit. |
| **Fireworks pi** | `hourly-twitter.yml backend=fireworks-pi` manual comparison lane | `FIREWORKS_API_KEY` | Uses pi's built-in Fireworks provider with `accounts/fireworks/models/kimi-k2p7`; writes `research/twitter-fireworks-pi/` plus a Telegram summary. |
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
| `CLAUDE_CODE_OAUTH_TOKEN` | Native Claude workflows and `.github/actions/agent-run` | Required by `anthropics/claude-code-action@v1`; Fireworks-routed wrapper runs still pass it for action schema compatibility. **Expiry is a fleet-wide outage** — every production lane routes to `backend: claude`. Signature in the logs: `is_error: true`, `num_turns: 1`, `total_cost_usd: 0`, `duration_ms` under ~2000, `permission_denials_count: 0`, i.e. the agent dies before it does any work (`show_full_output` is off, so the provider error body is hidden — that shape IS the diagnosis). Re-mint with `claude setup-token` and `gh secret set CLAUDE_CODE_OAUTH_TOKEN`. To tell a dead credential from a broken runner/sandbox, dispatch `zai-claude-code-canary.yml`: it exercises the same Claude Code harness and bwrap sandbox over a different credential, so canary-green + lanes-red isolates the fault to the Claude token. Last expiry: 2026-07-24 (see Load-bearing rule 14). |
| `CODEX_AUTH_JSON` | `generative-research backend=codex` | Required for the Codex CLI ChatGPT-auth path. Store the file-backed `~/.codex/auth.json` produced by `codex login`; treat it like a password and use one auth file per serialized runner stream. |
| `OPENCODE_API_KEY` | `generative-research backend=opencode-kimi-k3`; `opencode-kimi-canary.yml` | OpenCode Go subscription key (sign in at https://opencode.ai/auth, subscribe to Go, copy the key). Preferred Kimi K3 route; the opencode CLI reads it straight from env. Validate with the canary workflow before a full research run; watch the Go usage caps ($12/5h, $30/wk, $60/mo — K3 bills at full $3/$15 value). |
| `MOONSHOT_API_KEY` | `generative-research backend=opencode-kimi-k3` (fallback route when `OPENCODE_API_KEY` is unset); `opencode-kimi-canary.yml` | Moonshot platform API key from https://platform.kimi.ai/console/api-keys (account needs real balance — new-user vouchers cannot bill kimi-k3). Pay-per-token alternative to the Go subscription. |
| `DEEPSEEK_API_KEY` | _Retired_ — DeepSeek lanes now route through Fireworks | No longer referenced by any workflow. |
| `FIREWORKS_API_KEY` | Preferred scheduled content lanes through `.github/actions/agent-run`; `generative-research backend=glm-5p2`; explicit DeepSeek/Kimi comparison lanes | Required for the GLM-via-Fireworks, DeepSeek-V4-Flash, and Kimi lanes. |
| `ZAI_API_KEY` | `.github/actions/agent-run` when `backend=zai-glm-5p2`; default manual `hourly-twitter.yml backend=zai-glm-5p2`; `zai-claude-code-canary.yml` | Z.ai Coding Plan API key for Claude Code's Anthropic-compatible route. |
| `BIRD_AUTH_TOKEN`, `BIRD_CT0` | All bird-CLI workflows (`hourly-twitter*`, `24h-model-timeline`) | X/Twitter cookies. |
| `EXA_API_KEY`, `PERPLEXITY_API_KEY` | `daily-digest`, `ai-news-research`, `research-issue` | Optional; enhance MCP search. **Currently unset in the repo** (verified absent 2026-07-02) — `daily-digest` detects the absence, emits a run warning, and uses its local-source synthesis path until they are restored. |
| `GEMINI_API_KEY` | `daily-digest` (inline Gemini Flash TTS for digest audio); also the manual `generate_generative_article_audio.py` | Optional; without it, audio generation is skipped. |
| `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`, `S3_ENDPOINT_URL`, `S3_BUCKET` | `daily-digest` (audio upload) | Optional; generated digest mp3s upload to S3 while the working tree keeps 0-byte stubs. Missing = upload skipped. |
| `HOOKER_TOKEN` | Telemetry composite action | Optional; without it, telemetry steps no-op. |
| `HOOKER_URL` | Hooker telemetry composite + most workflows (the hooker endpoint, distinct from `HOOKER_TOKEN`) | The `https://hooker.guzus.xyz`-style base URL the telemetry/alert steps POST to. Referenced widely across workflows/actions. |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | `blog-subscriptions.yml`, `daily-digest.yml`, `liveness-check.yml` | For subscribed-blog alerts, digest delivery, and liveness escalation. |
| `VERCEL_DEPLOY_HOOK` | `24h-model-timeline`, `wiki-ingest`, `hourly-twitter` (claude tier) | **Secret removed from the repo** (verified absent 2026-07-02); the referencing steps are permanent no-ops kept as legacy scaffolding and safe to delete in a future cleanup. Vercel does NOT serve ara.guzus.xyz — prod deploys are Railway, git-push driven (Load-bearing rule 3). |
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
   NOT by Vercel, whose last recorded deploy failed 2026-05-25. Its
   `dashboard/vercel.json` was removed during open-sourcing, and the
   `VERCEL_DEPLOY_HOOK` secret has since been deleted from the repo —
   the steps that still reference it in a few workflows are permanent
   no-ops. There is still no workflow file for deploys.
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
   production self-hosted tier is the native Ubuntu host `gunux`, with one
   persistent systemd runner per repository (see
   `../runner/docs/CLOUD-RUN-SUNSET.md`). It carries the Birdy read-only CLI +
   warm daemon (`hourly-twitter*`, `24h-model-timeline`), recent `research/`
   checkout context, and pre-installed tooling. Its persistent home also
   means actions must overwrite stale user-level settings explicitly and
   must not assume a fresh container. Digest audio lives in S3 (uploaded by
   `daily-digest` via the `S3_*` secrets; the committed
   `research/audio/*.mp3` files are 0-byte stubs), while `daily-front-page`
   renders via resvg and commits the PNG alongside the interactive edition.
   Use `[self-hosted, Linux]` for anything touching that state, which is
   nearly everything. Reserve `ubuntu-latest` for watchdogs and CI jobs that
   must survive or avoid the self-hosted tier. The paused Cloud Run fleet is
   rollback infrastructure only; if it is deliberately restored, re-validate
   sandbox, Docker, state, and concurrency assumptions before routing jobs.

6. **X/Twitter CLI calls must be graceful and read-only.** Use Birdy for
   Twitter workflows, pass `--json --plain`, and pipe to a fallback
   (`|| echo "[]"`). The Twitter cookies expire; workflows must continue
   (with empty data) rather than crash the run.

7. **Improvement logs belong in `docs/archive/`.** When
   `daily-improve.yml` (or any agent) generates a new improvements
   file, write it to `docs/archive/YYYY-MM-DD-improvements.md`, not
   to repo root. (The workflow prompt now says this too — the old
   "Create an IMPROVEMENTS.md" wording is gone. The improve loop runs
   weekly on Mondays and auto-closes its own stale `improve/*` PRs.)

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
    (bump the OKF `timestamp`, refine `[[links]]`/`aliases`) rather than
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

The article-fragment class allowlist lives in **`ARA_CATALOG.json`**
(currently 87 base `ara-*` classes). The validator
(`scripts/check_generative_research.py` → `write_generative_research.py`
→ `ara_catalog.load_catalog`/`catalog_classes`) loads its allowlist from
that file, NOT from `COMPONENTS.md`. `COMPONENTS.md` is the human
reference and documents the **same cataloged base classes**;
`scripts/ara_catalog.py` (`validate_catalog_against_components`) asserts
the two stay in perfect lockstep and CI enforces it via
`test_ara_dsl.py`. To add a new primitive, add it to BOTH files in the
same PR (and ship the matching CSS); a class present in one but not the
other fails CI.

The CSS intentionally defines **more** `ara-*` classes than the article
allowlist. The extra classes are NOT drift and are NOT a commit-time
rejection risk — they belong to layers that live outside the
article-fragment contract on purpose:

- `dashboard/src/components/ara-research.css` defines more `ara-*`
  classes than the catalog: the cataloged article primitives (`ara-doc`,
  `ara-callout`, `ara-figure`, …) that DO appear in `.ara.md` and ARE the
  allowlist, **plus** **runtime/interactive extras** — table-of-
  contents, figure lightbox, chart tooltips/axes/series, generated chart
  internals (e.g.
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
