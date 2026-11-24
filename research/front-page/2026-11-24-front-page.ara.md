---
title: "THE AGI AWARENESS POST"
kicker: "Your Daily Artificial Intelligence Briefing"
date: "November 24, 2026"
edition: "All Sources Edition"
volume: "2026"
number: "328"
deck: "An interactive newspaper edition generated from the daily AI digest."
---

:::paper-index
- label: "Lead"
  target: "#lead-top-story"
- label: "Stories"
  target: "#briefs-stories"
- label: "Signals"
  target: "#meter-signal-mix"
:::

:::lead(id="lead-top-story", label="Top Story", title="Anthropic quietly posted an AI-authored VP ≠ VNP proof")
a 70-page paper, credited only to an unspecified "internal research Claude model," plus a Lean 4 formalization appeared in Anthropic's formal-math repo with no announcement. The README says no human mathematician has checked it yet (Twitter: @AndrewCurran, @MTSlive).

OpenAI and Cisco open-sourced the Shirudo exploit-shield runtime: in Shirudo, AI agents write and deploy eBPF "shields" that block exploits on running Linux systems before a patch lands. Hours later OpenAI said GPT-6 Cyber helped validate 948 kernel bugs that grant local root in a single run (Twitter: @OpenAI; The Register).

Anthropic launched Claude Ship for pull requests: a new /ship command lets Claude review PRs, fix failing checks, and approve changes when the repo's policy file allows it. It was the most-liked AI post of the cycle (Twitter: @ClaudeDevs).

NVIDIA's board reinstated Jensen Huang as CEO: he returns on Nov 23, 11 days after his forced resignation. Hard Fork and The AI Daily Brief both frame the White House as wanting him back (Twitter: @AndrewCurran; Podcasts).
:::

:::briefs(id="briefs-stories", title="Stories", columns=2)
- headline: "The VP ≠ VNP claim is unverified beyond Lean"
  tag: "Breaking"
- headline: "It is the repo's third machine-proved headline result"
  tag: "Breaking"
- headline: "GPT-6 Cyber's 948-bug figure is OpenAI's own count"
  tag: "Breaking"
- headline: "GLM-5.4 claims 2–3T-class quality from looped layers"
  tag: "Models"
- headline: "Gemini 4 Neon reached Google Workspace"
  tag: "Models"
- headline: "Claude Code desktop got a tabbed side panel"
  tag: "Models"
- headline: "Claude Ship's three parts have different maturity: Code Review is generally available"
  tag: "Models"
- headline: "Washington's hand in Huang's return is the story"
  tag: "Policy"
- headline: "ChinaTalk made the case for an \"Agentic State\""
  tag: "Policy"
- headline: "Consulting is not a thin wrapper, Normal Tech argues"
  tag: "Policy"
:::

:::news-meter(id="meter-signal-mix", title="Signal Mix")
- label: "Breaking news"
  value: 75
  display: "3 items"
  tone: hot
- label: "Model releases"
  value: 100
  display: "4 items"
  tone: watch
- label: "Research highlights"
  value: 80
  display: "4 items"
  tone: research
- label: "Funding and compute"
  value: 100
  display: "4 items"
  tone: market
:::

:::quote(label="Quote of the Day")
Claude can "review your pull requests, work on fixes, and approve the ones your team's policy allows." — @ClaudeDevs, announcing Claude Ship (X)
:::
