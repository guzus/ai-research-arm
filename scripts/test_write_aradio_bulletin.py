#!/usr/bin/env python3
"""Tests for scripts/write_aradio_bulletin.py (the research/aradio/ committer)."""

from __future__ import annotations

import contextlib
import copy
import datetime as dt
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import check_aradio as ca
import write_aradio_bulletin as wb

NOW = dt.datetime(2026, 10, 30, 8, 50, tzinfo=dt.timezone.utc)
NOW_S = "2026-10-30T08:50:00Z"
URL_A = "https://x.com/a/status/1"
URL_B = "https://x.com/b/status/2"
EP_URL = "https://www.youtube.com/watch?v=frYSOKvNiiE"


def inbox() -> ca.TrustedInbox:
    return ca.TrustedInbox.from_obj({"schema": 1, "now": NOW_S, "items": [
        {"key": f"tw:{URL_A}", "kind": "twitter", "priority": False, "source": "X: @a",
         "title": "A", "url": URL_A, "at": "2026-10-30T00:00:00Z", "text": "a", "links": [URL_A]},
        {"key": f"tw:{URL_B}", "kind": "twitter", "priority": False, "source": "X: @b",
         "title": "B", "url": URL_B, "at": "2026-10-30T03:00:00Z", "text": "b", "links": [URL_B]},
        {"key": "ep:dwarkesh:frYSOKvNiiE", "kind": "podcast", "priority": True,
         "source": "Dwarkesh Podcast", "title": "Chips", "url": EP_URL,
         "at": "2026-10-29T16:00:00Z", "text": "notes", "links": [EP_URL]},
    ]})


def thread(slug: str, *, status: str = "developing", importance: int = 3,
           updated: str = "2026-10-29T08:50:00Z", evidence: list | None = None) -> dict:
    return {"slug": slug, "title": f"Title {slug}", "status": status,
            "importance": importance, "first_seen": "2026-10-20T08:50:00Z",
            "updated_at": updated, "now": f"Now {slug}.", "changed": f"Changed {slug}.",
            "watch": "", "evidence": evidence if evidence is not None else [],
            "history": [{"at": "2026-10-20T08:50:00Z", "change": f"Created {slug}."}]}


def script() -> list[str]:
    return [f"Speaker {1 if i % 2 == 0 else 2}: " + ("[high_energy] " if i == 0 else "")
            + " ".join(["word"] * 30) for i in range(12)]


def edit(ops: list[dict], *, on_air: bool = True, covers: list[str] | None = None) -> dict:
    return {"schema": 1, "on_air": on_air, "headline": "The situation, in one line",
            "ops": ops, "script": script() if on_air else [],
            "covers": (covers if covers is not None else [o["slug"] for o in ops[:1]])
            if on_air else [], "note": "" if on_air else "Nothing material."}


class WriterBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.lane = self.repo / "research" / "aradio"
        self.lane.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True,
                              capture_output=True, text=True).stdout

    def init_git(self) -> None:
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.repo / "README.md").write_text("readme\n", encoding="utf-8")
        self.git("add", "README.md")
        self.git("commit", "-q", "-m", "init")

    def board(self, threads: list[dict], headline: str = "old") -> None:
        ca.atomic_write_json(self.lane / "state.json", {
            "schema": 1, "updated_at": "2026-10-29T08:50:00Z", "headline": headline,
            "threads": threads})

    def state(self) -> dict:
        return json.loads((self.lane / "state.json").read_text(encoding="utf-8"))

    def threads(self) -> dict[str, dict]:
        return {t["slug"]: t for t in self.state()["threads"]}

    def write(self, raw_edit: dict, *, now: dt.datetime = NOW, tts: dict | None = None,
              key: str | None = None, error: str | None = None, commit: bool = False,
              the_inbox: ca.TrustedInbox | None = None) -> dict:
        return wb.write(repo_root=self.repo, edit_raw=raw_edit,
                        inbox=the_inbox or inbox(), now=now, tts_result=tts,
                        audio_key=key, audio_error=error, backend="cursor-grok-4p6-fast",
                        model="cursor-grok-4.6-high-fast", commit=commit)


