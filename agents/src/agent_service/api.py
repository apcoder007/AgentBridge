from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
import uvicorn

from agent_service.config import get_settings
from agent_service.orchestrations import build_orchestrations
from agent_service.schemas import InvokeRequest, InvokeResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agents = build_orchestrations(get_settings())
    yield


app = FastAPI(
    title="LangGraph Agent API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/agents", tags=["agent"])
def list_agents(http_request: Request) -> dict[str, list[dict[str, str]]]:
    return {"agents": [{"id": agent_id} for agent_id in http_request.app.state.agents]}


def _invoke_agent(agent_id: str, message: str, http_request: Request) -> InvokeResponse:
    agents = http_request.app.state.agents
    try:
        agent = agents[agent_id]
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {agent_id}") from exc

    return InvokeResponse(response=agent(message))


@app.post("/v1/invoke", response_model=InvokeResponse, tags=["agent"])
def invoke(request: InvokeRequest, http_request: Request) -> InvokeResponse:
    return _invoke_agent(request.agent_id, request.message, http_request)


@app.post("/v1/agents/{agent_id}/invoke", response_model=InvokeResponse, tags=["agent"])
def invoke_named_agent(
    agent_id: str,
    request: InvokeRequest,
    http_request: Request,
) -> InvokeResponse:
    return _invoke_agent(agent_id, request.message, http_request)

