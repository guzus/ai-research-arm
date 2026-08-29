#!/usr/bin/env python3
"""Atomically attach methodology sidecars and the rebuilt claim index.

The Git commit is the publication transaction: a commit may contain both the
new claim ledger and the index derived from it, or neither.  This helper amends
the writer-owned article commit only after every file is present and the index
has been rebuilt, then verifies the committed result before returning.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import build_claim_index as claims


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(repo), *args], check=check, text=True, capture_output=True)


def _atomic_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as out, source.open("rb") as incoming:
            shutil.copyfileobj(incoming, out)
        os.replace(temporary, target)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def _restore_owned(repo: Path, snapshots: dict[Path, bytes | None]) -> None:
    """Restore only files this helper owns; never reset unrelated checkout state."""
    rels = [str(path.relative_to(repo)) for path in snapshots]
    _git(repo, "restore", "--staged", "--", *rels, check=False)
    for target, previous in snapshots.items():
        if previous is None:
            target.unlink(missing_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.", suffix=".restore")
            try:
                with os.fdopen(fd, "wb") as out:
                    out.write(previous)
                os.replace(temporary, target)
            except BaseException:
                Path(temporary).unlink(missing_ok=True)
                raise


def finalize(repo: Path, article_file: str, ledger: Path, verification: Path, redteam: Path) -> list[Path]:
    repo = repo.resolve()
    if _git(repo, "diff", "--cached", "--quiet", check=False).returncode != 0:
        raise RuntimeError("refusing to amend while unrelated changes are already staged")
    article = repo / "research" / "generative" / article_file
    if article.parent != repo / "research" / "generative" or article.suffix != ".html" or not article.is_file():
        raise ValueError("article-file must name an existing top-level generative .html artifact")
    stem = article.stem
    inputs = (ledger.resolve(), verification.resolve(), redteam.resolve())
    if not all(path.is_file() for path in inputs):
        raise ValueError("ledger, verification, and redteam inputs must all exist")

    targets = [
        repo / "research" / "generative" / f"{stem}.claims.json",
        repo / "research" / "generative" / f"{stem}.verification.json",
        repo / "research" / "generative" / f"{stem}.redteam.json",
    ]
    index_path = repo / "research" / "claims" / "index.json"
    owned = [*targets, index_path]
    dirty = _git(repo, "status", "--porcelain", "--", *(str(p.relative_to(repo)) for p in owned)).stdout.strip()
    if dirty:
        raise RuntimeError(f"refusing to overwrite dirty transactional path(s):\n{dirty}")
    for source in inputs:
        payload = json.loads(source.read_text(encoding="utf-8"))
        if source == inputs[0] and not isinstance(payload.get("claims") if isinstance(payload, dict) else None, list):
            raise ValueError("claims ledger must contain claims[]")
    snapshots = {target: target.read_bytes() if target.exists() else None for target in owned}
    try:
        for source, target in zip(inputs, targets):
            _atomic_copy(source, target)
        claims._atomic_write(index_path, claims.render(claims.build_index(article.parent)))
        rels = [str(path.relative_to(repo)) for path in [*targets, index_path]]
        _git(repo, "add", "--", *rels)
        if _git(repo, "diff", "--cached", "--quiet", check=False).returncode == 0:
            raise RuntimeError("methodology finalization produced no staged changes")
        expected = claims.render(claims.build_index(article.parent))
        staged_index = _git(repo, "show", f":{index_path.relative_to(repo)}").stdout
        if staged_index != expected:
            raise RuntimeError("staged claim index does not match staged ledgers")
        staged = set(_git(repo, "diff", "--cached", "--name-only").stdout.splitlines())
        # An empty ledger can legitimately leave the derived index byte-for-byte
        # identical. `git add` still stages the path transactionally, but Git has
        # no diff entry for unchanged content, so only new sidecars are mandatory.
        missing = set(rels[:3]) - staged
        if missing:
            raise RuntimeError(f"staged transaction omitted path(s): {sorted(missing)}")
        # Final action: all fallible validation is complete. Git updates the
        # commit ref atomically; no broad checkout rollback is ever needed.
        _git(repo, "commit", "--amend", "--no-edit")
        return [*targets, index_path]
    except BaseException:
        _restore_owned(repo, snapshots)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--article-file", required=True)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--verification", required=True)
    parser.add_argument("--redteam", required=True)
    args = parser.parse_args(argv)
    paths = finalize(Path(args.repo), args.article_file, Path(args.ledger), Path(args.verification), Path(args.redteam))
    print("finalized transactional publication: " + ", ".join(str(p.relative_to(Path(args.repo).resolve())) for p in paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
