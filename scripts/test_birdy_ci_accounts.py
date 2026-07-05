from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from birdy_ci_accounts import BirdyAccountError, build_accounts


class BirdyCiAccountsTests(unittest.TestCase):
    def test_builds_read_only_fallback_account(self):
        accounts = build_accounts("", "auth", "ct0")

        self.assertEqual(
            accounts,
            [{"name": "ci", "auth_token": "auth", "ct0": "ct0", "read_only": True}],
        )

    def test_forces_secret_accounts_read_only_and_preserves_fields(self):
        accounts = build_accounts(
            json.dumps(
                [
                    {"name": "alpha", "auth_token": "a", "ct0": "ca", "read_only": False, "proxy": "p1"},
                    {"auth_token": "b", "ct0": "cb"},
                ]
            ),
            None,
            None,
        )

        self.assertEqual(accounts[0]["name"], "alpha")
        self.assertEqual(accounts[0]["proxy"], "p1")
        self.assertEqual(accounts[1]["name"], "ci-2")
        self.assertTrue(all(account["read_only"] is True for account in accounts))

    def test_rejects_invalid_accounts_json(self):
        with self.assertRaisesRegex(BirdyAccountError, "valid JSON"):
            build_accounts("{", "auth", "ct0")

    def test_rejects_empty_accounts_array(self):
        with self.assertRaisesRegex(BirdyAccountError, "non-empty JSON array"):
            build_accounts("[]", "auth", "ct0")

    def test_rejects_missing_fallback_cookies(self):
        with self.assertRaisesRegex(BirdyAccountError, "BIRD_AUTH_TOKEN and BIRD_CT0"):
            build_accounts("", "", "ct0")

    def test_rejects_account_without_cookie_fields(self):
        with self.assertRaisesRegex(BirdyAccountError, "entry 1"):
            build_accounts('[{"name":"alpha","auth_token":"a"}]', None, None)


if __name__ == "__main__":
    unittest.main()
