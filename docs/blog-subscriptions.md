# Blog Subscriptions

`blog-subscriptions.yml` turns explicitly subscribed entries in
`data/sources/ai_blogs.json` into Hooker notifications. It currently watches
the Naver blog `tosoha1` every two hours and publishes to the existing
`ara-research` topic.

## Configuration contract

A normal AI-blog registry entry becomes a subscription when it has:

```json
"subscription": {
  "hooker_topic": "ara-research",
  "priority": 3
}
```

`hooker_topic` must match Hooker's exact `^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$`
contract. `priority` is an integer from 0 through 5. `HOOKER_URL` and
`HOOKER_TOKEN` are required; the workflow hard-fails before polling when
either secret is absent.

The Naver feed does not return `ETag` or `Last-Modified`, and its channel-level
`pubDate` changes on every request. Neither can represent post identity. The
watcher therefore deduplicates on each item's `<guid>`; URL-shaped GUIDs are
canonicalized to remove tracking parameters. If a feed omits `<guid>`, the
canonical post link is the fallback identity. Channel metadata is never used.
Both GUID URLs and post links must stay on the source's configured host/path,
so an upstream feed cannot turn the Hooker button into an arbitrary URL.

## State and delivery contract

Committed state lives at
`research/summaries/blog-subscriptions.json`:

```json
{
  "version": 1,
  "sources": {
    "tosoha1": {
      "seen_guids": ["https://blog.naver.com/tosoha1/224346445662"],
      "updated_at": "2026-07-15T12:00:00Z"
    }
  }
}
```

- A source absent from state is seeded with every normalized item identity
  currently in its feed.
  That first poll sends no notifications, so adding a 50-item feed does not
  flood Hooker with history.
- Existing malformed state is a hard failure. It is never silently reset,
  because resetting would either replay history or lose delivery knowledge.
- Unseen posts are sent oldest first. Each request uses a stable
  `blog-subscription-<source>-<guid-hash>` Hooker idempotency key.
- A GUID is added to state immediately after Hooker accepts that item. If a
  later item fails, the workflow still commits and pushes the accepted subset,
  then reports a failed job; only unaccepted GUIDs retry.
- State commits must land on `main` (`safe-push` output `pushed=true`). A
  delivery whose state push fails is safe to retry because its idempotency key
  is derived from the normalized item identity.
- A poll with no seed and no accepted posts creates no commit or push.

The state file is written atomically. Workflow concurrency never cancels an
in-progress run, and the runner-loss watchdog covers this workflow. Hooker
workflow telemetry remains non-blocking, but subscription delivery itself is
fail-closed. Manual dispatch is also guarded to `main` before polling or
delivery; a feature-ref run cannot send a notification that safe-push would
later refuse to persist.

## Local verification

```bash
python3 -m unittest scripts.test_watch_blog_subscriptions
python3 scripts/watch_blog_subscriptions.py poll \
  --state /tmp/blog-subscriptions-state.json \
  --pending /tmp/blog-subscriptions-pending.json
```

The local poll command only fetches and writes local files. Hooker delivery is
performed by the workflow, not by the Python script.
