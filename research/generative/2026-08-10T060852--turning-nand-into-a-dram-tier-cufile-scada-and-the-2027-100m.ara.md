---
eyebrow: REPORT · MEMORY & STORAGE
title: The 512-byte misunderstanding
deck: NVIDIA's SCADA, Kioxia's 10-million-IOPS drive and the 2027 roadmap are real. The KV cache they are supposedly for is not the workload they were built for.
domain: semiconductor
lede: |
  In the first week of August 2026, at the Future of Memory and Storage summit in Santa Clara, NVIDIA open-sourced its cuFile APIs, named a framework called SCADA, and put a number in front of the storage industry: one hundred million IOPS from a single drive, at 512-byte granularity, on a PCIe 7.0 link. Kioxia shipped the first product on that path and rated it at ten million. The trade press converted this, within roughly seventy-two hours, into a story about turning NAND into a DRAM tier for KV-cache offload under the HBM shortage. That story is wrong in a specific and checkable way, and the way it is wrong tells you more about the 2026 memory market than the story itself does.
stats:
  - {label: Kioxia GP1, value: "10M", unit: "IOPS @512B", note: samples end-2026}
  - {label: Roadmap target, value: "100M", unit: IOPS, note: "PCIe 7.0, unbuilt"}
  - {label: vLLM offload block, value: "0.5–2", unit: MB, note: "~10³× a 512B unit"}
  - {label: 1Q26 DRAM contract, value: "+93–98%", note: QoQ}
  - {label: Flash vs HBM read energy, value: "26×", note: peer-reviewed}
---

## 01. The short answer

The premise deserves a direct response before the argument, because five of its six components survive scrutiny and one does not.

:::kv
- {term: "Is SCADA real?", def: "Yes. NVIDIA defines it as “scaled, accelerated data access”, a framework in which the GPU — not the host CPU — initiates and controls storage I/O. It descends directly from the 2022 BaM research paper. There is no published specification, no version number and no standards body."}
- {term: "Was cuFile open-sourced?", def: "Announced, yes. Delivered, not yet. As of 10 August 2026 the XIO-SIG GitHub organisation holds a single placeholder repository and no published code; the shipping cuFile v1.18 documentation still states that every API is issued from the CPU."}
- {term: "Is 100M IOPS a product?", def: "No. It is one forward-looking per-drive target for an unbuilt PCIe 7.0 generation. Every 100M-class result demonstrated so far is either an emulator or an aggregate across 32–44 drives. The best shipping drive is rated 5.5M."}
- {term: "Is there an HBM shortage?", def: "There is a DRAM shortage. Conventional DRAM contract prices rose 93–98% in a single quarter, and HBM per-wafer revenue was overtaken by DDR5 RDIMM in the same quarter — the reverse of the usual telling."}
- {term: "Is 512 bytes the KV-cache block size?", def: "No, and this is the load-bearing error. Real serving engines move 0.5–2 MB per KV block and have been growing that number, not shrinking it. 512 bytes is the size of a recommender embedding row and a GNN node feature."}
:::

Each of those five answers is sourced in the sections below: SCADA's definition and lineage,[^1,6] the state of the cuFile repositories and the CPU-issued API contract,[^92,2] the provenance of the 100-million-IOPS figure,[^9,10] the DRAM-versus-HBM price inversion,[^29,31] and the block sizes that serving engines actually move.[^17,54]

The claim that NAND is becoming a DRAM tier is not fabricated. NVIDIA is genuinely building toward it, Kioxia is genuinely shipping silicon toward it, and the economics of a 2026 memory market where a petabyte of DDR5 costs more than a thousand H200s genuinely demand it. But the specific architecture being pointed at — 512-byte random reads at extreme IOPS — was designed for graph neural networks, vector search and recommender embedding tables, and it arrived at the KV cache by way of a press extrapolation. NVIDIA's actual proposal for putting KV cache on flash is a different program, on different hardware, with a different unit of transfer, announced seven months earlier.

{accent}The distinction matters commercially{/}, because the two architectures have opposite requirements. One wants command-processing throughput and pays for it in controller silicon. The other wants bandwidth and capacity, and pays for it in Ethernet and RDMA. Buying the first to solve the second is how a memory-tier thesis becomes a write-off — which is what happened the last time, and cost Intel $559 million.[^46]

---

## 02. Anatomy of a number

The single most-repeated figure in this cycle is "100 million IOPS", and it is one number restated by four vendors as though each restatement were independent evidence.

Kioxia's own August 2026 press release is the honest version: it puts **10 million** random-read IOPS at a 512-byte block size in the headline for the GP1 Series, and puts 100 million in a forward-looking clause about "future generations".[^9] The GP1 is PCIe 6.0, NVMe 2.2, second-generation XL-FLASH, rated up to 50 DWPD — and evaluation samples reach select customers only "by the end of 2026", explicitly for functional checking, with production specifications subject to change.[^9] Kioxia's April 2026 roadmap page adds the missing detail: the 100 MIOPS figure attaches to a *second-generation* product at a PCIe 7.0 intercept, and the only demonstration of it — 107 MIOPS — ran on an emulation platform, not on silicon.[^10]

Everything else at the 100M level is an array.

:::rank-list
- {label: "Smart IOPS + H3 — 20-slot appliance (“designed to deliver”)", value: "1,000M", pct: 100}
- {label: "Micron — 44× 9650 Gen6 SSDs, 512B, SC25 demo", value: 230M, pct: 23}
- {label: "Kioxia — emulated device, not silicon", value: 107M, pct: 11}
- {label: "Graid — 32× Kioxia XD8, RAID-5 protected", value: 100M, pct: 10}
- {label: "Kioxia GP1 — per drive, 512B, samples end-2026", value: 10M, pct: 1, highlight: true}
- {label: "Micron 9650 — per drive, 4KB, shipping", value: 5.5M, pct: 0.55}
:::

Micron's 230 million IOPS is the largest published GPU-initiated result and it comes from forty-four Gen6 SSDs behind three Broadcom PCIe switches, scaling linearly from one drive to forty-four.[^7] Divide it out and each drive is contributing roughly 5.2M IOPS — against the 9650's headline rating of 5.5M random-read IOPS, a figure Micron's product page publishes without stating a block size.[^7,16] That arithmetic is the most instructive number in the dataset: **a Gen6 drive driven at 512 bytes lands within about 5% of its own headline IOPS rating.** Shrinking the request does not multiply the operation count, because the limit is the controller's command-processing rate rather than the link. Graid's 100 million is thirty-two Kioxia XD8s under RAID-5 — about 3.1M per drive, which is unremarkable; the news there is that parity did not cost throughput.[^13] Smart IOPS and H3's "up to one billion random IOPS" is twenty E3.S slots multiplied by a 50M-per-slot rating, in a press release whose own verb is "designed to deliver".[^14]

