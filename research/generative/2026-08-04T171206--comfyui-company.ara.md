---
eyebrow: REPORT · COMPANY
domain: software
title: "Comfy Org: the $500M company that won the substrate and forgot to build the tollbooth"
deck: ComfyUI is the default runtime for open-weight generative media. Comfy Organization, Inc. is a Delaware corporation with a metered GPU business and no disclosed revenue. These are not the same asset.
lede: |
  In April 2026 Comfy Org announced a $30 million financing at a $500 million
  valuation, bringing total funding to $47 million — a number its own
  same-day press release put at $48 million. The company behind ComfyUI has a
  genuine claim to owning the layer every open-weight image, video and audio
  model passes through on its way to a working machine. What it does not have,
  on any public evidence, is a business that taxes that position: the workflow
  format is freely executable by anyone, the API-node margin is priced at
  provider list, the enterprise tier gives that margin away by design, the
  largest national market is served end-to-end by Alibaba and Tencent, and the
  ~5,000 node authors whose work makes the moat are paid nothing. In the same
  year, the company shipped an app mode that hides the node graph, an agentic
  layer that replaces it with natural language on the billed path first, and a
  contributor licence agreement whose own bot names a future relicense away
  from GPL-3.0 as the benefit that matters most.
stats:
  - {label: Valuation, value: $500M, note: "Apr 2026 · $30M round led by Craft"}
  - {label: Total raised, value: $47M, note: "$48M per the same-day release"}
  - {label: Disclosed revenue, value: "None", note: "no first-party figure, ever"}
  - {label: GitHub stars, value: 123.6, unit: "k", note: "as of 2026-08-05"}
  - {label: Registry node packs, value: "4,995", note: "vs 60,000+ nodes claimed"}
---

## 01. The short answer

Two entities share one name, and almost every confused claim about "the ComfyUI company" comes from collapsing them.

:::callout(kind=info, label="The short answer")
- **The project** is ComfyUI, a GPL-3.0 node-graph execution engine for diffusion and video models, first released January 2023 by a solo developer, now at 123,602 GitHub stars as of 2026-08-05.[^6]
- **The company** is Comfy Organization, Inc., a Delaware corporation headquartered at 201 Spear Street, San Francisco — legally distinct from the project it stewards.[^13]
- **The money**: $47 million raised in total, most recently $30 million at a $500 million valuation announced 2026-04-24, led by Craft.[^1]
- **The revenue**: never disclosed, in any first-party document, ever — and absent from Sacra's April 2026 equity research too.[^5]
- **The business**: Comfy Cloud, a metered GPU service starting at $20/month, plus credit-billed Partner Nodes and an unpriced enterprise tier.[^15]
:::

The funding history is worth reconstructing because the public record is inconsistent and no tracker is authoritative. Comfy Org never announced its 2024 seed contemporaneously; it disclosed the whole pre-2026 stack once, as "$17 million," on 2025-09-16, from Pace Capital, Chemistry, Abstract Ventures and others.[^3] That $17 million plus April's $30 million reproduces the company's own $47 million total exactly — which makes the blog the most internally consistent account available, even as its own press release the same day said $48 million.[^1] [^2] TechCrunch compresses the pre-2026 capital into a single "$19 million Series A" in late 2024; the company has never used a series label in any first-party document.[^4]

The leadership split is the second thing routinely got wrong. The pseudonymous creator "comfyanonymous" — named by the company as Yannik Marek — is described in its own funding post as "cofounder and the creator of ComfyUI," not as chief executive.[^1] The CEO is Yoland Yan, a different person who announced the company's formation eighteen months after the software existed.[^12]

What follows tests one question: whether the position ComfyUI occupies can be converted into the revenue a $500 million mark assumes. The registry, at 4,995 published node packs as of 2026-08-05, is the clearest measure of the position.[^9] Everything after this section is about the conversion step.

## 02. The anti-usability bet

ComfyUI exists because one developer with no machine-learning background deliberately optimized for power over ease at the exact moment every competitor was optimizing for ease — and the company that now owns it was assembled around him eighteen months later, by different people.

The provenance is unusually crisp. GitHub records the project as created at 2023-01-17T03:15:56Z.[^6] The creator's own account narrows it further: "So I started writing the code January one. 2023, and then I released the first version on GitHub, January 16th, 2023."[^10] Roughly sixteen days separate the first line of code from a public release that would go on to become the default execution layer for open-weight generative media.

What makes that release consequential is not the speed but the design posture. The stated founding thesis was an inversion of the entire 2023 field:

:::quote(attr="Yannik Marek, creator of ComfyUI")
everyone was trying to make like easy to use interface... let me try to make a powerful interface that's not easy to use
:::

That is a deliberate anti-usability bet, and it was placed by someone with no credential in the domain. The creator spent roughly a decade writing C++ at his father's dental implant factory in Quebec City, and says plainly: "I hadn't written a line of PyTorch before that."[^10] The absence of ML priors is arguably why the graph abstraction survived — a practitioner steeped in existing tooling would likely have reached for the existing tooling's shape.

The tidy origin story should be discounted, though, because the creator has told it two different ways. His own contemporaneous blog post from May 2023 gives a straightforwardly hobbyist motivation — "The reason I started writing ComfyUI is that I got a bit too addicted to generating images with Stable Diffusion" — and makes no mention of any competing interface's architectural limits.[^11] The retrospective framing of ComfyUI as an intentional answer to what everyone else was building is therefore at least partly retrofitted. That matters for valuation: a position arrived at by accident is weaker evidence of institutional design capability than one arrived at by strategy.

The corporate layer arrived much later, and from elsewhere. Stability AI hired the creator in June 2023 — roughly five months *after* first release — so the causal arrow runs the other way than is usually assumed: ComfyUI existed first, and SDXL's base-plus-refiner chaining happened to require exactly the pipeline composition ComfyUI already did.[^10]

:::timeline
- {date: 2023-01, headline: "First public release", body: "Sixteen days from first commit to GitHub publication."}
- {date: 2023-06, headline: "Stability AI hires the creator", body: "Five months after release; ComfyUI predates the relationship."}
- {date: 2024-04, headline: "Comfy-Org GitHub organization appears", body: "The corporate account predates the public announcement."}
- {date: 2024-06, headline: "Comfy Org announced", body: "A coalition of six separately-credited ecosystem maintainers."}
- {date: 2025-03, headline: "ComfyUI-Manager transferred in", body: "Moved to Comfy-Org; no compensation terms disclosed."}
- {date: 2025-09, headline: "$17M disclosed", body: "First publicly confirmed institutional round."}
- {date: 2026-04, headline: "$30M at $500M valuation", body: "The mark this analysis interrogates."}
:::

Comfy Org was announced on 2024-06-18 — by Yoland Yan, not by the creator — as a coalition of six separately-credited maintainers: comfyanonymous (ComfyUI), mcmonkey4eva (SwarmUI), Dr.Lt.Data (ComfyUI-Manager), pythongosssss, robinken (Comfy Registry) and yoland68 (ComfyCLI): "Super excited for the new chapter of our journey! We are forming Comfy Org with an insane team".[^73] The April 2026 funding post names Yannik Marek as "cofounder and the creator of ComfyUI" — not CEO, a title held by Yoland Yan.[^1,12]

The coalition has since only partly consolidated. ComfyUI-Manager was transferred into the Comfy-Org organization on 2025-03-29 with Dr.Lt.Data continuing to maintain it, and no compensation, equity or employment terms were disclosed.[^70] SwarmUI never came in at all: it remains at `mcmonkeyprojects/SwarmUI` under the MIT license, copyright Alex "mcmonkey" Goodwin, with mcmonkey4eva absent from the public Comfy-Org roster and no departure ever announced.[^89]

This matters because the founding bet and the current product thesis point in opposite directions. The CEO's pitch to TechCrunch is explicitly a usability argument — "you ask for something, it [gets only] 60% – 80% there... But to change that remaining 20%, you have to try this slot machine".[^4] The asset was built by refusing to be easy; the company is being sold on making it easy.

## 03. The engine, not the interface

The most common category error about ComfyUI is that it is a user interface with a Python backend; it is a graph execution engine with a browser front end, and that distinction is what a competitor would actually have to rebuild.

The engine does incremental recomputation, not rendering. `comfy_execution/caching.py` implements result caching keyed on structural input signatures, with several distinct eviction policies including a hierarchical cache, an LRU cache and one that evicts under RAM pressure.[^84] The user-visible consequence is stated in the project's own README: "Only re-executes the parts of the workflow that changes between executions."[^83] For an artist iterating on the last node of a twelve-stage graph, that is the difference between a two-second change and a two-minute one.

