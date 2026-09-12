# Mission state files

Use these canonical shapes when the captain creates or reconciles saved mission
state.

## 00_captain/mission.md

Global. Survives every release.

```markdown
# Mission: <product name>

Current release: v0.2
Shipped: v0.1 (2026-08-24)
Autonomy: checkpoint

## Releases
| Version | Status | Coverage | Phases | Started | Shipped |
|---------|--------|----------|--------|---------|---------|
| v0.1 | shipped | 7/7 (0 cut) | 4 | 2026-08-20 | 2026-08-24 |
| v0.2 | in progress | 5/8 (2 deferred, 1 cut) | 3 | 2026-08-26 | |

## Decisions
Decisions carry across releases until something overturns them.

| ID | Decision | Release | Stage | Date |
|----|----------|---------|-------|------|
| D-01 | Single user only, no roles | v0.1 | 2 | 2026-08-21 |
```

`Autonomy` is `gated`, `checkpoint`, or `unattended`. See Autonomy modes in `mission-control`.
`Coverage` is features shipping over features considered for the release, with the deferred
and cut counts. Recompute both columns whenever the release scope changes.

## 00_captain/releases/<version>/state.md

Per release. Gates and the artifact register live here, because both reset when a new
release starts.

```markdown
# v0.2 state

Current stage: 2 (product definition)
Current phase: none
Progress: stage 2 of 10, phase count not set yet
Stage status: needs_user
Blocked by: OQ-014

## Active handoff
Agent: 02-product-owner
Run ID: v0.2-02-product-owner-attempt-1
Runtime: codex
Transport: codex-subagent
Agent pane: none
Captain pane: none
Specialist session: <actual returned ID>
Captain task: <actual ID when available>
Conversation: relay
Inbox: 00_captain/releases/v0.2/inbox/02_product_owner.md
Last processed report sequence: 1
Draft: 02_product_owner/releases/v0.2/product_definition.md
Remaining: primary audience and core job
Awaiting acceptance: no
Proposed next action: review product definition and inventory when ready

## Gate log
| Gate | Phase | Passed | Date | User acceptance and evidence |
|------|-------|--------|------|------------------------------|
| G1 | release | yes | 2026-08-26 | User accepted the brief; artifact revision recorded |
| G2 | release | no | | Product conversation active |

## Artifact register
| File | Last written by | Revision | State |
|------|-----------------|----------|-------|
| 01_design_intake/releases/v0.2/design_brief.md | agent | <content hash> | accepted |
| 02_product_owner/releases/v0.2/product_definition.md | agent | <content hash> | draft |

## Processed reports
| Run ID | Agent | Phase | Latest sequence | Status |
|--------|-------|-------|-----------------|--------|
| v0.2-02-product-owner-attempt-1 | 02-product-owner | none | 1 | needs_user |
```

Runtime is `codex` or `claude`. Transport is `codex-pane`, `codex-subagent`, `codex-task`,
`inline`, `claude-pane`, or `claude-task`. Save only IDs returned by the host.
Legacy `pane` and `task` values mean the original Claude transports; do not attach
them as Codex sessions. A host switch reconciles saved files and stops any old writer
before allocating a new run.

Use `running`, `blocked`, `needs_user`, `awaiting_acceptance`, `accepted`, `failed`, or
`paused` for stage status. Conversation mode is `none`, `offered`, `direct`, or `relay`.
When reviewing a completed result, record each artifact revision shown to the user,
the exact next action offered, and the later acceptance. The register may use a content
hash to distinguish substantive changes from an unchanged file. Keep processed run IDs
so duplicate or late reports do not apply to a retry or a different phase.

Recompute `Progress` on every update, using the formula in `mission-control`. Once G4 passes,
use the real phase count; before that, write "phase count not set yet" rather than guessing.

## 00_captain/releases/<version>/autonomy_log.md

Written only in `checkpoint` or `unattended` mode. One row per gate the captain passed
without asking. Absent in `gated` mode.

```markdown
# v0.2 autonomy log

| Gate | Phase | Decision | Reason | Evidence | Date |
|------|-------|----------|--------|----------|------|
| G1 | release | passed | Brief matches the design, no discrepancy found | 01_design_intake/releases/v0.2/design_brief.md | 2026-08-26 |
| G7 | 1 | passed | All seven build-step verifications passed | 07_builder/releases/v0.2/phase_1_log.md | 2026-08-27 |
```

The captain appends a row before briefing the next specialist, never after. An empty log
in `checkpoint` or `unattended` mode means no objective gate has passed yet, not that the
mode is off. Show the full log to the user before shipping, alongside the release rollup.
