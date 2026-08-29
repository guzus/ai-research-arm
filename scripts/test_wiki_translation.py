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
            self.assertNotIn("stale", ko)

    def test_source_change_marks_translation_stale_not_invalid(self):
        # An English edit to a mirrored page is the daily ingest lane's normal
        # output. It must degrade the mirror to STALE — never fail validation,
        # or build_wiki_index dies inside a workflow whose allowed-paths
        # forbid touching the mirror (the 2026-08-20 wiki-lane deadlock).
        with tempfile.TemporaryDirectory() as td:
            wiki, translations = _fixture(Path(td))
            target = translations / "entities" / "alpha.md"
            _write(translations, "entities/alpha.md", _translation(wiki / "entities" / "alpha.md"))
            _write(wiki, "entities/alpha.md", ALPHA.replace("Alpha description.", "Changed description."))
            translation, errors = cwt.validate_file(
                target, wiki_dir=wiki, translation_root=translations
            )
            self.assertEqual(errors, [])
            self.assertIsNotNone(translation)
            self.assertTrue(translation.stale)

            # The index still attaches the mirror, flagged for the dashboard.
            index = bwi.build_index(wiki, translations)
            alpha = next(page for page in index["pages"] if page["slug"] == "alpha")
            self.assertIs(alpha["translations"]["ko"]["stale"], True)

    def test_stale_translation_fails_only_under_strict(self):
        with tempfile.TemporaryDirectory() as td:
            wiki, translations = _fixture(Path(td))
            _write(translations, "entities/alpha.md", _translation(wiki / "entities" / "alpha.md"))
            _write(wiki, "entities/alpha.md", ALPHA.replace("Alpha description.", "Changed description."))
            common = ["--wiki-root", str(wiki), "--root", str(translations)]
            self.assertEqual(cwt.main(common), 0)
            self.assertEqual(cwt.main(common + ["--strict"]), 1)

    def test_stale_mirror_still_requires_korean_content(self):
        # Target-only checks must not be skippable via staleness: a stale
        # mirror whose body was replaced with English (or emptied) fails.
        with tempfile.TemporaryDirectory() as td:
            wiki, translations = _fixture(Path(td))
            target = translations / "entities" / "alpha.md"
            anglicized = _translation(wiki / "entities" / "alpha.md").replace(
                "알파는 [[beta]]와 연결되며, 별칭 링크 [[b-one|베타]]로도 이어집니다.",
                "Alpha links to beta.",
            ).replace("title: 알파 코퍼레이션", "title: Alpha Corp").replace(
                "description: 알파 인프라 기업을 설명하는 한국어 위키 페이지입니다.",
                "description: An English description.",
            ).replace('alt: "알파 데이터센터의 인프라 랙"', 'alt: "Alpha datacenter racks"').replace(
                'caption: "알파 인프라를 보여 주는 사진"', 'caption: "Alpha infra photo"'
            )
            _write(translations, "entities/alpha.md", anglicized)
            _write(wiki, "entities/alpha.md", ALPHA.replace("Alpha description.", "Changed description."))
            translation, errors = cwt.validate_file(
                target, wiki_dir=wiki, translation_root=translations
            )
            self.assertIsNone(translation)
            self.assertTrue(any("too little Korean prose" in error for error in errors))
            self.assertTrue(any("Korean alt text is required" in error for error in errors))

    def test_growing_source_never_fails_a_stale_mirror(self):
        # The stale-branch Hangul floor must be source-independent: a large
        # English expansion (which raises the fresh-mode floor) must not flip
        # a legitimately stale mirror to failing — that would recreate the
        # ingest-lane deadlock.
        with tempfile.TemporaryDirectory() as td:
            wiki, translations = _fixture(Path(td))
            target = translations / "entities" / "alpha.md"
            _write(translations, "entities/alpha.md", _translation(wiki / "entities" / "alpha.md"))
            grown = ALPHA.replace(
                "Alpha description.",
                "Changed. " + " ".join(["expanded english prose"] * 800),
            )
            _write(wiki, "entities/alpha.md", grown)
            translation, errors = cwt.validate_file(
                target, wiki_dir=wiki, translation_root=translations
            )
            self.assertEqual(errors, [])
            self.assertIsNotNone(translation)
            self.assertTrue(translation.stale)

    def test_structural_defect_fails_even_when_stale(self):
        with tempfile.TemporaryDirectory() as td:
            wiki, translations = _fixture(Path(td))
            target = translations / "entities" / "alpha.md"
            broken = _translation(wiki / "entities" / "alpha.md").replace(
                "language: ko", "language: ja"
            )
            _write(translations, "entities/alpha.md", broken)
            _write(wiki, "entities/alpha.md", ALPHA.replace("Alpha description.", "Changed description."))
            translation, errors = cwt.validate_file(
                target, wiki_dir=wiki, translation_root=translations
            )
            self.assertIsNone(translation)
            self.assertTrue(any("language: must be 'ko'" in error for error in errors))

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

    def test_dropped_list_item_fails_structure_gate(self):
        with tempfile.TemporaryDirectory() as td:
            wiki, translations = _fixture(Path(td))
            source = wiki / "entities" / "alpha.md"
            source.write_text(
                ALPHA.replace(
                    "Alpha links to [[beta]] and again via alias [[b-one|Beta]].",
                    "## Details\n\n- First claim\n- Second claim\n"
                    "\nAlpha links to [[beta]] and again via alias [[b-one|Beta]].",
                ),
                encoding="utf-8",
            )
            target = translations / "entities" / "alpha.md"
            translated = _translation(source).replace(
                "알파는 [[beta]]와 연결되며, 별칭 링크 [[b-one|베타]]로도 이어집니다.",
                "## 세부 정보\n\n- 첫 번째 주장\n"
                "\n알파는 [[beta]]와 연결되며, 별칭 링크 [[b-one|베타]]로도 이어집니다.",
            )
            _write(translations, "entities/alpha.md", translated)
            _, errors = cwt.validate_file(
                target, wiki_dir=wiki, translation_root=translations
            )
            self.assertTrue(any("heading/list structure changed" in error for error in errors))

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
