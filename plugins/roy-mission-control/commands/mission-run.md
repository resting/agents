---
description: Ask the captain to run or rerun one named stage.
argument-hint: "design | product | release | phases | plan N | plan-review N | build N | code-review N | test-scope N | checklist N [--release v0.2]"
---

Load `captain` and read current state before dispatch.

| Argument | Agent |
|----------|-------|
| design | 01-design-intake |
| product | 02-product-owner |
| release | 03-release-scoper |
| phases | 04-phase-scoper |
| plan N | 05-plan-writer |
| plan-review N | 06-plan-reviewer |
| build N | 07-builder |
| code-review N | 08-code-reviewer |
| test-scope N | 09-test-scoper |
| checklist N | 10-manual-test-writer |

Use the current release unless `--release` says otherwise. Shipped release: explain
that it is read-only. Missing upstream file: name what is needed. An active run or
conversation: reconcile it first; do not start a second writer.

The command authorizes the named run, not automatic downstream work. If its upstream
result awaits acceptance, show the result and ask before running. If another upstream
gate is open, explain its unmet check and ask for an explicit exception for this run.
Record an accepted exception without marking the unmet gate passed. An exception
cannot bypass G3 for stages 4 onward or allow building without a current reviewed plan.

Use the captain's dispatch loop. A rerun reopens its gate and marks affected downstream
work stale. Return its result to the captain for review and user acceptance.

For user questions, prefer `AskUserQuestion`.
Load `agent-handoff` and follow its shared user-question policy before asking.
