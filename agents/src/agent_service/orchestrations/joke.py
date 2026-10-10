"""Joke-writing LangGraph orchestration."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    topic: str
    joke: str
    punchline_feedback: str
    steps: list[str]


def _model_text(model, prompt: str) -> str | None:
    if model is None:
        return None

    response = model.invoke(prompt)
    return str(response.content)


def generate_joke(state: AgentState, *, model) -> dict[str, str | list[str]]:
    topic = state["topic"]
    joke = _model_text(
        model,
        f"Write one short joke about {topic}. Include setup and punchline. Return only the joke.",
    )
    if joke is None:
        joke = f"Why did the {topic} bring a ladder? Because the punchline was on another level."

    return {"joke": joke, "steps": [*state.get("steps", []), "generate_joke"]}


def check_punchline(state: AgentState, *, model) -> dict[str, str | list[str]]:
    joke = state["joke"]
    feedback = _model_text(
        model,
        "Review this joke's punchline. Give one concise improvement suggestion, or say "
        f"'ready' if it works:\n\n{joke}",
    )
    if feedback is None:
        feedback = "Make the punchline concise and keep the wordplay clear."

    return {
        "punchline_feedback": feedback,
        "steps": [*state.get("steps", []), "check_punchline"],
    }


def improve_joke(state: AgentState, *, model) -> dict[str, str | list[str]]:
    joke = state["joke"]
    feedback = state["punchline_feedback"]
    improved = _model_text(
        model,
        f"Improve this joke using the feedback below. Return only the revised joke.\n\n"
        f"Joke: {joke}\nFeedback: {feedback}",
    )
    if improved is None:
        improved = joke.replace("another level", "a higher level")

    return {"joke": improved, "steps": [*state.get("steps", []), "improve_joke"]}


def polish_joke(state: AgentState, *, model) -> dict[str, str | list[str]]:
    joke = state["joke"]
    polished = _model_text(
        model,
        "Polish this joke for natural wording and clean punctuation. Return only the final joke.\n\n"
        f"{joke}",
    )
    if polished is None:
        polished = joke.strip()

    return {"joke": polished, "steps": [*state.get("steps", []), "polish_joke"]}


def build_graph(model=None):
    """Build the joke workflow with a model supplied by the shared app configuration."""

    builder = StateGraph(AgentState)
    builder.add_node("generate_joke", lambda state: generate_joke(state, model=model))
    builder.add_node("check_punchline", lambda state: check_punchline(state, model=model))
    builder.add_node("improve_joke", lambda state: improve_joke(state, model=model))
    builder.add_node("polish_joke", lambda state: polish_joke(state, model=model))
    builder.add_edge(START, "generate_joke")
    builder.add_edge("generate_joke", "check_punchline")
    builder.add_edge("check_punchline", "improve_joke")
    builder.add_edge("improve_joke", "polish_joke")
    builder.add_edge("polish_joke", END)
    return builder.compile()


def build_agent(model=None):
    """Build a callable joke agent with the common message-to-response interface."""

    graph = build_graph(model=model)

    def invoke(message: str) -> str:
        result = graph.invoke({"topic": message, "steps": []})
        return str(result["joke"])

    return invoke
