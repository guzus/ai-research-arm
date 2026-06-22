---
eyebrow: ANALYSIS · AI LABS
domain: finance
title: "Noam Shazeer leaves Google for OpenAI: what the reversal of a $2.7B acquihire signals about the talent moat"
deck: Less than two years after Google paid a reported $2.7 billion to bring him back, the Transformer co-author walked to OpenAI. The reversal is a clean experiment on whether money can buy a talent moat — and what the answer means for the structure being used to buy it.
lede: |
  On June 18, 2026, Noam Shazeer — co-author of the 2017 paper that
  invented the Transformer, and at the time Google's VP of Engineering
  and a co-lead of Gemini — posted that he was joining OpenAI. The line
  that makes it a story is the timing: in August 2024 Google had paid a
  reported $2.7 billion to license his startup's technology and bring him
  back. So a roughly $2.7B retention spend did not hold its central asset
  for even two years. That is not just a celebrity transfer. It is a
  natural experiment on the question every AI lab and its investors are
  implicitly betting on — is elite individual talent a durable
  competitive moat, and if so, can it be bought? The evidence says money
  buys the move, not the moat.
stats:
  - {label: Announced, value: "Jun 18, 2026"}
  - {label: Return deal, value: $2.7B, note: "Aug 2024 (reported)"}
  - {label: Time held, value: "<2 yrs"}
  - {label: New role, value: Architecture, note: "research lead (reported)"}
  - {label: GOOGL reaction, value: "~flat", note: "no sell-off"}
---

:::callout(kind=info, label="The short version")
- {accent}It's confirmed.{/} Shazeer announced the move himself; Sam Altman welcomed him publicly, saying it "only took 10 years."[^1,2,3]
- {accent}The role is reported, not self-stated.{/} "Lead for Architecture Research" comes from reporting; Shazeer's own post named no title or start date.[^4,3]
- {accent}The $2.7B was never about one salary.{/} It was a non-exclusive technology license plus a reverse-acquihire of ~30 people, structured so Google acquired no equity.[^5,6]
- {accent}Money buys the move, not the moat.{/} The lab paying the most (OpenAI) had the worst two-year retention of the big three; flows run toward mission and compute, not the highest bid.[^35]
- {accent}The structure that dodged merger review is now under review.{/} The DOJ is probing the Character.AI deal; a March 2026 FTC/DOJ notice names "reverse acquihires" explicitly.[^9,34]
:::

## 01. The move, in his own words

The primary source is a single post. "I'm excited to share that I'll be joining OpenAI and look forward to working with the exceptional team there," Shazeer wrote on June 18, 2026, adding that "it was a difficult decision to move on" and thanking "the amazing team at Google."[^1] Sam Altman answered in kind, calling Shazeer "one of the people I have most wanted to work with since the very beginning of openai" and noting it "only took 10 years."[^2] Google's response was a single graceful line — that it was "grateful for Noam's meaningful contributions to Google over the years."[^3] At the time of departure he was Google's VP of Engineering and a co-lead of Gemini.[^2]

What is *not* in the announcement matters for an analyst trying to size the event. Shazeer's own post named no title and no start date; the now-standard description of his OpenAI job — "Lead for Architecture Research," focused on next-generation model architectures — traces to reporting, not to Shazeer or to an OpenAI press release.[^4,3] So the verifiable core is narrow and solid: a confirmed departure from Google to a direct competitor by a foundational researcher, with the specifics of the new mandate still reported rather than declared.

:::statement(attr="ARA Research")
A roughly $2.7 billion deal brought Shazeer back to Google in August 2024. It did not keep him through the summer of 2026. The interesting question is not why he left — it is what the round trip reveals about what that money actually bought.
:::

Why it matters: the cleanest way to test whether talent is a moat is to watch what happens when someone pays top dollar to lock it down. Google ran that experiment in public, and the result is now in.

## 02. What $2.7 billion actually bought

Start by killing the viral framing. The headline "Google paid $2.7B for one engineer" is wrong in every structural particular. The August 2024 deal was a {accent}non-exclusive license{/} to Character.AI's technology, paired with the return of Shazeer, co-founder Daniel De Freitas, and about 30 of the startup's researchers to Google DeepMind — and Google took {accent}no ownership stake{/}, leaving Character.AI a standalone company.[^5,46] This is a "reverse acquihire": buy the people and a license, not the company.

