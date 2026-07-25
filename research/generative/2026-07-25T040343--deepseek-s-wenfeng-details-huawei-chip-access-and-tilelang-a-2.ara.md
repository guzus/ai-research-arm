---
eyebrow: UPDATE · AI POLICY
title: "Five Fights in 48 Hours"
deck: A leaked Wenfeng transcript, a tripled Kimi K3 price tag, dueling industry letters, and Beijing's own export-control mirror — what actually moved since "The Ban That Isn't One Yet"
lede: |
  Two days after nearly 200 startups asked Washington not to ban Chinese open-weight AI, the story didn't resolve — it multiplied. A leaked, unverified transcript surfaced with the on-the-record Wenfeng material the public record has lacked since 2024. Moonshot's Kimi K3 tripled its own price the same week it was accused of distilling a rival's model. Nvidia backed a rival industry letter in its CEO's first-ever post on X, while OpenAI and Anthropic stayed off both letters. And Beijing kept drafting the same kind of export controls Washington is threatening to impose. None of the five fights below existed in this form on July 23; each complicates, rather than resolves, who actually controls Chinese open-weight AI's path into the U.S. market.
stats:
  - {label: "Kimi K3 price hike", value: "3.75x", note: "output tokens, K2.6→K3 — now matches Claude Sonnet 5"}
  - {label: "Wenfeng transcript status", value: "Unconfirmed", note: "leaked, auto-transcribed; DeepSeek silent"}
  - {label: "New pro-open-weight signatories", value: "25", note: "Nvidia, Microsoft, Meta, Dell, Palantir...; OpenAI/Anthropic absent"}
  - {label: "PHLX Semiconductor Index", value: "-10%", note: "week of Kimi K3 launch"}
domain: policy
---

:::kv
- {term: "What's actually new since July 23", def: "A leaked Wenfeng transcript, a Kimi K3 price hike, a Kratsios/Moonshot fight with a Chinese-government rebuttal, a second pro-open-weight industry letter, and sharper — but still unconfirmed — Ascend order numbers"}
- {term: "What hasn't moved", def: "No enacted ban, no published signatory roster for the 200-firm letter, no committee markup on H.R. 4142, no sanctions actually imposed"}
- {term: "Most complicating new fact", def: "Kimi K3, July's loudest 'cheap Chinese AI' headline, just tripled its own price to Claude Sonnet 5's level"}
- {term: "Most fragile new fact", def: "The only new Wenfeng material is a leaked, machine-transcribed recording DeepSeek has not confirmed"}
:::

:::timeline
- {date: "2026-07-21", headline: "Bessent threatens sanctions", body: "Treasury Secretary cites AI-model \"watermarks\"; later reporting names four labs under review — Moonshot, DeepSeek, MiniMax, Alibaba."}
- {date: "2026-07-22", headline: "Little Tech Association letter; Huang defends China's models", body: "The 200-firm coalition's letter goes to five officials; Nvidia's CEO tells Axios Chinese open models are \"excellent.\""}
- {date: "2026-07-23", headline: "Kratsios accuses Moonshot; Wenfeng transcript surfaces; Moonshot denies", body: "OSTP's director alleges distillation and banned-chip use; Tencent Tech publishes the leaked investor transcript; Moonshot's Huang Zhenxin denies the distillation claim."}
- {date: "2026-07-24", headline: "25-company letter backs open weights", body: "Nvidia, Microsoft, Meta, Dell, Palantir and 21 others publish a counter-letter; OpenAI and Anthropic do not sign."}
- {date: "2026-07-27", headline: "Kimi K3's full weights are due", body: "Scheduled, not yet published as of this writing — the test of Moonshot's transparency offer."}
:::

## 01. The transcript that filled the gap — but didn't close it

The most-cited hole in the DeepSeek-Huawei story — no verified 2026 Wenfeng quote on the record — got a candidate fix this week, and it arrived exactly the way skepticism would predict: unconfirmed, secondhand, and machine-transcribed.

