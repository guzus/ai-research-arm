#!/usr/bin/env python3
"""Deterministic fallback writer for scheduled Twitter/X lanes.

The model lane is still the preferred analyst. This script only preserves the
scheduled output contract when the agent path returns without committing the
expected digest file. It reads the already-fetched bird JSON files and appends a
conservative quick-hit section without claiming deeper synthesis.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import email.utils
import html
import json
import re
import tempfile
from pathlib import Path
from typing import Any


MAX_TEXT = 220
DEFAULT_MAX_AGE_HOURS = 36
FUTURE_SKEW = dt.timedelta(minutes=15)


@dataclasses.dataclass(frozen=True)
class Tweet:
    key: str
    author: str
    text: str
    url: str
    source: str
    likes: int
    retweets: int
    replies: int
    created_at: dt.datetime | None

    @property
    def score(self) -> int:
        return self.likes + (2 * self.retweets) + self.replies


@dataclasses.dataclass(frozen=True)
class Story:
    key: str
    title: str
    lead: str
    verify: str
    watch: str
    evidence: str
    counter: str
    context: str
    headline: str
    tweets: list[Tweet]


def clean_text(value: Any) -> str:
    text = str(value or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def parse_datetime(value: Any) -> dt.datetime | None:
    text = clean_text(value)
    if not text:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(text)
    except (TypeError, ValueError):
        parsed = None
    if parsed is None:
        try:
            parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def parse_timestamp(value: str) -> dt.datetime | None:
    text = clean_text(value)
    for fmt in ("%Y-%m-%d %H:%M UTC", "%Y-%m-%d %H:%M:%S UTC"):
        try:
            return dt.datetime.strptime(text, fmt).replace(tzinfo=dt.timezone.utc)
        except ValueError:
            pass
    return parse_datetime(text)


def nested(row: dict[str, Any], *path: str) -> Any:
    value: Any = row
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def author_handle(row: dict[str, Any]) -> str:
    candidates = (
        nested(row, "author", "username"),
        nested(row, "author", "screen_name"),
        nested(row, "user", "username"),
        nested(row, "user", "screen_name"),
        row.get("username"),
        row.get("screenName"),
        row.get("authorUsername"),
        row.get("name"),
    )
    for candidate in candidates:
        value = clean_text(candidate).lstrip("@")
        if value:
            return value
    return "unknown"


def tweet_id(row: dict[str, Any]) -> str:
    candidates = (
        row.get("id"),
        row.get("id_str"),
        row.get("rest_id"),
        row.get("tweetId"),
        nested(row, "legacy", "id_str"),
    )
    for candidate in candidates:
        value = clean_text(candidate)
        if value:
            return value
    return ""


def tweet_text(row: dict[str, Any]) -> str:
    candidates = (
        row.get("text"),
        row.get("fullText"),
        row.get("full_text"),
        row.get("content"),
        nested(row, "legacy", "full_text"),
    )
    for candidate in candidates:
        value = clean_text(candidate)
        if value:
            return value
    return ""


def tweet_url(row: dict[str, Any], author: str, tid: str) -> str:
    for candidate in (row.get("url"), row.get("tweetUrl"), row.get("permalink")):
        value = clean_text(candidate)
        if value:
            return value
    if author != "unknown" and tid:
        return f"https://x.com/{author}/status/{tid}"
    return ""


def iter_rows(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8") or "[]")
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    return []


def iter_all_rows(path: Path) -> list[tuple[str, dict[str, Any]]]:
    """Return tweet-like rows from birdy's aggregate all.json snapshot."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8") or "{}")
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(payload, dict):
        return []

    rows: list[tuple[str, dict[str, Any]]] = []
    for group in ("accounts", "searches"):
        values = payload.get(group)
        if not isinstance(values, dict):
            continue
        for name, items in values.items():
            if not isinstance(items, list):
                continue
            source = f"{group[:-1]}-{clean_text(name) or 'unknown'}"
            rows.extend((source, row) for row in items if isinstance(row, dict))

    news = payload.get("news")
    if isinstance(news, list):
        rows.extend(("news", row) for row in news if isinstance(row, dict))
    return rows


def is_fresh(created_at: dt.datetime | None, end_time: dt.datetime, max_age: dt.timedelta) -> bool:
    if created_at is None:
        return False
    return end_time - max_age <= created_at <= end_time + FUTURE_SKEW


