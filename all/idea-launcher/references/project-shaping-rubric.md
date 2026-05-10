# Project Shaping Rubric

Use this rubric to turn an idea into a buildable project shape. Keep the output practical and opinionated.

## Scorecard

Score each dimension as `strong`, `okay`, or `weak`. Weak dimensions do not block the project automatically; they force scope cuts, assumptions, or questions.

| Dimension | Decide | Good Signs | Bad Signs |
| --- | --- | --- | --- |
| Usefulness | Who needs this and why now? | Repeated pain, clear saved time, obvious demo | Novelty only, vague "users", no workflow |
| Scope | What is v1 and what is not? | One core loop, few screens, obvious non-goals | Multiple products, admin panels too early, vague roadmap |
| Stack | What should it be built with? | Fits existing repo, deploy path is known | New stack for novelty, many services before need |
| Data model | What entities exist? | 3-7 clear entities, simple lifecycle | No owner, unclear source of truth, hidden sync |
| UI | What surfaces are required? | Primary workspace is obvious | Marketing page replaces the actual tool |
| Workflows | What must users do end to end? | Named happy path and failure path | Feature list with no journey |
| Automation | What should run without manual work? | Repeated trigger, clear output, logs | Unbounded agent loops, no approval boundaries |
| Risks | What can break the project? | Known hardest part and fallback | Risk hidden inside "AI will handle it" |
| Verification | How do we know it works? | Tests map to workflows and risks | Only visual checking, no acceptance criteria |
| Deployment | Where does it run? | Host, env vars, secrets, rollback known | Local-only assumptions for a public product |

## Tradeoff Output

Always include:

```text
Bet:
Good side:
Bad side:
Hidden complexity:
Smallest credible version:
Scope cuts:
Kill or pause trigger:
```

## Scope Rules

Default cuts for v1 unless they are the core value:

- Avoid multi-role auth.
- Avoid payments.
- Avoid public collaboration.
- Avoid full admin dashboards.
- Avoid custom design systems.
- Avoid background jobs without a clear trigger and retry model.
- Avoid AI autonomy where a generated draft plus user approval works.

## Stack Rules

Choose the stack in this order:

1. Existing repo patterns and deployment path.
2. User's explicit stack preference.
3. Fastest stable option for the project type.
4. Lowest operational burden.

Do not introduce a database, queue, auth provider, or external service until the workflow needs it.

## Data Model Prompt

Write entities as nouns with owners and lifecycle:

```text
Entity:
Purpose:
Created by:
Updated by:
Fields:
Relationships:
Retention or deletion:
```

## Verification Prompt

Tie verification to the actual risk:

- Core workflow test
- Edge case test
- Data integrity test
- Permission or approval test
- Error and retry test
- Deployment smoke test
- Manual visual check, if UI matters

## Recommendation Rule

End with a recommendation:

- **Build now:** Clear useful core and manageable risk.
- **Prototype first:** Unknown technical or UX feasibility.
- **Sharpen first:** The process, template, or problem framing is weaker than the build plan.
- **Do not build yet:** The user, workflow, or payoff is too unclear.
