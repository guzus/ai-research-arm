---
eyebrow: REPORT · SEMICONDUCTORS · INFERENCE ECONOMICS
title: "The 2.28x that was 4% silicon: does the TPU and Trainium perf-per-dollar edge survive pricing scrutiny?"
deck: SemiAnalysis's InferenceX now scores Google's TPU and Amazon's Trainium against Nvidia. Most of the advantage comes from the price column, a price nobody outside the hyperscalers can buy at.
domain: semiconductor
lede: |
  On 25–27 November 2026 SemiAnalysis said Google's TPUv7 Ironwood and Amazon's Trainium3 had joined its InferenceX and AgentX benchmarks. It said they beat comparable Nvidia GPUs by 1.2x to 2.5x on performance per dollar in one post and by 1.5–2.5x "at release" in another. The timing was pointed: seven months earlier Jensen Huang had said on a podcast that neither chip would show up. Taking the numbers apart gives a narrower answer than the headline. On SemiAnalysis's own figures, the best Trainium3 result is about 4% more tokens per chip, multiplied by a modeled 2.2x hourly-cost gap. Ironwood's best result is about 5% more tokens per chip, multiplied by a modeled 1.43x gap. The silicon is roughly at parity; the edge is a statement about cost. Whether that edge survives depends on who is buying, at what interactivity, in which precision, and against which Nvidia generation.
stats:
  - {label: "Trn3 vs GB300, best point", value: 2.28x, note: "perf per $, AgentX preview"}
  - {label: "Raw throughput gap there", value: "~4%", note: "9,266 vs 8,942 tok/chip-s"}
  - {label: "Modeled $/chip-hr", value: "$1.05 vs $2.31", note: "Trn3 vs GB300"}
  - {label: "AWS list, B300 vs Trn2", value: 7.2x, note: "Capacity Block $/accel-hr"}
---

:::kv
- {term: "Short answer", def: "Partly. The edge is real on SemiAnalysis's modeled cost basis, at specific operating points, in FP8 or against last-generation Nvidia parts. It is not a hardware-speed result."}
- {term: "Where it holds", def: "Large labs buying capacity directly from Google or AWS (Anthropic, OpenAI, Meta), at moderate interactivity, against Blackwell (B200, B300, GB300)."}
- {term: "Where it breaks", def: "Against Vera Rubin, which SemiAnalysis's own data shows ahead; against FP4 GB300 on several models; at the throughput peak, where Trainium3's lead falls to about 7%; and for a small renter paying Ironwood's reported $12 per chip-hour list price."}
- {term: "Pricing verdict", def: "Published prices make Trainium look cheaper than the model does (AWS lists Trn2 at $2.24 per chip-hour against $16.15 for B300). They make Ironwood look worse, since its reported list price is above CoreWeave's GB200."}
- {term: "What would settle it", def: "Public run logs for the Trainium3 rows, a published Trn3 hourly price, and a head-to-head against Vera Rubin and TPUv8i on the same AgentX trace."}
:::

## 01. What SemiAnalysis actually claimed, and what it did not

The headline compresses several separate results, published weeks apart, on different models and different cost bases, into one range. Pulling them apart is the first step in checking the claim. SemiAnalysis's announcement said seven months had passed since Nvidia's CEO said TPU and Trainium would not come to its benchmark, and that both were now on InferenceX and its agentic successor AgentX[^1,3]. Huang's remark is on the record. On the Dwarkesh Podcast on 15 April 2026 he said "Dylan's InferenceMAX is sitting out there for everybody to use, and not one… TPU won't come, Trainium won't come", and he added "I would welcome Trainium to demonstrate their 40% that they claim all the time"[^2]. When the benchmark launched in October 2025, Nvidia's own blog had said "NVIDIA Blackwell swept the new SemiAnalysis InferenceMAX v1 benchmarks"[^34].

The range itself is not stable. The first post, as reported by OfficeChai, gave 1.2x to 2.5x[^1,3]. A follow-up post amplified on X described Google and Amazon as "demonstrating 1.5-2.5x better perf per $ at release versus equivalent NVIDIA GPUs"[^45]. The higher lower bound does not match SemiAnalysis's own TPU work, whose September headline was "up to 50%" better performance per dollar, a 1.5x ceiling rather than a floor[^7].

:::timeline
- {date: 2025-10-09, headline: "InferenceMAX launches", body: "Open-source, nightly inference benchmark; Nvidia's blog says Blackwell 'swept' v1."}
- {date: 2026-04-15, headline: "Huang on Dwarkesh", body: "'TPU won't come, Trainium won't come'; invites both to prove their cost claims."}
- {date: 2026-09-07, headline: "Ironwood debut", body: "Up to 50% better perf per dollar than B200/B300 at FP8 on Qwen3.5 397B; Official Preview, private-beta TorchTPU stack."}
- {date: 2026-11-05, headline: "'The Iron(wood) Throne'", body: "TPUv7 1.67x GB300 FP4 on Qwen3.5 AgentX, but GB300 FP4 leads by 1.5–2.6x on Kimi K3."}
- {date: 2026-11-25, headline: "Trainium3 on AgentX", body: "Up to 2.28x perf per dollar vs GB300 NVL72, B300 and MI355X on GLM-5.2/5.3 744B, FP4, vLLM; preview."}
- {date: 2026-11-27, headline: "Trainium3 deep dive", body: "SemiAnalysis: Trn3 beats every accelerator 'besides Vera Rubin' across the TCO vs interactivity curve."}
:::

