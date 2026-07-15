# Blog Subscriptions

`blog-subscriptions.yml` turns explicitly subscribed entries in
`data/sources/ai_blogs.json` into direct Telegram notifications. It currently
watches the Naver blog `tosoha1` every two hours. Hooker remains the lane's
non-blocking workflow telemetry sink, not its delivery-success gate.

## Configuration contract

A normal AI-blog registry entry becomes a subscription when it has:

```json
"subscription": {
  "delivery": "telegram"
}
```

`delivery` must currently be `telegram`. `TELEGRAM_BOT_TOKEN` and
`TELEGRAM_CHAT_ID` are required; the workflow hard-fails before polling when
either secret is absent.

The Naver feed does not return `ETag` or `Last-Modified`, and its channel-level
`pubDate` changes on every request. Neither can represent post identity. The
watcher therefore deduplicates on each item's `<guid>`; URL-shaped GUIDs are
canonicalized to remove tracking parameters. If a feed omits `<guid>`, the
canonical post link is the fallback identity. Channel metadata is never used.
Both GUID URLs and post links must stay on the source's configured host/path,
so an upstream feed cannot turn the Telegram button into an arbitrary URL.

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

- The repository includes the observed 50-item `tosoha1` baseline so a post
  published between merge and the first scheduled run is still detected.
  Independently, a source absent from state is seeded with every normalized
  item identity currently in its feed. That bootstrap poll sends no
  notifications, so a newly configured historical feed does not flood the
  destination.
- Existing malformed state is a hard failure. It is never silently reset,
  because resetting would either replay history or lose delivery knowledge.
- Unseen posts are sent oldest first through Telegram `sendMessage`.
- A response proves delivery only when the HTTP request succeeds and its JSON
  has `ok=true`, a positive `result.message_id`, and the configured
  `result.chat.id`. A generic HTTP 2xx response is insufficient.
- A GUID is added to state immediately after that proof. If a later item
  fails, the workflow still commits and pushes the accepted subset, then
  reports a failed job; only unaccepted GUIDs retry.
- There is deliberately no blind transport retry. If Telegram accepted a
  message but its response was lost, the GUID remains unseen and a later run
  may duplicate the alert. A visible duplicate is preferable to silently
  losing a subscribed post.
- Each Telegram request has a three-second connect timeout and an eight-second
  total timeout. This keeps a stalled item inside the delivery loop's failure
  path so earlier successful acknowledgements can still be persisted before
  the ten-minute job deadline.
- State commits must land on `main` (`safe-push` output `pushed=true`).
- A poll with no seed and no accepted posts creates no commit or push.

Hooker topic publish is intentionally not used for subscription delivery:
Hooker stores an idempotency key before route delivery, so a failed delivery
can later return an idempotency hit with HTTP 200 and `delivered=0`. That does
not prove delivery and cannot safely advance this ledger.

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

The local poll command only fetches and writes local files. Telegram delivery is
performed by the workflow, not by the Python script.
