---
eyebrow: FRONTIER AI · COMPUTE INFRASTRUCTURE · REGULATORY ASYMMETRY
title: "Grok 4.5 and the hardware-shielded frontier: SpaceX's monthly 1.5T V9 cadence under the de facto licensing regime"
deck: Elon Musk announced Grok 4.5 on June 28, 2026 — a 1.5-trillion-parameter model in private beta at SpaceX and Tesla. More consequentially, he committed to monthly from-scratch V9 retrains released by SpaceX for the rest of the year. This article examines how SpaceX/xAI's vertical integration (Colossus 1 and 2, C/C++ rewrites, orbital compute) creates a regulatory asymmetry against the backdrop of the June 12 Fable 5 export-control precedent.
lede: |
  On June 28, 2026, Elon Musk announced that Grok 4.5 — based on xAI's 1.5-trillion-parameter V9 foundation model, with supplementary Cursor developer data — was entering private beta at SpaceX and Tesla, with early evaluations showing performance "close to, perhaps exceeding Opus."[^1] That sentence alone would be significant. But the operative line came at the end: "Completely trained from scratch new models will be released by @SpaceX every month this year."[^1] This is not a product roadmap. It is a claim about compute sovereignty — one that becomes analytically tractable only when mapped against the emerging regulatory framework that, two weeks earlier, forced Anthropic to globally shut down Fable 5 and Mythos 5 three days after launch.[^2]
stats:
  - {label: Grok V9 parameter count, value: 1.5T, note: "Dense architecture"}
  - {label: Colossus 1 GPUs, value: "220,000+", note: "H100/H200/GB200"}
  - {label: Colossus 2 power, value: "1+ GW", note: "550k+ Blackwell GPUs"}
  - {label: Fable 5 lifetime, value: "~3 days", note: "June 9–12, 2026"}
  - {label: Monthly retrain cadence, value: "28 days", note: "From scratch per Musk"}
  - {label: Grok 5 target, value: "6T MoE", note: "Training on Colossus 2"}
---

## 01. The announcement: more than a model launch

The June 28 tweet was not an ordinary model release. Musk's thread — 5,241 replies, 33,919 likes, 4,334 retweets — packaged four distinct claims in a single post, each with different evidentiary weight and different implications for the broader AI landscape.[^1]

**Claim 1: Grok 4.5 approaches or exceeds Claude Opus.** The phrasing "close to, perhaps exceeding Opus" is deliberately ambiguous — it does not specify which Opus variant (Opus 4.6 or Opus 4.8), nor which benchmarks.[^1] One weak signal: the Engineering Lead for Grok, Yagiz Nizipli, responded to the thread saying "this one is extremely fast and extremely smart. can't wait to share with everyone!"[^3] A company insider claiming its own unreleased model is "very smart" is not independent corroboration. But the specific claim of Cursor data supplementation is falsifiable — if Grok 4.5's SWE-bench scores do not materially improve over Grok 4.3's reported 75%, the coding-data thesis weakens.[^4]

**Claim 2: Cursor data in supplemental training.** Cursor, with approximately 7 million daily active developers, generates millions of real-world coding traces — prompts, completions, diffs, accepted/rejected edits — when privacy mode is off (the default for many users).[^5] This is a genuinely differentiated training signal: whereas most code-training corpora are static GitHub snapshots, Cursor's corpus captures *process* — the iteration cycles, partial completions, and debug loops that reveal how code is actually written. The key unknown is volume: xAI and Cursor have not disclosed token counts, repository count, or total edit count for the supplemental training dataset.[^5]

**Claim 3: Private beta at SpaceX and Tesla.** This is the claim with the strongest operational signal. If Grok 4.5 is running real inference workloads inside two of the world's most demanding engineering organizations — Tesla's FSD stack and SpaceX's Starship telemetry — that is a genuinely different deployment stress test than Anthropic's Claude Code beta or OpenAI's ChatGPT code interpreter. The engineering cultures share lineage: SpaceX/Starlink engineers have been shifting to AI, contributing both reliability discipline and low-level optimization expertise.[^6]

