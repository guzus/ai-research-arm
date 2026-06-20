#!/usr/bin/env python3

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import dedupe_headline_alerts as dedupe
import headline_judge as judge


def _write(path: Path, data) -> None:
    path.write_text(json.dumps(data))


class ShortlistTest(unittest.TestCase):
    def _run(self, to_send, history, **kw):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root / "to_send.json", to_send)
            _write(root / "history.json", history)
            argv = [
                "shortlist",
                "--to-send-file", str(root / "to_send.json"),
                "--history-file", str(root / "history.json"),
                "--out-file", str(root / "doubtful.json"),
            ]
            for k, v in kw.items():
                argv += [f"--{k.replace('_', '-')}", str(v)]
            with redirect_stdout(StringIO()):
                self.assertEqual(judge.main(argv), 0)
            return json.loads((root / "doubtful.json").read_text())

    def test_in_band_item_is_shortlisted_with_candidate(self):
        # Jaccard ~0.42, in [0.35,0.50): suspicious but below the 0.5 suppress floor.
        history = [
            dedupe.make_record(
                {
                    "headline": "CHINA ORDERS META TO UNWIND $2B MANUS AI DEAL — 100 STAFF ALREADY INSIDE",
                    "url": "https://x.com/a/status/1",
                },
                "2026-06-18 01:00 UTC",
            )
        ]
        to_send = [
            {
                "headline": "CHINA NDRC ORDERS META TO UNWIND $2B MANUS ACQUISITION — FIRST FORCED UNWIND",
                "url": "https://x.com/b/status/2",
                "category": "policy",
            }
        ]
        out = self._run(to_send, history)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["url"], "https://x.com/b/status/2")
        self.assertEqual(len(out[0]["candidates"]), 1)
        self.assertEqual(out[0]["candidates"][0]["url"], "https://x.com/a/status/1")

    def test_distinct_entity_pair_is_still_shortlisted(self):
        # Micron vs SK Hynix: same metric, different subject. Shortlist only
        # SURFACES it (in-band) — the judge, not the math, decides it's distinct.
        history = [
            dedupe.make_record(
                {
                    "headline": "SK HYNIX MARKET CAP CROSSES $900 BILLION ON HBM SUPER-CYCLE",
                    "url": "https://x.com/a/status/1",
                },
                "2026-06-18 01:00 UTC",
            )
        ]
        to_send = [
            {
                "headline": "MICRON MARKET CAP CROSSES $900B — JOINS SK HYNIX IN MEMORY SUPER-CYCLE MEGA-RALLY",
                "url": "https://x.com/b/status/2",
            }
        ]
        out = self._run(to_send, history)
        self.assertEqual(len(out), 1)

    def test_above_floor_is_not_shortlisted(self):
        # Jaccard >= 0.50 is the deterministic layer's job, not the judge's band.
        history = [
            dedupe.make_record(
                {"headline": "NEBIUS TO ACQUIRE EIGEN AI FOR $643M IN CASH AND SHARES", "url": "https://x.com/a/status/1"},
                "2026-06-18 01:00 UTC",
            )
        ]
        to_send = [
            {"headline": "NEBIUS ACQUIRES EIGEN AI FOR $643M CASH AND SHARES", "url": "https://x.com/b/status/2"}
        ]
        out = self._run(to_send, history)
        self.assertEqual(out, [])

    def test_below_band_is_not_shortlisted(self):
        history = [
            dedupe.make_record(
                {"headline": "OPENAI SHIPS GPT-5.6 WITH LIVE VIDEO", "url": "https://x.com/a/status/1"},
                "2026-06-18 01:00 UTC",
            )
        ]
        to_send = [
            {"headline": "MISTRAL OPEN-SOURCES A NEW 8B CODER MODEL", "url": "https://x.com/b/status/2"}
        ]
        out = self._run(to_send, history)
        self.assertEqual(out, [])

    def test_same_url_prior_is_excluded(self):
        history = [
            dedupe.make_record(
                {"headline": "ANTHROPIC ORBIT LEAK: PROACTIVE ASSISTANT FOR CLAUDE COWORK PULLING DATA", "url": "https://x.com/same/status/9"},
                "2026-06-18 01:00 UTC",
            )
        ]
        to_send = [
            {"headline": "ANTHROPIC ORBIT RE-LEAKED — PROACTIVE CLAUDE COWORK ASSISTANT AUTO-BRIEFING", "url": "https://x.com/same/status/9"}
        ]
        out = self._run(to_send, history)
        self.assertEqual(out, [])

    def test_candidates_ranked_and_capped(self):
        # Synthetic tokens with controlled overlap so four priors land at distinct
        # in-band Jaccards (0.444, 0.400, 0.385, 0.364) — lets us assert the
        # candidate list is sorted by descending similarity and capped.
        incoming = "AONE ATWO ATHREE AFOUR AFIVE ASIX ASEVEN AEIGHT"
        priors = [
            "AONE ATWO ATHREE AFOUR UAA",                       # 4/9  = 0.444
            "AONE ATWO ATHREE AFOUR UBB UBC",                   # 4/10 = 0.400
            "AONE ATWO ATHREE AFOUR AFIVE UCA UCB UCC UCD UCE", # 5/13 = 0.385
            "AONE ATWO ATHREE AFOUR UDA UDB UDC",               # 4/11 = 0.364
        ]
        history = [
            dedupe.make_record({"headline": h, "url": f"https://x.com/a/status/{i}"}, "2026-06-18 01:00 UTC")
            for i, h in enumerate(priors)
        ]
        to_send = [{"headline": incoming, "url": "https://x.com/b/status/99"}]
        out = self._run(to_send, history, max_candidates=3)
        self.assertEqual(len(out), 1)
        self.assertEqual(len(out[0]["candidates"]), 3)
        sims = [c["jaccard"] for c in out[0]["candidates"]]
        self.assertEqual(sims, sorted(sims, reverse=True))
        self.assertAlmostEqual(sims[0], 0.444, places=2)


