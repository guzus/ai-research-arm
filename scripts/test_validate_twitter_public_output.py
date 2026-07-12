import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_twitter_public_output import ContractError, validate


class ValidateTwitterPublicOutputTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.status = self.root / "status.json"
        self.digest = self.root / "digest.md"
        self.summary = self.root / "summary.txt"
        self.headlines = self.root / "headlines.json"
        self.headlines.write_text("[]\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_status(
        self,
        state: str,
        public_items: int,
        generated_at: str = "2026-07-10 10:07:09 UTC",
        *,
        recovery: bool | None = None,
    ) -> None:
        payload = {
            "schema_version": 1,
            "date": "2026-07-10",
            "hour": "10:00 UTC",
            "generated_at": generated_at,
            "run_id": "1234",
            "run_attempt": 2,
            "status": state,
            "public_items": public_items,
        }
        if recovery is not None:
            payload["recovery"] = recovery
        self.status.write_text(
            json.dumps(payload),
            encoding="utf-8",
        )

    def validate(self) -> None:
        validate(
            backend="claude",
            status_file=self.status,
            digest_file=self.digest,
            summary_file=self.summary,
            headlines_file=self.headlines,
            date="2026-07-10",
            hour="10",
            generated_at="2026-07-10 10:07:09 UTC",
            run_id="1234",
            run_attempt=2,
        )

    def test_accepts_concrete_published_section(self) -> None:
        self.write_status("published", 2)
        self.summary.write_text("Concrete Meta API and safety update.\n", encoding="utf-8")
        self.digest.write_text(
            "# Twitter/X AI Pulse\n\n"
            "## 10:00 UTC\n\n"
            "**Cycle summary**: Meta released Muse Spark 1.1 and a public Model API preview.\n\n"
            "<article class=\"twitter-story\">"
            "<h3 class=\"twitter-story-title\">Muse Spark 1.1</h3>"
            "<p class=\"twitter-story-lead\">Meta released the model and API preview.</p>"
            "<a class=\"twitter-source-chip\" href=\"https://x.com/AIatMeta/status/122\">@AIatMeta</a>"
            "</article>\n\n"
            "### Quick hits\n"
            "- @AIatMeta: Model API preview [source](https://x.com/AIatMeta/status/123)\n",
            encoding="utf-8",
        )
        self.validate()

    def test_rejects_summary_only_fake_publication(self) -> None:
        self.write_status("published", 1)
        self.summary.write_text("AI agents are the future.\n", encoding="utf-8")
        self.digest.write_text(
            "## 10:00 UTC\n\n**Cycle summary**: AI agents are the future.\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ContractError, "no story card"):
            self.validate()

    def test_rejects_empty_story_shell(self) -> None:
        self.write_status("published", 1)
        self.summary.write_text("Meta released Muse Spark 1.1.\n", encoding="utf-8")
        self.digest.write_text(
            "## 10:00 UTC\n\n"
            "**Cycle summary**: Meta released Muse Spark 1.1.\n\n"
            "<article class=\"twitter-story\"></article>\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ContractError, "no story card"):
            self.validate()

    def test_rejects_story_with_source_only_in_html_comment(self) -> None:
        self.write_status("published", 1)
        self.summary.write_text("Meta released Muse Spark 1.1.\n", encoding="utf-8")
        self.digest.write_text(
            "## 10:00 UTC\n\n"
            "**Cycle summary**: Meta released Muse Spark 1.1.\n\n"
            "<article class=\"twitter-story\">"
            "<h3 class=\"twitter-story-title\">Muse Spark 1.1</h3>"
            "<p class=\"twitter-story-lead\">Meta released a model.</p>"
            "<!-- <a class=\"twitter-source-chip\" "
            "href=\"https://x.com/AIatMeta/status/122\">source</a> -->"
            "</article>\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ContractError, "no story card"):
            self.validate()

    def test_rejects_html_entity_only_story_text(self) -> None:
        self.write_status("published", 1)
        self.summary.write_text("Meta released Muse Spark 1.1.\n", encoding="utf-8")
        self.digest.write_text(
            "## 10:00 UTC\n\n"
            "**Cycle summary**: Meta released Muse Spark 1.1.\n\n"
            "<article class=\"twitter-story\">"
            "<h3 class=\"twitter-story-title\">&nbsp;</h3>"
            "<p class=\"twitter-story-lead\">&#160;</p>"
            "<a class=\"twitter-source-chip\" "
            "href=\"https://x.com/AIatMeta/status/122\">source</a>"
            "</article>\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ContractError, "no story card"):
            self.validate()

    def test_trailing_space_heading_counts_as_public_section(self) -> None:
        self.write_status("no_update", 0)
        self.summary.write_text("", encoding="utf-8")
        self.digest.write_text(
            "# Twitter/X AI Pulse\r\n\r\n## 10:00 UTC \r\n\r\n"
            "**Cycle summary**: Hidden card.\r\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ContractError, "must not leave"):
            self.validate()

    def test_recovery_no_update_accepts_baseline_same_hour_section(self) -> None:
        self.write_status("no_update", 0, recovery=True)
        self.summary.write_text("", encoding="utf-8")
        self.digest.write_text(
            "# Twitter/X AI Pulse\n\n## 10:00 UTC\n\n"
            "**Cycle summary**: Previously committed valid update.\n",
            encoding="utf-8",
        )
        self.validate()

    def test_rejects_stale_run_identity(self) -> None:
        self.write_status("no_update", 0, generated_at="2026-07-10 10:07:00 UTC")
        self.summary.write_text("", encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "generated_at"):
            self.validate()

    def test_rejects_operational_filler_anywhere_in_section(self) -> None:
        self.write_status("published", 1)
        self.summary.write_text("Concrete launch.\n", encoding="utf-8")
        self.digest.write_text(
            "## 10:00 UTC\n\n"
            "**Cycle summary**: Meta released Muse Spark 1.1.\n\n"
            "<article class=\"twitter-story\"></article>\n\n"
            "### Watch list (next 24h)\n- Next scheduled Twitter/X AI monitor run.\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ContractError, "operational/no-news filler"):
            self.validate()

    def test_rejects_equivalent_no_news_narration(self) -> None:
        phrases = (
            "No noteworthy AI updates this cycle.",
            "No significant AI developments in this window.",
            "None this cycle.",
            "Monitoring found no material AI changes.",
            "Only earlier AI items repeated.",
            "No follow-ups needed — pre-fetched snapshot was sufficient.",
        )
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.write_status("published", 1)
                self.summary.write_text("Meta released Muse Spark 1.1.\n", encoding="utf-8")
                self.digest.write_text(
                    "## 10:00 UTC\n\n"
                    "**Cycle summary**: Meta released Muse Spark 1.1.\n\n"
                    "### Quick hits\n"
                    "- @AIatMeta: Muse Spark 1.1 released "
                    "[source](https://x.com/AIatMeta/status/123)\n\n"
                    f"### Watch list (next 24h)\n- {phrase}\n",
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ContractError, "operational/no-news filler"):
                    self.validate()


if __name__ == "__main__":
    unittest.main()
