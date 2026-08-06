/**
 * Loads the dashboard's three faces through @remotion/google-fonts so every
 * frame renders deterministically (the helper registers delayRender handles
 * internally and resolves them once the webfonts are ready).
 *
 * Faces match dashboard/index.html: Source Serif 4 (display), Inter (UI),
 * JetBrains Mono (eyebrows / metadata).
 */
import {
  loadFont as loadSerif,
  fontFamily as serifFamily,
} from "@remotion/google-fonts/SourceSerif4";
import {
  loadFont as loadSans,
  fontFamily as sansFamily,
} from "@remotion/google-fonts/Inter";
import {
  loadFont as loadMono,
  fontFamily as monoFamily,
} from "@remotion/google-fonts/JetBrainsMono";

loadSerif();
loadSans();
loadMono();

export const SERIF = `'${serifFamily}', Georgia, 'Times New Roman', serif`;
export const SANS = `'${sansFamily}', Inter, -apple-system, system-ui, sans-serif`;
export const MONO = `'${monoFamily}', ui-monospace, 'SFMono-Regular', monospace`;
