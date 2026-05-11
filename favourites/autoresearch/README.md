# Autoresearch Skill

`autoresearch` is a reusable Codex skill for measured improvement work across software projects. It makes an agent slow down, ask clarifying questions, define a metric, establish a baseline, run small experiments, keep only measurable wins, and revert failures.

## Use cases

- Build reliability and TypeScript error reduction.
- Parser, classifier, or fixture accuracy.
- Backend latency and benchmark improvement.
- Test reliability and flaky test reduction.
- Bundle size, runtime performance, memory usage, accessibility, Lighthouse, lint, documentation, or developer-experience improvement.

## Required inputs

The skill asks for:

- Project type.
- Improvement target.
- Exact measurable metric.
- Metric command.
- Approved scope.
- Forbidden scope.
- Experiment budget.
- Risk level.
- Git behavior.
- Final output format.

It refuses to run an experiment loop without a measurable metric.

## Sample prompt

> "Use the autoresearch skill on this repo. Ask me clarifying questions first. I want to improve [target]. Use [command] as the metric command. Only touch [scope]. Do not touch [forbidden scope]. Run [number] experiments, keep only measurable improvements, revert regressions, then give me a PR-ready summary."

## Safety warnings

Autoresearch is intentionally conservative. It treats `.env` files, secrets, auth flows, payment logic, database migrations, lockfiles unless approved, generated files, unrelated UI redesigns, and public API changes unless approved as forbidden by default.

Experiment logs are local-only and should be ignored through `.git/info/exclude`, not committed through `.gitignore`.

## Reviewing results

Review the final report and kept commits before merge. Confirm the metric improved, the changed files are within scope, the exact commands ran successfully, and no forbidden scope changed.