In late July, Tencent Tech published a lightly edited transcript of what it describes as a roughly three-hour-forty-four-minute closed-door investor meeting with Liang Wenfeng, sourced from a recording ("deepseek_0520.m4a") pointing to a May 20, 2026 meeting date [^1,2]. Multiple Chinese outlets circulated overlapping versions after the file spread on WeChat before being taken down; Tencent's version is the most complete of those in circulation [^1]. DeepSeek has not confirmed the recording is authentic, and the publisher's own release carries a disclaimer that the text was auto-transcribed from speech recognition and "individual proper nouns and numbers may contain recognition errors" [^1] — a caveat doing real work, given the numbers in it.

:::quote(attr="Attributed to Liang Wenfeng, leaked transcript, published 2026-07-23")
NVIDIA's CUDA moat is rapidly disintegrating.
:::

The transcript, as published, has the speaker saying Huawei allocates DeepSeek roughly 16,000 cards of capacity, that "four Huawei cards equal one Nvidia card" in practical throughput, and that broader ecosystem parity should arrive "within a year" even as production-capacity constraints persist longer [^1]. It separately attributes to the speaker a claim that China is running on the order of 20,000 H-equivalent compute cards under acquisition constraints — DeepSeek's own holdings, per the text, not a national figure [^1].

==unverified: every quote in this section traces to one leaked, auto-transcribed recording with no confirmation from DeepSeek, no named publication byline claiming direct access to Wenfeng, and an explicit machine-transcription-error disclaimer from the outlet that published it — treat the specific numbers (16,000 cards, a 4:1 card ratio, "within a year") as reported content of a disputed document, not as verified facts about DeepSeek's compute position==. That is a materially different evidentiary category from the confirmed, dual-sourced fact this publication previously treated as the strongest item in the record: Huawei's own statement, corroborated by DeepSeek's V4 technical report, that Ascend chips trained part of V4-Flash [^3]. A leaked recording of unverified provenance saying the moat is "disintegrating" does not carry the same weight as two institutions independently confirming a specific technical fact.

The tension is worth sitting with rather than resolving prematurely: if the transcript is genuine, it is the first extended Wenfeng-attributed remarks on exactly the questions — chip access, CUDA dependency, timeline to parity — that reporting has spent eighteen months answering without him. If it is embellished, garbled by transcription, or not him at all, it is simply the loudest unverified claim yet in a story that has repeatedly rewarded skepticism toward secondhand attribution. Why it matters: everything downstream in this piece and its predecessor about DeepSeek's hardware trajectory still rests more on documents (technical reports, chip-order reporting) than on founder testimony — and that gap, not this transcript, remains the load-bearing fact.

## 02. The discount was the product

Kimi K3 was July's loudest argument that Chinese open-weight models undercut American ones on price. In the same week Washington accused its maker of stealing a rival's technology, Moonshot tripled that price — complicating the exact economic case the 200-firm coalition in Section 4 is built on.

Moonshot's own API pricing for Kimi K3 is $3 per million input tokens and $15 per million output tokens — a figure independently confirmed on OpenRouter's own listing — versus $0.95 and $4 for predecessor Kimi K2.6, a 3.16x jump on input and 3.75x on output, inside the same lab, under three months apart [^4,5,29]. The new number is not incidentally close to a leading closed-source competitor's price; it lands exactly on Claude Sonnet 5's published rate, prompting at least one independent outlet to frame the release as signaling "the end of super cheap Chinese AI" [^4,30].

:::slope(left-label="Kimi K2.6", right-label="Kimi K3", unit=$)
| Item | Kimi K2.6 | Kimi K3 |
|------|-----------|---------|
| Input $/Mtok | 0.95 | 3 |
| Output $/Mtok | 4 | 15 |
:::

Capability moved too, in both directions. On Artificial Analysis's own AA-Omniscience benchmark, K3's accuracy climbed from 33% to 46% relative to K2.6 — but its hallucination rate climbed alongside it, from 39% to 51%, and Moonshot's own published charts carry the accuracy gain without the hallucination number, which surfaced through Artificial Analysis's independent evaluation rather than Moonshot's marketing materials [^6,28]. Artificial Analysis frames this as structural, not K3-specific: benchmark scoring across frontier models generally rewards confident answers and penalizes abstention more than it penalizes being wrong [^28]. On the broader Artificial Analysis Intelligence Index v4.1, K3 scored 57.1 against GPT-5.6 Sol Max's 58.9 and Claude Fable 5's 59.9 — third place among the tracked frontier configurations, not a clean win, though K3 separately topped LMArena's blind Frontend Code Arena [^7].

