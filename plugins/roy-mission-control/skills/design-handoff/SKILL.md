---
name: design-handoff
description: >
  Turn Claude Design output into a written design brief that the rest of the
  pipeline can scope from. Use this skill whenever the user says "I made this in
  Claude Design", "here is the design", "here are the screens", "turn this design
  into a spec", "hand this off", or shares mockups, a prototype link, or
  screenshots and wants engineering work to follow. Run this before any scoping.
metadata:
  version: "0.1.1"
---

# Design handoff

When asking the user, prefer `AskUserQuestion`.
Read the [user-question policy](../agent-handoff/references/user-questions.md) before asking.

Read the design. Write down what is actually there. Send everything else to the
open-questions ledger.

Load `unslop` before writing. Load `open-questions` before asking anything.

Load `agent-handoff` for questions, reports, and user conversations. Report gaps to
the captain before asking the user. Only the captain records gate acceptance and
starts the next stage.

## Read first

Ask where the design lives if it is not obvious: exported HTML or React from Claude
Design, a share link, screenshots, or a description in chat. Read all of it before
writing a word. Do not brief from one screen.

## Hard rule

Describe only what the design shows. The moment you write a behaviour that no screen
demonstrates, stop and file an open question instead. Common inventions to catch
yourself on: what happens on error, what an empty list looks like, what a field
accepts, who is allowed to do it, what happens after the last step.

## Output: docs/roy_mission_control/01_design_intake/releases/<version>/design_brief.md

```markdown
# Design brief: <product name>

## What it is
One sentence. What a user can do that they could not before.

## Who uses it
One or two sentences. Name the person and the moment they open this.

## The core job
"A user can ______ without help." Fill the blank with a complete task, not a feature.

## Screen inventory
| Screen | Purpose | Key elements | States shown | States missing |
|--------|---------|--------------|--------------|----------------|
| Inbox | See what needs action | list rows, filter, new button | full list | empty, loading, error |

## Flows
### Flow 1: <name>
1. Start: screen X
2. User does Y
3. Ends at screen Z, with <observable result>

Every flow must end somewhere. A flow that trails off is an open question.

## Data implied by the UI
| Object | Fields visible | Where it appears | Who creates it |
|--------|----------------|------------------|----------------|
| Task | title, due date, status, assignee | inbox, detail | user, via new button |

## External dependencies visible in the design
Login providers, payments, maps, email, uploads, anything the UI implies but does
not contain.

## Non-goals
What the design deliberately leaves out. Write only what the user confirmed.

## Gaps
Point at docs/roy_mission_control/00_captain/releases/<version>/open_questions.md. List the blocking IDs here.
```

## Coverage checks before you finish

1. Every screen appears in at least one flow. An orphan screen is either dead or a
   missing flow.
2. Every flow ends at a screen with an observable result.
3. Every data object has something that creates it and something that reads it.
4. Every button and link in the inventory leads somewhere named.
5. Every list has an answer for empty, one item, and many items, or an open question.

## Stay implementation-neutral

No frameworks, no database choices, no file paths, no API shapes. The brief says
what the product does. Later stages decide how.

## Gate

Report the completed brief to the captain. The captain asks whether it matches
what the user designed and arranges any corrections. After the user accepts, the
captain records the gate decision and proposes the next stage.