The 2027 date has a similarly thin provenance. It traces to Nikkei quoting a Kioxia chief engineer in September 2025, echoed in Kioxia's own roadmap as "an expected second generation release sometime in 2027".[^12,10] NVIDIA's published Storage-Next material states the goal without a public date. And the schedule risk is structural: PCI-SIG released PCIe 7.0 to members on 11 June 2025,[^15] while the first Gen6 datacenter SSDs only reached mass production in 2026 and Marvell's Gen6 controller was still "expected to begin sampling in Q4 2026" as of FMS.[^70] A Gen7 drive shipping in 2027 would be unusually fast by the industry's own recent cadence.

:::callout(kind=warn, label="Unit check")
100 million IOPS at 512 bytes is **51.2 GB/s of payload** — about one sixty-fifth of an H100's 3.35 TB/s of HBM bandwidth, and roughly one quarter of a PCIe 7.0 x4 link's practical read ceiling.[^15,82] The target is link-rate-matched by construction. It is a claim about *access granularity*, not about throughput, and anyone quoting it as evidence that flash is approaching memory bandwidth has misread the unit.
:::

Objective Analysis principal Jim Handy — a NAND analyst whose clients are the vendors making the claim — headlined a post "100 Million IOPS SSDs? You Must be Kidding!", noting that today's highest-performing SSDs deliver well under ten million. ==The headline is more sceptical than the analysis: Handy goes on to explain how Storage-Next gets there and calls it a real opportunity to reshape the SSD market.==[^47] A 2026 architecture paper from KAIST targeting exactly this roadmap is blunter still: enterprise SSDs support only about 3 MIOPS today, and the benefits of GPU-initiated storage "cannot yet be evaluated because the hardware is not commercially available."[^48] That is a chicken-and-egg gap, not a schedule.

---

## 03. Whose 512 bytes is this?

Here the evidence is unusually clean, because it consists mostly of things the vendors did *not* say.

NVIDIA's FMS 2026 announcement blog — the primary document for both SCADA and the cuFile open-sourcing — contains no mention of KV cache, embeddings, vectors, RAG, retrieval, graph analytics or recommenders in connection with SCADA, and states neither "512 bytes" nor any IOPS figure anywhere.[^1] It does name a KV-shaped workload exactly once, and it attaches it to a different product: "NVIDIA CMX Context Memory Storage provides an AI-native context tier for long-context, multi-turn, agentic AI inference."[^1] {accent}Context memory is CMX's job in NVIDIA's own sentence; SCADA's job is left unnamed.{/} Independent analysis of the same announcement reaches the same split, attributing the KV mission to CMX and "not to SCADA, Storage-Next, or cuFile."[^93]

The BaM paper that NVIDIA staff co-authored and that SCADA descends from is explicit about its target: "graph and data analytics, recommender systems, or graph neural networks", which "require fine-grained, data-dependent access to storage".[^6] It was posted in March 2022, before ChatGPT, and evaluated breadth-first search and connected components. Its measured configuration is the origin of the number: with 512-byte cache lines BaM achieved 85% of peak throughput at 17 MIOPS, against a 4KB configuration that saturated the PCIe link.[^6]

Kioxia's own FMS 2026 booth listing is the decisive artefact. It advertises three demonstrations on three different products:[^11]

| Demo | Product |
|---|---|
| *"10 million IOPS in 512-byte random read performance for near GPU Workloads"* | KIOXIA GP1 Series |
| *"Context Memory Caching for Maximizing AI Inferencing"* | KIOXIA CM9 Series |
| *"AI RAG: Improving Scalability for Vector Databases"* | AiSAQ software |

The vendor building the 512-byte drive assigns context-memory caching to a *different drive*. The GP1 press release itself never uses the words "KV cache", "vector", "embedding" or "inference"; its stated purpose is to "extend High Bandwidth Memory (HBM) as a fast flash memory media-based tier".[^9] Micron's SCADA blogs name graph neural networks and vector databases, and describe the 230M result as coming from a synthetic "SOL benchmark SCADA workload" — a speed-of-light measurement, not an application trace.[^7,8]

So where does 512 bytes actually come from? From workloads where an object genuinely is that size:

- **Recommender embedding rows.** Meta's Bandana paper states plainly that "user embedding vectors are only 64-128 B", against an NVM read granularity of 4KB, so that "the effective bandwidth is only 4% of the total bandwidth of the NVM, and the rest is discarded."[^54] Meta's later ZionEX production tables show embedding dimensions of 92, 93, 128 and 256 — which at fp32 land at 368, 372, 512 and 1,024 bytes.
- **GNN node features.** The GIDS paper, from the same NVIDIA/UIUC lineage as BaM, states that node feature size "typically ranges from 512B to 4KB" and sizes the GPU cache line to the embedding specifically to avoid I/O amplification.[^55] `ogbn-papers100M` carries 128-dimension features: at fp32 that is 512 bytes, exactly.
- **Quantised retrieval vectors.** A 768-dimension embedding at int8 is 768 bytes; a 1024-dimension one is 1KB. DiskANN's per-node payload — a degree-128 adjacency list plus a vector — is 384 to 1,024 bytes, and the paper rounds up to 4KB purely because in 2019 "reading 4KB-aligned disk address into memory is no more expensive than reading 512 B".[^56] That assumption is exactly what a 512-byte-optimised device would invalidate.

This is a coherent, valuable, well-motivated engineering program. It is simply not a KV-cache program.

:::callout(kind=info, label="Where the error entered")
StorageReview's FMS write-up — the most widely-cited secondary account — asserts that "embeddings run a few hundred bytes, and KV cache blocks are well under a kilobyte."[^3] The first half is right. The second half mistakes a *per-layer, per-token, per-head slice* for an I/O unit. No serving engine has ever moved KV at that granularity, and the gap between the claim and practice is three to four orders of magnitude. That one sentence is the hinge on which the popular version of this story turns.
:::

---

## 04. What a KV cache actually weighs

The arithmetic is short enough to do in full, which is why the error is worth correcting precisely rather than by assertion.

For a grouped-query-attention model the per-token KV footprint is `2 × layers × kv_heads × head_dim × bytes_per_element`. Llama-3.1-70B has 80 layers, 8 KV heads and head dimension 128, in bf16:

`2 × 80 × 8 × 128 × 2 = 327,680 bytes` — **320 KiB per token**, across the whole model.[^89]

A single token, a single layer and a single KV head is `2 × 128 × 2 = 512 bytes`. That is where the number comes from — and it is an *atom*, not a transfer. No engine issues I/O at that size, because doing so would mean 2,560 separate reads to reconstruct one token's cache.

What engines actually do runs hard in the opposite direction. vLLM re-laid-out its KV cache in January 2026 so that one physical block spans every layer, multiplying the offload block by `2 × num_layers`:

:::compare
- {role: LOWEST, name: "One token, one layer, one KV head (an atom, never an I/O)", value: 512 B}
- {role: HIGHEST, name: "vLLM new layout (all-layer physical block)", value: 0.5–2 MB}
- {role: SUBJECT, name: "vLLM old layout (per-layer block)", value: a few KB}
:::

