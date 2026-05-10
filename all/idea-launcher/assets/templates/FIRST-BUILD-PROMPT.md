# First Build Prompt: {{PROJECT_NAME}}

Use this prompt to start a fresh implementation thread.

```text
Use $idea-launcher in ship mode for this project.

Project:
{{PROJECT_NAME}}

Goal:
{{ONE_LINE_CONCEPT}}

Read first:
- AGENTS.md
- MEMORY.md
- docs/SPEC.md
- docs/TASKS.md
- docs/IMPLEMENTATION-CHECKLIST.md
- docs/TEST-PLAN.md
- docs/DEPLOY-PLAN.md

Build target:
{{CORE_WORKFLOW}}

Non-goals for v1:
{{NON_GOALS}}

Constraints:
{{CONSTRAINTS}}

Expected work:
1. Inspect the repo and confirm commands.
2. Implement the smallest end-to-end version of the core workflow.
3. For frontend work, make the UI domain-specific, responsive, and fast before adding dependencies.
4. Add focused tests for the riskiest behavior.
5. Run available verification commands.
6. Start the dev server or provide the executable/open path if appropriate.
7. Summarize files changed, tests run, deploy status, and residual risks.

Use subagents only if the current session allows it and the work can be split without overlapping file ownership.
```
