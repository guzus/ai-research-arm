---
eyebrow: ANALYSIS · AI EVALUATION · GAME BENCHMARKS
title: "Gemini 4 Neon, Hydrogen and Terra on a Sokoban eval: what one tweet does and does not establish"
deck: A 24-word post about a puzzle benchmark is a good test of how much a single leaderboard row can carry once you price the tokens behind it.
domain: software
lede: |
  On 2026-11-19 the developer banteg posted that Gemini 4 Neon "takes 4th place" in his Sokoban eval and that Hydrogen "has matched terra at 7.5x higher cost"[^1]. Both halves can be checked against public material, but only partly. The benchmark's methodology is published in detail[^2,3]; the list prices of the three models are published[^5,9,11]; the leaderboard numbers behind the tweet are not retrievable as static text. This article separates what is verified, what is arithmetic, and what is still an unverified single-source claim.
stats:
  - {label: Rooms in the eval, value: "66", note: "3 parts × 22 rooms"}
  - {label: Neon list price, value: "$3 / $15", note: "per M tokens in / out"}
  - {label: Hydrogen list price, value: "$1.50 / $7.50"}
  - {label: Terra list price, value: "$1 / $5"}
---

## 01. The direct answer

:::callout(kind=info, label="Short answer")
- **What the tweet says.** Neon is 4th on banteg's Sokoban leaderboard, and Gemini 4 Hydrogen reached the same result as GPT-6.1 Terra while costing 7.5 times as much.[^1]
- **What is confirmed.** The eval exists, its rules are public, and Neon, Hydrogen and Terra are all real, priced models released between 2026-10-26 and 2026-11-18.[^2,3,5,6,11]
- **What is not confirmed.** The 4th-place rank and the 7.5x ratio. The leaderboard renders client-side and the first-race write-up keeps no dollar accounting, so neither number could be reproduced from text.[^2,3]
- **What the 7.5x can and cannot be.** List prices make Hydrogen only 1.5x Terra per token, so a 7.5x bill means roughly five times the tokens, or a different cost basis.[^9,11]
:::

The question implied by the tweet is simple: *is Google's cheap tier actually cheap when it is made to think hard?* The answer depends on a gap between price per token and tokens per solved problem, and that gap is exactly what puzzle benchmarks with long reasoning chains expose. The tweet carries 13 likes, 1 reply and about 1,443 views at the time of the fetch used for this article, so it is a lightly circulated data point, not a consensus finding.[^1]

The tweet itself is the only evidence for its own two claims. It reports an observation by the author of the benchmark, which makes the author a primary source for what the eval shows. It is not independent corroboration of the underlying result, and this article treats it that way throughout.

## 02. What the Sokoban Eval measures

The benchmark is a long-horizon planning test with unusually explicit budgets, which makes its outputs interpretable but also makes cross-vendor comparison harder than a headline rank suggests.

The eval has models play Jonah Ostroff's *Heroes of Sokoban* trilogy: 66 rooms across three games of 22 rooms each, where clearing all 22 rooms of a game unlocks the next.[^3] Each model gets a board image, a text transcription of visible tiles, and any tutorial message; replies must be one JSON object such as `{"keys":"UULLDD"}`, and a reply can batch a route, switch heroes, undo or restart.[^3] The public site states one scored attempt per model, medium reasoning effort, and a budget per part of 5 hours of active time, 1,000 turns and 10,000 keys.[^2]

:::kv
- {term: Source puzzles, def: "Jonah Ostroff's Heroes of Sokoban trilogy, keys replayed in the original PuzzleScript game"}
- {term: Rooms, def: "66 (3 games × 22)"}
- {term: Attempts, def: "One scored run per model per condition"}
- {term: Reasoning effort, def: "Medium"}
- {term: Budget per game, def: "5 h active time, 1,000 turns, 10,000 keys"}
- {term: Conditions, def: "Keys only, or with a sandboxed Python notebook"}
- {term: Scoring, def: "Rooms cleared; time at the winning keypress for full clears"}
:::

