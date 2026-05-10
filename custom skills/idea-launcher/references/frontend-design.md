# Frontend Design Guidance

Use this reference whenever Idea Launcher generates or implements a web app, dashboard, tool UI, landing page, or browser game.

## Speed First

Default to fast, low-dependency frontends unless the target repo already uses a framework:

- Use static HTML, CSS, and vanilla JavaScript for generated starters.
- Add React, Next.js, animation libraries, charting libraries, or component frameworks only when the requested workflow needs them.
- Avoid dependency-heavy scaffolds for simple tools.
- Keep the first generated app runnable without install when possible.
- Make `npm test` and `npm run build` cheap smoke checks.

## Design First Pass

Before editing UI code, write three short decisions:

```text
Visual thesis:
Primary workspace:
Interaction thesis:
```

Then build the actual working surface. Do not create a marketing landing page unless the user asked for one.

## Generated App Defaults

For tools and apps:

- Start with the primary workspace, not a hero.
- Use restrained layout, clear labels, and domain-specific sample content.
- Make input, output, status, and next action visible in the first viewport.
- Include empty, success, and error states.
- Use cards only for repeated items, modals, or genuinely framed tools.
- Keep typography readable and stable across mobile and desktop.

For games:

- Make the loop playable before adding visual polish.
- Include score or feedback, restart, and clear controls.
- Use simple shapes or generated assets only when they support the mechanic.

For landing pages:

- Use the product, place, or offer as the first-viewport signal.
- Use a strong visual anchor, not a generic gradient.
- Keep the headline literal and concise.

## Avoid

- Heavy frameworks for a one-screen utility.
- Decorative dashboards that do not implement the workflow.
- Generic SaaS card grids.
- UI text explaining that this is a prototype.
- Overlapping text or controls.
- Slow install/build paths when a static app would work.

## Verification

Before finishing frontend work:

- Run the local smoke/build checks.
- Open the generated app if browser tooling is available.
- Check desktop and mobile widths.
- Confirm buttons, inputs, and generated output work.
- Confirm text fits in controls and panels.
- Confirm there are no unresolved placeholders.
