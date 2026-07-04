---
slug: claude-fable-5
title: Claude Fable 5 — public release of the Mythos-class model
company: Anthropic
model: Claude Fable 5
status: released
status_note: |
  **Publicly released 2026-06-09** (@claudeai 17:08 UTC: "Introducing Claude
  Fable 5: a Mythos-class model that we've made safe for general use. Its
  capabilities exceed those of any model we've ever made generally available.").
  Fable 5 is the **public-safe derivative of the Mythos class** ([[mythos-public-release]]):
  same frontier intelligence, wrapped in safety classifiers that **block or
  downgrade high-risk prompts** (cybersecurity, biology, chemistry, model
  distillation) and silently fall back to **Opus 4.8** ([[opus-4-8]]) — reported
  to trigger in **<5% of sessions**. The unrestricted twin, **Mythos 5**, ships
  only to vetted defenders / governments and stays tracked on
  [[mythos-public-release]]. Pricing **$10 / $50 per MTok** in/out (less than half
  the prior Mythos Preview's $25/$125). **Free for Pro / Max / Team until
  2026-06-22**, then usage credits required. Anthropic also introduced a new
  **30-day data-retention** policy across Fable/Mythos traffic. Available via
  the Claude apps, Claude API, Claude Code, and major cloud platforms.
  **2026-06-11/12 update:** after disclosing that Fable 5 would *silently*
  nerf AI/ML development tasks (pretraining, distributed training, accelerator
  design) via prompt modification / steering vectors / PEFT — reportedly only
  ~0.03% of traffic — **Anthropic apologized and walked the invisible
  guardrails back**, committing to **visible refusals or explicit model
  rerouting** instead of silent steering.
  **2026-06-13/14 — GLOBALLY DISABLED by US export-control order.** Anthropic
  abruptly **suspended Fable 5 (and Mythos 5) for ALL customers worldwide** to
  comply with a US government export-control directive barring access by any
  foreign national — the regulatory action itself is tracked on
  [[anthropic-fable-mythos-export-control-2026-06]]. New sessions fall back to
  **Opus 4.8** ([[opus-4-8]]); Fable 5 Platform/API calls now error
  ("It may not exist or you may not have access to it"). Anthropic calls it a
  "misunderstanding," disputes the jailbreak's severity (arguing GPT-5.5 shares
  the vulnerability), and says it is working to restore access. Both models
  remained dark into a second day; a Polymarket on restoration priced ~65% "back
  by July 1." Per this ticket's transition triggers, a pause of general
  availability keeps status `released` and is documented via history.
  **2026-06-16 — benchmark crown, still suspended (day 4).** Despite the
  worldwide suspension, capability rankings caught up to the launch: Fable 5
  **set a record on the Epoch Capabilities Index, dethroning GPT-5.5 Pro**, and
  tops the latest Artificial Analysis ladder at **~64.9** (ahead of Opus 4.8 and
  GPT-5.5; Chinese models Qwen 3.7 Max / MiniMax M3 / Kimi K2.6 cluster ~55).
  The export-control suspension remains unresolved on day 4 (see
  [[anthropic-fable-mythos-export-control-2026-06]]).
  **2026-06-23 — subscription cliff passed, still dark.** The **2026-06-22
  free-access cliff arrived**: Fable 5 was removed from Pro/Max/Team/Enterprise
  plans (moot while the model is suspended). The model stays globally offline
  under the export-control order; Anthropic still says it aims to restore access
  "as quickly as possible." Per transition triggers, an availability/billing
  change keeps status `released` and is documented via history.
  **2026-06-26 — partial restoration surfaces in AWS Bedrock.** Fable 5
  reappeared in the **Amazon Bedrock model catalog** as `anthropic.claude-fable-5`,
  listed **Active and sold by Anthropic** (independently screenshotted by
  @chetaslua with a screen recording, @alphabatcher, @LuminaXspace, @plasmakick,
  @VincentLogic). **Claude Code v2.1.190 binary strings** now show "You've used
  your included Fable 5 usage for this week" — the old "purchased separately
  from your plan" model is **dropped in favor of bundled weekly allocation**
  (verified by Decrypt via npm extraction, per @synthwavedd ~4.6K likes). Both a
  **US-region and a global model ID** are present (@plasmakick). Access is
  gated: **US identity verification via Persona** (live 2026-07-08), a use-case
  submission, and an Anthropic account review — the US-only re-entry mechanism
  inferred on [[anthropic-fable-mythos-export-control-2026-06]] now has product
  footing. Political backdrop warmed: **Trump walked back calling Anthropic a
  national-security threat**, and cofounder **Tom Brown replaced Dario Amodei**
  as the White House point person (the admin is reportedly "happier with Brown").
  Skeptical read: a Bedrock listing is infra-provisioning, not full restoration —
  Anthropic's own status page still shows the 2026-06-13 suspension as active
  with no restoration date, the Persona July 8 date could slip, and US-only ID
  gating means most of the market still can't use it. But Bedrock listing +
  Claude Code bundled-usage strings + political thaw + Persona infra is more
  restoration signals than any prior day. Per transition triggers, a
  re-availability event keeps status `released` and is documented via history.
  **2026-07-01 — Sonnet 5 shipped, Fable 5 re-release still absent.** Anthropic
  launched **Claude Sonnet 5** ([[claude-sonnet-5]]) on 2026-06-30 as the new
  default mid-tier — widely read as the mass-market "consolation tier" for
  users shut out of gated Fable 5 — but **no Fable 5 general re-release
  accompanied it**. The US ID-verification (Persona) gate remains dated
  2026-07-08; no fresh restoration progress this cycle. Still globally
  suspended for general use under the export-control order
  ([[anthropic-fable-mythos-export-control-2026-06]]).
  **2026-07-02 — BACK ONLINE GLOBALLY (metered).** Commerce **lifted the
  export-control order** (June 30 23:52 UTC @AnthropicAI + Politico; regulatory
  event on [[anthropic-fable-mythos-export-control-2026-06]]) and Anthropic
  **restored Fable 5 worldwide on July 1 as a general re-release** — not the
  US-only regime datamined strings had implied. Access is **metered: ≤50% of
  each plan's weekly usage limits through July 7, then usage credits**;
  @ClaudeDevs **reset all users' 5-hour and weekly rate limits** as it came back
  (~12K likes). A **small fraction of routine coding still falls back to Opus
  4.8**, and **tightened cyber + bio/chem safety classifiers** ship with the
  redeploy. Reception: strong praise for the model itself alongside friction
  with the terms — heavy users report **exhausting the 50% cap almost
  immediately** and call the bio/chem classifiers **over-restrictive** on
  legitimate science (single-amplifier enthusiast sentiment, @kimmonismus, not
  usage data). Capability datum: Fable 5 **tops the Scale AI + CAIS Remote Labor
  Index at 16.10%** (240 real paid freelance projects), ahead of Opus 4.8 and
  Codex GPT-5.5 — best automation up from <3% to 16% in under a year, though the
  leader still fails ~84% of real freelance work (@ScaleAILabs July 1). Status
  stays `released`; verification stays `confirmed`.
  **2026-07-03 — guardrail cost quantified; subscription-return commitment
  reaffirmed.** Independent benchmark firm **BridgeMind** re-ran the July 1
  relaunch build on **BridgeBench** and found the new cyber/bio/chem
  classifiers over-triggering the Opus 4.8 fallback so aggressively that
  debugging collapsed **86.2 → 25.9**, refactoring **73.6 → 38.4**, and
  hallucination rate worsened **75.9 → 61.7** — the first hard numbers behind
  the "Fable 5 feels nerfed" complaints tracked since relaunch. Single
  benchmark org, no independent replication yet, but directionally consistent
  with Anthropic's own relaunch disclosure. Separately, **Epoch AI** reports
  June 2026 saw ~1,500 high/critical CVE disclosures — 3.5x the prior monthly
  record, set before Mythos Preview shipped — read by some (@kimmonismus) as
  retroactive justification for the tightened classifiers, though Epoch's own
  framing hedges on causation. On the access side, an Anthropic team member
  (**@trq212**) reaffirmed late 2026-07-02 that Fable 5 **will return to
  Pro/Max/Team subscriptions "as soon as capacity allows,"** addressing an
  analyst concern that the July 1 blog's "temporary" framing had gone quiet —
  not yet matched by an official @AnthropicAI/@claudeai statement. Status
  stays `released`; verification stays `confirmed`.
  **2026-07-04 — jailbreak severity framework "first draft" published.**
  Anthropic posted a new blog page ("More details on Fable 5's cyber
  safeguards and our jailbreak framework") describing a **first-draft 0-4
  severity scale** for grading AI jailbreaks, developed with **Amazon,
  Microsoft, and Google** — a "CVSS for jailbreaks" (per @Ruben_Luetke)
  expanding on the vaguer "consensus framework" language from the July 1
  restoration post. Independently fetched the Anthropic blog URL this cycle
  to confirm it exists and matches the described content; Anthropic's own
  page labels it a "first draft," and no Amazon/Microsoft/Google statement
  confirms adopting the specific 0-4 delineations rather than just the
  general collaborative effort already announced July 1. Status stays
  `released`; verification stays `confirmed`.
expected: "BACK ONLINE GLOBALLY (2026-07-02): export controls lifted, Fable 5 restored worldwide as a general re-release, metered (≤50% of weekly usage limits through July 7, then usage credits; @ClaudeDevs reset all rate limits on relaunch); tightened cyber + bio/chem classifiers, small fraction of routine coding still routed to Opus 4.8; tops Scale AI + CAIS Remote Labor Index at 16.10% (ahead of Opus 4.8 / Codex GPT-5.5). Next watch: July 7 shift from the 50%-of-weekly cap to usage credits (day-one cap-exhaustion complaints), and whether Anthropic loosens the bio/chem classifier false positives as promised. Prior — partial restoration surfacing: Fable 5 listed Active in AWS Bedrock (anthropic.claude-fable-5) with bundled weekly Claude Code usage; US ID verification via Persona live 2026-07-08 + use-case review + Anthropic approval; both US and global model IDs present. Anthropic status page still shows the 2026-06-13 suspension as active (see [[anthropic-fable-mythos-export-control-2026-06]]). Was free for Pro/Max/Team through 2026-06-22, credit-metered thereafter"
labels:
  - frontier-model
  - released
  - mythos-class
  - safety-gated
  - coding
  - vision
verification: confirmed
sources:
  - "@claudeai"
  - "@AnthropicAI"
  - "@venturetwins"
  - "@chimpansky"
  - "@scaling01"
  - "@simonw"
  - "@ClaudeDevs"
  - "@DavidSacks"
  - "@AndrewCurran_"
  - "@chetaslua"
  - "@alphabatcher"
  - "@LuminaXspace"
  - "@synthwavedd"
  - "@plasmakick"
  - "@ScaleAILabs"
  - "@bridgemindai"
  - "@Hesamation"
  - "@EpochAIResearch"
  - "@trq212"
created_at: 2026-06-10
updated_at: 2026-07-04
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-10
    change: "Created — Anthropic publicly released **Claude Fable 5** on 2026-06-09 (@claudeai 17:08 UTC, ~90K likes / 12.8K RT): a Mythos-class model 'made safe for general use,' Anthropic's strongest generally-available model. Two-tier launch alongside the restricted **Mythos 5** (vetted defenders/govts, tracked on [[mythos-public-release]]). Fable 5 falls back to **Opus 4.8** on high-risk prompts (cyber/bio/chem/distillation), reportedly <5% of sessions. Pricing $10/$50 per MTok (≈½ the Mythos Preview's $25/$125); free for Pro/Max/Team until 2026-06-22, then credit-metered; new 30-day retention policy. Benchmarks: SOTA on Artificial Analysis (~65), SWE-bench Pro 80.3, Hex first-ever 90% on its analytics benchmark; Stripe used it to migrate a 50M-line Ruby codebase in ~a day. Spun out from [[mythos-public-release]] per that ticket's dedup note (a toned-down public variant with its own release plan = separate ticket). Status released, verification confirmed (official @claudeai/@AnthropicAI primary)"
  - ts: 2026-06-12
    change: "Update — guardrails reversal. After disclosing that Fable 5 would *silently* nerf AI/ML development tasks (pretraining, distributed training, accelerator design) via prompt modification / steering vectors / PEFT — reportedly affecting only ~0.03% of traffic — Anthropic apologized and walked the invisible guardrails back, committing to visible refusals or explicit model rerouting instead of silent steering (r/MachineLearning + press, 2026-06-11/12). Separately, Simon Willison documented Fable 5 as 'relentlessly proactive' (autonomously opening test pages in Safari, writing custom JS, spinning up a Python CORS server), underscoring the unboxed-agent security concern. Per this ticket's transition triggers, a material change to safety-fallback behaviour keeps status released and is documented via history; verification stays confirmed"
  - ts: 2026-06-14
    change: "Major update — GLOBALLY DISABLED by US export control (2026-06-13). Anthropic abruptly suspended Fable 5 AND Mythos 5 for ALL customers worldwide to comply with a US government export-control directive barring access by any foreign national (inc. its own foreign-national staff). New sessions fall back to Opus 4.8; Fable 5 API/Platform calls now error. The regulatory action itself is spun out to its own legal-event ticket [[anthropic-fable-mythos-export-control-2026-06]]; this entry records the product impact. Anthropic calls it a 'misunderstanding,' disputes the jailbreak's severity (argues GPT-5.5 shares it), and says it is working to restore access; White House AI czar @DavidSacks says the Admin asked Anthropic to fix or de-deploy and Anthropic refused. Both models still dark into day 2; Polymarket priced ~65% restoration by July 1. Per transition triggers, a pause of general availability keeps status released and is documented via history; verification stays confirmed (Anthropic's own statement + @ClaudeDevs notice + Reuters/Techmeme + Sacks on-record)"
  - ts: 2026-06-16
    change: "Benchmark crown while still dark (day 4). Fable 5 set a record on the Epoch Capabilities Index, dethroning GPT-5.5 Pro, and tops the latest Artificial Analysis ladder at ~64.9 (ahead of Opus 4.8 and GPT-5.5; Chinese open models Qwen 3.7 Max / MiniMax M3 / Kimi K2.6 cluster ~55) — capability rankings catching up to the launch even though the model remains globally suspended. Export-control suspension unresolved on day 4 ([[anthropic-fable-mythos-export-control-2026-06]]). Status stays released; verification stays confirmed (benchmark figures are secondary/social)."
  - ts: 2026-06-23
    change: "Subscription cliff passed, model still dark. The 2026-06-22 free-access cliff arrived — Fable 5 removed from Pro/Max/Team/Enterprise plans (moot while suspended). The model remains globally offline under the export-control order ([[anthropic-fable-mythos-export-control-2026-06]]); Anthropic still says it aims to restore access 'as quickly as possible.' Per transition triggers, an availability/billing change keeps status released and is documented via history; verification stays confirmed."
  - ts: 2026-06-26
    change: "Partial restoration surfaces in AWS Bedrock. Fable 5 reappeared in the Bedrock catalog as anthropic.claude-fable-5, listed Active and sold by Anthropic (multi-source screenshots: @chetaslua screen recording, @alphabatcher, @LuminaXspace, @plasmakick, @VincentLogic). Claude Code v2.1.190 binaries now show 'You've used your included Fable 5 usage for this week' — the 'purchased separately' add-on model is dropped for bundled weekly allocation (Decrypt-verified npm extraction, @synthwavedd ~4.6K likes). Both US and global model IDs present. Access gated: US ID verification via Persona (live 2026-07-08) + use-case submission + Anthropic review — the US-only re-entry mechanism inferred on [[anthropic-fable-mythos-export-control-2026-06]] now has product footing. Political thaw: Trump walked back the national-security-threat framing; Tom Brown replaced Dario as White House point person (admin reportedly 'happier with Brown'). Caveat: Anthropic's status page still shows the 06-13 suspension active with no restoration date; a Bedrock listing is infra-provisioning, not full restoration. Per transition triggers, a re-availability event keeps status released and is documented via history; verification stays confirmed."
  - ts: 2026-07-01
    change: "Sonnet 5 shipped, Fable 5 re-release still absent. Anthropic launched Claude Sonnet 5 ([[claude-sonnet-5]]) on 2026-06-30 as the new default mid-tier — widely framed as the mass-market consolation tier for users locked out of gated Fable 5 — but no Fable 5 general re-release accompanied it. The US ID-verification (Persona) gate stays dated 2026-07-08; no fresh restoration progress this cycle. Model remains globally suspended for general use under the export-control order ([[anthropic-fable-mythos-export-control-2026-06]]). Per transition triggers, this availability observation keeps status released and is documented via history; verification stays confirmed."
  - ts: 2026-07-02
    change: "BACK ONLINE GLOBALLY (metered). Commerce lifted the export-control order (June 30 23:52 UTC @AnthropicAI + Politico; regulatory event on [[anthropic-fable-mythos-export-control-2026-06]]) and Anthropic restored Fable 5 worldwide on July 1 as a general re-release — not the US-only regime datamined strings implied. Access is metered: ≤50% of each plan's weekly usage limits through July 7, then continuation via usage credits; @ClaudeDevs reset all users' 5-hour and weekly rate limits on relaunch (~12K likes). A small fraction of routine coding still falls back to Opus 4.8, and tightened cyber + bio/chem safety classifiers ship with the redeploy. Reception: strong praise for the model itself ('I forgive you for the bad Sonnet 5 launch') alongside term-friction — heavy users report exhausting the 50% cap almost immediately and call the bio/chem classifiers over-restrictive on legitimate science (single-amplifier enthusiast sentiment @kimmonismus, not usage data). Capability datum: Fable 5 tops the Scale AI + CAIS Remote Labor Index at 16.10% (240 real paid freelance projects), ahead of Opus 4.8 and Codex GPT-5.5 — best automation up from <3% to 16% in under a year, though the leader still fails ~84% of real freelance work (@ScaleAILabs July 1 17:33 UTC). Per transition triggers, a re-availability event keeps status released and is documented via history; verification stays confirmed."
  - ts: 2026-07-03
    change: "Guardrail cost quantified + subscription-return reaffirmed. BridgeMind's BridgeBench re-test of the July 1 build found the new classifiers over-triggering the Opus 4.8 fallback hard enough to crater debugging 86.2→25.9, refactoring 73.6→38.4, and worsen hallucination 75.9→61.7 (single-benchmark-org, no independent replication, but directionally consistent with Anthropic's own relaunch disclosure and widespread anecdotal complaints). Epoch AI reports June 2026 CVE disclosures hit ~1,500 (3.5x prior record, set before Mythos Preview shipped) — read by some as retroactive justification for the classifiers, though Epoch hedges on causation. Anthropic team member @trq212 reaffirmed Fable 5 will return to Pro/Max/Team subscriptions 'as soon as capacity allows,' addressing a dropped-commitment concern; not yet matched by an official @AnthropicAI/@claudeai statement. Status stays released; verification stays confirmed."
  - ts: 2026-07-04
    change: "Anthropic published a 'first draft' jailbreak severity framework blog post — a 0-4 severity scale developed with Amazon, Microsoft, and Google, expanding on the July 1 restoration post's vaguer 'consensus framework' language ('a CVSS for jailbreaks' per @Ruben_Luetke). Independently fetched the Anthropic blog URL to confirm; the page itself labels it a first draft, and no Amazon/Microsoft/Google statement confirms adopting these specific delineations. Status stays released; verification stays confirmed."
---

**Claude Fable 5** is the public-facing resolution of the long-running
question tracked on [[mythos-public-release]]: whether Anthropic would
ever bring its post-Opus, Mythos-class frontier intelligence out of the
gated Project Glasswing preview and into general availability. On
**2026-06-09** it did — but as a **two-tier launch**, not a single
public release.

**The two products, one set of weights.**
- **Fable 5 (public):** Mythos-class capability with hard safety
  classifiers. When a prompt touches cybersecurity, biology, chemistry,
  or model distillation, the classifier blocks or downgrades the request
  and hands it to **Opus 4.8** ([[opus-4-8]]) — no refusal banner, just a
  quieter answer. Anthropic reports the fallback triggers in **fewer than
  5% of sessions**.
- **Mythos 5 (restricted):** the unrestricted twin, available only to
  approved organizations (critical-infrastructure defenders, select
  life-sciences partners, government) via Project Glasswing and an
  upcoming trusted-access program. It is **not** publicly available and
  continues to be tracked on [[mythos-public-release]].

**Why this is its own ticket.** Per the dedup note on
[[mythos-public-release]], a toned-down Anthropic variant with a
*different release plan* gets its own ticket. Fable 5 is exactly that:
the Cherny-floated "toned-down version in the foreseeable future" became
a real, publicly-shipping product, while Mythos proper stays gated. This
ticket carries the public-release lifecycle; the Mythos ticket carries
the gated line.

**Commercial shape.** Pricing is **$10 per MTok input / $50 per MTok
output** — less than half the $25/$125 reported for the earlier Mythos
Preview. It is **free for Pro, Max, and Team subscribers until
2026-06-22**, after which continued use requires purchased credits.
Early users widely flag it as **token-hungry and expensive** ("burst
compute" — best reserved for hard planning, refactors, and final review,
then routing down to cheaper models). Anthropic also shipped a new
**30-day data-retention** policy across Fable/Mythos traffic concurrent
with launch.

**Capability signal.** Independent and Anthropic-cited benchmarks put
Fable 5 at the frontier: ~65 on Artificial Analysis (chart-topping),
**80.3 on SWE-bench Pro**, Hex's first-ever 90% on its long-running
analytics benchmark, and strong vision results (rebuilding web apps from
screenshots; beating Pokémon FireRed from raw frames). The marquee
real-world demo: **Stripe migrated a ~50-million-line Ruby codebase in
about a day**, work normally measured in months.

**Transition triggers:**
- Successor public model (e.g. a Fable 5.x or next-class public release)
  → create a new ticket; do not reopen this one.
- ≥4 weeks past 2026-06-09 release with no successor → close with
  `released-and-aged`.
- Anthropic pulls or pauses general availability, or materially changes
  the safety-fallback behaviour → keep `released`, document via history.
- Mythos 5 itself flips to public availability → that is a state change on
  [[mythos-public-release]], not here.

**Dedup note:** Fable 5 pricing, availability, benchmark, and safety-
classifier signal UPDATES this ticket. Mythos 5 (restricted) /
Glasswing / gated-preview signal stays on [[mythos-public-release]].
