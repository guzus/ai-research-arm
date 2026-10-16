---
slug: openai-moonshot-distillation-disclosure-2026-10
title: "OpenAI says it blocked a reasoning-trace distillation campaign it links to Moonshot AI"
company: "OpenAI / Moonshot AI"
model: null
status: closed
status_note: |
  Per @findchain's 2026-10-01 digest: OpenAI says that on 2026-07-24/25 it saw
  16,000 requests from 4,000+ users across 15,000+ linked accounts targeting model
  reasoning chains, linked the activity to people associated with Moonshot AI,
  and shut it down on 2026-07-28. Researchers reportedly say the same technique
  still extracts reasoning content from models such as GPT-6 Astra served on
  Azure. Single digest relay; no OpenAI post captured → verification unverified.
expected: "Disclosed. Open: OpenAI's primary write-up, any Moonshot response, and whether Microsoft closes the Azure path."
labels:
  - openai
  - moonshot
  - distillation
  - security
  - china
verification: unverified
sources:
  - https://x.com/findchain/status/2105653235491184775
created_at: 2026-10-01
updated_at: 2026-10-16
closed_at: 2026-10-16
closed_reason: stale-rumor-unverified
history:
  - ts: 2026-10-01
    change: "Created — CONFIRMED / unverified. A single digest (@findchain) reports OpenAI disclosed blocking a July 24-25 distillation campaign against its reasoning traces (16K requests, 4K+ users, 15K+ linked accounts), attributed to Moonshot-linked people and shut down July 28; researchers say the same method still works against GPT-6 Astra on Azure."
  - ts: 2026-10-16
    change: "CLOSED — stale-rumor-unverified. Verification has been unverified since creation on 2026-10-01, and no history entry or corroboration has arrived in 15 daily cycles (2026-10-01 -> 2026-10-16). This ticket rested on a single @findchain digest relay of an OpenAI distillation-campaign disclosure tied to Moonshot AI, with no primary source captured. Closed per the 15-cycle rule; history is preserved. A primary source arriving later opens a successor ticket that links back here."
---

Second frontier lab pointing at Moonshot for distillation, after the US-official
allegations about Claude in [[moonshot-claude-distillation-us-scrutiny-2026-07]].
Also context for Anthropic's decision to bill blocked distillation attempts
([[anthropic-billable-safeguard-blocks-2026-09]]). Kept separate because the
actor making the claim and the targeted model differ.
