#!/usr/bin/env python3
"""Deterministic *content / rhetorical* features for a tweet.

`tweet_features.py` measures surface FORM (length, caps, punctuation). This
module measures what the tweet *does* — its rhetorical move — which is what the
round-1 analysis was blind to. Same contract: pure, stdlib-only, every feature
numeric (bools as 0/1), shared by the analyzer and (if a signal survives) the
verifier so they can't drift.

These are heuristic detectors (keyword/structure), so they trade recall for
determinism and zero dependencies. They are validated against the qualitative
read in `research/twitter-viral/overperformance_qualitative.md`.
"""
from __future__ import annotations

import re

_THREAD = re.compile(r"🧵|👇|\bthread\b", re.IGNORECASE)
_THREAD_NUM = re.compile(r"^\s*1\s*[\./)]\s", re.MULTILINE)  # "1/" "1." "1)" opener
_ANNOUNCE = re.compile(
    r"\b(introducing|announc\w+|launch\w+|shipp\w+|released?|releasing|"
    r"now (?:available|live)|excited to|thrilled to|proud to|"
    r"we['’]re (?:launching|building|shipping)|just (?:shipped|launched|released|built))\b",
    re.IGNORECASE)
_PERSONAL = re.compile(
    r"\b(i|we)\b[^.?!]{0,60}\b(built|made|spent|quit|tried|learned|started|"
    r"failed|shipped|launched|realized|realised|discovered|found|wrote|left)\b",
    re.IGNORECASE)
_OPINION = re.compile(
    r"\b(unpopular opinion|hot take|controversial|honestly|the truth is|"
    r"nobody (?:talks|tells|wants)|everyone(?:'s| is) wrong|you should|"
    r"the real reason|here'?s the thing|change my mind|imo|in my opinion|"
    r"i think|i believe|let'?s be honest|the problem (?:with|is))\b",
    re.IGNORECASE)
_ADVICE = re.compile(
    r"\b(how to|here'?s how|the trick|the secret|the key to|tip:|pro tip|"
    r"\d+ tips|lesson|steps to|if you want to|the best way to|you need to)\b",
    re.IGNORECASE)
_PREDICTION = re.compile(
    r"\b(by 20\d\d|the future of|is the future|is dead|will (?:be|change|kill|"
    r"replace|win|never)|going to|prediction|coming soon|next year)\b",
    re.IGNORECASE)
_NEWS = re.compile(
    r"\b(breaking|just in|confirmed|reportedly|sources say|update:|developing|"
    r"announced|has (?:died|passed))\b",
    re.IGNORECASE)
_QUESTION_HOOK = re.compile(
    r"^\s*\W*(what|why|how|who|when|where|is|are|should|can|could|would|do|does|"
    r"did|will|if|which)\b",
    re.IGNORECASE)
_LIST = re.compile(r"(?:^\s*\d\s*[\.\)]\s.*\n?){2,}", re.MULTILINE)
_N_THINGS = re.compile(
    r"\b\d+\s+(things|ways|reasons|lessons|tips|steps|rules|signs|mistakes|"
    r"facts|tools|tricks|examples)\b",
    re.IGNORECASE)
_GRATITUDE = re.compile(r"\b(thank\w*|grateful|honou?red|blessed|proud of)\b", re.IGNORECASE)
_CURIOSITY = re.compile(
    r"\b(here'?s why|this is why|the reason|what happened|you won'?t believe|"
    r"wait (?:until|til|till)|turns out|here'?s what|watch this)\b",
    re.IGNORECASE)
_SUPERLATIVE = re.compile(
    r"\b(insane|crazy|wild|huge|massive|game.?chang\w+|mind.?blow\w+|"
    r"unbelievable|shocking|incredible|amazing|biggest|fastest|revolutionary|"
    r"historic|unprecedented|best|worst|first ever|never before)\b",
    re.IGNORECASE)
_NEGATION = re.compile(
    r"\b(no|not|never|stop|fail\w*|wrong|worst|scam|hate|broke\w*|dead|kill\w*|"
    r"don'?t|can'?t|won'?t|nobody|nothing|isn'?t|aren'?t)\b",
    re.IGNORECASE)
# is_stance: a first-person claim or a correction of someone's take. The best
# content lever by pooled lift (~1.9x), but barely real: after removing a regex
# artifact (a bare "actually" intensifier had inflated it ~27%), it is ~chance
# WITHIN author (AUC ~0.51, paired sign even leans negative). The defensible
# round-2 finding is negative — see overperformance_analysis.md.
# Correction phrases below are kept deliberately specific to avoid firing on
# "actually" / "not a ..." used as ordinary intensifiers/negations.
_STANCE_FIRST_PERSON = re.compile(
    r"\b(i|we)\b[^.?!]{0,40}\b(think|believe|handled|asked|don'?t|wouldn'?t|"
    r"won'?t|disagree|argue|claim|refuse)\b",
    re.IGNORECASE)
_STANCE_CORRECTION = re.compile(
    r"(\bthe real reason\b|\bthe truth is\b|\bfact[- ]?check\b|"
    r"\bthat'?s (false|not true|wrong|nonsense)\b|"
    r"\bhere'?s the (thing|truth)\b|\bno,? that'?s not\b|"
    r"\b(stop|quit) (saying|pretending|acting)\b)",
    re.IGNORECASE)


def extract_content_features(text: str) -> dict[str, float]:
    """Return ``{feature: value}`` rhetorical features for one tweet."""
    text = text or ""
    stripped = text.strip()
    is_thread = bool(_THREAD.search(text) or _THREAD_NUM.search(text))
    is_list = bool(_LIST.search(text) or _N_THINGS.search(text))
    superl = len(_SUPERLATIVE.findall(text))
    neg = len(_NEGATION.findall(text))
    return {
        "is_thread": 1.0 if is_thread else 0.0,
        "is_announcement": 1.0 if _ANNOUNCE.search(text) else 0.0,
        "is_personal": 1.0 if _PERSONAL.search(text) else 0.0,
        "starts_with_i": 1.0 if stripped[:2].lower() == "i " else 0.0,
        "is_opinion": 1.0 if _OPINION.search(text) else 0.0,
        "is_stance": 1.0 if (_STANCE_FIRST_PERSON.search(text) or _STANCE_CORRECTION.search(text)) else 0.0,
        "is_advice": 1.0 if _ADVICE.search(text) else 0.0,
        "is_prediction": 1.0 if _PREDICTION.search(text) else 0.0,
        "is_news_break": 1.0 if _NEWS.search(text) else 0.0,
        "is_question_hook": 1.0 if _QUESTION_HOOK.search(stripped) else 0.0,
        "is_list": 1.0 if is_list else 0.0,
        "is_gratitude": 1.0 if _GRATITUDE.search(text) else 0.0,
        "is_curiosity_gap": 1.0 if _CURIOSITY.search(text) else 0.0,
        "superlative_count": float(superl),
        "has_superlative": 1.0 if superl else 0.0,
        "negation_count": float(neg),
        "has_negation": 1.0 if neg else 0.0,
    }


CONTENT_FEATURE_NAMES = list(extract_content_features("seed").keys())
BINARY_CONTENT_FEATURES = {
    n for n in CONTENT_FEATURE_NAMES if not n.endswith("_count")
}


if __name__ == "__main__":
    import json
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else (
        "Introducing our new model 🧵 here's why it's the biggest leap yet")
    print(json.dumps(extract_content_features(sample), indent=2))