The second engine capability is memory management. ComfyUI performs partial weight residency and CPU offloading at the tensor level, claiming in its README to "automatically run large models on GPUs with as low as 1GB vram with smart offloading."[^83] Treat the specific number as a marketing floor rather than a spec: no model, resolution or throughput is attached to it, and at that budget most weights stream from CPU on every step. The capability is real; the headline figure is unfalsifiable as stated.

Engine-level features have landed as dated releases rather than as marketing: asynchronous API nodes in v0.3.50 (2025-08-13), subgraph support in v0.3.51 (2025-08-20), and the V3 node schema beginning v0.3.52 (2025-08-23), which gates dynamic inputs and async support that V1 nodes cannot reach.[^71] Release cadence then accelerated sharply through 2026 — the project targets a weekly Monday release, and the minor version went from v0.7.0 at the end of 2025 to v0.30.0 by 2026-08-03.[^71] [^83]

:::exhibit(num="Exhibit 1", title="Minor-version releases accelerated through 2026", subtitle="ComfyUI minor version number, by release date", source="ComfyUI changelog and releases page", note="The v0.3.x to v0.7.0 jump in December 2025 was an unexplained numbering-scheme change and is excluded from the series.")
:::line-chart(title="ComfyUI minor version", subtitle="docs.comfy.org changelog")
x: 2025-12-31,2026-01-21,2026-02-24,2026-04-27,2026-08-03
Minor version: 7,10,15,20,30
:::
:::

The commercial surface grew alongside it. The Comfy Registry launched 2025-01-03 with more than 800 publishing node authors, giving the ecosystem a versioned distribution channel it previously lacked.[^24] Partner Nodes followed, letting a workflow call roughly 35 commercial providers from inside the graph against a prepaid credit balance.[^16] Comfy Cloud went to general availability on 2026-03-04, at which point the company claimed the custom nodes powering "~90% of local workflows" were available in the hosted environment.[^17] Of that stack, the client side — core, Manager, `comfy-cli`, frontend, Desktop — is GPL-3.0; the credits service, cloud runtime and registry hosting are proprietary.[^6]

The counterpoint is maintenance load, and it is visible in the same API that reports the stars. As of 2026-08-05 the repository carries 4,422 open issues against 123,602 stars.[^6] A weekly release cadence driven by external model launches is not a schedule the company controls, and every accelerated release is a compatibility surface for 4,995 third-party node packs. The engine is a genuine asset; it is also a treadmill with no brake.

Why this matters: everything defensible about ComfyUI lives here, in scheduling, caching and memory behaviour — not in the workflow file, which as the next sections show is a JSON blob anyone can execute.[^77]

## 04. Why every open-weight model lands here first

ComfyUI has genuinely become the default *end-user runtime* for open-weight generative media — but the evidence behind the "every model ships a ComfyUI workflow" slogan is thinner than it sounds, because most day-0 posts are published by Comfy Org rather than by the labs, and where both are datable, Diffusers is still the reference implementation.

Comfy Org states the goal plainly in its own funding announcement: {accent}"Every major model release should work in ComfyUI on day one."{/}[^1] The distinction that matters for valuation is who does the work and who says so. The same post names zero model labs as partners.[^1] A lab advertising ComfyUI in its own launch material is a commitment; Comfy Org publishing its own day-0 support post is evidence of Comfy Org's engineering speed, which is a different and more perishable asset.

The strong cases exist. Black Forest Labs' FLUX.1 launch post is the earliest clean instance of a lab's own material carrying the endorsement — verbatim, "Moreover we're happy to have day-1 integration for ComfyUI."[^33] Stability AI's SD 3.5 launch on 2024-10-22 listed ComfyUI among five access platforms and did not mention Diffusers at all; the qualifier is that the other four were hosted APIs, so ComfyUI was the only local runtime it could name.[^85] Tencent's Hunyuan team goes furthest, shipping a first-party ComfyUI usage guide and workflow templates inside its own HunyuanVideo-1.5 repository under the Tencent Hunyuan Community License — a lab spending engineering budget on the ComfyUI surface rather than linking to it.[^86]

The weak cases are more numerous. Lightricks' LTX-Video was announced as "natively supported in ComfyUI on Day 1!" — in a post written by Comfy Org, not by Lightricks.[^36] For MiniMax H3 on 2026-08-03, Comfy Org did the model-compression engineering itself, finding that the modulation weights, "(~40% of the total parameters) could be pruned and replaced with a functionally equivalent lookup table," cutting memory from 123.6 GB to 42.5 GB so the model runs on an RTX 3060.[^37] No partnership with MiniMax is stated anywhere in that post.[^37] That is impressive unpaid integration labour, not a distribution agreement.

The counter-evidence is decisive on the narrower claim. Alibaba's Qwen-Image repository credits Diffusers, not ComfyUI, with true day-zero support — "Diffusers has supported Qwen-Image since day 0" — while the ComfyUI entry appears as a later dated changelog line on 2025.08.05.[^35] NVIDIA's Cosmos family, released 2025-01-06, did not get native ComfyUI support until a Comfy Org post on 2025-01-17: eleven days, not zero.[^87] Even the best-behaved case is co-equal rather than preferential — Alibaba's Wan2.2 repository logged ComfyUI and Diffusers integrations on the same day, 2025-07-28, treating them as parallel checklist targets.[^34] Comfy Org published its own Wan2.2 day-0 post that same day.[^38]

| Model | Released | ComfyUI support | Published by |
|---|---|---|---|
| *FLUX.1 | 2024-08-01 | Day-1 | Black Forest Labs |
| LTX-Video | 2024-11-22 | Day-1 | Comfy Org |
| NVIDIA Cosmos | 2025-01-06 | +11 days | Comfy Org |
| *Wan 2.2 | 2025-07-28 | Day-0 | Both |
| Qwen-Image | 2025-08-05 | After Diffusers | Alibaba |
| MiniMax H3 | 2026-08-03 | Day-0 | Comfy Org |

:::source
Lab launch posts and repositories; Comfy Org announcements.[^33,36,87,34,38,35,37]
:::

Lead investor Craft Ventures, which led the $30M round and is talking its book, frames the position as infrastructural: "Comfy is more analogous to GitHub than it is to a design tool."[^68] The honest reading of the record above is narrower. ComfyUI is where open-weight models go to be *run* by end users; Diffusers remains where they go to be *implemented*. That matters because the substrate claim underwriting the $500M mark rests on a position no lab has contracted for, that Comfy Org largely maintains at its own expense, and that no counterparty is obliged to preserve.

## 05. The metrics that don't survive an audit

Every headline number in Comfy Org's funding announcement is either unverifiable by construction, contradicted by the company's own same-day press release, or counting a different object than the reader assumes.

The announcement's community paragraph reads, verbatim: "That community now spans 4 million users, 60,000+ nodes built by contributors, and 150,000+ daily downloads."[^1] Each of the three is doing different work, and none is defined. ComfyUI is self-hosted open-source software with no account requirement and opt-in desktop telemetry, so there is no mechanism by which a true unique-user count could be observed — the post distinguishes nowhere between installs, monthly actives, unique devices and cumulative downloads, and states no measurement method at all.[^1] A "user" here is whatever the reader assumes it is.

The internal contradiction is sharper, because it does not require any outside data to detect. The company's GlobeNewswire release disagrees with its own blog twice on the same day: the release subheadline says "50K daily downloads" where the blog says "150,000+ daily downloads" — a 3x gap — and the release reports total funding of $48 million against the blog's $47 million.[^2] [^1] Neither figure was subsequently reconciled.

The node count counts a third object again. The official Comfy Registry API reports a `total` of 4,995 published node packs as of 2026-08-05, roughly one-twelfth of the advertised "60,000+ nodes."[^9] Both can be true: a pack bundles multiple node classes, and ~12 classes per pack closes the gap arithmetically. But the company never states the denominator, so the reader is left to assume the registry is the source of the 60,000 when it is not.

| Denominator | Figure | As of |
|---|---|---|
| Registry node **packs** (live API) | 4,995 | 2026-08-05 |
| *Community "nodes" (company claim) | 60,000+ | 2026-04-24 |

The registry figure is a live, monotonically growing counter: two fetches on 2026-08-05 returned 4,993 and 4,995 hours apart, so treat it as "about five thousand packs" rather than a fixed number.[^9]

The one metric anyone can check independently is GitHub stars — and it ranks a dead project first. As of 2026-08-05 the ComfyUI repository carries 123,602 stars and 14,603 forks, last pushed 2026-08-04.[^6] AUTOMATIC1111's stable-diffusion-webui carries 164,387 stars and 30,545 forks, more than ComfyUI on both counts — while its `master` branch has received no commit since 2024-07-27, and its final release v1.10.1 points at that same July 2024 commit.[^7] [^8]

