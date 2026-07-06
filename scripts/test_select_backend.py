"""Tests for scripts/select_backend.py — the runtime backend selector that
walks the SSOT fallback chain in order. Probes are monkeypatched so no
network is touched; chain-walk ORDER is the load-bearing behavior."""

import contextlib
import io
import json
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
