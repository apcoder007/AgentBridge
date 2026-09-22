from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
import uvicorn

from agent_service.config import get_settings
from agent_service.graph import build_graph
from agent_service.schemas import InvokeRequest, InvokeResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.graph = build_graph(get_settings())
    yield


app = FastAPI(
    title="LangGraph Agent API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/invoke", response_model=InvokeResponse, tags=["agent"])
def invoke(request: InvokeRequest, http_request: Request) -> InvokeResponse:
    graph = http_request.app.state.graph
    result = graph.invoke({"topic": request.message, "steps": []})
    return InvokeResponse(response=str(result["joke"]))

