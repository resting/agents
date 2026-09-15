# Portable handoff

Write the checkpoint for an agent with no access to this conversation. Any model
with the required capabilities can take over. The original agent and runtime are
provenance only. Never require its memory, hidden reasoning, or live session.

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

## Runtime and recovery
Required tools, environment setup, and permission needs. List active operations,
their status, and whether the previous writer has stopped. Session or process IDs
are diagnostic only. Explain how to recover if those sessions no longer exist.

## Mission state
Release, stage, phase, original run ID, source role and model, checkpoint path,
inbox path, pending gates, usage reading, pause reason, and user decision still needed.
```

Before reporting, verify that the files exist and that the next action is explicit.
The captain must give the replacement agent this checkpoint and the saved files.
If the next agent uses another checkout, transfer local changes and verify them
before resuming. Missing work is a blocker, not permission to recreate it by guess.

The receiving agent reads the checkpoint and governing instructions, checks the
actual workspace against the saved state, and confirms the old writer has stopped.
It checks usage for its own account and runtime. The captain assigns the stage role
and a new run ID; the replacement may use any suitable model or supported host.
Capabilities and stage file ownership still apply. User approval and a passing
usage check are required before resuming. Continue the first unfinished step and
preserve passed gates and verified work.
