---
slug: deepseek
title: DeepSeek
type: entity
aliases: [DeepSeek, "DeepSeek AI", "深度求索", "DeepSeek-V4", "DeepSeek V4 Pro", "Liang Wenfeng"]
tags: [frontier-lab, chinese-llm, open-weights, foundation-models, commercialization]
description: Hangzhou-based Chinese frontier lab; closed its first-ever external round (~$7.4B / ~50B yuan at a $50B+ valuation, the largest in Chinese AI history) on 2026-06-18 — founder-controlled, vote-less capital from Tencent + CATL, with the state AI fund the only voting investor — pivoting to commercialization toward AGI, and shipped V4 Pro's repriced card on 2026-08-18.
created_at: 2026-06-04
timestamp: 2026-08-18T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-18", path: research/digest/2026-08-18-digest.md}
  - {title: "ARA daily digest 2026-08-13", path: research/digest/2026-08-13-digest.md}
  - {title: "ARA daily digest 2026-08-02", path: research/digest/2026-08-02-digest.md}
  - {title: "ARA daily digest 2026-08-01", path: research/digest/2026-08-01-digest.md}
  - {title: "ARA model ticket — DeepSeek V4 GA + surge pricing", path: research/models/tickets/deepseek-v4-ga-surge-pricing-2026-06.md}
  - {title: "ARA daily digest 2026-07-27", path: research/digest/2026-07-27-digest.md}
  - {title: "ARA model ticket — DeepSeek second funding round", path: research/models/tickets/deepseek-second-round-2026-07.md}
  - {title: "ARA daily digest 2026-06-30", path: research/digest/2026-06-30-digest.md}
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

- **V4 dated for mid-July GA — with the first major LLM API surge pricing
  (2026-06-30).** DeepSeek emailed API users that **V4-Pro and V4-Flash** (~1M
  context) leave preview **mid-July**, paired with the first major LLM
  **time-of-day demand pricing**: **peak hours cost ~2× off-peak** (reported as
  ~9:00–12:00 and 14:00–18:00 Beijing time; exact windows still diverge across
  reposters). V4-Flash is already in wide use, so "V4" here means **full GA**. The
  surge-pricing move is a notable inversion of DeepSeek's flat-low-price reputation —
  a demand-management lever on the inference base it has spent the [[ai-capex]]
  buildout trying to capture. Separately, a single-sourced practitioner claim says
  DeepSeek's **"DSpark" speculative decoding** beats DFlash and EAGLE-3 on AMD MI300X
  (avg ~127 tok/s vs 111/81; +20% acceptance length). *(Watch the official pricing
  page for exact windows/rates.)* See [[open-weights]] (ARA digest 2026-06-30).

- **A second funding round, then a pause after a leaked compute-gap admission
  (2026-07-16 → 2026-07-27).** Weeks after the June round closed, Bloomberg
  reported DeepSeek preparing a **second, distinct round of up to $7.4B**,
  targeting overseas (Middle East) dollar capital and a **~$71-74B
  valuation**, as part of a push toward a mainland China **STAR Market IPO**
  by 2027 — up from the ~$66.6B post-money valuation of the first round.
  *The Information's* separate "tenfold valuation increase" claim could not
  be reconciled with this figure and is treated as an unverified outlier.
  On **2026-07-26/27**, a **leaked investor-meeting transcript** had founder
  **Liang Wenfeng** reportedly acknowledging DeepSeek **still relies heavily
  on Nvidia chips** and that **China trails the US in capability** — an
  unusually candid admission from the lab whose open-weights releases have
  anchored the "China is closing the gap" narrative on [[open-weights]]. The
  round has reportedly been **paused before investors signed new
  agreements**, with investors unsettled by the leak. See the
  [DeepSeek second-round ticket](../../models/tickets/deepseek-second-round-2026-07.md)
  (ARA digest 2026-07-27).

