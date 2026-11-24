// V2 entry program for news-image-20261123: copies the pre-built
// entry.png (drawn by draw.py) into the output directory. Validates the
// image before copying so a corrupt or oversized file fails loudly
// instead of submitting a broken entry.
import { copyFileSync, existsSync, statSync, mkdirSync, openSync, readSync, closeSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const SRC = join(BOT_DIR, "entry.png");
const DEST = join(OUT_DIR, "entry.png");
const MAX_BYTES = 1024 * 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

if (!existsSync(SRC)) {
  console.error(`entry image not found: ${SRC}`);
  process.exit(1);
}
const info = statSync(SRC);
if (info.size === 0) {
  console.error("entry image is empty");
  process.exit(1);
}
if (info.size > MAX_BYTES) {
  console.error(`entry image too large: ${info.size} bytes (max ${MAX_BYTES})`);
  process.exit(1);
}
const fd = openSync(SRC, "r");
const head = Buffer.alloc(8);
readSync(fd, head, 0, 8, 0);
closeSync(fd);
if (!head.equals(PNG_MAGIC)) {
  console.error("entry image is not a PNG (bad magic bytes)");
  process.exit(1);
}
mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, DEST);
console.log(`copied entry.png (${info.size} bytes) to ${DEST}`);
