# Office Chubby project key

ARA has a service-scoped Chubby client named `ai-research-arm`. Provisioning
and allowlist readback were verified on 2026-11-05. This is optional direct
inference access, not a new workflow backend or a migration of scheduled lanes.
The routing source of truth remains `data/agent-backends.json`.

## Configuration and storage

The endpoint is `https://gunux.tailc0c7fe.ts.net/office/api/chubby/v1` and
requires tailnet connectivity from the calling runtime.

The Office session `gunux/ai-research-arm-3` holds `CHUBBY_API_KEY`,
`CHUBBY_BASE_URL`, `CHUBBY_MODEL`, and `CHUBBY_CLIENT_ID` in its Secrets.
The key is not in Git or GitHub Actions secrets. Office loads these variables
on the session's next Resume/Restart; an already-running agent does not
receive them automatically. On gunux, sessionctl stores them in the protected
`~/.local/state/sessionctl/secrets/ai-research-arm-3.env` file (mode 0600).
Do not print this file or paste its contents into a transcript.

For another authorized server-side runtime, provision the same project key
through its secret store and use the placeholders in [`.env.example`](../.env.example).
Do not use the Office operator password or provider credentials as the project key.
The public dashboard must never receive `CHUBBY_API_KEY`.

## Allowed models

The existing key permits these exact Chubby IDs as of 2026-11-05:

| Model | Chubby ID |
| --- | --- |
| Muse Spark 1.3 | `meta/muse-spark-1.3` |
| Claude Opus 5.5 | `anthropic/claude-opus-5-5` |
| GLM 5.3 Flash, OpenCode | `opencode/glm-5.3-flash` |
| GLM 5.3, OpenCode | `opencode/glm-5.3` |
| DeepSeek V4.1 Flash, OpenCode | `opencode/deepseek-v4.1-flash` |
| GLM 5.3, Fireworks | `fireworks/accounts/fireworks/models/glm-5p3` |
| DeepSeek V4.1 Flash, Fireworks | `fireworks/accounts/fireworks/models/deepseek-v4p1-flash-1017` |
| Kimi K3, Fireworks | `fireworks/accounts/fireworks/models/kimi-k3` |

The allowlist covers currently available counterparts of model/provider families
configured in ARA, not exact compatibility with every historical pin. Opus 5.5,
DeepSeek V4.1 Flash, GLM 5.3, and Kimi K3 are not aliases for older workflow
versions. OpenCode Zen access through Office is not the repository's OpenCode Go
subscription, and Meta's direct Muse route is not the OpenCode Contributor route.
Z.ai's direct provider route, Cursor/Codex subscription transports, and Gemini
TTS are not provided by this key. Allowlisting a model does not verify its upstream
credentials or authorize silently replacing an existing lane.

`CHUBBY_MODEL` currently defaults to `meta/muse-spark-1.3`; callers must select
an exact allowed model. Limits remain 4 concurrent requests and 60 requests per
minute. Future allowlist changes should update the existing client rather than
issue replacement keys.

## Verify access

From a shell with the session secrets loaded, this read-only check verifies
connectivity, authentication, and the current allowlist without printing the key:

```bash
python3 - <<'PYTHON'
import json
import os
import urllib.request

request = urllib.request.Request(
    os.environ["CHUBBY_BASE_URL"].rstrip("/") + "/models",
    headers={"Authorization": "Bearer " + os.environ["CHUBBY_API_KEY"]},
)
with urllib.request.urlopen(request, timeout=30) as response:
    for model in json.load(response)["data"]:
        print(model["id"])
PYTHON
```

The initial key's `/models` check returned HTTP 200; the expanded eight-model
allowlist was verified through the operator client readback. No inference call
was made, so provider availability and end-to-end generation remain unverified.

For a future direct-inference integration, use the
[Office Chubby contract](https://github.com/guzus/office/blob/main/docs/chubby.md).
Its chat subset does not replace CLI harnesses or their tools. Preserve exact
model IDs, validate the supported request shape, disable automatic paid retries,
and use an idempotency key per logical request. Verify one small inference call
and its request/usage record before routing production work through it.
