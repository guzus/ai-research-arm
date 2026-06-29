---
slug: openai-gpt-5-6
title: OpenAI GPT-5.6 (Sol / Terra / Luna) — government-gated frontier preview
company: OpenAI
model: GPT-5.6
status: confirmed
status_note: |
  GPT-5.6 is the most-watched unreleased OpenAI model, expected **alongside the
  ChatGPT "super app" overhaul** ([[openai-chatgpt-superapp-2026-06]]). Signal is
  anticipation, not artifact: Andrew Curran flagged a "next week" window;
  **prediction markets price a by-2026-06-30 release at ~89%**; and multiple
  developers independently hit **"Model not found: gpt-5.5" 404s inside Codex** —
  a *weak* backend tell equally consistent with a routing hiccup, and about 5.5
  rather than 5.6. **No OpenAI on-record date, no public artifact, no benchmarks.**
  A newer **low-credibility, single secondary/social** rumor (2026-06-15) pins
  a **2026-06-23** release with ~1.5M-token context, stronger agentic coding,
  and pricing ~3x cheaper than Fable 5 — timed to the date many Fable 5 users
  are pushed to a premium plan. Consistent with the by-2026-06-30 window;
  unconfirmed, no primary.

  **2026-06-20:** Rumor still live inside the window. @iruletheworldmo floated a
  fresh **"next week"** launch claim (2026-06-19), and a separate post
  (@rishflips, 2026-06-20) claims OpenAI is **stealth-testing a model** —
  speculated GPT-5.6 — via a "Deployment Simulation" method, citing only
  "users say ChatGPT suddenly feels smarter." Both are zero-artifact influencer
  teases (the amplifier itself notes "no official GPT-5.6 in OpenAI release
  notes"). No OpenAI on-record date, public artifact, or benchmarks. Status
  stays `rumored`, verification stays `partial`.

  **2026-06-21:** Timing firmed toward late June but stayed unconfirmed.
  Chief Scientist **Jakub Pachocki** reportedly told staff GPT-5.6 is a
  "**meaningful improvement**" over 5.5 (attributed to **The Information**) —
  the most senior-attributed signal yet, though still a relayed internal remark,
  not a public artifact. Leak-trackers peg a launch "as soon as next week," and
  **Polymarket moved to ~83% on a 2026-06-22→28 drop**. Notably, the viral
  "**stealth GPT-5.6-Pro**" capability demos were **debunked as model-tier
  confusion** — testers were on GPT-5.5-Pro, not 5.6 (@MarMarLabs). Leaked specs
  (~1.5M context, faster Codex, cheaper pricing) remain rumor; still no system
  card or API listing. Status stays `rumored`, verification stays `partial`.

  **2026-06-22:** Window arrived; chatter persisted, artifact did not. Leak
  relays now cite a specific **"Thursday" / June 25** date and a Japanese
  aggregator (@redcord_okumura) lists **"GPT-5.6 being tested in Codex,"**
  dovetailing with OpenAI's @thsottiaux teasing a **big front-end capability
  jump** (~7–8K likes). All still leak/anon-grade — no OpenAI system card, API
  listing, or confirmed date this window. Status stays `rumored`, verification
  stays `partial`.

  **2026-06-23:** Window firmed to a **"Thursday (~June 25)"** leak date and
  picked up a **surprise bidirectional voice model, "GPT-Bidi-1,"** in the same
  leak bundle. Betting markets now price a **June 22–28 launch near 90–100%**.
  Still **no system card, API listing, or OpenAI-confirmed date**, and the
  loudest "leaked" posts remain SEO spam. GPT-Bidi-1 is a zero-artifact,
  single-bundle leak folded here as part of the same anticipated launch event.
  Status stays `rumored`, verification stays `partial`.

  **2026-06-25:** A real artifact appeared. Two independent leakers (@scaling01
  ~742 likes, @haider1 ~141 likes) spotted a **`gpt-5.6-preview` route in
  OpenAI's internal admin model-access panel** (`admin/model-access/gpt-5.6-
  preview`), visible in routing and frontend files. The "Preview" suffix
  historically preceded OpenAI's biggest capability leaps (o1-preview,
  o3-preview, GPT-4.5-Preview) and signals readiness for external testing — a
  materially different stage from "in training." @scaling01 himself cautioned it
  may be "just for testing and not for release," and there is zero first-party
  OpenAI acknowledgement, but a console route is the kind of artifact this
  ticket's transition trigger says moves the lifecycle toward `in-testing`.

  **2026-06-26:** The regulatory picture crystallized around the preview. **The
  Information** broke (and **Axios** confirmed) that the **Trump administration
  formally asked OpenAI to stagger GPT-5.6's release** — Sam Altman told staff
  the government will approve access **"customer by customer"** during a limited
  preview, with a broader release possibly "a couple of weeks" later; the
  request came through the Office of the National Cyber Director and OSTP under
  the voluntary June 2 frontier-model review EO ([[us-ai-model-review-eo-2026-06]]).
  **Axios** adds GPT-5.6 has **"Mythos-like" capability** — the same tier that
  triggered the Fable 5/Mythos 5 export suspension
  ([[anthropic-fable-mythos-export-control-2026-06]]) — and that **OpenAI had
  been pushing for its release since before the Fable ban**, implying the model
  was ready weeks ago and is held up by the review environment. No OpenAI
  official tweet/blog/denial. The admin-route leak plus the reported limited
  preview clear the `in-testing` bar (a real artifact + a gated external
  preview); still no OpenAI on-record date, system card, or API string, so
  verification stays `partial` (The Information + Axios are credible secondary,
  not OpenAI-primary). Status advances to `in-testing`.

  **2026-06-29:** **Confirmed — official preview shipped.** OpenAI published
  **"Previewing GPT-5.6 Sol"** (openai.com/index/previewing-gpt-5-6-sol/),
  launching the **GPT-5.6 family — Sol (flagship), Terra (balanced), Luna
  (fast/cheap)** — in a **limited, US-government-approved preview** (access
  restricted to a small group of trusted partners shared with the government
  before broader release; OpenAI: "this kind of government access process
  shouldn't become the long-term default"). **Sol sets a new SOTA on
  Terminal-Bench 2.1** and improves agentic coding, biology, and cybersecurity;
  new **"max" reasoning effort** and an **"ultra" mode** (spawns subagents).
  **Pricing per 1M tokens:** Sol **$5 in / $30 out**, Terra **$2.50 / $15**,
  Luna **$1 / $6**, with explicit cache breakpoints (30-min minimum cache life).
  **GA "in the coming weeks"**; Polymarket prices **~90% public release by
  2026-07-31**. With an official OpenAI blog + named tiers + pricing + benchmarks,
  corroborated by VentureBeat / Axios / Simon Willison / TechCrunch → status
  **in-testing → confirmed**, verification **partial → confirmed**. Not yet
  `released`: the preview is gated/limited, not publicly available to anyone.
expected: "GPT-5.6 family (Sol flagship / Terra balanced / Luna fast) shipped in a US-government-approved limited preview ~2026-06-26 (official OpenAI blog); Sol new SOTA on Terminal-Bench 2.1, max + ultra (subagent) modes; pricing Sol $5/$30, Terra $2.50/$15, Luna $1/$6, 30-min min cache. GA 'in the coming weeks' — Polymarket ~90% public release by 2026-07-31"
labels:
  - openai
  - frontier-model
  - gated-preview
verification: confirmed
sources:
  - "@AndrewCurran_"
  - "@Polymarket"
  - "@MarMarLabs"
  - "@scaling01"
  - "@haider1"
  - "@theinformation"
  - "@OpenAI"
  - https://openai.com/index/previewing-gpt-5-6-sol/
  - https://simonwillison.net/2026/Jun/26/openai/
created_at: 2026-06-09
updated_at: 2026-06-29
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-09
    change: "Created — GPT-5.6 anticipated alongside OpenAI's ChatGPT 'super app' overhaul ([[openai-chatgpt-superapp-2026-06]]). Andrew Curran flagged a 'next week' window; prediction markets price a by-2026-06-30 release ~89%; multiple devs hit 'gpt-5.5' 404s in Codex (weak tell, and about 5.5 not 5.6). No OpenAI on-record date, no artifact, no benchmarks → status rumored, verification partial (multiple secondary corroborations, no primary)"
  - ts: 2026-06-15
    change: "Rumor refresh — a low-credibility single-source social rumor now pins a 2026-06-23 GPT-5.6 release with ~1.5M-token context, stronger agentic coding, and ~3x-cheaper-than-Fable-5 pricing, timed to the date many Fable 5 users are pushed to premium. Consistent with the existing by-2026-06-30 window; still no OpenAI on-record date or public artifact. Status stays rumored; verification stays partial."
  - ts: 2026-06-16
    change: "Rumor at 'fever pitch' — the 2026-06-23 / ~1.5M-context / ~3x-cheaper claim recirculated heavily (the seed post ~276 RT / 1.7K likes) and accounts now add that GPT-5.6 'reportedly surfaced in internal Codex logs' with sources describing it as a 'meaningful improvement' over GPT-5.5. The Codex-logs mention is a weak backend tell (consistent with the earlier 'gpt-5.5' 404s), not a captured artifact. Still no OpenAI on-record date, public artifact, or benchmarks. Status stays rumored; verification stays partial."
  - ts: 2026-06-20
    change: "Rumor still live in-window. @iruletheworldmo floated a fresh 'next week' launch claim (2026-06-19); a separate post (@rishflips 2026-06-20) claims OpenAI is stealth-testing a model (speculated GPT-5.6) via a 'Deployment Simulation' method, citing only 'users say ChatGPT suddenly feels smarter.' Both are zero-artifact influencer teases (the amplifier flags 'no official GPT-5.6 in OpenAI release notes'). No OpenAI on-record date, artifact, or benchmarks. Status stays rumored; verification stays partial."
  - ts: 2026-06-21
    change: "Timing firmed, still unconfirmed. Chief Scientist Jakub Pachocki reportedly told staff GPT-5.6 is a 'meaningful improvement' over 5.5 (attributed to The Information) — most senior-attributed signal yet but still a relayed internal remark, not an artifact. Leak-trackers peg 'as soon as next week'; Polymarket moved to ~83% on a 2026-06-22→28 drop. The viral 'stealth GPT-5.6-Pro' capability demos were debunked as model-tier confusion — testers were on GPT-5.5-Pro, not 5.6 (@MarMarLabs). Leaked specs (~1.5M context, faster Codex, cheaper pricing) remain rumor; no system card or API listing. Status stays rumored; verification stays partial."
  - ts: 2026-06-22
    change: "Window arrived, chatter persisted, no artifact. Leak relays now cite a specific 'Thursday' / June 25 date; a Japanese aggregator (@redcord_okumura) lists 'GPT-5.6 being tested in Codex,' dovetailing with OpenAI's @thsottiaux teasing a big front-end capability jump (~7–8K likes). Still leak/anon-grade — no OpenAI system card, API listing, or confirmed date this window. Status stays rumored; verification stays partial."
  - ts: 2026-06-23
    change: "Window firmed to 'Thursday (~June 25)' and the leak bundle added a surprise bidirectional voice model, 'GPT-Bidi-1.' Betting markets now price a June 22–28 launch near 90–100%. Still no system card, API listing, or OpenAI-confirmed date; loudest 'leaked' posts remain SEO spam. GPT-Bidi-1 is a zero-artifact single-bundle leak, folded here as part of the same anticipated launch event rather than a separate ticket. Status stays rumored; verification stays partial."
  - ts: 2026-06-25
    change: "First real artifact — two independent leakers (@scaling01 ~742 likes, @haider1 ~141 likes) spotted a `gpt-5.6-preview` route in OpenAI's internal admin model-access panel (visible in routing/frontend files). The 'Preview' suffix historically precedes OpenAI's biggest capability leaps (o1/o3/GPT-4.5-Preview); @scaling01 cautioned it may be 'just for testing,' and there is no OpenAI acknowledgement, but a console route is the artifact class this ticket's transition trigger says moves the lifecycle toward in-testing. No system card, API listing, or OpenAI-confirmed date. Status stays rumored this entry; verification stays partial."
  - ts: 2026-06-26
    change: "Status → in-testing. The Information broke (Axios confirmed) that the Trump administration asked OpenAI to stagger GPT-5.6's release: Altman told staff the government will approve access 'customer by customer' during a limited preview, broader release possibly 'a couple of weeks' later, via ONCD/OSTP under the voluntary June 2 frontier-model review EO ([[us-ai-model-review-eo-2026-06]]). Axios adds GPT-5.6 has 'Mythos-like' capability (the Fable 5/Mythos 5 export-suspension tier, [[anthropic-fable-mythos-export-control-2026-06]]) and that OpenAI had pushed for release since before the Fable ban — implying the model was ready weeks ago and is held up by the review environment. The admin-route leak (06-25) + the reported gated limited preview clear the in-testing bar (real artifact + external preview). Still no OpenAI on-record date, system card, or API string → verification stays partial (credible secondary via The Information + Axios, not OpenAI-primary)."
  - ts: 2026-06-29
    change: "Status → confirmed; verification → confirmed. OpenAI published the official 'Previewing GPT-5.6 Sol' blog (openai.com/index/previewing-gpt-5-6-sol/), launching the GPT-5.6 family — Sol (flagship), Terra (balanced), Luna (fast/cheap) — in a limited, US-government-approved preview (access restricted to a small group of trusted partners shared with the government before broader release; OpenAI: 'this kind of government access process shouldn't become the long-term default'). Sol sets a new SOTA on Terminal-Bench 2.1, improves agentic coding/biology/cybersecurity; new 'max' reasoning effort + 'ultra' subagent-spawning mode. Pricing/1M tok: Sol $5/$30, Terra $2.50/$15, Luna $1/$6, explicit cache breakpoints (30-min min cache). GA 'in the coming weeks'; Polymarket ~90% public release by 2026-07-31. Official OpenAI primary + named tiers + pricing + benchmarks, corroborated by VentureBeat/Axios/Simon Willison/TechCrunch → status advances to confirmed, verification to confirmed. Not released yet: preview is gated/limited, not public to anyone. The leak-grade 'GPT-Bidi-1' bidirectional voice model from the prior bundle was NOT part of this preview; it stays a folded rumor pending its own artifact. Sources: @OpenAI, openai.com blog, Simon Willison."
---

**GPT-5.6** is OpenAI's most-anticipated unreleased frontier model, widely
expected to land **alongside the "super app" ChatGPT overhaul**
([[openai-chatgpt-superapp-2026-06]]). As of this cycle the signal is
**anticipation rather than a shipping artifact**.

**What there is:** Andrew Curran flagged a **"next week"** window;
**prediction markets price a by-2026-06-30 release at ~89%**; and several
developers independently reported **"Model not found: gpt-5.5" 404s inside
Codex**. The 404s are a *weak* rollout tell — equally consistent with a backend
hiccup, and they reference **gpt-5.5**, not 5.6.

**What there isn't:** no OpenAI on-record date, no public artifact, no
benchmarks, no pricing. That maps cleanly to `rumored`. `verification` is
`partial` (not `unverified`) only because the expectation is corroborated by
**multiple independent secondary signals** (a credible reporter + prediction
markets + multi-dev 404 reports), none of them primary.

**Transition triggers:**
- A console/API artifact, leaked spec, or private preview of GPT-5.6 → `in-testing`.
- An OpenAI on-record announcement → `confirmed`.
- Public rollout (API / ChatGPT) → `released`.
- ≥15 cycles with the window lapsed and no fresh corroboration → `closed: stale-rumor-unverified`.

**Dedup note:** GPT-5.6 model signal (artifacts, benchmarks, launch) UPDATES
this ticket. The ChatGPT product overhaul stays on
[[openai-chatgpt-superapp-2026-06]]; the Codex platform stays on its own ticket.
