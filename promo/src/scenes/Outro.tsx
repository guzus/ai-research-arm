import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { COLOR, SOURCES, SITE_URL } from "../theme";
import { SANS, MONO } from "../fonts";
import { Wordmark } from "../components/Wordmark";
import { Vignette } from "../components/Vignette";
import { enterSpring, fadeIn } from "../anim";

export const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const wmO = fadeIn(frame, 2, 14);
  const wmScale = interpolate(enterSpring(frame, fps, 2), [0, 1], [0.9, 1]);
  const urlO = fadeIn(frame, 18, 16);
  const urlY = interpolate(enterSpring(frame, fps, 18), [0, 1], [18, 0]);
  const tagO = fadeIn(frame, 32, 16);
  const footO = fadeIn(frame, 48, 20);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 120% at 50% 36%, ${COLOR.navy3}, ${COLOR.navy} 60%)`,
      }}
    >
      <Vignette strength={0.5} />
      {/* glow behind url */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <div
          style={{
            position: "absolute",
            width: width * 0.5,
            height: width * 0.5,
            borderRadius: "50%",
            background: `radial-gradient(circle, rgba(34,81,255,0.22), transparent 65%)`,
            top: "42%",
            transform: "translateY(-50%)",
          }}
        />
      </AbsoluteFill>

      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "column" }}>
        <div style={{ opacity: wmO, transform: `scale(${wmScale})` }}>
          <Wordmark size={Math.min(width * 0.058, 108)} onDark underline={1} />
        </div>

        <div style={{ opacity: urlO, transform: `translateY(${urlY}px)`, marginTop: height * 0.07, textAlign: "center" }}>
          <div
            style={{
              fontFamily: SANS,
              fontWeight: 700,
              fontSize: Math.min(width * 0.04, 74),
              color: COLOR.white,
              letterSpacing: "-0.01em",
            }}
          >
            {SITE_URL}
          </div>
          <div
            style={{
              height: 5,
              width: "100%",
              marginTop: 12,
              borderRadius: 999,
              background: `linear-gradient(90deg, ${COLOR.royal}, ${COLOR.cyan})`,
            }}
          />
        </div>

        <div
          style={{
            opacity: tagO,
            marginTop: height * 0.05,
            fontFamily: SANS,
            fontSize: Math.min(width * 0.02, 34),
            color: COLOR.sky,
            fontWeight: 400,
          }}
        >
          Automated AI-news intelligence —{" "}
          <span style={{ color: COLOR.white, fontWeight: 600 }}>updated daily.</span>
        </div>

        <div
          style={{
            opacity: footO,
            position: "absolute",
            bottom: height * 0.07,
            fontFamily: MONO,
            fontSize: Math.min(width * 0.0115, 20),
            color: COLOR.sec3,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
          }}
        >
          {SOURCES.join("  ·  ")}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
