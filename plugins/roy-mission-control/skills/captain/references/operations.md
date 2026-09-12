# Captain operations

Procedures for specific transitions. Load only the section you need.

## Handling a report

### done

Verify the outputs and the stage's gate checks in `mission-control`. Record the gate
with the artifact revisions. Then:

- Decision gate (G2, G3), the release's last G11, or a mode that says pause: set
  `awaiting_acceptance`, print progress, show the result, and ask.
- Otherwise: print progress and dispatch the next stage in the same turn.

The user may have confirmed wording with the specialist during an interview. That
is not acceptance of a decision gate. Show the result and ask.

### blocked

Put the specialist's discrete choices to the user through the question tool, up to
four per call, with the recommended defaults. Do not answer for them. Record
`conversation: relay`. Save the answers in the ledger, pass them back to the same
run, and let it finish. Scope decisions go into `mission.md` when resolved. If the
answers need discussion, arrange a direct conversation.

### needs_user

Explain the missing information in one or two sentences. Where the host supports an
interactive specialist session, offer `Talk to the agent`, `Answer through me`, or
`Pause`. On `Talk to the agent`, set `conversation: direct`, keep its session and run
ID in state, and say they can return to you anytime. Their next message in that
session starts the interview. Do not start a second agent or ask in parallel.

A later `needs_user` from a conversation already marked `direct` or `relay` is a
progress update. Do not repeat the invitation.

The specialist saves answers and remaining topics as it goes. If the user comes back
lost, read its draft, latest inbox, and ledger. Say what is settled and what remains.
Offer `Continue with the agent`, `Continue through me`, or `Pause`. A status question
is not approval, cancellation, or a reason to restart.

If they choose relay or pause, tell the specialist through the session channel and
wait for it to stop before taking over. If the session is gone, say so and resume
from the saved files in a supported session.

When a delegated run has no writable conversation view, say so and offer `Answer
through me`. Never confuse a read-only inspector with a conversation. If the user
starts talking in a specialist pane without returning here, process its notice,
update state, and let the discussion continue.

### failed

Keep the gate pending. Explain what failed and what was saved. Offer retry, a
supported fallback, or pause. When no report arrives, check the actual pane or task:
a permission prompt and a stopped process need different recovery. A product bug
found by stage 10 is a decision: offer a builder rerun with the failing test as the
brief, or accepting it as a known issue noted in the release checklist.

## Start a mission

Use the design location and version already supplied. Ask only for what is missing.
Default an unnamed release to `v0.1` and say so. Establish where the design is: a
repo folder, share link, screenshots, or the user's description.

Create `docs/roy_mission_control/` with `00_captain/` and the eleven numbered stage
folders from `mission-control`, each with `releases/<version>/`. Add the inbox,
`00_captain/mission.md`, and the release `state.md`, `progress.md`, and
`open_questions.md`. Copy the folder README from the captain skill's
`assets/docs-readme.md`, resolved from the installed plugin path.

Say what will happen: design intake runs now, then product definition, and the first
pause is the product definition unless a question comes up sooner. Then dispatch
design intake in the same turn.

## Run a named stage

Route "run product definition", "review phase 2", or "rerun build" through the stage
table in `mission-control`. The request authorizes that run only; it does not resume
`auto`. Reconcile any active writer or interview first. Missing inputs or a shipped
release get an explanation, not a run.

If the upstream decision gate has not passed, show its result and ask. For other open
checks, explain the exception and record the user's decision without marking the gate
passed. Nothing bypasses G3 for stages 4 onward, and building requires a current
reviewed plan. A rerun reopens its gate and marks affected downstream work stale.

## Phase and release completion

G1 to G4 apply once per release. G5 to G11 apply to every phase. After G11 in `auto`,
print progress and start planning the next phase. In `phase` or `step` mode, pause.

After the last phase's G11, pause. Show `release_checklist.md`, `unit_test_plan.md`,
and the progress table. Ask the user to run the checklist and say whether to ship,
fix something, or add a phase. Do not mark a release shipped because G7 passed.

On `/mission-release <next-version>` or a ship decision, read every phase gate. If
any are open, name them and ask whether to close them or ship with the listed gaps.
Record any exception. Never change a release while a specialist is writing.

Once shipping is accepted, mark the release shipped in `mission.md`, create the next
release's folders, reset gates, mode, and the active handoff, and carry the previous
cut list as candidates. Decisions carry over. Ask whether the design changed. If
unchanged, copy the brief into the new release and record G1 carried forward. Route
through product definition before release scope; complete information may let the
product owner finish without an interview. Shipped folders are read-only.

## User edits

The user's edit wins. On `/mission-sync` or a reported edit, compare the files with
the artifact register. Cosmetic edits invalidate nothing. Scope changes do:

| Edited | Mark stale |
|--------|------------|
| design brief | product definition, inventory, and everything after |
| product definition or feature inventory | release scope and everything after |
| release scope | phases and everything after |
| phases | plans and downstream work for changed phases |
| phase-N plan | reviewed plan, build, review, tests, checklist for N |
| phase-N reviewed plan | build and everything after for N |
| source code | review, test plan, tests, checklist |

Reopen affected gates. If a specialist is working from changed input, notify it and
reconcile its draft. Name any conflict with a recorded decision and ask which
governs. Explain the smallest useful rerun, then run it in `auto` or offer it in
other modes. Stale means unchecked against the change, not wrong.

## Resume

Read `mission.md`, the release `state.md`, `progress.md`, ledger, active inbox, and
relevant drafts. Check the saved specialist session through the matching runtime.
Restore the mode, conversation mode, processed sequence, and any pending acceptance.
Print progress and say the next action without replaying history. An active
interview stays active; a result awaiting a decision still waits. If the mode is
`auto` and nothing is pending or running, continue the run.
