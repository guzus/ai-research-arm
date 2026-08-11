# Generative Research Backends

> Repo-wide per-workflow harness/provider/token mapping (all lanes, not
> just generative research): [`backend-matrix.md`](backend-matrix.md).

`generative-research.yml` supports these model backends for the same deep
research pipeline:

| Dispatch value | Served model | Auth path | Notes |
|---|---|---|---|
| `glm-5p2` | `GLM 5.2` via Fireworks | `FIREWORKS_API_KEY` via Fireworks' Anthropic-compatible endpoint | Opt-in Fireworks route (was the default before `claude`, which was in turn replaced by `opus-5` on 2026-07-31). Routes through `accounts/fireworks/models/glm-5p2` and records `glm-5p2` in article metadata. Uses the same retry, quality-gate, verifier, methodology-artifact, and safe-push path as `deepseek-v4-flash`. |
| `claude` | `claude-sonnet-5` | `CLAUDE_CODE_OAUTH_TOKEN` | Explicit native Anthropic Claude Code path and default fallback when a Fireworks backend is unavailable. The workflow pins `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-sonnet-5`, so the Claude Code `opus` alias resolves to Sonnet 5 for this lane. |
| `fable-5` | `claude-fable-5` | `CLAUDE_CODE_OAUTH_TOKEN` | Explicit premium native Anthropic path for deliberate one-off runs. It is never the default or a fallback target, and it gets one model-action attempt rather than Claude's automatic recovery retry. The workflow passes the literal model ID to Claude Code and resolves every alias/subagent pin plus article metadata from `claude-fable-5`, preventing a Fable-labeled article from silently running on Sonnet. |
| `opus-5` | `claude-opus-5` | `CLAUDE_CODE_OAUTH_TOKEN` | **The default** (SSOT lane `generative-research-default`, since 2026-07-31) — inherited by manual dispatch with no `backend` input, `gen-research`-labelled issues, and `hourly-twitter.yml`'s throttled auto-research dispatch. Native Anthropic on Opus 5 (released 2026-07-24). It is still **not** the Fireworks-unavailable fallback target: that stays `claude`, because a fallback should be the cheap reliable path. Because it bills against the same OAuth subscription as `claude`, it keeps Claude's single automatic recovery retry — the retry costs no more than the first attempt would have. Like `fable-5`, the workflow pins the literal model ID across every alias/subagent slot and article metadata, and additionally verifies the committed `index.json` row records `claude-opus-5` before pushing (mismatch = hard rollback). Selectors: `opus-5`, `opus5`, `claude-opus-5`. |
| `codex` | Codex CLI default model for ChatGPT auth | `CODEX_AUTH_JSON` seeded into file-backed `auth.json` | Optional Codex backend using ChatGPT-managed Codex auth rather than OpenAI API billing. Codex reads the same staged input files, writes the same methodology artifacts, and publishes through the same writer contract; article metadata records `codex`. |
| `opencode-kimi-k3` | **TEMPORARY 2026-08-07:** `deepseek-v4-flash` (1M context, the 2026-07-31 build) via the opencode CLI — was `kimi-k3`; swapped to spare Claude Max quota | `OPENCODE_API_KEY` (OpenCode Go subscription), read directly from env by opencode's built-in `opencode-go` provider. `MOONSHOT_API_KEY` is NO LONGER a route — Moonshot serves Kimi only, so a Moonshot-only environment hard-fails at preflight rather than authoring with the wrong model | Optional comparison backend on a third harness (opencode, pinned `opencode-ai@1.18.3`). No interactive login and no auth-file seeding — the env var IS the auth. Strict: preflight failure fails the run (no Claude fallback). Same staged inputs, methodology artifacts, and writer contract; article metadata records `deepseek-v4-flash`. Validate the secret first with `opencode-kimi-canary.yml`. |
| `deepseek-v4-flash` | `deepseek-v4-flash` via Fireworks | `FIREWORKS_API_KEY` via Fireworks' Anthropic-compatible endpoint | Optional comparison backend. Routes through Fireworks (`accounts/fireworks/models/deepseek-v4-flash`); the direct DeepSeek API is retired (billing/credits). The `--model opus` passed to Claude Code is ignored — `ANTHROPIC_MODEL` env governs the served model. All model slots (incl. subagents) use the Fireworks model id. Retries up to two times if the Anthropic-compatible socket drops before an article commit is produced. |