Three design choices matter for reading any later result. First, **the budgets were raised after the first runs**: earlier presets were 45 minutes, 300 turns and 2,400 keys per game, and the keys-only race began at 2h15m, 600 turns and 4,800 keys before the limits were lifted.[^3] A result from before and after that change is not comparable. Second, **the harness changed**: the site notes that harness 0.2.0 counted time spent on requests that later failed, while retry pauses are otherwise excluded.[^2] Third, **the cost metric is not dollars**: the first-race write-up states that cost is measured in time, turns and keys, with no dollar accounting.[^3]

The third point bears directly on the tweet. A "7.5x higher cost" is a dollar-or-token claim, and the published methodology of the first race does not define one. Either a later harness version added token or dollar accounting (a KuCoin-relayed post from 2026-11-18 quotes dollar figures for two other models, "about $20" and "$52"[^4]) or the author computed the ratio off-site. The tweet does not say which.

Why Sokoban at all? The decision problem is PSPACE-complete (Culberson 1997; Hearn 2006) and NP-hard by earlier results, and a 20×20 maze has an estimated search space on the order of 10^98.[^13] One wrong push can make a room unsolvable many moves later, which is what makes it a planning test and not a pattern-completion test. Other groups use the same property: SokoBench evaluates long-horizon planning of reasoning models and pairs them with external PDDL planners,[^14] and lmgame-Bench converts games into benchmarks for 13 leading models, arguing that naïve game evaluations suffer from brittle perception, prompt sensitivity and contamination.[^15]

The counterpoint is that a game with one author, one scored run per model and a moving harness is a thin basis for ranking. The eval's own write-up concedes as much by publishing its contamination probe: Opus and Sol recognised the game and its author, Astra recognised it when only the warrior was named, and all 21 attempts to draw Part I room 18 from memory failed.[^3] That is evidence against memorised solutions, not proof of their absence.

This matters because a cheap-looking model's apparent parity or deficit on such an eval can come from budget, harness, refusal behaviour or genuine planning ability, and the headline rank cannot separate them.

## 03. The first race: where Terra and Argon actually landed

The only complete public table is the 2026-11-10 race, and it already shows that the cheap tiers sit in the bottom half of the field.

The first race ran eight models in two conditions and reported rooms cleared (out of 66).[^3]

:::bars
- {label: "Fable 5.2 — keys only", value: "66 (3:07:50)", pct: 100}
- {label: "Opus 5.5 — keys only", value: "66 (5:13:44)", pct: 100}
- {label: "GPT-6 Astra — keys only", value: "64", pct: 97}
- {label: "Sonnet 5.5 — keys only", value: "63", pct: 95}
- {label: "GPT-6.1 Sol — keys only", value: "51", pct: 77}
- {label: "Gemini 4 Argon — keys only", value: "43", pct: 65}
- {label: "GPT-6.1 Terra — keys only", value: "41", pct: 62}
- {label: "Haiku 5.5 — keys only", value: "3", pct: 5}
:::

:::note
Rooms cleared out of 66, keys-only condition, first race published 2026-11-10. Full clears show their time. Source: banteg, "Eight moves to the exit."
:::

With a Python notebook the order changed in ways that matter for tool-use comparisons: Fable 66 (2:12:07), Opus 66 (4:00:57), Astra 66 (4:32:42), Sol 66 (4:06:49), Argon 54, Terra 43, Sonnet 43, Haiku 16.[^3]

:::slope(left-label="Keys only", right-label="With Python", unit=" rooms")
| Model | Keys only | With Python |
|-------|-----------|-------------|
| GPT-6.1 Sol | 51 | 66 |
| Gemini 4 Argon | 43 | 54 |
| GPT-6.1 Terra | 41 | 43 |
| Sonnet 5.5 | 63 | 43 |
| Haiku 5.5 | 3 | 16 |
:::

Two readings follow. Terra was a bottom-three model in the first race in both conditions (41 and 43 rooms), so "Hydrogen matched Terra" is a statement about the lower half of the table, not about parity with the leaders.[^3] And Argon, the Gemini 4 tier that Neon replaces in the Gemini app,[^6] scored 43 and 54, so a Gemini-family model reaching 4th place would be a large jump over its sibling. The write-up also records that Argon lost 154 turns, 105 of them to filter blocks, which points to a harness or safety-filter interaction as a partial explanation of its score.[^3]

