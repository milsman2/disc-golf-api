# Builder stage
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project
COPY . /app
RUN uv sync --locked

FROM python:3.13-slim-bookworm
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends postgresql-client \
    gpgv libpam-modules libpam-modules-bin libpam-runtime libpam0g && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder --chown=nonroot:nonroot /app /app
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
USER nonroot
CMD ["/app/.venv/bin/python", "start_app.py"]