---
name: idea-inbox
description: Capture a raw product idea in one line without shaping it. Use when the user has an idea, a want, or a complaint about the product and does not want to stop and specify it. Appends one dated line and asks nothing.
---

# Idea inbox

Catch an idea before it evaporates. This is the front door, not the feature
list. Shaping happens later, in `feature-writer`.

## Rules

1. **Ask nothing.** No clarifying questions, ever. A vague idea gets logged
   vague. Speed is the whole point and a question defeats it.
2. **One line, one file.** Append to
   `docs/mission-control/source/_inbox.md`. Nothing else.
3. **Never touch the feature list, the index, or a release.** An inbox item is
   not a feature yet.
4. **No ID, no status.** Those come at promotion time.
5. **Keep the user's words.** Trim to one line. Do not rewrite or expand.
6. **Reply in one line.** Then get out of the way.

## Steps

### 1. Append

Create the file with a heading if it does not exist.

```markdown
# Inbox

Raw ideas, unshaped. Promoted by feature-writer, or deleted.

- 2026-08-22 | budget rollover should be per-category, not global | me
- 2026-08-22 | the transaction list feels slow past a few hundred rows | me
- 2026-08-22 | someone asked for splitting a bill between people | user
```

Format is `date | the idea in the user's words | source`. Source is `me`,
`user`, `bug` or `competitor`. Default to `me`.

### 2. Reply

"Logged." and nothing more. Do not summarise it back, suggest where it fits, or
ask whether it should go in a release.

## Review mode

If the user asks what is in the inbox, list the open items with dates and
sources, then stop. Promoting is `feature-writer`'s job. Offer to hand over.

Delete a line only when the user says to drop that idea.

<!-- END OF INSTRUCTIONS -->

## Notes

Context only. Skip unless you are stuck.

Knowing later which ideas came from real use rather than from your own head is
worth the one extra word in the source column.
