"""Recovery dates, parent handoffs, and the diagnostic publication boundary."""

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

from digest_edition import resolve_date, validate_date

ROOT = Path(__file__).resolve().parents[1]


class EditionTest(unittest.TestCase):
    def test_historical_input_wins_and_midnight_delay_preserves_parent_date(self):
        now = datetime(2026, 10, 25, 1, tzinfo=timezone.utc)
        self.assertEqual(resolve_date("2026-10-22", "2026-10-24T23:59:00Z", now), "2026-10-22")
        self.assertEqual(resolve_date("", "2026-10-24T23:59:00Z", now), "2026-10-24")
        self.assertEqual(resolve_date("", "2026-10-25T08:59:00+09:00", now), "2026-10-24")
        self.assertEqual(resolve_date("", "", now), "2026-10-25")

    def test_invalid_dates_fail_before_shell_interpolation(self):
        for value in ("2026-02-30", "2026-1-2", "20261024", "$(echo bad)", "../file", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_date(value)

    def test_documented_cli_round_trip_and_missing_parent_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "digest-edition.json"
            command = [sys.executable, str(ROOT / "scripts/digest_edition.py")]
            write = subprocess.run(command + ["--date", "2026-10-22", "--output", str(path)], capture_output=True, text=True)
            self.assertEqual(write.returncode, 0, write.stderr)
            self.assertEqual(json.loads(path.read_text()), {"date": "2026-10-22"})
            read = subprocess.run(command + ["--manifest", str(path)], capture_output=True, text=True)
            self.assertEqual(read.stdout.strip(), "2026-10-22")
            for content in ('{"date":"2026-02-30"}', '{"date":null}', '{}'):
                path.write_text(content)
                self.assertNotEqual(subprocess.run(command + ["--manifest", str(path)], capture_output=True).returncode, 0)
            path.unlink()
            self.assertNotEqual(subprocess.run(command + ["--manifest", str(path)], capture_output=True).returncode, 0)

    def test_workflow_keeps_diagnostics_but_requires_editorial_success(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/daily-digest.yml").read_text())
        self.assertEqual(workflow["jobs"]["daily-digest"]["permissions"]["actions"], "read")
        steps = workflow["jobs"]["daily-digest"]["steps"]
        names = [step.get("name", "") for step in steps]
        self.assertLess(names.index("Push changes"), names.index("Require editorial publication"))
        self.assertLess(names.index("Require editorial publication"), names.index("Hand off exact digest edition"))
        gate = next(step for step in steps if step.get("name") == "Require editorial publication")
        self.assertIn("--require-editorial", gate["run"])
        self.assertFalse(gate.get("continue-on-error", False))
        for name in ("Push changes", "Push audio stub"):
            publish = next(step for step in steps if step.get("name") == name)
            self.assertEqual(publish["with"]["strict-publication"], "true")
        front = yaml.safe_load((ROOT / ".github/workflows/daily-front-page.yml").read_text())
        handoff = next(step for step in front["jobs"]["front-page"]["steps"] if step.get("name") == "Read parent digest edition")
        self.assertEqual(handoff["with"]["run-id"], "${{ github.event.workflow_run.id }}")
        self.assertEqual(handoff["with"]["name"], "digest-edition-${{ github.event.workflow_run.run_attempt }}")

    def test_manual_recovery_notifications_are_opt_in(self):
        for filename, names in {
            "daily-digest.yml": ["Send Telegram notification (audio + caption)", "Send audio to Hooker (parallel delivery channel)"],
            "daily-front-page.yml": ["Publish front page via hooker", "Publish digest audio via hooker"],
        }.items():
            workflow = yaml.safe_load((ROOT / ".github/workflows" / filename).read_text())
            inputs = workflow[True]["workflow_dispatch"]["inputs"]
            self.assertFalse(inputs["notify"]["default"])
            steps = next(iter(workflow["jobs"].values()))["steps"]
            for name in names:
                step = next(step for step in steps if step.get("name") == name)
                self.assertIn("inputs.notify", step["if"])


if __name__ == "__main__":
    unittest.main()
