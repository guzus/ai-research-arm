---
slug: huggingface-sale-exploration-2026-08
title: NVIDIA agrees to acquire Hugging Face for $12.9B (ticket opened as a sale exploration)
company: Hugging Face / NVIDIA
model: null
status: confirmed
status_note: |
  **Reuters, citing Business Insider sources**, reports that **Hugging
  Face is exploring a potential sale** that could value the company at
  **$13B or more** (relayed by @dongwukeji, 2026-08-24 07:01 UTC). The
  relay is explicit about what has *not* happened: **no transaction has
  been announced and no buyer has been publicly identified.**

  Scale context carried in the same relay, from Hugging Face's own
  published figures: the Hub hosts **2M+ models, 1.5M+ datasets and 1.5M+
  AI applications**, with enterprise features (private repos, SSO, access
  controls, resource groups, private datasets, managed collaboration)
  layered on top.

  Status `rumored`: "exploring a sale" is a process, not an event, and
  the source chain itself (Reuters → Business Insider sources → a single
  aggregator relay) is two removes from anyone with knowledge.
  Verification `partial`: two named outlets are in the chain, which is
  more than an anonymous leak, but **no Hugging Face statement and no
  direct capture of either outlet's article** exists in this run, and
  @HuggingFace's own account posted nothing in the window.

  **2026-08-25 — the financials behind the price arrived, and the process
  got two concrete details.**

  *Revenue.* **The Information**, via @rohanpaul_ai (2026-08-25 01:27
  UTC): Hugging Face's **annualized revenue has jumped 50% to more than
  $150M in two months**, driven by **paid compute, storage and
  subscriptions** around the model hub. That is the first number that
  makes the $13B ask legible — it implies roughly an **~85x forward
  revenue multiple**, which is a platform-optionality price, not a SaaS
  price.

  *Process.* @mark_k (2026-08-24 15:13 UTC): the company is "**working
  with a bank** to gauge acquisition interest at a valuation of $13B+,
  according to **Business Insider**. **No bidder has been named yet**,"
  and notes the ask is "almost **3x its $4.5B valuation from 2023**."
  @ValonHajredini adds the founders' posture: it "is fielding $13B buyout
  offers. **Founders say they still feel loyal to the community, so a
  sale is no sure thing.**"

  Status stays `rumored` — a retained bank gauging interest with no named
  bidder is still a process, and the founders are on record that it may
  not happen. Verification stays `partial`: a second named outlet (The
  Information) now sits alongside Reuters/BI, which is real corroboration
  of the *process*, but **still no Hugging Face statement and still no
  direct capture of any of the three articles**.

  **What the revenue mix says about why anyone would pay.** @stretchcloud
  makes the structural argument on the record: the growth is coming from
  the **infrastructure layer** — caching, bandwidth, inference endpoints,
  hosting — not from enterprise contracts or licensing, so "whoever hosts
  the weights collects the infrastructure tax," with data gravity making
  migration expensive. That is an argument about *durability* of the cash
  flow, and it is analysis rather than a disclosed figure.

  **2026-08-27 — the bidder is NVIDIA and the deal is reported done, at
  $12.9B.** The sequence landed inside 34 minutes overnight.
  @AndrewCurran_ (01:03 UTC) first reported that "**NVIDIA and Hugging
  Face have had serious acquisition conversations in recent weeks** about
  a deal that would value Hugging Face at over $13 billion," matching
  @jukan05's "NVIDIA Seeks to Acquire Hugging Face." At **01:35 UTC**
  @AndrewCurran_ followed with "**The Information is reporting that the
  deal is done**," and @jukan05 carried the headline verbatim: "**THE
  INFORMATION: NVIDIA AGREES TO BUY OPEN-SOURCE MODEL REPOSITORY HUGGING
  FACE FOR $12.9 BILLION**." **@theinformation itself RT'd its reporter
  @amir** ("big news y'all: Nvidia agrees to take Hugging Face for $12.9
  billion"), which puts the outlet's own account behind the scoop rather
  than a relay of it.

  Status moves `rumored` → `confirmed` on the contract's
  "primary-source news, or multi-source corroboration" leg: the reporting
  outlet's own account plus the byline reporter, with TechCrunch
  (@AlchemyGrove, @TechThought_org relaying) and a Reuters-linked
  aggregator carrying the same $12.9B figure independently.
  **Verification stays `partial`, deliberately** — there is still **no
  NVIDIA statement, no Hugging Face statement, no filing, and no
  regulatory notice**. Every account in the window says "reportedly" or
  "agrees to," which is signed-deal reporting, not a closed transaction.

  **The one datapoint from inside Hugging Face is a non-denial.**
  @mervenoyann (HF) posted a long correction of "misinfo… about our job"
  describing the compute/storage/hosting business, and ended it: "**AMA if
  you have more questions (except for nvidia deal)**." Carving the deal
  out of an otherwise open AMA is not confirmation, but it is
  inconsistent with there being nothing to confirm.

  **The price is now reconcilable with this ticket's own revenue figure.**
  @kimmonismus: The Information puts HF at "**roughly $150 million in
  annualized revenue, valuing the deal at about 80× forward revenue**" —
  the same ~$150M this ticket recorded on 2026-08-25, so the multiple
  is internally consistent (~80–86× depending on the exact revenue
  denominator). @mark_k notes the price is "nearly 3x its $4.5B valuation
  from 2023."

  **Why NVIDIA, per the analysts on the record.** @kimmonismus:
  "Nvidia is paying for **strategic control, not current sales**. Strong
  open models help protect demand for its GPUs as OpenAI, Anthropic,
  Google and other major customers develop competing AI chips" — i.e. the
  hedge is against exactly the custom-silicon programs this ticket set
  already tracks ([[openai-jalapeno-chip-2026-06]],
  [[google-frozen-v2-chip-2026-07]]). @MikeBradleyAI reads it as
  cumulative: "Stacking the Poolside deal (which they worked so hard not
  to call an acquisition) with a HF purchase would really lock Nvidia
  into the ultimate epicenter of the open weights LLM universe"
  ([[nvidia-poolside-license-2026-08]]). @theo's comparison —
  "Microsoft buying GitHub feels identical to NVIDIA buying HuggingFace…
  wild that GitHub was worth $7.5b and HuggingFace is $12.9b" — is the
  cleanest frame for what is being priced.

  **The unpriced risk nobody in-window has answered:** a hardware vendor
  owning the default distribution point for open weights is a
  concentration question, and antitrust review is raised only by low-reach
  aggregator commentary here, not by any named outlet. Recorded as an open
  question, not a finding.
