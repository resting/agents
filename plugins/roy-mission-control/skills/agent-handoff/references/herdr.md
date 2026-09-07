# Herdr pane workflow

Use this only when the captain is running inside Herdr. Every specialist starts
in a sibling pane below the captain. Keep focus on the captain.

## Check the calling session

Before controlling Herdr, check that `HERDR_ENV=1`. If it is unset, do not
control another focused Herdr session. Use the current host's non-pane fallback.

Inside Herdr, inspect the installed CLI with `herdr --help`, `herdr pane`, and
`herdr agent`. If Herdr is missing or a control call fails, report the failure.
Do not silently substitute another transport and claim a pane opened.

## Start a specialist below the captain

1. Read the caller with `herdr pane current --current` and record its pane ID.
2. Run the bundled helper from the mission checkout:

   ```bash
   python3 "<plugin-root>/skills/agent-handoff/scripts/herdr-split-down.py" --cwd "$PWD"
   ```

   The helper fixes `--current --direction down --no-focus`. If it fails, inspect
   the layout before retrying. Never retry to the right.
3. Start the current host in the returned pane. Use `--kind claude` for Claude
   Code or `--kind codex` for Codex. Apply the selected agent's model settings
   through options supported by that host.
4. Wait for readiness. Record the real pane ID, agent name, runtime, transport,
   and requested settings.
5. Send a bounded stage brief with the project, mission, plugin, role, skill,
   input, output, report, release, phase, run, and captain-pane paths or IDs.
6. End with one status line naming the specialist and pane.

Use argument arrays or safe quoting so user text remains data. Do not launch a
native subagent as well. Reuse the saved pane for interviews and follow-ups.

## Report to the captain

Write artifacts and the inbox report first. Then notify the known captain pane:

```text
herdr agent prompt <captain-pane-id> "RMC_END <role> <version> <run_id> <report_seq> <status>"
```

Print `RMC_END` as the specialist's final line as a visible fallback. Keep the
session open for `needs_user`. If notification fails, preserve the report and
say delivery failed.

Inspect stalled panes with `herdr agent get` and `herdr agent read`. A permission
prompt, an idle process, and completed work are different states. Never pass a
gate from terminal status alone.
