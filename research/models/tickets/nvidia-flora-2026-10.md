---
slug: nvidia-flora-2026-10
title: "NVIDIA open-sources Flora — open model suite that labels robot and human video for robotics data engines (used to train GR00T)"
company: "NVIDIA"
model: "Flora"
status: released
status_note: |
  **Announcement from NVIDIA's robotics lead.** @DrJimFan (NVIDIA, 2026-10-20 17:31 UTC):
  "Introducing Flora, a suite of open models to parse the physical world and turn raw
  footage into rich training signals", with weights open-sourced the same day. Claimed:
  "Astra-level performance at 125x lower cost"; already powers NVIDIA's in-house data
  engine, labeling 200K hours of video a day on 500 GPUs.

  **What it outputs.** Timestamped captions to curate and filter egocentric human and
  robot data, dense progress rewards for quality control and RL post-training, and
  rubric scoring for real-world benchmarking. NVIDIA researcher @yunzeman's technical
  thread says it is used to train NVIDIA GR00T.

  "Astra-level" presumably means GPT-6 Astra as an annotator; the 125x cost figure is
  NVIDIA's own and was not independently measured.
expected: "Released 2026-10-20 (open weights). Open: licence terms, independent comparisons of annotation quality against frontier-model labelers, and outside adoption."
labels:
  - nvidia
  - robotics
  - open-weights
  - data-engine
  - gr00t
verification: confirmed
sources:
  - "https://x.com/DrJimFan/status/2112597587987689912"
  - "https://x.com/DrJimFan/status/2112597589388652719"
  - "https://x.com/DrJimFan/status/2112597590571450505"
created_at: 2026-10-21
updated_at: 2026-10-21
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-21
    change: "Created — RELEASED / confirmed. @DrJimFan (NVIDIA, 2026-10-20 17:31 UTC) open-sourced Flora, a suite of models that annotate robot and human video with timestamped captions, dense progress rewards and rubric scores. NVIDIA claims Astra-level labeling at 125x lower cost; it labels 200K hours of video a day on 500 GPUs in NVIDIA's own data engine and is used to train GR00T (@yunzeman thread). Cost/quality claims are NVIDIA's own."
---

Robot learning is data-limited, and most of the cost is turning raw footage into
labelled, filtered, reward-annotated training data. Flora is NVIDIA releasing the
labeler rather than a robot policy. If the quality claim holds, teams that today pay
a frontier API to caption video can run the job on their own GPUs.

It fits NVIDIA's pattern of open-sourcing the tooling around its robotics stack
(GR00T, Cosmos, the SONIC humanoid model in [[nvidia-sonic-humanoid-model-2026-09]]).
