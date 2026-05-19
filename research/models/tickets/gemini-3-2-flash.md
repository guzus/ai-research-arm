---
slug: gemini-3-2-flash
title: Gemini 3.2 Flash — Google I/O 2026 reveal
company: Google / DeepMind
model: Gemini 3.2 Flash
status: in-testing
status_note: |
  GCP Cloud Console artifact (Gemini 3.2 Flash-lite-live, 2026-05-16) — strong
  signal that the I/O reveal will be the 3.2 series rather than the previously
  rumored 3.5. iOS app + AI Studio leak May 5 already showed Gemini 3.2 Flash
  priced $0.25 / $2.00 per MTok with "Liquid Glass" iOS redesign + Agents (Beta).
expected: 2026-05-19 / 2026-05-20 (Google I/O keynote, 10am PT)
labels:
  - google-io
  - flash-tier
  - leaked-pricing
verification: partial
sources:
  - https://byteiota.com/gemini-3-2-flash-leaked-what-developers-need-to-know-before-i-o/
  - https://pasqualepillitteri.it/en/news/2013/gemini-3-2-flash-leak-ios-ai-studio-2026-en
  - https://www.androidauthority.com/what-to-expect-from-google-io-2026-3664979/
  - "@AiBattle_"
  - "@testingcatalog"
  - "@mark_k"
  - "@deployedmind"
  - "@kimmonismus"
created_at: 2026-05-05
updated_at: 2026-05-16
closed_at: null
closed_reason: null
history:
  - ts: 2026-05-05
    change: Created — Gemini 3.2 Flash spotted in iOS app + AI Studio with pricing ($0.25 / $2.00 per MTok)
  - ts: 2026-05-14
    change: "Alex Heath frames Google I/O reveal as \"in the class of GPT-5.5, well short of Mythos\""
  - ts: 2026-05-15
    change: mark_k floats "Gemini 3.5 Flash / Pro" as the I/O reveal — tier still ambiguous
  - ts: 2026-05-16
    change: GCP Cloud Console find (AiBattle_, testingcatalog) — "Gemini 3.2 Flash-lite-live" listed alongside the existing 3.2 Flash leak; reframes I/O reveal as the 3.2 series rather than 3.5
  - ts: 2026-05-16
    change: "Material framing: if Google ships 3.2 (not 3.5/4) at I/O, the gap-vs-GPT-5.5/Mythos narrative widens"
---

Three days before Google I/O 2026, the leak picture is now consistent:
Google is shipping the **Gemini 3.2 series**, not the previously rumored
3.5. Evidence:

- **iOS + AI Studio (May 5)**: Gemini 3.2 Flash with concrete pricing
  ($0.25 / $2.00 per MTok), outperforming 3.1 Pro on creative coding
  (ASCII animation benchmark), shipped with "Liquid Glass" iOS redesign
  and an Agents (Beta) tab.
- **GCP Cloud Console (May 16)**: Gemini 3.2 Flash-lite-live traces
  appear in the Cloud Console — same path Opus 4.7 took before its
  public release. AiBattle_ flagged this first; testingcatalog
  corroborated 18 minutes later.

Alex Heath's framing — Mythos has reset what "leading" means, and the
Google reveal "lands in the class of GPT-5.5, well short of Mythos" —
is the controlling narrative. A 3.2 ship (rather than 3.5) widens the
perceived gap to Mythos and re-frames the Gemini roadmap as iterative
rather than leapfrogging.

**Why this ticket exists separately from a "Gemini 3.5" ticket:** the
3.5 expectation was an unresolved rumor that the May 16 GCP find now
disproves. If a `gemini-3-5-pro` ticket existed earlier, it should
close with `closed_reason: superseded-by:gemini-3-2-flash`.

**Transition triggers:**
- I/O reveal happens (May 19-20) → `status: confirmed` with the official
  spec, plus history entry capturing what shipped vs. what leaked.
- Public rollout (Vertex AI GA, Gemini app, AI Studio default) →
  `status: released`.
- ≥4 weeks past public release → `status: closed` with
  `closed_reason: released-and-aged`.
