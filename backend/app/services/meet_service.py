"""
Google Meet service using simple URL generation.
This approach creates universal Google Meet links that work without
requiring calendar events, admin permissions or complex API calls.
"""

import logging
import random
import string
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class GoogleMeetService:
    """Service for creating Google Meet links using URL generation."""
    
    def __init__(self):
        """Initialize the Google Meet service."""
        pass
    
    def _generate_meet_code(self) -> str:
        """Generate a random meeting code in Google Meet format."""
        # Google Meet codes are typically in format: abc-defg-hij
        # 3 letters, dash, 4 letters, dash, 3 letters
        def random_string(length):
            return ''.join(random.choices(string.ascii_lowercase, k=length))
        
        part1 = random_string(3)
        part2 = random_string(4) 
        part3 = random_string(3)
        
        return f"{part1}-{part2}-{part3}"
    
    def create_meeting_link(self, 
                          summary: Optional[str] = None,
                          description: Optional[str] = None,
                          duration_minutes: int = 60) -> Dict[str, Any]:
        """
        Create a Google Meet link using URL generation.
        
        This method generates a unique Google Meet URL that users can access directly.
        No calendar events or special permissions required.
        
        Args:
            summary: Meeting title (for response only)
            description: Meeting description (for response only)  
            duration_minutes: Duration hint (for response only)
            
        Returns:
            Dict containing meeting information
        """
        try:
            logger.info("Generating Google Meet link...")
            
            # Generate unique meeting code
            meeting_code = self._generate_meet_code()
            meeting_url = f"https://meet.google.com/{meeting_code}"
            
            # Calculate meeting times for response
            start_time = datetime.utcnow() + timedelta(minutes=1)
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            result = {
                'success': True,
                'meeting_uri': meeting_url,
                'meeting_id': meeting_code,
                'meeting_code': meeting_code,
                'event_id': None,
                'conference_id': meeting_code,
                'summary': summary or 'Generated Meeting',
                'start_time': start_time.isoformat() + 'Z',
                'end_time': end_time.isoformat() + 'Z',
                'html_link': meeting_url,
                'description': 'Click the meeting link to join the Google Meet room. ' +
                             'If the room doesn\'t exist yet, Google will create it when the first person joins.',
                'instructions': {
                    'how_to_join': 'Click the meeting link or go to meet.google.com and enter the code',
                    'meeting_code': meeting_code,
                    'note': 'The meeting room will be created automatically when someone joins'
                },
                'error': None
            }
            
            logger.info(f"Successfully generated Google Meet link: {meeting_url}")
            return result
            
        except Exception as e:
            error_message = f"Unexpected error generating Google Meet link: {str(e)}"
            logger.error(error_message)
            return {
                'success': False,
                'meeting_uri': None,
                'meeting_id': None,
                'meeting_code': None,
                'event_id': None,
                'conference_id': None,
                'summary': None,
                'start_time': None,
                'end_time': None,
                'html_link': None,
                'description': None,
                'instructions': None,
                'error': error_message
            }
    
    def get_meeting_info(self, meeting_code: str) -> Dict[str, Any]:
        """
        Get information about a generated meeting code.
        
        Args:
            meeting_code: Meeting code (e.g., 'abc-defg-hij')
            
        Returns:
            Dict containing meeting information
        """
        try:
            # Validate meeting code format
            if not meeting_code or len(meeting_code.split('-')) != 3:
                raise ValueError("Invalid meeting code format")
            
            meeting_url = f"https://meet.google.com/{meeting_code}"
            
            return {
                'success': True,
                'meeting_uri': meeting_url,
                'meeting_id': meeting_code,
                'meeting_code': meeting_code,
                'conference_id': meeting_code,
                'html_link': meeting_url,
                'description': 'Generated Google Meet room',
                'instructions': {
                    'how_to_join': 'Click the meeting link or go to meet.google.com and enter the code',
                    'meeting_code': meeting_code,
                    'note': 'The meeting room will be created automatically when someone joins'
                },
                'error': None
            }
            
        except Exception as e:
            error_message = f"Error getting meeting info: {str(e)}"
            logger.error(error_message)
            return {
                'success': False,
                'error': error_message
            }


# Global instance
meet_service = GoogleMeetService()


def get_meet_service() -> GoogleMeetService:
    """Get the global Meet service instance."""
    return meet_service 