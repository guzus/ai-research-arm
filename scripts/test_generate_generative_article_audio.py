#!/usr/bin/env python3
"""Tests for scripts/generate_generative_article_audio.py.

Focused on update_index, which mutates the shared research/generative/
index.json — the same file write_generative_research.py owns. The mutation
must run under that writer's lock and use its atomic temp-file+os.replace
writer so a concurrent publish and an audio backfill can't clobber each other
(Rule 8). These tests pin two invariants:

  * the audio_file field is set on the right row and other rows are untouched;
  * the on-disk shape (2-space indent, ensure_ascii=False, trailing newline)
    is byte-identical to what the writer produces — so routing through
    atomic_write_json did not change index.json's serialized form.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import generate_generative_article_audio as audio  # noqa: E402
import write_generative_research as writer  # noqa: E402


def _sample_rows() -> list[dict]:
    return [
        {
            "slug": "first-article",
            "file": "2026-05-01T000000--first-article.html",
            "kind": "fragment",
            "language": "en",
            "title": "First Article — détail",  # non-ASCII to lock ensure_ascii=False
            "model": "claude-opus-4-8",
            "created_at": "2026-05-01T00:00:00Z",
            "source": "workflow_dispatch",
            "prompt": "first",
            "tags": ["a", "b"],
        },
        {
            "slug": "second-article",
            "file": "2026-05-02T000000--second-article.html",
            "kind": "fragment",
            "language": "en",
            "title": "Second Article",
            "model": "claude-opus-4-8",
            "created_at": "2026-05-02T00:00:00Z",
            "source": "workflow_dispatch",
            "prompt": "second",
            "tags": [],
        },
    ]


class UpdateIndexTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.gen_dir = self.root / "research" / "generative"
        self.gen_dir.mkdir(parents=True)
        self.index_path = self.gen_dir / "index.json"
        # Seed using the writer's own serializer so "before" reflects the
        # canonical on-disk shape.
        writer.atomic_write_json(self.index_path, _sample_rows())

    def tearDown(self):
        self.tmp.cleanup()

    def test_sets_audio_file_on_matching_row_only(self):
        audio.update_index(self.root, "second-article", "audio/second-article.mp3")
        rows = json.loads(self.index_path.read_text(encoding="utf-8"))
        by_slug = {r["slug"]: r for r in rows}
        self.assertEqual(by_slug["second-article"]["audio_file"], "audio/second-article.mp3")
        # The other row is untouched — no stray audio_file key.
        self.assertNotIn("audio_file", by_slug["first-article"])
        # Every other field on the mutated row is preserved.
        self.assertEqual(by_slug["second-article"]["title"], "Second Article")
        self.assertEqual(by_slug["second-article"]["model"], "claude-opus-4-8")

    def test_shape_byte_identical_to_writer(self):
        # Capture the exact bytes the old hand-rolled writer would have produced
        # (json.dumps(..., indent=2, ensure_ascii=False) + "\n") and confirm the
        # locked atomic path produces the same bytes.
        rows = json.loads(self.index_path.read_text(encoding="utf-8"))
        for row in rows:
            if row["slug"] == "first-article":
                row["audio_file"] = "audio/first-article.mp3"
        expected_bytes = (
            json.dumps(rows, indent=2, ensure_ascii=False) + "\n"
        ).encode("utf-8")

        audio.update_index(self.root, "first-article", "audio/first-article.mp3")
        actual_bytes = self.index_path.read_bytes()
        self.assertEqual(actual_bytes, expected_bytes)
        # Belt-and-suspenders: trailing newline present, non-ASCII kept literal.
        self.assertTrue(actual_bytes.endswith(b"\n"))
        self.assertIn("détail", actual_bytes.decode("utf-8"))

    def test_unknown_slug_raises_and_leaves_index_unchanged(self):
        before = self.index_path.read_bytes()
        with self.assertRaises(SystemExit):
            audio.update_index(self.root, "does-not-exist", "audio/x.mp3")
        # The file must be unchanged: the slug check happens before any write.
        self.assertEqual(self.index_path.read_bytes(), before)

    def test_uses_writer_lockfile_path(self):
        # The lock must be the SAME file the article writer locks, or the two
        # writers wouldn't serialize. append_index_atomically locks
        # index.json + ".lock"; assert update_index creates exactly that file.
        lock_path = self.index_path.with_suffix(self.index_path.suffix + ".lock")
        self.assertFalse(lock_path.exists())
        audio.update_index(self.root, "first-article", "audio/first-article.mp3")
        self.assertTrue(lock_path.exists())


if __name__ == "__main__":
    unittest.main()
