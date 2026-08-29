#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import check_generative_translation as parity
import generative_translation_segments as segments
import prepare_generative_translation as prepare
import verify_generative_translation_commit as verifier
import write_generative_research as writer
from compile_ara import compile_source


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
            self.assertTrue(values["draft_path"].endswith(".ko.html"))
            self.assertTrue(values["result_path"].endswith(".segments.jsonl"))
            self.assertEqual(values["translation_type"], "html")

    def test_rejects_legacy_html_only_article(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_repo(root, ara=False)
            with self.assertRaisesRegex(ValueError, "legacy HTML-only"):
                prepare.prepare(root, "alpha", force=False)

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

    def test_stages_only_metadata_without_untrusted_source_prose(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gen, _ = seed_repo(root)
            values = prepare.prepare(root, "alpha", force=False)
            request = prepare.stage_agent_request(
                root, values, ".agent-input/translation.json"
            )

            self.assertNotIn("source_path", request)
            self.assertEqual(
                request,
                json.loads((root / ".agent-input/translation.json").read_text()),
            )
            self.assertNotIn(values["source_path"], json.dumps(request))


class TranslationSegmentsTest(unittest.TestCase):
    @staticmethod
    def _korean_text(segment: segments.Segment) -> str:
        pieces = segments.TOKEN_RE.split(segment.text)
        tokens = segments.TOKEN_RE.findall(segment.text)
        out: list[str] = []
        for index, piece in enumerate(pieces):
            if piece.strip():
                out.append("안전한 한국어 번역문")
            if index < len(tokens):
                out.append(tokens[index])
        return " ".join(out) or "한국어"

    def test_renderer_preserves_structure_and_immutable_literals(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "alpha.ara.md"
            source.write_text(SOURCE, encoding="utf-8")
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            compiled, manifest = segments.build_manifest(source, source_sha)
            extracted = segments.extract_segments(compiled)
            result = root / segments.RESULT_PATH
            result.parent.mkdir()
            result.write_text(
                "".join(
                    json.dumps(
                        {"id": segment.id, "text": self._korean_text(segment)},
                        ensure_ascii=False,
                    )
                    + "\n"
                    for segment in extracted
                ),
                encoding="utf-8",
            )
            draft = root / segments.DRAFT_PATH
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                segments.render(source, source_sha, segments.RESULT_PATH, segments.DRAFT_PATH)
            finally:
                os.chdir(old_cwd)
            self.assertEqual(manifest["segment_count"], len(extracted))
            self.assertEqual(parity.check_pair(source, draft), [])

    def test_renderer_recovers_concatenated_and_leaky_jsonl_rows(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "alpha.ara.md"
            source.write_text(SOURCE, encoding="utf-8")
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            compiled, _ = segments.build_manifest(source, source_sha)
            extracted = segments.extract_segments(compiled)
            result = root / segments.RESULT_PATH
            result.parent.mkdir()
            rows = [
                json.dumps(
                    {"id": segment.id, "text": self._korean_text(segment)},
                    ensure_ascii=False,
                )
                for segment in extracted
            ]
            leaked = rows[0][:-1] + ' extra quote"} trailing'
            glued = rows[1] + rows[2]
            inner = json.loads(rows[3])
            quoted = (
                '{"id":"'
                + inner["id"]
                + '","text":"'
                + inner["text"][:8]
                + ' "중간" '
                + inner["text"][8:]
                + '"}'
            )
            body = [leaked, glued, quoted, rows[3], *rows[4:]]
            result.write_text("\n".join(body) + "\n", encoding="utf-8")
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                segments.render(
                    source, source_sha, segments.RESULT_PATH, segments.DRAFT_PATH
                )
            finally:
                os.chdir(old_cwd)
            self.assertEqual(
                parity.check_pair(source, root / segments.DRAFT_PATH), []
            )

    def test_renderer_skips_blank_and_non_object_jsonl_lines(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "alpha.ara.md"
            source.write_text(SOURCE, encoding="utf-8")
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            compiled, _ = segments.build_manifest(source, source_sha)
            extracted = segments.extract_segments(compiled)
            result = root / segments.RESULT_PATH
            result.parent.mkdir()
            rows = [
                json.dumps(
                    {"id": segment.id, "text": self._korean_text(segment)},
                    ensure_ascii=False,
                )
                for segment in extracted
            ]
            result.write_text(
                "\n---\n".join(rows) + "\n\n// trailing note\n",
                encoding="utf-8",
            )
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                segments.render(
                    source, source_sha, segments.RESULT_PATH, segments.DRAFT_PATH
                )
            finally:
                os.chdir(old_cwd)
            self.assertEqual(
                parity.check_pair(source, root / segments.DRAFT_PATH), []
            )

    def test_model_manifest_is_compact_json_lines(self):
        repo = Path(__file__).resolve().parent.parent
        source = repo / (
            "research/generative/2026-08-11T084945--"
            "eu-ai-act-article-50-2-claude-s-text-watermark-the-six-signa.ara.md"
        )
        source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".agent-input").mkdir()
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                manifest = segments.write_manifest(
                    source, source_sha, segments.MANIFEST_PATH
                )
            finally:
                os.chdir(old_cwd)
            payload = (root / segments.MANIFEST_PATH).read_text(encoding="utf-8")
            lines = payload.splitlines()
            self.assertEqual(len(lines), manifest["segment_count"] + 1)
            self.assertEqual(json.loads(lines[0])["segment_count"], 438)
            self.assertEqual(len(json.loads(lines[1])), 3)
            self.assertLess(len(payload.encode("utf-8")), 65_000)

    def test_renderer_rejects_missing_or_changed_tokens(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "alpha.ara.md"
            source.write_text(SOURCE, encoding="utf-8")
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            compiled, _ = segments.build_manifest(source, source_sha)
            extracted = segments.extract_segments(compiled)
            result = root / segments.RESULT_PATH
            result.parent.mkdir()
            rows = [
                {"id": segment.id, "text": self._korean_text(segment)}
                for segment in extracted
            ]
            token_row = next(row for row in rows if segments.TOKEN_RE.search(row["text"]))
            token_row["text"] = segments.TOKEN_RE.sub("", token_row["text"], count=1)
            result.write_text(
                "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                encoding="utf-8",
            )
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                with self.assertRaisesRegex(ValueError, "changed immutable tokens"):
                    segments.render(source, source_sha, segments.RESULT_PATH, segments.DRAFT_PATH)
            finally:
                os.chdir(old_cwd)

    def test_renderer_allows_swapped_token_order(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "alpha.ara.md"
            source.write_text(SOURCE, encoding="utf-8")
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            compiled, _ = segments.build_manifest(source, source_sha)
            extracted = segments.extract_segments(compiled)
            swapped = next(
                segment for segment in extracted if len(segment.tokens) >= 2
            )
            (root / ".tmp").mkdir()
            (root / segments.RESULT_PATH).write_text(
                "".join(
                    json.dumps(
                        {
                            "id": segment.id,
                            "text": (
                                " ".join(
                                    reversed(segments.TOKEN_RE.findall(self._korean_text(segment)))
                                )
                                if segment.id == swapped.id
                                else self._korean_text(segment)
                            ),
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                    for segment in extracted
                ),
                encoding="utf-8",
            )
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                segments.render(
                    source, source_sha, segments.RESULT_PATH, segments.DRAFT_PATH
                )
            finally:
                os.chdir(old_cwd)
            self.assertEqual(
                parity.check_pair(
                    source,
                    root / segments.DRAFT_PATH,
                    allow_localized_number_rendering=True,
                ),
                [],
            )

    def test_live_failure_fixture_now_passes_structural_parity(self):
        repo = Path(__file__).resolve().parent.parent
        source = repo / (
            "research/generative/2026-08-11T084945--"
            "eu-ai-act-article-50-2-claude-s-text-watermark-the-six-signa.ara.md"
        )
        source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
        compiled, _ = segments.build_manifest(source, source_sha)
        extracted = segments.extract_segments(compiled)
        self.assertGreater(len(extracted), 400)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".tmp").mkdir()
            (root / segments.RESULT_PATH).write_text(
                "".join(
                    json.dumps(
                        {"id": segment.id, "text": self._korean_text(segment)},
                        ensure_ascii=False,
                    )
                    + "\n"
                    for segment in extracted
                ),
                encoding="utf-8",
            )
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                segments.render(source, source_sha, segments.RESULT_PATH, segments.DRAFT_PATH)
            finally:
                os.chdir(old_cwd)
            self.assertEqual(parity.check_pair(source, root / segments.DRAFT_PATH), [])

    def test_strip_unsafe_digits_keeps_tokens_and_korean_integer_forms(self):
        token = "⟦ARA0007⟧"
        self.assertEqual(
            segments.strip_unsafe_digits(f"{token} 1차 9일 $1,000 30% 2.5 42"),
            f"{token} 1차 9일    ",
        )
        # Leftover currency/percent/dot must not remain to glue onto the
        # restored token and change 2.5 into $2.5 or 25 into 25%.
        self.assertEqual(segments.strip_unsafe_digits(f"${token}"), token)
        self.assertEqual(segments.strip_unsafe_digits(f"{token}%"), token)
        self.assertEqual(segments.strip_unsafe_digits(f"$2.5{token}"), token)

    def test_renderer_allows_korean_integer_forms_and_strips_unsafe_numbers(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "alpha.ara.md"
            source.write_text(SOURCE, encoding="utf-8")
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            compiled, _ = segments.build_manifest(source, source_sha)
            extracted = segments.extract_segments(compiled)
            (root / ".tmp").mkdir()

            def write_rows(extra: str) -> None:
                (root / segments.RESULT_PATH).write_text(
                    "".join(
                        json.dumps(
                            {
                                "id": segment.id,
                                "text": self._korean_text(segment)
                                + (extra if segment.id == extracted[0].id else ""),
                            },
                            ensure_ascii=False,
                        )
                        + "\n"
                        for segment in extracted
                    ),
                    encoding="utf-8",
                )

            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                write_rows(" 1차 9일 30배")
                segments.render(
                    source, source_sha, segments.RESULT_PATH, segments.DRAFT_PATH
                )
                for leftover in (" $1,000", " -30%", " 2.5×", " 42", "$2.5", "$", "%"):
                    with self.subTest(leftover=leftover):
                        write_rows(leftover)
                        segments.render(
                            source,
                            source_sha,
                            segments.RESULT_PATH,
                            segments.DRAFT_PATH,
                        )
                        draft = (root / segments.DRAFT_PATH).read_text(encoding="utf-8")
                        self.assertEqual(
                            parity.check_pair(
                                source,
                                root / segments.DRAFT_PATH,
                                allow_localized_number_rendering=True,
                            ),
                            [],
                        )
                        self.assertNotIn("$$", draft)
                        self.assertNotIn("$12%", draft)
            finally:
                os.chdir(old_cwd)

    def test_renderer_rejects_unprotected_list_separator(self):
        source_raw = """---
title: Allocation mix
---

:::donut
- {label: "R&D, platform", value: 25}
- {label: Cloud, value: 75}
:::
"""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "list.ara.md"
            source.write_text(source_raw, encoding="utf-8")
            source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
            compiled, _ = segments.build_manifest(source, source_sha)
            extracted = segments.extract_segments(compiled)
            protected = next(segment for segment in extracted if segment.forbid_commas)
            (root / ".tmp").mkdir()
            (root / segments.RESULT_PATH).write_text(
                "".join(
                    json.dumps(
                        {
                            "id": segment.id,
                            "text": self._korean_text(segment)
                            + (",추가" if segment.id == protected.id else ""),
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                    for segment in extracted
                ),
                encoding="utf-8",
            )
            old_cwd = Path.cwd()
            try:
                os.chdir(root)
                with self.assertRaisesRegex(ValueError, "unprotected list separator"):
                    segments.render(source, source_sha, segments.RESULT_PATH, segments.DRAFT_PATH)
            finally:
                os.chdir(old_cwd)

    def test_rejects_noncanonical_request_or_linked_input_directory(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed_repo(root)
            values = prepare.prepare(root, "alpha", force=False)
            with self.assertRaisesRegex(ValueError, "request file must be exactly"):
                prepare.stage_agent_request(root, values, ".tmp/request.json")

            outside = root / "outside"
            outside.mkdir()
            (root / ".agent-input").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "unsafe agent input directory"):
                prepare.stage_agent_request(
                    root, values, ".agent-input/translation.json"
                )


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

    def test_trusted_html_allows_localized_digits_but_preserves_source_literals(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "alpha.ara.md"
            target = root / "alpha.ko.html"
            source.write_text(SOURCE, encoding="utf-8")
            localized = compile_source(KOREAN).replace(
                "안정적인 수치를", "9일 전의 안정적인 수치를", 1
            )
            target.write_text(localized, encoding="utf-8")
            self.assertIn("numeric-token multiset changed", parity.check_pair(source, target))
            self.assertEqual(
                parity.check_pair(
                    source,
                    target,
                    allow_localized_number_rendering=True,
                ),
                [],
            )

            target.write_text(localized.replace("25%", "향상"), encoding="utf-8")
            self.assertIn(
                "source numeric-token multiset was not preserved or target added "
                "a non-localized numeric token",
                parity.check_pair(
                    source,
                    target,
                    allow_localized_number_rendering=True,
                ),
            )

            for unsafe in ("$1,000", "-30%", "2.5×", "42"):
                target.write_text(
                    localized.replace("안정적인", f"{unsafe} 안정적인", 1),
                    encoding="utf-8",
                )
                self.assertIn(
                    "source numeric-token multiset was not preserved or target added "
                    "a non-localized numeric token",
                    parity.check_pair(
                        source,
                        target,
                        allow_localized_number_rendering=True,
                    ),
                )

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

    def test_accepts_trusted_html_translation_of_ara_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gen, _ = seed_repo(root)
            self._git(root, "init", "-q")
            self._git(root, "config", "user.name", "Test Writer")
            self._git(root, "config", "user.email", "writer@example.test")
            self._git(root, "add", ".")
            self._git(root, "commit", "-qm", "seed")
            base_sha = self._git(root, "rev-parse", "HEAD")

            body = root / "alpha.ko.html"
            body.write_text(compile_source(KOREAN), encoding="utf-8")
            writer_test = TranslationWriterTest()
            self.assertEqual(writer_test._run_writer(root, body, replace=False), 0)
            generated = sorted(gen.glob("*--alpha.ko.html"))
            self.assertEqual(len(generated), 1)
            self._git(
                root,
                "add",
                "research/generative/index.json",
                generated[0].relative_to(root).as_posix(),
            )
            self._git(root, "commit", "-qm", "publish protected html translation")

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
                "html",
            )
            self.assertEqual(len(result["allowed_paths"].splitlines()), 2)
            self.assertEqual(result["source_artifact_path"], "")


if __name__ == "__main__":
    unittest.main()
