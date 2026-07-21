---
slug: anthropic-claude-conway-2026-07
title: Claude Conway — remote always-on agent, internal access cutoff
company: Anthropic
model: Claude Conway
status: in-testing
status_note: |
  Leak via testingcatalog: "Claude Conway" is a remote, always-on Claude
  Agent that runs in a dedicated container. Internal access is reportedly
  being cut off Friday July 24, 2026 — ambiguous whether that means
  discontinuation or a transition toward broader release.
expected: "Internal access cutoff reported for 2026-07-24; outcome (kill vs. graduate to release) unclear"
labels:
  - agent
  - leak
verification: partial
sources:
  - https://x.com/testingcatalog/status/2079224348351582412
created_at: 2026-07-21
updated_at: 2026-07-21
closed_at: null
closed_reason: null
history:
  - ts: 2026-07-21
    change: Created — successor to the closed anthropic-conway-orbit-2026-05 ticket; testingcatalog leak describes "Claude Conway," a remote always-on Claude Agent running in a dedicated container, with internal access reportedly cut off 2026-07-24.
---

`anthropic-conway-orbit-2026-05` was closed 2026-06-16 as a stale,
unverified rumor. This new leak — from testingcatalog, a leak-tracking
account with a track record across this pipeline's other product
tickets — names the same "Conway" codeword explicitly and adds concrete
detail: it's a remote, always-on Claude Agent running in a dedicated
container, and internal access is reportedly being cut off this Friday
(2026-07-24).

Because the prior ticket is closed (read-only per the CRUD contract),
this is filed as a new successor ticket rather than reopening the old
one. Whether the Friday cutoff means the project is being killed or
transitioning toward a public release is unclear from the leak alone —
worth watching for what actually happens on/after 2026-07-24.
