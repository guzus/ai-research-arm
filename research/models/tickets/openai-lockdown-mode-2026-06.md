---
slug: openai-lockdown-mode-2026-06
title: OpenAI ships ChatGPT "Lockdown Mode" against prompt-injection data exfiltration
company: OpenAI
model: null
status: released
status_note: |
  OpenAI **unveiled "Lockdown Mode"** for ChatGPT (TechCrunch, 2026-06-06), a
  hardened setting that **reduces the likelihood that sensitive data gets
  exfiltrated via prompt-injection attacks**. OpenAI is explicit that it does
  not fully eliminate prompt-injection risk — the goal is risk reduction. A
  named, announced product feature → released / confirmed.
expected: null
labels:
  - openai
  - security
  - prompt-injection
  - product-feature
  - released
verification: confirmed
sources:
  - https://techcrunch.com/2026/06/06/openai-unveils-lockdown-mode-to-protect-sensitive-data-from-prompt-injection-attacks/
created_at: 2026-06-07
updated_at: 2026-06-07
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-07
    change: "Created — OpenAI unveiled ChatGPT 'Lockdown Mode' (TechCrunch 2026-06-06), a hardened setting to reduce sensitive-data exfiltration from prompt-injection attacks; OpenAI notes it mitigates rather than eliminates the risk. Announced product feature → released / confirmed"
---

OpenAI **unveiled "Lockdown Mode"** for ChatGPT on 2026-06-06 (TechCrunch), a
hardened operating setting designed to **reduce the likelihood that sensitive
data is exfiltrated through prompt-injection attacks**. OpenAI is careful to
note that ChatGPT **could still be vulnerable** even with Lockdown Mode on —
the explicit goal is to **lower the probability** that sensitive data leaks in
the process, not to eliminate prompt injection.

**Why this is a ticket.** It is a concrete, announced **product/security
feature release** from a frontier lab, and it lands amid a cycle of
agentic-security incidents — most prominently the
**Meta AI-chatbot Instagram-account-hijack** breach (MIT Tech Review /
this.weekinsecurity, 2026-06-05/07), which underscored that agentic systems
need exactly this class of trust-boundary hardening.

**Verification.** A named, on-record OpenAI feature reported by primary tech
press → `released` / `confirmed`.

**Transition triggers:**
- Rollout details (availability tiers, enterprise vs consumer, defaults) →
  UPDATE.
- Independent security research evaluating Lockdown Mode's efficacy → UPDATE.
- Feature settles into normal coverage ≥4 weeks post-release → `closed:
  released-and-aged`.

**Dedup note:** further ChatGPT Lockdown Mode / OpenAI prompt-injection-defense
signal UPDATES this ticket.
