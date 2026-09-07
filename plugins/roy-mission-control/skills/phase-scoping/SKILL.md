---
name: phase-scoping
description: >
  Break a v0.1 release scope into ordered implementation phases, each ending in
  something runnable. Use this skill whenever the user says "break this into
  phases", "what order should we build in", "milestones", "sequence the work",
  "what is phase 1", or hands over a release scope and asks how to implement it.
  Runs after release scoping, before plan writing.
metadata:
  version: "0.1.1"
---

# Phase scoping

When asking the user, prefer `AskUserQuestion`.
Read the [user-question policy](../agent-handoff/references/user-questions.md) before asking.

Turn the v0.1 feature list into three to six phases. Every phase ends with something
that runs and can be shown to a person.

Load `unslop` and `open-questions`. Read `docs/roy_mission_control/03_release_scoper/releases/<version>/release_scope.md`.

Load `agent-handoff` for questions, reports, and user conversations. Report gaps to
the captain before asking the user. Only the captain records gate acceptance and
starts the next stage.

## The rule that decides everything

A phase ends demoable. If the end of a phase is "the types are defined" or "the API
layer is complete", it is not a phase, it is a layer. Merge it into the phase that
uses it.

Slice vertically. One thin path through the whole stack beats a finished data layer
with no screen.

## Ordering

1. Walking skeleton first. The narrowest end-to-end path, one screen, one action,
   one save, one read back. Name this phase explicitly.
2. Riskiest unknown next. Whatever could invalidate the rest of the plan goes early,
   while changing course is still cheap. Third-party APIs, anything real-time,
   anything with money or auth.
3. Then the rest by dependency.
4. Polish last, if at all.

## Output: docs/roy_mission_control/04_phase_scoper/releases/<version>/phases.md

```markdown
# Phases: v0.1

## Phase 1: walking skeleton
Goal: one sentence.
Features: F1, F3 (partial)
Runnable at the end: what a person can do and see. Be specific.
Depends on: nothing
Risk: low
Size: S

## Phase 2: <name>
...

## Phase map
| Phase | Features | Runnable output | Depends on | Risk | Size |
|-------|----------|-----------------|------------|------|------|
| 1 | F1, F3p | Create one task and see it after refresh | none | low | S |

## Coverage check
Every v0.1 feature appears in exactly one phase, or is split with the split named.
| Feature | Phase | Split? |
|---------|-------|--------|
| F1 | 1 | no |
| F3 | 1, 3 | yes: create in 1, edit in 3 |
```

## Sizing

S is one sitting. M is a day. L is more than a day, which means split it. Never write
L without also writing what the split would be.

## Grill the user

Check these sequencing questions against the supplied material. Route unresolved
ones through `open-questions` and the captain:

- Is there a demo or deadline that forces a particular order
- Which unknown worries you most
- Is any part already built or already decided
- Does anything need to be real before someone else can start

## Gate

Report the phase map to the captain. The captain asks the user to accept the order
and walking skeleton, then records acceptance before starting the next stage.
