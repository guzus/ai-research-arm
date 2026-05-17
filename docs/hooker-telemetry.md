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

`generative-research.yml` also publishes article-level telemetry to the same
topic. Route delivery gets only the backend, slug, run/dashboard link, and a
one-line quality summary. The full payload saved in Postgres includes output
file, GitHub article URL, model attempt outcomes, index metadata, and final
article quality metrics.
