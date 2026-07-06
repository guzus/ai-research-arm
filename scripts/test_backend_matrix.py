"""Invariant tests for scripts/build_backend_matrix.py.

These pin the load-bearing facts the matrix must keep reporting correctly —
if a workflow edit changes one of these, the test failing is the signal to
update BOTH the workflow intent and this pin, not to loosen the parser.
(The doc-sync gate itself is the separate `--check` step in ci.yml.)
"""

import unittest

from build_backend_matrix import (
    AGENT_RUN_ACTION,
    agent_run_defaults,
    load_yaml,
    parse_agent_run_profiles,
    rows_for_workflow,
    workflow_files,
)


def all_rows():
    action = load_yaml(AGENT_RUN_ACTION)
    profiles = parse_agent_run_profiles(action)
    defaults = agent_run_defaults(action)
    rows = []
    for wf_path in workflow_files():
        rows.extend(rows_for_workflow(wf_path, profiles, defaults))
    return rows


class BackendMatrixInvariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = all_rows()

    def rows_for(self, workflow):
        return [r for r in self.rows if r.workflow == workflow]

    def test_profiles_cover_known_backends(self):
        profiles = parse_agent_run_profiles(load_yaml(AGENT_RUN_ACTION))
        normalized = {p.normalized for p in profiles.values()}
        self.assertLessEqual(
            {"claude", "fireworks-glm-5p2", "fireworks-deepseek-v4-flash", "zai-glm-5p2"},
            normalized,
        )

    def test_zai_lanes_use_zai_key_and_fail_closed(self):
        zai_rows = [r for r in self.rows if "Z.ai" in r.provider]
        self.assertGreaterEqual(len(zai_rows), 2)  # twitter tier + canary
        for row in zai_rows:
            self.assertEqual(row.token, "ZAI_API_KEY", row)
            self.assertIn("hard fail", row.fallback, row)

    def test_fireworks_lanes_use_fireworks_key(self):
        fw_rows = [r for r in self.rows if "Fireworks" in r.provider or "fireworks" in r.provider]
        self.assertGreaterEqual(len(fw_rows), 10)
        for row in fw_rows:
            self.assertEqual(row.token, "FIREWORKS_API_KEY", row)

    def test_hourly_twitter_covers_all_five_tiers(self):
        tiers = {r.lane.split(" ")[0] for r in self.rows_for("hourly-twitter.yml")}
        self.assertLessEqual(
            {"tier:claude", "tier:deepseek-claude-code", "tier:zai-glm-5p2",
             "tier:deepseek-pi", "tier:fireworks-pi"},
            tiers,
        )

    def test_hourly_twitter_pi_tiers_use_pi_harness(self):
        pi_rows = [r for r in self.rows_for("hourly-twitter.yml") if "pi ·" in r.harness]
        self.assertEqual(len(pi_rows), 2)
        models = {r.model for r in pi_rows}
        self.assertIn("`accounts/fireworks/models/kimi-k2p7`", models)

    def test_generative_research_has_codex_lane(self):
        codex_rows = [r for r in self.rows_for("generative-research.yml") if r.harness == "Codex CLI"]
        self.assertEqual(len(codex_rows), 1)
        self.assertEqual(codex_rows[0].token, "CODEX_AUTH_JSON")

    def test_native_lanes_use_oauth_token(self):
        native = [r for r in self.rows if r.provider == "Anthropic (native)"]
        self.assertGreaterEqual(len(native), 5)
        for row in native:
            self.assertEqual(row.token, "CLAUDE_CODE_OAUTH_TOKEN", row)

if __name__ == "__main__":
    unittest.main()
