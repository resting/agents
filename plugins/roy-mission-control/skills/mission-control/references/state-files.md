# Mission state files

Use these canonical shapes when the captain creates or reconciles saved mission
state.

## 00_captain/mission.md

Global. Survives every release.

```markdown
# Mission: <product name>

Current release: v0.2
Shipped: v0.1 (2026-08-24)

## Releases
| Version | Status | Features | Phases | Started | Shipped |
|---------|--------|----------|--------|---------|---------|
| v0.1 | shipped | 7 | 4 | 2026-08-20 | 2026-08-24 |
| v0.2 | in progress | 5 | 3 | 2026-08-26 | |

## Decisions
Decisions carry across releases until something overturns them.

| ID | Decision | Release | Stage | Date |
|----|----------|---------|-------|------|
| D-01 | Single user only, no roles | v0.1 | 2 | 2026-08-21 |
```

## 00_captain/releases/<version>/progress.md

Per release. The file the user reads. The captain rewrites it at every transition.

```markdown
# v0.1 progress

Stage: 7 build, phase 2 of 4
Mode: auto
Needs you: nothing

## Features
| ID | Feature | Phase | Status |
|----|---------|-------|--------|
| F1 | Create a task | 1 | done |
| F2 | Edit a task | 2 | building |
| F4 | Filter by status | 3 | planned |
| F6 | Export to CSV | 4 | not started |

## Phases
| Phase | Name | Gates passed | Status |
|-------|------|--------------|--------|
| 1 | Walking skeleton | G5 to G11 | done |
| 2 | Edit and delete | G5, G6 | building |
| 3 | Filters | | planned |
| 4 | Export | | not started |

## Next
Code review of phase 2 starts when the build passes.

## Recent
- 2026-09-12 10:42 Phase 2 plan reviewed: 12 steps to 8, nothing blocking.
- 2026-09-12 09:50 Phase 1 done. Checklist at 11_manual_test_writer/releases/v0.1/phase_1_checklist.md.
```

Feature status is `not started`, `planned`, `building`, `done`, `blocked`, or `cut`.
Keep `Recent` to the last five entries.

## 00_captain/releases/<version>/state.md

Per release. Gates and the artifact register live here, because both reset when a new
release starts.

```markdown
# v0.2 state

Current stage: 2 (product definition)
Current phase: none
Mode: auto
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

Mode is `auto`, `phase`, or `step`. Use `running`, `blocked`, `needs_user`,
`awaiting_acceptance`, `accepted`, `failed`, or `paused` for stage status. Conversation mode is `none`, `offered`, `direct`, or `relay`.
At a pause, record each artifact revision shown to the user, the exact next action
offered, and the later acceptance. At an automatic gate, record the checks and the
revision instead. The register may use a content
hash to distinguish substantive changes from an unchanged file. Keep processed run IDs
so duplicate or late reports do not apply to a retry or a different phase.
