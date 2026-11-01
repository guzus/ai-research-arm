---
slug: black-october-ai-platform-breaches
title: Black October AI Platform Breaches
type: theme
aliases: ["Black October", "Wiz nine-platform breach list", "Northflank breach", "stolen AI API keys"]
tags: [security, supply-chain, api-keys, inference-infra, agents]
description: Wiz counts nine AI platforms breached in October 2026 (Northflank, Fireworks AI, Railway, Warp, OpenCode, Lightning AI among them), with stolen AI keys resold and two keys alone running up more than $100K of Bedrock calls.
created_at: 2026-11-01
timestamp: 2026-11-01T00:00:00Z
sources:
  - {title: "ARA daily digest 2026-11-01", path: research/digest/2026-11-01-digest.md}
---

**Black October** is the label attached to a cluster of October 2026 breaches at
developer and AI-infrastructure platforms, tallied by Wiz at **nine platforms**.
It is a concrete, metered-cost instance of the supply-chain axis tracked on
[[agentic-ai-security]]: the attack surface is the platform that stores a
developer's AI provider keys, not the model.

## What is reported (2026-11-01)

- **Northflank** told customers to **assume every stored secret was
  decrypted**, and later said users reported unauthorized use of AI API keys.
- Wiz's list names [[fireworks-ai|Fireworks AI]], Railway, Warp, OpenCode and
  Lightning AI among the nine. Zeabur is reportedly shutting down after its
  own incident.
- **Stolen AI keys are being resold.** Wiz traced one key to about **800K
  Bedrock calls in 30 hours** and another to about **1.7M calls in 13 hours**;
  two keys alone ran up more than **$100K** of [[amazon|Amazon]] Bedrock usage.
- Hygiene advice in the digest: rotate keys stored on any named platform, scope
  keys per project, and set provider spend alerts.

## Caveats

The numbers reach the digest through a **single secondhand summary of Wiz's
report** (relayed by @2logics and @AndrewCurran_); the primary Wiz write-up was
not reviewed. Per-platform scope, and whether Fireworks AI customers' keys were
actually used, is not established in the source.

## Why it matters

Agent and coding-tool workflows concentrate long-lived provider credentials in
third-party platforms. Metered inference makes theft immediately expensive, so
key theft is monetized faster than data theft. See [[agentic-ai-security]] for
the wider supply-chain pattern and [[ai-capex]] for the inference-demand
backdrop.
