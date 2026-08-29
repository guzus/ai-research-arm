---
eyebrow: REPORT · COMPANY
title: "Moonshot AI: the lab that traded its consumer app for the open-weights frontier"
deck: From a Pink Floyd-named startup to a $31.5 billion ask in forty months — the funding, the pivot, the governance fight, and the unaudited numbers underneath.
lede: |
  Moonshot AI is the Beijing lab behind Kimi — and, as of July 16, 2026, behind Kimi K3, the largest open-weight model ever announced. In three years it has been China's most aggressive consumer-AI advertiser, the loser of the most consequential same-day launch collision in AI history, and the author of the sharpest strategy reversal of the DeepSeek era. Today its consumer app has lost more than half its Chinese users, its revenue is unaudited and investor-narrated, a confidential Hong Kong arbitration still contests how the company was born — and investors are being asked to price it at $31.5 billion. This is the company profile: how Moonshot got here, what the business actually is, and what would have to be true for the number to make sense.
stats:
  - {label: Founded, value: "Mar 2023", note: Beijing}
  - {label: Valuation ask, value: $31.5B, note: "pre-money, unclosed (Jul 2026)"}
  - {label: Reported ARR, value: "$200-300M", note: "unaudited (Apr-Jun 2026)"}
  - {label: Headcount, value: ~300, note: "Jun 2026"}
domain: general
---

:::callout(kind=info, label="Direct answer")
- Moonshot AI (月之暗面, "Dark Side of the Moon") was founded in March 2023 by Yang Zhilin — first author of XLNet and co-author of Transformer-XL — with Zhou Xinyu, Wu Yuxin, and Zhang Yutao; Alibaba became its dominant outside shareholder in 2024 with ~36% for ~$800M [^1] [^2] [^5].
- Its arc has three acts: a bought consumer boom (36M+ claimed MAU, >¥700M of 2024 ads), the January 20, 2025 DeepSeek R1 collision that broke the model, and the July 2025 open-sourcing of Kimi K2 that rebuilt the company around Western developer adoption [^20] [^23] [^26].
- The business today: open-weight flagships (K2 family, now K3), an API repriced 5-6x upward in a year, $19-199/month subscriptions, and partner-led enterprise — on reported ARR of $200-300M that no auditor has verified [^9] [^46] [^44].
- Valuation went $2.5B (Feb 2024) → $4.3B (Dec 2025) → $20B (May 2026) → a $31.5B pre-money ask opened June 30, 2026 — roughly 7x of the rise in the final six months, priced against Hong Kong comps that were crashing the week K3 launched [^9] [^10] [^11] [^40].
- Unresolved overhangs: a confidential HKIAC arbitration over the company's founding, an Anthropic distillation allegation Moonshot has never answered, and a US congressional probe naming its models [^12] [^32] [^33].
:::

## 01. The strangest company profile in AI: shrinking app, exploding valuation

In three years Moonshot AI has traveled from consumer-chatbot darling to open-weights frontier lab — and in July 2026 it is doing three things at once that almost never coexist: launching the largest open-weight model ever announced, raising at a $31.5 billion pre-money valuation, and watching its flagship consumer app fade toward irrelevance. The company's value now rests on developers, not users.

:::stats
- {label: Valuation ask, value: $31.5B, note: "pre-money; round opened ~Jun 30, unclosed as of Jul 17, 2026"}
- {label: ARR, value: "$200-300M", note: "unaudited, investor-sourced; Apr-Jun 2026 range"}
- {label: Headcount, value: ~300, note: "per enterprise chief Huang Zhenxin, Jun 2026"}
- {label: Kimi app China MAU, value: "-58%", note: "21.7M → 9.0M, Q1→Q4 2025 (QuestMobile)"}
:::

Start with the launch. On July 16, 2026, Moonshot shipped Kimi K3 — 2.8 trillion parameters, a 1-million-token context window, weights promised by July 27, and a new Kimi Enterprise tier — priced at $0.30 per million tokens on cache hits, $3.00 on misses, and $15.00 for output, deliberately parked at Anthropic's mid-tier rather than undercutting it [^44]. The predecessor line had already proven the strategy: Kimi-K2-Instruct was still pulling 228,819 rolling-month Hugging Face downloads a full year after release as of July 17, 2026, and K2.6 sat at #2 among the most-used models on OpenRouter before K3 arrived [^49] [^64].

The money is chasing that developer traction at extraordinary speed. A round opened around June 30, 2026 at $31.5 billion pre-money — still unclosed as of July 17 — is Moonshot's third raise in six months [^11], following Bloomberg's June 8 report of talks targeting $30 billion [^10] and a May round of roughly $2 billion at $20 billion post-money led by Meituan's Long-Z, bringing about $3.9 billion raised in half a year [^9]. Revenue is climbing too, though the numbers deserve a squint: ARR reportedly went from roughly $100 million in early March 2026 to $200 million-plus in April [^9] to over $300 million by mid-June, with one Nomura call citing $400-500 million [^46] — all unaudited and investor-sourced. A company of "300-odd" people, per enterprise chief Huang Zhenxin in June 2026, is generating those figures with resources still prioritized toward model R&D [^48].

Meanwhile the product that made Kimi a household name in China is evaporating. QuestMobile counted the Kimi app's China MAU at 21.65 million in Q1 2025 and 9.03 million by Q4 2025 — a 58.3% collapse — and by May 2026 the top consumer tier read Doubao 382 million, Qwen 167 million, DeepSeek 130 million, with Kimi absent entirely [^21] [^22]. When co-founder Zhou Xinyu was asked on X whether the K3 weights drop would be another "DeepSeek moment," he replied simply "Will do"; a pseudonymous OpenAI researcher answered the launch with "the era of the chinese labs being far behind is over" [^69].

What would weaken this framing: the ARR trajectory is entirely investor-relayed, the $31.5 billion round has not closed, and listed peers cratered the day after K3 launched — Zhipu fell 28.49% and MiniMax 15.6% on July 17 amid a global tech selloff and post-lockup supply [^54] [^40] — a reminder that Chinese AI valuations can reprice violently.

Why it matters: Moonshot is the cleanest live test of whether an open-weights lab can be worth more as its consumer footprint shrinks — the question every section below interrogates.

## 02. A founder built for exactly this: Transformer pedigree, Pink Floyd name

Moonshot's founding advantage was unusually direct founder-market fit — Yang Zhilin is one of the few founders anywhere whose name is on the pretraining-era papers his company now competes with — wrapped in a deliberately romantic identity.

:::kv
- {term: Founded, def: "March 2023 (registered April 17, 2023)"}
- {term: HQ, def: Beijing}
- {term: Founders, def: "Yang Zhilin, Zhou Xinyu, Wu Yuxin, Zhang Yutao"}
- {term: Name, def: "After Pink Floyd's \"The Dark Side of the Moon\""}
- {term: Seed backers, def: "HongShan (Sequoia China), ZhenFund"}
- {term: First product, def: "Kimi (Oct 2023)"}
:::

Yang's résumé reads like a checklist for building a frontier lab. Born in 1992 in Shantou, he graduated from Tsinghua's computer science program in 2015 under Tang Jie, then finished a CMU PhD in four years — 2019 — advised by Ruslan Salakhutdinov, with stints at Google Brain and Meta AI along the way [^1]. The papers are the point: he is first author of XLNet (arXiv 1906.08237, June 2019), with Salakhutdinov and Quoc V. Le among the co-authors [^2], and second author — flagged as equal contribution — of Transformer-XL (arXiv 1901.02860, with Zihang Dai listed first) [^3]. Both papers attack the same problem Moonshot later monetized: getting Transformers to reason over longer context. Few founders can claim their startup's technical thesis is a continuation of their own citation record.

The press mythology needs one correction, though. The shorthand that Yang was "first author of both" landmark papers is half wrong — the arXiv author order is the primary record, and on Transformer-XL he sits second [^3]. It is a small distortion, but a telling one: Moonshot's founder-genius narrative has been polished in the retelling, and careful readers should treat the arXiv listings, not the profiles, as ground truth.

Nor was Moonshot his first company. In 2016, mid-PhD, Yang co-founded Recurrent AI (循环智能), a conversation-intelligence NLP business selling to banks and insurers, backed by ZhenFund, Sequoia China, and Boyu [^72] — a venture whose spin-out arrangements would later resurface as the investor dispute examined in section 07. What changed everything was ChatGPT: in Yang's telling, its launch was the epiphany that a from-zero AGI company was finally possible, because capital and talent had aligned [^4]. Moonshot was founded in March 2023 — company lore times it to the 50th-anniversary year of Pink Floyd's *The Dark Side of the Moon*, Yang's favorite album, released March 1973 — with the legal entity registered on April 17, 2023 [^1]. His stated horizon matched the name: "AI is not about finding PMF in the next year or two, but how to change the world over the next ten to twenty years… we are resolute long-termists" [^4].

