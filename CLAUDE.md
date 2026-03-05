# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**cn-todo** — a two-service todo app:
- `backend/` — FastAPI REST API with an in-memory todo store, serves on port 8000
- `frontend/` — FastAPI server-side app using Jinja2 templates, serves on port 3000

Both services use Python 3.12+ and `uv` for dependency management.

## Development Commands

Run from each service's directory:

```bash
# Install dependencies
uv sync

# Run backend (port 8000)
cd backend && uv run uvicorn main:app --reload

# Run frontend (port 3000)
cd frontend && uv run uvicorn main:app --reload --port 3000
```

The frontend reads `BACKEND_URL` from the environment (default: `http://localhost:8000`).

## Architecture

```
backend/main.py       # FastAPI app: CRUD routes for /todos, in-memory dict store
frontend/main.py      # FastAPI app: single GET / route, renders Jinja2 template
frontend/templates/   # index.html — full UI with vanilla JS that calls the backend API
k8s.yaml              # Kubernetes Deployment + NodePort Service (port 30080 → 8000)
```

**Data flow:** Browser loads `frontend/` → HTML template inlines `backend_url` → JS fetches `/todos` directly from backend API.

**State:** The backend uses a plain in-memory `dict[int, Todo]` — data is lost on restart.

**CORS:** Backend allows only `http://localhost:3000`.

## Kubernetes

`k8s.yaml` deploys a single `cn-todo` container (image: `cn-todo:latest`, `imagePullPolicy: Never`) with NodePort 30080. No Dockerfiles exist yet — the `docker-expert` skill is available to generate them.
