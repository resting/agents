# Progress, coverage, and autonomy

How to state where a mission stands, and how much the captain decides without asking.

## Progress

Stages 1 to 4 run once per release. Stages 5 to 10 repeat per phase. Report progress as a
count of stage-runs, not a percentage. A percentage hides how much a newly split phase adds.

Total stage-runs for a release = 4 + 6 × phase count. Phase count is unknown before G4
passes. Say "phase count not set yet" instead of guessing one.

Stages remaining from the current position:

- On stage 1 to 4: (4 − current stage), plus 6 × phase count once phase count is known.
- On stage 5 to 10, phase P of N: (10 − current stage) + 6 × (N − P).

State it wherever progress comes up: "stage 7 of 10, phase 2 of 4, 13 stage-runs left."
Recompute it. Do not carry a number forward once the current stage or phase count changes.

During stage 7 (build), also give the step the builder is on, read from its own
`phase_N_log.md`. The builder already tracks steps; do not re-derive the count.

## Release coverage

`release_scope.md` splits every candidate feature into this release, a later release, and
the cut list. State that split as a ratio wherever the release comes up, not only at G3:
"5 of 9 features ship in v0.2, 3 move to v0.3, 1 is cut." A feature count with no
denominator does not say whether a release is the whole thing or a slice of it.

Mirror the ratio in `mission.md`'s release table as a `Coverage` column. Recompute it after
`/mission-sync` changes the scope.

## Autonomy modes

Set at `/mission-start`, changed anytime with `/mission-autonomy`. Recorded as `Autonomy` in
`mission.md`, one setting for the whole mission.

| Mode | Stops for | Decides alone |
|------|-----------|----------------|
| `gated` (default) | Every gate | Nothing |
| `checkpoint` | G2, G3, G4, G6, and shipping | G1, G5, G7, G8, G9, G10 |
| `unattended` | `needs_user` and shipping | Every gate, including G2, G3, G4, G6 |

G1, G5, and G7 to G10 are objective: a check passes or it does not. G2, G3, G4, and G6 name
the user directly in their own definition, agreement, confirmation, acceptance, so
`checkpoint` still stops for them. G3 is also the decision point everything downstream is
scoped from; an unattended miss there costs the whole release, not one stage.

`needs_user` stops the mission in every mode. It means a fact nobody wrote down, like who
the audience is, and no mode substitutes a guess for that. Shipping a release stops the
mission in every mode too; it is the one action a later release cannot quietly undo. So
does starting the next release afterward: its goal is the user's to give, not the
captain's to infer from how the last one shipped.

When the captain decides a gate on its own, it still writes the decision, its reason, and
the evidence to `00_captain/releases/<version>/autonomy_log.md` before moving on. Nothing
is hidden, the user just is not asked to approve it first. Read
[the captain operations reference](../../captain/references/operations.md) for what the
captain does in each mode. A later `/mission-sync` or direct edit reopens an autonomous
decision the same as any other gate.
