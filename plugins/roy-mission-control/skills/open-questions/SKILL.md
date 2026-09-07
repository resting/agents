---
name: open-questions
description: >
  Maintain the shared open-questions ledger and run the grilling protocol that
  closes gaps before they reach code. Use this skill whenever a pipeline stage hits
  something undecided, whenever the user says "what do you need from me",
  "any questions", "what is blocking", "close the open questions", or whenever a
  plan or code review needs a decision from the user. Every roy-mission-control
  agent uses this skill to record questions and route them through the captain.
metadata:
  version: "0.2.1"
---

# Open questions

When asking the user, prefer `AskUserQuestion`.
Read the [user-question policy](../agent-handoff/references/user-questions.md) before asking.

One ledger at `docs/roy_mission_control/00_captain/releases/<version>/open_questions.md`.
Every stage records its questions and answers here. Preserve other stages' entries.
Nothing gets decided in chat and then forgotten.

## Route questions through the captain

Load `agent-handoff`. Search the supplied documents and the ledger before asking.
Report discrete decisions as `blocked`, with options and a recommendation. Report
missing context that needs a conversation as `needs_user`, with the topics to cover.
The captain explains the need to the user and arranges the conversation.

Do not initiate questions in an agent pane before that handoff. If the user visits
an agent directly, welcome them, save the context they provide, report `needs_user`,
and notify the captain. Follow `agent-handoff` to continue within the same stage.
When direct agent conversations are unavailable, send questions and follow-ups to
the captain, who relays the answers. Do not direct the user to a nonexistent pane.

Only the captain changes `mission.md` or `state.md`, records gate acceptance, and
starts another stage. Answering a question or approving document wording does not
authorise the next stage.

Apply the `unslop` skill to every question. Plain words, no stacked hedging, no
"it is important to note that".

## Ledger format

```markdown
# Open questions

| ID | Question | Why it matters | Options | Default | Blocking | Stage | Status | Answer |
|----|----------|----------------|---------|---------|----------|-------|--------|--------|
| OQ-001 | Can two people edit the same list at once? | Decides whether phase 2 needs locking | a) single editor b) last write wins c) live merge | b | yes | 3 | open | |
| OQ-002 | Keep deleted items for 30 days? | Adds a soft-delete column and a purge job | a) hard delete b) 30 day trash | a | no | 4 | closed | a, hard delete for v0.1 |
```

## Asking rules

1. Ask only as many questions as needed, up to the current runtime's tool limit
   and never more than four. One focused question is often enough.
2. For discrete decisions, offer choices and a recommended default. For missing
   product context, ask a focused question and use examples only when grounded in
   the supplied material. Do not invent the user's mission, audience, or principles
   as defaults.
3. State the cost of the wrong choice in one line. "Decides whether phase 2 needs
   locking" beats "affects the architecture".
4. Mark blocking or non-blocking. Blocking stops the stage. Non-blocking becomes a
   recorded assumption and the work continues.
5. Never ask what an upstream artifact already answers. Search `docs/roy_mission_control/`
   first.
6. Never ask about taste when the answer does not change the code. Button colour is
   a design question, not a pipeline question.
7. Keep questions specific. Prefer the question tool for both choices and open-ended
   answers. Use its free-text input for context that does not fit preset options.

## Closing rules

When the user answers:

1. Write the answer into the ledger row and set status to closed.
2. Write the answer into the artifact that needed it. A closed question that never
   reaches the plan is still an open question.
3. If the answer changes scope, include the change and affected artifacts in your
   report to the captain. The captain updates `mission.md` and reviews stale work.
4. If the answer contradicts an earlier decision, keep the conflict open. Route it
   through the captain, or ask during the arranged conversation, before using it.

## Non-blocking assumptions

When a non-blocking question stays open, record the assumption in the artifact
where it applies:

```markdown
> Assumption (OQ-002): hard delete, no trash. Revisit if support asks for undo.
```

## Presenting questions to the user

The captain, or an agent in an arranged conversation, follows the shared
[user-question policy](../agent-handoff/references/user-questions.md). Prefer the
tool for open-ended context as well as choices. Options come from the ledger row,
with any recommended default first and a short explanation of the tradeoff. Lead
with blocking topics. Use plain text only under the policy's fallback conditions.
