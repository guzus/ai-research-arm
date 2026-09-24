---
slug: anthropic-opus-5-5-2026-09
title: Claude Opus 5.5 — first model in the Claude 5.5 family, public release
company: Anthropic
model: Claude Opus 5.5
status: released
status_note: |
  Shipped 2026-09-22 16:31 UTC. @AnthropicAI: "Claude Opus 5.5 is available
  today." @ClaudeDevs, same hour: "Opus 5.5 performs at the level of Fable 5.1.
  It's ~30% faster and ~40% cheaper than Opus 5 per task" and "available now in
  Claude Code and the Claude Platform... our new daily driver for coding and
  agentic work."

  The @claudeai launch post (relayed verbatim by @arankomatsuzaki) frames it as
  "the first model in our new Claude 5.5 family" — so this is a family opener,
  not a point release, which is what makes the stealth-tested Sonnet 5.5
  ([[anthropic-sonnet-5-5-2026-09]]) a plausible second entry rather than a
  rumour with no scaffolding behind it.

  Product terms shipped with it, per @ClaudeDevs and @trq212 (Anthropic): 5-hour
  Claude Code session limits up 20%; the lower price means the same limit goes
  ~25% further; Pro, Max and Team users got a banked reset. Safeguards: the
  first Opus carrying Fable 5.1-class safeguards on cyber, bio and frontier-LLM
  development, with flagged requests falling back to another model — a
  user-visible behaviour third parties are already hitting ("i get cyber gated
  by opus 5.5 so right now I'm stuck with opus 4.8", @polydaic 2026-09-24).

  Third-party positioning is unusually consistent for a launch week. @rauchg's
  Next.js eval tally (2026-09-22): Opus 5.5 97%, GPT-6 Sol 97%, Fable 5.1 97%,
  Grok 4.7 94%. @danshipper (Every) tested it before launch and called it better
  than Fable 5.1 on writing, instruction-following and long-context work, and
  said it pulled some of their Codex converts back. @AravSrinivas made it the
  "Standard" effort orchestrator on Perplexity Computer for Pro and Max.
expected: "Released and GA. Open question is the rest of the 5.5 family — Sonnet 5.5 is already stealth-tested ([[anthropic-sonnet-5-5-2026-09]])."
labels:
  - anthropic
  - frontier-model
  - released
  - claude-5-5-family
verification: confirmed
sources:
  - https://x.com/AnthropicAI/status/2102435703535939725
  - https://x.com/ClaudeDevs/status/2102438800836489554
  - https://x.com/ClaudeDevs/status/2102438807698370775
  - https://x.com/ClaudeDevs/status/2102438808952467507
  - https://x.com/trq212/status/2102437686967738431
  - https://x.com/arankomatsuzaki/status/2102445494735982603
  - https://x.com/rauchg/status/2102519097770885231
  - https://x.com/danshipper/status/2102509857870155878
  - https://x.com/AravSrinivas/status/2102440114295369796
  - https://x.com/davis7/status/2102973164494139663
  - https://x.com/cgtwts/status/2102761743168811489
  - https://x.com/polydaic/status/2103086632895385823
created_at: 2026-09-24
updated_at: 2026-09-24
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — RELEASED. Anthropic shipped Claude Opus 5.5 on 2026-09-22 16:31 UTC (@AnthropicAI: \"Claude Opus 5.5 is available today\"), live immediately in Claude Code and on the Claude Platform. Anthropic's own claims (@ClaudeDevs): performs at Fable 5.1 level, ~30% faster and ~40% cheaper than Opus 5 per task; 5-hour Claude Code limits up 20%, effective limit up a further ~25% from the lower price, plus a banked reset for Pro/Max/Team. First Opus with Fable 5.1-class cyber/bio/frontier-LLM safeguards, flagged requests falling back to another model. @claudeai framed it as \"the first model in our new Claude 5.5 family.\" Verification confirmed on company-primary posts. Independent corroboration inside 48h: @rauchg's Next.js eval (Opus 5.5 97%, GPT-6 Sol 97%, Fable 5.1 97%, Grok 4.7 94%); @danshipper (Every) rated it above Fable 5.1 on writing/instruction-following/long context; @AravSrinivas made it Perplexity Computer's Standard-effort orchestrator. Created late: no ticket existed for this release, and the 2026-09-23 run recorded no changes across the whole set, so the gap is being closed now while the launch is still generating daily signal."
---

Anthropic shipped Claude Opus 5.5 on 2026-09-22, and the framing matters more
than the benchmark line: @claudeai called it "the first model in our new Claude
5.5 family." Opus has historically been the expensive tier that a cheaper
Sonnet or a smarter Fable flanked. Opening a *family* with Opus, priced ~40%
below Opus 5 and claimed at Fable 5.1's capability level, collapses that
ladder — and the Sonnet 5.5 stealth test surfaced two days later
([[anthropic-sonnet-5-5-2026-09]]) is the shape you would expect if the rest of
the family is already trained.

The commercial claim is per-task, not per-token, and both were stated: cheaper
per token than Opus 5.0 *and* "very token efficient" (@trq212). That pairing is
what produces the ~40%-cheaper-per-task number, and it is the axis competitors
answered on the same day — OpenAI's GPT-6 Sol and Luna shipped roughly 90
minutes later with a permanent 50% API price cut ([[openai-gpt-6]]).

The safeguards change is the part with a visible cost. Opus 5.5 is the first
Opus carrying Fable 5.1-class safeguards on cyber, bio and frontier-LLM
development; Anthropic said up front that flagged requests fall back to another
model and that it is "working to reduce incorrect flags." Users are already
reporting exactly that failure mode in normal coding work. Read alongside
[[anthropic-pace-the-frontier-2026-09]], the release is Anthropic arguing that
pacing and shipping are not in tension — a claim several observers found
strained ("Dario: we need to slow down AI development / Anthropic a week later:
introducing Claude Opus 5.5", @cgtwts).

Distinct from [[anthropic-opus-5-leak-2026-07]] (Opus 5, closed) and
[[anthropic-claude-fable-5-1-2026-08]] (Fable 5.1, the model Opus 5.5 is
benchmarked against). This ticket tracks the 5.5 release and the family it
opens.
