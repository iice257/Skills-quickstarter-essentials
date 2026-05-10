# Test Plan: {{PROJECT_NAME}}

## Test Strategy

The highest-risk behavior is:

- {{RISKY_BEHAVIOR}}

The first tests should prove:

- {{CORE_ASSERTION}}

## Automated Checks

| Area | Check | Tool | Acceptance |
| --- | --- | --- | --- |
| Unit | {{UNIT_CHECK}} | {{TOOL}} | {{ACCEPTANCE}} |
| Integration | {{INTEGRATION_CHECK}} | {{TOOL}} | {{ACCEPTANCE}} |
| End-to-end | {{E2E_CHECK}} | {{TOOL}} | {{ACCEPTANCE}} |

## Manual Checks

1. Start the app or tool.
2. Complete the core workflow.
3. Trigger one known error state.
4. Confirm data is saved, exported, sent, or displayed as expected.
5. Confirm the app recovers after refresh or restart if persistence exists.

## UI Checks

- Desktop:
- Mobile:
- Keyboard:
- Screen reader labels:
- Empty states:
- Error states:

## Deployment Smoke Test

- Deployed URL or executable:
- Required env vars present:
- Health check:
- Core workflow:
- Logs checked:

## Release Criteria

- [ ] Core workflow passes.
- [ ] Highest-risk failure path passes.
- [ ] Build passes.
- [ ] Deployment smoke test passes.
- [ ] Known limitations are documented.
