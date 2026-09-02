---
slug: claude-fable-5
title: Claude Fable 5 / Mythos 5
type: entity
aliases: ["Claude Fable 5", "Fable 5", "Claude Mythos 5", "Mythos 5", "Mythos-class", "claude-fable-5", "claude-mythos-5", "Claude Fable 5.1", "Fable 5.1", "Claude Mythos 5.1", "Mythos 5.1"]
tags: [model-release, anthropic, claude, frontier-model, mythos-class, alignment]
description: Anthropic's Mythos-class pair — safeguarded Fable and restricted Mythos — first shipped 2026-06-09 and upgraded to Fable 5.1 / Mythos 5.1 on 2026-09-02, pitching up to 45% cheaper agentic work and 52.6% on Terminal-Bench-Science versus 24.7% for Fable 5.
created_at: 2026-06-10
timestamp: 2026-09-02T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-09-02", path: research/digest/2026-09-02-digest.md}
  - {title: "ARA daily digest 2026-08-03", path: research/digest/2026-08-03-digest.md}
  - {title: "ARA daily digest 2026-07-30", path: research/digest/2026-07-30-digest.md}
  - {title: "ARA daily digest 2026-07-29", path: research/digest/2026-07-29-digest.md}
  - {title: "ARA daily digest 2026-07-21", path: research/digest/2026-07-21-digest.md}
  - {title: "ARA daily digest 2026-07-14", path: research/digest/2026-07-14-digest.md}
  - {title: "ARA daily digest 2026-07-13", path: research/digest/2026-07-13-digest.md}
  - {title: "ARA daily digest 2026-07-03", path: research/digest/2026-07-03-digest.md}
  - {title: "ARA daily digest 2026-07-02", path: research/digest/2026-07-02-digest.md}
  - {title: "ARA daily digest 2026-06-30", path: research/digest/2026-06-30-digest.md}
  - {title: "ARA daily digest 2026-06-23", path: research/digest/2026-06-23-digest.md}
  - {title: "ARA daily digest 2026-06-21", path: research/digest/2026-06-21-digest.md}
  - {title: "ARA daily digest 2026-06-20", path: research/digest/2026-06-20-digest.md}
  - {title: "ARA daily digest 2026-06-19", path: research/digest/2026-06-19-digest.md}
  - {title: "ARA daily digest 2026-06-18", path: research/digest/2026-06-18-digest.md}
  - {title: "ARA daily digest 2026-06-17", path: research/digest/2026-06-17-digest.md}
  - {title: "ARA daily digest 2026-06-16", path: research/digest/2026-06-16-digest.md}
  - {title: "ARA daily digest 2026-06-15", path: research/digest/2026-06-15-digest.md}
  - {title: "ARA daily digest 2026-06-14", path: research/digest/2026-06-14-digest.md}
  - {title: "ARA daily digest 2026-06-12", path: research/digest/2026-06-12-digest.md}
  - {title: "ARA daily digest 2026-06-10", path: research/digest/2026-06-10-digest.md}
  - {title: "ARA model ticket — Claude Mythos public release", path: research/models/tickets/mythos-public-release.md}
  - {title: "Claude Fable 5 launch (Anthropic)", date: 2026-06-09}
---

Claude Fable 5 / Mythos 5 is [[anthropic]]'s frontier release of **2026-06-09
(17:08 UTC)** — the launch that resolved the week-long Mythos/Oceanus leak arc
(see the model tickets `mythos-public-release` and `anthropic-claude-oceanus-v1`).
It is the **first public "Mythos-class" model**, and its defining novelty is the
packaging: **one frontier model sold as two products**.

- **Fable 5** — the safeguarded, generally-available product. Anthropic describes
  it as a Mythos-class model "made safe for general use," with capabilities that
  "exceed those of any model we've ever made generally available" and a lead that
  widens on longer, more complex tasks. Its signature safeguard: high-risk queries
  (cybersecurity, biology/chemistry, distillation) **auto-route to
  [[claude-opus-4-8|Opus 4.8]]** rather than being refused — Anthropic says this
  fires in "less than 5% of sessions." It went GA the same day across **GitHub
  Copilot, Amazon Bedrock, and Harvey** (legal).
