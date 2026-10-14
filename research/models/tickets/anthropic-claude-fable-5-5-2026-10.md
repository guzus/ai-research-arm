---
slug: anthropic-claude-fable-5-5-2026-10
title: "Claude Fable 5.5 — claude-fable-5-5 record reportedly found in Microsoft's Azure model catalog"
company: Anthropic
model: Claude Fable 5.5
status: in-testing
status_note: |
  **2026-10-14 — first artifact claim: an Azure catalog record.** @chetaslua
  (2026-10-14 11:39 UTC, two screenshots) says Microsoft's raw Azure model catalog
  contains a `claude-fable-5-5` record. Per the post, it was registered on
  2026-09-28, the same day as the Sonnet 5.5 and Haiku 5.5 records (both since
  shipped), across 9 regions, which is the same footprint as Fable 5.1. Relayed by
  @srikanthvaluri. This is a cloud-catalog listing, the artifact class this
  schema maps to `in-testing`. It has one originator and no Anthropic or Microsoft
  statement, so verification stays `unverified`. The rumored 2026-10-06 date
  passed without a release.

  **Earlier (2026-10-02/04):** A single account (@MehdiCade, 2026-10-02) claims Fable 5.1 "is reportedly
  being routed to a backend that looks like Fable 5.5" and speculates Anthropic
  is testing the next checkpoint on real users. No screenshot, model ID, API
  artifact or Anthropic statement captured. "Reportedly" is not attributed.
  The rest of the 5.5 family (Opus, Sonnet) shipped in late September, which
  makes the name plausible but is not evidence.
expected: "No date. The rumored 2026-10-06 date passed without a release. An Azure catalog record (registered 2026-09-28) is reported as staged. Watch for an independent reproduction of that record, an API/console model ID, or an Anthropic post."
labels:
  - anthropic
  - claude
  - unreleased
  - cloud-catalog-leak
verification: unverified
sources:
  - https://x.com/MehdiCade/status/2105999647688819140
  - https://x.com/mark_k/status/2106719758544457927
  - https://x.com/zwb44/status/2106721228543189454
  - "https://x.com/chetaslua/status/2110334798694859171"
  - "https://x.com/srikanthvaluri/status/2110339193419555323"
created_at: 2026-10-02
updated_at: 2026-10-14
closed_at: null
closed_reason: null
history:
  - ts: 2026-10-02
    change: "Created — RUMORED / unverified. Single-source claim (@MehdiCade, 2026-10-02 12:33 UTC) that Fable 5.1 requests are being routed to a backend 'that looks like Fable 5.5', with no artifact, model ID or Anthropic statement. Predecessor tickets [[anthropic-claude-fable-5-1-2026-08]] and [[claude-fable-5]] are closed and untouched."
  - ts: 2026-10-04
    change: "Rumor broadens, still no artifact. @mark_k (2026-10-04 12:15 UTC, a recap of the claim rather than new evidence) says 'several users claim they're being routed to a newer model' while the picker still says Fable 5.1, citing creative-coding / motion-design demos (Blender, audio APIs), and that 'a Tuesday, October 6 release is circulating as a rumor' — adding 'Anthropic hasn't confirmed the model or the date, and the demos alone can't establish what's running behind the scenes.' Counter-view (@zwb44, 12:20 UTC): Anthropic 'have made it pretty clear haiku 5.5 is next' ([[anthropic-haiku-5-5-2026-10]]); routing does not imply a release date. Expected updated to the circulating 2026-10-06 date, explicitly as rumor. Status rumored, verification unverified."
  - ts: 2026-10-14
    change: "RUMORED -> IN-TESTING; verification stays unverified; title updated. This is the first artifact-class claim. @chetaslua (2026-10-14 11:39 UTC, with two screenshots) says Microsoft's raw Azure model catalog has a claude-fable-5-5 record. The post says it was registered on 2026-09-28, the same day as the Sonnet 5.5 and Haiku 5.5 records (both now shipped: [[anthropic-sonnet-5-5-2026-09]], [[anthropic-haiku-5-5-2026-10]]), across 9 regions, matching Fable 5.1's footprint. @srikanthvaluri relays it and asks whether it is a pre-staged record or a launch signal. A cloud-catalog listing is the artifact class this schema maps to in-testing, so the status advances. Verification stays unverified because there is one originator, the screenshots have not been reproduced independently, and neither Anthropic nor Microsoft has commented. The rumored 2026-10-06 release date passed without a release; expected is updated."
---

This is a tease with no artifact. "Routed to a backend that looks like" is the
kind of claim that usually comes from output-style or latency impressions, which
are not identification.

It is opened rather than ignored because the 5.5 numbering now covers Opus
([[anthropic-opus-5-5-2026-09]]) and Sonnet ([[anthropic-sonnet-5-5-2026-09]]),
and a Haiku 5.5 rumor is already open ([[anthropic-haiku-5-5-2026-10]]). If no
corroboration arrives within ~15 cycles it closes as stale-rumor-unverified.

Prior Fable tickets, both closed: [[claude-fable-5]], [[anthropic-claude-fable-5-1-2026-08]].

**2026-10-14 — an artifact, finally.** The reported Azure catalog record is the
first thing on this ticket that can be checked, unlike routing impressions. Its
main detail is the registration date: it matches Sonnet 5.5 and Haiku 5.5, which
fits a family that was staged together and shipped in sequence. Fable 5.5 is the
last of the family still unshipped. One originator is not corroboration, so
verification stays `unverified`.
