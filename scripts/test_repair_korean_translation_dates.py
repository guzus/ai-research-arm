#!/usr/bin/env python3

from __future__ import annotations

import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import repair_korean_translation_dates as repair
from compile_ara import compile_source


SOURCE = """---
title: Link launched on October 26–27
deck: The seed tweet is dated October 29, 2026.
---

## 01. Timeline

On 21 September 2026 the index was rebased, after Stripe bought Privy in June 2025 [^1].

The window opened on March 18, 2026 and the filing calls it "the October 26, 2026 launch" [^1].

:::references
- {id: 1, title: "Launch notes, October 26, 2026", url: "https://example.com/a"}
:::
"""

# The shapes the segment protocol published, one per run.
GARBLED = {
    "Link launched on October 26–27": "Link 출시는 26월 27에 이루어졌다",
    "The seed tweet is dated October 29, 2026.": "시드 트윗은 29월 2026자이다.",
    "Timeline": "타임라인",
    "On 21 September 2026 the index was rebased, after Stripe bought Privy in June 2025 ":
        "21년 2026월 지수가 재조정되었고, Stripe는 6월 2025에 Privy를 샀다 ",
    'The window opened on March 18, 2026 and the filing calls it "the October 26, 2026 launch" ':
        "창은 3월 18, 2026에 열렸고 신고서는 이를 「10월 26, 2026 출시」라고 부른다 ",
    "References": "참고문헌",
    "Launch notes, October 26, 2026": "출시 노트, 10월 26, 2026",
}


def seed(root: Path) -> Path:
    gen = root / "research" / "generative"
    gen.mkdir(parents=True)
    source = gen / "2026-10-31T000000--link.ara.md"
    source.write_text(SOURCE, encoding="utf-8")
    korean = compile_source(SOURCE)
    for english, garbled in GARBLED.items():
        assert english in korean, english
        korean = korean.replace(english, garbled, 1)
    (gen / "2026-10-31T010000--link.ko.html").write_text(korean, encoding="utf-8")
    row = {
        "slug": "link",
        "file": "2026-10-31T000000--link.html",
        "title": "Link launched on October 26–27",
        "translations": {
            "ko": {
                "file": "2026-10-31T010000--link.ko.html",
                "title": "Link 출시는 26월 27에 이루어졌다",
                "source_file": "research/generative/2026-10-31T000000--link.ara.md",
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            }
        },
    }
    (gen / "index.json").write_text(json.dumps([row], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return gen


class RepairKoreanTranslationDatesTest(unittest.TestCase):
    def test_parse_back_reads_the_same_date_in_both_languages(self):
        cases = {
            "October 29, 2026": "2026년 10월 29일",
            "October 26–27": "10월 26–27일",
            "4 and 7 September 2026": "2026년 9월 4일과 7일",
            "September 29-October 1": "9월 29일–10월 1일",
            "April–February 2026": "4월–2026년 2월",
            "June 2025": "2025년 6월",
        }
        for english, korean in cases.items():
            with self.subTest(english=english):
                [(form, match)] = repair.segments.date_matches(english)
                self.assertEqual(repair.segments.korean_date(form, match), korean)
                self.assertEqual(repair.korean_components(korean), repair.english_components(form, match))
        self.assertEqual(repair.korean_components("2026년 유월 17일"), ("2026", (6,), ("17",)))

    def test_classes_split_factual_from_format_and_b_skips_quotes_titles_and_ranges(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed(root)
            changes, report = repair.run(root, {"A", "B"}, write=False)
            got = {(c.cls, c.before, c.after) for c in changes if c.file != "index.json"}
            self.assertEqual(
                got,
                {
                    ("A", "26월 27", "10월 26–27일"),
                    ("A", "29월 2026", "2026년 10월 29일"),
                    ("A", "21년 2026월", "2026년 9월 21일"),
                    ("B", "6월 2025", "2025년 6월"),
                    ("B", "3월 18, 2026", "2026년 3월 18일"),
                },
            )
            range_fix = next(c for c in changes if c.before == "26월 27")
            self.assertIn("range", range_fix.flags)
            reasons = {entry["reason"] for entry in report.unresolved}
            self.assertIn("B skips dates in a quote", reasons)
            self.assertIn("B skips dates in a reference", reasons)
            [title] = [c for c in changes if c.file == "index.json"]
            self.assertEqual((title.cls, title.before, title.after), ("A", "26월 27", "10월 26–27일"))

    def test_write_is_byte_identical_outside_dates_and_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gen = seed(root)
            path = gen / "2026-10-31T010000--link.ko.html"
            before = path.read_text(encoding="utf-8")
            changes, _ = repair.run(root, {"A", "B"}, write=True)
            after = path.read_text(encoding="utf-8")
            self.assertIn("Link 출시는 10월 26–27일에 이루어졌다", after)
            self.assertIn("시드 트윗은 2026년 10월 29일자이다.", after)
            self.assertIn("2026년 9월 21일 지수가 재조정되었고, Stripe는 2025년 6월에 Privy를 샀다", after)
            self.assertIn("창은 2026년 3월 18일에 열렸고", after)
            self.assertIn("「10월 26, 2026 출시」", after)  # a quote stays as published
            self.assertIn("출시 노트, 10월 26, 2026", after)  # so does a work's title
            spans = [(c.start, c.end) for c in changes if c.file != "index.json"]
            self.assertEqual(
                repair.masked(before, spans).count("\0"), len(spans)
            )
            self.assertIn("10월 26–27일에", json.loads((gen / "index.json").read_text())[0]["translations"]["ko"]["title"])
            again, _ = repair.run(root, {"A", "B"}, write=True)
            self.assertEqual(again, [])
            self.assertEqual(path.read_text(encoding="utf-8"), after)

    def test_a_only_leaves_format_fixes_for_b(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            gen = seed(root)
            repair.run(root, {"A"}, write=True)
            text = (gen / "2026-10-31T010000--link.ko.html").read_text(encoding="utf-8")
            self.assertIn("2026년 10월 29일", text)
            self.assertIn("6월 2025에", text)
            later, _ = repair.run(root, {"A", "B"}, write=False)
            self.assertEqual({c.cls for c in later}, {"B"})

    def test_masked_comparison_rejects_a_change_outside_the_spans(self):
        old = "앞 29월 2026 뒤"
        edits = [(2, 10, "2026년 10월 29일")]
        repair.assert_identical_outside(old, "앞 2026년 10월 29일 뒤", edits, "ok")
        with self.assertRaises(SystemExit):
            repair.assert_identical_outside(old, "앞 2026년 10월 29일 뒤!", edits, "bad")

    def test_report_writes_table_samples_and_counts(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seed(root)
            changes, report = repair.run(root, {"A", "B"}, write=False)
            out = root / "report"
            repair.write_reports(out, changes, report, seed=0)
            with (out / "repair-table.csv").open(encoding="utf-8") as handle:
                table = list(csv.DictReader(handle))
            self.assertEqual(len(table), len(changes))
            self.assertEqual(
                set(table[0]),
                {"file", "class", "rule", "unit", "flags", "english_source", "before", "after", "context"},
            )
            self.assertTrue((out / "samples.csv").is_file())
            with (out / "per-file-counts.csv").open(encoding="utf-8") as handle:
                counts = list(csv.DictReader(handle))
            self.assertEqual(sum(int(row["total"]) for row in counts), len(changes))


if __name__ == "__main__":
    unittest.main()