The counterpoint is that the models ran through different vendor harnesses (Codex, Claude Code or Antigravity), all at medium effort with built-in tools disabled, so vendor harness is confounded with vendor model.[^3] The write-up lists the harnesses but does not publish an ablation holding the model fixed across them.

This matters because "Neon is 4th" is only informative relative to who is above it. The first-race table leaves Fable, Opus, Astra and Sonnet ahead of any Gemini entrant in the keys-only condition, which is consistent with the tweet's rank but does not prove it, since the post-2026-11-10 leaderboard is not in the retrieved text.

## 04. Price per token: Hydrogen is 1.5x Terra, not 7.5x

Published list prices put Hydrogen only modestly above Terra, so a 7.5x total-cost gap must be driven by token volume, not price.

Hydrogen launched on 2026-11-12 and is positioned for everyday execution, replacing Flash in the Gemini app.[^6] Its direct standard price is $1.50 input and $7.50 output per million tokens, with cached input at $0.075.[^9,10] GPT-6.1 Terra, released 2026-10-26, is $1 input, $0.05 cached input and $5 output, with prompts above 272K input tokens billed at higher full-request rates, and Batch and Flex at half price.[^9,11] Press coverage frames Terra's price as half the rate of its predecessor.[^17,23]

:::compare
- {role: LOWEST, name: "GPT-6.1 Terra (output)", value: "$5 / M"}
- {role: SUBJECT, name: "Gemini 4 Hydrogen (output)", value: "$7.50 / M"}
- {role: HIGHEST, name: "Gemini 4 Neon (output)", value: "$15 / M"}
:::

On those numbers the unit-price ratio is 1.5 on both input and output (as of 2026-11-16 for Hydrogen and Terra).[^9] A reader who sees "7.5x higher cost" next to a $7.50 Hydrogen output price should at least notice the numerical coincidence. The tweet does not define its denominator and nothing retrieved shows the two are related, so this article does not infer that. It is a reason to ask the author for the cost basis, not a finding.

Arithmetic, labelled as analysis and not a sourced claim: if the unit-price ratio is 1.5 and the total-cost ratio is 7.5, then Hydrogen consumed about 5 times as many billed tokens as Terra on the eval (7.5 ÷ 1.5 = 5), assuming a similar input-to-output mix. Token-hungry behaviour on a trial-and-error puzzle is plausible, since the eval rewards undo and restart, but this is a hypothesis.

Independent evidence on how large the token gap usually is comes from Artificial Analysis-style task costs reported by a third-party review: Hydrogen at high effort scores 51 at $1.87 per task, Terra also scores 51 at $0.96 per task, a ratio of roughly 1.95, with Hydrogen faster (8.3 versus 14.2 minutes per task).[^10] Another review gives Hydrogen at xhigh a score of 54 at $3.16 per task.[^12] So at *matched score* on a broad agentic index the cost gap between Hydrogen and Terra is about 2x, which is not 7.5x.

That is not the right comparison for an eval that fixes the effort label instead of the score. Artificial Analysis's own comparison pages show the gap at matched *effort*: at xhigh, Hydrogen used 304M output tokens to run the index against 34.7M for Terra, roughly 8.8 times as many, and took 13.5 minutes per task against 6.4.[^25] Multiplying that token ratio by the 1.5x output-price ratio would give a cost ratio well above 7.5, so a 7.5x bill at the eval's fixed effort is entirely plausible in size. The red-team pass for this article found exactly this gap, which is why the sentence above is scoped to matched score.

:::stats
- {label: "Hydrogen cost / task (AA, high)", value: "$1.87", note: "score 51; as of 2026-11-16"}
- {label: "Terra cost / task (AA)", value: "$0.96", note: "score 51; 14.2 min / task"}
- {label: "Implied ratio on AA workload", value: "≈1.95", unit: "x"}
- {label: "Ratio claimed on Sokoban", value: "7.5", unit: "x", note: "unverified, single source"}
:::

