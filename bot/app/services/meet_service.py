"""
Service for communicating with the Google Meet backend API.
"""

import logging
import aiohttp
import asyncio
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class MeetService:
    """Service for interacting with the Google Meet backend."""
    
    def __init__(self, backend_url: str):
        """Initialize the meet service.
        
        Args:
            backend_url: URL of the backend API
        """
        self.backend_url = backend_url.rstrip('/')
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=10)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def test_backend(self) -> bool:
        """Test if backend is reachable.
        
        Returns:
            True if backend is reachable, False otherwise
        """
        try:
            session = await self._get_session()
            async with session.get(f"{self.backend_url}/ping") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Backend test successful: {data}")
                    return True
                else:
                    logger.warning(f"Backend test failed with status: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Backend test error: {e}")
            return False
    
    async def create_meeting(self, 
                           summary: Optional[str] = None,
                           description: Optional[str] = None,
                           duration_minutes: int = 60) -> Dict[str, Any]:
        """Create a new Google Meet link.
        
        Args:
            summary: Meeting title (optional)
            description: Meeting description (optional)
            duration_minutes: Meeting duration in minutes
            
        Returns:
            Dict containing meeting information or error
        """
        try:
            session = await self._get_session()
            
            # Prepare request data
            request_data = {
                "summary": summary,
                "description": description,
                "duration_minutes": duration_minutes
            }
            
            # Remove None values
            request_data = {k: v for k, v in request_data.items() if v is not None}
            
            logger.info(f"Creating meeting with data: {request_data}")
            
            # Make API request
            async with session.post(
                f"{self.backend_url}/create-meet-link",
                json=request_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Meeting created successfully: {result.get('meeting_uri')}")
                    return result
                else:
                    error_text = await response.text()
                    logger.error(f"Backend API error {response.status}: {error_text}")
                    return {
                        'success': False,
                        'error': f"Backend API error: {response.status}"
                    }
                    
        except asyncio.TimeoutError:
            logger.error("Timeout while creating meeting")
            return {
                'success': False,
                'error': "Timeout connecting to backend"
            }
        except Exception as e:
            logger.error(f"Error creating meeting: {e}")
            return {
                'success': False,
                'error': f"Network error: {str(e)}"
            }
    
    async def get_meeting_info(self, meeting_code: str) -> Dict[str, Any]:
        """Get information about a meeting.
        
        Args:
            meeting_code: Meeting code (e.g., 'abc-defg-hij')
            
        Returns:
            Dict containing meeting information or error
        """
        try:
            session = await self._get_session()
            
            async with session.get(f"{self.backend_url}/meet/{meeting_code}") as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Meeting info retrieved: {meeting_code}")
                    return result
                elif response.status == 404:
                    logger.warning(f"Meeting not found: {meeting_code}")
                    return {
                        'success': False,
                        'error': "Meeting not found"
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"Backend API error {response.status}: {error_text}")
                    return {
                        'success': False,
                        'error': f"Backend API error: {response.status}"
                    }
                    
        except Exception as e:
            logger.error(f"Error getting meeting info: {e}")
            return {
                'success': False,
                'error': f"Network error: {str(e)}"
            }
    
    async def close(self):
        """Close the HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close() 