---
name: code-review
description: >
  Review code that was just built against its plan, cut what is not needed, close
  edge cases, resolve undecided behaviour, and verify the final diff. Use this skill whenever the user says "review the code", "review what you
  built", "tighten this code", "is this too complex", "check this before I merge", or
  after any build phase finishes. Runs after build execution, before test scoping.
metadata:
  version: "0.1.1"
---

# Code review

When asking the user, prefer `AskUserQuestion`.
Read the [user-question policy](../agent-handoff/references/user-questions.md) before asking.

Review the phase diff. Cut before you critique. Finish with the verification pass
below, using the current host's tools.

Load `unslop` and `open-questions`. Read `docs/roy_mission_control/06_plan_reviewer/releases/<version>/phase_N_reviewed.md` and
`docs/roy_mission_control/07_builder/releases/<version>/phase_N_log.md`. Diff the phase against its starting point.

Load `agent-handoff` for questions, reports, and user conversations. Report gaps to
the captain before asking the user. Only the captain records gate acceptance and
starts the next stage.

## Eight passes

### 1. Delete
Read every added file and ask what breaks if it goes. Delete unused exports, dead
branches, commented-out code, unused imports, unreachable error handling, helpers with
no caller, and any file the plan did not ask for.

### 2. Duplicate
Two functions doing the same thing with different names. Logic copied between a route
and a component. Validation written twice. A helper that already exists upstream.

### 3. Complexity
Flag functions over about 50 lines, nesting past three levels, more than four
positional arguments, boolean arguments that switch behaviour, and any function whose
name needs "and" in it. Each of these is a split, not a comment.

### 4. Against the plan
Every plan step landed. Every deviation in the build log is defensible. Nothing shipped
that the plan excluded.

### 5. Edge cases
Same list as the plan review, checked against real code this time: zero, one, many.
Missing data. Bad input. Slow and failed network. Double submit. Concurrency. Partial
writes. Permissions. Back button and refresh. Time and timezones.

For each hit: fixed here, filed as an open question, or written down as an accepted
risk. No fourth option.

### 6. Errors
Every failure path either recovers or tells the user something true. No swallowed
exceptions. No `catch` that logs and continues into broken state. No error message that
leaks a stack trace to a user or hides the cause from a developer.

### 7. Names and comments
Names say what the thing is. Comments say why, never what. Apply `unslop` to every
comment, log line, and error string.

### 8. Security basics
Input validated at the boundary. No secrets in code or logs. Authorisation checked on
the server, not only in the UI. Queries parameterised. User content escaped on output.

## Output: docs/roy_mission_control/08_code_reviewer/releases/<version>/phase_N_review.md

```markdown
# Code review: phase N

Diff: 14 files, +820 / -110. After review: 11 files, +540 / -180.

## Must fix
| # | File:line | Finding | Fix |
|---|-----------|---------|-----|
| 1 | src/routes/tasks.ts:42 | No length limit on title, writes straight to the database | Cap at 200, reject with 400 |

## Should fix
| # | File:line | Finding | Why it can wait |

## Cut
| File:line | What | Why |

## Notes
Things worth knowing, no action.

## Questions for the user
OQ IDs and the one-line reason each one matters.

## Final verification
Method used, checks run, remaining findings, and their disposition.
```

## Then act

1. Apply every Must fix.
2. Re-run the phase verification from the plan.
3. Report decisions needed on the Should fix list and open questions to the captain.
   During an arranged conversation, ask up to four at a time through `open-questions`.
4. Re-read the final changed code against the reviewed plan. Check that each must-fix
   item is resolved and the phase's required checks pass. Record the actual method
   and evidence.

   An installed, distinct `/code-review low` command may supply this check.
   Do not recursively invoke this skill or claim a missing external command ran.
   Repeat only after a new fix or a failed check.

## Gate

Report readiness when must-fix items are applied, phase verification passes, and
the final verification has no unresolved must-fix finding. The captain presents the result, records acceptance,
and handles the handoff to test scoping.
