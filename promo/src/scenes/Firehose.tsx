import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { COLOR, SOURCES } from "../theme";
import { SANS, SERIF, MONO } from "../fonts";
import { Kicker } from "../components/Kicker";
import { SourceChip } from "../components/SourceChip";
import { enterSpring, fadeIn } from "../anim";
import { HEADLINES } from "../data";

const ROW_H = 88;

const TickerPanel: React.FC<{ frame: number; height: number }> = ({ frame, height }) => {
  const items = [...HEADLINES, ...HEADLINES];
  const loopH = HEADLINES.length * ROW_H;
  const y = -((frame * 1.5) % loopH);
  return (
    <div
      style={{
        position: "relative",
        height,
        width: "100%",
        overflow: "hidden",
        borderLeft: `2px solid ${COLOR.rule}`,
        WebkitMaskImage:
          "linear-gradient(to bottom, transparent, #000 12%, #000 86%, transparent)",
        maskImage:
          "linear-gradient(to bottom, transparent, #000 12%, #000 86%, transparent)",
      }}
    >
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, transform: `translateY(${y}px)` }}>
        {items.map((it, i) => (
          <div
            key={i}
            style={{
              height: ROW_H,
              display: "flex",
              alignItems: "center",
              gap: 18,
              padding: "0 8px 0 28px",
              borderBottom: `1px solid ${COLOR.rule}`,
            }}
          >
            <span style={{ fontFamily: MONO, fontSize: 19, color: COLOR.sec3, width: 64, flex: "0 0 auto" }}>
              {it.t}
            </span>
            <span
              style={{
                fontFamily: MONO,
                fontSize: 16,
                fontWeight: 500,
                color: COLOR.royal,
                background: COLOR.periwinkle,
                padding: "5px 11px",
                borderRadius: 6,
                width: 96,
                textAlign: "center",
                flex: "0 0 auto",
                letterSpacing: "0.04em",
              }}
            >
              {it.src}
            </span>
            <span
              style={{
                fontFamily: SANS,
                fontSize: 25,
                color: COLOR.ink,
                fontWeight: 500,
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
              }}
            >
              {it.h}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export const Firehose: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const portrait = height > width;
  const pad = Math.round(width * 0.065);

  const count = Math.round(
    interpolate(frame, [8, 92], [126, 1287], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }),
  );
  const introO = fadeIn(frame, 0, 16);
  const introY = interpolate(enterSpring(frame, fps, 2), [0, 1], [28, 0]);

  return (
    <AbsoluteFill style={{ background: COLOR.paper }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: portrait ? "column" : "row",
          alignItems: "center",
          gap: portrait ? 36 : pad * 0.7,
          padding: pad,
        }}
      >
        <div
          style={{
            flex: portrait ? "0 0 auto" : "1 1 0",
            opacity: introO,
            transform: `translateY(${introY}px)`,
          }}
        >
          <Kicker center={false}>Signal, not noise</Kicker>
          <h1
            style={{
              fontFamily: SERIF,
              fontWeight: 700,
              fontSize: Math.min(width * 0.05, 98),
              lineHeight: 1.02,
              color: COLOR.ink,
              margin: "22px 0 0",
              letterSpacing: "-0.02em",
            }}
          >
            Everything in AI.
            <br />
            As it happens.
          </h1>
          <div style={{ display: "flex", alignItems: "baseline", gap: 16, marginTop: 34 }}>
            <span
              style={{
                fontFamily: SERIF,
                fontWeight: 700,
                fontSize: Math.min(width * 0.058, 112),
                color: COLOR.royal,
                lineHeight: 1,
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {count.toLocaleString()}
            </span>
            <span style={{ fontFamily: SANS, fontSize: 27, color: COLOR.sec, fontWeight: 500 }}>
              signals scanned today
            </span>
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 14, marginTop: 36, maxWidth: 640 }}>
            {SOURCES.map((src, i) => {
              const sp = enterSpring(frame, fps, 38 + i * 5);
              return (
                <div
                  key={src}
                  style={{ opacity: sp, transform: `translateY(${(1 - sp) * 14}px)` }}
                >
                  <SourceChip label={src} />
                </div>
              );
            })}
          </div>
        </div>

        <div
          style={{
            flex: "1 1 0",
            width: "100%",
            height: portrait ? "46%" : "84%",
            display: "flex",
            alignItems: "center",
          }}
        >
          <TickerPanel frame={frame} height={portrait ? height * 0.42 : height * 0.74} />
        </div>
      </div>
    </AbsoluteFill>
  );
};
