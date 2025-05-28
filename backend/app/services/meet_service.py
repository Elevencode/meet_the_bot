"""
Google Meet service using Google Calendar API.
Since Google Meet API requires domain-wide delegation or user authentication,
we use Calendar API to create events with Meet links instead.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .google_auth import GoogleAuthService

logger = logging.getLogger(__name__)


class GoogleMeetService:
    """Service for creating Google Meet links using Calendar API."""
    
    def __init__(self):
        """Initialize the Google Meet service."""
        self.auth_service = GoogleAuthService()
        self._calendar_service = None
    
    def _get_calendar_service(self):
        """Get authenticated Google Calendar service."""
        if not self._calendar_service:
            credentials = self.auth_service.get_credentials()
            if not credentials:
                raise Exception("Failed to get Google credentials")
            
            self._calendar_service = build('calendar', 'v3', credentials=credentials)
            logger.info("Successfully created Google Calendar API client")
        
        return self._calendar_service
    
    def create_meeting_link(self, 
                          summary: Optional[str] = None,
                          description: Optional[str] = None,
                          duration_minutes: int = 60) -> Dict[str, Any]:
        """
        Create a Google Meet link by creating a calendar event.
        
        Args:
            summary: Event title (optional)
            description: Event description (optional)
            duration_minutes: Duration of the meeting in minutes
            
        Returns:
            Dict containing meeting information
        """
        try:
            logger.info("Creating Google Meet link via Calendar API...")
            
            service = self._get_calendar_service()
            
            # Generate start time (current time + 1 minute to avoid immediate start)
            start_time = datetime.utcnow() + timedelta(minutes=1)
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            # Create event with Google Meet conference
            event = {
                'summary': summary or 'Generated Meeting',
                'description': description or 'Meeting created via Telegram bot',
                'start': {
                    'dateTime': start_time.isoformat() + 'Z',  # 'Z' indicates UTC time
                },
                'end': {
                    'dateTime': end_time.isoformat() + 'Z',
                },
                'conferenceData': {
                    'createRequest': {
                        'requestId': str(uuid.uuid4()),  # Unique request ID
                        'conferenceSolutionKey': {
                            'type': 'hangoutsMeet'
                        }
                    }
                }
            }
            
            # Create the event with conference data
            created_event = service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1  # Required for conference data
            ).execute()
            
            # Extract meeting information
            conference_data = created_event.get('conferenceData', {})
            entry_points = conference_data.get('entryPoints', [])
            
            # Find the video entry point (Google Meet link)
            meeting_url = None
            for entry_point in entry_points:
                if entry_point.get('entryPointType') == 'video':
                    meeting_url = entry_point.get('uri')
                    break
            
            if not meeting_url:
                raise Exception("No Google Meet link found in created event")
            
            result = {
                'success': True,
                'meeting_uri': meeting_url,
                'meeting_id': created_event.get('id'),
                'event_id': created_event.get('id'),
                'conference_id': conference_data.get('conferenceId'),
                'summary': created_event.get('summary'),
                'start_time': created_event.get('start', {}).get('dateTime'),
                'end_time': created_event.get('end', {}).get('dateTime'),
                'html_link': created_event.get('htmlLink'),
                'error': None
            }
            
            logger.info(f"Successfully created Google Meet link: {meeting_url}")
            return result
            
        except HttpError as e:
            error_message = f"Google Calendar API error: {e.resp.status} {e.content.decode()}"
            logger.error(error_message)
            return {
                'success': False,
                'meeting_uri': None,
                'meeting_id': None,
                'event_id': None,
                'conference_id': None,
                'summary': None,
                'start_time': None,
                'end_time': None,
                'html_link': None,
                'error': error_message
            }
        except Exception as e:
            error_message = f"Unexpected error creating Google Meet link: {str(e)}"
            logger.error(error_message)
            return {
                'success': False,
                'meeting_uri': None,
                'meeting_id': None,
                'event_id': None,
                'conference_id': None,
                'summary': None,
                'start_time': None,
                'end_time': None,
                'html_link': None,
                'error': error_message
            }
    
    def get_meeting_info(self, event_id: str) -> Dict[str, Any]:
        """
        Get information about an existing calendar event with Meet link.
        
        Args:
            event_id: Calendar event ID
            
        Returns:
            Dict containing meeting information
        """
        try:
            service = self._get_calendar_service()
            
            event = service.events().get(
                calendarId='primary',
                eventId=event_id
            ).execute()
            
            conference_data = event.get('conferenceData', {})
            entry_points = conference_data.get('entryPoints', [])
            
            meeting_url = None
            for entry_point in entry_points:
                if entry_point.get('entryPointType') == 'video':
                    meeting_url = entry_point.get('uri')
                    break
            
            return {
                'success': True,
                'meeting_uri': meeting_url,
                'meeting_id': event.get('id'),
                'conference_id': conference_data.get('conferenceId'),
                'summary': event.get('summary'),
                'start_time': event.get('start', {}).get('dateTime'),
                'end_time': event.get('end', {}).get('dateTime'),
                'html_link': event.get('htmlLink'),
                'error': None
            }
            
        except HttpError as e:
            error_message = f"Google Calendar API error: {e.resp.status} {e.content.decode()}"
            logger.error(error_message)
            return {
                'success': False,
                'error': error_message
            }
        except Exception as e:
            error_message = f"Unexpected error getting meeting info: {str(e)}"
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