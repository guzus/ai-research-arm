"""Guard: every workflow must compute dates and timestamps in UTC.

The self-hosted runner's clock is CORRECT, but its timezone is KST (UTC+9).
A bare `date` therefore returns local time while every consumer treats the
value as UTC:

- commit messages and Telegram captions are formatted `'%Y-%m-%d %H:%M UTC'`,
  so a local `date` produces a string that literally lies;
- `research/<lane>/<date>.md` filenames are the pipeline's calendar, and the
  dashboard parses them as UTC (`dashboard/src/main.ts` — "the pipeline's UTC
  write schedule", and its `HH:MM UTC` title parser converts to viewer-local,
  so a KST value renders 9h off).

It only diverges for runs landing between 15:00Z and 24:00Z, which is why it
hid for months — and then cost `research/digest/2026-07-24-digest.md`
entirely when a runner outage pushed the 00:00Z digest to 16:13Z: local had
already rolled to 07-25, so 07-24 was never written.

`date +%s` is exempt: epoch seconds are timezone-independent.
"""

import re
import unittest
from pathlib import Path

WORKFLOW_DIR = Path(__file__).resolve().parent.parent / ".github" / "workflows"

# A `date` call with a quoted format string, not already in UTC mode.
# `date -u +'...'` and `date +%s` both pass.
LOCAL_DATE_RE = re.compile(r"\bdate\s+\+['\"]")

# A real `$(date ...)` command substitution, capturing its arguments.
DATE_SUBSTITUTION_RE = re.compile(r"\$\(\s*date\b([^()]*)\)")


class WorkflowTimeConventionTest(unittest.TestCase):
    def test_no_workflow_formats_dates_in_local_time(self):
        offenders = []
        for path in sorted(WORKFLOW_DIR.glob("*.yml")):
            for lineno, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if LOCAL_DATE_RE.search(line):
                    offenders.append(f"{path.name}:{lineno}: {line.strip()}")
        self.assertEqual(
            [],
            offenders,
            "workflows must use `date -u` — the runner is KST but every "
            "consumer reads these values as UTC:\n  " + "\n  ".join(offenders),
        )

    def test_utc_labelled_timestamps_are_actually_utc(self):
        """A format string containing 'UTC' must be produced by `date -u`.

        Scoped to real `$(date ...)` substitutions: a looser pattern matched
        the JSON key in `{"date":"...","hour":"...:00 UTC"}` in
        hourly-twitter.yml, which is a template field, not a date call.
        """
        offenders = []
        for path in sorted(WORKFLOW_DIR.glob("*.yml")):
            for lineno, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                for call in DATE_SUBSTITUTION_RE.finditer(line):
                    args = call.group(1)
                    if "UTC" in args and "-u" not in args:
                        offenders.append(f"{path.name}:{lineno}: {line.strip()}")
        self.assertEqual(
            [], offenders,
            "these format a 'UTC'-labelled string from local time:\n  "
            + "\n  ".join(offenders),
        )

    def test_guard_actually_detects_a_violation(self):
        """Control: the regex must catch the exact shape that was in the tree,
        so a future refactor cannot quietly neuter this suite."""
        self.assertRegex("""          echo "date=$(date +'%Y-%m-%d')" """, LOCAL_DATE_RE)
        self.assertRegex('''          TS=$(date +"%Y-%m-%d")''', LOCAL_DATE_RE)
        # ...and must not fire on the corrected forms or on epoch seconds.
        self.assertNotRegex("""          echo "date=$(date -u +'%Y-%m-%d')" """, LOCAL_DATE_RE)
        self.assertNotRegex("          NOW=$(date +%s)", LOCAL_DATE_RE)
        self.assertNotRegex("          NOW=$(date -u +%s)", LOCAL_DATE_RE)

    def test_utc_guard_detects_a_violation_and_ignores_json_keys(self):
        """Control for the second guard, including the false positive that a
        looser pattern produced on hourly-twitter.yml's heartbeat template."""
        def utc_offenders(line):
            return [
                m.group(1) for m in DATE_SUBSTITUTION_RE.finditer(line)
                if "UTC" in m.group(1) and "-u" not in m.group(1)
            ]

        self.assertTrue(utc_offenders("""TS=$(date +'%Y-%m-%d %H:%M UTC')"""))
        self.assertFalse(utc_offenders("""TS=$(date -u +'%Y-%m-%d %H:%M UTC')"""))
        # JSON template field named "date" alongside a literal UTC — not a call.
        self.assertFalse(utc_offenders(
            '{"date":"${{ steps.datetime.outputs.date }}","hour":"${{ x }}:00 UTC"}'
        ))


if __name__ == "__main__":
    unittest.main()