## Local Oracle / GPT-5.5 Pro

Use the local Oracle checkout when you want the generative-research lane to run
from this machine instead of GitHub Actions:

```bash
uv run python scripts/run_generative_research_oracle.py \
  "The Home Inference Rack: can a Mac mini plus consumer GPU fleet beat cloud APIs?" \
  --slug home-inference-rack \
  --tags "local-ai,home-inference,hardware,mac-mini,gpu-fleet"
```

Defaults:

- Oracle checkout: `../oracle`
- Model: `gpt-5.5-pro`
- Engine: `browser`
- Thinking: `heavy`
- Source metadata: `local-oracle`

The script bundles ARA DSL docs, the rendered component reference, prior local
generative-research context, and the latest digest/model/arXiv/community/Twitter
research files. Oracle writes a draft `.ara.md`; the script extracts the marked
article source, runs:

```bash
uv run python scripts/check_generative_research.py "$DRAFT" \
  --diversity-min 3 --callout-max 5 --strict-shape
```

Then it publishes through `scripts/write_generative_research.py`, so the
dashboard artifact, `research/generative/index.json`, DSL source file, and git
commit follow the same contract as GitHub Actions.

## Korean Backfills

Korean generative-research articles are stored as translations of an existing
English article row, not as separate research-index entries. Generate or edit
the Korean `.ara.md`, run the normal checker, then publish it against the
existing slug:

```bash
uv run python scripts/write_generative_research.py \
  --topic "Korean translation of <title>" \
  --translation-of "<existing-slug>" \
  --language ko \
  --model "<model>" \
  --html-body "$KOREAN_DRAFT"
```

The writer emits `research/generative/<timestamp>--<slug>.ko.html` and stores
it under `translations.ko` in `research/generative/index.json`. The dashboard
runtime can load that variant; its visible language control is currently a
separate UI rollout, so this workflow establishes the publishing contract
without claiming the translation is already discoverable in the interface.

For model-assisted backfills, dispatch **Korean Generative Research Backfill**
from the default branch with one existing `slug`. The workflow resolves the
canonical `.ara.md` source (falling back to legacy HTML), sends only that
public article to the dedicated isolated `generative-translation` route, and
imports one uncommitted Korean draft. Trusted host steps then enforce URL,
citation, numeric, and component-topology parity before calling the writer.

```bash
gh workflow run translate-generative-research.yml \
  -f slug="<existing-slug>" \
  -f overwrite=false \
  -f auto_merge=false
```

`overwrite=false` refuses an existing `translations.ko` pointer before model
spend. `overwrite=true` publishes a new immutable artifact revision without
deleting the prior files. Publication opens a review PR by default;
`auto_merge=true` opts into the normal protected-branch squash-merge path.
The lane deliberately disables `safe-push`'s append-oriented index merge:
translation mutates an existing slug, so an index conflict fails for a clean
rerun rather than risking a dropped nested translation.

## Article Audio

Generative-research articles can carry an `audio_file` field in
`research/generative/index.json`. The dashboard renders that file as the
article's native audio player and keeps browser read-aloud as a fallback.

Generate audio for the latest article locally:

```bash
GEMINI_API_KEY=... python3 scripts/generate_generative_article_audio.py --force
```

Generate audio for a specific article:

```bash
GEMINI_API_KEY=... python3 scripts/generate_generative_article_audio.py \
  --slug servicenow-stock \
  --force
```

The default is `gemini-2.5-flash-preview-tts` with the `Charon` voice and
64 kbps mono MP3 output. That model is the default because Google's pricing
page positions it as the price-performant TTS model: paid tier input is
$0.50 per 1M text tokens and output is $10.00 per 1M audio tokens. The
script allows `--model` and `--voice` overrides for deliberate higher-cost
experiments, but the default should be the production path unless an article
needs special treatment.

Local generation can also use Vertex AI through the active `gcloud` account:

```bash
python3 scripts/generate_generative_article_audio.py \
  --api vertex \
  --vertex-project <project-id> \
  --slug servicenow-stock \
  --force
```