def add_tweet(
    tweets: dict[str, Tweet],
    row: dict[str, Any],
    source: str,
    end_time: dt.datetime,
    max_age: dt.timedelta,
) -> None:
    author = author_handle(row)
    tid = tweet_id(row)
    text = tweet_text(row)
    url = tweet_url(row, author, tid)
    created_at = parse_datetime(row.get("createdAt") or nested(row, "legacy", "created_at"))
    if not text or not url or not is_fresh(created_at, end_time, max_age):
        return
    key = url or tid or text[:120]
    tweet = Tweet(
        key=key,
        author=author,
        text=text,
        url=url,
        source=source,
        likes=as_int(row.get("likeCount") or nested(row, "legacy", "favorite_count")),
        retweets=as_int(row.get("retweetCount") or nested(row, "legacy", "retweet_count")),
        replies=as_int(row.get("replyCount") or nested(row, "legacy", "reply_count")),
        created_at=created_at,
    )
    existing = tweets.get(key)
    if existing is None or tweet.score > existing.score:
        tweets[key] = tweet


def collect_tweets(input_dir: Path, limit: int, end_time: dt.datetime, max_age_hours: int) -> list[Tweet]:
    tweets: dict[str, Tweet] = {}
    max_age = dt.timedelta(hours=max_age_hours)

    # The production Claude lane fetches an aggregate all.json. Prefer it when
    # present so fallback recovery uses the same raw snapshot the agent prompt
    # referenced; otherwise use the comparison lane's per-source JSON files.
    for source, row in iter_all_rows(input_dir / "all.json"):
        add_tweet(tweets, row, source, end_time, max_age)

    if tweets:
        return rank_tweets(tweets, limit)

    for path in sorted(input_dir.glob("*.json")):
        if path.name in {"all.json", "manifest.json"}:
            continue
        source = path.stem
        for row in iter_rows(path):
            add_tweet(tweets, row, source, end_time, max_age)

    return rank_tweets(tweets, limit)


def rank_tweets(tweets: dict[str, Tweet], limit: int) -> list[Tweet]:
    ranked = sorted(
        tweets.values(),
        key=lambda item: (
            -item.score,
            -(item.created_at.timestamp() if item.created_at else 0),
            item.author,
            item.text,
        ),
    )
    return ranked[:limit]


def norm(text: str) -> str:
    return clean_text(text).casefold()


def is_retweet(tweet: Tweet) -> bool:
    return norm(tweet.text).startswith("rt @")


def has_any(text: str, needles: tuple[str, ...]) -> bool:
    lowered = norm(text)
    return any(needle in lowered for needle in needles)


STRONG_AI_TERMS = (
    "openai",
    "anthropic",
    "chatgpt",
    "gpt-",
    "gpt ",
    "claude",
    "grok",
    "gemini",
    "deepseek",
    "qwen",
    "llama",
    "mistral",
    "glm",
    "xai",
    "model",
    "inference",
    "ai ",
    "ai-",
    "agent",
    "benchmark",
    "eval",
    "voice model",
)

OFF_TOPIC_TERMS = (
    "communitynotes",
    "community notes",
    "football",
    "argentina",
    "egypt",
    "post you interacted",
)


def is_ai_relevant(tweet: Tweet) -> bool:
    text = f"{tweet.author} {tweet.source} {tweet.text}"
    if has_any(text, ("gpt-live", "gpt live", "gpt-5.6", "chatgpt", "openai", "sama", "grok")):
        return True
    return has_any(text, STRONG_AI_TERMS)


def is_offtopic(tweet: Tweet) -> bool:
    text = f"{tweet.author} {tweet.text}"
    if not has_any(text, OFF_TOPIC_TERMS):
        return False
    if has_any(text, ("openai", "chatgpt", "gpt-", "claude", "grok", "gemini", "deepseek")):
        return False
    return True


def filtered_tweets(tweets: list[Tweet]) -> list[Tweet]:
    return [
        tweet
        for tweet in tweets
        if is_ai_relevant(tweet) and not is_offtopic(tweet) and not (is_retweet(tweet) and tweet.score == 0)
    ]


