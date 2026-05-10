# Full Build Workflow

Use this when the user wants Idea Launcher to create the actual project, not just planning documents.

## Mental Model

The factory script creates a runnable baseline. Codex then performs a normal implementation pass inside that generated project. Do not treat generated docs as the final output.

## Sequence

1. Pick the closest starter pack: `web-app`, `automation`, `game`, or `data-tool`.
2. Run `scripts/launch_project.py`.
3. Run `scripts/validate_placeholders.py`.
4. Inspect generated `AGENTS.md`, `docs/SPEC.md`, and source files.
5. Replace demo logic with the real core workflow.
6. Replace generic copy and layout with domain-specific design.
7. Add or update tests around the real behavior.
8. Run the generated project commands.
9. Start the app/server when useful and provide the local URL or runnable command.

## Design Expectations

For web apps:

- Build the actual working surface first, not a landing page.
- Use restrained visual hierarchy, clear controls, and useful empty/error states.
- Include domain-specific labels and sample content.
- Avoid generic card grids unless cards are the actual interaction.
- Prefer static HTML/CSS/vanilla JS for generated starters unless an existing repo or user requirement calls for a framework.
- Keep the app fast to install, run, test, and build.
- Load `references/frontend-design.md` for the full frontend checklist.

For games:

- Make the core loop playable.
- Include start, active play, score or feedback, and restart.
- Use placeholder art only when the mechanic is still clear.

For automations:

- Include dry-run behavior by default.
- Produce logs or output artifacts.
- Keep risky actions approval-gated.

For data tools:

- Include fixture data.
- Validate input shape.
- Produce a concrete report/export.

## Done Means

- The project runs locally.
- The primary workflow works end to end.
- The generated docs match the implementation.
- Tests or smoke checks pass.
- The remaining limitations are explicit.
