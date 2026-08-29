---
eyebrow: MARKETS · AI INFRASTRUCTURE
title: "The Moonshot Moment That Wasn't (Quite): What Actually Happened When Kimi K3 Met Wall Street"
deck: A tweet asked whether Jevons Paradox logic holds up a second time. The forensic answer — the July 2026 selloff was real, but smaller and more misattributed than the DeepSeek comparison implies, and the mechanism that actually explains both events is only partly about elasticity.
lede: |
  On July 17, 2026, Bloomberg's Joe Weisenthal floated a narrow but consequential question on X: does Moonshot AI's Kimi K3 shock replay January 2025's DeepSeek shock, or does "the Jevons Paradox logic" break down this time? Tracing the actual stock data, the actual DeepSeek recovery timeline, and the actual market structure underneath both events shows the popular comparison is doing more work than the facts support.
stats:
  - {label: "NVDA move, Jan 27 2025", value: "-17%", note: "-$588.8B, one day"}
  - {label: "NVDA move, Jul 16-17 2026", value: "-3.5%", note: "two days"}
  - {label: "Kimi K3 parameters", value: "2.8T", note: "1M-token context"}
  - {label: "Days to independent weight check", value: "10", note: "open weights due Jul 27, 2026"}
domain: finance
---

## 01. The tweet and the two "moments"

A single tweet on the afternoon of July 17, 2026 reopened a question markets thought they had already settled eighteen months earlier: does a cheaper, more capable Chinese open-weight model make the American AI-infrastructure trade more valuable, or less?

:::quote(attr="Joe Weisenthal, @TheStalwart, X, July 17 2026")
For markets, it's possible that the "Moonshot moment" doesn't play out the same way as DeepSeek did early last year.
:::

Weisenthal's tweet did more than note a coincidence of timing. He explicitly flagged that "the Jevons Paradox logic may be different this time" — the same efficiency-begets-more-demand argument that talked Nvidia off the ledge in January 2025 might not do the same work now. That is a testable claim, not a vibe, and testing it requires laying out every Chinese-model market moment between the two reference events side by side, because the tweet's premise — that there have only been two "moments" — is itself worth checking before anything else.

:::timeline
- {date: 2025-01-27, headline: "DeepSeek R1 releases", body: "Nvidia loses $588.8B in market cap in a single day, a ~17% decline — the largest one-day market-cap loss in stock-market history to that point [^1]."}
- {date: 2025-01-28, headline: "Nadella invokes Jevons Paradox", body: "Satya Nadella posts on X: \"Jevons paradox strikes again! As AI gets more efficient and accessible, we will see its use skyrocket, turning it into a commodity we just can't get enough of\" [^2]."}
- {date: 2025-07, headline: "Kimi K2 releases — no selloff", body: "Moonshot AI ships Kimi K2 with no comparable US chip-stock reaction; Nvidia crosses its first-ever $4T market cap the same week [^33][^34]."}
- {date: 2026-01, headline: "Kimi K2.5 releases — no reported reaction", body: "Moonshot's next iteration lands with no reported market moment at all [^33]."}
- {date: 2026-06, headline: "GLM-5.2 open-sourced", body: "Z.ai's release rallies Zhipu's own Hong Kong-listed shares +32.8% — a Chinese-stock story, not a US-semiconductor selloff [^35]."}
- {date: 2026-07-16, headline: "Kimi K3 releases", body: "Moonshot's largest model yet ships open-weight-bound; Nvidia falls 2.40% that day and a further 1.04% the next, a ~3.4% two-day decline [^12][^16]."}
:::

Laid end to end, the record between the two "moments" is thinner than the tweet's framing implies. Four Chinese frontier-model releases sit between DeepSeek R1 and Kimi K3 — Kimi K2, Kimi K2.5, GLM-5.2, and now Kimi K3 itself — and only one of them, the most recent, moved a US chip stock by more than a rounding error. Kimi K2 shipped into a market that pushed Nvidia to its first $4 trillion valuation the same week [^33][^34]; GLM-5.2 moved a Chinese stock, not an American one [^35]. Kimi K3 is the outlier that revived the comparison, and on paper it's a serious model: 2.8 trillion parameters, a 1M-token context window, $3/$15 per million input/output tokens, and a #4-of-189 ranking on the Artificial Analysis Intelligence Index with a score of 57, putting it in the neighborhood of Claude Opus 4.8 [^12]. But "serious model" and "DeepSeek-magnitude shock" are not the same claim, and the two-day Nvidia move it actually produced — roughly 3.5% [^16] — is an order of magnitude smaller than the 17%, $589B single-day move R1 triggered [^1].

That gap is the whole article's starting tension, and it cuts against treating the "Moonshot moment" label as self-evidently earned. Whether Kimi K3 is even the right comparison point for DeepSeek R1 — in capability, in market conditions, in what each release actually revealed about training or inference cost — is precisely what is contested here, not a premise this section is entitled to assume. Three other threads run underneath the price chart and need separating before any verdict is possible: whether Nadella's Jevons Paradox framing was ever the right model for what happened in January 2025, whether the market has simply gotten desensitized to Chinese model releases in the eighteen months since (which would explain the muted reaction to K2, K2.5, and GLM-5.2 without needing an elasticity argument at all), and whether Kimi K3's smaller reaction is proof the market shrugged or proof the market hasn't finished pricing it in.

None of that is answered yet — that's the rest of the article. What's established here is only the chronology and the shape of the question: one release moved markets by double digits, three didn't move them at all, and a fourth moved them by low single digits under a banner claiming Jevons-Paradox logic itself might be breaking. Getting the comparison right matters beyond a Twitter thread, because whether this is a repeat of DeepSeek, a muted echo, or a genuinely different mechanism determines whether anyone holding — or shorting — chip and AI-infrastructure equities should treat model-efficiency headlines as a buying signal, a selling signal, or noise.

## 02. What actually happened July 16-17, 2026 — separating signal from headline drift

The forensic question isn't whether a selloff happened on July 16-17, 2026 — it did — but whether the numbers now circulating actually describe it, and once the misattributed figures are stripped out, the verified Kimi K3-attributable move is real but far smaller than the DeepSeek shock it keeps getting compared to.

Start with what is directly attributable to the two trading sessions in question. On July 16, 2026, Marvell fell 8.71%, closing at $188.30 versus $206.26 the prior session [^13]. Intel fell 5.84% the same day, to $96.98 [^14]. AMD fell 5.33%, to $500.94 [^15]. Nvidia's move was more modest: -2.40% on July 16 (close $207.40) followed by a further ~-1.1% on July 17 (close ~$205), a cumulative two-day decline of roughly 3.5% [^16]. The Philadelphia Semiconductor Index (SOX) captures the sector-wide shape of the move: -4.29% on July 16 (close 11,867.50), then a further -1.03% on July 17 (close 11,745.4) — a combined two-session decline of about 5.3%, not the flat second day an earlier draft of this analysis mistakenly read off a stale data snapshot [^17].

:::bars
- {label: Marvell, value: "-8.71%", pct: 87}
- {label: Intel, value: "-5.84%", pct: 58}
- {label: "Philadelphia Semiconductor Index", value: "-5.32%", pct: 53}
- {label: AMD, value: "-5.33%", pct: 53}
- {label: Nvidia, value: "-3.5%", pct: 35}
:::

That is a real, broad-based semiconductor selloff — Marvell and Intel both down mid-to-high single digits in a single session is not noise. But set beside the January 27, 2025 DeepSeek shock, in which Nvidia alone lost $588.8B, or about 17% of its value, in one trading day [^1], the July 2026 move is a different order of magnitude. Nvidia's cumulative two-day decline this time was roughly a fifth the size of DeepSeek's one-day move, and even Marvell — the hardest-hit name in the July basket — fell about half as much in percentage terms as Nvidia alone fell in January 2025.

