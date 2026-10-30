#!/usr/bin/env python3
"""Tests for scripts/check_aradio.py (the Aradio editor-artifact validator)."""

from __future__ import annotations

import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path

import check_aradio as ca

EP_URL = "https://www.youtube.com/watch?v=frYSOKvNiiE"
EP_EXCERPT_URL = "https://www.youtube.com/watch?v=frYSOKvNiiE&t=1234s"
TW_URL = "https://x.com/rohanpaul_ai/status/2115938869082542548"
TW_LINK = "https://x.com/AndrewCurran_/status/2115897550914158832"
EARN_URL = "https://www.sec.gov/Archives/edgar/data/1018724/000101872426000038/"
BOARD_URL = "https://x.com/old/status/1"


def inbox_obj() -> dict:
    return {"schema": 1, "now": "2026-10-30T08:50:00Z", "items": [
        {"key": "ep:dwarkesh:frYSOKvNiiE", "kind": "podcast", "priority": True,
         "source": "Dwarkesh Podcast", "title": "What will chips look like in 2045?",
         "url": EP_URL, "at": "2026-10-22T16:00:00Z",
         "text": "Show notes about the semiconductor cycle.",
         "links": [EP_URL, EP_EXCERPT_URL], "transcript_file": "transcripts/1.txt",
         "transcript_source": "transcript"},
        {"key": f"tw:{TW_URL}", "kind": "twitter", "priority": False,
         "source": "X: @rohanpaul_ai", "title": "Anthropic is SpaceX's largest customer",
         "url": TW_URL, "at": "2026-10-30T00:00:00Z",
         "text": "SpaceX's filing names an anonymous \"Customer B\" as 34.5% of revenue.",
         "links": [TW_URL, TW_LINK]},
        {"key": "earn:0001018724-26-000038", "kind": "earnings", "priority": True,
         "source": "Amazon.com, Inc. (AMZN)", "title": "Amazon Q3",
         "url": EARN_URL, "at": "2026-10-29T20:05:27Z",
         "text": "Key quotes:\n- Andy Jassy: “There has never been a trillion dollar "
                 "revenue business, and we may have two of them.”",
         "links": [EARN_URL]},
    ]}


TRANSCRIPT = ("[20:34] There's never been as big a shock to the semiconductor industry "
              "as the current surge in demand from AI.\n"
              "[41:10] Easily 40-50% above our maximum capacity, which I've never seen before.\n")


def board_obj() -> dict:
    return {"schema": 1, "updated_at": "2026-10-29T08:50:00Z", "headline": "old",
            "threads": [
                {"slug": "hbm-shortage", "title": "The HBM crunch", "status": "developing",
                 "importance": 4, "first_seen": "2026-10-20T08:50:00Z",
                 "updated_at": "2026-10-29T08:50:00Z", "now": "Tight.", "changed": "x",
                 "watch": "y", "evidence": [{"url": BOARD_URL, "kind": "twitter",
                                             "label": "@old", "at": "2026-10-20T00:00:00Z"}],
                 "history": [{"at": "2026-10-20T08:50:00Z", "change": "Created."}]},
                {"slug": "devday-launches", "title": "DevDay", "status": "resolved",
                 "importance": 2, "first_seen": "2026-10-10T08:50:00Z",
                 "updated_at": "2026-10-25T08:50:00Z", "now": "Done.", "changed": "x",
                 "watch": "", "evidence": [], "history": [
                     {"at": "2026-10-10T08:50:00Z", "change": "Created."}]},
            ]}


def script(lines: int = 12, words_per_line: int = 30) -> list[str]:
    out = []
    for index in range(lines):
        speaker = 1 if index % 2 == 0 else 2
        out.append(f"Speaker {speaker}: " + " ".join(["word"] * words_per_line))
    return out