If the Sokoban ratio is real, the puzzle workload is unusually unfavourable to Hydrogen: it thinks much longer per turn, needs more turns, or fails rooms and retries them. The first-race write-up shows how lopsided token-like costs get on this eval. Sol sent 2,778 keys in one reply and spent 9,475 keys on one Part III room that Opus cleared in 38, and Terra used 6,179 keys on Part II room 20, which Sonnet cleared in 101.[^3] Cost on this eval is dominated by a few rooms: five rooms took 38% of all play time.[^3] A single bad room can move a cost ratio by a large factor without changing anyone's general capability.

The counterpoint is that list price is not what an operator pays. Cached-input rates, batch discounts and aggregator reseller pricing differ widely (one reseller quotes both models at 70–85% below the direct price),[^9] and a Hydrogen run with implicit caching could be cheaper than the arithmetic above. The tweet gives no cache-hit information.

This matters because a cost ratio on a leaderboard is only comparable when the basis is stated: tokens billed, dollars at list, or dollars paid.

## 05. Neon in context: the model in 4th place

Neon is a plausible 4th-place model on a planning task because Google positions it as balancing depth and efficiency, but its own cost and speed profile is double-edged.

Google announced Neon on 2026-11-18. It is priced at $3 per million input tokens, $0.15 cached and $15 per million output tokens, with a 1M-token context window, and is described as sitting between Hydrogen and Carbon: Hydrogen for fast everyday execution, Carbon for the hardest long-horizon projects, Neon balancing depth and efficiency.[^5] Google reports Neon at 32% lower cost per task than Carbon at default high thinking.[^5]

:::timeline
- {date: "2026-10-26", headline: "GPT-6.1 Terra released", body: "$1 / $5 per M tokens, half its predecessor's rate."}
- {date: "2026-11-10", headline: "Carbon in the Gemini app; Sokoban race published", body: "banteg's first race: 8 models, 66 rooms."}
- {date: "2026-11-12", headline: "Gemini 4 Hydrogen", body: "$1.50 / $7.50 per M tokens; replaces Flash."}
- {date: "2026-11-18", headline: "Gemini 4 Neon", body: "$3 / $15; replaces Argon in the app."}
- {date: "2026-11-19", headline: "banteg posts Neon 4th, Hydrogen ≈ Terra", body: "The claim under review."}
:::

Independent trackers put Neon at 61 on the Artificial Analysis Intelligence Index at xhigh, with $6.44 per index task, about 21.5 minutes per task and a 56-second median time to first answer token, which the site itself labels notably slow against a 12.1-minute median.[^7] VentureBeat reports the same 61 and lists Carbon 60, Opus 5.5 59, Sol 57, Sonnet 55 and Hydrogen 54 on that index.[^8] Most benchmark figures in launch coverage were supplied by Google, and peer data predates release.[^8]

Neon's price is 25% under Opus 5.5 and 50% over Sonnet 5.5 and Sol, which VentureBeat calculates means Neon needs roughly one-third fewer tokens than those models to break even on cost.[^8] That token-efficiency requirement is the same variable that determines the Hydrogen-versus-Terra comparison: price per token is only half the cost equation.

On Sokoban, the relevant facts about Neon are limited. Its speed profile (long thinking at xhigh) interacts with the eval's 5-hour clock, and in the first race no finisher used more than 69% of the clock, while four of the ten runs that fell short ran out of clock.[^3] A slow-thinking model with a strong score would show up as a clean finisher with a large wall-clock total, while a slow-thinking model that stalls would show up as a clock failure. The tweet does not say which Neon was.

:::callout(kind=warn, label="Evidence gap")
The retrieved material contains no Neon row for the Sokoban eval. The rank "4th" is the author's statement and could not be matched to a leaderboard cell, a rooms-cleared count or a time.
:::

The counterpoint is reasoning-effort mismatch. The eval fixes medium effort,[^2] while Neon's headline index score comes from xhigh, where AA reports 61, versus 60 at high, 55 at medium and 44 at low.[^7] A gap of that size between medium and xhigh on a general index could be large on a planning task, so medium-effort Neon in 4th place says little about its best effort.

This matters because the ordering of mid-priced frontier models is decided by effort setting and harness as much as by the underlying weights.

## 06. Why token count, not list price, drives puzzle-benchmark cost

On trial-and-error tasks, cost per solved room is a product of unit price, reasoning tokens per turn, turns per room and failure rate, and each factor varies by an order of magnitude across models.

