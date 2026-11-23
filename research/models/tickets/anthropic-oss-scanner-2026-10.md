---
slug: anthropic-oss-scanner-2026-10
title: Anthropic releases OSS Scanner, a free open-source LLM vulnerability scanner (reported)
company: Anthropic
model: OSS Scanner (on Claude)
status: closed
status_note: Single news-brief report; no Anthropic post captured.
expected: Released per report.
labels:
  - security
  - open-source
  - tooling
verification: unverified
sources:
  - https://x.com/ChinaAIDaily/status/2114707775658037337
created_at: 2026-10-26
updated_at: 2026-11-23
closed_at: 2026-11-23
closed_reason: released-and-aged
history:
  - ts: 2026-10-26
    change: "Created — RELEASED / unverified. @ChinaAIDaily's 2026-10-26 brief reports Anthropic OSS Scanner: a free, open-source vulnerability-scanning tool that uses an LLM in place of fuzzing, finding hundreds of vulnerabilities in 11 days with 88% of findings meeting disclosure standards. Single secondary source; no Anthropic post captured."
  - ts: 2026-11-23
    change: "CLOSED — released-and-aged. OSS Scanner (on Claude) was reported released in a 2026-10-26 brief, 28 days ago, past the four-week threshold, so the lifecycle close trigger applies. Verification at close: unverified. Verification stays unverified: no Anthropic post was ever captured, so the closure does not confirm the tool exists as described. No signal was captured for this ticket after its last history entry (the timeline lane did not publish 2026-11-04 to 2026-11-22, and today's fetch returned no posts), so later developments are not reflected here. Closure means the release event has aged out of active tracking; any successor version is a new ticket, not a reopening."
---

A Chinese-language news brief reports that Anthropic released **OSS Scanner**, a free, open-source tool that finds vulnerabilities with a language model instead of fuzzing. In the reported trial it found hundreds of vulnerabilities in 11 days, and **88%** of findings met disclosure standards.

If confirmed, it fits Anthropic's defensive-cyber positioning around its gated cyber-capable models (see [[mythos-public-release]]). Verification is `unverified` because the only source is one relay. Upgrade on an Anthropic post or repo; otherwise close as stale.
