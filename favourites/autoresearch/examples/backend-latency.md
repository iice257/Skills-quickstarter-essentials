# Example: Backend API Latency

Use autoresearch when a backend API has a repeatable benchmark or load-test command.

## Clarifying answers

- Project type: backend API.
- Main improvement target: API latency.
- Exact metric: p95 latency decreases. Lower p95 latency is better.
- Metric command: `npm run bench`, or the detected benchmark command approved by the user.
- Approved scope: backend handlers, service code, query paths, caching code, and benchmark-safe configuration.
- Forbidden scope: `.env` files, secrets, auth flows, payment logic, database migrations, lockfiles unless approved, generated files, and public API contract changes unless approved.
- Experiment budget: 10.
- Risk level: conservative.
- Git behavior: branch and commit kept experiments.
- Final output format: PR-ready report.

## Example prompt

Use the autoresearch skill on this repo. Ask me clarifying questions first. I want to reduce backend API p95 latency. Use `npm run bench` or the detected benchmark command after I approve it. Only touch backend request handling and performance-related service code. Do not touch secrets, auth, payments, migrations, lockfiles, generated files, or public API contracts. Run 10 experiments, keep only measurable improvements, revert regressions, then give me a PR-ready summary.

## Measurement notes

Record baseline p95 latency, final p95 latency, and percentage change. If benchmark variance is high, repeat the metric command enough to confirm the direction before keeping an experiment.
