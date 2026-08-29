#!/usr/bin/env python3
"""Copy a trusted Cursor CLI permission config into the run-scoped mount.

The model is selected by `agent --model`, not by this file. The helper
validates the committed policy is a JSON object, fills the CLI schema
fields the official client self-repairs (`version`, `editor.vimMode`,
`permissions.allow`/`deny`), and materializes an owner-read-only copy
the container can mount without giving the agent a writable path back
to the real checkout.
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
    # The CLI self-repairs missing required fields by rewriting the file.
    # The host mount is mode 0400 and :ro, so that rewrite EACCES-exits
    # before the model runs (Cursor CLI Canary 31997748051). Fill them
    # here so the mounted policy is already valid.
    config.setdefault("version", 1)
    editor = config.setdefault("editor", {})
    if not isinstance(editor, dict):
        raise ValueError("editor must be a JSON object")
    editor.setdefault("vimMode", False)
    permissions = config.setdefault("permissions", {})
    if not isinstance(permissions, dict):
        raise ValueError("permissions must be a JSON object")
    permissions.setdefault("allow", [])
    permissions.setdefault("deny", [])

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
