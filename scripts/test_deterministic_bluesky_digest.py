#!/usr/bin/env python3
"""Tests for the deterministic Bluesky fallback composer (fixture-based, no network)."""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import deterministic_bluesky_digest as bluesky  # noqa: E402

NOW = dt.datetime(2026, 7, 2, 10, 15, tzinfo=dt.timezone.utc)
TIMESTAMP = "2026-07-02 10:15 UTC"


def feed_item(
    *,
    handle: str = "emollick.bsky.social",
    text: str = "Homework really does matter for learning.",
    hours_ago: float = 5,
    likes: int = 10,
    reposts: int = 1,
    rkey: str = "3mphafafkek2g",
    reason: dict | None = None,
) -> dict:
    created = (NOW - dt.timedelta(hours=hours_ago)).isoformat().replace("+00:00", "Z")
    item: dict = {
        "post": {
            "author": {"handle": handle, "displayName": handle.split(".")[0]},
            "record": {"text": text, "createdAt": created},
            "likeCount": likes,
            "repostCount": reposts,
            "uri": f"at://did:plc:x/app.bsky.feed.post/{rkey}",
        }
    }
    if reason is not None:
        item["reason"] = reason
    return item


class ExtractPostsTest(unittest.TestCase):
    def test_parses_post_fields_and_link_rkey(self):
        posts = bluesky.extract_posts({"feed": [feed_item()]}, "emollick.json")

        self.assertEqual(len(posts), 1)
        post = posts[0]
        self.assertEqual(post.handle, "emollick.bsky.social")
        self.assertEqual(post.likes, 10)
        self.assertEqual(post.reposts, 1)
        self.assertEqual(post.rkey, "3mphafafkek2g")
        self.assertEqual(
            post.link,
            "https://bsky.app/profile/emollick.bsky.social/post/3mphafafkek2g",
        )

    def test_skips_reposts_with_reason_set(self):
        item = feed_item(reason={"$type": "app.bsky.feed.defs#reasonRepost"})
        self.assertEqual(bluesky.extract_posts({"feed": [item]}, "x.json"), [])

    def test_skips_structurally_broken_entries_but_keeps_good_ones(self):
        payload = {
            "feed": [
                {"post": {"author": {}, "record": {}}},  # missing everything
                "not-a-dict",
                feed_item(),
            ]
        }
        self.assertEqual(len(bluesky.extract_posts(payload, "x.json")), 1)

    def test_unexpected_shape_returns_empty(self):
        self.assertEqual(bluesky.extract_posts({"error": "nope"}, "x.json"), [])
        self.assertEqual(bluesky.extract_posts([], "x.json"), [])


class LoadPostsTest(unittest.TestCase):
    def test_malformed_json_file_is_skipped_and_others_survive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "broken.json").write_text("{not json", encoding="utf-8")
            (root / "good.json").write_text(
                json.dumps({"feed": [feed_item()]}), encoding="utf-8"
            )

            posts = bluesky.load_posts(root)

            self.assertEqual(len(posts), 1)


class SelectPostsTest(unittest.TestCase):
    def test_window_and_engagement_filters(self):
        posts = bluesky.extract_posts(
            {
                "feed": [
                    feed_item(rkey="fresh-engaged", hours_ago=2, likes=5, reposts=0),
                    feed_item(rkey="too-old", hours_ago=49, likes=100, reposts=10),
                    feed_item(rkey="low-engagement", hours_ago=1, likes=1, reposts=0),
                    feed_item(rkey="repost-only-signal", hours_ago=1, likes=0, reposts=1),
                ]
            },
            "x.json",
        )
        selected = bluesky.select_posts(posts, NOW)

        rkeys = [post.rkey for post in selected]
        self.assertIn("fresh-engaged", rkeys)
        self.assertIn("repost-only-signal", rkeys)  # >=1 repost qualifies
        self.assertNotIn("too-old", rkeys)
        self.assertNotIn("low-engagement", rkeys)

    def test_ranked_by_likes_plus_double_reposts(self):
        posts = bluesky.extract_posts(
            {
                "feed": [
                    feed_item(handle="a.bsky.social", rkey="r1", likes=10, reposts=0),  # 10
                    feed_item(handle="b.bsky.social", rkey="r2", likes=4, reposts=4),   # 12
                    feed_item(handle="c.bsky.social", rkey="r3", likes=11, reposts=0),  # 11
                ]
            },
            "x.json",
        )
        selected = bluesky.select_posts(posts, NOW)

        self.assertEqual([post.rkey for post in selected], ["r2", "r3", "r1"])

    def test_total_and_per_author_caps(self):
        feed = [
            feed_item(handle="prolific.bsky.social", rkey=f"p{i}", likes=50 - i)
            for i in range(6)
        ] + [
            feed_item(handle=f"other{i}.bsky.social", rkey=f"o{i}", likes=10 - i)
            for i in range(6)
        ]
        posts = bluesky.extract_posts({"feed": feed}, "x.json")
        selected = bluesky.select_posts(posts, NOW)

        self.assertEqual(len(selected), bluesky.MAX_TOTAL)
        prolific = [p for p in selected if p.handle == "prolific.bsky.social"]
        self.assertEqual(len(prolific), bluesky.MAX_PER_AUTHOR)


