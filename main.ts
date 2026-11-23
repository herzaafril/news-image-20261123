// News-image entry for make.fun news-image-20261123 ("Sum up 23 November's
// world news in one image"). The image is drawn by draw.py (kept in this
// repo) and shipped as entry.png beside this file. This program only
// validates the image and copies it to /output/entry.png.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = join(botDir, 'entry.png');

if (!existsSync(src)) {
  throw new Error(`entry.png not found in ${botDir}`);
}
const size = statSync(src).size;
if (!statSync(src).isFile() || size === 0) {
  throw new Error('entry.png is not a non-empty file');
}
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB gate`);
}
// The gate tells PNG from JPEG by the first bytes: refuse anything that is
// not a PNG, so a bad build fails loudly here instead of at the gate.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!readFileSync(src).subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png does not start with the PNG signature');
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, 'entry.png'));
console.log(`copied entry.png (${size} bytes) to ${outDir}`);
