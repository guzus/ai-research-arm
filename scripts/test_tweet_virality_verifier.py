#!/usr/bin/env python3
"""Tests for ``tweet_virality_verifier``.

Stdlib only. No network, and deliberately NO dependency on
``viral_tweets.jsonl`` or ``feature_weights.json`` — the module ships with
baked-in reviewed weights, so CI must pass with the data files absent.

Several tests are *regression guards* for the analyst review's two key
corrections: length is the primary lever (not ALL-CAPS), and the tool must
never advise adding ALL-CAPS (a topic/ticker artifact, not emphasis).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import tweet_virality_verifier as v

SCRIPT = Path(__file__).resolve().parent / "tweet_virality_verifier.py"

# Long + substantive (and happens to contain an ALL-CAPS word).
STRONG_DRAFT = (
    "BREAKING: the new model just shipped and the benchmarks are genuinely "
    "wild — it beats every prior release on reasoning, coding, and long "
    "context by a clear margin, and the API pricing somehow got cheaper too. "
    "This changes how a lot of teams will build for the rest of the year."
)
# Short, plain, lowercase — none of the levers.
WEAK_DRAFT = "this is a small update"
NO_CAPS_DRAFTS = [
    "",
    "hello world",
    "this is a quiet lowercase thought about language models and agents",
    WEAK_DRAFT,
]


def test_strong_outscores_weak():
    strong = v.score_tweet(STRONG_DRAFT)
    weak = v.score_tweet(WEAK_DRAFT)
    assert strong["score"] > weak["score"]
    assert strong["score"] - weak["score"] > 20  # meaningful gap, not rounding


def test_length_is_the_strongest_factor():
    """The reviewed conclusion: length is the primary lever, above ALL-CAPS."""
    weights = {f["name"]: f["weight"] for f in v.score_tweet("x")["factors"]}
    assert weights["length"] == max(weights.values())
    assert weights["length"] > weights["has_allcaps"] > weights["has_question"]


def test_length_and_question_each_raise_score():
    base = "the model shipped today"  # short, lowercase, no question
    longer = (
        "the model shipped today and here is a much longer, substantive "
        "description of exactly what changed across reasoning, coding, pricing "
        "and latency so the draft comfortably clears the winner length band"
    )
    with_q = "the model shipped today, but is that actually a big deal?"
    s_base = v.score_tweet(base)["score"]
    assert v.score_tweet(longer)["score"] > s_base
    assert v.score_tweet(with_q)["score"] > s_base


def test_allcaps_scored_but_never_suggested():
    """has_allcaps contributes when present, but is NEVER recommended."""
    plain = v.score_tweet("the model shipped today")
    caps = v.score_tweet("the model SHIPPED today")
    assert caps["score"] > plain["score"]  # it does contribute to the score
    caps_factor = {f["name"]: f for f in caps["factors"]}["has_allcaps"]
    assert caps_factor["present"] is True and caps_factor["contribution"] > 0
    # ...but no draft is ever told to add caps.
    for res in (plain, caps):
        assert not _mentions_caps_advice(res["suggestions"])


def test_no_cargo_cult_caps_advice():
    """Regression guard: drafts lacking caps must not be told to add them."""
    for text in NO_CAPS_DRAFTS:
        res = v.score_tweet(text)
        assert not _mentions_caps_advice(res["suggestions"]), text[:30]


def test_dropped_artifacts_are_not_scored():
    """has_numbers / money_or_pct / hashtag / media were confirmed artifacts."""
    names = {f["name"] for f in v.score_tweet("up 50% to $1B today #ai").get("factors", [])}
    assert names == {"length", "has_allcaps", "has_question"}
    for dropped in ("has_numbers", "money_or_pct", "has_hashtag", "has_media", "has_emoji"):
        assert dropped not in names


def test_score_in_range_for_edge_inputs():
    huge = "WOW " * 5000
    for text in ["", " ", WEAK_DRAFT, STRONG_DRAFT, huge, "?", "$100 50% UP!"]:
        res = v.score_tweet(text)
        assert 0.0 <= res["score"] <= 100.0, (text[:20], res["score"])
        assert res["verdict"] in {"weak", "promising", "strong"}


def test_empty_string_is_weak_with_suggestions():
    res = v.score_tweet("")
    assert res["score"] == 0.0
    assert res["verdict"] == "weak"
    assert res["suggestions"], "an empty draft should suggest the missing levers"


def test_bare_allcaps_shout_is_not_promising():
    """A 3-word ticker shout shouldn't be flattered as 'promising'."""
    res = v.score_tweet("$BTC NEW ATH")
    assert res["verdict"] == "weak"


