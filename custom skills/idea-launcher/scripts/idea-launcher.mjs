#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const launcher = join(here, "launch_project.py");
const rawArgs = process.argv.slice(2);

function normalizeArgs(args) {
  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    return args;
  }

  const hasLongForm = args.some((arg) => arg.startsWith("--name") || arg.startsWith("--idea"));
  if (hasLongForm) {
    return args;
  }

  const [type = "web-app", name = "Idea App", idea = name, ...rest] = args;
  return ["--type", type, "--name", name, "--idea", idea, "--out", "./output", ...rest];
}

const args = normalizeArgs(rawArgs);

const candidates = process.platform === "win32" ? ["python", "py"] : ["python3", "python"];
let result;

for (const command of candidates) {
  result = spawnSync(command, [launcher, ...args], { stdio: "inherit" });
  if (result.error?.code === "ENOENT") {
    continue;
  }
  process.exit(result.status ?? 1);
}

console.error("Idea Launcher requires Python 3 on PATH.");
process.exit(1);
