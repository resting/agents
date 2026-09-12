---
name: unit-test-writing
description: >
  Write and run the unit tests named in a phase test plan, in the project's own
  test framework. Use when the user says "write the tests", "run the tests",
  "make the test plan real", "add the unit tests for phase N", or after test
  scoping finishes. Produces passing tests and a log of what was written, what
  failed, and what was fixed.
metadata:
  version: "0.1.0"
---

# Unit test writing

Turn the named cases into tests. Run them. Fix the tests, not the plan.

Load `unslop` and `open-questions`. Read
`docs/roy_mission_control/09_test_scoper/releases/<version>/phase_N_unit_tests.md`
and the code it names.

## Framework

Use what the project already has: its runner, file layout, naming, fixtures, and
run command. Read two existing test files before writing one. If the project has
no tests, pick the standard runner for the language, add it with the smallest setup
that works, and record the choice in the log.

## Writing

- Work through the plan in priority order. Skip nothing marked high.
- One idea per test. The test name is the case sentence from the plan: "due date
  is null" becomes `test_due_date_is_null`, or the project's equivalent.
- Every module gets at least one failure case. The plan names them; write them.
- Use the fixtures the plan names. If a test needs a mock so thorough that it only
  proves the mock works, skip it and say why.
- Cases under "cover with one integration test instead": write that one test if
  the project already has integration tests. Otherwise log it as skipped.
- Cases under "untestable as written": do not refactor product code to reach them.
  Log them as skipped with the plan's suggested fix.

## Running

Run the whole suite, not just the new files. A failing test is one of three things:

1. A test bug. Fix the test.
2. A product bug with a small, local fix that the reviewed plan clearly intended.
   Fix it, keep the test, and log the file and the reason.
3. Anything else. Leave the test failing. Log it. Report `failed` with the test
   name and what it proves.

Never delete, skip, or weaken a test to make the suite green.

## Output: docs/roy_mission_control/10_unit_test_writer/releases/<version>/phase_N_tests.md

```markdown
# Tests: phase N

Run: `npm test`. Result: 24 passed, 0 failed.

## Written
| Test file | Case | Result |
|-----------|------|--------|
| tests/due.test.ts | due date is null | pass |

## Product fixes
| File | What | Why the test caught it |
|------|------|------------------------|

## Skipped
| Case | Why |
|------|-----|
| report totals across timezones | Untestable as written; plan suggests passing `now` in |
```

## Report

Report `done` through `agent-handoff` when every written test passes and the log
is complete. Report `failed` when a product bug stays open. The captain decides
what happens next.
