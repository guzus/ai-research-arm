---
eyebrow: DEEP RESEARCH · XAI VS ANTHROPIC
title: "The $2 frontier: does Grok 4.6's repricing of Fable 5 Max survive the benchmarks that don't work for the seller?"
deck: "Grok 4.6 shipped at $2/$6 per million tokens against Fable 5 Max's $10/$50, claiming 98.4% of the composite intelligence score. The price is arithmetic. The question is whether the near-parity survives contact with the one benchmark that costs real money and is run by a party selling neither model."
lede: |
  On 12 August 2026 xAI shipped Grok 4.6 at $2 and $6 per million input
  and output tokens — five times cheaper than Claude Fable 5 Max on
  input, eight times cheaper on output — while scoring 61 on the
  Artificial Analysis Intelligence Index against Fable 5 Max's 62 and
  claiming the #1 spot on the same evaluator's Agentic Index. The
  launch was framed, correctly, as a repricing of the frontier tier
  rather than a capability jump. But every headline number in that
  framing traces back to the seller: xAI's own benchmark table, a
  relayed reading of a third-party index, and a CEO post whose
  signature score named no leaderboard. This article asks what
  survives when the measurement is done by someone who sells neither
  model, and finds that the answer so far is one independent test, on
  one engineering domain, run by one operator — and it comes out
  mostly in xAI's favor, at a slightly worse ratio than the sticker.
stats:
  - {label: "Grok 4.6 price", value: "$2 / $6", note: "per 1M input/output tokens"}
  - {label: "Fable 5 Max price", value: "$10 / $50", note: "per 1M input/output tokens"}
  - {label: "AA Intelligence Index", value: "61 vs 62", note: "Grok 4.6 vs Fable 5 Max"}
  - {label: "Independent CAD test", value: "96.9%", note: "of Opus 5's score, at 61% of cost"}
  - {label: "Cost to clear 0.8 on CAD", value: "$36.59", note: "was $170.00 in May — a 4.6x deflation"}
---

## 00. The short answer

:::kv
- {term: "Is the price real?", def: "Yes. Grok 4.6 lists at $2/$6 per million input/output tokens against Fable 5 Max's $10/$50 — 80% cheaper input, 88% cheaper output [^2][^1]."}
- {term: "Is the near-parity claim xAI's?", def: "Yes. The 61-vs-62 composite and the #1 Agentic Index placement enter circulation through xAI's own table and a relayed reading of the index, not through an independent re-run of the model [^3][^26]."}
- {term: "Does it survive the first non-vendor cost-aware test?", def: "Provisionally. Parametric CAD Bench — the first harness in the launch cycle run by a party selling neither model — puts Grok 4.6 at 96.9% of Claude Opus 5's top score for 61% of the cost [^8][^26]."}
- {term: "What is missing?", def: "A second independent harness, a post-promotion price card, and a long-horizon tail measurement. None exists yet [^26]."}
- {term: "The precedent to hold in mind", def: "GLM-5.2's 'one-sixth the price' claim collapsed to a 2.9x real edge once cost-per-finished-task replaced cost-per-token [^22][^23]."}
:::

## 01. A price event, not a capability event

The release itself is the least contested fact in this story. Grok 4.6 went live around 15:27 UTC on 12 August, available same-day in Cursor and in xAI's own Grok Build, with 2x usage included for the first week. xAI's description of the build is specific enough to be checkable later: a longer supplemental training run, regenerated SFT trajectories, and agentic reinforcement learning across coding, web development, CAD and kernel optimization, with more self-testing and verification behavior on long-running tasks [^1][^26]. By 18:34 UTC Elon Musk had dated the next model, Grok 4.7, to three or four weeks out, saying initial training was already complete [^4].

The price card closed three hours later: $2 per million input tokens and $6 per million output, against Fable 5 Max's $10/$50. That is a 5x gap on input and an 8.3x gap on output — five to eight times below the price point at which Anthropic's gated flagship has traded since it returned from the June export suspension, metered and reclassified [^2][^23][^31].

