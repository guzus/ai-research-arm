---
eyebrow: RESEARCH · AI-ASSISTED SYSTEMS ENGINEERING
title: "50 ms to under 1 ms: what a Claude-written Python-to-Rust arbitrage rewrite proves, and what it can't"
deck: A trader's 34.5-billion-token Opus 5.5 rewrite is a clean test of three separate claims — about Python's tails, about on-chain latency economics, and about what LLM-driven translation costs.
lede: |
  On 2026-11-18 an X account that posts about DeFi and AI tooling said it rewrote its on-chain arbitrage scripts from Python to Rust in three days, spending roughly 34.5 billion Opus 5.5 tokens across two "Claude 20X" subscriptions, and now sees P99 tick-to-trade and tick-to-cancel latency below 1 ms against Python P99 "often above 50 ms".[^1] Each half of that sentence is checkable against first principles: whether a 50 ms-to-1 ms drop is mechanically plausible, whether it matters to profit on the venues where such bots trade, and what 34.5 billion tokens actually is in dollars, in agent-hours, and in verification burden. The answer is: plausible, venue-dependent, and expensive-but-subsidized — with the one number nobody can see being the test suite.
stats:
  - {label: Claimed P99 latency, value: "<1 ms", note: "vs. Python P99 often >50 ms"}
  - {label: Tokens burned, value: 34.5B, note: "self-reported, 3 days"}
  - {label: Implied average rate, value: "~133k", unit: "tokens/s", note: "derived, 72 h wall-clock"}
  - {label: List-price floor, value: "$6,900", note: "all cache reads; derived"}
---

:::kv
- {term: "Is 50 ms → <1 ms plausible?", def: "Yes for an internal software path: Python's GIL and cycle collector create tail pauses that a compiled, GC-free runtime avoids.[^4,5]"}
- {term: "Does it make money?", def: "Only where the rest of the path is already fast: a 50 ms Python tail equals one whole Jito auction tick, but only 0.42% of an Ethereum slot.[^8,10]"}
- {term: "Is the token bill plausible?", def: "Yes if the work ran as parallel agents on cache-heavy sessions; list price would be $6,900 at the very least, probably more, against $400 of subscription.[^2,23]"}
- {term: "What is unproven?", def: "Equivalence. Nothing public shows the Rust bot trades identically to the Python one; the author's own tweet reports latency, not P&L or fill parity.[^1]"}
:::

## 01. What was actually claimed

**The tweet is a latency claim plus a cost anecdote, not a trading result.** @LumaoDoggie, a verified account with about 21.5K followers whose bio describes a former big-tech programmer posting about DeFi, airdrops and AI, said the rewrite took three days of nonstop work, burned a large share of two Claude 20X plans plus "two usage resets", and produced P99 tick-to-trade and tick-to-cancel latency under 1 ms.[^1] The post carried one image whose content we could not retrieve; at fetch time it had about 16.5K views and 166 bookmarks.[^1] No venue, chain, strategy or hardware is named.

**What a named principal's tweet proves.** It is primary evidence for what the author said and believes. It is not evidence of the measurement method. "Tick-to-trade" conventionally means the time from receiving a market-data event to emitting an order; "tick-to-cancel" is the same for a cancel. Both are internal-path measurements that end at the process's network write, so they exclude exchange or sequencer processing, which is where most wall-clock time lives on any blockchain venue.

**The product naming has moved.** The author's "Claude 20X" most likely refers to the $200 tier, which Anthropic's pricing page now lists as Ultra at $200 per month with "10x Pro" weekly usage and no 5-hour limit for verified accounts, while Max is $100 at 5x.[^23] The "two usage resets" the author mentions are consistent with weekly-limit windows, which Anthropic raised 25% above their pre-promotion level on 2026-09-14 after a 50%-higher promotion that ran 2026-05-13 to 2026-09-13.[^20]

**Why this seed is worth expanding.** It bundles three things the market is currently confusing: a *language* claim (Rust beats Python), a *venue* claim (microseconds matter on-chain) and an *agent* claim (a model can port a trading system in three days). A single anecdote cannot establish any of them, but each has public evidence that does.

:::callout(kind=warn, label="Evidence status")
Only the tweet's text was retrievable; the authenticated X reader was not configured in this run, so the text came from a public mirror and the attached image was not read.[^1] Every number attributed to the author below is self-reported and unaudited.
:::

