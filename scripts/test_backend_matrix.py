"""Invariant tests for the backend routing SSOT (data/agent-backends.json)
and its validator/generator (scripts/build_backend_matrix.py).

These pin the load-bearing routing facts — if a change flips one, the test
failing is the signal to update BOTH the routing intent and this pin, not to
loosen the parser. (Doc-freshness itself is the separate `--check` CI step.)
"""

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from build_backend_matrix import (
    LANES_FILE,
    check_fallback,
    cross_check,
    load_lanes,
    load_profiles,
    observe_workflow,
    workflow_files,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
RESOLVER = REPO_ROOT / "scripts" / "resolve_backend_lane.py"


def observations():
    return {p.name: observe_workflow(p) for p in workflow_files()}


class RoutingInvariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lanes, cls.fallback = load_lanes()
        cls.profiles = load_profiles()
        cls.obs = observations()

    def test_cross_check_is_clean_on_repo_state(self):
        errors = check_fallback(self.fallback, self.profiles) \
            + cross_check(self.lanes, self.obs, self.profiles)
        self.assertEqual(errors, [])

    def test_global_fallback_chain_shape(self):
        self.assertEqual(self.fallback["harness"], "agent-run")
        chain = self.fallback["chain"]
        self.assertIsInstance(chain, list)
        self.assertGreaterEqual(len(chain), 1)
        # Terminal claude guarantees selection always succeeds when the
        # OAuth token exists. Deliberate invariant — change it only if you
        # accept lanes that can hard-fail with every provider down.
        self.assertEqual(self.profiles[chain[-1]].provider, "claude")
        self.assertTrue(self.fallback["native_model"])

    def test_every_agent_run_lane_backend_has_a_profile(self):
        for key, lane in self.lanes.items():
            if lane.get("harness") == "agent-run":
                self.assertIn(lane["backend"], self.profiles, key)

    def test_zai_canary_is_pinned_and_strict(self):
        canary = self.lanes["zai-canary"]
        self.assertTrue(canary.get("pinned"), "canary must stay pinned to zai")
        self.assertIs(canary.get("strict"), True,
                      "canary must never walk the fallback chain — a Z.ai outage "
                      "has to fail the diagnostic, not silently test Claude")
        self.assertEqual(self.profiles[canary["backend"]].provider, "zai")

    def test_hourly_twitter_covers_all_five_tiers(self):
        tiers = {l.get("tier") for l in self.lanes.values()
                 if l.get("workflow") == "hourly-twitter.yml"}
        self.assertLessEqual(
            {"claude", "deepseek-claude-code", "zai-glm-5p2", "deepseek-pi", "fireworks-pi"},
            tiers,
        )

    def test_primary_twitter_lanes_route_to_claude(self):
        for lane in ("twitter-primary", "twitter-judge", "twitter-autoresearch"):
            self.assertEqual(self.lanes[lane]["backend"], "claude", lane)

    def test_twitter_deterministic_fallback_is_primary_lane_only(self):
        hourly = self.obs["hourly-twitter.yml"]
        self.assertEqual(
            hourly.det_by_lane,
            {"twitter-primary": "deterministic_twitter_digest.py"},
        )
        self.assertEqual(hourly.det_by_tier, {})

    def test_pi_mirror_matches_workflow(self):
        pi_models = {s.model for s in self.obs["hourly-twitter.yml"].pi}
        self.assertEqual(
            pi_models,
            {self.lanes["twitter-deepseek-pi"]["model"], self.lanes["twitter-fireworks-pi"]["model"]},
        )

    def test_all_agent_run_call_sites_carry_all_provider_secrets(self):
        for obs in self.obs.values():
            for step in obs.agent_run:
                self.assertEqual(step.secrets["claude-code-oauth-token"], "CLAUDE_CODE_OAUTH_TOKEN", step)
                self.assertEqual(step.secrets["fireworks-api-key"], "FIREWORKS_API_KEY", step)
                self.assertEqual(step.secrets["zai-api-key"], "ZAI_API_KEY", step)

    def test_gen_research_default_is_runtime_resolved(self):
        self.assertIn("generative-research-default",
                      self.obs["generative-research.yml"].resolver_lanes)

    def test_gen_research_fable_is_explicit_and_fail_closed(self):
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "generative-research.yml").read_text(encoding="utf-8")
        self.assertIn('- fable-5', workflow)
        self.assertIn('fable-5) model="claude-fable-5"', workflow)
        self.assertIn('ANTHROPIC_DEFAULT_OPUS_MODEL: ${{ steps.native-model.outputs.model }}', workflow)
        self.assertIn('CLAUDE_CODE_SUBAGENT_MODEL: ${{ steps.native-model.outputs.model }}', workflow)
        self.assertIn('--model ${{ steps.native-model.outputs.model }}', workflow)
        self.assertIn('--model "$GEN_MODEL"', workflow)
        self.assertIn("if: steps.effective.outputs.backend == 'claude'\n        id: claude-attempt-1", workflow)
        self.assertIn("Verify Fable model provenance", workflow)
        self.assertIn("actual_model=$(jq -r", workflow)
        self.assertTrue(self.obs["generative-research.yml"].has_fable_dispatch)
        self.assertEqual(self.lanes["generative-research-default"]["backend"], "claude")

    def test_comparison_tiers_are_strict(self):
        # Comparison artifacts must be attributable to their labeled backend:
        # a silent chain re-route would corrupt the comparison (round-3 F1).
        for lane in ("twitter-zai", "twitter-deepseek", "zai-canary"):
            self.assertTrue(self.lanes[lane].get("strict"), lane)

    def test_readme_diagram_generated_and_deterministic(self):
        from build_backend_matrix import build_generated_blocks
        _, diagram1 = build_generated_blocks()
        _, diagram2 = build_generated_blocks()
        self.assertEqual(diagram1, diagram2)
        self.assertIn("flowchart LR", diagram1)
        self.assertIn("claude-sonnet-5", diagram1)
        self.assertIn("fallback chain: `claude`", diagram1)
        self.assertIn("zai-canary", diagram1)