:::rank-list
- {label: "Claude Fable 5", value: "59.9", pct: 100}
- {label: "GPT-5.6 Sol Max", value: "58.9", pct: 98}
- {label: "Kimi K3", value: "57.1", pct: 95, highlight: true}
:::

The full open weights — the step that lets outside researchers actually verify Moonshot's architecture claims (Section 3) — are scheduled for HuggingFace on July 27 under a Modified MIT license [^7,8]; as of this writing they have not shipped. Until they do, every capability and cost figure above describes API access to a hosted model, not an inspectable open-weight release.

:::callout(kind=warn, label="Counterpoint")
One model's price hike is not proof the broader "cheap Chinese open-weight" thesis in this publication's prior coverage has collapsed. DeepSeek's own API pricing did not move, and Section 4's coalition includes firms that migrated to DeepSeek, GLM-5.2, and other models whose pricing is unchanged. K3 pricing tripling is a genuine complication for K3 specifically — treating it as refutation of the whole category overstates a single data point.
:::

Why it matters: the economic argument the Little Tech Association leans on — that a ban would strip U.S. startups of cheap, capable open-weight options — gets weaker precisely where the story got loudest. The highest-profile new Chinese model of the month didn't stay cheap; it repriced itself into direct competition with the U.S. labs the coalition says a ban would entrench.

## 03. Kratsios vs. Moonshot: an accusation, a named rebuttal, and a government-to-government fight

The prior article noted Moonshot "has not publicly addressed" Kratsios's allegations. That has changed, and the exchange since is more informative than the original accusation.

OSTP Director Michael Kratsios posted on X that "we have information that Moonshot AI distilled Anthropic's Fable for the development of its K3 model," describing "a sophisticated internal platform to conduct large scale distillation against U.S. models" and separately alleging Moonshot "acquired GB300-equipped servers and has accessed GB300s in Thailand, likely to train its AI models" [^9]. Treasury's parallel review, per multiple outlets, now reportedly spans four labs rather than one: Moonshot, DeepSeek, MiniMax, and Alibaba [^10,11].

:::kv
- {term: "The allegation", def: "Large-scale, covert distillation of Anthropic's Fable, plus unauthorized access to export-banned Nvidia GB300 servers via Thailand"}
- {term: "Who made it", def: "Michael Kratsios, White House OSTP Director, via X — no logs or procurement trail disclosed publicly"}
- {term: "The rebuttal", def: "Moonshot's Huang Zhenxin (head of enterprise business) denies distillation, credits three named architecture changes instead"}
- {term: "The government response", def: "Chinese embassy: \"entirely unfounded\" / \"pure slander\"; Foreign Ministry: opposes \"politicizing and instrumentalizing trade and tech issues\""}
:::

Moonshot's rebuttal is unusually specific for a corporate denial: Huang Zhenxin named three architecture changes — Moon Clip, Kimi Delta Attention, and Attention Residuals — as the actual source of K3's gains, crediting Moon Clip with roughly doubling training efficiency while halving compute cost, Kimi Delta Attention with a tenfold context-window expansion, and Attention Residuals with a 25% reasoning-speed increase [^12]. Two of those three names independently appear in Moonshot's own HuggingFace release page and launch blog, which is corroboration of the architecture's existence, not of the denial's truth [^12].

Outside experts lean toward the rebuttal on timeline grounds rather than trust. Braden Hancock (Laude Institute, Snorkel AI co-founder) argued the roughly two-week gap between Fable 5's July 1 public release and K3's July 16–17 launch left too little time to extract, train, and ship a model of that caliber — "there's just not even frankly time" [^13]. Nathan Lambert (Allen Institute for AI) made a structural version of the same point: as Chinese labs approach the frontier, simple output-copying delivers diminishing returns, and the reinforcement-learning infrastructure needed for real capability gains is a different, harder-to-hide undertaking than querying a rival's API — "if it were the case, everyone would be easily able to catch up" [^13]. Neither expert had access to Kratsios's underlying evidence, which — as of this writing — has not been disclosed publicly: no query logs, no procurement paper trail for the alleged GB300 servers [^13].