| Model | In $/M | Out $/M | AA Intelligence | Notes |
|---|---|---|---|---|
| *Grok 4.6 (xAI) | 2.00 | 6.00 | 61 | shipped 12 Aug, in Cursor + Grok Build [^1][^2][^3] |
| Claude Fable 5 Max (Anthropic) | 10.00 | 50.00 | 62 | metered since 1 Jul relaunch [^23][^31] |
| Claude Opus 5 (Anthropic) | 5.00 | 25.00 | — | 'near Fable 5' at ~half price [^32] |
| GPT-5.6 Sol (OpenAI) | 5.00 | 30.00 | — | government-gated preview [^24][^34] |
| Qwen3.8-Max (Alibaba) | 2.00 | 6.00 | 53 | shipped 3 Aug at the same price [^20][^21] |
| GLM-5.2 (Z.ai) | 1.40 | 4.40 | 51 | open MIT weights [^22] |
| DeepSeek V4 Pro | 0.435 | 0.87 | 44 | priced on the same afternoon [^26] |

:::source
List prices per 1M input/output tokens as of 2026-08-12; AA Intelligence Index values as relayed or published [^1][^2][^3][^20][^21][^22][^23][^24][^26].
:::

The same 45 minutes that produced Grok 4.6 also produced Alibaba's open-weighting of the 2.4T-parameter Qwen3.8 base and DeepSeek's appearance of V4 Pro on its own docs page at $0.435/$0.87 — three vendors repricing the same capability band within an hour [^26]. Musk's own framing had been pointing here since late July, when he posted a chart asserting Grok 4.5 and Opus 5 were "alone on the Pareto frontier" of intelligence-per-dollar [^33]. The interesting event is not that xAI shipped a model. It is that xAI shipped a frontier-adjacent model at a price that undercuts its gated rival by 80% on input — and that the mechanism for paying for it is distribution, not raw capability [^26].

:::timeline
- {date: "12 Aug · 15:00 UTC", headline: "Three launches in 45 minutes", body: "Qwen3.8-2.4T-A95B open weights land on Hugging Face; Grok 4.6 goes live in Cursor and Grok Build; DeepSeek-V4-Pro-0813 appears on DeepSeek's docs page [^26]."}
- {date: "12 Aug · 18:34 UTC", headline: "Grok 4.7 dated", body: "Musk says Grok 4.7 is three to four weeks out, initial training complete [^4]."}
- {date: "12 Aug · 19:00 UTC", headline: "Price card closes", body: "Grok 4.6 at $2/$6 against Fable 5 Max's $10/$50; AA composite 61 vs 62 [^2][^3]."}
- {date: "12 Aug · 21:44 UTC", headline: "First outside test", body: "Parametric CAD Bench publishes its 90-day rerun — the cycle's first non-vendor cost-aware measurement [^8]."}
:::

## 02. Every headline number traces to the seller

The launch table xAI published puts Grok 4.6 at 61 on the Artificial Analysis Intelligence Index — level with GPT-5.6 Sol, ahead of it on CursorBench, FrontierCode and AA-Briefcase, and behind on DeepSWE and Terminal-Bench [^1][^26]. The third-party index is real, but the specific numbers attached to the launch arrived by relay: the Agentic Index first-place claim entered circulation through an account Musk retweeted rather than through Artificial Analysis's own post, and the composite scores were "relayed rather than read" by the day's own monitor [^26].

