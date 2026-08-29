"""Tests for scripts/select_backend.py — the runtime backend selector that
walks the SSOT fallback chain in order. Probes are monkeypatched so no
network is touched; chain-walk ORDER is the load-bearing behavior."""

import contextlib
import io
import json
import os
import tempfile
import unittest
import unittest.mock
from pathlib import Path

import select_backend


def fake_data(chain, lanes=None):
    return {
        "backends": {
            "claude": {"provider": "claude", "model": "", "display_name": "Claude", "aliases": []},
            "fireworks-glm-5p2": {"provider": "fireworks",
                                  "model": "accounts/fireworks/models/glm-5p2",
                                  "display_name": "GLM 5.2 via Fireworks",
                                  "aliases": ["glm-5p2", "glm"]},
            "zai-glm-5p2": {"provider": "zai", "model": "glm-5.2",
                            "display_name": "GLM 5.2 via Z.ai", "aliases": ["zai"]},
            "opencode-glm-5p3-flash": {
                "adapter": "opencode",
                "provider": "opencode-go", "model": "glm-5.3-flash",
                "display_name": "GLM 5.3 Flash via OpenCode Go",
                "aliases": ["opencode-glm"],
            },
        },
        "fallback": {"harness": "agent-run", "chain": chain,
                     "native_model": "claude-sonnet-5"},
        "lanes": lanes or {
            "rss": {"workflow": "hourly-rss.yml", "harness": "agent-run",
                    "backend": "fireworks-glm-5p2"},
            "strict-lane": {"workflow": "x.yml", "harness": "agent-run",
                            "backend": "zai-glm-5p2", "strict": True},
            "mirror": {"workflow": "y.yml", "harness": "pi",
                       "provider": "fireworks", "model": "m"},
        },
    }


