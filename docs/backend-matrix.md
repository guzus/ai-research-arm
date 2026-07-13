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
| Claude Code · agent-run | `anthropics/claude-code-action@v1` wrapped by `.github/actions/agent-run`: resolves the lane from the SSOT, selects provider env (Fireworks / Z.ai Anthropic-compatible endpoints, or native), preflights Fireworks with native-Claude fallback, then enforces `expected-paths` / `allowed-paths`. |
| Claude Code · claude-code-action | The action invoked directly. Native Anthropic unless the step's `env` reroutes `ANTHROPIC_BASE_URL` (generative-research does this on its Fireworks paths). |
| pi · run-pi-container | The pi coding-agent harness in a container with pi's own provider config. Twitter comparison tiers only. |
| Codex CLI | `codex exec` with ChatGPT-managed file auth (subscription entitlement, not API billing). |
| dispatch default | Not an agent itself: the SSOT-resolved default backend a dispatch/issue run uses when none is specified. |

## How routing consumption works

Two modes, chosen per harness:

| Mode | Harnesses | Semantics |
|---|---|---|
| **Runtime SSOT** | `agent-run`, `dispatch-default` | The workflow step passes `lane: <key>`; the runner selects the backend from the file via `scripts/select_backend.py`. **Editing the file re-routes the lane with no workflow change.** Every agent-run call site passes all provider secrets (`CLAUDE_CODE_OAUTH_TOKEN`, `FIREWORKS_API_KEY`, `ZAI_API_KEY`) so a flip never needs a workflow edit; an unknown lane fails the run loudly. |
| **CI-enforced mirror** | `pi`, `claude-code-action` | The model/provider stays literal in the workflow step (these workflows either run manual comparisons or don't check out before the agent step); `build_backend_matrix.py --check` fails CI until workflow and file agree. A flip is a two-line PR: edit the file, edit the step. |

Fallback is an ORDERED CHAIN, SSOT-defined: the top-level `fallback.chain`
lists backend selectors tried in order. At run time `scripts/select_backend.py`
walks `[lane's backend] + chain` (deduplicated — a failed primary isn't
retried from the chain), probes each candidate's provider (fireworks =
preflight request, zai = Z.ai endpoint probe, claude = always available),
and runs the first available candidate. Keeping `claude` terminal in the
chain guarantees selection succeeds whenever the OAuth token exists — a
unit test pins this invariant. Lanes marked `"strict": true` (zai-canary)
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
  route. agent-run lanes always carry all three secrets (see above); the
  unused ones are inert.
- **`--model opus` in `claude_args` is an alias**, not a provider model:
  agent-run remaps it to the effective profile's model id (Fireworks/Z.ai)
  or to the SSOT's global `fallback.native_model` on the native path.
