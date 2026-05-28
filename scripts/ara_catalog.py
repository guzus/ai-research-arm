#!/usr/bin/env python3
"""Load and validate the machine-readable ARA component catalog."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG_PATH = REPO_ROOT / "ARA_CATALOG.json"
COMPONENT_ROW_RE = re.compile(r"\|\s*`(ara-[a-z0-9-]+)`\s*\|")


def catalog_path() -> Path:
    return DEFAULT_CATALOG_PATH


def load_catalog(path: Path | None = None) -> dict[str, Any]:
    """Return the parsed ARA catalog, raising loudly on malformed input."""
    target = path or DEFAULT_CATALOG_PATH
    if not target.exists():
        raise RuntimeError(f"ARA catalog not found at {target}")
    try:
        catalog = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise RuntimeError(f"ARA catalog at {target} is invalid JSON: {e}") from e
    if not isinstance(catalog, dict):
        raise RuntimeError(f"ARA catalog at {target} must be a JSON object")
    if not catalog.get("components"):
        raise RuntimeError(f"ARA catalog at {target} has no components")
    return catalog


def catalog_classes(catalog: dict[str, Any]) -> set[str]:
    """Return every base class documented by the catalog.

    Variant classes are intentionally excluded: validator logic accepts
    modifier classes like ara-callout--warn when the base ara-callout is
    present. Keeping the returned set to base classes preserves that rule.
    """
    classes: set[str] = set()
    for comp in catalog.get("components", []):
        if not isinstance(comp, dict):
            raise RuntimeError("each ARA catalog component must be an object")
        for cls in comp.get("classes", []):
            if not isinstance(cls, str) or not cls.startswith("ara-"):
                raise RuntimeError(f"invalid ARA catalog class: {cls!r}")
            if "--" not in cls:
                classes.add(cls)
    if not classes:
        raise RuntimeError("ARA catalog parsed to zero base ara-* classes")
    return classes


def components_md_classes(path: Path | None = None) -> set[str]:
    """Parse the human reference table in COMPONENTS.md.

    This deliberately reads only table first-column class rows so anti-examples
    such as ara-grid in prose do not become valid classes.
    """
    target = path or (REPO_ROOT / "COMPONENTS.md")
    text = target.read_text(encoding="utf-8")
    return {m.group(1) for line in text.splitlines() if (m := COMPONENT_ROW_RE.match(line))}


def validate_catalog_against_components(
    catalog_path_: Path | None = None,
    components_path: Path | None = None,
) -> list[str]:
    catalog = load_catalog(catalog_path_)
    from_catalog = catalog_classes(catalog)
    from_components = components_md_classes(components_path)
    errors: list[str] = []
    missing = sorted(from_components - from_catalog)
    extra = sorted(from_catalog - from_components)
    if missing:
        errors.append("catalog missing COMPONENTS.md classes: " + ", ".join(missing))
    if extra:
        errors.append("catalog has classes absent from COMPONENTS.md: " + ", ".join(extra))
    return errors


def main() -> int:
    errors = validate_catalog_against_components()
    if errors:
        for error in errors:
            print(error)
        return 1
    catalog = load_catalog()
    print(f"OK: {len(catalog_classes(catalog))} ARA classes in {DEFAULT_CATALOG_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
