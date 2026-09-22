# A2A Joke Agent

This service exposes agents through an A2A-style HTTP adapter. It forwards requests to each registered agent's HTTP API and does not import or run LangGraph directly. Add new agents in `src/a2a_service/agents.py`.

## Run

Install dependencies into the shared environment:

```bash
cd a2a
/Users/abhayprakash/Projects/Learning/myenv/bin/python -m pip install -r requirements.txt
```

Start the A2A server:

```bash
PYTHONPATH=src:../agents/src /Users/abhayprakash/Projects/Learning/myenv/bin/python src/main.py
```

The server listens on `http://127.0.0.1:8003`. Start the joke agent API on port `8000` first.

## Discover the agent

```bash
curl http://127.0.0.1:8003/.well-known/agent-card.json
```

The default card points to the registered `joke-writer` agent. Its namespaced card is also available at:

```text
http://127.0.0.1:8003/agents/joke-writer/.well-known/agent-card.json
```

List all registered agents:

```bash
curl http://127.0.0.1:8003/agents
```

The root card remains the default agent card. Add additional agents to `AGENTS` in `src/a2a_service/agents.py`; each one then gets its own namespaced card and endpoint.

## Send a message

```bash
curl -X POST http://127.0.0.1:8003/agents/joke-writer \
  -H 'content-type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/send",
    "params": {
      "message": {
        "messageId": "msg-1",
        "role": "user",
        "parts": [{"kind": "text", "text": "space travel"}]
      }
    }
  }'
```

The response contains a completed task with the final joke returned by the agent API. The legacy `/joke` route targets the default registered agent.
