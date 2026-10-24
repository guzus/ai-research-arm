#!/usr/bin/env python3
"""Capture content-free research execution evidence before retries overwrite it.

No network or credentials. Only allowlisted identifiers, numbers, hashes and
statuses cross the artifact boundary. Raw prompts, reasoning, arguments, tool
results, exception text and environment variables are never copied.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import tempfile

from summarize_claude_execution import parse_objects

SCHEMA_VERSION = 1
MAX_TRANSCRIPT_BYTES = 32 * 1024 * 1024
MAX_EVENTS = 2000
ATTEMPTS = {
    "gen-claude": "Run Generative Research (Claude, attempt 1)",
    "gen-claude-retry": "Run Generative Research (Claude, retry 1)",
    "gen-deepseek": "Run Generative Research (Fireworks, attempt 1)",
    "gen-deepseek-retry": "Run Generative Research (Fireworks, retry 1)",
    "gen-deepseek-retry-2": "Run Generative Research (Fireworks, retry 2)",
}
TOOLS = frozenset({
    "Read", "Write", "Edit", "MultiEdit", "Bash", "Glob", "Grep", "LS",
    "WebSearch", "WebFetch", "Task", "Agent", "TodoWrite", "TodoRead",
    "NotebookEdit", "TaskOutput", "TaskStop", "Skill", "ToolSearch",
})
OUTCOMES = frozenset({"success", "failure", "cancelled", "skipped", "unknown"})
USAGE_FIELDS = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def number(value):
    return value if type(value) in (int, float) and 0 <= value <= 1e12 and math.isfinite(value) else None


def boolean(value):
    return True if value == "true" else False if value == "false" else None


def choice(value, options, default="unknown"):
    return value if isinstance(value, str) and value in options else default


def known_identifiers(registry: dict) -> set[str]:
    """The registry supplies identifiers; transcripts cannot invent labels."""
    result = set()
    def visit(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if isinstance(child, str) and key in {"model", "native_model", "provenance_model", "model_ref"}:
                    result.add(child)
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    visit(registry)
    return result - {""}


def read_regular(path: Path, limit: int) -> bytes:
    # O_NONBLOCK avoids hanging on a FIFO from an agent-controlled path.
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as handle:
        info = os.fstat(handle.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError("not a bounded regular file")
        data = handle.read(limit + 1)
        if len(data) > limit:
            raise ValueError("file grew beyond limit")
        return data


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".trace-")
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(value, handle, allow_nan=False, separators=(",", ":"))
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def normalize(objects: list[dict], models: set[str]) -> dict:
    events = []
    messages = {}
    tools = {}
    result = {}
    recognized = 0
    for obj in objects:
        kind = choice(obj.get("type"), {"assistant", "user", "result", "system"})
        if kind in {"assistant", "user", "result", "system"}:
            recognized += 1
        if kind == "result":
            result = {
                "is_error": obj.get("is_error") if type(obj.get("is_error")) is bool else None,
                "duration_ms": number(obj.get("duration_ms")),
                "num_turns": number(obj.get("num_turns")),
                # Claude's USD estimate is NOT the subscription invoice.
                "runtime_estimated_cost_usd": number(obj.get("total_cost_usd")),
            }
        message = obj.get("message")
        if not isinstance(message, dict):
            continue
        content = message.get("content", [])
        if not isinstance(content, list):
            continue
        if kind == "assistant":
            message_id = message.get("id")
            # Streaming updates with the same message id are one generation.
            key = message_id if isinstance(message_id, str) else f"missing-{len(events)}"
            model = message.get("model")
            usage = message.get("usage")
            usage = usage if isinstance(usage, dict) else {}
            event = {
                "kind": "generation", "model": model if isinstance(model, str) and model in models else "unknown",
                "usage": {k: int(v) for k in USAGE_FIELDS if (v := number(usage.get(k))) is not None},
            }
            if key in messages:
                existing = events[messages[key]]
                existing["usage"].update(event["usage"])
            elif len(events) < MAX_EVENTS:
                messages[key] = len(events)
                events.append(event)
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                call_id = block.get("id")
                if not isinstance(call_id, str) or call_id in tools or len(events) >= MAX_EVENTS:
                    continue
                tools[call_id] = len(events)
                events.append({"kind": "tool", "name": block.get("name") if isinstance(block.get("name"), str) and block["name"] in TOOLS else "other",
                               "generation": messages.get(key), "outcome": "unknown"})
        elif kind == "user":
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_result":
                    continue
                call_id = block.get("tool_use_id")
                if isinstance(call_id, str) and call_id in tools:
                    events[tools[call_id]]["outcome"] = "failure" if block.get("is_error") is True else "success"
    return {"coverage": "structured" if recognized else "unrecognized",
            "events": events, "events_capped": len(events) >= MAX_EVENTS, "result": result}


def capture(path: str, models: set[str]) -> dict:
    if not path:
        return {"coverage": "missing", "events": [], "result": {}}
    try:
        raw = read_regular(Path(path), MAX_TRANSCRIPT_BYTES)
        return {**normalize(parse_objects(raw.decode(errors="replace")), models),
                "transcript_sha256": hashlib.sha256(raw).hexdigest()}
    except (OSError, ValueError, RecursionError):
        return {"coverage": "unreadable", "events": [], "result": {}}


def summary(steps: dict, registry: dict) -> dict:
    def output(step, key):
        return steps.get(step, {}).get("outputs", {}).get(key)
    backends = set(registry.get("backends", {}))
    # Selectors are registry keys in current SSOT, plus explicit generative aliases.
    def labels(value):
        if isinstance(value, dict):
            for k, v in value.items():
                if k in {"selector", "backend"} and isinstance(v, str):
                    backends.add(v)
                labels(v)
        elif isinstance(value, list):
            for v in value:
                labels(v)
    labels(registry)
    selected = output("effective", "requested_backend")
    effective = output("effective", "backend")
    outcomes = {}
    for step in [*ATTEMPTS, "gen-codex", "gen-opencode", "gen-cursor", "quality", "verifier-audit", "methodology", "push", "fireworks-preflight"]:
        outcome = steps.get(step, {}).get("outcome", "unknown")
        outcomes[step] = choice(outcome, OUTCOMES)
    return {
        "schema_version": SCHEMA_VERSION,
        "requested_backend": selected if isinstance(selected, str) and selected in backends else "unknown",
        "effective_backend": effective if isinstance(effective, str) and effective in backends else "unknown",
        "used_fallback": boolean(output("effective", "used_fallback")),
        "published": boolean(output("push", "pushed")),
        "has_article": boolean(output("outfile", "has_file")),
        "outcomes": outcomes,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["capture", "summary"])
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--attempt", choices=ATTEMPTS)
    args = parser.parse_args()
    registry = json.loads(Path("data/agent-backends.json").read_text())
    if args.command == "capture":
        if not args.attempt:
            parser.error("capture requires --attempt")
        record = capture(os.environ.get("EXECUTION_FILE", ""), known_identifiers(registry))
        record.update(schema_version=SCHEMA_VERSION, attempt=args.attempt)
        write_json(args.output_dir / f"{args.attempt}.json", record)
        print(f"Research trace captured: {args.attempt}, coverage={record['coverage']}")
    else:
        write_json(args.output_dir / "summary.json", summary(json.loads(os.environ["RESEARCH_STEPS"]), registry))


if __name__ == "__main__":
    main()
