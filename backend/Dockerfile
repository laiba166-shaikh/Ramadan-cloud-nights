# Stage 1: resolve and install dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv --no-cache-dir && \
    uv sync --frozen --no-dev --no-install-project

# Stage 2: lean runtime image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser

WORKDIR /app

COPY --from=builder /app/.venv .venv
COPY main.py .

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/todos')" || exit 1

CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
