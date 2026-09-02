# Backend Matrix — harness × token provider per lane

**The routing SSOT is [`data/agent-backends.json`](../data/agent-backends.json).**
Every model lane in the pipeline is defined there — one entry per lane with
its workflow, harness, backend/model, and notes. This doc is the generated,
human-readable projection of that file; the per-*backend* contracts (env
slots, endpoints, selector tokens) live in `CLAUDE.md` → "Backends" and
`docs/generative-research-backends.md`.

## Harness vocabulary

| Harness | What it means |
|---|---|
| Claude Code · agent-run | `anthropics/claude-code-action@v1` wrapped by `.github/actions/agent-run`: resolves the lane from the SSOT, probes the requested provider, walks either the global chain or a lane-local compatibility override, and enforces `expected-paths` / `allowed-paths`. Explicit isolated OpenCode/Cursor candidates run in their container action; only the selected child receives its credential. |
| Claude Code · claude-code-action | The action invoked directly. Native Anthropic unless the step's `env` reroutes `ANTHROPIC_BASE_URL` (generative-research does this on its Fireworks paths). |
| pi · run-pi-container | The pi coding-agent harness in a container with pi's own provider config. Twitter comparison tiers only. |
| Codex CLI | `codex exec` with ChatGPT-managed file auth (subscription entitlement, not API billing). |
| opencode CLI | `opencode run` **inside a Docker container** (`.github/actions/run-opencode-container`: `--cap-drop ALL`, `no-new-privileges`, non-root, throwaway HOME, disposable clone). The registered editorial profile is temporarily off production routes while the monthly plan is exhausted; its independent canary is the reversion signal. |
| Cursor CLI | `agent -p` **inside a Docker container** (`.github/actions/run-cursor-container`: same isolation contract as OpenCode). Authenticated by `CURSOR_API_KEY`; model selected by `agent --model` (canonical `cursor-grok-4.6-high-fast`). Cursor temporarily serves both strict editorial routes and four named lane-local fallback contracts; it is never on the global chain. Missing Docker is a hard failure. Validate with `cursor-cli-canary.yml`. |
| dispatch default | Not an agent itself: the SSOT-resolved default backend a dispatch/issue run uses when none is specified. |

## How routing consumption works

Two modes, chosen per harness:

| Mode | Harnesses | Semantics |
|---|---|---|
| **Runtime SSOT** | `agent-dispatch`, `agent-run`, `dispatch-default` | Dispatched lanes resolve lane → route → backend profile → registered adapter. **Editing one route backend re-routes every lane sharing it without workflow edits**, provided the adapter registry declares the isolation/editorial capabilities and the dispatcher implements it. Current host-checkout agent-run is rejected. Callers prewire known credentials, but only the selected child receives its key. |
| **CI-enforced mirror** | `pi`, direct `opencode`, direct `cursor`, `claude-code-action` | Direct comparison/model pins remain literal; `build_backend_matrix.py --check` fails CI until workflow and file agree. |

Fallback is an ORDERED CHAIN, SSOT-defined: the top-level `fallback.chain`
lists backend selectors tried in order. At run time `scripts/select_backend.py`
walks `[lane's backend] + chain` (deduplicated — a failed primary isn't
retried from the chain), probes each candidate's provider (fireworks =
preflight request, zai = Z.ai endpoint probe, claude = OAuth preflight),
and runs the first available candidate. Claude 401/403 auth rejection or
HTTP 429 rate limiting advances ordinary non-strict callers to Z.ai; the
local digest, primary Twitter/repair, and no-MCP AI-news lanes explicitly
override that chain with isolated Cursor because their inputs and exact commit
contracts are adapter-compatible. Each lane declares `fallback_mode`; CI
checks `twitter` for the staged Twitter snapshot and `editorial` elsewhere.
A lane override replaces the global chain, so Cursor failure never silently
continues into Z.ai. MCP AI-news remains direct native Claude because Cursor
denies MCP tools. HTTP 400, 5xx, and network faults
retain the narrow fail-open behavior. Lanes marked
`"strict": true` (zai-canary)
and runs with `fireworks-fallback: none` never walk the chain: requested
backend or hard fail. The `backends` profile table (selector → provider /
model / aliases) also lives in the SSOT file — the action has no routing
knowledge of its own left.