The Trainium3 result is the anchor for the high end. Press accounts citing SemiAnalysis describe a Trainium3 UltraServer delivering "up to 2.28x better performance per dollar" than GB300 NVL72, B300 and MI355X. The model was Z.ai's 744-billion-parameter GLM-5.2/5.3, run in FP4 on vLLM[^3,4]. The free portion of SemiAnalysis's 27 November deep dive does not print the 2.28x figure or the hourly costs. It says Trainium3 with vLLM "is better than every other accelerator besides Vera Rubin across the entire TCO versus p90 interactivity curve"[^6]. Both TPU and Trainium results carry preview labels. The Ironwood runs came from a private-beta software stack on a SemiAnalysis fork, with the firm promising to move them "to our public repo"[^7]. The TorchTPU stack itself is described in a 53-author paper as "an open-source collaboration between Google and Meta"[^32], so the TPU runs are vendor-built software measured on a third party's harness.

**Counterpoint.** None of this means the numbers were invented. InferenceX's throughput side is open source under Apache-2.0, and its repository says only it carries the official results[^33]; commentary notes that GB300 rows link to recorded runs[^5]. Vendors have also fought over its rules before: a warmup step in Nvidia's submission was banned for everyone after AMD queried it[^37]. The main independent alternative, MLCommons' MLPerf Inference, measures performance in "an architecture-neutral, representative, and reproducible manner" but does not measure cost[^38]. The weak point is narrower: one dashboard series, priced by one firm, turned into a range that spans two chips, several models and two cost bases.

**Why this matters.** A "1.5–2.5x" headline invites buyers to apply the multiplier to their own workloads. The underlying results show the multiplier attaches to specific operating points, not to the chips.

## 02. Decomposing 2.28x: speed times price

The central arithmetic is simple, and it carries the article: performance per dollar is throughput per chip divided by cost per chip-hour. InferenceX states this directly. Its cost per million tokens is "TCO($/chip-hour) × 1,000,000 / (3600 × tok/s/chip)"[^9]. Once the two inputs are known, the multiplier can be split into a hardware part and a price part.

At the operating point where Trainium3's lead peaks (about 246 tokens per second per user at P90 in the commentary's reading, about 250 in press accounts), a reading of the dashboard reports about 9,266 total tokens per chip-second for Trainium3 and about 8,942 for GB300 NVL72[^5]. Crypto Briefing independently describes the same point as "only a marginal 4% performance lead"[^4]. The modeled hourly costs are $1.05 per chip for Trainium3 and $2.31 for GB300[^3,4].

:::exhibit(num="Exhibit 1", title="Where the 2.28x comes from", subtitle="Multiplier, Trainium3 over GB300 NVL72, at ~250 tok/s/user", source="Throughput: dev.to reading of InferenceX; cost: SemiAnalysis TCO as reported by OfficeChai and Crypto Briefing; ARA arithmetic.")
:::bar-chart(title="Throughput, price and the product", orientation=horizontal, value-suffix=x)
categories: Throughput per chip, Modeled cost per chip-hour, Perf per dollar
Trainium3 advantage: 1.04, 2.20, 2.28
:::
:::

Multiplying the two reproduces the headline: 9,266 / 8,942 is 1.036, 2.31 / 1.05 is 2.20, and the product is 2.28[^3,5]. In log terms, about 96% of the multiplier is the cost assumption and about 4% is silicon. Ironwood's September result splits the same way. At 20 tokens per second per user, TPUv7 produced 9,364 tokens per second per chip against 8,903 for B200, about 5% more, yet "50.4% more tokens per dollar"[^7]. Dividing one by the other, the external TCO basis prices Ironwood about 1.43x cheaper per hour than B200.

:::compare
- {role: "THROUGHPUT GAP", name: "Trn3 vs GB300 at ~250 tok/s/user", value: "+3.6%"}
- {role: "COST GAP (MODELED)", name: "GB300 $2.31 / Trn3 $1.05", value: "2.20x"}
- {role: SUBJECT, name: "Headline perf per dollar", value: "2.28x"}
:::

SemiAnalysis's own framing is consistent with this. Trainium3 has "only 17% the theoretical FP4 flops as Blackwell Ultra (2,517 TFLOPS versus 15,000 TFLOPS)" and "61% of the bandwidth at about 30% the TCO"[^6]. On a first-principles view that is plausible for this workload. AgentX replays opt-in Claude Code sessions whose median request is about 142,000 input tokens and 444 output tokens[^28,5]. That trace is dominated by prefill and KV-cache traffic. It rewards cheap memory bandwidth and scale-up networking more than peak FP4 math. Per modeled dollar, Trainium3 buys 4.9 / 1.05 ≈ 4.67 TB/s of HBM bandwidth against GB300's 8.0 / 2.31 ≈ 3.46. That is about a 1.35x edge before any topology work[^6,14]. Ironwood fits the same pattern. Google rates it at 4,614 FP8 TFLOPS and 7.37 TB/s per chip[^29], less bandwidth than GB300's 8 TB/s[^10], so its wins also have to come from cost or software rather than raw memory speed.

**Counterpoint.** SemiAnalysis argues the advantage "is not purely due to Amazon's ultra low cost supply chain", pointing to Amazon's wide expert-parallel decode design[^6]. That is a fair point about system engineering. But the same deep dive says Trainium "lags behind in some p90 TTFT cases against GB300"[^6]. The topology that wins on cost also costs latency: P90 time to first token was 4.5 seconds for Trainium3 against 1.8 seconds for GB300 at the comparison point[^4,5].

**Why this matters.** If the hardware is at parity and the cost column does the work, the debate is not about whether Trainium or TPU silicon is "better". It is about whose price list is believable.

## 03. The multiplier moves along the curve

A perf-per-dollar ratio is a point on a curve, and the curve here is steep. InferenceX plots tokens per dollar against interactivity (tokens per second per user). The headline is the single best point.

