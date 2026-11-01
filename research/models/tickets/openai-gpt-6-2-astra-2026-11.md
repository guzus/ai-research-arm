---
slug: openai-gpt-6-2-astra-2026-11
title: "GPT-6.2 Astra — gpt-6.2-astra model string reportedly appearing in Codex usage analytics (gray rollout)"
company: OpenAI
model: GPT-6.2 Astra
status: in-testing
status_note: |
  **Secondary only, but from several accounts.** @TokenGremlin (2026-11-01 10:09 UTC): the Codex model picker
  still says "GPT-6 Astra", but the usage breakdown for some accounts lists `gpt-6.2-astra` separately, and
  multiple users see the same thing. @shiparena (11:15 UTC) relays this as a gray rollout. @AnikaCodes (12:13 UTC)
  says someone inspected an API response that returned `gpt-6.2-astra`.

  **Why `in-testing`:** a model identifier showing up in production telemetry is a real artifact. It is not an
  announcement. As @SlimAssiliX points out, matching strings across accounts rule out a one-off glitch, but they
  do not tell an A/B test apart from internal routing or a label change.
expected: "No date. Commentary calls a release imminent; no OpenAI post captured."
labels:
  - frontier-model
  - openai
  - codex
  - leak
  - gray-rollout
verification: partial
sources:
  - "https://x.com/TokenGremlin/status/2116834891744600291"
  - "https://x.com/shiparena/status/2116851716222255580"
  - "https://x.com/AnikaCodes/status/2116866259182911713"
  - "https://x.com/SlimAssiliX/status/2116864487978385882"
  - "https://x.com/pradeepXkapoor/status/2116882770190299219"
created_at: 2026-11-01
updated_at: 2026-11-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-11-01
    change: "Created — IN-TESTING / partial. Several accounts (@TokenGremlin 10:09 UTC, @shiparena, @AnikaCodes) report that `gpt-6.2-astra` appears separately in Codex usage analytics, and reportedly in an API response, while the picker still reads 'GPT-6 Astra'. No OpenAI announcement. Commentary (@pradeepXkapoor) asks whether this is the model OpenAI shelved before DevDay ([[openai-gpt-6-1-astra-shelved-2026-09]]). That link is speculation and is not adopted."
---

OpenAI's Astra line is its frontier tier. GPT-6.1 Astra was finished and then shelved after internal safety
tests in late September ([[openai-gpt-6-1-astra-shelved-2026-09]]). Its cheaper sibling GPT-6.1 Terra shipped
in late October ([[openai-gpt-6-1-terra-2026-10]]). A `gpt-6.2-astra` string in Codex telemetry is the first
sign of the next Astra version.

This is a separate ticket rather than an update to the shelved 6.1 Astra ticket because it is a different
version number and possibly a different checkpoint. Whether 6.2 is a retrained 6.1, or something new, is not
known.

The evidence pattern (a version string in usage data before the picker changes) has come before past OpenAI
releases. It is still only community reports.

**Transition triggers:** OpenAI post, release notes or picker change → `confirmed` / `released`. If nothing
corroborates within about 15 cycles → close as stale-rumor-unverified.
