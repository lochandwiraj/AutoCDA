FROM python:3.11-slim

# Prevent tzdata prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# ----------------------------
# INSTALL DEPENDENCIES
# ----------------------------

# Option A: Poetry available (your setup)
RUN pip install --upgrade pip setuptools wheel \
    && pip install poetry

# Copy Poetry config
COPY pyproject.toml poetry.lock* /app/

# Install deps via Poetry (no virtualenv inside container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi || true

# ----------------------------
# COPY PROJECT
# ----------------------------
COPY . /app

# Expose port
EXPOSE 8000

# ----------------------------
# START APP
# ----------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
