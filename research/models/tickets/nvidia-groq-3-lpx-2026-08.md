---
slug: nvidia-groq-3-lpx-2026-08
title: NVIDIA Groq 3 LPX inference accelerator enters full production
company: NVIDIA / Groq
model: null
status: released
status_note: |
  **NVIDIA says Groq 3 LPX — its low-latency inference accelerator
  designed to extend Vera Rubin NVL72 — is now in full production**
  (@wallstengine, relayed by @jukan05 2026-08-24 15:21 UTC;
  independently carried by @AlphaWireNewsAi, which frames it as "the
  commercial rollout of technology acquired through the company's
  largest-ever acquisition").

  **The performance figure given:** in Artificial Analysis testing,
  Groq 3 LPX reached **3,400 output tokens/sec running Gemma 4 31B at a
  100K-token context**.

  **Groq itself is a launch customer.** @GroqInc (RT'd by founder
  @JonathanRoss321, 2026-08-24 15:45 UTC): "Groq will be among the first
  adopters of **NVIDIA Groq 3 LPX**, deploying it alongside NVIDIA
  Vera Rubin…"

  Status `released`: "full production" plus a named first adopter plus a
  published third-party throughput number is a shipping artifact, not a
  roadmap item. Verification `partial`: **no NVIDIA newsroom post or
  Artificial Analysis page was captured in-window**; the production claim
  and the benchmark both trace to financial-wire relays, and the only
  first-party voice captured is the customer's, not NVIDIA's.

  **Read the name carefully — it encodes an acquisition.** The product is
  branded *NVIDIA Groq 3 LPX* and the relay ties it to NVIDIA's
  largest-ever acquisition, which means the Groq LPU line now ships as
  NVIDIA silicon and Groq the cloud operator is a customer of it. This
  ticket records the product entering production; the acquisition itself
  predates this ticket and is not established here beyond that relay.
expected: "Entered full production per NVIDIA, announced 2026-08-24, with Groq named among the first adopters deploying it alongside Vera Rubin and Nebius reported 2026-08-25 as the first named external adopter. Pending: an NVIDIA first-party post, the Artificial Analysis test page behind the 3,400 tok/s Gemma 4 31B figure, pricing, availability outside launch partners, and how it is positioned against Cerebras CS-4"
labels:
  - nvidia
  - groq
  - inference
  - accelerator
  - vera-rubin
verification: partial
sources:
  - "@jukan05"
  - "@GroqInc"
  - "@JonathanRoss321"
  - "@AlphaWireNewsAi"
  - "@theinformation"
  - "@rohanpaul_ai"
created_at: 2026-08-25
updated_at: 2026-08-26
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-25
    change: "Created — NVIDIA says Groq 3 LPX, a low-latency inference accelerator designed to extend Vera Rubin NVL72, has entered full production (@wallstengine via @jukan05 2026-08-24 15:21 UTC; @AlphaWireNewsAi frames it as the commercial rollout of technology from NVIDIA's largest-ever acquisition). Quoted figure: 3,400 output tok/s on Gemma 4 31B at 100K context in Artificial Analysis testing. @GroqInc, RT'd by founder @JonathanRoss321, says Groq will be among the first adopters, deploying it alongside Vera Rubin. Status released on a full-production claim plus a named first adopter plus a published throughput number; verification partial — no NVIDIA newsroom post or Artificial Analysis page captured, and the only first-party voice is the customer's. Lands two days before NVIDIA's 2026-08-26 earnings, alongside [[nvidia-server-price-increase-2026-08]] and [[nvidia-rubin-ultra-hbm-downgrade-2026-08]]."
  - ts: 2026-08-26
    change: "First named external customer, plus a mechanism-level description of why the part exists. @theinformation's TITV rundown (2026-08-25 16:30 UTC) leads with 'Nebius signs deal to adopt Nvidia Groq chip,' interviewing Nebius CRO Marc Boroditsky - the first adopter outside Groq itself, and it lands the same day Nebius disclosed a $5.75B convertible debt offering explicitly to 'build more data centers, and fill them with more GPU capacity.' The same segment carries a sell-side skeptic on the other side of the question ('Will Nvidia's Groq chip live up to the hype?', @gilluria of D.A. Davidson), so the item is not one-sided promotion. @rohanpaul_ai relays WSJ on the design rationale: 'Agentic AI creates two distinct computing challenges: efficiently processing enormous amounts of context and generating tokens with extremely low latency' - one agent task can require hundreds of sequential inference steps, so decoding delay compounds in a way it does not for ordinary chat. Groq 3 LPX attacks that with deterministic compiler scheduling, 128GB of SRAM across the rack, and preplanned chip-to-chip transfers that reduce small-batch coordination overhead. That is the first architectural detail on this ticket beyond the headline 3,400 tok/s figure, and it explains the positioning against both Vera Rubin (which it extends rather than replaces) and SRAM-heavy rivals like [[cerebras-cs-4-2026-08]]. Status stays released; verification stays partial - still no NVIDIA newsroom post captured, and Nebius's adoption comes via an interview segment rather than either company's own release."
---

**Groq 3 LPX**, NVIDIA's low-latency inference part, is in **full
production**, positioned as an extension to the Vera Rubin NVL72 rather
than a replacement for it.

**The interesting structural fact is the branding.** It ships as *NVIDIA
Groq 3 LPX*, and Groq — the company whose LPU architecture the name comes
from — is a **customer**, publicly committing to deploy it alongside Vera
Rubin. A specialist low-latency architecture that used to compete with
NVIDIA at the token-throughput end is now an NVIDIA SKU that its
originator rents.

**What the throughput number means and does not mean.** 3,400 output
tok/s on **Gemma 4 31B at 100K context** is a genuinely high figure, but
it is a small-dense-model, long-context decode result. It says the part is
built for interactivity — high tokens per second per user — not for
aggregate frontier-model serving. @teortaxesTex's observation the same day
is the relevant frame: labs do not serve users at 100+ tok/s today, and
"people will pay 2x for 3x speed in a heartbeat" if the model is cheap
enough. That is the market this silicon addresses.

**It also lands into a contested week for NVIDIA.** Rubin Ultra's HBM
content was reported cut to a fifth of the original preview
([[nvidia-rubin-ultra-hbm-downgrade-2026-08]]), server prices are reported
up 15-17% on memory inflation
([[nvidia-server-price-increase-2026-08]]), the stock ran a
seven-session losing streak into the **2026-08-26** earnings call, and the
SpaceX Starmind rack partnership
([[spacex-nvidia-starmind-orbital-compute-2026-08]]) was announced the
same day. Read together, these are a supply-constrained vendor
diversifying its product line away from HBM-hungry parts.

**Verification caveat worth keeping.** Everything here except Groq's own
adoption post came through financial wires. The NVIDIA first-party
announcement and the Artificial Analysis test page are the two documents
that would move this to `confirmed` verification.

Related: [[cerebras-cs-4-2026-08]] (the other fast-inference accelerator
on this board), [[groq-funding-2026-06]], [[nvidia-gtc-taipei-2026-06]].