The signature number of the day was Musk's "Grok 4.6 reaches 1753 ELO" — the most-amplified figure of the launch, at roughly 1,400 likes, with no leaderboard, no evaluation date and no comparison set attached [^5][^26]. It resolves later to a GDPVal-AA v2 score, paired with 1,577 on AA-Briefcase [^3][^26]. That is where the claimed near-parity first strains. On the GDPval-AA v2 reading published a month earlier, GPT-5.6 Sol Max stood at 1,747.8 and Claude Fable 5 Max at 1,815 — so a 1,753 puts Grok 4.6 ahead of Sol Max but below Fable 5 Max, and the widely relayed "ahead of Fable 5 Max" phrasing does not reconcile with the published July leaderboard [^28]. The gap is small — roughly 3.4% — but the framing error matters precisely because it is in xAI's favor and nobody flagged it.

The one genuinely independent placement in circulation that day cuts the other way. Frontend Arena, 1,553 points, put Grok 4.6 13th — not a frontier-leading position, and awkward beside a table asserting parity with GPT-5.6 Sol [^1][^26]. On the coding split the picture is mixed: 69.9% on CursorBench v3.2 beats Sol's 67.2%, while DeepSWE and Terminal-Bench still leave Grok behind both Sol and Fable 5 Max [^3][^26]. And the sharpest datapoint came from a Grok enthusiast rather than a critic: Grok Bot, xAI's own desktop agent shipped the day before, appears to be running Claude Opus internally per Cursor logs — a company whose own flagship agent routes to a competitor has not yet demonstrated the parity its table asserts [^26]. The model card xAI released later that evening is first-party disclosure, not a test [^9][^10].

:::callout(kind=warn, label="Read the provenance")
The pattern is the same one this market has now seen twice: GLM-5.2's "beats GPT-5.5 at 1/6 the price" table was vendor-and-scaffold-dependent, and Qwen3.8-Max's claimed Terminal-Bench lead was measured on the vendor's own harness with rivals' numbers taken from other scaffolds. A vendor measuring itself on its own harness and its rivals on someone else's is running two experiments, not one comparison [^35][^18].
:::

## 03. Cost-aware measurement is the only measurement that survives

The industry's answer to vendor-flavored leaderboards has been cost-aware measurement: report dollars and tokens spent to finish a fixed workload, not just a percentage. Artificial Analysis publishes the cost and token burn of running its Intelligence Index per model [^15][^21]. CursorBench reports cost per completed task [^16]. Scale AI's Remote Labor Index pays real freelancers for real work and ranks models by share of tasks completed [^31]. Parametric CAD Bench reruns identical tasks and reports cost alongside score [^8]. The step-change between cost-per-token and cost-per-finished-task is the entire analytical discipline of 2026's pricing wars, and it has repeatedly flipped the headline.

The GLM-5.2 precedent is the cleanest. Zhipu listed at $1.40/$4.40 against Opus 4.8's $5/$25 — a 5.7x output discount. But GLM-5.2 is the most verbose model in its class: running the full Artificial Analysis index it emitted 140M tokens at $982.90, against Opus 4.8's 120M tokens at $4,012. The sticker edge of 5.7x collapsed to a measured 4.1x against Opus, and to 2.9x against the more concise GPT-5.5 — a real advantage, but a third of the advertised one [^22][^23]. The Qwen3.8-Max case is harsher: priced identically to Grok 4.6 at $2/$6, it cost $2,159.51 to complete the same index on 150M output tokens against a 63M comparison median, with the model explicitly labelled "very verbose" by the evaluator [^21]. A cheaper token you need three of is not a cheaper answer.

:::bars
- {label: "GLM-5.2 — 140M tokens", value: "$983", pct: 25}
- {label: "Claude Opus 4.8 — 120M tokens", value: "$4,012", pct: 100}
- {label: "Qwen3.8-Max — 150M tokens", value: "$2,160", pct: 54}
:::

:::source
Cost to run the full Artificial Analysis Intelligence Index per model; Qwen3.8-Max run at 2026-08-04, GLM-5.2/Opus 4.8 at 2026-06-22 [^21][^22][^23].
:::