:::line-chart(title="Trainium3 perf-per-dollar advantage over GB300 NVL72", subtitle="AgentX, GLM-5.2/5.3 744B, by P90 interactivity (tok/s/user); as of 2026-11-26", y-unit=x)
x: 140,190,250,350
Trainium3 / GB300: 1.98,2.18,2.28,2.01
:::

The reported points are 1.98x at about 140 tokens per second per user, 2.18x at about 190, 2.28x at about 250 and 2.01x at about 350[^3]. At each system's throughput peak the picture changes. There Trainium3 reaches about 31,045 tokens per chip-second while GB300 reaches about 63,647, so GB300 does roughly twice the work per chip. On the same cost basis Trainium3's lead narrows to about 7%[^5]. The arithmetic checks: 31,045 / 63,647 × 2.20 ≈ 1.07.

The TPU results show the same dependence on operating point, and SemiAnalysis says so plainly. "The previously discussed 50% to 96% advantage applies to this datapoint specifically, rather than every latency target," the September article states. It adds that "across most of the raw-performance curve, TPU does not outperform Nvidia GPUs"[^7].

| Comparison (SemiAnalysis, InferenceX) | Result | Basis |
|---|---|---|
| *Ironwood vs B200 at 100 tok/s/user, Qwen3.5 FP8 | $0.181 vs $0.222 per M tokens (19% cheaper) | External TCO |
| Ironwood vs B300, same point | $0.181 vs $0.276 (34% cheaper) | External TCO |
| GB300 NVL72 disagg vs Ironwood agg, mid-latency | ~30% GB300 advantage | External TCO |
| Mean TTFT at concurrency 256 | 5.41 s TPU vs 2.40 s B300 | Latency |
| Ironwood vs B200, B300 on internal Google TCO | +76.7% and +130.2% tokens per $ | Internal TCO |

The table draws on the September Ironwood article[^7,9]. Not every TPU number in circulation is an InferenceX cost result. A widely repeated claim that TPUv7 ran 56% ahead of GB200 on Kimi K3 comes from Inferact's megakernel demo. That run used 16 chips against 16 GPUs, speculative decoding, and vLLM's stock GB200 recipe as the baseline. Inferact reports "over 700 tokens/s with speculative decoding, compared with 452 tokens/s on GB200"[^31]. That is a batch-1 latency result, not a tokens-per-dollar one.

**Counterpoint.** A defender of the headline would say buyers do operate near the sweet spot. Agentic serving at 140–350 tokens per second per user is a realistic band, and across that whole band Trainium3 stays at or above 1.98x on the modeled basis[^3]. That is a fair reading of the curve. But it holds only while the modeled prices hold, and it is measured against GB300 rather than Nvidia's current rack.

**Why this matters.** Capacity planners buy for a service-level target, not for a curve's best point. The 7% figure at peak throughput and the 2.5x latency penalty are as much part of the result as the 2.28x.

## 04. The price tag nobody publishes

Every multiplier in the headline rests on SemiAnalysis's hourly cost estimates. Those are model outputs from a paywalled TCO product, not quotes. InferenceX labels its GPU rates as "owning at large hyperscaler volume"[^10]. Its glossary defines two bases. "Internal TCO is the hourly cost of a chip to the company that designs and operates it". External TCO "is the cost to a third party buying or renting the same chip, including the vendor's margin"[^9].

:::exhibit(num="Exhibit 2", title="The cost column behind every InferenceX ratio", subtitle="SemiAnalysis modeled $ per chip-hour, hyperscaler-volume tier", source="InferenceX chip pages and press reporting of the AgentX dashboard; TPUv7 is Google internal TCO.", note="Trainium3 and TPUv7 have no published per-chip price; Nvidia/AMD figures are modeled owning costs, not rental prices.")
:::rank-list
- {label: "Vera Rubin NVL72 (internal basis)", value: "$3.61", pct: 100}
- {label: "GB300 NVL72", value: "$2.31", pct: 64}
- {label: "B300", value: "$2.26", pct: 63}
- {label: "GB200 NVL72", value: "$1.86", pct: 52}
- {label: "MI355X", value: "$1.50", pct: 42}
- {label: "Trainium3 (external)", value: "$1.05", pct: 29, highlight: true}
- {label: "TPUv7 Ironwood (internal)", value: "$1.03", pct: 29}
:::
:::

The GB300 to MI355X figures are $2.31, $2.26, $1.86 and $1.50, with Trainium3 at $1.05[^3,10]. Ironwood's internal figure is $1.03 per chip-hour[^7,9]. Vera Rubin's $3.61 comes from the GLM-5.3 Rubin preview and a commentary reading of the dashboard's internal basis[^5,12]. Two structural problems sit inside these numbers.

First, the bases are not symmetric. For Nvidia, InferenceX notes there is only an external TCO from the buyer's point of view, because Nvidia does not run its GPUs as a service[^9]. For TPU and Trainium the "external" figure is a price SemiAnalysis infers Google or Amazon would charge a large lab. Neither company publishes it. The glossary concedes the bases "can differ a lot". Switching Ironwood from external to internal moves its lead over B300 from 96.0% to 130.2%[^9].

Second, the basis can flip the winner outright. On the dashboard's internal basis, a commentary reading reports Trainium3 at $0.83 per chip-hour against $3.61 for Vera Rubin NVL72. On that basis Vera Rubin delivers 3.3x Trainium3's tokens per dollar at 273 tokens per second per user[^5]. In the commentator's words: "Same benchmark, same week, opposite headline — because the cost basis changed"[^5].