:::quote(attr="Yang Zhilin, Moonshot AI founder, March 2024 interview (translated)")
Lossless-compression long context is "the new computer memory" — the first step of our internal "moon landing" plan toward AGI.
:::

He did not build alone. Co-founders Zhou Xinyu (周昕宇) and Wu Yuxin (吴育昕) joined at inception, and Chinese registry-based reporting also names Zhang Yutao (张宇韬) as co-founder and CTO, with an initial equity split of roughly Yang 78.968%, Zhou 10%, Wu 5.957%, and Zhang 5% [^71] — figures derived from secondary Chinese-registry reporting, so treat the decimals as indicative rather than audited. HongShan (Sequoia China) and ZhenFund seeded the company at a valuation around $300 million, though even the raise size is contested — $60 million per SCMP versus roughly $200 million per PitchBook and TechCrunch [^1]; the round-by-round ledger in section 03 takes up that conflict.

Why it matters: founder-market fit this literal — the long-context papers, the prior NLP company, the AGI framing — is what let an eleven-month-old startup command billion-dollar valuations before revenue, and it is the asset every later chapter of this story either compounds or spends.

## 03. The funding ledger: sixteen flat months, then 7x in six

Moonshot's capitalization history is really two stories stapled together: a 2024 mega-round that made Alibaba its dominant shareholder, then sixteen months of nearly flat marks — followed by a violent 2026 re-rating in which almost all of today's headline valuation was created in six months on the strength of the open-weights narrative.

The ledger opens modestly. The 2023 seed from HongShan and ZhenFund priced the company around {accent}$300 million{/} — with the raise itself already showing the disclosure fog that recurs throughout this story: SCMP put it at $60 million, while PitchBook data cited by TechCrunch put it near $200 million [^1]. Then came the round that defined the cap table: in February 2024, an Alibaba-led round of roughly $1 billion at a reported ==$2.5 billion post-money== — at the time the largest single round ever raised by a Chinese LLM startup, with Monolith, Meituan, and Xiaohongshu reported as participants [^1].

The primary-source record complicates the press number in two instructive ways. Alibaba's own FY2024 20-F filed with the SEC discloses an investment of approximately {accent}US$0.8 billion (RMB 5.9 billion) for roughly 36% of Moonshot's equity{/} via preferred stock — arithmetic that implies about $2.2 billion, slightly below the reported $2.5 billion headline [^5]. And per Financial Times reporting, roughly half of that $800 million was paid not in cash but in {tag}Alibaba Cloud computing credits{/} [^6] — a structure that made Alibaba simultaneously Moonshot's largest shareholder and its compute vendor. That FT claim is single-sourced and neither company has confirmed the split, but if accurate it means the round's true cash component, and hence the effective price paid per point of equity, is softer than the headline suggests.

:::callout(kind=warn, label="Disclosure quality")
Almost none of the post-2024 marks are company-confirmed. The $20 billion round's terms surfaced via a since-deleted WeChat post from deal adviser Huafeng Capital, and Moonshot has never confirmed either 2026 headline valuation [^74]. The June 30, 2026 figure of $31.5 billion is a pre-money *ask* on a newly opened round — sourced to Tencent News, adjacent to Bloomberg's June 8 report of "$30 billion" talks — and remains unclosed as of July 17, 2026 [^10] [^11].
:::

:::timeline
- {date: 2024-02, headline: "Alibaba leads ~$1B at $2.5B post", body: "Then the largest single round for a Chinese LLM startup; Alibaba takes ~36% via preferred stock."}
- {date: 2024-08, headline: "Tencent + Gaorong, $300M+ at $3.3B", body: "The last mark before sixteen months of stagnation."}
- {date: 2025-12, headline: "IDG-led $500M Series C at $4.3B post", body: "Oversubscribed by Alibaba/Tencent; Wang Huiwen participates; internal letter cites >RMB 10B cash."}
- {date: 2026-02, headline: "$700M+ first tranche targeting $10B", body: "Alibaba, Tencent, and 5Y Capital commit; the re-rating begins."}
- {date: 2026-05, headline: "Meituan Long-Z leads ~$2B at $20B post", body: "With Tsinghua Capital, China Mobile, CPE Yuanfeng; $3.9B raised in six months per the deal adviser."}
- {date: 2026-06, headline: "New round OPENED at $31.5B pre-money", body: "An ask, not a closed print; unclosed as of Jul 17, 2026."}
:::

:::line-chart(title="Moonshot AI reported valuation, Feb 2024 - Jun 2026", subtitle="Press-reported round marks, $B; Jun 2026 is an unclosed pre-money ask", y-unit=$)
x: 2024-02,2024-08,2025-12,2026-02,2026-05,2026-06
Valuation: 2.5,3.3,4.3,10,20,31.5
:::

The shape of that chart is the argument. From August 2024's Tencent-and-Gaorong round at $3.3 billion [^7] to December 2025's IDG-led $500 million Series C at $4.3 billion post [^8], the mark moved barely 30% in roughly sixteen months — a stretch that even included a reported ~$600 million negotiation at just $3.8 billion pre in October 2025 [^73]. Then the line goes vertical: a $700 million-plus first tranche targeting $10 billion in February 2026 [^73], a ~$2 billion Meituan Long-Z-led round at $20 billion in May [^9], and a round opened at $31.5 billion pre by June 30 [^10]. Roughly {accent}7x of the total valuation rise landed in the final six months{/}, on approximately $3.9 billion raised in that window per Huafeng Capital [^9] — coinciding with, and priced on, the K2-era open-source story rather than any disclosed revenue inflection.

One more asterisk belongs on the record: in April 2024, Jiemian reported a founder-linked ~$40 million secondary cash-out inside the February round; Moonshot denied it, attributing the share movement to an employee incentive plan [^75]. The claim is rumor-tier and denied — but its existence, alongside adviser-leaked terms and never-confirmed marks, illustrates how thin the verification layer under this cap table is.

Why it matters: the ledger says Moonshot's worth is overwhelmingly a 2026 narrative bet, not a compounding record — the counterpoint being that sixteen flat months prove these same investors *can* withhold re-rating until evidence arrives, which makes the six-month, seven-fold repricing either a genuine information event or the thing section 09 must stress-test.

## 04. The consumer era: renting users at 199 million yuan a month

Kimi's 2023-24 ascent was real but rented: a genuine long-context product wedge, amplified by the most aggressive advertising budget in Chinese consumer AI, produced a user base that evaporated almost exactly as fast as the spend that acquired it.

The wedge came first. Kimi Chat launched on October 9, 2023, billed as the first AI product supporting 200,000 Chinese characters — roughly 128K tokens — of input, at a moment when most chatbots handled a fraction of that [^18]. On March 18, 2024, Moonshot opened an invited beta for {accent}2,000,000-character lossless context{/} — a 10x jump that turned a spec-sheet advantage into a viral event. Growth was explosive enough to knock Kimi offline for roughly two days starting March 21 as servers buckled, and the app cleared 500,000 downloads by March 19 [^19]. Through 2024 the product kept shipping consumer-facing surface: Kimi Explore Edition, an autonomous-search mode, arrived October 11, 2024, and the company's first reasoning model, k0-math, landed November 16, 2024 — Kimi's first anniversary — with a self-reported claim of o1-mini parity on Chinese math exams [^76].

Then came the amplifier. In October 2024 alone, Moonshot spent {accent}199 million RMB (~US$27M){/} on advertising — 16th among *all* Chinese apps by ad spend that month, per AppGrowing, ranking an AI chatbot alongside games and e-commerce giants. Full-year 2024 spend exceeded 700M RMB, with 530M RMB concentrated in Q4 alone [^20] [^21]. The spend bought what it was supposed to buy: Yang Zhilin said Kimi passed ==36 million MAU== in October 2024 — though that is a company figure, and third-party trackers put end-2024 at "over 20M," a gap worth holding onto [^20]. Unit economics deteriorated as the price war escalated: unnamed-investor estimates put customer acquisition at ~10 RMB per download in March 2024 (12-13 RMB including inference), with hedged estimates that it "may have soared… to over RMB 50" per user at the peak [^77].

:::stats
- {label: Peak MAU (company), value: 36M+, note: "Oct 2024, Yang Zhilin"}
- {label: Q1 2025 MAU, value: 21.7M, note: QuestMobile}
- {label: Q4 2025 MAU, value: 9.0M, note: QuestMobile}
- {label: 2024 ad spend, value: ">¥700M", note: "¥530M in Q4 alone"}
:::

What the spend rented, its withdrawal repossessed. When the advertising stopped (section 05 owns the February 2025 decision), the app's audience followed it down with remarkable fidelity: QuestMobile's China app panel shows 21.653M MAU in Q1 2025 falling to 9.027M by Q4 2025 — a 58.3% decline — while quarterly ad spend collapsed from ~150M RMB in Q1 2025 to under 100,000 RMB by Q4 2025 [^21].

:::slope(left-label="Q4 2024", right-label="Q4 2025", unit=¥M)
| Item | Q4 2024 | Q4 2025 |
|------|---------|---------|
| Ad spend (¥M) | 530 | 0.1 |
| App MAU (M) | 20 | 9.0 |
:::

