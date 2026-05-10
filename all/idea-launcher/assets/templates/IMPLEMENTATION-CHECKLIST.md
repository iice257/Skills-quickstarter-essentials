# Implementation Checklist: {{PROJECT_NAME}}

## Before Coding

- [ ] Read `AGENTS.md`, `MEMORY.md`, `docs/SPEC.md`, and `docs/TASKS.md`.
- [ ] Confirm the current branch and worktree state.
- [ ] Identify existing patterns, commands, and deployment path.
- [ ] Confirm the first workflow and non-goals.
- [ ] List assumptions that will be used without more questions.

## Build

- [ ] Scaffold only the structure needed for v1.
- [ ] Implement the core workflow end to end.
- [ ] Add persistence or state handling.
- [ ] Add error handling and empty states.
- [ ] Add configuration through environment variables where needed.
- [ ] Keep secrets out of source control.

## Quality

- [ ] Add focused tests for risky behavior.
- [ ] Run build, lint, typecheck, and tests when available.
- [ ] Verify the UI at desktop and mobile sizes if applicable.
- [ ] Check accessibility basics: labels, focus, contrast, keyboard flow.
- [ ] Remove unused files, placeholders, and debug output.

## Handoff

- [ ] Update docs or comments only where they help future work.
- [ ] Record durable facts in `MEMORY.md` if needed.
- [ ] Commit and push if this is a major completed task and instructions require it.
- [ ] Summarize changed files, verification, and residual risk.
