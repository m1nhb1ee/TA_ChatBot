#!/bin/bash
set -e

echo "==========================================="
echo "Starting TA_ChatBot Backend API"
echo "==========================================="
echo "Python version: $(python --version)"
echo "FastAPI/Uvicorn starting..."
echo ""

# Use PORT from environment, default to 8000 if not set
export PORT=${PORT:-8000}
export HOST=${HOST:-0.0.0.0}

echo "PORT is set to: $PORT"
echo "HOST is set to: $HOST"

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY is NOT set"
    echo "   Please set OPENAI_API_KEY environment variable"
    echo ""
fi

echo "Starting FastAPI server..."
echo "==========================================="
echo ""

exec uvicorn app:app \
  --host $HOST \
  --port $PORT \
  --log-level info