class ApplyVerdictsTest(unittest.TestCase):
    def _run(self, to_send, verdicts, *, write_verdicts=True, raw_verdicts=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root / "to_send.json", to_send)
            vpath = root / "verdicts.json"
            if write_verdicts:
                if raw_verdicts is not None:
                    vpath.write_text(raw_verdicts)
                else:
                    _write(vpath, verdicts)
            argv = [
                "apply",
                "--to-send-file", str(root / "to_send.json"),
                "--verdicts-file", str(vpath),
                "--out-file", str(root / "out.json"),
                "--audit-file", str(root / "audit.jsonl"),
                "--timestamp", "2026-06-20 04:00 UTC",
            ]
            with redirect_stdout(StringIO()):
                self.assertEqual(judge.main(argv), 0)
            kept = json.loads((root / "out.json").read_text())
            audit = []
            if (root / "audit.jsonl").exists():
                audit = [json.loads(line) for line in (root / "audit.jsonl").read_text().splitlines() if line]
            return kept, audit

    def test_high_confidence_duplicate_is_dropped_and_audited(self):
        to_send = [
            {"headline": "A DUP", "url": "https://x.com/b/1", "category": "policy"},
            {"headline": "B KEEP", "url": "https://x.com/b/2"},
        ]
        verdicts = [
            {"url": "https://x.com/b/1", "verdict": "duplicate", "confidence": "high", "matched_url": "https://x.com/a/1", "reason": "same event"},
            {"url": "https://x.com/b/2", "verdict": "distinct", "confidence": "high"},
        ]
        kept, audit = self._run(to_send, verdicts)
        self.assertEqual([k["url"] for k in kept], ["https://x.com/b/2"])
        self.assertEqual(len(audit), 1)
        self.assertEqual(audit[0]["url"], "https://x.com/b/1")
        self.assertEqual(audit[0]["matched_url"], "https://x.com/a/1")
        self.assertEqual(audit[0]["reason"], "same event")

    def test_distinct_verdict_is_kept(self):
        to_send = [{"headline": "MICRON $900B", "url": "https://x.com/b/1"}]
        verdicts = [{"url": "https://x.com/b/1", "verdict": "distinct", "confidence": "high"}]
        kept, audit = self._run(to_send, verdicts)
        self.assertEqual(len(kept), 1)
        self.assertEqual(audit, [])

    def test_low_and_medium_confidence_duplicate_is_kept(self):
        # Default-keep: only HIGH-confidence duplicates are eaten.
        to_send = [
            {"headline": "MAYBE DUP 1", "url": "https://x.com/b/1"},
            {"headline": "MAYBE DUP 2", "url": "https://x.com/b/2"},
        ]
        verdicts = [
            {"url": "https://x.com/b/1", "verdict": "duplicate", "confidence": "medium"},
            {"url": "https://x.com/b/2", "verdict": "duplicate", "confidence": "low"},
        ]
        kept, audit = self._run(to_send, verdicts)
        self.assertEqual(len(kept), 2)
        self.assertEqual(audit, [])

    def test_missing_verdict_for_item_is_kept(self):
        to_send = [{"headline": "NO VERDICT", "url": "https://x.com/b/1"}]
        kept, _ = self._run(to_send, [])
        self.assertEqual(len(kept), 1)

    def test_missing_verdicts_file_fails_open(self):
        to_send = [{"headline": "X", "url": "https://x.com/b/1"}, {"headline": "Y", "url": "https://x.com/b/2"}]
        kept, audit = self._run(to_send, None, write_verdicts=False)
        self.assertEqual(len(kept), 2)
        self.assertEqual(audit, [])

    def test_malformed_verdicts_file_fails_open(self):
        to_send = [{"headline": "X", "url": "https://x.com/b/1"}]
        kept, _ = self._run(to_send, None, raw_verdicts="{not json at all")
        self.assertEqual(len(kept), 1)

    def test_verdicts_matched_by_url_not_index(self):
        # Verdicts arrive in a different order than to-send; the right item must drop.
        to_send = [
            {"headline": "FIRST KEEP", "url": "https://x.com/b/1"},
            {"headline": "SECOND DUP", "url": "https://x.com/b/2"},
        ]
        verdicts = [
            {"url": "https://x.com/b/2", "verdict": "duplicate", "confidence": "high"},
            {"url": "https://x.com/b/1", "verdict": "distinct", "confidence": "high"},
        ]
        kept, audit = self._run(to_send, verdicts)
        self.assertEqual([k["url"] for k in kept], ["https://x.com/b/1"])
        self.assertEqual(audit[0]["url"], "https://x.com/b/2")


if __name__ == "__main__":
    unittest.main()