:::exhibit(num="Exhibit 2", title="GitHub stars rank a two-year-dormant project first", subtitle="Stars as of 2026-08-05, indexed to the leader", source="GitHub REST API, fetched 2026-08-05", note="Stars are a cumulative lifetime counter and never decay; they measure historical mindshare, not current use.")
:::rank-list
- {label: "AUTOMATIC1111 stable-diffusion-webui", value: "164,387", pct: 100}
- {label: "ComfyUI", value: "123,602", pct: 75, highlight: true}
- {label: "Fooocus", value: "51,943", pct: 32}
- {label: "InvokeAI", value: "27,767", pct: 17}
- {label: "SwarmUI", value: "4,408", pct: 3}
:::
:::

The counterpoint is the section's actual point. Stars are a cumulative lifetime counter that never decays: a repository created 2022-08-22 accumulates against one created 2023-01-17 for five months before the competition exists, and historical mindshare keeps accruing after the code stops.[^7] [^6] AUTOMATIC1111 leading is therefore an artifact of sequencing, not evidence it is more used today — a two-years-abandoned repository outranking the live substrate is a fact about the metric, not about the projects. Stars are a bad instrument in both directions, which is precisely why they cannot be used to check the company's claims either. And unverifiable is not false: 4 million users may well be right. It simply cannot be checked by anyone outside the company, including an investor.

Two structural gaps make it worse. The comparison set is itself thinning — invoke.ai now publishes no pricing tiers at all, so InvokeAI's 27,767 stars measure a historical position rather than a live commercial one.[^56] [^7] And the largest uncounted channel is Chinese: the dominant mainland on-ramp is a Bilibili creator's pre-packaged 整合包 (integration package) distributed through Baidu and Quark netdisk rather than GitHub, pip, or the Comfy installer — and netdisk services publish no download statistics.[^62] That traffic is invisible to every counter on both sides of the ledger, which means the download figure is not merely imprecise but systematically incomplete in an unknown direction.

Why this matters: a company that cannot hold its own daily-download figure steady across two paragraphs of a single announcement is asking investors to underwrite an unaudited number.

## 06. The business is metered GPU time, wearing an open-source hat

Strip the open-source framing and what remains is a metered GPU business, because the two other stated revenue lines — API-node margin and enterprise licensing — are structurally given away. How large the GPU margin is cannot be computed from public data, and that is itself a finding.

The metered layer is Comfy Cloud. As of 2026-08-05 the published tiers run Standard $20/month for 4,200 credits, Creator $35 for 7,400, Pro $100 for 21,100 and Team $700 for 147,700, with an unpriced Enterprise tier and annual pricing at $16/$28/$80/$630 per month; the underlying hardware is an RTX PRO 6000 Blackwell, and billing is explicitly metered — "You're only charged for active GPU time while a workflow is running. Idle time (e.g. time spent building workflows) does not consume GPU hours."[^15]

:::exhibit(num="Exhibit 3", title="Comfy Cloud published monthly tiers", subtitle="Monthly list price, as of 2026-08-05", source="comfy.org/cloud/pricing", note="The pricing page's own FAQ describes Team as a credit-commit slider spanning $200 to $2,500 per month, so $700 is one slider position rather than the tier price.")
:::bars
- {label: "Standard", value: "$20/mo", pct: 3}
- {label: "Creator", value: "$35/mo", pct: 5}
- {label: "Pro", value: "$100/mo", pct: 14}
- {label: "Team", value: "$700/mo", pct: 100}
:::
:::

Two caveats on that ladder. Monthly credits reset each cycle and do not roll over, and the tiers are feature-gated — importing your own models or LoRAs is blocked on Standard, maximum workflow runtime is capped at 30 minutes until Pro, and concurrent workflows run 1/3/5 by tier.[^15] The lane is young: public beta opened 2025-11-04 on A100 40GB at $20/month, and general availability followed on 2026-03-04.[^18] [^17]

The second stated line is Partner Nodes — formerly API Nodes, launched 2025-05-06 — which expose roughly 35 commercial providers inside a workflow, including Anthropic, Google, OpenAI, OpenRouter, Runway, Kling, Luma, Ideogram, ElevenLabs, ByteDance, Tencent and Topaz, billed against a prepaid credit balance with no free tier and no refunds: "Partner Nodes require credits for API calls to closed-source models, so they do not support free usage."[^16] [^81] The margin, however, is not visible. Credit prices reproduce the underlying providers' public list prices to the cent — Google Veo 3.1 at 720p and 1080p bills at 84.4 credits/sec, or $0.40/sec, Google's list price; GPT-5 input bills at 263.75 credits per million tokens, or $1.25/1M, OpenAI's list price — and in the token-billed sections the docs state that actual API usage is authoritative.[^16] Comfy Org says so outright in its own launch post: "We charge the same as the original price for each API."[^81] The observable take rate on API calls is therefore approximately zero, and any margin must come from an undisclosed wholesale discount. Routed traffic is the one exception: OpenRouter-hosted GPT-5.5 is priced at 1,508.65 credits/1M against 1,055 for the directly-hosted row, roughly 1.4x.[^16] Enterprise then gives the residual away by name: "Bring your own API key" is a listed Enterprise feature, letting the highest-volume customers route through their own model-provider contracts.[^14] One dissent is worth recording: Sacra's research asserts that ComfyUI "takes a margin on API calls" — a ==contested: reputable secondary claim that the company's own price-parity statement and the published credit table both cut against==.[^5] [^81]

Those two node rows do fix the credit unit, and that arithmetic is reproducible. This article's derivation, not a company-published figure: $0.40 ÷ 84.4 and $1.25 ÷ 263.75 both yield about $0.00474 per credit, roughly 211 credits per dollar. At that rate Standard's 4,200 credits are worth about $19.91 against a $20 price — the subscription is a credit pre-purchase at par, not a margin layer.[^16] [^15]

What the credit unit does *not* unlock is the GPU margin, because Comfy Org does not publish a per-GPU-hour rate. The pricing page's only compute anchor is a workload benchmark — Standard's 4,200 credits "Generates ~380 5s videos" on a stated Wan 2.2 image-to-video template — which prices output, not machine time.[^15] A rental reference exists on the other side: the same RTX PRO 6000 class rents on Vast.ai at roughly $1.20/hour as of 2026-08-05.[^78] But without a published credits-per-second rate there is no arithmetic that turns $20/month into dollars per GPU-hour, so ==unverified: the size of Comfy Cloud's markup over commodity GPU rental cannot be computed from any public figure== — and any specific multiple quoted elsewhere rests on an unpublished input.

:::callout(kind=warn, label=Caveat)
Even with a published rate, a spot-rental comparison would overstate margin. Comfy bills only active GPU time on warm pooled capacity carrying 900+ preloaded models, so idle time, storage, cold starts and multi-tenancy overhead are real costs a spot price ignores.[^67] The honest position is that the gross margin on Comfy Cloud is undisclosed and not externally derivable.
:::

Comfy Org has never disclosed revenue, ARR, or a paying-customer count in any first-party document, and Sacra's April 2026 equity research on the company carries no revenue estimate.[^5] [^1] What it has disclosed is hiring: thirteen open San Francisco roles including "Account Executive: SMB & Mid-Market," "Enterprise Account Executive," "Head of Finance" and "Lead, Strategic Finance" — a GPL-licensed-client company staffing a metered-cloud sales motion.[^72] This matters because it collapses the investable question from "can an open-source standard monetize" to the far narrower "can a GPU rental business defend an undisclosed spread against commodity suppliers its own users can reach directly."

## 07. What a $500 million mark implies

The "Hugging Face of generative media" framing fails on both halves: the multiple it imports has been refused by the market for three years, and the hosting choke point Hugging Face monetizes is precisely what a GPL-3.0, local-first tool forfeits.

Comfy Org raised $30 million at a $500 million valuation announced 2026-04-24, led by Craft, taking total funding to $47 million — and no revenue figure has ever been disclosed.[^1] [^4] Sacra's April 2026 equity research on ComfyUI, the kind of note that exists to publish exactly that number, contains no revenue or ARR figure at all.[^5] With nothing to anchor on, the mark has to be read against comparables.

Start with the analogy. Hugging Face has not repriced since its August 2023 Series D at $4.5 billion, and in late 2025 it reportedly declined a $500 million Nvidia investment at $7 billion.[^50] [^49] Third-party ARR estimates — never company-reported — put it near $70 million at end-2023 and roughly $130 million in 2024, making $4.5 billion about 64x the 2023 estimate and about 35x the 2024 one.[^49] Revenue roughly doubled; the valuation did not move. A private mark held flat through a doubling of revenue is the market declining to underwrite the multiple.