def edit_obj(**overrides) -> dict:
    edit = {
        "schema": 1,
        "on_air": True,
        "headline": "Chips, compute and capex",
        "ops": [
            {"op": "create", "slug": "anthropic-compute", "title": "Anthropic's compute",
             "status": "developing", "importance": 5, "now": "Anthropic is renting.",
             "changed": "Named as SpaceX's top customer.", "watch": "Confirmation.",
             "evidence": [{"url": TW_URL, "label": "@rohanpaul_ai on X", "kind": "earnings"}],
             "change": "Created."},
            {"op": "update", "slug": "hbm-shortage", "changed": "Supply still short.",
             "change": "Dwarkesh guest on capacity.",
             "add_evidence": [{"url": EP_URL, "label": "Dwarkesh Podcast",
                               "speaker": "Guest",
                               "quote": "Easily 40-50% above our maximum capacity"}]},
            {"op": "resolve", "slug": "devday-launches", "changed": "Absorbed.",
             "change": "Resolved."},
        ],
        "script": script(),
        "covers": ["anthropic-compute", "hbm-shortage"],
        "note": "",
    }
    edit.update(overrides)
    return edit


class ValidatorBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "trusted" / "transcripts").mkdir(parents=True)
        (self.root / "trusted" / "transcripts" / "1.txt").write_text(TRANSCRIPT, encoding="utf-8")
        (self.root / "trusted" / "inbox.json").write_text(json.dumps(inbox_obj()),
                                                          encoding="utf-8")
        self.inbox = ca.TrustedInbox.load(self.root / "trusted" / "inbox.json")
        self.board = board_obj()

    def tearDown(self):
        self.tmp.cleanup()

    def validate(self, edit, board=None):
        return ca.validate_edit(edit, self.inbox, self.board if board is None else board)

    def assertHard(self, edit, fragment, board=None):
        normalized, report = self.validate(edit, board)
        self.assertIsNone(normalized, report.warnings)
        self.assertTrue(any(fragment in error for error in report.errors), report.errors)


class ValidEditTest(ValidatorBase):
    def test_valid_edit_is_normalized_with_trusted_kinds(self):
        normalized, report = self.validate(edit_obj())
        self.assertEqual([], report.errors)
        self.assertIsNotNone(normalized)
        create = normalized["ops"][0]
        self.assertEqual("twitter", create["evidence"][0]["kind"])  # editor said earnings
        self.assertEqual("2026-10-30T00:00:00Z", create["evidence"][0]["at"])
        update = normalized["ops"][1]
        self.assertEqual("podcast", update["add_evidence"][0]["kind"])
        self.assertEqual("Easily 40-50% above our maximum capacity",
                         update["add_evidence"][0]["quote"])
        self.assertEqual(["anthropic-compute", "hbm-shortage"], normalized["covers"])
        self.assertEqual(12, normalized["stats"]["script_lines"])
        self.assertEqual(360, normalized["stats"]["script_words"])

    def test_normalization_is_idempotent(self):
        first, _ = self.validate(edit_obj())
        second, report = self.validate(copy.deepcopy(first))
        self.assertEqual([], report.errors)
        for key in ("ops", "script", "covers", "headline", "on_air", "note"):
            self.assertEqual(first[key], second[key], key)

    def test_create_then_update_same_slug_in_one_edit(self):
        edit = edit_obj()
        edit["ops"].append({"op": "update", "slug": "anthropic-compute",
                            "changed": "More.", "change": "Follow-up."})
        normalized, report = self.validate(edit)
        self.assertEqual([], report.errors)
        self.assertEqual(4, len(normalized["ops"]))

    def test_on_air_false_drops_script_and_covers(self):
        normalized, report = self.validate(edit_obj(on_air=False, note="Nothing material."))
        self.assertEqual([], report.errors)
        self.assertEqual([], normalized["script"])
        self.assertEqual([], normalized["covers"])
        self.assertTrue(any("script ignored" in w for w in report.warnings))

    def test_update_evidence_alias_is_repaired(self):
        edit = edit_obj()
        edit["ops"][1]["evidence"] = edit["ops"][1].pop("add_evidence")
        normalized, report = self.validate(edit)
        self.assertEqual([], report.errors)
        self.assertEqual(EP_URL, normalized["ops"][1]["add_evidence"][0]["url"])
        self.assertTrue(any("treated as add_evidence" in w for w in report.warnings))


