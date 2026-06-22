---
eyebrow: ANALYSIS · AI LABS
title: "John Jumper leaves DeepMind for Anthropic: what a Nobel laureate's move actually signals"
deck: A confirmed hire with an unannounced job. What the AlphaFold founder's jump tells us about Anthropic's science bet — and what it doesn't.
domain: general
lede: |
  On June 19, 2026, John Jumper — co-creator of AlphaFold and a 2024
  Nobel laureate in Chemistry — posted that he was leaving Google
  DeepMind after nearly nine years to join Anthropic. The post drew
  more than 14,000 likes and a warm reply from his Nobel co-winner.
  It also disclosed no title, no start date, and no mandate. That gap
  between the symbolism of the hire and the silence about the job is
  the whole story: it is simultaneously the loudest validation yet of
  Anthropic's "AI for science" thesis and a hire we know almost
  nothing concrete about. This is an attempt to separate the signal
  from the projection.
stats:
  - {label: Announced, value: "Jun 19, 2026"}
  - {label: DeepMind tenure, value: "~9 yrs"}
  - {label: Nobel, value: "2024", note: Chemistry}
  - {label: Anthropic valuation, value: $965B, note: "Series H, May 2026"}
  - {label: Disclosed role, value: None}
---

:::callout(kind=info, label="The short version")
- {accent}It's real.{/} Jumper announced the move himself; his DeepMind boss Demis Hassabis publicly thanked him minutes later.[^1,5]
- {accent}But the job is undefined.{/} Neither Anthropic nor Jumper has named a role, and Jumper says he will "recharge" before starting.[^1,4]
- {accent}It lands in a pattern.{/} It came one day after Gemini co-lead Noam Shazeer left Google for OpenAI, and a month after OpenAI co-founder Andrej Karpathy joined Anthropic.[^13,15]
- {accent}Anthropic's science program is resourced, not vapor{/} — a launched product, named institutional partners, grants, an acquisition, and a founder thesis.[^19,16,17,18]
- {accent}The hard part isn't talent.{/} AlphaFold rested on decades of open structural data and specialized, non-LLM architecture. A single hire doesn't transfer that.[^9]
:::

## 01. The move, in his own words

The primary source is a single tweet. "After nearly 9 years, I have decided to leave Google DeepMind and join Anthropic (after taking some time to recharge)," Jumper wrote on June 19, 2026, crediting Hassabis with "a real chance letting me lead the AlphaFold team just six months after finishing my PhD."[^1] The post is the most-engaged artifact in the story — more than 14,000 likes as of June 22[^1] — and Hassabis quote-tweeted a cordial send-off within six minutes: "Thanks John for an extraordinary partnership… What we achieved with AlphaFold changed the world."[^5] Both companies confirmed the departure to the press.[^2,4]

What is *not* in the announcement matters as much as what is. There is no title, no start date, and no description of what Jumper will build; reporting is explicit that "neither Anthropic nor Jumper has disclosed what role he will take."[^4] As of his announcement, Anthropic's own account had posted no welcome, and no Dario or Daniela Amodei statement surfaced.[^4] A handful of outlets and anonymous accounts floated specific titles such as "Chief Scientist," but those trace to zero-engagement commentary, not to Anthropic.[^3,4]

:::statement(attr="ARA Research")
This is a confirmed intent-to-join with an unannounced job — not a hire who has started with a mandate. Read the symbolism; discount the specifics.
:::

The counterpoint to over-reading any of this is the timing. Jumper's exit came one day after Noam Shazeer, a Gemini co-lead and "Attention Is All You Need" co-author, said he was leaving Google for OpenAI — two landmark departures in 48 hours, but in *different* directions.[^13] That is a useful caution: a star move is an event, not a destiny. Why it matters: the headline writes itself as "Anthropic wins science," but the verifiable facts support only "a Nobel laureate intends to join Anthropic, eventually, to do something not yet named."

## 02. Who Jumper is, and what AlphaFold actually was

Jumper is not a generic prestige hire. He has a PhD in theoretical chemistry from the University of Chicago (2017), worked at D. E. Shaw Research on molecular dynamics before that, and was made to lead DeepMind's protein-folding team within months of finishing his doctorate.[^12,1] He left as a Director after nearly nine years.[^1,12]