**Claim 4: Monthly from-scratch V9 retrains.** This is the most consequential and least verified claim. A 1.5-trillion-parameter dense model retrained from scratch every ~28 days implies training throughput that no other frontier lab has publicly claimed. OpenAI's GPT-5.5 reportedly took months of continuous training on tens of thousands of GPUs. Anthropic's Fable 5 training timeline spanned multiple quarters.[^7] For context, Meta's Llama 4 (1T parameters, MoE) was trained on 61,440 H100s over approximately 21 days — and that was an MoE architecture where only a fraction of parameters activate per token.[^8] A 1.5T *dense* model retrained from scratch monthly would require roughly 3-4x the effective FLOPs of a Llama 4-scale run, compressed into a 28-day window. The compute requirement is staggering: roughly 8-10 exaFLOP-days per training run at FP8 precision, sustained across a full month.

:::callout(kind=warn, label="Skeptic's note")
The monthly-cadence claim is the hardest to verify without infrastructure data. If Colossus 1 (220k GPUs, 300 MW) is fully dedicated to training V9, the math almost works: at ~2 EFLOPS per GPU-day, 220k GPUs running continuously for 28 days produce ~12 exaFLOP-days — enough for a 1.5T dense model with a reasonable Chinchilla-optimal data budget (~30 trillion tokens). But Musk stated SpaceX moved xAI training to Colossus 2,[^9] and Colossus 1 capacity is now partially rented to Anthropic.[^10] The training allocation between the two clusters is opaque.
:::

:::kv
- {term: "Model architecture", def: "Dense (non-MoE) 1.5T parameters"}
- {term: "Supplemental data", def: "Cursor developer traces"}
- {term: "Beta venue", def: "SpaceX internal + Tesla internal"}
- {term: "Monthly cadence claim", def: "Each retrain from scratch"}
- {term: "V9 type variant", def: "V9-Medium at 1.5T (V9-Large pending)"}
- {term: "Public availability", def: "Not announced for Grok 4.5"}
:::

## 02. The compute stack: Colossus 1, Colossus 2, and the orbital frontier

The distinction between xAI and SpaceX on compute infrastructure has become blurred to the point of irrelevance. Earlier in 2026, xAI was absorbed into the broader SpaceX structure, with the combined entity increasingly referring to itself internally as "SpaceXAI."[^9] This consolidation turned xAI's training cluster into a SpaceX asset — and fundamentally changed both the economics and the politics of the operation.

**Colossus 1** (Memphis, Tennessee): Built at extreme speed through 2025, this facility houses more than 220,000 NVIDIA GPUs spanning H100, H200, and GB200 generations, with approximately 300 MW of power capacity.[^10] The facility was originally built exclusively for xAI's Grok training. But after the xAI→SpaceX merger and the stand-up of Colossus 2, SpaceX began commercializing the compute overhang. In May 2026, Anthropic announced a partnership with SpaceX to "substantially increase our compute capacity" — effectively renting Colossus 1 capacity.[^11] Dion Hinchcliffe, a close observer of enterprise infrastructure, noted that the deal reflected a strategic shift: "Compute itself is becoming a standalone business."[^9]

**Colossus 2** (also Memphis-area): The successor cluster is operating at a different magnitude entirely. It comprises over 550,000 NVIDIA Blackwell GPUs (primarily GB200 and GB300 variants) and is on track to expand toward one million GPUs, operating at more than 1 gigawatt of power capacity.[^12] Hardware investment is estimated at approximately $18 billion for the GPU fleet alone, before networking, cooling, and real estate.[^12] This is where the truly ambitious work happens: Grok 5 is being trained here as a 6-trillion-parameter Mixture-of-Experts model, alongside a larger 10-trillion-parameter variant.[^13] A 6T MoE model with ~10% activation per token would have roughly 600 billion active parameters per forward pass — comparable to the total size of the V9 dense model but with dramatically larger total knowledge capacity.

