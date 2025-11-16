FROM python:3.11-slim

# Prevent tzdata prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install required system packages (small set)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . /app

# Upgrade pip & install Python dependencies
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run uvicorn to serve main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
