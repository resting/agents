# Roy Mission Control

Version 0.21.0. A captain and ten specialists guide a project from design to
tested code.

This directory is the Claude Code source of truth. This repository's adapters
generate Codex, Copilot, Cursor, OpenCode, and Antigravity artifacts from it.

## Start here

In Claude Code, run `/mission-start` with a design path and release version, or
ask for the captain in plain language.

In another supported harness, invoke the generated `captain` skill or ask to
start or resume a Roy Mission Control mission.

The captain briefs one specialist, reviews its work, and asks for acceptance
before continuing. Specialists can report missing context and resume after the
captain obtains the answer.

Questions use the host's permitted structured-question interface when suitable.
Plain text is the fallback. See
[the question policy](skills/agent-handoff/references/user-questions.md).

## Herdr bottom panes

Inside Herdr, each specialist starts in a sibling pane below the captain. The
bundled [split helper](skills/agent-handoff/scripts/herdr-split-down.py) fixes
the direction to `down` and keeps focus on the captain. Outside Herdr, the
captain uses the current host's supported delegation fallback.

## Stages

The ten stages are design intake, product definition, release scoping, phase
scoping, implementation planning, plan review, building, code review, unit-test
scoping, and manual checklists. Each stage has its own acceptance gate.

Project state and deliverables live under `docs/roy_mission_control/` in the
mission project. The [pipeline reference](skills/mission-control/SKILL.md)
defines the folders, state format, gates, and ownership.

## Models

Claude Code reads the model and effort fields in the canonical agent files.
The repository adapters map model aliases to each target harness. An explicit
user choice takes precedence.

## Maintaining this plugin

Edit only this Claude-native source. Regenerate and validate through the root
Makefile:

```bash
make generate HARNESS=codex PLUGIN=roy-mission-control
make generate-all
make validate STRICT=1
```

## Credits

The bundled unslop skill comes from
[pstack unslop](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md).
