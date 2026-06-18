---
slug: deepseek-v4-vision-2026-06
title: DeepSeek ships Vision (image understanding) for V4
company: DeepSeek
model: DeepSeek V4 (Vision)
status: released
status_note: |
  DeepSeek turned on **image understanding for its V4 model** — a team
  researcher (**@PKUCXK / Xiaokang Chen**, 2026-06-18) announced "**Vision is now
  live on web and app**." It adds multimodal capability to the existing V4 line
  rather than a new base model. Live and widely relayed → status `released`; the
  announcement is from a **DeepSeek team member's personal account** (not the
  official @deepseek_ai handle or a model card) and no independent vision
  benchmarks exist yet → verification `partial`. Whether it reaches the **API and
  open weights** (vs. just the consumer app) is open.
expected: "Vision live on DeepSeek web + app now; official @deepseek_ai post / model card, API + open-weights rollout, and third-party multimodal benchmarks pending"
labels:
  - multimodal
  - china
  - deepseek
  - released
verification: partial
sources:
  - "@PKUCXK"
  - "@ns123abc"
created_at: 2026-06-18
updated_at: 2026-06-18
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-18
    change: "Created — DeepSeek shipped Vision (image understanding) for V4: researcher @PKUCXK announced 'Vision is now live on web and app' (2026-06-18), a capability turn-on for the existing V4 line. Live + widely relayed → status released; announced from a team member's personal account (not official @deepseek_ai / model card) with no independent benchmarks → verification partial. API/open-weights reach and quality vs. frontier multimodal models still open."
---

On **2026-06-18**, **DeepSeek** turned on **image understanding for its
V4 model**. DeepSeek researcher **Xiaokang Chen (@PKUCXK)** announced on
his own account: "**Vision is now live on web and app.**" This is a
**capability turn-on for the existing V4 line**, not a new base-model
release.

**Why `released` / `partial`.** The feature is **live now** on DeepSeek's
web and app and was **widely relayed**, so the lifecycle is `released`.
But the announcement comes from a **team member's personal account** —
not the official **@deepseek_ai** handle or a model card — and **no
independent multimodal benchmarks** exist yet, so `verification: partial`.
Aggregator "BREAKING: DEEPSEEK DROPPED V4 VISION" framings overstate a
feature flip into a new flagship.

**Context.** Caps a strong week for Chinese open/efficient models —
DeepSeek's ~$7.4B raise ([[deepseek-funding-round-2026-05]]), Microsoft's
reported Cowork evaluation of DeepSeek V4
([[microsoft-copilot-cowork-2026-06]]), and GLM-5.2's MIT release
([[zhipu-glm-5-2]]) — all positioned as the shutdown-proof alternative
while US frontier models sit export-embargoed
([[anthropic-fable-mythos-export-control-2026-06]]).

**Transition triggers:**
- An official @deepseek_ai post / model card, or API + open-weights
  rollout → UPDATE, advance `verification` to `confirmed`.
- Independent vision benchmarks vs. Gemini/GPT/Claude → UPDATE.
- A successor (V4.1 / V5 multimodal) → new ticket; do not reopen this one.
- ≥4 weeks past release, settled into normal coverage →
  `closed: released-and-aged`.

**Dedup note:** further DeepSeek V4 Vision signal UPDATES this ticket; the
funding round and V4-Pro price cut stay on their own tickets
([[deepseek-funding-round-2026-05]], [[deepseek-v4-pro-price-cut-2026-05]]).