class ProvenanceTest(ValidatorBase):
    def evidence_after(self, evidence):
        edit = edit_obj()
        edit["ops"][0]["evidence"] = evidence
        normalized, report = self.validate(edit)
        self.assertEqual([], report.errors)
        return normalized["ops"][0]["evidence"], report

    def test_url_not_in_inbox_or_board_is_dropped(self):
        evidence, report = self.evidence_after([
            {"url": "https://example.com/fabricated", "label": "Fake"},
            {"url": TW_URL + "?s=20", "label": "Altered"},
            {"url": TW_LINK, "label": "Linked"},
        ])
        self.assertEqual([TW_LINK], [e["url"] for e in evidence])
        self.assertEqual(2, sum("not in this run's inbox" in w for w in report.warnings))

    def test_board_url_is_allowed_and_keeps_board_kind(self):
        evidence, _ = self.evidence_after([{"url": BOARD_URL, "label": "Again"}])
        self.assertEqual("twitter", evidence[0]["kind"])
        self.assertEqual("2026-10-20T00:00:00Z", evidence[0]["at"])

    def test_quote_must_be_verbatim_and_short(self):
        long_quote = " ".join(["capacity"] * 41)
        evidence, report = self.evidence_after([
            {"url": EP_URL, "label": "a", "quote": "We will triple capacity next year"},
            {"url": EP_EXCERPT_URL, "label": "b", "quote": long_quote},
            {"url": EARN_URL, "label": "c",
             "quote": "there has never been a trillion-dollar revenue business"},
        ])
        self.assertNotIn("quote", evidence[0])
        self.assertNotIn("quote", evidence[1])
        self.assertIn("quote", evidence[2])  # case, dash and quote marks are folded
        self.assertTrue(any("not found verbatim" in w for w in report.warnings))
        self.assertTrue(any("over 40 words" in w for w in report.warnings))

    def test_stitched_quotes_are_dropped(self):
        # Every one of these is assembled from words that really occur in the
        # source, so a whole-haystack or fragment-by-fragment match passes
        # them; none is a sentence anyone said.
        cases = {
            "ellipsis joining two real fragments of one sentence": (
                EARN_URL, "there has never been a trillion-dollar revenue business ... "
                          "we may have two of them"),
            "ellipsis gluing short fragments from different windows": (
                EP_URL, "never been … seen before"),
            "no ellipsis, bridging two transcript windows 20 minutes apart": (
                EP_URL, "the current surge in demand from AI. Easily 40-50% above our "
                        "maximum capacity"),
            "no ellipsis, bridging two separate lines of item text": (
                EARN_URL, "Key quotes: Andy Jassy: There has never been"),
        }
        for name, (url, quote) in cases.items():
            with self.subTest(name):
                evidence, report = self.evidence_after([{"url": url, "label": "x", "quote": quote}])
                self.assertNotIn("quote", evidence[0])
                self.assertTrue(any("not found verbatim" in w for w in report.warnings))

    def test_quote_within_one_window_survives(self):
        evidence, _ = self.evidence_after([
            {"url": EP_URL, "label": "a",
             "quote": "Easily 40-50% above our maximum capacity, which I've never seen before."}])
        self.assertIn("quote", evidence[0])

    def test_transcript_window_quote_is_verified(self):
        evidence, _ = self.evidence_after([
            {"url": EP_URL, "label": "Dwarkesh",
             "quote": "There's never been as big a shock to the semiconductor industry"}])
        self.assertIn("quote", evidence[0])

    def test_label_defaults_to_trusted_source(self):
        evidence, _ = self.evidence_after([{"url": EARN_URL, "label": ""}])
        self.assertEqual("Amazon.com, Inc. (AMZN)", evidence[0]["label"])

    def test_evidence_is_capped_and_deduped(self):
        evidence, _ = self.evidence_after([{"url": TW_URL, "label": "x"}] * 3)
        self.assertEqual(1, len(evidence))


