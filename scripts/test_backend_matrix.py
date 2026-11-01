"""Invariant tests for the backend routing SSOT (data/agent-backends.json)
and its validator/generator (scripts/build_backend_matrix.py).

These pin the load-bearing routing facts — if a change flips one, the test
failing is the signal to update BOTH the routing intent and this pin, not to
loosen the parser. (Doc-freshness itself is the separate `--check` CI step.)
"""

import copy
import json
import datetime
import os
import re
import signal
import shlex
import stat
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from unittest import mock
from pathlib import Path

import yaml

from build_backend_matrix import (
    LANES_FILE,
    Profile,
    build_readme_diagram,
    build_rows,
    check_fallback,
    check_opencode_selectors,
    cross_check,
    generative_profiles,
    load_adapters,
    load_lanes,
    load_profiles,
    load_routes,
    observe_workflow,
    workflow_files,
)
from resolve_agent_route import resolve_route
from resolve_generative_backend import load_config as load_generative_config, resolve as resolve_generative

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
            + check_opencode_selectors(self.profiles) \
            + cross_check(self.lanes, self.obs, self.profiles)
        self.assertEqual(errors, [])

    def test_research_editorial_rejects_host_checkout_adapter(self):
        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        config["routes"]["research-editorial"]["backend"] = "claude"
        for lane in ("rss", "bluesky", "community"):
            with self.assertRaisesRegex(ValueError, "isolated_workspace"):
                resolve_route(config, lane)

        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        config["routes"]["research-editorial-secondary"]["backend"] = "claude"
        for lane in ("arxiv", "wiki-ingest"):
            with self.assertRaisesRegex(ValueError, "isolated_workspace"):
                resolve_route(config, lane)

    def test_editorial_routes_temporarily_use_isolated_claude(self):
        """Cursor's weekly limit and OpenCode Go's plan are both exhausted."""
        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        for route in ("research-editorial", "research-editorial-secondary",
                      "generative-translation", "aradio"):
            self.assertEqual("claude-sonnet-5p5-isolated", config["routes"][route]["backend"])
            self.assertEqual("none", config["routes"][route]["fallback"])
        for lane in ("rss", "bluesky", "community", "arxiv", "wiki-ingest",
                     "generative-research-ko"):
            selected = resolve_route(config, lane)
            self.assertEqual("claude-container", selected.adapter, lane)
            self.assertEqual("claude/claude-sonnet-5-5", selected.model_ref, lane)
            self.assertEqual("claude-code-oauth-token", selected.credential, lane)
        # Pointing a route back is an SSOT-only edit: the profiles stay registered.
        for backend in ("cursor-grok-4p6-fast", "opencode-glm-5p3-flash",
                        "opencode-deepseek-v4-flash"):
            self.assertIn(backend, config["backends"])
            for route in ("research-editorial", "research-editorial-secondary",
                          "generative-translation"):
                repointed = copy.deepcopy(config)
                repointed["routes"][route]["backend"] = backend
                lane = next(key for key, lane in config["lanes"].items()
                            if lane.get("route") == route)
                self.assertNotEqual("claude-container",
                                    resolve_route(repointed, lane).adapter)

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
            "production_eligible": True,
        }
        config["routes"]["research-editorial"]["backend"] = "opencode-novel-flash"
        config["routes"]["research-editorial-secondary"]["backend"] = "opencode-novel-flash"
        profiles = copy.deepcopy(self.profiles)
        profile = Profile("opencode-novel-flash", "opencode", "opencode-go",
                          "novel-flash", "Novel Flash via OpenCode",
                          ["opencode-novel-flash"], production_eligible=True)
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
            "production_eligible": True,
        }
        config["routes"]["research-editorial"]["backend"] = "cursor-composer-novel"
        config["routes"]["research-editorial-secondary"]["backend"] = "cursor-composer-novel"
        profiles = copy.deepcopy(self.profiles)
        profile = Profile("cursor-composer-novel", "cursor", "cursor",
                          "composer-novel", "Composer Novel via Cursor CLI",
                          ["cursor-composer-novel"], production_eligible=True)
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
        config["routes"]["research-editorial"]["backend"] = \
            "opencode-glm-5p3-flash"
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

    def test_restricted_profiles_cannot_enter_defaults_or_fallbacks(self):
        lanes = copy.deepcopy(self.lanes)
        lanes["generative-research-default"]["backend"] = \
            "opencode-muse-spark-1p3-contributor"
        errors = cross_check(lanes, self.obs, self.profiles)
        self.assertTrue(any("default backend" in error and "production-eligible" in error
                            for error in errors), errors)

        lanes = copy.deepcopy(self.lanes)
        lanes["digest-synthesis-fallback"]["fallback_chain"].append(
            "opencode-muse-spark-1p3-contributor"
        )
        errors = cross_check(lanes, self.obs, self.profiles)
        self.assertTrue(any("fallback backend" in error and "production-eligible" in error
                            for error in errors), errors)

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
            "aradio": ("", "", ".tmp/aradio/edit.json"),
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
        self.assertEqual(3, len(local_children))
        by_uses = {child["uses"]: child for child in local_children}
        opencode = by_uses["./.github/actions/run-opencode-container"]
        cursor = by_uses["./.github/actions/run-cursor-container"]
        claude = by_uses["./.github/actions/run-claude-container"]
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
        self.assertEqual("${{ inputs.claude-code-oauth-token }}",
                         claude["with"]["claude-code-oauth-token"])
        self.assertEqual("${{ inputs.claude-config }}",
                         claude["with"]["claude-config"])
        self.assertEqual("${{ steps.route.outputs.model_ref }}", claude["with"]["model"])
        self.assertEqual("editorial", claude["with"]["mode"])
        self.assertEqual("steps.route.outputs.adapter == 'claude-container'",
                         claude.get("if"))
        for child, foreign in (
                (opencode, ("claude-code-oauth-token", "fireworks-api-key",
                            "zai-api-key", "cursor-api-key")),
                (cursor, ("claude-code-oauth-token", "fireworks-api-key",
                          "zai-api-key", "opencode-api-key")),
                (claude, ("fireworks-api-key", "zai-api-key", "opencode-api-key",
                          "cursor-api-key")),
        ):
            rendered_child = json.dumps(child, sort_keys=True)
            for secret_input in foreign:
                self.assertNotIn(secret_input, rendered_child)

        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        for name, credential in (
                ("opencode", {"opencode-go": "opencode-api-key"}),
                ("cursor", {"cursor": "cursor-api-key"}),
                ("claude-container", {"claude": "claude-code-oauth-token"}),
        ):
            adapter = config["adapters"][name]
            self.assertIs(adapter["isolated_workspace"], True)
            self.assertIs(adapter["editorial_contract"], True)
            self.assertEqual(credential, adapter["provider_credentials"])

    def test_aradio_dispatch_uses_capability_minimized_policy(self):
        """The Aradio editor reads its staged inbox and writes one ops file."""
        workflow = yaml.safe_load(
            (REPO_ROOT / ".github/workflows/aradio.yml").read_text(encoding="utf-8")
        )
        steps = workflow["jobs"]["aradio"]["steps"]
        dispatch = next(step for step in steps
                        if step.get("uses") == "./.github/actions/agent-dispatch")
        self.assertEqual(".github/cursor/aradio.json",
                         dispatch["with"].get("cursor-config"))
        self.assertEqual(".github/opencode/aradio.json",
                         dispatch["with"].get("opencode-config"))
        self.assertEqual(".github/claude/aradio.json",
                         dispatch["with"].get("claude-config"))
        claude_policy = json.loads(
            (REPO_ROOT / ".github/claude/aradio.json").read_text(encoding="utf-8"))
        # Claude Code matches Write calls against Edit rules; Write(path) rules
        # never match, so the one writable file is an Edit rule.
        self.assertEqual(["Read(.agent-input/aradio/**)", "Edit(.tmp/aradio/edit.json)"],
                         claude_policy["permissions"]["allow"])
        for denied in ("Bash", "Task", "WebFetch", "WebSearch", "NotebookEdit", "mcp__*",
                       "Read(//proc/**)", "Read(~/**)", "Edit(research/**)",
                       "Edit(.agent-input/**)", "Edit(.github/**)"):
            self.assertIn(denied, claude_policy["permissions"]["deny"])
        self.assertTrue(dispatch.get("continue-on-error"))
        self.assertNotIn("allowed-paths", dispatch["with"])
        self.assertNotIn("expected-paths", dispatch["with"])
        translation = json.loads(
            (REPO_ROOT / ".github/cursor/translation.json").read_text(encoding="utf-8"))
        cursor_policy = json.loads(
            (REPO_ROOT / ".github/cursor/aradio.json").read_text(encoding="utf-8"))
        self.assertEqual(translation["permissions"]["deny"],
                         cursor_policy["permissions"]["deny"])
        self.assertEqual(["Read(.agent-input/aradio/**/*)",
                          "Write(.tmp/aradio/edit.json)"],
                         cursor_policy["permissions"]["allow"])
        policy = json.loads(
            (REPO_ROOT / ".github/opencode/aradio.json").read_text(encoding="utf-8"))
        self.assertIs(False, policy["formatter"])
        self.assertIs(False, policy["lsp"])
        permission = policy["permission"]
        self.assertEqual("deny", permission["*"])
        self.assertEqual({"*": "deny", ".agent-input/aradio/*": "allow"},
                         permission["read"])
        self.assertEqual({"*": "deny", ".tmp/aradio/edit.json": "allow"},
                         permission["edit"])
        self.assertNotIn("bash", permission)
        self.assertNotIn("webfetch", permission)
        # Trusted host steps consume only the trusted inbox copy and the
        # validator's normalized output, never the agent's staging paths.
        by_id = {step.get("id"): step for step in steps if step.get("id")}
        validate = by_id["validate"]["run"]
        self.assertIn("--inbox \"$SCRATCH/trusted/inbox.json\"", validate)
        for step_id in ("tts", "writer"):
            self.assertIn("$SCRATCH/edit.normalized.json", by_id[step_id]["run"])
            self.assertNotIn(".agent-input", by_id[step_id]["run"])
        self.assertEqual("false", str(workflow["concurrency"]["cancel-in-progress"]).lower())

    # Each dispatched lane and its Claude Code policy. The Cursor policy is
    # what the lane ran under before the 2026-10-31 move; a lane without a
    # cursor-config input gets the dispatcher's default.
    CLAUDE_LANE_POLICIES = {
        "rss": ".github/claude/rss.json",
        "bluesky": ".github/claude/bluesky.json",
        "community": ".github/claude/community.json",
        "arxiv": ".github/claude/arxiv.json",
        "wiki-ingest": ".github/claude/wiki.json",
        "aradio": ".github/claude/aradio.json",
        "generative-research-ko": ".github/claude/translation.json",
    }

    # Every allow rule each lane holds. A capability change must show up here,
    # in review, next to the policy file it widens.
    CLAUDE_LANE_ALLOW = {
        "rss": ["Read(.agent-input/rss/**)", "Read(research/rss/**)",
                "Edit(research/rss/**)", "Bash(git add research/rss/*)",
                "Bash(git commit -m *)"],
        "bluesky": ["Read(.agent-input/bluesky/**)", "Glob", "Edit(.tmp/bluesky-section.md)"],
        "community": ["Read(.agent-input/hn/**)", "Read(.agent-input/reddit/**)",
                      "Read(research/community/**)", "Edit(research/community/**)",
                      "Bash(git add research/community/*)", "Bash(git commit -m *)"],
        "arxiv": ["Read(research/arxiv/**)", "Read(research/summaries/**)",
                  "Edit(research/arxiv/**)", "Edit(research/summaries/**)",
                  'Bash(curl -q -s "https://export.arxiv.org/api/query?*)',
                  "Bash(git add research/arxiv/*)", "Bash(git add research/summaries/*)",
                  "Bash(git commit -m *)"],
        "wiki-ingest": ["Read(docs/wiki-schema.md)", "Read(research/digest/**)",
                        "Read(research/models/tickets/**)", "Read(research/wiki/**)", "Glob",
                        "Edit(research/wiki/**)",
                        'Bash(uv run python scripts/wiki_search.py "*)',
                        "Bash(uv run python scripts/check_wiki.py)",
                        "Bash(uv run python scripts/check_wiki.py --lint)",
                        "Bash(uv run python scripts/build_wiki_index.py)",
                        "Bash(git add research/wiki/*)", "Bash(git commit -m *)"],
        "aradio": ["Read(.agent-input/aradio/**)", "Edit(.tmp/aradio/edit.json)"],
        "generative-research-ko": ["Read(.agent-input/translation-segments.json)",
                                   "Read(.tmp/generative-translation.ko.segments.jsonl)",
                                   "Edit(.tmp/generative-translation.ko.segments.jsonl)"],
    }

    @staticmethod
    def dispatch_steps() -> dict[str, tuple[dict, list[dict]]]:
        """Each dispatched lane's agent-dispatch inputs and its job's steps."""
        found = {}
        for path in workflow_files():
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
            for job in (doc.get("jobs") or {}).values():
                steps = job.get("steps") or []
                for step in steps:
                    if step.get("uses") == "./.github/actions/agent-dispatch":
                        found[step["with"]["lane"]] = (step["with"], steps)
        return found

    @classmethod
    def dispatch_inputs(cls) -> dict[str, dict]:
        return {lane: inputs for lane, (inputs, _) in cls.dispatch_steps().items()}

    @classmethod
    def lane_prompt(cls, lane: str) -> str:
        """The prompt the lane really sends: its literal prompt-text, or the one
        prompts/ file that the step named by a steps.<id>.outputs reference
        prints. Anything else fails rather than validating some other prompt."""
        inputs, steps = cls.dispatch_steps()[lane]
        prompt = str(inputs["prompt-text"])
        reference = re.fullmatch(r"\$\{\{\s*steps\.([A-Za-z0-9_-]+)\.outputs\.[A-Za-z0-9_-]+\s*\}\}",
                                 prompt.strip())
        if reference is None:
            return prompt
        producers = [step for step in steps if step.get("id") == reference.group(1)]
        assert len(producers) == 1, f"{lane}: prompt step {reference.group(1)!r} not found"
        files = set(re.findall(r"\bcat (prompts/[A-Za-z0-9_.-]+\.md)\b",
                               str(producers[0].get("run", ""))))
        assert len(files) == 1, f"{lane}: prompt step prints {sorted(files)}, not one file"
        return (REPO_ROOT / files.pop()).read_text(encoding="utf-8")

    @staticmethod
    def lane_outputs(inputs: dict) -> list[str]:
        """The lane's committed paths and returned artifacts, dates made literal."""
        paths = "\n".join(str(inputs.get(key, ""))
                          for key in ("allowed-paths", "return-artifacts"))
        prepared = "${{ steps.prepare.outputs.result_path }}"
        if prepared in paths:
            # prepare_generative_translation.py emits one fixed path.
            fixed = ".tmp/generative-translation.ko.segments.jsonl"
            source = (REPO_ROOT / "scripts/prepare_generative_translation.py").read_text(
                encoding="utf-8")
            assert f'result_path = Path("{fixed}")' in source
            paths = paths.replace(prepared, fixed)
        paths = re.sub(r"\$\{\{[^}]*\}\}", "DATE", paths)
        return [line.strip() for line in paths.splitlines() if line.strip()]

    @staticmethod
    def claude_rules(policy: dict) -> list[tuple[str, str, bool]]:
        """(kind, target, prefix) for each allow rule; kind is Read, Edit, Glob,
        git, curl or uv, and git targets are the staged directories."""
        from copy_claude_settings import CURL_RULE, GIT_ADD_RULE, GIT_COMMIT_RULE, RULE, UV_RULE
        rules = []
        for rule in policy["permissions"]["allow"]:
            if match := RULE.fullmatch(rule):
                rules.append((match.group(1), match.group(2), bool(match.group(3))))
            elif match := GIT_ADD_RULE.fullmatch(rule):
                rules.append(("git", match.group(1), True))
            elif rule == GIT_COMMIT_RULE:
                rules.append(("git", "", False))
            elif CURL_RULE.fullmatch(rule):
                rules.append(("curl", "", False))
            elif UV_RULE.fullmatch(rule):
                rules.append(("uv", "", False))
            elif rule == "Glob":
                rules.append(("Glob", "", False))
            else:
                raise AssertionError(f"unclassified Claude allow rule {rule!r}")
        return rules

    def test_every_dispatched_lane_passes_its_claude_policy(self):
        from copy_claude_settings import validate
        inputs = self.dispatch_inputs()
        self.assertEqual(set(self.CLAUDE_LANE_POLICIES), set(inputs))
        for lane, policy_path in self.CLAUDE_LANE_POLICIES.items():
            with self.subTest(lane=lane):
                self.assertEqual(policy_path, inputs[lane].get("claude-config"))
                self.assertEqual("${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}",
                                 inputs[lane].get("claude-code-oauth-token"))
                validate(json.loads((REPO_ROOT / policy_path).read_text(encoding="utf-8")))

    def test_claude_lane_policies_grant_exactly_the_reviewed_rules(self):
        self.assertEqual(set(self.CLAUDE_LANE_POLICIES), set(self.CLAUDE_LANE_ALLOW))
        for lane, policy_path in self.CLAUDE_LANE_POLICIES.items():
            with self.subTest(lane=lane):
                policy = json.loads((REPO_ROOT / policy_path).read_text(encoding="utf-8"))
                self.assertEqual(sorted(self.CLAUDE_LANE_ALLOW[lane]),
                                 sorted(policy["permissions"]["allow"]))

    def test_lane_prompt_resolves_the_prompt_each_lane_really_sends(self):
        self.assertIn("You are an RSS feed processor", self.lane_prompt("rss"))
        aradio = (REPO_ROOT / "prompts/aradio-editor.md").read_text(encoding="utf-8")
        self.assertEqual(aradio, self.lane_prompt("aradio"))
        for lane in set(self.CLAUDE_LANE_POLICIES) - {"aradio"}:
            self.assertNotEqual(aradio, self.lane_prompt(lane), lane)
        # A reference to a step that is missing, or that prints no single
        # prompts/ file, fails instead of falling back to another prompt.
        steps = self.dispatch_steps()
        rss_inputs, rss_steps = steps["rss"]
        broken = {**rss_inputs, "prompt-text": "${{ steps.prompt.outputs.text }}"}
        for job_steps in (rss_steps, rss_steps + [{"id": "prompt", "run": "echo hi"}],
                          rss_steps + [{"id": "prompt",
                                        "run": "cat prompts/a.md; cat prompts/b.md"}]):
            with mock.patch.object(type(self), "dispatch_steps",
                                   classmethod(lambda cls, s=job_steps: {"rss": (broken, s)})):
                with self.assertRaises(AssertionError):
                    self.lane_prompt("rss")

    def test_claude_lane_policies_grant_no_more_than_cursor(self):
        """Every Claude capability maps onto one the lane's Cursor policy grants."""
        def covers(pattern: str, target: str, prefix: bool) -> bool:
            if pattern == "**/*":
                return True
            if pattern.endswith("/**/*"):
                base = pattern[:-len("/**/*")]
                return (prefix and target == base) or target.startswith(base + "/")
            return not prefix and pattern == target

        def overlaps(pattern: str, target: str, prefix: bool) -> bool:
            if pattern == "**/*":
                return True
            stem = pattern[:-len("/**/*")] if pattern.endswith("/**/*") else pattern
            if pattern.endswith("/**/*"):
                hit = target == stem or target.startswith(stem + "/")
            elif pattern.endswith("*"):
                stem = stem[:-1]
                hit = target.startswith(stem)
            else:
                hit = target == stem
            return hit or (prefix and stem.startswith(target + "/"))

        def granted(rules: list[str], kind: str) -> list[str]:
            return [rule[len(kind) + 1:-1] for rule in rules
                    if rule.startswith(f"{kind}(") and rule.endswith(")")]

        inputs = self.dispatch_inputs()
        for lane, policy_path in self.CLAUDE_LANE_POLICIES.items():
            with self.subTest(lane=lane):
                cursor_path = inputs[lane].get("cursor-config", ".github/cursor/cli-config.json")
                cursor = json.loads((REPO_ROOT / cursor_path).read_text(encoding="utf-8"))
                allow, deny = cursor["permissions"]["allow"], cursor["permissions"]["deny"]
                claude = json.loads((REPO_ROOT / policy_path).read_text(encoding="utf-8"))
                shell = {"git": "git", "curl": "curl", "uv": "uv"}
                for kind, target, prefix in self.claude_rules(claude):
                    if kind in {"Read", "Edit"}:
                        cursor_kind = "Read" if kind == "Read" else "Write"
                        self.assertTrue(any(covers(p, target, prefix)
                                            for p in granted(allow, cursor_kind)),
                                        f"{lane}: Cursor grants no {cursor_kind}({target})")
                        self.assertFalse(any(overlaps(p, target, prefix)
                                             for p in granted(deny, cursor_kind)),
                                         f"{lane}: Cursor denies {cursor_kind}({target})")
                    elif kind == "Glob":
                        self.assertTrue(granted(allow, "Read"), f"{lane}: Cursor reads nothing")
                    else:
                        command = shell[kind]
                        self.assertIn(command, granted(allow, "Shell"), f"{lane}: {command}")
                        self.assertFalse({command, "*"} & set(granted(deny, "Shell")),
                                         f"{lane}: Cursor denies Shell({command})")
                claude_deny = claude["permissions"]["deny"]
                if "*" in granted(deny, "Shell"):
                    self.assertIn("Bash", claude_deny, lane)
                if "*" in granted(deny, "WebFetch"):
                    self.assertIn("WebFetch", claude_deny, lane)
                if "*" in granted(deny, "Mcp"):
                    self.assertIn("mcp__*", claude_deny, lane)

    def test_claude_lane_policies_match_each_lane_contract(self):
        """Writes, staging, and reads are exactly what each lane's contract and
        prompt use: no stray write path, no commit right for an artifact lane."""
        from copy_claude_settings import CURL_HOSTS, CURL_RULE, GIT_COMMIT_RULE, UV_RULE
        inputs = self.dispatch_inputs()
        for lane, policy_path in self.CLAUDE_LANE_POLICIES.items():
            with self.subTest(lane=lane):
                policy = json.loads((REPO_ROOT / policy_path).read_text(encoding="utf-8"))
                rules = self.claude_rules(policy)
                outputs = self.lane_outputs(inputs[lane])
                committed = [line.strip() for line in str(
                    inputs[lane].get("allowed-paths", "")).splitlines() if line.strip()]

                def writable(path: str, kind: str = "Edit") -> list[tuple]:
                    path = path.rstrip("/")
                    return [rule for rule in rules if rule[0] == kind and (
                        path == rule[1] or (rule[2] and path.startswith(rule[1] + "/")))]

                for path in outputs:
                    self.assertTrue(writable(path), f"{lane}: cannot write {path}")
                for kind, target, prefix in rules:
                    if kind == "Edit":
                        self.assertTrue(any(path.rstrip("/") == target or (
                            prefix and path.startswith(target + "/")) for path in outputs),
                            f"{lane}: Edit({target}) is no output of the lane")
                staged = [target for kind, target, prefix in rules if kind == "git" and target]
                if not committed:
                    self.assertFalse([rule for rule in rules if rule[0] == "git"], lane)
                for directory in staged:
                    self.assertTrue(any(path.startswith(directory + "/") for path in
                                        self.lane_outputs({"allowed-paths": "\n".join(committed)})),
                                    f"{lane}: git add {directory}/ stages no committed output")
                prompt = re.sub(r"\$\{\{[^}]*\}\}", "DATE", self.lane_prompt(lane))
                # A Read rule names an output (Write must read a file before
                # replacing it) or a path the prompt itself names, exactly:
                # never a parent such as Read(research/**).
                tokens = [token.rstrip(".,:;") for token in re.findall(
                    r"(?<![A-Za-z0-9_.-])[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.*{},-]+)+/?", prompt)]
                named_files = {token for token in tokens if not token.endswith("/")
                               and re.search(r"[.*]", token.rsplit("/", 1)[-1])}
                named_dirs = ({token.rstrip("/") for token in tokens} - named_files) | {
                    path.rsplit("/", 1)[0] for path in named_files}
                output_files = {path for path in outputs if not path.endswith("/")}
                output_dirs = {path.rstrip("/") for path in outputs if path.endswith("/")} | {
                    path.rsplit("/", 1)[0] for path in output_files}
                for kind, target, prefix in rules:
                    if kind == "Read":
                        justified = (target in named_dirs | output_dirs if prefix
                                     else target in named_files | output_files)
                        self.assertTrue(justified, f"{lane}: Read({target}) is neither an "
                                        "output nor a path its prompt names")
                    elif kind == "Glob":
                        self.assertTrue("`ls " in prompt, f"{lane}: its prompt lists nothing")
                staged_words = [word for line in prompt.splitlines() if "git add " in line
                                for word in line.split("git add ", 1)[1].split()]
                for directory in staged:
                    self.assertTrue(any(word.startswith(directory + "/") for word in staged_words),
                                    f"{lane}: its prompt never stages {directory}/")
                # The exact URL prefix and the exact script invocations the
                # prompt uses, compared with the rules, host and script included.
                fetched = {url.split("?", 1)[0] + "?" for url in re.findall(
                    r'curl (?:-[A-Za-z]+ )*"(https://[^"\s`]+)', prompt)}
                runs = set(re.findall(
                    r'uv run python scripts/([a-z0-9_]+)\.py(?: (--[a-z][a-z-]*\b|"))?', prompt))
                for rule in policy["permissions"]["allow"]:
                    if rule == GIT_COMMIT_RULE:
                        self.assertTrue("git commit -m " in prompt, f"{lane}: never commits")
                    elif match := CURL_RULE.fullmatch(rule):
                        self.assertIn(match.group(1), fetched, f"{lane}: its prompt never fetches {rule}")
                        host = match.group(1).removeprefix("https://").split("/", 1)[0]
                        self.assertIn(host, CURL_HOSTS, f"{lane}: {host} is not a pinned curl host")
                    elif match := UV_RULE.fullmatch(rule):
                        shape = {None: "", ' "*': '"'}.get(match.group(3), (match.group(3) or "").strip())
                        self.assertIn((match.group(2), shape), runs,
                                      f"{lane}: its prompt never runs {rule}")

    def test_documented_lane_commands_and_the_addendum_pass_the_guard(self):
        """What each lane prompt tells the model to run, and every form the
        generated addendum lists, passes the real guard under that lane's
        policy, and what a prompt forbids is refused. The 2026-10-31 arXiv and
        wiki runs failed exactly here: the prompts documented `ls` and an
        oversized curl page that the sandbox could not serve."""
        import shutil
        from copy_claude_settings import (CURL_PAGE_LIMITS, GIT_ADD_RULE, RULE, addendum,
                                          validate)
        node = shutil.which("node")
        self.assertIsNotNone(node, "node is required to run the Claude tool guard")
        guard = REPO_ROOT / ".github/actions/run-claude-container/tool-guard.mjs"
        values = {"date": "2026-10-31", "timestamp": "2026-10-31 12:00 UTC",
                  "yesterday": "2026-10-30", "hour": "12"}

        def instantiate(text: str) -> str:
            return re.sub(r"\$\{\{\s*steps\.[A-Za-z0-9_-]+\.outputs\.([A-Za-z0-9_-]+)\s*\}\}",
                          lambda match: values.get(match.group(1), "2026-10-31"), text)

        words = ("git ", "curl ", "uv ", "ls ", "cat ", "python", "jq ", "wget ")
        for lane, policy_path in self.CLAUDE_LANE_POLICIES.items():
            with self.subTest(lane=lane), tempfile.TemporaryDirectory() as tmp:
                policy = json.loads((REPO_ROOT / policy_path).read_text(encoding="utf-8"))
                allow = policy["permissions"]["allow"]
                settings, tools = validate(policy)
                settings_file = Path(tmp) / "settings.json"
                settings_file.write_text(json.dumps(settings), encoding="utf-8")
                workspace = Path(os.path.realpath(tmp)) / "workspace"
                # Every policy path and every lane output exists, as in a run.
                outputs = [instantiate(line.strip()) for key in ("allowed-paths", "return-artifacts")
                           for line in str(self.dispatch_inputs()[lane].get(key, "")).splitlines()
                           if line.strip()]
                for rule in allow:
                    if match := RULE.fullmatch(rule):
                        outputs.append(match.group(2) + ("/" if match.group(3) else ""))
                for output in outputs:
                    if "${{" in output:
                        output = ".tmp/generative-translation.ko.segments.jsonl"
                    target = workspace / output
                    if output.endswith("/"):
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.touch()

                def admitted(tool: str, tool_input: dict) -> subprocess.CompletedProcess:
                    return subprocess.run(
                        [node, str(guard), str(settings_file), str(workspace)],
                        input=json.dumps({"tool_name": tool, "tool_input": tool_input}),
                        text=True, capture_output=True, check=False)

                text = addendum(allow)
                documented = []
                for line in instantiate(self.lane_prompt(lane)).splitlines():
                    spans = [(match.start(), match.group(1))
                             for match in re.finditer(r"`([^`]+)`", line)]
                    if not spans and line.strip().startswith(words):
                        spans = [(line.index(line.strip()), line.strip())]
                    for start, command in spans:
                        if command.startswith(words):
                            negated = re.search(r"\b(?:not|NOT|never|Never)\b[^.;]*$",
                                                line[:start]) is not None
                            documented.append((command.replace("<query>", "OpenAI")
                                               .replace("<name>", "OpenAI"), negated))
                for command, negated in documented:
                    if command.startswith("ls "):
                        # The addendum sends a listing to Glob, the only lister.
                        self.assertIn("use it instead of `ls`", text, f"{lane}: {command}")
                        call = ("Glob", {"pattern": "*", "path": command[3:].strip().rstrip("/")})
                    elif command.startswith("cat "):
                        call = ("Read", {"file_path": str(workspace / command[4:].strip())})
                    else:
                        call = ("Bash", {"command": command, "description": "x"})
                    result = admitted(*call)
                    self.assertEqual(2 if negated else 0, result.returncode,
                                     f"{lane}: documented {command!r}: {result.stderr}")
                    # A documented page must also fit in what the CLI shows.
                    for host, (size, _, limit) in CURL_PAGE_LIMITS.items():
                        if command.startswith(f'curl -q -s "https://{host}/'):
                            pages = re.findall(rf"[?&]{size}=(\d+)", command)
                            self.assertTrue(pages and all(int(page) <= limit for page in pages),
                                            f"{lane}: {command!r} asks for more than {limit}")
                # Every form the addendum lists, with its placeholders filled.
                staged = [match.group(1) for rule in allow if (match := GIT_ADD_RULE.fullmatch(rule))]
                sample = f"{staged[0]}/addendum-check.md" if staged else ""
                if sample:
                    (workspace / sample).touch()
                fill = {"<path>": sample, "<message>": "Update 2026-10-31",
                        "<query>": "search_query=cat:cs.AI&start=0&max_results=40", "<text>": "OpenAI"}
                forms = re.findall(r"^  - `([^`]+)`", text, re.MULTILINE)
                self.assertEqual("Bash" in tools.split(","), bool(forms), lane)
                for form in forms:
                    for placeholder, value in fill.items():
                        form = form.replace(placeholder, value)
                    variants = [form] + ([form + ' || echo "No changes"']
                                         if form.startswith("git commit") else [])
                    for command in variants:
                        result = admitted("Bash", {"command": command, "description": "x"})
                        self.assertEqual(0, result.returncode,
                                         f"{lane}: addendum form {command!r}: {result.stderr}")
                if "Glob" in tools.split(","):
                    for rule in allow:
                        if (match := RULE.fullmatch(rule)) and match.group(1) == "Read" \
                                and match.group(3):
                            result = admitted("Glob", {"pattern": "*", "path": match.group(2)})
                            self.assertEqual(0, result.returncode, f"{lane}: {result.stderr}")

    def test_aradio_routes_to_isolated_claude(self):
        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        selected = resolve_route(config, "aradio")
        self.assertEqual("claude-container", selected.adapter)
        self.assertEqual("claude-sonnet-5p5-isolated", selected.backend)
        self.assertEqual("claude/claude-sonnet-5-5", selected.model_ref)
        self.assertEqual("claude-code-oauth-token", selected.credential)
        self.assertEqual("none", selected.fallback)
        self.assertTrue(selected.strict)
        self.assertEqual(["aradio"], [key for key, lane in config["lanes"].items()
                                      if lane.get("route") == "aradio"])
        adapter = config["adapters"]["claude-container"]
        self.assertEqual(".github/actions/run-claude-container", adapter["implementation"])
        self.assertTrue((REPO_ROOT / adapter["implementation"] / "action.yml").exists())
        backend = config["backends"]["claude-sonnet-5p5-isolated"]
        self.assertNotIn("generative", backend)
        self.assertEqual([], backend["aliases"])

    def test_claude_container_route_validation_fails_closed(self):
        def broken(mutate):
            config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
            mutate(config)
            return config

        cases = {
            "global fallback": (lambda c: c["routes"]["aradio"].update(fallback="global"),
                                "must use 'none'"),
            "other provider": (lambda c: c["backends"]["claude-sonnet-5p5-isolated"].update(
                provider="cursor"), "credential input|provider 'claude'"),
            "empty model": (lambda c: c["backends"]["claude-sonnet-5p5-isolated"].update(
                model=""), "non-empty model"),
            "alias model": (lambda c: c["backends"]["claude-sonnet-5p5-isolated"].update(
                model="sonnet"), "full claude-\\* model id"),
            "suffix model": (lambda c: c["backends"]["claude-sonnet-5p5-isolated"].update(
                model="claude-sonnet-5-5[1m]"), "full claude-\\* model id"),
            "credential remap": (lambda c: c["adapters"]["claude-container"][
                "provider_credentials"].update(claude="cursor-api-key"),
                "claude-code-oauth-token"),
            "not isolated": (lambda c: c["adapters"]["claude-container"].update(
                isolated_workspace=False), "isolated_workspace"),
            "not production": (lambda c: c["backends"]["claude-sonnet-5p5-isolated"].update(
                production_eligible=False), "production-eligible"),
        }
        for name, (mutate, message) in cases.items():
            with self.subTest(name), self.assertRaisesRegex(ValueError, message):
                resolve_route(broken(mutate), "aradio")
        # The host-checkout adapter serves the same provider and credential,
        # and must stay incompatible.
        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        config["routes"]["aradio"]["backend"] = "claude"
        with self.assertRaisesRegex(ValueError, "isolated_workspace"):
            resolve_route(config, "aradio")

    def test_isolated_claude_never_enters_a_fallback_chain(self):
        fallback = copy.deepcopy(self.fallback)
        fallback["chain"].append("claude-sonnet-5p5-isolated")
        self.assertTrue(any("fallback executes inside agent-run" in error
                            for error in check_fallback(fallback, self.profiles)))
        lanes = copy.deepcopy(self.lanes)
        lanes["digest-synthesis-fallback"]["fallback_chain"] = ["claude-sonnet-5p5-isolated"]
        errors = cross_check(lanes, self.obs, self.profiles)
        self.assertTrue(any("unsupported adapter 'claude-container'" in error
                            for error in errors), errors)

    def test_isolated_claude_lanes_route_only_through_agent_dispatch(self):
        from build_backend_matrix import ClaudeContainerStep, Observation
        obs = copy.deepcopy(self.obs)
        rogue = Observation()
        rogue.claude_container = True
        rogue.claude_container_steps.append(ClaudeContainerStep(
            "aradio.yml", "aradio", "claude/claude-sonnet-5-5", "CLAUDE_CODE_OAUTH_TOKEN",
            "direct call"))
        rogue.claude_container_steps.append(ClaudeContainerStep(
            "aradio.yml", "", "claude/sonnet", "CURSOR_API_KEY", "bad canary"))
        obs["rogue.yml"] = rogue
        errors = cross_check(self.lanes, obs, self.profiles)
        for message in ("must route through agent-dispatch",
                        "must pin one literal claude/claude-* model ref",
                        "must pass claude-code-oauth-token"):
            self.assertTrue(any(message in error for error in errors), (message, errors))

    def test_claude_container_never_runs_unsandboxed(self):
        action_path = REPO_ROOT / ".github/actions/run-claude-container/action.yml"
        action_doc = yaml.safe_load(action_path.read_text(encoding="utf-8"))
        run = "\n".join(st.get("run") or "" for st in action_doc["runs"]["steps"])
        code = "\n".join(line for line in run.splitlines()
                         if not line.lstrip().startswith("#"))
        def array(opening: str) -> list[str]:
            """The stripped lines of a bash array literal, opening line excluded."""
            lines = code.splitlines()
            start = next(i for i, line in enumerate(lines) if line.strip() == opening)
            body = []
            for line in lines[start + 1:]:
                if line.strip() in {"bash -lc '", ")"}:
                    break
                body.append(line.strip())
            return body

        # The exact container flag set: an allowlist, so an added --cap-add,
        # seccomp/apparmor override, env file, device, or host namespace fails.
        self.assertEqual([
            '--name "$container_name" \\', '--user "$(id -u):$(id -g)" \\',
            "--workdir /workspace \\", "--cap-drop ALL \\",
            "--security-opt no-new-privileges \\", "--pids-limit 512 \\", "--read-only \\",
            "--tmpfs /tmp:rw,nosuid,nodev,mode=1777 \\", "--env HOME=/tmp/claude-home \\",
            "--env XDG_CONFIG_HOME=/tmp/claude-home/.config \\",
            "--env XDG_DATA_HOME=/tmp/claude-home/.local/share \\",
            "--env XDG_CACHE_HOME=/tmp/claude-home/.cache \\",
            "--env CLAUDE_CONFIG_DIR=/tmp/claude-home/.claude \\",
            "--env DISABLE_AUTOUPDATER=1 \\",
            "--env CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \\",
            "--env CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 \\",
            "--env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 \\",
            "--env CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1 \\",
            "--env UV_CACHE_DIR=/tmp/claude-home/.cache/uv \\",
            "--env UV_PYTHON_INSTALL_DIR=/workspace/.claude-uv-python \\",
            "--env UV_LINK_MODE=copy \\", "--env UV_FROZEN=1 \\",
            "--env GITHUB_WORKSPACE=/workspace \\",
            '--env "GIT_AUTHOR_NAME=github-actions[bot]" \\',
            '--env "GIT_AUTHOR_EMAIL=41898282+github-actions[bot]@users.noreply.github.com" \\',
            '--env "GIT_COMMITTER_NAME=github-actions[bot]" \\',
            '--env "GIT_COMMITTER_EMAIL=41898282+github-actions[bot]@users.noreply.github.com" \\',
            "--env CLAUDE_MODEL_REF \\", '--env "CLAUDE_TOOLS=$claude_tools" \\',
            "--env CLAUDE_MAX_TURNS \\", "--env AGENT_TIMEOUT_MINUTES \\",
            "--env AGENT_LANE \\", "--env RUN_MODE \\", "--env ALLOWED_PATHS \\",
            "--env RETURN_ARTIFACTS \\", '--env "PRE_SHA=$pre_sha" \\',
            '--volume "$isolated_workspace:/workspace" \\',
            '--volume "$PROMPT_FILE:/tmp/claude-prompt.md:ro" \\',
            '--volume "$generated_claude_settings:/tmp/claude-config/settings.json:ro" \\',
            '"$image" \\',
        ], array("docker_cmd=(docker run --rm -i \\"))
        # The exact CLI lockdown flag set, shared by the liveness probe and
        # the one real turn so both load the settings identically.
        self.assertEqual([
            "--restricted", '--tools "$CLAUDE_TOOLS"', "--permission-mode dontAsk",
            "--permission-prompts none", "--strict-mcp-config",
            '--mcp-config "{\\"mcpServers\\":{}}"',
            "--settings /tmp/claude-config/settings.json", "--disable-slash-commands",
            "--no-session-persistence",
        ], array("claude_flags=("))
        for flag in ('claude --init-only "${claude_flags[@]}" \\',
                     'timeout "${model_budget_seconds}s" claude -p \\',
                     '--model "$claude_model" \\', '"${claude_flags[@]}" \\',
                     '--max-turns "$CLAUDE_MAX_TURNS" \\', "--output-format json \\"):
            self.assertIn(flag, [line.strip() for line in code.splitlines()],
                          f"CLI lost {flag}")
        self.assertEqual(1, code.count("claude -p \\\n"), "exactly one CLI invocation")
        self.assertEqual(1, code.count("claude --init-only"), "exactly one liveness probe")
        from copy_claude_settings import CONTAINER_LIVENESS_MARKER
        self.assertIn(f"liveness_marker={CONTAINER_LIVENESS_MARKER}", code)
        for forbidden in ("--dangerously-skip-permissions", "bypassPermissions",
                          "--allowedTools", "--allowed-tools", "--add-dir",
                          '--volume "$HOME', "seccomp", "apparmor", "systempaths",
                          "docker.sock", "-e CLAUDE_CODE_OAUTH_TOKEN",
                          "--env CLAUDE_CODE_OAUTH_TOKEN", "--env=CLAUDE_CODE_OAUTH_TOKEN"):
            self.assertNotIn(forbidden, code, f"container gained {forbidden}")
        for flag in ("--privileged", "--network", "--net", "--cap-add", "--env-file",
                     "--mount", "--device", "--pid", "--ipc", "--userns", "--uts",
                     "--cgroupns", "--group-add", "--bare"):
            self.assertNotRegex(code, rf"(^|\s){re.escape(flag)}(\s|=|$)",
                                f"container gained {flag}")
        # The CLI's own output never reaches the public log: its JSON holds
        # the reply and every denied call's input, a denied Write's content
        # included. Only the redirections and the copy for the host remain.
        self.assertNotIn('cat -- "$attempt_log"', code)
        self.assertEqual(3, code.count('"$attempt_log"'), "attempt log only redirected/copied")
        self.assertEqual(2, code.count('"$attempt_err"'), "stderr only redirected")
        self.assertIn("Docker is required for sandboxed Claude Code runs", code)
        self.assertIn("trap cleanup EXIT", code)
        self.assertIn('docker image rm -f "$image"', code)
        self.assertIn('rm -rf -- "$isolated_workspace"', code)
        self.assertIn("scripts/copy_claude_settings.py", code)
        self.assertIn("COPY tool-guard.mjs /opt/ara-claude/tool-guard.mjs", code)
        self.assertIn("sha512sum -c -", code)
        self.assertIn("claude --version", code)
        for workflow_path in sorted((REPO_ROOT / ".github/workflows").glob("*.y*ml")):
            doc = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
            for job in (doc.get("jobs") or {}).values():
                for step in job.get("steps") or []:
                    for line in (step.get("run") or "").splitlines():
                        self.assertNotRegex(
                            line.split("#", 1)[0], r"(^|[;&|]|\s)claude\s+-p\b",
                            f"{workflow_path.name}: `claude -p` outside the container")

    def test_claude_container_keeps_the_token_out_of_every_environment(self):
        action_path = REPO_ROOT / ".github/actions/run-claude-container/action.yml"
        run = "\n".join(st.get("run") or "" for st in
                        yaml.safe_load(action_path.read_text(encoding="utf-8"))["runs"]["steps"])
        code_lines = [line.strip() for line in run.splitlines()
                      if not line.lstrip().startswith("#")]
        # Every mention of the variable, in any form (-e NAME, --env NAME,
        # --env-file, export): host side it is validated, then piped by the
        # printf builtin, never argv; container side only the descriptor
        # variable names it.
        mentions = [line for line in code_lines if "CLAUDE_CODE_OAUTH_TOKEN" in line]
        self.assertEqual([
            'if [[ ! "$CLAUDE_CODE_OAUTH_TOKEN" =~ ^[A-Za-z0-9._~+/=-]{20,4096}$ ]]; then',
            "CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR=3 \\",
            'printf \'%s\\n\' "$CLAUDE_CODE_OAUTH_TOKEN" | "${docker_cmd[@]}" >"$container_out" 2>&1 &',
        ], mentions)
        for forbidden in ("--env-file", "-e CLAUDE_CODE_OAUTH_TOKEN",
                          "--env CLAUDE_CODE_OAUTH_TOKEN", "--env=CLAUDE_CODE_OAUTH_TOKEN",
                          "export CLAUDE_CODE_OAUTH_TOKEN"):
            self.assertNotIn(forbidden, run)
        self.assertIn("docker_cmd=(docker run --rm -i \\", code_lines)
        # Container side: one stdin line into a non-exported variable, handed
        # to the CLI on descriptor 3 and unset afterwards.
        self.assertIn("IFS= read -r claude_oauth_token || true", code_lines)
        self.assertIn("exec </dev/null", code_lines)
        self.assertIn("CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR=3 \\", code_lines)
        self.assertIn('3< <(printf "%s" "$claude_oauth_token") \\', code_lines)
        self.assertIn("unset claude_oauth_token", code_lines)
        self.assertNotIn("export claude_oauth_token", run)
        # Expanded exactly once: into the pipe the CLI reads.
        self.assertEqual(1, sum(line.count("$claude_oauth_token") for line in code_lines))

    def test_claude_container_trusted_blocks_match_cursor_runner(self):
        """The isolated Claude runner copies the hardened Cursor runner verbatim.

        A containment fix in one copy must land in the other, so the trusted
        spans are compared with only the adapter name normalized.
        """
        def shell(name: str) -> str:
            doc = yaml.safe_load((REPO_ROOT / ".github/actions" / name / "action.yml")
                                 .read_text(encoding="utf-8"))
            return "\n".join(st.get("run") or "" for st in doc["runs"]["steps"])

        def normalize(text: str, adapter: str) -> str:
            for spelling in (adapter.upper(), adapter.capitalize(), adapter):
                text = text.replace(spelling, "ADAPTER")
            return text

        cursor = normalize(shell("run-cursor-container"), "cursor")
        claude = normalize(shell("run-claude-container"), "claude")
        spans = (
            ("cleanup() {", "trap 'exit 130' INT"),
            ('if { [ "$RUN_MODE" = "twitter" ]', 'staged_prompt="${RUNNER_TEMP:-/tmp}'),
            ("# TRUSTED_AGENT_INPUT_GUARD_BEGIN", "# TRUSTED_AGENT_INPUT_GUARD_END"),
            ("# TRUSTED_CLONE_SETUP_BEGIN", "# TRUSTED_CLONE_SETUP_END"),
            ('image="ara-ADAPTER-agent:', 'docker build --pull -t "$image" "$build_dir"'),
            ("# The host deliberately cloned without a checkout",
             'trusted_packed=$(base64 -w0 .git/packed-refs)'),
            ("# The model child is gone before this fixed-format file is",
             "} > .ADAPTER-attempt-telemetry"),
            ("# This fixed container tail runs after the agent child exits.",
             "# TRUSTED_COMMIT_NORMALIZATION_END"),
            ("# TRUSTED_ATTEMPT_TELEMETRY_BEGIN", "# TRUSTED_ATTEMPT_TELEMETRY_END"),
            ("# TRUSTED_IMPORT_GUARD_BEGIN", "# TRUSTED_IMPORT_GUARD_END"),
        )

        def block(text: str, begin: str, end: str) -> str:
            start = text.index(begin)
            return text[start:text.index(end, start) + len(end)]

        for begin, end in spans:
            with self.subTest(begin=begin):
                expected = block(cursor, begin, end)
                if begin.startswith("image="):
                    # The build context carries the path guard, not birdy-fast.
                    expected = expected.replace(
                        'cp "$GITHUB_ACTION_PATH/birdy-fast" "$build_dir/birdy-fast"',
                        'cp "$GITHUB_ACTION_PATH/tool-guard.mjs" "$build_dir/tool-guard.mjs"')
                self.assertEqual(expected, block(claude, begin, end))
        # OpenCode shares every span but its attempt telemetry, and its
        # CONTAINER_RUN block is Cursor's; Claude's adds the token pipe.
        opencode = normalize(shell("run-opencode-container").replace("OpenCode", "opencode"),
                             "opencode")
        for begin, end in spans + (("# CONTAINER_RUN_BEGIN", "# CONTAINER_RUN_END"),):
            if begin == "# TRUSTED_ATTEMPT_TELEMETRY_BEGIN":
                continue
            with self.subTest(runner="opencode", begin=begin):
                self.assertEqual(block(cursor, begin, end), block(opencode, begin, end))
        # pi shares every span but two. Its image block names the image and
        # container with a random suffix and builds no birdy-fast, so only its
        # name check and background build are compared; it takes no inline
        # prompt or return artifacts, so its mode checks end at the allowed
        # paths. It adds the twitter-only checks, mounts, and attempt
        # telemetry that the Claude runner does not use.
        pi = re.sub(r"\bpi\b", "ADAPTER", shell("run-pi-container"))
        pi_spans = tuple(span for span in spans
                         if not span[0].startswith(("image=", "if { [")))
        pi_spans += (
            ('if [ "$RUN_MODE" = "twitter" ] && [ -z "$ALLOWED_PATHS" ]',
             'twitter mode requires allowed-paths."'),
            ('if [ -n "$BIRDY_TOOL_LOG_REL" ]; then',
             'birdy-tool-log-path cannot traverse directories."'),
            ('if { [ "$RUN_MODE" = "twitter" ]', 'allowed-paths must contain 1-8 paths."'),
            ("# TRUSTED_BIRD_MOUNT_GUARD_BEGIN", "# TRUSTED_BIRD_MOUNT_GUARD_END"),
            ('case "$container_name" in', 'container name exceeds 120 characters."'),
            ("# Bash runs a trap only after a foreground command exits, so build in",
             'build_job=""'),
            ("extra_args=()", 'BIRDY_TOOL_LOG_PATH=/workspace/${BIRDY_TOOL_LOG_REL#/}")'),
            ("# CONTAINER_RUN_BEGIN", "# CONTAINER_RUN_END"),
        )
        for begin, end in pi_spans:
            with self.subTest(runner="pi", begin=begin):
                self.assertEqual(block(cursor, begin, end), block(pi, begin, end))
        # The wiki lane's uv is the Cursor image's pinned copy, with the same
        # copy-mode install; only its Python moves off the noexec /tmp.
        def lines_with(text: str, needle: str) -> list[str]:
            return [line.strip() for line in text.splitlines() if needle in line]
        self.assertEqual(lines_with(cursor, "COPY --from=ghcr.io/astral-sh/uv:"),
                         lines_with(claude, "COPY --from=ghcr.io/astral-sh/uv:"))
        self.assertEqual(1, len(lines_with(claude, "COPY --from=ghcr.io/astral-sh/uv:")))
        self.assertEqual(lines_with(cursor, "--env UV_LINK_MODE="),
                         lines_with(claude, "--env UV_LINK_MODE="))

    @staticmethod
    def claude_action_shell() -> str:
        action_path = REPO_ROOT / ".github/actions/run-claude-container/action.yml"
        return "\n".join(st.get("run") or "" for st in
                         yaml.safe_load(action_path.read_text(encoding="utf-8"))["runs"]["steps"])

    def test_claude_result_summary_fails_closed_and_never_prints_the_reply(self):
        shell = self.claude_action_shell()
        block = shell.split("# TRUSTED_RESULT_SUMMARY_BEGIN", 1)[1].split(
            "# TRUSTED_RESULT_SUMMARY_END", 1)[0]
        reply = "INBOX-QUOTE-THAT-MUST-NOT-BE-LOGGED"
        good = {"type": "result", "subtype": "success", "is_error": False, "num_turns": 2,
                "result": reply, "modelUsage": {"claude-sonnet-5-5": {"outputTokens": 9}},
                "permission_denials": [{"tool_name": "Write", "tool_input": {
                    "file_path": "/workspace/x", "content": "DENIED-CONTENT"}}]}

        def run(case: str, status: int, result: object = None, link: bool = False,
                oversize: bool = False, denials: str | None = None,
                link_denials: bool = False) -> tuple[int, str, str]:
            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                isolated = tmp_path / "isolated"
                build = tmp_path / "build"
                isolated.mkdir()
                build.mkdir()
                if denials is not None:
                    log = isolated / ".claude-guard-denials.tsv"
                    if link_denials:
                        (tmp_path / "elsewhere.tsv").write_text(denials, encoding="utf-8")
                        os.symlink(tmp_path / "elsewhere.tsv", log)
                    else:
                        log.write_text(denials, encoding="utf-8")
                result_file = isolated / ".claude-result.json"
                if link:
                    target = tmp_path / "elsewhere.json"
                    target.write_text(json.dumps(good), encoding="utf-8")
                    os.symlink(target, result_file)
                elif oversize:
                    result_file.write_text(" " * 1048577, encoding="utf-8")
                elif result is not None:
                    result_file.write_text(json.dumps(result), encoding="utf-8")
                output_file = tmp_path / "output.txt"
                env = os.environ.copy()
                env.update({"isolated_workspace": str(isolated), "build_dir": str(build),
                            "OUTPUT_FILE": str(output_file), "agent_status": str(status)})
                checked = subprocess.run(
                    ["bash", "-c", "set -euo pipefail\n" + block
                     + '\necho "final_status=$agent_status"'],
                    cwd=REPO_ROOT, env=env, capture_output=True, text=True, check=False)
                self.assertEqual(0, checked.returncode, (case, checked.stderr))
                final = int(checked.stdout.rsplit("final_status=", 1)[1].strip())
                written = output_file.read_text(encoding="utf-8") if output_file.exists() else ""
                return final, checked.stdout, written

        final, stdout, written = run("good", 0, good)
        self.assertEqual(0, final)
        self.assertIn("::notice title=Claude result::is_error=false", stdout)
        self.assertIn("output_tokens=claude-sonnet-5-5:9", written)
        self.assertIn("::notice title=Claude denials::Write:cli_rule=1", written)
        for leaked in (reply, "DENIED-CONTENT", "/workspace/x"):
            self.assertNotIn(leaked, stdout)
            self.assertNotIn(leaked, written)
        # The guard's reason codes reach the summary; a linked log is ignored.
        _, coded, _ = run("guard codes", 0, good, denials="Write\tpath_not_allowed\n")
        self.assertIn("::notice title=Claude denials::Write:path_not_allowed=1", coded)
        _, linked, _ = run("linked codes", 0, good, denials="Write\tpath_not_allowed\n",
                           link_denials=True)
        self.assertIn("::notice title=Claude denials::Write:cli_rule=1", linked)
        self.assertEqual(1, run("is_error on exit 0", 0, {**good, "is_error": True})[0])
        self.assertIn("reported is_error; failing closed",
                      run("is_error on exit 0", 0, {**good, "is_error": True})[1])
        self.assertEqual(1, run("missing", 0)[0])
        self.assertEqual(1, run("not json", 0, "not an object")[0])
        self.assertEqual(1, run("linked", 0, link=True)[0])
        self.assertEqual(1, run("oversize", 0, oversize=True)[0])
        # A real failure keeps its own status; nothing ever turns it green.
        self.assertEqual(124, run("timeout", 124, good)[0])
        self.assertEqual(124, run("timeout and error", 124, {**good, "is_error": True})[0])

    def test_claude_attempt_never_starts_the_model_without_live_settings(self):
        shell = self.claude_action_shell()
        block = shell.split("# CLAUDE_ATTEMPT_BEGIN", 1)[1].split("# CLAUDE_ATTEMPT_END", 1)[0]
        fake = r"""#!/usr/bin/env bash
if [ "$1" = "--init-only" ]; then
  echo "init-only $*" >> "$FAKE_LOG"
  if [ "$FAKE_INIT_MARKER" = 1 ]; then touch "$FAKE_MARKER"; fi
  exit "$FAKE_INIT_STATUS"
fi
echo "run $*" >> "$FAKE_LOG"
token=$(cat <&3)
echo "token-fd=$token token-env=${CLAUDE_CODE_OAUTH_TOKEN:-unset}" >> "$FAKE_LOG"
if [ "$FAKE_RUN_MARKER" = 1 ]; then touch "$FAKE_MARKER"; fi
echo '{"type":"result","is_error":false,"result":"RAW-REPLY-NOT-FOR-LOGS"}'
exit "$FAKE_RUN_STATUS"
"""

        def run(init_marker: int, init_status: int, run_marker: int, run_status: int):
            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                bin_dir = tmp_path / "bin"
                work = tmp_path / "work"
                bin_dir.mkdir()
                work.mkdir()
                (bin_dir / "claude").write_text(fake, encoding="utf-8")
                (bin_dir / "claude").chmod(0o755)
                (tmp_path / "claude-prompt.md").write_text("prompt\n", encoding="utf-8")
                log = tmp_path / "calls.log"
                env = os.environ.copy()
                env.pop("CLAUDE_CODE_OAUTH_TOKEN", None)
                env.update({
                    "PATH": f"{bin_dir}:{env['PATH']}", "FAKE_LOG": str(log),
                    "FAKE_MARKER": f"{tmp}/claude-liveness/session-start",
                    "FAKE_INIT_MARKER": str(init_marker), "FAKE_INIT_STATUS": str(init_status),
                    "FAKE_RUN_MARKER": str(run_marker), "FAKE_RUN_STATUS": str(run_status),
                    "CLAUDE_MODEL_REF": "claude/claude-sonnet-5-5", "AGENT_TIMEOUT_MINUTES": "1",
                    "CLAUDE_TOOLS": "Read,Write", "CLAUDE_MAX_TURNS": "4",
                    "RETURN_ARTIFACTS": ".tmp/aradio/edit.json",
                })
                script = ("set -uo pipefail\nclaude_oauth_token=TOKEN-ON-FD\n"
                          + block.replace("/tmp/", f"{tmp}/")
                          + '\necho "final_status=$agent_status"')
                checked = subprocess.run(["bash", "-c", script], cwd=work, env=env,
                                         capture_output=True, text=True, check=False)
                self.assertEqual(0, checked.returncode, checked.stderr)
                calls = log.read_text(encoding="utf-8") if log.exists() else ""
                telemetry = (work / ".claude-attempt-telemetry").read_text(encoding="utf-8")
                final = int(checked.stdout.rsplit("final_status=", 1)[1].strip())
                return final, calls, checked, telemetry

        # The settings file did not load: no marker, so the model never runs.
        final, calls, checked, telemetry = run(0, 0, 1, 0)
        self.assertEqual(1, final)
        self.assertIn("init-only --restricted", calls)
        self.assertNotIn("run ", calls)
        self.assertIn("refusing to start the model without its guard", checked.stderr)
        self.assertEqual("attempt_count=1\nlast_agent_status=1\ntranslation_segment_calls=0\n"
                         "artifact_count=0\nretry_reason=none\n", telemetry)
        final, calls, _, _ = run(1, 2, 1, 0)
        self.assertEqual(1, final)
        self.assertNotIn("run ", calls)
        # Live settings: one real turn, token on descriptor 3, never in env,
        # and the CLI's own output is never echoed.
        final, calls, checked, telemetry = run(1, 0, 1, 0)
        self.assertEqual(0, final)
        self.assertIn("token-fd=TOKEN-ON-FD token-env=unset", calls)
        self.assertIn("run -p --model claude-sonnet-5-5 --restricted --tools Read,Write", calls)
        self.assertNotIn("RAW-REPLY-NOT-FOR-LOGS", checked.stdout + checked.stderr)
        self.assertIn("last_agent_status=0\n", telemetry)
        # The real session dropped its hooks: fail closed after the fact.
        final, _, checked, _ = run(1, 0, 0, 0)
        self.assertEqual(1, final)
        self.assertIn("without its session hooks", checked.stderr)
        # A failed turn keeps its own status.
        self.assertEqual(3, run(1, 0, 1, 3)[0])

    def test_claude_container_host_script_parses_under_bash(self):
        action_path = REPO_ROOT / ".github/actions/run-claude-container/action.yml"
        run = "\n".join(st.get("run") or "" for st in
                        yaml.safe_load(action_path.read_text(encoding="utf-8"))["runs"]["steps"])
        start = run.index("bash -lc '") + len("bash -lc '")
        body = run[start:run.index("\n  ')", start)]
        self.assertNotIn("'", body, "apostrophe inside the bash -lc body")
        with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as fh:
            fh.write(run)
            script_path = fh.name
        try:
            checked = subprocess.run(["bash", "-n", script_path],
                                     capture_output=True, text=True, check=False)
        finally:
            Path(script_path).unlink(missing_ok=True)
        self.assertEqual(0, checked.returncode, checked.stderr)
        body_check = subprocess.run(["bash", "-n"], input=body, capture_output=True,
                                    text=True, check=False)
        self.assertEqual(0, body_check.returncode, body_check.stderr)

    def test_claude_isolated_canary_probes_the_model_production_runs(self):
        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        model = config["backends"][config["routes"]["aradio"]["backend"]]["model"]
        workflow_path = REPO_ROOT / ".github/workflows/claude-isolated-canary.yml"
        canary = workflow_path.read_text(encoding="utf-8")
        doc = yaml.safe_load(canary)
        steps = doc["jobs"]["canary"]["steps"]
        call = next(step for step in steps
                    if step.get("uses") == "./.github/actions/run-claude-container")
        self.assertEqual("canary", call["with"]["mode"])
        self.assertEqual(f"claude/{model}", call["with"]["model"])
        self.assertEqual(".github/claude/canary.json", call["with"]["claude-config"])
        self.assertEqual("${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}",
                         call["with"]["claude-code-oauth-token"])
        self.assertNotIn("lane", call["with"])
        self.assertIn("CLAUDE-ISOLATED-CANARY-OK", call["with"]["prompt-text"])
        check = steps[-1]["run"]
        self.assertIn("scripts/check_claude_isolated_canary.py", check)
        self.assertIn(f"--model {model}", check)
        self.assertIn("--token CLAUDE-ISOLATED-CANARY-OK", check)
        self.assertEqual({"contents": "read"}, doc["jobs"]["canary"]["permissions"])
        self.assertEqual(["self-hosted", "Linux"], doc["jobs"]["canary"]["runs-on"])
        self.assertIn(".claude-precheckout.", canary)
        checkout = next(step for step in steps
                        if str(step.get("uses", "")).startswith("actions/checkout@"))
        self.assertIs(False, checkout["with"]["persist-credentials"])
        self.assertIs(False, checkout["with"]["set-safe-directory"])
        policy = json.loads((REPO_ROOT / ".github/claude/canary.json").read_text(encoding="utf-8"))
        self.assertEqual([], policy["permissions"]["allow"])

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
            [
                "Shell(*)",
                "Write(.env*)",
                "Write(.git/**/*)",
                "Write(.github/**/*)",
                "Write(research/**/*)",
                "Write(data/**/*)",
                "Write(scripts/**/*)",
                "Write(dashboard/**/*)",
                "Write(docs/**/*)",
                "WebFetch(*)",
                "Mcp(*)",
            ],
            cursor_policy["permissions"]["deny"],
        )
        self.assertNotIn("Write(*)", cursor_policy["permissions"]["deny"])
        self.assertIn(
            "Read(.agent-input/translation-segments.json)",
            cursor_policy["permissions"]["allow"],
        )
        self.assertIn(
            "Write(.tmp/generative-translation.ko.segments.jsonl)",
            cursor_policy["permissions"]["allow"],
        )
        self.assertIn(
            "Write(.tmp/**/*)",
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

    def test_local_content_lanes_have_cross_adapter_overrides(self):
        overrides = {
            key: lane["fallback_chain"]
            for key, lane in self.lanes.items() if lane.get("fallback_chain")
        }
        self.assertEqual(
            {
                "ai-news-research": ["cursor-grok-4p6-fast"],
                "digest-audio-script": ["cursor-grok-4p6-fast"],
                "digest-synthesis-fallback": ["cursor-grok-4p6-fast"],
                "twitter-primary": ["cursor-grok-4p6-fast"],
                "twitter-primary-repair": ["cursor-grok-4p6-fast"],
            },
            overrides,
        )
        # The lane override replaces this global chain; it never appends Z.ai
        # as a third provenance hop.
        self.assertEqual(["claude", "zai-glm-5p3"], self.fallback["chain"])

        isolated_lanes = {
            "digest-audio-script",
            "digest-synthesis-fallback",
            "ai-news-research",
            "twitter-primary",
            "twitter-primary-repair",
        }
        local_steps = [
            step for obs in self.obs.values() for step in obs.agent_run
            if step.lane in isolated_lanes
        ]
        self.assertEqual(isolated_lanes, {step.lane for step in local_steps})
        self.assertTrue(all(
            step.secrets["cursor-api-key"] == "CURSOR_API_KEY"
            for step in local_steps
        ))
        other_steps = [
            step for obs in self.obs.values() for step in obs.agent_run
            if step.lane not in isolated_lanes
        ]
        self.assertTrue(all(not step.secrets.get("cursor-api-key")
                            for step in other_steps))
        modes = {step.lane: step.cursor_mode for step in local_steps}
        self.assertEqual(
            {
                "ai-news-research": "editorial",
                "digest-audio-script": "editorial",
                "digest-synthesis-fallback": "editorial",
                "twitter-primary": "twitter",
                "twitter-primary-repair": "twitter",
            },
            modes,
        )

    def test_agent_run_scopes_isolated_adapter_child_contracts(self):
        action = yaml.safe_load(
            (REPO_ROOT / ".github/actions/agent-run/action.yml").read_text()
        )
        steps = action["runs"]["steps"]
        opencode = next(
            step for step in steps
            if step.get("uses") == "./.github/actions/run-opencode-container"
        )
        self.assertEqual("steps.select.outputs.adapter == 'opencode'",
                         opencode.get("if"))
        self.assertEqual("editorial", action["inputs"]["opencode-mode"]["default"])
        self.assertEqual("${{ inputs.opencode-mode }}", opencode["with"]["mode"])

        cursor = next(
            step for step in steps
            if step.get("uses") == "./.github/actions/run-cursor-container"
        )
        self.assertEqual("steps.select.outputs.adapter == 'cursor'", cursor.get("if"))
        self.assertEqual("editorial", action["inputs"]["cursor-mode"]["default"])
        self.assertEqual("${{ inputs.cursor-mode }}", cursor["with"]["mode"])
        self.assertEqual("${{ inputs.cursor-api-key }}",
                         cursor["with"]["cursor-api-key"])

        for child in (opencode, cursor):
            self.assertEqual("${{ inputs.prompt }}", child["with"]["prompt-text"])
            self.assertEqual("${{ steps.isolated-contract.outputs.paths }}",
                             child["with"]["allowed-paths"])
            rendered = json.dumps(child, sort_keys=True)
            for secret_input in ("claude-code-oauth-token", "fireworks-api-key",
                                 "zai-api-key"):
                self.assertNotIn(secret_input, rendered)
        self.assertNotIn("cursor-api-key", json.dumps(opencode, sort_keys=True))
        self.assertNotIn("opencode-api-key", json.dumps(cursor, sort_keys=True))

        execution_output = action["outputs"]["execution-file"]["value"]
        self.assertNotIn("run-opencode", execution_output)
        self.assertNotIn("run-cursor", execution_output)

    def test_agent_run_post_agent_dead_start_fallback_contract(self):
        """The 2026-08-30..09-06 incident fix: 429 no longer reroutes at the
        probe, so a REAL throttle must be caught after the Claude step and
        re-walk the same chain. Four invariants keep that from becoming a
        swallow or a secret leak; preserve them if you edit agent-run."""
        action = yaml.safe_load(
            (REPO_ROOT / ".github/actions/agent-run/action.yml").read_text()
        )
        steps = action["runs"]["steps"]
        by_id = {step.get("id"): step for step in steps if step.get("id")}

        # (1) Both Claude steps are continue-on-error, else the classifier
        # never runs; and the classifier re-raises anything but a dead-start.
        for step_id in ("run-claude", "run-claude-bots"):
            self.assertIs(True, by_id[step_id].get("continue-on-error"), step_id)
        outcome = by_id["claude-outcome"]
        self.assertEqual("steps.select.outputs.provider == 'claude'", outcome["if"])
        self.assertIn("classify_claude_execution.py", outcome["run"])
        self.assertIn('if [ "$outcome" = "dead-start" ]', outcome["run"])
        self.assertIn("exit 1", outcome["run"],
                      "a non-dead-start Claude failure must stay red")

        # (2) Reselection is the SAME selector with claude excluded — same
        # lane/global chain, strictness and eligibility rules — and it
        # only fires on a dead-start.
        reselect = by_id["reselect"]
        self.assertEqual("steps.claude-outcome.outputs.dead-start == 'true'",
                         reselect["if"])
        self.assertIn("select_backend.py", reselect["run"])
        self.assertIn("--exclude-backend claude", reselect["run"])
        self.assertEqual("${{ inputs.fireworks-fallback }}",
                         reselect["env"]["FALLBACK_POLICY"])

        # (3) Fallback children are keyed on the RESELECT outputs and carry
        # the same secret scoping as the primary isolated children.
        opencode = by_id["run-opencode-fallback"]
        cursor = by_id["run-cursor-fallback"]
        self.assertEqual("./.github/actions/run-opencode-container", opencode["uses"])
        self.assertEqual("./.github/actions/run-cursor-container", cursor["uses"])
        self.assertEqual("steps.reselect.outputs.adapter == 'opencode'", opencode["if"])
        self.assertEqual("steps.reselect.outputs.adapter == 'cursor'", cursor["if"])
        for child in (opencode, cursor):
            self.assertEqual("${{ inputs.prompt }}", child["with"]["prompt-text"])
            self.assertEqual("${{ steps.isolated-contract-fallback.outputs.paths }}",
                             child["with"]["allowed-paths"])
            self.assertIn("steps.reselect.outputs.model-id", child["with"]["model"])
            rendered = json.dumps(child, sort_keys=True)
            for secret_input in ("claude-code-oauth-token", "fireworks-api-key",
                                 "zai-api-key"):
                self.assertNotIn(secret_input, rendered)
        self.assertNotIn("cursor-api-key", json.dumps(opencode, sort_keys=True))
        self.assertNotIn("opencode-api-key", json.dumps(cursor, sort_keys=True))
        for step_id in ("run-zai-fallback", "run-zai-fallback-bots"):
            zai = by_id[step_id]
            self.assertIn("steps.reselect.outputs.provider == 'zai'", zai["if"])
            self.assertEqual("${{ steps.reselect.outputs.model-id }}",
                             zai["env"]["ANTHROPIC_MODEL"])

        # (4) Outputs report the EFFECTIVE backend after reselection, and the
        # execution-file output still never points at an isolated child.
        outputs = action["outputs"]
        for key in ("effective-backend", "used-fallback", "model-id"):
            self.assertIn("steps.reselect.outputs", outputs[key]["value"], key)
        self.assertIn("claude-dead-start", outputs)
        execution_output = outputs["execution-file"]["value"]
        self.assertIn("run-zai-fallback", execution_output)
        self.assertNotIn("run-opencode", execution_output)
        self.assertNotIn("run-cursor", execution_output)
        # After a dead-start the failed Claude transcript still exists; when an
        # ISOLATED adapter then served the run the output must be empty, not
        # that stale path (review finding on PR #3698). The guard must precede
        # the step chain so the whole `||` chain is short-circuited to ''.
        guard = ("steps.reselect.outputs.adapter != 'opencode' && "
                 "steps.reselect.outputs.adapter != 'cursor' && (")
        self.assertTrue(execution_output.strip().startswith("${{ " + guard),
                        execution_output)
        self.assertTrue(execution_output.rstrip().endswith(") || '' }}"), execution_output)

    def test_twitter_native_model_dispatch_input_reaches_agent_run(self):
        """hourly-twitter's `native_model` input is the one-off model switch
        (e.g. claude-fable-5-1). It must reach BOTH twitter-primary agent-run
        calls, be validated, and be rejected off the Claude tier."""
        workflow_path = REPO_ROOT / ".github/workflows/hourly-twitter.yml"
        text = workflow_path.read_text()
        workflow = yaml.safe_load(text)
        inputs = workflow[True]["workflow_dispatch"]["inputs"]
        self.assertEqual("", inputs["native_model"]["default"])
        self.assertEqual("string", inputs["native_model"]["type"])
        job = next(iter(workflow["jobs"].values()))
        agent_runs = [step for step in job["steps"]
                      if step.get("uses") == "./.github/actions/agent-run"
                      and str((step.get("with") or {}).get("lane", "")).startswith("twitter-primary")]
        self.assertEqual(2, len(agent_runs))
        for step in agent_runs:
            self.assertEqual("${{ steps.backend.outputs.native_model }}",
                             step["with"]["native-model"], step["with"]["lane"])
        resolve = next(step for step in job["steps"] if step.get("id") == "backend")
        self.assertIn('[ "$BACKEND" != "claude" ]', resolve["run"])
        self.assertIn("^claude-[a-z0-9][a-z0-9.-]*$", resolve["run"])
        self.assertIn('echo "native_model=${NATIVE_MODEL}"', resolve["run"])

    def test_ai_news_mcp_cannot_select_cursor(self):
        mcp = self.lanes["ai-news-research-mcp"]
        self.assertEqual("claude-code-action", mcp["harness"])
        self.assertTrue(mcp["strict"])
        self.assertNotIn("fallback_chain", mcp)
        workflow = yaml.safe_load(
            (REPO_ROOT / ".github/workflows/ai-news-research.yml").read_text()
        )
        steps = workflow["jobs"]["ai-news-research"]["steps"]
        mcp_step = next(step for step in steps if step.get("name") ==
                        "Run AI News Research with Claude (with MCP)")
        self.assertIn("anthropics/claude-code-action", mcp_step["uses"])
        self.assertNotIn("cursor-api-key", mcp_step["with"])
        cursor_policy = json.loads(
            (REPO_ROOT / ".github/cursor/cli-config.json").read_text()
        )
        self.assertIn("Mcp(*)", cursor_policy["permissions"]["deny"])

        portable = next(step for step in steps if step.get("name") ==
                        "Run AI News Research with SSOT-routed agent (without MCP)")
        prompt = portable["with"]["prompt"]
        self.assertIn("scripts/research_search.py gdelt", prompt)
        self.assertIn("scripts/research_search.py arxiv", prompt)
        self.assertIn("scripts/research_search.py github", prompt)
        self.assertIn("scripts/source_cache.py get", prompt)
        self.assertIn("Do NOT call WebSearch or MCP tools", prompt)
        claude_args = portable["with"]["claude-args"]
        self.assertNotIn("WebSearch", claude_args)
        self.assertNotIn("mcp__", claude_args)
        self.assertIn("Bash(uv:*)", claude_args)

    def test_local_digest_exact_paths_and_post_recovery_scope_gate(self):
        workflow = yaml.safe_load(
            (REPO_ROOT / ".github/workflows/daily-digest.yml").read_text()
        )
        steps = workflow["jobs"]["daily-digest"]["steps"]
        local = next(step for step in steps
                     if step.get("id") == "digest-agent-local")
        dated_paths = (
            "research/digest/${{ steps.date.outputs.date }}-digest.md\n"
            "research/summaries/${{ steps.date.outputs.date }}-digest-summary.txt"
        )
        self.assertEqual(dated_paths, local["with"]["expected-paths"].strip())
        self.assertEqual(dated_paths, local["with"]["allowed-paths"].strip())

        recovery = next(step for step in steps
                        if step.get("name") == "Commit recovered agent digest output")
        self.assertIn('git add "$DIGEST_FILE" "$SUMMARY_FILE"', recovery["run"])
        self.assertNotIn("git add research/digest/ research/summaries/", recovery["run"])

        scope = next(step for step in steps
                     if step.get("uses") == "./.github/actions/require-diff-scope"
                     and step.get("name") == "Require digest diff scope")
        self.assertEqual("${{ steps.digest-output-base.outputs.sha }}",
                         scope["with"]["base-sha"])
        self.assertEqual(dated_paths, scope["with"]["allowed-paths"].strip())

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
            {"claude", "deepseek-claude-code", "zai-glm-5p3", "deepseek-pi", "fireworks-pi"},
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
        selected = resolve_generative(load_generative_config(LANES_FILE), "fable-5")
        self.assertEqual("claude-fable-5", selected.provenance_model)
        self.assertIn('ANTHROPIC_DEFAULT_OPUS_MODEL: ${{ steps.native-model.outputs.model }}', workflow)
        self.assertIn('CLAUDE_CODE_SUBAGENT_MODEL: ${{ steps.native-model.outputs.model }}', workflow)
        self.assertIn('--model ${{ steps.native-model.outputs.model }}', workflow)
        self.assertIn('--model "$GEN_MODEL"', workflow)
        # Fable gets exactly one model-action attempt: the recovery retry is
        # gated on the subscription-billed lanes only, and fable-5 is not one.
        retry_gate = ("if: contains(fromJSON('[\"claude\",\"opus-5-5\"]'), "
                      "steps.effective.outputs.backend)\n        id: claude-attempt-1")
        self.assertIn(retry_gate, workflow)
        self.assertNotIn("fable-5\"]'), steps.effective.outputs.backend)\n        id: claude-attempt-1",
                         workflow)
        self.assertIn("Verify pinned model provenance", workflow)
        self.assertIn("actual_model=$(jq -r", workflow)
        self.assertIn("python3 scripts/resolve_generative_backend.py", workflow)
        # Fable is never reachable without asking for it by name.
        self.assertNotEqual(self.lanes["generative-research-default"]["backend"], "fable-5")

    def test_gen_research_opus_5_5_is_explicit_and_provenance_checked(self):
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "generative-research.yml").read_text(encoding="utf-8")
        selected = resolve_generative(load_generative_config(LANES_FILE), "opus5")
        self.assertEqual("opus-5-5", selected.selector)
        # Served model is pinned from the single resolver output, so an
        # opus-5-5-labelled article can never be authored by Sonnet.
        self.assertEqual("claude-opus-5-5", selected.provenance_model)
        # Runs on the shared native-Claude model step, and its committed
        # index row is provenance-verified before the push.
        self.assertIn('contains(fromJSON(\'["claude","fable-5","opus-5-5"]\'), '
                      'steps.effective.outputs.backend)', workflow)
        self.assertIn("EXPECTED_MODEL: ${{ steps.backend.outputs.provenance_model }}", workflow)
        # Opus 5.5 is the SSOT default: manual dispatch with no backend input,
        # gen-research issues, and hourly-twitter's auto-research all inherit
        # it. The workflow must keep resolving that default at runtime rather
        # than hard-coding a backend of its own.
        self.assertEqual(self.lanes["generative-research-default"]["backend"],
                         "claude-opus-5-5")
        self.assertIn("generative-research-default",
                      self.obs["generative-research.yml"].resolver_lanes)
        # The Fireworks-unavailable fallback is deliberately NOT the default:
        # a fallback target should be the cheap reliable path.
        self.assertIn('backend="claude"', (REPO_ROOT / ".github" / "workflows" /
                      "generative-research.yml").read_text(encoding="utf-8"))

    def test_gen_research_default_backend_normalizes_for_every_trigger(self):
        workflow_path = REPO_ROOT / ".github" / "workflows" / "generative-research.yml"
        workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        steps = workflow["jobs"]["generative-research"]["steps"]
        derive_script = next(step["run"] for step in steps
                             if step.get("name") == "Derive parameters")

        base_env = {
            "INPUT_TOPIC": "Uniswap CCA",
            "INPUT_TWITTER_URL": "",
            "INPUT_SLUG": "",
            "INPUT_BACKEND": "default",
            "INPUT_TAGS": "",
            "ISSUE_TITLE": "Uniswap CCA",
            "ISSUE_BODY": "",
        }
        cases = (
            ("workflow_dispatch", ""),
            ("issues", "backend: default"),
        )
        for event_name, issue_body in cases:
            with self.subTest(event_name=event_name), tempfile.NamedTemporaryFile() as output:
                env = os.environ.copy()
                env.update(base_env)
                env.update({
                    "EVENT_NAME": event_name,
                    "ISSUE_BODY": issue_body,
                    "GITHUB_OUTPUT": output.name,
                })
                result = subprocess.run(
                    ["bash", "-c", derive_script],
                    cwd=REPO_ROOT,
                    env=env,
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                output.seek(0)
                expected = "backend=default" if event_name == "workflow_dispatch" else "backend=default"
                self.assertIn(expected, output.read().decode("utf-8"))
        self.assertEqual(
            "opus-5-5",
            resolve_generative(load_generative_config(LANES_FILE), "default").selector,
        )

    def test_gen_research_opencode_deepseek_is_explicit_and_fail_closed(self):
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "generative-research.yml").read_text(encoding="utf-8")
        selected = resolve_generative(load_generative_config(LANES_FILE), "opencode")
        self.assertEqual("opencode-deepseek-v4-flash", selected.selector)
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
        # ATTRIBUTION COUPLING: the selected bare model id is passed into both
        # writer call sites; it is never hard-coded to the first OpenCode model.
        prompt = (REPO_ROOT / ".github" / "opencode" / "prompts" /
                  "generative-research.md").read_text(encoding="utf-8")
        self.assertEqual(['"$GEN_MODEL"', '"$GEN_MODEL"'],
                         re.findall(r"--model (\S+)", prompt))
        self.assertIn("gen-model: ${{ steps.backend.outputs.provenance_model }}", workflow)
        self.assertIn("steps.backend.outputs.adapter == 'opencode'", workflow)
        self.assertIn("EXPECTED_MODEL: ${{ steps.backend.outputs.provenance_model }}", workflow)
        self.assertIn('if [ "$actual_model" != "$EXPECTED_MODEL" ]; then', workflow)
        self.assertIn('git reset --hard "$PRE_SHA"', workflow)
        self.assertIn('git clean -fd -- research/generative', workflow)
        # The scanner must see both opencode call sites (research + canary),
        # which drive the matrix rows and the README diagram edge.
        self.assertTrue(self.obs["generative-research.yml"].opencode)
        self.assertEqual(self.obs["generative-research.yml"].opencode_token,
                         "OPENCODE_API_KEY")
        self.assertTrue(self.obs["opencode-deepseek-canary.yml"].opencode)

    def test_gen_research_opencode_muse_is_explicit_provenance_correct_and_opt_in(self):
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "generative-research.yml").read_text(encoding="utf-8")
        selected = resolve_generative(load_generative_config(LANES_FILE), "muse-1.3")
        self.assertEqual("opencode-go/muse-spark-1.3-contributor", selected.model_ref)
        self.assertEqual("openai-responses", selected.protocol)
        self.assertIn("openai-responses)", workflow)
        self.assertIn("max_output_tokens:128", workflow)
        self.assertNotEqual(
            self.lanes["generative-research-default"]["backend"],
            "opencode-muse-spark-1p3-contributor",
        )
        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        profile = config["backends"]["opencode-muse-spark-1p3-contributor"]
        self.assertEqual("opencode-go", profile["provider"])
        self.assertEqual("muse-spark-1.3-contributor", profile["model"])
        self.assertIn("muse-spark-1.3", profile["aliases"])
        self.assertFalse(profile["production_eligible"])
        self.assertTrue(profile["restrictions"]["requires_workspace_contributor_consent"])

    def test_gen_research_cursor_is_explicit_and_fail_closed(self):
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "generative-research.yml").read_text(encoding="utf-8")
        selected = resolve_generative(load_generative_config(LANES_FILE), "composer-2.5")
        self.assertEqual("cursor-grok-4p6-fast", selected.selector)
        self.assertIn("Resolve and preflight Cursor CLI route", workflow)
        self.assertIn("Fail Cursor run without article", workflow)
        self.assertIn("uses: ./.github/actions/run-cursor-container", workflow)
        self.assertIn("model: ${{ steps.backend.outputs.model_ref }}", workflow)
        self.assertIn("gen-model: ${{ steps.backend.outputs.provenance_model }}", workflow)
        model_id = selected.provenance_model
        prompt = (REPO_ROOT / ".github" / "cursor" / "prompts" /
                  "generative-research.md").read_text(encoding="utf-8")
        self.assertEqual(['"$GEN_MODEL"', '"$GEN_MODEL"'], re.findall(r"--model (\S+)", prompt))
        action = (REPO_ROOT / ".github" / "actions" / "run-cursor-container" /
                  "action.yml").read_text(encoding="utf-8")
        self.assertIn("GEN_MODEL: ${{ inputs.gen-model }}", action)
        self.assertIn("--env GEN_MODEL", action)
        self.assertTrue(self.obs["generative-research.yml"].cursor)
        self.assertEqual(self.obs["generative-research.yml"].cursor_token,
                         "CURSOR_API_KEY")
        self.assertTrue(self.obs["cursor-cli-canary.yml"].cursor)
        self.assertNotEqual(self.lanes["generative-research-default"]["backend"],
                            "cursor-grok-4p6-fast")

    # Every workflow that can run the opencode harness. hourly-twitter is the
    # one most easily forgotten in a model swap — it resolves its own model in
    # its own step rather than sharing gen-research's preflight.
    OPENCODE_WORKFLOWS = (
        "2h-bluesky.yml",
        "4h-community.yml",
        "aradio.yml",
        "daily-arxiv.yml",
        "generative-research.yml",
        "hourly-rss.yml",
        "hourly-twitter.yml",
        "opencode-deepseek-canary.yml",
        "translate-generative-research.yml",
        "wiki-ingest.yml",
    )

    def direct_opencode_models(self) -> dict[str, set[str]]:
        """Return literal OpenCode model refs by direct-caller workflow.

        Parses `run:` shell and skips comment lines. A whole-file substring
        scan cannot tell live routing from a REVERT marker that quotes the old
        assignment — it already false-positived on one. Multiple explicit
        models are valid; every discovered ref must still use opencode-go.
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
        for name, found in seen.items():
            if name == "generative-research.yml":
                found.update(
                    profile.model_ref for profile in generative_profiles(self.profiles, "opencode")
                )
            self.assertTrue(found, f"{name} has no inspectable OpenCode model")
            self.assertTrue(all(ref.startswith("opencode-go/") for ref in found),
                            f"unexpected OpenCode provider in {name}: {found}")
        return seen

    CURSOR_WORKFLOWS = (
        "cursor-cli-canary.yml",
        "generative-research.yml",
        "hourly-twitter.yml",
    )

    def assert_single_cursor_model(self) -> str:
        """Legacy production/canary callers pin one model; generative is a registry."""
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
        generative_models = {
            profile.model_id for profile in generative_profiles(self.profiles, "cursor")
        }
        legacy = {name: found for name, found in seen.items()
                  if name != "generative-research.yml"}
        union = set().union(*legacy.values()) if legacy else set()
        self.assertEqual(
            1, len(union),
            f"Cursor production/canary workflows must route to one model; found {legacy}")
        model_id = union.pop()
        for name, found in legacy.items():
            self.assertEqual({model_id}, found,
                             f"{name} does not route to {model_id}")
        self.assertTrue(generative_models, "generative registry has no Cursor model")
        self.assertIn(model_id, generative_models,
                      "production Cursor model is not exposed in the generative registry")
        return model_id

    def test_generative_cursor_registry_allows_multiple_models(self):
        profiles = copy.deepcopy(self.profiles)
        profiles["cursor-future"] = Profile(
            normalized="cursor-future",
            adapter="cursor",
            provider="cursor",
            model_id="future-model",
            display_name="Future Cursor model",
            selectors=["cursor-future"],
            production_eligible=False,
            generative_selector="cursor-future",
            provenance_model="future-model",
            protocol="cursor-cli",
            preflight_path="harness",
        )
        original = self.profiles
        self.profiles = profiles
        try:
            self.assertEqual("cursor-grok-4.6-high-fast", self.assert_single_cursor_model())
        finally:
            self.profiles = original

    def test_all_opencode_callers_disable_checkout_credentials(self):
        """Every known caller removes checkout auth before metadata cleanup."""
        self.assertEqual(
            {"2h-bluesky.yml", "4h-community.yml", "aradio.yml", "daily-arxiv.yml",
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

    def test_opencode_canary_covers_direct_deepseek_and_registered_editorial_glm(self):
        # The raw + first harness probes cover the direct DeepSeek comparison
        # paths. The second harness probe resolves the registered editorial
        # profile independently, so it remains a useful reversion signal while
        # the production editorial route temporarily points to Cursor.
        models = self.direct_opencode_models()
        canary = (REPO_ROOT / ".github" / "workflows" /
                  "opencode-deepseek-canary.yml").read_text(encoding="utf-8")
        gen = (REPO_ROOT / ".github" / "workflows" /
               "generative-research.yml").read_text(encoding="utf-8")
        # The RAW API probes bill the bare id; they must match the harness id
        # or the cheap preflight certifies an entitlement the run never uses.
        self.assertIn('"model": "deepseek-v4-flash"', canary)
        self.assertIn("MODEL_ID: ${{ steps.backend.outputs.model }}", gen)
        self.assertIn("--arg model \"$MODEL_ID\"", gen)
        self.assertIn('"opencode-glm-5p3-flash"', canary)
        self.assertIn('model: ${{ steps.glm_route.outputs.model_ref }}', canary)
        config = json.loads(LANES_FILE.read_text(encoding="utf-8"))
        profile = config["backends"]["opencode-glm-5p3-flash"]
        self.assertEqual("opencode", profile["adapter"])
        self.assertEqual("opencode-go", profile["provider"])
        self.assertEqual("glm-5.3-flash", profile["model"])
        muse = config["backends"]["opencode-muse-spark-1p3-contributor"]
        self.assertEqual("opencode", muse["adapter"])
        self.assertEqual("opencode-go", muse["provider"])
        self.assertEqual("muse-spark-1.3-contributor", muse["model"])
        self.assertIn("opencode-go/muse-spark-1.3-contributor",
                      models["generative-research.yml"])
        self.assertIn("opencode-go/muse-spark-1.3-contributor",
                      models["opencode-deepseek-canary.yml"])
        self.assertIn("test_muse:", canary)
        self.assertIn("if: inputs.test_muse == true", canary)
        self.assertGreaterEqual(canary.count("if: inputs.test_muse != true"), 4)
        self.assertIn("Probe Meta Muse Spark Responses API eligibility", canary)
        self.assertIn("https://opencode.ai/zen/go/v1/responses", canary)
        self.assertIn('"model":"muse-spark-1.3-contributor"', canary)
        self.assertIn("Check OpenCode workspace Contributor consent and Meta regional availability", canary)
        # The production config deliberately carries no static model/default:
        # every action call is authoritative through `opencode run -m`, so a
        # newly registered SSOT profile does not require a config edit.
        production = json.loads((REPO_ROOT / ".github" / "opencode" / "opencode.json")
                                .read_text(encoding="utf-8"))
        self.assertNotIn("model", production)
        self.assertNotIn("provider", production)
        for name in ("opencode.json", "opencode-canary.json", "translation.json",
                     "aradio.json"):
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
        model_id = "deepseek-v4-flash"
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
        # Nothing in the attempt log is streamed. The old `tail --pid` usually
        # lost its race with the redirect that creates the log, and when it
        # won it streamed raw model and provider text.
        self.assertNotIn("tail -n +1 -f", action)
        self.assertNotIn("tail_pid", action)
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
        # The CLI's own output never reaches the public log: in text mode the
        # attempt log is the model reply or the CLI error. It is only created,
        # written by the one CLI call, grepped by the fixed fatal and segment
        # patterns, and copied (capped) for the host's typed summary.
        self.assertNotIn('cat -- "$attempt_log"', action)
        self.assertNotIn("tail -n +1 -f", action)
        self.assertNotIn("tail_pid", action)
        self.assertEqual([
            'attempt_log="/tmp/cursor-attempt-${attempt_count}.log"',
            'rm -f -- "$attempt_log"',
            '"$(cat /tmp/cursor-prompt.md)" > "$attempt_log" 2>&1 &',
            '"$(cat /tmp/cursor-prompt.md)" > "$attempt_log" 2>&1 &',
            'fatal=$(grep -m1 -oiE "$cursor_fatal_pattern" "$attempt_log" 2>/dev/null \\',
            'segment_calls=$(grep -cF "translation_segment {" "$attempt_log" || true)',
            'if [ -f "${attempt_log:-}" ] && [ ! -L "${attempt_log:-}" ]; then',
            'head -c 1048576 -- "$attempt_log" > .cursor-result.txt || true',
        ], [line.strip() for line in action.splitlines() if "attempt_log" in line])
        self.assertIn("/usr/bin/python3 -I scripts/summarize_cursor_result.py", action)
        self.assertIn("HOME=/tmp/cursor-home", action)
        self.assertIn('--sandbox disabled', action)
        self.assertIn('timeout "${remaining_seconds}s" agent -p --force --trust', action)
        self.assertIn('timeout "${remaining_seconds}s" agent -p --mode ask --trust', action)
        self.assertIn("git bundle create .cursor-export.bundle", action)
        self.assertIn("Cursor attempt telemetry is malformed", action)
        self.assertIn("https://downloads.cursor.com/lab/", action)
        self.assertIn("sha256sum -c -", action)
        self.assertNotIn("curl https://cursor.com/install", action)
        self.assertIn("agent --version", action)
        # The published `agent` name is a wrapper around its package payload.
        # Installing only the wrapper regresses to MODULE_NOT_FOUND index.js.
        self.assertIn("/opt/cursor-agent", action)
        self.assertIn("test -f /opt/cursor-agent/index.js", action)
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
        # The adapter never logs the reply, so the token is proven from the
        # typed summary it appends to the output file, not by grepping text.
        steps = yaml.safe_load(canary)["jobs"]["canary"]["steps"]
        call = next(step for step in steps
                    if step.get("uses") == "./.github/actions/run-cursor-container")
        self.assertEqual("canary", call["with"]["mode"])
        self.assertIn("CURSOR-CLI-CANARY-OK", call["with"]["prompt-text"])
        self.assertEqual("${{ runner.temp }}/cursor-cli-canary.out", call["with"]["output-file"])
        self.assertLess(steps.index(call), len(steps) - 1)
        check = steps[-1]["run"]
        self.assertIn("python3 scripts/check_cursor_canary.py", check)
        self.assertIn('"${RUNNER_TEMP:-/tmp}/cursor-cli-canary.out"', check)
        self.assertIn("--token CURSOR-CLI-CANARY-OK", check)
        self.assertNotIn("grep", check)
        self.assertIn("persist-credentials: false", canary)
        self.assertIn("set-safe-directory: false", canary)
        self.assertIn(".cursor-precheckout.", canary)
        self.assertIn("quarantine_workspace", canary)
        production = json.loads(
            (REPO_ROOT / ".github" / "cursor" / "cli-config.json")
            .read_text(encoding="utf-8"))
        self.assertNotIn("model", production)
        self.assertNotIn("provider", production)
        for name in ("cli-config.json", "cli-config-canary.json", "translation.json",
                     "aradio.json"):
            cfg = json.loads((REPO_ROOT / ".github" / "cursor" / name)
                             .read_text(encoding="utf-8"))
            self.assertEqual(1, cfg.get("version"), name)
            self.assertEqual(False, (cfg.get("editor") or {}).get("vimMode"), name)
            self.assertIn("permissions", cfg, name)
            self.assertIsInstance((cfg["permissions"]).get("allow", []), list, name)
            self.assertIsInstance((cfg["permissions"]).get("deny", []), list, name)

    @staticmethod
    def cursor_action_shell() -> str:
        action_path = REPO_ROOT / ".github/actions/run-cursor-container/action.yml"
        return "\n".join(st.get("run") or "" for st in
                         yaml.safe_load(action_path.read_text(encoding="utf-8"))["runs"]["steps"])

    @staticmethod
    def write_fakes(bin_dir: Path, **scripts: str) -> None:
        """timeout runs its command directly; sleep is short, so a poll is fast."""
        scripts = {"timeout": '#!/bin/bash\nshift\nexec "$@"\n',
                   "sleep": "#!/bin/bash\nexec /bin/sleep 0.05\n", **scripts}
        for name, body in scripts.items():
            (bin_dir / name).write_text(body, encoding="utf-8")
            (bin_dir / name).chmod(0o755)

    def test_cursor_attempt_loop_hands_the_reply_to_the_host_and_never_prints_it(self):
        shell = self.cursor_action_shell()
        loop = shell.split("# CURSOR_ATTEMPT_LOOP_BEGIN", 1)[1].split(
            "# CURSOR_ATTEMPT_LOOP_END", 1)[0]
        fake_agent = r"""#!/bin/bash