expected: "As of 2026-08-27: The Information reports NVIDIA has AGREED to acquire Hugging Face for $12.9B (~80x the ~$150M annualized revenue, ~3x the $4.5B 2023 mark), carried by the outlet's own account and its byline reporter @amir, with TechCrunch and Reuters-linked coverage matching the figure. Neither company has issued a statement; an HF employee explicitly excluded the deal from an open AMA. Pending: an NVIDIA or Hugging Face confirmation, deal terms and structure, regulatory/antitrust review of a chip vendor owning the default open-weights host, and what changes for Hub distribution, the CUDA-neutrality of hosted inference, and Nemotron"
labels:
  - hugging-face
  - nvidia
  - open-weights
  - infrastructure
  - m-and-a
verification: partial
sources:
  - "@dongwukeji"
  - https://x.com/dongwukeji/status/2091782952657244467
  - "@rohanpaul_ai"
  - "@mark_k"
  - "@ValonHajredini"
  - "@stretchcloud"
  - "@AndrewCurran_"
  - https://x.com/AndrewCurran_/status/2092788129052909831
  - "@jukan05"
  - https://x.com/jukan05/status/2092788554216992815
  - "@theinformation"
  - "@amir"
  - "@kimmonismus"
  - "@mervenoyann"
  - "@theo"
  - "@MikeBradleyAI"