CRAFTED_URLS = [
    "https://a.example/x) [y](javascript:alert(1))",
    "javascript:alert(1)",
    "https://a.example/a b",
    "https://a.example/a\nb",
    'https://a.example/"q"',
    "https://a.example/'q'",
    "https://a.example/<script>",
    "https://a.example/x‮",
    "https:///no-host",
    "ftp://a.example/file",
    "https://a.example/" + "x" * 2048,
]


class UrlSafetyTest(ValidatorBase):
    def test_safe_url_rule(self):
        for url in CRAFTED_URLS:
            with self.subTest(url=url):
                self.assertIsNone(ca.safe_url(url))
        for url in (TW_URL, EP_EXCERPT_URL, "http://a.example/p?q=1&r=2#frag"):
            self.assertEqual(url, ca.safe_url(url))

    def test_unsafe_evidence_url_is_dropped_even_when_the_inbox_lists_it(self):
        obj = inbox_obj()
        obj["items"][1]["links"] = [TW_URL] + CRAFTED_URLS
        self.inbox = ca.TrustedInbox.from_obj(obj, base_dir=self.root / "trusted")
        edit = edit_obj()
        edit["ops"][0]["evidence"] = ([{"url": url, "label": "x"} for url in CRAFTED_URLS]
                                      + [{"url": f"<{TW_URL}>", "label": "autolink"}])
        normalized, report = self.validate(edit)
        self.assertEqual([], report.errors)
        evidence = normalized["ops"][0]["evidence"]
        self.assertEqual([TW_URL], [entry["url"] for entry in evidence])
        self.assertTrue(any("unsafe URL dropped" in w for w in report.warnings))
        self.assertNotIn("javascript", json.dumps(normalized))

    def test_link_syntax_and_urls_are_stripped_from_prose(self):
        edit = edit_obj(headline="Big day [y](javascript:alert(1)) https://a.example/x",
                        note="")
        edit["ops"][0]["now"] = "See https://a.example/x) [y](javascript:alert(1)) now."
        edit["ops"][0]["evidence"] = [{"url": TW_URL, "label": "[x](javascript:alert(1))",
                                       "quote": "34.5% javascript:alert(1)"}]
        lines = script()
        lines[2] = "Speaker 1: Read more at [this](javascript:alert(1)) " + " ".join(
            ["word"] * 28)
        edit["script"] = lines
        normalized, report = self.validate(edit)
        self.assertEqual([], report.errors)
        rendered = json.dumps(normalized)
        self.assertNotIn("javascript", rendered)
        self.assertNotIn("a.example", rendered)
        self.assertEqual("Big day y", normalized["headline"])
        self.assertNotIn("quote", normalized["ops"][0]["evidence"][0])


