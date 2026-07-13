---
eyebrow: REPORT · ANTHROPIC
title: The Anthropic Flywheel — What Eight Hires in Ten Weeks Actually Reveal
deck: A paywalled Substack post argued Anthropic's 2026 hiring spree wasn't IPO prestige-signaling but a bet on talent, compute, and customers reinforcing each other toward recursive self-improvement. We checked all eight names against primary sources. Most of the underlying facts hold. The framing oversells the pattern.
lede: |
  Between April 7 and July 13, 2026, Anthropic added eight publicly named senior hires: a co-founder of OpenAI, a Nobel laureate, a UC Berkeley department chair, two former Microsoft Azure executives, an xAI co-founder, a fintech founder, and a career public-sector dealmaker. A Substack post by investor Guillermo Flor read the cluster as evidence of a deliberate strategy — not prestige-building ahead of an IPO, but resource acquisition for a self-reinforcing loop of research talent, compute, and paying customers. We verified all eight hires independently, cross-checked the recursive-self-improvement framing against what Anthropic itself has said on the record, and stress-tested the IPO counter-explanation the original post dismissed. The hires are real. The "distinctive strategy" reading survives only partially.
domain: general
stats:
  - {label: Named hires, value: 8, note: "Apr 7 – Jul 13, 2026"}
  - {label: Run-rate revenue, value: $47B, note: "May 2026, up from $9B (Dec 2025)"}
  - {label: Valuation, value: $965B, note: "Series H, May 28, 2026"}
  - {label: AWS compute commitment, value: $100B+, note: "10-yr, up to 5GW"}
---

## 01. Eight names, one theory to test

The seed for this piece is a single tweet: investor Guillermo Flor posted "Anthropic's hiring pattern reveals its bet on recursive self-improvement," linking to his own paywalled Substack essay, "Anthropic is becoming this."[^1] The visible preview names eight hires by surname only — Karpathy, Jumper, Blomfield, Nordeen, Fontoura, Nelson, Carlson, Boyd — and argues that grouping them by function (research talent, compute infrastructure, enterprise/government demand) reveals a flywheel strategy rather than "prestige signaling ahead of an IPO."[^1]

That is a strong, specific, checkable claim, and a paywalled Substack post is a weak foundation for it. So we treated the tweet and its linked essay as a hypothesis, not a source, and rebuilt the case from primary material: the hires' own social posts, company announcements, SEC-adjacent disclosures, and named reporting.

:::stats
- {label: Karpathy → Anthropic, value: "May 19"}
- {label: Boyd → Anthropic, value: "Apr 7"}
- {label: Jumper → Anthropic, value: "Jun 19"}
- {label: Carlson → Anthropic, value: "Jul 7"}
:::

All eight names check out as real people who joined Anthropic in 2026.[^2][^3][^4][^5][^6][^7][^8][^9][^10][^11][^12] None is a hallucination or a misread section title — a real risk with a paywalled source relayed secondhand. What is contestable is not the roster but the interpretation layered on top of it: whether the pattern is *Anthropic-distinctive* strategy, or the general shape every frontier lab's 2026 hiring has taken.

Anthropic itself has never used the phrase "resource-acquisition flywheel" to describe its hiring. Every on-the-record rationale we found from the hires themselves — Blomfield on compute scarcity, Fontoura on safety, Carlson on early government engagement[^28][^29][^13] — talks about mission and constraints, not strategy architecture. The flywheel is an outside reading of a real pattern, which is a different, weaker claim than the original post makes.

## 02. The talent axis: Karpathy, Jumper, Nelson

Three of the eight hires are research names whose value is reputational and cognitive, not operational.

**Andrej Karpathy** — OpenAI co-founder, former Tesla AI director, founder of Eureka Labs since 2024 — announced on May 19, 2026 that he had joined Anthropic's pretraining team.[^2] This is a real reversal worth flagging: in 2024 Karpathy said he was stepping back from frontier-lab work to focus on AI education.[^14] His own 2026 post software-pedals the change rather than disavowing it — "I remain deeply passionate about education and plan to resume my work on it in time"[^2] — but the fact remains that a person who spent two years publicly building an education startup returned to a frontier lab. His new manager, Nick Joseph, Anthropic's Head of Pretraining, gave the most concrete on-record articulation of the recursive-self-improvement thesis in this entire dataset: "He'll be building a team focused on using Claude to accelerate pretraining research itself. I can't think of anyone better suited to do it."[^3] That sentence — Claude accelerating the research that builds better Claudes — is the single strongest piece of primary evidence for Flor's framing anywhere in the eight hires.

