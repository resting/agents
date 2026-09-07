---
name: mission-control
description: >
  Use when running or inspecting the roy-mission-control pipeline: its ten stages, release folder
  layout, the gates, and the handoff rules. Load this skill whenever running or
  resuming a mission, before dispatching any pipeline agent, or when the user asks
  what stage something is at, where a file lives, or why a stage is blocked. The
  captain skill loads this first.
metadata:
  version: "0.4.1"
---

# Mission control

When asking the user, prefer `AskUserQuestion`.
Read the [user-question policy](../agent-handoff/references/user-questions.md) before asking.

The pipeline, the folders, the gates. The `captain` skill runs it. The ten agents
work inside it.

Load `unslop` before writing anything. It applies to every artifact this pipeline
produces, including plan documents, code comments, commit messages, and the questions
put to the user.

## The pipeline

Every path below is relative to `docs/roy_mission_control/`, and `<version>` is the
release folder name, for example `v0.1`.

| # | Stage | Agent | Reads | Writes | Gate |
|---|-------|-------|-------|--------|------|
| 1 | Design intake | `01-design-intake` | Claude Design output | `01_design_intake/releases/<version>/design_brief.md` | Brief matches the design |
| 2 | Product definition | `02-product-owner` | design brief, the user | `02_product_owner/releases/<version>/product_definition.md`, `feature_inventory.md` | User agrees both are right |
| 3 | Release scope | `03-release-scoper` | inventory, definition | `03_release_scoper/releases/<version>/release_scope.md` | User confirms the release, and it works end to end |
| 4 | Phase scope | `04-phase-scoper` | release scope | `04_phase_scoper/releases/<version>/phases.md` | User confirms phase order |
| 5 | Plan | `05-plan-writer` | phases | `05_plan_writer/releases/<version>/phase_N.md` | Plan covers every feature in the phase |
| 6 | Plan review | `06-plan-reviewer` | plan | `06_plan_reviewer/releases/<version>/phase_N_reviewed.md` | Blocking questions closed, cuts accepted |
| 7 | Build | `07-builder` | reviewed plan | source code, `07_builder/releases/<version>/phase_N_log.md` | Every verification passes |
| 8 | Code review | `08-code-reviewer` | code, reviewed plan | `08_code_reviewer/releases/<version>/phase_N_review.md` | Must-fix applied, final verification clean |
| 9 | Unit test scope | `09-test-scoper` | code, review | `09_test_scoper/releases/<version>/phase_N_unit_tests.md` | High-priority modules have named cases |
| 10 | Manual checklist | `10-manual-test-writer` | code, release scope | `10_manual_test_writer/releases/<version>/phase_N_checklist.md` | A non-technical person can follow it |

Stages 1 to 4 run once per release. Stages 5 to 10 repeat for each phase.

Stage 3 is the decision point. Nothing from stage 4 on starts until G3 passes, because
everything downstream is scoped from that decision.

Any stage may need a direct user conversation. The agent reports the missing
information to the captain, which explains it and arranges the conversation. The
captain remains available for help and asks for acceptance when the result is ready.
Complete information lets an agent finish without an interview.

At the last phase of a release, stage 9 also writes
`09_test_scoper/releases/<version>/unit_test_plan.md` and stage 10 also writes
`10_manual_test_writer/releases/<version>/release_checklist.md`. Those two are the
rollups somebody reads before shipping.

## Folder layout

One folder per agent. Inside it, one folder per release. An agent reads the folders
above it and writes its stage artifacts there. Shared report and question files follow
`agent-handoff`; only the captain writes mission state and gates.

```
docs/roy_mission_control/
  README.md
  00_captain/
    mission.md                                  global, spans every release
    releases/v0.1/state.md                      stage, gates, artifact register
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
  10_manual_test_writer/releases/v0.1/phase_1_checklist.md
  10_manual_test_writer/releases/v0.1/release_checklist.md
```

v0.2 adds a sibling `releases/v0.2/` under every agent. Nothing in `releases/v0.1/`
gets edited once that release ships. It is the record of what was built and why.

### Version folder names

Lowercase `v`, then the number, no spaces: `v0.1`, `v0.2`, `v1.0`. Use whatever the
user calls the release. If they have not named it, default to `v0.1` and say so.

## State files

Read [the state-file reference](references/state-files.md) when creating, updating,
or reconciling `mission.md` and release `state.md`.

## Gates

| Gate | Passes when |
|------|-------------|
| G1 | The brief matches the design |
| G2 | The user agrees the definition and the inventory are right |
| G3 | The release is confirmed, and it works end to end |
| G4 | The user confirms the phase order |
| G5 | The plan covers every feature in the phase |
| G6 | Blocking questions closed, plan cuts accepted |
| G7 | Every build step verification passes |
| G8 | Must-fix items applied, final verification clean |
| G9 | Unit test plan written |
| G10 | Manual checklist written |

G1 to G4 are per release. G5 to G10 are per phase; passing G6 for phase 1 never
approves phase 2. Starting a new release resets its gates. A stage's objective checks
and the user's acceptance of the shown result are both required. `done` alone passes
no gate. The captain records the evidence and acceptance.

## Operating rules

Read [the operating rules](references/rules.md) before dispatching, passing a
gate, handling missing information, or reconciling changed work.
