import { readFile } from "node:fs/promises";

const html = await readFile("index.html", "utf8");
const js = await readFile("src/main.js", "utf8");
const css = await readFile("src/styles.css", "utf8");

for (const [name, content] of [["index.html", html], ["src/main.js", js], ["src/styles.css", css]]) {
  if (content.includes("{{")) {
    throw new Error(`${name} contains unresolved template placeholders`);
  }
}

if (!html.includes("{{PROJECT_NAME}}") && !html.includes("<form")) {
  throw new Error("App shell is missing the core form");
}

console.log("Smoke test passed");
