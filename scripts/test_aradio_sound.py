#!/usr/bin/env python3
"""Tests for scripts/aradio_sound.py: the station's synthesized sound kit."""

from __future__ import annotations

import io
import math
import unittest
import wave
from array import array

import aradio_sound as sound

RATE = 8000


def tone(seconds: float, amplitude: int = 6000, rate: int = RATE) -> sound.Pcm:
    return sound.Pcm(array("h", (int(amplitude * math.sin(2 * math.pi * 220 * n / rate))
                                 for n in range(int(seconds * rate)))), rate)


class KitTest(unittest.TestCase):
    def test_kit_is_deterministic_and_bounded(self):
        for make in (sound.intro, sound.transition, sound.outro):
            first, second = make(RATE), make(RATE)
            self.assertEqual(first, second, make.__name__)
            self.assertLessEqual(max(abs(v) for v in first), 0.95 + 1e-9)
            self.assertGreater(max(abs(v) for v in first), 0.5)

    def test_intro_is_long_enough_for_the_voice_entry(self):
        self.assertGreater(len(sound.intro(RATE)) / RATE, sound.INTRO_VOICE_AT_S)
        self.assertGreater(len(sound.transition(RATE)) / RATE, sound.TRANSITION_VOICE_AT_S)


class MixTest(unittest.TestCase):
    def test_voice_lands_untouched_outside_the_music_and_spans_are_exact(self):
        segments = [tone(3.0), tone(2.0), tone(4.0)]
        result = sound.mix(segments)
        self.assertEqual(3, len(result.spans))
        self.assertAlmostEqual(sound.INTRO_VOICE_AT_S, result.spans[0][0], places=3)
        for (start, end), segment in zip(result.spans, segments):
            self.assertAlmostEqual(segment.seconds, end - start, places=3)
        for (_, end), (start, _) in zip(result.spans, result.spans[1:]):
            gap = sound.SEGMENT_GAP_S + sound.TRANSITION_VOICE_AT_S
            self.assertAlmostEqual(gap, start - end, places=2)
        # The outro follows the last line.
        self.assertGreater(result.pcm.seconds, result.spans[-1][1] + 3.0)
        # Mid-way through a long segment, after the transition's tail, it is pure voice.
        start = int(result.spans[2][0] * RATE)
        middle = start + int(2.5 * RATE)
        self.assertEqual(list(segments[2].samples[int(2.5 * RATE):int(2.5 * RATE) + 200]),
                         list(result.pcm.samples[middle:middle + 200]))

    def test_music_is_ducked_under_speech(self):
        voice = tone(3.0)
        result = sound.mix([voice])
        start = int(result.spans[0][0] * RATE)
        out = result.pcm.samples
        # Music alone, just before the voice enters (outside the duck ramp) ...
        before = max(abs(v) for v in out[start - int(0.6 * RATE):start - int(0.3 * RATE)])
        # ... and the music under the voice: the mix minus the voice it holds.
        under = max(abs(out[n] - voice.samples[n - start])
                    for n in range(start + int(0.3 * RATE), start + int(0.6 * RATE)))
        self.assertGreater(before, 300)
        self.assertLess(under, 0.4 * before)

    def test_never_wraps_around_int16(self):
        loud = sound.Pcm(array("h", [32000 if (n // 20) % 2 else -32000
                                     for n in range(int(4 * RATE))]), RATE)
        result = sound.mix([loud, loud])
        self.assertLessEqual(max(result.pcm.samples), sound.INT16_MAX)
        self.assertGreaterEqual(min(result.pcm.samples), -sound.INT16_MAX)

    def test_limiter_is_continuous_and_never_folds_back(self):
        previous = -1
        for x in range(0, 60000, 37):
            y = sound._limit(float(x))
            self.assertGreaterEqual(y, previous, x)        # monotonic: no fold-back
            self.assertLessEqual(y, sound.INT16_MAX)
            previous = y
        self.assertEqual(1000, sound._limit(1000.0))      # linear below the knee
        knee = sound.LIMIT_KNEE
        self.assertLessEqual(abs(sound._limit(knee + 1) - sound._limit(knee)), 2)
        self.assertEqual(-sound._limit(40000.0), sound._limit(-40000.0))

    def test_hot_voice_under_music_has_no_dropouts(self):
        hot = sound.Pcm(array("h", [32000 if (n // 20) % 2 else -32000
                                    for n in range(int(4 * RATE))]), RATE)
        result = sound.mix([hot, hot])
        for (start_s, end_s) in result.spans:
            start, end = int(start_s * RATE), int(end_s * RATE)
            for n in range(start, end):
                voice = hot.samples[n - start]
                # Music may only add to a peak's magnitude or trim it gently.
                self.assertLess(abs(result.pcm.samples[n] - voice), 7000)
                if abs(voice) == 32000:
                    self.assertGreater(abs(result.pcm.samples[n]), 0.8 * sound.INT16_MAX)

    def test_unmixable_voices_raise(self):
        with self.assertRaises(sound.SoundError):
            sound.mix([])
        with self.assertRaises(sound.SoundError):
            sound.mix([tone(1.0), tone(1.0, rate=16000)])
        with self.assertRaises(sound.SoundError):
            sound.mix([sound.Pcm(array("h", [0] * RATE), RATE)])


class WavTest(unittest.TestCase):
    def wav(self, channels: int = 1, width: int = 2) -> bytes:
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as handle:
            handle.setnchannels(channels)
            handle.setsampwidth(width)
            handle.setframerate(RATE)
            handle.writeframes(b"\x01\x00" * channels * (width // 2 or 1) * 100)
        return buffer.getvalue()

    def test_round_trip(self):
        pcm = sound.read_wav(self.wav())
        self.assertEqual(RATE, pcm.rate)
        self.assertEqual(100, len(pcm.samples))
        self.assertEqual(pcm.samples, sound.read_wav(sound.write_wav(pcm)).samples)

    def test_streaming_size_reads_to_the_end(self):
        raw = bytearray(self.wav())
        data_at = raw.index(b"data")
        raw[data_at + 4:data_at + 8] = b"\xff\xff\xff\xff"
        self.assertEqual(100, len(sound.read_wav(bytes(raw)).samples))

    def test_rejects_non_mono_16_bit(self):
        with self.assertRaises(sound.SoundError):
            sound.read_wav(self.wav(channels=2))
        with self.assertRaises(sound.SoundError):
            sound.read_wav(b"not a wav")


if __name__ == "__main__":
    unittest.main()