In vLLM's own words, "the new vLLM KV cache layout yields a physical block size of about 0.5-2 MB, while in the old layout it is only a few KB" — and fragmentation, harmless for compute, "is devastating for KV offloading."[^17] The change delivered up to 4× TTFT and 5× throughput improvement across versions.[^17] llm-d, working the same problem from the file-system side, states that Llama-3.1-70B "requires 305 GB of KV-cache for one million tokens" — which reproduces the 320 KiB-per-token figure above to within a rounding error.[^18] Even the *old* vLLM layout never went below single-digit kilobytes.

The direction of travel is the whole argument. Every serving engine that has profiled KV offload has concluded that its problem is *too many small objects*, and has responded by making them larger. The Tutti paper measures the pathology directly: reloading a 128K-token KV for a 64-layer model at block size 64 requires fetching roughly 256,000 scattered ~80KB objects, and fixing the layout — not the device — took retrieval from 11.9 GB/s to 25.9 GB/s and cut TTFT 78.3%.[^20]

Architecture is also shrinking the footprint, though less than the headlines claim. DeepSeek's Multi-head Latent Attention compresses KV to `(d_c + d_h^R) × l` elements per token against multi-head attention's `2 × n_h × d_h × l`.[^19] Apply that formula to DeepSeek-V3's published shape — 61 layers, `kv_lora_rank` 512, `qk_rope_head_dim` 64, bf16 — and you get 68.6 KiB per token: a 57× reduction against MHA, but only about 3.6× against an 8-head GQA baseline at the same depth.[^90] ==Those three multiples are my arithmetic from the paper's own formula and V3's config; DeepSeek publishes no bytes-per-token figure.== The 93.3% number everyone quotes is measured against MHA, a baseline nobody has shipped in years. Hybrid linear-attention models go further — Qwen3-Next keeps full KV on only 12 of 48 layers[^84] — and DeepSeek-V4 reports needing 10% of V3.2's KV cache.[^83] But MiniMax publicly *reverted* M2 to full attention, citing immature infrastructure for linear and sparse attention,[^85] and DeepSeek's own sparse attention cuts compute while keeping every KV entry resident. Meanwhile context windows went from 128K to 1M over the same period, cancelling most of the per-token win.

The honest reading: KV blocks are megabytes and getting bigger; KV *volume* per token is shrinking and being spent immediately on longer contexts. Neither trend points at a 512-byte device.

---

## 05. The shortage is real. The diagnosis is not.

The economic pressure behind all of this is not in dispute. What is in dispute is which constraint is binding.

:::line-chart(title="Conventional DRAM contract price change, QoQ (range midpoints)", subtitle="TrendForce; 1Q26 is actual, 2Q26 and 3Q26 are forecasts, as of 2026-07-03", y-unit=%)
x: 4Q25,1Q26,2Q26,3Q26F
Contract price change: 20.5,95.5,60.5,15.5
:::

Conventional DRAM contract prices rose approximately 93–98% quarter-on-quarter in 1Q26 alone, lifting DRAM industry revenue 81% QoQ to $97 billion.[^29] Compounding the quarterly range midpoints gives roughly +260% from late 2025 through 3Q26 (==my arithmetic; TrendForce publishes the quarterly changes, not a compounded figure==), and the series is decelerating sharply — the 3Q26 forecast is 13–18%.[^30] HP told investors that memory and storage went from 15–18% of its PC bill of materials to roughly 35% in a single quarter, with memory cost up about 100% sequentially.[^35] Micron printed $41.456 billion of revenue at an 84.9% non-GAAP gross margin in FQ3 FY2026 and guided the next quarter to $50 billion,[^32] on DRAM bit shipments up only low single digits with ASPs up in the low sixties percent — a price event, not a volume one.[^32]

But the specifically-HBM part of the story does not hold up. TrendForce measures HBM per-wafer revenue as having been *overtaken* by DDR5 64GB RDIMM in 1Q26.[^31] HBM took roughly 22% of top-three DRAM wafer input at end-2026 while producing about 9% of DRAM bits — a real crowding-out mechanism, but one that TrendForce now expects suppliers to re-weigh as HBM pricing settles, rather than one driven by superior per-wafer economics.[^31] Packaging is not the gate either: JEDEC relaxed the stack-height limit from 720µm to 775µm, deferring hybrid bonding past HBM4 entirely, and the CoWoS supply-demand gap is narrowing from roughly 20% to 10% by end-2026.[^80] The binding constraint is front-end DRAM wafer and cleanroom capacity, and it does not clear before the second half of 2027.

:::stack-bar(legend=true)
- {label: "Memory", pct: 63}
- {label: "Logic", pct: 13}
- {label: "Packaging", pct: 15}
- {label: "Auxiliary", pct: 9}
:::

Epoch AI's bottom-up model puts memory at about 63% of AI-chip component cost in Q4 2025, up from about 52% in Q1 2024, with packaging *falling* from 19% to 15% over the same window.[^34] The demand side confirms the direction: OpenAI's COO named memory as the current bottleneck to expanding AI infrastructure,[^79] and NVIDIA is reported to be evaluating *reduced* HBM stacks for Rubin Ultra because 2027 wafer supply limits what can be allocated.[^36]

Here is the part that undercuts the flash escape hatch. NAND is not a cheap escape from a squeezed DRAM market: NOR flash and SLC NAND contract prices cumulatively rose more than 100% across the first half of 2026, with structural shortages expected to keep them rising through the second half.[^87] XL-FLASH is SLC-mode BiCS. Building an AI memory tier on it means competing for the most supply-constrained NAND category in the market, on mature nodes everyone else is converting away from — while NAND capex rises only about 5% against DRAM's 14%.[^58]

---

## 06. Three walls an interface cannot move

Strip away the roadmaps and three physical constraints remain, and they fail independently.

**Latency.** Kioxia specifies XL-FLASH at "a read latency of less than 5 microseconds", on a 128Gb SLC die with a 16-plane architecture and a 4KB page.[^21] DRAM's core latency is tens of nanoseconds. That is roughly a 60× gap, and it is NAND array sense time — not link time — so no interface change touches it. UCIe does not touch it, PCIe 7.0 does not touch it, and stacking does not touch it. The first OCP High Bandwidth Flash specification was announced on 4 August 2026, defining three bandwidth grades from about 0.4 TB/s to 3.0 TB/s and up to 512GB per stack over a UCIe interface. **The published announcement quotes no latency figure at all** — every number in it is bandwidth, capacity or packaging.[^33] HBF is a parallelism and packaging standard, and its own publishers do not claim otherwise.

The counter-intuitive finding is that this may not matter. Take the per-token prefill time implied by a 70B model on eight H100s — tens of microseconds — and a 128-token block affords a recompute budget in the low milliseconds, against NVMe access latencies in the hundreds of microseconds. That is one to two orders of magnitude of headroom, ==and it is my arithmetic rather than a published threshold; no paper I found publishes a universal break-even latency, and every system treats it as a runtime decision.== What the literature does establish is that the observed bottleneck is elsewhere: Tutti attributes GPU stalls to fragmented I/O and layout, and fixed them without changing the device.[^20] Latency was plausibly never the binding constraint — which makes the industry's choice of low-latency SLC media a curious answer to a question nobody asked.

