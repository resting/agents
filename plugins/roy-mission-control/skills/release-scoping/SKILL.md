---
name: release-scoping
description: >
  Cut a design brief down to a v0.1 release and push everything else into later
  releases with reasons. Use this skill whenever the user says "scope this",
  "what goes in v0.1", "what should we build first", "MVP", "cut this down",
  "which features ship first", or hands over a design brief and asks what to build.
  Produces the release scope the phase scoper reads.
metadata:
  version: "0.1.2"
---

# Release scoping

Pick the smallest release where a real user finishes the core job end to end. Then
defend it against everything else.

Load `unslop` and `open-questions` first. Read `docs/roy_mission_control/01_design_intake/releases/<version>/design_brief.md`.

## The v0.1 test

Write the core job as one sentence: "A user can ______ without help."

Then for every candidate feature ask: if I delete this, does that sentence stop being
true? If no, it is not in v0.1. There is no third answer. "It would feel unfinished"
means v0.2.

## Size ceiling

Five to nine features in v0.1. Cross nine and you have two releases pretending to be
one. Split and say so.

## Banned from v0.1 unless the core job breaks without them

Settings screens. Admin panels. Onboarding tours. Roles and permissions. Multi-user
anything. Offline mode. Dark mode. Translations. Analytics dashboards. Export.
Search over fewer than 100 items. Undo. Bulk actions. Notifications.

Each of these has shipped as a v0.2 a thousand times. Put them in the cut list with
a reason, not in v0.1 with a shrug.

## Output: docs/roy_mission_control/03_release_scoper/releases/<version>/release_scope.md

```markdown
# Release scope: <product name>

## Core job
A user can ______ without help.

## v0.1
| # | Feature | User-visible behaviour | Done when | Why it is in v0.1 |
|---|---------|------------------------|-----------|-------------------|
| F1 | Create a task | Type a title, press enter, row appears in the list | A refreshed page still shows the row | No task, no job |

## v0.2
| Feature | Why it waits |
|---------|--------------|
| Due date reminders | The job works without them, they need a scheduler |

## Later
Short list. One line each. No detail, it will change.

## Cut list
| Cut | Reason | Revisit when |
|-----|--------|--------------|
| Roles and permissions | Single user in v0.1 (D-01) | A second user asks |

## Assumptions
Non-blocking open questions and the default taken for each.
```

## Writing rules

- "Done when" is observable by a person, not by a developer. "A refreshed page still
  shows the row" is done. "The API returns 201" is not.
- User-visible behaviour is one sentence in the user's words. No component names, no
  endpoints, no table names.
- The cut list is the important half. A scope with no cut list means nothing was cut.

## Grill the user

Before you finish, check these choices against the supplied material. Record any
unanswered ones through `open-questions` and route them through the captain:

- Single user or many people at once
- Does data survive a browser refresh, and where does it live
- Login required in v0.1, or open
- Does anything need to be private from other users
- What must never break, even in v0.1

## Report

Report the release table and cut list through `agent-handoff`. The captain pauses
here: the user confirms the scope, or names the cuts they disagree with, before
phase scoping starts.
