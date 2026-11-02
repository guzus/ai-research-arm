#!/usr/bin/env python3
"""Aradio's sonic identity: the signature sting, story transitions, the outro.

Contract: docs/aradio.md -> "Sound design". Every sound is SYNTHESIZED here,
deterministically, from the standard library: no sample files, no music
model, no licence to track, and the same bytes on every run (the noise is
seeded). A change to the sound is a reviewed diff to this file.

The identity is one three-note motif, A - E - A an octave up ("A-R-A"),
played on an FM bell:

  intro       riser + snare-roll build -> THE HIT (kick, sub boom, crash,
              brass stab) -> the motif -> a 128 bpm groove the opening line
              rides over, ducked
  transition  a reverse-cymbal swell into a hit and the motif's last two
              notes, where the editor marked `[transition]` (a new storyline)
  gong        a big tam-tam, where the editor marked `[gong]` (the one huge
              moment of a bulletin: a mega round, an acquisition, an IPO)
  outro       a bar of groove under the motif descending, then a final hit
              ringing out, after the sign-off

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
# Sound level relative to the voice's RMS: stings hit at full speech level.
SOUND_TO_VOICE_RMS = 1.0
# Where the voice enters each sound, and the silence after the last line.
INTRO_VOICE_AT_S = 4.2
TRANSITION_VOICE_AT_S = 1.3
GONG_VOICE_AT_S = 1.7
OUTRO_GAP_S = 0.35
SEGMENT_GAP_S = 0.15
# Cues between segments (check_aradio.CUE_TAGS without the brackets).
CUES = ("transition", "gong")

BPM = 128.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT

A1, E2, A2, CS3, D3, E3, FS3, A3, CS4, D4, E4, FS4, A4, B4, CS5, E5, A5, CS6, E6 = (
    55.0, 82.41, 110.0, 138.59, 146.83, 164.81, 185.0, 220.0, 277.18, 293.66,
    329.63, 369.99, 440.0, 493.88, 554.37, 659.26, 880.0, 1108.73, 1318.51)
A_MAJOR = (A2, E3, A3, CS4, E4)
D_MAJOR = (D3, FS3, A3, D4, FS4)


class SoundError(Exception):
    """The voice audio cannot be mixed (format, rate); the caller decides."""


# ── Synthesis primitives (float buffers in [-1, 1]) ───────────────────────
#
# Pure Python, so everything expensive is a table lookup: oscillators read
# precomputed single-cycle wavetables, noise comes from a seeded RNG.

TABLE = 2048
TWO_PI = 2.0 * math.pi


def _silence(seconds: float, rate: int) -> list[float]:
    return [0.0] * max(0, int(round(seconds * rate)))


def _add(dest: list[float], src: list[float], at_s: float, rate: int,
         gain: float = 1.0) -> None:
    start = int(round(at_s * rate))
    if start + len(src) > len(dest):
        dest.extend([0.0] * (start + len(src) - len(dest)))
    for i, value in enumerate(src):
        dest[start + i] += value * gain


def _saw_table(freq: float, rate: int, brightness: float) -> list[float]:
    """One band-limited sawtooth cycle; `brightness` 0..1 rolls off the top."""
    limit = max(1, int(min(rate / 2.2, 9000.0 * brightness + 400.0) / freq))
    weights = [(k, (1.0 / k) * math.exp(-k * (1.0 - brightness) * 0.35))
               for k in range(1, limit + 1)]
    table = [sum(w * math.sin(TWO_PI * k * i / TABLE) for k, w in weights)
             for i in range(TABLE)]
    top = max(abs(v) for v in table) or 1.0
    return [v / top for v in table]


def _brass(freqs: tuple[float, ...], seconds: float, rate: int, *,
           attack: float = 0.012, decay: float = 2.5, sustain: float = 0.0) -> list[float]:
    """A brassy synth stab: detuned saws whose brightness falls after the hit
    (a crossfade between a bright and a dark wavetable per voice)."""
    voices = []
    for freq in freqs:
        bright, dark = _saw_table(freq, rate, 1.0), _saw_table(freq, rate, 0.15)
        for detune, phase in ((1.0, 0.0), (1.006, 0.37), (0.994, 0.71)):
            voices.append((bright, dark, freq * detune * TABLE / rate, phase * TABLE))
    scale = 1.0 / len(voices)
    total = int(seconds * rate)
    out = []
    for n in range(total):
        t = n / rate
        amp = min(1.0, t / attack) * (sustain + (1.0 - sustain) * math.exp(-t * decay))
        amp *= min(1.0, (total - n) / (0.08 * rate))
        mix = math.exp(-t * 6.0)  # 1 = bright at the hit, toward dark
        sample = 0.0
        for bright, dark, step, phase in voices:
            i = int(phase + n * step) % TABLE
            sample += dark[i] + mix * (bright[i] - dark[i])
        out.append(amp * scale * sample)
    return out


def _bass(freq: float, seconds: float, rate: int) -> list[float]:
    """A plucked saw bass note for the groove."""
    table = _saw_table(freq, rate, 0.35)
    step = freq * TABLE / rate
    total = int(seconds * rate)
    return [table[int(n * step) % TABLE] * min(1.0, n / (0.003 * rate))
            * math.exp(-n / rate * 7.0) * min(1.0, (total - n) / (0.01 * rate))
            for n in range(total)]


def _bell(freq: float, seconds: float, rate: int, *, ratio: float = 3.5,
          index: float = 2.2) -> list[float]:
    """FM bell: a carrier whose modulation index decays faster than its body."""
    out = []
    for n in range(int(seconds * rate)):
        t = n / rate
        mod = index * math.exp(-t * 6.0) * math.sin(TWO_PI * freq * ratio * t)
        out.append(min(1.0, t / 0.004) * math.exp(-t * 3.2) * math.sin(TWO_PI * freq * t + mod))
    return out


def _kick(rate: int, seconds: float = 0.45) -> list[float]:
    """Punchy kick: a sine diving 160 -> 48 Hz, a click, a fast body decay."""
    out, phase = [], 0.0
    for n in range(int(seconds * rate)):
        t = n / rate
        phase += TWO_PI * (48.0 + 112.0 * math.exp(-t * 30.0)) / rate
        body = math.sin(phase) * math.exp(-t * 7.5)
        out.append(math.tanh(1.6 * body + math.exp(-t * 600.0) * 0.6))
    return out


def _noise(seconds: float, rate: int, seed: int) -> list[float]:
    rng = random.Random(seed)
    return [rng.uniform(-1.0, 1.0) for _ in range(int(seconds * rate))]


def _highpass(buffer: list[float], cutoff: float, rate: int) -> list[float]:
    alpha = 1.0 - math.exp(-TWO_PI * cutoff / rate)
    low, out = 0.0, []
    for v in buffer:
        low += alpha * (v - low)
        out.append(v - low)
    return out


def _lowpass(buffer: list[float], cutoff: float, rate: int) -> list[float]:
    alpha = 1.0 - math.exp(-TWO_PI * cutoff / rate)
    low, out = 0.0, []
    for v in buffer:
        low += alpha * (v - low)
        out.append(low)
    return out


def _clap(rate: int, seed: int) -> list[float]:
    """Clap: three quick noise bursts and a tail, band-limited, plus a snare body."""
    noise = _highpass(_lowpass(_noise(0.35, rate, seed), 5000.0, rate), 700.0, rate)
    out = []
    for n, v in enumerate(noise):
        t = n / rate
        bursts = max(math.exp(-((t - at) if t >= at else 1e9) * 140.0)
                     for at in (0.0, 0.011, 0.022))
        env = max(bursts, 0.6 * math.exp(-max(0.0, t - 0.03) * 18.0) if t >= 0.03 else 0.0)
        body = 0.5 * math.sin(TWO_PI * 190.0 * t) * math.exp(-t * 30.0)
        out.append(1.6 * v * env + body)
    return out


def _hat(rate: int, seed: int, *, open_hat: bool = False) -> list[float]:
    noise = _highpass(_noise(0.3 if open_hat else 0.06, rate, seed), 7000.0, rate)
    decay = 9.0 if open_hat else 70.0
    return [v * math.exp(-n / rate * decay) for n, v in enumerate(noise)]


def _crash(rate: int, seed: int, seconds: float = 2.2) -> list[float]:
    """Crash cymbal: bright noise plus a few clangy FM partials, long decay."""
    noise = _highpass(_noise(seconds, rate, seed), 4000.0, rate)
    out = []
    for n, v in enumerate(noise):
        t = n / rate
        clang = sum(math.sin(TWO_PI * f * t + 2.0 * math.sin(TWO_PI * f * 1.41 * t))
                    for f in (3150.0, 4410.0, 5870.0)) / 3.0
        out.append((0.8 * v + 0.25 * clang) * math.exp(-t * 2.4) * min(1.0, t / 0.002))
    return out


def _boom(seconds: float, rate: int) -> list[float]:
    """Cinematic sub hit: a sine sweeping 140 -> 38 Hz with a long tail."""
    out, phase = [], 0.0
    for n in range(int(seconds * rate)):
        t = n / rate
        phase += TWO_PI * (38.0 + 102.0 * math.exp(-t * 14.0)) / rate
        out.append(math.sin(phase) * math.exp(-t * 2.6) * min(1.0, t / 0.002))
    return out


def _riser(seconds: float, rate: int, seed: int) -> list[float]:
    """Build-up: noise opening from dark to bright plus a saw sweeping up two octaves."""
    rng = random.Random(seed)
    table = _saw_table(110.0, rate, 0.5)
    total = int(seconds * rate)
    out, low, phase = [], 0.0, 0.0
    for n in range(total):
        x = n / max(1, total - 1)
        shape = x ** 2.0
        alpha = 1.0 - math.exp(-TWO_PI * (300.0 + 9000.0 * shape) / rate)
        low += alpha * (rng.uniform(-1.0, 1.0) - low)
        phase += (220.0 * 4.0 ** x) * TABLE / rate
        out.append(shape * (0.7 * low + 0.25 * table[int(phase) % TABLE]))
    return out


def _gong(rate: int, seconds: float = 4.5) -> list[float]:
    """A big tam-tam: inharmonic partials whose upper ones swell after the
    strike (the gong's "bloom"), a mallet thump, and a long shimmering decay."""
    fundamental = 68.0
    partials = ((1.0, 1.0, 0.0), (1.47, 0.8, 0.15), (2.09, 0.7, 0.25), (2.56, 0.6, 0.35),
                (3.14, 0.5, 0.45), (3.92, 0.45, 0.6), (4.73, 0.35, 0.7), (5.81, 0.3, 0.8),
                (7.13, 0.25, 0.9))
    out = []
    for n in range(int(seconds * rate)):
        t = n / rate
        sample = 0.0
        for ratio, weight, bloom in partials:
            swell = 1.0 - bloom * math.exp(-t * 3.0)       # upper partials bloom in
            wobble = 1.0 + 0.002 * math.sin(TWO_PI * 4.5 * t * ratio)
            sample += (weight * swell * math.exp(-t * (0.7 + 0.18 * ratio))
                       * math.sin(TWO_PI * fundamental * ratio * wobble * t))
        thump = math.sin(TWO_PI * 55.0 * t) * math.exp(-t * 18.0)
        out.append((sample / 3.0 + thump) * min(1.0, t / 0.003))
    return out


def _normalize(buffer: list[float], peak: float = 0.95) -> list[float]:
    top = max((abs(v) for v in buffer), default=0.0)
    return [v * peak / top for v in buffer] if top > 0 else buffer


def _groove(out: list[float], at_s: float, bars: float, rate: int, *, seed: int,
            bass_notes: tuple[float, ...] = (A1, A1, A2, A1), level: float = 1.0) -> None:
    """Four-on-the-floor: kick every beat, clap on 2 and 4, 16th hats with an
    open hat on the off-beat, and an 8th-note bass line."""
    kick, clap = _kick(rate), _clap(rate, seed)
    hat, open_hat = _hat(rate, seed + 1), _hat(rate, seed + 2, open_hat=True)
    steps = int(bars * 16)
    for step in range(steps):
        t = at_s + step * BEAT / 4
        if step % 4 == 0:
            _add(out, kick, t, rate, 0.9 * level)
        if step % 8 == 4:
            _add(out, clap, t, rate, 0.55 * level)
        if step % 4 == 2:
            _add(out, open_hat, t, rate, 0.16 * level)
        else:
            _add(out, hat, t, rate, (0.12 if step % 2 else 0.2) * level)
        if step % 2 == 0:
            note = bass_notes[(step // 2) % len(bass_notes)]
            _add(out, _bass(note, BEAT / 2 * 0.9, rate), t, rate, 0.45 * level)


def _snare_roll(out: list[float], at_s: float, seconds: float, rate: int, seed: int) -> None:
    """A build: claps accelerating from 8ths to 32nds, getting louder."""
    clap = _clap(rate, seed)
    t = 0.0
    while t < seconds:
        x = t / seconds
        _add(out, clap, at_s + t, rate, 0.12 + 0.35 * x)
        t += BEAT / (2 if x < 0.4 else 4 if x < 0.75 else 8)


# ── The kit ───────────────────────────────────────────────────────────────

def intro(rate: int) -> list[float]:
    """~8 s: a one-bar build (riser + snare roll), then THE HIT (kick, sub boom,
    crash, brass stab in A) with the A-E-A motif on bell + brass, a groove
    the voice enters over at 4.2 s, ducked, ending on a last crash."""
    hit = BAR
    out = _silence(8.0, rate)
    _add(out, _riser(hit, rate, seed=11), 0.0, rate, 0.5)
    _snare_roll(out, BEAT * 2, BAR - BEAT * 2, rate, seed=13)
    _add(out, _kick(rate), hit, rate, 1.0)
    _add(out, _boom(2.4, rate), hit, rate, 0.9)
    _add(out, _crash(rate, seed=17, seconds=2.6), hit, rate, 0.45)
    _add(out, _brass(A_MAJOR, 1.2, rate, decay=3.0), hit, rate, 0.9)
    for at, note in ((0.0, A4), (BEAT / 2, E5), (BEAT, A5)):
        _add(out, _bell(note, 1.6, rate), hit + at, rate, 0.45)
        _add(out, _brass((note / 2,), BEAT * 0.9, rate, decay=4.0), hit + at, rate, 0.35)
    _add(out, _brass(A_MAJOR, BEAT * 1.6, rate, decay=2.0, sustain=0.3), hit + BEAT * 2.5,
         rate, 0.5)
    _groove(out, hit, 2.0, rate, seed=19)
    _add(out, _crash(rate, seed=23, seconds=2.0), hit + 2 * BAR, rate, 0.3)
    _add(out, _kick(rate), hit + 2 * BAR, rate, 0.8)
    return _normalize(out)


def transition(rate: int) -> list[float]:
    """~2.4 s: a reverse-cymbal suck-in, a HIT (kick, crash, D-major brass stab)
    with the motif's E -> A, half a bar of groove; voice back at 1.3 s."""
    hit = 0.45
    out = _silence(2.4, rate)
    swell = _crash(rate, seed=29, seconds=hit)[::-1]
    _add(out, swell, 0.0, rate, 0.5)
    _add(out, _riser(hit, rate, seed=31), 0.0, rate, 0.25)
    _add(out, _kick(rate), hit, rate, 1.0)
    _add(out, _boom(1.0, rate), hit, rate, 0.5)
    _add(out, _clap(rate, seed=37), hit, rate, 0.5)
    _add(out, _crash(rate, seed=41, seconds=1.6), hit, rate, 0.35)
    _add(out, _brass(D_MAJOR, 0.7, rate, decay=4.5), hit, rate, 0.75)
    _add(out, _bell(E5, 1.1, rate, index=1.8), hit, rate, 0.4)
    _add(out, _bell(A5, 1.2, rate, index=1.8), hit + BEAT / 2, rate, 0.45)
    _groove(out, hit + BEAT, 0.5, rate, seed=43, bass_notes=(D3 / 2, D3 / 2, A1, A1),
            level=0.8)
    return _normalize(out)


def gong(rate: int) -> list[float]:
    """~4.5 s: THE gong, for the one huge moment of a bulletin (a mega round,
    an acquisition, an IPO). A short swell into the strike; voice at 1.7 s
    while it rings on, ducked."""
    strike = 0.25
    out = _silence(4.8, rate)
    _add(out, _crash(rate, seed=47, seconds=strike)[::-1], 0.0, rate, 0.3)
    _add(out, _gong(rate), strike, rate, 1.0)
    _add(out, _boom(1.6, rate), strike, rate, 0.4)
    return _normalize(out)


def outro(rate: int) -> list[float]:
    """~6 s: a bar of groove under the motif descending in brass and bell,
    then the final HIT (kick, boom, crash, A-major brass) ringing out."""
    out = _silence(6.2, rate)
    _groove(out, 0.0, 1.0, rate, seed=53, level=0.85)
    for at, note in ((0.0, A5), (BEAT / 2, E5), (BEAT, A4)):
        _add(out, _bell(note, 1.6, rate), at, rate, 0.45)
        _add(out, _brass((note / 2,), BEAT * 0.9, rate, decay=4.0), at, rate, 0.35)
    _snare_roll(out, BEAT * 2, BEAT * 2, rate, seed=59)
    final = BAR
    _add(out, _kick(rate), final, rate, 1.0)
    _add(out, _boom(2.6, rate), final, rate, 0.9)
    _add(out, _crash(rate, seed=61, seconds=3.0), final, rate, 0.5)
    _add(out, _brass(A_MAJOR + (A4,), 3.0, rate, decay=1.2), final, rate, 0.9)
    _add(out, _bell(CS6, 2.4, rate, index=1.2), final, rate, 0.25)
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


def mix(segments: list[Pcm], cues: list[str] | None = None) -> Mix:
    """intro, voice segments joined by cue sounds, outro; music ducked under voice.

    `cues[i]` is the sound between segment i and i + 1 ("transition" or
    "gong"); it defaults to transitions.
    """
    if not segments:
        raise SoundError("no voice segments to mix")
    cues = list(cues) if cues is not None else ["transition"] * (len(segments) - 1)
    if len(cues) != len(segments) - 1 or any(cue not in CUES for cue in cues):
        raise SoundError(f"cues {cues!r} do not fit {len(segments)} segments")
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
    kit_outro = outro(rate)
    between = {cue: (make(rate), voice_at) for cue, make, voice_at in (
        ("transition", transition, TRANSITION_VOICE_AT_S), ("gong", gong, GONG_VOICE_AT_S))
        if cue in cues}
    sounds.append((0, intro(rate)))
    cursor = int(INTRO_VOICE_AT_S * rate)
    for index, segment in enumerate(segments):
        if index:
            buffer, voice_at = between[cues[index - 1]]
            cursor += int(SEGMENT_GAP_S * rate)
            sounds.append((cursor, buffer))
            cursor += int(voice_at * rate)
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
    parser.add_argument("--gong", action="store_true",
                        help="make the first cue a gong instead of a transition")
    args = parser.parse_args(argv)
    # A quiet 200 Hz hum stands in for speech, so the ducking is audible.
    tone = array("h", (int(3000 * math.sin(2 * math.pi * 200 * n / args.rate))
                       for n in range(int(args.segment_seconds * args.rate))))
    count = max(1, args.segments)
    cues = ["transition"] * (count - 1)
    if args.gong and cues:
        cues[0] = "gong"
    result = mix([Pcm(tone, args.rate) for _ in range(count)], cues)
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
