# Usage sources

The Codex reader uses Python 3 and its standard library. Claude also uses `pyte`. Resolve its path from the
installed `usage-monitor` skill. Run it in the target checkout, not the plugin cache.
These checks read account usage. Claude may write its normal local runtime state.
Never use context-window percentages, token totals, or session cost as subscription
allowance. Missing subscription data on API billing needs a separately configured
budget source. Until one exists, report `usage_unknown`.

## Codex app

Discover and call the host's `get_usage_limits` tool with an empty argument object.
Prefer `rateLimitsByLimitId`; fall back to `rateLimits` only when the map is absent
or empty. Check `usedPercent` on each returned `primary` and `secondary` window.
At 95 or higher, pause. Also pause if the account reports usage blocked, a reached
limit, or reached spend control. Missing buckets or percentages are unknown.

Use the host's known allowance bucket mapping when available. Otherwise check all
returned buckets conservatively. Do not guess a mapping from model names or choose
only the bucket with the lowest usage. Report any uncertainty to the captain.

The native result can be evaluated directly under these rules. For the helper,
save the decoded JSON object from the tool's text content in a temporary file,
then run the following. Do not save the MCP content wrapper or credentials.

```bash
python3 "<skill-root>/scripts/usage_monitor.py" codex --input "<fresh-json-path>"
```

`--limit-id <id>` can be repeated only for a verified set of applicable buckets.
The helper rejects input files older than two minutes. Never refresh their timestamp
or copy an old reading to make it appear fresh. Remove the temporary raw response
after checking. Store only percentages, window names, check time, and reset times
in mission reports, not the raw account response.

## Codex CLI

When the current session uses the installed local CLI's account and configuration:

```bash
python3 "<skill-root>/scripts/usage_monitor.py" codex
```

This starts a short-lived local `codex app-server`, initializes its documented
protocol, calls `account/rateLimits/read`, and closes the process. It makes no model
request and reads no credential files. The request has a 15-second deadline.
Authentication failures, unsupported auth modes, malformed replies, and timeouts
produce `usage_unknown`. Never launch a second model to ask it about usage.

Do not use this fallback for a remote host or a session with different auth or
configuration overrides. Use that host's native account interface. If there is
none, pause and report the limitation.

Protocol reference: https://developers.openai.com/codex/app-server/

## Claude Code

Use Claude Code's built-in `/usage` command. Each agent runs this probe from the
mission checkout using the same local Claude account as its work session:

```bash
uv run --script "<skill-root>/scripts/usage_monitor.py" claude \
  --project-root "<project-root>"
```

The helper opens a disposable Claude terminal in safe mode with model tools
disabled. It waits for the prompt, sends `/usage`, waits for the page's refresh to
finish, reads the rendered screen, and closes only its own process. It sends no
model work prompt and does not interrupt the captain or a specialist's terminal.
It needs `uv`, Python 3.12+, the installed Claude CLI, and the pinned `pyte` terminal
decoder. `uv` loads the decoder from the script metadata. A missing dependency,
permission denial, or failed invocation means usage is unavailable, not permission
to continue. The PTY reader supports macOS and Linux.

Both native subagents and pane agents can run this read-only probe. The helper
removes `CLAUDECODE` only in its child process so the diagnostic terminal can start
inside Claude. It never uses that terminal for a nested model job. Authentication
and the other environment values stay inherited. Do not use the probe if the
current session has different account or provider overrides from the local CLI.
In that case, the captain must arrange `/usage` in a controlled terminal with the
correct account, or report monitoring unavailable. A model name does not establish
which account pays for its work.

The reader requires a visible refresh cycle. It never accepts the cached page
shown before that refresh. It reconstructs the screen after cursor movements and
line replacements, so a changed percentage replaces the old one. It reads only
allowance sections, including the session, all-model weekly window, and any
model-specific weekly windows. Skill contribution percentages are not allowances.
Reset labels are preserved exactly in `reset_text`; `resets_at` stays null because
`/usage` shows human-readable dates. Do not invent a Unix reset time from those
labels. Show the recorded timezone to the user.

Trust or sign-in prompts, an incomplete page, failed refresh, unknown window
layout, or a 30-second timeout produce `usage_unknown`. The helper never answers
trust prompts or logs in for the user. Resolve these through the ordinary Claude
interface. A shell failure must also follow the checkpoint-and-pause rule.
No status-line configuration or shared snapshots are needed. Never use an older
reading when a fresh command fails. Recheck after switching accounts or hosts.

Verified with live `/usage` on Claude Code 2.1.271 and the helper on 2.1.272.
Terminal layouts may change; unrecognized output pauses rather than guessing.
These checks happen between work steps and cannot interrupt a model request that
is already running. Keep saving progress throughout the job.