:::callout(kind=warn, label="Source caveat")
The Trainium3 dollar figures ($1.05, $0.83) and the 3.3x Rubin figure come from press and commentary readings of the dashboard, not from SemiAnalysis's free text. The same commentary reports that the Trainium3 rows carry no run link, commit or public logs, while GB300 rows link to recorded runs[^5]. Treat them as single-source until the rows are reproducible.
:::

**Counterpoint.** Someone has to estimate a price for chips that are not sold on the open market, and SemiAnalysis's TCO model is widely used for exactly that. InferenceX attributes its rate tiers to the SemiAnalysis AI Cloud TCO Model rather than to guesswork[^10]. Publishing both bases is arguably more transparent than vendor marketing, which publishes neither.

**Why this matters.** A perf-per-dollar ratio can only be as good as its denominator. When the denominator for half the chips is an inferred, unpublished price, the ratio is a hypothesis about cost, not a measurement.

## 05. Pricing scrutiny: what a buyer can actually pay

The test the topic asks for is to replace modeled prices with prices someone can actually pay. Doing so does not kill the edge. It splits it: Trainium's case gets stronger, Ironwood's gets weaker, and both depend on who the buyer is.

Start with the only first-party, per-accelerator price list from a cloud that sells both kinds of chip. AWS's EC2 Capacity Blocks page, fetched 28 November 2026, lists the following US prices per accelerator-hour[^13]:

:::exhibit(num="Exhibit 3", title="AWS's own price list makes Trainium look cheaper than the model does", subtitle="EC2 Capacity Blocks, $ per accelerator-hour, US regions, as of 2026-11-28", source="aws.amazon.com/ec2/capacityblocks/pricing; next update January 2027.", note="Trainium3 has no listed price; Trn2 is the prior generation.")
:::bar-chart(title="Capacity Block $/accelerator-hour", orientation=horizontal, value-unit=$)
categories: trn2 (Trainium2), p5 (H100), p5e (H200), p5en (H200), GB200 NVL72, p6-b200, p6-b300
Price: 2.235, 5.970, 6.866, 7.895, 10.582, 14.208, 16.146
:::
:::

On AWS's own list, a B300 accelerator-hour costs 7.2x a Trainium2 accelerator-hour ($16.146 against $2.235)[^13]. The modeled gap between GB300 and Trainium3 is 2.2x. So for a customer renting from AWS, the published spread is far wider than the one SemiAnalysis used. The comparison is imperfect: Trn2 is a generation older, and AWS publishes no Trn3 hourly price on either its Trn3 page or the Capacity Blocks list[^13,14]. AWS's own marketing claim is modest by comparison. It says Trn2 offers "30-40% better price performance than GPU-based EC2 P5e and P5en instances", which are H200 machines[^15]. On the Q1 2026 call Andy Jassy said Trainium2 "has about 30% better price-performance than comparable GPUs" and that Trainium3 is "30-40% more price-performant than Trainium2"[^21].

GPU rental markets show how far modeled owning costs sit from what renters pay. SemiAnalysis's own September article put 3-year rental at "over $8.5/hr/chip for Rubin and $5/hr/chip for Blackwell Ultra NVL72" in July 2026[^11]. That is 2.16x the $2.31 GB300 owning cost it uses in the benchmark.

:::slope(left-label="Modeled owning cost", right-label="Market price", unit=$)
| Chip | Modeled | Market |
|------|---------|--------|
| B200 (Vast.ai median ask) | 1.73 | 9.06 |
| B300 (Vast.ai median ask) | 2.26 | 10.63 |
| GB300 NVL72 (3-yr rental, Jul 2026) | 2.31 | 5.00 |
| GB200 NVL72 (CoreWeave on-demand) | 1.86 | 10.50 |
:::

Spot asks on Vast.ai, collected by this site's own price lane on 27 November, had median rentable prices of $10.63 per GPU-hour for B300 and $9.06 for B200[^18]. CoreWeave lists GB200 NVL72 at $42.00 per four-GPU instance on demand, $10.50 per GPU, and advertises "up to 60% discounts" for commitments[^17]. Azure's retail API prices an ND GB200 v6 VM in East US at $108.16 an hour pay-as-you-go[^19]. Lambda lists B200 from $7.69 per GPU-hour[^20]. The modeled rates come from SemiAnalysis's chip pages[^10].

Ironwood is where list prices hurt the thesis. Google's TPU pricing page could not be read first-hand for this article. Secondary reports put Ironwood at $12.00 per chip-hour on demand in Iowa, $8.40 on a one-year commitment and $5.40 on three years[^16]. At list, an Ironwood chip-hour costs about 1.14x a CoreWeave GB200 GPU-hour ($12.00 against $10.50)[^16,17]. Ironwood's measured throughput lead was about 5% at its best point[^7]. So at on-demand list prices its perf-per-dollar edge over Blackwell would disappear. The same report cites a SemiAnalysis estimate that Anthropic's contract rate is "roughly $1.60 per TPU-hour", about one-seventh of list[^16].

:::callout(kind=info, label="Reading the split")
Published prices make Trainium cheaper and Ironwood dearer than the model assumes. The reason is the business model. AWS prices its own chip aggressively on its own cloud, while Google's list price is a ceiling few large buyers pay. In both cases the edge belongs to the buyer with negotiating leverage, not to anyone who swipes a credit card.
:::

**Counterpoint.** List prices are a poor proxy for frontier inference economics, because the big buyers sign multi-year, multi-gigawatt contracts. SemiAnalysis's choice of hyperscaler-volume costs is defensible for the buyers who actually move markets. The firm's own margin model assumes 3-year rental prices, Z.ai list token prices and 60% fleet utilization. On that basis it gives Trainium3 a 73.5% profit margin against 53% for GB300 with SGLang at 135 tokens per second per user[^6].

