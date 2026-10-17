---
slug: meta-muse-spark-open-2026-10
title: "Meta releases Muse Spark Open — 816B-total / 42B-active open-weight model for coding and agents"
company: "Meta (Meta Superintelligence Labs)"
model: "Muse Spark Open"
status: released
status_note: |
  **2026-10-17 — verification confirmed.** @alexandr_wang names the Muse Spark Open launch on
  his own handle (2026-10-16 23:26 UTC), and @ArtificialAnlys, which had pre-release access,
  scores it 39 on its Intelligence Index: #1 among US open-weights models, 40K output
  tokens per task, 24% AA-Omniscience hallucination rate.

  **Reported launched 2026-10-16, several independent relays.** @ithertz (11:29 UTC):
  "Meta says its new open-weight AI model, Muse Spark Open, can run on your desk:
  816B total / 42B active parameters, a 1M-token context window, built for coding and
  agentic work. Weights on Hugging Face and major clouds; runs locally via MLX on two
  M5 Ultra Mac Studios." @Shadowfetch adds that Meta's AI chief calls it "the most
  capable U.S. open-weight model to date". @pricepertoken and @BT_Bazaar (Business
  Today) report the launch, and one of them says Meta claims it rivals or beats leading
  Chinese developers' open models.

  **Not adopted:** @lionofkurdistan says it was "developed in partnership with Apple".
  That comes from a single source and is hedged with "reportedly". The MLX / Mac Studio
  local-run path is consistent with Apple involvement but does not prove it.

  **Why `partial`.** No @AIatMeta post or Hugging Face model card was captured in this
  window (a direct HF check was not possible from this runner). The launch is
  corroborated by several unrelated outlets that agree on name and parameter counts.
expected: "Released 2026-10-16 (weights on Hugging Face and major clouds). Confirmed by MSL chief @alexandr_wang and pre-release benchmarking by Artificial Analysis. Open: license terms and the reported Apple partnership."
labels:
  - meta
  - open-weights
  - moe
  - coding
  - agents
  - released
verification: confirmed
sources:
  - "https://x.com/alexandr_wang/status/2111237499083252185"
  - "https://x.com/ArtificialAnlys/status/2110893784422908225"
  - "https://x.com/Mekarly/status/2111407881585136042"
  - "https://x.com/AlchemyJ_io/status/2111389252848386136"
  - "https://x.com/ithertz/status/2111056829186711775"
  - "https://x.com/Shadowfetch/status/2111058872391684523"
  - "https://x.com/pricepertoken/status/2111053531499164155"
  - "https://x.com/BT_Bazaar/status/2111057704072741231"
  - "https://x.com/lionofkurdistan/status/2111021350060019917"
created_at: 2026-10-16
updated_at: 2026-10-17
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-16
    change: "Created — RELEASED / partial. Multiple independent relays on 2026-10-16 report Meta launched Muse Spark Open, an open-weight model for coding and agentic work: 816B total / 42B active parameters, 1M-token context, weights on Hugging Face and major clouds, local inference via MLX on two M5 Ultra Mac Studios (@ithertz). Meta's AI chief reportedly calls it the most capable U.S. open-weight model to date (@Shadowfetch), and coverage says Meta claims parity with or wins over leading Chinese open models (@pricepertoken, @BT_Bazaar). A single-source claim of an Apple co-development partnership (@lionofkurdistan, 'reportedly') is logged, not adopted. No @AIatMeta post or model card captured, so verification is partial. This fulfils Meta's 2026-10-12 statement that open weights were coming for Muse Spark rather than Muse Wonder ([[meta-watermelon-2026-10]]). It is a new artifact, distinct from the closed [[meta-muse-spark-1-4-2026-09]] and [[meta-hatch-muse-spark-2026-06]], which are untouched. Hardware context: [[apple-m5-ultra-mac-studio-2026-08]]."
  - ts: 2026-10-17
    change: "Released, unchanged; verification partial -> confirmed. Two primary-grade sources. (1) MSL chief @alexandr_wang (2026-10-16 23:26 UTC), on his own handle, thanks the team after 'an exciting week of launches (muse wonder [full] & muse spark open)' and calls the open release 'thoughtfully open-sourcing strong models'. (2) @ArtificialAnlys (2026-10-16 00:41 UTC, quoted by @Mekarly) says Meta shared pre-release access and scores Muse Spark Open (xhigh) 39 on its Intelligence Index, the #1 US open-weights model. That is ahead of NVIDIA's Nemotron 3.5 Super VL (26, [[nvidia-nemotron-3-5-super-vl-2026-10]]), within a point of Muse Spark 1.2 (xhigh, 40), and behind Muse Wonder (52) and Muse Wonder Full (56). It uses 40K output tokens per task, the fewest of the top nine open-weights models, and has a 24% AA-Omniscience hallucination rate. Hosting is reported at Together AI and Fireworks, among others. A single-source report that Meta 'teamed up with Apple to run Muse locally on the Mac' (@AlchemyJ_io) is still logged, not adopted."
---

When Meta launched the closed Muse Wonder on 2026-10-12, it said open weights would
come for Muse Spark instead ([[meta-watermelon-2026-10]]). Muse Spark Open is that
release: Meta keeps an open tier while the frontier stays API-only.

The size matters. At 816B total parameters, "runs on your desk" means two top-end
Mac Studios with about 1TB of unified memory, not a consumer GPU. The 42B active
count is what makes local inference fast enough to be practical.

Earlier Muse Spark tickets are closed: [[meta-hatch-muse-spark-2026-06]],
[[meta-muse-spark-1-4-2026-09]].

**Transition triggers:** an @AIatMeta post, model card or license → verification
`confirmed`. A primary statement on the Apple partnership → UPDATE.