:::kv
- {term: PhD, def: "Theoretical chemistry, University of Chicago (2017)"}
- {term: Before DeepMind, def: "D. E. Shaw Research (molecular dynamics)"}
- {term: Role at exit, def: "Director, Google DeepMind"}
- {term: Signature work, def: "AlphaFold 1, 2 and 3 (lead/core contributor)"}
- {term: Recognition, def: "2024 Nobel Prize in Chemistry (shared)"}
:::

The 2024 Nobel Prize in Chemistry was split: one half to David Baker for computational protein design, the other half jointly to Hassabis and Jumper "for protein structure prediction."[^6] AlphaFold2 (Nature, 2021) effectively solved the 50-year problem of predicting a protein's 3D shape from its amino-acid sequence; AlphaFold3 (Nature, 2024), co-developed with DeepMind's drug-discovery spinout Isomorphic Labs, extended that to complexes of proteins with DNA, RNA and small molecules.[^8,10] The impact figures are genuinely large — and worth stating *currently*, not from the Nobel-era press kit.

:::stats
- {label: "Researchers (Nov 2025)", value: "3M+"}
- {label: Countries, value: "190+"}
- {label: Predicted structures, value: "200M+"}
- {label: "CASP14 median GDT", value: "92.4"}
:::

By DeepMind's own November 2025 accounting, the AlphaFold database had been used by over 3 million researchers in more than 190 countries and holds over 200 million predicted structures.[^7] (Many secondary write-ups still cite the stale "2 million scientists" figure from October 2024 — use the current one.[^6,7]) The accuracy leap was decisive: AlphaFold's median GDT score jumped from 58.9 at the CASP13 benchmark in 2018 to 92.4 at CASP14 in 2020, a result the field read as "solved."[^9]

:::slope(left-label="CASP13 · 2018", right-label="CASP14 · 2020", unit=GDT)
| AlphaFold median GDT | CASP13 · 2018 | CASP14 · 2020 |
|----------------------|---------------|---------------|
| AlphaFold            | 58.9          | 92.4          |
:::

Here is the first-principles caveat that shadows the entire "Jumper changes everything" narrative: AlphaFold was a *team plus data plus compute* achievement, not a lone-genius one. The AlphaFold2 paper carries dozens of authors, and it was trained on a Protein Data Bank snapshot of roughly 170,000 experimentally determined structures — decades of open, community-deposited experimental work.[^9] Jumper carries irreplaceable tacit knowledge of how to build such a system. He does not carry the Protein Data Bank. Why it matters: the asset that made AlphaFold possible largely stayed in public repositories and at DeepMind.

## 03. The war for AI's scarcest input

Strip away the science angle and the move is also a data point in a brutal talent market. The clearest evidence the flow is real — and directional — comes from VC firm SignalFire's 2025 talent report, which found DeepMind engineers were nearly 11 times more likely to leave for Anthropic than the reverse, and put Anthropic's two-year retention at 80%, ahead of DeepMind and OpenAI.[^14]

:::rank-list
- {label: Anthropic, value: "80%", pct: 100, highlight: true}
- {label: Google DeepMind, value: "78%", pct: 97}
- {label: OpenAI, value: "67%", pct: 84}
:::

Jumper is the brightest name in a documented Anthropic hiring run: OpenAI co-founder Andrej Karpathy joined its pre-training team on May 19, 2026, a hire confirmed by TechCrunch and CNBC rather than viral rosters.[^15] The compensation backdrop is extraordinary — OpenAI alone reportedly pays around $1.5 million in average stock-based compensation per employee, the highest of any startup on record, a number that exists to *keep* people, not just attract them.[^41] No Jumper package was disclosed; pre-IPO Anthropic equity is the obvious unstated lever, but it is genuinely unstated, and should be labeled as inference.[^1]

The honest counter-pressure here is that the "everyone is fleeing Google" frame is half-true. The very same week, Shazeer went to *OpenAI*, not Anthropic, and Shazeer's own career — Google to Character.AI to a reported $2.7B return to Google to OpenAI — is a vivid reminder that elite-AI moves are noisy and reversible.[^13] Why it matters: retention ratios describe a trend; they do not make any single hire permanent or productive.

## 04. Anthropic's science bet, itemized

The strongest reason to take the hire seriously is that Jumper would not be parachuting into a slide deck. Anthropic has been building a science program with dated, named artifacts for more than a year, and the most useful thing an analyst can do is list them rather than gesture at them.