## 02. Why Python's tail is the mechanism, not its median

**Thesis: the 50 ms figure is a tail statistic, and tails are where Python's runtime design bites.** The Global Interpreter Lock "prevents multiple threads from executing Python code at the same time", which PEP 703 calls an obstacle to using multi-core CPUs efficiently.[^5] A trading process that decodes market data, evaluates a strategy and signs orders on one thread therefore queues work behind itself; any slow event delays every event behind it.

**The collector adds pauses that do not scale with the work being done.** CPython's reference counting is supplemented by a generational cycle collector whose collection starts when allocations minus deallocations exceed a threshold, with older generations examined less often.[^4] The standard library exposes `gc.disable()`, `gc.freeze()` and threshold setters precisely because collection timing is a tuning problem; 3.15 added `duration` and `candidates` to the collector's stats and callback info so collection time can be measured.[^4] A burst of allocation in a decoder can therefore trigger an older-generation sweep at the worst moment.

**The cheap alternatives exist, and the tweet doesn't say they were tried.** The free-threaded build removes the GIL but is optional, can re-enable it when an unready C extension is imported, and costs about 1% to 8% average overhead on pyperformance, depending on platform.[^6] PEP 703 measured 5–6% single-thread overhead on its test machines.[^5] Disabling the collector and freezing startup objects is documented for process-forking recipes.[^4] None of that gets a Python process to sub-millisecond P99 on its own, but it changes the baseline: "Python P99 often above 50 ms" may describe an untuned asyncio service rather than the language's floor.

:::stack-rows
categories: [Rust path, Python path]
rows:
  - {label: "Thread parallelism", values: [100, 0]}
  - {label: "Cycle collector pauses", values: [0, 100]}
  - {label: "Interpreter dispatch overhead", values: [0, 100]}
:::

:::note
Qualitative illustration only; the bars mark which stack carries each cost, not a measured magnitude. Python mechanics from the PEP 703 and `gc` documentation.[^4,5]
:::

**Counterpoint.** Rust removes the interpreter and the collector, not the other sources of tail latency: kernel scheduling, a noisy neighbour, lock contention, a cold cache or a TLS handshake. A sub-millisecond P99 is a claim about the whole machine, which makes the unreported hardware and isolation settings the main unknown. The mechanism explains why the direction is right; it cannot validate the magnitude.

**Why it matters.** Without a tuned-Python control, the experiment bundles "rewrite" with "rewrite plus finally measuring the tail". The 49 ms saved is real only if the old number was properly measured.

## 03. The latency ladder: where 49 ms is everything and where it is nothing

**Thesis: an internal speedup is worth exactly as much as the slowest unavoidable hop it sits beside.** Ethereum divides time into twelve-second slots with one proposer per slot.[^10] A 50 ms Python tail is 0.42% of that slot. On Jito's documented Block Engine path, parallel bundle auctions run at 50 ms ticks, so the same tail spans a whole auction round — the bot would miss the tick it was aiming for.[^8] That asymmetry is the whole economics of the claim.

:::rank-list
- {label: "Hyperliquid co-located end-to-end, P99", value: "900 ms", pct: 100}
- {label: "Hyperliquid co-located end-to-end, median", value: "200 ms", pct: 22}
- {label: "Base canonical block interval (since 2026-11-05)", value: "200 ms", pct: 22}
- {label: "Jito parallel-auction tick", value: "50 ms", pct: 6}
- {label: "Claimed Python P99 (before)", value: "50 ms", pct: 6, highlight: true}
- {label: "Claimed Rust P99 (after)", value: "<1 ms", pct: 1, highlight: true}
:::

:::note
Sub-second venue timings, as of 2026-11-18. Hyperliquid figures are its docs' co-located request-to-committed-response latency; Jito's is the documented auction tick; Base's is the post-Denim canonical block cadence. Ethereum's 12,000 ms slot is omitted for scale.[^8,9,10,12]
:::

