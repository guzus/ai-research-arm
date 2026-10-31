# Hooker Telemetry

ARA workflow telemetry is published to Hooker topic `ara-telemetry`.

Route:

- Hooker URL: `https://hooker.guzus.xyz`
- Topic: `ara-telemetry`
- Telegram chat: `-1003805075491`
- Telegram thread: `75713`

All GitHub Actions workflows include a final non-blocking telemetry step using
the local composite action at `.github/actions/hooker-telemetry`. Telegram route
delivery receives only a compact summary: status, workflow, job, and run link.
The full structured request is stored by Hooker in Postgres
`messages.payload` JSONB, including event, ref, SHA, actor, run metadata, and
the exact summary text sent to the route.

Each event carries an `Idempotency-Key`, and Hooker drops a repeat of a key it
already stored for the topic (14 days by default). The action's default key is
per run, job and status, so every run posts. A caller may pass
`idempotency-key` to collapse repeats: `aradio.yml` keys a run that failed
without publishing on the failing stage, the cursor's last publication and the
UTC date, so an outage that fails every hour alerts once a day
(`scripts/aradio_run_alert.py`). Keep some rollover in any stable key: Hooker
records the key before it delivers and keeps it when every delivery fails, so
a key that never changes turns one lost delivery into silence.

`generative-research.yml` also publishes article-level telemetry to the same
topic. Route delivery gets only the backend, slug, run/dashboard link, and a
one-line quality summary. The full payload saved in Postgres includes output
file, GitHub article URL, model attempt outcomes, index metadata, and final
article quality metrics.

Langfuse now complements this path for the generative-research pilot with
content-free attempt observations, tool/model markers and mechanical gate scores.
It uses a separate nonblocking reporting job; Hooker remains the notification
route. See [research observability and RSI](research-observability.md) for coverage,
credential boundaries, missing-data semantics, and the bounded improvement loop.