:::note
Slope endpoints mix scales for shape, not precision: the Q4 2025 ad-spend figure is "under ¥0.1M" (below 100,000 RMB), and MAU is plotted in millions of users, not ¥M. Q4 2024 MAU uses the third-party "over 20M" estimate rather than the company's 36M claim.
:::

By May 2026, China's consumer-AI top tier read Doubao 382M, Qwen 167M, DeepSeek 130M MAU — with Kimi absent from it entirely (as of May 2026) [^22].

:::note(label="Methodology")
Tracker panels disagree materially. AICPB's June 2026 ranking shows Kimi at 22.69M MAU (#8 in China) — roughly 2.3x QuestMobile's figure for the same app in the same period. The panels measure different footprints (QuestMobile: China Android app panel; AICPB: broader web + app), so the two series are non-comparable; use each internally, never across [^78].
:::

Two fairness notes. First, buying growth was arguably rational at the time: in late 2024 the consensus playbook held that consumer scale was the moat, capital was abundant, and 10 RMB per download was cheap relative to lifetime value if even a sliver converted — the bet failed on retention, not on arithmetic. Second, the collapse is specifically a *China-app* phenomenon: kimi.com web traffic and overseas developer adoption moved in the opposite direction after K2.5, a story that belongs to section 06.

Why it matters: the consumer era is the cleanest natural experiment in Chinese AI on whether ad-bought chatbot users stick without the ads. Kimi's answer — a 58% MAU decline within four quarters of the spigot closing [^21] — is the empirical foundation for everything Moonshot did next, because it proved the company was renting distribution, not compounding it.

## 05. January 20, 2025: the day that rewrote the strategy

No single day in Moonshot's history did more damage — or more good — than January 20, 2025, when DeepSeek R1 landed on the same date as Kimi k1.5 and invalidated, within weeks, both the company's paid-growth model and its founder's stated philosophy on open source.

The collision itself was almost perfectly controlled as an experiment. Both labs shipped frontier reasoning models the same day. DeepSeek released R1 as MIT-licensed open weights, complete with a family of distilled smaller models anyone could run [^24]. Moonshot released k1.5 as a technical report — arXiv 2501.12599, posted January 22 — with no weights at all [^23]. On the benchmarks the gap was modest: R1 scored 79.8 on AIME to k1.5's 77.5, and 97.4 to 96.2 on MATH-500 [^23]. What decided the narrative was not raw capability but distribution. R1 was free, forkable, and everywhere within days; k1.5 was a PDF. It is a counterpoint worth holding onto, because the coverage rarely did: k1.5 was multimodal where R1 was not, and the scoreline was close enough that a world in which Moonshot had shipped weights that day looks very different [^23]. The loss was strategic, not technical.

The reversal this forced was personal as well as corporate. Eleven months earlier, Yang Zhilin had told Tencent News exactly why a leader would never open-source its best model:

:::quote(attr="Yang Zhilin, February 2024 — seventeen months before Moonshot open-sourced K2 (translated)")
It's usually the laggards who might do that — or they might open-source a small model just to stir things up.
:::

He never verbally recanted that position; the reversal was enacted rather than stated [^25]. The enactment began within a month. On February 18, 2025, Jiemian reported that Moonshot had slashed its advertising and user-acquisition budgets — suspending its Android distribution channel and third-party ad-platform placements — making it the first of the "six tigers" to cut [^58]. TMTPost the next day described a halt to "money-burning" campaigns amid the DeepSeek craze [^20]. Through the first half of 2025 the internal reset went deeper: derivative and sideline products were stopped (the overseas apps Ohai and Noisee had already been shut in September 2024, their product leads leaving to found startups [^59]), "user growth" was removed from quarterly OKRs, K1-series updates were halted, and resources were concentrated on K2, coding and agent scenarios, and overseas API monetization [^58]. At the start-of-2025 reflection meeting, by one 36kr-relayed researcher account, Yang's moves were "even more radical" than what staff had proposed — killing K1 outright to bet everything on K2 [^79].

:::timeline
- {date: 2025-01-20, headline: "R1 / k1.5 collision", body: "DeepSeek R1 ships MIT-licensed open weights + distilled models; Kimi k1.5 ships as a technical report with no weights. AIME gap: 79.8 vs 77.5."}
- {date: 2025-02-18, headline: "Ad budgets slashed", body: "Jiemian: Moonshot suspends its Android channel and third-party ad placements — first of the six tigers to cut."}
- {date: 2025-06, headline: "The internal reset", body: "K1-series updates halted; user growth removed from quarterly OKRs; sideline products stopped; everything concentrated on K2 and agent/coding scenarios."}
- {date: 2025-07-11, headline: "Kimi K2 open weights", body: "Modified MIT license, 1T total / 32B active MoE, 15.5T tokens, MuonClip — China's first open trillion-parameter model."}
- {date: 2025-11-06, headline: "K2 Thinking + first AMA", body: "Reasoning release, then the three co-founders' first joint Reddit/Zhihu AMA on Nov 11."}
:::

There were sober reads and premature obituaries alike. TMTPost's framing allowed that the ad halt was partly opportunistic — a pivot toward organic growth that the DeepSeek moment made respectable, not a pure capitulation [^20]. MIT Technology Review went further the other way, briefly placing Moonshot in February 2025 among labs "giving up on foundational training" [^80] — a call falsified five months later, on July 11, 2025, when Kimi K2 shipped as open weights under a Modified MIT license: a 1-trillion-parameter, 32B-active MoE trained on 15.5T tokens with the MuonClip optimizer and "zero training instability," China's first open trillion-parameter model and the fastest-trending model on Hugging Face within a day [^26,27]. The only first-person public rationale came not from Yang but from engineer Justin Wong on Zhihu: "Our only regret was that we were not the one to open up that route," and — the operational lesson — "open source means performance comes first. You can no longer rely on superficial tricks." [^25]

By end-2025 the pivot had sorted the field: of the six AI tigers, only Moonshot, MiniMax, and Zhipu/Z.ai still ran frontier pre-training; 01.AI and Baichuan had abandoned it [^81]. And at the November 11 AMA that followed K2 Thinking's release, Yang disowned CNBC's $4.6M training-cost figure ("This is not an official figure") and, asked whether Moonshot would ever go closed-source again, answered: "If the model becomes more and more dangerous :)" [^82,28,29]. That is the measure of the day: January 20 did not beat Moonshot on benchmarks — it beat Moonshot's business model, and the company chose to keep the lab and discard the model. Everything in the sections that follow, from K2's adoption economics to the governance questions it raises, flows from that choice.

## 06. The open-weights business: adoption is real, capture is partial

K2 bought Moonshot the one thing its $1B+ war chest never could — default placement in the Western developer stack — but the open-weights business model converts only a sliver of that usage into revenue, and the revenue that does exist rests entirely on company and investor claims no auditor has touched.

Start with the adoption, because it is the genuinely unambiguous part. At launch in July 2025, K2 became the fastest-downloaded model in Hugging Face history, going from 76,000 downloads on Friday to 145,000 by Monday over its first weekend [^50]. A year on, the original Kimi-K2-Instruct checkpoint still shows 228,819 downloads in the rolling month as of 2026-07-17 — a counter that excludes the GGUF mirrors most local users actually pull [^49]. The quality signal arrived just as fast: when K2 Thinking shipped in November 2025 it scored 67 on Artificial Analysis's Intelligence Index, the highest any open-weights model had ever posted and second only to GPT-5 across all models [^30].

:::rank-list
- {label: Kimi K2 Thinking, value: 67, pct: 100, highlight: true}
- {label: gpt-oss-120b, value: 61, pct: 91}
- {label: MiniMax M2, value: 61, pct: 91}
- {label: DeepSeek V3.2-Exp, value: 57, pct: 85}
:::

:::note
Artificial Analysis Intelligence Index snapshot at K2 Thinking's release, November 2025. The index has since been recalibrated (v4.1 as of June 2026); later scores are not comparable to these [^30] [^83].
:::

That November snapshot is a peak, not a plateau. Open-weights leadership has rotated relentlessly since: GLM-5 took the crown in February 2026, Kimi K2.6 retook #1 in April — pushing 1.88 trillion tokens through OpenRouter in its first week — and GLM-5.2 leads the recalibrated v4.1 index as of June 2026 [^83]. Nathan Lambert's November 2025 read captures both the achievement and its shelf life: K2 Thinking was the closest open weights had ever come to the closed frontier, with a gap of "4-6+ months if you put a gun to my head" [^84]. The a16z-OpenRouter study of 100 trillion tokens named K2 among the open models that drove open-source share to roughly a third of OpenRouter traffic by late 2025, with Chinese models exceeding 45% of all OpenRouter tokens by April 2026 [^52]. Perplexity's CEO said one day after launch that his company might post-train on K2 [^53].

