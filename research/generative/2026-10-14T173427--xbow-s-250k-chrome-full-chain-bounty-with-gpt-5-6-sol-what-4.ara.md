---
eyebrow: SECURITY ECONOMICS · AI OFFENSE
title: "$40K of Tokens, a $250K Bounty, and Months Nobody Billed: What XBOW's Chrome Full Chain Says About AI Exploit Economics"
deck: XBOW's GPT-5.6 Sol-assisted Chrome chain is real, patched and paid. The headline ratio is not the economics. The true story is a collapse in marginal cost sitting on top of fixed costs that the press release leaves out.
lede: |
  On October 13, 2026, XBOW said Google had paid it $250,000 for a full-chain Chrome exploit. Its researchers built the chain in six days in Las Vegas with AI agents running OpenAI's GPT-5.6 Sol, for about $40,000 in API charges. Every number in that sentence checks out against XBOW's own posts, and two of the three bugs check out against Google's release notes. The ratio the sentence invites ("16 cents of compute per bounty dollar") is the least informative part. This brief separates three things: the marginal cost of the awarded sprint, the fixed cost of the program behind it, and the market price of what was produced.
domain: general
stats:
  - {label: Chrome VRP award, value: "$250K", note: "XBOW, 2026-10-13"}
  - {label: API compute (reconstructed), value: "~$40K", note: "six-day sprint only"}
  - {label: Build window, value: "6", unit: days, note: "Aug 2–7, 2026"}
  - {label: Bugs in final chain, value: "3", note: "V8 · WebP · Crashpad"}
---

:::callout(kind=info, label="Short answer")
- **The facts hold up.** Google paid $250,000 for a three-bug Chrome chain that XBOW built from August 2–7, 2026, using `gpt-5.6-sol` agents. XBOW reconstructed about $40,000 of API charges from archived Codex logs [^1,2].
- **The ratio misleads.** $40K buys the *last* six days. It leaves out a two-month first chain that died on a duplicate, an effort that began with a challenge set in January, and four senior researchers' salaries [^1,2].
- **The marginal cost is the real signal.** Dolan-Gavitt's pre-LLM baseline is a team of four for 6–9 months, roughly 24–36 researcher-months. The awarded sprint was one researcher plus agents for six days [^1,2].
- **Prices did not move with costs.** A Chrome RCE-plus-privilege-escalation chain was listed at $2–3M by a broker in 2024 [^10]. Google pays $250K for a full chain, or up to ~$500K with the MiraclePtr bonus [^8]. Google has already cut bounties on the bug classes AI finds cheaply [^8,9].
:::

## 01. What actually happened, with the press errors removed

The verifiable core is narrow and solid: three bugs, three Chrome components, two public CVEs, one $250,000 award, and a disclosure date of October 13, 2026 [^1,2].

XBOW CEO Oege de Moor's announcement says Google awarded $250,000, "the first under its 2026 new rules," and that the bugs "are now fixed" [^1]. The companion technical post by Brendan Dolan-Gavitt names the parts at component level: "a V8 compiler bug, an animated-WebP decoder bug, and a memory-safety bug in Crashpad" [^2]. On model choice, de Moor says the team deliberately used "a model that is available to anyone, not a specialized security model or one with restricted access". He names it as GPT-5.6 Sol "and its predecessors" [^1]. The technical post names only `gpt-5.6-sol` [^2].

Google's own release notes confirm two of the three components independently. The August 25 desktop stable update lists CVE-2026-78952, a High-severity out-of-bounds write in Crashpad reported by Dolan-Gavitt of XBOW on August 13 [^5,7]. The September 3 update lists CVE-2026-85045, a High-severity race condition in V8 reported by Dolan-Gavitt on August 17 [^4,6].

:::kv
- {term: "Stage 1 — V8 (Maglev compiler)", def: "CVE-2026-85045 · High · reported 2026-08-17 · fixed in 2026-09-03 stable update"}
- {term: "Stage 2 — animated WebP decoder", def: "No public CVE located as of 2026-10-15; swapped in after a duplicate"}
- {term: "Stage 3 — Crashpad (Windows)", def: "CVE-2026-78952 · High · reported 2026-08-13 · fixed in 2026-08-25 stable update"}
- {term: "Reach (XBOW estimate)", def: "~1 billion Chrome-on-Windows users"}
- {term: "Model", def: "gpt-5.6-sol (\"and its predecessors\")"}
- {term: "Humans", def: "Dolan-Gavitt, Luksenberg, Lee, Pinckaers"}
:::

:::callout(kind=warn, label=Correction)
XBOW's press release, and coverage that copied it, puts CVE-2026-85045 on the WebP bug [^3,32]. Google's release notes and the CVE record put CVE-2026-85045 on the **V8** race condition. Its Chromium issue ID matches the one XBOW's own technical post gives for the Maglev bug [^4,6]. We found no public CVE for the WebP stage. Treat any "WebP = CVE-2026-85045" line as wrong.
:::