class OpsTest(WriterBase):
    def test_create_update_resolve_semantics(self):
        old_evidence = [{"url": URL_B, "kind": "twitter", "label": "@b"}]
        self.board([thread("alpha", evidence=old_evidence), thread("beta"),
                    thread("gamma", updated="2026-10-29T09:00:00Z")])
        before_gamma = copy.deepcopy(self.threads()["gamma"])
        self.write(edit([
            {"op": "create", "slug": "delta", "title": "Delta", "status": "escalating",
             "importance": 5, "now": "N", "changed": "C", "watch": "W",
             "evidence": [{"url": EP_URL, "label": "Dwarkesh"}], "change": "Created delta."},
            {"op": "update", "slug": "alpha", "status": "steady", "changed": "Alpha moved.",
             "change": "Alpha update.", "add_evidence": [{"url": URL_A, "label": "@a"},
                                                         {"url": URL_B, "label": "dupe"}]},
            {"op": "resolve", "slug": "beta", "changed": "Over.", "change": "Beta resolved."},
        ], covers=["delta", "alpha", "beta"]))
        threads = self.threads()
        alpha = threads["alpha"]
        self.assertEqual("steady", alpha["status"])
        self.assertEqual(3, alpha["importance"])  # not named, not changed
        self.assertEqual("Now alpha.", alpha["now"])
        self.assertEqual([URL_A, URL_B], [e["url"] for e in alpha["evidence"]])
        self.assertEqual("@a", alpha["evidence"][0]["label"])
        # Prepend-then-dedupe: a re-cited URL is refreshed by its newest citation.
        self.assertEqual("dupe", alpha["evidence"][1]["label"])
        self.assertEqual([{"at": "2026-10-20T08:50:00Z", "change": "Created alpha."},
                          {"at": NOW_S, "change": "Alpha update."}], alpha["history"])
        self.assertEqual(NOW_S, alpha["updated_at"])
        self.assertEqual("2026-10-20T08:50:00Z", alpha["first_seen"])
        self.assertEqual("resolved", threads["beta"]["status"])
        self.assertEqual("Over.", threads["beta"]["changed"])
        delta = threads["delta"]
        self.assertEqual(NOW_S, delta["first_seen"])
        self.assertEqual([{"at": NOW_S, "change": "Created delta."}], delta["history"])
        self.assertEqual("podcast", delta["evidence"][0]["kind"])
        self.assertEqual(before_gamma, threads["gamma"])  # untouched

    def test_evidence_is_capped_at_eight_newest_first(self):
        old = [{"url": f"https://x.com/old/status/{i}", "kind": "twitter", "label": str(i)}
               for i in range(8)]
        self.board([thread("alpha", evidence=old)])
        self.write(edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "h",
                          "add_evidence": [{"url": URL_A, "label": "a"},
                                           {"url": URL_B, "label": "b"}]}]))
        urls = [e["url"] for e in self.threads()["alpha"]["evidence"]]
        self.assertEqual(8, len(urls))
        self.assertEqual([URL_A, URL_B], urls[:2])

    def test_ops_cannot_rewrite_history(self):
        self.board([thread("alpha")])
        original = copy.deepcopy(self.threads()["alpha"]["history"])
        self.write(edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "new",
                          "history": [{"at": "2020-01-01T00:00:00Z", "change": "forged"}],
                          "first_seen": "2020-01-01T00:00:00Z"}]))
        alpha = self.threads()["alpha"]
        self.assertEqual(original, alpha["history"][:1])
        self.assertEqual("new", alpha["history"][-1]["change"])
        self.assertEqual("2026-10-20T08:50:00Z", alpha["first_seen"])
        rewritten = copy.deepcopy(alpha)
        rewritten["history"][0]["change"] = "tampered"
        with self.assertRaises(wb.WriterError):
            wb.assert_history_append_only([alpha], [rewritten], [], [], NOW_S)

    def test_fabricated_evidence_is_dropped_on_revalidation(self):
        self.board([thread("alpha")])
        self.write(edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "h",
                          "add_evidence": [{"url": "https://evil.example/x", "label": "x"}]}]))
        self.assertEqual([], self.threads()["alpha"]["evidence"])

    def test_invalid_edit_is_rejected_before_anything_is_written(self):
        self.board([thread("alpha")])
        before = (self.lane / "state.json").read_bytes()
        with self.assertRaises(wb.WriterError):
            self.write(edit([{"op": "update", "slug": "ghost", "changed": "c", "change": "h"}]))
        self.assertEqual(before, (self.lane / "state.json").read_bytes())
        self.assertFalse((self.lane / "cursor.json").exists())