The allegation is not manufactured from nothing, which cuts against reading it as pure pretext — but the strongest evidence predates and cannot cover the specific claim. Anthropic itself reported in February 2026 that it had identified industrial-scale attempts by three labs, including Moonshot, to extract Claude's capabilities via roughly 16 million exchanges through some 24,000 accounts [^31]. That report establishes a documented pattern of the kind of behavior Kratsios is now alleging — but Fable 5 did not launch until June 9, 2026, four months later, so the February evidence cannot by itself demonstrate that Fable 5 specifically was distilled into K3 [^31].

China's government answered with volume rather than technical rebuttal. Embassy spokesperson Liu Chang called the allegations "entirely unfounded" in one statement and "pure slander" in another, framing them as an attempt to "discredit China's AI industry achievements"; Foreign Ministry spokesperson Lin Jian added that Beijing "opposes politicizing and instrumentalizing trade and tech issues" [^14,15].

:::callout(kind=danger, label="Unresolved")
Nobody outside the U.S. government has seen Kratsios's evidence, and nobody outside Moonshot has independently verified the architecture claims in its denial. The July 27 weights release is the first point at which outside researchers could actually check — which is also, not coincidentally, the date Moonshot itself has pointed to as vindication [^7].
:::

Why it matters: this is no longer a one-sided allegation sitting unanswered, as it was on July 23. It is now a credibility contest between a government accusation with no public evidence trail and a corporate denial with partial, self-interested corroboration — and the strongest independent voices in the debate (Hancock, Lambert) currently lean toward "the timeline doesn't support the accusation," not toward either side's preferred narrative.

## 04. Two letters, not one

The 200-firm coalition covered in this publication's prior piece is no longer the only organized voice in the fight. In 48 hours it acquired both a mirror-image ally and a pointed omission.

On July 24, a 25-company coalition — Nvidia, Microsoft, Meta, Dell Technologies, IBM, Palantir, CrowdStrike, ServiceNow, Hugging Face, Mistral, Andreessen Horowitz, Y Combinator, the Linux Foundation, and others — published "Open Weights and American AI Leadership," arguing that U.S. AI dominance depends on a thriving open-weight ecosystem, not a handful of closed frontier models [^16,17]. The letter explicitly defends distillation as "a widely used technique for model improvement, evaluation, and validation... a long tradition of learning from, building upon, and improving existing technologies," distinguishing it from unlawful extraction, which it argues should be handled through narrow legal remedies rather than blanket restrictions [^16]. Jensen Huang publicized it in the first post of his career on X: "open models strengthen safety and cybersecurity, accelerate innovation and diffusion, and enable sovereignty" [^16].

The pointed part is who is missing. OpenAI, Anthropic, and Google did not sign [^17] — the same two U.S. labs the Little Tech Association's Suhail Doshi named as the beneficiaries of a ban ("it's great for Anthropic. We're all going to have to spend money on Anthropic") [^18]. OpenAI's Sam Altman offered a hedge rather than a signature, writing on X that he was "glad to see" the letter and that he wants "the US to win in AI both in open source and proprietary models" [^17] — rhetorical support without joining the coalition asking Washington not to restrict the category OpenAI itself avoids releasing weights for.

| Coalition | Signed Jul 22 letter | Signed Jul 24 letter |
|---|---|---|
| ~200 venture-backed startups (Little Tech Association) | Yes | No |
| 25 chipmakers/cloud/infra/security firms (Nvidia, Microsoft, Dell, IBM...) | No | Yes |
| *OpenAI, Anthropic, Google | No | No |

The administration's own response has stayed generic. White House spokesperson Liz Huston offered a talking point — "the United States leads the world in AI innovation, and President Trump will keep it that way" — that addresses neither letter's specific ask, while an unnamed official separately dismissed ban-imminent speculation as "baseless" [^19]. Commerce Secretary Lutnick, addressee of both letters, has issued no public response to either as of this writing [^19].

