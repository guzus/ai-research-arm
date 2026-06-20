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
