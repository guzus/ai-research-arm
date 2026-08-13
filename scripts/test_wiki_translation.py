#!/usr/bin/env python3
"""Tests for the locale mirror contract in check_wiki_translation.py."""

import hashlib
import tempfile
import unittest
from pathlib import Path

import build_wiki_index as bwi
import check_wiki_translation as cwt
from test_build_wiki_index import ALPHA, BETA, LOG, _write


def _fixture(root: Path) -> tuple[Path, Path]:
    wiki = root / "wiki"
    translations = root / "wiki-translations" / "ko"
    _write(wiki, "entities/alpha.md", ALPHA)
    _write(wiki, "concepts/beta.md", BETA)
    _write(wiki, "log.md", LOG)
    return wiki, translations


def _translation(source: Path) -> str:
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    return f"""---
slug: alpha
language: ko
source_file: research/wiki/entities/alpha.md
source_sha256: {digest}
title: 알파 코퍼레이션
description: 알파 인프라 기업을 설명하는 한국어 위키 페이지입니다.
images:
  - url: "https://example.com/alpha-datacenter.jpg"
    alt: "알파 데이터센터의 인프라 랙"
    caption: "알파 인프라를 보여 주는 사진"
    credit: "Alpha"
    source_url: "https://example.com/alpha-media"
---
알파는 [[beta]]와 연결되며, 별칭 링크 [[b-one|베타]]로도 이어집니다.
"""


class WikiTranslationTest(unittest.TestCase):
    def test_valid_translation_is_attached_to_index(self):
        with tempfile.TemporaryDirectory() as td:
            wiki, translations = _fixture(Path(td))
            target = translations / "entities" / "alpha.md"
            _write(translations, "entities/alpha.md", _translation(wiki / "entities" / "alpha.md"))

            translation, errors = cwt.validate_file(
                target, wiki_dir=wiki, translation_root=translations
            )
            self.assertEqual(errors, [])
            self.assertIsNotNone(translation)

            index = bwi.build_index(wiki, translations)
            alpha = next(page for page in index["pages"] if page["slug"] == "alpha")
            ko = alpha["translations"]["ko"]
            self.assertEqual(ko["title"], "알파 코퍼레이션")
            self.assertEqual(ko["file"], "wiki-translations/ko/entities/alpha.md")
            self.assertEqual(ko["source_file"], "research/wiki/entities/alpha.md")

    def test_source_change_invalidates_translation(self):
        with tempfile.TemporaryDirectory() as td:
            wiki, translations = _fixture(Path(td))
            target = translations / "entities" / "alpha.md"
            _write(translations, "entities/alpha.md", _translation(wiki / "entities" / "alpha.md"))
            _write(wiki, "entities/alpha.md", ALPHA.replace("Alpha description.", "Changed description."))
            _, errors = cwt.validate_file(
                target, wiki_dir=wiki, translation_root=translations
            )
            self.assertTrue(any("canonical source changed" in error for error in errors))

    def test_wikilinks_urls_and_numbers_are_immutable(self):
        with tempfile.TemporaryDirectory() as td:
            wiki, translations = _fixture(Path(td))
            source = wiki / "entities" / "alpha.md"
            target = translations / "entities" / "alpha.md"
            valid = _translation(source)
            _write(translations, "entities/alpha.md", valid.replace("[[beta]]", "[[alpha]]"))
            _, errors = cwt.validate_file(
                target, wiki_dir=wiki, translation_root=translations
            )
            self.assertTrue(any("wikilink target multiset changed" in error for error in errors))

    def test_english_copy_through_with_korean_blob_fails(self):
        with tempfile.TemporaryDirectory() as td:
            wiki, translations = _fixture(Path(td))
            source = wiki / "entities" / "alpha.md"
            source.write_text(
                ALPHA.replace(
                    "Alpha links to [[beta]] and again via alias [[b-one|Beta]].",
                    " ".join(["ordinary lowercase prose remains copied from the source"] * 30)
                    + " [[beta]] [[b-one|Beta]].",
                ),
                encoding="utf-8",
            )
            target = translations / "entities" / "alpha.md"
            copied_body = source.read_text(encoding="utf-8").split("\n---\n", 1)[1]
            translated = _translation(source).rsplit("\n---\n", 1)[0] + "\n---\n" + copied_body + ("가" * 200)
            _write(translations, "entities/alpha.md", translated)
            _, errors = cwt.validate_file(
                target, wiki_dir=wiki, translation_root=translations
            )
            self.assertTrue(any("copied unchanged" in error for error in errors))

    def test_cli_accepts_repo_relative_translation_path(self):
        with tempfile.TemporaryDirectory() as td:
            wiki, translations = _fixture(Path(td))
            target = translations / "entities" / "alpha.md"
            _write(translations, "entities/alpha.md", _translation(wiki / "entities" / "alpha.md"))
            self.assertEqual(
                cwt.main(
                    [
                        "--wiki-root",
                        str(wiki),
                        "--root",
                        str(translations),
                        str(target),
                    ]
                ),
                0,
            )


if __name__ == "__main__":
    unittest.main()
