"""Usage handoffs remain portable across models and runtimes."""

import re
from pathlib import Path

from tools.adapters.base import load_plugin

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins/roy-mission-control"


def test_portable_handoff_separates_source_provenance_from_target_config():
    handoff = (
        PLUGIN / "skills/usage-monitor/references/handoff.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(handoff.split())

    required = [
        "## Source provenance",
        "## Resume contract",
        "## Cross-runtime resume",
        "The source account may remain over its limit",
        "Never copy the source model name as configuration",
        "record the old checkpoint as `resumed_from`",
    ]
    for text in required:
        assert text in compact

    report_contract = (PLUGIN / "skills/agent-handoff/SKILL.md").read_text(
        encoding="utf-8"
    )
    for field in ("resume_role", "first_action", "required_capabilities"):
        assert field in report_contract


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
