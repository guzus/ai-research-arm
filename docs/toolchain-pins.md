# Agent toolchain pins

Generated from `data/toolchain-pins.json` by `scripts/check_toolchain_pins.py`.
The JSON is the reviewable update manifest; CI verifies every trusted build call site matches it.

| Input | Immutable pin | Integrity |
|---|---|---|
| Node agent base | `node:22-bookworm-slim@sha256:83f487e0a63425e5b4d146fb5e5be574bcbe1b7b843d3ebafdd95eaf7767a7e5` | OCI index digest |
| uv copy image | `ghcr.io/astral-sh/uv:0.9.7@sha256:ba4857bf2a068e9bc0e64eed8563b065908a4cd6bfb66b531a9c424c8e25e142` | OCI index digest |
| Birdy | `v1.1.0` | SHA-256 per OS/architecture |
| Cursor Agent | `2026.08.25-3e8eec8` | SHA-256 per Linux architecture |
| OpenCode | `1.18.3` | `sha512-HnItl/+uhSpj7JV9x6ITiE0XFq4b/PKF5OM03TIyiFoFiLw3MQoJOAXZFTEzC7IOgAIYcysRQBBmCmlXILkxww==` |
| Pi coding agent | `0.73.1` | `sha512-gXQh3SaZmWTfVMc4Ao5+LGbVeKvzyO7tolok0nLsZgq9nGjZx/EEU3NM8C+qUnB4Nvs2rswG5qOVgLzQkq0fHQ==` |
| Codex CLI | `0.151.0` | `sha512-mhtWmOZRdmWD1jPbLDnQb59BsaVP/V+lXe/OFNR9ZcLZU0UCiBwn98Fcav1ss7sDIlHkuqj6nWd44IPeXoOhJA==` |
| GitHub Actions | `7 actions` | Full commit SHA per action |

## Update procedure

1. Resolve the exact release/package and independently obtain its digest or registry integrity.
2. Update the version and integrity together in `data/toolchain-pins.json` and every call site named by the checker.
3. Run `uv run python scripts/check_toolchain_pins.py`, the backend container tests, and the relevant canary before merging.
4. Review the generated diff here; do not accept a version-only update without a new integrity value.

Codex remains pinned but host-executed. Containerization is intentionally deferred until its refreshed ChatGPT auth cache and writer-owned import/commit boundary can be preserved; wrapping only the CLI while mounting the writable host checkout would not reduce the trust boundary.
