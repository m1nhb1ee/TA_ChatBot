# TA ChatBot - Backend API

Backend for the AI Teaching Assistant chatbot, built with **FastAPI** and **LangGraph**.

## Architecture Overview

```
backend/
├── app.py                 # FastAPI main application
├── config.py              # Configuration constants
├── requirements.txt       # Dependencies (FastAPI, LangChain, FAISS)
├── Dockerfile             # Multi-stage production Docker build
├── startup.sh             # Startup script with PORT handling
│
├── agent/
│   ├── __init__.py
│   └── core.py            # LangGraph agent with tools
│
├── api/
│   ├── __init__.py
│   ├── routes.py          # REST API endpoints
│   └── schemas.py         # Pydantic models for requests/responses
│
├── tools/                 # LangChain tools
│   ├── search_materials.py      # Search course materials (RAG)
│   ├── code_analyzer.py         # Analyze C/C++ code errors
│   ├── course_info.py           # Get course information
│   ├── escalation.py            # Escalate to human TA
│   ├── detect_trigger.py        # Detect escalation triggers
│   └── verify_information.py    # Verify info in knowledge base
│
├── rag/                   # Retrieval-Augmented Generation
│   ├── __init__.py
│   ├── retriever.py       # FAISS vector store interface
│   └── indexer.py         # Build FAISS index from knowledge base
│
├── utils/                 # Utilities
│   ├── __init__.py
│   ├── storage.py         # File-based metrics storage
│   └── email_service.py   # Email notifications for escalations
│
├── knowledge_base/        # Course materials (copied from root)
│   ├── course_info.json
│   ├── faq.md
│   ├── slides/            # 7 markdown slides
│   └── code_samples/      # C/C++ code examples
│
└── faiss_index/           # Pre-built FAISS vector index
```

## API Endpoints

### 1. **Chat** - `POST /api/chat`
Send a message to the AI Teaching Assistant.

**Request:**
```json
{
  "message": "Con trỏ là gì?",
  "session_id": "user-123-session-456"  // optional
}
```

**Response:**
```json
{
  "response": "Con trỏ là một biến lưu trữ địa chỉ của một biến khác...",
  "session_id": "user-123-session-456",
  "type": "normal",
  "timestamp": "2026-04-17T10:50:42.123Z"
}
```

Response types:
- `normal`: Standard response
- `code_analysis`: Response contains code analysis
- `escalation`: Issue escalated to human TA

---

### 2. **Course Info** - `GET /api/course-info`
Get course information.

**Response:**
```json
{
  "course_name": "Lập trình C/C++ cơ bản",
  "course_code": "CS101",
  "description": "Khóa học về lập trình C/C++ từ cơ bản",
  "timestamp": "2026-04-17T10:50:42.123Z"
}
```

---

### 3. **Metrics** - `GET /api/metrics`
Get system usage statistics.

**Response:**
```json
{
  "total_conversations": 42,
  "total_messages": 256,
  "uptime_seconds": 3600.0,
  "timestamp": "2026-04-17T10:50:42.123Z"
}
```

---

### 4. **Health Check** - `GET /health`
Check if API is running and dependencies are available.

**Response:**
```json
{
  "status": "healthy",
  "api_version": "1.0.0",
  "timestamp": "2026-04-17T10:50:42.123Z"
}
```

Error (503):
```json
{
  "error": "API Key not configured",
  "detail": "OPENAI_API_KEY environment variable is not set",
  "code": 503,
  "timestamp": "2026-04-17T10:50:42.123Z"
}
```

---

### 5. **Streamlit-compatible Health** - `GET /_stcore/health`
For Railway/Streamlit compatibility.

**Response:**
```json
{
  "status": "ok"
}
```

---

### 6. **API Info** - `GET /`
Get general API information.

**Response:**
```json
{
  "name": "TA ChatBot API",
  "version": "1.0.0",
  "description": "Backend API for AI Teaching Assistant",
  "course": "Lập trình C/C++ cơ bản",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

---

## Running Locally

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Set Environment Variable
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### 3. Start Backend
```bash
cd backend
python app.py
```

The API will be available at `http://localhost:8000`

- **API Docs (Swagger)**: `http://localhost:8000/docs`
- **Alternative Docs (ReDoc)**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

---

## Docker Deployment

### Build Image
```bash
docker build -t ta-chatbot-backend:latest backend/
```

### Run Container
```bash
docker run -d \
  --name ta-chatbot-backend \
  -p 8000:8000 \
  -e PORT=8000 \
  -e OPENAI_API_KEY="sk-your-key-here" \
  ta-chatbot-backend:latest
```

### Check Health
```bash
curl http://localhost:8000/health
docker inspect ta-chatbot-backend --format='{{.State.Health.Status}}'
```

---

## Railway Deployment

### 1. Create Railway Project
```bash
railway login
railway init
```

