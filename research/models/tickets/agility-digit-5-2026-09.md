---
slug: agility-digit-5-2026-09
title: Agility Robotics introduces Digit 5
company: Agility Robotics
model: Digit 5
status: confirmed
status_note: |
  **Introduced by the company, 2026-09-15 11:09 UTC.** @agilityrobotics:
  "Introducing Digit 5. Agility's next-generation humanoid, engineered for
  cooperatively safe work at scale, allowing it to work in close proximity to
  people without the physical safety barriers required by traditional
  automation." Independently noted the same day by @aleabitoreddit ("$CCXI
  releases their Digit 5 next-generation humanoid").

  **The headline spec is a safety claim, not a capability claim,** and that is
  unusual enough to be the point. "Cooperatively safe" — working alongside
  people without cages — is the constraint that actually gates humanoid
  deployment in warehouses and plants, because the alternative is fencing that
  destroys the labour-substitution economics. Agility is selling the removal
  of the fence.

  **Not stated in-window:** payload, runtime, price, availability date, or any
  customer. No third-party hands-on. A safety architecture claim of this kind
  normally requires certification against an industrial standard, and none is
  named.
expected: "Introduced. Open: payload/runtime specs, price, ship date, named customers, and — most importantly — which functional-safety standard the 'cooperatively safe' claim is certified against."
labels:
  - robotics
  - humanoid
  - industrial
  - safety
verification: confirmed
sources:
  - https://x.com/agilityrobotics/status/2099817779637706755
  - "@aleabitoreddit"
created_at: 2026-09-16
updated_at: 2026-09-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-16
    change: "Created — CONFIRMED. @agilityrobotics introduced Digit 5 on 2026-09-15 11:09 UTC as its next-generation humanoid 'engineered for cooperatively safe work at scale, allowing it to work in close proximity to people without the physical safety barriers required by traditional automation', with product page and full video linked; separately noted by @aleabitoreddit the same day. Company announcement is the primary source → verification confirmed on the introduction. Status confirmed rather than released: no ship date, price, availability or customer was stated. The distinguishing claim is safety architecture, not capability — removing the safety cage is what gates humanoid economics in warehouses, since fencing negates the labour-substitution case. NOT stated and not inferred: payload, runtime, price, date, customers, or any named functional-safety certification, which is the specific thing a 'cooperatively safe' claim would normally rest on. Joins the humanoid line alongside [[figure-helix-02-2026-05]], [[skild-s1-2026-08]], [[unitree-ipo-debut-2026-08]] and [[nvidia-sonic-humanoid-model-2026-09]]."
---

**Digit 5** is Agility's next-generation humanoid, and it is being sold on
**cage-free operation** rather than on dexterity, speed or a model.

**Why that framing is the interesting one.** Every humanoid deployment
economic case runs into the same wall: if the robot needs a fenced cell, it
competes with fixed automation, which is cheaper and better at fixed tasks.
The entire argument for a humanoid is that it works in the space built for
humans, next to humans. "Cooperatively safe work at scale, without the
physical safety barriers" is Agility claiming it has cleared that wall.

**What would substantiate it.** A named functional-safety certification.
Collaborative-robot safety is a certified property in industrial settings, not
a marketing adjective, and nothing in the announcement names a standard, a
body, or a rating. Until one appears, the claim is a design intent.

**What is missing entirely.** Payload, runtime, price, availability, and
customers. Agility has shipped into real logistics sites before, so those
numbers exist; they were simply not in this post.

**Transition triggers:**
- A named safety certification → UPDATE, this is the load-bearing one.
- Specs, price, or availability → UPDATE; a shipping date to customers →
  advance to `released`.
- A named deployment or customer → UPDATE.
- ≥4 weeks past general availability → `closed: released-and-aged`.

**Dedup note:** other humanoid platforms stay on their own tickets
([[figure-helix-02-2026-05]], [[skild-s1-2026-08]],
[[unitree-ipo-debut-2026-08]]); humanoid *foundation models* stay on
[[nvidia-sonic-humanoid-model-2026-09]] and
[[odyssey-3-world-model-2026-09]].
