import React from "react";
import { COLOR } from "../theme";
import { SANS } from "../fonts";

/** A labeled source pill (Twitter / X, arXiv, …). */
export const SourceChip: React.FC<{
  label: string;
  onDark?: boolean;
  scale?: number;
}> = ({ label, onDark = false, scale = 1 }) => (
  <div
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 10 * scale,
      padding: `${11 * scale}px ${20 * scale}px`,
      borderRadius: 999,
      background: onDark ? "rgba(255,255,255,0.06)" : COLOR.white,
      border: `1.5px solid ${onDark ? "rgba(127,179,255,0.35)" : COLOR.rule}`,
      boxShadow: onDark ? "none" : "0 2px 10px rgba(5,28,44,0.05)",
      fontFamily: SANS,
      fontWeight: 600,
      fontSize: 26 * scale,
      color: onDark ? COLOR.white : COLOR.ink,
      whiteSpace: "nowrap",
    }}
  >
    <span
      style={{
        width: 9 * scale,
        height: 9 * scale,
        borderRadius: 999,
        background: COLOR.royal,
        boxShadow: `0 0 ${10 * scale}px ${COLOR.royal}`,
      }}
    />
    {label}
  </div>
);
