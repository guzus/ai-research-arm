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
  **2026-09-16 — THE AGENT LEG FINALLY SHIPPED, and the pricing question this
  ticket has carried since June is answered.** The invite-gated alpha recorded
  on 2026-09-07/14 is gone: the window is saturated with **ordinary users
  describing completed real-world tasks**, which is a distribution signal no
  closed alpha produces. @alexandr_wang: "muse saved people **$9,649.71 across
  100 different stories**… we are working hard to expand access and get it
  everywhere!" Firsthand accounts from unaffiliated accounts include an agent
  that **navigated an Xfinity phone tree to a human, hit an SMS verification
  it could not read, and patched the user in live** for $85.30/mo locked five
  years (@raunaqbn); one that found an unrecognized Adobe subscription billing
  a stranger's account and that **Chase had not flagged** (@Trace_Cohen); and
  ordinary "it just works" reactions from previously skeptical developers
  (@_coenen, @ryanmcadams). Also in-window: **MUSEBOOK** teased, a **Muse Code
  contributor-tier limit increase with a usage reset**, and Wang crediting
  **Nat Friedman** with assembling and running the team.

  **Pricing answered — and it is not $199.99.** A daily AI news digest reports
  **Meta One**, bundling app extras plus more AI image and video generation at
  **$7.99/mo, $19.99 for Premium**, limits undisclosed (@FadyEid, sourced to
  TechCrunch). If that is the monetization surface, the up-to-$199.99/mo
  Hatch tier this ticket has carried since June — outlet-sourced as a *ceiling*
  on 2026-08-26 — is nowhere near where Meta actually landed. Third-party
  relay of a paywalled outlet, so it is recorded, not adopted as final
  pricing; but it is the first consumer price actually attached to the
  product.

  **Muse Spark 1.3 capability claim, and the independent counterweight, in the
  same window.** Wang: "muse spark 1.3 is the **best frontier model at NOT
  cheating / reward hacking**." That is a first-party eval claim with no
  published methodology. Dan Hendrycks released **CheatBench**, a reward-gaming
  evaluation spanning math, coding, knowledge work and visual tasks, the same
  day, reporting that "frontier agents still cheat frequently" — an
  independent instrument for exactly this claim, from a neutral party, with no
  captured per-model row for Muse Spark 1.3. Treat Wang's claim as unverified
  until a CheatBench row exists.

  **Watermelon gets a venue and an institutional source.** Citi, reiterating
  Buy and a $800 PT on META ahead of **Meta Connect, Sept 23-24**, expects
  updates on Muse — noting **Muse app downloads have exceeded Instagram and
  Facebook on several days** — and flags "a potential launch of Meta's next
  foundation model, internally codenamed **Watermelon**" (@wallstengine). This
  is the third independent carry of the Watermelon codename on this ticket
  (Business Insider 2026-07-03, an aggregator 2026-08-26, Citi now) and the
  first with a **named launch venue and date window**. It is still sell-side
  expectation, not a Meta statement, so `model:` is unchanged. **If Watermelon
  launches as a named artifact at Connect, it gets its own ticket** — a
  next-generation foundation model is a distinct shipping artifact from the
  Muse Spark 1.x line.

expected: "BOTH LEGS SHIPPED. Muse Spark 1.3 / 1.3 max released (Muse Code + Meta Model API); the consumer Muse agent is out of closed alpha and in broad public use, with Meta One reported at $7.99/$19.99 as the consumer price. Still pending: Muse Spark open weights and the 'bigger models' teased at launch; Watermelon, the next foundation model, with Meta Connect Sept 23-24 as the venue in frame (sell-side expectation, not a Meta statement); and a CheatBench row for the reward-hacking claim."
labels:
  - consumer-agent
  - pricing
  - muse-spark
  - released
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
  - https://x.com/alexandr_wang/status/2099337296487333978
  - https://x.com/alexandr_wang/status/2100026470089499010
  - https://x.com/alexandr_wang/status/2099984011791839542
  - https://x.com/alexandr_wang/status/2100087304803295715
  - https://x.com/hendrycks/status/2099901663062679853
  - https://x.com/wallstengine/status/2100189982799315397
  - https://x.com/FadyEid/status/2100184052338667874
  - "@raunaqbn"
  - "@Trace_Cohen"
  - "@_coenen"
