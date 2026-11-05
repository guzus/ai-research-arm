# Chubby direct-chat project key

ARA has a service-scoped Chubby client named `ai-research-arm`. Provisioning
and allowlist readback were verified on 2026-11-05. This is optional direct
inference access, not a new workflow backend or a migration of scheduled lanes.
The routing source of truth remains `data/agent-backends.json`.

## Configuration and storage

Configure the deployment's HTTPS direct-chat endpoint in `CHUBBY_CHAT_BASE_URL`
(including `/v1`) and keep the project-scoped `chb_` key in
`CHUBBY_CHAT_API_KEY` in a server-side secret store. The caller must have network
access to that endpoint. Use the placeholders in [`.env.example`](../.env.example);
no deployment address, session identifier, or secret value belongs in Git.

These `CHUBBY_CHAT_*` names keep direct-chat configuration separate from the
Claude Code Messages adapter in [the Messages guide](chubby.md). The Messages
canary requires its own `cbm_` key, a base URL without `/v1`, and its separately
registered model. The direct-chat key cannot authorize that canary.

Do not use an operator credential or upstream provider key as the project key.
The public dashboard must never receive either API key.

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

`CHUBBY_CHAT_MODEL` currently defaults to `meta/muse-spark-1.3`; callers must select
an exact allowed model. Limits remain 4 concurrent requests and 60 requests per
minute. Future allowlist changes should update the existing client rather than
issue replacement keys.

## Verify access

From a shell with the direct-chat configuration loaded, this read-only check verifies
connectivity, authentication, and the current allowlist without printing the key:

```bash
python3 - <<'PYTHON'
import json
import os
import urllib.request

request = urllib.request.Request(
    os.environ["CHUBBY_CHAT_BASE_URL"].rstrip("/") + "/models",
    headers={"Authorization": "Bearer " + os.environ["CHUBBY_CHAT_API_KEY"]},
)
with urllib.request.urlopen(request, timeout=30) as response:
    for model in json.load(response)["data"]:
        print(model["id"])
PYTHON
```

The initial key's `/models` check returned HTTP 200; the expanded eight-model
allowlist was verified through the operator client readback. No inference call
was made, so provider availability and end-to-end generation remain unverified.

For a future direct-inference integration, consult the deployment's Chubby chat
contract. Its chat subset does not replace CLI harnesses or their tools.
Preserve exact model IDs, validate the supported request shape, disable
automatic paid retries, and use an idempotency key per logical request. Verify
one small inference call and its request/usage record before routing production
work through it.