The timeline matters for the economics because it shows how much work sat outside the six days. De Moor says he set the challenge at a company all-hands in Malta at the start of 2026, with Black Hat in August as the target [^1]. A first full chain "died when its final stage collided with a bug that had been found internally by Google months before" [^2]. That chain took two months [^2].

:::timeline
- {date: "2026-01", headline: "Challenge set", body: "De Moor sets the full-chain goal at XBOW's all-hands in Malta; target is Black Hat in August."}
- {date: "2026-04/05", headline: "Google rewrites Chrome VRP", body: "Base rewards cut; full-chain cap kept at $250K; AI-driven report volume cited."}
- {date: "2026-07-09", headline: "GPT-5.6 system card", body: "OpenAI rates Sol High (not Critical) for cyber, after a gated preview from June 26."}
- {date: "2026-08-02 → 08-07", headline: "Awarded chain built", body: "Six days in Las Vegas during Black Hat / DEF CON; ~$40K API charges."}
- {date: "2026-08-13 / 08-17", headline: "Bugs reported", body: "Crashpad and V8 issues reported to Google."}
- {date: "2026-08-25 / 09-03", headline: "Fixes ship", body: "CVE-2026-78952 and CVE-2026-85045 patched in stable."}
- {date: "2026-10-13", headline: "Award disclosed", body: "XBOW announces the $250K award."}
:::

There is also a bug-count discrepancy. Every XBOW primary source says three bugs, built "as three independent parts, each with an alternative" [^1,2]. Higher counts circulating in early commentary are best explained by swapped-out alternates: an early version of the awarded chain used a different V8-sandbox escape that turned out to duplicate an existing issue [^2]. No XBOW or Google source gives a count other than three.

The "first" and "second-ever" framings deserve less weight than they got. Google's own 2025 year-in-review lists a $250,000 top reward for 2025 [^11]. SecurityWeek reported a $250,000 payout for a Chrome Mojo sandbox escape (CVE-2025-4609) in August 2025 [^16]. So a $250K Chrome payout is not new. XBOW's narrower claim, the first full-chain award under the *2026* rules, is plausible but rests on XBOW's word [^1].

**Why this matters:** the economics below only work if the inputs are real. They mostly are. The two public CVEs are independently verifiable, the fixes shipped within 12 and 17 days of report, and the money came from Google, not from a benchmark [^4,5].

## 02. The $40,000 is a marginal cost, not a production cost

The most-quoted number in the story is accurate, and almost nobody reads it the way its own author warns them to. $40,000 against $250,000 is 16 cents of compute per bounty dollar. It describes the final sprint, not the cost of producing a Chrome full chain.

Dolan-Gavitt's sentence is precise: "Reconstructing usage from the archived Codex logs puts the six-day campaign at roughly $40,000 in API charges" [^2]. That figure is reconstructed after the fact from logs, not an invoice. It covers the six-day campaign only, and he warns that it "does not mean that anyone can get a Chrome chain" [^2]. De Moor frames the same number as "a fraction of the bounty" [^1].

:::compare
- {role: LOWEST, name: "API compute, awarded sprint", value: "~$40K"}
- {role: HIGHEST, name: "Broker price, Chrome RCE+LPE (2024)", value: "$2–3M"}
- {role: SUBJECT, name: "Google Chrome VRP award", value: "$250K"}
:::

Here is what the $40K excludes, all from XBOW's own disclosures:

- **The failed first chain.** It took two months and was rejected because Google already knew one of its bugs [^1,2].
- **The swapped-out stage.** The awarded chain's early V8-sandbox escape was a duplicate and had to be replaced with the WebP bug [^2].
- **Seven months of program time.** The challenge was set in January; the awarded sprint ended August 7 [^1,2].
- **Four named researchers.** Dolan-Gavitt, Luksenberg, Lee and Pinckaers. Dolan-Gavitt alone, with agents, built the final chain [^1].
- **Prior tooling.** Outside analysis notes the agents built on XBOW's existing internal techniques and team knowledge [^32].

A labor floor can be estimated. The US Bureau of Labor Statistics puts the median annual wage for information security analysts at $129,180 as of May 2025, about $10,765 a month [^31]. Browser exploit developers earn well above the median analyst, so this is a floor, not an estimate. At that floor, Dolan-Gavitt's pre-LLM baseline of 24–36 researcher-months costs about $258K–$388K in wages alone [^2,31]. That is already at or above the $250K bounty. Before LLMs, a Chrome VRP full chain was roughly a break-even trade for a salaried team, which is one reason full chains went to brokers.

Apply the same floor to the *whole* XBOW program and the picture changes. Four researchers from January to August is up to about 28 researcher-months, or about $300K at the median wage [^1,31]. That is an upper bound: none of XBOW's posts say the four worked on Chrome full time, and part of their work also produced other Chrome bugs. XBOW's credits include a $1,000 Blink bug reported in July [^5]. Still, the program-level labor input is not obviously smaller than the pre-LLM baseline. What collapsed is the *last mile*.

