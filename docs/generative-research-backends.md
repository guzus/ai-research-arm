# Generative Research Backends

`generative-research.yml` supports two model backends for the same deep
research pipeline:

| Dispatch value | Served model | Auth path | Notes |
|---|---|---|---|
| `claude` | `claude-opus-4-7` | `CLAUDE_CODE_OAUTH_TOKEN` | Default for manual and issue-triggered generative research. Native Anthropic Claude Code path. |
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
language switch will show Korean only after that file and index update have
been pushed and deployed.

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

The DeepSeek path mirrors the `deepseek-claude-code` backend in
`.github/workflows/hourly-twitter.yml` — both route through Fireworks'
Anthropic-compatible endpoint (the direct DeepSeek API is retired):

```yaml
ANTHROPIC_BASE_URL: https://api.fireworks.ai/inference
ANTHROPIC_AUTH_TOKEN: ${{ secrets.FIREWORKS_API_KEY }}
ANTHROPIC_MODEL: accounts/fireworks/models/deepseek-v4-flash
ANTHROPIC_DEFAULT_OPUS_MODEL: accounts/fireworks/models/deepseek-v4-flash
ANTHROPIC_DEFAULT_SONNET_MODEL: accounts/fireworks/models/deepseek-v4-flash
ANTHROPIC_DEFAULT_HAIKU_MODEL: accounts/fireworks/models/deepseek-v4-flash
CLAUDE_CODE_SUBAGENT_MODEL: accounts/fireworks/models/deepseek-v4-flash
```

## Comparing Claude And DeepSeek

Use the same topic and distinct slugs. The topic drives the prompt and
prior-context lookup; the slug only keeps artifacts separate.

```bash
TOPIC="QA comparison: AI infrastructure power bottlenecks in 2026"

gh workflow run generative-research.yml \
  -f topic="$TOPIC" \
  -f slug="qa-deepseek-v4-flash-power-bottlenecks" \
  -f backend=deepseek-v4-flash \
  -f tags="qa,comparison,deepseek"

gh workflow run generative-research.yml \
  -f topic="$TOPIC" \
  -f slug="qa-claude-power-bottlenecks" \
  -f backend=claude \
  -f tags="qa,comparison,claude"
```

Both runs execute the same writer contract, ARA DSL validation,
design gates, quality report, commit writer, and push/rebase logic.
The expected difference is the model backend:

- DeepSeek (via Fireworks): Anthropic-compatible Fireworks endpoint, `deepseek-v4-flash`
  metadata in `research/generative/index.json`. This path has a longer
  action timeout because the Anthropic shim plus large sub-agent waves can
  run slower than the native Claude path. The workflow makes the first
  DeepSeek attempt recoverable: if Claude Code returns a transient API/socket
  error before the writer commits a generated HTML file, the job cleans any
  partial repository artifacts and retries up to two times. Draft recovery is
  limited to the workflow's run-scoped `$GEN_DRAFT` path, so a self-hosted
  runner cannot reuse stale `/tmp/gen-research*.ara.md` content from another
  backend or run.
- Claude: native Anthropic endpoint, `claude-opus-4-7` metadata in
  `research/generative/index.json`.

After both runs finish, compare:

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