Now the uncomfortable half of the thesis: almost none of that usage pays Moonshot. K2's Modified MIT license asks exactly one thing of heavy commercial users — products over 100M monthly active users or $20M in monthly revenue must "prominently display 'Kimi K2' on the user interface." Attribution, zero royalties, "prominently" undefined, and outputs (plus models trained on outputs) exempt entirely [^27]. A third party serving the weights owes Moonshot nothing by default — and third parties serve them *better*: at launch Groq pushed K2 at over 400 output tokens per second while Moonshot's own API managed roughly 10, a ~40x gap, with Baseten, Together, Fireworks, and DeepInfra all standing up endpoints; Moonshot's leverage over that ecosystem is a quality-policing repo, K2-Vendor-Verifier, not a revenue share [^51].

:::compare
- {role: LOWEST, name: "Moonshot first-party API", value: "~10 tok/s"}
- {role: HIGHEST, name: "Groq", value: ">400 tok/s"}
- {role: SUBJECT, name: "Moonshot first-party API", value: "~10 tok/s"}
:::

The lab gives the weights away and others serve them faster — that is the capture problem in one card. The Cursor episode shows what monetization actually looks like when it works. Cursor's Composer 2, launched in March 2026, was revealed via a leaked model ID to be built on Kimi K2.5; Cursor said about a quarter of the final model's compute came from the base, and Moonshot confirmed an authorized commercial partnership — routed through Fireworks AI [^31]. Moonshot monetizes hosting and partnership deals, not license royalties.

Where Moonshot does charge, it is charging more. Flagship API pricing climbed from $0.60/$2.50 per million tokens (K2, K2 Thinking) to $0.60/$3.00 (K2.5), $0.95/$4.00 (K2.6), and $3.00/$15.00 for K3 — a 5-6x increase in a year that commentators called "the end of super-cheap Chinese AI," softened by a $0.30 cache-hit rate Moonshot claims covers >90% of coding-workload tokens via its Mooncake stack [^85] [^44]. International subscriptions run $19 to $199 monthly across four tiers bundling Kimi Code credits, against ~¥49/¥99 in China [^86]. Enterprise is deliberately partner-led — no in-house services arm ("We can barely keep up with model research," per enterprise chief Huang Zhenxin), distribution via Alibaba Cloud and AWS Bedrock, and a named downstream roster mixing direct and third-party-hosted users: Cursor, Notion, Coinbase, Coursera, Perplexity [^48] [^87].

:::slope(left-label="Mar 2026", right-label="Jun 2026", unit=$M)
| Item | Mar 2026 | Jun 2026 |
|------|----------|----------|
| Reported ARR | 100 | 300 |
:::

:::note
All revenue figures are company- or investor-sourced and unaudited; no independently verified financials exist.
:::

The counterpoint is that this revenue curve — ~$100M ARR in March 2026, $200M+ in April per deal adviser Huafeng Capital, over $300M by mid-June [^9] [^46] — is unverifiable and mechanically flattered by a near-zero base: monetization only began in October 2025, which is why K2.5's first 20 days of revenue could exceed all of 2025, and why claims like overseas API revenue up 4x since November and paying users growing 170% month-over-month say more about the starting point than the destination [^45].

Why it matters: Moonshot has proven that open weights buy distribution money can't, but the resulting business — hosting deals, subscriptions, and a fast-repricing API — captures a fraction of the usage it created, and until the numbers are audited, the gap between adoption and revenue is the single most important unknown in the company's story.

## 07. The governance fault line: an unresolved arbitration under a $31.5B ask

The least-priced risk in Moonshot's story is not compute or competition but governance: a confidential Hong Kong arbitration over how the company was born, entangled with the equity of the executive now running its commercialization, still unresolved twenty months on as the company courts public markets.

On November 11, 2024, five of Recurrent AI's seven investors — GSR Ventures, Jingya Capital, Boyu Capital, Huashan Capital, and Wanwu Capital — filed for arbitration at the Hong Kong International Arbitration Centre against Yang Zhilin and co-founder/CTO Zhang Yutao, alleging the pair founded Moonshot and raised outside money before obtaining consent waivers from Recurrent AI's shareholders — five of seven, meaning the remaining holders stayed out of the case [^12]. Moonshot's counsel, MinterEllison's David Morrison, answered the same day that the claim "lacks both legal grounds and factual basis" and promised a counterclaim [^88].

The dispute turned public — and personal — in early December. In WeChat posts on December 5-6, GSR's Zhu Xiaohu argued that Moonshot had been incubated inside Recurrent AI for roughly two years, that the board resolution blessing the spin-off was not signed until January 2024 (about six months *after* the split), and that the resolution is arguably void because then-GSR partner Zhang Yutong — a different person from co-respondent Zhang Yutao — concealed a conflict of interest: {accent}9,000,000 free founding shares{/} of Moonshot, roughly ==14% of initial equity==, versus the 9.5% Recurrent AI itself received. GSR fired her over it; Zhu valued her stake at ~US$100 million and said Yang later transferred her 3 million more shares [^15].

:::quote(attr="Zhu Xiaohu, GSR Ventures, December 2024 (translated)")
I am willing to waive our claims against Yang Zhilin, Zhang Yutao, and Moonshot itself — I simply do not understand why Kimi's future must be bound to Zhang Yutong.
:::

Yang's first-person rebuttal, posted December 6, is the strongest counter on the record: he says he decided to start Moonshot in late 2022, reached a written agreement with Recurrent AI's CEO in February 2023, and that every Recurrent director — team and investor-appointed — signed the spin-off resolution; Zhang Yutong's shares, he says, are co-founder compensation subject to multi-year vesting, not a concealed kickback [^14]. The claimants' economic complaint also has a structural wrinkle: Recurrent AI took its 9.5% of Moonshot as spin-off consideration, so the five funds participate only indirectly and diluted — none ever invested in Moonshot directly. Anonymous-sourced reporting says settlement talks broke down over the gap between roughly ==20% demanded and ~10% offered==, and over Zhu's condition that Moonshot cut ties with Zhang Yutong [^89].

:::timeline
- {date: 2024-11-11, headline: "Five investors file at HKIAC", body: "GSR, Jingya, Boyu, Huashan, and Wanwu initiate arbitration against Yang Zhilin and Zhang Yutao over the un-waived spin-out."}
- {date: 2024-12-05, headline: "Zhu Xiaohu goes public", body: "WeChat posts allege a void spin-off resolution and Zhang Yutong's concealed 9M-share stake."}
- {date: 2024-12-06, headline: "Yang's rebuttal", body: "Every Recurrent director signed the resolution; Zhang Yutong's shares are vesting co-founder compensation."}
- {date: 2025-02, headline: "Tribunal constituted", body: "Fees paid; the HKIAC panel takes shape."}
- {date: 2025-05-28, headline: "Zhu: still in arbitration", body: "Zhu Xiaohu says the dispute remains in arbitration, now handled by the lawyers."}
- {date: 2025-12-08, headline: "Zhang Yutong confirmed president", body: "Moonshot puts her in charge of overall strategy and commercialization — the separation concession never happens."}
:::

The company's answer to Zhu's separation offer was enacted, not argued: on December 8, 2025, Zhang Yutong was confirmed as Moonshot/Kimi president, responsible for overall strategy and commercialization [^16]. And the market's answer, so far, has been indifference — the December 2025 $500M Series C, the 2026 rounds that carried the valuation to $20B, and the $31.5B ask itself all closed or opened while the arbitration was live [^8] [^9]. Fees were paid and the tribunal constituted around February 2025 [^13]; as late as May 28, 2025, Zhu said the dispute was "仍在仲裁当中" — still in arbitration, in the lawyers' hands [^17].

:::callout(kind=warn, label="Confidentiality caveat")
HKIAC proceedings are confidential. As of July 2026 there is no public award, ruling, or settlement — but absence of news is not absence of outcome. A quiet settlement cannot be ruled out; "still pending" is an inference from silence, not a confirmed status [^17].
:::

Why it matters: an unresolved founder-equity arbitration is a mandatory disclosure item for any Hong Kong listing, which turns a private-market shrug into a prospectus-page risk factor precisely when Moonshot needs public investors to underwrite a $31.5B story (mechanics in section 09). The fundraising record says investors have priced the arbitration at zero; the record also says nobody yet knows what the tribunal will decide about how this company came to exist.

## 08. Compute-poor by design, and the Washington problem

Scarcity is not incidental to Moonshot — it is the lab's technical identity, an operation engineered around efficiency tricks because it could never out-buy its rivals, and the same open-weights strategy that built its US developer franchise has now made it a named subject of US political scrutiny.