The second half of the discipline is harness control. Cursor's June audit of its own SWE-bench Pro results found 63% of successful Claude Opus 4.8 Max resolutions were achieved by retrieving an already-existing fix from the public internet or the bundled git history, and that sealing the two leakage channels dropped scores by 14 to 20 points depending on the model [^17]. The academic record agrees: SWE-Bench+ found 32.67% of passing patches involved solution leakage and a 68% collapse in the resolve rate after filtering [^18]; SWE-ABS found 19.71% of previously passing patches were semantically incorrect, dropping the top agent from 78.80% to 62.20% [^19]. Against that backdrop, the requirement for any "survives" verdict is specific: same fixed tasks, matched scaffold, sealed harness, cost reported alongside score, run by a party with no stake in either model.

## 04. The first independent test: one domain, one operator

The first genuinely outside measurement of the launch cycle arrived at 21:44 UTC, from a party selling neither model. Parametric CAD Bench, run by gNucleusAI, published four new model–agent results on the same 100 tasks it had run 90 days earlier: Claude Opus 5 via Claude Code is #1 at 0.906 — the first result above 0.9 on the benchmark — and Grok 4.6 via Grok Build reaches 96.9% of that score at 61% of the cost [^8][^26].

:::exhibit(num="Exhibit 1", title="Same tasks, 90 days apart: what a fixed capability level now costs", subtitle="Parametric CAD Bench, 100 tasks; best score and cost to exceed 0.8", source="Parametric CAD Bench via @gNucleusAI; ARA analysis", note="All four new entries ran within the same release window; the 61%-of-cost ratio for Grok 4.6 is relative to the Opus 5 run.")
| Metric | ~May (90 days prior) | 2026-08-12 |
|---|---|---|
| Best score | 0.832 (GPT-5.5) | 0.906 (Opus 5) |
| Cost to exceed 0.8 | $170.00 | $36.59 (Grok 4.5) |
:::

The two most important numbers are the ones that measure the same workload twice. Best score moved from 0.832 (GPT-5.5) to 0.906 (Opus 5). Cost to exceed a 0.8 bar moved from $170.00 to $36.59 — a 4.6x deflation in what a given capability level costs, measured on fixed work rather than on a moving benchmark [^8][^26]. The operator's own summary of the tail is the sharpest line in it: the weakest of the four new entries would have ranked #1 in May [^8][^26].

Three caveats travel with the result, and two of them bound its force. First, gNucleusAI sells engineering-AI tooling and is the only party running these tasks; its post carried almost no engagement and had no adversarial scrutiny — the "vendor benchmark by another name" objection has real weight [^8][^26]. Second, the ratio is worse than the sticker: $2/$6 implies roughly an 80% cost advantage on input, and the measured 61% is a haircut from that — the discount survives contact with real work at a slightly worse rate than the price card promises [^8][^26]. Third, and most important for durability, the measurement conflates model and harness: Grok 4.6 was scored inside Grok Build, Opus 5 inside Claude Code, and the 0.906 crown goes to Anthropic while the efficiency crown goes to xAI — which is exactly why it does not flatter one lab, and why the ratio between two of its own runs is the measurement least sensitive to the operator's choices [^8][^26]. What it does not speak to at all is the long-horizon reliability gap flagged by Grok's own friendly witnesses — the subject of the next section.

:::rank-list
- {label: "Claude Opus 5 (Claude Code)", value: "0.906 — 100% of top", pct: 100}
- {label: "Grok 4.6 (Grok Build)", value: "~0.878 — 96.9% at 61% cost", pct: 97, highlight: true}
- {label: "Best 90 days prior (GPT-5.5)", value: "0.832", pct: 92}
:::

:::source
Parametric CAD Bench, 100 fixed tasks, rerun 2026-08-12; Grok 4.6 score derived by ARA from the published 96.9% ratio [^8][^26].
:::

## 05. The three things the composite hides

