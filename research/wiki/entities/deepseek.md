---
slug: deepseek
title: DeepSeek
type: entity
aliases: [DeepSeek, "DeepSeek AI", "深度求索", "DeepSeek-V4", "DeepSeek V4 Pro", "Liang Wenfeng"]
tags: [frontier-lab, chinese-llm, open-weights, foundation-models, commercialization]
description: Hangzhou-based Chinese frontier lab; closed its first-ever external round (~$7.4B / ~50B yuan at a $50B+ valuation, the largest in Chinese AI history) on 2026-06-18 — founder-controlled, vote-less capital from Tencent + CATL, with the state AI fund the only voting investor — marking its pivot from research to commercialization toward AGI.
created_at: 2026-06-04
timestamp: 2026-06-29T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-06-29", path: research/digest/2026-06-29-digest.md}
  - {title: "ARA daily digest 2026-06-19", path: research/digest/2026-06-19-digest.md}
  - {title: "ARA daily digest 2026-06-18", path: research/digest/2026-06-18-digest.md}
  - {title: "ARA daily digest 2026-06-05", path: research/digest/2026-06-05-digest.md}
  - {title: "ARA daily digest 2026-06-04", path: research/digest/2026-06-04-digest.md}
  - {title: "ARA model ticket — DeepSeek funding round", path: research/models/tickets/deepseek-funding-round-2026-05.md}
  - {title: "ARA model ticket — DeepSeek V4 Pro price cut", path: research/models/tickets/deepseek-v4-pro-price-cut-2026-05.md}
  - {title: "The Information — DeepSeek seeks $7.35B funding round", url: "https://www.theinformation.com/articles/deepseek-seeks-7-35-billion-funding-round", date: 2026-05-25}
---

DeepSeek (深度求索) is the Hangzhou-based Chinese frontier lab founded by
**Liang Wenfeng**, known for shipping high-capability open-weights models at
aggressive price points. For most of its life it operated as a
research-focused, self-funded operation (backed by Liang's quant fund
High-Flyer); the 2026-06-04 cycle marks its decisive pivot to
**commercialization** — the first time it has taken outside capital.

## Why it matters

- **First-ever external round (2026-06-04).** DeepSeek disclosed a round of
  **~50B yuan (~$7.4B) at up to a $59B valuation**, with **Tencent and CATL
  as the largest outside investors**, NetEase participating, and founder
  **Liang Wenfeng reportedly contributing personally**. The print resolves a
  ~$7–13B raise cluster that had circulated since mid-May (see the
  [DeepSeek funding-round ticket](../../models/tickets/deepseek-funding-round-2026-05.md));
  the long-running ">$50B" shorthand was always the *valuation*, not the round
  size. *(Reuters/CNBC/Jiemian multi-source; valuation is a ceiling, round
  still finalizing.)*
- **Commercialization under compute-cost pressure.** The raise lands alongside
  aggressive API price moves: a permanent V4-Pro price cut in late May, and on
  2026-06-04 **Tencent Cloud cutting DeepSeek-V4 API pricing up to 97.5%**.
  Read together, the capital and the pricing describe a single strategy —
  funding cheap, broadly-deployed inference to capture share, the demand-side
  mirror of the [[ai-capex]] buildout.
- **Open-weights pressure.** DeepSeek anchors the Chinese open-weights wave
  alongside peers like [[minimax-m3]], Google's [[gemma-4]], and Alibaba's Qwen line — capable
  downloadable models that compress closed-API pricing and expand the
  inference base routed through layers like [[openrouter]].

