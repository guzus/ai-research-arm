---
description: Route a generative-research topic to the GitHub workflow (self-hosted runner, ~20-45 min). Thin pointer to the gen-research-dispatch skill.
argument-hint: <topic> [backend=<selector>]
---

# Generative Research — Route to GitHub Workflow

Input: **$ARGUMENTS**

Use the `gen-research-dispatch` skill with this input in topic mode. It owns the dispatch contract: it reads backends from `data/agent-backends.json`, omits `-f backend` unless the input names one, dispatches `generative-research.yml`, and reports the run.

If that skill is not available, dispatch directly and report the run URL:

```bash
gh workflow run generative-research.yml -f topic='<the exact topic>'
```

Add `-f backend=<selector>` only when the input names a selector that `data/agent-backends.json` lists. Do not write the article locally in this session; for in-chat research, use `/gen-research`.
