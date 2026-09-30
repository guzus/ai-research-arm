#!/usr/bin/env python3
"""Fail closed unless a native model canary proves model identity and tool use."""

import argparse
from pathlib import Path

from summarize_claude_execution import parse_objects


def validate(objects: list[dict], model: str, fixture: Path) -> None:
    results = [obj for obj in objects if obj.get("type") == "result"]
    if not results or results[-1].get("is_error") is not False:
        raise ValueError("canary has no successful result")
    result = results[-1]
    if result.get("subtype") != "success":
        raise ValueError("canary did not complete successfully")
    if result.get("permission_denials"):
        raise ValueError("canary encountered permission denials")
    usage = result.get("modelUsage", {})
    if model not in usage or usage[model].get("outputTokens", 0) <= 0:
        raise ValueError("requested model has no observed output usage")
    messages = [obj.get("message", {}) for obj in objects
                if obj.get("type") == "assistant"]
    if any(msg.get("model") != model for msg in messages):
        raise ValueError("canary used a different assistant model")
    reads = [part for msg in messages for part in msg.get("content", [])
             if part.get("type") == "tool_use" and part.get("name") == "Read"]
    read_ids = {part.get("id") for part in reads
                if Path(part.get("input", {}).get("file_path", "")).resolve()
                == fixture.resolve() and part.get("id")}
    if not read_ids:
        raise ValueError("canary did not read the requested fixture")
    token = fixture.read_text().strip()
    tool_results = [part for obj in objects if obj.get("type") == "user"
                    for part in obj.get("message", {}).get("content", [])
                    if isinstance(part, dict) and part.get("type") == "tool_result"]
    if not any(part.get("tool_use_id") in read_ids and not part.get("is_error")
               and token in str(part.get("content", "")) for part in tool_results):
        raise ValueError("canary has no successful fixture Read result")
    if result.get("result", "").strip() != token:
        raise ValueError("canary did not return the fixture contents")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("execution_file", type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    args = parser.parse_args()
    validate(parse_objects(args.execution_file.read_text()), args.model, args.fixture)
    print(f"Verified {args.model}: successful Read-tool round trip, no publication")


if __name__ == "__main__":
    main()
