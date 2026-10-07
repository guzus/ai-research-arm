---
slug: mistral
title: Mistral AI
type: entity
aliases: ["Mistral", "Mistral AI", "Firefox Smart Window"]
tags: [frontier-lab, europe, open-weights, foundation-models, funding]
description: European frontier lab; launched Large 4 (1T / 49B-active multimodal MoE) with API access now and open weights promised for end of October.
created_at: 2026-09-09
timestamp: 2026-10-07T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-10-07", path: research/digest/2026-10-07-digest.md}
  - {title: "ARA model ticket — Mistral Large 4", path: research/models/tickets/mistral-large-4-2026-10.md}
  - {title: "ARA daily digest 2026-10-04", path: research/digest/2026-10-04-digest.md}
  - {title: "ARA daily digest 2026-09-17", path: research/digest/2026-09-17-digest.md}
  - {title: "ARA model ticket — Mistral × Mozilla partnership", path: research/models/tickets/mistral-mozilla-partnership-2026-09.md}
  - {title: "ARA daily digest 2026-09-09", path: research/digest/2026-09-09-digest.md}
---

**Mistral AI** is the European frontier lab behind the Mistral / Mixtral
model line and a cluster of open-weight specialist models —
[[mistral-leanstral-1-5|Leanstral 1.5]] (Lean 4 formal verification),
[[mistral-robostral-navigate|Robostral Navigate]] (embodied navigation),
and [[mistral-shieldstral|Shieldstral]] (3B multimodal moderation). This
page is the company; those pages stay the shipping artifacts.

## Why it matters

- **€3B Series D at more than €21B post-money (2026-09-09).** Samsung
  Electronics led; EQT's Scaleup Europe Fund and PSG Equity co-led;
  **ASML, [[nvidia|Nvidia]], a16z, BlackRock-managed funds and
  [[salesforce|Salesforce]] Ventures** participated. Mistral calls it
  **Europe's largest-ever equity round**. The HN thread peaked at
  **774 points / 553 comments** before the [[openai]] Navier–Stokes
  cluster displaced it. First-party plus TechCrunch / The Decoder
  (ARA daily digest 2026-09-09).
- **The round is paired with an on-premises deployment inside
  Samsung's semiconductor operations.** That is a customer
  relationship, not just a cap table entry — the lead investor is
  also putting the models on the factory floor. Dollar/euro
  contract value for the deployment was not disclosed.
- **It is the missing company node for three existing product
  pages.** Until this ingest, [[mistral-leanstral-1-5]],
  [[mistral-robostral-navigate]] and [[mistral-shieldstral]] had no
  maker page to resolve to. See [[open-weights]] and [[ai-capex]].

## Open questions

- **Does "Europe's largest-ever equity round" survive a
  like-for-like check?** It is Mistral's own framing; the digest
  does not adjudicate against other European tech rounds.
- **What does the Samsung on-prem deployment actually run** — a
  general Mistral model, a semiconductor-tuned stack, or air-gapped
  inference only?
- **How much of the €21B+ is cash vs. strategic-investor
  optionality?** ASML / Nvidia / Samsung sitting in the same round
  is a supply-chain syndicate as much as a growth round.

## Firefox Smart Window on Mistral (2026-09-17)

- **Mozilla shipped Firefox Smart Window in beta in
  France and North America**, with the UK and
  Germany later this year. Mozilla says
  conversations are not saved on its servers by
  default; Mistral agrees to **zero data
  retention**. Firefox is the last major browser not
  owned by a frontier lab, but it is still
  **low-single-digit share**, and **neither party
  named the models or an on-device split**. The
  partnership itself was announced first-party on
  2026-09-16; today's digest supplies the product
  name and the geography. Commenters treated the
  assistant as a **provider slot, not a new model**
  — it became the #2 HN story at **509 points**
  after Jev exited. See [[eu-ai-regulation]]
  (Mistral, Mozilla, HN; ARA daily digest
  2026-09-17 and model ticket
  mistral-mozilla-partnership-2026-09).

## Aleph Alpha returns to training (2026-10-04)

[[aleph-alpha|Aleph Alpha]] shipped Kolibri-1
(78.1B / 3.46B-active, Apache 2.0, validated to
1M context), a European open-weight return to
training from a lab that had pivoted to
enterprise tooling. It is a peer observation
on the same sovereign-deployment buyer Mistral
has been chasing, not a bake-off. See
[[open-weights]] and [[soofi-s-30b-a3b]] (ARA
daily digest 2026-10-04).

## Large 4 ships as a trillion-parameter preview (2026-10-07)

- **[[mistral-large-4|Mistral Large 4]]
  ("Le Chonk") is live on the API**:
  a natively multimodal MoE at **1T /
  49B active** (blog) or **1.05T /
  52B** plus a 1.6B vision encoder
  and 1M context (docs). Open weights
  are promised for the end of
  October; Lample says the RL run is
  still in flight. Launch prices are
  **$1.36 / $4.18** per Mtok. Mistral
  pitches it at cybersecurity work
  that closed US models refuse
  (CyberGym-E2E **82%**;
  [[claude-opus-5-5|Opus 5.5]] and
  [[gpt-6|GPT-6 Astra]] score near
  zero because they refuse).
  Artificial Analysis places it 6th
  among open-weight models. It led
  HN at **1,543 / 944**. This is the
  first product the €3B Series D
  paid for. See [[open-weights]] and
  [[agentic-ai-security]] (Mistral,
  TechCrunch, The Decoder, Hacker
  News; ARA daily digest 2026-10-07
  and ticket `mistral-large-4-2026-10`).
