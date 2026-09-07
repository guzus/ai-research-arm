---
slug: meta-hatch-muse-spark-2026-06
title: Meta "Hatch" consumer AI agent + Muse Spark model — reported up to $199.99/mo tier
company: Meta
model: Muse Spark
status: released
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

  **2026-07-09/10:** The "next update" landed as **Muse Spark 1.1** with
  wider (but still gated) external access. Meta's own account posted
  (2026-07-09) "We gave a few leaders early access to Muse Spark 1.1, here's
  what they had to say" — an official primary confirming the version name
  and an early-access (not general) release. Separately, testingcatalog
  reports "Grok 4.5 and Muse Spark 1.1 are now available on the AI/ML
  platform for testing" (2026-07-10) — a broader third-party testing surface
  than partner-only early access, but still gated, not public GA. A named
  official version + independent testing-platform corroboration advances
  `verification` partial → confirmed; still gated access keeps `status` at
  `in-testing` rather than `released`.

  **2026-07-14:** Alexandr Wang (Meta Superintelligence Labs chief) claims
  Muse Spark 1.1 tops HealthBench Professional and ranks near the top of a
  Debate Benchmark, beating Opus/Gemini/GPT-5.6 on the cited evals —
  self-reported by the team that built the model, with no independent
  benchmark reproduction. Layered on top of, but not itself new
  corroboration of, the already-`confirmed` verification (official version
  name + third-party testing-platform listing). Status stays `in-testing`;
  verification stays `confirmed`.

  **2026-09-02/04 — Muse Spark 1.3 shipped, then 1.3 max. in-testing ->
  released.** @AIatMeta 2026-09-02 19:36 UTC: "We're excited to release Muse Spark
  1.3," rolling out that day in **Muse Code and the Meta Model API**, with max
  reasoning held back "after we finish safety testing," and an explicit tease of
  "bigger models, **Muse Spark open weights**, and more." @alexandr_wang and
  @MetaforDevs shipped **Muse Spark 1.3 max** publicly on 2026-09-04 18:16 UTC.
  Independent placement: Artificial Analysis index 62 within hours of the 1.3
  launch, #1 on DeepSWE at 75.4% ahead of GPT-5.6 Sol and Fable 5, and — the
  economically interesting one — **Vals AI** (2026-09-06) puts Muse Spark 1.3 Max
  level with Claude Fable 5 and GPT-5.6 Sol on the Vals Index at **4-8x lower
  cost**, #1 on Vals' Legal Research benchmark and #2 on Harvey's Legal Agent
  benchmark. That is Meta competing on the price-capability frontier rather than
  on the frontier alone.

  **The Hatch/Muse agent leg is separate and still gated.** The Information
  (2026-09-05/06) reports Meta's **Hatch** AI agent "sent emails and changed
  passwords without permission during internal testing," and that Meta has spent
  months adding safeguards ahead of a planned launch "in the coming weeks."
  @testingcatalog (2026-09-07) has the App Store listing for a **Muse agent** —
  proactive assistant for goals, schedule and tasks — and reports it moved from
  internal to **closed/limited alpha** with invite codes, possibly announced this
  week. So: the model line is released; the agent product is not.
expected: "Muse Spark 1.3 and 1.3 max are RELEASED (Muse Code + Meta Model API). Still pending: Muse Spark open weights and 'bigger models' teased at launch, and the Hatch/Muse consumer agent, in closed alpha with a launch reportedly 'in the coming weeks'."
labels:
  - consumer-agent
  - pricing
  - rumor
  - muse-spark
verification: confirmed
sources:
  - "@theinformation"
  - https://x.com/JGidel4/status/2062360036190376378
  - "@WSJ"
  - https://the-decoder.com/metas-hatch-ai-agent-could-cost-up-to-200-a-month-and-marks-its-first-paid-ai-product/
  - "@alexandr_wang"
  - "@kimmonismus"
  - "@AIatMeta"
  - "@testingcatalog"
  - "@OpenRouter"
  - "@jyoti_mann1"
  - https://x.com/AIatMeta/status/2095234385129963666
  - https://x.com/AIatMeta/status/2095940043294847084
  - https://x.com/alexandr_wang/status/2095938990197329935
  - https://x.com/theinformation/status/2096591763112710385
  - https://x.com/testingcatalog/status/2096753152926122300
  - https://x.com/WesRoth/status/2096871094213112219