The first-race write-up gives concrete evidence for several of these factors. **Turns:** Fable's keys-only run used 4,384 keys, 13% over the reference composite of shortest clean solves, and cleared 32 rooms in a single reply, with no format rejections across 282 replies.[^3] **Failure rate:** Haiku wasted 398 turns refusing room four, which the author solved in 32 keys, and Sonnet burned 790 turns in one room, 381 of them refusals.[^3] **Wasted overhead:** Opus lost 2h 09m to 55 format rejections in the keys-only race and, in the Python race, spent 2h 54m on rejected replies against 52 minutes on accepted ones.[^3] **Tool use:** Python reduced Opus's time by 73 minutes and Fable's by 56 minutes, yet Sonnet fell from 63 to 43 rooms.[^3]

The relative-cost evidence from outside the eval points the same way. A dollar comparison relayed on 2026-11-18 reported Astra 6.2 finishing all 66 rooms about 33 minutes after Fable 5.2 for roughly $20 against $52, in 540 versus 198 turns.[^4] If accurate, a model taking 2.7 times as many turns still spent less than half the money, so turns and dollars are far from proportional. That source is a social-media post relayed by a news aggregator, and no absolute times were given, so treat it as low confidence.[^4]

:::rank-list
- {label: "Hydrogen vs Terra, claimed on Sokoban", value: "7.5x", pct: 100, highlight: true}
- {label: "Hydrogen vs Terra, AA task cost (high)", value: "≈1.95x", pct: 26}
- {label: "Hydrogen vs Terra, list price per token", value: "1.5x", pct: 20}
:::

:::note
Ratios are Hydrogen cost ÷ Terra cost. The 7.5x figure is from the tweet and is unverified; the other two come from a price page and a third-party review as of 2026-11-16.
:::

The first-principles takeaway: an eval's cost ratio between two models is a poor proxy for their price ratio, so a cost claim only means something with the denominator (tokens, dollars, turns) and the numerator (list, cached, batch) both stated. A second point is selection: on a game where rooms differ by orders of magnitude in difficulty, mean cost is dominated by a few catastrophic rooms. The write-up shows this directly, with the last Part II room alone taking 6h 50m of play time.[^3]

The counterpoint is that vendors design reasoning to be adaptive, and a model that thinks long on hard rooms and short on easy ones can be efficient overall; averaged cost would then understate its efficiency on the easy majority and overstate it on the tail.

This matters because buyers choosing between a "fast tier" and a "cheap tier" are choosing between two cost curves, not two prices.

## 07. What the Hydrogen–Terra comparison does and does not tell a buyer

Even if the 7.5x is accurate, it is a statement about one planning workload and says little about the typical agentic or coding task these tiers are sold for.

On suites that vendors and trackers publish, the two models trade wins. A reseller's compilation lists Hydrogen ahead of Terra on SWE-sweep (13.5% versus 5.8%), AutomationBench-AA (76.1% versus 60.2%), Vending-Bench 2 ($14,549 versus $9,107), HLE-Diamond (58.8% versus 47.3%) and Chartography (66.6% versus 63.2%), while Terra leads on Terminal-Bench-Science 0.1 (58.3% versus 51.4%).[^9] The same compilation warns that APIMaster did not run the benchmarks, that harnesses differ and that its cost table excludes retries and tools.[^9] A separate review concludes that Terra suits unattended batch work on cost, while Hydrogen is faster, with first answer token in 18.9 seconds against 164.7 seconds.[^10]

:::stack-rows
categories: [Hydrogen, Terra]
rows:
  - {label: "SWE-sweep (%)", values: [13.5, 5.8]}
  - {label: "AutomationBench-AA (%)", values: [76.1, 60.2]}
  - {label: "HLE-Diamond (%)", values: [58.8, 47.3]}
  - {label: "Terminal-Bench-Science 0.1 (%)", values: [51.4, 58.3]}
:::

The structure of those results suggests why a puzzle benchmark could diverge from them. Agentic suites reward tool use and short verified steps; Sokoban rewards holding a global invariant (no unrecoverable push) across hundreds of moves. A model strong at the first can be a high-variance performer on the second, and the Python condition in banteg's eval changes the picture again, since notebook access let Sol jump from 51 to 66 rooms while Sonnet fell from 63 to 43.[^3]

