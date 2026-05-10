# Tasks: {{PROJECT_NAME}}

Status: `[ ]` todo, `[-]` in progress, `[x]` done, `[!]` blocked.

## Milestone 0 - Shape And Setup

- [ ] Confirm MVP scope and non-goals.
- [ ] Choose stack and deployment target.
- [ ] Create or update `AGENTS.md` with project commands and conventions.
- [ ] Create `.env.example` for required configuration.
- [ ] Verify local install, build, and test commands.

Acceptance:

- Spec has no hidden critical assumptions.
- Project starts locally.
- First build command is known.

## Milestone 1 - Core Workflow

- [ ] Implement the smallest end-to-end workflow.
- [ ] Add the minimum data model or file format needed.
- [ ] Add user-visible success and error states.
- [ ] Add tests for the happy path and one failure path.

Acceptance:

- A user can complete the core workflow without manual database or file edits.
- Tests cover the riskiest behavior.

## Milestone 2 - Product Fit

- [ ] Tighten UI, copy, and defaults.
- [ ] Add persistence, export, or automation only if needed for the core workflow.
- [ ] Add empty, loading, error, and recovery states.
- [ ] Document known limitations.

Acceptance:

- The project feels usable for the first target user.
- Non-goals remain out of scope.

## Milestone 3 - Verification And Deploy

- [ ] Run unit or integration tests.
- [ ] Run end-to-end or manual workflow checks.
- [ ] Run build and lint/typecheck if available.
- [ ] Configure deployment environment variables and secrets.
- [ ] Deploy preview or production target.
- [ ] Run post-deploy smoke test.

Acceptance:

- Deploy URL or executable path works.
- Rollback path is known.

## Later

- [ ] {{LATER_TASK}}