:::exhibit(num="Exhibit 4", title="Revenue multiples across the honest comparable set", subtitle="Enterprise or market value divided by revenue, derived", source="Company filings, exchange data and third-party ARR estimates", note="Every multiple is this article's own arithmetic on the cited figures — none is a published number. Public comps as of 2026-08-04; the Hugging Face and Docker rows rest on third-party ARR estimates the companies have never confirmed.")
:::bars
- {label: "Hugging Face (2023 est. ARR)", value: 64.3x, pct: 100}
- {label: "Figma", value: 12.2x, pct: 19}
- {label: "HashiCorp/IBM exit", value: 11.0x, pct: 17}
- {label: "Docker", value: 10.1x, pct: 16}
- {label: "GitLab", value: 6.1x, pct: 9}
- {label: "Adobe", value: 4.0x, pct: 6}
:::
:::

GitLab, the closest public open-core benchmark, carried a $6.14 billion market cap on $1.00 billion of TTM revenue (+24.9% YoY) at 86.76% gross margin while loss-making at the GAAP line as of 2026-08-04 — about 6.1x, and nearer 4.6x against its lower ~$4.57 billion enterprise value on net cash.[^45] The canonical open-core exit, HashiCorp/IBM, was $6.4 billion of enterprise value against $583.1 million of fiscal-2024 revenue (+23% YoY), about 11.0x — and a strategic acquisition normally carries a control premium, which makes 11x an upper bound for a private financing mark, not a floor.[^46] [^47] Adobe printed 4.0x on 2026-08-04 ($100.82 billion market cap, $25.20 billion TTM revenue, +11.5%, cap down about 32%); Figma printed 12.2x the same day ($14.13 billion on $1.16 billion TTM, +41.4%, cap down about 76%).[^51] [^52]

The closest *structural* comparable is neither: it is Docker — local-first, open-core, developer-desktop, a vast free base and thin paid conversion. Docker was last valued at $2.1 billion in March 2022 and has not been repriced in over four years, on an estimated ~$207 million ARR from more than one million paid subscriber seats, about 10.1x, again on third-party estimates rather than company disclosure.[^48]

Apply an assumed 20–40x band and the implied revenue is plain arithmetic: $500M ÷ 20 = $25.0M; $500M ÷ 30 = $16.7M; $500M ÷ 40 = $12.5M. Sanity-check that against the $20/month Standard tier ($240/year): $25.0M ÷ $240 ≈ 104,000 paid seats, roughly 2.6% of the claimed four million users; $12.5M ÷ $240 ≈ 52,000 seats, roughly 1.3%. This is derivation, not disclosure — and the assumed band is *narrower* than reality, since the observed comps above straddle 4x to 64x.

Two datapoints cut across the frame. Krea reportedly raised a $47 million Series B in April 2025 at a reported $500 million valuation — nominal parity with Comfy Org on a fundamentally closed, hosted product, though that figure is aggregator-sourced rather than a company announcement.[^80] And Figma acquired the node-based AI canvas Weavy on 2025-10-30 and relaunched it as Figma Weave, with TechCrunch naming Weavy a ComfyUI rival.[^53] [^4]

**The counterpoint is strong.** All of the above assumes ComfyUI should be priced as a software business. If it should not, the numbers invert: $500 million is 11% of fal.ai's $4.5 billion (Series D, 2025-12-09, Sequoia), 6% of Together AI's $8.3 billion, and 11% of Modal Labs' $4.65 billion (Series C, May 2026) — all of which *capture* compute rather than orchestrate it.[^55] [^92] [^93] On that reading the mark is an option premium on Comfy Org converting a fraction of its position into metered inference, the comp set is fal/Modal/Together rather than GitLab/Docker, and $500 million looks cheap. Adobe's own de-rating cuts both ways too: 4.0x means the market is not paying for creative-tools franchises at all right now — bearish for a challenger's exit, but it also makes the obvious incumbent a weaker acquirer.[^51]

Why this matters: the distance between $12.5 million of implied ARR and a fal-style option premium is not a matter of taste. It decides whether Comfy Org's next round is an up round on revenue it has never disclosed, or a repricing onto an inference comp set it does not yet operate in.

## 08. Where the value leaks out

ComfyUI sits underneath a large and growing volume of commercial image and video generation, and Comfy Org monetizes almost none of it: the workflow format is freely executable by anyone, the largest national market is served end-to-end by domestic clouds, and the ~5,000 node authors whose work the company resells access to are paid nothing.

:::kv
- {term: "Workflow JSON", def: "Anyone — the graph ships inside every generated image"}
- {term: "RunComfy / Replicate", def: "The host — a JSON blob becomes a billed API"}
- {term: "Alibaba Cloud", def: "Alibaba — weights, runtime distribution and GPU rent"}
- {term: "Tencent Cloud", def: "Tencent — HAI sells ComfyUI compute directly"}
- {term: "LiblibAI", def: "LiblibAI and its Series B investors"}
- {term: "AICU (Japan)", def: "AICU — regional hosted GPU subscriptions"}
- {term: "Node authors", def: "Nobody — no revenue share exists"}
:::

### The format is not the moat

A ComfyUI workflow is human-readable JSON, written automatically into the metadata of every image the engine generates, so any recipient can reopen the exact graph that produced it.[^77] That makes the format trivially portable. Replicate ingests a raw ComfyUI API-format JSON blob and executes it as a hosted, billed API — *"It works by using a ComfyUI JSON blob. You send us your workflow as a JSON blob and we'll generate your outputs"* — with no license, contract, or negotiation with Comfy Org.[^57] RunComfy does the same for arbitrary workflows and adds deployment: *"Drop your workflow.json. We handle every dependency, custom node, and model"* and *"Deploy any saved workflow as a Serverless API with a single click,"* against a claimed "1M+ creators" — an unaudited vendor figure on its own landing page.[^58]

The nuance matters: this weakens the *format* moat, not the *ecosystem* moat. Replicate supports only a curated subset of custom nodes and weights, and its documentation concedes that upstream ComfyUI and custom-node updates can introduce breaking changes.[^57] The real switching cost was never the JSON schema — it is the Python custom-node ABI and the day-one model treadmill.

### China is the largest leak

Alibaba Cloud sells one-click ComfyUI deployment as an official documented product on both Function Compute and PAI-EAS, with serverless GPU billing that charges idle GPU at only {accent}10–20%{/} of the active rate.[^59] Alibaba publishes the open weights (Wan, Qwen-Image), ComfyUI is the runtime, and Alibaba Cloud rents the GPU: one firm monetizes all three layers and Comfy Org monetizes none. Tencent Cloud's 高性能应用服务 (HAI) lists ComfyUI as a supported compute-connection method alongside Notebook and WebUI — "支持 Notebook、WebUI、ComfyUI 等多种算力连接方式" ("supports Notebook, WebUI, ComfyUI and other compute-connection methods").[^60] Tencent is therefore simultaneously a logo on Comfy Org's enterprise page, a model supplier via Hunyuan, and a competing seller of ComfyUI compute.[^14]

The independent tier is capitalized too. LiblibAI (哩布哩布AI) raised a $130M Series B in October 2025, co-led by Sequoia China and CMC Capital, on a reported 25 million registered users, and runs ComfyUI itself as its hosted online-workflow engine.[^61] Those user figures are attributed to unnamed sources rather than the company, and outlets disagree on whether the 4 million actives are daily or monthly. Comfy Org's own China presence, by contrast, is a documentation mirror: `comfy.ac.cn`, Mintlify-hosted, carrying a mainland-specific troubleshooting section — "以下情况主要适用于中国大陆地区的用户" ("the following mainly applies to users in mainland China") — that points readers at Alibaba Cloud, Tencent Cloud, USTC and SJTU PyPI mirrors, with no ICP filing or corporate entity in its footer.[^63] The pattern repeats regionally: AICU Inc. of Tokyo launched ComfyPods on 2026-03-14, a browser-accessible hosted service with dedicated 20GB+ VRAM and no credit card required — hosted-ComfyUI revenue accruing to AICU.[^74]

### The contributors are the unpaid input

Comfy Cloud preinstalls community node packs on a paid GPU service, with a repository link as the only consideration returned.[^75] The registry offers authors the ability to publish, version, deprecate and track metrics; no revenue share, payout or bounty exists, and none is published.[^26] As of 2026-08-05 the registry lists 4,995 published node packs,[^9] and the funding announcement credits the value to them in as many words: *"The 60,000+ nodes you've built. The workflows you've shared."*[^1]

None of this is automatically a defect. Every party named above runs ComfyUI, and each deployment further entrenches the engine as the default — which is precisely the position a $500M mark is buying. A company that had successfully taxed Alibaba, Tencent, Replicate and five thousand node authors would most likely have been forked. The openness is arguably the distribution mechanism itself: every shared image is a working, install-and-run artifact, a viral loop closed-source rivals structurally lack. The honest bear case is narrower than "leakage is bad" — it is that the position may prove permanently *untaxable*.