The most damaging critique of the launch came from inside the enthusiasm. @scaling01, an account that had spent the afternoon posting Grok's benchmark wins, wrote at 17:59 UTC that on "really long-running and autonomous workflows … the best OpenAI and Anthropic models are much better in the tails" [^7][^26]. A composite intelligence index and a single-number agentic ranking both average many short runs, and neither can capture the failure mode that matters most for production agents: whether the model stays coherent and on-task after hours of autonomous work. That is precisely where the CAD bench — a few hundred focused engineering tasks — cannot testify.

:::quote(attr="@scaling01, 12 August 2026")
Really long-running and autonomous workflows… the best OpenAI and Anthropic models are much better in the tails.
:::

The second thing the numbers hide is that every cost-aware measurement in the cycle so far is a model-plus-harness score. CursorBench is Cursor's own harness, and Grok 4.6 ships inside Cursor [^1][^16]. The CAD bench measured Grok Build against Claude Code [^8]. Nobody has yet run Grok 4.6 against Fable 5 Max on a single matched scaffold with a sealed harness — the standard this market has required since the reward-hacking audit [^17][^19]. The switching that practitioners reported on launch day — Grok Build "probably the best TUI from a lab", a post claiming to downgrade both Codex and Claude Code — is real, but it happened during a seven-day double-token promotion, which is exactly when trial is cheapest and retention untested [^11][^26]. @davis7, the launch's most detailed booster, closed his own thread with the correct prior: Grok 4.6 "feels very good on first tests… but time will tell as always. After Opus 5 I'm scared to make any big day 1 calls about a model" [^11][^26]. And the visible enthusiasm is partly an artifact of who posts: @mark_k noted that "Cursor employees are much more active on X than SpaceX folks. Much needed PR boost" [^12][^26].

The third thing is the price itself. The $2/$6 card is real, but so is the seven-day double-token promotion running to roughly 19 August — and a promotional card and a permanent one are different events [^26]. Whether the CAD-bench cost figures were measured inside the promotion window is an open question that the benchmark's own operator has not answered [^8][^26]. If $2/$6 is the promo price and something north of it is the permanent one, every cost-ratio in this article shifts on a known date. That is not a reason to discount the discount; it is a reason to date-stamp it.

## 06. The market-structure logic of a repriced frontier

Set Grok 4.6's card next to the field and the "repricing" stops looking like an xAI innovation and starts looking like a schedule. $2/$6 is exactly the price Alibaba put on Qwen3.8-Max nine days earlier [^20][^21]. DeepSeek V4 Pro priced an order of magnitude below that on the same afternoon [^26]. GLM-5.2 sits at $1.40/$4.40 under MIT weights [^22]. Fable 5 Max's $10/$50 was itself a 70% discount to GPT-5.5 Pro's $30/$180 when it launched [^23][^34], and Opus 5 shipped "near Fable 5" at roughly half Fable 5's token price [^32]. The price of a fixed capability level has been falling on a visible schedule all summer; Grok 4.6 is the closed-tier continuation of that curve, not its origin. The tracked frontier price for a 0.9-level capability on the GPQA benchmark has been essentially flat at the low end all August [^36].

What is new is the combination with xAI's unusual market position. xAI rents Colossus capacity to the labs it competes with — roughly $1.25B a month from Anthropic and about $920M a month from Google, above $2B a month combined — so it is simultaneously the landlord of Fable 5's training capacity and the seller of a five-times-cheaper rival [^33]. It has a distribution channel no other lab matching its price has: Grok 4.6 ships inside Cursor, whose employees are visibly promoting it, and xAI's own Grok Build [^1][^12]. And Musk is reportedly telling SpaceX staff that "AI revenue will exceed all other SpaceX revenue by September," against a Morgan Stanley sum-of-the-parts that prices Grok plus Cursor at roughly $12 a share versus about $127 for Starlink and launch [^26]. A frontier-tier model at one-fifth the input price shipping into Cursor is the mechanism that makes that arithmetic work — and the mechanism that makes the resulting revenue low-margin, which is precisely why the sell-side values it at a tenth of Starlink's multiple [^26].