**Why this matters.** For the handful of labs that negotiate directly with Google and Amazon, the edge plausibly survives. For everyone else, the real perf per dollar depends on a quote they have not yet received.

## 06. The moving target: Vera Rubin and FP4

"At release" is doing a lot of work in the headline. The comparisons are against Blackwell-generation Nvidia parts, mostly in FP8, while Nvidia's current rack is Vera Rubin and its default precision is FP4. SemiAnalysis's own data shows the edge shrinking or reversing on both counts.

On Vera Rubin, SemiAnalysis says Trainium3 beats "every other accelerator besides Vera Rubin"[^6]. On Kimi K3, "VR200 delivers 4.3x to 5.6x TPUv7"[^8]. A FourWeekMBA write-up of SemiAnalysis posts, not checked against the dashboard here, reported a GLM-5.3 preview with Vera Rubin NVL72 at 9.11x GB300's tokens per dollar at 200 tokens per second per user, priced at $3.61 against $2.31 per chip-hour[^12]. SemiAnalysis calls the TPU comparison "unfair", since "Rubin should be compared to TPUv8i", and notes that "Rubin's results remain preview submissions"[^8].

On precision and software, Nvidia has caught up on several models. On Kimi K3, Ironwood launched at 0.77–0.91x GB300's tokens per dollar, and "GB300 FP4 now leads by 1.5x to 2.6x after four NVIDIA refreshes". On GLM, "at 100 tok/s/user, GB300 and GB200 FP4 deliver 3.6x and 3.5x the tokens per dollar of TPUv7"[^8]. Ironwood "does not have native FP4 computation thus on FP4, NVIDIA GPUs still maintains the lead"[^7].

:::exhibit(num="Exhibit 4", title="The TPU edge depends on the model", subtitle="TPUv7 tokens per dollar relative to the named Nvidia system (1.0 = parity), as of 2026-11-05", source="SemiAnalysis, 'The Iron(wood) Throne' (2026-11-05); ARA inversion of 'Nvidia leads by Nx' figures; midpoints used for ranges.")
:::bar-chart(title="TPUv7 / Nvidia tokens per dollar", orientation=horizontal, value-suffix=x)
categories: Qwen3.5 AgentX vs GB300 FP4, Kimi K3 vs GB300 FP4, GLM at 100 tok/s/user vs GB300 FP4, Kimi K3 vs VR200
TPUv7 relative: 1.67, 0.49, 0.28, 0.20
:::
:::

The same article still credits TPUv7 with 1.15–2.5x the tokens per dollar of GB200, B200 and B300 on Kimi K3, and 1.67x better than FP4 GB300 on Qwen3.5[^8]. The pattern is consistent: the custom chips beat the Blackwell parts they launched against, on the models their teams tuned, and lose to Nvidia's newest rack and to FP4 on models where Nvidia has pushed software updates.

**Counterpoint.** Vera Rubin is priced at a premium ($3.61 modeled, more than $8.5 rented) and arrives in volume later[^11,12]. TPUv8i and Trainium4 are the fair comparisons, and SemiAnalysis says it plans to benchmark TPUv8i "very soon"[^8]. Anthropic's next multi-gigawatt TPU tranche starts coming online in 2027[^36]. On a like-for-like generational basis, the custom chips' cost structure may well persist.

**Why this matters.** A buyer signing a 2027 contract is choosing between Rubin, TPUv8i and Trainium4, not between Trainium3 and GB300. The published multipliers answer last year's procurement question.

## 07. Why custom silicon is cheaper per hour at all

The modeled cost gap is not arbitrary, and it has a structural explanation: the margin stack. Nvidia reported GAAP gross margin of 74.8% for the quarter ended 25 October 2026, on revenue of $115.8 billion, $107.6 billion of it from data center[^41]. A 74.8% gross margin means the selling price is about 4.0x the cost of goods (1 / 0.252). A TPU passes through Broadcom instead. On a machine transcript of Broadcom's fiscal Q3 call, its semiconductor segment gross margin was given as about 56.7%, after a first figure of about 76% was corrected[^43]. That figure is unconfirmed, and a higher one in the high 60s would fit Broadcom's reported 75% consolidated margin with high-margin software. So the Broadcom markup is somewhere between about 2.3x and 3.0x, and Google then decides what to charge on top.

:::stats
- {label: "Nvidia GAAP gross margin", value: "74.8%", note: "Q3 FY27, qtr to 2026-10-25"}
- {label: "Implied price / COGS", value: "~4.0x", note: "1 / (1 − 0.748)"}
- {label: "Broadcom semis GM (range)", value: "~57–67%", note: "FY26 Q3; transcript figure unconfirmed"}
- {label: "Implied price / COGS", value: "~2.3–3.0x", note: "1 / (1 − GM)"}
- {label: "Nvidia Q4 FY27 GM guide", value: "71–72%", note: "first step down"}
- {label: "Google TCO vs GB200 (SemiAnalysis est.)", value: "~44% lower", note: "Ironwood, Google's own cost"}
:::

On identical silicon cost, the two markups alone would produce a price gap of about 1.3x to 1.7x (4.0 divided by 3.0 or 2.3). That brackets the modeled 1.43x Ironwood gap, though not the 2.2x Trainium3 gap, where Amazon designs with Annapurna and has no Broadcom-sized partner margin to pay. SemiAnalysis reached a similar conclusion a year ago. It called Nvidia's "eye-watering 4x markup (~75% gross margin)" the source of Google's pricing room. It estimated Ironwood's all-in cost of ownership at about 44% below a GB200 server for Google, and up to about 30% below GB200 and 41% below GB300 for external customers after Google's markup[^44]. Its glossary describes the internal–external gap as "how much room Google has to cut external pricing if it chooses to"[^9]. Hock Tan was blunter on Broadcom's call: "you can do all this at half the cost of a GPU"[^43].