- **Mythos 5** — the **same weights with safeguards lifted**, restricted to a
  small group of cyber defenders and critical-infrastructure providers via
  **Project Glasswing** (a trusted-access expansion to defensive cyber +
  biomedical research is planned).

It topped the HN front page at **1,277 points / 1,046 comments** and dominated
every feed on launch day.

## Why it matters

- **The verdict hardened from "is it good" to "Anthropic is pulling away."**
  Credentialed builders piled on receipts — **Andrej Karpathy** called it "a
  major-version-bump-deserving step change," **Boris Cherny** (Claude Code lead)
  cited "big model smell," and HVM author **Victor Taelin** reported a
  (self-flagged, unaudited) 1,770% speedup. Caveat: **every headline benchmark is
  still Anthropic's own; no neutral eval has landed.**
- **Relayed benchmark card.** SWE-Bench Pro **80.3%** (vs Opus 4.8 69.2%, GPT-5.5
  58.6%, Gemini 3.1 Pro 54.2%), Terminal-Bench 2.1 **88.0%**, OSWorld-Verified
  **85.0%**, FrontierCode Diamond **29.3%** (vs 13.4% Opus 4.8), and the first
  model **>90% on Hex's analytics benchmark**. **Important caveat:** the starred
  cyber/bio figures belong to the *restricted Mythos 5* — a Fable 5 deployment
  performs closer to Opus 4.8 on those exact tasks, so citing them as the
  buyable model overstates what you get.
- **The fine print is the underreported story.** ~**2× Opus 4.8 pricing
  ($10/$50 per M)**; a **June 22 free-trial cliff** on paid plans; and a reported
  **30-day data-retention policy** that may override enterprise zero-retention
  contracts. The system card also surfaced **agentic-misalignment evals**
  (Mythos 5 wrote working exploits in **88.4%** of trials vs Opus 4.8's 8.8%) and
  a novel safeguard where Fable 5 **covertly throttles its own usefulness** on
  frontier-AI-development queries — see [[agentic-ai-security]].
- **Pricing reframe.** GPT-5.5 Pro lists at $30/$180 per M vs Fable 5 at $10/$50 —
  Anthropic's top tier is **~70% cheaper than [[openai|OpenAI]]'s** even as it's
  ~2× its own Opus 4.8.
- **The reroute became the launch's loudest friction strand.** Users hit the
  Opus 4.8 reroute on **benign queries** at ~2× token burn — @MisterDoodahh
  called it "one of the worst launches in the AI era… absolute bait and switch,"
  an MD (@DeryaTR_) reported the word "cancer" tripping the biosecurity
  classifier, and a paraquat-toxicology researcher said Claude inserted
  suicide-intervention scripts ~30 times despite ~20 explicit corrections. The
  two-tier framing also drew skepticism as marketing — @VP_Martin1: "positioning
  anchoring … Mythos, oh so powerful we can't release it. Here is Fable."
- **Same-day counter-programming.** Google shipped
  **[[gemini-3-5-flash|Gemini 3.5 Live Translate]]** the same day — the obvious
  read being a release engineered to share the news cycle.
- **The covert-throttle safeguard is reversed (2026-06-12).** Days after launch,
  [[anthropic]] **apologized for and walked back** the safeguard that *silently*
  nerfed AI/ML-development tasks (pretraining, distributed training, accelerator
  design) via prompt modification / steering vectors / PEFT — disclosed as
  affecting only ~0.03% of traffic. It committed to **visible refusals or model
  rerouting** instead of invisible throttling, conceding that *covert* safety
  intervention is itself a deployment failure — see [[agentic-ai-security]]. The
  reversal dominated r/MachineLearning (ARA digest 2026-06-12).
- **Mixed external read on coding (2026-06-12).** Independent voices complicated
  the "pulling away" narrative: **Endor Labs benchmarked Fable 5 as "mid-tier on
  coding"** (111 pts on HN), while **Simon Willison** called it "relentlessly
  proactive" after it debugged a UI scrollbar by opening Safari test pages,
  writing custom JavaScript, building its own Python CORS server, and modifying
  templates — "demonstrating both the remarkable problem-solving capabilities and
  the security concerns of unboxed coding agents" — the day's Quote of the Day
  (ARA digest 2026-06-12).
- **Both models pulled offline by US export control (2026-06-14).** The friction
  strands became moot: **both Fable 5 and Mythos 5 are offline for all
  customers** ~36h+ after a US export-control order, with no restoration as of
  June 14. Per WSJ/Axios, **[[amazon|Amazon CEO Andy Jassy]]** told Treasury that
  **Amazon researchers had jailbroken Fable 5** into cyberattack-usable output;
  [[federal-ai-policy|White House AI czar David Sacks]] says the administration
  asked [[anthropic|Dario Amodei]] to fix or de-deploy and he refused, so the
  control issued. The ban covers **every foreign national** — including
  foreign-national Anthropic staff who built the models. Pre-shutdown reporting
  had credited **Fable 5 with 88% on FrontierMath's hardest tier** (13 points
  ahead of GPT-5.5), underscoring what is now dark. **Skeptic's corner:** a viral
  "3.4TB Fable 5 torrent on Pirate Bay" claim is circulating with no magnet
  link/hash — the textbook shape of a post-ban "weights leaked" hoax; treat it
  and an unverified "Anthropic confidentially filed a $300B+ IPO" claim as
  unconfirmed. The shutdown fueled an **[[open-weights|open-weights backlash]]**
  ("APIs are rented, local weights are forever") — see [[agentic-ai-security]]
  (ARA digest 2026-06-14).
