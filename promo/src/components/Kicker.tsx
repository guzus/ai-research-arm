import React from "react";
import { COLOR } from "../theme";
import { MONO } from "../fonts";

/** Mono eyebrow label, flanked by short rules. The house "kicker". */
export const Kicker: React.FC<{
  children: React.ReactNode;
  color?: string;
  size?: number;
  center?: boolean;
}> = ({ children, color = COLOR.royal, size = 21, center = true }) => (
  <div
    style={{
      display: "flex",
      alignItems: "center",
      gap: 14,
      justifyContent: center ? "center" : "flex-start",
    }}
  >
    <span style={{ width: 26, height: 2, background: color, opacity: 0.85 }} />
    <span
      style={{
        fontFamily: MONO,
        fontSize: size,
        letterSpacing: "0.3em",
        textTransform: "uppercase",
        color,
        fontWeight: 500,
        paddingLeft: "0.3em",
      }}
    >
      {children}
    </span>
    {center && (
      <span style={{ width: 26, height: 2, background: color, opacity: 0.85 }} />
    )}
  </div>
);
