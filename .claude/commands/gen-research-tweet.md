---
description: Route a Twitter/X status URL to the generative-research GitHub workflow and expand it into a full article.
argument-hint: <twitter-or-x-status-url>
---

# Generative Research From Twitter/X

Twitter/X seed URL: **$ARGUMENTS**

If the argument is empty or just whitespace, ask the user for the
Twitter/X status URL and stop until they answer.

Validate that the argument starts with `https://x.com/` or
`https://twitter.com/` and contains `/status/`. If it does not, ask
for a direct status URL and stop.

## What this does

Dispatches `generative-research.yml` with only `twitter_url`. The
workflow reads the tweet and thread with the authenticated bird CLI,
infers the underlying research question, expands outward to primary
sources, writes the article through `scripts/write_generative_research.py`,
and pushes the result to `main`.

Default backend is `claude` unless the user explicitly asks for
`deepseek-v4-flash`.

## Steps

1. Verify `gh` auth:

   ```bash
   gh auth status >/dev/null
   ```

2. Dispatch the workflow:

   ```bash
   gh workflow run generative-research.yml \
     -f twitter_url="$ARGUMENTS" \
     -f backend=claude
   ```

3. Wait for the run to register, then fetch the run metadata:

   ```bash
   sleep 5
   gh run list --workflow=generative-research.yml --limit 1 \
     --json databaseId,status,url,createdAt,event \
     --jq '.[0]'
   ```

   If the latest run is older than 60s or its `event` is not
   `workflow_dispatch`, sleep 3s and retry once.

## Report Back

Return one short message with:

- "Dispatched Twitter-seeded generative research."
- The run URL.
- `gh run watch <id>`.
- Expected runtime: ~20-45 min.
- Destination: `research/generative/`; the runner pushes the commit
  and the article appears at `https://ara.guzus.xyz/research/<slug>`
  after Vercel deploys.

Do not write the article locally in this session.