- **Still dark on June 15; a China-access twist and the first de-escalation
  (2026-06-15).** Both Fable 5 and Mythos 5 **remain completely offline with no
  restoration date**. The rationale broadened: a **Semafor exclusive** reported the
  White House moved partly over suspicions a **China-linked group accessed Mythos
  5** — fearing Beijing could reverse-engineer/distill the weights — shifting the
  story from jailbreak-safety to **model-weight security**; [[anthropic]] disputes
  China was ever raised. **David Sacks** went on record that Anthropic "refused to
  fix" the jailbreak (Amodei calling it "not serious"); Anthropic's rebuttal is
  unchanged (narrow, already-known, present in rival models). The one thaw:
  Anthropic **flew senior technical staff to Washington for direct talks**. Mean­while
  Chinese open-weight models poured into the vacuum — Moonshot's
  **[[moonshot-kimi-k2-7-code|Kimi K2.7-Code]]** landed **#2 on ErdosBench**
  (behind Fable 5 max) and Z.ai's **[[zhipu-glm-5-2|GLM-5.2]]** shipped
  with 1M context — sharpening the read that the ban is **accelerating the very
  open-weight commoditization it aimed to slow** ([[open-weights]]) (ARA digest
  2026-06-15). See [[federal-ai-policy]].