**Hyperliquid is the likeliest home for "tick-to-cancel".** Cancels are meaningful on a central limit order book, and Hyperliquid's docs give a co-located median end-to-end latency of 0.2 seconds and a 99th percentile of 0.9 seconds, at roughly 200k orders per second.[^12] There, a 50 ms Python tail is 25% of the median round trip and 5.6% of the P99 — material for queue position, small relative to the venue's own variance. A secondary report puts median order-to-fill at about 884 ms from Tokyo and 1,079 ms from Ashburn, a gap near 195 ms, though it does not describe its methodology.[^24] Whether the venue is Hyperliquid is an inference: the tweet names none.[^1]

**Base removed one reason to be fast, and added another.** Base's docs say that at the Denim activation (Sepolia 2026-10-21, mainnet 2026-11-05) Flashblocks were replaced by a complete canonical block every 200 ms, so "there are no preconfirmed receipts" and integrations must poll canonical state instead.[^9] A bot built around pending-tag preconfirmation had to be rewritten that week regardless of language — a plausible confounder for a "rewrite from scratch" story, though the tweet does not link the two.

**Physics sets a floor the code can't touch.** Fiber carries light at about 200,000 km/s, so New York to London's 5,585 km costs 28 ms one way and 56 ms round trip on the idealized path.[^22] A Python P99 of 50 ms is therefore roughly one transatlantic round trip: eliminating it matters enormously to a bot colocated with the venue and little to one whose price source or block builder is an ocean away.

**Counterpoint and why it matters.** Colocation, not code, may have been the cheaper fix; the tweet doesn't say whether the bot's network position changed. Language speed and network position multiply, and an LLM-assisted rewrite only helps if the former was the binding constraint.

## 04. Does speed win the auction? What the on-chain evidence says

**Thesis: on-chain venues mostly sell ordering by price, so latency pays only where the rules still reward arrival time.** Flashbots' documentation describes searchers submitting bundles directly to builders and bidding by gas price or a direct coinbase transfer in a "first-price sealed-bid auction"; builders assemble the most profitable block and relays and validators pick the most profitable one.[^7] Selection is bid-driven, not arrival-time-driven — so a faster bot gains only through *which opportunities it can still see and price in time*, not through queue priority.

**Jito inverts that inside a short window.** Bundles hold up to five transactions executed atomically, compete on tips, and are ordered within a 50 ms auction by tip relative to requested compute.[^8] A bot that finishes inside the tick can bid; one that finishes after is in the next. That is where a 49 ms internal saving converts directly into opportunity count.

**Where races exist, the literature says latency spend competes the rent away.** Schlegel's game-theoretic model concludes that in the ex-ante stage bidders "invest into latency until they make zero profit in expectation".[^15] Arbitrum's Timeboost literally auctions a 200 ms ordering edge, and an empirical study of it finds bids are only "noisy predictors" of short-horizon CEX–DEX profit; after a resale intermediary (Kairos) appeared, paid bids fell from 62.7% to 14.8% of the top bid while total searcher profits stayed broadly similar.[^14]

**The profit pool is concentrated, which changes what a retail rewrite buys.** A 19-month study of Ethereum CEX–DEX arbitrage estimates $233.8M extracted by 19 major searchers across 7,203,560 arbitrages, with three searchers capturing about 75% of both volume and value.[^13] The same authors tie profitability to integration with block builders rather than raw code speed.[^13] On the supply side, two builders produced more than 85% of Ethereum blocks when measured.[^11]

:::donut(center-label="75%")
- {label: "Top 3 searchers (volume and value)", value: 75}
- {label: "Other 16 major searchers", value: 25}
:::

:::note
CEX–DEX arbitrage on Ethereum, August 2023 – March 2025 (as of study window end 2025-03-31); shares are approximate.[^13]
:::

**Counterpoint.** A small account may not be playing the Ethereum CEX–DEX game at all. Order-book venues and niche chains can have thin, less-contested edges where a 49 ms improvement is a bigger fraction of the competition's edge. And execution-quality research shows routing and block composition decide outcomes: about 21% of user transactions appeared in candidate blocks yet missed the winning block, and two arbitrage bots measurably changed which same- and opposite-direction swaps executed.[^16]

**Why it matters.** The tweet's latency number is necessary for some strategies and irrelevant for others. Without a P&L or fill-rate comparison, "better latency" is not "better arbitrage".

## 05. The token bill: 34.5 billion tokens, in dollars and in hours

