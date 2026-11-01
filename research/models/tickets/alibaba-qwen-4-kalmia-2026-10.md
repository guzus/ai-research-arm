---
slug: alibaba-qwen-4-kalmia-2026-10
title: Stealth "Kalmia" model in Arena Code Arena, attributed by testers to Alibaba Qwen 4
company: Alibaba
model: Qwen 4 (suspected; codename Kalmia)
status: in-testing
status_note: |
  Anonymous arena model; the Kalmia → Qwen attribution still rests on community tokenizer fingerprinting
  relayed by one account. Separately, a Qwen team member said on stage (2026-10-29, Amsterdam) that Qwen 4
  is coming "next week", and a Qwen4 model-name handling change has landed in the official Qwen code repo.
expected: "Week of 2026-11-02 per an on-stage Qwen team remark (secondary relay); no official date."
labels:
  - frontier-model
  - stealth-model
  - arena
  - china
verification: partial
sources:
  - https://x.com/volatilemarkts/status/2114676123359498542
  - "https://x.com/Smlay_ero/status/2115014572004561199"
  - "https://x.com/kimmonismus/status/2115794808497168787"
  - "@jtdavies"
  - "https://x.com/RagerrrYT/status/2116877919054397950"
created_at: 2026-10-26
updated_at: 2026-11-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-26
    change: "Created — IN-TESTING / unverified. @volatilemarkts (2026-10-26 11:10 UTC) reports a stealth model codenamed 'Kalmia' in Arena's Code Arena blind tests, attributed to Alibaba's Qwen 4 by community tokenizer fingerprinting; the same post ties a sibling stealth model, 'Kibitz', to Kimi K3.1 ([[moonshot-kimi-k3-1-pro-2026-10]]). The post's architecture claims (51B lookup-embedding layer, RSI training) are unsourced and not adopted. Prior Qwen-4 coverage sits on the closed [[alibaba-qwen-4-architecture-2026-08]], left untouched."
  - ts: 2026-10-27
    change: "In-testing, unverified — Qwen 4 architecture recap, no new Kalmia evidence. @Smlay_ero (2026-10-27 09:35 UTC) lists the upcoming Qwen4 series features: QSA (Query-Sparse Attention) + GDN with a 7.6x prefill speedup at 1M context ('per Tongyi Cloud'), gated residual, 51B N-gram embedding parameters and the Muon optimizer, with Qwen4-Max positioned against Opus 5.5. This matches the 51B embedding claim in the creation entry and the architecture preview on the closed [[alibaba-qwen-4-architecture-2026-08]]. It does not tie the Kalmia arena model to Qwen 4, so verification stays unverified."
  - ts: 2026-10-29
    change: "In-testing; verification unverified -> partial. Qwen 4 release timing: @jtdavies (2026-10-29 09:20 UTC, 'Live from Amsterdam') quotes Xudong Guo, a Qwen research scientist, saying Qwen4 is coming 'next week'. @kimmonismus (2026-10-29 13:16 UTC) repeats this as the 'Qwen CTO' (the title is disputed by the original post) and adds that a change handling model names for the upcoming Qwen4 family has been merged into the official Qwen code repository. This is a second, independent signal that the Qwen 4 family is close. It is still secondary, with no Alibaba post, and it does not prove that Kalmia is Qwen 4. Expected set to the week of 2026-11-02."
  - ts: 2026-11-01
    change: "In-testing, partial, unchanged — timing restated, one new detail. @RagerrrYT (2026-11-01 13:00 UTC) repeats that Qwen 4 model names are showing up in Qwen Code and that an Alibaba Cloud speaker said 'next week' on stage, with no official date. New detail, unchecked: the Qwen 4 entries reportedly default to a 1M-token context window. Still no Alibaba announcement, and nothing new ties the Kalmia arena model to Qwen 4. Separately, a Qwen-in-Apple-Intelligence (China) ship date is tracked at [[alibaba-qwen-apple-intelligence-china-2026-11]]."
---

A stealth model codenamed **"Kalmia"** has appeared in Arena's Code Arena. Community testers attribute it to **Alibaba's Qwen 4** generation by tokenizer fingerprinting. Its sibling stealth model, "Kibitz", was tied to Kimi K3.1, which launched on 2026-10-26 ([[moonshot-kimi-k3-1-pro-2026-10]]). That track record is why arena sightings like this are worth a ticket.

The anonymous arena entry is a real artifact, so the status is `in-testing`. The Qwen attribution is weaker: it comes from one aggregator account. The same post lists many architecture details with no sources: a 51B parameter-free lookup embedding, RSI + Muon training, and a four-tier Max/Plus/Flash/27B family. Only the sighting and the attribution claim are recorded here.

The earlier Qwen 4 architecture ticket, [[alibaba-qwen-4-architecture-2026-08]], is closed as `released-and-aged` and stays closed. This ticket tracks the next shipping artifact.