class CrossCheckEnforcement(unittest.TestCase):
    """The cross-check must FAIL on each violation class, not just pass on
    the happy path."""

    @classmethod
    def setUpClass(cls):
        cls.lanes, cls.fallback = load_lanes()
        cls.profiles = load_profiles()
        cls.obs = observations()

    def mutated(self):
        return copy.deepcopy(self.lanes), copy.deepcopy(self.obs)

    def test_missing_secret_is_an_error(self):
        lanes, obs = self.mutated()
        obs["hourly-rss.yml"].agent_run[0].secrets["zai-api-key"] = ""
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("zai-api-key" in e for e in errors), errors)

    def test_explicit_backend_in_workflow_is_an_error(self):
        lanes, obs = self.mutated()
        obs["hourly-rss.yml"].agent_run[0].raw_backend = "fireworks-glm-5p2"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("explicit backend" in e for e in errors), errors)

    def test_unknown_lane_is_an_error(self):
        lanes, obs = self.mutated()
        obs["hourly-rss.yml"].agent_run[0].lane = "no-such-lane"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("not defined" in e for e in errors), errors)

    def test_orphan_lane_is_an_error(self):
        lanes, obs = self.mutated()
        lanes["ghost"] = {"workflow": "hourly-rss.yml", "harness": "agent-run",
                          "backend": "fireworks-glm-5p2"}
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("orphan" in e for e in errors), errors)

    def test_pi_mirror_divergence_is_an_error(self):
        lanes, obs = self.mutated()
        lanes["twitter-fireworks-pi"]["model"] = "accounts/fireworks/models/other"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("mirror contract" in e for e in errors), errors)

    def test_native_mirror_divergence_is_an_error(self):
        lanes, obs = self.mutated()
        lanes["claude-code-review"]["model"] = "claude-opus-4-8"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("claude-code-review" in e and "mirror" in e for e in errors), errors)

    def test_unsupported_gen_research_default_is_an_error(self):
        lanes, obs = self.mutated()
        lanes["generative-research-default"]["backend"] = "zai-glm-5p2"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("not supported by" in e for e in errors), errors)

    def test_rerouting_a_pinned_lane_is_an_error(self):
        lanes, obs = self.mutated()
        lanes["zai-canary"]["backend"] = "fireworks-glm-5p2"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("PINNED" in e for e in errors), errors)

    def test_pinned_lane_without_declared_provider_is_an_error(self):
        lanes, obs = self.mutated()
        del lanes["zai-canary"]["pinned_provider"]
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("pinned_provider" in e for e in errors), errors)

    def test_lying_tier_in_ssot_is_an_error(self):
        lanes, obs = self.mutated()
        lanes["twitter-judge"]["tier"] = "deepseek-claude-code"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("must not lie about tier" in e for e in errors), errors)

    def test_rerouted_direct_action_outside_gen_research_is_an_error(self):
        lanes, obs = self.mutated()
        obs["ai-news-research.yml"].native[0].rerouted_provider = "zai"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("outside generative-research.yml" in e for e in errors), errors)

    def test_duplicate_lane_across_steps_is_an_error(self):
        lanes, obs = self.mutated()
        obs["hourly-rss.yml"].agent_run[0].lane = "bluesky"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("2 agent-run steps" in e for e in errors), errors)

    def test_lane_workflow_mismatch_is_an_error(self):
        lanes, obs = self.mutated()
        lanes["rss"]["workflow"] = "2h-bluesky.yml"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("belongs to workflow" in e for e in errors), errors)

    def test_wrong_harness_for_agent_run_lane_is_an_error(self):
        lanes, obs = self.mutated()
        lanes["rss"]["harness"] = "pi"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("expected agent-run" in e for e in errors), errors)

    def test_unknown_chain_entry_is_an_error(self):
        errors = check_fallback({"harness": "agent-run", "chain": ["nonsense"],
                                 "native_model": "claude-sonnet-5"}, self.profiles)
        self.assertTrue(any("not in the backends table" in e for e in errors), errors)

    def test_empty_chain_is_an_error(self):
        errors = check_fallback({"harness": "agent-run", "chain": [],
                                 "native_model": "claude-sonnet-5"}, self.profiles)
        self.assertTrue(any("non-empty" in e for e in errors), errors)

    def test_duplicate_chain_entry_is_an_error(self):
        errors = check_fallback({"harness": "agent-run", "chain": ["claude", "claude"],
                                 "native_model": "claude-sonnet-5"}, self.profiles)
        self.assertTrue(any("duplicates" in e for e in errors), errors)

    def test_non_boolean_strict_is_an_error(self):
        lanes, obs = self.mutated()
        lanes["rss"]["strict"] = "yes"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("strict must be a boolean" in e for e in errors), errors)

    def test_fallback_missing_native_model_is_an_error(self):
        errors = check_fallback({"harness": "agent-run", "chain": ["claude"]}, self.profiles)
        self.assertTrue(any("native_model" in e for e in errors), errors)


class ResolverCli(unittest.TestCase):
    def run_resolver(self, *args):
        return subprocess.run([sys.executable, str(RESOLVER), *args],
                              capture_output=True, text=True)

    def test_resolves_lane_backend(self):
        lanes, _ = load_lanes()
        result = self.run_resolver("twitter-judge")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), lanes["twitter-judge"]["backend"])

    def test_resolves_dotted_fallback_paths(self):
        data = json.loads(LANES_FILE.read_text())
        result = self.run_resolver("--top", "fallback.native_model")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), data["fallback"]["native_model"])

    def test_missing_dotted_path_fails_fast(self):
        result = self.run_resolver("--top", "fallback.nope")
        self.assertEqual(result.returncode, 2)

    def test_unknown_lane_fails_fast(self):
        result = self.run_resolver("no-such-lane")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown lane", result.stderr)


if __name__ == "__main__":
    unittest.main()
