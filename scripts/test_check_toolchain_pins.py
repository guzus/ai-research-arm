#!/usr/bin/env python3

import unittest

import check_toolchain_pins as ctp


class ToolchainPinsTest(unittest.TestCase):
    def test_shipped_manifest_and_call_sites_are_consistent(self):
        data = ctp.load()
        self.assertEqual(ctp.validate(data), [])

    def test_every_binary_checksum_is_sha256(self):
        data = ctp.load()
        digests = [digest for tool in ("birdy", "cursor_agent", "agent_bun")
                   for digest in data[tool]["sha256"].values()]
        for digest in digests:
            self.assertRegex(digest, r"^[0-9a-f]{64}$")

    def test_generated_doc_matches_manifest(self):
        self.assertEqual(ctp.DOC_FILE.read_text(encoding="utf-8"), ctp.render(ctp.load()))

    def test_agent_bun_requires_complete_release_integrity(self):
        data = ctp.load()
        data["agent_bun"]["sha256"].pop("linux_aarch64")
        self.assertIn("agent_bun must pin both supported Linux architectures", ctp.validate(data))
        data = ctp.load()
        data["agent_bun"]["version"] = "latest"
        self.assertIn("agent_bun.version must be an exact release version", ctp.validate(data))


if __name__ == "__main__":
    unittest.main()
