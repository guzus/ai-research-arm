---
description: Route a Twitter/X status URL to the generative-research GitHub workflow and expand it into a full article.
argument-hint: <twitter-or-x-status-url>
---

# Generative Research From Twitter/X

Input: **$ARGUMENTS**

Reason from first principles before dispatching: the user is not asking
for a tweet summary. They are asking the GitHub Action to use the tweet
as a seed, infer the real research question, verify the claims against
primary sources, and publish a full generative-research article.

If the argument is empty, ask for a direct Twitter/X status URL. If it
does not start with `https://x.com/` or `https://twitter.com/`, or does
not contain `/status/`, ask for a direct status URL.

Run:

```bash
gh auth status >/dev/null
gh workflow run generative-research.yml \
  -f twitter_url="$ARGUMENTS" \
  -f backend=claude
sleep 5
gh run list --workflow=generative-research.yml --limit 1 \
  --json databaseId,status,url,createdAt,event \
  --jq '.[0]'
```

Use `backend=deepseek-v4-pro` only when the user explicitly asks for
DeepSeek.

Report the run URL, `gh run watch <id>`, expected runtime (~20-45 min),
and destination (`research/generative/`). Do not write the article
locally.