def test_determinism():
    a = v.score_tweet(STRONG_DRAFT, has_media=True, is_quote=False)
    b = v.score_tweet(STRONG_DRAFT, has_media=True, is_quote=False)
    assert a == b
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_suggestions_surface_length_lever():
    res = v.score_tweet(WEAK_DRAFT)
    blob = " ".join(res["suggestions"]).lower()
    assert "substantive" in blob  # the primary lever is surfaced
    assert "question" in blob     # the weak tertiary lever
    assert not _mentions_caps_advice(res["suggestions"])


def test_no_suggestions_when_levers_present():
    res = v.score_tweet(STRONG_DRAFT + " Is that actually a big deal?")
    # Long + question present; caps never suggested -> nothing left to advise.
    assert res["suggestions"] == []
    assert res["verdict"] == "strong"


def test_factor_strength_labels():
    by_name = {f["name"]: f for f in v.score_tweet(STRONG_DRAFT)["factors"]}
    assert by_name["length"]["strength"] == "primary"
    assert by_name["has_allcaps"]["strength"] == "weak"
    assert by_name["has_question"]["strength"] == "weak"


def test_weights_constant_shape():
    assert abs(sum(v.WEIGHTS.values()) - 100.0) < 1e-9
    assert v.WEIGHTS["length"] == max(v.WEIGHTS.values())


def test_disclaimer_is_honest():
    d = v.score_tweet(STRONG_DRAFT)["disclaimer"].lower()
    assert "not a like" in d
    assert "nudge" in d or "not a forecast" in d


def test_cli_json_smoke():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), STRONG_DRAFT, "--json"],
        capture_output=True, text=True, cwd=str(SCRIPT.parent),
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert set(payload) >= {"score", "verdict", "factors", "suggestions", "disclaimer"}
    assert 0.0 <= payload["score"] <= 100.0


def test_cli_human_smoke():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), WEAK_DRAFT],
        capture_output=True, text=True, cwd=str(SCRIPT.parent),
    )
    assert proc.returncode == 0, proc.stderr
    assert "Conformance score:" in proc.stdout
    assert "Suggestions" in proc.stdout


# --- round 2: assess_overperformance ---------------------------------------
STANCE_DRAFT = ("I think the AI-detection panic is wrong. The real reason students "
                "get flagged is broken tools, not cheating.")
PLAIN_DRAFT = "the model shipped today"


def test_overperformance_keys():
    res = v.assess_overperformance(PLAIN_DRAFT)
    assert set(res) >= {"levers_present", "suggestions", "anti_levers", "note"}


def test_overperformance_detects_stance():
    res = v.assess_overperformance(STANCE_DRAFT)
    assert "stance" in {lv["name"] for lv in res["levers_present"]}
    assert not any("stance" in s.lower() for s in res["suggestions"])  # present -> not suggested


def test_overperformance_suggests_media_when_missing():
    res = v.assess_overperformance(PLAIN_DRAFT, has_media=False)
    assert "media" not in {lv["name"] for lv in res["levers_present"]}
    assert any(("media" in s.lower() or "visual" in s.lower()) for s in res["suggestions"])


def test_overperformance_media_is_primary_lever():
    """Bigger AI corpus: attaching media is the one within-author-robust lever."""
    with_media = v.assess_overperformance(PLAIN_DRAFT, has_media=True)
    assert "media" in {lv["name"] for lv in with_media["levers_present"]}
    # media must NOT be advertised as something to add when it's already there
    assert not any("media" in s.lower() or "visual" in s.lower() for s in with_media["suggestions"])
    # ...and media is no longer an anti-lever (round-1 said it was; bigger data flipped it)
    assert "media" not in with_media["anti_levers"]


def test_overperformance_does_not_reward_text_form():
    """Length/caps are anti-levers here — a long shouty text-only tweet earns no levers."""
    res = v.assess_overperformance("THIS IS HUGE " * 30, has_media=False)
    names = {lv["name"] for lv in res["levers_present"]}
    assert "length" not in names and "media" not in names
    assert "length" in res["anti_levers"] and "ALL-CAPS" in res["anti_levers"]