:::callout(kind=info, label="How to read the ratio")
The useful comparison is not $40K vs $250K. It is the cost of the *next* chain, given a team that already has the scaffolding, the target knowledge and the review discipline. On that basis, XBOW's numbers say the marginal chain costs one senior researcher-week plus ~$40K. That is a real collapse. It is not the same as "anyone can buy Chrome for $40K."
:::

**Counterpoint:** an incumbent can say marginal cost is the *only* number that matters, because fixed costs are sunk once the capability exists, and every subsequent chain inherits them. That argument is right for XBOW and wrong for a new entrant. The question is which of the two will be producing most chains in 2027.

**Why this matters:** bounty and broker prices will reprice around marginal cost only if many teams reach XBOW's fixed-cost position. Until then, the $210K gap between award and compute is a return on XBOW's sunk investment, not a free lunch.

## 03. Six days versus six months: the labor curve is the real story

The strongest claim in XBOW's disclosure is not about dollars. It is about how much skilled labor a chain needs. The awarded chain took one senior researcher six days. XBOW's pre-LLM benchmark is a team of four for most of a year.

Dolan-Gavitt's own timeline is unusually candid: "Pre-LLMs a Chrome full chain would take a team of four around 6-9 months to be produced … our first submission took 2 months. The awarded one? six days" [^2]. De Moor cites a different anchor, a former intelligence-agency staffer who said his team "used to spend six months trying to identify this kind of vulnerability and get total access." De Moor's own reply: "We did it in six days" [^1]. The two baselines disagree slightly (6 months versus 6–9 months; team size unstated versus four), and both are anecdotes, not measured data.

At the low end of the baseline (four people, six months), the labor input is about 104 researcher-weeks. The awarded sprint was about one [^1,2]:

:::iso
- {label: "Pre-LLM baseline (4 × 6 mo, low end)", glyph: "👤", count: 104}
- {label: "XBOW first chain (2 months, team)", glyph: "👤", count: 9}
- {label: "XBOW awarded chain (1 researcher, 6 days)", glyph: "👤", count: 1}
:::

The first-chain figure (nine glyphs) assumes one researcher-equivalent for two months; XBOW does not say how many people worked on it. The pre-LLM and awarded-chain figures follow from XBOW's own numbers [^2].

What did the agents actually do? XBOW's division of labor is consistent across both posts. The agents "searched source code, tested hypotheses, built proofs of concept, and developed exploit stages". The humans "chose targets, supplied context, challenged results, redirected searches, and decided which components to join" [^2]. The work ran as parallel campaigns covering broad vulnerability search, V8 memory corruption, a V8 sandbox escape, a renderer sandbox escape and integration [^2]. The human decision XBOW singles out is building the chain as modular, swappable stages. That is what let it survive a duplicate [^1].

That split matches the vendor's own ceiling. OpenAI's system card treats GPT-5.6 Sol as High capability in cybersecurity under its Preparedness Framework, below Critical [^20,21]. Summaries of OpenAI's Chromium and Firefox evaluations say the models found bugs and exploitation primitives but "could not autonomously chain those primitives into a complete, functional exploit" [^21]. XBOW's result is therefore not evidence that the model crossed OpenAI's Critical line. It shows a human-in-the-loop system doing what the model alone could not.

**Counterpoint:** the labor curve is measured on a single, hand-picked senior team, not on a population of exploit developers. A median exploit developer with the same agents may not get the same 100× compression. XBOW's own forecast, that "within a year, each of the three bugs could be found by agents working on their own," is a prediction, not data [^1].

**Why this matters:** if the scarce input moves from *hands* to *judgment*, the supply of full chains is set by how many senior reviewers can steer agents, not by how many exploit developers exist. That pool is larger than the pool of people who can write a chain from scratch, but not infinitely larger.

## 04. Token economics: what $40,000 of GPT-5.6 Sol actually buys

Read through the model price sheet, the $40K is a statement about *volume*. It implies tens of billions of tokens of agentic search, most of it re-read context rather than generated text.

Before an August price cut, GPT-5.6 Sol listed at $5 per million input tokens and $30 per million output tokens [^19]. OpenAI's GPT-5.6 system card is dated July 9, 2026, after a gated preview that began June 26 [^20,21]. On August 21, Reuters reported a temporary cut. OpenAI's model page now lists $4 input, $0.40 cached input and $20 output, "available at least through November 21, 2026" [^18,19]. XBOW's sprint (August 2–7) predates the cut, so list prices applied. Long prompts above 272K input tokens are billed at 2× input and 1.5× output for the whole request [^18].

:::stats
- {label: "Sol list price (in / out, per M)", value: "$5 / $30", note: "at launch, 2026-07-09"}
- {label: "Sol promo price (in / out)", value: "$4 / $20", note: "as of 2026-10-15; ≥ Nov 21"}
- {label: "Cached input (promo)", value: "$0.40", note: "per M tokens"}
- {label: "Context window", value: "1.05M", note: "128K max output"}
:::