class RenderSectionTest(unittest.TestCase):
    def test_section_format_matches_append_step_contract(self):
        posts = bluesky.extract_posts({"feed": [feed_item()]}, "x.json")
        selected = bluesky.select_posts(posts, NOW)
        section = bluesky.render_section(TIMESTAMP, selected)

        lines = section.splitlines()
        self.assertEqual(lines[0], f"## {TIMESTAMP}")
        self.assertIn(bluesky.FALLBACK_HEADING, lines)
        self.assertTrue(any(line.startswith("### Highlights") for line in lines))
        self.assertIn(
            '- **@emollick.bsky.social**: "Homework really does matter for learning." - '
            "[link](https://bsky.app/profile/emollick.bsky.social/post/3mphafafkek2g) "
            "(❤️ 10, 🔄 1)",
            lines,
        )

    def test_zero_posts_writes_agent_contract_empty_message(self):
        section = bluesky.render_section(TIMESTAMP, [])

        self.assertEqual(
            section,
            f"## {TIMESTAMP}\n\n_No qualifying posts this cycle._\n",
        )

    def test_excerpt_is_clamped_and_whitespace_flattened(self):
        posts = bluesky.extract_posts(
            {"feed": [feed_item(text="line one\nline two   spaced " + "y" * 400)]},
            "x.json",
        )
        section = bluesky.render_section(TIMESTAMP, bluesky.select_posts(posts, NOW))

        self.assertIn("line one line two spaced", section)
        bullet = next(line for line in section.splitlines() if line.startswith("- "))
        self.assertLess(len(bullet), 350)


class MainTest(unittest.TestCase):
    def test_main_end_to_end_writes_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "data"
            input_dir.mkdir()
            (input_dir / "emollick.json").write_text(
                json.dumps({"feed": [feed_item()]}), encoding="utf-8"
            )
            out = root / ".tmp" / "bluesky-section.md"

            code = bluesky.main(
                [
                    "--input-dir",
                    str(input_dir),
                    "--out",
                    str(out),
                    "--timestamp",
                    TIMESTAMP,
                    "--now-utc",
                    NOW.isoformat(),
                ]
            )

            self.assertEqual(code, 0)
            text = out.read_text(encoding="utf-8")
            self.assertTrue(text.startswith(f"## {TIMESTAMP}"))
            self.assertIn("emollick.bsky.social", text)

    def test_window_anchors_on_now_utc_not_on_timestamp_heading(self):
        # The workflow's --timestamp is KST wall time mislabelled " UTC"
        # (+9h ahead of real UTC). Anchoring the window on it dropped posts
        # 39-48h old. A 45h-old post must survive a +9h-skewed heading.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "data"
            input_dir.mkdir()
            (input_dir / "old.json").write_text(
                json.dumps({"feed": [feed_item(hours_ago=45, likes=10)]}),
                encoding="utf-8",
            )
            out = root / "section.md"
            skewed_heading = (NOW + dt.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M UTC")

            code = bluesky.main(
                [
                    "--input-dir",
                    str(input_dir),
                    "--out",
                    str(out),
                    "--timestamp",
                    skewed_heading,
                    "--now-utc",
                    NOW.isoformat(),
                ]
            )

            self.assertEqual(code, 0)
            text = out.read_text(encoding="utf-8")
            # Heading text is used verbatim; the 45h-old post is selected
            # because the window anchors on --now-utc, not on the heading.
            self.assertTrue(text.startswith(f"## {skewed_heading}"))
            self.assertIn("emollick.bsky.social", text)
            self.assertNotIn("No qualifying posts", text)

    def test_main_with_missing_input_dir_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = bluesky.main(
                [
                    "--input-dir",
                    str(Path(tmp) / "absent"),
                    "--out",
                    str(Path(tmp) / "out.md"),
                    "--timestamp",
                    TIMESTAMP,
                ]
            )
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