**John Jumper** — AlphaFold co-creator, 2024 Nobel laureate in Chemistry — left Google DeepMind for Anthropic on June 19, 2026, after nearly nine years, in a post that thanked Demis Hassabis but disclosed no title, team, or start date.[^4][^15] That silence has held for weeks. Anthropic's flagship science product, Claude Science, launched eleven days later on June 30, 2026; MIT Technology Review names Jumper only once, purely as background on Anthropic's broader science ambitions, and STAT News's accessible launch coverage does not mention him at all — neither credits him with building or leading the product, which is instead attributed to Alexander Tarashansky and Eric Kauderer-Abrams.[^16][^17] Anthropic has multiple open "founding member of Life Sciences" roles on its careers page describing exactly the kind of computational-biology group Jumper would plausibly lead, but none names him.[^18] ==unverified: any claim that Jumper is leading, or will lead, a specific Anthropic biology division==. The Information's own analysis of the hire put it bluntly: reporting that he will "lead Anthropic's biology division" is "invention, not fact."[^15]

**Jelani Nelson** — chair of UC Berkeley's Computer Science Division, a streaming-algorithms and dimensionality-reduction theorist — joined Anthropic's pretraining team on academic leave (not resignation) effective July 1, 2026.[^9] His specialty is processing data too large to hold in memory in a single pass, a body of theory that maps onto the practical problem of KV-cache and inference-memory limits at scale — a plausible but not company-confirmed connection.[^10]

:::timeline
- {date: "2026-04-07", headline: "Eric Boyd", body: "Ex-Microsoft Azure AI President joins as Head of Infrastructure."}
- {date: "2026-05-06", headline: "SpaceX compute deal", body: "Anthropic secures 300MW+/220,000+ GPUs from Colossus 1."}
- {date: "2026-05-19", headline: "Andrej Karpathy", body: "OpenAI co-founder joins pretraining team, reversing his 2024 pivot to education."}
- {date: "2026-05-07", headline: "Ross Nordeen", body: "xAI co-founder and infrastructure dealmaker joins Anthropic's compute team."}
- {date: "2026-06-01", headline: "Confidential S-1 filed", body: "Anthropic submits a draft registration statement to the SEC."}
- {date: "2026-06-17", headline: "Marcus Fontoura", body: "Ex-Microsoft Azure Core CTO joins as Member of Technical Staff."}
- {date: "2026-06-19", headline: "John Jumper", body: "AlphaFold co-creator, Nobel laureate, leaves DeepMind for Anthropic — no title disclosed."}
- {date: "2026-07-01", headline: "Jelani Nelson", body: "UC Berkeley CS chair joins pretraining team on academic leave."}
- {date: "2026-07-07", headline: "Teresa Carlson", body: "Ex-AWS/Microsoft/Splunk exec named first Global Head of Public Sector."}
- {date: "2026-07-13", headline: "Tom Blomfield", body: "Monzo co-founder takes leave from Y Combinator to join the compute team."}
:::

## 03. The compute axis: Boyd, Fontoura, Nordeen, Blomfield

This is the largest cluster by headcount and the one with the clearest, best-documented rationale: Anthropic is acutely compute-constrained, and it is hiring people who have run compute at hyperscaler scale to fix that.

**Eric Boyd**, Microsoft's President of AI Platform and Azure AI lead for roughly seventeen years — managing around 1,500 people and, notably, the very Azure infrastructure that hosted Anthropic's own models under the companies' prior commercial relationship — joined Anthropic as Head of Infrastructure on April 7, 2026.[^5][^19] **Marcus Fontoura**, CTO of Microsoft's Azure Core and previously CVP of Azure Compute, joined as a Member of Technical Staff around June 17, 2026 — Anthropic's flat title convention applies to founders and new hires alike, so the title itself signals nothing about seniority.[^7][^20] **Ross Nordeen**, one of xAI's founding eleven and the person credited with driving its infrastructure dealmaking (including the original Colossus buildout), joined Anthropic's compute team in early May 2026, in the same week Anthropic signed a deal for the full capacity of SpaceX's Colossus 1 data center — 300+ MW, 220,000+ Nvidia GPUs, reportedly worth $1.25B/month through 2029.[^6][^21][^22] **Tom Blomfield**, Monzo's co-founder and a Y Combinator group partner since 2021, took a leave of absence from YC to join the compute team on July 13, 2026 — the same day Flor's tweet went out — working alongside Anthropic co-founder Tom Brown, described in coverage as Anthropic's chief compute officer.[^11][^23] Blomfield's own words are the most explicit compute-scarcity statement in the dataset: "as we enter the early stages of recursive self-improvement, availability of compute becomes one of the most important issues to solve."[^11]

