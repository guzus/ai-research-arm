#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import check_generative_translation as parity
import prepare_generative_translation as prepare
import verify_generative_translation_commit as verifier
import write_generative_research as writer


SOURCE = """---
title: Alpha costs $12 in 2026
deck: Source deck with a stable number.
---

## 01. Alpha

Alpha costs $12 in 2026 and links to [the source](https://example.com/a) [^1].

:::callout(kind=info, label=Note)
The measured gain is 25% [^1].
:::

:::references
- {id: 1, title: "Primary source", url: "https://example.com/a"}
:::
"""

KOREAN = """---
title: 2026년 알파 가격은 $12
deck: 안정적인 수치를 담은 원문 설명입니다.
---

## 01. 알파

알파의 2026년 가격은 $12이며 [원문](https://example.com/a)에서 확인할 수 있습니다 [^1].

:::callout(kind=info, label=참고)
측정된 향상률은 25%입니다 [^1].
:::

:::references
- {id: 1, title: "원출처", url: "https://example.com/a"}
:::
"""


def seed_repo(root: Path, *, translated: bool = False, ara: bool = True) -> tuple[Path, dict]:
    gen = root / "research" / "generative"
    gen.mkdir(parents=True)
    html_name = "2026-01-01T000000--alpha.html"
    (gen / html_name).write_text(
        '<article class="ara-doc"><h2 class="ara-display">Alpha</h2><p>Body.</p></article>\n',
        encoding="utf-8",
    )
    if ara:
        (gen / html_name.replace(".html", ".ara.md")).write_text(SOURCE, encoding="utf-8")
    row = {
        "slug": "alpha",
        "file": html_name,
        "kind": "fragment",
        "language": "en",
        "title": "Alpha",
        "model": "seed",
        "created_at": "2026-01-01T00:00:00Z",
        "source": "seed",
        "prompt": "Alpha",
        "tags": ["semiconductors", "cost"],
    }
    if translated:
        row["translations"] = {"ko": {"file": "old--alpha.ko.html", "language": "ko"}}
    (gen / "index.json").write_text(json.dumps([row]) + "\n", encoding="utf-8")
    return gen, row


