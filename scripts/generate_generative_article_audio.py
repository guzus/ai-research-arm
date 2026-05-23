#!/usr/bin/env python3
"""Generate Gemini TTS audio for a generative research article.

Default model choice is intentionally cost-aware: Gemini 2.5 Flash Preview
TTS is the price-performant TTS model. Use --model to spend more when a
specific higher-priced model is worth it for a given article.
"""

from __future__ import annotations

import argparse
import base64
import html
import html.parser
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import ssl
from pathlib import Path
from typing import Any


DEFAULT_DEVELOPER_MODEL = "gemini-2.5-flash-preview-tts"
DEFAULT_VERTEX_MODEL = "gemini-2.5-flash-tts"
DEFAULT_VOICE = "Charon"
DEFAULT_BITRATE = "64k"
PCM_RATE = 24000
PCM_CHANNELS = 1

SKIP_TAGS = {"script", "style", "svg", "table", "thead", "tbody", "tr", "th", "td"}
BLOCK_TAGS = {
    "article",
    "header",
    "section",
    "h1",
    "h2",
    "h3",
    "h4",
    "p",
    "li",
    "dt",
    "dd",
    "blockquote",
    "figcaption",
}


class ArticleTextExtractor(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0
        self.ref_depth = 0
        self.current_tag: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_dict = {k.lower(): (v or "") for k, v in attrs}
        classes = set(attrs_dict.get("class", "").split())
        element_id = attrs_dict.get("id", "")
        if tag in SKIP_TAGS:
            self.skip_depth += 1
        if (
            "ara-refs" in classes
            or element_id.startswith("ref-")
            or attrs_dict.get("role") == "doc-bibliography"
        ):
            self.ref_depth += 1
        if self.skip_depth or self.ref_depth:
            return
        if tag in BLOCK_TAGS:
            self.current_tag = tag
            self._break()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.ref_depth:
            self.ref_depth -= 1
            return
        if tag in BLOCK_TAGS:
            self._break()
            self.current_tag = None

    def handle_data(self, data: str) -> None:
        if self.skip_depth or self.ref_depth:
            return
        text = normalize_text(data)
        if not text:
            return
        if self.current_tag in {"h1", "h2", "h3", "h4"}:
            text = text.rstrip(".") + "."
        self.parts.append(text)

    def _break(self) -> None:
        if self.parts and self.parts[-1] != "\n":
            self.parts.append("\n")

    def text(self) -> str:
        raw = " ".join(self.parts)
        raw = re.sub(r" *\n *", "\n", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        raw = re.sub(r"[ \t]{2,}", " ", raw)
        return raw.strip()


def normalize_text(text: str) -> str:
    text = html.unescape(text)
    replacements = {
        "×": " times ",
        "&": " and ",
        "—": ", ",
        "–": ", ",
        "‐": "-",
        "‑": "-",
        "•": " ",
        "$": " dollars ",
        "%": " percent ",
        "≈": " approximately ",
        "~": " approximately ",
        "→": " to ",
        "≥": " at least ",
        "≤": " at most ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\bAI\b", "A I", text)
    text = re.sub(r"\bNYSE\b", "N Y S E", text)
    text = re.sub(r"\bSaaS\b", "sass", text)
    text = re.sub(r"\bYoY\b", "year over year", text)
    text = re.sub(r"\bFCF\b", "free cash flow", text)
    text = re.sub(r"\bCRPO\b", "current remaining performance obligation", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_index(root: Path) -> list[dict[str, Any]]:
    path = root / "research" / "generative" / "index.json"
    return json.loads(path.read_text(encoding="utf-8"))


def select_row(rows: list[dict[str, Any]], slug: str | None) -> dict[str, Any]:
    if slug:
        for row in rows:
            if row.get("slug") == slug:
                return row
        raise SystemExit(f"unknown generative article slug: {slug}")
    if not rows:
        raise SystemExit("research/generative/index.json is empty")
    return max(rows, key=lambda r: r.get("created_at", ""))


def chunk_text(text: str, max_chars: int) -> list[str]:
    blocks = [b.strip() for b in re.split(r"\n{2,}", text) if b.strip()]
    chunks: list[str] = []
    current = ""
    for block in blocks:
        if len(block) > max_chars:
            sentences = re.split(r"(?<=[.!?])\s+", block)
            for sentence in sentences:
                current = append_chunk(chunks, current, sentence, max_chars)
            continue
        current = append_chunk(chunks, current, block, max_chars)
    if current.strip():
        chunks.append(current.strip())
    return chunks


def append_chunk(chunks: list[str], current: str, block: str, max_chars: int) -> str:
    block = block.strip()
    if not block:
        return current
    candidate = f"{current}\n\n{block}".strip() if current else block
    if len(candidate) <= max_chars:
        return candidate
    if current.strip():
        chunks.append(current.strip())
    return block


def build_prompt(chunk: str, part: int, total: int, title: str) -> str:
    return (
        "Read this ARA research article excerpt as a polished financial research "
        "audiobook. Use a calm, precise, newsroom tone with natural pacing. "
        "Do not add commentary, summaries, introductions, or citations beyond the "
        "text below. Pronounce ticker symbols and acronyms clearly.\n\n"
        f"Article: {title}\n"
        f"Part {part} of {total}.\n\n"
        f"{chunk}"
    )


def call_gemini_developer_tts(api_key: str, model: str, voice: str, text: str) -> bytes:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice,
                    }
                }
            },
        },
        "model": model,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180, context=ssl_context()) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini TTS HTTP {e.code}: {detail[:1200]}") from e
    data = (
        payload.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("inlineData", {})
        .get("data", "")
    )
    if not data:
        redacted = json.dumps(payload)
        raise RuntimeError(f"Gemini TTS returned no audio data: {redacted[:1200]}")
    return base64.b64decode(data)


