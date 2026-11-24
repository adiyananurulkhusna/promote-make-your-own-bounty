// Entry program for the post-x-promote-make-your-own-bounty-01 bounty
// (Node 22, standard library only).
//
// The entry is the X post itself: a quote of make.fun's make-your-own-bounty
// post, carrying a poster that asks readers what bounty THEY would post with
// $250 in USDC. The score is replies + reposts + quotes, so the post is a
// question, not a punchline.
//
// This program has exactly one job — carry POST.json, the posted entry's
// address, from the repository into the output directory where the gate can
// read it.
//
// POST.json starts as a placeholder. After the post is published on X, the
// real post address replaces the placeholder and this program is run again;
// the gate then fetches the post itself. Nothing this program prints is
// judged.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const POST_FILE = "POST.json";

// A post address is https://x.com/<handle>/status/<digits> (twitter.com
// works too). Anything else is a placeholder that has not been filled in yet.
// Links copied out of the X app often carry tracking queries (?a=...&s=19)
// and fragments; those are stripped, so the canonical address is what the
// gate fetches — the same post, without the tracking tail.
function canonicalPostUrl(value: unknown): string | null {
  if (typeof value !== "string") return null;
  let parsed: URL;
  try {
    parsed = new URL(value);
  } catch {
    return null;
  }
  const hostOk =
    parsed.hostname === "x.com" ||
    parsed.hostname === "twitter.com" ||
    parsed.hostname.endsWith(".x.com") ||
    parsed.hostname.endsWith(".twitter.com");
  if (!hostOk || parsed.protocol !== "https:") return null;
  const parts = parsed.pathname.split("/").filter(Boolean);
  if (parts.length !== 3 || parts[1] !== "status") return null;
  if (parts[0].length === 0 || !/^\d+$/.test(parts[2])) return null;
  parsed.search = "";
  parsed.hash = "";
  return parsed.toString();
}

function loadPostUrl(): string {
  const source = join(botDir, POST_FILE);
  if (!existsSync(source)) {
    console.error(`no ${POST_FILE} found in ${botDir}; cannot hand off a post`);
    process.exit(1);
  }
  let raw: string;
  try {
    raw = readFileSync(source, "utf8");
  } catch (err) {
    console.error(`could not read ${source}: ${(err as Error).message}`);
    process.exit(1);
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    console.error(`${POST_FILE} is not valid JSON: ${(err as Error).message}`);
    process.exit(1);
  }
  const url = (parsed as { url?: unknown }).url;
  const canonical = canonicalPostUrl(url);
  if (canonical === null) {
    console.error(
      `${POST_FILE} has no posted address yet (expected ` +
        `https://x.com/<handle>/status/<id>); post on X first, ` +
        `then replace the placeholder and run again.`,
    );
    process.exit(1);
  }
  return canonical;
}

function main(): void {
  const url = loadPostUrl();
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, POST_FILE);
  try {
    writeFileSync(target, JSON.stringify({ url }) + "\n");
  } catch (err) {
    console.error(`could not write ${target}: ${(err as Error).message}`);
    process.exit(1);
  }
  const postId = url.split("/").filter(Boolean).pop();
  console.log(`handing off post ${postId}: ${url}`);
}

main();
