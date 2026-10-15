---
description: Expand a Twitter/X status URL into a full generative-research article via the GitHub workflow. Thin pointer to the gen-research-dispatch skill.
argument-hint: <twitter-or-x-status-url> [framing]
---

# Generative Research From Twitter/X

Input: **$ARGUMENTS**

Use the `gen-research-dispatch` skill with this input in tweet mode. It owns the dispatch contract: it validates and normalizes the status URL, passes any extra text as framing, reads backends from `data/agent-backends.json`, omits `-f backend` unless the input names one, and reports the run.

If that skill is not available, dispatch directly and report the run URL:

```bash
gh workflow run generative-research.yml -f twitter_url='<x.com status URL>'
```

Add `-f backend=<selector>` only when the input names a selector that `data/agent-backends.json` lists. Do not write the article locally in this session.
