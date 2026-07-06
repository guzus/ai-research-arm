# Backend Matrix — harness × token provider per workflow

This is the **canonical per-workflow mapping** of which agent harness each
GitHub Actions workflow runs, which provider serves its tokens, under which
model id, authenticated by which GitHub secret, and what the fallback chain
is. The per-*backend* contracts (env slots, endpoints, selector tokens) live
in `CLAUDE.md` → "Backends" and `docs/generative-research-backends.md`; this
file is the per-*workflow* view that used to exist only implicitly across
the workflow files.

The table below is **generated, not hand-maintained** — the repo has been
burned twice by hand-maintained lists drifting (the `runs-on:` list, the
pre-Z.ai backend table). Rows are derived from `.github/workflows/*.yml`
plus the backend profile block in `.github/actions/agent-run/action.yml`:

```bash
uv run python scripts/build_backend_matrix.py          # regenerate after editing a workflow
uv run python scripts/build_backend_matrix.py --check  # CI gate: exit 1 when stale
```

CI runs `--check` on every PR that touches workflows, actions, scripts, or
this file — a workflow edit that changes a lane's harness/provider/token
fails CI until this table is regenerated in the same PR.

## Harness vocabulary

| Harness | What it means | Where defined |
|---|---|---|
| Claude Code · agent-run | `anthropics/claude-code-action@v1` wrapped by the local composite: backend profile selects provider env (Fireworks / Z.ai Anthropic-compatible endpoints, or native), preflights Fireworks, falls back to native Claude, then enforces `expected-paths` / `allowed-paths`. | `.github/actions/agent-run/action.yml` |
| Claude Code · claude-code-action (direct) | The action invoked directly. Native Anthropic unless the step's `env` reroutes `ANTHROPIC_BASE_URL` (generative-research does this for its Fireworks paths). | each workflow step |
| pi · run-pi-container | The pi coding-agent harness in a container, with pi's own provider config. Twitter comparison tiers only. | `.github/actions/run-pi-container/action.yml` |
| Codex CLI | `codex exec` with ChatGPT-managed file auth (subscription entitlement, not API billing). | `generative-research.yml` codex path |

Reading notes:

- **Token secret** is the secret that pays for the tokens on the requested
  path. Every agent-run and direct-action step *also* receives
  `CLAUDE_CODE_OAUTH_TOKEN` because the action's input schema requires it —
  for Fireworks/Z.ai-routed runs it is inert unless the native-Claude
  fallback fires.
- **`--model opus` in `claude_args` is an alias**, not a provider model:
  agent-run remaps it to the profile model id (Fireworks/Z.ai) or to
  `native-model` (default `claude-sonnet-5`) on the native path.
- **Fallback** shows the chain: provider fallback first (Fireworks preflight
  → native Claude unless `fireworks-fallback: none`; Z.ai fails closed),
  then `; then \`deterministic_*.py\`` where the lane has a model-free
  composer guarding output freshness.
- `hourly-twitter.yml` lane names are the *tier* selectors from its matrix.
  Historical warning: the tier named `claude` is the tier *slot* name — its
  requested backend is whatever the workflow passes (GLM-5.2 via Fireworks
  since 2026-07-06), which is exactly why this table exists.
- `generative-research.yml`'s Fireworks model is `dynamic:` because one env
  block serves both `deepseek-v4-flash` and `glm-5p2` via its profile step.

<!-- BEGIN GENERATED BACKEND MATRIX (scripts/build_backend_matrix.py — do not edit by hand) -->

### Model lanes