- **V4-Flash GA, then the weights — the surge-pricing arc lands as an MIT
  release (2026-07-31, digested 2026-08-01).** The mid-July GA promised in
  June arrived a fortnight late and in two steps on the same day: the
  **[[deepseek-v4-flash|V4-Flash-0731]] official API went live in public
  beta** at **$0.28 input / $0.87 output per Mtok** with heavily upgraded
  agent capability, native Responses-API support and Codex adaptation — and
  **hours later DeepSeek released the weights on Hugging Face under MIT**
  with a technical report. Artificial Analysis scored it **50 on its
  intelligence index, one point behind [[gpt-5-6|GPT-5.6 Luna]] at roughly
  60% lower cost per task**; it held the top Hacker News AI slot across
  three consecutive front-page snapshots, peaking at 652 points. Two things
  are worth separating from the launch noise: the conflicting
  ~$0.14/$0.28 vs $0.28/$0.87 rate-card relays from July 31 resolve to the
  higher pair in the digest, and the **June surge-pricing scheme is not
  evidenced as live** on this GA. Strategically the release re-anchors
  [[open-weights]] — the cheapest near-frontier model of the cycle is now
  downloadable, days after [[moonshot-kimi-k3|Kimi K3]] made the same move
  at 2.8T parameters (ARA digest 2026-08-01).

- **Its first self-owned hyperscaler-scale site: a 1GW campus in Inner
  Mongolia (2026-08-02).** Bloomberg reports DeepSeek is **building a
  1-gigawatt datacenter campus in Inner Mongolia**, its **first
  self-owned site at hyperscaler scale**, with part of the capacity
  targeted for **late 2027 or early 2028**. That is a structural change in
  posture: the lab that built its reputation on training-efficiency under
  export controls is now buying its own power envelope, the same move the US
  hyperscalers are making inside [[ai-capex]]. **Which accelerators fill the
  racks is the part nobody will confirm** — the whole export-control question
  sits in that gap (Bloomberg via @rohanpaul_ai; **single-source in window**).
  Same cycle, [[deepseek-v4-flash|V4-Flash]] kept clearing outside tests and
  was relayed as **105× cheaper per task than [[claude-fable-5|Fable 5]]**
  (ARA digest 2026-08-02).

- **V4-Pro-0813 lands on the API — and the cheap sibling outperforms it on a
  friendly test (2026-08-13).** DeepSeek listed **`DeepSeek-V4-Pro-0813`** on
  its own API documentation page at **$0.435 input / $0.87 output per million
  tokens** at **1M context** — roughly **4.5× the cost of the
  [[deepseek-v4-flash|V4 Flash 0731]]** — confirmed across two independent
  readings. SemiAnalysis put the parameter count at **1.5T**; a competing
  relay says **1.6T with 49B active**. There is **no official model card**;
  circulating benchmark tables come from **WeChat screenshots comparing
  against [[claude-opus-4-8|Claude Opus 4.8]] rather than
  [[claude-opus-5|Opus 5]]**. Within two hours, @teortaxesTex — a
  consistently pro-DeepSeek analyst — reported the cheaper V4 Flash 0731
  outperforming it on his own tasks, calling the release evidence that
  **"they need more than scale"** (ARA digest 2026-08-13).

- **V4 Pro's repriced card goes live — peak/off-peak tiering (2026-08-18).**
  DeepSeek's V4 Pro now charges **$1.32/M input and $3.96/M output at peak,
  exactly half off-peak**, with **cached input as low as $0.022/M**. The peak
  windows are **01:00–04:00 and 06:00–10:00 UTC** — the Chinese working day
  with the lunch break cut out — so **US-hours developers pay off-peak by
  default**. V4 Pro also ships **native Responses API support**, **1M-token
  context with up to 384K output**, and **reasoning-effort controls currently
  exposing only high and max**. Independent **WeirdML** scoring (benchmark
  author @htihle) puts **V4 Pro 0813 at maximum reasoning at 66.2% against
  63.0% for the cheaper [[deepseek-v4-flash|V4 Flash 0731]]** — the premium
  tier buys about **3.2 points** — with @teortaxesTex, a consistently
  DeepSeek-favorable analyst, calling it **"functionally Flash."** VentureBeat
  framed the API change as prices "up to **1,100%**" higher, a figure nobody
  has tied to a named line item and which is **inconsistent with the
  published per-Mtok rates** (which make even the cheapest output rate 2.28x
  last week's). Treat the surge-style peak/off-peak scheme as the long-flagged
  pricing lever finally going live; see the earlier June surge-pricing entry
  above (ARA digest 2026-08-18).

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
