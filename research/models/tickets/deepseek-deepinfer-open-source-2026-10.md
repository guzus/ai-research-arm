---
slug: deepseek-deepinfer-open-source-2026-10
title: "DeepSeek open-sources DeepInfer, the inference framework behind V4.1-Flash"
company: DeepSeek
model: DeepInfer (inference framework)
status: released
status_note: |
  **Primary announcement, 2026-10-20 09:30 UTC (@deepseek_ai, ~11.7K likes):**
  "Introducing DeepInfer, our in-house inference framework, now fully open source!
  Powering DeepSeek-V4.1-Flash at scale with high throughput and low latency."

  **Scope, per @teortaxesTex's translation of the Chinese announcement.** DeepInfer
  supports distributed inference, speculative decoding, "SWA Bounded Replay" and
  structured output, and runs on both NVIDIA and Huawei Ascend. It ships with
  deepseek-recipe, a token encoding/decoding component that DeepSeek says matches its
  official API's processing. DeepSeek says inference code for future models will be
  released in the same repository. A technical report is on Zhihu. Repository URLs
  are t.co-shortened in signal and were not resolved here.
expected: "Released 2026-10-20 (open source). Watch: licence, third-party adoption (vLLM / SGLang comparisons), and whether the next DeepSeek model ships its inference code here on day one."
labels:
  - deepseek
  - open-source
  - inference
  - huawei-ascend
  - released
verification: confirmed
sources:
  - "https://x.com/deepseek_ai/status/2112476496283775135"
  - "https://x.com/teortaxesTex/status/2112493775465443641"
  - "https://x.com/cheese_cakee_9/status/2112506742257205556"
created_at: 2026-10-20
updated_at: 2026-10-20
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-20
    change: "Created — RELEASED / confirmed. @deepseek_ai (2026-10-20 09:30 UTC) open-sourced DeepInfer, its production inference framework for DeepSeek-V4.1-Flash, plus the deepseek-recipe encode/decode component. Per the translated Chinese announcement (@teortaxesTex): distributed inference, speculative decoding, SWA Bounded Replay, structured output; NVIDIA and Huawei Ascend support; future DeepSeek models' inference code to land in the same repo. Related model ticket: [[deepseek-v4-1-flash-1017-2026-10]]."
---

DeepSeek has now open-sourced each layer of its serving stack: model weights, the
TileLang compiler, an operator library and, as of today, the inference framework
itself. DeepSeek presents DeepInfer as the system that runs V4.1-Flash in
production, so outside deployments can match the first-party API's
behaviour, not just its weights.

Ascend support matters most for Chinese deployments. A production-grade engine that
runs on both NVIDIA and Huawei hardware makes domestic-chip serving of DeepSeek
models easier, which ties into [[deepseek-huawei-ascend-950dt-2026-09]].

Every performance claim so far is DeepSeek's own. Nothing in signal benchmarks
DeepInfer against vLLM or SGLang yet.

**Transition triggers:** independent throughput/latency comparisons or major
adopters → UPDATE; about four weeks after release → close as released-and-aged.
