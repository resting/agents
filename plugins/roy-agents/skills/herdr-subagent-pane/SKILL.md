---
name: herdr-subagent-pane
description: "Run every Claude Code subagent in its own Herdr pane. Use this whenever you are about to spawn, delegate to, or create a subagent (Agent tool, --agent, .claude/agents/*.md), even if the user never says Herdr. Reads model and effort from the agent definition. Loads the herdr skill for all pane and agent commands. Requires HERDR_ENV=1."
---

# Herdr subagent pane

One subagent, one pane. The user watches it work. Focus stays put.

Load the `herdr` skill first. It owns the command syntax. This skill only says what to pass.

## Guard

```bash
test "${HERDR_ENV:-}" = 1
```

If this fails, use the normal Agent tool and say so in one line.

## Ask once

Before the first split in a session, call `AskUserQuestion`. Do not ask in plain text.

- question: "Where should the subagent pane go?"
- header: "Split"
- options: `Down` (below the current pane), `Right` (beside the current pane)
- multiSelect: false

Map the pick to `down` or `right`. Keep it for the whole session.

## Steps

1. Find the agent file. `.claude/agents/<name>.md`, then `~/.claude/agents/<name>.md`.
2. Read `model:` and `effort:` from its frontmatter. Drop a flag if the key is absent or `inherit`.
3. Split with `herdr pane split --current --direction <down|right> --cwd "$PWD" --no-focus`. Take the pane ID from the JSON.
4. Start with `herdr agent start <name> --kind claude --pane <id> -- --agent <name> --model <model> --effort <effort>`.
5. Send the task with `herdr agent prompt <name> "<task>" --wait --timeout 600000`.
6. Read the result with `herdr agent read <name> --source recent-unwrapped --lines 120`.
7. On `blocked`, run `agent get` and `agent read`. Ask the user before answering the dialog.

## Rules

- Direction comes from the user. Do not read layout to pick one.
- Agent name is the subagent's own name. Add `-2`, `-3` if it is already live. Check with `herdr agent list`.
- Two subagents at once: split the first subagent pane, not the caller again.
- Close a pane only if you made it and the agent is done.
- No definition file: start plain `claude`, pass the task as the prompt, tell the user.
