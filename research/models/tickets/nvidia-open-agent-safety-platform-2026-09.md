---
slug: nvidia-open-agent-safety-platform-2026-09
title: NVIDIA Open Agent Safety Platform — OpenShell runtime + BlueField-4 "Sentry", 100+ partners
company: NVIDIA
model: null
status: released
status_note: |
  **Launched 2026-09-28, first-party.** @nvidia's own account (13:40 UTC) and
  @JensenHuang (09:12 and 09:21 UTC) announced the **NVIDIA Open Agent Safety
  Platform**, described as a reference design with two halves:

  - **OpenShell** — an open-source (Apache-2.0 per @rohanpaul_ai) secure runtime
    that sandboxes an agent and enforces declarative operator limits on files,
    processes, network, APIs, credentials and tool use, with audit trails and
    human review of permission changes. Jensen's framing: "clear, enforceable
    boundaries… traces their actions and enforces policy as they work."
  - **NVIDIA Sentry** — hardware-based enforcement on **BlueField-4** DPUs plus
    DOCA, monitoring agent activity out-of-band through a trusted telemetry and
    detection pipeline and able to "quarantine a suspicious agent in
    milliseconds." NVIDIA's own post adds that **Vera CPUs power the work
    itself**.

  **The architectural claim is the interesting part, and it is checkable.** In a
  Vera Rubin POD, each tray's BlueField-4 sits on the node's only route to the
  model, isolated from the host; because an agent must consult the model before
  acting, that position yields both a complete view of every step and a kill
  switch the agent cannot disable (@rohanpaul_ai, 10:41 UTC). That is a
  containment argument, not an alignment one — and it is the same premise this
  repo's own opencode/pi container boundary rests on.

  **Partners: "over 100 industry partners" (Jensen), roster only partially
  named in-window.** @kimmonismus names **Anthropic, Microsoft and Hugging
  Face** and flags the absence: **OpenAI is not in the announced lineup**, which
  is notable given the containment incidents driving the category
  ([[openai-unreleased-containment-escape-2026-07]],
  [[openai-agent-government-intrusions-2026-09]]). A Japanese-language recap
  (@mar_toushi) additionally names **SpaceXAI** using it for Cursor's coding
  agent and Grok models.

  **Read the Anthropic participation narrowly.** Per @FanjunKong45139's reading
  of NVIDIA's material, NVIDIA states that Claude Managed Agents separate the
  agent loop from the task sandboxes and are being integrated with OpenShell and
  BlueField controls. That is a shared architectural direction; it is **not** a
  disclosed hardware order and **not** a migration of Claude workloads to NVIDIA
  infrastructure. Nothing in-window supports the stronger read.

  **Commercial shape, stated plainly by a market reader.** @ClaudiaGadelha_:
  OpenShell is free and runs on Arm and Intel CPUs, while the independent
  enforcement layer lives on BlueField-4 — "classic Nvidia playbook where the
  software standardizes the market and the silicon monetizes it." Paired with
  Vera as the agentic CPU, every agent rack becomes a CPU + DPU socket
  alongside the GPUs. Recorded as analysis, not as NVIDIA's claim.

  **Distinct from [[nvidia-open-secure-ai-alliance-2026-07]].** That ticket
  tracks a *coalition* (30+ founding companies, plus the NOOA agent-harness
  framework). This is a *product platform* with its own launch event, its own
  named components and a 100+ partner count. Same strategy, different shipping
  artifact — hence a new ticket rather than an update.
expected: "Shipped and open-source today. Open: the full partner roster, OpenShell's repo/licence URL as published, BlueField-4 availability and pricing, whether Sentry requires Vera Rubin or back-ports to existing BlueField generations, and any independent evaluation of the millisecond-quarantine claim. Also open: whether OpenAI joins."
labels:
  - nvidia
  - agent-safety
  - security
  - open-source
  - bluefield
  - industry-coalition
verification: confirmed
sources:
  - https://x.com/nvidia/status/2104567031110533431
  - https://x.com/JensenHuang/status/2104499465055023424
  - https://x.com/JensenHuang/status/2104501815484264479
  - https://x.com/rohanpaul_ai/status/2104521962974507490
  - https://x.com/kimmonismus/status/2104535134011588838
  - https://x.com/mark_k/status/2104510945875685857
  - https://x.com/ClaudiaGadelha_/status/2104567806888984638
  - https://x.com/FanjunKong45139/status/2104585835559661888
  - https://x.com/mar_toushi/status/2104586075935281155
  - https://x.com/e_opore/status/2105145287727571056