The Vertex path defaults to the stable `gemini-2.5-flash-tts` model name and
uses `gcloud auth print-access-token`. The Developer API path keeps the
preview model name because that is the public Gemini API model code.

The `generative-research.yml` workflow runs the same script after article
quality gates pass when `GEMINI_API_KEY` is configured. The script extracts
readable article text, skips tables/references, chunks long reports for TTS
reliability, concatenates Gemini's 24 kHz mono PCM, writes
`research/audio/<article-stem>.mp3`, and updates the article row's
`audio_file`.

If the local Oracle checkout is not installed yet:

```bash
pnpm -C ../oracle install
```

Preview the bundle without sending it to a model:

```bash
uv run python scripts/run_generative_research_oracle.py "Topic" --oracle-dry-run
```

## Codex Via ChatGPT Auth

The Codex path runs `codex exec` in GitHub Actions with a file-backed
ChatGPT-managed `auth.json`. It does not use `OPENAI_API_KEY`, so usage follows
the ChatGPT/Codex subscription entitlement attached to the account that created
the auth cache.

Dispatch with:

```bash
gh workflow run generative-research.yml \
  --ref main \
  -f topic="$TOPIC" \
  -f slug="qa-codex-power-bottlenecks" \
  -f backend=codex \
  -f tags="qa,comparison,codex"
```

Use `--ref <branch>` for a PR-branch smoke test. The generated article and
index update publish back to that same branch; only runs dispatched from `main`
publish to `main`. Dispatching from tags is rejected because the workflow
writes commits and needs a branch target.

Seed `CODEX_AUTH_JSON` once from a trusted machine:

```bash
codex login
AUTH_FILE="${CODEX_HOME:-$HOME/.codex}/auth.json"
jq '{
  auth_mode,
  has_refresh_token: ((.tokens.refresh_token // "") != ""),
  last_refresh
}' "$AUTH_FILE"
gh secret set CODEX_AUTH_JSON < "$AUTH_FILE"
```

Continue only if `auth_mode` is `chatgpt` and `has_refresh_token` is `true`.
Treat this file like a password: do not commit it, print it in logs, paste it
into tickets, or reuse one copy across concurrent jobs.

The workflow seeds `auth.json` only when missing:

```yaml
CODEX_HOME="${CODEX_HOME:-$HOME/.codex-ara}"
if [ ! -s "$CODEX_HOME/auth.json" ]; then
  printf '%s' "$CODEX_AUTH_JSON" > "$CODEX_HOME/auth.json"
fi
codex --search -a never exec --ephemeral --sandbox danger-full-access \
  -C "$GITHUB_WORKSPACE" < .github/codex/prompts/generative-research.md
```

That seed-if-missing behavior matters on persistent self-hosted runners: Codex
can refresh the session during normal `codex exec` runs and write the refreshed
tokens back to `auth.json`. Overwriting the file from the original secret on
every run would discard those refreshed tokens. On ephemeral runners, reseed
`CODEX_AUTH_JSON` whenever the cached session can no longer refresh.

The Codex prompt follows the same data boundary as the Claude path: user
topic/prompt/tags live in `.gen-input/*.txt`; workflow-owned metadata is in env;
and Codex subprocesses receive only the allowlisted env vars needed by the repo
tools. The writer script owns the commit.

## OpenCode + DeepSeek V4 Flash

> **TEMPORARY (2026-08-07).** This backend ran **Kimi K3**
> (`opencode-go/kimi-k3`, with a `moonshotai/kimi-k3` pay-per-token second
> route). It is pinned to `opencode-go/deepseek-v4-flash` to take load off
> the Claude Max subscription quota. The selector token
> (`backend=opencode-kimi-k3`), the Twitter output dir
> (`research/twitter-opencode-kimi/`) and the canary filename keep their
> historical Kimi names so the swap stays a small, reversible diff — but
> every *model-identifying* label (article `--model` metadata, dashboard
> lane label, digest title suffix, commit prefix, Telegram title) names
> DeepSeek, because a strict no-fallback lane must never ship an artifact
> attributed to a model that did not write it. **The Moonshot route is
> gone, not repointed** — Moonshot serves Kimi only.

### Reverting this swap

