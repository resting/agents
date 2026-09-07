# Captain operations

These procedures extend the captain entry point. Load only the section needed for
the current transition.

## When an agent needs the user

### blocked

Put the agent's discrete choices to the user. Do not answer for them. While you relay,
record `conversation: relay`. Save the answers in the ledger and pass them back to
the specialist to update its artifact and finish. Scope decisions go into `mission.md`
when resolved. If the answers need discussion, arrange a direct conversation.

### needs_user

Explain the missing information in one or two sentences. Any specialist may request
this. The product owner often will, but complete supplied information should let it
finish without an interview.

For a supported interactive specialist session, offer to talk there and identify it. When the user
chooses it, set `conversation: direct`, keep its session and run ID in state, and tell
them they can return to you anytime. Their next message in that session starts the
interview. Do not start a second agent or keep asking questions in parallel.

For a conversation already marked `direct` or `relay`, a newer `needs_user` report
updates progress. Do not repeat the invitation or interrupt unless a new blocker or
requested mode change needs attention.

The specialist saves answers and remaining topics as it goes. If the user comes back
lost, read its draft, latest inbox, and ledger. Explain what has been settled and what
remains. Offer `Continue with the agent`, `Continue through me`, or `Pause`. A status
question is not approval, cancellation, or a reason to restart the interview.

If they choose to relay or pause, tell the existing specialist through the supported
session channel and wait for it to stop questioning before taking over. Preserve its
draft and answers. If the session is gone, explain that and resume from those files in a
supported session; do not point to a session that no longer exists.

When a delegated run has no writable conversation view, say so and offer `Answer
through me`. If the host can create a separate interactive task, follow the runtime
reference and obtain the user's explicit request for that new task first. Never
confuse a read-only subagent inspector with a conversation. Save the chosen mode, collect answers, and resume
the same stage with the saved context. The captain remains the contact throughout.

If a user starts talking in an existing specialist pane without returning here first,
process its conversation notice, update state, and let the discussion continue.

### done

`done` means ready for your review. Verify the outputs and relevant checks, summarize
what is ready, set `awaiting_acceptance`, and ask the user whether to proceed. This
also applies when the agent needed no conversation at all.

The user may have confirmed the document's wording with the agent. You still present
its result and ask before the next stage. Record acceptance only for the version and
phase shown. Then pass the gate and run the accepted next action.

Only after the result is accepted or work is explicitly abandoned may you suggest
closing the finished pane. Never close it for the user.

### failed

Keep the gate pending. Explain the failure and what was saved. Offer retry, a supported
fallback, or pause. Check the actual pane status when no report arrives; a blocked
permission prompt and a stopped process need different recovery actions.

## Start a mission

Use the design location and version already supplied. Ask only for missing details.
Default an unnamed release to `v0.1` and say so. Establish where the design is: a repo
folder, share link, screenshots, or the user's description.

Create `docs/roy_mission_control/` with `00_captain/` and all ten numbered stage
folders from `mission-control`, each with `releases/<version>/`. Add the captain inbox,
`00_captain/mission.md`, and the release `state.md` and `open_questions.md`. Create the
folder README from the captain skill's `assets/docs-readme.md`. Resolve it from
the installed skill path, not the mission project path.

Explain design intake and offer `Go` or `Review the input first`. Run it when accepted,
then return its result for G1 acceptance. Setup does not approve later stages.

## Run a named stage

Route requests such as "run product definition", "review phase 2", or "rerun build"
through the stage table in `mission-control`. The request authorizes only that named
run. Reconcile any active writer or interview first. Missing inputs or a shipped
release require an explanation, not a new run.

If an upstream result awaits acceptance, show it and ask before proceeding. For other
open checks, explain any proposed exception and record the user's explicit decision
without falsely passing the gate. Nothing bypasses G3 for stages 4 onward, and building
requires a current reviewed plan. A rerun reopens its gate and marks affected work
stale. Review its result with the user before the following stage.

## Phase and release completion

G1 to G4 apply once per release. G5 to G10 apply separately to every phase. After G10
is accepted, offer planning the next phase, or the release review if this was the last
phase. Do not mark a release shipped just because the build gate G7 passed.

On `/mission-release <next-version>`, read all phase gates and release rollups. If any
are open, name them and ask whether to close them or explicitly ship with the listed
gaps. Record any exception. Never change a release while its specialist is still
writing; finish or pause that run first.

Once shipping is accepted, mark the release shipped in `mission.md`, create the next
release's folders, reset its gates and active handoff, and carry the previous cut list
as candidates. Decisions remain available. Ask whether the design changed. If unchanged,
copy the brief into the new release and record G1 carried forward with the user's
agreement. Route through product definition before release scope; existing information
may let the product owner finish without another interview. Shipped folders are read-only.

## User edits

The user's edit wins. On `/mission-sync` or a reported edit, compare the files with
the artifact register. Cosmetic edits do not invalidate later work. Scope changes do:

| Edited | Mark stale |
|--------|------------|
| design brief | product definition, inventory, and everything after |
| product definition or feature inventory | release scope and everything after |
| release scope | phases and everything after |
| phases | plans and downstream work for changed phases |
| phase-N plan | reviewed plan, build, review, tests, checklist for N |
| phase-N reviewed plan | build and everything after for N |
| source code | review, tests, checklists |

Reopen affected gates and invalidate acceptance of changed results. If an agent is
working from changed input, notify it and reconcile its draft before accepting it.
Name any conflict with a recorded decision and ask which should govern. Explain the
smallest useful rerun and offer to run it. Stale means it needs checking against the
change, not that it is wrong.

## Resume

Read `mission.md`, the release `state.md`, ledger, active inbox, and relevant drafts.
Check the saved specialist session using the matching runtime when needed. Restore the conversation mode,
processed report sequence, and pending acceptance. Explain the current state and next
action without replaying history. An active interview stays active; a completed result
awaits user acceptance. Neither state starts a new stage by itself.
