"""
FastAPI Backend for TA ChatBot
"""

import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import config
from api.routes import router
from api.schemas import HealthCheckResponse, ErrorResponse

# Start time for uptime tracking
START_TIME = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    print("=" * 70)
    print("🚀 Starting TA ChatBot Backend API")
    print("=" * 70)
    print(f"• API Version: {config.API_VERSION}")
    print(f"• Course: {config.COURSE_NAME}")
    print(f"• LLM Model: {config.LLM_MODEL}")
    print(f"• OPENAI_API_KEY: {'✅ SET' if config.OPENAI_API_KEY else '❌ NOT SET'}")
    print("=" * 70)
    print()
    
    yield
    
    print("=" * 70)
    print("🛑 Shutting down TA ChatBot Backend API")
    print("=" * 70)


# Create FastAPI app
app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (configure in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== MIDDLEWARE =====
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log incoming requests."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Log request
    print(f"[{request.method}] {request.url.path} | "
          f"Status: {response.status_code} | "
          f"Time: {process_time:.3f}s")
    
    return response


# ===== HEALTH CHECK =====
@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """Check if API is running and dependencies are available."""
    uptime = time.time() - START_TIME
    
    # Check if OpenAI API key is set
    if not config.OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key not configured"
        )
    
    return HealthCheckResponse(
        status="healthy",
        api_version=config.API_VERSION,
    )


@app.get("/_stcore/health")
async def stcore_health():
    """Streamlit-compatible health check endpoint."""
    uptime = time.time() - START_TIME
    
    # Check if OpenAI API key is set
    if not config.OPENAI_API_KEY:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "reason": "API key not configured"}
        )
    
    return {"status": "ok"}


# ===== ERROR HANDLERS =====
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "code": exc.status_code,
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    print(f"❌ Error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "code": 500,
        }
    )


# ===== INCLUDE ROUTES =====
app.include_router(router, prefix="/api", tags=["API"])


# ===== ROOT ENDPOINT =====
@app.get("/", tags=["Info"])
async def root():
    """API information endpoint."""
    return {
        "name": config.API_TITLE,
        "version": config.API_VERSION,
        "description": config.API_DESCRIPTION,
        "course": config.COURSE_NAME,
        "docs": "/docs",
        "redoc": "/redoc",
    }


# ===== STARTUP MESSAGE =====
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print('\n')
    print(f"🌍 Starting server on {host}:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print(f"🔄 Health check: http://localhost:{port}/health")
    print('\n')
    
    uvicorn.run(app, host=host, port=port)
