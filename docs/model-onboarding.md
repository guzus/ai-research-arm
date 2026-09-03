# Model onboarding

`data/agent-backends.json` is the model registry. For **a model already served
by a registered provider and adapter**, exposing it to `generative-research`
is one hand-authored backend entry followed by generated artifacts:

```json
"opencode-example": {
  "adapter": "opencode",
  "provider": "opencode-go",
  "model": "vendor/example-model",
  "display_name": "Example via OpenCode Go",
  "aliases": ["example"],
  "production_eligible": false,
  "generative": {
    "exposed": true,
    "selector": "opencode-example",
    "provenance_model": "vendor/example-model",
    "protocol": "openai-chat-completions",
    "preflight_path": "chat/completions"
  }
}
```

Then run:

```bash
uv run python scripts/build_backend_matrix.py
uv run python scripts/build_backend_matrix.py --check
uv run python scripts/test_resolve_generative_backend.py
```

The resolver accepts the canonical backend key, `generative.selector`, and
declared aliases. It rejects non-exposed entries, unsafe shell/output values,
unsupported adapter/provider/protocol combinations, and ambiguous aliases.
Model IDs may contain nested `/` segments; the fully qualified reference is
always formed as `provider/model`, splitting only at the provider boundary.

## The boundary that remains code

A new provider or adapter is **not** a registry-only change. It needs an
explicit credential binding under `adapters.provider_credentials`, a contained
runner implementation, preflight/auth behavior, workflow secret plumbing, and
tests of the artifact/import contract. Do not claim onboarding is complete
from a registry row when those mechanics do not already exist.

`generative.exposed` permits an explicit/manual research run; it does not grant
production routing. Production `research-editorial` routes additionally require
`production_eligible: true`, isolation/editorial capabilities, the exact
credential binding, and a supported dispatcher adapter. Live provider proof is
an operational canary, separate from static registration.

Muse Spark Contributor demonstrates the distinction: it is exposed for
explicit runs but has `production_eligible: false` plus structured manual,
workspace-consent, and region restrictions. Route resolution fails closed if a
route edit attempts to promote it.