:::timeline
- {date: 2024-10, headline: "Machines of Loving Grace", body: "Amodei publishes the biology-compression thesis."}
- {date: 2025-05, headline: "AI for Science Program", body: "Up to $20k in API credits per researcher."}
- {date: 2025-10, headline: "Claude for Life Sciences", body: "Sonnet 4.5 plus lab-data connectors."}
- {date: 2026-02, headline: "Allen Institute + HHMI", body: "Founding institutional partners."}
- {date: 2026-04, headline: "Coefficient Bio acquired", body: "~$400M all-stock; computational-biology talent."}
- {date: 2026-06, headline: "Jumper announces", body: "A Nobel laureate, role undisclosed."}
:::

The thesis is the founder's. In his October 2024 essay "Machines of Loving Grace," Dario Amodei argued AI could "compress the progress that human biologists would have achieved over the next 50-100 years into 5-10 years," reframing AI as "a virtual biologist" rather than a data-analysis tool.[^19] The operational layer followed: an AI for Science Program offering researchers up to $20,000 in API credits (May 2025); Claude for Life Sciences on Sonnet 4.5 with connectors to Benchling, 10x Genomics and PubMed (October 2025); and founding research partnerships with the Allen Institute and Howard Hughes Medical Institute's Janelia campus (February 2026).[^18,16,17] In April 2026 Anthropic acquired Coefficient Bio, an eight-month-old startup of fewer than ten computational biologists, in an all-stock deal reported at roughly $400 million.[^40] It has also published genuine bench evaluation — on its BioMysteryBench test, Claude Opus 4.6 scored 77.4% on human-solvable bioinformatics tasks (though only 23.5% on human-difficult ones).[^31]

:::callout(kind=warn, label="The tension Jumper inherits")
Anthropic is the lab that activated ASL-3 safeguards with Claude Opus 4 in May 2025 *specifically* to limit chemical- and biological-weapons misuse.[^20] Building aggressively capable biology models while constraining biological capability is a real, structural friction — not a talking point. A Nobel biologist joins a company whose own safety policy is designed to slow parts of biology down.
:::

The counterpoint to the build-out is timing and attribution. The program predates Jumper and runs without him: Anthropic's "Briefing: AI for Science" event on June 30, 2026 features executives from Novartis, Bristol Myers Squibb and Genentech — and does not list Jumper at all.[^32] Why it matters: the bet is real and resourced, but it was a bet *before* the hire, which means the hire is an accelerant and a credibility stamp, not the origin of the strategy.

## 05. Can an LLM lab actually do AlphaFold-class science?

This is the question the celebratory coverage skips, and it is the one that most determines whether the hire pays off. AlphaFold is not a large language model. Its architecture — an Evoformer trunk operating over multiple-sequence alignments and pairwise representations, feeding an explicit 3D structure module — is a geometric model trained on evolutionary and structural data, a fundamentally different object from a next-token text transformer like Claude.[^9] AlphaFold3 added a diffusion component; none of it is "predict the next word."[^11]

So what is Anthropic's actual capability today? On the public evidence, it is general Claude models plus tool connectors and agents — not a native specialized scientific model. The Claude for Life Sciences launch is built around Claude acting as a research assistant wired into external platforms; it makes no mention of structure prediction.[^16] That points to a specific bet: the emerging design pattern in AI-for-biology is an LLM *agent that orchestrates and calls* specialized models like AlphaFold as tools, rather than one model that does folding itself.[^16] On that reading, Jumper's job is plausibly to build new specialized science capability inside an LLM-first shop — which is closer to a green-field than a transplant.

:::callout(kind=info, label="What the AlphaFold playbook actually required")
- A large, curated public dataset — the ~170,000-structure Protein Data Bank.[^9]
- A shared, adversarial benchmark — the biennial CASP competition.[^9]
- Years of integrated effort — roughly two years from CASP13 to a "solved" CASP14, atop earlier foundational work.[^9]
- Dedicated compute and a large multi-disciplinary team.[^9]
:::

The honest two-sided read: the AlphaFold recipe is *portable* — the data (PDB), the evolutionary inputs, and the CASP benchmark are public — but each scientific field has its own data bottleneck, and Anthropic has not shown a structural-biology data pipeline of its own. Its Coefficient Bio acquisition and reported wet labs may begin to close that gap, but a ten-person agentic-biology startup does not supply PDB-scale structural training data.[^40] Why it matters: hiring the chef does not stock the pantry. The bet only works if Anthropic builds or buys the specialized data and infrastructure layer, and that is a multi-year program, not a signing.

