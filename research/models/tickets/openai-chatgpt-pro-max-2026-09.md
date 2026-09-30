---
slug: openai-chatgpt-pro-max-2026-09
title: "ChatGPT Pro 500 — $500/mo tier shipped at DevDay 2026; Pro 200 limits cut"
company: OpenAI
model: null
status: released
status_note: |
  **App-artifact leak, 2026-09-24, single outlet.** @testingcatalog found a new
  "ChatGPT Pro Max" plan in development (21:26 UTC), then priced it at $500/mo
  (21:42 UTC: "the plan price is $500; it shows $600 due to VAT"), then added
  (23:05 UTC) that it "will likely be powered by @cerebras infrastructure" and
  that "'Fastest Work and Codex' are the only changes in the plan description
  compared to ChatGPT Pro". Their 2026-09-25 daily brief restates all three and
  fixes DevDay at Sept 29.

  **What is artifact and what is inference.** ARTIFACT: a plan entry exists in
  the product with a $500 price and a description string differing from Pro by
  "Fastest Work and Codex". INFERENCE: that Cerebras serves the fast path, and
  that limits rise. @testingcatalog labels the Cerebras claim "likely", which
  is their own hedge, not a source. Treat the plan string as real and
  everything downstream of it as unconfirmed.

  **Why the Cerebras read is plausible but unproven.** "Fastest" as the sole
  differentiator points at an inference-speed tier rather than a capability
  tier, and a speed tier implies non-NVIDIA serving silicon. That is an
  inference from a product string, not evidence; OpenAI has its own Jalapeño
  inference ASIC in flight ([[openai-jalapeno-chip-2026-06]]), which is an
  equally good fit for the same string.

  **Pricing context.** $500/mo would be five times the $200 ChatGPT Pro tier
  and, if it ships, among the most expensive publicly-listed AI subscriptions.
  It lands against Anthropic's opposite move in the same week — Opus 5.5 at
  ~40% below Opus 5 with limits users describe as effectively unlimited
  ([[anthropic-opus-5-5-2026-09]]) — which is the competitive frame to read it
  in, not the absolute number.
expected: "RELEASED 2026-09-29 at OpenAI DevDay as ChatGPT Pro 500 ($500/mo, ~25x Plus, includes Ultrafast and a first Dot). The leaked $500 price was right; the leaked NAME ('Pro Max') was not, and the Cerebras attribution is still unconfirmed. Open: what silicon is behind Ultrafast, whether the announced Pro 200 cuts take effect as stated on 2026-10-30, and whether Plus gets any of it."
labels:
  - openai
  - chatgpt
  - pricing
  - leak
  - unreleased
verification: confirmed
sources:
  - https://x.com/testingcatalog/status/2103234677842559034
  - https://x.com/testingcatalog/status/2103238785278312463
  - https://x.com/testingcatalog/status/2103259620592542102
  - https://x.com/testingcatalog/status/2103371709281632423
  - https://x.com/TokenGremlin/status/2103974482217976138
  - https://x.com/testingcatalog/status/2103824776905028038
  - https://x.com/AM09_21/status/2104567237428629560
  - https://x.com/damobianyuan/status/2105149575598379257
  - https://x.com/masahirochaen/status/2105147966889886057
  - https://x.com/insanekrishnaa/status/2105147666850304017
  - https://x.com/MagicPower21M/status/2105148814105710821
  - https://x.com/sir_franco_/status/2105146907530006880
