# Idea Launcher

Idea Launcher is a local Codex skill for turning rough app, tool, game, automation, and data-product ideas into build-ready specs, task plans, verification checklists, deploy plans, and runnable starter projects.

It is designed as a one-person software factory: clarify the idea quickly, cut scope hard, generate the right starting structure, and move Codex into implementation instead of stopping at planning docs.

## How To Use

Install the skill into Codex with the skill installer:

```text
$skill-installer install https://github.com/iice257/Skills/tree/main/all/idea-launcher
```

Use it inside Codex:

```text
Use $idea-launcher in full-build mode. Build me a small web app called Signal Notes that turns rough notes into decisions, tasks, and follow-ups. Generate the project, implement the working UI, add tests, and run it locally.
```

Generate a runnable starter from an installed copy:

```powershell
node scripts/idea-launcher.mjs web-app "Signal Notes" "Turns rough notes into decisions and tasks"
```

Or use PowerShell directly after cloning/installing the skill:

```powershell
node scripts/idea-launcher.mjs web-app "Signal Notes" "Turns rough notes into decisions and tasks"
```

Long-form flags still work when you need custom output paths:

```powershell
node scripts/idea-launcher.mjs --name "Signal Notes" --idea "Turns rough notes into decisions and tasks" --type web-app --out ./output
```

## What It Does

- Interviews lightly without over-questioning.
- Surfaces the good side, bad side, hidden complexity, and smallest credible version.
- Generates `SPEC.md`, `TASKS.md`, test plans, deploy plans, and first-build prompts.
- Creates runnable starter projects for web apps, automations, games, and data tools.
- Reinforces frontend design and speed defaults for generated web projects.
- Guides when to use subagents for faster planning, review, and implementation.

## Starter Packs

- `web-app`: static browser app with working UI, CSS, JS, build script, and smoke test.
- `automation`: Python automation with dry-run behavior, output artifact, and tests.
- `game`: canvas game loop with controls, restart, build script, and smoke test.
- `data-tool`: CSV fixture, report generator, and tests.

## Validate Output

```powershell
python scripts/validate_placeholders.py ./output/signal-notes
```

Then open the generated folder, read `AGENTS.md`, and run the commands listed there.

## Install

Copy this folder to:

```text
%USERPROFILE%\.codex\skills\idea-launcher
```

Restart Codex if the skill does not appear immediately.

## Repository Description

Codex skill that turns rough ideas into build-ready specs, tasks, deploy plans, and runnable starter projects.