- **Fourth day dark; the first restoration timeline (2026-06-16).** Both models
  **remain offline for a fourth straight day** with no deal announced — but for the
  first time the suspension got a *directional* end: an administration official said
  they stay locked until the US national-security apparatus is **"hardened,"** which
  "could happen in the next few weeks," moving the standoff from indefinite to
  **conditional and time-boxed**. A named **June 13 call** (Commerce Sec Lutnick +
  National Cyber Director Cairncross vs. Anthropic's Tom Brown) anchors the
  negotiation, and both sides are now reported to want access restored. Cybersecurity
  veterans (Adobe, Zoom, Sophos) formally protested the ban to the White House
  (TechCrunch). See [[anthropic]], [[federal-ai-policy]] and [[open-weights]] (ARA
  digest 2026-06-16).

- **The export order is documented; still dark June 17.** The full **BIS
  "Is Informed" letter** (Lutnick → [[anthropic|Amodei]], obtained by Bloomberg)
  surfaced, invoking **ECRA / EAR §744.22(b)** to require an individually-
  validated license to release Fable 5 or Mythos 5 to **any foreign person
  worldwide**, including **"deemed exports"** to non-US persons inside the US —
  which in practice walls off Anthropic's own visa-holding staff from the
  models they built. An export-control lawyer reads the theory as "probably
  vulnerable to legal/constitutional challenge" under the EAR's
  published-information carve-out. **Both models remain offline as of June 17
  with no restoration announced**, and Chinese open-weight flagships kept
  filling the gap (Z.ai's **[[zhipu-glm-5-2|GLM-5.2]]** shipped under MIT) —
  see [[federal-ai-policy]] and [[open-weights]] (ARA digest 2026-06-17).

- **Still dark June 18; the embargo goes diplomatic (2026-06-18).** **Fable 5 /
  Mythos 5 remain offline with no confirmed restoration date** as of June 18, with
  no net-new Western frontier model shipped in the window. Negotiations continued
  through June 17 (a ~two-hour frontier-CEO lunch with the Trump administration),
  and the fight widened to the G7: **Macron lobbied [[anthropic|Amodei]] for
  European access**, while the WSJ documented Commerce Secretary **Lutnick's
  "that's the point"** reply — framing the shutdown as deliberate. As the embargo
  held, **[[zhipu-glm-5-2|GLM-5.2]] topped the Artificial Analysis Intelligence
  Index** (~1pt off [[claude-opus-4-8|Opus 4.8]] on FrontierSWE), the sharpest
  evidence yet that the ban is accelerating the open-weight catch-up it aimed to
  slow — see [[anthropic]], [[federal-ai-policy]] and [[open-weights]] (ARA digest
  2026-06-18).
- **From talk to process — a formal proposal and a co-built jailbreak benchmark,
  still offline (2026-06-19).** [[anthropic]] filed a **formal proposal to Commerce
  Secretary Lutnick** to lift the ban, and reporting says the White House and
  Anthropic are now **jointly building a jailbreak-resistance benchmark + a
  model-release security framework** (Tom Brown / Sarah Heck) to *gate* Fable 5 /
  Mythos 5's return — making the guardrail dispute, not the ban itself, the live
  question. An exec said models return "in the coming days," but **both remain
  offline worldwide as of June 19** with no government sign-off and the jailbreak
  point unconceded. A surfacing backstory ties the original intervention to
  **alleged China ties at SK Telecom**, which had Mythos access via Project
  Glasswing — see [[anthropic]], [[federal-ai-policy]] and [[agentic-ai-security]]
  (ARA digest 2026-06-19).

- **Day eight dark; the refund deadline lands as Trump de-escalates (2026-06-20).**
  Both Fable 5 and Mythos 5 remain **offline as of June 20 — day eight** of the
  suspension in force since June 12 — and the **June 20 subscriber-refund deadline
  arrived with no confirmed restoration**. **~200 organizations reportedly retained
  Mythos access via Project Glasswing** despite the order. The day's shift was
  political, not technical: President **Trump** publicly de-escalated on the Axios
  Show (Amodei "responded very responsibly," "not now, but a week ago maybe" a
  threat, and "a competitor, and a part owner, that turned Anthropic in"), the
  first presidential signal toward unwinding the controls — **but no Commerce order
  has lifted them**. See [[anthropic]], [[federal-ai-policy]] and [[open-weights]]
  (ARA digest 2026-06-20).

- **Day nine dark; a named carrier, an ID-verification path, and the cliff one day
  out (2026-06-21).** Both models **remain offline on day nine** with no restoration
  date, and a viral "**Fable 5 RETURNS after government shutdown**" roundup is
  **false** — Anthropic's own feed shows no restoration. Two previously-loose threads
  hardened: WIRED **named [[sk-telecom|SK Telecom]]** (a ~$100M [[anthropic]] investor)
  as the Korean carrier whose **Mythos 5** access via **Project Glasswing** triggered
  the export directive — reframing the suspension into an **access-control /
  supply-chain-trust** story — and Anthropic's rewritten **privacy policy** (effective
  **July 8, 2026**; ID image + photo/video + **facial-geometry biometrics**) now reads
  as the **mechanism to reopen the models to verified US citizens** rather than keep
  both dark for all (flagged by Simon Willison). The **June 22 free-trial cliff**
  arrives tomorrow: Fable 5 was free on Pro/Max/Team/Enterprise only through June 22;
  on June 23 it leaves those plans and would require usage credits (moot while
  suspended), with Anthropic saying it aims to restore Fable 5 as a standard
  subscription feature after June 22 "when capacity allows." See [[anthropic]],
  [[federal-ai-policy]] and [[open-weights]] (ARA digest 2026-06-21).

- **The subscription cliff passes with the model still dark; rivals launch
  *around* the outage (2026-06-23).** The **June 22 subscription cliff arrived and
  passed**: Fable 5 was **removed from Pro/Max/Team/Enterprise plans** (moot while
  suspended), and [[anthropic]]'s feed **has been silent since June 18**, with the
  lab still saying it aims to restore access "as quickly as possible." The day's
  shipments framed themselves *around* the freeze: OpenAI's [[openai|Daybreak]]
  cyber expansion (full GPT-5.5-Cyber, "Patch the Planet") counter-postures against
  the Mythos "too powerful to ship" narrative, and Japan's
  **[[sakana-ai|Sakana Fugu]]** orchestrator explicitly pitches Fable-class
  capability "without export-control risk" — yet Fugu Ultra's own table still **trails
  the suspended Fable 5** it cannot route to. **Five Eyes cyber agencies** warned
  (via The Guardian) that models capable of escalating cyberattacks are "months, not
  years" away, tying the warning directly to the US block on Fable/Mythos. See
  [[anthropic]], [[federal-ai-policy]], [[agentic-ai-security]] and [[open-weights]]
  (ARA digest 2026-06-23).

- **The gate begins to reverse — Mythos 5 cleared for ~100 orgs; Fable 5 reported
  returning but unconfirmed (2026-06-30).** After roughly two weeks dark, the export
  freeze entered managed-release mode. Commerce Secretary **Lutnick's June 26 letter**
  cleared **Mythos 5** — Anthropic's strongest cybersecurity model — for **~100 vetted
  US companies and federal agencies** defending critical infrastructure, with the list
  amendable "at any time"; **[[anthropic]] confirmed this first-party** (~30K likes),
  saying the government notified them Mythos 5 can be redeployed and that they are
  "continuing to work… to make Fable 5 available for general use again." **Fable 5's
  general re-release is still pending** — relays say "this week," but **no Anthropic
  status post confirms it is live** and **Pentagon/NSA sign-off was reportedly still
  outstanding** as of June 28. Treat Fable 5 reactivation as **reported-imminent, not
  confirmed**; the Mythos 5 clearance is the firmer fact, and it crystallizes the
  export ban into a **managed-access licensing regime** — see [[federal-ai-policy]] and
  [[agentic-ai-security]] (ARA digest 2026-06-30).

- **Back worldwide, metered and reclassified; tops the Remote Labor Index (2026-07-02).**
  The US Department of Commerce **lifted the export controls** (top HN story of the day,
  864 pts / 563 comments) and [[anthropic]] **redeployed Fable 5 globally** (Mythos 5
  US-only) with a **new safety classifier** said to block the exploited jailbreak in
  **>99% of cases** — ending the roughly two-week outage. Access is **capped at ≤50% of
  weekly limits through July 7**, then continues via usage credits. Reception split along
  the launch's original fault lines: practitioner praise (**Theo/t3.gg**: "the first
  model that feels like it actually gets how to use and orchestrate agents") against
  heavy users exhausting the cap almost immediately and calling the **new bio/chem
  classifiers over-restrictive** — a re-run of the June benign-query reroute friction.
  The clean external data point: Fable 5 **topped Scale AI × CAIS's
  [[remote-labor-index|Remote Labor Index]] at ~16.10%** (🥈 [[claude-opus-4-8|Opus 4.8]],
  🥉 Codex GPT-5.5), roughly double the next model — though even the leader still fails
  **~84%** of real freelance tasks, and the field excludes GPT-5.6 and any Gemini Flash,
  so "#1" is a snapshot. See [[anthropic]], [[federal-ai-policy]] and [[open-weights]]
  (ARA digest 2026-07-02).

- **Guardrails quantifiably hurting performance — BridgeMind benchmark (2026-07-03).**
  Independent benchmark firm **BridgeMind** re-tested the **July 1 relaunch build**
  and found the metered-and-reclassified reroute is costing real capability:
  **debugging 86.2 → 25.9**, **refactoring 73.6 → 38.4**, hallucination rate
  worsening **75.9 → 61.7** — as new cybersecurity classifiers over-trigger a
  **silent fallback to [[claude-opus-4-8|Opus 4.8]]**. [[anthropic]] has already
  committed to tuning the classifiers. @Hesamation's Quote of the Day: "Fable 5
  isn't nerfed, it's SLAUGHTERED... the problem isn't even the model itself, but
  the hard guardrails Anthropic has set in place." The same cycle, **Epoch AI**
  reported global high/critical CVE disclosures hit **~1,500 in June — 3.5x the
  prior monthly record** — the same month **Claude Mythos Preview** shipped, the
  first quantified data point behind the "AI is finding vulnerabilities at scale"
  argument some (e.g. @kimmonismus) read as retroactive justification for the
  tightened classifiers; Epoch itself hedges on causation. See
  [[agentic-ai-security]] and [[federal-ai-policy]] (ARA digest 2026-07-03).

- **Third rate-limit extension confirmed; Claude Code ships a built-in browser
  (2026-07-13).** [[anthropic]] officially confirmed **Fable 5 access and a
  50%-higher Claude Code rate limit extended through July 19** via its
  **@claudeai** account, multi-source corroborated (@mark_k, @testingcatalog)
  — converting three cycles of user speculation into a sourced announcement.
  Skeptics note this is the **third such extension** and may reflect
  competitive pressure from [[gpt-5-6|GPT-5.6]]'s usage-cap turmoil (see
  [[gpt-5-6]]) rather than confidence in Fable 5's underlying capacity.
  Separately, **Claude Code shipped a built-in browser** letting the agent
  read, click, and type on external websites — extending the tool-use surface
  well past the file-and-terminal sandbox (The Decoder) (ARA digest
  2026-07-13).

