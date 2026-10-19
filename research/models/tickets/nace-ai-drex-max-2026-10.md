---
slug: nace-ai-drex-max-2026-10
title: Nace AI releases Drex Max, a multimodal decision model for computer-use agents
company: Nace AI
model: Drex Max
status: released
status_note: |
  **Primary launch.** @NaceAI (2026-10-19 13:33 UTC): "Drex Max is here: our multimodal
  decision model — text, images, and video. 34 ms/decision, under 1s at 262K tokens.
  $0.06 / 1M input tokens. Available today."

  **Company-reported benchmarks via a sponsored-style relay.** @systemdesignone
  (13:38 UTC) lists a 67.59 Decision Index across 37 benchmarks (vs 60.70 for Jev 1.14),
  88.3% on Mind2Web (vs 86.5%), 174 ms median latency on its vision benchmark (vs 253 ms),
  and "up to 167× cheaper per token" than the models behind Claude, GPT and Gemini
  computer use. No independent measurement yet. Note that this "Decision Index" is not
  necessarily the Artificial Analysis Decision Index v1.0 cited in
  [[liquid-ai-d1-ultra-2026-10]].
expected: "Available 2026-10-19 per Nace AI. Open: independent Decision Index placement and weights/licensing."
labels:
  - decision-model
  - computer-use
  - multimodal
  - startup
verification: confirmed
sources:
  - "https://x.com/NaceAI/status/2112175183448461683"
  - "https://x.com/systemdesignone/status/2112176629816438895"
created_at: 2026-10-19
updated_at: 2026-10-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-19
    change: "Created — RELEASED / confirmed. @NaceAI announced Drex Max on 2026-10-19 13:33 UTC as available today: a text/image/video decision model at 34 ms per decision, under 1s at 262K tokens, priced at $0.06 per 1M input tokens. Benchmark claims (67.59 Decision Index across 37 benchmarks vs 60.70 for Jev 1.14; 88.3% Mind2Web) are company-reported, relayed by @systemdesignone. Joins the October decision-model cluster with [[liquid-ai-d1-ultra-2026-10]], [[microsoft-decision-1-2026-10]], [[perplexity-decider-v1-2-2026-10]] and [[typesafe-jev-1-14-2026-10]]."
---

"Decision models" became a product category in October 2026. They score or pick
among options in one pass instead of generating text token by token. That makes them
cheap and fast for the many small choices a computer-use agent makes. Drex Max is the
fifth entrant this desk has logged in a week.

Nace AI's claims are self-reported and compare only against Jev 1.14. The key check is
whether Artificial Analysis or another independent party places it on a shared
leaderboard against d1-ultra, Microsoft-Decision-1 and Decider v1.2.

**Transition triggers:** independent benchmark placement → note here; released ≥4
weeks → close as released-and-aged.
