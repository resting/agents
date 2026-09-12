---
name: test-scoping
description: >
  Decide which parts of the code deserve unit tests and name the cases for each. Use
  this skill whenever the user says "what should we test", "can we unit test this",
  "write a test plan", "add automated tests", "is this testable", or after a code
  review finishes. Produces the unit test plan that stage 10 writes and runs.
metadata:
  version: "0.1.2"
---

# Test scoping

Find the logic worth testing. Name the cases. Say plainly what is not worth it.

Load `unslop` and `open-questions`. Read the phase code and
`docs/roy_mission_control/08_code_reviewer/releases/<version>/phase_N_review.md`.

## Worth a unit test

- Pure functions with rules in them. Pricing, scoring, eligibility, sorting.
- Parsers, formatters, serialisers. Anything converting between shapes.
- Money, dates, durations, units, timezones. These break quietly.
- Permission and access checks.
- State machines and status transitions.
- Validation logic.
- Boundary logic. Limits, pagination, truncation, retries.
- Anything that already had a bug. A bug is proof the case is reachable.

## Not worth a unit test

- Thin wrappers that call one library function.
- Framework glue. Route registration, dependency wiring, config loading.
- Layout and styling.
- One-line getters and setters.
- Code you already plan to rewrite next phase.
- Anything a mock would have to fake so thoroughly that the test only proves the mock
  works.

Write the second list down. Naming what you skipped is part of the plan, not a gap
in it.

## Output: docs/roy_mission_control/09_test_scoper/releases/<version>/phase_N_unit_tests.md

```markdown
# Unit test plan: phase N

## Unit tests
| Module | Function | What the test proves | Cases | Fixtures needed | Priority |
|--------|----------|---------------------|-------|-----------------|----------|
| src/lib/due.ts | isOverdue | Due dates compare correctly across timezones | due yesterday, due today, due in an hour, null due date, UTC vs local | frozen clock | high |

## Cover with one integration test instead
| Path | Why a unit test is the wrong shape |
|------|-----------------------------------|
| Create task through the API and read it back | Crosses route, validation, and database. Mocking all three proves nothing |

## Not testing
| Code | Why |
|------|-----|
| src/routes/index.ts | Route registration, a test would only re-state the file |

## Untestable as written
| Code | Problem | Smallest fix |
|------|---------|--------------|
| src/lib/report.ts | Reads the clock and the database inside the calculation | Take `now` and the rows as arguments, move the fetching out |

## Suggested order
Highest priority first, with a rough count. Aim for the smallest set that would have
caught the bugs found in this phase's code review.
```

## Rules

- Every case is a sentence a person can read: "due date is null" beats "case 4".
- Include at least one failure case per module. Tests that only prove the happy path
  give false confidence.
- Name the fixture or fake each test needs. If the list is long, that module is the
  wrong shape, and it belongs under "untestable as written".
- Do not propose a coverage percentage. Name the modules instead.

## Who writes the tests

Stage 10, `unit-test-writing`, writes and runs the tests from this plan. Write the
plan so it can: name the module, the function, the case as a sentence, and the
fixture. A case it cannot locate from the plan will be skipped.

## Report

Report `done` through `agent-handoff` with the plan path. The captain continues to
stage 10, which writes and runs the tests.
