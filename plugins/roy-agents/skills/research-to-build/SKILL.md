---
name: research-to-build
description: >
  A three-phase, document-driven project workflow: Phase 1 (Study) researches an unfamiliar 
  domain and produces a comprehensive knowledge base. Phase 2 (Plan) reads the research and 
  creates a detailed implementation plan. Phase 3 (Build) executes the plan. Each phase runs 
  in a SEPARATE session with its own folder under /docs. Use this skill whenever the user says 
  "I want to build X but I don't know how it works", "research this topic then build an app", 
  "start a new project from scratch", "I need to understand X before building", "create a project 
  plan with research", "continue to phase 2", "continue to phase 3", "start the planning phase", 
  "start the build phase", or any request that combines domain learning with application development. 
  Also trigger when the user references a /docs folder with phase subfolders, or says "pick up 
  where we left off" on a research-to-build project.
---

# Research-to-Build: Three-Phase Project Workflow

## How This Works

Three phases. Three separate sessions. Each phase gets its own folder under `/docs`.

```
/docs/
├── phase1/                          ← STUDY (Session 1)
│   ├── 00-project-brief.md
│   ├── 01-domain-research.md
│   ├── 01a-deep-dive-[topic].md     (optional)
│   ├── 02-research-review.md
│   └── step-log.md
│
├── phase2/                          ← PLAN (Session 2)
│   ├── 03-architecture.md
│   ├── 04-prd.md
│   ├── 05-implementation-plan.md
│   └── step-log.md
│
└── phase3/                          ← BUILD (Session 3+)
    ├── 05a-refined-plan.md          (if needed)
    ├── 06-build-log.md
    ├── 07-project-status.md
    └── step-log.md
```

Each phase is a **separate chat session**. The `/docs` folder tree is the handoff.

---

## GOLDEN RULE: Document Every Step

**Every meaningful action taken in every phase MUST be logged as a numbered step in that phase's step log.**

Each phase maintains its own step log:

| Phase | Step Log File |
|-------|--------------|
| Phase 1 (Study) | `/docs/phase1/step-log.md` |
| Phase 2 (Plan) | `/docs/phase2/step-log.md` |
| Phase 3 (Build) | `/docs/phase3/step-log.md` |

Step log format — append a new entry for every action:

```markdown
# Phase [X] Step Log

## Step [X]-001: [Action taken]
- **Timestamp**: [when]
- **What was done**: [description]
- **Output**: [what was produced — file name, decision, finding]
- **References**: [any docs or sources used]

## Step [X]-002: [Action taken]
- **Timestamp**: [when]
- **What was done**: [description]
- **Output**: [what was produced]
- **References**: [any docs or sources used]
```

**What counts as a step:**
- Searched the web for something → log it (what was searched, what was found)
- Created a document → log it (which doc, what it contains)
- Made a design decision → log it (what was decided, why)
- Asked the user a question → log it (what was asked, what they answered)
- Wrote code for a task → log it (which task, what files)
- Encountered a problem → log it (what happened, how it was resolved)
- Read/analyzed an existing doc → log it (which doc, key takeaways)

**Why**: So anyone can open the step log and see exactly what happened, in what order, and trace back to any point in the process. This is the project's timeline.

**Create the step log file as the FIRST action in every phase.** It should be the first document written, and the last document updated, in every session.

---

## Detecting Which Phase to Run

When the skill triggers, determine the phase by checking what exists:

1. **No `/docs/phase1/` folder** → Phase 1 (Study)
2. **`/docs/phase1/` exists with docs, but no `/docs/phase2/`** → Phase 2 (Plan)
3. **`/docs/phase2/` exists with docs, but no `/docs/phase3/`** → Phase 3 (Build)
4. **`/docs/phase3/` exists** → Continue Phase 3 (check `07-project-status.md` for where to resume)
5. **User explicitly says** "phase 1/2/3" or "study/plan/build" → Go to that phase

