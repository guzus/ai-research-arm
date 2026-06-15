import React from "react";
import { AbsoluteFill } from "remotion";
import {
  TransitionSeries,
  linearTiming,
  springTiming,
} from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { COLOR } from "./theme";
import { ColdOpen } from "./scenes/ColdOpen";
import { Firehose } from "./scenes/Firehose";
import { Pipeline } from "./scenes/Pipeline";
import { FrontPage } from "./scenes/FrontPage";
import { Product } from "./scenes/Product";
import { Outro } from "./scenes/Outro";

// Per-scene hold (frames @ 30fps) and the transition that follows it.
export const SCENES = {
  cold: 90,
  fire: 120,
  pipe: 120,
  front: 200,
  prod: 280,
  outro: 140,
};
export const TRANSITIONS = { a: 15, b: 18, c: 15, d: 18, e: 15 };

const sceneSum = Object.values(SCENES).reduce((x, y) => x + y, 0);
const transSum = Object.values(TRANSITIONS).reduce((x, y) => x + y, 0);
/** TransitionSeries overlaps sequences by each transition's duration. */
export const PROMO_DURATION = sceneSum - transSum;

export const Promo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: COLOR.navy }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={SCENES.cold}>
          <ColdOpen />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          timing={linearTiming({ durationInFrames: TRANSITIONS.a })}
          presentation={fade()}
        />
        <TransitionSeries.Sequence durationInFrames={SCENES.fire}>
          <Firehose />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          timing={springTiming({ config: { damping: 200 }, durationInFrames: TRANSITIONS.b })}
          presentation={wipe({ direction: "from-left" })}
        />
        <TransitionSeries.Sequence durationInFrames={SCENES.pipe}>
          <Pipeline />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          timing={linearTiming({ durationInFrames: TRANSITIONS.c })}
          presentation={fade()}
        />
        <TransitionSeries.Sequence durationInFrames={SCENES.front}>
          <FrontPage />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          timing={linearTiming({ durationInFrames: TRANSITIONS.d })}
          presentation={slide({ direction: "from-right" })}
        />
        <TransitionSeries.Sequence durationInFrames={SCENES.prod}>
          <Product />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          timing={linearTiming({ durationInFrames: TRANSITIONS.e })}
          presentation={fade()}
        />
        <TransitionSeries.Sequence durationInFrames={SCENES.outro}>
          <Outro />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
