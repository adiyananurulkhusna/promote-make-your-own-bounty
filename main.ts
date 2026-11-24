// Handoff for the promote-make-your-own-bounty entry: the X post itself is the
// entry, and this program only carries the post's address (POST.json) into the
// output directory where the grader reads it.
//
// The address is checked with a pattern, not parsed: a post address is
// https://x.com/<handle>/status/<digits> (twitter.com works too). Anything
// else means the post has not been published yet, or POST.json still holds
// the placeholder.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import * as fs from "node:fs";
import * as path from "node:path";

const POST_PATTERN =
  /^https:\/\/(www\.)?(x\.com|twitter\.com)\/[A-Za-z0-9_]+\/status\/[0-9]+$/;

function die(message: string): never {
  console.error(`post handoff: ${message}`);
  process.exit(1);
}

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const postFile = path.join(botDir, "POST.json");
if (!fs.existsSync(postFile)) {
  die(`no POST.json found in ${botDir}`);
}

let doc: unknown;
try {
  doc = JSON.parse(fs.readFileSync(postFile, "utf8"));
} catch (err) {
  die(`POST.json is not valid JSON: ${(err as Error).message}`);
}

const address = (doc as { url?: unknown }).url;
if (typeof address !== "string" || !POST_PATTERN.test(address)) {
  die(
    "POST.json has no posted X address yet — post on X first, then put its address in POST.json and run again",
  );
}

const canonical = address
  .replace(/^https:\/\/www\./, "https://")
  .split(/[?#]/)[0];

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(
  path.join(outDir, "POST.json"),
  JSON.stringify({ url: canonical }) + "\n",
);

console.log(`post handoff ok: ${canonical}`);