:::compare
- {role: HIGHEST, name: "DeepSeek shock, Jan 27 2025 (1 day)", value: "-17%"}
- {role: LOWEST, name: "Marvell, Kimi K3 shock (1 day)", value: "-8.71%"}
- {role: SUBJECT, name: "Nvidia, Kimi K3 shock (2 days)", value: "-3.5%"}
:::

The gap between the real move and the viral retelling is explained almost entirely by two misattributions. The first is the "$1 trillion in chipmaker value erased" / "SOX down more than 10% over two sessions" figure that has been recirculating as if it belonged to the Kimi K3 event. It doesn't: that number traces to a Broadcom-earnings-driven chip selloff on June 5, 2026 — six weeks before Moonshot AI shipped anything — and the original reporting makes no mention of Kimi K3 or Moonshot at all [^18]. The second is the claim that Alibaba jumped 5-9% "amid" the Kimi K3 selloff, offered as evidence that Chinese AI models were repricing the whole US-China compute trade. Alibaba's real multi-day surge — on the order of 11% to 17% — happened around July 8, 2026, driven by a DOJ settlement, a Pentagon litigation stay, and Nvidia's approval to sell H200 chips into China's cloud market, a distinct catalyst more than a week before Kimi K3 shipped [^19]. On the actual dates in question, Alibaba was flat-to-down: -0.17% on July 16 and -1.66% on July 17 [^19] — the opposite of the "AI-model-triggered rotation into Chinese tech" story that got attached to it.

:::callout(kind=warn, label="Headline drift")
Two of the most-repeated numbers from this event describe different events entirely. The "$1 trillion lost" / "SOX -10%" figures come from a Broadcom-earnings chip selloff on June 5, 2026, with zero reference to Kimi K3 in the original coverage [^18]. The "Alibaba up 5-9%" figure comes from a July 8, 2026 rally driven by a DOJ settlement and H200 China-cloud approval — over a week before Kimi K3 shipped, and on the actual July 16-17 dates Alibaba was flat-to-down [^19]. Both got folded into the Kimi K3 narrative simply because they landed in the same news cycle.
:::

None of this means the smaller-percentage framing settles the comparison. Nvidia's 2026 market capitalization is substantially larger than its January 2025 base, so a proportionally smaller decline can still represent a larger absolute dollar swing — a question this section deliberately leaves open, because none of the verified sources above report a 2026 market-cap figure precise enough to compute it without guessing. "Smaller shock" in percentage terms is not automatically "smaller shock" in dollar terms, and conflating the two would just be a subtler version of the same headline-drift error this section is correcting.

This matters because every downstream argument in this piece — about Jevons Paradox, about elasticity, about whether markets have gotten desensitized to open-weight Chinese model releases — is only as good as the underlying facts, and right now a meaningful share of the public "Kimi K3 shock" narrative is built on numbers that describe two unrelated events from adjacent weeks.

## 03. The DeepSeek "rescue" myth — Jevons Paradox's real track record

The version of the DeepSeek story that gets repeated every time a cheaper model rattles chip stocks — Nadella invoked Jevons Paradox, the market took the hint, and AI infrastructure demand proved itself unstoppable — is a retelling that compresses a slow, non-monotonic, multi-cause recovery into a one-line vindication, and the record does not support the clean version.

:::quote(attr="Satya Nadella, CEO, Microsoft, X post, Jan 26 2025")
Jevons paradox strikes again! As AI gets more efficient and accessible, we will see its use skyrocket, turning it into a commodity we just can't get enough of.
:::

Start with what actually happened to the stock. Nvidia lost $588.8B in market cap — roughly 17% — in a single session on January 27, 2025, the largest one-day loss for any company in market history [^1]. Nadella's Jevons framing landed the next day [^2], while the panic was still fresh, and it is the line everyone quotes. What gets dropped from the retelling is that the framing arrived as commentary on the shock, not as a data point about usage — nobody had a real-time measurement of AI-token consumption skyrocketing on January 28. It was a prediction, offered by the CEO of a company with an obvious interest in the AI-capex thesis holding, not a settled fact the market then priced in.

The first real move in the recovery direction wasn't a demand signal at all — it was a spend signal, and it undercut the shock's own premise rather than validating Jevons. Within days, SemiAnalysis reported that DeepSeek had actually spent well over $500M on GPUs and roughly $1.6B on total server buildout, directly contradicting the viral "$5.6M training run" framing that had triggered the sell-off in the first place [^4]. If DeepSeek's efficiency gain was real but smaller than advertised, then some of the early bounce reflected the panic itself being overcorrected — a repricing of a bad headline, not evidence that cheaper inference was inducing proportionally more of it.

:::timeline
- {date: 2025-01-27, headline: "DeepSeek shock", body: "Nvidia loses $588.8B (~17%) in a single session, the largest one-day market-cap loss on record. [^1]"}
- {date: 2025-01-31, headline: "Counter-narrative gains traction", body: "SemiAnalysis estimates DeepSeek actually spent well over $500M on GPUs and ~$1.6B on total server buildout, undercutting the '$5.6M' framing that drove the panic. [^4]"}
- {date: 2025-02-26, headline: "Huang's earnings-call reassurance", body: "Jensen Huang: 'Demand for Blackwell is amazing as reasoning AI adds another scaling law.' Nvidia reports Q4 FY25 revenue of $39.3B, +78% YoY. [^6]"}
- {date: 2025-04, headline: "A separate correction", body: "Nvidia falls below $100/share — a tariff-driven selloff unrelated to DeepSeek or Jevons. [^7]"}
- {date: 2025-05-28, headline: "Q1 FY26 earnings beat plus Middle East AI deals", body: "Strong quarterly results and newly announced Saudi/UAE chip agreements drive the stock up double digits — the actual proximate catalyst of the recovery. [^56]"}
- {date: 2025-06-25, headline: "New all-time high, ~5 months later", body: "Nvidia reclaims its pre-shock high on the earnings-beat/Middle East momentum, three weeks BEFORE the H20 policy reversal below. [^56]"}
- {date: 2025-07-15, headline: "H20 export ban reversed — a further leg up, not the initial recovery", body: "The China policy reversal Huang lobbied for lands after the stock had already made a new high, adding to the rally rather than causing the reclaim. [^7]"}
:::

The reassurance that actually moved analysts first wasn't Jevons at all — it was Jensen Huang's, delivered a full month later on Nvidia's first earnings call after the shock. Huang attributed continued demand strength to reasoning-model compute intensity: "Demand for Blackwell is amazing as reasoning AI adds another scaling law," alongside Q4 FY25 revenue of $39.3B, up 78% year-over-year [^6]. That is a distinct causal mechanism from Nadella's framing — Huang is arguing test-time compute scaling keeps inference expensive per query, not that cheaper models induce proportionally more total queries. Treating the two as the same "Jevons consensus" flattens a real disagreement about why demand held up.