def gcloud_access_token() -> str:
    result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    token = result.stdout.strip()
    if not token:
        raise RuntimeError("gcloud returned an empty access token")
    return token


def ssl_context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def call_vertex_tts(project: str, location: str, model: str, voice: str, text: str) -> bytes:
    host = "aiplatform.googleapis.com" if location == "global" else f"{location}-aiplatform.googleapis.com"
    url = (
        f"https://{host}/v1beta1/projects/{project}/locations/{location}"
        f"/publishers/google/models/{model}:generateContent"
    )
    body = {
        "contents": {
            "role": "user",
            "parts": {
                "text": text,
            },
        },
        "generation_config": {
            "speech_config": {
                "language_code": "en-us",
                "voice_config": {
                    "prebuilt_voice_config": {
                        "voice_name": voice.lower(),
                    }
                },
            },
            "temperature": 1.0,
        },
    }
    token = gcloud_access_token()
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "x-goog-user-project": project,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180, context=ssl_context()) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Vertex Gemini TTS HTTP {e.code}: {detail[:1200]}") from e
    data = (
        payload.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("inlineData", {})
        .get("data", "")
    )
    if not data:
        redacted = json.dumps(payload)
        raise RuntimeError(f"Vertex Gemini TTS returned no audio data: {redacted[:1200]}")
    return base64.b64decode(data)


def encode_mp3(pcm_path: Path, mp3_path: Path, bitrate: str) -> None:
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "s16le",
        "-ar",
        str(PCM_RATE),
        "-ac",
        str(PCM_CHANNELS),
        "-i",
        str(pcm_path),
        "-codec:a",
        "libmp3lame",
        "-b:a",
        bitrate,
        "-ac",
        str(PCM_CHANNELS),
        str(mp3_path),
    ]
    subprocess.run(cmd, check=True)