If ambiguous, ask the user which phase they're starting.

---

## PHASE 1: STUDY

**Goal**: Become an expert in the domain. Document everything so thoroughly that someone with ZERO prior knowledge can read the docs and fully understand the subject.

**No architecture. No tech decisions. No code. Pure learning.**

### Step 1.0: Initialize Phase 1

Create the folder `/docs/phase1/` and initialize the step log.

Create `/docs/phase1/step-log.md`:

```markdown
# Phase 1 (Study) Step Log

## Step 1-001: Phase 1 initialized
- **Timestamp**: [now]
- **What was done**: Created /docs/phase1/ folder and step log. Beginning Study phase.
- **Output**: /docs/phase1/step-log.md
```

Log every subsequent action as a numbered step in this file (1-002, 1-003, etc.).

### Step 1.1: Project Brief

Talk to the user. Understand what they want to build and what they don't know.

Create `/docs/phase1/00-project-brief.md`:

```markdown
# Project Brief

## Project Name
[name]

## One-Line Description
[what is this app in one sentence]

## The Domain
[what subject area needs to be researched — e.g., "Bazi / Four Pillars of Destiny"]

## What the User Wants to Build
[app type, platform, rough feature ideas]

## Target Users
[who will use this]

## What the User Already Knows
[any existing knowledge — could be "nothing"]

## What the User Needs to Learn
[specific questions and knowledge gaps]

## Constraints
[budget, timeline, tech preferences, anything relevant]
```

**→ Log step**: "Step 1-002: Created 00-project-brief.md in /docs/phase1/. Captured [summary of what user wants]."

### Step 1.2: Deep Domain Research

This is the heart of Phase 1. Use web search **extensively** — minimum 10-15 searches across different aspects of the domain.

Read the research template at `references/research-template.md` for the full structure.

Create `/docs/phase1/01-domain-research.md`:

This document must be **comprehensive enough that a developer who has never heard of this domain can read it and understand**:
- What the domain is and where it comes from
- Every key concept and term (with a glossary)
- Exactly how the system/process works, step by step
- All formulas, algorithms, scoring systems, decision trees
- What data structures are involved
- What existing solutions look like
- What the common mistakes and edge cases are

**Research approach — do all of these:**

1. **Foundational search**: What is [topic]? History, origins, purpose.
2. **Mechanics search**: How does [topic] work? Step-by-step process.
3. **Technical search**: Algorithms, formulas, calculations used in [topic].
4. **Data search**: What data does [topic] use? What are the inputs/outputs?
5. **Implementation search**: Existing apps, libraries, APIs for [topic].
6. **Edge case search**: Common mistakes, misconceptions, pitfalls in [topic].
7. **Expert search**: Authoritative sources, academic papers, books on [topic].

**Write for a newcomer.** If a concept needs a concept to explain it, explain that too. 
Use tables for structured data. Use numbered steps for processes. Use examples liberally.

If the domain is large, create supplementary deep-dive documents:

```
/docs/phase1/01a-deep-dive-[subtopic].md
/docs/phase1/01b-deep-dive-[subtopic].md
```

**→ Log steps**: Log EVERY search performed as its own step:
- "Step 1-003: Searched 'What is Bazi'. Found [key finding]. Source: [URL]."
- "Step 1-004: Searched 'Bazi calculation algorithm'. Found [key finding]. Source: [URL]."
- Continue numbering for each search.
- Final step: "Step 1-0XX: Created 01-domain-research.md in /docs/phase1/. [X] sections covering [summary]."

### Step 1.3: Research Review & Validation

Summarize the key findings for the user in plain language. Ask them:
- Does this match your understanding?
- Anything that seems wrong or missing?
- Any areas you want explored deeper?
- What's most important for the app?

Create `/docs/phase1/02-research-review.md`:

