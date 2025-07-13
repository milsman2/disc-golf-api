# Builder stage
FROM python:3.13-slim AS builder

WORKDIR /app

# Install build dependencies and uv
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    make \
    libffi-dev \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

# Copy the application code
COPY ./src /app/src
COPY ./alembic.ini /app/alembic.ini
COPY ./migrations /app/migrations

# Final stage
FROM python:3.13-slim

WORKDIR /app

# Install psql client and uv
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \
    && pip install uv

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy the application code from builder
COPY --from=builder /app/src /app/src
COPY --from=builder /app/alembic.ini /app/alembic.ini
COPY --from=builder /app/migrations /app/migrations

# Copy the pre-start script
COPY ./bash_scripts/pre_start.sh /app/bash_scripts/pre_start.sh

# Ensure the pre-start script is executable
RUN chmod +x /app/bash_scripts/pre_start.sh

# Add the virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Command to run the pre-start script and then start the FastAPI application
CMD ["/bin/bash", "-c", "/app/bash_scripts/pre_start.sh && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000"]