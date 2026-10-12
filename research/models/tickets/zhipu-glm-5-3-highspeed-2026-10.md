---
slug: zhipu-glm-5-3-highspeed-2026-10
title: "GLM-5.3-HighSpeed — ~490 tok/s serving variant gray-tested in ZCode"
company: "Zhipu AI / Z.ai"
model: "GLM-5.3-HighSpeed"
status: in-testing
status_note: |
  **Gray test, no announcement.** @leo114119 (2026-10-11 05:05 UTC) reports a
  **GLM-5.3-Highspeed** model in ZCode 3.15.1 at up to **490 TPS**, offered to
  random subscribers. @Z3nlyte (2026-10-12 15:11 UTC) restates it as ~7x the
  standard GLM-5.3 API, with the same 1M-context model and only serving speed
  changed.

  **Status `in-testing`:** a selectable model in a shipping client for a random
  subset of subscribers is a real artifact, not a tease. **Verification
  `partial`:** two secondary accounts, one quoting the other; no Zhipu post.

  **Lineage.** The GLM-5.3 / GLM-5.3-Flash release is tracked on the closed
  [[zhipu-glm-5-3-2026-08]]. That ticket is left untouched. This is a new serving
  tier, not a new model.
expected: "No date. Watch for a Zhipu announcement, general availability in ZCode or the API, and pricing."
labels:
  - zhipu
  - glm
  - inference-speed
  - gray-test
verification: partial
sources:
  - "https://x.com/leo114119/status/2109148486239215803"
  - "https://x.com/Z3nlyte/status/2109663128648589784"
created_at: 2026-10-12
updated_at: 2026-10-12
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-12
    change: "Created — IN-TESTING / partial. @leo114119 (2026-10-11) and @Z3nlyte (2026-10-12) report GLM-5.3-HighSpeed randomly enabled for ZCode 3.15.1 subscribers at ~490 tok/s, ~7x the standard GLM-5.3 API, same 1M-context model. No Zhipu announcement. Distinct serving-tier artifact; the base model is on the closed [[zhipu-glm-5-3-2026-08]]."
---

Speed tiers are now a release axis in their own right. xAI and Cursor already ship
fast variants per effort level, and a 7x serving-speed tier of the same weights
changes what long agent runs cost in wall-clock time.