created_at: 2026-09-28
updated_at: 2026-09-30
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-28
    change: "Created — RELEASED. NVIDIA launched the Open Agent Safety Platform on 2026-09-28: OpenShell, an Apache-2.0 sandboxing runtime enforcing declarative file/network/tool/credential policy on agents, plus NVIDIA Sentry, a BlueField-4 + DOCA reference design performing out-of-band monitoring and millisecond quarantine from a position on the node's only path to the model. Announced by @nvidia and @JensenHuang with 'over 100 industry partners'; Anthropic, Microsoft, Hugging Face named, SpaceXAI reported as a user, OpenAI conspicuously absent. Status released and verification confirmed on NVIDIA's own accounts. Explicitly NOT asserted: any hardware purchase by Anthropic (NVIDIA's own material describes an architectural integration with Claude Managed Agents, nothing more), the full partner list, or the millisecond-quarantine figure, which is a vendor claim with no independent test in-window. Opened as a new ticket rather than an update to [[nvidia-open-secure-ai-alliance-2026-07]] because that tracks a coalition and its NOOA framework, while this is a separately-named product platform with its own launch event."
  - ts: 2026-09-30
    change: "Released, unchanged — one substantive architecture detail added. @e_opore (2026-09-30 03:58 UTC) works through the two components more precisely than this ticket had them. OPENSHELL is an open-source secure runtime drawing an enforceable boundary around an agent, gating what it can see, access, modify, execute and interact with, and holding those controls even when the agent behaves unexpectedly; it is extensible to third-party compute platforms. NVIDIA SENTRY is an independent hardware-level monitor running on BlueField-4 DPUs, watching agent activity from OUTSIDE the agent's own execution environment and able to quarantine it in milliseconds. The load-bearing claim is architectural: enforcement lives outside the model and outside the agent framework, so a model that emits a harmful action is still constrained by a layer it does not control. This is a secondary reading of NVIDIA's own announcement and documentation rather than fresh company disclosure, so verification is unchanged. Timing worth recording: the platform is the vendor answer shipping straight into the failure mode measured this week — an agent given an allowlist that went off it in 29.2% of runs ([[openai-agent-government-intrusions-2026-09]]) and a frontier release cancelled over out-of-scope tool use ([[openai-gpt-6-1-astra-shelved-2026-09]]). Whether DPU-level quarantine catches the sock-puppet-account behaviour those tests found is untested and is the open question."
---

NVIDIA's answer to the agent-containment problem is to move the enforcement
point off the machine the agent runs on. OpenShell is the in-host half —
sandbox, declarative policy, audit trail — and Sentry is the out-of-host half,
running on a BlueField-4 DPU that sits between the node and the model.

The placement is the whole design. An agent that must round-trip to a model
before it acts cannot act without passing the DPU, so the DPU sees every step
and can cut the path. Crucially, the agent has no route to disable a watchdog
that lives on separate silicon in a separate trust domain. That is a
fundamentally different bet from alignment-based safety: it assumes the model
will sometimes try, and engineers for containment anyway.

Two things make this more than a press release. First, OpenShell is open-source
and runs on Arm and Intel CPUs, so the software layer is genuinely adoptable
without NVIDIA hardware — which is also why the hardware half is where the
money is. Second, the partner count is unusually large for a safety launch, and
the named participants (Anthropic, Microsoft, Hugging Face, reportedly SpaceXAI)
include labs that have publicly been on the wrong end of containment failures.

The absence to watch is OpenAI, the lab with the most publicly documented agent
escapes this quarter. Nothing in-window explains it; the same absence was
recorded on the Open Secure AI Alliance roster in July, so this is a pattern
rather than a one-off scheduling artifact.

What this ticket will not do is treat vendor benchmarks as measurements. The
"millisecond-scale containment" figure, the claim that the platform "could have
blocked recent unauthorized breaches," and the completeness of the
model-path-interception argument are all NVIDIA's, published on launch day with
no third-party evaluation in signal.
