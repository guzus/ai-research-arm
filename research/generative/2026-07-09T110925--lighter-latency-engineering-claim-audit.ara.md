---
eyebrow: ANALYSIS · PERP DEX INFRASTRUCTURE
title: Lighter's microsecond story is really a systems-boundary story
deck: |
  Lighter says it flattened end-to-end p99 to roughly 55 ms while processing
  hundreds of millions of daily transactions. The numbers are self-reported,
  but the architecture lesson is independently legible: keep proving, custody,
  execution, and client-facing reads on different latency budgets.
lede: |
  On 8 July 2026, Lighter published a long-form engineering note claiming that
  its end-to-end p99 fell from roughly 280 ms to 55 ms, transaction processing
  p99 moved from 20-30 ms spikes to under 1 ms, and hot-path apply time now sits
  around 100-250 us. It also claimed an 811 million transaction day on 5 June
  2026, averaging 9,388 TPS with peaks of 20,740 TPS. Treat those performance
  numbers as company-reported until independently reproduced. The more durable
  insight is architectural: a trading venue can expose CEX-like latency only if
  the user-facing execution path is not waiting on proof generation, L1
  settlement, cold storage reads, garbage collection, or scheduler jitter.
domain: general
stats:
  - {label: Claimed e2e p99, value: 55 ms, note: "from ~280 ms"}
  - {label: Claimed tx p99, value: "<1 ms", note: "from 20-30 ms spikes"}
  - {label: Claimed apply time, value: "100-250 us", note: "hot path"}
  - {label: Claimed daily txs, value: 811M, note: "2026-06-05"}
  - {label: L2BEAT type, value: "ZK Rollup", note: "Stage 0 appchain"}
---

The headline version is simple: Lighter says it cut the tail latency of a live
perpetuals exchange from hundreds of milliseconds into a roughly 55 ms p99 band
while sustaining very high transaction throughput on mainnet.[^1] The first
principles version is more useful. A perp exchange has at least four clocks:
the trading clock, the API/read clock, the proof clock, and the Ethereum
settlement clock. If those clocks are coupled, the slowest one dominates. If
they are decoupled with explicit safety boundaries, the trader can receive a
fast soft-confirmed experience while proofs and L1 state roots catch up on a
separate budget.[^1][^2][^3]

:::callout(kind=info, label="Bottom line")
- {accent}The latency metrics are self-reported.{/} The 55 ms p99, sub-1 ms transaction p99, 100-250 us apply time, and 811M transaction day all come from Lighter's own post.[^1]
- {accent}The rollup architecture is externally supported.{/} L2BEAT classifies Lighter as an application-specific ZK rollup, and zkSecurity describes Lighter state transitions as verified and finalized on L1 with zero-knowledge proofs.[^2][^3]
- {accent}The engineering lesson is not just "write faster Go."{/} The post describes cache immutability, allocation reduction, CPU pinning, NUMA placement, binary serialization, and loadtest observability as one latency system.[^1]
- {accent}The unresolved question is fairness under a fast sequencer.{/} A centralized sequencer can be fast; the hard question is what users can verify or escape when the operator is slow, censoring, or wrong.[^2][^7]
:::

## 01. Separate what is claimed from what is checkable

Lighter's article is primary evidence for what Lighter says it achieved. It is
not, by itself, independent proof of the latency distribution. The post reports
that end-to-end p99 on the `order_book` WebSocket path dropped from 200-280 ms
spikes to a flat 50-60 ms band, that execution-engine GC duration fell toward a
roughly 10 us band after `GOGC` tuning, and that transaction processing p99
mostly stayed under 1 ms after the change.[^1] Those are precise metrics, but
the underlying dashboards and raw samples are not public in the post.