And demand holding up in February did not mean the stock recovered. Nvidia fell back below $100 a share by April 2025, in a tariff-driven correction that had nothing to do with DeepSeek or efficiency narratives at all [^7]. What actually drove the reclaim of the January high was a concrete earnings beat and new Middle East chip deals: Nvidia's Q1 FY26 results, reported May 28, 2025, combined with newly announced Saudi Arabia/UAE agreements, pushed the stock to a fresh all-time high around June 25, 2025 — roughly five months after the shock [^56]. The Trump administration's reversal of the H20 China-export ban, which Huang had lobbied for directly, didn't land until July 15, 2025 — three weeks AFTER the stock had already made its new high — and drove a further leg of the rally rather than the initial recovery itself [^7][^56]. Correcting the popular timeline this way, if anything, strengthens rather than weakens the skeptical thesis: the recovery traces to a hard earnings beat and specific commercial deals, not to trade policy and certainly not to any real-time evidence that "usage skyrocketed" the way Nadella's framing implied. One analyst rebuttal published in the interim went further, arguing the coal analogy itself is weak: 19th-century coal was one undifferentiated commodity, whereas AI "efficiency" gains substitute one input mix for another and can just as easily enable creative destruction of incumbents — Nvidia, the US labs — as proportional demand growth for their existing infrastructure [^55].

:::callout(kind=info, label="What actually explains the recovery")
The recovery was slow, non-monotonic, and driven by a concrete earnings beat and Middle East chip deals in May-June 2025 — with the H20 export-ban reversal arriving weeks AFTER the stock had already reclaimed its high, as a second catalyst rather than the first — not by any observable "AI usage skyrocketed" data point in real time [^6][^56][^55].
:::

None of this means Jevons-style demand growth was fake — aggregate AI usage and revenue genuinely did grow enormously over the course of 2025, and that growth is real regardless of what caused the January-to-June share-price recovery specifically. The two claims are separable: usage can have skyrocketed and still not be the thing that explains why Nvidia stock spent five months underwater. What would weaken this section's argument is direct evidence that inference/token volumes measurably inflected upward within weeks of the DeepSeek release, ahead of the May earnings beat — that data point, if it exists, would restore the tight Jevons-as-immediate-cause story this section is disputing. Absent it, the burden sits with the popularized version, not the skeptical one.

This matters because the same one-liner is now being redeployed for Kimi K3: readers reaching for "Jevons rescued the market last time, so it will again" are borrowing a causal claim the historical record only weakly supports, and a five-month recovery driven by a hard earnings beat and specific commercial deals — with trade policy arriving as a second, later catalyst — is a very different bet to be making than a fast, demand-driven one.

## 04. Is Jevons Paradox even the right model? — the elasticity question

Jevons Paradox is not a universal law of cheaper inputs — it is a conditional prediction that only fires when demand for the resource in question is price-elastic, and whether AI inference clears that bar is an open empirical question the market keeps answering by assertion rather than by evidence.

The textbook version of the mechanism is narrower than the shorthand "cheaper compute → more compute demand" that gets applied to every model-pricing shock. Standard treatments contrast an elastic good, where a price cut induces proportionally more consumption, against an inelastic good like salt, where a 90% price cut would not make anyone eat ten times as much of it — the same job (seasoning food) gets done more cheaply, with no proportional growth in the number of jobs [^10]. Which bucket AI inference falls into is not self-evident. A lot of inference spend is committed to fixed workloads — a customer-support bot answering a roughly fixed volume of tickets, a coding agent running a roughly fixed number of CI checks — where a lower per-token price just lowers the bill for the same amount of work, which is the salt case, not the elastic case.

==Unverified: a specific numeric elasticity estimate for Anthropic's API pricing was checked against the secondary source that supposedly reported it and could not be confirmed there or anywhere else in an independent search — it does not appear in the cited analysis and no corroborating figure was found, so it is dropped here rather than repeated.== What the qualitative literature on the subject does support is more modest: AI-inference pricing almost certainly sits somewhere between the fully-inelastic "salt" case and the fully-elastic textbook case, with the mix skewed toward fixed, already-committed workloads (support bots, CI pipelines) where a lower per-token price mostly just lowers the bill rather than unlocking materially more volume [^10]. Absent a credible measured elasticity for AI inference specifically, the honest position is that the sign of the effect (some elasticity exists) is more defensible than any claimed magnitude — and a market pricing in a *specific* elasticity number, rather than the mere existence of one, is pricing in more precision than the evidence supports.

That gap between the two readings — genuinely new use cases unlocked versus the same fixed workload billed at a lower rate — is the fork this section exists to name, and it is also testable directly against the shock the rest of this article is examining. Kimi K3 is priced at $3/$15 per million input/output tokens, independently verified as "somewhat expensive" relative to average model pricing — not the dramatic undercut that DeepSeek R1 was framed as delivering in January 2025 [^12]. If the Jevons framework is the right lens at all, that pricing should predict a smaller demand-unlock effect from K3 than from a genuinely cheap release, because the mechanism's own logic ties the size of the rebound to the size of the price cut — a modest cut should buy, at most, a modest rebound, if it buys one at all.

There is also a structural objection to reaching for the 19th-century analogy in the first place. One financial-analyst critique argues that Victorian coal was a single undifferentiated commodity, elastic in aggregate — burn coal cheaper, burn more of it, full stop. AI "efficiency" gains do not necessarily work that way: a cheaper or more capable model can instead substitute one input mix for another — one vendor's tokens for another's, one architecture for another's — which is Schumpeterian creative destruction of incumbents, a redistribution mechanism, not the aggregate-consumption-rebound mechanism the coal story describes [^55]. Those two mechanisms produce opposite verdicts for the same headline: substitution is compatible with total AI infrastructure revenue falling even as usage holds constant, exactly the outcome Jevons Paradox is invoked to rule out.

:::kv
- {term: "Condition for Jevons Paradox to apply", def: "Demand must be price-elastic — a cheaper resource must unlock genuinely new/expanded use, not just cheaper delivery of the same fixed amount of use"}
- {term: "Confidently claimed elasticity magnitudes for AI inference", def: "None survive independent verification as of this writing — treat any specific number circulating as unconfirmed until a primary source discloses it"}
:::

This matters because the market's post-shock relief rally treats "Jevons Paradox will save this trade" as a law rather than a hypothesis, and hypotheses need falsification conditions, not applause.

:::callout(kind=info, label="The test this section applies")
Does Kimi K3-style competition make AI inference cheaper in a way that unlocks NEW use cases and NEW total volume (Jevons-consistent), or does it just let the same volume of existing work get done for less money (Jevons-inconsistent, and actually bad for revenue-per-token infrastructure providers)?
:::

## 05. The bull case: agentic compute intensity is genuinely different this time

The strongest version of the bull case does not rest on Jevons Paradox as an abstract law — it rests on a concrete, measurable shift in what a "unit of AI usage" actually costs in compute, and by that measure mid-2026 looks structurally unlike January 2025.

In January 2025, when DeepSeek's cheaper training run rattled markets, "AI usage" for the overwhelming majority of paying traffic meant a single chat turn: a prompt in, a completion out, a few hundred to a few thousand tokens total. By mid-2026, a large and growing share of frontier-model demand instead comes from agentic workloads — coding agents, autonomous multi-step task runners, tool-calling pipelines — that do not resemble that pattern at all. Gartner's March 2026 analysis quantifies the gap directly: a standard chatbot interaction is the baseline, but agentic tasks run 5-30x that in tokens, with simple tool-calling agents consuming 5,000-15,000 tokens per task, complex multi-agent systems running 200,000 to over 1,000,000 tokens per task, and agentic coding workflows averaging 1 to 3.5 million tokens per task once retries are counted [^42]. That is not a marginal efficiency change; it is a different order of magnitude of compute consumed per completed unit of work.

This shift shows up in platform-level data, not just vendor benchmarking. OpenRouter's own "State of AI" analysis found programming's share of total token volume on its platform rose from roughly 11% at the start of 2025 to over 50% by the end of the year, with agent-driven workflows generating more than half of all output tokens by December 2025 [^43]. That is a compositional shift in demand, not merely a growth story — the mix of what the median token is being spent on moved from conversational completions toward iterative, tool-using, multi-step execution, which is exactly the category Gartner shows costs 5-30x more per task.

