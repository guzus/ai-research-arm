#!/usr/bin/env python3
"""Tests for the durable RSS-to-Telegram blog subscription watcher."""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

import watch_blog_subscriptions as watcher  # noqa: E402


SOURCE = watcher.SubscriptionSource(
    id="tosoha1",
    name="이것 또한 지나가리라",
    url="https://blog.naver.com/tosoha1",
    feed_url="https://rss.blog.naver.com/tosoha1.xml",
)
NOW = dt.datetime(2026, 7, 15, 12, tzinfo=dt.timezone.utc)


def rss(*items: tuple[str | None, str, str, str], channel_date: str = "now") -> bytes:
    rendered_items = []
    for guid, title, link, published in items:
        guid_xml = f"<guid>{guid}</guid>" if guid is not None else ""
        rendered_items.append(
            f"""
            <item>
              {guid_xml}
              <title>{title}</title>
              <link>{link}</link>
              <pubDate>{published}</pubDate>
            </item>
            """
        )
    return (
        "<?xml version='1.0'?><rss version='2.0'><channel>"
        f"<pubDate>{channel_date}</pubDate>{''.join(rendered_items)}"
        "</channel></rss>"
    ).encode()


OLD = (
    "https://blog.naver.com/tosoha1/1",
    "기존 글",
    "https://blog.naver.com/tosoha1/1?fromRss=true&amp;trackingCode=rss",
    "Tue, 14 Jul 2026 17:30:00 +0900",
)
NEWER = (
    "https://blog.naver.com/tosoha1/3",
    "새 글 2",
    "https://blog.naver.com/tosoha1/3?fromRss=true&amp;trackingCode=rss",
    "Wed, 15 Jul 2026 18:30:00 +0900",
)
NEW = (
    "https://blog.naver.com/tosoha1/2",
    "새 글 1",
    "https://blog.naver.com/tosoha1/2?fromRss=true&amp;trackingCode=rss",
    "Wed, 15 Jul 2026 17:30:00 +0900",
)


