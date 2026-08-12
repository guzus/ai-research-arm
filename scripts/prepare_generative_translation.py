#!/usr/bin/env python3
"""Resolve one English generative article into a safe Korean backfill request.

This is trusted preflight code for ``translate-generative-research.yml``.  It
does not translate or mutate the research store.  It validates the user-owned
slug, rejects accidental replacement, requires the canonical ARA source, and
emits the exact source/draft/output contract consumed by later workflow steps.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import uuid
from pathlib import Path


SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,119}$")
AGENT_INPUT_DIR = Path(".agent-input")
REQUEST_PATH = AGENT_INPUT_DIR / "translation.json"


def _regular_file(path: Path, root: Path) -> bool:
    return (
        path.is_file()
        and not path.is_symlink()
        and path.resolve().parent == root.resolve()
    )


def prepare(repo: Path, slug: str, *, force: bool) -> dict[str, str]:
    if not SLUG_RE.fullmatch(slug) or slug in {".", ".."}:
        raise ValueError(f"invalid generative article slug: {slug!r}")

    gen_dir = repo / "research" / "generative"
    index_path = gen_dir / "index.json"
    try:
        rows = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read generative index: {exc}") from exc
    if not isinstance(rows, list):
        raise ValueError("generative index must be a JSON array")

    matches = [
        row for row in rows if isinstance(row, dict) and row.get("slug") == slug
    ]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one index row for {slug!r}, found {len(matches)}")
    row = matches[0]
    if (row.get("kind") or "fragment") != "fragment":
        raise ValueError("Korean backfill currently supports fragment articles only")
    if row.get("language") not in (None, "en"):
        raise ValueError(f"translation source must be English, got {row.get('language')!r}")
    translations = row.get("translations")
    if translations is not None and not isinstance(translations, dict):
        raise ValueError(f"index row for {slug!r} has malformed translations metadata")
    if isinstance(translations, dict) and "ko" in translations and not force:
        raise ValueError(
            f"Korean translation already exists for {slug!r}; "
            "dispatch with overwrite=true to replace it"
        )

    filename = row.get("file")
    if (
        not isinstance(filename, str)
        or Path(filename).name != filename
        or not filename.endswith(".html")
    ):
        raise ValueError(f"index row has unsafe or unsupported source file: {filename!r}")
    html_path = gen_dir / filename
    if not _regular_file(html_path, gen_dir):
        raise ValueError(f"canonical HTML source is missing or unsafe: {html_path}")
    ara_path = html_path.with_suffix(".ara.md")
    if not _regular_file(ara_path, gen_dir):
        raise ValueError(
            "canonical ARA source is missing; legacy HTML-only articles are "
            "not supported by the Korean backfill workflow"
        )
    source_path = ara_path
    source_type = "ara"
    draft_path = Path(".tmp/generative-translation.ko.html")
    result_path = Path(".tmp/generative-translation.ko.segments.jsonl")

    title = row.get("title")
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"index row for {slug!r} has no title")
    source_rel = source_path.relative_to(repo).as_posix()
    source_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()
    return {
        "slug": slug,
        "title": title.strip(),
        "source_path": source_rel,
        "source_type": source_type,
        "source_sha256": source_sha256,
        "draft_path": draft_path.as_posix(),
        "result_path": result_path.as_posix(),
        "translation_type": "html",
    }


def _atomic_write(path: Path, payload: bytes) -> None:
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError(f"refusing unsafe staged input path: {path}")
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def stage_agent_request(
    repo: Path, values: dict[str, str], request_file: str
) -> dict[str, str]:
    """Stage the minimum model-visible input under one canonical directory."""
    if Path(request_file) != REQUEST_PATH:
        raise ValueError(f"request file must be exactly {REQUEST_PATH.as_posix()!r}")
    input_dir = repo / AGENT_INPUT_DIR
    if input_dir.is_symlink() or (input_dir.exists() and not input_dir.is_dir()):
        raise ValueError(f"refusing unsafe agent input directory: {input_dir}")
    input_dir.mkdir(exist_ok=True)
    if input_dir.resolve() != repo.resolve() / AGENT_INPUT_DIR:
        raise ValueError(f"agent input directory is noncanonical: {input_dir}")

    request_values = dict(values)
    request_values.pop("source_path")
    request_payload = (
        json.dumps(request_values, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")
    _atomic_write(repo / REQUEST_PATH, request_payload)
    return request_values


def _write_github_output(path: Path, values: dict[str, str]) -> None:
    with path.open("a", encoding="utf-8") as out:
        for key, value in values.items():
            if "\n" not in value:
                out.write(f"{key}={value}\n")
                continue
            marker = f"__ARA_TRANSLATION_{uuid.uuid4().hex}__"
            out.write(f"{key}<<{marker}\n{value}\n{marker}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--force", choices=("true", "false"), default="false")
    parser.add_argument("--request-file", required=True)
    parser.add_argument("--github-output")
    args = parser.parse_args(argv)

    repo = Path(args.repo_root).resolve()
    values = prepare(repo, args.slug, force=args.force == "true")
    stage_agent_request(repo, values, args.request_file)
    (repo / ".tmp").mkdir(exist_ok=True)
    output_path = Path(args.github_output or os.environ.get("GITHUB_OUTPUT", ""))
    if str(output_path):
        _write_github_output(output_path, values)
    print(
        f"translation source: {values['source_path']} ({values['source_type']}); "
        f"title: {values['title']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
