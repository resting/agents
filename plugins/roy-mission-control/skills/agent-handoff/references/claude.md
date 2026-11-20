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

## Delegation

Use Claude's Task or Agent tool with `runtime: claude` and
`transport: claude-task`. The captain relays specialist questions and resumes the
same stage with the saved answers. Use the host's completion or wait mechanism.
Keep the saved inbox report available if notification fails.

## The roster

| Agent | Model | Effort |
|-------|-------|--------|
| `01-design-intake` | opus | medium |
| `02-product-owner` | opus | high |
| `03-release-scoper` | opus | high |
| `04-phase-scoper` | opus | high |
| `05-plan-writer` | opus | high |
| `06-plan-reviewer` | opus | xhigh |
| `07-builder` | sonnet | high |
| `08-code-reviewer` | opus | high |
| `09-test-scoper` | opus | medium |
| `10-unit-test-writer` | sonnet | medium |
| `11-manual-test-writer` | sonnet | low |

This table matches the agents' frontmatter. Apply model and effort through the
host's supported launch options, and say both in the brief.

`CLAUDE_CODE_SUBAGENT_MODEL` overrides this table for Task-tool dispatch. If it is
set, say so once and stop quoting the table.


## Specialist notification

Return the inbox report as the final response and print `RMC_END` as the last line.
The captain relays questions and resumes the same stage with the saved answers.
