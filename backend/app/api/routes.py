"""
API routes for the backend service.
Handles authentication testing and Google Meet link creation.
"""

import logging
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.services.google_auth import get_google_auth_service
from app.services.meet_service import get_meet_service

logger = logging.getLogger(__name__)

router = APIRouter()


class CreateMeetRequest(BaseModel):
    """Request model for creating a Google Meet link."""
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: int = 60


@router.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with API information."""
    return {
        "message": "Google Meet Telegram Bot Backend",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "auth_test": "GET /auth/test - Test Google API authentication",
            "create_meet": "POST /create-meet-link - Create a new Google Meet link",
            "get_meet": "GET /meet/{event_id} - Get meeting information",
            "health": "GET /ping - Health check"
        }
    }


@router.get("/ping")
async def ping() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "message": "pong"}


@router.get("/auth/test")
async def test_google_auth() -> Dict[str, Any]:
    """Test Google API authentication."""
    logger.info("Google authentication test requested")
    
    try:
        auth_service = get_google_auth_service()
        result = auth_service.test_authentication()
        
        if result.get("authenticated"):
            logger.info("Google authentication test successful")
        else:
            logger.warning(f"Google authentication test failed: {result.get('error')}")
        
        return result
        
    except Exception as e:
        logger.error(f"Authentication test error: {e}")
        raise HTTPException(status_code=500, detail=f"Authentication test failed: {str(e)}")


@router.post("/create-meet-link")
async def create_meet_link(request: CreateMeetRequest = None) -> Dict[str, Any]:
    """Create a new Google Meet link via Calendar API."""
    logger.info("Google Meet link creation requested")
    
    try:
        meet_service = get_meet_service()
        
        # Use request data or defaults
        if request:
            result = meet_service.create_meeting_link(
                summary=request.summary,
                description=request.description,
                duration_minutes=request.duration_minutes
            )
        else:
            # Default request
            result = meet_service.create_meeting_link()
        
        if result.get("success"):
            logger.info(f"Successfully created Google Meet link: {result.get('meeting_uri')}")
            return {
                "success": True,
                "meeting_uri": result.get("meeting_uri"),
                "meeting_id": result.get("meeting_id"),
                "event_id": result.get("event_id"),
                "conference_id": result.get("conference_id"),
                "summary": result.get("summary"),
                "start_time": result.get("start_time"),
                "end_time": result.get("end_time"),
                "calendar_link": result.get("html_link"),
                "error": None
            }
        else:
            error_msg = result.get("error", "Unknown error occurred")
            logger.error(f"Failed to create Google Meet link: {error_msg}")
            return {
                "success": False,
                "meeting_uri": None,
                "meeting_id": None,
                "event_id": None,
                "conference_id": None,
                "summary": None,
                "start_time": None,
                "end_time": None,
                "calendar_link": None,
                "error": "Failed to create Google Meet link"
            }
            
    except Exception as e:
        logger.error(f"Meet link creation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create meet link: {str(e)}")


@router.get("/meet/{event_id}")
async def get_meet_info(event_id: str) -> Dict[str, Any]:
    """Get information about an existing meeting."""
    logger.info(f"Meeting info requested for event: {event_id}")
    
    try:
        meet_service = get_meet_service()
        result = meet_service.get_meeting_info(event_id)
        
        if result.get("success"):
            logger.info(f"Successfully retrieved meeting info for: {event_id}")
            return result
        else:
            error_msg = result.get("error", "Unknown error occurred")
            logger.error(f"Failed to get meeting info: {error_msg}")
            raise HTTPException(status_code=404, detail=f"Meeting not found: {error_msg}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get meeting info error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get meeting info: {str(e)}") 