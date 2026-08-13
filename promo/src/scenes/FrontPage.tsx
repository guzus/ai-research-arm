import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { COLOR } from "../theme";
import { EDITIONS } from "../frontpages";
import { SANS, SERIF, MONO } from "../fonts";
import { fadeIn, ramp } from "../anim";

/** Horizontal "press run" of real AGI Awareness Post editions. Holds on the
 *  latest edition, then scrolls the back-catalogue past camera with a subtle
 *  coverflow scale so the centred paper is always the hero. */
export const FrontPage: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();

  const cardH = height * 0.72;
  const cardW = cardH * 0.772; // newspaper portrait ratio
  const gap = Math.round(width * 0.035);
  const step = cardW + gap;

  // Hold the newest edition centred, then scroll the rest past.
  const progress = ramp(frame, 30, durationInFrames - 80, Easing.inOut(Easing.cubic));
  const startX = width / 2 - cardW / 2;
  const translateX = startX - progress * (EDITIONS.length - 1) * step;

  const captionSwap = interpolate(frame, [88, 104], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${COLOR.paper}, ${COLOR.paper2})` }}>
      {/* top hairline + kicker, like a masthead rule */}
      <div
        style={{
          position: "absolute",
          top: height * 0.085,
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 14,
          opacity: fadeIn(frame, 4, 16),
          zIndex: 5,
        }}
      >
        <div style={{ fontFamily: MONO, fontSize: 20, letterSpacing: "0.34em", color: COLOR.royal, textTransform: "uppercase" }}>
          The AGI Awareness Post
        </div>
        <div style={{ width: Math.min(width * 0.4, 760), height: 2, background: COLOR.ink, opacity: 0.85 }} />
      </div>

      {/* filmstrip */}
      <AbsoluteFill style={{ alignItems: "center" }}>
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: 0,
            display: "flex",
            gap,
            transform: `translateY(-46%) translateX(${translateX}px)`,
          }}
        >
          {EDITIONS.map((d, i) => {
            const cardCenter = i * step + cardW / 2 + translateX;
            const dist = Math.abs(cardCenter - width / 2);
            const prox = interpolate(dist, [0, width * 0.5], [1, 0], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            const scale = 0.84 + prox * 0.16;
            const lift = prox * 26;
            return (
              <div
                key={d}
                style={{
                  width: cardW,
                  height: cardH,
                  flex: "0 0 auto",
                  transform: `scale(${scale}) translateY(${-lift}px)`,
                  borderRadius: 8,
                  overflow: "hidden",
                  background: COLOR.white,
                  boxShadow: `0 ${30 + prox * 40}px ${70 + prox * 60}px rgba(5,28,44,${0.16 + prox * 0.16})`,
                  border: `1px solid ${COLOR.rule}`,
                }}
              >
                <Img
                  src={staticFile(`frontpages/${d}.png`)}
                  style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "center top" }}
                />
              </div>
            );
          })}
        </div>
      </AbsoluteFill>

      {/* bottom caption (cross-faded) */}
      <div
        style={{
          position: "absolute",
          bottom: height * 0.07,
          left: 0,
          right: 0,
          textAlign: "center",
          zIndex: 5,
        }}
      >
        <div style={{ position: "relative", height: 64 }}>
          <Caption show={1 - captionSwap} text="A new edition. Every morning." accent="Every morning." />
          <Caption show={captionSwap} text="365 mornings a year — written by no one." accent="written by no one." />
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Caption: React.FC<{ show: number; text: string; accent: string }> = ({ show, text, accent }) => {
  const [pre, post] = text.split(accent);
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        opacity: show,
        transform: `translateY(${(1 - show) * 10}px)`,
        fontFamily: SERIF,
        fontStyle: "italic",
        fontSize: 40,
        color: COLOR.ink,
      }}
    >
      <span style={{ fontFamily: SANS, fontStyle: "normal", fontWeight: 500 }}>{pre}</span>
      <span style={{ color: COLOR.royal, fontWeight: 600 }}>{accent}</span>
      {post}
    </div>
  );
};