class BoundsTest(WriterBase):
    def test_quiet_threads_auto_resolve_and_old_resolved_threads_archive(self):
        self.board([thread("quiet", updated="2026-10-22T08:00:00Z"),
                    thread("done", status="resolved", updated="2026-10-21T08:00:00Z"),
                    thread("live")])
        self.write(edit([{"op": "update", "slug": "live", "changed": "c", "change": "h"}]))
        threads = self.threads()
        self.assertEqual("resolved", threads["quiet"]["status"])
        self.assertEqual(wb.QUIET_CHANGE, threads["quiet"]["history"][-1]["change"])
        self.assertNotIn("done", threads)
        archive = json.loads((self.lane / "archive" / "2026-10.json").read_text())
        self.assertEqual(["done"], [t["slug"] for t in archive["threads"]])
        self.assertEqual(NOW_S, archive["threads"][0]["archived_at"])

    def test_board_full_resolves_least_important_untouched_first(self):
        threads = [thread(f"t{i:02d}", importance=1 + (i % 5),
                          updated=f"2026-10-{24 + (i % 5):02d}T08:00:00Z") for i in range(12)]
        self.board(threads)
        # t00 is importance 1 and the oldest, but it is touched this run.
        self.write(edit([{"op": "update", "slug": "t00", "changed": "c", "change": "h"}]))
        live = [t for t in self.state()["threads"] if t["status"] != "resolved"]
        self.assertEqual(ca.MAX_UNRESOLVED, len(live))
        resolved = sorted(t["slug"] for t in self.state()["threads"]
                          if t["status"] == "resolved")
        self.assertEqual(["t05", "t10"], resolved)
        self.assertEqual(wb.FULL_CHANGE, self.threads()["t05"]["history"][-1]["change"])


def long_thread(slug: str, entries: int, **kwargs) -> dict:
    base = thread(slug, **kwargs)
    base["history"] = [{"at": f"2026-10-{1 + i // 24:02d}T{i % 24:02d}:00:00Z",
                        "change": f"{slug} step {i}"} for i in range(entries)]
    return base


def entries_of(rows: list[dict], slug: str) -> list[dict]:
    return [{k: v for k, v in row.items() if k not in wb.ARCHIVE_ROW_KEYS}
            for row in rows if row["slug"] == slug]