:::exhibit(num="Exhibit 1", title="Anthropic's disclosed compute commitments, 2025–2026", subtitle="$ and capacity by counterparty", source="Anthropic newsroom; TechCrunch; DataCenterDynamics", note="Figures as disclosed by Anthropic or reported via named secondary sourcing; not all deals report both a dollar figure and a capacity figure.")
:::bars
- {label: "AWS ($100B+/10yr, up to 5GW)", value: "5GW", pct: 100}
- {label: "Google/Broadcom TPU (~3.5GW, from 2027)", value: "3.5GW", pct: 70}
- {label: "xAI/SpaceX Colossus 1 (300MW+)", value: "0.3GW", pct: 6}
- {label: "TeraWulf Kentucky ($19B/20yr, up to 401MW)", value: "0.4GW", pct: 8}
:::
:::

The scale context matters: Anthropic's own newsroom describes running Claude across three separate chip platforms — Google TPU, AWS Trainium, and Nvidia GPU — "a diversified approach that efficiently uses three chip platforms" to advance capability while sustaining partnerships.[^24] By April 2026, CFO Krishna Rao was reportedly spending 30-40% of his time on compute purchasing, framed internally as an existential trade-off: overbuy and the company risks insolvency; underbuy and it falls off the capability frontier.[^25] Dario Amodei told Axios the company had planned for roughly 10x annual usage growth and got closer to 80x, which he directly cited as the cause of 2026's service reliability problems.[^26] Four compute-infrastructure hires in ten weeks reads less like an abstract "flywheel" and more like a company visibly scrambling to keep pace with demand it did not forecast.

## 04. The customer axis: Carlson and the government rollercoaster

**Teresa Carlson** — who built AWS's Worldwide Public Sector business over a decade, then held federal sales and growth roles at Microsoft, Splunk, and General Catalyst's policy institute — was named Anthropic's first-ever Global Head of Public Sector on July 7, 2026.[^12][^13] Anthropic executive Kate Earle Jensen's public endorsement leaned entirely on trust and adoption, not compute or research: "Few people are as trusted across government and industry as Teresa."[^12]

The hire lands in the middle of an unusually volatile year for Anthropic's federal relationship — the kind of environment that would justify creating a first-ever public-sector leadership role on its own, independent of any broader flywheel theory:

:::timeline
- {date: "2025-08-12", headline: "GSA OneGov deal", body: "Claude offered to all three federal branches for a nominal $1/year via GSA's Multiple Award Schedule."}
- {date: "2026-02-27", headline: "Trump directive", body: "Federal agencies directed to cease Anthropic use; GSA removes Anthropic from its schedule."}
- {date: "2026-03", headline: "'Supply chain risk' designation", body: "DOD's CDAO designates Anthropic a supply-chain risk after it refuses surveillance/autonomous-weapons use cases."}
- {date: "2026-03-26", headline: "Preliminary injunction", body: "N.D. Cal. court pauses the directive's rollout (Case No. 26-cv-01996-RFL)."}
- {date: "2026-04-03", headline: "GSA reinstatement", body: "GSA restores Anthropic to pre-Feb-27 status on its Multiple Award Schedule."}
- {date: "2026-04-08", headline: "DOD exclusion persists", body: "Anthropic loses an appeals-court bid to block the DOD-specific supply-chain-risk ruling."}
- {date: "2026-07-07", headline: "Carlson hired", body: "First Global Head of Public Sector named into this exact turbulence."}
:::

No source — Anthropic's own or independent reporting — discloses a segment-level revenue figure for the government business specifically; the GSA's "$1" pricing and DOD's "$200M" contract ceiling (a July 2025 CDAO prototype award shared with Google, OpenAI, and xAI) are pricing mechanisms and ceilings, not realized revenue.[^27][^28] That gap is itself informative: Carlson's hire is best read as institutional-relationship repair and demand-generation infrastructure, not evidence of an already-large government revenue line that needs managing.

:::callout(kind=warn, label=Caveat)
The seed article's specific editorial framing for each hire — "compute as an executive-level challenge" for Blomfield, "improving compute efficiency" for Fontoura, "internal compute platform reliability" for Boyd — could not be independently verified verbatim, because the source essay is paywalled. The underlying hires and their general functional area check out; the precise phrasing attributed to each section does not.
:::

## 05. What "recursive self-improvement" means in Anthropic's own words

This is the section that decides whether Flor's framing is accurate or oversold, because "recursive self-improvement" (RSI) is a term with a specific, narrow meaning in AI safety research — and Anthropic itself has published a position on exactly this question.