def update_index(root: Path, slug: str, audio_rel: str) -> None:
    path = root / "research" / "generative" / "index.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    for row in rows:
        if row.get("slug") == slug:
            row["audio_file"] = audio_rel
            break
    else:
        raise SystemExit(f"cannot update audio_file, slug not found: {slug}")
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def estimate_cost(text_chars: int, duration_seconds: float, model: str) -> str:
    # Rough planning estimate. Text tokens are approximated as chars / 4.
    # Gemini pricing docs state audio tokens correspond to 25 tokens/sec.
    text_tokens = text_chars / 4
    audio_tokens = duration_seconds * 25
    if model == "gemini-2.5-flash-preview-tts":
        cost = (text_tokens / 1_000_000 * 0.50) + (audio_tokens / 1_000_000 * 10.00)
    elif model in {"gemini-2.5-pro-preview-tts", "gemini-3.1-flash-tts-preview"}:
        cost = (text_tokens / 1_000_000 * 1.00) + (audio_tokens / 1_000_000 * 20.00)
    else:
        return "unknown"
    return f"${cost:.2f}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", help="Article slug. Defaults to the latest article.")
    parser.add_argument(
        "--api",
        choices=("developer", "vertex"),
        default=os.getenv("GEMINI_TTS_API", "developer"),
        help="developer uses GEMINI_API_KEY; vertex uses gcloud ADC.",
    )
    parser.add_argument("--model", default=os.getenv("GEMINI_TTS_MODEL"))
    parser.add_argument("--vertex-project", default=os.getenv("GOOGLE_CLOUD_PROJECT"))
    parser.add_argument("--vertex-location", default=os.getenv("GOOGLE_CLOUD_REGION", "global"))
    parser.add_argument("--voice", default=os.getenv("GEMINI_TTS_VOICE", DEFAULT_VOICE))
    parser.add_argument("--bitrate", default=os.getenv("ARTICLE_AUDIO_BITRATE", DEFAULT_BITRATE))
    parser.add_argument("--chunk-chars", type=int, default=4200)
    parser.add_argument("--force", action="store_true", help="Overwrite an existing MP3.")
    parser.add_argument("--dry-run", action="store_true", help="Extract text and estimate cost only.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.model:
        args.model = DEFAULT_VERTEX_MODEL if args.api == "vertex" else DEFAULT_DEVELOPER_MODEL
    root = repo_root()
    rows = load_index(root)
    row = select_row(rows, args.slug)
    title = row["title"]
    slug = row["slug"]
    article_path = root / "research" / "generative" / row["file"]
    if not article_path.exists():
        raise SystemExit(f"article file not found: {article_path}")

    extractor = ArticleTextExtractor()
    extractor.feed(article_path.read_text(encoding="utf-8"))
    text = extractor.text()
    if len(text) < 500:
        raise SystemExit(f"extracted article text is suspiciously short: {len(text)} chars")
    chunks = chunk_text(text, args.chunk_chars)
    stem = Path(row["file"]).with_suffix("").name
    audio_dir = root / "research" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    mp3_path = audio_dir / f"{stem}.mp3"
    audio_rel = f"audio/{mp3_path.name}"

    # Reading speed estimate: 145 words/min for dense finance research.
    words = len(re.findall(r"\b\w+\b", text))
    duration_seconds = words / 145 * 60
    print(f"Article: {title}", file=sys.stderr)
    print(f"Slug: {slug}", file=sys.stderr)
    print(f"Text: {len(text)} chars, {words} words, {len(chunks)} chunks", file=sys.stderr)
    print(f"API: {args.api}", file=sys.stderr)
    print(f"Model: {args.model}, voice: {args.voice}, bitrate: {args.bitrate}", file=sys.stderr)
    print(f"Estimated duration: {duration_seconds / 60:.1f} min", file=sys.stderr)
    print(f"Estimated Gemini cost: {estimate_cost(len(text), duration_seconds, args.model)}", file=sys.stderr)

    if args.dry_run:
        return 0
    if mp3_path.exists() and not args.force:
        raise SystemExit(f"{mp3_path} already exists; pass --force to overwrite")
    api_key = os.getenv("GEMINI_API_KEY")
    if args.api == "developer" and not api_key:
        raise SystemExit("GEMINI_API_KEY is required")
    if args.api == "vertex" and not args.vertex_project:
        raise SystemExit("--vertex-project or GOOGLE_CLOUD_PROJECT is required")

    with tempfile.TemporaryDirectory(prefix="ara-gemini-tts-") as tmp:
        pcm_path = Path(tmp) / f"{stem}.pcm"
        with pcm_path.open("wb") as out:
            for i, chunk in enumerate(chunks, start=1):
                print(f"Generating chunk {i}/{len(chunks)} ({len(chunk)} chars)...", file=sys.stderr)
                prompt = build_prompt(chunk, i, len(chunks), title)
                if args.api == "vertex":
                    pcm = call_vertex_tts(
                        args.vertex_project,
                        args.vertex_location,
                        args.model,
                        args.voice,
                        prompt,
                    )
                else:
                    pcm = call_gemini_developer_tts(api_key or "", args.model, args.voice, prompt)
                out.write(pcm)
                # Gentle pacing for preview-model rate limits.
                if i < len(chunks):
                    time.sleep(0.5)
        encode_mp3(pcm_path, mp3_path, args.bitrate)

    if not mp3_path.exists() or mp3_path.stat().st_size == 0:
        raise SystemExit("ffmpeg produced no MP3")
    update_index(root, slug, audio_rel)
    print(f"Generated {mp3_path} ({mp3_path.stat().st_size} bytes)", file=sys.stderr)
    print(f"Updated research/generative/index.json audio_file={audio_rel}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
