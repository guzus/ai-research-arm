# AGENTS.md

Agents working in this repo: read [`CLAUDE.md`](CLAUDE.md) — it is the
full operating guide (pipeline architecture, workflows, output
locations, authentication, and the load-bearing rules). This file is a
short pointer plus the few genuinely agent-specific notes.

> New to the repo and not operating the live pipeline? Start with
> [`README.md`](README.md) — its Quickstart runs with no accounts, and it
> documents the License and the runnable-vs-not boundary.

## Agent-specific notes

- **Scheduled content workflows** use `.github/actions/agent-run` so the
  provider route is modular and Fireworks-backed lanes can enforce committed
  output. Direct Claude workflows may still use
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

- **Fireworks scheduled lanes** should select `fireworks-deepseek-v4-flash`
  for high-frequency summarization and `fireworks-glm-5p2` for deeper CRUD or
  synthesis work. `agent-run` preflights Fireworks and falls back to native
  Claude by default when Fireworks is unavailable; set `fireworks-fallback:
  none` only when strict provider failure is desired. Set `expected-paths` in
  `agent-run`, or call `.github/actions/require-output` after deterministic
  commit steps, so green no-op runs do not leave the freshness watchdog stale.
  RSS, HN/Reddit community, arXiv, daily-digest, and Bluesky lanes (plus the
  twitter-deepseek comparison tier) have deterministic model-free fallbacks;
  a green run there means committed lane output exists, not necessarily that
  the model provider was healthy. Check the agent/fallback step logs before
  drawing provider conclusions.

- **Z.ai GLM-5.2** is available through `agent-run` as `zai-glm-5p2` using
  `ZAI_API_KEY` and Claude Code's Anthropic-compatible route. Keep it manual
  until quota behavior is measured; `hourly-twitter.yml backend=zai-glm-5p2`
  is the smoke-test lane and writes to `research/twitter-zai/`.

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

- **bird CLI** invocations must always pass `--json --plain` and fall
  back gracefully (`|| echo "[]"`); the X/Twitter cookies expire and a
  workflow must continue with empty data rather than crash.

- Everything else — runner choice, the ARA DSL compile/validate
  contract, model-ticket and wiki CRUD protocols, telemetry, atomic
  writes — is documented in `CLAUDE.md`. Follow that.
