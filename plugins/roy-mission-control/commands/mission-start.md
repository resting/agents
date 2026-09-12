---
description: Start a mission. Sets up the release folders and runs design intake.
argument-hint: "[design path or link] [version, default v0.1] [--autonomy gated|checkpoint|unattended, default gated]"
---

Load `captain`. Follow "Start a mission". Use $ARGUMENTS for the design location,
version, and autonomy mode if given.

For user questions, prefer `AskUserQuestion`.
Load `agent-handoff` and follow its shared user-question policy before asking.