Why it matters: the July 22 story was "startups vs. an undecided administration." By July 24 it had become "most of the AI infrastructure stack, on both the chip and cloud side, plus most open-weight-friendly startups, against two frontier labs that stayed silent on both letters" — a coalition map that makes a blanket ban look more politically costly than it did 48 hours earlier, independent of whether the underlying security case strengthens or weakens.

## 05. The chip numbers get specific — and thinner

Ascend 950PR order figures moved from "hundreds of thousands, thirdhand" to a named dollar amount and company — but the sourcing got no more solid, and arguably less.

Multiple aggregator sites now report ByteDance committed $5.6 billion to Ascend 950PR orders, the largest single AI-chip procurement commitment from a Chinese firm to a domestic chipmaker, implying roughly 350,000 units at an assumed ~$16,000 per-unit price [^20,21]. Combined with unspecified orders from Alibaba Cloud and Tencent, total committed procurement is reported above 500,000 units against Huawei's stated 2026 production target of 750,000 [^20,21]. None of the pieces carrying this figure cites a named primary source — no Reuters byline, no regulatory filing, no earnings-call disclosure — a step down in sourcing rigor from the TrendForce-relayed, Reuters-sourced figures this publication treated cautiously in its prior coverage.

:::compare
- {role: "BYTEDANCE ORDER (implied, unattributed)", name: "Ascend 950PR units", value: "~350,000"}
- {role: "HUAWEI 2026 PRODUCTION TARGET", name: "Ascend 950PR units", value: "750,000"}
- {role: "SEMIANALYSIS HBM CEILING (910C-gen est.)", name: "Ascend units/yr", value: "~275,000-300,000"}
:::