class SelectBackendTest(unittest.TestCase):
    def setUp(self):
        self._orig_probes = dict(select_backend.PROBES)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(lambda: select_backend.PROBES.update(self._orig_probes))

    def set_availability(self, **by_provider):
        for provider, available in by_provider.items():
            select_backend.PROBES[provider] = (
                lambda model, a=available, p=provider: (a, f"{p} stub")
            )

    def run_select(self, *argv, chain=("zai-glm-5p2", "claude"), lanes=None):
        data_file = Path(self.tmp.name) / "backends.json"
        data_file.write_text(json.dumps(fake_data(list(chain), lanes)))
        out_file = Path(self.tmp.name) / "out.txt"
        out_file.write_text("")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stdout):
            code = select_backend.main_with_args(
                ["--file", str(data_file), "--github-output", str(out_file), *argv])
        outputs = dict(line.split("=", 1) for line in out_file.read_text().splitlines() if "=" in line)
        return code, outputs, stdout.getvalue()

    def test_primary_available_no_fallback(self):
        self.set_availability(fireworks=True, zai=True, claude=True)
        code, out, _ = self.run_select("--lane", "rss")
        self.assertEqual(code, 0)
        self.assertEqual(out["backend"], "fireworks-glm-5p2")
        self.assertEqual(out["used-fallback"], "false")

    def test_chain_walked_in_order(self):
        self.set_availability(fireworks=False, zai=True, claude=True)
        code, out, _ = self.run_select("--lane", "rss")
        self.assertEqual(code, 0)
        self.assertEqual(out["backend"], "zai-glm-5p2")
        self.assertEqual(out["provider"], "zai")
        self.assertEqual(out["used-fallback"], "true")

    def test_claude_429_uses_lane_local_opencode_before_global_zai(self):
        lanes = {
            "digest": {"workflow": "daily-digest.yml", "harness": "agent-run",
                       "backend": "claude",
                       "fallback_chain": ["opencode-glm-5p3-flash"]},
        }
        self.set_availability(zai=True, **{"opencode-go": True})
        with unittest.mock.patch.dict(
                os.environ, {"CLAUDE_CODE_OAUTH_TOKEN": "sk-ant-oat01-test"}), \
                unittest.mock.patch.object(
                    select_backend, "request_oauth_preflight",
                    return_value=(429, '{"error":{"message":"rate limit exceeded"}}')):
            code, out, log = self.run_select(
                "--lane", "digest", chain=("claude", "zai-glm-5p2"), lanes=lanes)

        self.assertEqual(code, 0)
        self.assertEqual(out["backend"], "opencode-glm-5p3-flash")
        self.assertEqual(out["provider"], "opencode-go")
        self.assertEqual(out["used-fallback"], "true")
        self.assertIn("rate limited for this run", log)

    def test_twitter_primary_and_repair_use_opencode_on_claude_429(self):
        lanes = {
            lane: {
                "workflow": "hourly-twitter.yml",
                "harness": "agent-run",
                "backend": "claude",
                "fallback_chain": ["opencode-glm-5p3-flash"],
            }
            for lane in ("twitter-primary", "twitter-primary-repair")
        }
        self.set_availability(zai=True, **{"opencode-go": True})
        with unittest.mock.patch.dict(
                os.environ, {"CLAUDE_CODE_OAUTH_TOKEN": "sk-ant-oat01-test"}), \
                unittest.mock.patch.object(
                    select_backend, "request_oauth_preflight",
                    return_value=(429, '{"error":{"message":"rate limit exceeded"}}')):
            for lane in lanes:
                with self.subTest(lane=lane):
                    code, out, log = self.run_select(
                        "--lane", lane,
                        chain=("claude", "zai-glm-5p2"), lanes=lanes)
                    self.assertEqual(code, 0)
                    self.assertEqual(out["backend"], "opencode-glm-5p3-flash")
                    self.assertEqual(out["provider"], "opencode-go")
                    self.assertEqual(out["used-fallback"], "true")
                    self.assertIn("rate limited for this run", log)

    def test_claude_429_does_not_cross_strict_lane_boundary(self):
        lanes = {
            "digest": {"workflow": "daily-digest.yml", "harness": "agent-run",
                       "backend": "claude",
                       "fallback_chain": ["opencode-glm-5p3-flash"]},
        }
        self.set_availability(zai=True, **{"opencode-go": True})
        with unittest.mock.patch.dict(
                os.environ, {"CLAUDE_CODE_OAUTH_TOKEN": "sk-ant-oat01-test"}), \
                unittest.mock.patch.object(
                    select_backend, "request_oauth_preflight",
                    return_value=(429, '{"error":{"message":"rate limit exceeded"}}')):
            code, out, log = self.run_select(
                "--lane", "digest", "--fallback-policy", "none",
                chain=("claude", "zai-glm-5p2"), lanes=lanes)

        self.assertEqual(code, 1)
        self.assertNotIn("backend", out)
        self.assertIn("rate limited for this run", log)
        self.assertNotIn("candidate opencode-glm-5p3-flash", log)
        self.assertNotIn("candidate zai-glm-5p2", log)

    def test_lane_override_does_not_continue_to_global_zai(self):
        lanes = {
            "digest": {"workflow": "daily-digest.yml", "harness": "agent-run",
                       "backend": "claude",
                       "fallback_chain": ["opencode-glm-5p3-flash"]},
        }
        self.set_availability(zai=True, **{"opencode-go": False})
        with unittest.mock.patch.dict(
                os.environ, {"CLAUDE_CODE_OAUTH_TOKEN": "sk-ant-oat01-test"}), \
                unittest.mock.patch.object(
                    select_backend, "request_oauth_preflight", return_value=(429, "{}")):
            code, out, log = self.run_select(
                "--lane", "digest", chain=("claude", "zai-glm-5p2"), lanes=lanes)

        self.assertEqual(code, 1)
        self.assertNotIn("backend", out)
        self.assertIn("candidate opencode-glm-5p3-flash", log)
        self.assertNotIn("candidate zai-glm-5p2", log)

    def test_explicit_cross_adapter_override_requires_lane_contract(self):
        code, out, log = self.run_select(
            "--backend", "opencode-glm", chain=("claude", "zai-glm-5p2"))
        self.assertEqual(code, 2)
        self.assertNotIn("backend", out)
        self.assertIn("requires a lane fallback_chain contract", log)

    def test_chain_skips_unavailable_middle_candidate(self):
        self.set_availability(fireworks=False, zai=False, claude=True)
        code, out, _ = self.run_select("--lane", "rss")
        self.assertEqual(code, 0)
        self.assertEqual(out["backend"], "claude")
        self.assertEqual(out["native-model"], "claude-sonnet-5")

    def test_requested_backend_not_retried_from_chain(self):
        self.set_availability(fireworks=True, zai=False, claude=True)
        code, out, log = self.run_select("--lane", "rss", chain=("fireworks-glm-5p2", "claude"))
        self.assertEqual(code, 0)
        self.assertEqual(out["backend"], "fireworks-glm-5p2")
        # now make fireworks unavailable: chain's identical entry must be skipped
        self.set_availability(fireworks=False, zai=False, claude=True)
        code, out, log = self.run_select("--lane", "rss", chain=("fireworks-glm-5p2", "claude"))
        self.assertEqual(code, 0)
        self.assertEqual(out["backend"], "claude")
        self.assertEqual(log.count("candidate fireworks-glm-5p2"), 1)

    def test_strict_lane_never_walks_chain(self):
        self.set_availability(fireworks=True, zai=False, claude=True)
        code, out, _ = self.run_select("--lane", "strict-lane")
        self.assertEqual(code, 1)
        self.assertNotIn("backend", out)

    def test_policy_none_is_strict(self):
        self.set_availability(fireworks=False, zai=True, claude=True)
        code, out, _ = self.run_select("--lane", "rss", "--fallback-policy", "none")
        self.assertEqual(code, 1)

    def test_all_candidates_down_fails_loud(self):
        self.set_availability(fireworks=False, zai=False, claude=False)
        code, out, log = self.run_select("--lane", "rss")
        self.assertEqual(code, 1)
        self.assertIn("no available backend", log)

    def test_explicit_backend_override_and_alias(self):
        self.set_availability(fireworks=True, zai=True, claude=True)
        code, out, _ = self.run_select("--backend", "glm")
        self.assertEqual(code, 0)
        self.assertEqual(out["backend"], "fireworks-glm-5p2")
        self.assertEqual(out["requested-backend"], "fireworks-glm-5p2")

    def test_native_model_override(self):
        self.set_availability(fireworks=False, zai=False, claude=True)
        code, out, _ = self.run_select("--lane", "rss", "--native-model-override", "claude-opus-4-8")
        self.assertEqual(code, 0)
        self.assertEqual(out["native-model"], "claude-opus-4-8")

    def test_unknown_lane_is_config_error(self):
        code, out, _ = self.run_select("--lane", "nope")
        self.assertEqual(code, 2)

    def test_mirror_lane_rejected(self):
        code, out, _ = self.run_select("--lane", "mirror")
        self.assertEqual(code, 2)

    def test_missing_lane_and_backend_is_config_error(self):
        code, out, _ = self.run_select()
        self.assertEqual(code, 2)


