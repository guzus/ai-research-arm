#!/usr/bin/env python3
"""Tests for scripts/aradio_tts.py. No network, no real ffmpeg, no API key."""

from __future__ import annotations

import base64
import contextlib
import io
import json
import os
import struct
import tempfile
import unittest
import wave
from pathlib import Path
from unittest import mock

import aradio_tts as tts

RATE = 8000


def wav_bytes(seconds: float, rate: int = RATE, *, voiced: bool = False) -> bytes:
    """Silence by default (the mixer refuses it, so the voice airs dry);
    `voiced` gives a square wave the mixer accepts."""
    buffer = io.BytesIO()
    frames = (b"".join(struct.pack("<h", 4000 if (n // 20) % 2 else -4000)
                       for n in range(int(seconds * rate))) if voiced
              else b"\x00\x00" * int(seconds * rate))
    with wave.open(buffer, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(frames)
    return buffer.getvalue()


def response(audio: bytes | None, mime: str = "audio/wav") -> bytes:
    content = [] if audio is None else [{"type": "audio", "mime_type": mime,
                                         "data": base64.b64encode(audio).decode()}]
    return json.dumps({"id": "int-1", "steps": [
        {"type": "user_input", "content": [{"type": "text", "text": "hi"}]},
        {"type": "model_output", "content": content}]}).encode()


def script(lines: int = 12, words: int = 25) -> list[str]:
    return [f"Speaker {1 if i % 2 == 0 else 2}: " + " ".join(["word"] * words)
            for i in range(lines)]


class FakePost:
    def __init__(self, *replies):
        self.replies = list(replies)
        self.calls: list[dict] = []

    def __call__(self, url, headers, body, timeout):
        self.calls.append({"url": url, "headers": headers, "body": json.loads(body)})
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply


class TTSBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.ffmpeg = self.root / "bin" / "ffmpeg"
        self.ffmpeg.parent.mkdir()
        self.ffmpeg.write_text('#!/bin/sh\nfor a; do out="$a"; done\n'
                               'printf "ID3-fake-mp3-bytes" > "$out"\n', encoding="utf-8")
        self.ffmpeg.chmod(0o755)
        self.edit_path = self.root / "edit.json"
        self.write_edit({"schema": 1, "on_air": True, "headline": "h", "ops": [],
                         "script": script(), "covers": [], "note": ""})
        self.work = self.root / "work"
        self.out = self.work / "bulletin.mp3"
        self.result = self.root / "result.json"

    def tearDown(self):
        self.tmp.cleanup()

    def write_edit(self, edit: dict) -> None:
        self.edit_path.write_text(json.dumps(edit), encoding="utf-8")

    def run_main(self, post, *, key="test-key", ffmpeg=True, extra=()):
        sleeps: list[float] = []
        stdout, stderr = io.StringIO(), io.StringIO()
        env = {"GEMINI_API_KEY": key} if key else {}
        with mock.patch.dict(os.environ, env, clear=False), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            if not key:
                os.environ.pop("GEMINI_API_KEY", None)
            code = tts.main(["--edit", str(self.edit_path), "--out", str(self.out),
                             "--result", str(self.result), "--work-dir", str(self.work),
                             *extra],
                            post_fn=post, sleep_fn=sleeps.append,
                            which=lambda name: str(self.ffmpeg) if ffmpeg else None)
        return code, stdout.getvalue(), stderr.getvalue(), sleeps

    def result_json(self) -> dict:
        return json.loads(self.result.read_text(encoding="utf-8"))


class RequestShapeTest(unittest.TestCase):
    def test_request_uses_documented_fields_only(self):
        request = tts.build_request(script(lines=2))
        self.assertEqual("gemini-3.8-flash-tts", request["model"])
        self.assertEqual({"type": "audio"}, request["response_format"])
        speech = request["generation_config"]["speech_config"]
        self.assertEqual({"speakers"}, set(speech))
        self.assertNotIn('"mode"', json.dumps(request))
        self.assertEqual([{"speaker": "Speaker 1", "voice": "Charon"},
                          {"speaker": "Speaker 2", "voice": "Puck"}], speech["speakers"])
        part = request["input"][0]["content"][1]
        self.assertEqual("user_input", request["input"][0]["type"])
        self.assertEqual("text", part["type"])
        self.assertEqual([{"type": "speech_metadata", "speaker": "Speaker 2",
                           "style": tts.STYLES["Speaker 2"]}], part["annotations"])
        self.assertFalse(part["text"].startswith("Speaker"))

    def test_audio_tags_are_translated(self):
        turns = tts.build_request([
            "Speaker 1: [high_energy] Big news tonight.",
            "Speaker 2: Revenue hit [emphasis]ten billion dollars[/emphasis], a record.",
            "Speaker 1: And then [dramatic_pause] it was over × two & more — really.",
        ])["input"][0]["content"]
        self.assertEqual("Big news tonight.", turns[0]["text"])
        self.assertEqual(tts.ENERGETIC_STYLE, turns[0]["annotations"][0]["style"])
        self.assertEqual("Revenue hit ten billion dollars, a record.", turns[1]["text"])
        self.assertTrue(turns[1]["annotations"][0]["style"].endswith("stress the key figure"))
        self.assertIn("<short pause>", turns[2]["text"])
        self.assertIn("times two and more, really", turns[2]["text"])
        for turn in turns:
            self.assertNotIn("[", turn["text"])
            self.assertNotIn("Speaker", turn["text"])


class SynthesisTest(TTSBase):
    def test_success_writes_mp3_and_result(self):
        post = FakePost((200, response(wav_bytes(100))))
        code, stdout, _, _ = self.run_main(post)
        self.assertEqual(0, code, stdout)
        result = self.result_json()
        self.assertTrue(result["ok"])
        self.assertEqual(str(self.out), result["mp3"])
        self.assertEqual(self.out.stat().st_size, result["bytes"])
        self.assertAlmostEqual(100.0, result["duration_s"], places=1)
        self.assertEqual(300, result["words"])
        self.assertEqual("test-key", post.calls[0]["headers"]["x-goog-api-key"])
        self.assertEqual(tts.API_URL, post.calls[0]["url"])
        self.assertEqual([], list(self.work.glob("*.wav")))

    def test_truncated_audio_fails_loudly(self):
        code, stdout, _, _ = self.run_main(FakePost((200, response(wav_bytes(20)))))
        self.assertEqual(tts.EXIT_TRUNCATED, code)
        self.assertFalse(self.out.exists())
        result = self.result_json()
        self.assertFalse(result["ok"])
        self.assertIn("truncated", result["error"])
        self.assertIn("::error::aradio TTS failed", stdout)

    def test_http_error_reports_status_and_body_without_retry(self):
        body = json.dumps({"error": {"code": 400, "message": "Unknown name \"mode\"",
                                     "status": "INVALID_ARGUMENT"}}).encode()
        post = FakePost((400, body))
        code, _, stderr, sleeps = self.run_main(post)
        self.assertEqual(tts.EXIT_HTTP, code)
        self.assertEqual(1, len(post.calls))
        self.assertEqual([], sleeps)
        self.assertIn("HTTP status: 400", stderr)
        self.assertIn("INVALID_ARGUMENT", stderr)
        result = self.result_json()
        self.assertEqual(400, result["status"])
        self.assertIn("HTTP 400", result["error"])
        self.assertIn("Unknown name", result["error"])

    def test_server_error_retries_once_then_succeeds(self):
        post = FakePost((503, b"busy"), (200, response(wav_bytes(100))))
        code, _, _, sleeps = self.run_main(post)
        self.assertEqual(0, code)
        self.assertEqual(2, len(post.calls))
        self.assertEqual([tts.RETRY_DELAY_S], sleeps)

    def test_rate_limit_twice_fails(self):
        post = FakePost((429, b"slow down"), (429, b"slow down"))
        code, _, stderr, _ = self.run_main(post)
        self.assertEqual(tts.EXIT_HTTP, code)
        self.assertEqual(2, len(post.calls))
        self.assertIn("slow down", stderr)

    def test_network_error_retries_once(self):
        post = FakePost(OSError("reset"), TimeoutError("timed out"))
        code, _, _, sleeps = self.run_main(post)
        self.assertEqual(tts.EXIT_HTTP, code)
        self.assertEqual(1, len(sleeps))
        self.assertIn("TimeoutError", self.result_json()["error"])

    def test_response_without_audio_fails(self):
        code, _, stderr, _ = self.run_main(FakePost((200, response(None))))
        self.assertEqual(tts.EXIT_NO_AUDIO, code)
        self.assertIn("model_output", stderr)

    def test_missing_key_or_ffmpeg_never_calls_the_api(self):
        post = FakePost()
        code, _, _, _ = self.run_main(post, key="")
        self.assertEqual(tts.EXIT_CONFIG, code)
        self.assertIn("GEMINI_API_KEY", self.result_json()["error"])
        code, _, _, _ = self.run_main(post, ffmpeg=False)
        self.assertEqual(tts.EXIT_ENCODE, code)
        self.assertEqual([], post.calls)

    def test_off_air_edit_is_rejected(self):
        self.write_edit({"schema": 1, "on_air": False, "headline": "h", "ops": [],
                         "script": [], "covers": [], "note": "quiet"})
        code, _, _, _ = self.run_main(FakePost())
        self.assertEqual(tts.EXIT_CONFIG, code)

    def test_dry_run_prints_request_without_network(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = tts.main(["--edit", str(self.edit_path), "--dry-run"],
                            post_fn=FakePost(), which=lambda name: None)
        self.assertEqual(0, code)
        request = json.loads(stdout.getvalue())
        self.assertEqual("gemini-3.8-flash-tts", request["model"])
        self.assertIn("nothing sent", stderr.getvalue())


class AudioDecodingTest(unittest.TestCase):
    def test_streaming_wav_header_uses_actual_bytes(self):
        wav = bytearray(wav_bytes(3))
        data_at = bytes(wav).index(b"data")
        wav[data_at + 4:data_at + 8] = struct.pack("<I", 0xFFFFFFFF)
        self.assertAlmostEqual(3.0, tts.wav_duration(bytes(wav)), places=3)

    def test_l16_payload_is_wrapped_as_wav(self):
        pcm = b"\x00\x00" * 24000 * 2
        wav, parts = tts.extract_audio(response(pcm, mime="audio/l16;codec=pcm;rate=24000"))
        self.assertEqual(1, parts)
        self.assertAlmostEqual(2.0, tts.wav_duration(wav), places=3)

    def test_last_audio_block_is_used(self):
        payload = json.loads(response(wav_bytes(1)))
        payload["steps"][1]["content"].append(
            {"type": "audio", "data": base64.b64encode(wav_bytes(5)).decode()})
        wav, parts = tts.extract_audio(json.dumps(payload).encode())
        self.assertEqual(2, parts)
        self.assertAlmostEqual(5.0, tts.wav_duration(wav), places=3)


class SoundDesignTest(TTSBase):
    def segmented_script(self) -> list[str]:
        lines = script()
        lines[4] = lines[4].replace(": ", ": [transition] ", 1)
        lines[9] = lines[9].replace(": ", ": [transition] ", 1)
        return lines

    def test_segments_split_at_transition_lines(self):
        self.assertEqual([[0, 1, 2, 3], [4, 5, 6, 7, 8], [9, 10, 11]],
                         tts.split_segments(self.segmented_script()))
        self.assertEqual([list(range(12))], tts.split_segments(script()))

    def test_each_segment_is_voiced_then_mixed_with_exact_spans(self):
        self.write_edit({"schema": 1, "on_air": True, "headline": "h", "ops": [],
                         "script": self.segmented_script(), "covers": [], "note": ""})
        post = FakePost(*[(200, response(wav_bytes(seconds, voiced=True)))
                          for seconds in (30, 40, 30)])
        code, stdout, _, _ = self.run_main(post)
        self.assertEqual(0, code, stdout)
        self.assertEqual([4, 5, 3], [len(call["body"]["input"][0]["content"])
                                     for call in post.calls])
        for call in post.calls:
            for part in call["body"]["input"][0]["content"]:
                self.assertNotIn("[", part["text"])
        result = self.result_json()
        self.assertTrue(result["sound"])
        self.assertEqual(3, result["requests"])
        self.assertAlmostEqual(100.0, result["voice_s"], places=1)
        self.assertGreater(result["duration_s"], result["voice_s"] + 5)
        spans = result["segments"]
        self.assertEqual([[0, 3], [4, 8], [9, 11]], [span["lines"] for span in spans])
        self.assertAlmostEqual(40.0, spans[1]["end_s"] - spans[1]["start_s"], places=1)
        self.assertLessEqual(spans[-1]["end_s"], result["duration_s"])

    def test_no_sound_is_one_dry_request(self):
        self.write_edit({"schema": 1, "on_air": True, "headline": "h", "ops": [],
                         "script": self.segmented_script(), "covers": [], "note": ""})
        post = FakePost((200, response(wav_bytes(100, voiced=True))))
        code, stdout, _, _ = self.run_main(post, extra=("--no-sound",))
        self.assertEqual(0, code, stdout)
        result = self.result_json()
        self.assertEqual((1, False, None), (result["requests"], result["sound"],
                                            result["segments"]))
        self.assertAlmostEqual(100.0, result["duration_s"], places=1)

    def test_unmixable_single_voice_airs_dry_with_a_warning(self):
        code, stdout, _, _ = self.run_main(FakePost((200, response(wav_bytes(100)))))
        self.assertEqual(0, code, stdout)
        result = self.result_json()
        self.assertFalse(result["sound"])
        self.assertIn("silent", result["sound_error"])
        self.assertIn("::warning::", stdout)

    def test_unmixable_segments_fail_loudly(self):
        self.write_edit({"schema": 1, "on_air": True, "headline": "h", "ops": [],
                         "script": self.segmented_script(), "covers": [], "note": ""})
        post = FakePost(*[(200, response(wav_bytes(35))) for _ in range(3)])
        code, _, _, _ = self.run_main(post)
        self.assertEqual(tts.EXIT_NO_AUDIO, code)
        self.assertFalse(self.result_json()["ok"])

    def test_a_truncated_segment_falls_back_to_one_dry_take(self):
        # Segment 2 (5 of 12 lines, ~48 s) comes back at 2 s: the total (62 s
        # of 115 s expected) would pass the whole-voice ratio, the segment must not.
        self.write_edit({"schema": 1, "on_air": True, "headline": "h", "ops": [],
                         "script": self.segmented_script(), "covers": [], "note": ""})
        post = FakePost((200, response(wav_bytes(30, voiced=True))),
                        (200, response(wav_bytes(2, voiced=True))),
                        (200, response(wav_bytes(100, voiced=True))))
        code, stdout, _, _ = self.run_main(post)
        self.assertEqual(0, code, stdout)
        result = self.result_json()
        self.assertEqual(12, len(post.calls[-1]["body"]["input"][0]["content"]))
        self.assertEqual((False, None, 3), (result["sound"], result["segments"],
                                            result["requests"]))
        self.assertIn("segment 2 of 3", result["sound_error"])
        self.assertAlmostEqual(100.0, result["duration_s"], places=1)

    def test_a_failed_segment_request_falls_back_and_a_failed_fallback_fails(self):
        self.write_edit({"schema": 1, "on_air": True, "headline": "h", "ops": [],
                         "script": self.segmented_script(), "covers": [], "note": ""})
        post = FakePost((200, response(wav_bytes(30, voiced=True))),
                        (400, b'{"error": {"message": "bad"}}'),
                        (400, b'{"error": {"message": "still bad"}}'))
        code, _, _, _ = self.run_main(post)
        self.assertEqual(tts.EXIT_HTTP, code)
        self.assertIn("still bad", self.result_json()["error"])

    def test_segmented_budget_stops_new_requests(self):
        ticks = iter([0.0, 10.0, 20.0, tts.SEGMENTED_BUDGET_S + 1, 0.0])
        post = FakePost((200, response(wav_bytes(30, voiced=True))),
                        (200, response(wav_bytes(40, voiced=True))),
                        (200, response(wav_bytes(100, voiced=True))))
        result = tts.synthesize(
            {"on_air": True, "script": self.segmented_script()}, out=self.out,
            work_dir=self.work, api_key="k", post_fn=post, sleep_fn=lambda _: None,
            which=lambda _: str(self.ffmpeg), clock=lambda: next(ticks))
        self.assertEqual(3, len(post.calls))           # 2 segments, then the dry take
        self.assertIn("budget", result["sound_error"])
        self.assertFalse(result["sound"])

    def test_segment_requests_use_the_shorter_timeout(self):
        timeouts = []

        def post(url, headers, body, timeout):
            timeouts.append(timeout)
            return 200, response(wav_bytes(40, voiced=True))

        self.write_edit({"schema": 1, "on_air": True, "headline": "h", "ops": [],
                         "script": self.segmented_script(), "covers": [], "note": ""})
        code, stdout, _, _ = self.run_main(post)
        self.assertEqual(0, code, stdout)
        self.assertEqual([tts.SEGMENT_HTTP_TIMEOUT_S] * 3, timeouts)


if __name__ == "__main__":
    unittest.main()
