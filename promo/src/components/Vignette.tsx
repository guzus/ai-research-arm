import React from "react";
import { AbsoluteFill } from "remotion";

/** Soft radial darkening for navy scenes — adds depth without banding. */
export const Vignette: React.FC<{ strength?: number; cx?: number; cy?: number }> = ({
  strength = 0.45,
  cx = 50,
  cy = 42,
}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(130% 130% at ${cx}% ${cy}%, transparent 38%, rgba(0,0,0,${strength}) 100%)`,
      pointerEvents: "none",
    }}
  />
);
