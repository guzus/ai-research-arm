---
slug: anthropic-opus-5-5-2026-09
title: Claude Opus 5.5 — first model in the Claude 5.5 family, public release
company: Anthropic
model: Claude Opus 5.5
status: released
status_note: |
  **2026-09-25 — first independent benchmark and market-share data, 48h
  after ship.** Three measurements landed, all from parties that are not
  Anthropic:
  - **SimpleBench: 88.4%, highest score on the board** (@AiBattle_, 2026-09-24
    17:16 UTC).
  - **Terminal-Bench-Science 0.1: 62% at xhigh, second** — @ArtificialAnlys
    launched the leaderboard 2026-09-24 23:30 UTC with GPT-6 Astra (max) top at
    63%. 70 expert-curated tasks over five scientific domains, built with
    Stanford and the terminal-bench team. A one-point gap on a 70-task benchmark
    is not a ranking.
  - **Vercel AI Gateway spend: Opus 5.5 reached up to 10% of all spend in two
    days** (@rauchg, 2026-09-24). Same dataset shows Anthropic's overall share
    falling 69% -> 40% over two months while OpenAI went 10% -> 24%, with Kimi K3
    and DeepSeek taking roughly half of Anthropic's loss — so Opus 5.5 is a sharp
    recovery inside a declining share, not a reversal of it.

  **Vision is the capability claim with the most specific third-party support.**
  @skalskip92 ran it as a vision model and reported it beats Fable 5.1 (high) on
  detection +11.84pp and reasoning +12.80pp at ~60% lower estimated cost, and
  beats GPT-6 Sol (high) on extraction +11.00pp and reasoning +7.95pp, while
  still losing to GPT-6 Astra. Single evaluator, own harness.

  **A reproducible operational finding worth recording: `xhigh` outperforms
  `max`.** @theo, 2026-09-25: "Opus 5.5 scores higher with xhigh than it does
  with max. I HIGHLY recommend avoiding 'max' reasoning" — because max sets a
  reasoning-effort *minimum*, so it prevents the model from spending less on easy
  sub-tasks. Anthropic's own leaderboard submission also used xhigh. This is the
  same class of footgun as the effort-mapping bug at
  [[anthropic-claude-code-effort-mapping-2026-08]]: a knob whose label implies
  "better" and whose behaviour is "floor".

  **Usage limits are the other half of the reception.** Multiple developers
  independently report limits that feel effectively unlimited — @theo ran a
  13-hour continuous goal without hitting usage, @davis7 and @kimmonismus say the
  same. Recorded as widespread first-hand report, not as a published policy
  change; Anthropic has published no limit change.

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
expected: "Released and GA, with first independent benchmarks in: SimpleBench 88.4% (1st), Terminal-Bench-Science 0.1 62% at xhigh (2nd, one point behind GPT-6 Astra), up to 10% of Vercel AI Gateway spend within 48h. Open: the rest of the 5.5 family — Sonnet 5.5 is already stealth-tested ([[anthropic-sonnet-5-5-2026-09]]) and users are already asking for Fable 5.5; an Anthropic statement on whether usage limits actually changed; and independent reproduction of the vision deltas."
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
  - https://x.com/AiBattle_/status/2103171713672372379
  - https://x.com/ArtificialAnlys/status/2103265956479070260
  - https://x.com/rauchg/status/2103216656747262419
  - https://x.com/skalskip92/status/2103124154765484505
  - https://x.com/theo/status/2103274408567881948
created_at: 2026-09-24
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-24
    change: "Created — RELEASED. Anthropic shipped Claude Opus 5.5 on 2026-09-22 16:31 UTC (@AnthropicAI: \"Claude Opus 5.5 is available today\"), live immediately in Claude Code and on the Claude Platform. Anthropic's own claims (@ClaudeDevs): performs at Fable 5.1 level, ~30% faster and ~40% cheaper than Opus 5 per task; 5-hour Claude Code limits up 20%, effective limit up a further ~25% from the lower price, plus a banked reset for Pro/Max/Team. First Opus with Fable 5.1-class cyber/bio/frontier-LLM safeguards, flagged requests falling back to another model. @claudeai framed it as \"the first model in our new Claude 5.5 family.\" Verification confirmed on company-primary posts. Independent corroboration inside 48h: @rauchg's Next.js eval (Opus 5.5 97%, GPT-6 Sol 97%, Fable 5.1 97%, Grok 4.7 94%); @danshipper (Every) rated it above Fable 5.1 on writing/instruction-following/long context; @AravSrinivas made it Perplexity Computer's Standard-effort orchestrator. Created late: no ticket existed for this release, and the 2026-09-23 run recorded no changes across the whole set, so the gap is being closed now while the launch is still generating daily signal."
  - ts: 2026-09-25
    change: "Released and GA, unchanged. First independent measurements, 48h after ship, all third-party: SimpleBench 88.4%, the highest score on that board (@AiBattle_, 2026-09-24 17:16 UTC, ~671 likes); Terminal-Bench-Science 0.1 at 62% with xhigh, SECOND behind GPT-6 Astra (max) at 63% on @ArtificialAnlys's newly launched leaderboard (2026-09-24 23:30 UTC, ~743 likes) — 70 expert-curated tasks across five scientific domains built with Stanford and the terminal-bench team, and a one-point gap there is not a ranking; and up to 10% of ALL spend on the Vercel AI Gateway within two days (@rauchg, 2026-09-24, ~733 likes). The gateway data is recorded with its context rather than as a win: Anthropic's overall share fell 69% -> 40% over two months while OpenAI rose 10% -> 24% and Kimi K3 plus DeepSeek absorbed roughly half of Anthropic's loss, so Opus 5.5 is a sharp recovery inside a declining share. Vision: @skalskip92 reports Opus 5.5 beating Fable 5.1 (high) by +11.84pp detection and +12.80pp reasoning at ~60% lower estimated cost, and GPT-6 Sol (high) by +11.00pp extraction and +7.95pp reasoning, while still losing to GPT-6 Astra — single evaluator, own harness, recorded as one data point. Operationally important and reproducible: xhigh outperforms max, because max imposes a reasoning-effort MINIMUM and blocks the model from spending less on easy sub-tasks (@theo, 2026-09-25); Anthropic's own leaderboard entry used xhigh. Same knob-semantics trap as [[anthropic-claude-code-effort-mapping-2026-08]]. Finally, multiple independent developers (@theo with a 13-hour continuous goal, @davis7, @kimmonismus) report usage limits that feel effectively unlimited — logged as consistent first-hand report only; Anthropic has published no limit change."
  - ts: 2026-09-25
    change: "Bookkeeping — citations added for the 2026-09-25 entry: @AiBattle_ (SimpleBench 88.4%), @ArtificialAnlys (Terminal-Bench-Science 0.1 leaderboard launch), @rauchg (Vercel AI Gateway spend shares), @skalskip92 (vision deltas vs Fable 5.1 and GPT-6 Sol), @theo (xhigh outperforms max because max sets a reasoning-effort floor). No status, verification or content change."
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