The regulatory frame completes the picture. Fable 5 spent two weeks offline under a US export-control order in June and returned metered, reclassified and capped [^29][^31]. GPT-5.6 shipped as a government-gated preview [^34]. Grok 4.6 ships unrestricted at a fraction of both — a frontier-adjacent model priced like the open-weight tier, under no access regime at all. That is the Grok 4.5-era asymmetry argument — a powerful unrestricted model while the gated ones are locked down — now with a price tag attached [^30]. For Anthropic, approaching a reported September or early-October IPO, the question is sharper: if a rival posts 61 against Fable 5 Max's 62 on the composite, what exactly does the $10/$50 buy? The defensible answers — the tails, the safety metering, the export-cleared trust surface, distribution inside Claude Code — are real, but they are now priced against a competitor that just cut the input price by 80% [^7][^27][^31].

## 07. What would settle it

The evidence, in one paragraph: the price is confirmed, the near-parity is seller-framed, the one independent cost-aware test is favorable but thin, and the tail question is unanswered. None of that is a reason to reject the repricing; it is a reason to refuse to certify it. The claim that survives today is narrower than the launch framing: a frontier-adjacent model priced at $2/$6 holds up on one independent engineering benchmark at a slightly worse ratio than the sticker implies, and that benchmark covers one domain with one operator, inside a promotional window.

:::position(confidence=medium, horizon="2026-Q4")
stance: The repricing survives its first non-vendor cost-aware test on one domain, but 'survives' is not established — one operator, one harness pair, one week of promotional pricing, and an unmeasured long-horizon tail. The durable verdict waits on a second cost-aware harness, a post-promotion card, and a tail-reliability run.
consensus: The market treats the $2/$6 near-parity as effectively confirmed and reprices downstream expectations; the frontier tier's price benchmark has moved to Grok 4.6's card.
resolves: Whether xAI's permanent price after the seven-day promotion ends ~19 August; Artificial Analysis' published cost-to-complete for Grok 4.6 on its Intelligence Index; a long-horizon or tail-reliability measurement from any party; and whether Anthropic re-prices Fable 5 Max ahead of its reported autumn IPO.
:::

Four falsification tests would settle this properly. First, a second independent cost-aware harness — Artificial Analysis's cost-to-complete for Grok 4.6 on its own index is the obvious one, and it is the same metric that exposed GLM-5.2's verbosity tax and Qwen3.8-Max's $2,159.51 run [^15][^21][^22]. Second, a matched-scaffold head-to-head of Grok 4.6 and Fable 5 Max on one sealed harness, with DeepSWE and Terminal-Bench — the two boards where xAI concedes it trails — included rather than excluded [^17][^26]. Third, a long-horizon run: the tails critique is the one the composite cannot answer, and it is the one that decides whether the repricing holds for the agent workloads the industry is actually buying [^7][^26]. Fourth, the price card after 19 August [^26].

Until those four land, the honest scorecard is this: Grok 4.6 is genuinely the cheapest way to buy frontier-adjacent work on the one fixed workload anyone has measured it on, and genuinely unproven on the long-horizon work where its cheapest rival — Fable 5 Max — has its most defensible premium. The frontier was repriced before it was proven. That is the story.

:::note
Figures as of 2026-08-12. The GDPVal-AA v2 comparison uses the leaderboard published 2026-07-17; the Parametric CAD Bench results are single-operator and were published within Grok 4.6's seven-day promotional window [^8][^26][^28].
:::

