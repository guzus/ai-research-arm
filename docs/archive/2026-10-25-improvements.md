# Langfuse observability foundation — 2026-10-25

This change validates evidence capture and transport. It does **not** demonstrate
better research output, a better model, or an improved autonomous optimizer.

## Contract

- Baseline: `a7a572604ca734588d4c6f7e9a4b9069bd9e419b` on `main`. Hooker retained
  outcomes, Claude-compatible actions exposed overwriteable execution files,
  and the weekly methodology agent had no Langfuse evidence or matched-evaluation
  contract. No Langfuse repository configuration existed.
- Treatment: capture a content-free projection immediately after each native/
  Fireworks attempt; export from an isolated reporting job; feed bounded
  production diagnostics to the existing weekly job.
- Acceptance: preserve failed-attempt evidence across path reuse; export no raw
  text/secrets; keep unknown fields unknown; return the correct observation
  hierarchy/model/usage; replay without duplicates; exclude smoke data from RSI;
  leave publication gates intact.
- Regression boundary: existing routing, retry/translation dispatch, immutable
  tool pins, workflow lint and CI workflow contracts. No model routing changed.
- Cases: fixed synthetic array/JSONL transcripts, repeated message IDs, failed
  tools, overwritten paths, missing/malformed/oversized data, malicious labels,
  capped observations, absent raw outcomes and bounded network failure. Transfer
  check: real completed research run `40015845309`, imported without inventing
  missing detailed traces or publication scores.
- Budget: one implementation candidate, deterministic local checks, bounded API
  smoke/replay/readback checks; no new model calls or research dispatches.

## Observed result

- Normal capture → offline-export CLI entrypoint passed without keys/network.
- Japan Langfuse project accepted and returned the synthetic root, agent,
  generation and tool as `SPAN`, `AGENT`, `GENERATION`, and `TOOL`.
- Re-export of an identical synthetic trace retained **4 observations / 2
  scores**, with exact reported usage: 10 input, 2 output, 5 cache-read tokens.
  These are fixture values in `smoke-test`, not real billed usage.
- Production evidence excluded both smoke traces. The historical failed run
  yielded 3 workflow/attempt observations and no manufactured gate scores.
- Independent review found and corrected missing→false coercion, missing
  environment filtering, truncated API metadata, unbounded integer conversion,
  and unreported capture truncation. Root attempt diagnostics now make model,
  coverage, reported usage and tool-failure evidence available to RSI.
- GitHub's post-`continue-on-error` step conclusion cannot establish an agent's
  raw success. When a snapshot is absent, that raw outcome remains unknown.

Validation: 21 focused behavioral/entrypoint tests, 92 backend-matrix tests,
toolchain-pin tests, UTC workflow tests, translation-dispatch tests, CI workflow
tests, backend matrix consistency, actionlint and diff whitespace checks.

## Retained state and next hypothesis

Retain the observability pilot and bounded weekly experiment contract. Actual
production capture/upload/reporting still requires the next generative run after
delivery; API smoke/readback and historical ingestion do not establish that path.
The weekly model has not yet executed the revised RSI instructions, so its
experimental compliance and any research-quality gain remain untested.

Next bounded workstream: validate structured output for the pinned Cursor CLI
against its current fatal-error detection and translation retry/canary contracts,
then expand capture to the editorial lanes. Do not label plain-text adapters as
fully instrumented or use missing usage as zero cost. A research-improvement
experiment still needs frozen source inputs, an evaluator, and independent
reserved cases before any candidate is promoted.
