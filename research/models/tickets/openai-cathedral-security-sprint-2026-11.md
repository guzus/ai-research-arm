---
slug: openai-cathedral-security-sprint-2026-11
title: "OpenAI partners with Cathedral Systems for its next internal security sprint and raises bug bounties up to $172K"
company: OpenAI / Cathedral Systems
model: null
status: confirmed
status_note: |
  **First-party, 2026-11-03 02:29 UTC (@OpenAI):** "We're planning our next internal security sprint
  at OpenAI and partnering with Cathedral Systems, whose researchers will use our models alongside
  our teams to challenge our defenses." OpenAI is also raising bug bounty rewards, "including more
  than quadrupling rewards for critical findings". Exceptional findings can earn up to $172,000
  including bonuses. The new ranges apply to reports awaiting a bounty, and OpenAI will pay the
  difference on bounties awarded in the past 30 days.

  **Secondary, quoting the announcement page (@SteveAIStudio):** the previous sprint put 25% of
  product engineers on finding and fixing weaknesses using Codex. OpenAI is also offering $1B in
  subsidized access over six months to frontline defenders of essential services.

  The sprint is planned, not completed. Its date and scope are not stated.
expected: "Bounty increase effective now (announced 2026-11-03). Sprint date not given. Open: Cathedral Systems' role and findings, and any public sprint report."
labels:
  - security
  - partnership
  - bug-bounty
  - openai
verification: confirmed
sources:
  - "https://x.com/OpenAI/status/2117444048227123277"
  - "https://x.com/OpenAI/status/2117444049900654743"
  - "https://x.com/SteveAIStudio/status/2117623501997932686"
created_at: 2026-11-03
updated_at: 2026-11-03
closed_at: null
closed_reason: null
history:
  - ts: 2026-11-03
    change: "Created — CONFIRMED / confirmed. @OpenAI (2026-11-03 02:29 UTC) announced that its next internal security sprint will partner with Cathedral Systems, whose researchers will use OpenAI's models to challenge its defenses. It also raised bug bounty rewards, more than quadrupling critical-finding payouts, with up to $172,000 for exceptional findings. The new ranges apply to pending reports and are applied retroactively to bounties from the past 30 days. Secondary (@SteveAIStudio, quoting the announcement page): the last sprint put 25% of product engineers on security work using Codex, and OpenAI offers $1B in subsidized access over six months to frontline defenders."
---

This is OpenAI's response to its own capability findings. Models that find vulnerabilities well can
be used by attackers too, so OpenAI wants defenders using them first. The earlier incidents tracked at
[[openai-agent-government-intrusions-2026-09]] and [[openai-unreleased-containment-escape-2026-07]]
are the context.

The partner name matters for another ticket. [[anthropic-slack-breach-2026-10]] tracks a claim that
"cathedral" gained admin access to Anthropic's Slack. If that refers to Cathedral Systems, the claim
may describe a red-team engagement rather than a hostile breach. Nothing in signal confirms that link.

**Transition triggers:** a published sprint report or Cathedral Systems disclosure → history update;
the bounty change is a one-time event, so close as superseded or aged once no follow-up arrives.
