#!/usr/bin/env python3

import json
import tempfile
import unittest
from pathlib import Path

import artifact_slos


class ArtifactSloRegistryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = artifact_slos.load_registry()
        cls.by_id = {entry["id"]: entry for entry in cls.entries}

    def test_producers_and_validators_exist(self):
        root = artifact_slos.REPO_ROOT
        for entry in self.entries:
            self.assertTrue((root / entry["producer"]).is_file(), entry["id"])
            self.assertTrue(entry["artifacts"], entry["id"])
            for validator in entry["validators"]:
                self.assertTrue((root / validator).is_file(), f"{entry['id']}: {validator}")

    def test_market_artifacts_have_independent_freshness_paths(self):
        paths = {
            artifact_id: self.by_id[artifact_id]["freshness_paths"]
            for artifact_id in ("market-quotes", "model-pricing", "gpu-spot")
        }
        self.assertEqual(len({tuple(value) for value in paths.values()}), 3)
        self.assertNotIn(["research/market"], paths.values())

    def test_event_and_on_demand_artifacts_have_no_false_freshness_slo(self):
        self.assertNotIn("freshness_slo_hours", self.by_id["earnings"]["cadence"])
        self.assertNotIn("freshness_slo_hours", self.by_id["generative-research"]["cadence"])

    def test_fixed_cadence_registry_drives_both_watchdogs(self):
        import check_lane_freshness as freshness
        import check_lane_content as content

        expected = {e["id"] for e in artifact_slos.freshness_entries()}
        self.assertEqual(set(freshness.LANE_THRESHOLDS_HOURS), expected)
        self.assertEqual(set(content.LANE_SPECS), {e["id"] for e in artifact_slos.content_entries()})

    def test_every_publishable_degraded_policy_has_an_executable_signal(self):
        for entry in self.entries:
            if entry["degraded_policy"] in artifact_slos.PUBLISHED_DEGRADED_POLICIES:
                self.assertIn("degraded_signal", entry, entry["id"])
                self.assertIn(
                    entry["degraded_signal"]["kind"],
                    artifact_slos.DEGRADED_SIGNAL_KINDS,
                    entry["id"],
                )

    def test_json_signal_optional_fields_are_typed(self):
        base = {
            "schema_version": 1,
            "artifacts": [
                {
                    "id": "test",
                    "producer": "workflow.yml",
                    "artifacts": ["artifact.json"],
                    "freshness_paths": ["artifact.json"],
                    "validators": ["validator.py"],
                    "degraded_policy": "per-symbol-stale-carry-forward",
                    "degraded_signal": {
                        "kind": "json_boolean_any",
                        "label": "stale",
                        "path": "artifact.json",
                        "selectors": ["stale"],
                    },
                    "cadence": {
                        "kind": "interval",
                        "hours": 1,
                        "freshness_slo_hours": 3,
                    },
                }
            ],
        }
        for key, value, message in (
            ("absent_means_false", "false", "must be boolean"),
            ("required_selectors", [], "non-empty string list"),
        ):
            payload = json.loads(json.dumps(base))
            payload["artifacts"][0]["degraded_signal"][key] = value
            with tempfile.TemporaryDirectory() as tmp:
                registry = Path(tmp) / "artifact-slos.json"
                registry.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, message):
                    artifact_slos.load_registry(registry)

        payload = json.loads(json.dumps(base))
        signal = payload["artifacts"][0]["degraded_signal"]
        signal["selectors"] = ["rows.*.stale"]
        signal["absent_means_false"] = True
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "artifact-slos.json"
            registry.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "cannot be used with wildcard"):
                artifact_slos.load_registry(registry)


if __name__ == "__main__":
    unittest.main()
