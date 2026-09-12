---
name: agent-handoff
description: >
  Use when a roy-mission-control specialist must report progress to the captain, request a user
  conversation, and return completed work for user acceptance. Preloaded by every
  pipeline agent. The captain reads this for the shared report format.
metadata:
  version: "0.6.0"
---

# Agent handoff

When asking the user, prefer the current host's permitted structured-question tool.
Read the [user-question policy](references/user-questions.md) before asking.

The captain runs the mission end to end and remains available throughout. You own
the current stage's work. When information is missing, report it; the captain puts
the question to the user or arranges a direct conversation with you. You never
launch the next stage or pass a gate.

The captain's brief names your version and, from stage 5, your phase. If either is
missing, report the gap. Do not guess.

## Runtime and workspace

Determine the current host before dispatching. In Claude Code, read the
[Claude runtime](references/claude.md). In Codex, read the
[Codex runtime](references/codex.md). In another generated harness, use its
native delegation and question interfaces while preserving the same report and
acceptance rules. The runtime reference supplies launch, direct-conversation, and notification
rules. Follow the current tool schemas and permissions.

The captain applies the role's model and effort through the host's launch interface.
Mentioning them in the specialist's prompt does not configure its model.

The captain supplies three absolute paths: `project_root`, the target checkout;
`mission_root`, exactly `<project_root>/docs/roy_mission_control`; and `plugin_root`,
the installed plugin folder. Paths starting `docs/roy_mission_control/` resolve from
`project_root`. Report output paths starting with a numbered stage folder resolve
from `mission_root`. Bundled role and skill paths resolve from `plugin_root`.
Never write project state into the plugin cache.

## Check before asking

Read the captain's brief, current artifacts, relevant previous definitions, and
recorded user answers. Ask only about missing or conflicting information. Complete
information can come from the current release; a previous release is not required.
If it is enough, finish the work and report `done` without an interview.

On a judgment call after product definition, read
`02_product_owner/releases/<version>/product_definition.md` and cite the principle
you used. A non-blocking question becomes a recorded assumption; keep working.

Use `blocked` for decisions with discrete choices. Use `needs_user` when resolving
the gaps needs a conversation. Record the gaps and why they matter before reporting.
Do not begin an interview on your own. The captain explains the need and arranges it.

If the user visits your interactive specialist session directly, welcome them. Record the active
conversation and its purpose in your draft and report `needs_user` to the captain.
Their message starts the conversation; do not send them away for another approval.
Keep the work within your stage.

## Direct conversation

After reporting `needs_user`, end your turn and leave the session available. This is
a pause for input, not completion. Begin when the user arrives or the captain sends
their choice to talk directly. Do not close the interactive session.

Save each substantive answer, decisions, and remaining topics in your draft and the
question ledger as they change. Keep the inbox `needs` summary current, using the
next report sequence when it changes. Notify the captain again only for completion,
a new blocker, a pause, or a change of conversation mode. This lets the captain help
the user from the files without interrupting the interview.

Ask as many rounds as needed, respecting the runtime's question limit. There is no minimum
round count. Confirm unclear answers; do not invent the user's mission or audience.
Once the gaps are resolved, write the final artifacts, run the stage's checks, and
report `done`. If the user pauses, keep `needs_user` and record what remains.

Tell the user the captain reviews the result and continues the mission from there.
Agreement on wording in your pane does not pass a gate. If the user asks to proceed
here, include that request in the report.

When the delegated run has no direct user channel, return the same report to the
captain and let it relay questions or arrange a supported interactive session. Do not
ask the user directly from that run or promise a conversation view that does not exist.

## Report format

Write to the exact inbox path in your agent definition. All artifact paths are
relative to `docs/roy_mission_control/`. Use the captain's `run_id` unchanged. Increase
`report_seq` with each saved report in that run, starting at 1. A retry gets a new
run ID from the captain; an interview in the same session keeps its run ID.

```yaml
status: needs_user
runtime: <current-host>
transport: <current-transport>
agent: 02-product-owner
version: v0.1
phase: null
run_id: v0.1-02-product-owner-attempt-1
report_seq: 1
output: 02_product_owner/releases/v0.1/product_definition.md
outputs:
  - 02_product_owner/releases/v0.1/product_definition.md
summary: Draft saved; the primary audience is still unclear.
blocking: [OQ-003]
needs: Establish who uses the app and which job they need to finish.
```

`output` is the primary artifact or draft. Use `null` if none exists, never an invented
path. `outputs` lists all written deliverables, including both product documents when
complete. Keep drafts clearly marked. Include relevant evidence in the artifacts.

| Status | Meaning | Extra report content |
|--------|---------|----------------------|
| `done` | Deliverables complete, required checks pass, no unresolved blockers | What is ready and any recorded user feedback |
| `blocked` | A user decision is needed before work can finish | `asks` with question IDs, two to four choices and a recommended default |
| `needs_user` | A conversation is needed, active, or paused | `needs` with missing topics, why they matter, and progress so far |
| `failed` | The stage could not finish | Failure, partial output if any, and a useful recovery step |

Missing release or run information: report the problem back to the captain. Do not
guess identifiers or write into an arbitrary release.

## Notify the captain

Save the artifacts and inbox report first. Then follow the runtime's notification
instructions. Pane sessions use the Herdr report-back workflow. Non-pane sessions
use the runtime's supported return or callback. Delivery failure never erases the
saved report or implies success.

Return the report and actual artifact paths. Do not start the next stage. The captain
reads the saved work, records the gate, and continues or pauses.

## File ownership

Write your stage's artifacts, your inbox report, and relevant question-ledger rows.
Source changes are allowed only where your agent's role permits them: the builder,
code reviewer, and unit test writer. The captain alone writes `mission.md`,
`state.md`, `progress.md`, the gate log, and the artifact register. Report proposed
cross-stage changes to it instead of editing another agent's work. Preserve user
edits and never change a shipped release.
