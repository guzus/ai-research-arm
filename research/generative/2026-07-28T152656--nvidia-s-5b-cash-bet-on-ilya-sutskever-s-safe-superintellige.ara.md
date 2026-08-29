---
eyebrow: REPORT · AI VENTURE FINANCE
title: NVIDIA's $5 Billion Bet on a Lab With Nothing to Show
deck: Safe Superintelligence has shipped zero public products since its June 2024 founding. NVIDIA just handed it a compute upgrade of unconfirmed size anyway — here is what the deal actually proves, and what it doesn't.
lede: |
  On July 27, 2026, NVIDIA and Ilya Sutskever's Safe Superintelligence Inc. announced a "long-term strategic partnership" that press reports pegged at $5 billion. Neither company confirmed a number. What is confirmed is narrower and more interesting: a repeat investor is buying — or renting — an unproven lab's most scarce resource, more compute, on terms nobody outside the two companies has actually seen. This piece traces the deal, corrects a factual error in the premise that prompted it (SSI was founded in 2024, not 2023), and stress-tests every claim that made this into a $32 billion story.
stats:
  - {label: Reported deal size, value: $5B, note: Bloomberg/Reuters-sourced}
  - {label: SSI valuation, value: $32B, note: unchanged since Apr 2025}
  - {label: SSI founded, value: "Jun 2024"}
  - {label: Public products shipped, value: 0}
domain: finance
---

:::kv
- {term: "What happened", def: "NVIDIA committed to a large investment in Safe Superintelligence (SSI), announced July 27, 2026, alongside access to NVIDIA's next-generation Vera Rubin platform"}
- {term: "How much", def: "Reported at $5B by Bloomberg and independently corroborated by Reuters — neither company has confirmed a number"}
- {term: "SSI's valuation", def: "$32B, unchanged from an April 2025 round, per all available reporting"}
- {term: "What SSI has shipped publicly", def: "Zero papers, products, patents, or code since its June 2024 founding — a premise correction from the 2023 figure commonly cited"}
- {term: "Why it matters", def: "It is the purest live test of whether a frontier AI lab's valuation requires a product at all"}
:::

## 01. The Deal: What NVIDIA Actually Committed

On July 27, 2026, NVIDIA and Safe Superintelligence announced what both companies called a "long-term strategic partnership" — and what most headlines instantly priced at $5 billion, even though neither company has confirmed that number.

Start with what is actually on the record. NVIDIA's own newsroom post says only that "NVIDIA has additionally made an investment in SSI" — no dollar figure, no equity percentage, no term sheet detail [^1]. The joint release carried by GlobeNewswire adds texture but still no number: Ilya Sutskever, SSI's CEO, is quoted saying "NVIDIA is making a substantial investment in SSI that will let us 10x our compute in the next 12 months," and that "we are confident that our big bet on the Vera Rubin platform will take us to the next level" [^2]. Jensen Huang's line in the same release frames the bet as a bet on the man, not a product: "Ilya has pioneered fundamental breakthroughs at the foundation of modern AI, beginning with AlexNet... We are excited to see what new breakthroughs SSI will discover powered by our Vera Rubin platform" [^1] [^2]. Compute access and a founder's credibility are confirmed. A price tag is not.

:::quote(attr="Ilya Sutskever, CEO, Safe Superintelligence")
NVIDIA is making a substantial investment in SSI that will let us 10x our compute in the next 12 months. We have research that is worthy of scaling up, and having access to a big NVIDIA computer will let us do so... we are confident that our big bet on the Vera Rubin platform will take us to the next level.
:::

The $5 billion figure has a traceable origin, and it matters that readers can trace it. Bloomberg published it first, sourced to "people familiar with the matter" — not a filing, not a company statement [^3]. Reuters, via Investing.com, then corroborated the same $5 billion independently through a separate unnamed source, adding a structural detail Bloomberg didn't specify: the deal is described as an "equity investment" paired with Vera Rubin hardware access, meaning the number — if accurate — is likely a blend of a cash-for-stake purchase and a separate compute-access grant, not a single lump-sum check [^4]. Two independent sourcing chains landing on the same figure is meaningfully stronger than one, but it is still not company confirmation. TechCrunch, reporting the same day, hedges further, with a source describing the investment only as one that "stretches into multiple billions" — directionally consistent with $5 billion but explicitly softer on precision [^5]. Treat $5 billion as the market's best current estimate, not an audited fact.

:::stats
- {label: Reported deal size, value: "$5B", note: "Bloomberg/Reuters-sourced, not company-confirmed"}
- {label: Compute increase claimed, value: "10x", unit: "in 12 mo."}
- {label: Officially disclosed terms, value: "None"}
- {label: Prior NVIDIA stake in SSI, value: "Yes", note: "since ~2025"}
:::

:::quote(attr="Jensen Huang, CEO, NVIDIA")
Ilya has pioneered fundamental breakthroughs at the foundation of modern AI, beginning with AlexNet... We are excited to see what new breakthroughs SSI will discover powered by our Vera Rubin platform.
:::

A second fact gets buried under the "$5B" headline treatment: this is not NVIDIA's first bet on SSI. TechCrunch notes NVIDIA was already an investor via SSI's 2025 round, reported at roughly $2 billion raised against a $32 billion valuation [^5][^13]. That reframes the July 27 announcement — it is an *escalation* of an existing position, made by an investor who already had a year-plus of diligence exposure to SSI, not a cold first-look bet on an unproven lab. SiliconANGLE's framing supports this reading: NVIDIA "secured 'rare access into the company's closely guarded research'" as part of the process [^8], language consistent with a follow-on investor deepening a relationship rather than a new entrant doing first-time diligence from scratch.

One structural question the coverage leaves open, and which Section 06 examines in depth: whether the Vera Rubin hardware supplements or replaces SSI's existing Google TPU infrastructure. Some outlets frame this as a wholesale pivot away from TPUs [^6], but Neowin is more precise: "SSI hasn't said whether the Vera Rubin systems will replace [Google TPU] infrastructure or simply run alongside it" [^7] — the "shift" framing in headlines is not the same as confirmed exclusivity.

What would change this analysis: if a future SEC filing or an on-record statement from either company confirms $5 billion exactly — or reveals a materially different number — the sourcing-uncertainty framing above needs direct revision, and the "reported, not confirmed" caveat retires. Until then, a lab that has shipped no product is about to get a hardware upgrade of unclear size and structure — which is exactly why the number is worth scrutinizing before it's treated as settled fact.

## 02. SSI's Valuation Ladder

In under two years, Safe Superintelligence's valuation climbed from $5B to a reported $32B — and the July 2026 NVIDIA deal, still unpriced in any public disclosure, may not have moved that number at all.

SSI's price history is short and sharply punctuated. Roughly three months after its June 2024 founding, the company raised a $1B seed round at a $5B post-money valuation, backed by SV Angel, DST Global, Sequoia Capital, and Andreessen Horowitz [^9]. By February 2025, reporting placed SSI "close to raising roughly $1B" in a follow-on round [^11] — context for what actually closed two months later: an approximately $2B raise at a $32B valuation, led by Greenoaks Capital alongside Andreessen Horowitz, DST Global, and Lightspeed Venture Partners [^10]. Crucially, that April 2025 round was never announced by SSI itself — it was first reported by the Financial Times, and SSI "did not comment on the new funding" [^10]. Every valuation figure attached to this company, including the $32B mark still being quoted fourteen months later, traces back to press reporting rather than a company statement.

