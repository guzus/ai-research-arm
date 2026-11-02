#!/usr/bin/env python3
"""Voice an Aradio bulletin with Gemini 3.8 Flash TTS (Interactions API).

Contract: docs/aradio.md -> "Audio". Input is the validator's normalized edit
(never the agent's raw file). Each `Speaker N:` line becomes one content part
annotated with `speech_metadata {speaker, style}`; the editor's audio tags are
translated because 3.8 reads its input verbatim:

  [high_energy]           -> turn style "high energy, excited"
  [emphasis]X[/emphasis]  -> tags stripped; style adds "; stress the key figure"
  [dramatic_pause]        -> " <short pause> " (a 3.8 point-in-time vocal event)
  [transition] / [gong]   -> starts a new SEGMENT (see "Sound design" below)

Sound design (scripts/aradio_sound.py): the script is cut into segments at
each line the validator kept a leading cue on, each segment is voiced by its
own request (same voices and styles), and the segments are mixed between the
signature intro, the cue sounds (transition stinger or gong) and the outro.
The result records the exact span of each segment in the final audio
(`segments`), which the dashboard uses to follow the transcript. Sound is
fail-soft for a single segment (a voice it cannot mix airs dry, with
`sound_error`) and `--no-sound` airs the voice dry on purpose; with several
segments the voice cannot be joined without the mixer, so that fails loudly.

Voices: Speaker 1 = Charon (anchor), Speaker 2 = Puck (co-host). Only fields in
the documented REST schema are sent (`speech_config.speakers`; no `mode`).

Failure is LOUD, unlike the daily broadcast's continue-on-error step that
exited 0 on Gemini errors: every failure writes `{ok: false, error, status}` to
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

import aradio_sound as sound
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
# A short segment's pace varies more, so each one gets a little slack on top
# of the ratio; the whole voice is still held to the plain ratio.
SEGMENT_SLACK_S = 2.0
HTTP_TIMEOUT_S = 180
# The segmented path stops starting requests after this long and falls back to
# one dry request, and a segment (<= ~1/2 of the script) gets a shorter HTTP
# timeout. Worst case: 240 s budget + one in-flight segment (2 x 120 s + 15 s
# retry) + the dry fallback (2 x 180 s + 15 s) ~= 14.5 min, inside the job's
# 30 min after a 12 min editor.
SEGMENTED_BUDGET_S = 240
SEGMENT_HTTP_TIMEOUT_S = 120
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
    for tag in contract.CUE_TAGS:
        raw = raw.replace(tag, " ")
    text = (raw.replace("[high_energy]", " ").replace("[emphasis]", " ")
            .replace("[/emphasis]", " ").replace("[dramatic_pause]", SHORT_PAUSE))
    text = contract.tidy_spaces(text)
    if not text:
        return None
    style = ENERGETIC_STYLE if energetic else STYLES[speaker]
    if emphasis:
        style += EMPHASIS_SUFFIX
    return {"speaker": speaker, "text": text, "style": style}


def line_cue(line: str) -> str | None:
    """"transition" or "gong" when the line opens with that sound cue."""
    _, raw = contract.split_script_line(line)
    return next((tag.strip("[]") for tag in contract.CUE_TAGS
                 if raw.lstrip().startswith(tag)), None)


def split_segments(script: list[str]) -> list[list[int]]:
    """Line indexes per segment: a new one starts at each cue line."""
    segments: list[list[int]] = []
    for index, line in enumerate(script):
        if not segments or line_cue(line):
            segments.append([])
        segments[-1].append(index)
    return segments


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
             sleep_fn: Callable[[float], None], timeout: float = HTTP_TIMEOUT_S) -> bytes:
    """POST once; retry once on 429, 5xx or a network failure."""
    body = json.dumps(request).encode("utf-8")
    headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}
    status: int | None = None
    payload = b""
    for attempt in (1, 2):
        try:
            status, payload = post_fn(API_URL, headers, body, timeout)
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


def _voice(script: list[str], segments: list[list[int]], api_key: str, post_fn: PostFn,
           sleep_fn: Callable[[float], None], clock: Callable[[], float]
           ) -> tuple[list[bytes], int]:
    """One WAV per segment; every segment is checked for truncation on its own,
    so a storyline that came back empty cannot hide inside a long total."""
    wavs: list[bytes] = []
    parts = 0
    started = clock()
    for lines in segments:
        if len(segments) > 1 and clock() - started > SEGMENTED_BUDGET_S:
            raise TTSFailure(EXIT_HTTP, f"segmented voicing passed its "
                                        f"{SEGMENTED_BUDGET_S}s budget")
        part = [script[i] for i in lines]
        timeout = SEGMENT_HTTP_TIMEOUT_S if len(segments) > 1 else HTTP_TIMEOUT_S
        wav, blocks = extract_audio(call_api(build_request(part), api_key, post_fn, sleep_fn,
                                             timeout))
        words = contract.count_spoken_words(part)
        expected = contract.expected_duration_s(words)
        seconds = wav_duration(wav)
        floor = MIN_DURATION_RATIO * expected - (SEGMENT_SLACK_S if len(segments) > 1 else 0)
        if seconds < floor:
            where = f"segment {len(wavs) + 1} of {len(segments)}: " if len(segments) > 1 else ""
            raise TTSFailure(EXIT_TRUNCATED,
                             f"{where}audio is {seconds:.1f}s but {words} words need about "
                             f"{expected:.0f}s; treated as truncated", 200)
        wavs.append(wav)
        parts += blocks
    return wavs, parts


def synthesize(edit: dict, *, out: Path, work_dir: Path, api_key: str,
               post_fn: PostFn = http_post,
               sleep_fn: Callable[[float], None] = time.sleep,
               which: Callable[[str], str | None] = shutil.which,
               with_sound: bool = True,
               clock: Callable[[], float] = time.monotonic) -> dict:
    script = edit.get("script") if edit.get("on_air") is True else None
    if not isinstance(script, list) or not script:
        raise TTSFailure(EXIT_CONFIG, "edit is not on air or has no script")
    whole = [list(range(len(script)))]
    segments = split_segments(script) if with_sound else whole
    for lines in segments:  # fail on an unspeakable segment before any spend
        build_request([script[i] for i in lines])
    words = contract.count_spoken_words(script)
    expected = contract.expected_duration_s(words)
    if not api_key:
        raise TTSFailure(EXIT_CONFIG, "GEMINI_API_KEY is not configured")
    ffmpeg = which("ffmpeg")
    if not ffmpeg:  # checked before spending on the API call
        raise TTSFailure(EXIT_ENCODE, "ffmpeg is not installed on this runner")

    calls = 0

    def counted(url: str, headers: dict, body: bytes, timeout: float) -> tuple[int, bytes]:
        nonlocal calls
        calls += 1
        return post_fn(url, headers, body, timeout)

    sound_error: str | None = None
    try:
        wavs, parts = _voice(script, segments, api_key, counted, sleep_fn, clock)
    except TTSFailure as exc:
        if len(segments) == 1:
            raise
        # More requests are more chances to fail; the bulletin still airs, as
        # one dry take (no stingers), rather than not at all.
        sound_error = contract.clip(contract.clean_text(
            f"segmented voicing failed, aired as one dry take: {exc}"), 200)[0]
        print(f"::warning::aradio sound: {contract.gh_escape(sound_error)}")
        segments = whole
        wavs, parts = _voice(script, segments, api_key, counted, sleep_fn, clock)
    requests = calls  # HTTP requests made, retries included
    voice_s = sum(wav_duration(wav) for wav in wavs)
    if voice_s < MIN_DURATION_RATIO * expected:
        raise TTSFailure(EXIT_TRUNCATED,
                         f"audio is {voice_s:.1f}s but {words} words need about "
                         f"{expected:.0f}s; treated as truncated", 200)

    final, spans = wavs[0], None
    if with_sound and sound_error is None:
        try:
            cues = [line_cue(script[lines[0]]) or "transition" for lines in segments[1:]]
            mixed = sound.mix([sound.read_wav(wav) for wav in wavs], cues)
        except Exception as exc:  # the sound must never cost a voice it can air dry
            if len(wavs) > 1:
                raise TTSFailure(EXIT_NO_AUDIO, f"cannot join voice segments: {exc}",
                                 200) from exc
            sound_error = contract.clip(contract.clean_text(
                f"{type(exc).__name__}: {exc}"), 200)[0]
            print(f"::warning::aradio sound: airing the voice dry: "
                  f"{contract.gh_escape(sound_error)}")
        else:
            final = sound.write_wav(mixed.pcm)
            spans = [{"start_s": round(begin, 2), "end_s": round(end, 2),
                      "lines": [lines[0], lines[-1]],
                      "cue": line_cue(script[lines[0]]) if index else "intro"}
                     for index, ((begin, end), lines) in enumerate(zip(mixed.spans, segments))]
    duration = wav_duration(final)

    work_dir.mkdir(parents=True, exist_ok=True)
    wav_path = work_dir / f"aradio-{os.getpid()}.wav"
    try:
        wav_path.write_bytes(final)
        out.parent.mkdir(parents=True, exist_ok=True)
        encode_mp3(ffmpeg, wav_path, out)
    finally:
        wav_path.unlink(missing_ok=True)
    return {"ok": True, "mp3": str(out), "bytes": out.stat().st_size,
            "duration_s": round(duration, 1), "voice_s": round(voice_s, 1),
            "expected_s": round(expected, 1),
            "words": words, "error": None, "status": 200, "model": MODEL,
            "audio_parts": parts, "requests": requests,
            "sound": spans is not None, "sound_error": sound_error, "segments": spans}


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
    parser.add_argument("--no-sound", action="store_true",
                        help="air the voice dry: one request, no intro/transitions/outro")
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
        script = edit.get("script") or []
        try:
            segments = (split_segments(script) if not args.no_sound
                        else [list(range(len(script)))])
            requests = [build_request([script[i] for i in lines]) for lines in segments]
        except (TTSFailure, ValueError) as exc:
            print(f"::error::aradio TTS dry run: {contract.gh_escape(exc)}")
            return EXIT_CONFIG
        print(json.dumps(requests if len(requests) > 1 else requests[0],
                         indent=2, ensure_ascii=False))
        words = contract.count_spoken_words(script)
        turns = sum(len(request["input"][0]["content"]) for request in requests)
        print(f"dry run: {len(requests)} segment(s), {turns} turns, {words} words, "
              f"expected ~{contract.expected_duration_s(words):.0f}s; nothing sent",
              file=sys.stderr)
        return EXIT_OK

    if args.out is None:
        parser.error("--out is required unless --dry-run")
    work_dir = args.work_dir or args.out.parent
    try:
        result = synthesize(edit, out=args.out, work_dir=work_dir,
                            api_key=os.environ.get("GEMINI_API_KEY", "").strip(),
                            post_fn=post_fn, sleep_fn=sleep_fn, which=which,
                            with_sound=not args.no_sound)
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
          f"({result['voice_s']}s of voice in {result['requests']} segment(s), expected "
          f"~{result['expected_s']}s for {result['words']} words; "
          f"sound {'on' if result['sound'] else 'off'})")
    return finish(result, EXIT_OK)


if __name__ == "__main__":
    sys.exit(main())
