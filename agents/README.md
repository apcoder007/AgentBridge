# LangGraph Joke Agent API

A FastAPI service that orchestrates a four-node LangGraph joke writer:
`generate_joke` -> `check_punchline` -> `improve_joke` -> `polish_joke`.

## Project layout

```text
agents/
├── src/agent_service/
│   ├── api.py                  # FastAPI application and routes
│   ├── config.py               # Central environment-backed settings
│   ├── graph.py                # Backward-compatible joke workflow facade
│   ├── llm/
│   │   └── factory.py          # Shared OpenAI/Anthropic/Groq model factory
│   ├── orchestrations/
│   │   ├── __init__.py         # Workflow registry and shared model injection
│   │   └── joke.py             # Joke-writing LangGraph workflow
│   └── schemas.py              # Request and response models
├── tests/
│   ├── test_api.py
│   └── test_orchestrations.py
├── .env.example
├── pyproject.toml
└── requirements.txt
```

## Setup

```bash
cd agents
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set `LLM_PROVIDER` to `openai`, `anthropic`, or `groq`, then add the matching API key and model in `.env`. For example, `openai` uses `OPENAI_API_KEY` and `OPENAI_MODEL` (GPT); `anthropic` uses `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL` (Claude). Without the selected provider's key, the service uses a deterministic local workflow so development works without external services.

All workflows are registered in `agent_service.orchestrations` and receive the same model instance created by `agent_service.llm.factory` from the shared settings. To add another workflow, place its graph builder in `orchestrations/` and register it in `build_orchestrations`, passing it the existing `model` rather than creating a provider client in the workflow.

## Run

Run the graph directly from the command line:

```bash
python scripts/run_joke.py space travel
```

Or run the FastAPI service:

```bash
uvicorn main:app --app-dir src --reload
```

You can also run `api.py` as a Python module:

```bash
PYTHONPATH=src python -m agent_service.api
```

With the server running, call the endpoint from Python:

```bash
python scripts/call_api.py space travel
```

The existing endpoint defaults to the `joke` agent. Get registered agent IDs from `GET /v1/agents`, then select one in the request body:

```bash
curl -X POST http://127.0.0.1:8000/v1/invoke \
  -H 'content-type: application/json' \
  -d '{"agent_id":"joke","message":"space travel"}'
```

Or select an agent in the URL:

```bash
curl -X POST http://127.0.0.1:8000/v1/agents/joke/invoke \
  -H 'content-type: application/json' \
  -d '{"message":"space travel"}'
```

Add workflows to `ORCHESTRATION_BUILDERS` in `agent_service.orchestrations`. Each builder receives the shared configured model and should return a handler with the `message: str -> response: str` interface. Both invoke routes dispatch to that registered handler; unknown agent IDs return HTTP 404.

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Test

```bash
pytest
```
