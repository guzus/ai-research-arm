// One-shot asset prep: stage front pages + (re)build the screens manifest.
// Wired into the studio/render/poster npm scripts so a clean checkout renders.
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {dirname, join} from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
for (const s of ['copy-frontpages.mjs', 'gen-screens.mjs']) {
  execFileSync(process.execPath, [join(here, s)], {stdio: 'inherit'});
}
