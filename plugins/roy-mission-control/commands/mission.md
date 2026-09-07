---
description: Ask the captain where you are, what is pending, and how to continue.
---

Load `captain`. Follow `Resume`. Answer the user's question, including during an
agent conversation, and offer the next useful action. Do not restart active work.

For user questions, prefer `AskUserQuestion`.
Load `agent-handoff` and follow its shared user-question policy before asking.
