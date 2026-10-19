---
eyebrow: POLICY · SUPPLY CHAIN · DEEPSEEK
title: "Six words carry the DeepSeek ban: what DHS's first FASCSA order on an AI lab actually reaches"
deck: "The order goes past DeepSeek's app to \"third-party products and services developed using DeepSeek implementations.\" Those six words never define \"implementation,\" and no vendor can prove the absence of a teacher model."
domain: policy
lede: |
  On October 19, 2026, the Department of Homeland Security put a six-page notice on public inspection. It disclosed that the Secretary had, months earlier, used the Federal Acquisition Supply Chain Security Act to exclude Hangzhou DeepSeek Artificial Intelligence from civilian federal procurement and order its products removed. The headline is not the ban on DeepSeek's chatbot, which most agencies had blocked since early 2025. It is a removal clause covering "third-party products and services developed using DeepSeek implementations." That clause applies regardless of where a model runs. It draws no line between a Beijing API endpoint and a fine-tuned open-weight checkpoint on a U.S. cloud. And it gives contractors no definition to test their supply chains against. This report reads the primary text, separates what it reaches from what commentators claim it reaches, and works out what a vendor can and cannot prove about model lineage.
stats:
  - {label: FR document, value: "2026-21447", note: "Public inspection Oct 19, 2026"}
  - {label: Reported order date, value: "Jul 24", note: "2026; CyberScoop cites Jun 26"}
  - {label: R1 derivative repos, value: "524", note: "Hugging Face, as of 2026-10-20"}
  - {label: Contractor report window, value: "3", unit: "bus. days", note: "FAR 52.204-30"}
---

:::kv
- {term: "What it bans", def: "Civilian agencies may not buy IT products or services developed by DeepSeek or its affiliates, and must remove DeepSeek products plus third-party products and services developed using DeepSeek implementations."}
- {term: "Who it binds", def: "Federal civilian executive agencies directly. Contractors only through FAR 52.204-30 (or its FAR-overhaul successor) in their contracts. DoD, the intelligence community, and national security systems sit under separate authorities."}
- {term: "Open weights on U.S. clouds", def: "Not mentioned in the notice, but not exempted either. A DeepSeek checkpoint served from AWS or a vendor's own GPUs is still a DeepSeek product, so the plain text reaches it whatever the hosting."}
- {term: "Fine-tunes and distills", def: "Fine-tunes of DeepSeek weights are plausibly in scope. Students distilled on DeepSeek outputs, and models that only reuse DeepSeek's published architecture, are genuinely ambiguous because \"implementations\" is undefined."}
- {term: "What vendors can prove", def: "Positive provenance: signed weights, hashes, declared base models, weight-similarity tests. Not the absence of distillation. Attestations should be knowledge-qualified, as the FAR's reasonable-inquiry standard already allows."}
:::

## 1. What the primary text says, and what it doesn't

The notice is short and states only two operative commands. Everything else in circulation comes from the scanned order pages, read secondhand. The Federal Register notice (FR Doc. 2026-21447, docket DHS-2026-0628) describes an order with two parts. The first is "excluding information technology products and services developed by Hangzhou DeepSeek Artificial Intelligence Co., Ltd (DeepSeek), to include affiliated entities as defined in applicable regulations, from federal civilian agency procurements." The second is "removal of all DeepSeek and DeepSeek-affiliate products, and third-party products and services developed using DeepSeek implementations, from civilian agency information technology"[^1]. It cites 41 U.S.C. 1321–1328 and the Federal Acquisition Security Council's rule at 41 CFR 201-1, defines "affiliated entities" by reference to 48 CFR 2.101, and routes questions to a FASCSA Order Implementation Team in CISA's Cybersecurity Division[^1]. The signature on the notice is DHS General Counsel James H. Percival II's, not the Secretary's[^1].

The two clauses are not symmetric. Third parties appear **only in the removal clause**. The procurement exclusion reaches only what was "developed by" DeepSeek or its affiliates[^1]. Read literally, an agency may not *buy* DeepSeek's own products, and must *remove* third-party products built with DeepSeek implementations. That is an odd split: nothing in the exclusion clause bars buying the very derivative products the removal clause makes agencies take out. It may be drafting shorthand, and the scanned order may close the gap. But the notice, the only machine-readable text, says what it says.

Several words that dominate the coverage do not appear in the notice at all: "derivative," "open-weight," "weights," "model," "hosted," and "cloud"[^1]. The often-quoted phrase "developed using DeepSeek's model or its underlying implementations" is a paraphrase circulated by secondary outlets. The notice says "developed using DeepSeek implementations"[^1,2]. That difference matters, because "model" would have been a narrower and more testable hook than "implementations."

:::kv
- {term: "Document", def: "FR Doc. 2026-21447, Notice of order; filed Oct 19, 2026, 8:45 a.m.; published Oct 20, 2026; 6 pages."}
- {term: "Legal basis", def: "FASCSA, 41 U.S.C. 1321–1328; 41 CFR 201-1 (FASC rule)."}
- {term: "Covered source", def: "Hangzhou DeepSeek Artificial Intelligence Co., Ltd and affiliates per 48 CFR 2.101."}
- {term: "Removal reach", def: "DeepSeek products, affiliate products, and third-party products and services developed using DeepSeek implementations."}
- {term: "Carve-outs", def: "National security systems and SCI systems of civilian agencies (as quoted by outlets that read the order); DoD and IC by statute."}
- {term: "Review", def: "Within one year and annually thereafter (order text as quoted); statute requires at least annual review."}
- {term: "Point of contact", def: "CISA FASCSA Order Implementation Team, Cybersecurity Division."}
:::

The appended order is on pages that are mostly scanned images. So the details beyond the notice come from outlets that say they read those pages. They disagree. CellCog, which says it read the signed order directly, reports an "Original Release Date of July 24, 2026"[^3]. MeriTalk says Secretary Markwayne Mullin signed the order on July 24[^4]. CyberScoop describes "a letter from Secretary of Homeland Security Markwayne Mullin ordering the exclusion of DeepSeek products on June 26"[^5]. Reuters, via BNN Bloomberg, calls it "a July memo"[^6]. The most defensible reading: the order carries a July 24, 2026 release date, and the June 26 reference is either an earlier letter or a misreading. Either way, the restriction had been in force for roughly three months before the public saw it.

The exception mechanics are also reported inconsistently. IBTimes says requests "must be submitted in writing within 60 days of the order's issuance and include a compelling justification"[^7]. CyberScoop paraphrases them as due "60 days in advance"[^5]. MeriTalk's subheadline speaks of "60 days to remove"[^4]. CellCog quotes the order as requiring action "immediately after the issuance of the Order, or seek an Exception"[^3]. The quoted operative text supports immediate effect with a 60-day exception window. Counted from July 24, that window closed around September 22, about four weeks before anyone outside government could read the order.