Laid against the earlier SemiAnalysis estimate that domestic HBM supply from CXMT caps prior-generation Ascend production near 275,000–300,000 units per year, an unattributed ~350,000-unit single-customer order — before Alibaba's and Tencent's volumes are even counted — would already sit at or past that ceiling [^22]. Two readings are both consistent with the same numbers: either domestic HBM output has scaled meaningfully past the earlier estimate (plausible, given the 950PR's newer "HiBL 1.0" in-house memory), or the $5.6B figure is inflated, mis-sourced, or describes multi-year commitments compressed into a single-year headline. Nothing in available reporting resolves which.

:::note
The $5.6B figure and its 350,000-unit implication appear identically across several aggregator sites without a traceable original source — a pattern consistent with one unverified number propagating through republication rather than being independently confirmed by multiple reporting chains.
:::

Why it matters: a specific dollar figure reads as more credible than "hundreds of thousands" did in the prior piece, but specificity is not the same as verification. The gap between a headline order size and a supply-chain capacity ceiling that was already tight is exactly the kind of tension a confirmed IR filing or earnings-call disclosure would resolve — and none has surfaced.

## 06. Beijing's mirror gets a tier system, and a September deadline

China's own draft export controls on AI model weights, reported in outline on July 21, gained structural detail this week — and a diplomatic calendar that explains the timing.

MOFCOM, consulting Alibaba, ByteDance, and Z.ai (the rebranded Zhipu), is reportedly weighing a tiered regime: simple filing requirements for less-capable open-source models, security reviews for stronger systems, and a possible outright ban on public release for the most capable ones — with models not yet released explicitly in scope [^23,24]. A separate, related proposal would tighten scrutiny of foreign acquisitions of Chinese AI and agentic-technology firms, reportedly informed by what officials view as a loophole behind Meta's roughly $2 billion Manus acquisition, a deal Chinese regulators later ordered unwound [^23]. Officials have also discussed treating leaks of proprietary Chinese AI technology as a national-security-law violation [^23] — the same "IP theft" framing Bessent is applying to Chinese models trained on U.S. output (Section 3), mirrored back onto China's own companies.

:::kv
- {term: "Tier 1", def: "Less-capable open models — filing requirement only"}
- {term: "Tier 2", def: "Stronger systems — mandatory security review"}
- {term: "Tier 3", def: "Most capable models — possible public-release ban"}
- {term: "Also considered", def: "Foreign-acquisition scrutiny for AI/agentic-tech firms; chip-design export bar for TSMC/Qualcomm on Huawei/Alibaba/ByteDance designs"}
:::

The timing is the genuinely new context: both governments are reportedly heading toward their first official AI dialogue under the Trump administration in September 2026, ahead of a planned September 24 Xi Jinping visit to the U.S., with Bessent expected to lead the American delegation and raise distillation concerns directly [^23]. Read against that calendar, both countries' current posture — threats and drafts, not enacted rules — looks less like imminent unilateral action and more like each side establishing a negotiating position before the same conversation.

Why it matters: the prior article treated Beijing's drafting as an irony — a government publicly championing open AI while privately restricting its own exports. The September dialogue reframes that irony as leverage-building: neither Washington's procurement-rule threats nor Beijing's tiered-release drafts need to become law to do political work if both sides expect to trade concessions at the table in six weeks.

## 07. What hasn't moved

Against five fast-moving fights, three load-bearing facts from the prior piece are exactly where they were on July 23 — worth stating plainly, because escalating rhetoric can create an impression of motion that the record doesn't support.

No signatory roster for the Little Tech Association's "nearly 200" companies has been published; the association's own site names a handful of members (Proton, Y Combinator, Replit, Yelp, Particle) without a full list, unchanged from the prior article's finding [^25]. H.R. 4142, the No Adversarial AI Act, remains referred to the House Committee on Oversight and Government Reform with no recorded markup, vote, or committee report; its Senate companion, S.2177, is similarly parked in committee [^26,27]. And despite two rounds of sanctions rhetoric from Bessent and a formal accusation from Kratsios, no sanction, Entity List addition, or enforcement action against any of the four named labs has actually been imposed [^10].

:::stats
- {label: "Signatory roster published", value: "No", note: "littletech.org lists members, not a full list"}
- {label: "H.R. 4142 status", value: "In committee", note: "No markup since June 2025 introduction"}
- {label: "Sanctions imposed", value: "0", note: "Of 4 named labs, as of Jul 25"}
:::

Why it matters: the volume of the past 48 hours' rhetoric — a government accusation, a corporate denial, two competing industry letters, a leaked founder transcript — has not yet translated into a single new enacted rule, roster, or sanction. That gap between escalating talk and static process is itself the most stable fact in this update.

## 08. What could break this update's thesis

This piece has treated the leaked Wenfeng transcript skeptically, the Kimi K3 price hike as a genuine complication, and the distillation accusation as unresolved in Moonshot's favor on timeline grounds. Each of those readings has a specific failure mode.

The transcript skepticism collapses if DeepSeek confirms the recording, or if a second independently sourced recording of the same meeting surfaces with matching content — convergent leaks are harder to dismiss than a single one, even without an official confirmation. Nothing in current reporting suggests that is imminent, but it is the single fact that would most change Section 1's conclusion [^1].

The pricing-complication argument weakens if Moonshot walks the price back before or shortly after the July 27 weights release, which would reframe the hike as a temporary hosted-API premium rather than a durable repricing of the "cheap Chinese AI" category — plausible given that self-hosted deployment of the open weights, once available, would let large customers bypass Moonshot's API pricing entirely [^7,8].

The distillation-skepticism argument is the most exposed. Hancock's and Lambert's timeline objections both rest on an assumption that large-scale RL-based distillation requires proportionally large compute and time; neither has seen Kratsios's underlying evidence, and a government intelligence assessment — if one exists and is later disclosed — could rest on access (server logs, procurement records) that outside researchers structurally cannot replicate from the outside [^13]. The July 27 weights release will let outside researchers inspect K3's architecture directly, which narrows but does not eliminate this gap: architectural novelty is evidence against wholesale weight-copying, but it does not, by itself, rule out output-level distillation during training.

:::callout(kind=info, label="Net read")
None of the five fights in this update resolved the underlying question the prior article posed — whether "banning" Chinese open-weight AI is legally coherent or enforceable. What changed is that the evidentiary record on both the technical claims (Wenfeng's chip access, Moonshot's architecture) and the political ones (who's lobbying whom) got denser without getting more settled. That is a meaningfully different state than July 23, even though the headline legal status — no enacted ban — has not moved at all.
:::

:::references
- {id: 1, title: "DeepSeek's Liang Wenfeng Breaks His Silence", url: "https://www.fredgao.com/p/deepseeks-liang-wenfeng-breaks-his", source: "Fred Gao (translated transcript)", date: "2026-07-23"}
- {id: 2, title: "Full transcript of Wenfeng's investor conference call", url: "https://thelowdown.momentum.asia/full-transcript-of-deepseek-founder-liang-wenfengs-fundraising-meeting/", source: "The Low Down / Momentum Works", date: "2026-07-23"}
- {id: 3, title: "Exclusive: China's DeepSeek developing its own AI chip, sources say", url: "https://www.usnews.com/news/top-news/articles/2026-07-07/exclusive-chinas-deepseek-developing-its-own-ai-chip-sources-say", source: "Reuters / US News", date: "2026-07-07"}
- {id: 4, title: "Kimi K3 Pricing: Moonshot Triples Its Own Rate Card", url: "https://tokencost.app/blog/kimi-k3-pricing", source: "TokenCost", date: "2026-07-24"}
- {id: 5, title: "The Discount Was the Product: Kimi K3 and the End of Cheap Chinese AI", url: "https://paddo.dev/blog/kimi-k3-discount-ends/", source: "paddo.dev", date: "2026-07-24"}
- {id: 6, title: "Kimi K3's Benchmarks and Hallucinations — What That Tells Us About AI Evaluation", url: "https://kili-technology.com/blog/kimi-k3s-benchmarks-and-hallucinations----what-that-tells-us-about-ai-evaluation", source: "Kili Technology", date: "2026-07-24"}
- {id: 7, title: "Kimi K3 Open Weights Drop July 27: Near-Frontier Coding, Undisclosed Hallucination Risk", url: "https://www.techtimes.com/articles/321499/20260724/kimi-k3-open-weights-drop-july-27-near-frontier-coding-undisclosed-hallucination-risk.htm", source: "Tech Times", date: "2026-07-24"}
- {id: 8, title: "China's Moonshot AI releases Kimi K3, the largest open-source model ever", url: "https://venturebeat.com/technology/chinas-moonshot-ai-releases-kimi-k3-the-largest-open-source-model-ever-rivaling-top-u-s-systems", source: "VentureBeat", date: "2026-07-17"}
- {id: 9, title: "Director Michael Kratsios on X — Moonshot AI distillation and GB300 allegation", url: "https://x.com/mkratsios47/status/2079933645888880708", source: "X / Michael Kratsios", date: "2026-07-23"}
- {id: 10, title: "Chinese AI Models Sanctioned? What's Actually Happening", url: "https://vibraniumlabs.ai/blog/chinese-ai-models-sanctioned-whats-actually-happening", source: "Vibranium Labs", date: "2026-07-22"}
- {id: 11, title: "Bessent says U.S. could sanction China over AI model 'theft'", url: "https://www.cnbc.com/2026/07/21/bessent-china-ai-sanctions.html", source: "CNBC", date: "2026-07-21"}
- {id: 12, title: "Moonshot Denies Distilling Fable and Credits K3 Gains to Its Own Architecture", url: "https://www.implicator.ai/moonshot-denies-distilling-fable-and-credits-k3-gains-to-its-own-architecture/", source: "Implicator.ai, citing Asia Times", date: "2026-07-21"}
- {id: 13, title: "Experts say exploiting Anthropic's Fable isn't how Kimi K3 got so good", url: "https://techcrunch.com/2026/07/23/experts-say-exploiting-anthropics-fable-isnt-how-kimi-k3-got-so-good/", source: "TechCrunch", date: "2026-07-23"}
- {id: 14, title: "China defends AI development amid US allegations of Moonshot AI IP theft", url: "https://thehill.com/policy/technology/5986143-china-defends-ai-development/", source: "The Hill", date: "2026-07-23"}
- {id: 15, title: "US accuses China's Moonshot of stealing from Anthropic's Fable for latest AI model", url: "https://cybernews.com/ai-news/us-accuses-china-moonshot-fable-distillation/", source: "Cybernews", date: "2026-07-23"}
- {id: 16, title: "Meta, Microsoft, Palantir, Nvidia and 21 Others Sign Letter Backing Open-Weight AI Models", url: "https://www.benzinga.com/markets/tech/26/07/60673099/meta-microsoft-palantir-nvidia-and-21-others-sign-letter-backing-open-weight-ai-models", source: "Benzinga", date: "2026-07-24"}
- {id: 17, title: "Nvidia and 24 other companies sign open-weights letter as Washington weighs Chinese AI model ban", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-and-24-other-companies-sign-open-weights-letter-as-washington-weighs-chinese-ai-model-ban", source: "Tom's Hardware", date: "2026-07-24"}
- {id: 18, title: "Startup founders urge Trump not to shut off Chinese open-weight AI", url: "https://www.politico.com/news/2026/07/22/startup-founders-urge-trump-not-to-shut-off-chinese-open-weight-ai-01008992", source: "Politico", date: "2026-07-22"}
- {id: 19, title: "Silicon Valley startups fight to keep Chinese AI models Trump wants to restrict", url: "https://northeasttimes.com/2026/07/24/silicon-valley-startups-fight-to-keep-chinese-ai-models-trump-wants-to-restrict/", source: "Northeast Times", date: "2026-07-24"}
- {id: 20, title: "Huawei Ascend 950PR: ByteDance $5.6B Order, CUDA-Compatible, 750K Units in 2026", url: "https://www.abhs.in/blog/huawei-ascend-950pr-bytedance-alibaba-cuda-compatible-nvidia-china-2026", source: "Abhishek Gautam", date: "2026-04-27"}
- {id: 21, title: "CUDA-compatible AI chip: ByteDance $5.6B backs Huawei 950PR", url: "https://aitoolsbee.com/news/cuda-compatible-ai-chip-bytedance-5-6b-backs-huawei-950pr/", source: "AI Tools Bee", date: "2026-04-28"}
- {id: 22, title: "Huawei Ascend production ramp", url: "https://newsletter.semianalysis.com/p/huawei-ascend-production-ramp", source: "SemiAnalysis", date: "2025-09-08"}
- {id: 23, title: "China Weighs Export Controls on AI Models, Including Open Weight LLMs", url: "https://www.implicator.ai/china-considers-adding-ai-model-weights-and-chip-designs-to-export-list/", source: "Implicator.ai, citing FT/Reuters", date: "2026-07-21"}
- {id: 24, title: "China is considering stricter controls on exports of more advanced AI models", url: "https://en.ilsole24ore.com/art/china-is-considering-stricter-controls-on-exports-of-more-advanced-models-AJPV8pQ", source: "Il Sole 24 Ore", date: "2026-07-21"}
- {id: 25, title: "Little Tech Association", url: "https://littletech.org/", source: "Little Tech Association", date: "2026-07-25"}
- {id: 26, title: "No Adversarial AI Act, H.R. 4142", url: "https://www.congress.gov/bill/119th-congress/house-bill/4142/text", source: "Congress.gov", date: "2025-06-25"}
- {id: 27, title: "No Adversarial AI Act, S.2177", url: "https://www.congress.gov/bill/119th-congress/senate-bill/2177/all-info", source: "Congress.gov", date: "2025-06-25"}
- {id: 28, title: "AA-Omniscience: Knowledge and Hallucination Benchmark", url: "https://artificialanalysis.ai/articles/aa-omniscience-knowledge-hallucination-benchmark", source: "Artificial Analysis", date: "2026-07-24"}
- {id: 29, title: "Kimi K3 — Intelligence, Performance & Price Analysis", url: "https://artificialanalysis.ai/models/kimi-k3", source: "Artificial Analysis / OpenRouter listing", date: "2026-07-24"}
- {id: 30, title: "Kimi's open model K3 nears GPT-5.6 Sol and Fable 5 while signaling the end of super cheap Chinese AI", url: "https://the-decoder.com/kimis-open-model-k3-nears-gpt-5-6-sol-and-fable-5-while-signaling-the-end-of-super-cheap-chinese-ai/", source: "The Decoder", date: "2026-07-24"}
- {id: 31, title: "Detecting and preventing distillation attacks", url: "https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks", source: "Anthropic", date: "2026-02"}
:::
