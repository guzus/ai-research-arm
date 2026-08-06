import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { COLOR } from "../theme";
import { SANS, SERIF, MONO } from "../fonts";
import { Kicker } from "../components/Kicker";
import { Vignette } from "../components/Vignette";
import { enterSpring, fadeIn } from "../anim";

const NODES = [
  { n: "01", title: "Aggregate", sub: "6 sources · hourly" },
  { n: "02", title: "Synthesize", sub: "digest · timeline · wiki" },
  { n: "03", title: "Generate", sub: "long-form research" },
  { n: "04", title: "Publish", sub: "ara.guzus.xyz" },
];

const Node: React.FC<{
  node: (typeof NODES)[number];
  on: number;
  size: number;
}> = ({ node, on, size }) => (
  <div
    style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 18,
      opacity: on,
      transform: `translateY(${(1 - on) * 22}px)`,
      zIndex: 2,
    }}
  >
    <div
      style={{
        width: size,
        height: size,
        borderRadius: "50%",
        background: `linear-gradient(150deg, ${COLOR.navy3}, ${COLOR.navy})`,
        border: `2px solid ${COLOR.royal}`,
        boxShadow: `0 0 ${36 * on}px rgba(34,81,255,${0.5 * on})`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: MONO,
        fontSize: size * 0.3,
        fontWeight: 500,
        color: COLOR.sky,
      }}
    >
      {node.n}
    </div>
    <div style={{ textAlign: "center" }}>
      <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 38, color: COLOR.white }}>
        {node.title}
      </div>
      <div style={{ fontFamily: MONO, fontSize: 18, color: COLOR.sky, marginTop: 6, letterSpacing: "0.02em" }}>
        {node.sub}
      </div>
    </div>
  </div>
);

export const Pipeline: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const portrait = height > width;
  const nodeSize = Math.min(width * 0.075, 132);

  // Connector fill + traveling pulse (after nodes settle).
  const fill = interpolate(frame, [16, 78], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const pulse = ((frame - 60) / 46) % 1;
  const showPulse = frame > 62;

  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${COLOR.navy2}, ${COLOR.navy})` }}>
      <Vignette strength={0.4} cy={48} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "column", padding: width * 0.06 }}>
        <div style={{ opacity: fadeIn(frame, 0, 14), marginBottom: height * 0.07 }}>
          <Kicker color={COLOR.cyan}>The pipeline</Kicker>
        </div>

        <div
          style={{
            position: "relative",
            width: portrait ? "auto" : "100%",
            maxWidth: 1500,
            display: "flex",
            flexDirection: portrait ? "column" : "row",
            alignItems: "center",
            justifyContent: "space-between",
            gap: portrait ? 46 : 0,
          }}
        >
          {/* baseline track */}
          {!portrait && (
            <>
              <div
                style={{
                  position: "absolute",
                  top: nodeSize / 2,
                  left: "8%",
                  right: "8%",
                  height: 3,
                  background: COLOR.navy3,
                  transform: "translateY(-50%)",
                  zIndex: 0,
                }}
              />
              <div
                style={{
                  position: "absolute",
                  top: nodeSize / 2,
                  left: "8%",
                  width: `${fill * 84}%`,
                  height: 3,
                  background: `linear-gradient(90deg, ${COLOR.royal}, ${COLOR.cyan})`,
                  transform: "translateY(-50%)",
                  zIndex: 1,
                  boxShadow: `0 0 14px ${COLOR.cyan}`,
                }}
              />
              {showPulse && (
                <div
                  style={{
                    position: "absolute",
                    top: nodeSize / 2,
                    left: `${8 + pulse * 84}%`,
                    width: 16,
                    height: 16,
                    borderRadius: "50%",
                    background: COLOR.cyan,
                    transform: "translate(-50%, -50%)",
                    boxShadow: `0 0 24px ${COLOR.cyan}`,
                    zIndex: 3,
                  }}
                />
              )}
            </>
          )}

          {NODES.map((node, i) => (
            <Node key={node.n} node={node} size={nodeSize} on={enterSpring(frame, fps, 10 + i * 14)} />
          ))}
        </div>

        <div
          style={{
            marginTop: height * 0.09,
            opacity: fadeIn(frame, 70, 18),
            fontFamily: SANS,
            fontSize: Math.min(width * 0.02, 36),
            color: COLOR.white,
            fontWeight: 400,
            textAlign: "center",
          }}
        >
          Aggregate. Synthesize. Publish.{" "}
          <span style={{ color: COLOR.cyan, fontWeight: 600 }}>No human in the loop.</span>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