:::kv
- {term: Headline value, def: "~$2.7B (reported; deal terms were never officially disclosed or SEC-filed)"}
- {term: Instrument, def: "Non-exclusive technology license + talent return"}
- {term: Equity acquired, def: "None — Character.AI remained independent"}
- {term: Talent returned, def: "Shazeer, Daniel De Freitas + ~30 researchers"}
- {term: Investor buyout, def: "~$88/share, ~2.5x the 2023 Series A price"}
- {term: Shazeer's estimated take, def: "~$750M–$1B (an estimate from a reported ~30–40% stake, not a disclosed figure)"}
:::

The money's path tells you what it was for. The cash repriced Character.AI's cap table: existing investors were bought out at roughly $88 a share — about 2.5x the company's 2023 Series A, which had valued it near $1 billion — implying a buyout valuation around $2.5 billion.[^7,8] If the prize had been the *intellectual property*, Google would have taken an exclusive license or simply acquired the asset; you do not need to physically relocate three dozen researchers to use a codebase. If the prize were the *people*, you take the people and license the tech non-exclusively — which is exactly what happened.[^5] The structure is the tell: this was an acquihire wearing a license as a coat.

That reading is reinforced by what the licensed technology demonstrably did *not* do. Across the public record there is no statement — from Google, Shazeer, or any filing — that Character.AI's models improved Gemini.[^19] The named Gemini asset is consistently Shazeer-the-researcher, not Character's roleplay-tuned stack. And the rump company's own behavior corroborates it: within roughly two months Character.AI ==abandoned building its own foundation models== and pivoted to fine-tuning open-source models, reporting "20%+ jumps in time spent" once it did.[^10] A firm that had just sold "valuable model technology" stopped building models — consistent with the *model-builders* having left, not with the *models* having been the durable asset.

The aftermath was not kind to the shell. Character.AI's estimated valuation slid from a ~$2.5B peak to roughly $1B in 2025; leadership turned over twice (general counsel Dominic Perella as interim CEO, then ex-Meta executive Karandeep Anand permanently in June 2025); and the company absorbed the legal liability that the founders left behind.[^11,12] The wrongful-death suit brought by Megan Garcia over her son's suicide — filed October 2024, naming Character.AI and Google — survived a dismissal motion in May 2025 and was settled on undisclosed terms in January 2026; under regulatory pressure the company barred under-18 users from open-ended chat effective November 25, 2025, amputating its highest-engagement cohort.[^13,14,15]

:::slope(left-label="2024 peak", right-label=2025, unit=$B)
| Item | 2024 | 2025 |
|------|------|------|
| Character.AI valuation (est.) | 2.5 | 1.0 |
:::

The honest counterpoint: Character.AI's *engagement-tuning* know-how is genuinely valuable, and "the tech was worthless" overshoots — Google does not itemize Gemini's ingredients, so absence of disclosure is not proof of non-use. But the load-bearing reading survives that caveat: ==the $2.7 billion bought talent and competitive denial, papered as a license.== Why it matters: if the asset was the people, then the relevant question is not whether Google overpaid for code, but whether any price can hold people who do not want to stay.

## 03. The reverse-acquihire playbook

Shazeer's deal was not a one-off; it is the signature transaction structure of the 2024–2026 AI consolidation. The pattern is mechanical: license the startup's IP (usually non-exclusively), hire the founders and key staff, deliberately *do not* acquire the company, and leave a hollowed-out independent shell behind. The point of the structure is that an acquisition triggers Hart-Scott-Rodino premerger review; a license-and-hire, on its face, does not.[^33]

| Deal | Date | Reported value | Structure | Target afterward |
|------|------|----------------|-----------|------------------|
| Microsoft / Inflection | Mar 2024 | ~$650M | $620M license + $30M legal waiver | Independent; pivoted to enterprise[^23] |
| Amazon / Adept | Jun 2024 | ~$330M (reported) | License + founders hired | Independent; refocused on agents[^25] |
| *Google / Character.AI | Aug 2024 | ~$2.7B | Non-exclusive license + ~30 hires | Independent; dropped own models[^5] |
| Amazon / Covariant | Aug 2024 | ~$380M (reported) | License + founders hired | Reduced; independent[^26] |
| Google / Windsurf | Jul 2025 | ~$2.4B | License + top staff; no stake | Hollowed; sold to Cognition[^27] |
| Nvidia / Groq | Dec 2025 | ~$20B (reported) | Non-exclusive license + leaders hired | Independent[^29] |
| Google / Contextual AI | May 2026 | ~$85M | License + 20+ researchers | Independent[^28] |

Two things stand out. First, the cadence and the dollar size are both escalating: from Microsoft's $650M Inflection template in early 2024 to a *reported* ~$20B Nvidia/Groq deal in December 2025, the structure scaled by roughly thirty-fold in under two years.[^23,29] Second, Google ran the play at least three times — Character.AI, Windsurf, and Contextual AI — making it less an opportunistic move than a repeatable corporate-development pattern.[^5,27,28] Reporting on the May 2026 Contextual AI deal said the quiet part out loud: the structure "continues Google's acquihire pattern that avoids review by United States antitrust regulators."[^28]

:::compare
- {role: LOWEST, name: "Google / Contextual AI", value: "~$0.09B"}
- {role: HIGHEST, name: "Nvidia / Groq", value: "~$20B"}
- {role: SUBJECT, name: "Google / Character.AI", value: "~$2.7B"}
:::

A necessary caveat keeps the comparison honest: not every "talent grab" is the same instrument. Meta's ~$14.3B move on Scale AI in June 2025 took a 49% *non-voting equity stake* — a minority investment plus acquihire, not a license — and it carried a unique cost: Scale's biggest customers (Google, OpenAI, Microsoft) pulled back over conflict-of-interest fears once a rival part-owned their data vendor.[^30,48] Lumping Meta/Scale in with the license deals would misrepresent the financial instrument. But the through-line holds across both species: each was engineered to clear the threshold for *automatic* merger control while delivering the substance of an acquisition. Why it matters: when an entire industry converges on one deal structure to move its scarcest input, that structure becomes the place to look for both the strategy and its vulnerabilities.

## 04. The retention math: money buys the move, not the moat

Here is the premise the whole talent war rests on: pay a researcher enough and you lock them in. The Shazeer round trip is the cleanest available disproof. A ~$2.7B-backed deal that, by reported estimates, personally enriched him by something like $750M–$1B did not anchor him to Google's mission for even two years.[^6] He was already, by any definition, permanently wealthy. OpenAI did not need to make him rich; whatever it offered, the marginal dollar was not the lever.

The market-level data confirms the inversion. SignalFire's State of Talent 2025 report measured two-year retention across the frontier labs — and the ranking runs *inverse* to headline compensation.

:::rank-list
- {label: Anthropic, value: 80%, pct: 100}
- {label: Google DeepMind, value: 78%, pct: 98}
- {label: OpenAI, value: 67%, pct: 84, highlight: true}
- {label: Meta, value: 64%, pct: 80}
:::

OpenAI — which paid a reported ~$1.5 million in average *stock-based* compensation per employee in 2025, the highest of any major tech startup on record, and which had built the most aggressive financial handcuff (a two-year sale lock on its profit units) — posted the *worst* two-year retention of the big three at 67%, and bled researchers to Anthropic at roughly 8x the reverse rate.[^35,38] From DeepMind, the flow to Anthropic ran nearly 11:1.[^35] SignalFire attributes Anthropic's edge to factors "beyond salary" — culture, autonomy, mission. The lab that pays most is not the lab that keeps most.

The first-principles mechanism is wealth saturation. Once a researcher clears the "never has to work again" threshold — which elite frontier researchers cross in a single vesting cycle — the marginal utility of the next dollar collapses, while the marginal utility of compute access, research freedom, team density, and mission stays high and undiminished. {accent}You can out-bid a competitor on those dimensions without out-paying them{/} — which is precisely the dimension money cannot defend. Vesting schedules and golden handcuffs are best read not as the solution but as evidence of the problem: you only need to forfeit-engineer equity because paid-out money provably does not hold anyone. Over the prior year the industry escalated to packages it could barely believe — Altman claimed Meta dangled "$100 million signing bonuses" at OpenAI staff; Meta's CTO countered that the figure applied to a handful of senior roles and was not an upfront bonus, and an actual OpenAI-to-Meta hire flatly denied receiving it.[^36,37]

:::callout(kind=warn, label="The honest counter")
Money's retention power is weak, but it is not zero. Thinking Machines co-founder Andrew Tulloch reportedly declined a Meta package worth up to ~$1.5 billion over six years — and then later joined Meta anyway.[^39] A strong "no" that did not durably hold is the most intellectually honest data point in the set: comp is a necessary table-stakes floor with a steep diminishing return, not a binding lock. The defensible conclusion is directional, not absolute.
:::

Why it matters: if retention spend has a short half-life on exactly the people you most want to keep, then "we paid to lock down the talent" is a weaker thesis than the deal sizes imply — and the $2.7B that bought Shazeer back is the proof of concept that it can evaporate.

## 05. Was Shazeer even the moat?

There is a prior question the celebratory coverage skips: was losing Shazeer actually a capability hit to Gemini, or mostly a hit to prestige? The bull case for "this dents Gemini" is real and rests on a genuinely rare pedigree. Shazeer is a co-author of "Attention Is All You Need" (2017), the eight-author paper that introduced the Transformer; first author of the sparsely-gated Mixture-of-Experts paper (2017), the sparsity technique underpinning modern frontier models; and sole author of multi-query attention (2019), a literal inference-efficiency primitive.[^16,17,18] Google revealed its own valuation of him by paying ~$2.7B to bring him back, and Altman says he chased him for a decade.[^2]

But the attribution is weaker than the headline. Gemini's technical leadership was an explicitly *named multi-person set* — Shazeer alongside Jeff Dean and Oriol Vinyals, sitting under Demis Hassabis and Koray Kavukcuoglu — built by hundreds of engineers drawn from Google Brain and DeepMind.[^19,20] Jeff Dean co-authored the Mixture-of-Experts paper too, so even the architecture lineage Shazeer is famous for survives in the building.[^17] The specific media claim that he was "singularly responsible for Gemini closing the gap with ChatGPT" is supported by no primary source; it is a compression of "he co-invented the Transformer."

The base rate is the decisive evidence. {accent}All eight authors of the Transformer paper eventually left Google{/} — and Google still shipped Gemini 2.5 Pro to a #1 debut on LMArena in March 2025.[^16,21] OpenAI lost Ilya Sutskever and three senior leaders inside a single 2024 window and still shipped o1 and, later, GPT-5.[^22] At a compute-, data-, and org-rich incumbent, frontier capability has repeatedly proven robust to the departure of even its most celebrated individuals. Continued shipping proves cadence, not unchanged quality — that is the fair caveat — but the pattern is strong: no single person has been the causal bottleneck.

The market agreed. GOOGL did not sell off on the June 18–19 departures (Shazeer to OpenAI, and Nobel laureate John Jumper to Anthropic a day later); the monthly close trend {sparkline:338,311.76,287.56,384.8,380.34,368.03} shows the stock far above its March low, with June only modestly below May.[^45]

:::line-chart(title="GOOGL didn't flinch", subtitle="Monthly close, USD — Yahoo Finance (as of 2026-06)", y-unit=$)
x: 2026-01,2026-02,2026-03,2026-04,2026-05,2026-06
GOOGL: 338.0,311.76,287.56,384.8,380.34,368.03
:::

Monthly granularity cannot isolate the single-day move, so read this as "no crash," not "no reaction." But a company expecting a capability hit rarely responds with one gracious sentence, and the market rarely yawns.[^3,45] Why it matters: if the moat were any one researcher, $2.7B retention deals and $100M offers would be rational insurance. The base rate says the moat is elsewhere — which makes the spending look more like a status auction than a defense of a defensible asset.

## 06. The structure that dodged review is now under review

The reverse-acquihire's entire appeal is regulatory: a license-and-hire avoids the *automatic* Hart-Scott-Rodino premerger filing that an acquisition would trigger. But "avoided the mandatory filing" is not the same as "escaped scrutiny," and conflating them is the strategy's central misread. Regulators came anyway — after the fact, and with rising appetite.

:::timeline
- {date: 2024-01, headline: "FTC opens 6(b) inquiry", body: "Compulsory orders to Alphabet, Amazon, Anthropic, Microsoft, OpenAI on AI partnerships."}
- {date: 2024-03, headline: "Microsoft / Inflection", body: "The ~$650M template case that defines the structure."}
- {date: 2024-08, headline: "Google / Character.AI", body: "~$2.7B license + reverse-acquihire."}
- {date: 2024-09, headline: "UK CMA clears Inflection", body: "But first deems it a 'relevant merger situation' — jurisdiction asserted."}
- {date: 2025-01, headline: "FTC staff report", body: "Flags risks to compute and engineering-talent access, and switching costs."}
- {date: 2025-05, headline: "DOJ probes Character.AI", body: "Examines whether the deal was structured to avoid merger scrutiny."}
- {date: 2026-03, headline: "FTC/DOJ HSR notice", body: "Explicitly names 'acquihires' and 'reverse acquihires' as deals that eliminate a competitor."}
:::

The escalation is the point. The FTC's January 2024 6(b) study produced a January 2025 staff report warning that these partnerships "may impact access to certain inputs, such as computing resources and engineering talent" and raise switching costs.[^31,32] The UK's CMA cleared Microsoft/Inflection in September 2024 — but only after explicitly finding it *was* a "relevant merger situation" under the Enterprise Act, i.e., that merger control reached it despite the structure.[^24] In May 2025 the DOJ told Google it was examining whether the Character.AI deal specifically was "structured to avoid formal government merger scrutiny."[^9] And in March 2026 a joint FTC/DOJ Request for Information stated the agencies had seen "an uptick in business transactions that parties are not reporting … yet which have the practical effect of eliminating a market participant" — naming "acquihires," "reverse acquihires," and non-exclusive IP licenses outright.[^34] Senators Warren, Wyden, and Blumenthal have pressed both agencies to scrutinize the pattern, naming Inflection, Windsurf, and Nvidia/Groq.[^33]

The counter-case is that scrutiny has produced little: the Character.AI probe is early-stage with no enforcement action, the CMA *cleared* Inflection, and the current FTC leadership has at times blamed prior over-blocking for pushing deals into this structure in the first place.[^9,24,33] So the structure still works *operationally*. But it now carries a tail risk it did not in early 2024 — the deals are individually un-reviewed but collectively flagged, and the legal apparatus to reach them (Clayton §7, Sherman §1) does not depend on an HSR filing. Why it matters: the very feature that makes the reverse-acquihire attractive — invisibility to automatic review — is the feature regulators are now writing rules to remove. Shazeer's deal helped define both the playbook and, via the DOJ probe, its first concrete legal exposure.

## 07. What OpenAI is actually buying

If individual talent is a shaky moat, why does OpenAI want Shazeer badly enough that Altman frames it as a decade-long pursuit? The answer is specific, not sentimental. Shazeer's signature contributions — Mixture-of-Experts sparsity and multi-query/fast attention — are not abstract laurels; they are the levers of {accent}inference economics at scale{/}.[^17,18] Post-GPT-5, the binding constraint on a lab serving hundreds of millions of users is not whether a bigger model exists but whether it can be served cheaply enough. ChatGPT reached 800 million weekly active users by October 2025; every fractional improvement in tokens-per-dollar at that volume is worth more than most acquisitions.[^43] A "Lead for Architecture Research" whose body of work is precisely "how to make attention and routing cheaper" is a targeted hire against OpenAI's largest cost line.

That reframes the move. OpenAI is not buying a moat — it is buying a *specialist* against a concrete bottleneck, at a price (a hire, not a $2.7B deal) far below what Google paid to hold him. The asymmetry is the lesson: the incumbent paid acquisition-scale money to retain him and lost him; the challenger paid recruiting-scale money to take him. If talent were a moat, that asymmetry would be impossible. The most an analyst should claim is that Shazeer's depth is rare enough that his *movements carry signal* — about where the efficiency frontier is heading and which lab is prioritizing it — even when his marginal effect on any one product is modest.

Why it matters: the rational read of OpenAI's move is not "we acquired Google's edge" but "we cheaply hired against our own cost curve." That is a far more defensible use of a star researcher than treating him as a fortress wall.

## 08. What would break this thesis

The thesis here — money buys the move, not the moat; the real moat is compute, data, distribution, and mission — has serious counter-arguments that deserve to be stated, not waved away.

The strongest is revealed preference. Sophisticated buyers acted as if talent *is* the scarce, defensible input: Google paid a reported ~$2.7B for a non-exclusive license whose only coherent justification is the people, and Meta reportedly offered packages up to ~$1.5B to individuals.[^5,39] Markets are not always right, but when the most capital-rich firms on earth repeatedly pay acquisition prices for individuals, "talent is not a moat" has to explain why they are all wrong simultaneously. A second counter: small teams *have* produced outsized breakthroughs — the eight-author Transformer paper is the canonical case — so the "hundreds of engineers" framing can understate how concentrated the genuinely novel ideas are. A third: the base-rate argument (departures rarely break the product) measures *shipping cadence*, which can mask a slower erosion of quality or roadmap ambition that only shows up in a year or two.

:::callout(kind=info, label="Red-team pass")
We asked an adversarial reviewer to falsify the three load-bearing claims — that the deal was a license-not-acquisition, that two-year retention runs counter to headline pay, and that the market shrugged. {accent}All three survived: 3/3 top claims unbroken{/}, with no contradicting primary or secondary source surfaced across 6+ searches. Where the evidence carries nuance it is already marked or counter-argued above (the Tulloch reversal, the monthly-granularity caveat on GOOGL, the early-stage status of the DOJ probe, and that DeepMind pays well yet still ranks second on retention).
:::

The honest synthesis is two-sided. Talent is necessary but not sufficient, and the deal structure proves the asymmetry: an incumbent can spend acquisition money to retain a star and still lose him, while a challenger spends recruiting money to take him. The durable advantages — Alphabet's ~$61B FY2025 R&D, the roughly $725B of combined 2026 hyperscaler capex, Google's ~90% search distribution and OpenAI's 800M-user funnel — are the things money *can* defend because they compound and cannot walk out the door.[^41,42,43,44] As Marc Andreessen put it, "the moat is not the model … it is the product, integration, distribution, and captured value."[^44] Shazeer can carry his expertise to OpenAI. He cannot carry Google's TPUs, its data, or its distribution — and he could not be made to stay by any price.

The final read for the desk: the reversal of the $2.7B acquihire is bearish for "talent as a buyable moat" and bullish for "the moat is the boring, compounding stuff." The talent war is real, expensive, and — on the retention evidence — substantially a status auction. The labs that win will be the ones that treat star hires as specialists against concrete bottlenecks, as OpenAI appears to be doing with Shazeer, rather than as fortress walls that can be purchased and held.

:::references
- {id: 1, title: "Noam Shazeer: 'I'll be joining OpenAI'", url: "https://x.com/NoamShazeer/status/2067400851438932297", source: "X (primary)", date: "2026-06-18"}
- {id: 2, title: "Google Gemini co-lead Noam Shazeer leaves for OpenAI", url: "https://www.cnbc.com/2026/06/18/google-gemini-co-lead-noam-shazeer-leaves-for-openai.html", source: CNBC, date: "2026-06-18"}
- {id: 3, title: "Gemini's co-lead is leaving Google to join OpenAI", url: "https://9to5google.com/2026/06/17/geminis-co-lead-is-leaving-google-to-join-openai/", source: 9to5Google, date: "2026-06-17"}
- {id: 4, title: "OpenAI hires Transformer co-inventor Noam Shazeer away from Google DeepMind", url: "https://mlq.ai/news/openai-hires-transformer-co-inventor-noam-shazeer-away-from-google-deepmind/", source: "MLQ News", date: "2026-06-18"}
- {id: 5, title: "Character.AI CEO Noam Shazeer returns to Google", url: "https://techcrunch.com/2024/08/02/character-ai-ceo-noam-shazeer-returns-to-google/", source: TechCrunch, date: "2024-08-02"}
- {id: 6, title: "Two years after a $2.7B return, Noam Shazeer is leaving for OpenAI", url: "https://www.calcalistech.com/ctechnews/article/sy06wllflg", source: "Calcalist / CTech", date: "2025-05-25"}
- {id: 7, title: "On the Google–Character.AI deal", url: "https://spyglass.org/google-character-ai-deal/", source: "Spyglass (M.G. Siegler)", date: "2024-08-05"}
- {id: 8, title: "Character.AI co-founders hired by Google in licensing deal", url: "https://finance.yahoo.com/news/character-ai-co-founders-hired-233448298.html", source: "Yahoo Finance / Bloomberg", date: "2024-08-02"}
- {id: 9, title: "Google faces DOJ antitrust investigation over Character.AI deal", url: "https://fortune.com/2025/05/22/google-antitrust-investigation-character-ai-chatbot-doj/", source: Fortune, date: "2025-05-22"}
- {id: 10, title: "Our open-source models are a lot of fun", url: "https://blog.character.ai/breaking-news-our-open-source-models-are-a-lot-of-fun/", source: "Character.AI blog (primary)", date: "2024-10-01"}
- {id: 11, title: "Character.AI company profile", url: "https://sacra.com/c/character-ai/", source: Sacra, date: "2025-12-31"}
- {id: 12, title: "Character.AI taps Meta's former VP as CEO", url: "https://techcrunch.com/2025/06/20/character-ai-taps-metas-former-vp-of-business-products-as-ceo/", source: TechCrunch, date: "2025-06-20"}
- {id: 13, title: "US judge rejects AI free-speech claim in teen chatbot death suit", url: "https://www.euronews.com/next/2025/05/22/us-judge-rejects-claims-made-in-teen-chatbot-death-lawsuit-that-ai-has-free-speech-rights", source: Euronews, date: "2025-05-22"}
- {id: 14, title: "Google, Character.AI to settle Florida teen suicide lawsuit", url: "https://www.cbsnews.com/news/google-settle-lawsuit-florida-teens-suicide-character-ai-chatbot/", source: "CBS News", date: "2026-01-07"}
- {id: 15, title: "Character.AI to ban under-18 open-ended chat", url: "https://fortune.com/2025/10/29/character-ai-ban-children-teens-chatbots-regulatory-pressure-age-verification-online-harms/", source: Fortune, date: "2025-10-29"}
- {id: 16, title: "Attention Is All You Need", url: "https://arxiv.org/abs/1706.03762", source: "arXiv (primary)", date: "2017-06-12"}
- {id: 17, title: "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer", url: "https://arxiv.org/abs/1701.06538", source: "arXiv (primary)", date: "2017-01-23"}
- {id: 18, title: "Fast Transformer Decoding: One Write-Head Is All You Need (multi-query attention)", url: "https://arxiv.org/abs/1911.02150", source: "arXiv (primary)", date: "2019-11-06"}
- {id: 19, title: "Noam Shazeer", url: "https://en.wikipedia.org/wiki/Noam_Shazeer", source: Wikipedia, date: "2026-06-22"}
- {id: 20, title: "Gemini (language model)", url: "https://en.wikipedia.org/wiki/Gemini_(language_model)", source: Wikipedia, date: "2026-06-22"}
- {id: 21, title: "Gemini 2.5: our most intelligent model", url: "https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/", source: "Google DeepMind (primary)", date: "2025-03-25"}
- {id: 22, title: "OpenAI's chief research officer has left", url: "https://techcrunch.com/2024/09/25/openais-chief-research-officer-has-left/", source: TechCrunch, date: "2024-09-25"}
- {id: 23, title: "Microsoft pays Inflection AI $650 million, hires most of its staff", url: "https://www.deeplearning.ai/the-batch/microsoft-pays-inflection-ai-650-million-hires-most-of-its-staff/", source: "DeepLearning.AI (The Batch)", date: "2024-03-27"}
- {id: 24, title: "Microsoft / Inflection AI inquiry", url: "https://www.gov.uk/cma-cases/microsoft-slash-inflection-ai-inquiry", source: "UK CMA (primary)", date: "2024-09-04"}
- {id: 25, title: "Amazon hires founders away from AI startup Adept", url: "https://techcrunch.com/2024/06/28/amazon-hires-founders-away-from-ai-startup-adept/", source: TechCrunch, date: "2024-06-28"}
- {id: 26, title: "Amazon hires the founders of robotics AI startup Covariant", url: "https://techcrunch.com/2024/08/31/amazon-hires-the-founders-of-robotics-ai-startup-covariant/", source: TechCrunch, date: "2024-08-31"}
- {id: 27, title: "Windsurf's CEO goes to Google; OpenAI's acquisition falls apart", url: "https://techcrunch.com/2025/07/11/windsurfs-ceo-goes-to-google-openais-acquisition-falls-apart/", source: TechCrunch, date: "2025-07-11"}
- {id: 28, title: "Google DeepMind hires Contextual AI talent amid antitrust scrutiny", url: "https://www.benzinga.com/markets/tech/26/05/52681185/google-deepmind-contextual-ai-talent-antitrust-scrutiny", source: Benzinga, date: "2026-05-19"}
- {id: 29, title: "Nvidia to license Groq technology, hire executives (~$20B)", url: "https://www.cnbc.com/2025/12/24/nvidia-buying-ai-chip-startup-groq-for-about-20-billion-biggest-deal.html", source: CNBC, date: "2025-12-24"}
- {id: 30, title: "Scale AI founder Wang exits for Meta in $14B deal", url: "https://www.cnbc.com/2025/06/12/scale-ai-founder-wang-announces-exit-for-meta-part-of-14-billion-deal.html", source: CNBC, date: "2025-06-12"}
- {id: 31, title: "FTC launches inquiry into generative AI investments and partnerships", url: "https://www.ftc.gov/news-events/news/press-releases/2024/01/ftc-launches-inquiry-generative-ai-investments-partnerships", source: "FTC (primary)", date: "2024-01-25"}
- {id: 32, title: "FTC issues staff report on AI partnerships and investments", url: "https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-issues-staff-report-ai-partnerships-investments-study", source: "FTC (primary)", date: "2025-01-17"}
- {id: 33, title: "FTC eyeing acquihire transactions in tech", url: "https://www.wilmerhale.com/en/insights/client-alerts/20260129-ftc-eyeing-acquihire-transactions-in-tech-industry", source: WilmerHale, date: "2026-01-29"}
- {id: 34, title: "Joint FTC/DOJ HSR Request for Information", url: "https://www.ftc.gov/system/files/ftc_gov/pdf/2026.03.25-HSR-RFI.pdf", source: "FTC/DOJ (primary)", date: "2026-03-25"}
- {id: 35, title: "SignalFire State of Talent Report 2025", url: "https://www.signalfire.com/blog/signalfire-state-of-talent-report-2025", source: "SignalFire (primary)", date: "2025-05-20"}
- {id: 36, title: "Sam Altman says Meta tried to poach OpenAI staff with $100M bonuses", url: "https://www.cnbc.com/2025/06/18/sam-altman-says-meta-tried-to-poach-openai-staff-with-100-million-bonuses-mark-zuckerberg.html", source: CNBC, date: "2025-06-18"}
- {id: 37, title: "Meta is offering multimillion-dollar pay — but not $100M signing bonuses", url: "https://techcrunch.com/2025/06/27/meta-is-offering-multimillion-dollar-pay-for-ai-researchers-but-not-100m-signing-bonuses/", source: TechCrunch, date: "2025-06-27"}
- {id: 38, title: "OpenAI's record million-dollar equity compensation", url: "https://fortune.com/2026/02/18/openai-chatgpt-creator-record-million-dollar-equity-compensation-ai-tech-talent-war-career-retention-sam-altman-millionaire-staff/", source: Fortune, date: "2026-02-18"}
- {id: 39, title: "AI researcher declines ~$1B Meta offer", url: "https://futurism.com/ai-researcher-declines-1-billion-offer-meta-mark-zuckerberg", source: Futurism, date: "2025-08-06"}
- {id: 40, title: "Altman 'missionaries vs mercenaries' memo (Wired)", url: "https://www.techmeme.com/250701/p19", source: "Techmeme / Wired", date: "2025-07-01"}
- {id: 41, title: "Alphabet research & development expenses", url: "https://www.macrotrends.net/stocks/charts/GOOGL/alphabet/research-development-expenses", source: "Macrotrends (from 10-K)", date: "2026-02-01"}
- {id: 42, title: "Big Tech's AI spending plans reach $725 billion", url: "https://www.tomshardware.com/tech-industry/big-tech/big-techs-ai-spending-plans-reach-725-billion", source: "Tom's Hardware", date: "2026-02-01"}
- {id: 43, title: "Sam Altman says ChatGPT has hit 800M weekly active users", url: "https://techcrunch.com/2025/10/06/sam-altman-says-chatgpt-has-hit-800m-weekly-active-users/", source: TechCrunch, date: "2025-10-06"}
- {id: 44, title: "Marc Andreessen: the AI moat is not the model", url: "https://www.the-ai-corner.com/p/marc-andreessen-ai-moat-not-the-model-2026", source: "The AI Corner", date: "2026-01-15"}
- {id: 45, title: "GOOGL price history", url: "https://finance.yahoo.com/quote/GOOGL", source: "Yahoo Finance", date: "2026-06-30"}
- {id: 46, title: "Ex-Google engineers from Character.AI re-join with AI partnership", url: "https://www.cnbc.com/2024/08/02/ex-google-engineers-from-characterai-re-join-company-with-ai-partnership-.html", source: CNBC, date: "2024-08-02"}
- {id: 47, title: "Alphabet Q1 2026 earnings call transcript", url: "https://www.investing.com/news/transcripts/earnings-call-transcript-alphabet-q1-2026-earnings-beat-expectations-93CH-4654863", source: "Investing.com", date: "2026-05-03"}
- {id: 48, title: "Google, Scale AI's largest customer, plans split after Meta deal", url: "https://www.cnbc.com/2025/06/14/google-scale-ais-largest-customer-plans-split-after-meta-deal.html", source: CNBC, date: "2025-06-14"}
:::