This is the canonical checklist; the `REVERT` comments in the workflows point
here. Files 1–6 are required for a working Kimi lane, 7 for correct history,
8–9 for accurate docs. **Nothing in `scripts/` needs editing**: both
`build_backend_matrix.py` and `test_backend_matrix.py` derive the model from
the workflows, so a consistent revert regenerates and passes on its own — and
an *inconsistent* one red-lights CI, which is the point.

| # | File | What to restore |
|---|---|---|
| 1 | `.github/opencode/opencode.json` | `"model": "opencode-go/kimi-k3"`. Keep the key set minimal — opencode **rejects unknown top-level keys** (`Unrecognized key: $comment`), which breaks config injection for the whole lane. Put notes in the workflows, never here. |
| 2 | `.github/opencode/opencode-canary.json` | Nothing required (it declares both models and has no `model` key). |
| 3 | `.github/opencode/prompts/generative-research.md` | `--model kimi-k3` at **both** writer call sites (slug and no-slug). |
| 4 | `.github/workflows/generative-research.yml` | The Go model id; the raw preflight probe body (`"model":"kimi-k3"`); the `moonshotai/kimi-k3` preflight branch replacing the hard-fail; **and `MOONSHOT_API_KEY` back into the agent step's `env:`** — the preflight can resolve a Moonshot route the agent step then has no credential for. |
| 5 | `.github/workflows/hourly-twitter.yml` | The Go model id; the `moonshotai/kimi-k3` `elif` branch (deleted, not edited — reconstruct it); `MOONSHOT_API_KEY` back into the step `env:`; and the four labels `TITLE_SUFFIX` / `COMMIT_PREFIX` / `HARNESS_LABEL` / the Telegram title. |
| 6 | `.github/workflows/opencode-kimi-canary.yml` | The Go model id; the probe payload; the Moonshot route branch; `MOONSHOT_API_KEY` in the harness step `env:`; the workflow `name:` (`OpenCode Canary` → `OpenCode Kimi Canary`). Several `go_route` else-branches are dead while the swap is active and come back to life here. |
| 7 | `dashboard/src/main.ts` | Move the era bound in `TWITTER_AB_LANE_META_HISTORY['twitter-opencode-kimi']`: add a `{ before: '<revert date>' , … DeepSeek … }` entry and restore the Kimi entry as current. Reports keep the label of whatever actually wrote them. |
| 8 | `docs/generative-research-backends.md`, `docs/backend-matrix.md` (hand-written harness table only) | This section and the harness row. Then run `uv run python scripts/build_backend_matrix.py` to regenerate the generated blocks + README diagram. |
| 9 | `CLAUDE.md`, `README.md` | The backend row and the secrets rows. |

