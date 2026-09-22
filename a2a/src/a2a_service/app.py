import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException
import httpx

from a2a_service.agents import AGENTS, AgentDefinition, get_agent

SERVER_URL = os.getenv("A2A_SERVER_URL", "http://127.0.0.1:8003")


app = FastAPI(
    title="Joke Agent A2A Server",
    version="0.1.0",
)


def _agent_card(agent: AgentDefinition) -> dict:
    return {
        "name": agent.name,
        "description": agent.description,
        "url": f"{SERVER_URL}/agents/{agent.id}",
        "version": "0.1.0",
        "capabilities": {"streaming": False, "pushNotifications": False},
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": [
            {
                "id": agent.id,
                "name": agent.skill_name,
                "description": agent.skill_description,
                "tags": ["joke", "humor"],
            }
        ],
    }


@app.get("/.well-known/agent-card.json", tags=["a2a"])
def agent_card() -> dict:
    return _agent_card(get_agent())


@app.get("/agents", tags=["a2a"])
def list_agents() -> dict[str, list[dict]]:
    return {"agents": [_agent_card(agent) for agent in AGENTS.values()]}


@app.get("/agents/{agent_id}/.well-known/agent-card.json", tags=["a2a"])
def named_agent_card(agent_id: str) -> dict:
    try:
        agent = get_agent(agent_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _agent_card(agent)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


def _text_from_message(message: dict) -> str:
    parts = message.get("parts", [])
    text = " ".join(
        part.get("text", "")
        for part in parts
        if part.get("kind", "text") == "text"
    ).strip()
    if not text:
        raise HTTPException(status_code=400, detail="Message must contain text.")
    return text


def _call_agent_api(agent: AgentDefinition, topic: str) -> str:
    try:
        response = httpx.post(
            f"{agent.backend_url.rstrip('/')}/v1/invoke",
            json={"message": topic},
            timeout=60,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Agent API is unavailable at {agent.backend_url}: {exc}",
        ) from exc

    return str(response.json()["response"])


def _send_message(request: dict, agent: AgentDefinition) -> dict:
    if request.get("jsonrpc") != "2.0" or request.get("method") != "message/send":
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {"code": -32601, "message": "Only message/send is supported."},
        }

    params = request.get("params", {})
    message = params.get("message", {})
    topic = _text_from_message(message)
    joke = _call_agent_api(agent, topic)
    task_id = str(uuid4())
    context_id = message.get("contextId", str(uuid4()))

    return {
        "jsonrpc": "2.0",
        "id": request.get("id"),
        "result": {
            "id": task_id,
            "contextId": context_id,
            "status": {"state": "completed"},
            "artifacts": [
                {
                    "artifactId": str(uuid4()),
                    "name": "joke",
                    "parts": [{"kind": "text", "text": joke}],
                }
            ],
        },
    }


@app.post("/joke", tags=["a2a"])
def send_message(request: dict) -> dict:
    return _send_message(request, get_agent())


@app.post("/agents/{agent_id}", tags=["a2a"])
def send_message_to_agent(agent_id: str, request: dict) -> dict:
    try:
        agent = get_agent(agent_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _send_message(request, agent)