```markdown
# Research Review

## Key Findings Summary
[bullet points of the most important discoveries]

## User Feedback
[what the user confirmed, corrected, or added]

## Priority Areas for the App
[which parts of the domain matter most for the intended application]

## Open Questions
[anything still unclear or needing further research]

## Phase 1 Status: COMPLETE
```

**→ Log step**: "Step 1-0XX: Created 02-research-review.md in /docs/phase1/. User validated findings. Phase 1 complete."

### Phase 1 Wrap-Up

Tell the user EXACTLY this:

---

> ✅ **Phase 1 (Study) is complete.**
>
> Your `/docs/phase1/` folder now contains:
> - `00-project-brief.md` — What you want to build
> - `01-domain-research.md` — Complete domain knowledge base
> - `02-research-review.md` — Validated findings and priorities
> - `step-log.md` — Every step taken during research, in order
>
> **To start Phase 2 (Plan), open a new chat session and say:**
>
> *"Start Phase 2 (Plan) for [project name]. The research docs are in /docs/phase1/."*
>
> Phase 2 will read all your research and produce the architecture, PRD, and a step-by-step implementation plan. No coding — just planning.

---

## PHASE 2: PLAN

**Goal**: Read all the research. Design the application. Plan every implementation step. Produce documents detailed enough that any developer (or AI) can execute the build without asking questions.

**No code. No building. Pure planning and design.**

### Step 2.0: Initialize Phase 2 & Load Context

Create the folder `/docs/phase2/` and initialize the step log.

Create `/docs/phase2/step-log.md`:

```markdown
# Phase 2 (Plan) Step Log

## Step 2-001: Phase 2 initialized
- **Timestamp**: [now]
- **What was done**: Created /docs/phase2/ folder and step log. Beginning Plan phase.
- **Output**: /docs/phase2/step-log.md
```

Then read these Phase 1 documents in order:
1. `/docs/phase1/00-project-brief.md`
2. `/docs/phase1/01-domain-research.md` (and any 01a, 01b supplements)
3. `/docs/phase1/02-research-review.md`
4. `/docs/phase1/step-log.md` (to understand the research trail)

Confirm to the user: "I've read through all the Phase 1 research. Here's what I understand: [brief summary]. Ready to start planning?"

**→ Log step**: "Step 2-002: Read all Phase 1 docs from /docs/phase1/ ([X] files). Key understanding: [brief summary]."

### Step 2.1: Architecture Design

Read the architecture template at `references/architecture-template.md` for the full structure.

Create `/docs/phase2/03-architecture.md`:

Key decisions to make and document:
- **Tech stack**: What languages, frameworks, databases, and why
- **System architecture**: Components, how they connect, data flow
- **Data models**: Entities, fields, types, relationships — derived directly from the domain research
- **API design**: Endpoints, methods, request/response shapes (if applicable)
- **UI/UX design**: Screen descriptions, user flows, layout sketches in text
- **Third-party dependencies**: Libraries, APIs, services needed
- **Security**: Auth, data validation, sensitive data handling

Every architecture decision must reference the research:
> "Per /docs/phase1/01-domain-research.md, Section 5, the scoring algorithm requires X, 
> so the data model needs fields for Y and Z."

**→ Log steps**: Log each major architecture decision as its own step:
- "Step 2-003: Chose tech stack — [stack]. Rationale: [why]."
- "Step 2-004: Designed data model — [X] entities derived from phase1/01-domain-research.md Section [Y]."
- "Step 2-005: Created 03-architecture.md in /docs/phase2/."

### Step 2.2: Product Requirements Document

Create `/docs/phase2/04-prd.md`:

