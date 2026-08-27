---
slug: stealth-ox-alpha-model-2026-08
title: "\"Ox Alpha\" — stealth frontier model on OpenRouter, revealed as Zhipu GLM-5.3-Flash"
company: Zhipu AI / Z.ai (revealed 2026-08-26; opened as unattributed)
model: Ox Alpha (= GLM-5.3-Flash)
status: closed
status_note: |
  A stealth model shipped as **`stealth/ox-alpha`** on **OpenRouter**
  around **2026-08-20** and is free to use through OpenRouter, opencode,
  Hermes Agent (**@Teknium**, 2026-08-21: "Ox Alpha now available in
  Hermes Agent through @opencode and @OpenRouter"; **@NousResearch**
  offering it free "for a limited time… capacity for 1 quadrillion tokens
  per day"), and Cursor. **No lab has claimed it**, which is why this is
  its own ticket rather than an update to a named-model ticket.

  **What is actually established, from firsthand testers:** it is a
  **long-horizon, multimodal model with a 1M context window**
  (@AndrewCurran_, 2026-08-21). @davis7 ran the **full 113-task DeepSWE
  benchmark** and landed at **~63%**, explicitly retracting his own
  earlier ~80% subset figure ("Ended at ~63% NOT the 80% my first subset
  test got, which makes way more sense"). He rates it "on around Sol
  medium", praising voice, design, subagent handling and long complex
  work, and faulting leftover dead code and slow wall-clock at high
  reasoning effort. @teortaxesTex independently reads a 58.4 DeepSWE and
  calls it "a very good subagent"; @kimmonismus relays parity with
  GPT-5.6 Sol mid.

  **Attribution is contested and remains unverified.** @davis7 is "99%
  sure it's GLM-5.x — same video encoder, same tokenizer, style matches,
  same audio rejection"; @kimmonismus and @synthwavedd say GLM-5.3 Flash;
  @AndrewCurran_'s canvass lands on "a new Flash model in the GLM family
  from Z.ai, possibly a smaller variant of the new flagship large model
  they are still training… I'm assuming it will be open-weight."
  **@mark_k asserts the opposite** — "Ox Alpha is a Gemini model by
  @GoogleDeepMind" — and **@teortaxesTex argues against the Cursor
  hypothesis on training grounds** ("why would Cursor post-train vision?
  Why would Cursor expose full CoTs?"). No lab post, model card, or
  pricing exists.

  **Dissent on the capability claim is on the record too**, and should
  not be smoothed over: @emollick ("Nice model, but not frontier and I am
  not sure why there has been so much buzz as if it is") and
  @iruletheworldmo ("don't fall for this ox alpha campaign") both tested
  it and came away unimpressed.

  **2026-08-24 — a full day later, still nobody has claimed it, and the
  speculation has turned into a joke about itself.** The signal moved
  from testing to meta-commentary: @iruletheworldmo — who two days ago
  said "don't fall for this ox alpha campaign" — posted an elaborate
  pseudo-architecture ("recursively updates a persistent latent state
  instead of reasoning entirely through tokens... attractors generate
  shards... metaparameters that dynamically alter the residual geometry
  without changing its weights"), and @teortaxesTex answered with open
  parody of the guessing game ("a Sarvam-Google colab, on a GLM base,
  with Google helping on vision, Nvidia providing hardware and safety
  finetuning from SSI. duh"). **Neither is evidence and neither is
  recorded here as a capability claim.** Two genuinely new hypotheses
  did appear, both unsupported: @simonepaciaroni suspects an
  **Anthropic** experiment on a "telltale marker," and @Norwakar claims
  it is **xAI's unreleased Grok 4.7** being pre-release tested. Both are
  single low-engagement accounts with no artifact; the GLM-family
  reading from firsthand testers on 2026-08-23 remains the
  best-supported one. Coverage did widen — trade aggregators are now
  writing it up as "a mysterious new AI model... no maker attached."
  Status stays `in-testing`, verification stays `partial`: another cycle
  with **no lab claim, no model card, no pricing, no weights**.

  **2026-08-25 — the usage data arrived, and it is the largest number on
  this ticket.** @OpenRouter: "**Ox Alpha is on track to hit nearly 6
  trillion tokens today**," and @rohanpaul_ai reports the cumulative
  figure — **11.6T tokens in three days, 2.6x OpenRouter's previous
  biggest model launch** — with context now stated precisely as
  **1.05M tokens**. A trending item ("Ox Alpha Tops OpenRouter Rankings in
  Record Debut," ~760 posts) confirms the ranking independently of the
  router's own post. **This is the first hard, third-party-measured fact
  on the ticket**: unlike capability impressions, token throughput is
  metered by the venue serving it. The caveat is that the model is
  **free**, so volume measures demand at zero price, and @rohanpaul_ai's
  own framing is that agentic loops (long contexts, retries, repeated tool
  calls) multiply consumption per task.

  **A first quantitative negative also landed.** @patience_cave's
  MazeBench run scores **ox-alpha 0%**, alongside **grok 4.6 0%,
  glm-5.3 0%, qwen 3.8-max 0%**, with **gemini 3.7 flash at 1%** the only
  non-zero. Read narrowly: a benchmark on which nearly every frontier
  model scores zero discriminates almost nothing, and its main use here is
  that it does **not** separate ox-alpha from GLM-5.3 — consistent with,
  but not evidence for, the GLM-family hypothesis.

  **Attribution moved from vibes to a priced market, weakly.**
  @nicbstme reports the model is from **@Zai_org per a current prediction
  market** while flagging **low volume**, and @teortaxesTex adds the
  adversarial read that insiders have an incentive to *misdirect* before
  betting ("convince everyone else it's not GLM but
  Gemini/Cursor/Sarvam/SSI before making a bet"). A thin market is not a
  source; recorded as the state of speculation. Separately @teortaxesTex,
  reading @sam_paech's slop-profile comparison, argues DeepSeek has fallen
  behind on internal RL and that "**the gap between 0731 and ox-alpha is
  Opus-shaped**" — an inference from output-style clustering, not an
  attribution.

  Six days in: **still no lab claim, no model card, no pricing, no
  weights.** Status stays `in-testing`; verification stays `partial`.

  **2026-08-26/27 — RESOLVED, and the ticket closes.** Z.ai claimed it on
  the record. **@Zai_org**: "Introducing **GLM-5.3-Flash** — Leading
  capabilities at a highly competitive price — Natively multimodal with a
  **1M-token context window** — A **320B-A18B** model released under the
  **MIT License** — **Previously previewed as Ox Alpha**, running entirely
  on Chinese AI chips." **@OpenRouter** confirmed from the venue side:
  "**Ox Alpha revealed: @Zai_org's GLM-5.3-Flash**… Ox Alpha was **the
  biggest model ever on OpenRouter, processing over 20 trillion tokens in
  6 days**," and @Teknium noted "Ox Alpha free period is over, but GLM-5.3
  Flash is now available." @louszbd (Zhipu-side) made the framing
  explicit: "**Ox Alpha put GLM-5.3-Flash in more people's hands.** We've
  read every piece of feedback. The model you're using now is better."

  That settles every open question this ticket was carrying. The
  attribution the firsthand testers reached on 2026-08-23 — @davis7's
  shared video encoder, tokenizer, output style and audio-rejection
  evidence, @kimmonismus's and @synthwavedd's specific "GLM-5.3 Flash"
  call, @AndrewCurran_'s "a Z.ai GLM Flash variant, possibly a smaller
  variant of the new flagship" — **was correct in full, including the
  Flash sizing**. @mark_k's Google DeepMind attribution, and the
  Anthropic / Grok 4.7 / Cursor / Sarvam hypotheses, were **wrong**.
  @rasbt's teardown supplies the architecture the guessing game never
  got at: a **Kimi Linear-style 3:1 hybrid attention** (34 Kimi Delta
  Attention layers + 11 MLA/DeepSeek-Sparse-Attention layers), a
  scaled-down GLM-5.2 sparse MoE backbone (744B-A40B → **320B-A18B**), a
  **DeepSeek-V4-style mHC residual path with four parallel streams**, and
  a native vision encoder.

  **The one fact nobody predicted is the serving substrate, and it is the
  real story.** @SemiAnalysis_: "Ox Alpha has been unveiled as
  GLM-5.3-Flash, but **what's shocking is that the 100T tokens per day is
  served on Chinese chips**… **ALL traffic was served on Chinese chips,
  attaining hardware efficiency and per-token cost comparable to Nvidia
  GPUs.** The CUDA moat is being tested once again." @teortaxesTex adds
  the sharpening detail that this was **not even the current generation**
  of domestic silicon in mass production.

  Closing `superseded-by: zhipu-glm-5-3-2026-08`. This ticket's entire
  premise — an artifact with **no vendor** — is contradicted by a
  first-party vendor claim, and the successor already tracks the GLM-5.3
  family. All further GLM-5.3-Flash signal (weights, pricing, benchmarks,
  the domestic-silicon serving thread) belongs there.
expected: "Resolved 2026-08-26: Ox Alpha is Zhipu/Z.ai's GLM-5.3-Flash — 320B-A18B, natively multimodal, 1M context, MIT license, first-party claimed by @Zai_org and independently confirmed by @OpenRouter, which recorded it as the biggest model ever on the router at 20T+ tokens in 6 days. Nothing further is pending on this ticket; it closes into [[zhipu-glm-5-3-2026-08]]"
labels:
  - stealth-model
  - frontier-model
  - openrouter
  - resolved
  - closed
verification: confirmed
sources:
  - "@davis7"
  - "@teortaxesTex"
  - "@kimmonismus"
  - "@AndrewCurran_"
  - "@Teknium"
  - "@mark_k"
  - "@emollick"
  - "@iruletheworldmo"
  - "@scaling01"
  - "@simonepaciaroni"
  - "@Norwakar"
  - "@OpenRouter"
  - "@rohanpaul_ai"
  - "@patience_cave"
  - "@nicbstme"
  - "@spark_arena"
  - "@elliotarledge"
  - "@LottoLabs"
  - "@Zai_org"
  - "@OpenRouter"
  - "@louszbd"
  - "@rasbt"
  - "@SemiAnalysis_"
  - "@Teknium"
  - https://x.com/SemiAnalysis_/status/2092623833630998556
created_at: 2026-08-23
updated_at: 2026-08-27
closed_at: 2026-08-27
closed_reason: superseded-by:zhipu-glm-5-3-2026-08
history:
  - ts: 2026-08-23
    change: "Created — an unattributed stealth model shipping as stealth/ox-alpha on OpenRouter since ~2026-08-20, free via OpenRouter, opencode, Hermes Agent (@Teknium, @NousResearch) and Cursor. Established by firsthand testers: long-horizon multimodal, 1M context (@AndrewCurran_); ~63% on the full 113-task DeepSWE run (@davis7, who publicly retracted his own earlier ~80% subset number), 58.4 read independently by @teortaxesTex, roughly GPT-5.6 Sol mid class. Attribution unresolved: @davis7 99% GLM-5.x on encoder/tokenizer/style evidence, @kimmonismus and @synthwavedd say GLM-5.3 Flash, @AndrewCurran_ canvass lands on a Z.ai GLM Flash variant, but @mark_k claims Google DeepMind and @teortaxesTex argues against Cursor. Capability claim itself is contested — @emollick and @iruletheworldmo both tested it and rate it non-frontier. Status in-testing (real, publicly usable artifact under a stealth alias, no vendor claim); verification partial (many independent firsthand runs establish the artifact; no primary source establishes who made it)."
  - ts: 2026-08-24
    change: "Another cycle with no attribution progress: still no lab claim, model card, pricing, or weights. Speculation turned reflexive — @iruletheworldmo posted an elaborate pseudo-architecture (persistent latent state, attractors, shards, metaparameters) and @teortaxesTex answered with open parody of the guessing game; neither is recorded as evidence. Two new unsupported hypotheses appeared from single low-engagement accounts: an Anthropic experiment (@simonepaciaroni, on a claimed telltale marker) and xAI's unreleased Grok 4.7 in pre-release testing (@Norwakar). The GLM-family reading from 2026-08-23 firsthand testers remains best-supported. Trade aggregators began covering it as an unclaimed mystery model. Status stays in-testing; verification stays partial."
  - ts: 2026-08-25
    change: "First hard third-party-measured fact lands, and it is large: @OpenRouter says Ox Alpha was on track for nearly 6T tokens in a single day, and @rohanpaul_ai reports 11.6T tokens across three days — 2.6x OpenRouter's previous biggest model launch — with context now stated as 1.05M. A trending item ('Ox Alpha Tops OpenRouter Rankings in Record Debut', ~760 posts) confirms the ranking independently of the router. Caveat recorded: the model is free, so the volume measures demand at zero price, and agentic loops multiply per-task consumption. First quantitative negative also landed — @patience_cave's MazeBench scores ox-alpha 0%, alongside grok 4.6, glm-5.3 and qwen 3.8-max all at 0%, with gemini 3.7 flash at 1%; a benchmark where nearly everything scores zero discriminates almost nothing, and its only bearing here is that it does not separate ox-alpha from GLM-5.3. Attribution moved to a thin prediction market: @nicbstme reports it prices Z.ai as the source while flagging low volume, and @teortaxesTex notes insiders have an incentive to misdirect before betting; he separately reads @sam_paech's slop-profile comparison as showing 'the gap between 0731 and ox-alpha is Opus-shaped', an output-style inference rather than an attribution. Six days in: still no lab claim, model card, pricing or weights. Status stays in-testing; verification stays partial."
  - ts: 2026-08-26
    change: "First concrete vendor identification, plus the first head-to-head kernel numbers. @spark_arena (relayed by @LottoLabs, 2026-08-25 20:59 UTC): 'GLM 5.3 Flash is 0x Alpha for those that are curious. Tomorrow it's going to be a great day for Local AI with Qwen and GLM.' That is a direct claim that Ox Alpha is Zhipu's GLM 5.3 Flash, which would place it inside [[zhipu-glm-5-3-2026-08]]'s family exactly as this ticket's Zhipu suspicion predicted - but it is one unattributed account with no lab confirmation and no model card, so verification stays partial and the company field keeps its 'suspected' hedge. @teortaxesTex separately jokes at the same Zhipu/'Ox' association without adding evidence. The substantive news is capability data from @elliotarledge's KernelBench runs (2026-08-25), the first evidence on this ticket that is neither volume nor vibes. On KernelBench-Hard's Top-K Bitonic kernel for RTX PRO 6000, Ox Alpha reaches 7.17% of roofline, 'just behind Opus 5', writing one raw CUDA kernel with order-preserving value and index keys, per-thread top-R filtering and warp-shuffle bitonic sorting - and he explicitly certifies 'No reward hacking/cheating here!', which matters given @ArtificialAnlys's same-day introduction of reward-hacking score corrections to Terminal-Bench v2.1. On KernelBench-CUDA's DeepSeek Native Sparse Attention kernel it came LAST: it nailed the CUDA-core-specific parts (TopK, softmax) but 'completely missed tensor core tiling of QK and PV' and mapped one query per warp with serial loops, adding shuffle and latency overhead. So the picture is a genuinely competent frontier-adjacent kernel writer with a specific tensor-core blind spot. Status stays in-testing; verification stays partial."
  - ts: 2026-08-27
    change: "CLOSED — superseded-by:zhipu-glm-5-3-2026-08. Z.ai claimed the model on the record and the ticket's premise (an artifact with no vendor) no longer holds. @Zai_org: 'Introducing GLM-5.3-Flash - Leading capabilities at a highly competitive price - Natively multimodal with a 1M-token context window - A 320B-A18B model released under the MIT License - Previously previewed as Ox Alpha, running entirely on Chinese AI chips.' @OpenRouter confirmed independently from the venue side: 'Ox Alpha revealed: @Zai_org's GLM-5.3-Flash... Ox Alpha was the biggest model ever on OpenRouter, processing over 20 trillion tokens in 6 days', and @Teknium noted the free period ended with GLM-5.3-Flash taking its place. @louszbd (Zhipu-side) framed the stealth run as deliberate feedback collection: 'Ox Alpha put GLM-5.3-Flash in more people's hands. We've read every piece of feedback. The model you're using now is better.' Scoring the ticket's own attribution record honestly: the 2026-08-23 firsthand-tester reading (@davis7 on shared video encoder/tokenizer/style/audio-rejection, @kimmonismus and @synthwavedd naming GLM-5.3 Flash specifically, @AndrewCurran_ reading it as a Z.ai GLM Flash variant of a larger flagship) was correct in full including the Flash sizing; @mark_k's Google DeepMind call and the Anthropic, Grok 4.7, Cursor and Sarvam hypotheses were wrong. @rasbt's teardown supplies the architecture: Kimi Linear-style 3:1 hybrid attention (34 Kimi Delta Attention + 11 MLA/DSA layers), a scaled-down GLM-5.2 sparse MoE backbone (744B-A40B -> 320B-A18B), a DeepSeek-V4-style mHC residual path with four parallel streams, and a native vision encoder. The genuinely unanticipated fact is the serving substrate: @SemiAnalysis_ reports ALL of that traffic — 100T tokens/day of capacity — was served on domestic Chinese chips 'attaining hardware efficiency and per-token cost comparable to Nvidia GPUs', with @teortaxesTex adding it was not even the current generation in mass production. Verification advances partial -> confirmed on the first-party vendor claim plus independent venue confirmation. All further GLM-5.3-Flash signal (weights, pricing, benchmarks, domestic-silicon serving) goes to [[zhipu-glm-5-3-2026-08]]; this ticket is read-only from here."
---

A stealth alias on a router is not normally worth a ticket. This one is,
because the artifact behind `stealth/ox-alpha` is a long-horizon
multimodal model with a 1M context window that a dozen serious testers
put in the neighbourhood of GPT-5.6 Sol mid — and nobody has claimed it.

The interesting question is not "how good is it" but **what its size
implies**. The load-bearing rumor is that it is a *Flash-class* model. If
that is true, @davis7's framing is the right one: "If ox-alpha actually
ends up being a flash model, it's as big of a deal as Mythos or DeepSeek
R1 — the implications of a small model with this level of capability are
insane." @kimmonismus makes the same point from the deployment side: a
GPT-5.6-Sol-mid-class model that runs on 2× DGX Spark, at the cost of
electricity, changes what local inference is for. That claim is entirely
unverified. It is also the reason this ticket exists.

**The evidence for the GLM attribution is technical, not social.**
@davis7 lists a shared video encoder, a shared tokenizer, matching
output style, and matching audio-rejection behaviour with the GLM line;
Z.ai announced [[zhipu-glm-5-3-2026-08]] on 2026-08-14 with heavy
emphasis on coding, long-horizon agents, and cyber evaluations, and Ox
Alpha surfaced six days later scoring well on exactly those axes.
@teortaxesTex's counter-argument to the rival Cursor hypothesis is
similarly mechanical — Cursor trains for agentic SWE and would have no
reason to post-train vision or expose full chains of thought.

**The evidence against taking any of it at face value is that two
careful testers came away unimpressed.** @emollick ran his own shader
test and rates it below Kimi K3; @iruletheworldmo calls the wave a
campaign. Both are firsthand, and both cut against the consensus. This
ticket records the disagreement rather than resolving it.

@giffmana raises the operational wrinkle that makes deanonymization
likely regardless: OpenRouter returns true token counts for stealth
models, which he argues is enough to identify the vendor with reasonable
confidence. Expect attribution to arrive from that direction, or from a
lab announcement, well before any model card does.

Related: [[zhipu-glm-5-3-2026-08]] (the named GLM-5.3 flagship this is
suspected to descend from), [[moonshot-kimi-k3]], [[openai-gpt-5-6]].
