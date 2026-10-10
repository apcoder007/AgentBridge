import pytest
from fastapi.testclient import TestClient

from agent_service import api


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(
        api,
        "build_orchestrations",
        lambda settings: {
            "joke": lambda message: f"joke: {message}",
            "summarizer": lambda message: f"summary: {message}",
        },
    )
    with TestClient(api.app) as test_client:
        yield test_client


def test_list_agents(client):
    response = client.get("/v1/agents")

    assert response.status_code == 200
    assert response.json() == {"agents": [{"id": "joke"}, {"id": "summarizer"}]}


def test_invoke_selects_agent_from_request(client):
    response = client.post(
        "/v1/invoke",
        json={"agent_id": "summarizer", "message": "some text"},
    )

    assert response.status_code == 200
    assert response.json() == {"response": "summary: some text"}


def test_invoke_named_agent_route(client):
    response = client.post(
        "/v1/agents/summarizer/invoke",
        json={"message": "some text"},
    )

    assert response.status_code == 200
    assert response.json() == {"response": "summary: some text"}


def test_invoke_returns_404_for_unknown_agent(client):
    response = client.post(
        "/v1/invoke",
        json={"agent_id": "missing", "message": "some text"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Unknown agent: missing"}
