# DevOps AI Bot

AI-powered bot that generates code and automatically creates GitHub Pull Requests.

## Features

- AI code generation via OpenAI or Bluesmind
- Automatic fallback to OpenAI if Bluesmind is unavailable
- GitHub branch creation, file commit, and PR opening in one request
- Fully Dockerized

## Stack

- **FastAPI** — REST API framework
- **OpenAI / Bluesmind** — LLM providers
- **GitHub API** — branch & PR automation
- **Docker** — containerized deployment

## Project Structure

```
devops-ai-bot/
├── backend/
│   ├── config.py               # App settings loaded from .env
│   ├── main.py                 # FastAPI app & routes
│   ├── models/
│   │   └── request.py          # Pydantic request/response models
│   └── services/
│       ├── ai_service.py       # Code generation logic
│       ├── llm_adapter.py      # OpenAI / Bluesmind adapter
│       └── github_service.py   # GitHub API integration
├── scripts/
│   └── generate_code.py        # CLI for quick local testing
├── .env.example                # Environment variable template
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Setup

**1. Copy and fill in your environment variables:**

```bash
cp .env.example .env
```

**2. Run with Docker:**

```bash
docker-compose up --build
```

**3. Or run locally:**

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## API

### `POST /generate-pr`

Generates code from a prompt and opens a GitHub PR.

**Request body:**

```json
{
  "prompt": "Create a FastAPI CRUD API for a User model",
  "repo": "my-repo",
  "branch": "ai-generated",
  "filename": "api/users.py",
  "commit_message": "feat: add user CRUD endpoints"
}
```

**Response:**

```json
{
  "pr_url": "https://github.com/owner/my-repo/pull/1",
  "branch": "ai-generated",
  "message": "PR successfully created"
}
```

### `GET /`

Health check — returns `{"status": "ok"}`.

## CLI Testing

Test AI generation locally without hitting the API:

```bash
python -m scripts.generate_code --prompt "Create a FastAPI CRUD API"
```
