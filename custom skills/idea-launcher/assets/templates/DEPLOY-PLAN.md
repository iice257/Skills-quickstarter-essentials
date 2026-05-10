# Deploy Plan: {{PROJECT_NAME}}

## Target

- Environment:
- Host:
- URL or distribution target:
- Owner:

## Build And Runtime

- Install command:
- Build command:
- Runtime command:
- Output directory:
- Required runtime:

## Configuration

| Name | Purpose | Required | Source |
| --- | --- | --- | --- |
| {{ENV_VAR}} | {{ENV_PURPOSE}} | yes/no | {{ENV_SOURCE}} |

## Secrets

- Secret manager:
- Rotation expectation:
- Local `.env` handling:
- Production setup:

## Data And Migrations

- Database or storage:
- Migration command:
- Seed data:
- Backup:
- Rollback:

## Pre-Deploy Checklist

- [ ] Tests pass.
- [ ] Build passes.
- [ ] Env vars are configured.
- [ ] Secrets are configured.
- [ ] Database migrations are reviewed.
- [ ] Rollback path is known.

## Post-Deploy Smoke Test

1. Open deployed target.
2. Complete the core workflow.
3. Check logs for errors.
4. Confirm data persistence or output delivery.
5. Verify rollback or redeploy command is available.

## Rollback

- Command or platform action:
- Data rollback:
- User communication:
