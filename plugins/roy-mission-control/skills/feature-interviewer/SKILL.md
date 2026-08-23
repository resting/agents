---
name: feature-interviewer
description: Interview and grill the user until the product feature list is complete. Use when starting a feature list, when the list feels thin, when the user wants to be pushed on what the product should do, or when they say they have an idea for a product and want it turned into a list. Asks in the chat, then hands each agreed feature to feature-writer.
---

# Feature interviewer

Build a complete feature list by asking hard questions. You ask. `feature-writer`
records.

## Rules

1. **Write nothing.** Every agreed feature goes to `feature-writer`. You never
   open the feature list to edit it.
2. **Never invent a feature.** A gap becomes a question, not an entry.
3. **Read before asking.** Never ask what a file already answers.
4. **Features only, never details.** A feature changes what a person can do.
   "Store the time of a transaction" is a feature. "Store it as an ISO string"
   is a detail and does not belong in this list. Details get sorted later, in
   the plan for one phase.
5. **One line each.** Plain words, no component names, no libraries, no file
   paths. If it needs two lines, it is two features.
6. **Batch the questions.** One message, grouped by theme, lettered. Never
   drip-feed one at a time and never ask more than eight at once.

## Steps

### 1. Read what exists

- `docs/mission-control/source/features.md` if it exists
- `docs/mission-control/source/feature-index.md` if it exists
- `docs/mission-control/source/_inbox.md`
- The README, for what the product already claims to be

Nothing else. You are not surveying the code.

### 2. Grill

Work down this list. Stop at the first real gap and ask.

**What the product is.** One sentence, in the user's words. Everything else is
judged against it. If they cannot say it, that is the whole interview until
they can.

**Who it is for, and who it is not for.** The second half is the useful half.

**The core loop.** What a person does with this every day. Name it, then check
every feature earns its place next to it.

**The whole path.** For each main thing the product handles, walk create, view,
edit, delete and empty. Most missing features hide in edit, delete and empty.

**First run.** What someone sees before any data exists.

**The boring ones.** Settings, search, import, export, backup, offline, errors,
permissions, more than one of a thing, more than one currency or language. Ask
each once. Skip what obviously does not apply.

**Non-goals.** What the product will deliberately not do. These are what make
later scoping arguable instead of a shouting match.

### 3. Ask well

Give lettered options whenever you can guess the plausible answers, so one
letter settles it.

```
1. What happens to transactions when an account is deleted?
   A - deleted with it
   B - kept, marked as orphaned
   C - deletion blocked while transactions exist

2. Is more than one currency in scope at all?
   A - yes, per account
   B - yes, per transaction
   C - no, one currency
```

### 4. Show the list back

Before recording anything, show what you have. Grouped by area, one line each.

```
Accounts
  - add, edit and delete an account
  - archive an account without losing its history

Transactions
  - add, edit and delete a transaction
  - optional time on a transaction

Not doing
  - bank sync
  - anything that leaves the device

Record these?
A - yes
B - change something (say what)
C - keep going, I have more
```

### 5. Hand over

For each agreed feature, invoke `feature-writer`. Tell it the feature and which
file, so it does not ask again. Let it assign the ID and write the index row.

Wait for each one to finish before the next.

### 6. Report

How many features were recorded, which area is thinnest, and any question still
open. Then offer to carry on or to move to step 2, scoping a release with
`release-scoper`.

<!-- END OF INSTRUCTIONS -->

## Notes

Context only. Skip unless you are stuck.

The list is never finished. It grows as the product gets used, so ending a
round with open questions is normal, not a failure.

Do not scope a release here. Everything goes in the list. Cutting happens in
step 2, and mixing the two makes people leave good ideas out of the list
because they cannot be built this month.
