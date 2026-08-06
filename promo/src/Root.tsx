import React from "react";
import { Composition } from "remotion";
import { Promo, PROMO_DURATION } from "./Promo";

/**
 * Three deliverables share one timeline:
 *  - Promo          16:9  landing hero / YouTube / X
 *  - PromoSquare    1:1   feed posts
 *  - PromoVertical  9:16  Shorts / Reels / TikTok
 * Scenes read useVideoConfig() and re-flow for portrait.
 */
export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="Promo"
      component={Promo}
      durationInFrames={PROMO_DURATION}
      fps={30}
      width={1920}
      height={1080}
    />
    <Composition
      id="PromoSquare"
      component={Promo}
      durationInFrames={PROMO_DURATION}
      fps={30}
      width={1080}
      height={1080}
    />
    <Composition
      id="PromoVertical"
      component={Promo}
      durationInFrames={PROMO_DURATION}
      fps={30}
      width={1080}
      height={1920}
    />
  </>
);