Which condition the tweet refers to is not stated. If the 7.5x is from the keys-only condition, token volume is the driver. If from the Python condition, notebook execution and failed cells (cells time out after four seconds; five players lost notebook state at least once) add another cost layer.[^3]

The counterpoint for buyers is that none of this makes the cost claim wrong; it makes it narrow. For a workload resembling a long-horizon planning puzzle, a cheap-per-token tier that consumes five times the tokens is not cheap, and that conclusion would hold regardless of the broader suites.

This matters because it converts a leaderboard curiosity into a procurement rule: pilot on your own workload and measure tokens per success, not just price per token.

## 08. Method: how to check the tweet's claims yourself

Both claims are checkable in principle, and a short protocol would settle them.

1. **Pull the leaderboard data.** The public site renders results client-side and showed only a loading message in the text fetch used here, so the ranking could not be read as text.[^2] The author's write-up and changelog are the authoritative places to look for the table after 2026-11-10.[^3]
2. **Fix the cost basis.** Ask whether "cost" is billed dollars from the provider, tokens at list price, or wall-clock. The first-race write-up measured time, turns and keys, not dollars, so a dollar figure is new information.[^3]
3. **Hold effort and harness fixed.** The eval uses medium effort and one scored run per model,[^2] so a single run's variance is unquantified. A second run per model would give a noise floor.[^3]
4. **Separate price from volume.** Report tokens billed, input and output separately, and cached versus uncached. Without that, the 7.5x cannot be decomposed into the 1.5x price ratio and a token ratio.[^9,11]
5. **Report rank with uncertainty.** A 4th place among a handful of models with one run each should carry a "± one position" caveat.

:::callout(kind=success, label="What would confirm the tweet")
A leaderboard row for Neon at rank 4 with a rooms-cleared count; a Hydrogen row with the same rooms-cleared count as Terra; and a stated cost basis in which Hydrogen's figure is 7.5 times Terra's.
:::

The counterpoint on the method itself: a single-author eval is a fast, transparent signal, and its openness (published rules, published budget changes, a "Frontier" challenge inviting humans to beat model routes)[^2] is a strength relative to closed vendor benchmarks. The weakness is the standard one for solo work: no replication, no confidence intervals, and a harness that changed between runs.

This matters because the discipline of stating the cost basis is what separates a useful leaderboard from an anecdote.

## 09. What could break the thesis

The strongest challenges to this article's reading are that the tweet is right and complete, that unit price is the wrong frame, or that the rank itself is an artefact.

- **The tweet may be fully correct.** Nothing retrieved contradicts either claim. Absence of evidence in a client-rendered page is not evidence of absence, and the author is the best-placed person to report his own eval.[^1,2]
- **Token volume may be the entire story, and may be a feature.** If Hydrogen's extra tokens bought extra rooms, the correct reading is "Hydrogen buys parity with Terra at five times the tokens", a quality-for-cost trade, not a defect. The tweet says "matched", which implies equal outcomes.[^1]
- **Harness effects may dominate.** Argon's 105 filter-blocked turns show a single vendor-specific interaction can cost 154 turns and a large part of a score.[^3] A Hydrogen run could suffer the same kind of problem.
- **Reasoning-effort normalisation is imperfect.** "Medium" is a vendor-defined setting, and Google exposes four thinking levels for Neon (Low to Extra High).[^6] Equal labels do not imply equal compute.
- **Prices move.** Carbon's $2/$10 rate is promotional through 2026-11-30 before moving to $4/$20,[^8] and Terra's long-context pricing changes beyond 272K input tokens.[^9] Any cost ratio is dated.
- **The source base is mostly secondary.** Several figures here (index scores, per-task costs, reseller prices) come from trackers, reviews and launch coverage that cite vendors, so they inherit those sources' errors. Explainers comparing the Gemini 4 tiers exist, but they largely restate Google's launch figures.[^20,21,22]