```markdown
# PRD: [Project Name]

## Overview
[1-2 sentences: what it is, core value]

## Goals
- [Primary objective]
- [Secondary objective]  
- [Success metric — be specific]

## User Stories
- As a [user], I want to [action] so that [benefit]
- [3-5 stories max]

## Core Features (v1 — keep it tight)

### Feature 1: [Name]
- [Specific requirement — use imperative verbs: Display, Calculate, Validate]
- [Acceptance criteria]
- [Domain reference: "Based on /docs/phase1/01-domain-research.md Section X"]

### Feature 2: [Name]
[repeat pattern]

### Feature 3: [Name]
[repeat pattern]

[3-5 features MAX for v1]

## Out of Scope (v1)
- [Feature explicitly excluded]
- [Feature deferred to v2]

## Open Questions
- [Anything that needs user input before building]
```

**→ Log step**: "Step 2-0XX: Created 04-prd.md in /docs/phase2/. [X] features defined for v1. [Y] features deferred to v2."

### Step 2.3: Implementation Plan

This is the most critical document. Break the build into **ordered, atomic tasks** that can be executed sequentially. Each task must be specific enough that Phase 3 can execute it without asking "but how?"

Create `/docs/phase2/05-implementation-plan.md`:

```markdown
# Implementation Plan: [Project Name]

## Prerequisites
- [ ] Development environment: [specific tools, versions, setup commands]
- [ ] Dependencies: [exact package names and versions]
- [ ] Accounts/API keys: [list what's needed]
- [ ] Reference docs to read: [list full paths under /docs/phase1/ and /docs/phase2/]

## Build Order

### Stage 1: Project Setup & Foundation
- [ ] **Task 1.1**: [Initialize project with [framework/tool]]
  - What: [specific action]
  - Files to create: [list]
  - Acceptance: [how to verify it worked]

- [ ] **Task 1.2**: [Set up data models/database schema]
  - What: [specific action]
  - Source: /docs/phase2/03-architecture.md Section [X], /docs/phase1/01-domain-research.md Section [Y]
  - Files to create: [list]
  - Acceptance: [how to verify]

### Stage 2: Core Domain Logic
- [ ] **Task 2.1**: [Implement [algorithm/calculation] from /docs/phase1/01-domain-research.md Section X]
  - What: [specific action]
  - Input: [what this function/module takes]
  - Output: [what it produces]
  - Test data: [example from research — specific input → expected output]
  - Files to create: [list]

- [ ] **Task 2.2**: [Next piece of domain logic]
  [repeat pattern]

### Stage 3: User Interface
- [ ] **Task 3.1**: [Build [screen/component]]
  - What: [specific layout and behavior]
  - Source: /docs/phase2/03-architecture.md Section [X], /docs/phase2/04-prd.md Feature [Y]
  - Files to create: [list]

### Stage 4: Integration & Wiring
- [ ] **Task 4.1**: [Connect UI to domain logic]
  - What: [specific wiring/data flow]
  - Files to modify: [list]

### Stage 5: Testing & Polish
- [ ] **Task 5.1**: [Test with example data from domain research]
  - Test cases: [specific inputs → expected outputs from /docs/phase1/01-domain-research.md]

- [ ] **Task 5.2**: [Error handling and edge cases]
  - Edge cases: [from /docs/phase1/01-domain-research.md Section 7]

### Stage 6: Deployment
- [ ] **Task 6.1**: [Deployment steps — exact commands]

## Task Summary
- Total tasks: [count]
- Estimated stages: [count]

## Phase 2 Status: COMPLETE
```

**→ Log step**: "Step 2-0XX: Created 05-implementation-plan.md in /docs/phase2/. [X] tasks across [Y] stages. Phase 2 complete."

### Phase 2 Wrap-Up

Tell the user EXACTLY this:

---

> ✅ **Phase 2 (Plan) is complete.**
>
> Your `/docs/phase2/` folder now contains:
> - `03-architecture.md` — Tech stack, system design, data models
> - `04-prd.md` — Product requirements and feature specs
> - `05-implementation-plan.md` — Step-by-step build checklist ([X] tasks across [Y] stages)
> - `step-log.md` — Every planning decision and action, in order
>
> **To start Phase 3 (Build), open a new chat session and say:**
>
> *"Start Phase 3 (Build) for [project name]. The plan is in /docs/phase2/."*
>
> Phase 3 will analyze the plan, break down any large tasks if needed, then execute the build task by task.

