"""
Google Meet service.
Handles creation and management of Google Meet meeting spaces.
"""

from typing import Optional, Dict, Any
from google.apps import meet_v2
from google.api_core.exceptions import GoogleAPIError

from app.services.google_auth import get_google_auth_service
from app.core.logger import get_logger

logger = get_logger(__name__)


class MeetService:
    """Service for Google Meet API operations."""
    
    def __init__(self):
        self.auth_service = get_google_auth_service()
    
    def create_meeting_space(self) -> Optional[Dict[str, Any]]:
        """
        Create a new Google Meet meeting space.
        
        Returns:
            Dict containing meeting space information or None if failed
        """
        try:
            meet_client = self.auth_service.get_meet_client()
            if not meet_client:
                logger.error("Failed to get Google Meet client")
                return None
            
            # Create a new meeting space
            # According to the API docs, we can create an empty space
            request = meet_v2.CreateSpaceRequest()
            
            logger.info("Creating new Google Meet space...")
            space = meet_client.create_space(request=request)
            
            logger.info(f"Successfully created meeting space: {space.name}")
            
            # Extract the meeting URI and other useful information
            meeting_info = {
                "space_name": space.name,
                "meeting_uri": space.meeting_uri,
                "meeting_code": space.meeting_code,
                "config": space.config,
                "active_conference": space.active_conference
            }
            
            return meeting_info
            
        except GoogleAPIError as e:
            logger.error(f"Google Meet API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to create meeting space: {e}")
            return None
    
    def get_meeting_space(self, space_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a meeting space.
        
        Args:
            space_name: The name/ID of the meeting space
            
        Returns:
            Dict containing meeting space information or None if failed
        """
        try:
            meet_client = self.auth_service.get_meet_client()
            if not meet_client:
                logger.error("Failed to get Google Meet client")
                return None
            
            logger.info(f"Fetching meeting space: {space_name}")
            request = meet_v2.GetSpaceRequest(name=space_name)
            space = meet_client.get_space(request=request)
            
            meeting_info = {
                "space_name": space.name,
                "meeting_uri": space.meeting_uri,
                "meeting_code": space.meeting_code,
                "config": space.config,
                "active_conference": space.active_conference
            }
            
            return meeting_info
            
        except GoogleAPIError as e:
            logger.error(f"Google Meet API error when fetching space: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to get meeting space: {e}")
            return None


# Global instance
meet_service = MeetService()


def get_meet_service() -> MeetService:
    """Get the global Meet service instance."""
    return meet_service 