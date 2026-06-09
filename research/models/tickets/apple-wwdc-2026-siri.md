---
slug: apple-wwdc-2026-siri
title: Apple WWDC 2026 — distilled Gemini on-device + full Gemini on Google Cloud via NVIDIA confidential-compute
company: Apple
model: null
status: confirmed
status_note: |
  **CONFIRMED at WWDC 2026 (keynote 2026-06-08, Tim Cook's final keynote as
  CEO).** Apple unveiled a ground-up **"Siri AI"**: a standalone, conversational
  assistant with on-device personal context, real-time screen awareness,
  multi-step cross-app actions, and a Dynamic Island "Search or Ask" entry.
  Confirmed architecture is **three-tier routing** — Tier 1 on-device Apple
  models, Tier 2 Apple Private Cloud Compute, **Tier 3 a custom ~1.2T-parameter
  Google Gemini on Nvidia Blackwell B200s via Google Cloud** for heavy
  reasoning, queries anonymized/tokenized at each hop. iOS/iPadOS/macOS 27
  developer betas dropped immediately; **iOS 27 Extensions** make Claude,
  ChatGPT, Gemini, and Grok user-selectable default assistants (Claude a
  built-in iPhone option for the first time). The Gemini backend was confirmed
  on stage; the "$1B/yr to Google" license and the "1.2T parameters" figure
  were NOT stated on stage (Gurman pre-reporting) — those specific numbers
  remain leak-only. **Siri AI reportedly geofenced out of the EU (DMA impasse)
  and China at launch.** Cook becomes executive chairman 2026-09-01; John
  Ternus succeeds as CEO. Prior (pre-keynote) reporting retained below for the
  record:

  The Information's WWDC preview (paywalled, relayed by @kimmonismus
  2026-05-31 12:12 UTC) reports Apple's long-delayed on-device Siri
  will run a **distilled version of Google's Gemini** locally on iPhone
  silicon, with anything too heavy for the device routed to **Google
  Cloud rather than Apple's own Private Cloud Compute** — a material
  retreat from the 2024 promise that nothing would leave Apple silicon.
  Apple has reportedly **signed off on NVIDIA's confidential-compute
  stack** to process those cloud queries. The **Private Cloud Compute
  brand is staying** even though queries leave Apple silicon. Apple is
  also reportedly hunting on-device-AI startups (Liquid AI named) to
  accelerate model-shrinking work. WWDC 2026 keynote confirmed for
  2026-06-08 per Apple's WWDC subdomain registration. @theinformation
  ran its own enterprise framing of the on-device pivot 2026-05-31
  16:00 + 20:00 UTC. **Talent vector**: Mark Gurman scooped 2026-05-31
  23:59 UTC that **Kelsey Peterson** — the Apple AI engineer who
  introduced the never-launched 2024 Siri revamp on stage at WWDC —
  just started at OpenAI, eight days before WWDC 2026.
expected: "iOS/iPadOS/macOS 27 developer betas live (2026-06-08); consumer Siri AI GA expected with the autumn 2026 public releases; blocked in EU + China at launch. homeOS/HomePad autumn 2026; AI Glasses late 2027, Vision Air 2029 per Gurman"
labels:
  - rumored
  - apple
  - wwdc
  - apple-gemini-partnership
  - on-device
  - private-cloud-compute
  - nvidia-confidential-compute
verification: confirmed
sources:
  - "@kimmonismus"
  - "@theinformation"
  - "@markgurman"
  - "@9to5mac"
  - "@t0nAr1sm"
  - https://www.theverge.com/tech/944245/apple-wwdc-2026-ai-siri-gemini
  - https://techcrunch.com/2026/06/06/what-to-expect-from-wwdc-2026-siris-highly-anticipated-revamp-and-apple-intelligence-updates/
  - https://www.apple.com/newsroom/