**Thesis: 34.5B tokens is large but ordinary for agentic coding once cache reads are counted, and the subscription is the story.** Opus 5.5 lists at $4 per million input tokens, $20 per million output tokens and $0.20 per million cache-read tokens, with 5-minute cache writes at $5; Anthropic says typical workloads cost about 40% less than Opus 5, citing both lower prices and fewer tokens per task.[^2,3] Claude Code resends the full conversation with each request and bills it at the cached rate, so a long session's token count is dominated by re-reading context.[^21]

**The implied burn rate says "parallel agents".** Over 72 hours, 34.5 billion tokens is about 133,000 tokens per second sustained. A single sequential session cannot produce that on its own, so the figure implies several concurrent agents or very large contexts re-read on every call.[^1] Anthropic's own docs note that agent teams use roughly 7x the tokens of a standard session when teammates run in plan mode, and that thinking cannot be turned off on Opus 5.5 and bills as output.[^21]

:::bar-chart(title="Illustrative list-price cost of 34.5B Opus 5.5 tokens", subtitle="USD, as of 2026-11-18; assumptions in text", orientation=horizontal, value-unit=$)
categories: Two Ultra plans (1 month), All cache reads (floor), Mixed 95/3/1.5/0.5 (illustrative), Anthropic C compiler (Feb 2026)
Cost: 400, 6900, 17250, 20000
:::

:::note
Derived. Floor: 34,500 MTok × $0.20. Mixed: 95% cache reads, 3% 5-minute writes, 1.5% fresh input, 0.5% output, an assumption not reported by the author. Compiler bar is Anthropic's reported "just under $20,000".[^2,17]
:::

**Two bounds.** If every token were a cache read, list price would be $6,900; a plausible mixed profile (95% reads, 3% 5-minute writes, 1.5% fresh input, 0.5% output) gives about $17,250, a blended $0.50 per million.[^2] Against two $200-per-month subscriptions the floor alone is 17.25 months of fees.[^23] The author paid a flat price for what a metered customer would pay thousands for — a subsidy that depends on weekly limits staying where they are, and which Anthropic has already moved twice in 2026.[^20]

**A useful yardstick.** Anthropic's own C-compiler experiment used nearly 2,000 sessions, about 2 billion input and 140 million output tokens, and just under $20,000 on Opus 4.6.[^17] The tweet's 34.5B is about 16 times those 2.14B tokens, if the two counts are comparable (the author's count likely includes cache reads; Anthropic's lists input and output separately).[^17] Typical enterprise Claude Code use averages $13 per developer per active day, with 90% of users under $30.[^21] This was not typical use.

**Counterpoint.** The 34.5B figure is self-reported and its composition is unknown; if it was read from a usage tracker that counts cache reads as tokens, the dollar range above is right, but the "work done" implied is far smaller than the headline suggests. Tokens measure re-reading as much as thinking.

**Why it matters.** The cost of a port is now measured in plan limits, not salaries, which is why a solo trader can attempt it, and why the comparison against a human rewrite is mostly about verification time, not typing.

## 06. Can a model port a trading system faithfully?

**Thesis: translation quality is bounded by the verifier, and a trading bot's best verifier is replay.** Academic evidence on LLM code translation to Rust is sobering even if dated. The Fluorine study used differential fuzzing to check I/O equivalence and found the best of five LLMs translated 47% of benchmarks;[^18] RustRepoTrans built a repository-level benchmark of 375 tasks translating C, Java and Python into Rust, precisely because function-level benchmarks overstate how well models handle real project context.[^19] Both studies tested models far weaker than Opus 5.5, so their figures are historical floors on capability, not predictions.[^2]

**The strongest recent public datapoint is an optimistic one with a warning label.** Anthropic's agent-team C compiler in Rust passed 99% of the GCC torture tests and built Linux 6.9, but its output with all optimizations on was less efficient than GCC with none, and the author warned the task verifier must be "nearly perfect, otherwise Claude will solve the wrong problem".[^17] Passing tests, the post notes, can create a false sense that the job is finished.[^17]

**What a perfect verifier looks like for an arbitrage bot.** Record a day of market data and chain events; replay it through both the Python and Rust implementations; require identical decisions (what to quote, when to cancel, how much to size) and compare timing separately. Fluorine's differential approach is the same idea applied to function I/O.[^18] A rewrite that preserved latency while changing cancel logic by one tick would look like a win in the tweet's metric and a loss in P&L.