**Energy.** A peer-reviewed IEEE Computer Architecture Letters analysis puts flash read energy at 102.4 pJ/bit against HBM3's 4.2 pJ/bit, for a total access path of 110.8 pJ/bit and roughly a 26-fold increase in access energy versus an HBM baseline.[^24] The authors' own stated threshold for viability is a 10× improvement in flash read energy — which no announced HBF or XL-FLASH product claims. Prefetching hides latency; it cannot hide joules. Two honest qualifiers: the figures are modelled rather than measured on a rig, and the workload studied is MoE *expert weights*, which are read-mostly and reusable. KV cache is write-heavy and largely single-use, so this is the charitable case, not the harsh one.

**Endurance.** This is the axis that actually binds, and there is now a measurement. StorageReview instrumented a real KV-offload deployment — four Blackwell GPUs, eight Solidigm D7-PS1030 drives, vLLM plus LMCache — and found the array running at roughly **3.2 drive-writes-per-day against a 3 DWPD rating**, while consuming about one twenty-eighth of available bandwidth. Their conclusion, in a test sponsored by the drive vendor: "Endurance is the constraint that defines this tier."[^26]

The same test is also the strongest available rebuttal to my framing, and it deserves the space. The 3.2 DWPD figure is a RAID10 artifact — "mirroring doubles what the media absorbs" — and StorageReview's own recommendation is RAID0, "cutting the media rate to about 1.6 DWPD, comfortably inside the rating."[^26] It argues that exceeding the rating would be disqualifying for primary storage but is acceptable here, "because the cache is disposable by design, and the failure mode of a worn drive is recompute, not data loss."[^26] That is a serious answer. And on 30 July 2026 ScaleFlux launched a KV-cache SSD platform claiming 7–10+ effective DWPD over five years using more than 200 FDP write streams — an explicit attempt to engineer the problem away.[^91] Kioxia's decision to rate GP1 at up to 50 DWPD points the same direction: the vendors know exactly what the write load is, and are pricing silicon against it.[^9] ==Endurance is therefore a design cost, not a physical impossibility — but it is a cost the $/GB comparisons in the next section systematically omit.==

:::bars
- {label: "Flash read energy vs HBM3 (pJ/bit)", value: "26×", pct: 100}
- {label: "XL-FLASH read latency vs DRAM core", value: "~60×", pct: 70}
- {label: "Bandwidth headroom in measured KV tier", value: "28× spare", pct: 12}
- {label: "Endurance headroom in same tier", value: "0.94× (over)", pct: 3}
:::

The pattern is consistent across all three axes: the device is never short of bandwidth, is comfortably fast enough on latency, and is at or past its limit on writes and energy. Every marketing number published in this cycle addresses the two axes that were not constrained.

---

## 07. The wrong denominator

The economic case is always made in dollars per gigabyte, and for a write-saturated tier that is the wrong unit.

The $/GB gap is real and large. Enterprise TLC NVMe runs roughly $0.58–0.83/GB and high-capacity QLC around $0.42/GB, against DDR5 RDIMM spot at $25–48/GB depending on whether you price the die or the module.[^71] The Tutti paper independently publishes rental rates of $0.0088/GB-hour for DRAM and $0.000082/GB-hour for NVMe — a 107× ratio that corroborates the street-price gap from an entirely different basis.[^20] For a thousand-GPU fleet, a petabyte of QLC is roughly $415,000 against $35 million of GPU capex; the same petabyte in DDR5 costs more than the GPUs.

Then endurance arrives. Take a Solidigm D7-PS1030 at 12.8TB and 3 DWPD over five years: that is 70.08 PB written per drive. A QLC D5-P5336 at 61.44TB and 0.58 DWPD gives 65.06 PBW.[^67] Divide by list price and the *more expensive per gigabyte* TLC drive is roughly 2.6× cheaper per petabyte written. StorageReview's rig sustained 1.9 GB/s of array writes across four GPUs; dividing gives about 0.475 GB/s per GPU (==my arithmetic — the source publishes the array rate, not a per-GPU figure==).[^26] Scale that to a thousand GPUs and you are writing on the order of 15 exabytes a year, which annualises to single-digit-to-low-double-digit percentages of GPU capex in replacement drives alone — and the number is invariant to how much capacity you provision, because capacity and replacement rate trade off exactly.

| Media | $ per GB (list) | Rated PB written | **$ per PB written** |
|---|---|---|---|
| Enterprise TLC — D7-PS1030 12.8TB, 3 DWPD | 0.83 | 70.1 | **152** |
| *High-capacity QLC — D5-P5336 61.44TB, 0.58 DWPD | 0.42 | 65.1 | **393** |

Read that table twice. On the metric the marketing uses, QLC wins by roughly 2×. On the metric a write-saturated KV tier actually pays, TLC wins by 2.6×. The ranking inverts, and every published comparison in this cycle uses the first column.

Samsung's own white paper is the most useful economic document in the set precisely because it publishes its own losing regime. Its NVMe-offload configuration costs approximately 4% *more* than the baseline below the crossover, and reaches only 1.5× cost efficiency at 240 concurrent users.[^27] The 4% is not a rounding error — it is exactly the NVMe line item in Samsung's own bill of materials.

The vendor multipliers collapse under the same scrutiny. WEKA publishes 41× time-to-first-token against full prefill recompute, 4.2× tokens per GPU against a DRAM cache, and — in the only dollar-denominated figure any storage vendor published — a 24% reduction in token throughput cost.[^69] Forty-one times, to four times, to twenty-four percent, depending entirely on what the baseline was. The multiplier measures how expensive prefill is, not how good the storage is.

The market does price a cache hit, incidentally, and the price is remarkably consistent: four independent API providers charge roughly 10% of uncached input for a cache read, with OpenAI and Anthropic now adding a 1.25×–2× write premium.[^42,43] But that is a price, not a cost — Google moved its implicit discount from 75% to 90% with no architectural change, and Anthropic's cached-read price is *defined* as 0.1× a base price that moves independently.

---

## 08. Does anyone actually run this?

No named operator has published production scale numbers for an SSD KV-cache tier. That is a finding, not a gap.

The two systems most often cited as counter-examples do not say what they are quoted as saying. Mooncake's paper lists SSD in a resource inventory — "the underutilized CPU, DRAM, and SSD resources of the GPU cluster" — but every measured path in it is CPU DRAM, and the experiments run on a cluster of twenty machines with a dummy LLaMA2-70B-shaped model.[^38] The actual SSD implementation is a July 2026 open-source feature, benchmarked on a single 8×A100 node, and its own authors call it "only the first step toward a fully tiered KV cache architecture."[^39] DeepSeek's 3FS pitches NVMe KVCache as "a cost-effective alternative to DRAM-based caching" and shows a 40 GiB/s-per-client figure — but the widely-circulated 180-node cluster spec belongs to the *training* dataloader benchmark, not the KV section.[^40]

