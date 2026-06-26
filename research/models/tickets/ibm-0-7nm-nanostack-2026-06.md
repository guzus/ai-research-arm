---
slug: ibm-0-7nm-nanostack-2026-06
title: IBM 0.7nm "nanostack" 3D transistor — sub-1nm research breakthrough
company: IBM
model: null
status: confirmed
status_note: |
  IBM announced the **world's first publicly disclosed sub-1nm semiconductor
  node** at **0.7nm (7 angstroms)** on 2026-06-25 (@IBMNews, ~5.3K likes), using
  a 3D **"nanostack"** transistor architecture that stacks transistors
  vertically with staggered arrangement — the industry's first 3D
  nanosheet-based design. Specs: **~100 billion transistors** on a
  fingernail-sized chip (~2x density vs IBM's 2021 2nm node), up to **50%
  higher performance OR 70% greater energy efficiency** vs 2nm, and **40% SRAM
  scaling improvement for AI workloads**. IBM Director of Research **Jay
  Gambetta** quoted on the announcement. **Critically research-stage**:
  production "as early as the next 5 years," with **no foundry commitment,
  tape-out, or production timeline** beyond that. IBM operates as a chip
  designer/licensor (sold its fabs to GlobalFoundries in 2014); the 0.7nm node
  depends on partners (TSMC/Samsung/Intel Foundry) adopting the nanostack
  design — none announced. IBM's own 2nm node from 2021 has not reached
  commercial production. Lands in a chip-heavy week: OpenAI Jalapeño ASIC
  ([[openai-jalapeno-chip-2026-06]], 3nm, shipping 2026–27) and NVIDIA DFlash
  ([[nvidia-dflash-2026-06]], shipping now) — three speeds of semiconductor
  innovation.
expected: "~5 years to commercial production (IBM's stated timeline, historically understated); no foundry partner commitment yet; IBM's 2021 2nm node still unshipped"
labels:
  - hardware
  - semiconductor
  - research
  - ai-infrastructure
  - ibm
verification: confirmed
sources:
  - https://x.com/IBMNews/status/2070100944017092734
  - "@IBMNews"
  - "@kimmonismus"
created_at: 2026-06-26
updated_at: 2026-06-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-26
    change: "Created — IBM announced the world's first publicly disclosed sub-1nm node at 0.7nm (7Å) on 2026-06-25 (@IBMNews ~5.3K likes): a 3D 'nanostack' transistor architecture, ~100B transistors on a fingernail-sized chip (~2x density vs its 2021 2nm node), up to 50% higher perf OR 70% greater energy efficiency vs 2nm, 40% SRAM scaling for AI workloads. Research-stage: production 'as early as the next 5 years,' no foundry commitment/tape-out. IBM Director of Research Jay Gambetta quoted. Official @IBMNews announcement + @kimmonismus technical relay → status confirmed (it is an announced, demonstrated research milestone), verification confirmed. Caveat logged: IBM's 2021 2nm node never reached commercial production; the 5-year timeline historically understates the real gap. Three-speeds-of-silicon context with [[openai-jalapeno-chip-2026-06]] and [[nvidia-dflash-2026-06]]."
---

IBM announced the **world's first publicly disclosed sub-1nm semiconductor
technology** — a **0.7nm (7 angstrom)** node using a 3D **"nanostack"**
transistor architecture — on 2026-06-25. It is a genuine engineering milestone
in extending Moore's Law via 3D architectures, with particular relevance to
AI-workload SRAM scaling.

**Why `confirmed` for a research demo.** The announcement is first-party
(@IBMNews official, ~5.3K likes) with consistent technical specifics relayed
independently (@kimmonismus, ~2.1K likes). `confirmed` here reflects that an
official, demonstrated research milestone was announced — the lifecycle
analog of "official announcement" — not that a product ships. It is
explicitly **research-stage, ~5 years from production**, with no foundry
commitment.

**The honest caveats.** (1) IBM's **2nm node from 2021 has not reached
commercial production** in any foundry; IBM is a chip designer/licensor, not a
volume manufacturer (it sold its fabs to GlobalFoundries in 2014). The 0.7nm
node depends on partners (TSMC/Samsung/Intel Foundry) adopting the nanostack
design — none have committed. (2) The 5-year timeline is standard for IBM
research breakthroughs and historically understates the real gap. (3) Node
naming has become marketing (TSMC's "2nm" is a process label, not a literal
dimension); the commercial node that eventually ships may carry a different
label.

**Context.** It lands in a chip-heavy week alongside OpenAI's Jalapeño ASIC
([[openai-jalapeno-chip-2026-06]], near-term 3nm silicon) and NVIDIA's
open-sourced DFlash ([[nvidia-dflash-2026-06]], shipping software
optimization) — illustrating three speeds of semiconductor innovation:
foundational research (IBM sub-1nm), near-term silicon (OpenAI/Broadcom), and
forward-deployed software (NVIDIA).

**Transition triggers:**
- A foundry partner commits to productionizing, or a technical paper/demo →
  UPDATE, append history.
- Production tape-out announced → advance toward `released`.
- Abandoned or superseded by a different IBM node → close per reason.

**Dedup note:** further 0.7nm/nanostack signal (foundry adoption, papers,
productionization) UPDATES this ticket. Other chip stories stay on their own
tickets.
