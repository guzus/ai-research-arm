#!/usr/bin/env python3
"""Build the run-scoped OpenCode config for one validated provider/model ref."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


MODEL_REF = re.compile(r"^[a-z0-9][a-z0-9-]*/[A-Za-z0-9][A-Za-z0-9._/-]*$")


def build(source: Path, destination: Path, model_ref: str) -> None:
    if not MODEL_REF.fullmatch(model_ref):
        raise ValueError("model must be one canonical provider/model ref")
    provider_id, model_id = model_ref.split("/", 1)
    if any(part in {"", ".", ".."} for part in model_id.split("/")):
        raise ValueError("model contains an unsafe or empty path segment")
    config = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("base OpenCode config must be a JSON object")
    providers = config.setdefault("provider", {})
    if not isinstance(providers, dict):
        raise ValueError("base OpenCode provider config must be an object")
    provider = providers.setdefault(provider_id, {})
    if not isinstance(provider, dict):
        raise ValueError("selected OpenCode provider config must be an object")
    models = provider.setdefault("models", {})
    if not isinstance(models, dict):
        raise ValueError("selected OpenCode model catalog must be an object")
    models.setdefault(model_id, {})

    temporary = destination.with_name(destination.name + ".tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(config, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("model_ref")
    args = parser.parse_args()
    try:
        build(args.source, args.destination, args.model_ref)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
