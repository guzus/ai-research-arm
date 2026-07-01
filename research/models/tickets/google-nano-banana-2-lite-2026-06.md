---
slug: google-nano-banana-2-lite-2026-06
title: Google Nano Banana 2 Lite — cheap at-scale image model
company: Google / DeepMind
model: gemini-3.1-flash-lite-image (Nano Banana 2 Lite)
status: released
status_note: |
  **Shipped 2026-06-30** as a live model on **Google AI Studio** and as the
  Flash Lite option in the Gemini app (@testingcatalog 15:38 UTC, ~80 likes):
  `gemini-3.1-flash-lite-image`, "our smallest and most cost-effective image
  generation and editing model, built for at-scale usage." **~4s generation**
  at ~**$0.034/image** (**$0.25 image input / $0.0336 output**). The shipped
  follow-through to the prior cycle's string leak — Google's fastest/cheapest
  image SKU yet, trading some quality for speed. A distinct SKU below the
  full Nano Banana 2 / Pro line (closed [[google-nano-banana-2-2026-05]]).
expected: null
labels:
  - google
  - image-generation
  - multimodal
  - released
  - low-cost
verification: confirmed
sources:
  - "@testingcatalog"
  - https://x.com/i/status/2071981784846258503
created_at: 2026-07-01
updated_at: 2026-07-01
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-01
    change: "Created — Google shipped Nano Banana 2 Lite (`gemini-3.1-flash-lite-image`) on 2026-06-30, surfaced live on Google AI Studio with published pricing and selectable as the Flash Lite option in the Gemini app (@testingcatalog 15:38 UTC). ~4s images at ~$0.034 each ($0.25 input / $0.0336 output); Google's smallest/cheapest image model, built for at-scale usage. Status released (live and usable on Google's own surfaces), verification confirmed — but no official Google/DeepMind blog post or independent capability benchmarks yet; 'cost-effective'/'at-scale' framing is Google's. Distinct SKU below the full Nano Banana 2 / Pro line, which closed released-and-aged ([[google-nano-banana-2-2026-05]])."
---

**Nano Banana 2 Lite** (`gemini-3.1-flash-lite-image`) is Google's cheapest,
fastest image-generation-and-editing SKU, **shipped 2026-06-30** as a live
model on **Google AI Studio** and as the Flash Lite option in the Gemini app
(first surfaced by @testingcatalog). It generates images in **~4 seconds** at
roughly **$0.034 apiece** ($0.25 image input / $0.0336 output), explicitly
"built for at-scale usage."

**Why its own ticket.** The full **Nano Banana 2 / Nano Banana Pro** line
([[google-nano-banana-2-2026-05]]) shipped in May and was **closed
released-and-aged** on 2026-06-26. Per that ticket's transition triggers, a
new SKU (a distinct Lite tier on a new model id) gets its own ticket rather
than reopening the closed one. This ticket carries the Lite lifecycle; the
video-first Gemini Omni stack is separate ([[gemini-omni]] /
[[gemini-omni-api-2026-06]]).

**Confirmed vs. pending.** The launch is not in doubt — it is live on
Google's own platform with published pricing, so `released` / `confirmed`.
What's missing is an **official Google/DeepMind announcement post** and any
**independent capability benchmarks**: "cost-effective" and "at-scale" are
Google's framing, and quality versus the full Nano Banana 2 (or rival cheap
image models) is untested in public.

**Transition triggers:**
- Official Google post / benchmarks / Vertex rollout → UPDATE.
- Pricing or availability moves → append history here.
- ≥4 weeks settled into normal coverage → close `released-and-aged`.

**Dedup note:** further Nano Banana 2 Lite pricing/benchmark/availability
signal UPDATES this ticket; a later Nano Banana 3 or rebrand gets a new
ticket.
</content>
