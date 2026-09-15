---
name: usage-monitor
description: >
  Use when a roy-mission-control captain or specialist starts, resumes, dispatches,
  or works on a stage. Check Codex or Claude Code account usage and save a handoff
  at 90 percent consumed, or when usage cannot be verified.
---

# Usage monitor

Check account allowance before doing mission work. At **90% consumed or more** in
any applicable window, stop substantive work and save a handoff. Missing, stale,
invalid, or unsupported readings also pause the mission. Never interpret them as
zero usage. This rule applies in `auto`, `phase`, `step`, named reruns, interviews,
and inline work. It takes precedence over instructions to finish or advance a stage.

## Check points

- Captain: at the start of each turn, before dispatch, and before any automatic
  transition. Read an incoming pause report and preserve state even if usage is low.
- Specialist: before the first work step, before each later step or tool batch,
  after a long operation, before retrying, and before reporting completion.
- Both: refresh at least every two minutes while active. Check before launching a
  long operation. A running model request cannot be stopped by this skill.

Save progress after each useful step. Ten percent is a reserve, not a guarantee
that the remaining job or even its handoff will fit. Other sessions share allowance.
Do not estimate whether a large job will fit from a percentage alone.

## Read the correct account

Read [the source instructions](references/sources.md). Use the actual host, account,
and allowance bucket for the current model. Do not infer the host or account from
the model's name. Recheck after switching either. Never use Codex readings for a
Claude session or another account's reading because it has more allowance.

The bundled helper is `scripts/usage_monitor.py`, relative to this skill. It emits
JSON with `ok`, `paused_usage`, or `usage_unknown`. A pause exits with code 2.
These are expected outcomes, not reasons to retry work. Use the native Codex app
tool when available; the helper also accepts its raw JSON. It queries the local
Codex CLI when that is the session's account. Each Claude agent runs the helper
through `uv run --script` to read a fresh `/usage` page in a disposable terminal.
A failed helper invocation also means `usage_unknown`; checkpoint and pause.

## Wrap up, then report

On `paused_usage` or `usage_unknown`:

1. Stop starting work, retries, tests, interviews, and new agents. Finish only the
   minimum action needed to leave an in-flight write safe. Do not finish the stage
   or run its remaining checks. Preserve unverified changes as unverified.
2. Save a checkpoint in your own stage folder, named
   `usage_handoff_<run_id>.md`. Follow [the portable handoff](references/handoff.md).
   It must let another agent or model resume without this conversation or session.
   Include version, phase, run ID, runtime, model,
   completed steps, changed files, pending work, checks passed or not run, active
   commands and their real IDs, and the exact next action. Keep existing drafts.
   The captain writes `usage_handoff_captain.md` in its own release folder when it
   is the one pausing, including when no specialist run has started.
3. Save the inbox report with `status: paused_usage`. Include `usage_reason` as
   `threshold` or `unavailable`, the helper result or equivalent native reading in
   `usage`, and the saved path in `checkpoint`. Keep normal run ID and sequence
   rules. Include the checkpoint in `outputs`; do not invent a completed artifact.
4. Notify the captain through the existing runtime channel, then end the turn.
   If notification fails, keep the saved report. Do not spend the reserve retrying
   indefinitely. Never edit the captain's state as a specialist.

The captain stops dispatch, requests that any active specialist checkpoint through
its existing channel, and waits for that writer to stop. It records `paused_usage`
and the checkpoint in state and progress before telling the user. The captain must
follow this rule for its own allowance even if the specialist uses another account.
If the specialist cannot report, record the last saved state and that its latest
work is unconfirmed. Do not mark its gate passed.

Tell the user what was saved, what remains, which window is low or unavailable, and
its reset time in their timezone. Use Asia/Singapore for this user's missions.
Keep check timestamps as Unix seconds. Preserve Claude reset labels as shown. Ask the user to choose what happens next.

## Resume requires the user

The pause stays recorded after an allowance reset, session restart, or a later
`done` notification. A status request never resumes it. `go` after a usage pause
requests a fresh check and resumption of the saved step. Resume only if all
applicable readings are available and below 90%. If not, explain why it stays paused.
The user may choose to wait, repair monitoring, or switch to another available
account or host. Reconcile the old writer and saved artifacts before switching.
Never silently switch models, buy credits, consume a reset, or bypass monitoring.
Only an explicit user instruction can change this policy; record its scope.

Read the checkpoint on resume. Confirm the previous writer stopped, allocate a new
run ID for a stopped run, and link the old checkpoint in the brief. Resume the
unfinished step. Do not replay completed work or pass incomplete gates.
The captain may assign any suitable replacement agent or model. Follow the portable
handoff's transfer and recovery checks; the original session is never required.