:::callout(kind=info, label="Scale comparison")
The Colossus 2 cluster at 1+ GW consumes as much electricity as approximately 800,000 US homes. At $0.05/kWh wholesale rate, the electricity bill alone is ~$1.3M per day, or ~$475M per year — for one facility.[^14] This is the energy cost of frontier AI, concentrated in a single campus.
:::

**The C/C++ rewrite and the GB300 play.** The June 2026 roadmap includes a plan to rewrite the entire Grok training and inference stack from Python (JAX/PyTorch layers) to C/C++, deleting "most software layers" and exact-mapping the model to NVIDIA's GB300 Grace Blackwell Ultra superchips.[^6] This is a defensible strategic move: NVIDIA's GB300 integrates Grace CPUs with Blackwell Ultra GPUs on a unified memory fabric that benefits enormously from low-level optimization. The current AI stack norm — Python frameworks with multiple abstraction layers — leaves 15-30% performance on the table compared to hand-optimized C++. If xAI closes that gap, the effective compute advantage over stack-constrained competitors could be equivalent to adding 50,000+ GPUs without spending a dollar on hardware.

**Orbital compute: AI1.** SpaceX has introduced AI1, described as the first generation of its AI satellite — an orbital datacenter.[^15] While details are sparse, the strategic logic is clear: terrestrial compute faces growing constraints on power availability, cooling, grid access, datacenter permits, and construction timelines. Orbital compute bypasses most of those constraints, at the cost of latency, radiation hardening, and launch mass. For training workloads with relaxed latency requirements, low-earth-orbit compute could become a complementary scaling layer — and SpaceX's launch monopoly (via Starship) gives it a cost advantage no other AI lab can match.

## 03. The cadence claim: what "monthly from scratch" requires

Musk's claim of monthly from-scratch V9 retrains demands closer scrutiny, because it is the claim that most directly separates xAI/SpaceX from every other frontier lab. The industry norm is quarterly-to-annual base model releases, with continuous fine-tuning and RL in between.

The reported V9-Medium training trajectory: the 1.5T parameter model completed its initial training run around June 5, 2026 — three times larger than the prior production model.[^4] Fine-tuning was underway at that point, with a public release expected within "days."[^4] From the June 28 announcement, the timeline fits: initial training completed early June, fine-tuning through mid-June, Cursor data supplementation in parallel, private beta by late June.

:::timeline
- {date: "2026-01", headline: "xAI merges into SpaceX structure", body: "xAI becomes a subsidiary inside SpaceX. Combined entity internally called SpaceXAI. Compute resources consolidated.[^9]"}
- {date: "2026-06-05", headline: "V9-Medium (1.5T) training completes", body: "Fine-tuning underway. Three times larger than prior model. Public release anticipated within days.[^4]"}
- {date: "2026-06-09", headline: "Fable 5 and Mythos 5 launch", body: "Anthropic releases its most capable models. Both globally suspended on June 12 by US export control directive.[^2]"}
- {date: "2026-06-12", headline: "Fable 5 export control", body: "US government orders access suspension for foreign nationals. First direct model-level export control in history.[^2]"}
- {date: "2026-06-28", headline: "Grok 4.5 announced in private beta", body: "Based on V9 foundation. Monthly from-scratch V9 cadence promised. Cursor supplemental data confirmed.[^1]"}
- {date: "Late 2026 (projected)", headline: "C/C++ rewrite delivers gains", body: "Truly massive gains predicted by Musk from stack rewrite + GB300 exact-mapping.[^6]"}
- {date: "Late 2026 (projected)", headline: "Grok 5 training completion", body: "6T MoE model training on Colossus 2. Larger 10T variant also in pipeline.[^12,13]"}
:::

:::callout(kind=warn, label="Risk factor")
The monthly cadence depends critically on uninterrupted access to the full Colossus 2 cluster. If Colossus 1 (partially rented to Anthropic) were reclaimed for training, or if Colossus 2 faced power constraints — Tennessee Valley Authority grid capacity is already stretched by the simultaneous buildout of multiple gigawatt-scale datacenters in the Memphis corridor — the cadence slips immediately. Power availability is the binding constraint on the entire frontier AI industry, not parameter count or GPU supply.[^16]
:::

