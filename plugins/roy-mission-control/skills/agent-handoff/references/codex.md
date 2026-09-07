# Codex runtime

Use this reference only in Codex. Keep the same stages, files, reports, and
acceptance gates as Claude Code. The captain stays in the main task.

## Delegation

Inside Herdr, follow [the pane workflow](herdr.md) first and use
`transport: codex-pane`.

Outside Herdr, use the available native subagent interface. Give the subagent a
bounded stage assignment and absolute paths to the generated agent definition,
required skills, project root, mission root, inputs, outputs, and report. Do not
create a sidebar task for ordinary delegation. If native delegation is absent,
run the role inline and record `transport: inline`.

Use the model and reasoning settings in the generated Codex agent definition.
An explicit user choice takes precedence. If the host cannot apply an override,
state that limitation instead of claiming it was applied.

## Questions and reports

Use the permitted structured-question interface when suitable. In a delegated
run without an interactive user channel, return `blocked` or `needs_user` to the
captain. The captain gathers answers and resumes the same stage.

A specialist writes its artifacts and inbox report before returning status.
Use the native parent-message channel when available. Otherwise, completion and
the saved inbox notify the captain. Follow-up work must keep the same run ID.

Create a separate user-visible task only when the user explicitly requests one.
That task conducts the specialist conversation; it does not become another
captain.

Installing the plugin exposes generated skills and agent definitions. Start a
new task after installation so Codex discovers them.
