---
slug: minimax-m3-1-flash-2026-10
title: "MiniMax M3.1 Flash — the stealth 'Space Bunny' model, now named and on sale"
company: MiniMax
model: MiniMax-M3.1-Flash
status: released
status_note: |
  **Identity confirmed by MiniMax.** @MiniMax_AI (2026-10-19 09:21 UTC): "Welcome back.
  Space Bunny. 🚀 MiniMax-M3.1-Flash is coming." This settles the attribution of the
  anonymous OpenRouter model tracked (and closed as stale) in
  [[minimax-space-bunny-alpha-2026-09]].

  **Availability and price come from secondary accounts only.** @cdiamond (13:36 UTC)
  says M3.1 Flash "launched today" at $0.15 / $0.60 per 1M input / output tokens on the
  pay-as-you-go API, with MiniMax docs showing how to run it inside Claude Code and Codex
  on its M Plan subscription; thinking must stay on, and the Codex guide recommends a
  512K working context out of 1M. @kreoxi (13:34 UTC) says OpenCode confirmed the
  identity and is serving it free for three days, and that in the window to 2026-10-05
  it served ~106T tokens on OpenCode's board (vs ~62T for DeepSeek V4.1 Flash).
  @Startup_Fortune says it was folded into MiniMax Code on 2026-09-27 with no
  announcement. Benchmarks cited (Terminal-Bench 4.0, CyberGym, DeepSWE) are
  company-reported.
expected: "Live per secondary reports; open weights, a model card and independent benchmarks unconfirmed. A larger 'pro' sibling is being asked about in replies to MiniMax staff."
labels:
  - minimax
  - stealth-model
  - coding
  - long-context
  - china
verification: partial
sources:
  - "https://x.com/MiniMax_AI/status/2112111925975032241"
  - "https://x.com/window98se/status/2112147985501180193"
  - "https://x.com/cdiamond/status/2112176087488737422"
  - "https://x.com/kreoxi/status/2112175517608669358"
  - "https://x.com/Startup_Fortune/status/2112141214397137222"
created_at: 2026-10-19
updated_at: 2026-10-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-19
    change: "Created — RELEASED / partial. Successor to the closed [[minimax-space-bunny-alpha-2026-09]] (closed 2026-10-13 as stale-rumor-unverified, with the standing condition that a primary-sourced signal open a successor). Condition met: @MiniMax_AI (2026-10-19 09:21 UTC) names Space Bunny as MiniMax-M3.1-Flash. Status is released because several independent accounts report it live the same day: pay-as-you-go API at $0.15/$0.60 per MTok (@cdiamond), free for three days on OpenCode (@kreoxi), and inside MiniMax Code since 2026-09-27 (@Startup_Fortune). Verification is partial because MiniMax's own post says 'coming' and the launch, price and token-volume figures come only from secondary accounts."
---

MiniMax ran M3.1 Flash anonymously as "Space Bunny" on OpenRouter and OpenCode for
about two weeks before naming it. The earlier ticket closed as stale because nobody
claimed the model in 15 days. The lesson is that heavy, unbranded usage was a real
signal even though no source confirmed it at the time.

The spec matches what the stealth listing showed: 1M-token context, image and video
input, and a pitch as a fast coding model. The commercial angle is MiniMax publishing
guides to run it inside rival harnesses (Claude Code, Codex). Developers keep the agent
they know, and MiniMax supplies the cheaper inference behind it.

The usage numbers are the most interesting claim and also the weakest. The 106T-token
figure is relayed from OpenCode's board by one account and has not been checked here.

**Transition triggers:** a MiniMax launch post, model card or pricing page →
verification confirmed; independent benchmark placements → note here; released
publicly ≥4 weeks → close as released-and-aged.