To re-route a lane:

```bash
# 1. Edit data/agent-backends.json (runtime lanes: done; mirror lanes: also update the workflow step)
# 2. Regenerate this doc — CI fails otherwise:
uv run python scripts/build_backend_matrix.py
# 3. Sanity-check the whole contract:
uv run python scripts/build_backend_matrix.py --check
```

Reading notes:

- **Token secret** is the secret that pays for tokens on the lane's current
  route. agent-run callers preserve the standard provider-key plumbing and
  add isolated-adapter keys only where the lane contract permits them; only
  the selected child receives its credential.
- **`--model opus` in `claude_args` is an alias**, not a provider model:
  agent-run remaps it to the effective profile's model id (Fireworks/Z.ai)
  or to the SSOT's global `fallback.native_model` on the native path.
- **Fallback** shows the provider-selection chain (already excluding the
  lane's own backend); strict lanes show `hard fail` instead. Editorial lanes
  are expected to fail closed when their configured agent produces no output. Manual emergency
  workflow-dispatch fallbacks are not shown as scheduled/default behavior.
- `hourly-twitter.yml` tier names are dispatch/cron *slots*, not routing:
  the tier named `claude` hosts three lanes (`twitter-primary`,
  `twitter-judge`, `twitter-autoresearch`) whose backends come from the
  file. `(dispatch path)` rows are execution paths of
  `generative-research-default`, not independent routing decisions.

<!-- BEGIN GENERATED BACKEND MATRIX (scripts/build_backend_matrix.py — do not edit by hand) -->

### Lanes

| Lane | Workflow | Harness | Provider | Model | Token secret | Fallback |
|---|---|---|---|---|---|---|
| ai-news-research | `ai-news-research.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` (workflow `native-model` override) | `CLAUDE_CODE_OAUTH_TOKEN` | chain: `cursor-grok-4p6-fast` |
| ai-news-research-mcp | `ai-news-research.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| arxiv (route:research-editorial-secondary) | `daily-arxiv.yml` | agent-dispatch → Cursor CLI (runtime SSOT) | Grok 4.6 Fast via Cursor CLI | `cursor-grok-4.6-high-fast` | `CURSOR_API_KEY` | hard fail (route fallback=none) |
| bluesky (route:research-editorial) | `2h-bluesky.yml` | agent-dispatch → Cursor CLI (runtime SSOT) | Grok 4.6 Fast via Cursor CLI | `cursor-grok-4.6-high-fast` | `CURSOR_API_KEY` | hard fail (route fallback=none) |
| claude-code-review | `claude-code-review.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| claude-interactive | `claude.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| community (route:research-editorial) | `4h-community.yml` | agent-dispatch → Cursor CLI (runtime SSOT) | Grok 4.6 Fast via Cursor CLI | `cursor-grok-4.6-high-fast` | `CURSOR_API_KEY` | hard fail (route fallback=none) |
| daily-improve | `daily-improve.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| digest-audio-script | `daily-digest.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-opus-5` | `CLAUDE_CODE_OAUTH_TOKEN` | chain: `zai-glm-5p2`; then `deterministic_daily_digest.py` |
| digest-synthesis | `daily-digest.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-opus-5` | `CLAUDE_CODE_OAUTH_TOKEN` | chain: `zai-glm-5p2`; then `deterministic_daily_digest.py` |
| digest-synthesis-fallback | `daily-digest.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-opus-5` | `CLAUDE_CODE_OAUTH_TOKEN` | chain: `cursor-grok-4p6-fast`; then `deterministic_daily_digest.py` |
| generative-research-claude (+1 retry step) | `generative-research.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| generative-research-default | `generative-research.yml` | dispatch default (runtime SSOT) | (per chosen backend) | default: `claude-opus-5` | (per chosen backend) | workflow-level `fireworks_fallback` input (default `claude`) |
| generative-research-ko (route:generative-translation) | `translate-generative-research.yml` | agent-dispatch → Cursor CLI (runtime SSOT) | Grok 4.6 Fast via Cursor CLI | `cursor-grok-4.6-high-fast` | `CURSOR_API_KEY` | hard fail (route fallback=none) |
| model-timeline | `24h-model-timeline.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-opus-5` | `CLAUDE_CODE_OAUTH_TOKEN` | chain: `zai-glm-5p2` |
| research-issue (×2 step variants) | `research-issue.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| rss (route:research-editorial) | `hourly-rss.yml` | agent-dispatch → Cursor CLI (runtime SSOT) | Grok 4.6 Fast via Cursor CLI | `cursor-grok-4.6-high-fast` | `CURSOR_API_KEY` | hard fail (route fallback=none) |
| twitter-ab-claude · PINNED | `twitter-model-ab.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-opus-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (strict — never walks the chain) |
| twitter-ab-judge · PINNED | `twitter-model-ab.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-opus-4-8` (workflow `native-model` override) | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (strict — never walks the chain) |
| twitter-ab-judge-swapped · PINNED | `twitter-model-ab.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-opus-4-8` (workflow `native-model` override) | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (strict — never walks the chain) |
| twitter-ab-zai · PINNED | `twitter-model-ab.yml` | Claude Code · agent-run (runtime SSOT) | GLM 5.2 via Z.ai | `glm-5.2` | `ZAI_API_KEY` | hard fail (strict — never walks the chain) |
| twitter-account-explorer | `twitter-account-explorer.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| twitter-autoresearch (tier:claude) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-opus-5` | `CLAUDE_CODE_OAUTH_TOKEN` | chain: `zai-glm-5p2` |
| twitter-deepseek (tier:deepseek-claude-code) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | DeepSeek V4 Flash via Fireworks | `accounts/fireworks/models/deepseek-v4-flash` | `FIREWORKS_API_KEY` | hard fail (strict — never walks the chain) |
| twitter-deepseek-pi (tier:deepseek-pi) | `hourly-twitter.yml` | pi · run-pi-container (CI-enforced mirror) | fireworks (pi built-in) | `accounts/fireworks/models/deepseek-v4-flash` | `FIREWORKS_API_KEY` | — |
| twitter-fireworks-pi (tier:fireworks-pi) | `hourly-twitter.yml` | pi · run-pi-container (CI-enforced mirror) | fireworks (pi built-in) | `accounts/fireworks/models/kimi-k2p7` | `FIREWORKS_API_KEY` | — |
| twitter-judge (tier:claude) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-opus-5` | `CLAUDE_CODE_OAUTH_TOKEN` | chain: `zai-glm-5p2` |
| twitter-primary (tier:claude) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-opus-5` | `CLAUDE_CODE_OAUTH_TOKEN` | chain: `cursor-grok-4p6-fast`; then `deterministic_twitter_digest.py` |
| twitter-primary-repair (tier:claude) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-opus-5` | `CLAUDE_CODE_OAUTH_TOKEN` | chain: `cursor-grok-4p6-fast` |
| twitter-zai (tier:zai-glm-5p2) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | GLM 5.2 via Z.ai | `glm-5.2` | `ZAI_API_KEY` | hard fail (strict — never walks the chain) |
| wiki-ingest (route:research-editorial-secondary) | `wiki-ingest.yml` | agent-dispatch → Cursor CLI (runtime SSOT) | Grok 4.6 Fast via Cursor CLI | `cursor-grok-4.6-high-fast` | `CURSOR_API_KEY` | hard fail (route fallback=none) |
| zai-canary · PINNED | `zai-claude-code-canary.yml` | Claude Code · agent-run (runtime SSOT) | GLM 5.2 via Z.ai | `glm-5.2` | `ZAI_API_KEY` | hard fail (strict — never walks the chain) |
| (canary) cursor + cursor-grok-4.6-high-fast | `cursor-cli-canary.yml` | Cursor CLI (containerised) | Cursor CLI | `cursor-grok-4.6-high-fast` | `CURSOR_API_KEY` | hard fail (diagnostics lane) |
| (dispatch path) backend=fireworks (+2 retry steps) | `generative-research.yml` | Claude Code · claude-code-action (env-rerouted) | Fireworks (Anthropic-compatible endpoint) | dynamic: per fireworks profile step | `FIREWORKS_API_KEY` | workflow-level `fireworks_fallback` input (default `claude`) |
| (dispatch path) backend=codex | `generative-research.yml` | Codex CLI | OpenAI (ChatGPT subscription auth) | codex CLI default | `CODEX_AUTH_JSON` | — |
| (dispatch path) backend=opencode-deepseek-v4-flash | `generative-research.yml` | opencode CLI (containerised) | OpenCode Go | `deepseek-v4-flash` | `OPENCODE_API_KEY` | hard fail (strict comparison backend) |
| (dispatch path) backend=fable-5 | `generative-research.yml` | Claude Code · claude-code-action (explicit premium selector) | Anthropic (native) | `claude-fable-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (no model-action retry) |
| (dispatch path) backend=opus-5 | `generative-research.yml` | Claude Code · claude-code-action (explicit model selector) | Anthropic (native) | `claude-opus-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (one recovery retry, same as `claude`) |
| (dispatch path) backend=cursor-grok-4p6-fast | `generative-research.yml` | Cursor CLI (containerised) | Cursor CLI | `cursor-grok-4.6-high-fast` | `CURSOR_API_KEY` | hard fail (strict comparison backend) |
| (tier) backend=opencode-deepseek-v4-flash | `hourly-twitter.yml` | opencode CLI (containerised) | OpenCode Go | `deepseek-v4-flash` | `OPENCODE_API_KEY` | hard fail (strict comparison tier) |
| (tier) backend=cursor-grok-4p6-fast | `hourly-twitter.yml` | Cursor CLI (containerised) | Cursor CLI | `cursor-grok-4.6-high-fast` | `CURSOR_API_KEY` | hard fail (strict comparison tier) |
| (canary) opencode + deepseek-v4-flash | `opencode-deepseek-canary.yml` | opencode CLI (containerised) | OpenCode Go | `deepseek-v4-flash` | `OPENCODE_API_KEY` | hard fail (diagnostics lane) |

### Workflows with no model lane (deterministic / infra)

- `arm-timeline.yml`
- `auto-rerun-on-runner-loss.yml`
- `blog-subscriptions.yml`
- `ci.yml`
- `cleanup-fallback-publications.yml`
- `daily-ai-blogs.yml`
- `daily-earnings.yml`
- `daily-front-page.yml`
- `daily-youtube.yml`
- `gpu-spot.yml`
- `liveness-check.yml`
- `market-quotes.yml`
- `model-pricing.yml`
- `production-synthetic.yml`

_Global ordered fallback chain (SSOT `fallback.chain`): `claude` → `zai-glm-5p2`; native path serves `claude-opus-5`. 32 SSOT lanes (+10 dispatch execution paths) across 34 workflows; 14 workflows run no model._

_Explicit lane fallback overrides (replace, never extend, the global chain): `ai-news-research`: `cursor-grok-4p6-fast`; `digest-synthesis-fallback`: `cursor-grok-4p6-fast`; `twitter-primary`: `cursor-grok-4p6-fast`; `twitter-primary-repair`: `cursor-grok-4p6-fast`._

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