:::callout(kind=warn, label="Source caveat")
Signing date, footnote wording, procurement-channel list, and exception mechanics all come from secondary transcriptions of scanned pages. Only the notice text is machine-verified here[^1]. Treat any vendor guidance that quotes the order beyond the notice's two clauses as provisional until the docket copy is OCR'd.
:::

This matters because the operational question for vendors, whether their product is a "third-party product developed using DeepSeek implementations," turns on a term that appears in a two-clause notice with no definitions section. CellCog reports that a footnote extends coverage to third-party implementations of DeepSeek, and that "the order does not define an implementation"[^3].

## 2. The machinery: how a FASCSA order actually reaches a vendor

The thesis of this section: a DHS FASCSA order is a direct command to agencies and only an indirect, contract-mediated command to vendors. So the "audit burden on every vendor" framing is legally overstated and commercially accurate at the same time.

FASCSA (Title II of the SECURE Technology Act, enacted December 21, 2018) splits order authority three ways. The Secretary of Homeland Security issues orders for civilian agencies. The Secretary of Defense issues them for DoD and national security systems other than SCI systems. The Director of National Intelligence issues them for the intelligence community and SCI systems[^8]. The statute's compliance duty falls on agencies: "Executive agencies shall comply with exclusion and removal orders"[^8]. Before an order issues, the named source gets confidential notice and 30 days to submit "information and argument in opposition"[^8]. The FASC rule pushes exclusion down the supply chain, so covered items are excluded "from being supplied by any prime contractor and subcontractor at any tier"[^9].

Contractors feel this through FAR 52.204-30, created by the FAR Council's interim rule published October 5, 2023 and effective December 4, 2023[^10,11]. Its prohibition has no knowledge qualifier: "Contractors shall not provide or use as part of the performance of the contract any covered article"[^11]. Its discovery duty, by contrast, is bounded. A "reasonable inquiry" is "an inquiry designed to uncover any information in the entity's possession about the identity of any covered articles," and it "excludes the need to include an internal or third-party audit"[^11]. Contractors must check SAM.gov "at least once every three months," report within 3 business days of identifying a covered article, follow up within 10 business days, and flow the clause into subcontracts, "including subcontracts for the acquisition of commercial products and commercial services"[^11].

:::timeline
- {date: "2017-09-13", headline: "BOD 17-01 (Kaspersky)", body: "DHS orders agencies to identify Kaspersky products in 30 days and begin removal at 90; Congress codifies it in the FY2018 NDAA."}
- {date: "2018-11-30", headline: "Kaspersky v. DHS", body: "D.C. Circuit affirms dismissal: the statutory ban is 'prophylactic, not punitive.'"}
- {date: "2018-12-21", headline: "FASCSA enacted", body: "Creates the Federal Acquisition Security Council and three-way order authority."}
- {date: "2021-08-26", headline: "FASC final rule", body: "41 CFR 201-1 finalizes how recommendations and orders are made."}
- {date: "2023-12-04", headline: "FAR clauses live", body: "52.204-29/-30 take effect: SAM.gov checks, reasonable inquiry, 3-day reporting."}
- {date: "2025-09", headline: "First order: Acronis", body: "DNI excludes Acronis AG from IC procurement; GSA pulls it from GSA Advantage."}
- {date: "2025-12-18", headline: "FY2026 NDAA", body: "Section 1532 bans DeepSeek AI for DoD and its contractors; Section 6604 covers IC systems."}
- {date: "2026-07-24", headline: "DHS order 2026-01 (reported date)", body: "Civilian exclusion and removal order against DeepSeek, unpublished."}
- {date: "2026-10-20", headline: "Federal Register publication", body: "Notice 2026-21447 makes the order public."}
:::

The detail that most changes vendor exposure is FAR 52.204-30(b)(4). "A FASCSA order issued after the date of solicitation applies to this contract only if added by an amendment" to the solicitation "or modification to the contract"[^11]. The clause then points to paragraph (c), so monitoring, inquiry and reporting duties continue[^11]. For contracts already in performance, the DeepSeek order bites through GSA schedule mass modifications and new task orders, not automatically. The Acronis precedent shows how fast that happens. GSA removed Acronis from GSA Advantage within three days of the September 2025 order and announced modifications to its multiple-award schedule contracts[^12,13].

Review is real but narrow. A petition must go to the D.C. Circuit "not later than 60 days after a party is notified." The court sets aside orders "lacking substantial support in the administrative record," and classified material is "submitted only to the court ex parte and in camera"[^14]. The Kaspersky litigation shows how deferential that forum is. The court treated a security-motivated exclusion as "prophylactic, not punitive" and rejected the bill-of-attainder theory[^15,16].

There is a structural gap here. Notice, the 30-day response window, and the 60-day petition clock all run to the named *source*, which here is DeepSeek. A U.S. integrator whose product is swept in by the "implementations" language gets no pre-order notice and has no obvious "party notified" trigger for review[^8,14]. Section 889 of the FY2019 NDAA has a similar "products containing" reach. But that was a statute naming its targets and reaching equipment used "as a substantial or essential component of any system"[^17]. This order reaches derivative products through a single undefined noun.

The counterpoint is fair: the FAR clause's no-audit definition means a contractor that genuinely does not know its product embeds DeepSeek has not breached its inquiry duty[^11]. But the prohibition itself is strict, and the False Claims Act punishes reckless disregard. In practice "reasonable inquiry" drifts toward "know your model stack." AI Weekly's phrase, that the order "pushes the audit burden onto every vendor," is editorial, not order text. It describes the commercial reality better than the legal one[^18].

## 3. Three regimes, three scopes: the order next to the NDAA

This section's claim: the DHS order did not create the first federal DeepSeek ban. It closes the civilian gap left by Congress, with broader derivative language than Congress used.

The FY2026 NDAA (Public Law 119-60, signed December 18, 2025) already did the heavy lifting for defense[^21]. Section 1532 defines covered AI as "any artificial intelligence, or successor artificial intelligence, developed by the Chinese company DeepSeek," plus AI developed by High Flyer or entities in which High Flyer "directly or indirectly owns at least a 20 percent stake"[^19]. It bars contractors from using covered AI "with respect to the performance of a contract with the Department"[^19]. Waivers are case-by-case, for research, national-security testing, operational activities, or mission-critical functions[^19]. Section 6604 separately requires removal of "the DeepSeek application or any successor application or service" from intelligence-community national security systems, including those run by contractors[^20]. CRS summarizes Section 1532 as prohibiting DoD "from using or acquiring covered AI systems—including those from DeepSeek and High Flyer"[^21].

