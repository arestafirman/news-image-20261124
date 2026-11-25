// news-image-20261124: copy the rendered poster to the output directory.
// The poster itself is entry.png, drawn by generate_image.py from the 36
// verified stories of Tuesday 24 November 2026. Node 22 stdlib only.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
console.log("wrote entry.png to", outDir);
