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
import { COLOR, PILLARS, SITE_URL } from "../theme";
import { SANS, SERIF, MONO } from "../fonts";
import { Kicker } from "../components/Kicker";
import { BrowserFrame } from "../components/BrowserFrame";
import { fadeIn } from "../anim";
import { SCREENS, hasScreen } from "../screens";

const TABS = ["Today", "Twitter", "Model Timeline", "Research", "Wiki"];

/** Maps a pillar to the capture key in public/screens (see scripts/gen-screens). */
const SHOT_KEY: Record<string, string> = {
  Today: "today",
  "Model Timeline": "models",
  Wiki: "wiki",
  Research: "research",
};

/** Auto-scrolling full-page screenshot — the "screen recording" effect. */
const ScrollingShot: React.FC<{ k: string; w: number; h: number; t: number; seg: number }> = ({
  k,
  w,
  h,
  t,
  seg,
}) => {
  const shot = SCREENS[k];
  const scale = w / shot.w;
  const scaledH = shot.h * scale;
  // Cap the pan so very tall pages (the model board, the digest) scroll at a
  // readable rate rather than racing to the bottom in one segment.
  const overscroll = Math.min(Math.max(0, scaledH - h), h * 1.5);
  const p = interpolate(t, [6, seg - 6], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.quad),
  });
  return (
    <Img
      src={staticFile(shot.src)}
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: w,
        transform: `translateY(${-p * overscroll}px)`,
      }}
    />
  );
};