attempt=$(( $(cat "$FAKE_COUNT" 2>/dev/null || echo 0) + 1 ))
echo "$attempt" > "$FAKE_COUNT"
echo "agent $*" >> "$FAKE_LOG"
case "$FAKE_BEHAVIOR" in
  token) echo "CURSOR-CLI-CANARY-OK" ;;
  model) echo "Cannot use this model: grok-4.6-fast. Available models: auto" >&2; exit 1 ;;
  flood) yes FLOOD-REPLY | head -c 2097152 ;;
  fatal)
    echo "ActionRequiredError: Weekly usage limit reached. ::warning::INJECTED-REPLY"
    exec /bin/sleep 30 ;;
  ko-retry)
    if [ "$attempt" -eq 2 ]; then
      mkdir -p .tmp
      echo segment > .tmp/generative-translation.ko.segments.jsonl
      echo "SECOND-REPLY"
    else
      echo "FIRST-REPLY"
    fi ;;
esac
"""
        status_line = (r"Cursor attempt {n}: status={status} translation_segment_calls=0 "
                       r"artifacts={artifacts} remaining_seconds=([1-5][0-9]|60)")

        with tempfile.TemporaryDirectory() as tmp:
            bin_dir = Path(tmp) / "bin"
            bin_dir.mkdir()
            self.write_fakes(bin_dir, agent=fake_agent)

            def run_case(behavior: str, mode: str = "editorial", lane: str = "",
                         artifacts: str = "", plant: str = ""):
                case = Path(tempfile.mkdtemp(dir=tmp))
                work = case / "work"
                work.mkdir()
                (case / "cursor-prompt.md").write_text("prompt-body", encoding="utf-8")
                result = work / ".cursor-result.txt"
                if plant == "symlink":
                    (case / "outside.txt").write_text("OUTSIDE\n", encoding="utf-8")
                    result.symlink_to(case / "outside.txt")
                elif plant == "directory":
                    result.mkdir()
                    (result / "inner").write_text("x", encoding="utf-8")
                env = {**os.environ, "PATH": f"{bin_dir}:/usr/bin:/bin",
                       "FAKE_COUNT": str(case / "count"), "FAKE_LOG": str(case / "calls"),
                       "FAKE_BEHAVIOR": behavior,
                       "CURSOR_MODEL_REF": "cursor/cursor-grok-4.6-high-fast",
                       "AGENT_TIMEOUT_MINUTES": "1", "AGENT_LANE": lane, "RUN_MODE": mode,
                       "RETURN_ARTIFACTS": artifacts}
                script = ("set -uo pipefail\n" + loop.replace("/tmp/", f"{case}/")
                          + '\necho "final_status=$agent_status"')
                checked = subprocess.run(["bash", "-c", script], cwd=work, env=env,
                                         capture_output=True, text=True, timeout=60,
                                         check=False)
                self.assertEqual(0, checked.returncode, (behavior, checked.stderr))
                self.assertFalse(result.is_symlink(), behavior)
                self.assertTrue(result.is_file(), behavior)
                return (checked.stdout.splitlines(), checked.stderr, result.read_bytes(),
                        (work / ".cursor-attempt-telemetry").read_text(encoding="utf-8"),
                        (case / "calls").read_text(encoding="utf-8"), case)

            # Canary: the token reaches the host file, never the log, and the
            # read-only CLI branch is unchanged.
            stdout, stderr, result, telemetry, calls, _ = run_case("token", mode="canary")
            self.assertEqual(2, len(stdout), stdout)
            self.assertRegex(stdout[0], status_line.format(n=1, status=0, artifacts=0))
            self.assertEqual("final_status=0", stdout[1])
            self.assertNotIn("CANARY-OK", "\n".join(stdout) + stderr)
            self.assertEqual(b"CURSOR-CLI-CANARY-OK\n", result)
            self.assertEqual("attempt_count=1\nlast_agent_status=0\ntranslation_segment_calls=0\n"
                             "artifact_count=0\nretry_reason=none\n", telemetry)
            self.assertEqual("agent -p --mode ask --trust --sandbox disabled --workspace "
                             "/workspace --model cursor-grok-4.6-high-fast --output-format text "
                             "--disable-auto-update prompt-body\n", calls)
            # A link or directory the model left at the path is replaced, and
            # the link target is never written.
            for plant in ("symlink", "directory"):
                stdout, _, result, _, calls, case = run_case("token", plant=plant)
                self.assertEqual(b"CURSOR-CLI-CANARY-OK\n", result)
                self.assertIn("agent -p --force --trust", calls)
                if plant == "symlink":
                    self.assertEqual("OUTSIDE\n",
                                     (case / "outside.txt").read_text(encoding="utf-8"))
            # A CLI error keeps its status and stays out of the log.
            stdout, stderr, result, telemetry, _, _ = run_case("model")
            self.assertEqual(["final_status=1"], stdout[1:])
            self.assertRegex(stdout[0], status_line.format(n=1, status=1, artifacts=0))
            self.assertIn(b"Cannot use this model", result)
            self.assertNotIn("Cannot use", "\n".join(stdout) + stderr)
            self.assertIn("last_agent_status=1\n", telemetry)
            # A runaway reply is capped at the 1 MiB the host accepts.
            stdout, stderr, result, _, _, _ = run_case("flood")
            self.assertEqual(1048576, len(result))
            self.assertNotIn("FLOOD", "\n".join(stdout) + stderr)
            # The fatal abort records only the fixed keyword for the host, and
            # the container prints no ::error:: (the host re-announces it) and
            # never the provider text.
            stdout, stderr, result, telemetry, _, fatal_case = run_case("fatal")
            self.assertEqual(3, len(stdout), stdout)
            self.assertRegex(stdout[0], r"^Cursor CLI returned an unrecoverable error; aborting "
                             r"this attempt instead of waiting out the ([1-5][0-9]|60)s timeout\.$")
            self.assertRegex(stdout[1], status_line.format(n=1, status=143, artifacts=0))
            self.assertEqual("final_status=143", stdout[2])
            self.assertNotIn("::error::", "\n".join(stdout))
            self.assertNotIn("INJECTED", "\n".join(stdout) + stderr)
            self.assertNotIn("Weekly", "\n".join(stdout) + stderr)
            self.assertIn(b"Weekly usage limit reached", result)
            self.assertEqual("usage limit\n",
                             (fatal_case / "work" / ".cursor-fatal").read_text(encoding="utf-8"))
            self.assertIn("last_agent_status=143\n", telemetry)
            # The Korean zero-output retry is unchanged and the host gets the
            # last attempt's reply.
            stdout, stderr, result, telemetry, _, _ = run_case(
                "ko-retry", lane="generative-research-ko",
                artifacts=".tmp/generative-translation.ko.segments.jsonl")
            self.assertEqual(4, len(stdout), stdout)
            self.assertRegex(stdout[0], status_line.format(n=1, status=0, artifacts=0))
            self.assertEqual("Retrying Korean translation once after a zero-output Cursor attempt.",
                             stdout[1])
            self.assertRegex(stdout[2], status_line.format(n=2, status=0, artifacts=1))
            self.assertEqual("final_status=0", stdout[3])
            self.assertEqual(b"SECOND-REPLY\n", result)
            self.assertNotIn("REPLY", "\n".join(stdout) + stderr)
            self.assertEqual("attempt_count=2\nlast_agent_status=0\ntranslation_segment_calls=0\n"
                             "artifact_count=1\n"
                             "retry_reason=zero-artifact-zero-translation-segment\n", telemetry)

    def test_cursor_result_summary_never_prints_the_reply_or_changes_the_status(self):
        from summarize_cursor_result import MAX_RESULT_BYTES, summarize

        shell = self.cursor_action_shell()
        block = shell.split("# CURSOR_RESULT_SUMMARY_BEGIN", 1)[1].split(
            "# CURSOR_RESULT_SUMMARY_END", 1)[0]
        # Cursor-only and outside every TRUSTED_* span the Claude runner
        # copies; nothing in it may exit or set the status.
        self.assertLess(shell.index("# TRUSTED_ATTEMPT_TELEMETRY_END"),
                        shell.index("# CURSOR_RESULT_SUMMARY_BEGIN"))
        self.assertLess(shell.index("# CURSOR_RESULT_SUMMARY_END"),
                        shell.index("# TRUSTED_IMPORT_GUARD_BEGIN"))
        code = "\n".join(line for line in block.splitlines()
                         if not line.lstrip().startswith("#"))
        self.assertNotRegex(code, r"\bexit\b")
        self.assertNotRegex(code, r"\bagent_status=")
        token = b"CURSOR-CLI-CANARY-OK\n"
        hostile = b"done\r::add-mask::SECRET-VALUE\n::error::INJECTED\r\n%0A::warning::X"
        usage_limit = b"ActionRequiredError: Weekly usage limit reached. Buy credits.\n"

        def run(case: str, status: int, content: bytes = b"", kind: str = "file",
                output: str = "file", cwd: Path = REPO_ROOT) -> tuple[int, str, str]:
            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                isolated = tmp_path / "isolated"
                build = tmp_path / "build"
                isolated.mkdir()
                build.mkdir()
                result = isolated / ".cursor-result.txt"
                if kind == "file":
                    result.write_bytes(content)
                elif kind == "symlink":
                    (tmp_path / "elsewhere.txt").write_bytes(token)
                    result.symlink_to(tmp_path / "elsewhere.txt")
                elif kind == "directory":
                    result.mkdir()
                elif kind == "fifo":
                    os.mkfifo(result)
                elif kind == "unreadable":
                    result.write_bytes(token)
                    result.chmod(0)
                output_file = tmp_path / "output.txt"
                output_file.write_text("container line\n", encoding="utf-8")
                env = os.environ.copy()
                env.update({
                    "isolated_workspace": str(isolated), "build_dir": str(build),
                    "agent_status": str(status),
                    "OUTPUT_FILE": {"file": str(output_file), "none": "",
                                    "missing-dir": str(tmp_path / "nodir" / "out.txt")}[output],
                })
                # Bytes, not text mode: universal newlines would turn a
                # leaked carriage return into an innocent line break.
                checked = subprocess.run(
                    ["bash", "-c", "set -euo pipefail\n" + block
                     + '\necho "final_status=$agent_status"'],
                    cwd=cwd, env=env, capture_output=True, timeout=60, check=False)
                self.assertEqual(0, checked.returncode, (case, checked.stderr))
                stdout, _, final = checked.stdout.decode("utf-8").rpartition("final_status=")
                written = output_file.read_bytes().decode("utf-8")
                for text in (stdout, written):
                    for leaked in ("SECRET-VALUE", "INJECTED", "add-mask", "Weekly", "\r"):
                        self.assertNotIn(leaked, text, case)
                return int(final.strip()), stdout, written

        final, stdout, written = run("canary token", 0, token)
        self.assertEqual(0, final)
        self.assertEqual(summarize(0, token) + "\n", stdout)
        self.assertEqual("container line\n" + summarize(0, token) + "\n", written)
        self.assertEqual((0, summarize(0, hostile) + "\n"), run("hostile reply", 0, hostile)[:2])
        # A failure keeps its own status and gets a class, never the text.
        final, stdout, _ = run("usage limit", 1, usage_limit)
        self.assertEqual((1, summarize(1, usage_limit) + "\n"), (final, stdout))
        self.assertTrue(stdout.endswith(" cli_error=usage_limit\n"))
        self.assertEqual((124, summarize(124, b"") + "\n"), run("timeout", 124)[:2])
        self.assertEqual((0, summarize(0, b"y" * MAX_RESULT_BYTES) + "\n"),
                         run("at the cap", 0, b"y" * MAX_RESULT_BYTES)[:2])
        # Anything but a regular, unlinked file within 1 MiB is not read: the
        # summary carries placeholders, not the link target's hash.
        unread = [("symlink", b""), ("directory", b""), ("fifo", b""), ("missing", b""),
                  ("file", b"z" * (MAX_RESULT_BYTES + 1))]
        if os.geteuid() != 0:
            unread.append(("unreadable", b""))
        for kind, content in unread:
            with self.subTest(kind=kind, size=len(content)):
                self.assertEqual((0, summarize(0, None) + "\n"),
                                 run(kind, 0, content, kind=kind)[:2])
                self.assertEqual((3, summarize(3, None) + "\n"),
                                 run(kind, 3, content, kind=kind)[:2])
        # No output file: the line is still logged. A broken one, or a
        # missing summarizer, never fails the step or touches the status.
        final, stdout, written = run("no output file", 0, token, output="none")
        self.assertEqual((0, summarize(0, token) + "\n", "container line\n"),
                         (final, stdout, written))
        self.assertEqual((0, summarize(0, token) + "\n"),
                         run("unwritable output", 0, token, output="missing-dir")[:2])
        with tempfile.TemporaryDirectory() as elsewhere:
            self.assertEqual((7, ""), run("no summarizer", 7, token, cwd=Path(elsewhere))[:2])
        # The host gate holds on its own, not only through the summarizer's
        # O_NOFOLLOW: a stand-in that would read anything is never handed a
        # link, a special file, or an oversized one.
        with tempfile.TemporaryDirectory() as stand_in:
            (Path(stand_in) / "scripts").mkdir()
            (Path(stand_in) / "scripts" / "summarize_cursor_result.py").write_text(
                "import sys\nprint('ARGS', *(arg.rsplit('/', 1)[-1] for arg in sys.argv[1:]))\n",
                encoding="utf-8")
            for kind, content, handed in (
                    ("file", token, True), ("symlink", b"", False), ("directory", b"", False),
                    ("fifo", b"", False), ("file", b"z" * (MAX_RESULT_BYTES + 1), False)):
                with self.subTest(gate=kind, size=len(content)):
                    expected = "ARGS --status 0" + (
                        " --result-file .cursor-result.txt" if handed else "") + "\n"
                    self.assertEqual(expected, run(f"gate {kind}", 0, content, kind=kind,
                                                   cwd=Path(stand_in))[1])

    def test_opencode_fatal_abort_names_only_the_fixed_keyword(self):
        action_doc = yaml.safe_load(
            (REPO_ROOT / ".github/actions/run-opencode-container/action.yml")
            .read_text(encoding="utf-8"))
        run = action_doc["runs"]["steps"][0]["run"]
        loop = run.split("# OPENCODE_ATTEMPT_LOOP_BEGIN", 1)[1].split(
            "# OPENCODE_ATTEMPT_LOOP_END", 1)[0]
        fake_opencode = r"""#!/bin/bash
