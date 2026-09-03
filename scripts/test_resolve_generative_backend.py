"""Focused tests for registry-driven generative backend resolution."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from resolve_agent_route import resolve_route
from resolve_generative_backend import ResolutionError, load_config, resolve


ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "data" / "agent-backends.json"


class GenerativeBackendResolverTests(unittest.TestCase):
    def setUp(self):
        self.data = load_config(REGISTRY)

    def test_aliases_normalize_to_canonical_selector(self):
        self.assertEqual("codex", resolve(self.data, "openai-codex").selector)
        self.assertEqual("claude", resolve(self.data, "claude-sonnet-5").selector)
        self.assertEqual(
            "opencode-muse-spark-1p3-contributor",
            resolve(self.data, "muse-1.3").selector,
        )

    def test_model_ref_splits_only_at_provider_and_preserves_nested_model(self):
        data = copy.deepcopy(self.data)
        data["backends"]["opencode-openrouter-example"] = {
            "adapter": "opencode",
            "provider": "opencode-go",
            "model": "openrouter/vendor/future-model",
            "display_name": "Future model via registered OpenCode adapter",
            "aliases": ["future-model"],
            "production_eligible": False,
            "generative": {
                "exposed": True,
                "selector": "opencode-openrouter-example",
                "provenance_model": "openrouter/vendor/future-model",
                "protocol": "openai-chat-completions",
                "preflight_path": "chat/completions",
            },
        }
        selection = resolve(data, "future-model")
        self.assertEqual("opencode-go/openrouter/vendor/future-model", selection.model_ref)
        self.assertEqual("opencode-openrouter-example", selection.selector)

    def test_synthetic_exposed_model_needs_only_one_registry_entry(self):
        data = copy.deepcopy(self.data)
        data["backends"]["cursor-future"] = {
            "adapter": "cursor",
            "provider": "cursor",
            "model": "future-model",
            "display_name": "Future Cursor model",
            "aliases": ["future"],
            "production_eligible": False,
            "generative": {
                "exposed": True,
                "selector": "cursor-future",
                "provenance_model": "future-model",
                "protocol": "cursor-cli",
                "preflight_path": "harness",
            },
        }
        before = (ROOT / ".github/workflows/generative-research.yml").read_bytes()
        self.assertEqual("cursor-future", resolve(data, "future").selector)
        self.assertEqual(before, (ROOT / ".github/workflows/generative-research.yml").read_bytes())

    def test_rejects_non_exposed_and_injection_selectors(self):
        with self.assertRaisesRegex(ResolutionError, "non-exposed"):
            resolve(self.data, "opencode-glm-5p3-flash")
        for selector in ("codex\nfoo=bar", "--model", "../codex", "codex;id"):
            with self.subTest(selector=selector), self.assertRaises(ResolutionError):
                resolve(self.data, selector)

    def test_new_provider_needs_explicit_adapter_credential_plumbing(self):
        data = copy.deepcopy(self.data)
        data["backends"]["unwired-model"] = {
            "adapter": "opencode",
            "provider": "openrouter",
            "model": "vendor/model",
            "display_name": "Unwired model",
            "aliases": [],
            "production_eligible": False,
            "generative": {
                "exposed": True,
                "selector": "unwired-model",
                "provenance_model": "vendor/model",
                "protocol": "openai-chat-completions",
                "preflight_path": "chat/completions",
            },
        }
        with self.assertRaisesRegex(ResolutionError, "credential binding|unsupported"):
            resolve(data, "unwired-model")

    def test_provenance_and_protocol_are_exact(self):
        muse = resolve(self.data, "opencode-muse-spark-1p3-contributor")
        self.assertEqual("muse-spark-1.3-contributor", muse.provenance_model)
        self.assertEqual("openai-responses", muse.protocol)
        self.assertEqual("responses", muse.preflight_path)

    def test_isolated_adapter_provenance_must_equal_served_model(self):
        for backend in ("opencode-deepseek-v4-flash", "cursor-grok-4p6-fast"):
            with self.subTest(backend=backend):
                data = copy.deepcopy(self.data)
                data["backends"][backend]["generative"]["provenance_model"] = \
                    "different-model"
                with self.assertRaisesRegex(ResolutionError, "must equal the served model"):
                    resolve(data, backend)

    def test_restricted_muse_cannot_be_promoted_to_production_route(self):
        data = copy.deepcopy(self.data)
        data["routes"]["research-editorial"]["backend"] = \
            "opencode-muse-spark-1p3-contributor"
        with self.assertRaisesRegex(ValueError, "active production restrictions"):
            resolve_route(data, "rss")

    def test_restricted_model_cannot_be_automated_default_or_boolean_bypassed(self):
        data = copy.deepcopy(self.data)
        data["lanes"]["generative-research-default"]["backend"] = \
            "opencode-muse-spark-1p3-contributor"
        with self.assertRaisesRegex(ResolutionError, "default.*not production-eligible"):
            resolve(data, "default")

        data = copy.deepcopy(self.data)
        data["backends"]["opencode-muse-spark-1p3-contributor"] \
            ["production_eligible"] = True
        with self.assertRaisesRegex(ResolutionError, "restrictions are active"):
            resolve(data, "muse-1.3")

    def test_cursor_rejects_nested_cli_model_ids_at_registration(self):
        data = copy.deepcopy(self.data)
        data["backends"]["cursor-grok-4p6-fast"]["model"] = "vendor/nested-model"
        with self.assertRaisesRegex(ResolutionError, "one CLI model id"):
            resolve(data, "cursor-grok-4p6-fast")

    def test_github_output_is_single_line_and_canonical(self):
        selection = resolve(self.data, "muse-1.3")
        from resolve_generative_backend import write_outputs
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "output"
            write_outputs(path, selection)
            values = dict(line.split("=", 1) for line in path.read_text().splitlines())
        self.assertEqual("opencode-muse-spark-1p3-contributor", values["selector"])
        self.assertEqual("opencode-go/muse-spark-1.3-contributor", values["model_ref"])
        self.assertEqual("false", values["production_eligible"])


if __name__ == "__main__":
    unittest.main()