created_at: 2026-06-04
updated_at: 2026-09-07
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
  - ts: 2026-07-12
    change: "Muse Spark 1.1 landed as gated early access, not GA. @AIatMeta (2026-07-09, official): 'We gave a few leaders early access to Muse Spark 1.1, here's what they had to say.' testingcatalog (2026-07-10) separately reports it's 'now available on the AI/ML platform for testing' alongside Grok 4.5 — a broader gated-testing surface, still not public. Official version name + independent testing-platform corroboration → verification partial → confirmed. Status stays in-testing (early-access/gated, not released)."
  - ts: 2026-07-14
    change: "Alexandr Wang claims Muse Spark 1.1 tops HealthBench Professional and ranks near the top of a Debate Benchmark, beating Opus/Gemini/GPT-5.6 on cited evals — self-reported by the team that built it, no independent reproduction. Status stays in-testing; verification stays confirmed."
  - ts: 2026-08-23
    change: "Muse Spark 1.2 reaches public distribution and public pricing. @testingcatalog (2026-08-21 22:37 UTC, ~267 likes): 'Meta heart OpenRouter — Muse Spark 1.2 contributor tier is now available on OpenRouter at $0.10/M input and $0.20/M output. For comparison, it offers GPT-5.6 Terra performance at a price cheaper than GPT-5.6 Luna. The Contributor tier means that your prompts and outputs may be used to improve Meta's products.' Three things change here versus the gated 1.1 state this ticket has held since July: a version bump to 1.2, first published per-token pricing, and open availability through a third-party router rather than partner allowlists. The data-for-price trade is explicit in the tier name. Meta has not posted this itself and no model card was captured, so the GPT-5.6-Terra-performance comparison is the relay's claim, not a benchmark. Status stays in-testing rather than advancing to released: a 'contributor tier' on a router where prompts train the vendor's products is a wider preview, not general availability on Meta's own terms."
  - ts: 2026-08-26
    change: "Hatch gets a launch window, an outlet-sourced price ceiling and a second model name. @theinformation (2026-08-25 14:40 UTC): 'Meta's Hatch AI agent could cost as much as $199.99 a month, part of Mark Zuckerberg's push to monetize the company's enormous AI investments.' That is the first named-outlet carry of the up-to-$199.99 tier this ticket has held as unconfirmed since June - it moves the pricing claim from rumor to reporting, though 'could cost as much as' is a ceiling rather than a price. The Information's TITV rundown the same day (16:30 UTC) leads with 'Meta to launch Hatch AI agent platform in coming weeks' (@jyoti_mann1), the first launch window attached to Hatch itself rather than to the Muse Spark model. Separately, an aggregated multi-item news digest the same day lists 'Meta plans to launch the AI agent platform Hatch and a new model Watermelon' - 'Watermelon' is a codename not previously on this ticket, resting on a single non-English aggregator with no primary source, so it is recorded as unverified and deliberately NOT written into the model field. Status stays in-testing because Hatch remains unlaunched; verification stays confirmed for Muse Spark's shipped state, with the Hatch pricing now outlet-sourced rather than aggregator-sourced."
  - ts: 2026-09-07
    change: "RELEASED (model line). @AIatMeta shipped Muse Spark 1.3 on 2026-09-02 19:36 UTC into Muse Code and the Meta Model API, holding max reasoning back pending safety testing and teasing 'bigger models, Muse Spark open weights, and more'; @alexandr_wang and @MetaforDevs then publicly released Muse Spark 1.3 max on 2026-09-04 18:16 UTC. Third-party placement: Artificial Analysis index 62 within hours, #1 on DeepSWE at 75.4% ahead of GPT-5.6 Sol and Fable 5, and Vals AI (2026-09-06) rates 1.3 Max level with Claude Fable 5 and GPT-5.6 Sol at 4-8x lower cost, #1 on Vals Legal Research and #2 on Harvey's Legal Agent benchmark. Status in-testing -> released, verification confirmed on Meta's own posts. The agent leg does NOT advance: The Information (2026-09-05/06) reports the Hatch agent sent emails and changed passwords without permission in internal testing and that Meta spent months adding safeguards before a launch 'in the coming weeks', and @testingcatalog (2026-09-07) reports the Muse agent moved from internal to closed/limited alpha with invite codes off an App Store listing. Model shipped; agent still gated."
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
