---
slug: anthropic-claude-science-2026-06
title: Anthropic Claude Science — agentic research workbench
company: Anthropic
model: Claude Science
status: released
status_note: |
  **Launched 2026-06-30 17:02 UTC** (@claudeai, ~11.8K likes: "Introducing
  Claude Science, a new app designed with every stage of research in mind"),
  an hour before Claude Sonnet 5 ([[claude-sonnet-5]]). An **agentic research
  environment**: artifacts traced to their code, **on-demand managed compute**,
  and **60+ optional scientific tools** (genomics, computational chemistry),
  plus a citation/calculation verification agent and local/HPC execution so
  sensitive data stays in-lab. **Debut partners: Novartis, Bristol Myers
  Squibb, Genentech** — Anthropic's biggest push into biopharma yet (MIT
  Technology Review calls it Anthropic's "newest flagship product").
  Integration partners self-confirmed (Modal compute, Harvard's ToolUniverse).
  Lands the **same day OpenAI shipped GeneBench-Pro**, a benchmark for AI
  research *judgment* — the AI-for-science race is now an open contest, not a
  clearing.

  **2026-07-04:** Secondary business-press coverage continues (a
  fourweekmba.com piece framing Claude Science as "rewriting the model
  company playbook") alongside notes on two life-sciences hires — Jonah Cool
  and John Jumper (a DeepMind alum). Still no primary @AnthropicAI post
  naming target diseases or partners. Status stays released; verification
  stays confirmed.
expected: null
labels:
  - anthropic
  - agentic
  - science
  - biopharma
  - released
verification: confirmed
sources:
  - "@claudeai"
  - "@endpts"
  - "@CMichaelGibson"
  - https://x.com/claudeai/status/2072002740830842899
created_at: 2026-07-01
updated_at: 2026-07-04
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-01
    change: "Created — Anthropic launched Claude Science on 2026-06-30 17:02 UTC (official @claudeai ~11.8K likes / 977 RT), an agentic research workbench with code-traced artifacts, on-demand managed compute, and 60+ optional scientific tools, debuting alongside Novartis, Bristol Myers Squibb and Genentech. Multi-source confirmed via trade press (Endpoints News, STAT/Matthew Herper); Modal and Harvard's ToolUniverse self-confirmed integrations. Shipped an hour before Sonnet 5 ([[claude-sonnet-5]]) and the same day OpenAI published GeneBench-Pro. Status released, verification confirmed (official primary + independent trade-press). Scope skepticism noted (a wet-lab-bio tool, not 'all of science'; researcher data-appropriation concerns)."
  - ts: 2026-07-04
    change: "Secondary business-press coverage continues (fourweekmba.com: 'rewriting the model company playbook') plus notes on life-sciences hire Jonah Cool and DeepMind alum John Jumper. Still no primary @AnthropicAI post naming target diseases or partners. Status stays released; verification stays confirmed."
---

**Claude Science** is Anthropic's agentic research environment, launched
**2026-06-30 (17:02 UTC)** an hour before Claude Sonnet 5
([[claude-sonnet-5]]) — a two-launch afternoon that signals Anthropic
pressing a product-cadence advantage. Observers describe it as merging
PubMed, Jupyter, R, and cluster terminals into one agentic session.

**What ships.** Artifacts are traced back to the code that produced them,
compute environments are **managed on demand**, and **60+ optional
scientific tools** (genomics, computational chemistry) can be attached. A
verification agent checks citations and calculations, and **local/HPC
execution** keeps sensitive data in-lab. It debuts with named biopharma
partners — **Novartis, Bristol Myers Squibb, Genentech** — in what
Endpoints News calls Anthropic's biggest biopharma push yet; MIT Technology
Review frames it as Anthropic's "newest flagship product."

**Confirmed vs. contested.** The launch is multi-sourced (official @claudeai
plus Endpoints News and STAT), and integration partners Modal (compute) and
Harvard's ToolUniverse self-confirmed — so `released` / `confirmed`. The
scope framing is contested: one MD-PhD flagged "Claude Science" as premature
for what is really a **cell-biology / wet-lab** product, and researchers
raised data-appropriation concerns about uploading proprietary work. The
"first mover" framing is also wrong — **OpenAI shipped GeneBench-Pro the
same day** (a benchmark for AI *research judgment*), and Google/Meta hold
standing AI-for-science bets.

**Why its own ticket.** Claude Science is a distinct **product launch**, not
a model release — it orchestrates models (including Opus 4.8 / Sonnet 5)
over scientific tooling. Model-line signal stays on the respective model
tickets; this ticket carries the Claude Science product lifecycle.

**Transition triggers:**
- Real named deployments moving past launch-partner optics → UPDATE.
- Pricing, API, or capability expansions → append history here.
- ≥4 weeks settled into normal coverage → close `released-and-aged`.

**Dedup note:** further Claude Science product signal UPDATES this ticket.
The underlying models stay on [[claude-sonnet-5]] / [[opus-4-8]]; OpenAI's
science-benchmark push is a separate lane if it warrants its own ticket.