class HardErrorTest(ValidatorBase):
    def test_not_an_object(self):
        self.assertHard([1, 2], "JSON object")

    def test_schema(self):
        self.assertHard(edit_obj(schema=2), "schema")
        self.assertHard(edit_obj(schema=True), "schema")

    def test_unknown_op(self):
        edit = edit_obj()
        edit["ops"].append({"op": "delete", "slug": "hbm-shortage"})
        self.assertHard(edit, "unknown op")

    def test_create_existing_slug(self):
        edit = edit_obj()
        edit["ops"][0]["slug"] = "hbm-shortage"
        self.assertHard(edit, "already exists")

    def test_malformed_slugs(self):
        for slug in ("Anthropic-IPO", "a--b", "-a", "a" * 65, "a_b", ""):
            edit = edit_obj()
            edit["ops"][0]["slug"] = slug
            with self.subTest(slug=slug):
                self.assertHard(edit, "malformed slug")

    def test_update_and_resolve_unknown_slug(self):
        for op in ("update", "resolve"):
            edit = edit_obj()
            edit["ops"] = [{"op": op, "slug": "never-seen", "changed": "x", "change": "y"}]
            edit["covers"] = ["hbm-shortage"]
            with self.subTest(op=op):
                self.assertHard(edit, "unknown slug")

    def test_more_than_three_creates(self):
        edit = edit_obj()
        edit["ops"] = [dict(edit["ops"][0], slug=f"story-{i}") for i in range(4)]
        edit["covers"] = ["story-0"]
        self.assertHard(edit, "at most 3")

    def test_missing_required_fields(self):
        edit = edit_obj()
        del edit["ops"][1]["change"]
        self.assertHard(edit, "missing required field 'change'")

    def test_on_air_needs_a_well_formed_script(self):
        self.assertHard(edit_obj(script=None), "requires script")
        bad = script()
        bad[3] = "Host: hello there"
        self.assertHard(edit_obj(script=bad), "does not start with")
        self.assertHard(edit_obj(script=script(lines=7, words_per_line=40)), "7 lines")
        self.assertHard(edit_obj(script=script(lines=31, words_per_line=10)), "31 lines")
        self.assertHard(edit_obj(script=script(lines=10, words_per_line=20)),
                        "200 spoken words")
        self.assertHard(edit_obj(script=script(lines=20, words_per_line=46)),
                        "920 spoken words")

    def test_covers_must_be_on_board_after_ops(self):
        self.assertHard(edit_obj(covers=["anthropic-compute", "ghost-story"]),
                        "not on the board")

    def test_read_edit_file_rejects_invalid_json_and_symlinks(self):
        bad = self.root / "edit.json"
        bad.write_text("{not json", encoding="utf-8")
        with self.assertRaises(ValueError):
            ca.read_edit_file(bad)
        link = self.root / "link.json"
        link.symlink_to(bad)
        with self.assertRaises(ValueError):
            ca.read_edit_file(link)
        big = self.root / "big.json"
        big.write_bytes(b" " * (ca.MAX_EDIT_BYTES + 1))
        with self.assertRaises(ValueError):
            ca.read_edit_file(big)


class SoftRepairTest(ValidatorBase):
    def test_long_fields_are_truncated(self):
        edit = edit_obj(headline="H" * 200)
        edit["ops"][0]["now"] = "word " * 200
        normalized, report = self.validate(edit)
        self.assertEqual([], report.errors)
        self.assertLessEqual(len(normalized["headline"]), ca.HEADLINE_MAX)
        self.assertLessEqual(len(normalized["ops"][0]["now"]), ca.TEXT_LIMITS["now"])
        self.assertTrue(normalized["ops"][0]["now"].endswith("…"))

    def test_script_urls_unknown_and_excess_tags_are_stripped(self):
        lines = script()
        lines[0] = ("Speaker 1: [high_energy] Welcome [laughs] to the show "
                    "https://evil.example/x <cough> " + " ".join(["word"] * 26))
        lines[1] = ("Speaker 2: [high_energy] again [emphasis]one[/emphasis] "
                    "[emphasis]two[/emphasis] [emphasis]three[/emphasis] "
                    "[emphasis]four[/emphasis] " + " ".join(["word"] * 26))
        normalized, report = self.validate(edit_obj(script=lines))
        self.assertEqual([], report.errors)
        first, second = normalized["script"][0], normalized["script"][1]
        self.assertNotIn("http", first)
        self.assertNotIn("[laughs]", first)
        self.assertNotIn("<cough>", first)
        self.assertIn("[high_energy]", first)
        self.assertNotIn("[high_energy]", second)  # only one per script
        self.assertEqual(3, second.count("[emphasis]"))
        self.assertEqual(3, second.count("[/emphasis]"))
        joined = " ".join(report.warnings)
        self.assertIn("URL stripped", joined)
        self.assertIn("unknown audio tag", joined)

    def test_unknown_fields_and_invalid_values_are_repaired(self):
        edit = edit_obj(extra="ignored")
        edit["ops"][0].update({"importance": 9, "status": "exploding", "history": []})
        normalized, report = self.validate(edit)
        self.assertEqual([], report.errors)
        create = normalized["ops"][0]
        self.assertEqual(5, create["importance"])
        self.assertEqual("developing", create["status"])
        self.assertNotIn("history", create)
        self.assertNotIn("extra", normalized)

    def test_injection_text_stays_data_and_is_escaped_for_workflow_logs(self):
        edit = edit_obj()
        edit["ops"][0]["evidence"] = [{"url": "https://evil.example/\n::stop-commands::x",
                                       "label": "x"}]
        normalized, report = self.validate(edit)
        self.assertEqual([], report.errors)
        self.assertEqual([], normalized["ops"][0]["evidence"])
        for warning in report.warnings:
            escaped = ca.gh_escape(warning)
            self.assertNotIn("\n", escaped)


