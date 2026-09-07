---
name: manual-checklist
description: >
  Write a plain-language checklist a person can run by hand to confirm the build
  works. Use this skill whenever the user says "give me a checklist", "how do I test
  this", "what should I click", "QA list", "acceptance list", "let me try it", or
  after a build phase finishes. Written for a human tester, not for a developer.
metadata:
  version: "0.1.1"
---

# Manual checklist

When asking the user, prefer `AskUserQuestion`.
Read the [user-question policy](../agent-handoff/references/user-questions.md) before asking.

A list someone can follow with no help, ticking boxes as they go.

Load `unslop`. Read `docs/roy_mission_control/03_release_scoper/releases/<version>/release_scope.md` and the phase code.

Load `agent-handoff` for questions, reports, and user conversations. Report gaps to
the captain before asking the user. Only the captain records gate acceptance and
starts the next stage.

## Writing rules

1. Plain language. No component names, endpoints, table names, or file paths.
2. One action per line. If a line has "and", split it.
3. Every line says what to do and what you should see. Both halves, always.
4. Order the list the way a real person would use the product, not the way it was
   built.
5. Under 30 items. Longer and it goes untested.
6. Say what to do when a step fails. One line at the top is enough.
7. No jargon in the failure notes either. "Nothing appears" beats "the request 500s".

## Output: docs/roy_mission_control/10_manual_test_writer/releases/<version>/phase_N_checklist.md

```markdown
# Test checklist: phase N

Takes about 10 minutes. If a step fails, tick "no", write what you saw, and keep
going. Later steps may still work.

## Before you start
- [ ] Open <url>
- [ ] Sign in as <account>

## The main thing it should do
| # | Do this | You should see | OK? | What you saw |
|---|---------|----------------|-----|--------------|
| 1 | Type "Buy milk" in the box and press enter | "Buy milk" appears at the top of the list | [ ] | |
| 2 | Refresh the page | "Buy milk" is still there | [ ] | |

## When things are empty or full
| # | Do this | You should see | OK? | What you saw |
| 3 | Delete every item | A message saying the list is empty | [ ] | |
| 4 | Add 20 items | All 20 appear, the page still scrolls smoothly | [ ] | |

## When you do something wrong
| # | Do this | You should see | OK? | What you saw |
| 5 | Press enter with the box empty | Nothing is added, no error box | [ ] | |
| 6 | Press the save button twice quickly | Only one item is added | [ ] | |

## Stop here if
Any item in "the main thing it should do" fails. The rest of the list will not tell
you anything useful until that is fixed.
```

## Coverage

Cover, in this order: the core job end to end, empty and full states, wrong input,
double clicks, refresh mid-task, and going back. Skip anything the phase did not
build, and say so at the top rather than leaving a gap.

## Tone

Write it for a person who did not build this and does not want a lecture. Short lines.
No praise, no filler, no "great job". Just what to do and what should happen.

## Report readiness

Report the completed artifacts and any blocking questions to the captain through
`agent-handoff`. The captain presents them to the user and handles the next step.
