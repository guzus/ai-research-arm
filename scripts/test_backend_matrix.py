"""Invariant tests for the backend routing SSOT (data/agent-backends.json)
and its validator/generator (scripts/build_backend_matrix.py).

These pin the load-bearing routing facts — if a change flips one, the test
failing is the signal to update BOTH the routing intent and this pin, not to
loosen the parser. (Doc-freshness itself is the separate `--check` CI step.)
"""

import copy
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

import yaml

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
        # The chain LEADS with native Claude: it is the default backend and
        # the model every lane prompt is tuned against.
        self.assertEqual(self.profiles[chain[0]].provider, "claude")
        # ...but it must not TERMINATE there. The old invariant pinned
        # claude last, reasoning that "terminal claude guarantees selection
        # always succeeds when the OAuth token exists". 2026-07-24 falsified
        # the premise: the token existed and was dead, selection duly
        # "succeeded" onto Claude, and every agent lane in the fleet failed
        # instantly with no route out. Selection succeeding is worthless if
        # the selected backend cannot serve. Require a second provider so a
        # single dead credential cannot strand the whole fleet.
        providers = [self.profiles[key].provider for key in chain]
        self.assertGreaterEqual(
            len(set(providers)), 2,
            "fallback.chain must span >=2 providers so one dead credential "
            f"cannot take down every agent lane; got {providers}",
        )
        self.assertEqual(len(chain), len(set(chain)), "chain has duplicates")
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
        # Fable gets exactly one model-action attempt: the recovery retry is
        # gated on the subscription-billed lanes only, and fable-5 is not one.
        retry_gate = ("if: contains(fromJSON('[\"claude\",\"opus-5\"]'), "
                      "steps.effective.outputs.backend)\n        id: claude-attempt-1")
        self.assertIn(retry_gate, workflow)
        self.assertNotIn("fable-5\"]'), steps.effective.outputs.backend)\n        id: claude-attempt-1",
                         workflow)
        self.assertIn("Verify pinned model provenance", workflow)
        self.assertIn("actual_model=$(jq -r", workflow)
        self.assertTrue(self.obs["generative-research.yml"].has_fable_dispatch)
        # Fable is never reachable without asking for it by name.
        self.assertNotEqual(self.lanes["generative-research-default"]["backend"], "fable-5")

    def test_gen_research_opus_5_is_explicit_and_provenance_checked(self):
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "generative-research.yml").read_text(encoding="utf-8")
        # Dispatch option, both case-normalizations, and the runtime allowlist.
        self.assertIn('- opus-5', workflow)
        self.assertIn('claude-opus-5|opus-5|opus5) CANDIDATE="opus-5"', workflow)
        self.assertIn('claude-opus-5|opus-5|opus5) BACKEND="opus-5"', workflow)
        self.assertIn('[ "$BACKEND" != "opus-5" ]', workflow)
        # Served model is pinned from the single resolver output, so an
        # opus-5-labelled article can never be authored by Sonnet.
        self.assertIn('opus-5) model="claude-opus-5"', workflow)
        # Runs on the shared native-Claude model step, and its committed
        # index row is provenance-verified before the push.
        self.assertIn('contains(fromJSON(\'["claude","fable-5","opus-5"]\'), '
                      'steps.effective.outputs.backend)', workflow)
        self.assertIn('contains(fromJSON(\'["fable-5","opus-5"]\'), '
                      'steps.effective.outputs.backend)', workflow)
        self.assertTrue(self.obs["generative-research.yml"].has_opus_dispatch)
        from build_backend_matrix import GEN_RESEARCH_BACKENDS
        self.assertIn("opus-5", GEN_RESEARCH_BACKENDS)
        # opus-5 is the SSOT default: manual dispatch with no backend input,
        # gen-research issues, and hourly-twitter's auto-research all inherit
        # it. The workflow must keep resolving that default at runtime rather
        # than hard-coding a backend of its own.
        self.assertEqual(self.lanes["generative-research-default"]["backend"], "opus-5")
        self.assertIn("generative-research-default",
                      self.obs["generative-research.yml"].resolver_lanes)
        # The Fireworks-unavailable fallback is deliberately NOT the default:
        # a fallback target should be the cheap reliable path.
        self.assertIn('backend="claude"', (REPO_ROOT / ".github" / "workflows" /
                      "generative-research.yml").read_text(encoding="utf-8"))

    def test_gen_research_opencode_kimi_is_explicit_and_fail_closed(self):
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "generative-research.yml").read_text(encoding="utf-8")
        # Dispatch option, both case-normalizations, and the runtime allowlist.
        self.assertIn("- opencode-kimi-k3", workflow)
        self.assertIn('opencode|opencode-kimi|opencode-kimi-k3|kimi|kimi-k3) CANDIDATE="opencode-kimi-k3"', workflow)
        self.assertIn('opencode|opencode-kimi|opencode-kimi-k3|kimi|kimi-k3) BACKEND="opencode-kimi-k3"', workflow)
        self.assertIn('[ "$BACKEND" != "opencode-kimi-k3" ]', workflow)
        # Fail-closed route preflight and the output guard stay in the
        # workflow; the version-pinned install and the env-var auth moved into
        # the container action and are asserted there (see the containment
        # test below), because that is now the only place opencode runs.
        self.assertIn("Resolve and preflight OpenCode route", workflow)
        self.assertIn("Fail OpenCode run without article", workflow)
        self.assertIn("uses: ./.github/actions/run-opencode-container", workflow)
        # MOONSHOT_API_KEY may appear exactly once — the preflight step, purely
        # to emit a precise error when it is the only key configured. It must
        # NOT reach the agent step: opencode has no subprocess env allowlist,
        # so the agent's bash tool inherits every secret in that step's env.
        self.assertEqual(
            1, workflow.count("MOONSHOT_API_KEY: ${{ secrets.MOONSHOT_API_KEY }}"),
            "MOONSHOT_API_KEY must be scoped to the preflight step only")
        # ATTRIBUTION COUPLING: the model every opencode workflow resolves and
        # the model the writer stamps into index.json must be the same string,
        # so a half-done swap cannot ship articles credited to the wrong model.
        model_id = self.assert_single_opencode_model()
        prompt = (REPO_ROOT / ".github" / "opencode" / "prompts" /
                  "generative-research.md").read_text(encoding="utf-8")
        # BOTH writer call sites (slug / no-slug), not just one: assertIn would
        # be satisfied by a single updated invocation.
        self.assertEqual([model_id, model_id], re.findall(r"--model (\S+)", prompt))
        # The scanner must see both opencode call sites (research + canary),
        # which drive the matrix rows and the README diagram edge.
        self.assertTrue(self.obs["generative-research.yml"].opencode)
        self.assertEqual(self.obs["generative-research.yml"].opencode_token,
                         "OPENCODE_API_KEY")
        self.assertTrue(self.obs["opencode-kimi-canary.yml"].opencode)
        from build_backend_matrix import GEN_RESEARCH_BACKENDS
        self.assertIn("opencode-kimi-k3", GEN_RESEARCH_BACKENDS)

    # Every workflow that can run the opencode harness. hourly-twitter is the
    # one most easily forgotten in a model swap — it resolves its own model in
    # its own step rather than sharing gen-research's preflight.
    OPENCODE_WORKFLOWS = ("generative-research.yml", "hourly-twitter.yml",
                          "opencode-kimi-canary.yml")

    def assert_single_opencode_model(self) -> str:
        """Exactly one opencode-go model id across every opencode workflow.

        Parses `run:` shell and skips comment lines. A whole-file substring
        scan cannot tell live routing from a REVERT marker that quotes the old
        assignment — it already false-positived on one — which pressures the
        next maintainer to write vaguer comments to stay green. Set equality
        (not "no moonshot") is strictly stronger: any second route fails.
        """
        seen: dict[str, set] = {}
        for name in self.OPENCODE_WORKFLOWS:
            doc = yaml.safe_load((REPO_ROOT / ".github" / "workflows" / name)
                                 .read_text(encoding="utf-8"))
            found = set()
            for job in (doc.get("jobs") or {}).values():
                for step in job.get("steps") or []:
                    # (a) shell assignments, e.g. the gen-research preflight
                    for line in (step.get("run") or "").splitlines():
                        if line.lstrip().startswith("#"):
                            continue
                        # Scoped to the opencode PROVIDERS, not every model=
                        # assignment (gen-research also pins claude-* ids for
                        # other backends). Still catches a resurrected
                        # moonshotai/ route, which is the thing to forbid.
                        found.update(re.findall(
                            r'\bmodel="((?:opencode-go|opencode|moonshotai)/[^"]+)"',
                            line))
                    # (b) the `model:` input to the container action. Skip
                    # ${{ }} expressions: those indirect to a preflight
                    # literal already counted by (a), and treating the
                    # expression text as an id would always mismatch.
                    if "run-opencode-container" in str(step.get("uses") or ""):
                        model = str((step.get("with") or {}).get("model") or "")
                        if model and "${{" not in model:
                            found.add(model)
            seen[name] = found
        union = set().union(*seen.values())
        self.assertEqual(
            1, len(union),
            f"opencode workflows must route to exactly one model; found {seen}")
        model_ref = union.pop()
        self.assertTrue(model_ref.startswith("opencode-go/"),
                        f"unexpected opencode provider in {model_ref}")
        for name, found in seen.items():
            self.assertEqual({model_ref}, found,
                             f"{name} does not route to {model_ref}")
        return model_ref.split("/", 1)[1]

    def test_opencode_canary_probes_the_model_production_runs(self):
        # A canary that probes a different model than production runs is worse
        # than no canary: it goes green on an entitlement the real lane never
        # uses. Pin them to the same id (2026-08-07 DeepSeek swap).
        model_id = self.assert_single_opencode_model()
        canary = (REPO_ROOT / ".github" / "workflows" /
                  "opencode-kimi-canary.yml").read_text(encoding="utf-8")
        gen = (REPO_ROOT / ".github" / "workflows" /
               "generative-research.yml").read_text(encoding="utf-8")
        # The RAW API probes bill the bare id; they must match the harness id
        # or the cheap preflight certifies an entitlement the run never uses.
        self.assertIn(f'"model": "{model_id}"', canary)
        self.assertIn(f'{{"model":"{model_id}"', gen)
        # The declared provider models must cover the pinned id, or resolution
        # breaks on a runner whose models.dev cache predates it.
        for name in ("opencode.json", "opencode-canary.json"):
            cfg = json.loads((REPO_ROOT / ".github" / "opencode" / name)
                             .read_text(encoding="utf-8"))
            self.assertIn(model_id, cfg["provider"]["opencode-go"]["models"], name)
            # opencode REJECTS unknown top-level keys ("Unrecognized key:
            # $comment"), which breaks config injection for the whole lane.
            # Keep revert notes in the workflows and docs, never in here.
            self.assertLessEqual(set(cfg) - {"$schema", "model", "provider",
                                             "permission", "agent", "mcp"}, set(),
                                 f"{name}: unknown top-level key rejected by opencode")
        default_model = json.loads(
            (REPO_ROOT / ".github" / "opencode" / "opencode.json")
            .read_text(encoding="utf-8"))["model"]
        self.assertEqual(f"opencode-go/{model_id}", default_model)

    def test_opencode_twitter_tier_labels_name_the_served_model(self):
        # The tier's selector token and output dir keep historical Kimi names
        # for a cheap revert, so the human-facing labels are the ONLY thing
        # telling a reader who wrote the artifact. They must name the served
        # model — a committed report headed "Kimi K3" that DeepSeek wrote is
        # the exact failure this strict, no-fallback tier exists to prevent.
        model_id = self.assert_single_opencode_model()
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "hourly-twitter.yml").read_text(encoding="utf-8")
        # Pick the tier-CONFIG case arm by content: the workflow has an earlier
        # `...|opencode-kimi-k3) ;;` validation arm that carries no labels.
        arms = [chunk.split(";;", 1)[0]
                for chunk in workflow.split("opencode-kimi-k3)")[1:]]
        arm = next(a for a in arms if "OUTPUT_DIR=" in a)
        # Symmetric, so this test survives the revert it documents: assert the
        # served family IS named and every OTHER known family is not. Hard-
        # coding "must not say kimi" would red-light the very revert the
        # REVERT markers describe.
        family = model_id.split("-")[0].lower()          # e.g. "deepseek"
        others = {"deepseek", "kimi", "glm", "claude", "gpt", "qwen"} - {family}
        targets = [(f, next(ln for ln in arm.splitlines() if f"{f}=" in ln))
                   for f in ("TITLE_SUFFIX", "COMMIT_PREFIX", "HARNESS_LABEL")]
        # ...and the Telegram notification title for the same tier.
        targets.append(("notification title",
                        next(ln for ln in workflow.splitlines()
                             if "Twitter/X AI Pulse — opencode" in ln)))
        for field, line in targets:
            self.assertIn(family, line.lower(), f"{field} must name {family}")
            for other in others:
                self.assertNotIn(other, line.lower(),
                                 f"{field} names {other} but the tier serves {family}")

    def test_opencode_never_runs_unsandboxed(self):
        # opencode was the only agent harness with no containment: it ran bare
        # on the self-hosted host with edit/bash/webfetch all "allow" plus
        # --auto, while generative-research.yml triggers on `issues:` and feeds
        # the agent live tweets. Every invocation must now go through the
        # container action, and that action must keep its teeth.
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        # EXECUTABLE shell only. The action's header comment explains the very
        # flags asserted below, so a whole-file substring check passes on the
        # prose while the real flag is gone — verified: deleting
        # `--cap-drop ALL` from the docker invocation left the file-wide
        # assertion green. Strip comments and assert on what actually runs.
        action = "\n".join(
            line for line in
            "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"]).splitlines()
            if not line.lstrip().startswith("#"))
        for name in self.OPENCODE_WORKFLOWS:
            doc = yaml.safe_load((REPO_ROOT / ".github" / "workflows" / name)
                                 .read_text(encoding="utf-8"))
            for job in (doc.get("jobs") or {}).values():
                for step in job.get("steps") or []:
                    for line in (step.get("run") or "").splitlines():
                        code = line.split("#", 1)[0]
                        self.assertNotRegex(
                            code, r"(^|[;&|]|\s)opencode\s+run\b",
                            f"{name}: `opencode run` outside the container "
                            f"action reintroduces the unsandboxed posture")
        # Container hardening, mirroring run-pi-container.
        for flag in ("--cap-drop ALL", "--security-opt no-new-privileges",
                     "--pids-limit", '--user "$(id -u):$(id -g)"',
                     "HOME=/tmp/opencode-home"):
            self.assertIn(flag, action, f"container lost {flag}")
        # A missing Docker daemon must FAIL, never silently degrade to a host
        # run — that is the exact posture this action removes.
        self.assertIn("Docker is required for sandboxed opencode runs", action)
        # Pinned install lives here now.
        self.assertIn("opencode-ai@1.18.3", action)
        self.assertIn("OPENCODE_DISABLE_AUTOUPDATE=1", action)
        # The runner's real home holds other lanes' credentials; the agent gets
        # the workspace and the prompt, nothing else by default.
        self.assertNotIn('--volume "$HOME', action)
        self.assertNotIn("--privileged", action)

    def test_comparison_tiers_are_strict(self):
        # Comparison artifacts must be attributable to their labeled backend:
        # a silent chain re-route would corrupt the comparison (round-3 F1).
        for lane in ("twitter-zai", "twitter-deepseek", "zai-canary"):
            self.assertTrue(self.lanes[lane].get("strict"), lane)

    def test_native_model_override_is_rendered_in_the_matrix(self):
        # A workflow `native-model:` input silently beats fallback.native_model
        # for that step. If the Model column renders the global default anyway,
        # the row is a lie that reads as plausible — the A/B judge lanes pin
        # claude-opus-4-8 precisely so the judge is NOT a contestant, and the
        # matrix claiming they run the fleet default hides an invalidated eval.
        from build_backend_matrix import build_generated_blocks
        matrix, _ = build_generated_blocks()
        judge_rows = [ln for ln in matrix.splitlines()
                      if ln.startswith("| twitter-ab-judge")]
        self.assertEqual(2, len(judge_rows), matrix)
        for row in judge_rows:
            self.assertIn("claude-opus-4-8", row)
            self.assertIn("native-model` override", row)
        # The contestant leg has no override and must track the global default.
        leg_a = [ln for ln in matrix.splitlines()
                 if ln.startswith("| twitter-ab-claude")]
        self.assertEqual(1, len(leg_a), matrix)
        self.assertIn(self.fallback["native_model"], leg_a[0])
        self.assertNotIn("override", leg_a[0])

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
