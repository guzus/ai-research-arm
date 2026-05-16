---
description: Route a generative-research topic to the GitHub Actions workflow (deep pipeline, ~20-45 min on the self-hosted runner)
argument-hint: <topic>
---

# Generative Research — Route to GitHub Workflow

User-supplied topic: **$ARGUMENTS**

If the topic is empty or just whitespace, ask the user for a topic
and stop until they answer.

## What this does

Dispatches the `generative-research.yml` GitHub Actions workflow
with `backend=claude` (Claude Opus 4.7 via OAuth). The workflow
runs on the self-hosted Linux runner and executes the full deep
pipeline documented in the workflow file:

- 16–32 evidence-collection sub-agents (waves of ≤8)
- 5–10 section-writer sub-agents (waves of ≤4)
- Verifier sub-agent + bounded revision pass
- Quality targets: ≥90% claims cited, ≥50% primary sources,
  ≥12 cites per 1000 words, ≥20 references, 4500–7000 words

Article writes to `research/generative/` via the canonical writer
and the runner pushes the commit directly to `main`. Your local
chat is freed immediately.

Runtime is typically 20–45 min depending on topic complexity.

## Steps

1. **Verify gh auth** (one-liner; if this errors, stop and ask the
   user to fix their gh auth before continuing):

   ```bash
   gh auth status >/dev/null
   ```

2. **Dispatch the workflow.** Quote the topic so spaces and
   special characters survive the shell:

   ```bash
   gh workflow run generative-research.yml \
     -f topic="$ARGUMENTS" \
     -f backend=claude
   ```

   If the user passed a brief in their topic that mentions
   `backend: deepseek`, honor it by switching `-f backend=deepseek`
   instead. Otherwise default to `claude`.

3. **Wait a few seconds for the run to register, then look it up.**
   GitHub takes a moment to enqueue dispatched runs:

   ```bash
   sleep 5
   gh run list --workflow=generative-research.yml --limit 1 \
     --json databaseId,status,url,createdAt,event \
     --jq '.[0]'
   ```

   If the most recent run is older than 60s or its `event` isn't
   `workflow_dispatch`, sleep another 3s and retry once — the
   dispatch hasn't shown up yet.

## Report back to the user

A short message containing:

- "Dispatched to GitHub workflow."
- The run URL (clickable in the terminal).
- The command to watch live progress: `gh run watch <id>`.
- Expected runtime (~20–45 min) and where the article will land
  (`research/generative/<timestamp>--<slug>.html`).
- A reminder that the runner will push the commit automatically.

Do NOT write the article locally in this session — the workflow
is the writer.