class HistoryBoundTest(WriterBase):
    """state.json keeps 12 history entries per thread; older ones are archived."""

    def archive(self) -> dict:
        return json.loads((self.lane / "archive" / "2026-10.json").read_text(encoding="utf-8"))

    def test_history_beyond_the_bound_moves_oldest_first_to_the_archive(self):
        prior = long_thread("alpha", 12)
        legacy = long_thread("legacy", 40, updated="2026-10-29T08:00:00Z")
        self.board([prior, legacy])
        summary = self.write(edit([{"op": "update", "slug": "alpha", "changed": "c",
                                    "change": "Alpha moved."}]))
        alpha = self.threads()["alpha"]["history"]
        kept_legacy = self.threads()["legacy"]["history"]
        appended = [{"at": NOW_S, "change": "Alpha moved."}]
        self.assertEqual(prior["history"][1:] + appended, alpha)
        self.assertEqual(legacy["history"][-wb.HISTORY_KEEP:], kept_legacy)
        rows = self.archive()["history"]
        self.assertEqual(1 + 28, len(rows))
        self.assertEqual(1 + 28, summary["history_archived"])
        for row in rows:
            self.assertEqual("2026-10-20T08:50:00Z", row["first_seen"])
            self.assertEqual(NOW_S, row["archived_at"])
        # Archived + retained == everything before + this run's entry, in order.
        self.assertEqual(prior["history"] + appended, entries_of(rows, "alpha") + alpha)
        self.assertEqual(legacy["history"], entries_of(rows, "legacy") + kept_legacy)
        self.assertEqual([], self.archive()["threads"])

    def test_trimmed_history_appends_to_an_existing_archive(self):
        earlier = {"slug": "old", "first_seen": "2026-10-01T00:00:00Z",
                   "at": "2026-10-02T00:00:00Z", "change": "kept verbatim",
                   "archived_at": "2026-10-03T00:00:00Z"}
        gone = thread("gone", status="resolved", updated="2026-10-05T00:00:00Z")
        ca.atomic_write_json(self.lane / "archive" / "2026-10.json", {
            "schema": 1, "month": "2026-10", "updated_at": "2026-10-03T00:00:00Z",
            "threads": [gone], "history": [earlier]})
        self.board([long_thread("alpha", 13)])
        self.write(edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "h"}]))
        archive = self.archive()
        self.assertEqual(earlier, archive["history"][0])
        self.assertEqual(["old", "alpha", "alpha"], [row["slug"] for row in archive["history"]])
        self.assertEqual(["gone"], [row["slug"] for row in archive["threads"]])

    def test_short_history_is_untouched_and_writes_no_archive(self):
        self.board([long_thread("alpha", 11)])
        self.write(edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "h"}]))
        self.assertEqual(wb.HISTORY_KEEP, len(self.threads()["alpha"]["history"]))
        self.assertFalse((self.lane / "archive").exists())

    def test_corrupt_archive_is_refused_not_overwritten(self):
        (self.lane / "archive").mkdir()
        (self.lane / "archive" / "2026-10.json").write_text("[]", encoding="utf-8")
        self.board([long_thread("alpha", 12)])
        before = (self.lane / "state.json").read_bytes()
        with self.assertRaises(wb.WriterError):
            self.write(edit([{"op": "update", "slug": "alpha", "changed": "c",
                              "change": "h"}]))
        self.assertEqual(before, (self.lane / "state.json").read_bytes())
        self.assertEqual("[]", (self.lane / "archive" / "2026-10.json").read_text())
        self.assertFalse((self.lane / "cursor.json").exists())

    def test_malformed_archive_is_refused_not_rewritten(self):
        # Reviewer probe: a dict-shaped `threads` was rewritten as [], and
        # non-object rows were dropped, silently losing archived content.
        row = thread("gone", status="resolved", updated="2026-10-05T00:00:00Z")
        good = {"schema": 1, "month": "2026-10", "updated_at": "2026-10-03T00:00:00Z",
                "threads": [row], "history": []}
        cases = {
            "threads is an object": dict(good, threads={"gone": row}),
            "threads is null": dict(good, threads=None),
            "a thread row is not an object": dict(good, threads=[row, "gone"]),
            "history is an object": dict(good, history={"0": {}}),
            "a history row is not an object": dict(good, history=[["at", "change"]]),
            "an unknown field would be dropped": dict(good, notes="hand-kept"),
            "another month's file": dict(good, month="2026-09"),
            "another schema": dict(good, schema=2),
            # Re-sanitizing used to drop this URL from the archived row.
            "a row that fails the URL rule": dict(good, threads=[dict(
                row, evidence=[{"url": "javascript:alert(1)", "kind": "twitter",
                                "label": "x"}])]),
        }
        for name, archive in cases.items():
            with self.subTest(name):
                self.lane.joinpath("cursor.json").unlink(missing_ok=True)
                ca.atomic_write_json(self.lane / "archive" / "2026-10.json", archive)
                written = (self.lane / "archive" / "2026-10.json").read_bytes()
                self.board([long_thread("alpha", 12)])
                before = (self.lane / "state.json").read_bytes()
                with self.assertRaises(wb.WriterError):
                    self.write(edit([{"op": "update", "slug": "alpha", "changed": "c",
                                      "change": "h"}]))
                self.assertEqual(before, (self.lane / "state.json").read_bytes())
                self.assertEqual(written, (self.lane / "archive" / "2026-10.json").read_bytes())
                self.assertFalse((self.lane / "cursor.json").exists())

    def test_existing_archive_rows_are_kept_verbatim(self):
        # Rows the writer itself would never produce (duplicate and > 8
        # evidence entries, no evidence key) are still not "repaired".
        crowded = thread("crowded", status="resolved", updated="2026-10-05T00:00:00Z",
                         evidence=[{"url": URL_A, "kind": "twitter", "label": f"a{i}"}
                                   for i in range(9)])
        bare = thread("bare", status="resolved", updated="2026-10-05T00:00:00Z")
        del bare["evidence"]
        history = [{"slug": "old", "first_seen": None, "at": "2026-10-02T00:00:00Z",
                    "change": "kept", "archived_at": "2026-10-03T00:00:00Z", "extra": [1]}]
        ca.atomic_write_json(self.lane / "archive" / "2026-10.json", {
            "schema": 1, "month": "2026-10", "updated_at": "2026-10-03T00:00:00Z",
            "threads": [crowded, bare], "history": history})
        self.board([long_thread("alpha", 12),
                    thread("done", status="resolved", updated="2026-10-20T00:00:00Z")])
        self.write(edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "h"}]))
        archive = self.archive()
        self.assertEqual([crowded, bare], archive["threads"][:2])
        self.assertEqual(["crowded", "bare", "done"], [t["slug"] for t in archive["threads"]])
        self.assertEqual(history, archive["history"][:1])
        self.assertEqual(["old", "alpha"], [r["slug"] for r in archive["history"]])

    def test_check_allows_an_archived_prefix(self):
        before = long_thread("alpha", 12)
        kept = copy.deepcopy(before)
        kept["history"].append({"at": NOW_S, "change": "new"})
        moved = wb.trim_history([kept], NOW)
        self.assertEqual(before["history"][:1], entries_of(moved, "alpha"))
        wb.assert_history_append_only([before], [kept], [], moved, NOW_S)  # no error

    def test_check_refuses_every_other_change_to_history(self):
        before = long_thread("alpha", 12)

        def trimmed() -> tuple[dict, list[dict]]:
            kept = copy.deepcopy(before)
            kept["history"].append({"at": NOW_S, "change": "new"})
            return kept, wb.trim_history([kept], NOW)

        cases = {}
        kept, moved = trimmed()
        kept["history"][0]["change"] = "edited"
        cases["edited retained entry"] = ([kept], moved, "rewritten")
        kept, moved = trimmed()
        moved[0]["change"] = "edited"
        cases["edited archived entry"] = ([kept], moved, "rewritten")
        kept, moved = trimmed()
        kept["history"][0], kept["history"][1] = kept["history"][1], kept["history"][0]
        cases["reordered"] = ([kept], moved, "rewritten")
        kept, moved = trimmed()
        cases["trimmed without archiving"] = ([kept], [], "rewritten")
        kept, moved = trimmed()
        del kept["history"][4]
        cases["middle entry dropped"] = ([kept], moved, "rewritten")
        kept, moved = trimmed()
        kept["history"].append({"at": "2026-10-29T00:00:00Z", "change": "backdated"})
        del kept["history"][0]
        moved.append(dict(moved[0], **before["history"][1]))  # keeps the prefix intact
        cases["entry this run did not make"] = ([kept], moved, "did not make")
        kept, moved = trimmed()
        moved[0]["archived_at"] = "2026-10-01T00:00:00Z"
        cases["archive row from another run"] = ([kept], moved, "not stamped by this run")
        kept, moved = trimmed()
        cases["rows for no thread"] = ([kept], moved + [dict(moved[0], slug="ghost")],
                                       "match no thread")
        kept, moved = trimmed()
        kept["first_seen"] = "2020-01-01T00:00:00Z"
        cases["identity changed"] = ([kept], moved, "first_seen")
        kept = copy.deepcopy(before)
        kept["history"].append({"at": NOW_S, "change": "new"})
        cases["kept beyond the bound"] = ([kept], [], "more than 12")
        cases["thread deleted"] = ([], [], "deleted")
        for name, (kept_threads, rows, reason) in cases.items():
            with self.subTest(name), self.assertRaisesRegex(wb.WriterError, reason):
                wb.assert_history_append_only([before], kept_threads, [], rows, NOW_S)

    def test_rerun_for_the_same_stamp_commits_the_archive_too(self):
        self.init_git()
        self.board([long_thread("alpha", 12)])
        self.git("add", "research/aradio/state.json")
        self.git("commit", "-q", "-m", "seed board")
        raw = edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "h"}])
        self.write(raw)  # applied, but the commit did not happen
        summary = self.write(raw, commit=True)
        self.assertTrue(summary["already_applied"])
        self.assertTrue(summary["committed"])
        files = sorted(self.git("show", "--name-only", "--format=", "HEAD").split())
        self.assertIn("research/aradio/archive/2026-10.json", files)
        self.assertIn("research/aradio/state.json", files)


