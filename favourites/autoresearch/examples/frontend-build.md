# Example: Frontend Build Reliability

Use autoresearch when a frontend app has failing builds, TypeScript errors, or unstable validation commands.

## Clarifying answers

- Project type: frontend app.
- Main improvement target: build reliability and TypeScript errors.
- Exact metric: build succeeds and TypeScript error count decreases. Lower TypeScript error count is better.
- Metric commands: `npm run typecheck` and `npm run build`.
- Approved scope: application source files and local config needed to fix type errors.
- Forbidden scope: `.env` files, secrets, auth flows, payment logic, lockfiles unless approved, generated files, public API changes, and unrelated UI redesigns.
- Experiment budget: 10.
- Risk level: conservative.
- Git behavior: branch and commit kept experiments.
- Final output format: PR-ready report.

## Example prompt

Use the autoresearch skill on this repo. Ask me clarifying questions first. I want to improve frontend build reliability. Use `npm run typecheck` and `npm run build` as the metric commands. Only touch frontend source and config files needed for type/build fixes. Do not touch secrets, auth, payments, lockfiles, generated files, or unrelated UI. Run 10 experiments, keep only measurable improvements, revert regressions, then give me a PR-ready summary.

## Measurement notes

Record the baseline TypeScript error count and build result. A kept experiment should reduce the error count or preserve zero errors while fixing build failure. Do not keep visual redesigns unless they are required for the build metric.
