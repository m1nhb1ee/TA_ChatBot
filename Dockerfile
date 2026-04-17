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
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Streamlit configuration
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_LOGGER_LEVEL=info
ENV STREAMLIT_CLIENT_SHOWERRORDETAILS=true

# Create a startup script with better error handling
RUN mkdir -p /app/startup && \
    printf '#!/bin/bash\nset -e\necho "========================================="\necho "Starting TA_ChatBot Streamlit Application"\necho "========================================="\necho "Python version: $(python --version)"\necho "Streamlit version: $(streamlit --version)"\necho ""\n\nif [ -z "$OPENAI_API_KEY" ]; then\n    echo "⚠️  WARNING: OPENAI_API_KEY environment variable is NOT set"\n    echo "   The application will start but the chatbot will not function"\n    echo "   Please set OPENAI_API_KEY environment variable on Railway"\n    echo ""\nfi\n\necho "Starting Streamlit server on port $PORT"\necho "========================================="\necho ""\n\nexec streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --logger.level=info --client.showErrorDetails=true\n' > /app/startup/entrypoint.sh && \
    chmod +x /app/startup/entrypoint.sh

# ============================================================
# HEALTHCHECK
# ============================================================
# Streamlit health check - wait for startup period before checking
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; resp = requests.get('http://localhost:${STREAMLIT_SERVER_PORT}/_stcore/health', timeout=5); resp.raise_for_status()" || exit 1

# ============================================================
# START COMMAND
# ============================================================
# Use startup script for better error handling and logging
CMD ["/app/startup/entrypoint.sh"]