XBOW did not publish a token count. Hacktron did, for a closely related workload. In a July 14 lab benchmark, GPT-5.6 Sol Ultra built a working V8 exploit from public security-fix commits for $1,596.89 of compute. The root agent consumed 819.6 million input tokens, and 74 subagents together processed 1.27 billion input tokens and 4.04 million output tokens [^22]. That is roughly 2.1 billion tokens, more than 99% input, at a blended ~$0.76 per million, which only makes sense if most of it was cache hits [^22,23].

At Hacktron's blended rate, $40,000 corresponds to on the order of 50 billion tokens. At the uncached list input price the same money buys 8 billion. Either way, XBOW's sprint was tens of times larger than Hacktron's run: about 25× the dollars [^2,23].

:::bars
- {label: "Hacktron, Sol Ultra n-day V8 (Jul 2026)", value: "$1,597", pct: 4}
- {label: "Anthropic Mythos, Linux kernel n-day chain", value: "<$2,000", pct: 5}
- {label: "Anthropic Mythos, 1,000 OpenBSD runs", value: "<$20,000", pct: 50}
- {label: "Trail of Bits, whole AIxCC final", value: "$39,600", pct: 99}
- {label: "XBOW, awarded Chrome full chain", value: "~$40,000", pct: 100}
:::

The ladder is not apples to apples, and the differences are the lesson. Hacktron's run was an **n-day** V8 chain with public fix commits as a map, built against a V8 test shell rather than a shipping browser, with what Hacktron called "limited nudges" [^22,23]. Anthropic's sub-$2,000 kernel chain was also n-day work, and its OpenBSD figure covers a thousand runs of *search* [^24]. Trail of Bits' $39.6K bought 28 vulnerabilities and 19 patches across a whole competition, not one exploit [^27]. XBOW's $40K bought three **zero-days**, two sandbox escapes and a working integration on a hardened, shipping target [^1,2]. Anthropic makes the same point about its own numbers: the single run that found the OpenBSD bug "cost under $50, that number only makes sense with full hindsight" [^24].

**Counterpoint:** token prices are not a stable input. OpenAI has already cut Sol's price once, and the promo end date is a floor, not a schedule [^18]. A 33% output-price cut does little for a workload that is more than 99% input, if Hacktron's profile is representative. Caching discounts matter far more than headline per-token prices.

**Why this matters:** for a defender budgeting an AI red team, the relevant unit is not price per token. It is dollars per *validated finding*. On today's evidence that unit spans roughly two orders of magnitude, from n-day reproduction to zero-day full chains.

## 05. The price ladder: bounty, contest, broker

A full Chrome chain now has at least three public prices, and they differ by more than 10×. AI lowers the production cost for every buyer at once. Whether the gap narrows depends on whether supply rises faster than the bounty caps.

:::rank-list
- {label: "Broker — Chrome RCE + LPE (Crowdfense, 2024)", value: "$2M–$3M", pct: 100}
- {label: "Chrome VRP — full chain + MiraclePtr bonus (max)", value: "$500,128", pct: 17}
- {label: "Chrome VRP — full chain (XBOW's award)", value: "$250,000", pct: 8, highlight: true}
- {label: "Pwn2Own Berlin 2026 — Chrome sandbox escape", value: "$175,000", pct: 6}
- {label: "Pwn2Own Berlin 2026 — Chrome + Windows kernel EoP", value: "$125,000", pct: 4}
- {label: "Pwn2Own Berlin 2026 — Chrome renderer only", value: "$75,000", pct: 3}
:::

The broker anchor is old but public. In April 2024 Crowdfense advertised a $30 million acquisition program that would pay "between $2 million and $3 million for Chrome exploits leading to remote code execution and local privilege escalation" [^10]. Google's top Chrome tier has risen from up to $180,000 for the first full chain in a temporary 2023 offer [^15] to $250,000 since its August 2024 restructure. A MiraclePtr bypass bonus of $250,128 can stack on top [^33,8]. Pwn2Own Berlin 2026 priced a Chrome sandbox escape at $175,000 [^17].

On these numbers, Google's full-chain bounty is about 8–12% of the advertised broker price for comparable impact [^10,1]. That gap is not new. Before LLMs it was what made selling to brokers rational for profit-maximizing developers. What is new is the cost side. If the marginal chain costs one senior researcher-week plus ~$40K, then at $250K the bounty is comfortably profitable for a team with XBOW's tooling. A full chain was a break-even trade at the pre-LLM labor floor estimated in Section 02 [^2,31].

That changes the incentive for *defenders*. Google can now buy full chains well below the old break-even cost. The capped bounty no longer needs to compete with brokers on price, only on legality and reputation, which XBOW plainly values. Crowdfense's own price schedule also implies the opposite pressure: if production gets cheaper for everyone, broker prices are set by scarcity of *fresh* bugs in a hardening target, not by labor cost. GTIG data suggests browsers are getting scarcer as zero-day targets (Section 07).