created_at: 2026-06-01
updated_at: 2026-06-09
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-01
    change: "Created — The Information's WWDC preview (paywalled, relayed by @kimmonismus 2026-05-31 12:12 UTC, ~76 likes): Apple's on-device Siri runs distilled Gemini locally; heavier queries route to Google Cloud via NVIDIA confidential-compute, not Apple's Private Cloud Compute (PCC brand stays). Apple reportedly scouting Liquid AI for distillation help. @theinformation's own enterprise framing of the on-device pivot 16:00 + 20:00 UTC the same day corroborates. Kelsey Peterson defection to OpenAI 2026-05-31 23:59 UTC (Gurman scoop, ~656 likes) sets the talent vector. WWDC 2026 keynote confirmed 2026-06-08; Apple AI Glasses pushed to late 2027, Vision Air to 2029 (Gurman via @9to5mac, @t0nAr1sm)"
  - ts: 2026-06-07
    change: "Pre-keynote corroboration in primary tech press: The Verge 'Here comes new Siri again' (2026-06-06) and TechCrunch's WWDC-2026 preview (2026-06-06) both frame Apple as set to reintroduce a Gemini-assisted Siri with Apple Intelligence updates, consistent with the distilled-Gemini reporting. Keynote is **tomorrow (2026-06-08)** — the on-stage architecture will confirm or contradict the routing/PCC detail. Status stays rumored / partial pending the keynote"
  - ts: 2026-06-08
    change: "Keynote day (WWDC 2026, 1pm PT today). Pre-keynote preview relay (Gurman PowerOn newsletter, via @dlimeng192048 08:01 UTC) restates the architecture and adds detail: Apple to launch a **standalone AI-assistant app** capable of competing with ChatGPT (chatbot-style interaction + generative AI image editing), with Siri's underlying technical stack reportedly **replaced by Google's Gemini model on Google Cloud infrastructure**; iOS 27 / macOS 27 / watchOS 27 / visionOS 27 unveiled simultaneously; framed as Apple's largest-ever Siri/AI update and **Tim Cook's last major product unveiling before retirement**. Org backdrop: the internal AI team once nicknamed 'AIMLess', a 2025 crisis meeting after Apple Intelligence 1.0 failed, Mike Rockwell now over Siri, Craig Federighi over AI strategy, Amar Subramanya leading model research, John Giannandrea departed this year. Still **pre-stage** — no on-record Apple confirmation yet; status stays rumored / partial pending the actual keynote later today, which will confirm (→ confirmed/released) or contradict (→ closed:disproved + successor) the Gemini routing detail"
  - ts: 2026-06-09
    change: "KEYNOTE OUTCOME — rumored → confirmed, partial → confirmed. WWDC 2026 (2026-06-08, Tim Cook's final keynote as CEO) shipped **Siri AI**: a standalone conversational assistant (on-device personal context, real-time screen awareness, multi-step cross-app actions, Dynamic Island 'Search or Ask'). Apple **confirmed the Gemini backend on stage** via a **three-tier routing** stack — Tier 1 on-device Apple models, Tier 2 Private Cloud Compute, **Tier 3 a custom ~1.2T-param Gemini on Nvidia Blackwell B200s on Google Cloud** — vindicating the distilled-Gemini + cloud-routing reporting (though the 'cloud' tier is Google Cloud + Nvidia, with PCC retained as Tier 2). iOS/iPadOS/macOS 27 dev betas dropped immediately; **iOS 27 Extensions** make Claude/ChatGPT/Gemini/Grok user-selectable default assistants (first time Claude is a built-in iPhone option). Also: homeOS + HomePad (7-inch hub, A18, autumn 2026), Photos Extend/Enhance/Reframe, a free on-device Foundation Models API for devs, 'Liquid Glass' UI. **Siri AI reportedly geofenced out of the EU (DMA) and China at launch.** The '$1B/yr to Google' and '1.2T params' figures were NOT stated on stage (Gurman pre-reporting) → remain leak-only. Cook → executive chairman 2026-09-01, John Ternus succeeds as CEO. Reception 'underwhelmed' ('bought time, not independence'). Status confirmed; consumer GA expected with the autumn public releases (→ released then)"
---

**Apple's WWDC 2026 Siri rebuild** has now been previewed across two
independent reporting paths in the 2026-05-31 window, with the
keynote itself scheduled for **2026-06-08**. The headline architecture
shift, per The Information's paywalled WWDC preview (relayed by
@kimmonismus 12:12 UTC, with @theinformation's own enterprise
framing landing at 16:00 + 20:00 UTC the same day):

- **On-device Siri runs a distilled version of Google Gemini** on
  iPhone silicon, pitched on privacy and lower token cost.