**The data bottleneck.** Each monthly retrain requires not just compute but a fresh training corpus. Pre-training data availability is becoming a structural constraint: the frontier data supply chain — Scale AI, Surge AI, Mercor, Turing, Appen — already operates at capacity.[^17] Proprietary sources like Cursor traces provide differentiation but cannot substitute for the breadth of web-scale pre-training data. A monthly cadence implies either: (a) continuous data pipelining from user-generated sources (X platform posts, Tesla fleet data, SpaceX telemetry) that only the Musk ecosystem can provide, or (b) synthetic data generation at a scale no other lab has successfully deployed for pre-training (as distinct from post-training RL). Option (a) is the more plausible thesis: the Musk companies generate data — real-world operational data — at a volume and variety that no other AI lab's parent ecosystem can match.

## 04. The infrastructure business: SpaceX as the compute landlord

The May 2026 Anthropic-Colossus deal is arguably the most important signal about SpaceX/xAI's strategy that has emerged this year. One frontier model company — Anthropic, reportedly with a $30B+ annualized revenue run rate and a $965B IPO target[^18] — is renting compute from another frontier competitor's infrastructure.[^10,11]

This is not a partnership of equals. It is a landlord-tenant relationship in the compute layer. And it mirrors the original AWS playbook: Amazon built internal infrastructure, discovered it had surplus capacity, monetized it, and the resulting business (AWS) became larger than Amazon's retail operations. SpaceX/xAI appears to be executing the same strategy with AI compute.

:::kv
- {term: "Colossus 1 capacity", def: "220k+ GPUs, ~300 MW"}
- {term: "Tenant", def: "Anthropic (Claude models)"}
- {term: "Colossus 2 use", def: "xAI training (Grok 5)"}
- {term: "Colossus 2 scale", def: "550k+ GPUs, 1+ GW"}
- {term: "GPU investment", def: "~$18B (Colossus 2)"}
- {term: "Business model", def: "Internal training + external rental"}
:::

The strategic implications are subtle but important. By renting Colossus 1 to Anthropic, SpaceX/xAI accomplishes three things simultaneously: (a) it generates cash flow from an asset that would otherwise sit partially idle during the Colossus 2 build-out, (b) it creates dependency — Anthropic's inference and fine-tuning workloads now run on infrastructure that Musk controls, and (c) it gives SpaceX/xAI a privileged window into the compute demands and growth trajectory of a competitor. This last point is the closest the AI industry has come to the "Amazon selling diapers and watching what parents buy" data advantage — except here the "diapers" are compute cycles and the "parents" are Anthropic's entire model fleet.

The business model extends to orbital compute. If AI1 — the orbital datacenter satellite[^15] — reaches operational capability, SpaceX would offer compute that is physically inaccessible to any regulator or competitor without its own launch capacity. The latency penalty (several milliseconds to LEO, vs. sub-millisecond on the same rack) is irrelevant for training workloads. The regulatory inaccessibility is extremely relevant.

## 05. The regulatory asymmetry: Fable 5, the June 2 EO, and the SpaceX exception

This section examines the central asymmetry thesis: that the same US government that shut down Anthropic's Fable 5 three days after launch has both the incentive and the structural relationship to treat SpaceX/xAI's monthly frontier model releases differently — whether by explicit policy design or by the accumulated effect of procurement politics, personal relationships, and institutional capture.

**The Fable 5 precedent.** On June 12, 2026, the US government issued an export control directive ordering Anthropic to "suspend all access to Fable 5 and Mythos 5 by any foreign national, whether inside or outside the United States."[^2] The legal basis was a narrow, non-universal jailbreak technique that Anthropic characterized as exposing "a small number of previously known, minor vulnerabilities" — capabilities the company argued were "widely available from other models (including OpenAI's GPT-5.5)."[^2] The directive cited "national security authorities" but did not specify a particular statute. Model weights have no established Export Control Classification Number under the Commerce Control List.[^19] The legal novelty of the action is substantial — it is the first time a frontier AI model, rather than the hardware used to train or run it, has been the direct target of an export control action.

