"""Backward-compatible convenience API for the joke orchestration."""

from agent_service.config import Settings, get_settings
from agent_service.llm import create_chat_model
from agent_service.orchestrations.joke import AgentState
from agent_service.orchestrations.joke import build_graph as build_joke_graph


def build_graph(settings: Settings | None = None):
    """Build the joke graph using the application's centralized model settings."""

    model = create_chat_model(settings or get_settings())
    return build_joke_graph(model=model)


def invoke_agent(message: str, settings: Settings | None = None) -> str:
    graph = build_graph(settings)
    result = graph.invoke({"topic": message, "steps": []})
    return str(result["joke"])


def invoke_joke(message: str, settings: Settings | None = None) -> AgentState:
    """Run the joke graph and return the full state, useful for tests and tracing."""

    graph = build_graph(settings)
    return graph.invoke({"topic": message, "steps": []})
