---
slug: alibaba-qwen-3-8-27b-2026-08
title: Qwen3.8-27B — dense open-weight model running frontier-adjacent agentic work on consumer hardware
company: Alibaba
model: Qwen3.8-27B
status: released
status_note: |
  **Qwen3.8-27B is out and is the dominant open-weights story of the
  cycle.** Evidence in the 2026-08-17→19 window is ecosystem-level rather
  than announcement-level: the Unsloth GGUF build is **#2 trending on
  Hugging Face with ~2.7M downloads** (@UnslothAI), Hugging Face itself
  crossed **3M models on the Hub** the same week, and practitioner reports
  put it on **~$2–3K of hardware** (RTX 5090 / 3090s / DGX Station at
  2,713 tok/s aggregate, 88 tok/s single-stream at BF16).

  **Claimed placement:** ~**51 on the Artificial Analysis Agentic Index**,
  reported ahead of GLM 5.2 and DeepSeek V4 Pro 0813 and behind only a
  handful of far larger SOTA models (@TheAhmadOsman). @kimmonismus calls it
  "the DeepSeek moment for open source." Treat the index number as
  community-relayed — no neutral benchmark org's own primary post was
  captured in-window.

  **The strongest counter-evidence is also in-window and comes from a
  careful source.** @emollick, testing it directly: "really good local
  model but, when you use it, it is immediately absolutely and obviously
  nowhere near as good as the other models listed here for agentic tasks,
  and especially for the kinds of complex tasks that GDPval-AA purports to
  measure. Do your own benchmarking!" So the honest state is: real
  capability jump for a 27B dense model, contested on whether the agentic
  leaderboard placement survives hands-on use.

  **Safety surface.** A refusal-removed ("abliterated") build shipped as
  MLX in 2/4/6/8-bit and runs locally on Apple Silicon; the uploader claims
  zero refusals at 4/6/8-bit while preserving vision, reasoning and
  tool-calling across a 262K context, and @kimmonismus reports even its
  creators warn it will produce malware, fraud and weapons instructions on
  demand. It trended as its own AI news item. This is a derivative of the
  same weights, so it is tracked here rather than as a separate ticket.
expected: "Shipped — weights on Hugging Face, GGUF/MLX/Unsloth builds live, running on consumer GPUs and Apple Silicon. Pending: a captured primary Qwen/Alibaba model card or launch post, and a neutral benchmark org's own agentic-index publication rather than community relays"
labels:
  - open-weights
  - china
  - local-inference
  - agentic
  - released
verification: partial
sources:
  - "@UnslothAI"
  - "@kimmonismus"
  - "@TheAhmadOsman"
  - "@emollick"
  - "@LottoLabs"
  - "@alecqfong"
  - "@Hikari_07_jp"
  - "@huggingface"
created_at: 2026-08-19
updated_at: 2026-08-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-19
    change: "Created — Qwen3.8-27B is shipped and is the cycle's dominant open-weights release. Unsloth GGUF #2 trending on Hugging Face at ~2.7M downloads (@UnslothAI 2026-08-18); reported ~51 on the Artificial Analysis Agentic Index, ahead of GLM 5.2 and DeepSeek V4 Pro 0813 (@TheAhmadOsman); runs on ~$2-3K hardware (RTX 5090; DGX Station at 2,713 tok/s aggregate per @alecqfong); DFlash 2 hits 70 tok/s for it on an M5 Max MacBook Pro. @kimmonismus: the DeepSeek moment for open source. Counter-evidence logged from @emollick, who says hands-on it is obviously not near the larger models on complex agentic tasks. A refusal-removed MLX build (2/4/6/8-bit, 262K context) also trended, with its own uploader warning it answers malware/fraud/weapons prompts — tracked here as a derivative of the same weights. Status released; verification partial (no primary Qwen/Alibaba post or neutral benchmark-org publication captured in-window)."
---

**Qwen3.8-27B** is the open-weights event of the cycle, and the thing that
makes it one is the hardware floor rather than the leaderboard row: a
**dense 27B** model that community reports put in agentic company with
models "several to tens of times its size," running on a single consumer
GPU. @TheAhmadOsman's framing — "runs on ~2-3k USD hardware btw. Permanent
underclass is officially cancelled" — is the sentiment the release
generated.

**What is actually verified.** Distribution is: the Unsloth GGUF build hit
**#2 trending on Hugging Face at ~2.7M downloads**, Unsloth reached #3
trending on GitHub off the back of it, and independent operators posted
working numbers — 2,713 tok/s aggregate / 88 tok/s single-stream at BF16 on
a DGX Station, and 70 tok/s on an M5 Max MacBook Pro via the DFlash 2
diffusion-decoding release. Multiple people one-shot non-trivial artifacts
with it (a mobile 2D platformer with sound, physics, checkpoints and
enemies; a Metal Slug emulator). That much is multi-sourced and firsthand.

**What is not.** The headline **~51 on the Artificial Analysis Agentic
Index**, ahead of GLM 5.2 and DeepSeek V4 Pro 0813, reached us through a
community account relaying a screenshot, not through Artificial Analysis's
own post. And no primary Qwen or Alibaba announcement was captured in the
window at all — the release is visible entirely through its ecosystem. That
is why `verification` is `partial` despite the release itself being
unambiguous.

**The dissent is worth more than the hype.** @emollick used it and reported
the opposite of the leaderboard story: obviously behind larger models on
complex agentic tasks, with an explicit "do your own benchmarking." A 27B
dense model topping an agentic index while underperforming hands-on is
exactly the shape a contaminated or narrow benchmark produces, and nobody
has yet run the check. Both claims stay on the record here until someone
does.

**The abliterated build is part of this ticket, not a separate one.** A
refusal-removed MLX conversion (2/4/6/8-bit, vision and tool-calling
preserved, 262K context) trended as its own news item, with its own
uploader warning it will supply malware, fraud and weapons instructions on
demand. It is a derivative of these weights and belongs to the same
shipping artifact; if it produces a distinct regulatory or platform
response, that gets its own ticket.

**Context.** This lands in the same week that OpenAI publicly paused
frontier RL training ([[openai-frontier-rl-pause-2026-08]]) and that
Zhipu shipped GLM-5.3 ([[zhipu-glm-5-3-2026-08]]) — @kimmonismus's read is
that the open tier is now close enough that a US slowdown is a Chinese
opening.

**Transition triggers:**
- A captured primary Qwen/Alibaba model card or launch post → UPDATE,
  advance `verification` to `confirmed`.
- Artificial Analysis or another neutral org publishes the agentic index
  placement directly → UPDATE.
- A successor (Qwen 3.9 / Qwen 4 class) → new ticket; do not reopen.
- ≥4 weeks past release with the debate settled → `closed: released-and-aged`.

**Dedup note:** the **Max** tier is a different artifact and stays on
[[alibaba-qwen-3-8-max-2026-07]]. Other open-weight contenders stay on
their own tickets ([[zhipu-glm-5-3-2026-08]], [[moonshot-kimi-k3]]).