Amazon has said it plans to use that room. On the Q3 2026 call Jassy described Trainium as having "meaningful advantage it has in price performance versus other alternatives". He also said "the majority and most of Bedrock today is being run on top of Trainium"[^22].

**Counterpoint.** Huang disputed the margin arithmetic on Dwarkesh: "Nvidia's margin is 70%, let's say. But ASIC margins are 65%. What are you really saving?"[^2]. If he were right, the markup gap would be about 1.2x, at the low end of the range above. In this article's reading, the parts of a system bought from third parties (HBM, optics, power, buildings) do not carry Nvidia's markup on either side, which dilutes any chip-level gap at rack level. Nvidia also has a lever. Its Q4 guidance steps down to 71–72%, and on the 17 November call interim CEO Colette Kress called Q4 "our bottom"[^41,42]. Kress was briefly in charge: Huang resigned on 12 November[^40] and the board reinstated him as CEO on 23 November[^46]. That is why SemiAnalysis's post called him "NVIDIA's former and current CEO"[^45].

**Why this matters.** If the edge is mostly margin, it is a pricing decision, not a physics result. Nvidia can narrow it by giving up margin, and Google and Amazon can widen it the same way. Either side can move it within a quarter, much faster than a tape-out.

## 08. Revealed preference: the buyers who could check

The strongest corroboration comes from buyers who can run their own benchmarks and have signed for these chips at enormous scale. The weakest point in that corroboration is that every one of them also kept buying Nvidia, and most of the deals came with investment from the chip vendor.

:::timeline
- {date: 2025-10-23, headline: "Anthropic: up to 1M TPUs", body: "'Well over a gigawatt' online in 2026; Anthropic runs TPUs, Trainium and Nvidia GPUs."}
- {date: 2025-11-03, headline: "OpenAI–AWS $38B", body: "Seven-year deal for Nvidia GB200 and GB300 capacity."}
- {date: 2025-11-18, headline: "Anthropic–Azure $30B", body: "Up to 1 GW of Nvidia Grace Blackwell and Vera Rubin; Nvidia invests up to $10B."}
- {date: 2026-02-27, headline: "OpenAI commits ~2 GW of Trainium", body: "Alongside a $50B Amazon investment."}
- {date: 2026-04-06, headline: "Anthropic–Google–Broadcom", body: "'Multiple gigawatts' of next-generation TPU capacity from 2027."}
- {date: 2026-04-20, headline: "Anthropic–Amazon up to 5 GW", body: "New AWS capacity across Trainium generations; more than $100B AWS commitment over 10 years."}
- {date: 2026-10-29, headline: "Amazon Q3 call", body: "Jassy: most of Bedrock runs on Trainium; prior-gen Trainium capacity sells at a premium."}
:::

Anthropic agreed to use up to one million TPUs, with "well over a gigawatt" online in 2026, and described "a diversified approach that efficiently uses three chip platforms"[^23]. In April 2026 it added "multiple gigawatts of next-generation TPU capacity" through Google and Broadcom[^36]. It also committed to up to 5 GW of new AWS capacity spanning Trainium generations, and more than $100 billion of AWS spending over ten years[^24]. OpenAI committed to "approximately 2 gigawatts of Trainium capacity through AWS"[^26]. That came months after a $38 billion AWS deal for Nvidia GB200 and GB300 capacity[^27]. Anthropic also signed $30 billion with Azure for up to 1 GW of Nvidia Grace Blackwell and Vera Rubin systems, alongside up to $10 billion of Nvidia investment[^25]. Jassy said on the Q3 call that "short-term capacity for prior generation Trainium instances sell at a premium compared to the first half of the year"[^22]. On Alphabet's Q3 call, Google Cloud said nearly 100 customers use TPUs and guided to "a meaningful revenue ramp in 2027" for TPU system sales[^35].

The counter-evidence is about who can capture the edge. A leaked July 2025 Amazon document reported by Business Insider said Cohere found Trainium less competitive than H100 and Stability AI found Trainium2 less competitive on speed and cost. Amazon described Trainium2 users as mainly "a small number of large customers, such as Anthropic"[^30].

**Counterpoint.** Prior-generation Trainium selling at a premium is a sign of scarce compute, not proof of a cost edge; in a supply-constrained market, any accelerator sells. And investment-linked purchases are weak revealed preference, since Amazon funds the buyer that buys its chips[^24,26].

**Why this matters.** The buyers best placed to check SemiAnalysis's claim are behaving as if a cost edge exists for them. They are also hedging as if it might not last.

## 09. What could break the thesis

This article's thesis is that the TPU and Trainium edge is real but mostly a pricing result, concentrated among large-volume buyers and against Blackwell. Four findings would overturn it, in either direction.

1. **Reproducible Trainium3 runs show higher throughput.** If public logs show Trainium3 well ahead per chip at the comparison point, the "4% silicon" reading is wrong. That reading rests on a commentary extraction of the dashboard[^5] and on Crypto Briefing's matching "4%" figure[^4]. SemiAnalysis's free text does not print the per-chip numbers.
2. **AWS publishes a Trn3 price near $1 per chip-hour.** Trn2's $2.235 Capacity Block price is already below every Nvidia part on AWS's list[^13]. A published Trn3 price near SemiAnalysis's $1.05 would make the edge available to any AWS customer, not just to labs.
3. **Vera Rubin and TPUv8i results land as final.** If Rubin's preview multiples hold, the "at release" framing has a short shelf life[^8,12]. If TPUv8i and Trainium4 restore a similar edge over Rubin, the structural margin argument wins instead.
4. **SemiAnalysis's cost model is wrong about hyperscaler prices.** The Ironwood list price of $12.00 and the reported $1.60 Anthropic rate differ by 7.5x[^16]. Where a given buyer lands in that range decides the answer.

