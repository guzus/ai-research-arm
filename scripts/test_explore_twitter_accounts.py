from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from explore_twitter_accounts import candidates_from_tweets


class TwitterAccountExplorerTests(unittest.TestCase):
    def test_candidates_from_tweets_scores_unknown_authors(self):
        tweets = [
            {
                "id": "1",
                "author": {"username": "newsignal"},
                "likeCount": 120,
                "retweetCount": 20,
                "replyCount": 4,
            },
            {
                "id": "2",
                "author": {"username": "newsignal"},
                "likeCount": 60,
                "retweetCount": 5,
                "replyCount": 1,
            },
            {
                "id": "3",
                "author": {"username": "OpenAI"},
                "likeCount": 10000,
                "retweetCount": 100,
                "replyCount": 50,
            },
        ]

        candidates = candidates_from_tweets(tweets, {"openai"}, min_score=3, max_candidates=10)

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["handle"], "newsignal")
        self.assertEqual(candidates[0]["category"], "others")
        self.assertEqual(candidates[0]["evidence"][0], "https://x.com/newsignal/status/1")

    def test_candidates_from_tweets_respects_threshold_and_cap(self):
        tweets = [
            {"id": str(index), "author": {"username": f"user{index}"}, "likeCount": 1000}
            for index in range(5)
        ]

        candidates = candidates_from_tweets(tweets, set(), min_score=2, max_candidates=2)

        self.assertEqual(len(candidates), 2)

    def test_candidates_from_tweets_uses_mention_graph_signal(self):
        tweets = [
            {
                "id": "1",
                "author": {"username": "seed1"},
                "text": "good thread by @networknode on AI infra",
                "likeCount": 20,
            },
            {
                "id": "2",
                "author": {"username": "seed2"},
                "text": "@networknode has the better sourcing here",
                "likeCount": 30,
            },
        ]

        candidates = candidates_from_tweets(tweets, set(), min_score=4, max_candidates=10)

        by_handle = {item["handle"]: item for item in candidates}
        self.assertIn("networknode", by_handle)
        self.assertEqual(by_handle["networknode"]["source"], "mention_graph")
        self.assertIn("@seed1", by_handle["networknode"]["reason"])
        self.assertTrue(by_handle["networknode"]["evidence"][0].startswith("cited in: "))

    def test_monitored_authors_still_contribute_mention_graph_signal(self):
        tweets = [
            {
                "id": "1",
                "author": {"username": "OpenAI"},
                "text": "interesting work from @networknode",
            },
            {
                "id": "2",
                "author": {"username": "AnthropicAI"},
                "text": "also watching @networknode",
            },
        ]

        candidates = candidates_from_tweets(tweets, {"openai", "anthropicai"}, min_score=4, max_candidates=10)

        self.assertEqual([item["handle"] for item in candidates], ["networknode"])

    def test_single_mention_does_not_clear_mention_graph_threshold(self):
        tweets = [
            {
                "id": "1",
                "author": {"username": "seed1"},
                "text": "one-off mention of @networknode",
                "likeCount": 10000,
            }
        ]

        candidates = candidates_from_tweets(tweets, set(), min_score=3, max_candidates=10)

        self.assertNotIn("networknode", {item["handle"] for item in candidates})


if __name__ == "__main__":
    unittest.main()
