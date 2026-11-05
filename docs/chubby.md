# ARA through Office Chubby

ARA's optional `chubby-deepseek-v4p1-flash` backend keeps the existing Claude
Code harness, local tools, sandbox, and output/commit validation. Office owns
provider credentials, model admission, spend limits, and usage accounting.
This uses Chubby's **Anthropic Messages** endpoint, not its direct-chat or
managed-agent API. Managed agents cannot execute an ARA checkout unchanged.

The initial integration is a manual, strict `chubby-canary` lane. No scheduled
lane or global fallback selects Chubby. A passing local test suite establishes
the adapter contract; activation additionally requires the real runner canary
and Office accounting checks below.

## Configuration

| Setting | Location | Value |
| --- | --- | --- |
| `CHUBBY_API_KEY` | GitHub Actions repository secret | Dedicated ARA **Claude Code** key, `cbm_` followed by 64 hex characters |
| `CHUBBY_BASE_URL` | Optional GitHub Actions repository variable | `https://gunux.tailc0c7fe.ts.net/office/api/chubby` (no `/v1`; the Claude SDK appends `/v1/messages`) |
| `CHUBBY_CLIENT_ID` | Recommended repository variable / operator record | Non-secret ARA client ID for Office usage correlation |
| Model | `data/agent-backends.json` | `openrouter/deepseek/deepseek-v4.1-flash-1017` |

The endpoint needs tailnet access from the self-hosted runner. Railway serves
the resulting static artifacts and does not need Chubby credentials or access.
Do not expose Office publicly to work around a routing failure.

Ordinary `chb_` service keys and Office operator/session/verifier tokens do
**not** authorize Messages. An Office operator should first inspect existing
ARA clients and the current `/api/chubby/messages-models` catalog, then reuse
the existing ARA key if available. Otherwise create a dedicated Claude Code
key through Chubby's **Use with Claude Code** interface or
`POST /api/chubby/clients`:

```json
{
  "name": "ara-production",
  "allowedModels": ["openrouter/deepseek/deepseek-v4.1-flash-1017"],
  "messages": true,
  "budgetUsd": 10,
  "maxConcurrent": 2,
  "requestsPerMinute": 30
}
```

Capture the one-time key directly in the repository's Actions secret store;
never commit it or put it in a workflow argument, log, or chat. Do not copy
Office's operator credential or an upstream provider key to ARA. Record the
non-secret client ID. The $10 example is a **lifetime** cap, not a daily reset;
Office reserves each request's maximum possible cost while it is running.
These calls use Office's provider billing, not ARA's Claude subscription.
Catalog membership alone does not prove provider health.

## Run the canary

Once the workflow is present on the repository default branch and the secret
is configured:

```bash
gh workflow run chubby-canary.yml --repo guzus/ai-research-arm
gh run list --repo guzus/ai-research-arm --workflow chubby-canary.yml --limit 1
gh run watch <run-id> --repo guzus/ai-research-arm --exit-status
```

The canary runs on the same self-hosted runner class as ARA's pipelines. It
creates a fresh random input, asks Claude Code to read it and write the exact
contents, and checks the successful transcript, served model identity, both
completed tools, exact file contents, and committed path scope. It permits
only Read/Write, caps the run at eight turns and ten minutes, and publishes
nothing. The backend bounds each response to 4,096 tokens.

Configuration checks make no paid inference call and never claim provider
health. Missing/incorrect keys, unreachable Office, budget exhaustion, and
upstream failures fail the strict canary; it cannot fall back to another
model. Stop and diagnose a failed or ambiguous run before rerunning it.

Then inspect Office **Chubby → Requests/Usage**, filtered by the recorded ARA
client and the GitHub run time. Confirm successful `chbm_` request records,
the exact upstream model, and usage/cost (missing values mean unknown).
Messages currently exposes neither Chubby request/trace response headers nor
an idempotency contract; `cbm_` keys also cannot read `/v1/models`,
`/v1/requests`, or `/v1/usage`. An Office operator/verifier must inspect the
admin ledger. Do not apply the direct-chat API's replay or ledger contract to
this adapter. Automatic Claude request retries are disabled; a manually
repeated run can incur additional spend.

## First production rollout

After the canary and accounting checks pass, use `digest-audio-script` as the
first pilot. It reads one existing digest summary and writes one exact spoken
script, with trusted host output and commit checks. In a reviewed change:

1. Mark the verified profile production eligible and change only that lane's
   backend. Explicitly choose a strict pilot policy so Chubby failure remains
   attributable, rather than inheriting the ordinary provider fallback chain.
2. Pass `chubby-api-key` and the endpoint to that action call, with bounded
   turns and wall-clock time. Generate the backend matrix and README diagram
   using `uv run python scripts/build_backend_matrix.py`.
3. Validate one actual spoken script before wider adoption; inspect the next
   daily-digest run and Office usage for quality, latency, and spend.

Rollback restores that lane's previous SSOT backend/fallback configuration
and regenerates the matrix. Keep Chubby out of the global fallback chain:
Office must not become the sole inference failure domain for ARA. The isolated
editorial dispatcher cannot select this host-checkout adapter; migrating
those lanes needs an adapter that preserves their disposable workspace and
trusted artifact-import boundary.

Current upstream contract: Office
[`docs/chubby.md`](https://github.com/guzus/office/blob/main/docs/chubby.md),
“Claude Code keys.” Integration procedure:
[`chubby-integrate`](https://github.com/guzus/unix-config/blob/main/skills/chubby-integrate/SKILL.md).
