import { readFile } from "node:fs/promises";

const html = await readFile("index.html", "utf8");
const game = await readFile("src/game.js", "utf8");

if (html.includes("{{") || game.includes("{{")) {
  throw new Error("Unresolved template placeholder found");
}

if (!html.includes("<canvas") || !game.includes("requestAnimationFrame")) {
  throw new Error("Game loop scaffold is incomplete");
}

console.log("Smoke test passed");