:::callout(kind=danger, label="Disclosure risk")
SemiAnalysis sells TCO and accelerator models to the industry it benchmarks. A third-party profile found no editorial-independence policy on its site[^39]. Google and Annapurna engineers co-developed or validated the stacks being measured: SemiAnalysis thanks Annapurna's Nafea Bshara and Ron Diamant for helping "validate our benchmark experiments"[^6,7]. That does not make the numbers wrong. It does mean independent reproduction matters more than usual.
:::

Red-team pass: 3/3 top claims unbroken. Adversarial searches found nothing contradicting the 2.28x decomposition, the AWS Capacity Block spread, or the Ironwood-versus-GB200 list comparison. The verifier rated most per-chip throughput figures "weak" only because they rest on a single commentary reading of the dashboard. The biggest open item is the unpublished Trainium3 price. Until AWS or Google prices these chips publicly, "1.5–2.5x better perf per dollar" answers a question most buyers cannot ask: what would a chip cost if you were Anthropic?

:::references
- {id: 1, title: "SemiAnalysis on X: TPU & Trainium are on InferenceX/AgentX", url: "https://x.com/SemiAnalysis_/status/2125867835050111357", source: "SemiAnalysis (X)", date: "2026-11-25"}
- {id: 2, title: "Jensen Huang – TPU competition, why we should sell chips to China, & Nvidia's supply chain moat", url: "https://www.dwarkesh.com/p/jensen-huang", source: "Dwarkesh Podcast", date: "2026-04-15"}
- {id: 3, title: "7 Months After Jensen Huang Said TPU And Trainium Would Never Show Up On InferenceMAX, Both Are Beating NVIDIA On It", url: "https://officechai.com/ai/7-months-after-jensen-huang-said-tpu-and-trainium-would-never-show-up-on-inferencemax-both-are-beating-nvidia-on-it/", source: OfficeChai, date: "2026-11-26"}
- {id: 4, title: "Trainium3 vs Nvidia GB300 inference benchmark", url: "https://cryptobriefing.com/trainium3-nvidia-gb300-inference-benchmark/", source: "Crypto Briefing", date: "2026-11-27"}
- {id: 5, title: "A 2.28x speedup that wasn't about speed: how to read an inference benchmark in 2026", url: "https://dev.to/iiruchating/a-228x-speedup-that-wasnt-about-speed-how-to-read-an-inference-benchmark-in-2026-5hbo", source: "DEV Community", date: "2026-11-27"}
- {id: 6, title: "AWS Challenger: Trainium3 Inference and Microarchitecture Deep Dive", url: "https://newsletter.semianalysis.com/p/trainium3-inferencex", source: SemiAnalysis, date: "2026-11-27"}
- {id: 7, title: "TPU Inference Externalization Full Steam Ahead (Ironwood on InferenceX)", url: "https://newsletter.semianalysis.com/p/tpu-inferencex-full-steam", source: SemiAnalysis, date: "2026-09-07"}
- {id: 8, title: "The Iron(wood) Throne: Google's TPU Stakes Its Claim on Inference", url: "https://newsletter.semianalysis.com/p/tpu-strikes-the-king", source: SemiAnalysis, date: "2026-11-05"}
- {id: 9, title: "Internal vs external TCO (glossary)", url: "https://inferencex.semianalysis.com/glossary/internal-vs-external-tco", source: "InferenceX", date: "2026-11-28"}
- {id: 10, title: "NVIDIA GB300 NVL72 chip page", url: "https://inferencex.semianalysis.com/chips/gb300-nvl72", source: "InferenceX", date: "2026-11-28"}
- {id: 11, title: "Vera Rubin NVL72 agentic inference", url: "https://newsletter.semianalysis.com/p/vera-rubin-nvl72-agentic-inference", source: SemiAnalysis, date: "2026-09-14"}
- {id: 12, title: "Rubin Gets 9x to 21x GB300's Tokens per Dollar in Benchmark", url: "https://fourweekmba.com/ai-rubin-gets-9x-to-21x-gb300s-tokens-per-dollar-in-benchmark/", source: FourWeekMBA, date: "2026-11-01"}
- {id: 13, title: "Amazon EC2 Capacity Blocks for ML pricing", url: "https://aws.amazon.com/ec2/capacityblocks/pricing/", source: AWS, date: "2026-11-28"}
- {id: 14, title: "Amazon EC2 Trn3 instances", url: "https://aws.amazon.com/ec2/instance-types/trn3/", source: AWS, date: "2026-11-28"}
- {id: 15, title: "Amazon EC2 Trn2 instances", url: "https://aws.amazon.com/ec2/instance-types/trn2/", source: AWS, date: "2026-11-28"}
- {id: 16, title: "Google Ironwood TPU pricing vs Nvidia (2026)", url: "https://shattered.io/google-ironwood-tpu-pricing-vs-nvidia-2026/", source: shattered.io, date: "2026-11-16"}
- {id: 17, title: "CoreWeave pricing", url: "https://www.coreweave.com/pricing", source: CoreWeave, date: "2026-11-28"}
- {id: 18, title: "Vast.ai rentable offers API (ARA gpu-spot lane snapshot)", url: "https://console.vast.ai/api/v0/bundles/", source: "Vast.ai via ARA", date: "2026-11-27"}
- {id: 19, title: "Azure Retail Prices API (ND GB200 v6, East US)", url: "https://prices.azure.com/api/retail/prices", source: "Microsoft Azure", date: "2026-11-28"}
- {id: 20, title: "Lambda pricing", url: "https://lambda.com/pricing", source: Lambda, date: "2026-11-28"}
- {id: 21, title: "Andy Jassy on Amazon's chips business, Q1 2026 earnings", url: "https://www.aboutamazon.com/news/company-news/amazon-ceo-andy-jassy-amazon-chips-business-q1-2026-earnings", source: Amazon, date: "2026-04-29"}
- {id: 22, title: "Amazon Q3 2026 earnings call transcript", url: "https://stockanalysis.com/stocks/amzn/transcripts/720308-q3-2026/", source: "Stock Analysis", date: "2026-10-29"}
- {id: 23, title: "Expanding our use of Google Cloud TPUs and services", url: "https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services", source: Anthropic, date: "2025-10-23"}
- {id: 24, title: "Anthropic and Amazon expand compute partnership", url: "https://www.anthropic.com/news/anthropic-amazon-compute", source: Anthropic, date: "2026-04-20"}
- {id: 25, title: "Microsoft, NVIDIA and Anthropic announce strategic partnerships", url: "https://www.anthropic.com/news/microsoft-nvidia-anthropic-announce-strategic-partnerships", source: Anthropic, date: "2025-11-18"}
- {id: 26, title: "OpenAI and Amazon partnership", url: "https://openai.com/index/amazon-partnership/", source: OpenAI, date: "2026-02-27"}
- {id: 27, title: "AWS and OpenAI announce multi-year strategic partnership", url: "https://www.aboutamazon.com/news/aws/aws-open-ai-workloads-compute-infrastructure", source: Amazon, date: "2025-11-03"}
- {id: 28, title: "AgentX methodology", url: "https://inferencex.semianalysis.com/infx/agentx", source: "InferenceX", date: "2026-11-28"}
- {id: 29, title: "Ironwood: The first Google TPU for the age of inference", url: "https://blog.google/products/google-cloud/ironwood-tpu-age-of-inference/", source: Google, date: "2025-04-09"}
- {id: 30, title: "Startups found Amazon's AI chips less competitive than Nvidia GPUs", url: "https://www.businessinsider.jp/article/startups-amazon-ai-chips-less-competitive-nvidia-gpus-trainium-aws-2025-11/", source: "Business Insider Japan", date: "2025-11-10"}
- {id: 31, title: "TPU megakernels", url: "https://inferact.ai/blog/tpu-megakernels", source: Inferact, date: "2026-09-23"}
- {id: 32, title: "TorchTPU - A Hybrid Eager/Compiled Architecture for Native PyTorch Execution on TPU", url: "https://arxiv.org/abs/2610.24161", source: arXiv, date: "2026-10-16"}
- {id: 33, title: "SemiAnalysisAI/InferenceX repository", url: "https://github.com/SemiAnalysisAI/InferenceX", source: GitHub, date: "2026-11-28"}
- {id: 34, title: "NVIDIA Blackwell Raises Bar in New InferenceMAX Benchmarks", url: "https://blogs.nvidia.com/blog/blackwell-inferencemax-benchmark-results/", source: NVIDIA, date: "2025-10-09"}
- {id: 35, title: "Alphabet Q3 2026 earnings call transcript", url: "https://tradingkey.com/news/transcripts/262249599-tradingkey", source: TradingKey, date: "2026-10-28"}
- {id: 36, title: "Anthropic expands partnership with Google and Broadcom", url: "https://www.anthropic.com/news/google-broadcom-partnership-compute", source: Anthropic, date: "2026-04-06"}
- {id: 37, title: "InferenceMAX: Open Source Inference Benchmarking", url: "https://newsletter.semianalysis.com/p/inferencemax-open-source-inference", source: SemiAnalysis, date: "2025-10-09"}
- {id: 38, title: "MLPerf Inference v6.0 results", url: "https://mlcommons.org/2026/04/mlperf-inference-v6-0-results/", source: MLCommons, date: "2026-04-01"}
- {id: 39, title: "SemiAnalysis / Dylan Patel profile", url: "https://qai.io/finance/funds/semianalysis-dylan-patel", source: qai.io, date: "2026-08-01"}
- {id: 40, title: "NVIDIA announces CEO transition (8-K exhibit)", url: "https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000082/nvidiaannouncesceotransiti.htm", source: "SEC EDGAR", date: "2026-11-12"}
- {id: 41, title: "NVIDIA Announces Financial Results for Third Quarter Fiscal 2027", url: "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx", source: "NVIDIA IR", date: "2026-11-17"}
- {id: 42, title: "NVIDIA Q3 FY2027 earnings call transcript", url: "https://www.fool.com/earnings/call-transcripts/2026/11/18/nvidia-nvda-q3-2027-earnings-call-transcript/", source: "Motley Fool", date: "2026-11-17"}
- {id: 43, title: "Broadcom Q3 FY2026 earnings call transcript", url: "https://www.webull.com/news/15511095937917952", source: Webull, date: "2026-09-02"}
- {id: 44, title: "TPUv7: Google takes a swing at the king", url: "https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the", source: SemiAnalysis, date: "2025-11-28"}
- {id: 45, title: "SemiAnalysis follow-up post on TPU and Trainium perf per dollar (via AGI Hunt)", url: "https://agihunt.info/en/p/1a21fd33be5aaaa5725e939e7b0", source: "AGI Hunt", date: "2026-11-28"}
- {id: 46, title: "NVIDIA 8-K: Jensen Huang reinstated as President and CEO", url: "https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000090/nov23pressrelease.htm", source: "SEC EDGAR", date: "2026-11-23"}
:::
