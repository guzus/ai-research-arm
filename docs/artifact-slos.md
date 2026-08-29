# Artifact and publication SLO registry

`data/artifact-slos.json` is the machine-readable contract for pipeline output.
Each entry names the producer workflow, exact artifact paths, cadence kind,
freshness SLO (only for fixed cadence), validators, degraded-output policy, and
optional content-volume policy. Policies that can publish usable-but-degraded
output also carry an executable `degraded_signal`; the watchdog does not infer
producer health from prose names.

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

Freshness reporting has two independent axes:

- **availability** is `available`, `unavailable`, or `unknown`, derived from
  path existence and the most recent commit age;
- **producer state** is `healthy`, `degraded`, or `unknown`, derived only from
  a registry-declared signal.

This preserves the useful distinction between `available/degraded` (for
example, today's deterministic digest exists but model synthesis failed) and
`unavailable/healthy` (the last normal artifact exceeded its SLO). Both alert.
The legacy JSON `state` (`fresh|stale|missing|unknown`), `stale` action output,
and `stale_lanes` output remain compatibility fields; `stale` now means the
same thing as the new aggregate alert bit, so a degraded producer cannot emit
a false healthy heartbeat. New consumers should use `availability`,
`producer_state`, `alert_lanes`, `unavailable_lanes`, and `degraded_lanes`.
Producer-signal uncertainty is separately listed in `producer_unknown_lanes`,
so an `available/unknown` lane can never disappear between the availability
and degraded bucket lists.

Supported executable signals are intentionally narrow:

- `commit_subject` is available for lane-specific, fully anchored workflow
  contracts, but current fallback state uses durable artifact markers so a
  later audio/spoken-script commit cannot mask a degraded digest.
- `json_boolean_any` resolves registry-declared dotted selectors with `*`
  collection wildcards. Market `stale` flags therefore expose carry-forward
  directly from their public artifact rather than from a commit-message guess.
- `text_regex` matches a fully specified producer field in the latest matching
  artifact. The digest fallback banner persists across same-path audio updates;
  the blog lane's numeric `Fetch errors` summary makes partial-source
  publication visible without guessing from natural-language article copy.

Twitter restore-baseline state comes from the latest status artifact's boolean
`recovery` field. Status remains broader producer-health evidence only: it is
not added to `freshness_paths`, so a recovery heartbeat cannot make an unchanged
public digest available.

A configured signal whose git, JSON, or text evidence cannot be read is
producer-`unknown` and alerts. Exit codes remain `0` for all available/healthy,
`2` for any availability or producer alert, and `1` for an internal error.

The external production synthetic also validates the semantic JSON contracts
for `/research/evidence-search.json` and `/research/claims/public.json`.
It checks stable keys/types—including boolean `reusable` provenance on claim
entries—without coupling liveness to mutable editorial copy, counts, or order.

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
