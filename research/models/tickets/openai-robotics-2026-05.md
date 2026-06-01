---
slug: openai-robotics-2026-05
title: OpenAI Robotics — world-simulation program formally becomes a named hardware-manufacturing org
company: OpenAI
model: null
status: confirmed
status_note: |
  Primary @sama post 2026-05-31 16:07 UTC (~7,612 likes / 522 RT /
  1,193 replies): "OpenAI Robotics is hiring, looking for exceptional
  full-stack hardware, ops, systems, and ML engineers to help us
  **program and manufacture robots** that are useful for society."
  Short-term: robots supporting skilled workers to build "future
  infrastructure"; long-term: "everyone having a personal robot doing
  anything they need." The world-simulation research program led by
  **Aditya Ramesh (@model_mechanic)** — OpenAI's DALL·E co-creator —
  "has evolved over the past year into OpenAI Robotics." Recruiting
  funnel: `robotics-recruiting@openai.com`. The "co-design between
  robotics hardware and ML research" wording is a vertical-integration
  commitment, not a partnership posture. @AndrewCurran_ (16:12 UTC)
  immediately read it as "the same world sim route Dr Fan is taking at
  NVIDIA" — paralleling the Cosmos / GR00T arc on
  [[nvidia-gtc-taipei-2026-06]]. OpenAI shuttered its first robotics
  team in 2021 and re-formed a smaller one in 2024; this is a
  strategic-direction post by the CEO with a named lead and a recruiting
  funnel, not a product disclosure.
expected: "Hardware prototype, manufacturing-partner disclosure, headcount, or first product launch TBD"
labels:
  - openai
  - robotics
  - world-simulation
  - org-launch
  - hardware
  - co-design
verification: confirmed
sources:
  - "@sama"
  - "@AndrewCurran_"
  - "@model_mechanic"
created_at: 2026-06-01
updated_at: 2026-06-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-01
    change: "Created — @sama primary post 2026-05-31 16:07 UTC (~7.6K likes / 522 RT) formalizes OpenAI Robotics: world-sim research program led by Aditya Ramesh (@model_mechanic, DALL·E co-creator) 'has evolved over the past year into OpenAI Robotics', hiring full-stack hardware/ops/systems/ML engineers to 'program and manufacture robots'. Short-term: skilled-worker infrastructure robots; long-term: 'everyone having a personal robot'. Recruiting at robotics-recruiting@openai.com. 'Co-design between robotics hardware and ML research' wording = vertical-integration commitment, not partnership. @AndrewCurran_ reads it as parallel to Dr Jim Fan / NVIDIA world-sim arc ([[nvidia-gtc-taipei-2026-06]] Cosmos / Isaac GR00T). Lands same weekend as [[figure-helix-02-2026-05]] capability disclosure"
---

**OpenAI Robotics** became a publicly named OpenAI org on
**2026-05-31 at 16:07 UTC**, when @sama posted a recruiting note that
doubles as the first official public framing. The post (~7,612 likes
/ 522 RT / 1,193 replies — among the cycle's most engaged frontier-lab
primaries) reads in full:

> "OpenAI Robotics is hiring, looking for exceptional full-stack
> hardware, ops, systems, and ML engineers to help us program and
> manufacture robots that are useful for society. AI should be able
> to help people in the physical world. In the short term, we are
> focused on robots to support skilled workers to build our future
> infrastructure; in the long term, we imagine everyone having a
> personal robot doing anything they need. Our world simulation
> research program, led by Aditya Ramesh (@model_mechanic), has
> evolved over the past year into OpenAI Robotics. Progress is rapid,
> and based on a foundation of co-design between robotics hardware
> and ML research. If you love working hands-on across the robotics
> stack and want to build the future, please consider joining us. Send
> an email with your background and evidence of exceptional
> accomplishment to: robotics-recruiting@openai.com."

**Why the post is load-bearing despite being a "hiring announcement":**

- The unit gets a **public name** ("OpenAI Robotics") and a **named
  lead** (Aditya Ramesh — @model_mechanic, OpenAI's DALL·E co-creator).
- @sama explicitly **commits the OpenAI brand to "program and
  manufacture robots"** — vertical-integration language, not a
  research-only posture.
- The "**co-design between robotics hardware and ML research**" phrase
  signals a hardware-CAPEX-bearing strategic direction; OpenAI
  shuttered its first robotics team in 2021 and re-formed a smaller
  research-only one in 2024 — this is the public framing of a
  third-generation, vertically-integrated unit.
- A **recruiting funnel** (`robotics-recruiting@openai.com`) is on
  the post.

**Strategic context.** @AndrewCurran_ at 16:12 UTC ("the same world
sim route Dr Fan is taking at NVIDIA") flagged the parallel arc to
NVIDIA's Cosmos / Isaac GR00T humanoid reference design on
[[nvidia-gtc-taipei-2026-06]]. The two together — plus the Figure
Helix-02 200-hour autonomous fleet run on
[[figure-helix-02-2026-05]] — define a coherent **physical-AI / VLA
competitive lane** within the same 72-hour window. The four-corner
positioning across labs is:

- **Anthropic** — enterprise infrastructure pricing
  ([[anthropic-series-h-2026-05]], [[mythos-public-release]]) + the
  Conway/Orbit/Operon/.EXT product surface
  ([[anthropic-conway-orbit-2026-05]]).
- **Google** — Gemini 3.5 family + Gemini Spark consumer agent +
  Antigravity orchestration ([[gemini-3-2-flash]],
  [[gemini-spark]]).
- **Microsoft** — homegrown MAI model stack + Copilot super app at
  Build 2026 ([[microsoft-build-2026-models]]).
- **OpenAI** — public commitment to manufacture robots (this ticket)
  + Codex platform agentic-coding cadence
  ([[openai-codex-platform-2026-05]]).

**Why this is its own ticket** (not folded into the Codex platform or
the OpenAI Rosalind biodefense ticket): the surface is structurally
new — *hardware* — and it has its own named lead, its own recruiting
funnel, and its own roadmap (hardware prototype, manufacturing partner,
first physical product). Codex is the developer-platform surface;
Rosalind is the gated bio model; Robotics is the manufacturing org.

**Transition triggers:**

- First hardware prototype disclosure or demo → UPDATE, possibly
  advance to `in-testing` if a private hardware preview ships.
- Manufacturing-partner disclosure (contract manufacturer / OEM
  partnership) → UPDATE.
- Acqui-hire of an existing robotics startup → UPDATE with the named
  target.
- First OpenAI-branded robot product ships → `status: released`.
- ≥15 daily cycles with no fresh signal AND no roadmap milestone →
  treat as standing strategic announcement; do not auto-close (it's
  primary @sama disclosure).

**Dedup note:** further OpenAI Robotics signal (headcount disclosures,
hardware partnerships, manufacturing decisions, first product, follow-
up posts from @gdb / @kevinweil / @model_mechanic) UPDATES this
ticket. A separate, distinct OpenAI-branded robot model (e.g. a
`gpt-robot-*` family) gets its own model ticket and back-links here.
The world-sim research lane that pre-dated the org name is not
separately tracked.
