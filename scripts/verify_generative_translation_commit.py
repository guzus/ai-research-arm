#!/usr/bin/env python3
"""Verify the exact committed output of one generative translation backfill."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import uuid
from pathlib import Path


def _changed(repo: Path, base_sha: str) -> list[tuple[str, str]]:
    raw = subprocess.check_output(
        ["git", "-C", str(repo), "diff", "--name-status", "--no-renames", "-z", f"{base_sha}..HEAD"]
    )
    parts = raw.split(b"\0")
    return [
        (parts[i].decode("utf-8"), parts[i + 1].decode("utf-8"))
        for i in range(0, len(parts) - 1, 2)
        if parts[i]
    ]


def verify(
    repo: Path,
    base_sha: str,
    slug: str,
    source_type: str,
    source_file: str,
    source_sha256: str,
    model: str,
    translation_type: str = "ara",
) -> dict[str, str]:
    entries = _changed(repo, base_sha)
    if source_type not in {"ara", "html"}:
        raise ValueError(f"unknown source type: {source_type!r}")
    if translation_type not in {"ara", "html"}:
        raise ValueError(f"unknown translation type: {translation_type!r}")
    expected_count = 3 if translation_type == "ara" else 2
    if len(entries) != expected_count:
        raise ValueError(f"expected {expected_count} committed paths, got {entries}")

    index_path = "research/generative/index.json"
    if ("M", index_path) not in entries:
        raise ValueError("translation commit must modify research/generative/index.json")
    added = [path for status, path in entries if status == "A"]
    if len(added) != expected_count - 1 or any(status not in {"A", "M"} for status, _ in entries):
        raise ValueError(f"translation commit has forbidden path statuses: {entries}")

    rows = json.loads((repo / index_path).read_text(encoding="utf-8"))
    matches = [row for row in rows if isinstance(row, dict) and row.get("slug") == slug]
    if len(matches) != 1:
        raise ValueError(f"expected one index row for {slug!r}, found {len(matches)}")
    translation = (matches[0].get("translations") or {}).get("ko")
    if not isinstance(translation, dict):
        raise ValueError("index row has no translations.ko object")

    html_path = f"research/generative/{translation.get('file', '')}"
    if html_path not in added or not html_path.endswith(f"--{slug}.ko.html"):
        raise ValueError(f"translations.ko.file does not name the added Korean HTML: {html_path}")
    if translation.get("language") != "ko" or translation.get("model") != model:
        raise ValueError("translation language/model provenance does not match the workflow")
    if translation.get("source_file") != source_file:
        raise ValueError("translation source_file provenance does not match preflight")
    if translation.get("source_sha256") != source_sha256:
        raise ValueError("translation source_sha256 provenance does not match preflight")
    if not translation.get("translated_at"):
        raise ValueError("translation has no translated_at timestamp")

    source_artifact_path = ""
    if translation_type == "ara":
        source_artifact_path = html_path.removesuffix(".html") + ".ara.md"
        if source_artifact_path not in added:
            raise ValueError("translation commit lacks the matching Korean ARA source")

    return {
        "html_path": html_path,
        "source_artifact_path": source_artifact_path,
        "allowed_paths": "\n".join([index_path, html_path, *([source_artifact_path] if source_artifact_path else [])]),
    }


def _write_outputs(path: Path, values: dict[str, str]) -> None:
    with path.open("a", encoding="utf-8") as out:
        for key, value in values.items():
            if "\n" not in value:
                out.write(f"{key}={value}\n")
                continue
            marker = f"__ARA_VERIFY_{uuid.uuid4().hex}__"
            out.write(f"{key}<<{marker}\n{value}\n{marker}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--source-type", choices=("ara", "html"), required=True)
    parser.add_argument("--source-file", required=True)
    parser.add_argument("--source-sha256", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--translation-type", choices=("ara", "html"), default="ara")
    parser.add_argument("--github-output")
    args = parser.parse_args(argv)
    values = verify(
        Path(args.repo_root).resolve(),
        args.base_sha,
        args.slug,
        args.source_type,
        args.source_file,
        args.source_sha256,
        args.model,
        args.translation_type,
    )
    output = args.github_output or os.environ.get("GITHUB_OUTPUT")
    if output:
        _write_outputs(Path(output), values)
    print(f"verified Korean translation commit: {values['html_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
