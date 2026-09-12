---
name: implementation-planning
description: >
  Write a step-by-step implementation plan for one phase, with files, contracts, and
  a verification command for every step. Use this skill whenever the user says
  "write the plan", "plan phase 2", "implementation plan", "how do we build this",
  "spec out the work", or hands over a phase and asks for detail before coding.
  Runs after phase scoping, before the plan review.
metadata:
  version: "0.1.2"
---

# Implementation planning

One plan per phase. Detailed enough that someone else could build it and get the
same result.

Load `unslop` and `open-questions`. Read `docs/roy_mission_control/04_phase_scoper/releases/<version>/phases.md` and the release
scope. Read the existing codebase before planning changes to it.

## Hard rules

1. Every step names the files it touches, with paths.
2. Every step ends with a verification that a machine or a person can run. A command,
   a test, or a click path. "It works" is not verification.
3. Contracts come before the code that uses them. Types, function signatures, request
   and response shapes, error cases, all decided in writing first.
4. No step should take more than one sitting. Split anything longer.
5. Plan nothing you cannot verify. If you cannot say how to prove a step is done,
   the step is wrong.
6. Do not plan abstractions with one caller. Do not plan config for a value that
   never changes. Do not plan interfaces for a second implementation nobody asked for.

## Output: docs/roy_mission_control/05_plan_writer/releases/<version>/phase_N.md

```markdown
# Phase N plan: <name>

## Goal
One sentence. What runs at the end.

## In scope
Features from the release scope, by ID.

## Out of scope
Named, so the builder does not drift. Include the tempting adjacent work.

## Files
| Path | New or changed | What changes |
|------|----------------|--------------|
| src/db/schema.ts | changed | add tasks table |
| src/routes/tasks.ts | new | create and list endpoints |

## Data model
Tables or types, with fields, types, nullability, defaults, and indexes. Say what
happens to existing rows if this is a change.

## Contracts
For each interface: signature, inputs with types, output, error cases, and who calls
it. An interface with no named caller does not get planned.

## Steps
### Step 1: <name>
Files: src/db/schema.ts
Do: add the tasks table with id, title, status, created_at.
Verify: `npm run db:migrate && npm run db:check` exits 0 and the table exists.

### Step 2: ...

## Verification for the whole phase
The click path or command that proves the phase goal. Written so a person who did not
build it can run it.

## Rollback
How to undo this phase if it goes wrong. Migration down, feature flag, or revert.

## Risks
| Risk | Likelihood | What it breaks | What to do |

## Open questions
Blocking IDs from docs/roy_mission_control/00_captain/releases/<version>/open_questions.md. The plan is not final while any are open.
```

## Verification patterns

- Backend: a curl or test command with the expected status and body shape.
- Database: a migration command plus one query that must return rows.
- UI: a click path with the exact expected text on screen.
- Build: the build command exits 0 with no new warnings.

## Before handing off

Check the plan against the phase definition. Every feature in the phase appears in
at least one step. Every step has files and a verification. Report the plan through
`agent-handoff`. The captain continues to plan review.