class CursorAndIndexTest(WriterBase):
    def test_cursor_records_consumed_keys_and_prunes_old_ones(self):
        ca.atomic_write_json(self.lane / "cursor.json", {
            "schema": 1, "updated_at": "2026-10-29T08:50:00Z",
            "last_editor_run_at": "2026-10-29T08:50:00Z",
            "last_bulletin_at": "2026-10-28T08:50:00Z",
            "keys": {"tw:old": "2026-10-08T08:00:00Z", "tw:recent": "2026-10-25T08:00:00Z"}})
        self.board([thread("alpha")])
        self.write(edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "h"}],
                        on_air=False))
        cursor = json.loads((self.lane / "cursor.json").read_text())
        self.assertEqual(NOW_S, cursor["last_editor_run_at"])
        self.assertEqual("2026-10-28T08:50:00Z", cursor["last_bulletin_at"])  # off air
        self.assertNotIn("tw:old", cursor["keys"])
        self.assertEqual("2026-10-25T08:00:00Z", cursor["keys"]["tw:recent"])
        for key in inbox().keys():
            self.assertEqual(NOW_S, cursor["keys"][key])

    def test_off_air_run_creates_empty_index_once_and_no_bulletin(self):
        self.board([thread("alpha")])
        summary = self.write(edit([{"op": "update", "slug": "alpha", "changed": "c",
                                    "change": "h"}], on_air=False))
        self.assertFalse(summary["on_air"])
        index = json.loads((self.lane / "index.json").read_text())
        self.assertEqual({"schema": 1, "updated_at": NOW_S, "degraded": False,
                          "latest": None, "bulletins": []}, index)
        self.assertFalse((self.lane / "bulletins").exists())
        before = (self.lane / "index.json").read_bytes()
        later = NOW + dt.timedelta(hours=2)
        self.write(edit([{"op": "update", "slug": "alpha", "changed": "c2", "change": "h2"}],
                        on_air=False), now=later)
        self.assertEqual(before, (self.lane / "index.json").read_bytes())
        # state.json changes on every writer run, board-only runs included.
        self.assertEqual("2026-10-30T10:50:00Z", self.state()["updated_at"])

    def test_on_air_bulletin_with_audio(self):
        self.board([thread("alpha")])
        rows = [{"id": f"2026-10-2{i % 9}-{i:04d}", "aired_at": "2026-10-20T00:00:00Z",
                 "headline": "old", "path": "x", "audio": None, "covers": [], "kinds": []}
                for i in range(wb.MAX_INDEX)]
        ca.atomic_write_json(self.lane / "index.json", {
            "schema": 1, "updated_at": "x", "degraded": True, "latest": rows[0]["id"],
            "bulletins": rows})
        key = "audio/aradio/2026-10-30-0850.mp3"
        self.write(edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "h",
                          "add_evidence": [{"url": URL_A, "label": "@a"}]}]),
                   tts={"ok": True, "bytes": 123456, "duration_s": 201.37}, key=key)
        bulletin = json.loads((self.lane / "bulletins" / "2026-10-30" / "0850.json").read_text())
        self.assertEqual("2026-10-30-0850", bulletin["id"])
        self.assertEqual({"key": key, "bytes": 123456, "duration_s": 201.4}, bulletin["audio"])
        self.assertIsNone(bulletin["audio_error"])
        self.assertEqual([{"url": URL_A, "kind": "twitter", "label": "@a"}], bulletin["sources"])
        self.assertEqual([{"op": "update", "slug": "alpha"}], bulletin["ops"])
        self.assertEqual([{"slug": "alpha", "title": "Title alpha", "status": "developing"}],
                         bulletin["threads"])
        self.assertEqual({"items": 3, "kinds": {"podcast": 1, "twitter": 2}}, bulletin["inbox"])
        self.assertEqual({"backend": "cursor-grok-4p6-fast",
                          "model": "cursor-grok-4.6-high-fast"}, bulletin["editor"])
        self.assertTrue(bulletin["script"][0].startswith("Speaker 1: [high_energy]"))
        self.assertEqual("Speaker 1", bulletin["lines"][0]["speaker"])
        self.assertNotIn("[", bulletin["lines"][0]["text"])
        index = json.loads((self.lane / "index.json").read_text())
        self.assertFalse(index["degraded"])
        self.assertEqual("2026-10-30-0850", index["latest"])
        self.assertEqual(bulletin["id"], index["bulletins"][0]["id"])
        self.assertEqual(bulletin["audio"], index["bulletins"][0]["audio"])
        self.assertRegex(index["bulletins"][0]["audio"]["key"], wb.AUDIO_KEY_RE)
        self.assertEqual(wb.MAX_INDEX, len(index["bulletins"]))
        self.assertEqual("bulletins/2026-10-30/0850.json", index["bulletins"][0]["path"])
        self.assertEqual(["twitter"], index["bulletins"][0]["kinds"])
        cursor = json.loads((self.lane / "cursor.json").read_text())
        self.assertEqual(NOW_S, cursor["last_bulletin_at"])

    def test_on_air_bulletin_without_audio_is_degraded(self):
        self.board([thread("alpha")])
        self.write(edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "h"}]),
                   tts={"ok": False, "error": "Gemini TTS returned HTTP 400: bad"})
        bulletin = json.loads((self.lane / "bulletins" / "2026-10-30" / "0850.json").read_text())
        self.assertIsNone(bulletin["audio"])
        self.assertEqual("Gemini TTS returned HTTP 400: bad", bulletin["audio_error"])
        self.assertTrue(json.loads((self.lane / "index.json").read_text())["degraded"])

    def test_audio_outcomes(self):
        self.assertEqual((None, "TTS did not run"),
                         wb.audio_outcome(True, "2026-10-30-0850", None, None, None))
        self.assertEqual((None, "audio upload to S3 failed"),
                         wb.audio_outcome(True, "2026-10-30-0850",
                                          {"ok": True, "bytes": 1, "duration_s": 1.0},
                                          None, None))
        self.assertEqual((None, None), wb.audio_outcome(False, "x", None, None, None))
        with self.assertRaises(wb.WriterError):
            wb.audio_outcome(True, "2026-10-30-0850", {"ok": True, "bytes": 1,
                                                       "duration_s": 1.0},
                             "audio/aradio/other.mp3", None)