| Instrument | Covered set | Derivative reach | Who is bound | Relief valve |
|---|---|---|---|---|
| *DHS FASCSA Order 2026-01 | DeepSeek + 48 CFR 2.101 affiliates | Explicit: third-party products "developed using DeepSeek implementations" (removal) | Civilian agencies; contractors via FAR clause | Agency exception, 60 days, compelling justification |
| NDAA FY2026 §1532 | AI "developed by" DeepSeek or High Flyer (≥20% stakes) | None explicit; reached only through "use" | DoD and its contractors, by statute | SecDef case-by-case waiver, four categories |
| NDAA FY2026 §6604 | "DeepSeek application or any successor application or service" | App/service test only | IC national security systems, incl. contractor-operated | DNI exceptions for national security and research |
| DNI FASCSA order (Acronis, 2025) | Acronis AG and affiliates | "All Acronis products or services" | IC and SCI systems | Order-specific |

The contrast in derivative reach is the point. Congress tested *who developed* the AI. A fine-tune that Microsoft post-trains from R1 is still AI "developed by" DeepSeek in part, but a Qwen network distilled on R1 outputs is not obviously covered. DHS instead tested *what the product was developed using*, which reaches further down the lineage tree. Neither instrument names Qwen, Kimi or GLM. Section 1532's broader covered-nation language only says the Secretary "shall consider issuing" guidance[^19].

The pre-2026 history explains why the order reads as codification rather than novelty. NASA's chief AI officer barred DeepSeek from NASA data, devices and networks on January 31, 2025, because its servers "operate outside of the United States"[^22]. The House's Chief Administrative Officer declared it "unauthorized for official House use"[^22]. By April 2025, 14 states had banned it on government devices, starting with Texas on January 31[^23]. The House China Select Committee's April 16, 2025 report claimed "more than 85% of DeepSeek's responses are manipulated to suppress content"[^24]. The No Adversarial AI Act of June 2025 would have had the FASC maintain a public list of adversary-developed AI barred from executive agencies[^25]. It was never enacted, and this order reaches a similar result for one company using authority that existed since 2018.

What would weaken this reading: if the scanned order defines "implementations" narrowly (for example, as DeepSeek-hosted services), then DHS's reach collapses toward Section 6604's app test. The CellCog account suggests no definition exists[^3]. Why it matters: a contractor serving both DoD and civilian agencies now runs two lineage tests with different words. The stricter DHS phrasing governs any product sold on a civilian vehicle.

## 4. What "developed using DeepSeek implementations" plausibly reaches

The thesis: the derivative clause is easy to apply at the top of the lineage tree and nearly impossible to apply at the bottom, and the bottom is where most of the ecosystem lives.

Start with what DeepSeek itself licensed. The R1 model card states: "This code repository and the model weights are licensed under the MIT License," and expressly permits "distillation for training other LLMs"[^26]. DeepSeek also published six distilled models. Four are Qwen2.5 networks and two are Llama networks, all fine-tuned on "800k samples curated with DeepSeek-R1"[^26]. The flagship DeepSeek-branded "R1-Distill" models are therefore Alibaba and Meta architectures carrying DeepSeek-generated training data. The original V3 weights were different: the code was MIT, but "use of DeepSeek-V3 Base/Chat models is subject to the Model License"[^27].

Hugging Face's self-declared lineage metadata gives a floor on the derivative tree. As of October 20, 2026, deepseek-ai/DeepSeek-R1 lists 327 finetunes, 122 adapters, 70 quantizations and 5 merges[^26]. DeepSeek-V3 lists 87 finetunes, 36 adapters, 17 quantizations and 1 merge[^27].

:::donut(center-label="524 repos")
- {label: "Finetunes (327)", value: 62.4}
- {label: "Adapters (122)", value: 23.3}
- {label: "Quantizations (70)", value: 13.4}
- {label: "Merges (5)", value: 0.9}
:::

Those counts are self-reported. The `base_model` field is typed by the uploader, and Hugging Face infers the relationship type without verifying it[^28]. Omitting the tag makes a re-upload invisible, and distillation is not a relation type at all[^28]. One notable entry is microsoft/MAI-DS-R1, described as "a DeepSeek-R1 reasoning model that has been post-trained by the Microsoft AI team" to improve "responsiveness on blocked topics"[^29]. A major U.S. vendor's model is plainly "developed using" a DeepSeek implementation, whatever its post-training changed.

The hardest case is architectural borrowing. Moonshot's Kimi K2 ships a config declaring `"architectures": ["DeepseekV3ForCausalLM"]` and loads `modeling_deepseek.DeepseekV3ForCausalLM`[^30]. That is DeepSeek's literal model code, under a different company's weights. Further out, Group Relative Policy Optimization (GRPO), introduced in DeepSeek's 2024 DeepSeekMath paper, has since been widely reused in open reasoning-model training[^31]. Calling a published algorithm an "implementation" would turn a supply-chain order into a ban on ideas. But the text does not rule it out.

| Tier | Example | Plausibly in scope? | Provable either way? |
|---|---|---|---|
| *1. DeepSeek app or API (PRC-hosted) | chat.deepseek.com, api.deepseek.com | Yes, the core case | Yes, by network egress logs |
| 2. Original weights, U.S.-hosted | Bedrock, Azure AI Foundry, Vertex endpoints | Yes: still a DeepSeek product | Yes, by model ID and hash |
| 3. Fine-tune, quant, adapter, merge | MAI-DS-R1; 524 R1-tree repos | Likely | Mostly: weight-similarity tests |
| 4. Distilled student | R1-Distill-Qwen/Llama | Ambiguous | Only if declared |
| 5. Architecture borrower | Kimi K2 (DeepseekV3ForCausalLM) | Ambiguous for literal code reuse | Yes for code, by config inspection |
| 6. Trained partly on DeepSeek outputs, or using GRPO | Undisclosed synthetic data pipelines | Unlikely, but not excluded | No |

The counter-argument deserves weight: an agency lawyer would read "implementations" in light of the order's stated risks, and those concern data flowing to the PRC and code that might be malicious. Under that purposive reading, tiers 4–6 fall out because they carry no DeepSeek code or weights at inference time. Tier 5 stays only where DeepSeek code is literally imported. That reading is sensible, but it is not written down anywhere a vendor can cite. Why it matters: until CISA publishes guidance, the operational definition will be set by risk-averse contracting officers, who tend to read ambiguity broadly.

## 5. Matching the three threat vectors to the deployment modes they actually touch

The thesis: the order's stated threat vectors are strong for DeepSeek's hosted service, collapse for U.S.-hosted weights on two of three counts, and survive in an altered form (integrity rather than espionage) for every deployment mode.

The order, as quoted, says "DeepSeek presents multiple threat vectors that pose significant risk to the cybersecurity of U.S. government systems"[^4]. Use "may result in the transfer of sensitive data to the PRC if used by U.S. government employees or vendors"[^6], such data "could produce actionable intelligence on U.S. persons and/or government programs"[^5], and "the models themselves may contain malware or other security vulnerabilities"[^6]. Outlets split between "government programs" and "government agencies" in the intelligence sentence, which cannot be settled without OCR of the scanned pages[^5,6].