## 06. The money: who can actually afford the bet

Anthropic can clearly afford to fund a long-horizon science effort, and the trajectory is vertical. Its post-money valuation climbed from $183B (Series F, September 2025) to $380B (Series G, February 2026) to $965B (Series H, May 2026) — a roughly five-fold step-up in nine months, alongside a confidential IPO filing.[^23,22,21] Revenue run-rate scaled on a similar curve, from about $1B in early 2025 to a reported $14B by February 2026.[^22]

:::line-chart(title="Anthropic revenue run-rate", subtitle="USD billions, run-rate snapshots", y-unit=$)
x: 2025-01,2025-08,2025-12,2026-02
Run-rate: 1,5,9,14
:::

There is a concentration caveat buried in that growth: the engine is coding, not biology. Claude Code's run-rate alone exceeded $2.5B by February 2026, and Anthropic's incentives, compute and revenue overwhelmingly point at enterprise agents.[^22] Science is, today, an investment center funded by coding revenue — which makes a Nobel science hire a statement about where the *next* frontier is, not where the money currently is.

Then there is the comparison that should temper any "Anthropic is winning science" triumphalism: the resources of the company Jumper just left. Alphabet's FY2025 research-and-development expense was $61.1 billion — by itself larger than Anthropic's entire annualized revenue — and Alphabet guided 2026 capital expenditure to $175-185 billion.[^24,25] The market, for its part, treated the twin departures as noise: GOOGL did not sell off, rising about 1.17% on June 19 and finishing the week up.[^33] Over the prior year, Alphabet stock had nearly doubled.[^42]

:::line-chart(title="GOOGL did not flinch", subtitle="Monthly close, USD (Yahoo Finance)", y-unit=$)
x: 2025-07,2025-08,2025-09,2025-10,2025-11,2025-12,2026-01,2026-02,2026-03,2026-04,2026-05,2026-06
GOOGL: 191.9,212.91,243.1,281.19,320.18,313.0,338.0,311.76,287.56,384.8,380.34,368.03
:::

Why it matters: Anthropic has enough capital to make a real science bet, but it is funding science off a single, coding-driven P&L, while Alphabet funds DeepMind and its separately capitalized drug spinout, Isomorphic Labs, out of operating cash flow. On raw resources, the incumbent is not weakened by losing one Director.

## 07. What a Nobel actually buys

If the science transfer is hard and the money favors the incumbent, why is this hire still a coup? Because in life sciences, a Nobel Prize is the single most legible, hardest-to-fake credibility signal there is — and credibility is the currency of business development. A Nobel laureate on the org chart compresses due diligence for skeptical pharma scientific-advisory boards and doubles as a talent magnet. The pattern is visible across the field: David Baker, the third 2024 chemistry laureate, anchored the drug-design startup Xaira Therapeutics, which launched with roughly $1 billion.[^39] And the AlphaFold lineage has *already* converted credibility into commerce — Isomorphic Labs signed deals with Eli Lilly and Novartis worth nearly $3 billion in potential milestones, raised $600M externally in 2025 and a reported $2.1B round in 2026.[^26,27,28]

But the commercial reality should puncture the hype, and this is where most coverage fails. The "AI for science" market is reported as one number when it is really three, with a roughly ten-fold spread that is a scope artifact, not a measurement disagreement.

:::bar-chart(title="Three different 'AI for science' markets, reported as one", subtitle="USD billions, 2024-2025 estimates", orientation=horizontal, value-unit=$, value-suffix=B)
categories: AI drug-discovery tools, AI across life sciences, McKinsey annual value potential
Estimate: 2, 17, 85
:::

The defensible figure for AI drug-discovery *software* spend today is roughly $1-3 billion; "AI across all life sciences" runs to perhaps $13-21 billion; and McKinsey's widely cited "$60-110 billion" is an annual *economic value potential* spread across an entire industry, not an addressable market.[^38,35] More sobering still: no AI-designed drug has yet won FDA approval, Isomorphic itself slipped its first-in-human timeline from end-2025 to end-2026, and 2025 brought shutdowns and layoffs among AI drug-discovery startups.[^29,35] Even AlphaFold3's headline result — a 58% ligand-binding success rate versus 24% for the classical docking tool AutoDock Vina — is a prediction-accuracy gain, not a cure.[^11]

