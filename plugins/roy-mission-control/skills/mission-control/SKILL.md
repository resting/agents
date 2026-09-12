---
name: mission-control
description: >
  Use when running or inspecting the roy-mission-control pipeline: its eleven
  stages, release folder layout, gates, pauses, and handoff rules. Load this
  whenever running or resuming a mission, before dispatching any pipeline agent,
  or when the user asks what stage something is at, where a file lives, or why a
  stage is waiting. The captain skill loads this first.
metadata:
  version: "0.5.0"
---

# Mission control

The pipeline, the folders, the gates. The `captain` skill runs it. The eleven
agents work inside it. Load `unslop` before writing anything this pipeline
produces, including plans, code comments, commit messages, and questions.

## The pipeline

Every path below is relative to `docs/roy_mission_control/`, and `<version>` is the
release folder name, for example `v0.1`.

| # | Stage | Agent | Reads | Writes | Gate |
|---|-------|-------|-------|--------|------|
| 1 | Design intake | `01-design-intake` | the design | `01_design_intake/releases/<version>/design_brief.md` | Coverage checks pass, no blocking gap |
| 2 | Product definition | `02-product-owner` | design brief, the user | `02_product_owner/releases/<version>/product_definition.md`, `feature_inventory.md` | User confirms both |
| 3 | Release scope | `03-release-scoper` | inventory, definition | `03_release_scoper/releases/<version>/release_scope.md` | User confirms the release, and it works end to end |
| 4 | Phase scope | `04-phase-scoper` | release scope | `04_phase_scoper/releases/<version>/phases.md` | Every feature in exactly one phase |
| 5 | Plan | `05-plan-writer` | phases | `05_plan_writer/releases/<version>/phase_N.md` | Plan covers every feature in the phase |
| 6 | Plan review | `06-plan-reviewer` | plan | `06_plan_reviewer/releases/<version>/phase_N_reviewed.md` | Blocking questions closed, cuts recorded |
| 7 | Build | `07-builder` | reviewed plan | source code, `07_builder/releases/<version>/phase_N_log.md` | Every verification passes |
| 8 | Code review | `08-code-reviewer` | code, reviewed plan | `08_code_reviewer/releases/<version>/phase_N_review.md` | Must-fix applied, final verification clean |
| 9 | Test scope | `09-test-scoper` | code, review | `09_test_scoper/releases/<version>/phase_N_unit_tests.md` | High-priority modules have named cases |
| 10 | Unit tests | `10-unit-test-writer` | test plan, code | tests, `10_unit_test_writer/releases/<version>/phase_N_tests.md` | Every written test passes |
| 11 | Manual checklist | `11-manual-test-writer` | code, release scope | `11_manual_test_writer/releases/<version>/phase_N_checklist.md` | A non-technical person can follow it |

Stages 1 to 4 run once per release. Stages 5 to 11 repeat for each phase.

Stage 3 is the decision point. Nothing from stage 4 on starts until G3 passes,
because everything downstream is scoped from that decision.

At the last phase of a release, stage 9 also writes
`09_test_scoper/releases/<version>/unit_test_plan.md` and stage 11 also writes
`11_manual_test_writer/releases/<version>/release_checklist.md`. Those two are what
somebody reads before shipping.

Any stage may need the user. The agent reports `blocked` for a discrete choice or
`needs_user` for a conversation. The captain puts the question to the user or
arranges the conversation, then resumes the same stage. Complete information lets
an agent finish without asking.

## Folder layout

One folder per agent. Inside it, one folder per release. An agent reads the folders
above it and writes its stage artifacts there. Shared report and question files follow
`agent-handoff`; only the captain writes mission state, progress, and gates.

```
docs/roy_mission_control/
  README.md
  00_captain/
    mission.md                                  global, spans every release
    releases/v0.1/progress.md                   what is done, in progress, left, and waiting on you
    releases/v0.1/state.md                      stage, mode, gates, artifact register
    releases/v0.1/open_questions.md
    releases/v0.1/inbox/                        agent reports to the captain
  01_design_intake/releases/v0.1/design_brief.md
  02_product_owner/releases/v0.1/product_definition.md
  02_product_owner/releases/v0.1/feature_inventory.md
  03_release_scoper/releases/v0.1/release_scope.md
  04_phase_scoper/releases/v0.1/phases.md
  05_plan_writer/releases/v0.1/phase_1.md
  06_plan_reviewer/releases/v0.1/phase_1_reviewed.md
  07_builder/releases/v0.1/phase_1_log.md
  08_code_reviewer/releases/v0.1/phase_1_review.md
  09_test_scoper/releases/v0.1/phase_1_unit_tests.md
  09_test_scoper/releases/v0.1/unit_test_plan.md
  10_unit_test_writer/releases/v0.1/phase_1_tests.md
  11_manual_test_writer/releases/v0.1/phase_1_checklist.md
  11_manual_test_writer/releases/v0.1/release_checklist.md
```

v0.2 adds a sibling `releases/v0.2/` under every agent. Nothing in `releases/v0.1/`
gets edited once that release ships. It is the record of what was built and why.

### Version folder names

Lowercase `v`, then the number, no spaces: `v0.1`, `v0.2`, `v1.0`. Use whatever the
user calls the release. If they have not named it, default to `v0.1` and say so.

## State files

Read [the state-file reference](references/state-files.md) when creating, updating,
or reconciling `mission.md`, `state.md`, and `progress.md`.

## Gates

| Gate | Passes when | Pauses in `auto` |
|------|-------------|------------------|
| G1 | Coverage checks pass and no blocking gap is open | no |
| G2 | The user confirms the definition and the inventory | yes |
| G3 | The user confirms the release, and it works end to end | yes |
| G4 | Every release feature is in exactly one phase, or split by name | no |
| G5 | Every feature in the phase has a step; every step has files and a verification | no |
| G6 | Blocking questions closed, cuts recorded in the reviewed plan | no |
| G7 | Every step and the whole-phase verification pass | no |
| G8 | Must-fix items applied, final verification clean | no |
| G9 | High-priority modules have named cases | no |
| G10 | Every written test passes | no |
| G11 | Checklist written; at the last phase, the release checklist too | last phase only |

G1 to G4 are per release. G5 to G11 are per phase; passing G6 for phase 1 never
passes it for phase 2. A new release resets its gates. `done` alone passes no gate:
the captain checks the evidence and records it. A `blocked`, `needs_user`, or
`failed` report pauses any stage. `phase` mode pauses after every G11 and `step`
mode after every gate.

## Operating rules

Read [the operating rules](references/rules.md) before dispatching, passing a
gate, handling missing information, or reconciling changed work.
