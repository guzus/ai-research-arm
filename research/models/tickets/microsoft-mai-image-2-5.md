---
slug: microsoft-mai-image-2-5
title: Microsoft MAI-Image-2.5 (Preview) — #3 on Text-to-Image Arena
company: Microsoft AI
model: MAI-Image-2.5
status: released
status_note: |
  Mustafa Suleyman announced MAI-Image-2.5 (Preview) on 2026-05-26 18:48 UTC,
  the same day LMArena listed it at **#3 on the Text-to-Image Arena** with a
  score of **1,254 (+72 points vs prior MAI image model)**. Live on
  Copilot.com today; coming to the MAI Playground and Microsoft Foundry
  "next week". Framed as the typography / layout / professional-creative
  upgrade in the MAI-Image line (sharper text, brand visuals, deliberate
  scenes). Lands one week before Microsoft Build 2026 — Suleyman: "Build is
  just a week away, there's much more to come." Successor to MAI-Image-2 /
  MAI-Image-2-Efficient (Apr 14–15, 2026).
expected: "Microsoft Foundry + MAI Playground rollout week of 2026-06-01"
labels:
  - text-to-image
  - microsoft-ai
  - preview
  - released
verification: confirmed
sources:
  - "@mustafasuleyman"
  - "@MicrosoftAI"
  - "@arena"
  - "@satyanadella"
  - "@NeowinFeed"
created_at: 2026-05-27
updated_at: 2026-05-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-27
    change: "Created — Mustafa Suleyman announced MAI-Image-2.5 (Preview) on 2026-05-26 18:48 UTC; debuts at #3 on the @arena Text-to-Image leaderboard with score 1,254 (+72 pts); live now on Copilot.com, rolling out to MAI Playground + Microsoft Foundry next week. Satya Nadella RT'd the announcement at 21:05 UTC. Pitched as typography / layout / brand-visual upgrade in the MAI-Image line; Microsoft Build 2026 a week out"
---

**MAI-Image-2.5 (Preview)** is Microsoft AI's new text-to-image model,
announced by Mustafa Suleyman on **2026-05-26 18:48 UTC** and landing the
same day on the LMArena leaderboard. Per the Arena post, the model debuts
at **#3 on the Text-to-Image Arena with a score of 1,254 — a +72-point
jump over Microsoft's prior MAI image model**, putting it squarely on the
podium alongside the leading frontier image labs.

Suleyman's pitch is targeted at **professional creative work**: "script
on a poster, labels on packaging, the way light falls across a scene."
The model is positioned to fix the long-standing weak spots of
text-to-image systems — **sharper text rendering, layouts that hold
together, deliberately composed scenes, brand visuals with more polish**.
Sample images released alongside the announcement lean heavily on
typography and packaging mockups.

**Distribution:**
- **Live today** on [Copilot.com](https://copilot.com) (anyone with
  Copilot access can try it).
- **Next week**: rolling out to the **MAI Playground** and **Microsoft
  Foundry** (the enterprise-facing model surface that hosts the rest of
  the MAI series and Cohere Command A+).
- Status is `released` rather than `in-testing` because anyone with
  Copilot can use it today, even though the "Preview" label remains in
  the model name.

**Context within the MAI-Image line:**
- 2026-04-14: MAI-Image-2-Efficient (production workhorse, 22% faster +
  41% cheaper than MAI-Image-2).
- 2026-04-15: MAI-Image-2 (precision tool, highest fidelity).
- **2026-05-26: MAI-Image-2.5 (Preview) — frontier-quality jump, #3 on
  Arena.**

Microsoft's own [Satya Nadella RT'd](https://x.com/satyanadella) the
launch at 21:05 UTC the same day, signalling a primary-source corporate
endorsement and tying the launch to Microsoft Build 2026 ("Build just a
week away"). Independent press coverage (Neowin, 2026-05-27 05:48 UTC)
framed it as Microsoft "finally catching up with the top leaders in the
highly competitive AI image generation space."

**What is unverified:** no published pricing, no model card, no API
specs, no parameter / inference-cost numbers. The +72-point Arena delta
is the only quantitative comparator in the public signal so far. Watch
Microsoft Build 2026 (week of June 1) for the Foundry+Playground GA + a
likely API surface.

**Transition triggers:**
- Foundry / MAI Playground GA → UPDATE with the surface details + API
  availability.
- Pricing, model card, or parameter disclosure at Microsoft Build 2026 →
  UPDATE.
- A successor (MAI-Image-3 / MAI-Image-2.5 GA without "Preview" tag) →
  new ticket and link back here.
- ≥4 weeks past public availability with the launch settled into normal
  coverage → `status: closed` with `closed_reason: released-and-aged`.

**Dedup note:** further MAI-Image-2.5 signal (Foundry GA, pricing,
Arena rank moves, benchmarks, Copilot integration changes) UPDATES this
ticket. Other MAI models (MAI-Voice-1, future MAI-Image-3) get their own
tickets and reference this one.
