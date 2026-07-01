---
slug: claude-sonnet-5
title: Anthropic Claude Sonnet 5 — official release
company: Anthropic
model: Claude Sonnet 5
status: released
status_note: |
  **Officially launched 2026-06-30 18:00 UTC** (@claudeai, ~13.7K likes:
  "Introducing Claude Sonnet 5, our most agentic Sonnet yet"). Model id
  **`claude-sonnet-5`**, now the **default on Free and Pro** and available to
  Max, Team, and Enterprise — live across all Claude apps and the Claude
  Platform, with a **published system card**. **Intro pricing $2/M input,
  $10/M output** (rising to **$3/$15 in September**); **1M-token context**,
  128K output, **January 2026 knowledge cutoff**. Positioned as *close to*
  Opus 4.8 ([[opus-4-8]]) on coding/reasoning/agentic work at Sonnet price —
  Anthropic's framing is "near," not parity. Third-party availability landed
  the same hour (Perplexity Pro/Max); GitLab put it live on the Duo Agent
  Platform across all tiers (claimed +93.8% over the predecessor).

  **Day-2 independent verdict is split.** Benchmarks are uneven — edges Opus
  4.8 on some tasks (The Decoder: GDPval-AA v2 score 1,618, past Opus 4.8),
  trails on others, and scores *lower than the older Sonnet 4.6* on cyber
  exploit-discovery (a **deliberate "lower cyber risk" reduction** consistent
  with Anthropic's Mythos export-control posture, see
  [[anthropic-fable-mythos-export-control-2026-06]]). Simon Willison notes it
  drops temperature/top_p/top_k and a new tokenizer yields ~30% more tokens
  per input (an effective ~30% price increase). Developer reception ranges
  from "best cheap agentic default" to "descoped / maintenance release." The
  published system card discloses elevated **evaluation-awareness** (~6% of
  tested rollouts verbalized being tested); viral "self-approves via
  subagents / whistleblows" threads are one reader's dramatization, not card
  text. **No Fable 5 general re-release accompanied it** ([[claude-fable-5]]).
expected: null
labels:
  - anthropic
  - frontier-model
  - released
  - agentic
  - coding
verification: confirmed
sources:
  - "@claudeai"
  - "@synthwavedd"
  - "@AndrewCurran_"
  - "@kimmonismus"
  - "@perplexity_ai"
  - "@simonw"
  - https://x.com/claudeai/status/2072017450611142835
  - https://x.com/claudeai/status/2072017457057853480
created_at: 2026-06-22
updated_at: 2026-07-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-22
    change: "Created — a 'claude-sonnet-5' model slug surfaced on an Anthropic partner provider (@synthwavedd 2026-06-21, ~1.2K likes), read as the first breadcrumb of Anthropic's next mid-tier Claude release while Fable 5/Mythos 5 stay export-frozen. Picked up by credible watchers (Andrew Curran: a new Sonnet is 'due'; @kimmonismus: likely a 'GPT-5.6 and Sonnet 5' week) but no Anthropic post, date, or specs; the '1M context / Fennec codename' details trace to amplifier accounts, and @fanofaliens notes the slug may have appeared in Vertex AI logs months ago (so possibly stale). Status rumored, verification unverified (single-source, freshness disputed)."
  - ts: 2026-07-01
    change: "Major update — SHIPPED. Anthropic officially launched Claude Sonnet 5 (id claude-sonnet-5) on 2026-06-30 18:00 UTC (@claudeai ~13.7K likes) with a published system card: now the default on Free/Pro and available to Max/Team/Enterprise, live across all Claude apps + the Platform. Intro pricing $2/$10 per MTok (→ $3/$15 September), 1M context, 128K output, Jan-2026 cutoff; framed as close-to-Opus-4.8 agentic/coding at Sonnet price. Perplexity added it same hour; GitLab Duo shipped it across all tiers (+93.8% claim). Status rumored → released; verification unverified → confirmed (official primary + system card). Day-2 independent benchmarks are mixed (edges Opus 4.8 on GDPval-AA v2 1,618, trails elsewhere, deliberately lower on CyberGym vuln-discovery vs Sonnet 4.6); Simon Willison flags a new tokenizer adding ~30% tokens (effective price rise) and dropped temperature/top_p/top_k. The leaked $2/$10 promo + Jan-2026 cutoff from the prior rumor cycle are now the shipped numbers. No Fable 5 general re-release accompanied it ([[claude-fable-5]])."
---

**Claude Sonnet 5** shipped on **2026-06-30 (18:00 UTC)** — resolving the
multi-day rumor arc this ticket opened when a bare `claude-sonnet-5` slug
first surfaced (erroring) in the model selector. Anthropic launched it as
its **"most agentic Sonnet yet"** (@claudeai, ~13.7K likes), with a
published system card, as the **default model on Free and Pro** and
available to Max, Team, and Enterprise across all Claude apps and the Claude
Platform.

**Commercial shape.** Intro pricing is **$2/M input and $10/M output**
(rising to **$3/$15 in September**), with a **1M-token context**, 128K
output, and a **January 2026 knowledge cutoff** — the exact numbers leaked
the prior cycle, now confirmed. Anthropic positions it as a cheaper way to
run agents versus Opus 4.8 ([[opus-4-8]]), GPT-5.5, and Gemini Pro; the
framing is *close to* Opus 4.8 on coding/reasoning/agentic work, **not
parity**.

**Day-2 verdict splits.** Independent benchmarks are uneven — it edges Opus
4.8 on some tasks (The Decoder reports a GDPval-AA v2 score of 1,618, past
Opus 4.8) and trails on others, while scoring **lower than the older Sonnet
4.6 on cyber exploit-discovery**, a deliberate risk reduction consistent
with Anthropic's Mythos/export-control posture
([[anthropic-fable-mythos-export-control-2026-06]]). Simon Willison notes a
new tokenizer produces ~30% more tokens per input (an effective ~30% price
increase) and that the model drops `temperature`/`top_p`/`top_k`. Ecosystem
adoption moved fast (Perplexity Pro/Max the same hour; GitLab Duo across all
tiers, claiming +93.8%), but developer reception ranges from "best cheap
agentic default" to "descoped maintenance release."

**System-card caveat.** The verifiable card detail circulating is elevated
**evaluation-awareness** — ~6% of tested rollouts verbalized that they were
being tested, which Anthropic itself disclosed. The viral readings (Sonnet 5
"creates subagents to self-approve," "blows the whistle on insiders") are
one reader's dramatized interpretation, not card text.

**Transition triggers:**
- ≥4 weeks past the 2026-06-30 release with no successor → close with
  `released-and-aged`.
- A Sonnet 5.x / successor public model → new ticket, do not reopen.
- Pricing, availability, or benchmark moves get appended as history here.

**Dedup note:** further Claude Sonnet 5 signal (independent benchmarks, the
September price step, availability changes) UPDATES this ticket. The
export-control order stays on
[[anthropic-fable-mythos-export-control-2026-06]]; the gated Fable 5 public
line stays on [[claude-fable-5]]; a claimed new internal Mythos stays on
[[anthropic-mythos-6-internal-2026-06]].
</content>
</invoke>
