from agent_service import orchestrations
from agent_service.config import Settings
from agent_service.orchestrations.joke import build_graph


def test_all_orchestrations_receive_the_same_configured_model(monkeypatch):
    shared_model = object()
    received_models = []

    monkeypatch.setattr(orchestrations, "create_chat_model", lambda settings: shared_model)
    monkeypatch.setattr(
        orchestrations,
        "ORCHESTRATION_BUILDERS",
        {
            "first": lambda *, model: received_models.append(model) or "first-graph",
            "second": lambda *, model: received_models.append(model) or "second-graph",
        },
    )

    built = orchestrations.build_orchestrations(Settings(llm_provider="openai"))

    assert built == {"first": "first-graph", "second": "second-graph"}
    assert received_models == [shared_model, shared_model]


def test_joke_orchestration_runs_without_an_external_model():
    result = build_graph(model=None).invoke({"topic": "hello", "steps": []})

    assert result["steps"] == [
        "generate_joke",
        "check_punchline",
        "improve_joke",
        "polish_joke",
    ]
    assert result["joke"] == (
        "Why did the hello bring a ladder? Because the punchline was on a higher level."
    )
