#!/usr/bin/env python3
"""Validate audited agent toolchain pins and generate their human inventory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIN_FILE = ROOT / "data" / "toolchain-pins.json"
DOC_FILE = ROOT / "docs" / "toolchain-pins.md"


def load() -> dict:
    return json.loads(PIN_FILE.read_text(encoding="utf-8"))


def render(data: dict) -> str:
    npm = data["npm"]
    lines = [
        "# Agent toolchain pins",
        "",
        "Generated from `data/toolchain-pins.json` by `scripts/check_toolchain_pins.py`.",
        "The JSON is the reviewable update manifest; CI verifies every trusted build call site matches it.",
        "",
        "| Input | Immutable pin | Integrity |",
        "|---|---|---|",
        f"| Node agent base | `{data['container_images']['node_22_bookworm_slim']}` | OCI index digest |",
        f"| uv copy image | `{data['container_images']['uv_0_9_7']}` | OCI index digest |",
        f"| Birdy | `{data['birdy']['version']}` | SHA-256 per OS/architecture |",
        f"| Cursor Agent | `{data['cursor_agent']['version']}` | SHA-256 per Linux architecture |",
        f"| OpenCode | `{npm['opencode-ai']['version']}` | `{npm['opencode-ai']['integrity']}` |",
        f"| Pi coding agent | `{npm['@mariozechner/pi-coding-agent']['version']}` | `{npm['@mariozechner/pi-coding-agent']['integrity']}` |",
        f"| Codex CLI | `{npm['@openai/codex']['version']}` | `{npm['@openai/codex']['integrity']}` |",
        f"| GitHub Actions | `{len(data['github_actions'])} actions` | Full commit SHA per action |",
        "",
        "## Update procedure",
        "",
        "1. Resolve the exact release/package and independently obtain its digest or registry integrity.",
        "2. Update the version and integrity together in `data/toolchain-pins.json` and every call site named by the checker.",
        "3. Run `uv run python scripts/check_toolchain_pins.py`, the backend container tests, and the relevant canary before merging.",
        "4. Review the generated diff here; do not accept a version-only update without a new integrity value.",
        "",
        "Codex remains pinned but host-executed. Containerization is intentionally deferred until its refreshed ChatGPT auth cache and writer-owned import/commit boundary can be preserved; wrapping only the CLI while mounting the writable host checkout would not reduce the trust boundary.",
        "",
    ]
    return "\n".join(lines)


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    files = {
        "birdy": ROOT / ".github/actions/install-birdy/action.yml",
        "pi": ROOT / ".github/actions/run-pi-container/action.yml",
        "opencode": ROOT / ".github/actions/run-opencode-container/action.yml",
        "cursor": ROOT / ".github/actions/run-cursor-container/action.yml",
        "generative": ROOT / ".github/workflows/generative-research.yml",
    }
    text = {name: path.read_text(encoding="utf-8") for name, path in files.items()}
    node = data["container_images"]["node_22_bookworm_slim"]
    uv = data["container_images"]["uv_0_9_7"]
    for name in ("pi", "opencode", "cursor"):
        if node not in text[name]:
            errors.append(f"{files[name]} does not use audited Node image {node}")
    for name in ("opencode", "cursor"):
        if uv not in text[name]:
            errors.append(f"{files[name]} does not use audited uv image {uv}")

    birdy = data["birdy"]
    if f"default: {birdy['version']}" not in text["birdy"]:
        errors.append("install-birdy default does not match birdy.version")
    for name in ("pi", "opencode", "cursor"):
        if birdy["version"] not in text[name]:
            errors.append(f"{files[name]} does not pin Birdy {birdy['version']}")
        for arch in ("linux_amd64", "linux_arm64"):
            if birdy["sha256"][arch] not in text[name]:
                errors.append(f"{files[name]} lacks Birdy checksum {arch}")

    cursor = data["cursor_agent"]
    if cursor["version"] not in text["cursor"] or "https://cursor.com/install" in text["cursor"]:
        errors.append("Cursor container must use the audited direct package, never the mutable installer")
    for digest in cursor["sha256"].values():
        if digest not in text["cursor"]:
            errors.append("Cursor container lacks an audited architecture checksum")

    npm = data["npm"]
    expected = {
        "pi": f"@mariozechner/pi-coding-agent@{npm['@mariozechner/pi-coding-agent']['version']}",
        "opencode": f"opencode-ai@{npm['opencode-ai']['version']}",
        "generative": f"@openai/codex@{npm['@openai/codex']['version']}",
    }
    for name, literal in expected.items():
        if literal not in text[name]:
            errors.append(f"{files[name]} lacks exact npm pin {literal}")
    if "releases/latest/" in "\n".join(text.values()):
        errors.append("trusted toolchain downloads must not use a mutable latest release URL")

    action_pattern = re.compile(r"^\s*uses:\s+([^./][^@\s]+)@([^\s#]+)", re.MULTILINE)
    observed: dict[str, set[str]] = {}
    for path in (ROOT / ".github").rglob("*.yml"):
        for action, ref in action_pattern.findall(path.read_text(encoding="utf-8")):
            observed.setdefault(action, set()).add(ref)
    expected_actions = data["github_actions"]
    for action, refs in sorted(observed.items()):
        pin = expected_actions.get(action)
        if not pin:
            errors.append(f"external action {action} is missing from github_actions pins")
            continue
        if refs != {pin['sha']}:
            errors.append(f"external action {action} uses {sorted(refs)}, expected {pin['sha']}")
    for action in expected_actions:
        if action not in observed:
            errors.append(f"github_actions pin {action} has no workflow call site")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    data = load()
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    content = render(data)
    if args.check:
        if not DOC_FILE.exists() or DOC_FILE.read_text(encoding="utf-8") != content:
            print(f"error: {DOC_FILE} is stale; run without --check", file=sys.stderr)
            return 1
        print("toolchain pins and generated inventory are in sync")
        return 0
    DOC_FILE.write_text(content, encoding="utf-8")
    print(f"updated {DOC_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
