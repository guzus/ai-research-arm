import { Easing, interpolate, spring } from "remotion";

/** Symmetric fade at the head and tail of a clip. */
export const fadeEdges = (
  frame: number,
  durationInFrames: number,
  fade = 12,
): number =>
  interpolate(
    frame,
    [0, fade, durationInFrames - fade, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

/** Fade-in only (for elements that persist to the cut). */
export const fadeIn = (frame: number, start = 0, len = 14): number =>
  interpolate(frame, [start, start + len], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

/** A snappy-but-soft spring used for entrances. */
export const enterSpring = (frame: number, fps: number, delay = 0): number =>
  spring({
    frame: frame - delay,
    fps,
    config: { damping: 200, mass: 0.7, stiffness: 110 },
  });

/** Eased 0→1 ramp over [start, start+len]. */
export const ramp = (
  frame: number,
  start: number,
  len: number,
  easing = Easing.out(Easing.cubic),
): number =>
  interpolate(frame, [start, start + len], [0, 1], {
    easing,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