:::bars
- {label: "AlphaFold3 ligand binding", value: "58%", pct: 58}
- {label: "AutoDock Vina", value: "24%", pct: 24}
:::

Why it matters: the prize buys negotiating leverage, recruiting gravity and a halo of seriousness — all real and valuable to a pre-IPO Anthropic. It does not buy an approved drug, and the gap between "predict a structure" and "ship a medicine" is measured in years and failed trials. The state is also putting money behind the same thesis: the US DOE's Genesis Mission committed over $320 million to AI-for-science in December 2025 with Anthropic, OpenAI and DeepMind as partners, and NIH's Bridge2AI invested $130 million — so credibility now also unlocks government doors.[^36,37,44]

## 08. What would break this thesis

The strongest version of this article is the one that tries hardest to falsify its own headline. Here is the disconfirming case, taken seriously.

First, the load-bearing fact is an absence. The role is undisclosed and Jumper is taking time off before he starts, so the entire "Anthropic will win science" reading rests on a hire with no announced mandate and no immediate output.[^4,1] Second, the science may not port: AlphaFold's moat was data and a specialized, non-LLM architecture, and Anthropic has shown a general-LLM-plus-agents capability, not a structure-prediction pipeline.[^9,16] Third, the incumbent's bench is deep — DeepMind's science portfolio spans GNoME (2.2 million predicted crystals), AlphaGenome, AlphaProteo and weather forecasting, and Alphabet's drug effort lives in Isomorphic Labs, where Jumper did *not* work — so losing one Director is a reputational hit, not an operational one.[^34] Fourth, the field is structurally over-hyped: a systematic review by physicist Nick McGreivy found 79% of surveyed AI-for-science papers leaned on weak baselines, and even AlphaFold is best understood as a tool that complements experiment rather than replacing it.[^35,43]

:::callout(kind=danger, label="The bear case in one line")
A confirmed hire with an unannounced job, a subject on sabbatical, a company whose revenue and compute point at coding, and a safety policy designed to slow biology down — over-reading this as "Anthropic wins science" is exactly the AI-for-science hype the evidence warns against.[^4,20,35]
:::

And yet the move resists pure dismissal, which is itself a finding. An adversarial pass over the three load-bearing claims — that the hire is real, that Anthropic's science program is genuinely resourced, and that a Nobel confers outsized business-development leverage — surfaced no credible contradicting source on any of them; the only "skeptical" reactions found were anonymous trolls.[^4] The most defensible synthesis is the unglamorous one: this is a high-conviction, long-horizon bet by a company that has clearly decided science is its next frontier, made credible by exactly the person who proved the frontier exists — and it will take years, specialized data, and at least one shipped scientific result before anyone can say it worked. Watch for three tells: a named role and mandate for Jumper; a specialized (non-LLM) science model or dataset effort; and a first concrete scientific result with Jumper's name on it. Until then, the honest verdict is that Anthropic bought the loudest possible signal that it is serious — and signals are not yet science.

