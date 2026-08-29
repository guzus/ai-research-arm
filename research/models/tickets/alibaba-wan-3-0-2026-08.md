---
slug: alibaba-wan-3-0-2026-08
title: Wan 3.0 video model surfaces in the wild, priced on third-party hosts
company: Alibaba (Tongyi Wan line)
model: Wan 3.0
status: released
status_note: |
  **Two independent kinds of evidence appeared inside 24h.**

  *Capability:* @mark_k (2026-08-24 09:07 UTC, ~50 likes) — "**WAN 3.0
  generated this 30-second video in one take!** Looks like we might have a
  new king of video models. This could actually **challenge SeeDance
  2.5**." A 30-second single-take generation is the specific, checkable
  claim; it is the axis [[bytedance-seedance-2-5-2026-07]] was built to
  win on (native 30s single-shot).

  *Commercial availability:* @Hailey4AI and @Flovaai (2026-08-25 ~07:01
  UTC) — "**FlovaAI × Wan 3.0 is officially live**… Wan 3.0 in **480p**
  with high quality video generation starting from just **$0.013/sec**,"
  with audio/video sync and rhythm transitions cited. A third-party host
  quoting per-second pricing means the weights or an API exist and are
  being resold.

  Status `released` — a model that a commercial host is serving at a
  posted price is publicly available, whatever its announcement state.
  Verification `partial`, and the gap is specific: **no Alibaba /
  Tongyi / Wan first-party post, model card, weights link or benchmark was
  captured in-window.** The company attribution rests on Wan being
  Alibaba's Tongyi video line, not on any in-window statement — treat the
  vendor as inferred until a first-party post lands.

  **What is NOT established:** resolution ceiling (the only priced tier
  captured is 480p), duration limits beyond the single 30s demo, licence
  terms, whether weights are open, and any head-to-head benchmark against
  Seedance 2.5 or Veo. "New king of video models" is one enthusiast's
  read of one clip and is recorded as such, not as a ranking.
expected: "Live on at least one commercial host (FlovaAI) at $0.013/sec for 480p as of 2026-08-25, with a 30-second single-take demo circulating. Pending: an Alibaba/Tongyi first-party announcement, model card and weights status, higher-resolution tiers and their pricing, licence terms, and a measured comparison against Seedance 2.5"
labels:
  - alibaba
  - wan
  - video-generation
  - released
verification: partial
sources:
  - "@mark_k"
  - "@Hailey4AI"
  - "@Flovaai"
  - "@0xm4sud"
created_at: 2026-08-25
updated_at: 2026-08-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-25
    change: "Created — Wan 3.0 appeared with two independent kinds of evidence in one window: @mark_k (2026-08-24 09:07 UTC) posted a 30-second single-take generation and called it a challenger to Seedance 2.5, and @Flovaai / @Hailey4AI announced FlovaAI is serving Wan 3.0 live at $0.013/sec for 480p with audio-video sync. Status released — a commercial host serving it at a posted price makes it publicly available. Verification partial and the gap is named: no Alibaba/Tongyi first-party post, model card, weights link or benchmark was captured, so the Alibaba attribution is inferred from the Wan line's provenance rather than established in-window. Resolution ceiling, duration limits, licence and open-weights status are all unknown; the 'new king of video models' framing is one tester's read of one clip and is not recorded as a ranking. Directly competitive with [[bytedance-seedance-2-5-2026-07]]."
---

**Wan 3.0** is being served commercially and generating 30-second
single-take video, without any first-party announcement having been
captured.

**The two datapoints are unusually complementary.** An enthusiast demo
alone would be a rumor; a reseller price sheet alone would be a listing.
Together — a working 30s generation *and* a host charging $0.013/sec —
they establish that a real artifact exists and is in commercial
distribution. That is enough for `released`; it is not enough to say who
shipped it or under what licence.

**Why the 30-second single take is the number that matters.** Seedance
2.5's headline capability was native 30s single-shot generation with
consistency ([[bytedance-seedance-2-5-2026-07]]). If Wan 3.0 matches that,
the frontier of open/Chinese video generation has two entrants at the same
duration inside a month, and duration stops being the differentiator —
which pushes the competition toward consistency, controllability and
cost. At $0.013/sec for 480p, cost is where Wan 3.0 is currently
arguing.

**The attribution caveat is load-bearing and should not be quietly
dropped.** Nothing captured in-window says "Alibaba." Wan is Alibaba's
Tongyi video line, which is why this ticket carries that company, but a
first-party post is what would confirm it — and would also settle whether
this is an open-weights release, which is the single fact that most
changes its significance.

**The signal source is also weak in a specific way.** The pricing posts
come from a host promoting a limited-time launch offer; promotional
accounts overstate. The independent check is @mark_k's separate,
non-commercial demo, which is why both are recorded rather than either
alone.

Related: [[bytedance-seedance-2-5-2026-07]],
[[alibaba-qwen-image-3-2026-07]], [[google-lyria-3-5-2026-07]],
[[xai-grok-imagine-video-1-5-2026-06]].
