---
slug: zhipu-glm-5-3
title: Zhipu GLM-5.3
type: entity
aliases: ["Zhipu GLM 5.3", "GLM 5.3", "GLM-5.3", "Z.ai GLM-5.3", "GLM-5.3-Flash", "GLM-5.3 Flash"]
tags: [open-weights, china, agentic, frontier-model]
description: Zhipu AI / Z.ai's successor to GLM-5.2; open-weighted on 2026-08-29 (post-trained on the 743B GLM-5.2 base; 753B total per Baseten) with day-0 vLLM/SGLang/Baseten serving, topping Hacker News at 733 points — after scoring 60 on the Artificial Analysis Intelligence Index and shipping GLM-5.3-Flash on 2026-08-27.
created_at: 2026-08-19
timestamp: 2026-08-29T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-08-29", path: research/digest/2026-08-29-digest.md}
  - {title: "ARA model ticket — Zhipu GLM-5.3 family", path: research/models/tickets/zhipu-glm-5-3-2026-08.md}
  - {title: "ARA daily digest 2026-08-27", path: research/digest/2026-08-27-digest.md}
  - {title: "ARA daily digest 2026-08-23", path: research/digest/2026-08-23-digest.md}
  - {title: "ARA daily digest 2026-08-21", path: research/digest/2026-08-21-digest.md}
  - {title: "ARA daily digest 2026-08-20", path: research/digest/2026-08-20-digest.md}
  - {title: "ARA daily digest 2026-08-19", path: research/digest/2026-08-19-digest.md}
---

Zhipu AI / Z.ai's **GLM-5.3** is the follow-on to [[zhipu-glm-5-2]] — the same
**753B-total / 40B-active** MoE architecture with **1M-token context** as its
predecessor, but carrying the cycle's headline **agentic** gain. Its scoring is
distinct from the model itself: **Artificial Analysis published the first
independent evaluation on 2026-08-19**, and it is the day's marquee Chinese
open-weight agentic development.

## Why it matters

- **Second worldwide on agentic work (2026-08-19).** Artificial Analysis scores
  GLM-5.3 at **60 on its Intelligence Index v4.1** — **tied with
  [[moonshot-kimi-k3|Kimi K3]]** — with the load-bearing gain in agentic Elo:
  **GDPval-AA v2 jumped 1524 → 1770**, **second overall behind
  [[claude-opus-5|Claude Opus 5]] (1855)** and **more than 100 points above
  Kimi K3 (1668)**. Real-world knowledge on **AA-Omniscience moved 4 → 14**.
  Pricing is **$1.40/$4.40 per Mtok** (see [[open-weights]] for the
  open-weight price-pressure context).
- **Caveats to hold.** Z.ai claimed **~22% *fewer*** output tokens than
  GLM-5.2, but the independent harness measured **~18,700 tokens per task —
  about 20% *more***. The **hallucination rate also regressed 26% → 30%**. And
  the **MIT-licensed weights remain a promise, not a download** — "within
  a week" is still unfulfilled, the same verification gap that marked the
  GLM-5.2 arc (ARA daily digest 2026-08-19).
- **The post-training thesis and the parameter discrepancy harden (2026-08-20).**
  The day-two read sharpens the story the page opened with: founder **Jie Tang**
  frames GLM-5.3 explicitly as a **controlled experiment that capability now
  comes from post-training depth, not parameter count** — a relayed claim says
  it **reuses GLM-5.2's base and architecture with roughly one extra month of
  RL** — and the **743B-vs-753B base-parameter discrepancy is still unresolved**.
  The 60-on-the-Intelligence-Index score now reads as **tying Kimi K3 top of the
  open-model rankings and seven points ahead of GLM-5.2**, with the **weights
  release delayed** past the initial promise (ARA daily digest 2026-08-20).
- **Fourth independent frontier placement — Terminal-Bench 3.0 near Fable 5
  (2026-08-21).** A posted chart has GLM-5.3 **scoring near
  [[claude-fable-5|Fable 5]] on Terminal-Bench 3.0** — the **fourth independent
  leaderboard** placing the open-weights model **in frontier range** since its
  14 August release, reinforcing the agentic-coding claim. Separately, Z.ai
  shipped **ZCode v3.8.1**, letting **Coding Plan subscribers reset five-hour
  usage limits off-peak** — a **load-shifting mechanism rather than a quota
  increase** (ARA daily digest 2026-08-21).
