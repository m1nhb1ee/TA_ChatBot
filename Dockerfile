# ============================================================
# Dockerfile — AI TA ChatBot (Streamlit) for Railway
# ============================================================
# Build optimized for:
# - Small image size (~500MB)
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

RUN pip install streamlit

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

# Streamlit configuration - DO NOT set STREAMLIT_SERVER_PORT here
# Let the startup script handle port via command-line argument
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_LOGGER_LEVEL=info
ENV STREAMLIT_CLIENT_SHOWERRORDETAILS=true

# Create startup and health check scripts
RUN mkdir -p /app/startup && \
    # ===== STARTUP SCRIPT =====
    printf '#!/bin/bash\nset -e\necho "========================================="\necho "Starting TA_ChatBot Streamlit Application"\necho "========================================="\necho "Python version: $(python --version)"\necho "Streamlit version: $(streamlit --version)"\necho ""\n\n# Use PORT from environment, default to 8501 if not set\nexport PORT=${PORT:-8501}\necho "PORT is set to: $PORT"\necho "PYTHONPATH: $PYTHONPATH"\n\nif [ -z "$OPENAI_API_KEY" ]; then\n    echo "⚠️  WARNING: OPENAI_API_KEY is NOT set"\n    echo "   Please set OPENAI_API_KEY on Railway dashboard"\n    echo ""\nfi\n\necho "Starting Streamlit on port $PORT"\necho "========================================="\necho ""\n\nexec streamlit run app.py \\\n  --server.port=$PORT \\\n  --server.address=0.0.0.0 \\\n  --logger.level=info \\\n  --client.showErrorDetails=true\n' > /app/startup/entrypoint.sh && \
    chmod +x /app/startup/entrypoint.sh && \
    # ===== HEALTH CHECK SCRIPT =====
    printf '#!/bin/bash\nPORT=${PORT:-8501}\necho "Checking health on port $PORT"\npython -c "import requests; resp = requests.get(\"http://localhost:$PORT/_stcore/health\", timeout=5); resp.raise_for_status()"\n' > /app/startup/healthcheck.sh && \
    chmod +x /app/startup/healthcheck.sh

# ============================================================
# HEALTHCHECK
# ============================================================
# Use separate health check script that properly handles PORT variable
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /app/startup/healthcheck.sh

# ============================================================
# START COMMAND
# ============================================================
CMD ["/app/startup/entrypoint.sh"]

