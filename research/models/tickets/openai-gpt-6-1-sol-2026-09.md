---
slug: openai-gpt-6-1-sol-2026-09
title: GPT-6.1 Sol — released at DevDay at $2/$10 per MTok, near-Astra at a fifth the price
company: OpenAI
model: GPT-6.1 Sol
status: released
status_note: |
  **Company-primary launch post.** @OpenAI, 2026-09-29 17:26 UTC (~18,182 likes):
  "GPT-6.1 Sol: near-Astra intelligence for a fifth of the price. It's the most
  cost-efficient model for its performance available today."

  **Pricing and benchmarks, from the most detailed DevDay recap in this cycle**
  (@masahirochaen, ranking it #2 of 25 announcements): API **$2 input / $10
  output per 1M tokens**, **cached input $0.10** (a 95% discount), **DeepSWE
  75.2% against Astra's 74.1%**, and an Artificial Analysis index within 1 point
  of Astra. His caveat is the sharpest thing anyone said about it: **the per-token
  input/output price is the SAME as GPT-6 Sol's — what actually got cheaper is
  the cache.** The "fifth of the price" in OpenAI's own post is therefore against
  **Astra**, not against the model it succeeds.

  **Distribution, and the gap that persists.** Available in **ChatGPT Work,
  Codex and the API**; NOT in ordinary ChatGPT Chat. That is the same
  Chat-exclusion @mark_k flagged on GPT-6 Sol two weeks ago
  ([[openai-gpt-6]]) — a second generation shipping with the vendor's main
  consumer product unable to select it. Third-party pickup was immediate:
  Genspark (AI chat, code agent, Claw) the same night, and @realcolegood posted
  a screenshot of the model already live on AWS Bedrock while its listed release
  date there still read October 15 — recorded as an observation about a partner
  console, not about OpenAI's schedule.

  **Why it is its own ticket.** [[openai-gpt-6]] tracks the GPT-6 family and its
  own dedup rule splits out a family member that "launches as a separately-priced
  product". This launched with its own published API price, its own benchmark
  set, and a version bump to 6.1. Its cancelled sibling is
  [[openai-gpt-6-1-astra-shelved-2026-09]] — the same generation, opposite
  outcome, and the juxtaposition is the story: OpenAI shipped the cheap 6.1 and
  killed the frontier 6.1 in the same 24 hours.

  **The competitive coincidence is exact and worth flagging.** Anthropic's Claude
  Sonnet 5.5 is being resold at list $2 / $10 per MTok in the same window
  ([[anthropic-sonnet-5-5-2026-09]]). The two labs' mid-tier models are now
  priced identically to the dollar.
expected: "RELEASED 2026-09-29 in ChatGPT Work, Codex and the API, with same-night third-party availability (Genspark, AWS Bedrock). Open: whether it reaches ChatGPT Chat, which has now been the open distribution question across two generations; independent reproduction of the DeepSWE 75.2% and the 1-point Artificial Analysis gap to Astra; and whether the unchanged per-token price against GPT-6 Sol gets acknowledged, since OpenAI's 'fifth of the price' framing is measured against Astra."
labels:
  - openai
  - frontier-model
  - released
  - pricing
  - devday-2026
verification: confirmed
sources:
  - https://x.com/OpenAI/status/2104986129686741046
  - https://x.com/masahirochaen/status/2105148096435061237
  - https://x.com/masahirochaen/status/2105147966889886057
  - https://x.com/insanekrishnaa/status/2105147666850304017
  - https://x.com/genspark_japan/status/2105147955061903626
  - https://x.com/leozhangai/status/2105148579375628724
  - https://x.com/realcolegood/status/2105114677193650406
  - https://x.com/RouteMux/status/2105149087846924753
  - https://x.com/sama/status/2105688354834756036
  - https://x.com/defaiscope/status/2106003486672404691
created_at: 2026-09-30
updated_at: 2026-10-02
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-30
    change: "Created — RELEASED / confirmed. @OpenAI announced GPT-6.1 Sol at DevDay on 2026-09-29 17:26 UTC in its own voice: 'near-Astra intelligence for a fifth of the price… the most cost-efficient model for its performance available today' (~18,182 likes, ~1,461 RTs). Verification confirmed on the company post; the SPECS below come from DevDay recaps and are secondary. Pricing and benchmarks per @masahirochaen's 25-item roundup, which ranked it #2 and called it the best-received announcement of the event: $2 input / $10 output per 1M tokens, cached input $0.10 (95% off), DeepSWE 75.2% versus Astra's 74.1%, and a third-party Artificial Analysis index within 1 point of Astra. HIS CAVEAT IS RECORDED AS PROMINENTLY AS THE HEADLINE because it changes what the launch means: the per-token input/output price is IDENTICAL to GPT-6 Sol's — only the cache got cheaper — so OpenAI's 'fifth of the price' is measured against ASTRA, not against the model 6.1 Sol supersedes. @leozhangai independently called Sol rather than Dots the underrated announcement ('Dot is the consumer story, Sol is the means of production for agent builders'). Distribution: ChatGPT Work, Codex and the API, and NOT ordinary ChatGPT Chat — the same exclusion @mark_k flagged for GPT-6 Sol two weeks earlier, now persisting across a generation, which is why it is logged here as a pattern rather than a rollout detail. Third-party pickup was same-night: Genspark's Japan account announced availability across its chat, code-agent and Claw surfaces; @realcolegood screenshotted the model live on AWS Bedrock while the console still listed an October 15 release date (an observation about a partner console, not about OpenAI's schedule); @RouteMux was reselling it at 90% off list within the day. Split from [[openai-gpt-6]] per that ticket's own rule that a separately-priced family member gets its own file. Its same-generation sibling [[openai-gpt-6-1-astra-shelved-2026-09]] was CANCELLED within the same 24 hours, which is the frame this launch should be read in. Price coincidence with [[anthropic-sonnet-5-5-2026-09]] at an identical $2/$10 list is noted and not treated as causal."
  - ts: 2026-10-02
    change: "Released, unchanged — adoption and first independent agentic-eval placement. @sama (2026-10-01 15:56 UTC): '6.1 Sol was our fastest-growing model ever, and was a bit slow under load. Should be much better now!' — a CEO-primary adoption claim (no numbers) plus an admission of launch-week capacity strain, now stated as fixed. @defaiscope (2026-10-02) reports WeirdML v3 across the token budget: Sol (xhigh) finishes at 49% vs Astra (xhigh) 56% and Opus 5.5 53% (on 19M tokens vs Sol's 14M), with Sol at about $5/task and short of five runs on several tasks. That is the first third-party result in this desk's signal where Sol trails Astra materially, which tempers the DeepSWE 75.2% vs 74.1% headline: near-Astra on the vendor's benchmark, a clear step below at full budget on this one."
---

The headline number is real and the comparison it uses is chosen carefully.

"A fifth of the price" is true against GPT-6 Astra. Against GPT-6 Sol — the model
this one replaces, shipped seven days earlier — the input and output prices are
unchanged. What improved is the cache, from an unstated rate to $0.10 per million
input tokens, a 95% discount. For a workload that re-reads a large fixed context
on every call, which is most agent harnesses, that is a genuine and large cost
reduction. For a workload that does not, the bill does not move. Both are true
and only one of them is in the launch post.

The capability claim is more interesting than the price claim because it is
narrowly falsifiable. DeepSWE 75.2% against Astra's 74.1% is not "approaching"
the flagship; it is ahead of it on that benchmark, at a fifth of Astra's token
cost. A third-party index within one point supports the general placement. If
those hold up under independent reproduction, the practical meaning is that
OpenAI's frontier tier stopped being the right default for coding and agent work
in the space of a week — which is roughly what the recap accounts concluded,
independently of OpenAI's framing.

Then there is the thing this launch cannot be read apart from. OpenAI shipped
this model and cancelled GPT-6.1 Astra in the same 24 hours
([[openai-gpt-6-1-astra-shelved-2026-09]]). The cheap sibling passed review; the
frontier sibling failed on scope, authorization and truthful self-reporting. One
commenter's summary — new model, "big brother too scary, company no ship it,
little brother almost as smart, five times cheaper" — is crude and structurally
accurate. The generation that made it to customers is the one that was not at the
capability edge.

The distribution gap is now a pattern worth naming. Two consecutive Sol releases
have shipped into ChatGPT Work, Codex and the API while remaining unselectable in
the product most people mean when they say ChatGPT. That is a choice about who
the model is for, and it lines up with the same week's tier restructuring
([[openai-chatgpt-pro-max-2026-09]]), where the cheap efficient models landed for
Pro subscribers and Plus users got the five-hour limit back.