**Counterpoint:** broker prices are list prices, often paid in installments contingent on the bug staying unpatched. Crowdfense's own research director attributed the 2024 increases to vendor mitigations that make the work "much more time consuming" [^34]. In the same reporting, industry insiders said private deals can go higher than published lists [^34]. The 8–12% ratio may overstate how cheap Google's bounty is relative to realized grey-market revenue, or understate it.

**Why this matters:** in a market where the legitimate buyer pays a tenth of the illegitimate one, the main thing keeping capability on the legitimate side is that the producers are companies with venture investors, customers and reputations. XBOW is one. That is a fragile basis for a security equilibrium.

## 06. Google is already repricing around AI, and the full chain is the category it protected

Google's 2026 VRP rewrite is the clearest primary evidence that AI has changed the cost of finding bugs. Google cut what it pays for the cheap end and protected the full chain.

In its spring 2026 revision Google cut the Chrome memory-safety base reward to $500 with multipliers, and phased out the bonuses for arbitrary read/write and renderer RCE introduced the year before [^8,9]. It explicitly prioritized "categories that remain more challenging for automated AI tooling to find" [^8]. Full-chain exploits on current OS and hardware kept their "up to $250,000" ceiling, plus the MiraclePtr bonus [^8,9]. Chrome Security's Q2 2026 summary says the reward structure was adjusted "to reflect the volume of reports being discovered and fixed using internal AI tooling". It adds that the Big Sleep agent "now operates as a fully automated pipeline, helping secure V8" [^14].

:::slope(left-label=2024, right-label=2025, unit=$M)
| Program | 2024 | 2025 |
|---|---|---|
| Google VRP, all programs | 11.8 | 17.1 |
| Chrome VRP | 3.4 | 3.72 |
:::

Spending is still rising. Google paid a record $17.1 million across all programs in 2025, to 747 researchers, more than 40% above 2024 [^11,13]. Chrome's VRP paid $3,716,750 in 2025 against $3.4 million to 137 researchers for 337 valid bugs in 2024 [^12,13]. Google told reporters it still expects aggregate rewards to rise in 2026 despite lower per-bug payouts [^9]. On 2025 numbers, XBOW's single award equals about 6.7% of the entire Chrome VRP year [^13,1].

Google's design choice follows from first principles. If AI makes individual memory-safety bugs cheap to find, paying a lot for each one just subsidizes report spam and turns triage into the bottleneck. Chrome Security says it will be "more frequently rejecting reports that are not compliant" [^14]. Paying for *demonstrated, end-to-end impact* is still a good trade, because a full chain proves the mitigations failed. That is the information Chrome's sandbox and MiraclePtr investments need. XBOW's award is the first big data point that the protected category can also be attacked with AI.

**Counterpoint:** the April rewrite has been contentious. SecurityWeek has since linked to a story headlined "Google Partially Reverses Chrome Bug Bounty Cuts," which we could not retrieve. At least one report says Google raised the base reward again in October 2026, which we could not corroborate, so the base-reward figures may have moved since May [^9]. The full-chain ceiling is not reported to have changed.

**Why this matters:** if agent-assisted teams can produce full chains at XBOW's marginal cost, Google faces the same problem one level up. Either the full-chain bonus gets rationed, or its price falls the way the base rewards did.

## 07. Where this sits on the AI exploit cost curve

XBOW's chain is the most expensive point on a public AI exploit cost curve that has fallen fast. It is also the most valuable. The curve's slope matters more than any single point.

Two and a half years ago, a University of Illinois team reported that GPT-4 could exploit 87% of a set of 15 one-day vulnerabilities when given the CVE description, versus 7% without it [^28]. It estimated about $8.80 per successful exploit at $10/$30 per million tokens [^28]. The set spanned website, container and Python-package one-days, and the agent had the CVE text as a map [^28]. In August 2025, DARPA's AI Cyber Challenge finalists found and patched real bugs at industrial scale: Trail of Bits' system found 28 vulnerabilities and applied 19 patches for $39.6K total, $181 per scored point [^27]. In April 2026, Anthropic reported Mythos Preview producing Linux kernel n-day chains for under $2,000. It described exploits "in every major web browser", but withheld cost and detail because those bugs were not yet patched [^24]. In July 2026, Hacktron's Sol Ultra run produced a V8 n-day exploit for $1,597 [^22,23]. In August 2026, XBOW's team produced a patched, paid zero-day full chain for about $40K [^2].

:::timeline
- {date: "2024-04", headline: "UIUC one-day agents", body: "GPT-4 exploits 87% of 15 one-days given CVE text; ~$8.80 per exploit."}
- {date: "2025-08", headline: "DARPA AIxCC final", body: "Trail of Bits finds 28 vulns, 19 patches, $39.6K total spend."}
- {date: "2026-04", headline: "Anthropic Mythos Preview", body: "Kernel n-day chains under $2K; browser exploits reported, details withheld."}
- {date: "2026-07", headline: "Hacktron Sol Ultra", body: "V8 n-day exploit from patch commits, $1,597 compute."}
- {date: "2026-08", headline: "XBOW Chrome full chain", body: "Three zero-days, two sandbox escapes, ~$40K, six days."}
:::

