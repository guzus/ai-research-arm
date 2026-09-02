# AGENTS.md

Agents working in this repo: read [`CLAUDE.md`](CLAUDE.md) — it is the
full operating guide (pipeline architecture, workflows, output
locations, authentication, and the load-bearing rules). This file is a
short pointer plus the few genuinely agent-specific notes.

> New to the repo and not operating the live pipeline? Start with
> [`README.md`](README.md) — its Quickstart runs with no accounts, and it
> documents the License and the runnable-vs-not boundary.

## Agent-specific notes

- **Scheduled model workflows** use the Claude-harness `.github/actions/agent-run`
  directly or, for RSS, community, arXiv, Bluesky, and wiki, the trusted
  `.github/actions/agent-dispatch`. RSS/community/Bluesky reference
  `research-editorial`; arXiv/wiki reference `research-editorial-secondary`.
  Both temporarily select the registered Cursor CLI adapter
  (`cursor-grok-4p6-fast`, Grok 4.6 Fast) because the OpenCode Go monthly plan
  is exhausted. Host-checkout `agent-run` is deliberately
  capability-incompatible and rejected. This emergency convergence restores
  the three actively failing lanes but temporarily expands one Cursor failure
  domain across all five editorial lanes. Direct
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

- **GLM-5.2 is the default fallback for ordinary Claude-harness lanes.** The
  editorial dispatcher temporarily serves both strict routes with Cursor Grok
  4.6 Fast while the OpenCode Go monthly plan is exhausted. Known
  credential slots are prewired for a future isolated adapter, but the current
  host-checkout `agent-run` profiles cannot be selected by this route. `agent-run`
  probes the requested provider and walks the ordered `fallback.chain` from
  `data/agent-backends.json` when it is unavailable (currently native Claude →
  Z.ai GLM). Compatibility-tested local digest synthesis/audio, primary
  Twitter/repair, and no-MCP AI-news lanes are explicit exceptions: their
  lane-local chains replace the currently unusable global secondary with
  isolated Cursor. Claude remains
  primary and currently healthy; these Cursor paths are standby fallbacks.
  The MCP AI-news path stays direct native Claude because Cursor denies MCP.
  Lanes marked `"strict": true` and `fireworks-fallback:
  none` runs never fall back. Set `expected-paths` in `agent-run`, or call
  `.github/actions/require-output` after deterministic commit steps, so green
  no-op runs do not leave the freshness watchdog stale. RSS, HN/Reddit
  community, arXiv, Bluesky, and wiki fail closed; only daily-digest has a
  deterministic publishing fallback. Check the agent/fallback step logs before
  drawing provider conclusions.

- **Backend routing SSOT: `data/agent-backends.json`.** Every model lane,
  the backend profile table, and the ordered `fallback.chain` are defined
  there. Runtime-dispatched lanes resolve lane → route → backend profile;
  `.github/actions/agent-dispatch` selects the registered adapter while
  `agent-run` lanes select at runtime via `scripts/select_backend.py`
  (workflow steps pass `lane:` and all provider secrets — editing the file
  re-routes or re-orders fallbacks with no workflow change; on provider
  outage the chain is walked in order and the first available candidate
  runs); pi, opencode, and direct claude-code-action lanes are CI-enforced mirrors;
  strict lanes (zai-canary) never fall back. After any routing change run
  `uv run python scripts/build_backend_matrix.py` to regenerate
  `docs/backend-matrix.md` (CI runs `--check` and fails on drift, missing
  secrets, orphan lanes, or mirror divergence).
  To switch one failure domain, edit its route backend to a pre-registered
  compatible backend, then run the generator. To move one lane, change only its `route`
  reference (define the new route/profile first when needed).

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

- **OpenCode Go runs** use the opencode CLI (pinned `opencode-ai@1.18.3`)
  with plain env-var auth. The registered editorial profile uses
  `glm-5.3-flash`; explicit generative-research, Twitter comparison, and canary
  paths remain pinned to `deepseek-v4-flash`. A single secret is the whole login;
  there is no `opencode auth login` step and no auth-file seeding. The workflow
  resolves the route exclusively through `OPENCODE_API_KEY` (OpenCode Go subscription — sign in
  at https://opencode.ai/auth, subscribe, copy the key). The Go plan caps are
  $12/5h, $30/week, and $60/month. It is temporarily absent from production
  routing because the monthly cap is exhausted. Revert only after
  `opencode-deepseek-canary.yml`'s registered editorial GLM probe succeeds:
  point only `routes.research-editorial.backend` back to
  `opencode-glm-5p3-flash`, regenerate the matrix, and redispatch
  RSS/community/Bluesky.
  Moonshot is not a provider for either pinned model and is not a fallback.
  Store the key with `gh secret set OPENCODE_API_KEY`; the retained
  `opencode-deepseek-canary.yml` validates both the explicit DeepSeek path and
  the registered editorial GLM profile before dispatching
  `generative-research.yml backend=opencode-deepseek-v4-flash`.

- **Cursor CLI + Grok 4.6 Fast** is an isolated editorial adapter
  (`run-cursor-container`, official `agent` binary, `CURSOR_API_KEY`).
  It is selectable via SSOT / `generative-research.yml
  backend=cursor-grok-4p6-fast` / `hourly-twitter.yml
  backend=cursor-grok-4p6-fast` and temporarily serves both production
  editorial routes plus lane-local standby fallbacks for compatible local
  digest synthesis/audio, Twitter, and no-MCP AI-news contracts. It is never
  in the global chain.
  Store the key with `gh secret set CURSOR_API_KEY`, then validate
  cheaply with `cursor-cli-canary.yml`. Korean translation currently
  selects this profile via `routes.generative-translation`.

- **bird CLI** invocations must always pass `--json --plain` and fall
  back gracefully (`|| echo "[]"`); the X/Twitter cookies expire and a
  workflow must continue with empty data rather than crash.

- Everything else — runner choice, the ARA DSL compile/validate
  contract, model-ticket and wiki CRUD protocols, telemetry, atomic
  writes — is documented in `CLAUDE.md`. Follow that.