CRAFTED = [
    "https://a.example/x) [y](javascript:alert(1))",
    "javascript:alert(1)",
    "https://a.example/a b",
    "https://a.example/a\nb",
    'https://a.example/"q"',
    "https://a.example/<b>",
]


class UrlSafetyTest(WriterBase):
    def published(self) -> dict[str, str]:
        return {str(p.relative_to(self.lane)): p.read_text(encoding="utf-8")
                for p in sorted(self.lane.rglob("*.json"))}

    def test_unsafe_urls_never_reach_published_files(self):
        legacy = [{"url": url, "kind": "twitter", "label": "legacy"} for url in CRAFTED]
        legacy.append({"url": URL_B, "kind": "twitter", "label": "@b"})
        self.board([thread("alpha", evidence=legacy),
                    thread("old", status="resolved", updated="2026-10-20T08:00:00Z",
                           evidence=list(legacy))])
        tainted = ca.TrustedInbox.from_obj({"schema": 1, "items": [
            dict(item, links=item["links"] + CRAFTED) for item in inbox().items]})
        raw = edit([{"op": "update", "slug": "alpha",
                     "now": "Read [y](javascript:alert(1)) at https://a.example/z",
                     "changed": "c", "change": "h [x](javascript:alert(1))",
                     "add_evidence": [{"url": url, "label": "x"} for url in CRAFTED]
                     + [{"url": URL_A, "label": "[a](javascript:alert(1))"}]}])
        self.write(raw, the_inbox=tainted,
                   tts={"ok": True, "bytes": 10, "duration_s": 1.0},
                   key="audio/aradio/2026-10-30-0850.mp3")
        files = self.published()
        self.assertIn("archive/2026-10.json", files)
        for name, text in files.items():
            with self.subTest(file=name):
                self.assertNotIn("javascript", text)
                self.assertNotIn("a.example", text)
                self.assertEqual([], wb.unsafe_urls(json.loads(text)))
        evidence = self.threads()["alpha"]["evidence"]
        self.assertEqual([URL_A, URL_B], [entry["url"] for entry in evidence])

    def test_writer_refuses_to_publish_an_unsafe_url_it_did_not_sanitize(self):
        self.assertEqual(["$.threads[0].evidence[0].url"], wb.unsafe_urls(
            {"threads": [{"evidence": [{"url": "javascript:alert(1)"}]}]}))

    def test_audio_key_must_match_the_dashboard_pattern(self):
        good = "audio/aradio/2026-10-30-0850.mp3"
        self.assertRegex(good, wb.AUDIO_KEY_RE)
        for bad in ("audio/aradio/../x.mp3", "audio/2026-10-30-0850.mp3",
                    "/audio/aradio/2026-10-30-0850.mp3"):
            with self.subTest(key=bad), self.assertRaises(wb.WriterError):
                wb.audio_outcome(True, "2026-10-30-0850",
                                 {"ok": True, "bytes": 1, "duration_s": 1.0}, bad, None)


