"""Allowance checks must never turn missing evidence into permission to continue."""

import json
import os
import runpy
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins/roy-mission-control"
SCRIPT = PLUGIN / "skills/usage-monitor/scripts/usage_monitor.py"
usage = SimpleNamespace(**runpy.run_path(str(SCRIPT)))
NOW = 1000


def claude_screen(session=11, weekly=18):
    return f"""Settings  Status   Config   Usage   Stats
Current session
{session}% {session}% used
Resets 10pm (Asia/Singapore)
Current week (all models)
{weekly}% {weekly}% used
Resets Sep 20 at 10pm (Asia/Singapore)
What's contributing to your limits usage?
84% of your usage came from the plugin roy-mission-control
Usage credits
Usage credits are off
Esc to cancel
"""


@pytest.mark.parametrize(
    "consumed,status",
    [(0, "ok"), (89.99, "ok"), (90, "paused_usage"), (100, "paused_usage")],
)
@pytest.mark.parametrize("which", ["session", "weekly"])
def test_claude_usage_boundary(consumed, status, which):
    assert usage.claude_usage(claude_screen(**{which: consumed}))["status"] == status


@pytest.mark.parametrize(
    "notice",
    [
        "Refreshing…",
        "Loading…",
        "Failed to fetch usage",
        "Error loading usage",
        "Unable to refresh",
    ],
)
def test_claude_refresh_failure_never_uses_cached_values(notice):
    assert usage.claude_usage(claude_screen() + notice)["status"] == "usage_unknown"


def test_claude_missing_or_unrecognized_window_pauses():
    assert usage.claude_usage("Login required")["status"] == "usage_unknown"
    assert (
        usage.claude_usage(
            claude_screen().replace("Current week (all models)", "Current day")
        )["status"]
        == "usage_unknown"
    )
    assert (
        usage.claude_usage(claude_screen().replace("18% 18% used", "unavailable"))[
            "status"
        ]
        == "usage_unknown"
    )
    assert (
        usage.claude_usage(claude_screen().replace("Resets 10pm (Asia/Singapore)", ""))[
            "status"
        ]
        == "usage_unknown"
    )


def test_claude_checks_model_window_and_ignores_contribution_percentages():
    reading = usage.claude_usage(claude_screen())
    assert [item["used_percent"] for item in reading["windows"]] == [11, 18]
    assert reading["windows"][0]["reset_text"] == "Resets 10pm (Asia/Singapore)"
    assert reading["windows"][0]["resets_at"] is None
    extra = (
        "Current week (Sonnet only)\n90% used\nResets Sep 20 at 10pm (Asia/Singapore)\n"
    )
    assert usage.claude_usage(claude_screen() + extra)["status"] == "paused_usage"
    assert usage.claude_usage(claude_screen() * 2)["status"] == "usage_unknown"


def test_expired_codex_reset_cannot_resume():
    payload = codex_payload()
    payload["rateLimitsByLimitId"]["codex"]["primary"]["resetsAt"] = NOW
    assert usage.codex_usage(payload, now=NOW)["status"] == "usage_unknown"


@pytest.mark.parametrize(
    "mode,expected",
    [
        ("success", "ok"),
        ("cached", "usage_unknown"),
        ("failed", "usage_unknown"),
        ("trust", "usage_unknown"),
        ("closed", "usage_unknown"),
    ],
)
def test_claude_probe_refresh_and_cleanup(tmp_path, monkeypatch, mode, expected):
    # The live test covers VT rendering. This test controls terminal events and timeouts.
    class Screen:
        def __init__(self, *_args):
            self.display = []

    class Stream:
        def __init__(self, screen):
            self.screen = screen
            self.buffer = ""

        def feed(self, text):
            self.buffer = (self.buffer + text).split("\f")[-1]
            self.screen.display = self.buffer.splitlines()

    monkeypatch.setitem(
        sys.modules, "pyte", SimpleNamespace(Screen=Screen, Stream=Stream)
    )
    script = tmp_path / "fake_claude.py"
    script.write_text(
        "import sys, time\n"
        f"mode = {mode!r}\n"
        "if mode == 'trust':\n"
        "    print('Do you trust this folder?', flush=True)\n"
        "    time.sleep(10)\n"
        "if mode == 'closed':\n"
        "    sys.exit(0)\n"
        "print('$', flush=True)\n"
        "assert sys.stdin.readline().strip() == '/usage'\n"
        f"page = {claude_screen()!r}\n"
        "print('\\f' + page + ('Refreshing…' if mode != 'cached' else ''), flush=True)\n"
        "time.sleep(0.1)\n"
        "if mode != 'cached':\n"
        "    print('\\f' + page + ('Failed to fetch usage' if mode == 'failed' else ''), flush=True)\n"
        "time.sleep(10)\n"
    )
    real_popen = subprocess.Popen
    processes = []

    def fake_popen(command, **kwargs):
        assert command == ["claude", "--safe-mode", "--ax-screen-reader", "--tools", ""]
        assert "CLAUDECODE" not in kwargs["env"]
        assert kwargs["cwd"] == tmp_path
        process = real_popen([sys.executable, str(script)], **kwargs)
        processes.append(process)
        return process

    monkeypatch.setattr(usage.subprocess, "Popen", fake_popen)
    monkeypatch.setenv("CLAUDECODE", "1")
    reading = usage.claude_read(tmp_path, timeout=1.5)
    assert reading["status"] == expected
    assert processes[0].poll() is not None


