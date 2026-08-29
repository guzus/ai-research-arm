#!/usr/bin/env python3

import unittest

import check_toolchain_pins as ctp


class ToolchainPinsTest(unittest.TestCase):
    def test_shipped_manifest_and_call_sites_are_consistent(self):
        data = ctp.load()
        self.assertEqual(ctp.validate(data), [])

    def test_every_binary_checksum_is_sha256(self):
        data = ctp.load()
        digests = list(data["birdy"]["sha256"].values()) + list(data["cursor_agent"]["sha256"].values())
        for digest in digests:
            self.assertRegex(digest, r"^[0-9a-f]{64}$")

    def test_generated_doc_matches_manifest(self):
        self.assertEqual(ctp.DOC_FILE.read_text(encoding="utf-8"), ctp.render(ctp.load()))


if __name__ == "__main__":
    unittest.main()