:::stats
- {label: "Compute per agentic task vs. prior generative-AI era", value: "~10x", note: "Huang's figure, reported inconsistently as '1,000%' or '1,000x' across outlets — ServiceNow Knowledge 2026, May 2026"}
- {label: "Tokens per agentic task vs. chat", value: "5–30x", note: "up to 1–3.5M for agentic coding, Gartner Mar 2026"}
- {label: "OpenRouter programming token share", value: ">50%", note: "up from ~11% start of 2025"}
- {label: "Anthropic Q1 2026 usage growth", value: "~80x", note: "vs. 10x planned (Amodei)"}
:::

Two data points sharpen the picture further. Nvidia CEO Jensen Huang, speaking at ServiceNow's Knowledge 2026 conference in May, put a number on the same phenomenon from the supply side: compute required per agentic-AI workload has risen sharply versus earlier generative-AI-era usage — secondary coverage of the same remarks reports the figure inconsistently, some outlets rendering it as "1,000%" (~10x) and others as "1,000x," a materially different magnitude the original wording does not cleanly resolve — because agents read, reason, invoke tools, and generate far more tokens per completed task than chat-era interactions ever did [^41]. And on the demand side, Anthropic CEO Dario Amodei disclosed that the company had planned for 10x usage and revenue growth in Q1 2026 but actual annualized growth came in around 80x — a gap he attributed directly to the compute shortage the surge produced, substantially driven by coding and agentic use [^44]. The aggregate throughput trend is consistent with both: OpenRouter's platform-wide token volume scaled from roughly 5 trillion tokens per week in April 2025 to over 20 trillion tokens per week in April 2026, a roughly fourfold increase in a single year even as the model mix shifted toward cheaper Chinese open-weight models [^31].

:::slope(left-label="April 2025", right-label="April 2026", unit="T tokens/wk")
| Item | April 2025 | April 2026 |
|---|---|---|
| OpenRouter platform token throughput | 5 | 20 |
:::

The mechanism this points to is specific, not hand-wavy: agents burn tokens on tool calls, on multi-step chain-of-thought reasoning, and on repeatedly resending accumulated context on every turn of a long-running task — none of which existed at scale in the January 2025 usage mix. That means the same dollar of cheaper-per-token pricing now buys categorically more total compute consumption per completed unit of work than it did during the DeepSeek shock, because the unit of work itself changed shape. If elasticity is the right frame at all, this is the channel through which falling per-token prices could plausibly translate into rising aggregate compute demand rather than falling revenue — not because users respond to price signals the way commodity-demand curves assume, but because the task composition of demand shifted toward inherently token-hungry workloads independent of price.

The skepticism has to be equally specific, though. Huang has a direct financial stake in a bigger-compute-demand narrative — Nvidia sells the chips agentic workloads consume — so his 1,000% figure should be read as informed but interested-party commentary, not neutral measurement [^41]. Amodei's 80x is a single quarter's annualized extrapolation, not a demonstrated steady-state growth rate, and one-quarter spikes are exactly the kind of number that regresses toward trend once a novelty effect wears off [^44]. And the OpenRouter throughput trend, while real, is also fully consistent with an entirely different explanation than price elasticity: simple category growth and new-user adoption of agentic tools would produce the same quadrupling in total tokens even if the price of a token had never moved at all — rising volume does not by itself prove the elasticity mechanism the bull case needs.

This matters because it is the one place in the whole DeepSeek-January-2025-versus-now debate where the bull case has something Section 04's contested-elasticity question lacked: an actual structural change in the unit of demand, not just an assumption that cheaper compute must eventually get used up.

## 06. The bear case: this shock landed on an already-fragile market

Kimi K3 did not arrive as a bolt from a clear sky the way the original DeepSeek shock did in January 2025 — it landed on a market that had spent the prior two weeks accumulating specific, documented reasons to distrust the AI-capex financing structure underneath the entire trade, which reframes July 16-17 as a trigger for a pre-existing vulnerability rather than an independent new risk.

Start with positioning. Goldman Sachs' prime-brokerage book showed hedge funds net-selling semiconductor and hardware single-name stocks for four straight weeks through July 3, 2026 — while continuing to buy the broad index and ETF wrapper [^28]. That is not indiscriminate risk-off; it is a rotation out of single-name chip exposure specifically, and it was already three weeks old by the time Kimi K3 shipped. Six days later, on July 9, S&P Global cut Oracle from BBB to BBB- — one notch above speculative grade — citing AI-capex leverage and revenue concentration in OpenAI directly [^25]. A credit downgrade of that magnitude, on that rationale, from a ratings agency rather than a momentum trader, is a structural signal: it says the balance sheet, not just the stock price, was already flagged as stretched before Kimi K3 existed as a headline. Four days after that, on July 13, Michael Burry — a name synonymous with pre-crisis positioning — disclosed a short against Nvidia and specifically flagged aggressive GPU-depreciation-schedule accounting as the mechanism he doesn't trust [^26]. None of this required Kimi K3. All of it was already on the tape.

:::timeline
- {date: 2026-07-03, headline: "Hedge funds' fourth straight week net-selling chip stocks", body: "Single-name semiconductor and hardware exposure trimmed while broad index/ETF buying continues — rotation, not blanket risk-off."}
- {date: 2026-07-06, headline: "Goldman prime-brokerage data confirms the rotation", body: "Prime-brokerage positioning data makes the four-week de-risking pattern visible to the wider market."}
- {date: 2026-07-09, headline: "S&P downgrades Oracle to BBB-, citing AI-capex leverage and OpenAI concentration", body: "One notch above speculative grade — a credit-rating agency, not a short-seller, flags the balance sheet."}
- {date: 2026-07-13, headline: "Michael Burry discloses Nvidia short, flags GPU-depreciation risk", body: "A prominent bear names the specific accounting mechanism he distrusts: depreciation schedules on GPU fleets."}
- {date: 2026-07-16, headline: "Kimi K3 releases into this already-jittery market", body: "The release that triggered the selloff was the fifth event in a two-week sequence, not the first."}
:::

What made the balance-sheet worry credible in the first place is the scale of the circular financing web underneath it. Market estimates put the Nvidia-OpenAI-Oracle-Microsoft-AMD-CoreWeave web of cross-investment and vendor-financing arrangements at over $800B [^27] — and OpenAI's own disclosed infrastructure commitments alone total roughly $1.15 trillion across seven vendors, an obligation structure where the company's largest "customers" are simultaneously its largest investors and lenders:

:::rank-list
- {label: Broadcom, value: "$350B", pct: 100}
- {label: Oracle, value: "$300B", pct: 86}
- {label: Microsoft, value: "$250B", pct: 71}
- {label: Nvidia, value: "$100B", pct: 29}
- {label: AMD, value: "$90B", pct: 26}
- {label: AWS, value: "$38B", pct: 11}
- {label: CoreWeave, value: "$22B", pct: 6}
:::

Figures are rounded market estimates, not audited disclosures [^27] — but the order of magnitude is what matters: a $1.15T commitment stack concentrated in seven counterparties, several of whom are also equity or debt participants in the entities they're selling to, is a structure where reported revenue growth is partly self-referential. That is precisely the kind of leverage a credit downgrade [^25] and a depreciation-accounting short thesis [^26] are built to interrogate, and it is precisely the kind of structure that turns "one open-weights model from a Chinese lab looks unexpectedly good" into a systemic scare rather than a sector-specific one.

