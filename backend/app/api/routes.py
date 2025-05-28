"""
API routes for the backend service.
"""

from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.logger import get_logger
from app.services.google_auth import get_google_auth_service
from app.services.meet_service import get_meet_service

logger = get_logger(__name__)

# Create API router
router = APIRouter()


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    timestamp: datetime
    service: str
    version: str


class ErrorResponse(BaseModel):
    """Response model for error responses."""
    error: str
    message: str
    timestamp: datetime


class AuthTestResponse(BaseModel):
    """Response model for authentication test endpoint."""
    authenticated: bool
    service_account_file_exists: bool
    credentials_loaded: bool
    meet_client_created: bool
    error: Optional[str] = None


class MeetingResponse(BaseModel):
    """Response model for meeting creation endpoint."""
    success: bool
    meeting_uri: Optional[str] = None
    meeting_code: Optional[str] = None
    space_name: Optional[str] = None
    error: Optional[str] = None


@router.get("/ping", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Service status and metadata
    """
    logger.info("Health check requested")
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        service="meet_the_bot_backend",
        version="1.0.0"
    )


@router.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint with basic service information.
    
    Returns:
        Dict[str, str]: Basic service information
    """
    logger.info("Root endpoint accessed")
    
    return {
        "service": "Google Meet Telegram Bot Backend",
        "status": "running",
        "docs": "/docs",
        "health": "/ping",
        "auth_test": "/auth/test",
        "create_meeting": "/create-meet-link"
    }


@router.get("/auth/test", response_model=AuthTestResponse)
async def test_google_auth() -> AuthTestResponse:
    """
    Test Google API authentication.
    
    Returns:
        AuthTestResponse: Authentication test results
    """
    logger.info("Google authentication test requested")
    
    auth_service = get_google_auth_service()
    result = auth_service.test_authentication()
    
    return AuthTestResponse(**result)


@router.post("/create-meet-link", response_model=MeetingResponse)
async def create_meet_link() -> MeetingResponse:
    """
    Create a new Google Meet link.
    
    Returns:
        MeetingResponse: Meeting creation result with link
    """
    logger.info("Google Meet link creation requested")
    
    meet_service = get_meet_service()
    meeting_info = meet_service.create_meeting_space()
    
    if meeting_info:
        return MeetingResponse(
            success=True,
            meeting_uri=meeting_info.get("meeting_uri"),
            meeting_code=meeting_info.get("meeting_code"),
            space_name=meeting_info.get("space_name")
        )
    else:
        return MeetingResponse(
            success=False,
            error="Failed to create Google Meet link"
        ) 