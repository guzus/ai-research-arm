#!/usr/bin/env python3
"""Measure which tweet *form* features separate high-engagement (>=100 likes)
from low-engagement tweets, using two complementary views:

1. **Global** point-biserial correlation r between each feature and the
   high/low label across all tweets. Simple, but confounded by author and
   topic (popular accounts clear 100 likes on almost anything).

2. **Within-author paired** difference: for authors who have BOTH high and low
   tweets in the window, compute (mean_high - mean_low) per feature per author,
   then average. This holds follower count ~constant, so it isolates the
   content effect. A feature we trust ("robust") points the SAME direction in
   both views.

Outputs (offline, no network):
  research/twitter-viral/analysis.md           human-readable report
  research/twitter-viral/feature_weights.json  machine-readable, consumed by the verifier
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from tweet_features import BINARY_FEATURES, FEATURE_NAMES, extract_features

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA = REPO_ROOT / "research" / "twitter-viral" / "viral_tweets.jsonl"
OUT_MD = REPO_ROOT / "research" / "twitter-viral" / "analysis.md"
OUT_WEIGHTS = REPO_ROOT / "research" / "twitter-viral" / "feature_weights.json"

# A feature is "robust" (verifier-worthy) if the global signal is non-trivial
# AND it survives the follower-controlled within-author check.
MIN_ABS_R = 0.10            # global point-biserial threshold
MIN_DUAL_AUTHORS = 8        # need enough authors for the paired view to matter
MIN_SIGN_AGREEMENT = 0.60   # fraction of dual authors agreeing with the sign


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 3:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0 or syy <= 0:
        return 0.0
    return sxy / math.sqrt(sxx * syy)


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def load_rows() -> list[dict]:
    rows = []
    with open(DATA, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            r["_feats"] = extract_features(
                r.get("text", ""), has_media=r.get("has_media", False), is_quote=r.get("is_quote", False)
            )
            r["_y"] = 1.0 if r.get("label") == "high" else 0.0
            rows.append(r)
    return rows


def analyze(rows: list[dict]) -> dict:
    highs = [r for r in rows if r["_y"] == 1.0]
    lows = [r for r in rows if r["_y"] == 0.0]
    ys = [r["_y"] for r in rows]

    # Authors with both classes -> within-author paired view.
    by_author: dict[str, dict[str, list[dict]]] = defaultdict(lambda: {"high": [], "low": []})
    for r in rows:
        by_author[r.get("author_username") or "?"][r["label"]].append(r)
    dual = {a: g for a, g in by_author.items() if g["high"] and g["low"]}

    features = {}
    for feat in FEATURE_NAMES:
        xs = [r["_feats"][feat] for r in rows]
        r_global = pearson(xs, ys)

        is_binary = feat in BINARY_FEATURES
        info = {
            "r_global": round(r_global, 4),
            "binary": is_binary,
            "mean_high": round(mean([r["_feats"][feat] for r in highs]), 3),
            "mean_low": round(mean([r["_feats"][feat] for r in lows]), 3),
        }
        if is_binary:
            rate_high = mean([r["_feats"][feat] for r in highs])
            rate_low = mean([r["_feats"][feat] for r in lows])
            info["rate_high"] = round(rate_high, 3)
            info["rate_low"] = round(rate_low, 3)
            info["lift"] = round(rate_high / rate_low, 2) if rate_low > 0 else (float("inf") if rate_high > 0 else 0.0)

        # Within-author paired difference.
        diffs = []
        for g in dual.values():
            dh = mean([r["_feats"][feat] for r in g["high"]])
            dl = mean([r["_feats"][feat] for r in g["low"]])
            diffs.append(dh - dl)
        paired_mean = mean(diffs)
        pos = sum(1 for d in diffs if d > 0)
        neg = sum(1 for d in diffs if d < 0)
        agree = (pos if paired_mean >= 0 else neg) / len(diffs) if diffs else 0.0
        info["paired_diff_mean"] = round(paired_mean, 4)
        info["paired_pos_authors"] = pos
        info["paired_neg_authors"] = neg
        info["paired_sign_agreement"] = round(agree, 3)

        # Robust if the global signal is real AND survives the controlled view.
        robust = (
            abs(r_global) >= MIN_ABS_R
            and len(diffs) >= MIN_DUAL_AUTHORS
            and (r_global >= 0) == (paired_mean >= 0)
            and agree >= MIN_SIGN_AGREEMENT
        )
        info["robust"] = robust
        features[feat] = info

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_total": len(rows),
        "n_high": len(highs),
        "n_low": len(lows),
        "n_dual_authors": len(dual),
        "dual_authors": sorted(dual.keys()),
        "thresholds": {
            "min_abs_r": MIN_ABS_R,
            "min_dual_authors": MIN_DUAL_AUTHORS,
            "min_sign_agreement": MIN_SIGN_AGREEMENT,
        },
        "features": features,
    }


def _fmt_r(v: float) -> str:
    return f"{v:+.3f}"


def write_markdown(report: dict) -> None:
    feats = report["features"]
    ranked = sorted(feats.items(), key=lambda kv: -abs(kv[1]["r_global"]))
    robust_pos = [(f, i) for f, i in ranked if i["robust"] and i["r_global"] > 0]
    robust_neg = [(f, i) for f, i in ranked if i["robust"] and i["r_global"] < 0]

    lines: list[str] = []
    lines.append("# What separates a >=100-like tweet from a flop")
    lines.append("")
    lines.append(f"*Generated {report['generated_at']} from "
                 f"`research/twitter-viral/viral_tweets.jsonl`.*")
    lines.append("")
    lines.append(f"- **{report['n_total']}** tweets analyzed: "
                 f"**{report['n_high']}** high (>=100 likes) / **{report['n_low']}** low.")
    lines.append(f"- **{report['n_dual_authors']}** authors appear with BOTH high and low "
                 "tweets — these drive the follower-controlled (paired) view.")
    lines.append("")
    lines.append("## How to read this")
    lines.append("")
    lines.append("- **r (global)** — point-biserial correlation between the feature and the "
                 "high/low label across all tweets. Sign = direction, magnitude = strength. "
                 "Confounded by who the author is.")
    lines.append("- **paired Δ** — average of (mean among the author's high tweets − mean "
                 "among their low tweets), over authors who have both. Holds follower count "
                 "~constant, so it isolates the *content* effect.")
    lines.append("- **robust** — the signal is non-trivial (|r| ≥ "
                 f"{report['thresholds']['min_abs_r']}) AND points the same way in both views "
                 "across enough authors. Only robust features feed the verifier.")
    lines.append("")

    # Secret ingredients.
    lines.append("## The secret ingredients (robust, follower-controlled)")
    lines.append("")
    if robust_pos:
        lines.append("**Do more of this** (raises odds of clearing 100 likes):")
        lines.append("")
        for f, i in robust_pos:
            lines.append(f"- `{f}` — {_explain(f, i, positive=True)}")
        lines.append("")
    if robust_neg:
        lines.append("**Do less of this** (drags engagement down):")
        lines.append("")
        for f, i in robust_neg:
            lines.append(f"- `{f}` — {_explain(f, i, positive=False)}")
        lines.append("")
    if not robust_pos and not robust_neg:
        lines.append("*No features cleared the robustness bar — treat all signals as weak.*")
        lines.append("")

    # Full ranked table.
    lines.append("## Full feature ranking")
    lines.append("")
    lines.append("| feature | r (global) | high | low | lift | paired Δ | agree | robust |")
    lines.append("|---|--:|--:|--:|--:|--:|--:|:--:|")
    for f, i in ranked:
        if i["binary"]:
            hi = f"{i['rate_high']:.0%}"
            lo = f"{i['rate_low']:.0%}"
            lift = "∞" if i["lift"] == float("inf") else f"{i['lift']:.2f}×"
        else:
            hi = f"{i['mean_high']:.1f}"
            lo = f"{i['mean_low']:.1f}"
            lift = "—"
        agree = f"{i['paired_sign_agreement']:.0%}"
        rob = "✅" if i["robust"] else ""
        lines.append(f"| `{f}` | {_fmt_r(i['r_global'])} | {hi} | {lo} | {lift} "
                     f"| {_fmt_r(i['paired_diff_mean'])} | {agree} | {rob} |")
    lines.append("")

    # Caveats — be honest about what this is and isn't.
    lines.append("## Caveats (read before trusting this)")
    lines.append("")
    lines.append("1. **Correlation, not causation.** These features co-occur with engagement; "
                 "they don't guarantee it. A verifier built on them is a *conformance scorer* "
                 "— \"does this draft resemble what works\" — not a like-count oracle.")
    lines.append("2. **Follower count is the elephant.** The paired view controls for it, but "
                 "only across the "
                 f"{report['n_dual_authors']} authors who had both high and low tweets. "
                 "Global r is still author-confounded.")
    lines.append("3. **Topic noise in the positive set.** The search query `Gemini`/`Claude` "
                 "also matches zodiac/astrology and people's names, so the corpus spans AI, "
                 "crypto, markets, astrology and politics. That actually makes the *form* "
                 "findings more topic-agnostic, but it is not a pure AI sample.")
    lines.append("4. **Top-search selection bias.** Positives come from X's \"Top\" ranking, "
                 "which already favors popular tweets.")
    lines.append("5. **`has_url` ↔ `has_media` overlap.** A media tweet carries a t.co link in "
                 "its text, so these two features are partly entangled.")
    lines.append("6. **Small low-N.** Only "
                 f"{report['n_low']} low tweets; per-feature rates for rare features are noisy.")
    lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def _explain(feat: str, info: dict, *, positive: bool) -> str:
    if info["binary"]:
        rh, rl = info["rate_high"], info["rate_low"]
        lift = info["lift"]
        lifts = "∞" if lift == float("inf") else f"{lift:.2f}×"
        return (f"present in {rh:.0%} of high vs {rl:.0%} of low tweets "
                f"({lifts} as common in winners), r={_fmt_r(info['r_global'])}.")
    direction = "higher" if positive else "lower"
    return (f"winners average {info['mean_high']:.1f} vs {info['mean_low']:.1f} "
            f"({direction}), r={_fmt_r(info['r_global'])}.")


def main() -> None:
    rows = load_rows()
    report = analyze(rows)
    OUT_WEIGHTS.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_markdown(report)
    robust = [f for f, i in report["features"].items() if i["robust"]]
    print(f"analyzed {report['n_total']} tweets "
          f"({report['n_high']} high / {report['n_low']} low, "
          f"{report['n_dual_authors']} dual authors)")
    print(f"robust features ({len(robust)}): {', '.join(robust) or '(none)'}")
    print(f"wrote {OUT_MD.relative_to(REPO_ROOT)} and {OUT_WEIGHTS.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
