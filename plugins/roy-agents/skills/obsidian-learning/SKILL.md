---
name: obsidian-learning
description: Use when the user asks to document, save, or capture a coding learning, lesson, TIL, gotcha, or post-mortem insight to their Obsidian vault (e.g. "document this learning to Obsidian", "save this lesson", "add this to my coding notes"). Also use when asked to consult past learnings before starting work in a familiar problem area.
---

# Document Coding Learnings to Obsidian

Write learnings as markdown notes into the Obsidian vault folder:

```
/Users/roywong/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal/Coding
```

(Quote the path in shell commands — it contains spaces and `~` characters that are literal, not home-dir expansions.)

## Purpose: notes that prevent repeated mistakes

These notes are not a diary. They are **reusable guardrails**, written so that
any future reader — the user, a teammate, or an AI agent dropped into a fresh
session with zero context — can:

1. **Find the note from the symptom** they're seeing (so include the symptom's
   words, error messages, and API names verbatim — that's what gets searched).
2. **Recognize they're about to repeat a known mistake** before they make it.
3. **Apply the working pattern** without access to the original codebase or
   conversation.

Optimize every section for that reader. If a future agent could read the note
and still walk into the same trap, the note has failed.

## Workflow

1. **Identify the learning.** Default to the most recent hard-won insight in
   the conversation (a debugging conclusion, a failed-approaches-then-fix arc,
   an API gotcha). If the user named a specific topic, use that. If a repo doc
   was just written about it (e.g. `docs/learnings/*.md`), use it as source
   material — but rewrite for the vault, don't copy verbatim: vault notes are
   project-independent first, with project specifics as supporting context.

2. **Check for an existing note.** Search the vault folder for notes on the
   same topic (`Grep`/`Glob` on keywords, symptoms, API names). If one exists,
   extend or update it instead of creating a near-duplicate. Read any file
   before overwriting it.

3. **Gather metadata:**
   - Date and time: `date "+%Y-%m-%d %H:%M"`
   - Project: the repo/app name the learning came from (e.g. from the working
     directory or git remote)
   - Tech involved: language, frameworks, APIs (for tags and aliases)

4. **Write the note** using the template below. Prefix the title (both the
   frontmatter `title` and the `# <Title>` heading) with `obsidian-learning: `,
   e.g. `obsidian-learning: SwiftUI macOS Cursor Management`. Filename: prefix
   with `obsidian-learning-` followed by a short descriptive Title Case name,
   e.g. `obsidian-learning-SwiftUI macOS Cursor Management.md`. No `/` or `:`
   in filenames. Match the vault's existing flat style (no subfolders unless
   one already fits).

5. **Confirm** by telling the user the note path and a one-line summary of
   what was captured.

## Note template

```markdown
---
title: "obsidian-learning: <Human-readable title>"
date: <YYYY-MM-DD HH:MM>
project: <project name>
source: <repo path or repo doc the learning came from, if any>
aliases:
  - <symptom phrasing someone would search for, e.g. "cursor won't change in List">
tags:
  - coding/learning
  - <tech tags, e.g. swiftui, macos, appkit>
---

# obsidian-learning: <Title>

> **TL;DR** — <the learning in one or two sentences; the rule future-you
> needs when skimming>

## When this applies

<Trigger conditions, phrased as symptoms: "You are doing X and Y happens."
Include exact error messages, API names, and observable behavior — these are
the search keys that let a future reader or agent land on this note.>

## Context

<What was being built/fixed and in which project. Brief.>

## What didn't work (and why)

<Each failed approach as: the approach → the observable symptom → the root
cause. The *why it fails* is the durable part; a reader who understands the
mechanism can recognize variants of the trap, not just this instance.
Skip this section only if the learning isn't of the trial-and-error kind.>

## What works

<The working approach/pattern, with a minimal code snippet if it helps.
Self-contained: enough detail to re-apply without the original codebase.>

## Rules

<2–5 imperative do/don't bullets, generalized beyond the original project.
Write them as instructions an AI agent could follow directly, e.g.
"Never attach tap gestures to List row content that also uses .draggable —
even .simultaneousGesture blocks drag initiation.">

## Related

<Wiki-links to related vault notes if any exist (e.g. [[MOC SwiftUI]]),
links to docs/references, path to the in-repo learning doc.>
```

## Style rules

- **Symptom-first findability.** Frontmatter `aliases` and the "When this
  applies" section must contain the words a frustrated person (or an agent
  mid-debugging) would actually search: error text, API names, observed
  behavior ("drag doesn't start", "selection turns grey").
- **Mechanism over fix.** Capture *why* each failed approach fails. A fix
  without the mechanism only prevents the identical mistake; the mechanism
  prevents the whole family.
- **Self-contained.** No references that require the original conversation,
  session, or codebase to make sense. Spell out names; no shorthand.
- **Rules as imperatives.** The "Rules" section is the part an AI agent can
  ingest directly — phrase each as a do/don't instruction, not an anecdote.
- **Generalize first, project detail second.** The vault outlives any single
  repo; lead with the transferable mental model.
- **Link, don't duplicate.** If the vault already has a note or MOC for the
  technology, add a wiki-link rather than restating its content.

## Consulting learnings (the other direction)

When starting work in an area where past learnings may exist (the user hints
"didn't we hit this before?", or the tech matches existing notes), grep the
vault folder for the symptom/API keywords and read any matching note **before**
choosing an approach — that is the entire point of this collection.