:::line-chart(title="SSI reported valuation", subtitle="$ billion, by funding round", y-unit=$)
x: 2024-09,2025-04,2026-07
SSI: 5,32,32
:::

The flat line between 2025 and 2026 is a statement about disclosure, not price. No new valuation accompanied the ~$5B NVIDIA commitment reported in July 2026 [^3,4] — press coverage simply continues to cite the same $32B figure set fourteen months earlier. Read plainly, that means the July 2026 investment is best understood as carried at (or near) the prior mark, not as confirmed evidence of a fresh up-round.

| Round | Date | Amount | Valuation | Lead investor(s) |
|---|---|---|---|---|
| Seed | Sept 2024 | $1B | $5B | SV Angel / DST Global / Sequoia / a16z |
| Series | Apr 2025 | ~$2B | $32B | Greenoaks Capital |
| NVIDIA tranche | Jul 2026 | ~$5B (reported) | $32B (unchanged, per reporting) | NVIDIA |

Two details complicate the tidy version of this ladder. First, the popular "total raised" figures circulating for SSI — $6B, $7B — do not reconcile against any confirmed set of rounds. CB Insights' company profile tracks only $3B in disclosed equity ($1B seed plus the $2B 2025 round) [^12]; adding the ~$5B NVIDIA tranche gets to roughly $8B, not $6B or $7B. Those intermediate aggregates appear to be unreconciled press estimates, not verified sums. Second, and more consequential for the valuation-math question specifically: NVIDIA was not a new name in SSI's cap table when the July 2026 deal was reported. Reuters' coverage of the April 2025 round confirms that both Alphabet/Google and NVIDIA participated in that $32B raise [^13] — meaning NVIDIA had already been an SSI shareholder for well over a year before committing another ~$5B. Existing shareholders adding capital without a disclosed new valuation is consistent with a continuation of the 2025 mark — it is not, by itself, proof of a materially higher one.

The honest counterpoint is that we cannot rule out a re-rating either way. If the July 2026 tranche in fact priced SSI at a materially higher mark than $32B, as TechCrunch's softer "multiple billions" language hints it could be, the flat line on the chart above understates the real re-rating [^5]. But SSI's pattern of total non-disclosure — no press release for the seed, no comment on the 2025 round, silence again in 2026 — means neither the bull case (a quiet up-round) nor the bear case (a flat continuation) can be verified from the public record.

This matters because a company with zero shipped product and zero revenue disclosure is nonetheless being priced — and re-priced, or not — entirely through the inferences of outside reporters, which means the $32B figure anchoring every downstream comparison in this piece is substantially softer than its ubiquity in press coverage suggests.

## 03. The Zero-Product Premise, Stress-Tested

A targeted research audit — not just the recycled "no product" line — finds zero papers, zero patents, zero public code, and zero published safety methodology from Safe Superintelligence Inc. across the entirety of its existence, a stronger and more falsifiable claim than the popular shorthand implies.

:::callout(kind=warn, label="Premise correction")
SSI was founded in June 2024 — not 2023 [^15] — a detail worth correcting since it changes the company's age at deal time from roughly three years to about 25 months. "Zero shipped models since 2023" should read "zero shipped models across the company's full ~25-month existence."
:::

Start from the founding document itself. At its June 19, 2024 public launch, SSI stated its mission in one sentence: "We will pursue safe superintelligence in a straight shot, with one focus, one goal, and one product," adding that "our singular focus means no distraction by management overhead or product cycles" [^15]. That framing was always an explicit bet against the normal cadence of AI labs — no intermediate releases, by design — so the audit below should be read against that stated intent, not as a surprise discovery.

The paper trail matches the "one product" framing almost too literally: there isn't one. A targeted search across arXiv, Google Scholar, and Semantic Scholar turns up zero papers carrying an SSI affiliation for Ilya Sutskever or any co-founder since founding. There are zero public GitHub repositories under an SSI account. On the IP side, the only filing found is a pending trademark on the "SSI" mark itself, filed 2025-05-15 — brand protection, not an invention disclosure — and zero patents. Safety methodology, the company's namesake concern, fares no better: SSI's entire public safety commitment is a single paragraph on ssi.inc stating it will "approach safety and capabilities in tandem... advance capabilities as fast as possible while making sure our safety always [remains ahead]... so we can scale in peace," with no attached metrics, red-team results, or governance framework [^21]. The site's "Updates" section has carried exactly three posts since September 2024 — a funding round, a leadership change, and the NVIDIA compute deal — zero of them a research post [^21]. Anthropic (Responsible Scaling Policy), OpenAI (Preparedness Framework), and DeepMind (Frontier Safety Framework) have each published a formal, versioned safety framework; SSI, despite putting "safety" in its name, has published none [^21].

:::stats
- {label: "Papers published (SSI-affiliated)", value: "0"}
- {label: "Public code repositories", value: "0"}
- {label: "Patents filed", value: "0", note: "1 pending trademark only"}
- {label: "Published safety framework", value: "None", note: "vs. Anthropic/OpenAI/DeepMind, which each have one"}
:::

Even NVIDIA's own announcement doesn't close the gap. NVIDIA's framing of the deal claims SSI "has achieved significant research milestones" [^5], and the NVIDIA Newsroom release carries the same deal terms with no accompanying technical disclosure [^1] — neither attaches a paper, benchmark, model weight, or demo to substantiate the claim. The sharpest outside framing of this gap: "For two years, Safe Superintelligence Inc. said practically nothing — no model, no product, no demo, no revenue, just a website with a manifesto and a $32 billion valuation" [^47].

The closest thing to a technical disclosure is Sutskever's own words, and it deserves real nuance rather than a one-sided reading. On the Dwarkesh Patel podcast, Sutskever argued that large language models "generalize dramatically worse than people" and that pre-training "overshot the target" rather than under-delivering — a substantive, falsifiable claim about where the field's returns have gone, not empty PR [^20]. Asked directly what makes SSI's approach different, though, he answered only that "we live in a world where not all machine learning ideas are discussed freely, and this is one of them" [^20] — an assertion of differentiation offered with zero technical content behind it. Pressed on timeline ("5 to 20 years?"), he answered "I think like 5 to 20" [^20] — vague, but a genuine hedge rather than a marketing number.

:::quote(attr="Ilya Sutskever, Dwarkesh Patel podcast, Nov 2025")
We live in a world where not all machine learning ideas are discussed freely, and this is one of them.
:::

The audit's own limits matter as a counterpoint: a lab genuinely pursuing a multi-year, pre-paradigm research bet should look quiet from the outside almost by construction — zero papers, zero repos, and no safety framework are also what a legitimately careful, pre-product effort looks like before it has anything worth disclosing. Silence is consistent with both "there is nothing here" and "the team is deliberately avoiding premature disclosure," and a desk audit of public artifacts cannot distinguish the two [^20]. What the audit *can* establish, and what the NVIDIA deal does nothing to resolve, is that every remaining public signal is unverifiable by outside researchers — precisely the gap a $32B valuation is being asked to fill without evidence [^5],[^47].

## 04. Founders in Flux

SSI's leadership has been unstable since its first day: the man who is now its CEO co-founded the company five weeks after a public, regretted attempt to remove a rival lab's chief executive, and the firm's original co-founder and first CEO left for Meta a little over a year later, in the immediate wake of a rejected acquisition bid.

