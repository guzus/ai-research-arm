---
slug: alibaba-qwen-4-architecture-2026-08
title: Qwen4 architecture preview + Qwen3.8-Flash / Flash-Next
company: Alibaba
model: Qwen3.8-Flash / Qwen3.8-Flash-Next / Qwen4
status: released
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

  **2026-08-26 — it shipped, open-weight, and the leaked parameter shape
  was right.** **@Alibaba_Qwen**: "Meet **Qwen3.8-Flash**, a multimodal
  MoE and **an early preview of the Qwen4 architecture, now open-weight!**
  The production version Qwen3.8-Flash will be available soon via
  QwenCloud API at just **$0.16/1M input tokens and $0.47/1M output
  tokens**. **125B parameters + 51B N-gram embeddings, with just 6B
  active**." That confirms @AiBattle_'s 2026-08-25 leak *exactly* —
  125B + 51B N-gram + 6B active — so the "either novel architecture or
  garbled leak" question this ticket flagged resolves to **novel
  architecture**. @testingcatalog adds **262K native context, extensible
  to 1M with YaRN**, and **58.7 on DeepSWE 1.1 / 62.5 on SWE-bench Pro**.

  **The architecture is now first-party, and @SemiAnalysis_ names the
  three innovations** it says carry over to Qwen4: a **51B-param N-gram
  Embedding** that is a cheap table lookup, so the embedding table can be
  offloaded to slower and cheaper DRAM tiers; a **Gated Residual (GR)**;
  and **Qwen Sparse Attention (QSA)**, a lightning indexer selecting
  context at micro-block granularity. @Alibaba_Qwen's own architecture
  post frames the attention as a **GDN + QSA hybrid** — Gated DeltaNet
  compressing history, QSA selecting from it. The N-gram-offload point is
  the load-bearing one for local inference: it is why a 176B-parameter
  model runs in ~75GB.

  **Local-inference evidence arrived day-0 and is unusually strong.**
  @UnslothAI: "Qwen3.8-Flash can now be run **locally**! The 125B MoE
  model **outperforms Claude-Opus-4.6 (Max)**. Run on **75GB RAM** via
  Unsloth GGUFs. Qwen3.8-Flash-Next enables CPU RAM / unified mem setups
  to deliver near VRAM speeds," with @Alibaba_Qwen RT'ing the day-0
  support. @atomic_chat_hq (relayed by @Hikari_07_jp and @LottoLabs) ran
  **1-bit Qwen3.8-Flash-Next (79GB) on a 64GB M5 MacBook Pro Max at 30
  tok/s** through an 8-minute agent loop with 6 web searches and 3 Python
  runs; @analogalok ran it at a **250,000-token context on a single**
  card. @kimmonismus's read of the benchmark table: it "beats Claude Opus
  4.6 Max on **8 of 9** comparable benchmarks, including SWE-bench Pro,
  CoWorkBench, GPQA Diamond and LiveCodeBench" — with his own caveat that
  6B active does not mean 6B-model quality or 6B memory.

  **Practitioner verdicts, unprompted:** @TheAhmadOsman — "Qwen 3.8 Flash
  Next has **dethroned DeepSeek V4 Flash 0731** for me."

  **What is still NOT established:** the DeepSeek **Engram** attribution
  for Qwen4. @NielsRogge reported it; nothing in the official architecture
  material in this window names Engram. It stays recorded as reported.
  @eliebakouch's cross-lab summary is the fair generalisation instead:
  every Chinese frontier model now uses linear attention (except
  DeepSeek), sparse attention with similar indexer/compression designs,
  and elaborate residuals — @NielsRogge notes the residual work "has
  devolved to something extremely extremely cursed."
expected: "Qwen3.8-Flash shipped open-weight 2026-08-26 as an explicit early preview of the Qwen4 architecture: 125B params + 51B N-gram embeddings, 6B active, 262K native context (1M via YaRN), $0.16/$0.47 per Mtok on QwenCloud, day-0 Unsloth GGUFs running in ~75GB RAM. The leaked parameter shape was confirmed exactly. Pending: Qwen4 itself, a full architecture paper, neutral-org benchmark placement rather than the lab table (the Opus-4.6-Max comparison is Qwen-published), whether DeepSeek's Engram actually underlies Qwen4 (still only @NielsRogge's report), and the production QwenCloud endpoint going live"
labels:
  - alibaba
  - qwen
  - open-weights
  - architecture
  - local-inference
  - released
verification: confirmed
sources:
  - "@QwenDevs"
  - "@NielsRogge"
  - "@AiBattle_"
  - "@MiaAI_lab"
  - "@huggingface"
  - "@Alibaba_Qwen"
  - "@UnslothAI"
  - "@SemiAnalysis_"
  - https://x.com/SemiAnalysis_/status/2092688580111974648
  - "@testingcatalog"
  - "@kimmonismus"
  - "@TheAhmadOsman"
  - "@Hikari_07_jp"
  - "@atomic_chat_hq"
  - "@eliebakouch"
