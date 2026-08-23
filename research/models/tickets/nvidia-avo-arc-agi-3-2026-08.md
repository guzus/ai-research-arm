---
slug: nvidia-avo-arc-agi-3-2026-08
title: NVIDIA's AVO coding agent scores 100% on the ARC-AGI-3 public set
company: NVIDIA
model: AVO (agent architecture, on Claude Opus 5)
status: confirmed
status_note: |
  **NVIDIA's AVO**, a general-purpose coding agent, **completed all 183
  levels across the 25 public ARC-AGI-3 games** — a 100% public-set
  score. Reported by @testingcatalog (2026-08-21 14:28 UTC) and
  @kimmonismus, and amplified by Hugging Face CEO **@ClementDelangue**:
  "NVIDIA built its own coding harness to optimize CUDA GPU kernels and
  achieved a 100% score on ARC-AGI-3's 25 public games."

  **The load-bearing detail is the model/harness split.** Per @mark_k,
  **Claude Opus 5 scores ~30% on ARC-AGI-3 as a bare model baseline**;
  placed inside AVO — with persistent memory, supervision, tools, and a
  long-horizon execution loop — it reaches 100%. The agent receives no
  rules or stated goals and must learn by acting, observing and
  correcting; AVO's claimed edge is *retaining* what it learned across
  context resets instead of restarting.

  The same architecture is credited with a prior result: **seven days of
  autonomous GPU-kernel optimization**, 500+ directions explored,
  producing kernels reported to beat **FlashAttention-4 by up to 10.5%**.

  Status `confirmed` (multiple independent relays plus an amplifying
  primary in @ClementDelangue); verification `partial` — no NVIDIA
  primary post, technical report, or **ARC Prize verification** was
  captured, and the ARC-AGI-3 *public* set is the tuning set, not the
  semi-private/private evaluation. @testingcatalog's own one-word
  reaction was "Oversaturated 👀", which is the right caution: a 100% on
  a public split is a claim about the harness fitting the benchmark
  until a held-out score exists.
expected: "Reported 2026-08-21 as 100% on the ARC-AGI-3 public set (183/183 levels, 25 games). Pending: an NVIDIA primary post or technical report, ARC Prize verification, a semi-private/private-set score, and whether AVO is released or stays internal"
labels:
  - nvidia
  - agentic
  - benchmark
  - arc-agi
  - harness
verification: partial
sources:
  - "@testingcatalog"
  - "@kimmonismus"
  - "@mark_k"
  - "@ClementDelangue"
  - "@huggingface"
created_at: 2026-08-23
updated_at: 2026-08-23
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-23
    change: "Created — NVIDIA's AVO general-purpose coding agent reported completing all 183 levels across the 25 public ARC-AGI-3 games, a 100% public-set score (@testingcatalog 2026-08-21 14:28 UTC, @kimmonismus, amplified by Hugging Face CEO @ClementDelangue). Key datapoint per @mark_k: Claude Opus 5 scores ~30% on ARC-AGI-3 as a bare model but reaches 100% inside AVO's persistent-memory, supervised, long-horizon loop — the same architecture previously credited with 7 days of autonomous GPU-kernel optimization producing kernels up to 10.5% faster than FlashAttention-4. Status confirmed on multiple independent relays plus an amplifying primary; verification partial — no NVIDIA primary post or technical report, no ARC Prize verification, and the public set is the tuning split rather than a held-out evaluation (@testingcatalog: 'Oversaturated')."
---

This ticket is in the model lane because of what it claims about **where
capability now comes from**, not because of the score itself.

The reported gap is the whole argument: the same model — Claude Opus 5
([[anthropic-opus-5-leak-2026-07]]) — goes from roughly 30% to 100% on
the same benchmark depending only on the scaffolding around it. If that
holds, the frontier being measured is the *system*, not the weights, and
model-vs-model leaderboards under-describe deployed capability by a
large factor.

**Two reasons to hold it loosely.** First, ARC-AGI-3's public set is the
split you are allowed to tune against; the semi-private and private sets
exist precisely because saturating the public one is achievable by
fitting. No held-out number has been published, and ARC Prize has not
verified the run in anything captured here. Second, every figure in
circulation — the 30% baseline, the 100%, the FlashAttention-4 margin —
traces to secondary relays. NVIDIA has not posted a technical report.

**The kernel-optimization precedent is the more checkable claim** and
points the same direction: a seven-day autonomous loop exploring 500+
directions is a statement about long-horizon persistence and tool use,
which is exactly what the ARC-AGI-3 setup rewards (no stated rules,
learn by acting, survive context resets). Both results are about memory
and loop design.

That reading has independent support in the same window from an
unrelated direction: @alexocheema describes non-experts using cheap
agents to port CUDA kernels to other hardware in "a fairly simple
autoresearch loop," because kernel performance is objectively
measurable by running it. Verifiable reward plus a persistent loop is
the pattern.

Related: [[anthropic-opus-5-leak-2026-07]],
[[nvidia-open-secure-ai-alliance-2026-07]],
[[nvidia-nemotron-openrouter-2026-06]].