The chain starts at OpenAI. On November 17, 2023, Ilya Sutskever joined the OpenAI board's vote to remove Sam Altman as CEO; the board's official statement said Altman "was not consistently candid in his communications with the board, hindering its ability to exercise its responsibilities" [^25]. The reaction was immediate and severe: within three days, more than 700 of OpenAI's roughly 770 staff signed an open letter threatening to resign and follow Altman to Microsoft, where Satya Nadella announced Altman and Greg Brockman "will be joining Microsoft to lead a new advanced AI research team" [^26]. Sutskever reversed course publicly the same day.

:::quote(attr="Ilya Sutskever, X post, Nov 20 2023")
I deeply regret my participation in the board's actions. I never intended to harm OpenAI. I love everything we've built together and I will do everything I can to reunite the company.
:::

Sutskever's regret was public and immediate [^22]. The reversal didn't save his board seat. On November 22, OpenAI reinstated Altman as CEO under a reconstituted board — Bret Taylor as chair, joined by Larry Summers and Adam D'Angelo — and confirmed Sutskever "will no longer serve on the board" [^27]. Nearly six months after that, on May 14, 2024, Sutskever announced he was leaving OpenAI outright, writing that he was "excited for what comes next — a project that is very personally meaningful to me about which I will share details in due time," without naming it [^24][^23]. The project surfaced five weeks later: on June 19, 2024, he publicly launched Safe Superintelligence Inc. [^15].

:::timeline
- {date: "2023-11-17", headline: "Board votes to remove Altman", body: "Sutskever joins the OpenAI board vote to fire Sam Altman as CEO."}
- {date: "2023-11-20", headline: "Staff revolt, Sutskever's regret", body: "Over 700 staff threaten to quit for Microsoft; Sutskever publicly regrets his vote the same day."}
- {date: "2023-11-22", headline: "Altman reinstated, Sutskever off the board", body: "OpenAI reconstitutes its board without Sutskever as Altman returns as CEO."}
- {date: "2024-05-14", headline: "Sutskever leaves OpenAI", body: "He announces departure, citing a personally meaningful project still unnamed."}
- {date: "2024-06-19", headline: "SSI launches", body: "Sutskever unveils Safe Superintelligence Inc. five weeks after leaving OpenAI."}
- {date: "2025-06-19", headline: "Meta's rejected bids", body: "Meta reportedly tries to acquire SSI outright and separately tries to hire Sutskever directly; both rebuffed."}
- {date: "2025-06-29", headline: "Gross departs for Meta", body: "Co-founder Daniel Gross leaves SSI for Meta Superintelligence Labs; Sutskever becomes CEO."}
- {date: "2025-10", headline: "Premeditation revealed", body: "Sutskever testifies he considered removing Altman for over a year before the 2023 vote."}
:::

A deposition unsealed roughly two years later adds weight to how that "regret" should be read: in October 2025 testimony in *Musk v. OpenAI*, Sutskever said he had considered removing Altman for "at least a year" before the vote and had authored an internal memo accusing him of "a consistent pattern of lying" [^28]. That doesn't overturn the public apology, but it recasts the November 20 statement as a retreat from a long-considered position rather than a snap reaction.

A second, separate instability arrived at SSI itself almost exactly a year after launch. Reporting from June 19, 2025 describes Meta attempting to acquire all of SSI outright, and — when that failed — trying to hire Sutskever directly; both approaches were rebuffed [^18]. Sutskever's on-record response downplayed the episode: "We are flattered by their attention but are focused on seeing our work through. We have the compute, we have the team, and we know what to do," with the rejected offer reportedly pegged near SSI's then-$32B valuation [^19]. Ten days later, on June 29, 2025, Meta instead hired SSI co-founder Daniel Gross, who departed for Meta Superintelligence Labs; Sutskever's internal note called Gross's time at SSI "winding down" and said he was "grateful for his early contributions" — phrasing notably cooler and more formal than a typical warm founder send-off — and Sutskever assumed the CEO role in the aftermath [^17].

That sequence — a rejected buyout, a rejected direct hire, then a successful hire of the company's other founder — is suggestive, not conclusive. No named source has stated Gross left because of dissatisfaction with SSI, and the "winding down" phrasing is at most a tonal signal, not a documented account of why he went.

There is also a real counterpoint. Founders leaving high-profile roles to start narrower, more focused ventures — or moving on to another major lab — is common across the industry and isn't inherently a red flag. Gross didn't disappear into obscurity; he went on to lead superintelligence research at one of the best-resourced labs in the world, which cuts against reading his exit as a "failure" signal for either him or SSI.

Why it matters: a research organization valued at $32B on zero revenue is, functionally, a bet on one person's judgment and credibility holding steady over a decade-plus AGI timeline. A lab this concentrated in a single founder — one whose board history includes both a reversed vote to fire a peer CEO and, a year later, losing his own co-founder to that peer's biggest competitor — is a single-point-of-failure bet for any investor writing a check against the founder rather than the product.

## 05. NVIDIA's Circular-Financing Playbook

By the time SSI's $5 billion appeared on NVIDIA's books, it was not a bespoke event — it was the fifth entry in a single year's ledger. NVIDIA had already committed more than $40 billion to AI-startup equity in 2026 alone by early May, with PitchBook separately counting a broader ~$53 billion across some 170 deals [^33]. The pattern is what deserves scrutiny more than any single check: a chipmaker financing the very customers whose demand is cited as evidence of a durable AI boom.

:::bar-chart(title="NVIDIA's disclosed 2026 AI-startup commitments", subtitle="$ billion, selected deals", orientation=horizontal, value-unit=$, value-suffix=B)
categories: OpenAI, xAI, CoreWeave, Mistral, SSI
Committed: 30, 2, 2, 2, 5
:::

The OpenAI bar is worth reading carefully, because it is itself a lesson in how fast these numbers move. In September 2025, NVIDIA framed a headline $100 billion pledge to OpenAI; five months later Jensen Huang was already walking the framing back: "It was never a commitment" [^30]. What actually closed, inside OpenAI's larger $122 billion round in March 2026, was a direct equity stake of roughly $30 billion — with no gigawatt-deployment conditionality attached, unlike the original framing [^31]. The lesson for SSI's own $5 billion: a first number attached to a young lab has, in NVIDIA's own recent history, moved substantially before the ink fully dried.

The skepticism sharpened on the very day the SSI deal broke. Bloomberg reported NVIDIA was separately discussing guaranteeing up to $250 billion of OpenAI's data-center lease debt in Ohio, prompting an investment strategist to note that "Nvidia guaranteeing more of OpenAI's data center debt deepens vendor financing that's already under scrutiny" [^29]. Jim Cramer, invoking the dot-com collapse the same day — "I lived through 2000... I don't want the sequel" — still called NVIDIA "an exceptionally strong company," which is the useful nuance: the concern is the financing structure of the ecosystem, not a verdict on NVIDIA's own fundamentals [^29]. A Wedbush analyst landed in between, allowing that the investments fit "squarely into the circular investment theme" while arguing they could "create a competitive moat if Nvidia executes" [^29] — the bull and bear case sitting inside the same sentence.

NVIDIA's own rebuttal is quantified, not just rhetorical, and it predates SSI by several months. Responding directly to circular-financing critiques that had invoked Enron-style comparisons in broader AI-bubble commentary (Michael Burry's own public critique reportedly favored a different historical analogy), the company sent Wall Street analysts a seven-page memo putting strategic investments at $3.7 billion in a single quarter — about 7% of that quarter's revenue [^32]. That is NVIDIA's own self-reported figure, not an independent audit, and it excludes larger off-balance-sheet exposure like the OpenAI lease-guarantee talks [^29][^32]. Scaled against the underlying business, the number is genuinely modest: Q1 FY2027 revenue ran $81.6 billion, with $58.3 billion in GAAP net income and $50.3 billion of operating cash flow [^34].

