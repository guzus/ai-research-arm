---
slug: etched-funding-round-2026-08
title: Etched raises $700M at a $21B valuation
company: Etched
model: null
status: confirmed
status_note: |
  Etched announced on **2026-08-18** that it raised **$700M at a $21B
  valuation** from **Jane Street, Kleiner Perkins, Sequoia, a16z, Peter
  Thiel, BCV and Blackstone**. Posted by Etched's own account and relayed
  in-window by @jukan05 and @jxnlco.

  **The mark is the story.** Etched exited stealth on 2026-06-30 at a
  reported **~$5B** valuation with $800M raised and $1B+ in signed
  contracts ([[etched-stealth-2026-06]]). Seven weeks later it is marked at
  **$21B** — roughly **4.2x** — on a transformer-only inference ASIC
  (Sohu) whose first racks were said to ship "this summer." No independent
  Sohu-vs-NVIDIA benchmark has been published, and the customers behind the
  $1B contracts remain unnamed, so the re-rating is currently priced off
  the thesis rather than off measured silicon.

  The investor list is the other signal: **Jane Street** and **Blackstone**
  alongside the usual venture names is balance-sheet money, not seed money,
  which is what the ASIC buildout would require.
expected: "Round announced 2026-08-18. Pending: confirmation that Sohu racks shipped on the stated summer timeline, named customers behind the $1B+ in contracts, and any independent Sohu-vs-NVIDIA inference benchmark"
labels:
  - funding
  - hardware
  - inference
  - asic
  - nvidia-alternative
verification: confirmed
sources:
  - "@Etched"
  - "@jukan05"
  - "@jxnlco"
created_at: 2026-08-19
updated_at: 2026-08-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-19
    change: "Created — Etched announced on 2026-08-18 a $700M raise at a $21B valuation from Jane Street, Kleiner Perkins, Sequoia, a16z, Peter Thiel, BCV and Blackstone, posted by its own account and relayed by @jukan05 and @jxnlco. Roughly a 4.2x mark-up from the ~$5B recorded at the 2026-06-30 stealth exit ([[etched-stealth-2026-06]]), which is a distinct funding event and so gets its own ticket. Status confirmed / verification confirmed on the company's own announcement. Open: whether Sohu racks shipped on the stated summer timeline, who the $1B+ contracts are with, and any independent Sohu-vs-NVIDIA benchmark."
---

**Etched** raised **$700M at a $21B valuation** on **2026-08-18**, from a
list that mixes venture (Kleiner Perkins, Sequoia, a16z, BCV, Peter Thiel)
with balance-sheet capital (**Jane Street**, **Blackstone**).

**The interesting number is the multiple, not the round.** Etched came out
of stealth on **2026-06-30** at a reported **~$5B** with $800M raised and
$1B+ in signed customer contracts ([[etched-stealth-2026-06]]). Seven weeks
later it is marked at **$21B** — about **4.2x** — on the same product
story: **Sohu**, a transformer-only inference ASIC whose first racks were
said to ship "this summer."

**What is still unverified is unchanged from June.** No independent
Sohu-vs-NVIDIA inference benchmark has been published, the customers behind
the $1B+ in contracts are unnamed, and no confirmation was captured that
the summer racks actually shipped. So the re-rating is priced off the
thesis — that a fixed-function transformer ASIC beats general-purpose GPUs
badly enough to matter — rather than off measured silicon. The round is
`confirmed`; the product claims it implies are not.

**Why it lands now.** Serving economics are the live constraint across the
board this cycle: Cerebras announced CS-4 with a claimed 10x
throughput-per-MW the same week ([[cerebras-cs-4-2026-08]]), OpenAI is
building its own inference ASIC ([[openai-jalapeno-chip-2026-06]]), and the
frontier labs are visibly capacity-bound. Etched is being underwritten
against that, not against a benchmark.

**Transition triggers:**
- Sohu racks confirmed shipping, or a named customer deployment → UPDATE,
  and consider whether it belongs on the stealth ticket's product thread
  instead.
- Independent Sohu inference benchmark published → UPDATE.
- ≥4 weeks past announcement, settled into normal coverage →
  `closed: released-and-aged`.

**Dedup note:** the stealth exit, the Sohu product timeline and the $1B
contract claim stay on [[etched-stealth-2026-06]]. This ticket is scoped to
the August 2026 round. Rival inference silicon stays on
[[cerebras-cs-4-2026-08]], [[openai-jalapeno-chip-2026-06]] and
[[groq-funding-2026-06]].
