---
slug: anthropic-fable-mythos-export-control-2026-06
title: US export-control order forces Anthropic to suspend Fable 5 & Mythos 5 worldwide
company: Anthropic / US Government
model: null
status: confirmed
status_note: |
  On **2026-06-12** the US government issued an **export-control directive**
  barring access to **Fable 5** ([[claude-fable-5]]) and **Mythos 5**
  ([[mythos-public-release]]) by **any foreign national** — inside or outside
  the US, including Anthropic's own foreign-national employees — forcing
  Anthropic to **abruptly disable both models for ALL customers worldwide**
  late 2026-06-12 to stay compliant. All other Claude models are unaffected;
  new sessions fall back to **Opus 4.8** ([[opus-4-8]]). This is widely read as
  the **first time US export controls reached a frontier *model* rather than
  chips.**

  **Trigger (reported, not in a primary govt doc):** a jailbreak of Fable 5's
  guardrails — Amazon CEO **Andy Jassy** told Treasury Sec. **Bessent** that
  Amazon researchers induced Fable 5 to produce cyberattack-usable info; the
  White House convened, asked **Dario Amodei** to fix or de-deploy, and (per
  White House AI czar @DavidSacks) Amodei refused → export control followed.
  Anthropic disputes severity, calls it a "misunderstanding," argues the same
  vuln exists in other public models (e.g. GPT-5.5), and says it is working to
  restore access. Anthropic's account says it got a **90-minute hard deadline**;
  the Admin says it "begged for hours." The actual Commerce/Lutnick directive
  text remains **unpublished**.

  **As of 2026-06-15 (day 3):** both models remain suspended worldwide — no
  restoration, license carve-out, or published Commerce/BIS directive yet, and
  the open-weights / sovereignty discourse continues. Additional *unverified*
  secondary/social claims are circulating and are **not** primary-sourced:
  Microsoft reportedly told its own staff to stop using Fable 5 (citing a
  30-day data-retention rule) even before the order; **Andrej Karpathy** and
  other non-US Anthropic staff reportedly locked out; and a low-credibility
  claim that a China-linked group had obtained access to Mythos.

  **As of 2026-06-16 (day 4):** still no restoration. Anthropic leaders **met
  with White House officials to discuss Fable 5's risks and the talks ended
  without consensus** (per WIRED, secondary), with export controls left in
  place — confirming the dispute is now a sustained standoff rather than a
  one-off shock. Reporting (FT, attributed to a source close to OpenAI) frames
  the directive as a **"deemed export control"** — the deemed-export regime
  normally reserved for defense/nuclear tech, where a foreign national merely
  *touching* the technology counts as an export — and says **frontier labs
  worked with the government** as the industry pushes to keep foreign-national
  researchers able to work on advanced models. Anthropic's leadership is
  reportedly **split internally** on how much risk Fable 5 actually presents.
  All remains secondary/social-sourced; the Commerce/BIS directive text is
  still unpublished.

  **As of 2026-06-18 (days 5–6):** still no restoration, but the documentary
  record hardened and the dispute internationalized. The **full BIS "Is
  Informed" letter** Lutnick sent Amodei — **obtained by Bloomberg** — circulated
  in full: an individually-validated license now required to release Mythos 5 /
  Fable 5 to **any "foreign person" worldwide**, including **"deemed exports"** to
  non-US persons inside the US, under threat of criminal/civil penalty, invoking
  EAR §744.22(b). Two **export-control lawyers** (@CharlieBull0ck, @alasdairpr)
  published teardowns arguing the order is legally vulnerable (EAR
  published-information carve-out, First Amendment, AI-as-a-service may not be an
  "export" of an "item"). On **2026-06-17** the frontier-lab CEOs (Amodei,
  Altman, Hassabis) appeared at the **G7 summit in Évian, France**, where
  **Macron held a bilateral with Amodei** reportedly to seek Europe's Claude
  access back; **WIRED** reports the admin will only allow a re-release if
  guardrails are made **uncircumventable** (experts say impossible), AI czar
  **David Sacks** blamed Anthropic's "needlessly confrontational posture," and
  **Amodei/Hassabis called for a US-led, China-excluding AI coalition**. A
  **WIRED scoop** (Matsakis/Zeff) refines the trigger to a **two-step sequence**:
  South Korean carrier **SK Telecom's** Mythos access (alleged China ties, which
  SKT denies) cracked Washington's trust **first**, and Amazon's Fable 5
  jailbreak report was the **final straw** — not the origin. **WSJ** surfaced
  Lutnick's "that's the point" reply to Amodei; **40+ CISOs** signed a letter
  demanding reversal; **JPMorgan pulled Claude for Hong Kong staff** (following
  Goldman, licensing-driven) as access fragmentation reached enterprise. With the
  full letter text Bloomberg-obtained and independently read, corroborated by
  WIRED/WSJ/FT named reporting, **verification advances to `confirmed`** (the
  government's own PDF is still unpublished, the lone remaining gap).

  **As of 2026-06-21 (days 7–9):** still no restoration; the standoff warmed
  rhetorically but the order stands. Three threads advanced. (1) **WIRED /
  Tom's Hardware / Korea JoongAng named the carrier as SK Telecom** — South
  Korea's largest wireless operator and a **~$100M Anthropic investor** since
  2023, reportedly among **~150 orgs added to Project Glasswing** in early June,
  with Mythos 5 access **revoked days before** the suspension; SKT flatly
  **denies** the China linkage. This reframes the trigger from a
  model-capability/jailbreak story toward an **access-control / supply-chain-
  trust** one. (2) Anthropic's **rewritten privacy policy** (published
  2026-06-08, effective **2026-07-08**) lets it ask Free/Pro/Max users to
  **verify identity** — a government-ID image, a photo/video, and
  **facial-geometry biometric templates** (not applied to business subs) —
  read (flagged by Simon Willison) as the staged mechanism to reopen Fable 5 /
  Mythos 5 to **verified US citizens** under a nationality-scoped restoration
  rather than keep both dark for everyone. (3) A fuller **Trump/Axios
  transcript** circulated — he calls Anthropic "not now, but a week ago maybe"
  a national-security threat, praises Amodei, and names "a competitor and a
  part owner that turned Anthropic in" (widely **inferred as Amazon**, not a
  name Trump said). **No Commerce order has been rescinded** — warming rhetoric,
  not a lifted ban; a viral "Fable 5 RETURNS after government shutdown" roundup
  is **false** (Anthropic's own feed shows no restoration). The **June 22
  subscription cliff** arrives one day out. Status stays `confirmed`;
  verification stays `confirmed`.

  **As of 2026-06-22 (day 10):** still no restoration; the inferred restoration
  mechanism acquired a **hard date and a vendor**. Anthropic's revised privacy
  policy now carries a firm enforcement date — **starting 2026-07-08**, Claude
  **Free/Pro/Max** users may be required to upload a **government ID** (passport,
  license, national ID) and capture a **live selfie**, processed by third-party
  verifier **Persona** (not applied to business subs). Framed by Anthropic as
  "age and identity verification," but the timing — two weeks after foreign
  access to Fable 5 / Mythos was cut — is widely read as the **compliance gate
  for a US-only model restoration**, now with trade-press footing (Tech Times).
  The policy and date are confirmed fact; the "this is how Fable comes back,
  US-only" purpose remains well-motivated inference, not an Anthropic statement.
  Status stays `confirmed`; verification stays `confirmed`.

  **As of 2026-06-26 (day ~14):** still no formal Commerce rescission, but the
  inferred US-only restoration mechanism crossed from policy inference into a
  **product artifact**. Fable 5 reappeared in the **AWS Bedrock catalog** as
  `anthropic.claude-fable-5` (Active, sold by Anthropic; multi-source
  screenshots), and **Claude Code v2.1.190 binaries** now carry bundled-weekly
  Fable 5 usage strings — product impact tracked on [[claude-fable-5]]. Access
  is gated through the **Persona US-ID verification** (live 2026-07-08) +
  use-case review + Anthropic approval first inferred here on day 10. The
  political backdrop warmed: **Trump walked back the "national-security threat"
  framing** ("not now, but a week ago maybe"), and cofounder **Tom Brown
  replaced Dario Amodei** as the White House point person — the admin is
  reportedly "happier with Brown." Anthropic's own status page still shows the
  2026-06-13 suspension as active with no restoration date, and the
  Commerce/BIS directive text remains unpublished, so this is a **controlled
  re-opening** (US-ID-gated Bedrock availability), not a lifted ban. The same
  review logic is now being applied to OpenAI's GPT-5.6 ([[openai-gpt-5-6]]),
  which Axios reports was classified "Mythos-like." Status stays `confirmed`;
  verification stays `confirmed`.

  **As of 2026-06-29 (day ~17):** still no formal rescission; the order's
  **geographic fallout** surfaced. **Austria publicly courted Anthropic to
  relocate to the EU** — an open letter offering "legal certainty, market
  access, capital" and pitching Anthropic's safety-first values as "a deeply
  European attitude." Analysts read it as **performative** (compute, USG
  relationships, and the Mythos 5 license are all US-bound; @kimmonismus:
  anyone who thinks the US would let Anthropic move to Europe if Fable/Mythos
  are deemed national security is "out of touch with reality") and the **first
  explicit acknowledgment that US export controls structurally exclude Europe**
  from frontier models — the UK's similar overtures months ago went nowhere.
  The **de facto licensing regime** hardened into a recognized "new normal"
  (The Information's Leo Schwartz: "a de facto licensing regime with no rules"),
  now visible in two fresh data points: GPT-5.6 Sol's government-gated preview
  ([[openai-gpt-5-6]]) and Anthropic's Alibaba-distillation letter
  ([[anthropic-alibaba-distillation-2026-06]]). Anthropic's revised privacy
  policy (ID + biometric verification) takes effect **2026-07-08**. Status stays
  `confirmed`; verification stays `confirmed`.

  **As of 2026-06-30 (day ~18) — the gate visibly reverses (first-party):**
  The official **@AnthropicAI** account (June 27 statement, ~30K likes)
  confirmed the **first un-gating**: "the government notified us that Mythos 5…
  can be redeployed to a set of US organizations that operate and defend
  critical infrastructure," and Anthropic is "continuing to work with the
  government to expand access to Mythos 5 and **make Fable 5 available for
  general use again**." Commerce Secretary **Lutnick's June 26 letter** cleared
  Mythos 5 for **~100 vetted US companies and federal agencies** (list amendable
  "at any time") — relayed via an Axios scoop (@WesRoth, @argofowl, @Mr_Salio).
  **Fable 5's general re-release is reported imminent but NOT confirmed live**:
  relays say "this week," but no Anthropic status post confirms it, and
  Pentagon/NSA sign-off was reportedly still pending. A fresh datamine
  (**@M1Astra**, June 30) of Claude app strings ties Fable 5 to **a usage-credit
  system billed separately from your plan, gated behind identity verification**
  ("Your credits will be added once your identity is verified") — consistent
  with the Persona US-ID mechanism (live 2026-07-08), though string presence ≠
  shipped policy. The managed-access regime is now visibly **two-way** (gate →
  selectively un-gate to vetted users), and Marc Andreessen's new Pentagon
  Defense Policy Board seat ([[andreessen-defense-policy-board-2026-06]]) sits
  adjacent to the gatekeeping. Status stays `confirmed`; verification stays
  `confirmed`.
expected: "Day ~18: the gate reverses — @AnthropicAI first-party confirmed Mythos 5 cleared for ~100 critical-infra orgs (Lutnick June 26 letter, list amendable 'at any time'), and says it is working to make Fable 5 available for general use again. Fable 5 re-release reported imminent ('this week') but NOT confirmed live (Pentagon/NSA sign-off reportedly pending). Datamined Claude app strings (@M1Astra, June 30) tie Fable 5 to a separate metered-credit system gated behind identity verification ('credits added once your identity is verified'), consistent with the Persona US-ID mechanism (live 2026-07-08). Andreessen's Pentagon Defense Policy Board seat ([[andreessen-defense-policy-board-2026-06]]) now sits adjacent to the gatekeeping. Earlier: No formal Commerce rescission (day ~17). Austria publicly courted Anthropic to relocate to the EU (open letter; read as performative, first explicit acknowledgment US export controls structurally exclude Europe). De facto licensing regime now a recognized 'new normal' (GPT-5.6 Sol gated preview + Alibaba-distillation letter as fresh data points). Persona US-ID verification live 2026-07-08. Earlier: US-only restoration mechanism now has a product artifact — Fable 5 active in AWS Bedrock (anthropic.claude-fable-5) + Claude Code bundled-weekly usage strings, gated by Persona US-ID verification (live 2026-07-08) + use-case review + Anthropic approval (product impact on [[claude-fable-5]]). Political thaw: Trump walked back the national-security-threat framing; Tom Brown replaced Dario as WH point person. Anthropic status page still shows the 2026-06-13 suspension active; Commerce/BIS directive text still unpublished. Same review logic now applied to OpenAI GPT-5.6 ([[openai-gpt-5-6]], 'Mythos-like' per Axios). SK Telecom named as the Project Glasswing carrier (denies China ties)"
labels:
  - regulatory
  - export-control
  - anthropic
  - national-security
  - legal-action
verification: confirmed
sources:
  - "@AnthropicAI"
  - "@ClaudeDevs"
  - "@DavidSacks"
  - "@AndrewCurran_"
  - https://www.theverge.com/ai-artificial-intelligence/949553/anthropic-fable-5-mythos-5-government-national-security
  - https://arstechnica.com/ai/2026/06/anthropic-shuts-down-fable-mythos-models-following-trump-admin-directive/
  - https://www.wsj.com/tech/ai/amazon-ceos-talks-with-u-s-officials-triggered-crackdown-on-anthropic-models-dcc90578
  - "@WIRED"
  - "@LaurenGoode"
  - "@AmrithRamkumar"
  - "@alasdairpr"
  - https://www.tomshardware.com/tech-industry/artificial-intelligence/sk-telecom-named-as-the-korean-carrier-at-the-center-of-anthropics-mythos-export-controls
  - https://www.computerworld.com/article/4185515/anthropics-new-privacy-policy-offers-us-consumers-a-way-around-fable-ban-2.html
  - https://www.techtimes.com/articles/claude-identity-verification-persona-july-8
  - "@chetaslua"
  - "@alphabatcher"
  - "@kimmonismus"
  - "@WesRoth"
  - "@M1Astra"
created_at: 2026-06-14
updated_at: 2026-06-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-14
    change: "Created — US export-control directive (2026-06-12) bars foreign-national access to Anthropic's Fable 5 and Mythos 5, forcing a worldwide shutdown of both models for all customers late 2026-06-12 (other Claude models unaffected; sessions fall back to Opus 4.8). First US export control reaching a frontier model rather than chips. Reported trigger: an Amazon-surfaced Fable 5 jailbreak; Amazon CEO Jassy briefed Treasury's Bessent; White House asked Dario Amodei to fix or de-deploy and (per @DavidSacks) he refused. Anthropic calls it a 'misunderstanding,' disputes severity (says GPT-5.5 shares the vuln), and is working to restore access; dueling timelines on whether it was a 90-min ultimatum or hours of negotiation. Reuters/Techmeme, The Verge, Ars Technica, WSJ all carry it; Anthropic's own statement (@AnthropicAI, ~70K+ likes) + @ClaudeDevs product notice are primary for the suspension. Status confirmed (the order and shutdown are on-record/multi-source); verification partial (no published Commerce/BIS directive text; trigger details rest on anonymous/secondary sourcing). Product impact tracked on [[claude-fable-5]] and [[mythos-public-release]]"
  - ts: 2026-06-15
    change: "Day 3 — Fable 5 and Mythos 5 remain suspended worldwide; no restoration, license carve-out, or published Commerce/BIS directive text yet, and the open-weights / sovereignty discourse continues. Additional *unverified* secondary/social claims circulating (none primary-sourced): Microsoft reportedly told its own staff to stop using Fable 5 over a 30-day data-retention rule even before the order; Andrej Karpathy and other non-US Anthropic staff reportedly locked out; and a low-credibility claim that a China-linked group obtained access to Mythos. Status stays confirmed; verification stays partial."
  - ts: 2026-06-16
    change: "Day 4 — still no restoration; the dispute hardens into a sustained standoff. Anthropic leaders met with White House officials over Fable 5's risks and the talks ended without consensus, export controls left in place (WIRED, secondary). FT (source close to OpenAI) frames the order as a 'deemed export control' — the defense/nuclear-style regime where a foreign national merely touching the tech counts as an export — and reports frontier labs worked with the government, with the industry now pushing to preserve foreign-national researchers' ability to work on advanced models; Anthropic's leadership is reportedly split internally on how much risk Fable 5 presents. Still no published Commerce/BIS directive text. Status stays confirmed; verification stays partial (all new detail secondary/social)."
  - ts: 2026-06-18
    change: "Days 5–6 — documentary record hardens, dispute internationalizes; verification → confirmed. The full BIS 'Is Informed' letter (Lutnick→Amodei), obtained by Bloomberg, circulated in full: individually-validated license required to release Mythos 5/Fable 5 to any 'foreign person' worldwide incl. 'deemed exports' inside the US, under criminal/civil penalty, invoking EAR §744.22(b). Two export-control lawyers (@CharlieBull0ck, @alasdairpr) published teardowns (published-information carve-out, First Amendment, AI-as-a-service may not be an 'export'). 2026-06-17: frontier-lab CEOs at G7 Évian; Macron–Amodei bilateral reportedly sought Europe's Claude access back; WIRED says re-release bar is uncircumventable guardrails (experts: impossible); Sacks blamed Anthropic's 'confrontational posture'; Amodei/Hassabis called for a US-led China-excluding AI coalition. WIRED scoop (Matsakis/Zeff) refines trigger to a two-step sequence — SK Telecom's Mythos access (alleged China ties, SKT denies) cracked trust first, Amazon's jailbreak report was the final straw. WSJ surfaced Lutnick's 'that's the point'; 40+ CISOs signed a reversal letter; JPMorgan pulled Claude for Hong Kong staff (after Goldman, licensing-driven). Bloomberg-obtained letter text + WIRED/WSJ/FT named reporting → verification confirmed; only the government's own PDF remains unpublished."
  - ts: 2026-06-21
    change: "Days 7–9 — still no restoration; rhetoric warmed, order stands. (1) WIRED/Tom's Hardware/Korea JoongAng named the carrier as SK Telecom — South Korea's largest wireless operator and a ~$100M Anthropic investor since 2023, reportedly among ~150 orgs added to Project Glasswing in early June with Mythos 5 access revoked days before the suspension; SKT denies China ties, reframing the trigger toward access-control / supply-chain-trust. (2) Anthropic's rewritten privacy policy (published 2026-06-08, effective 2026-07-08) lets it ask Free/Pro/Max users to verify identity (government-ID image, photo/video, facial-geometry biometric templates; not business subs) — read (Simon Willison) as the staged mechanism to reopen Fable 5/Mythos 5 to verified US citizens. (3) Fuller Trump/Axios transcript: 'not now, but a week ago maybe' a threat, praises Amodei, names 'a competitor and a part owner that turned Anthropic in' (widely inferred as Amazon — not a name Trump said). No Commerce rescission; a viral 'Fable 5 RETURNS' roundup is false. June 22 subscription cliff one day out. Status stays confirmed; verification stays confirmed. Sources: Tom's Hardware (SKT), Computerworld/The Register (privacy policy), @AndrewCurran_ (Trump transcript)."
  - ts: 2026-06-22
    change: "Day 10 — still no restoration; the inferred US-only re-entry mechanism got a hard date and a vendor. Anthropic's revised privacy policy now sets enforcement at 2026-07-08: Free/Pro/Max users may be required to upload a government ID (passport/license/national ID) and a live selfie, processed by third-party verifier Persona (not business subs). Anthropic labels it 'age and identity verification,' but the timing (two weeks after the foreign-access cutoff) is widely read as the compliance gate for a US-only model restoration, now with trade-press footing (Tech Times). Policy + date are confirmed fact; the US-only-restoration purpose stays inference. Status stays confirmed; verification stays confirmed."
  - ts: 2026-06-26
    change: "Day ~14 — no formal Commerce rescission, but the US-only restoration mechanism crossed from policy inference into a product artifact. Fable 5 reappeared in the AWS Bedrock catalog as anthropic.claude-fable-5 (Active, sold by Anthropic; multi-source screenshots) and Claude Code v2.1.190 binaries now carry bundled-weekly Fable 5 usage strings (product impact on [[claude-fable-5]]). Access gated by Persona US-ID verification (live 2026-07-08) + use-case review + Anthropic approval — the re-entry path first inferred on day 10. Political thaw: Trump walked back the 'national-security threat' framing; Tom Brown replaced Dario Amodei as WH point person (admin reportedly 'happier with Brown'). Anthropic's status page still shows the 06-13 suspension active and the Commerce/BIS directive text remains unpublished — a controlled US-ID-gated re-opening, not a lifted ban. The same review logic is now applied to OpenAI GPT-5.6 ([[openai-gpt-5-6]], 'Mythos-like' per Axios). Status stays confirmed; verification stays confirmed."
  - ts: 2026-06-29
    change: "Day ~17 — still no formal rescission; the order's geographic fallout surfaced. Austria publicly courted Anthropic to relocate to the EU (open letter offering 'legal certainty, market access, capital,' pitching Anthropic's safety-first values as 'a deeply European attitude'), read by analysts as performative (compute/USG ties/Mythos license are all US-bound; @kimmonismus: anyone who thinks the US would let Anthropic move to Europe if Fable/Mythos are national security is 'out of touch with reality') and the first explicit acknowledgment that US export controls structurally exclude Europe from frontier models — the UK's similar overtures months ago went nowhere. The de facto frontier-model licensing regime hardened into a recognized 'new normal' (The Information's Leo Schwartz: 'a de facto licensing regime with no rules'), now visible in two fresh data points — GPT-5.6 Sol's government-gated preview ([[openai-gpt-5-6]]) and Anthropic's Alibaba-distillation letter ([[anthropic-alibaba-distillation-2026-06]]). Anthropic's revised privacy policy (ID + biometric verification) takes effect 2026-07-08. Status stays confirmed; verification stays confirmed. Sources: @kimmonismus, 2026-06-29 digest (Policy & Regulation)."
  - ts: 2026-06-30
    change: "Day ~18 — the gate visibly reverses, first-party. @AnthropicAI (June 27 statement, ~30K likes) confirmed the government notified it that Mythos 5 can be redeployed to a set of US organizations that defend critical infrastructure, and that it is working to expand Mythos 5 access and 'make Fable 5 available for general use again.' Commerce Sec. Lutnick's June 26 letter cleared Mythos 5 for ~100 vetted US companies/federal agencies (list amendable 'at any time'; Axios scoop relayed by @WesRoth/@argofowl/@Mr_Salio). Fable 5's general re-release reported imminent ('this week') but NOT confirmed live — no Anthropic status post, Pentagon/NSA sign-off reportedly pending. Fresh datamine (@M1Astra, June 30) of Claude app strings ties Fable 5 to a usage-credit system billed separately from your plan and gated behind identity verification ('Your credits will be added once your identity is verified'), consistent with the Persona US-ID mechanism (live 2026-07-08); string presence ≠ shipped policy. Managed-access regime now visibly two-way (gate → selectively un-gate to vetted users); Andreessen's Pentagon Defense Policy Board seat ([[andreessen-defense-policy-board-2026-06]]) sits adjacent. Status stays confirmed; verification stays confirmed. Sources: @AnthropicAI (primary), @WesRoth/Axios relay, @M1Astra datamine, 2026-06-30 digest + Twitter pulse."
---

On **2026-06-12** the US government issued an **export-control directive**
that barred access to Anthropic's two strongest models — the public
**Fable 5** ([[claude-fable-5]]) and the gated **Mythos 5**
([[mythos-public-release]]) — by **any foreign national**, inside or
outside the United States, including Anthropic's own foreign-national
staff. To comply, Anthropic **abruptly disabled both models for every
customer worldwide** late that night. All other Claude models stayed up,
and new sessions fall back to **Opus 4.8** ([[opus-4-8]]).

**Why it's its own ticket.** This is a discrete **regulatory / legal
action** — the event class this timeline tracks alongside releases,
funding, and acquisitions. It is distinct from the model-release
lifecycles it disrupts: the product impact (sessions erroring, fallback
to Opus 4.8, the free-access window) is recorded on the [[claude-fable-5]]
and [[mythos-public-release]] tickets; this ticket carries the **order
itself** — its scope, trigger, and resolution.

**The reported trigger.** Coverage converges on a Fable 5 jailbreak:
Amazon CEO **Andy Jassy** (Anthropic's largest backer) told Treasury
Secretary **Scott Bessent** that Amazon researchers had, via a prompt
sequence, induced Fable 5 to produce information usable in cyberattacks.
The White House convened, security researchers corroborated the finding,
and the Administration asked **Dario Amodei** to fix the jailbreak or
de-deploy the model. Per White House AI czar **David Sacks**, Amodei
refused; the export control followed. Anthropic's camp says it was handed
a **90-minute hard deadline**; a senior White House official says controls
were "a last resort after begging them for hours."

**What's confirmed vs. reported.** The suspension is first-party
(Anthropic's own statement + @ClaudeDevs notice) and corroborated by
Reuters/Techmeme, The Verge, Ars Technica, and WSJ — hence `confirmed`.
But the **actual Commerce/BIS directive text is unpublished**, and the
Jassy→Bessent trigger and the "refused to fix" framing rest on anonymous
or interested-party sourcing — hence `verification: partial`. Anthropic
disputes the jailbreak's severity and argues other public models (e.g.
GPT-5.5) can exploit the same vulnerability, framing the singling-out of
Fable as selective.

**Why it matters.** Treating a hosted frontier model as an
export-controlled strategic capability is a precedent shift, and it
supercharged the open-weights / sovereignty discourse (r/LocalLLaMA
torrent-network calls, "APIs are rented, local weights are forever").
Anthropic's deputy CISO estimated open weights reach this capability in
~7–10 months — raising whether export-controlling a hosted model buys
durable time at all. It also lands against Anthropic's pending IPO
([[anthropic-ipo-2026-06]]) and a longer admin–Anthropic rupture (Pentagon
"kicked Anthropic out" months earlier, per @PeteHegseth).

**Transition triggers:**
- Anthropic restores Fable 5 / Mythos 5, or a license/carve-out is granted
  → UPDATE, append history (do not close until settled).
- A published Commerce/BIS directive or White House statement → UPDATE,
  advance `verification` toward `confirmed`.
- The order is formally rescinded or made permanent → UPDATE; close only
  once the dispute fully resolves and rolls into normal coverage.
- ≥4 weeks of settled coverage after resolution → `closed: released-and-aged`.

**Dedup note:** further signal about the *order* (restoration, license,
published directive text, legal challenge) UPDATES this ticket. Signal
about the *models'* capabilities, pricing, or availability stays on
[[claude-fable-5]] and [[mythos-public-release]].
