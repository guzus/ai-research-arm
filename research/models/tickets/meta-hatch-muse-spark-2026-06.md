---
slug: meta-hatch-muse-spark-2026-06
title: Meta "Hatch" consumer AI agent + Muse Spark model — reported up to $199.99/mo tier
company: Meta
model: Muse Spark
status: in-testing
status_note: |
  **Muse Spark corroborated as a real Meta model in private testing.** WSJ
  reporting (relayed 2026-06-05) says Meta has repeatedly delayed the
  **Muse Spark developer API** — no firm public date as of 2026-06-02,
  ~2 months past Alexandr Wang's early-April "soon"; a Meta spokesperson
  says it is being tested with select partners and is still expected
  "later this month." Muse Spark is described as Meta's debut proprietary,
  closed-source foundation model from Wang's Superintelligence Labs (TBD
  Lab), already used internally to power WhatsApp/Instagram business
  agents (model itself "done"; the API is the bottleneck). This adds a
  second outlet (WSJ) beyond The Information, so the Muse Spark model
  advances to in-testing / partial. The "Hatch" consumer-agent angle and
  the up-to-$199.99/mo pricing remain single-source (The Information) and
  unconfirmed.

  **2026-07-03:** Alexandr Wang confirmed (own tweet) a "next Muse Spark
  update" is coming soon with big coding/agentic gains; Business Insider
  (secondary) names it "Watermelon" and claims GPT-5.5-parity on internal
  benchmarks with ~10x Muse Spark's training compute — unconfirmed by Meta.
expected: "Muse Spark developer API expected 'later this month' (late June 2026, repeatedly slipped); Hatch launch + up-to-$199.99/mo pricing still TBD/unconfirmed. 2026-07-03: next Muse Spark update ('Watermelon' per BI) coming soon per Wang; GPT-5.5-parity claim unconfirmed"
labels:
  - consumer-agent
  - pricing
  - rumor
  - muse-spark
verification: partial
sources:
  - "@theinformation"
  - https://x.com/JGidel4/status/2062360036190376378
  - "@WSJ"
  - https://the-decoder.com/metas-hatch-ai-agent-could-cost-up-to-200-a-month-and-marks-its-first-paid-ai-product/
  - "@alexandr_wang"
  - "@kimmonismus"
created_at: 2026-06-04
updated_at: 2026-07-03
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-04
    change: "Created — The Information (relayed @JGidel4 02:25 UTC) reports Meta weighing up to $199.99/mo for 'Hatch', a consumer AI-agent (consumer OpenClaw) that builds tools/automations from prompts, with a 'Hatch Plus' premium tier; reportedly developed with Claude but expected to run on Meta's own Muse Spark model at launch. Single-source, no Meta primary → rumored / unverified"
  - ts: 2026-06-05
    change: "Status rumored → in-testing, verification unverified → partial. WSJ reporting (relayed via aggregators 2026-06-05, citing a 2026-06-02 status) corroborates **Muse Spark** as Meta's debut proprietary closed-source foundation model (Superintelligence Labs / TBD Lab, led by Alexandr Wang), already in internal production for WhatsApp/Instagram business agents — the model is 'done', but its **developer API has been repeatedly delayed** (~2 months past Wang's early-April 'soon'). A Meta spokesperson says the API is in testing with select partners and is still expected 'later this month.' Real artifact in partner testing → in-testing; second outlet (WSJ) beyond The Information → partial. The Hatch consumer-agent product and up-to-$199.99/mo pricing remain single-source (The Information) and unconfirmed"
  - ts: 2026-06-07
    change: "The Decoder (2026-06-06) published a full writeup framing **Hatch** as **Meta's first paid AI product** at **up to $200/mo**: users describe what they need in plain language and Hatch builds working tools, schedules appointments, or sends emails. Second independent outlet on the Hatch consumer-agent angle (beyond The Information), reinforcing the pricing band; still no Meta primary on a launch date and the Muse Spark backend is unconfirmed. Status stays in-testing / partial"
  - ts: 2026-07-03
    change: "Next Muse Spark update confirmed coming, codename + benchmark claim still secondary. Meta Superintelligence Labs chief Alexandr Wang tweeted (01:01 UTC Jul 3, primary, 2,116 likes): 'Our next Muse Spark update is coming soon. Big improvements in coding and agentic capabilities.' Separately, Business Insider reporting (relayed by @kimmonismus) names the update 'Watermelon,' claims it already matches GPT-5.5 on internal benchmarks, and says it trains with ~10x the compute of Muse Spark (internal codename Avocado) — this specific codename/benchmark claim is BI-secondary, not in Wang's own tweet, and not independently verified. A real primary confirms an update is coming; the Watermelon specifics stay unconfirmed. Status stays in-testing; verification stays partial."
---

**The Information** (relayed on 2026-06-04, 02:25 UTC) reports that Meta is
weighing pricing of **up to $199.99/mo** for **"Hatch,"** a consumer
AI-agent product — described as a consumer version of **OpenClaw** that
builds tools and automations from plain-language prompts — with a premium
**"Hatch Plus"** tier above it.

The model angle is the reason this is tracked: Hatch was reportedly **built
using Claude during development**, but is **expected to run on Meta's own
"Muse Spark" model at launch**. If accurate, Muse Spark would be the
production model behind Meta's consumer-agent push, and the Claude-in-dev /
own-model-at-launch pattern echoes the broader "own your intelligence"
vertical-integration move Microsoft made with its MAI family (see
[microsoft-build-2026-models](./microsoft-build-2026-models.md)).

**Why verification is `unverified`:** this is a single outlet's reporting
(The Information) carried via a dev-circuit relay, with no Meta primary,
no confirmed launch date, and pricing still "weighed," not set. The
$199.99/mo figure and the Muse Spark backend both need a Meta primary or
independent corroboration.

**Transition triggers:**
- A Meta primary or independent corroboration of Hatch / Muse Spark →
  UPDATE, advance status (`in-testing`/`confirmed`) and verification.
- Confirmed launch with public availability → `released`.
- 15+ daily cycles with no fresh corroboration → `closed:
  stale-rumor-unverified`.

**Dedup note:** new signal about Hatch, Hatch Plus pricing, or the Muse
Spark model UPDATES this ticket. A separate Meta model release (other than
Muse Spark) gets its own ticket.
