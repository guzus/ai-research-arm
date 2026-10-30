#!/usr/bin/env python3
"""Voice an Aradio bulletin with Gemini 3.8 Flash TTS (Interactions API).

Contract: docs/aradio.md -> "Audio". Input is the validator's normalized edit
(never the agent's raw file). Each `Speaker N:` line becomes one content part
annotated with `speech_metadata {speaker, style}`; the editor's audio tags are
translated because 3.8 reads its input verbatim:

  [high_energy]           -> turn style "high energy, excited"
  [emphasis]X[/emphasis]  -> tags stripped; style adds "; stress the key figure"
  [dramatic_pause]        -> " <short pause> " (a 3.8 point-in-time vocal event)

Voices: Speaker 1 = Charon (anchor), Speaker 2 = Puck (co-host). Only fields in
the documented REST schema are sent (`speech_config.speakers`; no `mode`).

Failure is LOUD, unlike the daily broadcast's continue-on-error step that
exits 0 on Gemini errors: every failure writes `{ok: false, error, status}` to
--result, prints the HTTP status and the first ~2 KB of the error body to
stderr, and exits non-zero with a distinct code. Audio shorter than 60 % of
the expected duration (spoken words / 188 wpm) is treated as truncated and is
never published. The WAV is written under --work-dir (pass $RUNNER_TEMP:
`.wav` is an LFS-tracked extension in this repo) and deleted after encoding.

Exit codes: 0 ok, 2 config/input, 3 HTTP/network, 4 no or unreadable audio,
5 truncated audio, 6 ffmpeg missing or failed, 1 unexpected.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import ssl
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

import check_aradio as contract

API_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL = "gemini-3.8-flash-tts"
VOICES = (("Speaker 1", "Charon"), ("Speaker 2", "Puck"))
STYLES = {
    "Speaker 1": "confident, informative news anchor",
    "Speaker 2": "energetic, conversational podcast co-host",
}
ENERGETIC_STYLE = "high energy, excited"
EMPHASIS_SUFFIX = "; stress the key figure"
SHORT_PAUSE = " <short pause> "
# Same safety-net symbol normalization as the daily broadcast.
SYMBOLS = (("×", " times "), ("&", " and "), ("—", ", "), ("–", ", "),
           ("‐", "-"), ("‑", "-"), ("•", " "), ("’", "'"),
           ("‘", "'"), ("“", '"'), ("”", '"'))
MIN_DURATION_RATIO = 0.6
HTTP_TIMEOUT_S = 180
RETRY_DELAY_S = 15
MAX_ERROR_BODY = 2048
DEFAULT_PCM_RATE = 24000
FFMPEG_TIMEOUT_S = 300

EXIT_OK = 0
EXIT_UNEXPECTED = 1
EXIT_CONFIG = 2
EXIT_HTTP = 3
EXIT_NO_AUDIO = 4
EXIT_TRUNCATED = 5
EXIT_ENCODE = 6

PostFn = Callable[[str, dict, bytes, float], tuple[int, bytes]]


class TTSFailure(Exception):
    def __init__(self, code: int, message: str, status: int | None = None,
                 body: bytes = b"") -> None:
        super().__init__(message)
        self.code = code
        self.status = status
        self.body = body


def turn_from_line(line: str) -> dict | None:
    speaker, raw = contract.split_script_line(line)
    for symbol, replacement in SYMBOLS:
        raw = raw.replace(symbol, replacement)
    energetic = "[high_energy]" in raw
    emphasis = "[emphasis]" in raw
    text = (raw.replace("[high_energy]", " ").replace("[emphasis]", " ")
            .replace("[/emphasis]", " ").replace("[dramatic_pause]", SHORT_PAUSE))
    text = contract.tidy_spaces(text)
    if not text:
        return None
    style = ENERGETIC_STYLE if energetic else STYLES[speaker]
    if emphasis:
        style += EMPHASIS_SUFFIX
    return {"speaker": speaker, "text": text, "style": style}


def build_request(script: list[str]) -> dict:
    turns = [turn for turn in (turn_from_line(line) for line in script) if turn]
    if not turns:
        raise TTSFailure(EXIT_CONFIG, "script has no speakable lines")
    return {
        "model": MODEL,
        "input": [{
            "type": "user_input",
            "content": [{
                "type": "text",
                "text": turn["text"],
                "annotations": [{
                    "type": "speech_metadata",
                    "speaker": turn["speaker"],
                    "style": turn["style"],
                }],
            } for turn in turns],
        }],
        "response_format": {"type": "audio"},
        "generation_config": {
            "speech_config": {
                "speakers": [{"speaker": speaker, "voice": voice}
                             for speaker, voice in VOICES],
            },
        },
    }


def _ssl_context() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE")
    if cafile and os.path.isfile(cafile):
        return ssl.create_default_context(cafile=cafile)
    for path in ("/etc/ssl/certs/ca-certificates.crt", "/etc/ssl/cert.pem",
                 "/etc/pki/tls/certs/ca-bundle.crt"):
        if os.path.isfile(path):
            return ssl.create_default_context(cafile=path)
    return ssl.create_default_context()


def http_post(url: str, headers: dict, body: bytes, timeout: float) -> tuple[int, bytes]:
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout,
                                    context=_ssl_context()) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        try:
            payload = exc.read() or b""
        except OSError:
            payload = b""
        return exc.code, payload


def call_api(request: dict, api_key: str, post_fn: PostFn,
             sleep_fn: Callable[[float], None]) -> bytes:
    """POST once; retry once on 429, 5xx or a network failure."""
    body = json.dumps(request).encode("utf-8")
    headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}
    status: int | None = None
    payload = b""
    for attempt in (1, 2):
        try:
            status, payload = post_fn(API_URL, headers, body, HTTP_TIMEOUT_S)
        except OSError as exc:  # URLError, timeouts and resets are OSErrors
            if attempt == 1:
                print(f"Gemini TTS network error ({type(exc).__name__}); retrying once",
                      file=sys.stderr)
                sleep_fn(RETRY_DELAY_S)
                continue
            raise TTSFailure(EXIT_HTTP, f"Gemini TTS request failed: "
                                        f"{type(exc).__name__}: {exc}") from exc
        if status == 200:
            return payload
        if attempt == 1 and (status == 429 or 500 <= status <= 599):
            print(f"Gemini TTS returned HTTP {status}; retrying once", file=sys.stderr)
            sleep_fn(RETRY_DELAY_S)
            continue
        break
    raise TTSFailure(EXIT_HTTP, f"Gemini TTS returned HTTP {status}{_api_message(payload)}",
                     status, payload)


def _api_message(payload: bytes) -> str:
    try:
        data = json.loads(payload.decode("utf-8", errors="replace"))
    except ValueError:
        return ""
    error = data.get("error") if isinstance(data, dict) else None
    message = error.get("message") if isinstance(error, dict) else None
    if not isinstance(message, str) or not message.strip():
        return ""
    return ": " + contract.clip(contract.clean_text(message), 200)[0]


def _redacted(payload: bytes) -> bytes:
    """The response with base64 audio removed, for diagnostics."""
    try:
        data = json.loads(payload.decode("utf-8", errors="replace"))
    except ValueError:
        return payload[:MAX_ERROR_BODY]

    def scrub(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: ("<omitted>" if k == "data" else scrub(v)) for k, v in value.items()}
        if isinstance(value, list):
            return [scrub(v) for v in value]
        return value

    return json.dumps(scrub(data))[:MAX_ERROR_BODY].encode("utf-8")


def _pcm_to_wav(pcm: bytes, rate: int) -> bytes:
    header = b"RIFF" + struct.pack("<I", 36 + len(pcm)) + b"WAVE"
    header += b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, rate, rate * 2, 2, 16)
    return header + b"data" + struct.pack("<I", len(pcm)) + pcm


def extract_audio(payload: bytes) -> tuple[bytes, int]:
    """Return (WAV bytes, number of audio blocks) from an Interactions response."""
    try:
        data = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise TTSFailure(EXIT_NO_AUDIO, "Gemini TTS response is not JSON", 200,
                         payload[:MAX_ERROR_BODY]) from exc
    blocks: list[dict] = []
    steps = data.get("steps") if isinstance(data, dict) else None
    for step in steps if isinstance(steps, list) else []:
        if not isinstance(step, dict) or step.get("type") not in (None, "model_output"):
            continue
        for part in step.get("content") or []:
            if (isinstance(part, dict) and part.get("type") in (None, "audio")
                    and isinstance(part.get("data"), str) and part["data"]):
                blocks.append(part)
    if not blocks:
        raise TTSFailure(EXIT_NO_AUDIO, "Gemini TTS response contained no audio data",
                         200, _redacted(payload))
    # The documented SDK convenience (`interaction.output_audio`) is the LAST
    # audio block; a unary TTS response normally carries exactly one.
    chosen = blocks[-1]
    try:
        raw = base64.b64decode(chosen["data"], validate=False)
    except (ValueError, TypeError) as exc:
        raise TTSFailure(EXIT_NO_AUDIO, "audio data is not valid base64", 200,
                         _redacted(payload)) from exc
    if raw[:4] == b"RIFF" and raw[8:12] == b"WAVE":
        return raw, len(blocks)
    mime = str(chosen.get("mime_type") or chosen.get("mimeType") or "").lower()
    if "l16" in mime or "pcm" in mime:
        match = re.search(r"rate=(\d+)", mime)
        return _pcm_to_wav(raw, int(match.group(1)) if match else DEFAULT_PCM_RATE), len(blocks)
    raise TTSFailure(EXIT_NO_AUDIO, f"unrecognized audio payload (mime {mime or 'none'!r})",
                     200, _redacted(payload))


def wav_duration(wav: bytes) -> float:
    """Duration from the fmt chunk and the bytes actually present.

    Streaming writers can declare a 0 or 0xFFFFFFFF data size, so the declared
    length is capped by (and replaced with) the real remainder.
    """
    if wav[:4] != b"RIFF" or wav[8:12] != b"WAVE":
        raise TTSFailure(EXIT_NO_AUDIO, "audio is not a RIFF/WAVE file")
    offset = 12
    channels = sample_width = rate = 0
    while offset + 8 <= len(wav):
        chunk_id = wav[offset:offset + 4]
        size = struct.unpack("<I", wav[offset + 4:offset + 8])[0]
        start = offset + 8
        if chunk_id == b"fmt " and size >= 16:
            _, channels, rate, _, _, bits = struct.unpack("<HHIIHH", wav[start:start + 16])
            sample_width = bits // 8
        elif chunk_id == b"data":
            available = len(wav) - start
            data_len = available if size in (0, 0xFFFFFFFF) else min(size, available)
            if not (channels and sample_width and rate):
                raise TTSFailure(EXIT_NO_AUDIO, "WAV has no usable fmt chunk")
            return data_len / float(channels * sample_width * rate)
        offset = start + size + (size & 1)
    raise TTSFailure(EXIT_NO_AUDIO, "WAV has no data chunk")


def encode_mp3(ffmpeg: str, wav_path: Path, mp3_path: Path) -> None:
    try:
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                        "-i", str(wav_path), "-codec:a", "libmp3lame", "-b:a", "48k",
                        "-ac", "1", str(mp3_path)],
                       check=True, capture_output=True, timeout=FFMPEG_TIMEOUT_S)
    except subprocess.CalledProcessError as exc:
        raise TTSFailure(EXIT_ENCODE, "ffmpeg failed: " + contract.clean_text(
            exc.stderr.decode("utf-8", errors="replace"))[:300]) from exc
    except subprocess.TimeoutExpired as exc:
        raise TTSFailure(EXIT_ENCODE, "ffmpeg timed out") from exc
    if not mp3_path.is_file() or mp3_path.stat().st_size == 0:
        raise TTSFailure(EXIT_ENCODE, "ffmpeg produced no mp3")


def synthesize(edit: dict, *, out: Path, work_dir: Path, api_key: str,
               post_fn: PostFn = http_post,
               sleep_fn: Callable[[float], None] = time.sleep,
               which: Callable[[str], str | None] = shutil.which) -> dict:
    script = edit.get("script") if edit.get("on_air") is True else None
    if not isinstance(script, list) or not script:
        raise TTSFailure(EXIT_CONFIG, "edit is not on air or has no script")
    request = build_request(script)
    words = contract.count_spoken_words(script)
    expected = contract.expected_duration_s(words)
    if not api_key:
        raise TTSFailure(EXIT_CONFIG, "GEMINI_API_KEY is not configured")
    ffmpeg = which("ffmpeg")
    if not ffmpeg:  # checked before spending on the API call
        raise TTSFailure(EXIT_ENCODE, "ffmpeg is not installed on this runner")
    payload = call_api(request, api_key, post_fn, sleep_fn)
    wav, parts = extract_audio(payload)
    duration = wav_duration(wav)
    if duration < MIN_DURATION_RATIO * expected:
        raise TTSFailure(EXIT_TRUNCATED,
                         f"audio is {duration:.1f}s but {words} words need about "
                         f"{expected:.0f}s; treated as truncated", 200)
    work_dir.mkdir(parents=True, exist_ok=True)
    wav_path = work_dir / f"aradio-{os.getpid()}.wav"
    try:
        wav_path.write_bytes(wav)
        out.parent.mkdir(parents=True, exist_ok=True)
        encode_mp3(ffmpeg, wav_path, out)
    finally:
        wav_path.unlink(missing_ok=True)
    return {"ok": True, "mp3": str(out), "bytes": out.stat().st_size,
            "duration_s": round(duration, 1), "expected_s": round(expected, 1),
            "words": words, "error": None, "status": 200, "model": MODEL,
            "audio_parts": parts}


def main(argv: list[str] | None = None, *, post_fn: PostFn = http_post,
         sleep_fn: Callable[[float], None] = time.sleep,
         which: Callable[[str], str | None] = shutil.which) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--edit", type=Path, required=True, help="normalized edit JSON")
    parser.add_argument("--out", type=Path, default=None, help="mp3 path ($RUNNER_TEMP)")
    parser.add_argument("--result", type=Path, default=None, help="result JSON path")
    parser.add_argument("--work-dir", type=Path, default=None,
                        help="where the temporary WAV lives (default: --out's directory)")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the request body and exit without network")
    args = parser.parse_args(argv)

    def finish(result: dict, code: int) -> int:
        if args.result is not None:
            contract.atomic_write_json(args.result, result)
        return code

    try:
        edit = json.loads(args.edit.read_text(encoding="utf-8"))
        if not isinstance(edit, dict):
            raise ValueError("edit must be a JSON object")
    except (OSError, ValueError) as exc:
        print(f"::error::aradio TTS: cannot read the normalized edit: "
              f"{contract.gh_escape(exc)}")
        return finish({"ok": False, "mp3": None, "bytes": 0, "duration_s": None,
                       "error": "normalized edit unreadable", "status": None}, EXIT_CONFIG)

    if args.dry_run:
        try:
            request = build_request(edit.get("script") or [])
        except (TTSFailure, ValueError) as exc:
            print(f"::error::aradio TTS dry run: {contract.gh_escape(exc)}")
            return EXIT_CONFIG
        print(json.dumps(request, indent=2, ensure_ascii=False))
        script = edit.get("script") or []
        words = contract.count_spoken_words(script)
        print(f"dry run: {len(request['input'][0]['content'])} turns, {words} words, "
              f"expected ~{contract.expected_duration_s(words):.0f}s; nothing sent",
              file=sys.stderr)
        return EXIT_OK

    if args.out is None:
        parser.error("--out is required unless --dry-run")
    work_dir = args.work_dir or args.out.parent
    try:
        result = synthesize(edit, out=args.out, work_dir=work_dir,
                            api_key=os.environ.get("GEMINI_API_KEY", "").strip(),
                            post_fn=post_fn, sleep_fn=sleep_fn, which=which)
    except TTSFailure as exc:
        print(f"::error::aradio TTS failed: {contract.gh_escape(exc)}")
        print(f"HTTP status: {exc.status if exc.status is not None else 'n/a'}",
              file=sys.stderr)
        if exc.body:
            print("Error body (first 2 KB):", file=sys.stderr)
            print(exc.body[:MAX_ERROR_BODY].decode("utf-8", errors="replace"),
                  file=sys.stderr)
        return finish({"ok": False, "mp3": None, "bytes": 0, "duration_s": None,
                       "error": contract.clip(contract.clean_text(str(exc)), 300)[0],
                       "status": exc.status}, exc.code)
    except Exception as exc:  # never let an unexpected error look like success
        print(f"::error::aradio TTS crashed: {contract.gh_escape(type(exc).__name__)}: "
              f"{contract.gh_escape(exc)}")
        return finish({"ok": False, "mp3": None, "bytes": 0, "duration_s": None,
                       "error": f"unexpected {type(exc).__name__}", "status": None},
                      EXIT_UNEXPECTED)
    print(f"aradio TTS: {result['bytes']} bytes mp3, {result['duration_s']}s "
          f"(expected ~{result['expected_s']}s for {result['words']} words)")
    return finish(result, EXIT_OK)


if __name__ == "__main__":
    sys.exit(main())