Put the sequence together and the "last straw, not a bolt from the blue" framing holds: a market that had been quietly de-risking single-name chip exposure for a month [^28], had just been told by a major rating agency that its bellwether AI-infrastructure vendor was one downgrade from junk [^25], and had just watched a well-known short-seller publicly stake a position against the sector's most important supplier on an accounting thesis [^26] was primed to sell off hard on any negative catalyst — independent of whether that catalyst was Kimi K3 specifically, a weak hyperscaler capex guide, or something else entirely.

The necessary counterpoint: none of this implies Kimi K3 was irrelevant or that the selloff was "really" about financing structure and not about the model. Pre-existing fragility and Kimi K3 being a real, independently negative catalyst are not mutually exclusive — a fragile market amplifies a genuine shock, it does not manufacture a fake one out of nothing. Kimi K3's efficiency claims still had to be real enough to move capex-intensity assumptions for the selloff to find its trigger; a market this jittery would not have cratered on a non-event. What the fragility evidence changes is the counterfactual: had Kimi K3 shipped into the relatively unworried market of, say, six months earlier, the same technical shock plausibly produces a smaller, more contained move.

This distinction is exactly what an investor betting on "Jevons will rescue it again" needs to price correctly. Betting on Jevons Paradox as the rescue mechanism only works if July 2026 is a repeat of the relatively isolated, single-cause DeepSeek shock of January 2025. If instead the market is now structurally more leveraged — via circular financing [^27] — and already flagged as such by a rating agency [^25], a known short [^26], and smart-money positioning [^28] before Kimi K3 ever shipped, then the relevant base rate isn't "how did the market recover from one surprising model" but "how does an already-fragile, circularly-financed capex cycle behave under repeated shocks." Those are different bets with different tail risk, and conflating them is the single easiest way to misprice what comes next.

## 07. Substitution vs. new demand — where does the marginal token actually go

The rising Chinese-model usage share documented in Section 02 forces a mechanism question the bull/bear framing in Sections 05-06 mostly skips past: when a token that used to run on Claude or GPT now runs on DeepSeek or Kimi, has the AI pie grown (Jevons-consistent) or just been redivided (Jevons-neutral for the pie, Jevons-hostile for the vendor who lost the token) — and either way, does the answer change what NVIDIA sells?

Start with the redivision, because it is not speculative. CNBC's OpenRouter breakdown shows Chinese-origin models exceeding 30% of US-company token usage every single week since February 8, 2026, peaking near 46%, against an 11% trailing-12-month average and just 4.5% in H1 2025 [^30] — a share shift too fast and too sustained to read as noise. On the platform today, DeepSeek holds roughly 17.6% of routed tokens and Alibaba's Qwen roughly 13.9%, while Anthropic, the largest single US-origin vendor on OpenRouter, captures only about 14.8% [^30] — two Chinese labs, combined, already out-route the leading American one.

:::donut(center-label="OpenRouter tokens")
- {label: DeepSeek, value: 17.6}
- {label: Qwen, value: 13.9}
- {label: Anthropic, value: 14.8}
- {label: Other, value: 53.7}
:::

That is not an abstraction. It has a name and a dollar figure attached.

:::callout(kind=warn, label="A documented substitution case")
AI startup Lindy moved 100% of its production traffic from Anthropic's Claude to DeepSeek, citing multi-million-dollar savings [^30]. This is not a hypothetical elasticity argument — it is one customer's entire workload migrating wholesale from a US-hosted frontier model to a Chinese open-weight one, for a stated reason (cost) that scales to any workload sensitive to per-token price. For a substitution-driven bear case on model-layer vendors, Lindy is Exhibit A: this is what "share loss" looks like at the level of an individual buying decision, not a statistical drift.
:::

So the model layer has a real substitution story. Does the chip layer inherit it? This is where the naive "Chinese models threaten American AI" framing collapses two different questions into one, and the answer diverges. The actual cloud infrastructure serving popular Chinese open-weight models — the OpenRouter-listed providers that route DeepSeek, Kimi, and GLM traffic, including GMI Cloud, Together AI, Fireworks AI, DeepInfra, and Parasail — runs predominantly on Nvidia H100/H200 GPU infrastructure, not Huawei Ascend or other non-Nvidia silicon [^32]. Self-hosting Kimi K2.6, for instance, is specified as requiring "8x H100 or H200 with Q4 weights (~620GB VRAM)" [^32] — Nvidia parts, not a domestic alternative. Lindy's traffic did not leave the Nvidia compute base when it left Claude; it moved from one Nvidia-hosted inference stack to another. The token substitution is real at the model-vendor layer and largely invisible at the chip layer, because both sides of that substitution are, in practice, still Nvidia GPU cycles being billed by different companies.

Layer on the aggregate-demand context: OpenRouter's platform-wide throughput scaled from roughly 5 trillion tokens/week in April 2025 to over 20 trillion tokens/week in April 2026 — the pie roughly quadrupled over the same span that its composition shifted hard toward Chinese open-weight models [^31]. That is a partial Jevons-consistent signal sitting directly on top of a partial substitution signal: total inference volume grew ~4x while US-lab share of that volume fell, and the infrastructure underneath the growth stayed Nvidia-denominated regardless of which model brand won the routing decision. Put together, [^31] and [^32] argue that "Chinese models are taking share" and "Nvidia demand is threatened" are not the same claim, however naturally they get bundled in headline coverage — a dollar of inference spend can migrate labs entirely while the GPU-hour underneath it barely moves.

The obvious counterpoint is that this decoupling is an artifact of where the measurement was taken, not a structural guarantee. OpenRouter is a third-party marketplace; its infrastructure partners are Western GPU clouds by construction, so of course they run Nvidia. The load-bearing risk this section does not resolve is what happens to usage that never touches OpenRouter at all — the first-party infrastructure Chinese labs run themselves, domestically, for their home markets and increasingly for export customers who route around US-adjacent platforms. If DeepSeek, Moonshot, or Zhipu's own hosted APIs are increasingly served on Huawei Ascend or other domestic accelerators rather than Nvidia parts, that slice of the substitution would be genuinely bearish for Nvidia — a token leaving Claude for a Chinese lab's own Ascend cluster is share loss at both layers simultaneously, with no Nvidia-cycle offset. Nothing in the OpenRouter-sourced evidence here measures that slice; it is a real, unresolved exposure this argument does not fully address, and its size likely matters more to the long-run NVDA thesis than the OpenRouter numbers do.

Why this matters: the market's fastest available signal for "is the AI trade breaking" is model-layer usage share, which moves weekly and is where headlines like [^30] concentrate — but if that signal is currently decoupled from actual chip demand because the underlying compute stays Nvidia either way, then a further deterioration in US-lab OpenRouter share is not, by itself, sufficient evidence for a bearish Nvidia call; the falsification test has to look at where the infrastructure, not the brand, sits.

## 08. The desensitization pattern — and why Kimi K3 broke it

Three Chinese frontier-model releases in the eighteen months after DeepSeek R1 produced no comparable US chip-stock selloff at all — and that quiet stretch is itself the puzzle this section examines, because Kimi K3 in July 2026 ended it.

:::rank-list
- {label: "DeepSeek R1, Jan 2025", value: "-17%", pct: 100, rank: 1}
- {label: "Kimi K3, Jul 2026", value: "-3.5%", pct: 21, rank: 2, highlight: true}
- {label: "Kimi K2, Jul 2025", value: "~0%", pct: 1, rank: 3}
- {label: "Kimi K2.5, Jan 2026", value: "~0%", pct: 1, rank: 4}
- {label: "GLM-5.2, mid-2026 (US chips)", value: "~0%", pct: 1, rank: 5}
:::

