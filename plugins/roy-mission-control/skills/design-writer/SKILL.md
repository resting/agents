---
name: design-writer
description: Record the design for a release, pairing the Claude Design canvas with the decisions a canvas cannot show. Use once a release scope exists and before any implementation plan is written, when the user asks to design a release, or when a design has been made and needs writing down. Writes one design doc per release.
---

# Design writer

A release gets one design, not one per phase. The screens belong to the
release; the phases are only the order they get built in.

The canvas is made in Claude Design. You write down what the canvas cannot
show, and where the canvas lives.

## Rules

1. **One file.** `docs/mission-control/designs/<version>/design.md`.
   Never the scope, the feature list, the index, a phase index, or a plan.
2. **Never design anything yourself.** The `design` skill makes the canvas. You
   record it.
3. **The canvas is the source of truth for what a screen looks like.** Never
   describe layout, colour or spacing in this doc. If it is visible on an
   artboard, link to it instead of retelling it.
4. **This doc is the source of truth for what a canvas cannot show.** Empty
   states nobody drew, error behaviour, what happens on slow networks, what a
   person sees the very first time.
5. **Refer to features by ID.** Every screen names the features it serves.
6. **Every question goes through AskUserQuestion**, so the user can select an
   option instead of typing a letter. Never present options as plain text.
7. **No implementation detail.** What a person sees and does, not how it gets
   built. That is step 5.

## Steps

### 1. Read the scope

Read `docs/mission-control/releases/<version>/scope.md`. That is what the
design has to cover. Read the source sections only for features you cannot
place on a screen.

If a design doc already exists for this version, ask through AskUserQuestion
whether to replace it, add to it, or leave it alone.

### 2. Make the canvas

Invoke the `design` skill, seeded from the release scope. One canvas per
release, one artboard per screen.

If the `design` skill is not available, say so and stop. Do not draw screens in
markdown as a substitute.

Wait for the user to refine and save it, then take the published artifact URL.

If the release has no interface worth designing, say so, write nothing, and
send the user to step 5.

### 3. Ask for what the canvas cannot show

One AskUserQuestion call. Ask only what the artboards leave open, and only what
changes what a person sees.

Typical gaps: what an empty list says, what happens when something fails, what
a person sees before any data exists, what is hidden rather than disabled.

### 4. Write the doc

```markdown
# v0.1 design

Updated 2026-08-22.

**Canvas:** https://claude.ai/public/artifacts/...
**Covers:** ACC-01, TXN-01, CAT-01

## Screens

| Screen | Covers | Notes |
| --- | --- | --- |
| Account list | `ACC-01` | Entry point. |
| Add transaction | `TXN-01` | Reached from the account list only. |
| Category picker | `CAT-01` | A sheet over add transaction, not a screen. |

## What the canvas does not show

- An account with no transactions says "nothing here yet", not an empty list.
- A failed save keeps the form filled and shows the error above the amount.
- The first run has no accounts, so the account list is the empty state, not a
  screen a person passes through.

## Decided against

- A separate edit screen. Editing happens in place.
- A dashboard for v0.1. It needs categories to settle first.
```

The Canvas link is the one thing this file must never lose. Everything else can
be rebuilt from the artboards; the URL cannot.

### 5. Clean the wording

Run the `roy-pstack:unslop` skill on the doc before saving. If it is not
available, apply these by hand:

- no em dashes
- sentence case headings
- no emojis
- no "seamlessly", "robust", "leverage", "empower", "comprehensive"
- one idea per sentence, active voice
- cut any line that would read the same in another project's design doc

### 6. Report

The path, the canvas URL, how many screens, and any feature in the scope that
landed on no screen. That last one is the finding. Say it plainly.

Close by naming what comes next: the implementation plan for the first
unplanned phase, with `roy-agents:implementation-plan-writer`. Do not run it
yourself.

<!-- END OF INSTRUCTIONS -->

## Notes

Context only. Skip unless you are stuck.

The design is release-scoped on purpose. Designing one phase at a time produces
a release that looks like it was drawn by four people, because it was.

A canvas is visual, so anything that is not visible on an artboard does not
survive the handoff to `implementation-plan-writer`. That is the whole reason
this file exists. It is not a summary of the canvas and it should never grow
into one.

`implementation-plan-writer` can read the canvas itself through the artifact
URL. Give it the URL and this doc in the dispatch and it needs nothing else
from the design.