Red-team status: an adversarial pass was run inline by the orchestrating agent (not a separate sub-agent) on the three load-bearing claims. The list-price ratio survived: Hydrogen $1.50/$7.50 against Terra $1/$5 is repeated by independent price trackers.[^9,10,11,26] The "about 2x" cost gap was narrowed to matched score after Artificial Analysis's xhigh-versus-xhigh page showed a much larger token gap.[^25] Neon's index score of 61 agrees across Artificial Analysis and VentureBeat; an unrelated search surfaced only older Carbon scores (59 on 2026-10-28), which pre-date Neon and do not contradict it.[^7,8]

## 10. Conclusions and open questions

The defensible reading is narrow. The Sokoban Eval is a real, well-documented, single-author benchmark whose first public race placed Terra and Argon in the lower half of eight models and Fable, Opus and Astra at the top.[^3] Neon launched on 2026-11-18 as a mid-priced, slow-thinking model with strong general-index scores,[^5,7] which makes a 4th-place planning result plausible. The claim that Hydrogen matched Terra "at 7.5x higher cost" is the interesting one, and the public numbers bracket it: a 1.5x list-price ratio, a roughly 2x cost ratio at matched index score, and a token gap of about 8.8x at matched xhigh effort that would put the ratio at or above 7.5x.[^9,10,25] Which of those the eval's "medium" setting resembles is the finding to chase.

:::statement(attr="ARA Research")
A cost ratio on a leaderboard is a claim about tokens, not about price lists, and until the denominator is stated it cannot be compared with anything else.
:::

Open questions for the author or a replicator:

1. Which condition (keys-only or Python) and which harness version produced the 7.5x?
2. Is cost billed dollars, tokens at list, or a derived metric, and is caching included?
3. How many rooms did Hydrogen and Terra each clear, and how did the cost split between completed rooms and abandoned ones?
4. How stable is the 4th-place rank for Neon across repeated runs and at higher effort?

:::note(label="Methods note")
Research was done by the orchestrating agent directly: the tweet was read through a public mirror because the authenticated X client had no accounts configured; sources were fetched or searched in-session; the leaderboard could not be read as text. No sub-agent waves or verifier sub-agent were run in this execution, and the red-team pass was done inline by the same agent, not by an independent sub-agent. Claim-level support was checked by the author against the fetched pages, and unverified claims are marked as such in the text.
:::

