#!/usr/bin/env python3
"""Pin the CI inputs that protect committed data contracts."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"

REQUIRED_CONTRACT_PATHS = {
    ".dockerignore",
    ".opencode/tools/**",
    "data/sources/ai_blogs.json",
    "prompts/**",
    "research/models/tickets/**",
    "research/wiki/**",
    "research/wiki-translations/**",
    "research/generative/**",
    "research/front-page/*.ara.md",
    "research/claims/index.json",
    "pyproject.toml",
    "uv.lock",
    "ARA_CATALOG.json",
    "COMPONENTS.md",
    "data/artifact-slos.json",
}
BROAD_RESEARCH_GLOBS = {"research/**", "research/**/*", "research/**/**"}


def load_ci_workflow() -> dict[str, object]:
    # BaseLoader keeps GitHub's `on` key as text instead of applying YAML 1.1's
    # legacy boolean conversion.
    return yaml.load(CI_WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


class CiWorkflowContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = load_ci_workflow()

    def test_push_and_pull_request_cover_committed_contract_inputs(self) -> None:
        triggers = self.workflow["on"]
        self.assertIsInstance(triggers, dict)
        push_paths = triggers["push"]["paths"]
        pull_request_paths = triggers["pull_request"]["paths"]

        self.assertEqual(push_paths, pull_request_paths)
        self.assertTrue(
            REQUIRED_CONTRACT_PATHS.issubset(push_paths),
            f"CI contract paths missing: {sorted(REQUIRED_CONTRACT_PATHS - set(push_paths))}",
        )
        self.assertFalse(
            BROAD_RESEARCH_GLOBS.intersection(push_paths),
            "Raw high-frequency research lanes must not trigger the full CI workflow: "
            f"{sorted(BROAD_RESEARCH_GLOBS.intersection(push_paths))}",
        )

    def test_dashboard_job_runs_unit_tests(self) -> None:
        dashboard = self.workflow["jobs"]["dashboard"]
        run_commands = [step.get("run") for step in dashboard["steps"] if "run" in step]
        self.assertIn("bun run test", run_commands)


if __name__ == "__main__":
    unittest.main()
