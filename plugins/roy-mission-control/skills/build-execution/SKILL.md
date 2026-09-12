---
name: build-execution
description: >
  Build code from a reviewed implementation plan, one step at a time, verifying after
  each. Use this skill whenever the user says "build it", "implement the plan",
  "start phase 2", "write the code for this plan", or hands over a reviewed plan and
  expects working code. Runs after the plan review, before the code review.
metadata:
  version: "0.1.2"
---

# Build execution

Follow the plan. Verify each step. Change nothing outside it.

Load `unslop` and `open-questions`. Read `docs/roy_mission_control/06_plan_reviewer/releases/<version>/phase_N_reviewed.md`. If only
the unreviewed plan exists, stop and say the review has not run.

## The loop

For each step in the plan:

1. Read the files the step names.
2. Make the change.
3. Run the step's verification.
4. Pass: log it and move on. Fail: fix it. Fail twice: stop and report.

Do not batch steps. Do not run ahead to step 5 because it seems obvious.

## Stop conditions

Stop and report to the captain when:

- A step is ambiguous enough that two builders would do different things.
- Verification fails twice for the same reason.
- The plan contradicts what the code actually does.
- The change needs a file the plan does not list.
- A dependency is missing, out of date, or has a different API than the plan assumes.

When you stop, say which step, what you found, and the two or three ways forward with
a recommendation. File it as an open question if the user needs to decide.

## Scope discipline

Build what the plan says. Nothing adjacent. When you spot something worth doing that
is not in the plan, write it to `docs/roy_mission_control/00_captain/releases/<version>/open_questions.md` and keep going.

Do not add, even when it seems free:
- Abstractions with one caller
- Options, flags, or config for values that never change
- Error handling for impossible errors
- Placeholder functions for later phases
- Reformatting of files you are not otherwise changing

## Code style

- Match the surrounding code. Its conventions beat your preferences.
- Name things after what they are. No `data`, `info`, `handler2`, `utils`.
- Comments explain why, never what. Apply `unslop` to comments too.
- Delete code you replace. No commented-out blocks.
- Commit per step, present tense, plain words: "add tasks table", not "feat: implement
  comprehensive task persistence layer".

## Output: docs/roy_mission_control/07_builder/releases/<version>/phase_N_log.md

```markdown
# Build log: phase N

| Step | Files | Verification | Result | Note |
|------|-------|--------------|--------|------|
| 1 | src/db/schema.ts | npm run db:migrate | pass | |
| 2 | src/routes/tasks.ts | curl POST /tasks returns 201 | pass | |
| 3 | src/ui/list.tsx | click path in plan | pass | Used existing Row component, plan said new |

## Deviations from the plan
| Step | Plan said | I did | Why |

## Found but not built
Anything spotted outside the plan. Open question IDs.
```

## Report

Report `done` when every step and the whole phase pass verification, with the
results in the build log. The captain continues to code review. A stop condition is
a `blocked` or `failed` report, and the captain pauses for the user.