On June 4, 2026, the Anthropic Institute published "When AI Builds Itself: Our Progress Toward Recursive Self-Improvement, and Its Implications." Its headline finding is a hedge, not a declaration: "We are not there yet, and recursive self-improvement is not inevitable."[^29] That sentence is the load-bearing fact for this entire article. Outside commentary compresses it into present-tense claims — Scientific American's own headline reads "Anthropic warns AI may soon begin recursive self-improvement"[^30] — but Anthropic's own position is explicitly conditional and forward-looking, not a claim that RSI is the current operating mode the eight hires were made to serve.

That said, the same document backs up a real and fast-moving trend with concrete, self-disclosed numbers:

:::stats
- {label: "Code merged, Claude-authored", value: ">80%", note: "vs. low single digits before Feb 2025"}
- {label: "Code shipped per engineer", value: "8x", note: "per quarter, 2021–2025 baseline"}
- {label: "AI task-length doubling time", value: "4 mo.", note: "down from ~7 months"}
- {label: "Internal training-code speedup", value: "~52x", note: "Claude Mythos Preview vs. ~3x a year earlier"}
:::

Anthropic's own footnotes discipline these figures more than most companies bother to: the 8x code-shipped number is flagged internally as "almost certainly an overstatement," since lines-of-code rewards volume over quality, and the piece separately cites both a "per day vs. 2024" and a "per quarter vs. 2021-2025" framing for what reads like the same headline statistic — an internal inconsistency worth noting rather than smoothing over.[^29]