The one large-cloud production characterisation that exists argues against the tier outright. Alibaba and SJTU, at USENIX ATC'25, found that "a KV$ with capacity 2× of the GPU HBM per-GPU is sufficient to approach an ideal hit rate", explicitly "eliminating the cost and complexity of deploying and managing a CPU-RDMA-SSD storage hierarchy."[^37] Their traces show why: 80% of reuse happens within ten minutes on one trace and within ten seconds on another. The working set dies before a capacity tier can earn its latency.

OpenAI documents its prompt cache as living "within volatile GPU memory" with 5–10 minute eviction.[^42] Anthropic documents a 5-minute default and a paid 1-hour option.[^43] Neither discloses flash anywhere.

:::timeline
- {date: 2019-08, headline: "XL-FLASH launched", body: "Toshiba Memory ships the SLC BiCS die at <5µs read latency, positioned to bridge DRAM and NAND."}
- {date: 2019-11, headline: "GPUDirect Storage announced", body: "NVIDIA launches Magnum IO at SC19; broader release “planned for the first half of 2020”. GA slips to roughly mid-2021."}
- {date: 2022-03, headline: "BaM paper posted", body: "GPU threads initiate NVMe I/O directly. Workloads: graph analytics, recommenders, GNNs. arXiv:2203.04910."}
- {date: 2022-07, headline: "Intel winds down Optane", body: "$559M inventory impairment in Q2 2022. Gelsinger names CXL, not flash, as the replacement direction."}
- {date: 2025-02, headline: "High Bandwidth Flash debuts", body: "Sandisk unveils HBF at Investor Day; completes separation from Western Digital as SNDK the same month."}
- {date: 2025-06, headline: "PCIe 7.0 released to members", body: "128 GT/s, up to 512 GB/s bidirectional over x16 — the link the 100M-IOPS target is matched to."}
- {date: 2025-08, headline: "Sandisk and SK hynix sign HBF MOU", body: "HBF moves from one vendor's concept to a would-be industry tier."}
- {date: 2025-10, headline: "Micron publishes 230M IOPS", body: "44 Gen6 SSDs, 512B random read, “SOL benchmark SCADA workload”. Demoed at SC25."}
- {date: 2026-01, headline: "vLLM grows its offload block", body: "KV cache re-laid-out across layers: a few KB → 0.5–2 MB. The serving stack moves away from small I/O."}
- {date: 2026-01, headline: "NVIDIA announces CMX on BlueField-4", body: "An Ethernet-attached “G3.5” flash tier optimized specifically for KV cache. No mention of 512B or IOPS."}
- {date: 2026-08, headline: "FMS 2026: cuFile open-sourced, SCADA named", body: "40+ Storage-Next vendors; Kioxia GP1 at 10M IOPS @512B; first OCP HBF specification published."}
:::

The one place the argument genuinely bites is agentic work. Traces from 4,265 coding-agent sessions across 43 developers, published in 2026, show token-weighted prefix-cache hit rates around 95.7–95.8%, with misses clustering exactly at human thinking gaps: "when the gap is larger than 5 minutes, low-hit-rate steps begin to appear, and after 1 hour, almost all steps miss the cache."[^41] Sweeping the eviction timeout from one minute to one hour lifts the hit rate from 85.4% to 98.6%.[^41] The commercially interesting leg is the last one — going from a five-minute to a one-hour window buys roughly four more points of hit rate for about 2.7× more resident KV, which is precisely the trade a cheap capacity tier exists to make. That is a *residency* problem, which flash is genuinely good at, rather than a bandwidth problem, which it is not. It is also the only version of this thesis with a credible mechanism.

---

## 09. NVIDIA's own answer is not the 512-byte drive

The strongest correction to the popular story is that NVIDIA does propose putting KV cache on flash — through a completely different program, with a completely different vocabulary.

On 5 January 2026, seven months before FMS, NVIDIA announced BlueField-4 alongside what it calls the NVIDIA Inference Context Memory Storage Platform: a network-attached flash tier for KV cache, claiming up to 5× tokens per second and 5× power efficiency, sized against "Rubin cluster-level KV cache capacity".[^44] Neither "512" nor "IOPS" appears anywhere in that release. The unit of transfer is the KV block, and the tiering model it slots into — HBM, host DRAM, local SSD, network flash, shared storage — is the same shape as Dynamo's KV Block Manager.[^63] By August the same tier had picked up the CMX name and the "context tier" framing in the FMS blog.[^1]

And NVIDIA's answer to the *context* problem is not storage at all. Rubin CPX, announced September 2025, is "the first CUDA GPU purpose-built for massive-context AI", and it solves the problem with 128GB of "cost-efficient GDDR7 memory".[^45] Given a choice between a flash tier and cheaper DRAM, NVIDIA's own product decision was cheaper DRAM.

Two programs, then. A 512-byte IOPS architecture for fine-grained embedding, graph and vector retrieval — descended from BaM, benchmarked with SOL, productised as GP1. And a bandwidth-and-capacity architecture for KV cache — CMX, BlueField-4, megabyte blocks over the network. ==The honest caveat is that NVIDIA co-announced both in the same August blog post, so it invited the conflation rather than merely suffering it.==[^1] But it did not blur them internally: in NVIDIA's own sentences, context memory belongs to CMX and the small-block program is never given a workload. The collapse into a single story happened downstream, and it produced a thesis more exciting and less true than either program on its own.

Marvell's positioning makes the split visible from the other side. Its GPU-initiated storage blog attributes the 100M-IOPS requirement to NVIDIA's Gen7 Storage-Next target rather than to any Marvell part,[^51] while a separate Marvell product line sells rack-scale CXL DRAM pooling explicitly on the KV-cache pitch, at sub-microsecond access.[^52] The same company answers the KV question with DRAM and the small-block question with flash.

---

## 10. What would break this reading

A thesis that cannot be falsified is not worth publishing, so here is what would overturn it, ranked by how likely I think each is.

**The 512-byte program could absorb KV cache after all.** If NVIDIA publishes a SCADA specification that names KV cache and defines sub-4KB KV transfer — or if a serving engine ships a layout that *shrinks* rather than grows its offload block — the workload-mismatch argument collapses. The evidence currently runs the other way: vLLM, llm-d and LMCache have all moved toward megabyte blocks, and Tutti's measured fix was layout, not device.[^17,18,20] But NVIDIA has published no architecture document at all, so this is inference from absence.

**Agentic workloads could rewrite the residency economics.** The Alibaba result that kills the tier is measured on chat traffic in late 2024 and early 2025, before agentic coding volume ramped.[^37] The coding-trace study points the other way, hard.[^41] If a hyperscaler publishes a production KV cache in the petabyte range serving multi-hour agent sessions, the capacity argument becomes real regardless of block size. I would treat this as the most likely path by which the tier ships.