That is what matters here. The valuation assumes standard-setting eventually converts into rent, and every leak documented above is a point where the conversion step is already owned by someone else.

## 09. The ecosystem's structural liability

The custom-node graph that constitutes ComfyUI's real moat is also its largest unmanaged attack surface: every node pack is arbitrary Python executed in-process, with full filesystem and network access, installed from third-party repositories, frequently by artists rather than developers — and the Registry lists **4,995 published node packs as of 2026-08-05**.[^9]

The proof is not hypothetical. The `ComfyUI_LLMVISION` custom node exfiltrated browser passwords, credit-card details and browsing history to an attacker-controlled Discord server.[^27] The forensically important detail is where the malicious code lived: not in the node's own source, but in trojanized OpenAI and Anthropic Python wheels — `openai-1.16.2-py3-none-any.whl` and `anthropic-0.21.3-py3-none-any.whl` — pulled in through a modified `requirements.txt`. A source-level review of the node would have come back clean.[^27] SentinelLABS attributes the repository to the actor "NullBulge," which also released roughly 1.1–1.2 TB of Disney internal Slack data on 2024-07-12, and which "has claimed to control the ComfyUI_LLMVISION GitHub repository for the duration of it being active."[^27] On 2025-05-01 the Department of Justice announced that Ryan Mitchell Kramer of Santa Clarita, a/k/a NullBulge, agreed to plead guilty to two counts — "one count of accessing a computer and obtaining information and one count of threatening to damage a protected computer" — over a program that "purported to be computer program that could be used to create A.I.-generated art."[^28] Precision matters here: the DOJ documents never name ComfyUI, `ComfyUI_LLMVISION`, or any repository. The link to this ecosystem comes from security research, not from prosecutors.[^27,28]

| Identifier / finding | Date | Severity or scale | Component |
|---|---|---|---|
| ComfyUI_LLMVISION | 2024-06 | Credential theft via trojanized wheels | Custom node |
| CVE-2024-21575 | 2024-12-12 | CVSS 3.1 8.6 HIGH | ComfyUI-Impact-Pack |
| UpGuard exposure scan | 2025-06-22 | 60 of ~2,800 abusable | Self-hosted instances |
| CVE-2025-67303 | 2026-01-06 | Unauthenticated RCE | ComfyUI-Manager |
| Censys botnet | 2026-04-06 | 1,000+ instances exploited | Custom-node extension surface |

Comfy Org's January 2025 security update describes scanning as an alerting system, not a gate: results "alert a private channel," the company asks the community to "help us and the rest of the ecosystem to verify the security issues being flagged in that channel as a second line of defense," and the scanning code itself "will be held privately" — making coverage unauditable from outside.[^25] The published Registry standards reduce to three source-level prohibitions: `eval`/`exec` are prohibited, runtime package installation via subprocess is not permitted, and code obfuscation is prohibited. There is no code signing and no mandatory human review.[^26]

:::callout(kind=danger, label=Structural)
All three Registry prohibitions are **source-level**, and the attack that produced a federal guilty plea used none of them — it lived in pinned third-party wheels, so source-level review was clean.[^26,27] Comfy Org's own security update names that exact vector as unresolved, listing "custom wheels, binaries, git python dependencies" under open questions rather than under covered controls.[^25]
:::

The exposure is live, not historical. UpGuard's June 2025 scan found roughly 2,800 ComfyUI instances online, of which 93 allowed unauthenticated access and 60 were confirmed leaking data or abusable.[^32] On 2026-04-06 Censys reported a botnet mass-exploiting more than 1,000 internet-exposed instances, targeting extension mechanisms rather than the core application; the nodes in question are not malicious — `ComfyUI-Shell-Executor`, `FL_CodeNode`, `SrlEval`, `EvaluateMultiple` are legitimate and popular, and their advertised feature *is* accepting and executing raw Python. Censys notes that targeting "extensibility mechanisms rather than the core application itself… is not something we commonly observe."[^31] These two figures are **not a time series**: different dates, different methodology, UpGuard hand-verifying abusability while Censys counts scanner-visible hosts. Alongside them sit disclosed defects in the node layer itself — CVE-2024-21575, a path-traversal-to-arbitrary-file-write in ComfyUI-Impact-Pack, CVSS 3.1 8.6 HIGH, published 2024-12-12, potentially resulting in remote code execution[^29] — and in the installer, CVE-2025-67303, unauthenticated RCE against default ComfyUI-Manager installations because Manager's data and configuration directories "were insufficiently protected by ComfyUI's Web API access control mechanisms." That fix requires *both* Manager v3.38+ **and** core v0.3.76+ plus a manual data migration, so an upgraded Manager alone does not mean patched.[^30]

The fair counterpoint: this mechanism is not unique to ComfyUI. Sonatype reported 34,319 malicious open-source packages discovered in Q3 2025 alone across npm, PyPI and Hugging Face, against 877,522 cumulative since 2019 — vendor detection counts inflated by mass-registered typosquats, not 877,000 real compromises, but the install-time-arbitrary-code mechanism is identical to PyPI's and thoroughly understood.[^88] By raw volume ComfyUI is a rounding error. What is different is the population and the packaging: the installer is a one-click Manager whose security level the user can lower, the installers are largely artists rather than developers, and a meaningful subset of popular nodes have arbitrary code execution as their *advertised feature* rather than their vulnerability.[^9,31]

Commercially, this is where the logo wall meets procurement: enterprise buyers price third-party-execution risk explicitly, and a moat made of 4,995 unsigned, unreviewed Python packages is the single largest discount a security review will apply to a $500M mark.[^9,26]

## 10. The company is quietly dismantling its own graph

In 2026 Comfy Org shipped three things that each cut against the asset it was funded on: an app mode that hides the node graph, an agentic layer that replaces the graph with natural language on the billed path first, and a contributor licence agreement whose own bot names a future relicense away from GPL-3.0 as the benefit that matters most.

| Shipped | Date | What it does to the graph | Available where |
|---|---|---|---|
| App Mode (with App Builder and ComfyHub) | 2026-03-10 | Hides the node graph behind a purpose-built interface[^20] | Local and cloud |
| Comfy MCP | 2026-06-29 | Replaces the graph with natural language[^19] | Public beta[^19] |
| Contributor Licence Agreement | 2026-07-06 | Enables a future relicense away from GPL-3.0[^21] | Repository-wide |

The App Mode launch post does not hedge about what it removes. Verbatim: "When you enter App Mode, the node graph disappears and is replaced by a clean, purpose-built interface," with "no node graph experience required."[^20] Three and a half months later, Comfy MCP connected agents such as Claude, Codex and Cursor to the ecosystem, letting a model build, edit and run workflows, search models, nodes and template workflows, save and re-run them, and read and execute shared workflow URLs.[^19]

:::quote(attr="Comfy Org, Comfy MCP launch post, 2026-06-29")
Everything is now in natural language. No nodes, no download, no GPU, no node graphs if you don't want them.
:::

The framing in that launch is the part worth reading twice. What Comfy MCP removes is not only the graph but the machine: the post's own list of what the user no longer needs is "no nodes, no download, no GPU."[^19] An agent driving Comfy MCP is an agent running workflows on Comfy Org's hardware rather than the user's — which is to say the product that makes the node graph optional is also the product that meters. The post describes it as being in public beta.[^19]

The licence move is the third leg. On 2026-07-06 ComfyUI added a CLA Assistant workflow using `contributor-assistant/github-action` v2.6.1, with signatures stored in `Comfy-Org/comfy-cla`.[^21] The bot's PR-comment template tells contributors the CLA "would enable us to relicense the project under a more permissive license in the future, giving the project and its community greater flexibility" — framed as the most important benefit.[^21] The Individual CLA grants Comfy Organization, Inc. a "perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license" to reproduce, prepare derivative works of, sublicense and distribute contributions, with no outbound copyleft or reciprocity condition, covering "all of my past, present and future Contributions."[^22] Both CLA pull requests are locked and carry only automated review comments: a retroactive, relicensing-enabling CLA landed on a 123,000-star GPL-3.0 project with no visible public debate.[^21]

:::statement(attr="ARA Research")
A company whose asset is a node graph shipped two products in 2026 to hide it and a licence instrument to be free of the copyleft that protects it.
:::

