---
slug: mistral-large-4-2026-10
title: Mistral Large 4 ("Le Chonk") — 1T-parameter / 49B-active multimodal model, API preview live; open weights due end of October
company: Mistral AI
model: Mistral Large 4
status: released
status_note: |
  **First-party launch, 2026-10-06 13:06 UTC (@MistralAI):** "Meet Mistral Large 4,
  aka Le Chonk. 1T parameters, natively multimodal. 49B active. It is the best open
  weights model from US or Europe on aggregated benchmarks. State-of-the-art on
  critical workloads, including cyber defense, manufacturing and finance and it
  surpasses closed frontier models on visual grounding. Forged in Europe end-to-end
  and is deployable from Europe via our own Mistral Cloud infrastructure. Available
  to all via API today. Working with cybersecurity partners privately. Open weights
  release end of October."

  **It is a preview.** @GuillaumeLample (co-founder, 13:24 UTC): "The RL run behind
  this preview is still in flight and shows no sign of saturation — we will release
  a final version before the end of the month along with the weights of the model."
  Self-reported: 82% on vulnerability reproduction and patching, 93% on Cybench,
  among the best on the AA Cyber Index; matches the best open-weight models on
  DeepSWE, AutomationBench and AA-Briefcase; SOTA on finance/legal workflows and
  multimodal grounding.

  **Secondary detail, not first-party in-window:** trained on 4,000 NVIDIA Grace
  Blackwell GPUs, 160+ languages, weights on October 27 (@Daily_Cron); DeepSWE 62%,
  FinWorkBench 67%, Harvey legal-agent 15% vs Kimi K3 13% / GPT-6 Astra 5%
  (@Daviswh). Covered by CNBC, WSJ and WIRED ("still in the race"); CEO Arthur
  Mensch previewed it in Abu Dhabi the same morning without naming benchmarks.
expected: "API preview live 2026-10-06. Final version plus open weights before end of October (Oct 27 per secondary reports). Open: licence, independent benchmarks, pricing, and whether the final RL checkpoint differs materially from the preview."
labels:
  - frontier-model
  - open-weights
  - multimodal
  - europe
  - moe
verification: confirmed
sources:
  - https://x.com/MistralAI/status/2107457414387622310
  - https://x.com/GuillaumeLample/status/2107461898127954001
  - https://x.com/GuillaumeLample/status/2107461907313475700
  - https://x.com/GuillaumeLample/status/2107461910702465095
  - https://x.com/Daily_Cron/status/2107462654910456306
  - https://x.com/Daviswh/status/2107460591111799042
  - https://x.com/CNBCtech/status/2107459992236278207
  - https://x.com/WSJbusiness/status/2107459898594230708
  - https://x.com/WIRED/status/2107461283750580705
  - "@MistralAI"
  - "@GuillaumeLample"
created_at: 2026-10-06
updated_at: 2026-10-06
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-06
    change: "Created — RELEASED / confirmed. @MistralAI announced Mistral Large 4 ('Le Chonk') on 2026-10-06 13:06 UTC: 1T total / 49B active parameters, natively multimodal, claimed best open-weights model from the US or Europe on aggregated benchmarks, SOTA on cyber defense, manufacturing and finance, ahead of closed frontier models on visual grounding, available to all via API today, open weights end of October. Co-founder @GuillaumeLample says it is a preview — the RL run is still in flight and a final version ships with weights before month-end — and self-reports 82% vulnerability reproduction/patching and 93% Cybench. Released because API access is open to all now; weights are not yet out. Secondary: 4,000 Grace Blackwell GPUs, 160+ languages, Oct 27 weights date, DeepSWE 62% / FinWorkBench 67% / Harvey legal 15%. Covered by CNBC, WSJ, WIRED. Mistral's first model release since April per @GenAISpotlight; follows the ~€3B round at [[mistral-funding-round-2026-06]]."
---

Mistral's first frontier-scale release in roughly six months, and its first model
at the trillion-parameter MoE scale that Chinese labs (Kimi K3, DeepSeek V4) have
defined for open weights. The framing is explicitly geopolitical: "best open weights
model from US or Europe", "forged in Europe end-to-end", deployable from Mistral's
own cloud. Coverage (CNBC's headline) read it as "rivals best open
systems from China" — i.e. matching, not beating, the Chinese open frontier on
general benchmarks.

The lead claims are domain-specific: cyber defense, finance, legal, visual
grounding. That is where Mistral says it is SOTA; on agentic coding it claims parity
with the best open models. The private work with cybersecurity partners mirrors the
gated-cyber pattern of [[google-gemini-4-2026-09]] and [[mythos-public-release]],
but here the weights are promised to everyone within weeks — which is the point
Lample makes when he says open models "do not refuse to help".

Funding context: the ~€3B round at >€21B valuation tracked at
[[mistral-funding-round-2026-06]] closed in September; this is the first product it
paid for. Sovereign-procurement context sits at
[[france-sovereign-ai-procurement-2026-08]] and [[mistral-humain-saudi-2026-08]].

Transition triggers: weights published (record licence and date) → UPDATE; final
non-preview checkpoint → UPDATE; ≥4 weeks after weights → close as
released-and-aged.