created_at: 2026-09-25
updated_at: 2026-09-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-25
    change: "Created — IN-TESTING / unverified. @testingcatalog surfaced a 'ChatGPT Pro Max' plan in development on 2026-09-24 across three posts: the plan exists (21:26 UTC), it is priced at $500/mo with $600 shown inclusive of VAT (21:42 UTC, ~2,037 likes), and its description differs from ChatGPT Pro only by 'Fastest Work and Codex', with Cerebras 'likely' behind the fast path (23:05 UTC, ~1,603 likes); their 2026-09-25 daily brief repeats all three and pins DevDay to Sept 29. Status in-testing rather than rumored because a concrete product artifact exists — a plan entry with a price and a description string — not merely a tease. Verification unverified because it is ONE outlet reading one app surface, with no OpenAI statement. The Cerebras attribution is explicitly the outlet's own inference and is recorded as such; OpenAI's Jalapeno inference ASIC ([[openai-jalapeno-chip-2026-06]]) fits the same 'Fastest' string equally well. Recorded against [[anthropic-opus-5-5-2026-09]] as the competitive frame: OpenAI appears to be testing a 5x-of-Pro premium tier in the same week Anthropic cut Opus pricing ~40% and shipped limits users describe as effectively unlimited."
  - ts: 2026-09-28
    change: "Two independent product-surface changes now point the same way, and one of them is a REGRESSION in disclosure rather than a feature. (1) @TokenGremlin (2026-09-26 22:26 UTC): OpenAI removed the '5x, 10x, 20x' usage multipliers from the plan-upgrade UI, replacing them with 'More usage than Plus' — 'I really hate this kind of vague wording, and I hope they reconsider it before this goes public around DevDay.' Amplified critically by @ns123abc. That matters for this ticket specifically: the leaked Pro Max description differs from Pro only by 'Fastest Work and Codex' and says nothing about limits, and a vendor that has just deleted its numeric limit disclosures is a vendor about to sell a tier whose limits cannot be compared. (2) @testingcatalog (2026-09-26 12:31 UTC): a Speed selector with Fast / Standard / Ultrafast modes is coming to the Responses API Playground after DevDay, expanding the previously partner-only Ultrafast model. An inference-speed product line existing at the API layer is direct support for reading 'Fastest' in the Pro Max string as a serving-speed tier rather than a capability tier — which is what this ticket already inferred and can now point at something for. Verification unverified -> partial: the plan string, the multiplier removal and the Ultrafast selector are three separate observed surfaces from two independent accounts. Status stays in-testing; still no OpenAI announcement, final price, limit disclosure or confirmation of the Cerebras inference (which remains @testingcatalog's own hedge). DevDay is 2026-09-29 and @AM09_21 lists ChatGPT Pro Max ($500), 'o' and Aeon as the strongest leaks going in."
  - ts: 2026-09-30
    change: "SHIPPED, AND THE LEAK SCORES AS HALF-RIGHT. At OpenAI DevDay on 2026-09-29 OpenAI introduced a new top consumer tier at $500/mo. The leaked PRICE was exactly right; the leaked NAME was not — it shipped as 'Pro 500', not 'ChatGPT Pro Max'. That is the cheapest available calibration on @testingcatalog's app-surface reads: the plan entry and its price were real observations, the label attached to them was not. Status in-testing -> released, verification partial -> confirmed. What the tier contains, per multiple independent DevDay recaps (@masahirochaen's 25-item roundup, @insanekrishnaa, @MagicPower21M, and @damobianyuan quoting the customer email he received): roughly 25x Plus allowances against Pro 200's 20x, inclusion of Ultrafast, and a bundled Dot ([[openai-dots-agents-2026-09]]). This ticket's central inference is VINDICATED — 'Fastest' was a serving-speed SKU, and Ultrafast is described at about 300 tokens/sec, up to ~8x normal generation at roughly 6x the API price. The Cerebras attribution remains unconfirmed and is still @testingcatalog's own hedge; nothing in this cycle names the silicon, so [[openai-jalapeno-chip-2026-06]] stays an equally live explanation. THE PART THE LEAK NEVER MENTIONED, AND THE MORE CONSEQUENTIAL HALF: the existing $200 Pro 200 tier is being CUT, not left alone. Per @damobianyuan's copy of the email — he confirmed the credits landed in his Codex client, so this is a firsthand artifact rather than a relay — from 2026-10-30 ChatGPT Work + Codex allowances drop from 20x Plus to 10x, and GPT-6 Pro chat messages drop from 200/week to 100/week, with OpenAI stating it will not restore the old 5-hour windows. Existing Pro subscribers are compensated with 62,500 credits (~$2,500) valid to 2026-12-31. This is why the 2026-09-28 entry's read on the deleted '5x/10x/20x' multipliers matters: a vendor that removes numeric limit disclosure two days before repricing the tier those numbers described was not tidying up its UI. Reception is hostile from below rather than above — @sir_franco_ catalogues Plus getting the 5-hour limit back, no day-one Dots access and no new Astra-line chat models, and @AaronBergquist reads the move as 'economic necessity rather than greed' while calling a 2.5x rise to keep existing usage 'a tough pill to swallow'. Both are user sentiment, recorded as such."
---

A $500 tier is a pricing experiment, and its interesting feature is that the
leaked description does not promise a better model.

The only delta from ChatGPT Pro is "Fastest Work and Codex". That is a
latency/throughput SKU, not a capability SKU — you are buying the same
intelligence sooner. Selling speed as the premium good only works if the
marginal buyer is running long agentic jobs where wall-clock is the binding
constraint, which is exactly the Codex workload OpenAI has been building
toward.

It also arrives at an awkward moment. The same week, Anthropic shipped Opus 5.5
roughly 40% cheaper than its predecessor with usage limits developers
publicly describe as feeling unlimited, and Vercel's gateway data showed Opus
5.5 taking up to 10% of spend within two days. Launching a five-times-Pro tier
into that is either a confident read of a distinct segment or a margin move
that invites unflattering comparison.

Two things would move this off `unverified`: an OpenAI announcement at DevDay
on Sept 29, or a second independent observer finding the same plan string. A
Cerebras confirmation would be a third, separate claim and should not be
folded into the first.

If DevDay comes and goes without it, this is a staged-and-shelved product entry
and should close as a stale rumor rather than linger.