For the hosted service, vectors one and two are well documented. DeepSeek's own privacy policy (last updated May 6, 2026) states its servers are located in the People's Republic of China[^32]. In January 2025 Wiz found an exposed DeepSeek ClickHouse database holding "over a million lines of log streams," including chat history and API keys[^33]. NowSecure found the iOS app "globally disables App Transport Security" and "hardcodes encryption keys"[^34]. None of these vectors require weights at all. Each is a property of DeepSeek's operations.

For open weights the evidence changes character. NIST's Center for AI Standards and Innovation (CAISI) evaluated R1, R1-0528 and V3.1 against GPT-5, GPT-5-mini, gpt-oss and Opus 4 across 19 benchmarks[^35]:

:::stats
- {label: Agent hijacking, value: "12×", note: "R1-0528 vs U.S. frontier models"}
- {label: Jailbroken compliance, value: "94%", note: "vs 8% for U.S. reference models"}
- {label: CCP narratives echoed, value: "4×", note: "vs U.S. reference models"}
- {label: Download growth, value: "~1,000%", note: "since Jan 2025, per CAISI"}
:::

CAISI's figures: agents built on R1-0528 were "12 times more likely than evaluated U.S. frontier models to follow malicious instructions," and R1-0528 complied with 94% of overtly malicious requests under a common jailbreak versus 8% for U.S. reference models[^35]. On capability, "the best U.S. model evaluated solves over 20% more tasks than the best DeepSeek model" on software and cyber tasks[^35]. Cisco's January 2025 HarmBench test found DeepSeek-R1 "failed to block a single harmful prompt" across 50 prompts. It was not alone at the weak end[^36]:

:::bar-chart(title="HarmBench attack success rate, 50 prompts (Jan 2025)", orientation=horizontal, value-suffix=%)
categories: DeepSeek R1, Llama-3.1-405B, GPT-4o, Gemini-1.5-pro, Claude-3.5-Sonnet, o1-preview
Attack success rate: 100, 96, 86, 64, 36, 26
:::

That chart is the strongest counterpoint to treating jailbreak weakness as a supply-chain reason for exclusion: Meta's Llama-3.1-405B scored 96%, and Llama models sit inside AWS's FedRAMP-authorized Bedrock catalog[^36,37]. Weak refusal behavior is a property shared by a U.S. model the government approves.

The more DeepSeek-specific finding comes from CrowdStrike, which "tested the raw, open-source DeepSeek-R1 671B model directly to avoid any confounding effects from API-level guardrails." It ran 30,250 prompts per model[^38]. With no trigger words, the model produced vulnerable code in 19% of cases. For an industrial-control system "located in Tibet," severe vulnerabilities rose to 27.2%, "an increase of almost 50%"[^38].

:::slope(left-label="Neutral prompt", right-label="Tibet trigger", unit=%)
| Item | Neutral prompt | Tibet trigger |
|---|---|---|
| DeepSeek-R1 671B severe-vuln rate | 19 | 27.2 |
:::

This is the crux of the "malware in the models" vector. No public evidence shows executable malware in DeepSeek's weights. They ship as safetensors shards, a format that cannot execute code. The live code-execution surface is the repository's `modeling_deepseek.py`, which runs when loaded with `trust_remote_code`[^26,27]. Anthropic's Sleeper Agents work showed that "backdoor behavior can be made persistent, so that it is not removed by standard safety training"[^39]. A trigger-conditioned degradation like CrowdStrike's cannot be ruled out by inspection, and no buyer's evaluation can prove its absence.

| Threat vector | DeepSeek app/API | U.S.-hosted original weights | Air-gapped, no tools |
|---|---|---|---|
| *Data to PRC servers | Live: servers in PRC by policy | Absent: host is U.S. | Absent |
| Intelligence on U.S. persons | Live | Absent, unless agentic tools enable exfiltration | Absent |
| Malware / integrity sabotage | Live (client code) | Live as integrity risk (CrowdStrike, CAISI hijacking) | Live as integrity risk via outputs |

What would weaken the integrity argument: CrowdStrike's trigger effect was measured on politically sensitive prompts that federal civilian code rarely contains, and its two Western comparison models are unnamed[^38]. Why it matters: the honest justification for reaching U.S.-hosted weights is integrity, not espionage. Integrity risks call for evaluation and output controls that apply to *every* open model, not to one vendor's name.

## 6. Where the exposure actually sits: clouds, aggregators, and one search engine

The thesis: the big FedRAMP clouds are barely exposed inside their authorization boundaries. The live exposure sits in commercial-region endpoints, multi-model aggregators, and vendors that quietly add DeepSeek to model menus.

AWS made DeepSeek-R1 "generally available in Amazon Bedrock" on March 10, 2025, stating that "users' inputs and model outputs aren't shared with any model providers"[^40]. The current Bedrock model card serves R1 through the U.S. geo inference profile `us.deepseek.r1-v1:0`, that is, through commercial U.S. regions[^41]. AWS's list of Bedrock models in scope for FedRAMP and DoD IL4/IL5 (last updated October 5, 2026) names AI21, Amazon, Anthropic, Cohere, Google Gemma, Meta, Mistral, Nvidia, OpenAI, Stability and xAI. DeepSeek is not on it[^37]. Microsoft announced R1 on Azure AI Foundry on January 29, 2025[^42]. Its Azure Government page lists only OpenAI models among "Foundry Models sold by Azure"[^43].

:::compare
- {role: "INSIDE FEDRAMP", name: "Bedrock GovCloud / FedRAMP list", value: "0 DeepSeek models"}
- {role: "COMMERCIAL U.S.", name: "Bedrock commercial regions", value: "DeepSeek-R1 (us.deepseek.r1-v1:0)"}
- {role: SUBJECT, name: "Civilian agency exposure", value: "Commercial-region model IDs"}
:::

The implication: for a cloud provider, the covered article is the DeepSeek endpoint, not the cloud service. Agencies can comply by denying `deepseek.*` model IDs in access policies, without removing Bedrock or Foundry. A model catalog that *offers* DeepSeek is not plausibly a "product developed using DeepSeek implementations."

Two vendor patterns are more exposed. Perplexity built R1 1776 on DeepSeek-R1 in February 2025. Microsoft's own card describes it as reaching the same 99.3% unblocking rate as MAI-DS-R1[^29]. In mid-2026 Perplexity announced that "DeepSeek V4 Pro, hosted in the U.S., is now available in Perplexity Computer"[^44]. Separately, GSA's November 2025 OneGov deal priced Perplexity Enterprise Pro for Government at "$0.25 per agency over an 18-month term" and said it "supports multiple leading AI models, including Perplexity, OpenAI, and Anthropic"[^45]. Nothing public shows the government tier includes DeepSeek. But this is the kind of product whose model menu a contracting officer now has to ask about.

