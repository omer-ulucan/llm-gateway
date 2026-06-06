# llm-gateway

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

**OpenAI-compatible local LLM inference gateway with MLflow observability.**

Drop-in replacement for the OpenAI API that runs entirely on your machine. Send requests in the standard OpenAI chat format — no API keys, no internet, no data leaving your machine.

## Architecture

```
Client (curl / OpenAI SDK / any app)
        |
        v
POST /v1/chat/completions
        |
        v
  FastAPI + Pydantic
  (request validation)
        |
        v
  llama.cpp (local inference)
  Qwen3.5-2B Q4_K_M
        |
        v
  MLflow (tracing + metrics)
  latency | token_count | response_length
        |
        v
    ChatResponse
```

## Features

- **OpenAI-compatible API** — swap `base_url` in any OpenAI SDK, works out of the box
- **Fully local** — no API costs, no data leaves your machine
- **Lazy model loading** — model loads on first request, cached in memory
- **Pydantic validation** — malformed requests rejected automatically
- **Qwen3.5 reasoning** — hybrid thinking mode, fast responses by default
- **MLflow observability** — request tracing, latency, token count, response length logged per request

## Stack

| Component | Technology |
|-----------|------------|
| API framework | FastAPI + Uvicorn |
| Inference engine | llama.cpp (llama-cpp-python) |
| Model | Qwen3.5-2B Q4_K_M GGUF |
| Validation | Pydantic v2 |
| Observability | MLflow (tracing + metrics) |
| Model hub | HuggingFace Hub |

## Quick Start

### Prerequisites

- Python 3.11+
- HuggingFace account + read token

### Setup

```bash
git clone https://github.com/omer-ulucan/llm-gateway
cd llm-gateway

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### Authenticate with HuggingFace

```bash
huggingface-cli login
```

### Run

Start MLflow first, then the API:

```bash
mlflow ui                    # http://localhost:5000
uvicorn main:app --reload    # http://localhost:8000
```

Model downloads automatically on first request (~1.2GB).

## Usage

### curl

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5",
    "messages": [{"role": "user", "content": "merhaba"}]
  }'
```

### OpenAI Python SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="qwen3.5",
    messages=[{"role": "user", "content": "hello"}]
)

print(response.choices[0].message.content)
```

### Response

```json
{
  "model": "qwen3.5",
  "content": "Hello there! How can I help you?"
}
```

## MLflow Observability

Every request is automatically traced and evaluated. View at `http://localhost:5000`:

| Metric | Description |
|--------|-------------|
| `latency` | End-to-end response time (seconds) |
| `token_count` | Total tokens consumed |
| `response_length` | Response character count |

## Project Structure

```
llm-gateway/
├── main.py          # FastAPI app, endpoints, MLflow tracing
├── model.py         # llama.cpp model loading (lazy)
├── schemas.py       # Pydantic request/response models
├── requirements.txt
└── README.md
```

## Requirements

```
fastapi
uvicorn
llama-cpp-python
pydantic
python-dotenv
huggingface-hub
mlflow
```