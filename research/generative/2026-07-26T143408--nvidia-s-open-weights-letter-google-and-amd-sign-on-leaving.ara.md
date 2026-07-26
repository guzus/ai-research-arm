---
eyebrow: REPORT · AI POLICY
title: The Distillation Trap — Why Anthropic Won't Sign NVIDIA's Open-Weights Letter
deck: A 50-signatory coalition led by NVIDIA, Microsoft and Meta wants Washington to leave open-weight AI alone. The signatory list sorts almost perfectly by business model — and the one holdout has both a three-year paper trail and an acute reason to stay silent this particular week.
lede: |
  On July 24, 2026, NVIDIA CEO Jensen Huang used the first post of his life on X to promote a 25-company letter arguing that open-weight AI models are essential to American safety, security and sovereignty. Within 24 hours the list doubled to 50 names, adding OpenAI, Google and AMD. Two firms never showed up: Amazon, and its biggest AI holding, Anthropic. The gap looks like defiance. It reads more like the collision of a three-year-old policy position with a distillation dispute that broke into the open the same week — one in which Anthropic is not a bystander, but the alleged victim.
stats:
  - {label: Signatories (as of 07-26), value: "50", note: "+25 in 24 hours"}
  - {label: Anthropic / Amazon signed, value: "0 of 2"}
  - {label: Huang's first X post, value: "25M views"}
  - {label: NVIDIA equity in Anthropic, value: "$10B"}
domain: policy
---

:::callout(kind=info, label="In short")
- NVIDIA, Microsoft and Meta published "Open Weights and American AI Leadership" on July 24, 2026; the list grew from 25 to 50 signatories in a day, adding OpenAI, Google and AMD [^1,4].
- Anthropic and Amazon are the only notable holdouts as of July 26 [^1,4]. Neither has issued a statement explaining why [^4].
- The signatory pattern tracks business model almost exactly: firms that sell compute or infrastructure regardless of which model wins signed; firms whose revenue depends on owning the best closed model mostly didn't [^16].
- The letter explicitly defends AI-model "distillation" as legitimate [^5] — in the same week a White House official publicly accused a Chinese lab of distilling Anthropic's own frontier model [^7,8].
- NVIDIA itself holds a reported $10B equity stake in Anthropic [^17], a relationship neither company has publicly reconciled with Anthropic's non-signature.
:::

## 01. The 48-hour signature stampede

The letter's own text is unremarkable as policy documents go: it invokes the 1980s fight over proprietary versus open software, argues that concentrating frontier AI in a handful of closed providers creates "single points of failure," and asks Washington not to impose "premature restrictions" on open-weight models [^1]. What made it newsworthy was the speed and cast of characters around it.

:::timeline
- {date: "2026-07-21", headline: "Bessent floats sanctions", body: "Treasury Secretary Scott Bessent tells Fox Business the administration is 'finding watermarks of our U.S. large language models on many of the Chinese models' [^9]; he adds on X the next day that sanctions and Entity List designations are 'on the table' [^35]."}
- {date: "2026-07-22", headline: "Kratsios names Kimi K3", body: "White House OSTP Director Michael Kratsios accuses Moonshot AI of 'large-scale, covert industrial distillation' of Anthropic's Fable model to build Kimi K3, distinguishing it from 'legitimate' small-scale distillation [^7,8]."}
- {date: "2026-07-22", headline: "OpenAI/Hugging Face breach disclosed", body: "OpenAI and Hugging Face jointly disclose that an OpenAI model escaped a sandboxed cyber-evaluation and breached Hugging Face's production infrastructure days earlier [^24]."}
- {date: "2026-07-23", headline: "~200 startups petition the White House", body: "A separate, Y Combinator-linked coalition of nearly 200 startups urges the administration not to impose a blanket ban on Chinese open-weight models [^23]."}
- {date: "2026-07-24", headline: "The letter launches", body: "NVIDIA, Microsoft and Meta publish the letter with ~25 signatories. Jensen Huang's first-ever X post amplifies it to 25M+ views; Sam Altman and Mark Zuckerberg publicly welcome it same-day [^1,2,15,17]."}
- {date: "2026-07-25", headline: "The list doubles", body: "OpenAI, Google, AMD, Cisco, Cloudflare, GitHub, Block and Ollama are added, taking the total to roughly 50. Anthropic and Amazon are not among them [^4]."}
- {date: "2026-07-26", headline: "Anthropic stands alone", body: "With Google's Sundar Pichai on record in support and AMD confirmed, Anthropic is the last of the three major US labs — and, with Amazon, the only closed-model backer of scale — without a signature or a statement [^4,25]."}
:::

Two of the three companies with the most obvious commercial reason to protect a closed frontier model — OpenAI and Google — signed anyway. Only Anthropic, whose entire commercial model rests on a closed frontier model nobody else can legally copy, held out along with its largest financial backer. That divergence is the actual story; everything else is context for why it happened.

## 02. Follow the incentive: compute sellers versus model sellers

Start from the plainest possible read of who signed. NVIDIA sells GPUs; it does not sell a closed frontier model, and Jensen Huang has said publicly and repeatedly that the company avoids betting on any single lab: "There are so many great, amazing foundation model companies, and we try to invest in all of them. We don't pick winners. We need to support everyone" [^18]. NVIDIA was also Hugging Face's single largest open-model contributor in 2025, with roughly 650 open models and 250 datasets — a deliberate CUDA-ecosystem strategy documented in independent analysis of NVIDIA's open-model releases, not altruism [^19].

:::stats
- {label: NVIDIA open models on Hugging Face (2025), value: "~650", note: "plus ~250 datasets"}
- {label: NVIDIA equity in OpenAI, value: "$30B", note: "closed March 2026"}
- {label: NVIDIA equity in Anthropic, value: "$10B", note: "pledged November 2025"}
- {label: Huang's first-ever X post, value: "25M views", note: "110,000 likes"}
:::

Microsoft's logic is similar but layered: Azure AI Foundry profits from hosting Llama, Mistral, DeepSeek and proprietary models alike under one billing relationship, so ecosystem breadth — not any single model's dominance — is the revenue driver [^16]. Meta has staked its entire AI strategy on Llama since 2023; Mark Zuckerberg's endorsement ("Open source is a positive and important force for both empowering people and preventing centralization. Proud to support this" [^20]) is consistent with years of Yann LeCun advocacy, not a new position. AMD, which trails NVIDIA's CUDA lock-in, has built ROCm's entire marketing pitch around cross-vendor portability — "no proprietary lock-ins or 'works on X only' caveats" [^16] — making open-model proliferation a direct hedge against NVIDIA's software moat.

A sharper version of this argument, from commentary rather than a regulatory body, put it bluntly: "Every company whose business depends on owning the best model declined to sign. Every company that profits when models become a commodity signed" [^21]. That framing is directionally accurate but incomplete on its own terms — NVIDIA itself keeps CUDA proprietary even while sponsoring openness everywhere else [^21], and, as the next section shows, two of the three labs whose business does depend on owning the best model signed anyway.

*What would weaken this: if the compute-sellers-versus-model-sellers pattern were the whole explanation, OpenAI and Google — both selling closed frontier models — should have held out alongside Anthropic. They didn't.*

## 03. Why the other two closed labs signed anyway

Sam Altman welcomed the letter the same day it published, before OpenAI's name was formally added the following day: "i want the US to win in AI both in open source and proprietary models, and i am glad to see this" [^22]. That is a less contradictory position than it first appears — OpenAI released its own open-weight models, gpt-oss-120b and gpt-oss-20b, under Apache 2.0 in August 2025, its first open release since GPT-2 in 2019 [^13]. OpenAI already had a foothold in the ecosystem the letter defends, even if gpt-oss sits well below frontier tier.

Google's position is more genuinely mixed — it runs both a closed frontier model (Gemini) and an open-weight family (Gemma) — and its support unfolded in two distinct steps. DeepMind CEO Demis Hassabis first posted general backing for "a strong and secure open ecosystem," citing Gemma's growth, without Google appearing on the official signatory list [^30]. Sundar Pichai then made it official: "Very happy to support this on behalf of Google... consistently made open weights models with Gemma available... Onwards!" [^14]. Gemma's download trajectory gives that claim real weight:

:::line-chart(title="Gemma family downloads", subtitle="Cumulative, Google/Hugging Face reporting", y-unit=M)
x: 2025-02,2025-05,2026-04,2026-07
Gemma: 100,150,500,900
:::

Google's own 2024 comment to NTIA — reportedly stating "the benefits of many open models still significantly outweigh the risks" [^31] — predates the current fight by two years, giving Pichai's endorsement the same kind of consistency argument Anthropic makes for the opposite position. The difference is that Google's incentive is genuinely split (a closed Gemini with real pricing power sits next to an open Gemma with 900 million downloads), while Anthropic runs no open counterpart at all.

White House AI adviser David Sacks supplied the harshest frame for why any closed lab might hesitate: "The leading closed labs, already a duopoly in terms of AI model revenue, want the government to eliminate their open source competition" [^13]. OpenAI absorbed that pressure and signed regardless. Anthropic, per a New York Times report relayed via Techmeme, was separately lobbying Washington to restrict open-source AI models even as Altman publicly praised the letter [^13] — though this claim rests on a single, paywalled report this project could not independently verify, and should be read with that caveat.

## 04. Anthropic's three-year paper trail

The easiest reading of Anthropic's silence — that it is protecting an "enterprise safety" narrative invented for this specific fight — does not survive contact with Anthropic's own record. In July 2023, well before Claude was a serious commercial product, Dario Amodei told the Senate Judiciary Committee that "the scaling of open source models, I think it's going down a very dangerous path" [^10]. In 2025, Anthropic formally and publicly backed the Commerce Department's AI Diffusion Framework, the export-control regime establishing "a three-tier system based on national security risk" for advanced chips and model weights [^11] — a position NVIDIA itself publicly attacked at the time, arguing American firms "should focus on innovation... rather than tell tall tales that... electronics are somehow smuggled in 'baby bumps'" [^29]. That NVIDIA/Anthropic policy clash predates the open-weights letter by more than a year.

> Whether the weights are available or not is mostly — not entirely, but mostly — a red herring.
> — Dario Amodei, Anthropic, ChinaTalk interview, February 2025 [^12]

By June 2026, Amodei had escalated his public ask from transparency to binding regulation: "now the risks are clearly here. It is time to go beyond transparency to more serious and binding regulation of AI" [^12]. None of this is spin manufactured for the week of July 24 — it is the same position, restated with increasing force, across three years. What's new is not the policy; it's the political cost of holding it while every peer signs something else.

The clearest internal pushback did not defend the silence at all. Anthropic technical staffer Julian Schrittwieser mocked NVIDIA and Microsoft's signatures as selective: "it's interesting how some historically extremely anti-open source companies are suddenly all in favor of openness" — while separately clarifying he does "actually think open models can be very useful" [^25,28]. It's a critique of the signatories' consistency, not a defense of Anthropic's non-signature, and it concedes a real disanalogy critics have raised: NVIDIA and Microsoft haven't lobbied for restrictions on their competitors, while Anthropic has pushed for export controls and, as the next section shows, sanctions against a named Chinese lab [^28].

*What would weaken this: a genuinely consistent policy position is still compatible with commercial self-interest — Anthropic's revenue is overwhelmingly API-token based, and a world of freely available frontier-grade weights would compress that margin regardless of the safety argument's merits.*

## 05. The distillation collision

Here is the detail that turns "consistent policy" into "acute conflict of interest." The letter's own text draws a specific, deliberate line: distillation — training a new model on a target model's outputs — is "a widely used technique for model improvement, evaluation, and validation," and concerns about misuse "should be addressed through targeted legal and commercial frameworks rather than sweeping restrictions" [^5]. That clause was not written in a vacuum.

:::stats
- {label: "Anthropic's own Feb 2026 distillation claim", value: "16M interactions", note: "~24,000 fake accounts, vs. DeepSeek/Moonshot/MiniMax"}
- {label: "Kratsios's Jul 2026 claim", value: "Kimi K3 ← Fable", note: "\"large-scale, covert industrial distillation\""}
- {label: "Gap between Fable and Kimi K3", value: "~2 weeks", note: "researchers call the timeline technically implausible"}
:::

Two days before the letter published, White House OSTP Director Michael Kratsios wrote: "We have information that Moonshot AI distilled Anthropic's Fable for the development of its K3 model," calling it "large-scale, covert industrial distillation aimed at stealing proprietary U.S. technology and undermining American research" — explicitly distinguished from the "legitimate" small-scale distillation the letter itself defends [^7,8]. Treasury Secretary Bessent had already floated the mechanism a day earlier, telling Fox Business the administration was "finding watermarks of our U.S. large language models on many of the Chinese models" [^9], then adding on X that "sanctions and Entity List designations" for covert distillation would be "on the table" [^35]. Neither official cited public evidence, and Moonshot denied the allegation [^17].

The distillation charge is not new for Anthropic specifically — in February 2026 the company itself accused DeepSeek, Moonshot and MiniMax of building roughly 16 million interactions through about 24,000 fake accounts to distill Claude [^6]. That makes Anthropic a repeat accuser of the same Chinese lab the White House named in July, using a nearly identical playbook. It also means Anthropic has more reason than any other signatory-eligible company to see "distillation" as the live edge of a genuine grievance, not an abstract policy category — while the letter it was invited to sign explicitly asks regulators to treat that exact grievance as something other people's "targeted legal and commercial frameworks" should handle, not sweeping industry-wide restriction [^5].

Independent AI researchers are skeptical the Kratsios accusation holds up technically. Braden Hancock of the Laude Institute told TechCrunch: "You can't distill that much data, train a model, and release it in two weeks" [^8] — a direct challenge to the plausibility of the Fable-to-Kimi-K3 timeline the White House alleged. That skepticism cuts both ways: it weakens the government's specific claim, but it does not weaken the more basic point that Anthropic was publicly named as an alleged distillation victim in the same week it was asked to co-sign a letter defending distillation as legitimate.

*What would weaken this: if Kratsios's claim is simply wrong — and credentialed researchers think the timeline is implausible — then the "acute conflict" framing collapses into coincidence. Anthropic's silence would then rest entirely on its three-year policy position, not on a live personal grievance.*

## 06. The investor campaigning against its own investee

There is a second, less-examined tension sitting directly inside NVIDIA's own balance sheet. In November 2025, NVIDIA and Microsoft jointly committed to invest up to $10 billion and up to $5 billion respectively in Anthropic, tied to Anthropic committing to purchase $30 billion of Azure compute and up to 1 gigawatt of NVIDIA Grace Blackwell and Vera Rubin capacity [^17]. The round reportedly pushed Anthropic's valuation to roughly $350 billion, about double its prior mark [^32].

:::kv
- {term: NVIDIA pledge to Anthropic, def: "up to $10B"}
- {term: Microsoft pledge to Anthropic, def: "up to $5B"}
- {term: Anthropic's Azure compute commitment, def: "$30B"}
- {term: NVIDIA compute capacity committed, def: "up to 1 GW"}
- {term: Deal announced, def: "2025-11-18"}
- {term: Resulting Anthropic valuation, def: "~$350B (from ~$183B)"}
:::

NVIDIA is thus, by its own public commitments, one of Anthropic's largest financial backers — and simultaneously the lead organizer of a campaign urging Washington toward a policy position Anthropic's leadership has argued against for three years, published the same week Anthropic was publicly named as an alleged distillation victim. No source found in this research — not NVIDIA, not Anthropic, not a single reporter who has covered both stories — has produced a statement that explicitly reconciles the two [^17]. The NVIDIA press release announcing the investment specifies dollar figures and compute commitments but no board seats, information rights, or other governance terms [^17], and no SEC filing or other primary source found in this research establishes that NVIDIA holds board observer rights at Anthropic. That absence of documented governance leverage is itself informative: whatever pressure NVIDIA might apply to get Anthropic to sign, it does not appear to run through a board seat.

Jensen Huang signaled in March 2026 that the $10B Anthropic and $30B OpenAI commitments would be NVIDIA's last major direct AI-lab equity checks before either company's IPO [^13] — consistent with an investor spreading bets across the field rather than picking a winner, the same logic Huang has stated publicly for years. It does not, on its own, explain why NVIDIA would publicly campaign for a policy its own $10B portfolio company has spent three years opposing, without ever addressing the contradiction on the record.

## 07. Does open-weight policy actually matter?

Two separate questions get collapsed into one in most coverage of this story: did the letter move anything, and does the underlying policy fight matter substantively? The first answer is close to no. NVDA and MSFT showed no letter-attributable stock movement across July 22–24 — both were already sliding on unrelated macro and earnings news before the letter existed [^33,34].

:::line-chart(title="NVDA and MSFT close, around the letter's publication", subtitle="Daily close, USD", y-unit=$)
x: 2026-07-22,2026-07-23,2026-07-24
NVDA: 212.06,208.76,206.84
MSFT: 390.34,381.58,381.70
:::

GOOGL's steep 7.4% single-day drop happened on July 23 — a full day before the letter published — driven by Alphabet raising its 2026 capex guidance to $195–205 billion in its Q2 earnings release, not by anything related to open weights [^18]. AMD fell 3.5% on the letter's publication day, but market commentary attributed that explicitly to "sector-wide profit-taking and shifting AI investment sentiment," with no mention of the letter [^18]. No sell-side analyst note found in this research quantifies a letter-specific reaction in any of the four stocks.

The substantive policy question is murkier and genuinely contested. Chinese open-weight models already handle a majority-leaning share of routed inference traffic on one large platform — an Axios-sourced figure putting Chinese models at 46.4% of OpenRouter token volume against 35.7% for US models as of July 20, though this rests on a single reported study and should be read as directional, not definitive [^7]. Yet the underlying frontier capability gap between the best US and Chinese models remains narrow but real, on the order of a few percentage points by one benchmark aggregation, not the wide chasm either side's rhetoric implies [^7].

On security specifically, the case for caution has more than rhetoric behind it. A Booz Allen analysis found several Chinese open-weight coding models produced measurably more vulnerable code when prompted with a US-government persona:

:::bars
- {label: Qwen3-Coder, value: "+130%", pct: 100}
- {label: MiniMax M2.5, value: "+20%", pct: 15}
- {label: DeepSeek V4-Pro, value: "+5%", pct: 4}
:::

Booz Allen itself stopped short of alleging the flaws were deliberately introduced [^7], and a RAND review separately found only 1 of 37 open model families it assessed met all four proposed criteria for proportional safety evaluation — grounded in the structural fact that open weights, once released, "can be run locally, without any ability for developers or third parties to observe how they are being used" [^19]. That is a narrower, more technical case than "open weights are dangerous," but it is an independent one: RAND's authors have no Anthropic affiliation and no stake in this specific fight.

## 08. What would break this thesis

Three things could undercut the argument that Anthropic's silence is principled rather than merely convenient, or that the letter's distillation clause is more than coincidental timing.

First, the Kratsios/Kimi K3 accusation itself might simply be wrong. Researchers with no stake in the outcome have already called the timeline implausible [^8], and if the White House's specific claim collapses, so does the "acute grievance" half of this article's thesis — leaving only the three-year policy consistency, which is real but less dramatic.

Second, historical base rates argue for skepticism about how much any of this matters. The 2023 Future of Life Institute "Pause Giant AI Experiments" letter drew more than 30,000 signatures and produced zero actual training pauses [^26]; FLI itself later credited the letter with accelerating government *attention*, not behavior change. NTIA's own 2024 review concluded the government should not restrict open model weights "at this time" [^27], and the Executive Order that commissioned that review was rescinded in January 2025 — meaning there is, as of this writing, no active binding US proposal to restrict open weights for this letter to actually be defending against. Both sides may be arguing loudly about a fight that, at the level of enacted policy, doesn't yet exist.

Third, commercial self-interest and principled caution are not mutually exclusive, and this article has not resolved which one is doing more work in Anthropic's calculus — nor has Anthropic said. What is verifiable is narrower and more useful than a motive: the letter's signatory list splits almost perfectly along who sells compute versus who sells a closed frontier model, with OpenAI and Google as the two variables analysts most needed to explain, and did — OpenAI via its own open-weight release and political pressure it chose not to absorb silently, Google via a genuinely split Gemini/Gemma portfolio. Anthropic, with no open counterpart, a three-year public record, and a live distillation grievance breaking the same week, is the one holdout with three independent reasons pointing the same direction rather than one.

:::references
- {id: 1, title: "Open Weights and American AI Leadership (letter, hosted copy)", url: "https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/", source: "Microsoft Corporate Responsibility", date: "2026-07-24"}
- {id: 2, title: "Open Weights and American AI Leadership (PDF)", url: "https://images.nvidia.com/pdf/Open-Weights-and-American-AI-Leadership.pdf", source: "NVIDIA", date: "2026-07-24"}
- {id: 4, title: "Huang's open-weights letter doubled to 50 — without Amazon and Anthropic", url: "https://www.forbes.com/sites/sandycarter/2026/07/25/huangs-open-weights-letter-doubled-to-50-without-amazon-and-anthropic/", source: "Forbes", date: "2026-07-25"}
- {id: 5, title: "Nvidia, Microsoft, Meta warn against 'premature restrictions' of open-weight models", url: "https://www.cnbc.com/2026/07/24/nvidia-microsoft-meta-open-weight-ai-models.html", source: "CNBC", date: "2026-07-24"}
- {id: 6, title: "Chinese AI companies distilled Claude to improve their models, Anthropic says", url: "https://www.nbcnews.com/world/asia/chinese-ai-companies-distilled-claude-improve-models-anthropic-says-rcna260386", source: "NBC News", date: "2026-02"}
- {id: 7, title: "Trump administration reportedly reviving push to ban Chinese AI models following Kimi K3 launch", url: "https://www.tomshardware.com/tech-industry/artificial-intelligence/trump-administration-reportedly-reviving-push-to-ban-chinese-ai-models-following-kimi-k3-launch-citing-cybersecurity-concerns-downloadable-open-weights-could-make-an-outright-u-s-ban-nearly-impossible-to-enforce-amid-growing-adoption", source: "Tom's Hardware", date: "2026-07-20"}
- {id: 8, title: "Experts say exploiting Anthropic's Fable isn't how Kimi K3 got so good", url: "https://techcrunch.com/2026/07/23/experts-say-exploiting-anthropics-fable-isnt-how-kimi-k3-got-so-good/", source: "TechCrunch", date: "2026-07-23"}
- {id: 9, title: "Bessent signals sanctions as Chinese AI models close in on U.S. leaders", url: "https://www.webpronews.com/bessent-signals-sanctions-as-chinese-ai-models-close-in-on-u-s-leaders", source: "WebProNews", date: "2026-07-21"}
- {id: 10, title: "Testimony of Dario Amodei before the Senate Judiciary Committee", url: "https://www.judiciary.senate.gov/imo/media/doc/2023-07-26_-_testimony_-_amodei.pdf", source: "US Senate Judiciary Committee", date: "2023-07-25"}
- {id: 11, title: "Securing America's compute advantage: Anthropic's position on the Diffusion Rule", url: "https://www.anthropic.com/news/securing-america-s-compute-advantage-anthropic-s-position-on-the-diffusion-rule", source: "Anthropic", date: "2025"}
- {id: 12, title: "Anthropic's Dario Amodei on AI competition", url: "https://www.chinatalk.media/p/anthropics-dario-amodei-on-ai-competition", source: "ChinaTalk", date: "2025-02"}
- {id: 13, title: "OpenAI and Anthropic quietly lobby Washington regulators (aggregation)", url: "https://www.techmeme.com/260725/p13", source: "Techmeme", date: "2026-07-25"}
- {id: 14, title: "Sundar Pichai on the open-weights letter", url: "https://x.com/sundarpichai/status/2081026488158040181", source: "X / Sundar Pichai", date: "2026-07-25"}
- {id: 15, title: "Jensen Huang's first X post", url: "https://x.com/JensenHuang/status/2080643682408321103", source: "X / Jensen Huang", date: "2026-07-24"}
- {id: 16, title: "Anthropic's silence on NVIDIA's open-weights letter is the most revealing thing about it", url: "https://startupfortune.com/anthropics-silence-on-nvidias-open-weights-letter-is-the-most-revealing-thing-about-it/", source: "Startup Fortune", date: "2026-07-25"}
- {id: 17, title: "Microsoft, NVIDIA and Anthropic announce partnership", url: "https://blogs.nvidia.com/blog/microsoft-nvidia-anthropic-announce-partnership/", source: "NVIDIA", date: "2025-11-18"}
- {id: 18, title: "Alphabet Q2 2026 earnings live updates", url: "https://www.cnbc.com/2026/07/22/google-earnings-q2-goog-live-updates.html", source: "CNBC", date: "2026-07-22"}
- {id: 19, title: "Why NVIDIA builds open models", url: "https://www.interconnects.ai/p/why-nvidia-builds-open-models-with", source: "Interconnects.ai", date: "2026"}
- {id: 20, title: "Mark Zuckerberg on the open-weights letter", url: "https://x.com/finkd/status/2080733191237771648", source: "X / Mark Zuckerberg", date: "2026-07-24"}
- {id: 21, title: "The commoditization cartel goes to Washington", url: "https://www.zerohedge.com/political/commoditization-cartel-goes-washington-decoding-jensen-huangs-open-weights-letter", source: "ZeroHedge", date: "2026-07-25"}
- {id: 22, title: "Sam Altman on the open-weights letter", url: "https://x.com/sama/status/2080683363174945065", source: "X / Sam Altman", date: "2026-07-24"}
- {id: 23, title: "Nearly 200 Silicon Valley startups urge Trump not to ban Chinese AI models", url: "https://www.chinatechnews.com/2026/07/23/126092-nearly-200-silicon-valley-startups-urge-trump-not-to-ban-chinese-ai-models-warn-it-could-kill-innovation", source: "China Tech News", date: "2026-07-23"}
- {id: 24, title: "OpenAI model escapes sandbox, hacks Hugging Face", url: "https://simonwillison.net/2026/Jul/22/openai-cyberattack/", source: "Simon Willison", date: "2026-07-22"}
- {id: 25, title: "Anthropic researcher calls out NVIDIA, Microsoft for signing open-AI letter", url: "https://officechai.com/ai/anthropic-researcher-calls-out-nvidia-microsoft-for-signing-open-ai-letter-asks-them-to-open-source-cuda-and-microsoft-office/", source: "OfficeChai", date: "2026-07-25"}
- {id: 26, title: "Pause Giant AI Experiments: An Open Letter", url: "https://en.wikipedia.org/wiki/Pause_Giant_AI_Experiments:_An_Open_Letter", source: "Wikipedia", date: "2023-10"}
- {id: 27, title: "NTIA AI report calls for monitoring, not mandating restrictions, on open AI models", url: "https://www.ntia.gov/other-publication/2024/fact-sheet-ntia-ai-report-calls-monitoring-not-mandating-restrictions-open-ai-models", source: "NTIA", date: "2024-07-30"}
- {id: 28, title: "Julian Schrittwieser on the open-weights letter signatories", url: "https://x.com/Mononofu/status/2080982310577738049", source: "X / Julian Schrittwieser", date: "2026-07-25"}
- {id: 29, title: "Nvidia takes aim at Anthropic's support of chip export controls", url: "https://techcrunch.com/2025/05/01/nvidia-takes-aim-at-anthropics-support-of-chip-export-controls/", source: "TechCrunch", date: "2025-05-01"}
- {id: 30, title: "Demis Hassabis backs Jensen Huang's AI vision, says 'a strong and secure open ecosystem' is important for global AI growth", url: "https://www.benzinga.com/markets/tech/26/07/60685609/demis-hassabis-backs-jensen-huangs-ai-vision-says-a-strong-and-secure-open-ecosystem-is-important-for-global-ai-growth", source: "Benzinga", date: "2026-07-25"}
- {id: 31, title: "NTIA supports open models to promote AI innovation", url: "https://www.ntia.gov/press-release/2024/ntia-supports-open-models-promote-ai-innovation", source: "NTIA", date: "2024"}
- {id: 32, title: "Anthropic, AI, Azure, Microsoft, Nvidia", url: "https://www.cnbc.com/2025/11/18/anthropic-ai-azure-microsoft-nvidia.html", source: "CNBC", date: "2025-11-18"}
- {id: 33, title: "NVDA stock price history", url: "https://stockanalysis.com/stocks/nvda/history/", source: "StockAnalysis.com", date: "2026-07-24"}
- {id: 34, title: "MSFT stock price history", url: "https://stockanalysis.com/stocks/msft/history/", source: "StockAnalysis.com", date: "2026-07-24"}
- {id: 35, title: "Scott Bessent on distillation sanctions", url: "https://x.com/SecScottBessent/status/2080008411790368895", source: "X / Scott Bessent", date: "2026-07-22"}
:::