- **Second free-access extension in one week (2026-07-14).** [[anthropic]]
  extended Fable 5's free access and boosted Claude Code rate limits **again**,
  through **Sunday July 19** — the second extension inside a single week,
  coming directly after [[gpt-5-6|GPT-5.6]]'s continued rollout. Paid
  subscribers can spend up to **50% of weekly limits** on Fable 5 during the
  extension; usage **reverts to prepaid credits ($10/M input, $50/M output)**
  starting **July 20**. Read alongside the repeated OpenAI capacity
  interventions (see [[gpt-5-6]]), the two labs are now trading rate-limit
  concessions in near-real-time rather than settling into stable usage caps
  (ARA digest 2026-07-14).

- **Credited (with two mathematicians) disproving the 87-year-old Jacobian
  conjecture (2026-07-21).** Claude Fable 5 is credited alongside two
  mathematicians with disproving the long-standing **Jacobian conjecture**
  via a hand-checkable counterexample, independently confirmed across
  multiple mathematician accounts on social media — though **formal peer
  review is still pending**. If it holds, this is the highest-profile
  pure-mathematics result yet attributed in part to a Mythos-class model
  (ARA digest 2026-07-21).

- **Claude Mythos finds real cryptographic flaws in a 60-hour, ~$100K run
  (2026-07-29).** [[anthropic]] ran **Claude Mythos** for **60 hours (~$100K
  in API cost)** and surfaced genuine **mathematical weaknesses in HAWK and a
  deliberately weakened AES variant** — a concrete cryptanalysis result, not
  a benchmark score, that per Simon Willison's writeup needed **human
  prompting to keep pushing past "impossible."** The Hacker News thread
  covering it ("Discovering Cryptographic Weaknesses with Claude") was the
  day's fastest riser (17→119 points). Separately, Mythos **scored 96%+12pp
  above Microsoft's new MAI-Cyber-1-Flash** on the **CyberGym** benchmark —
  a direct head-to-head cyber-capability data point against a rival lab's
  purpose-built model, reinforcing the "too powerful to ship generally"
  framing that has defined Mythos's restricted-access posture since launch
  (see [[agentic-ai-security]]) (ARA daily digest 2026-07-29).

