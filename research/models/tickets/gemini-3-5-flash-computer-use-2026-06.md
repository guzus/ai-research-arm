---
slug: gemini-3-5-flash-computer-use-2026-06
title: Gemini 3.5 Flash gets Computer Use as a native built-in tool
company: Google / DeepMind
model: Gemini 3.5 Flash
status: released
status_note: |
  Google announced on 2026-06-26 (@Google official, ~76 likes) that **Computer
  Use is now a built-in tool in Gemini 3.5 Flash** — no longer a separate
  model — supporting **browser, mobile (Android emulator), and desktop**
  environments, **available immediately** via the Gemini API and the Gemini
  Enterprise Agent Platform. The safety architecture pairs targeted
  adversarial training with two enterprise safeguard systems: **Explicit User
  Confirmation** (requires opt-in before an agent can click/type/navigate) and
  **Enterprise Agents** (prevents violations of organizational security
  policies). @_philschmid published a working Android-emulator quickstart;
  @jimclydego summarized "computer use is no longer a separate Gemini model —
  it's built into Gemini 3.5 Flash." Google's differentiated thesis: fold
  agentic computer control into the **cheap/lightweight tier** for mass-market
  distribution at inference-cost parity with the base tier (rather than the Pro
  model). The base Gemini 3.5 Flash GA lives on the closed
  [[gemini-3-2-flash]] ticket (slug retained from the pre-I/O "3.2" leak); this
  ticket tracks the **Computer Use capability addition** as a distinct
  shipping event on top of that GA.
expected: null
labels:
  - google
  - computer-use
  - agentic
  - released
  - gemini-3-5
verification: confirmed
sources:
  - https://x.com/Google/status/2070155847606571286
  - "@Google"
  - "@_philschmid"
  - "@jimclydego"
created_at: 2026-06-26
updated_at: 2026-06-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-26
    change: "Created — Google announced (@Google official ~76 likes, 2026-06-26) that Computer Use is now a built-in tool in Gemini 3.5 Flash (not a separate model), supporting browser/mobile/desktop, available immediately via the Gemini API + Enterprise Agent Platform. Safety arch: adversarial training + Explicit User Confirmation + Enterprise Agents safeguards. @_philschmid published an Android-emulator quickstart; @jimclydego confirmed 'no longer a separate Gemini model.' Available today via API → status released; verification confirmed (official @Google + dev-advocate quickstart + independent relays). Distinct shipping event from the base 3.5 Flash GA (closed [[gemini-3-2-flash]]) — this ticket tracks the Computer Use capability addition. Context: lands same week as Anthropic's Claude Tag Slack agent; Google's bet is the cheap tier for mass-market agentic capability."
---

Google announced on 2026-06-26 that **Computer Use is now a built-in tool in
Gemini 3.5 Flash** — no longer a separate model. Developers can use 3.5 Flash
to build custom agents that see and take action across **browser, mobile
(Android emulator), and desktop** environments, **available immediately** via
the Gemini API and the Gemini Enterprise Agent Platform.

**Why its own ticket.** The base **Gemini 3.5 Flash** GA is tracked on the
closed [[gemini-3-2-flash]] ticket (slug retained from the pre-I/O "3.2" leak,
closed `released-and-aged`). A closed ticket is left alone; folding Computer
Use into the already-released 3.5 Flash is a **distinct shipping event** — a
new capability now publicly available — so it gets its own ticket rather than
reopening the closed GA ticket. The Pro tier stays on [[gemini-3-5-pro]].

**Google's differentiated thesis.** The notable strategic choice is folding
computer control into the **cheap/lightweight tier** (3.5 Flash) rather than
the Pro model — mass-market agentic capability at inference-cost parity with
the base tier. The safety architecture pairs adversarial training with
**Explicit User Confirmation** (opt-in before click/type/navigate) and
**Enterprise Agents** (org-policy enforcement).

**Honest caveats.** (1) Google has shipped computer-use capabilities before
(Project Mariner, earlier Gemini demos) that didn't gain enterprise traction
— the bottleneck was reliability, not availability. (2) The per-action user
confirmation may be too slow for scaled agentic workflows, a structural
latency disadvantage vs less-gated competitors. (3) 3.5 Flash is the
lightweight tier; whether the smaller model reliably executes complex
multi-step desktop interactions at scale is plausible but unproven. Lands the
same week as Anthropic's Claude Tag (Slack agent) — the industry-wide push to
embed agentic computer control at the model level.

**Transition triggers:**
- Enterprise adoption / latency-cost benchmarks vs dedicated computer-use
  agents → UPDATE, append history.
- A successor capability or Pro-tier computer-use → new ticket.
- ≥4 weeks past release, settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further Computer Use in 3.5 Flash signal (adoption, benchmarks,
safety findings) UPDATES this ticket. Gemini 3.5 Pro stays on [[gemini-3-5-pro]];
the base 3.5 Flash GA stays on the closed [[gemini-3-2-flash]].