The charitable reading is strong, and it should be stated at full strength. None of these three moves is sinister on its face. App Mode and MCP are how a power tool reaches a wider market, and the CEO's own thesis is that prompt-only tools fail at the last 20% — an agent that can drive a graph makes the graph more valuable, not less. The CLA derives from Apache's, is a licence rather than an assignment (contributors "reserve all right, title, and interest"), and 142 signatures gathered between 2026-06-22 and 2026-08-04 cannot relicense a project with thousands of historical commits.[^22] [^23] The overwhelming majority of historical copyright remains unsigned, so a full relicense is not mechanically available today.[^23] The core software remains GPL-3.0 as of 2026-08-05.[^6] The funding post pledges "We are not building a walled garden" and that ComfyUI "will always stays open," and the CEO, asked the odds of acquisition, answered in one word: "Zero."[^1] [^12] Lead investor Craft Ventures cites Adobe's Project Graph, Figma's Weavy acquisition and Runway's Workflows as incumbent validation — while talking its book.[^68] The one substantive maintainer-answered objection to paid nodes in core drew three comments and zero reactions, with the creator explaining that `--disable-api-nodes` exists for users who want no communication with online servers at all.[^69] That is not a community in revolt.

So the evidence supports "the company is optimising for its cloud business" — not "the company is about to close the source," which would be unsupported. The shared-codebase evidence cuts the same way: the frontend repository carries six commercial telemetry SDKs for the cloud build, and a CI job fails the pull request if any survive into the open-source distribution — active policing, on one codebase serving both products.[^91]

This matters because a $500M mark rests on owning the graph everyone standardises on. Each of these three moves is defensible on its own; together they describe a company converting a defensible open artifact into a funnel for a metered one.

## 11. The enterprise story, and what would falsify all of this

The bear case above rests on a claim that can be checked: that Comfy Org's enterprise traction is thinner than its marketing implies. It is — but the same audit turns up the strongest single piece of evidence for the bull case, and the thesis has four other ways to be wrong.

### The logo wall does not say what readers think it says

Comfy Org's enterprise page displays eleven company logos — Amazon Studios, Apple, Autodesk, Harman, HP, Lucid, Netflix, Nike, Pixomondo, Tencent, Ubisoft — with no accompanying text asserting a customer, partner, or payment relationship. The logos are unlinked images; the relationship is asserted purely by placement.[^14] This article audited all eleven against public artifacts — job postings, published repositories, conference material — and found something naming ComfyUI for four of them, and nothing at all for HP, Harman and Lucid; the last cannot even be disambiguated between Lucid Motors, Lucid Software and the AI video startup of the same name.[^14] [^41] [^79] [^90] [^39]

What evidence does exist is real but narrower than the placement implies. Netflix names ComfyUI in job postings for its Inkubator unit, in both qualifications and responsibilities — the strongest independent artifact behind any logo, though Inkubator is an experimental unit spun up in 2026 and the work described is concept and design frames, not final pixel.[^41] Amazon MGM Studios lists ComfyUI in the basic and preferred qualifications for a Gen AI / VFX Coordinator, one item in a seven-tool list at coordinator level.[^79] An Apple careers posting named ComfyUI as a preferred qualification — on a Marcom product-design req, not an engineering one.[^90] Ubisoft La Forge published genuine first-party ComfyUI custom nodes for its CHORD material-estimation model.[^39]

That last one inverts on inspection. The CHORD nodes ship under the Ubisoft Machine Learning License, research-only, with commercial use strictly prohibited — and Ubisoft's own La Forge blog says the results are "not production-ready yet, but a solid first step," and that "the quality isn't where it needs to be for AAA video games material."[^39] [^40] Comfy Org files the same release on its customers page under the heading of AAA game production.[^42] The published case studies are advertising, not pipeline: the most detailed one, an agency spot, concedes that Nuke did the finishing while ComfyUI orchestrated generation upstream.[^43] The verifiable job market is roughly forty postings, dominated by AI startups and agencies, with Comfy Org itself among the largest single posters and no VFX facility appearing at all.[^76]

A named ILM compositor who *builds* ComfyUI tooling — a sympathetic critic — identifies the structural mismatch: "The single largest gap between ComfyUI's defaults and a real compositing pipeline is color management," with default nodes assuming 8-bit sRGB and simplified merge math. His assessment is that shops face a choice between re-engineering the pipeline around ComfyUI's assumptions or dropping AI at comp — and that most have chosen the latter.[^44]

### The legal surface is heavier than a $20/month product implies

Three constraints bear on enterprise conversion. First, licensing: FLUX.1 [dev] version 1.1.1 permits commercial use of outputs in section 2(d) while conditioning the entire grant in section 1(c) on receiving no direct or indirect payment — so the default local FLUX workflow is a gray zone for revenue-generating work.[^64] Comfy Cloud's answer is to market that every one of its 900+ models is "cleared for commercial use" with "no license ambiguity," a representation that appears in marketing copy but not in the governing Terms of Service.[^67] [^13] Second, procurement: Google's published third-party licensing policy places GPL v3 in the restricted category, barred from products delivered to outside customers — narrow, since running an unmodified tool on a workstation does not trigger distribution, but real.[^65] Third, the contract itself caps Comfy Organization's total liability at the greater of $1,000 or six months of fees, and requires the customer to defend and indemnify Comfy.[^13] Meanwhile EU AI Act Article 50 transparency obligations became applicable on 2026-08-02, and deployers cannot discharge their disclosure duty by relying on a provider's marking.[^66] None of the unresolved copyright litigation — Andersen, the consolidated Disney and Universal action against Midjourney — names Comfy Org, but none has been decided either.[^82]

### What would falsify the thesis

- **Disclosed revenue.** The entire bear case rests on an absence. If Comfy Org discloses ARR above roughly $25 million, the implied-conversion arithmetic in section 07 collapses and the mark is ordinary rather than aspirational.[^1]
- **A signed enterprise contract, named.** One published, named, paying enterprise deal — not a logo — converts the position-versus-business distinction into a business.[^14]
- **A lab paying for placement.** If a model lab pays Comfy Org for day-zero integration rather than receiving it free, the substrate becomes taxable and the leakage analysis in section 08 inverts.[^1]
- **Comfy Cloud API deployment at scale.** RunComfy and Replicate currently capture the hosted-execution layer; Comfy Org has said workflow API deployment is coming. Shipping it would reclaim the leak rather than concede it.[^57] [^17]
- **A competitor importing the ecosystem, not the format.** The format is already portable. If Figma Weave, Flora or a successor ships a working ComfyUI custom-node compatibility layer, the last moat goes.[^53] [^54] [^55]

:::note
Adversarial pass: the three load-bearing claims above were re-attacked against independent sources. The funding-and-no-disclosed-revenue claim survived unbroken. The registry count was corrected from a same-day re-fetch. The price-parity claim drew one reputable dissent — Sacra asserts a margin on API calls — which is recorded and rebutted in section 06 rather than dropped.
:::

The honest summary is that Comfy Org has won something genuinely difficult and rare — a de facto standard, built by refusing to be easy, maintained largely at its own expense, adopted by labs that never signed anything. The $500 million question is not whether that position is real. It is whether a position this open can ever be taxed by the company that created it, and every mechanism examined here suggests the answer is not yet.

