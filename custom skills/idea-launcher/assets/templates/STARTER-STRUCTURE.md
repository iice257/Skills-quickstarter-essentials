# Starter Structure: {{PROJECT_NAME}}

Use this in factory mode to create repeatable project scaffolds. Tailor it to the stack before creating files.

## Minimal Structure

```text
AGENTS.md
MEMORY.md
docs/
  SPEC.md
  TASKS.md
  IMPLEMENTATION-CHECKLIST.md
  TEST-PLAN.md
  DEPLOY-PLAN.md
  FIRST-BUILD-PROMPT.md
src/
tests/
.env.example
```

## Add When Needed

For web apps:

```text
app/ or src/
components/
lib/
public/
```

For automations:

```text
scripts/
jobs/
logs/ or output/
config/
```

For games:

```text
src/game/
src/assets/
src/scenes/
src/systems/
```

For data products:

```text
data/
notebooks/
pipelines/
schemas/
```

## Required Starter Decisions

- Project type:
- Stack:
- Package manager:
- Dev command:
- Test command:
- Deployment target:
- Persistence:
- Secrets:
- First workflow:

## Factory Defaults

- Keep generated docs under `docs/` unless the repo already has a docs convention.
- Keep project instructions in `AGENTS.md`.
- Keep durable project facts in `MEMORY.md`.
- Use `.env.example` for names and comments, never real secrets.
- Add only the directories needed by the first workflow.
