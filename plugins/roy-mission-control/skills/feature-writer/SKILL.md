---
name: feature-writer
description: Add or change a feature in the project feature list and keep the feature index in step. Use when the user describes something the product should let a person do, when an inbox idea is being promoted, when feature-interviewer returns proposals, or when building turns up something new. Refuses details. Edits two files and nothing else.
---

# Feature writer

The feature list says what a person can do with the product. One line per
feature, no detail. You are the gate: nothing gets in without passing the test.

## Rules

1. **Features only, never details.** Apply the test below before anything else.
   A detail gets refused, not written.
2. **One line per feature.** High level, plain words. "Store the time of a
   transaction", not how it is stored or what it defaults to.
3. **Two files only.** `docs/mission-control/source/features.md` and
   `docs/mission-control/source/feature-index.md`. Nothing else, ever.
4. **No release information in the feature list.** Status and release live in
   the index. The list says what the product should be, with no version on it.
5. **Every feature gets an ID.** Next unused number in its area. Never reuse
   one, not even from a deleted feature.
6. **Every question goes through AskUserQuestion**, so the user can select an
   option instead of typing a letter. Never present options as plain text.
7. **No code.**

## Steps

### 1. Apply the test

> **Does it change what a person can do?**

Yes, it is a feature. No, it is a detail. Refuse details, say why in one line,
and write nothing.

| Offered | Verdict |
| --- | --- |
| Pick from times you used recently | Feature. Someone can do something new. |
| Deleting an account keeps its transactions | Feature. What a person sees changed. |
| Times are stored as ISO strings | Detail. Nothing new is possible. |
| The time field defaults to now, not blank | Detail. Same feature, different default. |
| Switched the date column to an index | Detail. |

Details belong in a phase plan. They are meant to change many times while
building, and nobody records that.

If you genuinely cannot tell, ask through AskUserQuestion, never as plain
lettered text, and put the test in the question:

> Does "archive instead of delete" change what a person can do, or is it how
> delete already works underneath?

Options:

- a person can now archive and delete separately, two different things
- same thing, just how it works inside

### 2. Read

Read the index if it exists, then the area of `features.md` you are writing
into. Match its bullet shape exactly.

If neither file exists, ask whether to create them, then create both.

### 3. Check nothing downstream breaks

Only when **changing** a feature that already exists.

Look up its row in the index. If the Release column is filled in, stop, say
what the change makes wrong, then ask through AskUserQuestion:

```
TXN-11 is in v0.1 and phase 02 is already built.

Changing it means the built app and the feature list disagree.
```

Options:

- change the feature and re-scope v0.1
- leave the feature, this is a v0.2 change

If the Release column is empty, carry on. Nothing depends on it yet.

### 4. Assign the ID

Three uppercase letters for the area, from the prefix list at the top of the
index. If the area has no prefix, ask which area it belongs to and propose one.
Never invent a prefix silently.

Two digits, so `TXN-11`. Next number is the highest ever used plus one.

### 5. Write the line

```markdown
## Transactions

- `TXN-01` add, edit and delete a transaction
- `TXN-11` store the time of a transaction
- `TXN-14` pick from times you used recently
```

ID in backticks, then what a person can do, in plain words. One line. If it
needs two, it is two features or you have written a detail into it.

Say what a person can do, not why it is good. No bold, no sub-bullets, no
"blank by default", no screen names.

### 6. Update the index

One row, file sorted by ID.

```markdown
| TXN-11 | Store the time of a transaction | Transactions | shaped | |
```

Columns are ID, Feature, Area, Status, Release. Status is `shaped` for anything
new. Release stays empty. `release-writer` fills it later, never this skill.

### 7. Clean the wording

Run the `roy-pstack:unslop` skill on the line you wrote. If it is not
available, apply these by hand:

- no em dashes
- no emojis
- no "seamlessly", "robust", "leverage", "empower", "comprehensive"
- active voice, present tense
- cut any line that would read the same in another project's docs

### 8. Report

The ID you assigned and the line you wrote. One sentence. If you refused
something as a detail, say that instead.

<!-- END OF INSTRUCTIONS -->

## Notes

Context only. Skip unless you are stuck.

The list stays useful because it stays high level. A feature written at the
right altitude survives every rewrite of how it works underneath. One written
at the wrong altitude is wrong within a week and nobody trusts the file again.

The index holds status and release because the feature list deliberately does
not. That is its whole job, not a size optimisation.

To build the index the first time, walk `features.md` area by area with the
user, assigning IDs, and record the area prefixes at the top. That runs once.