case "$FAKE_BEHAVIOR" in
  fatal)
    printf "%s %s\n" "ERROR service=llm level=ERROR msg=::warning::INJECTED-FREE-TEXT" \
      "sk-SECRET error=Insufficient balance"
    exec /bin/sleep 30 ;;
  prose) echo "The model wrote: level=WARN Insufficient balance is a story." ;;
esac
"""
        with tempfile.TemporaryDirectory() as tmp:
            bin_dir = Path(tmp) / "bin"
            bin_dir.mkdir()
            self.write_fakes(bin_dir, opencode=fake_opencode)

            def run_case(behavior: str) -> tuple[list[str], str]:
                case = Path(tempfile.mkdtemp(dir=tmp))
                (case / "opencode-prompt.md").write_text("prompt", encoding="utf-8")
                work = case / "work"
                work.mkdir()
                env = {**os.environ, "PATH": f"{bin_dir}:/usr/bin:/bin",
                       "FAKE_BEHAVIOR": behavior, "OPENCODE_MODEL_REF": "opencode-go/x",
                       "AGENT_TIMEOUT_MINUTES": "1", "AGENT_LANE": "", "RUN_MODE": "canary",
                       "ALLOWED_PATHS": "", "RETURN_ARTIFACTS": ""}
                script = ("set -uo pipefail\n" + loop.replace("/tmp/", f"{case}/")
                          + '\necho "final_status=$agent_status"')
                checked = subprocess.run(["bash", "-c", script], cwd=work, env=env,
                                         capture_output=True, text=True, timeout=60,
                                         check=False)
                self.assertEqual(0, checked.returncode, (behavior, checked.stderr))
                return checked.stdout.splitlines(), checked.stderr

            stdout, stderr = run_case("fatal")
            self.assertEqual(3, len(stdout), stdout)
            self.assertRegex(stdout[0], r"^::error::OpenCode provider returned an unrecoverable "
                             r"error; aborting this attempt instead of waiting out the "
                             r"([1-5][0-9]|60)s timeout: Insufficient balance$")
            self.assertRegex(stdout[1], r"^OpenCode attempt 1: status=143 ")
            self.assertEqual("final_status=143", stdout[2])
            for leaked in ("INJECTED", "SECRET", "level=ERROR", "msg="):
                self.assertNotIn(leaked, "\n".join(stdout) + stderr)
            # Detection itself is unchanged: the keyword alone, outside an
            # ERROR log line, never aborts the run.
            stdout, _ = run_case("prose")
            self.assertEqual(2, len(stdout), stdout)
            self.assertRegex(stdout[0], r"^OpenCode attempt 1: status=0 ")
            self.assertEqual("final_status=0", stdout[1])

    def test_cursor_twitter_tier_labels_name_the_served_model(self):
        model_id = self.assert_single_cursor_model()
        workflow = (REPO_ROOT / ".github" / "workflows" /
                    "hourly-twitter.yml").read_text(encoding="utf-8")
        arms = [chunk.split(";;", 1)[0]
                for chunk in workflow.split("cursor-grok-4p6-fast)")[1:]]
        arm = next(a for a in arms if "OUTPUT_DIR=" in a)
        family = model_id.split("-")[0].lower()
        if family == "cursor" and "-" in model_id:
            family = model_id.split("-", 1)[1].split("-")[0].lower()
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

    RUNNERS = ("claude", "cursor", "opencode", "pi")

    def runner_harness(self, adapter: str, root: Path, output_file: str = "") -> str:
        """The runner's real cleanup, traps and CONTAINER_RUN block, around a
        fake `docker` that runs until `docker rm -f` stops it."""
        run = yaml.safe_load((REPO_ROOT / ".github/actions" / f"run-{adapter}-container"
                              / "action.yml").read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
        setup = run[run.index('build_dir=""'):run.index("trap 'exit 130' INT")]
        block = run.split("# CONTAINER_RUN_BEGIN", 1)[1].split("# CONTAINER_RUN_END", 1)[0]
        bin_dir = root / "bin"
        bin_dir.mkdir(exist_ok=True)
        docker = bin_dir / "docker"
        docker.write_text(
            "#!/bin/bash\n"
            'log="$DOCKER_TEST_LOG"; flag="$DOCKER_TEST_LOG.stopped"\n'
            'created="$DOCKER_TEST_LOG.created"; image="$DOCKER_TEST_LOG.image"\n'
            'case "$1 $2" in\n'
            "  'run '*|'run --rm')\n"
            '    echo run >> "$log"; cat > /dev/null\n'
            '    sleep "${FAKE_CREATE_DELAY:-0}"; touch "$created"\n'
            '    for _ in $(seq 1 "${FAKE_RUN_TICKS:-600}"); do\n'
            '      [ -f "$flag" ] && exit 137; sleep 0.1\n'
            "    done\n"
            '    echo container-output; exit "${FAKE_STATUS:-0}" ;;\n'
            "  'build --pull')\n"
            "    trap 'exit 143' TERM; echo build >> \"$log\"\n"
            '    sleep "${FAKE_BUILD_SECONDS:-0}" & wait "$!"; touch "$image" ;;\n'
            "  'container inspect')\n"
            '    [ -f "$created" ] && [ ! -f "$flag" ] ;;\n'
            "  'rm -f') echo rm >> \"$log\"; touch \"$flag\" ;;\n"
            "  'image inspect') [ -f \"$image\" ] || [ -z \"${FAKE_BUILD_SECONDS:-}\" ] ;;\n"
            "  'image rm') echo image-rm >> \"$log\"; rm -f \"$image\" ;;\n"
            "  *) exit 1 ;;\n"
            "esac\n", encoding="utf-8")
        docker.chmod(0o755)
        return "\n".join([
            "set -euo pipefail", textwrap.dedent(setup), "trap 'exit 130' INT",
            'container_name="ara-test-run"', 'image="ara-test-image"',
            f'build_dir="{root}/build"', 'mkdir -p "$build_dir"',
            f'isolated_workspace="{root}/workspace"', 'mkdir -p "$isolated_workspace"',
            f'OUTPUT_FILE="{output_file}"', "CLAUDE_CODE_OAUTH_TOKEN=test-token",
            'docker_cmd=(docker run --rm -i --name "$container_name" "$image")',
            textwrap.dedent(block), 'echo "agent_status=$agent_status"',
        ])

    @staticmethod
    def kill_group(pgid: int) -> None:
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    def test_stale_adapter_image_tags_from_other_runs_are_swept_before_build(self):
        """BuildKit can tag after a cancelled client exits, so each runner
        removes its own image tags from other runs before building, keeping
        the current run+attempt (shared by sibling matrix legs)."""
        for adapter in self.RUNNERS:
            with self.subTest(adapter=adapter), tempfile.TemporaryDirectory() as tmp:
                run = yaml.safe_load((REPO_ROOT / ".github/actions" / f"run-{adapter}-container"
                                      / "action.yml").read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
                start = run.index('image_repo="${image%%:*}"')
                block = run[start:run.index("docker build --pull", start)]
                repo = f"ara-{adapter}-agent"
                root = Path(tmp)
                bindir = root / "bin"
                bindir.mkdir()
                now = datetime.datetime.now(datetime.timezone.utc)

                def created(minutes_ago: int) -> str:
                    return (now - datetime.timedelta(minutes=minutes_ago)).strftime(
                        "%Y-%m-%dT%H:%M:%S.123456789Z")

                images = {
                    f"{repo}:100-1-job-aaaa": created(900),      # sibling leg: kept
                    f"{repo}:100-1-twitter-bbbb": created(5),    # sibling leg: kept
                    f"{repo}:99-1-job-cccc": created(400),       # old other run: removed
                    f"{repo}:100-2-job-dddd": created(400),      # old other attempt: removed
                    f"{repo}:98-1-job-eeee": created(30),        # may still run elsewhere
                    f"{repo}:97-1-job-ffff": None,               # inspect fails: kept
                    f"{repo}:96-1-job-gggg": "",                 # no timestamp: kept
                }
                (root / "tags").write_text("".join(f"{ref}\n" for ref in images), encoding="utf-8")
                (root / "created").write_text(
                    "".join(f"{ref} {value}\n" for ref, value in images.items()
                            if value is not None), encoding="utf-8")
                docker = bindir / "docker"
                docker.write_text(
                    "#!/bin/bash\n"
                    'if [ "$1 $2" = "image rm" ]; then echo "$3" >> "$RMLOG"; exit 0; fi\n'
                    'if [ "$1 $2" = "image inspect" ]; then\n'
                    '  line=$(grep -F -- "${@: -1} " "$CREATED" || true)\n'
                    '  [ -n "$line" ] || exit 1\n'
                    '  printf "%s\\n" "${line#* }"; exit 0\n'
                    "fi\n"
                    'if [ "$1" = images ]; then cat "$TAGS"; exit 0; fi\n'
                    "exit 0\n", encoding="utf-8")
                docker.chmod(0o755)
                rmlog = root / "rm.log"
                script = (f'image="{repo}:100-1-twitter-zzzz"\n' + block)
                subprocess.run(["bash", "-c", "set -euo pipefail\n" + script],
                               env={**os.environ, "PATH": f"{bindir}:/usr/bin:/bin",
                                    "RMLOG": str(rmlog), "TAGS": str(root / "tags"),
                                    "CREATED": str(root / "created"),
                                    "GITHUB_RUN_ID": "100", "GITHUB_RUN_ATTEMPT": "1"},
                               check=True)
                removed = set(rmlog.read_text(encoding="utf-8").split()) if rmlog.exists() else set()
                self.assertEqual({f"{repo}:99-1-job-cccc", f"{repo}:100-2-job-dddd"}, removed)
                # Never forced: an image a container still uses is refused.
                self.assertIn('docker image rm "$stale_image"', block)
                self.assertNotIn("image rm -f", block)

    def test_stale_tag_sweep_outlasts_every_runner_job_timeout(self):
        """Another run's tag is removed only once it is older than any job
        that runs these actions can last, so a concurrent run on a runner
        sharing this Docker daemon never loses its image mid-job."""
        callers = ("run-cursor-container", "run-opencode-container", "run-claude-container",
                   "run-pi-container", "agent-dispatch", "agent-run")
        longest = 0
        for path in sorted((REPO_ROOT / ".github/workflows").glob("*.y*ml")):
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
            for job in (doc.get("jobs") or {}).values():
                if any(any(f"actions/{caller}" in str(step.get("uses") or "")
                           for caller in callers) for step in job.get("steps") or []):
                    # A job without a cap runs up to GitHub's 360-minute default.
                    longest = max(longest, int(job.get("timeout-minutes", 360)))
        self.assertGreater(longest, 0)
        for adapter in self.RUNNERS:
            with self.subTest(adapter=adapter):
                run = yaml.safe_load((REPO_ROOT / ".github/actions" / f"run-{adapter}-container"
                                      / "action.yml").read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
                minutes = int(re.search(r"^image_stale_minutes=(\d+)$", run, re.M).group(1))
                self.assertGreaterEqual(minutes, longest)

    def test_runner_names_carry_a_per_invocation_random_suffix(self):
        """Two hourly-twitter matrix legs on one runner must not share a
        container name or image tag; a random tail makes every name unique."""
        for adapter in self.RUNNERS:
            with self.subTest(adapter=adapter):
                run = yaml.safe_load((REPO_ROOT / ".github/actions" / f"run-{adapter}-container"
                                      / "action.yml").read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
                self.assertRegex(run, r'run_suffix="[^"]*\$\(od -An -N4 -tx1 /dev/urandom')
                self.assertIn(f'image="ara-{adapter}-agent:${{run_suffix}}"', run)
                self.assertIn(f'container_name="ara-{adapter}-${{run_suffix}}"', run)
                self.assertIn(f"{adapter}-container-${{run_suffix}}", run)
                self.assertIn(f"{adapter}-workspace-${{run_suffix}}", run)
                # No bare run-id names remain, which two legs of one run share.
                self.assertNotIn("${GITHUB_RUN_ID:-local}-${GITHUB_RUN_ATTEMPT:-1}\"", run)

    def test_runner_build_dir_clone_and_output_file_are_private(self):
        """Other runner accounts on this host can reach RUNNER_TEMP, and the
        container's output can hold anything it printed: the build directory
        and clone are 0700 and the output file 0600, whatever the umask."""
        for adapter in self.RUNNERS:
            with self.subTest(adapter=adapter), tempfile.TemporaryDirectory() as tmp:
                run = yaml.safe_load((REPO_ROOT / ".github/actions" / f"run-{adapter}-container"
                                      / "action.yml").read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
                start = run.index('build_dir="${RUNNER_TEMP:-/tmp}/')
                block = run[start:run.index('mkdir -m 700 -p -- "$build_dir"', start)]
                block += 'mkdir -m 700 -p -- "$build_dir"\necho "$build_dir"\n'
                made = subprocess.run(["bash", "-c", "set -euo pipefail\numask 022\n" + block],
                                      env={**os.environ, "RUNNER_TEMP": tmp, "run_suffix": "t"},
                                      capture_output=True, text=True, check=True).stdout.strip()
                self.assertEqual(0o700, os.stat(made).st_mode & 0o777)
                setup = run.split("# TRUSTED_CLONE_SETUP_BEGIN", 1)[1].split(
                    "# TRUSTED_CLONE_SETUP_END", 1)[0]
                self.assertIn('rm -rf "$isolated_workspace"\n'
                              '# The container writes into this clone; keep it private to this\n'
                              '# runner account. git clones into an existing empty directory.\n'
                              'mkdir -m 700 -- "$isolated_workspace"\n', setup)
                container_run = run.split("# CONTAINER_RUN_BEGIN", 1)[1].split(
                    "# CONTAINER_RUN_END", 1)[0]
                create = container_run.index('( umask 077 && : > "$container_out" )')
                self.assertLess(create, container_run.index('chmod 600 -- "$container_out"'))
                self.assertLess(create, container_run.index('"${docker_cmd[@]}"'))

    def test_cleanup_resumes_commands_only_after_removing_the_container(self):
        """On cancel the container is removed before workflow commands resume,
        so a model still writing to its PID 1 stdout cannot reach the log as
        the window reopens."""
        for adapter in self.RUNNERS:
            with self.subTest(adapter=adapter):
                run = yaml.safe_load((REPO_ROOT / ".github/actions" / f"run-{adapter}-container"
                                      / "action.yml").read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
                cleanup = run.split("cleanup() {", 1)[1].split("trap cleanup EXIT", 1)[0]
                remove = cleanup.index('docker rm -f "$container_name"')
                resume = cleanup.index('echo "::${stop_token}::"')
                self.assertEqual(1, cleanup.count('echo "::${stop_token}::"'))
                self.assertLess(remove, resume,
                                f"{adapter}: cleanup resumes commands before removing the container")

    def test_cancelling_a_runner_stops_its_container_at_once(self):
        """INT or TERM during the container used to wait it out (bash defers a
        trap until a foreground command exits) and lose cleanup to SIGKILL."""
        for adapter in self.RUNNERS:
            for sig, code in ((signal.SIGINT, 130), (signal.SIGTERM, 143)):
                with self.subTest(adapter=adapter, signal=sig.name), \
                        tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    log = root / "docker.log"
                    env = {**os.environ, "PATH": f"{root}/bin:/usr/bin:/bin",
                           "DOCKER_TEST_LOG": str(log)}
                    proc = subprocess.Popen(["bash", "-c", self.runner_harness(adapter, root)],
                                            env=env, stdout=subprocess.PIPE, text=True,
                                            start_new_session=True)
                    self.addCleanup(lambda pgid=proc.pid: self.kill_group(pgid))
                    deadline = time.monotonic() + 10
                    while not (log.exists() and "run" in log.read_text(encoding="utf-8")):
                        if time.monotonic() > deadline:
                            self.fail("the fake container never started")
                        time.sleep(0.05)
                    started = time.monotonic()
                    proc.send_signal(sig)
                    try:
                        stdout, _ = proc.communicate(timeout=10)
                    except subprocess.TimeoutExpired:
                        self.fail(f"{adapter} waited out its container after {sig.name}")
                    self.assertEqual(code, proc.returncode)
                    self.assertLess(time.monotonic() - started, 5)
                    self.assertEqual(["run", "rm", "image-rm"],
                                     log.read_text(encoding="utf-8").split())
                    self.assertFalse((root / "build").exists())
                    self.assertFalse((root / "workspace").exists())
                    self.assertNotIn("agent_status=", stdout)
                    stop = re.findall(r"^::stop-commands::([0-9a-f]{32})$", stdout, re.MULTILINE)
                    self.assertEqual(1, len(stop), stdout)
                    self.assertIn(f"::{stop[0]}::", stdout.splitlines())

    def test_cancelling_before_the_container_exists_still_removes_it(self):
        """The signal can land while `docker run` is still creating the
        container: cleanup keeps removing while the job lives."""
        for adapter in self.RUNNERS:
            with self.subTest(adapter=adapter), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                log = root / "docker.log"
                env = {**os.environ, "PATH": f"{root}/bin:/usr/bin:/bin",
                       "DOCKER_TEST_LOG": str(log), "FAKE_CREATE_DELAY": "2.5"}
                proc = subprocess.Popen(["bash", "-c", self.runner_harness(adapter, root)],
                                        env=env, stdout=subprocess.DEVNULL, start_new_session=True)
                self.addCleanup(lambda pgid=proc.pid: self.kill_group(pgid))
                deadline = time.monotonic() + 10
                while not (log.exists() and "run" in log.read_text(encoding="utf-8")):
                    if time.monotonic() > deadline:
                        self.fail("the fake container never started")
                    time.sleep(0.05)
                proc.send_signal(signal.SIGINT)
                self.assertEqual(130, proc.wait(timeout=12))
                self.assertEqual(["run", "rm", "image-rm"],
                                 log.read_text(encoding="utf-8").split())

    def test_cancelling_a_build_leaves_no_image(self):
        for adapter in self.RUNNERS:
            with self.subTest(adapter=adapter), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                run = yaml.safe_load((REPO_ROOT / ".github/actions" / f"run-{adapter}-container"
                                      / "action.yml").read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
                build = run[run.index("# Bash runs a trap only after a foreground command exits, so build in"):
                            run.index('build_job=""\n', run.index('wait "$build_job"'))]
                harness = self.runner_harness(adapter, root).split("\ndocker_cmd=(", 1)[0]
                script = harness + "\n" + textwrap.dedent(build) + '\nbuild_job=""\necho built\n'
                log = root / "docker.log"
                env = {**os.environ, "PATH": f"{root}/bin:/usr/bin:/bin",
                       "DOCKER_TEST_LOG": str(log), "FAKE_BUILD_SECONDS": "3"}
                proc = subprocess.Popen(["bash", "-c", script], env=env, stdout=subprocess.PIPE,
                                        text=True, start_new_session=True)
                self.addCleanup(lambda pgid=proc.pid: self.kill_group(pgid))
                deadline = time.monotonic() + 10
                while not (log.exists() and "build" in log.read_text(encoding="utf-8")):
                    if time.monotonic() > deadline:
                        self.fail("the fake build never started")
                    time.sleep(0.05)
                proc.send_signal(signal.SIGINT)
                stdout, _ = proc.communicate(timeout=10)
                self.assertEqual(130, proc.returncode)
                self.assertNotIn("built", stdout)
                time.sleep(3.5)  # past the build's own finish line
                self.assertFalse(Path(str(log) + ".image").exists(), "the build left an image")
                self.assertFalse((root / "build").exists())

    def test_opencode_host_reannounces_only_a_fixed_fatal_keyword(self):
        run = yaml.safe_load((REPO_ROOT / ".github/actions/run-opencode-container/action.yml")
                             .read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
        block = run.split("# OPENCODE_FATAL_NOTICE_BEGIN", 1)[1].split(
            "# OPENCODE_FATAL_NOTICE_END", 1)[0]
        container = re.search(r'opencode_fatal_keywords="(\([^"]+\))"', run).group(1)
        self.assertIn(f"grep -m1 -xiE '{container}'", block)

        def notice(content: str | None, link: bool = False, status: str = "1") -> str:
            with tempfile.TemporaryDirectory() as tmp:
                fatal = Path(tmp) / ".opencode-fatal"
                if link:
                    (Path(tmp) / "elsewhere").write_text(content or "", encoding="utf-8")
                    os.symlink(Path(tmp) / "elsewhere", fatal)
                elif content is not None:
                    fatal.write_text(content, encoding="utf-8")
                result = subprocess.run(["bash", "-c", "set -euo pipefail\n" + block],
                                        env={**os.environ, "isolated_workspace": tmp,
                                             "agent_status": status},
                                        capture_output=True, text=True, check=True)
                return result.stdout

        self.assertEqual("::error::OpenCode provider returned an unrecoverable error "
                         "(Invalid API key); the attempt was aborted.\n",
                         notice("Invalid API key\n"))
        for content in (None, "", "Invalid API key; ::add-mask::x\n", "::warning::x\n",
                        "usage limit reached " + "x" * 200 + "\n"):
            with self.subTest(content=content):
                self.assertEqual("", notice(content))
        self.assertEqual("", notice("Invalid API key\n", link=True))
        self.assertEqual("", notice("Invalid API key\n", status="0"))

    def test_cursor_host_reannounces_only_a_fixed_fatal_keyword(self):
        run = yaml.safe_load((REPO_ROOT / ".github/actions/run-cursor-container/action.yml")
                             .read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
        block = run.split("# CURSOR_FATAL_NOTICE_BEGIN", 1)[1].split(
            "# CURSOR_FATAL_NOTICE_END", 1)[0]
        # The host prints only the fixed keyword set the container matches.
        container = re.search(r'cursor_fatal_keywords="(\([^"]+\))"', run).group(1)
        self.assertIn(f"grep -m1 -xiE '{container}'", block)
        # The container no longer echoes the matched provider text to its
        # stdout; it records the fixed keyword in the clone for the host.
        self.assertNotIn("Cursor CLI returned an unrecoverable error; aborting this attempt "
                         "instead of waiting out the ${remaining_seconds}s timeout: ${fatal}", run)
        self.assertIn('printf "%s\\n" "$fatal" > .cursor-fatal', run)

        def notice(content: str | None, link: bool = False, status: str = "1") -> str:
            with tempfile.TemporaryDirectory() as tmp:
                fatal = Path(tmp) / ".cursor-fatal"
                if link:
                    (Path(tmp) / "elsewhere").write_text(content or "", encoding="utf-8")
                    os.symlink(Path(tmp) / "elsewhere", fatal)
                elif content is not None:
                    fatal.write_text(content, encoding="utf-8")
                return subprocess.run(["bash", "-c", "set -euo pipefail\n" + block],
                                      env={**os.environ, "isolated_workspace": tmp,
                                           "agent_status": status},
                                      capture_output=True, text=True, check=True).stdout

        self.assertEqual("::error::Cursor CLI returned an unrecoverable error "
                         "(Invalid API key); the attempt was aborted.\n",
                         notice("Invalid API key\n"))
        for content in (None, "", "Invalid API key; ::add-mask::x\n", "::warning::x\n",
                        "usage limit reached " + "x" * 200 + "\n"):
            with self.subTest(content=content):
                self.assertEqual("", notice(content))
        self.assertEqual("", notice("Invalid API key\n", link=True))
        self.assertEqual("", notice("Invalid API key\n", status="0"))

    def test_container_stdout_and_stderr_go_to_a_host_file_not_the_log(self):
        """A shell-capable model can write to its PID 1 stdout (/proc/1/fd/1),
        so the container's stdout/stderr must be redirected to a host file; the
        job log takes only the typed summary."""
        for adapter in self.RUNNERS:
            with self.subTest(adapter=adapter):
                run = yaml.safe_load((REPO_ROOT / ".github/actions" / f"run-{adapter}-container"
                                      / "action.yml").read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
                block = run.split("# CONTAINER_RUN_BEGIN", 1)[1].split("# CONTAINER_RUN_END", 1)[0]
                self.assertIn('container_out="${OUTPUT_FILE:-$build_dir/container-output.log}"', block)
                self.assertIn('"${docker_cmd[@]}" >"$container_out" 2>&1', block)
                self.assertNotIn("| tee ", block)
                self.assertNotIn('"${docker_cmd[@]}" &', block)
                # The window stays as defense in depth: one stop and one resume.
                self.assertEqual(1, block.count('echo "::stop-commands::${stop_token}"'))
                self.assertEqual(1, block.count('echo "::${stop_token}::"'))

    def test_import_guard_keeps_the_bundle_ref_listing_out_of_the_log(self):
        """`git bundle verify` lists the refs a bundle advertises: bytes the
        container wrote, printed after workflow commands resume. Keep its
        output out of the log; unbundle's ref list is already captured."""
        for adapter in self.RUNNERS:
            with self.subTest(adapter=adapter):
                run = yaml.safe_load((REPO_ROOT / ".github/actions" / f"run-{adapter}-container"
                                      / "action.yml").read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
                guard = run.split("# TRUSTED_IMPORT_GUARD_BEGIN", 1)[1].split(
                    "# TRUSTED_IMPORT_GUARD_END", 1)[0]
                calls = [line.strip() for line in guard.splitlines()
                         if "bundle verify" in line or "bundle unbundle" in line]
                self.assertEqual([
                    'if ! "${trusted_git[@]}" bundle verify "$bundle_file" >/dev/null 2>&1; then',
                    'bundle_heads=$("${trusted_git[@]}" bundle unbundle "$bundle_file")',
                ], [line for line in calls if not line.startswith("#")])

    def test_pi_runner_prints_only_a_typed_summary_and_keeps_its_status(self):
        run = yaml.safe_load((REPO_ROOT / ".github/actions/run-pi-container/action.yml")
                             .read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
        summary = run.split("# PI_RESULT_SUMMARY_BEGIN", 1)[1].split("# PI_RESULT_SUMMARY_END", 1)[0]
        # The summary prints before the telemetry and import checks can stop
        # the step, and it is the real checkout's summarizer: the container
        # mounts only the disposable clone, never that checkout.
        self.assertLess(run.index("# CONTAINER_RUN_END"), run.index("# PI_RESULT_SUMMARY_BEGIN"))
        self.assertLess(run.index("# PI_RESULT_SUMMARY_END"),
                        run.index("# TRUSTED_ATTEMPT_TELEMETRY_BEGIN"))
        self.assertIn("/usr/bin/python3 -I scripts/summarize_pi_result.py", summary)
        self.assertIn('pi_result_file="$isolated_workspace/.pi-result.txt"', summary)
        # pi's reply and errors go to the attempt log inside the container,
        # which hands the host a capped copy, never to the log.
        self.assertIn('--model "$PI_MODEL" > "$attempt_log" 2>&1', run)
        self.assertIn('head -c 1048576 -- "$attempt_log" > .pi-result.txt || true', run)
        self.assertTrue(run.rstrip().endswith('exit "$agent_status"'))
        # Credentials reach the container by name only and are never expanded
        # by the host script, so no argv or echo can carry them.
        for secret in ("AUTH_TOKEN", "CT0", "FIREWORKS_API_KEY"):
            self.assertIn(f"--env {secret} \\", run)
            self.assertNotRegex(run, rf"\${{?{secret}\b")
        self.assertIn('--name "$container_name"', run)
        self.assertIn('container_name="ara-pi-${run_suffix}"', run)
        self.assertIn('image="ara-pi-agent:${run_suffix}"', run)
        self.assertRegex(run, r'run_suffix="[^"]*\$\(od -An -N4 -tx1 /dev/urandom')

        from summarize_pi_result import reply_sha256
        hostile = "done\r::add-mask::SECRET\n::error::INJECTED\n##[warning]x\n"
        for link in (False, True):
            with self.subTest(link=link), tempfile.TemporaryDirectory() as tmp:
                workspace = Path(tmp) / "workspace"
                workspace.mkdir()
                result = workspace / ".pi-result.txt"
                if link:
                    (Path(tmp) / "elsewhere.txt").write_text(hostile, encoding="utf-8")
                    os.symlink(Path(tmp) / "elsewhere.txt", result)
                else:
                    result.write_text(hostile, encoding="utf-8")
                checked = subprocess.run(
                    ["bash", "-c", "set -euo pipefail\nagent_status=3\n"
                     f'isolated_workspace="{workspace}"\n' + summary
                     + '\necho "status=$agent_status"'],
                    cwd=REPO_ROOT, capture_output=True, text=True, check=True)
                lines = checked.stdout.splitlines()
                self.assertEqual("status=3", lines[-1])
                self.assertEqual(2, len(lines), checked.stdout)
                fields = ("reply_sha256=- reply_bytes=- reply_lines=-" if link else
                          f"reply_sha256={reply_sha256(hostile)} reply_bytes={len(hostile)} "
                          "reply_lines=3")
                self.assertEqual(f"::notice title=pi result::status=3 {fields} cli_error=other",
                                 lines[0])
                for leaked in ("SECRET", "INJECTED", "##["):
                    self.assertNotIn(leaked, checked.stdout + checked.stderr)

    def test_pi_writes_only_its_disposable_clone(self):
        """pi used to mount the real checkout read-write, so an injected model
        could edit the scripts, local actions, or .git/config that later steps
        of its job run. It now gets the Cursor runner's clone and import."""
        action = yaml.safe_load((REPO_ROOT / ".github/actions/run-pi-container/action.yml")
                                .read_text(encoding="utf-8"))
        run = action["runs"]["steps"][0]["run"]
        code = [line.strip() for line in run.splitlines()
                if line.strip() and not line.strip().startswith("#")]
        self.assertEqual(
            ['extra_args+=(--volume "/tmp/bird:/tmp/bird:ro")',
             '--volume "$isolated_workspace:/workspace" \\',
             '--volume "$PROMPT_FILE:/tmp/pi-prompt.md:ro" \\'],
            [line for line in code if "--volume" in line])
        self.assertNotIn('"$GITHUB_WORKSPACE:', run)
        # The exact container flag set: an allowlist, so an added --cap-add,
        # seccomp/apparmor override, env file, device, or host namespace fails.
        start = code.index("docker_cmd=(docker run --rm \\")
        self.assertEqual([
            '--name "$container_name" \\', '--user "$(id -u):$(id -g)" \\',
            "--workdir /workspace \\", "--cap-drop ALL \\",
            "--security-opt no-new-privileges \\", "--pids-limit 512 \\",
            "--env HOME=/tmp/pi-home \\", "--env XDG_CONFIG_HOME=/tmp/pi-home/.config \\",
            "--env FIREWORKS_API_KEY \\", "--env AUTH_TOKEN \\", "--env CT0 \\",
            "--env BIRDY_READ_ONLY=1 \\",
            '--env "GIT_AUTHOR_NAME=$GIT_USER_NAME" \\',
            '--env "GIT_AUTHOR_EMAIL=$GIT_USER_EMAIL" \\',
            '--env "GIT_COMMITTER_NAME=$GIT_USER_NAME" \\',
            '--env "GIT_COMMITTER_EMAIL=$GIT_USER_EMAIL" \\',
            "--env PI_PROVIDER \\", "--env PI_MODEL \\", "--env PI_THINKING \\",
            "--env PI_TOOLS \\", "--env RUN_MODE \\", "--env ALLOWED_PATHS \\",
            '--env "PRE_SHA=$pre_sha" \\', '${extra_args[@]+"${extra_args[@]}"} \\',
            '--volume "$isolated_workspace:/workspace" \\',
            '--volume "$PROMPT_FILE:/tmp/pi-prompt.md:ro" \\', '"$image" \\',
        ], code[start + 1:code.index("bash -lc '", start)])
        self.assertEqual(
            ['extra_args+=(--volume "/tmp/bird:/tmp/bird:ro")',
             'extra_args+=(--env "BIRDY_TOOL_LOG_PATH=/workspace/${BIRDY_TOOL_LOG_REL#/}")'],
            [line for line in code if line.startswith("extra_args+=")])
        text = "\n".join(code)
        for forbidden in ('--volume "$HOME', "seccomp", "apparmor", "systempaths",
                          "docker.sock"):
            self.assertNotIn(forbidden, text, f"container gained {forbidden}")
        for flag in ("--privileged", "--network", "--net", "--cap-add", "--env-file",
                     "--mount", "--device", "--pid", "--ipc", "--userns", "--uts",
                     "--cgroupns", "--group-add"):
            self.assertNotRegex(text, rf"(^|\s){re.escape(flag)}(\s|=|$)",
                                f"container gained {flag}")
        # The clone is made, run, and imported in this order, and the step
        # ends with the status the host observed.
        order = ["# TRUSTED_CLONE_SETUP_END", "# CONTAINER_RUN_BEGIN",
                 "# TRUSTED_ATTEMPT_TELEMETRY_BEGIN", "# TRUSTED_IMPORT_GUARD_BEGIN",
                 "# TRUSTED_IMPORT_GUARD_END"]
        self.assertEqual(sorted(run.index(marker) for marker in order),
                         [run.index(marker) for marker in order])
        self.assertIn("twitter) ;;", run)
        self.assertIn("mode must be twitter, the only pi output contract", run)
        # The container body sits inside bash -lc '...': one apostrophe ends it.
        start = run.index("bash -lc '") + len("bash -lc '")
        self.assertNotIn("'", run[start:run.index("\n  ')", start)])
        with tempfile.NamedTemporaryFile("w", suffix=".sh") as fh:
            fh.write(run)
            fh.flush()
            self.assertEqual(0, subprocess.run(["bash", "-n", fh.name]).returncode)
        # Both pi tiers declare the same output contract as the contained
        # Cursor tier of the same job.
        steps = yaml.safe_load((REPO_ROOT / ".github/workflows/hourly-twitter.yml")
                               .read_text(encoding="utf-8"))["jobs"]["twitter"]["steps"]
        cursor = next(step for step in steps if step.get("id") == "twitter-cursor-agent")["with"]
        pi_calls = [step["with"] for step in steps
                    if step.get("uses") == "./.github/actions/run-pi-container"]
        self.assertEqual(2, len(pi_calls))
        for call in pi_calls:
            with self.subTest(model=call["model"]):
                for key in ("mode", "allowed-paths", "prompt-file", "mount-bird-snapshot",
                            "birdy-tool-log-path"):
                    self.assertEqual(cursor[key], call[key], key)

    def test_pi_tiers_refuse_before_any_container_sees_a_secret(self):
        """The pi tiers would pass the X cookies and the Fireworks key into a
        prompt-injectable container. Until bird and Fireworks go through host
        proxies on an egress-restricted network, the action fails fast before
        it builds or runs any container, so no secret ever reaches one."""
        run = yaml.safe_load((REPO_ROOT / ".github/actions/run-pi-container/action.yml")
                             .read_text(encoding="utf-8"))["runs"]["steps"][0]["run"]
        refusal = run.index('Refusing to run rather than expose secrets.')
        self.assertLess(refusal, run.index("docker_cmd=(docker run"))
        for secret in ("--env FIREWORKS_API_KEY", "--env AUTH_TOKEN", "--env CT0"):
            self.assertLess(refusal, run.index(secret))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bindir = root / "bin"
            bindir.mkdir()
            docker = bindir / "docker"
            docker.write_text('#!/bin/bash\necho "$@" >> "$DOCKER_CALLS"\nexit 0\n',
                              encoding="utf-8")
            docker.chmod(0o755)
            calls = root / "calls"
            result = subprocess.run(
                ["bash", "-c", run],
                env={**os.environ, "PATH": f"{bindir}:/usr/bin:/bin",
                     "DOCKER_CALLS": str(calls), "FIREWORKS_API_KEY": "fw-SECRET",
                     "AUTH_TOKEN": "cookie-SECRET", "CT0": "ct0-SECRET",
                     "GITHUB_WORKSPACE": tmp, "RUNNER_TEMP": tmp},
                capture_output=True, text=True)
            self.assertEqual(1, result.returncode)
            self.assertIn("::error::The pi Twitter tiers are disabled", result.stdout)
            # The docker binary is never invoked, so no container, no secret.
            self.assertFalse(calls.exists(), calls.read_text() if calls.exists() else "")
            for secret in ("fw-SECRET", "cookie-SECRET", "ct0-SECRET"):
                self.assertNotIn(secret, result.stdout + result.stderr)

    def test_import_guard_keeps_the_bundle_ref_listing_out_of_the_log(self):
        """`git bundle verify` lists the refs a bundle advertises: bytes the
        container wrote, printed after workflow commands resume."""
        for adapter in self.RUNNERS:
            with self.subTest(adapter=adapter):
                run = yaml.safe_load((REPO_ROOT / ".github/actions" / f"run-{adapter}-container"
                                      / "action.yml").read_text(encoding="utf-8"))
                guard = run["runs"]["steps"][0]["run"].split(
                    "# TRUSTED_IMPORT_GUARD_BEGIN", 1)[1].split("# TRUSTED_IMPORT_GUARD_END", 1)[0]
                calls = [line.strip() for line in guard.splitlines()
                         if "bundle verify" in line or "bundle unbundle" in line]
                self.assertEqual([
                    'if ! "${trusted_git[@]}" bundle verify "$bundle_file" >/dev/null 2>&1; then',
                    'bundle_heads=$("${trusted_git[@]}" bundle unbundle "$bundle_file")',
                ], [line for line in calls if not line.startswith("#")])

    def test_a_finished_runner_container_keeps_its_status(self):
        for adapter in self.RUNNERS:
            for tee in (False, True):
                with self.subTest(adapter=adapter, tee=tee), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    output = root / "output.txt"
                    env = {**os.environ, "PATH": f"{root}/bin:/usr/bin:/bin",
                           "DOCKER_TEST_LOG": str(root / "docker.log"),
                           "FAKE_RUN_TICKS": "0", "FAKE_STATUS": "7"}
                    if tee:
                        output.write_text("stale\n", encoding="utf-8")
                        output.chmod(0o644)
                    result = subprocess.run(
                        ["bash", "-c", "umask 022\n" + self.runner_harness(
                            adapter, root, str(output) if tee else "")],
                        env=env, capture_output=True, text=True, timeout=20)
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertIn("agent_status=7", result.stdout)
                    if tee:
                        self.assertEqual("container-output\n", output.read_text(encoding="utf-8"))
                        self.assertEqual(0o600, output.stat().st_mode & 0o777)
                    lines = result.stdout.splitlines()
                    token = lines[lines.index(next(line for line in lines
                                                   if line.startswith("::stop-commands::")))]
                    self.assertIn(f"::{token.split('::')[2]}::", lines)
                    # The workflow log takes commands again before the host's own lines.
                    self.assertLess(lines.index(f"::{token.split('::')[2]}::"),
                                    lines.index("agent_status=7"))

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

    def test_editorial_zero_commit_retry_is_clean_bounded_and_fail_closed(self):
        """Commit editorials retry one clean-workspace no-op, then fail."""
        action_doc = yaml.safe_load(
            (REPO_ROOT / ".github/actions/run-opencode-container/action.yml")
            .read_text(encoding="utf-8")
        )
        run = action_doc["runs"]["steps"][0]["run"]
        self.assertEqual(2, run.count('exit "$agent_status"'))
        loop = run.split("# OPENCODE_ATTEMPT_LOOP_BEGIN", 1)[1].split(
            "# OPENCODE_ATTEMPT_LOOP_END", 1)[0]

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("curate arxiv\n", encoding="utf-8")
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
                "write_commit() {\n"
                "  mkdir -p research/arxiv\n"
                "  printf 'papers\\n' > research/arxiv/2026-08-26-papers.md\n"
                "  git add research/arxiv/2026-08-26-papers.md\n"
                "  git commit -qm 'arXiv papers'\n"
                "}\n"
                "case \"$OPENCODE_FAKE_BEHAVIOR\" in\n"
                "  retry-commit) [ \"$attempt\" -eq 2 ] && write_commit || : ;;\n"
                "  dirty-retry)\n"
                "    if [ \"$attempt\" -eq 1 ]; then\n"
                "      mkdir -p research/arxiv\n"
                "      printf 'partial\\n' > research/arxiv/2026-08-26-papers.md\n"
                "    else\n"
                "      [ ! -e research/arxiv/2026-08-26-papers.md ] || exit 97\n"
                "      write_commit\n"
                "    fi\n"
                "    ;;\n"
                "  first-commit) write_commit ;;\n"
                "  mutate-input)\n"
                "    if [ \"$attempt\" -eq 1 ]; then\n"
                "      printf 'changed\\n' > .agent-input/source.txt\n"
                "    else\n"
                "      grep -qx 'source' .agent-input/source.txt || exit 96\n"
                "      write_commit\n"
                "    fi\n"
                "    ;;\n"
                "  nonzero) exit 9 ;;\n"
                "  no-output) ;;\n"
                "  *) exit 98 ;;\n"
                "esac\n",
                encoding="utf-8")
            opencode.chmod(0o755)

            def run_case(name: str, behavior: str, *, mode: str = "editorial",
                         allowed_paths: str = (
                             "research/arxiv/2026-08-26-papers.md"),
                         return_artifacts: str = ""):
                case_dir = root / name
                case_dir.mkdir()
                subprocess.run(["git", "init", "-q"], cwd=case_dir,
                               check=True)
                subprocess.run(["git", "config", "user.name", "Test"],
                               cwd=case_dir, check=True)
                subprocess.run(["git", "config", "user.email", "test@example.com"],
                               cwd=case_dir, check=True)
                (case_dir / "seed.txt").write_text("seed\n", encoding="utf-8")
                agent_input = case_dir / ".agent-input"
                agent_input.mkdir()
                (agent_input / "source.txt").write_text(
                    "source\n", encoding="utf-8")
                subprocess.run(["git", "add", "seed.txt"], cwd=case_dir,
                               check=True)
                subprocess.run(["git", "commit", "-qm", "seed"],
                               cwd=case_dir, check=True)
                pre_sha = subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=case_dir,
                    text=True).strip()
                attempts = root / f"{name}-attempts"
                env = {
                    **os.environ,
                    "PATH": f"{bin_dir}:/usr/bin:/bin",
                    "AGENT_TIMEOUT_MINUTES": "1",
                    "AGENT_LANE": "arxiv",
                    "RUN_MODE": mode,
                    "ALLOWED_PATHS": allowed_paths,
                    "RETURN_ARTIFACTS": return_artifacts,
                    "PRE_SHA": pre_sha,
                    "OPENCODE_MODEL_REF": "opencode-go/deepseek-v4-flash",
                    "OPENCODE_ATTEMPT_FILE": str(attempts),
                    "OPENCODE_FAKE_BEHAVIOR": behavior,
                }
                result = subprocess.run(
                    ["bash", "-c", (
                        "set -euo pipefail\n" + loop
                        + '\nexit "$agent_status"\n')],
                    cwd=case_dir, env=env, text=True, capture_output=True,
                    check=False)
                telemetry = (case_dir / ".opencode-attempt-telemetry").read_text(
                    encoding="utf-8")
                count = attempts.read_text(encoding="utf-8").strip()
                return result, count, telemetry

            retried, attempts, telemetry = run_case("retry", "retry-commit")
            self.assertEqual(0, retried.returncode,
                             retried.stdout + retried.stderr)
            self.assertEqual("2", attempts)
            self.assertIn("attempt_count=2", telemetry)
            self.assertIn("last_agent_status=0", telemetry)
            self.assertIn("retry_reason=zero-commit-editorial", telemetry)

            cleaned, attempts, telemetry = run_case("clean", "dirty-retry")
            self.assertEqual(0, cleaned.returncode,
                             cleaned.stdout + cleaned.stderr)
            self.assertEqual("2", attempts)
            self.assertIn("last_agent_status=0", telemetry)

            exhausted, attempts, telemetry = run_case("exhausted", "no-output")
            self.assertEqual(86, exhausted.returncode,
                             exhausted.stdout + exhausted.stderr)
            self.assertEqual("2", attempts)
            self.assertIn("last_agent_status=86", telemetry)
            self.assertIn("retry_reason=zero-commit-editorial", telemetry)
            self.assertIn("exited successfully twice without committing output",
                          exhausted.stdout)

            committed, attempts, telemetry = run_case(
                "first-commit", "first-commit")
            self.assertEqual(0, committed.returncode,
                             committed.stdout + committed.stderr)
            self.assertEqual("1", attempts)
            self.assertIn("retry_reason=none", telemetry)

            failed, attempts, telemetry = run_case("nonzero", "nonzero")
            self.assertEqual(9, failed.returncode, failed.stdout + failed.stderr)
            self.assertEqual("1", attempts)
            self.assertIn("last_agent_status=9", telemetry)
            self.assertIn("retry_reason=none", telemetry)

            artifact_only, attempts, telemetry = run_case(
                "artifact-only", "no-output", allowed_paths="",
                return_artifacts=".tmp/bluesky-section.md")
            self.assertEqual(0, artifact_only.returncode,
                             artifact_only.stdout + artifact_only.stderr)
            self.assertEqual("1", attempts)
            self.assertIn("retry_reason=none", telemetry)

            generative, attempts, telemetry = run_case(
                "generative", "no-output", mode="generative")
            self.assertEqual(0, generative.returncode,
                             generative.stdout + generative.stderr)
            self.assertEqual("1", attempts)
            self.assertIn("retry_reason=none", telemetry)

            restored, attempts, telemetry = run_case(
                "mutated-input", "mutate-input")
            self.assertEqual(0, restored.returncode,
                             restored.stdout + restored.stderr)
            self.assertEqual("2", attempts)
            self.assertIn("last_agent_status=0", telemetry)
            self.assertIn("retry_reason=zero-commit-editorial", telemetry)

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
                "run_suffix": "hostsetup-1-job-test",
                "RUN_MODE": "canary",
                "build_dir": str(build_dir),
                "empty_git_template": str(empty_template),
                "GIT_CONFIG_GLOBAL": str(global_config),
                "GITHUB_SERVER_URL": "https://github.com",
                "GITHUB_REPOSITORY": "example/repository",
                "GITHUB_ENV": str(github_env),
            })
            result = subprocess.run(
                ["bash", "-c", "set -euo pipefail\numask 022\n" + setup],
                text=True, capture_output=True, env=env, check=False)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse(marker.exists(), result.stdout + result.stderr)
            isolated = tmp_path / "opencode-workspace-hostsetup-1-job-test"
            self.assertEqual(0o700, isolated.stat().st_mode & 0o777)
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

    def test_trusted_import_guard_never_imports_git_metadata(self):
        """Under a directory-prefix lane, a committed .git* path never crosses
        into the real checkout, in any of the three runners."""
        def run_guard(adapter: str, files: dict[str, str]) -> tuple:
            action = REPO_ROOT / ".github" / "actions" / f"run-{adapter}-container" / "action.yml"
            shell = "\n".join(st.get("run") or "" for st in
                              yaml.safe_load(action.read_text(encoding="utf-8"))["runs"]["steps"])
            guard = shell.split("# TRUSTED_IMPORT_GUARD_BEGIN", 1)[1].split(
                "# TRUSTED_IMPORT_GUARD_END", 1)[0]
            tmp = tempfile.TemporaryDirectory()
            self.addCleanup(tmp.cleanup)
            original, isolated = Path(tmp.name) / "original", Path(tmp.name) / "isolated"

            def git(repo: Path, *args: str) -> str:
                return subprocess.run(["git", "-C", str(repo), *args], text=True,
                                      capture_output=True, check=True).stdout.strip()

            (original / "research" / "wiki" / "entities").mkdir(parents=True)
            (original / "research" / "wiki" / "index.md").write_text("# Wiki\n", encoding="utf-8")
            git(original, "init", "-q", "-b", "main")
            git(original, "-c", "user.name=t", "-c", "user.email=t@example.invalid",
                "add", ".")
            git(original, "-c", "user.name=t", "-c", "user.email=t@example.invalid",
                "commit", "-q", "-m", "base")
            pre_sha = git(original, "rev-parse", "HEAD")
            subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", str(original),
                            str(isolated)], check=True)
            for name, content in files.items():
                (isolated / name).parent.mkdir(parents=True, exist_ok=True)
                (isolated / name).write_text(content, encoding="utf-8")
            git(isolated, "add", "-f", *files)
            git(isolated, "-c", "user.name=t", "-c", "user.email=t@example.invalid",
                "commit", "-q", "-m", "agent output")
            post_sha = git(isolated, "rev-parse", "HEAD")
            git(isolated, "bundle", "create", "-q", f".{adapter}-export.bundle",
                "HEAD", f"^{pre_sha}")
            (isolated / f".{adapter}-post-sha").write_text(post_sha + "\n", encoding="utf-8")
            build_dir = Path(tmp.name) / "build"
            build_dir.mkdir()
            env = {**os.environ, "GITHUB_WORKSPACE": str(original),
                   "isolated_workspace": str(isolated), "pre_sha": pre_sha,
                   "RUN_MODE": "editorial", "ALLOWED_PATHS": "research/wiki/",
                   "RETURN_ARTIFACTS": "", "BIRDY_TOOL_LOG_REL": "", "agent_status": "0",
                   "build_dir": str(build_dir)}
            result = subprocess.run(["bash", "-c", "set -euo pipefail\n" + guard], text=True,
                                    capture_output=True, env=env, check=False)
            return result, git(original, "rev-parse", "HEAD"), pre_sha, post_sha, original

        for adapter in ("claude", "cursor", "opencode"):
            for name in ("research/wiki/.gitattributes", "research/wiki/entities/.GitIgnore",
                         "research/wiki/.gitmodules"):
                with self.subTest(adapter=adapter, path=name):
                    result, head, pre_sha, _, original = run_guard(adapter, {
                        "research/wiki/entities/page.md": "page\n",
                        name: "* filter=lfs diff=lfs merge=lfs -text\n"})
                    self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
                    self.assertIn(f"commit path is git metadata: {name}",
                                  result.stdout + result.stderr)
                    self.assertEqual(pre_sha, head)
                    self.assertFalse((original / name).exists())
                    self.assertFalse((original / "research/wiki/entities/page.md").exists())
            with self.subTest(adapter=adapter, path="control"):
                result, head, _, post_sha, original = run_guard(adapter, {
                    "research/wiki/entities/page.md": "page\n"})
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertEqual(post_sha, head)
                self.assertEqual("page\n", (original / "research/wiki/entities/page.md")
                                 .read_text(encoding="utf-8"))

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

        ai_news = [ln for ln in matrix.splitlines()
                   if ln.startswith("| ai-news-research ")]
        self.assertEqual(1, len(ai_news), matrix)
        self.assertIn("claude-sonnet-5-5", ai_news[0])
        self.assertIn("native-model` override", ai_news[0])

    def test_readme_diagram_generated_and_deterministic(self):
        from build_backend_matrix import build_generated_blocks
        _, diagram1 = build_generated_blocks()
        _, diagram2 = build_generated_blocks()
        self.assertEqual(diagram1, diagram2)
        self.assertIn("flowchart LR", diagram1)
        self.assertIn("claude-sonnet-5-5", diagram1)
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

    def test_cursor_fallback_mode_mismatch_is_an_error(self):
        lanes, obs = self.mutated()
        step = next(
            step for step in obs["hourly-twitter.yml"].agent_run
            if step.lane == "twitter-primary"
        )
        step.cursor_mode = "editorial"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("fallback_mode 'twitter'" in e for e in errors), errors)

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
        lanes["generative-research-default"]["backend"] = "zai-glm-5p3"
        errors = cross_check(lanes, obs, self.profiles)
        self.assertTrue(any("not supported by" in e for e in errors), errors)

    def test_restricted_manual_backend_cannot_become_production_route(self):
        lanes, obs = self.mutated()
        routes = copy.deepcopy(load_routes())
        routes["research-editorial"]["backend"] = \
            "opencode-muse-spark-1p3-contributor"
        errors = cross_check(lanes, obs, self.profiles, routes)
        self.assertTrue(any("not production-eligible" in e for e in errors), errors)

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
