import { Config } from "@remotion/cli/config";

// Promo render defaults. The CLI scripts in package.json override codec/crf
// per target (mp4 / gif). JPEG frames keep the render fast; the newspaper
// B-roll is already lossy PNG so the quality ceiling is the source art.
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.setConcurrency(null); // let Remotion pick based on cores