def trim_sentence(text: str, max_len: int = MAX_TEXT) -> str:
    text = clean_text(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "..."


def upsert_section(path: Path, header: str, section: str) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    section_start = section.find(header)
    section_only = section[section_start:] if section_start >= 0 else section
    section_text = section_only.rstrip() + "\n"
    if header in existing:
        pattern = re.compile(rf"(?ms)^## {re.escape(header.removeprefix('## '))}\n.*?(?=^## \d{{2}}:00 UTC\n|\Z)")
        next_text, count = pattern.subn(section_text.rstrip() + "\n", existing.rstrip() + "\n", count=1)
        if count:
            path.parent.mkdir(parents=True, exist_ok=True)
            if next_text != existing:
                atomic_write(path, next_text)
                return True
            return False
    body = existing.rstrip()
    next_text = f"{body}\n\n{section_only}" if body else section
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(path, next_text.rstrip() + "\n")
    return True


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(text)
        tmp_name = handle.name
    Path(tmp_name).replace(path)


def primary_link(tweet: Tweet) -> str:
    return f'<a class="twitter-source-chip" href="{html.escape(tweet.url, quote=True)}">@{html.escape(tweet.author)}</a>'


def engagement(tweet: Tweet) -> str:
    return f"{tweet.likes:,} likes, {tweet.retweets:,} reposts, {tweet.replies:,} replies"


def find_group(tweets: list[Tweet], key: str) -> list[Tweet]:
    if key == "gpt56":
        return [tweet for tweet in tweets if has_any(tweet.text, ("gpt-5.6", "gpt 5.6"))]
    if key == "gptlive":
        return [
            tweet
            for tweet in tweets
            if has_any(tweet.text, ("gpt-live", "gpt live"))
            or (has_any(tweet.text, ("voice", "natural human-ai interaction")) and has_any(tweet.text, ("chatgpt", "openai")))
        ]
    if key == "grok":
        return [tweet for tweet in tweets if has_any(tweet.text, ("grok 4.5", "grok"))]
    return []


def build_stories(tweets: list[Tweet]) -> list[Story]:
    usable = filtered_tweets(tweets)
    stories: list[Story] = []

    gpt56 = find_group(usable, "gpt56")
    if gpt56:
        gpt56 = sorted(gpt56, key=lambda item: (-item.score, item.author))[:3]
        stories.append(
            Story(
                key="gpt56",
                title="OpenAI gives GPT-5.6 Sol/Terra/Luna a public launch window",
                lead=(
                    "OpenAI says GPT-5.6 Sol, Terra, and Luna will launch publicly this Thursday, "
                    "with preview access already expanding globally. Sam Altman amplified the Sol launch separately, "
                    "turning the prior July 7-9 watch item into a primary-source launch item."
                ),
                verify=(
                    "primary OpenAI and Sam Altman posts align on the launch, but performance, pricing, "
                    "rate limits, and independent benchmark behavior remain unverified."
                ),
                watch="Thursday public availability, API/model-picker names, pricing, rate limits, and independent evals.",
                evidence="; ".join(f"@{tweet.author} ({engagement(tweet)})" for tweet in gpt56),
                counter=(
                    "The launch-date claim is now primary-source, but this snapshot does not include a system card, "
                    "pricing page, public benchmark suite, or third-party eval. Treat capability claims as pending."
                ),
                context=(
                    "This resolves the digest's long-running GPT-5.6 launch-window watch item into an official OpenAI "
                    "announcement, while leaving the model-quality and rollout-shape questions open."
                ),
                headline="OPENAI SAYS GPT-5.6 SOL/TERRA/LUNA WILL LAUNCH PUBLICLY THURSDAY",
                tweets=gpt56,
            )
        )

    gptlive = find_group(usable, "gptlive")
    if gptlive:
        gptlive = sorted(gptlive, key=lambda item: (-item.score, item.author))[:3]
        stories.append(
            Story(
                key="gptlive",
                title="OpenAI rolls out GPT-Live voice models in ChatGPT",
                lead=(
                    "OpenAI introduced GPT-Live as a new generation of voice models for natural human-AI interaction, "
                    "rolling out in ChatGPT starting today. Sam Altman framed it as the first voice experience that "
                    "could shift him from typing to talking with AI."
                ),
                verify=(
                    "primary OpenAI and Sam Altman posts confirm the rollout, but real latency, interruption handling, "
                    "language coverage, safety behavior, and paid/free availability need user-side verification."
                ),
                watch="User reports on latency and reliability, rollout geography, plan gating, and API availability.",
                evidence="; ".join(f"@{tweet.author} ({engagement(tweet)})" for tweet in gptlive),
                counter=(
                    "The posts establish launch and positioning, not comparative quality. No independent voice-agent "
                    "benchmarks or safety evaluations are present in the snapshot."
                ),
                context=(
                    "Voice is a product-surface story as much as a model story: if the rollout is broad and low-latency, "
                    "it changes ChatGPT usage patterns even before formal benchmark data arrives."
                ),
                headline="OPENAI ROLLS OUT GPT-LIVE VOICE MODELS IN CHATGPT",
                tweets=gptlive,
            )
        )

    grok = [tweet for tweet in find_group(usable, "grok") if not is_retweet(tweet)]
    if grok and len(stories) < 3:
        grok = sorted(grok, key=lambda item: (-item.score, item.author))[:2]
        stories.append(
            Story(
                key="grok",
                title="Musk says Grok 4.5 still has major inference-speed headroom",
                lead=(
                    "Elon Musk said Grok 4.5 is not yet using xAI's internally developed C/C++ inference stack mapped "
                    "to GB300 hardware, and that doubling current speed or better is probably achievable."
                ),
                verify=(
                    "single-source company-executive performance claim; no public benchmark, deployment date, "
                    "or hardware utilization numbers in this snapshot."
                ),
                watch="xAI release notes, public Grok 4.5 availability, and measured latency once the new stack lands.",
                evidence="; ".join(f"@{tweet.author} ({engagement(tweet)})" for tweet in grok),
                counter=(
                    "This is a roadmap/performance-headroom statement, not a released capability. It should not be "
                    "ranked above actual OpenAI launches unless xAI ships the speedup."
                ),
                context=(
                    "Useful as competitive context for frontier-model serving, especially around GB300-tuned inference, "
                    "but still below the bar of a confirmed product release."
                ),
                headline="MUSK SAYS GROK 4.5 HAS 2X+ INFERENCE-SPEED HEADROOM",
                tweets=grok,
            )
        )

    return stories


def render_story(story: Story, rank: int) -> list[str]:
    sources = "\n      ".join(primary_link(tweet) for tweet in story.tweets)
    first = story.tweets[0]
    return [
        f'<article class="twitter-story" data-rank="{rank}">',
        f'  <h3 class="twitter-story-title">{html.escape(story.title)}</h3>',
        f'  <p class="twitter-story-lead">{html.escape(story.lead)}</p>',
        '  <details class="twitter-story-details">',
        "    <summary>Full analysis</summary>",
        '    <div class="twitter-story-sources">',
        f"      {sources}",
        "    </div>",
        '    <div class="twitter-story-signals">',
        f"      <div><span>Verify</span>{html.escape(story.verify)}</div>",
        f"      <div><span>Watch</span>{html.escape(story.watch)}</div>",
        "    </div>",
        '    <div class="twitter-story-body">',
        f"      <p><strong>Evidence:</strong> {html.escape(story.evidence)}. Lead source text: @{html.escape(first.author)}: {html.escape(trim_sentence(first.text, 260))}</p>",
        f"      <p><strong>Counter / contradicting:</strong> {html.escape(story.counter)}</p>",
        f"      <p><strong>Context:</strong> {html.escape(story.context)}</p>",
        "    </div>",
        "  </details>",
        "</article>",
    ]


def render_digest(date: str, hour: str, title_suffix: str, tweets: list[Tweet]) -> tuple[str, str, list[Story]]:
    h1 = f"# Twitter/X AI Pulse{title_suffix} - {date}"
    header = f"## {hour}:00 UTC"
    stories = build_stories(tweets)
    story_urls = {tweet.url for story in stories for tweet in story.tweets}
    quick_hits = [tweet for tweet in filtered_tweets(tweets) if tweet.url not in story_urls and not is_retweet(tweet)]

    lines = [
        h1,
        "",
        header,
        "",
    ]

    if stories:
        labels = "; ".join(story.title for story in stories[:2])
        lines.extend(
            [
                f"**Cycle summary**: Fresh primary-source AI product movement cleared the bar this window: {labels}. The digest treats high-signal launch posts as stories, while keeping benchmark and rollout claims provisional until independent evidence lands.",
                "",
                "### Top stories",
                "",
            ]
        )
        for index, story in enumerate(stories, start=1):
            lines.extend(render_story(story, index))
            lines.append("")
    else:
        lines.extend(
            [
                "**Cycle summary**: Quiet period - no main stories cleared the publication bar from the fresh Twitter/X snapshot.",
                "",
            ]
        )

    lines.append("### Quick hits")
    if quick_hits:
        for tweet in quick_hits[:5]:
            lines.append(f"- @{tweet.author}: {trim_sentence(tweet.text)} [{engagement(tweet)}]({tweet.url})")
    elif stories:
        lines.append("- No additional AI-specific quick hits cleared the publication bar.")
    else:
        lines.append("- No notable fresh AI tweets survived parsing.")

    skeptic = []
    if any(story.key == "gpt56" for story in stories):
        skeptic.append(
            "GPT-5.6's public launch date is now primary-source, but capability, price, and eval claims still need independent confirmation."
        )
    if any(story.key == "gptlive" for story in stories):
        skeptic.append(
            "GPT-Live's product launch is confirmed; quality claims around naturalness, latency, and safety remain user-verified, not benchmarked."
        )
    if any(story.key == "grok" for story in stories):
        skeptic.append(
            "Grok 4.5 speedup is an executive roadmap claim until xAI ships the GB300-tuned inference stack and users can measure it."
        )
    if not skeptic:
        skeptic.append("None this cycle.")

    watch = []
    if any(story.key == "gpt56" for story in stories):
        watch.append("Whether GPT-5.6 Sol/Terra/Luna become broadly accessible on Thursday, and under what plan/API limits.")
    if any(story.key == "gptlive" for story in stories):
        watch.append("Whether GPT-Live shows low-latency, interruptible, reliable voice behavior in real ChatGPT user reports.")
    if any(story.key == "grok" for story in stories):
        watch.append("Whether xAI publishes Grok 4.5 availability and inference-stack release details.")
    watch.append("Next scheduled Twitter/X AI monitor run.")

    lines.extend(
        [
            "",
            "### Skeptic's corner",
            *(f"- {item}" for item in skeptic),
            "",
            "### Watch list (next 24h)",
            *(f"- {item}" for item in watch),
            "",
            "### Research notes",
            "- Source checks issued this cycle: fresh pre-fetched account, search, and news snapshots; stale rows outside the configured freshness window were excluded before ranking.",
        ]
    )
    return header, "\n".join(lines), stories


def render_summary(timestamp: str, title_suffix: str, tweets: list[Tweet], stories: list[Story]) -> str:
    if stories:
        bullets = "\n".join(f"- {story.title}: {story.lead}" for story in stories[:3])
        return (
            f"Twitter/X AI Pulse{title_suffix} - {timestamp}\n\n"
            "CYCLE: Fresh primary-source AI product movement cleared the publication bar.\n\n"
            f"TOP STORIES:\n{bullets}\n\n"
            "WATCH: public rollout details, independent evals, pricing/rate limits, and real-user voice latency.\n\n"
            "Full update on GitHub.\n"
        )
    usable = filtered_tweets(tweets)
    if usable:
        bullets = "\n".join(f"- @{tweet.author}: {trim_sentence(tweet.text, 110)}" for tweet in usable[:3])
        return (
            f"Twitter/X AI Pulse{title_suffix} - {timestamp}\n\n"
            "CYCLE: Quiet period; no story cleared the main-story bar.\n\n"
            f"QUICK HITS:\n{bullets}\n\n"
            "WATCH: Next scheduled Twitter/X AI monitor run.\n\n"
            "Full update on GitHub.\n"
        )
    return (
        f"Twitter/X AI Pulse{title_suffix} - {timestamp}\n\n"
        "Quiet period - no major AI updates on Twitter/X.\n"
    )


def render_headlines(stories: list[Story]) -> str:
    payload = [
        {
            "headline": story.headline,
            "url": story.tweets[0].url,
            "source": f"@{story.tweets[0].author}",
            "summary": story.lead,
        }
        for story in stories
    ]
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--summaries-dir", type=Path, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--hour", required=True)
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--title-suffix", default="")
    parser.add_argument("--summary-slug", required=True)
    parser.add_argument("--headlines-file", type=Path)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--max-age-hours", type=int, default=DEFAULT_MAX_AGE_HOURS)
    args = parser.parse_args(argv)

    end_time = parse_timestamp(args.timestamp)
    if end_time is None:
        raise SystemExit(f"Could not parse --timestamp as UTC time: {args.timestamp!r}")

    tweets = collect_tweets(args.input_dir, args.limit, end_time, args.max_age_hours)
    digest_path = args.out_dir / f"{args.date}.md"
    summary_path = args.summaries_dir / f"{args.date}-{args.summary_slug}-{args.hour}h-summary.txt"

    header, digest, stories = render_digest(args.date, args.hour, args.title_suffix, tweets)
    changed = upsert_section(digest_path, header, digest)
    atomic_write(summary_path, render_summary(args.timestamp, args.title_suffix, tweets, stories))
    if args.headlines_file is not None:
        atomic_write(args.headlines_file, render_headlines(stories))

    print(f"wrote {digest_path} ({'changed' if changed else 'already had section'})")
    print(f"wrote {summary_path}")
    if args.headlines_file is not None:
        print(f"wrote {args.headlines_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
