#!/usr/bin/env python3
"""Tests for export_wiki_okf.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

import check_wiki
import export_wiki_okf as okf


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


ALPHA = """---
slug: alpha
title: Alpha Corp
type: entity
aliases: [A1]
tags: [infra]
description: Alpha description.
created_at: 2026-05-01
timestamp: 2026-05-02T00:00:00Z
sources:
  - {title: "ARA digest", path: research/digest/2026-05-02-digest.md}
images:
  - url: "https://example.com/alpha-ui.jpg"
    alt: "Alpha Corp product UI illustrating the entity page."
    caption: "Alpha product surface."
    credit: "Alpha"
    source_url: "https://example.com/alpha-media"
---

Alpha links to [[beta]] and [[b-one|Beta by alias]].

```
[[beta]] inside a fence stays literal.
```
"""

BETA = """---
slug: beta
title: Beta Concept
type: concept
aliases: [b-one]
description: Beta description.
created_at: 2026-05-01
timestamp: 2026-05-03T00:00:00Z
---

Beta links back to [[alpha]].
"""

INDEX = """# Wiki Index

## Entities
- [[alpha]] — Alpha description.

## Concepts
- [[beta]] — Beta description.

## Themes
"""

LOG = """# Wiki Log

## [2026-05-01] seed | seeded alpha and beta
"""


def _fixture(root: Path) -> None:
    for subdir in check_wiki.PAGE_SUBDIRS:
        (root / subdir).mkdir(parents=True, exist_ok=True)
    _write(root, "entities/alpha.md", ALPHA)
    _write(root, "concepts/beta.md", BETA)
    _write(root, "index.md", INDEX)
    _write(root, "log.md", LOG)


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    header = text.split("\n---\n", 1)[0][4:]
    data = yaml.safe_load(header)
    assert isinstance(data, dict)
    return data


class ExportWikiOkfTest(unittest.TestCase):
    def test_export_maps_frontmatter_to_okf(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "wiki"
            out = Path(td) / "okf"
            _fixture(root)

            okf.export_okf(root, out, clean=False)

            data = _frontmatter(out / "entities" / "alpha.md")
            self.assertEqual(data["type"], "entity")
            self.assertEqual(data["title"], "Alpha Corp")
            self.assertEqual(data["description"], "Alpha description.")
            self.assertEqual(data["timestamp"], "2026-05-02T00:00:00Z")
            self.assertEqual(data["ara_slug"], "alpha")
            self.assertEqual(data["aliases"], ["A1"])
            self.assertEqual(data["tags"], ["infra"])
            self.assertEqual(data["sources"][0]["title"], "ARA digest")
            self.assertEqual(data["images"][0]["url"], "https://example.com/alpha-ui.jpg")
            self.assertEqual(data["images"][0]["alt"], "Alpha Corp product UI illustrating the entity page.")

    def test_export_rewrites_wikilinks_to_markdown_links(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "wiki"
            out = Path(td) / "okf"
            _fixture(root)

            okf.export_okf(root, out, clean=False)

            body = (out / "entities" / "alpha.md").read_text(encoding="utf-8")
            self.assertIn("[Beta Concept](../concepts/beta.md)", body)
            self.assertIn("[Beta by alias](../concepts/beta.md)", body)
            self.assertIn("[[beta]] inside a fence stays literal.", body)

            index = (out / "index.md").read_text(encoding="utf-8")
            self.assertIn("* [Alpha Corp](entities/alpha.md) - Alpha description.", index)
            self.assertNotIn("[[", index)

    def test_clean_replaces_existing_output(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "wiki"
            out = Path(td) / "okf"
            _fixture(root)
            out.mkdir()
            (out / "stale.txt").write_text("old", encoding="utf-8")

            okf.export_okf(root, out, clean=True)

            self.assertFalse((out / "stale.txt").exists())
            self.assertTrue((out / "index.md").exists())


if __name__ == "__main__":
    unittest.main()
