---
slug: gemini-3-2-flash
title: Gemini 3.5 Flash — Google I/O 2026 release
company: Google / DeepMind
model: Gemini 3.5 Flash
status: released
status_note: |
  Revealed and shipped GA at Google I/O 2026 (2026-05-19) as **Gemini 3.5
  Flash** — not the leaked "3.2 Flash". The pre-I/O GCP console artifact
  ("Gemini 3.2 Flash-lite-live") was an internal codename; Google branded
  the public release 3.5. Live everywhere now: Gemini app, AI Mode in
  Search (new default), Antigravity, Gemini API, and AI Studio. Reported
  pricing $1.50 / $9.00 per MTok (secondary); ~4x faster than comparable
  frontier models (12x / ~800 tok/s inside Antigravity) and beats Gemini
  3.1 Pro on coding + agentic tasks. Gemini 3.5 Pro confirmed for next
  month — see gemini-3-5-pro. Post-launch (2026-05-21): Antigravity 3x'd
  Gemini rate limits across all paid tiers and reset weekly quotas after
  users hit limits fast; 3.5 Flash ranks #1 on Zapier's Automation Bench.
expected: null
labels:
  - google-io
  - flash-tier
  - released
  - frontier-model
verification: confirmed
sources:
  - https://byteiota.com/gemini-3-2-flash-leaked-what-developers-need-to-know-before-i-o/
  - https://pasqualepillitteri.it/en/news/2013/gemini-3-2-flash-leak-ios-ai-studio-2026-en
  - https://www.androidauthority.com/what-to-expect-from-google-io-2026-3664979/
  - "@GoogleDeepMind"
  - "@OfficialLoganK"
  - "@demishassabis"
  - "@AiBattle_"
  - "@testingcatalog"
  - "@mark_k"
  - "@kimmonismus"
  - "@_mohansolo"
created_at: 2026-05-05
updated_at: 2026-05-21
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
  - ts: 2026-05-19
    change: "Google I/O reveal — shipped as **Gemini 3.5 Flash** (not the leaked 3.2), GA the same day across the Gemini app, AI Mode in Search, Antigravity, and the Gemini API (official @GoogleDeepMind)"
  - ts: 2026-05-20
    change: "status → released. Demis Hassabis: 4x faster than comparable frontier models (12x / ~800 tok/s in Antigravity), beats Gemini 3.1 Pro on coding + agentic; reported pricing $1.50 / $9.00 per MTok (secondary). Gemini 3.5 Pro confirmed for next month (new ticket gemini-3-5-pro)"
  - ts: 2026-05-21
    change: "Post-launch momentum: Antigravity 3x'd Gemini rate limits across all paid tiers + reset weekly quotas after users hit limits fast (@_mohansolo / @OfficialLoganK); 3.5 Flash ranks #1 on Zapier's Automation Bench, beating other frontier models at lower cost; \"Gemini 3.5 Flash has landed\" (official @GoogleDeepMind)"
---

Google I/O 2026 (2026-05-19) resolved this ticket: the Flash-tier reveal
shipped publicly as **Gemini 3.5 Flash**, not the "Gemini 3.2 Flash" that
the iOS/AI-Studio and GCP-console leaks had pointed to. The slug stays
`gemini-3-2-flash` (slugs are immutable) even though the title now tracks
the 3.5 branding — this is the version-number drift the ticket schema
anticipates.

**What shipped (official @GoogleDeepMind, @OfficialLoganK, @demishassabis):**

- **Gemini 3.5 Flash**, the first release of the new Gemini 3.5 family
  ("frontier intelligence + real-world action"). Generally available the
  same day across the Gemini app, AI Mode in Google Search (new global
  default model), Antigravity, the Gemini API, and AI Studio.
- Demis Hassabis: better than Gemini 3.1 Pro on coding and agentic tasks,
  4x faster than comparable frontier models (12x and ~800 tok/s inside
  Antigravity), "often at less than half the cost."
- Reported pricing **$1.50 / $9.00 per MTok** (secondary report, not the
  official blog) — materially higher than the $0.25 / $2.00 the earlier
  "3.2 Flash" leak quoted, so the "cheap Flash" framing no longer holds.

**Why the leak was off on the version:** the GCP console artifact
("3.2 Flash-lite-live") and the iOS leak both used a "3.2" label that
turned out to be an internal codename. Google's public branding is 3.5,
which also re-validates the earlier "Gemini 3.5" rumors that the May 16
GCP find had appeared to disprove.

**Related tickets:**
- [gemini-3-5-pro](./gemini-3-5-pro.md) — the Pro tier of the 3.5 family,
  officially confirmed at I/O for "next month."
- [gemini-omni](./gemini-omni.md) — the multimodal video model launched
  alongside Flash.
- The "GCP-console-before-release" detection pattern is documented on
  [opus-4-7](./opus-4-7.md) and [mythos](./mythos-public-release.md).

**Transition triggers:**
- ≥4 weeks past public release (after ~2026-06-16) → `status: closed`
  with `closed_reason: released-and-aged`.
