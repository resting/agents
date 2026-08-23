---
name: release-writer
description: Write the release feature list, pulling features from the source list into v0.1, v0.2 and so on. Use when the user says what should be in a release and wants it recorded, or once release-scoper's proposal has been decided. Writes one scope doc per release and stamps the release into the feature index.
---

# Release writer

Take the features the user wants for a release and write one scope doc. That
doc is the source of truth for the release.

## Rules

1. **Two writes.** `docs/mission-control/releases/<version>/scope.md`, and the
   Release and Status columns of `docs/mission-control/source/feature-index.md`.
   Nothing else, ever.
2. **Never edit the feature list.** Only `feature-writer` writes that file.
3. **Refer to features by ID**, with the section reference alongside. Titles
   and section numbers move, IDs do not.
4. **Link, do not retell.** A scope doc says what ships. It does not re-explain
   the feature.
5. **Only features that exist.** Refuse any ID that is not in the index.
6. **Stop on any ambiguity.** Do not write a line while a question is open. A
   guess that looks reasonable is still a guess.
7. **No implementation detail.** What ships, not how it gets built.

## Steps

### 1. Read the index, then only what you need

Read `docs/mission-control/source/feature-index.md` first. Then open only the source
sections for the features in play, and note their section numbers.

If a scope doc already exists for this version, ask:

```
releases/v0.1/scope.md already exists.
A - replace it
B - add to it, keep what is there
C - skip this version
```

### 2. Match the ask to real features

Where the match is loose, ask. One message, all questions, lettered.

```
1. You said "budgets" for v0.1. There are two:
   A - BUD-01 monthly budget per category
   B - BUD-04 envelope budgets
   C - both

2. v0.1 has transactions but no accounts. Add accounts?
   A - yes, ACC-01 manual accounts
   B - no, leave it out
```

If the user asked for something the feature list does not cover, stop:

```
"Split bills between people" is not in the feature list yet.
A - add it first, then scope   (hands over to feature-writer)
B - leave it out
C - it is there under another name (tell me which)
```

On A, invoke `feature-writer`, wait for it to finish, re-read the index for the
new ID, then carry on. Never write the feature list yourself.

### 3. Confirm before writing

```
v0.1: ACC-01 accounts, TXN-01 transactions, CAT-01 categories
v0.2: BUD-01 budgets, SYN-02 bank sync

ACC-01 is partial: checking, savings, credit card and cash only.

Write these two files?
A - yes
B - change something (say what)
```

### 4. Write the scope doc

```markdown
# v0.1

**Goal:** one line on what a person can do with this build.
**For:** who this release is for.
**Done means:** the condition that makes this release finished.
**Deferred:** the big things left out, and why.
**Success signal:** how the user will know v0.1 worked.
**Target:** a date.

## In scope

- `ACC-01` **Manual accounts** (2.1) - add, edit, delete cash and bank
  accounts. Checking, savings, credit card and cash only, not the other eight
  types. No sync.
- `TXN-01` **Transactions** (2.2) - add, edit, delete. Amount, date, category,
  note.

## Not in this release

- `SYN-02` Bank sync (2.13) - waits for v0.2.
- `BUD-01` Budgets (2.6) - needs categories to settle first.

## Notes

Anything a builder needs that the feature list does not say.
```

Rules for entries:

- ID in backticks, then the name, then the section reference.
- One line each, in plain words, saying what a person can do.
- A partial feature keeps its ID. Say which part is in and which waits. Never
  split it into a new ID.
- "Not in this release" covers only what someone would expect to be there.

The header block is what makes this a release rather than a list. Without a
goal and a "done means", nothing can be scoped and no cut can be argued. If you
cannot fill it in, ask before writing.

### 5. Stamp the index

For every ID in the release, set Release to the version and Status to `scoped`.
Change nothing else in that file.

### 6. Clean the wording

Run the `roy-pstack:unslop` skill on each doc before saving. If it is not
available, apply these by hand:

- no em dashes
- sentence case headings
- no emojis
- no "seamlessly", "robust", "leverage", "empower", "comprehensive", "streamline"
- one idea per sentence, active voice
- cut any line that would read the same in another project's release doc

### 7. Report

Each path, how many features it covers, how many index rows you stamped, and
any feature the user asked for that landed in no release.

Close by naming what comes next: breaking the release into phases, with
`phase-planner`. Do not run it yourself.

<!-- END OF INSTRUCTIONS -->

## Notes

Context only. Skip unless you are stuck.

Read the index rather than the feature list wherever you can. Opening the whole
list to find one feature is what makes this workflow expensive.
