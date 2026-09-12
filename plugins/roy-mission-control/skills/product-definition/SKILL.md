---
name: product-definition
description: >
  Establish what the product is for from the supplied material and any needed
  conversation with the user, then inventory every
  screen, function, and feature it could have. Use when the user says "what are we
  building", "define the product", "mission", "core principles", "who is this for",
  "list the features", "product owner", or after design intake and before any release
  is scoped. Produces the document every later stage consults when a judgment call
  comes up.
metadata:
  version: "0.2.2"
---

# Product definition

Two documents. The first says why the product exists. The second says everything it
could ever do. Later stages cut the second down using the first.

Load `unslop`, `open-questions`, and `agent-handoff`. Read the design brief, supplied
answers, and any current or relevant earlier product documents first.

## Use the context, then resolve gaps

Check what the available material establishes before asking anything. A complete
current brief or earlier definition can supply the needed context. Write the two
documents and report readiness without requiring an interview.

If the product's purpose or behavior is unclear, report `needs_user` to the captain
with the missing topics. For discrete decisions, report `blocked` with options.
The captain explains the gap and arranges the conversation. Use `agent-handoff`
when the user visits directly or direct agent conversations are unavailable.

During an arranged conversation, ask only about unresolved topics. When an answer
is vague, offer two readings. When answers contradict, ask which wins. When a
principle would not change a decision, ask what it rules out. There is no minimum
number of rounds. Stop when the material gaps are resolved.

Save answers and remaining topics in the draft and question ledger. Show the wording
for correction during the conversation. Confirmation of the wording does not approve
the next stage. The captain presents the completed documents and asks the user to
accept proceeding.

## Document 1: product_definition.md

```markdown
# <product name>

## Mission
One sentence. What changes in the world because this exists. Not a feature list.

## The core job
"A user can ______ without help." One task, start to finish.

## Target audience
| Who | Their situation | What they use today | Why they would switch |

Name one primary audience. A second is allowed. A third means the product is not
defined yet, say so.

## Core principles
Three to seven. Each one has to be able to lose an argument.

| # | Principle | What it rules out |
|---|-----------|-------------------|
| P1 | Never lose user data, even at the cost of speed | No optimistic writes without a durable queue |

A principle that rules nothing out is a slogan. Delete it or sharpen it.

## Non-goals
What this product will not do, and why. This is the principles applied.

## How we decide
For the recurring tension in this product, which principle wins. Later stages read
this instead of asking you again.
```

## Document 2: feature_inventory.md

Everything the product could do, whatever the release. No prioritising here. That is
the next stage's job, and doing it now hides options.

```markdown
# Feature inventory

## Screens
| ID | Screen | Purpose | From the design? | States needed |
|----|--------|---------|------------------|---------------|
| S1 | Inbox | See what needs action | yes | empty, loading, error, full |

## Functions
What a user can do. One row per verb.

| ID | Function | Screen | Who can do it | Principle it serves |
|----|----------|--------|---------------|--------------------|
| F1 | Create a task | S1 | any user | P2 |

## Features
Larger capabilities made of functions.

| ID | Feature | Functions | Serves | Notes |

## Implied but not designed
Things the product needs that no screen shows: auth, billing, notifications, search,
export, admin. Name them. They are real work even when nobody drew them.

## Open
IDs from the ledger.
```

## Coverage checks

1. Every screen in the design brief appears, or is explicitly dropped with a reason.
2. Every function names the screen it happens on.
3. Every feature maps to a principle, or is flagged for release scoping to resolve.
   Keep the inventory unranked and preserve candidates for that stage.
4. Check for needed capabilities the design omits. List only relevant ones; if the
   design covers them all, record that instead of inventing features.

## Interviewing

During an arranged conversation, ask up to four questions per round through
`open-questions`. Use these only where the supplied material leaves a gap:

- Who opens this, and what happened just before they did?
- What do they do today instead, and what is wrong with it?
- If it did only one thing well, which thing?
- What must never happen, even if it costs a feature?
- What is deliberately not in this product?

Follow up where answers reveal another material gap. Read the answers back as
principles and check the wording. Save progress before reporting to the captain.

## Report readiness

When both documents pass the coverage checks and blocking questions are closed,
report `done` through `agent-handoff` with both output paths and the sources used.
The captain pauses here: the user confirms the definition and the inventory before
release scoping starts.

## Later stages read this

Every stage after this one consults `product_definition.md` when a judgment call comes
up: which of two features survives a cut, whether an edge case matters, whether a
shortcut is acceptable. Write it so that a stranger could settle an argument with it.
