import React from "react";
import { COLOR } from "../theme";
import { SERIF, MONO } from "../fonts";

/** The ara brand lockup: a telescope badge + the serif wordmark. */
export const Wordmark: React.FC<{
  size?: number;
  onDark?: boolean;
  underline?: number; // 0..1 reveal of the royal underline
}> = ({ size = 150, onDark = true, underline = 1 }) => {
  const ink = onDark ? COLOR.white : COLOR.ink;
  const badge = size * 0.62;
  return (
    <div style={{ display: "flex", alignItems: "center", gap: size * 0.22 }}>
      <div
        style={{
          width: badge,
          height: badge,
          borderRadius: badge * 0.26,
          background: `linear-gradient(150deg, ${COLOR.royal}, ${COLOR.navy})`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: badge * 0.56,
          boxShadow: `0 12px 40px ${onDark ? "rgba(34,81,255,0.4)" : "rgba(5,28,44,0.22)"}`,
        }}
      >
        🔭
      </div>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <div
          style={{
            position: "relative",
            fontFamily: SERIF,
            fontWeight: 700,
            fontSize: size,
            lineHeight: 0.9,
            color: ink,
            letterSpacing: "-0.02em",
          }}
        >
          ara
          <div
            style={{
              position: "absolute",
              left: 2,
              bottom: -size * 0.06,
              height: size * 0.07,
              width: `${underline * 100}%`,
              background: COLOR.royal,
              borderRadius: 4,
            }}
          />
        </div>
        <div
          style={{
            fontFamily: MONO,
            fontSize: size * 0.115,
            letterSpacing: "0.34em",
            textTransform: "uppercase",
            color: onDark ? COLOR.sky : COLOR.sec,
            marginTop: size * 0.14,
            paddingLeft: 3,
          }}
        >
          AI&nbsp;research&nbsp;arm
        </div>
      </div>
    </div>
  );
};
