"""Invariant tests for the backend routing SSOT (data/agent-backends.json)
and its validator/generator (scripts/build_backend_matrix.py).

These pin the load-bearing routing facts — if a change flips one, the test
failing is the signal to update BOTH the routing intent and this pin, not to
loosen the parser. (Doc-freshness itself is the separate `--check` CI step.)
"""

import copy
import json
import os
import re
import signal
import shlex
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

import yaml

from build_backend_matrix import (
    LANES_FILE,
    Profile,
    build_readme_diagram,
    build_rows,
    check_fallback,
    cross_check,
    load_adapters,
    load_lanes,
    load_profiles,
    load_routes,
    observe_workflow,
    workflow_files,
)
from resolve_agent_route import resolve_route

REPO_ROOT = Path(__file__).resolve().parent.parent
RESOLVER = REPO_ROOT / "scripts" / "resolve_backend_lane.py"


def observations():
    return {p.name: observe_workflow(p) for p in workflow_files()}


class RoutingInvariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lanes, cls.fallback = load_lanes()
        cls.profiles = load_profiles()
        cls.adapters = load_adapters()
        cls.obs = observations()

    def test_cross_check_is_clean_on_repo_state(self):
        errors = check_fallback(self.fallback, self.profiles) \
            + cross_check(self.lanes, self.obs, self.profiles)
        self.assertEqual(errors, [])

    def test_research_editorial_rejects_host_checkout_adapter(self):
        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        config["routes"]["research-editorial"]["backend"] = "claude"
        for lane in ("rss", "bluesky", "community", "arxiv", "wiki-ingest"):
            with self.assertRaisesRegex(ValueError, "isolated_workspace"):
                resolve_route(config, lane)

    def test_synthetic_opencode_profile_needs_only_profile_and_route_data(self):
        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        workflows_before = {
            name: (REPO_ROOT / ".github/workflows" / name).read_bytes()
            for name in ("hourly-rss.yml", "2h-bluesky.yml", "4h-community.yml",
                         "daily-arxiv.yml", "wiki-ingest.yml")
        }
        config["backends"]["opencode-novel-flash"] = {
            "adapter": "opencode", "provider": "opencode-go",
            "model": "novel-flash",
            "display_name": "Novel Flash via OpenCode",
        }
        config["routes"]["research-editorial"]["backend"] = "opencode-novel-flash"
        profiles = copy.deepcopy(self.profiles)
        profile = Profile("opencode-novel-flash", "opencode", "opencode-go",
                          "novel-flash", "Novel Flash via OpenCode",
                          ["opencode-novel-flash"])
        profiles[profile.normalized] = profile
        for lane in ("rss", "bluesky", "community", "arxiv", "wiki-ingest"):
            selected = resolve_route(config, lane)
            self.assertEqual("opencode", selected.adapter)
            self.assertEqual("opencode-go/novel-flash", selected.model_ref)
        self.assertEqual([], cross_check(
            self.lanes, self.obs, profiles, config["routes"]
        ))
        rows = build_rows(
            self.lanes, self.obs, profiles, self.fallback["native_model"],
            "claude", self.fallback["chain"], config["routes"],
        )
        for lane in ("rss", "bluesky", "community", "arxiv", "wiki-ingest"):
            row = next(row for row in rows if row[0].startswith(f"{lane} (route:"))
            self.assertIn("novel-flash", row[4])
        diagram = build_readme_diagram(
            self.lanes, profiles, self.fallback["chain"],
            self.fallback["native_model"], True, True, config["routes"],
        )
        group_node = next(line.split("[", 1)[0].strip() for line in diagram.splitlines()
                          if "arxiv" in line and "bluesky" in line and "rss" in line)
        self.assertIn(f'{group_node} -->|"novel-flash"| OC', diagram)
        production_config = json.loads(
            (REPO_ROOT / ".github/opencode/opencode.json").read_text()
        )
        self.assertNotIn("model", production_config)
        self.assertNotIn("provider", production_config)
        for name, content in workflows_before.items():
            self.assertEqual(content, (REPO_ROOT / ".github/workflows" / name).read_bytes())

    def test_synthetic_cursor_profile_needs_only_profile_and_route_data(self):
        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        workflows_before = {
            name: (REPO_ROOT / ".github/workflows" / name).read_bytes()
            for name in ("hourly-rss.yml", "2h-bluesky.yml", "4h-community.yml",
                         "daily-arxiv.yml", "wiki-ingest.yml")
        }
        config["backends"]["cursor-composer-novel"] = {
            "adapter": "cursor", "provider": "cursor",
            "model": "composer-novel",
            "display_name": "Composer Novel via Cursor CLI",
        }
        config["routes"]["research-editorial"]["backend"] = "cursor-composer-novel"
        profiles = copy.deepcopy(self.profiles)
        profile = Profile("cursor-composer-novel", "cursor", "cursor",
                          "composer-novel", "Composer Novel via Cursor CLI",
                          ["cursor-composer-novel"])
        profiles[profile.normalized] = profile
        for lane in ("rss", "bluesky", "community", "arxiv", "wiki-ingest"):
            selected = resolve_route(config, lane)
            self.assertEqual("cursor", selected.adapter)
            self.assertEqual("cursor/composer-novel", selected.model_ref)
        self.assertEqual([], cross_check(
            self.lanes, self.obs, profiles, config["routes"]
        ))
        rows = build_rows(
            self.lanes, self.obs, profiles, self.fallback["native_model"],
            "claude", self.fallback["chain"], config["routes"],
        )
        for lane in ("rss", "bluesky", "community", "arxiv", "wiki-ingest"):
            row = next(row for row in rows if row[0].startswith(f"{lane} (route:"))
            self.assertIn("composer-novel", row[4])
            self.assertIn("Cursor CLI", row[2])
        diagram = build_readme_diagram(
            self.lanes, profiles, self.fallback["chain"],
            self.fallback["native_model"], True, True, config["routes"], True,
        )
        group_node = next(line.split("[", 1)[0].strip() for line in diagram.splitlines()
                          if "arxiv" in line and "bluesky" in line and "rss" in line)
        self.assertIn(f'{group_node} -->|"composer-novel"| CUR', diagram)
        production_config = json.loads(
            (REPO_ROOT / ".github/cursor/cli-config.json").read_text()
        )
        self.assertNotIn("model", production_config)
        self.assertNotIn("provider", production_config)
        for name, content in workflows_before.items():
            self.assertEqual(content, (REPO_ROOT / ".github/workflows" / name).read_bytes())

    def test_route_contract_and_provider_credential_binding_fail_closed(self):
        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        config["routes"]["research-editorial"]["contract"] = "other"
        with self.assertRaisesRegex(ValueError, "contract"):
            resolve_route(config, "rss")

        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        config["adapters"]["opencode"]["provider_credentials"]["opencode-go"] = \
            "claude-code-oauth-token"
        with self.assertRaisesRegex(ValueError, "opencode-api-key"):
            resolve_route(config, "rss")

        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        config["backends"]["cursor-grok-4p6-fast"]["adapter"] = "cursor"
        config["routes"]["research-editorial"]["backend"] = "cursor-grok-4p6-fast"
        config["adapters"]["cursor"]["provider_credentials"]["cursor"] = \
            "opencode-api-key"
        with self.assertRaisesRegex(ValueError, "cursor-api-key"):
            resolve_route(config, "rss")

    def test_dispatched_lane_io_contracts_are_exact_and_route_neutral(self):
        expected = {
            "rss": ("research/rss/${{ steps.datetime.outputs.date }}.md",
                    "research/rss/${{ steps.datetime.outputs.date }}.md", ""),
            "community": ("research/community/${{ steps.datetime.outputs.date }}-hn.md\nresearch/community/${{ steps.datetime.outputs.date }}-reddit.md",
                          "research/community/${{ steps.datetime.outputs.date }}-hn.md\nresearch/community/${{ steps.datetime.outputs.date }}-reddit.md", ""),
            "arxiv": ("research/arxiv/${{ steps.date.outputs.date }}-papers.md",
                      "research/arxiv/${{ steps.date.outputs.date }}-papers.md\nresearch/summaries/${{ steps.date.outputs.date }}-arxiv-summary.txt", ""),
            "wiki-ingest": ("research/wiki/", "research/wiki/", ""),
            "bluesky": ("", "", ".tmp/bluesky-section.md"),
            "generative-research-ko": (
                "", "", "${{ steps.prepare.outputs.result_path }}"
            ),
        }
        seen = {}
        for obs in self.obs.values():
            for step in obs.dispatch_steps:
                seen[step.lane] = (step.expected_paths, step.allowed_paths,
                                   step.return_artifacts)
        self.assertEqual(expected, seen)

    def test_dispatcher_executes_only_compatible_isolated_child_and_scopes_secret(self):
        action = yaml.safe_load(
            (REPO_ROOT / ".github/actions/agent-dispatch/action.yml").read_text()
        )
        steps = action["runs"]["steps"]
        local_children = [step for step in steps if "uses" in step]
        self.assertEqual(2, len(local_children))
        by_uses = {child["uses"]: child for child in local_children}
        opencode = by_uses["./.github/actions/run-opencode-container"]
        cursor = by_uses["./.github/actions/run-cursor-container"]
        self.assertEqual("${{ inputs.opencode-api-key }}",
                         opencode["with"]["opencode-api-key"])
        self.assertEqual("${{ inputs.opencode-config }}",
                         opencode["with"]["opencode-config"])
        self.assertEqual("${{ inputs.cursor-api-key }}",
                         cursor["with"]["cursor-api-key"])
        self.assertEqual("${{ inputs.cursor-config }}",
                         cursor["with"]["cursor-config"])
        self.assertEqual("steps.route.outputs.adapter == 'opencode'",
                         opencode.get("if"))
        self.assertEqual("steps.route.outputs.adapter == 'cursor'",
                         cursor.get("if"))
        for child, foreign in (
                (opencode, ("claude-code-oauth-token", "fireworks-api-key",
                            "zai-api-key", "cursor-api-key")),
                (cursor, ("claude-code-oauth-token", "fireworks-api-key",
                          "zai-api-key", "opencode-api-key")),
        ):
            rendered_child = json.dumps(child, sort_keys=True)
            for secret_input in foreign:
                self.assertNotIn(secret_input, rendered_child)

        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        for name, credential in (
                ("opencode", {"opencode-go": "opencode-api-key"}),
                ("cursor", {"cursor": "cursor-api-key"}),
        ):
            adapter = config["adapters"][name]
            self.assertIs(adapter["isolated_workspace"], True)
            self.assertIs(adapter["editorial_contract"], True)
            self.assertEqual(credential, adapter["provider_credentials"])

    def test_korean_translation_dispatch_uses_capability_minimized_policy(self):
        workflow = yaml.safe_load(
            (REPO_ROOT / ".github/workflows/translate-generative-research.yml")
            .read_text(encoding="utf-8")
        )
        dispatch = next(
            step
            for step in workflow["jobs"]["translate"]["steps"]
            if step.get("uses") == "./.github/actions/agent-dispatch"
        )
        self.assertEqual(
            ".github/opencode/translation.json",
            dispatch["with"].get("opencode-config"),
        )
        self.assertEqual(
            ".github/cursor/translation.json",
            dispatch["with"].get("cursor-config"),
        )
        cursor_policy = json.loads(
            (REPO_ROOT / ".github/cursor/translation.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            ["Shell(*)", "Write(*)", "WebFetch(*)", "Mcp(*)"],
            cursor_policy["permissions"]["deny"],
        )
        self.assertIn(
            "Read(.agent-input/translation-segments.json)",
            cursor_policy["permissions"]["allow"],
        )
        self.assertIn(
            "Write(.tmp/generative-translation.ko.segments.jsonl)",
            cursor_policy["permissions"]["allow"],
        )

        policy = json.loads(
            (REPO_ROOT / ".github/opencode/translation.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIs(False, policy["formatter"])
        self.assertIs(False, policy["lsp"])
        policy = policy["permission"]
        self.assertEqual("deny", policy["*"])
        self.assertEqual(
            {
                "*": "deny",
                ".agent-input/translation-segments.json": "allow",
            },
            policy["read"],
        )
        self.assertEqual(
            "allow",
            policy["translation_segment"],
        )
        self.assertNotIn("edit", policy)

        segment_tool = (
            REPO_ROOT / ".opencode/tools/translation_segment.ts"
        ).read_text(encoding="utf-8")
        self.assertIn(
            'const RESULT_RELATIVE_PATH = ".tmp/generative-translation.ko.segments.jsonl"',
            segment_tool,
        )
        self.assertIn("constants.O_NOFOLLOW", segment_tool)
        self.assertIn("withExclusiveWrite", segment_tool)
        self.assertIn("MAX_TEXT_BYTES = 16 * 1024", segment_tool)
        self.assertIn("MAX_RESULT_BYTES = 1024 * 1024", segment_tool)
        self.assertIn("immutable tokens for", segment_tool)
        self.assertIn("unsafe localized numeric token", segment_tool)
        self.assertIn("PENDING_RELATIVE_PATH", segment_tool)
        self.assertIn("await rename(pendingPath, resultPath)", segment_tool)
        self.assertIn("duplicate translation segment", segment_tool)
        self.assertIn("unprotected list separator", segment_tool)
        self.assertNotIn("filePath:", segment_tool)
        self.assertNotIn("path:", segment_tool)

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
        # DeepSeek/OpenCode is the SSOT default: manual dispatch with no backend input,
        # gen-research issues, and hourly-twitter's auto-research all inherit
        # it. The workflow must keep resolving that default at runtime rather
        # than hard-coding a backend of its own.
        self.assertEqual(self.lanes["generative-research-default"]["backend"],
                         "opencode-deepseek-v4-flash")
        self.assertIn("generative-research-default",
                      self.obs["generative-research.yml"].resolver_lanes)
        # The Fireworks-unavailable fallback is deliberately NOT the default:
        # a fallback target should be the cheap reliable path.
        self.assertIn('backend="claude"', (REPO_ROOT / ".github" / "workflows" /
                      "generative-research.yml").read_text(encoding="utf-8"))

    def test_gen_research_opencode_deepseek_is_explicit_and_fail_closed(self):
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "generative-research.yml").read_text(encoding="utf-8")
        # Dispatch option, both case-normalizations, and the runtime allowlist.
        self.assertIn("- opencode-deepseek-v4-flash", workflow)
        self.assertIn('opencode|opencode-deepseek|opencode-deepseek-v4-flash|deepseek-opencode) CANDIDATE="opencode-deepseek-v4-flash"', workflow)
        self.assertIn('opencode|opencode-deepseek|opencode-deepseek-v4-flash|deepseek-opencode) BACKEND="opencode-deepseek-v4-flash"', workflow)
        self.assertIn('[ "$BACKEND" != "opencode-deepseek-v4-flash" ]', workflow)
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
        self.assertTrue(self.obs["opencode-deepseek-canary.yml"].opencode)
        from build_backend_matrix import GEN_RESEARCH_BACKENDS
        self.assertIn("opencode-deepseek-v4-flash", GEN_RESEARCH_BACKENDS)

    def test_gen_research_cursor_is_explicit_and_fail_closed(self):
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "generative-research.yml").read_text(encoding="utf-8")
        self.assertIn("- cursor-grok-4p6-fast", workflow)
        self.assertIn(
            'cursor|cursor-cli|cursor-agent|cursor-composer-2p5|composer-2.5|cursor-grok-4p6-fast|grok-4.6-fast|grok-4.6|grok) CANDIDATE="cursor-grok-4p6-fast"',
            workflow)
        self.assertIn(
            'cursor|cursor-cli|cursor-agent|cursor-composer-2p5|composer-2.5|cursor-grok-4p6-fast|grok-4.6-fast|grok-4.6|grok) BACKEND="cursor-grok-4p6-fast"',
            workflow)
        self.assertIn('[ "$BACKEND" != "cursor-grok-4p6-fast" ]', workflow)
        self.assertIn("Resolve and preflight Cursor CLI route", workflow)
        self.assertIn("Fail Cursor run without article", workflow)
        self.assertIn("uses: ./.github/actions/run-cursor-container", workflow)
        self.assertIn('model="cursor/grok-4.6-fast"', workflow)
        model_id = self.assert_single_cursor_model()
        prompt = (REPO_ROOT / ".github" / "cursor" / "prompts" /
                  "generative-research.md").read_text(encoding="utf-8")
        self.assertEqual([model_id, model_id], re.findall(r"--model (\S+)", prompt))
        self.assertTrue(self.obs["generative-research.yml"].cursor)
        self.assertEqual(self.obs["generative-research.yml"].cursor_token,
                         "CURSOR_API_KEY")
        self.assertTrue(self.obs["cursor-cli-canary.yml"].cursor)
        from build_backend_matrix import GEN_RESEARCH_BACKENDS
        self.assertIn("cursor-grok-4p6-fast", GEN_RESEARCH_BACKENDS)
        self.assertNotEqual(self.lanes["generative-research-default"]["backend"],
                            "cursor-grok-4p6-fast")

    # Every workflow that can run the opencode harness. hourly-twitter is the
    # one most easily forgotten in a model swap — it resolves its own model in
    # its own step rather than sharing gen-research's preflight.
    OPENCODE_WORKFLOWS = (
        "2h-bluesky.yml",
        "4h-community.yml",
        "daily-arxiv.yml",
        "generative-research.yml",
        "hourly-rss.yml",
        "hourly-twitter.yml",
        "opencode-deepseek-canary.yml",
        "translate-generative-research.yml",
        "wiki-ingest.yml",
    )

    def assert_single_opencode_model(self) -> str:
        """Exactly one opencode-go model id across every opencode workflow.

        Parses `run:` shell and skips comment lines. A whole-file substring
        scan cannot tell live routing from a REVERT marker that quotes the old
        assignment — it already false-positived on one — which pressures the
        next maintainer to write vaguer comments to stay green. Set equality
        (not "no moonshot") is strictly stronger: any second route fails.
        """
        seen: dict[str, set] = {}
        direct_workflows = (
            "generative-research.yml", "hourly-twitter.yml",
            "opencode-deepseek-canary.yml",
        )
        for name in direct_workflows:
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

    CURSOR_WORKFLOWS = (
        "cursor-cli-canary.yml",
        "generative-research.yml",
        "hourly-twitter.yml",
    )

    def assert_single_cursor_model(self) -> str:
        """Exactly one Cursor model id across every Cursor workflow."""
        from build_backend_matrix import CURSOR_ACTION_MODEL_RE, CURSOR_MODEL_RE
        seen: dict[str, set[str]] = {}
        for name in self.CURSOR_WORKFLOWS:
            doc = yaml.safe_load((REPO_ROOT / ".github" / "workflows" / name)
                                 .read_text(encoding="utf-8"))
            found: set[str] = set()
            for job in (doc.get("jobs") or {}).values():
                for step in job.get("steps") or []:
                    for line in (step.get("run") or "").splitlines():
                        if line.lstrip().startswith("#"):
                            continue
                        found.update(CURSOR_MODEL_RE.findall(line))
                    if "run-cursor-container" in str(step.get("uses") or ""):
                        model = str((step.get("with") or {}).get("model") or "")
                        if model and "${{" not in model:
                            found.update(CURSOR_ACTION_MODEL_RE.findall(model))
            seen[name] = found
        union = set().union(*seen.values()) if seen else set()
        self.assertEqual(
            1, len(union),
            f"Cursor workflows must route to exactly one model; found {seen}")
        model_id = union.pop()
        for name, found in seen.items():
            self.assertEqual({model_id}, found,
                             f"{name} does not route to {model_id}")
        return model_id

    def test_all_opencode_callers_disable_checkout_credentials(self):
        """Every known caller removes checkout auth before metadata cleanup."""
        self.assertEqual(
            {"2h-bluesky.yml", "4h-community.yml", "daily-arxiv.yml",
             "generative-research.yml", "hourly-rss.yml",
             "hourly-twitter.yml", "opencode-deepseek-canary.yml",
             "translate-generative-research.yml",
             "wiki-ingest.yml"},
            set(self.OPENCODE_WORKFLOWS))
        for name in self.OPENCODE_WORKFLOWS:
            doc = yaml.safe_load((REPO_ROOT / ".github" / "workflows" / name)
                                 .read_text(encoding="utf-8"))
            containing_jobs = [job for job in (doc.get("jobs") or {}).values()
                               if any(str(step.get("uses") or "") in {
                                      "./.github/actions/run-opencode-container",
                                      "./.github/actions/agent-dispatch"}
                                      for step in (job.get("steps") or []))]
            self.assertTrue(containing_jobs, name)
            for job in containing_jobs:
                checkouts = [step for step in (job.get("steps") or [])
                             if str(step.get("uses") or "").startswith(
                                 "actions/checkout@")]
                self.assertTrue(checkouts, name)
                self.assertTrue(
                    all((step.get("with") or {}).get("persist-credentials")
                        is False for step in checkouts), name)
                for checkout in checkouts:
                    self.assertEqual(
                        {"GIT_CONFIG_NOSYSTEM": "1",
                         "GIT_CONFIG_GLOBAL": "/dev/null"},
                        checkout.get("env") or {}, name)
                    self.assertIs(
                        False,
                        (checkout.get("with") or {}).get("set-safe-directory"),
                        name)

    def test_opencode_callers_quarantine_stale_workspace_before_checkout(self):
        """The exact pre-checkout shell removes stale Git and untracked state."""
        guards = []
        for name in self.OPENCODE_WORKFLOWS:
            doc = yaml.safe_load((REPO_ROOT / ".github" / "workflows" / name)
                                 .read_text(encoding="utf-8"))
            containing_jobs = [job for job in (doc.get("jobs") or {}).values()
                               if any(str(step.get("uses") or "") in {
                                      "./.github/actions/run-opencode-container",
                                      "./.github/actions/agent-dispatch"}
                                      for step in (job.get("steps") or []))]
            self.assertEqual(1, len(containing_jobs), name)
            steps = containing_jobs[0].get("steps") or []
            quarantine_i = next(
                i for i, step in enumerate(steps)
                if step.get("id") == "quarantine_workspace")
            checkout_i = next(
                i for i, step in enumerate(steps)
                if str(step.get("uses") or "").startswith("actions/checkout@"))
            self.assertLess(quarantine_i, checkout_i, name)
            quarantine = steps[quarantine_i]
            self.assertNotIn("uses", quarantine, name)
            self.assertEqual("bash", quarantine.get("shell"), name)
            guards.append(quarantine.get("run") or "")
        self.assertEqual(1, len(set(guards)), "pre-checkout guards diverged")
        guard = guards[0]
        self.assertNotRegex(guard, r"(^|\s)git(\s|$)")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runner_workspace = tmp_path / "runner-workspace"
            workspace = runner_workspace / "repository"
            workspace.mkdir(parents=True)

            source = tmp_path / "source"
            source.mkdir()
            subprocess.run(["git", "-C", str(source), "init", "-b", "main"],
                           check=True, capture_output=True)
            subprocess.run(["git", "-C", str(source), "config", "user.name",
                            "Source"], check=True)
            subprocess.run(["git", "-C", str(source), "config", "user.email",
                            "source@example.invalid"], check=True)
            (source / "clean.txt").write_text("clean\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(source), "add", "clean.txt"],
                           check=True)
            subprocess.run(["git", "-C", str(source), "commit", "-m", "source"],
                           check=True, capture_output=True)

            def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
                return subprocess.run(
                    ["git", "-C", str(workspace), *args], text=True,
                    capture_output=True, check=check)

            git("init", "-b", "main")
            git("config", "user.name", "Prior Job")
            git("config", "user.email", "prior@example.invalid")
            (workspace / "tracked.html").write_text(
                "<p>trusted</p>\n", encoding="utf-8")
            git("add", "tracked.html")
            git("commit", "-m", "base")

            marker = tmp_path / "stale-git-executed"
            evil_smudge = tmp_path / "evil-smudge"
            evil_smudge.write_text(
                "#!/bin/sh\n"
                f"printf 'smudge\\n' >> '{marker}'\n"
                "cat\n", encoding="utf-8")
            evil_smudge.chmod(0o755)
            git("config", "filter.evil.smudge", str(evil_smudge))
            (workspace / ".git" / "info" / "attributes").write_text(
                "*.html filter=evil\n", encoding="utf-8")
            (workspace / "tracked.html").write_text("dirty\n", encoding="utf-8")
            git("reset", "--hard", "HEAD")
            self.assertIn("smudge", marker.read_text(encoding="utf-8"))
            marker.unlink()

            # A persistent global init.templateDir is outside the quarantined
            # workspace. Calibrate that a checkout-shaped init/fetch/checkout
            # really does copy and execute its post-checkout hook without the
            # Git config restrictions added below.
            template = tmp_path / "evil-template"
            (template / "hooks").mkdir(parents=True)
            template_hook = template / "hooks" / "post-checkout"
            template_hook.write_text(
                "#!/bin/sh\n"
                f"printf 'global-template\\n' >> '{marker}'\n",
                encoding="utf-8")
            template_hook.chmod(0o755)
            global_config = tmp_path / "persistent-global-config"
            global_config.write_text(
                "[init]\n"
                f"\ttemplateDir = {template}\n",
                encoding="utf-8")
            unsafe_checkout = tmp_path / "unsafe-checkout"
            unsafe_checkout.mkdir()
            unsafe_env = os.environ.copy()
            unsafe_env.update({
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": str(global_config),
            })
            for command in (
                    ["git", "-C", str(unsafe_checkout), "init"],
                    ["git", "-C", str(unsafe_checkout), "remote", "add",
                     "origin", str(source)],
                    ["git", "-C", str(unsafe_checkout), "fetch", "origin",
                     "main"],
                    ["git", "-C", str(unsafe_checkout), "checkout", "--detach",
                     "FETCH_HEAD"]):
                subprocess.run(command, env=unsafe_env, check=True,
                               capture_output=True)
            self.assertIn(
                "global-template", marker.read_text(encoding="utf-8"))
            marker.unlink()

            poison = workspace / "untracked-validator"
            poison.write_text("#!/bin/sh\nexit 99\n", encoding="utf-8")
            poison.chmod(0o755)
            (workspace / ".venv").mkdir()
            (workspace / ".venv" / "sitecustomize.py").write_text(
                "raise SystemExit('stale prior job')\n", encoding="utf-8")

            github_env = tmp_path / "github-env"
            env = os.environ.copy()
            env.update({
                "RUNNER_WORKSPACE": str(runner_workspace),
                "GITHUB_WORKSPACE": str(workspace),
                "GITHUB_REPOSITORY": "example/repository",
                "GITHUB_ENV": str(github_env),
                "GIT_CONFIG_GLOBAL": str(global_config),
            })
            result = subprocess.run(
                ["bash", "-c", guard], cwd=workspace, env=env,
                text=True, capture_output=True, check=False)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse(marker.exists(), result.stdout + result.stderr)
            self.assertTrue(workspace.is_dir())
            self.assertEqual([], list(workspace.iterdir()))
            self.assertEqual([], list(runner_workspace.glob(
                ".opencode-precheckout.*")))
            restrictions = {
                line.split("=", 1)[0]: line.split("=", 1)[1]
                for line in github_env.read_text(encoding="utf-8").splitlines()
            }
            self.assertEqual(
                {"GIT_CONFIG_NOSYSTEM": "1",
                 "GIT_CONFIG_GLOBAL": "/dev/null",
                 "GIT_NO_REPLACE_OBJECTS": "1"},
                restrictions)

            # A checkout-shaped init/fetch/checkout inherits the restrictions
            # written to GITHUB_ENV and cannot reach either the old local
            # metadata or the persistent global template hook.
            checkout_env = env.copy()
            checkout_env.update(restrictions)
            for command in (
                    ["git", "-C", str(workspace), "init"],
                    ["git", "-C", str(workspace), "remote", "add", "origin",
                     str(source)],
                    ["git", "-C", str(workspace), "fetch", "origin", "main"],
                    ["git", "-C", str(workspace), "checkout", "--detach",
                     "FETCH_HEAD"]):
                subprocess.run(command, env=checkout_env, check=True,
                               capture_output=True)
            self.assertFalse(marker.exists())
            self.assertFalse(
                (workspace / ".git" / "hooks" / "post-checkout").exists())

            # A mismatched basename fails closed and preserves that unrelated
            # sibling instead of widening the recursive-removal target.
            unrelated = runner_workspace / "unrelated"
            unrelated.mkdir()
            (unrelated / "sentinel").write_text("keep\n", encoding="utf-8")
            bad_env = env.copy()
            bad_env["GITHUB_WORKSPACE"] = str(unrelated)
            rejected = subprocess.run(
                ["bash", "-c", guard], cwd=workspace, env=bad_env,
                text=True, capture_output=True, check=False)
            self.assertNotEqual(0, rejected.returncode)
            self.assertEqual(
                "keep\n", (unrelated / "sentinel").read_text(encoding="utf-8"))

    def test_opencode_canary_probes_the_model_production_runs(self):
        # A canary that probes a different model than production runs is worse
        # than no canary: it goes green on an entitlement the real lane never
        # uses. Pin them to the same id.
        model_id = self.assert_single_opencode_model()
        canary = (REPO_ROOT / ".github" / "workflows" /
                  "opencode-deepseek-canary.yml").read_text(encoding="utf-8")
        gen = (REPO_ROOT / ".github" / "workflows" /
               "generative-research.yml").read_text(encoding="utf-8")
        # The RAW API probes bill the bare id; they must match the harness id
        # or the cheap preflight certifies an entitlement the run never uses.
        self.assertIn(f'"model": "{model_id}"', canary)
        self.assertIn(f'{{"model":"{model_id}"', gen)
        # The production config deliberately carries no static model/default:
        # every action call is authoritative through `opencode run -m`, so a
        # newly registered SSOT profile does not require a config edit.
        production = json.loads((REPO_ROOT / ".github" / "opencode" / "opencode.json")
                                .read_text(encoding="utf-8"))
        self.assertNotIn("model", production)
        self.assertNotIn("provider", production)
        for name in ("opencode.json", "opencode-canary.json", "translation.json"):
            cfg = json.loads((REPO_ROOT / ".github" / "opencode" / name)
                             .read_text(encoding="utf-8"))
            # opencode REJECTS unknown top-level keys ("Unrecognized key:
            # $comment"), which breaks config injection for the whole lane.
            # Keep prose notes in the workflows and docs, never in here.
            self.assertLessEqual(set(cfg) - {"$schema", "model", "provider",
                                             "permission", "agent", "mcp",
                                             "formatter", "lsp"}, set(),
                                 f"{name}: unknown top-level key rejected by opencode")
        self.assertNotIn(
            "kimi",
            (REPO_ROOT / ".github" / "opencode" / "opencode-canary.json")
            .read_text(encoding="utf-8").lower(),
            "DeepSeek canary config must not retain a selectable Kimi model",
        )
        self.assertNotIn("OPENCODE-KIMI-CANARY-OK", canary)

    def test_opencode_twitter_tier_labels_name_the_served_model(self):
        # The output dir is a legacy namespace, so human-facing labels must
        # name the served model rather than inheriting the directory label.
        model_id = self.assert_single_opencode_model()
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "hourly-twitter.yml").read_text(encoding="utf-8")
        # Pick the tier-CONFIG case arm by content: the workflow has an earlier
        # `...|opencode-deepseek-v4-flash) ;;` validation arm that carries no labels.
        arms = [chunk.split(";;", 1)[0]
                for chunk in workflow.split("opencode-deepseek-v4-flash)")[1:]]
        arm = next(a for a in arms if "OUTPUT_DIR=" in a)
        # Assert the served family IS named and every OTHER known family is not.
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
        workflow_paths = sorted((REPO_ROOT / ".github" / "workflows").glob("*.yml"))
        workflow_paths += sorted((REPO_ROOT / ".github" / "workflows").glob("*.yaml"))
        for workflow_path in workflow_paths:
            name = workflow_path.name
            doc = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
            for job in (doc.get("jobs") or {}).values():
                steps = job.get("steps") or []
                for step in steps:
                    for line in (step.get("run") or "").splitlines():
                        code = line.split("#", 1)[0]
                        self.assertNotRegex(
                            code, r"(^|[;&|]|\s)opencode\s+run\b",
                            f"{name}: `opencode run` outside the container "
                            f"action reintroduces the unsandboxed posture")
                if any("run-opencode-container" in str(step.get("uses") or "")
                       for step in steps):
                    checkouts = [step for step in steps
                                 if str(step.get("uses") or "").startswith(
                                     "actions/checkout@")]
                    self.assertTrue(
                        checkouts,
                        f"{name}: opencode job must check out the contained workspace")
                    for checkout in checkouts:
                        self.assertIs(
                            False,
                            (checkout.get("with") or {}).get("persist-credentials"),
                            f"{name}: opencode checkout must remove credential "
                            "wiring as least privilege")
        # Container hardening, mirroring run-pi-container.
        for flag in ("--cap-drop ALL", "--security-opt no-new-privileges",
                     "--pids-limit", '--user "$(id -u):$(id -g)"',
                     "HOME=/tmp/opencode-home"):
            self.assertIn(flag, action, f"container lost {flag}")
        # A missing Docker daemon must FAIL, never silently degrade to a host
        # run — that is the exact posture this action removes.
        self.assertIn("Docker is required for sandboxed opencode runs", action)
        # The runner and its Docker daemon persist across jobs. The per-run
        # build context, inline prompt, and image must be removed even when the
        # agent fails or times out; EXIT preserves the original exit status.
        self.assertIn("trap cleanup EXIT", action)
        self.assertIn('docker image rm -f "$image"', action)
        self.assertIn('rm -rf -- "$build_dir"', action)
        self.assertIn('rm -rf -- "$isolated_workspace"', action)
        self.assertIn('rm -f -- "$staged_prompt"', action)
        # Pinned install lives here now.
        self.assertIn("opencode-ai@1.18.3", action)
        self.assertIn("OPENCODE_DISABLE_AUTOUPDATE=1", action)
        self.assertIn("model must be one canonical provider/model ref", action)
        self.assertIn("scripts/build_opencode_config.py", action)
        self.assertIn('--volume "$generated_opencode_config:/tmp/opencode.generated.json:ro"', action)
        self.assertIn("--env OPENCODE_CONFIG=/tmp/opencode.generated.json", action)
        self.assertIn('[ ! -f "$config_path" ] || [ -L "$config_path" ]', action)
        self.assertIn('mkdir -- "$isolated_tmp"', action)
        self.assertIn('trap \'exit 143\' TERM', action)
        self.assertIn('trap \'exit 130\' INT', action)
        self.assertIn("trap '' TERM INT", action)
        self.assertIn('--name "$container_name"', action)
        self.assertIn('timeout 30s docker rm -f "$container_name"', action)
        self.assertLess(action.index('docker rm -f "$container_name"'),
                        action.index('docker image rm -f "$image"'),
                        "cancellation cleanup must stop the secret-bearing container first")
        self.assertLess(action.index("trap '' TERM INT"),
                        action.index('docker rm -f "$container_name"'),
                        "cleanup must ignore cancellation escalation before Docker removal")
        self.assertIn('cp "$GITHUB_ACTION_PATH/birdy-fast"', action)
        self.assertIn("--env GITHUB_WORKSPACE=/workspace", action)
        self.assertIn("clone --quiet --no-hardlinks", action)
        self.assertIn("--no-checkout --template=\"$empty_git_template\"", action)
        self.assertIn('--volume "$isolated_workspace:/workspace"', action)
        self.assertNotIn('--volume "$GITHUB_WORKSPACE:/workspace"', action)
        self.assertIn("git bundle create .opencode-export.bundle", action)
        self.assertIn('bundle unbundle "$bundle_file"', action)
        self.assertNotIn('fetch --no-tags "$bundle_file"', action)
        self.assertNotIn('fetch --no-tags "$isolated_workspace"', action)
        self.assertIn('mv -f -- "$trusted_config" "$git_dir/config"', action)
        self.assertIn('"$git_dir/info/attributes"', action)
        self.assertIn('rm -f -- "$git_dir/commondir"', action)
        self.assertIn('"$git_dir/HEAD" "$git_dir/index"', action)
        self.assertIn("logallrefupdates = false", action)
        self.assertIn('cat-file blob "$tree_oid"', action)
        self.assertIn('read-tree --reset --no-sparse-checkout "$post_sha"', action)
        self.assertIn('update-ref HEAD "$post_sha" "$pre_sha"', action)
        self.assertNotIn('"${trusted_git[@]}" reset --hard', action)
        self.assertIn('tree_mode" != "100644', action)
        self.assertIn("tree_type\" != \"blob", action)
        # A provider-success/no-output retry is deliberately narrower than
        # editorial mode: one exact KO lane, one exact draft, one shared
        # deadline, and no retry after a tool call, artifact, or nonzero exit.
        self.assertIn('--env AGENT_LANE', action)
        self.assertIn('--env RETURN_ARTIFACTS', action)
        self.assertIn(
            'model_budget_seconds=$((AGENT_TIMEOUT_MINUTES * 60))',
            action)
        self.assertIn('model_started_seconds=$SECONDS', action)
        self.assertIn('(SECONDS - model_started_seconds)', action)
        self.assertIn('timeout "${remaining_seconds}s" opencode run', action)
        self.assertIn('[ "$AGENT_LANE" = "generative-research-ko" ]', action)
        self.assertIn(
            '[ "$RETURN_ARTIFACTS" = ".tmp/generative-translation.ko.segments.jsonl" ]',
            action)
        self.assertIn('[ "$agent_status" -eq 0 ]', action)
        self.assertIn('[ "$artifact_count" -eq 0 ]', action)
        self.assertIn('[ "$segment_calls" -eq 0 ]', action)
        self.assertIn('[ "$attempt_count" -eq 1 ]', action)
        self.assertIn("opencode attempt telemetry is malformed", action)
        for name, expected_mode in {
                "generative-research.yml": "generative",
                "hourly-twitter.yml": "twitter",
                "opencode-deepseek-canary.yml": "canary",
        }.items():
            doc = yaml.safe_load((REPO_ROOT / ".github" / "workflows" / name)
                                 .read_text(encoding="utf-8"))
            calls = [step for job in (doc.get("jobs") or {}).values()
                     for step in (job.get("steps") or [])
                     if "run-opencode-container" in str(step.get("uses") or "")]
            self.assertTrue(calls, name)
            self.assertTrue(all((step.get("with") or {}).get("mode") == expected_mode
                                for step in calls), name)
        # The runner's real home holds other lanes' credentials; the agent gets
        # the workspace and the prompt, nothing else by default.
        self.assertNotIn('--volume "$HOME', action)
        self.assertNotIn("--privileged", action)

    def test_cursor_never_runs_unsandboxed(self):
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-cursor-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        action = "\n".join(
            line for line in
            "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"]).splitlines()
            if not line.lstrip().startswith("#"))
        workflow_paths = sorted((REPO_ROOT / ".github" / "workflows").glob("*.yml"))
        workflow_paths += sorted((REPO_ROOT / ".github" / "workflows").glob("*.yaml"))
        for workflow_path in workflow_paths:
            name = workflow_path.name
            doc = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
            for job in (doc.get("jobs") or {}).values():
                steps = job.get("steps") or []
                for step in steps:
                    for line in (step.get("run") or "").splitlines():
                        code = line.split("#", 1)[0]
                        self.assertNotRegex(
                            code, r"(^|[;&|]|\s)agent\s+-p\b",
                            f"{name}: `agent -p` outside the container "
                            f"action reintroduces the unsandboxed posture")
                if any("run-cursor-container" in str(step.get("uses") or "")
                       for step in steps):
                    checkouts = [step for step in steps
                                 if str(step.get("uses") or "").startswith(
                                     "actions/checkout@")]
                    self.assertTrue(
                        checkouts,
                        f"{name}: Cursor job must check out the contained workspace")
                    for checkout in checkouts:
                        self.assertIs(
                            False,
                            (checkout.get("with") or {}).get("persist-credentials"),
                            f"{name}: Cursor checkout must remove credential "
                            "wiring as least privilege")
        for flag in ("--cap-drop ALL", "--security-opt no-new-privileges",
                     "--pids-limit", '--user "$(id -u):$(id -g)"',
                     "HOME=/tmp/cursor-home"):
            self.assertIn(flag, action, f"container lost {flag}")
        self.assertIn("Docker is required for sandboxed Cursor CLI runs", action)
        self.assertIn("trap cleanup EXIT", action)
        self.assertIn('docker image rm -f "$image"', action)
        self.assertIn('rm -rf -- "$build_dir"', action)
        self.assertIn('rm -rf -- "$isolated_workspace"', action)
        self.assertIn("scripts/copy_cursor_config.py", action)
        self.assertIn('--volume "$generated_cursor_config:/tmp/cursor-config/cli-config.json:ro"', action)
        self.assertIn("--env CURSOR_CONFIG_DIR=/tmp/cursor-config", action)
        self.assertIn('export CURSOR_CONFIG_DIR="$HOME/.cursor"', action)
        self.assertIn(
            'cp -- "$CURSOR_CONFIG_DIR/cli-config.json" "$HOME/.cursor/cli-config.json"',
            action)
        self.assertIn(
            'if [ "$RUN_MODE" = "canary" ] || [ "$agent_status" -ne 0 ]; then',
            action)
        self.assertIn('cat -- "$attempt_log"', action)
        self.assertIn("HOME=/tmp/cursor-home", action)
        self.assertIn('--sandbox disabled', action)
        self.assertIn('timeout "${remaining_seconds}s" agent -p --force --trust', action)
        self.assertIn('timeout "${remaining_seconds}s" agent -p --mode ask --trust', action)
        self.assertIn("git bundle create .cursor-export.bundle", action)
        self.assertIn("Cursor attempt telemetry is malformed", action)
        self.assertIn("curl https://cursor.com/install -fsS | bash", action)
        self.assertIn("agent --version", action)
        # The published `agent` name is a symlink into a Node package.
        # Copying only the wrapper regresses to MODULE_NOT_FOUND index.js.
        self.assertIn("/opt/cursor-agent", action)
        self.assertIn('test -f "$pkg/index.js"', action)
        self.assertIn('ln -sfn /opt/cursor-agent/cursor-agent /usr/local/bin/agent', action)
        self.assertNotIn(
            "install -m 755 /root/.local/bin/agent /usr/local/bin/agent", action)
        for name, expected_mode in {
                "generative-research.yml": "generative",
                "hourly-twitter.yml": "twitter",
                "cursor-cli-canary.yml": "canary",
        }.items():
            doc = yaml.safe_load((REPO_ROOT / ".github" / "workflows" / name)
                                 .read_text(encoding="utf-8"))
            calls = [step for job in (doc.get("jobs") or {}).values()
                     for step in (job.get("steps") or [])
                     if "run-cursor-container" in str(step.get("uses") or "")]
            self.assertTrue(calls, name)
            self.assertTrue(all((step.get("with") or {}).get("mode") == expected_mode
                                for step in calls), name)
        self.assertNotIn('--volume "$HOME', action)
        self.assertNotIn("--privileged", action)

    def test_container_action_host_scripts_parse_under_bash(self):
        # Regression for Cursor CLI Canary run 31993098610 / RSS 31991149151:
        # the container body is wrapped in bash -lc '...', so a single quote
        # anywhere in that body (pattern literals OR comment apostrophes)
        # ends the outer string early and turns the rest into a host-shell
        # syntax error before docker ever starts.
        actions = (
            REPO_ROOT / ".github" / "actions" / "run-cursor-container" / "action.yml",
            REPO_ROOT / ".github" / "actions" / "run-opencode-container" / "action.yml",
        )
        for action_path in actions:
            with self.subTest(action=action_path.parent.name):
                action_doc = yaml.safe_load(
                    action_path.read_text(encoding="utf-8"))
                run = "\n".join(
                    step.get("run") or ""
                    for step in action_doc["runs"]["steps"])
                self.assertIn("bash -lc '", run, action_path)
                start = run.index("bash -lc '") + len("bash -lc '")
                end = run.index("\n  ')", start)
                body = run[start:end]
                self.assertNotIn(
                    "'", body,
                    f"{action_path}: apostrophe inside bash -lc body "
                    f"(use double quotes for regexes; reword comments)")
                self.assertRegex(
                    body,
                    r'(cursor|opencode)_fatal_pattern="[^"]+"',
                    f"{action_path}: fatal_pattern must be double-quoted")
                with tempfile.NamedTemporaryFile(
                        "w", suffix=".sh", delete=False) as fh:
                    fh.write(run)
                    script_path = fh.name
                try:
                    checked = subprocess.run(
                        ["bash", "-n", script_path],
                        capture_output=True, text=True, check=False)
                finally:
                    Path(script_path).unlink(missing_ok=True)
                self.assertEqual(
                    0, checked.returncode,
                    f"{action_path}: bash -n failed:\n{checked.stderr}")

    def test_cursor_canary_probes_the_model_production_runs(self):
        model_id = self.assert_single_cursor_model()
        canary = (REPO_ROOT / ".github" / "workflows" /
                  "cursor-cli-canary.yml").read_text(encoding="utf-8")
        self.assertIn(f"model: cursor/{model_id}", canary)
        self.assertIn("CURSOR-CLI-CANARY-OK", canary)
        self.assertIn("persist-credentials: false", canary)
        self.assertIn("set-safe-directory: false", canary)
        self.assertIn(".cursor-precheckout.", canary)
        self.assertIn("quarantine_workspace", canary)
        production = json.loads(
            (REPO_ROOT / ".github" / "cursor" / "cli-config.json")
            .read_text(encoding="utf-8"))
        self.assertNotIn("model", production)
        self.assertNotIn("provider", production)
        for name in ("cli-config.json", "cli-config-canary.json", "translation.json"):
            cfg = json.loads((REPO_ROOT / ".github" / "cursor" / name)
                             .read_text(encoding="utf-8"))
            self.assertEqual(1, cfg.get("version"), name)
            self.assertEqual(False, (cfg.get("editor") or {}).get("vimMode"), name)
            self.assertIn("permissions", cfg, name)
            self.assertIsInstance((cfg["permissions"]).get("allow", []), list, name)
            self.assertIsInstance((cfg["permissions"]).get("deny", []), list, name)

    def test_cursor_twitter_tier_labels_name_the_served_model(self):
        model_id = self.assert_single_cursor_model()
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "hourly-twitter.yml").read_text(encoding="utf-8")
        arms = [chunk.split(";;", 1)[0]
                for chunk in workflow.split("cursor-grok-4p6-fast)")[1:]]
        arm = next(a for a in arms if "OUTPUT_DIR=" in a)
        family = model_id.split("-")[0].lower()
        others = {"deepseek", "kimi", "glm", "claude", "gpt", "qwen", "composer"} - {family}
        targets = [(f, next(ln for ln in arm.splitlines() if f"{f}=" in ln))
                   for f in ("TITLE_SUFFIX", "COMMIT_PREFIX", "HARNESS_LABEL")]
        targets.append(("notification title",
                        next(ln for ln in workflow.splitlines()
                             if "Twitter/X AI Pulse — Cursor CLI" in ln)))
        for field, line in targets:
            self.assertIn(family, line.lower(), f"{field} must name {family}")
            for other in others:
                self.assertNotIn(other, line.lower(),
                                 f"{field} names {other} but the tier serves {family}")

    def test_cursor_twitter_repairs_contract_once(self):
        workflow_path = (REPO_ROOT / ".github" / "workflows" /
                         "hourly-twitter.yml")
        workflow = workflow_path.read_text(encoding="utf-8")
        doc = yaml.safe_load(workflow)
        steps = doc["jobs"]["twitter"]["steps"]
        names = [step.get("name") for step in steps]
        process = next(i for i, name in enumerate(names)
                       if name == "Process tweets with Cursor CLI + Grok 4.6 Fast "
                       "(cursor-grok-4p6-fast tier)")
        repair = next(i for i, name in enumerate(names)
                      if name == "Repair Cursor Twitter contract once")
        rerun = next(i for i, name in enumerate(names)
                     if name == "Re-run Cursor CLI to repair Twitter contract")
        validate = next(i for i, name in enumerate(names)
                        if name == "Validate Twitter signal-only public output")
        self.assertLess(process, repair)
        self.assertLess(repair, rerun)
        self.assertLess(rerun, validate)
        self.assertIn("validate_twitter_public_output.py", steps[repair]["run"])
        self.assertNotIn("deterministic_twitter_digest.py", steps[repair]["run"])
        self.assertEqual(
            steps[rerun].get("uses"),
            "./.github/actions/run-cursor-container",
        )
        self.assertEqual((steps[rerun].get("with") or {}).get("mode"), "twitter")
        self.assertIn("validate_twitter_public_output.py",
                      (REPO_ROOT / ".github" / "actions" /
                       "render-twitter-prompt" / "action.yml")
                      .read_text(encoding="utf-8"))
        self.assertIn("**Cycle summary**:",
                      (REPO_ROOT / "prompts" / "twitter-analyst.md")
                      .read_text(encoding="utf-8"))
        self.assertNotIn("deterministic_twitter_digest.py",
                         workflow[workflow.index("Repair Cursor Twitter"):
                                  workflow.index(
                                      "Validate Twitter signal-only public output")])

    def test_all_dispatch_callers_prewire_cursor_credential(self):
        for obs in self.obs.values():
            for step in obs.dispatch_steps:
                self.assertEqual(
                    step.secrets.get("cursor-api-key"), "CURSOR_API_KEY", step)

    def test_opencode_cleanup_survives_cancellation_escalation(self):
        action_doc = yaml.safe_load(
            (REPO_ROOT / ".github/actions/run-opencode-container/action.yml")
            .read_text(encoding="utf-8")
        )
        run = action_doc["runs"]["steps"][0]["run"]
        start = run.index("cleanup() {")
        end = run.index("\ntrap cleanup EXIT", start)
        cleanup_function = run[start:end]

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            log = root / "docker.log"
            docker = bin_dir / "docker"
            docker.write_text(
                "#!/bin/bash\n"
                "set -eu\n"
                "case \"$*\" in\n"
                "  'container inspect ara-opencode-test') exit 0 ;;\n"
                "  'rm -f ara-opencode-test')\n"
                "    echo rm-start >> \"$DOCKER_TEST_LOG\"\n"
                "    /bin/sleep 1\n"
                "    echo rm-end >> \"$DOCKER_TEST_LOG\"\n"
                "    exit 0 ;;\n"
                "  *) exit 1 ;;\n"
                "esac\n",
                encoding="utf-8",
            )
            docker.chmod(0o755)
            timeout = bin_dir / "timeout"
            timeout.write_text(
                "#!/bin/bash\n"
                "set -eu\n"
                "shift\n"
                "exec \"$@\"\n",
                encoding="utf-8",
            )
            timeout.chmod(0o755)
            script = "\n".join([
                "set -euo pipefail",
                'container_name="ara-opencode-test"',
                'image=""', 'build_dir=""', 'isolated_workspace=""',
                'staged_prompt=""', cleanup_function,
                "trap cleanup EXIT", "trap 'exit 143' TERM", "exit 143",
            ])
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:/usr/bin:/bin"
            env["DOCKER_TEST_LOG"] = str(log)
            proc = subprocess.Popen(["bash", "-c", script], env=env)
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                if log.exists() and "rm-start" in log.read_text(encoding="utf-8"):
                    break
                time.sleep(0.02)
            else:
                proc.kill()
                self.fail("cleanup never began Docker removal")
            os.kill(proc.pid, signal.SIGTERM)
            self.assertEqual(143, proc.wait(timeout=5))
            self.assertIn("rm-end", log.read_text(encoding="utf-8"))

    def test_korean_zero_output_retry_is_bounded_and_fail_closed(self):
        """Only the exact KO zero-output state gets one shared-budget retry."""
        action_doc = yaml.safe_load(
            (REPO_ROOT / ".github/actions/run-opencode-container/action.yml")
            .read_text(encoding="utf-8")
        )
        run = action_doc["runs"]["steps"][0]["run"]
        loop = run.split("# OPENCODE_ATTEMPT_LOOP_BEGIN", 1)[1].split(
            "# OPENCODE_ATTEMPT_LOOP_END", 1)[0]

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("translate\n", encoding="utf-8")
            loop = loop.replace("/tmp/opencode-prompt.md", str(prompt))
            loop = loop.replace(
                'attempt_log="/tmp/opencode-attempt-${attempt_count}.log"',
                'attempt_log="$PWD/opencode-attempt-${attempt_count}.log"')

            timeout = bin_dir / "timeout"
            timeout.write_text(
                "#!/bin/bash\nset -eu\nshift\nexec \"$@\"\n",
                encoding="utf-8")
            timeout.chmod(0o755)
            opencode = bin_dir / "opencode"
            opencode.write_text(
                "#!/bin/bash\n"
                "set -eu\n"
                "attempt=0\n"
                "if [ -f \"$OPENCODE_ATTEMPT_FILE\" ]; then "
                "attempt=$(tr -d '\\r\\n' < \"$OPENCODE_ATTEMPT_FILE\"); fi\n"
                "attempt=$((attempt + 1))\n"
                "printf '%s\\n' \"$attempt\" > \"$OPENCODE_ATTEMPT_FILE\"\n"
                "case \"$OPENCODE_FAKE_BEHAVIOR\" in\n"
                "  retry-success)\n"
                "    if [ \"$attempt\" -eq 2 ]; then\n"
                "      mkdir -p .tmp\n"
                "      printf 'translated\\n' > .tmp/generative-translation.ko.segments.jsonl\n"
                "      echo 'translation_segment {'\n"
                "    fi\n"
                "    ;;\n"
                "  nonzero) exit 9 ;;\n"
                "  partial)\n"
                "    mkdir -p .tmp\n"
                "    printf 'partial\\n' > .tmp/generative-translation.ko.segments.jsonl\n"
                "    ;;\n"
                "  no-output) ;;\n"
                "  *) exit 98 ;;\n"
                "esac\n",
                encoding="utf-8")
            opencode.chmod(0o755)

            def run_case(name: str, lane: str, behavior: str):
                case_dir = root / name
                case_dir.mkdir()
                attempts = case_dir / "attempts"
                env = {
                    **os.environ,
                    "PATH": f"{bin_dir}:/usr/bin:/bin",
                    "AGENT_TIMEOUT_MINUTES": "1",
                    "AGENT_LANE": lane,
                    "RETURN_ARTIFACTS": ".tmp/generative-translation.ko.segments.jsonl",
                    "OPENCODE_MODEL_REF": "opencode-go/deepseek-v4-flash",
                    "OPENCODE_ATTEMPT_FILE": str(attempts),
                    "OPENCODE_FAKE_BEHAVIOR": behavior,
                }
                result = subprocess.run(
                    ["bash", "-c", "set -euo pipefail\n" + loop],
                    cwd=case_dir, env=env, text=True, capture_output=True,
                    check=False)
                return result, attempts.read_text(encoding="utf-8").strip(), (
                    case_dir / ".opencode-attempt-telemetry").read_text(
                        encoding="utf-8")

            retry, attempts, telemetry = run_case(
                "retry", "generative-research-ko", "retry-success")
            self.assertEqual(0, retry.returncode, retry.stdout + retry.stderr)
            self.assertEqual("2", attempts)
            self.assertIn("attempt_count=2", telemetry)
            self.assertIn("translation_segment_calls=1", telemetry)
            self.assertIn("artifact_count=1", telemetry)
            self.assertIn(
                "retry_reason=zero-artifact-zero-translation-segment", telemetry)

            other, attempts, telemetry = run_case(
                "other-lane", "bluesky-watch", "no-output")
            self.assertEqual(0, other.returncode, other.stdout + other.stderr)
            self.assertEqual("1", attempts)
            self.assertIn("attempt_count=1", telemetry)
            self.assertIn("retry_reason=none", telemetry)

            failed, attempts, telemetry = run_case(
                "nonzero", "generative-research-ko", "nonzero")
            self.assertEqual(0, failed.returncode, failed.stdout + failed.stderr)
            self.assertEqual("1", attempts)
            self.assertIn("last_agent_status=9", telemetry)
            self.assertIn("retry_reason=none", telemetry)

            partial, attempts, telemetry = run_case(
                "partial", "generative-research-ko", "partial")
            self.assertEqual(0, partial.returncode, partial.stdout + partial.stderr)
            self.assertEqual("1", attempts)
            self.assertIn("artifact_count=1", telemetry)
            self.assertIn("retry_reason=none", telemetry)

    def test_opencode_attempt_telemetry_is_strictly_validated(self):
        """Only the fixed five-line numeric/enumerated record is logged."""
        action_doc = yaml.safe_load(
            (REPO_ROOT / ".github/actions/run-opencode-container/action.yml")
            .read_text(encoding="utf-8")
        )
        run = action_doc["runs"]["steps"][0]["run"]
        guard = run.split("# TRUSTED_ATTEMPT_TELEMETRY_BEGIN", 1)[1].split(
            "# TRUSTED_ATTEMPT_TELEMETRY_END", 1)[0]

        with tempfile.TemporaryDirectory() as tmp:
            isolated = Path(tmp) / "isolated"
            isolated.mkdir()
            telemetry = isolated / ".opencode-attempt-telemetry"
            telemetry.write_text(
                "attempt_count=2\n"
                "last_agent_status=0\n"
                "translation_segment_calls=15\n"
                "artifact_count=1\n"
                "retry_reason=zero-artifact-zero-translation-segment\n",
                encoding="utf-8")
            valid = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + guard],
                env={**os.environ, "isolated_workspace": str(isolated),
                     "agent_status": "0"},
                text=True, capture_output=True, check=False)
            self.assertEqual(0, valid.returncode, valid.stdout + valid.stderr)
            self.assertIn("attempts=2 last_status=0 translation_segment_calls=15",
                          valid.stdout)

            telemetry.write_text(
                telemetry.read_text(encoding="utf-8") + "untrusted=field\n",
                encoding="utf-8")
            malformed = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + guard],
                env={**os.environ, "isolated_workspace": str(isolated),
                     "agent_status": "0"},
                text=True, capture_output=True, check=False)
            self.assertNotEqual(0, malformed.returncode)
            self.assertIn("attempt telemetry is malformed",
                          malformed.stdout + malformed.stderr)

    def test_editorial_mode_accepts_artifact_only_but_twitter_does_not(self):
        """Bluesky returns a temp section; Twitter still requires commit paths."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        start = shell.index('case "$RUN_MODE" in')
        end = shell.index('if [ -n "$PROMPT_FILE" ] && [ ! -f "$PROMPT_FILE" ]')
        preflight = shell[start:end]
        base_env = {
            **os.environ,
            "ALLOWED_PATHS": "",
            "RETURN_ARTIFACTS": ".tmp/bluesky-section.md",
            "OPENCODE_CONFIG_REL": ".github/opencode/opencode.json",
            "OPENCODE_MODEL_REF": "opencode-go/deepseek-v4-flash",
            "AGENT_TIMEOUT_MINUTES": "45",
            "BIRDY_TOOL_LOG_REL": "",
        }
        editorial = subprocess.run(
            ["bash", "-c", "set -euo pipefail\n" + preflight],
            env={**base_env, "RUN_MODE": "editorial"}, text=True,
            capture_output=True, check=False)
        self.assertEqual(0, editorial.returncode,
                         editorial.stdout + editorial.stderr)
        twitter = subprocess.run(
            ["bash", "-c", "set -euo pipefail\n" + preflight],
            env={**base_env, "RUN_MODE": "twitter"}, text=True,
            capture_output=True, check=False)
        self.assertNotEqual(0, twitter.returncode)
        self.assertIn("twitter mode requires allowed-paths",
                      twitter.stdout + twitter.stderr)

    def test_bird_snapshot_replaces_symlink_root_and_rejects_linked_entries(self):
        """The fetched snapshot is fresh, and only its safe tree is mounted."""
        fetch_path = (REPO_ROOT / ".github" / "actions" /
                      "twitter-fetch" / "action.yml")
        fetch_doc = yaml.safe_load(fetch_path.read_text(encoding="utf-8"))
        fetch_shell = next(
            step.get("run") or "" for step in fetch_doc["runs"]["steps"]
            if step.get("name") ==
            "Fetch tweets, searches, and news via birdy multi-fetch")
        setup = fetch_shell.split(
            "# TRUSTED_BIRD_SNAPSHOT_SETUP_BEGIN", 1)[1].split(
                "# TRUSTED_BIRD_SNAPSHOT_SETUP_END", 1)[0]
        self.assertLess(
            fetch_shell.index("# TRUSTED_BIRD_SNAPSHOT_SETUP_END"),
            fetch_shell.index("birdy multi-fetch"))

        container_path = (REPO_ROOT / ".github" / "actions" /
                          "run-opencode-container" / "action.yml")
        container_doc = yaml.safe_load(
            container_path.read_text(encoding="utf-8"))
        container_shell = "\n".join(
            step.get("run") or "" for step in container_doc["runs"]["steps"])
        mount_guard = container_shell.split(
            "# TRUSTED_BIRD_MOUNT_GUARD_BEGIN", 1)[1].split(
                "# TRUSTED_BIRD_MOUNT_GUARD_END", 1)[0]
        self.assertLess(
            container_shell.index("# TRUSTED_BIRD_MOUNT_GUARD_END"),
            container_shell.index(
                'extra_args+=(--volume "/tmp/bird:/tmp/bird:ro")'))

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            bird_root = tmp_path / "bird"
            outside = tmp_path / "outside"
            outside.mkdir()
            sentinel = outside / "sentinel.json"
            sentinel.write_text('{"keep":true}\n', encoding="utf-8")
            os.symlink(outside, bird_root, target_is_directory=True)

            def for_test(shell: str) -> str:
                self.assertEqual(1, shell.count("bird_root=/tmp/bird"))
                return shell.replace(
                    "bird_root=/tmp/bird",
                    f"bird_root={shlex.quote(str(bird_root))}", 1)

            # Before the fetch owns a new root, the exact mount guard fails.
            # Because the full action uses `set -e`, Docker argument assembly
            # and the mount that follows this guard are unreachable.
            rejected_root = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" +
                 for_test(mount_guard)],
                env={**os.environ, "MOUNT_BIRD_SNAPSHOT": "true"},
                text=True, capture_output=True, check=False)
            self.assertNotEqual(0, rejected_root.returncode)
            self.assertEqual(
                '{"keep":true}\n', sentinel.read_text(encoding="utf-8"))

            created = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + for_test(setup)],
                text=True, capture_output=True, check=False)
            self.assertEqual(0, created.returncode,
                             created.stdout + created.stderr)
            self.assertTrue(bird_root.is_dir())
            self.assertFalse(bird_root.is_symlink())
            self.assertEqual(
                0o700, stat.S_IMODE(bird_root.stat().st_mode))
            self.assertEqual(
                '{"keep":true}\n', sentinel.read_text(encoding="utf-8"))

            # A nested symlink is data to neither Birdy nor the agent. Reject
            # it just like a device/socket before constructing the bind mount.
            os.symlink(sentinel, bird_root / "linked.json")
            rejected_entry = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" +
                 for_test(mount_guard)],
                env={**os.environ, "MOUNT_BIRD_SNAPSHOT": "true"},
                text=True, capture_output=True, check=False)
            self.assertNotEqual(0, rejected_entry.returncode)
            self.assertIn("linked or special entry",
                          rejected_entry.stdout + rejected_entry.stderr)
            (bird_root / "linked.json").unlink()
            (bird_root / "safe.json").write_text("[]\n", encoding="utf-8")
            accepted = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" +
                 for_test(mount_guard)],
                env={**os.environ, "MOUNT_BIRD_SNAPSHOT": "true"},
                text=True, capture_output=True, check=False)
            self.assertEqual(0, accepted.returncode,
                             accepted.stdout + accepted.stderr)

    def test_container_birdy_fast_wrapper_executes_read_only_and_logs_redacted(self):
        wrapper = (REPO_ROOT / ".github" / "actions" /
                   "run-opencode-container" / "birdy-fast")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fake_birdy = tmp_path / "birdy"
            observed = tmp_path / "observed.txt"
            tool_log = tmp_path / "tool-log.jsonl"
            fake_birdy.write_text(
                '#!/bin/sh\n'
                'printf "%s\\n" "$BIRDY_READ_ONLY" > "$FAKE_BIRDY_OUT"\n'
                'printf "%s\\n" "$@" >> "$FAKE_BIRDY_OUT"\n'
                'printf "fake stdout\\n"\n'
                'printf "fake stderr\\n" >&2\n'
                'exit "${FAKE_BIRDY_EXIT:-0}"\n',
                encoding="utf-8")
            fake_birdy.chmod(0o755)
            env = {
                "PATH": f"{tmp_path}:/usr/bin:/bin",
                "FAKE_BIRDY_OUT": str(observed),
                "BIRDY_TOOL_LOG_PATH": str(tool_log),
            }

            result = subprocess.run(
                [str(wrapper), "--account", "account-name", "--strategy",
                 "least-used", "--vpn-server", "vpn.example", "search",
                 "private query", "--json", "--plain"],
                text=True, capture_output=True, env=env, check=False)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("fake stdout\n", result.stdout)
            self.assertEqual("fake stderr\n", result.stderr)
            self.assertEqual(
                ["1", "--account", "account-name", "--strategy", "least-used",
                 "--vpn-server", "vpn.example", "search", "private query",
                 "--json", "--plain"],
                observed.read_text(encoding="utf-8").splitlines())
            event = json.loads(tool_log.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual("birdy-fast", event["tool"])
            self.assertEqual("search", event["command"])
            self.assertIs(event["blocked"], False)
            self.assertIs(event["ok"], True)
            self.assertEqual(0, event["exit_code"])
            self.assertIsInstance(event["duration_ms"], int)
            self.assertGreaterEqual(event["duration_ms"], 0)
            self.assertIs(event["cached"], False)
            self.assertIs(event["redacted"], True)
            self.assertNotIn("private query", tool_log.read_text(encoding="utf-8"))

            observed.unlink()
            env["FAKE_BIRDY_EXIT"] = "7"
            failed = subprocess.run(
                [str(wrapper), "--account", "search", "read", "tweet-id"],
                text=True, capture_output=True, env=env, check=False)
            self.assertEqual(7, failed.returncode)
            self.assertEqual("fake stdout\n", failed.stdout)
            self.assertEqual("fake stderr\n", failed.stderr)
            failed_event = json.loads(
                tool_log.read_text(encoding="utf-8").splitlines()[-1])
            self.assertEqual("read", failed_event["command"])
            self.assertIs(failed_event["ok"], False)
            self.assertEqual(7, failed_event["exit_code"])
            self.assertIsInstance(failed_event["duration_ms"], int)
            self.assertIs(failed_event["cached"], False)

            observed.unlink()
            env.pop("FAKE_BIRDY_EXIT")
            blocked = subprocess.run(
                [str(wrapper), "reply", "tweet-id", "secret text"],
                text=True, capture_output=True, env=env, check=False)
            self.assertEqual(2, blocked.returncode)
            self.assertFalse(observed.exists(), "blocked command reached birdy")
            blocked_event = json.loads(
                tool_log.read_text(encoding="utf-8").splitlines()[-1])
            self.assertEqual("reply", blocked_event["command"])
            self.assertIs(blocked_event["blocked"], True)
            self.assertIs(blocked_event["ok"], False)
            self.assertEqual(2, blocked_event["exit_code"])
            self.assertEqual(0, blocked_event["duration_ms"])
            self.assertIs(blocked_event["cached"], False)
            self.assertNotIn("secret text", tool_log.read_text(encoding="utf-8"))

    def test_trusted_clone_setup_ignores_host_git_execution_config(self):
        """Persistent runner Git config cannot execute before container entry."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        setup = shell.split("# TRUSTED_CLONE_SETUP_BEGIN", 1)[1].split(
            "# TRUSTED_CLONE_SETUP_END", 1)[0]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            original = tmp_path / "original"
            original.mkdir()

            def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
                return subprocess.run(
                    ["git", "-C", str(repo), *args], text=True,
                    capture_output=True, check=True)

            git(original, "init", "-b", "main")
            git(original, "config", "user.name", "Clone Guard Test")
            git(original, "config", "user.email", "guard@example.invalid")
            (original / "tracked.txt").write_text("trusted\n", encoding="utf-8")
            (original / "tracked.html").write_text("<p>trusted</p>\n",
                                                   encoding="utf-8")
            git(original, "add", "tracked.txt", "tracked.html")
            git(original, "commit", "-m", "base")
            bundle = tmp_path / "payload.bundle"
            git(original, "bundle", "create", str(bundle), "--all")

            marker = tmp_path / "host-git-executed"
            fsmonitor = tmp_path / "malicious-fsmonitor"
            fsmonitor.write_text(
                "#!/bin/sh\n"
                f"printf 'fsmonitor\\n' >> '{marker}'\n"
                "printf 'test-token\\000'\n"
                "exit 0\n", encoding="utf-8")
            fsmonitor.chmod(0o755)
            git(original, "config", "core.fsmonitor", str(fsmonitor))

            evil_smudge = tmp_path / "evil-smudge"
            evil_smudge.write_text(
                "#!/bin/sh\n"
                f"printf 'smudge\\n' >> '{marker}'\n"
                "cat\n", encoding="utf-8")
            evil_smudge.chmod(0o755)
            evil_process = tmp_path / "evil-process"
            evil_process.write_text(
                "#!/bin/sh\n"
                f"printf 'process\\n' >> '{marker}'\n"
                "exit 1\n", encoding="utf-8")
            evil_process.chmod(0o755)
            git(original, "config", "filter.evil.smudge", str(evil_smudge))
            git(original, "config", "filter.evil.process", str(evil_process))
            (original / ".git" / "info" / "attributes").write_text(
                "*.html filter=evil\n", encoding="utf-8")

            evil_ssh = tmp_path / "evil-ssh"
            evil_ssh.write_text(
                "#!/bin/sh\n"
                f"printf 'ssh\\n' >> '{marker}'\n"
                "exit 1\n", encoding="utf-8")
            evil_ssh.chmod(0o755)
            git(original, "config", "core.sshCommand", str(evil_ssh))
            git(original, "config",
                "url.ssh://attacker.invalid/.insteadOf", f"{tmp_path}/")

            template = tmp_path / "malicious-template"
            hooks = template / "hooks"
            hooks.mkdir(parents=True)
            post_checkout = hooks / "post-checkout"
            post_checkout.write_text(
                "#!/bin/sh\n"
                f"printf 'template-hook\\n' >> '{marker}'\n",
                encoding="utf-8")
            post_checkout.chmod(0o755)
            global_config = tmp_path / "malicious-global-config"
            subprocess.run(
                ["git", "config", "-f", str(global_config),
                 "init.templateDir", str(template)], check=True)

            # Prove every fixture really executes under an unsanitized command,
            # so this is behavioral coverage rather than a marker that could
            # never be reached on the test host.
            subprocess.run(
                ["git", "-C", str(original), "diff", "--quiet"],
                check=False, capture_output=True)
            self.assertIn("fsmonitor", marker.read_text(encoding="utf-8"))
            marker.unlink()
            git(original, "config", "--unset", "core.fsmonitor")
            (original / "tracked.html").unlink()
            subprocess.run(
                ["git", "-C", str(original), "checkout-index", "-f", "--",
                 "tracked.html"], check=False, capture_output=True)
            self.assertIn("process", marker.read_text(encoding="utf-8"))
            marker.unlink()
            git(original, "config", "--unset", "filter.evil.process")
            (original / "tracked.html").write_text("dirty\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(original), "reset", "--hard", "HEAD"],
                check=True, capture_output=True)
            self.assertIn("smudge", marker.read_text(encoding="utf-8"))
            marker.unlink()
            git(original, "config", "filter.evil.process", str(evil_process))
            git(original, "config", "core.fsmonitor", str(fsmonitor))
            subprocess.run(
                ["git", "-C", str(original), "fetch", str(bundle), "HEAD"],
                check=False, capture_output=True)
            self.assertIn("ssh", marker.read_text(encoding="utf-8"))
            marker.unlink()
            raw_clone_env = os.environ.copy()
            raw_clone_env["GIT_CONFIG_GLOBAL"] = str(global_config)
            subprocess.run(
                ["git", "clone", "--quiet", str(original),
                 str(tmp_path / "unsafe-clone")],
                env=raw_clone_env, check=True)
            self.assertIn("template-hook", marker.read_text(encoding="utf-8"))
            marker.unlink()

            # Seed every durable local metadata bridge removed by the action.
            local_hook = original / ".git" / "hooks" / "post-checkout"
            local_hook.write_text(post_checkout.read_text(encoding="utf-8"),
                                  encoding="utf-8")
            local_hook.chmod(0o755)
            (original / ".git" / "info" / "grafts").write_text(
                "# malicious graft placeholder\n", encoding="utf-8")
            external_objects = tmp_path / "external-objects"
            external_objects.mkdir()
            (original / ".git" / "objects" / "info" / "alternates").write_text(
                str(external_objects) + "\n", encoding="utf-8")
            (original / ".git" / "objects" / "info" /
             "http-alternates").write_text(
                 "https://attacker.invalid/objects\n", encoding="utf-8")
            replace_dir = original / ".git" / "refs" / "replace"
            replace_dir.mkdir()
            external_common = tmp_path / "external-common"
            external_common.mkdir()
            (original / ".git" / "commondir").write_text(
                str(external_common) + "\n", encoding="utf-8")

            build_dir = tmp_path / "build"
            empty_template = build_dir / "empty-git-template"
            empty_template.mkdir(parents=True)
            github_env = tmp_path / "github-env"
            env = os.environ.copy()
            env.update({
                "GITHUB_WORKSPACE": str(original),
                "RUNNER_TEMP": str(tmp_path),
                "GITHUB_RUN_ID": "hostsetup",
                "GITHUB_RUN_ATTEMPT": "1",
                "RUN_MODE": "canary",
                "build_dir": str(build_dir),
                "empty_git_template": str(empty_template),
                "GIT_CONFIG_GLOBAL": str(global_config),
                "GITHUB_SERVER_URL": "https://github.com",
                "GITHUB_REPOSITORY": "example/repository",
                "GITHUB_ENV": str(github_env),
            })
            result = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + setup],
                text=True, capture_output=True, env=env, check=False)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse(marker.exists(), result.stdout + result.stderr)
            isolated = tmp_path / "opencode-workspace-hostsetup-1"
            self.assertFalse((isolated / ".git" / "hooks" /
                              "post-checkout").exists())
            self.assertFalse((isolated / "tracked.txt").exists(),
                             "host clone unexpectedly materialized a checkout")
            local_config = (original / ".git" / "config").read_text(
                encoding="utf-8")
            for forbidden in ("fsmonitor", "sshcommand", "filter.evil",
                              "insteadof", "hookspath"):
                self.assertNotIn(forbidden, local_config.lower())
            self.assertIn(
                "url = https://github.com/example/repository.git", local_config)
            self.assertIn("name = github-actions[bot]", local_config)
            for removed in (
                    original / ".git" / "info" / "attributes",
                    original / ".git" / "info" / "grafts",
                    original / ".git" / "objects" / "info" / "alternates",
                    original / ".git" / "objects" / "info" / "http-alternates",
                    original / ".git" / "refs" / "replace",
                    original / ".git" / "hooks" / "post-checkout",
                    original / ".git" / "logs",
                    original / ".git" / "commondir"):
                self.assertFalse(removed.exists(), str(removed))
            self.assertEqual(
                "+refs/heads/*:refs/remotes/origin/*",
                git(original, "config", "--local", "--get",
                    "remote.origin.fetch").stdout.strip())
            self.assertEqual(
                {"GIT_CONFIG_NOSYSTEM=1", "GIT_CONFIG_GLOBAL=/dev/null",
                 "GIT_NO_REPLACE_OBJECTS=1"},
                set(github_env.read_text(encoding="utf-8").splitlines()))

            # Representative later Git operations inherit the sanitized
            # checkout and cannot revive the removed execution paths.
            (original / "tracked.html").write_text("dirty again\n",
                                                   encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(original), "diff", "--quiet"], check=False)
            subprocess.run(
                ["git", "-C", str(original), "reset", "--hard", "HEAD"],
                check=True, capture_output=True)
            subprocess.run(
                ["git", "-C", str(original), "fetch", str(bundle), "HEAD"],
                check=True, capture_output=True)
            self.assertFalse(marker.exists(), "sanitized later Git executed a marker")

    def test_trusted_clone_setup_rejects_linked_git_control_file(self):
        """Index/HEAD plumbing must never follow a stale control-file link."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        setup = shell.split("# TRUSTED_CLONE_SETUP_BEGIN", 1)[1].split(
            "# TRUSTED_CLONE_SETUP_END", 1)[0]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            original = tmp_path / "original"
            original.mkdir()
            subprocess.run(["git", "-C", str(original), "init", "-b", "main"],
                           check=True, capture_output=True)
            subprocess.run(
                ["git", "-C", str(original), "config", "user.name", "Guard"],
                check=True)
            subprocess.run(
                ["git", "-C", str(original), "config", "user.email",
                 "guard@example.invalid"], check=True)
            (original / "tracked.txt").write_text("trusted\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(original), "add", "tracked.txt"],
                           check=True)
            subprocess.run(["git", "-C", str(original), "commit", "-m", "base"],
                           check=True, capture_output=True)

            outside_index = tmp_path / "outside-index"
            outside_index.write_text("sentinel\n", encoding="utf-8")
            index = original / ".git" / "index"
            index.unlink()
            os.symlink(outside_index, index)
            build_dir = tmp_path / "build"
            empty_template = build_dir / "empty-git-template"
            empty_template.mkdir(parents=True)
            env = os.environ.copy()
            env.update({
                "GITHUB_WORKSPACE": str(original),
                "RUNNER_TEMP": str(tmp_path),
                "GITHUB_RUN_ID": "linked-index",
                "GITHUB_RUN_ATTEMPT": "1",
                "RUN_MODE": "canary",
                "build_dir": str(build_dir),
                "empty_git_template": str(empty_template),
                "GITHUB_SERVER_URL": "https://github.com",
                "GITHUB_REPOSITORY": "example/repository",
            })
            result = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + setup],
                text=True, capture_output=True, env=env, check=False)
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("linked or malformed Git control file",
                          result.stdout + result.stderr)
            self.assertEqual("sentinel\n",
                             outside_index.read_text(encoding="utf-8"))

    def test_empty_template_clone_gets_trusted_git_info_before_container(self):
        """The empty-template clone lacks .git/info; trusted setup creates it."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        setup = shell.split("# TRUSTED_ISOLATED_CONTROL_SETUP_BEGIN", 1)[1].split(
            "# TRUSTED_ISOLATED_CONTROL_SETUP_END", 1)[0]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            origin = tmp_path / "origin"
            isolated = tmp_path / "isolated"
            empty_template = tmp_path / "empty-template"
            origin.mkdir()
            empty_template.mkdir()
            subprocess.run(["git", "-C", str(origin), "init", "-b", "main"],
                           check=True, capture_output=True)
            subprocess.run(["git", "-C", str(origin), "config", "user.name", "Setup"],
                           check=True)
            subprocess.run(["git", "-C", str(origin), "config", "user.email",
                            "setup@example.invalid"], check=True)
            (origin / "tracked.txt").write_text("trusted\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(origin), "add", "tracked.txt"],
                           check=True)
            subprocess.run(["git", "-C", str(origin), "commit", "-m", "base"],
                           check=True, capture_output=True)
            subprocess.run(
                ["git", "clone", "--quiet", "--no-hardlinks", "--no-checkout",
                 f"--template={empty_template}", str(origin), str(isolated)],
                check=True)
            # Reproduce canary 31290819841 exactly: this clone shape never
            # created .git/info, before OpenCode had a chance to touch it.
            self.assertFalse((isolated / ".git" / "info").exists())
            env = os.environ.copy()
            env["isolated_workspace"] = str(isolated)
            result = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + setup],
                text=True, capture_output=True, env=env, check=False)
            self.assertEqual(0, result.returncode,
                             result.stdout + result.stderr)
            self.assertTrue((isolated / ".git" / "info").is_dir())
            self.assertFalse((isolated / ".git" / "info").is_symlink())
            self.assertTrue((isolated / ".git" / "objects" / "info").is_dir())

    def test_container_tail_normalizes_two_commits_and_excludes_intermediate_objects(self):
        """Only one final-tree commit crosses out of the disposable clone."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        normalize = shell.split("# TRUSTED_COMMIT_NORMALIZATION_BEGIN", 1)[1].split(
            "# TRUSTED_COMMIT_NORMALIZATION_END", 1)[0]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            trusted = tmp_path / "trusted"
            isolated = tmp_path / "isolated"
            trusted.mkdir()

            def git(repo: Path, *args: str, check: bool = True):
                return subprocess.run(
                    ["git", "-C", str(repo), *args], text=True,
                    capture_output=True, check=check)

            git(trusted, "init", "-b", "main")
            git(trusted, "config", "user.name", "Trusted")
            git(trusted, "config", "user.email", "trusted@example.invalid")
            (trusted / "base.txt").write_text("base\n", encoding="utf-8")
            git(trusted, "add", "base.txt")
            git(trusted, "commit", "-m", "base")
            pre_sha = git(trusted, "rev-parse", "HEAD").stdout.strip()

            subprocess.run(["git", "clone", "--quiet", "--no-hardlinks",
                            str(trusted), str(isolated)], check=True)
            git(isolated, "config", "user.name", "Agent")
            git(isolated, "config", "user.email", "agent@example.invalid")
            arxiv = isolated / "research" / "arxiv"
            summaries = isolated / "research" / "summaries"
            arxiv.mkdir(parents=True)
            summaries.mkdir(parents=True)
            report = arxiv / "2026-08-09-papers.md"
            summary = summaries / "2026-08-09-arxiv-summary.txt"
            report.write_text("final report\n", encoding="utf-8")
            summary.write_text("overlong draft summary\n", encoding="utf-8")
            intermediate_oid = git(
                isolated, "hash-object", str(summary.relative_to(isolated))).stdout.strip()
            git(isolated, "add", str(report.relative_to(isolated)),
                str(summary.relative_to(isolated)))
            git(isolated, "commit", "-m", "report plus summary")
            first_agent_sha = git(isolated, "rev-parse", "HEAD").stdout.strip()

            summary.write_text("trimmed summary\n", encoding="utf-8")
            git(isolated, "add", str(summary.relative_to(isolated)))
            git(isolated, "commit", "-m", "trim final output")
            second_agent_sha = git(isolated, "rev-parse", "HEAD").stdout.strip()

            env = {
                **os.environ,
                "PRE_SHA": pre_sha,
                "GIT_AUTHOR_NAME": "Trusted Normalizer",
                "GIT_AUTHOR_EMAIL": "normalizer@example.invalid",
                "GIT_COMMITTER_NAME": "Trusted Normalizer",
                "GIT_COMMITTER_EMAIL": "normalizer@example.invalid",
                "RUN_MODE": "editorial",
                "ALLOWED_PATHS": (
                    "research/arxiv/2026-08-09-papers.md\n"
                    "research/summaries/2026-08-09-arxiv-summary.txt"
                ),
            }
            result = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + normalize],
                cwd=isolated, env=env, text=True, capture_output=True,
                check=False)
            self.assertEqual(0, result.returncode,
                             result.stdout + result.stderr)

            post_sha = (isolated / ".opencode-post-sha").read_text(
                encoding="utf-8").strip()
            self.assertNotIn(post_sha, {first_agent_sha, second_agent_sha})
            self.assertEqual("1", git(
                isolated, "rev-list", "--count", f"{pre_sha}..{post_sha}"
            ).stdout.strip())
            self.assertEqual(pre_sha, git(
                isolated, "rev-parse", f"{post_sha}^"
            ).stdout.strip())
            self.assertEqual("final report\n", git(
                isolated, "show",
                f"{post_sha}:research/arxiv/2026-08-09-papers.md"
            ).stdout)
            self.assertEqual("trimmed summary\n", git(
                isolated, "show",
                f"{post_sha}:research/summaries/2026-08-09-arxiv-summary.txt"
            ).stdout)

            # Unbundle into the trusted repository: the normalized final
            # commit is present, while agent commits and their intermediate-
            # only blob never crossed the static bundle boundary.
            bundle = isolated / ".opencode-export.bundle"
            git(trusted, "bundle", "verify", str(bundle))
            git(trusted, "bundle", "unbundle", str(bundle))
            self.assertEqual(0, git(
                trusted, "cat-file", "-e", f"{post_sha}^{{commit}}",
                check=False).returncode)
            for isolated_oid in (first_agent_sha, second_agent_sha, intermediate_oid):
                self.assertNotEqual(0, git(
                    trusted, "cat-file", "-e", isolated_oid,
                    check=False).returncode, isolated_oid)

    def test_container_tail_normalizes_community_and_wiki_repairs(self):
        """Exact-file and trailing-slash editorial allowlists both squash safely."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        normalize = shell.split("# TRUSTED_COMMIT_NORMALIZATION_BEGIN", 1)[1].split(
            "# TRUSTED_COMMIT_NORMALIZATION_END", 1)[0]
        cases = {
            "community-exact": (
                ["research/community/2026-08-09-hn.md",
                 "research/community/2026-08-09-reddit.md"],
                "research/community/2026-08-09-reddit.md",
                ("research/community/2026-08-09-hn.md\n"
                 "research/community/2026-08-09-reddit.md"),
            ),
            "wiki-prefix": (
                ["research/wiki/entities/deepseek.md"],
                "research/wiki/entities/deepseek.md",
                "research/wiki/",
            ),
        }

        for name, (paths, repair_path, allowed_paths) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                trusted = tmp_path / "trusted"
                isolated = tmp_path / "isolated"
                trusted.mkdir()

                def git(repo: Path, *args: str):
                    return subprocess.run(
                        ["git", "-C", str(repo), *args], text=True,
                        capture_output=True, check=True)

                git(trusted, "init", "-b", "main")
                git(trusted, "config", "user.name", "Trusted")
                git(trusted, "config", "user.email", "trusted@example.invalid")
                (trusted / "base.txt").write_text("base\n", encoding="utf-8")
                git(trusted, "add", "base.txt")
                git(trusted, "commit", "-m", "base")
                pre_sha = git(trusted, "rev-parse", "HEAD").stdout.strip()
                subprocess.run(["git", "clone", "--quiet", "--no-hardlinks",
                                str(trusted), str(isolated)], check=True)
                git(isolated, "config", "user.name", "Agent")
                git(isolated, "config", "user.email", "agent@example.invalid")
                for rel in paths:
                    target = isolated / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("draft\n", encoding="utf-8")
                git(isolated, "add", *paths)
                git(isolated, "commit", "-m", "initial editorial output")
                (isolated / repair_path).write_text("repaired\n", encoding="utf-8")
                git(isolated, "add", repair_path)
                git(isolated, "commit", "-m", "repair editorial output")

                env = {
                    **os.environ,
                    "PRE_SHA": pre_sha,
                    "RUN_MODE": "editorial",
                    "ALLOWED_PATHS": allowed_paths,
                    "GIT_AUTHOR_NAME": "Trusted Normalizer",
                    "GIT_AUTHOR_EMAIL": "normalizer@example.invalid",
                    "GIT_COMMITTER_NAME": "Trusted Normalizer",
                    "GIT_COMMITTER_EMAIL": "normalizer@example.invalid",
                }
                result = subprocess.run(
                    ["bash", "-c", "set -euo pipefail\n" + normalize],
                    cwd=isolated, env=env, text=True, capture_output=True,
                    check=False)
                self.assertEqual(0, result.returncode,
                                 result.stdout + result.stderr)
                post_sha = (isolated / ".opencode-post-sha").read_text(
                    encoding="utf-8").strip()
                self.assertEqual("1", git(
                    isolated, "rev-list", "--count", f"{pre_sha}..{post_sha}"
                ).stdout.strip())
                self.assertEqual("repaired\n", git(
                    isolated, "show", f"{post_sha}:{repair_path}"
                ).stdout)

    def test_container_tail_refuses_to_normalize_rewritten_history(self):
        """Normalization cannot disguise an agent HEAD unrelated to PRE_SHA."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        normalize = shell.split("# TRUSTED_COMMIT_NORMALIZATION_BEGIN", 1)[1].split(
            "# TRUSTED_COMMIT_NORMALIZATION_END", 1)[0]

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "isolated"
            repo.mkdir()

            def git(*args: str):
                return subprocess.run(
                    ["git", "-C", str(repo), *args], text=True,
                    capture_output=True, check=True)

            git("init", "-b", "main")
            git("config", "user.name", "Agent")
            git("config", "user.email", "agent@example.invalid")
            (repo / "base.txt").write_text("base\n", encoding="utf-8")
            git("add", "base.txt")
            git("commit", "-m", "base")
            pre_sha = git("rev-parse", "HEAD").stdout.strip()
            git("checkout", "--orphan", "rewritten")
            git("rm", "-rf", ".")
            (repo / "other.txt").write_text("unrelated\n", encoding="utf-8")
            git("add", "other.txt")
            git("commit", "-m", "unrelated root")

            result = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + normalize],
                cwd=repo, env={**os.environ, "PRE_SHA": pre_sha}, text=True,
                capture_output=True, check=False)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("does not descend from the pre-run HEAD",
                          result.stdout + result.stderr)
            self.assertFalse((repo / ".opencode-export.bundle").exists())

    def test_container_tail_preserves_generative_and_canary_contracts(self):
        """Generative repairs normalize, while canary commits remain forbidden."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        normalize = shell.split("# TRUSTED_COMMIT_NORMALIZATION_BEGIN", 1)[1].split(
            "# TRUSTED_COMMIT_NORMALIZATION_END", 1)[0]

        def initialized_repo(tmp_path: Path):
            repo = tmp_path / "isolated"
            repo.mkdir()

            def git(*args: str):
                return subprocess.run(
                    ["git", "-C", str(repo), *args], text=True,
                    capture_output=True, check=True)

            git("init", "-b", "main")
            git("config", "user.name", "Agent")
            git("config", "user.email", "agent@example.invalid")
            index = repo / "research" / "generative" / "index.json"
            index.parent.mkdir(parents=True)
            index.write_text("[]\n", encoding="utf-8")
            git("add", str(index.relative_to(repo)))
            git("commit", "-m", "base")
            return repo, git, git("rev-parse", "HEAD").stdout.strip()

        trusted_identity = {
            "GIT_AUTHOR_NAME": "Trusted Normalizer",
            "GIT_AUTHOR_EMAIL": "normalizer@example.invalid",
            "GIT_COMMITTER_NAME": "Trusted Normalizer",
            "GIT_COMMITTER_EMAIL": "normalizer@example.invalid",
        }
        with self.subTest(mode="generative"), tempfile.TemporaryDirectory() as tmp:
            repo, git, pre_sha = initialized_repo(Path(tmp))
            generated = repo / "research" / "generative"
            html = generated / "deepseek.html"
            source = generated / "deepseek.ara.md"
            index = generated / "index.json"
            html.write_text("draft\n", encoding="utf-8")
            source.write_text("source\n", encoding="utf-8")
            index.write_text('["deepseek"]\n', encoding="utf-8")
            git("add", str(index.relative_to(repo)), str(html.relative_to(repo)),
                str(source.relative_to(repo)))
            git("commit", "-m", "write generative output")
            html.write_text("repaired\n", encoding="utf-8")
            git("add", str(html.relative_to(repo)))
            git("commit", "-m", "repair generated html")
            result = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + normalize], cwd=repo,
                env={**os.environ, **trusted_identity, "PRE_SHA": pre_sha,
                     "RUN_MODE": "generative", "ALLOWED_PATHS": ""},
                text=True, capture_output=True, check=False)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            post_sha = (repo / ".opencode-post-sha").read_text(
                encoding="utf-8").strip()
            self.assertEqual("1", git(
                "rev-list", "--count", f"{pre_sha}..{post_sha}"
            ).stdout.strip())
            changed = git(
                "diff", "--name-status", f"{pre_sha}..{post_sha}"
            ).stdout.splitlines()
            self.assertEqual(
                ["A\tresearch/generative/deepseek.ara.md",
                 "A\tresearch/generative/deepseek.html",
                 "M\tresearch/generative/index.json"],
                changed)

        with self.subTest(mode="canary"), tempfile.TemporaryDirectory() as tmp:
            repo, git, pre_sha = initialized_repo(Path(tmp))
            git("commit", "--allow-empty", "-m", "unexpected canary commit")
            result = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + normalize], cwd=repo,
                env={**os.environ, **trusted_identity, "PRE_SHA": pre_sha,
                     "RUN_MODE": "canary", "ALLOWED_PATHS": ""},
                text=True, capture_output=True, check=False)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("canary opencode run created a commit",
                          result.stdout + result.stderr)
            self.assertFalse((repo / ".opencode-export.bundle").exists())

    def test_container_tail_rejects_hidden_forbidden_long_and_merge_chains(self):
        """Squashing never conceals forbidden, unbounded, or merged history."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        normalize = shell.split("# TRUSTED_COMMIT_NORMALIZATION_BEGIN", 1)[1].split(
            "# TRUSTED_COMMIT_NORMALIZATION_END", 1)[0]

        def initialized_repo(tmp_path: Path):
            repo = tmp_path / "isolated"
            repo.mkdir()

            def git(*args: str, check: bool = True):
                return subprocess.run(
                    ["git", "-C", str(repo), *args], text=True,
                    capture_output=True, check=check)

            git("init", "-b", "main")
            git("config", "user.name", "Agent")
            git("config", "user.email", "agent@example.invalid")
            (repo / "base.txt").write_text("base\n", encoding="utf-8")
            git("add", "base.txt")
            git("commit", "-m", "base")
            return repo, git, git("rev-parse", "HEAD").stdout.strip()

        def normalize_result(repo: Path, pre_sha: str, allowed: str):
            return subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + normalize], cwd=repo,
                env={
                    **os.environ,
                    "PRE_SHA": pre_sha,
                    "RUN_MODE": "editorial",
                    "ALLOWED_PATHS": allowed,
                    "GIT_AUTHOR_NAME": "Trusted Normalizer",
                    "GIT_AUTHOR_EMAIL": "normalizer@example.invalid",
                    "GIT_COMMITTER_NAME": "Trusted Normalizer",
                    "GIT_COMMITTER_EMAIL": "normalizer@example.invalid",
                },
                text=True, capture_output=True, check=False)

        with self.subTest(case="hidden-forbidden"), tempfile.TemporaryDirectory() as tmp:
            repo, git, pre_sha = initialized_repo(Path(tmp))
            allowed = "research/arxiv/report.md"
            (repo / allowed).parent.mkdir(parents=True)
            (repo / allowed).write_text("draft\n", encoding="utf-8")
            forbidden = repo / "scripts" / "poison.sh"
            forbidden.parent.mkdir()
            forbidden.write_text("echo poison\n", encoding="utf-8")
            git("add", allowed, "scripts/poison.sh")
            git("commit", "-m", "draft with hidden forbidden path")
            (repo / allowed).write_text("final\n", encoding="utf-8")
            forbidden.unlink()
            git("add", allowed, "scripts/poison.sh")
            git("commit", "-m", "hide forbidden path")
            result = normalize_result(repo, pre_sha, allowed)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("intermediate commit changed forbidden path/status",
                          result.stdout + result.stderr)
            self.assertFalse((repo / ".opencode-export.bundle").exists())

        with self.subTest(case="hidden-executable-mode"), tempfile.TemporaryDirectory() as tmp:
            repo, git, pre_sha = initialized_repo(Path(tmp))
            allowed = "research/wiki/report.md"
            target = repo / allowed
            target.parent.mkdir(parents=True)
            target.write_text("draft\n", encoding="utf-8")
            target.chmod(0o755)
            git("add", allowed)
            git("commit", "-m", "write executable intermediate output")
            target.chmod(0o644)
            target.write_text("final\n", encoding="utf-8")
            git("add", allowed)
            git("commit", "-m", "repair output mode")
            result = normalize_result(repo, pre_sha, allowed)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("not a <=5 MiB regular non-executable blob",
                          result.stdout + result.stderr)
            self.assertFalse((repo / ".opencode-export.bundle").exists())

        with self.subTest(case="chain-too-long"), tempfile.TemporaryDirectory() as tmp:
            repo, git, pre_sha = initialized_repo(Path(tmp))
            allowed = "research/wiki/log.md"
            target = repo / allowed
            target.parent.mkdir(parents=True)
            for i in range(9):
                target.write_text(f"revision {i}\n", encoding="utf-8")
                git("add", allowed)
                git("commit", "-m", f"revision {i}")
            result = normalize_result(repo, pre_sha, allowed)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("must contain 1-8 commits; got 9",
                          result.stdout + result.stderr)
            self.assertFalse((repo / ".opencode-export.bundle").exists())

        with self.subTest(case="merge"), tempfile.TemporaryDirectory() as tmp:
            repo, git, pre_sha = initialized_repo(Path(tmp))
            side_path = "research/community/side.md"
            main_path = "research/community/main.md"
            git("checkout", "-b", "side")
            (repo / side_path).parent.mkdir(parents=True)
            (repo / side_path).write_text("side\n", encoding="utf-8")
            git("add", side_path)
            git("commit", "-m", "side output")
            git("checkout", "main")
            (repo / main_path).parent.mkdir(parents=True)
            (repo / main_path).write_text("main\n", encoding="utf-8")
            git("add", main_path)
            git("commit", "-m", "main output")
            git("merge", "--no-ff", "side", "-m", "merge agent outputs")
            result = normalize_result(
                repo, pre_sha, f"{side_path}\n{main_path}")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("merge-free linear chain rooted at PRE_SHA",
                          result.stdout + result.stderr)
            self.assertFalse((repo / ".opencode-export.bundle").exists())

    def test_trusted_import_guard_rejects_forbidden_committed_path(self):
        """Execute the real inline guard against an adversarial static bundle."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        guard = shell.split("# TRUSTED_IMPORT_GUARD_BEGIN", 1)[1].split(
            "# TRUSTED_IMPORT_GUARD_END", 1)[0]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            original = tmp_path / "original"
            isolated = tmp_path / "isolated"
            original.mkdir()

            def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
                return subprocess.run(
                    ["git", "-C", str(repo), *args], text=True,
                    capture_output=True, check=True)

            git(original, "init", "-b", "main")
            git(original, "config", "user.name", "Guard Test")
            git(original, "config", "user.email", "guard@example.invalid")
            (original / "research" / "generative").mkdir(parents=True)
            (original / "scripts").mkdir()
            (original / "research" / "generative" / "index.json").write_text(
                "[]\n", encoding="utf-8")
            (original / "scripts" / "validator.py").write_text(
                "TRUSTED = True\n", encoding="utf-8")
            git(original, "add", ".")
            git(original, "commit", "-m", "base")
            pre_sha = git(original, "rev-parse", "HEAD").stdout.strip()

            subprocess.run(
                ["git", "clone", "--quiet", "--no-hardlinks",
                 str(original), str(isolated)], check=True)
            git(isolated, "config", "user.name", "Attacker")
            git(isolated, "config", "user.email", "attacker@example.invalid")
            (isolated / "scripts" / "validator.py").write_text(
                "TRUSTED = False\n", encoding="utf-8")
            git(isolated, "add", "scripts/validator.py")
            git(isolated, "commit", "-m", "poison validator")
            post_sha = git(isolated, "rev-parse", "HEAD").stdout.strip()
            git(isolated, "bundle", "create", ".opencode-export.bundle",
                "HEAD", f"^{pre_sha}")
            (isolated / ".opencode-post-sha").write_text(
                post_sha + "\n", encoding="utf-8")

            build_dir = tmp_path / "build"
            build_dir.mkdir()
            env = os.environ.copy()
            env.update({
                "GITHUB_WORKSPACE": str(original),
                "isolated_workspace": str(isolated),
                "pre_sha": pre_sha,
                "RUN_MODE": "generative",
                "ALLOWED_PATHS": "",
                "BIRDY_TOOL_LOG_REL": "",
                "agent_status": "0",
                "build_dir": str(build_dir),
            })
            result = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + guard],
                text=True, capture_output=True, env=env, check=False)
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("forbidden path/status", result.stdout + result.stderr)
            self.assertEqual(pre_sha, git(original, "rev-parse", "HEAD").stdout.strip())
            self.assertEqual("TRUSTED = True\n",
                             (original / "scripts" / "validator.py").read_text(
                                 encoding="utf-8"))
            self.assertEqual("", git(original, "status", "--porcelain").stdout)

    def test_trusted_import_guard_rejects_artifact_parent_symlink(self):
        """A regular final file cannot escape through a linked parent."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        guard = shell.split("# TRUSTED_IMPORT_GUARD_BEGIN", 1)[1].split(
            "# TRUSTED_IMPORT_GUARD_END", 1)[0]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            original = tmp_path / "original"
            isolated = tmp_path / "isolated"
            outside = tmp_path / "outside-host-dir"
            original.mkdir()
            outside.mkdir()

            def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
                return subprocess.run(
                    ["git", "-C", str(repo), *args], text=True,
                    capture_output=True, check=True)

            git(original, "init", "-b", "main")
            git(original, "config", "user.name", "Artifact Guard Test")
            git(original, "config", "user.email", "guard@example.invalid")
            (original / "tracked.txt").write_text("trusted\n", encoding="utf-8")
            git(original, "add", "tracked.txt")
            git(original, "commit", "-m", "base")
            pre_sha = git(original, "rev-parse", "HEAD").stdout.strip()
            (original / ".twitter-input").mkdir()

            subprocess.run(
                ["git", "clone", "--quiet", "--no-hardlinks",
                 str(original), str(isolated)], check=True)
            (isolated / ".opencode-post-sha").write_text(
                pre_sha + "\n", encoding="utf-8")
            (outside / "birdy-tool-log.jsonl").write_text(
                '{"tool":"birdy-fast"}\n', encoding="utf-8")
            os.symlink(outside, isolated / ".twitter-input",
                       target_is_directory=True)

            build_dir = tmp_path / "build"
            build_dir.mkdir()
            env = os.environ.copy()
            env.update({
                "GITHUB_WORKSPACE": str(original),
                "isolated_workspace": str(isolated),
                "pre_sha": pre_sha,
                "RUN_MODE": "twitter",
                "ALLOWED_PATHS": "research/twitter/test.md",
                "BIRDY_TOOL_LOG_REL": ".twitter-input/birdy-tool-log.jsonl",
                "agent_status": "0",
                "build_dir": str(build_dir),
            })
            result = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + guard],
                text=True, capture_output=True, env=env, check=False)
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("escapes the isolated workspace or crosses a symlink",
                          result.stdout + result.stderr)
            self.assertFalse(
                (original / ".twitter-input" / "birdy-tool-log.jsonl").exists())

    def test_trusted_import_guard_imports_exact_generative_bundle_and_data(self):
        """A valid writer commit crosses the bundle boundary and nothing else."""
        action_path = (REPO_ROOT / ".github" / "actions" /
                       "run-opencode-container" / "action.yml")
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        shell = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        guard = shell.split("# TRUSTED_IMPORT_GUARD_BEGIN", 1)[1].split(
            "# TRUSTED_IMPORT_GUARD_END", 1)[0]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            original = tmp_path / "original"
            isolated = tmp_path / "isolated"
            original.mkdir()

            def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
                return subprocess.run(
                    ["git", "-C", str(repo), *args], text=True,
                    capture_output=True, check=True)

            git(original, "init", "-b", "main")
            git(original, "config", "user.name", "Guard Test")
            git(original, "config", "user.email", "guard@example.invalid")
            gen_dir = original / "research" / "generative"
            gen_dir.mkdir(parents=True)
            (gen_dir / "index.json").write_text("[]\n", encoding="utf-8")
            git(original, "add", ".")
            git(original, "commit", "-m", "base")
            pre_sha = git(original, "rev-parse", "HEAD").stdout.strip()

            subprocess.run(
                ["git", "clone", "--quiet", "--no-hardlinks",
                 str(original), str(isolated)], check=True)
            git(isolated, "config", "user.name", "Writer")
            git(isolated, "config", "user.email", "writer@example.invalid")
            isolated_gen = isolated / "research" / "generative"
            html_name = "2026-08-08T000000--valid.html"
            ara_name = "2026-08-08T000000--valid.ara.md"
            (isolated_gen / "index.json").write_text(
                '[{"slug":"valid","file":"' + html_name + '"}]\n',
                encoding="utf-8")
            (isolated_gen / html_name).write_text(
                '<article class="ara-article"></article>\n', encoding="utf-8")
            (isolated_gen / ara_name).write_text(
                '---\ntitle: Valid\n---\n\n## Valid\n', encoding="utf-8")
            git(isolated, "add", "research/generative")
            git(isolated, "commit", "-m", "valid writer output")
            post_sha = git(isolated, "rev-parse", "HEAD").stdout.strip()
            git(isolated, "bundle", "create", ".opencode-export.bundle",
                "HEAD", f"^{pre_sha}")
            (isolated / ".opencode-post-sha").write_text(
                post_sha + "\n", encoding="utf-8")
            methodology = {
                ".gen-verifier-findings.json": '{"findings":[]}\n',
                ".gen-redteam-findings.json": '{"findings":[]}\n',
                ".gen-claims-ledger.json": '{"claims":[]}\n',
            }
            for name, content in methodology.items():
                (isolated / name).write_text(content, encoding="utf-8")

            marker = tmp_path / "host-reset-executed"
            fsmonitor = tmp_path / "malicious-fsmonitor"
            fsmonitor.write_text(
                "#!/bin/sh\n"
                f"printf 'fsmonitor\\n' >> '{marker}'\n"
                "printf 'test-token\\000'\n"
                "exit 0\n", encoding="utf-8")
            fsmonitor.chmod(0o755)
            hooks = tmp_path / "malicious-hooks"
            hooks.mkdir()
            post_checkout = hooks / "post-checkout"
            post_checkout.write_text(
                "#!/bin/sh\n"
                f"printf 'hook\\n' >> '{marker}'\n",
                encoding="utf-8")
            post_checkout.chmod(0o755)
            git(original, "config", "core.fsmonitor", str(fsmonitor))
            git(original, "config", "core.hooksPath", str(hooks))

            evil_filter = tmp_path / "evil-filter"
            evil_filter.write_text(
                "#!/bin/sh\n"
                f"printf 'filter\\n' >> '{marker}'\n"
                "cat\n", encoding="utf-8")
            evil_filter.chmod(0o755)
            evil_process = tmp_path / "evil-filter-process"
            evil_process.write_text(
                "#!/bin/sh\n"
                f"printf 'filter-process\\n' >> '{marker}'\n"
                "exit 1\n", encoding="utf-8")
            evil_process.chmod(0o755)
            git(original, "config", "filter.evil.smudge", str(evil_filter))
            git(original, "config", "filter.evil.process", str(evil_process))
            (original / ".git" / "info" / "attributes").write_text(
                "*.html filter=evil\n", encoding="utf-8")

            evil_ssh = tmp_path / "evil-ssh"
            evil_ssh.write_text(
                "#!/bin/sh\n"
                f"printf 'ssh\\n' >> '{marker}'\n"
                "exit 1\n", encoding="utf-8")
            evil_ssh.chmod(0o755)
            git(original, "config", "core.sshCommand", str(evil_ssh))
            git(original, "config",
                "url.ssh://attacker.invalid/.insteadOf", f"{tmp_path}/")

            # Calibrate the exact transport exploit: an ordinary fetch of the
            # absolute bundle path is rewritten to SSH and executes local
            # core.sshCommand. The guard below must import the same bundle
            # without touching that transport layer.
            subprocess.run(
                ["git", "-C", str(original), "fetch",
                 str(isolated / ".opencode-export.bundle"), "HEAD"],
                check=False, capture_output=True)
            self.assertIn("ssh", marker.read_text(encoding="utf-8"))
            marker.unlink()

            build_dir = tmp_path / "build"
            build_dir.mkdir()
            env = os.environ.copy()
            env.update({
                "GITHUB_WORKSPACE": str(original),
                "isolated_workspace": str(isolated),
                "pre_sha": pre_sha,
                "RUN_MODE": "generative",
                "ALLOWED_PATHS": "",
                "BIRDY_TOOL_LOG_REL": "",
                "agent_status": "0",
                "build_dir": str(build_dir),
            })
            result = subprocess.run(
                ["bash", "-c", "set -euo pipefail\n" + guard],
                text=True, capture_output=True, env=env, check=False)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse(marker.exists(), result.stdout + result.stderr)
            self.assertEqual(post_sha, git(original, "rev-parse", "HEAD").stdout.strip())
            self.assertTrue((original / "research" / "generative" / html_name).is_file())
            self.assertTrue((original / "research" / "generative" / ara_name).is_file())
            for name, content in methodology.items():
                self.assertEqual(content, (original / name).read_text(encoding="utf-8"))

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
        obs["daily-digest.yml"].agent_run[0].secrets["zai-api-key"] = ""
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("zai-api-key" in e for e in errors), errors)

    def test_explicit_backend_in_workflow_is_an_error(self):
        lanes, obs = self.mutated()
        obs["daily-digest.yml"].agent_run[0].raw_backend = "fireworks-glm-5p2"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("explicit backend" in e for e in errors), errors)

    def test_suffixed_dispatch_action_is_not_trusted(self):
        source = REPO_ROOT / ".github/workflows/hourly-rss.yml"
        with tempfile.TemporaryDirectory() as tmp:
            mutated = Path(tmp) / "hourly-rss.yml"
            mutated.write_text(source.read_text().replace(
                "uses: ./.github/actions/agent-dispatch",
                "uses: ./.github/actions/agent-dispatch-evil",
            ))
            observed = observe_workflow(mutated)
        self.assertEqual([], observed.dispatch_steps)

    def test_unknown_lane_is_an_error(self):
        lanes, obs = self.mutated()
        obs["daily-digest.yml"].agent_run[0].lane = "no-such-lane"
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

    def test_opencode_mirror_divergence_is_an_error(self):
        lanes, obs = self.mutated()
        obs["hourly-rss.yml"].dispatch_steps[0].lane = "community"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("belongs to workflow" in e for e in errors), errors)

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
        obs["daily-digest.yml"].agent_run[1].lane = \
            obs["daily-digest.yml"].agent_run[0].lane
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("2 agent-run steps" in e for e in errors), errors)

    def test_duplicate_named_opencode_lane_across_steps_is_an_error(self):
        lanes, obs = self.mutated()
        duplicate = copy.deepcopy(obs["hourly-rss.yml"].dispatch_steps[0])
        obs["hourly-rss.yml"].dispatch_steps.append(duplicate)
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("2 agent-dispatch steps" in e for e in errors), errors)

    def test_lane_workflow_mismatch_is_an_error(self):
        lanes, obs = self.mutated()
        lanes["rss"]["workflow"] = "2h-bluesky.yml"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("belongs to workflow" in e for e in errors), errors)

    def test_wrong_harness_for_opencode_lane_is_an_error(self):
        lanes, obs = self.mutated()
        lanes["rss"]["route"] = "no-such-route"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("unknown route" in e for e in errors), errors)

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
        routes = copy.deepcopy(json.loads(LANES_FILE.read_text())["routes"])
        routes["research-editorial"]["fallback"] = True
        errors = cross_check(lanes, obs, self.profiles, routes)
        self.assertTrue(any("fallback must be" in e for e in errors), errors)

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