class RegistryTest(unittest.TestCase):
    def test_only_entries_with_subscription_are_loaded(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "blogs.json"
            path.write_text(
                json.dumps(
                    [
                        {
                            "id": "ordinary",
                            "name": "Ordinary",
                            "url": "https://example.com",
                            "feed_url": "https://example.com/feed",
                        },
                        {
                            "id": "tosoha1",
                            "name": "이것 또한 지나가리라",
                            "url": "https://blog.naver.com/tosoha1",
                            "feed_url": "https://rss.blog.naver.com/tosoha1.xml",
                            "subscription": {"delivery": "telegram"},
                        },
                    ]
                ),
                encoding="utf-8",
            )

            sources = watcher.load_sources(path)

        self.assertEqual(sources, [SOURCE])

    def test_unknown_delivery_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "blogs.json"
            path.write_text(
                json.dumps(
                    [
                        {
                            "id": "tosoha1",
                            "name": "이것 또한 지나가리라",
                            "url": "https://blog.naver.com/tosoha1",
                            "feed_url": "https://rss.blog.naver.com/tosoha1.xml",
                            "subscription": {"delivery": "hooker"},
                        }
                    ]
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(watcher.SubscriptionError, "delivery must be 'telegram'"):
                watcher.load_sources(path)


class FeedContractTest(unittest.TestCase):
    def test_parser_uses_item_guid_and_not_channel_pubdate(self):
        first = watcher.parse_rss(SOURCE, rss(OLD, channel_date="request time one"))
        second = watcher.parse_rss(SOURCE, rss(OLD, channel_date="request time two"))

        self.assertEqual(first, second)
        self.assertEqual(first[0].guid, OLD[0])
        self.assertEqual(first[0].url, "https://blog.naver.com/tosoha1/1")

    def test_item_without_guid_falls_back_to_canonical_post_link(self):
        missing_guid = (None, "글", "https://blog.naver.com/tosoha1/1", OLD[3])

        items = watcher.parse_rss(SOURCE, rss(missing_guid, channel_date="request timestamp"))

        self.assertEqual(items[0].guid, "https://blog.naver.com/tosoha1/1")

    def test_url_shaped_guid_is_canonicalized_before_deduplication(self):
        tracked_guid = (
            "https://blog.naver.com/tosoha1/1?fromRss=true&amp;trackingCode=rss",
            OLD[1],
            OLD[2],
            OLD[3],
        )

        items = watcher.parse_rss(SOURCE, rss(tracked_guid))

        self.assertEqual(items[0].guid, "https://blog.naver.com/tosoha1/1")

    def test_post_link_must_stay_under_configured_blog_path(self):
        malicious = (
            "https://blog.naver.com/other/1",
            "다른 블로그",
            "https://blog.naver.com/other/1",
            OLD[3],
        )

        with self.assertRaisesRegex(watcher.SubscriptionError, "escapes configured blog path"):
            watcher.parse_rss(SOURCE, rss(malicious))


class PollAndAckTest(unittest.TestCase):
    def test_first_poll_seeds_every_historical_guid_without_alerting(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "state.json"
            pending = Path(directory) / "pending.json"

            result = watcher.poll_subscriptions(
                sources=[SOURCE],
                state_path=state,
                pending_path=pending,
                fetcher=lambda _: rss(NEWER, NEW, OLD),
                now=NOW,
            )

            self.assertEqual(result["seeded_sources"], ["tosoha1"])
            self.assertEqual(result["notifications"], [])
            saved = json.loads(state.read_text(encoding="utf-8"))
            self.assertEqual(
                saved["sources"]["tosoha1"]["seen_guids"],
                sorted([OLD[0], NEW[0], NEWER[0]]),
            )

    def test_unseen_posts_are_oldest_first_and_state_changes_only_after_ack(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "state.json"
            pending = Path(directory) / "pending.json"
            watcher.write_json_atomic(
                state,
                {
                    "version": 1,
                    "sources": {
                        "tosoha1": {
                            "seen_guids": [OLD[0]],
                            "updated_at": "2026-07-14T00:00:00Z",
                        }
                    },
                },
            )
            before = state.read_text(encoding="utf-8")

            result = watcher.poll_subscriptions(
                sources=[SOURCE],
                state_path=state,
                pending_path=pending,
                fetcher=lambda _: rss(NEWER, OLD, NEW),
                now=NOW,
            )

            self.assertEqual([item["guid"] for item in result["notifications"]], [NEW[0], NEWER[0]])
            self.assertEqual(state.read_text(encoding="utf-8"), before)
            notification = result["notifications"][0]
            self.assertEqual(set(notification["payload"]), {"text", "reply_markup"})
            self.assertNotIn("topic", notification)
            self.assertNotIn("idempotency_key", notification)

            acknowledged = watcher.ack_pending(state_path=state, pending_path=pending, now=NOW)

            self.assertEqual(acknowledged, 2)
            saved = json.loads(state.read_text(encoding="utf-8"))
            self.assertEqual(
                saved["sources"]["tosoha1"]["seen_guids"],
                sorted([OLD[0], NEW[0], NEWER[0]]),
            )

    def test_retry_after_ack_has_no_notifications(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "state.json"
            pending = Path(directory) / "pending.json"
            watcher.poll_subscriptions(
                sources=[SOURCE],
                state_path=state,
                pending_path=pending,
                fetcher=lambda _: rss(OLD),
                now=NOW,
            )
            second = watcher.poll_subscriptions(
                sources=[SOURCE],
                state_path=state,
                pending_path=pending,
                fetcher=lambda _: rss(NEW, OLD),
                now=NOW,
            )
            self.assertEqual(len(second["notifications"]), 1)
            watcher.ack_pending(state_path=state, pending_path=pending, now=NOW)

            third = watcher.poll_subscriptions(
                sources=[SOURCE],
                state_path=state,
                pending_path=pending,
                fetcher=lambda _: rss(NEW, OLD),
                now=NOW,
            )

            self.assertEqual(third["notifications"], [])

    def test_partial_success_acknowledges_only_the_accepted_item(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "state.json"
            pending = Path(directory) / "pending.json"
            watcher.poll_subscriptions(
                sources=[SOURCE],
                state_path=state,
                pending_path=pending,
                fetcher=lambda _: rss(OLD),
                now=NOW,
            )
            watcher.poll_subscriptions(
                sources=[SOURCE],
                state_path=state,
                pending_path=pending,
                fetcher=lambda _: rss(NEWER, NEW, OLD),
                now=NOW,
            )

            acknowledged = watcher.ack_pending(
                state_path=state,
                pending_path=pending,
                source_id="tosoha1",
                guid=NEW[0],
                now=NOW,
            )

            self.assertEqual(acknowledged, 1)
            saved = json.loads(state.read_text(encoding="utf-8"))
            self.assertIn(NEW[0], saved["sources"]["tosoha1"]["seen_guids"])
            self.assertNotIn(NEWER[0], saved["sources"]["tosoha1"]["seen_guids"])
            retry = watcher.poll_subscriptions(
                sources=[SOURCE],
                state_path=state,
                pending_path=pending,
                fetcher=lambda _: rss(NEWER, NEW, OLD),
                now=NOW,
            )
            self.assertEqual([item["guid"] for item in retry["notifications"]], [NEWER[0]])

    def test_malformed_existing_state_hard_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "state.json"
            pending = Path(directory) / "pending.json"
            state.write_text('{"version": 1, "sources": {"tosoha1": {}}}', encoding="utf-8")

            with self.assertRaisesRegex(watcher.SubscriptionError, "seen_guids"):
                watcher.poll_subscriptions(
                    sources=[SOURCE],
                    state_path=state,
                    pending_path=pending,
                    fetcher=lambda _: rss(OLD),
                    now=NOW,
                )


class TelegramDeliveryResponseTest(unittest.TestCase):
    def write_response(self, directory: str, value: object) -> Path:
        path = Path(directory) / "telegram.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_ok_message_for_expected_chat_proves_delivery(self):
        with tempfile.TemporaryDirectory() as directory:
            response = self.write_response(
                directory,
                {"ok": True, "result": {"message_id": 42, "chat": {"id": -100123}}},
            )

            message_id = watcher.verify_telegram_delivery(response, "-100123")

        self.assertEqual(message_id, 42)

    def test_http_200_style_ok_false_does_not_prove_delivery(self):
        with tempfile.TemporaryDirectory() as directory:
            response = self.write_response(directory, {"ok": False, "description": "rejected"})

            with self.assertRaisesRegex(watcher.SubscriptionError, "ok=true"):
                watcher.verify_telegram_delivery(response, "-100123")

    def test_wrong_destination_does_not_prove_delivery(self):
        with tempfile.TemporaryDirectory() as directory:
            response = self.write_response(
                directory,
                {"ok": True, "result": {"message_id": 42, "chat": {"id": -100999}}},
            )

            with self.assertRaisesRegex(watcher.SubscriptionError, "chat id"):
                watcher.verify_telegram_delivery(response, "-100123")

    def test_missing_message_id_does_not_prove_delivery(self):
        with tempfile.TemporaryDirectory() as directory:
            response = self.write_response(
                directory,
                {"ok": True, "result": {"chat": {"id": -100123}}},
            )

            with self.assertRaisesRegex(watcher.SubscriptionError, "message_id"):
                watcher.verify_telegram_delivery(response, "-100123")


if __name__ == "__main__":
    unittest.main()
