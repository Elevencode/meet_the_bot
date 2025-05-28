"""
API routes for the backend service.
Handles Google Meet link generation and meeting information.
"""

import logging
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel

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
        "status": "online",
        "endpoints": [
            "GET /ping - Health check",
            "POST /create-meet-link - Create Google Meet link", 
            "GET /meet/{meeting_code} - Get meeting information"
        ],
        "description": "Simple Google Meet link generator for Telegram bot"
    }


@router.get("/ping")
async def ping() -> Dict[str, str]:
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"message": "pong", "status": "healthy"}


@router.post("/create-meet-link")
async def create_meet_link(request: CreateMeetRequest = None) -> Dict[str, Any]:
    """
    Create a new Google Meet link.
    
    Returns:
        Dict containing meeting information and link
    """
    try:
        logger.info("Google Meet link generation requested")
        
        # Use default empty request if none provided
        if request is None:
            request = CreateMeetRequest()
        
        meet_service = get_meet_service()
        result = meet_service.create_meeting_link(
            summary=request.summary,
            description=request.description,
            duration_minutes=request.duration_minutes
        )
        
        if result['success']:
            logger.info("Google Meet link generated successfully")
            return result
        else:
            logger.error(f"Failed to generate Google Meet link: {result.get('error')}")
            raise HTTPException(status_code=500, detail="Failed to create Google Meet link")
            
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        logger.error(error_message)
        return {
            "success": False,
            "error": "Failed to create Google Meet link"
        }


@router.get("/meet/{meeting_code}")
async def get_meeting_info(meeting_code: str) -> Dict[str, Any]:
    """
    Get information about a meeting by its code.
    
    Args:
        meeting_code: The meeting code (e.g., 'abc-defg-hij')
        
    Returns:
        Dict containing meeting information
    """
    try:
        logger.info(f"Meeting info requested for code: {meeting_code}")
        
        meet_service = get_meet_service()
        result = meet_service.get_meeting_info(meeting_code)
        
        if result['success']:
            logger.info("Meeting info retrieved successfully")
            return result
        else:
            logger.error(f"Failed to get meeting info: {result.get('error')}")
            raise HTTPException(status_code=404, detail="Meeting not found")
            
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail="Failed to get meeting info") 