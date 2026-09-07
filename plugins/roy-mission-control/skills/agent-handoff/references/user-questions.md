# User questions

All Mission Control skills and agents prefer a structured question tool over a
plain-text question. This includes clarifications, product interviews, choices,
and stage acceptance when the host permits that use. Ask only for information
that is still needed. Existing answers and authorizations remain valid.

## Choose the host's tool



Prefer `AskUserQuestion`, using its current schema and limits.

Use the actual callable name in the session. The tool must support the question's
purpose, including approval or a required answer where applicable. Tool permission
prompts stay in the host's permission flow.

## Ask through the tool

Keep each question focused. Offer grounded choices for discrete decisions, with
a recommendation and its tradeoff when appropriate. Respect the tool's question
and option limits. Use its built-in free-text answer for context or explanations;
needing the user's own words is not a reason to switch to plain text. Omit choices
when the schema permits free-text-only questions. If choices are required, use
only honest options and keep the tool's custom-answer path available. Do not invent
the user's audience, mission, or priorities to fill an options array.

Wait for the user's submitted answer before doing work that depends on it. With an
asynchronous tool, continue independent work while the question is pending. Never
treat a preselected choice, silence, timeout, or empty tool result as an answer or
stage acceptance. Do not repeat a pending tool question in plain text.

## Fallback and handoff

Use a concise plain-text question only when no permitted tool is available, the
tool fails, or its schema cannot represent the needed request. For example, a
text-only tool cannot collect an attachment. Briefly explain the limitation once.
Do not fabricate options just to avoid this fallback.

A specialist without a direct user channel reports `blocked` or `needs_user` to
the captain. The captain asks through its question tool and relays the answer.
Interactive specialists follow the existing handoff rules before questioning the
user. This preference does not start an interview, change who owns it, or approve
another stage. Save substantive answers in the shared ledger and relevant artifact.