- **Heavy queries route to Google Cloud** — not Apple's own Private
  Cloud Compute (PCC). Apple has reportedly signed off on **NVIDIA's
  confidential-compute stack** to process those cloud queries.
- The **Private Cloud Compute brand stays** in marketing, even though
  the underlying trust boundary has materially changed — the 2024
  promise that anything leaving the iPhone would run on Apple silicon
  is no longer the operating posture.
- Apple is reportedly **scouting on-device-AI shops** (Liquid AI
  named) to accelerate the model-shrinking work that the distilled
  Gemini stack needs.

**Talent vector — Kelsey Peterson to OpenAI** (Bloomberg's Mark
Gurman, 2026-05-31 23:59 UTC, ~656 likes / 27 RT, photo of Peterson
on stage attached): Peterson is the Apple AI engineer who
**introduced the never-launched 2024 Siri revamp on stage at WWDC**.
She just started at OpenAI — eight days before WWDC 2026. The defection
is single-source on the move itself (Gurman is Bloomberg's primary
Apple reporter), but the timing and vector — to OpenAI specifically,
the lab whose competing model (GPT-5.5 / GPT-Rosalind / Codex) is
*not* the partner Apple's reported architecture sits behind — is the
story.

**Adjacent hardware roadmap signal** (Gurman via @9to5mac 2026-05-31
15:13 UTC; @t0nAr1sm Japanese relay 2026-06-01 01:16 UTC): **Apple AI
Glasses pushed to late 2027**, **Vision Air to 2029**; the first
glasses revision is reportedly **AR-display-free** with camera,
microphone, Siri, and Visual Intelligence as the centerpieces.

**Why this is `rumored` + `partial`:** the WWDC preview is single-
sourced to The Information (paywalled), with @theinformation's own
follow-on posts elevating it from a kimmonismus relay to enterprise
reporting in the same day; no Apple, Google, or NVIDIA primary handle
has confirmed in-window. The Peterson defection is single-source
(Gurman), credible but not multi-source. Per the schema, that maps to
`rumored` + `verification: partial`. The keynote itself in 8 days
will either confirm or contradict the architecture detail on stage.

**Why this is its own ticket:** Apple's Siri rebuild is a material
**multi-lab partnership event** (Apple + Google + NVIDIA) with a fixed
verification date (WWDC 2026-06-08). It is structurally distinct from
both the Gemini 3.5 Flash model ticket ([[gemini-3-2-flash]]) and the
Gemini Spark consumer-agent ticket ([[gemini-spark]]) — those are
Google products with Google distribution; this is Apple consuming
Gemini via a confidential-compute-mediated cloud relationship. If
Apple announces the on-device + cloud-routing arrangement on stage,
the ticket advances to `confirmed` (or `released` if Siri ships at GA
on June 8); if Apple announces a different stack, the ticket closes
with `disproved` and a successor ticket captures whatever Apple did
ship.

**Transition triggers:**

- WWDC keynote (2026-06-08) confirms the distilled-Gemini + Google
  Cloud routing architecture on stage → `status: confirmed` (or
  `released` if Siri ships GA the same day).
- Keynote ships a materially different architecture (e.g.
  Apple-silicon-only with no Gemini, or a different cloud partner) →
  `closed: disproved`, create successor ticket.
- Liquid AI acquisition / partnership confirmed → UPDATE.
- Independent privacy-research analysis of the PCC scope change (EFF,
  Mozilla, named privacy researcher) → UPDATE.
- Additional Apple-AI defections to frontier labs (Gurman has reported
  prior cycles' moves to OpenAI / Meta) → UPDATE the talent vector
  in history.
- ≥15 daily cycles at `rumored` / `partial` with no fresh
  corroboration AND keynote passes without confirmation → close with
  `stale-rumor-unverified`.

**Dedup note:** further Apple WWDC 2026 / Siri / on-device-Gemini /
Private Cloud Compute / NVIDIA confidential-compute / Apple-OpenAI
talent-flow signal UPDATES this ticket. Apple-Google search / payments
deal coverage stays on the relevant ticket if/when it exists. Apple
Vision Air and AI Glasses release dates get appended in history here
until they spin out as their own tickets at concrete launches.
