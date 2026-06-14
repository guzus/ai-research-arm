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
expected: "Restoration pending — Anthropic 'working to restore access'; Polymarket priced ~65% restoration by 2026-07-01. No published Commerce/BIS document yet"
labels:
  - regulatory
  - export-control
  - anthropic
  - national-security
  - legal-action
verification: partial
sources:
  - "@AnthropicAI"
  - "@ClaudeDevs"
  - "@DavidSacks"
  - "@AndrewCurran_"
  - https://www.theverge.com/ai-artificial-intelligence/949553/anthropic-fable-5-mythos-5-government-national-security
  - https://arstechnica.com/ai/2026/06/anthropic-shuts-down-fable-mythos-models-following-trump-admin-directive/
  - https://www.wsj.com/tech/ai/amazon-ceos-talks-with-u-s-officials-triggered-crackdown-on-anthropic-models-dcc90578
created_at: 2026-06-14
updated_at: 2026-06-14
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-14
    change: "Created — US export-control directive (2026-06-12) bars foreign-national access to Anthropic's Fable 5 and Mythos 5, forcing a worldwide shutdown of both models for all customers late 2026-06-12 (other Claude models unaffected; sessions fall back to Opus 4.8). First US export control reaching a frontier model rather than chips. Reported trigger: an Amazon-surfaced Fable 5 jailbreak; Amazon CEO Jassy briefed Treasury's Bessent; White House asked Dario Amodei to fix or de-deploy and (per @DavidSacks) he refused. Anthropic calls it a 'misunderstanding,' disputes severity (says GPT-5.5 shares the vuln), and is working to restore access; dueling timelines on whether it was a 90-min ultimatum or hours of negotiation. Reuters/Techmeme, The Verge, Ars Technica, WSJ all carry it; Anthropic's own statement (@AnthropicAI, ~70K+ likes) + @ClaudeDevs product notice are primary for the suspension. Status confirmed (the order and shutdown are on-record/multi-source); verification partial (no published Commerce/BIS directive text; trigger details rest on anonymous/secondary sourcing). Product impact tracked on [[claude-fable-5]] and [[mythos-public-release]]"
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
