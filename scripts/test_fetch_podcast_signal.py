#!/usr/bin/env python3
"""Tests for the Aradio spoken-media source lane (scripts/fetch_podcast_signal.py).

The network boundary is a fake tuber transport; no test touches the network.
"""

from __future__ import annotations

import copy
import datetime as dt
import io
import json
import os
import re
import sys
import tempfile
import unittest
import unittest.mock
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import fetch_podcast_signal as pod  # noqa: E402

NOW = dt.datetime(2026, 10, 30, 8, 41, tzinfo=dt.timezone.utc)
CH_LAB = "UC" + "L" * 22
CH_POD = "UC" + "P" * 22
CH_CALL = "UC" + "C" * 22
CH_OTHER = "UC" + "X" * 22
RSS = "https://feeds.example.test/show.rss"
SEARCH_Q = "Acme earnings call"


def vid(number: int) -> str:
    return f"vid{number:08d}"  # 11 characters, like a YouTube id


def token(number: int) -> str:
    """A unique, digit-free word so filler text adds no numeric signal."""
    letters = []
    number += 1
    while number:
        number, rest = divmod(number - 1, 26)
        letters.append(chr(97 + rest))
    return "zq" + "".join(reversed(letters))


def filler_sentence(number: int) -> str:
    return f"We chatted about {token(number)} and the weather and gardens in general terms."


def filler_segments(count: int, *, step_ms: int = 5000, start: int = 0) -> list[dict]:
    return [{"startMs": (start + i) * step_ms, "text": filler_sentence(start + i)} for i in range(count)]


INFORMATIVE = ("Our data center capacity will double next year to 2 gigawatts, and we expect "
               "revenue growth of 30% as Nvidia GPU supply improves.")
SPONSOR_READ = ("This episode is sponsored by Acme Cloud. Acme serves 3,000 enterprise customers "
                "and cut GPU costs 40% for $5 million in savings. Use code AI50 and go to "
                "acme.com/podcast for a free trial.")


def show_row(**overrides) -> dict:
    row = {"id": "lab", "name": "Lab", "kind": "channel", "channel_id": CH_LAB, "priority": "P0",
           "tags": ["official", "frontier-lab"], "ai_filter": False, "min_duration_s": 90,
           "include_in_aradio": True}
    row.update(overrides)
    return row


def e2e_shows() -> list[dict]:
    return [
        show_row(),
        show_row(id="pod", name="Pod Show", channel_id=CH_POD, priority="P1", tags=["interviews"],
                 ai_filter=True, min_duration_s=900),
        show_row(id="acme-call", name="Acme earnings call", kind="search", query=SEARCH_Q,
                 channel_id=CH_CALL, tags=["official", "earnings-call"], min_duration_s=1800),
        {"id": "notes", "name": "Notes FM", "kind": "podcast", "rss": RSS, "priority": "P2",
         "tags": ["research", "audio-only"], "ai_filter": False, "min_duration_s": 300,
         "include_in_aradio": True},
    ]


def write_registry(directory: Path, shows: list[dict]) -> Path:
    path = directory / "podcasts.json"
    path.write_text(json.dumps({"schema": 1, "shows": shows}), encoding="utf-8")
    return path


def video_row(number: int, title: str, label: str, duration, **extra) -> dict:
    row = {"id": vid(number), "title": title, "publishedAt": label, "duration": duration,
           "views": "1K", "isSummarized": False}
    row.update(extra)
    return row


def transcript_payload(segments, *, source="youtube_captions", language="en") -> dict:
    return {"segments": segments, "languages": [], "language": language, "source": source}


RATE_LIMITED = pod.TuberError("HTTP 500: YouTube temporarily rate-limited transcript access",
                              status=500, rate_limited=True)


def e2e_routes() -> dict:
    lab_transcript = filler_segments(60) + [{"startMs": 300_000, "text": INFORMATIVE}] + filler_segments(60, start=61)
    call_transcript = filler_segments(400, step_ms=9000) + [{"startMs": 3_610_000, "text": INFORMATIVE}]
    return {
        f"/channel/{CH_LAB}": {"name": "Lab", "videos": [
            video_row(1, "Introducing Model X", "3h ago", 600),
            video_row(2, "Model X in 30 seconds", "1h ago", 30),
            video_row(3, "An older launch", "3w ago", 900),
        ]},
        f"/channel/{CH_POD}": {"name": "Pod", "videos": [
            video_row(4, "Scaling AI agents with Jane", "5h ago", 3600),
            video_row(5, "Gardening with Bob", "6h ago", 3600),
            video_row(6, "A conversation with Sam", "7h ago", 3600),
            video_row(7, "History of Rome", "8h ago", 3600),
        ]},
        ("/search", SEARCH_Q): {"query": SEARCH_Q, "videos": [
            video_row(8, "Acme Q3 2026 Earnings Call", "Streamed 2h ago", 3700, channelId=CH_CALL, isLive=False),
            video_row(9, "LIVE: Acme earnings call watch party", "Streamed 2h ago", 3700,
                      channelId=CH_OTHER, isLive=False),
            video_row(10, "Acme Q3 call (live now)", "", 0, channelId=CH_CALL, isLive=True),
        ]},
        ("/podcast/episodes", RSS): {"showName": "", "rssUrl": RSS, "episodes": [
            {"id": "pod-abc123", "title": "Weekly notes on model evals",
             "description": "Evals are hard. Follow us on X: https://x.com/notes",
             "audioUrl": "https://cdn.example.test/ep1.mp3",
             "publishedAt": "Wed, 28 Oct 2026 12:58:39 GMT", "duration": "638", "isSummarized": False},
        ]},
        f"/video/{vid(5)}": {"id": vid(5), "description": "Bob shows his tomato beds and compost heap."},
        f"/video/{vid(6)}": {"id": vid(6), "description":
                             "Sam explains how AI labs buy compute and why inference demand keeps rising."},
        # Past streams report isLive=true here; that must not drop the call.
        f"/video/{vid(8)}": {"id": vid(8), "isLive": True, "description": ""},
        f"/video/{vid(1)}/transcript": transcript_payload(lab_transcript),
        f"/video/{vid(4)}/transcript": [RATE_LIMITED, RATE_LIMITED],
        f"/video/{vid(6)}/transcript": transcript_payload([]),
        f"/video/{vid(8)}/transcript": transcript_payload(call_transcript),
    }


class FakeTuber:
    """Fake transport: routes keyed by path (or (path, q|rss)); a list value
    is consumed one response per call, its last element repeating."""

    def __init__(self, routes: dict):
        self.routes = routes
        self.calls: list[tuple[str, dict]] = []

    def __call__(self, base_url, path, params, timeout):
        self.calls.append((path, dict(params or {})))
        key: object = path
        if path == "/search":
            key = (path, params["q"])
        elif path == "/podcast/episodes":
            key = (path, params["rss"])
        handler = self.routes.get(key)
        if handler is None:
            raise pod.TuberError("HTTP 404: Not Found", status=404)
        if isinstance(handler, list):
            item = handler.pop(0) if len(handler) > 1 else handler[0]
        else:
            item = handler
        if isinstance(item, Exception):
            raise item
        return copy.deepcopy(item)

    def paths(self) -> list[str]:
        return [path for path, _ in self.calls]


def make_client(fake: FakeTuber, sleeps: list | None = None, clock=None) -> pod.TuberClient:
    sleeps = [] if sleeps is None else sleeps
    return pod.TuberClient("https://tuber.example.test", transport=fake, sleep=sleeps.append,
                           monotonic=clock or (lambda: 0.0))


class LaneTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.out = self.tmp / "out"
        self.registry = write_registry(self.tmp, e2e_shows())

    def tearDown(self):
        self._tmp.cleanup()

    def run_lane(self, routes: dict, now: dt.datetime = NOW, **kwargs):
        fake = FakeTuber(routes)
        sleeps: list = []
        result = pod.run(registry=self.registry, out_dir=self.out, base_url="https://tuber.example.test",
                         now=now, client=make_client(fake, sleeps), **kwargs)
        return result, fake, sleeps

    def index(self) -> dict:
        return json.loads((self.out / "index.json").read_text(encoding="utf-8"))

    def episodes(self) -> dict:
        return {episode["id"]: episode for episode in self.index()["episodes"]}

    def snapshot(self) -> dict:
        return {path.name: path.read_bytes() for path in sorted(self.out.iterdir())} if self.out.exists() else {}


# ---------------------------------------------------------------------------


class RegistryValidationTest(unittest.TestCase):
    def load(self, shows, **top):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "r.json"
            path.write_text(json.dumps({"schema": 1, "shows": shows, **top}), encoding="utf-8")
            return pod.load_registry(path)

    def assertRejected(self, shows, pattern):
        with self.assertRaisesRegex(pod.RegistryError, pattern):
            self.load(shows)

    def test_valid_registry_loads_every_kind(self):
        shows = self.load(e2e_shows())
        self.assertEqual([show.kind for show in shows], ["channel", "channel", "search", "podcast"])
        self.assertEqual(shows[0].count, pod.DEFAULT_COUNT["channel"])
        self.assertEqual(shows[2].count, pod.DEFAULT_COUNT["search"])

    def test_duplicate_ids_rejected(self):
        self.assertRejected([show_row(), show_row()], "duplicate show id")

    def test_unknown_kind_and_priority_rejected(self):
        self.assertRejected([show_row(kind="trending")], "kind must be one of")
        self.assertRejected([show_row(priority="P3")], "priority must be P0-P2")

    def test_search_requires_channel_id_and_query(self):
        search = show_row(kind="search", query="x")
        del search["channel_id"]
        self.assertRejected([search], "requires a UC")
        self.assertRejected([show_row(kind="search")], "requires query")
        self.assertRejected([show_row(kind="search", query="   ")], "requires query")

    def test_channel_requires_valid_channel_id(self):
        row = show_row()
        del row["channel_id"]
        self.assertRejected([row], "requires a UC")
        self.assertRejected([show_row(channel_id="@handle")], "requires a UC")

    def test_podcast_requires_https_rss(self):
        row = {"id": "p", "name": "P", "kind": "podcast", "priority": "P2", "tags": [], "ai_filter": False,
               "min_duration_s": 0, "include_in_aradio": True}
        self.assertRejected([row], "https rss")
        self.assertRejected([dict(row, rss="http://insecure.example.test/feed")], "https rss")
        # The feed URL is a published fallback link, so it must be a safe URL too.
        self.assertRejected([dict(row, rss="https://feeds.example.test/x)[y](javascript:alert(1))")], "https rss")
        self.assertRejected([dict(row, rss="https://feeds.example.test/a b")], "https rss")

    def test_typos_and_wrong_kind_fields_rejected(self):
        self.assertRejected([show_row(channel="UC" + "a" * 22)], "unknown keys")
        self.assertRejected([show_row(query="not for channels")], "not valid for kind channel")
        self.assertRejected([show_row(rss=RSS)], "not valid for kind channel")

    def test_field_types_enforced(self):
        self.assertRejected([show_row(min_duration_s=-1)], "min_duration_s")
        self.assertRejected([show_row(min_duration_s=True)], "min_duration_s")
        self.assertRejected([show_row(ai_filter="no")], "ai_filter must be a boolean")
        self.assertRejected([show_row(count=0)], "count")
        self.assertRejected([show_row(id="Bad Id")], "kebab-case")
        self.assertRejected([show_row(id="a:b")], "kebab-case")

    def test_unknown_top_level_key_and_schema(self):
        with self.assertRaisesRegex(pod.RegistryError, "unknown registry keys"):
            self.load(e2e_shows(), extra=1)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "r.json"
            path.write_text(json.dumps({"schema": 2, "shows": e2e_shows()}), encoding="utf-8")
            with self.assertRaisesRegex(pod.RegistryError, "schema must be 1"):
                pod.load_registry(path)

    def test_listener_kind_precedence(self):
        shows = {show.id: show for show in self.load(e2e_shows())}
        self.assertEqual(shows["lab"].listener_kind, "video")
        # Earnings-call shows are ALSO tagged official; earnings-call must win.
        self.assertEqual(shows["acme-call"].listener_kind, "earnings-call")
        self.assertEqual(shows["pod"].listener_kind, "podcast")
        self.assertEqual(shows["notes"].listener_kind, "podcast")

    def test_main_exits_2_on_invalid_registry_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as td:
            registry = write_registry(Path(td), [show_row(kind="nope")])
            out = Path(td) / "out"
            with redirect_stderr(io.StringIO()):
                rc = pod.main(["--registry", str(registry), "--out-dir", str(out)])
            self.assertEqual(rc, 2)
            self.assertFalse(out.exists())


class ShippedRegistryTest(unittest.TestCase):
    """Offline structural checks on the registry the workflow ships."""

    def setUp(self):
        self.shows = pod.load_registry(pod.DEFAULT_REGISTRY)
        self.by_id = {show.id: show for show in self.shows}

    def test_registry_loads_and_is_non_trivial(self):
        self.assertGreaterEqual(len(self.shows), 30)
        self.assertTrue(all(show.include_in_aradio for show in self.shows))

    def test_every_search_source_is_channel_constrained(self):
        searches = [show for show in self.shows if show.kind == "search"]
        self.assertTrue(searches)
        for show in searches:
            self.assertRegex(show.channel_id, pod.CHANNEL_ID_RE, show.id)
            self.assertTrue(show.query, show.id)

    def test_earnings_calls_are_first_party_official_searches(self):
        calls = [show for show in self.shows if "earnings-call" in show.tags]
        self.assertGreaterEqual(len(calls), 2)
        for show in calls:
            self.assertEqual(show.kind, "search", show.id)
            self.assertIn("official", show.tags, show.id)
            self.assertEqual(show.listener_kind, "earnings-call", show.id)
            self.assertGreaterEqual(show.min_duration_s, 1800, show.id)

    def test_official_lab_channels_are_not_ai_filtered(self):
        for show in self.shows:
            if "frontier-lab" in show.tags and "official" in show.tags:
                self.assertFalse(show.ai_filter, f"{show.id}: a lab's own channel is on-topic by definition")

    def test_livestream_publishers_also_have_a_search_entry(self):
        # /api/channel omits live streams (verified 2026-10-30 for both).
        searched_channels = {show.channel_id for show in self.shows if show.kind == "search"}
        for show_id in ("openai", "cognitive-revolution"):
            self.assertIn(self.by_id[show_id].channel_id, searched_channels, show_id)

    def test_podcast_feeds_are_https_and_unique(self):
        feeds = [show.rss for show in self.shows if show.kind == "podcast"]
        self.assertEqual(len(feeds), len(set(feeds)))
        self.assertTrue(all(feed.startswith("https://") for feed in feeds))

    def test_channel_sources_are_unique(self):
        channels = [show.channel_id for show in self.shows if show.kind == "channel"]
        self.assertEqual(len(channels), len(set(channels)), "duplicate channel_id among channel sources")


CRAFTED_URLS = (
    "https://a.example/x) [y](javascript:alert(1))",
    "javascript:alert(1)",
    "https://a.example/x y",
    "https://a.example/<script>",
    "https://a.example/x\nhttps://b.example/y",
    "https://a.example/x\n",
    "https://a.example/‮evil",          # bidi override
    "https://a.example/x\"onmouseover=\"1",
    "https://a.example/x'y",
    "https://a.example/{x}",
    "https://a.example/x|y",
    "https://a.example/x\\y",
    "https://a.example/x^y",
    "https://a.example/x`y",
    "https://user:pass@a.example/x",       # credentials are never published
    "https://a.example:notaport/x",
    "ftp://a.example/x",
    "data:text/html,hi",
    "https:///no-host",
    "//a.example/protocol-relative",
    "https://a.example/" + "a" * 2048,
    "",
)


