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

    def test_unverified_only_mentions_do_not_qualify(self):
        # seed1/seed2 are not in the monitored manifest, so their mentions are an
        # unverified (possibly spam-ring) signal. Even cited by two distinct
        # accounts, the candidate must be dropped — only trusted vouchers count.
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

        self.assertNotIn("networknode", {item["handle"] for item in candidates})

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
        networknode = candidates[0]
        self.assertEqual(networknode["source"], "mention_graph")
        self.assertIn("vouched by 2 monitored", networknode["reason"])
        self.assertTrue(networknode["evidence"][0].startswith("cited in: "))

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

    def test_topicality_lifts_on_topic_author_over_viral_off_topic(self):
        tweets = [
            # Off-topic but extremely viral — engagement alone must not dominate.
            {
                "id": "1",
                "author": {"username": "viralpundit"},
                "text": "huge breaking news today, everyone is talking about this",
                "likeCount": 100000,
            },
            # On-topic with modest engagement.
            {
                "id": "2",
                "author": {"username": "mlperson"},
                "text": "new open-weights LLM with strong inference benchmarks",
                "likeCount": 50,
            },
        ]

        candidates = candidates_from_tweets(tweets, set(), min_score=3, max_candidates=10)
        by_handle = {item["handle"]: item for item in candidates}

        self.assertIn("mlperson", by_handle)
        if "viralpundit" in by_handle:
            self.assertGreaterEqual(by_handle["mlperson"]["score"], by_handle["viralpundit"]["score"])

    def test_lone_trusted_mention_needs_corroboration(self):
        # One bare mention by a single trusted account, with no AI topicality and
        # no engagement, scores 3.0 — below the default bar of 4, so it is held
        # back until corroborated by topicality, more vouchers, or engagement.
        tweets = [
            {
                "id": "1",
                "author": {"username": "OpenAI"},
                "text": "watching @newcomer",
            }
        ]

        candidates = candidates_from_tweets(tweets, {"openai"}, min_score=4, max_candidates=10)

        self.assertNotIn("newcomer", {item["handle"] for item in candidates})


if __name__ == "__main__":
    unittest.main()
