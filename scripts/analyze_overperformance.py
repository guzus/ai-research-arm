#!/usr/bin/env python3
"""Does CONTENT beat FORM at predicting over-performance?

Round 1 asked "what separates >=100-like tweets from flops" and found mostly
author/topic artifacts (length was the only semi-stable lever). This asks the
reach-controlled question on `overperformance_tweets.jsonl`: within an author's
own timeline, which tweets beat their median by >=3x — and do *rhetorical*
features (announce / hot-take / personal / prediction / list ...) predict that
better than surface *form* (length / caps / punctuation)?

Because the over-performer label is defined per-author, the pooled comparison is
already largely reach-controlled; we still also report the within-author paired
signal and within-author AUC for rigor.

Outputs (offline):
  research/twitter-viral/overperformance_analysis.md
  research/twitter-viral/overperformance_weights.json
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from tweet_content import BINARY_CONTENT_FEATURES, CONTENT_FEATURE_NAMES, extract_content_features
from tweet_features import BINARY_FEATURES, FEATURE_NAMES, extract_features

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA = REPO_ROOT / "research" / "twitter-viral" / "overperformance_tweets.jsonl"
OUT_MD = REPO_ROOT / "research" / "twitter-viral" / "overperformance_analysis.md"
OUT_WEIGHTS = REPO_ROOT / "research" / "twitter-viral" / "overperformance_weights.json"

MIN_ABS_R = 0.08
MIN_DUAL_AUTHORS = 8
MIN_SIGN_AGREEMENT = 0.60

# Form composite drops word_count (collinear with char_len) to avoid double-count.
FORM_GROUP = [f for f in FEATURE_NAMES if f != "word_count"]
CONTENT_GROUP = list(CONTENT_FEATURE_NAMES)
BINARY_ALL = BINARY_FEATURES | BINARY_CONTENT_FEATURES


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else 0.0


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def pstd(xs):
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def auc(scores, labels):
    """ROC AUC via the rank (Mann-Whitney) statistic, average ranks for ties."""
    n = len(scores)
    order = sorted(range(n), key=lambda i: scores[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0  # 1-based average rank
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    n_pos = sum(1 for l in labels if l == 1)
    n_neg = n - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.5
    sum_pos = sum(ranks[i] for i in range(n) if labels[i] == 1)
    return (sum_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def within_author_auc(rows, score_of):
    """Pair-weighted average of per-author AUCs."""
    groups = defaultdict(list)
    for r in rows:
        groups[r["author_username"]].append(r)
    num = den = 0.0
    for recs in groups.values():
        labels = [r["_y"] for r in recs]
        n_pos = sum(labels)
        n_neg = len(labels) - n_pos
        if n_pos and n_neg:
            a = auc([score_of(r) for r in recs], labels)
            w = n_pos * n_neg
            num += a * w
            den += w
    return num / den if den else 0.5


def load_rows():
    rows = []
    with open(DATA, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            feats = extract_features(r.get("text", ""), has_media=r.get("has_media", False),
                                     is_quote=r.get("is_quote", False))
            feats.update(extract_content_features(r.get("text", "")))
            r["_feats"] = feats
            r["_y"] = 1 if r.get("overperformer") else 0
            rows.append(r)
    return rows


def analyze(rows):
    over = [r for r in rows if r["_y"] == 1]
    norm = [r for r in rows if r["_y"] == 0]
    ys = [r["_y"] for r in rows]

    by_author = defaultdict(lambda: {"over": [], "norm": []})
    for r in rows:
        by_author[r["author_username"]]["over" if r["_y"] else "norm"].append(r)
    dual = {a: g for a, g in by_author.items() if g["over"] and g["norm"]}

    # z-score normalization stats (over full set) for composites.
    stats = {}
    for feat in FORM_GROUP + CONTENT_GROUP:
        xs = [r["_feats"][feat] for r in rows]
        stats[feat] = (mean(xs), pstd(xs) or 1.0)

    features = {}
    for feat in FORM_GROUP + CONTENT_GROUP:
        xs = [r["_feats"][feat] for r in rows]
        r_global = pearson(xs, ys)
        is_bin = feat in BINARY_ALL
        info = {
            "group": "content" if feat in CONTENT_GROUP else "form",
            "r_global": round(r_global, 4),
            "binary": is_bin,
            "auc": round(auc(xs, ys), 4),
            "mean_over": round(mean([r["_feats"][feat] for r in over]), 3),
            "mean_norm": round(mean([r["_feats"][feat] for r in norm]), 3),
        }
        if is_bin:
            ro = mean([r["_feats"][feat] for r in over])
            rn = mean([r["_feats"][feat] for r in norm])
            info["rate_over"], info["rate_norm"] = round(ro, 3), round(rn, 3)
            info["lift"] = round(ro / rn, 2) if rn > 0 else (float("inf") if ro > 0 else 0.0)
        diffs = []
        for g in dual.values():
            diffs.append(mean([r["_feats"][feat] for r in g["over"]])
                         - mean([r["_feats"][feat] for r in g["norm"]]))
        pm = mean(diffs)
        pos = sum(1 for d in diffs if d > 0)
        neg = sum(1 for d in diffs if d < 0)
        agree = (pos if pm >= 0 else neg) / len(diffs) if diffs else 0.0
        info["paired_diff_mean"] = round(pm, 4)
        info["paired_agreement"] = round(agree, 3)
        info["robust"] = (abs(r_global) >= MIN_ABS_R and len(diffs) >= MIN_DUAL_AUTHORS
                          and (r_global >= 0) == (pm >= 0) and agree >= MIN_SIGN_AGREEMENT)
        features[feat] = info

    # Composite scorers: direction-corrected z-sum within each group.
    def composite(group):
        def score_of(r):
            s = 0.0
            for feat in group:
                m, sd = stats[feat]
                sign = 1.0 if features[feat]["r_global"] >= 0 else -1.0
                s += sign * (r["_feats"][feat] - m) / sd
            return s
        return score_of

    form_score = composite(FORM_GROUP)
    content_score = composite(CONTENT_GROUP)
    both_score = composite(FORM_GROUP + CONTENT_GROUP)

    composites = {
        "form": {
            "auc_global": round(auc([form_score(r) for r in rows], ys), 4),
            "auc_within_author": round(within_author_auc(rows, form_score), 4),
        },
        "content": {
            "auc_global": round(auc([content_score(r) for r in rows], ys), 4),
            "auc_within_author": round(within_author_auc(rows, content_score), 4),
        },
        "combined": {
            "auc_global": round(auc([both_score(r) for r in rows], ys), 4),
            "auc_within_author": round(within_author_auc(rows, both_score), 4),
        },
    }

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_total": len(rows), "n_over": len(over), "n_norm": len(norm),
        "n_dual_authors": len(dual),
        "thresholds": {"min_abs_r": MIN_ABS_R, "min_dual_authors": MIN_DUAL_AUTHORS,
                       "min_sign_agreement": MIN_SIGN_AGREEMENT},
        "composites": composites,
        "features": features,
    }


def _fmt(v):
    return f"{v:+.3f}"


def write_md(rep):
    feats = rep["features"]
    ranked = sorted(feats.items(), key=lambda kv: -kv[1]["auc"])
    robust = [(f, i) for f, i in ranked if i["robust"]]
    comp = rep["composites"]

    L = []
    L.append("# Does content beat form? (over-performance analysis)")
    L.append("")
    L.append(f"*Generated {rep['generated_at']} from `overperformance_tweets.jsonl`.*")
    L.append("")
    L.append(f"- **{rep['n_total']}** timeline tweets: **{rep['n_over']}** over-performers "
             f"(>=3x the author's median) / **{rep['n_norm']}** normal, across "
             f"**{rep['n_dual_authors']}** authors with both classes.")
    L.append("- Label is per-author, so the pooled comparison is already largely "
             "reach-controlled. AUC = P(rank an over-performer above a normal tweet).")
    L.append("")
    L.append("## Headline: form vs content vs combined")
    L.append("")
    L.append("| feature group | global AUC | within-author AUC |")
    L.append("|---|--:|--:|")
    for name in ("form", "content", "combined"):
        L.append(f"| {name} | {comp[name]['auc_global']:.3f} | {comp[name]['auc_within_author']:.3f} |")
    L.append("")
    best = max(("form", "content"), key=lambda k: comp[k]["auc_within_author"])
    L.append(f"**Within-author, the {best} composite separates over-performers better.** "
             "Both are weak — over-performance is mostly not explained by these features, "
             "consistent with round 1 (engagement is dominated by reach + luck + timing).")
    L.append("")
    L.append("## Robust features (survived the within-author paired check)")
    L.append("")
    if robust:
        for f, i in robust:
            direction = "more" if i["r_global"] > 0 else "less"
            if i["binary"]:
                detail = (f"{i['rate_over']:.0%} of over-performers vs {i['rate_norm']:.0%} "
                          f"of normal" + (f", {i['lift']:.2f}x" if i['lift'] != float('inf') else ""))
            else:
                detail = f"over avg {i['mean_over']:.1f} vs {i['mean_norm']:.1f}"
            L.append(f"- **`{f}`** ({i['group']}, {direction}) — {detail}; "
                     f"r={_fmt(i['r_global'])}, AUC={i['auc']:.3f}, "
                     f"paired agree {i['paired_agreement']:.0%}.")
    else:
        L.append("*None cleared the bar — no feature reliably predicts over-performance "
                 "within author. The honest answer: it's mostly not in the text.*")
    L.append("")
    L.append("## Full ranking by single-feature AUC")
    L.append("")
    L.append("| feature | group | AUC | r | over | normal | lift | paired Δ | agree | robust |")
    L.append("|---|:--|--:|--:|--:|--:|--:|--:|--:|:--:|")
    for f, i in ranked:
        if i["binary"]:
            o = f"{i['rate_over']:.0%}"; n = f"{i['rate_norm']:.0%}"
            lift = "∞" if i["lift"] == float("inf") else f"{i['lift']:.1f}x"
        else:
            o = f"{i['mean_over']:.1f}"; n = f"{i['mean_norm']:.1f}"; lift = "—"
        L.append(f"| `{f}` | {i['group']} | {i['auc']:.3f} | {_fmt(i['r_global'])} | {o} | {n} "
                 f"| {lift} | {_fmt(i['paired_diff_mean'])} | {i['paired_agreement']:.0%} "
                 f"| {'✅' if i['robust'] else ''} |")
    L.append("")
    L.append("## Caveats")
    L.append("")
    L.append(f"1. **Small N.** {rep['n_over']} over-performers across {rep['n_dual_authors']} "
             "authors; rare rhetorical features are noisy. Treat as directional.")
    L.append("2. **Heuristic content detectors.** Keyword/structure based — they under-detect "
             "(see `overperformance_qualitative.md` for what they miss).")
    L.append("3. **Population is not pure AI.** Authors span markets/crypto/astrology/news; "
             "conclusions are about *this mix*, not AI Twitter specifically.")
    L.append("4. **Over-performance ≠ likes.** A small account's over-performer may have few "
             "absolute likes. This measures relative pop, which is the writer-actionable part.")
    L.append("5. **Composite AUCs are in-sample.** Each composite takes its feature signs from "
             "the global r on the *same* rows it scores, so the content/combined numbers are "
             "optimistic. On a held-out 50/50 split the content composite within-author is "
             "~0.53 (not ~0.60); form stays sub-chance (~0.41). The direction (content > form) "
             "survives ~18/20 splits, but the *gap* is widest exactly at the 3x cutoff.")
    L.append("6. **No single feature is a reliable lever.** Even `is_stance` (best by pooled "
             "lift, ~1.9x) is ~chance within author (AUC ~0.51). Read this analysis for the "
             "**negative** result — the text barely predicts over-performance — not for a lever.")
    OUT_MD.write_text("\n".join(L), encoding="utf-8")


def main():
    rows = load_rows()
    rep = analyze(rows)
    OUT_WEIGHTS.write_text(json.dumps(rep, indent=2), encoding="utf-8")
    write_md(rep)
    c = rep["composites"]
    print(f"{rep['n_total']} tweets ({rep['n_over']} over / {rep['n_norm']} normal), "
          f"{rep['n_dual_authors']} dual authors")
    print(f"within-author AUC  form={c['form']['auc_within_author']}  "
          f"content={c['content']['auc_within_author']}  combined={c['combined']['auc_within_author']}")
    robust = [f for f, i in rep["features"].items() if i["robust"]]
    print(f"robust features ({len(robust)}): {', '.join(robust) or '(none)'}")
    print(f"wrote {OUT_MD.relative_to(REPO_ROOT)} and {OUT_WEIGHTS.name}")


if __name__ == "__main__":
    main()
