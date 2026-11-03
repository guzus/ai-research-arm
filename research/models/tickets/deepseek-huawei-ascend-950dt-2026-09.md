---
slug: deepseek-huawei-ascend-950dt-2026-09
title: DeepSeek said to buy 160,000 Huawei Ascend 950DT chips for a 1GW Inner Mongolia datacenter
company: DeepSeek / Huawei
model: null
status: rumored
status_note: |
  @ns123abc, 2026-09-04: "DeepSeek purchased **160,000 Huawei Ascend 950DT**
  chips for new **1 gigawatt data center in inner Mongolia**. 950DT are
  Hopper-class so **only for inference**. **TRAINING stays on NVIDIA**."

  The last clause is the load-bearing one and it is what makes this worth a
  ticket rather than a headline. If accurate, DeepSeek is doing exactly the
  split Zhipu disclosed in its interim filing
  ([[zhipu-domestic-chip-datacenter-2026-07]]): serve inference on domestic
  silicon at scale, keep training on NVIDIA. That is the operative shape of
  Chinese lab compute under export controls — not substitution, but
  segregation by workload.

  Status `rumored`, verification `partial`: one relay account, no DeepSeek or
  Huawei statement, no filing, and no corroborating report in this cycle's
  signal. The numbers (160k units, 1GW, Hopper-class) are internally
  consistent and the Inner Mongolia siting is plausible for power, but none of
  it is confirmed. Do not treat the chip count as established.

  Related but distinct: [[deepseek-second-round-2026-07]] (funding),
  [[china-nvidia-h200-import-2026-07]] (import policy).

  **2026-11-03 — second report, different workload split.** @StarsLevels, citing TrendForce and
  The Information: DeepSeek plans to PRE-TRAIN V5 mainly on Ascend 950 (160,000+ 950DT at Ulanqab,
  Inner Mongolia), with pre-training possibly from late 2026 and V5 in 2027. This corroborates the chip
  count and site but contradicts the inference-only claim above. Still no company confirmation.
expected: "Unconfirmed. Corroboration would come from a Huawei or DeepSeek statement, a provincial energy/permitting filing for the Inner Mongolia site, or a second independent outlet."
labels:
  - deepseek
  - huawei
  - domestic-silicon
  - compute
  - china
verification: partial
sources:
  - https://x.com/ns123abc/status/2095838690681454963
  - "https://x.com/StarsLevels/status/2117622026554757616"
created_at: 2026-09-07
updated_at: 2026-11-03
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-07
    change: "Created — RUMORED. @ns123abc reported on 2026-09-04 that DeepSeek purchased 160,000 Huawei Ascend 950DT chips for a new 1 gigawatt data center in Inner Mongolia, adding that the 950DT is Hopper-class and therefore inference-only, with training staying on NVIDIA. The inference/training split is the substantive claim: it matches what Zhipu disclosed in its interim filing ([[zhipu-domestic-chip-datacenter-2026-07]]) — domestic silicon for serving at scale, NVIDIA for training — which is workload segregation rather than substitution. Status rumored, verification partial: a single relay account with no DeepSeek or Huawei statement, no filing and no corroborating outlet in this cycle's signal. Figures are internally consistent and the Inner Mongolia siting is plausible on power grounds, but the 160k chip count is NOT established. Related: [[deepseek-second-round-2026-07]], [[china-nvidia-h200-import-2026-07]]."
  - ts: 2026-11-03
    change: "Rumored / partial, unchanged — a second report that CONTRADICTS the original inference-only framing. @StarsLevels (2026-11-03 14:16 UTC), citing TrendForce and The Information, reports that DeepSeek plans to pre-train its next model, V5, mainly on Huawei Ascend 950 chips, using 160,000+ Ascend 950DT at a new data center in Ulanqab, Inner Mongolia. It says founder Liang Wenfeng has claimed four Ascend 950s match one NVIDIA GB300, that pre-training could start as soon as late 2026, and that V5 is expected in 2027. The 160K chip count and Inner Mongolia siting now have a second relay, but @ns123abc's 'training stays on NVIDIA' clause does not: this report puts training on Ascend. Neither DeepSeek nor Huawei has confirmed. The outlet attribution is from the relay, not the outlets' own posts, so verification stays partial."
---

Strip the headline number away and the interesting claim survives: Chinese
frontier labs appear to be converging on the same compute architecture, and it
is not the one export controls were designed to force.

The expectation behind the controls was substitution — cut off NVIDIA, and
Chinese labs either stop or move wholesale onto domestic accelerators. What
Zhipu confirmed in a filing and this report claims for DeepSeek is different:
segregate by workload. Inference, which is throughput-bound, latency-tolerant
and enormous in aggregate, runs on Ascend at 100k-plus scale. Training, which is
where interconnect and numerical precision bite hardest, stays on NVIDIA. That
lets a lab absorb almost all of its compute growth domestically while keeping
its frontier runs on the hardware that is hardest to replace.

Two loud caveats. This is one account with no corroboration — the specific
figures, especially 160,000 units, should not be repeated as fact. And a 1GW
site is a multi-year construction claim being reported as a purchase, which is
the kind of detail that tends to be either substantially early or substantially
wrong.

What would settle it: a Huawei or DeepSeek statement, provincial permitting or
grid-interconnect filings for the Inner Mongolia site, or a second independent
outlet.
