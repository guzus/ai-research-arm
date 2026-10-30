---
slug: zhipu-glm-5-5-flash-2026-10
title: "GLM-5.5-Flash — reported Zhipu model listing on OpenCode ahead of any announcement"
company: "Zhipu AI (Z.ai)"
model: "GLM-5.5-Flash"
status: in-testing
status_note: |
  Single-source report (@nivlek_smada, 2026-10-29 12:57 UTC) of a GLM-5.5-Flash entry under Zhipu on OpenCode.
  No pricing, usage data or release date, and no Zhipu statement. The same account warns that fake listings
  have appeared before. A sibling post in the same thread mentions a "744B flagship" with no benchmarks or
  announcement. That claim is too garbled to adopt.
expected: "TBD — no date or official signal."
labels:
  - china
  - registry-leak
  - open-weights-lineage
verification: partial
sources:
  - "https://x.com/nivlek_smada/status/2115790078630838545"
  - "https://x.com/nivlek_smada/status/2115790085593673924"
  - https://x.com/_elenajoseph_/status/2116129236251754758
created_at: 2026-10-29
updated_at: 2026-10-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-29
    change: "Created — IN-TESTING / unverified. @nivlek_smada (2026-10-29 12:57 UTC) reports a GLM-5.5-Flash listing under Zhipu on OpenCode with no pricing, usage data or release date, and adds that fake listings have appeared before. A registry entry counts as an artifact, so the status is in-testing. Verification is unverified: one account, no screenshot text in signal, and no Zhipu statement. The prior GLM generation is on the closed [[zhipu-glm-5-3-2026-08]]."
  - ts: 2026-10-30
    change: "In-testing, unchanged; verification unverified -> partial. A second account, @_elenajoseph_ (2026-10-30 11:25 UTC), describes the same OpenCode page for glm-5.5-flash and links it. The page reports 0 observed tokens, 0 unique users, and no context window, pricing or release date. This is a second independent observer of the same registry artifact, so the listing itself is now partially corroborated. The model's existence and timing are not: there is still no Zhipu statement, and the account itself says the entry could be a placeholder. Same thread context: Zhipu CEO Zhang Peng reportedly plans a Singapore research centre and an NUS PhD collaboration (reported plans, not tracked here)."
---
A model-registry entry is the same class of evidence that came before Meta's Muse Spark 1.4
([[meta-muse-spark-1-4-2026-09]], an OpenCode registry sighting). This is why a single sighting still gets a ticket.
The report is thin, though: one account, no pricing, and the poster's own warning about fake listings.

The version jump from GLM-5.3 ([[zhipu-glm-5-3-2026-08]], closed) to "5.5" skips a number. That fits Zhipu's
history of uneven version steps, but nothing in signal confirms it. A GLM-5.3-HighSpeed serving variant is
tracked separately ([[zhipu-glm-5-3-highspeed-2026-10]]).

If no second sighting or Zhipu signal appears within the stale-rumor window, close this as `stale-rumor-unverified`.
