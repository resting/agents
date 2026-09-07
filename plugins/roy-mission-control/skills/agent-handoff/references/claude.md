# Claude runtime

Use this reference only inside Claude. The captain uses the launch instructions;
specialists only use the notification instructions. Keep the shared stage, report,
and user-acceptance rules from `captain` and `agent-handoff`.

## Capabilities and paths

Load skills through Claude's Skill tool or read their files. Agent `skills` frontmatter
preloads the listed skills. Resolve bundled files against the installed plugin root,
using `CLAUDE_PLUGIN_ROOT` when supplied. Never use a plugin-cache folder as the user's
mission workspace.

For user questions, follow the shared [user-question policy](user-questions.md).
Prefer `AskUserQuestion` for choices, open-ended context, and stage acceptance.
Use its custom-answer input when the user needs their own words. Respect its
current schema and limits. A default option is not an answer.

## The bottom pane

Inside Herdr, follow [Herdr pane workflow](herdr.md). Split down and start the specialist
with `--kind claude`, then the named Claude agent and roster options after `--`.
Use `runtime: claude` and `transport: claude-pane`. Follow the shared pane direction,
saved IDs, direct-conversation rules, and report-back sequence.

Outside Herdr, use Claude's Task or Agent tool with `transport: claude-task`. Tell the
user that questions will come through the captain. An in-Herdr launch failure requires
inspection and an explicit choice before changing to a non-pane fallback.

### Notifications and permissions

Agents have Bash available to send their captain notification. Tool access and action
permissions are separate. Use the project's existing permissions; do not widen them
silently. If a required notification is denied, the saved inbox remains the fallback.
Every user message to the captain triggers an inbox check.

At mission setup in Herdr, explain and offer the existing project's optional
`Bash(herdr:*)` allow rule if notifications need it. This rule allows Herdr commands;
do not call it permission for only one message. Merge an accepted rule into existing
settings without replacing them. Declining it keeps inbox-based recovery available.

Auto mode availability depends on the installed Claude version, model, and settings.
If a pane is quiet, inspect its status and any permission prompt before declaring a
failure. Auto mode does not replace product questions or the captain's user gates.
Do not switch to a permission-bypassing mode to make a handoff work.

## The roster

| Agent | Model | Effort |
|-------|-------|--------|
| `01-design-intake` | opus | medium |
| `02-product-owner` | opus | high |
| `03-release-scoper` | opus | high |
| `04-phase-scoper` | opus | high |
| `05-plan-writer` | opus | high |
| `06-plan-reviewer` | opus | xhigh |
| `07-builder` | sonnet | medium |
| `08-code-reviewer` | opus | high |
| `09-test-scoper` | opus | medium |
| `10-manual-test-writer` | sonnet | low |

Say model and effort in the brief. Pass `--model` and supported `--effort` from this table.

`CLAUDE_CODE_SUBAGENT_MODEL` overrides this table for Task-tool dispatch. If it is
set, say so once and stop quoting the table.


## Specialist notification

For `claude-pane`, follow the shared Herdr workflow's notification steps. Keep the
interactive session open on `needs_user`. For `claude-task`, return the inbox report
as the final response and print `RMC_END` as the last line. The captain relays questions
and resumes the same stage with the saved answers.
