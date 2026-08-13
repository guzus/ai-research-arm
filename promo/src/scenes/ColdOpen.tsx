import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { COLOR, SOURCES } from "../theme";
import { SANS, SERIF } from "../fonts";
import { Wordmark } from "../components/Wordmark";
import { Vignette } from "../components/Vignette";
import { enterSpring, fadeIn, ramp } from "../anim";

const BackgroundWords: React.FC<{ frame: number; width: number; height: number }> = ({
  frame,
  width,
  height,
}) => {
  const rows = 7;
  const words = [...SOURCES, ...SOURCES, ...SOURCES];
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {Array.from({ length: rows }).map((_, r) => {
        const dir = r % 2 === 0 ? -1 : 1;
        const speed = 0.4 + (r % 3) * 0.14;
        const x = ((frame * speed * dir) % 700) - 100;
        return (
          <div
            key={r}
            style={{
              position: "absolute",
              top: (r + 0.5) * (height / rows),
              left: 0,
              right: 0,
              transform: `translateY(-50%) translateX(${x}px)`,
              whiteSpace: "nowrap",
              display: "flex",
              gap: 64,
              opacity: 0.055,
              fontFamily: SERIF,
              fontSize: width * 0.05,
              color: COLOR.white,
              fontWeight: 600,
            }}
          >
            {words.map((w, i) => (
              <span key={i}>{w}</span>
            ))}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

export const ColdOpen: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const s = enterSpring(frame, fps, 6);
  const wmScale = interpolate(s, [0, 1], [0.84, 1]);
  const wmOpacity = fadeIn(frame, 4, 16);
  const underline = ramp(frame, 28, 24);
  const tagOpacity = fadeIn(frame, 38, 18);
  const tagY = interpolate(enterSpring(frame, fps, 38), [0, 1], [24, 0]);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 120% at 50% 28%, ${COLOR.navy3}, ${COLOR.navy} 58%)`,
      }}
    >
      <BackgroundWords frame={frame} width={width} height={height} />
      <Vignette strength={0.5} />
      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
        }}
      >
        <div style={{ transform: `scale(${wmScale})`, opacity: wmOpacity }}>
          <Wordmark size={Math.min(width * 0.085, 156)} onDark underline={underline} />
        </div>
        <div
          style={{
            opacity: tagOpacity,
            transform: `translateY(${tagY}px)`,
            marginTop: height * 0.06,
            fontFamily: SANS,
            fontSize: Math.min(width * 0.022, 40),
            color: COLOR.sky,
            fontWeight: 400,
            letterSpacing: "0.01em",
          }}
        >
          AI research,{" "}
          <span style={{ color: COLOR.white, fontWeight: 600 }}>on autopilot.</span>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
