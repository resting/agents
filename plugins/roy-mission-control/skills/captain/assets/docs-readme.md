# Mission folder

This folder is the paper trail for the build. One numbered folder per agent, in the order
they run. Inside each, one folder per release. Agents write their own stage artifacts
and reports to the captain. They also record questions and answers in the shared
ledger. The captain owns the mission record, state, and gate decisions.

You can edit anything in here. Your edits win. Tell the captain what you changed, or
run `/mission-sync`, and it will work out what needs redoing.

## Where to go for help

The captain is your main contact throughout the mission. Return to the captain or
run `/mission` whenever you are unsure what is happening or what to do next. It will
check the current reports, explain any blocker, and recommend the next step.

When an agent needs a decision, it reports the question to the captain. When it
needs a longer conversation, the captain explains why and directs you to that agent.
You can also visit an agent directly. It records your context and informs the captain
so the mission stays up to date. If direct conversations are unavailable, the captain
relays questions and answers for you.


After the agent has enough information, it finishes its documents and reports back
to the captain. The captain shows what is ready and asks whether to proceed.
Answering questions or confirming document wording does not start the next stage.
You can always return to the captain during a conversation for guidance.

## Structure

```
docs/roy_mission_control/
├── README.md
├── 00_captain/
│   ├── mission.md                             every release, decisions so far
│   └── releases/v0.1/
│       ├── state.md                           runtime, active conversation, gates, artifacts
│       ├── open_questions.md                  what nobody has decided yet
│       ├── autonomy_log.md                    gates the captain passed on its own, and why
│       └── inbox/                             each agent's report to the captain
├── 01_design_intake/releases/v0.1/
│   └── design_brief.md                        what the design shows, in words
├── 02_product_owner/releases/v0.1/
│   ├── product_definition.md                  mission, audience, core principles
│   └── feature_inventory.md                   every screen, function, and feature
├── 03_release_scoper/releases/v0.1/
│   └── release_scope.md                       what ships, and what got cut
├── 04_phase_scoper/releases/v0.1/
│   └── phases.md                              the build order, three to six phases
├── 05_plan_writer/releases/v0.1/
│   └── phase_1.md                             the plan for one phase, step by step
├── 06_plan_reviewer/releases/v0.1/
│   └── phase_1_reviewed.md                    the same plan, cut and stress-tested
├── 07_builder/releases/v0.1/
│   └── phase_1_log.md                         what got built, verified, deviated
├── 08_code_reviewer/releases/v0.1/
│   └── phase_1_review.md                      findings, cuts, what needs fixing
├── 09_test_scoper/releases/v0.1/
│   ├── phase_1_unit_tests.md                  what deserves automated tests
│   └── unit_test_plan.md                      the whole release, written at the end
└── 10_manual_test_writer/releases/v0.1/
    ├── phase_1_checklist.md                   what to click after one phase
    └── release_checklist.md                   the full run-through before shipping
```

v0.2 adds a sibling `releases/v0.2/` under every folder. Once a release ships, its
folder stops changing. It is the record of what was built and why.

## How far along this is

`00_captain/mission.md` states the current release's `Coverage`: how many of the
features considered for it are actually shipping, against how many got deferred or
cut. Five features shipping out of five considered is the whole thing. Five out of
nine is a slice, and the other four are named in that release's cut list.

The captain's status messages state the stage, the phase, and roughly how many
stage-runs are left before the release is done. Ask it directly if you just want
that number.

## Autonomy

`00_captain/mission.md` also states `Autonomy`: `gated` asks before every stage,
`checkpoint` skips asking on the stages that are a plain pass-or-fail check,
`unattended` skips asking on every stage except a real conversation it cannot have
for you. Change it anytime with `/mission-autonomy`. Whatever the mode, the captain
never ships a release or starts the next one without asking first, and it logs every
gate it passed on its own in that release's `autonomy_log.md`.

## The two files to read first

`00_captain/mission.md` tells you which release is in flight and what has been decided.

`00_captain/releases/<version>/open_questions.md` tells you what the captain is waiting
on. Answers go here and then get written into the plan that needed them.

## The three you will read most

`03_release_scoper/releases/<version>/release_scope.md` when you want to know what is
being built.

`06_plan_reviewer/releases/<version>/phase_N_reviewed.md` when you want to know how.

`10_manual_test_writer/releases/<version>/release_checklist.md` when you want to try it.

## Editing

Edit the file, then tell the captain. If you change the scope, the plans downstream get
marked stale, which means nobody has checked them against your change yet. Stale is not
the same as wrong. The captain will tell you the cheapest thing to re-run.

Editing a shipped release folder changes nothing about the release in flight. If the
change matters now, it belongs in the current release.

## Why the cut list matters

`release_scope.md` ends with a cut list: everything that did not make the release, and
why. When the next release starts, the captain copies that list in as the candidate
set. It is the reason the next scoping session takes minutes instead of an afternoon.