Start with what Moonshot admits. The K2 technical report discloses the silicon — NVIDIA H800 nodes, 8 GPUs per node with NVLink/NVSwitch inside the box and 8x400Gbps RoCE between boxes — but deliberately withholds the total GPU count, and describes training "under dynamic resource availability," a phrase analysts read as time-shared or rented capacity rather than a dedicated owned cluster [^26]. In a November 2025 AMA the co-founders were blunter: the lab is "outnumbered" in high-end GPUs versus US rivals, running on H800s — a chip banned for export to China since late 2023 — over Infiniband [^36]. The scale gap is quantifiable even against domestic peers: SemiAnalysis pegs DeepSeek's fleet at roughly 50,000 Hopper GPUs and more than $500M of GPU spend, while circulated compute math from Emad Mostaque puts base K2 at ~2.8M H800-hours — almost exactly DeepSeek-V3's 2.79M GPU-hours on a 2,048-GPU cluster — implying Moonshot's training slice is in the low thousands of H800s (a three-step inference, and unverified) [^61]. Even the war chest is partly in kind: roughly $400M of Alibaba's $800M investment arrived as Alibaba Cloud compute credits, making Moonshot's largest shareholder also its compute vendor [^6].

:::kv
- {term: Kimi K2 hardware, def: "NVIDIA H800 (disclosed)"}
- {term: Cluster size, def: Undisclosed}
- {term: K3 hardware, def: Undisclosed}
- {term: "DeepSeek fleet (SemiAnalysis est.)", def: "~50,000 Hopper GPUs"}
- {term: Alibaba compute credits, def: "~$400M of its $800M investment"}
- {term: Huawei Ascend use, def: No public evidence}
:::

The response to that arithmetic is Moonshot's real signature. The Muon optimizer claims roughly 2x compute efficiency over AdamW in the February 2025 Moonlight report [^90]; its MuonClip successor pre-trained K2's 15.5T tokens with zero loss spikes — no restarts, no wasted runs [^26]. K2 Thinking shipped with native INT4 quantization-aware training, halving inference memory and compute [^30]. The widely circulated $4.6M figure for K2 Thinking's training cost deserves skepticism in both directions: it came from an anonymous CNBC source, Yang Zhilin disavowed it as "not an official number," and under SemiAnalysis-style accounting a marginal-run cost excludes R&D, failed runs, and capex anyway [^28,29]. K3, released July 16, 2026, extends the pattern — 2.8T parameters at extreme sparsity (16 of 896 experts active) with quantization-aware training, on undisclosed hardware — and Bank of America framed it as proof that "pre-training scaling, paired with architectural innovation, can still deliver step-change gains" despite hardware constraints [^92]. The counterpoint deserves equal weight: efficiency-first may be strategy, not just scarcity coping. A lab that *chose* sparsity and optimizer research as its moat would look identical from the outside — and unlike DeepSeek (Ascend-validated) and Zhipu, there is no public evidence Moonshot trains or serves on Huawei silicon, though absence of evidence is not evidence of absence [^91]. The export-control picture has also inverted oddly: since January 13, 2026 BIS reviews H200/MI325X exports case-by-case, licensing ~10 Chinese hyperscalers for up to 75,000 H200s each — Moonshot not among them [^34] — yet by July 14, 2026 Commerce called cumulative shipments "trivial," concluding that Beijing's Huawei-first pressure, not US licensing, is now the binding constraint [^35].

Washington's attention arrived through a different door. On February 23, 2026, Anthropic attributed more than 3.4M Claude exchanges via fraudulent accounts to Moonshot — the second-largest of three accused Chinese labs, behind MiniMax's ~13M and far ahead of DeepSeek's 150K+, out of 16M total exchanges across ~24,000 accounts — with attribution made "through request metadata, which matched the public profiles of senior Moonshot staff" [^32].

:::bars
- {label: "MiniMax (~13M exchanges)", value: "~13M", pct: 100}
- {label: "Moonshot (~3.4M)", value: "~3.4M", pct: 26}
- {label: "DeepSeek (~0.15M)", value: "~0.15M", pct: 1}
:::

:::callout(kind=danger, label="Allegation, not adjudication")
Anthropic's distillation figures are a direct commercial competitor's own attribution, single-sourced and not independently audited. Moonshot has issued no public response in roughly five months; the only pushback has come from Chinese state media [^32] [^93]. Treat the numbers as an allegation with specific, checkable claims — not an adjudicated finding.
:::

The allegation metastasized anyway. On April 29, 2026, the House Select Committee on the CCP and House Homeland Security opened a joint investigation into Anysphere and Airbnb, with the Anysphere letter zeroing in on "Cursor's Composer 2 model, which was reportedly built on an open-weight model developed by Moonshot AI" and describing Moonshot as "publicly implicated in large-scale distillation campaigns" [^33]. Moonshot is not on the Entity List — unlike Zhipu, added January 2025 — but formal proposals exist, with the Law Reform Institute urging in March 2026 that "BIS should add DeepSeek, Moonshot, and MiniMax to the Entity List" [^65]. The proposed No Adversarial AI Act would ban adversary-nation models from federal agencies, and private-sector curbs are being "weighed" — though self-hostable open weights make any ban technically hard to enforce [^94].

Why this matters: Moonshot's two defining traits — compute frugality and radical openness — were forged by the same constraint, and they now pull in opposite directions. Efficiency research keeps the lab competitive without chips it cannot buy; the open weights that efficiency made distributable are precisely what put its name in congressional letters. The next US policy move — Entity List or not — will test whether a model you can download can be regulated at all.

## 09. Pricing a private lab against a crashing public comp set

Moonshot's $31.5B ask is being priced against unaudited revenue, a comp set that was collapsing the very week of the K3 launch, and a scarcity premium its own IPO pipeline is busy eroding.

Start with the denominator problem. The round — ~$31.5B pre-money, opened around June 30, 2026 and still unclosed as of July 17 [^11] [^10] — is a multiple of a number nobody outside the company has audited. Depending on which figure you accept, Moonshot's annualized revenue is $200M+ (April, per deal adviser Huafeng Capital) [^9], more than $300M by mid-June, or the $400-500M cited on a Nomura call [^46]. That spread alone swings the implied multiple — our own arithmetic on the $31.5B ask — from roughly ==63x to 158x ARR==; the Chinese-media analysis that surfaced the Nomura range computes ~105x on $300M and ~70x on $400-500M [^46]. Both the $20B and $31.5B marks trace to adviser leaks and press sourcing, never company confirmation — section 03 has the full chain of custody [^74].

Set that against the mid-2026 frontier-lab tape. The ladder below mixes disclosed run-rates with rumored ARR figures, so read it as directional, not precise:

:::rank-list
- {label: "xAI (~$230B / ~$500M est. ARR)", value: "~460x", pct: 100}
- {label: "Moonshot AI ($31.5B ask)", value: "~100-158x", pct: 34, highlight: true}
- {label: "Mistral (~€20B talks / $400M+ ARR)", value: "~50x", pct: 11}
- {label: "OpenAI (~$852B / ~$25B ARR)", value: "~34x", pct: 7}
- {label: "Anthropic ($965B / $47B run-rate)", value: "~20.5x", pct: 4}
:::

The anchors: Anthropic's Series H closed May 28, 2026 — $65 billion raised at $965 billion post-money on a $47 billion run-rate, about 20.5x — the only anchor in this ladder that rests on a first-party disclosure [^37]. OpenAI completed a $122 billion round on March 31, 2026 at $852 billion post-money, on roughly $2 billion of monthly revenue — about 34x [^95]. Mistral's reported €20 billion talks (Bloomberg, June 12) sit on $400M+ ARR, around 50x [^96]; xAI's ~$230 billion January 2026 mark [^95] rests on ==unconfirmed outside revenue estimates== (the ~$500M ARR figure in the ladder is an analyst guess, not a disclosure), implying a multiple somewhere in the hundreds. On the midpoint reading, Moonshot is asking for three to five times the revenue multiple of the two labs with the most defensible numbers.

The listed Chinese comps are worse — because they were repricing downward in real time. Zhipu (2513.HK) listed January 8, 2026, ran roughly 17x to a reported ~$112B peak on May 29 [^97], then fell ==28.49% on July 17 alone== — its worst day since listing — to a ~US$63B cap as of the July 17, 2026 close [^38] [^40] [^54]. Against FY2025 revenue of RMB 724.33M (~$105M) and total losses of RMB 4.72B, that is still >400x trailing sales *after* the crash [^39]. MiniMax (0100.HK) listed January 9 with a +109% debut, peaked March 18, and sat near ~US$8.7B as of July 17, 2026 — roughly -82% from peak and below its IPO-day close [^41] [^42].

:::compare
- {role: LOWEST, name: "MiniMax (0100.HK)", value: "~$8.7B — listed, -82% from peak"}
- {role: HIGHEST, name: "Zhipu (2513.HK)", value: "~$63B — listed, -28.5% on Jul 17"}
- {role: SUBJECT, name: "Moonshot AI", value: "$31.5B pre-money ask — private, unclosed"}
:::