def test_overperformance_note_is_honest():
    note = v.assess_overperformance(PLAIN_DRAFT)["note"].lower()
    assert "reach" in note and "not a prediction" in note


def test_overperformance_deterministic():
    assert v.assess_overperformance(STANCE_DRAFT) == v.assess_overperformance(STANCE_DRAFT)


def test_cli_overperformance_json_smoke():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), STANCE_DRAFT, "--overperformance", "--json"],
        capture_output=True, text=True, cwd=str(SCRIPT.parent),
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert "levers_present" in payload and "note" in payload


# --- bookmarks: assess_saveability -----------------------------------------
SAVE_DENSE = (
    "Here is the full breakdown of how we cut inference latency by 42% and cost by "
    "roughly 3x over 6 weeks. We moved off the managed API to a self-hosted cluster, "
    "tuned batch sizes from 8 to 32, switched to fp8, and pre-warmed 4 replicas. p50 "
    "dropped from 900ms to 520ms, p99 from 3.1s to 1.4s, and monthly spend fell from "
    "$48k to about $17k. Full numbers, configs, and the 3 gotchas that cost us a week."
)
PLAIN_SHORT = "shipped a small update"


def test_saveability_keys():
    res = v.assess_saveability(PLAIN_SHORT)
    assert set(res) >= {"score", "verdict", "factors", "suggestions", "disclaimer"}


def test_saveability_in_range():
    for text in ["", " ", PLAIN_SHORT, SAVE_DENSE, "WOW " * 4000, "42% $1B 2030"]:
        for media in (False, True):
            res = v.assess_saveability(text, has_media=media)
            assert 0.0 <= res["score"] <= 100.0, (text[:20], res["score"])
            assert res["verdict"] in {"weak", "promising", "strong"}


def test_saveability_rewards_info_density():
    dense = v.assess_saveability(SAVE_DENSE, has_media=True)["score"]
    plain = v.assess_saveability(PLAIN_SHORT)["score"]
    assert dense > plain and dense - plain > 30


def test_saveability_media_and_numbers_each_raise_score():
    base = v.assess_saveability("a quiet lowercase thought about models")["score"]
    assert v.assess_saveability("a quiet lowercase thought about models", has_media=True)["score"] > base
    assert v.assess_saveability("a quiet lowercase thought about 3 models")["score"] > base


def test_saveability_never_advises_caps():
    for text in ["", PLAIN_SHORT, "a quiet lowercase note", SAVE_DENSE]:
        assert not _mentions_caps_advice(v.assess_saveability(text)["suggestions"]), text[:20]


def test_saveability_suggests_clean_levers_when_missing():
    blob = " ".join(v.assess_saveability(PLAIN_SHORT)["suggestions"]).lower()
    assert "substantive" in blob and "number" in blob and "visual" in blob


def test_saveability_clean_levers_dominate():
    weights = {f["name"]: f["weight"] for f in v.assess_saveability("x")["factors"]}
    assert weights["has_allcaps"] < min(weights["length"], weights["has_numbers"], weights["has_media"])
    clean = weights["length"] + weights["has_numbers"] + weights["has_media"]
    assert clean >= 0.8 * sum(weights.values())


def test_saveability_factor_labels():
    by_name = {f["name"]: f for f in v.assess_saveability(SAVE_DENSE)["factors"]}
    assert {"length", "has_numbers", "has_media", "has_allcaps"} <= set(by_name)
    assert by_name["has_allcaps"]["strength"] == "weak/hype"
    assert by_name["length"]["strength"] == "clean"


def test_saveability_determinism():
    assert v.assess_saveability(SAVE_DENSE, has_media=True) == v.assess_saveability(SAVE_DENSE, has_media=True)


def test_cli_saveability_json_smoke():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), SAVE_DENSE, "--saveability", "--media", "--json"],
        capture_output=True, text=True, cwd=str(SCRIPT.parent),
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert set(payload) >= {"score", "verdict", "factors", "suggestions"}
    assert 0.0 <= payload["score"] <= 100.0


def _mentions_caps_advice(suggestions: list[str]) -> bool:
    """True if any suggestion tells the user to add caps/ALL-CAPS."""
    blob = " ".join(suggestions).lower()
    return "caps" in blob or "all-caps" in blob or "capital" in blob


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-q"]))
