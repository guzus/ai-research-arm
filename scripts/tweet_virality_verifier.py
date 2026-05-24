#!/usr/bin/env python3
"""Score how much a tweet draft *resembles* tweets that cleared 100 likes.

This is a **conformance scorer / writing nudge**, NOT a like-count predictor.
It answers one narrow question — "does this draft have the *form* properties
that co-occur with >=100-like tweets in our sample?" — and surfaces the one or
two levers the data actually supports.

Two questions, two functions:

- ``score_tweet`` (round 1) — RAW-LIKES conformance: does this resemble tweets
  that pulled >=100 absolute likes? Validated AUC ~0.67 — but raw likes mostly
  track follower count, so a high score largely means "you write like a big
  account."
- ``assess_overperformance`` (round 2) — the *better* question: what (weakly)
  helps a tweet beat its OWN author's median? On the larger AI-focused corpus
  (3924 tweets, 57 authors) NO single feature is robust; attaching **media** is
  the most *consistent* (but small) edge (over-performers 72% vs 65%; ~74% of
  authors). Text form and content moves are ~chance within author. Out-of-sample
  the whole model is weak (LOO within-author ~0.60); reach, timing and luck
  dominate. See research/twitter-viral/SYNTHESIS.md.

Grounding: built from `research/twitter-viral/viral_tweets.jsonl` (677 tweets,
484 high / 193 low) and stress-tested in `research/twitter-viral/analysis.md`
and `analyst_review.md`. The weights below are the *reviewed* conclusion, not a
naive correlation ranking — see WHY-THESE-WEIGHTS.

Read this before trusting the number (the honest version):

- **Who tweets dominates, not how.** Author identity alone separates high from
  low at AUC ~= 0.82. This whole scorer adds only a faint signal — global
  AUC ~= 0.67, within-author AUC ~= 0.64 — and actively misfires for some
  account types (5 of the 19 dual authors are anti-predictive). Follower count
  is not modeled at all.
- **Length is the one semi-stable lever.** Longer, more substantive / multi-line
  posts do better even within the same author. This is the only feature that
  survives both the follower-controlled and same-source checks.
- **ALL-CAPS is mostly a topic artifact, NOT emphasis.** In the data, the
  all-caps tokens in winners are overwhelmingly tickers / acronyms / topic words
  (AI, BTC, NVDA, IRAN) — not "BREAKING/HUGE". It collapses to a coin flip
  (AUC ~= 0.50) once you compare same-source tweets. We *score* it (it does
  co-occur with winners) but we deliberately **never advise "add ALL-CAPS"** —
  that would be cargo-culting a markets/news-account signal.
- **Correlation, not causation; selection bias baked in.** Positives are partly
  X "Top" search results; negatives are an author's own timeline. The score
  measures resemblance to tweets that *got surfaced*, not a like forecast.

Feature extraction is delegated to ``tweet_features.extract_features`` so this
module can never drift from the analyzer that produced the evidence.

CLI::

    python scripts/tweet_virality_verifier.py "draft text" [--media] [--quote] [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from tweet_features import extract_features
from tweet_content import extract_content_features

# ---------------------------------------------------------------------------
# Reference numbers from the analysis (high vs low), used to normalize the
# length factor and to word the suggestions with real figures.
#   char_len:   high ~281 / low ~149      word_count: high ~43.5 / low ~23
#   has_allcaps rate: high 66% / low 41%  (kept for the note, NOT for advice)
# ---------------------------------------------------------------------------
_LEN_LOW_CHARS, _LEN_HIGH_CHARS = 149.0, 281.0
_LEN_LOW_WORDS, _LEN_HIGH_WORDS = 23.0, 43.5

# ---------------------------------------------------------------------------
# WHY-THESE-WEIGHTS (reviewed constants; see analyst_review.md)
# ---------------------------------------------------------------------------
# The naive ranking by global correlation r puts has_allcaps first. The
# independent review showed that r is inflated by (a) between-author topic
# differences and (b) mixing X "Top" search results with timeline tweets. After
# controlling for author AND source, the picture is:
#
#   length        PRIMARY  — only feature stable within-author (0.63) AND
#                            same-source (0.56). The real, if weak, lever.
#   has_allcaps   weak     — largest raw r but ~97% tickers/topic, drops to
#                            AUC 0.50 same-source. Scored (it co-occurs) but
#                            never recommended.
#   has_question  weak     — promoted from the rejects: consistent paired sign
#                            (11/13 nonzero authors). Lowest-confidence lever.
#
# Relative emphasis 0.5 / 0.3 / 0.2 (analyst's recommendation), as a 100-pt
# budget. Deliberately DROPPED as actionable: has_hashtag (pure source
# artifact), has_media / has_emoji / has_numbers / money_or_pct (failed the
# within-author control — author-style, not writing tactics).
WEIGHTS: dict[str, float] = {
    "length": 50.0,        # primary, most stable lever
    "has_allcaps": 30.0,   # weak; scored but never advised (topic artifact)
    "has_question": 20.0,  # weak; lowest-confidence lever
}

# Verdict bucketing on the 0-100 conformance score. Tuned so:
#   - length alone (50)            -> "promising"  (the one real lever)
#   - a bare ALL-CAPS shout (30)   -> "weak"       (don't reward ticker spam)
#   - length + another signal (>=70)-> "strong"
_PROMISING_MIN = 35.0
_STRONG_MIN = 70.0


def _length_strength(char_len: float, word_count: float) -> float:
    """Map raw length onto [0, 1] using the low/high means as anchors.

    0.0 at or below the low-tweet average, 1.0 at or above the high-tweet
    average. We take the max of the char- and word-based fractions (they are
    collinear, r=0.994 — one axis) so a single length factor isn't penalised by
    tokenization quirks.
    """
    def frac(value: float, low: float, high: float) -> float:
        return (value - low) / (high - low) if high > low else 0.0

    by_chars = frac(char_len, _LEN_LOW_CHARS, _LEN_HIGH_CHARS)
    by_words = frac(word_count, _LEN_LOW_WORDS, _LEN_HIGH_WORDS)
    return max(0.0, min(1.0, max(by_chars, by_words)))


def score_tweet(text: str, *, has_media: bool = False, is_quote: bool = False) -> dict[str, Any]:
    """Score a draft for *conformance* to >=100-like tweets (0-100).

    Returns a deterministic dict:

    - ``score`` (float, 0-100): conformance score — how much the draft has the
      form properties that co-occur with high-engagement tweets. **Not** a
      predicted like count.
    - ``verdict`` (str): ``"weak"`` / ``"promising"`` / ``"strong"``.
    - ``factors`` (list[dict]): one entry per scored factor with ``name``,
      ``present``/``value``, ``weight`` (max pts), ``contribution`` (pts
      awarded), ``strength`` (``"primary"``/``"weak"``) and a human ``note``.
    - ``suggestions`` (list[str]): levers the draft is missing *that the data
      supports recommending*. Notably this never tells you to add ALL-CAPS.
    - ``disclaimer`` (str): the honesty note.

    ``has_media`` / ``is_quote`` come from the API and can't be read off the
    text; they're accepted for parity with the dataset but are not scored
    (both failed the within-author control).
    """
    feats = extract_features(text, has_media=has_media, is_quote=is_quote)
    factors: list[dict[str, Any]] = []
    suggestions: list[str] = []
    score = 0.0

    # --- PRIMARY: length (char_len + word_count collapsed to one axis) -------
    char_len, word_count = feats["char_len"], feats["word_count"]
    strength = _length_strength(char_len, word_count)
    contrib_len = WEIGHTS["length"] * strength
    score += contrib_len
    factors.append({
        "name": "length",
        "value": {"chars": int(char_len), "words": int(word_count)},
        "strength_frac": round(strength, 3),
        "weight": WEIGHTS["length"],
        "contribution": round(contrib_len, 2),
        "strength": "primary",
        "note": (
            "Substantive / multi-line length — the one lever stable within "
            f"author. Winners average ~{int(_LEN_HIGH_CHARS)} chars / "
            f"~{int(_LEN_HIGH_WORDS)} words vs ~{int(_LEN_LOW_CHARS)} / "
            f"~{int(_LEN_LOW_WORDS)} for flops."
        ),
    })
    if strength < 0.5:
        suggestions.append(
            "Make it more substantive (ideally multi-line) — winners average "
            f"~{int(_LEN_HIGH_CHARS)} chars / ~{int(_LEN_HIGH_WORDS)} words vs "
            f"~{int(_LEN_LOW_CHARS)} / ~{int(_LEN_LOW_WORDS)}. This is the only "
            "lever that held up within-author; write substance, don't pad."
        )

    # --- WEAK: has_allcaps (scored, but NEVER advised — topic artifact) ------
    has_allcaps = feats["has_allcaps"] >= 1.0
    contrib_caps = WEIGHTS["has_allcaps"] if has_allcaps else 0.0
    score += contrib_caps
    factors.append({
        "name": "has_allcaps",
        "present": has_allcaps,
        "value": int(feats["allcaps_words"]),
        "weight": WEIGHTS["has_allcaps"],
        "contribution": round(contrib_caps, 2),
        "strength": "weak",
        "note": (
            "ALL-CAPS token(s) present. Co-occurs with winners (66% vs 41%) but "
            "is ~97% tickers/acronyms/topic (AI, BTC, NVDA), not emphasis, and "
            "collapses to a coin flip same-source. Scored, NOT a lever — we do "
            "not suggest adding caps."
        ),
    })
    # Intentionally NO suggestion for has_allcaps (see module docstring).

    # --- WEAK: has_question (lowest-confidence genuine lever) ----------------
    has_question = feats["has_question"] >= 1.0
    contrib_q = WEIGHTS["has_question"] if has_question else 0.0
    score += contrib_q
    factors.append({
        "name": "has_question",
        "present": has_question,
        "weight": WEIGHTS["has_question"],
        "contribution": round(contrib_q, 2),
        "strength": "weak",
        "note": (
            "Contains a question. Weak, lowest-confidence lever: consistent "
            "paired sign (11/13 authors) but it did not clear the robustness "
            "bar. A genuine question, not a rhetorical tic."
        ),
    })
    if not has_question:
        suggestions.append(
            "If it fits naturally, pose a genuine question (weak, "
            "lowest-confidence lever — don't force it)."
        )

    score = max(0.0, min(100.0, score))
    if score >= _STRONG_MIN:
        verdict = "strong"
    elif score >= _PROMISING_MIN:
        verdict = "promising"
    else:
        verdict = "weak"

    return {
        "score": round(score, 1),
        "verdict": verdict,
        "factors": factors,
        "suggestions": suggestions,
        "disclaimer": (
            "Conformance score (form resemblance to >=100-like tweets in a "
            "small AI/markets/news sample), NOT a like prediction. Who tweets "
            "dominates: author identity alone scores AUC ~0.82; this scorer "
            "adds only ~0.67 global / ~0.64 within-author and misfires for some "
            "accounts. Length is the one semi-stable lever; ALL-CAPS reflects "
            "tickers/topic (don't add caps to chase likes). Use as a writing "
            "nudge, not a forecast."
        ),
    }


# ---------------------------------------------------------------------------
# Round 2: over-performance guidance (what helps a tweet beat its OWN baseline)
# ---------------------------------------------------------------------------
# On the larger AI-focused corpus (3924 tweets, 51 dual authors) NO feature is
# robust. Attaching MEDIA is the most *consistent* direction (over-performers 72%
# vs 65% of an author's normal tweets; ~74% of authors lean positive) but the
# effect is small (lift 1.11) and shrank as the sample grew. Everything below is
# ~chance within author. We still surface media as the least-bad nudge, labeled
# honestly. (Stance, an earlier "best content lever," did not survive: AUC ~0.50.)
_WEAK_CONTENT = [
    ("is_stance", "stance",
     "First-person stance / correction — the qualitative read liked it, but ~chance "
     "within author on the bigger sample. Unproven."),
    ("is_question_hook", "question_hook", "Question hook — weak/unproven."),
    ("is_news_break", "news_break", "News-break framing — weak; mostly news-cycle timing."),
    ("is_curiosity_gap", "curiosity_gap", "Curiosity gap ('here's why…') — weak; topic-shaped."),
    ("is_list", "standalone_list", "Self-contained list / data-drop — weak; likes under-count saves."),
]


def assess_overperformance(text: str, *, has_media: bool = False, is_quote: bool = False) -> dict[str, Any]:
    """Round-2 guidance: what (weakly) helps a tweet beat its AUTHOR'S baseline.

    Unlike ``score_tweet`` (raw-likes conformance), this reflects the
    reach-controlled analysis on the larger AI-focused corpus. No feature is
    robust; the most *consistent* (but small) edge is **attaching media**
    (image/chart/video); surface text form (length/caps) is ~chance within
    author, and content moves (stance/question/news) did not survive. Returns
    levers present, a suggestion if media is missing, the features that do NOT
    help (anti-levers), and an honest note. A nudge, never a prediction.
    """
    cf = extract_content_features(text)
    levers_present: list[dict[str, Any]] = []
    suggestions: list[str] = []

    # The most consistent (but small, non-robust) direction: attaching media.
    if has_media:
        levers_present.append({
            "name": "media", "strength": "weak(consistent)",
            "note": ("Has media (image/chart/video) — the most consistent direction "
                     "(72% of over-performers vs 65% of normal; ~74% of authors lean positive), "
                     "but small (lift 1.11) and not robust."),
        })
    else:
        suggestions.append(
            "Attach a visual — chart, screenshot, or short demo clip. It's the most consistent "
            "(if small) edge: present in 72% of over-performers vs 65% of normal, leaning "
            "positive for ~74% of authors (lift ~1.1x). Nothing here is a strong lever."
        )

    # Weak/unproven content tendencies — reported if present, never pushed.
    for key, name, note in _WEAK_CONTENT:
        if cf.get(key, 0.0) >= 1.0:
            levers_present.append({"name": name, "strength": "weak/unproven", "note": note})

    return {
        "levers_present": levers_present,
        "suggestions": suggestions,
        "anti_levers": ["length", "ALL-CAPS", "emoji", "$/%", "hashtags", "stance/question hooks"],
        "anti_levers_note": (
            "No reliable within-author signal — their global correlation is a between-author "
            "artifact (they mark high-follower or topical accounts)."
        ),
        "note": (
            "Reach-controlled view: text predicts over-performance only weakly. Out-of-sample "
            "(leave-one-author-out, 51 authors) AUC ~0.60 within-author / ~0.65 global (the "
            "global is partly between-author). No single feature is robust; attaching media is "
            "the most consistent (but small) edge, and length/caps/stance/questions are ~chance "
            "within author. Reach, timing and luck dominate. A nudge, NOT a prediction."
        ),
        "has_media": bool(has_media),
        "is_quote": bool(is_quote),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _format_overperformance(result: dict[str, Any]) -> str:
    lines = ["Over-performance guidance (beat your OWN baseline) — faint nudges only", ""]
    if result["levers_present"]:
        lines.append("Levers present:")
        for lv in result["levers_present"]:
            lines.append(f"  [{lv['strength']:<11}] {lv['name']:<14} {lv['note']}")
    else:
        lines.append("Levers present: none of the (weak) content levers detected.")
    lines.append("")
    if result["suggestions"]:
        lines.append("Suggestions:")
        for s in result["suggestions"]:
            lines.append(f"  - {s}")
    lines.append("")
    lines.append("Does NOT help (within your own feed): " + ", ".join(result["anti_levers"]))
    lines.append(f"  {result['anti_levers_note']}")
    lines.append("")
    lines.append(f"Note: {result['note']}")
    return "\n".join(lines)


def _format_human(result: dict[str, Any]) -> str:
    lines = [f"Conformance score: {result['score']}/100  ->  {result['verdict'].upper()}", ""]
    lines.append("Factors:")
    for f in result["factors"]:
        tag = f"{f['strength']:<7}"
        if f["name"] == "length":
            v = f["value"]
            state = f"{v['chars']} chars / {v['words']} words (frac {f['strength_frac']})"
        else:
            state = "yes" if f.get("present") else "no"
            if f["name"] == "has_allcaps" and f.get("present"):
                state = f"yes ({f['value']} word(s))"
        lines.append(f"  [{tag}] {f['name']:<13} {state:<34} "
                     f"+{f['contribution']:.1f} / {f['weight']:.0f} pts")
    lines.append("")
    if result["suggestions"]:
        lines.append("Suggestions (data-supported levers you're missing):")
        for s in result["suggestions"]:
            lines.append(f"  - {s}")
    else:
        lines.append("Suggestions: none — the draft already has the levers we'd recommend.")
    lines.append("")
    lines.append(f"Note: {result['disclaimer']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=("Score how much a tweet draft resembles tweets that cleared "
                     "100 likes (a conformance/writing aid, NOT a like predictor)."))
    parser.add_argument("text", help="The draft tweet text to score.")
    parser.add_argument("--media", action="store_true", help="Mark the draft as carrying media.")
    parser.add_argument("--quote", action="store_true", help="Mark the draft as a quote tweet.")
    parser.add_argument("--overperformance", action="store_true",
                        help="Show round-2 over-performance guidance (beat your OWN baseline) "
                             "instead of the raw-likes conformance score.")
    parser.add_argument("--json", action="store_true", help="Emit raw JSON instead of pretty text.")
    args = parser.parse_args(argv)

    if args.overperformance:
        result = assess_overperformance(args.text, has_media=args.media, is_quote=args.quote)
        print(json.dumps(result, indent=2) if args.json else _format_overperformance(result))
    else:
        result = score_tweet(args.text, has_media=args.media, is_quote=args.quote)
        print(json.dumps(result, indent=2) if args.json else _format_human(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
