"""
API Routes for TA ChatBot Backend
"""

import uuid
from fastapi import APIRouter, HTTPException
from api.schemas import ChatRequest, ChatResponse, CourseInfoResponse, MetricsResponse
import config
import sys
from pathlib import Path
import json

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.core import stream_chat
from utils.storage import get_metrics, update_metric, save_chat_session

router = APIRouter()


# ===== CHAT ENDPOINT =====
@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with the AI Teaching Assistant.
    
    - **message**: User message (required)
    - **session_id**: Optional session ID for chat continuity
    """
    # Check if OpenAI API key is configured
    if not config.OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    # Validate message
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )
    
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        print(f"\n📨 Incoming message from session {session_id[:8]}...")
        print(f"   Message: {request.message[:50]}...")
        
        # Stream chat response
        response_text = stream_chat(request.message)
        
        # Determine response type
        response_type = "normal"
        if "ESCALATION REPORT" in response_text:
            response_type = "escalation"
        elif "analyzing" in response_text.lower():
            response_type = "code_analysis"
        
        # Save session and update metrics
        save_chat_session(session_id, request.message, response_text)
        update_metric("total_messages", 1)
        
        print(f"✅ Response sent ({len(response_text)} chars)")
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            type=response_type,
        )
        
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat: {str(e)}"
        )


# ===== COURSE INFO ENDPOINT =====
@router.get("/course-info", response_model=CourseInfoResponse, tags=["Course"])
async def get_course_information() -> CourseInfoResponse:
    """Get course information."""
    try:
        # Load course info from JSON
        if not config.COURSE_INFO_PATH.exists():
            raise FileNotFoundError(f"Course info file not found at {config.COURSE_INFO_PATH}")
        
        with open(config.COURSE_INFO_PATH, 'r', encoding='utf-8') as f:
            course_data = json.load(f)
        
        return CourseInfoResponse(
            course_name=config.COURSE_NAME,
            course_code=config.COURSE_CODE,
            description=course_data.get("description", ""),
        )
        
    except Exception as e:
        print(f"❌ Error loading course info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error loading course information: {str(e)}"
        )


# ===== METRICS ENDPOINT =====
@router.get("/metrics", response_model=MetricsResponse, tags=["Metrics"])
async def get_system_metrics() -> MetricsResponse:
    """Get system metrics and statistics."""
    try:
        metrics = get_metrics()
        
        return MetricsResponse(
            total_conversations=metrics.get("total_conversations", 0),
            total_messages=metrics.get("total_messages", 0),
            uptime_seconds=metrics.get("uptime_seconds", 0),
        )
        
    except Exception as e:
        print(f"❌ Error getting metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving metrics: {str(e)}"
        )
