"""The runner-loss watchdog (rule 11) triggers on workflow *display names*.

`on.workflow_run.workflows` is matched against each target's `name:` string,
so a rename silently drops that lane from auto-recovery. Found 2026-09-06:
two of nine entries were stale (Twitter's name carried its backend tier list
and had been renamed with every tier change; Bluesky had been renamed), so
neither lane had been covered for weeks. This test pins the list to reality.
"""

import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = REPO_ROOT / ".github" / "workflows"
WATCHDOG = WORKFLOWS / "auto-rerun-on-runner-loss.yml"


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class AutoRerunWatchdogTest(unittest.TestCase):
    def setUp(self):
        self.watchdog = load(WATCHDOG)
        self.names = {}
        for path in sorted(WORKFLOWS.glob("*.yml")):
            doc = load(path)
            if isinstance(doc, dict) and isinstance(doc.get("name"), str):
                self.names[doc["name"]] = path.name

    def watched(self) -> list[str]:
        return list(self.watchdog[True]["workflow_run"]["workflows"])

    def test_every_watched_name_matches_a_real_workflow(self):
        missing = [n for n in self.watched() if n not in self.names]
        self.assertEqual([], missing,
                         f"watchdog entries match no workflow `name:` — rename drift: {missing}")

    def test_core_unattended_lanes_are_covered(self):
        by_file = {v: k for k, v in self.names.items()}
        for wf in ("hourly-twitter.yml", "2h-bluesky.yml", "hourly-rss.yml",
                   "4h-community.yml", "daily-arxiv.yml", "daily-digest.yml"):
            with self.subTest(workflow=wf):
                self.assertIn(by_file[wf], self.watched())

    def test_watchdog_is_not_self_referential_and_runs_hosted(self):
        self.assertNotIn(self.watchdog["name"], self.watched())
        for job in self.watchdog["jobs"].values():
            self.assertEqual("ubuntu-latest", job.get("runs-on"))


if __name__ == "__main__":
    unittest.main()
