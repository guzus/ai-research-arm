---
slug: google-gemini-robotics-2-2026-07
title: Google DeepMind launches Gemini Robotics 2 and Gemini Robotics ER 2
company: Google / DeepMind
model: Gemini Robotics 2 / Gemini Robotics ER 2
status: confirmed
status_note: |
  @GoogleDeepMind launched **Gemini Robotics 2**: "one brain for any
  robot" — whole-body humanoid control, advanced dexterity, and
  multi-robot teamwork. A companion embodied-reasoning model, **Gemini
  Robotics ER 2** (`gemini-robotics-er-2-preview`), built on Gemini 3.5
  Flash, claims 91.3% moment-finding accuracy at 4x faster execution
  speed per @_philschmid. Google also introduced the **"ASIMOV-Agentic"**
  safety benchmark alongside the launch. Corroborated by 4+ independent
  official Google accounts (@GoogleDeepMind, @GoogleAI, @GoogleAIStudio,
  @_philschmid, @OfficialLoganK) with concrete model IDs and benchmark
  figures. `status: confirmed` rather than `released`: robotics/embodied
  models of this class typically ship via controlled partner/developer
  access (the "-preview" suffix on the ER 2 model ID is consistent with
  gated rollout), not unrestricted public availability — watch for a
  broader-access announcement to advance to `released`.
expected: "Watching for: broader developer/API access beyond preview, named robot-platform partners, and independent benchmark reproduction of the 91.3% moment-finding / 4x speed claims"
labels:
  - google
  - deepmind
  - robotics
  - embodied-ai
verification: confirmed
sources:
  - "@GoogleDeepMind"
  - "@GoogleAI"
  - "@GoogleAIStudio"
  - "@_philschmid"
  - "@OfficialLoganK"
created_at: 2026-07-31
updated_at: 2026-07-31
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-31
    change: "Created — Google DeepMind launched Gemini Robotics 2 (whole-body humanoid control, dexterity, multi-robot teamwork) and a companion embodied-reasoning model Gemini Robotics ER 2 (gemini-robotics-er-2-preview, built on Gemini 3.5 Flash, 91.3% moment-finding accuracy at 4x faster execution per @_philschmid), plus a new ASIMOV-Agentic safety benchmark. Corroborated by 4+ official Google accounts with concrete model IDs and figures → status confirmed, verification confirmed. Held at confirmed rather than released pending clarity on public/developer access breadth (ER 2 model ID carries a '-preview' suffix)."
---

**Google DeepMind** launched **Gemini Robotics 2**, pitched as "one brain
for any robot": full-body intelligence for humanoids, advanced dexterity,
and multi-robot collaboration. Alongside it, Google introduced a companion
**embodied-reasoning model, Gemini Robotics ER 2** — model ID
`gemini-robotics-er-2-preview`, built on **Gemini 3.5 Flash**
([[gemini-3-5-flash-cyber-2026-07|see related Gemini 3.5 Flash line]]) —
which @_philschmid reports at **91.3% moment-finding accuracy at 4x
faster execution speed**. Google also introduced **"ASIMOV-Agentic,"** a
new safety benchmark for embodied/agentic robotics systems.

**Why `confirmed` not `released`.** The launch is corroborated across
four-plus official Google accounts with concrete model IDs and benchmark
figures — clearly a real, named product line, not a rumor. But the `-2
preview` suffix on the ER 2 model ID and the general pattern for
robotics-class models (gated partner/developer access rather than
unrestricted public availability) argue against `released` until a
broader-access announcement surfaces.

**Why tracked.** This is Google's most significant robotics/embodied-AI
model announcement in this ticket set — no prior Gemini Robotics ticket
existed before this launch.

**Transition triggers:**
- Broader developer/API access, pricing, or a named robot-hardware partner
  → UPDATE, consider advancing to `released`.
- Independent (non-Google) benchmark reproduction of the ER 2 figures →
  UPDATE.
- A successor generation → new ticket; do not reopen this one.

**Dedup note:** further Gemini Robotics 2 / ER 2 signal (access, partners,
benchmarks) UPDATES this ticket.