**The failure modes are domain-specific.** Floating-point versus fixed-point rounding in price and size, integer overflow in release builds, and silently different retry and timeout semantics between an asyncio client and a Rust async runtime all pass casual tests. None is documented in the tweet; all are standard review items for any port of this kind, which is an analytical judgment, not a sourced claim.

:::timeline
- {date: "2024-05", headline: "Fluorine", body: "Best of five LLMs translates 47% of benchmarks to Rust; differential fuzzing as the equivalence check."}
- {date: "2024-11", headline: "RustRepoTrans", body: "375-task repository-level benchmark for translating C, Java and Python into Rust."}
- {date: "2026-02", headline: "C compiler in Rust", body: "~2,000 sessions, ~$20k; passes 99% of torture tests, but slower than unoptimized GCC."}
- {date: "2026-09", headline: "Opus 5.5 ships", body: "$4/$20 per MTok; typical workloads ~40% cheaper than Opus 5."}
- {date: "2026-11", headline: "The tweet", body: "34.5B tokens, 3 days, P99 <1 ms claimed."}
:::

**Why it matters.** The rewrite's value hinges on a test artifact the author has not shown. If it exists, three days is a credible result. If it doesn't, the latency win is an unverified hypothesis about strategy parity.

## 07. What could break the thesis

**Thesis: the claim survives as a narrow engineering result; every broader reading needs more evidence.** The following would falsify or weaken it.

- **The baseline was untuned.** If the Python service used a single asyncio loop with default collector thresholds, much of the 50 ms may be recoverable with `gc.freeze()`/threshold tuning, process-per-core isolation or a native hot path, at a fraction of the effort.[^4,6]
- **The metric ends before the bottleneck.** Tick-to-trade excludes the venue; Hyperliquid's co-located P99 is 0.9 seconds and Ethereum's slot is 12 seconds.[^10,12] If the strategy is bound by those, the user-visible change is small.
- **The race is zero-sum and equilibrates.** Latency spending competes expected profit away, and on Timeboost the observed pattern was resale coordination, not a latency arms race that smaller entrants win.[^14,15]
- **The pool is concentrated.** Three searchers took about 75% of Ethereum CEX–DEX value; a retail bot's marginal 49 ms may not reach the same opportunities.[^13]
- **The subsidy is unstable.** Weekly limits have moved repeatedly in 2026, and list-price equivalent is at least $6,900 against $400 of fees; a repeat at metered price is a different business case.[^20,23]
- **Unobserved correctness regressions.** Latency parity without decision parity is the classic rewrite failure, and the tweet reports only latency.[^1,17]

:::callout(kind=info, label="Red-team status")
This run's adversarial pass is summarized in the findings file; where a top claim could not be falsified it is reported as surviving, and where evidence was thin it is labelled as inference above.
:::

## 08. Verdict and what to check next

**The defensible reading.** An AI-assisted Python-to-Rust port of a latency-sensitive loop in three days is credible given the model and the economics: the mechanism for the speedup is documented,[^4,5] the venue timing ladder says it matters most on fast-auction venues like Jito and least on slot-bound chains,[^8,10] and the token volume is consistent with parallel agent use at a subsidized flat price.[^20,21,23] What is not established is whether the Rust bot is *equivalent* or *more profitable*, and whether the same engineering would have come from tuning Python plus colocation.

**Five questions that would settle it, in order of cost:**

1. Which venue and chain, and where is the bot hosted relative to it?
2. What is the Python control after `gc` tuning and process isolation — the honest baseline?
3. What replay or differential test proves decision parity between the two implementations?[^18]
4. What are fill rate and net P&L per unit of risk before and after, on the same days?
5. What was the 34.5B token composition — cache reads, fresh input, output, thinking?[^21]

**Why this matters beyond one account.** The seed is a small, clean example of a general shift: the marginal cost of porting a performance-critical system has fallen to a few days of subscription limits, so the bottleneck moves to verification and to network position. The same shift lowers the barrier for every other searcher, which is exactly the condition under which latency rents compress.[^15]

