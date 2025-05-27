# Use a multi-stage build to reduce the final image size
FROM python:3.13-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    make \
    gcc \
    libffi-dev \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Copy the application code
COPY ./src /code/src
COPY ./alembic.ini /code/alembic.ini
COPY ./migrations /code/migrations

# Final stage
FROM python:3.13-alpine

WORKDIR /app

# Copy the wheels and application code from the builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
COPY --from=builder /code /app

# Install the Python dependencies
RUN pip install --no-cache /wheels/*

# Copy the pre-start script
COPY ./bash_scripts/pre_start.sh /app/bash_scripts/pre_start.sh

# Ensure the pre-start script is executable
RUN chmod +x /app/bash_scripts/pre_start.sh

# Command to run the pre-start script and then start the FastAPI application
CMD ["/bin/bash", "-c", "/app/bash_scripts/pre_start.sh && uvicorn src.main:app --host 0.0.0.0"]