# Since the Open-Sourcing Post

The [open-sourcing post](https://guzus.substack.com/p/open-sourcing-ai-research-arm-ara)
(published **2026-07-03**) is the best introduction to ARA's philosophy. The
repo keeps moving, though — this page bridges the post to the current state,
section by section, so readers arriving from the article aren't navigating a
snapshot. Last reconciled: **2026-07-06**. When this page itself drifts,
update it or move it to [`docs/archive/`](archive/).

## Power of Audit Logs — holds, now mechanically enforced

"Every Action ends with a commit" was a convention when the post was
written. It is now a **contract**: agent lanes declare `expected-paths` and
`allowed-paths`, and composite guards
(`.github/actions/require-output`, `require-diff-scope`) fail the run if the
promised artifact wasn't committed or the diff strayed out of bounds.
Publishing goes through `safe-push`. Two GitHub-hosted watchdogs survive
self-hosted outages: one re-runs jobs whose ephemeral Cloud Run worker
vanished mid-run, and `scripts/check_lane_freshness.py` alerts when any
lane's committed output goes stale against its cadence.

## Power of Constraints — holds, and spread to the infrastructure

The ARA DSL story is unchanged (compiler → validator → allowlisted
components, with [`ARA_CATALOG.json`](../ARA_CATALOG.json) and
[`COMPONENTS.md`](../COMPONENTS.md) kept in CI-enforced lockstep). What's
new is that the same philosophy — constrain the output shape, validate
deterministically, reject drift — now governs the *routing layer* too:
the backend matrix and the README routing diagram are **generated** from
config and CI refuses to let them lie (see next section).

## Power of Budget Optimization — inverted, three days after the post

The post described the routing as: Claude subscription primary; when the
weekly quota runs out, route to cheap OSS models on Fireworks. That was
true at publish time. Since then the arrangement flipped into **OSS-first
with Claude as the safety net**, and the whole thing became a single
declarative file:

- **[`data/agent-backends.json`](../data/agent-backends.json)** is the
  single source of truth: every lane, the backend profile table, and an
  **ordered fallback chain**. Scheduled lanes resolve it *at runtime*
  ([`scripts/select_backend.py`](../scripts/select_backend.py)), so
  re-routing the fleet is a one-line JSON edit — no workflow changes.
- **GLM-5.2 via Fireworks is the primary backend** for effectively every
  scheduled lane ([`689087e2`](https://github.com/guzus/ai-research-arm/commit/689087e2)).
  DeepSeek V4 Flash powers the headline-dedupe judge and a comparison tier.
- **Z.ai joined as a second GLM-5.2 source**
  ([`acebfe5e`](https://github.com/guzus/ai-research-arm/commit/acebfe5e)) —
  a Claude-Code-compatible Anthropic endpoint on the Z.ai Coding Plan, with
  a dedicated canary workflow for provider diagnostics.
- **On a provider outage the chain walks in order** — currently
  `zai-glm-5p2 → claude` — probing each candidate and running the first
  one that's up. Native Claude went from "the default" to "the guaranteed
  terminal fallback."
- **Comparison lanes are strict** (never fall back): their artifacts must
  stay attributable to the backend on the label.
- **Below the models sits a zero-model floor**: deterministic composers
  (`scripts/deterministic_*.py`) keep the RSS, HN/Reddit, arXiv, digest,
  Bluesky, and Twitter lanes shipping honestly-labeled output even if every
  provider is down at once.

The forcing function was real: a Fireworks account suspension in early July
took the primary provider offline for days. The system now assumes any
provider can vanish. The full per-lane picture is the generated
[`docs/backend-matrix.md`](backend-matrix.md) and the routing diagram in
the [README](../README.md#backend-routing).

## Power of Composability — holds

Birdy still crawls X for free; the Twitter pipeline is now **Birdy-only and
read-only**, with multi-account rotation. Hooker still delivers headline
alerts to Telegram — now behind a layered dedupe ledger plus an
agent-in-the-loop judge for the contested band
([`docs/headline-dedupe.md`](headline-dedupe.md)). The Gemini-TTS daily
brief and the S3-backed Mac-mini playback loop are unchanged.

## Systems the post didn't cover

These predate the post but didn't fit its four themes:

- **LLM Wiki** ([`research/wiki/`](../research/wiki/)) — a compounding,
  CRUD'd knowledge base (one page per entity/concept/theme) ingested daily
  from the curated digest, exportable as an Open Knowledge Format bundle
  ([`docs/okf.md`](okf.md)).
- **Model-release tickets** ([`research/models/tickets/`](../research/models/tickets/))
  — a persistent CRUD store behind the dashboard's "Jira" tab (renamed from
  the timeline tab in [#200](https://github.com/guzus/ai-research-arm/pull/200)).
- **Arm timeline lane** — keeps the dashboard's Arm tab fresh in the
  Docker-built production image (born from the 2026-07-02 empty-tab
  incident).
