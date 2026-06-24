# AGENTS.md

Agents working in this repo: read [`CLAUDE.md`](CLAUDE.md) — it is the
full operating guide (pipeline architecture, workflows, output
locations, authentication, and the load-bearing rules). This file is a
short pointer plus the few genuinely agent-specific notes.

> New to the repo and not operating the live pipeline? Start with
> [`README.md`](README.md) — its Quickstart runs with no accounts, and it
> documents the License and the runnable-vs-not boundary.

## Agent-specific notes

- **Claude workflows** use `anthropics/claude-code-action@v1`. Pass the
  model via `claude_args`, never as a separate `model:` input:

  ```yaml
  # Correct (v1)
  claude_args: "--model opus"

  # Wrong (do not use a separate model input here)
  model: <versioned-model-name>
  ```

  Reference: https://code.claude.com/docs/en/github-actions
  (action repo: https://github.com/anthropics/claude-code-action)

- **Codex workflows** use `openai/codex-action@v1`. Pass the OpenAI key
  via the action input, never as job-level env:

  ```yaml
  openai-api-key: ${{ secrets.OPENAI_API_KEY }}
  ```

  Do not copy Claude Code inputs such as `claude_args`,
  `claude_code_oauth_token`, or `allowed_bots` into Codex steps; Codex
  uses inputs such as `prompt` / `prompt-file`, `codex-args`, `sandbox`,
  and `allow-bots`.

- **bird CLI** invocations must always pass `--json --plain` and fall
  back gracefully (`|| echo "[]"`); the X/Twitter cookies expire and a
  workflow must continue with empty data rather than crash.

- Everything else — runner choice, the ARA DSL compile/validate
  contract, model-ticket and wiki CRUD protocols, telemetry, atomic
  writes — is documented in `CLAUDE.md`. Follow that.
