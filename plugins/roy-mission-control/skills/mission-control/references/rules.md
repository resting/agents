# Mission operating rules

## Rules

1. The captain chooses the next stage and asks the user to accept its predecessor's
   result before proceeding. `go` accepts only a result already presented. For a named
   rerun, follow `/mission-run`; never silently override a gate or active interview.
2. Nothing from stage 4 onward starts before G3 passes. The confirmed scope must cover
   the core job end to end. Building also requires a current reviewed plan.
3. Hand off through saved files. Each agent reads upstream artifacts rather than relying
   on a chat summary. User answers must reach the artifact that needs them.
4. One specialist owns the active stage's work. It never launches the next agent, passes
   gates, or writes the captain's state. The captain reads the result and records it.
5. All agents follow `agent-handoff`. They can write their own stage artifacts, inbox
   report, and relevant ledger rows. The builder and code reviewer may also change
   source as their roles allow. They do not edit another stage's artifacts.
6. Missing information goes to the captain as `blocked` for discrete decisions or
   `needs_user` for a conversation. Any specialist may request a conversation. The user
   can return to the captain for orientation, relay, or pause at any time.
7. Direct conversations save answers and remaining topics so the captain can help.
   Interview completion is `done`, followed by captain review and user acceptance.
   Without an interactive session, the captain relays questions.
8. On judgment calls after product definition, read
   `02_product_owner/releases/<version>/product_definition.md` and cite the principle.
9. Save the inbox report before sending the runtime's completion notification. The captain matches the run and
   sequence and reads the files; a notification alone never changes a gate.
10. A user edit takes precedence. The captain marks affected downstream work stale and
    reopens its gates. Do not accept or build from superseded artifacts.
11. Shipped release folders are read-only. Changes belong in a later release.
