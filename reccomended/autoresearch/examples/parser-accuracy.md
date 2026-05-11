# Example: Parser Accuracy

Use autoresearch when a parser, classifier, extractor, or evaluator has fixtures that can measure correctness.

## Clarifying answers

- Project type: parser/classifier.
- Main improvement target: parser fixture accuracy.
- Exact metric: fixture pass rate increases. Higher pass rate is better.
- Metric command: `npm run test:parser`.
- Approved scope: parser implementation, parser tests, and fixtures approved for correction.
- Forbidden scope: unrelated application code, generated files, public API changes unless approved, and fixture expectation changes that hide real failures.
- Experiment budget: 10.
- Risk level: moderate.
- Git behavior: branch and commit kept experiments.
- Final output format: full experiment log.

## Example prompt

Use the autoresearch skill on this repo. Ask me clarifying questions first. I want to improve parser fixture accuracy. Use `npm run test:parser` as the metric command. Only touch parser implementation and approved parser fixtures. Do not touch unrelated app code, generated files, or public APIs. Run 10 experiments, keep only measurable improvements, revert regressions, then give me a full experiment log.

## Measurement notes

Record passed fixtures, failed fixtures, and pass rate. Prefer implementation fixes over changing expected outputs. Only update fixtures when the user confirms the previous fixture was wrong.
