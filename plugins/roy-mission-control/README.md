# Roy Mission Control

Hand the captain a design. It writes the brief, checks the product definition and
release scope with you, then plans, builds, reviews, and tests each phase on its own.
It stops only when you have a decision to make, and it tells you where things stand
after every stage.

## Start

In Claude Code:

```
/mission-start ./design v0.1
```

Or ask for the captain in plain language. In Codex or another supported harness,
invoke the generated `captain` skill or ask to start a Roy Mission Control mission.

## What happens

```
design -> brief -> product definition -> release scope -> phases
                        (pause)              (pause)
                                                |
          per phase: plan -> review -> build -> code review -> test scope -> tests -> checklist
                                                                                        |
                                                              last phase: release checklist (pause)
```

The captain pauses at the product definition, at the release scope, whenever an
agent has a question only you can answer, when something fails, and at the end of the
release so you can run the checklist. Say `go` to continue. Tell the captain to pause
after every phase, or every stage, if you want to watch more closely.

Every pause, and every stage in between, comes with the same short block:

```
v0.1  stage 7 build  phase 2 of 4  auto

Done      phase 1 (F1, F3)
Building  phase 2 (F2), builder running
Left      phases 3 and 4 (F4, F5, F6)
Needs you nothing

Next: code review of phase 2 starts when the build passes.
```

The same block lives in `docs/roy_mission_control/00_captain/releases/<version>/progress.md`
in your project, with a feature table and a phase table under it.

## Commands

| Command | What it does |
|---------|--------------|
| `/mission-start [design] [version]` | Set up the folders and run until the first decision |
| `/mission` | Where am I, what needs me, what is left |
| `/go` | Accept what was shown at the last pause and continue |
| `/mission-run <stage> [N]` | Run or rerun one stage by name |
| `/mission-sync [what changed]` | You edited a file; work out what is stale |
| `/mission-release <version>` | Ship the current release and open the next |

## Stages

Eleven agents, numbered in the order they run, so the stage number in the progress
block is also the agent and the folder.

| # | Agent | Produces |
|---|-------|----------|
| 1 | design intake | design brief |
| 2 | product owner | product definition, feature inventory |
| 3 | release scoper | release scope with a cut list |
| 4 | phase scoper | three to six phases, walking skeleton first |
| 5 | plan writer | step-by-step plan for one phase |
| 6 | plan reviewer | the plan, cut and stress-tested |
| 7 | builder | code, one verified step at a time |
| 8 | code reviewer | review with must-fix items applied |
| 9 | test scoper | which cases deserve unit tests |
| 10 | unit test writer | the tests, written and passing |
| 11 | manual test writer | a checklist a person can run |

Stages 1 to 4 run once per release. Stages 5 to 11 repeat per phase. Everything
lands under `docs/roy_mission_control/` in your project, one folder per agent, one
subfolder per release. The [pipeline reference](skills/mission-control/SKILL.md)
defines the folders, gates, and ownership.

## Hosts

Inside Herdr, each specialist runs in its own pane below the captain, created by the
bundled [split helper](skills/agent-handoff/scripts/herdr-split-down.py). Outside
Herdr, the captain uses the host's delegation tool and relays questions itself.
Questions use the host's structured-question tool when one exists; see
[the question policy](skills/agent-handoff/references/user-questions.md).

Claude Code reads model and effort from each agent file. The repository adapters map
those to other harnesses. An explicit user choice wins.

## Maintaining this plugin

This directory is the Claude Code source of truth. Edit only here, then regenerate
and validate through the root Makefile:

```bash
make generate-all
make validate STRICT=1
```

The bundled unslop skill comes from
[pstack unslop](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md).
