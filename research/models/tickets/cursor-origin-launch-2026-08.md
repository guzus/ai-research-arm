---
slug: cursor-origin-launch-2026-08
title: Cursor Origin — code-hosting platform launches in beta
company: Anysphere (Cursor) / SpaceX
model: null
status: released
status_note: |
  **Cursor Origin**, a code-hosting platform "deeply integrated with
  Cursor," began rolling out in **beta** on 2026-08-17 (@testingcatalog,
  17:30 UTC; @mark_k relaying the launch post the same day). Vercel CEO
  **Guillermo Rauch** confirmed the end-to-end path from the other side:
  "You can now host your repos in Cursor Origin and deploy to Vercel via
  Cursor Origin which is itself hosted on Vercel. And unlike GitHub, it's
  online 😁."

  This is a **GitHub-substitution** move, not a model release, which is why
  it matters for the roadmap: it puts the repository — the artifact agents
  actually operate on — inside the agent vendor's own perimeter. @mark_k's
  one-line read: "It's over for GitHub."

  Ownership context: Cursor/Anysphere was acquired by SpaceX in a ~$60B
  all-stock deal ([[spacex-cursor-acquisition-2026-06]]), so this ships
  under SpaceX-owned Anysphere alongside the jointly-trained Composer 3
  model ([[cursor-spacexai-model-2026-06]]).
expected: "Beta rolling out from 2026-08-17. Pending: general availability, pricing, migration/import tooling, and whether agent-side features (Composer 3, Sand) get repo-level integration that GitHub cannot match"
labels:
  - cursor
  - developer-platform
  - code-hosting
  - agentic
  - released
verification: confirmed
sources:
  - "@testingcatalog"
  - "@rauchg"
  - "@mark_k"
created_at: 2026-08-19
updated_at: 2026-08-19
closed_at: null
closed_reason: null
history:
  - ts: 2026-08-19
    change: "Created — Cursor Origin, a code-hosting platform deeply integrated with Cursor, started rolling out in beta on 2026-08-17 (@testingcatalog 17:30 UTC; @mark_k relaying the launch post). Corroborated from the counterparty side by Vercel CEO @rauchg, who confirmed hosting repos in Origin and deploying to Vercel works end to end. Status released (beta is publicly rolling out); verification confirmed (launch post plus an independent CEO-level firsthand confirmation). Ships under SpaceX-owned Anysphere ([[spacex-cursor-acquisition-2026-06]])."
---

**Cursor Origin** is Anysphere's own **code-hosting platform**, rolled out
in beta from **2026-08-17** and described as "fast, easy to use, and deeply
integrated with Cursor."

**Why a git host belongs on a model timeline.** Because the repository is
where coding agents actually live. Every agent vendor currently rents that
surface from GitHub — a Microsoft property that also ships a competing
agent. Owning the host means the agent can be wired into the repo at a
level a third-party API cannot reach, and it removes a dependency on a
rival. @mark_k's reaction ("It's over for GitHub") is hyperbole; the
strategic direction it points at is not.

**Corroboration from the other end of the pipe.** Vercel CEO **Guillermo
Rauch** posted that you can host repos in Cursor Origin and deploy to
Vercel from it — a firsthand, CEO-level confirmation from a counterparty
with no reason to promote a competitor's launch. That plus the launch post
is why `verification` is `confirmed` on a product that is only in beta.

**Ownership matters here.** Anysphere is SpaceX-owned as of the ~$60B
all-stock acquisition ([[spacex-cursor-acquisition-2026-06]]), and it also
ships the jointly-trained frontier coding model Composer 3
([[cursor-spacexai-model-2026-06]]) and is reported to be building a
general-purpose agent, Sand ([[cursor-sand-agent-2026-07]]). Origin is the
storage layer under all of it.

**What is not known.** No GA date, no pricing, no migration/import tooling
detail, and no announced repo-level agent capability that would actually
justify leaving GitHub. Until one appears, this is a well-executed
commodity launch with a strategic thesis attached.

**Transition triggers:**
- General availability, pricing, or a named enterprise migration → UPDATE.
- An agent capability that requires owning the host (repo-native Composer 3
  or Sand integration) → UPDATE; that is the claim to watch.
- ≥4 weeks past GA, settled into normal coverage →
  `closed: released-and-aged`.

**Dedup note:** the Cursor/SpaceX model stays on
[[cursor-spacexai-model-2026-06]], the general agent on
[[cursor-sand-agent-2026-07]], and the acquisition on
[[spacex-cursor-acquisition-2026-06]]. Further Origin signal UPDATES this
ticket.
