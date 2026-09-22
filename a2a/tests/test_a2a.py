from fastapi.testclient import TestClient

from a2a_service import app as app_module


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"response": "Why did the space travel bring a ladder?"}


def fake_agent_api_call(*args, **kwargs):
    return FakeResponse()


def test_agent_card_and_message_send():
    app_module.httpx.post = fake_agent_api_call

    with TestClient(app_module.app) as client:
        card = client.get("/.well-known/agent-card.json")
        assert card.status_code == 200
        assert card.json()["name"] == "LangGraph Joke Agent"
        assert card.json()["url"] == "http://127.0.0.1:8003/agents/joke-writer"

        agents = client.get("/agents")
        assert agents.status_code == 200
        assert [agent["name"] for agent in agents.json()["agents"]] == [
            "LangGraph Joke Agent"
        ]

        named_card = client.get(
            "/agents/joke-writer/.well-known/agent-card.json"
        )
        assert named_card.status_code == 200

        response = client.post(
            "/agents/joke-writer",
            json={
                "jsonrpc": "2.0",
                "id": "1",
                "method": "message/send",
                "params": {
                    "message": {
                        "messageId": "msg-1",
                        "role": "user",
                        "parts": [{"kind": "text", "text": "space travel"}],
                    }
                },
            },
        )

        body = response.json()
        assert response.status_code == 200
        assert body["result"]["status"]["state"] == "completed"
        assert body["result"]["artifacts"][0]["parts"][0]["text"] == (
            "Why did the space travel bring a ladder?"
        )
