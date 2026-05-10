# Modes

Select the mode from the user's wording and the state of the idea.

## Default Launch Mode

Use when the user wants to turn an idea into a plan.

Output:

- Idea summary
- Good side and bad side
- Assumptions
- MVP
- Project shaping rubric
- Recommended artifacts to create
- Up to 3 questions

## Factory Mode

Use when the user wants reusable starter structures, repeatable templates, or a project factory.

Behavior:

- Create a reusable starter layout, not a one-off plan.
- Include naming conventions, doc templates, setup commands, quality gates, and handoff prompts.
- Keep defaults minimal so future projects can specialize them.
- Separate "always included" from "add when needed".
- Use `scripts/launch_project.py` when the user wants an actual folder generated.
- Run `scripts/validate_placeholders.py` after generation.

Starter structure should usually include:

```text
AGENTS.md
MEMORY.md
docs/SPEC.md
docs/TASKS.md
docs/IMPLEMENTATION-CHECKLIST.md
docs/TEST-PLAN.md
docs/DEPLOY-PLAN.md
docs/FIRST-BUILD-PROMPT.md
src/
tests/
.env.example
```

Built-in starter packs:

- `web-app`: browser-first tools and deployable apps.
- `automation`: scripts, scheduled jobs, and personal workflows.
- `game`: tiny playable prototypes and browser games.
- `data-tool`: ingestion, transformation, reports, and exports.

Factory mode deliverable levels:

- **Plan only:** docs and next build prompt.
- **Starter:** docs plus runnable baseline from `assets/blueprints/`.
- **Full build:** generated baseline plus project-specific implementation, tests, and local run command.

If the user asks for "the full project", "the app", "designs", "everything", or "build it out", use full build.

## Sharpen-The-Axe Mode

Use when the user wants to improve the process before building.

Behavior:

- Inspect existing templates, failed plans, or previous project artifacts.
- Find ambiguity, repeated rework, missing checks, and weak handoffs.
- Improve templates, rubrics, prompts, or starter structures.
- Do not start implementation unless the user explicitly switches to build mode.

Output:

- What the process is currently optimized for
- Where it will fail
- Template or workflow changes
- Updated prompts or checklists
- How to test the improved process on a small idea

## Ship Mode

Use when the user wants aggressive narrowing and implementation momentum.

Behavior:

- Freeze the first build around one core workflow.
- Convert unclear features into assumptions or later tasks.
- Prefer boring stack choices and low operational burden.
- Produce tasks that can be executed in order.
- Start implementation when the user has asked to build and the repo context is clear.
- For generated projects, edit the runnable blueprint into the real product before finishing.

Ship mode refuses scope creep with:

```text
Not in v1:
- ...

Later:
- ...

Current build target:
- ...
```

## Brainstorm Mode

Use when the user explicitly wants to expand the idea first.

Behavior:

- Explore variants, audiences, monetization or value paths, and failure modes.
- Include good and bad sides for each promising direction.
- End by recommending one direction, one smaller version, and one thing not to build yet.

Do not produce a large task plan until a direction is chosen.

## Serious Pass Before Build

Use before implementation when the prompt is already specific enough to act on. This is not a long planning phase; it is a short checkpoint that prevents Codex from building the wrong thing too confidently.

Output:

- Build summary
- Assumptions
- Pushbacks and risks
- Suggestions
- Current v1 boundary
- Immediate execution plan

If the user already asked to build and the assumptions are low-risk, continue into implementation after the serious pass. If one missing answer would change the stack, data model, auth, deployment, or primary workflow, ask that single question first.