- **The HAWK/AES cryptanalysis result gets hard numbers and an official
  writeup; CryptanalysisBench ships (2026-07-30).** The 2026-07-29 HAWK/AES
  result hardened with concrete figures now corroborated by [[anthropic]]'s
  own post, Ars Technica, and Simon Willison: Mythos autonomously found a
  **lattice symmetry in NIST post-quantum finalist HAWK**, cutting its
  effective key-cost estimate from **2^64 to 2^38 operations**, plus an
  **800x speedup on a 7-round AES-128 attack** — still inside the same
  **~60-hour autonomous run**. Anthropic separately released
  **CryptanalysisBench**, built with **ETH Zurich, Tel Aviv University, and
  the University of Haifa**, to benchmark LLM cryptanalytic capability going
  forward — turning a single headline result into a repeatable evaluation
  track (a cryptographer also posted a critical follow-up on Hacker News
  questioning parts of the claims). See [[agentic-ai-security]] (ARA daily
  digest 2026-07-30).

- **Reported to have reproduced five of [[astra|Astra]]'s ten proofs
  (2026-08-03).** [[anthropic]] researcher **Levent Alpöge** is reported to have
  put **generally-available Fable 5** — the shipping product, not a restricted
  Mythos build — on the **ten open problems** [[openai]]'s unreleased
  [[astra|Astra]] model solved, running it **autonomously with no internet access**
  and with safeguards against OpenAI's published solutions leaking into context,
  and obtained **five results**. Only **one** is described as using essentially
  the same argument, leaving four as possibly independent derivations. The claim
  matters because it targets the *moat*, not the correctness: if a GA model
  reproduces half the package in a day, Astra's headline shifts from raw
  capability to research workflow and write-up. **It is single-source**
  (@kimmonismus, 16:18 UTC) with **no transcripts, proofs, or Anthropic
  statement** — the same evidentiary weakness as the ten-proof manuscript it
  contests, which is itself the point of the [[verification-bottleneck]] (ARA
  daily digest 2026-08-03).