---

## PHASE 3: BUILD

**Goal**: Execute the implementation plan. Write code. Build the thing. Log everything.

### Step 3.0: Initialize Phase 3, Load Context & Analyze Plan

Create the folder `/docs/phase3/` and initialize the step log.

Create `/docs/phase3/step-log.md`:

```markdown
# Phase 3 (Build) Step Log

## Step 3-001: Phase 3 initialized
- **Timestamp**: [now]
- **What was done**: Created /docs/phase3/ folder and step log. Beginning Build phase.
- **Output**: /docs/phase3/step-log.md
```

Read ALL documents across both phase folders, in order:
1. `/docs/phase1/` — all files (00, 01, 01a-01x, 02, step-log)
2. `/docs/phase2/` — all files (03, 04, 05, step-log)

**→ Log step**: "Step 3-002: Read all Phase 1 and Phase 2 docs. [X] total documents across /docs/phase1/ and /docs/phase2/."

Then analyze the implementation plan (`/docs/phase2/05-implementation-plan.md`):
- Is any task too large or vague? Break it down further.
- Is any task ambiguous? Clarify using the research and architecture docs.
- Are there hidden dependencies between tasks that need reordering?
- Are there missing tasks implied by the architecture but not listed?

If changes are needed, create `/docs/phase3/05a-refined-plan.md`:

```markdown
# Refined Implementation Plan

## Changes from Original Plan (/docs/phase2/05-implementation-plan.md)
- Task 2.1 split into 2.1a and 2.1b because [reason]
- Task 3.2 moved before 3.1 because [dependency]
- Added Task 2.3: [missing task] because [reason]

## Updated Task List
[complete refined checklist — this becomes the execution guide]
```

Tell the user: "I've analyzed the plan. [Describe any refinements.] Here's the build order: [summary]. Starting now."

**→ Log step**: "Step 3-003: Analyzed implementation plan. [Refined/No changes needed]. [X] tasks to execute."

### Step 3.1: Execute Tasks

Work through the plan task by task. For each task:

1. **Announce** which task you're starting
2. **Reference** the relevant docs by full path (e.g., "/docs/phase1/01-domain-research.md Section 5")
3. **Write** the code
4. **Verify** it works (run it if possible)
5. **Log** completion in BOTH the build log AND the step log

**→ Log every task as a step**: "Step 3-0XX: Executed Task [X.X] — [name]. Files: [list]. Status: [complete/partial]. Notes: [any issues]."

### Step 3.2: Build Log

Create `/docs/phase3/06-build-log.md` and **append to it** as you work:

```markdown
# Build Log: [Project Name]

## Session Start — [Date/Time]
- Starting from: Task [X.X]
- Plan version: [/docs/phase2/05-implementation-plan.md or /docs/phase3/05a-refined-plan.md]

---

### Task 1.1: [Name] — ✅ COMPLETE
- What was done: [brief description]
- Files created/modified: [list]
- Notes: [deviations from plan, decisions made]

### Task 1.2: [Name] — ✅ COMPLETE
- What was done: [brief description]
- Blocker encountered: [if any, and how resolved]

### Task 2.1: [Name] — 🔄 IN PROGRESS
- Status: [where things stand]
- Next action needed: [what to do if session ends here]
```

### Step 3.3: Project Status

Create or update `/docs/phase3/07-project-status.md` at the end of each session (or when the build is complete):