**Endurance is already being engineered around.** This is the falsifier furthest along. ScaleFlux announced a KV-cache SSD platform on 30 July 2026 claiming 7–10+ effective DWPD over five years with more than 200 FDP write streams,[^91] Kioxia rates GP1 at up to 50 DWPD,[^9] and StorageReview's own measured overrun disappears under RAID0 rather than RAID10.[^26] What nobody has published is a five-year field measurement, or a price for the drives that carry those ratings. Until one exists, "endurance is a solved design problem" and "endurance is the cost that eats the $/GB advantage" are both defensible readings of the same evidence.

**The counter-case could be understated.** Everything here assumes flash competes with DRAM. It also competes with CXL memory pooling, which Meta has now deployed at fleet scale on custom silicon at 0.13× the cost per gigabyte of local DRAM — achieved by reusing decommissioned DDR4, a mechanism no flash vendor can match.[^62] If CXL clears at sub-microsecond latency, flash is relegated to cold overflow. Marvell is selling exactly that.[^52]

**And the base rate is unkind.** The last purpose-built memory tier — 3D XPoint — died seven years after launch with a $559 million write-off, and its owner named CXL, not flash, as the successor.[^46,64] The closest comparable NVMe feature, Zoned Namespaces, was ratified in 2021 and is described by Samsung's own scorecard as having "low traction in NVMe" because "adoption requires major changes to the host stack."[^50] GPU-initiated 512-byte NVMe would require exactly that, and as of August 2026 no standards body has ratified anything for it. GPUDirect Storage itself, six years in, still concedes in NVIDIA's own documentation that upstream OS support is unavailable and that production deployments depend on proprietary filesystem stacks.[^49]

An adversarial pass over the three load-bearing claims broke two of them, and both corrections are folded in above. The claim that NVIDIA "names no motivating workload" was false — NVIDIA's FMS blog does name one, and attaches it to CMX, which sharpens the two-programs argument rather than dissolving it.[^1] The claim that endurance is a hard wall was overstated: the source I cited recommends RAID0 and calls the wear "acceptable in this case",[^26] and ScaleFlux is already selling against the problem.[^91] The third claim — that serving engines move megabyte KV blocks and are growing them — survived five distinct falsification attempts with no contradicting source found. It is the one load-bearing assertion in this piece I would defend without qualification.

:::callout(kind=danger, label="The one-line version")
The roadmap is real, the shortage is real, the physics is unforgiving, and the workload is somebody else's. Buy the 512-byte drive if you are running vector search, graph neural networks or a recommender embedding table — those are genuine, underserved, IOPS-starved workloads and the economics are excellent. Do not buy it because you read that it fixes the KV cache. For that, NVIDIA is selling you a different box.
:::

The equity market has already priced something. ==SanDisk reported roughly $9.0 billion of FQ4 FY2026 revenue with datacenter at about $3.0 billion — a third of the total, up close to 103% sequentially; the investor-relations release did not resolve on repeated fetches, so treat these as unverified against the primary filing.==[^60] Kioxia, meanwhile, round-tripped from a June peak to roughly 56% below it by early August, printing record results on the way down. Management at both attributes growth to NAND pricing and datacenter mix, not to any AI-SSD product launch. Enterprise SSD revenue among the top five suppliers hit $18.46 billion in 1Q26, up 86.1% QoQ, on contract prices up roughly 80% in the same quarter.[^57] That is a memory-cycle trade wearing an architecture story.

The architecture story may still come true. It will just arrive over Ethernet, in megabyte blocks, on TLC — and the drive that gets the headlines will be selling to the vector-database market that asked for it in 2022.