:::stats
- {label: "Strategic investments, one quarter", value: "$3.7B", note: "~7% of quarterly revenue, per NVIDIA's own memo"}
- {label: "Non-marketable equity securities balance", value: "$22.25B", note: "up from $3.39B a year earlier"}
- {label: "Q1 FY2027 revenue", value: "$81.6B"}
- {label: "Q1 FY2027 operating cash flow", value: "$50.3B"}
:::

What has moved since that memo is the balance, not the flow. NVIDIA's 10-Q shows cumulative gross unrealized gains on its non-marketable equity book of $5.3 billion as of April 26, 2026, against just $396 million a year earlier, and secondary reporting puts the carrying-value balance itself at roughly $22.25 billion — up from $3.39 billion twelve months prior, a roughly 6x jump in one year [^33][^35]. A 7%-of-revenue quarterly flow is easy to wave away; a balance sheet position compounding sixfold in a year is the number that keeps the "vendor financing" critique alive even when NVIDIA's own math checks out.

:::quote(attr="Jensen Huang, CEO, NVIDIA")
It was never a commitment.
:::

Where does SSI itself sit in this? Less exposed to the strict version of the critique than the chart implies. The circularity argument bites hardest when the mechanism is direct — NVIDIA equity funding a lab whose next move is an NVIDIA chip order, as with OpenAI's own compute-and-investment loop. SSI's compute was previously TPU-based, not NVIDIA GPUs, a materially different starting point (the mechanics of that pivot are Section 06's subject). So SSI's $5 billion belongs on the chart as part of the aggregate pattern NVIDIA is building — but as the weakest single case for a strict, closed-loop financing accusation, since there is no prior NVIDIA hardware relationship being reinforced.

Why this matters: NVIDIA's per-quarter math is a legitimate rebuttal to the loudest version of the Burry-style bear case, but it doesn't resolve the more patient concern — that a rapidly compounding investment balance, an OpenAI pledge that already shrank once, and a nine-figure debt-guarantee conversation happening in parallel are, together, a bet that AI-lab demand stays solvent long enough to justify the exposure NVIDIA is accumulating on all of them at once, SSI included.

## 06. From TPUs to Vera Rubin: the Compute Pivot

SSI's compute base was built on Google TPUs, not NVIDIA GPUs, which means the new NVIDIA arrangement reads less like a captive customer reinforcing its own vendor and more like a genuine second bet on a different hardware stack — with the terms of that bet still unstated.

The starting point matters. Google Cloud announced its partnership to supply SSI with TPUs for research and development at Google Cloud Next '25, back in April 2025 — a full 15 months before Vera Rubin access made headlines. No chip count or dollar figure was ever disclosed for that arrangement, a notable contrast with, for instance, Anthropic's publicly quantified TPU commitments [^14]. What's easy to miss is that the same week Google's TPU deal surfaced, both Alphabet and NVIDIA put cash into SSI's roughly $2B raise at a $32B valuation [^13]. Google (the compute supplier) and NVIDIA (now also a compute supplier) have both been SSI shareholders since spring 2025. Whatever changed on July 27, it wasn't NVIDIA showing up for the first time.

:::timeline
- {date: "2025-04", headline: "Google TPU partnership", body: "SSI partners with Google Cloud to use TPUs for R&D; no chip count or dollar figure disclosed."}
- {date: "2025-04", headline: "Alphabet and NVIDIA both invest", body: "Both companies join SSI's $32B-valuation round the same week — one supplying compute, the other now a shareholder."}
- {date: "2026-07-27", headline: "Vera Rubin access announced", body: "NVIDIA grants SSI priority access to its next-gen platform; SSI does not confirm whether this replaces or supplements TPUs."}
:::

The headline framing — "SSI shifts from Google TPUs to NVIDIA GPUs" [^6] — is tidier than the underlying reporting supports. The more careful account states plainly that "SSI hasn't said whether the Vera Rubin systems will replace [Google TPU] infrastructure or simply run alongside it" [^7]. No primary statement from SSI, Google, or NVIDIA uses "replace," "terminate," or "exclusive." TechCrunch's own direct coverage mentions the Google Cloud partnership only as prior background, without asserting termination or exclusivity in either direction — the absence of "instead of" language from the outlet closest to the announcement is itself informative [^5]. What is confirmed is narrower and more interesting: NVIDIA secured "rare access into the company's closely guarded research" as part of its diligence for the deal [^8].

If this were purely a cost decision, it would run backwards. SemiAnalysis's technical accounting puts Google's TPUv7 at roughly 20-50% lower total cost per useful FLOP than NVIDIA's GB200/GB300 — around 30% lower than GB200 specifically — even after Google's leasing margin, using Anthropic's TPU deployment as the load-bearing case study [^37]. {accent}A pure economics-driven switch would point SSI toward more TPUs, not away from them{/}. The SemiAnalysis cost data argues against a rational pure-cost migration to NVIDIA, so if SSI genuinely displaces TPU capacity with GPU capacity rather than adding to it, the more plausible drivers are pricing leverage, priority access to scarce next-generation hardware, or terms attached to a compute-for-equity relationship — not a spreadsheet favoring NVIDIA on raw FLOPS-per-dollar.

:::compare
- {role: "COST ADVANTAGE", name: "Google TPUv7", value: "-20 to -50%", note: "vs. GB200/GB300 (SemiAnalysis)"}
- {role: "TIMING", name: "NVIDIA Vera Rubin", value: "H2 2026", note: "partner availability, just ramping"}
- {role: "SUBJECT", name: "SSI's choice", value: "Both?", note: "exclusivity unconfirmed"}
:::

There is also a dual-vendor logic that doesn't require SSI to be choosing sides at all. Frontier labs increasingly run mixed compute fleets partly to hedge vendor lock-in and gain pricing leverage against either supplier — Anthropic reportedly runs on the order of 400K purchased TPUv7 units plus 600K rented from Google alongside its own NVIDIA fleet [^37]. That is one company's disclosed strategy, extrapolated here as an industry pattern rather than a direct claim about SSI's motives — SSI's infrastructure operation is far smaller than Anthropic's.

Timing adds another wrinkle to the "10x compute in 12 months" framing: Vera Rubin — Blackwell's successor, 336 billion transistors, roughly 3.5x Blackwell's training FLOPS via a new Vera CPU replacing Grace — entered production around mid-2026, with partner and cloud availability only beginning in the second half of 2026 [^38]. That's real, shipping-imminent silicon, not vaporware, but it was not yet broadly deployed in the field when SSI's announcement landed on July 27, and no SSI-specific delivery date within that H2 2026 rollout has been reported [^38].

Why it matters: whether NVIDIA is adding capacity alongside TPUs or displacing them changes the read on SSI's capital efficiency, its independence from any single supplier, and — given the unresolved cost gap — whether this deal was priced as compute or as something closer to a strategic-access arrangement dressed as one.

## 07. SSI Against Its Peers

Every other frontier lab in this comparison set can be priced against at least a computable — if generous — revenue denominator; Safe Superintelligence is the only $32B-plus company here with no revenue line to divide by at all, run-rate or actual.

That distinction matters because "run-rate revenue" and "actual trailing revenue" are not interchangeable, and the gap between them is where most of the industry's valuation optimism hides. A run-rate is one month's revenue multiplied by twelve — a snapshot, not a track record. Anthropic's headline $47B figure is exactly that: its most recent monthly revenue, annualized [^51]. ==unverified: independent analysis puts Anthropic's actual calendar-2026 revenue at $20-26B — nearly half the run-rate headline — with FY2025 actual revenue estimated at roughly $9-10B, though the precise figure varies by source and is harder to pin down than the run-rate headline==[^52]. OpenAI shows the same pattern at smaller scale: a ~$25B annualized run-rate by early 2026 sat alongside $13.1B in FY2025 actual booked revenue [^58]. In both cases, the number a company chooses to lead with is the one that makes the growth curve look steepest.

Against that backdrop, SSI's valuation is priced on team and mission alone. Founded in June 2024, it raised at a $32B valuation in April 2025 with $0 revenue and no shipped public product [^10] — not a small run-rate, not an early ARR ramp, but a genuine absence of a revenue line.

:::exhibit(num="Exhibit 1", title="Six labs, one missing denominator", subtitle="Founded · Valuation · Revenue (run-rate vs. actual) · Shipped product", source="Company disclosures; TechCrunch; Bloomberg; Yahoo Finance; ValueAdd VC; Forbes; Wikipedia")
| Lab | Founded | Latest valuation | Revenue (run-rate) | Revenue (actual trailing) | Shipped product? |
|---|---|---|---|---|---|
| *Safe Superintelligence | June 2024 [^10] | $32B (Apr 2025) [^10] | N/A | N/A | No [^10] |
| OpenAI | Dec 2015 [^50] | $852B (Mar 2026) [^50] | ~$25B annualized [^58] | $13.1B FY2025 [^58] | Yes — ChatGPT, GPT API [^50] |
| Anthropic | 2021 [^51] | $965B (May 2026) [^51] | $47B [^51] | ~$9-10B FY2025 (est., varies by source) [^52] | Yes — Claude, Claude Code [^51] |
| xAI | Mar 2023 [^54] | $250B (Feb 2026) [^53] | Not separately disclosed | $3.2B FY2025 (filing-disclosed) [^53] | Yes — Grok [^54] |
| Mistral AI | Apr 2023 [^55] | €11.7B confirmed (Sept 2025) [^55] | $400M ARR (Jan 2026) [^55] | N/A — ARR-only | Yes — Le Chat, API [^55] |
| Perplexity | Aug 2022 [^56] | $22.6-23B (Jan 2026) [^56] | $450M+ ARR (Mar 2026) [^56] | N/A — ARR-only | Yes — search engine, Comet [^56] |

:::note
xAI's $3.2B figure is unusually reliable for this set: it comes from a SpaceX-merger IPO filing, not a company press release, alongside a disclosed $6.4B operating loss [^53].
:::
:::

Ranking the five labs with any revenue at all by valuation per dollar of actual trailing revenue (using ARR where no actual-trailing figure is disclosed) produces multiples that are themselves eye-watering before SSI even enters the picture:

:::rank-list
- {label: "Anthropic", value: "≈97-107x — $965B ÷ ~$9-10B FY2025 (est.)", pct: 100}
- {label: "xAI", value: "≈78x — $250B ÷ $3.2B FY2025 actual", pct: 80}
- {label: "OpenAI", value: "≈65x — $852B ÷ $13.1B FY2025 actual", pct: 67}
- {label: "Perplexity (ARR-based)", value: "≈51x — $22.6B ÷ $450M ARR", pct: 53}
- {label: "Mistral (ARR-based)", value: "≈33x — €11.7B ÷ $400M ARR", pct: 34}
- {label: "Safe Superintelligence", value: "N/A — no revenue", pct: 0, highlight: true}
:::

Using the ~$9-10B FY2025 actual-revenue estimate gives a rough ~97-107x multiple; swapping in the 2026 analyst-estimated actual range ($20-26B) instead would pull that down to roughly 37-48x — still rich, just less extreme than the run-rate-driven headline implies. Either way, Anthropic anchors the top of this list, which is itself the point: {accent}the labs with the most defensible product-market fit are also the most expensively priced against their own fundamentals{/}.

That is the counterpoint that keeps SSI's position from reading as uniquely irrational. A 65-97x multiple on actual trailing revenue is not a conservative valuation by any traditional standard — it prices in years of assumed growth that has not yet happened, for companies that do have paying customers today. SSI's problem is not that it breaks this pattern; it is that it removes the denominator that makes the pattern computable at all. {tag}Difference of degree, not of kind{/}: the market has already shown it will price frontier AI labs almost entirely on trajectory rather than trailing fundamentals — SSI is simply the limiting case of a bet the market was already making.

Why this matters: if $965B for Anthropic already prices in a decade of assumed dominance against $10B of real revenue, then $32B for a team with zero revenue and zero shipped product is not a different kind of bet — it is the same bet, stripped of even the fig leaf of a financial denominator, which means SSI's valuation floor and ceiling are set entirely by narrative, comparable-company anchoring, and founder reputation, with no earnings report anywhere on the horizon to correct it.

## 08. Bull, Bear, and the Verdict of the Market

The market's actual verdict on the NVIDIA-SSI deal was neither euphoria nor panic — NVIDIA shares fell as much as 5.3% intraday and closed down roughly 5% the same day the deal was announced, but reporting attributes that move mainly to a broader semiconductor and China-chip-competition selloff, not to specific doubts about paying into a zero-revenue lab [^48]. That's an important distinction: the stock's move is evidence about sentiment toward NVIDIA's chip franchise that day, not a clean read on how investors price the SSI bet itself. The analyst community's actual language skewed toward measured rather than alarmed: a Wedbush analyst described the investment as fitting "squarely into the circular investment theme" while noting it "could create a competitive moat if Nvidia executes" — hedge language, not a sell call [^29]. Even the most quotable bear reaction stopped short of calling a top: Jim Cramer's "I lived through 2000... I don't want the sequel" was paired, in the same breath, with him calling NVIDIA "an exceptionally strong company" [^49].

:::quote(attr="Jim Cramer, CNBC, Jul 27 2026")
I lived through 2000... I don't want the sequel.
:::

The louder bear case lives one level up, in critiques of the AI capex cycle broadly rather than SSI by name. Michael Burry has pointed to a Shiller CAPE ratio of 40.1 as of May 2026 as a dot-com-peak-grade valuation signal for the AI rally [^40]. Jim Chanos argues the mechanics are worse than the number: he sees the current AI infrastructure buildout as structurally identical to the 1998-2000 telecom capacity glut that preceded the dot-com bust — "we have the same setup" of companies over-ordering capacity ahead of demand [^41]. Josh Wolfe of Lux Capital frames the gap in dollar terms, estimating frontier AI labs need somewhere between $250-400B of additional realized economic value to justify valuations already on the books [^42]. And the macro backstop for all three came from the Bank for International Settlements, whose annual report warned that disappointing AI returns could turn hyperscaler capex — over $1T combined across the top five in 2025-2026, funded partly by $159B in tech corporate bond issuance in just five months of 2026 — into a "protracted investment bust" [^43]. None of these four target SSI specifically; all four describe the pool SSI's valuation swims in.

Set against that is a genuinely serious bull case that doesn't depend on SSI hitting conventional revenue multiples at all. One analysis frames SSI's price as rational precisely because it isn't a bet on near-term cash flow: it's an option on being one of a small number of eventual AGI winners, where "overpaying on valuation today is almost irrelevant if you think SSI has, say, a 5-10% chance of being that winner" [^46]. That's the analyst's own illustrative math, not a number any actual SSI investor has disclosed — but the logic has real precedent. ==unverified: DeepMind ran roughly a decade from its 2010 founding to its first reported profit in 2020 (cited at roughly £44M / $60M, though exact figures vary by source), and needed a mid-journey de-risking event — Google's 2014 acquisition, reported in the $400-650M range depending on source — to survive heavy annual losses through 2018-19==[^44]. OpenAI's runway was shorter, about 4.5 years from its no-product, no-revenue December 2015 founding to its first monetized product, the GPT-3 API beta in June 2020 [^45] — but it too was de-risked mid-journey, via a 2019 for-profit restructuring and a $1B Microsoft cash infusion. SSI, by contrast, has neither had nor needed either kind of event yet; the NVIDIA round is arguably the closest thing to one it has taken.

| Company | Founded | First product / profit | Time to milestone | De-risked mid-journey? |
|---|---|---|---|---|
| *Safe Superintelligence | Jun 2024 | None disclosed as of Jul 2026 | 25 months and still pre-product | No — this NVIDIA round is the closest analog to date |
| DeepMind | 2010 | First reported profit, 2020 (est., figure disputed) [^44] | ~10 yrs | Yes — Google acquisition, 2014 (reported $400-650M) |
| OpenAI | Dec 2015 | GPT-3 API beta, Jun 2020 [^45] | ~4.5 yrs | Yes — 2019 for-profit restructuring + $1B Microsoft cash infusion |

Even the intellectual foundation for Sutskever's own "safe superintelligence first" framing has been contested rather than accepted wholesale. A detailed independent critique of his Dwarkesh interview reasoning disputes a load-bearing premise — that LLMs generalize worse than humans do — flatly countering that "humans do not actually generalize all that well" [^57]. That's one well-regarded critic's view, not a peer-reviewed consensus, but it matters here because it cuts at the justification for the zero-product runway, not just its price tag.

Where does the market itself come down, stripped of all this commentary? Polymarket's "AI bubble burst by...?" contract, resolving whether a bust occurs by December 31, 2026, was pricing roughly 19.9% Yes against 83.7% No on $2.91M of volume as of July 28, 2026 [^39].

:::compare
- {role: "BEAR CASE (Yes)", name: "Bubble bursts by Dec 2026", value: "19.9%"}
- {role: "BULL CASE (No)", name: "No bust by Dec 2026", value: "83.7%"}
- {role: "SUBJECT", name: "Polymarket, as of Jul 28 2026", value: "$2.91M vol."}
:::

That 83.7% No is genuine counter-evidence to an imminent-collapse consensus — but the contract only resolves Yes if any of several severe, specific conditions occurs (e.g., a sustained NVDA drawdown from its all-time high, a major AI-lab bankruptcy, or a broad semiconductor-index collapse), not a simple "valuations look stretched" bar, so the low Yes price reflects the difficulty of tripping any one of those triggers more than it reflects confidence that deals like SSI's are fairly priced today. Both things can be true — professional bettors aren't pricing a near-term systemic collapse, even as respected voices argue the underlying capex mechanics rhyme with 2000 — and the SSI deal is a clean test case precisely because it sits at the extreme end of the "priced on faith, not fundamentals" spectrum the whole debate is about.

## 09. What Would Break This Thesis

Everything argued above is a bet on incomplete information, and the honest close is to name exactly what would prove it wrong — in either direction — rather than let the ambiguity stand as an implicit verdict.

Start with the number the whole analysis pivots on. If NVIDIA or SSI ever confirms a dollar figure — via a filing or an on-record statement — that matches Bloomberg's $5 billion almost exactly [^3][^4], the sourcing-uncertainty framing in Section 01 becomes moot, and the "unconfirmed number" caveat should retire; if instead a future disclosure reveals a figure meaningfully larger or smaller, or reveals the "equity investment" language in [^4] actually described a different structure than a cash-for-stake purchase, the "escalation of an existing stake" reading needs revision. NVIDIA's own history with OpenAI is the cautionary case here: a headline commitment shrank substantially between announcement and close [^30][^31]. There is no reason SSI's number is immune to the same kind of drift, in either direction.

The zero-product premise (Section 03) is the single most falsifiable claim in this article. Any public paper, model weight, benchmark submission, or product launch from SSI would directly contradict the "zero shipped models" framing this piece and its source topic both start from. Absence of evidence has been treated carefully throughout — as evidence of secrecy or of genuine emptiness, not proof of either — but that hedge has an expiration date. If SSI's compute base actually increases 10x over the next 12 months as claimed [^2] and still produces nothing publishable, the "deliberately avoiding premature disclosure" reading becomes harder to sustain; conversely, a single credible technical disclosure would validate Sutskever's own claim that "we have research that is worthy of scaling up" [^2][^20] and undercut this piece's skepticism directly.

Governance is the third open variable. Sutskever is a single point of failure for a $32B company by design — no other named technical staff, no published safety framework, and a co-founder who already left for a rival lab within SSI's first 13 months [^17][^18][^21]. That structure would be validated as sound if SSI's headcount, safety disclosures, or public technical bench visibly deepens over the next year; it would be undermined further if Sutskever himself departs, or if reporting surfaces internal dissent beyond the ambiguous "winding down" language already on the record [^17].

Finally, the macro backdrop this deal sits inside is itself a falsifiable claim on a defined timeline. Polymarket's "AI bubble burst by...?" contract resolves by December 31, 2026 [^39] — if it resolves Yes, the BIS's "protracted investment bust" warning [^43] and Burry's and Chanos's dot-com comparisons [^40][^41] gain real evidentiary weight retroactively, and SSI's valuation should be read as a casualty of the same overextension, not a special case. If it resolves No, and NVIDIA's revenue, cash flow, and buyback capacity (Section 05) keep compounding without a demand shock, the bear case loses its strongest piece of supporting evidence, and the option-value bull case [^46] gains ground by default — not because SSI shipped anything, but because the capital underlying the whole ecosystem proved resilient.

:::kv
- {term: "Confirms/contradicts the deal-size claim", def: "A filing or on-record statement naming an exact dollar figure"}
- {term: "Confirms/contradicts the zero-product premise", def: "Any published paper, model, benchmark, or product from SSI"}
- {term: "Confirms/contradicts the single-founder risk", def: "Sutskever's departure, incapacity, or documented internal dissent"}
- {term: "Confirms/contradicts the bubble thesis", def: "Polymarket's Dec 31, 2026 resolution on an AI-bubble-burst event"}
:::

None of these four tests has resolved as of this writing, which is itself the honest finding: this is a live, contested bet, not a settled scandal or a settled triumph. The same discipline applies to this piece's own starting point — the premise correction in Section 03 (SSI founded 2024, not 2023) is a reminder that even a widely repeated detail in a "well-known" story can be wrong, and that the rest of this analysis is only as solid as the sourcing chain behind each number, all of which is laid out, reference by reference, below.

:::references
- {id: 1, title: "Ilya Sutskever's Safe Superintelligence Inc. and NVIDIA Announce Long-Term Strategic Partnership", url: "https://nvidianews.nvidia.com/news/ilya-sutskevers-safe-superintelligence-inc-and-nvidia-announce-long-term-strategic-partnership", source: "NVIDIA Newsroom", date: "2026-07-27"}
- {id: 2, title: "Ilya Sutskever's Safe Superintelligence Inc. and NVIDIA Announce Long-Term Strategic Partnership (joint release)", url: "https://www.globenewswire.com/news-release/2026/07/27/3333561/0/en/Ilya-Sutskever-s-Safe-Superintelligence-Inc-and-NVIDIA-Announce-Long-Term-Strategic-Partnership.html", source: "GlobeNewswire", date: "2026-07-27"}
- {id: 3, title: "Nvidia Makes Substantial Investment in Sutskever's AI Startup", url: "https://www.bloomberg.com/news/articles/2026-07-27/nvidia-makes-substantial-investment-in-sutskever-s-ai-startup", source: "Bloomberg", date: "2026-07-27"}
- {id: 4, title: "Nvidia to invest $5 billion in Ilya Sutskever's AI startup, source says", url: "https://www.investing.com/news/stock-market-news/nvidia-to-invest-5-billion-in-ilya-sutskevers-ai-startup-source-says-4814862", source: "Reuters via Investing.com", date: "2026-07-27"}
- {id: 5, title: "Ilya Sutskever's Safe Superintelligence partners with Nvidia to scale its AI research", url: "https://techcrunch.com/2026/07/27/ilya-sutskevers-safe-superintelligence-partners-with-nvidia-to-scale-its-ai-research/", source: "TechCrunch", date: "2026-07-27"}
- {id: 6, title: "Nvidia invests $5 billion in Ilya Sutskever's Safe Superintelligence as AI startup shifts from Google TPUs to GPUs", url: "https://techstartups.com/2026/07/27/nvidia-invests-5-billion-in-ilya-sutskevers-safe-superintelligence-as-ai-startup-shifts-from-google-tpus-to-gpus/", source: "Tech Startups", date: "2026-07-27"}
- {id: 7, title: "Ilya Sutskever's SSI chooses Nvidia Vera Rubin systems after earlier Google TPU partnership", url: "https://www.neowin.net/news/ilya-sutskevers-ssi-chooses-nvidia-vera-rubin-systems-after-earlier-google-tpu-partnership/", source: "Neowin", date: "2026-07-27"}
- {id: 8, title: "Ilya Sutskever's Safe Superintelligence gets access to Nvidia's Vera Rubin platform", url: "https://siliconangle.com/2026/07/27/ilya-sutskevers-safe-superintelligence-gets-access-nvidias-vera-rubin-platform/", source: "SiliconANGLE", date: "2026-07-27"}
- {id: 9, title: "Ilya Sutskever's startup Safe Super Intelligence raises $1B", url: "https://techcrunch.com/2024/09/04/ilya-sutskevers-startup-safe-super-intelligence-raises-1b", source: "TechCrunch", date: "2024-09-04"}
- {id: 10, title: "OpenAI co-founder Ilya Sutskever's Safe Superintelligence reportedly valued at $32B", url: "https://techcrunch.com/2025/04/12/openai-co-founder-ilya-sutskevers-safe-superintelligence-reportedly-valued-at-32b", source: "TechCrunch", date: "2025-04-12"}
- {id: 11, title: "Safe Superintelligence, Ilya Sutskever's AI startup, is reportedly close to raising roughly $1B", url: "https://techcrunch.com/2025/02/18/safe-superintelligence-ilya-sutskevers-ai-startup-is-reportedly-close-to-raising-roughly-1b", source: "TechCrunch", date: "2025-02-18"}
- {id: 12, title: "Safe Superintelligence — Financials", url: "https://www.cbinsights.com/company/safe-superintelligence/financials", source: "CB Insights", date: "2026"}
- {id: 13, title: "Alphabet, Nvidia invest in AI startup Safe Superintelligence", url: "https://finance.yahoo.com/news/alphabet-nvidia-invest-ai-startup-102359815.html", source: "Yahoo Finance (Reuters)", date: "2025-04"}
- {id: 14, title: "AI startup Safe Superintelligence to use Google's TPU chips for research", url: "https://www.datacenterdynamics.com/en/news/ai-startup-safe-superintelligence-to-use-googles-tpu-chips-for-research/", source: "DataCenterDynamics", date: "2025-04-09"}
- {id: 15, title: "OpenAI co-founder Ilya Sutskever announces Safe Superintelligence", url: "https://www.cnbc.com/2024/06/19/openai-co-founder-ilya-sutskever-announces-safe-superintelligence.html", source: "CNBC", date: "2024-06-19"}
- {id: 17, title: "Ilya Sutskever is CEO of Safe Superintelligence after Meta hired Gross", url: "https://www.cnbc.com/2025/07/03/ilya-sutskever-is-ceo-of-safe-superintelligence-after-meta-hired-gross.html", source: "CNBC", date: "2025-07-03"}
- {id: 18, title: "Meta tried to buy Safe Superintelligence, hired CEO Daniel Gross", url: "https://www.cnbc.com/2025/06/19/meta-tried-to-buy-safe-superintelligence-hired-ceo-daniel-gross.html", source: "CNBC", date: "2025-06-19"}
- {id: 19, title: "Meta hires Safe Superintelligence execs after CEO Ilya Sutskever rejects $32B acquisition offer", url: "https://techstartups.com/2025/06/20/meta-hires-safe-superintelligence-execs-after-ceo-ilya-sutskever-rejects-32b-acquisition-offer/", source: "Tech Startups", date: "2025-06-20"}
- {id: 20, title: "Ilya Sutskever interview", url: "https://www.dwarkesh.com/p/ilya-sutskever-2", source: "Dwarkesh Podcast", date: "2025-11-25"}
- {id: 21, title: "Safe Superintelligence Inc.", url: "https://ssi.inc/", source: "SSI official site", date: "2026-07-28"}
- {id: 22, title: "X post: 'I deeply regret my participation in the board's actions'", url: "https://x.com/ilyasut/status/1726590052392956028", source: "X / Ilya Sutskever", date: "2023-11-20"}
- {id: 23, title: "X post: 'After almost a decade, I have made the decision to leave OpenAI'", url: "https://x.com/ilyasut/status/1790517455628198322", source: "X / Ilya Sutskever", date: "2024-05-14"}
- {id: 24, title: "OpenAI co-founder Ilya Sutskever says he will leave the startup", url: "https://www.cnbc.com/2024/05/14/openai-co-founder-ilya-sutskever-says-he-will-leave-the-startup.html", source: "CNBC", date: "2024-05-14"}
- {id: 25, title: "OpenAI board fires Sam Altman", url: "https://sfstandard.com/2023/11/17/openai-sam-altman-firing-board-members/", source: "SF Standard", date: "2023-11-17"}
- {id: 26, title: "OpenAI staff threaten to go to Microsoft if board doesn't quit", url: "https://www.bloomberg.com/news/articles/2023-11-20/openai-staff-threaten-to-go-to-microsoft-if-board-doesn-t-quit", source: "Bloomberg", date: "2023-11-20"}
- {id: 27, title: "Sam Altman returns as CEO, OpenAI has a new initial board", url: "https://openai.com/index/sam-altman-returns-as-ceo-openai-has-a-new-initial-board/", source: "OpenAI", date: "2023-11-22"}
- {id: 28, title: "Ilya Sutskever deposition reveals how Sam Altman's 2023 firing was planned for over a year", url: "https://winbuzzer.com/2025/11/03/ilya-sutskever-deposition-reveals-how-sam-altmans-2023-firing-was-planned-for-over-a-year-xcxwbn/", source: "WinBuzzer", date: "2025-11-03"}
- {id: 29, title: "Nvidia's $750 Billion Deals Revive Fear of AI Circular Financing", url: "https://finance.yahoo.com/technology/ai/articles/nvidia-750-billion-deals-revive-102003935.html", source: "Bloomberg via Yahoo Finance", date: "2026-07-27"}
- {id: 30, title: "Jensen Huang: Nvidia's OpenAI investment was 'never a commitment'", url: "https://fortune.com/2026/02/02/jensen-huang-nvidia-ceo-on-openai-investment-never-a-commitment/", source: "Fortune", date: "2026-02-02"}
- {id: 31, title: "Nvidia-OpenAI investment shrinks from $100B to $30B as compute-lock war continues", url: "https://www.techtimes.com/articles/317839/20260605/nvidia-openai-investment-shrinks-100b-30b-compute-lock-war-continues.htm", source: "Tech Times", date: "2026-06-05"}
- {id: 32, title: "Nvidia memo responds to Michael Burry's AI-bubble fears", url: "https://www.theglobeandmail.com/business/article-nvidia-michael-burry-memo-ai-bubble-fears/", source: "The Globe and Mail", date: "2025-11"}
- {id: 33, title: "Nvidia embraces AI investor role, topping $40 billion in equity bets in 2026", url: "https://www.cnbc.com/2026/05/09/nvidia-embraces-ai-investor-topping-40-billion-in-equity-bets-2026.html", source: "CNBC", date: "2026-05-09"}
- {id: 34, title: "NVIDIA Announces Financial Results for First Quarter Fiscal 2027", url: "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-first-quarter-fiscal-2027", source: "NVIDIA Newsroom", date: "2026-05-20"}
- {id: 35, title: "NVIDIA Corporation Form 10-Q, quarter ended April 26, 2026", url: "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000052/nvda-20260426.htm", source: "SEC EDGAR", date: "2026-05-20"}
- {id: 37, title: "TPUv7: Google Takes a Swing at the Merchant Silicon Market", url: "https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the", source: "SemiAnalysis", date: "2026"}
- {id: 38, title: "Nvidia Launches Next-Generation Rubin AI Compute Platform at CES 2026", url: "https://www.servethehome.com/nvidia-launches-next-generation-rubin-ai-compute-platform-at-ces-2026/", source: "ServeTheHome", date: "2026"}
- {id: 39, title: "AI bubble burst by...?", url: "https://polymarket.com/event/ai-bubble-burst-by", source: "Polymarket", date: "2026-07-28"}
- {id: 40, title: "Michael Burry warns AI boom may echo past market bubbles", url: "https://www.gurufocus.com/news/8955042/michael-burry-warns-ai-boom-may-echo-past-market-bubbles", source: "GuruFocus", date: "2026-05-08"}
- {id: 41, title: "Jim Chanos warns AI spending mirrors dot-com era", url: "https://finance.yahoo.com/news/jim-chanos-warns-ai-spending-171853416.html", source: "Yahoo Finance", date: "2026-06"}
- {id: 42, title: "Top VC explains why he thinks AI valuations are unjustified", url: "https://tech.yahoo.com/ai/articles/top-vc-explains-why-thinks-172300936.html", source: "Yahoo Tech", date: "2026"}
- {id: 43, title: "How the AI bubble could pop and take down the global economy, according to the BIS", url: "https://www.theregister.com/ai-and-ml/2026/06/29/how-the-ai-bubble-could-pop-and-take-down-the-global-economy-according-to-the-bis/5263793", source: "The Register", date: "2026-06-29"}
- {id: 44, title: "DeepMind: company history and financials", url: "https://fourweekmba.com/deepmind/", source: "FourWeekMBA", date: "2026"}
- {id: 45, title: "OpenAI", url: "https://en.wikipedia.org/wiki/OpenAI", source: "Wikipedia", date: "2026-07-28"}
- {id: 46, title: "Safe Superintelligence at $32B: Ilya Sutskever's slow-safe vs. fast-deployed bet", url: "https://agentmarketcap.ai/blog/2026/04/06/safe-superintelligence-32b-ilya-sutskever-slow-safe-vs-fast-deployed", source: "AgentMarketCap", date: "2026-04-06"}
- {id: 47, title: "Nvidia pours billions into Safe Superintelligence, a startup with no product and no revenue", url: "https://www.trendingtopics.eu/nvidia-pours-billions-into-safe-superintelligence-a-startup-with-no-product-and-no-revenue/", source: "Trending Topics", date: "2026-07-28"}
- {id: 48, title: "Nvidia's reported $5 billion SSI investment fails to lift NVDA stock amid chip stocks selloff", url: "https://finance.yahoo.com/markets/stocks/articles/nvidias-reported-5-billion-ssi-174148818.html", source: "Yahoo Finance", date: "2026-07-27"}
- {id: 49, title: "Jim Cramer warns AI circular financing echoes dot-com bubble", url: "https://www.cnbc.com/2026/07/27/jim-cramer-warns-ai-circular-financing-echoes-dot-com-bubble.html", source: "CNBC", date: "2026-07-27"}
- {id: 50, title: "Accelerating the next phase of AI", url: "https://openai.com/index/accelerating-the-next-phase-ai/", source: "OpenAI", date: "2026-03-31"}
- {id: 51, title: "Series H", url: "https://www.anthropic.com/news/series-h", source: "Anthropic", date: "2026-05-28"}
- {id: 52, title: "Why Anthropic's $965 billion IPO could pay off massively for investors", url: "https://www.forbes.com/sites/petercohan/2026/05/29/why-anthropics-965-billion-ipo-could-pay-off-massively-for-investors/", source: "Forbes", date: "2026-05-29"}
- {id: 53, title: "xAI burned $6.4B last year on $3.2B in revenue, SpaceX filing shows", url: "https://finance.yahoo.com/sectors/technology/articles/xai-burned-6-4b-last-222608682.html", source: "Yahoo Finance", date: "2026"}
- {id: 54, title: "xAI (company)", url: "https://en.wikipedia.org/wiki/XAI_(company)", source: "Wikipedia", date: "2026-07-28"}
- {id: 55, title: "France's Mistral in funding talks at about $20 billion valuation", url: "https://www.bloomberg.com/news/articles/2026-06-12/france-s-mistral-in-funding-talks-at-about-20-billion-valuation", source: "Bloomberg", date: "2026-06-12"}
- {id: 56, title: "Perplexity AI valuation and revenue 2026: $23B, $450M ARR", url: "https://valueaddvc.com/blog/perplexity-ai-valuation-revenue-2026-23b-450m-arr", source: "ValueAdd VC", date: "2026"}
- {id: 57, title: "On Dwarkesh Patel's Second Interview With Ilya Sutskever", url: "https://www.lesswrong.com/posts/bMvCNtSH8DiGDTvXd/on-dwarkesh-patel-s-second-interview-with-ilya-sutskever", source: "LessWrong (Zvi Mowshowitz)", date: "2025-11-26"}
- {id: 58, title: "OpenAI revenue 2026: $25B ARR, $2B/month, and the path to profitability", url: "https://valueaddvc.com/blog/openai-revenue-2026-25b-arr-2b-month-and-the-path-to-profitability", source: "ValueAdd VC", date: "2026"}
:::