created_at: 2026-06-04
updated_at: 2026-09-16
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
  - ts: 2026-09-14
    change: "Meta states the model line was purpose-built for the agent, and the agent is still gated. @alexandr_wang (2026-09-14 03:19 UTC): 'something people may have missed: we have been building our models (muse spark 1 through 1.3) specifically to be exceptional for muse over many months. in each of our releases, we made big gains on agentic and multimodal capability.' That is a first-party statement of model/product co-design and is the clearest account yet of why the Spark line looks the way it does. Also from Wang (2026-09-13): 'muse code + muse spark 1.3 max is really good at real-world software engineering', and on the release gate — 'we took security extremely seriously in building muse. the thing that took the longest before we felt comfortable releasing was security and safety', which corroborates from the company side The Information's earlier reporting that Hatch's unauthorized-action problems delayed launch. AGENT STILL NOT OPEN: @steipete (2026-09-13 00:28 UTC) 'Anyone got an invite code for Meta's Muse?' — invite-gated as of this window, consistent with the closed/limited alpha recorded 2026-09-07. Third-party capability note: @giffmana reports it 'has gotten pretty good at interleaving an image gen into the answer unprompted'. Sell-side reaction recorded as market context, not as evidence: JPMorgan upgraded META to Overweight, PT $640 -> $820, on Muse, the Model API and AI-agent monetization; Goldman Sachs reiterated Buy on the agent launch. Status stays released for the model line and the agent leg still does not advance — unchanged from 2026-09-07."
  - ts: 2026-09-16
    change: "THE AGENT LEG SHIPPED — the last unresolved half of this ticket closes. Status stays released (the model line was already there); what changes is that the consumer agent is no longer invite-gated. EVIDENCE IS DISTRIBUTION-SHAPED, not announcement-shaped, which is the point: the window is full of unaffiliated ordinary users describing completed real-world tasks, something a closed alpha cannot produce. @alexandr_wang (2026-09-15 20:58 UTC): 'muse saved people $9,649.71 across 100 different stories… we are working hard to expand access and get it everywhere!' Firsthand third-party accounts: @raunaqbn had the agent navigate an Xfinity phone tree to a human, hit an SMS verification it could not read, and patch him in live, locking $85.30/mo for five years (~$5,118); @Trace_Cohen connected it to Chase via Plaid and it surfaced a recurring Adobe charge billing a stranger's account that Chase had never flagged; @_coenen and @ryanmcadams, both previously skeptical, posted 'fast easy just works' reactions. Also in-window: MUSEBOOK teased, a Muse Code contributor-tier limit increase with a usage reset for all subs, and Wang crediting Nat Friedman with assembling and running the team. PRICING ANSWERED, and not at the number this ticket has carried since June: a daily AI digest sourced to TechCrunch reports Meta One bundling app extras plus more AI image and video at $7.99/mo and $19.99 Premium, limits undisclosed (@FadyEid 2026-09-16). If that is the monetization surface, the up-to-$199.99/mo Hatch ceiling recorded 2026-08-26 is nowhere near where Meta landed. Third-party relay of a paywalled outlet → recorded, not adopted as final pricing. CAPABILITY CLAIM AND ITS COUNTERWEIGHT, same window: Wang says 'muse spark 1.3 is the best frontier model at NOT cheating / reward hacking' — first-party, no published methodology; @hendrycks released CheatBench the same day, a neutral reward-gaming evaluation across math, coding, knowledge work and visual tasks, reporting that 'frontier agents still cheat frequently', with no captured per-model row for Muse Spark 1.3. Wang's claim stays UNVERIFIED until a CheatBench row exists. WATERMELON GETS A VENUE AND AN INSTITUTIONAL SOURCE: Citi, reiterating Buy and an $800 PT on META ahead of Meta Connect Sept 23-24, expects Muse updates — noting Muse app downloads have exceeded Instagram and Facebook on several days — and flags 'a potential launch of Meta's next foundation model, internally codenamed Watermelon' (@wallstengine 2026-09-16). Third independent carry of the codename on this ticket (Business Insider 2026-07-03, aggregator 2026-08-26, Citi now) and the first with a named venue and date window, but it is sell-side expectation rather than a Meta statement, so the model: field is unchanged. IF WATERMELON LAUNCHES AS A NAMED ARTIFACT AT CONNECT IT GETS ITS OWN TICKET — a next-generation foundation model is a distinct shipping artifact from the Muse Spark 1.x line. Cross-reference: Wang's 'Meta delayed shipping Muse for several months to focus on safety and security. We didn't call for everyone else to do this before we would' is logged on [[anthropic-pace-the-frontier-2026-09]] as that ticket's first cited held release."
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