- **The "filing would make it real" critique (2026-06-05).** A day later the
  round was still **anonymously sourced** — no DeepSeek, Tencent, or CATL
  primary or filing — even as it was bundled into the day's wall-to-wall
  AI-financing headlines alongside [[spacex|SpaceX's]] *filed* prospectus and
  Alphabet's *oversubscribed* convertible. The digest's Quote of the Day
  (@Signal8Ai) made DeepSeek the cleanest case study in financing discipline:
  "no press release. no S-1. no filing of any kind. $59B valuation built
  entirely on what unnamed insiders told a reporter… the $7B is real until it
  isn't. the filing would make it real. there isn't one." The contrast with the
  same week's hard SEC filings is the point (ARA digest 2026-06-05).

- **The round closes — founder-controlled, vote-less capital (2026-06-18).** The
  "filing would make it real" critique was answered: per *The Information*,
  DeepSeek **closed its first-ever external round at roughly RMB 50B (~$7.4B) at a
  $50B+ valuation**, with founder **Liang Wenfeng writing the biggest check
  (~$2.8B)**, **Tencent ~$1.4B**, and **CATL ~$700M**. The decisive structural
  detail: **investors received *no voting rights*** and capital flowed into a
  **founder-controlled LP** — Liang kept hard control while raising the largest
  Chinese-AI round of the cycle. It landed the same day frontier-lab CEOs sat with
  the Trump administration over the [[claude-fable-5|Fable 5 / Mythos 5]] export
  embargo, sharpening the "China's open frontier ascends as America embargoes its
  own" frame (see [[open-weights]] and [[federal-ai-policy]]).
- **US declines to blacklist DeepSeek (2026-06-18).** Reuters reported Washington
  **held off adding DeepSeek to the entity list** as part of a broader review of
  100+ Chinese firms deemed security risks — the policy counterpoint to the
  megaround, and a notable restraint given the parallel Fable 5 export crackdown.
  Separately, **Microsoft is reportedly evaluating a fine-tuned DeepSeek V4** as a
  cheaper [[microsoft|Copilot Cowork]] tier than [[openai]] or [[anthropic]] — a
  Western hyperscaler treating DeepSeek's open weights as a production backend.

- **DeepSeek introduces Vision — going multimodal (2026-06-19).** DeepSeek added
  **multimodal Vision** capability, its most significant capability expansion
  since V4, reigniting the open-weight-vs-closed-frontier debate (HN: 432 pts,
  176 comments). Combined with the closed [[claude-fable-5|Fable 5]] embargo and
  [[zhipu-glm-5-2|GLM-5.2]] topping the open-weights board, it extends the Chinese
  open-weights wave from text into modality — see [[open-weights]] (ARA digest
  2026-06-19).

- **The round is the largest in Chinese AI history — and a state-directed read
  hardens (2026-06-29).** The 2026-06-18 close is now framed as the **largest
  external round in Chinese AI history**: **>¥50B (~$7.4B) at a post-money
  valuation exceeding $50B**, with founder **Liang Wenfeng** personally in
  **~$3B** (the single largest check, retaining voting control), **Tencent
  ~$1.5B**, **CATL ~$740M**, and NetEase / JD.com / IDG Capital among the
  backers. The decisive structural tell: most outside investors got **no voting
  rights and a five-year lock-up**; only the state-backed **National AI Industry
  Investment Fund** took **direct equity with voting rights and no lock-up**.
  Reporting frames [[anthropic|Anthropic's]] Mythos preview as the catalyst that
  convinced Liang the lab needed far more capital; the lab plans to **double
  every department** toward AGI. The counter-read: $50B for a discount-API lab is
  rich by public-market standards, and the structure reads more like a
  **state-directed capital injection with a commercial veneer** than a
  market-priced round — notably **`@deepseek_ai` has not tweeted since May 22**,
  so all detail remains The Information-sourced with no DeepSeek primary (ARA
  digest 2026-06-29).

## Open questions

- **Does the round close at the reported size/valuation?** Reported-closed at
  ~$7.4B / $50B+ (The Information, 2026-06-18), now framed as the largest in
  Chinese AI history — but still no DeepSeek primary statement or filing, and
  the official @deepseek_ai account has been silent since May 22.
- **What does outside capital do to the open-weights posture?** Tencent/CATL
  involvement and a commercialization mandate could pull DeepSeek toward more
  gated or monetized releases over time.
- **Strategic-investor logic.** CATL (a battery maker) as a lead outside
  investor is unusual; the bet reads as energy/compute-adjacent rather than
  product-strategic.
