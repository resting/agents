---
description: Run or rerun one named stage, without resuming the automatic run.
argument-hint: "design | product | release | phases | plan N | plan-review N | build N | code-review N | test-scope N | tests N | checklist N [--release v0.2]"
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
| tests N | 10-unit-test-writer |
| checklist N | 11-manual-test-writer |

Use the current release unless `--release` says otherwise. Shipped release: explain
that it is read-only. Missing upstream file: name what is needed. An active run or
conversation: reconcile it first; do not start a second writer.

The command authorizes the named run only. It does not resume `auto`. If the
upstream decision gate has not passed, show its result and ask. If another upstream
gate is open, explain its unmet check and ask for an explicit exception for this
run. Record an accepted exception without marking the unmet gate passed. An
exception cannot bypass G3 for stages 4 onward or allow building without a current
reviewed plan.

Use the captain's dispatch loop. A rerun reopens its gate and marks affected
downstream work stale. Return its result to the captain, which prints progress and
records the gate.
