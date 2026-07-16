---
slug: openai-codex-hardware-2026-06
title: OpenAI teases its first Codex hardware — a Work Louder macro pad, reveal July 15
company: OpenAI
model: null
status: released
status_note: |
  Teased **2026-06-30** (The Verge via Techmeme; OpenAI's own teaser video):
  OpenAI launched a **Codex-focused physical device** built with
  mechanical-keyboard maker **Work Louder**, with the reveal happening
  on schedule on **2026-07-15**. The silhouette matched Work Louder's
  **Creator Micro 2** (13 mechanical switches, joystick, touch sensor): a
  macro pad for binding Codex actions ("refactor this," "write tests") to
  physical keys. Explicitly **NOT** the Jony Ive AI device.

  **Reveal (2026-07-15):** the product is named **Codex Micro**, priced
  **$230**, live now on the **OpenAI Supply** site (product id
  `kbd-1.0-codex-micro`), built with Work Louder as teased — **6 RGB
  agent-status keys, a reasoning-level dial, Bluetooth/USB-C**. Reported
  by **@testingcatalog** and **@kimmonismus**, independently corroborated
  by **@rohanpaul_ai** on 2026-07-16 → status `released`, verification
  `confirmed`.
expected: null
labels:
  - hardware
  - openai
  - codex
  - developer-tools
verification: confirmed
sources:
  - "@Techmeme"
  - https://x.com/Techmeme/status/2071768358182334546
  - "@testingcatalog"
  - https://x.com/testingcatalog/status/2077426702582792549
  - "@kimmonismus"
  - "@rohanpaul_ai"
created_at: 2026-06-30
updated_at: 2026-07-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-30
    change: "Created — OpenAI teased its first Codex hardware (2026-06-30, The Verge via Techmeme + OpenAI teaser video): a physical device built with keyboard maker Work Louder, reveal July 15, 'your favorite Codex shortcuts are getting an upgrade.' Silhouette matches Work Louder's Creator Micro 2 (13 switches, joystick, touch sensor) — a macro pad for binding Codex actions to physical keys; explicitly not the Jony Ive device. Status confirmed (official teaser, The Verge/Techmeme); verification confirmed; spec/price/ambitions unknown until July 15 (teased, not shipped). Links to the Codex platform lane ([[openai-codex-platform-2026-05]])."
  - ts: 2026-07-16
    change: "Reveal happened on schedule 2026-07-15: the product is Codex Micro, $230, live on the OpenAI Supply site (product id kbd-1.0-codex-micro), built with Work Louder — 6 RGB agent-status keys, a reasoning-level dial, Bluetooth/USB-C. Reported by @testingcatalog and @kimmonismus, independently corroborated by @rohanpaul_ai on 2026-07-16 → status advances confirmed → released; expected set to null (nothing pending, it shipped)."
---

On **2026-06-30**, OpenAI teased its **first Codex hardware** — a physical
device built in partnership with mechanical-keyboard maker **Work Louder**,
with a **July 15** reveal and the tagline "your favorite Codex shortcuts are
getting an upgrade." The silhouette matches Work Louder's **Creator Micro
2** (13 mechanical switches, joystick, touch sensor): a macro pad for binding
Codex actions ("refactor this," "write tests") to physical keys. It is
explicitly **not** the Jony Ive AI device.

**Why a separate ticket.** This is a discrete **hardware product** event,
distinct from the Codex software platform ([[openai-codex-platform-2026-05]]).
A teased device with a named partner and a launch date is a trackable
shipping artifact.

**Confirmed vs. unknown.** The teaser is official (OpenAI's own video,
reported by The Verge and carried by Techmeme) → `confirmed` /
`verification: confirmed`. But **a teaser is not a product**: spec, price,
and whether it's a one-off dev toy or a "Codex-as-platform" surface (custom
shortcut packs, team profiles) are unknown until July 15.

**Context.** Easy to dismiss as a gimmick — any IDE binds shortcuts for free.
The more interesting read is positioning: OpenAI signaling that **coding
agents are graduating to first-class dev tools with dedicated hardware
surfaces**, the same week coding-cost competition intensifies
([[cognition-devin-fusion-2026-06]], [[meituan-longcat-2-2026-06]]).

**Transition triggers:**
- The July 15 reveal (spec, price, platform scope) → UPDATE; `status:
  released` once it ships.
- The reveal slipping or being cancelled → UPDATE.
- ≥4 weeks past launch settled into normal coverage → `closed:
  released-and-aged`.

**Dedup note:** further Codex-hardware signal UPDATES this ticket; Codex
software-platform signal stays on [[openai-codex-platform-2026-05]].