What is independently corroborated is the broad security architecture. L2BEAT
lists Lighter as an exchange-purpose ZK rollup and marks it as a Stage 0
appchain.[^2] zkSecurity's public report describes an L2 exchange whose state
transitions are verified and finalized on L1 by zero-knowledge proofs; it also
describes the data published to L1 as part of the recovery story if the service
stops operating normally.[^3] Blockworks' launch coverage gives the same
high-level split: centralized sequencing and matching for performance, Ethereum
contracts for custody/state roots, and validity proofs for state advancement.[^5]

:::kv
- {term: "Self-reported by Lighter", def: "55 ms p99, sub-1 ms tx p99, 100-250 us apply time, 811M transaction day"}
- {term: "Externally supported", def: "ZK rollup classification, Ethereum settlement, ZK circuit/security architecture"}
- {term: "Still opaque", def: "Raw latency histograms, independent p99 reproduction, exact load mix on the 811M-tx day"}
:::

That distinction matters because crypto infrastructure teams routinely confuse
throughput marketing with production reliability. If a venue cannot show the
measurement path, the correct posture is not disbelief; it is source labeling.
The metric can be operationally interesting while still carrying a "company
reported" tag.

## 02. The real architecture is latency-budget isolation

The most important sentence in Lighter's post is not the TPS claim. It is the
claim that proof generation is asynchronous and does not block trading.[^1] In
rollup terms, this is the product trade: the user-facing exchange gives a fast
sequencer acknowledgement, while the slower cryptographic proof and Ethereum
finalization path provide eventual settlement guarantees.[^2][^3]

That makes Lighter closer to a low-latency exchange with a cryptographic audit
and escape layer than to a conventional EVM DEX where each trade waits for block
production and state inclusion. Lighter's docs reflect that product split in a
different way: account type can affect API trading latency, with Standard
Accounts showing explicit taker, maker, and cancel latency values, while Premium
Accounts can receive lower latency tiers.[^4]

:::statement(attr="ARA Research")
The operating lesson is to put every subsystem on the clock it deserves: API
reads in memory, execution on pinned hot paths, proofs off the trading path, and
Ethereum settlement as the canonical backstop.
:::

This is also why the "decentralized exchange" label is too coarse. A smart
contract AMM, a decentralized order book, a CEX, Hyperliquid, and Lighter all
make different choices about custody, ordering, execution, latency, and exit
rights. L2BEAT's Lighter-versus-Hyperliquid analysis frames the key difference
as settlement domain: Hyperliquid is a standalone L1, while Lighter posts
validity proofs to Ethereum, a chain the Lighter operator does not control.[^7]

## 03. Go was not the thesis; tail control was

Lighter's engineering list reads like a checklist for reducing tail latency in a
garbage-collected, high-throughput matching stack: remove deep copies, replace
heap-heavy numerics on hot paths, pre-size collections, reuse buffers, tune
`GOGC`, keep complete exchange state in memory, pin critical goroutines to OS
threads, set CPU affinity, use high-priority scheduling, avoid NUMA remote
memory, and replace reflection-heavy serialization with fixed binary codecs.[^1]

The first-principles reason these changes work is not language-specific. Tail
latency comes from variance: GC pauses, allocator churn, cache misses, scheduler
wakeups, cross-NUMA memory reads, network round trips, serialization overhead,
and cold reads. A matching engine can have a good average and still be unusable
if a small fraction of orders land behind those stalls. Lighter's post is
interesting because it treats p99 as the product metric, not a post-hoc graph.[^1]

:::callout(kind=warn, label="What not to copy blindly")
Busy-wait loops, `SCHED_FIFO`, CPU affinity, and NUMA isolation are powerful but
dangerous. They trade spare CPU and operational complexity for lower jitter. The
move is justified only when the hot path is already understood, instrumented,
and isolated from unrelated workloads.[^1]
:::

For MEV, market making, and arbitrage systems, the useful takeaway is that
"faster RPC" is often the wrong bottleneck. If the process allocates on every
quote, rebuilds books on every tick, waits on a shared lock, or lets the OS move
critical work across cores, buying a better endpoint only hides the real tail.

