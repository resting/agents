# /// script
# requires-python = ">=3.12"
# dependencies = ["pyte==0.8.2"]
# ///
"""Read account allowances without making a model request. Exit 2 means pause."""

import argparse
import json
import math
import os
import re
import selectors
import subprocess
import sys
import time
from pathlib import Path

THRESHOLD = 95
MAX_AGE = 120


def number(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def result(runtime, windows, problems=()):
    problems = list(problems)
    reached = any(window["used_percent"] >= THRESHOLD for window in windows)
    return {
        "status": "paused_usage"
        if reached
        else "usage_unknown"
        if problems or not windows
        else "ok",
        "runtime": runtime,
        "checked_at": time.time(),
        "threshold_used_percent": THRESHOLD,
        "source": "claude /usage"
        if runtime == "claude"
        else "codex account rate limits",
        "windows": windows,
        "problems": problems or ([] if windows else ["No usable allowance windows"]),
    }


def window(name, raw, percent_key, reset_key, now):
    if not isinstance(raw, dict):
        raise TypeError(f"Missing allowance window: {name}")
    used, resets = raw.get(percent_key), raw.get(reset_key)
    if not number(used) or used < 0:
        raise ValueError(f"Invalid usage percentage: {name}")
    if resets is not None and (not number(resets) or resets <= now):
        raise ValueError(f"Expired or invalid reset time: {name}")
    return {
        "name": name,
        "used_percent": used,
        "remaining_percent": max(0, 100 - used),
        "resets_at": resets,
    }


def codex_usage(payload, limit_ids=(), now=None):
    now = time.time() if now is None else now
    buckets = payload.get("rateLimitsByLimitId")
    if not isinstance(buckets, dict) or not buckets:
        legacy = payload.get("rateLimits")
        buckets = (
            {legacy.get("limitId") or "codex": legacy}
            if isinstance(legacy, dict)
            else {}
        )
    selected = list(limit_ids) or list(buckets)
    windows, problems = [], []
    for name in selected:
        bucket = buckets.get(name)
        if not isinstance(bucket, dict):
            problems.append(f"Missing allowance bucket: {name}")
            continue
        if bucket.get("spendControlReached") or bucket.get("rateLimitReachedType"):
            windows.append(
                {
                    "name": f"{name}/reached",
                    "used_percent": 100,
                    "remaining_percent": 0,
                    "resets_at": None,
                }
            )
        count = len(windows)
        for key in ("primary", "secondary"):
            if bucket.get(key) is None:
                continue
            try:
                item = window(
                    f"{name}/{key}", bucket[key], "usedPercent", "resetsAt", now
                )
                item["window_duration_mins"] = bucket[key].get("windowDurationMins")
                windows.append(item)
            except (ValueError, TypeError) as error:
                problems.append(str(error))
        if len(windows) == count:
            problems.append(f"No percentage allowance in bucket: {name}")
    if payload.get("ordinaryUsageAllowed") is False:
        windows.append(
            {
                "name": "ordinary_usage_blocked",
                "used_percent": 100,
                "remaining_percent": 0,
                "resets_at": None,
            }
        )
    return result("codex", windows, problems)


def codex_read(timeout=15):
    """Use the installed CLI's account and configuration. Never inspect auth files."""
    process = subprocess.Popen(
        ["codex", "app-server", "--listen", "stdio://"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    stdin, stdout = process.stdin, process.stdout
    assert stdin is not None and stdout is not None
    selector = selectors.DefaultSelector()
    selector.register(stdout, selectors.EVENT_READ)
    deadline, pending = time.monotonic() + timeout, b""

    def send(message):
        stdin.write((json.dumps(message) + "\n").encode())
        stdin.flush()

    try:
        send(
            {
                "id": 1,
                "method": "initialize",
                "params": {"clientInfo": {"name": "rmc_usage", "version": "1.0"}},
            }
        )
        while time.monotonic() < deadline:
            if not selector.select(max(0, deadline - time.monotonic())):
                break
            chunk = os.read(stdout.fileno(), 65536)
            if not chunk:
                raise ValueError("Codex usage connection closed")
            pending += chunk
            if len(pending) > 2_000_000:
                raise ValueError("Codex usage response too large")
            while b"\n" in pending:
                line, pending = pending.split(b"\n", 1)
                message = json.loads(line)
                if message.get("id") not in (1, 2):
                    continue
                if "error" in message:
                    raise ValueError("Codex account usage request failed")
                if message["id"] == 1:
                    send({"method": "initialized"})
                    send({"id": 2, "method": "account/rateLimits/read"})
                else:
                    return message["result"]
        raise ValueError("Codex usage request timed out")
    finally:
        selector.close()
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        stdin.close()
        stdout.close()


def claude_usage(screen):
    """Parse the rendered /usage page, never its append-only terminal stream."""
    lower = screen.lower()
    if any(
        word in lower
        for word in (
            "refreshing",
            "loading",
            "failed",
            "error",
            "unable to",
            "could not",
        )
    ):
        return result(
            "claude", [], ["Claude /usage is incomplete or failed to refresh"]
        )
    lines = [line.strip() for line in screen.splitlines() if line.strip()]
    windows, problems = [], []
    for index, line in enumerate(lines):
        if not line.startswith("Current "):
            continue
        if not re.fullmatch(r"Current (session|week(?: \([^)]+\))?)", line):
            problems.append("Unrecognized Claude allowance window")
            continue
        following = lines[index + 1 : index + 3]
        matches = re.findall(
            r"(?<![\d.+-])([\d]+(?:\.[\d]+)?)%\s+used\b",
            following[0] if following else "",
        )
        if (
            len(matches) != 1
            or len(following) < 2
            or not following[1].startswith("Resets ")
        ):
            problems.append(f"Incomplete allowance: {line}")
            continue
        item = window(line, {"used": float(matches[0])}, "used", "reset", time.time())
        item["reset_text"] = following[1]
        windows.append(item)
    names = [item["name"] for item in windows]
    if "Current session" not in names or "Current week (all models)" not in names:
        problems.append("Claude /usage lacks the session or all-model weekly allowance")
    if len(set(names)) != len(names):
        problems.append("Duplicate Claude allowance windows")
    return result("claude", windows, problems)


def claude_read(project_root, timeout=30):
    """Open /usage in a disposable terminal using the local Claude account."""
    import codecs
    import fcntl
    import pty
    import struct
    import termios

    import pyte

    master, slave = pty.openpty()
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 80, 160, 0, 0))
    env = os.environ.copy()
    # This probe runs a built-in command only, never a nested model job.
    env.pop("CLAUDECODE", None)
    env["TERM"] = "xterm-256color"
    process = None
    selector = selectors.DefaultSelector()
    try:
        process = subprocess.Popen(
            ["claude", "--safe-mode", "--ax-screen-reader", "--tools", ""],
            stdin=slave,
            stdout=slave,
            stderr=slave,
            cwd=project_root,
            env=env,
            start_new_session=True,
        )
        os.close(slave)
        slave = None
        selector.register(master, selectors.EVENT_READ)
        screen = pyte.Screen(160, 80)
        stream = pyte.Stream(screen)
        decoder = codecs.getincrementaldecoder("utf-8")("replace")
        deadline = time.monotonic() + timeout
        sent = saw_refresh = False
        refresh_tail = ""
        last_output = time.monotonic()
        while time.monotonic() < deadline:
            if selector.select(min(0.2, max(0, deadline - time.monotonic()))):
                try:
                    chunk = os.read(master, 65536)
                except OSError:
                    break
                if not chunk:
                    break
                decoded = decoder.decode(chunk)
                stream.feed(decoded)
                last_output = time.monotonic()
                if sent:
                    refresh_text = refresh_tail + decoded
                    saw_refresh = saw_refresh or "refreshing" in refresh_text.lower()
                    refresh_tail = refresh_text[-32:]
            rendered = "\n".join(screen.display)
            if any(
                text in rendered.lower()
                for text in ("trust this folder", "enter y/n", "sign in", "log in")
            ):
                return result(
                    "claude",
                    [],
                    ["Open Claude interactively to resolve trust or sign-in first"],
                )
            if not sent and any(
                line.strip() in ("$", "❯", ">") for line in screen.display
            ):
                os.write(master, b"/usage\r")
                sent = True
            if (
                sent
                and saw_refresh
                and time.monotonic() - last_output >= 0.5
                and "refreshing" not in rendered.lower()
                and "Esc to cancel" in rendered
            ):
                reading = claude_usage(rendered)
                reading["project_root"] = str(Path(project_root).resolve())
                return reading
            if process.poll() is not None:
                break
        return result(
            "claude",
            [],
            ["Claude /usage did not finish a verifiable refresh before timeout"],
        )
    finally:
        selector.close()
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        os.close(master)
        if slave is not None:
            os.close(slave)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    codex = commands.add_parser("codex")
    codex.add_argument("--input", type=Path, help="Fresh raw get_usage_limits JSON")
    codex.add_argument("--limit-id", action="append", default=[])
    claude = commands.add_parser("claude")
    claude.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "codex":
            if args.input:
                age = time.time() - args.input.stat().st_mtime
                if age < 0 or age > MAX_AGE:
                    raise ValueError("Codex input is stale; fetch a new reading")
                payload = json.loads(args.input.read_text())
            else:
                payload = codex_read()
            value = codex_usage(payload, args.limit_id)
        else:
            value = claude_read(args.project_root.resolve())
    except ImportError:
        value = result(
            "claude", [], ["Use uv run --script to load the terminal decoder"]
        )
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        value = result(
            args.command,
            [],
            [
                "Usage source unavailable or invalid; preserve work and report to the captain"
            ],
        )
    print(json.dumps(value, indent=2, allow_nan=False))
    return 2 if value.get("status") in ("paused_usage", "usage_unknown") else 0


if __name__ == "__main__":
    sys.exit(main())
