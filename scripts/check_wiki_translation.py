#!/usr/bin/env python3
"""Validate localized Wiki mirrors without mutating the English CRUD graph.

Korean Wiki pages live under ``research/wiki-translations/ko/``.  Each file
points at one canonical English page and records its SHA-256.  That makes a
source edit fail CI until the translation is reviewed, instead of silently
serving stale Korean copy.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import check_wiki as cw


REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "research" / "wiki"
TRANSLATION_ROOT = REPO_ROOT / "research" / "wiki-translations" / "ko"
ALLOWED_FIELDS = {
    "slug",
    "language",
    "source_file",
    "source_sha256",
    "title",
    "description",
    "images",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
HANGUL_RE = re.compile(r"[가-힣]")
URL_RE = re.compile(r"https?://[^\s<>\"'()\]}]+")
NUMBER_RE = re.compile(
    r"(?<!\d)[+\-−]?(?:[$€£₩¥]\s*)?(?:\d{1,3}(?:,\d{3})+|\d+)"
    r"(?:\.\d+)?(?:%|×|x)?(?!\d)"
)
LATIN_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z'-]*\b")
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")


@dataclass(frozen=True)
class WikiTranslation:
    path: Path
    slug: str
    title: str
    description: str
    body: str
    source_path: Path
    source_file: str
    source_sha256: str
    images: list[dict[str, str]]

    def index_doc(self, translation_root: Path) -> dict[str, Any]:
        doc: dict[str, Any] = {
            "title": self.title,
            "summary": self.description,
            "description": self.description,
            "file": str(Path("wiki-translations") / "ko" / self.path.relative_to(translation_root)),
            "source_file": self.source_file,
            "source_sha256": self.source_sha256,
        }
        if self.images:
            doc["images"] = self.images
        return doc


def _split(path: Path, errors: list[str]) -> tuple[dict[str, Any], str]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read file: {exc}")
        return {}, ""
    report = cw.Report()
    data, body = cw._split_frontmatter(raw, path, report)
    errors.extend(f"{failure.field}: {failure.msg}" for failure in report.failures)
    return (data or {}), body


def _text(value: Any, field: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field}: must be a non-empty string")
        return ""
    return value.strip()


def _counter(pattern: re.Pattern[str], text: str) -> collections.Counter[str]:
    return collections.Counter(match.rstrip(".,;:!?") for match in pattern.findall(text))


def _fenced_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] | None = None
    marker = ""
    indent = ""
    for line in text.splitlines(keepends=True):
        match = FENCE_RE.match(line)
        if current is None:
            if match:
                current = [line]
                marker = match.group(2)
                indent = match.group(1)
        else:
            current.append(line)
            if (
                match
                and match.group(1) == indent
                and match.group(2)[0] == marker[0]
                and len(match.group(2)) >= len(marker)
                and not line[match.end() :].strip()
            ):
                blocks.append("".join(current))
                current = None
    if current is not None:
        blocks.append("".join(current))
    return blocks


def _visible_text(text: str) -> str:
    lines: list[str] = []
    fenced = False
    marker = ""
    indent = ""
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if not fenced:
            if match:
                fenced = True
                marker = match.group(2)
                indent = match.group(1)
                continue
            lines.append(line)
        elif (
            match
            and match.group(1) == indent
            and match.group(2)[0] == marker[0]
            and len(match.group(2)) >= len(marker)
            and not line[match.end() :].strip()
        ):
            fenced = False
    return "\n".join(lines)


def _english_ngrams(text: str, size: int = 5) -> collections.Counter[tuple[str, ...]]:
    tokens = [
        token
        for token in LATIN_WORD_RE.findall(_visible_text(text))
        if token.islower() and len(token) >= 3
    ]
    return collections.Counter(
        tuple(tokens[index : index + size])
        for index in range(max(0, len(tokens) - size + 1))
    )


def _validate_images(
    source_images: list[dict[str, str]], value: Any, errors: list[str]
) -> list[dict[str, str]]:
    if value is None:
        return []
    images = cw.normalize_images(value)
    if not isinstance(value, list) or len(images) != len(value):
        errors.append("images: every item requires valid url and alt strings")
        return []
    if len(images) != len(source_images):
        errors.append("images: count must match the canonical source")
        return images
    for index, (source, target) in enumerate(zip(source_images, images, strict=True)):
        for key in ("url", "credit", "source_url"):
            if source.get(key) != target.get(key):
                errors.append(f"images[{index}].{key}: must match the canonical source")
        if not HANGUL_RE.search(target.get("alt", "")):
            errors.append(f"images[{index}].alt: Korean alt text is required")
        if source.get("caption") and not HANGUL_RE.search(target.get("caption", "")):
            errors.append(f"images[{index}].caption: Korean caption is required")
    return images


def validate_file(
    path: Path,
    *,
    wiki_dir: Path = WIKI_DIR,
    translation_root: Path = TRANSLATION_ROOT,
) -> tuple[WikiTranslation | None, list[str]]:
    errors: list[str] = []
    try:
        relative = path.relative_to(translation_root)
    except ValueError:
        return None, ["path is outside the Korean translation root"]
    if len(relative.parts) != 2 or relative.parts[0] not in cw.PAGE_SUBDIRS:
        errors.append("path must be <entities|concepts|themes>/<slug>.md")

    data, body = _split(path, errors)
    extra = set(data) - ALLOWED_FIELDS
    if extra:
        errors.append(f"frontmatter: unknown keys {sorted(extra)}")
    missing = ALLOWED_FIELDS - {"images"} - set(data)
    if missing:
        errors.append(f"frontmatter: missing keys {sorted(missing)}")

    slug = _text(data.get("slug"), "slug", errors)
    language = _text(data.get("language"), "language", errors)
    source_file = _text(data.get("source_file"), "source_file", errors)
    source_sha256 = _text(data.get("source_sha256"), "source_sha256", errors)
    title = _text(data.get("title"), "title", errors)
    description = _text(data.get("description"), "description", errors)

    if language and language != "ko":
        errors.append("language: must be 'ko'")
    if slug and (path.stem != slug or not cw.SLUG_RE.fullmatch(slug)):
        errors.append("slug: must match the translation filename")
    if source_sha256 and not SHA256_RE.fullmatch(source_sha256):
        errors.append("source_sha256: must be 64 lowercase hex characters")

    repo_prefix = "research/wiki/"
    source_path = Path()
    if source_file:
        if not source_file.startswith(repo_prefix):
            errors.append("source_file: must start with research/wiki/")
        else:
            source_relative = Path(source_file.removeprefix(repo_prefix))
            if (
                source_relative.is_absolute()
                or ".." in source_relative.parts
                or len(source_relative.parts) != 2
                or source_relative.parts[0] not in cw.PAGE_SUBDIRS
                or source_relative.suffix != ".md"
            ):
                errors.append("source_file: unsafe or non-canonical wiki path")
            else:
                source_path = wiki_dir / source_relative
                if source_relative != relative:
                    errors.append("source_file: path must mirror the translation path")
    if not source_path.is_file():
        errors.append("source_file: canonical source does not exist")
        return None, errors

    source_raw = source_path.read_bytes()
    actual_sha = hashlib.sha256(source_raw).hexdigest()
    if source_sha256 and actual_sha != source_sha256:
        errors.append(
            "source_sha256: canonical source changed; refresh the translation "
            f"({source_sha256} != {actual_sha})"
        )

    source_report = cw.Report()
    source_data, source_body = cw._split_frontmatter(
        source_raw.decode("utf-8"), source_path, source_report
    )
    if source_report.failures or not source_data:
        errors.append("source_file: canonical source frontmatter is invalid")
        return None, errors
    if source_data.get("slug") != slug:
        errors.append("slug: does not match canonical source")

    source_images = cw.normalize_images(source_data.get("images"))
    images = _validate_images(source_images, data.get("images"), errors)
    if source_images and data.get("images") is None:
        errors.append("images: translated metadata is required when the source has images")

    source_visible = "\n".join(
        [str(source_data.get("title") or ""), str(source_data.get("description") or ""), source_body]
    )
    target_visible = "\n".join([title, description, body])
    if _counter(URL_RE, source_visible) != _counter(URL_RE, target_visible):
        errors.append("content: URL multiset changed")
    if _counter(NUMBER_RE, source_visible) != _counter(NUMBER_RE, target_visible):
        errors.append("content: numeric-token multiset changed")
    if collections.Counter(cw.extract_wikilinks(source_body)) != collections.Counter(
        cw.extract_wikilinks(body)
    ):
        errors.append("body: wikilink target multiset changed")
    if _fenced_blocks(source_body) != _fenced_blocks(body):
        errors.append("body: fenced code blocks must remain byte-identical")

    source_ngrams = _english_ngrams(source_visible)
    if sum(source_ngrams.values()) >= 20:
        target_ngrams = _english_ngrams(target_visible)
        reused = sum((source_ngrams & target_ngrams).values())
        reuse_share = reused / sum(source_ngrams.values())
        if reuse_share > 0.35:
            errors.append(
                "content: too much visible English prose was copied unchanged "
                f"({reuse_share:.0%} of source lowercase 5-grams)"
            )
    source_words = len(LATIN_WORD_RE.findall(_visible_text(source_visible)))
    hangul = len(HANGUL_RE.findall(target_visible))
    minimum_hangul = min(200, max(8, (source_words + 9) // 10))
    if hangul < minimum_hangul:
        errors.append(
            f"content: too little Korean prose ({hangul} syllables; need {minimum_hangul})"
        )

    if errors:
        return None, errors
    return (
        WikiTranslation(
            path=path,
            slug=slug,
            title=title,
            description=description,
            body=body,
            source_path=source_path,
            source_file=source_file,
            source_sha256=source_sha256,
            images=images,
        ),
        [],
    )


def gather(root: Path) -> list[Path]:
    return [
        path
        for subdir in cw.PAGE_SUBDIRS
        for path in sorted((root / subdir).glob("*.md"))
        if path.is_file()
    ]


def load_all(
    *, wiki_dir: Path = WIKI_DIR, translation_root: Path = TRANSLATION_ROOT
) -> tuple[dict[str, WikiTranslation], list[tuple[Path, str]]]:
    translations: dict[str, WikiTranslation] = {}
    failures: list[tuple[Path, str]] = []
    if not translation_root.is_dir():
        return translations, failures
    for path in gather(translation_root):
        translation, errors = validate_file(
            path, wiki_dir=wiki_dir, translation_root=translation_root
        )
        failures.extend((path, error) for error in errors)
        if translation:
            if translation.slug in translations:
                failures.append((path, f"duplicate translation for {translation.slug!r}"))
            else:
                translations[translation.slug] = translation
    return translations, failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--wiki-root", default=str(WIKI_DIR))
    parser.add_argument("--root", default=str(TRANSLATION_ROOT))
    args = parser.parse_args(argv)
    wiki_dir = Path(args.wiki_root)
    root = Path(args.root)

    if args.paths:
        failures: list[tuple[Path, str]] = []
        valid = 0
        for raw_path in args.paths:
            path = Path(raw_path)
            translation, errors = validate_file(
                path, wiki_dir=wiki_dir, translation_root=root
            )
            failures.extend((path, error) for error in errors)
            valid += int(translation is not None)
    else:
        translations, failures = load_all(wiki_dir=wiki_dir, translation_root=root)
        valid = len(translations)

    for path, error in failures:
        print(f"FAIL {path}: {error}", file=sys.stderr)
    if failures:
        print(f"\n{len(failures)} failure(s)", file=sys.stderr)
        return 1
    print(f"OK — {valid} Korean wiki translation(s) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