:::references
- {id: 1, title: "banteg on X: gemini 4 neon takes 4th place in my sokoban eval", url: "https://x.com/banteg/status/2123449380921594315", source: "X / banteg", date: "2026-11-19"}
- {id: 2, title: "Sokoban Eval: Language models play Heroes of Sokoban", url: "https://soko.banteg.xyz/", source: "banteg", date: "2026-11-20"}
- {id: 3, title: "Eight moves to the exit", url: "https://banteg.xyz/posts/sokoban/", source: "banteg.xyz", date: "2026-11-10"}
- {id: 4, title: "Astra 6.2 also did pretty well on banteg's sokoban benchmark", url: "https://www.kucoin.com/news/insight/ASTRA/6afd4b109278e40007d87a20", source: "KuCoin News (relaying an X post)", date: "2026-11-18"}
- {id: 5, title: "Introducing Gemini 4 Neon", url: "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/", source: "Google", date: "2026-11-18"}
- {id: 6, title: "Google launches Gemini 4 Neon with Carbon quality at Flash speeds", url: "https://9to5google.com/2026/11/18/gemini-4-neon-announcement/", source: "9to5Google", date: "2026-11-18"}
- {id: 7, title: "Gemini 4 Neon: Intelligence, Performance & Price", url: "https://artificialanalysis.ai/models/gemini-4-neon", source: "Artificial Analysis", date: "2026-11-20"}
- {id: 8, title: "Google launches Gemini 4 Neon with Opus 5.5-level coding performance at 25% lower API token prices", url: "https://venturebeat.com/technology/google-launches-gemini-4-neon-with-opus-5-5-level-coding-performance-at-25-lower-api-token-prices", source: VentureBeat, date: "2026-11-18"}
- {id: 9, title: "Gemini 4 Hydrogen vs Sonnet 5.5 vs GPT-6.1 Terra", url: "https://apimaster.ai/blog/gemini-4-hydrogen-vs-sonnet-5-5-vs-gpt-6-1-terra", source: APIMaster, date: "2026-11-16"}
- {id: 10, title: "Gemini 4 Hydrogen review: benchmarks, cost per task, and verdict", url: "https://www.eesel.ai/blog/gemini-4-hydrogen-review", source: eesel, date: "2026-11-16"}
- {id: 11, title: "GPT-6.1 Terra launched with 50% lower API pricing for developers", url: "https://yourstory.com/ai-story/gpt-6-1-terra-lower-api-pricing-developers", source: YourStory, date: "2026-10-26"}
- {id: 12, title: "Gemini 4 Neon Pricing and Benchmarks: Is It Worth Using?", url: "https://www.mindstudio.ai/blog/gemini-4-neon-pricing-benchmarks", source: MindStudio, date: "2026-11-19"}
- {id: 13, title: "Sokoban", url: "https://en.wikipedia.org/wiki/Sokoban", source: Wikipedia}
- {id: 14, title: "SokoBench: Evaluating Long-Horizon Planning and Reasoning in Large Language Models", url: "https://arxiv.org/pdf/2601.20856", source: arXiv, date: "2026-01"}
- {id: 15, title: "lmgame-Bench: How Good are LLMs at Playing Games?", url: "https://arxiv.org/abs/2505.15146", source: arXiv, date: "2025-05-21"}
- {id: 16, title: "GPT-6.1 Terra Is OpenAI's Bet on Computer Use, at About a Ninth of Opus 5.5's Cost per Task", url: "https://www.buildmvpfast.com/blog/gpt-6-1-terra-computer-use-api-pricing-2026", source: BuildMVPFast}
- {id: 17, title: "OpenAI releases GPT-6.1 Terra at half the API price of predecessor", url: "https://www.siliconreport.com/openai-releases-gpt-6-1-terra-at-half-the-api-price-of-predecessor", source: "Silicon Report"}
- {id: 18, title: "Gemini 4 Neon: Google Takes Third Place in A.I. Rankings at a Discount", url: "https://www.trendingtopics.eu/gemini-4-neon-google-third-place-ai-rankings/", source: "Trending Topics", date: "2026-11"}
- {id: 19, title: "Gemini 4 Neon review: benchmarks, cost per task, and verdict", url: "https://www.eesel.ai/blog/gemini-4-neon-review", source: eesel, date: "2026-11"}
- {id: 20, title: "Gemini 4 Neon vs Hydrogen: Coding, Pricing, and Access", url: "https://myclaw.ai/blog/gemini-4-neon-vs-hydrogen", source: MyClaw, date: "2026-11"}
- {id: 21, title: "Gemini 4 vs Gemini 4 Neon: Four Models, One Confusing Name", url: "https://www.orcarouter.ai/blog/gemini-4-neon-vs-gemini-4", source: OrcaRouter, date: "2026-11"}
- {id: 22, title: "Gemini 4 Neon: The Balance Point Between Carbon and Hydrogen", url: "https://dev.to/uulab/gemini-4-neon-the-balance-point-between-carbon-and-hydrogen-benchmarks-api-pricing-and-4pa6", source: "DEV Community", date: "2026-11"}
- {id: 23, title: "OpenAI's GPT-6.1 Terra Enters Orbit with 50% Cheaper Tokens", url: "https://aimagazine.com/news/how-openais-gpt-6-1-terra-is-much-faster-and-50-cheaper", source: "AI Magazine", date: "2026-10"}
- {id: 24, title: "GPT-6.1 Terra API pricing: rates, cache fees and thresholds", url: "https://www.neoteo.com/en/gpt-61-terra-api-pricing-rates-cache-fees-and-thresholds", source: NeoTeo, date: "2026-10"}
- {id: 25, title: "Gemini 4 Hydrogen (xhigh) vs GPT-6.1 Terra (xhigh): comparison", url: "https://artificialanalysis.ai/models/comparisons/gemini-4-hydrogen-vs-gpt-6-1-terra-xhigh", source: "Artificial Analysis", date: "2026-11-20"}
- {id: 26, title: "Gemini 4 Hydrogen's $3 Workload Costs 1.5x GPT-6.1 Terra", url: "https://fourweekmba.com/ai-gemini-4-hydrogens-3-workload-costs-1-5x-gpt-6-1-terra/", source: FourWeekMBA, date: "2026-11"}
:::