The pattern looks like textbook market learning. R1 cost Nvidia -17%, -$588.8B in a single day [^1] — the shock that taught markets to associate a cheap, capable Chinese open-weights model with an existential threat to the US AI-capex thesis. Six months later, Kimi K2 landed with analysts pre-announcing the muted outcome: commentary before the release explicitly predicted only a "much slower style" DeepSeek Moment, because K2 lacked the two features that made R1 go viral — a visible chain-of-thought and a novel shockingly-cheap training-cost claim [^33]. The market obliged: Nvidia crossed its first-ever $4 trillion market cap the same week K2 shipped, with no negative reaction at all [^33][^34]. Kimi K2.5 in January 2026 didn't even register as an adversarial event — no US chip-stock reaction shows up in contemporaneous coverage, and instead Nvidia launched GPU-accelerated hosting endpoints for K2.5, a commercial-partner relationship rather than a competitive-threat one [^33]. GLM-5.2 in mid-2026 went further still: it triggered a +32.8% close (intraday +48%) rally in Zhipu's own Hong Kong-listed shares, the mirror image of a US semiconductor selloff, with one contemporaneous analysis noting explicitly that "US AI equities have not yet been forced into a full rethink" by the release [^35]. Three releases, one from the same lab that shipped R1, and the US chip-stock reaction across all three rounds to roughly zero.

Then Kimi K3 broke it. Nvidia fell -2.40% on the first day and roughly -1.1% on the second, a cumulative ~3.5% two-day decline [^16] — an order of magnitude smaller than R1's -17% single-day move, but the first negative US chip-stock reaction to a Chinese model release in the eighteen months since January 2025. That's the fact this section has to explain: why did the fourth release in this sequence produce a real, if modest, selloff when the second and third produced none, and the same lab's own prior release produced none?

Three candidate explanations sit on the table, and the evidence assembled here doesn't cleanly adjudicate between them. First, K3 may simply have been a bigger deal on its technical merits — a 2.8T-parameter model with a competitive frontier-benchmark rank (see section 01's framing of the scale claim) could plausibly be the first release since R1 to read as a capability inflection rather than incremental progress, in which case "desensitization" never really applied and investors were correctly discriminating between genuinely threatening releases and merely competent ones. Second, K3 landed on a market already primed to de-risk the AI-capex trade for reasons unrelated to any single model release (developed at length elsewhere in this article); a similarly-sized surprise dropped into that more fragile backdrop could produce a bigger reaction than an identical surprise would have generated against the calmer tape of mid-2025 or early 2026. Third, simple reversion is on the table too — after three consecutive non-events from the same competitive vector, some reaction was arguably overdue on priors alone, independent of what K3 specifically contained.

The honest caveat is that the absence of a selloff around K2, K2.5, and GLM-5.2 is not, by itself, strong evidence of genuine market learning. It is equally consistent with those three releases simply being — on their own technical and narrative merits — less threatening than either R1 or K3, a confound this section's design cannot separate from the desensitization story: a null result across three data points proves the market didn't panic, not why it didn't. One additional data point worth weighing on the "market learning is real" side: the K2.5 case isn't merely neutral, it's actively cooperative — Nvidia building hosting infrastructure for a Chinese frontier model is a stronger signal of assimilated non-threat status than silence alone would be.

This matters because it reframes the whole "why was July 2026 smaller than January 2025" question this article opens with: the muted reaction may have less to do with any elasticity or substitution mechanism in AI-compute demand and more to do with markets' pattern-recognition over which announcements now warrant a reaction at all — a behavioral explanation sitting alongside, not necessarily competing with, the economic ones examined in the sections that surround it.

## 09. Reading past the "sold out" reassurance — the real falsification test

Every piece of evidence cited in the 24 hours after Kimi K3 to argue "AI-chip demand is fine" was locked in before anyone at TSMC, Alphabet, Microsoft, Meta, or Amazon had seen the release — which means the real test of whether the shock changes anything hasn't happened yet, and it arrives on a specific, dated calendar.

Start with the line that did the most reassuring: TSMC's CoWoS packaging capacity is "sold out." That quote is real, but it is stale by design — CEO C.C. Wei said it at TSMC's annual shareholder meeting on June 4, 2026, six full weeks before Kimi K3 existed as a headline [^36]. Repeating it on July 17 as evidence that this week's demand is intact describes a different moment, not the current one. TSMC's Q2 2026 earnings print landed on July 16, the same calendar day as the Kimi K3 release, and showed 33.7% YoY revenue growth with FY2026 capex guidance raised to $60-64B from $52-56B [^37]. That looks like unambiguous confirmation — until you account for lead times: wafer starts and packaging bookings reflected in a Q2 print were committed many months earlier, so the number is mechanically incapable of reflecting a same-day release. Tellingly, when a UBS analyst pushed CFO Wendell Huang on that same call for a specific three-year forward capex figure, he declined outright: "We do not have a number to share with you" [^37]. The company that supposedly just proved demand is fine would not commit to a forward number on the record.

The hyperscaler side of the reassurance is even more clearly backward-looking. None of Alphabet, Microsoft, Meta, or Amazon had reported Q2 2026 earnings as of July 17-18 — their dates fall entirely after the shock: Alphabet on July 22, Microsoft and Meta on July 29, Amazon on July 30 [^38]. The widely quoted ~$725B combined 2026 capex guidance figure was set at Q1 earnings in late April, roughly three months before Kimi K3 existed [^38]. So the two most commonly cited "demand is fine" data points — TSMC's sold-out packaging and the hyperscalers' three-quarters-of-a-trillion-dollar capex guide — were both decided before the thing they are supposedly reassuring us about had happened. Neither is evidence about Kimi K3. Both are evidence about the world as of April and June.

:::timeline
- {date: 2026-06-04, headline: "TSMC's Wei says CoWoS packaging 'sold out through 2026'", body: "Stated at the annual shareholder meeting, six weeks before Kimi K3."}
- {date: 2026-07-16, headline: "TSMC reports Q2 earnings, raises capex guidance", body: "Same calendar day as Kimi K3; reflects bookings made months earlier. CFO declines to give a forward 3-year capex figure."}
- {date: 2026-07-16, headline: "Kimi K3 releases", body: "The shock this article is testing the aftermath of."}
- {date: 2026-07-22, headline: "Alphabet reports Q2 2026", body: "First hyperscaler capex read since the shock."}
- {date: 2026-07-29, headline: "Microsoft and Meta report Q2 2026", body: "Second wave of post-shock capex commentary."}
- {date: 2026-07-30, headline: "Amazon reports Q2 2026", body: "Final of the four large US hyperscalers to report."}
- {date: 2026-08-26, headline: "Nvidia reports Q2 FY2027", body: "Pre-shock guidance was $91.0B ±2%; watch for reaffirm, raise, or cut."}
:::

So what actually is live right now, independent of any executive's talking points? GPU spot pricing. H100 cloud rental rates have fallen roughly 64-75%, from $8-10/hr in Q4 2024 to $2-3/hr in early 2026, as more than 300 new GPU cloud entrants added supply [^39]. Read in isolation, that looks bearish — a real-time, sentiment-independent signal of oversupply. But it is oversupply concentrated in older-generation compute; Blackwell and B200 capacity remained reservation-only and scarce through mid-2026 even as H100 prices cratered [^39]. That is a genuinely mixed signal, not a clean directional one — it says last-generation compute got cheap and fungible while frontier compute stayed scarce, which is a normal capacity-migration pattern and not obviously a verdict on whether Kimi K3 changes anyone's spending plans.

