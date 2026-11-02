#!/usr/bin/env python3
"""Aradio's sonic identity: the signature sting, story transitions, the outro.

Contract: docs/aradio.md -> "Sound design". Every sound is SYNTHESIZED here,
deterministically, from the standard library: no sample files, no music
model, no licence to track, and the same bytes on every run (the noise is
seeded). A change to the sound is a reviewed diff to this file.

The identity is one three-note motif, A - E - A an octave up ("A-R-A"),
played on an FM bell:

  intro       riser -> sub-bass hit + A-major stab -> the motif -> a pad that
              stays under the opening line, ducked, then fades
  transition  a short swoosh and the motif's last two notes, placed where the
              editor marked `[transition]` (a new storyline)
  outro       the motif descending over the resolving chord, after the
              sign-off

`mix()` lays voice segments and sounds on one timeline at the voice's own
sample rate and returns the mixed 16-bit mono PCM plus the exact span of each
voice segment, so the dashboard can follow the transcript inside the real
voice time instead of across the music.

`python scripts/aradio_sound.py --preview out.wav` renders the kit around
silent placeholders, for listening to a change before it airs.
"""

from __future__ import annotations

import argparse
import math
import random
import struct
import sys
import wave
from array import array
from dataclasses import dataclass
from pathlib import Path

INT16_MAX = 32767
# Music under speech sits about 14 dB down: present, never competing.
DUCK_GAIN = 0.2
DUCK_RAMP_S = 0.25
# Sound level relative to the voice's RMS (sounds are denser than speech).
SOUND_TO_VOICE_RMS = 0.75
# Where the voice enters each sound, and the silence after the last line.
INTRO_VOICE_AT_S = 3.1
TRANSITION_VOICE_AT_S = 0.75
OUTRO_GAP_S = 0.35
SEGMENT_GAP_S = 0.15

A2, E3, A3, CS4, E4, A4, B4, CS5, E5, A5, CS6, E6 = (
    110.0, 164.81, 220.0, 277.18, 329.63, 440.0, 493.88, 554.37, 659.26,
    880.0, 1108.73, 1318.51)


class SoundError(Exception):
    """The voice audio cannot be mixed (format, rate); the caller decides."""


# ── Synthesis primitives (float buffers in [-1, 1]) ───────────────────────

def _silence(seconds: float, rate: int) -> list[float]:
    return [0.0] * max(0, int(round(seconds * rate)))


def _add(dest: list[float], src: list[float], at_s: float, rate: int,
         gain: float = 1.0) -> None:
    start = int(round(at_s * rate))
    if start + len(src) > len(dest):
        dest.extend([0.0] * (start + len(src) - len(dest)))
    for i, value in enumerate(src):
        dest[start + i] += value * gain


def _bell(freq: float, seconds: float, rate: int, *, ratio: float = 3.5,
          index: float = 2.2) -> list[float]:
    """FM bell: a carrier whose modulation index decays faster than its body."""
    out = []
    two_pi = 2.0 * math.pi
    for n in range(int(seconds * rate)):
        t = n / rate
        mod = index * math.exp(-t * 6.0) * math.sin(two_pi * freq * ratio * t)
        attack = min(1.0, t / 0.004)
        out.append(attack * math.exp(-t * 3.2) * math.sin(two_pi * freq * t + mod))
    return out


def _pad(freqs: tuple[float, ...], seconds: float, rate: int, *,
         attack: float = 0.04, release: float = 1.6) -> list[float]:
    """A warm chord: three detuned voices per note, a few harmonics each."""
    voices = [(f * detune, phase) for f in freqs
              for detune, phase in ((1.0, 0.0), (1.0035, 1.3), (0.9965, 2.1))]
    harmonics = ((1, 1.0), (2, 0.35), (3, 0.12))
    scale = 1.0 / (len(voices) * sum(weight for _, weight in harmonics))
    out = []
    two_pi = 2.0 * math.pi
    total = int(seconds * rate)
    for n in range(total):
        t = n / rate
        env = min(1.0, t / attack) * min(1.0, (total - n) / (release * rate))
        sample = 0.0
        for freq, phase in voices:
            for harmonic, weight in harmonics:
                sample += weight * math.sin(two_pi * freq * harmonic * t + phase)
        out.append(env * scale * sample)
    return out


def _boom(seconds: float, rate: int) -> list[float]:
    """Sub-bass hit: a sine sweeping 140 -> 42 Hz with a short click on top."""
    out = []
    phase = 0.0
    for n in range(int(seconds * rate)):
        t = n / rate
        freq = 42.0 + 98.0 * math.exp(-t * 18.0)
        phase += 2.0 * math.pi * freq / rate
        click = math.exp(-t * 400.0) * 0.4
        out.append((math.sin(phase) + click) * math.exp(-t * 4.0) * min(1.0, t / 0.002))
    return out


