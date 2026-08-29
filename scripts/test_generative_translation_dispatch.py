"""Workflow invariants for automatic Korean generative-research translation."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent


def _workflow(name: str) -> dict:
    return yaml.safe_load(
        (REPO_ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
    )


class GenerativeTranslationDispatchTest(unittest.TestCase):
    def test_production_article_dispatches_final_slug_for_auto_merge(self):
        workflow = _workflow("generative-research.yml")
        job = workflow["jobs"]["generative-research"]
        self.assertEqual(job["permissions"]["actions"], "write")

        steps = job["steps"]
        by_id = {step.get("id"): step for step in steps if step.get("id")}
        dispatch = by_id["dispatch-translation"]
        self.assertGreater(steps.index(dispatch), steps.index(by_id["push"]))
        self.assertNotIn("continue-on-error", dispatch)

        condition = dispatch["if"]
        self.assertIn("steps.outfile.outputs.has_file == 'true'", condition)
        self.assertIn("steps.push.outputs.pushed == 'true'", condition)
        self.assertIn(
            "steps.publish-branch.outputs.branch == github.event.repository.default_branch",
            condition,
        )
        self.assertEqual(
            dispatch["env"]["ARTICLE_SLUG"], "${{ steps.outfile.outputs.slug }}"
        )
        command = dispatch["run"]
        self.assertIn("gh workflow run translate-generative-research.yml", command)
        self.assertIn('--repo "$GITHUB_REPOSITORY"', command)
        self.assertIn('--ref "$DEFAULT_BRANCH"', command)
        self.assertIn('-f "slug=$ARTICLE_SLUG"', command)
        self.assertIn("-f auto_merge=true", command)

        identify = by_id["outfile"]["run"]
        self.assertIn('map(select(.file == $file))', identify)
        self.assertIn('echo "slug=$ARTICLE_SLUG"', identify)
        self.assertIn('} >> "$GITHUB_OUTPUT"', identify)

    def test_distinct_articles_queue_and_read_latest_main(self):
        workflow = _workflow("translate-generative-research.yml")
        concurrency = workflow["concurrency"]
        self.assertIn("${{ inputs.slug }}", concurrency["group"])
        self.assertIs(concurrency["cancel-in-progress"], False)

        checkout = next(
            step
            for step in workflow["jobs"]["translate"]["steps"]
            if str(step.get("uses", "")).startswith("actions/checkout@")
        )
        self.assertEqual(
            "${{ github.event.repository.default_branch }}", checkout["with"]["ref"]
        )


if __name__ == "__main__":
    unittest.main()
