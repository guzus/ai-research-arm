#!/usr/bin/env python3

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


if __name__ == "__main__":
    unittest.main()
