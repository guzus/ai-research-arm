---
slug: alibaba-qwen-4-architecture-2026-08
title: Qwen4 architecture preview + Qwen3.8-Flash-Next
company: Alibaba
model: Qwen3.8-Flash-Next / Qwen4
status: in-testing
status_note: |
  Alibaba's Qwen team teased the next generation on 2026-08-25. @QwenDevs
  (11:09 UTC, ~2.5K engagement): "**The next Qwen wave is coming**."
  @NielsRogge the same day: "Looks like @Alibaba_Qwen set up a **countdown**
  for this one! **'A Preview of the Qwen4 Architecture'**" — so the artifact is
  an official countdown page naming the architecture, not a rumor of one.
  @MiaAI_lab (RT'd by @huggingface): "**22 hours to go for Qwen3.8 Flash**."

  The specs are leak-grade, not official. @AiBattle_ (11:18 UTC, ~1.1K
  engagement): "**Qwen 3.8 Flash Next** is releasing Tomorrow. **125B
  parameters + 51B N-gram and 6B active**. It's based on the **next generation
  Qwen 4 architecture**. Qwen 4 is coming." Single account, no model card.

  One architectural thread worth tracking: @NielsRogge points to **Engram**,
  "the key technique developed by **@deepseek_ai** powering Qwen4" — i.e. the
  next Qwen architecture is reported to build on a DeepSeek-published method,
  which is a cross-lab-diffusion datapoint rather than a Qwen claim.
expected: "Official Qwen countdown titled 'A Preview of the Qwen4 Architecture' running as of 2026-08-25, with Qwen3.8 Flash expected within ~22 hours (i.e. 2026-08-26). Leak-grade specs: 125B total + 51B N-gram, 6B active, on the Qwen4 architecture. Pending: the actual release, a model card confirming the parameter shape and the N-gram component, weights and license, benchmark numbers, and confirmation that DeepSeek's Engram underlies Qwen4"
labels:
  - alibaba
  - qwen
  - open-weights
  - architecture
  - in-testing
verification: partial
sources:
  - "@QwenDevs"
  - "@NielsRogge"
  - "@AiBattle_"
  - "@MiaAI_lab"
  - "@huggingface"
created_at: 2026-08-26
updated_at: 2026-08-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-26
    change: "Created — Alibaba's Qwen team began an official countdown to its next architecture generation on 2026-08-25, and a named next model is expected within a day. Official side: @QwenDevs (11:09 UTC, ~2.5K engagement) posted 'The next Qwen wave is coming', and @NielsRogge (13:47 UTC) reports 'Looks like @Alibaba_Qwen set up a countdown for this one! \"A Preview of the Qwen4 Architecture\"' — so the artifact is a real Qwen-run countdown page that names Qwen4, which is what puts this at in-testing rather than rumored. @MiaAI_lab, RT'd by @huggingface, put it at '22 hours to go for Qwen3.8 Flash' as of 17:06 UTC, implying a 2026-08-26 release. Leak side, which does NOT get official weight: @AiBattle_ (11:18 UTC, ~1.1K engagement) says 'Qwen 3.8 Flash Next is releasing Tomorrow. 125B paramters +51B N-gram and 6B active. Its based on the next generation Qwen 4 architecture. Qwen 4 is coming.' That parameter shape — a 125B backbone plus a separately-counted 51B N-gram component and only 6B active — is unusual enough to be worth flagging as either a genuinely novel architecture or a garbled leak; there is one source, no model card, and no benchmark. Cross-lab thread: @NielsRogge separately points to Engram as 'the key technique developed by @deepseek_ai powering Qwen4', which if true means the next Qwen architecture builds on a DeepSeek-published method — a diffusion datapoint between the two leading Chinese open-weight labs, recorded as reported rather than established. Status in-testing on the official countdown artifact; verification partial — the countdown and the teaser are first-party, but every substantive spec is single-source. This is the next-generation successor thread to [[alibaba-qwen-3-8-27b-2026-08]] and [[alibaba-qwen-3-8-max-2026-07]]; a shipped Qwen3.8-Flash-Next or Qwen4 model resolves it. Same-day local-AI context: @spark_arena claimed 'Tomorrow it's going to be a great day for Local AI with Qwen and GLM', pairing this with the Ox Alpha / GLM 5.3 Flash thread ([[stealth-ox-alpha-model-2026-08]])."
---

Alibaba's Qwen team started an official countdown on 2026-08-25 titled **"A
Preview of the Qwen4 Architecture,"** with **@QwenDevs** posting "the next Qwen
wave is coming" and community trackers putting **Qwen3.8 Flash** roughly 22
hours out.

**What is official.** The countdown page and the teaser — both from Qwen's own
channels — and the fact that the next architecture is called **Qwen4**. That
is enough to make this a real artifact in testing rather than a rumor.

**What is leak-grade.** @AiBattle_ reports **Qwen3.8-Flash-Next** at **125B
parameters + 51B N-gram and 6B active**, built on the Qwen4 architecture. The
shape is the interesting part: a separately-counted **N-gram component**
alongside a sparse 6B-active backbone is not a standard MoE description. It is
either a genuinely novel architecture worth understanding or a garbled leak,
and one account with no model card cannot settle which.

**The DeepSeek thread.** @NielsRogge points to **Engram** as "the key technique
developed by DeepSeek powering Qwen4." If that holds, the next Qwen generation
is built on a method its closest domestic open-weights rival published — a
notable diffusion datapoint about how fast published Chinese-lab research
propagates. Recorded as reported, not established.

**Why it matters here.** [[alibaba-qwen-3-8-27b-2026-08]] was the quarter's
dominant open-weights release, sized precisely for the consumer hardware that
Apple and NVIDIA are now selling into
([[apple-m5-ultra-mac-studio-2026-08]]). A Qwen4-architecture successor
shipping this week, alongside GLM 5.3 Flash
([[stealth-ox-alpha-model-2026-08]]), sets the open-weights floor for the rest
of the year.

**Transition triggers:**
- Qwen3.8-Flash-Next actually ships with weights and a model card → advance to
  `released`, confirm or correct the parameter shape.
- A Qwen4 architecture paper or blog → UPDATE, and confirm or drop the Engram
  attribution.
- The countdown resolves to something other than what was leaked → UPDATE with
  the correction; do not rewrite this entry.

**Dedup note:** Qwen4-architecture and Qwen3.8-Flash-Next signal UPDATES this
ticket. Qwen3.8-27B stays on [[alibaba-qwen-3-8-27b-2026-08]]; Qwen3.8-Max
stays on [[alibaba-qwen-3-8-max-2026-07]].
