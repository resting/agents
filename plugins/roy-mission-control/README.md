# roy-mission-control

A five-step workflow that takes a product from "I have an idea" to working
code, without losing track of what you decided along the way.

Start with `captain`. It is the only thing you talk to.

## How it works

Every step has one thing that **decides** and one thing that **writes**. The
split is deliberate. Anything that both proposes and writes will talk itself
into its own proposal.

| Step | Decides | Writes | Produces |
| --- | --- | --- | --- |
| 1 Features | `feature-interviewer` (skill) | `feature-writer` | the feature list |
| 2 Release | `release-scoper` (agent) | `release-writer` | what ships in v0.1 |
| 3 Phases | `phase-planner` (agent) | `phase-writer` | how v0.1 is broken up |
| 4 Plan | - | `roy-agents:plan-writer` | one plan per phase |
| 5 Build | - | `roy-agents:plan-implementer` | code |

Steps 2 and 3 are agents. They read, judge and report back, so running them
cold in their own context is cheaper. Step 1 is a skill because interviewing
has to talk to you directly.

`phase-planner` only decides which features go together and in what order. It
does not work out files or steps. That is step 4's job.

`captain` reads the state, says where you are, and dispatches one thing at a
time. It never writes a file itself. `idea-inbox` catches a raw idea in one
line at any point, without stopping the step you are on.

Steps 4 and 5 come from the `roy-agents` plugin. Install it too.

## The chain

Each step narrows the one before it, and each output is what the next step
treats as settled.

```
idea  ->  feature list  ->  release scope  ->  phases  ->  plan  ->  code
          (everything)      (this version)     (one        (throwaway)
                                                sitting)
             ^                                                     |
             |_____________ after every phase ____________________|
```

Features carry an ID from step 1 to step 5, so anything built can be traced
back to the feature that asked for it.

## Features, not details

The feature list is plain markdown, one line per feature, kept high level. One
question decides what belongs in it.

> **Does it change what a person can do?**

Yes, it is a feature. No, it is a detail.

| | |
| --- | --- |
| Store the time of a transaction | feature |
| Pick from times you used recently | feature |
| Deleting an account keeps its transactions | feature |
| Times are stored as ISO strings | detail |
| The time field defaults to now, not blank | detail |

Only `feature-writer` writes the feature list, and it refuses details. So the
test runs in one place and nothing can get past it.

Details get sorted in step 4, in the plan for one phase. They are meant to
change many times while you build, and nobody records that. Write a feature at
this height and it survives every rewrite of how it works underneath. Write it
lower and it is wrong within a week.

## Keeping the list current

Building teaches you things the list does not know. So after every phase,
`captain` asks once.

> Did building this turn up anything a person can now do that the list does not
> already say?

Anything that passes the test goes to `feature-writer` and becomes one more
line. Anything else is dropped and never written down. The sweep runs when work
has stopped anyway, never mid-build.

This is the only path that runs backward, from code to the feature list.
Without it the list slowly stops describing the app.

It catches what you or the implementer noticed. Something built subtly wrong
still goes through unnoticed.

## Folder structure

Everything lands under `docs/mission-control/`. One folder per step, one owner
per folder. `captain` scaffolds it on first run.

```
docs/mission-control/
  README.md                  what this holds and who writes what
  source/                    step 1, the source of truth
    features.md              one line per feature, high level
    feature-index.md         one row per feature: ID, area, status, release
    _inbox.md                raw ideas, not yet features
  releases/                  step 2, the source of truth per release
    v0.1/scope.md            what ships in v0.1
    v0.2/scope.md
  phases/                    step 3, how a release is broken up
    v0.1/_index.md           the phases in build order, with status
  plans/                     step 4, one plan per phase, gitignored
    v0.1/01-accounts.md
    v0.1/02-transactions.md
```

Step 5 writes code, not docs.

`plans/` is the one folder nobody keeps. It holds the details, the details are
meant to change constantly, and a diff full of them buries the changes that
matter. `captain` adds it to `.gitignore` when it scaffolds. How a release was
cut is worth keeping, so `phases/` stays.

| Folder | Written by | Never written by |
| --- | --- | --- |
| `source/features.md`, `source/feature-index.md` | `feature-writer` | anything else |
| `source/_inbox.md` | `idea-inbox` | anything else |
| `releases/` | `release-writer` | anything else |
| `phases/` | `phase-writer` | anything else |
| `plans/` | `roy-agents:plan-writer` | anything else |

`feature-index.md` holds the status and release for every feature, because the
feature list deliberately holds neither. The list says what the product should
do. The index says how far along each one is and which version it landed in.

## House style

Every agent and skill in this plugin follows the same shape.

- Instructions first, then `<!-- END OF INSTRUCTIONS -->`, then a `## Notes`
  section marked context-only. Skip the notes unless you are stuck.
- Plain human language. No jargon, no marketing voice.
- Writers run `roy-pstack:unslop` before saving, with a hand-applied fallback
  list if that skill is not installed.
- Stop and ask rather than guess. A reasonable-looking guess hardens into a
  spec the moment it is written down.
