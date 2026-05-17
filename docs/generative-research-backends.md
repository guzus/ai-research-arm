# Generative Research Backends

`generative-research.yml` supports two model backends for the same deep
research pipeline:

| Dispatch value | Served model | Auth path | Notes |
|---|---|---|---|
| `deepseek-v4-pro` | `deepseek-v4-pro` | `DEEPSEEK_API_KEY` via DeepSeek's Anthropic-compatible endpoint | Default for manual and issue-triggered generative research. The workflow still passes `--model opus` to Claude Code because the endpoint remaps the Opus request to DeepSeek V4 Pro through env vars. Subagents use `deepseek-v4-flash`. Retries once if the Anthropic-compatible socket drops before an article commit is produced. |
| `claude` | `claude-opus-4-7` | `CLAUDE_CODE_OAUTH_TOKEN` | Native Anthropic Claude Code path. Kept as the comparison baseline. |

The DeepSeek path mirrors `.github/workflows/hourly-twitter-deepseek-agentic.yml`:

```yaml
ANTHROPIC_BASE_URL: https://api.deepseek.com/anthropic
ANTHROPIC_AUTH_TOKEN: ${{ secrets.DEEPSEEK_API_KEY }}
ANTHROPIC_MODEL: deepseek-v4-pro
ANTHROPIC_DEFAULT_OPUS_MODEL: deepseek-v4-pro
ANTHROPIC_DEFAULT_SONNET_MODEL: deepseek-v4-pro
ANTHROPIC_DEFAULT_HAIKU_MODEL: deepseek-v4-flash
CLAUDE_CODE_SUBAGENT_MODEL: deepseek-v4-flash
```

## Comparing Claude And DeepSeek

Use the same topic and distinct slugs. The topic drives the prompt and
prior-context lookup; the slug only keeps artifacts separate.

```bash
TOPIC="QA comparison: AI infrastructure power bottlenecks in 2026"

gh workflow run generative-research.yml \
  -f topic="$TOPIC" \
  -f slug="qa-deepseek-v4-pro-power-bottlenecks" \
  -f backend=deepseek-v4-pro \
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

- DeepSeek: Anthropic-compatible DeepSeek endpoint, `deepseek-v4-pro`
  metadata in `research/generative/index.json`. This path has a longer
  action timeout because the Anthropic shim plus large sub-agent waves can
  run slower than the native Claude path. The workflow makes the first
  DeepSeek attempt recoverable: if Claude Code returns a transient API/socket
  error before the writer commits a generated HTML file, the job cleans any
  partial repository artifacts and retries once. If `/tmp/gen-research.ara.md`
  survived from the failed attempt, the retry prompt tells the model to
  validate and finish that draft instead of restarting research.
- Claude: native Anthropic endpoint, `claude-opus-4-7` metadata in
  `research/generative/index.json`.

After both runs finish, compare:

```bash
gh run list --workflow=generative-research.yml --limit 10
python3 scripts/check_generative_research.py research/generative/<deepseek>.ara.md
python3 scripts/check_generative_research.py research/generative/<claude>.ara.md
```

Then inspect the workflow "Article quality report" sections for words,
distinct visualization types, callouts, citations, references, and
standalone percentages in prose.