**The June 2, 2026 AI Executive Order.** On June 2, President Trump signed an executive order creating a mandatory 30-day pre-release government access framework for cybersecurity review of frontier models.[^20] The order explicitly states it does not authorize mandatory licensing, preclearance, or permitting for AI model release.[^20] But the de facto effect — a mandatory waiting period during which the government can evaluate and, potentially, block deployment — constitutes a licensing regime in all but name. The order followed by three days the CAISI pre-release evaluation MOUs signed by four frontier labs, including Anthropic and OpenAI.[^21]

**NSPM-11 (June 5, 2026).** Three days after the EO, the White House issued National Security Presidential Memorandum 11, "Artificial Intelligence in the National Security Enterprise."[^22] Most of NSPM-11 is about accelerating AI adoption across defense and intelligence. But two provisions are directly relevant. Its *Assurance* pillar requires that any fielded AI system "cannot be disabled, degraded, or materially modified without federal knowledge and approval." Its *Accountability* pillar requires a human chain of command for AI use in military contexts. Taken together, these provisions mean that any AI model deployed in a US national-security context becomes, in effect, government-controlled software — subject to federal override of the developer's own safety or policy constraints.[^22]

**SpaceX's position in the national-security AI ecosystem.** SpaceX was included in the Department of War's classified-network AI agreements announced in May 2026, alongside OpenAI, Google, NVIDIA, Microsoft, AWS, and Oracle.[^23] Anthropic was notably absent from those agreements — a direct consequence of its refusal to accept Pentagon terms on mass domestic surveillance and fully autonomous weapons, which led to Trump ordering a federal ban on Claude in February 2026 and the Pentagon labeling Anthropic a "supply chain risk."[^24,25] A federal judge temporarily blocked the supply-chain designation, writing that the measures "appeared designed to punish Anthropic" and bore the hallmarks of retaliation.[^26]

The asymmetry is structural:

:::compare
- {role: LOWEST, name: Anthropic, value: "Export-controlled"}
- {role: HIGHEST, name: "SpaceX/xAI", value: "Classified-network partner"}
- {role: SUBJECT, name: xAI, value: "Both train competitive frontier"}
:::

:::stats
- {label: "Anthropic: pre-release review choice", value: "Mandatory (EO)", note: "30-day framework June 2 [^20]"}
- {label: "SpaceX: DoW classification", value: "Classified partner", note: "May 2026 [^23]"}
- {label: "Anthropic: federal status", value: "Supply-chain risk", note: "Feb 2026; blocked by injunction [^26]"}
- {label: "Trump on Anthropic", value: "\"Leftwing nut jobs\"", note: "Truth Social, Feb 2026 [^25]"}
- {label: "Musk-Trump relationship", value: "Aligned", note: "Repeated public praise"}
- {label: "SpaceX AI export controlled?", value: "Not yet", note: "No known directive"}
:::

The political economy is straightforward. Musk and Trump have been publicly aligned throughout 2026. Musk endorsed Trump's 2024 presidential campaign, donated heavily to the administration's super-PACs, and has been a visible presence in Trump's technology policy circle. Meanwhile, the Trump administration has been hostile to Anthropic since early 2026, with Trump calling Anthropic "Leftwing nut jobs" and ordering federal agencies to cease using Claude.[^25] In this environment, the same government that imposed an emergency export control on Anthropic's model three days after its June 9 launch is also the government that welcomed SpaceX into its classified-network AI ecosystem.

The concrete question: if SpaceX/xAI releases a frontier model every month through the rest of 2026, does the 30-day pre-release review framework (June 2 EO) apply? The order applies to "covered frontier models" — a threshold defined by compute and capability metrics. The V9 model at 1.5T parameters, trained on Colossus 2, almost certainly exceeds any reasonable threshold. But enforcement is discretionary: the government must issue the review request, and SpaceX must comply. If the government chooses not to exercise its review authority for SpaceX/xAI models — or if the review is perfunctory — the asymmetry becomes explicit.

