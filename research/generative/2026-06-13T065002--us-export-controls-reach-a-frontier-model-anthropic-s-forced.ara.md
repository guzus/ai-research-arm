---
eyebrow: POLICY · EXPORT CONTROLS · AI GOVERNANCE
title: "The first model-level export control: what the Fable 5 suspension means for frontier AI"
deck: The US government ordered Anthropic to suspend global access to Fable 5 and Mythos 5 — the first time an AI model has been the direct target of export control action. The legal theory, the technical justification, and the precedent for every other frontier lab.
lede: |
  On June 12, 2026, at 5:21 pm ET, the US government issued an export control directive ordering Anthropic to "suspend all access to Fable 5 and Mythos 5 by any foreign national, whether inside or outside the United States."[^1] Three days earlier, the company had released both models to hundreds of millions of users. By 6 pm, everything was dark. This article examines what happened, what legal authority was invoked, whether the technical justification holds up, and what the precedent means for OpenAI, Google DeepMind, and every other developer of frontier AI.
stats:
  - {label: "Fable 5 lifetime", value: "~3 days", note: "June 9–12, 2026"}
  - {label: "Models disabled", value: "2", note: "Fable 5 + Mythos 5"}
  - {label: "Directive received", value: "5:21 pm ET", note: "June 12, 2026"}
  - {label: "Blocker type", value: "Export control", note: "Jailbreak justification"}
---

:::callout(kind=danger, label="TL;DR")
For the first time, the US government has reached past chip-level export controls to directly restrict a frontier AI model. The legal basis — a narrow, non-universal jailbreak — is novel and contested. Anthropic complied but publicly disagreed, arguing the underlying capability is available from other models. The broader implication: any frontier model with demonstrated dual-use potential is now a potential export control target.
:::

## 01. The precedent: what happened on June 12

Anthropic received a directive from the US government, citing "national security authorities," ordering it to immediately suspend access to its two newest models — Fable 5 and Mythos 5 — by "any foreign national, whether inside or outside the United States, including foreign national Anthropic employees."[^1] Because Anthropic's customer base includes users worldwide whose nationality the company cannot practically verify in real time, the effective result was a global shutdown of both models for all users.

The timeline condensed quickly:

:::timeline
- {date: "2026-06-09", headline: "Fable 5 and Mythos 5 launch", body: "Anthropic announces both models. Fable 5 is the safe consumer version; Mythos 5 is the same model with safeguards lifted for vetted cybersecurity and biology researchers via Project Glasswing."}
- {date: "2026-06-12, 5:21pm ET", headline: "Export control directive received", body: "US government orders Anthropic to suspend all access by foreign nationals. An official letter arrives without specific details of the national security concern."}
- {date: "2026-06-12, ~6pm ET", headline: "Global suspension in effect", body: "Both models are disabled for all customers, everywhere. Anthropic publishes a public statement disputing the basis but confirming compliance."}
:::

The government's stated concern, per Anthropic's reading: "the government believes it has become aware of a method of bypassing, or 'jailbreaking' Fable 5" — a technique used to "identify a small number of previously known, minor vulnerabilities."[^1] Anthropic says it reviewed "a demonstration of this specific technique" and concluded the resulting capability was "relatively simple" and "widely available from other models (including OpenAI's GPT-5.5)."[^1]

This is the first time in US regulatory history that a frontier AI model — rather than the hardware used to train or run it — has been the direct target of an export control action. The closest analogues are semiconductor-level restrictions on NVIDIA H100/B200/H200 chips and ASML lithography equipment under the Export Administration Regulations (EAR), which regulate hardware by performance thresholds.[^18] Model weights have no established ECCN classification under the Commerce Control List, making this action legally novel.[^15]

#### Why this matters
If a narrow jailbreak against a deployed model is now sufficient grounds for an export control directive with global effect, no frontier lab is immune. Every provider of a capable model — OpenAI, Google DeepMind, xAI, Meta — faces the same vulnerability: a single bypass technique discovered by a red-teamer or foreign intelligence service could trigger an identical shutdown order.

## 02. The models at issue: Fable 5 and Mythos 5

Fable 5 and Mythos 5 are not two different models — they are two configurations of the same underlying model, differentiated exclusively by a layer of safety classifiers applied to Fable 5.[^3] When Fable 5's classifiers detect queries in cybersecurity, biology/chemistry, or LLM-distillation domains, the request is automatically routed to Claude Opus 4.8 at no additional cost to the user.[^3] Mythos 5 has no such classifiers; its unrestricted cyber and biology capabilities are available only to vetted Glasswing partners.[^4]