| Workflow | Lane | Harness | Provider | Model | Token secret | Fallback |
|---|---|---|---|---|---|---|
| `24h-model-timeline.yml` | crud-model-tickets-via-fireworks | Claude Code · agent-run | GLM 5.2 via Fireworks | `accounts/fireworks/models/glm-5p2` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`) |
| `2h-bluesky.yml` | process-bluesky-feed-with-glm-5-2-via-fireworks | Claude Code · agent-run | GLM 5.2 via Fireworks | `accounts/fireworks/models/glm-5p2` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`); then `deterministic_bluesky_digest.py` |
| `4h-community.yml` | process-community-data-with-fireworks | Claude Code · agent-run | GLM 5.2 via Fireworks | `accounts/fireworks/models/glm-5p2` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`); then `deterministic_community_digest.py` |
| `ai-news-research.yml` | run-ai-news-research-with-claude-with-mcp | Claude Code · claude-code-action (direct) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| `ai-news-research.yml` | run-ai-news-research-with-claude-without-mcp | Claude Code · claude-code-action (direct) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| `claude-code-review.yml` | run-claude-code-review | Claude Code · claude-code-action (direct) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| `claude.yml` | run-claude-code | Claude Code · claude-code-action (direct) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| `daily-arxiv.yml` | fetch-arxiv-ai-papers | Claude Code · agent-run | GLM 5.2 via Fireworks | `accounts/fireworks/models/glm-5p2` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`); then `deterministic_arxiv_digest.py` |
| `daily-digest.yml` | synthesize-daily-digest-with-mcp-tools | Claude Code · agent-run | GLM 5.2 via Fireworks | `accounts/fireworks/models/glm-5p2` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`); then `deterministic_daily_digest.py` |
| `daily-digest.yml` | synthesize-daily-digest-local-source-fallback | Claude Code · agent-run | GLM 5.2 via Fireworks | `accounts/fireworks/models/glm-5p2` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`); then `deterministic_daily_digest.py` |
| `daily-digest.yml` | rewrite-summary-as-ara-spoken-script-glm-5-2-via-fireworks | Claude Code · agent-run | GLM 5.2 via Fireworks | `accounts/fireworks/models/glm-5p2` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`); then `deterministic_daily_digest.py` |
| `daily-improve.yml` | analyze-and-improve-methodology | Claude Code · claude-code-action (direct) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| `generative-research.yml` | backend=claude (+1 retry step) | Claude Code · claude-code-action (direct) | Anthropic (native) | `opus` → `claude-sonnet-5` (env pin) | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| `generative-research.yml` | backend=codex | Codex CLI | OpenAI (ChatGPT subscription auth) | codex CLI default | `CODEX_AUTH_JSON` | — |
| `generative-research.yml` | backend=fireworks (deepseek-v4-flash / glm-5p2) (+2 retry steps) | Claude Code · claude-code-action (direct) | Fireworks (Anthropic-compatible endpoint) | dynamic: `${{ steps.fireworks.outputs.model_id }}` | `FIREWORKS_API_KEY` | workflow-level `fireworks_fallback` input (default `claude`) |
| `hourly-rss.yml` | process-rss-feeds-with-glm-5-2-via-fireworks | Claude Code · agent-run | GLM 5.2 via Fireworks | `accounts/fireworks/models/glm-5p2` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`); then `deterministic_rss_digest.py` |
| `hourly-twitter.yml` | tier:claude · process-tweets-with-glm-5-2-via-fireworks-primary-tier | Claude Code · agent-run | GLM 5.2 via Fireworks | `accounts/fireworks/models/glm-5p2` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`) |
| `hourly-twitter.yml` | tier:deepseek-claude-code | Claude Code · agent-run | DeepSeek V4 Flash via Fireworks | `accounts/fireworks/models/deepseek-v4-flash` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`); then `deterministic_twitter_digest.py` |
| `hourly-twitter.yml` | tier:zai-glm-5p2 | Claude Code · agent-run | GLM 5.2 via Z.ai | `glm-5.2` | `ZAI_API_KEY` | hard fail if key unset (no provider fallback); then `deterministic_twitter_digest.py` |
| `hourly-twitter.yml` | tier:deepseek-pi | pi · run-pi-container | fireworks (pi built-in) | `accounts/fireworks/models/deepseek-v4-flash` | `FIREWORKS_API_KEY` | — |
| `hourly-twitter.yml` | tier:fireworks-pi | pi · run-pi-container | fireworks (pi built-in) | `accounts/fireworks/models/kimi-k2p7` | `FIREWORKS_API_KEY` | — |
| `hourly-twitter.yml` | tier:claude · adjudicate-near-duplicate-headlines-with-fireworks-primary | Claude Code · agent-run | DeepSeek V4 Flash via Fireworks | `accounts/fireworks/models/deepseek-v4-flash` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`) |
| `hourly-twitter.yml` | tier:claude · auto-research-topic-selection-primary-fireworks-tier | Claude Code · agent-run | GLM 5.2 via Fireworks | `accounts/fireworks/models/glm-5p2` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`) |
| `research-issue.yml` | run-deep-research-with-mcp | Claude Code · claude-code-action (direct) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| `research-issue.yml` | run-deep-research-without-mcp | Claude Code · claude-code-action (direct) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| `twitter-account-explorer.yml` | explore-and-curate-account-list | Claude Code · claude-code-action (direct) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| `wiki-ingest.yml` | ingest-digest-into-wiki-via-fireworks | Claude Code · agent-run | GLM 5.2 via Fireworks | `accounts/fireworks/models/glm-5p2` | `FIREWORKS_API_KEY` | native Claude (`claude-sonnet-5`) |
| `zai-claude-code-canary.yml` | run-claude-code-file-write-canary-via-z-ai | Claude Code · agent-run | GLM 5.2 via Z.ai | `glm-5.2` | `ZAI_API_KEY` | hard fail if key unset (no provider fallback) |

### Workflows with no model lane (deterministic / infra)

- `arm-timeline.yml`
- `auto-rerun-on-runner-loss.yml`
- `ci.yml`
- `daily-ai-blogs.yml`
- `daily-front-page.yml`
- `daily-youtube.yml`
- `liveness-check.yml`

_28 model lanes across 23 workflows; 7 workflows run no model._

<!-- END GENERATED BACKEND MATRIX -->

## Model calls outside the harness table

Model usage that is real but is not an agent-harness lane, so the generator
does not (and should not) row it:

| Lane | What it is | Provider / model | Auth |
|---|---|---|---|
| `scripts/run_generative_research_oracle.py` | Local Oracle runner on the developer machine (not GitHub Actions) | GPT-5.5 Pro via `../oracle` (browser engine by default) | local Oracle checkout |
| Digest TTS audio (inline step in `daily-digest.yml`) + manual `scripts/generate_generative_article_audio.py` | plain TTS API call, not an agent harness | Gemini Flash TTS | `GEMINI_API_KEY` (skipped when unset) |
| Raw endpoint probe in `zai-claude-code-canary.yml` | 256-token tool-use diagnostics POST straight to `api.z.ai/api/anthropic/v1/messages` before the agent-run canary step | Z.ai `glm-5.2` | `ZAI_API_KEY` |

## Related contracts

- Per-backend env mapping and selector tokens: `CLAUDE.md` → "Backends"
- Generative-research lane deep dive (Oracle, Codex auth, comparisons):
  [`generative-research-backends.md`](generative-research-backends.md)
- Freshness watchdog that alerts when a lane's output goes stale regardless
  of which backend served it: `scripts/check_lane_freshness.py`
