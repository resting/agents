---
name: spec-presentation
description: Turn one spec file into a single scrollable HTML page that briefs the team on the one change it describes. Use when the user points at a spec, plan, PRD, or design doc and asks to brief the team, share the change, make a deck or presentation or slides from it, or wants a simple HTML page explaining what's changing — even if they don't say "presentation". Requires a spec file; ask for one if the user hasn't given a path.
---

# Spec → team brief (one scrollable HTML page)

The output is one self-contained HTML file about **one change**: the change the
given spec describes. The team scrolls top to bottom and comes away knowing what
is changing. Nothing else belongs on the page.

## The spec file is the only source

The user must provide a spec file. If they haven't named a path, ask for one and
stop — guessing which document they mean, or assembling a brief from the
conversation, produces a page that says things nobody wrote down.

Everything on the page comes from that file. Don't add background the spec
doesn't state, don't reason out consequences for the team, don't invent
timelines, next steps, owners, or takeaways. If the spec doesn't say it, it
isn't on the page. This restraint is the point: a brief people trust is one they
can check against the spec line by line.

## One change, plain blocks

The page is a headline plus a handful of plain blocks lifted from the spec's own
structure — a heading, then a couple of lines or a few short bullets.

- **Headline** — the change in one sentence, ≤ 12 words. This is the whole brief;
  if a reader stops here they should still have the gist.
- **3–5 blocks**, in the spec's order. Each block is one idea from the spec,
  under its own heading, in ≤ 50 words. Use short bullets when the spec lists
  things, plain lines otherwise.

Skip everything that isn't the change itself: no "why now", no impact section,
no rollout plan, no open questions, no risks, no appendix — even when the spec
has them. Skip implementation detail too: no code beyond three lines, no API
signatures, no config, no file paths unless a path *is* the change.

Whole page ≤ 250 words. If content won't fit, an idea is doing too much — cut it
rather than compress it into dense prose.

## Workflow

1. **Get the spec file.** Read it fully.
2. **Write the headline first.** One sentence: what changes. If you can't say it
   in one sentence, the spec may cover more than one change — ask the user which
   one the brief is about rather than covering all of them.
3. **Pick the 3–5 blocks** that carry that change, and draft their text as plain
   prose before touching HTML. Cutting is easier before markup.
4. **Fill in `assets/template.html`.** Copy it, replace the placeholders, add or
   delete `<section>` blocks as needed. Leave the CSS alone unless the user asks
   for a different look.
5. **Save** as `<spec-name>-brief.html` next to the spec unless the user names a
   path. Open it and read it as a skimmer would: do the headings alone tell the
   story?
6. **Report the path and the headline sentence.**

## How to write the words

Plain present tense, aimed at a competent teammate who works on something else.

**Cut spec framing.** "This document proposes", "Requirements", "Scope",
"Phase 1" — scaffolding for a spec's readers, noise for a skimmer.

> Before: "This RFC proposes migrating the authentication subsystem from
> session-based auth to JWT-based auth in order to support the horizontal
> scaling requirements outlined in Q3 planning."
>
> After: **"Logins move to JWTs."**

**Lead with what changes, not how it's built.**

> Before: "The build pipeline will be refactored to use a shared cache layer
> backed by S3, with cache keys derived from a content hash of the lockfile."
>
> After: **"CI gets a shared build cache."**

**Use the team's everyday names.** "The checkout page", not
"the `CheckoutOrchestrator` subsystem". Expand any acronym the whole team
wouldn't recognize, once.

**No hedging.** "May potentially require some changes to" → "changes". If the
spec says something is undecided, say "not decided yet" and move on.

**Numbers the spec states, never adjectives.** "3× faster" if the spec says so;
otherwise leave it out entirely.

## HTML rules

Start from `assets/template.html` — it already handles readable measure, type
scale, light/dark, mobile, and print.

- **One file, no dependencies.** No CDN links, no external fonts, no frameworks,
  no scripts. People forward this file around and open it offline.
- **Blocks are separated by whitespace and a hairline rule**, not boxes, cards,
  or colour. Air is what makes the page feel light.
- **Don't touch the type scale or measure** to fit more in. If it doesn't fit,
  cut words.
- **No diagrams, no images, no animation.** Plain blocks only.
