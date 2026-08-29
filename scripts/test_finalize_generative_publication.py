#!/usr/bin/env python3

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import build_claim_index as claims
import finalize_generative_publication as finalizer


class TransactionalPublicationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self._git("config", "user.name", "Test")
        self._git("config", "user.email", "test@example.test")
        gen = self.repo / "research" / "generative"
        (self.repo / "research" / "claims").mkdir(parents=True)
        gen.mkdir(parents=True)
        self.stem = "2026-08-29T000000--transaction"
        (gen / f"{self.stem}.html").write_text('<article class="ara-doc"></article>\n')
        (gen / f"{self.stem}.ara.md").write_text("# Transaction\n")
        (gen / "index.json").write_text(json.dumps([{
            "file": f"{self.stem}.html", "slug": "transaction", "title": "Transaction",
            "created_at": "2026-08-29T00:00:00Z", "tags": []
        }]) + "\n")
        empty = claims.render(claims.build_index(gen))
        (self.repo / "research" / "claims" / "index.json").write_text(empty)
        self._git("add", ".")
        self._git("commit", "-qm", "seed")
        (gen / f"{self.stem}.html").write_text('<article class="ara-doc">writer revision</article>\n')
        self._git("add", ".")
        self._git("commit", "-qm", "writer article commit")
        self.ledger = Path(self.temp.name) / "incoming-claims.json"
        self.verification = Path(self.temp.name) / "incoming-verification.json"
        self.redteam = Path(self.temp.name) / "incoming-redteam.json"
        self.ledger.write_text(json.dumps({"claims": [{
            "id": "c1", "claim": "The transaction includes its index.", "type": "event",
            "source_urls": ["https://example.test/source"], "source_tiers": ["primary"],
            "as_of": "2026-08-29", "confidence": "high", "risk": "stable"
        }]}))
        self.verification.write_text("[]\n")
        self.redteam.write_text("[]\n")

    def tearDown(self):
        self.temp.cleanup()

    def _git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True, text=True, capture_output=True)

    def _finalize(self):
        return finalizer.finalize(
            self.repo, f"{self.stem}.html", self.ledger, self.verification, self.redteam
        )

    def test_full_writer_to_amended_commit_contains_ledger_and_derived_index(self):
        old_head = self._git("rev-parse", "HEAD").stdout.strip()
        self._finalize()
        new_head = self._git("rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(old_head, new_head)
        committed = self._git("show", "--name-only", "--format=").stdout.splitlines()
        self.assertIn(f"research/generative/{self.stem}.claims.json", committed)
        self.assertIn("research/claims/index.json", committed)
        payload = json.loads((self.repo / "research" / "claims" / "index.json").read_text())
        self.assertEqual(payload["article_count"], 1)
        self.assertEqual(payload["claim_count"], 1)
        self.assertEqual(self._git("status", "--porcelain").stdout, "")

    def test_commit_failure_rolls_back_every_transactional_file(self):
        old_head = self._git("rev-parse", "HEAD").stdout.strip()
        real_git = finalizer._git

        def fail_commit(repo, *args, **kwargs):
            if args[:2] == ("commit", "--amend"):
                raise subprocess.CalledProcessError(1, args)
            return real_git(repo, *args, **kwargs)

        with mock.patch.object(finalizer, "_git", side_effect=fail_commit):
            with self.assertRaises(subprocess.CalledProcessError):
                self._finalize()
        self.assertEqual(self._git("rev-parse", "HEAD").stdout.strip(), old_head)
        self.assertFalse((self.repo / "research" / "generative" / f"{self.stem}.claims.json").exists())
        self.assertEqual(json.loads((self.repo / "research" / "claims" / "index.json").read_text())["claim_count"], 0)
        self.assertEqual(self._git("status", "--porcelain").stdout, "")

    def test_refuses_dirty_owned_path_without_touching_unrelated_change(self):
        index = self.repo / "research" / "claims" / "index.json"
        index.write_text("user-owned dirty index\n")
        unrelated = self.repo / "notes.txt"
        unrelated.write_text("preserve me\n")
        with self.assertRaisesRegex(RuntimeError, "dirty transactional"):
            self._finalize()
        self.assertEqual(index.read_text(), "user-owned dirty index\n")
        self.assertEqual(unrelated.read_text(), "preserve me\n")

    def test_refuses_preexisting_staged_change_instead_of_amending_it(self):
        unrelated = self.repo / "notes.txt"
        unrelated.write_text("belongs to caller\n")
        self._git("add", "notes.txt")
        old_head = self._git("rev-parse", "HEAD").stdout.strip()
        with self.assertRaisesRegex(RuntimeError, "unrelated changes are already staged"):
            self._finalize()
        self.assertEqual(self._git("rev-parse", "HEAD").stdout.strip(), old_head)
        self.assertEqual(self._git("diff", "--cached", "--name-only").stdout.strip(), "notes.txt")
        self.assertEqual(unrelated.read_text(), "belongs to caller\n")


if __name__ == "__main__":
    unittest.main()