:::references
- {id: 1, title: "@LumaoDoggie status 2122919849982820473 (via fxtwitter mirror)", url: "https://api.fxtwitter.com/LumaoDoggie/status/2122919849982820473", source: "X / fxtwitter", date: "2026-11-18"}
- {id: 2, title: "Introducing Claude Opus 5.5", url: "https://www.anthropic.com/news/claude-opus-5-5", source: Anthropic, date: "2026-09-22"}
- {id: 3, title: "Pricing — Claude API docs", url: "https://platform.claude.com/docs/en/about-claude/pricing", source: Anthropic, date: "2026-11-18"}
- {id: 4, title: "gc — Garbage Collector interface", url: "https://docs.python.org/3/library/gc.html", source: "Python docs", date: "2026-11-18"}
- {id: 5, title: "PEP 703 — Making the GIL optional in CPython", url: "https://peps.python.org/pep-0703/", source: "Python.org"}
- {id: 6, title: "Python support for free threading", url: "https://docs.python.org/3/howto/free-threading-python.html", source: "Python docs", date: "2026-11-18"}
- {id: 7, title: "Flashbots Auction overview", url: "https://docs.flashbots.net/flashbots-auction/overview", source: Flashbots, date: "2026-11-18"}
- {id: 8, title: "Low latency transaction send — Jito docs", url: "https://docs.jito.wtf/lowlatencytxnsend/", source: Jito, date: "2026-11-18"}
- {id: 9, title: "Flashblocks overview — Base docs", url: "https://docs.base.org/base-chain/flashblocks/overview", source: Base, date: "2026-11-18"}
- {id: 10, title: "Blocks — Ethereum developer docs", url: "https://ethereum.org/en/developers/docs/blocks/", source: ethereum.org}
- {id: 11, title: "Decentralization of Ethereum's Builder Market (Yang, Nayak, Zhang)", url: "https://arxiv.org/abs/2405.01329", source: arXiv, date: "2025-04-29"}
- {id: 12, title: "HyperCore overview — Hyperliquid docs", url: "https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/overview", source: Hyperliquid, date: "2026-11-18"}
- {id: 13, title: "Measuring CEX-DEX Extracted Value and Searcher Profitability", url: "https://arxiv.org/abs/2507.13023", source: arXiv, date: "2025-07"}
- {id: 14, title: "Just-in-Time Resale in an Ahead-of-Time Auction for Faster Execution", url: "https://arxiv.org/abs/2603.20175", source: arXiv, date: "2026-08-10"}
- {id: 15, title: "Transaction Ordering Auctions (Schlegel)", url: "https://arxiv.org/abs/2312.02055", source: arXiv, date: "2026-02-26"}
- {id: 16, title: "Becoming Immutable: How Ethereum is Made (Canidio, Pahari)", url: "https://arxiv.org/abs/2506.04940", source: arXiv, date: "2026-05"}
- {id: 17, title: "Building a C compiler with a team of parallel Claudes", url: "https://www.anthropic.com/engineering/building-c-compiler", source: "Anthropic Engineering", date: "2026-02"}
- {id: 18, title: "Towards Translating Real-World Code with LLMs: A Study of Translating to Rust", url: "https://arxiv.org/abs/2405.11514", source: arXiv, date: "2024-05"}
- {id: 19, title: "RustRepoTrans: Repository-level Code Translation Benchmark Targeting Rust", url: "https://arxiv.org/abs/2411.13990", source: arXiv}
- {id: 20, title: "Claude Code weekly limits promotion", url: "https://support.claude.com/en/articles/15910845-claude-code-may-july-2026-weekly-limits-promotion", source: "Anthropic Help Center", date: "2026-09-14"}
- {id: 21, title: "Manage costs effectively — Claude Code docs", url: "https://code.claude.com/docs/en/costs", source: Anthropic, date: "2026-11-18"}
- {id: 22, title: "Primer on Latency and Bandwidth — High Performance Browser Networking", url: "https://hpbn.co/primer-on-latency-and-bandwidth/", source: "O'Reilly / Ilya Grigorik"}
- {id: 23, title: "Claude plans and pricing", url: "https://claude.com/pricing", source: Anthropic, date: "2026-11-18"}
- {id: 24, title: "Hyperliquid latency: Tokyo edge (order-to-fill medians)", url: "https://en.cryptonomist.ch/2026/03/30/hyperliquid-latency-tokyo-edge", source: "The Cryptonomist", date: "2026-03-30"}
:::
