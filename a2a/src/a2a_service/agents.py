from dataclasses import dataclass


@dataclass(frozen=True)
class AgentDefinition:
    id: str
    name: str
    description: str
    skill_name: str
    skill_description: str
    backend_url: str


AGENTS: dict[str, AgentDefinition] = {
    "joke-writer": AgentDefinition(
        id="joke-writer",
        name="LangGraph Joke Agent",
        description="Writes and polishes a joke using a four-node LangGraph workflow.",
        skill_name="Write a joke",
        skill_description="Generate a joke for a supplied topic.",
        backend_url="http://127.0.0.1:8000",
    ),
}

DEFAULT_AGENT_ID = "joke-writer"


def get_agent(agent_id: str = DEFAULT_AGENT_ID) -> AgentDefinition:
    try:
        return AGENTS[agent_id]
    except KeyError as exc:
        raise ValueError(f"Unknown agent: {agent_id}") from exc
