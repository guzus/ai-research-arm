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

    def test_claude_code_pin_must_match_the_isolated_container(self):
        data = ctp.load()
        self.assertRegex(data["claude_code"]["version"], r"^\d+\.\d+\.\d+$")
        for integrity in data["claude_code"]["integrity"].values():
            self.assertRegex(integrity, r"^sha512-[A-Za-z0-9+/]{86}==$")
        # A version bump without new integrity values, or a changed digest,
        # must fail: the container would install something nobody audited.
        data["claude_code"]["version"] = "2.1.999"
        self.assertTrue(any("platform package" in e for e in ctp.validate(data)))
        data = ctp.load()
        data["claude_code"]["integrity"]["linux_x64"] = (
            "sha512-" + "A" * 86 + "==")
        self.assertIn("Claude container lacks the audited linux_x64 SHA-512 checksum",
                      ctp.validate(data))
        data = ctp.load()
        data["claude_code"]["integrity"]["linux_arm64"] = "sha256-abc"
        self.assertIn("claude_code.integrity.linux_arm64 must be an npm sha512 SRI value",
                      ctp.validate(data))


if __name__ == "__main__":
    unittest.main()