class SafeUrlTest(unittest.TestCase):
    def test_crafted_urls_are_rejected(self):
        for url in CRAFTED_URLS:
            with self.subTest(url=url):
                self.assertIsNone(pod.safe_url(url))
        for value in (None, 42, b"https://a.example/x", ["https://a.example/x"]):
            self.assertIsNone(pod.safe_url(value))  # type: ignore[arg-type]

    def test_normal_urls_pass_unchanged(self):
        for url in ("https://cdn.example.test/ep1.mp3",
                    "http://feeds.example.test/podcast.rss",
                    "https://pscrb.fm/rss/p/prfx.byspotify.com/e/api.substack.com/feed/podcast/1/abc.mp3?x=1&y=2",
                    "https://www.youtube.com/watch?v=frYSOKvNiiE&t=1234s",
                    "HTTPS://Example.TEST:8443/Path/%20encoded?q=a%26b#frag",
                    "https://a.example/" + "a" * (pod.SAFE_URL_MAX_LENGTH - len("https://a.example/"))):
            with self.subTest(url=url):
                self.assertEqual(pod.safe_url(url), url)

    def test_youtube_urls_are_built_only_from_valid_ids(self):
        self.assertEqual(pod.youtube_watch_url(vid(1), 75), f"https://www.youtube.com/watch?v={vid(1)}&t=75s")
        for bad in ("short", "vid00000001)", "../../x/yy", None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                pod.youtube_watch_url(bad)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            pod.youtube_watch_url(vid(1), -1)


class UrlIngestTest(LaneTestCase):
    """Third-party URLs (RSS enclosures relayed by tuber) are validated at
    ingest; an unsafe one never reaches index.json or the Markdown."""

    def routes_with_enclosures(self, urls: list[str]) -> dict:
        routes = e2e_routes()
        routes[("/podcast/episodes", RSS)]["episodes"] = [
            {"id": f"pod-x{n}", "title": f"Episode {n} on model evals", "description": "Evals.",
             "audioUrl": url, "publishedAt": "Wed, 28 Oct 2026 12:58:39 GMT", "duration": "900"}
            for n, url in enumerate(urls)
        ]
        return routes

    def test_unsafe_enclosures_are_dropped_and_never_published(self):
        crafted = [url for url in CRAFTED_URLS if url]
        self.run_lane(self.routes_with_enclosures(crafted + ["https://cdn.example.test/good.mp3"]))
        episodes = self.episodes()
        for n in range(len(crafted)):
            episode = episodes[f"notes:pod-x{n}"]
            self.assertIsNone(episode["audio_url"], crafted[n])
            self.assertEqual(episode["url"], RSS)  # falls back to the registry's feed
        good = episodes[f"notes:pod-x{len(crafted)}"]
        self.assertEqual((good["audio_url"], good["url"]), ("https://cdn.example.test/good.mp3",) * 2)
        published = "".join(path.read_text(encoding="utf-8") for path in self.out.iterdir())
        for marker in ("javascript", "<script>", "a.example", "b.example", "‮", "user:pass", "onmouseover"):
            self.assertNotIn(marker, published)
        self.assertIn("(<https://cdn.example.test/good.mp3>)", published)

    def test_hand_edited_index_is_sanitized_on_reload(self):
        self.run_lane(e2e_routes())
        index = self.index()
        for episode in index["episodes"]:
            episode["url"] = "https://evil.example/x) [y](javascript:alert(1))"
            if episode["video_id"]:
                episode["audio_url"] = "https://evil.example/a.mp3"
                episode["excerpts"].append({"text": " ".join(["word"] * 500), "at_s": 9,
                                            "url": "javascript:alert(1)"})
                episode["excerpts"] *= 3
            else:
                episode["audio_url"] = "https://evil.example/<script>"
        (self.out / "index.json").write_text(json.dumps(index), encoding="utf-8")
        self.run_lane(e2e_routes(), now=NOW + dt.timedelta(minutes=30))
        published = "".join(path.read_text(encoding="utf-8") for path in self.out.iterdir())
        self.assertNotIn("evil.example", published)
        self.assertNotIn("javascript", published)
        for episode in self.index()["episodes"]:
            self.assertLessEqual(len(episode["excerpts"]), pod.MAX_EXCERPTS)
            if episode["video_id"]:
                self.assertEqual(episode["url"], pod.youtube_watch_url(episode["video_id"]))
                self.assertIsNone(episode["audio_url"])
                for excerpt in episode["excerpts"]:
                    self.assertLessEqual(len(excerpt["text"].split()), pod.MAX_EXCERPT_WORDS)
                    self.assertEqual(excerpt["url"], pod.youtube_watch_url(episode["video_id"], excerpt["at_s"]))
            else:
                self.assertEqual((episode["url"], episode["audio_url"]), (RSS, None))

    def test_records_whose_id_does_not_match_are_dropped(self):
        self.run_lane(e2e_routes())
        index = self.index()
        video = next(e for e in index["episodes"] if e["video_id"])
        rss = next(e for e in index["episodes"] if not e["video_id"])
        video["id"] = video["show_id"] + ":evil](javascript:alert(1))"
        rss["id"] = rss["show_id"] + ":pod-x) [y](javascript:alert(1))"
        (self.out / "index.json").write_text(json.dumps(index), encoding="utf-8")
        self.run_lane(e2e_routes(), now=NOW + dt.timedelta(minutes=30))
        self.assertNotIn("javascript", (self.out / "index.json").read_text(encoding="utf-8"))

    def test_markdown_text_is_inert_even_from_a_hand_edited_index(self):
        self.run_lane(e2e_routes())
        index = self.index()
        for episode in index["episodes"]:
            episode["title"] = "Real title\n# Injected heading\n[click](javascript:alert(1)) <img src=x>"
            episode["description"] = "notes\r\n- injected bullet \x00 \u202e"
        (self.out / "index.json").write_text(json.dumps(index), encoding="utf-8")
        self.run_lane(e2e_routes(), now=NOW + dt.timedelta(minutes=30))
        text = (self.out / "2026-10-30.md").read_text(encoding="utf-8")
        self.assertNotRegex(text, r"(?m)^# Injected")
        self.assertNotRegex(text, r"(?m)^- injected")
        self.assertNotRegex(text, r"(?<!\\)\[click(?<!\\)\]")  # brackets only appear escaped
        self.assertNotRegex(text, r"(?<!\\)<img")
        self.assertIn("\\<img src=x\\>", text)
        self.assertNotIn("\x00", text)
        self.assertNotIn("\u202e", text)

    def test_md_escape(self):
        self.assertEqual(pod._md_escape("a [b](c) <d>\n# e\x00f `g`"), "a \\[b\\](c) \\<d\\> # e f \\`g\\`")

    def test_records_with_an_invalid_video_id_are_dropped(self):
        self.run_lane(e2e_routes())
        index = self.index()
        index["episodes"][0]["video_id"] = "x) [y](javascript:alert(1))"
        dropped = index["episodes"][0]["id"]
        (self.out / "index.json").write_text(json.dumps(index), encoding="utf-8")
        self.run_lane(e2e_routes(), now=NOW + dt.timedelta(minutes=30))
        self.assertNotIn("javascript", (self.out / "index.json").read_text(encoding="utf-8"))
        # Re-discovered from the listing, it comes back as a clean record.
        if dropped in self.episodes():
            self.assertTrue(pod.VIDEO_ID_RE.fullmatch(self.episodes()[dropped]["video_id"]))


class ReadOnlyGuardTest(unittest.TestCase):
    def test_generation_endpoints_refused(self):
        for path in ("/summarize", f"/video/{vid(1)}/summarize", "/acp/jobs", "/acp/jobs/123",
                     "/podcast/episode/summarize", "/PODCAST/EPISODE/SUMMARIZE"):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "generation endpoint"):
                pod.check_read_only_path(path)

    def test_only_allowlisted_read_paths_pass(self):
        for path in (f"/channel/{CH_LAB}", "/search", "/podcast/episodes", f"/video/{vid(1)}",
                     f"/video/{vid(1)}/transcript"):
            pod.check_read_only_path(path)
        for path in ("/trending", f"/channel/{CH_LAB}/videos", f"/video/{vid(1)}/summary-preview",
                     "/video/short/transcript", "/admin", ""):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "non-allowlisted"):
                pod.check_read_only_path(path)

    def test_client_refuses_before_any_request(self):
        fake = FakeTuber({})
        client = make_client(fake)
        with self.assertRaises(ValueError):
            client.get("/podcast/episode/summarize")
        self.assertEqual(fake.calls, [])
        self.assertEqual(client.requests, 0)

    def test_http_layer_sends_get_and_guards_before_urlopen(self):
        with unittest.mock.patch.object(pod.urllib.request, "urlopen") as urlopen:
            with self.assertRaises(ValueError):
                pod.http_get_json("https://tuber.example.test", "/acp/jobs", None, 5)
            urlopen.assert_not_called()
            response = unittest.mock.MagicMock()
            response.__enter__.return_value.read.return_value = b'{"videos": []}'
            urlopen.return_value = response
            pod.http_get_json("https://tuber.example.test", f"/channel/{CH_LAB}", {"count": 3}, 5)
            request = urlopen.call_args.args[0]
            self.assertEqual(request.get_method(), "GET")
            self.assertIsNone(request.data)
            self.assertEqual(request.full_url, f"https://tuber.example.test/api/channel/{CH_LAB}?count=3")

    def classify(self, status: int, body: bytes) -> pod.TuberError:
        error = pod.urllib.error.HTTPError(
            "https://tuber.example.test/api/video/x/transcript", status, "Internal Server Error", {},
            io.BytesIO(body))
        with unittest.mock.patch.object(pod.urllib.request, "urlopen", side_effect=error):
            with self.assertRaises(pod.TuberError) as caught:
                pod.http_get_json("https://tuber.example.test", f"/video/{vid(1)}/transcript", None, 5)
        return caught.exception

    def test_youtube_throttling_bodies_are_classified(self):
        # Both messages were returned live on 2026-10-30.
        for message in (b"YouTube temporarily rate-limited transcript access",
                        b"YouTube temporarily blocked transcript access"):
            with self.subTest(message=message):
                error = self.classify(500, b'{"error":"' + message + b'","segments":[]}')
                self.assertTrue(error.rate_limited)
                self.assertEqual(error.status, 500)
        self.assertTrue(self.classify(429, b"slow down").rate_limited)
        self.assertFalse(self.classify(500, b'{"error":"database unavailable"}').rate_limited)
        self.assertFalse(self.classify(404, b'{"error":"rate-limited"}').rate_limited)

    def test_a_full_run_only_touches_read_paths(self):
        with tempfile.TemporaryDirectory() as td:
            registry = write_registry(Path(td), e2e_shows())
            fake = FakeTuber(e2e_routes())
            pod.run(registry=registry, out_dir=Path(td) / "out", base_url="https://tuber.example.test",
                    now=NOW, client=make_client(fake))
        self.assertTrue(fake.calls)
        for path in fake.paths():
            self.assertRegex(path, pod.READ_ONLY_PATH_RE)
            self.assertNotIn("summar", path)
            self.assertNotIn("acp", path)