Multi-model aggregators are the second pattern. In January 2025, Pentagon workers used DeepSeek's chatbot for days before the Defense Information Systems Agency moved to block the website[^65]. Website blocks do not reach API routing inside another vendor's product. That is exactly the case the removal clause targets, and the case that "reasonable inquiry" must cover: a vendor that routes prompts to whichever model is cheapest has to know when the cheapest model is DeepSeek.

Counterpoint: civilian agencies were never heavy DeepSeek users through authorized channels. GSA's USAi platform became a paid service used by 25 agencies in September 2026[^46]. The FedRAMP model lists checked here exclude DeepSeek[^37,43]. Why it matters: most of the removal burden falls not on the hyperscalers but on mid-sized SaaS vendors with model routers and on agency shadow IT.

## 7. Provenance: what a vendor can prove, and what nobody can

The thesis: positive provenance (this product uses exactly these signed weights) is now cheap and provable. Negative provenance (no DeepSeek output ever touched this model's training) is not provable with any current technique, so vendor attestations must be knowledge-qualified.

The tooling for positive claims is mature. The OpenSSF/Sigstore model-signing project signs (path, digest) pairs and verifies signer identity against a transparency log, establishing that "the model hasn't been tampered with after training"[^47]. The same project lists signing model-card metadata as future work, so the signature says nothing about what the model was trained on[^47]. CycloneDX's ML-BOM "documents provenance and ethical considerations for datasets"[^48]. The June 2026 CISA/G7 "Software Bill of Materials for AI – Minimum Elements" adds lineage and dataset-provenance fields, but is "voluntary and nonmandatory" and "expressly does not create new legal requirements"[^49]. All of these record claims. None verify them.

Verification exists only for weight-level derivation. Zhu et al. (February 2025) give statistical tests with "exact p-values with respect to the null hypothesis" that two models share an initialization. The tests stay effective after heavy fine-tuning, a companion activation-matching test also detects pruned derivatives, and the method flagged every non-independent pair among 210 model pairs tested[^50]. HuRef shows a model's parameter-vector direction survives "continued pretraining, supervised fine-tuning, and RLHF"[^51]. Both require white-box access to both models. Because DeepSeek's weights are public, a vendor can actually run these tests against its own checkpoint and produce affirmative evidence that its model is not a tier-3 derivative.

Distillation is the wall. A June 2026 study concludes that "identifying a teacher model from a student in isolation is highly challenging." It reaches near-perfect accuracy only in single-teacher settings with a reference checkpoint, and notes modern lineages are "already heavily entangled"[^52]. Anthropic's February 2026 disclosure illustrates the scale. It reported "over 16 million exchanges with Claude through approximately 24,000 fraudulent accounts," with DeepSeek accounting for more than 150,000[^53]. Distillation flows in every direction. Synthetic-data vendors resell outputs whose teachers are undisclosed. A U.S. model trained on a purchased instruction dataset may carry DeepSeek outputs without its developer knowing.

:::bars
- {label: "Signed weights / hashes match a named artifact", value: "Provable", pct: 100}
- {label: "Declared base model (model card, AI-BOM)", value: "Provable as a declaration only", pct: 70}
- {label: "Not a fine-tune of DeepSeek weights", value: "Testable (white-box)", pct: 60}
- {label: "No DeepSeek code at load or inference", value: "Testable (config, dependency scan)", pct: 55}
- {label: "Never distilled from DeepSeek outputs", value: "Unprovable", pct: 10}
:::

The model-file malware vector is a separate problem with a separate fix. ReversingLabs found two Hugging Face models carrying reverse shells inside deliberately broken pickle files that picklescan did not flag[^54]. That is a file-format risk, solved by loading safetensors with remote code disabled and by scanning. Provenance does not solve it, and the risk does not depend on DeepSeek origin.

The practical answer mirrors Section 889's covered-telecom representation, which offerors make "after conducting a reasonable inquiry"[^55]. A defensible DeepSeek attestation covers four things. No DeepSeek weights, code or API endpoint in the product. A weight-independence test against public DeepSeek checkpoints. Supplier flow-down certifications on training-data sources. And "no known use" of DeepSeek outputs in training. What would weaken this approach: a contracting officer could demand an unqualified "not developed using" warranty. Vendors should refuse it, because no technique can support it and an unsupportable certification is False Claims Act exposure. Why it matters: the order turns model provenance from a research topic into a contract representation, and the tooling only covers half of it.

## 8. How much of the ecosystem the clause actually touches

The thesis: DeepSeek is the largest Chinese open-model *API* vendor but not the dominant *build-on* base. So the clause's real cost is in routing and hosting, not in fine-tuned products. That holds unless future orders extend the same language to Qwen, Kimi or GLM.

The a16z/OpenRouter usage study (December 2025) shows DeepSeek as the largest open-model author on the platform by tokens over November 2024 to November 2025. It also notes that "its dominance has waned"[^56]:

:::rank-list
- {label: DeepSeek, value: "14.37T tokens", pct: 100, highlight: true}
- {label: Qwen (Alibaba), value: "5.59T", pct: 39}
- {label: Meta, value: "3.96T", pct: 28}
- {label: Mistral, value: "2.92T", pct: 20}
- {label: OpenAI (open models), value: "1.65T", pct: 11}
- {label: MiniMax, value: "1.26T", pct: 9}
- {label: Z-AI, value: "1.18T", pct: 8}
- {label: TNG, value: "1.13T", pct: 8}
- {label: Moonshot, value: "0.92T", pct: 6}
:::

Chinese open models' weekly token share on OpenRouter ran from 1.2% to a peak near 30% over that window, averaging 13.0%[^56]. By July 2026, Bloomberg data reported via AI Weekly put Chinese models at a record 58% of U.S. firms' OpenRouter tokens, with DeepSeek alone at 17.6% of routed tokens weekly[^57]. That source cautions that "token share is not revenue share"[^57]. On this evidence, DeepSeek is what U.S. software calls, often through routers.

Building on DeepSeek is a different matter. On October 20, 2026, Qwen2.5-7B-Instruct alone listed 3,174 finetunes on Hugging Face, against 327 for DeepSeek-R1[^58,26]. Hugging Face's summer 2026 review counts 151,448 Qwen derivatives and observes that "some U.S. model releases above 100B parameters this year are built on top of Chinese models"[^59]. Nathan Lambert's ATOM tracking describes adoption as "dominated by Qwen (with a little help from DeepSeek)"[^60]. The best-known U.S. product built on a Chinese base, Cursor's Composer 2, runs on Moonshot's Kimi K2.5[^61]. The original Kimi K2 declares DeepSeek-V3's architecture class[^30]. If K2.5 keeps that class, which this report assumes but has not verified, that is the tier-5 case, where "implementations" could reach a product that never used a DeepSeek weight.

The federal dollars at stake through this order are small. Brookings counts $91.8 billion in potential value of federal AI contracts with effective dates from September 2023 to March 2026. DoD holds $90.7 billion of that, 98.9%[^62]. DoD is outside the DHS order's authority, and Section 1532 already governs it[^8,19]. On these figures the civilian slice, where this order applies, is on the order of $1 billion in potential value.

Counterpoint: the order is a template. The July 2026 fight over a broader ban drew a letter from nearly 200 startups organized by the Little Tech Association[^63]. A separate open-weights letter followed on July 24, signed by firms including Nvidia, Microsoft, Meta and Hugging Face[^64]. The coverage of both letters centered on Moonshot's Kimi models, with Z.ai's GLM also cited, and neither named DeepSeek[^63,64]. Why it matters: if DHS reuses "developed using [X] implementations" for Moonshot, Z.ai or Alibaba, the tier-4 and tier-5 ambiguity stops being an edge case and starts reaching mainstream U.S. coding and agent products.

## 9. A vendor playbook that survives the ambiguity

The thesis: vendors can comply defensibly today by treating the order as three tests: endpoint, weights, and code. They should document a knowledge-qualified position on distillation rather than wait for CISA to define "implementations."

:::kv
- {term: "1. Endpoint inventory", def: "Enumerate every model ID your product can route to, including fallbacks in routers and aggregators. Block deepseek.* identifiers and api.deepseek.com egress for any civilian-agency tenant."}
- {term: "2. Weight lineage", def: "For every open-weight model you serve, record source repo, revision hash, and declared base_model. For tiers 2–3, run a weight-independence test against public DeepSeek-R1/V3 checkpoints and keep the p-values."}
- {term: "3. Code lineage", def: "Scan configs for DeepseekV3ForCausalLM or modeling_deepseek imports; disable trust_remote_code; load safetensors only."}
- {term: "4. Training-data flow-down", def: "Require synthetic-data suppliers to certify teacher models. Your attestation on distillation should say 'no known use after reasonable inquiry', never 'not developed using'."}
- {term: "5. Contract mechanics", def: "Check SAM.gov supply-chain orders at least quarterly; expect GSA mass modifications; report within 3 business days of identification."}
- {term: "6. Exceptions are the agency's", def: "Only the agency can request an exception, and the reported 60-day window has likely closed for existing deployments."}
:::

The supporting authorities are the FAR clause's SAM.gov and reporting cadence[^11], GSA's demonstrated speed in modifying schedules after the Acronis order[^12,13], and the provenance tooling limits described above[^47,50,52]. The counterpoint: this is more work than the legal standard demands, since a reasonable inquiry "excludes the need to include an internal or third-party audit"[^11]. The reason to do it anyway is commercial. A contracting officer cannot easily tell a vendor with documented lineage from one with none, and will default to the vendor with documents.

## 10. What could break this analysis

Five things could falsify or substantially change the conclusions above.

**The scanned order could define "implementations."** Every scope judgment here rests on the notice text plus secondary accounts saying the order leaves the term undefined[^1,3]. If the docket copy contains a definition limited to DeepSeek-hosted services, tiers 2–6 largely fall out, and the order is a narrower app-and-API ban than this report suggests.

**The asymmetry between clauses may be drafting noise.** This report notes that third parties appear only in the removal clause[^1]. A court or CISA guidance could read the exclusion clause as implicitly covering what the removal clause covers, making the asymmetry irrelevant. Reuters already paraphrases the order as "banning acquisition of DeepSeek products and third-party services developed using DeepSeek"[^6], although the notice's exclusion clause says only "developed by"[^1].

**The integrity case for reaching U.S.-hosted weights may be weaker than presented.** CAISI is a U.S. government body evaluating a rival nation's models in support of U.S. policy, so it is not an independent assessor[^35]. Cisco's data show a U.S. model nearly as jailbreakable[^36]. CrowdStrike's trigger effect concerns politically loaded prompts and unnamed comparison models[^38]. A reader could fairly conclude that the reach to U.S.-hosted weights is reputational and political, not technical. CyberScoop noted that some of DHS's stated concerns "could also apply to other Chinese and U.S. AI models"[^5].

**Reported dates could be wrong.** The July 24 date rests on outlets that read scanned pages, and CyberScoop's June 26 account conflicts[^3,4,5]. If the order postdates July 24, the exception window may still be open.

**Market exposure figures are volatile and venue-specific.** The OpenRouter and Hugging Face figures are as of December 2025, July 2026 and October 20, 2026 respectively. They measure one router and one hub, not federal production deployments[^56,57,26].

Red-team pass: 2 of 3 top claims were unbroken. The removal-clause quote and the absence of "model," "weights" and "cloud" from the notice survived term-by-term checks against the raw text[^1]. The July 24 date drew one medium-severity contradiction, CyberScoop's June 26 account, which this report already flags[^5].

What would *confirm* the thesis: CISA implementation guidance that adopts a lineage test, GSA mass modifications quoting the "implementations" language verbatim, or a second FASCSA order using the same phrase against another Chinese lab.

:::references
- {id: 1, title: "Order: Exclusion and Removal of DeepSeek Products from Federal Civilian Executive Branch Information Technology Systems and Procurements (FR Doc. 2026-21447), raw text", url: "https://www.federalregister.gov/public-inspection/raw_text/202/621/447.txt", source: "Federal Register (DHS)", date: "2026-10-19"}
- {id: 2, title: "FR Doc. 2026-21447 public inspection PDF", url: "https://public-inspection.federalregister.gov/2026-21447.pdf", source: "Federal Register", date: "2026-10-19"}
- {id: 3, title: "DHS Orders DeepSeek Off Federal Systems: What It Requires", url: "https://cellcog.ai/blog/dhs-deepseek-order/", source: CellCog, date: "2026-10-19"}
- {id: 4, title: "DHS orders civilian agencies to remove DeepSeek AI products", url: "https://www.meritalk.com/articles/dhs-orders-civilian-agencies-to-remove-deepseek-ai-products/", source: MeriTalk, date: "2026-10-19"}
- {id: 5, title: "DHS to ban DeepSeek from federal civilian agencies", url: "https://cyberscoop.com/dhs-bans-deepseek-federal-agencies/", source: CyberScoop, date: "2026-10-19"}
- {id: 6, title: "US banning Chinese AI DeepSeek from government agency IT systems (Reuters)", url: "https://www.bnnbloomberg.ca/business/international/2026/10/19/us-banning-chinese-ai-deepseek-from-government-agency-it-systems/", source: "BNN Bloomberg / Reuters", date: "2026-10-19"}
- {id: 7, title: "US agencies ordered to remove DeepSeek products from government systems", url: "https://www.ibtimes.co.uk/us-agencies-remove-deepseek-products-government-systems-1826567", source: "International Business Times", date: "2026-10-19"}
- {id: 8, title: "41 U.S.C. § 1323 — Functions of the Federal Acquisition Security Council", url: "https://www.law.cornell.edu/uscode/text/41/1323", source: "LII / U.S. Code"}
- {id: 9, title: "41 CFR § 201-1.303 — Exclusion and removal orders", url: "https://www.law.cornell.edu/cfr/text/41/201-1.303", source: "LII / CFR"}
- {id: 10, title: "B-335652: FAR Case 2020-011, Implementation of FASCSA (major rule report)", url: "https://www.gao.gov/products/b-335652", source: GAO, date: "2023"}
- {id: 11, title: "FAR 52.204-30 Federal Acquisition Supply Chain Security Act Orders—Prohibition", url: "https://www.acquisition.gov/far/52.204-30", source: "Acquisition.gov", date: "2023-12"}
- {id: 12, title: "DNI Issues First FASCSA Exclusion and Removal Order Against Acronis AG", url: "https://www.mayerbrown.com/en/insights/publications/2025/10/dni-issues-first-fascsa-exclusion-and-removal-order-against-acronis-ag", source: "Mayer Brown", date: "2025-10-02"}
- {id: 13, title: "Off the Supply Chain: DNI Issues First Exclusion and Removal Order Under FASCSA", url: "https://www.crowell.com/en/insights/client-alerts/off-the-supply-chain-director-of-national-intelligence-issues-first-exclusion-and-removal-order-under-the-federal-acquisition-supply-chain-security-act", source: "Crowell & Moring", date: "2025-09-22"}
- {id: 14, title: "41 U.S.C. § 1327 — Judicial review procedures", url: "https://www.law.cornell.edu/uscode/text/41/1327", source: "LII / U.S. Code"}
- {id: 15, title: "BOD 17-01: Removal of Kaspersky-branded Products", url: "https://www.cisa.gov/news-events/directives/bod-17-01-removal-kaspersky-branded-products", source: CISA, date: "2017-09-13"}
- {id: 16, title: "Kaspersky Lab, Inc. v. DHS, 909 F.3d 446 (D.C. Cir. 2018)", url: "https://caselaw.findlaw.com/court/us-dc-circuit/1964971.html", source: "D.C. Circuit via FindLaw", date: "2018-11-30"}
- {id: 17, title: "FAR 52.204-25 Prohibition on Contracting for Certain Telecommunications and Video Surveillance Services or Equipment", url: "https://www.acquisition.gov/far/52.204-25", source: "Acquisition.gov", date: "2021-11"}
- {id: 18, title: "DHS orders DeepSeek stripped from US civilian federal IT systems", url: "https://aiweekly.co/alerts/dhs-orders-deepseek-stripped-from-us-civilian-federal-it-systems", source: "AI Weekly", date: "2026-10-19"}
- {id: 19, title: "FY2026 NDAA Sec. 1532 — Prohibition on use of DeepSeek and related AI (unofficial enacted text)", url: "https://agora.eto.tech/instrument/2694", source: "ETO AGORA", date: "2025-12-18"}
- {id: 20, title: "FY2026 NDAA Sec. 6604 — Prohibition on use of DeepSeek on intelligence community systems (unofficial enacted text)", url: "https://agora.eto.tech/instrument/2699", source: "ETO AGORA", date: "2025-12-18"}
- {id: 21, title: "CRS In Focus IF13197: AI provisions in the FY2026 NDAA", url: "https://www.everycrsreport.com/files/2026-07-06_IF13197_040ec0186a0ab2f122d18ba43dc6b3c14e7f285e.html", source: "Congressional Research Service", date: "2026-07-06"}
- {id: 22, title: "NASA becomes latest federal agency to block China's DeepSeek", url: "https://www.nbcnewyork.com/news/business/money-report/nasa-becomes-latest-federal-agency-to-block-chinas-deepseek-on-security-and-privacy-concerns/6130603/?amp=1", source: "CNBC via NBC New York", date: "2025-01-31"}
- {id: 23, title: "These States Have Banned DeepSeek", url: "https://statetechmagazine.com/article/2025/04/these-states-have-banned-deepseek", source: "StateTech", date: "2025-04-14"}
- {id: 24, title: "Moolenaar, Krishnamoorthi Unveil Explosive Report on Chinese AI Firm DeepSeek", url: "https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-krishnamoorthi-unveil-explosive-report-chinese-ai-firm-deepseek", source: "House Select Committee on the CCP", date: "2025-04-16"}
- {id: 25, title: "China Select Committee launches AI campaign with legislation to block CCP-linked AI from U.S. government use", url: "https://chinaselectcommittee.house.gov/media/press-releases/china-select-committee-launches-ai-campaign-with-legislation-to-block-ccp-linked-ai-from-us-government-use", source: "House Select Committee on the CCP", date: "2025-06-25"}
- {id: 26, title: "deepseek-ai/DeepSeek-R1 model card and model tree", url: "https://huggingface.co/deepseek-ai/DeepSeek-R1", source: "Hugging Face", date: "2026-10-20"}
- {id: 27, title: "deepseek-ai/DeepSeek-V3 model card and model tree", url: "https://huggingface.co/deepseek-ai/DeepSeek-V3", source: "Hugging Face", date: "2026-10-20"}
- {id: 28, title: "Model Cards documentation (base_model metadata)", url: "https://huggingface.co/docs/hub/model-cards", source: "Hugging Face Docs"}
- {id: 29, title: "microsoft/MAI-DS-R1 model card", url: "https://huggingface.co/microsoft/MAI-DS-R1", source: "Hugging Face (Microsoft)", date: "2025-04"}
- {id: 30, title: "moonshotai/Kimi-K2-Instruct config.json", url: "https://huggingface.co/moonshotai/Kimi-K2-Instruct/raw/main/config.json", source: "Hugging Face (Moonshot AI)"}
- {id: 31, title: "DeepSeekMath: Pushing the Limits of Mathematical Reasoning (introduces GRPO)", url: "https://arxiv.org/abs/2402.03300", source: arXiv, date: "2024-02-05"}
- {id: 32, title: "DeepSeek Privacy Policy", url: "https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html", source: DeepSeek, date: "2026-05-06"}
- {id: 33, title: "Wiz Research Uncovers Exposed DeepSeek Database Leaking Sensitive Information", url: "https://www.wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak", source: "Wiz Research", date: "2025-01-29"}
- {id: 34, title: "NowSecure Uncovers Multiple Security and Privacy Flaws in DeepSeek iOS Mobile App", url: "https://www.nowsecure.com/blog/2025/02/06/nowsecure-uncovers-multiple-security-and-privacy-flaws-in-deepseek-ios-mobile-app/", source: NowSecure, date: "2025-02-06"}
- {id: 35, title: "CAISI Evaluation of DeepSeek AI Models Finds Shortcomings and Risks", url: "https://www.nist.gov/news-events/news/2025/09/caisi-evaluation-deepseek-ai-models-finds-shortcomings-and-risks", source: "NIST CAISI", date: "2025-09-30"}
- {id: 36, title: "Evaluating Security Risk in DeepSeek and Other Frontier Reasoning Models", url: "https://blogs.cisco.com/security/evaluating-security-risk-in-deepseek-and-other-frontier-reasoning-models", source: Cisco, date: "2025-01-31"}
- {id: 37, title: "Amazon Bedrock models in scope for FedRAMP and DoD IL4/5", url: "https://aws.amazon.com/compliance/services-in-scope/FedRAMP/amazon-bedrock-models/", source: AWS, date: "2026-10-05"}
- {id: 38, title: "CrowdStrike Researchers Identify Hidden Vulnerabilities in AI-Coded Software", url: "https://www.crowdstrike.com/en-us/blog/crowdstrike-researchers-identify-hidden-vulnerabilities-ai-coded-software/", source: CrowdStrike, date: "2025-11-20"}
- {id: 39, title: "Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training", url: "https://arxiv.org/abs/2401.05566", source: "arXiv (Anthropic)", date: "2024-01-10"}
- {id: 40, title: "DeepSeek-R1 now available as a fully managed serverless model in Amazon Bedrock", url: "https://aws.amazon.com/blogs/aws/deepseek-r1-now-available-as-a-fully-managed-serverless-model-in-amazon-bedrock/", source: "AWS News Blog", date: "2025-03-10"}
- {id: 41, title: "Amazon Bedrock model card: DeepSeek-R1", url: "https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-deepseek-deepseek-r1.html", source: "AWS Documentation", date: "2026-10-20"}
- {id: 42, title: "DeepSeek R1 is now available on Azure AI Foundry and GitHub", url: "https://azure.microsoft.com/en-us/blog/deepseek-r1-is-now-available-on-azure-ai-foundry-and-github/", source: "Microsoft Azure Blog", date: "2025-01-29"}
- {id: 43, title: "Foundry Models sold by Azure in Azure Government", url: "https://learn.microsoft.com/en-us/azure/ai-foundry/openai/azure-government", source: "Microsoft Learn", date: "2026-09-01"}
- {id: 44, title: "DeepSeek V4 Pro, hosted in the U.S., is now available in Perplexity Computer", url: "https://www.linkedin.com/posts/perplexity-ai_deepseek-v4-pro-hosted-in-the-us-is-now-activity-7495585357397258241-RnD8", source: "Perplexity (LinkedIn)", date: "2026-08-18"}
- {id: 45, title: "GSA, Perplexity sign first direct-to-government deal", url: "https://www.gsa.gov/about-us/newsroom/news-releases/gsa-perplexity-sign-first-direct-to-gov-deal-11192025", source: GSA, date: "2025-11-19"}
- {id: 46, title: "Agencies now have to pay to use USAi", url: "https://www.nextgov.com/artificial-intelligence/2026/09/agencies-now-have-pay-use-usai/415816/", source: "Nextgov/FCW", date: "2026-09-03"}
- {id: 47, title: "sigstore/model-transparency (OpenSSF model signing)", url: "https://github.com/sigstore/model-transparency", source: "GitHub (OpenSSF/Sigstore)"}
- {id: 48, title: "CycloneDX Machine Learning Bill of Materials (ML-BOM)", url: "https://cyclonedx.org/capabilities/mlbom/", source: "OWASP CycloneDX"}
- {id: 49, title: "US CISA, G7 partners release Minimum Elements for AI Software Bills of Materials", url: "https://www.morganlewis.com/pubs/2026/06/us-cisa-g7-partners-in-europe-and-asia-release-minimum-elements-for-ai-software-bills-of-materials", source: "Morgan Lewis", date: "2026-06-16"}
- {id: 50, title: "Independence Tests for Language Models (Zhu et al.)", url: "https://arxiv.org/abs/2502.12292", source: arXiv, date: "2025-02"}
- {id: 51, title: "HuRef: HUman-REadable Fingerprint for Large Language Models", url: "https://arxiv.org/abs/2312.04828", source: "arXiv (NeurIPS 2024)", date: "2023-12"}
- {id: 52, title: "Detecting knowledge distillation lineage between language models (Rawat et al.)", url: "https://arxiv.org/abs/2607.09692", source: arXiv, date: "2026-06"}
- {id: 53, title: "Detecting and preventing distillation attacks", url: "https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks", source: Anthropic, date: "2026-02-23"}
- {id: 54, title: "RL identifies malware ML model hosted on Hugging Face (nullifAI)", url: "https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face", source: ReversingLabs, date: "2025-02-06"}
- {id: 55, title: "FAR 52.204-26 Covered Telecommunications Equipment or Services—Representation", url: "https://www.acquisition.gov/far/52.204-26", source: "Acquisition.gov", date: "2021-10"}
- {id: 56, title: "State of AI: an empirical study of 100T tokens on OpenRouter", url: "https://openrouter.ai/state-of-ai", source: "OpenRouter / a16z", date: "2025-12"}
- {id: 57, title: "Chinese AI models hit record 58% of US OpenRouter traffic", url: "https://aiweekly.co/alerts/chinese-ai-models-hit-record-58-of-us-openrouter-traffic", source: "AI Weekly (citing Bloomberg)", date: "2026-07-22"}
- {id: 58, title: "Qwen/Qwen2.5-7B-Instruct model tree", url: "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct", source: "Hugging Face", date: "2026-10-20"}
- {id: 59, title: "State of Open Models, Summer 2026", url: "https://huggingface.co/blog/state-of-open-models-summer-2026", source: "Hugging Face", date: "2026-08-14"}
- {id: 60, title: "8 plots that explain the state of open models", url: "https://www.interconnects.ai/p/8-plots-that-explain-the-state-of", source: "Interconnects (Nathan Lambert)", date: "2026-01-07"}
- {id: 61, title: "Cursor's Composer 2 was secretly built on a Chinese AI model", url: "https://venturebeat.com/technology/cursors-composer-2-was-secretly-built-on-a-chinese-ai-model-and-it-exposes-a", source: VentureBeat, date: "2026-03-22"}
- {id: 62, title: "Where does federal AI spending stand in 2026?", url: "https://brookings.edu/articles/where-does-federal-ai-spending-stand-in-2026/", source: Brookings, date: "2026-05-18"}
- {id: 63, title: "Little Tech Association letter against a Chinese open-weight AI ban", url: "https://thenextweb.com/news/little-tech-association-chinese-open-weight-ai-ban-anthropic-startups", source: "The Next Web", date: "2026-07-24"}
- {id: 64, title: "As US weighs response to Chinese AI, industry urges against broad open-weight restrictions", url: "https://techcrunch.com/2026/07/24/as-us-weighs-response-to-chinese-ai-industry-urges-against-broad-open-weight-restrictions/", source: TechCrunch, date: "2026-07-24"}
- {id: 65, title: "Pentagon workers used DeepSeek's chatbot for days before block", url: "https://news.bloomberglaw.com/ip-law/pentagon-workers-used-deepseeks-chatbot-for-days-before-block", source: "Bloomberg Law", date: "2025-01-31"}
:::