## 04. Observability is part of the engine, not a dashboard afterthought

The post says Lighter runs an on-demand loadtest environment with identical
deployment topology, synthetic accounts, realistic trading load, extra timing
inside hot paths, CPU/memory/trace captures, Go flight recorder data, and
distributed traces.[^1] It also says mainnet monitoring focuses on freshness of
the `order_book` WebSocket path, dry-run latency, end-to-end transaction
lifecycle, and cache effectiveness.[^1]

That split is the right model. Production telemetry must stay cheap enough to
leave on permanently; loadtest telemetry can be expensive enough to expose the
micro-cause of a regression. If both environments share topology and configs,
operators can make a change under stress before real users feel it. If they do
not, the loadtest is theatre.

:::bars
- {label: "Trading clock", value: "soft confirmation and order-book freshness", pct: 95}
- {label: "API clock", value: "in-memory reads, dry-runs, WebSocket pushes", pct: 88}
- {label: "Proof clock", value: "async validity proof generation", pct: 62}
- {label: "Ethereum clock", value: "custody, state roots, exit backstop", pct: 45}
:::

The article's strongest operational claim is therefore not a single latency
number. It is that Lighter appears to have made latency an end-to-end lifecycle
metric, from submission through dry-run, execution, cache update, WebSocket
delivery, proof generation, and eventual settlement.[^1]

## 05. What this means for trading infrastructure

For an arbitrage or market-making operator, Lighter's post points to three
concrete design rules. First, keep quote state hot and immutable wherever
possible; readers should observe snapshots, not build them. Second, measure
freshness from the exchange state change to the strategy decision, not merely
from RPC response time. Third, label finality correctly: a fast exchange
acknowledgement, a sequencer-confirmed state, and Ethereum-settled finality are
not the same event.[^1][^2][^3]

The last point is the risk boundary. Lighter's external architecture sources
support the idea that assets and canonical state are anchored to Ethereum, but
L2BEAT still classifies the system as Stage 0, meaning users should not treat
the rollup as fully mature or governance-minimized.[^2] The latency story is
real enough to learn from; the trust story still needs the usual rollup risk
analysis.

:::callout(kind=success, label="Research conclusion")
Persist the Lighter post as a serious low-latency systems case study, not as a
fully independently verified benchmark. Its most transferable idea is the
systems boundary: decouple proof generation from trading latency, serve reads
from memory, attack p99 variance directly, and instrument the exact user-facing
freshness path.
:::

:::references
- {id: 1, title: "Chasing Microseconds: Lighter's Latency Engineering", url: "https://x.com/Lighter_xyz/status/2074905536122789917", source: "Lighter / X", date: "2026-07-08"}
- {id: 2, title: "Lighter - scaling project profile", url: "https://l2beat.com/scaling/projects/lighter", source: "L2BEAT", date: "accessed 2026-07-09"}
- {id: 3, title: "Public report of Lighter ZK circuits", url: "https://blog.zksecurity.xyz/posts/lighter-xyz/", source: "zkSecurity", date: "2024-04-24"}
- {id: 4, title: "Trading Fees", url: "https://docs.lighter.xyz/trading/trading-fees", source: "Lighter Docs", date: "accessed 2026-07-09"}
- {id: 5, title: "Lighter opens public mainnet with Ethereum-settled zk perps", url: "https://blockworks.com/news/lighter-opens-public-mainnet", source: "Blockworks", date: "2025-10-02"}
- {id: 6, title: "API Overview", url: "https://docs.growthepie.com/api-reference/api", source: "growthepie docs", date: "accessed 2026-07-09"}
- {id: 7, title: "Lighter vs Hyperliquid: Who has control over your collateral, orders, and exits?", url: "https://l2beat.com/publications/lighter-vs-hyperliquid", source: "L2BEAT", date: "2026-07"}
:::
