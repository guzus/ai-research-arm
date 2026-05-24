#!/usr/bin/env python3
"""Deterministic, dependency-free feature extraction for a tweet.

This is the single source of truth for *what we measure about a tweet*. Both
``analyze_viral_tweets.py`` (which measures how each feature correlates with
engagement) and ``tweet_virality_verifier.py`` (which scores a draft) import
``extract_features`` from here, so the two can never drift apart.

Every feature is a content/*form* property the author controls when writing —
length, structure, media, hooks, punctuation — deliberately **not** topic or
author identity. Form is what transfers across accounts and is what a verifier
can give actionable advice about. All features are numeric (bools as 0/1).
"""
from __future__ import annotations

import re

# Emoji-ish codepoint ranges (pictographs, dingbats, flags, symbols). Good
# enough to count without pulling in an emoji dependency.
_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"   # symbols & pictographs (incl. supplemental)
    "\U00002600-\U000027BF"   # misc symbols + dingbats
    "\U0001F1E6-\U0001F1FF"   # regional indicators (flags)
    "\U00002B00-\U00002BFF"   # arrows / stars
    "\U00002190-\U000021FF"   # arrows
    "]"
)
_WORD_RE = re.compile(r"[A-Za-z']+")
_NUMBER_RE = re.compile(r"\d[\d,\.]*")
_URL_RE = re.compile(r"https?://\S+")
_HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
_MENTION_RE = re.compile(r"(?:^|\s)@\w+")
_FIRST_PERSON_RE = re.compile(r"\b(i|i'm|i've|i'll|my|me|we|we're|our|us)\b", re.IGNORECASE)
# A leading "label:" / "Title:" within the first ~40 chars => listicle/title hook.
_TITLE_COLON_RE = re.compile(r"^.{1,40}?:\s")


def extract_features(text: str, *, has_media: bool = False, is_quote: bool = False) -> dict[str, float]:
    """Return a flat ``{feature_name: value}`` dict for a single tweet.

    ``text`` is the raw tweet text as posted. ``has_media`` / ``is_quote`` come
    from the API (a writer can't read them off the text alone, e.g. the t.co
    media link looks like any other URL).
    """
    text = text or ""
    # Text with t.co / URLs removed, so length & word stats reflect prose, not
    # the opaque media/link shortener tokens.
    no_urls = _URL_RE.sub(" ", text)
    words = _WORD_RE.findall(no_urls)
    lines = [ln for ln in text.split("\n")]
    non_empty_lines = [ln for ln in lines if ln.strip()]
    allcaps = [w for w in words if len(w) >= 2 and w.isupper()]

    first_token = ""
    stripped = text.strip()
    if stripped:
        first_token = re.sub(r"[^A-Za-z]", "", stripped.split()[0])

    urls = _URL_RE.findall(text)
    hashtags = _HASHTAG_RE.findall(text)
    mentions = _MENTION_RE.findall(text)
    numbers = _NUMBER_RE.findall(no_urls)
    emojis = _EMOJI_RE.findall(text)

    char_len = len(text)
    word_count = len(words)

    feats: dict[str, float] = {
        # size / shape
        "char_len": float(char_len),
        "word_count": float(word_count),
        "avg_word_len": float(sum(len(w) for w in words) / word_count) if word_count else 0.0,
        "line_count": float(len(non_empty_lines)),
        "is_multiline": 1.0 if len(non_empty_lines) > 1 else 0.0,
        # media / references
        "has_media": 1.0 if has_media else 0.0,
        "is_quote": 1.0 if is_quote else 0.0,
        "url_count": float(len(urls)),
        "has_url": 1.0 if urls else 0.0,
        # tags / handles
        "hashtag_count": float(len(hashtags)),
        "has_hashtag": 1.0 if hashtags else 0.0,
        "mention_count": float(len(mentions)),
        "has_mention": 1.0 if mentions else 0.0,
        # hooks / punctuation
        "has_question": 1.0 if "?" in text else 0.0,
        "question_count": float(text.count("?")),
        "has_exclaim": 1.0 if "!" in text else 0.0,
        "exclaim_count": float(text.count("!")),
        "title_colon": 1.0 if _TITLE_COLON_RE.search(no_urls) else 0.0,
        # emphasis / tone
        "emoji_count": float(len(emojis)),
        "has_emoji": 1.0 if emojis else 0.0,
        "allcaps_words": float(len(allcaps)),
        "has_allcaps": 1.0 if allcaps else 0.0,
        "starts_caps_word": 1.0 if (len(first_token) >= 2 and first_token.isupper()) else 0.0,
        # content signals
        "has_numbers": 1.0 if numbers else 0.0,
        "number_groups": float(len(numbers)),
        "first_person": 1.0 if _FIRST_PERSON_RE.search(no_urls) else 0.0,
        "money_or_pct": 1.0 if ("$" in text or "%" in text) else 0.0,
    }
    return feats


# Stable, documented ordering for reports/tests.
FEATURE_NAMES = list(extract_features("seed text").keys())

# Which features are binary (0/1) vs continuous — used for reporting rates/lift.
BINARY_FEATURES = {
    "is_multiline", "has_media", "is_quote", "has_url", "has_hashtag",
    "has_mention", "has_question", "has_exclaim", "title_colon", "has_emoji",
    "has_allcaps", "starts_caps_word", "has_numbers", "first_person", "money_or_pct",
}


if __name__ == "__main__":  # tiny smoke / demo
    import json
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else "BREAKING: GPT-5 just dropped. Here's why it matters 🧵"
    print(json.dumps(extract_features(sample), indent=2))
