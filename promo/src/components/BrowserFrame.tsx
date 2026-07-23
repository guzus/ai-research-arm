import React from "react";
import { COLOR } from "../theme";
import { MONO } from "../fonts";
import { SITE_URL } from "../theme";

const Dot: React.FC<{ c: string }> = ({ c }) => (
  <span style={{ width: 13, height: 13, borderRadius: 999, background: c }} />
);

/** A macOS-style browser chrome wrapper, used to frame dashboard captures. */
export const BrowserFrame: React.FC<{
  width: number;
  height: number;
  url?: string;
  radius?: number;
  children: React.ReactNode;
}> = ({ width, height, url = SITE_URL, radius = 20, children }) => (
  <div
    style={{
      width,
      height,
      borderRadius: radius,
      overflow: "hidden",
      background: COLOR.white,
      border: `1px solid ${COLOR.rule}`,
      boxShadow:
        "0 50px 140px rgba(5,28,44,0.30), 0 14px 40px rgba(5,28,44,0.14)",
      display: "flex",
      flexDirection: "column",
    }}
  >
    <div
      style={{
        height: 52,
        flex: "0 0 auto",
        background: "#f3f3ef",
        borderBottom: `1px solid ${COLOR.rule}`,
        display: "flex",
        alignItems: "center",
        padding: "0 20px",
        gap: 9,
      }}
    >
      <Dot c="#ff5f57" />
      <Dot c="#febc2e" />
      <Dot c="#28c840" />
      <div
        style={{
          marginLeft: 18,
          flex: 1,
          maxWidth: 460,
          height: 32,
          borderRadius: 16,
          background: COLOR.white,
          border: `1px solid ${COLOR.rule}`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 8,
          fontFamily: MONO,
          fontSize: 16,
          color: COLOR.sec,
        }}
      >
        <span style={{ color: COLOR.royal }}>🔒</span>
        {url}
      </div>
    </div>
    <div style={{ flex: 1, position: "relative", overflow: "hidden" }}>
      {children}
    </div>
  </div>
);
