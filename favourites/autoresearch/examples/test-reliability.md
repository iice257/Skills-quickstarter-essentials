# Example: Test Reliability

Use autoresearch when tests fail, are flaky, or need targeted reliability improvement.

## Clarifying answers

- Project type: unknown/mixed project unless the repo clearly indicates otherwise.
- Main improvement target: test reliability and flaky test reduction.
- Exact metric: passing tests increase and flaky tests decrease. Higher pass count and lower flaky count are better.
- Metric command: `npm test`, or the detected test command approved by the user.
- Approved scope: tests, test utilities, deterministic setup code, and narrowly related implementation defects.
- Forbidden scope: deleting tests to improve pass count, weakening assertions without approval, `.env` files, secrets, auth flows, payment logic, migrations, lockfiles unless approved, generated files, and unrelated refactors.
- Experiment budget: 10.
- Risk level: conservative.
- Git behavior: branch and commit kept experiments.
- Final output format: next-step recommendations plus experiment log.

## Example prompt

Use the autoresearch skill on this repo. Ask me clarifying questions first. I want to improve test reliability. Use `npm test` or the detected test command after I approve it. Only touch tests, test utilities, deterministic setup code, and narrowly related implementation defects. Do not delete tests, weaken assertions, or touch secrets, auth, payments, migrations, lockfiles, generated files, or unrelated code. Run 10 experiments, keep only measurable improvements, revert regressions, then give me an experiment log and next-step recommendations.

## Measurement notes

Record total tests, passing tests, failing tests, and known flaky tests when available. A kept experiment should increase stable passing tests or reduce confirmed flakiness without reducing meaningful coverage.
