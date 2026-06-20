# Twitter Account Curation

The production Twitter/X monitor reads accounts and search queries from
`data/sources/twitter_accounts.json`. The scheduled workflow should stay
deterministic: every run validates the manifest, builds a birdy multi-fetch
manifest, and fetches the exact reviewed account set.

Use `scripts/curate_twitter_accounts.py` for account changes:

```bash
uv run python scripts/curate_twitter_accounts.py validate
uv run python scripts/curate_twitter_accounts.py build-fetch-manifest \
  --output /tmp/manifest.json \
  --concurrency 8
```

To review candidates discovered by an agent or by manual research, put them in a
JSON file:

```json
[
  {
    "action": "add",
    "handle": "example_ai",
    "category": "others",
    "score": 4,
    "reason": "Repeatedly surfaced primary AI launch details before search lanes.",
    "evidence": ["https://x.com/example_ai/status/123"]
  },
  {
    "action": "remove",
    "handle": "old_handle",
    "reason": "No AI-relevant posts in recent monitored snapshots.",
    "evidence": ["research/twitter/2026-06-17.md"]
  }
]
```

Generate a reviewable proposal:

```bash
uv run python scripts/curate_twitter_accounts.py propose \
  --candidates /tmp/twitter-account-candidates.json \
  --output /tmp/twitter-account-proposal.md \
  --changes-output /tmp/twitter-account-changes.json
```

After review, apply the approved changes file:

```bash
uv run python scripts/curate_twitter_accounts.py apply \
  --changes /tmp/twitter-account-changes.json
```

The proposal step never mutates production state. The apply step preserves
category order, appends additions to their target category, removes matching
handles case-insensitively, and re-validates before writing.

## Explorer Loop

`.github/workflows/twitter-account-explorer.yml` runs weekly and by manual
dispatch. It is an agent loop, but it is intentionally review-gated:

1. `scripts/explore_twitter_accounts.py` runs broad bird searches and writes
   `/tmp/twitter-account-candidates.json` plus a Markdown evidence report.
   It uses the `goodtweet` lesson that mention-graph traversal is often higher
   signal than keyword search: unknown handles mentioned by multiple
   search-surfaced accounts are scored as candidates too.
2. A Claude explorer reads those candidates, the current manifest, recent
   Twitter outputs, and this curation contract.
3. If no strong evidence exists, it prints `no account changes`.
4. If evidence supports changes, it uses `curate_twitter_accounts.py propose`
   and `apply`, validates the manifest, runs focused tests, then opens a PR
   against `main`.

The loop caps each run at five additions and two removals. Removals require
clear observed evidence because losing a quiet but important source is costlier
than adding a marginal candidate.
