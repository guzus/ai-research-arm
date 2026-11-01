---
slug: anthropic-claude-text-watermarking-2026-11
title: "Claude text watermarking reportedly extends to older models (Mythos 5, Opus 4.7, Opus 4.6, Sonnet 4.6) from Nov 3"
company: Anthropic
model: Claude
status: confirmed
status_note: |
  **Single secondary source.** @DDJCXX (2026-11-01 13:37 UTC, Chinese): from November 3, four older Claude
  models (Mythos 5, Opus 4.7, Opus 4.6, Sonnet 4.6) start adding invisible watermarks to generated text.
  Newer models such as Opus 5.5 reportedly already do. It covers the web app, Claude Code and the API,
  worldwide, not only the EU. Detection is said to be open only to regulators, law enforcement, media, schools
  and research institutions, and shows only that Claude was involved, not who wrote the text.

  Verification is `unverified`: the post says the original source is in its replies, which were not captured.
expected: "Older-model watermarking from 2026-11-03 (reported)."
labels:
  - anthropic
  - watermarking
  - provenance
  - policy
  - unverified
verification: unverified
sources:
  - "https://x.com/DDJCXX/status/2116887342267199833"
created_at: 2026-11-01
updated_at: 2026-11-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-11-01
    change: "Created — CONFIRMED / unverified. Successor to the closed [[anthropic-claude-watermarking-2026-08]] (closed 2026-09-14 as stale-rumor-unverified). @DDJCXX reports that from 2026-11-03 Mythos 5, Opus 4.7, Opus 4.6 and Sonnet 4.6 begin watermarking output across web, Claude Code and API worldwide, that newer models like Opus 5.5 already do, and that detection is limited to vetted institutions. Single secondary source; the cited original was not captured."
---

In August a report said Anthropic would watermark everything Claude writes. That ticket,
[[anthropic-claude-watermarking-2026-08]], closed as stale after no corroboration, and it stays closed.
Today's claim is more specific: it implies watermarking is already live on the newest models and gives a
date for older ones. That makes it a new ticket rather than a reopening.

OpenAI launched text watermarking in early October, opt-in on the API and on by default in the EU under
the AI Act ([[openai-text-watermarking-2026-10]]). The reported Claude scheme differs in two ways: it is
global, and detection is restricted to institutions.

The post also lists practical effects: light grammar edits leave few traces, translations carry the mark
throughout, and code is largely unaffected. These are relayed, not checked.

**Transition triggers:** Anthropic post, docs or usage-policy change → verification `confirmed`. If nothing
corroborates within about 15 cycles → close as stale-rumor-unverified.
