#!/usr/bin/env python3
"""Tests for build_wiki_index.py — the committed research/wiki/index.json builder.

Mirrors test_wiki.py's tmp-dir fixture style. Verifies the index reuses
check_wiki's resolver (slug ∪ aliases), computes the inbound/outbound graph,
surfaces recent log entries newest-first, and that --check is a real drift gate.
"""

import tempfile
import unittest
from pathlib import Path

import build_wiki_index as bwi


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


ALPHA = """---
slug: alpha
title: Alpha Corp
type: entity
aliases: [A1]
tags: [infra]
summary: Alpha summary.
created_at: 2026-05-01
updated_at: 2026-05-02
---
Alpha links to [[beta]] and again via alias [[b-one|Beta]].
"""

BETA = """---
slug: beta
title: Beta Concept
type: concept
aliases: [b-one]
summary: Beta summary.
created_at: 2026-05-01
updated_at: 2026-05-03
---
Beta links back to [[alpha]].

```
this [[fenced-link]] must be ignored
```
"""

LOG = """# Wiki Log

## [2026-05-01] seed | seeded alpha and beta
## [2026-05-03] ingest | updated beta
"""


def _fixture(root: Path) -> None:
    _write(root, "entities/alpha.md", ALPHA)
    _write(root, "concepts/beta.md", BETA)
    _write(root, "log.md", LOG)


class BuildWikiIndexTest(unittest.TestCase):
    def test_index_shape_and_alias_resolution(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _fixture(root)
            idx = bwi.build_index(root)

            slugs = [p["slug"] for p in idx["pages"]]
            self.assertEqual(slugs, ["alpha", "beta"])  # sorted

            # Resolver maps slugs AND aliases, lowercased.
            self.assertEqual(idx["resolver"]["a1"], "alpha")
            self.assertEqual(idx["resolver"]["b-one"], "beta")
            self.assertEqual(idx["resolver"]["alpha"], "alpha")

            alpha = next(p for p in idx["pages"] if p["slug"] == "alpha")
            # [[beta]] and [[b-one]] both resolve to beta → deduped to one edge.
            self.assertEqual(alpha["outbound"], ["beta"])
            self.assertEqual(alpha["inbound"], ["beta"])
            self.assertEqual(alpha["file"], "entities/alpha.md")
            self.assertEqual(alpha["tags"], ["infra"])
            self.assertEqual(alpha["summary"], "Alpha summary.")
            self.assertEqual(alpha["created_at"], "2026-05-01")
            self.assertEqual(alpha["updated_at"], "2026-05-02")
            self.assertEqual(alpha["aliases"], ["A1"])

    def test_fenced_links_excluded_from_graph(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _fixture(root)
            idx = bwi.build_index(root)
            # 'fenced-link' is inside a code fence in beta.md → no edge, no resolver entry.
            self.assertNotIn("fenced-link", idx["resolver"])
            beta = next(p for p in idx["pages"] if p["slug"] == "beta")
            self.assertEqual(beta["outbound"], ["alpha"])

    def test_recent_log_newest_first(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _fixture(root)
            idx = bwi.build_index(root)
            self.assertEqual(idx["recent_log"][0]["date"], "2026-05-03")
            self.assertEqual(idx["recent_log"][0]["op"], "ingest")
            self.assertEqual(idx["recent_log"][-1]["date"], "2026-05-01")

    def test_check_is_a_drift_gate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _fixture(root)
            # Fresh write → --check passes.
            self.assertEqual(bwi.main(["--root", str(root)]), 0)
            self.assertEqual(bwi.main(["--root", str(root), "--check"]), 0)
            # Mutate a page → committed index.json is now stale → --check fails.
            _write(root, "concepts/beta.md", BETA.replace("updated_at: 2026-05-03", "updated_at: 2026-05-09"))
            self.assertEqual(bwi.main(["--root", str(root), "--check"]), 1)

    def test_check_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _fixture(root)
            self.assertEqual(bwi.main(["--root", str(root), "--check"]), 1)


if __name__ == "__main__":
    unittest.main()