class GitAndIdempotenceTest(WriterBase):
    def test_commits_exact_paths_only(self):
        self.init_git()
        self.board([thread("alpha")])
        self.git("add", "research/aradio/state.json")
        self.git("commit", "-q", "-m", "seed board")
        (self.repo / "README.md").write_text("changed\n", encoding="utf-8")
        for stray in (".agent-input/aradio/inbox.md", ".tmp/aradio/edit.json"):
            (self.repo / stray).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / stray).write_text("untrusted\n", encoding="utf-8")
        summary = self.write(edit([{"op": "update", "slug": "alpha", "changed": "c",
                                    "change": "h"}]), commit=True)
        self.assertTrue(summary["committed"])
        subject = self.git("log", "-1", "--format=%s").strip()
        self.assertEqual("Aradio bulletin 2026-10-30 08:50 UTC", subject)
        files = sorted(self.git("show", "--name-only", "--format=", "HEAD").split())
        self.assertEqual(["research/aradio/bulletins/2026-10-30/0850.json",
                          "research/aradio/cursor.json", "research/aradio/index.json",
                          "research/aradio/state.json"], files)
        status = self.git("status", "--porcelain")
        self.assertIn(" M README.md", status)
        self.assertIn("?? .agent-input/", status)
        self.assertIn("?? .tmp/", status)

    def test_rerun_for_same_stamp_is_a_noop(self):
        self.init_git()
        self.board([thread("alpha")])
        raw = edit([{"op": "create", "slug": "new-story", "title": "T", "now": "N",
                     "changed": "C", "change": "Created."}], covers=["new-story"])
        self.write(raw, commit=True)
        head = self.git("rev-parse", "HEAD")
        snapshot = {p: p.read_bytes() for p in self.lane.rglob("*.json")}
        summary = self.write(raw, commit=True)
        self.assertTrue(summary["already_applied"])
        self.assertFalse(summary["committed"])
        self.assertEqual(head, self.git("rev-parse", "HEAD"))
        self.assertEqual(snapshot, {p: p.read_bytes() for p in self.lane.rglob("*.json")})

    def test_off_air_commit_message(self):
        self.init_git()
        self.board([thread("alpha")])
        self.write(edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "h"}],
                        on_air=False), commit=True)
        self.assertEqual("Aradio board update 2026-10-30 08:50 UTC",
                         self.git("log", "-1", "--format=%s").strip())

    def test_outputs_are_deterministic(self):
        raw = edit([{"op": "update", "slug": "alpha", "changed": "c", "change": "h",
                     "add_evidence": [{"url": URL_A, "label": "@a"}]}])
        outputs = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as tmp:
                self.repo = Path(tmp) / "repo"
                self.lane = self.repo / "research" / "aradio"
                self.lane.mkdir(parents=True)
                self.board([thread("alpha")])
                self.write(copy.deepcopy(raw))
                outputs.append({str(p.relative_to(self.lane)): p.read_bytes()
                                for p in sorted(self.lane.rglob("*.json"))})
        self.assertEqual(outputs[0], outputs[1])

    def test_bulletin_collision_is_refused(self):
        self.board([thread("alpha")])
        target = self.lane / "bulletins" / "2026-10-30" / "0850.json"
        target.parent.mkdir(parents=True)
        target.write_text("{}", encoding="utf-8")
        with self.assertRaises(wb.WriterError):
            self.write(edit([{"op": "update", "slug": "alpha", "changed": "c",
                              "change": "h"}]))

    def test_interrupted_write_leaves_no_partial_or_temp_files(self):
        self.board([thread("alpha")])
        real_replace = ca.os.replace

        def flaky(src, dst):
            if str(dst).endswith("cursor.json"):
                raise OSError("disk full")
            return real_replace(src, dst)

        with mock.patch.object(ca.os, "replace", side_effect=flaky):
            with self.assertRaises(OSError):
                self.write(edit([{"op": "update", "slug": "alpha", "changed": "c",
                                  "change": "h"}]))
        self.assertEqual([], [p.name for p in self.lane.rglob("*") if p.name.endswith(".tmp")])
        self.assertFalse((self.lane / "cursor.json").exists())
        for path in self.lane.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))  # every file is complete