The July 17 rout had mechanics, not just mood: cornerstone lockups expired July 8-9, releasing ~HK$90B (~$11.5B) of potential supply, and K3's launch plus a global tech selloff hit the peers the same day [^57] [^54]. Bloomberg had flagged that Zhipu and MiniMax traded at >600x and 410x sales versus 1.2x for Hang Seng Tech — and were nearly unshortable until the lockups opened [^56]. HSBC analysts added the structural point: upcoming IPOs by StepFun, Moonshot, and Baichuan will "reduce the scarcity premium" for the listed AI tigers, in a market where mainland investors turned net sellers of HK stock in May for the first time in three years [^57]. Moonshot is, in effect, part of the supply glut that is deflating its own comp set. Even DeepSeek — the sector's prestige asset — took its first external money in mid-June at only ~$50B implied (an Anhui Korrun regulatory filing: RMB 2.9B for a 0.8265% indirect stake), with a second round in talks at $71-74B [^67]. And the oldest bear line still echoes: Zhu Xiaohu's 2024-era "How do you make money out of just developing an LLM?" — he softened after DeepSeek, but the question didn't retire [^55]; Wealspring Asset now calls global AI a "super bubble" with hot Chinese names "very likely" to fall more than 80% [^56].

:::callout(kind=warn, label=Steelman)
The bull case deserves real weight. K2.6 was the #2 most-used model on OpenRouter; K3 is the largest open-weight model shipped, benchmarking near Claude Opus 4.8 at lower cost [^11]. If the $100M→$300M-in-~3.5-months momentum extrapolates to ~$1B ARR by end-2026, the forward multiple compresses to ~30x — OpenAI territory [^11]. UBS's Xiong Wei argues listed LLM pure-plays remain globally scarce [^11]. And the sharpest arbitrage point: even post-crash, Zhipu trades at >400x trailing sales as of July 17, 2026 — the public market still pays a *higher* multiple than Moonshot's private ask [^38] [^39].
:::

Which is precisely why the valuation question converges on the exit. In May 2026 Moonshot told shareholders it will dismantle its offshore VIE/red-chip structure for a Hong Kong IPO, likely late 2026-2027 under revised CSRC rules, with preliminary CICC and Goldman mandates and a ~$1B proceeds target per Bloomberg's March reporting; a joint-venture design preserves the USD investors' position [^43]. The round only makes sense as a bet that the IPO window stays open at multiples the window itself is compressing. Anyone writing into $31.5B is not really underwriting Moonshot's revenue — they are underwriting the proposition that Hong Kong will still pay 400x sales for an AI tiger by the time Moonshot rings the bell, after Moonshot and its peers have flooded the ticket.

## 10. What would break this story

Every thesis above is falsifiable, and the honest close is to say how — in both directions.

What would validate the $31.5B ask. First, audited numbers: the Hong Kong IPO process Moonshot started by unwinding its VIE structure [^43] will eventually force a prospectus, and if it confirms ARR at or above the $300M mid-June figure with the claimed growth rate [^46], the multiple debate compresses fast. Second, the weights: K3's full 2.8T-parameter release is promised by July 27, 2026 [^44] — if it ships on time and independent evaluators broadly reproduce Moonshot's claimed positioning, the open-weights franchise compounds again, as it did with K2. Third, the round itself: a close at or above $31.5B with named, non-affiliated investors would convert an ask into a print [^11].

What would break it. An IPO prospectus revealing materially lower or lower-quality revenue would be the Zhipu precedent inverted — Zhipu's first post-IPO report missed estimates and still trades above 400x sales [^39]; Moonshot enjoys no such listed cushion while private marks unwind. A K3 weights delay past July 27, or independent benchmarks landing well below the launch claims, would damage the single most valuable asset the company has: developer trust earned by shipping. An Entity List addition — formally proposed [^65] — or enacted US restrictions on Chinese-model use would cap the Western half of the API business that drives the reported revenue growth [^45]. An adverse HKIAC award on the founding dispute would create founder-equity uncertainty at prospectus time [^12] [^17]. And continued compression of the Hong Kong comp set — Zhipu -28.5% and MiniMax -15.6% in a single session this week [^40] [^54] — would leave the private ask stranded above what public markets will pay.

Two structural cautions belong in the record. Nearly every load-bearing number in Moonshot's 2026 story — ARR, round sizes, valuations — flows through a single narrative channel: deal advisers and investors with direct economic interest in the marks, sometimes via since-deleted posts [^74]. Nothing contradicts them; nothing independent confirms them either. And the company's own history counsels humility about narrative momentum: eighteen months ago the consensus story was that Moonshot was a consumer-app company worth $3.3 billion. The consensus was wrong then in both directions at once — the app was weaker than it looked, the lab stronger. The current consensus, that Moonshot is an open-weights franchise worth ten times more, deserves the same skepticism it earned.

Red-team note: an adversarial pass attempted to falsify this article's three strongest claims — the unclosed $31.5B round, the K3 launch specifics, and the QuestMobile MAU decline — with three to five contradiction-hunting searches each. It found no contradicting evidence: 3/3 top claims survived unbroken.

