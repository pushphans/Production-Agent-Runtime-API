# AI Todo Assistant API

A FastAPI backend for managing personal todos through authenticated REST endpoints and a LangGraph-powered chat endpoint. It uses PostgreSQL, async SQLAlchemy, Alembic migrations, JWT authentication, and a Groq-hosted language model.

## Current functionality

- Register and log in with a password; receive an access token and a stored refresh token.
- Create, list, view, update, and delete todos through authenticated REST endpoints. Todo queries are scoped to the authenticated user.
- Send a natural-language request to the AI chat endpoint. The current agent has a **create-todo tool**; other todo operations are available through REST, not agent tools.
- Manage the `users`, `refresh_tokens`, and `todos` tables with Alembic migrations.

> **Project status:** This is a work in progress. Conversation persistence, streaming, usage telemetry, and agent tools for listing/updating/deleting todos are not implemented. The AI workflow also has a known end-of-conversation routing issue that can result in a 500 response even after a create-todo tool call. Check the todo list before retrying a failed create request.

## Tech stack

| Area | Technology |
| --- | --- |
| API | Python 3.12+, FastAPI, Uvicorn |
| AI | LangChain, LangGraph, Groq (`qwen/qwen3.8-27b`) |
| Database | PostgreSQL, async SQLAlchemy, asyncpg, Alembic |
| Authentication | JWT (PyJWT), Argon2 password hashing (pwdlib) |
| Dependencies | `uv`, `pyproject.toml`, `uv.lock` |

## Getting started

### Prerequisites

- Python 3.12 or newer and [uv](https://docs.astral.sh/uv/).
- A running PostgreSQL database and credentials for a user that can create tables.
- A [Groq API key](https://console.groq.com/keys) for the chat endpoint.

### 1. Install dependencies

From the repository root:

```bash
uv sync
```

### 2. Configure environment variables

Create a `.env` file in the repository root (it is ignored by Git):

```dotenv
DATABASE_URL=postgresql+asyncpg://app_user:your_password@localhost:5432/todo_agent
JWT_SECRET_KEY=replace_with_a_long_random_secret
ACCESS_TOKEN_EXPIRY_IN_MINUTES=30
REFRESH_TOKEN_EXPIRY_IN_DAYS=7
ALGORITHM=HS256
GROQ_API_KEY=replace_with_your_groq_api_key
```

Replace the example credentials and secrets with your own values. The database must exist before running migrations. `alembic/env.py` reads `DATABASE_URL` from the application settings, so the example URL in `alembic.ini` is not used for connections.

### 3. Apply migrations

```bash
uv run alembic upgrade head
```

### 4. Start the API

```bash
uv run uvicorn production_agent_runtime_api.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` for interactive Swagger documentation. `GET /` returns the application status.

## API overview

| Method | Path | Purpose | Bearer token |
| --- | --- | --- | --- |
| `POST` | `/auth/register` | Create a user account | No |
| `POST` | `/auth/login` | Get access and refresh tokens | No |
| `POST` | `/auth/refresh-token` | Get a new access token | Yes |
| `POST` | `/todos/todo` | Create a todo | Yes |
| `GET` | `/todos/todo` | List your todos; supports `page`, `page_size`, `is_completed`, `search_term` | Yes |
| `GET` | `/todos/todo/{todo_id}` | Get one of your todos | Yes |
| `PUT` | `/todos/todo/{todo_id}` | Update one of your todos | Yes |
| `DELETE` | `/todos/todo/{todo_id}` | Delete one of your todos | Yes |
| `POST` | `/ai/chat` | Send a message to the AI assistant | Yes |

To try the endpoints in Swagger, register with a `name`, `email`, and `password`, then log in and use the returned `access_token` in **Authorize**. For example, a chat request body is:

```json
{
  "message": "Create a todo to review the project documentation"
}
```

The refresh-token endpoint currently requires both a valid bearer access token and a `refresh_token` in its request body.

## Repository layout

```text
src/production_agent_runtime_api/
  main.py                 FastAPI app and router registration
  api/routers/             Authentication and todo REST endpoints
  ai/api/routers/          AI chat endpoint
  ai/workflows/            LangGraph agent definition
  ai/tools/                Agent-facing create-todo tool
  core/                    Configuration, database session, security
  models/                  SQLAlchemy models
  schemas/                 Request and response schemas
  services/                Todo database operations
alembic/                   Database migrations
alembic.ini                Alembic configuration
pyproject.toml             Project metadata and dependencies
uv.lock                    Resolved dependency versions
```

## Security and contribution notes

Keep `.env`, database credentials, JWT signing keys, and Groq keys out of Git. The `.gitignore` excludes local environments, generated files, and private configuration; migrations and `uv.lock` are intended to be committed. Before publishing, review `git status` and `git diff --cached --name-only` for unexpected files. A `.gitignore` does not remove secrets that were already committed to Git history.

See [LICENSE](LICENSE) for licensing information.
