---
slug: openai-gpt-5-6
title: OpenAI GPT-5.6 (Sol / Terra / Luna) — government-gated frontier preview
company: OpenAI
model: GPT-5.6
status: released
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

  **2026-07-03 — firsthand OpenAI-staffer reconfirmation, still gated.**
  @altryne relayed a firsthand conversation with OpenAI's own @dkundel at an
  AI conference booth, reconfirming the Sol/Terra/Luna tiers, Ultra mode, the
  Codex app, and a "token bank" concept. Separately, per-tier pricing
  ($5/$30, $2.50/$15, $1/$6 per MTok) already on this ticket recirculated via
  secondary relays (@amohan120) with no new figures. Still limited to ~20
  vetted organizations; no GA date. Status stays `confirmed`; verification
  stays `confirmed`.

  **2026-07-04 — tier names go primary-source via OpenAI's own GitHub repo;
  "Tuesday" firms the July 7 date.** A GPG-signed commit merged **2026-06-26**
  into OpenAI's public Codex repo (independently verified against GitHub's
  API this cycle) adds `openai.gpt-5.6-sol` / `-terra` / `-luna` to Codex's
  Amazon Bedrock model catalog — the first **primary-source** confirmation of
  the tier names, upgrading them from leaker-sourced to OpenAI-authored code.
  The commit is a catalog entry, not a launch announcement, and predates the
  "next week" rumor window by over a week — consistent with pre-launch prep,
  not proof of the ship date. Separately, a live Codex-app UI popup
  screenshot (@DevAdventur3s, 387 likes) shows the Sol/Terra/Luna tier
  selector visible in-product (not just code strings), and @kimmonismus
  replied with the first insider-adjacent nod to a specific weekday —
  "have to wait until tuesday" (July 7). The July 7-9 launch window itself
  remains single-leaker-sourced (no OpenAI on-record date). Status stays
  `confirmed`; verification stays `confirmed`.

  **2026-07-12 — status → released; GA confirmed.** OpenAI's own account
  posted "GPT-5.6 is a major step forward for health intelligence... GPT-5.6
  Luna outperforms GPT-5.5..." and separately confirmed "Yesterday, we made
  GPT-5.6 Sol Ultra generally available" (2026-07-10). Sam Altman added that
  GPT-5.6 is "now the preferred model in Microsoft 365 Copilot"
  (2026-07-10), and dozens of independent users report hitting rate limits
  on it — crossing from a gated ~20-org preview to broad general
  availability. Status advances `confirmed` → `released`; verification
  stays `confirmed` (official @OpenAI + @sama primary, multi-source
  corroboration).

  **2026-07-14 — post-GA quality regression + compensation.** Multiple
  independent accounts (@theo, @kimmonismus, testingcatalog, @jxnlco
  relaying @thsottiaux) report OpenAI quietly reduced GPT-5.6's
  reasoning-effort budget ("juice values") and discussed a context-window
  rollback (372k→272k) days after GA, then compensated with "banked
  resets" to ChatGPT Work/Codex usage limits for an estimated 500k–7M
  affected users. @theo's own thread partially walks back the precise
  mechanism ("point 1 is not correct, it just compounds after
  compactions"), so the exact technical detail stays contested even though
  multiple sources agree something regressed and OpenAI compensated users.
  No official OpenAI post addressing the regression itself. Status stays
  `released`; verification stays `confirmed` (the regression-and-
  compensation event is well-corroborated across independent accounts,
  even as its precise mechanics remain unsettled).
expected: "GA confirmed 2026-07-10: OpenAI's own account announced GPT-5.6 Sol Ultra generally available, and @sama says GPT-5.6 is now the preferred model in Microsoft 365 Copilot. Family is Sol (flagship) / Terra (balanced) / Luna (fast/cheap); Sol set SOTA on Terminal-Bench 2.1 with max + ultra (subagent) modes; pricing Sol $5/$30, Terra $2.50/$15, Luna $1/$6 per MTok"
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
  - "@sama"
  - https://openai.com/index/previewing-gpt-5-6-sol/
  - https://simonwillison.net/2026/Jun/26/openai/
created_at: 2026-06-09
updated_at: 2026-07-14
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
  - ts: 2026-07-03
    change: "Firsthand reconfirmation, no new state change. @altryne relayed a firsthand conversation with OpenAI's @dkundel at an AI conference reconfirming Sol/Terra/Luna, Ultra mode, the Codex app, and a 'token bank' concept; pricing figures already on this ticket recirculated via secondary relay (@amohan120) with no new numbers. Still ~20-org gated, no GA date. Status stays confirmed; verification stays confirmed."
  - ts: 2026-07-04
    change: "Tier names go primary-source. A GPG-signed commit merged 2026-06-26 into OpenAI's public Codex GitHub repo (independently verified via GitHub's API) adds openai.gpt-5.6-sol/-terra/-luna to the Bedrock model catalog — first primary-source confirmation of the tier names (a catalog entry, not a launch announcement; predates the rumor window by a week). A live Codex-app UI popup screenshot (@DevAdventur3s) shows the tier selector in-product; @kimmonismus adds the first insider-adjacent 'Tuesday' (July 7) nod. Launch date itself stays single-leaker-sourced. Status stays confirmed; verification stays confirmed."
  - ts: 2026-07-12
    change: "Status → released. @OpenAI's own account confirmed GA: 'Yesterday, we made GPT-5.6 Sol Ultra generally available' (2026-07-10), plus a health-intelligence post citing GPT-5.6 Luna outperforming GPT-5.5. @sama separately said GPT-5.6 is now the preferred model in Microsoft 365 Copilot. Multiple independent users report hitting rate limits on it, consistent with broad rollout beyond the ~20-org gated preview. Status advances confirmed → released; verification stays confirmed (official primary + broad corroboration)."
  - ts: 2026-07-14
    change: "Post-GA quality regression reported. @theo, @kimmonismus, testingcatalog, and @jxnlco (relaying @thsottiaux) say OpenAI quietly reduced GPT-5.6's reasoning-effort budget and discussed a context-window rollback (372k→272k), then compensated with 'banked resets' to ChatGPT Work/Codex usage limits for an estimated 500k-7M users. @theo partially walked back the precise mechanism in his own thread, so the exact technical cause is contested even though the regression-and-compensation event itself is well-corroborated. No official OpenAI statement on the regression. Status stays released; verification stays confirmed."
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
