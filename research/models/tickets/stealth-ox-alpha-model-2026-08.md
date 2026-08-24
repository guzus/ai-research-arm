---
slug: stealth-ox-alpha-model-2026-08
title: "\"Ox Alpha\" — unattributed stealth frontier model on OpenRouter"
company: Unattributed (stealth; Zhipu AI / Z.ai suspected)
model: Ox Alpha
status: in-testing
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
expected: "Live and free via OpenRouter/opencode/Hermes/Cursor as of 2026-08-24, vendor still unclaimed after 4+ days. Pending: a lab claiming it, a model card, pricing, weights (Z.ai's GLM line has shipped open weights), and whether it resolves into [[zhipu-glm-5-3-2026-08]]'s family or something else"
labels:
  - stealth-model
  - frontier-model
  - openrouter
  - unattributed
  - in-testing
verification: partial
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
created_at: 2026-08-23
updated_at: 2026-08-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-23
    change: "Created — an unattributed stealth model shipping as stealth/ox-alpha on OpenRouter since ~2026-08-20, free via OpenRouter, opencode, Hermes Agent (@Teknium, @NousResearch) and Cursor. Established by firsthand testers: long-horizon multimodal, 1M context (@AndrewCurran_); ~63% on the full 113-task DeepSWE run (@davis7, who publicly retracted his own earlier ~80% subset number), 58.4 read independently by @teortaxesTex, roughly GPT-5.6 Sol mid class. Attribution unresolved: @davis7 99% GLM-5.x on encoder/tokenizer/style evidence, @kimmonismus and @synthwavedd say GLM-5.3 Flash, @AndrewCurran_ canvass lands on a Z.ai GLM Flash variant, but @mark_k claims Google DeepMind and @teortaxesTex argues against Cursor. Capability claim itself is contested — @emollick and @iruletheworldmo both tested it and rate it non-frontier. Status in-testing (real, publicly usable artifact under a stealth alias, no vendor claim); verification partial (many independent firsthand runs establish the artifact; no primary source establishes who made it)."
  - ts: 2026-08-24
    change: "Another cycle with no attribution progress: still no lab claim, model card, pricing, or weights. Speculation turned reflexive — @iruletheworldmo posted an elaborate pseudo-architecture (persistent latent state, attractors, shards, metaparameters) and @teortaxesTex answered with open parody of the guessing game; neither is recorded as evidence. Two new unsupported hypotheses appeared from single low-engagement accounts: an Anthropic experiment (@simonepaciaroni, on a claimed telltale marker) and xAI's unreleased Grok 4.7 in pre-release testing (@Norwakar). The GLM-family reading from 2026-08-23 firsthand testers remains best-supported. Trade aggregators began covering it as an unclaimed mystery model. Status stays in-testing; verification stays partial."
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