class TimeParsingTest(unittest.TestCase):
    def test_label_age_seconds_matches_youtube_day_parser(self):
        for label, seconds in (("15h ago", 15 * 3600), ("Streamed 1d ago", 86400), ("2 days ago", 2 * 86400),
                               ("1mo ago", 30 * 86400), ("Premiered 22 hours ago", 22 * 3600),
                               ("5m ago", 300), ("3 weeks ago", 21 * 86400), ("Streamed 2y ago", 730 * 86400)):
            with self.subTest(label=label):
                self.assertEqual(pod.label_age_seconds(label), seconds)
                self.assertEqual(seconds // 86400, pod.youtube.approximate_age_days(label))
        for label in ("", "Scheduled for 11/2/26", "Oct 29, 2026"):
            self.assertIsNone(pod.label_age_seconds(label))
            self.assertIsNone(pod.estimated_age_seconds(label))

    def test_estimated_age_is_the_midpoint_of_the_floored_label(self):
        self.assertEqual(pod.estimated_age_seconds("15h ago"), 15 * 3600 + 1800)
        self.assertEqual(pod.estimated_age_seconds("Streamed 1d ago"), 36 * 3600)
        self.assertEqual(pod.estimated_age_seconds("5m ago"), 330)
        self.assertEqual(pod.estimated_age_seconds("just now"), 0)

    def test_rss_dates_and_durations(self):
        self.assertEqual(pod.parse_rss_date("Wed, 28 Oct 2026 12:58:39 GMT"),
                         dt.datetime(2026, 10, 28, 12, 58, 39, tzinfo=dt.timezone.utc))
        self.assertIsNone(pod.parse_rss_date("not a date"))
        self.assertEqual(pod.parse_duration("638"), 638)
        self.assertEqual(pod.parse_duration("1:02:03"), 3723)
        self.assertEqual(pod.parse_duration(4141), 4141)
        self.assertIsNone(pod.parse_duration(True))
        self.assertIsNone(pod.parse_duration("live"))


class AiFilterTest(unittest.TestCase):
    def test_title_hit_is_enough(self):
        self.assertTrue(pod.is_ai_topical("Satya Nadella on Open vs Closed Models", ""))
        self.assertTrue(pod.is_ai_topical("What will computer chips look like in 2045?", ""))
        self.assertTrue(pod.is_ai_topical("Inside OpenAI's compute deals", ""))

    def test_needs_two_hits_in_notes(self):
        self.assertTrue(pod.is_ai_topical("Crusoe CEO on stranded energy",
                                          "Crusoe runs gigawatt-scale data centers and a managed AI cloud."))
        self.assertFalse(pod.is_ai_topical("Gardening with Bob", "One passing mention of AI in a bio."))

    def test_unknown_without_notes(self):
        self.assertIsNone(pod.is_ai_topical("History of Rome", ""))

    def test_case_and_word_boundaries(self):
        self.assertEqual(pod.ai_hits("said aid maid Thai trail"), 0)
        self.assertEqual(pod.ai_hits("The AI-powered tool"), 1)

    def test_show_note_boilerplate_never_counts(self):
        notes = pod.clean_show_notes(
            "A conversation about tomatoes and compost.\n"
            "#20vc #ai #llm #agents\n"
            "Follow us on X: https://x.com/show\n"
            "This episode is brought to you by an AI startup — use code AI for GPU credits.\n"
            "Additional Reading:\n"
            "OpenAI and Anthropic race for compute and AI agents\n"
        )
        self.assertEqual(notes, "A conversation about tomatoes and compost.")
        self.assertFalse(pod.is_ai_topical("Gardening with Bob", notes))

    def test_sponsor_blurbs_after_partner_header_never_count(self):
        # Live regression (All-In, 2026-10-30): an episode about Theranos read
        # as AI through its sponsor blurbs.
        notes = pod.clean_show_notes(
            "(0:00) Billy Evans joins Friedberg\n"
            "(3:38) How they met, the indictment\n\n"
            "Thanks to our partners for making this possible!\n\n"
            "IREN is a vertically integrated AI Cloud platform for AI training and inference. https://iren.com/\n"
            "Keel owns the power that HPC and AI run on - backed by data centers.\n"
        )
        self.assertEqual(notes, "Billy Evans joins Friedberg How they met, the indictment")
        self.assertFalse(pod.is_ai_topical("Billy Evans Speaks Out", notes))

    def test_multiline_link_lines_drop_but_single_line_notes_keep_summary(self):
        self.assertEqual(pod.clean_show_notes("Summary of the AI episode.\nSponsor X: https://x.test/ai"),
                         "Summary of the AI episode.")
        self.assertEqual(pod.clean_show_notes("Evals are hard. Read more at https://x.test/p. Thanks!"),
                         "Evals are hard. Thanks!")

    def test_show_notes_keep_chapter_text_without_timestamps(self):
        notes = pod.clean_show_notes("(0:00) Welcome\n(19:31) The AI coach\n01:15:02 - Why compute matters")
        self.assertEqual(notes, "Welcome The AI coach Why compute matters")


class DiscoveryTest(unittest.TestCase):
    def setUp(self):
        with tempfile.TemporaryDirectory() as td:
            self.shows = pod.load_registry(write_registry(Path(td), e2e_shows()))

    def test_search_keeps_only_the_registered_channel(self):
        fake = FakeTuber(e2e_routes())
        found = pod.discover(self.shows, make_client(fake), NOW)
        search_hits = [c for c in found.candidates if c.show.id == "acme-call"]
        self.assertEqual({c.native_id for c in search_hits}, {vid(8), vid(10)})
        self.assertTrue(all(c.channel_id == CH_CALL for c in search_hits))
        self.assertEqual(found.third_party_dropped, 1)

    def test_video_rows_normalize_with_approximate_time(self):
        found = pod.discover(self.shows, make_client(FakeTuber(e2e_routes())), NOW)
        first = next(c for c in found.candidates if c.native_id == vid(1))
        # "3h ago" is floored by YouTube (3-4 h): the midpoint is published_at.
        self.assertEqual(first.published_at, NOW - dt.timedelta(hours=3, minutes=30))
        self.assertEqual(first.precision, "approximate")
        self.assertEqual(first.url, f"https://www.youtube.com/watch?v={vid(1)}")
        episode = next(c for c in found.candidates if c.native_id == "pod-abc123")
        self.assertEqual(episode.precision, "exact")
        self.assertEqual(episode.published_at, dt.datetime(2026, 10, 28, 12, 58, tzinfo=dt.timezone.utc))
        self.assertIsNone(episode.video_id)
        self.assertEqual(episode.url, "https://cdn.example.test/ep1.mp3")
        self.assertEqual(episode.description, "Evals are hard.")

    def test_empty_or_failing_sources_are_recorded_not_raised(self):
        routes = e2e_routes()
        routes[f"/channel/{CH_LAB}"] = {"name": "Lab", "videos": []}
        routes[f"/channel/{CH_POD}"] = pod.TuberError("HTTP 502: Bad Gateway", status=502)
        found = pod.discover(self.shows, make_client(FakeTuber(routes)), NOW)
        self.assertEqual(sorted(show.id for show, _ in found.errors), ["lab", "pod"])
        self.assertIn("empty listing", dict((s.id, e) for s, e in found.errors)["lab"])
        self.assertTrue(any(c.show.id == "acme-call" for c in found.candidates))

    def test_first_sight_filters(self):
        found = pod.discover(self.shows, make_client(FakeTuber(e2e_routes())), NOW)
        reasons = {c.native_id: pod.first_sight_rejection(c, NOW) for c in found.candidates}
        self.assertIsNone(reasons[vid(1)])
        self.assertEqual(reasons[vid(2)], "shorter than min_duration_s")
        self.assertEqual(reasons[vid(3)], "older than the first-sight window")
        self.assertEqual(reasons[vid(10)], "live now")
        self.assertIsNone(reasons["pod-abc123"])


class EndToEndTest(LaneTestCase):
    def test_first_run_builds_the_contract_index(self):
        result, fake, sleeps = self.run_lane(e2e_routes())
        self.assertEqual(result.exit_code, 0, result.summary)
        index = self.index()
        self.assertEqual(list(index), ["lane", "schema", "updated_at", "degraded", "episodes"])
        self.assertEqual((index["lane"], index["schema"], index["degraded"]), ("podcasts", 1, False))
        self.assertEqual(index["updated_at"], "2026-10-30T08:41:00Z")
        episodes = self.episodes()
        self.assertEqual(set(episodes), {f"lab:{vid(1)}", f"pod:{vid(4)}", f"pod:{vid(6)}",
                                         f"acme-call:{vid(8)}", "notes:pod-abc123"})
        call = episodes[f"acme-call:{vid(8)}"]
        self.assertEqual(list(call), ["id", "show_id", "show", "kind", "priority", "tags", "title", "url",
                                      "video_id", "audio_url", "published_at", "published_precision",
                                      "first_seen_at", "duration_s", "transcript", "excerpts", "description"])
        self.assertEqual(call["kind"], "earnings-call")
        self.assertEqual(call["published_at"], "2026-10-30T06:11:00Z")  # "Streamed 2h ago" -> 2.5 h
        self.assertEqual(call["first_seen_at"], "2026-10-30T08:41:00Z")
        self.assertEqual(list(call["transcript"]), ["available", "source", "words", "checked_at", "attempts"])
        self.assertTrue(call["transcript"]["available"])
        self.assertEqual(episodes[f"lab:{vid(1)}"]["kind"], "video")
        rss = episodes["notes:pod-abc123"]
        self.assertEqual((rss["kind"], rss["published_precision"], rss["video_id"]), ("podcast", "exact", None))
        self.assertEqual(rss["audio_url"], "https://cdn.example.test/ep1.mp3")
        self.assertEqual(rss["transcript"], pod.empty_transcript())
        self.assertEqual(rss["excerpts"], [])
        # ai_filter: notes about compute pass, gardening is rejected, no notes defers.
        self.assertNotIn(f"pod:{vid(5)}", episodes)
        self.assertNotIn(f"pod:{vid(7)}", episodes)
        self.assertIn("rejected 1, deferred 1", result.summary)
        # Third-party re-stream and the in-progress live stream never enter.
        self.assertFalse(any(vid(9) in key or vid(10) in key for key in episodes))
        self.assertNotIn(("/video/" + vid(9) + "/transcript"), fake.paths())
        self.assertNotIn(f"/podcast/episodes/transcript", fake.paths())

    def test_past_stream_with_details_islive_true_is_kept(self):
        # Regression: /api/video/{id} reports isLive=true for any PAST stream;
        # trusting it dropped the Alphabet Q3 call in a live run.
        self.run_lane(e2e_routes())
        self.assertIn(f"acme-call:{vid(8)}", self.episodes())

    def test_episode_ids_and_kinds_follow_the_contract(self):
        self.run_lane(e2e_routes())
        for episode in self.index()["episodes"]:
            self.assertEqual(episode["id"], f"{episode['show_id']}:{episode['video_id'] or 'pod-abc123'}")
            self.assertIn(episode["kind"], {"video", "earnings-call", "podcast"})
            self.assertLessEqual(len(episode["description"].split()), pod.MAX_DESCRIPTION_WORDS)

    def test_markdown_lists_todays_episodes_and_fetch_errors(self):
        routes = e2e_routes()
        routes[("/podcast/episodes", RSS)] = pod.TuberError("HTTP 502: Bad Gateway", status=502)
        self.run_lane(routes)
        text = (self.out / "2026-10-30.md").read_text(encoding="utf-8")
        self.assertIn("# Podcast Signal - 2026-10-30", text)
        self.assertRegex(text, r"(?m)^- Fetch errors: 1$")
        self.assertIn("## Fetch errors", text)
        self.assertIn("Notes FM (`notes`): TuberError: HTTP 502: Bad Gateway", text)
        # Angle-bracket destinations: safe because safe_url never passes < or >.
        self.assertIn(f"### [Acme Q3 2026 Earnings Call](<https://www.youtube.com/watch?v={vid(8)}>)", text)
        self.assertRegex(text, rf"(?m)^  - \[\d+:\d\d\]\(<https://www\.youtube\.com/watch\?v={vid(8)}&t=\d+s>\) ")
        self.assertIn("- Transcript: available (youtube_captions,", text)
        self.assertNotIn("Generated:", text)  # no run timestamp: a quiet rerun stays byte-identical

    def test_markdown_for_a_quiet_day_says_so(self):
        self.run_lane(e2e_routes())
        result, _, _ = self.run_lane(e2e_routes(), now=NOW + dt.timedelta(days=1))
        text = (self.out / "2026-10-31.md").read_text(encoding="utf-8")
        self.assertIn("_No new episodes first seen today._", text)
        self.assertEqual(result.exit_code, 0)


class StatePreservationTest(LaneTestCase):
    def test_first_seen_and_published_never_change(self):
        self.run_lane(e2e_routes())
        before = self.episodes()[f"lab:{vid(1)}"]
        later = NOW + dt.timedelta(hours=5)
        routes = e2e_routes()
        routes[f"/channel/{CH_LAB}"]["videos"][0].update(publishedAt="9h ago", title="Introducing Model X (edited)")
        self.run_lane(routes, now=later)
        after = self.episodes()[f"lab:{vid(1)}"]
        for field in ("first_seen_at", "published_at", "published_precision", "title", "duration_s"):
            self.assertEqual(after[field], before[field], field)

    def test_show_level_fields_follow_the_registry(self):
        self.run_lane(e2e_routes())
        shows = e2e_shows()
        shows[0].update(priority="P1", name="Lab Renamed")
        write_registry(self.tmp, shows)
        self.run_lane(e2e_routes(), now=NOW + dt.timedelta(minutes=30))
        episode = self.episodes()[f"lab:{vid(1)}"]
        self.assertEqual((episode["priority"], episode["show"]), ("P1", "Lab Renamed"))
        self.assertEqual(episode["first_seen_at"], "2026-10-30T08:41:00Z")

    def test_removed_show_and_expired_episodes_are_pruned(self):
        self.run_lane(e2e_routes())
        index = self.index()
        stale = copy.deepcopy(index["episodes"][0])
        stale.update(id=f"lab:{vid(99)}", video_id=vid(99), published_at="2026-09-29T08:00:00Z")
        index["episodes"].append(stale)
        (self.out / "index.json").write_text(json.dumps(index), encoding="utf-8")
        write_registry(self.tmp, [row for row in e2e_shows() if row["id"] != "pod"])
        self.run_lane(e2e_routes(), now=NOW + dt.timedelta(minutes=30))
        ids = set(self.episodes())
        self.assertNotIn(f"lab:{vid(99)}", ids)  # published > 30 days ago
        self.assertFalse(any(key.startswith("pod:") for key in ids))  # show left the registry
        self.assertIn(f"lab:{vid(1)}", ids)

    def test_same_video_from_two_sources_is_one_episode(self):
        shows = e2e_shows()
        shows.insert(1, show_row(id="lab-live", name="Lab livestreams", kind="search", query="Lab livestream",
                                 channel_id=CH_LAB, min_duration_s=60))
        write_registry(self.tmp, shows)
        routes = e2e_routes()
        routes[("/search", "Lab livestream")] = {"query": "Lab livestream", "videos": [
            video_row(1, "Introducing Model X", "3h ago", 600, channelId=CH_LAB, isLive=False),
            video_row(11, "Lab keynote livestream", "Streamed 4h ago", 2400, channelId=CH_LAB, isLive=False),
        ]}
        self.run_lane(routes)
        ids = set(self.episodes())
        self.assertIn(f"lab:{vid(1)}", ids)  # first registry claimant wins
        self.assertNotIn(f"lab-live:{vid(1)}", ids)
        self.assertIn(f"lab-live:{vid(11)}", ids)

    def test_existing_unparseable_index_is_refused(self):
        self.out.mkdir()
        (self.out / "index.json").write_text("{not json", encoding="utf-8")
        result, fake, _ = self.run_lane(e2e_routes())
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(fake.calls, [])
        self.assertEqual((self.out / "index.json").read_text(encoding="utf-8"), "{not json")


class TranscriptPolicyTest(LaneTestCase):
    def test_excerpt_caps_and_deep_links(self):
        self.run_lane(e2e_routes())
        for episode in self.index()["episodes"]:
            self.assertLessEqual(len(episode["excerpts"]), pod.MAX_EXCERPTS)
            for excerpt in episode["excerpts"]:
                self.assertEqual(list(excerpt), ["text", "at_s", "url"])
                self.assertLessEqual(len(excerpt["text"].split()), pod.MAX_EXCERPT_WORDS)
                self.assertEqual(excerpt["url"], f"{episode['url']}&t={excerpt['at_s']}s")
        lab = self.episodes()[f"lab:{vid(1)}"]
        self.assertTrue(any("2 gigawatts" in excerpt["text"] for excerpt in lab["excerpts"]))
        self.assertEqual(lab["transcript"]["words"], pod.transcript_word_count(
            e2e_routes()[f"/video/{vid(1)}/transcript"]["segments"]))

    def test_no_transcript_text_is_written_beyond_excerpts(self):
        self.run_lane(e2e_routes())
        excerpt_tokens: set[str] = set()
        for episode in self.index()["episodes"]:
            for excerpt in episode["excerpts"]:
                excerpt_tokens |= set(re.findall(r"\bzq[a-z]+\b", excerpt["text"]))
        written: set[str] = set()
        for path in self.out.iterdir():
            written |= set(re.findall(r"\bzq[a-z]+\b", path.read_text(encoding="utf-8")))
        self.assertTrue(written <= excerpt_tokens, sorted(written - excerpt_tokens)[:5])
        # 120 + 400 transcript sentences each carried a unique token; only the
        # handful inside the <= 6 x 60-word excerpts per episode may appear.
        self.assertLessEqual(len(written), 2 * pod.MAX_EXCERPTS * pod.MAX_EXCERPT_WORDS // 12)

    def test_rate_limit_is_retried_once_in_run_then_on_later_runs(self):
        _, fake, sleeps = self.run_lane(e2e_routes())
        self.assertEqual(fake.paths().count(f"/video/{vid(4)}/transcript"), 2)
        self.assertIn(pod.TRANSCRIPT_RETRY_BACKOFF_S, sleeps)
        state = self.episodes()[f"pod:{vid(4)}"]["transcript"]
        self.assertEqual((state["available"], state["attempts"], state["checked_at"]),
                         (False, 1, "2026-10-30T08:41:00Z"))
        # Not due again inside the retry interval...
        _, fake, _ = self.run_lane(e2e_routes(), now=NOW + dt.timedelta(minutes=100))
        self.assertNotIn(f"/video/{vid(4)}/transcript", fake.paths())
        # ...due on the next scheduled run, and a success fills it in.
        routes = e2e_routes()
        routes[f"/video/{vid(4)}/transcript"] = transcript_payload(filler_segments(500, step_ms=7000))
        _, fake, _ = self.run_lane(routes, now=NOW + dt.timedelta(minutes=120))
        self.assertIn(f"/video/{vid(4)}/transcript", fake.paths())
        state = self.episodes()[f"pod:{vid(4)}"]["transcript"]
        self.assertEqual((state["available"], state["attempts"]), (True, 2))
        self.assertEqual(self.episodes()[f"pod:{vid(4)}"]["first_seen_at"], "2026-10-30T08:41:00Z")

    def test_retry_schedule_and_three_day_window(self):
        episode = {"video_id": vid(1), "published_at": "2026-10-30T06:00:00Z",
                   "transcript": dict(pod.empty_transcript())}
        self.assertEqual(pod.transcript_bucket(episode, NOW), 0)
        episode["transcript"].update(attempts=1, checked_at="2026-10-30T08:00:00Z")
        self.assertIsNone(pod.transcript_bucket(episode, NOW))
        self.assertEqual(pod.transcript_bucket(episode, NOW + dt.timedelta(minutes=80)), 1)
        episode["transcript"].update(attempts=4, checked_at="2026-10-30T08:00:00Z")
        self.assertIsNone(pod.transcript_bucket(episode, NOW + dt.timedelta(hours=2)))
        self.assertEqual(pod.transcript_bucket(episode, NOW + dt.timedelta(hours=6)), 1)
        self.assertIsNone(pod.transcript_bucket(episode, NOW + dt.timedelta(days=3)))
        old = {"video_id": vid(2), "published_at": "2026-10-20T06:00:00Z",
               "transcript": dict(pod.empty_transcript())}
        self.assertEqual(pod.transcript_bucket(old, NOW), 2)  # one first look, even for backlog
        old["transcript"].update(attempts=1, checked_at="2026-10-29T06:00:00Z")
        self.assertIsNone(pod.transcript_bucket(old, NOW))
        self.assertIsNone(pod.transcript_bucket({"video_id": None, "published_at": "2026-10-30T06:00:00Z",
                                                 "transcript": pod.empty_transcript()}, NOW))
        self.assertIsNone(pod.transcript_bucket({"video_id": "../x", "published_at": "2026-10-30T06:00:00Z",
                                                 "transcript": pod.empty_transcript()}, NOW))

    def test_per_run_cap_prefers_fresh_episodes(self):
        episodes = []
        for number, published in ((1, "2026-10-20T00:00:00Z"), (2, "2026-10-30T07:00:00Z"),
                                  (3, "2026-10-30T05:00:00Z")):
            episodes.append({"id": f"s:{vid(number)}", "video_id": vid(number), "url": "u", "priority": "P1",
                             "published_at": published, "duration_s": 60,
                             "transcript": dict(pod.empty_transcript()), "excerpts": []})
        fake = FakeTuber({})
        stats = pod.update_transcripts(episodes, make_client(fake), NOW, max_fetches=2)
        self.assertEqual(stats.fetched, 2)
        self.assertEqual(stats.stopped, "per-run cap")
        self.assertEqual(fake.paths()[0], f"/video/{vid(2)}/transcript")
        self.assertEqual(fake.paths()[-1], f"/video/{vid(3)}/transcript")

    def test_rate_limit_breaker_stops_the_phase(self):
        episodes = [{"id": f"s:{vid(n)}", "video_id": vid(n), "url": "u", "priority": "P0",
                     "published_at": "2026-10-30T07:00:00Z", "duration_s": 60,
                     "transcript": dict(pod.empty_transcript()), "excerpts": []} for n in range(1, 9)]
        fake = FakeTuber({f"/video/{vid(n)}/transcript": RATE_LIMITED for n in range(1, 9)})
        stats = pod.update_transcripts(episodes, make_client(fake), NOW, max_fetches=12)
        self.assertEqual(stats.fetched, pod.RATE_LIMIT_BREAKER)
        self.assertEqual(stats.stopped, "rate-limit breaker")
        untouched = [e for e in episodes if e["transcript"]["attempts"] == 0]
        self.assertEqual(len(untouched), 8 - pod.RATE_LIMIT_BREAKER)

    def test_time_budget_stops_the_phase(self):
        ticks = iter([0.0, 0.0, 1000.0, 1000.0])
        episodes = [{"id": f"s:{vid(n)}", "video_id": vid(n), "url": "u", "priority": "P0",
                     "published_at": "2026-10-30T07:00:00Z", "duration_s": 60,
                     "transcript": dict(pod.empty_transcript()), "excerpts": []} for n in (1, 2)]
        client = make_client(FakeTuber({}), clock=lambda: next(ticks))
        stats = pod.update_transcripts(episodes, client, NOW, max_fetches=12)
        self.assertEqual((stats.fetched, stats.stopped), (1, "time budget"))

    def test_unusable_transcripts_are_not_marked_available(self):
        client = make_client(FakeTuber({
            f"/video/{vid(1)}/transcript": transcript_payload(filler_segments(20), language="es"),
            f"/video/{vid(2)}/transcript": transcript_payload(filler_segments(6)),  # 25 s of a 1-hour show
            f"/video/{vid(3)}/transcript": {"error": "boom"},
            f"/video/{vid(4)}/transcript": pod.TuberError("HTTP 404: Not Found", status=404),
        }))
        self.assertEqual(pod.fetch_transcript(client, vid(1), 120).status, "non-english")
        self.assertEqual(pod.fetch_transcript(client, vid(2), 3600).status, "incomplete")
        self.assertEqual(pod.fetch_transcript(client, vid(2), 90).status, "ok")  # short videos exempt
        self.assertEqual(pod.fetch_transcript(client, vid(3), 120).status, "error")
        self.assertEqual(pod.fetch_transcript(client, vid(4), 120).status, "error")
        self.assertEqual(client.requests, 5)  # a 404 is not retried


class IdempotencyTest(LaneTestCase):
    def test_quiet_rerun_is_byte_identical(self):
        self.run_lane(e2e_routes())
        before = self.snapshot()
        result, _, _ = self.run_lane(e2e_routes(), now=NOW + dt.timedelta(minutes=30))
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(result.wrote, [])
        self.assertIn("wrote nothing (no change)", result.summary)

    def test_updated_at_moves_only_with_content(self):
        self.run_lane(e2e_routes())
        self.run_lane(e2e_routes(), now=NOW + dt.timedelta(minutes=30))
        self.assertEqual(self.index()["updated_at"], "2026-10-30T08:41:00Z")
        routes = e2e_routes()
        routes[f"/channel/{CH_LAB}"]["videos"].insert(0, video_row(12, "Introducing Model Y", "1h ago", 400))
        self.run_lane(routes, now=NOW + dt.timedelta(minutes=50))
        self.assertEqual(self.index()["updated_at"], "2026-10-30T09:31:00Z")


class FailureModesTest(LaneTestCase):
    def failing_routes(self) -> dict:
        error = pod.TuberError("HTTP 502: Bad Gateway", status=502)
        return {f"/channel/{CH_LAB}": error, f"/channel/{CH_POD}": error,
                ("/search", SEARCH_Q): error, ("/podcast/episodes", RSS): error}

    def test_total_failure_exits_3_and_writes_nothing(self):
        result, _, _ = self.run_lane(self.failing_routes())
        self.assertEqual(result.exit_code, pod.EXIT_TOTAL_FETCH_FAILURE)
        self.assertFalse(self.out.exists())

    def test_total_failure_leaves_existing_output_untouched(self):
        self.run_lane(e2e_routes())
        before = self.snapshot()
        result, _, _ = self.run_lane(self.failing_routes(), now=NOW + dt.timedelta(days=1))
        self.assertEqual(result.exit_code, 3)
        self.assertEqual(self.snapshot(), before)

    def test_degraded_when_more_than_half_fail(self):
        routes = e2e_routes()
        error = pod.TuberError("HTTP 502: Bad Gateway", status=502)
        routes[f"/channel/{CH_LAB}"] = error
        routes[f"/channel/{CH_POD}"] = error
        result, _, _ = self.run_lane(routes)
        self.assertEqual(result.exit_code, 0)
        self.assertFalse(self.index()["degraded"])  # exactly half is not "more than half"
        routes[("/search", SEARCH_Q)] = error
        result, _, _ = self.run_lane(routes, now=NOW + dt.timedelta(minutes=30))
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(self.index()["degraded"])

    def test_publish_age_drift_exits_4_and_writes_nothing(self):
        routes = e2e_routes()
        for key in (f"/channel/{CH_LAB}", f"/channel/{CH_POD}"):
            for row in routes[key]["videos"]:
                row["publishedAt"] = "il y a 3 heures"
        for row in routes[("/search", SEARCH_Q)]["videos"]:
            row["publishedAt"] = "il y a 3 heures"
        result, _, _ = self.run_lane(routes)
        self.assertEqual(result.exit_code, pod.EXIT_PUBLISH_AGE_DRIFT)
        self.assertFalse(self.out.exists())

    def test_main_reports_total_failure_on_stderr(self):
        fake = FakeTuber(self.failing_routes())
        stderr = io.StringIO()
        with unittest.mock.patch.object(pod, "http_get_json", fake), redirect_stderr(stderr):
            rc = pod.main(["--registry", str(self.registry), "--out-dir", str(self.out),
                           "--now", "2026-10-30T08:41:00Z"])
        self.assertEqual(rc, 3)
        self.assertIn("total tuber-api fetch failure", stderr.getvalue())

    def test_main_happy_path_prints_one_line(self):
        fake = FakeTuber(e2e_routes())
        stdout = io.StringIO()
        with unittest.mock.patch.object(pod, "http_get_json", fake), \
                unittest.mock.patch.object(pod.time, "sleep"), redirect_stdout(stdout):
            rc = pod.main(["--registry", str(self.registry), "--out-dir", str(self.out),
                           "--now", "2026-10-30T08:41:00Z"])
        self.assertEqual(rc, 0)
        self.assertEqual(len(stdout.getvalue().strip().splitlines()), 1)
        self.assertIn("4/4 sources ok", stdout.getvalue())

    def test_main_rejects_bad_arguments(self):
        with redirect_stderr(io.StringIO()):
            self.assertEqual(pod.main(["--now", "yesterday"]), 2)
            self.assertEqual(pod.main(["--max-transcript-fetches", "-1"]), 2)
            self.assertEqual(pod.main(["--bogus"]), 2)


class SelectWindowsTest(unittest.TestCase):
    def transcript(self) -> list[dict]:
        segments = filler_segments(400)  # 0..1995 s
        segments[200] = {"startMs": 1_000_000, "text": INFORMATIVE}
        segments[300] = {"startMs": 1_500_000, "text": "Revenue rose 25% to $127.6 billion while Google Cloud grew 103%."}
        return segments

    def test_signature_is_keyword_only(self):
        with self.assertRaises(TypeError):
            pod.select_windows(self.transcript(), 6, 60)  # type: ignore[misc]

    def test_deterministic_and_order_independent(self):
        segments = self.transcript()
        first = pod.select_windows(segments, max_windows=6, max_words=60)
        self.assertEqual(first, pod.select_windows(copy.deepcopy(segments), max_windows=6, max_words=60))
        shuffled = list(reversed(segments))
        self.assertEqual(first, pod.select_windows(shuffled, max_windows=6, max_words=60))

    def test_caps_gap_order_and_verbatim(self):
        segments = self.transcript()
        windows = pod.select_windows(segments, max_windows=6, max_words=60)
        self.assertEqual(len(windows), 6)
        self.assertEqual([w["at_s"] for w in windows], sorted(w["at_s"] for w in windows))
        starts = [w["at_s"] for w in windows]
        self.assertTrue(all(b - a >= 120 for a, b in zip(starts, starts[1:])))
        corpus = " ".join(segment["text"] for segment in sorted(segments, key=lambda s: s["startMs"]))
        for window in windows:
            self.assertEqual(set(window), {"text", "at_s"})
            self.assertLessEqual(len(window["text"].split()), 60)
            self.assertIn(window["text"], corpus)
        self.assertIn(1000, starts)
        self.assertIn(1500, starts)

    def test_information_dense_windows_win(self):
        windows = pod.select_windows(self.transcript(), max_windows=2, max_words=60)
        self.assertEqual([w["at_s"] for w in windows], [1000, 1500])

    def test_sponsor_read_scores_low_even_when_dense(self):
        segments = filler_segments(400)
        segments[100] = {"startMs": 500_000, "text": SPONSOR_READ}
        segments[250] = {"startMs": 1_250_000, "text": "We expect revenue to grow 30% next year as GPU supply improves."}
        windows = pod.select_windows(segments, max_windows=1, max_words=60)
        self.assertEqual(windows[0]["at_s"], 1250)
        for window in pod.select_windows(segments, max_windows=6, max_words=60):
            self.assertNotIn("Use code", window["text"])

    def test_intro_and_outro_score_low(self):
        segments = filler_segments(400)
        segments[2] = {"startMs": 10_000, "text": INFORMATIVE}  # first 1%
        segments[397] = {"startMs": 1_985_000, "text": INFORMATIVE}  # last 1%
        segments[200] = {"startMs": 1_000_000, "text": INFORMATIVE}
        windows = pod.select_windows(segments, max_windows=1, max_words=60)
        self.assertEqual(windows[0]["at_s"], 1000)

    def test_unpunctuated_captions_use_fixed_word_windows(self):
        words = [token(i) for i in range(1200)]
        words[600:606] = ["revenue", "grew", "40", "percent", "to", "$3"]
        segments = [{"startMs": i * 2000, "text": " ".join(words[i * 8:(i + 1) * 8])} for i in range(150)]
        windows = pod.select_windows(segments, max_windows=3, max_words=50)
        self.assertEqual(len(windows), 3)
        self.assertTrue(all(len(w["text"].split()) <= 50 for w in windows))
        self.assertTrue(any("40 percent" in w["text"] for w in windows))
        stream = " ".join(words)
        self.assertTrue(all(w["text"] in stream for w in windows))

    def test_min_gap_keeps_windows_apart(self):
        segments = filler_segments(400)
        segments[200] = {"startMs": 1_000_000, "text": INFORMATIVE}
        segments[206] = {"startMs": 1_030_000, "text": INFORMATIVE.replace("2 gigawatts", "3 gigawatts")}
        segments[300] = {"startMs": 1_500_000, "text": "We expect revenue to grow 30% next year."}
        gapped = [w["at_s"] for w in pod.select_windows(segments, max_windows=2, max_words=30)]
        self.assertEqual(len(gapped), 2)
        self.assertGreaterEqual(gapped[1] - gapped[0], 120)
        packed = [w["at_s"] for w in pod.select_windows(segments, max_windows=2, max_words=30, min_gap_s=0)]
        self.assertEqual(packed, [1000, 1030])

    def test_caption_annotations_are_not_speech(self):
        segments = [{"startMs": i * 5000, "text": f">> [Music] {filler_sentence(i)} [ __ ]"} for i in range(50)]
        for window in pod.select_windows(segments, max_windows=3, max_words=40):
            self.assertNotIn("[", window["text"])
            self.assertNotIn(">>", window["text"])

    def test_degenerate_input(self):
        self.assertEqual(pod.select_windows([], max_windows=6, max_words=60), [])
        self.assertEqual(pod.select_windows(self.transcript(), max_windows=0, max_words=60), [])
        self.assertEqual(pod.select_windows(self.transcript(), max_windows=6, max_words=0), [])
        junk = [None, {"startMs": "x", "text": "a"}, {"startMs": -5, "text": "b"}, {"startMs": 1000},
                {"startMs": True, "text": "c"}, {"startMs": 2000, "text": "Only real line here."}]
        self.assertEqual(pod.select_windows(junk, max_windows=6, max_words=60),
                         [{"text": "Only real line here.", "at_s": 2}])

    def test_long_sentence_is_truncated_not_dropped(self):
        long_sentence = " ".join(token(i) for i in range(150)) + "."
        windows = pod.select_windows([{"startMs": 0, "text": long_sentence}], max_windows=2, max_words=60)
        self.assertEqual(len(windows), 1)
        self.assertEqual(len(windows[0]["text"].split()), 60)


if __name__ == "__main__":
    unittest.main()