created_at: 2026-08-26
updated_at: 2026-08-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-26
    change: "Created — Alibaba's Qwen team began an official countdown to its next architecture generation on 2026-08-25, and a named next model is expected within a day. Official side: @QwenDevs (11:09 UTC, ~2.5K engagement) posted 'The next Qwen wave is coming', and @NielsRogge (13:47 UTC) reports 'Looks like @Alibaba_Qwen set up a countdown for this one! \"A Preview of the Qwen4 Architecture\"' — so the artifact is a real Qwen-run countdown page that names Qwen4, which is what puts this at in-testing rather than rumored. @MiaAI_lab, RT'd by @huggingface, put it at '22 hours to go for Qwen3.8 Flash' as of 17:06 UTC, implying a 2026-08-26 release. Leak side, which does NOT get official weight: @AiBattle_ (11:18 UTC, ~1.1K engagement) says 'Qwen 3.8 Flash Next is releasing Tomorrow. 125B paramters +51B N-gram and 6B active. Its based on the next generation Qwen 4 architecture. Qwen 4 is coming.' That parameter shape — a 125B backbone plus a separately-counted 51B N-gram component and only 6B active — is unusual enough to be worth flagging as either a genuinely novel architecture or a garbled leak; there is one source, no model card, and no benchmark. Cross-lab thread: @NielsRogge separately points to Engram as 'the key technique developed by @deepseek_ai powering Qwen4', which if true means the next Qwen architecture builds on a DeepSeek-published method — a diffusion datapoint between the two leading Chinese open-weight labs, recorded as reported rather than established. Status in-testing on the official countdown artifact; verification partial — the countdown and the teaser are first-party, but every substantive spec is single-source. This is the next-generation successor thread to [[alibaba-qwen-3-8-27b-2026-08]] and [[alibaba-qwen-3-8-max-2026-07]]; a shipped Qwen3.8-Flash-Next or Qwen4 model resolves it. Same-day local-AI context: @spark_arena claimed 'Tomorrow it's going to be a great day for Local AI with Qwen and GLM', pairing this with the Ox Alpha / GLM 5.3 Flash thread ([[stealth-ox-alpha-model-2026-08]])."
  - ts: 2026-08-27
    change: "Status in-testing -> released, verification partial -> confirmed. It shipped open-weight on 2026-08-26 and the leaked parameter shape was exactly right. @Alibaba_Qwen: 'Meet Qwen3.8-Flash, a multimodal MoE and an early preview of the Qwen4 architecture, now open-weight! The production version Qwen3.8-Flash will be available soon via QwenCloud API at just $0.16/1M input tokens and $0.47/1M output tokens. 125B parameters + 51B N-gram embeddings, with just 6B active.' That confirms @AiBattle_'s 2026-08-25 leak verbatim (125B + 51B N-gram + 6B active), resolving this ticket's own 'novel architecture or garbled leak' question in favour of novel architecture. @testingcatalog adds 262K native context extensible to 1M via YaRN, 58.7 on DeepSWE 1.1 and 62.5 on SWE-bench Pro. Architecture now first-party: @Alibaba_Qwen describes a GDN + QSA hybrid attention (Gated DeltaNet compressing history, Qwen Sparse Attention selecting via a lightweight micro-block indexer), and @SemiAnalysis_ names the three Qwen4-bound innovations — the 51B N-gram Embedding as a cheap table lookup that can be offloaded to slower/cheaper DRAM tiers, Gated Residual, and QSA. The N-gram offload is why a 176B-parameter model fits in ~75GB. Local-inference evidence landed day-0: @UnslothAI shipped GGUFs running the 125B MoE in 75GB RAM and reports it outperforms Claude-Opus-4.6 (Max), with @Alibaba_Qwen RT'ing the day-0 support; @atomic_chat_hq ran 1-bit Flash-Next (79GB) on a 64GB M5 MacBook Pro Max at 30 tok/s through an 8-minute agent loop; @analogalok ran a 250K-token context on a single card. @kimmonismus's read of the lab table: beats Opus 4.6 Max on 8 of 9 comparable benchmarks including SWE-bench Pro, CoWorkBench, GPQA Diamond and LiveCodeBench, with his own caveat that 6B active means neither 6B quality nor 6B memory. @TheAhmadOsman, unprompted: Flash-Next 'has dethroned DeepSeek V4 Flash 0731 for me.' NOT established and explicitly still open: the DeepSeek Engram attribution for Qwen4 — @NielsRogge reported it, nothing in the official architecture material this window names Engram, so it stays recorded as reported. @eliebakouch's cross-lab generalisation stands in its place: every Chinese frontier model now uses linear attention (except DeepSeek), sparse attention with similar indexer designs, and elaborate residuals. Title and model fields widened to include the shipped Qwen3.8-Flash; slug immutable. Landed the same day as GLM-5.3-Flash ([[zhipu-glm-5-3-2026-08]])."
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

**Resolved 2026-08-26.** It shipped, open-weight, on the leaked shape
exactly. The interesting part is *why* the shape is what it is: the 51B
N-gram embedding is a lookup table, not compute, so it can live in cheap
slow DRAM while only 6B parameters are active per token. That is what
makes a 176B-parameter multimodal model a 75GB local workload — and it
landed on the same day as GLM-5.3-Flash ([[zhipu-glm-5-3-2026-08]]),
which is why practitioners spent the day reporting frontier-adjacent
throughput on single-workstation hardware rather than debating
benchmarks.

**Transition triggers:**
- Qwen4 itself, or a full architecture paper → UPDATE, and confirm or drop
  the Engram attribution (still unestablished).
- Neutral-org benchmark placement → UPDATE; the Opus-4.6-Max comparison is
  currently Qwen-published.
- The production QwenCloud endpoint going live at the stated
  $0.16/$0.47 → UPDATE.
- ≥4 weeks past release, settled into normal coverage →
  `closed: released-and-aged`.

**Dedup note:** Qwen4-architecture and Qwen3.8-Flash-Next signal UPDATES this
ticket. Qwen3.8-27B stays on [[alibaba-qwen-3-8-27b-2026-08]]; Qwen3.8-Max
stays on [[alibaba-qwen-3-8-max-2026-07]].
