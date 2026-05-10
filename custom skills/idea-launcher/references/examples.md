# Examples

Use these examples to calibrate output quality. Keep future examples short enough to copy into a real launch plan.

## Web App Example

Prompt:

```text
Use $idea-launcher in ship mode for a web app that turns messy meeting notes into decisions, tasks, and follow-ups.
```

Recommended v1:

- Paste notes into a single screen.
- Extract decisions, owners, tasks, and due dates.
- Let the user edit the result.
- Export Markdown.

Good side:

- Repeated personal workflow.
- Easy to demo.
- Does not need accounts in v1.

Bad side:

- AI extraction can be unreliable.
- The app can sprawl into calendars, Slack, email, and team collaboration.

Scope cut:

- No accounts, integrations, or automatic sending in v1.

## Automation Example

Prompt:

```text
Use $idea-launcher in factory mode for an automation that checks a folder of PDFs and creates a weekly summary.
```

Recommended v1:

- Manual command reads one folder.
- Extracts text from PDFs.
- Writes a Markdown summary and a run log.
- Fails visibly when a PDF cannot be parsed.

Good side:

- High leverage if the folder review happens repeatedly.
- Local dry-run avoids deployment risk.

Bad side:

- PDF extraction quality may vary.
- Scheduling too early can hide broken runs.

Scope cut:

- No email sending until summaries are accurate.

## Detailed Prompt Example

Prompt:

```text
Use $idea-launcher to build a local tool that watches a folder of CSV exports, detects duplicate customer records, and writes a cleanup report for an ops teammate. Keep it local, use Python, and avoid a database in v1.
```

Correct behavior:

- Treat it as detailed enough.
- Give a serious pass with summary, assumptions, pushbacks, suggestions, and v1 boundary.
- Then implement if the user asked to build.

Incorrect behavior:

- Silently generating code with no summary.
- Asking broad questions like "what features do you want?"

## Game Example

Prompt:

```text
Use $idea-launcher to shape a tiny browser game where you redirect falling signals into matching channels.
```

Recommended v1:

- One playable round.
- One input mechanic.
- Score, fail condition, restart.
- Placeholder visuals until the mechanic is fun.

Good side:

- Mechanic is easy to test quickly.
- Small enough for a weekend prototype.

Bad side:

- Can expand into levels, effects, unlocks, and art before the loop works.

Scope cut:

- No progression system or account storage in v1.