:::references
- {id: 1, title: "ComfyUI raises $30M to scale open-source AI for creative production", url: "https://blog.comfy.org/p/comfyui-raises-30m-to-scale-open", source: "Comfy Org", date: "2026-04-24"}
- {id: 2, title: "ComfyUI Raises $30M at $500M Valuation (press release)", url: "https://www.globenewswire.com/news-release/2026/04/24/3281014/0/en/comfyui-raises-30m-at-500m-valuation-to-scale-open-source-ai-for-creative-production.html", source: "GlobeNewswire", date: "2026-04-24"}
- {id: 3, title: "Comfy raises $17M in funding", url: "https://blog.comfy.org/p/comfy-raises-17m-funding", source: "Comfy Org", date: "2025-09-16"}
- {id: 4, title: "ComfyUI hits $500M valuation as creators seek more control over AI-generated media", url: "https://techcrunch.com/2026/04/24/comfyui-hits-500m-valuation-as-creators-seek-more-control-over-ai-generated-media/", source: TechCrunch, date: "2026-04-24"}
- {id: 5, title: "ComfyUI valuation, funding and news", url: "https://sacra.com/c/comfyui/", source: Sacra, date: "2026-04-26"}
- {id: 6, title: "Comfy-Org/ComfyUI repository metadata", url: "https://api.github.com/repos/Comfy-Org/ComfyUI", source: "GitHub REST API", date: "2026-08-05"}
- {id: 7, title: "AUTOMATIC1111/stable-diffusion-webui repository metadata", url: "https://api.github.com/repos/AUTOMATIC1111/stable-diffusion-webui", source: "GitHub REST API", date: "2026-08-05"}
- {id: 8, title: "stable-diffusion-webui master branch commit history", url: "https://github.com/AUTOMATIC1111/stable-diffusion-webui/commits/master", source: GitHub, date: "2024-07-27"}
- {id: 9, title: "Comfy Registry nodes endpoint", url: "https://api.comfy.org/nodes", source: "Comfy Registry API", date: "2026-08-05"}
- {id: 10, title: "ComfyUI: the creator interview", url: "https://www.latent.space/p/comfyui", source: "Latent Space", date: "2025-01-04"}
- {id: 11, title: "ComfyUI is 4 months old", url: "https://blog.comfyui.ca/comfyui/update/2023/05/18/ComfyUi-is-4-months-old.html", source: comfyanonymous, date: "2023-05-18"}
- {id: 12, title: "ComfyUI's CEO on control, adoption, and why the tool won't be acquired", url: "https://www.vp-land.com/p/comfyui-s-ceo-on-control-adoption-and-why-the-tool-won-t-be-acquired", source: "VP Land", date: "2026-03-20"}
- {id: 13, title: "Comfy Organization, Inc. Terms of Service", url: "https://www.comfy.org/terms-of-service", source: "Comfy Org", date: "2026-05-13"}
- {id: 14, title: "Comfy Cloud Enterprise", url: "https://comfy.org/cloud/enterprise/", source: "Comfy Org", date: "2026-08-05"}
- {id: 15, title: "Comfy Cloud pricing", url: "https://comfy.org/cloud/pricing/", source: "Comfy Org", date: "2026-08-05"}
- {id: 16, title: "Partner Nodes pricing", url: "https://docs.comfy.org/tutorials/partner-nodes/pricing", source: "Comfy Org docs", date: "2026-08-05"}
- {id: 17, title: "Comfy Cloud is out of beta", url: "https://blog.comfy.org/p/comfy-cloud-is-out-of-beta-and-its", source: "Comfy Org", date: "2026-03-04"}
- {id: 18, title: "Comfy Cloud is now in public beta", url: "https://blog.comfy.org/p/comfy-cloud-is-now-in-public-beta", source: "Comfy Org", date: "2025-11-04"}
- {id: 19, title: "Comfy MCP: turn your agent into a generative media studio", url: "https://blog.comfy.org/p/comfy-mcp-turn-your-agent-into-a", source: "Comfy Org", date: "2026-06-29"}
- {id: 20, title: "From workflow to app: introducing App Mode", url: "https://blog.comfy.org/p/from-workflow-to-app-introducing", source: "Comfy Org", date: "2026-03-10"}
- {id: 21, title: "ComfyUI CLA Assistant workflow", url: "https://raw.githubusercontent.com/Comfy-Org/ComfyUI/master/.github/workflows/cla.yml", source: GitHub, date: "2026-07-06"}
- {id: 22, title: "ComfyUI Individual Contributor License Agreement", url: "https://raw.githubusercontent.com/Comfy-Org/comfy-cla/main/comfyui_icla.md", source: GitHub, date: "2026-06-22"}
- {id: 23, title: "ComfyUI CLA signature register", url: "https://raw.githubusercontent.com/Comfy-Org/comfy-cla/main/signatures/cla.json", source: GitHub, date: "2026-08-04"}
- {id: 24, title: "Launching the ComfyUI Registry", url: "https://blog.comfy.org/p/launching-comfyui-registry", source: "Comfy Org", date: "2025-01-03"}
- {id: 25, title: "ComfyUI January 2025 security update", url: "https://blog.comfy.org/p/comfyui-2025-jan-security-update", source: "Comfy Org", date: "2025-01-03"}
- {id: 26, title: "Comfy Registry standards", url: "https://docs.comfy.org/registry/standards", source: "Comfy Org docs", date: "2026-08-05"}
- {id: 27, title: "NullBulge: threat actor masquerades as hacktivist group rebelling against AI", url: "https://www.sentinelone.com/labs/nullbulge-threat-actor-masquerades-as-hacktivist-group-rebelling-against-ai/", source: SentinelLABS, date: "2024-07-16"}
- {id: 28, title: "Santa Clarita man agrees to plead guilty to hacking Disney employee's computer", url: "https://www.justice.gov/usao-cdca/pr/santa-clarita-man-agrees-plead-guilty-hacking-disney-employees-computer-downloading", source: "US DOJ, C.D. Cal.", date: "2025-05-01"}
- {id: 29, title: "CVE-2024-21575", url: "https://nvd.nist.gov/vuln/detail/CVE-2024-21575", source: "NIST NVD", date: "2024-12-12"}
- {id: 30, title: "XLab-26-001: ComfyUI-Manager unauthenticated RCE (CVE-2025-67303)", url: "https://xlab.tencent.com/en/2026/01/06/xlab-26-001/", source: "Tencent Xuanwu Lab", date: "2026-01-06"}
- {id: 31, title: "ComfyUI servers exploited for cryptomining and proxy botnet", url: "https://censys.com/blog/comfyui-servers-cryptomining-proxy-botnet/", source: Censys, date: "2026-04-06"}
- {id: 32, title: "Detecting generative AI data leaks from ComfyUI", url: "https://www.upguard.com/blog/detecting-generative-ai-data-leaks-from-comfyui", source: UpGuard, date: "2025-06-22"}
- {id: 33, title: "Announcing Black Forest Labs and FLUX.1", url: "https://bfl.ai/blog/24-08-01-bfl", source: "Black Forest Labs", date: "2024-08-01"}
- {id: 34, title: "Wan2.2 repository", url: "https://github.com/Wan-Video/Wan2.2", source: "Alibaba Wan team", date: "2025-07-28"}
- {id: 35, title: "Qwen-Image repository", url: "https://github.com/QwenLM/Qwen-Image", source: "Alibaba Qwen team", date: "2025-08-05"}
- {id: 36, title: "LTXV day 1 support in ComfyUI", url: "https://blog.comfy.org/p/ltxv-day-1-comfyui", source: "Comfy Org", date: "2024-11-22"}
- {id: 37, title: "MiniMax H3 day-0 support in ComfyUI", url: "https://blog.comfy.org/p/minimax-h3-day-0-support-in-comfyui", source: "Comfy Org", date: "2026-08-03"}
- {id: 38, title: "Wan2.2 day-0 support in ComfyUI", url: "https://blog.comfy.org/p/wan22-day-0-support-in-comfyui", source: "Comfy Org", date: "2025-07-28"}
- {id: 39, title: "ubisoft/ComfyUI-Chord", url: "https://github.com/ubisoft/ComfyUI-Chord", source: Ubisoft, date: "2025-12-09"}
- {id: 40, title: "Generative Base Material: an open-source prototype for PBR material estimation", url: "https://www.ubisoft.com/en-us/studio/laforge/news/1i3YOvQX2iArLlScBPqBZs/generative-base-material-an-opensource-prototype-for-pbr-material-estimation-debuting-at-siggraph-asia-2025", source: "Ubisoft La Forge", date: "2025-12-09"}
- {id: 41, title: "Technical Director, Inkubator (job posting)", url: "https://explore.jobs.netflix.net/careers/job/790314754913-technical-director-inkubator-los-angeles-california-united-states-of-america", source: Netflix, date: "2026-03-09"}
- {id: 42, title: "Customer story: Ubisoft CHORD", url: "https://comfy.org/customers/ubisoft-chord/", source: "Comfy Org", date: "2026-08-05"}
- {id: 43, title: "Customer story: Groove Jones", url: "https://www.comfy.org/customers/groove-jones", source: "Comfy Org", date: "2026-08-05"}
- {id: 44, title: "Nuke ComfyUI nodes", url: "https://sumitc.com/work/nuke-comfyui-nodes", source: "Sumit Chatterjee, ILM", date: "2026-08-05"}
- {id: 45, title: "GitLab (GTLB) statistics", url: "https://stockanalysis.com/stocks/gtlb/", source: StockAnalysis, date: "2026-08-04"}
- {id: 46, title: "HashiCorp fiscal 2024 fourth quarter results", url: "https://www.sec.gov/Archives/edgar/data/1720671/000162828024008867/hcp-q4fy24xex991.htm", source: "SEC EDGAR", date: "2024-03-05"}
- {id: 47, title: "IBM to acquire HashiCorp", url: "https://newsroom.ibm.com/2024-04-24-IBM-to-Acquire-HashiCorp-Inc-Creating-a-Comprehensive-End-to-End-Hybrid-Cloud-Platform", source: IBM, date: "2024-04-24"}
- {id: 48, title: "Docker valuation, funding and revenue", url: "https://sacra.com/c/docker/", source: Sacra, date: "2026-08-04"}
- {id: 49, title: "Hugging Face valuation, funding and revenue", url: "https://sacra.com/c/hugging-face/", source: Sacra, date: "2026-08-04"}
- {id: 50, title: "Why AI start-up Hugging Face turned down a $500mn Nvidia deal", url: "https://oodaloop.com/briefs/technology/why-ai-start-up-hugging-face-turned-down-a-500mn-nvidia-deal/", source: "OODA Loop, citing the Financial Times", date: "2025-12-01"}
- {id: 51, title: "Adobe (ADBE) statistics", url: "https://stockanalysis.com/stocks/adbe/", source: StockAnalysis, date: "2026-08-04"}
- {id: 52, title: "Figma (FIG) statistics", url: "https://stockanalysis.com/stocks/fig/", source: StockAnalysis, date: "2026-08-04"}
- {id: 53, title: "Welcome Weavy to Figma", url: "https://www.figma.com/blog/welcome-weavy-to-figma/", source: Figma, date: "2025-10-30"}
- {id: 54, title: "Node-based design tool Flora raises $42M from Redpoint Ventures", url: "https://techcrunch.com/2026/01/27/node-based-design-tool-flora-raises-42m-from-redpoint-ventures/", source: TechCrunch, date: "2026-01-27"}
- {id: 55, title: "Fal nabs $140M led by Sequoia, tripling valuation to $4.5B", url: "https://techcrunch.com/2025/12/09/fal-nabs-140m-in-fresh-funding-led-by-sequoia-tripling-valuation-to-4-5b/", source: TechCrunch, date: "2025-12-09"}
- {id: 56, title: "Invoke pricing", url: "https://www.invoke.ai/pricing", source: "Invoke AI", date: "2026-08-05"}
- {id: 57, title: "Run ComfyUI workflows on Replicate", url: "https://replicate.com/docs/guides/extend/comfyui", source: Replicate, date: "2026-08-05"}
- {id: 58, title: "RunComfy", url: "https://www.runcomfy.com/", source: RunComfy, date: "2026-08-05"}
- {id: 59, title: "Function Compute ComfyUI quickstart", url: "https://help.aliyun.com/zh/functioncompute/fc/quick-start-comfyui", source: "Alibaba Cloud", date: "2026-08-05"}
- {id: 60, title: "High Performance Application Service (HAI)", url: "https://cloud.tencent.com/product/hai", source: "Tencent Cloud", date: "2026-08-05"}
- {id: 61, title: "LiblibAI closes $130M Series B", url: "https://finance.sina.com.cn/stock/t/2025-10-23/doc-infuvrat2626622.shtml", source: "Sina Finance", date: "2025-10-23"}
- {id: 62, title: "秋葉aaaki", url: "https://baike.baidu.com/item/秋葉aaaki/66132873", source: "Baidu Baike", date: "2025-12-30"}
- {id: 63, title: "ComfyUI desktop installation, China documentation mirror", url: "https://docs.comfy.ac.cn/installation/desktop/windows", source: "Comfy Org", date: "2026-08-05"}
- {id: 64, title: "FLUX.1 [dev] Non-Commercial License v1.1.1", url: "https://raw.githubusercontent.com/black-forest-labs/flux/main/model_licenses/LICENSE-FLUX1-dev", source: "Black Forest Labs", date: "2025-06-26"}
- {id: 65, title: "Third-party license categories", url: "https://opensource.google/documentation/reference/thirdparty/licenses", source: "Google Open Source", date: "2026-08-05"}
- {id: 66, title: "Transparency obligations under Article 50 AI Act (FAQ)", url: "https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act", source: "European Commission", date: "2026-08-05"}
- {id: 67, title: "Comfy Cloud", url: "https://comfy.org/cloud", source: "Comfy Org", date: "2026-08-05"}
- {id: 68, title: "Investing in Comfy: the operating system for generative media", url: "https://www.craftventures.com/articles/investing-in-comfy-the-operating-system-for-generative-media", source: "Craft Ventures", date: "2026-04-25"}
- {id: 69, title: "Issue 14887: hiding partner nodes breaks the node manager", url: "https://github.com/Comfy-Org/ComfyUI/issues/14887", source: GitHub, date: "2026-07-11"}
- {id: 70, title: "ComfyUI-Manager joins Comfy Org", url: "https://blog.comfy.org/p/comfyui-manager-joins-comfy-org", source: "Comfy Org", date: "2025-03-29"}
- {id: 71, title: "ComfyUI changelog", url: "https://docs.comfy.org/changelog", source: "Comfy Org docs", date: "2026-08-05"}
- {id: 72, title: "Comfy Org careers", url: "https://comfy.org/careers/", source: "Comfy Org", date: "2026-08-05"}
- {id: 73, title: "Announcing the formation of Comfy Org", url: "https://x.com/yoland_yan/status/1803104946679849253", source: "Yoland Yan", date: "2024-06-18"}
- {id: 74, title: "ComfyPods alpha launch", url: "https://corp.aicu.ai/ja/comfypods-20260314", source: "AICU Inc.", date: "2026-03-14"}
- {id: 75, title: "Comfy Cloud supported nodes", url: "https://comfy.org/cloud/supported-nodes/", source: "Comfy Org", date: "2026-08-05"}
- {id: 76, title: "ComfyUI job listings", url: "https://www.simplyhired.com/search?q=comfyui", source: SimplyHired, date: "2026-08-05"}
- {id: 77, title: "Core concept: workflow", url: "https://docs.comfy.org/development/core-concepts/workflow", source: "Comfy Org docs", date: "2026-08-05"}
- {id: 78, title: "RTX PRO 6000 rental pricing", url: "https://vast.ai/pricing/gpu/RTX-PRO-6000-S", source: "Vast.ai", date: "2026-08-05"}
- {id: 79, title: "Gen AI / VFX Coordinator, US Series VFX Department", url: "https://www.amazon.jobs/en/jobs/10479838/gen-ai-vfx-coordinator-us-series-vfx-department", source: "Amazon MGM Studios", date: "2026-07-21"}
- {id: 80, title: "Krea raises $47M Series B", url: "https://app.dealroom.co/news/feed/krea-raises-47m-series-b-funding", source: Dealroom, date: "2025-04-07"}
- {id: 81, title: "ComfyUI native API nodes", url: "https://blog.comfy.org/p/comfyui-native-api-nodes", source: "Comfy Org", date: "2025-05-06"}
- {id: 82, title: "Disney Enterprises, Inc. v. Midjourney, Inc. docket", url: "https://www.courtlistener.com/docket/70513159/disney-enterprises-inc-v-midjourney-inc/", source: CourtListener, date: "2026-08-05"}
- {id: 83, title: "ComfyUI README", url: "https://raw.githubusercontent.com/comfyanonymous/ComfyUI/master/README.md", source: GitHub, date: "2026-08-05"}
- {id: 84, title: "comfy_execution/caching.py", url: "https://raw.githubusercontent.com/comfyanonymous/ComfyUI/master/comfy_execution/caching.py", source: GitHub, date: "2026-08-05"}
- {id: 85, title: "Introducing Stable Diffusion 3.5", url: "https://stability.ai/news-updates/introducing-stable-diffusion-3-5", source: "Stability AI", date: "2024-10-22"}
- {id: 86, title: "HunyuanVideo-1.5 ComfyUI guide", url: "https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/tree/main/ComfyUI", source: "Tencent Hunyuan", date: "2025-11-21"}
- {id: 87, title: "ComfyUI now supports NVIDIA Cosmos", url: "https://blog.comfy.org/p/comfyui-now-supports-nvidia-cosmos", source: "Comfy Org", date: "2025-01-17"}
- {id: 88, title: "Open Source Malware Index Q3 2025", url: "https://www.sonatype.com/press-releases/open-source-malware-index-q3-2025", source: Sonatype, date: "2025-10-15"}
- {id: 89, title: "SwarmUI repository", url: "https://github.com/mcmonkeyprojects/SwarmUI", source: GitHub, date: "2026-08-05"}
- {id: 90, title: "Product Designer, Marcom (Apple job posting mirror)", url: "https://www.talentify.io/job/product-designer-marcom-sunnyvale-california-us-apple-200595581", source: Talentify, date: "2025-03-17"}
- {id: 91, title: "ComfyUI frontend dist telemetry scan workflow", url: "https://raw.githubusercontent.com/Comfy-Org/ComfyUI_frontend/main/.github/workflows/ci-dist-telemetry-scan.yaml", source: GitHub, date: "2026-08-05"}
- {id: 92, title: "Together AI raises $800 million", url: "https://finance.yahoo.com/technology/ai/articles/together-ai-raises-800-million-160522664.html", source: "Yahoo Finance", date: "2026-08-05"}
- {id: 93, title: "Modal Labs seals $355M funding round", url: "https://siliconangle.com/2026/05/21/serverless-ai-infrastructure-startup-modal-labs-seals-355m-funding-round/", source: SiliconANGLE, date: "2026-05-21"}
:::