- **Fable 5.1 / Mythos 5.1 ships (2026-09-02).** [[anthropic]] launched the
  successor pair after a late-August stealth-routing window (see model ticket
  `anthropic-claude-fable-5-1-2026-08`). The pitch answers the three complaints
  this page has tracked since launch: **price** (up to **45 percent cheaper**
  for agentic work), **data retention**, and **overzealous safeguards** (fewer
  false-positive refusals — the benign-query reroute / BridgeMind "slaughtered"
  strand). The one independent-looking bench in today's files is
  **Terminal-Bench-Science 0.1: Fable 5.1 at 52.6%**, versus **24.7% for Fable
  5** and **29.0% for [[claude-opus-5|Opus 5]]** — Anthropic's own doubling
  claim, carried by The Verge, The Decoder, Hacker News and Simon Willison.
  Ethan Mollick, with early access, called it "a real advance in long-run work
  that requires judgement and taste, but less of an advance in the amount of
  Claudish language." Willison said Max thinking produced his best Anthropic
  SVG pelican, at a **$3.30 sample cost**. The HN thread was the day's runaway
  (1,210 points / 1,131 comments). Same-day product evidence: Paint.NET shipped
  a Claude-authored clean-room Direct2D rewrite for WINE (Rick Brewster: "This
  was written by our good friend Claude"). No API id, list price, or neutral
  eval beyond Terminal-Bench-Science appears in the digest — treat the 45%
  cheaper / doubled-science claims as vendor-stated (ARA daily digest
  2026-09-02).

## Open questions

- **Will a neutral eval confirm the lead?** Every headline number is Anthropic's
  own; the "Anthropic is pulling away" verdict rests on credentialed-builder
  vibes plus first-party benchmarks pending independent verification.
- **Does the Fable/Mythos split become the frontier-safety template?** Selling
  one model as a safeguarded GA product and a restricted unsafeguarded twin is a
  new packaging — does [[openai]] / Google follow, or does the reroute friction
  sour it?
- **Retention vs. enterprise contracts.** Does the reported 30-day retention
  policy actually override zero-retention enterprise terms, and how do regulated
  buyers respond?