def _swoosh(seconds: float, rate: int, *, rising: bool, seed: int) -> list[float]:
    """Filtered noise whose brightness and level sweep toward the hit."""
    rng = random.Random(seed)
    out = []
    low = 0.0
    total = int(seconds * rate)
    for n in range(total):
        x = n / max(1, total - 1)
        shape = x ** 2.2 if rising else (1.0 - x) ** 1.6
        cutoff = 300.0 + 7000.0 * shape
        alpha = 1.0 - math.exp(-2.0 * math.pi * cutoff / rate)
        low += alpha * (rng.uniform(-1.0, 1.0) - low)
        out.append(low * shape)
    return out


def _normalize(buffer: list[float], peak: float = 0.95) -> list[float]:
    top = max((abs(v) for v in buffer), default=0.0)
    return [v * peak / top for v in buffer] if top > 0 else buffer


# ── The kit ───────────────────────────────────────────────────────────────

def intro(rate: int) -> list[float]:
    """~5.4 s: riser, hit at 1.0 s, motif, then a pad the voice enters over."""
    out = _silence(5.4, rate)
    _add(out, _swoosh(1.0, rate, rising=True, seed=11), 0.0, rate, 0.55)
    _add(out, _boom(1.4, rate), 1.0, rate, 0.9)
    _add(out, _pad((A2, E3, A3, CS4, E4), 4.4, rate, attack=0.01, release=2.6), 1.0, rate, 1.1)
    for at, note in ((1.0, A4), (1.25, E5), (1.5, A5)):
        _add(out, _bell(note, 1.8, rate), at, rate, 0.5)
    _add(out, _bell(CS6, 2.2, rate, index=1.4), 2.0, rate, 0.3)
    return _normalize(out)


def transition(rate: int) -> list[float]:
    """~1.6 s: a quick swoosh and the motif's E -> A, voice back at 0.75 s."""
    out = _silence(1.6, rate)
    _add(out, _swoosh(0.35, rate, rising=True, seed=23), 0.0, rate, 0.45)
    _add(out, _bell(E5, 1.2, rate, index=1.8), 0.3, rate, 0.55)
    _add(out, _bell(A5, 1.3, rate, index=1.8), 0.45, rate, 0.6)
    _add(out, _swoosh(0.5, rate, rising=False, seed=29), 0.35, rate, 0.12)
    return _normalize(out)


def outro(rate: int) -> list[float]:
    """~4 s: the motif descending over the A-major resolution, fading out."""
    out = _silence(4.0, rate)
    for at, note in ((0.0, A5), (0.25, E5), (0.5, A4)):
        _add(out, _bell(note, 2.0, rate), at, rate, 0.5)
    _add(out, _pad((A2, E3, A3, CS4, E4, B4), 3.6, rate, attack=0.2, release=2.8), 0.4, rate, 0.9)
    _add(out, _boom(1.2, rate), 0.5, rate, 0.45)
    _add(out, _bell(CS5, 2.6, rate, index=1.2), 0.75, rate, 0.25)
    return _normalize(out)


# ── Mixing ────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Pcm:
    """16-bit mono PCM samples at `rate`."""
    samples: array
    rate: int

    @property
    def seconds(self) -> float:
        return len(self.samples) / self.rate


def read_wav(wav: bytes) -> Pcm:
    """16-bit mono PCM from a RIFF/WAVE file; anything else is a SoundError.

    Like aradio_tts.wav_duration, a 0 or 0xFFFFFFFF data size (streaming
    writers) means "to the end of the file".
    """
    if wav[:4] != b"RIFF" or wav[8:12] != b"WAVE":
        raise SoundError("audio is not a RIFF/WAVE file")
    offset, channels, bits, rate, fmt = 12, 0, 0, 0, 0
    while offset + 8 <= len(wav):
        chunk_id = wav[offset:offset + 4]
        size = struct.unpack("<I", wav[offset + 4:offset + 8])[0]
        start = offset + 8
        if chunk_id == b"fmt " and size >= 16:
            fmt, channels, rate, _, _, bits = struct.unpack("<HHIIHH", wav[start:start + 16])
        elif chunk_id == b"data":
            if (fmt, channels, bits) != (1, 1, 16) or rate <= 0:
                raise SoundError(f"voice is not 16-bit mono PCM (format {fmt}, "
                                 f"{channels} ch, {bits} bit)")
            available = len(wav) - start
            length = available if size in (0, 0xFFFFFFFF) else min(size, available)
            samples = array("h")
            samples.frombytes(wav[start:start + length - (length % 2)])
            if sys.byteorder != "little":
                samples.byteswap()
            return Pcm(samples, rate)
        offset = start + size + (size & 1)
    raise SoundError("WAV has no data chunk")


def write_wav(pcm: Pcm) -> bytes:
    samples = array("h", pcm.samples)
    if sys.byteorder != "little":
        samples.byteswap()
    data = samples.tobytes()
    header = b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVE"
    header += b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, pcm.rate, pcm.rate * 2, 2, 16)
    return header + b"data" + struct.pack("<I", len(data)) + data


