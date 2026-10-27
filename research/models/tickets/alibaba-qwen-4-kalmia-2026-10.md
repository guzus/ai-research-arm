---
slug: alibaba-qwen-4-kalmia-2026-10
title: Stealth "Kalmia" model in Arena Code Arena, attributed by testers to Alibaba Qwen 4
company: Alibaba
model: Qwen 4 (suspected; codename Kalmia)
status: in-testing
status_note: Anonymous arena model; the Qwen attribution rests on community tokenizer fingerprinting relayed by one account.
expected: "TBD — the relay says a Qwen 4 roadmap (Max / Plus / Flash / 27B) was laid out at Apsara; no date."
labels:
  - frontier-model
  - stealth-model
  - arena
  - china
verification: unverified
sources:
  - https://x.com/volatilemarkts/status/2114676123359498542
  - "https://x.com/Smlay_ero/status/2115014572004561199"
created_at: 2026-10-26
updated_at: 2026-10-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-26
    change: "Created — IN-TESTING / unverified. @volatilemarkts (2026-10-26 11:10 UTC) reports a stealth model codenamed 'Kalmia' in Arena's Code Arena blind tests, attributed to Alibaba's Qwen 4 by community tokenizer fingerprinting; the same post ties a sibling stealth model, 'Kibitz', to Kimi K3.1 ([[moonshot-kimi-k3-1-pro-2026-10]]). The post's architecture claims (51B lookup-embedding layer, RSI training) are unsourced and not adopted. Prior Qwen-4 coverage sits on the closed [[alibaba-qwen-4-architecture-2026-08]], left untouched."
  - ts: 2026-10-27
    change: "In-testing, unverified — Qwen 4 architecture recap, no new Kalmia evidence. @Smlay_ero (2026-10-27 09:35 UTC) lists the upcoming Qwen4 series features: QSA (Query-Sparse Attention) + GDN with a 7.6x prefill speedup at 1M context ('per Tongyi Cloud'), gated residual, 51B N-gram embedding parameters and the Muon optimizer, with Qwen4-Max positioned against Opus 5.5. This matches the 51B embedding claim in the creation entry and the architecture preview on the closed [[alibaba-qwen-4-architecture-2026-08]]. It does not tie the Kalmia arena model to Qwen 4, so verification stays unverified."
---

A stealth model codenamed **"Kalmia"** has appeared in Arena's Code Arena. Community testers attribute it to **Alibaba's Qwen 4** generation by tokenizer fingerprinting. Its sibling stealth model, "Kibitz", was tied to Kimi K3.1, which launched on 2026-10-26 ([[moonshot-kimi-k3-1-pro-2026-10]]). That track record is why arena sightings like this are worth a ticket.

The anonymous arena entry is a real artifact, so the status is `in-testing`. The Qwen attribution is weaker: it comes from one aggregator account. The same post lists many architecture details with no sources: a 51B parameter-free lookup embedding, RSI + Muon training, and a four-tier Max/Plus/Flash/27B family. Only the sighting and the attribution claim are recorded here.

The earlier Qwen 4 architecture ticket, [[alibaba-qwen-4-architecture-2026-08]], is closed as `released-and-aged` and stays closed. This ticket tracks the next shipping artifact.