:::stats
- {label: "Nvidia Q2 FY2027 guidance (pre-shock)", value: "$91.0B", note: "±2%, reports Aug 26 2026 — watch for reaffirm/raise/cut"}
- {label: "Combined hyperscaler FY2026 capex guide (pre-shock)", value: "~$725B", note: "set late April 2026, watch for revision Jul 22-30"}
- {label: "H100 GPU cloud rental rate", value: "$2-3/hr", note: "down 64-75% from $8-10/hr in Q4 2024; B200 still reservation-only"}
:::

The falsification test, then, is not "did TSMC's quarter look good" — it already did, and it doesn't tell us anything about the shock. It is whether Nvidia's August 26 guidance holds at roughly $91B, whether the four hyperscalers revise their combined ~$725B capex number up, down, or not at all across the July 22-30 window, and whether H100/B200 spot pricing starts moving in a way that reflects a genuine demand shift rather than ordinary generation-to-generation migration.

:::callout(kind=warn, label="Counterpoint")
Even a materially negative hyperscaler reaction to Kimi K3 might not show up as a capex cut inside this window. Multi-year data-center leases and chip-supply contracts are not features you cancel in a quarter — they're the kind of commitment that unwinds, if it unwinds at all, across several more quarters of guidance revisions. That means the test this section proposes has its own lag, and August 26 will not fully resolve the question either; it is the first hard data point, not the last one.
:::

This matters because the entire "Jevons rescue" narrative examined in sections 03-04 rests on an empirical claim — that falling inference cost expands total compute demand rather than substituting for it — and that claim is falsifiable only against forward-looking numbers, not backward-looking ones dressed up as reassurance.

## 10. What would break this thesis

This article's core finding — that the "Moonshot moment" is real but smaller, partly built on misattributed headlines, and shaped as much by market structure and desensitization as by any Jevons-Paradox economics — rests on evidence that is itself incomplete. Six specific developments, most already on a dated calendar, would force a rewrite.

First, independent verification is still pending. Kimi K3's full open weights were not scheduled for release until July 27, 2026, ten days after the shock this article examines — meaning the API benchmark rankings that helped justify even the modest market reaction had not yet been independently reproduced by outside researchers at the time of writing [^12]. If the open-weight release shows K3 underperforming its API-reported scores, the "capability inflection" explanation offered in Section 08 collapses, and the muted reaction looks retrospectively like the better-calibrated call, not an anomaly to be explained away.

Second, the forward tests laid out in Section 09 could resolve the other way. If Nvidia's August 26, 2026 guidance is cut, or the four hyperscalers trim their combined ~$725B 2026 capex guidance across the July 22-30 window, that would be direct evidence the market was right to treat Kimi K3 as a genuine inflection point rather than an overreaction to partly misattributed headlines [^45][^38].

Third, the Nvidia-insulation argument in Section 07 has one specific, unresolved failure mode: if Chinese labs increasingly shift their own first-party infrastructure onto domestic silicon rather than Nvidia GPUs, the "substitution without chip-demand loss" story breaks down, and rising Chinese-model usage share becomes straightforwardly bearish for Nvidia after all [^32].

Fourth, if the circular-financing structure described in Section 06 — upward of $800B in cross-investment, OpenAI's $1.15T in vendor commitments — begins to visibly unwind (a credit event at Oracle, say, following its BBB- downgrade), that validates the "already-fragile market" bear case entirely on its own terms, independent of anything Jevons Paradox does or doesn't explain [^25][^27].

Fifth, a confound this article has not fully separated out: the macro backdrop was measurably calmer in July 2026 than in January 2025. The Federal Reserve's policy rate stood at 3.50-3.75% heading into the Kimi K3 shock — 75 basis points below the 4.25-4.50% rate in effect during the DeepSeek shock — and the VIX spiked only to roughly 18 (about +13%) on July 17, 2026, versus a panic-grade jump to 21.56 (+45%) on January 27, 2025 [^46][^47]. Some of the smaller Kimi K3 reaction plausibly reflects a more risk-tolerant macro environment rather than anything specific to Jevons Paradox, market desensitization, or the model's actual capabilities — a genuine confound the evidence assembled here cannot cleanly rule out.

Sixth, and more suggestive than conclusive: as of this writing, neither Satya Nadella nor Jensen Huang has publicly re-invoked the Jevons Paradox framing in connection with Kimi K3, despite financial media explicitly drawing the same "DeepSeek moment" analogy that originally produced Nadella's January 2025 framing [^48]. Huang's most recent on-record mention of Moonshot's models predates K3 by four months [^49]. That silence could mean the framing is now so well-established it doesn't need repeating — or it could mean the executives who popularized it are more cautious about restating a claim whose own track record, examined in Section 03, turned out to be messier than the one-line version suggests.

:::kv
- {term: "Weights underperform API scores (Jul 27 check)", def: "Would collapse the 'capability inflection' explanation for K3's outsized reaction"}
- {term: "Nvidia Aug 26 guidance cut, or hyperscaler capex trimmed Jul 22-30", def: "Would validate treating K3 as a genuine inflection, not an overreaction"}
- {term: "Chinese labs shift first-party inference to domestic silicon", def: "Breaks the Nvidia-insulation argument in Section 07"}
- {term: "Circular-financing structure visibly unwinds (e.g. an Oracle credit event)", def: "Validates the already-fragile-market bear case independent of Jevons Paradox"}
- {term: "Macro backdrop confound", def: "Fed funds 75bp lower and VIX reaction ~3x calmer than Jan 2025 — some of the smaller shock may just be a calmer market, not a different mechanism"}
- {term: "No Nadella/Huang Jevons restatement", def: "Suggestive, not conclusive — could mean the framing doesn't need repeating, or that its authors learned its track record was messier than advertised"}
:::

None of these six points individually overturns the article's central finding. But together they mark exactly where that finding is provisional rather than settled, and exactly what evidence, arriving over the following weeks, would force a rewrite.

