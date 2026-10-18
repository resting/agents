"""Mission runtime rosters match the agent definitions."""

import re
from pathlib import Path

from tools.adapters.base import load_plugin

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins/roy-mission-control"


def test_claude_runtime_roster_matches_agent_source():
    plugin = load_plugin("roy-mission-control")
    assert plugin is not None

    runtime = (
        PLUGIN / "skills/agent-handoff/references/claude.md"
    ).read_text(encoding="utf-8")
    rows = re.findall(
        r"^\| `([^`]+)` \| ([a-z0-9.-]+) \| ([a-z]+) \|$",
        runtime,
        re.MULTILINE,
    )
    actual = {name: (model, effort) for name, model, effort in rows}
    expected = {
        agent.name: (agent.model, agent.frontmatter["effort"])
        for agent in plugin.agents
    }

    assert actual == expected
