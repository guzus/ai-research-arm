#!/usr/bin/env python3
"""Build read-only Birdy account JSON for CI workflows."""
from __future__ import annotations

import json
import os
import sys
from typing import Any


class BirdyAccountError(ValueError):
    pass


def build_accounts(
    accounts_json: str | None,
    auth_token: str | None,
    ct0: str | None,
) -> list[dict[str, Any]]:
    raw = (accounts_json or "").strip()
    if raw:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise BirdyAccountError(f"BIRDY_ACCOUNTS must be valid JSON: {exc.msg}") from exc
        if not isinstance(parsed, list) or not parsed:
            raise BirdyAccountError("BIRDY_ACCOUNTS must be a non-empty JSON array")
        accounts = parsed
    else:
        if not auth_token or not ct0:
            raise BirdyAccountError("BIRD_AUTH_TOKEN and BIRD_CT0 are required when BIRDY_ACCOUNTS is empty")
        accounts = [{"name": "ci", "auth_token": auth_token, "ct0": ct0}]

    normalized = []
    for idx, account in enumerate(accounts, start=1):
        if not isinstance(account, dict):
            raise BirdyAccountError("every BIRDY_ACCOUNTS entry must be an object")
        item = dict(account)
        item.setdefault("name", f"ci-{idx}")
        if not isinstance(item["name"], str) or not item["name"].strip():
            raise BirdyAccountError(f"BIRDY_ACCOUNTS entry {idx} must have a non-empty string name")
        for key in ("auth_token", "ct0"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise BirdyAccountError(f"BIRDY_ACCOUNTS entry {idx} must have a non-empty {key}")
        item["read_only"] = True
        normalized.append(item)

    return normalized


def main() -> int:
    try:
        accounts = build_accounts(
            os.environ.get("BIRDY_ACCOUNTS_JSON"),
            os.environ.get("BIRD_AUTH_TOKEN"),
            os.environ.get("BIRD_CT0"),
        )
    except BirdyAccountError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(accounts, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