### 2. Set Environment Variables
```bash
railway variables set OPENAI_API_KEY="sk-your-key-here"
railway variables set PORT=8000
```

### 3. Deploy
```bash
railway deploy
```

Or use Git integration:
```bash
git push origin main  # Railway auto-deploys
```

### 4. Access Deployed API
```
https://your-project.railway.app/
https://your-project.railway.app/docs
https://your-project.railway.app/health
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | >=0.104.0 | Web framework |
| uvicorn | >=0.24.0 | ASGI server |
| pydantic | >=2.0.0 | Data validation |
| langchain | >=0.3.0 | LLM framework |
| langchain-openai | >=0.2.0 | OpenAI integration |
| langgraph | >=0.2.0 | Agentic framework |
| faiss-cpu | >=1.8.0 | Vector similarity search |
| python-dotenv | >=1.0.0 | Environment variables |
| requests | >=2.31.0 | HTTP client |

---

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY          # Required: OpenAI API key (sk-...)
PORT                    # Optional: Server port (default: 8000)
HOST                    # Optional: Server host (default: 0.0.0.0)
```

### Config Constants (backend/config.py)
```python
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0.3
EMBEDDING_MODEL = "text-embedding-3-large"
RETRIEVAL_K = 5  # Number of documents to retrieve
COURSE_NAME = "Lập trình C/C++ cơ bản"
COURSE_CODE = "CS101"
```

---

## Testing

### Test Backend Setup
```bash
cd backend
python test_setup.py
```

Output:
```
Testing Backend Setup...
============================================================
✓ Config loaded successfully
✓ API schemas loaded
✓ FastAPI application created
  - Routes: 10 total
============================================================
✅ Backend structure verified successfully!
```

### Test Endpoints with cURL
```bash
# Health check
curl http://localhost:8000/health

# Course info
curl http://localhost:8000/api/course-info

# Chat (simple query)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "C la gi?"}'

# Metrics
curl http://localhost:8000/api/metrics
```

### Test with Python
```python
import requests

# Chat
response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "Vòng lặp for hoạt động như thế nào?"}
)
print(response.json())

# Health
health = requests.get("http://localhost:8000/health")
print(health.json())
```

---

## Components

### Agent (LangGraph)
- **System Prompt**: Socratic method for teaching
- **Tools**: 6 specialized tools for course knowledge
- **LLM**: GPT-4o with temperature 0.3
- **Features**:
  - Semantic search over course materials
  - C/C++ code error analysis
  - Escalation detection
  - Information verification

### RAG (Retrieval-Augmented Generation)
- **Vector Store**: FAISS (pre-built index)
- **Embeddings**: OpenAI text-embedding-3-large
- **Retrieval**: Top-5 similar documents
- **Sources**: Course slides, code samples, FAQ

### Storage
- **Metrics**: JSON file-based (app_data/)
- **Sessions**: File-based chat history
- **Escalations**: Email notifications

---

## Error Handling

### Common Errors

**503 - OpenAI API Key Not Configured**
```json
{
  "error": "API Key not configured",
  "code": 503
}
```
*Solution*: Set `OPENAI_API_KEY` environment variable

**400 - Empty Message**
```json
{
  "error": "Message cannot be empty",
  "code": 400
}
```
*Solution*: Send non-empty message string

**500 - Internal Server Error**
```json
{
  "error": "Internal server error",
  "detail": "...",
  "code": 500
}
```
*Solution*: Check logs for details

---

## Health Check Details

The backend includes comprehensive health checking:

1. **FastAPI `/health` endpoint**
   - Verifies server is running
   - Checks OpenAI API key
   - Returns uptime

2. **Streamlit-compatible `/_stcore/health`**
   - Used by Railway
   - Lightweight check
   - Returns `{"status": "ok"}`

3. **Docker HEALTHCHECK**
   - Interval: 30 seconds
   - Start period: 60 seconds
   - Retries: 3 attempts
   - Uses separate health check script

---

## Scaling Considerations

### Stateless Design
- No server session state
- Session ID generated per chat
- Metrics stored to disk
- Can run multiple replicas

### Docker Optimization
- Multi-stage build (reduces image size)
- Non-root user for security
- Minimal base image (python:3.11-slim)
- Health checks for orchestration

### Railway Deployment
- Automatic PORT injection
- Restart on failure
- Health-check based recovery
- CORS enabled for cross-origin access

---

## Next Steps

1. ✅ Backend structure and API created
2. ✅ Test setup verification
3. ⏳ **Docker testing** (when daemon available)
4. ⏳ **Frontend creation** (connects to backend API)
5. ⏳ **Integration testing** (end-to-end)
6. ⏳ **Production deployment** (Railway)

---

## Support

For issues or questions, check:
- API Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`
- Logs: Container or terminal output
- Config: `backend/config.py`

---

**Status**: ✅ Backend API ready for testing and deployment
