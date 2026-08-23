---
name: phase-writer
description: Write the phase breakdown for a release and hand each phase to implementation-plan-writer. Use when phase-planner's breakdown has been agreed, when the user asks to record the phases, or when they ask what to plan or build next in a release. Writes one index file and dispatches steps 5 and 6.
---

# Phase writer

Record the phases of a release, then hand them out one at a time. This file is
what steps 5 and 6 run from.

## Rules

1. **One file.** `docs/mission-control/phases/<version>/_index.md`.
   Never the scope, the feature list, the index, or a plan body.
2. **Never write a plan yourself.** `roy-agents:implementation-plan-writer`
   writes plan bodies. You write the row that points at one.
3. **Never build anything.** `roy-agents:plan-implementer` builds.
4. **One phase at a time.** Dispatch, wait, update the row, then the next.
5. **Status words are fixed:** `unplanned`, `planned`, `building`, `built`.
   Nothing else. No percentages, no "mostly done".
6. **Evidence, not guesswork.** Set `planned` when the plan file exists. Set
   `built` when the work is done and the user says so. If you cannot tell,
   leave the row alone and say which one.
7. **Rerunning changes nothing.** Update rows in place. Never append a second
   table.

## Steps

### 1. Write the index

```markdown
# v0.1 phases

Updated 2026-08-22.

| # | Phase | Covers | Needs | Status | Plan |
| --- | --- | --- | --- | --- | --- |
| 01 | Storage and accounts | ACC-01, ACC-02 | - | built | 01-accounts.md |
| 02 | Transaction entry | TXN-01, TXN-11 | 01 | building | 02-transactions.md |
| 03 | Categories | CAT-01 | 02 | planned | 03-categories.md |
| 04 | Spending report | RPT-02 | 03 | unplanned | |

## What each phase ends at

- 01 - you can add an account and see it in a list
- 02 - you can record money against an account and see a balance
- 03 - you can sort spending into categories
- 04 - you can see where a month went
```

Rows in build order. The Plan column holds the filename only. It lives in
`docs/mission-control/plans/<version>/`. Filenames are `NN-slug.md` with no
date prefix, so the folder sorts by build order.

Check every ID in `scope.md` appears in exactly one row before saving. If one
does not, stop and say which.

### 2. Hand a phase to implementation-plan-writer

Only after the release has a design, or after the user has said the release
needs none. A plan written before the design gets rewritten.

Dispatch `roy-agents:implementation-plan-writer` with a prompt it can act on
cold. It has none of this conversation.

```
Write the implementation plan for phase 02 of v0.1.

Output path: docs/mission-control/plans/v0.1/02-transactions.md
Use that exact path. It replaces the usual docs location and datetime prefix.

Covers: TXN-01, TXN-11
Read for context:
  docs/mission-control/releases/v0.1/scope.md
  docs/mission-control/phases/v0.1/_index.md
  docs/mission-control/designs/v0.1/design.md
The design doc holds the canvas URL. Read the canvas artifact for the screens
this phase builds, and the doc for what the canvas does not show. Build what is
designed. If the design and this phase disagree, say so rather than choosing.
Depends on phase 01, already built. Its plan is 01-accounts.md.

This phase ends when a person can record money against an account and see a
balance. Do not plan beyond that.
```

Set the row to `planned` once the file exists.

### 3. Hand a phase to plan-implementer

Only after its plan exists and any phase it needs is `built`.

```
Implement docs/mission-control/plans/v0.1/02-transactions.md
```

Set the row to `building` when it starts and `built` when the user confirms it
works.

### 4. Report

What moved, then the counts. Not the table.

```
Moved: 02 planned to building.

v0.1: 1 built, 1 building, 1 planned, 1 unplanned.

Next: 03 has a plan and 02 is nearly done.
```

If nothing moved, say so in one line and write nothing.

<!-- END OF INSTRUCTIONS -->

## Notes

Context only. Skip unless you are stuck.

Steps 5 and 6 come from the `roy-agents` plugin. If those agents are missing,
say so rather than writing or building the plan yourself.

`implementation-plan-writer` normally names files with a datetime prefix and
drops them at the top of `docs/`. The explicit output path in the dispatch overrides that, which
is why the path has to be in every dispatch and not left implied.

Dispatching two phases at once looks faster and is not. The second plan gets
written against a codebase that the first one is still changing.
