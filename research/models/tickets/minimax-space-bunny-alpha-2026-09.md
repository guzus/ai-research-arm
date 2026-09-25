---
slug: minimax-space-bunny-alpha-2026-09
title: "\"Space Bunny Alpha\" — anonymous 1M-context coding model on OpenRouter, fingerprinted as a MiniMax M3.1 preview"
company: MiniMax (attribution unconfirmed)
model: Space Bunny Alpha (suspected MiniMax M3.1)
status: in-testing
status_note: |
  **Live anonymous model, 2026-09-24.** @mark_k: "A mystery model just appeared
  on OpenRouter: Space Bunny Alpha. It's free to try, has a 1M-token context
  window, accepts images and video, and is pitched as fast and strong at
  coding. Community fingerprinting points to a MiniMax M3.1 preview
  (@MiniMax_AI), but nobody has officially confirmed who made it."

  **Independent hands-on, next morning.** @mhdfaran (2026-09-25 11:43 UTC) ran
  it inside OpenCode against a FastAPI repo with three failing tests caused by
  broken order filtering, unsafe money calculations and incorrect product
  ranking, without being told where the bugs were: it read the product
  contract, found the root causes, fixed all three, added two edge-case tests,
  and went 3 failing → 6 passing in ~83 seconds touching two files. That is
  weak evidence of quality and strong evidence the endpoint is genuinely
  serving.

  **Attribution is the unconfirmed part, and it is the whole title.** The
  MiniMax M3.1 read is community fingerprinting only. No vendor has claimed it.
  Anonymous-alpha-then-reveal is now a well-worn launch pattern on OpenRouter —
  [[zhipu-glm-5-3-2026-08]] confirmed after the fact that it had been serving
  as "Ox Alpha", and [[stealth-ox-alpha-model-2026-08]] tracked that stealth
  slot while it was live — so the pattern is real and so is the failure mode of
  guessing the wrong lab.

  **Relationship to [[minimax-m3]].** That ticket is CLOSED; M3 launched
  2026-06-01. This is not a contradiction of the closure and does not reopen
  it — it is a putative successor checkpoint, tracked as its own artifact under
  a slug named for what is actually observable (the alpha handle), not for the
  guess.

  **Slug note.** Named `minimax-space-bunny-alpha-2026-09` rather than
  `minimax-m3-1-*` deliberately: slugs are immutable, and if the fingerprinting
  is wrong the stealth handle is still the correct name for the thing observed.
expected: "Free anonymous alpha live on OpenRouter now. Open: the vendor revealing itself, whether it is in fact MiniMax M3.1, any benchmark or model card, pricing after the free window, and whether the 1M context and image/video input survive into the named release."
labels:
  - minimax
  - stealth-model
  - openrouter
  - coding
  - long-context
  - in-testing
verification: unverified
sources:
  - https://x.com/mark_k/status/2103170218134491535
  - https://x.com/mhdfaran/status/2103450338548498615
created_at: 2026-09-25
updated_at: 2026-09-25
closed_at: null
closed_reason: null
history:
  - ts: 2026-09-25
    change: "Created — IN-TESTING / unverified. An anonymous model, 'Space Bunny Alpha', appeared on OpenRouter free to use, with a 1M-token context window, image and video input, and a fast-strong-coding pitch (@mark_k, 2026-09-24 17:10 UTC); community fingerprinting points at a MiniMax M3.1 preview but no vendor has confirmed. Independent hands-on the next morning: @mhdfaran ran it in OpenCode against a FastAPI repo with three planted failure modes it was not told the location of, and it went 3 failing to 6 passing tests in ~83 seconds across two files, adding two edge-case tests unprompted — recorded as evidence the endpoint is genuinely serving, not as a capability measurement. Status in-testing because a real, publicly callable artifact exists; verification unverified because the vendor is unnamed and the MiniMax attribution is community inference only. Slug deliberately names the observable stealth handle rather than the guessed model id, because slugs are immutable and the fingerprint may be wrong. Not a reopening of the closed [[minimax-m3]] ticket — that release stands; this is a putative successor checkpoint tracked as its own artifact. The anonymous-alpha-then-reveal pattern has precedent in this repo: [[stealth-ox-alpha-model-2026-08]] tracked the Ox Alpha slot that [[zhipu-glm-5-3-2026-08]] later confirmed as GLM-5.3-Flash."
---

The useful discipline here is to track the thing that exists, not the thing
people think it is.

What exists is a free, anonymous endpoint on OpenRouter with a 1M context
window that accepts images and video and is being handed real repair tasks by
strangers. That is a complete, checkable artifact. The MiniMax M3.1 label is a
community guess, and guesses about stealth slots have been wrong before.

The launch pattern itself is now standard and worth naming. Put a capable
checkpoint behind a nonsense handle, make it free, let OpenRouter's traffic
generate a week of organic evaluation and fingerprinting, then reveal. It buys
real-world load testing and a pre-built audience at the cost of a few days of
free inference. GLM-5.3-Flash ran the same play as Ox Alpha and came out of it
with the biggest launch in OpenRouter's history.

If the MiniMax read is right, the interesting question is what changed between
M3 and this. M3 shipped in June as an open-weights model with 1M context via
MiniMax Sparse Attention; an M3.1 arriving as a closed anonymous alpha rather
than a weights drop would be a notable shift in posture, and worth confirming
before it gets narrated as continuity.

Resolution is cheap and near: either the vendor reveals itself or the endpoint
disappears. Both are informative.