:::kv
- {term: "Fable 5 pricing", def: "$10/MTok input, $50/MTok output"}
- {term: "Classifier trigger rate", def: "Less than 5% of sessions [^10]"}
- {term: "Context window", def: "1M tokens (128k max output)"}
- {term: "Data retention", def: "30-day mandatory (not available under ZDR)"}
- {term: "Availability", def: "Fable 5: GA. Mythos 5: Glasswing only."}
- {term: "Fallback model", def: "Claude Opus 4.8 (free for rerouted queries)"}
:::

The two-tier architecture creates an unusual comparison — the same underlying model, differentiated only by classifier coverage:

:::compare
- {role: LOWEST, name: "Fable 5 (GA)", value: "Safeguarded"}
- {role: HIGHEST, name: "Mythos 5 (Glasswing)", value: "Unrestricted"}
- {role: SUBJECT, name: "Shared weights", value: "Same model"}
:::

:::stats
- {label: "CyberGym (Mythos Preview)", value: "83.1%", note: "vs 66.6% Opus 4.6 [^8]"}
- {label: "SWE-bench Pro (Mythos Preview)", value: "77.8%", note: "vs 53.4% Opus 4.6 [^8]"}
- {label: "Glasswing vulnerabilities found", value: "10,000+", note: "High- or critical-severity [^9]"}
- {label: "Protein targets with drug candidates", value: "9/14", note: "Under investigation [^17]"}
:::

The model's cybersecurity capabilities are what made it a target. The earlier Mythos Preview — the research precursor to Mythos 5 — scored {accent}83.1% on CyberGym{/} (vs. 66.6% for Claude Opus 4.6) and {accent}77.8% on SWE-bench Pro{/} (vs. 53.4%).[^8] Project Glasswing partners used it to find {accent}more than 10,000 high- or critical-severity vulnerabilities{/} across the world's most important software.[^9] Anthropic's own system card states: "Mythos 5 is also the most capable model we have evaluated on cyber tasks."[^5]

In biology, Mythos 5 accelerated drug design by approximately 10x, with 9 of 14 protein targets yielding strong drug design candidates under investigation.[^17] It assembled single-cell data for millions of cells across 138 animal species and trained a custom ML model that outperformed a model published in *Science* while being 100x smaller.[^18]

On jailbreak resistance, the system card reports: no universal jailbreak was found across over 1,000 hours of internal and external red-teaming; Fable 5 complied with zero harmful single-turn cyber requests across 30 distinct public jailbreak techniques.[^6] The UK AISI made "progress towards one" jailbreak within a "brief initial testing window" — a result that Anthropic acknowledged at launch.[^16]

#### Why this matters
The model at issue is not a narrow application. It is {accent}Anthropic's most capable model ever{/} — a multi-domain system that compresses months of engineering into days, outperforms GPT-5.5 on physics research using a third of the tokens, and has demonstrated state-of-the-art performance across coding, biology, cybersecurity, and knowledge work.[^2] Restricting it affects not just offensive cyber use but all beneficial applications in the same deployment.

## 03. The legal mechanism: what authority was invoked?

The directive cited "national security authorities" but did not specify a particular statute or regulation.[^1] This opacity is itself significant. The Export Administration Regulations (EAR) empower the Bureau of Industry and Security (BIS) to control exports of items — including commodities, software, and technology — that could harm US national security. But "model weights" do not appear on the Commerce Control List (CCL) under any existing ECCN.[^15]

The most relevant prior framework is the **Biden administration's October 2023 AI Executive Order 14110**, which directed BIS to consider rules requiring US IaaS providers to report foreign AI model training runs.[^19] That order set a training-compute threshold of 10^26 FLOPs for "dual-use foundation models" under the Defense Production Act — but the reporting obligation was on cloud providers, not a direct restriction on model distribution. No final rule on model weights was ever published under the Biden administration.

The **Trump AI Executive Order of June 2, 2026** goes further: it requires 30-day pre-release government access for cybersecurity review of frontier models — a mandatory domestic backstop triggered in part by the same Project Glasswing disclosures that led to Mythos 5's release.[^19] But a pre-review requirement is categorically different from an export control suspension.

