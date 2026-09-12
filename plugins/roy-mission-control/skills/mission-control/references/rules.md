# Mission operating rules

1. The captain runs stages in pipeline order and pauses only at decision gates,
   blockers, failures, the end of a release, or when the mode says so. `go` resumes
   from a pause. For a named rerun, follow `/mission-run`; never silently override
   a gate or an active interview.
2. Nothing from stage 4 onward starts before G3 passes. The confirmed scope must
   cover the core job end to end. Building requires a current reviewed plan.
3. Hand off through saved files. Each agent reads upstream artifacts rather than a
   chat summary. User answers must reach the artifact that needs them.
4. One specialist owns the active stage's work. It never launches the next agent,
   passes gates, or writes the captain's state. The captain reads the result and
   records it.
5. All agents follow `agent-handoff`. They write their own stage artifacts, inbox
   report, and ledger rows. The builder, code reviewer, and unit test writer may
   change source as their roles allow. Nobody edits another stage's artifacts.
6. Missing information goes to the captain as `blocked` for discrete decisions or
   `needs_user` for a conversation. Non-blocking questions become recorded
   assumptions and the work continues.
7. Direct conversations save answers and remaining topics so the captain can help.
   Interview completion is `done`, followed by captain review. Without an
   interactive session, the captain relays questions.
8. On a judgment call after product definition, read
   `02_product_owner/releases/<version>/product_definition.md` and cite the principle.
9. Save the inbox report before sending the runtime's completion notification. A
   notification alone never changes a gate.
10. A user edit takes precedence. The captain marks affected downstream work stale
    and reopens its gates. Do not build from superseded artifacts.
11. Shipped release folders are read-only. Changes belong in a later release.
12. The captain rewrites `progress.md` and prints the progress block at every
    transition, whether or not it pauses.