:::references
- {id: 1, title: "A bit of news… leaving Google DeepMind and join Anthropic", url: "https://x.com/JohnJumperSci/status/2068001285173834106", source: "John Jumper (X)", date: "2026-06-19"}
- {id: 2, title: "John Jumper to leave Google DeepMind for Anthropic", url: "https://www.cnbc.com/2026/06/19/john-jumper-to-leave-google-deepmind-for-anthropic.html", source: CNBC, date: "2026-06-19"}
- {id: 3, title: "Nobel laureate John Jumper is leaving DeepMind for rival Anthropic", url: "https://techcrunch.com/2026/06/20/nobel-laureate-john-jumper-is-leaving-deepmind-for-rival-anthropic/", source: TechCrunch, date: "2026-06-20"}
- {id: 4, title: "John Jumper is leaving Google DeepMind for Anthropic after nearly nine years", url: "https://thenextweb.com/news/john-jumper-nobel-deepmind-leaves-anthropic-alphafold", source: "The Next Web", date: "2026-06-19"}
- {id: 5, title: "Thanks John for an extraordinary partnership", url: "https://x.com/demishassabis/status/2068002732250640603", source: "Demis Hassabis (X)", date: "2026-06-19"}
- {id: 6, title: "The Nobel Prize in Chemistry 2024 — press release", url: "https://www.nobelprize.org/prizes/chemistry/2024/press-release/", source: NobelPrize.org, date: "2024-10-09"}
- {id: 7, title: "AlphaFold: five years of impact", url: "https://deepmind.google/blog/alphafold-five-years-of-impact/", source: "Google DeepMind", date: "2025-11-25"}
- {id: 8, title: "Highly accurate protein structure prediction with AlphaFold", url: "https://www.nature.com/articles/s41586-021-03819-2", source: "Nature 596", date: "2021-07-15"}
- {id: 9, title: "AlphaFold2 (Jumper et al.) — full text", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC8371605/", source: "Nature / PMC", date: "2021-07-15"}
- {id: 10, title: "Accurate structure prediction of biomolecular interactions with AlphaFold 3", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11168924/", source: "Nature / PMC", date: "2024-05-08"}
- {id: 11, title: "AlphaFold 3 predicts the structure and interactions of all of life's molecules", url: "https://blog.google/innovation-and-ai/products/google-deepmind-isomorphic-alphafold-3-ai-model/", source: "Google / DeepMind", date: "2024-05-08"}
- {id: 12, title: "John Jumper — Royal Society biography", url: "https://royalsociety.org/people/john-jumper-37403/", source: "Royal Society", date: "2025-01-01"}
- {id: 13, title: "Google Gemini co-lead Noam Shazeer leaves for OpenAI", url: "https://www.cnbc.com/2026/06/18/google-gemini-co-lead-noam-shazeer-leaves-for-openai.html", source: CNBC, date: "2026-06-18"}
- {id: 14, title: "How Anthropic wins the AI talent war (retention data)", url: "https://www.signalfire.com/blog/anthropic-talent-retention", source: "SignalFire", date: "2026-01-01"}
- {id: 15, title: "OpenAI co-founder Andrej Karpathy joins Anthropic's pre-training team", url: "https://techcrunch.com/2026/05/19/openai-co-founder-andrej-karpathy-joins-anthropics-pre-training-team/", source: TechCrunch, date: "2026-05-19"}
- {id: 16, title: "Claude for Life Sciences", url: "https://www.anthropic.com/news/claude-for-life-sciences", source: Anthropic, date: "2025-10-20"}
- {id: 17, title: "Anthropic partners with the Allen Institute and HHMI", url: "https://www.anthropic.com/news/anthropic-partners-with-allen-institute-and-howard-hughes-medical-institute", source: Anthropic, date: "2026-02-02"}
- {id: 18, title: "AI for Science Program", url: "https://www.anthropic.com/news/ai-for-science-program", source: Anthropic, date: "2025-05-05"}
- {id: 19, title: "Machines of Loving Grace", url: "https://www.darioamodei.com/essay/machines-of-loving-grace", source: "Dario Amodei", date: "2024-10"}
- {id: 20, title: "Activating ASL-3 protections", url: "https://www.anthropic.com/news/activating-asl3-protections", source: Anthropic, date: "2025-05-22"}
- {id: 21, title: "Anthropic raises $65B Series H at $965B post-money valuation", url: "https://www.anthropic.com/news/series-h", source: Anthropic, date: "2026-05-28"}
- {id: 22, title: "Anthropic raises $30B Series G at $380B post-money valuation", url: "https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation", source: Anthropic, date: "2026-02-12"}
- {id: 23, title: "Anthropic raises Series F at $183B post-money valuation", url: "https://www.anthropic.com/news/anthropic-raises-series-f-at-usd183b-post-money-valuation", source: Anthropic, date: "2025-09-02"}
- {id: 24, title: "Alphabet R&D expense (XBRL companyconcept, 10-K FY2025)", url: "https://data.sec.gov/api/xbrl/companyconcept/CIK0001652044/us-gaap/ResearchAndDevelopmentExpense.json", source: "SEC EDGAR", date: "2026-02-05"}
- {id: 25, title: "Alphabet resets the bar for AI infrastructure spending", url: "https://www.cnbc.com/2026/02/04/alphabet-resets-the-bar-for-ai-infrastructure-spending.html", source: CNBC, date: "2026-02-04"}
- {id: 26, title: "Isomorphic stacks two new deals with Lilly, Novartis worth nearly $3B", url: "https://www.fiercebiotech.com/biotech/alphabets-isomorphic-stacks-two-new-deals-lilly-novartis-worth-nearly-3b-ahead-buzzy-jpm", source: "Fierce Biotech", date: "2024-01-08"}
- {id: 27, title: "Isomorphic Labs announces $600M external investment round", url: "https://www.isomorphiclabs.com/articles/isomorphic-labs-announces-600m-external-investment-round", source: "Isomorphic Labs", date: "2025-03-31"}
- {id: 28, title: "Isomorphic Labs raises $2.1 billion", url: "https://www.rdworldonline.com/alphabet-spinoff-isomorphic-labs-raises-2-1-billion-in-quest-to-solve-all-disease-with-ai-based-drug-discovery-tools/", source: "R&D World", date: "2026-05-12"}
- {id: 29, title: "Google-backed AI drug discovery firm delays first human trials", url: "https://finance.yahoo.com/news/google-backed-ai-drug-discovery-195423147.html", source: "Reuters / Yahoo", date: "2026-01-20"}
- {id: 31, title: "Evaluating Claude for bioinformatics with BioMysteryBench", url: "https://www.anthropic.com/research/Evaluating-Claude-For-Bioinformatics-With-BioMysteryBench", source: Anthropic, date: "2026-04-29"}
- {id: 32, title: "The Briefing: AI for Science (virtual event)", url: "https://www.anthropic.com/events/the-briefing-ai-for-science-virtual-event", source: Anthropic, date: "2026-06-30"}
- {id: 33, title: "Alphabet finishes up in short week after two AI heads exit", url: "https://ts2.tech/en/alphabet-finishes-up-in-short-week-after-google-sees-two-ai-heads-exit/", source: "TS2", date: "2026-06-19"}
- {id: 34, title: "Millions of new materials discovered with deep learning (GNoME)", url: "https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/", source: "Google DeepMind", date: "2023-11-29"}
- {id: 35, title: "I got fooled by AI-for-science hype — here's what it taught me", url: "https://www.understandingai.org/p/i-got-fooled-by-ai-for-science-hypeheres", source: "Nick McGreivy / Understanding AI", date: "2025-05-19"}
- {id: 36, title: "Energy Department advances investments in AI for science (Genesis Mission)", url: "https://www.energy.gov/articles/energy-department-advances-investments-ai-science", source: "US DOE", date: "2025-12-10"}
- {id: 37, title: "Anthropic and the DOE Genesis Mission", url: "https://www.anthropic.com/news/genesis-mission-partnership", source: Anthropic, date: "2025-12-18"}
- {id: 38, title: "AI in Life Sciences / Drug Discovery market", url: "https://www.marketsandmarkets.com/Market-Reports/ai-in-life-science-market-1239.html", source: "MarketsandMarkets", date: "2025"}
- {id: 39, title: "HHMI's David Baker wins 2024 Nobel Prize in Chemistry", url: "https://www.hhmi.org/hhmi-david-baker-wins-2024-nobel-chemistry", source: HHMI, date: "2024-10-09"}
- {id: 40, title: "Anthropic acquires Coefficient Bio for $400M in all-stock deal", url: "https://www.tekedia.com/anthropic-acquires-coefficient-bio-for-400m-in-an-all-stock-deal/", source: Tekedia, date: "2026-04-03"}
- {id: 41, title: "OpenAI's record million-dollar equity compensation", url: "https://fortune.com/2026/02/18/openai-chatgpt-creator-record-million-dollar-equity-compensation-ai-tech-talent-war-career-retention-sam-altman-millionaire-staff/", source: Fortune, date: "2026-02-18"}
- {id: 42, title: "GOOGL historical prices (1y, monthly)", url: "https://finance.yahoo.com/quote/GOOGL/history", source: "Yahoo Finance", date: "2026-06-19"}
- {id: 43, title: "How AI revolutionized protein science, but didn't end it", url: "https://www.quantamagazine.org/how-ai-revolutionized-protein-science-but-didnt-end-it-20240626/", source: "Quanta Magazine", date: "2024-06-26"}
- {id: 44, title: "NIH launches Bridge2AI program ($130M)", url: "https://www.nih.gov/news-events/news-releases/nih-launches-bridge2ai-program-expand-use-artificial-intelligence-biomedical-behavioral-research", source: NIH, date: "2022-09-13"}
:::