Each step up the curve added a harder condition: from known bug to unknown bug, from one component to three, from lab build to shipping browser. Each step cost one to two orders of magnitude more compute. That is the shape you would expect if AI is turning exploit development from a labor problem into a search problem. Search cost scales with how much of the space must be explored, and a zero-day full chain explores far more of it than an n-day reproduction.

The threat data is mixed. Google Threat Intelligence Group tracked 90 in-the-wild zero-days in 2025, up from 78 in 2024 and below 2023's record 100. Browsers were "less than 10%" of exploitation, which GTIG reads as hardening working, possibly combined with better attacker operational security [^26]. GTIG also expects adversaries to use AI to accelerate "vulnerability discovery, and exploit development" in 2026 [^26]. So far the public browser data show defenders gaining ground, not losing it.

**Counterpoint:** declining observed browser zero-days could reflect detection gaps rather than scarcity, which GTIG itself flags [^26]. A low count says little about what well-resourced actors are holding.

**Why this matters:** the curve suggests the price of a browser full chain is set by *search volume*, which falls with token prices and better scaffolds. If XBOW's "within a year" forecast is even half right, the $40K point is the high-water mark, not the floor [^1].

## 08. Who captures the surplus

The $210,000 gap between award and compute is the smallest economic prize in this story. The larger one is the signal XBOW sends to buyers of its software. Read that way, the bounty is cheap marketing with a real security side-benefit.

XBOW raised a $120 million Series C on March 18, 2026, at a valuation over $1 billion, led by DFJ Growth and Northzone [^29]. It had previously reached the top of HackerOne's US leaderboard in 2025, submitting nearly 1,060 vulnerabilities. Bug bounty programs had resolved 130 of them, with 303 triaged, 208 duplicates and 209 informative at the time of its post [^30,25]. Those numbers already showed the pattern: high-volume automated discovery, with a long tail that consumed triage capacity.

The Chrome award is a different product signal. De Moor's post closes by inviting design partners for "an autonomous product for testing compiled software" [^1]. A $250,000 check from Google is a credential that no benchmark can buy. Against XBOW's valuation, the bounty is a rounding error. The demonstration is not.

:::stats
- {label: "XBOW Series C", value: "$120M", note: "2026-03-18"}
- {label: "Valuation", value: ">$1B", note: "per XBOW"}
- {label: "HackerOne submissions (2025)", value: "~1,060", note: "130 resolved at time of post"}
- {label: "Chrome bounty as share of Series C", value: "0.2%", note: "$250K / $120M"}
:::

Google captures the other share of the surplus. It gets three patched bugs in a browser XBOW estimates reaches about a billion Windows users, for less than the broker price of one of them, plus evidence that its full-chain tier still attracts the best AI-assisted teams [^1,10]. OpenAI also captures something: a public demonstration that its generally available model is useful for defense. That supports OpenAI's choice to release Sol beyond the gated preview it began with [^20,21].

**Counterpoint:** a vendor-reported success is selected. We see the chain that paid, not the campaigns that burned compute and found duplicates, which outside analysts also stress [^32]. Including those failures would raise XBOW's true cost per awarded chain, by an amount it has not disclosed.

**Why this matters:** when the main beneficiary of a bounty is the marketing value to the researcher, bounty size stops being the lever that pulls capability toward defense. Corporate reputation is the lever. That works for venture-backed firms and does nothing for anonymous sellers.

## 09. What could break the thesis

This brief argues that XBOW's numbers show a collapse in the *marginal* labor and compute cost of a browser full chain, sitting on fixed costs the headline omits. Five things would weaken that.

**1. The baseline may be overstated.** The "team of four, 6–9 months" comparison is Dolan-Gavitt's estimate, and de Moor's anecdote says six months [^1,2]. Elite pre-LLM researchers sometimes worked far faster. Pwn2Own's $175,000 prize for a Chrome sandbox escape only makes sense if individual entrants can field one [^17]. If the true pre-LLM baseline was a few researcher-months, the compression is 10×, not 100×. That is still large, but different.

**2. The $40K may be understated.** It is a reconstruction from Codex logs, covers only six days, and is labeled "roughly" [^2]. De Moor attributes the work to Sol "and its predecessors," which implies earlier-model compute outside the window [^1]. Neither post gives a token count, agent count or failed-run cost.

**3. One success is not a rate.** XBOW reports one awarded chain and one failed chain [^1,2]. Two data points cannot separate skill from luck, and duplicates appear to be getting more common as automated discovery spreads. Two of XBOW's own stages collided with known bugs [^2].