- **Fallback** shows the provider-selection chain (already excluding the
  lane's own backend); strict lanes show `hard fail` instead. Editorial lanes
  are expected to fail closed when Claude produces no output. Manual emergency
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
| ai-news-research (×2 step variants) | `ai-news-research.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| arxiv | `daily-arxiv.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted) |
| bluesky | `2h-bluesky.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted) |
| claude-code-review | `claude-code-review.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| claude-interactive | `claude.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| community | `4h-community.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted) |
| daily-improve | `daily-improve.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| digest-audio-script | `daily-digest.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted); then `deterministic_daily_digest.py` |
| digest-synthesis | `daily-digest.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted); then `deterministic_daily_digest.py` |
| digest-synthesis-fallback | `daily-digest.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted); then `deterministic_daily_digest.py` |
| generative-research-claude (+1 retry step) | `generative-research.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| generative-research-default | `generative-research.yml` | dispatch default (runtime SSOT) | (per chosen backend) | default: `claude` | (per chosen backend) | workflow-level `fireworks_fallback` input (default `claude`) |
| model-timeline | `24h-model-timeline.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted) |
| research-issue (×2 step variants) | `research-issue.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| rss | `hourly-rss.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted) |
| twitter-ab-claude · PINNED | `twitter-model-ab.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (strict — never walks the chain) |
| twitter-ab-judge · PINNED | `twitter-model-ab.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (strict — never walks the chain) |
| twitter-ab-judge-swapped · PINNED | `twitter-model-ab.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (strict — never walks the chain) |
| twitter-ab-zai · PINNED | `twitter-model-ab.yml` | Claude Code · agent-run (runtime SSOT) | GLM 5.2 via Z.ai | `glm-5.2` | `ZAI_API_KEY` | hard fail (strict — never walks the chain) |
| twitter-account-explorer | `twitter-account-explorer.yml` | Claude Code · claude-code-action (CI-enforced mirror) | Anthropic (native) | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | — |
| twitter-autoresearch (tier:claude) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted) |
| twitter-deepseek (tier:deepseek-claude-code) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | DeepSeek V4 Flash via Fireworks | `accounts/fireworks/models/deepseek-v4-flash` | `FIREWORKS_API_KEY` | hard fail (strict — never walks the chain) |
| twitter-deepseek-pi (tier:deepseek-pi) | `hourly-twitter.yml` | pi · run-pi-container (CI-enforced mirror) | fireworks (pi built-in) | `accounts/fireworks/models/deepseek-v4-flash` | `FIREWORKS_API_KEY` | — |
| twitter-fireworks-pi (tier:fireworks-pi) | `hourly-twitter.yml` | pi · run-pi-container (CI-enforced mirror) | fireworks (pi built-in) | `accounts/fireworks/models/kimi-k2p7` | `FIREWORKS_API_KEY` | — |
| twitter-judge (tier:claude) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted) |
| twitter-primary (tier:claude) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted); then `deterministic_twitter_digest.py` |
| twitter-primary-repair (tier:claude) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted) |
| twitter-zai (tier:zai-glm-5p2) | `hourly-twitter.yml` | Claude Code · agent-run (runtime SSOT) | GLM 5.2 via Z.ai | `glm-5.2` | `ZAI_API_KEY` | hard fail (strict — never walks the chain) |
| wiki-ingest | `wiki-ingest.yml` | Claude Code · agent-run (runtime SSOT) | Claude | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (chain exhausted) |
| zai-canary · PINNED | `zai-claude-code-canary.yml` | Claude Code · agent-run (runtime SSOT) | GLM 5.2 via Z.ai | `glm-5.2` | `ZAI_API_KEY` | hard fail (strict — never walks the chain) |
| (dispatch path) backend=fireworks (+2 retry steps) | `generative-research.yml` | Claude Code · claude-code-action (env-rerouted) | Fireworks (Anthropic-compatible endpoint) | dynamic: per fireworks profile step | `FIREWORKS_API_KEY` | workflow-level `fireworks_fallback` input (default `claude`) |
| (dispatch path) backend=codex | `generative-research.yml` | Codex CLI | OpenAI (ChatGPT subscription auth) | codex CLI default | `CODEX_AUTH_JSON` | — |
| (dispatch path) backend=fable-5 | `generative-research.yml` | Claude Code · claude-code-action (explicit premium selector) | Anthropic (native) | `claude-fable-5` | `CLAUDE_CODE_OAUTH_TOKEN` | hard fail (no model-action retry) |

### Workflows with no model lane (deterministic / infra)

- `arm-timeline.yml`
- `auto-rerun-on-runner-loss.yml`
- `ci.yml`
- `daily-ai-blogs.yml`
- `daily-front-page.yml`
- `daily-youtube.yml`
- `liveness-check.yml`

_Global ordered fallback chain (SSOT `fallback.chain`): `claude`; native path serves `claude-sonnet-5`. 30 SSOT lanes (+3 dispatch execution paths) across 24 workflows; 7 workflows run no model._

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
