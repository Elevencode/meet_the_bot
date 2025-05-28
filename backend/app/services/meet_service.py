"""
Google Meet service using Google Calendar API.
This approach creates Google Meet links by creating calendar events.
"""

import logging
import uuid
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.config import get_settings

logger = logging.getLogger(__name__)

# Scopes required for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

class GoogleMeetService:
    """Service for creating Google Meet links using Google Calendar API."""

    def __init__(self):
        """Initialize the Google Meet service."""
        self.settings = get_settings()
        self.credentials = self._get_credentials()
        if self.credentials:
            try:
                self.calendar_service = build('calendar', 'v3', credentials=self.credentials)
                logger.info("Google Calendar service initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to build Google Calendar service: {e}")
                self.calendar_service = None
        else:
            self.calendar_service = None
            logger.error("Google Calendar service could not be initialized due to missing credentials.")

    def _get_credentials(self) -> Optional[service_account.Credentials]:
        """Load service account credentials from the JSON key file."""
        if not self.settings.google_service_account_path:
            logger.error("Path to Google service account JSON key is not configured.")
            return None
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.settings.google_service_account_path, scopes=SCOPES
            )
            
            # Add impersonation - service account needs to impersonate a real user
            # to create Google Meet links. You need to replace this with a real email
            # that has granted domain-wide delegation to this service account
            impersonation_email = self.settings.google_impersonation_email
            
            if impersonation_email:
                creds = creds.with_subject(impersonation_email)
                logger.info(f"Service account credentials loaded with impersonation: {impersonation_email}")
            else:
                logger.warning("No impersonation email configured. Service account may not be able to create Meet links.")
                logger.info("Service account credentials loaded without impersonation")
            
            return creds
        except FileNotFoundError:
            logger.error(f"Service account key file not found at: {self.settings.google_service_account_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading service account credentials: {e}")
            return None

    def create_meeting_link(
        self,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        duration_minutes: int = 60,
        attendees: Optional[list[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a Google Meet link by creating an event in Google Calendar.

        Args:
            summary: Meeting title.
            description: Meeting description.
            duration_minutes: Duration of the meeting in minutes.
            attendees: List of attendee email addresses.

        Returns:
            Dict containing meeting information or error.
        """
        if not self.calendar_service:
            return {
                'success': False,
                'error': "Google Calendar service is not initialized. Check credentials and configuration."
            }

        logger.info(f"Attempting to create Google Calendar event for Meet link. Summary: {summary}")

        now = datetime.utcnow()
        start_time = (now + timedelta(minutes=2)).isoformat() + 'Z'  # Start in 2 mins
        end_time = (now + timedelta(minutes=2 + duration_minutes)).isoformat() + 'Z'

        event_summary = summary or "New Google Meet"
        event_description = description or "Google Meet created by Telegram Bot."

        event_body = {
            'summary': event_summary,
            'description': event_description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': str(uuid.uuid4()), # Unique ID for the meet creation request
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            },
            'attendees': [] # [{'email': email} for email in attendees] if attendees else []
            # Using 'primary' calendar for the service account.
            # If you want to use a specific calendar, you can add calendarId here.
            # e.g., calendarId='your_specific_calendar_id@group.calendar.google.com'
        }
        
        # Add attendees if provided
        if attendees:
            event_body['attendees'] = [{'email': email} for email in attendees]

        logger.info(f"Creating event with body: {json.dumps(event_body, indent=2)}")
        try:
            created_event = self.calendar_service.events().insert(
                calendarId='primary', # Use 'primary' for the authenticated user's main calendar
                body=event_body,
                conferenceDataVersion=1
            ).execute()

            meeting_url = created_event.get('hangoutLink')
            meeting_id = created_event.get('id')
            conference_id = None
            if created_event.get('conferenceData') and created_event['conferenceData'].get('conferenceId'):
                 conference_id = created_event['conferenceData']['conferenceId']


            if not meeting_url:
                logger.error("Failed to create Google Meet link: 'hangoutLink' not found in Calendar event response.")
                return {
                    'success': False,
                    'error': "Could not retrieve Google Meet link from Calendar event."
                }

            logger.info(f"Successfully created Google Meet link: {meeting_url}")
            return {
                'success': True,
                'meeting_uri': meeting_url,
                'meeting_id': meeting_id, # Calendar event ID
                'meeting_code': conference_id or meeting_url.split('/')[-1], # Use conference ID if available
                'event_id': meeting_id,
                'conference_id': conference_id,
                'summary': created_event.get('summary'),
                'start_time': created_event.get('start', {}).get('dateTime'),
                'end_time': created_event.get('end', {}).get('dateTime'),
                'html_link': created_event.get('htmlLink'), # Link to the calendar event
                'description': created_event.get('description'),
                'error': None
            }

        except HttpError as e:
            error_message = f"HttpError creating Google Calendar event: {e.resp.status} - {e._get_reason()}"
            logger.error(error_message)
            logger.error(f"Error details: {e.content}")
            return {'success': False, 'error': error_message, 'details': e.content.decode()}
        except Exception as e:
            error_message = f"Unexpected error creating Google Calendar event: {str(e)}"
            logger.error(error_message, exc_info=True)
            return {'success': False, 'error': error_message}

    def get_meeting_info(self, meeting_code: str) -> Dict[str, Any]:
        """
        Get information about a Google Meet link (event) by its code or ID.
        For this implementation, 'meeting_code' can be the Calendar Event ID or Conference ID.
        Actual lookup by short meet code (xxx-xxxx-xxx) via Calendar API is not straightforward
        if it wasn't created by this service account.
        This function is a placeholder or needs to be adapted if event_id is used as meeting_code.
        """
        logger.info(f"get_meeting_info called with meeting_code: {meeting_code}")
        # This is a simplified version. To get actual event details, you'd use
        # self.calendar_service.events().get(calendarId='primary', eventId=meeting_code).execute()
        # However, the meeting_code from the bot might be the short xxx-xxxx-xxx code.
        # The Calendar API does not directly resolve these short codes to events unless you know the event creator.
        
        # If the meeting_code is an event ID created by this service:
        if self.calendar_service and '-' not in meeting_code: # Simple check: event IDs usually don't have hyphens like meet codes
            try:
                event = self.calendar_service.events().get(calendarId='primary', eventId=meeting_code).execute()
                return {
                    'success': True,
                    'meeting_uri': event.get('hangoutLink'),
                    'meeting_id': event.get('id'),
                    'meeting_code': event.get('hangoutLink', '').split('/')[-1] if event.get('hangoutLink') else None,
                    'summary': event.get('summary'),
                    'start_time': event.get('start', {}).get('dateTime'),
                    'end_time': event.get('end', {}).get('dateTime'),
                    'html_link': event.get('htmlLink'),
                    'error': None
                }
            except HttpError as e:
                logger.warning(f"Could not retrieve event by ID '{meeting_code}': {e}")
                # Fall through to generic response if ID lookup fails
            except Exception as e:
                logger.warning(f"Unexpected error retrieving event by ID '{meeting_code}': {e}")


        # Fallback for codes that are not event IDs or if lookup failed:
        # Return a generic response as we can't fetch details for an arbitrary meet code
        # without knowing its origin or having Calendar API access to its creator's calendar.
        # The simple URL generation method didn't store details anyway.
        return {
            'success': True, # Or False, depending on how strictly you want to interpret "get_meeting_info"
            'meeting_uri': f"https://meet.google.com/{meeting_code}" if '-' in meeting_code else None,
            'meeting_id': None, # We don't know the event ID for an arbitrary code
            'meeting_code': meeting_code,
            'summary': "Meeting (details not retrievable for arbitrary code)",
            'description': "This link was likely generated directly. No further details stored.",
            'error': "Cannot retrieve detailed information for an arbitrary Meet code not created by this service as an event."
        }


# Global instance
meet_service = GoogleMeetService()

def get_meet_service() -> GoogleMeetService:
    """Get the global Meet service instance."""
    # Ensure the service is initialized, especially if creds might be missing at startup
    # and then added to config later (though less ideal)
    if not meet_service.calendar_service and meet_service.credentials:
        logger.warning("Re-attempting to build Google Calendar service in get_meet_service")
        try:
            meet_service.calendar_service = build('calendar', 'v3', credentials=meet_service.credentials)
            logger.info("Google Calendar service re-initialized successfully in get_meet_service.")
        except Exception as e:
            logger.error(f"Failed to re-build Google Calendar service in get_meet_service: {e}")
            meet_service.calendar_service = None
    elif not meet_service.credentials:
        logger.warning("Credentials not available when get_meet_service was called. Trying to re-load.")
        meet_service.credentials = meet_service._get_credentials()
        if meet_service.credentials and not meet_service.calendar_service:
             logger.info("Credentials re-loaded, attempting to build calendar service.")
             try:
                meet_service.calendar_service = build('calendar', 'v3', credentials=meet_service.credentials)
                logger.info("Google Calendar service built successfully after credential reload.")
             except Exception as e:
                logger.error(f"Failed to build calendar service after credential reload: {e}")
                meet_service.calendar_service = None

    return meet_service 