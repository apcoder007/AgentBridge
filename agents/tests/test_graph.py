from agent_service.config import Settings
from agent_service.graph import invoke_joke


def test_joke_graph_runs_all_requested_nodes_without_provider_credentials():
    result = invoke_joke(
        "hello",
        Settings(openai_api_key=None),
    )

    assert result["steps"] == [
        "generate_joke",
        "check_punchline",
        "improve_joke",
        "polish_joke",
    ]
    assert result["joke"] == (
        "Why did the hello bring a ladder? Because the punchline was on a higher level."
    )