```markdown
# Project Status: [Project Name]

## Current State
- Phase: 3 (Build)
- Last completed task: [Task X.X]
- Overall progress: [X of Y tasks complete] ([percentage]%)

## What's Working
- [Feature/component that's functional]
- [How to test it: specific commands]

## What's Left
- [ ] [Remaining task with brief description]
- [ ] [Remaining task]

## How to Run
[Exact commands to start/test the application]

## Known Issues
- [Issue and workaround if any]

## To Continue
Start a new chat session and say:
*"Continue Phase 3 (Build) for [project name]. Check /docs/phase3/07-project-status.md for where I left off."*
```

### Phase 3 Wrap-Up (when build is fully complete)

Tell the user:

---

> ✅ **Phase 3 (Build) is complete. Your project is built.**
>
> Your `/docs` folder contains the full project history:
>
> ```
> /docs/phase1/  — Domain knowledge + research trail
> /docs/phase2/  — Architecture, PRD, plan + decision trail
> /docs/phase3/  — Build log, status + execution trail
> ```
>
> **To run the app**: [exact commands]
>
> **To continue developing** (add features, fix bugs), start a new session and reference the docs.
> To review the full project history, read the step logs in each phase folder, in order.

---

## Cross-Session Rules

1. **Never skip phases.** Phase 2 requires `/docs/phase1/` docs. Phase 3 requires `/docs/phase2/` docs.
2. **Always read all existing docs** across all phase folders at the start of a session before doing anything.
3. **Always tell the user exactly what to say next** at the end of a session.
4. **The `/docs` folder tree is the single source of truth.** If it's not in a phase folder, it didn't happen.
5. **Reference prior docs by full path and section** when making decisions: "/docs/phase1/01-domain-research.md Section 5.2".
6. **No code in Phase 1 or Phase 2.** Not even pseudocode in Phase 2 unless it clarifies an algorithm from the research.
7. **Log every action as a numbered step.** The step log is the FIRST file created and the LAST file updated in every phase. No exceptions. If you did it, log it.
8. **Step numbers never reset within a phase.** They increment monotonically (1-001, 1-002... 1-047). Across phases they use the phase prefix (1-XXX, 2-XXX, 3-XXX).
9. **Each phase's files live ONLY in that phase's folder.** Phase 1 docs go in `/docs/phase1/`. Phase 2 docs go in `/docs/phase2/`. Phase 3 docs go in `/docs/phase3/`. Never mix.

---

## Document Index

| File | Location | Purpose |
|------|----------|---------|
| `00-project-brief.md` | `/docs/phase1/` | What we're building and why |
| `01-domain-research.md` | `/docs/phase1/` | Complete domain knowledge base |
| `01a-deep-dive-*.md` | `/docs/phase1/` | Optional deep dives on subtopics |
| `02-research-review.md` | `/docs/phase1/` | Validated findings, user feedback |
| `step-log.md` | `/docs/phase1/` | Every research action, numbered sequentially |
| `03-architecture.md` | `/docs/phase2/` | Tech stack, system design, data models |
| `04-prd.md` | `/docs/phase2/` | Product requirements, features, scope |
| `05-implementation-plan.md` | `/docs/phase2/` | Ordered, atomic build tasks |
| `step-log.md` | `/docs/phase2/` | Every planning decision, numbered sequentially |
| `05a-refined-plan.md` | `/docs/phase3/` | Decomposed/reordered tasks (if needed) |
| `06-build-log.md` | `/docs/phase3/` | Running log of what was built |
| `07-project-status.md` | `/docs/phase3/` | Current state, how to continue |
| `step-log.md` | `/docs/phase3/` | Every build action, numbered sequentially |

## Reading the Step Logs

The three step logs form a complete, chronological record of every action taken across the entire project. To reconstruct the full timeline:

1. Read `/docs/phase1/step-log.md` — Steps 1-001 through 1-XXX (research)
2. Read `/docs/phase2/step-log.md` — Steps 2-001 through 2-XXX (planning)
3. Read `/docs/phase3/step-log.md` — Steps 3-001 through 3-XXX (building)

This lets anyone — human or AI — understand not just *what* was produced, but *how* and *why*, in exact sequence.