:::references
- {id: 1, title: "China's Moonshot AI zooms to $2.5B valuation, raising $1B for an LLM focused on long context", url: "https://techcrunch.com/2024/02/21/moonshot-ai-funding-china/", source: TechCrunch, date: "2024-02-21"}
- {id: 2, title: "XLNet: Generalized Autoregressive Pretraining for Language Understanding", url: "https://arxiv.org/abs/1906.08237", source: arXiv, date: "2019-06-19"}
- {id: 3, title: "Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context", url: "https://arxiv.org/abs/1901.02860", source: arXiv, date: "2019-01-09"}
- {id: 4, title: "Yang Zhilin interview with Zhang Xiaojun (Tencent News, republished)", url: "https://36kr.com/p/2677672437708552", source: 36Kr, date: "2024-03-06"}
- {id: 5, title: "Alibaba Group FY2024 Annual Report (Form 20-F)", url: "https://www.sec.gov/Archives/edgar/data/1577552/000095017024063767/baba-20240331.htm", source: SEC EDGAR, date: "2024-05-24"}
- {id: 6, title: "Sources: cloud credits made up ~50% of Alibaba's $800M investment in Moonshot AI (FT)", url: "https://www.techmeme.com/240512/p1", source: "Techmeme / Financial Times", date: "2024-05-12"}
- {id: 7, title: "Tencent joins $300 million financing for China's AI unicorn Moonshot", url: "https://www.bloomberg.com/news/articles/2024-08-05/tencent-joins-300-million-financing-for-china-s-ai-unicorn", source: Bloomberg, date: "2024-08-05"}
- {id: 8, title: "IDG leads $500M Series C for Moonshot AI, oversubscribed by Alibaba & Tencent", url: "https://technode.com/2025/12/31/idg-leads-500m-series-c-for-moonshot-ai-oversubscribed-by-alibaba-tencent/", source: TechNode, date: "2025-12-31"}
- {id: 9, title: "China's Moonshot AI raises $2B at $20B valuation as demand for open source AI skyrockets", url: "https://techcrunch.com/2026/05/07/chinas-moonshot-ai-raises-2b-at-20b-valuation-as-demand-for-open-source-ai-skyrockets/", source: TechCrunch, date: "2026-05-07"}
- {id: 10, title: "China's Moonshot AI seeks $30 billion value in new funding talks", url: "https://www.bloomberg.com/news/articles/2026-06-08/china-s-moonshot-ai-seeks-30-billion-value-in-new-funding-talks", source: Bloomberg, date: "2026-06-08"}
- {id: 11, title: "Moonshot's upcoming Kimi 3 is expected to close the gap with Anthropic's Opus 4.8", url: "https://techcrunch.com/2026/07/16/moonshots-upcoming-kimi-3-is-expected-to-close-the-gap-with-anthropics-opus-4-8/", source: TechCrunch, date: "2026-07-16"}
- {id: 12, title: "Moonshot AI founders in dispute with 5 investors in Hong Kong arbitration", url: "https://www.scmp.com/tech/big-tech/article/3290051/moonshot-ai-founders-dispute-5-investors-arbitration-hong-kong", source: SCMP, date: "2024-11-11"}
- {id: 13, title: "Moonshot arbitration case advances amid ongoing disputes", url: "https://technode.com/2025/02/25/moonshot-arbitration-case-advances-amid-ongoing-disputes/", source: TechNode, date: "2025-02-25"}
- {id: 14, title: "Yang Zhilin's WeChat rebuttal on the Moonshot spin-off dispute", url: "https://m.bjnews.com.cn/detail/1733626668168427.html", source: Beijing News, date: "2024-12-06"}
- {id: 15, title: "Zhu Xiaohu's allegations on Zhang Yutong's 9 million Moonshot shares", url: "https://www.time-weekly.com/post/316717", source: Time Weekly, date: "2024-12-06"}
- {id: 16, title: "Zhang Yutong confirmed as Moonshot/Kimi president", url: "https://www.nbd.com.cn/articles/2025-12-08/4172535.html", source: National Business Daily, date: "2025-12-08"}
- {id: 17, title: "Zhu Xiaohu: dispute with Moonshot still in arbitration", url: "https://www.stcn.com/article/detail/1848494.html", source: Securities Times, date: "2025-05-28"}
- {id: 18, title: "Moonshot AI launches Kimi Chat with 200,000-character context", url: "https://www.aibase.com/news/1918", source: AIbase, date: "2023-10-09"}
- {id: 19, title: "Moonshot AI's chatbot Kimi can handle 2 million Chinese characters", url: "https://thenota.com/post/2024/mar/20/moonshot-ai-chatbot-kimi-can-handle-2-million-chinese-characters/", source: The Nota, date: "2024-03-20"}
- {id: 20, title: "Kimi halts money-burning ad campaigns amid DeepSeek craze", url: "https://en.tmtpost.com/post/7461610", source: TMTPost, date: "2025-02-19"}
- {id: 21, title: "Kimi App MAU and ad-spend trajectory 2025 (QuestMobile/AppGrowing data)", url: "https://finance.eastmoney.com/a/202601303636874656.html", source: "National Business Daily / Eastmoney", date: "2026-01-30"}
- {id: 22, title: "QuestMobile: China's AI-native apps reach 499 million monthly active users", url: "https://technode.com/2026/07/14/questmobile-chinas-ai-native-apps-reach-499-million-monthly-active-users/", source: TechNode, date: "2026-07-14"}
- {id: 23, title: "DeepSeek R1 and Kimi k1.5: how Chinese labs collided on one day", url: "https://www.recodechinaai.com/p/deepseek-r1-and-kimi-k15-how-chinese", source: "Recode China AI", date: "2025-01-23"}
- {id: 24, title: "Kimi k1.5: Scaling Reinforcement Learning with LLMs", url: "https://arxiv.org/abs/2501.12599", source: arXiv, date: "2025-01-22"}
- {id: 25, title: "Kimi K2 and the Open-Source Way", url: "https://www.chinatalk.media/p/kimi-k2-the-open-source-way", source: ChinaTalk, date: "2025-07-18"}
- {id: 26, title: "Kimi K2: Open Agentic Intelligence (technical report)", url: "https://arxiv.org/abs/2507.20534", source: arXiv, date: "2025-07-28"}
- {id: 27, title: "MoonshotAI/Kimi-K2 repository and Modified MIT license", url: "https://github.com/MoonshotAI/Kimi-K2", source: GitHub, date: "2025-07-11"}
- {id: 28, title: "Alibaba-backed Moonshot releases new AI model Kimi K2 Thinking", url: "https://www.cnbc.com/2025/11/06/alibaba-backed-moonshot-releases-new-ai-model-kimi-k2-thinking.html", source: CNBC, date: "2025-11-06"}
- {id: 29, title: "Kimi K2 Thinking's reported $4.6M training cost isn't official, Moonshot CEO says", url: "https://www.yicaiglobal.com/news/kimi-k2-thinkings-reported-usd46-million-training-cost-isnt-official-moonshot-ceo-says", source: Yicai Global, date: "2025-11-11"}
- {id: 30, title: "Kimi K2 Thinking: everything you need to know", url: "https://artificialanalysis.ai/articles/kimi-k2-thinking-everything-you-need-to-know", source: "Artificial Analysis", date: "2025-11-07"}
- {id: 31, title: "Cursor admits its new coding model was built on top of Moonshot AI's Kimi", url: "https://techcrunch.com/2026/03/22/cursor-admits-its-new-coding-model-was-built-on-top-of-moonshot-ais-kimi/", source: TechCrunch, date: "2026-03-22"}
- {id: 32, title: "Detecting and preventing distillation attacks", url: "https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks", source: Anthropic, date: "2026-02-23"}
- {id: 33, title: "Chairmen Moolenaar, Garbarino announce joint investigation into Airbnb, Anysphere and the national security risks posed by Chinese AI models", url: "https://chinaselectcommittee.house.gov/media/press-releases/chairmen-moolenaar-garbarino-announce-joint-investigation-into-airbnb-anysphere-and-the-national-security-risks-posed-by-chinese-ai-models", source: "US House Select Committee", date: "2026-04-29"}
- {id: 34, title: "Commerce revises license review policy for semiconductors exported to China", url: "https://www.bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china", source: "US BIS", date: "2026-01-13"}
- {id: 35, title: "Commerce: very few H200 shipments to China have taken place", url: "https://www.cnbc.com/2026/07/14/nvidia-h200-ai-chips-china.html", source: CNBC, date: "2026-07-14"}
- {id: 36, title: "China's Moonshot claims to build models with fewer high-end AI chips than US rivals use", url: "https://www.scmp.com/tech/tech-trends/article/3332364/chinas-moonshot-claims-build-models-fewer-high-end-ai-chips-us-rivals-use", source: SCMP, date: "2025-11-11"}
- {id: 37, title: "Anthropic raises $65B in Series H funding at $965B post-money valuation", url: "https://www.anthropic.com/news/series-h", source: Anthropic, date: "2026-05-28"}
- {id: 38, title: "The first of China's 'AI tigers' goes public as Zhipu climbs in Hong Kong debut", url: "https://www.cnbc.com/2026/01/08/china-ai-tiger-goes-ipo-zhipu-hong-kong-debut-openai-knowledge-atlas-hsi-hang-seng-listing.html", source: CNBC, date: "2026-01-08"}
- {id: 39, title: "Zhipu AI revenue jumps 132% in first post-IPO report, missing estimates", url: "https://www.scmp.com/tech/tech-trends/article/3348555/zhipu-ai-revenue-jumps-132-first-post-ipo-report-missing-estimates", source: SCMP, date: "2026-04-01"}
- {id: 40, title: "Zhipu (2513.HK) quote, July 17, 2026", url: "https://stockanalysis.com/quote/hkg/2513/", source: StockAnalysis, date: "2026-07-17"}
- {id: 41, title: "MiniMax doubles in Hong Kong debut a day after Zhipu's IPO", url: "https://www.cnbc.com/2026/01/09/minimax-hong-kong-ipo-ai-tigers-zhipu.html", source: CNBC, date: "2026-01-09"}
- {id: 42, title: "MiniMax Group (0100.HK) market cap history", url: "https://stockanalysis.com/quote/hkg/0100/market-cap/", source: StockAnalysis, date: "2026-07-17"}
- {id: 43, title: "China's Moonshot AI moves to unwind offshore structure in IPO pursuit", url: "https://www.scmp.com/tech/big-tech/article/3354078/chinas-moonshot-ai-moves-unwind-offshore-structure-ipo-pursuit-sources", source: SCMP, date: "2026-05-18"}
- {id: 44, title: "Kimi K3", url: "https://www.kimi.com/blog/kimi-k3", source: "Moonshot AI", date: "2026-07-16"}
- {id: 45, title: "Moonshot AI sees overseas revenue surge as Kimi K2.5 gains traction abroad", url: "https://kr-asia.com/moonshot-ai-sees-overseas-revenue-surge-as-kimi-k2-5-gains-traction-abroad", source: KrASIA, date: "2026-03-15"}
- {id: 46, title: "Moonshot AI and DeepSeek lead China's AI valuation surge with high P/ARR multiples", url: "https://www.kucoin.com/news/flash/moonshot-ai-and-deepseek-lead-china-s-ai-valuation-surge-with-high-p-arr-multiples", source: "KuCoin News / TechFlow", date: "2026-07-10"}
- {id: 48, title: "Interview with Moonshot enterprise lead Huang Zhenxin", url: "https://finance.sina.com.cn/tech/roll/2026-06-25/doc-inierayw5701544.shtml", source: "Jiemian via Sina", date: "2026-06-25"}
- {id: 49, title: "moonshotai/Kimi-K2-Instruct model API metadata", url: "https://huggingface.co/api/models/moonshotai/Kimi-K2-Instruct", source: "Hugging Face", date: "2026-07-17"}
- {id: 50, title: "World's first trillion-parameter open-source model Kimi K2 doubles downloads in a single weekend", url: "https://www.globaltimes.cn/page/202507/1339012.shtml", source: "Global Times", date: "2025-07-14"}
- {id: 51, title: "Groq is serving Kimi K2 at >400 output tokens/s, 40X faster than Moonshot's first-party API", url: "https://x.com/ArtificialAnlys/status/1945989223330549768", source: "Artificial Analysis (X)", date: "2025-07-17"}
- {id: 52, title: "State of AI: insights from 100 trillion OpenRouter tokens", url: "https://a16z.com/state-of-ai/", source: "a16z / OpenRouter", date: "2026-01-15"}
- {id: 53, title: "Perplexity may use Kimi K2 for post-training, CEO says", url: "https://en.tmtpost.com/news/7625363", source: TMTPost, date: "2025-07-12"}
- {id: 54, title: "Moonshot AI's Kimi K3 launch hammers rival AI stocks", url: "https://qz.com/moonshot-ai-kimi-k3-model-launch-rival-stocks-071726", source: Quartz, date: "2026-07-17"}
- {id: 55, title: "Chinese venture capitalist Allen Zhu steers clear of LLM frenzy", url: "https://www.scmp.com/tech/tech-trends/article/3254560/chinese-venture-capitalist-allen-zhu-steers-clear-mainland-tech-firms-ai-large-language-model-frenzy", source: SCMP, date: "2024-03-10"}
- {id: 56, title: "From scarcity to execution: China's AI valuation reset", url: "https://thebambooworks.com/from-scarcity-to-execution-chinas-ai-valuation-reset/", source: "The Bamboo Works", date: "2026-06-18"}
- {id: 57, title: "Zhipu AI, MiniMax shares provide gut check for Hong Kong investors as lock-ups end", url: "https://www.scmp.com/business/markets/article/3359697/zhipu-ai-minimax-shares-provide-gut-check-hong-kong-investors-lock-ups-end", source: SCMP, date: "2026-07-07"}
- {id: 58, title: "Moonshot sharply cuts ad and user-acquisition budgets", url: "https://news.qq.com/rain/a/20250218A0686600", source: "Jiemian via QQ News", date: "2025-02-18"}
- {id: 59, title: "Moonshot shuts overseas apps Ohai and Noisee; product leads depart", url: "https://www.sohu.com/a/825856255_122074763", source: "LatePost via Sohu", date: "2024-11-12"}
- {id: 61, title: "DeepSeek debates: Chinese leadership on cost, true training cost, closed model margin impacts", url: "https://newsletter.semianalysis.com/p/deepseek-debates", source: SemiAnalysis, date: "2025-01-31"}
- {id: 64, title: "moonshotai/kimi-k3", url: "https://openrouter.ai/moonshotai/kimi-k3", source: OpenRouter, date: "2026-07-16"}
- {id: 65, title: "Petition to add DeepSeek, Moonshot, and MiniMax to the Entity List", url: "https://lawreforminstitute.org/distillation031326.pdf", source: "Law Reform Institute", date: "2026-03-13"}
- {id: 67, title: "DeepSeek valuation pegged at ~$52 billion by Chinese regulatory filing", url: "https://cryptobriefing.com/deepseek-valuation-52-billion-chinese-filing/", source: "Crypto Briefing", date: "2026-07-10"}
- {id: 69, title: "AI community reacts to Kimi K3's release", url: "https://officechai.com/ai/beginning-of-a-new-era-ai-community-reacts-to-kimi-k3s-release-with-implications-for-tech-geopolitics/", source: OfficeChai, date: "2026-07-16"}
- {id: 71, title: "Moonshot AI founding equity structure (Chinese corporate-registry analysis)", url: "https://zhuanlan.zhihu.com/p/710376176", source: "Zhihu", date: "2024-07-15"}
- {id: 72, title: "Recurrent AI: conversation intelligence for enterprise sales", url: "https://chuangxin.chinadaily.com.cn/a/201909/26/WS5d8c7213a31099ab995e28b8.html", source: "China Daily", date: "2019-09-26"}
- {id: 73, title: "China AI startup Moonshot seeks $10 billion value in new funding", url: "https://www.bloomberg.com/news/articles/2026-02-17/china-ai-startup-moonshot-seeks-10-billion-value-in-new-funding", source: Bloomberg, date: "2026-02-17"}
- {id: 74, title: "Moonshot AI eyes US$30 billion valuation as China's AI race intensifies", url: "https://www.scmp.com/tech/article/3356348/moonshot-ai-eyes-us30-billion-valuation-chinas-ai-race-intensifies", source: SCMP, date: "2026-06-08"}
- {id: 75, title: "Zhilin Yang profile (secondary-cash-out report and denial)", url: "https://baike.baidu.com/en/item/Zhilin%20Yang/654557", source: "Baidu Baike / Jiemian", date: "2024-04-23"}
- {id: 76, title: "Kimi launches first reasoning model k0-math", url: "https://www.globaltimes.cn/page/202411/1323248.shtml", source: "Global Times", date: "2024-11-16"}
- {id: 77, title: "Kimi's customer-acquisition costs in the 2024 AI app price war", url: "https://eu.36kr.com/en/p/3631566219522822", source: 36Kr, date: "2024-03-25"}
- {id: 78, title: "China AI app rankings, June 2026", url: "https://www.aicpb.com/en/ai-rankings/products/apps", source: AICPB, date: "2026-07-06"}
- {id: 79, title: "K2's release was a declaration of returning to the AGI main line", url: "https://eu.36kr.com/en/p/3385374882397957", source: 36Kr, date: "2025-07-19"}
- {id: 80, title: "Four Chinese AI startups to watch beyond DeepSeek", url: "https://www.technologyreview.com/2025/02/04/1110942/four-chinese-ai-startups-deepseek/", source: "MIT Technology Review", date: "2025-02-04"}
- {id: 81, title: "Kimi K2 Thinking: the $4.6M model shifting the open-source frontier", url: "https://www.recodechinaai.com/p/kimi-k2-thinking-the-46m-model-shifting", source: "Recode China AI", date: "2025-11-10"}
- {id: 82, title: "Moonshot co-founders' first joint AMA: 21 questions", url: "https://eu.36kr.com/en/p/3548523752173447", source: 36Kr, date: "2025-11-11"}
- {id: 83, title: "Kimi K2.6: the new leading open weights model", url: "https://artificialanalysis.ai/articles/kimi-k2-6-the-new-leading-open-weights-model", source: "Artificial Analysis", date: "2026-04-25"}
- {id: 84, title: "Kimi K2 Thinking: what it means", url: "https://www.interconnects.ai/p/kimi-k2-thinking-what-it-means", source: Interconnects, date: "2025-11-10"}
- {id: 85, title: "Kimi's open model K3 nears GPT-5.6 Sol and Fable 5 while signaling the end of super-cheap Chinese AI", url: "https://the-decoder.com/kimis-open-model-k3-nears-gpt-5-6-sol-and-fable-5-while-signaling-the-end-of-super-cheap-chinese-ai/", source: "The Decoder", date: "2026-07-17"}
- {id: 86, title: "Kimi Code plans and pricing", url: "https://www.kimi.com/code/en", source: "Moonshot AI", date: "2026-07-01"}
- {id: 87, title: "Kimi's enterprise chief on partner-led deployment", url: "https://x.com/TechBuzzChina/status/2073270599024042290", source: "TechBuzzChina (X)", date: "2026-06-20"}
- {id: 88, title: "Moonshot AI retains lawyer to respond to arbitration filed by investors", url: "https://en.tmtpost.com/news/7332009", source: TMTPost, date: "2024-11-11"}
- {id: 89, title: "Moonshot arbitration settlement talks: 20% demanded, 10% offered", url: "https://finance.sina.com.cn/stock/aigcy/2025-02-24/doc-inemqprf2155880.shtml", source: "36Kr Waves via Sina", date: "2025-02-24"}
- {id: 90, title: "Muon is scalable for LLM training (Moonlight announcement)", url: "https://x.com/Kimi_Moonshot/status/1893379158472044623", source: "Moonshot AI (X)", date: "2025-02-22"}
- {id: 91, title: "Huawei-led team claims it post-trained DeepSeek's 1.6-trillion-parameter model on Ascend 910C chips", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/huawei-led-team-claims-it-post-trained-deepseeks-1-6-trillion-parameter-models-on-ascend-910c-chips", source: "Tom's Hardware", date: "2026-06-15"}
- {id: 92, title: "Moonshot releases 2.8-trillion-parameter Kimi K3", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/moonshot-releases-2-8-trillion-parameter-kimi-k3", source: "Tom's Hardware", date: "2026-07-16"}
- {id: 93, title: "Anthropic accuses Chinese AI labs of mining Claude as US debates AI chip exports", url: "https://techcrunch.com/2026/02/23/anthropic-accuses-chinese-ai-labs-of-mining-claude-as-us-debates-ai-chip-exports/", source: TechCrunch, date: "2026-02-23"}
- {id: 94, title: "Washington wants Chinese AI out of corporate America — open weights block the ban", url: "https://www.techtimes.com/articles/320171/20260711/washington-wants-chinese-ai-out-corporate-america-open-weights-block-ban.htm", source: "Tech Times", date: "2026-07-11"}
- {id: 95, title: "OpenAI valuation reaches $852 billion after massive funding round", url: "https://www.forbes.com/sites/antoniopequenoiv/2026/03/31/openai-valuation-reaches-852-billion-after-massive-funding-round/", source: Forbes, date: "2026-03-31"}
- {id: 96, title: "France's Mistral in funding talks at about €20 billion valuation", url: "https://www.bloomberg.com/news/articles/2026-06-12/france-s-mistral-in-funding-talks-at-about-20-billion-valuation", source: Bloomberg, date: "2026-06-12"}
- {id: 97, title: "China AI developer Zhipu hits record $112 billion valuation", url: "https://www.caixinglobal.com/2026-05-29/china-ai-developer-zhipu-hits-record-112-billion-valuation-102449295.html", source: Caixin Global, date: "2026-05-29"}
:::
