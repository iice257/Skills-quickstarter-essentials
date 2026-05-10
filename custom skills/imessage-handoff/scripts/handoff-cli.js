#!/usr/bin/env node
const { existsSync } = require("fs");
const { spawnSync } = require("child_process");
const path = require("path");

const skillDir = path.resolve(__dirname, "..");
const childEnv = {
  ...process.env,
  NODE_OPTIONS: withNodeOption(process.env.NODE_OPTIONS, "--use-system-ca"),
};
const candidates = [
  process.env.HANDOFF_CLI,
  path.resolve(skillDir, "..", "bin", "handoff.mjs"),
  path.resolve(skillDir, "..", "..", "bin", "handoff.mjs"),
].filter(Boolean);

let result = null;
for (const candidate of candidates) {
  if (existsSync(candidate)) {
    result = spawnSync(process.execPath, [candidate, ...process.argv.slice(2)], {
      stdio: "inherit",
      env: childEnv,
    });
    break;
  }
}

if (!result) {
  result = spawnSync("handoff", process.argv.slice(2), {
    stdio: "inherit",
    env: childEnv,
    shell: process.platform === "win32",
  });
}

if (result.error) {
  console.error("iMessage Handoff CLI is unavailable. Run `handoff doctor` after installing the package, or set HANDOFF_CLI to the repo bin/handoff.mjs path.");
  console.error(result.error.message);
  process.exit(1);
}

process.exit(result.status || 0);

function withNodeOption(current, option) {
  const value = String(current || "").trim();
  if (process.platform !== "win32") {
    return value;
  }
  if (value.split(/\s+/).includes(option)) {
    return value;
  }
  return value ? `${value} ${option}` : option;
}
