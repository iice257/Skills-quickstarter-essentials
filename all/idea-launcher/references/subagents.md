# Subagent Guidance

Use subagents only when the current system and user instructions allow it. Split work when independent passes will save time or improve quality.

## Good Uses

- Codebase explorer: identify stack, commands, deployment path, and project conventions.
- Product critic: test whether the MVP is useful and narrow.
- Architecture reviewer: find data model, integration, and operational risks.
- UI planner: shape screens and workflows for app, game, or dashboard ideas.
- Verification planner: produce tests and acceptance checks.
- Deployment planner: inspect hosting, secrets, migrations, and rollback needs.
- Worker: implement a bounded slice with a disjoint write set.

## Bad Uses

- Immediate blocking decisions.
- Highly coupled edits across the same files.
- Vague "think about this" prompts.
- Sensitive production operations.
- Work that would duplicate the main thread.

## Split Pattern

Use this pattern for planning:

```text
You are helping with an Idea Launcher pass. Inspect only the provided repo/artifact and answer this bounded question:

Question:
Scope:
Do not edit files:
Return:
- findings
- risks
- recommended decisions
- files or commands inspected
```

Use this pattern for implementation:

```text
You are not alone in the codebase. Do not revert edits made by others. Own only these files/modules:

Task:
Write scope:
Inputs:
Acceptance checks:
Return:
- files changed
- tests run
- risks or follow-up work
```

## Integration Checklist

After subagents return:

- Reconcile conflicting assumptions.
- Keep one source of truth for scope.
- Copy only useful findings into the plan.
- Run verification locally before declaring completion.
- Close or ignore side findings that do not affect the current build.