:::references
- {id: 1, title: "NVIDIA open-sources cuFile, launches Storage-Next and SCADA at FMS 2026", url: "https://blogs.nvidia.com/blog/ai-storage-fms/", source: NVIDIA, date: "2026-08-04"}
- {id: 2, title: "cuFile API Reference Guide v1.18", url: "https://docs.nvidia.com/gpudirect-storage/api-reference-guide/index.html", source: NVIDIA, date: "2026-05-21"}
- {id: 3, title: "NVIDIA SCADA Puts Storage Control on the GPU as cuFile Goes Open Source", url: "https://www.storagereview.com/news/nvidia-scada-puts-storage-control-on-the-gpu-as-cufile-goes-open-source", source: StorageReview, date: "2026-08-04"}
- {id: 6, title: "GPU-Initiated On-Demand High-Throughput Storage Access in the BaM System Architecture", url: "https://arxiv.org/abs/2203.04910", source: "arXiv:2203.04910 / ASPLOS 2023", date: "2022-03-09"}
- {id: 7, title: "SC25 performance breakthrough: 230M IOPS in a single server", url: "https://www.micron.com/about/blog/storage/ssd/sc25-performance-breakthrough-230m-iops-in-a-single-server", source: Micron, date: "2025-10-31"}
- {id: 8, title: "From breakthrough demo to deployment path: SCADA on production-grade PCIe Gen6 hardware at NVIDIA GTC 2026", url: "https://www.micron.com/about/blog/storage/ssd/from-breakthrough-demo-to-deployment-path-scada-on-production-grade-pcie-gen6-hardware-at-nvidia-gtc-2026", source: Micron, date: "2026-02-28"}
- {id: 9, title: "KIOXIA GP1 Series Super High IOPS SSDs for AI applications", url: "https://www.kioxia.com/en-jp/business/news/2026/20260804-1.html", source: Kioxia, date: "2026-08-04"}
- {id: 10, title: "Super High IOPS SSD", url: "https://americas.kioxia.com/en-us/insights/super-high-iops-ssd-202604.html", source: Kioxia, date: "2026-04-14"}
- {id: 11, title: "KIOXIA to demonstrate AI storage technologies at FMS 2026", url: "https://americas.kioxia.com/en-us/business/news/2026/ssd-20260803-2.html", source: Kioxia, date: "2026-08-03"}
- {id: 12, title: "Kioxia developing 100 million IOPS SSD for Nvidia", url: "https://blocksandfiles.com/2025/09/15/kioxia-100-million-iops-ssd-nvidia/", source: "Blocks & Files", date: "2025-09-15"}
- {id: 13, title: "Graid Technology Achieves Industry-First 100 Million IOPS on a Protected Volume", url: "https://www.accessnewswire.com/newsroom/en/computers-technology-and-internet/graid-technology-achieves-industry-first-100-million-iops-on-a-pr-1191189", source: "Graid / ACCESS Newswire", date: "2026-07-15"}
- {id: 14, title: "Smart IOPS and H3 Platform Unveil AI Compute Storage Solution Designed to Deliver Up to One Billion Random IOPS", url: "https://www.prnewswire.com/news-releases/smart-iops-and-h3-platform-unveil-ai-compute-storage-solution-designed-to-deliver-up-to-one-billion-random-iops-302845255.html", source: PR Newswire, date: "2026-08-06"}
- {id: 15, title: "PCI-SIG Releases PCIe 7.0 Specification at 128.0 GT/s", url: "https://www.businesswire.com/news/home/20250611299049/en/PCI-SIG-Releases-PCIe-7.0-Specification-to-Support-the-Bandwidth-Demands-of-Artificial-Intelligence-at-128.0-GTs-Transfer-Rates", source: PCI-SIG, date: "2025-06-11"}
- {id: 16, title: "Micron 9650 NVMe SSD", url: "https://www.micron.com/products/storage/ssd/data-center-ssd/9650-ssd", source: Micron, date: "2026-01-01"}
- {id: 17, title: "KV offloading connector: a new layout for CPU offloading", url: "https://vllm.ai/blog/2026-01-08-kv-offloading-connector", source: vLLM, date: "2026-01-08"}
- {id: 18, title: "Native KV cache offloading to any file system with llm-d", url: "https://llm-d.ai/blog/native-kv-cache-offloading-to-any-file-system-with-llm-d", source: llm-d, date: "2026-02-10"}
- {id: 19, title: "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model", url: "https://arxiv.org/html/2405.04434v5", source: "arXiv:2405.04434", date: "2024-05-07"}
- {id: 20, title: "Tutti: rethinking KV cache layout for SSD-backed LLM serving", url: "https://arxiv.org/html/2605.03375", source: "arXiv:2605.03375", date: "2026-05-05"}
- {id: 21, title: "XL-FLASH", url: "https://americas.kioxia.com/en-us/business/memory/xlflash.html", source: Kioxia, date: "2026-08-10"}
- {id: 24, title: "Energy analysis of flash-based memory expansion for LLM inference", url: "https://arxiv.org/html/2508.06978v1", source: "IEEE Computer Architecture Letters, DOI 10.1109/LCA.2025.3592563", date: "2025-08-12"}
- {id: 26, title: "The Token-Efficient Path for Long-Context Inference: KV Cache Offload to Flash", url: "https://www.storagereview.com/review/the-token-efficient-path-for-long-context-inference-kv-cache-offload-to-flash", source: StorageReview, date: "2026-07-22"}
- {id: 27, title: "Scaling AI Inference with KV Cache Offloading", url: "https://download.semiconductor.samsung.com/resources/white-paper/scaling_ai_inference_with_kv_cache_offloading.pdf", source: Samsung Semiconductor, date: "2026-07-06"}
- {id: 29, title: "1Q26 DRAM industry revenue rises 81% QoQ to $97 billion", url: "https://www.trendforce.com/presscenter/news/20260601-13070.html", source: TrendForce, date: "2026-06-01"}
- {id: 30, title: "3Q26 memory contract price outlook", url: "https://www.trendforce.com/presscenter/news/20260703-13134.html", source: TrendForce, date: "2026-07-03"}
- {id: 31, title: "HBM wafer input to reach 30% of total DRAM wafer input by end-2027", url: "https://www.trendforce.com/presscenter/news/20260602-13074.html", source: TrendForce, date: "2026-06-02"}
- {id: 32, title: "Micron Technology, Inc. Reports Record Results for the Third Quarter of Fiscal 2026", url: "https://www.globenewswire.com/news-release/2026/06/24/3317151/14450/en/micron-technology-inc-reports-record-results-for-the-third-quarter-of-fiscal-2026.html", source: Micron, date: "2026-06-24"}
- {id: 33, title: "High Bandwidth Flash at FMS 2026", url: "https://news.skhynix.com/en/hbf-at-fms-2026/", source: SK hynix, date: "2026-08-03"}
- {id: 87, title: "Structural shortages to keep NOR flash and SLC NAND prices rising in 2H26", url: "https://www.trendforce.com/presscenter/news/20260616-13102.html", source: TrendForce, date: "2026-06-16"}
- {id: 34, title: "AI chip component cost shares", url: "https://epoch.ai/data-insights/ai-chip-component-cost-shares", source: Epoch AI, date: "2026-05-21"}
- {id: 35, title: "HP says memory costs doubled to 35% of PC build materials in one quarter", url: "https://www.tomshardware.com/tech-industry/hp-says-memory-costs-doubled-to-35-percent-of-pc-build-materials-in-one-quarter", source: "Tom's Hardware (HP FQ1-26 call)", date: "2026-02-25"}
- {id: 36, title: "NVIDIA reportedly evaluating lower HBM configurations for Rubin Ultra", url: "https://www.trendforce.com/presscenter/news/20260804-13166.html", source: TrendForce, date: "2026-08-04"}
- {id: 37, title: "Characterizing KV cache in production LLM serving", url: "https://arxiv.org/html/2506.02634v3", source: "arXiv:2506.02634 / USENIX ATC'25 (Alibaba, SJTU)", date: "2025-06-03"}
- {id: 38, title: "Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving", url: "https://arxiv.org/html/2407.00079v1", source: "arXiv:2407.00079 (Moonshot AI)", date: "2024-07-01"}
- {id: 39, title: "Scaling KV cache beyond memory: SSD offloading in Mooncake Store", url: "https://kvcache.ai/blog/scaling-kv-cache-beyond-memory/", source: Mooncake, date: "2026-07-15"}
- {id: 40, title: "3FS: Fire-Flyer File System", url: "https://github.com/deepseek-ai/3FS", source: DeepSeek, date: "2025-02-28"}
- {id: 41, title: "Prefix cache behaviour in agentic coding traces", url: "https://arxiv.org/html/2606.30560v2", source: "arXiv:2606.30560", date: "2026-06-01"}
- {id: 42, title: "Prompt caching", url: "https://developers.openai.com/api/docs/guides/prompt-caching", source: OpenAI, date: "2026-08-10"}
- {id: 43, title: "Prompt caching", url: "https://platform.claude.com/docs/en/build-with-claude/prompt-caching", source: Anthropic, date: "2026-08-10"}
- {id: 44, title: "NVIDIA BlueField-4 Powers New Class of AI-Native Storage Infrastructure", url: "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-BlueField-4-Powers-New-Class-of-AI-Native-Storage-Infrastructure-for-the-Next-Frontier-of-AI/default.aspx", source: NVIDIA, date: "2026-01-05"}
- {id: 45, title: "NVIDIA Unveils Rubin CPX, a New Class of GPU Designed for Massive-Context Inference", url: "https://nvidianews.nvidia.com/news/nvidia-unveils-rubin-cpx-a-new-class-of-gpu-designed-for-massive-context-inference", source: NVIDIA, date: "2025-09-09"}
- {id: 46, title: "Intel Reports Second-Quarter 2022 Financial Results", url: "https://www.intc.com/news-events/press-releases/detail/1563/intel-reports-second-quarter-2022-financial-results", source: Intel, date: "2022-07-28"}
- {id: 47, title: "100 Million IOPS SSDs? You Must be Kidding!", url: "https://thessdguy.com/100-million-iops-ssds-you-must-be-kidding/", source: "Jim Handy, Objective Analysis", date: "2026-02-02"}
- {id: 48, title: "Emulating GPU-initiated storage for LLM and graph workloads", url: "https://arxiv.org/html/2604.06668v1", source: "arXiv:2604.06668 (KAIST)", date: "2026-04-08"}
- {id: 49, title: "GPUDirect Storage Overview Guide", url: "https://docs.nvidia.com/gpudirect-storage/overview-guide/index.html", source: NVIDIA, date: "2026-05-21"}
- {id: 50, title: "A Brief History of Data Placement Technologies", url: "https://semiconductor.samsung.com/news-events/tech-blog/a-brief-history-of-data-placement-technologies/", source: Samsung Semiconductor, date: "2023-08-31"}
- {id: 51, title: "The Next Step for AI Storage: GPU-initiated and CPU-initiated Storage", url: "https://www.marvell.com/blogs/the-next-step-for-ai-storage-gpu-initiated-cpu-initiated-storage.html", source: Marvell, date: "2026-08-04"}
- {id: 52, title: "Marvell next-gen CXL switch memory pooling breaks the AI memory wall", url: "https://www.marvell.com/company/newsroom/marvell-next-gen-cxl-switch-memory-pooling-breaks-ai-memory-wall.html", source: Marvell, date: "2026-03-17"}
- {id: 54, title: "Bandana: Using Non-volatile Memory for Storing Deep Learning Models", url: "https://arxiv.org/abs/1811.05922", source: "arXiv:1811.05922 (Facebook)", date: "2018-11-14"}
- {id: 55, title: "Accelerating Sampling and Aggregation Operations in GNN Frameworks with GPU Initiated Direct Storage Accesses", url: "https://arxiv.org/abs/2306.16384", source: "arXiv:2306.16384 (NVIDIA, UIUC)", date: "2023-06-28"}
- {id: 56, title: "DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node", url: "https://papers.neurips.cc/paper/9527-rand-nsg-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node", source: "NeurIPS 2019 (Microsoft Research)", date: "2019-12-08"}
- {id: 57, title: "1Q26 enterprise SSD revenue surges 86.1% QoQ to US$18.46 billion", url: "https://www.trendforce.com/presscenter/news/20260611-13092.html", source: TrendForce, date: "2026-06-11"}
- {id: 58, title: "Memory industry to maintain cautious capex in 2026, with limited impact on bit supply growth", url: "https://www.trendforce.com/presscenter/news/20251113-12780.html", source: TrendForce, date: "2025-11-13"}
- {id: 60, title: "Sandisk Reports Fiscal Fourth Quarter 2026 Financial Results", url: "https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-fourth-quarter-2026-financial-results", source: SanDisk, date: "2026-08-05"}
- {id: 62, title: "Vistara: Making CXL Real — Full Path from ASIC Design and OS Support to Hyperscale Deployment", url: "https://aisystemcodesign.github.io/papers/isca26/vistara_camera_ready.pdf", source: "ISCA 2026 (Meta Platforms)", date: "2026-06-29"}
- {id: 63, title: "KV Block Manager design", url: "https://docs.nvidia.com/dynamo/design-docs/component-design/kvbm-design", source: NVIDIA Dynamo, date: "2026-08-10"}
- {id: 64, title: "A requiem for Optane, Intel's KV cache killer that could have eased the RAM price crunch", url: "https://www.theregister.com/storage/2026/07/29/a-requiem-for-optane-intels-kv-cache-killer-that-could-have-eased-the-ram-price-crunch/5280063", source: The Register, date: "2026-07-29"}
- {id: 67, title: "Solidigm D5-P5336 Product Brief", url: "https://www.solidigm.com/content/dam/solidigm/en/site/products/technology/p5336-product-brief/documents/Solidigm-D5P5336-ProductBrief.pdf", source: Solidigm, date: "2025-04-03"}
- {id: 69, title: "New Augmented Memory Grid revolutionizes the economics of AI inference infrastructure", url: "https://www.weka.io/article/new-augmented-memory-grid-revolutionizes-the-economics-of-ai-inference-infrastructure", source: WEKA, date: "2025-03-18"}
- {id: 70, title: "FMS Storage Ticker — 4 Aug 2026", url: "https://www.blocksandfiles.com/flash/2026/08/04/fms-storage-ticker-4-aug-2026/5282932", source: "Blocks & Files", date: "2026-08-04"}
- {id: 71, title: "DRAM and NAND spot prices", url: "https://dramexchange.com/", source: DRAMeXchange, date: "2026-08-10"}
- {id: 79, title: "OpenAI's Lightcap sees memory shortage as bottleneck risk for AI", url: "https://www.bloomberg.com/news/articles/2026-03-24/openai-s-lightcap-sees-memory-shortage-as-bottleneck-risk-for-ai", source: Bloomberg, date: "2026-03-24"}
- {id: 80, title: "HBM4 sticks with microbumps, postponing hybrid bonding", url: "https://semiengineering.com/hbm4-sticks-with-microbumps-postponing-hybrid-bonding/", source: Semiconductor Engineering, date: "2026-07-07"}
- {id: 82, title: "NVIDIA H200 Tensor Core GPU", url: "https://www.nvidia.com/en-us/data-center/h200/", source: NVIDIA, date: "2026-08-10"}
- {id: 83, title: "DeepSeek-V4 technical report", url: "https://arxiv.org/html/2606.19348v1", source: "arXiv:2606.19348", date: "2026-04-26"}
- {id: 84, title: "Qwen3-Next-80B-A3B-Instruct model card", url: "https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct", source: "Qwen / Hugging Face", date: "2025-09-11"}
- {id: 85, title: "Why did M2 end up as a full attention model", url: "https://www.minimax.io/news/why-did-m2-end-up-as-a-full-attention-model", source: MiniMax, date: "2025-11-04"}
- {id: 89, title: "Meta-Llama-3.1-70B-Instruct config.json", url: "https://huggingface.co/unsloth/Meta-Llama-3.1-70B-Instruct/raw/main/config.json", source: Hugging Face, date: "2026-08-10"}
- {id: 90, title: "DeepSeek-V3 config.json", url: "https://huggingface.co/deepseek-ai/DeepSeek-V3/raw/main/config.json", source: Hugging Face, date: "2026-08-10"}
- {id: 91, title: "ScaleFlux KV Cache SSD Platform Claims 7-10+ DWPD and 200+ FDP Streams", url: "https://www.storagereview.com/news/scaleflux-kv-cache-ssd-platform-claims-7-10-dwpd-and-200-fdp-streams", source: StorageReview, date: "2026-07-30"}
- {id: 92, title: "XIO-SIG organisation", url: "https://github.com/xio-sig", source: GitHub, date: "2026-08-10"}
- {id: 93, title: "NVIDIA AI Storage Goes Open at FMS 2026: Is Open Source the New Moat?", url: "https://futurumgroup.com/insights/nvidia-ai-storage-goes-open-at-fms-2026-is-open-source-the-new-moat/", source: Futurum Group, date: "2026-08-06"}
:::
