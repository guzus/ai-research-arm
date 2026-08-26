---
slug: openai-jalapeno-chip-2026-06
title: OpenAI Jalapeño — first custom inference ASIC (with Broadcom)
company: OpenAI
model: Jalapeño
status: confirmed
status_note: |
  OpenAI unveiled its **first custom AI chip**, **Jalapeño**, on 2026-06-24
  (@OpenAI 13:10 UTC, ~20.7K–21.5K likes): "We've designed and built our first
  AI chip: Jalapeño. Designed from the ground up by OpenAI and brought to
  production with Broadcom." **Inference-only** (no claimed training capability).
  Broadcom CEO **Hock Tan** told Bloomberg early testing shows **~50% cost
  savings per inference token vs standard GPUs**, and told Reuters performance
  is "on par with NVIDIA Blackwell and Google TPUs" — the 50% figure is
  Broadcom's claim, not OpenAI's (OpenAI's own language hedges to "substantially
  better than state-of-the-art"). Claimed a **9-month design-to-tape-out**
  (accelerated by OpenAI's own models designing the chip); **3nm TSMC
  engineering samples** hand-delivered to Sam Altman and Greg Brockman by
  Broadcom's CEO. Microsoft reportedly guaranteed **~40% of initial output**
  (The Decoder, unconfirmed by either company). Prototype deployment **late
  2026**, ramps **2027–2028**, targeting gigawatt-scale data centers.
  Lands the same week as NVIDIA's open-sourced DFlash speculative-decoding
  ([[nvidia-dflash-2026-06]]) — competing answers to dropping inference cost.

  **2026-08-26 - Hot Chips benchmarks; in-testing -> confirmed.** OpenAI posted
  three first-party updates (2026-08-25 17:19 UTC): it has been testing
  "Jalapeno and the system around it", results show "more intelligence from
  every watt and faster responses ... higher throughput and lower latency in one
  architecture", and it "plan[s] to begin deploying Jalapeno in OpenAI's compute
  infrastructure by year-end" as step one of a multigenerational roadmap.
  Third-party Hot Chips numbers (via @mark_k, @SemiAnalysis_): 1.5-1.9x perf/W
  and 1.7-3.6x lower latency vs GB200/GB300 across GPT-OSS 120B, DeepSeek R1 670B
  and Kimi K2.5 1T; 700 tok/s/user on DeepSeek R1 vs 169 on GB300; a 128-chip rack
  at 1.7 EFLOPS MXFP4 / 27.5 TB HBM4; and - the more provocative claim - better
  output-throughput-per-MW than NVIDIA's **July Vera Rubin** results, without spec
  decoding enabled. Two named skeptics on the record: @GavinSBaker (the fair
  comparison is shipping Rubin Ultra and Feynman, not July Rubin) and @jukan05
  (Samsung-exclusive HBM4 sourcing caps the ramp). Still not `released` - nothing
  is serving user traffic yet.
expected: "Deployment into OpenAI's own compute infrastructure begins by year-end 2026 per OpenAI; Gen 2 'deep in development', Gen 3 'taking shape'. Pending: production user traffic served on it (the released trigger), the Hot Chips deck / OpenAI blog captured directly, an apples-to-apples comparison against shipping Rubin Ultra rather than July Rubin, and whether Samsung-only HBM4 sourcing caps the ramp"
labels:
  - hardware
  - inference-asic
  - openai
  - broadcom
  - confirmed
verification: confirmed
sources:
  - https://x.com/OpenAI/status/2069770172802773292
  - "@OpenAI"
  - "@TheValueist"
  - "@OwenGregorian"
  - https://x.com/OpenAI/status/2092300846675505602
  - https://x.com/OpenAI/status/2092300851482108064
  - "@sama"
  - "@SemiAnalysis_"
  - "@mark_k"
  - "@GavinSBaker"
  - "@jukan05"
  - "@AndrewCurran_"
created_at: 2026-06-26
updated_at: 2026-08-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-26
    change: "Created — OpenAI unveiled Jalapeño, its first custom AI inference ASIC, on 2026-06-24 (@OpenAI 13:10 UTC, ~20.7K–21.5K likes), designed in-house and brought to production with Broadcom. Inference-only. Broadcom CEO Hock Tan told Bloomberg ~50% cost savings per inference token in early testing vs GPUs, and told Reuters performance 'on par with NVIDIA Blackwell and Google TPUs' (the 50% is Broadcom's claim, not OpenAI's — OpenAI hedges to 'substantially better'). 9-month design-to-tape-out (AI-assisted chip design); 3nm TSMC engineering samples hand-delivered to Altman/Brockman; Microsoft reportedly guaranteed ~40% of initial output (The Decoder, unconfirmed). Prototype deployment late 2026, ramps 2027–2028. Real artifact (engineering samples) but not yet deployed at scale → status in-testing; verification confirmed (official @OpenAI post + Broadcom CEO on-record to Bloomberg/Reuters). Pairs with NVIDIA DFlash ([[nvidia-dflash-2026-06]] as competing inference-cost answers; analyst framing is pricing-power erosion for NVIDIA, not displacement."
  - ts: 2026-08-26
    change: "Hot Chips benchmarks land - the technical-report trigger this ticket set in June is met, and status advances in-testing -> confirmed. @OpenAI posted three first-party updates (2026-08-25 17:19 UTC, ~12.8K engagement on the lead): since announcing Jalapeno 'we've been testing it and the system around it,' the results show 'more intelligence from every watt and faster responses, delivering both higher throughput and lower latency in one architecture without sacrificing efficiency'; it means 'faster ChatGPT responses, more responsive Codex sessions and agents, and reliable access as demand continues to grow'; and OpenAI 'plan[s] to begin deploying Jalapeno in OpenAI's compute infrastructure by year-end,' the first step in a multigenerational roadmap where 'Gen 2 is deep in development, and Gen 3 is taking shape.' @sama's framing: 'we made a chip and it is fast' (~36.3K engagement). Third-party numbers from the Hot Chips session, via @mark_k (2026-08-25 17:25 UTC): the Gen-1 inference part beats GB200/GB300 across GPT-OSS 120B, DeepSeek R1 670B and Kimi K2.5 1T at 1.5-1.9x performance per watt, 1.7-3.6x lower end-to-end latency and 2.1-4.1x higher performance in highly interactive workloads; 700 tok/s/user on DeepSeek R1 vs 169 on GB300; a 128-chip rack delivering 1.7 EFLOPS of MXFP4 with 27.5 TB of HBM4. A separate relay puts power draw at 550W under load vs 1200W/1400W for GB200/GB300, and Kimi K2.5 at 694 vs 182 tok/s. @SemiAnalysis_ goes further (2026-08-25 18:15 and 2026-08-26 01:15 UTC): Jalapeno beats NVIDIA's *July Vera Rubin* results on output throughput per MW - 'up to 2x better perf per watt', 'didn't even enable spec decoding, yet beats Rubin NVL72 with spec decoding', and 'better performance across the entire Pareto versus July Rubin'; its long piece frames the real thesis as perf/W in a power-constrained industry, thousands of chips networked into one inference machine, and the possibility that frontier models writing kernels invalidate the industry's need for a perfect universal compiler. Two named skeptical caveats recorded rather than dropped: @GavinSBaker says the honest comparison is shipping Rubin Ultra and the fast-approaching Feynman, not July Rubin, and expects a disaggregated GPU/Trainium-plus-SRAM setup to significantly outperform - while still calling it the 'first good ASIC outside of TPU/Trainium'; @jukan05 says Jalapeno appears to source Samsung HBM4 almost exclusively, which limits the ramp unless OpenAI lowers the HBM4 speed requirement to qualify other suppliers. Separately, OpenAI's own blog names GPT-Astra as a builder of the chip - 'Using Codex with GPT-Astra, the team brought three open-weight models that were not part of Jalapeno's original production plan to high performance within two months' - the first OpenAI-sourced public use of the Astra name; that half is recorded on [[openai-gpt-6]]. Status advances to confirmed because the chip now has publicly benchmarked results and a committed deployment date rather than only engineering samples; verification stays confirmed. Not released: no production traffic yet."
---

**Jalapeño** is **OpenAI's first custom AI chip**, unveiled 2026-06-24 and
designed from the ground up by OpenAI with **Broadcom** bringing it to
production. It is **inference-only** — OpenAI makes no training-capability
claim — and is positioned as a vertical-integration move to reduce OpenAI's
dependency on NVIDIA GPUs at the inference layer.

**What's confirmed vs. claimed.** The announcement itself is first-party
(@OpenAI's official post, ~20.7K–21.5K likes) and Broadcom CEO **Hock Tan**
went on-record to Bloomberg and Reuters. That makes the *existence* of the
chip and the partnership `confirmed`. The headline economics — **~50% cost
savings per inference token** — is **Tan's claim, not OpenAI's**: OpenAI's
own statement notably hedges to "substantially better than state-of-the-art,"
unusual language for a flagship product launch. Treat the 50% as
Broadcom-sourced and unvalidated at production scale.

**Timeline.** Engineering samples (3nm TSMC) exist now and were hand-delivered
to Altman and Brockman, which is why this is `in-testing` rather than
`rumored`/`confirmed`-only. Meaningful deployment is **18+ months out**
(prototype late 2026, ramp 2027–2028). A reported **Microsoft guarantee of
~40% of initial output** (The Decoder) is unconfirmed by either company.

**Why it matters.** The honest analyst framing (@TheValueist) is that
Jalapeño is a **pricing-power erosion signal** for NVIDIA, not a displacement
event — inference-only, far from scale, with a Broadcom-CEO cost number and
no disclosed baseline. But the **9-month AI-assisted design cycle** is an
underappreciated proof point: it suggests OpenAI can iterate hardware fast
enough to make multi-generational improvements credible. It lands alongside
NVIDIA's open-sourced **DFlash** speculative decoding
([[nvidia-dflash-2026-06]]) — two competing answers to whether inference cost
can keep dropping fast enough to sustain demand growth.

**Transition triggers:**
- A technical report with benchmark numbers, or Microsoft's 40% guarantee
  confirmed → UPDATE, append history.
- Production deployment / first customer traffic → advance toward `released`.
- Abandoned or spun into a different silicon program → close per reason.

**Dedup note:** Jalapeño hardware signal (specs, deployment, benchmarks)
UPDATES this ticket. OpenAI's broader compute/datacenter buildout stays on
its own relevant tickets.
