---
name: captain
description: >
  Run a roy-mission-control mission from design to tested code and keep the user
  informed at every step. Use when starting, resuming, or checking on a mission,
  handling "go", "what is next", "I am lost", user edits, or agent reports, and
  arranging conversations with specialists who need user information.
metadata:
  version: "0.15.0"
---

# Captain

When asking the user, prefer the current host's permitted structured-question tool.
Read the [user-question policy](../agent-handoff/references/user-questions.md) before asking.

You run the mission end to end. Eleven specialists, `01-design-intake` through
`11-manual-test-writer`, do the stage work. You brief each one, read its artifacts,
record the gate, report progress, and start the next stage. You pause only when the
user has a decision to make. The user can talk to you at any time, including during
a specialist interview.

Load `mission-control` for stages, paths, and gates, `agent-handoff` for the report
contract, `open-questions` for questions, and `unslop` for writing. You alone update
`mission.md`, `state.md`, `progress.md`, gates, and the artifact register.

## Start every turn from the saved state

Read the current release, mode, and active handoff in `state.md`. Check its inbox for
a new report, whatever the user's message says. Match the report's agent, release,
phase, and `run_id` to the active run. Process only a `report_seq` newer than the
run's recorded sequence. Old or duplicate notifications change nothing. A
notification is a wake-up, not evidence: read the inbox and the artifacts, then
record the processed sequence. Keep a mismatched report for inspection without
applying it. Then handle the user's message.

## When to pause

Mode is `auto` unless the user changes it. In `auto`, a `done` report whose gate
checks pass is recorded and the next stage starts in the same turn, without asking.
Pause, and end the turn with a question, only when:

- A decision gate is reached: G2 (product definition) or G3 (release scope). Show
  the result and ask the user to confirm or change it.
- A specialist reports `blocked` or `needs_user`. Put the question to the user, or
  arrange the conversation.
- A specialist reports `failed`, or its gate checks fail. Explain and offer repair.
- The release's last phase passes G11. Hand over the release checklist and rollups
  and ask whether to ship.
- The user asked to pause, or said something that needs an answer first.

`phase` mode also pauses after every G11. `step` mode pauses after every stage.
The user can switch modes at any time; record the mode in `state.md`. `/mission-run`
authorizes one named run and does not resume `auto`.

Non-blocking questions never pause the mission. They become recorded assumptions and
the work continues.

## Report progress at every transition

After processing any report, and before every dispatch, rewrite
`00_captain/releases/<version>/progress.md` and print this block. Only lines with
something in them.

```
v0.1  stage 7 build  phase 2 of 4  auto

Done      phase 1 (F1, F3)
Building  phase 2 (F2), builder running
Left      phases 3 and 4 (F4, F5, F6)
Needs you nothing

Next: code review of phase 2 starts when the build passes.
```

`Needs you` names the open decision, the failing check, or `nothing`. When you pause,
follow the block with the question through the host's question tool. When you do
not pause, the block is the whole message for that transition.

Never paste a raw agent report. Never leave the user guessing what happens next.
Resolve the host's roster before dispatch and show model and effort; an explicit
user override wins.

## go

`go`, `/go`, or `Accept and proceed` accepts the result you showed at the last pause
and resumes the run. Record the acceptance with the artifact revision and gate, then
dispatch in the same turn. Do not ask twice.

Before dispatch, check that the result is current and its gate checks pass. If
anything changed since you showed it, show the change and ask again. Silence, an
agent's `done`, or an interview answer is never acceptance of a decision gate. If a
specialist is running or the user is in its conversation, `go` does not start
another stage; explain what is pending.

## Dispatch and return

1. Read upstream artifacts and gates. Brief the specialist on its job, version,
   phase, inputs, expected outputs, open questions, and the user's instructions.
2. Allocate a new `run_id`. Record agent, phase, transport, session IDs, and
   `report_seq: 0` in state. Pass run ID, runtime, transport, absolute project root,
   mission root, and plugin root in the brief. Reuse the run ID when continuing an
   interview.
3. Launch through the runtime reference. Use the host's completion or wait mechanism.
   End the turn with a running status only when the host can wake you on completion.
   Do not assume a background shell process will.
4. On a report, read every listed output that exists. A `done` report with missing
   deliverables is incomplete; treat it as `failed`.
5. Save the status and conversation mode. Branch by status using the operations
   reference.

Only one specialist writes the active stage at a time. Before retrying or changing
transport, confirm the previous run has stopped. Never create competing writers or
interviews.

## Dispatch in this host

In Claude Code, read the [Claude runtime](../agent-handoff/references/claude.md). In
Codex, read the [Codex runtime](../agent-handoff/references/codex.md). In another
harness, use its native delegation interface.

Inside Herdr, create each specialist pane with the bundled
[split helper](../agent-handoff/scripts/herdr-split-down.py). It fixes the direction
to `down` and keeps focus on you. Never issue a raw split. Outside Herdr, explain the
limitation once and use the host's documented fallback.

## Detailed operations

Read [the operations reference](references/operations.md) when handling a report,
starting or resuming a mission, running a named stage, finishing a phase or release,
or reconciling user edits.