class CliTest(WriterBase):
    def test_main_without_commit(self):
        self.board([thread("alpha")])
        edit_path = Path(self.tmp.name) / "edit.json"
        edit_path.write_text(json.dumps(edit([{"op": "update", "slug": "alpha",
                                               "changed": "c", "change": "h"}])))
        inbox_path = Path(self.tmp.name) / "inbox.json"
        inbox_path.write_text(json.dumps({"schema": 1, "items": inbox().items}))
        gh = Path(self.tmp.name) / "gh.txt"
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = wb.main(["--edit", str(edit_path), "--inbox", str(inbox_path),
                            "--now", NOW_S, "--repo-root", str(self.repo), "--no-commit",
                            "--audio-error", "GEMINI_API_KEY is not configured",
                            "--github-output", str(gh)])
        self.assertEqual(0, code, stdout.getvalue())
        self.assertIn("committed=false", gh.read_text())
        bulletin = json.loads((self.lane / "bulletins" / "2026-10-30" / "0850.json").read_text())
        self.assertEqual("GEMINI_API_KEY is not configured", bulletin["audio_error"])

    def test_main_rejects_unaligned_stamp(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            wb.main(["--edit", "x", "--inbox", "y", "--now", "2026-10-30T08:50:13Z"])


if __name__ == "__main__":
    unittest.main()
