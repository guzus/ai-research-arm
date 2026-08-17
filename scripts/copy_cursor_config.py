#!/usr/bin/env python3
"""Copy a trusted Cursor CLI permission config into the run-scoped mount.

The model is selected by `agent --model`, not by this file. The helper only
validates that the committed policy is a JSON object and materializes an
owner-read-only copy the container can mount without giving the agent a
writable path back to the real checkout.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


MODEL_REF = re.compile(r"^[a-z0-9][a-z0-9-]*/[A-Za-z0-9][A-Za-z0-9._-]*$")


def copy_config(source: Path, destination: Path, model_ref: str) -> None:
    if not MODEL_REF.fullmatch(model_ref):
        raise ValueError("model must be one canonical provider/model ref")
    config = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("base Cursor CLI config must be a JSON object")

    temporary = destination.with_name(destination.name + ".tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(config, handle, sort_keys=True, indent=2)
            handle.write("\n")
        os.replace(temporary, destination)
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("model_ref")
    args = parser.parse_args()
    copy_config(args.source, args.destination, args.model_ref)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
