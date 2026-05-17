# Hooker Telemetry

ARA workflow telemetry is published to Hooker topic `ara-telemetry`.

Route:

- Hooker URL: `https://hooker.guzus.xyz`
- Topic: `ara-telemetry`
- Telegram chat: `-1003805075491`
- Telegram thread: `75713`

All GitHub Actions workflows include a final non-blocking telemetry step using
the local composite action at `.github/actions/hooker-telemetry`. The payload
includes workflow name, job name, run URL, event, ref, SHA, actor, status, and
the raw structured object stored in Hooker message payload metadata.

`generative-research.yml` also publishes article-level telemetry to the same
topic: backend, slug, output file, dashboard link, model attempt outcomes, and
final article quality metrics.
