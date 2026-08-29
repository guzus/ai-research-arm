---
slug: huggingface-microduck-robot-2026-08
title: Hugging Face / Pollen Robotics Microduck — $399 open-source RL biped
company: Hugging Face / Pollen Robotics
model: Microduck
status: released
status_note: |
  **Announced and orderable 2026-08-27.** @ClementDelangue (Hugging Face
  CEO): "**BIG ANNOUNCEMENT FROM HUGGING FACE TODAY: We're unveiling
  Microduck** 🐥🤖 It's a tiny **$399 open-source robot** you can teach new
  tricks with **reinforcement learning**. It can walk, pick things up, get
  back up when it falls, and even roller-skate. Welcome to the era of
  open-source affordable robots to **democratize physical AI and world
  models**."

  **The spec, from @Thom_Wolf (HF co-founder/CSO):** "the **first truly
  accessible RL robot**… A **25 cm tiny open-source biped with 15
  actuators** and packed with sensors (**camera, speaker, LiDAR, NFC,
  bluetooth, wifi**) that **you train yourself with reinforcement
  learning**. It's also **playable out of the box with more than half a
  dozen… pre-trained policies** to have it walk, sit, crouch,
  roller-skate, **pick up objects with its articulated beak**, and
  **recover on its own**. And all for **less than $400**." Built by
  **Pollen Robotics**, the robotics team Hugging Face acquired —
  @antoinepirrone: "our newest robot at **Pollen Robotics x
  HuggingFace**."

  **It is a real product, not a demo.** The announcement links a simulator
  and an order page, third-party coverage is same-day (**Axios**: "Hugging
  Face debuts Microduck, an adorable $399 waddling robot"), and @Thom_Wolf
  posted working extension experiments within hours — "we vibe-coded an
  **image detector integration to detect and follow a laser pointer**."

  **Why it is a model-lane ticket and not a gadget.** The pitch is
  explicitly **world models and physical AI**, and the price is the
  argument: a $399 biped with LiDAR that you train yourself puts RL on
  physical hardware inside a hobbyist budget, which is the same
  distribution move Hugging Face made for weights. Read against
  [[skild-s1-2026-08]], [[figure-helix-02-2026-05]] and
  [[google-gemini-robotics-2-2026-07]] — those are capability tickets;
  this is an **access** ticket. @AndrewCurran_'s framing: "They beat OpenAI
  and Apple to the adorable droid market."

  **The timing is not incidental and should be read alongside
  [[huggingface-sale-exploration-2026-08]]**: Hugging Face shipped its most
  consumer-facing product ever on the same day The Information reported
  NVIDIA had agreed to buy it for $12.9B. Nothing in-window connects the
  two, and no HF account addressed the deal — @mervenoyann explicitly
  carved it out of an open AMA. Recorded as adjacency, not causation.

  Verification `confirmed`: announced by the CEO, the CSO, the Pollen
  Robotics lead and the @huggingface institutional account, with same-day
  named-outlet coverage. **Not** established: any performance claim beyond
  the vendor's own demos, shipping timelines, or how well the RL training
  loop works for a non-expert — no independent hands-on review existed
  in-window.
expected: "Announced 2026-08-27 with a simulator and an order page live: 25cm open-source biped, 15 actuators, camera/speaker/LiDAR/NFC/bluetooth/wifi, $399, ships with 6+ pre-trained policies (walk, sit, crouch, roller-skate, beak grasp, self-recovery) and is trainable by the user with RL. Built by Pollen Robotics under Hugging Face. Pending: ship dates and units, the licence and repo for the hardware and policies, any independent hands-on review, and how usable the RL loop actually is for a non-expert — no third-party evaluation existed in-window"
labels:
  - hugging-face
  - robotics
  - open-source
  - reinforcement-learning
  - hardware
  - released
verification: confirmed
sources:
  - "@ClementDelangue"
  - "@Thom_Wolf"
  - https://x.com/Thom_Wolf/status/2092952358359552197
  - "@huggingface"
  - "@antoinepirrone"
  - "@AndrewCurran_"
  - https://x.com/AndrewCurran_/status/2092959983369654780
  - "@kimmonismus"
created_at: 2026-08-27
updated_at: 2026-08-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-27
    change: "Created — Hugging Face and Pollen Robotics unveiled Microduck on 2026-08-27, a $399 open-source RL biped, announced by @ClementDelangue ('BIG ANNOUNCEMENT FROM HUGGING FACE TODAY... a tiny $399 open-source robot you can teach new tricks with reinforcement learning... Welcome to the era of open-source affordable robots to democratize physical AI and world models'), @Thom_Wolf ('the first truly accessible RL robot - a 25 cm tiny open-source biped with 15 actuators and packed with sensors (camera, speaker, LiDAR, NFC, bluetooth, wifi) that you train yourself with reinforcement learning... playable out of the box with more than half a dozen pre-trained policies... walk, sit, crouch, roller-skate, pick up objects with its articulated beak, and recover on its own'), @antoinepirrone of Pollen Robotics, and the @huggingface institutional account. Status released rather than confirmed because a simulator and an order page are live, not just an announcement; Axios covered it the same day, and @Thom_Wolf posted a working user-built extension (a vibe-coded image detector that makes it follow a laser pointer) within hours. Verification confirmed on four first-party accounts plus named-outlet coverage. NOT established: any performance claim beyond vendor demos, ship dates, or how usable the RL training loop is for a non-expert — no independent hands-on review in-window. Earns a model-lane ticket because the pitch is explicitly world models and physical AI and the argument is price: this is an ACCESS ticket where [[skild-s1-2026-08]], [[figure-helix-02-2026-05]] and [[google-gemini-robotics-2-2026-07]] are capability tickets. Adjacency recorded without causation: it shipped the same day The Information reported NVIDIA had agreed to acquire Hugging Face ([[huggingface-sale-exploration-2026-08]]), and no HF account addressed the deal."
---

**Microduck** is a 25cm, 15-actuator open-source biped from Hugging Face's
Pollen Robotics team, at **$399**, that ships with pre-trained policies and
is meant to be **retrained by its owner with reinforcement learning**.

**The price is the claim.** Everything else about the robot is modest —
it walks, crouches, roller-skates, grasps with its beak, and gets up when
it falls. What is not modest is putting a LiDAR-equipped bipedal RL
platform under $400. @Thom_Wolf's own comparison is the honest one: it
"probably wouldn't have won many gold medals at the Beijing Robot
Olympics, but OMG, it is cute (**and open-source and cheap**)."

**This is the Hugging Face playbook applied to hardware.** The company's
role in this ticket set has always been distribution — it is the default
host for the open weights that [[alibaba-qwen-4-architecture-2026-08]],
[[zhipu-glm-5-3-2026-08]] and [[thinking-machines-inkling-small-2026-07]]
ship through. Microduck extends that to embodiment: the constraint on
physical-AI research has been that the hardware costs more than a
graduate stipend, and a $399 platform with published policies changes who
can run the experiment, not what the experiment can prove.

**What would make this more than a nice gesture** is evidence that the RL
loop works for people who are not roboticists. The announcement claims it;
nobody outside Hugging Face has tested it yet. Until someone does, treat
"you train it yourself with RL" as a product promise.

**Transition triggers:**
- Independent hands-on review, or a third party successfully training a
  new policy → UPDATE.
- Hardware licence, repo and policy weights published → UPDATE.
- Ship dates, units sold, or a supply constraint → UPDATE.
- ≥4 weeks past release, settled into normal coverage →
  `closed: released-and-aged`.

**Dedup note:** the NVIDIA acquisition of Hugging Face stays on
[[huggingface-sale-exploration-2026-08]]. Humanoid and generalist-robot
capability stays on [[skild-s1-2026-08]],
[[google-gemini-robotics-2-2026-07]] and [[figure-helix-02-2026-05]].
Further Microduck signal UPDATES this ticket.