created_at: 2026-08-24
updated_at: 2026-08-27
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-24
    change: "Created — Reuters, citing Business Insider sources, reports Hugging Face is exploring a potential sale valuing it at $13B or more; no transaction announced and no buyer identified (relayed by @dongwukeji 2026-08-24 07:01 UTC, which also carries Hugging Face's own Hub scale figures: 2M+ models, 1.5M+ datasets, 1.5M+ applications). Status rumored — an exploration is a process, not an event. Verification partial: two named outlets sit in the chain but neither article was directly captured, no Hugging Face statement exists, and @HuggingFace posted nothing in the window. Matters to this lane because the Hub is the default distribution channel for every open-weights ticket in the set."
  - ts: 2026-08-25
    change: "Financials and process detail arrive. The Information (via @rohanpaul_ai 2026-08-25 01:27 UTC) reports annualized revenue jumped 50% to more than $150M in two months, driven by paid compute, storage and subscriptions around the model hub — the first figure that makes the ask legible, implying roughly an 85x forward multiple at $13B. @mark_k, citing Business Insider, says the company is working with a bank to gauge acquisition interest at $13B+ with no bidder named, and notes the ask is almost 3x its $4.5B 2023 valuation; @ValonHajredini adds the founders' posture that community loyalty means a sale is no sure thing. @stretchcloud argues the growth is infrastructure-layer (caching, bandwidth, inference endpoints) rather than enterprise contracts or licensing, so the cash flow is defended by data gravity — analysis, not a disclosed figure. Status stays rumored: a retained bank gauging interest with no named bidder and founders publicly hedging is still a process. Verification stays partial — The Information now joins Reuters/BI as a third named outlet corroborating the process, but there is still no Hugging Face statement and no direct capture of any article."
  - ts: 2026-08-27
    change: "Status rumored -> confirmed. The bidder is NVIDIA and the deal is reported agreed at $12.9B. Overnight sequence: @AndrewCurran_ (01:03 UTC) reported NVIDIA and Hugging Face had 'serious acquisition conversations in recent weeks' at a $13B+ valuation, matching @jukan05's 'NVIDIA Seeks to Acquire Hugging Face'; 32 minutes later @AndrewCurran_ posted 'The Information is reporting that the deal is done' and @jukan05 carried the headline 'THE INFORMATION: NVIDIA AGREES TO BUY OPEN-SOURCE MODEL REPOSITORY HUGGING FACE FOR $12.9 BILLION'. @theinformation's own account RT'd its byline reporter @amir ('Nvidia agrees to take Hugging Face for $12.9 billion'), so the outlet is behind the scoop directly rather than through a relay; TechCrunch and a Reuters-linked aggregator carry the same figure independently. Verification held at partial on purpose: no NVIDIA statement, no Hugging Face statement, no filing, no regulatory notice, and every account says 'reportedly'/'agrees to' — signed-deal reporting, not a closed transaction. The one inside-HF datapoint is a non-denial: @mervenoyann posted a long correction about what Hugging Face's business actually is and closed with 'AMA if you have more questions (except for nvidia deal)'. Price reconciles with this ticket's own 2026-08-25 figure — The Information puts HF at roughly $150M annualized revenue, making the deal ~80x forward revenue (@kimmonismus) and ~3x the $4.5B 2023 valuation (@mark_k). Rationale on the record from @kimmonismus: NVIDIA is buying strategic control rather than sales, hedging against OpenAI/Anthropic/Google custom silicon by keeping the open-weights ecosystem on CUDA; @MikeBradleyAI reads it as stacking on [[nvidia-poolside-license-2026-08]]; @theo's GitHub/Microsoft comparison ($7.5B then vs $12.9B now) frames what is being priced. Title updated to name the buyer, slug immutable per convention. Open and unanswered in-window: antitrust review of a hardware vendor owning the default open-weights distribution point, raised only by low-reach aggregators, recorded as a question rather than a finding."
---

**NVIDIA has agreed to acquire Hugging Face for $12.9B**, per The
Information (2026-08-27). The ticket opened three days earlier on a
buyer-less "exploring a sale at $13B+" report; the price barely moved and
the buyer turned out to be the chip vendor.

**Why an infrastructure company earns a ticket in a model lane.** Almost
every open-weights release this ticket set tracks — Qwen
([[alibaba-qwen-3-8-27b-2026-08]]), GLM ([[zhipu-glm-5-3-2026-08]]),
Kimi K3 ([[moonshot-kimi-k3]]), Gemma ([[gemma-4]]), Inkling
([[thinking-machines-inkling-small-2026-07]]) — reaches users through the
Hub. Distribution is not neutral: whoever owns the default host of open
weights owns a chokepoint on how, and to whom, open models propagate.
That is the same argument that made [[stripe-openrouter-acquisition-2026-08]]
a model-lane ticket rather than a fintech one, and the two land eight
days apart.

**The valuation is the thing to watch, not the rumor.** $13B for a
company that trains no frontier model, at a moment when open-weight
share of tokens on one large gateway went from 28% to 62% in two months
(@GavinSBaker's Vercel-sourced chart, same window), is a price on
*distribution* rather than on capability. If it clears, it is evidence
that the routing and hosting layer is being repriced upward while model
serving prices fall.

**Who is buying it changes the answer.** A financial buyer at $13B would
have been a price on distribution. NVIDIA at $12.9B is a price on
*keeping that distribution on CUDA*: the argument @kimmonismus relays is
that strong open models protect GPU demand precisely as OpenAI, Anthropic
and Google build their own silicon ([[openai-jalapeno-chip-2026-06]],
[[google-frozen-v2-chip-2026-07]]). Read against
[[nvidia-poolside-license-2026-08]] — the deal NVIDIA "worked so hard not
to call an acquisition" — this is the second time in a month NVIDIA has
paid to sit closer to where models are made and served.

**What would move this to `released`/closed:** an NVIDIA or Hugging Face
confirmation, or deal terms in a filing. What would reopen doubt: a
denial from either side, or the reporting failing to firm up — every
account in the window still says *reportedly*.

Related: [[openrouter-series-b-2026-05]],
[[industry-open-weights-letter-2026-07]],
[[nvidia-poolside-license-2026-08]].
