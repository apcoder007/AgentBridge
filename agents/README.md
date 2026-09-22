# LangGraph Joke Agent API

A FastAPI service that orchestrates a four-node LangGraph joke writer:
`generate_joke` -> `check_punchline` -> `improve_joke` -> `polish_joke`.

## Project layout

```text
agents/
├── src/agent_service/
│   ├── api.py       # FastAPI application and routes
│   ├── config.py    # Environment-backed settings
│   ├── graph.py     # LangGraph state and agent nodes
│   ├── api.py       # FastAPI application and entry point
│   └── schemas.py   # Request and response models
├── tests/
│   └── test_graph.py
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

Set `OPENAI_API_KEY` in `.env` to use the OpenAI-backed joke writer. Without a key, the service uses a deterministic local workflow so development works without external services.

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

The equivalent HTTP request is:

```bash
curl -X POST http://127.0.0.1:8000/v1/invoke \
  -H 'content-type: application/json' \
  -d '{"message":"space travel"}'
```

Then call it:

```bash
curl -X POST http://127.0.0.1:8000/v1/invoke \
  -H 'content-type: application/json' \
  -d '{"message":"programming"}'
```

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Test

```bash
pytest
```