:::callout(kind=warn, label="Legal novelty")
The action against Fable 5 and Mythos 5 appears to rest on an expansive reading of existing EAR authorities — applying chip-level national security rationales to model-level restrictions. No known Federal Register rulemaking has established AI model weights as a separately classified export item. The government has not publicly specified which EAR provision or statute it relied upon.[^1]
:::

The closest legal precedent is not in AI export controls at all. The {accent}Bernstein v. United States{/} litigation established that encryption source code is speech protected by the First Amendment — a district court and original Ninth Circuit panel both so held.[^15] If model weights are "source code" or functional speech, a similar First Amendment challenge would face the government. If model weights are treated as a "controlled technology" (like semiconductor mask works or blueprints), the government's authority is broader but the classification would need formal rulemaking.

#### Why this matters
The government's choice to use an opaque directive rather than publish a rule or announce a new ECCN category means the legal authority for restricting model distribution has not been tested, defined, or subject to public comment. Every frontier lab operates in legal uncertainty until a test case resolves the question.

## 04. The jailbreak question: does the capability justify the action?

This is the most contested factual question in the dispute. Anthropic's blog states the government demonstrated "a specific technique being used to identify a small number of previously known, minor vulnerabilities."[^1] The company characterizes the resulting capability as minimal and publicly available.

