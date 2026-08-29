# Artifact and publication SLO registry

`data/artifact-slos.json` is the machine-readable contract for pipeline output.
Each entry names the producer workflow, exact artifact paths, cadence kind,
freshness SLO (only for fixed cadence), validators, degraded-output policy, and
optional content-volume policy.

The distinction between cadence kinds is load-bearing:

- `interval` and `daily` entries are freshness-paged.
- `event` entries (for example earnings) remain visible in the inventory but
  have no clock-based SLO; a quiet earnings week is not an outage.
- `on_demand` entries are likewise inventoried without false freshness pages.

`check_lane_freshness.py` and `check_lane_content.py` load this registry.
Market artifacts use their exact files instead of the shared `research/market/`
directory, so a healthy quote refresh cannot hide a stale pricing or GPU lane.
Missing git evidence is `UNKNOWN` and alerts: inability to prove freshness is
not equivalent to healthy.

Scheduled `safe-push` calls are strict by default. Direct publication, a
successfully merged fallback PR, and a genuine no-op pass. A branch-only or
open-PR fallback fails the producing run. `liveness-check.yml` independently
queries open `automation/safe-push/*` PRs and alerts when one remains stranded
for at least one hour.

Generative publication has a second transaction: the methodology sidecars and
`research/claims/index.json` are generated and committed together by
`scripts/finalize_generative_publication.py`. Failure restores the writer-owned
transactional paths without resetting unrelated checkout state; the disposable
workflow checkout then rolls the entire article commit back before push.
