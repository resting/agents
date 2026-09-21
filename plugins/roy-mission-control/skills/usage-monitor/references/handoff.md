# Portable handoff

Write the checkpoint for an agent with no access to this conversation. Any model or
supported runtime with the required role capabilities can take over. The source
runtime, transport, model, account, and session IDs are provenance only. They never
configure the replacement. Never require the source agent's memory, hidden
reasoning, live session, provider, or model family.

Use this outline. Mark unknown or unavailable fields explicitly.

```markdown
# Work handoff

## Objective and constraints
User request, expected outcome, acceptance criteria, scope exclusions, and decisions.

## Workspace and inputs
Repository, branch, base commit, checkout location, and paths to governing
instructions, reviewed plan, source files, and stage artifacts.
Use repository-relative paths for portable references. Absolute paths only identify
the original checkout and must be resolved against the receiving checkout.

## Saved work
Completed steps, changed and untracked files, commits if any, and partial edits.
State whether changes are committed, pushed, or local only. Include a patch or
transfer instructions for local changes before moving to another checkout.
Do not assume a commit contains uncommitted work. Never include secrets.

## Verification
Exact commands, working directory, results, failures, and checks not yet run.
Separate observed results from assumptions. Link saved evidence where available.

## Remaining work
Ordered unfinished steps, blockers, dependencies, and the exact first action.
Include enough context to continue without repeating completed work.

## Source provenance
Original runtime, transport, role, model, account source, checkout, session IDs,
and process IDs. Mark them informational. State whether the previous writer has
stopped. Do not present a source model name, transport, or session as a resume
requirement.

## Resume contract
Required stage role, capabilities, tools, environment setup, permission needs,
prerequisites, and the exact first action. Describe the action by its result, not by
a provider-specific tool call. List active operations and whether each must be
observed, restarted, or ignored. Session and process IDs are diagnostic only.
Explain how to recover when the source runtime or its sessions are unavailable.

## Mission state
Release, stage, phase, original run ID, checkpoint path, inbox path, pending gates,
usage reading, pause reason, and user decision still needed.
```

Before reporting, verify that the files exist and that the next action is explicit.
The captain must give the replacement agent this checkpoint and the saved files.
If the next agent uses another checkout, transfer local changes and verify them
before resuming. Missing work is a blocker, not permission to recreate it by guess.

## Cross-runtime resume

The receiving captain must:

1. Read the checkpoint and governing instructions from saved files. The original
   chat is optional evidence, never a dependency.
2. Confirm the old writer stopped. If the source runtime is unavailable, use the
   checkpoint's stopped state and check the shared workspace for an active writer.
   If this cannot be established, keep the mission paused.
3. Reconcile the repository-relative file list, revision, local diff, untracked
   files, and saved artifacts. Transfer local changes when using another checkout,
   then verify the receiving checkout against the checkpoint.
4. Check usage for the receiving runtime and account. The source account may remain
   over its limit. Its reading explains the pause but does not govern the target.
5. Assign the same stage role through the target runtime's roster. Resolve the
   target model and effort there. Never copy the source model name as configuration.
6. Allocate a new run ID, record the old checkpoint as `resumed_from`, and use new
   target-runtime transport and session IDs.
7. Continue the first unfinished step. Preserve passed gates and verified work.

Capabilities and stage file ownership still apply. User approval and a passing
target usage check are required before resuming.