- **KernelBench-Mega: 21.4× the optimized baseline — and GLM-5.2 fails the same
  gate (2026-08-23).** A private-harness benchmark (@elliotarledge) has **GLM-5.3
  posting 21.4× the optimized PyTorch baseline on KernelBench-Mega**
  (Kimi-Linear Decode, RTX PRO 6000), against **11.1× for GLM-5.2 — which also
  failed the single-launch gate GLM-5.3 clears**. On the same evaluator's ladder
  GLM-5.3 **ranks second, behind [[claude-fable-5|Fable 5]] at 24.6× and ahead
  of [[moonshot-kimi-k3|Kimi K3]] at 18.1× and [[claude-opus-4-8|Opus 4.8]] at
  14.4×** — an efficiency read consistent with the post-training-depth thesis on
  this page. Single private harness, **unreproduced** (ARA daily digest
  2026-08-23).

## Open questions

- **Do independent evals confirm the Terminal-Bench 4.0 screenshot?** The
  relayed claim that GLM-5.3 (max) beats [[gpt-5-6|GPT-5.6 Sol]] (max) is
  single-source and unverified in the 2026-08-29 digest.
- **Does the agentic Elo transfer outside the harness?** The +246 Elo swing is
  on one benchmark; whether it holds on contamination-aware agentic and coding
  tasks is unverified.
- **Where does it sit in Z.ai's product ladder?** A distinct model from
  [[zhipu-glm-5-2]] — does it replace it as the flagship, or coexist as the
  agentic tier? The Flash sibling is already the computer-use favorite.

## GLM-5.3-Flash ships, and Z.ai confirms Ox Alpha (2026-08-27)

- **GLM-5.3-Flash is the day's top Hacker News item (2026-08-27).** Z.ai shipped
  **GLM-5.3-Flash** at **$0.25 per million output tokens** — the day's runaway
  HN thread (824 points / 414 comments) debating its speed, distillation from
  GLM-5.2, and pricing. An independent test reports **881 tok/s at 64-way
  concurrency, untuned on 2×DGX Station**, and **232 tok/s single-stream, with
  vision support** (@theo, @alecqfong; ARA daily digest 2026-08-27). The
  flash-tier speed/pricing echo of the flagship's post-training-depth thesis
  keeps the agentic positioning consistent across the family.
- **Z.ai confirms it is behind Ox Alpha — the stealth line resolves (2026-08-27).**
  Z.ai stated it is the **lab behind [[ox-alpha]]**, the unattributed model that
  topped leaderboards while unclaimed, with **weights said to be released soon**.
  This converts what this page's earlier ticket read as the "open question" of
  whether Ox Alpha is a GLM-5.3-Flash variant into a confirmed family launch —
  the unattributed model is a **Z.ai GLM variant**, and the flagship/Flash pair
  is now on the record (TechCrunch; ARA daily digest 2026-08-27). See
  [[ox-alpha]] and [[open-weights]].

## Flagship weights land — the promised download arrives (2026-08-29)

- **Z.ai published download weights for GLM-5.3 (2026-08-29).** The
  flagship — described as the lab's most capable **agentic coding and
  cyber-defense** model, **post-trained on the 743B [[zhipu-glm-5-2|GLM-5.2]]
  base** (753B total parameters per Baseten's Philip Kiely) — is now a
  download, with **day-0 serving on vLLM, SGLang and Baseten** (1M
  context, **US-only, ZDR**). This closes the "weights remain a promise"
  gap this page has carried since 2026-08-19 and matches the model
  ticket's 2026-08-27 trigger ("GLM-5.3's weights will be released
  tomorrow"). The release was the day's **biggest AI Hacker News
  thread at 733 points / 245 comments** (Z.ai, Hugging Face, Hacker
  News; ARA daily digest 2026-08-29). See [[open-weights]] and
  [[hugging-face]].
- **Same-evening local path: Unsloth 2-bit GGUF (2026-08-29).** Unsloth
  shipped **2-bit GGUF quants the same evening** — **239GB, ~81%
  accuracy retained, runs on a 256GB Mac**. Practitioners separately
  flagged the smaller **GLM-5.3 Flash** as unusually good for computer
  use (Hugging Face, X; ARA daily digest 2026-08-29).
- **Unverified Terminal-Bench 4.0 screenshot (2026-08-29).** A relayed
  screenshot claiming **GLM-5.3 (max) beats [[gpt-5-6|GPT-5.6 Sol]]
  (max) on Terminal-Bench 4.0** is **single-source and unverified** —
  the digest's coverage note flags it explicitly (X; ARA daily digest
  2026-08-29).
- **Offensive-cyber caveat from Ethan Mollick (2026-08-29).** Mollick
  flagged that GLM-5.3 **ships considerable offensive cyber capability
  with effectively no guardrails** — the open-weights counterpart to
  the [[agentic-ai-security]] story this cycle has been tracking on
  gated frontier models (Bluesky; ARA daily digest 2026-08-29).