**4. The model may matter less than claimed.** OpenAI's own evaluation found Sol could not autonomously finish a full chain [^21]. The human steering that XBOW describes may be doing most of the work, in which case "GPT-5.6 Sol builds a Chrome exploit" is the wrong headline. "Senior researcher with a fast search engine builds a Chrome exploit" is closer.

**5. Defense is scaling too.** Google's Big Sleep now runs as an automated V8 pipeline. Browser exploitation has fallen to historic lows in GTIG's data. Google patched XBOW's Crashpad bug 12 days after report [^5,14,26]. If defenders' AI finds the same bugs first, the market value of AI-found chains falls even as their cost falls.

:::callout(kind=warn, label=Unresolved)
We could not locate a public CVE for the WebP stage, could not read OpenAI's system-card PDF directly (it is cited through third-party summaries), and could not verify a claim, circulated in coverage of the announcement, that this was only the second $250K full-chain award in Chrome's history. Google's 2025 $250K payout for CVE-2025-4609, a sandbox escape, complicates that claim [^16].
:::

Red-team pass: 3/3 top claims unbroken. An adversarial search for contradicting evidence found none against the $250K / $40K / six-day core, the CVE-2026-85045 correction, or the 6–9-month team-of-four baseline as XBOW stated it [^2,6].

The net reading: AI did not make Chrome cheap to break. It made the *last step* cheap for a team that had already paid for the first steps. Whether that spreads beyond firms like XBOW depends less on token prices than on how fast senior judgment can be packaged into scaffolds. XBOW's own forecast is one year [^1]. The 2027 Chrome VRP results will test that forecast.