class TranslationPreparationTest(unittest.TestCase):
    def test_prefers_ara_and_emits_source_hash(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gen, _ = seed_repo(root)
            values = prepare.prepare(root, "alpha", force=False)
            source = gen / "2026-01-01T000000--alpha.ara.md"
            self.assertEqual(values["source_type"], "ara")
            self.assertEqual(values["source_path"], "research/generative/2026-01-01T000000--alpha.ara.md")
            self.assertEqual(values["source_sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertTrue(values["draft_path"].endswith(".ko.ara.md"))

    def test_uses_html_for_legacy_article(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_repo(root, ara=False)
            values = prepare.prepare(root, "alpha", force=False)
            self.assertEqual(values["source_type"], "html")
            self.assertTrue(values["draft_path"].endswith(".ko.html"))

    def test_rejects_existing_translation_without_force(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_repo(root, translated=True)
            with self.assertRaisesRegex(ValueError, "already exists"):
                prepare.prepare(root, "alpha", force=False)
            self.assertEqual(prepare.prepare(root, "alpha", force=True)["slug"], "alpha")

    def test_rejects_unsafe_or_unknown_slug(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_repo(root)
            for slug in ("../alpha", "ALPHA", "missing"):
                with self.subTest(slug=slug), self.assertRaises(ValueError):
                    prepare.prepare(root, slug, force=False)


class TranslationParityTest(unittest.TestCase):
    def test_faithful_korean_translation_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "alpha.ara.md"
            target = root / "alpha.ko.ara.md"
            source.write_text(SOURCE, encoding="utf-8")
            target.write_text(KOREAN, encoding="utf-8")
            self.assertEqual(parity.check_pair(source, target), [])

    def test_changed_number_and_url_fail(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "alpha.ara.md"
            target = root / "alpha.ko.ara.md"
            source.write_text(SOURCE, encoding="utf-8")
            target.write_text(KOREAN.replace("25%", "30%").replace("example.com/a", "example.com/b"), encoding="utf-8")
            errors = parity.check_pair(source, target)
            self.assertIn("URL multiset changed", errors)
            self.assertIn("numeric-token multiset changed", errors)

    def test_changed_directive_topology_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "alpha.ara.md"
            target = root / "alpha.ko.ara.md"
            source.write_text(SOURCE, encoding="utf-8")
            target.write_text(KOREAN.replace(":::callout", ":::statement"), encoding="utf-8")
            errors = parity.check_pair(source, target)
            self.assertIn("ARA block-directive topology changed", errors)

    def test_changed_anchor_id_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "alpha.ara.md"
            target = root / "alpha.ko.ara.md"
            source.write_text(SOURCE, encoding="utf-8")
            target.write_text(KOREAN.replace("[^1]", "[^x]"), encoding="utf-8")
            errors = parity.check_pair(source, target)
            self.assertIn("citation/reference-id multiset changed", errors)
            self.assertIn(
                "compiled HTML tag/class/immutable-attribute topology changed",
                errors,
            )

    def test_short_faithful_translation_passes_relative_language_floor(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "short.ara.md"
            target = root / "short.ko.ara.md"
            source.write_text(
                "---\ntitle: Short result\n---\n\n## Summary\n\nA short but complete result.\n",
                encoding="utf-8",
            )
            target.write_text(
                "---\ntitle: 짧은 결과\n---\n\n## 요약\n\n짧지만 완전한 결과입니다.\n",
                encoding="utf-8",
            )
            self.assertEqual(parity.check_pair(source, target), [])

    def test_chart_labels_translate_but_machine_values_stay_exact(self):
        source_html = (
            '<article class="ara-doc"><div class="ara-line-chart" '
            'data-x-labels="January,February" data-series-1="1,2" '
            'data-series-1-label="Revenue" data-title="Revenue trend" '
            'data-y-unit="$"></div><p>Revenue trend.</p></article>'
        )
        target_html = (
            '<article class="ara-doc"><div class="ara-line-chart" '
            'data-x-labels="일월,이월" data-series-1="1,2" '
            'data-series-1-label="매출" data-title="매출 추이" '
            'data-y-unit="$"></div><p>매출 추이입니다.</p></article>'
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "chart.html"
            target = root / "chart.ko.html"
            source.write_text(source_html, encoding="utf-8")
            target.write_text(target_html, encoding="utf-8")
            self.assertEqual(parity.check_pair(source, target), [])

    def test_chart_label_punctuation_does_not_define_item_count(self):
        source_html = (
            '<article class="ara-doc"><div class="ara-donut" '
            'data-labels="R&amp;D, platform,Cloud" data-values="25,75" '
            'data-center-label="Mix"></div><p>Allocation mix.</p></article>'
        )
        target_html = (
            '<article class="ara-doc"><div class="ara-donut" '
            'data-labels="연구개발 및 플랫폼,클라우드" data-values="25,75" '
            'data-center-label="구성"></div><p>배분 구성입니다.</p></article>'
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "donut.html"
            target = root / "donut.ko.html"
            source.write_text(source_html, encoding="utf-8")
            target.write_text(target_html, encoding="utf-8")
            self.assertEqual(parity.check_pair(source, target), [])

    def test_unknown_data_attribute_is_immutable(self):
        source_html = (
            '<article class="ara-doc"><div class="ara-callout" '
            'data-formula="revenue-cost"><p>Source prose.</p></div></article>'
        )
        target_html = source_html.replace("revenue-cost", "revenue+cost").replace(
            "Source prose", "원문 설명"
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "formula.html"
            target = root / "formula.ko.html"
            source.write_text(source_html, encoding="utf-8")
            target.write_text(target_html, encoding="utf-8")
            self.assertIn(
                "compiled HTML tag/class/immutable-attribute topology changed",
                parity.check_pair(source, target),
            )

    def test_long_english_copy_with_korean_blob_fails(self):
        paragraph = (
            "the company reported strong revenue growth while operating costs "
            "declined and customer demand remained durable across every region. "
        )
        source_body = paragraph * 80
        korean_blob = "가" * 200
        source_raw = f"---\ntitle: Long report\n---\n\n## Analysis\n\n{source_body}\n"
        target_raw = (
            f"---\ntitle: {korean_blob}\n---\n\n## Analysis\n\n{source_body}\n"
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "copied.ara.md"
            target = root / "copied.ko.ara.md"
            source.write_text(source_raw, encoding="utf-8")
            target.write_text(target_raw, encoding="utf-8")
            self.assertTrue(
                any(
                    "visible English prose was copied unchanged" in error
                    for error in parity.check_pair(source, target)
                )
            )

    def test_proper_noun_heavy_translation_passes(self):
        source_raw = """---
title: Model updates
---

## Models

OpenAI, Anthropic, Google, Meta, NVIDIA, Microsoft, DeepSeek, and Mistral published model updates.
"""
        target_raw = """---
title: 모델 업데이트
---

## 모델

OpenAI, Anthropic, Google, Meta, NVIDIA, Microsoft, DeepSeek, Mistral이 모델 업데이트를 발표했습니다.
"""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "models.ara.md"
            target = root / "models.ko.ara.md"
            source.write_text(source_raw, encoding="utf-8")
            target.write_text(target_raw, encoding="utf-8")
            self.assertEqual(parity.check_pair(source, target), [])


class TranslationWriterTest(unittest.TestCase):
    def _run_writer(self, root: Path, body: Path, *, replace: bool) -> int:
        source = root / "research/generative/2026-01-01T000000--alpha.ara.md"
        args = [
            "--topic", "Alpha Korean",
            "--html-body", str(body),
            "--model", "deepseek-v4-flash",
            "--language", "ko",
            "--translation-of", "alpha",
            "--translation-source-file", "research/generative/2026-01-01T000000--alpha.ara.md",
            "--translation-source-sha256", hashlib.sha256(source.read_bytes()).hexdigest(),
            "--repo-root", str(root),
            "--no-commit",
        ]
        if replace:
            args.append("--replace-translation")
        return writer.main(args)

    def test_writer_rejects_existing_translation_by_default(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gen, _ = seed_repo(root, translated=True)
            body = root / "alpha.ko.ara.md"
            body.write_text(KOREAN, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "already exists"):
                self._run_writer(root, body, replace=False)
            self.assertEqual(list(gen.glob("*--alpha.ko.html")), [])
            self.assertEqual(list(gen.glob("*--alpha.ko.ara.md")), [])

    def test_writer_replace_records_provenance_and_inherits_tags(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gen, _ = seed_repo(root, translated=True)
            body = root / "alpha.ko.ara.md"
            body.write_text(KOREAN, encoding="utf-8")
            self.assertEqual(self._run_writer(root, body, replace=True), 0)
            row = json.loads((gen / "index.json").read_text(encoding="utf-8"))[0]
            ko = row["translations"]["ko"]
            self.assertEqual(ko["source_file"], "research/generative/2026-01-01T000000--alpha.ara.md")
            self.assertEqual(ko["tags"], ["semiconductors", "cost"])
            self.assertRegex(ko["source_sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(ko["translated_at"].endswith("Z"))


class TranslationCommitVerifierTest(unittest.TestCase):
    @staticmethod
    def _git(root: Path, *args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(root), *args], text=True
        ).strip()

    def test_accepts_exact_writer_commit_and_rejects_extra_path(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gen, _ = seed_repo(root)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Test Writer")
            self._git(root, "config", "user.email", "writer@example.test")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "seed")
            base_sha = self._git(root, "rev-parse", "HEAD")

            body = root / "alpha.ko.ara.md"
            body.write_text(KOREAN, encoding="utf-8")
            writer_test = TranslationWriterTest()
            self.assertEqual(writer_test._run_writer(root, body, replace=False), 0)
            generated = sorted(gen.glob("*--alpha.ko.*"))
            self.assertEqual(len(generated), 2)
            self._git(
                root,
                "add",
                "research/generative/index.json",
                *(path.relative_to(root).as_posix() for path in generated),
            )
            self._git(root, "commit", "-qm", "publish ko translation")

            source_file = "research/generative/2026-01-01T000000--alpha.ara.md"
            source_sha = hashlib.sha256((root / source_file).read_bytes()).hexdigest()
            result = verifier.verify(
                root,
                base_sha,
                "alpha",
                "ara",
                source_file,
                source_sha,
                "deepseek-v4-flash",
            )
            row = json.loads((gen / "index.json").read_text(encoding="utf-8"))[0]
            self.assertEqual(
                result["html_path"],
                f"research/generative/{row['translations']['ko']['file']}",
            )
            self.assertEqual(len(result["allowed_paths"].splitlines()), 3)

            (root / "unexpected.txt").write_text("forbidden\n", encoding="utf-8")
            self._git(root, "add", "unexpected.txt")
            self._git(root, "commit", "-qm", "add forbidden output")
            with self.assertRaisesRegex(ValueError, "expected 3 committed paths"):
                verifier.verify(
                    root,
                    base_sha,
                    "alpha",
                    "ara",
                    source_file,
                    source_sha,
                    "deepseek-v4-flash",
                )


if __name__ == "__main__":
    unittest.main()
