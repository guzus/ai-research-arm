import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from deterministic_twitter_digest import main
from validate_twitter_public_output import validate


class DeterministicTwitterDigestTest(unittest.TestCase):
    def run_fallback(
        self,
        root: Path,
        *,
        hour: str = "12",
        timestamp: str = "2026-07-12 12:07 UTC",
        run_id: str = "1234",
        run_attempt: str = "1",
    ) -> tuple[Path, Path, Path]:
        input_dir = root / "bird"
        out_dir = root / "research" / "twitter"
        summaries_dir = root / "research" / "summaries"
        headlines_file = summaries_dir / f"2026-07-12-twitter-{hour}h-headlines.json"
        input_dir.mkdir(parents=True, exist_ok=True)

        rc = main(
            [
                "--input-dir",
                str(input_dir),
                "--out-dir",
                str(out_dir),
                "--summaries-dir",
                str(summaries_dir),
                "--date",
                "2026-07-12",
                "--hour",
                hour,
                "--timestamp",
                timestamp,
                "--run-id",
                run_id,
                "--run-attempt",
                run_attempt,
                "--summary-slug",
                "twitter",
                "--headlines-file",
                str(headlines_file),
            ]
        )
        self.assertEqual(rc, 0)
        return out_dir, summaries_dir, headlines_file

    def test_fresh_source_payload_never_becomes_fallback_news(self) -> None:
        """Regression: raw GPT-5.6/GPT-Live/Grok posts must not be authored into news."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "bird"
            input_dir.mkdir()
            (input_dir / "all.json").write_text(
                json.dumps(
                    {
                        "accounts": {
                            "OpenAI": [
                                {
                                    "id": "2074704958419792299",
                                    "author": {"username": "OpenAI"},
                                    "text": "GPT-5.6 Sol, Terra, and Luna will launch publicly this Thursday.",
                                    "createdAt": "Sun Jul 12 11:59:00 +0000 2026",
                                    "likeCount": 50000,
                                },
                                {
                                    "id": "2074907025537224840",
                                    "author": {"username": "OpenAI"},
                                    "text": "Introducing GPT-Live, rolling out in ChatGPT starting today.",
                                    "createdAt": "Sun Jul 12 12:00:00 +0000 2026",
                                    "likeCount": 20000,
                                },
                            ],
                            "elonmusk": [
                                {
                                    "id": "2074912099554201969",
                                    "author": {"username": "elonmusk"},
                                    "text": "Grok 4.5 has 2x inference-speed headroom.",
                                    "createdAt": "Sun Jul 12 12:01:00 +0000 2026",
                                    "likeCount": 30000,
                                }
                            ],
                        },
                        "searches": {},
                        "news": [],
                    }
                ),
                encoding="utf-8",
            )

            out_dir, summaries_dir, headlines_file = self.run_fallback(root)

            self.assertFalse((out_dir / "2026-07-12.md").exists())
            self.assertEqual(
                (summaries_dir / "2026-07-12-twitter-12h-summary.txt").read_text(encoding="utf-8"),
                "",
            )
            self.assertEqual(json.loads(headlines_file.read_text(encoding="utf-8")), [])
            status = json.loads((out_dir / "status" / "2026-07-12-12h.json").read_text(encoding="utf-8"))
            self.assertEqual(status["status"], "no_update")
            self.assertEqual(status["public_items"], 0)
            self.assertIs(status["recovery"], True)
            self.assertEqual(status["run_id"], "1234")
            validate(
                backend="claude",
                status_file=out_dir / "status" / "2026-07-12-12h.json",
                digest_file=out_dir / "2026-07-12.md",
                summary_file=summaries_dir / "2026-07-12-twitter-12h-summary.txt",
                headlines_file=headlines_file,
                date="2026-07-12",
                hour="12",
                generated_at="2026-07-12 12:07 UTC",
                run_id="1234",
                run_attempt=1,
            )

    def test_fallback_never_edits_public_digest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            digest_path = root / "research" / "twitter" / "2026-07-12.md"
            digest_path.parent.mkdir(parents=True)
            existing = (
                "# Twitter/X AI Pulse - 2026-07-12\n\n"
                "## 09:00 UTC\n\n"
                "**Cycle summary**: Prior analyst update.\n\n"
                "## 13:00 UTC\n\n"
                "**Cycle summary**: Failed-agent mutation at the wrong hour.\n"
            )
            digest_path.write_text(existing, encoding="utf-8")

            self.run_fallback(root)

            self.assertEqual(digest_path.read_text(encoding="utf-8"), existing)

    def test_workflow_restore_preserves_baseline_and_removes_all_agent_mutations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
            digest_path = repo / "research" / "twitter" / "2026-07-12.md"
            digest_path.parent.mkdir(parents=True)
            baseline = (
                "# Twitter/X AI Pulse - 2026-07-12\n\n"
                "## 12:00 UTC\n\n"
                "**Cycle summary**: Previously committed valid same-hour section.\n"
            )
            digest_path.write_text(baseline, encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repo, check=True)
            base_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()

            digest_path.write_text(
                "# Twitter/X AI Pulse - corrupted\n\n"
                "## 12:00 UTC\n\n**Cycle summary**: Corrupted current-hour section.\n\n"
                "## 13:00 UTC\n\n**Cycle summary**: Unexpected wrong-hour mutation.\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "agent mutation"], cwd=repo, check=True)

            subprocess.run(
                ["git", "restore", f"--source={base_sha}", "--", "research/twitter/2026-07-12.md"],
                cwd=repo,
                check=True,
            )
            subprocess.run(
                ["git", "add", "research/twitter/2026-07-12.md"],
                cwd=repo,
                check=True,
            )

            self.assertEqual(digest_path.read_text(encoding="utf-8"), baseline)
            self.assertEqual(
                subprocess.run(
                    ["git", "diff", "--quiet", base_sha, "--", "research/twitter/2026-07-12.md"],
                    cwd=repo,
                    check=False,
                ).returncode,
                0,
            )

    def test_workflow_removes_digest_absent_from_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
            (repo / "README").write_text("baseline\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repo, check=True)
            digest_path = repo / "research" / "twitter" / "2026-07-12.md"
            digest_path.parent.mkdir(parents=True)
            digest_path.write_text("agent-created corruption\n", encoding="utf-8")

            digest_path.unlink()

            self.assertFalse(digest_path.exists())

    def test_no_update_rerun_is_idempotent_and_refreshes_heartbeat(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out_dir, _, _ = self.run_fallback(root)
            out_dir, summaries_dir, headlines_file = self.run_fallback(
                root,
                timestamp="2026-07-12 12:12 UTC",
                run_attempt="2",
            )

            self.assertFalse((out_dir / "2026-07-12.md").exists())
            self.assertEqual(
                (summaries_dir / "2026-07-12-twitter-12h-summary.txt").read_text(encoding="utf-8"),
                "",
            )
            self.assertEqual(json.loads(headlines_file.read_text(encoding="utf-8")), [])
            status = json.loads((out_dir / "status" / "2026-07-12-12h.json").read_text(encoding="utf-8"))
            self.assertEqual(status["generated_at"], "2026-07-12 12:12 UTC")
            self.assertEqual(status["run_attempt"], 2)
            self.assertEqual(status["status"], "no_update")
            self.assertEqual(status["public_items"], 0)

    def test_workflow_publishes_recovery_then_fails_loud(self) -> None:
        workflow = (
            Path(__file__).resolve().parent.parent / ".github" / "workflows" / "hourly-twitter.yml"
        ).read_text(encoding="utf-8")

        push_index = workflow.index("      - name: Push changes")
        fail_index = workflow.index("      - name: Fail recovered Claude cycle")
        restore_index = workflow.index('if git cat-file -e "${BASE_SHA}:${DIGEST_FILE}"')
        fallback_index = workflow.index("uv run python scripts/deterministic_twitter_digest.py")
        reserved_index = workflow.index(
            "fallback-needed: recovery status is reserved for the deterministic recovery path"
        )
        self.assertLess(reserved_index, restore_index)
        self.assertLess(restore_index, fallback_index)
        restore_block = workflow[restore_index:fallback_index]
        self.assertIn('git restore --source="$BASE_SHA" -- "$DIGEST_FILE"', restore_block)
        self.assertIn('rm -f "$DIGEST_FILE"', restore_block)
        self.assertLess(push_index, fail_index)
        self.assertIn('echo "recovered=true" >> "$GITHUB_OUTPUT"', workflow)
        fail_step = workflow[fail_index : workflow.index("\n      - name:", fail_index + 1)]
        self.assertIn("steps.recover_claude.outputs.recovered == 'true'", fail_step)
        self.assertIn("exit 1", fail_step)


if __name__ == "__main__":
    unittest.main()