The `opencode-kimi-k3` backend runs the [opencode CLI](https://opencode.ai)
(github.com/anomalyco/opencode) against DeepSeek V4 Flash on the **OpenCode
Go** subscription. The 07-31 build is what `opencode-go/deepseek-v4-flash`
resolves to — on this provider the bare id **is** the 2026-07-31 release
(`release_date` per models.dev). Only Fireworks needs the explicit
`deepseek-v4-flash-0731` suffix, because there the bare id still points at
the older 2026-04-24 build. 1M-token context, tool calling, and **$0.07/Mtok
input ($0.0014 cache-read) / $0.14/Mtok output** on the Go route — roughly
40x cheaper on input than the K3 it replaces, which is most of the point.

**One auth route while the DeepSeek pin is active.** It is a plain env-var
API key — opencode documents environment variables as a full substitute for
interactive `opencode auth login` / `/connect` (which write
`~/.local/share/opencode/auth.json`); nothing is seeded to disk in CI. Do
not wire a key through a custom `provider.*.options.apiKey: "{env:...}"`
block — that substitution path is broken upstream
(anomalyco/opencode#19946); the built-in providers' native env pickup is
the supported path.

**OpenCode Go** — `OPENCODE_API_KEY`, provider `opencode-go`, model
`opencode-go/deepseek-v4-flash` (models.dev pins
`env = ["OPENCODE_API_KEY"]`, `api = https://opencode.ai/zen/go/v1`).
Go is opencode's $10/month plan ($5 first month). Usage is dollar-value
capped — **$12/5h, $30/week, $60/month** — but at Flash pricing a deep
research run is a small fraction of the weekly allowance, unlike K3 which
billed at its full $3/$15 rate ("Kimi K3 (2x usage)"). The console's "Use
balance" toggle lets Go fall back to Zen pay-as-you-go credits instead of
blocking when a cap is hit.

If `MOONSHOT_API_KEY` is set and `OPENCODE_API_KEY` is not, the preflight
**fails loudly** instead of routing to Moonshot: Moonshot cannot serve
DeepSeek, and silently authoring with Kimi under DeepSeek labels is the
exact failure this lane's strictness exists to prevent.

Seed the secret once:

```bash
# OpenCode Go: sign in at https://opencode.ai/auth, subscribe to Go,
# copy the API key from the console.
gh secret set OPENCODE_API_KEY
```

Then prove the key + harness before spending a 90-minute research run:

```bash
gh workflow run opencode-kimi-canary.yml
```

The canary resolves the same Go route as the production lane, then
runs two probes: a stdlib-only raw API check (a models listing plus one
tiny `deepseek-v4-flash` completion against the endpoint), followed by a
tool-denied headless `opencode run` using the exact production argv. On
the Go route the raw probe is **auth-fatal only** — 401/402 (bad key /
billing) fail the run, while any other status merely warns: the raw
`/zen/go/v1` surface is undocumented, and Cloudflare's bot filter in
front of opencode.ai answers 403 `error code: 1010` to client
signatures it dislikes (observed live), so a Go 403 is ambiguous. The
probes send an honest custom User-Agent to clear the common
python/curl signature ban, and the opencode harness stage — the exact
SDK client the gateway expects — is the authoritative check.

Dispatch a research run:

```bash
gh workflow run generative-research.yml \
  --ref main \
  -f topic="$TOPIC" \
  -f slug="qa-deepseek-v4-flash-power-bottlenecks" \
  -f backend=opencode-kimi-k3 \
  -f tags="qa,comparison,deepseek-v4-flash"
```

Lane mechanics, mirroring the Codex path:

- Version pinned: `npm install -g opencode-ai@1.18.3` (verified to resolve
  `opencode-go/deepseek-v4-flash`; Moonshot's opencode guide required the
  same >= 1.18.3 floor for kimi-k3) with `OPENCODE_DISABLE_AUTOUPDATE=1`
  so the persistent self-hosted runner cannot drift.
- Config at [`.github/opencode/opencode.json`](../.github/opencode/opencode.json)
  (injected via `OPENCODE_CONFIG`): grants headless
  `edit`/`bash`/`webfetch` permissions and declares `deepseek-v4-flash`
  under `provider.opencode-go.models` so model resolution survives a stale
  models.dev registry cache on the runner; the route-resolved `-m` flag
  picks the model at run time. The run also
  passes `--auto` so a headless session can never hang on a permission ask.
- Prompt at [`.github/opencode/prompts/generative-research.md`](../.github/opencode/prompts/generative-research.md):
  same data boundary (untrusted inputs in `.gen-input/*.txt`), same
  methodology artifacts, same validation gates, and the writer owns the
  commit with `--model deepseek-v4-flash` metadata.
- The workflow preflights the resolved route's API (missing secrets or a
  definitively dead key — HTTP 401/402 — fails in seconds, before
  install/agent) and fails closed — an explicit `opencode-kimi-k3`
  request never falls back to Claude, matching the comparison-lane
  strictness of `fireworks_fallback=none`. Other statuses from the
  undocumented Go raw endpoint (including Cloudflare bot-filter 403s)
  only warn; the opencode run itself is the authoritative check on that
  route.
- opencode has no Claude-style server WebSearch; the prompt steers research
  through `scripts/research_search.py`, `scripts/source_cache.py`,
  `curl`/`pdftotext`, `bird`, and opencode's webfetch tool.
- Security tradeoff vs. Codex: opencode has no
  `shell_environment_policy.include_only` equivalent, so agent subshells
  inherit the whole step env, including `OPENCODE_API_KEY`. Containment is
  the prompt's env-exfil prohibitions, Actions log masking, and the key being
  scoped to model billing only. Because that env is agent-readable, the step
  carries the minimum set: `MOONSHOT_API_KEY` is **not** passed to the agent
  step at all (it cannot serve the pinned DeepSeek model, so injecting it
  would widen the blast radius for nothing). It survives only in the
  preflight step, which runs no agent, purely to emit a precise error when it
  is the only key configured. `scripts/test_backend_matrix.py` asserts that
  scoping.

**No-new-harness alternative (not wired up):** Moonshot also runs an
official Anthropic-compatible endpoint that works with the existing Claude
Code harness pattern — `ANTHROPIC_BASE_URL=https://api.moonshot.ai/anthropic`,
`ANTHROPIC_AUTH_TOKEN=$MOONSHOT_API_KEY`, model `kimi-k3[1m]` (the `[1m]`
alias is endpoint-valid here, unlike Z.ai's rejection of `glm-5.2[1m]`).
If a Kimi lane is ever wanted without the opencode harness, that is the
Z.ai-style route to take.

## Fireworks Backends

The Fireworks paths route through Fireworks' Anthropic-compatible endpoint
(the direct DeepSeek API is retired). `generative-research.yml` resolves the
model id from the dispatch backend:

```yaml
ANTHROPIC_BASE_URL: https://api.fireworks.ai/inference
ANTHROPIC_API_KEY: ${{ secrets.FIREWORKS_API_KEY }}
ANTHROPIC_AUTH_TOKEN: ${{ secrets.FIREWORKS_API_KEY }}
ANTHROPIC_MODEL: accounts/fireworks/models/deepseek-v4-flash
ANTHROPIC_DEFAULT_OPUS_MODEL: accounts/fireworks/models/deepseek-v4-flash
ANTHROPIC_DEFAULT_SONNET_MODEL: accounts/fireworks/models/deepseek-v4-flash
ANTHROPIC_DEFAULT_HAIKU_MODEL: accounts/fireworks/models/deepseek-v4-flash
CLAUDE_CODE_SUBAGENT_MODEL: accounts/fireworks/models/deepseek-v4-flash
```

For GLM 5.2, the same env slots are set to
`accounts/fireworks/models/glm-5p2`.

The Fireworks Anthropic-compatible endpoint does not support Claude server
tools such as WebSearch/WebFetch. The Fireworks workflow path therefore
keeps research on local tools: `scripts/research_search.py`,
`scripts/source_cache.py`, `curl`, `pdftotext`, `bird`, `Glob`, and `Grep`.
For targeted debugging, dispatch with `debug_full_output=true` to expose the
Fireworks Claude Code transcript in the Actions log. Keep it off for routine
runs because full tool output can include fetched page bodies and draft text.

The Fireworks path preflights the selected model with a one-token
Anthropic-compatible request before Claude Code starts. Provider/account errors
that retries cannot fix (`400`, `401`, `402`, `403`, `404`, `412` — e.g. an
account suspension) no longer kill the run: by default the workflow resolves
the EFFECTIVE backend to native Claude and the normal Claude lane runs,
mirroring `.github/actions/agent-run`. Dispatch with `fireworks_fallback=none`
to restore the strict behavior (fail instead of substituting Claude) for
backend-comparison runs. Fallback runs are honest about provenance: a
`::warning` annotation records the reroute, the hooker telemetry payload
carries `backend` (effective) + `requested_backend` + `used_fallback`, and the
published article records `model claude-opus-4-8` with tags
`fireworks-fallback,requested-<backend>` in `research/generative/index.json` —
a fallback article never masquerades as a Fireworks one. Transient statuses
such as a lone `429` still proceed to the existing Fireworks retry path. The
retry gate also reads the Claude Code execution transcript and prints short
API-error annotations when the transcript includes provider status fields,
which is most useful during `debug_full_output=true` runs.

## Comparing Backends

Use the same topic and distinct slugs. The topic drives the prompt and
prior-context lookup; the slug only keeps artifacts separate. For the
Fireworks lanes, pass `fireworks_fallback=none` so an unavailable Fireworks
account fails the run instead of silently substituting a Claude article into
the comparison set (the default, `claude`, favors flow over strictness).

```bash
TOPIC="QA comparison: AI infrastructure power bottlenecks in 2026"

gh workflow run generative-research.yml \
  -f topic="$TOPIC" \
  -f slug="qa-deepseek-v4-flash-power-bottlenecks" \
  -f backend=deepseek-v4-flash \
  -f fireworks_fallback=none \
  -f tags="qa,comparison,deepseek"

gh workflow run generative-research.yml \
  -f topic="$TOPIC" \
  -f slug="qa-glm-5p2-power-bottlenecks" \
  -f backend=glm-5p2 \
  -f fireworks_fallback=none \
  -f tags="qa,comparison,glm-5p2"

gh workflow run generative-research.yml \
  -f topic="$TOPIC" \
  -f slug="qa-codex-power-bottlenecks" \
  -f backend=codex \
  -f tags="qa,comparison,codex"

gh workflow run generative-research.yml \
  -f topic="$TOPIC" \
  -f slug="qa-deepseek-v4-flash-power-bottlenecks" \
  -f backend=opencode-kimi-k3 \
  -f tags="qa,comparison,deepseek-v4-flash"

gh workflow run generative-research.yml \
  -f topic="$TOPIC" \
  -f slug="qa-claude-power-bottlenecks" \
  -f backend=claude \
  -f tags="qa,comparison,claude"

gh workflow run generative-research.yml \
  -f topic="$TOPIC" \
  -f slug="qa-fable-5-power-bottlenecks" \
  -f backend=fable-5 \
  -f tags="qa,comparison,fable-5"

gh workflow run generative-research.yml \
  -f topic="$TOPIC" \
  -f slug="qa-opus-5-power-bottlenecks" \
  -f backend=opus-5 \
  -f tags="qa,comparison,opus-5"
```

Each run executes the same writer contract, ARA DSL validation,
design gates, quality report, commit writer, and push/rebase logic.
The expected difference is the model backend:

- Codex: Codex CLI with ChatGPT-managed `CODEX_AUTH_JSON`, `codex` metadata
  in `research/generative/index.json`, and the prompt file at
  `.github/codex/prompts/generative-research.md`.
- Fireworks (`deepseek-v4-flash` or `glm-5p2`): Anthropic-compatible
  Fireworks endpoint, backend-specific metadata in
  `research/generative/index.json`. This path has a longer action timeout
  because the Anthropic shim plus large sub-agent waves can run slower than
  the native Claude path. It intentionally does not expose Claude server
  WebSearch/WebFetch tools, which Fireworks does not support; use the local
  repo search/fetch scripts in the prompt instead. The workflow makes the
  first Fireworks attempt recoverable: if Claude Code returns a transient
  API/socket error before the writer commits a generated HTML file, the job
  cleans any partial repository artifacts and retries up to two times.
  Draft recovery is limited to the
  workflow's run-scoped `$GEN_DRAFT` path, so a self-hosted runner cannot
  reuse stale `/tmp/gen-research*.ara.md` content from another backend or run.
- Claude: native Anthropic endpoint, `claude-sonnet-5` metadata in
  `research/generative/index.json`.
- Fable 5: native Anthropic endpoint, `claude-fable-5` metadata in
  `research/generative/index.json`. This opt-in selector does not change the
  normal `claude` or default routes, and it does not enter the Claude
  model-action retry path.
- Opus 5: native Anthropic endpoint, `claude-opus-5` metadata in
  `research/generative/index.json`. This is what a no-`backend` dispatch
  resolves to, and it DOES use the Claude recovery retry (same subscription
  billing as `claude`). Both explicit-model selectors share one provenance gate: the
  committed index row must match the resolved model or the run rolls back
  before the push.

After the runs finish, compare:

```bash
gh run list --workflow=generative-research.yml --limit 10
uv run python scripts/check_generative_research.py research/generative/<deepseek>.ara.md
uv run python scripts/check_generative_research.py research/generative/<claude>.ara.md
```

Then inspect the workflow "Article quality report" sections for words,
distinct visualization types, callouts, citations, references, and
standalone percentages in prose.

## Hooker Telemetry

Every generative-research run publishes a non-blocking summary to Hooker topic
`ara-telemetry` through `https://hooker.guzus.xyz` when
`HOOKER_TOKEN` is configured in GitHub Actions. The message includes run status,
backend, slug, output file, dashboard/GitHub links, model attempt outcomes, and
the same final article quality metrics printed in the workflow log. Hooker stores
the full structured telemetry object in the raw message payload so the topic can
be streamed or queried while iterating on model prompts and workflow behavior.