def _rms(samples: array, stride: int = 16) -> float:
    picked = samples[::stride]
    if not picked:
        return 0.0
    return math.sqrt(sum(v * v for v in picked) / len(picked))


def _active_rms(buffer: list[float]) -> float:
    """RMS over the part of a sound that is actually sounding."""
    loud = [v for v in buffer[::8] if abs(v) > 0.02]
    return math.sqrt(sum(v * v for v in loud) / len(loud)) if loud else 0.0


@dataclass(frozen=True)
class Mix:
    pcm: Pcm
    # Exact [start_s, end_s) of each voice segment in the mixed audio.
    spans: list[tuple[float, float]]


def mix(segments: list[Pcm]) -> Mix:
    """intro, voice segments joined by transitions, outro; music ducked under voice."""
    if not segments:
        raise SoundError("no voice segments to mix")
    rate = segments[0].rate
    if any(segment.rate != rate for segment in segments):
        raise SoundError("voice segments have different sample rates")
    if any(not segment.samples for segment in segments):
        raise SoundError("a voice segment is empty")

    voice_level = _rms(_concat([segment.samples for segment in segments]))
    if voice_level <= 0:
        raise SoundError("voice is silent")

    sounds: list[tuple[int, list[float]]] = []   # (start sample, buffer)
    spans: list[tuple[int, int]] = []
    kit_intro, kit_transition, kit_outro = intro(rate), transition(rate), outro(rate)
    sounds.append((0, kit_intro))
    cursor = int(INTRO_VOICE_AT_S * rate)
    for index, segment in enumerate(segments):
        if index:
            cursor += int(SEGMENT_GAP_S * rate)
            sounds.append((cursor, kit_transition))
            cursor += int(TRANSITION_VOICE_AT_S * rate)
        spans.append((cursor, cursor + len(segment.samples)))
        cursor += len(segment.samples)
    cursor += int(OUTRO_GAP_S * rate)
    sounds.append((cursor, kit_outro))
    total = max(cursor + len(kit_outro), max(start + len(buf) for start, buf in sounds))

    out = array("h", bytes(2 * total))
    for (start, _), segment in zip(spans, segments):
        out[start:start + len(segment.samples)] = segment.samples

    ramp = max(1, int(DUCK_RAMP_S * rate))

    def duck(n: int) -> float:
        # 1.0 away from speech, DUCK_GAIN inside it, a linear ramp into each span.
        for begin, end in spans:
            if begin <= n < end:
                return DUCK_GAIN
            if begin - ramp <= n < begin:
                return 1.0 - (1.0 - DUCK_GAIN) * (n - begin + ramp) / ramp
        return 1.0

    for start, buffer in sounds:
        level = _active_rms(buffer)
        gain = (SOUND_TO_VOICE_RMS * voice_level / level) if level else 0.0
        gain = min(gain, 0.9 * INT16_MAX)   # buffers peak at 0.95: never near full scale
        for i, value in enumerate(buffer):
            if value == 0.0:
                continue
            n = start + i
            out[n] = _limit(out[n] + value * gain * duck(n))
    return Mix(Pcm(out, rate), [(b / rate, e / rate) for b, e in spans])


LIMIT_KNEE = 0.8 * INT16_MAX


def _limit(x: float) -> int:
    """Soft knee: linear up to 80 % of full scale, then tanh-compressed into
    the remaining 20 %. Continuous and monotonic, so a speech peak plus music
    is rounded off, never folded back (a dropout click) or hard-clipped."""
    level = abs(x)
    if level <= LIMIT_KNEE:
        return int(x)
    room = INT16_MAX - LIMIT_KNEE
    return int(math.copysign(LIMIT_KNEE + room * math.tanh((level - LIMIT_KNEE) / room), x))


def _concat(parts: list[array]) -> array:
    joined = array("h")
    for part in parts:
        joined.extend(part)
    return joined


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--preview", type=Path, required=True,
                        help="write a WAV of the kit around placeholder voice segments")
    parser.add_argument("--rate", type=int, default=24000)
    parser.add_argument("--segments", type=int, default=3,
                        help="number of placeholder voice segments (transitions = n - 1)")
    parser.add_argument("--segment-seconds", type=float, default=4.0)
    args = parser.parse_args(argv)
    # A quiet 200 Hz hum stands in for speech, so the ducking is audible.
    tone = array("h", (int(3000 * math.sin(2 * math.pi * 200 * n / args.rate))
                       for n in range(int(args.segment_seconds * args.rate))))
    result = mix([Pcm(tone, args.rate) for _ in range(max(1, args.segments))])
    with wave.open(str(args.preview), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(args.rate)
        handle.writeframes(write_wav(result.pcm)[44:])
    spans = ", ".join(f"{b:.2f}-{e:.2f}s" for b, e in result.spans)
    print(f"wrote {args.preview} ({result.pcm.seconds:.1f}s); voice spans: {spans}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
