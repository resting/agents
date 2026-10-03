"""roy-mission-control keeps its Codex model choices explicit."""

from tools.adapters.base import load_plugin


def test_every_rmc_agent_has_the_expected_codex_model():
    plugin = load_plugin("roy-mission-control")
    assert plugin is not None

    expected = {
        "opus": "gpt-6-astra",
        "sonnet": "gpt-6.1-sol",
    }
    assert plugin.agents

    for agent in plugin.agents:
        assert agent.model in expected, f"unexpected Claude tier for {agent.name}"
        assert agent.frontmatter.get("codex-model") == expected[agent.model], agent.name
