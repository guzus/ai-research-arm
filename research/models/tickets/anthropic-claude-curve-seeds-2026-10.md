---
slug: anthropic-claude-curve-seeds-2026-10
title: "Claude reportedly finds the origin of the NSA-chosen seeds behind a widely used elliptic curve ($36,864 bounty)"
company: Anthropic
model: Claude (internal model, unnamed)
status: confirmed
status_note: |
  **Reported 2026-10-16.** Cryptographer @sweis posted "CLAUDE FOUND THE SEEDS"
  (2026-10-16 18:41 UTC). @Turbodev1x (2026-10-17 09:51 UTC) gives more detail: the
  NSA picked the seeds for "one of the most used elliptic curves in cryptography" about
  25 years ago, their origin was never explained, and a $36,864 bounty stood for it.
  "An internal Anthropic model cracked it in under 30 minutes." The post quotes the
  model mid-solve: "Let me be skeptical: am I in some sort of simulated/test
  environment?", and then "wow, it's a real discovery". It also cites 3.7M views on the
  announcement overnight.

  **What is not established here.** No @AnthropicAI post or write-up was captured, and
  neither source names the curve or the model in this window. @Turbodev1x is promoting a
  "$SEEDS" token, so treat its framing as promotional. Status is `confirmed` because two
  unrelated accounts, one of them a known cryptographer, report the same specific event.
  Verification is `partial` because there is no primary write-up.
expected: "Reported 2026-10-16. Open: the Anthropic or bounty-holder write-up, which curve and seeds, which model, and independent verification of the derivation."
labels:
  - anthropic
  - cryptography
  - capability
  - research
verification: partial
sources:
  - "https://x.com/sweis/status/2111165738836717980"
  - "https://x.com/Turbodev1x/status/2111394626976330226"
  - "https://x.com/bosatu1024/status/2111780020968390859"
created_at: 2026-10-17
updated_at: 2026-10-18
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-17
    change: "Created — CONFIRMED / partial. @sweis (2026-10-16 18:41 UTC): 'CLAUDE FOUND THE SEEDS'. @Turbodev1x (2026-10-17 09:51 UTC) says an internal Anthropic model explained, in under 30 minutes, where the NSA-chosen seeds of a widely used elliptic curve came from, claiming a $36,864 bounty. It quotes the model asking whether it was in a test environment before calling it 'a real discovery'. No Anthropic primary captured; the curve and model are unnamed in-window. Same-day first-party capability result: Mythos 5 quantum circuits ([[mythos-public-release]]). Prior capability-milestone precedent: [[anthropic-fermat-lean-proof-2026-09]]."
  - ts: 2026-10-18
    change: "Confirmed / partial, unchanged — mainstream Japanese pickup. A Japanese daily top-100 news roundup (@bosatu1024, 2026-10-18 11:22 UTC) lists as item 74: 'AIのClaudeが暗号技術の25年来の謎を30分足らずで解明' (Claude solves a 25-year-old cryptography mystery in under 30 minutes). That matches the 2026-10-17 entry's '25 years' and 'under 30 minutes' details, and shows the story has spread beyond the original posters. The roundup names no outlet, curve or model, so verification stays partial. Still no Anthropic or bounty-holder write-up captured."
---

The provenance of seeds behind standardized elliptic curves has been a standing
trust question in cryptography for decades. If a model really reconstructed how
they were generated, that is a public, checkable result: either the derivation
reproduces the seeds or it does not. That makes it unusually easy to verify, so a
primary write-up should settle it.

The reporting so far comes from social posts, and one of them is tied to a
memecoin. The ticket records the claim at the strength it has today and waits for
the write-up.

**Transition triggers:** an Anthropic or bounty-holder post naming the curve and
showing the derivation → verification `confirmed`; a public refutation → close and
record.
