"""Chubby contract tests: local preflight, strict selection and bearer isolation."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
from pathlib import Path
import shlex
import tempfile
import unittest
from unittest import mock

import yaml

from build_backend_matrix import cross_check, load_lanes, load_profiles, observe_workflow, workflow_files
from check_fireworks_backend import redact as redact_provider
from chubby_config import DEFAULT_BASE_URL, validate_config
from prepare_chubby_run import MODEL_ENV, prepare
from select_backend import main_with_args, probe_chubby
from summarize_claude_execution import redact as redact_execution

ROOT = Path(__file__).resolve().parent.parent
PROFILE = "chubby-deepseek-v4p1-flash"
MODEL_ID = "openrouter/deepseek/deepseek-v4.1-flash-1017"
KEY = "cbm_" + "a" * 64


class ChubbyConfigTest(unittest.TestCase):
    def test_valid_config_never_probes_network(self):
        with mock.patch.dict(os.environ, {"CHUBBY_API_KEY": KEY, "CHUBBY_BASE_URL": DEFAULT_BASE_URL}), \
             mock.patch("urllib.request.urlopen", side_effect=AssertionError("no paid preflight")):
            ok, reason = probe_chubby(MODEL_ID)
        self.assertTrue(ok)
        self.assertIn("live inference not checked", reason)

    def test_rejects_ordinary_keys_and_untrusted_url_shapes_without_echo(self):
        cases = [
            ("chb_" + "a" * 64, DEFAULT_BASE_URL),
            (KEY + "\n", DEFAULT_BASE_URL),
            (KEY, "http://example.com/office/api/chubby"),
            (KEY, "https://example.com/office/api/chubby/v1"),
            (KEY, f"https://{KEY}@example.com/office/api/chubby"),
            (KEY, DEFAULT_BASE_URL + "?token=" + KEY),
            (KEY, DEFAULT_BASE_URL + "#" + KEY),
            (KEY, "https://[bad/office/api/chubby"),
            (KEY, DEFAULT_BASE_URL + "\n"),
        ]
        for key, url in cases:
            with self.subTest(url=url), self.assertRaises(ValueError) as error:
                validate_config(key, url, MODEL_ID)
            self.assertNotIn(KEY, str(error.exception))
        with self.assertRaises(ValueError):
            validate_config(KEY, DEFAULT_BASE_URL, "claude-sonnet-5")

    def test_redacts_both_chubby_key_families_in_provider_and_transcript_errors(self):
        for redact in (redact_provider, redact_execution):
            message = f"error token={KEY} old=chb_{'b' * 64} Authorization: Bearer {KEY}"
            cleaned = redact(message)
            self.assertNotIn(KEY, cleaned)
            self.assertNotIn("b" * 64, cleaned)
            self.assertIn("redacted", cleaned)

    def test_prep_preserves_project_sandbox_and_writes_no_auth_or_global_env(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            original = json.loads((ROOT / ".claude/settings.json").read_text())
            outputs = prepare(ROOT, temp, KEY, DEFAULT_BASE_URL, MODEL_ID,
                              "--model opus --max-turns 8 --tools Read,Write")
            args = shlex.split(outputs["claude-args"])
            policy = json.loads(Path(args[args.index("--settings") + 1]).read_text())
            self.assertEqual(args[-2:], ["--model", MODEL_ID])
            self.assertEqual(args[args.index("--setting-sources") + 1], "user,project")
            self.assertLessEqual(set(original["permissions"]["deny"]), set(policy["permissions"]["deny"]))
            self.assertIn(str(Path.home().resolve()) + "/", policy["sandbox"]["filesystem"]["denyRead"])
            self.assertIn("Read(/" + str(Path.home().resolve()) + "/**)", policy["permissions"]["deny"])
            self.assertTrue(policy["sandbox"]["enabled"])
            self.assertTrue(policy["sandbox"]["failIfUnavailable"])
            self.assertFalse(policy["sandbox"]["allowUnsandboxedCommands"])
            self.assertFalse(policy["sandbox"]["enableWeakerNestedSandbox"])
            for name in MODEL_ENV:
                self.assertEqual(policy["env"][name], MODEL_ID)
            self.assertEqual(policy["env"]["ANTHROPIC_BASE_URL"], DEFAULT_BASE_URL)
            self.assertEqual(policy["env"]["ANTHROPIC_API_KEY"], "")
            self.assertEqual(policy["env"]["CLAUDE_CODE_OAUTH_TOKEN"], "")
            self.assertNotIn("ANTHROPIC_AUTH_TOKEN", policy["env"])
            self.assertEqual(policy["env"]["ENABLE_TOOL_SEARCH"], "false")
            self.assertEqual(policy["env"]["CLAUDE_CODE_MAX_RETRIES"], "0")
            self.assertEqual(policy["env"]["CLAUDE_CODE_MAX_OUTPUT_TOKENS"], "4096")
            self.assertEqual(policy["apiKeyHelper"], "")
            self.assertEqual(policy["env"]["HTTPS_PROXY"], "")
            self.assertEqual(Path(outputs["home"]).stat().st_mode & 0o777, 0o700)
            for file in temp.rglob("*"):
                if file.is_file():
                    self.assertNotIn(KEY, file.read_text())
                    self.assertNotIn(file.name, {".credentials.json", "auth.json"})

    def test_prep_rejects_auth_in_project_policy_and_caller_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            root = temp / "repo"
            (root / ".claude").mkdir(parents=True)
            settings = root / ".claude/settings.json"
            policy = json.loads((ROOT / ".claude/settings.json").read_text())
            for name in ("ANTHROPIC_AUTH_TOKEN", "CHUBBY_API_KEY"):
                policy["env"] = {name: "attacker"}
                settings.write_text(json.dumps(policy))
                with self.assertRaises(ValueError):
                    prepare(root, temp, KEY, DEFAULT_BASE_URL, MODEL_ID, "")
            for arg in ("--settings evil.json", "--setting-sources local", "--fallback-model claude"):
                with self.assertRaises(ValueError):
                    prepare(ROOT, temp, KEY, DEFAULT_BASE_URL, MODEL_ID, arg)


class ChubbySelectionTest(unittest.TestCase):
    def select(self, *args, key=KEY, mutate=None, event="workflow_dispatch"):
        data = json.loads((ROOT / "data/agent-backends.json").read_text())
        if mutate:
            mutate(data)
        with tempfile.TemporaryDirectory() as directory:
            config, output = Path(directory) / "registry.json", Path(directory) / "output"
            config.write_text(json.dumps(data))
            log = io.StringIO()
            with mock.patch.dict(os.environ, {"CHUBBY_API_KEY": key, "CHUBBY_BASE_URL": DEFAULT_BASE_URL,
                                              "GITHUB_EVENT_NAME": event,
                                              "CLAUDE_CODE_OAUTH_TOKEN": "",
                                              "ANTHROPIC_API_KEY": "",
                                              "FIREWORKS_API_KEY": "", "ZAI_API_KEY": ""}), \
                 mock.patch("urllib.request.urlopen", side_effect=AssertionError("no network")), \
                 contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                code = main_with_args(["--file", str(config), "--github-output", str(output), *args])
            return code, output.read_text() if output.exists() else "", log.getvalue()

    def test_manual_canary_selects_nonproduction_profile_without_native_credentials(self):
        code, out, log = self.select("--lane", "chubby-canary")
        self.assertEqual(code, 0, log)
        self.assertIn(f"model-id={MODEL_ID}", out)
        self.assertIn("used-fallback=false", out)

    def test_explicit_backend_without_strict_flag_still_cannot_fallback(self):
        code, out, log = self.select("--backend", PROFILE, key="")
        self.assertEqual(code, 1, log)
        self.assertEqual(out, "")
        self.assertNotIn("candidate claude", log)
        self.assertIn("walked 1 candidate", log)

    def test_scheduled_or_unpinned_manual_lane_cannot_bypass_eligibility(self):
        for event in ("schedule", "push", "workflow_call"):
            code, _, log = self.select("--lane", "chubby-canary", event=event)
            self.assertEqual(code, 2, log)
        for field in ("manual_only", "strict", "pinned", "pinned_provider"):
            def mutate(data):
                data["lanes"]["chubby-canary"].pop(field)
            code, _, log = self.select("--lane", "chubby-canary", mutate=mutate)
            self.assertEqual(code, 2, log)

    def test_manual_diagnostic_cannot_bypass_active_profile_restrictions(self):
        def mutate(data):
            data["backends"][PROFILE]["restrictions"] = {"requires_consent": True}
        code, _, log = self.select("--lane", "chubby-canary", mutate=mutate)
        self.assertEqual(code, 2, log)
        self.assertIn("active restrictions: requires_consent", log)

    def test_chubby_cannot_be_added_as_fallback_even_after_marked_eligible(self):
        def mutate(data):
            data["backends"][PROFILE]["production_eligible"] = True
            data["lanes"]["twitter-judge"]["fallback_chain"] = [PROFILE]
        code, _, log = self.select("--lane", "twitter-judge", mutate=mutate)
        self.assertEqual(code, 2, log)
        self.assertIn("Chubby cannot be selected from a fallback chain", log)


class ChubbyWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lanes, _ = load_lanes()
        cls.profiles = load_profiles()
        cls.observations = {p.name: observe_workflow(p) for p in workflow_files()}

    def test_credential_is_required_only_for_chubby_lane(self):
        obs = copy.deepcopy(self.observations)
        self.assertEqual(cross_check(self.lanes, obs, self.profiles), [])
        obs["chubby-canary.yml"].agent_run[0].secrets["chubby-api-key"] = ""
        self.assertTrue(any("Chubby requires" in e for e in cross_check(self.lanes, obs, self.profiles)))
        obs = copy.deepcopy(self.observations)
        obs["daily-digest.yml"].agent_run[0].secrets["chubby-api-key"] = "CHUBBY_API_KEY"
        self.assertTrue(any("unrelated lanes" in e for e in cross_check(self.lanes, obs, self.profiles)))

    def test_scoped_workflow_and_matrix_exclude_unrelated_credentials(self):
        step = self.observations["chubby-canary.yml"].agent_run[0]
        supplied = {key: value for key, value in step.secrets.items() if value}
        self.assertEqual(supplied, {"chubby-api-key": "CHUBBY_API_KEY"})
        for name, secret in (("claude-code-oauth-token", "CLAUDE_CODE_OAUTH_TOKEN"),
                             ("fireworks-api-key", "FIREWORKS_API_KEY"),
                             ("zai-api-key", "ZAI_API_KEY")):
            obs = copy.deepcopy(self.observations)
            obs["chubby-canary.yml"].agent_run[0].secrets[name] = secret
            self.assertTrue(any("unrelated credential" in error
                                for error in cross_check(self.lanes, obs, self.profiles)))

    def test_manual_diagnostic_matrix_cannot_bypass_active_restrictions(self):
        profiles = copy.deepcopy(self.profiles)
        profiles[PROFILE].production_restrictions = ["requires_consent"]
        errors = cross_check(self.lanes, self.observations, profiles)
        self.assertTrue(any("not production-eligible" in error for error in errors), errors)

    def test_canary_sets_commit_identity_in_repo_before_running_agent(self):
        workflow = yaml.safe_load((ROOT / ".github/workflows/chubby-canary.yml").read_text())
        steps = workflow["jobs"]["canary"]["steps"]
        identity_index = next(i for i, step in enumerate(steps)
                              if step.get("name") == "Configure local commit identity")
        agent_index = next(i for i, step in enumerate(steps) if step.get("id") == "agent")
        self.assertLess(identity_index, agent_index)
        self.assertIn("git config --local user.name", steps[identity_index]["run"])
        self.assertIn("git config --local user.email", steps[identity_index]["run"])

    def test_manual_lane_rejects_new_automatic_trigger(self):
        obs = copy.deepcopy(self.observations)
        obs["chubby-canary.yml"].events.add("schedule")
        errors = cross_check(self.lanes, obs, self.profiles)
        self.assertTrue(any("workflow_dispatch-only" in e for e in errors), errors)

    def test_action_passes_bearer_only_to_child_with_private_home_and_always_cleanup(self):
        action = yaml.safe_load((ROOT / ".github/actions/agent-run/action.yml").read_text())
        steps = action["runs"]["steps"]
        child = next(step for step in steps if step.get("id") == "run-chubby")
        self.assertEqual(child["with"]["anthropic_api_key"], "chubby-bearer-env-only")
        self.assertNotIn("claude_code_oauth_token", child["with"])
        self.assertEqual(child["env"]["CLAUDE_CODE_OAUTH_TOKEN"], "")
        self.assertEqual(child["env"]["ANTHROPIC_AUTH_TOKEN"], "${{ inputs.chubby-api-key }}")
        self.assertEqual(child["env"]["HOME"], "${{ steps.chubby-config.outputs.home }}")
        self.assertEqual(child["env"]["CLAUDE_CONFIG_DIR"], "${{ steps.chubby-config.outputs.config-dir }}")
        self.assertEqual(child["with"]["classify_inline_comments"], "false")
        self.assertEqual(child["env"]["ACTIONS_STEP_DEBUG"], "false")
        self.assertIn("run-chubby.outputs.execution_file", action["outputs"]["execution-file"]["value"])
        cleanup = next(step for step in steps if step.get("name") == "Remove isolated Chubby configuration")
        self.assertIn("always()", cleanup["if"])
        self.assertIn('"$RUNNER_TEMP"/ara-chubby-*', cleanup["run"])


if __name__ == "__main__":
    unittest.main()
