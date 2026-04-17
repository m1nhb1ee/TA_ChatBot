"""
Pydantic schemas for the TA ChatBot API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    """Request schema for /api/chat endpoint."""
    message: str = Field(..., description="User message", min_length=1)
    session_id: Optional[str] = Field(None, description="Optional session ID for continuity")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Con trỏ là gì?",
                "session_id": "user-123-session-456"
            }
        }


class ChatResponse(BaseModel):
    """Response schema for /api/chat endpoint."""
    response: str = Field(..., description="AI response")
    session_id: str = Field(..., description="Session ID for chat continuity")
    type: str = Field("normal", description="Response type: normal, code_analysis, escalation")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Con trỏ là một biến lưu trữ địa chỉ của một biến khác...",
                "session_id": "user-123-session-456",
                "type": "normal",
                "timestamp": "2026-04-17T10:50:42.123Z"
            }
        }


class CourseInfoResponse(BaseModel):
    """Response schema for /api/course-info endpoint."""
    course_name: str
    course_code: str
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "course_name": "Lập trình C/C++ cơ bản",
                "course_code": "CS101",
                "description": "Khóa học về lập trình C/C++ từ cơ bản"
            }
        }


class HealthCheckResponse(BaseModel):
    """Response schema for /health endpoint."""
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    api_version: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-04-17T10:50:42.123Z",
                "api_version": "1.0.0"
            }
        }


class MetricsResponse(BaseModel):
    """Response schema for /api/metrics endpoint."""
    total_conversations: int
    total_messages: int
    uptime_seconds: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_conversations": 42,
                "total_messages": 256,
                "uptime_seconds": 3600.0,
                "timestamp": "2026-04-17T10:50:42.123Z"
            }
        }


class ErrorResponse(BaseModel):
    """Response schema for error responses."""
    error: str
    detail: Optional[str] = None
    code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "API Key not configured",
                "detail": "OPENAI_API_KEY environment variable is not set",
                "code": 503,
                "timestamp": "2026-04-17T10:50:42.123Z"
            }
        }