class CliTest(ValidatorBase):
    def run_cli(self, edit) -> tuple[int, str, Path, Path]:
        edit_path = self.root / "edit.json"
        edit_path.write_text(json.dumps(edit), encoding="utf-8")
        state = self.root / "state.json"
        state.write_text(json.dumps(self.board), encoding="utf-8")
        out = self.root / "normalized.json"
        gh = self.root / "gh.txt"
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = ca.main(["--edit", str(edit_path), "--inbox",
                            str(self.root / "trusted" / "inbox.json"), "--state", str(state),
                            "--out", str(out), "--github-output", str(gh)])
        return code, buffer.getvalue(), out, gh

    def test_ok_writes_normalized_edit_and_outputs(self):
        code, _, out, gh = self.run_cli(edit_obj())
        self.assertEqual(0, code)
        self.assertTrue(json.loads(out.read_text())["on_air"])
        self.assertIn("on_air=true", gh.read_text())

    def test_hard_error_exits_one_and_writes_nothing(self):
        edit = edit_obj()
        edit["ops"][0]["slug"] = "line\n::error::injected"
        code, stdout, out, _ = self.run_cli(edit)
        self.assertEqual(1, code)
        self.assertFalse(out.exists())
        for line in stdout.splitlines():
            if line.startswith("::"):
                self.assertTrue(line.startswith(("::error::aradio", "::warning::aradio")), line)

    def test_missing_state_means_empty_board(self):
        edit = edit_obj(ops=[edit_obj()["ops"][0]], covers=["anthropic-compute"])
        edit_path = self.root / "edit.json"
        edit_path.write_text(json.dumps(edit), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            code = ca.main(["--edit", str(edit_path), "--inbox",
                            str(self.root / "trusted" / "inbox.json"), "--state",
                            str(self.root / "absent.json"), "--out",
                            str(self.root / "n.json")])
        self.assertEqual(0, code)


class HelperTest(unittest.TestCase):
    def test_spoken_words_ignore_tags_and_prefix(self):
        line = "Speaker 1: [high_energy] Ten [emphasis]billion[/emphasis] dollars."
        self.assertEqual("Ten billion dollars.", ca.spoken_text(line))
        self.assertEqual(3, ca.count_spoken_words([line]))

    def test_strip_audio_tags_does_not_leave_space_before_punctuation(self):
        self.assertEqual("five dollars, up", ca.strip_audio_tags(
            "[emphasis]five dollars[/emphasis], up"))

    def test_gh_escape(self):
        self.assertEqual("a%0A::x%25", ca.gh_escape("a\n::x%"))

    def test_clip_prefers_word_boundary(self):
        text, cut = ca.clip("alpha beta gamma delta", 15)
        self.assertTrue(cut)
        self.assertEqual("alpha beta…", text)


if __name__ == "__main__":
    unittest.main()