class ProbeClaudeTest(unittest.TestCase):
    """Regression tests for the 2026-07-24 fleet-wide outage.

    probe_claude used to hardcode "always available", so an expired
    CLAUDE_CODE_OAUTH_TOKEN killed every agent lane with no route out.
    The replacement must be sharp in BOTH directions: down on a real
    credential rejection or a run-scoped 429, without broadening other
    inconclusive failures into reroutes.
    """

    def setUp(self):
        self._orig = select_backend.request_oauth_preflight
        self.addCleanup(lambda: setattr(
            select_backend, "request_oauth_preflight", self._orig))
        os.environ["CLAUDE_CODE_OAUTH_TOKEN"] = "sk-ant-oat01-test"
        self.addCleanup(os.environ.pop, "CLAUDE_CODE_OAUTH_TOKEN", None)

    def stub(self, status, body='{"error":{"message":"x"}}'):
        select_backend.request_oauth_preflight = (
            lambda token, model, s=status, b=body: (s, b))

    def test_auth_rejection_marks_claude_down(self):
        for status in (401, 403):
            with self.subTest(status=status):
                self.stub(status)
                available, reason = select_backend.probe_claude("claude-sonnet-5")
                self.assertFalse(available)
                self.assertIn(str(status), reason)

    def test_rate_limit_marks_claude_unavailable_for_this_run(self):
        self.stub(429, '{"error":{"message":"rate limit exceeded"}}')
        available, reason = select_backend.probe_claude("claude-sonnet-5")
        self.assertFalse(available)
        self.assertIn("rate limited for this run", reason)

    def test_healthy_and_inconclusive_non_auth_failures_keep_claude_up(self):
        # Preserve the old narrow behavior for shapes this preflight cannot
        # mechanically prove will prevent Claude Code from serving the run.
        for status in (200, 400, 500, 529):
            with self.subTest(status=status):
                self.stub(status)
                available, _ = select_backend.probe_claude("claude-sonnet-5")
                self.assertTrue(available)

    def test_network_fault_fails_open(self):
        def boom(token, model):
            raise OSError("connection reset")
        select_backend.request_oauth_preflight = boom
        available, reason = select_backend.probe_claude("claude-sonnet-5")
        self.assertTrue(available, "a transient blip must not reroute the fleet")
        self.assertIn("inconclusive", reason)

    def test_missing_token_marks_claude_down(self):
        os.environ.pop("CLAUDE_CODE_OAUTH_TOKEN", None)
        available, reason = select_backend.probe_claude("claude-sonnet-5")
        self.assertFalse(available)
        self.assertIn("not configured", reason)

    def test_preflight_never_sends_x_api_key(self):
        """The header that would strand the fleet on the fallback backend.

        api.anthropic.com answers a healthy OAuth token with
        `401 invalid x-api-key` when x-api-key is present, so reusing the
        Fireworks-style preflight here would report Claude permanently dead.
        """
        captured = {}

        class FakeResponse:
            status = 200

            def read(self):
                return b"{}"

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

        def fake_urlopen(request, timeout=None):
            captured["headers"] = {k.lower(): v for k, v in request.header_items()}
            return FakeResponse()

        with unittest.mock.patch.object(
                select_backend.urllib.request, "urlopen", fake_urlopen):
            status, _ = select_backend.request_oauth_preflight("tok", "claude-sonnet-5")

        self.assertEqual(status, 200)
        self.assertNotIn("x-api-key", captured["headers"])
        self.assertEqual(captured["headers"]["authorization"], "Bearer tok")
        self.assertEqual(
            captured["headers"]["anthropic-beta"],
            select_backend.ANTHROPIC_OAUTH_BETA)


class ProbeOpenCodeTest(unittest.TestCase):
    def test_requires_scoped_credential(self):
        with unittest.mock.patch.dict(os.environ, {}, clear=True):
            available, reason = select_backend.probe_opencode("glm-5.3-flash")
        self.assertFalse(available)
        self.assertIn("not configured", reason)

    def test_configured_credential_is_available_without_network_probe(self):
        with unittest.mock.patch.dict(
                os.environ, {"OPENCODE_API_KEY": "test-key"}, clear=True):
            available, reason = select_backend.probe_opencode("glm-5.3-flash")
        self.assertTrue(available)
        self.assertIn("isolated OpenCode", reason)


if __name__ == "__main__":
    unittest.main()