const MockRow: React.FC<{ a: string; b: string; chip?: string }> = ({ a, b, chip }) => (
  <div
    style={{
      display: "flex",
      alignItems: "center",
      gap: 18,
      padding: "22px 4px",
      borderBottom: `1px solid ${COLOR.rule}`,
    }}
  >
    <span style={{ width: 9, height: 9, borderRadius: 999, background: COLOR.royal, flex: "0 0 auto" }} />
    <div style={{ flex: 1, minWidth: 0 }}>
      <div style={{ fontFamily: SERIF, fontWeight: 600, fontSize: 27, color: COLOR.ink, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
        {a}
      </div>
      <div style={{ fontFamily: SANS, fontSize: 18, color: COLOR.sec, marginTop: 3 }}>{b}</div>
    </div>
    {chip && (
      <span
        style={{
          fontFamily: MONO,
          fontSize: 15,
          color: COLOR.royal,
          background: COLOR.periwinkle,
          padding: "6px 12px",
          borderRadius: 6,
          flex: "0 0 auto",
          textTransform: "uppercase",
          letterSpacing: "0.05em",
        }}
      >
        {chip}
      </span>
    )}
  </div>
);

const MOCK: Record<string, { title: string; rows: { a: string; b: string; chip?: string }[] }> = {
  Today: {
    title: "Daily AI Digest",
    rows: [
      { a: "Frontier lab ships a 2M-token context window", b: "Models & Systems · 4 sources", chip: "new" },
      { a: "Open-weights release matches frontier reasoning", b: "Research Ledger · 7 sources", chip: "hot" },
      { a: "Inference cost falls 11× on new accelerator", b: "Capital & Compute · 3 sources" },
      { a: "Regulator opens inquiry into training data", b: "Policy Watch · 5 sources" },
    ],
  },
  "Model Timeline": {
    title: "Model Timeline",
    rows: [
      { a: "Fable 5 — flagship", b: "updated 2h ago", chip: "released" },
      { a: "Mythos 5 — reasoning", b: "updated today", chip: "confirmed" },
      { a: "Next-gen open weights", b: "updated yesterday", chip: "in-testing" },
      { a: "Fall flagship", b: "rumor · 2 sources", chip: "rumored" },
    ],
  },
  Wiki: {
    title: "LLM Wiki",
    rows: [
      { a: "Mixture-of-Experts", b: "concept · 12 backlinks", chip: "concept" },
      { a: "Test-time compute", b: "concept · 9 backlinks", chip: "concept" },
      { a: "Anthropic", b: "entity · 21 backlinks", chip: "entity" },
      { a: "The scaling debate", b: "theme · ongoing", chip: "theme" },
    ],
  },
  Research: {
    title: "Generative Research",
    rows: [
      { a: "The export-control saga, in five charts", b: "12 min · 38 citations", chip: "essay" },
      { a: "What 'test-time compute' actually buys you", b: "9 min · 27 citations", chip: "deep-dive" },
      { a: "The economics of open weights", b: "11 min · 31 citations", chip: "essay" },
    ],
  },
};

/** Faithful-enough mock of a dashboard page; used when a capture is missing. */
const MockPage: React.FC<{ tab: string }> = ({ tab }) => {
  const data = MOCK[tab] ?? MOCK.Today;
  return (
    <div style={{ position: "absolute", inset: 0, background: COLOR.white, display: "flex", flexDirection: "column" }}>
      {/* app header */}
      <div style={{ padding: "26px 40px 0" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div style={{ fontFamily: MONO, fontSize: 22, fontWeight: 600, color: COLOR.ink, letterSpacing: "-0.01em" }}>
            ai-research-arm
          </div>
          <div style={{ fontFamily: MONO, fontSize: 16, color: COLOR.sec3 }}>guzus/ai-research-arm</div>
        </div>
        {/* tabs */}
        <div style={{ display: "flex", gap: 28, marginTop: 24, borderBottom: `1px solid ${COLOR.rule}` }}>
          {TABS.map((t) => {
            const active = t === tab;
            return (
              <div
                key={t}
                style={{
                  fontFamily: SANS,
                  fontSize: 21,
                  fontWeight: active ? 600 : 500,
                  color: active ? COLOR.ink : COLOR.sec3,
                  paddingBottom: 14,
                  borderBottom: `3px solid ${active ? COLOR.royal : "transparent"}`,
                }}
              >
                {t}
              </div>
            );
          })}
        </div>
      </div>
      {/* content */}
      <div style={{ padding: "30px 40px", flex: 1 }}>
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 40, color: COLOR.ink, marginBottom: 8 }}>
          {data.title}
        </div>
        <div style={{ fontFamily: MONO, fontSize: 16, color: COLOR.sec, marginBottom: 18, textTransform: "uppercase", letterSpacing: "0.12em" }}>
          {SITE_URL}
        </div>
        {data.rows.map((r) => (
          <MockRow key={r.a} {...r} />
        ))}
      </div>
    </div>
  );
};

export const Product: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();
  const portrait = height > width;

  const segLen = durationInFrames / PILLARS.length;
  const idx = Math.min(PILLARS.length - 1, Math.floor(frame / segLen));
  const tIn = frame - idx * segLen;
  const pillar = PILLARS[idx];
  const swap = fadeIn(tIn, 0, 12);

  const frameW = portrait ? width * 0.86 : width * 0.585;
  const frameH = portrait ? height * 0.52 : height * 0.8;

  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${COLOR.paper}, ${COLOR.paper2})` }}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: portrait ? "column" : "row",
          alignItems: "center",
          justifyContent: "center",
          gap: portrait ? 34 : width * 0.05,
          padding: width * 0.05,
        }}
      >
        {/* caption column */}
        <div style={{ flex: portrait ? "0 0 auto" : "0 0 30%", maxWidth: portrait ? "100%" : 460 }}>
          <div style={{ opacity: fadeIn(frame, 0, 14) }}>
            <Kicker center={false}>Inside the dashboard</Kicker>
          </div>
          <div style={{ opacity: swap, transform: `translateY(${(1 - swap) * 14}px)` }}>
            <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: Math.min(width * 0.04, 76), color: COLOR.ink, marginTop: 22, lineHeight: 1.04, letterSpacing: "-0.02em" }}>
              {pillar.title}
            </div>
            <div style={{ fontFamily: SANS, fontSize: Math.min(width * 0.019, 32), color: COLOR.sec, marginTop: 18, lineHeight: 1.4, maxWidth: 460 }}>
              {pillar.blurb}
            </div>
          </div>
          {/* tab progress dots */}
          <div style={{ display: "flex", gap: 10, marginTop: 34 }}>
            {PILLARS.map((p, i) => (
              <div
                key={p.title}
                style={{
                  height: 6,
                  width: i === idx ? 44 : 20,
                  borderRadius: 999,
                  background: i === idx ? COLOR.royal : COLOR.rule,
                  transition: "all 0.2s",
                }}
              />
            ))}
          </div>
        </div>

        {/* browser frame */}
        <div style={{ flex: "0 0 auto", opacity: fadeIn(frame, 6, 16) }}>
          <BrowserFrame width={frameW} height={frameH}>
            <div style={{ position: "absolute", inset: 0, opacity: swap }}>
              {hasScreen(SHOT_KEY[pillar.tab] ?? "") ? (
                <ScrollingShot
                  k={SHOT_KEY[pillar.tab]}
                  w={frameW}
                  h={frameH - 52}
                  t={tIn}
                  seg={segLen}
                />
              ) : (
                <MockPage tab={pillar.tab} />
              )}
            </div>
          </BrowserFrame>
        </div>
      </div>
    </AbsoluteFill>
  );
};