:::references
- {id: 1, title: "XBOW Built a Chrome Full-Chain Exploit Affecting a Billion Users in Six Days", url: "https://xbow.com/blog/xbow-built-a-chrome-full-chain-exploit", source: "XBOW (Oege de Moor)", date: "2026-10-13"}
- {id: 2, title: "Zero to Calc in Six Days: Inside XBOW's Chrome Full Chain", url: "https://xbow.com/labs/research/zero-to-calc-in-six-days-inside-xbow-chrome-full-chain.md", source: "XBOW Labs (Brendan Dolan-Gavitt)", date: "2026-10-13"}
- {id: 3, title: "XBOW rewarded for exploit affecting a billion users (press release)", url: "https://xbow.com/news/xbow-rewarded-for-exploit-affecting-a-billion-users.md", source: "XBOW", date: "2026-10-13"}
- {id: 4, title: "Stable Channel Update for Desktop (Chrome 152.0.7977.82/.83)", url: "https://chromereleases.googleblog.com/2026/09/stable-channel-update-for-desktop_01882797386.html", source: "Chrome Releases", date: "2026-09-03"}
- {id: 5, title: "Stable Channel Update for Desktop (Chrome 152.0.7977.64/.65)", url: "https://chromereleases.googleblog.com/2026/08/stable-channel-update-for-desktop_0256176589.html", source: "Chrome Releases", date: "2026-08-25"}
- {id: 6, title: "CVE-2026-85045", url: "https://app.opencve.io/cve/CVE-2026-85045", source: "OpenCVE / NVD mirror", date: "2026-09-03"}
- {id: 7, title: "CVE-2026-78952", url: "https://app.opencve.io/cve/CVE-2026-78952", source: "OpenCVE / NVD mirror", date: "2026-08-25"}
- {id: 8, title: "Google to pay up to $1.5 million for zero-click Pixel Titan M exploits", url: "https://www.helpnetsecurity.com/2026/05/05/google-vulnerability-reward-program-android-chrome-pixel/", source: "Help Net Security", date: "2026-05-05"}
- {id: 9, title: "Google Adjusts Bug Bounties: Chrome Payouts Drop as Android Rewards Rise Amid AI Surge", url: "https://www.securityweek.com/google-adjusts-bug-bounties-chrome-payouts-drop-as-android-rewards-rise-amid-ai-surge/", source: "SecurityWeek", date: "2026-05-01"}
- {id: 10, title: "Company Offering $30 Million for Android, iOS, Browser Zero-Day Exploits", url: "https://www.securityweek.com/company-offering-30-million-for-android-ios-browser-zero-day-exploits/", source: "SecurityWeek", date: "2024-04-08"}
- {id: 11, title: "VRP 2025 Year in Review", url: "https://blog.google/security/vrp-2025-year-in-review/", source: "Google", date: "2026-03-31"}
- {id: 12, title: "Vulnerability Reward Program: 2024 in Review", url: "https://blog.google/security/vulnerability-reward-program-2024-in/", source: "Google", date: "2025-03-07"}
- {id: 13, title: "Google paid $17.1 million for vulnerability reports in 2025", url: "https://bleepingcomputer.com/news/google/google-paid-171-million-for-vulnerability-reports-in-2025", source: "BleepingComputer", date: "2026-03-12"}
- {id: 14, title: "Chrome Security Q2 2026 summary", url: "https://groups.google.com/a/chromium.org/g/security-dev/c/q2r512CzLio", source: "Chromium security-dev", date: "2026-07-15"}
- {id: 15, title: "Google triples reward for Chrome full chain exploits", url: "https://www.helpnetsecurity.com/2023/06/02/chrome-full-chain-exploit/", source: "Help Net Security", date: "2023-06-02"}
- {id: 16, title: "Chrome Sandbox Escape Earns Researcher $250,000", url: "https://www.securityweek.com/chrome-sandbox-escape-earns-researcher-250000/", source: "SecurityWeek", date: "2025-08-11"}
- {id: 17, title: "Pwn2Own Berlin 2026 Rules", url: "https://www.zerodayinitiative.com/Pwn2OwnBerlin2026Rules.html", source: "Zero Day Initiative", date: "2026-05"}
- {id: 18, title: "GPT-5.6 Sol model page", url: "https://developers.openai.com/api/docs/models/gpt-5.6-sol.md", source: "OpenAI", date: "2026-10-15"}
- {id: 19, title: "OpenAI Cuts GPT-5.6 Sol API Prices", url: "https://letsdatascience.com/news/openai-cuts-gpt-56-sol-api-prices-fbfd85f3", source: "Let's Data Science (citing Reuters)", date: "2026-08-22"}
- {id: 20, title: "GPT-5.6 System Card", url: "https://deploymentsafety.openai.com/gpt-5-6/gpt-5-6.pdf", source: "OpenAI", date: "2026-07-09"}
- {id: 21, title: "Government-Gated AI: GPT-5.6 Sol's Dual-Use Cybersecurity Implications", url: "https://labs.cloudsecurityalliance.org/research/csa-research-note-frontier-ai-dual-use-cybersecurity-gpt56-2/", source: "Cloud Security Alliance", date: "2026-06-28"}
- {id: 22, title: "Watching GPT-5.6 Sol Ultra Write a Chrome Exploit", url: "https://www.hacktron.ai/blog/watching-gpt-55-sol-ultra-write-a-chrome-exploit-exploit-development-as-we-know-it-is-over", source: "Hacktron", date: "2026-07-14"}
- {id: 23, title: "Hacktron's Chrome test put a complete AI-built exploit chain at $1,597", url: "https://runtimewire.com/article/hacktron-chrome-exploit-benchmark-gpt-56-sol-ultra", source: "RuntimeWire", date: "2026-09"}
- {id: 24, title: "Claude Mythos Preview (red-team report)", url: "https://www.anthropic.com/research/mythos-preview", source: "Anthropic", date: "2026-04-07"}
- {id: 25, title: "AI Bug Hunter Sets Milestone By Claiming Top Spot on HackerOne's Leaderboard", url: "https://www.techrepublic.com/article/news-ai-xbow-tops-hackerone-us-leaderboad/", source: "TechRepublic", date: "2025-06"}
- {id: 26, title: "2025 Zero-Days in Review", url: "https://cloud.google.com/blog/topics/threat-intelligence/2025-zero-day-review/", source: "Google Threat Intelligence Group", date: "2026-03-06"}
- {id: 27, title: "Trail of Bits' Buttercup wins 2nd place in AIxCC Challenge", url: "https://blog.trailofbits.com/2025/08/09/trail-of-bits-buttercup-wins-2nd-place-in-aixcc-challenge/", source: "Trail of Bits", date: "2025-08-09"}
- {id: 28, title: "LLM Agents can Autonomously Exploit One-day Vulnerabilities", url: "https://arxiv.org/abs/2404.08144", source: "arXiv (UIUC)", date: "2024-04-11"}
- {id: 29, title: "XBOW Raises $120M to Scale", url: "https://xbow.com/news/xbow-raises-120m-to-scale", source: "XBOW", date: "2026-03-18"}
- {id: 30, title: "Top 1: How XBOW Did It", url: "https://xbow.com/blog/top-1-how-xbow-did-it/", source: "XBOW (Nico Waisman)", date: "2025-06-24"}
- {id: 31, title: "Information Security Analysts — Occupational Outlook Handbook", url: "https://www.bls.gov/ooh/computer-and-information-technology/information-security-analysts.htm", source: "US Bureau of Labor Statistics", date: "2025-05"}
- {id: 32, title: "XBOW Chrome Exploit Won Google's $250,000 Bounty, but Humans Still Made the Critical Calls", url: "https://www.remio.ai/post/xbow-chrome-exploit-won-googles-250-000-bounty-but-humans-still-made-the-critica", source: "remio", date: "2026-10"}
- {id: 33, title: "The Chrome VRP full-chain reward restructure (Aug 2024)", url: "https://www.theregister.com/2024/08/29/google_chrome_vuln_rewards/", source: "The Register", date: "2024-08-29"}
- {id: 34, title: "Price of zero-day exploits rises as companies harden products against hackers", url: "https://www.yahoo.com/tech/price-zero-day-exploits-rises-150051973.html", source: "TechCrunch (via Yahoo Tech)", date: "2024-04-06"}
:::
