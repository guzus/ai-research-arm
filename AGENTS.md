# AGENTS.md

Agents working in this repo: read [`CLAUDE.md`](CLAUDE.md) — it is the
full operating guide (pipeline architecture, workflows, output
locations, authentication, and the load-bearing rules). This file is a
short pointer plus the few genuinely agent-specific notes.

> New to the repo and not operating the live pipeline? Start with
> [`README.md`](README.md) — its Quickstart runs with no accounts, and it
> documents the License and the runnable-vs-not boundary.

## Agent-specific notes

- **Claude-harness scheduled workflows** use `.github/actions/agent-run` so
  their provider route is modular and committed output is enforced centrally.
  The strict OpenCode exception is RSS, community, arXiv, Bluesky, and wiki:
  those five use `.github/actions/run-opencode-container`, share
  `OPENCODE_API_KEY` plus the Go-plan caps ($12/5h, $30/week, $60/month), and
  never fall back—one key/cap failure can stale all five together. Direct
  Claude workflows may still use
  `anthropics/claude-code-action@v1`; when they do, pass the model via
  `claude_args`, never as a separate `model:` input:

  ```yaml
  # Correct (v1)
  claude_args: "--model claude-sonnet-5"

  # Wrong (do not use a separate model input here)
  model: <versioned-model-name>
  ```

  Reference: https://code.claude.com/docs/en/github-actions
  (action repo: https://github.com/anthropics/claude-code-action)

- **GLM-5.2 is the preferred fallback for Claude-harness content lanes.** RSS,
  community, arXiv, Bluesky, and wiki are deliberate exceptions: they run the
  containerized OpenCode CLI pinned to `opencode-go/deepseek-v4-flash`, with
  `OPENCODE_API_KEY` as their single strict provider credential. `agent-run`
  probes the requested provider and walks the ordered `fallback.chain` from
  `data/agent-backends.json` when it is unavailable (currently Z.ai GLM →
  native Claude); lanes marked `"strict": true` and `fireworks-fallback:
  none` runs never fall back. Set `expected-paths` in `agent-run`, or call
  `.github/actions/require-output` after deterministic commit steps, so green
  no-op runs do not leave the freshness watchdog stale. RSS, HN/Reddit
  community, arXiv, Bluesky, and wiki fail closed; only daily-digest has a
  deterministic publishing fallback. Check the agent/fallback step logs before
  drawing provider conclusions.

- **Backend routing SSOT: `data/agent-backends.json`.** Every model lane,
  the backend profile table, and the ordered `fallback.chain` are defined
  there. agent-run lanes select at runtime via `scripts/select_backend.py`
  (workflow steps pass `lane:` and all provider secrets — editing the file
  re-routes or re-orders fallbacks with no workflow change; on provider
  outage the chain is walked in order and the first available candidate
  runs); pi, opencode, and direct claude-code-action lanes are CI-enforced mirrors;
  strict lanes (zai-canary) never fall back. After any routing change run
  `uv run python scripts/build_backend_matrix.py` to regenerate
  `docs/backend-matrix.md` (CI runs `--check` and fails on drift, missing
  secrets, orphan lanes, or mirror divergence).

- **Z.ai GLM-5.2** is available through `agent-run` as `zai-glm-5p2` using
  `ZAI_API_KEY` and Claude Code's Anthropic-compatible route. It is the
  preferred manual `hourly-twitter.yml` backend and writes to
  `research/twitter-zai/`; use `zai-claude-code-canary.yml` for focused
  provider diagnostics.

- **Codex generative-research workflows** use the Codex CLI with
  ChatGPT-managed file auth, not OpenAI API billing. Seed the workflow
  from `CODEX_AUTH_JSON`, whose value is the file-backed
  `~/.codex/auth.json` produced by `codex login`:

  ```bash
  codex login
  jq '{auth_mode, has_refresh_token: ((.tokens.refresh_token // "") != "")}' ~/.codex/auth.json
  ```

  Treat `auth.json` like a password. Do not commit it, print it, or share
  one copy across concurrent jobs. Do not switch this lane to
  `openai-api-key` unless the intent is API billing instead of the
  ChatGPT/Codex subscription.

- **OpenCode + DeepSeek V4 Flash runs** use the opencode CLI
  (pinned `opencode-ai@1.18.3`) driving `deepseek-v4-flash` with plain env-var
  auth — a single secret is the whole login; there is no `opencode auth
  login` step and no auth-file seeding. The workflow resolves the route
  exclusively through `OPENCODE_API_KEY` (OpenCode Go subscription — sign in
  at https://opencode.ai/auth, subscribe, copy the key). The Go plan caps are
  $12/5h, $30/week, and $60/month; because RSS, community, arXiv, Bluesky, and
  wiki share this one strict route, exhaustion can stale all five together.
  Moonshot is not a DeepSeek provider and is not a fallback. Store the key with
  `gh secret set OPENCODE_API_KEY`, then validate cheaply with
  `opencode-kimi-canary.yml` before dispatching
  `generative-research.yml backend=opencode-kimi-k3`.

- **bird CLI** invocations must always pass `--json --plain` and fall
  back gracefully (`|| echo "[]"`); the X/Twitter cookies expire and a
  workflow must continue with empty data rather than crash.

- Everything else — runner choice, the ARA DSL compile/validate
  contract, model-ticket and wiki CRUD protocols, telemetry, atomic
  writes — is documented in `CLAUDE.md`. Follow that.
