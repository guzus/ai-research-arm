---
slug: deepseek-v4-flash-vision-exp-2026-08
title: DeepSeek-V4-Flash-Vision-Exp lands on the DeepSeek API platform
company: DeepSeek
model: DeepSeek-V4-Flash-Vision-Exp
status: released
status_note: |
  **@testingcatalog** (2026-08-21 09:49 UTC): "DeepSeek-V4-Flash-Vision-Exp
  multimodal model is now available on the DeepSeek API Platform. It
  delivers performance close to Opus 4.8 and matches DeepSeek-V4-Flash on
  text. Supports Chat Completions, Messages & Responses, and mixed text +
  image input."

  The release was pre-signalled by a backend artifact rather than a
  launch post: **@MaxForAI** (relayed by @goodhunt, 2026-08-21) reported
  the exact string `deepseek-v4-flash-vision-exp` appearing in DeepSeek
  Harness code with native image-request adaptation added to the latest
  Harness build — a console/codebase tell that resolved into an API
  listing within hours.

  **Independent corroboration of the capability arrived a day later.**
  @teortaxesTex, benchmarking [[stealth-ox-alpha-model-2026-08]], used
  V4-Flash-Vision-exp as his yardstick: "58.4 DeepSWE… nominally it's the
  same as V4-Flash-Vision-exp, and an okay 'current gen Flash'." That is
  a third party running the model, not a relay of DeepSeek's claim.

  This is a **successor ticket** to the closed
  [[deepseek-v4-vision-2026-06]], which tracked DeepSeek turning on image
  understanding in the consumer web/app in June and closed
  `released-and-aged` on 2026-07-16 with the API and open-weights reach
  explicitly listed as unresolved. This is that unresolved half landing —
  an API-listed, separately-named, experimental Flash-tier multimodal
  model — so it gets its own ticket rather than reopening a closed one.

  Verification `partial`: no @deepseek_ai primary post or model card was
  captured, and the "close to Opus 4.8" figure originates with the
  relayed announcement, not an independent eval. Open weights remain
  unaddressed.

  **2026-08-24 — trade-press pickup and third-party hosting, no new
  evidence.** Aggregator coverage now frames it as "DeepSeek launches a
  new vision AI model **it says** rivals Anthropic's Opus 4.8," pointing
  at a DeepSeek blog post — note the framing preserves that the Opus-4.8
  comparison is DeepSeek's own claim, still not an independent eval.
  Separately the model is appearing on third-party inference platforms
  (a TRON-ecosystem host advertising free V4-Flash and
  V4-Flash-Vision-Exp access alongside Tencent Hy3), which widens reach
  but is promotional, not evidential. Status stays `released`;
  verification stays `partial` — the blog referenced in coverage was not
  itself captured or reachable from this run, and no published
  multimodal benchmark, pricing, or open-weights statement has
  appeared.
expected: "Live on the DeepSeek API platform as of 2026-08-21 (still live 2026-08-24) with Chat Completions / Messages / Responses and mixed text+image input. Pending: an official @deepseek_ai post or model card, published multimodal benchmarks, pricing, whether the 'Exp' tag graduates, and open weights"
labels:
  - deepseek
  - multimodal
  - china
  - flash-tier
  - released
verification: partial
sources:
  - "@testingcatalog"
  - "@goodhunt"
  - "@teortaxesTex"
  - "@MaxForAI"
created_at: 2026-08-23
updated_at: 2026-08-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-23
    change: "Created — DeepSeek-V4-Flash-Vision-Exp went live on the DeepSeek API platform (@testingcatalog, 2026-08-21 09:49 UTC): multimodal, mixed text+image input across Chat Completions/Messages/Responses, claimed close to Opus 4.8 and matching DeepSeek-V4-Flash on text. Pre-signalled by the exact model string appearing in DeepSeek Harness code with native image-request adaptation (@MaxForAI via @goodhunt) hours earlier. Independently exercised the next day by @teortaxesTex, who used it as the reference point for scoring Ox Alpha ('nominally the same as V4-Flash-Vision-exp, an okay current gen Flash'). Successor to the closed [[deepseek-v4-vision-2026-06]], whose closure note left API and open-weights reach explicitly unresolved — this is that half landing, under a distinct model name. Status released; verification partial (no @deepseek_ai primary post or model card, capability figure originates with the announcement relay, open weights unaddressed)."
  - ts: 2026-08-24
    change: "Trade-press pickup and third-party hosting, no new evidence. Aggregator coverage frames it as DeepSeek launching a vision model \"it says\" rivals Opus 4.8, pointing at a DeepSeek blog post — the framing preserves that the comparison is DeepSeek's own claim, not an independent eval, and the blog was not reachable from this run. The model is also now advertised free on third-party inference platforms (a TRON-ecosystem host, alongside Tencent Hy3), which widens reach but is promotional rather than evidential. Status stays released; verification stays partial — still no published multimodal benchmark, pricing, or open-weights statement."
---

The June ticket ([[deepseek-v4-vision-2026-06]]) closed with a specific
open question: DeepSeek had switched on image understanding in the
consumer web and app, announced from a researcher's personal account,
and whether it would reach the **API and open weights** was unresolved.
The API half has now landed — under a different, explicitly experimental
model name.

**The name carries information.** `V4-Flash-Vision-Exp` is scoped to the
*Flash* tier and tagged experimental, which is consistent with the June
capability turn-on rather than a new base model, and consistent with
@teortaxesTex's read of it as "an okay current gen Flash" rather than a
frontier multimodal system.

**The detection path is worth recording.** The model string appeared in
DeepSeek's own Harness codebase, with native image-request adaptation
added alongside it, before any announcement — the same class of
artifact (a console entry, a routing string, a catalog commit) that has
repeatedly front-run releases in this lane. When the string and the
plumbing land together, the listing follows in hours.

**What is still missing is the part that would make the "close to Opus
4.8" claim checkable.** There is no model card, no published multimodal
benchmark, and no @deepseek_ai post. The one independent number in
circulation is a DeepSWE score used as a comparison baseline, not a
vision evaluation.

Related: [[deepseek-v4-ga-surge-pricing-2026-06]],
[[deepseek-v4-pro-price-cut-2026-05]],
[[stealth-ox-alpha-model-2026-08]].