def codex_payload(primary=10, secondary=20):
    return {
        "rateLimitsByLimitId": {
            "codex": {
                "primary": {"usedPercent": primary, "resetsAt": 2000},
                "secondary": {"usedPercent": secondary, "resetsAt": 3000},
            }
        }
    }


@pytest.mark.parametrize(
    "consumed,status",
    [
        (0, "ok"),
        (89.99, "ok"),
        (90, "paused_usage"),
        (100, "paused_usage"),
        (103, "paused_usage"),
    ],
)
@pytest.mark.parametrize("which", ["primary", "secondary"])
def test_codex_boundary(consumed, status, which):
    payload = codex_payload()
    payload["rateLimitsByLimitId"]["codex"][which]["usedPercent"] = consumed
    assert usage.codex_usage(payload, now=NOW)["status"] == status


@pytest.mark.parametrize("invalid", [None, True, "90", -1, float("nan"), float("inf")])
def test_invalid_usage_is_unknown(invalid):
    assert (
        usage.codex_usage(codex_payload(invalid), now=NOW)["status"] == "usage_unknown"
    )


def test_codex_prefers_map_and_checks_all_buckets():
    payload = codex_payload()
    payload["rateLimits"] = {"primary": {"usedPercent": 100}}
    assert usage.codex_usage(payload, now=NOW)["status"] == "ok"
    payload["rateLimitsByLimitId"]["other"] = {"primary": {"usedPercent": 90}}
    assert usage.codex_usage(payload, now=NOW)["status"] == "paused_usage"
    assert usage.codex_usage(payload, ["codex"], now=NOW)["status"] == "ok"
    assert usage.codex_usage(payload, ["missing"], now=NOW)["status"] == "usage_unknown"


def test_codex_legacy_missing_and_blocked():
    assert (
        usage.codex_usage({"rateLimits": {"primary": {"usedPercent": 90}}})["status"]
        == "paused_usage"
    )
    assert usage.codex_usage({})["status"] == "usage_unknown"
    assert (
        usage.codex_usage({"ordinaryUsageAllowed": False})["status"] == "paused_usage"
    )
    payload = codex_payload()
    payload["rateLimitsByLimitId"]["codex"]["spendControlReached"] = True
    assert usage.codex_usage(payload, now=NOW)["status"] == "paused_usage"


def test_cli_invalid_and_stale_inputs_pause(tmp_path):
    source = tmp_path / "input.json"
    source.write_text("not json")
    command = [sys.executable, str(SCRIPT), "codex", "--input", str(source)]
    process = subprocess.run(command, capture_output=True, text=True, check=False)
    assert process.returncode == 2
    assert json.loads(process.stdout)["status"] == "usage_unknown"
    source.write_text(json.dumps({"rateLimits": {"primary": {"usedPercent": 90}}}))
    process = subprocess.run(command, capture_output=True, text=True, check=False)
    assert process.returncode == 2
    assert json.loads(process.stdout)["status"] == "paused_usage"
    os.utime(source, (time.time() - 121, time.time() - 121))
    process = subprocess.run(command, capture_output=True, text=True, check=False)
    assert process.returncode == 2
    assert json.loads(process.stdout)["status"] == "usage_unknown"


def test_every_stage_loads_usage_monitor():
    agents = list((PLUGIN / "agents").glob("*.md"))
    assert len(agents) == 11
    for path in agents:
        assert '"roy-mission-control:usage-monitor"' in path.read_text()
        assert "paused_usage" in path.read_text(), path.name
    captain = (PLUGIN / "skills/captain/SKILL.md").read_text()
    assert "usage-monitor" in captain
    assert "For `paused_usage`, `go`" in captain


@pytest.mark.parametrize("reply", ["success", "error", "closed", "timeout"])
def test_codex_protocol_and_process_cleanup(tmp_path, monkeypatch, reply):
    server = tmp_path / "fake_server.py"
    server.write_text(
        "import json, sys, time\n"
        "hello = json.loads(sys.stdin.readline())\n"
        "assert hello['method'] == 'initialize'\n"
        "print(json.dumps({'id': 1, 'result': {}}), flush=True)\n"
        "assert json.loads(sys.stdin.readline())['method'] == 'initialized'\n"
        "request = json.loads(sys.stdin.readline())\n"
        "assert request['method'] == 'account/rateLimits/read'\n"
        f"reply = {reply!r}\n"
        "if reply == 'success':\n"
        "    print(json.dumps({'method': 'unrelated', 'params': {}}), flush=True)\n"
        "    print(json.dumps({'id': 2, 'result': {'rateLimits': {'primary': {'usedPercent': 90}}}}), flush=True)\n"
        "elif reply == 'error':\n"
        "    print(json.dumps({'id': 2, 'error': {'message': 'private diagnostic'}}), flush=True)\n"
        "elif reply == 'timeout':\n"
        "    time.sleep(30)\n"
    )
    real_popen = subprocess.Popen
    processes = []

    def fake_popen(command, **kwargs):
        assert command == ["codex", "app-server", "--listen", "stdio://"]
        process = real_popen([sys.executable, str(server)], **kwargs)
        processes.append(process)
        return process

    monkeypatch.setattr(usage.subprocess, "Popen", fake_popen)
    if reply == "success":
        assert (
            usage.codex_usage(usage.codex_read(timeout=1))["status"] == "paused_usage"
        )
    else:
        with pytest.raises(ValueError) as failure:
            usage.codex_read(timeout=0.2)
        assert "private diagnostic" not in str(failure.value)
    assert processes[0].poll() is not None
    assert processes[0].stdin.closed
    assert processes[0].stdout.closed