**The OpenAI co-benefit problem.** The Fable 5 shutdown also benefited OpenAI, which competes directly with Anthropic in the enterprise AI market. OpenAI reported a $1 trillion IPO target, and its GPT-5.6 model was reportedly subjected to a government request that it be initially limited to government-approved partners.[^27] But OpenAI was not export-controlled — it was consulted. This creates a hierarchy: OpenAI faces *guidance*, Anthropic faces *directives*, and SpaceX/xAI faces neither, because SpaceX is already on the inside of the national-security AI infrastructure.

## 06. The data-and-distribution moat

Beyond compute and regulatory asymmetry, the Musk ecosystem has two structural advantages that are harder to replicate than model architecture.

**The X platform as distribution channel.** Grok ships inside X Premium, which has tens of millions of paid subscribers. Every new Grok model version reaches those subscribers instantly — no enterprise sales cycle, no cloud marketplace listing, no procurement review. The distribution cost is zero; the switching cost for users is zero (it's bundled). Competitors must negotiate cloud partnerships (Anthropic with AWS/GCP, OpenAI with Azure) and enterprise procurement contracts.[^10]

**Multi-modal data from real-world operations.** xAI has access to training data sources that no competitor can match: the full X firehose (real-time global text and media), Tesla's FSD fleet (millions of miles of real-world driving data, sensor streams, edge-case logs), and SpaceX telemetry (Starship launch data, Starlink network traffic patterns). This is not synthetic data or licensed corpora — it is operational telemetry from deployed systems at planetary scale. The Cursor coding-data deal extends this advantage to software development: a window into how 7 million developers actually write code, not just what gets committed to GitHub.[^5]

:::callout(kind=info, label="The moat")
No other frontier lab has access to real-time data from an operating global communications network (Starlink), a self-driving car fleet (Tesla), a spacecraft telemetry system (Starship), and a social media platform (X) — all under common ownership. The training data advantage is not model architecture; it is *operational scope*.
:::

## 07. What could break the thesis

The central thesis of this article — that SpaceX/xAI's monthly V9 cadence is both technically plausible and structurally shielded by regulatory/political asymmetry — faces several real counter-arguments.

**Counter-argument 1: The compute may not be there.** Colossus 2 is shared between training the 6T-parameter Grok 5 MoE model and running the monthly V9 retrains. These are not compatible workloads. A single training run of a 6T MoE model at scale can occupy the full cluster for months. The math only works if SpaceX has partitioned Colossus 2 into separate training and fine-tuning segments, or if the monthly V9 models are significantly smaller than the 1.5T claim (distilled versions, for instance). The monthly cadence claim may be directionally true — monthly *fine-tunes* or *model updates* — but the "completely trained from scratch" wording may not survive independent auditing.

**Counter-argument 2: The regulatory shield is not guaranteed.** Administrative relationships change. If the Trump administration were to apply the same Fable 5 standard to a SpaceX/xAI model — and a national-security finding against a Musk-affiliated model would be politically explosive — the result would be the most consequential test of the model-level export control regime yet. The Fable 5 precedent is a sword that can cut both ways: it established that the government can restrict any frontier model it chooses. That authority does not expire when the target company is politically connected.

**Counter-argument 3: The C/C++ rewrite is a flag-plant, not a delivery.** Rewriting a multi-million-line AI stack from Python to C/C++ while simultaneously pushing monthly model releases and training a 6T MoE model is a resource allocation problem of the first order. xAI/SpaceX has excellent engineering talent, but the stack rewrite alone is a multi-quarter project if done properly. The "truly massive gains in approximately 3 months" timeline (per Musk's June 29 follow-up)[^6] is aggressive even for a well-resourced team.

**Counter-argument 4: The monthly cadence may degrade quality.** A monthly from-scratch retrain cycle prioritizes velocity over iteration depth. Every frontier lab that has achieved top-tier benchmark scores (OpenAI with GPT-5.5, Anthropic with Fable 5, Google with Gemini 3.5) has invested heavily in post-training: RLHF, constitutional AI, targeted data augmentation, safety red-teaming. A 28-day cycle compresses all of that into a fraction of the normal timeline. The result may be models that achieve competitive single-benchmark scores but lack the robustness, safety alignment, and niche competency that comes from extended post-training. The prediction market asking "Which company has the best AI model at the end of 2026?" implies a 14% probability for Google, with xAI implied at lower but unquantified probability in the open set of competitors.[^28]

**Counter-argument 5: The enterprise adoption gap is structural.** Grok holds approximately 6% enterprise AI adoption versus established leaders.[^4] Enterprise procurement cycles run 6-18 months; security reviews, compliance certifications, and data-residency requirements are not solved by model quality alone. Even if Grok 4.5 genuinely matches or exceeds Opus on benchmarks, enterprise adoption will lag by quarters at minimum. The monthly cadence matters less if the distribution channel is mostly consumers on X Premium.

:::bars
- {label: OpenAI, value: "55%", pct: 100}
- {label: Anthropic, value: "47%", pct: 85}
- {label: Google, value: "28%", pct: 51}
- {label: xAI/Grok, value: "6%", pct: 11}
- {label: Others, value: "14%", pct: 25}
:::
:::source(label="Caveat")
Enterprise adoption figures from June 2026 industry reporting; survey methodology and sample sizes not disclosed. Directionally corroborated by multiple outlets but exact percentages should be treated as estimates.[^4]
:::

:::callout(kind=danger, label="The open question")
The central open question is whether SpaceX's monthly V9 releases will trigger the same Fable 5 response. If they proceed without government restriction through Q3 2026, the asymmetry is confirmed: the frontier licensing regime applies selectively based on political alignment, not technical risk. If the government does restrict a SpaceX/xAI model, the asymmetry collapses — but the constitutional and procedural questions raised by the Fable 5 precedent remain unresolved for everyone.
:::

---

## References

:::references
- {id: 1, title: "Elon Musk — Grok 4.5 announcement", url: "https://x.com/elonmusk/status/2071184354756477041", source: "X/Twitter (primary)", date: "2026-06-28"}
- {id: 2, title: "Statement on the US government directive to suspend access to Fable 5 and Mythos 5", url: "https://anthropic.com/news/fable-mythos-access", source: "Anthropic (primary)", date: "2026-06-12"}
- {id: 3, title: "Yagiz Nizipli — Grok 4.5 comment", url: "https://x.com/yagiznizipli/status/2071364044280197432", source: "X/Twitter (primary)", date: "2026-06-28"}
- {id: 4, title: "Global Wire Live — V9-Medium training complete", url: "https://x.com/GlobalWireLive/status/2062796857915346970", source: "X/Twitter (secondary)", date: "2026-06-05"}
- {id: 5, title: "Cursor developer traces discussion", url: "https://x.com/Rose_M_Leo/status/2071453009314246957", source: "X/Twitter (secondary)", date: "2026-06-29"}
- {id: 6, title: "Nagesh S — Grok C/C++ rewrite and GB300 optimization", url: "https://x.com/horanaS/status/2071456221186396213", source: "X/Twitter (secondary)", date: "2026-06-29"}
- {id: 7, title: "Claude Fable 5 and Claude Mythos 5", url: "https://anthropic.com/news/claude-fable-5-mythos-5", source: "Anthropic (primary)", date: "2026-06-09"}
- {id: 8, title: "Meta Llama 4 — training compute analysis", url: "https://ai.meta.com/blog/llama-4/", source: "Meta (primary)", date: "2025-04"}
- {id: 9, title: "Dion Hinchcliffe — Anthropic/SpaceX compute deal analysis", url: "https://x.com/dhinchcliffe/status/2052097490015670679", source: "X/Twitter (secondary)", date: "2026-05-06"}
- {id: 10, title: "Jack Vĩ — Anthropic/Colossus compute analysis", url: "https://x.com/jackvi810/status/2052248678354833827", source: "X/Twitter (secondary)", date: "2026-05-07"}
- {id: 11, title: "Claude — Anthropic/SpaceX compute partnership announcement", url: "https://x.com/claudeai/status/2052060691893227611", source: "X/Twitter (primary)", date: "2026-05-06"}
- {id: 12, title: "Fuzzygoat — Colossus 2 specs and Grok 5 training", url: "https://x.com/Fuzzygoat/status/2069014549395644672", source: "X/Twitter (secondary)", date: "2026-06-22"}
- {id: 13, title: "Shinka AI — Grok 5 MoE architecture analysis", url: "https://x.com/ShinkaIoT/status/2065583785958314179", source: "X/Twitter (secondary)", date: "2026-06-12"}
- {id: 14, title: "EIA — Industrial electricity costs", url: "https://www.eia.gov/electricity/monthly/", source: "US Energy Information Administration (primary)", date: "2026"}
- {id: 15, title: "SE Robinson Jr — SpaceX AI1 orbital datacenter", url: "https://x.com/SERobinsonJr/status/2064491214020161630", source: "X/Twitter (secondary)", date: "2026-06-09"}
- {id: 16, title: "TVA datacenter capacity constraints", url: "https://www.tva.com/environment/grid-capacity", source: "Tennessee Valley Authority (primary)", date: "2026"}
- {id: 17, title: "The data behind the models: inside the industry that sells human cognition to frontier AI labs", url: "https://ara.guzus.xyz/research/generative/2026-06-22T061332--frontier-ai-data-supply-chain.html", source: "ARA Research (secondary)", date: "2026-06-22"}
- {id: 18, title: "Anthropic confidential S-1 filing", url: "https://www.bloomberg.com/news/2026-06-01/anthropic-secretly-files-for-ipo", source: "Bloomberg (secondary)", date: "2026-06-01"}
- {id: 19, title: "Executive Order 14110 — Safe, Secure, and Trustworthy Development of AI", url: "https://www.whitehouse.gov/briefing-room/2023/10/30/", source: "White House (primary)", date: "2023-10-30"}
- {id: 20, title: "Trump AI Executive Order — Promoting Advanced AI Innovation and Security", url: "https://www.whitehouse.gov/", source: "White House (primary)", date: "2026-06-02"}
- {id: 21, title: "CAISI Pre-Release Frontier-AI Evaluation MOUs", url: "https://www.nist.gov/caisi", source: "NIST / CAISI (primary)", date: "2026-05-05"}
- {id: 22, title: "INTRANA — NSPM-11 AI national security analysis", url: "https://x.com/intrana/status/2070628174233235841", source: "X/Twitter (secondary)", date: "2026-06-26"}
- {id: 23, title: "Ollobrains — Trump/OpenAI/Anthropic detailed timeline", url: "https://x.com/ollobrains/status/2065753665009516636", source: "X/Twitter (secondary)", date: "2026-06-13"}
- {id: 24, title: "Trump orders ban on government use of Anthropic", url: "https://www.washingtonpost.com/technology/2026/02/27/anthropic-trump-ban-federal-agencies/", source: "Washington Post (secondary)", date: "2026-02-27"}
- {id: 25, title: "Anthropic Wikipedia entry", url: "https://en.wikipedia.org/wiki/Anthropic", source: "Wikipedia (secondary)", date: "2026"}
- {id: 26, title: "CNBC — Anthropic Pentagon lawsuit injunction", url: "https://www.cnbc.com/2026/03/26/anthropic-wins-injunction-trump-pentagon.html", source: "CNBC (secondary)", date: "2026-03-26"}
- {id: 27, title: "Axios — GPT-5.6 government-approved partners", url: "https://www.axios.com/", source: "Axios (secondary)", date: "2026-06"}
- {id: 28, title: "Polymarket — Best AI model end of 2026", url: "https://polymarket.com/event/which-company-has-best-ai-model-end-of-2026", source: "Polymarket (prediction market)", date: "2026-06"}
:::
