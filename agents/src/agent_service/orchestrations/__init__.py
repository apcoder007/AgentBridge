"""Agent orchestration builders sharing one centrally configured model."""

from collections.abc import Callable

from agent_service.config import Settings, get_settings
from agent_service.llm import create_chat_model
from agent_service.orchestrations.joke import build_agent as build_joke_agent

AgentHandler = Callable[[str], str]
OrchestrationBuilder = Callable[..., AgentHandler]

ORCHESTRATION_BUILDERS: dict[str, OrchestrationBuilder] = {"joke": build_joke_agent}


def build_orchestrations(settings: Settings | None = None) -> dict[str, AgentHandler]:
    """Build registered orchestrations using one shared configured model instance.

    Register future workflows in ``ORCHESTRATION_BUILDERS``. Each builder gets
    the same ``model`` instance and returns a handler accepting a message string
    and returning a response string.
    """

    resolved_settings = settings or get_settings()
    model = create_chat_model(resolved_settings)
    return {
        name: build_graph(model=model)
        for name, build_graph in ORCHESTRATION_BUILDERS.items()
    }


__all__ = ["ORCHESTRATION_BUILDERS", "build_orchestrations"]
