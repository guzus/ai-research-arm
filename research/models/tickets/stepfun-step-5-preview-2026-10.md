---
slug: stepfun-step-5-preview-2026-10
title: "StepFun Step-5-Preview — ~600B MoE, 1M context, API launch then open weights on Hugging Face"
company: "StepFun"
model: "Step-5-Preview"
status: released
status_note: |
  **Two independent secondary sources, no StepFun post in this signal.**
  @oscarsuiza (2026-10-15 11:45 UTC) reports open weights for
  `stepfun-ai/Step-5-Preview` on Hugging Face, last updated early on 15 Oct. It
  describes the API launch as earlier news. The benchmark scores on the model card
  are StepFun's own and Artificial Analysis figures. @JulianGoldieSEO (10:33 UTC)
  describes it as ~600B parameters, a sparse MoE with a 1M-token context, image and
  video input, and free for a limited launch window via OpenRouter, OpenCode, Cline
  and Kilo Code.

  **Status `released`, verification `partial`.** Two accounts independently describe
  public access (API and weights). This run could not reach Hugging Face to check the
  model card directly, and no StepFun primary was captured.
expected: "Released (API, then open weights ~2026-10-15). Open: StepFun primary announcement, licence, exact parameter/active counts, end of the free window, and independent benchmarks."
labels:
  - stepfun
  - open-weights
  - moe
  - china
  - long-context
verification: partial
sources:
  - "https://x.com/oscarsuiza/status/2110698495187316749"
  - "https://x.com/JulianGoldieSEO/status/2110680418379010264"
  - "https://huggingface.co/stepfun-ai/Step-5-Preview"
created_at: 2026-10-15
updated_at: 2026-10-15
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-15
    change: "Created — RELEASED / partial. Two independent secondary accounts describe StepFun's Step-5-Preview as publicly available. @oscarsuiza (2026-10-15 11:45 UTC) reports open weights on Hugging Face (stepfun-ai/Step-5-Preview, last updated early 15 Oct) following an earlier API launch, and warns that the model-card benchmarks are StepFun's and Artificial Analysis's. @JulianGoldieSEO (10:33 UTC) describes ~600B total parameters as a sparse MoE, a 1M-token context, image and video input, and free launch-window access via OpenRouter, OpenCode, Cline and Kilo Code. This is the first StepFun ticket in the set. Verification is partial because no StepFun post was captured and this run's sandbox could not reach huggingface.co to read the card. The Hugging Face URL is recorded as reported, not as fetched."
---
This is the first StepFun ticket in the set. StepFun is one of the Chinese labs
competing in large open-weight MoE releases, alongside DeepSeek, Qwen, Kimi and
Zhipu.

The described shape (~600B sparse MoE, 1M context, multimodal input, free launch
window on the agentic-coding routers) follows the standard playbook for a Chinese
open-weights launch this year. The detail to check is the benchmark provenance.
One source notes the model-card numbers are the vendor's own plus Artificial
Analysis figures, so independent coding evaluations are what would move this
ticket.

Verification can rise to `confirmed` once a StepFun post or the model card itself
is read directly.
