"""
API routes for the backend service.
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.logger import get_logger

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
        "health": "/ping"
    } 