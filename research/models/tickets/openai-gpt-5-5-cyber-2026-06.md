---
slug: openai-gpt-5-5-cyber-2026-06
title: OpenAI "Daybreak" — full GPT-5.5-Cyber release + Codex Security + Patch the Planet
company: OpenAI
model: GPT-5.5-Cyber
status: released
status_note: |
  On **2026-06-22** OpenAI expanded its **"Daybreak"** cyber program and
  shipped the **full GPT-5.5-Cyber** model — a permissive, cyber-tuned
  GPT-5.5 variant scoring **85.6% on CyberGym** (vs. 81.8–81.9% for the
  standard/early model) — alongside a **Codex Security** plugin (turning
  Codex into an enterprise app-security platform), a gated **Cyber Partner
  Program**, and **"Patch the Planet"**, an open-source mass-remediation
  push with **Trail of Bits + HackerOne** and 30+ committed projects. Sam
  Altman framed it as putting the strongest cyber AI only in the hands of
  "trusted defenders" — a deliberate counter-posture to Anthropic's Mythos
  "too powerful to ship" stance ([[anthropic-fable-mythos-export-control-2026-06]]).

  **Caveats:** the "beats Mythos on CyberGym" line is OpenAI's own
  single-vendor chart, and the widely-relayed concrete CVE list
  (OpenSSH/GnuTLS/PHP/Chromium) traces to a non-official relay, not OpenAI's
  posts. The model + program ship is primary-sourced (OpenAI index pages);
  the comparative superiority claim is not independently verified.
expected: "Shipped — GPT-5.5-Cyber live via tiered/gated access; Codex Security plugin + Cyber Partner Program + 'Patch the Planet' (Trail of Bits / HackerOne). Cross-vendor benchmark superiority is vendor-self-reported"
labels:
  - openai
  - released
  - cybersecurity
  - gated
verification: confirmed
sources:
  - https://openai.com/index/daybreak-securing-the-world
  - https://openai.com/index/patch-the-planet
  - https://cyberscoop.com/openai-daybreak-gpt-5-5-anthropic-mythos-cybersecurity/
created_at: 2026-06-23
updated_at: 2026-06-23
closed_at: null
closed_reason: null
history:
  - ts: 2026-06-23
    change: "Created — OpenAI 'Daybreak' expansion (2026-06-22): shipped the full GPT-5.5-Cyber model (permissive cyber-tuned GPT-5.5, 85.6% CyberGym vs 81.8–81.9% standard/early), a Codex Security plugin, a gated Cyber Partner Program, and 'Patch the Planet' (open-source mass remediation with Trail of Bits + HackerOne, 30+ projects). Altman frames it as strongest-cyber-AI-for-trusted-defenders-only — a counter-posture to Anthropic's Mythos export saga. Model + program ship primary-sourced (OpenAI index pages) → status released, verification confirmed. Caveat: the 'beats Mythos on CyberGym' line is OpenAI's own single-vendor chart, and the relayed CVE list traces to a non-official source."
---

**OpenAI's "Daybreak"** cyber program got its full release on **2026-06-22**.
The centerpiece is **GPT-5.5-Cyber**, a permissive, cyber-tuned variant of
GPT-5.5 that OpenAI says scores **85.6% on CyberGym** (against 81.8–81.9% for
the standard / early-access model). It ships through **tiered, gated access**
rather than to everyone — explicitly the opposite of an open frontier drop.

**The program around the model.** Alongside the model OpenAI shipped a
**Codex Security** plugin that turns Codex into an enterprise app-security
platform (find / validate / fix vulnerabilities), a gated **Cyber Partner
Program**, and **"Patch the Planet"** — an open-source mass-remediation push
run with **Trail of Bits** and **HackerOne**, with 30+ committed projects.
Sam Altman's framing — strongest cyber AI for "trusted defenders" only — is a
direct rhetorical counter to Anthropic's Mythos "too powerful to ship"
narrative ([[anthropic-fable-mythos-export-control-2026-06]]).

**Why `released` / `confirmed`.** The model and the program are live and
documented on OpenAI's own index pages, so the lifecycle is `released` and
verification `confirmed`. The **comparative** claims are the soft part: the
"beats Mythos on CyberGym" chart is OpenAI's own single-vendor benchmark, and
the much-shared concrete CVE list (OpenSSH/GnuTLS/PHP/Chromium) traces to a
non-official relay, not OpenAI's posts — neither is independently verified.

**Transition triggers:**
- Independent reproduction of the CyberGym / cross-vendor numbers → UPDATE,
  refine verification on the comparative claim.
- A successor cyber model or program rev → new ticket; do not reopen.
- ≥4 weeks past release, settled into normal coverage → `closed: released-and-aged`.

**Dedup note:** further GPT-5.5-Cyber / Daybreak / Codex Security / Patch the
Planet signal UPDATES this ticket. OpenAI's bio-defense line stays on
[[openai-rosalind-biodefense-2026-05]]; the Codex platform stays on
[[openai-codex-platform-2026-05]]; the export order stays on
[[anthropic-fable-mythos-export-control-2026-06]].
</content>