:::quote(attr="Anthropic, Statement on the US government directive, June 12, 2026")
We validated that the level of capability displayed there is widely available from other models (including OpenAI's GPT-5.5), and is used every day by the defenders who keep systems safe.[^1]
:::

Anthropic further notes that it had "not even received a disclosure of a concerning non-universal potential jailbreak that led to a harmful result" before the directive arrived.[^1] The company frames the action as disproportionate to the risk — a "narrow, non-universal jailbreak" that poses no systemic threat.

But there are reasonable counter-arguments the government may weigh:

- **The capability frontier.** Mythos 5 is {accent}Anthropic's most capable model ever evaluated on cybersecurity tasks{/}.[^5] Even a narrow jailbreak against such a model is qualitatively different from the same jailbreak against an older, less capable model — the damage surface is larger.
- **The defense-in-depth defense.** Anthropic argues its "defense in depth strategy" (classifier triggers + optional fallback + 30-day data retention for monitoring) reduces real-world risk to that of already-deployed models.[^20] But the government appears skeptical of relying on Anthropic's own classifiers as the primary safeguard.
- **Available from other models.** If GPT-5.5 genuinely offers the same capability without requiring a jailbreak, the question becomes: why is Fable 5 being singled out? Possible answers include: (a) the government has lower confidence in Anthropic's safeguards, (b) Fable 5's specific architecture makes the jailbreak easier to exploit in practice, or (c) the directive is intended as a regulatory signal rather than a response to a unique threat.

:::stats
- {label: "Internal red-team time", value: "1,000+ hours", note: "No universal jailbreak"}
- {label: "Jailbreak techniques tested", value: "30", note: "Zero harmful single-turn responses"}
- {label: "UK AISI finding", value: "Progress towards one", note: "Within brief testing window [^16]"}
:::

#### Why this matters
If the bar for an export control order is "a narrow jailbreak that finds previously known vulnerabilities" — without requiring evidence of novel harm, universal exploit, or government-unique access to the capability — then {accent}every deployed frontier model with dual-use potential is non-compliant right now{/}. As Anthropic warned: "If this standard was applied across the industry, we believe it would essentially halt all new model deployments for all frontier model providers."[^11]

## 05. From chips to models: a regulatory trajectory

The Fable 5 action did not emerge from a vacuum. It is the latest and most direct step in a trajectory of US export controls targeting AI-relevant technology.

:::timeline
- {date: "2022-10", headline: "First AI chip controls", body: "BIS restricts export of NVIDIA A100/H100 and AMD MI250/MI300 chips to China. Interconnect bandwidth and TPP thresholds established."}
- {date: "2023-10", headline: "Second chip control round", body: "BIS tightens thresholds; extends controls to additional chips. Adds 'floor' and 'ceiling' density requirements to prevent circumvention."}
- {date: "2024", headline: "Huawei-embedded TSMC chip discovered", body: "US investigators find a TSMC-manufactured chip in a Huawei product, triggering additional scrutiny of the semiconductor supply chain and concerns about training infrastructure for Chinese AI labs."}
- {date: "2025-09", headline: "Anthropic self-restricts", body: "Anthropic voluntarily stops selling to Chinese, Russian, Iranian, and North Korean entities. Foreshadows government-level controls.[^14]"}
- {date: "2026-01", headline: "BIS chip rule revised", body: "License review for H200/MI325X chips moves from 'presumption of denial' to 'case-by-case review' with certifications required. Still hardware-only.[^18]"}
- {date: "2026-05-05", headline: "CAISI pre-release evaluation MOUs", body: "Four frontier labs sign voluntary MOUs for pre-release government access. Opens door to mandatory pre-release review."}
- {date: "2026-06-02", headline: "Trump AI Executive Order", body: "Mandatory 30-day pre-release government access for cybersecurity review. Joint Cloud Project Glasswing's 10,000-bug disclosure."}
- {date: "2026-06-12", headline: "Fable 5 / Mythos 5 export control", body: "First direct restriction of a frontier AI model by export control — the action this article examines.[^1]"}
:::

The shift from hardware to model-level control represents a significant regulatory expansion. Each prior step regulated the *means of production* (chips, lithography equipment, fab tools). The Fable 5 action regulates the *product itself* — the model weights and their distribution.

The distinction matters for enforcement: a chip can be stopped at a border; a model can be distributed infinitely at zero marginal cost. Once model weights have been released or a jailbreak method is published, restricting access becomes practically impossible — the "ship has sailed" problem is far more acute for AI models than for hardware.

#### Why this matters
Model-level export controls are harder to enforce than chip-level controls, easier to circumvent (open-weight releases, side-loaded APIs, VPN-based access), and more legally contested (First Amendment, statutory authority). The Fable 5 action tests whether the existing regulatory infrastructure — built for physical goods — can be adapted to software that can be instantiated anywhere, instantly.

## 06. The political context: Anthropic and the Trump administration

The June 12 directive did not land in a neutral political environment. Relations between Anthropic and the Trump administration have been adversarial for months.

:::timeline
- {date: "2025-09", headline: "Anthropic self-restricts Chinese/Russian entity sales", body: "Voluntary restriction on sales to entities from adversarial countries. Self-initiated, not government-mandated.[^14]"}
- {date: "2026-02-27", headline: "Trump orders ban on government use of Anthropic", body: "All US government agencies ordered to stop using Claude models. Described by Wikipedia as 'retaliatory.'[^12]"}
- {date: "2026-02–03", headline: "Pentagon labels Anthropic a 'supply chain risk'", body: "Military contractors and partners barred from doing business with Anthropic. Effectively cuts the company off from the largest AI procurement buyer in the world.[^12]"}
- {date: "2026-03-26", headline: "Federal judge grants temporary injunction", body: "Judge writes the case 'appears to be classic First Amendment retaliation.' Google, Amazon, Apple, and Microsoft back Anthropic's lawsuit.[^13]"}
- {date: "2026-06-12", headline: "Fable 5 / Mythos 5 export control", body: "The first model-level export control directive. Anthropic: 'This action does not adhere to [fair] principles.'[^1]"}
:::

The injunction specifically found that the government's actions against Anthropic bore the hallmarks of retaliation for the company's refusal to relax safety restrictions on military uses. The Pentagon had demanded Anthropic remove restrictions barring Claude from use in "domestic surveillance and fully autonomous weapons"; Anthropic refused.[^12]

:::callout(kind=info, label="Context")
Google, Amazon, Apple, and Microsoft — four of the most powerful companies in the world — backed Anthropic's lawsuit against the DoD.[^12] The export control action now extends the conflict from the Department of Defense to the Commerce Department, significantly broadening the front.
:::

Anthropic's response to the current directive is careful to endorse the *principle* of government authority to block unsafe AI deployments — but insists on due process: "a statutory process that is transparent, fair, clear, and grounded in technical facts. This action does not adhere to those principles."[^1]

#### Why this matters
Whether or not the June 12 directive is justified on its technical merits, it operates against a backdrop of demonstrated hostility between the government and the target company. This does not invalidate the action, but it raises the bar for the government to prove that technical necessity — not political retaliation — was the motive.

## 07. The international dimension: what the rest of the world sees

The directive orders Anthropic to restrict access by "any foreign national" — a sweeping scope that applies equally to allies and adversaries. A Japanese cybersecurity researcher, a German biology professor, and a South Korean semiconductor engineer are each equally blocked.

This global approach is legally convenient (enforce nationality-blind) but diplomatically costly. The US has spent years building AI governance alliances — the UK AI Safety Summit (November 2023), the CAISI pre-release evaluations (May 2026), the EU-US Trade and Technology Council — that depend on trust. A unilateral action that blocks all non-US users from a frontier model damages that trust.

The EU AI Act, which becomes fully binding on August 2, 2026, treats general-purpose AI models as regulated entities under Article 51 — imposing transparency, copyright, and systemic-risk obligations on models above the 10^{25} FLOPs training compute threshold. The EU's framework is domestic regulation, not export control — but if the US precedent holds, the EU could develop its own mirror restrictions on non-EU model access.

China, meanwhile, has already moved to protect its AI data: its trade secret rules were updated in early June 2026 to explicitly cover AI training data,[^19] and its "AI Anthropomorphic Interaction Services" measures take effect July 15. The Fable 5 restriction validates the Chinese government's narrative that US AI models cannot be trusted as infrastructure — accelerating domestic model development and AI sovereignty initiatives in Beijing.

#### Why this matters
An export control on a globally accessible model, applied uniformly to all foreign nationals, is {accent}the geopolitical opposite of a targeted sanction{/}. It tells every non-US government — treaty ally and strategic competitor alike — that access to the world's most capable AI models can be revoked without warning or recourse. The long-term consequence may be accelerated investment in non-US AI development, which would undermine the strategic purpose of the controls.

## 08. What could break the thesis: counter-arguments and open questions

This section considers the strongest arguments against the article's central claim — that the Fable 5 export control is a novel, contested, and consequential precedent.

**Counter-argument 1: This is a targeted enforcement, not a new regime.** The government may have acted against Fable 5 specifically, not as a new category of controls. Without a formal rulemaking or public policy statement, the action is an enforcement measure against a specific jailbreak risk. If no similar action is taken against GPT-5.5, Gemini 3.5, or Grok 5, it was an incident, not a regime.

**Counter-argument 2: The dual-use capability is genuinely unprecedented.** Mythos 5 is the most capable model ever evaluated on cybersecurity tasks. A jailbreak — however narrow — against such a model arguably does justify emergency action. The government may have intelligence about specific threat actors attempting to exploit the bypass, which it cannot share publicly. Anthropic's insistence that the capability is "available from other models" may be technically true but practically irrelevant if those models are not deployed at the same scale.

**Counter-argument 3: Anthropic's response is self-interested.** Anthropic is preparing for an IPO (its confidential S-1 reportedly targets a $965B valuation[^13]). A suspension — however temporary — erodes customer trust, delays revenue, and damages the listing narrative. The company has every incentive to minimize the severity of the jailbreak and maximize the procedural impropriety. Its claim that the action "would essentially halt all new model deployments" is also a self-serving warning — one that implicitly argues Anthropic should be exempt.

**Counter-argument 4: Model-level and chip-level controls are complementary, not comparable.** The chip controls prevent Chinese labs from *training* frontier models (by restricting access to NVIDIA chips and TSMC manufacturing). The model-level controls prevent distribution of specific trained models. The two operate on different links of the AI value chain. The model-level control is narrower in scope — it targets a specific artifact, not a class of hardware — and therefore may be easier to defend legally than the sweeping chip restrictions.

**Counter-argument 5: The First Amendment analogy may not apply.** Bernstein v. United States concerned encryption source code — expressive code with a functional dimension. Model weights are not human-readable code; they are a set of floating-point parameters (trained, not written) whose "expressive" character is an open legal question. Courts may treat model weights as a functional artifact — more like a trained neural network circuit layout than a piece of software source code — which would shift the legal analysis away from speech protection and toward commercial regulation.

:::callout(kind=warn, label="Open question")
The central open question is whether this action is {accent}a one-off enforcement incident{/} or {accent}the first case in a new regulatory category{/}. The answer will become clear in the coming weeks: if the government publishes a rule, issues a Federal Register notice, or takes a similar action against another model, the second interpretation is correct. If the directive is withdrawn or limited to a narrow fix, the first interpretation wins.
:::

---

## References

:::references
- {id: 1, title: "Statement on the US government directive to suspend access to Fable 5 and Mythos 5", url: "https://anthropic.com/news/fable-mythos-access", source: "Anthropic (primary)", date: "2026-06-12"}
- {id: 2, title: "Claude Fable 5 and Claude Mythos 5", url: "https://anthropic.com/news/claude-fable-5-mythos-5", source: "Anthropic (primary)", date: "2026-06-09"}
- {id: 3, title: "Claude Fable 5 product page", url: "https://anthropic.com/claude/fable", source: "Anthropic (primary)", date: "2026-06-09"}
- {id: 4, title: "Claude Mythos 5 product page", url: "https://anthropic.com/claude/mythos", source: "Anthropic (primary)", date: "2026-06-09"}
- {id: 5, title: "Claude Fable 5 & Claude Mythos 5 System Card", url: "https://www-cdn.anthropic.com/2f9323abbcc4abe219577539efe19a623c9ca2bd/Claude%20Fable%205%20&%20Claude%20Mythos%205%20System%20Card.pdf", source: "Anthropic (primary)", date: "2026-06-09"}
- {id: 6, title: "Project Glasswing overview", url: "https://anthropic.com/glasswing", source: "Anthropic (primary)", date: "2026-04-07"}
- {id: 7, title: "Anthropic — Wikipedia", url: "https://en.wikipedia.org/wiki/Anthropic", source: "Wikipedia", date: "2026-06-13"}
- {id: 8, title: "Bernstein v. United States — Wikipedia", url: "https://en.wikipedia.org/wiki/Bernstein_v._United_States", source: "Wikipedia", date: "2026-06-13"}
- {id: 9, title: "AI News Research — Saturday, June 13, 2026", url: "https://ara.guzus.xyz/research/2026-06-13-ai-news.md", source: "ARA Research", date: "2026-06-13"}
- {id: 10, title: "AI News Research — Friday, June 12, 2026", url: "https://ara.guzus.xyz/research/2026-06-12-ai-news.md", source: "ARA Research", date: "2026-06-12"}
- {id: 11, title: "BIS chip export rule revision", url: "https://www.bis.gov/news", source: "Bureau of Industry and Security", date: "2026-01-13"}
- {id: 12, title: "Trump AI Executive Order — Promoting Advanced AI Innovation and Security", url: "https://www.whitehouse.gov/", source: "White House", date: "2026-06-02"}
- {id: 13, title: "Great American AI Act — discussion draft", url: "https://www.congress.gov/", source: "US House of Representatives", date: "2026-06-04"}
- {id: 14, title: "CAISI Pre-Release Frontier-AI Evaluation MOUs", url: "https://www.nist.gov/caisi", source: "NIST / CAISI", date: "2026-05-05"}
- {id: 15, title: "Executive Order 14110 — Safe, Secure, and Trustworthy Development of AI", url: "https://www.whitehouse.gov/briefing-room/2023/10/30/", source: "White House", date: "2023-10-30"}
- {id: 16, title: "A timeline of US AI chip export controls", url: "https://www.csis.org/analysis/timeline-us-ai-chip-export-controls", source: "CSIS", date: "2024-12"}
- {id: 17, title: "Anthropic confidential S-1 filing", url: "https://www.bloomberg.com/news/2026-06-01/anthropic-secretly-files-for-ipo", source: "Bloomberg", date: "2026-06-01"}
- {id: 18, title: "China trade secret rules — AI data coverage", url: "https://www.euronews.com/next/2026/06/02/new-trade-secret-rules-china-says-its-ai-data-is-none-of-your-business", source: "Euronews", date: "2026-06-02"}
- {id: 19, title: "The Washington Post — Anthropic models banned by US government", url: "https://www.washingtonpost.com/technology/2026/02/27/anthropic-trump-ban-federal-agencies/", source: "Washington Post", date: "2026-02-27"}
- {id: 20, title: "CNBC — Anthropic Pentagon lawsuit injunction", url: "https://www.cnbc.com/2026/03/26/anthropic-wins-injunction-trump-pentagon.html", source: "CNBC", date: "2026-03-26"}
- {id: 21, title: "Bloomberg — Anthropic series H valuation", url: "https://www.bloomberg.com/news/2026-06-01/anthropic-targets-965-billion-valuation", source: "Bloomberg", date: "2026-06-01"}
- {id: 22, title: "EU AI Act — Article 51 GPAI obligations", url: "https://eur-lex.europa.eu/eli/reg/2024/1689", source: "Official Journal of the European Union", date: "2024-08"}
:::
