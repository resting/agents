---
name: plan-review
description: >
  Review an implementation plan to cut it down, remove duplication, close edge cases,
  and grill the user on anything still undecided. Use this skill whenever the user
  says "review the plan", "tighten this plan", "is this plan too big", "poke holes in
  this", "what am I missing", or after any implementation plan is written. Produces
  the reviewed plan the builder works from.
metadata:
  version: "0.1.2"
---

# Plan review

Cut first. Question second. Approve last.

Load `unslop` and `open-questions`. Read `docs/roy_mission_control/05_plan_writer/releases/<version>/phase_N.md`, the phase
definition, and the current code.

## Six passes, in order

### 1. Deletion
Go step by step and ask what happens if this is removed. Target a 20 to 40 percent
cut. Delete on sight:
- Steps for features not in this phase
- Abstractions with one caller
- Config, flags, and options for values that never change
- Error handling for errors that cannot happen
- Logging nobody will read
- Wrappers that only rename something

### 2. Duplication
Same logic planned in two places. A new helper that already exists in the codebase.
Two steps that touch the same file for the same reason. Merge them.

### 3. Contracts
Every interface has argument types, a return type, named error cases, and at least
one named caller. Anything failing that check gets deleted or fixed.

### 4. Edge cases
Walk this list against every step. Each hit is either handled in the plan or filed as
an open question.

- Zero, one, many. Empty list, single item, 10,000 items.
- Missing data. Null, undefined, empty string, absent field.
- Bad input. Wrong type, too long, wrong format, hostile input.
- Slow and failed network. Timeout, retry, partial response, offline.
- Double submit. The user clicks twice. Two tabs. A retried request.
- Concurrency. Two writes to the same row. A read during a write.
- Partial writes. Step 2 of 3 fails. What state is left behind.
- Permissions. Not logged in, logged in as someone else, session expired.
- Navigation. Back button, refresh mid-flow, a deep link into step 3.
- Time. Timezones, daylight saving, clock skew, expiry at the boundary.

### 5. Verification
Every step has a runnable check. Rewrite any that say "confirm it works". The phase
verification must be runnable by someone who did not write the plan.

### 6. Questions
Everything unresolved becomes an open question with a recommended default. Follow the
`open-questions` rules: up to four per round, defaults included, blocking marked.

## Output: docs/roy_mission_control/06_plan_reviewer/releases/<version>/phase_N_reviewed.md

The full revised plan, plus this header:

```markdown
## Review summary
Steps: 14 to 9. Files: 11 to 7.

### Cut
| What | Why |
|------|-----|
| Step 6, generic adapter interface | One caller, one implementation |

### Added
| What | Why |
|------|-----|
| Step 4b, reject duplicate titles | Edge case, double submit |

### Blocking questions
OQ-014, OQ-017. The plan is not buildable until these close.
```

## Grilling style

Direct, specific, one line of context each. Never ask a question the plan already
answers. Never ask for permission to be thorough, just be thorough. If the user gives
a vague answer during an arranged conversation, name the remaining ambiguity.
Keep blocking questions open until answered. Record assumptions only for questions
marked non-blocking.

## Report

Report `done` when blocking questions are closed and every step is verifiable, with
the cut summary for the captain to show. Report `blocked` while a blocking question
is open; the captain puts it to the user and resumes you. The captain hands the
reviewed plan to the builder.