:::references
- {id: 1, title: "How the buzz around Chinese AI model DeepSeek sparked a massive Nasdaq sell-off", url: "https://www.cnbc.com/2025/01/27/how-the-buzz-around-chinese-ai-model-deepseek-sparked-a-massive-nasdaq-sell-off.html", source: CNBC, date: "2025-01-27"}
- {id: 2, title: "Jevons paradox strikes again", url: "https://x.com/satyanadella/status/1883753899255046301", source: "Satya Nadella, X", date: "2025-01-26"}
- {id: 4, title: "DeepSeek might not be as disruptive as claimed", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/deepseek-might-not-be-as-disruptive-as-claimed-firm-reportedly-has-50-000-nvidia-gpus-and-spent-usd1-6-billion-on-buildouts", source: "Tom's Hardware / SemiAnalysis", date: "2025-01-31"}
- {id: 6, title: "Jensen Huang hails DeepSeek, touts extraordinary Blackwell demand", url: "https://fortune.com/2025/02/26/jensen-huang-hails-deepseek-touts-extraordinary-blackwell-demand-nvidia-stock-earnings-call/", source: Fortune, date: "2025-02-26"}
- {id: 7, title: "Nvidia is rebounding after biggest market-cap loss in history, but it's a fragile bounce", url: "https://www.cnbc.com/2025/01/28/nvidia-is-rebounding-after-biggest-market-cap-loss-in-history-but-its-a-fragile-bounce.html", source: CNBC, date: "2025-01-28"}
- {id: 10, title: "Jevons Paradox — definition and explanation", url: "https://www.economicshelp.org/blog/220917/economics/jevons-paradox-definition-and-explanation/", source: "Economics Help"}
- {id: 12, title: "Kimi K3 model page", url: "https://artificialanalysis.ai/models/kimi-k3", source: "Artificial Analysis", date: "2026-07-17"}
- {id: 13, title: "MRVL price history", url: "https://stockanalysis.com/stocks/mrvl/history/", source: "StockAnalysis.com"}
- {id: 14, title: "INTC price history", url: "https://stockanalysis.com/stocks/intc/history/", source: "StockAnalysis.com"}
- {id: 15, title: "AMD price history", url: "https://stockanalysis.com/stocks/amd/history/", source: "StockAnalysis.com"}
- {id: 16, title: "NVDA price history", url: "https://stockanalysis.com/stocks/nvda/history/", source: "StockAnalysis.com"}
- {id: 17, title: "PHLX Semiconductor Index historical data", url: "https://www.investing.com/indices/phlx-semiconductor-historical-data", source: "Investing.com"}
- {id: 18, title: "Chip selloff erases over $1 trillion in value", url: "https://finance.yahoo.com/markets/stocks/articles/chip-selloff-erases-over-1-195406803.html", source: "Yahoo Finance", date: "2026-06-05"}
- {id: 19, title: "Alibaba (BABA) stock forecast: DOJ settlement, cloud, H200", url: "https://www.tradingkey.com/analysis/stocks/us-stocks/262022410-alibaba-baba-stock-forecast-july-2026-doj-settlement-cloud-h200-tradingkey", source: TradingKey, date: "2026-07"}
- {id: 25, title: "S&P downgrades Oracle to BBB-, one notch above junk, citing OpenAI concentration risk", url: "https://mlq.ai/news/sp-downgrades-oracle-to-bbb-one-notch-above-junk-citing-openai-concentration-risk/", source: "MLQ.ai", date: "2026-07-09"}
- {id: 26, title: "Michael Burry's newest short reveals what really worries him about AI", url: "https://www.thestreet.com/investing/michael-burrys-newest-short-reveals-what-really-worries-him-about-ai", source: TheStreet, date: "2026-07-13"}
- {id: 27, title: "The scale of AI circular financing arrangements", url: "https://www.calcalistech.com/ctechnews/article/z4lxiqbtw", source: CalcalisTech, date: "2026-07"}
- {id: 28, title: "Hedge funds dumped chip stocks for a fourth week as AI shares sold off", url: "https://www.investing.com/news/stock-market-news/hedge-funds-dumped-chip-stocks-for-a-fourth-week-as-ai-shares-sold-off-4776190", source: "Investing.com / Reuters", date: "2026-07-06"}
- {id: 30, title: "Chinese AI models are costing US labs like OpenAI and Anthropic market share", url: "https://www.cnbc.com/2026/07/07/chinese-ai-models-costs-us-openai-anthropic.html", source: CNBC, date: "2026-07-07"}
- {id: 31, title: "Chinese AI models drive US adoption surge on OpenRouter", url: "https://www.resultsense.com/news/2026-07-07-chinese-ai-models-us-adoption-surge/", source: ResultSense, date: "2026-07-07"}
- {id: 32, title: "Which GPU clouds support Kimi K2 and the latest open-source LLMs", url: "https://www.gmicloud.ai/en/blog/which-gpu-clouds-support-kimi-k2-and-the-latest-open-source-llms", source: "GMI Cloud", date: "2026"}
- {id: 33, title: "Kimi K2 and when 'DeepSeek moments' happen", url: "https://www.interconnects.ai/p/kimi-k2-and-when-deepseek-moments", source: "Interconnects.ai", date: "2025-07"}
- {id: 34, title: "Nvidia becomes first company to reach $4 trillion market cap", url: "https://www.washingtonpost.com/technology/2025/07/10/nvidia-4-trillion-market-cap/", source: "Washington Post", date: "2025-07-10"}
- {id: 35, title: "Zhipu AI's stock rockets after Chinese firm makes GLM-5.2 open source", url: "https://www.scmp.com/tech/tech-trends/article/3357115/zhipu-ais-stock-rockets-after-chinese-firm-makes-glm-52-open-source", source: "South China Morning Post", date: "2026-06"}
- {id: 36, title: "TSMC Q2 earnings: three CoWoS signals that test AI's spending ceiling", url: "https://www.techtimes.com/articles/320142/20260711/tsmc-q2-earnings-july-16-three-cowos-signals-that-test-ais-spending-ceiling.htm", source: TechTimes, date: "2026-06-04"}
- {id: 37, title: "TSMC Q2 2026 earnings call transcript", url: "https://www.investing.com/news/transcripts/earnings-call-transcript-tsmc-lifts-2026-outlook-as-ai-demand-stays-hot-in-q2-2026-93CH-4794777", source: "Investing.com", date: "2026-07-16"}
- {id: 38, title: "Big Tech Q2 2026 earnings — the AI capex question", url: "https://www.ig.com/uk/trading-strategies/big-tech-q2-2026-earnings---the-ai-capex-question-and-what-uk-in-260716", source: "IG.com", date: "2026-07-16"}
- {id: 39, title: "H100 rental price cloud comparison", url: "https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison", source: "IntuitionLabs", date: "2026"}
- {id: 41, title: "Jensen Huang, ServiceNow Knowledge 2026, on agentic AI compute", url: "https://fortune.com/2026/05/06/jensen-huang-servicenow-bill-mcdermott-agentic-ai-robos/", source: Fortune, date: "2026-05-06"}
- {id: 42, title: "Agentic AI token usage guide", url: "https://iternal.ai/token-usage-guide", source: "Iternal.ai / Gartner", date: "2026-03"}
- {id: 43, title: "State of AI", url: "https://openrouter.ai/state-of-ai", source: OpenRouter, date: "2026"}
- {id: 44, title: "Anthropic CEO Dario Amodei says company grew 80-fold in first quarter", url: "https://www.cnbc.com/2026/05/06/anthropic-ceo-dario-amodei-says-company-crew-80-fold-in-first-quarter.html", source: CNBC, date: "2026-05-06"}
- {id: 45, title: "Nvidia fiscal Q2 earnings date", url: "https://calendarial.com/nvidia-fiscal-q2-earnings/", source: Calendarial, date: "2026-07"}
- {id: 46, title: "FOMC statement, June 17, 2026", url: "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260617a.htm", source: "Federal Reserve", date: "2026-06-17"}
- {id: 47, title: "Stock market news for Jan 26, 2025 (VIX)", url: "https://www.cnbc.com/2025/01/26/stock-market-news-for-jan-26-2025.html", source: CNBC, date: "2025-01-26"}
- {id: 48, title: "Moonshot's Kimi K3 sparks AI semiconductor stocks selloff", url: "https://cryptobriefing.com/moonshot-kimi-k3-ai-semiconductor-stocks-selloff/", source: CryptoBriefing, date: "2026-07-17"}
- {id: 49, title: "An interview with Nvidia CEO Jensen Huang about accelerated computing", url: "https://stratechery.com/2026/an-interview-with-nvidia-ceo-jensen-huang-about-accelerated-computing/", source: Stratechery, date: "2026-03-17"}
- {id: 55, title: "The Jevons Paradox and AI tech stocks: a historical analysis", url: "https://www.investing.com/analysis/the-jevons-paradox-and-ai-tech-stocks--a-historical-analysis-200656932", source: "Investing.com", date: "2025-02-08"}
- {id: 56, title: "Nvidia stock notches fresh record high in remarkable 2025 turnaround", url: "https://finance.yahoo.com/news/nvidia-stock-notches-fresh-record-high-in-remarkable-2025-turnaround-200401502.html", source: "Yahoo Finance", date: "2025-06-25"}
:::