The closest thing to direct, human testimony behind these numbers comes from Boris Cherny, who leads Claude Code. In January 2026 he said he personally had not made a manual edit to code in over two months; by a June 11 on-stage interview, that streak had reportedly extended to roughly eight months.[^31][^32] An Anthropic spokesperson separately put the company-wide (not just Cherny's) share of AI-generated code between 70% and 90%.[^31]

:::quote(attr="Nick Joseph, Head of Pretraining, Anthropic, May 19 2026")
He'll be building a team focused on using Claude to accelerate pretraining research itself.
:::

Put together: Anthropic is genuinely, measurably using Claude to accelerate its own R&D, and that trend is accelerating. What it is *not* doing, by its own explicit statement, is claiming to have reached recursive self-improvement as an active, current state — the term the seed tweet applies to describe the hiring pattern already underway.

## 06. The compute-efficiency thesis, stress-tested

If Fontoura and Nelson were hired specifically to attack inference and training efficiency — the "compute efficiency" reading Flor's essay applies to Fontoura — that would meaningfully sharpen the flywheel argument. The evidence for it is thinner than the evidence for the hires themselves.

Neither Fontoura nor Nelson is quoted, anywhere we found, connecting their own move to inference cost, KV-cache compression, or algorithmic efficiency specifically. Fontoura's own stated reason for joining, per DataCenterDynamics, centers on "the company's clear commitment to building AI responsibly, ethically, and with deep consideration for its long-term impact" — safety framing, not compute economics.[^7] The efficiency link is layered on afterward by outside commentary, reasoning backward from his Azure Compute pedigree to an assumed mandate.[^33]

The macro data on efficiency gains is real, though, and independently corroborates that Anthropic has strong incentive to prioritize it regardless of any single hire's stated motive:

:::compare
- {role: "2020 ESTIMATE", name: "Hernandez & Brown", value: "1.68x/yr"}
- {role: "2025 ESTIMATE", name: "Dario Amodei", value: "~4x/yr"}
- {role: "SUBJECT", name: "Epoch AI (industry, 2025-26)", value: "2.6–6x/yr"}
:::

Epoch AI's tracked estimate of industry-wide algorithmic progress in language models is equivalent to compute-doubling every 5-14 months.[^34] Dario Amodei's own rough public estimate, from a January 2025 essay, put frontier algorithmic-efficiency gains at roughly 4x per year — more than double the 1.68x-per-year figure his own team measured in a 2020 paper, published before Anthropic's 2021 founding — and he explicitly flagged the newer figure as a personal guess, not a measured company statistic.[^35] Third-party analyst estimates go further: SemiAnalysis reportedly modeled Anthropic's revenue-per-megawatt of compute capacity nearly quadrupling, from roughly $16M to a projected $60M, over about nine months in 2026, alongside a swing from deeply negative to solidly positive blended gross margins.[^36] Those SemiAnalysis figures are third-party estimates of a private company's unaudited financials, not Anthropic disclosures, and should be read with that caveat.

What this section supports, on balance: Anthropic is compute-constrained enough that any genuine efficiency lever is a high organizational priority — but no primary source confirms that Fontoura or Nelson were hired *specifically* to pull that lever, as opposed to being folded into a broader talent-acquisition wave and assigned to it after the fact, or simply being infrastructure/theory hires whose relevance to "efficiency" is real but incidental to their actual mandate.

## 07. Is this actually distinctive, or just the industry-wide talent war?

Flor's framing implicitly treats Anthropic's hiring as sui generis — evidence of a deliberate, singular bet. The comparison set does not support that read.

Every hire *type* in Anthropic's cluster has a same-quarter mirror at a competing lab. The clearest single data point: Google lost Noam Shazeer to OpenAI and John Jumper to Anthropic within 48 hours of each other, June 18-19, 2026 — reported by press as one symmetrical event, not an Anthropic-specific coup.[^37] Jefferies analysts characterized the departures as evidence of "an industry-wide war for talent," not of any one lab's distinctive edge.[^37]

:::rank-list
- {label: "OpenAI", value: "6 professors", pct: 100}
- {label: "Meta", value: "6 professors", pct: 100}
- {label: "Anthropic", value: "5 professors", pct: 83, highlight: true}
- {label: "Google DeepMind", value: "5 professors", pct: 83}
:::

On the one clean, apples-to-apples measure we found — academic poaching in H1 2026, where at least 22 professors left universities for frontier labs — Anthropic (5) trails OpenAI and Meta (6 each) and ties Google DeepMind (5).[^38] Meta's own 2025-2026 poaching of Mira Murati's Thinking Machines Lab reportedly included a $1.5B, six-year package for one individual (co-founder Andrew Tulloch) — a single compensation figure that dwarfs anything disclosed about Anthropic's hires.[^39] OpenAI ran its own cross-company executive poach (hiring Google Cloud/DeepMind corporate-development lead Albert Lee in December 2025) and separately signed a March 2026 AWS deal to sell into U.S. government workloads — a government-relations buildout in the same functional lane as Carlson's mandate, if without one equally publicized marquee name yet attached to it.[^40][^41]

xAI is the mirror-image case: most of its original founding team, plus dozens of additional staff, are reported to have departed in the months around its SpaceX merger — a story of internal attrition, not competitive poaching pressure, and a reminder that "hiring aggressively" and "losing people" can coexist industry-wide in the same quarter. ==unverified: precise co-founder and staff-departure counts, which vary across secondary reports==.[^37]

One data point does support Flor's density argument, even after the individual-hire-type comparisons wash out: SignalFire's 2025 talent-retention report put Anthropic's two-year employee retention at 80%, ahead of DeepMind (78%), OpenAI (67%), and Meta (64%).[^42] The gap to DeepMind is narrow, but the gap to OpenAI and Meta is real — Anthropic is not just hiring aggressively, it is also keeping people at a rate its two most aggressive competitors are not. That combination — a dense, senior hiring cluster on top of unusually strong retention — is a more defensible claim than "Anthropic's hiring is strategically unique," which the comparison set does not support.

## 08. The IPO counter-narrative Flor dismissed too quickly

The seed essay explicitly argues against "prestige signaling ahead of an IPO" as an explanation, without engaging much with the timing evidence. That evidence deserves a direct look, because it complicates rather than confirms either single story.

Anthropic confidentially filed a draft S-1 with the SEC on June 1, 2026 — standard Rule 135 language, no disclosed timeline, no named-executive quote about IPO rationale anywhere in our research.[^43] Mapped against the hire dates:

:::slope(left-label="Before S-1 filing (Jun 1)", right-label="After S-1 filing", unit=" hires")
| Hire | Before | After |
|------|--------|-------|
| Karpathy, Boyd, Nordeen | 3 | 0 |
| Jumper, Fontoura, Nelson, Carlson, Blomfield | 0 | 5 |
:::

Three of the eight hires — Karpathy, Boyd, Nordeen — joined weeks to months *before* the S-1 existed, which directly undercuts a clean "hired to dress up the prospectus" story for at least those three.[^2][^5][^6] But five of eight — Jumper, Fontoura, Nelson, Carlson, and Blomfield — were announced 16 to 42 days *after* the filing, a pattern that is at minimum consistent with pre-listing equity becoming a uniquely valuable recruiting tool in the run-up to a liquidity event.[^4][^7][^9][^11][^12] No banker, underwriter, or named Anthropic communications official was found on the record connecting the hires to IPO narrative-building; the clearest connective language we found ("a clear signal to investors of Anthropic's commitment to strengthening corporate governance," describing former Fed chair Ben Bernanke's July 9 appointment to Anthropic's oversight trust — a governance body, not the hiring cluster examined here) came from unnamed "market observers" relayed by a secondary aggregator, not a primary source.[^44] Scientific American's own coverage of Anthropic's June 4 RSI post independently raises the same suspicion in a different context: it notes the post landed "just days after Anthropic confidentially filed for an initial public offering," and quotes a skeptic calling such pronouncements a way to "draw regulatory scrutiny to the frontier" while the company keeps racing toward it — the same business-optics doubt this section applies to the hiring cluster, aimed instead at Anthropic's public safety messaging.[^30]

:::callout(kind=info, label=Framing)
Resource-acquisition and IPO-narrative-building are not mutually exclusive. A capital-flush, pre-listing company can plausibly want the same senior operators for genuine capability reasons *and* benefit from the recruiting-narrative side effect of a well-timed roster — Flor's essay treats these as a strict either/or when the timing evidence better supports both/and.
:::

## 09. What would break this thesis

The article's central claim — that Anthropic's hiring reflects a coherent talent-compute-customer flywheel rather than routine scaling and industry-wide competition — rests on inference layered onto a real and well-verified roster. Three things would most directly falsify it:

First, if Anthropic's own executives explicitly denied any coordinated hiring strategy, or if Jumper's mandate turns out — once finally disclosed — to be unrelated to the life-sciences buildout the pattern implies, the "deliberate flywheel" reading loses its strongest research-axis anchor. As of publication, Jumper's role remains genuinely undisclosed more than three weeks after his hire; that silence cuts against the flywheel reading, not for it — a company confident in a legible strategic narrative usually announces the mandate alongside the hire.

Second, if the compute-infrastructure hires (Boyd, Fontoura, Nordeen, Blomfield) prove to be reactive rather than strategic — driven by acute 2026 service reliability failures (Amodei's own 80x-vs-10x usage overshoot admission[^26]) rather than a forward-looking efficiency bet — then "flywheel" mischaracterizes what is closer to firefighting at scale.

Third, if the industry-wide comparison data (Section 07) is the more durable signal — if Anthropic's hiring pace, once measured over a longer window, converges toward what OpenAI, Google DeepMind, and Meta are also doing — then what looks distinctive in a ten-week snapshot is simply what frontier-lab hiring looks like in 2026, at any of the four major labs, and Anthropic's cluster is a sampling artifact of when Flor happened to look.

None of these fully break the underlying facts: eight real, senior, well-sourced hires joined Anthropic in ten weeks, spanning research, compute, and government relations, against a backdrop of run-rate revenue that quadrupled in five months[^45] and a compute buildout spanning at least four separate multi-billion-dollar hyperscaler and neocloud commitments.[^24][^8][^46] What they do complicate is the leap from "this pattern exists" to "this pattern proves a distinctive, deliberate recursive-self-improvement bet, and not an IPO narrative or an industry-wide scramble." The most defensible version of Flor's thesis is narrower than his own framing: Anthropic is real-world compute-constrained, is using Claude to accelerate its own research at a documented and accelerating rate, and is hiring accordingly — but so, on the comparison evidence, is most of the rest of the frontier-lab field.

:::references
- {id: 1, title: "Anthropic's hiring pattern reveals its bet on recursive self-improvement", url: "https://x.com/guilleflorvs/status/2076708631408464202", source: "X / Guillermo Flor", date: "2026-07-13"}
- {id: 2, title: "Karpathy joins Anthropic's pretraining team", url: "https://x.com/karpathy/status/2056753169888334312", source: "X / Andrej Karpathy", date: "2026-05-19"}
- {id: 3, title: "Nick Joseph on Karpathy's mandate", url: "https://x.com/nickevanjoseph/status/2056760504949842219", source: "X / Nick Joseph", date: "2026-05-19"}
- {id: 4, title: "OpenAI co-founder Andrej Karpathy joins Anthropic's pre-training team", url: "https://techcrunch.com/2026/05/19/openai-co-founder-andrej-karpathy-joins-anthropics-pre-training-team/", source: "TechCrunch", date: "2026-05-19"}
- {id: 5, title: "Anthropic poaches Microsoft executive to lead infrastructure", url: "https://www.bloomberg.com/news/articles/2026-04-07/anthropic-poaches-microsoft-executive-to-lead-infrastructure", source: "Bloomberg", date: "2026-04-07"}
- {id: 6, title: "xAI cofounder Ross Nordeen joins Anthropic to focus on compute", url: "https://www.datacenterdynamics.com/en/news/xai-cofounder-ross-nordeen-joins-anthropic-to-focus-on-compute-following-colossus-lease-deal/", source: "DataCenterDynamics", date: "2026-05-07"}
- {id: 7, title: "Microsoft's Azure Core CTO latest to join Anthropic", url: "https://www.datacenterdynamics.com/en/news/microsofts-azure-core-cto-latest-to-join-anthropic/", source: "DataCenterDynamics", date: "2026-06-17"}
- {id: 8, title: "Anthropic and Amazon expand compute partnership", url: "https://www.anthropic.com/news/anthropic-amazon-compute", source: "Anthropic", date: "2026-04-20"}
- {id: 9, title: "Jelani Nelson joins Anthropic", url: "https://x.com/minilek/status/2072322757908664728", source: "X / Jelani Nelson", date: "2026-07-01"}
- {id: 10, title: "Anthropic hires Berkeley CS chair Jelani Nelson, signaling new phase of AI race", url: "https://www.techtimes.com/articles/319500/20260702/anthropic-hires-berkeley-cs-chair-jelani-nelson-signaling-new-phase-ai-race.htm", source: "Tech Times", date: "2026-07-02"}
- {id: 11, title: "Monzo co-founder Tom Blomfield takes leave from Y Combinator to join Anthropic", url: "https://techfundingnews.com/monzo-co-founder-tom-blomfield-takes-leave-from-y-combinator-to-join-anthropic/", source: "Tech Funding News", date: "2026-07-13"}
- {id: 12, title: "Anthropic taps Microsoft/AWS veteran Teresa Carlson to lead public sector", url: "https://fedscoop.com/anthropic-taps-microsoft-aws-teresa-carlson-lead-public-sector/", source: "FedScoop", date: "2026-07-07"}
- {id: 13, title: "Teresa Carlson named Anthropic global head of public sector", url: "https://www.govconwire.com/articles/teresa-carlson-anthropic-public-sector-global-head", source: "GovConWire", date: "2026-07-07"}
- {id: 14, title: "Eureka Labs and LLM101n", url: "https://techopedia.com/eureka-labs-llm101n-edtech-by-andrej-karpathy", source: "Techopedia", date: "2024-07"}
- {id: 15, title: "Nobel laureate John Jumper departs Google DeepMind for Anthropic", url: "https://www.theinformation.com/briefings/nobel-laureate-john-jumper-departs-google-deepmind-anthropic", source: "The Information", date: "2026-06-23"}
- {id: 16, title: "Claude Science is Anthropic's newest flagship product", url: "https://www.technologyreview.com/2026/06/30/1139987/claude-science-is-anthropics-newest-flagship-product/", source: "MIT Technology Review", date: "2026-06-30"}
- {id: 17, title: "Anthropic releases Claude Science", url: "https://www.statnews.com/2026/06/30/anthropic-release-claude-science-ceo-dario-amodei/", source: "STAT News", date: "2026-06-30"}
- {id: 18, title: "Biology & Life Sciences roles", url: "https://job-boards.greenhouse.io/anthropic/jobs/5285250008", source: "Anthropic Greenhouse", date: "2026-07"}
- {id: 19, title: "Anthropic names former Microsoft Azure AI executive Eric Boyd as infrastructure chief", url: "https://redmondmag.com/articles/2026/04/07/anthropic-names-former-microsoft-azure-ai-executive-eric-boyd-as-infrastructure-chief.aspx", source: "Redmond Magazine", date: "2026-04-07"}
- {id: 20, title: "Anthropic's uniform Member of Technical Staff title convention", url: "https://www.trevorlasn.com/blog/anthropic-anti-talent-poaching-tactics", source: "trevorlasn.com", date: "2026"}
- {id: 21, title: "Higher usage limits for Claude and a compute deal with SpaceX", url: "https://www.anthropic.com/news/higher-limits-spacex", source: "Anthropic", date: "2026-05-06"}
- {id: 22, title: "Anthropic will pay xAI $1.25 billion per month for compute", url: "https://techcrunch.com/2026/05/20/anthropic-will-pay-xai-1-25-billion-per-month-for-compute/", source: "TechCrunch", date: "2026-05-20"}
- {id: 23, title: "Anthropic-Monzo founder Tom Blomfield", url: "https://sifted.eu/articles/anthropic-monzo-founder-tom-blomfield", source: "Sifted", date: "2026-07-13"}
- {id: 24, title: "Expanding our use of Google Cloud TPUs and services", url: "https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services", source: "Anthropic", date: "2025-10-23"}
- {id: 25, title: "Compute as an existential trade-off (CFO framing)", url: "https://www.anthropic.com/news/anthropic-amazon-compute", source: "Anthropic / press synthesis", date: "2026-04-20"}
- {id: 26, title: "Anthropic on usage limits amid explosive growth", url: "https://www.axios.com/2026/04/02/anthropic-usage-limits-openai", source: "Axios", date: "2026-04-02"}
- {id: 27, title: "GSA strikes OneGov deal with Anthropic", url: "https://www.gsa.gov/about-gsa/newsroom/news-releases/gsa-strikes-onegov-deal-with-anthropic-08122025", source: "GSA", date: "2025-08-12"}
- {id: 28, title: "Anthropic and the Department of Defense to advance responsible AI in defense operations", url: "https://www.anthropic.com/news/anthropic-and-the-department-of-defense-to-advance-responsible-ai-in-defense-operations", source: "Anthropic", date: "2025-07"}
- {id: 29, title: "When AI Builds Itself: Our Progress Toward Recursive Self-Improvement, and Its Implications", url: "https://www.anthropic.com/institute/recursive-self-improvement", source: "Anthropic Institute", date: "2026-06-04"}
- {id: 30, title: "Anthropic warns AI may soon begin recursive self-improvement", url: "https://www.scientificamerican.com/article/anthropic-warns-ai-may-soon-begin-recursive-self-improvement/", source: "Scientific American", date: "2026-06-07"}
- {id: 31, title: "100% of code at Anthropic and OpenAI is now AI-written, says Boris Cherny", url: "https://fortune.com/2026/01/29/100-percent-of-code-at-anthropic-and-openai-is-now-ai-written-boris-cherny-roon/", source: "Fortune", date: "2026-01-29"}
- {id: 32, title: "Anthropic's Boris Cherny doesn't write code by hand anymore", url: "https://fortune.com/2026/06/11/anthropic-claude-boris-cherny-doesnt-write-code-by-hand-anymore/", source: "Fortune", date: "2026-06-11"}
- {id: 33, title: "Jelani Nelson joins Anthropic — efficiency framing", url: "https://cryptobriefing.com/jelani-nelson-berkeley-anthropic/", source: "CryptoBriefing", date: "2026-07-01"}
- {id: 34, title: "Software progress (algorithmic efficiency tracker)", url: "https://epoch.ai/topics/software-progress", source: "Epoch AI", date: "2026"}
- {id: 35, title: "On DeepSeek and export controls", url: "https://darioamodei.com/post/on-deepseek-and-export-controls", source: "Dario Amodei", date: "2025-01-31"}
- {id: 36, title: "SemiAnalysis: Anthropic Q3 2026 profit to exceed $10 billion", url: "https://www.kucoin.com/news/flash/semianalysis-anthropic-q3-2026-profit-to-exceed-10-billion", source: "KuCoin News (relaying SemiAnalysis)", date: "2026-07-08"}
- {id: 37, title: "Inside the xAI exodus", url: "https://www.fastcompany.com/91531084/inside-the-xai-exodus", source: "Fast Company", date: "2026-06-19"}
- {id: 38, title: "AI companies poach professors from academia", url: "https://cryptobriefing.com/ai-companies-poach-professors-academia/", source: "CryptoBriefing", date: "2026-06-30"}
- {id: 39, title: "Meta's Thinking Machines Lab talent raid", url: "https://thenextweb.com/news/meta-thinking-machines-lab-talent-raid", source: "The Next Web", date: "2026"}
- {id: 40, title: "OpenAI hires Google Cloud/DeepMind corporate development lead", url: "https://www.theinformation.com/briefings/exclusive-openai-hires-executive-google-lead-m", source: "The Information", date: "2025-12-15"}
- {id: 41, title: "OpenAI expands government footprint with AWS deal", url: "https://techcrunch.com/2026/03/17/openai-expands-government-footprint-with-aws-deal/", source: "TechCrunch", date: "2026-03-17"}
- {id: 42, title: "Anthropic's top 10 hires of 2026", url: "https://techfundingnews.com/anthropic-top-10-hires/", source: "Tech Funding News", date: "2026-07"}
- {id: 43, title: "Anthropic files confidential draft S-1", url: "https://www.cnbc.com/2026/06/01/anthropic-ipo-s1-prospectus.html", source: "CNBC", date: "2026-06-01"}
- {id: 44, title: "Ben Bernanke joins Anthropic's Long-Term Benefit Trust", url: "https://finance.biggo.com/news/f0e90dac-d52e-4c9e-8453-dfbe429cf671", source: "BigGo Finance (relaying market commentary)", date: "2026-07-10"}
- {id: 45, title: "Anthropic raises $65B Series H at $965B valuation", url: "https://www.anthropic.com/news/series-h", source: "Anthropic", date: "2026-05-28"}
- {id: 46, title: "Anthropic signs $19B, 20-year lease for Kentucky data center with TeraWulf", url: "https://www.datacenterdynamics.com/en/news/anthropic-signs-19bn-20-year-lease-for-kentucky-data-center-with-terawulf/", source: "DataCenterDynamics", date: "2026-07-06"}
:::
