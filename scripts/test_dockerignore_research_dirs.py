#!/usr/bin/env python3
"""Every research dir prebuild copies must be whitelisted in .dockerignore.

This closes a gap that CI structurally cannot see. `.dockerignore` excludes
`research/*` and re-includes specific dirs; `dashboard/scripts/prebuild.mjs`
copies some dirs into `public/research/` and reads other build-only inputs. The
three lists must agree, but nothing enforced it and the failure is SILENT in
both directions that matter:

  - prebuild skips a missing dir with `if (!existsSync(src)) continue;`
  - CI never builds the Dockerfile (load-bearing rule 3), so the local build
    is always fine — the miss only appears in production

Observed 2026-08-01: `market` was added to COPY_DIRS for the wiki hover quote
row and the dashboard build passed locally, but `research/market/` was absent
from the Docker context, so ara.guzus.xyz served 404 for
/research/market/quotes.json. The .dockerignore comment warns about exactly
this ("A research dir consumed by prebuild MUST be whitelisted here too") —
a comment is not a gate, so this is the gate.

Run: uv run python scripts/test_dockerignore_research_dirs.py
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCKERIGNORE = REPO_ROOT / ".dockerignore"
PREBUILD = REPO_ROOT / "dashboard" / "scripts" / "prebuild.mjs"

# `const COPY_DIRS = ['a', ...];` / `const BUILD_INPUT_DIRS = ['b', ...];` /
# `const AB_COMPARISON_LANES = [ ... ];`
ARRAY_RE = r"const\s+{name}\s*=\s*\[(.*?)\]"


def _js_string_array(source: str, name: str) -> list[str]:
    match = re.search(ARRAY_RE.format(name=name), source, re.DOTALL)
    if not match:
        raise AssertionError(
            f"could not find `const {name} = [...]` in {PREBUILD} — the parser and "
            "the file have drifted; fix this test rather than deleting it"
        )
    return re.findall(r"'([^']+)'", match.group(1))


def _dockerignore_reincludes(text: str) -> set[str]:
    """Return dir names re-included via `!research/<name>` lines."""
    out: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        m = re.fullmatch(r"!research/([A-Za-z0-9._-]+)", line)
        if m:
            out.add(m.group(1))
    return out


class DockerignoreResearchDirsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prebuild = PREBUILD.read_text(encoding="utf-8")
        cls.dockerignore = DOCKERIGNORE.read_text(encoding="utf-8")
        cls.reincluded = _dockerignore_reincludes(cls.dockerignore)

    def test_research_is_excluded_by_default(self):
        # The allowlist only means anything if the blanket exclude is present.
        self.assertIn("research/*", self.dockerignore.splitlines())

    def test_every_copy_dir_is_whitelisted(self):
        missing = [d for d in _js_string_array(self.prebuild, "COPY_DIRS") if d not in self.reincluded]
        self.assertEqual(
            [], missing,
            f"prebuild.mjs copies research/{missing} but .dockerignore does not re-include "
            f"them, so they are absent from the Railway build context and production will "
            f"404 that data while the local build looks fine. Add `!research/<dir>` and "
            f"`!research/<dir>/**` to .dockerignore.",
        )

    def test_every_build_input_dir_is_whitelisted(self):
        missing = [d for d in _js_string_array(self.prebuild, "BUILD_INPUT_DIRS") if d not in self.reincluded]
        self.assertEqual(
            [], missing,
            f"prebuild.mjs reads build-only research/{missing} but .dockerignore does not "
            f"re-include them, so Railway silently builds incomplete public artifacts. "
            f"Add `!research/<dir>` and `!research/<dir>/**` to .dockerignore.",
        )

    def test_every_ab_comparison_lane_is_whitelisted(self):
        lanes = _js_string_array(self.prebuild, "AB_COMPARISON_LANES")
        missing = [d for d in lanes if d not in self.reincluded]
        self.assertEqual([], missing, f"A/B lanes missing from .dockerignore: {missing}")

    def test_recursive_glob_accompanies_each_reinclude(self):
        # `!research/foo` alone re-includes the directory entry but not its
        # contents; the `/**` line is what actually ships the files.
        lines = {l.strip() for l in self.dockerignore.splitlines()}
        for name in sorted(self.reincluded):
            self.assertIn(
                f"!research/{name}/**", lines,
                f"`!research/{name}` has no matching `!research/{name}/**`, so the "
                f"directory is re-included but its files are still excluded",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
