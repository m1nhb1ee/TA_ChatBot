# ============================================================
# Dockerfile — TA ChatBot Backend (FastAPI)
# ============================================================
# Optimized for:
# - Small image size
# - Fast startup
# - Non-root security
# - Railway compatibility
# ============================================================

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -d /app appuser

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY . .

# Create app_data directory for storage
RUN mkdir -p app_data && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/home/appuser/.local/lib/python3.11/site-packages:/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# API configuration
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_LOG_LEVEL=info

# Create a startup script with better error handling
RUN mkdir -p /app/startup && \
    printf '#!/bin/bash\nset -e\necho "========================================="\necho "Starting TA_ChatBot Backend API"\necho "========================================="\necho "Python version: $(python --version)"\necho ""\n\n# Use PORT from environment, default to 8000 if not set\nexport PORT=${PORT:-8000}\nexport HOST=${HOST:-0.0.0.0}\necho "PORT is set to: $PORT"\necho "PYTHONPATH: $PYTHONPATH"\n\nif [ -z "$OPENAI_API_KEY" ]; then\n    echo "⚠️  WARNING: OPENAI_API_KEY is NOT set"\n    echo "   Please set OPENAI_API_KEY on Railway dashboard"\n    echo ""\nfi\n\necho "Starting FastAPI server on port $PORT"\necho "========================================="\necho ""\n\nexec uvicorn app:app \\\n  --host $HOST \\\n  --port $PORT \\\n  --log-level info\n' > /app/startup/entrypoint.sh && \
    chmod +x /app/startup/entrypoint.sh && \
    printf '#!/bin/bash\nPORT=${PORT:-8000}\necho "Checking health on port $PORT"\npython -c "import requests; resp = requests.get(\"http://localhost:$PORT/health\", timeout=5); resp.raise_for_status()"\n' > /app/startup/healthcheck.sh && \
    chmod +x /app/startup/healthcheck.sh

# ============================================================
# HEALTHCHECK
# ============================================================
# FastAPI health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /app/startup/healthcheck.sh

# ============================================================
# START COMMAND
# ============================================================
CMD ["/app/startup/entrypoint.sh"]
