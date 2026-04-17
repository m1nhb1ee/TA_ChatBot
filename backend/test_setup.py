#!/usr/bin/env python3
"""
Quick test of backend structure and FastAPI app
"""
import sys
from pathlib import Path

print('Testing Backend Setup...')
print('=' * 60)

# Test 1: Config
try:
    import config
    print('✓ Config loaded successfully')
    print(f'  - Course: {config.COURSE_NAME}')
    print(f'  - API Port: 8000 (default)')
except Exception as e:
    print(f'✗ Config error: {e}')
    sys.exit(1)

# Test 2: API Schemas
try:
    from api.schemas import ChatRequest, ChatResponse
    print('✓ API schemas loaded')
except Exception as e:
    print(f'✗ Schema error: {e}')
    sys.exit(1)

# Test 3: FastAPI app initialization
try:
    from app import app
    print('✓ FastAPI application created')
    print(f'  - Routes: {len(app.routes)} total')
except Exception as e:
    print(f'✗ FastAPI error: {e}')
    sys.exit(1)

print('=' * 60)
print('✅ Backend structure verified successfully!')
print()
print('Next steps:')
print('  1. docker build -t ta-chatbot-backend:latest backend/')
print('  2. docker run -p 8000:8000 -e OPENAI_API_KEY=$KEY ta-chatbot-backend')
print('  3. Visit http://localhost:8000/docs for API documentation')
