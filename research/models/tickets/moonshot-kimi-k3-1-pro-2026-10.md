---
slug: moonshot-kimi-k3-1-pro-2026-10
title: "Moonshot AI launches Kimi K3.1 Pro — 2.8T-total / 104B-active multimodal MoE, open weights due by Nov 4"
company: Moonshot AI
model: Kimi K3.1 Pro / K3.1 Pro Highspeed
status: released
status_note: "Live on Kimi web, Kimi Work, Kimi Code and the Kimi API per multiple relays; open weights promised by 2026-11-04. No Moonshot first-party post captured in this fetch."
expected: "API live 2026-10-26; open weights by 2026-11-04 (offensive-cyber data removed first, per relays)."
labels:
  - frontier-model
  - open-weights
  - multimodal
  - china
verification: partial
sources:
  - https://x.com/AINativeF/status/2114707850933178663
  - https://x.com/ChinaAIDaily/status/2114709154267021724
  - https://x.com/PraxeoSys/status/2114708860527423832
  - "@gzlin"
  - "@Kimi_Moonshot"
created_at: 2026-10-26
updated_at: 2026-10-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-26
    change: "Created — RELEASED / partial. Moonshot AI launched Kimi K3.1 Pro and a faster K3.1 Pro Highspeed via Kimi web, Kimi Work, Kimi Code and the Kimi API (@AINativeF, 2026-10-26 13:16 UTC, citing @Kimi_Moonshot): a mixture-of-experts model with 2.8T total / 104B active parameters, 1M-token context and multimodal input, with a claimed 65% hallucination reduction on financial modelling. Relayed pricing is $2/$10 per MTok, down from $3/$15 on K3 (@gzlin, @PraxeoSys), with Terminal-Bench 65.7% vs 66.4% for Claude Opus 5.5. Open weights promised by 2026-11-04; @ChinaAIDaily says Moonshot removed offensive-cyber data first, cutting a vulnerability-research score from 90.5% to 81.0%. Partial: several consistent relays, no Moonshot post captured. Successor to the closed [[moonshot-kimi-k3]]."
---

Moonshot AI shipped **Kimi K3.1 Pro**. The closed [[moonshot-kimi-k3]] ticket first flagged K3.1 as "incoming" in August. Relays of the launch article describe a 2.8T-total / 104B-active MoE with 1M-token context and multimodal input. A **K3.1 Pro Highspeed** variant ships alongside it.

**The main news is the price.** Relays put the API at $2/$10 per MTok. That is lower than K3's $3/$15, for a bigger model. On Terminal-Bench it scores 65.7%, about a point behind Claude Opus 5.5 (66.4%), at half the price.

**The weights arrive with a safety edit.** Open weights are due by 2026-11-04. Moonshot reportedly removed offensive-cyber training data before release, and a vulnerability-research score dropped from 90.5% to 81.0%. Open-weight labs rarely publish what capability they gave up, so that number is unusual.

Verification stays `partial` until a Moonshot post or the Hugging Face release is captured. The next update is the weights drop.