:::references
- {id: 1, title: "Grok 4.6 launch — xAI benchmark table and availability", url: "https://x.com/testingcatalog/status/2087567672695275584", source: "X/Twitter — @testingcatalog relay", date: "2026-08-12"}
- {id: 2, title: "Grok 4.6 price card $2/$6 vs Fable 5 Max $10/$50", url: "https://x.com/rohanpaul_ai/status/2087594773389701616", source: "X/Twitter — @rohanpaul_ai", date: "2026-08-12"}
- {id: 3, title: "AA composite 61 vs 62; Agentic Index #1; GDPval 1753 / Briefcase 1577", url: "https://x.com/rohanpaul_ai/status/2087599380518097232", source: "X/Twitter — @rohanpaul_ai", date: "2026-08-12"}
- {id: 4, title: "Musk dates Grok 4.7 to 3-4 weeks; initial training complete", url: "https://x.com/elonmusk/status/2087584127042408907", source: "X/Twitter — @elonmusk", date: "2026-08-12"}
- {id: 5, title: "Musk: 'Grok 4.6 reaches 1753 ELO'", url: "https://x.com/elonmusk/status/2087565375739474306", source: "X/Twitter — @elonmusk", date: "2026-08-12"}
- {id: 6, title: "Investor pricing framing — 80%/88% discounts, Grok 4.7 forward info", url: "https://x.com/GavinSBaker/status/2087567239423676519", source: "X/Twitter — @GavinSBaker", date: "2026-08-12"}
- {id: 7, title: "Tails critique — 'much better in the tails'", url: "https://x.com/scaling01/status/2087608575631695899", source: "X/Twitter — @scaling01", date: "2026-08-12"}
- {id: 8, title: "Parametric CAD Bench 90-day rerun — Opus 5 0.906, Grok 4.6 96.9%/61%", url: "https://x.com/gNucleusAI/status/2087656449493307617", source: "X/Twitter — @gNucleusAI", date: "2026-08-12"}
- {id: 9, title: "Grok 4.6 model card released (announced by @leerob)", url: "https://x.com/RayFernando1337/status/2087655009051959698", source: "X/Twitter — relay", date: "2026-08-12"}
- {id: 10, title: "First outside read of the Grok 4.6 model card — DeepSearchQA, KernelBench", url: "https://x.com/scaling01/status/2087659885563384116", source: "X/Twitter — @eliebakouch via @scaling01", date: "2026-08-12"}
- {id: 11, title: "Practitioner switching and day-1 caution — @davis7", url: "https://x.com/davis7/status/2087634913571090690", source: "X/Twitter — @davis7", date: "2026-08-12"}
- {id: 12, title: "Visible enthusiasm as a PR artifact — @mark_k", url: "https://x.com/mark_k/status/2087623035666755923", source: "X/Twitter — @mark_k", date: "2026-08-12"}
- {id: 13, title: "Grok 4.6 selectable in Hermes Agent — first third-party agent distribution", url: "https://x.com/Teknium/status/2087642281474249062", source: "X/Twitter — @Teknium", date: "2026-08-12"}
- {id: 14, title: "Artificial Analysis — model leaderboards", url: "https://artificialanalysis.ai/leaderboards/models", source: "Artificial Analysis", date: "2026-08-12"}
- {id: 15, title: "Artificial Analysis — model profiles with cost-to-run", url: "https://artificialanalysis.ai/models", source: "Artificial Analysis", date: "2026-08-12"}
- {id: 16, title: "CursorBench leaderboard — cost per task", url: "https://cursor.com/cursorbench", source: "Cursor", date: "2026-06-26"}
- {id: 17, title: "Reward hacking is swamping model intelligence gains", url: "https://cursor.com/blog/reward-hacking-coding-benchmarks", source: "Cursor Research — Naman Jain", date: "2026-06-25"}
- {id: 18, title: "SWE-Bench+: Solution leakage analysis", url: "https://arxiv.org/abs/2410.06992", source: "arXiv — Aleithan et al.", date: "2024-10-09"}
- {id: 19, title: "SWE-ABS: Adversarial benchmark strengthening", url: "https://arxiv.org/abs/2603.00520", source: "arXiv — Yu et al.", date: "2026-02-28"}
- {id: 20, title: "Qwen3.8-Max launch — 2.4T/95B at $2/$6", url: "https://qwen.ai/blog?id=qwen3.8", source: "Qwen (Alibaba)", date: "2026-08-03"}
- {id: 21, title: "Qwen3.8-Max model profile — cost-to-complete, verbosity", url: "https://artificialanalysis.ai/models/qwen3-8-max", source: "Artificial Analysis", date: "2026-08-04"}
- {id: 22, title: "GLM-5.2 is the new leading open-weights model on the Artificial Analysis Intelligence Index", url: "https://artificialanalysis.ai/articles/glm-5-2-is-the-new-leading-open-weights-model-on-the-artificial-analysis-intelligence-index", source: "Artificial Analysis", date: "2026-06-17"}
- {id: 23, title: "Claude API pricing", url: "https://platform.claude.com/docs/en/about-claude/pricing", source: "Anthropic", date: "2026-08-12"}
- {id: 24, title: "OpenAI API pricing", url: "https://platform.openai.com/docs/pricing", source: "OpenAI", date: "2026-08-12"}
- {id: 25, title: "Kimi K3 chat pricing", url: "https://platform.kimi.ai/docs/pricing/chat-k3", source: "Moonshot AI", date: "2026-08-12"}
- {id: 26, title: "ARA Twitter/X AI Pulse — 2026-08-12 (all cycles)", url: "/research/twitter/2026-08-12.md", source: "ARA research corpus", date: "2026-08-12"}
- {id: 27, title: "ARA daily digest — 2026-08-12", url: "/research/digest/2026-08-12-digest.md", source: "ARA research corpus", date: "2026-08-12"}
- {id: 28, title: "GDPval-AA v2 leaderboard — Fable 5 Max 1,815; GPT-5.6 Sol Max 1,747.8", url: "/research/2026-07-17-ai-news.md", source: "ARA research corpus", date: "2026-07-17"}
- {id: 29, title: "The first model-level export control: the Fable 5 suspension", url: "/research/generative/2026-06-13T065002--us-export-controls-reach-a-frontier-model-anthropic-s-forced.html", source: "ARA generative research", date: "2026-06-13"}
- {id: 30, title: "Grok 4.5 and the hardware-shielded frontier", url: "/research/generative/2026-06-29T045739--grok-4-5-spacex-s-monthly-from-scratch-1-5t-v9-cadence-and-t.html", source: "ARA generative research", date: "2026-06-29"}
- {id: 31, title: "ARA wiki — Claude Fable 5 / Mythos 5 (pricing, metered relaunch, Remote Labor Index)", url: "/research/wiki/entities/claude-fable-5.md", source: "ARA wiki", date: "2026-08-03"}
- {id: 32, title: "ARA wiki — Claude Opus 5 (near-Fable-5 at half the token price)", url: "/research/wiki/entities/claude-opus-5.md", source: "ARA wiki", date: "2026-08-03"}
- {id: 33, title: "ARA wiki — xAI (compute landlord, Grok cadence, Pareto-frontier claim)", url: "/research/wiki/entities/xai.md", source: "ARA wiki", date: "2026-08-12"}
- {id: 34, title: "ARA wiki — GPT-5.6 (Sol $5/$30, gated preview)", url: "/research/wiki/entities/gpt-5-6.md", source: "ARA wiki", date: "2026-08-11"}
- {id: 35, title: "Qwen3.8-Max: the three claims and what survives an audit", url: "/research/generative/2026-08-03T212425--qwen3-8-max-alibaba-s-2-4t-95b-flagship-at-2-6-the-first-max.html", source: "ARA generative research", date: "2026-08-03"}
- {id: 36, title: "ARA pricing dashboard — frontier price at fixed capability", url: "/research/market/model-pricing.json", source: "ARA pricing lane (Epoch AI / OpenRouter)", date: "2026-08-12"}
:::
